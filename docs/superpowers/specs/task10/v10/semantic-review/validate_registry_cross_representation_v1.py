#!/usr/bin/env python3
"""Read-only cross-representation audit for the frozen Task 10 v2 registry.

The instrument performs structural joins for all 23 decisions, but adjudicated
semantic checks for only the seven decisions named by a separately frozen oracle.
It is not an authority, a v3 builder, or a global semantic-pass instrument.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from hashlib import sha256
from pathlib import Path
from typing import Any

EXPECTED_FORMAT = "selcal.task10.g18.authority-design-decision-registry.v2"
EXPECTED_ORACLE_FORMAT = (
    "selcal.task10.g18.cross-representation-semantic-oracle.v1"
)
EXPECTED_REGISTRY_SHA256 = (
    "77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5"
)
EXPECTED_ORACLE_SHA256 = (
    "c9db64895c2cb802919b34e24f78551aabf2bee1530ac562515f428614fb2118"
)
EXPECTED_PREDECESSOR_SHA256 = (
    "74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff"
)
EXPECTED_CORRECTION_SPEC_SHA256 = (
    "85ababe68595f31f3df037a09d954b050fa718ecbc922bcd2bcf4b4838b20735"
)
EXPECTED_ORACLE_SCHEMA_SHA256 = (
    "94b316ee6036a9d912248c4acf1d031cca5570770023007da15e0ad4b7086066"
)
EXPECTED_DECISION_SOURCE_POINTERS_SHA256 = (
    "edbf9c354fdba1ddb1c9e5eb686990ef67925b1bae920afd947293225430767b"
)
EXPECTED_VALIDATOR_ONLY_BRANCH_IDS_SHA256 = (
    "3f333629a02f952f96336daf7b221fd11a49fcc20323226b5180da0a61554221"
)
EXPECTED_VALIDATOR_ONLY_BRANCH_PROJECTION_SHA256 = (
    "ffea529edf3fe20362a3a86a1deea11bae9b787d086c02fd3332a2f973214082"
)
EXPECTED_DECISION_IDS = tuple(
    f"T10-G18-DD-{ordinal:03d}" for ordinal in range(1, 24)
)
DEFAULT_ORACLE = (
    Path(__file__).resolve().parent
    / "adjudicated-cross-representation-oracle-v1.json"
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
EXPECTED_SOURCE_BINDINGS = {
    "correction_specification": {
        "path": (
            "docs/superpowers/plans/"
            "2026-08-31-task10-authority-review-package-v3-correction.md"
        ),
        "sha256": EXPECTED_CORRECTION_SPEC_SHA256,
    },
    "oracle_schema": {
        "path": (
            "docs/superpowers/specs/task10/v10/semantic-review/"
            "adjudicated-cross-representation-oracle-v1.schema.json"
        ),
        "sha256": EXPECTED_ORACLE_SCHEMA_SHA256,
    },
    "predecessor_authority": {
        "path": (
            "docs/superpowers/specs/"
            "2026-08-29-task10-deny-by-default-provider-proof-design.md"
        ),
        "sha256": EXPECTED_PREDECESSOR_SHA256,
    },
    "review_registry_v2": {
        "path": (
            "docs/superpowers/specs/idl/task10/v10/review/"
            "authority-design-decision-registry-v2.json"
        ),
        "sha256": EXPECTED_REGISTRY_SHA256,
    },
}
EXPECTED_GLOBAL_COUNTS = {
    "branches": 461,
    "coverage_rows": 264,
    "decisions": 23,
    "owner_field_rows": 1070,
    "owners": 66,
    "reference_fields": 312,
    "rules": 570,
    "schema_templates": 209,
}
EXPECTED_CLI_EXIT_CONTRACT = {
    "audit_error": 3,
    "findings_hold": 1,
    "usage_error": 2,
}
SEVERITIES = {"BLOCKER", "MAJOR", "MINOR"}


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label}_NOT_OBJECT")
    return value


def _sequence(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label}_NOT_ARRAY")
    return value


def _string_list(value: object, label: str) -> list[str]:
    result = _sequence(value, label)
    if not all(isinstance(item, str) for item in result):
        raise ValueError(f"{label}_NOT_STRING_ARRAY")
    return result


def _decision(registry: Mapping[str, Any], decision_id: str) -> Mapping[str, Any]:
    decisions = _mapping(registry.get("decisions_by_id"), "DECISIONS")
    return _mapping(decisions.get(decision_id), decision_id)


def _payload(registry: Mapping[str, Any], decision_id: str) -> Mapping[str, Any]:
    return _mapping(
        _decision(registry, decision_id).get("payload"),
        f"{decision_id}_PAYLOAD",
    )


def _exact(registry: Mapping[str, Any], decision_id: str) -> Mapping[str, Any]:
    return _mapping(
        _payload(registry, decision_id).get("exact_chosen_wire_or_matrix"),
        f"{decision_id}_EXACT",
    )


def _oracle_check(oracle: Mapping[str, Any], decision_id: str) -> Mapping[str, Any]:
    checks = _mapping(oracle.get("checks_by_decision"), "ORACLE_CHECKS")
    return _mapping(checks.get(decision_id), f"ORACLE_{decision_id}")


def _rule_payload(rule: Mapping[str, Any]) -> Mapping[str, Any]:
    return _mapping(rule.get("payload"), "RULE_PAYLOAD")


def _rules_for_decision(
    registry: Mapping[str, Any], decision_id: str
) -> list[Mapping[str, Any]]:
    decision = _decision(registry, decision_id)
    rule_ids = _string_list(
        decision.get("compiled_rule_ids"), f"{decision_id}_RULE_IDS"
    )
    rules = _mapping(registry.get("compiled_rules_by_id"), "RULES")
    return [_mapping(rules.get(rule_id), rule_id) for rule_id in rule_ids]


def _owner_field_rows(
    registry: Mapping[str, Any], owner_table: str, record_type: str
) -> list[Mapping[str, Any]]:
    owners = _mapping(registry.get("owners_by_id"), "OWNERS")
    owner = next(
        (
            _mapping(candidate, "OWNER")
            for candidate in owners.values()
            if isinstance(candidate, Mapping)
            and candidate.get("owner_table") == owner_table
        ),
        None,
    )
    if owner is None:
        raise ValueError(f"OWNER_NOT_FOUND:{owner_table}")
    rows = _sequence(
        _mapping(owner.get("payload"), "OWNER_PAYLOAD").get("field_ordinals"),
        "FIELD_ORDINALS",
    )
    selected = [
        _mapping(row, "FIELD_ORDINAL")
        for row in rows
        if isinstance(row, Mapping) and row.get("record_type") == record_type
    ]
    return sorted(selected, key=lambda row: int(row["field_ordinal"]))


def _selector_terms(rule_payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    discriminator = _mapping(
        rule_payload.get("record_discriminator"), "DISCRIMINATOR"
    )
    if discriminator.get("mode") == "ANY":
        return []
    if discriminator.get("mode") == "ANY_OF_EQUALITY_BRANCHES":
        terms: list[Mapping[str, Any]] = []
        for branch in _sequence(
            discriminator.get("branches"), "DISCRIMINATOR_BRANCHES"
        ):
            branch_value = _mapping(branch, "DISCRIMINATOR_BRANCH")
            terms.extend(
                _mapping(term, "DISCRIMINATOR_TERM")
                for term in _sequence(
                    branch_value.get("terms"), "DISCRIMINATOR_TERMS"
                )
            )
        return terms
    return [
        _mapping(term, "DISCRIMINATOR_TERM")
        for term in _sequence(
            discriminator.get("terms"), "DISCRIMINATOR_TERMS"
        )
    ]


def _enum_term(
    rule_payload: Mapping[str, Any], namespace: str, path: tuple[str, ...]
) -> str | None:
    values: list[str] = []
    for term in _selector_terms(rule_payload):
        selector = _mapping(term.get("selector"), "SELECTOR")
        literal = _mapping(term.get("literal"), "LITERAL")
        if (
            selector.get("namespace") == namespace
            and selector.get("path") == list(path)
            and literal.get("type") == "ENUM"
            and isinstance(literal.get("value"), str)
        ):
            values.append(literal["value"])
    return values[0] if len(values) == 1 else None


def _single_target(rule_payload: Mapping[str, Any]) -> str | None:
    targets = rule_payload.get("allowed_target_tables")
    if (
        not isinstance(targets, list)
        or len(targets) != 1
        or not isinstance(targets[0], str)
    ):
        return None
    return targets[0]


def _canonical_value_sha256(value: object) -> str:
    data = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(data).hexdigest()


def _canonical_document_sha256(value: object) -> str:
    data = (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    return sha256(data).hexdigest()


def _stat_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_uid,
        value.st_gid,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _read_bound_regular_bytes(
    path: Path,
    expected_sha256: str,
    label: str,
    *,
    expected_path: Path,
) -> tuple[bytes, str]:
    expected_absolute = expected_path.absolute()
    requested_absolute = path.absolute()
    if requested_absolute != expected_absolute:
        raise ValueError(f"{label}_PATH_MISMATCH:{requested_absolute}")
    try:
        relative_parts = requested_absolute.relative_to(REPOSITORY_ROOT).parts
    except ValueError as error:
        raise ValueError(f"{label}_OUTSIDE_REPOSITORY") from error
    current = REPOSITORY_ROOT
    for part in relative_parts:
        current = current / part
        component = os.lstat(current)
        if stat.S_ISLNK(component.st_mode):
            raise ValueError(f"{label}_SYMLINK_COMPONENT:{current}")
    before_path = os.lstat(requested_absolute)
    if not stat.S_ISREG(before_path.st_mode):
        raise ValueError(f"{label}_NOT_REGULAR_FILE")
    if stat.S_IMODE(before_path.st_mode) != 0o644:
        raise ValueError(f"{label}_MODE_MISMATCH")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(requested_absolute, flags)
    try:
        before_fd = os.fstat(descriptor)
        if _stat_identity(before_fd) != _stat_identity(before_path):
            raise ValueError(f"{label}_OPEN_IDENTITY_MISMATCH")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after_fd = os.fstat(descriptor)
        if _stat_identity(after_fd) != _stat_identity(before_fd):
            raise ValueError(f"{label}_CHANGED_DURING_READ")
        data = b"".join(chunks)
    finally:
        os.close(descriptor)
    after_path = os.lstat(requested_absolute)
    if _stat_identity(after_path) != _stat_identity(before_path):
        raise ValueError(f"{label}_PATH_IDENTITY_CHANGED")
    actual = sha256(data).hexdigest()
    if actual != expected_sha256:
        raise ValueError(f"{label}_SHA256_MISMATCH:{actual}")
    return data, actual


def _binding_details(
    oracle: Mapping[str, Any], binding_name: str
) -> Mapping[str, Any]:
    bindings = _mapping(oracle.get("source_bindings"), "ORACLE_BINDINGS")
    return _mapping(bindings.get(binding_name), f"BINDING_{binding_name}")


def _resolve_json_pointer(document: object, pointer: str) -> object:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON_POINTER_INVALID:{pointer}")
    value = document
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(value, Mapping) and part in value:
            value = value[part]
            continue
        if isinstance(value, list) and part.isdigit() and int(part) < len(value):
            value = value[int(part)]
            continue
        raise ValueError(f"JSON_POINTER_UNRESOLVED:{pointer}")
    return value


def _validate_bound_sources(
    oracle: Mapping[str, Any],
) -> dict[str, bytes]:
    verified_bytes: dict[str, bytes] = {}
    for binding_name, expected in EXPECTED_SOURCE_BINDINGS.items():
        observed = _binding_details(oracle, binding_name)
        if observed != expected:
            raise ValueError(f"ORACLE_SOURCE_BINDING_MISMATCH:{binding_name}")
        path = REPOSITORY_ROOT / str(expected["path"])
        data, _ = _read_bound_regular_bytes(
            path,
            str(expected["sha256"]),
            f"BOUND_SOURCE_{binding_name}",
            expected_path=path,
        )
        verified_bytes[binding_name] = data
    return verified_bytes


def _schema_ref(schema: Mapping[str, Any], reference: str) -> Mapping[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"ORACLE_SCHEMA_REF_UNSUPPORTED:{reference}")
    value: object = schema
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, Mapping) or part not in value:
            raise ValueError(f"ORACLE_SCHEMA_REF_MISSING:{reference}")
        value = value[part]
    return _mapping(value, f"ORACLE_SCHEMA_REF_{reference}")


def _schema_type_matches(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, Mapping)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ValueError(f"ORACLE_SCHEMA_TYPE_UNSUPPORTED:{expected}")


def _validate_oracle_schema_instance(
    schema: Mapping[str, Any], instance: object
) -> None:
    """Execute the JSON-Schema subset used by the frozen oracle schema."""

    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("ORACLE_SCHEMA_DIALECT_MISMATCH")

    def check(node: Mapping[str, Any], value: object, path: str) -> None:
        reference = node.get("$ref")
        if reference is not None:
            if not isinstance(reference, str):
                raise ValueError(f"ORACLE_SCHEMA_REF_INVALID:{path}")
            check(_schema_ref(schema, reference), value, path)

        expected_type = node.get("type")
        if expected_type is not None:
            if not isinstance(expected_type, str) or not _schema_type_matches(
                value, expected_type
            ):
                raise ValueError(f"ORACLE_SCHEMA_TYPE_MISMATCH:{path}")
        if "const" in node and (
            type(value) is not type(node["const"]) or value != node["const"]
        ):
            raise ValueError(f"ORACLE_SCHEMA_CONST_MISMATCH:{path}")

        if isinstance(value, Mapping):
            minimum_properties = node.get("minProperties")
            if isinstance(minimum_properties, int) and len(value) < minimum_properties:
                raise ValueError(f"ORACLE_SCHEMA_MIN_PROPERTIES:{path}")
            required = node.get("required", [])
            if not isinstance(required, list):
                raise ValueError(f"ORACLE_SCHEMA_REQUIRED_INVALID:{path}")
            for name in required:
                if name not in value:
                    raise ValueError(f"ORACLE_SCHEMA_REQUIRED_MISSING:{path}/{name}")
            properties = _mapping(node.get("properties", {}), "SCHEMA_PROPERTIES")
            for name, child_schema in properties.items():
                if name in value:
                    check(
                        _mapping(child_schema, f"SCHEMA_PROPERTY_{name}"),
                        value[name],
                        f"{path}/{name}",
                    )
            additional = node.get("additionalProperties", True)
            for name, child in value.items():
                if name in properties:
                    continue
                if additional is False:
                    raise ValueError(
                        f"ORACLE_SCHEMA_ADDITIONAL_PROPERTY:{path}/{name}"
                    )
                if isinstance(additional, Mapping):
                    check(additional, child, f"{path}/{name}")

        if isinstance(value, list):
            minimum_items = node.get("minItems")
            maximum_items = node.get("maxItems")
            if isinstance(minimum_items, int) and len(value) < minimum_items:
                raise ValueError(f"ORACLE_SCHEMA_MIN_ITEMS:{path}")
            if isinstance(maximum_items, int) and len(value) > maximum_items:
                raise ValueError(f"ORACLE_SCHEMA_MAX_ITEMS:{path}")
            if node.get("uniqueItems") is True:
                digests = [_canonical_value_sha256(child) for child in value]
                if len(digests) != len(set(digests)):
                    raise ValueError(f"ORACLE_SCHEMA_UNIQUE_ITEMS:{path}")
            item_schema = node.get("items")
            if item_schema is not None:
                item_mapping = _mapping(item_schema, "SCHEMA_ITEMS")
                for index, child in enumerate(value):
                    check(item_mapping, child, f"{path}/{index}")

        if isinstance(value, str):
            minimum_length = node.get("minLength")
            if isinstance(minimum_length, int) and len(value) < minimum_length:
                raise ValueError(f"ORACLE_SCHEMA_MIN_LENGTH:{path}")
            pattern = node.get("pattern")
            if isinstance(pattern, str) and re.search(pattern, value) is None:
                raise ValueError(f"ORACLE_SCHEMA_PATTERN:{path}")

    check(schema, instance, "$")


def _manifest_rule_ids(exact: Mapping[str, Any]) -> list[str]:
    result: list[str] = []
    for key in (
        "coverage_compilation_manifest",
        "post_schema_extra_compilation_manifest",
    ):
        for row in _sequence(exact.get(key, []), key.upper()):
            manifest_row = _mapping(row, f"{key}_ROW")
            if "compiled_rule_ids" in manifest_row:
                result.extend(
                    _string_list(
                        manifest_row.get("compiled_rule_ids"),
                        f"{key}_RULE_IDS",
                    )
                )
            elif isinstance(manifest_row.get("rule_id"), str):
                result.append(manifest_row["rule_id"])
            else:
                raise ValueError(f"{key}_RULE_IDS_NOT_ARRAY_OR_RULE_ID")
    return result


def _manifest_rows(exact: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    result: list[Mapping[str, Any]] = []
    for key in (
        "coverage_compilation_manifest",
        "post_schema_extra_compilation_manifest",
    ):
        result.extend(
            _mapping(row, f"{key}_ROW")
            for row in _sequence(exact.get(key, []), key.upper())
        )
    return result


def _closed_id_range(prefix: str, count: int, width: int = 4) -> set[str]:
    return {f"{prefix}-{ordinal:0{width}d}" for ordinal in range(1, count + 1)}


def global_structural_closure_details(
    registry: Mapping[str, Any], oracle: Mapping[str, Any]
) -> dict[str, object]:
    """Check frozen-v2 collection, ID, ordinal, and manifest closure."""

    details: dict[str, object] = {}
    observed_registry_projection_sha256 = _canonical_document_sha256(registry)
    if observed_registry_projection_sha256 != EXPECTED_REGISTRY_SHA256:
        details["frozen_v2_canonical_registry_projection_mismatch"] = {
            "expected": EXPECTED_REGISTRY_SHA256,
            "observed": observed_registry_projection_sha256,
        }
    owners = _mapping(registry.get("owners_by_id"), "OWNERS")
    decisions = _mapping(registry.get("decisions_by_id"), "DECISIONS")
    rules = _mapping(registry.get("compiled_rules_by_id"), "RULES")
    branches = _mapping(registry.get("discriminator_branches_by_id"), "BRANCHES")
    coverage = _mapping(registry.get("coverage_rows_by_id"), "COVERAGE")
    templates = _mapping(registry.get("schema_templates_by_id"), "TEMPLATES")
    reference_fields = _mapping(
        registry.get("reference_fields_by_id"), "REFERENCE_FIELDS"
    )
    owner_field_rows = sum(
        len(
            _sequence(
                _mapping(owner, "OWNER").get("payload", {}).get(
                    "field_ordinals"
                ),
                "OWNER_FIELD_ORDINALS",
            )
        )
        for owner in owners.values()
    )
    observed_counts = {
        "branches": len(branches),
        "coverage_rows": len(coverage),
        "decisions": len(decisions),
        "owner_field_rows": owner_field_rows,
        "owners": len(owners),
        "reference_fields": len(reference_fields),
        "rules": len(rules),
        "schema_templates": len(templates),
    }
    closure = _mapping(oracle.get("structural_closure"), "STRUCTURAL_CLOSURE")
    expected_counts = dict(
        _mapping(closure.get("expected_counts"), "STRUCTURAL_COUNTS")
    )
    if expected_counts != EXPECTED_GLOBAL_COUNTS:
        raise ValueError("ORACLE_GLOBAL_COUNTS_MISMATCH")
    if observed_counts != expected_counts:
        details["global_count_mismatch"] = {
            "expected": expected_counts,
            "observed": observed_counts,
        }

    validator_only_branches = {
        str(branch_id): branch
        for branch_id, branch in sorted(branches.items())
        if isinstance(branch, Mapping)
        and isinstance(branch.get("payload"), Mapping)
        and branch["payload"].get("validator_only") is True
    }
    observed_validator_ids_sha256 = _canonical_value_sha256(
        sorted(validator_only_branches)
    )
    observed_validator_projection_sha256 = _canonical_value_sha256(
        validator_only_branches
    )
    if (
        closure.get("validator_only_branch_ids_sha256")
        != EXPECTED_VALIDATOR_ONLY_BRANCH_IDS_SHA256
        or observed_validator_ids_sha256
        != EXPECTED_VALIDATOR_ONLY_BRANCH_IDS_SHA256
        or closure.get("validator_only_branch_projection_sha256")
        != EXPECTED_VALIDATOR_ONLY_BRANCH_PROJECTION_SHA256
        or observed_validator_projection_sha256
        != EXPECTED_VALIDATOR_ONLY_BRANCH_PROJECTION_SHA256
    ):
        details["validator_only_branch_projection_closure"] = {
            "ids_sha256": observed_validator_ids_sha256,
            "projection_sha256": observed_validator_projection_sha256,
        }

    expected_ids = {
        "coverage_rows": _closed_id_range(
            "ROW", expected_counts["coverage_rows"]
        ),
        "owners": {
            f"OWN-{ordinal:04d}"
            for ordinal in range(expected_counts["owners"])
        },
        "reference_fields": _closed_id_range(
            "FLD", expected_counts["reference_fields"]
        ),
        "rules": _closed_id_range("PCR", expected_counts["rules"]),
        "schema_templates": _closed_id_range(
            "TPL", expected_counts["schema_templates"]
        ),
    }
    observed_ids = {
        "coverage_rows": set(coverage),
        "owners": set(owners),
        "reference_fields": set(reference_fields),
        "rules": set(rules),
        "schema_templates": set(templates),
    }
    for collection, expected in expected_ids.items():
        observed = observed_ids[collection]
        if observed != expected:
            details.setdefault("closed_id_range_mismatch", {})[collection] = {
                "extra": sorted(observed - expected),
                "missing": sorted(expected - observed),
            }

    mismatched_identity_fields: dict[str, list[str]] = {}
    for collection_name, collection, field_name in (
        ("branches", branches, "branch_id"),
        ("coverage_rows", coverage, "coverage_row_id"),
        ("owners", owners, "owner_id"),
        ("reference_fields", reference_fields, "field_id"),
        ("rules", rules, "rule_id"),
        ("schema_templates", templates, "template_id"),
    ):
        mismatch = sorted(
            key
            for key, value in collection.items()
            if not isinstance(value, Mapping) or value.get(field_name) != key
        )
        if mismatch:
            mismatched_identity_fields[collection_name] = mismatch
    if mismatched_identity_fields:
        details["identity_field_mismatch"] = mismatched_identity_fields

    rule_ordinals = [
        _mapping(rule, "RULE").get("ordinal") for rule in rules.values()
    ]
    if set(rule_ordinals) != set(range(expected_counts["rules"])) or len(
        rule_ordinals
    ) != len(set(rule_ordinals)):
        details["rule_ordinal_closure"] = sorted(
            ordinal for ordinal in rule_ordinals if isinstance(ordinal, int)
        )
    branch_ordinals = [
        _mapping(_mapping(branch, "BRANCH").get("payload"), "BRANCH_PAYLOAD").get(
            "branch_ordinal"
        )
        for branch in branches.values()
    ]
    if set(branch_ordinals) != set(range(1, expected_counts["branches"] + 1)) or len(
        branch_ordinals
    ) != len(set(branch_ordinals)):
        details["branch_ordinal_closure"] = sorted(
            ordinal for ordinal in branch_ordinals if isinstance(ordinal, int)
        )

    template_ordinals_by_owner: dict[str, list[int]] = defaultdict(list)
    template_semantic_keys: list[str] = []
    owner_ordinals = {
        str(owner_id): _mapping(owner, str(owner_id)).get("ordinal")
        for owner_id, owner in owners.items()
    }
    invalid_template_semantic_ids: list[str] = []
    invalid_template_identity_ids: list[str] = []
    invalid_template_owner_projection_ids: list[str] = []
    template_order_entries: list[tuple[int, int, str]] = []
    for template_id, template in templates.items():
        template_value = _mapping(template, str(template_id))
        payload = _mapping(
            template_value.get("payload"), f"{template_id}_PAYLOAD"
        )
        owner_id_value = payload.get("owner_id")
        owner_id = str(owner_id_value)
        ordinal = payload.get("template_ordinal")
        owner_ordinal = owner_ordinals.get(owner_id)
        if (
            owner_id_value not in owners
            or not isinstance(owner_ordinal, int)
            or isinstance(owner_ordinal, bool)
            or not isinstance(ordinal, int)
            or isinstance(ordinal, bool)
        ):
            invalid_template_identity_ids.append(str(template_id))
        else:
            template_ordinals_by_owner[owner_id].append(ordinal)
            template_order_entries.append((owner_ordinal, ordinal, str(template_id)))
        semantic_key = template_value.get("semantic_key")
        if isinstance(semantic_key, str):
            template_semantic_keys.append(semantic_key)
        expected_semantic_key = "|".join(
            (
                str(owner_ordinals.get(owner_id)),
                str(payload.get("template_key")),
                str(payload.get("branch_tag_value")),
                str(payload.get("record_type")),
            )
        )
        if semantic_key != expected_semantic_key:
            invalid_template_semantic_ids.append(str(template_id))
        owner_value = owners.get(owner_id)
        if isinstance(owner_value, Mapping) and isinstance(ordinal, int):
            owner_rows = [
                row
                for row in _sequence(
                    _mapping(owner_value.get("payload"), "OWNER_PAYLOAD").get(
                        "field_ordinals"
                    ),
                    "OWNER_FIELD_ORDINALS",
                )
                if isinstance(row, Mapping)
                and row.get("template_ordinal") == ordinal
            ]
            owner_projection = {
                (
                    row.get("template_key"),
                    row.get("record_type"),
                    row.get("branch_tag_value"),
                )
                for row in owner_rows
            }
            template_projection = {
                (
                    payload.get("template_key"),
                    payload.get("record_type"),
                    payload.get("branch_tag_value"),
                )
            }
            if owner_rows and owner_projection != template_projection:
                invalid_template_owner_projection_ids.append(str(template_id))
    invalid_template_owners = sorted(
        owner_id
        for owner_id, ordinals in template_ordinals_by_owner.items()
        if set(ordinals) != set(range(len(ordinals)))
        or len(ordinals) != len(set(ordinals))
    )
    if invalid_template_owners:
        details["template_ordinal_closure"] = invalid_template_owners
    expected_template_id_order = sorted(templates)
    observed_template_id_order = [
        template_id for _, _, template_id in sorted(template_order_entries)
    ]
    if (
        invalid_template_identity_ids
        or observed_template_id_order != expected_template_id_order
    ):
        details["template_owner_order_closure"] = {
            "invalid_ids": invalid_template_identity_ids,
            "sorted_ids_match": observed_template_id_order
            == expected_template_id_order,
        }
    if invalid_template_semantic_ids or len(template_semantic_keys) != len(
        set(template_semantic_keys)
    ) or invalid_template_owner_projection_ids:
        details["template_semantic_key_closure"] = {
            "invalid_ids": invalid_template_semantic_ids,
            "owner_projection_invalid_ids": invalid_template_owner_projection_ids,
            "unique_count": len(set(template_semantic_keys)),
        }

    reference_entries: list[tuple[str, tuple[object, ...]]] = []
    invalid_reference_order_ids: list[str] = []
    for field_id, field in reference_fields.items():
        field_value = _mapping(field, str(field_id))
        payload = _mapping(field_value.get("payload"), f"{field_id}_PAYLOAD")
        order_key_value = field_value.get("order_key")
        if (
            not isinstance(order_key_value, list)
            or len(order_key_value) != 4
            or any(
                not isinstance(value, int) or isinstance(value, bool)
                for value in order_key_value
            )
        ):
            invalid_reference_order_ids.append(str(field_id))
            continue
        order_key = tuple(order_key_value)
        reference_entries.append((str(field_id), order_key))
        if order_key != (
            payload.get("owner_ordinal"),
            payload.get("template_ordinal"),
            payload.get("field_ordinal"),
            0,
        ):
            invalid_reference_order_ids.append(str(field_id))
            continue
        matching_owners = [
            owner
            for owner in owners.values()
            if isinstance(owner, Mapping)
            and owner.get("ordinal") == payload.get("owner_ordinal")
            and owner.get("owner_table") == payload.get("owner_table")
        ]
        matching_templates = [
            template
            for template in templates.values()
            if isinstance(template, Mapping)
            and isinstance(template.get("payload"), Mapping)
            and template["payload"].get("owner_id")
            == (matching_owners[0].get("owner_id") if len(matching_owners) == 1 else None)
            and template["payload"].get("template_ordinal")
            == payload.get("template_ordinal")
        ]
        matching_field_rows = []
        if len(matching_owners) == 1:
            path_segments = [
                segment.removesuffix("[*]")
                for segment in str(payload.get("field_path")).split(".")
            ]
            matching_field_rows = [
                row
                for row in _sequence(
                    _mapping(matching_owners[0].get("payload"), "OWNER_PAYLOAD").get(
                        "field_ordinals"
                    ),
                    "OWNER_FIELD_ORDINALS",
                )
                if isinstance(row, Mapping)
                and row.get("template_ordinal") == payload.get("template_ordinal")
                and row.get("field_ordinal") == payload.get("field_ordinal")
                and row.get("field_name") in path_segments
            ]
        if len(matching_owners) != 1 or len(matching_templates) != 1 or len(
            matching_field_rows
        ) != 1:
            invalid_reference_order_ids.append(str(field_id))
            continue
        matching_rule_records = {
            _rule_payload(rule).get("containing_record")
            for rule in rules.values()
            if isinstance(rule, Mapping)
            and _rule_payload(rule).get("owner_table")
            == payload.get("owner_table")
            and _rule_payload(rule).get("field_path") == payload.get("field_path")
        }
        if payload.get("containing_record") not in matching_rule_records:
            invalid_reference_order_ids.append(str(field_id))
    sorted_reference_ids = [
        field_id for field_id, _ in sorted(reference_entries, key=lambda item: item[1])
    ]
    if (
        invalid_reference_order_ids
        or len({order_key for _, order_key in reference_entries})
        != len(reference_entries)
        or sorted_reference_ids != sorted(reference_fields)
    ):
        details["reference_field_order_closure"] = {
            "invalid_ids": invalid_reference_order_ids,
            "sorted_ids_match": sorted_reference_ids == sorted(reference_fields),
            "unique_order_key_count": len(
                {order_key for _, order_key in reference_entries}
            ),
        }

    forward_rule_ids: list[str] = []
    for decision_id, decision in decisions.items():
        ids = _string_list(
            _mapping(decision, str(decision_id)).get("compiled_rule_ids"),
            f"{decision_id}_RULE_IDS",
        )
        forward_rule_ids.extend(ids)
        for rule_id in ids:
            rule = rules.get(rule_id)
            if isinstance(rule, Mapping) and _rule_payload(rule).get(
                "decision_id"
            ) != decision_id:
                details.setdefault("rule_decision_backlink_mismatch", []).append(
                    rule_id
                )
    forward_counts = Counter(forward_rule_ids)
    if set(forward_counts) != set(rules) or any(
        count != 1 for count in forward_counts.values()
    ):
        details["global_rule_forward_closure"] = {
            "missing": sorted(set(rules) - set(forward_counts)),
            "multiplicity": {
                rule_id: count
                for rule_id, count in sorted(forward_counts.items())
                if count != 1
            },
        }

    global_catalog_id = closure.get("global_branch_catalog_decision_id")
    catalog = _mapping(decisions.get(global_catalog_id), "GLOBAL_BRANCH_CATALOG")
    catalog_ids = _string_list(
        _mapping(catalog.get("design_payload"), "GLOBAL_CATALOG_DESIGN").get(
            "branch_instance_ids"
        ),
        "GLOBAL_BRANCH_CATALOG_IDS",
    )
    if set(catalog_ids) != set(branches) or len(catalog_ids) != len(branches):
        details["global_branch_catalog_closure"] = {
            "extra": sorted(set(catalog_ids) - set(branches)),
            "missing": sorted(set(branches) - set(catalog_ids)),
        }

    manifest_rule_counts: Counter[str] = Counter()
    for decision_id in decisions:
        for row in _manifest_rows(_exact(registry, str(decision_id))):
            owner_table = row.get("owner_table")
            inventory_path = row.get("inventory_field_path", row.get("field_path"))
            row_key = row.get("row_key")
            if row_key is not None and (
                not isinstance(row_key, str)
                or not row_key.endswith(f":{owner_table}:{inventory_path}")
            ):
                details.setdefault("manifest_row_key_mismatch", []).append(
                    row_key
                )
            if isinstance(row.get("rule_id"), str):
                rule_ids = [str(row["rule_id"])]
                field_paths = [str(row.get("field_path"))]
            else:
                rule_ids = _string_list(
                    row.get("compiled_rule_ids", []),
                    "MANIFEST_COMPILED_RULE_IDS",
                )
                field_paths = _string_list(
                    row.get("compiled_field_paths", []),
                    "MANIFEST_COMPILED_FIELD_PATHS",
                )
            if len(rule_ids) != len(field_paths):
                details.setdefault("manifest_rule_path_arity_mismatch", []).append(
                    row_key
                )
            for rule_id, compiled_path in zip(
                rule_ids, field_paths, strict=False
            ):
                manifest_rule_counts[rule_id] += 1
                rule = rules.get(rule_id)
                if not isinstance(rule, Mapping):
                    details.setdefault("manifest_missing_rule_ids", []).append(
                        rule_id
                    )
                    continue
                payload = _rule_payload(rule)
                if payload.get("owner_table") != owner_table or payload.get(
                    "field_path"
                ) != compiled_path:
                    details.setdefault("manifest_rule_projection_mismatch", []).append(
                        rule_id
                    )
                source_row_key = payload.get("source_row_key")
                if row_key is not None and source_row_key != row_key:
                    details.setdefault("manifest_source_row_mismatch", []).append(
                        rule_id
                    )
    expected_manifest_ids = {
        rule_id
        for rule_id, rule in rules.items()
        if _mapping(rule, str(rule_id)).get("provenance", {}).get("class")
        != "AUTHORITY_CLOSED_INVENTORY"
    }
    if set(manifest_rule_counts) != expected_manifest_ids or any(
        count != 1 for count in manifest_rule_counts.values()
    ):
        details["global_manifest_rule_closure"] = {
            "extra": sorted(set(manifest_rule_counts) - expected_manifest_ids),
            "missing": sorted(expected_manifest_ids - set(manifest_rule_counts)),
            "multiplicity": {
                rule_id: count
                for rule_id, count in sorted(manifest_rule_counts.items())
                if count != 1
            },
        }

    orphan_or_invalid_branches: list[str] = []
    for branch_id, branch in branches.items():
        branch_value = _mapping(branch, str(branch_id))
        payload = _mapping(branch_value.get("payload"), f"{branch_id}_PAYLOAD")
        consumers = _string_list(
            branch_value.get("consumer_rule_ids"),
            f"{branch_id}_CONSUMER_RULE_IDS",
        )
        validator_only = payload.get("validator_only") is True
        if validator_only:
            if consumers:
                orphan_or_invalid_branches.append(str(branch_id))
        elif not consumers:
            orphan_or_invalid_branches.append(str(branch_id))
        for rule_id in consumers:
            rule = rules.get(rule_id)
            if (
                not isinstance(rule, Mapping)
                or _rule_payload(rule).get("branch_instance_id") != branch_id
            ):
                orphan_or_invalid_branches.append(str(branch_id))
                break
    if orphan_or_invalid_branches:
        details["orphan_or_invalid_branch_ids"] = sorted(
            set(orphan_or_invalid_branches)
        )
    return details


def decision_join_details(
    registry: Mapping[str, Any], oracle: Mapping[str, Any], decision_id: str
) -> dict[str, object]:
    """Join decision, reverse rule, manifest, branch, and expected-count views."""

    details: dict[str, object] = {}
    decision = _decision(registry, decision_id)
    forward_ids = _string_list(
        decision.get("compiled_rule_ids"), f"{decision_id}_RULE_IDS"
    )
    if len(forward_ids) != len(set(forward_ids)):
        details["duplicate_forward_rule_ids"] = forward_ids

    rules_by_id = _mapping(registry.get("compiled_rules_by_id"), "RULES")
    reverse_ids = sorted(
        rule_id
        for rule_id, rule in rules_by_id.items()
        if isinstance(rule_id, str)
        and isinstance(rule, Mapping)
        and _mapping(rule.get("payload"), f"{rule_id}_PAYLOAD").get(
            "decision_id"
        )
        == decision_id
    )
    if sorted(forward_ids) != reverse_ids:
        details["forward_reverse_rule_id_mismatch"] = {
            "forward_only": sorted(set(forward_ids) - set(reverse_ids)),
            "reverse_only": sorted(set(reverse_ids) - set(forward_ids)),
        }

    manifest_ids = _manifest_rule_ids(_exact(registry, decision_id))
    if len(manifest_ids) != len(set(manifest_ids)):
        details["duplicate_manifest_rule_ids"] = manifest_ids
    manifest_expected = sorted(
        rule_id
        for rule_id in forward_ids
        if _mapping(rules_by_id.get(rule_id), rule_id)
        .get("provenance", {})
        .get("class")
        != "AUTHORITY_CLOSED_INVENTORY"
    )
    if sorted(manifest_ids) != manifest_expected:
        details["manifest_rule_id_mismatch"] = {
            "decision_only": sorted(set(manifest_expected) - set(manifest_ids)),
            "manifest_only": sorted(set(manifest_ids) - set(manifest_expected)),
        }

    effect = _mapping(
        _payload(registry, decision_id).get("expected_rl_universe_effect"),
        f"{decision_id}_EXPECTED_EFFECT",
    )
    if effect.get("emitted_reference_rules") != len(forward_ids):
        details["expected_rule_count_mismatch"] = {
            "declared": effect.get("emitted_reference_rules"),
            "observed": len(forward_ids),
        }

    branch_ids = _string_list(
        _mapping(decision.get("design_payload"), "DESIGN_PAYLOAD").get(
            "branch_instance_ids"
        ),
        f"{decision_id}_BRANCH_IDS",
    )
    if len(branch_ids) != len(set(branch_ids)):
        details["duplicate_decision_branch_ids"] = branch_ids
    branches = _mapping(
        registry.get("discriminator_branches_by_id"), "BRANCHES"
    )
    derived_consumers: dict[str, list[str]] = defaultdict(list)
    for rule_id in forward_ids:
        rule = _mapping(rules_by_id.get(rule_id), rule_id)
        payload = _rule_payload(rule)
        discriminator = _mapping(
            payload.get("record_discriminator"), f"{rule_id}_DISCRIMINATOR"
        )
        branch_id = payload.get("branch_instance_id")
        if discriminator.get("mode") == "ANY":
            if branch_id is not None:
                details.setdefault("any_rule_with_branch", []).append(rule_id)
            continue
        if not isinstance(branch_id, str):
            details.setdefault("discriminated_rule_without_branch", []).append(
                rule_id
            )
            continue
        derived_consumers[branch_id].append(rule_id)
        branch = branches.get(branch_id)
        if not isinstance(branch, Mapping):
            details.setdefault("missing_branch_ids", []).append(branch_id)
            continue
        if branch.get("predicate") != discriminator:
            details.setdefault("branch_predicate_mismatch", []).append(rule_id)
        exact_consumer = _mapping(
            _mapping(branch.get("payload"), f"{branch_id}_PAYLOAD").get(
                "exact_consumer"
            ),
            f"{branch_id}_EXACT_CONSUMER",
        )
        expected_consumer = {
            "containing_record": payload.get("containing_record"),
            "field_path": payload.get("field_path"),
            "owner_table": payload.get("owner_table"),
        }
        if any(
            exact_consumer.get(key) != value
            for key, value in expected_consumer.items()
        ):
            details.setdefault("branch_consumer_mismatch", []).append(rule_id)

    derived_ids = set(derived_consumers)
    listed_ids = set(branch_ids)
    if derived_ids - listed_ids:
        details["unlisted_consumed_branch_ids"] = sorted(derived_ids - listed_ids)
    missing_listed = sorted(branch_id for branch_id in listed_ids if branch_id not in branches)
    if missing_listed:
        details["missing_listed_branch_ids"] = missing_listed

    closure = _mapping(oracle.get("structural_closure"), "STRUCTURAL_CLOSURE")
    global_catalog_id = closure.get("global_branch_catalog_decision_id")
    allowed_by_decision = _mapping(
        closure.get("allowed_validator_only_branch_ids_by_decision"),
        "VALIDATOR_ONLY_BRANCH_ALLOWLIST",
    )
    if decision_id == global_catalog_id:
        if listed_ids != set(branches) or len(branch_ids) != len(branches):
            details["global_catalog_branch_mismatch"] = {
                "extra": sorted(listed_ids - set(branches)),
                "missing": sorted(set(branches) - listed_ids),
            }
    else:
        allowed_extras = set(
            _string_list(
                allowed_by_decision.get(decision_id, []),
                f"{decision_id}_VALIDATOR_ONLY_BRANCH_IDS",
            )
        )
        listed_extras = listed_ids - derived_ids
        if listed_extras != allowed_extras:
            details["listed_unconsumed_branch_mismatch"] = {
                "extra": sorted(listed_extras - allowed_extras),
                "missing": sorted(allowed_extras - listed_extras),
            }
        for branch_id in sorted(allowed_extras):
            branch = branches.get(branch_id)
            if not isinstance(branch, Mapping):
                continue
            branch_payload = _mapping(
                branch.get("payload"), f"{branch_id}_PAYLOAD"
            )
            linked_rules = _string_list(
                branch_payload.get("linked_rule_ids", []),
                f"{branch_id}_LINKED_RULE_IDS",
            )
            linked_branches = _string_list(
                branch_payload.get("linked_branch_instance_ids", []),
                f"{branch_id}_LINKED_BRANCH_IDS",
            )
            if (
                branch_payload.get("validator_only") is not True
                or branch.get("consumer_rule_ids") != []
                or any(rule_id not in rules_by_id for rule_id in linked_rules)
                or any(linked_id not in branches for linked_id in linked_branches)
            ):
                details.setdefault("invalid_validator_only_branch_ids", []).append(
                    branch_id
                )

    for branch_id in sorted(listed_ids.intersection(branches)):
        branch = _mapping(branches.get(branch_id), branch_id)
        branch_payload = _mapping(branch.get("payload"), f"{branch_id}_PAYLOAD")
        tag_field = branch_payload.get("branch_tag_field")
        tag_value = branch_payload.get("branch_tag_value")
        branch_domain = branch_payload.get("branch_domain")
        predicate_for_domain = _mapping(
            branch.get("predicate"), "BRANCH_DOMAIN_PREDICATE"
        )
        has_reference_selector = any(
            _mapping(term.get("selector"), "BRANCH_DOMAIN_SELECTOR").get(
                "namespace"
            )
            == "REFERENCE_RECORD"
            for term in _selector_terms(
                {"record_discriminator": predicate_for_domain}
            )
        )
        if branch_domain not in {
            "CLOSED_REFERENCE_RECORD",
            "OWNER_SCHEMA_DISCRIMINATOR",
        } or (has_reference_selector and branch_domain != "CLOSED_REFERENCE_RECORD"):
            details.setdefault("branch_domain_semantic_mismatch", []).append(
                branch_id
            )
        if branch_domain == "CLOSED_REFERENCE_RECORD":
            outer_tag_value = branch_payload.get("outer_tag_value")
            predicate = _mapping(branch.get("predicate"), "BRANCH_PREDICATE")
            terms = _selector_terms({"record_discriminator": predicate})
            reference_terms = [
                term
                for term in terms
                if term
                == {
                    "literal": {"type": "ENUM", "value": tag_value},
                    "operator": "EQUALS",
                    "selector": {
                        "namespace": "REFERENCE_RECORD",
                        "path": [outer_tag_value, "role"],
                    },
                }
            ]
            if (
                tag_field != "role"
                or not isinstance(tag_value, str)
                or branch_payload.get("outer_tag_field") != "$ref_kind"
                or not isinstance(outer_tag_value, str)
                or predicate.get("mode") != "ALL_EQUAL"
                or len(reference_terms) != 1
                or any(term.get("operator") != "EQUALS" for term in terms)
            ):
                details.setdefault(
                    "closed_reference_branch_tag_semantic_mismatch", []
                ).append(branch_id)
        if isinstance(tag_field, str) and isinstance(tag_value, str):
            matching_terms = [
                term
                for term in _selector_terms(
                    {"record_discriminator": branch.get("predicate")}
                )
                if _mapping(term.get("selector"), "BRANCH_SELECTOR").get("path")
                and _mapping(term.get("selector"), "BRANCH_SELECTOR").get("path")[-1]
                == tag_field
                and _mapping(term.get("literal"), "BRANCH_LITERAL").get("value")
                == tag_value
            ]
            if len(matching_terms) != 1:
                details.setdefault("branch_tag_predicate_mismatch", []).append(
                    branch_id
                )

    for branch_id, expected_consumers in sorted(derived_consumers.items()):
        branch = branches.get(branch_id)
        if not isinstance(branch, Mapping):
            continue
        observed = _string_list(
            branch.get("consumer_rule_ids"), f"{branch_id}_CONSUMER_RULE_IDS"
        )
        if sorted(observed) != sorted(expected_consumers):
            details.setdefault("branch_backlink_mismatch", {})[branch_id] = {
                "expected": sorted(expected_consumers),
                "observed": sorted(observed),
            }
    return details


def _validate_oracle(
    oracle: Mapping[str, Any], registry: Mapping[str, Any]
) -> tuple[list[str], list[str]]:
    if oracle.get("format") != EXPECTED_ORACLE_FORMAT:
        raise ValueError("ORACLE_FORMAT_MISMATCH")
    if oracle.get("artifact_state") != (
        "FROZEN_CANDIDATE_SEMANTIC_ORACLE_PENDING_INDEPENDENT_"
        "REREVIEW_NOT_AUTHORITY"
    ):
        raise ValueError("ORACLE_ARTIFACT_STATE_MISMATCH")
    if oracle.get("stop_boundary") != "STOP_BEFORE_AUTHORITY_IDL_AND_KATS":
        raise ValueError("ORACLE_STOP_BOUNDARY_MISMATCH")
    if oracle.get("cli_exit_contract") != EXPECTED_CLI_EXIT_CONTRACT:
        raise ValueError("ORACLE_CLI_EXIT_CONTRACT_MISMATCH")
    provenance = _mapping(
        oracle.get("adjudication_provenance"), "ADJUDICATION_PROVENANCE"
    )
    source_pointers = _mapping(
        provenance.get("decision_source_pointers"), "DECISION_SOURCE_POINTERS"
    )
    if (
        provenance.get("decision_source_pointers_sha256")
        != EXPECTED_DECISION_SOURCE_POINTERS_SHA256
        or _canonical_value_sha256(source_pointers)
        != EXPECTED_DECISION_SOURCE_POINTERS_SHA256
    ):
        raise ValueError("ORACLE_SOURCE_POINTER_DIGEST_MISMATCH")
    expected_pointer_keys = {
        "GLOBAL_STRUCTURAL_CLOSURE",
        "T10-G18-DD-001",
        "T10-G18-DD-004",
        "T10-G18-DD-006",
        "T10-G18-DD-007",
        "T10-G18-DD-009",
        "T10-G18-DD-011",
        "T10-G18-DD-016",
    }
    if set(source_pointers) != expected_pointer_keys:
        raise ValueError("ORACLE_SOURCE_POINTER_SCOPE_MISMATCH")
    for pointer_id, pointer_value in source_pointers.items():
        pointer = _mapping(pointer_value, f"SOURCE_POINTER_{pointer_id}")
        if not isinstance(pointer.get("correction_spec_line_range"), str):
            raise ValueError(f"ORACLE_SOURCE_LINE_RANGE_MISSING:{pointer_id}")
        registry_pointers = _string_list(
            pointer.get("registry_json_pointers"),
            f"SOURCE_POINTER_PATHS_{pointer_id}",
        )
        if not registry_pointers or any(
            not value.startswith("/") for value in registry_pointers
        ):
            raise ValueError(f"ORACLE_REGISTRY_POINTER_INVALID:{pointer_id}")
        for registry_pointer in registry_pointers:
            _resolve_json_pointer(registry, registry_pointer)
    correction = _mapping(
        provenance.get("normative_correction_spec"), "CORRECTION_PROVENANCE"
    )
    correction_binding = _binding_details(oracle, "correction_specification")
    if any(
        correction.get(key) != correction_binding.get(key)
        for key in ("path", "sha256")
    ):
        raise ValueError("ORACLE_CORRECTION_PROVENANCE_MISMATCH")
    checks = _mapping(oracle.get("checks_by_decision"), "ORACLE_CHECKS")
    scope = _mapping(oracle.get("machine_semantic_scope"), "ORACLE_SCOPE")
    checked = _string_list(scope.get("checked_decision_ids"), "CHECKED_IDS")
    not_checked = _string_list(
        scope.get("not_semantically_audited_by_this_instrument"),
        "NOT_CHECKED_IDS",
    )
    if set(checked) != set(checks):
        raise ValueError("ORACLE_CHECK_SCOPE_MISMATCH")
    if set(checked).intersection(not_checked):
        raise ValueError("ORACLE_SCOPE_OVERLAP")
    if set(checked).union(not_checked) != set(EXPECTED_DECISION_IDS):
        raise ValueError("ORACLE_SCOPE_NOT_EXHAUSTIVE")
    bound_source_bytes = _validate_bound_sources(oracle)
    schema_value = json.loads(bound_source_bytes["oracle_schema"].decode("utf-8"))
    _validate_oracle_schema_instance(
        _mapping(schema_value, "ORACLE_SCHEMA"), oracle
    )
    if registry.get("format") != EXPECTED_FORMAT:
        raise ValueError("REGISTRY_FORMAT_MISMATCH")
    return checked, not_checked


def reference_owner_tuple_details(
    registry: Mapping[str, Any], oracle: Mapping[str, Any], decision_id: str
) -> dict[str, object]:
    oracle_check = _oracle_check(oracle, decision_id)
    if oracle_check.get("owner_tuple_interpretation") != (
        "CLOSED_SET_UNIQUE_ORDER_NON_NORMATIVE"
    ):
        raise ValueError(f"{decision_id}_OWNER_TUPLE_INTERPRETATION")
    expected_list = _string_list(
        oracle_check.get("owner_tuple"),
        f"{decision_id}_ORACLE_OWNER_TUPLE",
    )
    if expected_list != sorted(set(expected_list)):
        raise ValueError(f"{decision_id}_ORACLE_OWNER_TUPLE_NOT_CANONICAL")
    expected = set(expected_list)
    contract = _mapping(
        _payload(registry, decision_id).get("reference_contract"),
        f"{decision_id}_REFERENCE_CONTRACT",
    )
    declared_list = _string_list(
        contract.get("owner_tuple"), f"{decision_id}_OWNER_TUPLE"
    )
    declared = set(declared_list)
    compiled: set[str] = set()
    for rule in _rules_for_decision(registry, decision_id):
        compiled.update(
            _string_list(
                _rule_payload(rule).get("allowed_target_tables"),
                f"{decision_id}_RULE_TARGETS",
            )
        )
    details: dict[str, object] = {}
    if len(declared_list) != len(declared):
        details["duplicate_declared_owner_tuple_items"] = sorted(
            owner
            for owner, count in Counter(declared_list).items()
            if count != 1
        )
    if declared != expected:
        details["declared_vs_oracle"] = {
            "extra": sorted(declared - expected),
            "missing": sorted(expected - declared),
        }
    if compiled != expected:
        details["compiled_vs_oracle"] = {
            "extra": sorted(compiled - expected),
            "missing": sorted(expected - compiled),
        }
    return details


def dd001_collision_details(
    registry: Mapping[str, Any], oracle: Mapping[str, Any]
) -> dict[str, object]:
    decision_id = "T10-G18-DD-001"
    expected = _oracle_check(oracle, decision_id)
    payload = _payload(registry, decision_id)
    exact = _exact(registry, decision_id)
    paths = _string_list(exact.get("exact_retyped_paths"), "DD001_PATHS")
    census = _sequence(exact.get("coverage_compilation_manifest"), "DD001_CENSUS")
    affected = _string_list(payload.get("affected_owner_paths"), "DD001_AFFECTED")
    duplicate_path = expected.get("duplicate_path")
    census_paths = []
    census_row_keys = []
    for row in census:
        census_row = _mapping(row, "DD001_CENSUS_ROW")
        census_paths.append(
            f"{census_row.get('owner_table')}."
            f"{census_row.get('inventory_field_path')}"
        )
        census_row_keys.append(census_row.get("row_key"))
    wording = " ".join(
        str(payload.get(key, ""))
        for key in (
            "authority_amendment_text_summary",
            "current_fact",
            "neutral_verdict",
        )
    ).lower()
    details: dict[str, object] = {}
    observed_counts = {
        "affected_paths": len(set(affected)),
        "census_rows": len(census),
        "duplicate_path_rows": census_paths.count(duplicate_path),
        "exact_retyped_paths": len(set(paths)),
    }
    expected_counts = {
        "affected_paths": expected.get("unique_affected_path_count"),
        "census_rows": expected.get("census_row_count"),
        "duplicate_path_rows": expected.get("duplicate_path_row_count"),
        "exact_retyped_paths": expected.get("exact_retyped_path_count"),
    }
    if observed_counts != expected_counts:
        details["count_mismatch"] = {
            "expected": expected_counts,
            "observed": observed_counts,
        }
    expected_affected = set(
        _string_list(expected.get("affected_owner_paths"), "DD001_AFFECTED_ORACLE")
    )
    expected_exact = set(
        _string_list(expected.get("exact_retyped_paths"), "DD001_EXACT_ORACLE")
    )
    if set(affected) != expected_affected or len(affected) != len(set(affected)):
        details["affected_path_set_mismatch"] = {
            "extra": sorted(set(affected) - expected_affected),
            "missing": sorted(expected_affected - set(affected)),
            "duplicates": sorted(
                path for path, count in Counter(affected).items() if count != 1
            ),
        }
    if set(paths) != expected_exact or len(paths) != len(set(paths)):
        details["exact_retyped_path_set_mismatch"] = {
            "extra": sorted(set(paths) - expected_exact),
            "missing": sorted(expected_exact - set(paths)),
            "duplicates": sorted(
                path for path, count in Counter(paths).items() if count != 1
            ),
        }
    expected_row_keys = _string_list(
        expected.get("exact_census_row_keys"), "DD001_CENSUS_ROW_KEYS_ORACLE"
    )
    if census_row_keys != expected_row_keys:
        details["census_row_key_mismatch"] = {
            "expected": expected_row_keys,
            "observed": census_row_keys,
        }
    expected_duplicate_keys = _string_list(
        expected.get("duplicate_path_row_keys"), "DD001_DUPLICATE_ROW_KEYS"
    )
    observed_duplicate_keys = [
        row_key
        for row_key, path in zip(census_row_keys, census_paths, strict=True)
        if path == duplicate_path
    ]
    if observed_duplicate_keys != expected_duplicate_keys:
        details["duplicate_path_row_key_mismatch"] = {
            "expected": expected_duplicate_keys,
            "observed": observed_duplicate_keys,
        }
    effect = _mapping(
        payload.get("expected_rl_universe_effect"), "DD001_EXPECTED_EFFECT"
    )
    expected_effect = _mapping(
        expected.get("expected_rl_universe_effect"), "DD001_ORACLE_EFFECT"
    )
    if effect != expected_effect:
        details["effect_contract_mismatch"] = {
            "expected": dict(expected_effect),
            "observed": dict(effect),
        }
    required = _string_list(
        expected.get("required_wording_fragments"), "DD001_WORDING"
    )
    missing_wording = [fragment for fragment in required if fragment not in wording]
    if missing_wording or "eleven exact paths" in wording:
        details["wording_mismatch"] = {
            "forbidden_present": "eleven exact paths" in wording,
            "missing_required": missing_wording,
        }
    return details


def _compiled_role_map(
    registry: Mapping[str, Any],
    decision_id: str,
    *,
    containing_record: str,
    field_path: str,
    namespace: str,
    selector_path: tuple[str, ...],
) -> tuple[dict[str, str], list[str], list[str]]:
    role_rows: dict[str, list[str]] = defaultdict(list)
    targets: dict[str, str] = {}
    malformed: list[str] = []
    for rule in _rules_for_decision(registry, decision_id):
        rule_id = str(rule.get("rule_id"))
        payload = _rule_payload(rule)
        if payload.get("containing_record") != containing_record:
            continue
        role = _enum_term(payload, namespace, selector_path)
        target = _single_target(payload)
        if role is None or target is None or payload.get("field_path") != field_path:
            malformed.append(rule_id)
            continue
        role_rows[role].append(rule_id)
        prior = targets.setdefault(role, target)
        if prior != target:
            malformed.append(rule_id)
    duplicates = sorted(role for role, ids in role_rows.items() if len(ids) != 1)
    return targets, sorted(malformed), duplicates


def _semantic_rule_projection(payload: Mapping[str, Any]) -> dict[str, object]:
    return {
        "allowed_target_tables": payload.get("allowed_target_tables"),
        "cardinality": payload.get("cardinality"),
        "containing_record": payload.get("containing_record"),
        "field_path": payload.get("field_path"),
        "kind": payload.get("kind"),
        "owner_table": payload.get("owner_table"),
        "record_discriminator": payload.get("record_discriminator"),
    }


def _dd004_rule_contract_details(
    registry: Mapping[str, Any], expected: Mapping[str, Any]
) -> dict[str, object]:
    expected_projections = [
        {
            "allowed_target_tables": [target],
            "cardinality": "SCALAR",
            "containing_record": expected.get("consumer_containing_record"),
            "field_path": expected.get("field_path"),
            "kind": "AUTH_REQUIRES",
            "owner_table": expected.get("owner_table"),
            "record_discriminator": _single_owner_discriminator(
                "capture_kind", role
            ),
        }
        for role, target in _mapping(
            expected.get("role_owner"), "DD004_ROLE_OWNER"
        ).items()
    ]
    observed_projections = [
        _semantic_rule_projection(_rule_payload(rule))
        for rule in _rules_for_decision(registry, "T10-G18-DD-004")
    ]
    expected_digests = sorted(
        _canonical_value_sha256(value) for value in expected_projections
    )
    observed_digests = sorted(
        _canonical_value_sha256(value) for value in observed_projections
    )
    if observed_digests == expected_digests:
        return {}
    return {
        "expected_digests": expected_digests,
        "observed_digests": observed_digests,
        "observed_projections": observed_projections,
    }


def dd004_collision_details(
    registry: Mapping[str, Any], oracle: Mapping[str, Any]
) -> dict[str, object]:
    decision_id = "T10-G18-DD-004"
    expected = _oracle_check(oracle, decision_id)
    exact = _exact(registry, decision_id)
    details: dict[str, object] = {}
    for key, observed_key in (
        ("role_owner", "CapturedEnvironmentRef"),
        ("fields", "fields"),
        ("ordering", "ordering"),
    ):
        if exact.get(observed_key) != expected.get(key):
            details[f"exact_{key}"] = exact.get(observed_key)

    contract = _mapping(
        _payload(registry, decision_id).get("reference_contract"),
        "DD004_REFERENCE_CONTRACT",
    )
    if contract.get("owner_tuple") != expected.get("owner_tuple"):
        details["contract_owner_tuple"] = contract.get("owner_tuple")

    owner_table = str(expected.get("owner_table"))
    record_type = str(expected.get("containing_record"))
    rows = _owner_field_rows(registry, owner_table, record_type)
    schema_fields = [row.get("field_name") for row in rows]
    schema_wires = {
        str(row.get("field_name")): row.get("wire_type") for row in rows
    }
    template_kinds = {
        str(row.get("template_key", "")).split(":", 1)[0] for row in rows
    }
    if schema_fields != expected.get("fields"):
        details["schema_fields"] = schema_fields
    if schema_wires != expected.get("field_wires"):
        details["schema_wires"] = schema_wires
    if template_kinds != {"EMBEDDED"}:
        details["schema_template_kinds"] = sorted(template_kinds)
    stale_templates = sorted(
        str(template_id)
        for template_id, template in _mapping(
            registry.get("schema_templates_by_id"), "TEMPLATES"
        ).items()
        if isinstance(template, Mapping)
        and isinstance(template.get("payload"), Mapping)
        and template["payload"].get("record_type") == record_type
        and template["payload"].get("template_kind") != "EMBEDDED"
    )
    if stale_templates:
        details["stale_schema_template_ids"] = stale_templates

    containing = _owner_field_rows(
        registry, owner_table, "ComprehensionMapping"
    )
    wire_rows = [
        row
        for row in containing
        if row.get("field_name") == "captured_environment_labels"
    ]
    observed_wire = wire_rows[0].get("wire_type") if len(wire_rows) == 1 else None
    if observed_wire != expected.get("containing_wire"):
        details["containing_wire"] = observed_wire

    compiled, malformed, duplicates = _compiled_role_map(
        registry,
        decision_id,
        containing_record=str(expected.get("consumer_containing_record")),
        field_path=str(expected.get("field_path")),
        namespace=str(expected.get("selector_namespace")),
        selector_path=tuple(
            _string_list(expected.get("selector_path"), "DD004_SELECTOR_PATH")
        ),
    )
    if compiled != expected.get("role_owner"):
        details["compiled_role_owner"] = compiled
    if malformed:
        details["malformed_rule_ids"] = malformed
    if duplicates:
        details["duplicate_compiled_roles"] = duplicates
    full_rule_contract = _dd004_rule_contract_details(registry, expected)
    if full_rule_contract:
        details["full_rule_contract"] = full_rule_contract
    decision = _decision(registry, decision_id)
    observed_counts = {
        "branches": len(
            _string_list(
                _mapping(decision.get("design_payload"), "DD004_DESIGN").get(
                    "branch_instance_ids"
                ),
                "DD004_BRANCH_IDS",
            )
        ),
        "compiled_rules": len(
            _string_list(decision.get("compiled_rule_ids"), "DD004_RULE_IDS")
        ),
        "manifest_rules": len(_manifest_rule_ids(exact)),
        "expected_rules": _mapping(
            _payload(registry, decision_id).get("expected_rl_universe_effect"),
            "DD004_EFFECT",
        ).get("emitted_reference_rules"),
    }
    expected_counts = {
        "branches": expected.get("branch_count"),
        "compiled_rules": expected.get("compiled_rule_count"),
        "manifest_rules": expected.get("coverage_manifest_rule_count"),
        "expected_rules": expected.get("expected_emitted_reference_rules"),
    }
    if observed_counts != expected_counts:
        details["count_views"] = {
            "expected": expected_counts,
            "observed": observed_counts,
        }
    return details


def _single_owner_discriminator(path: str, value: str) -> dict[str, object]:
    return {
        "mode": "ALL_EQUAL",
        "terms": [
            {
                "literal": {"type": "ENUM", "value": value},
                "operator": "EQUALS",
                "selector": {"namespace": "OWNER_RECORD", "path": [path]},
            }
        ],
    }


def _dd009_matrix_rule_contract_details(
    registry: Mapping[str, Any], expected: Mapping[str, Any]
) -> dict[str, object]:
    record_contracts: dict[str, tuple[str, str, Mapping[str, Any]]] = {}
    value_map = _mapping(expected.get("value_role_owner"), "DD009_VALUE_MAP")
    for record, field_path in _mapping(
        expected.get("value_record_field_paths"), "DD009_VALUE_PATHS"
    ).items():
        record_contracts[str(record)] = (
            str(field_path),
            "binding_kind",
            value_map,
        )
    record_contracts[str(expected.get("load_containing_record"))] = (
        str(expected.get("load_field_path")),
        "source_kind",
        _mapping(expected.get("load_kind_owner"), "DD009_LOAD_MAP"),
    )
    rules_by_record: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for rule in _rules_for_decision(registry, "T10-G18-DD-009"):
        payload = _rule_payload(rule)
        record = str(payload.get("containing_record"))
        if record in record_contracts:
            rules_by_record[record].append(payload)

    details: dict[str, object] = {}
    for record, (field_path, selector_path, role_map) in record_contracts.items():
        expected_projections = [
            {
                "allowed_target_tables": [target],
                "cardinality": "SCALAR",
                "containing_record": record,
                "field_path": field_path,
                "kind": "AUTH_REQUIRES",
                "owner_table": "generated_stdlib_callbacks",
                "record_discriminator": _single_owner_discriminator(
                    selector_path, role
                ),
            }
            for role, target in role_map.items()
        ]
        observed_projections = [
            {
                "allowed_target_tables": payload.get("allowed_target_tables"),
                "cardinality": payload.get("cardinality"),
                "containing_record": payload.get("containing_record"),
                "field_path": payload.get("field_path"),
                "kind": payload.get("kind"),
                "owner_table": payload.get("owner_table"),
                "record_discriminator": payload.get("record_discriminator"),
            }
            for payload in rules_by_record.get(record, [])
        ]
        expected_digests = sorted(
            _canonical_value_sha256(value) for value in expected_projections
        )
        observed_digests = sorted(
            _canonical_value_sha256(value) for value in observed_projections
        )
        if observed_digests != expected_digests:
            details[record] = {
                "expected_digests": expected_digests,
                "observed_digests": observed_digests,
                "observed_projections": observed_projections,
            }
    return details


def dd009_collision_details(
    registry: Mapping[str, Any], oracle: Mapping[str, Any]
) -> dict[str, object]:
    decision_id = "T10-G18-DD-009"
    expected = _oracle_check(oracle, decision_id)
    exact = _exact(registry, decision_id)
    details: dict[str, object] = {}
    if exact.get("CallbackTarget") != expected.get("value_role_owner"):
        details["exact_value_role_owner"] = exact.get("CallbackTarget")
    if exact.get("CallbackLoad") != expected.get("load_kind_owner"):
        details["exact_load_kind_owner"] = exact.get("CallbackLoad")
    if exact.get("CallbackLoadSourceKinds") != expected.get("load_source_kinds"):
        details["exact_load_source_kinds"] = exact.get("CallbackLoadSourceKinds")
    if exact.get("CallbackLoadPresence") != expected.get("load_presence"):
        details["exact_load_presence"] = exact.get("CallbackLoadPresence")
    if exact.get("transfer_direction") != expected.get("transfer_direction"):
        details["exact_transfer_direction"] = exact.get("transfer_direction")
    expected_presence_template = _mapping(
        expected.get("compiled_presence_template_contract"),
        "DD009_COMPILED_PRESENCE_TEMPLATE_CONTRACT",
    )
    callback_load_templates = [
        _mapping(template, "CALLBACK_LOAD_TEMPLATE")
        for template in _mapping(
            registry.get("schema_templates_by_id"), "TEMPLATES"
        ).values()
        if isinstance(template, Mapping)
        and isinstance(template.get("payload"), Mapping)
        and template["payload"].get("record_type") == "CallbackLoadBinding"
    ]
    observed_presence_templates = [
        {
            "presence_contract": template["payload"].get("presence_contract"),
            "record_type": template["payload"].get("record_type"),
            "source_kind_field": template["payload"].get("source_kind_field"),
            "source_kind_universe": template["payload"].get(
                "source_kind_universe"
            ),
            "template_key": template["payload"].get("template_key"),
            "template_kind": template["payload"].get("template_kind"),
        }
        for template in callback_load_templates
    ]
    if observed_presence_templates != [expected_presence_template]:
        details["compiled_presence_template_contract"] = {
            "expected": dict(expected_presence_template),
            "observed": observed_presence_templates,
        }
    matrix_contract_details = _dd009_matrix_rule_contract_details(
        registry, expected
    )
    if matrix_contract_details:
        details["matrix_rule_contracts"] = matrix_contract_details

    embedded_fields = _mapping(
        expected.get("embedded_record_fields"), "DD009_EMBEDDED_FIELDS"
    )
    embedded_wires = _mapping(
        expected.get("embedded_record_wires"), "DD009_EMBEDDED_WIRES"
    )
    for record, expected_fields_value in embedded_fields.items():
        expected_fields = _string_list(
            expected_fields_value, f"DD009_{record}_FIELDS"
        )
        rows = _owner_field_rows(
            registry, "generated_stdlib_callbacks", str(record)
        )
        observed_fields = [str(row.get("field_name")) for row in rows]
        observed_wires = {
            str(row.get("field_name")): row.get("wire_type") for row in rows
        }
        if observed_fields != expected_fields:
            details.setdefault("embedded_record_field_sequence", {})[
                str(record)
            ] = observed_fields
        if observed_wires != embedded_wires.get(record):
            details.setdefault("embedded_record_wires", {})[
                str(record)
            ] = observed_wires

    record_paths = _mapping(
        expected.get("value_record_field_paths"), "DD009_RECORD_PATHS"
    )
    for record in _string_list(
        expected.get("value_containing_records"), "DD009_VALUE_RECORDS"
    ):
        compiled, malformed, duplicates = _compiled_role_map(
            registry,
            decision_id,
            containing_record=record,
            field_path=str(record_paths.get(record)),
            namespace=str(expected.get("value_selector_namespace")),
            selector_path=tuple(
                _string_list(
                    expected.get("value_selector_path"),
                    "DD009_VALUE_SELECTOR_PATH",
                )
            ),
        )
        if compiled != expected.get("value_role_owner"):
            details.setdefault("compiled_value_maps", {})[record] = compiled
        if malformed:
            details.setdefault("malformed_value_rule_ids", {})[record] = malformed
        if duplicates:
            details.setdefault("duplicate_value_roles", {})[record] = duplicates

    load_record = str(expected.get("load_containing_record"))
    compiled_load, malformed_load, duplicate_load = _compiled_role_map(
        registry,
        decision_id,
        containing_record=load_record,
        field_path=str(expected.get("load_field_path")),
        namespace=str(expected.get("load_selector_namespace")),
        selector_path=tuple(
            _string_list(
                expected.get("load_selector_path"),
                "DD009_LOAD_SELECTOR_PATH",
            )
        ),
    )
    if compiled_load != expected.get("load_kind_owner"):
        details["compiled_load_map"] = compiled_load
    if malformed_load:
        details["malformed_load_rule_ids"] = malformed_load
    if duplicate_load:
        details["duplicate_load_kinds"] = duplicate_load

    matrix_records = set(
        _string_list(expected.get("value_containing_records"), "DD009_RECORDS")
    ) | {load_record}
    observed_non_matrix: list[dict[str, object]] = []
    for rule in _rules_for_decision(registry, decision_id):
        payload = _rule_payload(rule)
        if payload.get("containing_record") in matrix_records:
            continue
        observed_non_matrix.append(
            {
                "cardinality": payload.get("cardinality"),
                "containing_record": payload.get("containing_record"),
                "field_path": payload.get("field_path"),
                "kind": payload.get("kind"),
                "owner_table": payload.get("owner_table"),
                "target": _single_target(payload),
            }
        )
    if observed_non_matrix != expected.get("non_matrix_rule_contracts"):
        details["non_matrix_rule_contracts"] = observed_non_matrix

    owner_rows = _owner_field_rows(
        registry, "generated_stdlib_callbacks", "GeneratedStdlibCallbackBinding"
    )
    expected_wires = _mapping(expected.get("owner_wires"), "DD009_OWNER_WIRES")
    owner_wires = {
        str(row.get("field_name")): row.get("wire_type")
        for row in owner_rows
        if row.get("field_name") in expected_wires
    }
    if owner_wires != expected_wires:
        details["owner_wires"] = owner_wires

    forbidden = set(
        _string_list(
            expected.get("forbidden_record_types"), "DD009_FORBIDDEN_RECORDS"
        )
    )
    owner_forbidden = sorted(
        record
        for record in forbidden
        if _owner_field_rows(registry, "generated_stdlib_callbacks", record)
    )
    templates = _mapping(registry.get("schema_templates_by_id"), "TEMPLATES")
    template_forbidden = sorted(
        {
            str(_mapping(template, "TEMPLATE").get("payload", {}).get("record_type"))
            for template in templates.values()
            if isinstance(template, Mapping)
            and isinstance(template.get("payload"), Mapping)
            and template["payload"].get("record_type") in forbidden
        }
    )
    if owner_forbidden or template_forbidden:
        details["forbidden_reference_records"] = {
            "owner_fields": owner_forbidden,
            "schema_templates": template_forbidden,
        }

    transfer_contracts: list[dict[str, object]] = []
    expected_transfer_contracts = _sequence(
        expected.get("transfer_rule_contracts"), "DD009_TRANSFER_RULE_CONTRACTS"
    )
    transfer_keys = {
        (str(contract.get("owner_table")), str(contract.get("field_path")))
        for contract in (
            _mapping(value, "DD009_TRANSFER_RULE_CONTRACT")
            for value in expected_transfer_contracts
        )
    }
    for rule in _mapping(registry.get("compiled_rules_by_id"), "RULES").values():
        if not isinstance(rule, Mapping):
            continue
        payload = _rule_payload(rule)
        key = (str(payload.get("owner_table")), str(payload.get("field_path")))
        if key not in transfer_keys:
            continue
        transfer_contracts.append(
            {
                "cardinality": payload.get("cardinality"),
                "decision_id": payload.get("decision_id"),
                "field_path": payload.get("field_path"),
                "kind": payload.get("kind"),
                "owner_table": payload.get("owner_table"),
                "target": _single_target(payload),
            }
        )
    if transfer_contracts != expected_transfer_contracts:
        details["compiled_transfer_rule_contracts"] = transfer_contracts

    decision = _decision(registry, decision_id)
    observed_counts = {
        "branches": len(
            _string_list(
                _mapping(decision.get("design_payload"), "DD009_DESIGN").get(
                    "branch_instance_ids"
                ),
                "DD009_BRANCH_IDS",
            )
        ),
        "compiled_rules": len(
            _string_list(decision.get("compiled_rule_ids"), "DD009_RULE_IDS")
        ),
        "manifest_rules": len(_manifest_rule_ids(exact)),
        "expected_rules": _mapping(
            _payload(registry, decision_id).get("expected_rl_universe_effect"),
            "DD009_EFFECT",
        ).get("emitted_reference_rules"),
    }
    expected_counts = {
        "branches": expected.get("branch_count"),
        "compiled_rules": expected.get("compiled_rule_count"),
        "manifest_rules": expected.get("coverage_manifest_rule_count"),
        "expected_rules": expected.get("expected_emitted_reference_rules"),
    }
    if observed_counts != expected_counts:
        details["count_views"] = {
            "expected": expected_counts,
            "observed": observed_counts,
        }
    return details


def _role_values(value: object) -> set[str]:
    result: set[str] = set()
    if isinstance(value, Mapping):
        for child in value.values():
            result.update(_role_values(child))
    elif isinstance(value, list):
        if all(isinstance(item, str) for item in value):
            result.update(value)
        else:
            for child in value:
                result.update(_role_values(child))
    return result


def _provider_compiled_role_owner(
    registry: Mapping[str, Any],
) -> tuple[dict[str, str], list[str]]:
    compiled: dict[str, str] = {}
    conflicts: list[str] = []
    rules = _mapping(registry.get("compiled_rules_by_id"), "RULES")
    for rule in rules.values():
        rule_value = _mapping(rule, "RULE")
        payload = _rule_payload(rule_value)
        role = _enum_term(
            payload, "REFERENCE_RECORD", ("ProviderReference", "role")
        )
        if role is None:
            continue
        target = _single_target(payload)
        if target is None:
            conflicts.append(str(rule_value.get("rule_id")))
            continue
        prior = compiled.setdefault(role, target)
        if prior != target:
            conflicts.append(str(rule_value.get("rule_id")))
    return compiled, sorted(conflicts)


def _compiled_operation_role_matrix(
    registry: Mapping[str, Any]
) -> tuple[dict[str, dict[str, list[str]]], list[str]]:
    result: dict[str, dict[str, list[str]]] = {
        "binary": {},
        "protocol": {},
        "state": {},
    }
    malformed: list[str] = []
    category_by_owner = {
        "binary_operator_capabilities": ("binary", ("operator",)),
        "protocol_capabilities": ("protocol", ("operation",)),
        "state_operation_capabilities": ("state", ("operation",)),
    }
    for rule in _rules_for_decision(registry, "T10-G18-DD-011"):
        payload = _rule_payload(rule)
        role = _enum_term(
            payload, "REFERENCE_RECORD", ("ProviderReference", "role")
        )
        if role is None:
            continue
        category_config = category_by_owner.get(str(payload.get("owner_table")))
        if category_config is None:
            malformed.append(str(rule.get("rule_id")))
            continue
        category, operation_path = category_config
        operation = _enum_term(payload, "OWNER_RECORD", operation_path)
        if operation is None or payload.get("field_path") != "provider_labels[*]":
            malformed.append(str(rule.get("rule_id")))
            continue
        result[category].setdefault(operation, []).append(role)
    return result, sorted(malformed)


def _compiled_operation_rule_contract_digest_set_sha256(
    registry: Mapping[str, Any],
) -> tuple[str, list[dict[str, object]]]:
    projections: list[dict[str, object]] = []
    for rule in _rules_for_decision(registry, "T10-G18-DD-011"):
        payload = _rule_payload(rule)
        if payload.get("field_path") != "provider_labels[*]":
            continue
        projection = _semantic_rule_projection(payload)
        projection["matrix_constraint"] = payload.get("matrix_constraint")
        projections.append(projection)
    digest_set = sorted(
        _canonical_value_sha256(projection) for projection in projections
    )
    return _canonical_value_sha256(digest_set), projections


def _provider_roles_in_branch_predicates(
    registry: Mapping[str, Any]
) -> tuple[set[str], list[str]]:
    roles: set[str] = set()
    malformed: list[str] = []
    branches = _mapping(
        registry.get("discriminator_branches_by_id"), "BRANCHES"
    )
    for branch_id, branch in branches.items():
        branch_value = _mapping(branch, str(branch_id))
        predicate = _mapping(
            branch_value.get("predicate"), f"{branch_id}_PREDICATE"
        )
        for term in _selector_terms({"record_discriminator": predicate}):
            selector = _mapping(term.get("selector"), "BRANCH_SELECTOR")
            if selector.get("namespace") != "REFERENCE_RECORD" or selector.get(
                "path"
            ) != ["ProviderReference", "role"]:
                continue
            literal = _mapping(term.get("literal"), "BRANCH_LITERAL")
            value = literal.get("value")
            if literal.get("type") != "ENUM" or not isinstance(value, str):
                malformed.append(str(branch_id))
                continue
            roles.add(value)
    return roles, sorted(malformed)


def provider_reference_details(
    registry: Mapping[str, Any], oracle: Mapping[str, Any], decision_id: str
) -> dict[str, object]:
    expected = _oracle_check(oracle, decision_id)
    expected_map = _mapping(
        expected.get("provider_role_owner"), f"{decision_id}_PROVIDER_ORACLE"
    )
    exact = _exact(registry, decision_id)
    observed_map = exact.get("ProviderReference")
    details: dict[str, object] = {}
    if observed_map != expected_map:
        details["exact_provider_role_owner"] = observed_map

    hash_fields = {
        "T10-G18-DD-011": (
            "operation_exact_role_matrix",
            "operation_family_allowed_roles",
        ),
        "T10-G18-DD-016": ("protocol_provider_allowed_roles",),
    }
    for field in hash_fields[decision_id]:
        expected_digest = expected.get(f"{field}_sha256")
        observed_digest = _canonical_value_sha256(exact.get(field))
        if observed_digest != expected_digest:
            details[f"exact_{field}_sha256"] = observed_digest

    operation_roles: set[str] = set()
    for provider_decision_id in ("T10-G18-DD-011", "T10-G18-DD-016"):
        provider_exact = _exact(registry, provider_decision_id)
        provider_oracle = _oracle_check(oracle, provider_decision_id)
        for source in _string_list(
            provider_oracle.get("operation_role_sources"),
            f"{provider_decision_id}_OPERATION_ROLE_SOURCES",
        ):
            operation_roles.update(_role_values(provider_exact.get(source)))
    if operation_roles != set(expected_map):
        details["operation_role_union"] = sorted(operation_roles)

    compiled, conflicts = _provider_compiled_role_owner(registry)
    if compiled != expected_map:
        details["compiled_provider_role_owner"] = compiled
    if conflicts:
        details["compiled_provider_conflicts"] = conflicts
    branch_roles, malformed_provider_branches = _provider_roles_in_branch_predicates(
        registry
    )
    if not branch_roles.issubset(set(expected_map)):
        details["unexpected_provider_branch_roles"] = sorted(
            branch_roles - set(expected_map)
        )
    if malformed_provider_branches:
        details["malformed_provider_branch_ids"] = malformed_provider_branches
    compiled_matrix, malformed_matrix = _compiled_operation_role_matrix(registry)
    expected_matrix = _exact(registry, "T10-G18-DD-011").get(
        "operation_exact_role_matrix"
    )
    if compiled_matrix != expected_matrix:
        details["compiled_operation_role_matrix"] = compiled_matrix
    if malformed_matrix:
        details["malformed_operation_matrix_rule_ids"] = malformed_matrix
    full_contract_digest, full_contract_projections = (
        _compiled_operation_rule_contract_digest_set_sha256(registry)
    )
    expected_contract_digest = _oracle_check(
        oracle, "T10-G18-DD-011"
    ).get("compiled_operation_rule_contract_digest_set_sha256")
    if full_contract_digest != expected_contract_digest:
        details["compiled_operation_rule_contract_digest_set_sha256"] = {
            "expected": expected_contract_digest,
            "observed": full_contract_digest,
            "observed_rule_count": len(full_contract_projections),
        }
    return details


def _detail_codes(prefix: str, details: Mapping[str, object]) -> list[str]:
    categories: set[str] = set()
    for key in details:
        if key.startswith("exact_"):
            categories.add(f"{prefix}_EXACT")
        elif "schema" in key or "wire" in key or "template" in key:
            categories.add(f"{prefix}_SCHEMA_WIRE")
        elif "branch" in key or "compiled" in key or "rule" in key:
            categories.add(f"{prefix}_COMPILED_BRANCH")
        elif "count" in key or "manifest" in key:
            categories.add(f"{prefix}_COUNT_VIEW")
        else:
            categories.add(f"{prefix}_CONTRACT")
    return sorted(categories)


def _finding(
    decision_id: str,
    code: str,
    severity: str,
    details: object,
) -> dict[str, object]:
    if severity not in SEVERITIES:
        raise ValueError(f"INVALID_SEVERITY:{severity}")
    return {
        "code": code,
        "decision_id": decision_id,
        "details": details,
        "severity": severity,
    }


def _audit_registry(
    registry: Mapping[str, Any],
    oracle: Mapping[str, Any],
    *,
    identity_mode: str,
    actual_oracle_sha256: str | None,
    actual_registry_sha256: str | None,
    oracle_path: str | None = None,
    registry_path: str | None = None,
) -> dict[str, object]:
    decision_ids = tuple(
        sorted(_mapping(registry.get("decisions_by_id"), "DECISIONS"))
    )
    if decision_ids != EXPECTED_DECISION_IDS:
        raise ValueError("DECISION_ID_UNIVERSE_MISMATCH")
    checked, not_checked = _validate_oracle(oracle, registry)
    if identity_mode not in {
        "FROZEN_EXACT_BYTES",
        "UNBOUND_PARSED_OBJECT_DIAGNOSTIC_ONLY",
    }:
        raise ValueError("INVALID_IDENTITY_MODE")

    findings: list[dict[str, object]] = []
    global_closure = global_structural_closure_details(registry, oracle)
    if global_closure:
        findings.append(
            _finding(
                "GLOBAL_FROZEN_V2",
                "GLOBAL_STRUCTURAL_CLOSURE_MISMATCH",
                "BLOCKER",
                global_closure,
            )
        )
    for decision_id in decision_ids:
        join = decision_join_details(registry, oracle, decision_id)
        if join:
            findings.append(
                _finding(
                    decision_id,
                    "CROSS_REPRESENTATION_STRUCTURAL_JOIN_MISMATCH",
                    "BLOCKER",
                    join,
                )
            )

    dd001 = dd001_collision_details(registry, oracle)
    if dd001:
        findings.append(
            _finding(
                "T10-G18-DD-001",
                "DECISION_CENSUS_PATH_COUNT_MISMATCH",
                "MINOR",
                dd001,
            )
        )

    dd004 = dd004_collision_details(registry, oracle)
    if dd004:
        dd004["detail_codes"] = _detail_codes("DD004", dd004)
        findings.append(
            _finding(
                "T10-G18-DD-004",
                "CAPTURE_REFERENCE_SEMANTIC_COLLISION",
                "MAJOR",
                dd004,
            )
        )

    for decision_id in ("T10-G18-DD-006", "T10-G18-DD-007"):
        tuple_details = reference_owner_tuple_details(
            registry, oracle, decision_id
        )
        if tuple_details:
            findings.append(
                _finding(
                    decision_id,
                    "REFERENCE_OWNER_TUPLE_MISMATCH",
                    "MAJOR",
                    tuple_details,
                )
            )

    dd007_payload = _payload(registry, "T10-G18-DD-007")
    dd007_oracle = _oracle_check(oracle, "T10-G18-DD-007")
    dd007_text = " ".join(
        str(dd007_payload.get(key, ""))
        for key in ("authority_amendment_text_summary", "neutral_verdict")
    )
    forbidden = str(dd007_oracle.get("forbidden_type_name"))
    required = str(dd007_oracle.get("required_type_name"))
    if forbidden in dd007_text or required not in dd007_text:
        findings.append(
            _finding(
                "T10-G18-DD-007",
                "REFERENCE_TYPE_NAME_MISMATCH",
                "MINOR",
                {"forbidden": forbidden, "required": required},
            )
        )

    dd009 = dd009_collision_details(registry, oracle)
    if dd009:
        dd009["detail_codes"] = _detail_codes("DD009", dd009)
        findings.append(
            _finding(
                "T10-G18-DD-009",
                "CALLBACK_REFERENCE_SEMANTIC_COLLISION",
                "MAJOR",
                dd009,
            )
        )

    for decision_id in ("T10-G18-DD-011", "T10-G18-DD-016"):
        provider = provider_reference_details(registry, oracle, decision_id)
        if provider:
            provider["detail_codes"] = _detail_codes("PROVIDER", provider)
            findings.append(
                _finding(
                    decision_id,
                    "PROVIDER_REFERENCE_SEMANTIC_COLLISION",
                    "MAJOR",
                    provider,
                )
            )

    severity_counts = {
        severity: sum(
            finding["severity"] == severity for finding in findings
        )
        for severity in ("BLOCKER", "MAJOR", "MINOR")
    }
    if identity_mode == "FROZEN_EXACT_BYTES" and not findings:
        raise ValueError("FROZEN_ADVERSE_LEDGER_UNEXPECTEDLY_HAS_NO_FINDINGS")
    affected = {str(finding["decision_id"]) for finding in findings}
    return {
        "checks_executed_by_decision": checked,
        "claim_ceiling": (
            "READ_ONLY_SCOPED_COLLISION_LEDGER_NOT_AUTHORITY_NOT_V3_CORRECTION"
        ),
        "findings": findings,
        "identity_mode": identity_mode,
        "machine_semantic_scope_count": len(checked),
        "machine_stop_decision": "STOP_BEFORE_AUTHORITY_IDL_AND_KATS",
        "not_semantically_audited": not_checked,
        "oracle_binding": {
            "path": oracle_path,
            "sha256": actual_oracle_sha256,
        },
        "registry_binding": {
            "path": registry_path,
            "sha256": actual_registry_sha256,
        },
        "scoped_decisions_without_findings": [
            decision_id for decision_id in checked if decision_id not in affected
        ],
        "severity_counts": severity_counts,
        "status": (
            "HOLD_CROSS_REPRESENTATION_SEMANTIC_COLLISION"
            if identity_mode == "FROZEN_EXACT_BYTES"
            else (
                "UNBOUND_PARSED_OBJECT_DIAGNOSTIC_ONLY_WITH_FINDINGS"
                if findings
                else "UNBOUND_PARSED_OBJECT_DIAGNOSTIC_ONLY_NO_FINDINGS"
            )
        ),
        "structural_join_decision_count": len(decision_ids),
    }


def audit_registry(
    registry: Mapping[str, Any], oracle: Mapping[str, Any]
) -> dict[str, object]:
    """Audit parsed objects without granting any exact-byte identity claim."""

    return _audit_registry(
        registry,
        oracle,
        identity_mode="UNBOUND_PARSED_OBJECT_DIAGNOSTIC_ONLY",
        actual_oracle_sha256=None,
        actual_registry_sha256=None,
    )


def _read_json_object(
    path: Path,
    expected_sha256: str,
    label: str,
    *,
    expected_path: Path,
) -> tuple[Mapping[str, Any], str]:
    data, actual = _read_bound_regular_bytes(
        path,
        expected_sha256,
        label,
        expected_path=expected_path,
    )
    value = json.loads(data.decode("utf-8"))
    return _mapping(value, label), actual


def audit_registry_paths(
    registry_path: Path, oracle_path: Path = DEFAULT_ORACLE
) -> dict[str, object]:
    """Read, hash, and parse the same raw buffers before frozen auditing."""

    registry, registry_sha256 = _read_json_object(
        registry_path,
        EXPECTED_REGISTRY_SHA256,
        "REGISTRY",
        expected_path=(
            REPOSITORY_ROOT
            / EXPECTED_SOURCE_BINDINGS["review_registry_v2"]["path"]
        ),
    )
    oracle, oracle_sha256 = _read_json_object(
        oracle_path,
        EXPECTED_ORACLE_SHA256,
        "ORACLE",
        expected_path=DEFAULT_ORACLE,
    )
    return _audit_registry(
        registry,
        oracle,
        identity_mode="FROZEN_EXACT_BYTES",
        actual_oracle_sha256=oracle_sha256,
        actual_registry_sha256=registry_sha256,
        oracle_path=str(oracle_path.resolve()),
        registry_path=str(registry_path.resolve()),
    )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        report = audit_registry_paths(args.registry)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(
            json.dumps(
                {"error": str(error), "status": "AUDIT_ERROR"},
                sort_keys=True,
            )
        )
        return 3
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1


if __name__ == "__main__":
    sys.exit(main())
