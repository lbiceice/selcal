from __future__ import annotations

import importlib.util
import json
import os
import stat
from copy import deepcopy
from pathlib import Path

import pytest

# Retired 2026-09-22 (author decision): a historical governance gate bound to the 2026-08-30 review
# baseline (git HEAD 94f993b, STOP_ON_ANY_BASELINE_HASH_DRIFT). It fails by design on any later
# change and is not a product test. Kept unchanged; run with SELCAL_RUN_RETIRED_GATES=1.
# Record: docs/status/retired_task10_gate_20260922.md
pytestmark = pytest.mark.skipif(
    os.environ.get("SELCAL_RUN_RETIRED_GATES") != "1",
    reason="retired historical governance gate (2026-09-22); set SELCAL_RUN_RETIRED_GATES=1",
)

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "docs/superpowers/specs/task10/v10/authority-amendment/review"
VALIDATOR = REVIEW / "validate_authority_amendment_scope_v1.py"
TARGET_MAP = REVIEW / "authority-amendment-target-map-v1.json"
BASELINE = REVIEW / "authority-amendment-baseline-v1.json"
PREDECESSOR = (
    ROOT
    / "docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md"
)
REGISTRY = (
    ROOT
    / "docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v2.json"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("authority_scope_validator", VALIDATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_inputs() -> tuple[dict[str, object], str, dict[str, object]]:
    return (
        json.loads(TARGET_MAP.read_text("utf-8")),
        PREDECESSOR.read_text("utf-8"),
        json.loads(REGISTRY.read_text("utf-8")),
    )


def test_current_scope_package_passes() -> None:
    module = load_validator()
    result = module.validate_scope_package(ROOT)
    assert result == {
        "baseline_files": 31,
        "decision_targets": 23,
        "deny_by_default_files": 109,
        "future_outputs_absent": 5,
        "positive_package": "PASS",
        "protected_trees": 3,
    }


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (lambda value: value["decision_targets"].pop(), "DECISION_ID_SET_MISMATCH"),
        (
            lambda value: value["decision_targets"].__setitem__(
                1, deepcopy(value["decision_targets"][0])
            ),
            "DECISION_ID_SET_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][0].__setitem__(
                "registry_pointer", "/decisions_by_id/T10-G18-DD-023"
            ),
            "REGISTRY_POINTER_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][0].__setitem__(
                "authority_anchor", "#### missing authority anchor"
            ),
            "DECISION_ROUTE_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][0].__setitem__(
                "normative_delta_summary", "broaden everything"
            ),
            "DECISION_SUMMARY_MISMATCH",
        ),
        (
            lambda value: value["stop_boundary"].__setitem__(
                "authority_idl_allowed", True
            ),
            "STOP_BOUNDARY_MISMATCH",
        ),
        (
            lambda value: value["write_scope"]["modify_existing"].append(
                "docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md"
            ),
            "MODIFY_EXISTING_FORBIDDEN",
        ),
        (
            lambda value: value.__setitem__(
                "transfer_rule", "REGISTRY_IS_NORMATIVE_AUTHORITY"
            ),
            "TRANSFER_RULE_MISMATCH",
        ),
        (
            lambda value: value["write_scope"].__setitem__(
                "protected_path_patterns", ["nothing/**"]
            ),
            "PROTECTED_PATH_SET_MISMATCH",
        ),
        (
            lambda value: value["write_scope"].__setitem__("unknown", True),
            "WRITE_SCOPE_SHAPE_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][1].__setitem__(
                "authority_anchor", "#### 5.6.1 Closed literal and label universes"
            ),
            "DECISION_ROUTE_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][1].__setitem__(
                "mode", "CLARIFY_EXISTING_AUTHORITY"
            ),
            "DECISION_ROUTE_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][1].__setitem__(
                "normative_projection_sha256", "0" * 64
            ),
            "NORMATIVE_PROJECTION_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][1].__setitem__(
                "forbidden_expansion", "Allow every expansion."
            ),
            "AUTHORING_GUARD_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][1].__setitem__(
                "negative_mutation", "No negative test is required."
            ),
            "AUTHORING_GUARD_MISMATCH",
        ),
        (
            lambda value: value["decision_targets"][1].__setitem__(
                "preserve_clause", "Preserve nothing."
            ),
            "AUTHORING_GUARD_MISMATCH",
        ),
    ],
)
def test_target_map_mutations_fail_closed(mutation, code: str) -> None:
    module = load_validator()
    target_map, predecessor, registry = load_inputs()
    mutation(target_map)
    with pytest.raises(ValueError, match=code):
        module.validate_target_map(target_map, predecessor, registry)


def test_target_map_and_schema_are_canonical_json() -> None:
    module = load_validator()
    for path in (TARGET_MAP, REVIEW / "schema/authority-amendment-target-map-v1.schema.json"):
        value = json.loads(path.read_text("utf-8"))
        assert path.read_bytes() == module.canonical_json_bytes(value)


def test_normative_projection_contract_is_closed() -> None:
    module = load_validator()
    target_map, predecessor, registry = load_inputs()
    contract = target_map["normative_projection_contract"]
    assert contract == {
        "algorithm": "SHA-256",
        "canonicalization": "UTF8_JSON_SORT_KEYS_INDENT_2_TRAILING_LF",
        "fields": [
            "affected_owner_paths",
            "exact_chosen_wire_or_matrix",
            "expected_rl_universe_effect",
            "negative_mutations",
            "reference_contract",
        ],
        "future_candidate_binding": (
            "EACH_SELF_CONTAINED_NORMATIVE_BLOCK_MUST_REPRODUCE_THIS_PROJECTION"
        ),
    }
    module.validate_target_map(target_map, predecessor, registry)
    assert all(
        len(target["normative_projection_sha256"]) == 64
        for target in target_map["decision_targets"]
    )


def test_authoring_guard_contract_is_closed() -> None:
    module = load_validator()
    target_map, predecessor, registry = load_inputs()
    assert target_map["authoring_guard_contract"] == {
        "algorithm": "SHA-256",
        "canonicalization": "UTF8_JSON_SORT_KEYS_INDENT_2_TRAILING_LF",
        "enforcement": "PER_DECISION_EXPECTED_DIGEST_FIXED_IN_SCOPE_VALIDATOR",
        "fields": [
            "forbidden_expansion",
            "negative_mutation",
            "preserve_clause",
        ],
    }
    module.validate_target_map(target_map, predecessor, registry)
    assert {
        target["decision_id"]: target["authoring_guard_sha256"]
        for target in target_map["decision_targets"]
    } == module.EXPECTED_AUTHORING_GUARD_DIGESTS


def test_baseline_gate_precedes_semantic_reads(monkeypatch) -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    first = baseline["files"][0]
    first["sha256"] = "0" * 64
    events: list[str] = []

    monkeypatch.setattr(module, "load_baseline", lambda _: baseline)
    monkeypatch.setattr(
        module,
        "read_semantic_json_bytes",
        lambda data, path: events.append(str(path)) or {},
    )
    with pytest.raises(ValueError, match="BASELINE_HASH_DRIFT"):
        module.validate_scope_package(ROOT)
    assert events == []


def test_schema_instance_validator_is_executed(monkeypatch) -> None:
    module = load_validator()
    called: list[str] = []

    def observe(schema, instance) -> None:
        called.append(instance["format"])

    monkeypatch.setattr(module, "validate_schema_instance", observe)
    module.validate_scope_package(ROOT)
    assert called == ["selcal.task10.g18.authority-amendment-target-map.v1"]


def test_schema_instance_validator_rejects_an_unknown_target_field() -> None:
    module = load_validator()
    schema = json.loads(
        (REVIEW / "schema/authority-amendment-target-map-v1.schema.json").read_text(
            "utf-8"
        )
    )
    target_map = json.loads(TARGET_MAP.read_text("utf-8"))
    target_map["decision_targets"][0]["unknown"] = True
    with pytest.raises(ValueError, match="TARGET_SCHEMA_ADDITIONAL_PROPERTY"):
        module.validate_schema_instance(schema, target_map)


def test_schema_instance_validator_enforces_exact_decision_count() -> None:
    module = load_validator()
    schema = json.loads(
        (REVIEW / "schema/authority-amendment-target-map-v1.schema.json").read_text(
            "utf-8"
        )
    )
    target_map = json.loads(TARGET_MAP.read_text("utf-8"))
    target_map["decision_targets"].pop()
    with pytest.raises(ValueError, match="TARGET_SCHEMA_MIN_ITEMS"):
        module.validate_schema_instance(schema, target_map)


def test_schema_document_rejects_open_nested_object() -> None:
    module = load_validator()
    schema = json.loads(
        (REVIEW / "schema/authority-amendment-target-map-v1.schema.json").read_text(
            "utf-8"
        )
    )
    schema["$defs"]["decisionTarget"]["additionalProperties"] = True
    with pytest.raises(ValueError, match="TARGET_SCHEMA_OBJECT_OPEN"):
        module.validate_schema_document(schema)


def test_schema_document_rejects_wrong_dialect() -> None:
    module = load_validator()
    schema = json.loads(
        (REVIEW / "schema/authority-amendment-target-map-v1.schema.json").read_text(
            "utf-8"
        )
    )
    schema["$schema"] = "https://invalid.example/schema"
    with pytest.raises(ValueError, match="TARGET_SCHEMA_DIALECT_MISMATCH"):
        module.validate_schema_document(schema)


def test_review_input_binding_rejects_same_path_different_bytes() -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    verified_bytes = module.verify_baseline(ROOT, baseline)
    target_map = json.loads(TARGET_MAP.read_text("utf-8"))
    registry_relative = target_map["review_input_bindings"][0]["path"]
    registry = json.loads(verified_bytes[registry_relative].decode("utf-8"))
    registry["decisions_by_id"]["T10-G18-DD-001"]["current_fact"] = "DRIFT"
    verified_bytes[registry_relative] = module.canonical_json_bytes(registry)
    with pytest.raises(ValueError, match="REVIEW_INPUT_HASH_MISMATCH"):
        module.validate_review_input_bytes(target_map, verified_bytes)


def test_scope_uses_hash_verified_registry_bytes_without_semantic_reopen(
    monkeypatch,
) -> None:
    module = load_validator()
    original_reader = module._read_repository_regular_file
    registry_relative = REGISTRY.relative_to(ROOT).as_posix()
    registry_reads = 0

    def observe_reader(repository_root, relative, **kwargs):
        nonlocal registry_reads
        data, value = original_reader(repository_root, relative, **kwargs)
        if relative == registry_relative:
            registry_reads += 1
            if registry_reads >= 4:
                registry = json.loads(data.decode("utf-8"))
                registry["decisions_by_id"]["T10-G18-DD-001"]["current_fact"] = (
                    "DRIFT_AFTER_BASELINE"
                )
                data = module.canonical_json_bytes(registry)
        return data, value

    monkeypatch.setattr(module, "_read_repository_regular_file", observe_reader)
    result = module.validate_scope_package(ROOT)
    assert result["positive_package"] == "PASS"
    assert registry_reads == 3


def test_deny_by_default_manifest_covers_every_nonignored_nonallowlisted_file() -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    expected_paths = tuple(
        path
        for path in module.git_nonignored_paths(ROOT)
        if path not in module.EXPECTED_CURRENT_OUTPUTS
    )
    state = module.deny_by_default_state(ROOT)
    assert state["file_count"] == len(expected_paths) == 109
    assert state["excluded_current_outputs"] == list(module.EXPECTED_CURRENT_OUTPUTS)
    assert state["tree_record_format"] == module.IDENTITY_TREE_RECORD_FORMAT
    assert baseline["deny_by_default_manifest"] == state
    assert "README.md" in expected_paths
    assert "pyproject.toml" in expected_paths


@pytest.mark.parametrize("relative", ["README.md", "pyproject.toml"])
def test_deny_by_default_manifest_rejects_unallowlisted_drift(
    monkeypatch, relative: str
) -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    original_reader = module._read_repository_regular_file

    def drift_one_file(repository_root, current_relative, **kwargs):
        data, value = original_reader(repository_root, current_relative, **kwargs)
        if current_relative == relative:
            data += b"DRIFT"
        return data, value

    monkeypatch.setattr(module, "_read_repository_regular_file", drift_one_file)
    with pytest.raises(ValueError, match="DENY_BY_DEFAULT_HASH_DRIFT"):
        module.verify_deny_by_default_manifest(ROOT, baseline)


def test_deny_by_default_manifest_rejects_path_omission() -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    baseline["deny_by_default_manifest"]["file_count"] -= 1
    with pytest.raises(ValueError, match="DENY_BY_DEFAULT_PATH_SET_MISMATCH"):
        module.verify_deny_by_default_manifest(ROOT, baseline)


def _stat_with_mode(value: os.stat_result, mode: int) -> os.stat_result:
    fields = list(value)
    fields[stat.ST_MODE] = mode
    return os.stat_result(fields)


def test_deny_by_default_rejects_same_content_leaf_symlink(monkeypatch) -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    target = (ROOT / "README.md").absolute()
    original_lstat = module.os.lstat

    def substitute_symlink(path):
        value = original_lstat(path)
        if Path(path).absolute() == target:
            return _stat_with_mode(value, stat.S_IFLNK | 0o777)
        return value

    monkeypatch.setattr(module.os, "lstat", substitute_symlink)
    with pytest.raises(ValueError, match="DENY_BY_DEFAULT_SYMLINK_FORBIDDEN"):
        module.verify_deny_by_default_manifest(ROOT, baseline)


def test_deny_by_default_rejects_symlinked_ancestor(monkeypatch) -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    target = (ROOT / "docs/superpowers/specs").absolute()
    original_lstat = module.os.lstat

    def substitute_symlink(path):
        value = original_lstat(path)
        if Path(path).absolute() == target:
            return _stat_with_mode(value, stat.S_IFLNK | 0o777)
        return value

    monkeypatch.setattr(module.os, "lstat", substitute_symlink)
    with pytest.raises(ValueError, match="DENY_BY_DEFAULT_SYMLINK_FORBIDDEN"):
        module.verify_deny_by_default_manifest(ROOT, baseline)


def test_deny_by_default_rejects_regular_file_mode_drift(monkeypatch) -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    original_reader = module._read_repository_regular_file

    def substitute_mode(repository_root, relative, **kwargs):
        data, value = original_reader(repository_root, relative, **kwargs)
        if relative == "README.md":
            value = _stat_with_mode(value, stat.S_IFREG | 0o755)
        return data, value

    monkeypatch.setattr(module, "_read_repository_regular_file", substitute_mode)
    with pytest.raises(ValueError, match="DENY_BY_DEFAULT_HASH_DRIFT"):
        module.verify_deny_by_default_manifest(ROOT, baseline)


def test_baseline_rejects_role_path_rebinding() -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    baseline["files"][0]["logical_role"] = "V2_REVIEW_REGISTRY"
    with pytest.raises(ValueError, match="BASELINE_FILE_BINDING_MISMATCH"):
        module.verify_baseline(ROOT, baseline)


def test_baseline_loader_rejects_symlink_identity(tmp_path: Path) -> None:
    module = load_validator()
    target = tmp_path / "baseline-target.json"
    target.write_bytes(BASELINE.read_bytes())
    linked_baseline = tmp_path / module.BASELINE_RELATIVE
    linked_baseline.parent.mkdir(parents=True)
    linked_baseline.symlink_to(target)
    with pytest.raises(ValueError, match="BASELINE_SYMLINK_FORBIDDEN"):
        module.load_baseline(linked_baseline)


def test_baseline_bound_file_rejects_mode_drift(monkeypatch) -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    target_relative = TARGET_MAP.relative_to(ROOT).as_posix()
    original_reader = module._read_repository_regular_file

    def substitute_mode(repository_root, relative, **kwargs):
        data, value = original_reader(repository_root, relative, **kwargs)
        if relative == target_relative:
            value = _stat_with_mode(value, stat.S_IFREG | 0o755)
        return data, value

    monkeypatch.setattr(module, "_read_repository_regular_file", substitute_mode)
    with pytest.raises(ValueError, match="BASELINE_FILE_MODE_DRIFT"):
        module.verify_baseline(ROOT, baseline)


@pytest.mark.parametrize(
    ("field", "replacement", "code"),
    [
        ("baseline_id", "WRONG", "BASELINE_METADATA_MISMATCH"),
        ("git_head", "0" * 40, "BASELINE_GIT_HEAD_MISMATCH"),
        ("identity_rule", "trust me", "BASELINE_METADATA_MISMATCH"),
        ("schema", "wrong.schema", "BASELINE_METADATA_MISMATCH"),
        ("scope", "WRONG_SCOPE", "BASELINE_METADATA_MISMATCH"),
    ],
)
def test_baseline_rejects_wrong_identity_metadata(
    field: str, replacement: str, code: str
) -> None:
    module = load_validator()
    baseline = json.loads(BASELINE.read_text("utf-8"))
    baseline[field] = replacement
    with pytest.raises(ValueError, match=code):
        module.verify_baseline(ROOT, baseline)


def test_protected_source_tree_includes_non_python_package_metadata() -> None:
    baseline = json.loads(BASELINE.read_text("utf-8"))
    source_tree = next(
        entry
        for entry in baseline["protected_trees"]
        if entry["logical_role"] == "PRODUCTION_SOURCE_TREE"
    )
    assert source_tree["glob"] == "**/*"
    assert source_tree["file_count"] == 35


def test_future_outputs_are_prewrite_absent() -> None:
    module = load_validator()
    target_map = json.loads(TARGET_MAP.read_text("utf-8"))
    module.verify_future_outputs_absent(
        ROOT, target_map["write_scope"]["future_candidate_outputs"]
    )


def test_future_output_dangling_symlink_is_not_absent(monkeypatch) -> None:
    module = load_validator()
    relative = module.EXPECTED_FUTURE_OUTPUTS[0]
    target = (ROOT / relative).absolute()
    original_lexists = module.os.path.lexists
    original_lstat = module.os.lstat
    stat_template = original_lstat(target.parent)

    def expose_dangling_symlink(path):
        if Path(path).absolute() == target:
            return True
        return original_lexists(path)

    def substitute_symlink(path):
        if Path(path).absolute() == target:
            return _stat_with_mode(stat_template, stat.S_IFLNK | 0o777)
        return original_lstat(path)

    monkeypatch.setattr(module.os.path, "lexists", expose_dangling_symlink)
    monkeypatch.setattr(module.os, "lstat", substitute_symlink)
    with pytest.raises(ValueError, match="PREWRITE_OUTPUT_ALREADY_EXISTS"):
        module.verify_future_outputs_absent(ROOT, [relative])


def test_future_output_rejects_symlinked_ancestor(monkeypatch) -> None:
    module = load_validator()
    relative = module.EXPECTED_FUTURE_OUTPUTS[0]
    target = (ROOT / "docs/superpowers/specs").absolute()
    original_lstat = module.os.lstat

    def substitute_symlink(path):
        value = original_lstat(path)
        if Path(path).absolute() == target:
            return _stat_with_mode(value, stat.S_IFLNK | 0o777)
        return value

    monkeypatch.setattr(module.os, "lstat", substitute_symlink)
    with pytest.raises(ValueError, match="PREWRITE_OUTPUT_ALREADY_EXISTS"):
        module.verify_future_outputs_absent(ROOT, [relative])


def test_scope_evidence_reads_do_not_reopen_paths_with_read_bytes(monkeypatch) -> None:
    module = load_validator()

    def forbid_path_reopen(_path: Path) -> bytes:
        raise AssertionError("scope evidence must be read through a no-follow fd")

    monkeypatch.setattr(Path, "read_bytes", forbid_path_reopen)
    result = module.validate_scope_package(ROOT)
    assert result["positive_package"] == "PASS"


def test_fd_reader_rejects_leaf_symlink_swap_during_read(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_validator()
    evidence = tmp_path / "evidence.txt"
    target = tmp_path / "same-content-target.txt"
    evidence.write_bytes(b"same content")
    target.write_bytes(b"same content")
    original_read = module._read_fd_bytes

    def swap_after_descriptor_read(file_descriptor: int) -> bytes:
        data = original_read(file_descriptor)
        evidence.unlink()
        evidence.symlink_to(target)
        return data

    monkeypatch.setattr(module, "_read_fd_bytes", swap_after_descriptor_read)
    with pytest.raises(ValueError, match="TEST_IDENTITY_DRIFT"):
        module._read_repository_regular_file(
            tmp_path,
            "evidence.txt",
            symlink_code="TEST_SYMLINK_FORBIDDEN",
            kind_code="TEST_KIND_DRIFT",
            drift_code="TEST_IDENTITY_DRIFT",
        )


def test_fd_reader_rejects_regular_inode_swap_during_read(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_validator()
    evidence = tmp_path / "evidence.txt"
    replacement = tmp_path / "replacement.txt"
    evidence.write_bytes(b"same content")
    replacement.write_bytes(b"same content")
    original_read = module._read_fd_bytes

    def swap_after_descriptor_read(file_descriptor: int) -> bytes:
        data = original_read(file_descriptor)
        evidence.unlink()
        replacement.rename(evidence)
        return data

    monkeypatch.setattr(module, "_read_fd_bytes", swap_after_descriptor_read)
    with pytest.raises(ValueError, match="TEST_IDENTITY_DRIFT"):
        module._read_repository_regular_file(
            tmp_path,
            "evidence.txt",
            symlink_code="TEST_SYMLINK_FORBIDDEN",
            kind_code="TEST_KIND_DRIFT",
            drift_code="TEST_IDENTITY_DRIFT",
        )


def test_fd_reader_rejects_ancestor_symlink_swap_during_read(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_validator()
    evidence_directory = tmp_path / "evidence-directory"
    moved_directory = tmp_path / "moved-directory"
    evidence_directory.mkdir()
    evidence = evidence_directory / "evidence.txt"
    evidence.write_bytes(b"same content")
    original_read = module._read_fd_bytes

    def swap_after_descriptor_read(file_descriptor: int) -> bytes:
        data = original_read(file_descriptor)
        evidence_directory.rename(moved_directory)
        evidence_directory.symlink_to(moved_directory, target_is_directory=True)
        return data

    monkeypatch.setattr(module, "_read_fd_bytes", swap_after_descriptor_read)
    with pytest.raises(ValueError, match="TEST_SYMLINK_FORBIDDEN"):
        module._read_repository_regular_file(
            tmp_path,
            "evidence-directory/evidence.txt",
            symlink_code="TEST_SYMLINK_FORBIDDEN",
            kind_code="TEST_KIND_DRIFT",
            drift_code="TEST_IDENTITY_DRIFT",
        )


def test_no_follow_opener_closes_leaf_fd_when_initial_fstat_fails(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_validator()
    (tmp_path / "evidence.txt").write_bytes(b"evidence")
    original_open = module.os.open
    original_close = module.os.close
    opened: list[int] = []
    closed: list[int] = []

    def track_open(*args, **kwargs) -> int:
        file_descriptor = original_open(*args, **kwargs)
        opened.append(file_descriptor)
        return file_descriptor

    def track_close(file_descriptor: int) -> None:
        closed.append(file_descriptor)
        original_close(file_descriptor)

    def fail_fstat(_file_descriptor: int):
        raise OSError("simulated fstat failure")

    monkeypatch.setattr(module.os, "open", track_open)
    monkeypatch.setattr(module.os, "close", track_close)
    monkeypatch.setattr(module.os, "fstat", fail_fstat)
    try:
        with pytest.raises(OSError, match="simulated fstat failure"):
            module._open_repository_regular_file_no_follow(
                tmp_path,
                "evidence.txt",
                symlink_code="TEST_SYMLINK_FORBIDDEN",
                kind_code="TEST_KIND_DRIFT",
            )
    finally:
        for file_descriptor in set(opened) - set(closed):
            original_close(file_descriptor)
    assert sorted(opened) == sorted(closed)
