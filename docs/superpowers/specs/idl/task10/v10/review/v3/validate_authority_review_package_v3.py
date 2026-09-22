"""Independent fail-closed validator for the Task 10 v3 review input.

The validator contains its own expectations and never executes the builder.  A
PASS establishes review-input consistency only; it grants no authority, KAT,
implementation, release, or submission permission.
"""

from __future__ import annotations

import json
import os
import re
import stat
import sys
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from typing import Any, NoReturn

V2_FORMAT = "selcal.task10.g18.authority-design-decision-registry.v2"
V3_FORMAT = "selcal.task10.g18.authority-design-decision-registry.v3"
V2_SHA256 = "77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5"
V2_PATH = (
    "docs/superpowers/specs/idl/task10/v10/review/"
    "authority-design-decision-registry-v2.json"
)
EXPECTED_PREDECESSOR_BINDING = {
    "bytes": 4_282_426,
    "format": V2_FORMAT,
    "mode": "0644",
    "path": V2_PATH,
    "sha256": V2_SHA256,
}
V3_SCHEMA_PATH = (
    "docs/superpowers/specs/idl/task10/v10/review/v3/schema/"
    "authority-design-decision-registry-v3.schema.json"
)
V3_BASELINE_PATH = (
    "docs/superpowers/specs/idl/task10/v10/review/v3/"
    "authority-review-package-v3-baseline.json"
)
EXPECTED_V3_BASELINE_SHA256 = (
    "d040bd9ff1377d41e6202a1483662bd9f9a03e04263f5897e1bd4e750bd35de0"
)
EXPECTED_V3_SCHEMA_SHA256 = (
    "2be51b068bda2096374f97281de57d5675181812074c4c6b3d5e93cff1acb4c2"
)
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
EXPECTED_COUNTS = {
    "owners_by_id": 66,
    "decisions_by_id": 23,
    "coverage_rows_by_id": 264,
    "compiled_rules_by_id": 570,
    "discriminator_branches_by_id": 461,
    "reference_fields_by_id": 312,
    "schema_templates_by_id": 207,
    "evidence_refs_by_id": 149,
    "invariants_by_id": 23,
    "source_bindings_by_id": 6,
    "evidence_binding_expectations_by_key": 146,
    "legacy_aliases_by_id": 16,
}
EXPECTED_PROVENANCE = {
    "COVERAGE_DERIVED": 509,
    "POST_SCHEMA_EXTRA": 9,
    "AUTHORITY_CLOSED_INVENTORY": 52,
}
EXPECTED_TOP_LEVEL_KEYS = {
    "artifact_state",
    "authority_amendment_scope_v1_authoring_authority",
    "authority_amendment_status",
    "compiled_rules_by_id",
    "correction_class",
    "coverage_rows_by_id",
    "decisions_by_id",
    "discriminator_branches_by_id",
    "evidence_binding_expectations_by_key",
    "evidence_refs_by_id",
    "format",
    "invariants_by_id",
    "legacy_aliases_by_id",
    "legacy_rehydration",
    "machine_stop_decision",
    "normative_projection_digests_by_collection",
    "normative_projection_digests_by_decision",
    "normative_registry_projection_sha256",
    "owners_by_id",
    "predecessor_binding",
    "predecessor_v2_attestations_inherited",
    "reference_fields_by_id",
    "schema_binding",
    "schema_templates_by_id",
    "scope_boundary",
    "source_bindings_by_id",
}
DD001_PATHS = {
    "behavior_slot_manifests.entries[*].raw_member_identity_label",
    "exception_contracts.mro_identity_labels[*]",
    "external_classes.base_identity_labels[*]",
    "external_classes.mro_identity_labels[*]",
    "generated_artifacts.namedtuple_recipe.direct_tuple_base_label",
    "generated_artifacts.namedtuple_recipe.new_identity_label",
    "project_classes.exception_mro_labels[*]",
    "runtime_locator_access_steps.expected_identity_label",
    "runtime_values.kind_payload.callback_identity_label",
    "runtime_values.kind_payload.referent_identity_label",
}
DD004_ROLE_OWNER = {
    "VALUE_CONTRACT": "value_contracts",
    "PROJECT_RUNTIME_VALUE": "runtime_values",
    "PROCESS_LOCAL_IDENTITY_TOKEN": "process_local_identity_tokens",
    "PROJECT_FUNCTION_BINDING": "project_function_bindings",
}
DD009_VALUE_ROLE_OWNER = {
    "VALUE_CONTRACT": "value_contracts",
    "EXTERNAL_IDENTITY": "external_identities",
    "PROJECT_RUNTIME_VALUE": "runtime_values",
    "GENERATED_CALLBACK": "generated_stdlib_callbacks",
    "BOUND_TYPE_MEMBER": "bound_type_members",
}
DD009_LOAD_KIND_OWNER = {
    "PROJECT_GLOBAL": "project_function_bindings",
    "EXTERNAL_GLOBAL": "external_identities",
    "BUILTIN": "external_identities",
    "CLOSURE_CONTRACT": "value_contracts",
    "CLOSURE_VALUE": "runtime_values",
    "ATTRIBUTE_BOUND_MEMBER": "bound_type_members",
    "ATTRIBUTE_EXTERNAL_MEMBER": "external_type_members",
    "ATTRIBUTE_GENERATED_ACCESSOR": "generated_field_accessors",
    "ATTRIBUTE_PROJECT_DESCRIPTOR": "project_descriptors",
}
DD009_SOURCE_KINDS = [
    "CONSTANT",
    "POSITIONAL_PARAMETER",
    "KEYWORD_PARAMETER",
    "DERIVED_LOCAL",
    "PROJECT_GLOBAL",
    "EXTERNAL_GLOBAL",
    "BUILTIN",
    "CLOSURE_CONTRACT",
    "CLOSURE_VALUE",
    "ATTRIBUTE_BOUND_MEMBER",
    "ATTRIBUTE_EXTERNAL_MEMBER",
    "ATTRIBUTE_GENERATED_ACCESSOR",
    "ATTRIBUTE_PROJECT_DESCRIPTOR",
]
DD009_VALUE_PATHS = {
    "CallbackClosureBinding": "closure_cells[*].target_label",
    "CallbackDefaultBinding": "positional_defaults[*].target_label",
    "CallbackKeywordDefaultBinding": "keyword_defaults[*].target_label",
}
DD009_PRESENCE = {
    "CONSTANT": {
        "required": ["literal_value"],
        "forbidden": ["literal_name", "source_ordinal", "target_label"],
    },
    "DERIVED_LOCAL|KEYWORD_PARAMETER|POSITIONAL_PARAMETER": {
        "required": ["source_ordinal"],
        "forbidden": ["literal_name", "literal_value", "target_label"],
    },
    "TARGET_KINDS": {
        "required": ["literal_name", "target_label"],
        "forbidden": ["literal_value", "source_ordinal"],
    },
}
PROVIDER_ROLE_OWNER = {
    "EXTERNAL_PYTHON_INTRINSIC": "external_python_intrinsics",
    "EXTERNAL_TYPE_MEMBER": "external_type_members",
    "GENERATED_METHOD": "generated_methods",
    "GENERATED_STDLIB_CALLBACK": "generated_stdlib_callbacks",
    "PROJECT_DESCRIPTOR": "project_descriptors",
    "PROJECT_FUNCTION_BINDING": "project_function_bindings",
}
DD011_MATRIX_SHA256 = "c5f89afe9b88c01ea0ea0e2bb799fe33554732bed1327cab0ce534cdcce260f3"
DD011_FAMILY_SHA256 = "7d604b04ff0aa382405db55c4da2d8c400602a82f4cdf41247830b53621e3d30"
DD016_PROTOCOL_SHA256 = "94cdc5bd86547a1b7805204f1d79ee6719bc31a67fe15218631e67f14b11ccd6"
EXPECTED_NORMATIVE_PROJECTION_DIGESTS = {
    "T10-G18-DD-001": "33734cc6dae5cee24754f73c31b01f81e941a7172f5fab6484bb3167749a8aca",
    "T10-G18-DD-004": "41da7253e189dab7446f42180a517758f07aa975a78bd3b1024fb5888c607765",
    "T10-G18-DD-006": "a1269dace56fef1babd331a3907b940380896d1244606ef9e4b1455407f4b291",
    "T10-G18-DD-007": "73d7b9743182edc7921eddaf2939d4c029bcdcc5a5adc81eab738ce1c034b24e",
    "T10-G18-DD-009": "306491c0c80714a386989536866e93913d2feea078d87359abc73485f4fef624",
    "T10-G18-DD-011": "62f14d83340b7b1a2e15e18946899da1260ed2beccae69295b91017992f1172a",
    "T10-G18-DD-016": "0e826100af9a6e9e706fb718651bbaf29e582b897ba0c8dcbc2c59b68c1a78cd",
    "T10-G18-DD-020": "7b7b4660043c81a46fd227f82a639ed7c9e703f2140c817cced09a597254e58b",
}
EXPECTED_COVERAGE_PROJECTION_SHA256 = (
    "1077a5f73e45b0b622a415a0ca2bb7867d7a2d32c3bbe8e6a0a92b426fdaf5e6"
)
EXPECTED_NORMATIVE_REGISTRY_PROJECTION_SHA256 = (
    "1c342b39aef04dd8d6b664833b9a1b5e222b4d1ec1618d681ed35b17a665e7c1"
)


def _reject_non_finite(value: str) -> NoReturn:
    raise ValueError(f"NON_FINITE_JSON_NUMBER:{value}")


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        )
        + "\n"
    ).encode("utf-8")


_SCHEMA_KEYWORDS = {
    "$defs",
    "$id",
    "$ref",
    "$schema",
    "additionalProperties",
    "const",
    "description",
    "enum",
    "items",
    "minItems",
    "minLength",
    "minimum",
    "oneOf",
    "pattern",
    "patternProperties",
    "properties",
    "required",
    "title",
    "type",
    "uniqueItems",
}


def _assert_supported_schema(schema: object, path: str = "$") -> None:
    if not isinstance(schema, dict):
        raise ValueError(f"JSON_SCHEMA_DEFINITION_INVALID:{path}")
    unsupported = set(schema) - _SCHEMA_KEYWORDS
    if unsupported:
        raise ValueError(
            f"JSON_SCHEMA_UNSUPPORTED_KEYWORD:{path}:{sorted(unsupported)[0]}"
        )
    for keyword in ("$defs", "properties", "patternProperties"):
        children = schema.get(keyword, {})
        if not isinstance(children, dict):
            raise ValueError(f"JSON_SCHEMA_DEFINITION_INVALID:{path}:{keyword}")
        for name, child in children.items():
            _assert_supported_schema(child, f"{path}/{keyword}/{name}")
    items = schema.get("items")
    if items is not None:
        _assert_supported_schema(items, f"{path}/items")
    variants = schema.get("oneOf", [])
    if not isinstance(variants, list):
        raise ValueError(f"JSON_SCHEMA_DEFINITION_INVALID:{path}:oneOf")
    for index, child in enumerate(variants):
        _assert_supported_schema(child, f"{path}/oneOf/{index}")
    additional = schema.get("additionalProperties", True)
    if not isinstance(additional, bool):
        _assert_supported_schema(additional, f"{path}/additionalProperties")


def _resolve_local_schema_ref(root: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"JSON_SCHEMA_EXTERNAL_REF_FORBIDDEN:{reference}")
    value: object = root
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or part not in value:
            raise ValueError(f"JSON_SCHEMA_REF_NOT_FOUND:{reference}")
        value = value[part]
    if not isinstance(value, dict):
        raise ValueError(f"JSON_SCHEMA_REF_NOT_OBJECT:{reference}")
    return value


def _json_schema_type_matches(instance: object, expected: str) -> bool:
    return {
        "array": isinstance(instance, list),
        "boolean": isinstance(instance, bool),
        "integer": isinstance(instance, int) and not isinstance(instance, bool),
        "null": instance is None,
        "number": isinstance(instance, int | float)
        and not isinstance(instance, bool),
        "object": isinstance(instance, dict),
        "string": isinstance(instance, str),
    }.get(expected, False)


def _validate_schema_node(
    root: dict[str, Any], schema: dict[str, Any], instance: object, path: str
) -> None:
    if "$ref" in schema:
        _validate_schema_node(
            root, _resolve_local_schema_ref(root, schema["$ref"]), instance, path
        )
        return
    expected_type = schema.get("type")
    if expected_type is not None:
        if not isinstance(expected_type, str) or not _json_schema_type_matches(
            instance, expected_type
        ):
            raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:type")
    if "const" in schema and instance != schema["const"]:
        raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:const")
    if "enum" in schema and instance not in schema["enum"]:
        raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:enum")
    if "oneOf" in schema:
        matches = 0
        for variant in schema["oneOf"]:
            try:
                _validate_schema_node(root, variant, instance, path)
            except ValueError as exc:
                if not str(exc).startswith("JSON_SCHEMA_VALIDATION_FAILED:"):
                    raise
            else:
                matches += 1
        if matches != 1:
            raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:oneOf")
    if isinstance(instance, dict):
        required = schema.get("required", [])
        if not isinstance(required, list):
            raise ValueError("JSON_SCHEMA_DEFINITION_INVALID:required")
        missing = [key for key in required if key not in instance]
        if missing:
            raise ValueError(
                f"JSON_SCHEMA_VALIDATION_FAILED:{path}:required:{missing[0]}"
            )
        properties = schema.get("properties", {})
        patterns = schema.get("patternProperties", {})
        matched: set[str] = set()
        for key, value in instance.items():
            if key in properties:
                _validate_schema_node(root, properties[key], value, f"{path}/{key}")
                matched.add(key)
            for pattern, child_schema in patterns.items():
                if re.search(pattern, key):
                    _validate_schema_node(root, child_schema, value, f"{path}/{key}")
                    matched.add(key)
        additional = schema.get("additionalProperties", True)
        for key in set(instance) - matched:
            if additional is False:
                raise ValueError(
                    f"JSON_SCHEMA_VALIDATION_FAILED:{path}/{key}:additionalProperties"
                )
            if isinstance(additional, dict):
                _validate_schema_node(
                    root, additional, instance[key], f"{path}/{key}"
                )
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:minItems")
        if schema.get("uniqueItems") is True:
            values = [canonical_json_bytes(value) for value in instance]
            if len(values) != len(set(values)):
                raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:uniqueItems")
        if "items" in schema:
            for index, value in enumerate(instance):
                _validate_schema_node(
                    root, schema["items"], value, f"{path}/{index}"
                )
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:minLength")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:pattern")
    if (
        isinstance(instance, int | float)
        and not isinstance(instance, bool)
        and "minimum" in schema
        and instance < schema["minimum"]
    ):
        raise ValueError(f"JSON_SCHEMA_VALIDATION_FAILED:{path}:minimum")


def validate_schema_instance(schema: dict[str, Any], instance: object) -> None:
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("JSON_SCHEMA_DIALECT_MISMATCH")
    _assert_supported_schema(schema)
    _validate_schema_node(schema, schema, instance, "$")


def _compact_digest(value: object) -> str:
    data = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(data).hexdigest()


def _decision(registry: dict[str, Any], decision_id: str) -> dict[str, Any]:
    value = registry["decisions_by_id"][decision_id]
    if not isinstance(value, dict):
        raise ValueError(f"DECISION_NOT_OBJECT:{decision_id}")
    return value


def _payload(registry: dict[str, Any], decision_id: str) -> dict[str, Any]:
    value = _decision(registry, decision_id)["payload"]
    if not isinstance(value, dict):
        raise ValueError(f"DECISION_PAYLOAD_NOT_OBJECT:{decision_id}")
    return value


def _exact(registry: dict[str, Any], decision_id: str) -> dict[str, Any]:
    value = _payload(registry, decision_id)["exact_chosen_wire_or_matrix"]
    if not isinstance(value, dict):
        raise ValueError(f"DECISION_EXACT_NOT_OBJECT:{decision_id}")
    return value


def _rule_projection(registry: dict[str, Any], rule_id: str) -> dict[str, Any]:
    rule = deepcopy(registry["compiled_rules_by_id"][rule_id])
    rule.pop("rule_id", None)
    rule.pop("ordinal", None)
    payload = rule["payload"]
    payload.pop("branch_instance_id", None)
    payload["schema_order_key"].pop("branch_ordinal", None)
    return rule


def _branch_projection(registry: dict[str, Any], branch_id: str) -> dict[str, Any]:
    branch = deepcopy(registry["discriminator_branches_by_id"][branch_id])
    branch.pop("branch_id", None)
    branch["payload"].pop("branch_ordinal", None)
    consumers = branch.pop("consumer_rule_ids")
    branch["consumer_rules"] = sorted(
        (_rule_projection(registry, rule_id) for rule_id in consumers),
        key=canonical_json_bytes,
    )
    return branch


def _strip_derived(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: _strip_derived(child)
            for key, child in value.items()
            if key
            not in {
                "compiled_rule_ids",
                "replacement_rule_ids",
                "rule_id",
                "branch_instance_id",
                "branch_ordinals",
                "compiled_reference_rule_order",
            }
        }
    if isinstance(value, list):
        return [_strip_derived(child) for child in value]
    return value


def _decision_projection(
    registry: dict[str, Any], decision_id: str
) -> dict[str, Any]:
    decision = deepcopy(_decision(registry, decision_id))
    rule_ids = list(decision.pop("compiled_rule_ids"))
    branch_ids = list(decision["design_payload"].pop("branch_instance_ids"))
    projected = _strip_derived(decision)
    if not isinstance(projected, dict):
        raise ValueError("DECISION_PROJECTION_INVALID")
    projected["resolved_rules"] = sorted(
        (_rule_projection(registry, rule_id) for rule_id in rule_ids),
        key=canonical_json_bytes,
    )
    if decision_id != "T10-G18-DD-018":
        projected["resolved_branches"] = sorted(
            (_branch_projection(registry, branch_id) for branch_id in branch_ids),
            key=canonical_json_bytes,
        )
    return projected


def _single_term(rule: dict[str, Any]) -> tuple[str, str, str]:
    discriminator = rule["payload"]["record_discriminator"]
    terms = discriminator.get("terms")
    if not isinstance(terms, list) or len(terms) != 1:
        raise ValueError("CROSS_FIELD_MATRIX_NOT_COMPILED")
    term = terms[0]
    selector = term.get("selector", {})
    literal = term.get("literal", {})
    path = selector.get("path")
    if not isinstance(path, list) or len(path) != 1:
        raise ValueError("CROSS_FIELD_MATRIX_NOT_COMPILED")
    return selector.get("namespace"), path[0], literal.get("value")


def _rules(registry: dict[str, Any], decision_id: str) -> list[dict[str, Any]]:
    return [
        registry["compiled_rules_by_id"][rule_id]
        for rule_id in _decision(registry, decision_id)["compiled_rule_ids"]
    ]


def dd004_errors(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    decision = _decision(registry, "T10-G18-DD-004")
    payload = decision["payload"]
    exact = payload["exact_chosen_wire_or_matrix"]
    if exact.get("CapturedEnvironmentRef") != DD004_ROLE_OWNER:
        errors.append("EXACT_ROLE_OWNER_MATRIX_MISMATCH")
    if exact.get("fields") != ["capture_kind", "capture_name", "label"]:
        errors.append("EXACT_RECORD_FIELD_SEQUENCE_MISMATCH")
    if exact.get("field_wires") != {
        "capture_kind": "E[CapturedEnvironmentKind]",
        "capture_name": "S",
        "label": "RL",
    }:
        errors.append("EXACT_RECORD_FIELD_SEQUENCE_MISMATCH")
    if exact.get("containing_wire") != "tuple[R[CapturedEnvironmentRef]]":
        errors.append("EXACT_RECORD_FIELD_SEQUENCE_MISMATCH")
    if set(payload["reference_contract"]["owner_tuple"]) != set(
        DD004_ROLE_OWNER.values()
    ):
        errors.append("REFERENCE_OWNER_TUPLE_MISMATCH")
    rules = _rules(registry, "T10-G18-DD-004")
    if len(rules) != 4 or len(decision["design_payload"]["branch_instance_ids"]) != 4:
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
        return list(dict.fromkeys(errors))
    seen: dict[str, str] = {}
    for rule in rules:
        rule_payload = rule["payload"]
        try:
            namespace, field, role = _single_term(rule)
        except ValueError:
            errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
            continue
        target = rule_payload.get("allowed_target_tables")
        if (
            namespace != "OWNER_RECORD"
            or field != "capture_kind"
            or role not in DD004_ROLE_OWNER
            or target != [DD004_ROLE_OWNER.get(role)]
            or rule_payload.get("containing_record") != "CapturedEnvironmentRef"
            or rule_payload.get("field_path")
            != "comprehension_mappings[*].captured_environment_labels[*].label"
            or rule_payload.get("cardinality") != "SCALAR"
        ):
            errors.append("EXACT_ROLE_OWNER_MATRIX_MISMATCH")
        else:
            seen[role] = target[0]
        branch_id = rule_payload.get("branch_instance_id")
        branch = registry["discriminator_branches_by_id"].get(branch_id)
        if (
            branch is None
            or branch.get("consumer_rule_ids") != [rule["rule_id"]]
            or branch.get("predicate") != rule_payload.get("record_discriminator")
            or branch.get("payload", {}).get("branch_domain")
            != "OWNER_SCHEMA_DISCRIMINATOR"
            or branch.get("payload", {}).get("tag_fields") != ["capture_kind"]
        ):
            errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    if seen != DD004_ROLE_OWNER:
        errors.append("EXACT_ROLE_OWNER_MATRIX_MISMATCH")
    manifests = exact.get("coverage_compilation_manifest")
    if (
        not isinstance(manifests, list)
        or len(manifests) != 1
        or set(manifests[0].get("compiled_rule_ids", []))
        != set(decision["compiled_rule_ids"])
    ):
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    return list(dict.fromkeys(errors))


def dd009_errors(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    decision = _decision(registry, "T10-G18-DD-009")
    exact = decision["payload"]["exact_chosen_wire_or_matrix"]
    if exact.get("CallbackTarget") != DD009_VALUE_ROLE_OWNER:
        errors.append("EXACT_ROLE_OWNER_MATRIX_MISMATCH")
    if exact.get("CallbackLoad") != DD009_LOAD_KIND_OWNER:
        errors.append("EXACT_ROLE_OWNER_MATRIX_MISMATCH")
    if exact.get("CallbackLoadSourceKinds") != DD009_SOURCE_KINDS:
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    if exact.get("CallbackLoadPresence") != DD009_PRESENCE:
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    rules = _rules(registry, "T10-G18-DD-009")
    if len(rules) != 33:
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
        return list(dict.fromkeys(errors))
    matrix_rules = [
        rule for rule in rules if rule["payload"].get("branch_instance_id") is not None
    ]
    if len(matrix_rules) != 24 or len(decision["design_payload"]["branch_instance_ids"]) != 24:
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    seen_values: set[tuple[str, str, str]] = set()
    seen_loads: set[tuple[str, str]] = set()
    for rule in matrix_rules:
        payload = rule["payload"]
        try:
            namespace, field, tag = _single_term(rule)
        except ValueError:
            errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
            continue
        target = payload.get("allowed_target_tables")
        record = payload.get("containing_record")
        if record in DD009_VALUE_PATHS:
            expected = DD009_VALUE_ROLE_OWNER.get(tag)
            if (
                namespace != "OWNER_RECORD"
                or field != "binding_kind"
                or target != [expected]
                or payload.get("field_path") != DD009_VALUE_PATHS[record]
            ):
                errors.append("EXACT_ROLE_OWNER_MATRIX_MISMATCH")
            else:
                seen_values.add((record, tag, expected))
        elif record == "CallbackLoadBinding":
            expected = DD009_LOAD_KIND_OWNER.get(tag)
            if (
                namespace != "OWNER_RECORD"
                or field != "source_kind"
                or target != [expected]
                or payload.get("field_path") != "load_bindings[*].target_label"
            ):
                errors.append("EXACT_ROLE_OWNER_MATRIX_MISMATCH")
            else:
                seen_loads.add((tag, expected))
        else:
            errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
        branch = registry["discriminator_branches_by_id"].get(
            payload.get("branch_instance_id")
        )
        if (
            branch is None
            or branch.get("consumer_rule_ids") != [rule["rule_id"]]
            or branch.get("predicate") != payload.get("record_discriminator")
            or branch.get("payload", {}).get("branch_domain")
            != "OWNER_SCHEMA_DISCRIMINATOR"
            or branch.get("payload", {}).get("tag_fields") != [field]
        ):
            errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    expected_values = {
        (record, role, target)
        for record in DD009_VALUE_PATHS
        for role, target in DD009_VALUE_ROLE_OWNER.items()
    }
    if seen_values != expected_values or seen_loads != set(DD009_LOAD_KIND_OWNER.items()):
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    manifests = exact.get("coverage_compilation_manifest")
    manifest_ids = [
        rule_id
        for manifest in manifests if isinstance(manifests, list)
        for rule_id in manifest.get("compiled_rule_ids", [])
    ] if isinstance(manifests, list) else []
    if (
        len(manifest_ids) != 33
        or len(set(manifest_ids)) != 33
        or set(manifest_ids) != set(decision["compiled_rule_ids"])
    ):
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    forbidden = {"CallbackValueRef", "CallbackLoadRef"}
    templates = {
        template["payload"]["record_type"]
        for template in registry["schema_templates_by_id"].values()
    }
    if templates & forbidden:
        errors.append("CROSS_FIELD_MATRIX_NOT_COMPILED")
    return list(dict.fromkeys(errors))


def owner_tuple_errors(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for decision_id, decision in registry["decisions_by_id"].items():
        if decision_id in {"T10-G18-DD-016", "T10-G18-DD-020"}:
            continue
        owner_tuple = set(decision["payload"]["reference_contract"]["owner_tuple"])
        target_union = {
            target
            for rule_id in decision["compiled_rule_ids"]
            for target in registry["compiled_rules_by_id"][rule_id]["payload"][
                "allowed_target_tables"
            ]
        }
        if owner_tuple != target_union:
            errors.append(f"REFERENCE_OWNER_TUPLE_MISMATCH:{decision_id}")
    return errors


def provider_reference_errors(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for decision_id in ("T10-G18-DD-011", "T10-G18-DD-016"):
        if _exact(registry, decision_id).get("ProviderReference") != PROVIDER_ROLE_OWNER:
            errors.append(f"ORPHAN_EXACT_ROLE:{decision_id}")
    dd011 = _exact(registry, "T10-G18-DD-011")
    if (
        _compact_digest(dd011.get("operation_exact_role_matrix"))
        != DD011_MATRIX_SHA256
        or _compact_digest(dd011.get("operation_family_allowed_roles"))
        != DD011_FAMILY_SHA256
    ):
        errors.append("ORPHAN_EXACT_ROLE:T10-G18-DD-011")
    dd016 = _exact(registry, "T10-G18-DD-016")
    if (
        _compact_digest(dd016.get("protocol_provider_allowed_roles"))
        != DD016_PROTOCOL_SHA256
    ):
        errors.append("ORPHAN_EXACT_ROLE:T10-G18-DD-016")
    return errors


def _global_structure_errors(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(registry) != EXPECTED_TOP_LEVEL_KEYS:
        errors.append("JSON_SCHEMA_VALIDATION_FAILED:$:top_level_keys")
    for collection, expected in EXPECTED_COUNTS.items():
        if len(registry.get(collection, {})) != expected:
            errors.append(f"GLOBAL_COLLECTION_COUNT_MISMATCH:{collection}")
    if Counter(
        rule["provenance"]["class"]
        for rule in registry.get("compiled_rules_by_id", {}).values()
    ) != Counter(EXPECTED_PROVENANCE):
        errors.append("GLOBAL_COLLECTION_COUNT_MISMATCH:rule_provenance")
    if sum(
        len(owner["payload"]["field_ordinals"])
        for owner in registry.get("owners_by_id", {}).values()
    ) != 1064:
        errors.append("GLOBAL_COLLECTION_COUNT_MISMATCH:owner_field_ordinals")
    rule_ids = set(registry.get("compiled_rules_by_id", {}))
    branch_ids = set(registry.get("discriminator_branches_by_id", {}))
    if rule_ids != {f"PCR-{index:04d}" for index in range(1, 571)}:
        errors.append("GLOBAL_COLLECTION_COUNT_MISMATCH:rule_ids")
    if branch_ids != {f"BR-{index:04d}" for index in range(1, 462)}:
        errors.append("GLOBAL_COLLECTION_COUNT_MISMATCH:branch_ids")
    for index, rule_id in enumerate(sorted(rule_ids)):
        rule = registry["compiled_rules_by_id"][rule_id]
        if rule.get("rule_id") != rule_id or rule.get("ordinal") != index:
            errors.append("GLOBAL_COLLECTION_COUNT_MISMATCH:rule_ordinals")
            break
        branch_id = rule["payload"].get("branch_instance_id")
        if branch_id is not None and branch_id not in branch_ids:
            errors.append("GLOBAL_COLLECTION_COUNT_MISMATCH:rule_branch_fk")
            break
    for branch_id, branch in registry.get(
        "discriminator_branches_by_id", {}
    ).items():
        if branch.get("branch_id") != branch_id:
            errors.append("GLOBAL_COLLECTION_COUNT_MISMATCH:branch_key")
            break
        if any(rule_id not in rule_ids for rule_id in branch["consumer_rule_ids"]):
            errors.append("GLOBAL_COLLECTION_COUNT_MISMATCH:branch_rule_fk")
            break
    for collection in ("decisions_by_id", "coverage_rows_by_id"):
        for record in registry.get(collection, {}).values():
            if any(rule_id not in rule_ids for rule_id in record["compiled_rule_ids"]):
                errors.append(f"GLOBAL_COLLECTION_COUNT_MISMATCH:{collection}_rule_fk")
                break
    return errors


def _rule_canonical_order_errors(registry: dict[str, Any]) -> list[str]:
    rules = list(registry.get("compiled_rules_by_id", {}).values())

    def order_key(rule: dict[str, Any]) -> tuple[int, int, int, int]:
        key = rule["payload"]["schema_order_key"]
        return (
            key["owner_ordinal"],
            key["template_ordinal"],
            key["field_ordinal"],
            key["branch_ordinal"],
        )

    keys = [order_key(rule) for rule in rules]
    if len(keys) != len(set(keys)):
        return ["RULE_CANONICAL_ORDER_MISMATCH:duplicate_complete_key"]
    for ordinal, rule in enumerate(sorted(rules, key=order_key)):
        if (
            rule.get("rule_id") != f"PCR-{ordinal + 1:04d}"
            or rule.get("ordinal") != ordinal
        ):
            return ["RULE_CANONICAL_ORDER_MISMATCH"]
    return []


def _branch_canonical_order_errors(registry: dict[str, Any]) -> list[str]:
    branches = list(registry.get("discriminator_branches_by_id", {}).values())
    domain_rank = {"OWNER_SCHEMA_DISCRIMINATOR": 0, "CLOSED_REFERENCE_RECORD": 1}

    def order_key(branch: dict[str, Any]) -> tuple[object, ...]:
        payload = branch["payload"]
        consumers = tuple(
            sorted(
                canonical_json_bytes(_rule_projection(registry, rule_id))
                for rule_id in branch["consumer_rule_ids"]
            )
        )
        return (
            domain_rank[payload["branch_domain"]],
            canonical_json_bytes(branch["predicate"]),
            canonical_json_bytes(payload["exact_consumer"]),
            consumers,
        )

    keys = [order_key(branch) for branch in branches]
    if len(keys) != len(set(keys)):
        return ["BRANCH_CANONICAL_ORDER_MISMATCH:duplicate_semantic_key"]
    for ordinal, branch in enumerate(sorted(branches, key=order_key), start=1):
        if (
            branch.get("branch_id") != f"BR-{ordinal:04d}"
            or branch["payload"].get("branch_ordinal") != ordinal
        ):
            return ["BRANCH_CANONICAL_ORDER_MISMATCH"]
    return []


def _normative_projection_digest_errors(
    registry: dict[str, Any],
) -> list[str]:
    observed = registry.get("normative_projection_digests_by_decision")
    recomputed = {
        decision_id: sha256(
            canonical_json_bytes(_decision_projection(registry, decision_id))
        ).hexdigest()
        for decision_id in sorted(ALLOWED_DECISION_DELTAS)
    }
    if (
        observed != EXPECTED_NORMATIVE_PROJECTION_DIGESTS
        or recomputed != EXPECTED_NORMATIVE_PROJECTION_DIGESTS
    ):
        return ["NORMATIVE_PROJECTION_DIGEST_MISMATCH"]
    return []


def _coverage_projection_digest_errors(registry: dict[str, Any]) -> list[str]:
    observed = registry.get("normative_projection_digests_by_collection", {}).get(
        "coverage_rows_by_id"
    )
    recomputed = sha256(
        canonical_json_bytes(registry.get("coverage_rows_by_id", {}))
    ).hexdigest()
    if (
        observed != EXPECTED_COVERAGE_PROJECTION_SHA256
        or recomputed != EXPECTED_COVERAGE_PROJECTION_SHA256
    ):
        return ["COVERAGE_PROJECTION_DIGEST_MISMATCH"]
    return []


def _reference_field_errors(registry: dict[str, Any]) -> list[str]:
    fields = registry.get("reference_fields_by_id", {})
    expected_ids = {f"FLD-{index:04d}" for index in range(1, 313)}
    if set(fields) != expected_ids:
        return ["REFERENCE_FIELD_IDENTITY_MISMATCH"]

    complete_keys: list[tuple[int, int, int, int]] = []
    projected_payloads: list[dict[str, Any]] = []
    for field_id in sorted(fields):
        record = fields[field_id]
        if record.get("field_id") != field_id:
            return ["REFERENCE_FIELD_IDENTITY_MISMATCH"]
        payload = record.get("payload", {})
        expected_key = [
            payload.get("owner_ordinal"),
            payload.get("template_ordinal"),
            payload.get("field_ordinal"),
            0,
        ]
        if record.get("order_key") != expected_key:
            return ["REFERENCE_FIELD_COMPLETE_KEY_MISMATCH"]
        complete_keys.append(tuple(expected_key))
        projected_payloads.append(deepcopy(payload))
    if len(complete_keys) != len(set(complete_keys)):
        return ["REFERENCE_FIELD_COMPLETE_KEY_MISMATCH"]

    dd020_projection = _exact(registry, "T10-G18-DD-020").get(
        "schema_ordering", {}
    ).get("reference_field_ordinals")
    if dd020_projection != projected_payloads:
        return ["REFERENCE_FIELD_DD020_PROJECTION_MISMATCH"]
    return []


def _normative_registry_projection_digest_errors(
    registry: dict[str, Any],
) -> list[str]:
    projection = deepcopy(registry)
    observed = projection.pop("normative_registry_projection_sha256", None)
    recomputed = sha256(canonical_json_bytes(projection)).hexdigest()
    if (
        observed != EXPECTED_NORMATIVE_REGISTRY_PROJECTION_SHA256
        or recomputed != EXPECTED_NORMATIVE_REGISTRY_PROJECTION_SHA256
    ):
        return ["NORMATIVE_REGISTRY_PROJECTION_DIGEST_MISMATCH"]
    return []


def _transfer_errors(registry: dict[str, Any]) -> list[str]:
    expected_direction = [
        {
            "field": "generated_callback_transfers.callback_binding_label",
            "kind": "AUTH_REQUIRES",
            "target": "generated_stdlib_callbacks",
        },
        {
            "field": "generated_stdlib_callbacks.transfer_label",
            "kind": "VALIDATES",
            "target": "generated_callback_transfers",
        },
    ]
    if _exact(registry, "T10-G18-DD-009").get("transfer_direction") != expected_direction:
        return ["TRANSFER_DIRECTION_RULE_LINK_MISMATCH"]
    expected_contracts = {
        (
            "generated_callback_transfers",
            "callback_binding_label",
            "AUTH_REQUIRES",
            "generated_stdlib_callbacks",
        ),
        (
            "generated_stdlib_callbacks",
            "transfer_label",
            "VALIDATES",
            "generated_callback_transfers",
        ),
    }
    observed = set()
    for rule in _rules(registry, "T10-G18-DD-020"):
        payload = rule["payload"]
        target = payload.get("allowed_target_tables")
        candidate = (
            payload.get("owner_table"),
            payload.get("field_path"),
            payload.get("kind"),
            target[0] if isinstance(target, list) and len(target) == 1 else None,
        )
        if candidate in expected_contracts:
            observed.add(candidate)
    return [] if observed == expected_contracts else ["TRANSFER_DIRECTION_RULE_LINK_MISMATCH"]


def _outside_allowlist_errors(
    registry: dict[str, Any], predecessor: dict[str, Any]
) -> list[str]:
    for decision_id in sorted(set(predecessor["decisions_by_id"]) - ALLOWED_DECISION_DELTAS):
        if _decision_projection(predecessor, decision_id) != _decision_projection(
            registry, decision_id
        ):
            return [f"SEMANTIC_DIFF_OUTSIDE_ALLOWLIST:{decision_id}"]
    for collection in (
        "source_bindings_by_id",
        "evidence_refs_by_id",
        "evidence_binding_expectations_by_key",
        "legacy_aliases_by_id",
    ):
        if registry[collection] != predecessor[collection]:
            return [f"SEMANTIC_DIFF_OUTSIDE_ALLOWLIST:{collection}"]
    return []


def validate_v3_registry(
    registry: dict[str, Any], predecessor: dict[str, Any]
) -> dict[str, object]:
    if predecessor.get("format") != V2_FORMAT or sha256(
        canonical_json_bytes(predecessor)
    ).hexdigest() != V2_SHA256:
        raise ValueError("PREDECESSOR_IDENTITY_DRIFT")
    if registry.get("predecessor_binding") != EXPECTED_PREDECESSOR_BINDING:
        raise ValueError("PREDECESSOR_IDENTITY_DRIFT")
    if registry.get("schema_binding") != {
        "path": V3_SCHEMA_PATH,
        "sha256": EXPECTED_V3_SCHEMA_SHA256,
    }:
        raise ValueError("V3_SCHEMA_IDENTITY_DRIFT")
    if registry.get("predecessor_v2_attestations_inherited") is not False:
        raise ValueError("STALE_V2_ATTESTATION_INHERITED")
    if registry.get("authority_amendment_scope_v1_authoring_authority") is not False:
        raise ValueError("STALE_SCOPE_V1_REUSED")
    expected_lifecycle = {
        "format": V3_FORMAT,
        "artifact_state": "REVIEW_DECISION_INPUT_NOT_AUTHORITY",
        "correction_class": (
            "NORMATIVE_REVIEW_INPUT_CORRECTION_NOT_REPRESENTATION_ONLY"
        ),
        "authority_amendment_status": "AUTHORITY_AMENDMENT_NOT_YET_REVIEWED",
        "machine_stop_decision": "STOP_BEFORE_AUTHORITY_IDL_AND_KATS",
        "scope_boundary": {
            "authority_idl_allowed": False,
            "implementation_allowed": False,
            "kats_allowed": False,
        },
    }
    if any(registry.get(key) != value for key, value in expected_lifecycle.items()):
        raise ValueError("STOP_BOUNDARY_VIOLATION")
    if registry.get("schema_binding", {}).get("path") != V3_SCHEMA_PATH:
        raise ValueError("STOP_BOUNDARY_VIOLATION:schema_binding")

    checks: list[str] = []
    checks.extend(_global_structure_errors(registry))
    checks.extend(_branch_canonical_order_errors(registry))
    checks.extend(_rule_canonical_order_errors(registry))
    if checks:
        raise ValueError(checks[0])

    dd001 = _payload(registry, "T10-G18-DD-001")
    dd001_exact = dd001["exact_chosen_wire_or_matrix"]
    wording = " ".join(
        dd001[key]
        for key in (
            "authority_amendment_text_summary",
            "current_fact",
            "neutral_verdict",
        )
    )
    if (
        set(dd001["affected_owner_paths"]) != DD001_PATHS
        or len(dd001["affected_owner_paths"]) != 10
        or set(dd001_exact["exact_retyped_paths"]) != DD001_PATHS
        or len(dd001_exact["coverage_compilation_manifest"]) != 11
        or "ten unique" not in wording
        or "eleven census" not in wording
    ):
        raise ValueError("DECISION_CENSUS_PATH_COUNT_MISMATCH")

    checks = dd004_errors(registry)
    if checks:
        raise ValueError(checks[0])
    dd006_owner = set(
        _payload(registry, "T10-G18-DD-006")["reference_contract"]["owner_tuple"]
    )
    dd006_targets = {
        target
        for rule in _rules(registry, "T10-G18-DD-006")
        for target in rule["payload"]["allowed_target_tables"]
    }
    dd007_owner = set(
        _payload(registry, "T10-G18-DD-007")["reference_contract"]["owner_tuple"]
    )
    dd007_targets = {
        target
        for rule in _rules(registry, "T10-G18-DD-007")
        for target in rule["payload"]["allowed_target_tables"]
    }
    if dd006_owner != dd006_targets or dd007_owner != dd007_targets:
        raise ValueError("REFERENCE_OWNER_TUPLE_MISMATCH")
    dd007_text = " ".join(
        _payload(registry, "T10-G18-DD-007")[key]
        for key in ("authority_amendment_text_summary", "neutral_verdict")
    )
    if "ProjectAccessRef" in dd007_text or dd007_text.count("RootFieldAccessRef") != 2:
        raise ValueError("REFERENCE_TYPE_NAME_MISMATCH")

    checks = dd009_errors(registry)
    if checks:
        raise ValueError(checks[0])
    checks = _transfer_errors(registry)
    if checks:
        raise ValueError(checks[0])
    checks = provider_reference_errors(registry)
    if checks:
        raise ValueError(checks[0])
    checks = owner_tuple_errors(registry)
    if checks:
        raise ValueError(checks[0])
    checks = _reference_field_errors(registry)
    if checks:
        raise ValueError(checks[0])
    checks = _outside_allowlist_errors(registry, predecessor)
    if checks:
        raise ValueError(checks[0])
    checks = _coverage_projection_digest_errors(registry)
    if checks:
        raise ValueError(checks[0])
    checks = _normative_projection_digest_errors(registry)
    if checks:
        raise ValueError(checks[0])
    checks = _normative_registry_projection_digest_errors(registry)
    if checks:
        raise ValueError(checks[0])

    return {
        "branches": 461,
        "coverage_rows": 264,
        "decisions": 23,
        "owners": 66,
        "reference_fields": 312,
        "rules": 570,
        "schema_templates": 207,
        "status": "V3_SEMANTIC_CORRECTION_PASS_NOT_AUTHORITY",
    }


def _assert_no_symlink_ancestry(path: Path) -> None:
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        metadata = current.lstat()
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError(f"BOUND_SOURCE_SYMLINK:{path}")


def _read_exact_regular_0644(path: Path) -> bytes:
    absolute = path.absolute()
    _assert_no_symlink_ancestry(absolute)
    path_before = absolute.lstat()
    if not stat.S_ISREG(path_before.st_mode):
        raise ValueError(f"BOUND_SOURCE_KIND_MISMATCH:{path}")
    if stat.S_IMODE(path_before.st_mode) != 0o644:
        raise ValueError(f"BOUND_SOURCE_MODE_MISMATCH:{path}")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(absolute, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"BOUND_SOURCE_KIND_MISMATCH:{path}")
        if stat.S_IMODE(before.st_mode) != 0o644:
            raise ValueError(f"BOUND_SOURCE_MODE_MISMATCH:{path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity_before = (
        before.st_dev,
        before.st_ino,
        before.st_mode,
        before.st_size,
        before.st_mtime_ns,
    )
    identity_after = (
        after.st_dev,
        after.st_ino,
        after.st_mode,
        after.st_size,
        after.st_mtime_ns,
    )
    if identity_before != identity_after:
        raise ValueError(f"BOUND_SOURCE_CHANGED_DURING_READ:{path}")
    path_after = absolute.lstat()
    path_identity = (
        path_after.st_dev,
        path_after.st_ino,
        path_after.st_mode,
        path_after.st_size,
        path_after.st_mtime_ns,
    )
    if path_identity != identity_after:
        raise ValueError(f"BOUND_SOURCE_PATH_IDENTITY_DRIFT:{path}")
    data = b"".join(chunks)
    if len(data) != after.st_size:
        raise ValueError(f"BOUND_SOURCE_SIZE_DRIFT:{path}")
    return data


def _load_and_verify_baseline(repository_root: Path) -> dict[str, bytes]:
    relative = Path(V3_BASELINE_PATH)
    try:
        baseline_bytes = _read_exact_regular_0644(repository_root / relative)
    except (OSError, ValueError) as exc:
        raise ValueError("V3_BASELINE_IDENTITY_DRIFT") from exc
    if sha256(baseline_bytes).hexdigest() != EXPECTED_V3_BASELINE_SHA256:
        raise ValueError("V3_BASELINE_IDENTITY_DRIFT")
    baseline = json.loads(
        baseline_bytes.decode("utf-8"), parse_constant=_reject_non_finite
    )
    if canonical_json_bytes(baseline) != baseline_bytes:
        raise ValueError("V3_BASELINE_IDENTITY_DRIFT")
    if baseline.get("machine_stop_decision") != (
        "STOP_ON_ANY_PREDECESSOR_IDENTITY_DRIFT"
    ):
        raise ValueError("PREDECESSOR_IDENTITY_DRIFT:baseline_stop")
    verified: dict[str, bytes] = {}
    for record in baseline.get("files", []):
        record_path = Path(record["path"])
        if record_path.is_absolute() or ".." in record_path.parts:
            raise ValueError("PREDECESSOR_IDENTITY_DRIFT:unsafe_path")
        try:
            data = _read_exact_regular_0644(repository_root / record_path)
        except (OSError, ValueError) as exc:
            raise ValueError(f"PREDECESSOR_IDENTITY_DRIFT:{record_path}") from exc
        if (
            record.get("mode") != "0644"
            or len(data) != record.get("bytes")
            or sha256(data).hexdigest() != record.get("sha256")
        ):
            raise ValueError(f"PREDECESSOR_IDENTITY_DRIFT:{record_path}")
        verified[record_path.as_posix()] = data
    if len(verified) != 8:
        raise ValueError("PREDECESSOR_IDENTITY_DRIFT:baseline_path_count")
    return verified


def _verify_registry_source_bindings(
    repository_root: Path, registry: dict[str, Any]
) -> dict[str, bytes]:
    verified: dict[str, bytes] = {}
    for binding in registry.get("source_bindings_by_id", {}).values():
        relative = Path(binding["logical_source"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("SOURCE_BINDING_UNSAFE_PATH")
        try:
            data = _read_exact_regular_0644(repository_root / relative)
        except (OSError, ValueError) as exc:
            raise ValueError(f"SOURCE_FILE_MISSING:{relative}") from exc
        if sha256(data).hexdigest() != binding.get("sha256"):
            raise ValueError(f"SOURCE_DIGEST_MISMATCH:{relative}")
        verified[relative.as_posix()] = data
    if len(verified) != 6:
        raise ValueError("SOURCE_BINDING_COUNT_MISMATCH")
    return verified


def validate_v3_paths(repository_root: Path) -> dict[str, object]:
    review = repository_root / "docs/superpowers/specs/idl/task10/v10/review"
    verified = _load_and_verify_baseline(repository_root)
    predecessor_relative = (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-registry-v2.json"
    )
    predecessor_bytes = verified[predecessor_relative]
    if sha256(predecessor_bytes).hexdigest() != V2_SHA256:
        raise ValueError("PREDECESSOR_IDENTITY_DRIFT")
    try:
        registry_bytes = _read_exact_regular_0644(
            review / "v3/authority-design-decision-registry-v3.json"
        )
    except (OSError, ValueError) as exc:
        raise ValueError("V3_REGISTRY_IDENTITY_DRIFT") from exc
    try:
        schema_bytes = _read_exact_regular_0644(repository_root / V3_SCHEMA_PATH)
    except (OSError, ValueError) as exc:
        raise ValueError("V3_SCHEMA_IDENTITY_DRIFT") from exc
    if sha256(schema_bytes).hexdigest() != EXPECTED_V3_SCHEMA_SHA256:
        raise ValueError("V3_SCHEMA_IDENTITY_DRIFT")
    predecessor = json.loads(
        predecessor_bytes.decode("utf-8"), parse_constant=_reject_non_finite
    )
    registry = json.loads(
        registry_bytes.decode("utf-8"), parse_constant=_reject_non_finite
    )
    schema = json.loads(
        schema_bytes.decode("utf-8"), parse_constant=_reject_non_finite
    )
    if canonical_json_bytes(registry) != registry_bytes:
        raise ValueError("V3_NON_CANONICAL_JSON")
    if registry["schema_binding"]["sha256"] != sha256(schema_bytes).hexdigest():
        raise ValueError("V3_SCHEMA_IDENTITY_DRIFT")
    _verify_registry_source_bindings(repository_root, registry)
    validate_schema_instance(schema, registry)
    return validate_v3_registry(registry, predecessor)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[8]
    try:
        result = validate_v3_paths(root)
    except (KeyError, TypeError, UnicodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
    print(json.dumps(result, sort_keys=True))
