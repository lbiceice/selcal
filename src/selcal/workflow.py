"""Public file-to-record workflow over the unchanged scientific v2 core.

A terminal record captures input, request and complete result content. It is not
an execution checkpoint, historical authentication or independent validation.
"""

from __future__ import annotations

import hashlib
import html
import json
import platform
import re
import tempfile
from dataclasses import dataclass
from fractions import Fraction
from math import exp, floor, lgamma, log
from pathlib import Path
from typing import Any

import numpy as np

from selcal import (
    __version__,
    calibrate_selected_family,
    resolve_plan_v2,
    verify_calibration_result,
)
from selcal.calibration_v2 import (
    _MAX_IN_MEMORY_CANDIDATE_EVALUATIONS_V2,
    _MAX_IN_MEMORY_REPLICATES_V2,
    _MAX_IN_MEMORY_TOKEN_STATE_UNITS_V2,
    _MAX_IN_MEMORY_WORK_UNITS_V2,
    _require_in_memory_execution_budget_values,
)
from selcal.canonical_v2 import scientific_plan_v2_sha256
from selcal.contracts_v2 import (
    CalibrationResult,
    PlanRequestV2,
    ResourceLimitError,
    SelCalV2Error,
)
from selcal.input_resources import INPUT_LIMITS_V1, read_regular_file_snapshot
from selcal.inputs import LoadedInput, load_csv, load_npz
from selcal.resolution_v2 import PlanResolutionV2
from selcal.result_wire import decode_calibration_result, encode_calibration_result
from selcal.workflow_config import (
    WorkflowConfig,
    WorkflowConfigError,
    decode_workflow_config,
    encode_workflow_config,
)
from selcal.workflow_store import read_record, write_record

CONFIG_BYTES = 65_536


class WorkflowError(ValueError):
    """A path-free application consistency error with a stable code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class WorkflowRecord:
    """Checked terminal content, not a live execution or resume capability."""

    config: WorkflowConfig
    result: CalibrationResult
    metadata: dict[str, Any]


def _limit(max_bytes: int) -> None:
    if type(max_bytes) is not int or max_bytes < 1:
        raise WorkflowError("invalid_limit")


def _json(data: object) -> bytes:
    return (
        json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def _software_identity() -> dict[str, Any]:
    package = Path(__file__).parent
    sources = {}
    for path in sorted(package.rglob("*.py")):
        if path.is_symlink():
            raise WorkflowError("unsupported_source")
        sources[path.relative_to(package).as_posix()] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    if not sources:
        raise WorkflowError("source_unavailable")
    return {
        "selcal_version": __version__,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "source_files": sources,
    }


def _load(path: Path, config: WorkflowConfig) -> LoadedInput:
    if config.source_format == "csv":
        assert config.source_column is not None and config.target_column is not None
        return load_csv(
            path,
            source_column=config.source_column,
            target_column=config.target_column,
            candidates=config.request.candidates,
        )
    return load_npz(path, candidates=config.request.candidates)


def _files(
    input_path: str | Path, config_path: str | Path
) -> tuple[WorkflowConfig, PlanResolutionV2, LoadedInput, bytes]:
    config_bytes = read_regular_file_snapshot(
        config_path, raw_limit=CONFIG_BYTES, reason="WORKFLOW_CONFIG_BYTES"
    )
    config = decode_workflow_config(config_bytes)
    resolution = resolve_plan_v2(config.request)
    loaded = _load(Path(input_path), config)
    raw_limit = (
        INPUT_LIMITS_V1.csv_raw_bytes
        if config.source_format == "csv"
        else INPUT_LIMITS_V1.npz_raw_bytes
    )
    raw = read_regular_file_snapshot(input_path, raw_limit=raw_limit, reason="WORKFLOW_INPUT_BYTES")
    if hashlib.sha256(raw).hexdigest() != loaded.raw_input_sha256:
        raise WorkflowError("input_changed")
    return config, resolution, loaded, raw


def _allowed_exceedances(replicates: int, alpha: float) -> int:
    """Count E in 0..B with (1 + E)/(B + 1) <= alpha, evaluated exactly as the calibrator does."""

    count = max(0, min(replicates + 1, floor(alpha * (replicates + 1))))
    while count > 0 and not count / (replicates + 1) <= alpha:
        count -= 1
    while count <= replicates and (count + 1) / (replicates + 1) <= alpha:
        count += 1
    return count


def _binomial_cdf_below(count: int, trials: int, probability: float) -> float:
    """P(X < count) for X ~ Binomial(trials, probability), in log space: O(count), no underflow."""

    if count <= 0:
        return 0.0
    if count > trials or probability <= 0.0:
        return 1.0
    if probability >= 1.0:
        return 0.0
    log_p, log_q = log(probability), log(1.0 - probability)
    head = lgamma(trials + 1)
    terms = [
        head - lgamma(k + 1) - lgamma(trials - k + 1) + k * log_p + (trials - k) * log_q
        for k in range(count)
    ]
    peak = max(terms)
    return min(1.0, exp(peak) * sum(exp(term - peak) for term in terms))


_SCIENTIFIC_ASSUMPTIONS: dict[str, tuple[tuple[str, str], ...]] = {
    "common": (
        (
            "lags_declared_before_seeing_data",
            "The candidate lag set was fixed before inspecting these data; otherwise the "
            "selection-aware p-value does not cover the extra choice.",
        ),
        (
            "series_aligned_and_sampled_as_supplied",
            "Both columns share one time index and sampling interval; SelCal does not align, "
            "resample, detrend or impute.",
        ),
        (
            "not_causal_inference",
            "A small p-value indicates lagged dependence beyond the null, not causation or an "
            "effect size.",
        ),
    ),
    "circular_shift_v2": (
        (
            "circular_shift_exchangeability",
            "Under the null, circular shifts of the source are exchangeable with the observed "
            "alignment: exact for circular series, approximate for stationary series whose ends "
            "join without a large jump; trends and seasonality should be removed beforehand.",
        ),
    ),
    "block_shuffle_v2": (
        (
            "block_exchangeability",
            "Under the null, source blocks are exchangeable: dependence within the source should "
            "be shorter than the block length.",
        ),
    ),
    "lagged_pearson_v1": (
        (
            "linear_dependence_statistic",
            "Pearson correlation detects linear lagged association; nonlinear dependence may be "
            "missed.",
        ),
    ),
    "equal_width_binned_nette_v1": (
        (
            "binned_estimator_adequacy",
            "The binned transfer-entropy estimate depends on the bin count and sample size.",
        ),
    ),
}


def _declared_assumptions(request: PlanRequestV2) -> list[dict[str, str]]:
    null_key = (
        "circular_shift_v2"
        if request.null_name in {"circular_shift_v2", "circular_shift_exact_v1"}
        else request.null_name
    )
    items = (
        *_SCIENTIFIC_ASSUMPTIONS["common"],
        *_SCIENTIFIC_ASSUMPTIONS.get(null_key, ()),
        *_SCIENTIFIC_ASSUMPTIONS.get(request.statistic_name, ()),
    )
    return [{"code": code, "statement": statement} for code, statement in items]


def _resource_budget(request: PlanRequestV2, sample_count: int) -> dict[str, Any]:
    """Apply the executor's own in-memory admission check without running anything."""

    replicates = request.replicates
    candidates = len(request.candidates)
    state_units: int | None = 1
    if request.null_name == "block_shuffle_v2":
        length = request.null_params.get("block_length")
        state_units = (
            sample_count // length
            if type(length) is int and length > 0 and sample_count % length == 0
            else None
        )
    budget: dict[str, Any] = {
        "B": replicates,
        "C": candidates,
        "N": sample_count,
        "S": state_units,
        "caps": {
            "B": _MAX_IN_MEMORY_REPLICATES_V2,
            "BC": _MAX_IN_MEMORY_CANDIDATE_EVALUATIONS_V2,
            "BS": _MAX_IN_MEMORY_TOKEN_STATE_UNITS_V2,
            "work": _MAX_IN_MEMORY_WORK_UNITS_V2,
        },
        "within_caps": None,
    }
    if state_units is None:
        return budget
    try:
        _require_in_memory_execution_budget_values(
            B=replicates, C=candidates, N=sample_count, S=state_units
        )
    except ResourceLimitError:
        budget["within_caps"] = False
    else:
        budget["within_caps"] = True
    return budget


def preflight(request: PlanRequestV2, sample_count: int) -> dict[str, Any]:
    """Separate three questions: is the input valid, is the plan executable, what is assumed.

    Called only after the input loaded, so the input level is VALID here; loader failures are
    reported by their own error codes before this point. The resource check runs first so that
    no plan-time arithmetic grows with an oversized replicate count.
    """

    reasons: list[str] = []
    warnings: list[str] = []
    budget = _resource_budget(request, sample_count)
    if budget["within_caps"] is False:
        reasons.append("resource_budget_exceeded")
    elif budget["within_caps"] is None:
        warnings.append("null_state_space_unavailable_expect_not_evaluable")
    attainable = attainability(request, sample_count)
    if attainable["status"].startswith("REFUSE"):
        reasons.append(attainable["status"])
    elif attainable["status"] == "NOT_ASSESSED_EMPTY_NULL_STATE_SPACE":
        warnings.append("null_state_space_empty_expect_not_evaluable")
    return {
        "input": {"status": "VALID", "sample_count": sample_count},
        "plan": {
            "status": "NOT_EXECUTABLE" if reasons else "EXECUTABLE",
            "reasons": reasons,
            "warnings": warnings,
            "resource_budget": budget,
            "attainability": attainable,
        },
        "scientific_assumptions": {
            "status": "DECLARED_NOT_VERIFIED",
            "assumptions": _declared_assumptions(request),
            "note": "SelCal cannot check these from the data; the analyst must justify them.",
        },
    }


def attainability(request: PlanRequestV2, sample_count: int) -> dict[str, Any]:
    """Report the smallest p-value a plan can produce, before any calibration.

    Every comparison mirrors the calibrator: p = (1 + E) / (B + 1) in float arithmetic and
    rejection iff p <= alpha. No run can reach p < 1 / (B + 1). For the circular-shift nulls
    with lagged Pearson, shift s = c* - c maps searched lag c onto the selected lag c*, so those
    states reproduce the observed maximum: for exact enumeration p is at least their share of
    the states; for sampling it is the chance per draw of an unavoidable exceedance, which caps
    power. Only min_shift = 1 keeps the null states a group under lag search.
    """
    alpha = request.alpha
    replicates = request.replicates
    report: dict[str, Any] = {
        "monte_carlo_p_floor": 1 / (replicates + 1),
        "null_state_count": None,
        "null_state_p_floor": None,
        "monte_carlo_power_cap": None,
        "scope": "plan_arithmetic_not_scientific_validity",
    }
    enumerating = request.null_name == "circular_shift_exact_v1"
    if (
        request.null_name not in {"circular_shift_v2", "circular_shift_exact_v1"}
        or request.statistic_name != "lagged_pearson_v1"
    ):
        report["status"] = "NOT_ASSESSED"
        return report
    min_shift = request.null_params["min_shift"]
    if type(min_shift) is not int:
        raise WorkflowError("invalid_null_parameters")
    if 2 * min_shift > sample_count:
        report["status"] = "NOT_ASSESSED_EMPTY_NULL_STATE_SPACE"
        return report
    states = sample_count - 2 * min_shift + 2
    candidates = request.candidates

    def in_state_space(shift: int) -> bool:
        return shift == 0 or min_shift <= shift <= sample_count - min_shift

    colliding = min(
        sum(in_state_space((selected - lag) % sample_count) for lag in candidates)
        for selected in candidates
    )
    share = Fraction(colliding, states)
    # The same float expression the calibrator evaluates for the smallest reachable E.
    floor_rejects = colliding / states <= alpha
    report.update(null_state_count=states, null_state_p_floor=float(share))
    if enumerating and replicates != states - 1:
        report["status"] = "REFUSE_ENUMERATION_REPLICATE_COUNT"
        return report
    if enumerating:
        report["monte_carlo_power_cap"] = 1.0 if floor_rejects else 0.0
    else:
        # Strongest signal: rejection needs an exceedance count E with (1 + E)/(B + 1) <= alpha,
        # while each draw lands on an unavoidable colliding state with probability `floor`.
        report["monte_carlo_power_cap"] = _binomial_cdf_below(
            _allowed_exceedances(replicates, alpha), replicates, float(share)
        )
    if not 1 / (replicates + 1) <= alpha:
        report["status"] = "REFUSE_REPLICATES_TOO_FEW"
    elif min_shift > 1 and len(candidates) > 1:
        report["status"] = "REFUSE_NON_GROUP_NULL"
    elif not floor_rejects:
        report["status"] = "REFUSE_NULL_STATES_TOO_FEW"
    else:
        report["status"] = "PASS"
    return report


def validate_files(input_path: str | Path, config_path: str | Path) -> dict[str, Any]:
    """Validate actual input/configuration without running surrogate calibration."""
    config, resolution, loaded, _ = _files(input_path, config_path)
    sample_count = int(loaded.pair.source.size)
    return {
        "sample_count": sample_count,
        "planned_replicates": config.request.replicates,
        "raw_input_sha256": loaded.raw_input_sha256,
        "semantic_input_sha256": loaded.semantic_input_sha256,
        "scientific_plan_sha256": scientific_plan_v2_sha256(resolution.plan),
        "attainability": attainability(config.request, sample_count),
        "preflight": preflight(config.request, sample_count),
        "validation_scope": "input_and_plan_not_execution_admission_or_scientific_validity",
    }


def run_files(
    input_path: str | Path,
    config_path: str | Path,
    output_path: str | Path,
    *,
    max_bytes: int,
    allow_unattainable: bool = False,
) -> CalibrationResult:
    """Run a real calibration and exclusively save a complete terminal record.

    Computation uses the existing in-memory admission limits. max_bytes separately
    limits the record; it does not promise a process memory bound or early pause.
    Plans refused by `attainability` run only with allow_unattainable=True.
    """
    _limit(max_bytes)
    if type(allow_unattainable) is not bool:
        raise WorkflowError("invalid_attainability_option")
    if Path(output_path).exists() or Path(output_path).is_symlink():
        raise FileExistsError("output already exists")
    config, resolution, loaded, raw = _files(input_path, config_path)
    plan = preflight(config.request, int(loaded.pair.source.size))["plan"]
    if "resource_budget_exceeded" in plan["reasons"]:
        raise WorkflowConfigError(
            "resource_budget_exceeded",
            f"plan exceeds the in-memory execution budget: {plan['resource_budget']}",
        )
    refusals = [reason for reason in plan["reasons"] if reason.startswith("REFUSE")]
    if refusals and not allow_unattainable:
        raise WorkflowConfigError(
            "unattainable_plan", f"plan cannot reach alpha on this input: {refusals[0]}"
        )
    software = _software_identity()
    result = calibrate_selected_family(loaded.pair, resolution)
    verify_calibration_result(result, resolution)
    if software != _software_identity():
        raise WorkflowError("source_changed")
    metadata = {
        "schema": "selcal.workflow-record.v1",
        "raw_input_sha256": loaded.raw_input_sha256,
        "semantic_input_sha256": result.semantic_input_sha256,
        "scientific_plan_sha256": result.scientific_plan_sha256,
        "software": software,
    }
    write_record(
        output_path,
        {
            "input": raw,
            "request": encode_workflow_config(config),
            "result": encode_calibration_result(result, max_bytes=max_bytes),
            "metadata": _json(metadata),
        },
        max_bytes=max_bytes,
    )
    return result


def _metadata(raw: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise WorkflowError("invalid_metadata")
            result[key] = value
        return result

    def forbidden(value: str) -> None:
        raise WorkflowError("invalid_metadata")

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=forbidden)
        keys = {
            "schema",
            "raw_input_sha256",
            "semantic_input_sha256",
            "scientific_plan_sha256",
            "software",
        }
        if type(value) is not dict or set(value) != keys:
            raise WorkflowError("invalid_metadata")
        if value["schema"] != "selcal.workflow-record.v1":
            raise WorkflowError("invalid_metadata")
        for key in keys - {"schema", "software"}:
            if type(value[key]) is not str or re.fullmatch("[0-9a-f]{64}", value[key]) is None:
                raise WorkflowError("invalid_metadata")
        software = value["software"]
        if type(software) is not dict or set(software) != {
            "selcal_version",
            "python_version",
            "numpy_version",
            "source_files",
        }:
            raise WorkflowError("invalid_metadata")
        for key in ("selcal_version", "python_version", "numpy_version"):
            if type(software[key]) is not str or not software[key] or len(software[key]) > 256:
                raise WorkflowError("invalid_metadata")
        sources = software["source_files"]
        if type(sources) is not dict or not sources:
            raise WorkflowError("invalid_metadata")
        for name, digest in sources.items():
            if (
                type(name) is not str
                or not re.fullmatch(r"[A-Za-z0-9_/]+\.py", name)
                or name.startswith("/")
                or "//" in name
                or type(digest) is not str
                or re.fullmatch("[0-9a-f]{64}", digest) is None
            ):
                raise WorkflowError("invalid_metadata")
        return value
    except (ValueError, TypeError, RecursionError) as error:
        raise WorkflowError("invalid_metadata") from error


def _read_context(
    record_path: str | Path, max_bytes: int
) -> tuple[WorkflowRecord, LoadedInput, PlanResolutionV2, bytes]:
    _limit(max_bytes)
    members = read_record(record_path, max_bytes=max_bytes)
    try:
        config = decode_workflow_config(members["request"])
        metadata = _metadata(members["metadata"])
        result = decode_calibration_result(members["result"], max_bytes=max_bytes)
        resolution = resolve_plan_v2(config.request)
        # Reuse the same strict file loader; never consult the original input path.
        with tempfile.TemporaryDirectory(prefix="selcal-read-") as folder:
            path = Path(folder) / ("input." + config.source_format)
            path.write_bytes(members["input"])
            loaded = _load(path, config)
        if (
            metadata["raw_input_sha256"] != loaded.raw_input_sha256
            or metadata["semantic_input_sha256"] != loaded.semantic_input_sha256
            or result.semantic_input_sha256 != loaded.semantic_input_sha256
            or metadata["scientific_plan_sha256"] != result.scientific_plan_sha256
        ):
            raise WorkflowError("identity_mismatch")
        verify_calibration_result(result, resolution)
    except (ValueError, TypeError, SelCalV2Error) as error:
        raise WorkflowError("invalid_record_content") from error
    return WorkflowRecord(config, result, metadata), loaded, resolution, members["result"]


def read_workflow(record_path: str | Path, *, max_bytes: int) -> WorkflowRecord:
    """Read a captured terminal and verify input/plan/result consistency, not replay."""
    return _read_context(record_path, max_bytes)[0]


def result_summary(result: CalibrationResult) -> dict[str, Any]:
    """Return explicit scientific status and decision fields without dropping failures."""
    selection = result.observed_selection
    return {
        "status": result.status.value,
        "failure_stage": None if result.failure_stage is None else result.failure_stage.value,
        "planned_replicates": result.planned_replicates,
        "retained_replicates": len(result.replicates),
        "exceedance_count": result.exceedance_count,
        "failure_count": result.failure_count,
        "p_value": result.p_value,
        "selected_candidate": None if selection is None else selection.selected_candidate,
        "decision_statistic": None if selection is None else selection.decision_statistic,
        "tied_candidates": None if selection is None else list(selection.tied_candidates),
        "reject_null": result.reject_null,
        "exceedance_bound_low": result.exceedance_bound_low,
        "exceedance_bound_high": result.exceedance_bound_high,
        "semantic_input_sha256": result.semantic_input_sha256,
        "scientific_plan_sha256": result.scientific_plan_sha256,
    }


def verify_record(
    record_path: str | Path, *, max_bytes: int, replay: bool = False
) -> dict[str, Any]:
    """Optionally execute an explicit full replay; never authenticate past execution."""
    if type(replay) is not bool:
        raise WorkflowError("invalid_replay_option")
    record, loaded, resolution, saved = _read_context(record_path, max_bytes)
    if replay:
        if record.metadata["software"] != _software_identity():
            raise WorkflowError("environment_mismatch")
        actual = calibrate_selected_family(loaded.pair, resolution)
        if encode_calibration_result(actual, max_bytes=max_bytes) != saved:
            raise WorkflowError("replay_mismatch")
    return {
        **result_summary(record.result),
        "attainability": attainability(record.config.request, int(loaded.pair.source.size)),
        "replay": "MATCH" if replay else "NOT_PERFORMED",
        "verification_scope": "input_plan_result_consistency",
        "historical_execution_authenticated": False,
    }


def report_record(
    record_path: str | Path, output_path: str | Path, *, max_bytes: int
) -> dict[str, Any]:
    """Render an exclusive HTML report from checked content, without scientific replay."""
    record, loaded, _, _ = _read_context(record_path, max_bytes)
    result = record.result
    summary = {
        **result_summary(result),
        "attainability": attainability(record.config.request, int(loaded.pair.source.size)),
        "replay": "NOT_PERFORMED",
    }
    body = [
        '<!doctype html><html lang="en"><meta charset="utf-8">',
        "<title>SelCal calibration report</title><style>"
        "body{max-width:960px;margin:2rem auto;padding:0 1rem;font:16px system-ui;color:#172b4d}"
        "pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f7;padding:1rem}"
        "section{border-top:1px solid #ccd3dc}h2{margin-top:2rem}"
        "</style><body><h1>SelCal calibration report</h1>",
        "<p>Input/plan/result consistency checked; replay NOT_PERFORMED. "
        "Recorded content is not authenticated historical execution.</p>",
        "<p>NOT_EVALUABLE is not evidence of no effect or non-significance.</p>",
        "<h2>Summary</h2><pre>",
        html.escape(json.dumps(summary, indent=2)),
        "</pre>",
        "<h2>Configuration</h2><pre>",
        html.escape(encode_workflow_config(record.config).decode()),
        "</pre><h2>Observed candidates</h2><pre>",
        html.escape(repr(result.observed_results)),
        "</pre><h2>Observed selection</h2><pre>",
        html.escape(repr(result.observed_selection)),
        "</pre><h2>Replicates</h2>",
    ]
    for outcome in result.replicates:
        body.extend(
            (
                f'<section data-replicate-id="{outcome.replicate_id}"><h3>Replicate '
                f"{outcome.replicate_id}</h3><pre>",
                html.escape(repr(outcome)),
                "</pre></section>",
            )
        )
    body.extend(
        (
            "<h2>Diagnostics</h2><pre>",
            html.escape(repr(result.diagnostics)),
            "</pre><h2>Recorded software identity (not authentication)</h2><pre>",
            html.escape(json.dumps(record.metadata["software"], indent=2)),
            "</pre></body></html>",
        )
    )
    payload = "\n".join(body).encode("utf-8")
    if len(payload) > max_bytes:
        raise WorkflowError("report_size_limit")
    with Path(output_path).open("xb") as stream:
        stream.write(payload)
    return summary


def doctor() -> dict[str, Any]:
    """Report this runtime, without claiming unexecuted tests or scientific validation."""
    import sqlite3

    return {
        "selcal_version": __version__,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "sqlite_version": sqlite3.sqlite_version,
        "sqlite_deserialize": hasattr(sqlite3.Connection, "deserialize"),
        "checkpoint_resume": "NOT_IMPLEMENTED",
        "scientific_validation": "NOT_EXECUTED",
    }
