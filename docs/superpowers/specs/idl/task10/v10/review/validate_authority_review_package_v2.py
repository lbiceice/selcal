"""Standard-library validation for the Task 10 v2 review package."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import NoReturn

ASSERTION_KEYWORDS = {
    "$ref",
    "$defs",
    "type",
    "required",
    "properties",
    "patternProperties",
    "additionalProperties",
    "oneOf",
    "const",
    "enum",
    "items",
    "minItems",
    "uniqueItems",
    "pattern",
    "minimum",
    "minLength",
}
ANNOTATION_KEYWORDS = {
    "$schema",
    "$id",
    "title",
    "description",
    "$comment",
    "default",
    "examples",
}
SUPPORTED_SCHEMA_KEYWORDS = ASSERTION_KEYWORDS | ANNOTATION_KEYWORDS

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


def _fail(code: str, path: str, detail: str = "") -> NoReturn:
    suffix = f":{detail}" if detail else ""
    raise ValueError(f"{code}:{path}{suffix}")


def validate_schema_document(schema: object) -> None:
    """Reject any schema keyword that this validator cannot enforce."""

    def walk(node: object, path: str) -> None:
        if not isinstance(node, dict):
            _fail("SCHEMA_DOCUMENT_NOT_OBJECT", path)
        for keyword in node:
            if keyword not in SUPPORTED_SCHEMA_KEYWORDS:
                _fail("UNSUPPORTED_SCHEMA_KEYWORD", path, keyword)

        definitions = node.get("$defs", {})
        if not isinstance(definitions, dict):
            _fail("SCHEMA_DOCUMENT_INVALID", path, "$defs")
        for name, child in definitions.items():
            walk(child, f"{path}/$defs/{name}")

        for container_keyword in ("properties", "patternProperties"):
            container = node.get(container_keyword, {})
            if not isinstance(container, dict):
                _fail("SCHEMA_DOCUMENT_INVALID", path, container_keyword)
            for name, child in container.items():
                walk(child, f"{path}/{container_keyword}/{name}")

        additional = node.get("additionalProperties", True)
        if not isinstance(additional, bool):
            walk(additional, f"{path}/additionalProperties")

        items = node.get("items")
        if items is not None:
            walk(items, f"{path}/items")

        alternatives = node.get("oneOf", [])
        if not isinstance(alternatives, list):
            _fail("SCHEMA_DOCUMENT_INVALID", path, "oneOf")
        for index, child in enumerate(alternatives):
            walk(child, f"{path}/oneOf/{index}")

    walk(schema, "#")


def _resolve_ref(root_schema: dict[str, object], reference: str) -> dict[str, object]:
    if not reference.startswith("#/"):
        _fail("SCHEMA_REF_UNSUPPORTED", "#", reference)
    value: object = root_schema
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or part not in value:
            _fail("SCHEMA_REF_MISSING", "#", reference)
        value = value[part]
    if not isinstance(value, dict):
        _fail("SCHEMA_REF_NOT_OBJECT", "#", reference)
    return value


def _is_type(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, int | float) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    _fail("SCHEMA_TYPE_UNSUPPORTED", "#", expected)


def _strict_equal(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right


def validate_instance(schema: dict[str, object], instance: object) -> None:
    """Validate one instance against the supported 2020-12 subset."""

    validate_schema_document(schema)

    def check(node: dict[str, object], value: object, path: str) -> None:
        reference = node.get("$ref")
        if reference is not None:
            if not isinstance(reference, str):
                _fail("SCHEMA_REF_INVALID", path)
            check(_resolve_ref(schema, reference), value, path)

        expected_type = node.get("type")
        if expected_type is not None:
            types = expected_type if isinstance(expected_type, list) else [expected_type]
            if not all(isinstance(item, str) for item in types):
                _fail("SCHEMA_DOCUMENT_INVALID", path, "type")
            if not any(_is_type(value, item) for item in types):
                _fail("SCHEMA_TYPE", path, repr(expected_type))

        if "const" in node and not _strict_equal(value, node["const"]):
            _fail("SCHEMA_CONST", path)

        choices = node.get("enum")
        if choices is not None:
            if not isinstance(choices, list):
                _fail("SCHEMA_DOCUMENT_INVALID", path, "enum")
            if not any(_strict_equal(value, choice) for choice in choices):
                _fail("SCHEMA_ENUM", path)

        alternatives = node.get("oneOf")
        if alternatives is not None:
            if not isinstance(alternatives, list):
                _fail("SCHEMA_DOCUMENT_INVALID", path, "oneOf")
            matches = 0
            for alternative in alternatives:
                try:
                    check(alternative, value, path)
                except ValueError:
                    continue
                matches += 1
            if matches != 1:
                _fail("SCHEMA_ONE_OF", path, f"matches={matches}")

        if isinstance(value, dict):
            required = node.get("required", [])
            if not isinstance(required, list):
                _fail("SCHEMA_DOCUMENT_INVALID", path, "required")
            for name in required:
                if name not in value:
                    _fail("SCHEMA_REQUIRED", path, str(name))

            properties = node.get("properties", {})
            patterns = node.get("patternProperties", {})
            if not isinstance(properties, dict) or not isinstance(patterns, dict):
                _fail("SCHEMA_DOCUMENT_INVALID", path, "object-properties")
            matched: set[str] = set()
            for name, child_schema in properties.items():
                if name in value:
                    matched.add(name)
                    check(child_schema, value[name], f"{path}/{name}")
            for expression, child_schema in patterns.items():
                for name, child in value.items():
                    if re.search(expression, name):
                        matched.add(name)
                        check(child_schema, child, f"{path}/{name}")
            additional = node.get("additionalProperties", True)
            for name, child in value.items():
                if name in matched:
                    continue
                if additional is False:
                    _fail("SCHEMA_ADDITIONAL_PROPERTY", path, name)
                if isinstance(additional, dict):
                    check(additional, child, f"{path}/{name}")

        if isinstance(value, list):
            minimum_items = node.get("minItems")
            if minimum_items is not None and len(value) < minimum_items:
                _fail("SCHEMA_MIN_ITEMS", path)
            if node.get("uniqueItems") is True:
                encoded = [
                    json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value
                ]
                if len(encoded) != len(set(encoded)):
                    _fail("SCHEMA_UNIQUE_ITEMS", path)
            item_schema = node.get("items")
            if isinstance(item_schema, dict):
                for index, child in enumerate(value):
                    check(item_schema, child, f"{path}/{index}")

        if isinstance(value, str):
            minimum_length = node.get("minLength")
            if minimum_length is not None and len(value) < minimum_length:
                _fail("SCHEMA_MIN_LENGTH", path)
            pattern = node.get("pattern")
            if pattern is not None and re.search(pattern, value) is None:
                _fail("SCHEMA_PATTERN", path, pattern)

        minimum = node.get("minimum")
        if minimum is not None and isinstance(value, int | float):
            if isinstance(value, bool) or value < minimum:
                _fail("SCHEMA_MINIMUM", path)

    check(schema, instance, "$")


def validate_registry_schema_binding(registry: dict[str, object], schema_path: Path) -> None:
    binding = registry.get("schema_binding")
    if not isinstance(binding, dict):
        _fail("SCHEMA_BINDING_MISSING", "$/schema_binding")
    expected = sha256(schema_path.read_bytes()).hexdigest()
    if binding.get("sha256") != expected:
        _fail("SCHEMA_SHA_MISMATCH", "$/schema_binding/sha256")


def _canonical_json_bytes(value: object) -> bytes:
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


def _content_id(prefix: str, value: object) -> str:
    return f"{prefix}-{sha256(_canonical_json_bytes(value)).hexdigest()}"


def _value_at(value: object, path: list[str]) -> object:
    current = value
    for part in path:
        if not isinstance(current, dict) or part not in current:
            _fail("INVARIANT_PATH_MISSING", "$", "/".join(path))
        current = current[part]
    return current


def _flatten_reference(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    _fail("FOREIGN_KEY_SHAPE_INVALID", "$")


def execute_declarative_invariants(package: dict[str, object], repository_root: Path) -> None:
    """Execute every invariant record; descriptions never act as assertions."""

    invariants = package["invariants_by_id"]
    for invariant_id in sorted(invariants):
        record = invariants[invariant_id]
        kind = record["kind"]
        assertion = record["assertion"]
        if kind == "COUNT_EQUALS":
            actual = len(package[assertion["collection"]])
            if actual != assertion["expected"]:
                _fail("COUNT_MISMATCH", f"$/invariants_by_id/{invariant_id}")
        elif kind == "PARTITION_COUNTS":
            counts: dict[str, int] = {}
            for value in package[assertion["collection"]].values():
                key = _value_at(value, assertion["value_path"])
                counts[key] = counts.get(key, 0) + 1
            if counts != assertion["expected"]:
                _fail("RULE_PARTITION_COUNTS", f"$/invariants_by_id/{invariant_id}")
        elif kind == "SUM_EQUALS":
            partition = invariants[assertion["partition_invariant_id"]]["assertion"]
            if sum(partition["expected"].values()) != assertion["expected"]:
                _fail("INVARIANT_SUM_MISMATCH", f"$/invariants_by_id/{invariant_id}")
        elif kind == "FOREIGN_KEY":
            target = package[assertion["target_collection"]]
            for source in package[assertion["source_collection"]].values():
                for identifier in _flatten_reference(_value_at(source, assertion["source_path"])):
                    if identifier not in target:
                        _fail(
                            "FOREIGN_KEY_MISSING", f"$/invariants_by_id/{invariant_id}", identifier
                        )
        elif kind == "UNIQUE_KEY":
            seen: set[str] = set()
            for value in package[assertion["collection"]].values():
                key = [_value_at(value, path) for path in assertion["value_paths"]]
                encoded = json.dumps(key, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                if encoded in seen:
                    _fail("UNIQUE_KEY_DUPLICATE", f"$/invariants_by_id/{invariant_id}")
                seen.add(encoded)
        elif kind == "ALL_MATCH":
            for check in assertion["checks"]:
                if not _strict_equal(_value_at(package, check["path"]), check["equals"]):
                    _fail("ALL_MATCH_FAILED", f"$/invariants_by_id/{invariant_id}")
        elif kind == "SOURCE_DIGEST_MATCH":
            for binding in package[assertion["collection"]].values():
                path = repository_root / binding["logical_source"]
                if not path.is_file():
                    _fail("SOURCE_FILE_MISSING", str(path))
                if sha256(path.read_bytes()).hexdigest() != binding["sha256"]:
                    _fail("SOURCE_DIGEST_MISMATCH", str(path))
        elif kind == "CANONICAL_ORDER":
            ordinals = sorted(
                _value_at(value, assertion["ordinal_path"])
                for value in package[assertion["collection"]].values()
            )
            expected = list(range(assertion["start"], assertion["start"] + len(ordinals)))
            if ordinals != expected:
                _fail("CANONICAL_ORDER_MISMATCH", f"$/invariants_by_id/{invariant_id}")
        elif kind == "SET_EQUALS":
            expected = {
                f"{assertion['prefix']}{index:0{assertion['width']}d}"
                for index in range(assertion["start"], assertion["end"] + 1)
            }
            if set(package[assertion["collection"]]) != expected:
                _fail("SET_MISMATCH", f"$/invariants_by_id/{invariant_id}")
        elif kind == "EXACT_PARTITION":
            members = {
                identifier
                for value in package[assertion["member_collection"]].values()
                for identifier in _flatten_reference(_value_at(value, assertion["member_path"]))
            }
            partition = {
                identifier
                for identifier, value in package[assertion["partition_collection"]].items()
                if _value_at(value, assertion["partition_path"]) == assertion["partition_value"]
            }
            if members != partition:
                _fail("EXACT_PARTITION_MISMATCH", f"$/invariants_by_id/{invariant_id}")
        else:
            _fail("INVARIANT_KIND_UNIMPLEMENTED", f"$/invariants_by_id/{invariant_id}", kind)


def _validate_evidence_integrity(package: dict[str, object]) -> None:
    sources = package["source_bindings_by_id"]
    expectations = package["evidence_binding_expectations_by_key"]
    for identifier, evidence in package["evidence_refs_by_id"].items():
        source_id = evidence["source_binding_id"]
        if source_id not in sources:
            _fail("EVIDENCE_SOURCE_MISSING", f"$/evidence_refs_by_id/{identifier}")
        locator = evidence["locator"]
        claim_role = evidence["claim_role"]
        if claim_role == "DESIGN_DECISION" and locator["kind"] != "DECISION_ONLY":
            _fail("DECISION_ONLY_PROMOTED_TO_LINE", f"$/evidence_refs_by_id/{identifier}")
        key = _content_id("EBK", {"claim_role": claim_role, "locator": locator})
        expected_source = expectations.get(key)
        if expected_source is not None and expected_source != source_id:
            _fail("EVIDENCE_WRONG_VALID_SOURCE", f"$/evidence_refs_by_id/{identifier}")
        if identifier != _content_id("EV", evidence):
            _fail("EVIDENCE_REF_ID_MISMATCH", f"$/evidence_refs_by_id/{identifier}")
        if expected_source is None:
            _fail("EVIDENCE_BINDING_EXPECTATION_MISSING", f"$/evidence_refs_by_id/{identifier}")


def _validate_source_binding_ids(package: dict[str, object]) -> None:
    for identifier, binding in package["source_bindings_by_id"].items():
        expected = _content_id(
            "SRC",
            {
                "logical_source": binding["logical_source"],
                "sha256": binding["sha256"],
            },
        )
        if identifier != expected:
            _fail("SOURCE_BINDING_ID_MISMATCH", f"$/source_bindings_by_id/{identifier}")


def _validate_specific_uniqueness(package: dict[str, object]) -> None:
    template_keys = [value["semantic_key"] for value in package["schema_templates_by_id"].values()]
    if len(template_keys) != len(set(template_keys)):
        _fail("DUPLICATE_TEMPLATE_SEMANTIC_KEY", "$/schema_templates_by_id")
    signatures = []
    for rule in package["compiled_rules_by_id"].values():
        signatures.append(
            json.dumps(
                {
                    "provenance": rule["provenance"],
                    "evidence_ref_ids": rule["evidence_ref_ids"],
                    "payload": rule["payload"],
                },
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
    if len(signatures) != len(set(signatures)):
        _fail("DUPLICATE_RULE_BODY", "$/compiled_rules_by_id")


def _load_migrator():
    path = Path(__file__).resolve().parent / "migrate_authority_decision_registry_v1_to_v2.py"
    spec = importlib.util.spec_from_file_location("task10_v2_validator_migrator", path)
    if spec is None or spec.loader is None:
        _fail("MIGRATOR_LOAD_FAILED", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _verify_hash_bound_baseline(repository_root: Path):
    migrator = _load_migrator()
    migrator.verify_hash_bound_baseline(repository_root)
    return migrator


def validate_markdown_index(markdown_text: str) -> None:
    if "```json" in markdown_text or "compiled_rules_by_id" in markdown_text:
        _fail("MARKDOWN_EMBEDDED_REGISTRY", "$/markdown")
    if len(markdown_text.encode("utf-8")) >= 100_000:
        _fail("MARKDOWN_INDEX_TOO_LARGE", "$/markdown")


def validate_package(
    package: dict[str, object],
    *,
    schema_path: Path,
    repository_root: Path,
    markdown_text: str,
) -> None:
    migrator = _verify_hash_bound_baseline(repository_root)
    schema = json.loads(schema_path.read_text("utf-8"))
    validate_registry_schema_binding(package, schema_path)
    validate_instance(schema, package)
    _validate_evidence_integrity(package)
    _validate_source_binding_ids(package)
    _validate_specific_uniqueness(package)
    execute_declarative_invariants(package, repository_root)
    v1_binding = next(
        binding
        for binding in package["source_bindings_by_id"].values()
        if binding["logical_source"].endswith("authority-design-decision-registry-v1.json")
    )
    v1_path = repository_root / v1_binding["logical_source"]
    v1_bytes = v1_path.read_bytes()
    v1 = migrator.parse_v1_bytes(v1_bytes)
    if migrator.rule_projection_from_v1(v1) != migrator.rule_projection_from_v2(package):
        _fail("RULE_PROJECTION_MISMATCH", "$/compiled_rules_by_id")
    if migrator.semantic_projection_from_v1(v1) != migrator.semantic_projection_from_v2(
        package
    ):
        _fail("SEMANTIC_PROJECTION_MISMATCH", "$")
    regenerated = migrator.canonical_json_bytes(
        migrator.migrate_v1_bytes(
            v1_bytes,
            registry_schema_sha256=sha256(schema_path.read_bytes()).hexdigest(),
        )
    )
    if regenerated != _canonical_json_bytes(package):
        _fail("DETERMINISTIC_REGENERATION_MISMATCH", "$")
    if sha256(migrator.legacy_v1_bytes(package)).hexdigest() != v1_binding["sha256"]:
        _fail("LEGACY_ROUNDTRIP_SHA_MISMATCH", "$/legacy_rehydration")
    validate_markdown_index(markdown_text)


def validate_registry_file(
    *,
    registry_path: Path,
    schema_path: Path,
    repository_root: Path,
    markdown_text: str,
) -> dict[str, object]:
    _verify_hash_bound_baseline(repository_root)
    data = registry_path.read_bytes()
    try:
        package = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        _fail("REGISTRY_JSON_INVALID", str(registry_path), str(error))
    if not isinstance(package, dict):
        _fail("REGISTRY_ROOT_NOT_OBJECT", str(registry_path))
    try:
        canonical = _canonical_json_bytes(package)
    except (TypeError, ValueError) as error:
        _fail("REGISTRY_JSON_INVALID", str(registry_path), str(error))
    if canonical != data:
        _fail("NON_CANONICAL_REGISTRY_BYTES", str(registry_path))
    validate_package(
        package,
        schema_path=schema_path,
        repository_root=repository_root,
        markdown_text=markdown_text,
    )
    return package


def adversarial_mutations(package: dict[str, object]) -> dict[str, dict[str, object]]:
    """Return one isolated, schema-valid where possible, adverse mutation per class."""

    cases: dict[str, dict[str, object]] = {}

    def add(
        name: str, registry: dict[str, object], markdown: str = "NON_NORMATIVE_DERIVED_VIEW"
    ) -> None:
        cases[name] = {"registry": registry, "markdown_text": markdown}

    mutation = copy.deepcopy(package)
    rule_ids = sorted(mutation["compiled_rules_by_id"])
    source = mutation["compiled_rules_by_id"][rule_ids[0]]
    target = mutation["compiled_rules_by_id"][rule_ids[1]]
    for key in ("provenance", "evidence_ref_ids", "payload"):
        target[key] = copy.deepcopy(source[key])
    add("duplicated_rule_body", mutation)

    mutation = copy.deepcopy(package)
    decision = next(
        value for value in mutation["decisions_by_id"].values() if value["compiled_rule_ids"]
    )
    decision["compiled_rule_ids"][0] = "PCR-9999"
    add("dangling_rule_id", mutation)

    mutation = copy.deepcopy(package)
    next(iter(mutation["compiled_rules_by_id"].values()))["provenance"]["class"] = (
        "POST_SCHEMA_EXTRA"
    )
    add("wrong_rule_partition", mutation)

    mutation = copy.deepcopy(package)
    mutation["coverage_rows_by_id"].pop(sorted(mutation["coverage_rows_by_id"])[-1])
    add("removed_coverage_row", mutation)

    mutation = copy.deepcopy(package)
    evidence = next(iter(mutation["evidence_refs_by_id"].values()))
    mutation["source_bindings_by_id"].pop(evidence["source_binding_id"])
    add("missing_source_binding", mutation)

    mutation = copy.deepcopy(package)
    evidence = next(iter(mutation["evidence_refs_by_id"].values()))
    evidence["source_binding_id"] = next(
        identifier
        for identifier in mutation["source_bindings_by_id"]
        if identifier != evidence["source_binding_id"]
    )
    add("wrong_valid_evidence_source", mutation)

    mutation = copy.deepcopy(package)
    evidence = next(
        value
        for value in mutation["evidence_refs_by_id"].values()
        if value["claim_role"] == "AUTHORITY_FACT"
    )
    evidence["locator"]["ranges"][0] = "L999999-L999999"
    add("changed_evidence_locator", mutation)

    mutation = copy.deepcopy(package)
    evidence = next(
        value
        for value in mutation["evidence_refs_by_id"].values()
        if value["claim_role"] == "DESIGN_DECISION"
    )
    evidence["locator"] = {
        "kind": "LINE_RANGE",
        "ranges": ["L1-L1"],
        "sections": ["invalid promotion"],
    }
    add("decision_only_promoted_to_line", mutation)

    mutation = copy.deepcopy(package)
    next(iter(mutation["decisions_by_id"].values()))["reference_kinds"] = "AUTH_REQUIRES"
    add("scalar_reference_kind", mutation)

    mutation = copy.deepcopy(package)
    mutation["scope_boundary"]["authority_idl_allowed"] = "false"
    add("string_boolean", mutation)

    mutation = copy.deepcopy(package)
    rule = next(
        value
        for value in mutation["compiled_rules_by_id"].values()
        if len(value["payload"].get("allowed_target_tables", [])) > 1
    )
    rule["payload"]["allowed_target_tables"].reverse()
    add("changed_ordered_tuple", mutation)

    mutation = copy.deepcopy(package)
    template_ids = sorted(mutation["schema_templates_by_id"])
    mutation["schema_templates_by_id"][template_ids[1]]["semantic_key"] = mutation[
        "schema_templates_by_id"
    ][template_ids[0]]["semantic_key"]
    add("duplicate_template_key", mutation)

    add(
        "embedded_full_registry_markdown",
        copy.deepcopy(package),
        "NON_NORMATIVE_DERIVED_VIEW\n```json\n" + json.dumps(package, sort_keys=True) + "\n```\n",
    )

    mutation = copy.deepcopy(package)
    mutation["review_verdict"] = "PASS"
    add("review_verdict_inside_registry", mutation)

    mutation = copy.deepcopy(package)
    next(iter(mutation["owners_by_id"].values()))["payload"]["record_type"] += (
        "Mutated"
    )
    add("changed_owner_semantics", mutation)

    mutation = copy.deepcopy(package)
    next(iter(mutation["owners_by_id"].values()))["owner_table"] += "_mutated"
    add("changed_owner_table_semantics", mutation)

    mutation = copy.deepcopy(package)
    next(iter(mutation["reference_fields_by_id"].values()))["payload"][
        "field_path"
    ] += ".mutated"
    add("changed_reference_field_semantics", mutation)

    mutation = copy.deepcopy(package)
    template = next(iter(mutation["schema_templates_by_id"].values()))
    template["payload"]["record_type"] += "Mutated"
    template["semantic_key"] += "|Mutated"
    add("changed_template_semantics", mutation)

    mutation = copy.deepcopy(package)
    coverage = next(
        value
        for value in mutation["coverage_rows_by_id"].values()
        if value["evidence_ref_ids"]
    )
    coverage["evidence_ref_ids"].pop()
    add("removed_coverage_evidence_semantics", mutation)

    mutation = copy.deepcopy(package)
    old_evidence_id, evidence = next(iter(mutation["evidence_refs_by_id"].items()))
    evidence["source_binding_id"] = next(
        source_id
        for source_id in mutation["source_bindings_by_id"]
        if source_id != evidence["source_binding_id"]
    )
    new_evidence_id = _content_id("EV", evidence)
    mutation["evidence_refs_by_id"].pop(old_evidence_id)
    mutation["evidence_refs_by_id"][new_evidence_id] = evidence

    def replace_evidence_id(value: object) -> None:
        if isinstance(value, dict):
            for child in value.values():
                replace_evidence_id(child)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                if child == old_evidence_id:
                    value[index] = new_evidence_id
                else:
                    replace_evidence_id(child)

    replace_evidence_id(mutation)
    expectation_key = _content_id(
        "EBK",
        {"claim_role": evidence["claim_role"], "locator": evidence["locator"]},
    )
    mutation["evidence_binding_expectations_by_key"][expectation_key] = evidence[
        "source_binding_id"
    ]
    add("coordinated_wrong_valid_evidence_source", mutation)

    mutation = copy.deepcopy(package)
    next(iter(mutation["invariants_by_id"].values()))["assertion"][
        "ignored_unknown_control"
    ] = True
    add("unknown_invariant_assertion_control", mutation)

    mutation = copy.deepcopy(package)
    v1_source = next(
        value
        for value in mutation["source_bindings_by_id"].values()
        if value["logical_source"].endswith("authority-design-decision-registry-v1.json")
    )
    v1_source["sha256"] = "f" * 64
    add("changed_v1_sha", mutation)
    return cases


MUTATION_FAILURE_CODES = {
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


def run_self_test(
    *, registry_path: Path, schema_path: Path, repository_root: Path
) -> dict[str, object]:
    _verify_hash_bound_baseline(repository_root)
    index_path = registry_path.with_name("authority-design-decision-index-v2.md")
    markdown_text = (
        index_path.read_text("utf-8") if index_path.is_file() else "NON_NORMATIVE_DERIVED_VIEW"
    )
    package = validate_registry_file(
        registry_path=registry_path,
        schema_path=schema_path,
        repository_root=repository_root,
        markdown_text=markdown_text,
    )
    observed = 0
    for name, case in adversarial_mutations(package).items():
        try:
            validate_package(
                case["registry"],
                schema_path=schema_path,
                repository_root=repository_root,
                markdown_text=case["markdown_text"],
            )
        except ValueError as error:
            expected = MUTATION_FAILURE_CODES[name]
            if expected not in str(error):
                raise ValueError(
                    f"MUTATION_WRONG_FAILURE:{name}:expected={expected}:actual={error}"
                ) from error
            observed += 1
        else:
            raise ValueError(f"MUTATION_FALSE_GREEN:{name}")
    return {
        "positive_package": "PASS",
        "mutation_cases": len(MUTATION_FAILURE_CODES),
        "mutation_failures_observed": observed,
    }


def validate_attestation(
    attestation: dict[str, object],
    *,
    attestation_schema_path: Path,
    subject_path: Path,
    registry_schema_path: Path,
    attestation_path: Path,
    mode: str = "PREWRITE",
) -> None:
    if mode not in {"PREWRITE", "READBACK"}:
        _fail("ATTESTATION_VALIDATION_MODE_UNKNOWN", mode)

    repository_root = Path(__file__).resolve().parents[7]
    _verify_hash_bound_baseline(repository_root)
    schema = json.loads(attestation_schema_path.read_text("utf-8"))
    validate_schema_document(schema)
    validate_instance(schema, attestation)

    provenance_values = [
        attestation["reviewer"]["identity"],
        attestation["reviewer"]["role"],
        attestation["reviewer"]["independence_declaration"],
        *attestation["review_scope"],
    ]
    if any(not value.strip() for value in provenance_values):
        _fail("ATTESTATION_BLANK_REVIEWER_PROVENANCE", "$/reviewer")

    try:
        parsed_created_at = datetime.strptime(
            attestation["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
    except ValueError as error:
        _fail("ATTESTATION_CREATED_AT_INVALID", "$/created_at", str(error))
    if parsed_created_at.strftime("%Y-%m-%dT%H:%M:%SZ") != attestation["created_at"]:
        _fail("ATTESTATION_CREATED_AT_INVALID", "$/created_at")

    subject_binding = attestation["subject_binding"]
    schema_binding = attestation["registry_schema_binding"]
    expected_subject_logical = REVIEWED_ARTIFACT_PATHS["V2_REGISTRY"]
    expected_schema_logical = REVIEWED_ARTIFACT_PATHS["REGISTRY_SCHEMA"]
    expected_attestation_schema_logical = REVIEWED_ARTIFACT_PATHS[
        "ATTESTATION_SCHEMA"
    ]
    if subject_binding["path"] != expected_subject_logical:
        _fail("ATTESTATION_SUBJECT_PATH_MISMATCH", "$/subject_binding/path")
    if schema_binding["path"] != expected_schema_logical:
        _fail(
            "ATTESTATION_SCHEMA_PATH_MISMATCH",
            "$/registry_schema_binding/path",
        )
    if subject_path.resolve() != (repository_root / expected_subject_logical).resolve():
        _fail("ATTESTATION_SUBJECT_PATH_MISMATCH", str(subject_path))
    if registry_schema_path.resolve() != (
        repository_root / expected_schema_logical
    ).resolve():
        _fail("ATTESTATION_SCHEMA_PATH_MISMATCH", str(registry_schema_path))
    if attestation_schema_path.resolve() != (
        repository_root / expected_attestation_schema_logical
    ).resolve():
        _fail("ATTESTATION_SCHEMA_DOCUMENT_PATH_MISMATCH", str(attestation_schema_path))

    actual_subject_sha = sha256(subject_path.read_bytes()).hexdigest()
    actual_schema_sha = sha256(registry_schema_path.read_bytes()).hexdigest()
    if subject_binding["sha256"] != actual_subject_sha:
        _fail("ATTESTATION_SUBJECT_SHA_MISMATCH", "$/subject_binding/sha256")
    if schema_binding["sha256"] != actual_schema_sha:
        _fail(
            "ATTESTATION_SCHEMA_SHA_MISMATCH",
            "$/registry_schema_binding/sha256",
        )
    reviewed_bindings = attestation["reviewed_artifact_bindings"]
    if set(reviewed_bindings) != set(REVIEWED_ARTIFACT_PATHS):
        _fail("ATTESTATION_PACKAGE_ROLE_SET_MISMATCH", "$/reviewed_artifact_bindings")
    for role, logical_path in REVIEWED_ARTIFACT_PATHS.items():
        binding = reviewed_bindings[role]
        if binding["path"] != logical_path:
            _fail(
                "ATTESTATION_PACKAGE_PATH_MISMATCH",
                f"$/reviewed_artifact_bindings/{role}/path",
            )
        artifact_path = repository_root / logical_path
        if not artifact_path.is_file():
            _fail("ATTESTATION_PACKAGE_FILE_MISSING", str(artifact_path))
        if binding["sha256"] != sha256(artifact_path.read_bytes()).hexdigest():
            _fail(
                "ATTESTATION_PACKAGE_SHA_MISMATCH",
                f"$/reviewed_artifact_bindings/{role}/sha256",
            )

    counts = attestation["finding_counts"]
    substantive_total = counts["blocker"] + counts["major"] + counts["minor"]
    if attestation["verdict"] == "PASS" and substantive_total != 0:
        _fail("ATTESTATION_PASS_WITH_FINDINGS", "$/finding_counts")
    if (
        attestation["verdict"] == "PASS"
        and attestation["reviewer"]["type"] != "INDEPENDENT_AGENT"
    ):
        _fail("ATTESTATION_IMPLEMENTER_PASS_FORBIDDEN", "$/reviewer/type")
    if counts["total"] != substantive_total:
        _fail("ATTESTATION_FINDING_TOTAL_MISMATCH", "$/finding_counts/total")

    expected_directory = f"sha256-{actual_subject_sha}"
    expected_filename = f"review-{attestation['attestation_id']}.json"
    if attestation_path.parent.name != expected_directory:
        _fail("ATTESTATION_DIRECTORY_MISMATCH", str(attestation_path.parent))
    if attestation_path.name != expected_filename:
        _fail("ATTESTATION_FILENAME_MISMATCH", str(attestation_path))
    expected_attestation_path = (
        repository_root
        / "docs/superpowers/specs/idl/task10/v10/review/attestations"
        / expected_directory
        / expected_filename
    )
    if attestation_path.resolve() != expected_attestation_path.resolve():
        _fail("ATTESTATION_PATH_OUTSIDE_REVIEW_ROOT", str(attestation_path))

    supersedes = attestation.get("supersedes")
    if supersedes is not None:
        superseded_path = repository_root / supersedes["path"]
        if superseded_path.resolve() == expected_attestation_path.resolve():
            _fail("ATTESTATION_SUPERSEDES_SELF", "$/supersedes/path")
        if not superseded_path.is_file():
            _fail("ATTESTATION_SUPERSEDED_FILE_MISSING", str(superseded_path))
        superseded_bytes = superseded_path.read_bytes()
        if sha256(superseded_bytes).hexdigest() != supersedes["sha256"]:
            _fail("ATTESTATION_SUPERSEDED_SHA_MISMATCH", "$/supersedes/sha256")
        try:
            superseded_record = json.loads(superseded_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            _fail("ATTESTATION_SUPERSEDED_CONTENT_INVALID", "$/supersedes", str(error))
        if not isinstance(superseded_record, dict):
            _fail("ATTESTATION_SUPERSEDED_CONTENT_INVALID", "$/supersedes")
        try:
            superseded_canonical = _canonical_json_bytes(superseded_record)
            validate_instance(schema, superseded_record)
        except (TypeError, ValueError) as error:
            _fail("ATTESTATION_SUPERSEDED_CONTENT_INVALID", "$/supersedes", str(error))
        if superseded_canonical != superseded_bytes:
            _fail("ATTESTATION_SUPERSEDED_CONTENT_INVALID", "$/supersedes")
        if superseded_record["subject_binding"]["sha256"] != actual_subject_sha:
            _fail("ATTESTATION_SUPERSEDED_SUBJECT_MISMATCH", "$/supersedes")
        expected_prior_directory = (
            "sha256-" + superseded_record["subject_binding"]["sha256"]
        )
        expected_prior_filename = (
            f"review-{superseded_record['attestation_id']}.json"
        )
        if (
            superseded_path.parent.name != expected_prior_directory
            or superseded_path.name != expected_prior_filename
        ):
            _fail("ATTESTATION_SUPERSEDED_CONTENT_INVALID", "$/supersedes/path")

    if mode == "PREWRITE":
        if attestation_path.exists():
            _fail("ATTESTATION_OVERWRITE_FORBIDDEN", str(attestation_path))
        return

    if not attestation_path.exists():
        _fail("ATTESTATION_READBACK_MISSING", str(attestation_path))
    expected_bytes = (
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
    if attestation_path.read_bytes() != expected_bytes:
        _fail("ATTESTATION_READBACK_CONTENT_MISMATCH", str(attestation_path))


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[7]
    schema_path = (
        Path(__file__).resolve().parent
        / "schema"
        / ("authority-design-decision-registry-v2.schema.json")
    )
    if arguments.self_test:
        result = run_self_test(
            registry_path=arguments.registry,
            schema_path=schema_path,
            repository_root=repository_root,
        )
        print(json.dumps(result, sort_keys=True))
    else:
        validate_registry_file(
            registry_path=arguments.registry,
            schema_path=schema_path,
            repository_root=repository_root,
            markdown_text="NON_NORMATIVE_DERIVED_VIEW",
        )
        print("PACKAGE_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
