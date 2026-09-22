"""Development-only pair adapter tests; no study-phase data are drawn."""

from __future__ import annotations

import importlib.util
import json
import math

import pytest
from test_m6_pearson_diagnostic_public import ROOT, driver, projected


def preparation():
    path = (
        ROOT
        / "docs/research/softwarex_2025_2026_20260909/study_preparation/prepare_bounded_study.py"
    )
    spec = importlib.util.spec_from_file_location("pair_test_preparation", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request_parameters(seed, *, alpha=0.05):
    return dict(
        candidates=(1, 2),
        statistic_name="lagged_pearson_v1",
        statistic_params={},
        selection_rule="max_upper",
        null_name="circular_shift_v2",
        null_params={"min_shift": 1},
        replicates=199,
        alpha=alpha,
        tie_tolerance=0.0,
        root_seed=seed,
    )


@pytest.mark.parametrize("cell", ["iid_null", "circular_ma2_null", "lag2_rho03", "lag2_rho06"])
@pytest.mark.parametrize("alpha", [0.05, 0.1])
def test_generated_development_pair_reaches_public_api_and_retains_every_state(
    cell, alpha, monkeypatch
):
    mod, prep = driver(), preparation()
    assert callable(getattr(mod, "run_pair", None)), "arbitrary-pair comparison entry is absent"
    x, y = prep.make_pair(cell, 0, phase="development")
    seed = int(prep.seed_hex("development", cell, 0, "null")[:16], 16)
    params = request_parameters(seed, alpha=alpha)
    original, captured = mod.calibrate_selected_family, []

    def observe(pair, resolution):
        actual = original(pair, resolution)
        captured.append((pair, resolution.plan, actual))
        return actual

    monkeypatch.setattr(mod, "calibrate_selected_family", observe)
    out = mod.run_pair(cell, x, y, params)
    assert out["comparison_status"] == "AGREEMENT", out["mismatches"]
    assert len(captured) == 1
    pair, plan, actual = captured[0]
    assert tuple(pair.source) == tuple(x) and tuple(pair.target) == tuple(y)
    assert all(value == getattr(plan, name) for name, value in params.items())
    assert out["request"] == params
    assert out["input"]["seed"] == seed != 17
    assert out["input"]["alpha"] == alpha
    assert out["input"]["source_hex"] == [float(v).hex() for v in x]
    assert out["input"]["target_hex"] == [float(v).hex() for v in y]
    assert out["checked_observed_candidates"] == 2
    assert out["checked_replicates"] == len(out["replicates"]) == 199
    exact = out["reference_exact"]
    assert exact["status"] == "COMPLETE_TABLE"
    assert exact["denominator"] == len(exact["states"]) == 64
    assert [row["state"] for row in exact["states"]] == list(range(64))
    assert [row["replicate_id"] for row in out["replicates"]] == list(range(199))
    assert all(len(row["candidate_comparisons"]) == 2 for row in out["replicates"])
    assert all(row["mismatches"] == [] for row in out["replicates"])
    indicators = [row["tail"]["reference_indicator"] for row in out["replicates"]]
    assert indicators == [row["tail"]["production_indicator"] for row in out["replicates"]]
    for summary in (out["reference_summary"], out["production_summary"]):
        assert (summary["B"], summary["E"], summary["F"]) == (199, sum(indicators), 0)
        assert summary["p"] == actual.p_value == (1 + sum(indicators)) / 200
        assert summary["reject_null"] is (summary["p"] <= alpha)
    json.dumps(out, allow_nan=False)


def observed_failure_pair():
    # At lag 1 the last source value is available; lag 2 has zero source variance.
    return (0.0,) * 62 + (1.0, 0.0), tuple(float(i) for i in range(64))


def test_actual_observed_failure_has_no_attempted_replicates_or_invented_p():
    mod = driver()
    x, y = observed_failure_pair()
    out = mod.run_pair("development_observed_failure", x, y, request_parameters(123))
    assert out["comparison_status"] == "AGREEMENT", out["mismatches"]
    assert out["checked_replicates"] == 0 and out["replicates"] == []
    assert len(out["reference_exact"]["states"]) == 64
    assert out["reference_exact"]["status"] == "ANALYTICALLY_UNEVALUABLE"
    assert out["observed"]["reference_selection"] is None
    assert out["observed"]["production_selection"] is None
    assert [row["reference_failure"] for row in out["observed_comparison"]] == [
        None, "ZERO_SOURCE_VARIANCE"
    ]
    for summary in (out["reference_summary"], out["production_summary"]):
        assert (summary["B"], summary["E"], summary["F"]) == (199, 0, 0)
        assert summary["status"] == "not_evaluable"
        assert summary["failure_stage"] == "observed_statistic_scan"
        assert summary["p"] is summary["reject_null"] is summary["bounds"] is None
    assert out["reference_summary"]["indicators"] == ()
    json.dumps(out, allow_nan=False)


@pytest.mark.parametrize(
    "field,value,mismatch",
    [
        ("status", "complete", "RUN_STATUS_DISAGREEMENT"),
        ("failure_stage", None, "RUN_FAILURE_STAGE_DISAGREEMENT"),
        ("p_value", 0.0, "SUMMARY_P_DISAGREEMENT"),
        ("reject_null", False, "REJECT_NULL_DISAGREEMENT"),
        ("exceedance_count", 1, "SUMMARY_E_DISAGREEMENT"),
        ("failure_count", 199, "SUMMARY_F_DISAGREEMENT"),
        ("exceedance_bound_low", 0.0, "FAILURE_BOUND_DISAGREEMENT"),
        ("exceedance_bound_high", 1.0, "FAILURE_BOUND_DISAGREEMENT"),
    ],
)
def test_observed_failure_corruption_is_compared_not_blanket_accepted(
    monkeypatch, field, value, mismatch
):
    from selcal.contracts import RunStatus

    mod = driver()
    original = mod.calibrate_selected_family
    if field == "status":
        value = RunStatus.COMPLETE

    def corrupt(*args):
        return projected(original(*args), **{field: value})

    monkeypatch.setattr(mod, "calibrate_selected_family", corrupt)
    x, y = observed_failure_pair()
    out = mod.run_pair("development_observed_failure", x, y, request_parameters(123))
    assert out["comparison_status"] == "DISAGREEMENT"
    assert mismatch in out["mismatches"]
    assert out["checked_replicates"] == 0


@pytest.mark.parametrize(
    "corruption,mismatch",
    [
        ("token", "INVALID_TRANSFORM_TOKEN"),
        ("tail", "TAIL_INDICATOR_DISAGREEMENT"),
        ("score", "SELECTION_SCORE_DISAGREEMENT"),
        ("identity", "RUN_SCIENTIFIC_PLAN_SHA256_DISAGREEMENT"),
        ("decision", "REJECT_NULL_DISAGREEMENT"),
    ],
)
def test_development_pair_retains_injected_disagreement_and_later_rows(
    monkeypatch, corruption, mismatch
):
    mod, prep = driver(), preparation()
    original = mod.calibrate_selected_family

    def corrupt(*args):
        actual = original(*args)
        if corruption == "identity":
            return projected(actual, scientific_plan_sha256="0" * 64)
        if corruption == "decision":
            return projected(actual, reject_null=not actual.reject_null)
        first = actual.replicates[0]
        if corruption == "token":
            first = projected(first, transform_token=None)
        elif corruption == "tail":
            observed = actual.observed_selection.decision_statistic
            value = (
                math.nextafter(observed, -math.inf)
                if first.selection.decision_statistic >= observed
                else observed
            )
            first = projected(first, selection=projected(first.selection, decision_statistic=value))
        else:
            first = projected(
                first,
                statistic_results=(
                    projected(first.statistic_results[0], selection_score=-9.0),
                    *first.statistic_results[1:],
                ),
            )
        return projected(actual, replicates=(first, *actual.replicates[1:]))

    monkeypatch.setattr(mod, "calibrate_selected_family", corrupt)
    x, y = prep.make_pair("iid_null", 1, phase="development")
    seed = int(prep.seed_hex("development", "iid_null", 1, "null")[:16], 16)
    out = mod.run_pair("development_corruption", x, y, request_parameters(seed))
    assert out["comparison_status"] == "DISAGREEMENT"
    assert mismatch in out["mismatches"]
    assert len(out["replicates"]) == 199
    assert out["replicates"][-1]["mismatches"] == []
    if corruption == "token":
        assert out["reference_summary"] is None
    json.dumps(out, allow_nan=False)


def test_observed_failure_must_still_retain_the_requested_budget(monkeypatch):
    mod = driver()
    original = mod.calibrate_selected_family
    monkeypatch.setattr(
        mod,
        "calibrate_selected_family",
        lambda *args: projected(original(*args), planned_replicates=0),
    )
    x, y = observed_failure_pair()
    out = mod.run_pair("development_observed_failure", x, y, request_parameters(123))
    assert "PLANNED_REPLICATE_COUNT_DISAGREEMENT" in out["mismatches"]
    assert "SUMMARY_B_DISAGREEMENT" in out["mismatches"]
    assert out["reference_summary"]["B"] == 199
    assert out["checked_replicates"] == 0


@pytest.mark.parametrize("field", ["exceedance_bound_low", "exceedance_bound_high"])
@pytest.mark.parametrize("value", [0.125, True, float("nan"), float("inf")])
def test_complete_run_checks_and_retains_raw_diagnostic_bound_corruption(monkeypatch, field, value):
    mod = driver()
    original = mod.calibrate_selected_family

    def corrupt(*args):
        actual = original(*args)
        assert actual.failure_count == 0
        assert actual.exceedance_bound_low is actual.exceedance_bound_high is None
        return projected(actual, **{field: value})

    monkeypatch.setattr(mod, "calibrate_selected_family", corrupt)
    out = mod.run_case("reselection")
    assert "FAILURE_BOUND_DISAGREEMENT" in out["mismatches"]
    assert out["comparison_status"] == "DISAGREEMENT"
    assert out["production_summary"]["bounds"] is None
    check = out["production_summary"]["raw_bounds"][field]
    assert check["expected"] is None and check["matches"] is False
    assert check["production_type"] == type(value).__name__
    if type(value) is float:
        assert check["production_hex"] == value.hex()
    else:
        assert check["production"] is value
    json.dumps(out, allow_nan=False)


@pytest.mark.parametrize(
    "field,cast,summary_field",
    [
        ("planned_replicates", float, "B"),
        ("exceedance_count", float, "E"),
        ("failure_count", float, "F"),
        ("failure_count", bool, "F"),
    ],
)
def test_equal_summary_count_with_wrong_type_is_a_disagreement(
    monkeypatch, field, cast, summary_field
):
    mod = driver()
    original = mod.calibrate_selected_family

    def corrupt(*args):
        actual = original(*args)
        value = cast(getattr(actual, field))
        assert value == getattr(actual, field)
        return projected(actual, **{field: value})

    monkeypatch.setattr(mod, "calibrate_selected_family", corrupt)
    out = mod.run_case("reselection")
    assert f"SUMMARY_{summary_field}_DISAGREEMENT" in out["mismatches"]
    assert type(out["production_summary"][summary_field]) is cast


@pytest.mark.parametrize("cast", [int, bool])
def test_equal_unit_p_with_wrong_type_is_a_disagreement(monkeypatch, cast):
    mod = driver()
    original = mod.calibrate_selected_family

    def corrupt(*args):
        actual = original(*args)
        assert actual.p_value == 1.0
        return projected(actual, p_value=cast(actual.p_value))

    monkeypatch.setattr(mod, "calibrate_selected_family", corrupt)
    x = tuple(float(i) for i in range(6))
    y = tuple(-v for v in x)
    params = dict(request_parameters(17), replicates=9)
    out = mod.run_pair("development_unit_p", x, y, params)
    assert "SUMMARY_P_DISAGREEMENT" in out["mismatches"]
    assert type(out["production_summary"]["p"]) is cast
