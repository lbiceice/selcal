from __future__ import annotations

import hashlib
import json
import re
import shlex
from datetime import datetime
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPOSITORY_ROOT / "docs/status/scientific_code_smell_audit_20260831_v3.json"
CURRENT_BINDING = REPOSITORY_ROOT / "docs/status/scientific_code_smell_binding_20260920.json"
VERIFICATION_RECEIPT = (
    REPOSITORY_ROOT / "docs/status/input_resource_envelope_verification_20260831.json"
)
HISTORICAL_AUDITS = (
    REPOSITORY_ROOT / "docs/status/scientific_code_smell_audit_20260831.json",
    REPOSITORY_ROOT / "docs/status/scientific_code_smell_audit_20260831_v2.json",
)
PRESSURE_HARNESS = REPOSITORY_ROOT / "scripts/verify_input_resource_pressure.py"
PACKAGE_INSTALL_HARNESS = REPOSITORY_ROOT / "scripts/verify_input_package_install.py"

EXPECTED_CHARACTERIZATION_NODE_IDS = [
    f"tests/test_input_npz_limits.py::"
    f"test_public_npz_rejection_mutations_reach_target_branch[{case}]"
    for case in (
        "trailing_partial_extra_header",
        "zip64_payload_missing",
        "zip64_ordinary_uncompressed_mismatch",
        "zip64_ordinary_compressed_mismatch",
        "local_offset_out_of_range",
        "bad_local_signature",
        "local_variable_fields_enter_central",
        "member_data_enters_central",
        "central_record_too_short",
        "bad_central_signature",
        "central_size_sentinel",
        "central_record_overflow",
        "npy_missing_header_length",
    )
] + [
    "tests/test_input_npz_limits.py::test_public_npz_rejects_numpy_header_cursor_contract_drift",
    "tests/test_input_csv_limits.py::"
    "test_public_csv_malformed_header_uses_header_exception_boundary",
]

EXPECTED_LIMITS = {
    "CSV_RAW_BYTES": 67_108_864,
    "CSV_RECORD_CHARACTERS": 1_024,
    "CSV_FIELD_CHARACTERS": 256,
    "CSV_DATA_ROWS": 1_000_000,
    "NPZ_RAW_BYTES": 33_554_432,
    "NPZ_CENTRAL_DIRECTORY_BYTES": 16_384,
    "NPY_HEADER_BYTES": 4_096,
    "NPY_ELEMENTS": 1_000_000,
    "NPZ_MEMBER_UNCOMPRESSED_BYTES": 8_004_108,
    "NPZ_TOTAL_UNCOMPRESSED_BYTES": 16_008_216,
}

EXPECTED_RED_GREEN_EVIDENCE = {
    "INITIAL_AUDIT_MISSING_RED": {
        "phase": "RED",
        "status": "EXPECTED_TDD_RED",
        "exitCode": 1,
        "command": (".venv/bin/python -m pytest tests/test_scientific_code_smell_audit.py -q"),
        "result": (
            "10 failed because the canonical v3 audit, input verification receipt "
            "and README contract section did not yet exist"
        ),
        "counts": {"failed": 10, "passed": 0, "skipped": 0},
        "provenance": ("RAW_OUTPUT_NOT_RETAINED_COUNT_SUMMARY_RECORDED_DURING_ORIGINAL_RUN"),
    },
    "BENCHMARK_SOURCE_BINDING_RED": {
        "phase": "RED",
        "status": "EXPECTED_SOURCE_BINDING_RED",
        "exitCode": 1,
        "command": (
            ".venv/bin/python -m pytest tests/test_benchmark_in_memory.py "
            "tests/test_benchmark_plot.py -q"
        ),
        "result": (
            "1 source-identity failure because the retained benchmark receipt bound "
            "30 source files while the frozen candidate contained 32"
        ),
        "counts": {"failed": 1, "passed": 5, "skipped": 0},
        "provenance": ("RAW_OUTPUT_NOT_RETAINED_COUNT_SUMMARY_RECORDED_DURING_ORIGINAL_RUN"),
    },
    "CHARACTERIZATION_BRANCH_COVERAGE_GREEN": {
        "phase": "GREEN",
        "status": "CHARACTERIZATION_COVERAGE_PASS_NOT_CLAIMED_AS_RED",
        "exitCode": 0,
        "command": (
            ".venv/bin/python -m pytest tests/test_input_npz_limits.py "
            "tests/test_input_csv_limits.py -k "
            "'reach_target_branch or cursor_contract_drift or malformed_header' -q"
        ),
        "result": "15 passed",
        "counts": {"failed": 0, "passed": 15, "skipped": 0},
        "provenance": "CURRENT_REPLAYABLE_COMMAND_OBSERVATION",
    },
    "BENCHMARK_REGEN_GREEN": {
        "phase": "GREEN",
        "status": "PASS",
        "exitCode": 0,
        "command": (
            ".venv/bin/python -m pytest tests/test_benchmark_in_memory.py "
            "tests/test_benchmark_plot.py -q"
        ),
        "result": (
            "6 passed after serial regeneration through the existing benchmark and plot route"
        ),
        "counts": {"failed": 0, "passed": 6, "skipped": 0},
        "provenance": "CURRENT_REPLAYABLE_COMMAND_OBSERVATION",
    },
    "SPEC_REVIEW_EVIDENCE_RED": {
        "phase": "RED",
        "status": "EXPECTED_SPEC_REVIEW_TDD_RED",
        "exitCode": 1,
        "command": (".venv/bin/python -m pytest tests/test_scientific_code_smell_audit.py -q"),
        "result": (
            "5 failed and 10 passed because pressure claim ceiling, Task3 RED "
            "provenance, Task4 attribution, current-wheel build/clean-install and "
            "final-verification identity were absent"
        ),
        "counts": {"failed": 5, "passed": 10, "skipped": 0},
        "provenance": ("RAW_OUTPUT_NOT_RETAINED_COUNT_SUMMARY_RECORDED_DURING_ORIGINAL_RUN"),
    },
    "QUALITY_REVIEW_EVIDENCE_RED": {
        "phase": "RED",
        "status": "EXPECTED_QUALITY_HOLD_TDD_RED",
        "exitCode": 1,
        "command": (".venv/bin/python -m pytest tests/test_scientific_code_smell_audit.py -q"),
        "result": (
            "6 failed and 6 passed because exact selector/count provenance, resolved "
            "matrix cells, replayable pressure/package harness bindings, Task10 "
            "aggregation and readiness recomputation were absent"
        ),
        "counts": {"failed": 6, "passed": 6, "skipped": 0},
        "provenance": ("RAW_OUTPUT_NOT_RETAINED_COUNT_SUMMARY_RECORDED_DURING_ORIGINAL_RUN"),
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _payload() -> dict[str, object]:
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def _verification_payload() -> dict[str, object]:
    return json.loads(VERIFICATION_RECEIPT.read_text(encoding="utf-8"))


def _verify_audit_source_binding(binding: dict[str, object]) -> None:
    payload = _payload()
    assert binding["priorAuditSha256"] == _sha256(AUDIT)
    assert binding["status"] == "HISTORICAL_AUDIT_CURRENT_SOURCE_DELTA_ONLY"
    assert binding["fullCodeSmellAuditReperformed"] is False
    assert binding["historicalFindingsPromoted"] is False
    assert binding["scientificValidation"] is False
    preimage_bound = binding["preimageBoundSource"]
    assert preimage_bound["path"] == "src/selcal/contracts_v2.py"
    assert preimage_bound["preimagePath"] == (
        "docs/status/evidence/product_gate_repair_20260908/"
        "contracts_v2.pre-extraction-20260908.py.txt"
    )
    assert preimage_bound["preimageSha256"] == _sha256(
        REPOSITORY_ROOT / preimage_bound["preimagePath"]
    )
    assert preimage_bound["currentSha256"] == _sha256(REPOSITORY_ROOT / preimage_bound["path"])
    added_paths = {"src/selcal/_verifier_primitives_v2.py"}
    for added in binding["addedSources"]:
        assert added["sha256"] == _sha256(REPOSITORY_ROOT / added["path"])
    assert added_paths <= {added["path"] for added in binding["addedSources"]}
    sources = payload["sourceIdentity"]
    assert isinstance(sources, list)
    assert {source["path"] for source in sources} == {
        "src/selcal/calibration_v2.py",
        "src/selcal/contracts_v2.py",
        "src/selcal/input_resources.py",
        "src/selcal/inputs.py",
        "src/selcal/migration_v1_to_v2.py",
        "src/selcal/npz_safe.py",
        "src/selcal/nulls/block_shuffle_v2.py",
        "src/selcal/nulls/circular_shift_v2.py",
        "src/selcal/nulls/owned_transform_v2.py",
        "src/selcal/randomness.py",
        "src/selcal/resolution_v2.py",
        "src/selcal/statistics/binned_nette.py",
        "src/selcal/statistics/lagged_pearson.py",
    }
    changed_rows = {row["path"]: row for row in binding["changedSincePriorAudit"]}
    unchanged_count = 0
    for source in sources:
        path = REPOSITORY_ROOT / source["path"]
        assert path.is_file()
        current = _sha256(path)
        if source["path"] in changed_rows:
            row = changed_rows[source["path"]]
            # The audit digest is retained as history; current bytes must differ from it.
            assert row["auditSha256"] == source["sha256"]
            assert row["currentSha256"] == current
            assert current != source["sha256"]
        else:
            assert source["sha256"] == current
            unchanged_count += 1
    assert binding["unchangedPriorSourceCount"] == unchanged_count


def test_audit_binds_every_cited_production_source() -> None:
    _verify_audit_source_binding(json.loads(CURRENT_BINDING.read_text(encoding="utf-8")))


@pytest.mark.parametrize(
    "location",
    ("audit", "preimage", "changed", "extracted", "unchanged"),
)
def test_historical_binding_rejects_changed_evidence_bytes(
    monkeypatch: pytest.MonkeyPatch,
    location: str,
) -> None:
    binding = json.loads(CURRENT_BINDING.read_text(encoding="utf-8"))
    paths = {
        "audit": AUDIT,
        "preimage": REPOSITORY_ROOT / binding["preimageBoundSource"]["preimagePath"],
        "changed": REPOSITORY_ROOT / binding["preimageBoundSource"]["path"],
        "extracted": REPOSITORY_ROOT / binding["addedSources"][0]["path"],
        "unchanged": REPOSITORY_ROOT / "src/selcal/inputs.py",
    }
    actual_sha256 = _sha256
    monkeypatch.setitem(
        globals(),
        "_sha256",
        lambda path: "0" * 64 if path == paths[location] else actual_sha256(path),
    )
    with pytest.raises(AssertionError):
        _verify_audit_source_binding(binding)


def test_audit_preserves_adverse_findings_and_evidence_classes() -> None:
    payload = _payload()
    findings = payload["findings"]
    assert payload["status"] == "MAJOR_REMEDIATION_REQUIRED_BEFORE_M3_M6_EXTENSION"
    assert payload["summary"] == {
        "blocker": 0,
        "majorOpen": 2,
        "majorResolvedInCurrentCandidate": 2,
        "minorOpen": 2,
    }
    assert {finding["id"] for finding in findings} == {
        "SCI-MAJOR-VERIFIER-COMPLEXITY",
        "SCI-MAJOR-HIDDEN-RUNTIME-STATE",
        "SCI-MAJOR-PEARSON-EXCEPTION-COLLAPSE",
        "SCI-MAJOR-INPUT-RESOURCE-BOUNDS",
        "SCI-MINOR-DUPLICATE-RNG-NULL-VALIDATION",
        "SCI-MINOR-NUMERIC-BACKEND-IDENTITY",
    }
    assert all(
        finding["evidenceClass"] in {"TOOL_MEASURED", "STATIC_CONFIRMED", "STATIC_RISK_INFERENCE"}
        for finding in findings
    )
    resolved = {
        finding["id"]
        for finding in findings
        if finding["status"] == "RESOLVED_IN_CURRENT_CANDIDATE"
    }
    assert resolved == {
        "SCI-MAJOR-PEARSON-EXCEPTION-COLLAPSE",
        "SCI-MAJOR-INPUT-RESOURCE-BOUNDS",
    }
    assert all(finding["status"] == "OPEN" for finding in findings if finding["id"] not in resolved)

    input_finding = next(
        finding for finding in findings if finding["id"] == "SCI-MAJOR-INPUT-RESOURCE-BOUNDS"
    )
    evidence = input_finding["resolutionEvidence"]
    assert evidence["receipt"] == {
        "path": "docs/status/input_resource_envelope_verification_20260831.json",
        "sha256": _sha256(VERIFICATION_RECEIPT),
    }
    assert evidence["focusedTests"] == "314 passed, 1 skipped"


def test_audit_does_not_promote_local_checks_to_cross_platform_evidence() -> None:
    payload = _payload()
    verification = payload["verification"]
    assert verification["originalAuditTargetedTests"] == "225 passed, 1 skipped"
    assert verification["laggedPearsonFocusedTests"] == "53 passed"
    assert verification["inputResourceFocusedTests"] == "314 passed, 1 skipped"
    assert verification["moduleAcceptance"]["status"] == "PASS"
    assert verification["unfilteredSuite"] == {
        "status": "EXPECTED_ADVERSE_TASK10_SCOPE_V1_RETAINED",
        "failures": 12,
    }
    assert verification["exactLockedRuff"] == "PASS_RUFF_0.16.5"
    assert verification["repositoryHygiene"] == "PASS_ZERO_FINDINGS"
    assert verification["freshMypyEvidence"] == "PASS_STRICT"
    assert verification["crossPlatformNumericCounterexample"] == "NOT_EXECUTED"
    assert payload["claimCeiling"] == (
        "READ_ONLY_STATIC_AND_LOCAL_TEST_EVIDENCE_NOT_SCIENTIFIC_VALIDATION"
    )
    _assert_final_verification_identity_and_readiness_are_explicit()


def test_audit_preserves_both_adverse_receipts_by_hash() -> None:
    payload = _payload()
    assert payload["historicalReceipts"] == [
        {
            "path": str(path.relative_to(REPOSITORY_ROOT)),
            "sha256": _sha256(path),
            "status": "HISTORICAL_ADVERSE_RECEIPT_RETAINED",
        }
        for path in HISTORICAL_AUDITS
    ]


def test_shared_environment_mutation_is_retained_as_an_adverse_observation() -> None:
    payload = _payload()
    environment = payload["environmentObservation"]
    assert environment["sharedProjectVenvAuthoritative"] is False
    assert environment["trackedRepositoryBytesChangedByAudit"] is False
    assert environment["status"] == "VOLATILE_EXCLUDED_FROM_AUTHORITY"


def test_input_verification_receipt_binds_exact_contract_and_current_sources() -> None:
    payload = _verification_payload()
    assert payload["schemaVersion"] == "selcal-input-resource-envelope-verification-v1.1"
    assert payload["status"] == ("INPUT_RESOURCE_ENVELOPE_V1_1_RESOLVED_IN_CURRENT_CANDIDATE")
    assert payload["exactLimits"] == EXPECTED_LIMITS
    sources = payload["sourceIdentity"]
    assert {source["path"] for source in sources} == {
        "src/selcal/inputs.py",
        "src/selcal/input_resources.py",
        "src/selcal/npz_safe.py",
    }
    for source in sources:
        assert source["sha256"] == _sha256(REPOSITORY_ROOT / source["path"])
    assert payload["claimCeiling"] == (
        "LOCAL_ENGINEERING_VERIFICATION_NOT_STREAMING_NOT_SECURITY_CERTIFICATION_"
        "NOT_CROSS_PLATFORM_NOT_M6_NOT_RELEASE_NOT_SUBMISSION"
    )
    _assert_task4_attribution_is_bounded_and_does_not_claim_dirty_tree_ownership()
    _assert_current_bytes_have_local_build_and_clean_wheel_install_evidence()


def test_input_verification_receipt_retains_red_green_and_task10_evidence() -> None:
    payload = _verification_payload()
    verification = payload["verification"]
    assert verification["focusedInputSuite"] == {
        "command": (
            ".venv/bin/python -m pytest tests/test_input_resources.py "
            "tests/test_input_csv_limits.py tests/test_input_npz_limits.py "
            "tests/test_inputs.py -q"
        ),
        "exitCode": 0,
        "result": "314 passed, 1 skipped",
        "status": "PASS",
    }
    assert verification["moduleAcceptance"]["exitCode"] == 0
    assert verification["moduleAcceptance"]["status"] == "PASS"
    assert verification["unfilteredSuite"]["exitCode"] != 0
    assert verification["unfilteredSuite"]["failed"] == 12
    assert verification["unfilteredSuite"]["status"] == (
        "EXPECTED_ADVERSE_TASK10_SCOPE_V1_RETAINED"
    )
    assert verification["coverage"]["exitCode"] == 0
    assert verification["coverage"]["combinedOpportunityCoveragePercent"] == (95.14908256880734)
    assert verification["coverage"]["lineCoveragePercent"] == 96.35639926515616
    assert verification["coverage"]["branchCoveragePercent"] == 91.54478976234003
    assert verification["coverage"]["combinedOpportunityCoveragePercent"] >= 95.07
    assert verification["coverage"]["thresholdPercent"] == 80.0
    assert verification["ruff"]["status"] == "PASS_RUFF_0.16.5"
    assert verification["mypy"]["status"] == "PASS_STRICT"
    assert verification["repositoryHygiene"]["status"] == "PASS_ZERO_FINDINGS"
    assert verification["uvLockCheck"]["status"] == "PASS"
    assert verification["gitDiffCheck"]["status"] == "PASS"

    red_green = payload["redGreenEvidence"]
    assert any(item["phase"] == "RED" and item["exitCode"] != 0 for item in red_green)
    assert any(item["phase"] == "GREEN" and item["exitCode"] == 0 for item in red_green)
    _assert_input_receipt_locks_exact_module_and_coverage_recomputation()
    _assert_task3_red_evidence_is_explicit_about_raw_log_limitations()


def test_receipt_evidence_entries_have_exact_selectors_nodes_and_counts() -> None:
    payload = _verification_payload()
    entries = payload["redGreenEvidence"]
    assert len(entries) == 6
    assert all("evidenceId" in item for item in entries)
    entries_by_id = {item["evidenceId"]: item for item in entries}
    assert len(entries_by_id) == len(entries)
    assert set(entries_by_id) == set(EXPECTED_RED_GREEN_EVIDENCE)
    for evidence_id, expected in EXPECTED_RED_GREEN_EVIDENCE.items():
        item = entries_by_id[evidence_id]
        assert {key: item[key] for key in expected} == expected

    characterization = entries_by_id["CHARACTERIZATION_BRANCH_COVERAGE_GREEN"]
    selector = "reach_target_branch or cursor_contract_drift or malformed_header"
    assert characterization["selector"] == selector
    assert characterization["nodeIds"] == EXPECTED_CHARACTERIZATION_NODE_IDS


def _assert_input_receipt_locks_exact_module_and_coverage_recomputation() -> None:
    verification = _verification_payload()["verification"]
    module = verification["moduleAcceptance"]
    assert module == {
        "command": (
            ".venv/bin/python -m pytest "
            "--ignore=tests/task10/test_authority_amendment_scope_v1.py -q"
        ),
        "exitCode": 0,
        "passed": 2851,
        "skipped": 1,
        "status": "PASS",
    }

    coverage = verification["coverage"]
    assert coverage["command"] == (
        ".venv/bin/python -m pytest "
        "--ignore=tests/task10/test_authority_amendment_scope_v1.py "
        "--cov=selcal --cov-branch --cov-report=term-missing -q"
    )
    assert coverage["exitCode"] == 0
    assert coverage["coveredLines"] + coverage["missingLines"] == coverage["numStatements"]
    assert coverage["coveredBranches"] + coverage["missingBranches"] == coverage["numBranches"]
    assert coverage["coveredOpportunities"] == (
        coverage["coveredLines"] + coverage["coveredBranches"]
    )
    assert coverage["totalOpportunities"] == (coverage["numStatements"] + coverage["numBranches"])
    assert coverage["lineCoveragePercent"] == (
        100 * coverage["coveredLines"] / coverage["numStatements"]
    )
    assert coverage["branchCoveragePercent"] == (
        100 * coverage["coveredBranches"] / coverage["numBranches"]
    )
    assert coverage["combinedOpportunityCoveragePercent"] == (
        100 * coverage["coveredOpportunities"] / coverage["totalOpportunities"]
    )
    assert coverage["combinedOpportunityCoveragePercent"] >= 95.07


def test_input_compatibility_matrix_runs_the_full_npz_limit_file() -> None:
    payload = _verification_payload()
    matrix = payload["compatibilityMatrix"]
    assert matrix["status"] == "FINITE_SAME_MACHINE_COMPATIBILITY_EVIDENCE_ONLY"
    assert matrix["crossPlatform"] is False
    entries = matrix["entries"]
    assert {(item["requestedPython"], item["requestedNumPy"]) for item in entries} == {
        ("3.11", "1.26.4"),
        ("3.11", "2.4.6"),
        ("3.12", "1.26.4"),
        ("3.12", "2.4.6"),
        ("3.13", "LATEST_INSTALLABLE_2_X_AT_CHECKPOINT"),
        ("3.14", "LATEST_INSTALLABLE_2_X_AT_CHECKPOINT"),
    }
    assert len(entries) == 6
    assert all(item["status"] == "PASS" for item in entries)
    observed_machines = set()
    observed_commands = set()
    observed_actual_cells = set()
    for item in entries:
        assert item["testTarget"] == "tests/test_input_npz_limits.py"
        command = shlex.split(item["command"])
        requested_python = item["requestedPython"]
        requested_numpy = item["requestedNumPy"]
        numpy_selector = (
            "numpy>=2,<3"
            if requested_numpy == "LATEST_INSTALLABLE_2_X_AT_CHECKPOINT"
            else f"numpy=={requested_numpy}"
        )
        assert command == [
            "PYTHONPATH=src",
            "uv",
            "run",
            "--no-project",
            "--python",
            requested_python,
            "--with",
            numpy_selector,
            "--with",
            "pytest==8.4.2",
            "python",
            "-m",
            "pytest",
            "tests/test_input_npz_limits.py",
            "-q",
        ]
        assert item["exitCode"] == 0
        assert item["passed"] == 150
        assert item["skipped"] == 0
        assert item["environment"]["pythonImplementation"] == "CPython"
        assert item["environment"]["os"] == "Darwin"
        assert item["environment"]["architecture"] == "arm64"
        assert item["environment"]["zlib"]
        assert re.fullmatch(
            rf"{re.escape(requested_python)}\.\d+",
            item["environment"]["python"],
        )
        if requested_numpy == "LATEST_INSTALLABLE_2_X_AT_CHECKPOINT":
            assert item["resolvedNumPyAtCheckpoint"] == item["environment"]["numpy"]
            assert re.fullmatch(r"2\.\d+\.\d+", item["environment"]["numpy"])
        else:
            assert item["environment"]["numpy"] == requested_numpy
            assert item["resolvedNumPyAtCheckpoint"] == requested_numpy
        observed_commands.add(item["command"])
        observed_actual_cells.add((item["environment"]["python"], item["environment"]["numpy"]))
        observed_machines.add(
            (
                item["environment"]["os"],
                item["environment"]["osRelease"],
                item["environment"]["architecture"],
            )
        )
    assert len(observed_machines) == 1
    assert len(observed_commands) == len(entries)
    assert len(observed_actual_cells) == len(entries)


def test_input_pressure_observation_is_local_serial_and_source_bound() -> None:
    payload = _verification_payload()
    observation = payload["pressureObservation"]
    assert observation["status"] == "LOCAL_DESIGN_PRESSURE_OBSERVATION_ONLY"
    assert observation["execution"] == {
        "freshSubprocessPerCase": True,
        "parallel": False,
        "temporaryInputsRetained": False,
    }
    assert observation["claimCeiling"] == (
        "LOCAL_DESIGN_PRESSURE_OBSERVATION_ONLY_NOT_PERFORMANCE_GUARANTEE_"
        "NOT_STREAMING_NOT_SECURITY_CERTIFICATION_NOT_CROSS_PLATFORM_NOT_M6"
    )
    assert observation["sourceIdentity"] == _verification_payload()["sourceIdentity"]
    method = observation["method"]
    assert method["command"] == (
        "PYTHONPATH=src uv run --no-project --python 3.11 --with numpy==2.4.6 "
        "--with psutil==7.0.0 python scripts/verify_input_resource_pressure.py "
        "--output <temporary-receipt-path>"
    )
    assert method["harnessPath"] == "scripts/verify_input_resource_pressure.py"
    assert method["harnessSha256"] == _sha256(PRESSURE_HARNESS)
    assert method["formats"] == ["CSV", "NPZ"]
    assert method["sizes"] == [10_000, 100_000, 250_000, 1_000_000]
    assert method["dtype"] == "float64"
    assert method["npzStorage"] == "NPZ_STORED"
    assert method["repeatCount"] == 1
    assert method["rssSampleIntervalSeconds"] == 0.001
    assert (
        method["inputGenerationContractSha256"]
        == hashlib.sha256(method["inputGenerationContract"].encode("utf-8")).hexdigest()
    )
    assert "shorter than" in method["rssSamplingLimitation"]
    assert "may miss" in method["rssSamplingLimitation"]
    assert method["temporaryWorkspace"].startswith("Created with tempfile.TemporaryDirectory")
    cases = observation["cases"]
    assert len(cases) == 8
    assert {(case["format"], case["rowsOrElements"]) for case in cases} == {
        (input_format, size)
        for input_format in ("CSV", "NPZ")
        for size in (10_000, 100_000, 250_000, 1_000_000)
    }
    for case in cases:
        assert case["status"] == "PASS"
        assert len(case["inputSha256"]) == 64
        assert case["repeatIndex"] == 1
        assert case["dtype"] == "float64"
        assert case["generationContractSha256"] == method["inputGenerationContractSha256"]
        assert case["wallSeconds"] >= 0
        assert case["rawBytes"] >= 0
        assert case["arrayPayloadBytes"] >= 0
        assert case["tracemallocPeakBytes"] >= 0
        assert case["rssBaselineBytes"] >= 0
        assert case["rssPeakBytes"] >= case["rssBaselineBytes"]
        assert case["rssDeltaBytes"] == (case["rssPeakBytes"] - case["rssBaselineBytes"])


def _assert_task3_red_evidence_is_explicit_about_raw_log_limitations() -> None:
    payload = _verification_payload()
    evidence = payload["task3TddRedEvidence"]
    assert {item["requirement"] for item in evidence} == {
        "PUBLIC_ZLIB_PATH",
        "STDLIB_ZIPFILE_FORBIDDEN",
        "SINGLE_DECOMPRESSOR",
        "UNCONSUMED_TAIL_DRAINED_FIRST",
        "NO_FLUSH",
        "TRUE_EOF_AND_EXACT_RANGE",
        "CRC_ORDER",
        "RESOURCE_PRIORITY",
    }
    for item in evidence:
        assert item["status"] == (
            "TDD_RED_OBSERVED_DURING_TASK3_IMPLEMENTATION_NOT_RETAINED_AS_RAW_LOG"
        )
        assert item["testNames"]
        assert item["failureNature"]
        assert item["subsequentGreen"] == "CURRENT_TARGET_TESTS_PASS"


def _assert_task4_attribution_is_bounded_and_does_not_claim_dirty_tree_ownership() -> None:
    attribution = _verification_payload()["task4Attribution"]
    expected_sources = {
        source["path"]: source["sha256"] for source in _verification_payload()["sourceIdentity"]
    }
    assert attribution["productionHashesAtStart"] == expected_sources
    assert attribution["productionHashesAtFinal"] == expected_sources
    assert attribution["productionBytesChangedByTask4"] is False
    assert set(attribution["implementerActionLogTouchedPaths"]) == {
        "README.md",
        "docs/benchmarks/in_memory_standard_20260831.json",
        "docs/benchmarks/in_memory_standard_20260831_figure.png",
        "docs/benchmarks/in_memory_standard_20260831_figure.svg",
        "docs/status/input_resource_envelope_verification_20260831.json",
        "docs/status/scientific_code_smell_audit_20260831_v3.json",
        "docs/status/softwarex_readiness_20260831.md",
        "tests/test_input_csv_limits.py",
        "tests/test_input_npz_limits.py",
        "tests/test_scientific_code_smell_audit.py",
        "scripts/verify_input_package_install.py",
        "scripts/verify_input_resource_pressure.py",
    }
    assert attribution["provenance"] == (
        "IMPLEMENTER_ACTION_LOG_PLUS_CURRENT_DIFF_NOT_CRYPTOGRAPHIC_OWNERSHIP_PROOF"
    )
    assert "dirty" in attribution["limitation"].lower()


def _assert_current_bytes_have_local_build_and_clean_wheel_install_evidence() -> None:
    evidence = _verification_payload()["packageBuildCleanInstall"]
    assert evidence["status"] == "PASS_LOCAL_CURRENT_WHEEL_ONLY"
    assert evidence["claimCeiling"] == (
        "LOCAL_PACKAGE_BUILD_AND_CLEAN_INSTALL_EVIDENCE_NOT_RELEASE_NOT_LICENCE_"
        "NOT_CROSS_PLATFORM_NOT_M6_NOT_SUBMISSION"
    )
    assert evidence["exactArtifactsRetained"] is False
    assert evidence["artifactDisposition"] == "DELETED_AFTER_TEMPORARY_VERIFICATION"
    assert evidence["artifactHashEvidence"] == (
        "EXECUTION_TIME_OBSERVATION_NOT_INDEPENDENTLY_REINSPECTABLE"
    )
    assert evidence["harness"] == {
        "path": "scripts/verify_input_package_install.py",
        "sha256": _sha256(PACKAGE_INSTALL_HARNESS),
    }
    assert evidence["supersededDistArtifact"] == {
        "path": "dist/selcal-0.1.0.dev0-py3-none-any.whl",
        "sha256": "41ff1ea7c303008e9eebc1f6c64c9324e2eb8645b3fdc23174da27456f2d27f7",
        "status": "SUPERSEDED_NOT_CURRENT_NOT_USED",
    }
    build = evidence["build"]
    assert build["command"] == (
        "<verification-python> -m build --outdir <temporary-build-dir>/artifacts"
    )
    assert build["exitCode"] == 0
    assert build["environment"]["python"] == "3.11.12"
    artifacts = build["artifacts"]
    assert {item["name"] for item in artifacts} == {
        "selcal-0.1.0.dev0-py3-none-any.whl",
        "selcal-0.1.0.dev0.tar.gz",
    }
    assert all(len(item["sha256"]) == 64 for item in artifacts)

    clean = evidence["cleanInstall"]
    assert clean["installedFrom"] == "CURRENT_WHEEL_ONLY_NOT_EDITABLE_NOT_SOURCE_TREE"
    assert clean["exitCode"] == 0
    assert clean["environment"]["pythonImplementation"] == "CPython"
    assert clean["environment"]["python"] == "3.11.12"
    assert clean["environment"]["numpy"]
    assert clean["packageMetadata"] == {"name": "selcal", "version": "0.1.0.dev0"}
    assert clean["repositoryPathOnSysPath"] is False
    assert clean["sourceTreeExcluded"] is True
    assert clean["cwdWasTemporaryWorkspace"] is True
    assert "/clean-venv/lib/python3.11/site-packages/selcal/__init__.py" in clean["packageFile"]
    assert clean["wheelRecordCheck"] == "PASS"
    assert clean["sourceModulePresence"] == [
        "selcal/input_resources.py",
        "selcal/inputs.py",
        "selcal/npz_safe.py",
    ]
    assert clean["publicSmoke"] == {
        "csv": "PASS",
        "npzDeflatedPublicZlib": "PASS",
        "npzStored": "PASS",
    }


def _assert_final_verification_identity_and_readiness_are_explicit() -> None:
    payload = _verification_payload()
    observed_at = payload["finalVerificationObservedAt"]
    assert datetime.fromisoformat(observed_at).tzinfo is not None
    final = payload["postWriteFinalVerification"]
    assert final["observedAt"] == observed_at
    assert final["sourceIdentity"] == payload["sourceIdentity"]
    assert final["status"] == "PASS_WITH_EXPECTED_TASK10_ADVERSE_RESULT"
    assert final["receiptSelfVerification"] == (
        "TARGETED_POST_RECEIPT_TEST_ONLY_NOT_SELF_CONTAINED_CRYPTOGRAPHIC_PROOF"
    )
    assert final["results"] == {
        "benchmarkAndAudit": "18 passed",
        "buildCleanInstall": "PASS_LOCAL_CURRENT_WHEEL_ONLY",
        "coverageCombinedOpportunityPercent": 95.14908256880734,
        "diffCheck": "PASS",
        "focusedInput": "314 passed, 1 skipped",
        "hygiene": "12 passed",
        "lock": "51 packages resolved",
        "moduleAcceptance": "2851 passed, 1 skipped",
        "mypy": "PASS_STRICT_32_FILES",
        "ruff": "PASS_RUFF_0.16.5",
        "unfiltered": "2891 passed, 1 skipped, 12 expected failures",
    }
    readiness = (REPOSITORY_ROOT / "docs/status/softwarex_readiness_20260831.md").read_text(
        encoding="utf-8"
    )
    assert _sha256(VERIFICATION_RECEIPT)[:8] in readiness
    declared = float(re.search(r"Declared overall readiness: \*\*([0-9.]+)%", readiness).group(1))
    rows = re.findall(
        r"^\| (?!\*\*Total)([^|]+) \| ([0-9]+) \| ([0-9]+) \| ([0-9.]+) \|",
        readiness,
        flags=re.MULTILINE,
    )
    assert len(rows) == 15
    assert sum(int(weight) for _, weight, _, _ in rows) == 100
    assert all(
        float(points) == int(weight) * int(completion) / 100
        for _, weight, completion, points in rows
    )
    assert declared == sum(float(points) for _, _, _, points in rows) == 42.00
    verification = payload["verification"]
    module = verification["moduleAcceptance"]
    assert f"`{module['passed']} passed, {module['skipped']} skipped`" in readiness
    coverage = verification["coverage"]
    for key in (
        "combinedOpportunityCoveragePercent",
        "lineCoveragePercent",
        "branchCoveragePercent",
    ):
        assert f"{coverage[key]}%" in readiness
    for item in payload["compatibilityMatrix"]["entries"]:
        assert item["environment"]["python"] in readiness
        assert item["environment"]["numpy"] in readiness
    for artifact in payload["packageBuildCleanInstall"]["build"]["artifacts"]:
        assert artifact["sha256"][:8] in readiness
    task10 = verification["task10Aggregate"]
    assert f"`{task10['passed']} passed, {task10['failed']} failed`" in readiness
    assert verification["unfilteredSuite"]["failed"] == task10["failed"]
    assert "not an acceptance probability" in readiness
