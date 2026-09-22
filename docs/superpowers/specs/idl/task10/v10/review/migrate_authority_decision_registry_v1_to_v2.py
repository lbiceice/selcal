"""Deterministic Task 10 review-registry v1 to v2 migration.

This module is representation-only.  It does not amend authority, create IDL,
or authorize KAT construction.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from copy import deepcopy
from hashlib import sha256
from pathlib import Path, PurePosixPath
from typing import NoReturn

V1_REGISTRY_SHA256 = "047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398"
V1_MATRIX_SHA256 = "8b75baf1db9425daddcfd150f0f3c4638684e42e15fa717c2c2044fb3a8f3287"
V1_REGISTRY_PATH = (
    "docs/superpowers/specs/idl/task10/v10/review/" "authority-design-decision-registry-v1.json"
)
REGISTRY_SCHEMA_RELATIVE_PATH = (
    "docs/superpowers/specs/idl/task10/v10/review/schema/"
    "authority-design-decision-registry-v2.schema.json"
)


def _reject_non_finite(value: str) -> NoReturn:
    raise ValueError(f"NON_FINITE_JSON_NUMBER:{value}")


def canonical_json_bytes(value: object) -> bytes:
    """Return stable, diffable UTF-8 JSON with a single trailing LF."""

    text = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    )
    return (text + "\n").encode("utf-8")


def parse_canonical_json(data: bytes) -> object:
    """Parse JSON only when its bytes already use the canonical encoding."""

    value = json.loads(data.decode("utf-8"), parse_constant=_reject_non_finite)
    if canonical_json_bytes(value) != data:
        raise ValueError("NON_CANONICAL_JSON_BYTES")
    return value


def parse_v1_bytes(data: bytes) -> dict[str, object]:
    """Parse legacy compact JSON without requiring the frozen baseline hash."""

    value = json.loads(data.decode("utf-8"), parse_constant=_reject_non_finite)
    if not isinstance(value, dict):
        raise ValueError("V1_ROOT_NOT_OBJECT")
    return value


def _content_id(prefix: str, value: object) -> str:
    return f"{prefix}-{sha256(canonical_json_bytes(value)).hexdigest()}"


def source_binding_id(path: str, digest: str) -> str:
    """Bind a logical repository path and content digest to one stable ID."""

    normalized_path = PurePosixPath(path).as_posix()
    return _content_id("SRC", {"logical_source": normalized_path, "sha256": digest})


def evidence_binding_key(locator: object, claim_role: str) -> str:
    return _content_id("EBK", {"claim_role": claim_role, "locator": locator})


def _iter_legacy_evidence(value: object) -> Iterator[dict[str, object]]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"evidence_refs", "authority_evidence"} and isinstance(child, dict):
                yield child
            else:
                yield from _iter_legacy_evidence(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_legacy_evidence(child)


def _legacy_evidence_records(
    legacy: dict[str, object], authority_binding: str, decision_binding: str
) -> list[dict[str, object]]:
    lines = legacy.get("authority_lines")
    sections = legacy.get("authority_sections")
    decision_id = legacy.get("new_design_decision")
    extras = {
        key: deepcopy(value)
        for key, value in legacy.items()
        if key not in {"authority_lines", "authority_sections", "new_design_decision"}
    }
    records: list[dict[str, object]] = []

    if isinstance(lines, list) and lines:
        authority_record: dict[str, object] = {
            "claim_role": "AUTHORITY_FACT",
            "locator": {
                "kind": "LINE_RANGE",
                "ranges": deepcopy(lines),
                "sections": deepcopy(sections) if isinstance(sections, list) else [],
            },
            "source_binding_id": authority_binding,
        }
        if extras:
            authority_record["rehydration"] = {"legacy_extra_fields": extras}
        records.append(authority_record)

    if isinstance(decision_id, str):
        decision_record: dict[str, object] = {
            "claim_role": "DESIGN_DECISION",
            "locator": {"kind": "DECISION_ONLY", "decision_id": decision_id},
            "source_binding_id": decision_binding,
        }
        if isinstance(lines, list) and not lines:
            decision_record["rehydration"] = {
                "legacy_authority_lines_empty": True,
                "legacy_authority_sections": (
                    deepcopy(sections) if isinstance(sections, list) else []
                ),
                "legacy_extra_fields": extras,
            }
        records.append(decision_record)

    if not records:
        raise ValueError("LEGACY_EVIDENCE_HAS_NO_LOCATOR")
    return records


def normalize_evidence_bindings(v1: dict[str, object]) -> dict[str, object]:
    """Intern legacy evidence as source-bound line and decision references."""

    raw_bindings = v1.get("input_bindings")
    if not isinstance(raw_bindings, list):
        raise ValueError("V1_INPUT_BINDINGS_MISSING")

    source_bindings_by_id: dict[str, dict[str, str]] = {}
    for binding in [
        *raw_bindings,
        {"path": V1_REGISTRY_PATH, "sha256": V1_REGISTRY_SHA256},
    ]:
        if not isinstance(binding, dict):
            raise ValueError("V1_SOURCE_BINDING_NOT_OBJECT")
        path = binding.get("path")
        digest = binding.get("sha256")
        if not isinstance(path, str) or not isinstance(digest, str):
            raise ValueError("V1_SOURCE_BINDING_INVALID")
        identifier = source_binding_id(path, digest)
        source_bindings_by_id[identifier] = {
            "logical_source": PurePosixPath(path).as_posix(),
            "sha256": digest,
        }

    authority_binding = next(
        identifier
        for identifier, binding in source_bindings_by_id.items()
        if binding["logical_source"].endswith(
            "2026-08-29-task10-deny-by-default-provider-proof-design.md"
        )
    )
    decision_binding = source_binding_id(V1_REGISTRY_PATH, V1_REGISTRY_SHA256)

    evidence_refs_by_id: dict[str, dict[str, object]] = {}
    expected_sources: dict[str, str] = {}

    def add_evidence(record: dict[str, object]) -> None:
        identifier = _content_id("EV", record)
        evidence_refs_by_id[identifier] = record
        locator = record["locator"]
        claim_role = record["claim_role"]
        source_id = record["source_binding_id"]
        key = evidence_binding_key(locator, claim_role)
        prior = expected_sources.setdefault(key, source_id)
        if prior != source_id:
            raise ValueError("EVIDENCE_BINDING_MAP_CONFLICT")

    for legacy in _iter_legacy_evidence(v1):
        for record in _legacy_evidence_records(legacy, authority_binding, decision_binding):
            add_evidence(record)

    normalized: dict[str, object] = {
        "source_bindings_by_id": dict(sorted(source_bindings_by_id.items())),
        "evidence_refs_by_id": dict(sorted(evidence_refs_by_id.items())),
        "legacy_locator_claim_to_source_binding": dict(sorted(expected_sources.items())),
    }
    validate_evidence_bindings(normalized)
    return normalized


def validate_evidence_bindings(normalized: dict[str, object]) -> None:
    sources = normalized.get("source_bindings_by_id")
    evidence_refs = normalized.get("evidence_refs_by_id")
    expected = normalized.get("legacy_locator_claim_to_source_binding")
    if not isinstance(sources, dict) or not isinstance(evidence_refs, dict):
        raise ValueError("EVIDENCE_BINDING_SHAPE_INVALID")
    if not isinstance(expected, dict):
        raise ValueError("EVIDENCE_BINDING_MAP_MISSING")
    for identifier, binding in sources.items():
        if not isinstance(binding, dict):
            raise ValueError("SOURCE_BINDING_NOT_OBJECT")
        if identifier != source_binding_id(
            str(binding.get("logical_source")), str(binding.get("sha256"))
        ):
            raise ValueError("SOURCE_BINDING_ID_MISMATCH")
    for evidence in evidence_refs.values():
        if not isinstance(evidence, dict):
            raise ValueError("EVIDENCE_REF_NOT_OBJECT")
        source_id = evidence.get("source_binding_id")
        if source_id not in sources:
            raise ValueError("EVIDENCE_SOURCE_MISSING")
        locator = evidence.get("locator")
        claim_role = evidence.get("claim_role")
        if not isinstance(locator, dict) or not isinstance(claim_role, str):
            raise ValueError("EVIDENCE_REF_SHAPE_INVALID")
        key = evidence_binding_key(locator, claim_role)
        if expected.get(key) != source_id:
            raise ValueError("EVIDENCE_WRONG_VALID_SOURCE")


def _evidence_ids_for_legacy(legacy: dict[str, object], normalized: dict[str, object]) -> list[str]:
    sources = normalized["source_bindings_by_id"]
    authority_binding = next(
        identifier
        for identifier, binding in sources.items()
        if binding["logical_source"].endswith(
            "2026-08-29-task10-deny-by-default-provider-proof-design.md"
        )
    )
    decision_binding = source_binding_id(V1_REGISTRY_PATH, V1_REGISTRY_SHA256)
    return [
        _content_id("EV", record)
        for record in _legacy_evidence_records(legacy, authority_binding, decision_binding)
    ]


def _normalize_nested_evidence(value: object, normalized: dict[str, object]) -> object:
    if isinstance(value, dict):
        result: dict[str, object] = {}
        for key, child in value.items():
            if key in {"evidence_refs", "authority_evidence"} and isinstance(child, dict):
                normalized_key = (
                    "evidence_ref_ids" if key == "evidence_refs" else "authority_evidence_ref_ids"
                )
                result[normalized_key] = _evidence_ids_for_legacy(child, normalized)
            else:
                result[key] = _normalize_nested_evidence(child, normalized)
        return result
    if isinstance(value, list):
        return [_normalize_nested_evidence(child, normalized) for child in value]
    return deepcopy(value)


def _collect_legacy_evidence_ids(value: object, normalized: dict[str, object]) -> list[str]:
    identifiers: set[str] = set()
    for legacy in _iter_legacy_evidence(value):
        identifiers.update(_evidence_ids_for_legacy(legacy, normalized))
    return sorted(identifiers)


def _schema_ordering(v1: dict[str, object]) -> dict[str, object]:
    decision = next(item for item in v1["decisions"] if item["decision_id"] == "T10-G18-DD-020")
    return decision["exact_chosen_wire_or_matrix"]["schema_ordering"]


def _declarative_invariants() -> dict[str, dict[str, object]]:
    records: list[tuple[str, str, dict[str, object]]] = [
        ("COUNT_EQUALS", "Owner count remains 66.", {"collection": "owners_by_id", "expected": 66}),
        (
            "COUNT_EQUALS",
            "Decision count remains 23.",
            {"collection": "decisions_by_id", "expected": 23},
        ),
        (
            "COUNT_EQUALS",
            "Coverage-row count remains 264.",
            {"collection": "coverage_rows_by_id", "expected": 264},
        ),
        (
            "COUNT_EQUALS",
            "Compiled-rule count remains 570.",
            {"collection": "compiled_rules_by_id", "expected": 570},
        ),
        (
            "COUNT_EQUALS",
            "Reference-field count remains 312.",
            {"collection": "reference_fields_by_id", "expected": 312},
        ),
        (
            "COUNT_EQUALS",
            "Schema-template count remains 209.",
            {"collection": "schema_templates_by_id", "expected": 209},
        ),
        (
            "COUNT_EQUALS",
            "Discriminator-branch count remains 461.",
            {"collection": "discriminator_branches_by_id", "expected": 461},
        ),
        (
            "PARTITION_COUNTS",
            "Rule provenance is the exact 509 plus 9 plus 52 partition.",
            {
                "collection": "compiled_rules_by_id",
                "value_path": ["provenance", "class"],
                "expected": {
                    "COVERAGE_DERIVED": 509,
                    "POST_SCHEMA_EXTRA": 9,
                    "AUTHORITY_CLOSED_INVENTORY": 52,
                },
            },
        ),
        (
            "SUM_EQUALS",
            "Rule-provenance partition sums to 570.",
            {"partition_invariant_id": "INV-0008", "expected": 570},
        ),
        (
            "FOREIGN_KEY",
            "Decision rule references resolve.",
            {
                "source_collection": "decisions_by_id",
                "source_path": ["compiled_rule_ids"],
                "target_collection": "compiled_rules_by_id",
            },
        ),
        (
            "FOREIGN_KEY",
            "Coverage rule references resolve.",
            {
                "source_collection": "coverage_rows_by_id",
                "source_path": ["compiled_rule_ids"],
                "target_collection": "compiled_rules_by_id",
            },
        ),
        (
            "FOREIGN_KEY",
            "Branch consumer rule references resolve.",
            {
                "source_collection": "discriminator_branches_by_id",
                "source_path": ["consumer_rule_ids"],
                "target_collection": "compiled_rules_by_id",
            },
        ),
        (
            "FOREIGN_KEY",
            "Evidence source references resolve.",
            {
                "source_collection": "evidence_refs_by_id",
                "source_path": ["source_binding_id"],
                "target_collection": "source_bindings_by_id",
            },
        ),
        (
            "UNIQUE_KEY",
            "Template semantic keys are unique.",
            {"collection": "schema_templates_by_id", "value_paths": [["semantic_key"]]},
        ),
        (
            "UNIQUE_KEY",
            "Reference-field order keys are unique.",
            {"collection": "reference_fields_by_id", "value_paths": [["order_key"]]},
        ),
        (
            "UNIQUE_KEY",
            "Compiled rule bodies are not duplicated under different IDs.",
            {
                "collection": "compiled_rules_by_id",
                "value_paths": [["provenance"], ["evidence_ref_ids"], ["payload"]],
            },
        ),
        (
            "ALL_MATCH",
            "STOP and no-promotion states remain exact.",
            {
                "checks": [
                    {"path": ["artifact_state"], "equals": "REVIEW_DECISION_INPUT_NOT_AUTHORITY"},
                    {
                        "path": ["authority_amendment_status"],
                        "equals": "AUTHORITY_AMENDMENT_NOT_YET_REVIEWED",
                    },
                    {
                        "path": ["machine_stop_decision"],
                        "equals": "STOP_BEFORE_AUTHORITY_IDL_AND_KATS",
                    },
                    {"path": ["scope_boundary", "authority_idl_allowed"], "equals": False},
                    {"path": ["scope_boundary", "kats_allowed"], "equals": False},
                ]
            },
        ),
        (
            "SOURCE_DIGEST_MATCH",
            "Every source binding resolves to its exact repository bytes.",
            {"collection": "source_bindings_by_id"},
        ),
        (
            "CANONICAL_ORDER",
            "Rule ordinals are the contiguous range zero through 569.",
            {"collection": "compiled_rules_by_id", "ordinal_path": ["ordinal"], "start": 0},
        ),
        (
            "CANONICAL_ORDER",
            "Decision ordinals are the contiguous range zero through 22.",
            {"collection": "decisions_by_id", "ordinal_path": ["ordinal"], "start": 0},
        ),
        (
            "CANONICAL_ORDER",
            "Coverage ordinals are the contiguous range zero through 263.",
            {"collection": "coverage_rows_by_id", "ordinal_path": ["ordinal"], "start": 0},
        ),
        (
            "SET_EQUALS",
            "Rule IDs are exactly PCR-0001 through PCR-0570.",
            {
                "collection": "compiled_rules_by_id",
                "prefix": "PCR-",
                "start": 1,
                "end": 570,
                "width": 4,
            },
        ),
        (
            "EXACT_PARTITION",
            "Coverage-derived rules equal the union of row rule references.",
            {
                "member_collection": "coverage_rows_by_id",
                "member_path": ["compiled_rule_ids"],
                "partition_collection": "compiled_rules_by_id",
                "partition_path": ["provenance", "class"],
                "partition_value": "COVERAGE_DERIVED",
            },
        ),
    ]
    return {
        f"INV-{index:04d}": {
            "invariant_id": f"INV-{index:04d}",
            "kind": kind,
            "description": description,
            "assertion": assertion,
        }
        for index, (kind, description, assertion) in enumerate(records, start=1)
    }


def migrate_v1(v1: dict[str, object], *, registry_schema_sha256: str) -> dict[str, object]:
    """Return the normalized representation without reading or writing files."""

    normalized_evidence = normalize_evidence_bindings(v1)
    ordering = _schema_ordering(v1)

    coverage_rows = v1["null_row_coverage"]["coverage_rows"]
    coverage_rule_ids = {rule["rule_id"] for row in coverage_rows for rule in row["compiled_rules"]}
    post_schema_rule_ids: set[str] = set()
    for decision in v1["decisions"]:
        manifests = decision["exact_chosen_wire_or_matrix"].get(
            "post_schema_extra_compilation_manifest", []
        )
        for manifest in manifests:
            post_schema_rule_ids.add(manifest["rule_id"])

    legacy_rules: dict[str, dict[str, object]] = {}
    for decision in v1["decisions"]:
        for rule in decision["compilation_rules"]:
            identifier = rule["rule_id"]
            prior = legacy_rules.setdefault(identifier, rule)
            if prior != rule:
                raise ValueError(f"RULE_BODY_CONFLICT:{identifier}")

    compiled_rules_by_id: dict[str, dict[str, object]] = {}
    for ordinal, identifier in enumerate(sorted(legacy_rules), start=0):
        legacy = deepcopy(legacy_rules[identifier])
        evidence = legacy.pop("evidence_refs")
        legacy.pop("rule_id")
        if identifier in coverage_rule_ids:
            provenance = "COVERAGE_DERIVED"
        elif identifier in post_schema_rule_ids:
            provenance = "POST_SCHEMA_EXTRA"
        else:
            provenance = "AUTHORITY_CLOSED_INVENTORY"
        compiled_rules_by_id[identifier] = {
            "rule_id": identifier,
            "ordinal": ordinal,
            "provenance": {"class": provenance},
            "evidence_ref_ids": _evidence_ids_for_legacy(evidence, normalized_evidence),
            "payload": _normalize_nested_evidence(legacy, normalized_evidence),
        }

    owners_by_id: dict[str, dict[str, object]] = {}
    schema_templates_by_id: dict[str, dict[str, object]] = {}
    template_sequence = 1
    for owner_schema in sorted(ordering["owner_schemas"], key=lambda item: item["owner_ordinal"]):
        owner_ordinal = owner_schema["owner_ordinal"]
        owner_id = f"OWN-{owner_ordinal:04d}"
        owner_payload = deepcopy(owner_schema)
        owner_payload.pop("owner_ordinal")
        owner_payload.pop("owner_table")
        owners_by_id[owner_id] = {
            "owner_id": owner_id,
            "ordinal": owner_ordinal,
            "owner_table": owner_schema["owner_table"],
            "payload": owner_payload,
        }
        for template in sorted(
            owner_schema["template_ordinals"],
            key=lambda item: item["template_ordinal"],
        ):
            template_id = f"TPL-{template_sequence:04d}"
            template_sequence += 1
            semantic_key = "|".join(
                [
                    str(owner_ordinal),
                    template["template_key"],
                    template["branch_tag_value"],
                    template["record_type"],
                ]
            )
            schema_templates_by_id[template_id] = {
                "template_id": template_id,
                "semantic_key": semantic_key,
                "payload": {"owner_id": owner_id, **deepcopy(template)},
            }

    reference_fields_by_id: dict[str, dict[str, object]] = {}
    ordered_fields = sorted(
        ordering["reference_field_ordinals"],
        key=lambda item: (
            item["owner_ordinal"],
            item["template_ordinal"],
            item["field_ordinal"],
            item["containing_record"],
            item["field_path"],
        ),
    )
    for sequence, field in enumerate(ordered_fields, start=1):
        field_id = f"FLD-{sequence:04d}"
        reference_fields_by_id[field_id] = {
            "field_id": field_id,
            "order_key": [
                field["owner_ordinal"],
                field["template_ordinal"],
                field["field_ordinal"],
                0,
            ],
            "payload": deepcopy(field),
        }

    branch_records = next(
        item for item in v1["decisions"] if item["decision_id"] == "T10-G18-DD-018"
    )["exact_chosen_wire_or_matrix"]["branch_instances"]
    branch_ordinals = {
        item["branch_instance_id"]: item["branch_ordinal"] for item in ordering["branch_ordinals"]
    }
    discriminator_branches_by_id: dict[str, dict[str, object]] = {}
    for legacy in sorted(
        branch_records, key=lambda item: branch_ordinals[item["branch_instance_id"]]
    ):
        branch_id = legacy["branch_instance_id"]
        payload = deepcopy(legacy)
        payload.pop("branch_instance_id")
        predicate = payload.pop("predicate")
        consumers = payload.pop("consumer_rule_ids")
        payload["branch_ordinal"] = branch_ordinals[branch_id]
        discriminator_branches_by_id[branch_id] = {
            "branch_id": branch_id,
            "predicate": predicate,
            "consumer_rule_ids": consumers,
            "payload": payload,
        }

    decisions_by_id: dict[str, dict[str, object]] = {}
    for ordinal, decision in enumerate(v1["decisions"]):
        decision_id = decision["decision_id"]
        payload = deepcopy(decision)
        payload.pop("decision_id")
        payload.pop("compilation_rules")
        legacy_discriminator_ids = payload.pop("discriminator_branch_instance_ids")
        payload["legacy_discriminator_branch_instance_ids"] = deepcopy(legacy_discriminator_ids)
        reference_contract = payload.pop("reference_kind_nullability_owner_tuple")
        reference_kind = reference_contract.pop("reference_kind")
        reference_kinds = (
            deepcopy(reference_kind) if isinstance(reference_kind, list) else [reference_kind]
        )
        payload["reference_contract"] = reference_contract
        payload["legacy_reference_kind_encoding"] = (
            "ARRAY" if isinstance(reference_kind, list) else "SCALAR"
        )
        exact = payload["exact_chosen_wire_or_matrix"]
        branch_instances = exact.pop("branch_instances", None)
        branch_ids = (
            [item["branch_instance_id"] for item in branch_instances]
            if isinstance(branch_instances, list)
            and branch_instances
            and all(isinstance(item, dict) for item in branch_instances)
            else deepcopy(legacy_discriminator_ids)
        )
        case_labels = (
            deepcopy(branch_instances)
            if isinstance(branch_instances, list)
            and all(isinstance(item, str) for item in branch_instances)
            else []
        )
        decision_without_rules = deepcopy(decision)
        decision_without_rules.pop("compilation_rules")
        decisions_by_id[decision_id] = {
            "decision_id": decision_id,
            "ordinal": ordinal,
            "reference_kinds": reference_kinds,
            "compiled_rule_ids": [rule["rule_id"] for rule in decision["compilation_rules"]],
            "evidence_ref_ids": _collect_legacy_evidence_ids(
                decision_without_rules, normalized_evidence
            ),
            "design_payload": {
                "branch_instance_ids": branch_ids,
                "case_labels": case_labels,
            },
            "payload": _normalize_nested_evidence(payload, normalized_evidence),
        }

    coverage_rows_by_id: dict[str, dict[str, object]] = {}
    for ordinal, row in enumerate(coverage_rows):
        row_id = f"ROW-{ordinal + 1:04d}"
        payload = deepcopy(row)
        payload.pop("compiled_rules")
        compiled_rule_ids = payload.pop("compiled_rule_ids")
        evidence = payload.pop("authority_evidence")
        coverage_rows_by_id[row_id] = {
            "coverage_row_id": row_id,
            "ordinal": ordinal,
            "compiled_rule_ids": compiled_rule_ids,
            "evidence_ref_ids": _evidence_ids_for_legacy(evidence, normalized_evidence),
            "payload": _normalize_nested_evidence(payload, normalized_evidence),
        }

    legacy_aliases_by_id: dict[str, dict[str, object]] = {}
    for sequence, alias in enumerate(v1["legacy_aliases"], start=1):
        alias_id = f"ALS-{sequence:04d}"
        payload = deepcopy(alias)
        decision_id = payload.pop("decision_id")
        legacy_aliases_by_id[alias_id] = {
            "alias_id": alias_id,
            "decision_id": decision_id,
            "payload": payload,
        }

    null_summary = deepcopy(v1["null_row_coverage"])
    null_summary.pop("coverage_rows")
    legacy_review_gate = deepcopy(v1["review_gate"])
    predecessor_review_state = legacy_review_gate.pop("independent_review_result")
    legacy_review_gate["predecessor_review_state"] = predecessor_review_state
    original_input_ids = [
        source_binding_id(binding["path"], binding["sha256"]) for binding in v1["input_bindings"]
    ]

    invariants_by_id = _declarative_invariants()

    return {
        "format": "selcal.task10.g18.authority-design-decision-registry.v2",
        "artifact_state": v1["artifact_status"],
        "authority_amendment_status": v1["authority_amendment_status"],
        "machine_stop_decision": v1["machine_stop_decision"],
        "scope_boundary": {
            "authority_idl_allowed": v1["review_gate"]["authority_idl_allowed"],
            "kats_allowed": v1["review_gate"]["kats_allowed"],
        },
        "schema_binding": {
            "path": REGISTRY_SCHEMA_RELATIVE_PATH,
            "sha256": registry_schema_sha256,
        },
        "source_bindings_by_id": normalized_evidence["source_bindings_by_id"],
        "evidence_refs_by_id": normalized_evidence["evidence_refs_by_id"],
        "evidence_binding_expectations_by_key": normalized_evidence[
            "legacy_locator_claim_to_source_binding"
        ],
        "owners_by_id": owners_by_id,
        "schema_templates_by_id": schema_templates_by_id,
        "reference_fields_by_id": reference_fields_by_id,
        "discriminator_branches_by_id": discriminator_branches_by_id,
        "decisions_by_id": decisions_by_id,
        "coverage_rows_by_id": coverage_rows_by_id,
        "compiled_rules_by_id": compiled_rules_by_id,
        "legacy_aliases_by_id": legacy_aliases_by_id,
        "invariants_by_id": invariants_by_id,
        "legacy_rehydration": {
            "predecessor_format": v1["schema"],
            "design_status_rule": v1["design_status_rule"],
            "input_binding_ids": original_input_ids,
            "null_row_summary": null_summary,
            "machine_verifiable_invariants": deepcopy(v1["machine_verifiable_invariants"]),
            "review_gate": legacy_review_gate,
            "scope_boundary": deepcopy(v1["scope_boundary"]),
        },
    }


def _expanded_evidence_projection(
    evidence_by_id: dict[str, object], sources_by_id: dict[str, object]
) -> list[dict[str, object]]:
    projection: list[dict[str, object]] = []
    for identifier in sorted(evidence_by_id):
        evidence = deepcopy(evidence_by_id[identifier])
        source_id = evidence.pop("source_binding_id")
        projection.append(
            {
                "evidence_ref_id": identifier,
                **evidence,
                "source": deepcopy(sources_by_id[source_id]),
            }
        )
    return projection


def rule_projection_from_v1(v1: dict[str, object]) -> dict[str, object]:
    """Compute normalized complete-rule semantics directly from v1."""

    normalized = normalize_evidence_bindings(v1)
    result: dict[str, object] = {}
    for decision in v1["decisions"]:
        for raw_rule in decision["compilation_rules"]:
            rule = deepcopy(raw_rule)
            identifier = rule.pop("rule_id")
            evidence = rule.pop("evidence_refs")
            record = {
                "rule_id": identifier,
                "payload": _normalize_nested_evidence(rule, normalized),
                "evidence": _expanded_evidence_projection(
                    {
                        evidence_id: normalized["evidence_refs_by_id"][evidence_id]
                        for evidence_id in _evidence_ids_for_legacy(evidence, normalized)
                    },
                    normalized["source_bindings_by_id"],
                ),
            }
            prior = result.setdefault(identifier, record)
            if prior != record:
                raise ValueError(f"RULE_PROJECTION_CONFLICT:{identifier}")
    return dict(sorted(result.items()))


def rule_projection_from_v2(v2: dict[str, object]) -> dict[str, object]:
    """Compute normalized complete-rule semantics directly from v2."""

    result: dict[str, object] = {}
    for identifier, rule in v2["compiled_rules_by_id"].items():
        result[identifier] = {
            "rule_id": identifier,
            "payload": deepcopy(rule["payload"]),
            "evidence": _expanded_evidence_projection(
                {
                    evidence_id: v2["evidence_refs_by_id"][evidence_id]
                    for evidence_id in rule["evidence_ref_ids"]
                },
                v2["source_bindings_by_id"],
            ),
        }
    return dict(sorted(result.items()))


def semantic_projection_from_v1(v1: dict[str, object]) -> dict[str, object]:
    """Compute the review semantics from predecessor structures only."""

    normalized = normalize_evidence_bindings(v1)
    ordering = _schema_ordering(v1)

    owners: list[dict[str, object]] = []
    templates: list[dict[str, object]] = []
    template_sequence = 1
    for owner_schema in sorted(ordering["owner_schemas"], key=lambda item: item["owner_ordinal"]):
        owner_ordinal = owner_schema["owner_ordinal"]
        owner_id = f"OWN-{owner_ordinal:04d}"
        owner_payload = deepcopy(owner_schema)
        owner_payload.pop("owner_ordinal")
        owner_payload.pop("owner_table")
        owners.append(
            {
                "owner_id": owner_id,
                "ordinal": owner_ordinal,
                "owner_table": owner_schema["owner_table"],
                "payload": owner_payload,
            }
        )
        for template in sorted(
            owner_schema["template_ordinals"],
            key=lambda item: item["template_ordinal"],
        ):
            template_id = f"TPL-{template_sequence:04d}"
            template_sequence += 1
            templates.append(
                {
                    "template_id": template_id,
                    "semantic_key": "|".join(
                        [
                            str(owner_ordinal),
                            template["template_key"],
                            template["branch_tag_value"],
                            template["record_type"],
                        ]
                    ),
                    "payload": {"owner_id": owner_id, **deepcopy(template)},
                }
            )

    fields: list[dict[str, object]] = []
    ordered_fields = sorted(
        ordering["reference_field_ordinals"],
        key=lambda item: (
            item["owner_ordinal"],
            item["template_ordinal"],
            item["field_ordinal"],
            item["containing_record"],
            item["field_path"],
        ),
    )
    for sequence, field in enumerate(ordered_fields, start=1):
        fields.append(
            {
                "field_id": f"FLD-{sequence:04d}",
                "order_key": [
                    field["owner_ordinal"],
                    field["template_ordinal"],
                    field["field_ordinal"],
                    0,
                ],
                "payload": deepcopy(field),
            }
        )

    branch_ordinals = {
        item["branch_instance_id"]: item["branch_ordinal"] for item in ordering["branch_ordinals"]
    }
    branch_source = next(
        decision for decision in v1["decisions"] if decision["decision_id"] == "T10-G18-DD-018"
    )["exact_chosen_wire_or_matrix"]["branch_instances"]
    branches: list[dict[str, object]] = []
    for raw_branch in sorted(
        branch_source,
        key=lambda item: branch_ordinals[item["branch_instance_id"]],
    ):
        branch = deepcopy(raw_branch)
        branch_id = branch.pop("branch_instance_id")
        predicate = branch.pop("predicate")
        consumers = branch.pop("consumer_rule_ids")
        branch["branch_ordinal"] = branch_ordinals[branch_id]
        branches.append(
            {
                "branch_id": branch_id,
                "predicate": predicate,
                "consumer_rule_ids": consumers,
                "payload": branch,
            }
        )

    decisions: list[dict[str, object]] = []
    for ordinal, raw_decision in enumerate(v1["decisions"]):
        decision = deepcopy(raw_decision)
        decision_id = decision.pop("decision_id")
        compiled_rule_ids = [rule["rule_id"] for rule in decision.pop("compilation_rules")]
        legacy_discriminator_ids = decision.pop("discriminator_branch_instance_ids")
        decision["legacy_discriminator_branch_instance_ids"] = deepcopy(legacy_discriminator_ids)
        contract = decision.pop("reference_kind_nullability_owner_tuple")
        reference_kind = contract.pop("reference_kind")
        reference_kinds = (
            deepcopy(reference_kind) if isinstance(reference_kind, list) else [reference_kind]
        )
        decision["reference_contract"] = contract
        decision["legacy_reference_kind_encoding"] = (
            "ARRAY" if isinstance(reference_kind, list) else "SCALAR"
        )
        branch_instances = decision["exact_chosen_wire_or_matrix"].pop("branch_instances", None)
        branch_ids = (
            [item["branch_instance_id"] for item in branch_instances]
            if isinstance(branch_instances, list)
            and branch_instances
            and all(isinstance(item, dict) for item in branch_instances)
            else deepcopy(legacy_discriminator_ids)
        )
        case_labels = (
            deepcopy(branch_instances)
            if isinstance(branch_instances, list)
            and all(isinstance(item, str) for item in branch_instances)
            else []
        )
        decisions.append(
            {
                "decision_id": decision_id,
                "ordinal": ordinal,
                "reference_kinds": reference_kinds,
                "compiled_rule_ids": compiled_rule_ids,
                "design_payload": {
                    "branch_instance_ids": branch_ids,
                    "case_labels": case_labels,
                },
                "payload": _normalize_nested_evidence(decision, normalized),
            }
        )

    coverage: list[dict[str, object]] = []
    for ordinal, raw_row in enumerate(v1["null_row_coverage"]["coverage_rows"]):
        row = deepcopy(raw_row)
        row.pop("compiled_rules")
        compiled_rule_ids = row.pop("compiled_rule_ids")
        row.pop("authority_evidence")
        coverage.append(
            {
                "coverage_row_id": f"ROW-{ordinal + 1:04d}",
                "ordinal": ordinal,
                "compiled_rule_ids": compiled_rule_ids,
                "payload": _normalize_nested_evidence(row, normalized),
            }
        )

    aliases = []
    for sequence, raw_alias in enumerate(v1["legacy_aliases"], start=1):
        alias = deepcopy(raw_alias)
        decision_id = alias.pop("decision_id")
        aliases.append(
            {
                "alias_id": f"ALS-{sequence:04d}",
                "decision_id": decision_id,
                "payload": alias,
            }
        )

    return {
        "states": {
            "artifact_state": v1["artifact_status"],
            "authority_amendment_status": v1["authority_amendment_status"],
            "machine_stop_decision": v1["machine_stop_decision"],
            "authority_idl_allowed": v1["review_gate"]["authority_idl_allowed"],
            "kats_allowed": v1["review_gate"]["kats_allowed"],
        },
        "owners": owners,
        "templates": templates,
        "fields": fields,
        "branches": branches,
        "decisions": decisions,
        "coverage": coverage,
        "rules": rule_projection_from_v1(v1),
        "evidence": _expanded_evidence_projection(
            normalized["evidence_refs_by_id"],
            normalized["source_bindings_by_id"],
        ),
        "aliases": aliases,
        "legacy_invariants": deepcopy(v1["machine_verifiable_invariants"]),
    }


def semantic_projection_from_v2(v2: dict[str, object]) -> dict[str, object]:
    """Compute the same review semantics directly from normalized v2 maps."""

    decisions = []
    for decision in sorted(v2["decisions_by_id"].values(), key=lambda item: item["ordinal"]):
        decisions.append(
            {
                key: deepcopy(decision[key])
                for key in (
                    "decision_id",
                    "ordinal",
                    "reference_kinds",
                    "compiled_rule_ids",
                    "design_payload",
                    "payload",
                )
            }
        )
    coverage = []
    for row in sorted(v2["coverage_rows_by_id"].values(), key=lambda item: item["ordinal"]):
        coverage.append(
            {
                key: deepcopy(row[key])
                for key in (
                    "coverage_row_id",
                    "ordinal",
                    "compiled_rule_ids",
                    "payload",
                )
            }
        )
    aliases = [
        deepcopy(v2["legacy_aliases_by_id"][identifier])
        for identifier in sorted(v2["legacy_aliases_by_id"])
    ]
    return {
        "states": {
            "artifact_state": v2["artifact_state"],
            "authority_amendment_status": v2["authority_amendment_status"],
            "machine_stop_decision": v2["machine_stop_decision"],
            "authority_idl_allowed": v2["scope_boundary"]["authority_idl_allowed"],
            "kats_allowed": v2["scope_boundary"]["kats_allowed"],
        },
        "owners": [
            deepcopy(item)
            for item in sorted(v2["owners_by_id"].values(), key=lambda item: item["ordinal"])
        ],
        "templates": [
            deepcopy(v2["schema_templates_by_id"][identifier])
            for identifier in sorted(v2["schema_templates_by_id"])
        ],
        "fields": [
            deepcopy(v2["reference_fields_by_id"][identifier])
            for identifier in sorted(v2["reference_fields_by_id"])
        ],
        "branches": [
            deepcopy(item)
            for item in sorted(
                v2["discriminator_branches_by_id"].values(),
                key=lambda item: item["payload"]["branch_ordinal"],
            )
        ],
        "decisions": decisions,
        "coverage": coverage,
        "rules": rule_projection_from_v2(v2),
        "evidence": _expanded_evidence_projection(
            v2["evidence_refs_by_id"], v2["source_bindings_by_id"]
        ),
        "aliases": aliases,
        "legacy_invariants": deepcopy(v2["legacy_rehydration"]["machine_verifiable_invariants"]),
    }


def _legacy_evidence_from_ids(identifiers: list[str], v2: dict[str, object]) -> dict[str, object]:
    evidence_by_id = v2["evidence_refs_by_id"]
    restored: dict[str, object] = {
        "authority_lines": [],
        "authority_sections": [],
        "new_design_decision": None,
    }
    saw_authority = False
    for identifier in identifiers:
        record = evidence_by_id[identifier]
        locator = record["locator"]
        if record["claim_role"] == "AUTHORITY_FACT":
            if locator["kind"] != "LINE_RANGE":
                raise ValueError("AUTHORITY_EVIDENCE_LOCATOR_INVALID")
            restored["authority_lines"] = deepcopy(locator["ranges"])
            restored["authority_sections"] = deepcopy(locator["sections"])
            saw_authority = True
        elif record["claim_role"] == "DESIGN_DECISION":
            if locator["kind"] != "DECISION_ONLY":
                raise ValueError("DECISION_EVIDENCE_LOCATOR_INVALID")
            restored["new_design_decision"] = locator["decision_id"]
        else:
            raise ValueError("LEGACY_EVIDENCE_CLAIM_ROLE_UNSUPPORTED")

        rehydration = record.get("rehydration", {})
        if not isinstance(rehydration, dict):
            raise ValueError("EVIDENCE_REHYDRATION_INVALID")
        extras = rehydration.get("legacy_extra_fields", {})
        if not isinstance(extras, dict):
            raise ValueError("EVIDENCE_REHYDRATION_EXTRAS_INVALID")
        restored.update(deepcopy(extras))
        if rehydration.get("legacy_authority_lines_empty") is True:
            restored["authority_lines"] = []
            restored["authority_sections"] = deepcopy(
                rehydration.get("legacy_authority_sections", [])
            )
            saw_authority = True
    if not saw_authority:
        raise ValueError("LEGACY_EVIDENCE_AUTHORITY_SHAPE_MISSING")
    return restored


def _rehydrate_nested_evidence(value: object, v2: dict[str, object]) -> object:
    if isinstance(value, dict):
        result: dict[str, object] = {}
        for key, child in value.items():
            if key == "evidence_ref_ids" and isinstance(child, list):
                result["evidence_refs"] = _legacy_evidence_from_ids(child, v2)
            elif key == "authority_evidence_ref_ids" and isinstance(child, list):
                result["authority_evidence"] = _legacy_evidence_from_ids(child, v2)
            else:
                result[key] = _rehydrate_nested_evidence(child, v2)
        return result
    if isinstance(value, list):
        return [_rehydrate_nested_evidence(child, v2) for child in value]
    return deepcopy(value)


def rehydrate_legacy_v1(v2: dict[str, object]) -> dict[str, object]:
    """Rebuild v1 solely from the supplied normalized v2 object."""

    legacy_rules: dict[str, dict[str, object]] = {}
    for identifier, normalized_rule in v2["compiled_rules_by_id"].items():
        rule = _rehydrate_nested_evidence(normalized_rule["payload"], v2)
        rule["rule_id"] = identifier
        rule["evidence_refs"] = _legacy_evidence_from_ids(normalized_rule["evidence_ref_ids"], v2)
        legacy_rules[identifier] = rule

    branch_by_id: dict[str, dict[str, object]] = {}
    for identifier, normalized_branch in v2["discriminator_branches_by_id"].items():
        branch = deepcopy(normalized_branch["payload"])
        branch.pop("branch_ordinal")
        branch["branch_instance_id"] = identifier
        branch["predicate"] = deepcopy(normalized_branch["predicate"])
        branch["consumer_rule_ids"] = deepcopy(normalized_branch["consumer_rule_ids"])
        branch_by_id[identifier] = branch

    decisions: list[dict[str, object]] = []
    normalized_decisions = sorted(v2["decisions_by_id"].values(), key=lambda item: item["ordinal"])
    for normalized_decision in normalized_decisions:
        decision = _rehydrate_nested_evidence(normalized_decision["payload"], v2)
        legacy_discriminator_ids = decision.pop("legacy_discriminator_branch_instance_ids")
        reference_contract = decision.pop("reference_contract")
        encoding = decision.pop("legacy_reference_kind_encoding")
        reference_kinds = deepcopy(normalized_decision["reference_kinds"])
        reference_contract["reference_kind"] = (
            reference_kinds if encoding == "ARRAY" else reference_kinds[0]
        )
        exact = decision["exact_chosen_wire_or_matrix"]
        design = normalized_decision["design_payload"]
        decision_id = normalized_decision["decision_id"]
        if design["case_labels"]:
            exact["branch_instances"] = deepcopy(design["case_labels"])
        elif decision_id == "T10-G18-DD-018":
            exact["branch_instances"] = [
                deepcopy(branch_by_id[identifier]) for identifier in design["branch_instance_ids"]
            ]
        decision["decision_id"] = decision_id
        decision["compilation_rules"] = [
            deepcopy(legacy_rules[identifier])
            for identifier in normalized_decision["compiled_rule_ids"]
        ]
        decision["discriminator_branch_instance_ids"] = deepcopy(legacy_discriminator_ids)
        decision["reference_kind_nullability_owner_tuple"] = reference_contract
        decisions.append(decision)

    coverage_rows: list[dict[str, object]] = []
    normalized_rows = sorted(v2["coverage_rows_by_id"].values(), key=lambda item: item["ordinal"])
    for normalized_row in normalized_rows:
        row = _rehydrate_nested_evidence(normalized_row["payload"], v2)
        row["compiled_rule_ids"] = deepcopy(normalized_row["compiled_rule_ids"])
        row["compiled_rules"] = [
            deepcopy(legacy_rules[identifier]) for identifier in normalized_row["compiled_rule_ids"]
        ]
        row["authority_evidence"] = _legacy_evidence_from_ids(
            normalized_row["evidence_ref_ids"], v2
        )
        coverage_rows.append(row)

    aliases: list[dict[str, object]] = []
    for identifier in sorted(v2["legacy_aliases_by_id"]):
        normalized_alias = v2["legacy_aliases_by_id"][identifier]
        alias = deepcopy(normalized_alias["payload"])
        alias["decision_id"] = normalized_alias["decision_id"]
        aliases.append(alias)

    rehydration = v2["legacy_rehydration"]
    sources = v2["source_bindings_by_id"]
    input_bindings = [
        {
            "path": sources[identifier]["logical_source"],
            "sha256": sources[identifier]["sha256"],
        }
        for identifier in rehydration["input_binding_ids"]
    ]
    null_row_coverage = deepcopy(rehydration["null_row_summary"])
    null_row_coverage["coverage_rows"] = coverage_rows
    review_gate = deepcopy(rehydration["review_gate"])
    predecessor_review_state = review_gate.pop("predecessor_review_state")
    review_gate["independent_review_result"] = predecessor_review_state

    return {
        "artifact_status": v2["artifact_state"],
        "authority_amendment_status": v2["authority_amendment_status"],
        "decisions": decisions,
        "design_status_rule": rehydration["design_status_rule"],
        "input_bindings": input_bindings,
        "legacy_aliases": aliases,
        "machine_stop_decision": v2["machine_stop_decision"],
        "machine_verifiable_invariants": deepcopy(rehydration["machine_verifiable_invariants"]),
        "null_row_coverage": null_row_coverage,
        "review_gate": review_gate,
        "schema": rehydration["predecessor_format"],
        "scope_boundary": deepcopy(rehydration["scope_boundary"]),
    }


def legacy_v1_bytes(v2: dict[str, object]) -> bytes:
    """Serialize a rehydrated v1 object in the predecessor's exact encoding."""

    text = json.dumps(
        rehydrate_legacy_v1(v2),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (text + "\n").encode("utf-8")


def migrate_v1_bytes(
    data: bytes, *, registry_schema_sha256: str | None = None
) -> dict[str, object]:
    if registry_schema_sha256 is None:
        schema_path = (
            Path(__file__).resolve().parent
            / "schema"
            / ("authority-design-decision-registry-v2.schema.json")
        )
        registry_schema_sha256 = sha256(schema_path.read_bytes()).hexdigest()
    return migrate_v1(parse_v1_bytes(data), registry_schema_sha256=registry_schema_sha256)


def verify_hash_bound_baseline(repository_root: Path) -> None:
    review_dir = repository_root / PurePosixPath(V1_REGISTRY_PATH).parent
    manifest = json.loads(
        (review_dir / "authority-review-package-v2-baseline.json").read_text("utf-8")
    )
    for binding in manifest["files"]:
        actual = sha256((repository_root / binding["path"]).read_bytes()).hexdigest()
        if actual != binding["sha256"]:
            raise ValueError(f"BASELINE_HASH_DRIFT:{binding['path']}")


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown_index(v2: dict[str, object], registry_bytes: bytes) -> str:
    """Render a bounded, non-normative review index without JSON mirroring."""

    registry_sha = sha256(registry_bytes).hexdigest()
    schema_binding = v2["schema_binding"]
    lines = [
        "# Task 10 authority design decision index v2",
        "",
        "Status: `NON_NORMATIVE_DERIVED_VIEW`",
        "",
        "This file is a concise navigation surface derived from the canonical v2 ",
        "registry. It is not authority, not an IDL, not a KAT, and not a substitute ",
        "for the normative JSON review input.",
        "",
        "## Exact subject bindings",
        "",
        "| Artifact | Path | SHA-256 |",
        "|---|---|---|",
        "| Registry | `docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-registry-v2.json` | `" + registry_sha + "` |",
        f"| Registry schema | `{schema_binding['path']}` | `{schema_binding['sha256']}` |",
        "",
        "## Boundary",
        "",
        "- Artifact state: `REVIEW_DECISION_INPUT_NOT_AUTHORITY`",
        "- Authority amendment: `AUTHORITY_AMENDMENT_NOT_YET_REVIEWED`",
        "- Machine stop: `STOP_BEFORE_AUTHORITY_IDL_AND_KATS`",
        "- Authority IDL allowed: `false`",
        "- KATs allowed: `false`",
        "",
        "## Counts",
        "",
        "| Surface | Count |",
        "|---|---:|",
        f"| Owners | {len(v2['owners_by_id'])} |",
        f"| Decisions | {len(v2['decisions_by_id'])} |",
        f"| Coverage rows | {len(v2['coverage_rows_by_id'])} |",
        f"| Compiled rules | {len(v2['compiled_rules_by_id'])} |",
        f"| Reference fields | {len(v2['reference_fields_by_id'])} |",
        f"| Schema templates | {len(v2['schema_templates_by_id'])} |",
        f"| Discriminator branches | {len(v2['discriminator_branches_by_id'])} |",
        "",
        "Rule provenance remains `509 COVERAGE_DERIVED + 9 POST_SCHEMA_EXTRA + ",
        "52 AUTHORITY_CLOSED_INVENTORY = 570`.",
        "",
        "## Decision index",
        "",
        "| Decision | Title | Status | Reference kinds | Rules | Branches |",
        "|---|---|---|---|---:|---:|",
    ]
    for decision in sorted(v2["decisions_by_id"].values(), key=lambda item: item["ordinal"]):
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_cell(decision["decision_id"]),
                    _markdown_cell(decision["payload"]["title"]),
                    _markdown_cell(decision["payload"]["status"]),
                    _markdown_cell(", ".join(decision["reference_kinds"])),
                    str(len(decision["compiled_rule_ids"])),
                    str(len(decision["design_payload"]["branch_instance_ids"])),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## v1 to v2 representation changes",
            "",
            "| v1 review surface | v2 representation | Scientific effect |",
            "|---|---|---|",
            "| Repeated rule objects in decisions and coverage rows | One canonical "
            "rule map plus ordered ID references | None |",
            "| Scalar/list reference-kind overload | Arrays only | None |",
            "| String/object branch-instance overload | Typed branch IDs and "
            "case-label arrays | None |",
            "| Unbound authority line strings | Content-addressed source plus "
            "locator references | None |",
            "| Review result inside reviewed bytes | Detached exact-hash attestation | None |",
            "| Full JSON mirror in Markdown | Concise index only | None |",
            "",
            "## Quality finding closure targets",
            "",
            "| Prior finding | v2 control | Current local evidence |",
            "|---|---|---|",
            "| Oversized Markdown mirror | Size and forbidden-dump test | "
            "Implemented, pending independent review |",
            "| 509 repeated rule bodies | Single-definition rule map | Implemented, "
            "pending independent review |",
            "| No enforceable schema | Closed versioned schema and validator | "
            "Implemented, pending independent review |",
            "| Lines not bound to sources | Source IDs bind logical path and "
            "SHA-256 | Implemented, pending independent review |",
            "| Self-invalidating embedded verdict | Detached attestation topology | "
            "Specified, no PASS attestation yet |",
            "| Prose-only invariants | Executable invariant records and mutations | "
            "Implemented, pending independent review |",
            "| Open invariant assertion controls | Kind-discriminated closed assertion "
            "schemas | Implemented, pending independent review |",
            "| Validator-local normalized drift | Independent rule/semantic projections "
            "plus exact deterministic regeneration | Implemented, pending independent review |",
            "| Partial review-byte binding | Ten fixed-role exact-hash package bindings | "
            "Implemented, pending independent review |",
            "| Persisted attestation verification gap | Separate PREWRITE and exact-byte "
            "READBACK modes | Implemented, pending independent review |",
            "",
            "## Detached review location",
            "",
            "After these registry bytes are frozen, reviewer verdicts are recorded under ",
            f"`attestations/sha256-{registry_sha}/review-<attestation-id>.json`. ",
            "A detached attestation does not promote this package to authority and must ",
            "not alter the registry or schema bytes.",
            "",
            "## Stop warning",
            "",
            "`STOP_BEFORE_AUTHORITY_IDL_AND_KATS` remains binding. No authority prose, ",
            "authority IDL, KAT, production implementation, UI, release, or manuscript ",
            "work is authorized by this index.",
            "",
        ]
    )
    return "\n".join(lines)


def write_v2_index(repository_root: Path, registry_path: Path) -> Path:
    registry_bytes = registry_path.read_bytes()
    v2 = parse_canonical_json(registry_bytes)
    if not isinstance(v2, dict):
        raise ValueError("V2_ROOT_NOT_OBJECT")
    output = registry_path.with_name("authority-design-decision-index-v2.md")
    output.write_text(render_markdown_index(v2, registry_bytes), encoding="utf-8")
    return output


def write_v2_registry(repository_root: Path) -> Path:
    verify_hash_bound_baseline(repository_root)
    review_dir = repository_root / PurePosixPath(V1_REGISTRY_PATH).parent
    v1_path = review_dir / "authority-design-decision-registry-v1.json"
    if sha256(v1_path.read_bytes()).hexdigest() != V1_REGISTRY_SHA256:
        raise ValueError("V1_REGISTRY_HASH_DRIFT")
    schema_path = repository_root / REGISTRY_SCHEMA_RELATIVE_PATH
    v2 = migrate_v1_bytes(
        v1_path.read_bytes(),
        registry_schema_sha256=sha256(schema_path.read_bytes()).hexdigest(),
    )
    output = review_dir / "authority-design-decision-registry-v2.json"
    output.write_bytes(canonical_json_bytes(v2))
    return output


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[7]
    destination = write_v2_registry(repository)
    write_v2_index(repository, destination)
    print(destination)
