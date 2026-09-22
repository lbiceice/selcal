from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "docs/superpowers/specs/idl/task10/v10/review"
SEMANTIC_REVIEW = ROOT / "docs/superpowers/specs/task10/v10/semantic-review"
REGISTRY = REVIEW / "authority-design-decision-registry-v2.json"
ORACLE = SEMANTIC_REVIEW / "adjudicated-cross-representation-oracle-v1.json"
ORACLE_SCHEMA = (
    SEMANTIC_REVIEW / "adjudicated-cross-representation-oracle-v1.schema.json"
)
AUDITOR = SEMANTIC_REVIEW / "validate_registry_cross_representation_v1.py"
PREDECESSOR = (
    ROOT
    / "docs/superpowers/specs/"
    "2026-08-29-task10-deny-by-default-provider-proof-design.md"
)
CORRECTION_SPEC = (
    ROOT
    / "docs/superpowers/plans/"
    "2026-08-31-task10-authority-review-package-v3-correction.md"
)
EXPECTED_REGISTRY_SHA256 = (
    "77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5"
)
EXPECTED_ORACLE_SHA256 = (
    "c9db64895c2cb802919b34e24f78551aabf2bee1530ac562515f428614fb2118"
)
EXPECTED_SCHEMA_SHA256 = (
    "94b316ee6036a9d912248c4acf1d031cca5570770023007da15e0ad4b7086066"
)
EXPECTED_PREDECESSOR_SHA256 = (
    "74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff"
)
EXPECTED_CORRECTION_SPEC_SHA256 = (
    "85ababe68595f31f3df037a09d954b050fa718ecbc922bcd2bcf4b4838b20735"
)
CHECKED_DECISIONS = {
    "T10-G18-DD-001",
    "T10-G18-DD-004",
    "T10-G18-DD-006",
    "T10-G18-DD-007",
    "T10-G18-DD-009",
    "T10-G18-DD-011",
    "T10-G18-DD-016",
}


def load_auditor() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "task10_cross_representation_v1", AUDITOR
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load auditor from {AUDITOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_bytes().decode("utf-8"))
    assert isinstance(value, dict)
    return value


def audit_frozen(module: ModuleType) -> dict[str, object]:
    return module.audit_registry_paths(REGISTRY)


def audit_candidate(
    module: ModuleType,
    registry: dict[str, object],
    oracle: dict[str, object] | None = None,
) -> dict[str, object]:
    return module.audit_registry(registry, oracle or load_json(ORACLE))


def finding_keys(report: dict[str, object]) -> set[tuple[str, str, str]]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return {
        (finding["decision_id"], finding["code"], finding["severity"])
        for finding in findings
    }


def set_owner_discriminator(
    rule_payload: dict[str, object], path: str, value: str
) -> None:
    rule_payload["record_discriminator"] = {
        "mode": "ALL_EQUAL",
        "terms": [
            {
                "literal": {"type": "ENUM", "value": value},
                "operator": "EQUALS",
                "selector": {"namespace": "OWNER_RECORD", "path": [path]},
            }
        ],
    }


def replace_enum_term(
    rule_payload: dict[str, object], namespace: str, path: list[str], value: str
) -> None:
    terms = rule_payload["record_discriminator"]["terms"]
    matching = [
        term
        for term in terms
        if term["selector"] == {"namespace": namespace, "path": path}
    ]
    assert len(matching) == 1
    matching[0]["literal"]["value"] = value


def test_oracle_is_canonical_frozen_and_binds_all_exact_sources() -> None:
    oracle_bytes = ORACLE.read_bytes()
    oracle = load_json(ORACLE)
    canonical = (
        json.dumps(oracle, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")

    assert oracle_bytes == canonical
    assert sha256(oracle_bytes).hexdigest() == EXPECTED_ORACLE_SHA256
    assert sha256(REGISTRY.read_bytes()).hexdigest() == EXPECTED_REGISTRY_SHA256
    assert sha256(ORACLE_SCHEMA.read_bytes()).hexdigest() == EXPECTED_SCHEMA_SHA256
    assert sha256(PREDECESSOR.read_bytes()).hexdigest() == (
        EXPECTED_PREDECESSOR_SHA256
    )
    assert sha256(CORRECTION_SPEC.read_bytes()).hexdigest() == (
        EXPECTED_CORRECTION_SPEC_SHA256
    )
    assert set(oracle["checks_by_decision"]) == CHECKED_DECISIONS
    assert oracle["cli_exit_contract"] == {
        "audit_error": 3,
        "findings_hold": 1,
        "usage_error": 2,
    }
    assert oracle["adjudication_provenance"]["independent_review_status"] == (
        "PENDING_REREVIEW_AFTER_FALSE_GREEN_CORRECTION"
    )


def test_frozen_v2_registry_has_exact_scoped_adverse_ledger() -> None:
    module = load_auditor()
    report = audit_frozen(module)

    assert report["status"] == "HOLD_CROSS_REPRESENTATION_SEMANTIC_COLLISION"
    assert report["identity_mode"] == "FROZEN_EXACT_BYTES"
    assert report["structural_join_decision_count"] == 23
    assert report["machine_semantic_scope_count"] == 7
    assert set(report["checks_executed_by_decision"]) == CHECKED_DECISIONS
    assert len(report["not_semantically_audited"]) == 16
    assert report["severity_counts"] == {"BLOCKER": 0, "MAJOR": 6, "MINOR": 2}
    assert report["oracle_binding"] == {
        "path": str(ORACLE.resolve()),
        "sha256": EXPECTED_ORACLE_SHA256,
    }
    assert report["registry_binding"] == {
        "path": str(REGISTRY.resolve()),
        "sha256": EXPECTED_REGISTRY_SHA256,
    }
    assert finding_keys(report) == {
        ("T10-G18-DD-001", "DECISION_CENSUS_PATH_COUNT_MISMATCH", "MINOR"),
        ("T10-G18-DD-004", "CAPTURE_REFERENCE_SEMANTIC_COLLISION", "MAJOR"),
        ("T10-G18-DD-006", "REFERENCE_OWNER_TUPLE_MISMATCH", "MAJOR"),
        ("T10-G18-DD-007", "REFERENCE_OWNER_TUPLE_MISMATCH", "MAJOR"),
        ("T10-G18-DD-007", "REFERENCE_TYPE_NAME_MISMATCH", "MINOR"),
        ("T10-G18-DD-009", "CALLBACK_REFERENCE_SEMANTIC_COLLISION", "MAJOR"),
        ("T10-G18-DD-011", "PROVIDER_REFERENCE_SEMANTIC_COLLISION", "MAJOR"),
        ("T10-G18-DD-016", "PROVIDER_REFERENCE_SEMANTIC_COLLISION", "MAJOR"),
    }


def test_unbound_library_diagnostic_never_claims_frozen_or_pass(
    tmp_path: Path,
) -> None:
    module = load_auditor()
    report = audit_candidate(module, load_json(REGISTRY))

    assert report["identity_mode"] == "UNBOUND_PARSED_OBJECT_DIAGNOSTIC_ONLY"
    assert report["status"] == (
        "UNBOUND_PARSED_OBJECT_DIAGNOSTIC_ONLY_WITH_FINDINGS"
    )
    assert report["oracle_binding"] == {"path": None, "sha256": None}
    assert report["registry_binding"] == {"path": None, "sha256": None}
    assert "PASS" not in report["status"]
    assert "audited_decision_count" not in report
    assert "decisions_without_detected_collision" not in report
    assert report["claim_ceiling"] == (
        "READ_ONLY_SCOPED_COLLISION_LEDGER_NOT_AUTHORITY_NOT_V3_CORRECTION"
    )

    spoofed = load_json(REGISTRY)
    spoofed["decisions_by_id"]["T10-G18-DD-002"]["payload"]["title"] = "FAKE"
    spoofed_report = module.audit_registry(spoofed, load_json(ORACLE))
    assert spoofed_report["identity_mode"] == (
        "UNBOUND_PARSED_OBJECT_DIAGNOSTIC_ONLY"
    )
    with pytest.raises(TypeError):
        module.audit_registry(
            spoofed,
            load_json(ORACLE),
            registry_path="FAKE",
        )

    minified = tmp_path / "minified-registry.json"
    minified.write_text(
        json.dumps(load_json(REGISTRY), ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="REGISTRY_PATH_MISMATCH"):
        module.audit_registry_paths(minified)


def test_structural_join_and_global_closure_reject_bidirectional_false_greens() -> None:
    module = load_auditor()
    registry = load_json(REGISTRY)
    oracle = load_json(ORACLE)

    assert module.global_structural_closure_details(registry, oracle) == {}
    assert all(
        module.decision_join_details(registry, oracle, decision_id) == {}
        for decision_id in registry["decisions_by_id"]
    )

    missing_forward = copy.deepcopy(registry)
    missing_forward["decisions_by_id"]["T10-G18-DD-002"][
        "compiled_rule_ids"
    ].pop()
    assert module.decision_join_details(
        missing_forward, oracle, "T10-G18-DD-002"
    )["forward_reverse_rule_id_mismatch"]

    fake_branch = copy.deepcopy(registry)
    fake_branch["decisions_by_id"]["T10-G18-DD-002"]["design_payload"][
        "branch_instance_ids"
    ].append("FAKE-ORPHAN-BRANCH")
    details = module.decision_join_details(fake_branch, oracle, "T10-G18-DD-002")
    assert details["missing_listed_branch_ids"] == ["FAKE-ORPHAN-BRANCH"]
    assert details["listed_unconsumed_branch_mismatch"]["extra"] == [
        "FAKE-ORPHAN-BRANCH"
    ]

    wrong_backlink = copy.deepcopy(registry)
    branch_id = wrong_backlink["compiled_rules_by_id"]["PCR-0213"]["payload"][
        "branch_instance_id"
    ]
    wrong_backlink["discriminator_branches_by_id"][branch_id][
        "consumer_rule_ids"
    ] = []
    assert module.decision_join_details(
        wrong_backlink, oracle, "T10-G18-DD-009"
    )["branch_backlink_mismatch"]

    wrong_tag = copy.deepcopy(registry)
    wrong_tag["discriminator_branches_by_id"]["T10-G18-DD-002-BR3-0007"][
        "payload"
    ]["branch_tag_value"] = "WRONG"
    assert module.decision_join_details(
        wrong_tag, oracle, "T10-G18-DD-002"
    )["branch_tag_predicate_mismatch"]

    missing_tag = copy.deepcopy(registry)
    missing_tag["discriminator_branches_by_id"]["T10-G18-DD-002-BR3-0007"][
        "payload"
    ]["branch_tag_field"] = None
    assert module.decision_join_details(
        missing_tag, oracle, "T10-G18-DD-002"
    )["closed_reference_branch_tag_semantic_mismatch"]

    wrong_manifest_path = copy.deepcopy(registry)
    rows = wrong_manifest_path["decisions_by_id"]["T10-G18-DD-009"]["payload"][
        "exact_chosen_wire_or_matrix"
    ]["coverage_compilation_manifest"]
    rows[0]["compiled_field_paths"][0] = "wrong.path"
    assert module.global_structural_closure_details(
        wrong_manifest_path, oracle
    )["manifest_rule_projection_mismatch"]

    coordinated_delete = copy.deepcopy(registry)
    del coordinated_delete["compiled_rules_by_id"]["PCR-0010"]
    coordinated_delete["decisions_by_id"]["T10-G18-DD-002"][
        "compiled_rule_ids"
    ].remove("PCR-0010")
    manifest = coordinated_delete["decisions_by_id"]["T10-G18-DD-002"][
        "payload"
    ]["exact_chosen_wire_or_matrix"]["coverage_compilation_manifest"]
    row = next(row for row in manifest if "PCR-0010" in row["compiled_rule_ids"])
    position = row["compiled_rule_ids"].index("PCR-0010")
    row["compiled_rule_ids"].pop(position)
    row["compiled_field_paths"].pop(position)
    coordinated_delete["decisions_by_id"]["T10-G18-DD-002"]["payload"][
        "expected_rl_universe_effect"
    ]["emitted_reference_rules"] -= 1
    closure = module.global_structural_closure_details(coordinated_delete, oracle)
    assert closure["global_count_mismatch"]["observed"]["rules"] == 569
    assert closure["closed_id_range_mismatch"]["rules"]["missing"] == [
        "PCR-0010"
    ]

    coordinated_orphan = copy.deepcopy(registry)
    orphan_rule = coordinated_orphan["compiled_rules_by_id"]["PCR-0012"]
    orphan_branch_id = orphan_rule["payload"]["branch_instance_id"]
    orphan_rule["payload"]["record_discriminator"] = {"mode": "ANY"}
    orphan_rule["payload"]["branch_instance_id"] = None
    coordinated_orphan["decisions_by_id"]["T10-G18-DD-002"][
        "design_payload"
    ]["branch_instance_ids"].remove(orphan_branch_id)
    coordinated_orphan["discriminator_branches_by_id"][orphan_branch_id][
        "consumer_rule_ids"
    ] = []
    closure = module.global_structural_closure_details(coordinated_orphan, oracle)
    assert orphan_branch_id in closure["orphan_or_invalid_branch_ids"]

    disguised_orphan = copy.deepcopy(coordinated_orphan)
    disguised_orphan["discriminator_branches_by_id"][orphan_branch_id]["payload"][
        "validator_only"
    ] = True
    closure = module.global_structural_closure_details(disguised_orphan, oracle)
    assert closure["validator_only_branch_projection_closure"]

    wrong_template_ordinal = copy.deepcopy(registry)
    wrong_template_ordinal["schema_templates_by_id"]["TPL-0001"]["payload"][
        "template_ordinal"
    ] = 999
    closure = module.global_structural_closure_details(
        wrong_template_ordinal, oracle
    )
    assert "OWN-0000" in closure["template_ordinal_closure"]

    missing_template_ordinal = copy.deepcopy(registry)
    missing_template_ordinal["schema_templates_by_id"]["TPL-0001"]["payload"][
        "template_ordinal"
    ] = None
    closure = module.global_structural_closure_details(
        missing_template_ordinal, oracle
    )
    assert "TPL-0001" in closure["template_owner_order_closure"]["invalid_ids"]

    swapped_template_ordinals = copy.deepcopy(registry)
    first = swapped_template_ordinals["schema_templates_by_id"]["TPL-0003"]
    second = swapped_template_ordinals["schema_templates_by_id"]["TPL-0004"]
    first["payload"]["template_ordinal"], second["payload"]["template_ordinal"] = (
        second["payload"]["template_ordinal"],
        first["payload"]["template_ordinal"],
    )
    closure = module.global_structural_closure_details(
        swapped_template_ordinals, oracle
    )
    assert closure["template_owner_order_closure"]["sorted_ids_match"] is False

    fake_owner = copy.deepcopy(registry)
    fake_owner["schema_templates_by_id"]["TPL-0001"]["payload"][
        "owner_id"
    ] = "OWN-FAKE"
    fake_owner["schema_templates_by_id"]["TPL-0001"]["semantic_key"] = (
        "None|OWNER:RootInputContract|ANY|RootInputContract"
    )
    closure = module.global_structural_closure_details(fake_owner, oracle)
    assert "TPL-0001" in closure["template_owner_order_closure"]["invalid_ids"]

    wrong_template_semantic_key = copy.deepcopy(registry)
    wrong_template_semantic_key["schema_templates_by_id"]["TPL-0001"][
        "semantic_key"
    ] = "WRONG"
    closure = module.global_structural_closure_details(
        wrong_template_semantic_key, oracle
    )
    assert "TPL-0001" in closure["template_semantic_key_closure"]["invalid_ids"]

    wrong_reference_order = copy.deepcopy(registry)
    wrong_reference_order["reference_fields_by_id"]["FLD-0001"]["order_key"][
        0
    ] = 999
    closure = module.global_structural_closure_details(
        wrong_reference_order, oracle
    )
    assert "FLD-0001" in closure["reference_field_order_closure"]["invalid_ids"]

    wrong_reference_tail = copy.deepcopy(registry)
    wrong_reference_tail["reference_fields_by_id"]["FLD-0001"]["order_key"][
        3
    ] = 999
    closure = module.global_structural_closure_details(
        wrong_reference_tail, oracle
    )
    assert "FLD-0001" in closure["reference_field_order_closure"]["invalid_ids"]

    mutated_validator = copy.deepcopy(registry)
    mutated_validator["discriminator_branches_by_id"][
        "T10-G18-DD-018-BR3-0449"
    ]["predicate"] = {"mode": "ANY"}
    closure = module.global_structural_closure_details(mutated_validator, oracle)
    assert closure["validator_only_branch_projection_closure"]

    synchronized_wrong_operator = copy.deepcopy(registry)
    branch = synchronized_wrong_operator["discriminator_branches_by_id"][
        "T10-G18-DD-002-BR3-0007"
    ]
    branch["predicate"]["terms"][0]["operator"] = "NOT_EQUALS"
    rule_id = branch["consumer_rule_ids"][0]
    synchronized_wrong_operator["compiled_rules_by_id"][rule_id]["payload"][
        "record_discriminator"
    ] = copy.deepcopy(branch["predicate"])
    details = module.decision_join_details(
        synchronized_wrong_operator, oracle, "T10-G18-DD-002"
    )
    assert details["closed_reference_branch_tag_semantic_mismatch"]

    downgraded_domain = copy.deepcopy(registry)
    downgraded_domain["discriminator_branches_by_id"][
        "T10-G18-DD-002-BR3-0007"
    ]["payload"]["branch_domain"] = "FAKE"
    details = module.decision_join_details(
        downgraded_domain, oracle, "T10-G18-DD-002"
    )
    assert details["branch_domain_semantic_mismatch"]

    self_consistent_fake_template = copy.deepcopy(registry)
    template = self_consistent_fake_template["schema_templates_by_id"]["TPL-0001"]
    template["payload"]["record_type"] = "FAKE"
    template["payload"]["template_key"] = "OWNER:FAKE"
    template["semantic_key"] = "0|OWNER:FAKE|ANY|FAKE"
    closure = module.global_structural_closure_details(
        self_consistent_fake_template, oracle
    )
    assert closure["frozen_v2_canonical_registry_projection_mismatch"]
    assert "TPL-0001" in closure["template_semantic_key_closure"][
        "owner_projection_invalid_ids"
    ]

    self_consistent_fake_reference = copy.deepcopy(registry)
    field = self_consistent_fake_reference["reference_fields_by_id"]["FLD-0001"]
    field["payload"]["containing_record"] = "FAKE"
    field["payload"]["field_path"] = "FAKE.argument_labels[*]"
    closure = module.global_structural_closure_details(
        self_consistent_fake_reference, oracle
    )
    assert closure["frozen_v2_canonical_registry_projection_mismatch"]
    assert "FLD-0001" in closure["reference_field_order_closure"]["invalid_ids"]

    missing_source_row = copy.deepcopy(registry)
    missing_source_row["compiled_rules_by_id"]["PCR-0010"]["payload"][
        "source_row_key"
    ] = None
    closure = module.global_structural_closure_details(missing_source_row, oracle)
    assert "PCR-0010" in closure["manifest_source_row_mismatch"]

    for surface_mutation in (
        lambda value: value["decisions_by_id"]["T10-G18-DD-002"].__setitem__(
            "ordinal", 999
        ),
        lambda value: value["coverage_rows_by_id"]["ROW-0001"].__setitem__(
            "ordinal", 999
        ),
        lambda value: value.__setitem__("invariants", []),
        lambda value: value.__setitem__("evidence_refs", []),
    ):
        changed_surface = copy.deepcopy(registry)
        surface_mutation(changed_surface)
        closure = module.global_structural_closure_details(changed_surface, oracle)
        assert closure["frozen_v2_canonical_registry_projection_mismatch"]


@pytest.mark.parametrize(
    ("decision_id", "missing"),
    [
        ("T10-G18-DD-006", {"runtime_values"}),
        ("T10-G18-DD-007", {"outcome_contracts", "semantic_models"}),
    ],
)
def test_owner_tuple_gate_is_unique_closed_set(
    decision_id: str, missing: set[str]
) -> None:
    module = load_auditor()
    registry = load_json(REGISTRY)
    oracle = load_json(ORACLE)

    details = module.reference_owner_tuple_details(registry, oracle, decision_id)
    assert set(details["declared_vs_oracle"]["missing"]) == missing

    corrected = copy.deepcopy(registry)
    corrected["decisions_by_id"][decision_id]["payload"]["reference_contract"][
        "owner_tuple"
    ] = copy.deepcopy(oracle["checks_by_decision"][decision_id]["owner_tuple"])
    assert module.reference_owner_tuple_details(corrected, oracle, decision_id) == {}

    corrected["decisions_by_id"][decision_id]["payload"]["reference_contract"][
        "owner_tuple"
    ].append(corrected["decisions_by_id"][decision_id]["payload"][
        "reference_contract"
    ]["owner_tuple"][0])
    details = module.reference_owner_tuple_details(corrected, oracle, decision_id)
    assert details["duplicate_declared_owner_tuple_items"]


def test_dd001_freezes_exact_paths_rows_and_effect_counts() -> None:
    module = load_auditor()
    registry = load_json(REGISTRY)
    oracle = load_json(ORACLE)
    baseline = module.dd001_collision_details(registry, oracle)
    assert set(baseline) == {"wording_mismatch"}

    candidate = copy.deepcopy(registry)
    payload = candidate["decisions_by_id"]["T10-G18-DD-001"]["payload"]
    exact = payload["exact_chosen_wire_or_matrix"]
    old_path = payload["affected_owner_paths"][0]
    payload["affected_owner_paths"][0] = "fake_owner.fake_path"
    exact["exact_retyped_paths"][
        exact["exact_retyped_paths"].index(old_path)
    ] = "fake_owner.fake_path"
    row = next(
        row
        for row in exact["coverage_compilation_manifest"]
        if f"{row['owner_table']}.{row['inventory_field_path']}" == old_path
    )
    row["owner_table"] = "fake_owner"
    row["inventory_field_path"] = "fake_path"
    row["row_key"] = "05:002:fake_owner:fake_path"
    details = module.dd001_collision_details(candidate, oracle)
    assert details["affected_path_set_mismatch"]
    assert details["exact_retyped_path_set_mismatch"]
    assert details["census_row_key_mismatch"]

    wrong_effect = copy.deepcopy(registry)
    wrong_effect["decisions_by_id"]["T10-G18-DD-001"]["payload"][
        "expected_rl_universe_effect"
    ]["new_owner_tables"] = 999
    details = module.dd001_collision_details(wrong_effect, oracle)
    assert details["effect_contract_mismatch"]["observed"]["new_owner_tables"] == 999


def test_dd004_reports_exact_schema_rule_count_and_stale_template_layers() -> None:
    module = load_auditor()
    details = module.dd004_collision_details(load_json(REGISTRY), load_json(ORACLE))

    assert details["exact_role_owner"]
    assert details["schema_fields"] == ["$ref_kind", "role", "target_label"]
    assert details["compiled_role_owner"] == {}
    assert details["count_views"]["observed"]["compiled_rules"] == 5
    assert details["stale_schema_template_ids"] == ["TPL-0008"]
    assert details["full_rule_contract"]

    module = load_auditor()
    registry = load_json(REGISTRY)
    oracle = load_json(ORACLE)
    expected = oracle["checks_by_decision"]["T10-G18-DD-004"]
    decision = registry["decisions_by_id"]["T10-G18-DD-004"]
    decision["compiled_rule_ids"] = decision["compiled_rule_ids"][:4]
    for rule_id, (role, target) in zip(
        decision["compiled_rule_ids"], expected["role_owner"].items(), strict=True
    ):
        payload = registry["compiled_rules_by_id"][rule_id]["payload"]
        payload["allowed_target_tables"] = [target]
        payload["cardinality"] = "SCALAR"
        payload["containing_record"] = "CapturedEnvironmentRef"
        payload["field_path"] = expected["field_path"]
        payload["kind"] = "AUTH_REQUIRES"
        set_owner_discriminator(payload, "capture_kind", role)
    assert module._dd004_rule_contract_details(registry, expected) == {}

    registry["compiled_rules_by_id"][decision["compiled_rule_ids"][0]]["payload"][
        "record_discriminator"
    ]["terms"].append(
        {
            "literal": {"type": "ENUM", "value": "EXTRA"},
            "operator": "EQUALS",
            "selector": {"namespace": "OWNER_RECORD", "path": ["extra"]},
        }
    )
    assert module._dd004_rule_contract_details(registry, expected)


@pytest.mark.parametrize(
    "record",
    [
        "CallbackClosureBinding",
        "CallbackDefaultBinding",
        "CallbackKeywordDefaultBinding",
    ],
)
def test_dd009_checks_each_value_consumer_independently(record: str) -> None:
    module = load_auditor()
    registry = load_json(REGISTRY)
    oracle = load_json(ORACLE)
    expected = oracle["checks_by_decision"]["T10-G18-DD-009"]
    expected_map = expected["value_role_owner"]
    field_path = expected["value_record_field_paths"][record]
    rules = [
        rule
        for rule in registry["compiled_rules_by_id"].values()
        if rule["payload"]["decision_id"] == "T10-G18-DD-009"
        and rule["payload"]["containing_record"] == record
    ]
    assert len(rules) == 5
    for rule, role in zip(rules, expected_map, strict=True):
        payload = rule["payload"]
        payload["allowed_target_tables"] = [expected_map[role]]
        payload["field_path"] = field_path
        set_owner_discriminator(payload, "binding_kind", role)

    compiled, malformed, duplicates = module._compiled_role_map(
        registry,
        "T10-G18-DD-009",
        containing_record=record,
        field_path=field_path,
        namespace="OWNER_RECORD",
        selector_path=("binding_kind",),
    )
    assert compiled == expected_map
    assert malformed == []
    assert duplicates == []

    set_owner_discriminator(rules[0]["payload"], "binding_kind", list(expected_map)[1])
    _, _, duplicates = module._compiled_role_map(
        registry,
        "T10-G18-DD-009",
        containing_record=record,
        field_path=field_path,
        namespace="OWNER_RECORD",
        selector_path=("binding_kind",),
    )
    assert duplicates == [list(expected_map)[1]]


def test_dd009_freezes_embedded_wires_presence_transfer_and_all_rule_groups() -> None:
    module = load_auditor()
    registry = load_json(REGISTRY)
    oracle = load_json(ORACLE)

    baseline = module.dd009_collision_details(registry, oracle)
    assert baseline["compiled_presence_template_contract"]
    compiled_presence = copy.deepcopy(registry)
    expected_presence = oracle["checks_by_decision"]["T10-G18-DD-009"][
        "compiled_presence_template_contract"
    ]
    template_payload = compiled_presence["schema_templates_by_id"]["TPL-0105"][
        "payload"
    ]
    for key in ("presence_contract", "source_kind_field", "source_kind_universe"):
        template_payload[key] = copy.deepcopy(expected_presence[key])
    details = module.dd009_collision_details(compiled_presence, oracle)
    assert "compiled_presence_template_contract" not in details

    wrong_wire = copy.deepcopy(registry)
    owner = next(
        value
        for value in wrong_wire["owners_by_id"].values()
        if value["owner_table"] == "generated_stdlib_callbacks"
    )
    row = next(
        row
        for row in owner["payload"]["field_ordinals"]
        if row["record_type"] == "CallbackLoadBinding"
        and row["field_name"] == "literal_value"
    )
    row["wire_type"] = "S"
    details = module.dd009_collision_details(wrong_wire, oracle)
    assert details["embedded_record_wires"]["CallbackLoadBinding"][
        "literal_value"
    ] == "S"

    wrong_direction = copy.deepcopy(registry)
    wrong_direction["decisions_by_id"]["T10-G18-DD-009"]["payload"][
        "exact_chosen_wire_or_matrix"
    ]["transfer_direction"][0]["kind"] = "VALIDATES"
    wrong_direction["compiled_rules_by_id"]["PCR-0530"]["payload"][
        "kind"
    ] = "VALIDATES"
    details = module.dd009_collision_details(wrong_direction, oracle)
    assert details["exact_transfer_direction"]
    assert details["compiled_transfer_rule_contracts"]

    wrong_non_matrix = copy.deepcopy(registry)
    wrong_non_matrix["compiled_rules_by_id"]["PCR-0101"]["payload"][
        "allowed_target_tables"
    ] = ["runtime_values"]
    details = module.dd009_collision_details(wrong_non_matrix, oracle)
    assert details["non_matrix_rule_contracts"][0]["target"] == "runtime_values"

    corrected_one_record = copy.deepcopy(registry)
    expected = oracle["checks_by_decision"]["T10-G18-DD-009"]
    role_map = expected["value_role_owner"]
    rules = [
        rule
        for rule in corrected_one_record["compiled_rules_by_id"].values()
        if rule["payload"]["decision_id"] == "T10-G18-DD-009"
        and rule["payload"]["containing_record"] == "CallbackDefaultBinding"
    ]
    for rule, (role, target) in zip(rules, role_map.items(), strict=True):
        payload = rule["payload"]
        payload["allowed_target_tables"] = [target]
        payload["cardinality"] = "SCALAR"
        payload["field_path"] = "positional_defaults[*].target_label"
        payload["kind"] = "AUTH_REQUIRES"
        set_owner_discriminator(payload, "binding_kind", role)
    contracts = module._dd009_matrix_rule_contract_details(
        corrected_one_record, expected
    )
    assert "CallbackDefaultBinding" not in contracts

    rules[0]["payload"]["cardinality"] = "UNORDERED_SET"
    rules[0]["payload"]["kind"] = "VALIDATES"
    rules[0]["payload"]["record_discriminator"]["terms"].append(
        {
            "literal": {"type": "ENUM", "value": "EXTRA"},
            "operator": "EQUALS",
            "selector": {"namespace": "OWNER_RECORD", "path": ["extra"]},
        }
    )
    contracts = module._dd009_matrix_rule_contract_details(
        corrected_one_record, expected
    )
    assert contracts["CallbackDefaultBinding"]


@pytest.mark.parametrize("decision_id", ["T10-G18-DD-011", "T10-G18-DD-016"])
def test_provider_gate_uses_exact_operation_matrices_and_global_universe(
    decision_id: str,
) -> None:
    module = load_auditor()
    registry = load_json(REGISTRY)
    oracle = load_json(ORACLE)
    baseline = module.provider_reference_details(registry, oracle, decision_id)
    assert set(baseline) == {"exact_provider_role_owner"}

    irrelevant = copy.deepcopy(registry)
    irrelevant["decisions_by_id"][decision_id]["payload"][
        "exact_chosen_wire_or_matrix"
    ]["irrelevant_string_array"] = ["GENERATED_FIELD_ACCESSOR"]
    assert module.provider_reference_details(irrelevant, oracle, decision_id) == baseline

    exact_matrix_mutation = copy.deepcopy(registry)
    exact_matrix_mutation["decisions_by_id"]["T10-G18-DD-011"]["payload"][
        "exact_chosen_wire_or_matrix"
    ]["operation_exact_role_matrix"]["protocol"]["ARRAY_COERCE"].remove(
        "PROJECT_DESCRIPTOR"
    )
    details = module.provider_reference_details(
        exact_matrix_mutation, oracle, decision_id
    )
    if decision_id == "T10-G18-DD-011":
        assert details["exact_operation_exact_role_matrix_sha256"]
    assert details["compiled_operation_role_matrix"]

    compiled_matrix_mutation = copy.deepcopy(registry)
    rule = next(
        rule
        for rule in compiled_matrix_mutation["compiled_rules_by_id"].values()
        if rule["payload"]["decision_id"] == "T10-G18-DD-011"
        and rule["payload"]["owner_table"] == "protocol_capabilities"
        and module._enum_term(rule["payload"], "OWNER_RECORD", ("operation",))
        == "ARRAY_COERCE"
        and module._enum_term(
            rule["payload"],
            "REFERENCE_RECORD",
            ("ProviderReference", "role"),
        )
        == "PROJECT_DESCRIPTOR"
    )
    replace_enum_term(
        rule["payload"],
        "REFERENCE_RECORD",
        ["ProviderReference", "role"],
        "EXTERNAL_TYPE_MEMBER",
    )
    rule["payload"]["allowed_target_tables"] = ["external_type_members"]
    details = module.provider_reference_details(
        compiled_matrix_mutation, oracle, decision_id
    )
    assert details["compiled_operation_role_matrix"]

    full_contract_mutation = copy.deepcopy(registry)
    full_rule = full_contract_mutation["compiled_rules_by_id"][rule["rule_id"]]
    full_rule["payload"]["cardinality"] = "SCALAR"
    full_rule["payload"]["kind"] = "VALIDATES"
    full_rule["payload"]["record_discriminator"]["terms"].append(
        {
            "literal": {"type": "ENUM", "value": "EXTRA"},
            "operator": "EQUALS",
            "selector": {"namespace": "OWNER_RECORD", "path": ["extra"]},
        }
    )
    details = module.provider_reference_details(
        full_contract_mutation, oracle, decision_id
    )
    assert details["compiled_operation_rule_contract_digest_set_sha256"]

    global_mutation = copy.deepcopy(registry)
    dd002_rule = global_mutation["compiled_rules_by_id"]["PCR-0029"]
    replace_enum_term(
        dd002_rule["payload"],
        "REFERENCE_RECORD",
        ["ProviderReference", "role"],
        "GENERATED_FIELD_ACCESSOR",
    )
    dd002_rule["payload"]["allowed_target_tables"] = [
        "generated_field_accessors"
    ]
    details = module.provider_reference_details(global_mutation, oracle, decision_id)
    assert details["compiled_provider_role_owner"]["GENERATED_FIELD_ACCESSOR"] == (
        "generated_field_accessors"
    )

    branch_mutation = copy.deepcopy(registry)
    branch_mutation["discriminator_branches_by_id"][
        "T10-G18-DD-018-BR3-0449"
    ]["predicate"] = {
        "mode": "ALL_EQUAL",
        "terms": [
            {
                "literal": {"type": "ENUM", "value": "FAKE_PROVIDER_ROLE"},
                "operator": "EQUALS",
                "selector": {
                    "namespace": "REFERENCE_RECORD",
                    "path": ["ProviderReference", "role"],
                },
            }
        ],
    }
    details = module.provider_reference_details(branch_mutation, oracle, decision_id)
    assert details["unexpected_provider_branch_roles"] == ["FAKE_PROVIDER_ROLE"]


def test_oracle_scope_and_provenance_mutations_fail_closed() -> None:
    module = load_auditor()
    oracle = load_json(ORACLE)
    oracle["machine_semantic_scope"]["checked_decision_ids"].pop()
    with pytest.raises(ValueError, match="ORACLE_CHECK_SCOPE_MISMATCH"):
        audit_candidate(module, load_json(REGISTRY), oracle)

    oracle = load_json(ORACLE)
    oracle["source_bindings"]["predecessor_authority"] = {
        "path": "FAKE",
        "sha256": "0" * 64,
    }
    with pytest.raises(ValueError, match="ORACLE_SOURCE_BINDING_MISMATCH"):
        audit_candidate(module, load_json(REGISTRY), oracle)

    oracle = load_json(ORACLE)
    oracle["cli_exit_contract"]["findings_hold"] = 0
    with pytest.raises(ValueError, match="ORACLE_CLI_EXIT_CONTRACT_MISMATCH"):
        audit_candidate(module, load_json(REGISTRY), oracle)

    schema = load_json(ORACLE_SCHEMA)
    oracle = load_json(ORACLE)
    oracle["checks_by_decision"]["T10-G18-DD-009"] = {}
    with pytest.raises(ValueError, match="ORACLE_SCHEMA_REQUIRED_MISSING"):
        module._validate_oracle_schema_instance(schema, oracle)

    oracle = load_json(ORACLE)
    for check in oracle["checks_by_decision"].values():
        for key in check:
            check[key] = None
    with pytest.raises(ValueError, match="ORACLE_SCHEMA_TYPE_MISMATCH"):
        module._validate_oracle_schema_instance(schema, oracle)

    oracle = load_json(ORACLE)
    dd009 = oracle["checks_by_decision"]["T10-G18-DD-009"]
    removed = next(iter(dd009))
    dd009["fake_same_count_key"] = dd009.pop(removed)
    with pytest.raises(ValueError, match="ORACLE_SCHEMA_REQUIRED_MISSING"):
        module._validate_oracle_schema_instance(schema, oracle)

    oracle = load_json(ORACLE)
    oracle["adjudication_provenance"]["decision_source_pointers"][
        "T10-G18-DD-009"
    ]["registry_json_pointers"] = ["/FAKE"]
    with pytest.raises(ValueError, match="ORACLE_SOURCE_POINTER_DIGEST_MISMATCH"):
        audit_candidate(module, load_json(REGISTRY), oracle)

    oracle = load_json(ORACLE)
    oracle["adjudication_provenance"]["decision_source_pointers"][
        "T10-G18-DD-009"
    ]["correction_spec_line_range"] = "L999-L999"
    with pytest.raises(ValueError, match="ORACLE_SOURCE_POINTER_DIGEST_MISMATCH"):
        audit_candidate(module, load_json(REGISTRY), oracle)

    oracle = load_json(ORACLE)
    oracle["adjudication_provenance"]["fake_approval"] = True
    with pytest.raises(ValueError, match="ORACLE_SCHEMA_ADDITIONAL_PROPERTY"):
        module._validate_oracle_schema_instance(schema, oracle)


def test_bound_sources_are_single_buffer_reads_without_schema_reopen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = load_auditor()
    original = module._read_bound_regular_bytes
    reads: list[str] = []

    def observe(path, expected_sha256, label, *, expected_path):
        reads.append(label)
        return original(
            path,
            expected_sha256,
            label,
            expected_path=expected_path,
        )

    monkeypatch.setattr(module, "_read_bound_regular_bytes", observe)
    report = audit_candidate(module, load_json(REGISTRY))

    assert report["identity_mode"] == "UNBOUND_PARSED_OBJECT_DIAGNOSTIC_ONLY"
    assert reads == [
        "BOUND_SOURCE_correction_specification",
        "BOUND_SOURCE_oracle_schema",
        "BOUND_SOURCE_predecessor_authority",
        "BOUND_SOURCE_review_registry_v2",
    ]


def test_cli_is_frozen_only_and_distinguishes_findings_usage_and_error() -> None:
    findings = subprocess.run(
        [sys.executable, str(AUDITOR), str(REGISTRY)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    usage = subprocess.run(
        [sys.executable, str(AUDITOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    error = subprocess.run(
        [sys.executable, str(AUDITOR), str(REGISTRY.with_name("missing.json"))],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    stdin_spoof = subprocess.run(
        [sys.executable, str(AUDITOR), "/dev/stdin"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        input=REGISTRY.read_text("utf-8"),
        text=True,
    )

    assert findings.returncode == 1
    assert json.loads(findings.stdout)["identity_mode"] == "FROZEN_EXACT_BYTES"
    assert usage.returncode == 2
    assert "usage:" in usage.stderr
    assert error.returncode == 3
    assert json.loads(error.stdout)["status"] == "AUDIT_ERROR"
    assert stdin_spoof.returncode == 3
    assert "REGISTRY_PATH_MISMATCH" in json.loads(stdin_spoof.stdout)["error"]


def test_auditor_is_independent_of_migrator_and_current_validator() -> None:
    source = AUDITOR.read_bytes().decode("utf-8")
    assert "migrate_authority_decision_registry_v1_to_v2" not in source
    assert "validate_authority_review_package_v2" not in source
    assert "importlib" not in source
    assert ".read_text(" not in source
