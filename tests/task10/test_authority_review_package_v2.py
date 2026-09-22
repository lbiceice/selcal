from __future__ import annotations

import copy
import importlib.util
import json
import shutil
from collections import Counter
from hashlib import sha256
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "docs/superpowers/specs/idl/task10/v10/review"
MIGRATOR = REVIEW / "migrate_authority_decision_registry_v1_to_v2.py"
VALIDATOR = REVIEW / "validate_authority_review_package_v2.py"
REGISTRY_SCHEMA = REVIEW / "schema/authority-design-decision-registry-v2.schema.json"
ATTESTATION_SCHEMA = REVIEW / "schema/authority-design-decision-review-attestation-v1.schema.json"
V1_REGISTRY = REVIEW / "authority-design-decision-registry-v1.json"
V1_MATRIX = REVIEW / "authority-design-decision-matrix-v1.md"
V2_REGISTRY = REVIEW / "authority-design-decision-registry-v2.json"
V2_INDEX = REVIEW / "authority-design-decision-index-v2.md"
ATTESTATION_README = REVIEW / "attestations/README.md"

REVIEWED_ARTIFACT_PATHS = {
    "ATTESTATION_README": (
        "docs/superpowers/specs/idl/task10/v10/review/attestations/README.md"
    ),
    "ATTESTATION_SCHEMA": (
        "docs/superpowers/specs/idl/task10/v10/review/schema/"
        "authority-design-decision-review-attestation-v1.schema.json"
    ),
    "FOCUSED_TEST": "tests/task10/test_authority_review_package_v2.py",
    "MARKDOWN_INDEX": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-index-v2.md"
    ),
    "MIGRATOR": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "migrate_authority_decision_registry_v1_to_v2.py"
    ),
    "REGISTRY_SCHEMA": (
        "docs/superpowers/specs/idl/task10/v10/review/schema/"
        "authority-design-decision-registry-v2.schema.json"
    ),
    "V1_MATRIX": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-matrix-v1.md"
    ),
    "V1_REGISTRY": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-registry-v1.json"
    ),
    "V2_REGISTRY": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-registry-v2.json"
    ),
    "VALIDATOR": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "validate_authority_review_package_v2.py"
    ),
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_migrator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("task10_registry_v2_migrator", MIGRATOR)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load migrator from {MIGRATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("task10_registry_v2_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load validator from {VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def minimal_valid_v2_registry_fixture(schema_sha256: str) -> dict[str, object]:
    digest64 = "0" * 64
    source_id = f"SRC-{digest64}"
    evidence_id = f"EV-{digest64}"
    return {
        "format": "selcal.task10.g18.authority-design-decision-registry.v2",
        "artifact_state": "REVIEW_DECISION_INPUT_NOT_AUTHORITY",
        "authority_amendment_status": "AUTHORITY_AMENDMENT_NOT_YET_REVIEWED",
        "machine_stop_decision": "STOP_BEFORE_AUTHORITY_IDL_AND_KATS",
        "scope_boundary": {
            "authority_idl_allowed": False,
            "kats_allowed": False,
        },
        "schema_binding": {
            "path": (
                "docs/superpowers/specs/idl/task10/v10/review/schema/"
                "authority-design-decision-registry-v2.schema.json"
            ),
            "sha256": schema_sha256,
        },
        "source_bindings_by_id": {
            source_id: {"logical_source": "fixture.json", "sha256": digest64}
        },
        "evidence_refs_by_id": {
            evidence_id: {
                "claim_role": "AUTHORITY_FACT",
                "locator": {
                    "kind": "LINE_RANGE",
                    "ranges": ["L1-L2"],
                    "sections": ["fixture"],
                },
                "source_binding_id": source_id,
            }
        },
        "evidence_binding_expectations_by_key": {},
        "owners_by_id": {
            "OWN-0000": {
                "owner_id": "OWN-0000",
                "ordinal": 0,
                "owner_table": "fixture_owner",
                "payload": {},
            }
        },
        "schema_templates_by_id": {
            "TPL-0001": {
                "template_id": "TPL-0001",
                "semantic_key": "fixture-template",
                "payload": {},
            }
        },
        "reference_fields_by_id": {
            "FLD-0001": {
                "field_id": "FLD-0001",
                "order_key": [0, 0, 0, 0],
                "payload": {},
            }
        },
        "discriminator_branches_by_id": {
            "BR-0001": {
                "branch_id": "BR-0001",
                "predicate": {"mode": "ANY"},
                "consumer_rule_ids": ["PCR-0001"],
                "payload": {},
            }
        },
        "decisions_by_id": {
            "T10-G18-DD-001": {
                "decision_id": "T10-G18-DD-001",
                "ordinal": 0,
                "reference_kinds": ["ANCHOR_NOT_RL"],
                "compiled_rule_ids": ["PCR-0001"],
                "evidence_ref_ids": [evidence_id],
                "design_payload": {
                    "branch_instance_ids": [],
                    "case_labels": [],
                },
                "payload": {},
            }
        },
        "coverage_rows_by_id": {
            "ROW-0001": {
                "coverage_row_id": "ROW-0001",
                "ordinal": 0,
                "compiled_rule_ids": ["PCR-0001"],
                "evidence_ref_ids": [evidence_id],
                "payload": {},
            }
        },
        "compiled_rules_by_id": {
            "PCR-0001": {
                "rule_id": "PCR-0001",
                "ordinal": 0,
                "provenance": {"class": "COVERAGE_DERIVED"},
                "evidence_ref_ids": [evidence_id],
                "payload": {},
            }
        },
        "legacy_aliases_by_id": {
            "ALS-0001": {
                "alias_id": "ALS-0001",
                "decision_id": "T10-G18-DD-001",
                "payload": {},
            }
        },
        "legacy_rehydration": {
            "predecessor_format": ("selcal.task10.g18.authority-design-decision-registry.v1"),
            "design_status_rule": "fixture design status",
            "input_binding_ids": [f"SRC-{index:064x}" for index in range(5)],
            "null_row_summary": {},
            "machine_verifiable_invariants": {},
            "review_gate": {},
            "scope_boundary": {},
        },
        "invariants_by_id": {
            "INV-0001": {
                "invariant_id": "INV-0001",
                "kind": "COUNT_EQUALS",
                "description": "fixture invariant",
                "assertion": {"collection": "owners_by_id", "expected": 1},
            }
        },
    }


def load_generated_v2() -> dict[str, object]:
    value = json.loads(V2_REGISTRY.read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def legacy_canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def valid_attestation_fixture() -> dict[str, object]:
    return {
        "format": ("selcal.task10.g18.authority-design-decision-review-attestation.v1"),
        "attestation_id": "specification-review-001",
        "subject_binding": {
            "path": (
                "docs/superpowers/specs/idl/task10/v10/review/"
                "authority-design-decision-registry-v2.json"
            ),
            "sha256": digest(V2_REGISTRY),
        },
        "registry_schema_binding": {
            "path": (
                "docs/superpowers/specs/idl/task10/v10/review/schema/"
                "authority-design-decision-registry-v2.schema.json"
            ),
            "sha256": digest(REGISTRY_SCHEMA),
        },
        "reviewed_artifact_bindings": {
            role: {"path": path, "sha256": digest(ROOT / path)}
            for role, path in REVIEWED_ARTIFACT_PATHS.items()
        },
        "reviewer": {
            "identity": "independent-specification-reviewer",
            "type": "INDEPENDENT_AGENT",
            "role": "specification-equivalence-review",
            "independence_declaration": (
                "Read-only reviewer; no subject, schema, generator, validator, "
                "test, index, or attestation bytes were edited."
            ),
        },
        "review_scope": [
            "representation equivalence",
            "STOP boundary preservation",
        ],
        "verdict": "PASS",
        "finding_counts": {"blocker": 0, "major": 0, "minor": 0, "total": 0},
        "effect": "NO_AUTHORITY_PROMOTION",
        "created_at": "2026-08-30T12:00:00Z",
    }


def attestation_target(
    attestation_id: str = "specification-review-001",
) -> Path:
    return (
        REVIEW
        / "attestations"
        / f"sha256-{digest(V2_REGISTRY)}"
        / f"review-{attestation_id}.json"
    )


def test_v1_review_evidence_is_immutable() -> None:
    assert digest(REVIEW / "authority-design-decision-registry-v1.json") == (
        "047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398"
    )
    assert digest(REVIEW / "authority-design-decision-matrix-v1.md") == (
        "8b75baf1db9425daddcfd150f0f3c4638684e42e15fa717c2c2044fb3a8f3287"
    )


def test_migrator_binds_exact_v1_hashes() -> None:
    module = load_migrator()
    assert module.V1_REGISTRY_SHA256 == (
        "047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398"
    )
    assert module.V1_MATRIX_SHA256 == (
        "8b75baf1db9425daddcfd150f0f3c4638684e42e15fa717c2c2044fb3a8f3287"
    )


def test_canonical_json_is_diffable_and_idempotent() -> None:
    module = load_migrator()
    value = {"z": 1, "a": {"d": 4, "b": 2}}
    expected = '{\n  "a": {\n    "b": 2,\n    "d": 4\n  },\n  "z": 1\n}\n'
    encoded = module.canonical_json_bytes(value)
    assert encoded.decode("utf-8") == expected
    assert module.parse_canonical_json(encoded) == value


def test_migrated_evidence_is_bound_to_the_exact_source() -> None:
    module = load_migrator()
    v1 = module.parse_v1_bytes((REVIEW / "authority-design-decision-registry-v1.json").read_bytes())
    normalized = module.normalize_evidence_bindings(v1)
    sources = normalized["source_bindings_by_id"]
    evidence_refs = normalized["evidence_refs_by_id"]

    assert len(sources) == 6
    assert evidence_refs
    for evidence in evidence_refs.values():
        assert evidence["source_binding_id"] in sources
        assert "authority_lines" not in evidence
        assert evidence["locator"]["kind"] in {
            "LINE_RANGE",
            "JSON_POINTER",
            "DECISION_ONLY",
        }
        key = module.evidence_binding_key(evidence["locator"], evidence["claim_role"])
        assert (
            normalized["legacy_locator_claim_to_source_binding"][key]
            == evidence["source_binding_id"]
        )

    decision_only = [
        evidence
        for evidence in evidence_refs.values()
        if evidence["locator"]["kind"] == "DECISION_ONLY"
    ]
    assert decision_only
    assert all(
        sources[evidence["source_binding_id"]]["sha256"] == module.V1_REGISTRY_SHA256
        for evidence in decision_only
    )


def test_valid_but_wrong_evidence_source_is_rejected() -> None:
    module = load_migrator()
    v1 = module.parse_v1_bytes((REVIEW / "authority-design-decision-registry-v1.json").read_bytes())
    normalized = module.normalize_evidence_bindings(v1)
    mutation = json.loads(json.dumps(normalized))
    evidence = next(iter(mutation["evidence_refs_by_id"].values()))
    wrong_source_id = next(
        source_id
        for source_id in mutation["source_bindings_by_id"]
        if source_id != evidence["source_binding_id"]
    )
    evidence["source_binding_id"] = wrong_source_id

    with pytest.raises(ValueError, match="EVIDENCE_WRONG_VALID_SOURCE"):
        module.validate_evidence_bindings(mutation)


def test_registry_schema_self_validates_and_accepts_minimal_fixture() -> None:
    validator = load_validator()
    schema = json.loads(REGISTRY_SCHEMA.read_text("utf-8"))
    fixture = minimal_valid_v2_registry_fixture(digest(REGISTRY_SCHEMA))
    validator.validate_schema_document(schema)
    validator.validate_registry_schema_binding(fixture, REGISTRY_SCHEMA)
    validator.validate_instance(schema, fixture)
    decision = fixture["decisions_by_id"]["T10-G18-DD-001"]
    assert isinstance(decision["reference_kinds"], list)
    assert "branch_instances" not in decision["design_payload"]


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-001"].__setitem__(
                "reference_kinds", "ANCHOR_NOT_RL"
            ),
            "SCHEMA_TYPE",
        ),
        (
            lambda value: value["scope_boundary"].__setitem__("authority_idl_allowed", "false"),
            "SCHEMA_TYPE",
        ),
        (
            lambda value: value["decisions_by_id"]["T10-G18-DD-001"]["design_payload"].__setitem__(
                "branch_instances", "legacy-overload"
            ),
            "SCHEMA_ADDITIONAL_PROPERTY",
        ),
        (
            lambda value: value.__setitem__("unexpected", True),
            "SCHEMA_ADDITIONAL_PROPERTY",
        ),
    ],
)
def test_registry_schema_rejects_overloads_and_open_shapes(mutation, code) -> None:
    validator = load_validator()
    schema = json.loads(REGISTRY_SCHEMA.read_text("utf-8"))
    fixture = minimal_valid_v2_registry_fixture(digest(REGISTRY_SCHEMA))
    mutation(fixture)
    with pytest.raises(ValueError, match=code):
        validator.validate_instance(schema, fixture)


def test_registry_rejects_changed_schema_sha() -> None:
    validator = load_validator()
    fixture = minimal_valid_v2_registry_fixture("f" * 64)
    with pytest.raises(ValueError, match="SCHEMA_SHA_MISMATCH"):
        validator.validate_registry_schema_binding(fixture, REGISTRY_SCHEMA)


def test_schema_document_rejects_unknown_keyword() -> None:
    validator = load_validator()
    schema = json.loads(REGISTRY_SCHEMA.read_text("utf-8"))
    mutation = copy.deepcopy(schema)
    mutation["unsupported_future_keyword"] = True
    with pytest.raises(ValueError, match="UNSUPPORTED_SCHEMA_KEYWORD"):
        validator.validate_schema_document(mutation)


def test_v2_has_one_rule_definition_and_exact_partitions() -> None:
    package = load_generated_v2()
    rules = package["compiled_rules_by_id"]
    assert len(rules) == 570
    assert list(rules) == [f"PCR-{index:04d}" for index in range(1, 571)]
    assert Counter(rule["provenance"]["class"] for rule in rules.values()) == {
        "COVERAGE_DERIVED": 509,
        "POST_SCHEMA_EXTRA": 9,
        "AUTHORITY_CLOSED_INVENTORY": 52,
    }
    assert all("compiled_rules" not in row for row in package["coverage_rows_by_id"].values())
    assert all(
        "compilation_rules" not in decision for decision in package["decisions_by_id"].values()
    )


def test_generated_v2_validates_against_its_exact_schema() -> None:
    validator = load_validator()
    schema = json.loads(REGISTRY_SCHEMA.read_text("utf-8"))
    package = load_generated_v2()
    validator.validate_registry_schema_binding(package, REGISTRY_SCHEMA)
    validator.validate_instance(schema, package)


def test_v1_v2_v1_is_exact_bytes() -> None:
    module = load_migrator()
    v1_bytes = (REVIEW / "authority-design-decision-registry-v1.json").read_bytes()
    v2 = module.migrate_v1_bytes(v1_bytes)
    assert module.legacy_v1_bytes(v2) == v1_bytes


def test_rehydrator_works_without_v1_or_repository_access(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    copied_path = tmp_path / MIGRATOR.name
    copied_path.write_bytes(MIGRATOR.read_bytes())
    v2_path = tmp_path / V2_REGISTRY.name
    v2_path.write_bytes(V2_REGISTRY.read_bytes())
    spec = importlib.util.spec_from_file_location("isolated_task10_migrator", copied_path)
    assert spec is not None and spec.loader is not None
    copied = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(copied)
    v2 = json.loads(v2_path.read_text("utf-8"))

    def repository_read_forbidden(*_args, **_kwargs):
        raise AssertionError("REPOSITORY_READ_FORBIDDEN_DURING_REHYDRATION")

    monkeypatch.setattr(copied.Path, "read_bytes", repository_read_forbidden)
    restored = copied.legacy_v1_bytes(v2)
    assert sha256(restored).hexdigest() == (
        "047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398"
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["decisions"][0].__setitem__(
            "strongest_support", "metamorphic support mutation"
        ),
        lambda value: value["null_row_coverage"].__setitem__(
            "measurement_basis", "metamorphic measurement mutation"
        ),
        lambda value: value["legacy_aliases"][0].__setitem__("legacy_code", "METAMORPHIC_ALIAS"),
    ],
)
def test_rehydrator_tracks_type_preserving_v1_mutations(mutation) -> None:
    module = load_migrator()
    original = module.parse_v1_bytes(
        (REVIEW / "authority-design-decision-registry-v1.json").read_bytes()
    )
    mutated = copy.deepcopy(original)
    mutation(mutated)
    v2 = module.migrate_v1(mutated, registry_schema_sha256=digest(REGISTRY_SCHEMA))
    assert module.legacy_v1_bytes(v2) == legacy_canonical_bytes(mutated)


def test_v1_and_v2_independent_semantic_projections_match() -> None:
    module = load_migrator()
    v1 = module.parse_v1_bytes((REVIEW / "authority-design-decision-registry-v1.json").read_bytes())
    v2 = load_generated_v2()
    from_v1 = module.semantic_projection_from_v1(v1)
    from_v2 = module.semantic_projection_from_v2(v2)
    v1_bytes = module.canonical_json_bytes(from_v1)
    v2_bytes = module.canonical_json_bytes(from_v2)
    assert v1_bytes == v2_bytes
    assert sha256(v1_bytes).hexdigest() == sha256(v2_bytes).hexdigest()


def test_v1_and_v2_independent_rule_projections_match() -> None:
    module = load_migrator()
    v1 = module.parse_v1_bytes((REVIEW / "authority-design-decision-registry-v1.json").read_bytes())
    v2 = load_generated_v2()
    assert module.rule_projection_from_v1(v1) == module.rule_projection_from_v2(v2)


def test_v2_generation_is_byte_deterministic() -> None:
    module = load_migrator()
    v1_bytes = (REVIEW / "authority-design-decision-registry-v1.json").read_bytes()
    schema_sha = digest(REGISTRY_SCHEMA)
    first = module.canonical_json_bytes(
        module.migrate_v1_bytes(v1_bytes, registry_schema_sha256=schema_sha)
    )
    second = module.canonical_json_bytes(
        module.migrate_v1_bytes(v1_bytes, registry_schema_sha256=schema_sha)
    )
    assert first == second == V2_REGISTRY.read_bytes()


def test_every_normative_invariant_is_declarative_and_executable() -> None:
    validator = load_validator()
    package = load_generated_v2()
    allowed = {
        "COUNT_EQUALS",
        "UNIQUE_KEY",
        "FOREIGN_KEY",
        "SET_EQUALS",
        "EXACT_PARTITION",
        "PARTITION_COUNTS",
        "ALL_MATCH",
        "SUM_EQUALS",
        "SOURCE_DIGEST_MATCH",
        "CANONICAL_ORDER",
    }
    assert len(package["invariants_by_id"]) >= 18
    for invariant in package["invariants_by_id"].values():
        assert invariant["kind"] in allowed
        assert invariant["description"]
        assert isinstance(invariant["assertion"], dict)
        assert invariant["assertion"]
    validator.validate_package(
        package,
        schema_path=REGISTRY_SCHEMA,
        repository_root=ROOT,
        markdown_text="NON_NORMATIVE_DERIVED_VIEW",
    )


def test_invariant_assertion_surfaces_reject_unknown_fields() -> None:
    validator = load_validator()
    schema = json.loads(REGISTRY_SCHEMA.read_text("utf-8"))
    package = load_generated_v2()
    invariant = next(iter(package["invariants_by_id"].values()))
    invariant["assertion"]["ignored_unknown_control"] = True

    with pytest.raises(ValueError, match="SCHEMA_ONE_OF"):
        validator.validate_instance(schema, package)


EXPECTED_MUTATION_FAILURES = {
    "duplicated_rule_body": "DUPLICATE_RULE_BODY",
    "dangling_rule_id": "FOREIGN_KEY_MISSING",
    "wrong_rule_partition": "RULE_PARTITION_COUNTS",
    "removed_coverage_row": "COUNT_MISMATCH",
    "missing_source_binding": "EVIDENCE_SOURCE_MISSING",
    "wrong_valid_evidence_source": "EVIDENCE_WRONG_VALID_SOURCE",
    "changed_evidence_locator": "EVIDENCE_REF_ID_MISMATCH",
    "decision_only_promoted_to_line": "DECISION_ONLY_PROMOTED_TO_LINE",
    "scalar_reference_kind": "SCHEMA_TYPE",
    "string_boolean": "SCHEMA_TYPE",
    "changed_ordered_tuple": "RULE_PROJECTION_MISMATCH",
    "duplicate_template_key": "DUPLICATE_TEMPLATE_SEMANTIC_KEY",
    "embedded_full_registry_markdown": "MARKDOWN_EMBEDDED_REGISTRY",
    "review_verdict_inside_registry": "SCHEMA_ADDITIONAL_PROPERTY",
    "changed_owner_semantics": "SEMANTIC_PROJECTION_MISMATCH",
    "changed_owner_table_semantics": "SEMANTIC_PROJECTION_MISMATCH",
    "changed_reference_field_semantics": "SEMANTIC_PROJECTION_MISMATCH",
    "changed_template_semantics": "SEMANTIC_PROJECTION_MISMATCH",
    "removed_coverage_evidence_semantics": "DETERMINISTIC_REGENERATION_MISMATCH",
    "coordinated_wrong_valid_evidence_source": "RULE_PROJECTION_MISMATCH",
    "unknown_invariant_assertion_control": "SCHEMA_ONE_OF",
    "changed_v1_sha": "SOURCE_BINDING_ID_MISMATCH",
}


def test_adversarial_mutation_catalog_rejects_every_quality_failure() -> None:
    validator = load_validator()
    package = load_generated_v2()
    cases = validator.adversarial_mutations(package)
    assert set(cases) == set(EXPECTED_MUTATION_FAILURES)
    for name, case in cases.items():
        expected_code = EXPECTED_MUTATION_FAILURES[name]
        with pytest.raises(ValueError, match=expected_code):
            validator.validate_package(
                case["registry"],
                schema_path=REGISTRY_SCHEMA,
                repository_root=ROOT,
                markdown_text=case["markdown_text"],
            )


def test_validator_self_test_executes_every_adverse_case() -> None:
    validator = load_validator()
    result = validator.run_self_test(
        registry_path=V2_REGISTRY,
        schema_path=REGISTRY_SCHEMA,
        repository_root=ROOT,
    )
    assert result == {
        "positive_package": "PASS",
        "mutation_cases": len(EXPECTED_MUTATION_FAILURES),
        "mutation_failures_observed": len(EXPECTED_MUTATION_FAILURES),
    }


def test_validator_file_entry_rejects_noncanonical_registry_bytes(
    tmp_path: Path,
) -> None:
    validator = load_validator()
    package = load_generated_v2()
    noncanonical = tmp_path / "authority-design-decision-registry-v2.json"
    noncanonical.write_text(
        json.dumps(package, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="NON_CANONICAL_REGISTRY_BYTES"):
        validator.validate_registry_file(
            registry_path=noncanonical,
            schema_path=REGISTRY_SCHEMA,
            repository_root=ROOT,
            markdown_text=V2_INDEX.read_text("utf-8"),
        )


def test_validator_file_entry_rejects_seven_file_baseline_drift(
    tmp_path: Path,
) -> None:
    validator = load_validator()
    baseline_relative = (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-review-package-v2-baseline.json"
    )
    baseline = json.loads((ROOT / baseline_relative).read_text("utf-8"))
    for binding in baseline["files"]:
        source = ROOT / binding["path"]
        target = tmp_path / binding["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    manifest_target = tmp_path / baseline_relative
    manifest_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / baseline_relative, manifest_target)
    matrix_target = tmp_path / REVIEWED_ARTIFACT_PATHS["V1_MATRIX"]
    matrix_target.write_bytes(matrix_target.read_bytes() + b"\nbaseline drift\n")

    with pytest.raises(ValueError, match="BASELINE_HASH_DRIFT"):
        validator.validate_registry_file(
            registry_path=V2_REGISTRY,
            schema_path=REGISTRY_SCHEMA,
            repository_root=tmp_path,
            markdown_text=V2_INDEX.read_text("utf-8"),
        )


def test_self_test_checks_baseline_before_reading_markdown_index(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    baseline_relative = (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-review-package-v2-baseline.json"
    )
    baseline = json.loads((ROOT / baseline_relative).read_text("utf-8"))
    for binding in baseline["files"]:
        source = ROOT / binding["path"]
        target = tmp_path / binding["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    manifest_target = tmp_path / baseline_relative
    manifest_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / baseline_relative, manifest_target)
    matrix_target = tmp_path / REVIEWED_ARTIFACT_PATHS["V1_MATRIX"]
    matrix_target.write_bytes(matrix_target.read_bytes() + b"\nbaseline drift\n")

    index_reads: list[Path] = []
    original_read_text = Path.read_text

    def tracked_read_text(path: Path, *args, **kwargs) -> str:
        if path == V2_INDEX:
            index_reads.append(path)
            raise AssertionError("INDEX_READ_BEFORE_BASELINE")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", tracked_read_text)

    with pytest.raises(ValueError, match="BASELINE_HASH_DRIFT"):
        validator.run_self_test(
            registry_path=V2_REGISTRY,
            schema_path=REGISTRY_SCHEMA,
            repository_root=tmp_path,
        )
    assert index_reads == []


def test_markdown_index_is_concise_and_non_normative() -> None:
    text = V2_INDEX.read_text("utf-8")
    assert "NON_NORMATIVE_DERIVED_VIEW" in text
    assert "STOP_BEFORE_AUTHORITY_IDL_AND_KATS" in text
    assert text.count("| T10-G18-DD-") == 23
    assert "```json" not in text
    assert "compiled_rules_by_id" not in text
    assert len(text.encode("utf-8")) < 100_000
    assert digest(V2_REGISTRY) in text
    assert digest(REGISTRY_SCHEMA) in text


def test_markdown_index_generation_is_byte_deterministic() -> None:
    module = load_migrator()
    package = load_generated_v2()
    registry_bytes = V2_REGISTRY.read_bytes()
    first = module.render_markdown_index(package, registry_bytes).encode("utf-8")
    second = module.render_markdown_index(package, registry_bytes).encode("utf-8")
    assert first == second == V2_INDEX.read_bytes()


def test_review_results_are_detached_from_subject_bytes() -> None:
    package = load_generated_v2()

    def keys(value: object) -> set[str]:
        if isinstance(value, dict):
            return set(value) | {key for child in value.values() for key in keys(child)}
        if isinstance(value, list):
            return {key for child in value for key in keys(child)}
        return set()

    all_keys = keys(package)
    assert "independent_review_result" not in all_keys
    assert "review_verdict" not in all_keys


def test_attestation_contract_is_append_only_and_exact_hash_bound() -> None:
    validator = load_validator()
    readme = ATTESTATION_README.read_text("utf-8")
    assert "APPEND_ONLY" in readme
    assert "NO_AUTHORITY_PROMOTION" in readme
    assert "read-only reviewer" in readme
    assert "`PREWRITE`" in readme
    assert "`READBACK`" in readme
    attestation = valid_attestation_fixture()
    target = attestation_target()
    validator.validate_attestation(
        attestation,
        attestation_schema_path=ATTESTATION_SCHEMA,
        subject_path=V2_REGISTRY,
        registry_schema_path=REGISTRY_SCHEMA,
        attestation_path=target,
    )


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (
            lambda value: value["subject_binding"].__setitem__("sha256", "f" * 64),
            "ATTESTATION_SUBJECT_SHA_MISMATCH",
        ),
        (
            lambda value: value["subject_binding"].__setitem__("path", "json"),
            "ATTESTATION_SUBJECT_PATH_MISMATCH",
        ),
        (
            lambda value: value["registry_schema_binding"].__setitem__("sha256", "f" * 64),
            "ATTESTATION_SCHEMA_SHA_MISMATCH",
        ),
        (
            lambda value: value["registry_schema_binding"].__setitem__("path", "json"),
            "ATTESTATION_SCHEMA_PATH_MISMATCH",
        ),
        (
            lambda value: value["finding_counts"].__setitem__("total", 1),
            "ATTESTATION_FINDING_TOTAL_MISMATCH",
        ),
        (
            lambda value: value["finding_counts"].__setitem__("major", 1),
            "ATTESTATION_PASS_WITH_FINDINGS",
        ),
        (
            lambda value: value["reviewer"].pop("independence_declaration"),
            "SCHEMA_REQUIRED",
        ),
        (
            lambda value: value.__setitem__("effect", "AUTHORITY_PROMOTION"),
            "SCHEMA_CONST",
        ),
        (
            lambda value: value["reviewer"].__setitem__(
                "type", "IMPLEMENTER_SELF_CHECK"
            ),
            "SCHEMA_ONE_OF",
        ),
        (
            lambda value: value["reviewed_artifact_bindings"]["VALIDATOR"].__setitem__(
                "sha256", "f" * 64
            ),
            "ATTESTATION_PACKAGE_SHA_MISMATCH",
        ),
        (
            lambda value: value["reviewed_artifact_bindings"]["VALIDATOR"].__setitem__(
                "path", REVIEWED_ARTIFACT_PATHS["V2_REGISTRY"]
            ),
            "ATTESTATION_PACKAGE_PATH_MISMATCH",
        ),
        (
            lambda value: value["reviewed_artifact_bindings"].pop("VALIDATOR"),
            "SCHEMA_REQUIRED",
        ),
        (
            lambda value: value.__setitem__(
                "supersedes",
                {
                    "path": (
                        "docs/superpowers/specs/idl/task10/v10/review/attestations/"
                        f"sha256-{digest(V2_REGISTRY)}/review-prior-review-001.json"
                    ),
                    "sha256": "0" * 64,
                },
            ),
            "ATTESTATION_SUPERSEDED_FILE_MISSING",
        ),
        (
            lambda value: value.__setitem__(
                "supersedes",
                {
                    "path": str(attestation_target().relative_to(ROOT)),
                    "sha256": "0" * 64,
                },
            ),
            "ATTESTATION_SUPERSEDES_SELF",
        ),
    ],
)
def test_attestation_rejects_invalid_binding_or_verdict(mutation, code) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    mutation(attestation)
    target = attestation_target()
    with pytest.raises(ValueError, match=code):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
        )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["reviewer"].__setitem__("identity", " "),
        lambda value: value["reviewer"].__setitem__("role", "\t"),
        lambda value: value["reviewer"].__setitem__(
            "independence_declaration", "\n"
        ),
        lambda value: value.__setitem__("review_scope", [" "]),
    ],
)
def test_attestation_rejects_blank_reviewer_provenance(mutation) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    mutation(attestation)

    with pytest.raises(ValueError, match="SCHEMA_PATTERN"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=attestation_target(),
        )


@pytest.mark.parametrize(
    "created_at",
    [
        "0000-00-00T00:00:00Z",
        "2026-02-29T12:00:00Z",
        "2026-08-30T24:00:00Z",
        "2026-08-30T12:60:00Z",
    ],
)
def test_attestation_rejects_invalid_utc_timestamp(created_at: str) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    attestation["created_at"] = created_at

    with pytest.raises(ValueError, match="ATTESTATION_CREATED_AT_INVALID"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=attestation_target(),
        )


def test_attestation_rejects_mutable_overwrite_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()
    original_exists = Path.exists
    monkeypatch.setattr(
        Path,
        "exists",
        lambda self: True if self == target else original_exists(self),
    )
    with pytest.raises(ValueError, match="ATTESTATION_OVERWRITE_FORBIDDEN"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
        )


def test_attestation_rejects_false_superseded_digest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()
    prior = target.with_name("review-prior-review-001.json")
    attestation["supersedes"] = {
        "path": str(prior.relative_to(ROOT)),
        "sha256": "0" * 64,
    }
    original_is_file = Path.is_file
    original_read_bytes = Path.read_bytes
    monkeypatch.setattr(
        Path,
        "is_file",
        lambda self: True if self == prior else original_is_file(self),
    )
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda self: b"prior-attestation\n" if self == prior else original_read_bytes(self),
    )

    with pytest.raises(ValueError, match="ATTESTATION_SUPERSEDED_SHA_MISMATCH"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
        )


def test_attestation_rejects_non_attestation_superseded_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()
    prior = target.with_name("review-prior-review-001.json")
    prior_bytes = b"not an attestation\n"
    attestation["supersedes"] = {
        "path": str(prior.relative_to(ROOT)),
        "sha256": sha256(prior_bytes).hexdigest(),
    }
    original_is_file = Path.is_file
    original_read_bytes = Path.read_bytes
    monkeypatch.setattr(
        Path,
        "is_file",
        lambda self: True if self == prior else original_is_file(self),
    )
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda self: prior_bytes if self == prior else original_read_bytes(self),
    )

    with pytest.raises(ValueError, match="ATTESTATION_SUPERSEDED_CONTENT_INVALID"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
        )


def test_attestation_accepts_canonical_same_subject_superseded_record(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()
    prior = valid_attestation_fixture()
    prior["attestation_id"] = "prior-review-001"
    prior["created_at"] = "2026-08-30T11:59:59Z"
    prior_path = target.with_name("review-prior-review-001.json")
    prior_bytes = (
        json.dumps(
            prior,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        )
        + "\n"
    ).encode("utf-8")
    attestation["supersedes"] = {
        "path": str(prior_path.relative_to(ROOT)),
        "sha256": sha256(prior_bytes).hexdigest(),
    }
    original_is_file = Path.is_file
    original_read_bytes = Path.read_bytes
    monkeypatch.setattr(
        Path,
        "is_file",
        lambda self: True if self == prior_path else original_is_file(self),
    )
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda self: prior_bytes if self == prior_path else original_read_bytes(self),
    )

    validator.validate_attestation(
        attestation,
        attestation_schema_path=ATTESTATION_SCHEMA,
        subject_path=V2_REGISTRY,
        registry_schema_path=REGISTRY_SCHEMA,
        attestation_path=target,
    )


def test_attestation_readback_revalidates_exact_canonical_existing_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()
    stored_bytes = (
        json.dumps(
            attestation,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        )
        + "\n"
    ).encode("utf-8")
    original_exists = Path.exists
    original_read_bytes = Path.read_bytes
    monkeypatch.setattr(
        Path,
        "exists",
        lambda self: True if self == target else original_exists(self),
    )
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda self: stored_bytes if self == target else original_read_bytes(self),
    )

    validator.validate_attestation(
        attestation,
        attestation_schema_path=ATTESTATION_SCHEMA,
        subject_path=V2_REGISTRY,
        registry_schema_path=REGISTRY_SCHEMA,
        attestation_path=target,
        mode="READBACK",
    )


@pytest.mark.parametrize(
    ("stored_bytes", "code"),
    [
        (b"{}\n", "ATTESTATION_READBACK_CONTENT_MISMATCH"),
        (b"{\"not\":\"canonical\"}\n", "ATTESTATION_READBACK_CONTENT_MISMATCH"),
    ],
)
def test_attestation_readback_rejects_nonmatching_existing_file(
    monkeypatch: pytest.MonkeyPatch,
    stored_bytes: bytes,
    code: str,
) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()
    original_exists = Path.exists
    original_read_bytes = Path.read_bytes
    monkeypatch.setattr(
        Path,
        "exists",
        lambda self: True if self == target else original_exists(self),
    )
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda self: stored_bytes if self == target else original_read_bytes(self),
    )

    with pytest.raises(ValueError, match=code):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
            mode="READBACK",
        )


def test_attestation_readback_rejects_noncanonical_bytes_of_same_record(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()
    stored_bytes = (
        json.dumps(attestation, ensure_ascii=False, sort_keys=True) + "\n"
    ).encode("utf-8")
    original_exists = Path.exists
    original_read_bytes = Path.read_bytes
    monkeypatch.setattr(
        Path,
        "exists",
        lambda self: True if self == target else original_exists(self),
    )
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda self: stored_bytes if self == target else original_read_bytes(self),
    )

    with pytest.raises(ValueError, match="ATTESTATION_READBACK_CONTENT_MISMATCH"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
            mode="READBACK",
        )


def test_attestation_readback_requires_existing_file() -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()

    with pytest.raises(ValueError, match="ATTESTATION_READBACK_MISSING"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
            mode="READBACK",
        )


def test_attestation_rejects_unknown_validation_mode() -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = attestation_target()

    with pytest.raises(ValueError, match="ATTESTATION_VALIDATION_MODE_UNKNOWN"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
            mode="UNKNOWN",
        )


def test_attestation_rejects_target_outside_exact_review_root(tmp_path: Path) -> None:
    validator = load_validator()
    attestation = valid_attestation_fixture()
    target = tmp_path / attestation_target().parent.name / attestation_target().name

    with pytest.raises(ValueError, match="ATTESTATION_PATH_OUTSIDE_REVIEW_ROOT"):
        validator.validate_attestation(
            attestation,
            attestation_schema_path=ATTESTATION_SCHEMA,
            subject_path=V2_REGISTRY,
            registry_schema_path=REGISTRY_SCHEMA,
            attestation_path=target,
        )
