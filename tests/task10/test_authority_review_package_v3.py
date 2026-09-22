from __future__ import annotations

import copy
import importlib.util
import json
import os
import stat
from hashlib import sha256
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]
V2_REVIEW = ROOT / "docs/superpowers/specs/idl/task10/v10/review"
V3_REVIEW = V2_REVIEW / "v3"
V2_REGISTRY = V2_REVIEW / "authority-design-decision-registry-v2.json"
V3_REGISTRY = V3_REVIEW / "authority-design-decision-registry-v3.json"
V3_SCHEMA = V3_REVIEW / "schema/authority-design-decision-registry-v3.schema.json"
V3_BASELINE = V3_REVIEW / "authority-review-package-v3-baseline.json"
MIGRATOR = V3_REVIEW / "migrate_authority_decision_registry_v2_to_v3.py"
VALIDATOR = V3_REVIEW / "validate_authority_review_package_v3.py"

V2_SHA256 = "77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5"
ALLOWED_DECISION_DELTAS = {
    "T10-G18-DD-001",
    "T10-G18-DD-004",
    "T10-G18-DD-006",
    "T10-G18-DD-007",
    "T10-G18-DD-009",
    "T10-G18-DD-011",
    "T10-G18-DD-016",
    "T10-G18-DD-020",
}


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def test_v2_predecessor_identity_is_frozen() -> None:
    assert V2_REGISTRY.stat().st_mode & 0o777 == 0o644
    assert V2_REGISTRY.stat().st_size == 4_282_426
    assert sha256(V2_REGISTRY.read_bytes()).hexdigest() == V2_SHA256


def test_every_v3_baseline_input_is_exact_regular_0644() -> None:
    baseline = load_json(V3_BASELINE)
    assert baseline["machine_stop_decision"] == (
        "STOP_ON_ANY_PREDECESSOR_IDENTITY_DRIFT"
    )
    for record in baseline["files"]:
        path = ROOT / record["path"]
        metadata = path.lstat()
        assert stat.S_ISREG(metadata.st_mode)
        assert not path.is_symlink()
        assert metadata.st_mode & 0o777 == 0o644
        data = path.read_bytes()
        assert len(data) == record["bytes"]
        assert sha256(data).hexdigest() == record["sha256"]


def test_validator_independently_anchors_the_v3_baseline(tmp_path: Path) -> None:
    validator = load_module(VALIDATOR, "task10_v3_baseline_anchor")
    assert validator.EXPECTED_V3_BASELINE_SHA256 == sha256(
        V3_BASELINE.read_bytes()
    ).hexdigest()
    relative = V3_BASELINE.relative_to(ROOT)
    candidate_path = tmp_path / relative
    candidate_path.parent.mkdir(parents=True)
    candidate = load_json(V3_BASELINE)
    candidate["git_head"] = "0" * 40
    candidate_path.write_bytes(validator.canonical_json_bytes(candidate))
    candidate_path.chmod(0o644)
    with pytest.raises(ValueError, match="V3_BASELINE_IDENTITY_DRIFT"):
        validator._load_and_verify_baseline(tmp_path)


def test_writer_verifies_all_eight_baseline_inputs_before_output(
    tmp_path: Path,
) -> None:
    migrator = load_module(MIGRATOR, "task10_v3_writer_baseline_gate")
    with pytest.raises(ValueError, match="V3_BASELINE_IDENTITY_DRIFT"):
        migrator.write_v3_registry(tmp_path)

    verified = migrator.verify_baseline_inputs(ROOT)
    assert set(verified) == {
        record["path"] for record in load_json(V3_BASELINE)["files"]
    }


def test_path_validator_executes_every_registry_source_binding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_module(VALIDATOR, "task10_v3_source_binding_gate")
    observed: list[int] = []
    original = validator._verify_registry_source_bindings

    def observe(repository_root, registry):
        result = original(repository_root, registry)
        observed.append(len(result))
        return result

    monkeypatch.setattr(validator, "_verify_registry_source_bindings", observe)
    validator.validate_v3_paths(ROOT)
    assert observed == [6]


def test_registry_source_binding_gate_rejects_missing_sources(tmp_path: Path) -> None:
    validator = load_module(VALIDATOR, "task10_v3_missing_source_binding")
    with pytest.raises(ValueError, match="SOURCE_FILE_MISSING"):
        validator._verify_registry_source_bindings(tmp_path, load_json(V3_REGISTRY))


def test_writer_rejects_non_hex_schema_digest() -> None:
    migrator = load_module(MIGRATOR, "task10_v3_schema_digest_contract")
    with pytest.raises(ValueError, match="V3_SCHEMA_SHA256_INVALID"):
        migrator.build_v3(load_json(V2_REGISTRY), registry_schema_sha256="z" * 64)


def test_writer_output_is_atomic_nofollow_and_forces_0644(tmp_path: Path) -> None:
    migrator = load_module(MIGRATOR, "task10_v3_atomic_writer")
    victim = tmp_path / "victim.json"
    victim.write_bytes(b"victim\n")
    victim.chmod(0o644)
    linked_output = tmp_path / "linked-output.json"
    linked_output.symlink_to(victim)
    with pytest.raises(ValueError, match="OUTPUT_PATH_SYMLINK"):
        migrator._atomic_write_regular_0644(linked_output, b"replacement\n")
    assert victim.read_bytes() == b"victim\n"

    output = tmp_path / "output.json"
    old_umask = os.umask(0o077)
    try:
        migrator._atomic_write_regular_0644(output, b"canonical\n")
    finally:
        os.umask(old_umask)
    assert output.read_bytes() == b"canonical\n"
    assert stat.S_IMODE(output.stat().st_mode) == 0o644
    assert "_atomic_write_regular_0644(output_path" in MIGRATOR.read_text("utf-8")


def test_hardened_bound_source_reader_accepts_only_regular_0644(
    tmp_path: Path,
) -> None:
    validator = load_module(VALIDATOR, "task10_v3_validator_bound_reader")
    regular = tmp_path / "regular.json"
    regular.write_bytes(b"{}\n")
    regular.chmod(0o644)
    assert validator._read_exact_regular_0644(regular) == b"{}\n"

    wrong_mode = tmp_path / "wrong-mode.json"
    wrong_mode.write_bytes(b"{}\n")
    wrong_mode.chmod(0o600)
    with pytest.raises(ValueError, match="BOUND_SOURCE_MODE_MISMATCH"):
        validator._read_exact_regular_0644(wrong_mode)

    symlink = tmp_path / "symlink.json"
    symlink.symlink_to(regular)
    with pytest.raises(ValueError, match="BOUND_SOURCE_SYMLINK"):
        validator._read_exact_regular_0644(symlink)

    fifo = tmp_path / "source.fifo"
    os.mkfifo(fifo, 0o644)
    with pytest.raises(ValueError, match="BOUND_SOURCE_KIND_MISMATCH"):
        validator._read_exact_regular_0644(fifo)

    special_mode = tmp_path / "special-mode.json"
    special_mode.write_bytes(b"{}\n")
    special_mode.chmod(0o4644)
    with pytest.raises(ValueError, match="BOUND_SOURCE_MODE_MISMATCH"):
        validator._read_exact_regular_0644(special_mode)


def test_hardened_validator_does_not_reopen_bound_sources_through_path_api() -> None:
    source = VALIDATOR.read_text("utf-8")
    assert ".read_bytes(" not in source
    assert 'getattr(os, "O_NOFOLLOW", 0)' in source
    assert "os.fstat" in source


def test_migration_is_deterministic_and_matches_frozen_v3(tmp_path: Path) -> None:
    migrator = load_module(MIGRATOR, "task10_v3_migrator")
    v2 = load_json(V2_REGISTRY)
    schema_sha = sha256(V3_SCHEMA.read_bytes()).hexdigest()

    first = migrator.build_v3(v2, registry_schema_sha256=schema_sha)
    second = migrator.build_v3(copy.deepcopy(v2), registry_schema_sha256=schema_sha)

    assert migrator.canonical_json_bytes(first) == migrator.canonical_json_bytes(second)
    assert migrator.canonical_json_bytes(first) == V3_REGISTRY.read_bytes()
    first_path = tmp_path / "first" / V3_REGISTRY.name
    second_path = tmp_path / "second" / V3_REGISTRY.name
    first_path.parent.mkdir()
    second_path.parent.mkdir()
    first_path.write_bytes(migrator.canonical_json_bytes(first))
    second_path.write_bytes(migrator.canonical_json_bytes(second))
    assert first_path.read_bytes() == second_path.read_bytes()
    assert sha256(first_path.read_bytes()).hexdigest() == sha256(
        second_path.read_bytes()
    ).hexdigest()


def test_only_adjudicated_decisions_change_semantics() -> None:
    migrator = load_module(MIGRATOR, "task10_v3_migrator_diff")
    v2 = load_json(V2_REGISTRY)
    v3 = load_json(V3_REGISTRY)

    assert migrator.changed_decision_ids(v2, v3) == ALLOWED_DECISION_DELTAS
    assert migrator.semantic_diff_outside_allowlist(v2, v3) == []


def test_semantic_allowlist_resolves_rule_bodies_not_only_decision_ids() -> None:
    migrator = load_module(MIGRATOR, "task10_v3_migrator_rule_diff")
    v2 = load_json(V2_REGISTRY)
    candidate = copy.deepcopy(v2)
    dd005_rule = candidate["decisions_by_id"]["T10-G18-DD-005"][
        "compiled_rule_ids"
    ][0]
    candidate["compiled_rules_by_id"][dd005_rule]["payload"][
        "allowed_target_tables"
    ] = ["UNAUTHORIZED_TARGET"]
    assert migrator.changed_decision_ids(v2, candidate) == {"T10-G18-DD-005"}
    assert migrator.semantic_diff_outside_allowlist(v2, candidate) == [
        "T10-G18-DD-005"
    ]


def test_v3_global_counts_and_stop_boundary() -> None:
    validator = load_module(VALIDATOR, "task10_v3_validator")
    result = validator.validate_v3_registry(load_json(V3_REGISTRY), load_json(V2_REGISTRY))

    assert result == {
        "branches": 461,
        "coverage_rows": 264,
        "decisions": 23,
        "owners": 66,
        "reference_fields": 312,
        "rules": 570,
        "schema_templates": 207,
        "status": "V3_SEMANTIC_CORRECTION_PASS_NOT_AUTHORITY",
    }


def test_v3_correction_lifecycle_cannot_promote_downstream_work() -> None:
    v3 = load_json(V3_REGISTRY)
    assert v3["format"] == "selcal.task10.g18.authority-design-decision-registry.v3"
    assert v3["correction_class"] == (
        "NORMATIVE_REVIEW_INPUT_CORRECTION_NOT_REPRESENTATION_ONLY"
    )
    assert v3["artifact_state"] == "REVIEW_DECISION_INPUT_NOT_AUTHORITY"
    assert v3["authority_amendment_status"] == "AUTHORITY_AMENDMENT_NOT_YET_REVIEWED"
    assert v3["machine_stop_decision"] == "STOP_BEFORE_AUTHORITY_IDL_AND_KATS"
    assert v3["scope_boundary"] == {
        "authority_idl_allowed": False,
        "implementation_allowed": False,
        "kats_allowed": False,
    }
    assert v3["predecessor_v2_attestations_inherited"] is False
    assert v3["authority_amendment_scope_v1_authoring_authority"] is False


def test_v3_registry_binds_the_exact_v2_predecessor() -> None:
    v3 = load_json(V3_REGISTRY)
    assert v3["predecessor_binding"] == {
        "bytes": 4_282_426,
        "format": "selcal.task10.g18.authority-design-decision-registry.v2",
        "mode": "0644",
        "path": (
            "docs/superpowers/specs/idl/task10/v10/review/"
            "authority-design-decision-registry-v2.json"
        ),
        "sha256": V2_SHA256,
    }


def test_v3_registry_binds_the_exact_authority_source() -> None:
    v3 = load_json(V3_REGISTRY)
    expected = {
        "logical_source": (
            "docs/superpowers/specs/"
            "2026-08-29-task10-deny-by-default-provider-proof-design.md"
        ),
        "sha256": "74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff",
    }
    assert list(v3["source_bindings_by_id"].values()).count(expected) == 1


def test_v3_registry_carries_all_eight_normative_projection_digests() -> None:
    v3 = load_json(V3_REGISTRY)
    assert set(v3["normative_projection_digests_by_decision"]) == (
        ALLOWED_DECISION_DELTAS
    )
    assert all(
        len(value) == 64
        for value in v3["normative_projection_digests_by_decision"].values()
    )
    assert set(v3["normative_projection_digests_by_collection"]) == {
        "coverage_rows_by_id"
    }
    assert len(v3["normative_registry_projection_sha256"]) == 64


def test_independent_validator_rejects_synchronized_coverage_forgery() -> None:
    validator = load_module(VALIDATOR, "task10_v3_coverage_digest")
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    candidate["coverage_rows_by_id"]["ROW-0001"]["payload"]["category"] = (
        "FORGED"
    )
    candidate["normative_projection_digests_by_collection"][
        "coverage_rows_by_id"
    ] = sha256(
        validator.canonical_json_bytes(candidate["coverage_rows_by_id"])
    ).hexdigest()
    with pytest.raises(ValueError, match="COVERAGE_PROJECTION_DIGEST_MISMATCH"):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["owners_by_id"]["OWN-0001"]["payload"].__setitem__(
            "unreviewed_extra", True
        ),
        lambda value: value["legacy_rehydration"]["scope_boundary"].__setitem__(
            "implementation_allowed", True
        ),
        lambda value: value["invariants_by_id"]["INV-0001"]["assertion"].__setitem__(
            "expected", 999
        ),
    ],
)
def test_independent_validator_rejects_synchronized_nested_registry_forgery(
    mutation,
) -> None:
    validator = load_module(VALIDATOR, "task10_v3_full_registry_digest")
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    mutation(candidate)
    projection = copy.deepcopy(candidate)
    projection.pop("normative_registry_projection_sha256")
    candidate["normative_registry_projection_sha256"] = sha256(
        validator.canonical_json_bytes(projection)
    ).hexdigest()
    with pytest.raises(
        ValueError, match="NORMATIVE_REGISTRY_PROJECTION_DIGEST_MISMATCH"
    ):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


@pytest.mark.parametrize(
    ("mutation", "failure_code"),
    [
        (
            lambda value: value["reference_fields_by_id"]["FLD-0001"].__setitem__(
                "field_id", "FLD-9999"
            ),
            "REFERENCE_FIELD_IDENTITY_MISMATCH",
        ),
        (
            lambda value: value["reference_fields_by_id"]["FLD-0002"].__setitem__(
                "order_key",
                copy.deepcopy(
                    value["reference_fields_by_id"]["FLD-0001"]["order_key"]
                ),
            ),
            "REFERENCE_FIELD_COMPLETE_KEY_MISMATCH",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-020"]["payload"][
                "exact_chosen_wire_or_matrix"
            ]["schema_ordering"]["reference_field_ordinals"][0].__setitem__(
                "field_path", "FORGED"
            ),
            "REFERENCE_FIELD_DD020_PROJECTION_MISMATCH",
        ),
    ],
)
def test_independent_validator_rejects_reference_field_mismatch(
    mutation,
    failure_code: str,
) -> None:
    validator = load_module(VALIDATOR, "task10_v3_reference_fields")
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    mutation(candidate)
    with pytest.raises(ValueError, match=failure_code):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


def test_validator_executes_the_frozen_json_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_module(VALIDATOR, "task10_v3_schema_execution")
    schema = load_json(V3_SCHEMA)
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    candidate["unexpected_top_level_property"] = True
    with pytest.raises(ValueError, match="JSON_SCHEMA_VALIDATION_FAILED"):
        validator.validate_schema_instance(schema, candidate)
    with pytest.raises(ValueError, match="JSON_SCHEMA_VALIDATION_FAILED"):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))

    calls: list[str] = []
    original = validator.validate_schema_instance

    def observe(bound_schema, instance) -> None:
        calls.append(instance["format"])
        original(bound_schema, instance)

    monkeypatch.setattr(validator, "validate_schema_instance", observe)
    validator.validate_v3_paths(ROOT)
    assert calls == ["selcal.task10.g18.authority-design-decision-registry.v3"]


def test_validator_freezes_schema_independently_of_registry_self_report() -> None:
    validator = load_module(VALIDATOR, "task10_v3_schema_identity")
    assert validator.EXPECTED_V3_SCHEMA_SHA256 == sha256(V3_SCHEMA.read_bytes()).hexdigest()
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    candidate["schema_binding"]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="V3_SCHEMA_IDENTITY_DRIFT"):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


def test_independent_validator_rejects_unreviewed_allowed_decision_delta() -> None:
    validator = load_module(VALIDATOR, "task10_v3_projection_digest")
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    candidate["decisions_by_id"]["T10-G18-DD-006"]["payload"][
        "exact_chosen_wire_or_matrix"
    ]["TypingParameterBinding"]["field_sequence_by_branch"]["TYPEVAR"][3] = (
        "BROKEN_UNREVIEWED_SEMANTIC_DELTA"
    )
    candidate["normative_projection_digests_by_decision"]["T10-G18-DD-006"] = (
        sha256(
            validator.canonical_json_bytes(
                validator._decision_projection(candidate, "T10-G18-DD-006")
            )
        ).hexdigest()
    )
    with pytest.raises(ValueError, match="NORMATIVE_PROJECTION_DIGEST_MISMATCH"):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


def test_independent_validator_recomputes_canonical_rule_id_order() -> None:
    validator = load_module(VALIDATOR, "task10_v3_rule_order")
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    left_id = "PCR-0111"
    right_id = "PCR-0252"
    left = copy.deepcopy(candidate["compiled_rules_by_id"][left_id])
    right = copy.deepcopy(candidate["compiled_rules_by_id"][right_id])
    for key in ("payload", "provenance", "evidence_ref_ids"):
        candidate["compiled_rules_by_id"][left_id][key] = copy.deepcopy(right[key])
        candidate["compiled_rules_by_id"][right_id][key] = copy.deepcopy(left[key])
    with pytest.raises(ValueError, match="RULE_CANONICAL_ORDER_MISMATCH"):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


def test_independent_validator_recomputes_canonical_branch_id_order() -> None:
    validator = load_module(VALIDATOR, "task10_v3_branch_order")
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    candidate["discriminator_branches_by_id"]["BR-0001"]["payload"][
        "branch_ordinal"
    ] = 2
    candidate["discriminator_branches_by_id"]["BR-0002"]["payload"][
        "branch_ordinal"
    ] = 1
    with pytest.raises(ValueError, match="BRANCH_CANONICAL_ORDER_MISMATCH"):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


def test_transfer_rule_semantics_survive_id_rebuild_with_explicit_mapping() -> None:
    migrator = load_module(MIGRATOR, "task10_v3_transfer_id_mapping")
    v2 = load_json(V2_REGISTRY)
    v3 = load_json(V3_REGISTRY)
    assert migrator._semantic_rule_projection(
        v2, "PCR-0530"
    ) == migrator._semantic_rule_projection(v3, "PCR-0111")
    assert migrator._semantic_rule_projection(
        v2, "PCR-0550"
    ) == migrator._semantic_rule_projection(v3, "PCR-0252")


def test_dd001_distinguishes_eleven_rows_from_ten_paths() -> None:
    decision = load_json(V3_REGISTRY)["decisions_by_id"]["T10-G18-DD-001"]
    payload = decision["payload"]
    exact = payload["exact_chosen_wire_or_matrix"]
    assert len(payload["affected_owner_paths"]) == 10
    assert len(exact["exact_retyped_paths"]) == 10
    assert len(exact["coverage_compilation_manifest"]) == 11
    text = " ".join(
        payload[key]
        for key in (
            "authority_amendment_text_summary",
            "current_fact",
            "neutral_verdict",
        )
    )
    assert "ten unique" in text
    assert "eleven census" in text
    assert "eleven exact paths" not in text


def test_dd004_is_four_branch_embedded_capture_record() -> None:
    validator = load_module(VALIDATOR, "task10_v3_validator_dd004")
    assert validator.dd004_errors(load_json(V3_REGISTRY)) == []


def test_dd009_is_direct_binding_and_source_kind_matrix() -> None:
    validator = load_module(VALIDATOR, "task10_v3_validator_dd009")
    assert validator.dd009_errors(load_json(V3_REGISTRY)) == []


def test_every_owner_tuple_equals_its_rule_target_union_except_dd020() -> None:
    validator = load_module(VALIDATOR, "task10_v3_validator_owner_tuple")
    assert validator.owner_tuple_errors(load_json(V3_REGISTRY)) == []


def test_provider_reference_has_no_orphan_role() -> None:
    validator = load_module(VALIDATOR, "task10_v3_validator_provider")
    assert validator.provider_reference_errors(load_json(V3_REGISTRY)) == []


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (
            lambda value: value["scope_boundary"].__setitem__(
                "implementation_allowed", True
            ),
            "STOP_BOUNDARY_VIOLATION",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-006"]["payload"]
            ["reference_contract"]["owner_tuple"].remove("runtime_values"),
            "REFERENCE_OWNER_TUPLE_MISMATCH",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-011"]["payload"]
            ["exact_chosen_wire_or_matrix"]["ProviderReference"].__setitem__(
                "GENERATED_FIELD_ACCESSOR", "generated_field_accessors"
            ),
            "ORPHAN_EXACT_ROLE",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-007"]["payload"].__setitem__(
                "neutral_verdict", "Use ProjectAccessRef."
            ),
            "REFERENCE_TYPE_NAME_MISMATCH",
        ),
    ],
)
def test_independent_validator_rejects_adverse_mutations(mutation, code: str) -> None:
    validator = load_module(VALIDATOR, f"task10_v3_validator_mutation_{code}")
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    mutation(candidate)
    with pytest.raises(ValueError, match=code):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-002"][
                "payload"
            ].__setitem__("neutral_verdict", "unauthorized semantic edit"),
            "SEMANTIC_DIFF_OUTSIDE_ALLOWLIST",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-001"][
                "payload"
            ]["affected_owner_paths"].pop(),
            "DECISION_CENSUS_PATH_COUNT_MISMATCH",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-004"][
                "payload"
            ]["exact_chosen_wire_or_matrix"]["CapturedEnvironmentRef"].__setitem__(
                "VALUE_CONTRACT", "runtime_values"
            ),
            "EXACT_ROLE_OWNER_MATRIX_MISMATCH",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-004"][
                "payload"
            ]["exact_chosen_wire_or_matrix"].__setitem__(
                "fields", ["capture_name", "capture_kind", "label"]
            ),
            "EXACT_RECORD_FIELD_SEQUENCE_MISMATCH",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-009"][
                "payload"
            ]["exact_chosen_wire_or_matrix"]["coverage_compilation_manifest"][
                -1
            ]["compiled_rule_ids"].pop(),
            "CROSS_FIELD_MATRIX_NOT_COMPILED",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-009"][
                "payload"
            ]["exact_chosen_wire_or_matrix"]["transfer_direction"].reverse(),
            "TRANSFER_DIRECTION_RULE_LINK_MISMATCH",
        ),
        (
            lambda value: value["owners_by_id"].pop("OWN-0065"),
            "GLOBAL_COLLECTION_COUNT_MISMATCH",
        ),
        (
            lambda value: value.__setitem__(
                "predecessor_v2_attestations_inherited", True
            ),
            "STALE_V2_ATTESTATION_INHERITED",
        ),
        (
            lambda value: value["predecessor_binding"].__setitem__(
                "bytes", 4_282_425
            ),
            "PREDECESSOR_IDENTITY_DRIFT",
        ),
        (
            lambda value: value.__setitem__(
                "authority_amendment_scope_v1_authoring_authority", True
            ),
            "STALE_SCOPE_V1_REUSED",
        ),
    ],
)
def test_independent_validator_covers_required_failure_codes(
    mutation, code: str
) -> None:
    validator = load_module(VALIDATOR, f"task10_v3_required_code_{code}")
    candidate = copy.deepcopy(load_json(V3_REGISTRY))
    mutation(candidate)
    with pytest.raises(ValueError, match=code):
        validator.validate_v3_registry(candidate, load_json(V2_REGISTRY))


def test_independent_validator_rejects_predecessor_identity_drift() -> None:
    validator = load_module(VALIDATOR, "task10_v3_predecessor_identity")
    predecessor = copy.deepcopy(load_json(V2_REGISTRY))
    predecessor["format"] = "drifted"
    with pytest.raises(ValueError, match="PREDECESSOR_IDENTITY_DRIFT"):
        validator.validate_v3_registry(load_json(V3_REGISTRY), predecessor)


def test_validator_does_not_import_or_execute_migrator() -> None:
    source = VALIDATOR.read_text("utf-8")
    assert "migrate_authority_decision_registry_v2_to_v3" not in source
    assert "importlib" not in source
