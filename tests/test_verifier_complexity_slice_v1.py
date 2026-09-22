"""Portable and self-auditing RED instrument for the verifier slice."""

from __future__ import annotations

import ast
import copy
import json
import subprocess
import sys
from collections import deque
from collections.abc import Mapping
from dataclasses import fields
from pathlib import Path
from types import FunctionType
from typing import NamedTuple

import _verifier_structure_gate_v1 as gate
import pytest
from _verifier_structure_gate_v1 import (
    GraphBudgets,
    GraphPolicy,
    freeze_budgets,
    function_inventory,
    gate_implementation_closure,
    normalized_source,
    source_identity_row,
    source_segment_digest,
    static_source_violations,
    validate_durable_r3_receipt_v1,
    validate_fixture_bytes,
    walk_identity_graph,
)

import selcal.calibration_v2 as calibration_v2
import selcal.canonical_v2 as canonical_v2
import selcal.contracts_v2 as contracts_v2
import selcal.resolution_v2 as resolution_v2
from selcal.contracts import SelectionResult, StatisticResult
from selcal.contracts_v2 import CalibrationResult, ReplicateOutcome

try:
    import selcal._verifier_primitives_v2 as verifier_primitives_v2
except ModuleNotFoundError as primitive_import_error:
    if primitive_import_error.name != "selcal._verifier_primitives_v2":
        raise
    verifier_primitives_v2 = None


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEST_PATH = Path(__file__).resolve()
HELPER_PATH = REPOSITORY_ROOT / "tests/_verifier_structure_gate_v1.py"
FIXTURE_PATH = REPOSITORY_ROOT / "tests/fixtures/verifier_structure_gate_v1.json"
CONTRACTS_PATH = REPOSITORY_ROOT / "src/selcal/contracts_v2.py"
PRIMITIVES_PATH = REPOSITORY_ROOT / "src/selcal/_verifier_primitives_v2.py"
CALIBRATION_PATH = REPOSITORY_ROOT / "src/selcal/calibration_v2.py"
EXPECTED_GATE_FILES = (
    HELPER_PATH.resolve(),
    TEST_PATH.resolve(),
)
EXPECTED_FAILED = (
    "test_verifier_primitives_module_exists",
    "test_verifier_slice_has_no_c901_findings",
    "test_verifier_slice_function_inventory_meets_span_and_parameter_gates",
)
EXPECTED_DEFERRED = (
    "test_primitive_static_inventory_has_no_hidden_dispatch_or_state",
    "test_verifier_typed_topology_is_exact_and_complete",
    "test_public_verifier_runtime_graph_has_exact_primitive_ops_topology",
    "test_runtime_verifier_slot_schema_covers_every_dataclass_field",
    "test_builder_runtime_graph_stops_only_at_exact_public_terminal_boundary",
)
R3_DURABLE_PATH = Path("docs/status/verifier_structure_red_r3_20260902.json")
R3_INPUT_PATHS = (
    "docs/status/evidence/verifier_structure_oracle_enumerator_v1.py",
    "docs/superpowers/plans/2026-09-01-verifier-complexity-slice-v1-implementation.md",
    "docs/superpowers/specs/2026-09-01-verifier-complexity-slice-v1-design.md",
    "tests/_verifier_structure_gate_v1.py",
    "tests/fixtures/verifier_structure_gate_v1.json",
    "tests/test_verifier_complexity_slice_v1.py",
    "tests/test_verifier_integration_v2.py",
)
R3_COMMANDS = (
    ("prefixedPy314", 1),
    ("prefixedPy311", 1),
    ("oracle", 0),
    ("py311Full", 1),
    ("py311Portable", 0),
    ("py311Environment", 0),
    ("py311Ruff", 0),
    ("py312Full", 1),
    ("py312Portable", 0),
    ("py312Environment", 0),
    ("py312Ruff", 0),
    ("py313Full", 1),
    ("py313Portable", 0),
    ("py313Environment", 0),
    ("py313Ruff", 0),
    ("py314Full", 1),
    ("py314Portable", 0),
    ("py314Environment", 0),
    ("py314Ruff", 0),
    ("integration102", 0),
    ("regression588", 0),
    ("related690", 0),
    ("ordinaryRuff", 0),
    ("selfC901", 0),
    ("strictMypy", 0),
    ("diffCheck", 0),
    ("gitStatus", 0),
    ("inputHashes", 0),
)
EXPECTED_SLOTS = (
    (CalibrationResult, tuple(field.name for field in fields(CalibrationResult))),
    (ReplicateOutcome, tuple(field.name for field in fields(ReplicateOutcome))),
    (StatisticResult, tuple(field.name for field in fields(StatisticResult))),
    (SelectionResult, tuple(field.name for field in fields(SelectionResult))),
)


class ApprovedProbe(NamedTuple):
    first: object
    second: object


class CallableProbe:
    def __call__(self) -> None:
        return None


class MutableProbe:
    pass


def _fixture() -> dict[str, object]:
    return validate_fixture_bytes(FIXTURE_PATH)


def _budgets(value: Mapping[str, object] | None = None) -> GraphBudgets:
    selected = value or {"nodes": 128, "edges": 128, "depth": 16}
    return GraphBudgets(
        nodes=int(selected["nodes"]),
        edges=int(selected["edges"]),
        depth=int(selected["depth"]),
    )


def _empty_policy(
    approved_record_types: tuple[type[object], ...] = (),
    approved_schema_types: tuple[type[object], ...] = (),
) -> GraphPolicy:
    return GraphPolicy(
        repository_root=REPOSITORY_ROOT,
        approved_record_types=approved_record_types,
        approved_schema_types=approved_schema_types,
    )


def _root_closure_values(function: FunctionType) -> tuple[object, ...]:
    values: list[object] = list(function.__defaults__ or ())
    values.extend(value for _key, value in sorted((function.__kwdefaults__ or {}).items()))
    for cell in function.__closure__ or ():
        try:
            values.append(cell.cell_contents)
        except ValueError:
            continue
    return tuple(values)


def _builder_policy(fixture: Mapping[str, object]) -> GraphPolicy:
    root = calibration_v2.calibrate_selected_family
    values = _root_closure_values(root)
    manifests = tuple(fixture["builderNeutralFrontier"])
    project_ids = {
        id(value)
        for value in values
        if type(value) is FunctionType
        and value.__module__.startswith("selcal.")
        and value is not contracts_v2.verify_calibration_result
    }
    terminal_ids = frozenset(
        id(value)
        for value in values
        if id(value) not in project_ids and value is not contracts_v2.verify_calibration_result
    )
    return GraphPolicy(
        repository_root=REPOSITORY_ROOT,
        project_manifest=manifests,
        terminal_identities=terminal_ids,
        stop_identities=frozenset({id(contracts_v2.verify_calibration_result)}),
        root_project_identities=frozenset({id(root)}),
    )


def _assert_builder_rows(fixture: Mapping[str, object]) -> None:
    limits = _budgets(fixture["graphBudgets"]["frozen"])
    result = walk_identity_graph(
        (calibration_v2.calibrate_selected_family,), limits, _builder_policy(fixture)
    )
    assert result.project_rows == tuple(fixture["builderNeutralFrontier"])
    observed = fixture["graphBudgets"]["observed"]
    assert (result.nodes, result.edges, result.depth) == (
        observed["nodes"],
        observed["edges"],
        observed["depth"],
    )


def _runtime_functions() -> tuple[FunctionType, ...]:
    roots: tuple[object, ...] = (
        canonical_v2._RESULT_VERIFIER_PLAN_SHA256_V2,
        contracts_v2.verify_calibration_result,
        resolution_v2._SEALED_RESULT_TOKEN_VERIFIERS_V2,
    )
    queue = deque(roots)
    seen: set[int] = set()
    found: list[FunctionType] = []
    while queue:
        value = queue.popleft()
        if id(value) in seen:
            continue
        seen.add(id(value))
        if type(value) is FunctionType:
            found.append(value)
            queue.extend(_root_closure_values(value))
        elif isinstance(value, Mapping):
            queue.extend(item for pair in value.items() for item in pair)
        elif isinstance(value, tuple) or type(value) in (list, set, frozenset):
            queue.extend(value)
    return tuple(found)


def _frontier_functions() -> tuple[tuple[dict[str, object], FunctionType], ...]:
    functions = _runtime_functions()
    rows = tuple(_fixture()["frontier"])
    pairs: list[tuple[dict[str, object], FunctionType]] = []
    for row in rows:
        matches = tuple(
            function
            for function in functions
            if function.__module__ == row["module"] and function.__qualname__ == row["qualname"]
        )
        assert len(matches) == 1, row
        pairs.append((row, matches[0]))
    return tuple(pairs)


def _assert_graph_error(value: object, label: str) -> None:
    with pytest.raises(AssertionError, match=label):
        walk_identity_graph((value,), _budgets(), _empty_policy())


def _canonical_fixture(candidate: Mapping[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(candidate, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _assert_fixture_failure(value: Mapping[str, object], label: str, path: Path) -> None:
    _canonical_fixture(value, path)
    with pytest.raises(AssertionError, match=f"^{label}$"):
        validate_fixture_bytes(path)


def _minimal_r3() -> dict[str, object]:
    commands = [
        {
            "name": name,
            "argv": ["python", name],
            "cwd": str(REPOSITORY_ROOT),
            "returnCode": return_code,
            "stdoutSha256": "0" * 64,
            "stderrSha256": "0" * 64,
            "junitSha256": (
                "0" * 64
                if name.startswith("prefixed") or "Full" in name or "Portable" in name
                else None
            ),
        }
        for name, return_code in R3_COMMANDS
    ]
    return {
        "schema": "selcal.verifier-structure-red-receipt.v3",
        "version": 3,
        "status": "EXPECTED_RED_CURRENT_PRODUCTION_UNMODIFIED",
        "date": "2026-09-02",
        "claimCeiling": "LOCAL_ADVERSE_STRUCTURE_INSTRUMENT_EVIDENCE_ONLY_NO_PRODUCTION_CLOSURE",
        "repository": {
            "baseCommit": "94f993bfd5240739f23dd5f5309a51e51034b962",
            "branch": "codex/contract-resolution-pearson",
            "dirtyPaths": [],
            "productionSha256": (
                "9e4cb4a945602c3ca8e299aefa73b01e753d3b90bdaa465b849d81bcc2b80ef5"
            ),
        },
        "inputs": {path: "0" * 64 for path in R3_INPUT_PATHS},
        "priorReceipts": [
            {
                "name": "R1",
                "reportedSha256": None,
                "path": None,
                "bytesVerified": False,
                "availability": "HISTORICAL_TEMPORARY_BYTES_AND_EXACT_IDENTITY_UNAVAILABLE",
            },
            {
                "name": "R2",
                "reportedSha256": (
                    "d2ad226b818c156c7651717c2658b58043fbd35dff4729758c15f6d72fab637b"
                ),
                "path": None,
                "bytesVerified": False,
                "availability": "HISTORICAL_REPORTED_IDENTITY_CURRENT_BYTES_UNAVAILABLE",
            },
            {
                "name": "Task1A",
                "reportedSha256": None,
                "path": None,
                "bytesVerified": False,
                "availability": "HISTORICAL_TEMPORARY_BYTES_AND_EXACT_IDENTITY_UNAVAILABLE",
            },
        ],
        "environmentCells": [
            {
                "label": label,
                "requestedPython": requested,
                "resolvedPython": requested,
                "numpy": "1.26.4" if label in {"py311", "py312"} else "2.4.6",
                "pytest": "8.4.2",
                "ruff": "0.16.5",
                "os": "Darwin",
                "architecture": "arm64",
                "machine": "arm64",
            }
            for label, requested in (
                ("py311", "3.11"),
                ("py312", "3.12"),
                ("py313", "3.13"),
                ("py314", "3.14"),
            )
        ],
        "commands": commands,
        "triState": {
            "collected": 50,
            "passed": 42,
            "failed": 3,
            "deferred": 5,
            "failedNodeIds": list(EXPECTED_FAILED),
            "deferredNodeIds": list(EXPECTED_DEFERRED),
        },
        "findingToFix": {
            "portable-frontier-identity": (
                "test_portable_frontier_identity_does_not_depend_on_co_code"
            ),
            "portable-legacy-identity": (
                "test_portable_legacy_identity_does_not_depend_on_ast_dump"
            ),
            "self-complexity": ("test_structure_gate_implementation_has_zero_self_c901_findings"),
            "custom-callable": "test_runtime_graph_rejects_direct_custom_callable_object",
            "direct-dunder-import": "test_static_gate_rejects_direct_dunder_import",
            "nested-writable-singleton": "test_static_gate_rejects_nested_writable_singleton",
            "self-cycle": "test_runtime_graph_terminates_pure_self_cycle",
            "unknown-builder-helper": "test_builder_rejects_unknown_reachable_project_helper",
        },
        "regressions": [
            {"name": "integration102", "passed": 102, "failed": 0, "skipped": 0},
            {"name": "regression588", "passed": 588, "failed": 0, "skipped": 0},
            {"name": "related690", "passed": 690, "failed": 0, "skipped": 0},
        ],
        "artifacts": {
            path: "0" * 64
            for path in (
                "docs/status/evidence/verifier_structure_oracle_enumerator_v1.py",
                "tests/_verifier_structure_gate_v1.py",
                "tests/fixtures/verifier_structure_gate_v1.json",
                "tests/test_verifier_complexity_slice_v1.py",
            )
        },
    }


def test_portable_frontier_identity_does_not_depend_on_co_code() -> None:
    helper_source = HELPER_PATH.read_text(encoding="utf-8")
    assert ".co_code" not in helper_source
    for row, function in _frontier_functions():
        observed = source_identity_row(function, REPOSITORY_ROOT)
        assert all(observed[key] == row[key] for key in observed)


def test_portable_legacy_identity_does_not_depend_on_ast_dump() -> None:
    assert "ast.dump" not in HELPER_PATH.read_text(encoding="utf-8")
    for row in _fixture()["legacyDeclarations"]:
        digest = source_segment_digest(
            REPOSITORY_ROOT / row["sourcePath"],
            kind=row["kind"],
            qualname_or_target=row["name"],
            first_line=row["firstLine"],
            legacy=True,
        )
        assert digest == row["sourceSegmentSha256"]


def test_structure_gate_implementation_has_zero_self_c901_findings() -> None:
    for path in EXPECTED_GATE_FILES:
        assert not static_source_violations(path.read_text(encoding="utf-8"))
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--select",
            "C901",
            "--config",
            "lint.mccabe.max-complexity=10",
            str(HELPER_PATH),
            str(TEST_PATH),
        ],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_runtime_graph_rejects_direct_custom_callable_object() -> None:
    _assert_graph_error(CallableProbe(), "GRAPH_FORBIDDEN_CALLABLE_V1")


def test_static_gate_rejects_direct_dunder_import() -> None:
    source = (
        "def probe():\n"
        "    global BEHAVIOR\n"
        "    import os\n"
        "    return __import__('sys')\n"
    )
    violations = static_source_violations(source)
    assert "behavior-global:BEHAVIOR:2" in violations
    assert "runtime-import:3" in violations
    assert "dynamic-call:__import__:4" in violations


def test_static_gate_rejects_nested_writable_singleton() -> None:
    violations = static_source_violations("VALUE = (('nested', {'key': []}),)\n")
    assert "nested-writable-singleton:1" in violations


def test_runtime_graph_terminates_pure_self_cycle() -> None:
    cycle: list[object] = []
    cycle.append(cycle)
    result = walk_identity_graph((cycle,), _budgets(), _empty_policy())
    assert (result.nodes, result.edges, result.depth) == (1, 1, 0)


def test_builder_rejects_unknown_reachable_project_helper() -> None:
    manifest = tuple(_fixture()["builderNeutralFrontier"])
    unknown_project_helper = calibration_v2._snapshot_selection

    def root() -> None:
        unknown_project_helper(None)

    policy = GraphPolicy(
        repository_root=REPOSITORY_ROOT,
        project_manifest=manifest,
        root_project_identities=frozenset({id(root)}),
    )
    with pytest.raises(AssertionError, match="UNKNOWN_PROJECT_FUNCTION_V1"):
        walk_identity_graph((root,), _budgets(), policy)


def test_source_identity_rejects_zero_match() -> None:
    with pytest.raises(AssertionError, match="SOURCE_IDENTITY_MATCH_COUNT:0"):
        source_segment_digest(
            CONTRACTS_PATH,
            kind="FunctionDef",
            qualname_or_target="missing",
            first_line=1,
        )


def test_source_identity_rejects_multiple_match(monkeypatch: pytest.MonkeyPatch) -> None:
    tree = ast.parse("def probe():\n    pass\n")
    node = tree.body[0]

    def duplicate_declarations(_tree: ast.Module) -> tuple[tuple[str, ast.AST], ...]:
        return ("probe", node), ("probe", node)

    monkeypatch.setattr(gate, "lexical_declarations", duplicate_declarations)
    with pytest.raises(AssertionError, match="SOURCE_IDENTITY_MATCH_COUNT:2"):
        source_segment_digest(
            TEST_PATH, kind="FunctionDef", qualname_or_target="probe", first_line=1
        )


def test_source_identity_rejects_missing_position(monkeypatch: pytest.MonkeyPatch) -> None:
    tree = ast.parse("def probe():\n    pass\n")
    node = tree.body[0]
    node.end_lineno = None

    def fixed_tree(_source: str, *, filename: str) -> ast.Module:
        assert filename
        return tree

    monkeypatch.setattr(gate.ast, "parse", fixed_tree)
    with pytest.raises(AssertionError, match="SOURCE_IDENTITY_INCOMPLETE_POSITION"):
        source_segment_digest(
            TEST_PATH, kind="FunctionDef", qualname_or_target="probe", first_line=1
        )


def test_source_identity_rejects_none_segment(monkeypatch: pytest.MonkeyPatch) -> None:
    tree = ast.parse("def probe():\n    pass\n")

    def fixed_tree(_source: str, *, filename: str) -> ast.Module:
        assert filename
        return tree

    def none_segment(_source: str, _node: ast.AST, *, padded: bool = False) -> None:
        assert padded is False
        return None

    monkeypatch.setattr(gate.ast, "parse", fixed_tree)
    monkeypatch.setattr(gate.ast, "get_source_segment", none_segment)
    with pytest.raises(AssertionError, match="SOURCE_IDENTITY_NONE_SEGMENT"):
        source_segment_digest(
            TEST_PATH, kind="FunctionDef", qualname_or_target="probe", first_line=1
        )


@pytest.mark.parametrize(
    ("value", "label"),
    (
        (sys, "GRAPH_FORBIDDEN_MODULE_V1"),
        ([].append, "GRAPH_FORBIDDEN_CALLABLE_V1"),
        (len, "GRAPH_FORBIDDEN_CALLABLE_V1"),
        (MutableProbe(), "GRAPH_FORBIDDEN_OBJECT_V1"),
        (ApprovedProbe(1, 2), "GRAPH_FORBIDDEN_OBJECT_V1"),
    ),
)
def test_runtime_graph_rejects_forbidden_runtime_objects(value: object, label: str) -> None:
    _assert_graph_error(value, label)


def test_runtime_graph_accepts_exact_approved_record() -> None:
    result = walk_identity_graph(
        (ApprovedProbe("a", "b"),),
        _budgets(),
        _empty_policy(approved_record_types=(ApprovedProbe,)),
    )
    assert (result.nodes, result.edges, result.depth) == (3, 2, 1)
    schema_result = walk_identity_graph(
        (ApprovedProbe,),
        _budgets(),
        _empty_policy(approved_schema_types=(ApprovedProbe,)),
    )
    assert (schema_result.nodes, schema_result.edges, schema_result.depth) == (1, 0, 0)


def test_runtime_graph_rejects_forbidden_object_inside_cycle() -> None:
    cycle: list[object] = []
    cycle.extend((cycle, CallableProbe()))
    with pytest.raises(AssertionError, match="GRAPH_FORBIDDEN_CALLABLE_V1"):
        walk_identity_graph((cycle,), _budgets(), _empty_policy())


def test_runtime_graph_edges_overflow_is_stable() -> None:
    with pytest.raises(
        AssertionError,
        match="GRAPH_BUDGET_EXCEEDED_V1 metric=edges limit=1 observed_at_least=2",
    ):
        walk_identity_graph((("a", "b"),), GraphBudgets(10, 1, 10), _empty_policy())


def test_runtime_graph_depth_overflow_is_stable() -> None:
    with pytest.raises(
        AssertionError,
        match="GRAPH_BUDGET_EXCEEDED_V1 metric=depth limit=1 observed_at_least=2",
    ):
        walk_identity_graph(((("a",),),), GraphBudgets(10, 10, 1), _empty_policy())


def test_runtime_graph_nodes_overflow_is_stable() -> None:
    with pytest.raises(
        AssertionError,
        match="GRAPH_BUDGET_EXCEEDED_V1 metric=nodes limit=2 observed_at_least=3",
    ):
        walk_identity_graph((("a", "b"),), GraphBudgets(2, 10, 10), _empty_policy())


def test_budget_formula_and_caps_are_exact(tmp_path: Path) -> None:
    fixture = _fixture()
    assert freeze_budgets(fixture["graphBudgets"]["observed"]) == fixture["graphBudgets"]["frozen"]
    with pytest.raises(AssertionError, match="STRUCTURE_GATE_BUDGET_DESIGN_HOLD"):
        freeze_budgets({"nodes": 1025, "edges": 1, "depth": 1})
    mutations: list[tuple[dict[str, object], str]] = []
    wrong_caps = copy.deepcopy(fixture)
    wrong_caps["graphBudgets"]["hardCaps"]["nodes"] = 9999
    mutations.append((wrong_caps, "FIXTURE_BUDGET_HARD_CAPS_V1"))
    wrong_formula = copy.deepcopy(fixture)
    wrong_formula["graphBudgets"]["formula"] = "WRONG"
    mutations.append((wrong_formula, "FIXTURE_BUDGET_FORMULA_LABEL_V1"))
    wrong_priority = copy.deepcopy(fixture)
    wrong_priority["graphBudgets"]["metricPriority"] = ["nodes", "depth", "edges"]
    mutations.append((wrong_priority, "FIXTURE_BUDGET_PRIORITY_V1"))
    negative_observed = copy.deepcopy(fixture)
    negative_observed["graphBudgets"]["observed"]["nodes"] = -1
    mutations.append((negative_observed, "FIXTURE_BUDGET_METRICS_V1"))
    extra_metric = copy.deepcopy(fixture)
    extra_metric["graphBudgets"]["observed"]["extra"] = 1
    mutations.append((extra_metric, "FIXTURE_BUDGET_METRIC_KEYS_V1"))
    for index, (candidate, label) in enumerate(mutations):
        _assert_fixture_failure(candidate, label, tmp_path / f"budget-{index}.json")


def test_gate_implementation_closure_is_exact_and_bidirectional() -> None:
    observed = gate_implementation_closure(TEST_PATH, TEST_PATH.parent)
    assert observed == EXPECTED_GATE_FILES
    assert tuple(_fixture()["structureGatePythonFiles"]) == tuple(
        path.relative_to(REPOSITORY_ROOT).as_posix() for path in observed
    )


def test_third_helper_bypass_fails_closure_and_self_c901(tmp_path: Path) -> None:
    helper = tmp_path / "extra.py"
    entry = tmp_path / "entry.py"
    helper.write_text(
        "def complex_value(x):\n" + "    if x:\n        x -= 1\n" * 12 + "    return x\n"
    )
    entry.write_text("import extra\n")
    closure = gate_implementation_closure(entry, tmp_path)
    assert len(closure) == 2 and set(closure) != set(EXPECTED_GATE_FILES)
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--select",
            "C901",
            "--config",
            "lint.mccabe.max-complexity=10",
            str(helper),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 1 and "C901" in completed.stdout


def test_dynamic_test_local_load_is_rejected(tmp_path: Path) -> None:
    entry = tmp_path / "entry.py"
    entry.write_text("import importlib\nvalue = importlib.import_module('extra')\n")
    with pytest.raises(AssertionError, match="DYNAMIC_TEST_LOCAL_LOAD_V1"):
        gate_implementation_closure(entry, tmp_path)


def test_builder_oracle_rows_and_observed_maxima_match_fixture() -> None:
    _assert_builder_rows(_fixture())


@pytest.mark.parametrize("mutation", ("missing", "extra", "duplicate", "reordered", "tampered"))
def test_fixture_rejects_builder_manifest_mutations(tmp_path: Path, mutation: str) -> None:
    candidate = copy.deepcopy(_fixture())
    rows = candidate["builderNeutralFrontier"]
    if mutation == "missing":
        rows.pop()
    elif mutation == "extra":
        rows.append({**rows[-1], "qualname": "extra"})
    elif mutation == "duplicate":
        rows.append(copy.deepcopy(rows[-1]))
    elif mutation == "reordered":
        rows[0], rows[1] = rows[1], rows[0]
    else:
        rows[0]["sourceSegmentSha256"] = "0" * 64
        candidate["builderNeutralFrontierCount"] = len(rows)
    path = tmp_path / "fixture.json"
    _canonical_fixture(candidate, path)
    if mutation == "tampered":
        loaded = validate_fixture_bytes(path)
        with pytest.raises(AssertionError):
            _assert_builder_rows(loaded)
    else:
        with pytest.raises(AssertionError):
            validate_fixture_bytes(path)
    if mutation == "tampered":
        row_cases: list[tuple[dict[str, object], str]] = []
        wrong_algorithm = copy.deepcopy(_fixture())
        wrong_algorithm["identityAlgorithm"]["digest"] = "WRONG"
        row_cases.append((wrong_algorithm, "FIXTURE_IDENTITY_ALGORITHM_VALUE_V1"))
        extra_frontier_key = copy.deepcopy(_fixture())
        extra_frontier_key["frontier"][0]["extra"] = "forbidden"
        row_cases.append((extra_frontier_key, "FIXTURE_FRONTIER_ROW_KEYS_V1"))
        missing_legacy_key = copy.deepcopy(_fixture())
        del missing_legacy_key["legacyDeclarations"][0]["sourceSha256"]
        row_cases.append((missing_legacy_key, "FIXTURE_LEGACY_ROW_KEYS_V1"))
        extra_builder_key = copy.deepcopy(_fixture())
        extra_builder_key["builderNeutralFrontier"][0]["extra"] = "forbidden"
        row_cases.append((extra_builder_key, "FIXTURE_BUILDER_ROW_KEYS_V1"))
        for index, (row_candidate, label) in enumerate(row_cases):
            _assert_fixture_failure(row_candidate, label, tmp_path / f"row-{index}.json")


def test_fixture_rejects_preauthorized_unreachable_builder_row(tmp_path: Path) -> None:
    candidate = copy.deepcopy(_fixture())
    candidate["builderNeutralFrontier"].append(
        {**candidate["builderNeutralFrontier"][-1], "qualname": "unreachable"}
    )

    def builder_row_key(row: Mapping[str, object]) -> tuple[object, ...]:
        return row["module"], row["qualname"], row["sourcePath"], row["firstLine"]

    candidate["builderNeutralFrontier"].sort(key=builder_row_key)
    candidate["builderNeutralFrontierCount"] += 1
    path = tmp_path / "fixture.json"
    _canonical_fixture(candidate, path)
    loaded = validate_fixture_bytes(path)
    with pytest.raises(AssertionError):
        _assert_builder_rows(loaded)


def _assert_r3_failure(
    value: Mapping[str, object], label: str, path: Path = R3_DURABLE_PATH
) -> None:
    _canonical_fixture(value, path)
    with pytest.raises(AssertionError, match=f"^{label}$"):
        validate_durable_r3_receipt_v1(path)


@pytest.mark.parametrize(
    "mutation_group",
    ("commands", "tristate", "prior", "missing-input", "claim-ceiling"),
)
def test_r3_validator_rejects_synthetic_receipt_mutations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutation_group: str
) -> None:
    monkeypatch.chdir(tmp_path)
    baseline = _minimal_r3()
    _canonical_fixture(baseline, R3_DURABLE_PATH)
    assert validate_durable_r3_receipt_v1(R3_DURABLE_PATH) == baseline
    cases: list[tuple[dict[str, object], str]] = []
    if mutation_group == "commands":
        missing_command = _minimal_r3()
        missing_command["commands"].pop()
        cases.append((missing_command, "R3_COMMAND_SET_V1"))
        missing_rc = _minimal_r3()
        del missing_rc["commands"][0]["returnCode"]
        cases.append((missing_rc, "R3_COMMAND_FIELDS_V1"))
    elif mutation_group == "tristate":
        wrong_failed = _minimal_r3()
        wrong_failed["triState"]["failedNodeIds"] = []
        cases.append((wrong_failed, "R3_FAILED_SET_V1"))
        wrong_deferred = _minimal_r3()
        wrong_deferred["triState"]["deferredNodeIds"] = []
        cases.append((wrong_deferred, "R3_DEFERRED_SET_V1"))
        deferred_as_pass = _minimal_r3()
        deferred_as_pass["triState"]["passed"] += 1
        cases.append((deferred_as_pass, "R3_TRISTATE_COUNTS_V1"))
        deferred_as_red = _minimal_r3()
        deferred_as_red["triState"]["failedNodeIds"].append(EXPECTED_DEFERRED[0])
        cases.append((deferred_as_red, "R3_TRISTATE_OVERLAP_V1"))
    elif mutation_group == "prior":
        false_bytes = _minimal_r3()
        false_bytes["priorReceipts"][1]["bytesVerified"] = True
        cases.append((false_bytes, "R3_R2_BYTES_VERIFIED_V1"))
        rewritten_prior = _minimal_r3()
        rewritten_prior["priorReceipts"][1]["reportedSha256"] = "1" * 64
        cases.append((rewritten_prior, "R3_PRIOR_RECEIPTS_V1"))
    elif mutation_group == "missing-input":
        missing_input = _minimal_r3()
        del missing_input["inputs"][R3_INPUT_PATHS[0]]
        cases.append((missing_input, "R3_INPUT_SET_V1"))
    else:
        changed_ceiling = _minimal_r3()
        changed_ceiling["claimCeiling"] = "READY"
        cases.append((changed_ceiling, "R3_CLAIM_CEILING_V1"))
    for value, label in cases:
        _assert_r3_failure(value, label)


def test_r3_validator_rejects_non_durable_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    _assert_r3_failure(_minimal_r3(), "R3_NON_DURABLE_PATH_V1", Path("receipt.json"))


def test_current_contract_slot_schema_baseline_is_exact_without_primitive_module() -> None:
    assert all(
        tuple(field.name for field in fields(owner)) == slots for owner, slots in EXPECTED_SLOTS
    )


def test_contracts_verifier_static_inventory_has_no_hidden_dispatch_or_state() -> None:
    source = CONTRACTS_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    verifier_function = contracts_v2.verify_calibration_result
    first_line = verifier_function.__code__.co_firstlineno
    lexical_qualname = gate.lexical_qualname_at_line(CONTRACTS_PATH, first_line)
    assert lexical_qualname == (
        "_freeze_result_verifier_capsule_v2.<locals>.verify_calibration_result"
    )
    matches = tuple(
        node
        for qualname, node in gate.lexical_declarations(tree)
        if type(node) is ast.FunctionDef
        and qualname == lexical_qualname
        and node.lineno == first_line
    )
    assert len(matches) == 1
    verifier = matches[0]
    assert not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(verifier))
    assert not any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "__import__"
        for node in ast.walk(verifier)
    )


def test_builder_static_boundary_is_exact_and_has_no_primitive_reference() -> None:
    source = CALIBRATION_PATH.read_text(encoding="utf-8")
    assert "_verifier_primitives_v2" not in source
    assert source.count("verify_calibration_result") >= 1


def _require_primitive_module(reason: str) -> None:
    if not PRIMITIVES_PATH.is_file():
        pytest.skip(f"DEFERRED_UNTIL_MODULE_EXISTS: {reason}")


def test_verifier_primitives_module_exists() -> None:
    assert PRIMITIVES_PATH.is_file(), "typed verifier primitives module is missing"


def test_verifier_slice_has_no_c901_findings() -> None:
    paths = [str(CONTRACTS_PATH.relative_to(REPOSITORY_ROOT))]
    if PRIMITIVES_PATH.is_file():
        paths.append(str(PRIMITIVES_PATH.relative_to(REPOSITORY_ROOT)))
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--select",
            "C901",
            "--config",
            "lint.mccabe.max-complexity=10",
            *paths,
        ],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_verifier_slice_function_inventory_meets_span_and_parameter_gates() -> None:
    paths = [CONTRACTS_PATH] + ([PRIMITIVES_PATH] if PRIMITIVES_PATH.is_file() else [])
    violations: list[str] = []
    for path in paths:
        _raw, source = normalized_source(path)
        for shape in function_inventory(source):
            if shape.span > 120:
                violations.append(f"{path.name}:{shape.qualname}:span={shape.span}")
            if len(shape.parameters) > 8:
                violations.append(
                    f"{path.name}:{shape.qualname}:parameters={len(shape.parameters)}"
                )
            if shape.variadic:
                violations.append(f"{path.name}:{shape.qualname}:variadic={shape.variadic!r}")
    assert not violations, "\n".join(violations)


def test_primitive_static_inventory_has_no_hidden_dispatch_or_state() -> None:
    _require_primitive_module("primitive static inventory")
    assert not static_source_violations(PRIMITIVES_PATH.read_text(encoding="utf-8"))


def test_verifier_typed_topology_is_exact_and_complete() -> None:
    _require_primitive_module("typed callable-container topology")
    assert verifier_primitives_v2 is not None
    assert hasattr(verifier_primitives_v2, "VerifierPrimitiveOpsV2")


def test_public_verifier_runtime_graph_has_exact_primitive_ops_topology() -> None:
    _require_primitive_module("runtime primitive ops topology")
    assert contracts_v2.verify_calibration_result is not None


def test_runtime_verifier_slot_schema_covers_every_dataclass_field() -> None:
    _require_primitive_module("runtime verifier slot schemas")
    assert all(
        tuple(field.name for field in fields(owner)) == slots for owner, slots in EXPECTED_SLOTS
    )


def test_builder_runtime_graph_stops_only_at_exact_public_terminal_boundary() -> None:
    _require_primitive_module("builder runtime scientific-leaf topology")
    _assert_builder_rows(_fixture())
