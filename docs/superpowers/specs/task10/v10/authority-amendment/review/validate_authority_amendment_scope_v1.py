"""Fail-closed validator for the Task 10 authority-amendment scope package.

This module validates only the pre-authoring scope.  It does not create or
promote authority, IDL, KAT, production, release, or manuscript artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
from hashlib import sha256
from pathlib import Path, PurePosixPath
from typing import NoReturn

REVIEW_RELATIVE = PurePosixPath(
    "docs/superpowers/specs/task10/v10/authority-amendment/review"
)
BASELINE_RELATIVE = REVIEW_RELATIVE / "authority-amendment-baseline-v1.json"
TARGET_MAP_RELATIVE = REVIEW_RELATIVE / "authority-amendment-target-map-v1.json"
TARGET_SCHEMA_RELATIVE = (
    REVIEW_RELATIVE / "schema/authority-amendment-target-map-v1.schema.json"
)
PREDECESSOR_RELATIVE = PurePosixPath(
    "docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md"
)
REGISTRY_RELATIVE = PurePosixPath(
    "docs/superpowers/specs/idl/task10/v10/review/"
    "authority-design-decision-registry-v2.json"
)

EXPECTED_DECISION_IDS = tuple(
    f"T10-G18-DD-{ordinal:03d}" for ordinal in range(1, 24)
)
EXPECTED_TOP_LEVEL_KEYS = {
    "authoring_guard_contract",
    "decision_targets",
    "effect",
    "format",
    "lifecycle_status",
    "normative_projection_contract",
    "predecessor_authority_binding",
    "required_decision_count",
    "review_input_bindings",
    "stop_boundary",
    "transfer_rule",
    "write_scope",
}
EXPECTED_TARGET_KEYS = {
    "authority_anchor",
    "authoring_guard_sha256",
    "decision_id",
    "forbidden_expansion",
    "mode",
    "negative_mutation",
    "normative_delta_summary",
    "normative_projection_sha256",
    "post_state",
    "pre_state",
    "preserve_clause",
    "registry_pointer",
}
EXPECTED_CURRENT_OUTPUTS = (
    "docs/superpowers/plans/2026-08-30-task10-authority-prose-amendment-exact-review.md",
    "docs/superpowers/specs/task10/v10/authority-amendment/review/authority-amendment-scope-addendum-v1.md",
    "docs/superpowers/specs/task10/v10/authority-amendment/review/authority-amendment-baseline-v1.json",
    "docs/superpowers/specs/task10/v10/authority-amendment/review/authority-amendment-target-map-v1.json",
    "docs/superpowers/specs/task10/v10/authority-amendment/review/schema/authority-amendment-target-map-v1.schema.json",
    "docs/superpowers/specs/task10/v10/authority-amendment/review/validate_authority_amendment_scope_v1.py",
    "tests/task10/test_authority_amendment_scope_v1.py",
)
EXPECTED_FUTURE_OUTPUTS = (
    "docs/superpowers/specs/2026-08-30-task10-deny-by-default-provider-proof-design-g18-authority-candidate.md",
    "docs/superpowers/specs/task10/v10/authority-amendment/authority-prose-amendment-result-v1.json",
    "docs/superpowers/specs/task10/v10/authority-amendment/build_authority_prose_candidate_v1.py",
    "docs/superpowers/specs/task10/v10/authority-amendment/validate_authority_prose_candidate_v1.py",
    "tests/task10/test_authority_prose_amendment_v1.py",
)
EXPECTED_BASELINE_FILE_MODE = 0o644
IDENTITY_TREE_RECORD_FORMAT = (
    "UTF8_PATH_NUL_REGULAR_NUL_MODE_OCTAL_NUL_SHA256_LF_SORTED_BY_PATH"
)
EXPECTED_STOP = {
    "authority_idl_allowed": False,
    "implementation_allowed": False,
    "kats_allowed": False,
    "machine_stop_decision": "STOP_BEFORE_AUTHORITY_IDL_AND_KATS",
}
EXPECTED_TRANSFER_RULE = (
    "SELF_CONTAINED_NORMATIVE_RESTATEMENT_REQUIRED; "
    "IDS_HASHES_AND_RULE_PROJECTIONS_ARE_PROVENANCE_ONLY"
)
EXPECTED_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"
EXPECTED_SCHEMA_ID = "selcal.task10.g18.authority-amendment-target-map.v1"
EXPECTED_AUTHORING_GUARD_FIELDS = (
    "forbidden_expansion",
    "negative_mutation",
    "preserve_clause",
)
EXPECTED_AUTHORING_GUARD_CONTRACT = {
    "algorithm": "SHA-256",
    "canonicalization": "UTF8_JSON_SORT_KEYS_INDENT_2_TRAILING_LF",
    "enforcement": "PER_DECISION_EXPECTED_DIGEST_FIXED_IN_SCOPE_VALIDATOR",
    "fields": list(EXPECTED_AUTHORING_GUARD_FIELDS),
}
EXPECTED_AUTHORING_GUARD_DIGESTS = {
    "T10-G18-DD-001": "a443a27b891f65c35e79961445aa1e6007f17a6cc90cf41713f4af86dd18a7d0",
    "T10-G18-DD-002": "0574db27b1458287bff39eb56b495609a924abaa531e2e98bc8d9c88f246d9aa",
    "T10-G18-DD-003": "0d7e8c429df60f4193bf0c53eb33fd5f197981006cd659ae81e1372101102480",
    "T10-G18-DD-004": "e3a4e204afb76e593ea6dc2bdf45468ab850019b4e6af1f2a338be0e28670ee2",
    "T10-G18-DD-005": "636d5755bbe22ae28a200719685b66b45ac81cf24ee31606fd28df4bd4a07047",
    "T10-G18-DD-006": "07667b5dd68ad14edc4ae719a0d27a33ac2a2d9141d9778010d4d2d1c811b28f",
    "T10-G18-DD-007": "b753db7ed7cfeca901b7a1d3bb2150e73bbedfb1f880b9b014344cd861f753a3",
    "T10-G18-DD-008": "93bd06c7811a215335d3c4aaa6e31d98996b0a1e0f2adcaf43fde90699e67c0b",
    "T10-G18-DD-009": "1b7af46b42f159fa428141c13fffcb9bae2735a0061e5edb1bb183e7d6de212d",
    "T10-G18-DD-010": "8be9bcef7dfd32405e3277d3f0d4a985a190cf1418ec4e462a89da4ef084cae0",
    "T10-G18-DD-011": "4cb004e9212a0c5ef3066b097a3656adba93a6f7c63eed8f191fc5947bfd95b2",
    "T10-G18-DD-012": "28d4e35cc75dadee727bd88b481c3fa71b6952ae2f59f3206b05ddc0c75af00f",
    "T10-G18-DD-013": "c14e96d49ca47ba9835dd507c3fbbeef9002636d85488506a5edb61c448d6479",
    "T10-G18-DD-014": "fbffbc4142c7a21ea2163131f132687db8673daca48e0218e5a8861e2517157a",
    "T10-G18-DD-015": "70a9d8ffebcded8294a5c95d06fe8f454fc636772a9b6d4f1f7f17afca66c119",
    "T10-G18-DD-016": "eba157c6b7e2628f9e80997c03b1bb41a611b078ac14272433508ca97df6ebb3",
    "T10-G18-DD-017": "580ae2a435637c4984494ffa759f5ead740d87c389a27476c327113ad78987cb",
    "T10-G18-DD-018": "3dd28403661634e8450b51c10052dc8c590abce4531e4d7baa8f0d33afd53c3e",
    "T10-G18-DD-019": "0c7329c6b0f51b05e2a2d9e76194eb2aafbd1cba656ed50a467cef595471ec0e",
    "T10-G18-DD-020": "58af7c4ceb3b46db47abbbca958cc5f0df00ec3c690b544ad9f1974c8010797c",
    "T10-G18-DD-021": "b0226565e51e3011464c6a3db19171fef75a2f2176be6c9f15a7467fa132adb2",
    "T10-G18-DD-022": "ba886eb7c4264fbf1787852b579a2295bc4556a10e3c5be6568f724f40cd19b3",
    "T10-G18-DD-023": "1bfc738d45cbc89db77140ff420cb7b78ee9e4bc3eb585180215a03894efcf8a",
}
EXPECTED_PROJECTION_FIELDS = (
    "affected_owner_paths",
    "exact_chosen_wire_or_matrix",
    "expected_rl_universe_effect",
    "negative_mutations",
    "reference_contract",
)
EXPECTED_PROJECTION_CONTRACT = {
    "algorithm": "SHA-256",
    "canonicalization": "UTF8_JSON_SORT_KEYS_INDENT_2_TRAILING_LF",
    "fields": list(EXPECTED_PROJECTION_FIELDS),
    "future_candidate_binding": (
        "EACH_SELF_CONTAINED_NORMATIVE_BLOCK_MUST_REPRODUCE_THIS_PROJECTION"
    ),
}
EXPECTED_WRITE_SCOPE_KEYS = {
    "current_scope_outputs",
    "future_candidate_outputs",
    "modify_existing",
    "prior_downstream_plan_status",
    "protected_path_patterns",
}
EXPECTED_PROTECTED_PATTERNS = (
    "docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md",
    "docs/superpowers/specs/idl/task10/v10/review/**",
    "docs/superpowers/specs/fixtures/**",
    "src/**",
    "tests/** except the two exact allowlisted Task10 scope/candidate test paths",
    "**/*idl*",
    "**/*kat*",
    "**/*ui*",
    "**/*release*",
    "**/*manuscript*",
)
EXPECTED_DECISION_ROUTES = {
    **{
        f"T10-G18-DD-{ordinal:03d}": (
            "#### 5.6.3 Derived reference classification and runtime graph",
            "NEW_NORMATIVE_DECISION",
        )
        for ordinal in (*range(2, 12), 13, 14, 18, 20, 22, 23)
    },
    "T10-G18-DD-001": (
        "#### 5.6.1 Closed literal and label universes",
        "CLARIFY_EXISTING_AUTHORITY",
    ),
    "T10-G18-DD-012": (
        "#### 5.6.3 Derived reference classification and runtime graph",
        "CLARIFY_EXISTING_AUTHORITY",
    ),
    "T10-G18-DD-015": (
        "#### 5.6.6 Closed replacements for former open records",
        "NEW_NORMATIVE_DECISION",
    ),
    "T10-G18-DD-016": (
        "#### 5.6.6 Closed replacements for former open records",
        "NEW_NORMATIVE_DECISION",
    ),
    "T10-G18-DD-017": (
        "#### 5.6.1 Closed literal and label universes",
        "CLARIFY_EXISTING_AUTHORITY",
    ),
    "T10-G18-DD-019": (
        "#### 5.6.1 Closed literal and label universes",
        "CLARIFY_EXISTING_AUTHORITY",
    ),
    "T10-G18-DD-021": (
        "#### 5.6.5 Label-free value expressions",
        "NEW_NORMATIVE_DECISION",
    ),
}
EXPECTED_BASELINE_FILE_BINDINGS = {
    "SCOPE_PLAN": EXPECTED_CURRENT_OUTPUTS[0],
    "SCOPE_ADDENDUM": EXPECTED_CURRENT_OUTPUTS[1],
    "TARGET_MAP": EXPECTED_CURRENT_OUTPUTS[3],
    "TARGET_MAP_SCHEMA": EXPECTED_CURRENT_OUTPUTS[4],
    "SCOPE_VALIDATOR": EXPECTED_CURRENT_OUTPUTS[5],
    "SCOPE_FOCUSED_TEST": EXPECTED_CURRENT_OUTPUTS[6],
    "AUTHORITY_PREDECESSOR": str(PREDECESSOR_RELATIVE),
    "FROZEN_DOWNSTREAM_DRAFT": (
        "docs/superpowers/plans/2026-08-30-task10-authoritative-provider-idl-implementation.md"
    ),
    "V1_REVIEW_REGISTRY": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-registry-v1.json"
    ),
    "V1_REVIEW_MATRIX": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-matrix-v1.md"
    ),
    "V2_REVIEW_REGISTRY": str(REGISTRY_RELATIVE),
    "V2_REGISTRY_SCHEMA": (
        "docs/superpowers/specs/idl/task10/v10/review/schema/"
        "authority-design-decision-registry-v2.schema.json"
    ),
    "V2_ATTESTATION_SCHEMA": (
        "docs/superpowers/specs/idl/task10/v10/review/schema/"
        "authority-design-decision-review-attestation-v1.schema.json"
    ),
    "V2_MIGRATOR": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "migrate_authority_decision_registry_v1_to_v2.py"
    ),
    "V2_VALIDATOR": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "validate_authority_review_package_v2.py"
    ),
    "V2_INDEX": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-design-decision-index-v2.md"
    ),
    "V2_ATTESTATION_README": (
        "docs/superpowers/specs/idl/task10/v10/review/attestations/README.md"
    ),
    "V2_FOCUSED_TEST": "tests/task10/test_authority_review_package_v2.py",
    "V2_PLAN": (
        "docs/superpowers/plans/"
        "2026-08-30-task10-authority-review-package-v2-quality-closure.md"
    ),
    "V2_SCOPE": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-review-package-v2-scope-addendum.md"
    ),
    "V2_BASELINE": (
        "docs/superpowers/specs/idl/task10/v10/review/"
        "authority-review-package-v2-baseline.json"
    ),
    "V2_SPEC_ATTESTATION": (
        "docs/superpowers/specs/idl/task10/v10/review/attestations/"
        "sha256-77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5/"
        "review-registry-v2-spec-exact-review-round4-20260830.json"
    ),
    "V2_QUALITY_ATTESTATION": (
        "docs/superpowers/specs/idl/task10/v10/review/attestations/"
        "sha256-77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5/"
        "review-data-code-quality-review-20260830-004.json"
    ),
    "OWNER_INVENTORY_00_20": (
        "docs/superpowers/specs/idl/task10/v10/review/owner-inventory-00-20.json"
    ),
    "OWNER_INVENTORY_21_44": (
        "docs/superpowers/specs/idl/task10/v10/review/owner-inventory-21-44.json"
    ),
    "OWNER_INVENTORY_45_65": (
        "docs/superpowers/specs/idl/task10/v10/review/owner-inventory-45-65.json"
    ),
    "INVENTORY_GAP_LEDGER": (
        "docs/superpowers/specs/idl/task10/v10/review/inventory-gap-ledger.json"
    ),
    "ADVERSE_PARTIAL_SCHEMA": (
        "docs/superpowers/specs/fixtures/task10-reference-schema-v10.json"
    ),
    "ADVERSE_PARTIAL_SCHEMA_MANIFEST": (
        "docs/superpowers/specs/fixtures/2026-08-30-task10-reference-schema-v10-manifest.md"
    ),
    "ADVERSE_COVERAGE": (
        "docs/superpowers/specs/fixtures/task10-provider-audit-full-kat-coverage.json"
    ),
    "ADVERSE_KAT_MANIFEST": (
        "docs/superpowers/specs/fixtures/2026-08-30-task10-provider-audit-full-kat-manifest.md"
    ),
}
EXPECTED_BASELINE_METADATA = {
    "artifact_status": "HASH_BOUND_SCOPE_BASELINE_NOT_AUTHORITY",
    "baseline_id": "SELCAL-TASK10-G18-AUTHORITY-AMENDMENT-SCOPE-BASELINE-20260830",
    "git_head": "94f993bfd5240739f23dd5f5309a51e51034b962",
    "identity_rule": (
        "Read evidence through component-wise no-follow descriptors; verify fstat "
        "ordinary-file kind, permission mode, stable identity and exact bytes; then "
        "confirm the path still maps to that inode before semantic inputs. The dirty "
        "worktree is preserved; git status is not a content-identity substitute."
    ),
    "machine_stop_decision": "STOP_ON_ANY_BASELINE_HASH_DRIFT",
    "schema": "selcal.task10.g18.authority-amendment-scope-baseline.v1",
    "scope": "SCOPE_REVIEW_ONLY_APPEND_ONLY_SUCCESSOR_PREWRITE",
}
EXPECTED_TREE_ROUTES = {
    "PRODUCTION_SOURCE_TREE": ("src", "**/*"),
    "TEST_TREE": ("tests", "**/*"),
    "V2_REVIEW_TREE": (
        "docs/superpowers/specs/idl/task10/v10/review",
        "**/*",
    ),
}
EXPECTED_REVIEW_INPUTS = {
    "REVIEW_DECISION_INPUT_NOT_AUTHORITY": (
        str(REGISTRY_RELATIVE),
        "77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5",
    ),
    "REGISTRY_SPEC_REVIEW_PASS_NO_PROMOTION": (
        "docs/superpowers/specs/idl/task10/v10/review/attestations/"
        "sha256-77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5/"
        "review-registry-v2-spec-exact-review-round4-20260830.json",
        "1c986a5d8e0325d93f2888bd4f3a8d773c102dc399519c32f32bfe09845ffd7f",
    ),
    "REGISTRY_DATA_CODE_REVIEW_PASS_NO_PROMOTION": (
        "docs/superpowers/specs/idl/task10/v10/review/attestations/"
        "sha256-77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5/"
        "review-data-code-quality-review-20260830-004.json",
        "4d5391d89974850e22caad046fbc30274f4aa31c0c40b3893d52f558e44388d8",
    ),
}


def _fail(code: str, detail: str = "") -> NoReturn:
    suffix = f":{detail}" if detail else ""
    raise ValueError(f"{code}{suffix}")


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


SUPPORTED_SCHEMA_KEYWORDS = {
    "$defs",
    "$id",
    "$ref",
    "$schema",
    "additionalProperties",
    "const",
    "enum",
    "items",
    "maxItems",
    "minItems",
    "minLength",
    "pattern",
    "properties",
    "required",
    "title",
    "type",
    "uniqueItems",
}


def _strict_equal(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right


def _schema_type_matches(value: object, expected: str) -> bool:
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
    _fail("TARGET_SCHEMA_UNSUPPORTED_TYPE", expected)


def validate_schema_document(schema: object) -> None:
    """Reject schema syntax that the local validator does not execute."""

    if not isinstance(schema, dict):
        _fail("TARGET_SCHEMA_DOCUMENT_INVALID", "#")
    if schema.get("$schema") != EXPECTED_SCHEMA_DIALECT:
        _fail("TARGET_SCHEMA_DIALECT_MISMATCH")
    if schema.get("$id") != EXPECTED_SCHEMA_ID:
        _fail("TARGET_SCHEMA_ID_MISMATCH")

    def walk(node: object, path: str) -> None:
        if not isinstance(node, dict):
            _fail("TARGET_SCHEMA_DOCUMENT_INVALID", path)
        unknown = set(node) - SUPPORTED_SCHEMA_KEYWORDS
        if unknown:
            _fail("TARGET_SCHEMA_KEYWORD_UNSUPPORTED", f"{path}:{sorted(unknown)}")
        for container_name in ("$defs", "properties"):
            container = node.get(container_name, {})
            if not isinstance(container, dict):
                _fail("TARGET_SCHEMA_DOCUMENT_INVALID", f"{path}/{container_name}")
            for name, child in container.items():
                walk(child, f"{path}/{container_name}/{name}")
        items = node.get("items")
        if items is not None:
            walk(items, f"{path}/items")
        if "additionalProperties" in node and not isinstance(
            node["additionalProperties"], bool
        ):
            _fail("TARGET_SCHEMA_DOCUMENT_INVALID", f"{path}/additionalProperties")
        if node.get("type") == "object" and node.get("additionalProperties") is not False:
            _fail("TARGET_SCHEMA_OBJECT_OPEN", path)
        required = node.get("required", [])
        if not isinstance(required, list) or not all(
            isinstance(item, str) for item in required
        ):
            _fail("TARGET_SCHEMA_DOCUMENT_INVALID", f"{path}/required")

    walk(schema, "#")


def validate_schema_instance(schema: dict[str, object], instance: object) -> None:
    """Execute the exact supported JSON Schema subset against ``instance``."""

    validate_schema_document(schema)

    def resolve(reference: str) -> dict[str, object]:
        if not reference.startswith("#/"):
            _fail("TARGET_SCHEMA_REF_UNSUPPORTED", reference)
        value: object = schema
        for raw_part in reference[2:].split("/"):
            part = raw_part.replace("~1", "/").replace("~0", "~")
            if not isinstance(value, dict) or part not in value:
                _fail("TARGET_SCHEMA_REF_MISSING", reference)
            value = value[part]
        if not isinstance(value, dict):
            _fail("TARGET_SCHEMA_REF_INVALID", reference)
        return value

    def check(node: dict[str, object], value: object, path: str) -> None:
        reference = node.get("$ref")
        if reference is not None:
            if not isinstance(reference, str):
                _fail("TARGET_SCHEMA_REF_INVALID", path)
            check(resolve(reference), value, path)

        expected_type = node.get("type")
        if expected_type is not None:
            if not isinstance(expected_type, str):
                _fail("TARGET_SCHEMA_DOCUMENT_INVALID", f"{path}/type")
            if not _schema_type_matches(value, expected_type):
                _fail("TARGET_SCHEMA_TYPE_MISMATCH", path)
        if "const" in node and not _strict_equal(value, node["const"]):
            _fail("TARGET_SCHEMA_CONST_MISMATCH", path)
        if "enum" in node:
            choices = node["enum"]
            if not isinstance(choices, list) or not any(
                _strict_equal(value, choice) for choice in choices
            ):
                _fail("TARGET_SCHEMA_ENUM_MISMATCH", path)

        if isinstance(value, dict):
            required = node.get("required", [])
            if not isinstance(required, list):
                _fail("TARGET_SCHEMA_DOCUMENT_INVALID", f"{path}/required")
            for name in required:
                if name not in value:
                    _fail("TARGET_SCHEMA_REQUIRED_MISSING", f"{path}/{name}")
            properties = node.get("properties", {})
            if not isinstance(properties, dict):
                _fail("TARGET_SCHEMA_DOCUMENT_INVALID", f"{path}/properties")
            for name, child in properties.items():
                if name in value:
                    if not isinstance(child, dict):
                        _fail("TARGET_SCHEMA_DOCUMENT_INVALID", f"{path}/{name}")
                    check(child, value[name], f"{path}/{name}")
            if node.get("additionalProperties") is False:
                extra = set(value) - set(properties)
                if extra:
                    _fail("TARGET_SCHEMA_ADDITIONAL_PROPERTY", f"{path}:{sorted(extra)}")

        if isinstance(value, list):
            minimum = node.get("minItems")
            maximum = node.get("maxItems")
            if minimum is not None and (
                not isinstance(minimum, int) or len(value) < minimum
            ):
                _fail("TARGET_SCHEMA_MIN_ITEMS", path)
            if maximum is not None and (
                not isinstance(maximum, int) or len(value) > maximum
            ):
                _fail("TARGET_SCHEMA_MAX_ITEMS", path)
            if node.get("uniqueItems") is True:
                encoded = [canonical_json_bytes(item) for item in value]
                if len(encoded) != len(set(encoded)):
                    _fail("TARGET_SCHEMA_UNIQUE_ITEMS", path)
            item_schema = node.get("items")
            if item_schema is not None:
                if not isinstance(item_schema, dict):
                    _fail("TARGET_SCHEMA_DOCUMENT_INVALID", f"{path}/items")
                for index, child in enumerate(value):
                    check(item_schema, child, f"{path}/{index}")

        if isinstance(value, str):
            minimum_length = node.get("minLength")
            if minimum_length is not None and (
                not isinstance(minimum_length, int) or len(value) < minimum_length
            ):
                _fail("TARGET_SCHEMA_MIN_LENGTH", path)
            pattern = node.get("pattern")
            if pattern is not None and (
                not isinstance(pattern, str) or re.search(pattern, value) is None
            ):
                _fail("TARGET_SCHEMA_PATTERN", path)

    check(schema, instance, "$")


def _digest_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def _repository_path_stat(
    repository_root: Path,
    relative: str,
    *,
    symlink_code: str,
    kind_code: str,
    leaf_kind: str,
) -> os.stat_result:
    """Return an lstat identity after rejecting every repository symlink hop."""

    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or relative in {"", "."}:
        _fail(kind_code, relative)
    root = repository_root.absolute()
    try:
        root_stat = os.lstat(root)
    except OSError as error:
        _fail(kind_code, f"{relative}:{error}")
    if stat.S_ISLNK(root_stat.st_mode):
        _fail(symlink_code, ".")
    if not stat.S_ISDIR(root_stat.st_mode):
        _fail(kind_code, ".")

    current = root
    value = root_stat
    for index, part in enumerate(pure.parts):
        current /= part
        try:
            value = os.lstat(current)
        except OSError as error:
            _fail(kind_code, f"{relative}:{error}")
        current_relative = current.relative_to(root).as_posix()
        if stat.S_ISLNK(value.st_mode):
            _fail(symlink_code, current_relative)
        is_leaf = index == len(pure.parts) - 1
        if not is_leaf and not stat.S_ISDIR(value.st_mode):
            _fail(kind_code, current_relative)
    if leaf_kind == "regular" and not stat.S_ISREG(value.st_mode):
        _fail(kind_code, relative)
    if leaf_kind == "directory" and not stat.S_ISDIR(value.st_mode):
        _fail(kind_code, relative)
    if leaf_kind not in {"any", "directory", "regular"}:
        _fail("INTERNAL_LEAF_KIND_INVALID", leaf_kind)
    return value


def _classify_open_failure(
    parent_fd: int,
    component: str,
    *,
    relative: str,
    symlink_code: str,
    kind_code: str,
) -> NoReturn:
    try:
        value = os.stat(component, dir_fd=parent_fd, follow_symlinks=False)
    except OSError as error:
        _fail(kind_code, f"{relative}:{error}")
    if stat.S_ISLNK(value.st_mode):
        _fail(symlink_code, relative)
    _fail(kind_code, relative)


def _open_repository_regular_file_no_follow(
    repository_root: Path,
    relative: str,
    *,
    symlink_code: str,
    kind_code: str,
) -> int:
    """Open a repository file without following any repository-relative link."""

    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or relative in {"", "."}:
        _fail(kind_code, relative)
    no_follow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if no_follow is None or directory is None:
        _fail("NOFOLLOW_DESCRIPTOR_OPEN_UNAVAILABLE")
    close_on_exec = getattr(os, "O_CLOEXEC", 0)
    directory_flags = os.O_RDONLY | no_follow | directory | close_on_exec
    file_flags = os.O_RDONLY | no_follow | close_on_exec

    root = repository_root.absolute()
    try:
        parent_fd = os.open(root, directory_flags)
    except OSError as error:
        try:
            value = os.lstat(root)
        except OSError:
            _fail(kind_code, f"{relative}:{error}")
        if stat.S_ISLNK(value.st_mode):
            _fail(symlink_code, ".")
        _fail(kind_code, f"{relative}:{error}")

    try:
        for index, component in enumerate(pure.parts[:-1]):
            current = PurePosixPath(*pure.parts[: index + 1]).as_posix()
            try:
                next_fd = os.open(component, directory_flags, dir_fd=parent_fd)
            except OSError:
                _classify_open_failure(
                    parent_fd,
                    component,
                    relative=current,
                    symlink_code=symlink_code,
                    kind_code=kind_code,
                )
            os.close(parent_fd)
            parent_fd = next_fd
        try:
            file_fd = os.open(pure.parts[-1], file_flags, dir_fd=parent_fd)
        except OSError:
            _classify_open_failure(
                parent_fd,
                pure.parts[-1],
                relative=relative,
                symlink_code=symlink_code,
                kind_code=kind_code,
            )
    finally:
        os.close(parent_fd)
    try:
        value = os.fstat(file_fd)
        if not stat.S_ISREG(value.st_mode):
            _fail(kind_code, relative)
    except BaseException:
        os.close(file_fd)
        raise
    return file_fd


def _read_fd_bytes(file_descriptor: int) -> bytes:
    os.lseek(file_descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        chunk = os.read(file_descriptor, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _stable_file_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        stat.S_IFMT(value.st_mode),
        stat.S_IMODE(value.st_mode),
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _read_repository_regular_file(
    repository_root: Path,
    relative: str,
    *,
    symlink_code: str,
    kind_code: str,
    drift_code: str,
) -> tuple[bytes, os.stat_result]:
    """Read one stable fd snapshot and prove the path still maps to that inode."""

    file_fd = _open_repository_regular_file_no_follow(
        repository_root,
        relative,
        symlink_code=symlink_code,
        kind_code=kind_code,
    )
    try:
        before = os.fstat(file_fd)
        data = _read_fd_bytes(file_fd)
        after = os.fstat(file_fd)
    finally:
        os.close(file_fd)
    if _stable_file_identity(before) != _stable_file_identity(after):
        _fail(drift_code, relative)
    if len(data) != after.st_size:
        _fail(drift_code, relative)

    current_fd = _open_repository_regular_file_no_follow(
        repository_root,
        relative,
        symlink_code=symlink_code,
        kind_code=kind_code,
    )
    try:
        current = os.fstat(current_fd)
    finally:
        os.close(current_fd)
    if _stable_file_identity(after) != _stable_file_identity(current):
        _fail(drift_code, relative)
    return data, after


def _identity_record(relative: str, value: os.stat_result, data: bytes) -> bytes:
    mode = f"{stat.S_IMODE(value.st_mode):04o}"
    return (
        relative
        + "\0REGULAR\0"
        + mode
        + "\0"
        + _digest_bytes(data)
        + "\n"
    ).encode("utf-8")


def load_baseline(path: Path) -> dict[str, object]:
    absolute = path.absolute()
    repository_root = absolute
    for _ in BASELINE_RELATIVE.parts:
        repository_root = repository_root.parent
    expected = repository_root / BASELINE_RELATIVE
    if absolute != expected:
        _fail("BASELINE_INVALID", str(path))
    data, value_stat = _read_repository_regular_file(
        repository_root,
        str(BASELINE_RELATIVE),
        symlink_code="BASELINE_SYMLINK_FORBIDDEN",
        kind_code="BASELINE_INVALID",
        drift_code="BASELINE_HASH_DRIFT",
    )
    if stat.S_IMODE(value_stat.st_mode) != EXPECTED_BASELINE_FILE_MODE:
        _fail("BASELINE_FILE_MODE_DRIFT", str(BASELINE_RELATIVE))
    try:
        value = json.loads(data.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        _fail("BASELINE_INVALID", str(error))
    if not isinstance(value, dict) or canonical_json_bytes(value) != data:
        _fail("BASELINE_NOT_CANONICAL")
    return value


def read_semantic_json_bytes(data: bytes, logical_path: str) -> dict[str, object]:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        _fail("SEMANTIC_JSON_INVALID", f"{logical_path}:{error}")
    if not isinstance(value, dict):
        _fail("SEMANTIC_JSON_NOT_OBJECT", logical_path)
    if canonical_json_bytes(value) != data:
        _fail("SEMANTIC_JSON_NOT_CANONICAL", logical_path)
    return value


def _tree_state(repository_root: Path, root: str, glob: str) -> tuple[int, str]:
    tree_root = repository_root / root
    _repository_path_stat(
        repository_root,
        root,
        symlink_code="BASELINE_TREE_SYMLINK_FORBIDDEN",
        kind_code="BASELINE_TREE_FILE_KIND_DRIFT",
        leaf_kind="directory",
    )
    paths: list[tuple[str, bytes, os.stat_result]] = []
    for path in sorted(tree_root.glob(glob)):
        relative = path.relative_to(repository_root).as_posix()
        if "__pycache__" in path.parts:
            continue
        value = _repository_path_stat(
            repository_root,
            relative,
            symlink_code="BASELINE_TREE_SYMLINK_FORBIDDEN",
            kind_code="BASELINE_TREE_FILE_KIND_DRIFT",
            leaf_kind="any",
        )
        if stat.S_ISREG(value.st_mode):
            data, stable_value = _read_repository_regular_file(
                repository_root,
                relative,
                symlink_code="BASELINE_TREE_SYMLINK_FORBIDDEN",
                kind_code="BASELINE_TREE_FILE_KIND_DRIFT",
                drift_code="BASELINE_TREE_IDENTITY_DRIFT",
            )
            paths.append((relative, data, stable_value))
        elif not stat.S_ISDIR(value.st_mode):
            _fail("BASELINE_TREE_FILE_KIND_DRIFT", relative)
    records = b"".join(
        _identity_record(relative, value, data)
        for relative, data, value in paths
    )
    return len(paths), _digest_bytes(records)


def git_nonignored_paths(repository_root: Path) -> tuple[str, ...]:
    """Return Git's exact tracked-plus-untracked, non-ignored file inventory."""

    try:
        raw = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=repository_root,
            check=True,
            capture_output=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        _fail("DENY_BY_DEFAULT_INVENTORY_UNAVAILABLE", str(error))
    try:
        paths = tuple(sorted(part.decode("utf-8") for part in raw.split(b"\0") if part))
    except UnicodeDecodeError as error:
        _fail("DENY_BY_DEFAULT_PATH_ENCODING_INVALID", str(error))
    if len(paths) != len(set(paths)):
        _fail("DENY_BY_DEFAULT_PATH_SET_MISMATCH", "duplicate")
    for path in paths:
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts or path in {"", "."}:
            _fail("DENY_BY_DEFAULT_PATH_INVALID", path)
        _repository_path_stat(
            repository_root,
            path,
            symlink_code="DENY_BY_DEFAULT_SYMLINK_FORBIDDEN",
            kind_code="DENY_BY_DEFAULT_PATH_INVALID",
            leaf_kind="regular",
        )
    return paths


def deny_by_default_state(repository_root: Path) -> dict[str, object]:
    """Hash every non-ignored repository file outside the seven current outputs."""

    all_paths = git_nonignored_paths(repository_root)
    if not set(EXPECTED_CURRENT_OUTPUTS).issubset(all_paths):
        _fail("CURRENT_OUTPUT_SET_MISMATCH")
    paths = tuple(path for path in all_paths if path not in EXPECTED_CURRENT_OUTPUTS)
    path_set_bytes = ("\n".join(paths) + "\n").encode("utf-8")
    records = b""
    for path in paths:
        data, value = _read_repository_regular_file(
            repository_root,
            path,
            symlink_code="DENY_BY_DEFAULT_SYMLINK_FORBIDDEN",
            kind_code="DENY_BY_DEFAULT_PATH_INVALID",
            drift_code="DENY_BY_DEFAULT_HASH_DRIFT",
        )
        records += _identity_record(path, value, data)
    return {
        "excluded_current_outputs": list(EXPECTED_CURRENT_OUTPUTS),
        "file_count": len(paths),
        "inventory": "GIT_LS_FILES_CACHED_AND_OTHERS_EXCLUDE_STANDARD_NUL",
        "path_set_sha256": _digest_bytes(path_set_bytes),
        "tree_record_format": IDENTITY_TREE_RECORD_FORMAT,
        "tree_sha256": _digest_bytes(records),
    }


def verify_deny_by_default_manifest(
    repository_root: Path, baseline: dict[str, object]
) -> None:
    manifest = baseline.get("deny_by_default_manifest")
    if not isinstance(manifest, dict) or set(manifest) != {
        "excluded_current_outputs",
        "file_count",
        "inventory",
        "path_set_sha256",
        "tree_record_format",
        "tree_sha256",
    }:
        _fail("DENY_BY_DEFAULT_MANIFEST_SHAPE_MISMATCH")
    actual = deny_by_default_state(repository_root)
    path_keys = {
        "excluded_current_outputs",
        "file_count",
        "inventory",
        "path_set_sha256",
        "tree_record_format",
    }
    if any(manifest[key] != actual[key] for key in path_keys):
        _fail("DENY_BY_DEFAULT_PATH_SET_MISMATCH")
    if manifest["tree_sha256"] != actual["tree_sha256"]:
        _fail("DENY_BY_DEFAULT_HASH_DRIFT")


def verify_baseline(
    repository_root: Path, baseline: dict[str, object]
) -> dict[str, bytes]:
    expected_keys = {
        "artifact_status",
        "baseline_id",
        "deny_by_default_manifest",
        "expected_absent_outputs",
        "files",
        "git_head",
        "identity_rule",
        "machine_stop_decision",
        "protected_trees",
        "schema",
        "scope",
    }
    if set(baseline) != expected_keys:
        _fail("BASELINE_SHAPE_MISMATCH")
    for key, expected in EXPECTED_BASELINE_METADATA.items():
        if baseline[key] != expected:
            if key == "git_head":
                _fail("BASELINE_GIT_HEAD_MISMATCH")
            _fail("BASELINE_METADATA_MISMATCH", key)
    try:
        actual_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        _fail("BASELINE_GIT_HEAD_UNAVAILABLE", str(error))
    if actual_head != baseline["git_head"]:
        _fail("BASELINE_GIT_HEAD_MISMATCH")
    verify_deny_by_default_manifest(repository_root, baseline)

    files = baseline["files"]
    if not isinstance(files, list) or len(files) != 31:
        _fail("BASELINE_FILE_SET_MISMATCH")
    bindings = {
        entry.get("logical_role"): entry.get("path")
        for entry in files
        if isinstance(entry, dict)
        and set(entry) == {"logical_role", "path", "sha256"}
    }
    if bindings != EXPECTED_BASELINE_FILE_BINDINGS or len(bindings) != len(files):
        _fail("BASELINE_FILE_BINDING_MISMATCH")
    verified_bytes: dict[str, bytes] = {}
    for entry in files:
        if set(entry) != {"logical_role", "path", "sha256"}:
            _fail("BASELINE_FILE_ENTRY_MISMATCH")
        data, value = _read_repository_regular_file(
            repository_root,
            entry["path"],
            symlink_code="BASELINE_SYMLINK_FORBIDDEN",
            kind_code="BASELINE_HASH_DRIFT",
            drift_code="BASELINE_HASH_DRIFT",
        )
        if stat.S_IMODE(value.st_mode) != EXPECTED_BASELINE_FILE_MODE:
            _fail("BASELINE_FILE_MODE_DRIFT", entry["path"])
        if _digest_bytes(data) != entry["sha256"]:
            _fail("BASELINE_HASH_DRIFT", entry["path"])
        verified_bytes[entry["path"]] = data

    trees = baseline["protected_trees"]
    if not isinstance(trees, list) or len(trees) != 3:
        _fail("BASELINE_TREE_SET_MISMATCH")
    routes: dict[str, tuple[str, str]] = {}
    for entry in trees:
        if set(entry) != {"file_count", "glob", "logical_role", "root", "sha256"}:
            _fail("BASELINE_TREE_ENTRY_MISMATCH")
        if entry["logical_role"] in routes:
            _fail("BASELINE_TREE_SET_MISMATCH")
        routes[entry["logical_role"]] = (entry["root"], entry["glob"])
        count, digest = _tree_state(repository_root, entry["root"], entry["glob"])
        if count != entry["file_count"] or digest != entry["sha256"]:
            _fail("BASELINE_TREE_DRIFT", entry["logical_role"])
    if routes != EXPECTED_TREE_ROUTES:
        _fail("BASELINE_TREE_BINDING_MISMATCH")

    absent = baseline["expected_absent_outputs"]
    if tuple(absent) != EXPECTED_FUTURE_OUTPUTS:
        _fail("BASELINE_ABSENT_SET_MISMATCH")
    verify_future_outputs_absent(repository_root, absent)
    return verified_bytes


def verify_future_outputs_absent(
    repository_root: Path, relatives: object
) -> None:
    """Treat dangling leaves and symlinked ancestors as occupied output paths."""

    if not isinstance(relatives, list | tuple) or not all(
        isinstance(relative, str) for relative in relatives
    ):
        _fail("BASELINE_ABSENT_SET_MISMATCH")
    root = repository_root.absolute()
    try:
        root_stat = os.lstat(root)
    except OSError:
        _fail("PREWRITE_OUTPUT_ALREADY_EXISTS", ".")
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        _fail("PREWRITE_OUTPUT_ALREADY_EXISTS", ".")
    for relative in relatives:
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or relative in {"", "."}:
            _fail("BASELINE_ABSENT_SET_MISMATCH", relative)
        current = root
        for index, part in enumerate(pure.parts):
            current /= part
            if not os.path.lexists(current):
                break
            try:
                value = os.lstat(current)
            except OSError:
                _fail("PREWRITE_OUTPUT_ALREADY_EXISTS", relative)
            is_leaf = index == len(pure.parts) - 1
            if stat.S_ISLNK(value.st_mode) or is_leaf:
                _fail("PREWRITE_OUTPUT_ALREADY_EXISTS", relative)
            if not stat.S_ISDIR(value.st_mode):
                _fail("PREWRITE_OUTPUT_ALREADY_EXISTS", relative)


def _verify_baseline(
    repository_root: Path, baseline: dict[str, object]
) -> dict[str, bytes]:
    """Backward-compatible private alias used by no external authority."""

    return verify_baseline(repository_root, baseline)


def validate_review_input_bytes(
    target_map: dict[str, object], verified_bytes: dict[str, bytes]
) -> dict[str, dict[str, object]]:
    """Bind every parsed review input to the exact bytes already hash-verified."""

    bindings = target_map.get("review_input_bindings")
    if not isinstance(bindings, list) or len(bindings) != 3:
        _fail("REVIEW_INPUT_BINDING_MISMATCH")
    actual_bindings = {
        entry.get("role"): (entry.get("path"), entry.get("sha256"))
        for entry in bindings
        if isinstance(entry, dict) and set(entry) == {"path", "role", "sha256"}
    }
    if actual_bindings != EXPECTED_REVIEW_INPUTS:
        _fail("REVIEW_INPUT_BINDING_MISMATCH")

    parsed: dict[str, dict[str, object]] = {}
    for entry in bindings:
        path = entry["path"]
        data = verified_bytes.get(path)
        if data is None or _digest_bytes(data) != entry["sha256"]:
            _fail("REVIEW_INPUT_HASH_MISMATCH", path)
        parsed[path] = read_semantic_json_bytes(data, path)
    return parsed


def _require_nonblank_strings(target: dict[str, object]) -> None:
    for key in EXPECTED_TARGET_KEYS - {"mode"}:
        value = target[key]
        if not isinstance(value, str) or not value.strip():
            _fail("TARGET_BLANK_FIELD", key)


def validate_target_map(
    target_map: dict[str, object],
    predecessor_text: str,
    registry: dict[str, object],
) -> None:
    if set(target_map) != EXPECTED_TOP_LEVEL_KEYS:
        _fail("TARGET_MAP_SHAPE_MISMATCH")
    if target_map["format"] != "selcal.task10.g18.authority-amendment-target-map.v1":
        _fail("TARGET_MAP_FORMAT_MISMATCH")
    if target_map["lifecycle_status"] != "TARGET_MAP_CANDIDATE_NOT_AUTHORITY":
        _fail("TARGET_MAP_STATUS_MISMATCH")
    if target_map["effect"] != "AUTHORING_SCOPE_ONLY_NO_AUTHORITY_PROMOTION":
        _fail("TARGET_MAP_EFFECT_MISMATCH")
    if target_map["required_decision_count"] != 23:
        _fail("DECISION_COUNT_MISMATCH")
    if target_map["stop_boundary"] != EXPECTED_STOP:
        _fail("STOP_BOUNDARY_MISMATCH")
    if target_map["transfer_rule"] != EXPECTED_TRANSFER_RULE:
        _fail("TRANSFER_RULE_MISMATCH")
    if target_map["authoring_guard_contract"] != EXPECTED_AUTHORING_GUARD_CONTRACT:
        _fail("AUTHORING_GUARD_CONTRACT_MISMATCH")
    if target_map["normative_projection_contract"] != EXPECTED_PROJECTION_CONTRACT:
        _fail("NORMATIVE_PROJECTION_CONTRACT_MISMATCH")

    predecessor = target_map["predecessor_authority_binding"]
    if predecessor != {
        "byte_length": 298339,
        "mutation_forbidden": True,
        "path": str(PREDECESSOR_RELATIVE),
        "sha256": "74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff",
    }:
        _fail("PREDECESSOR_BINDING_MISMATCH")

    bindings = target_map["review_input_bindings"]
    if not isinstance(bindings, list) or len(bindings) != 3:
        _fail("REVIEW_INPUT_BINDING_MISMATCH")
    actual_bindings = {
        entry.get("role"): (entry.get("path"), entry.get("sha256"))
        for entry in bindings
        if isinstance(entry, dict) and set(entry) == {"path", "role", "sha256"}
    }
    if actual_bindings != EXPECTED_REVIEW_INPUTS:
        _fail("REVIEW_INPUT_BINDING_MISMATCH")

    write_scope = target_map["write_scope"]
    if not isinstance(write_scope, dict) or set(write_scope) != EXPECTED_WRITE_SCOPE_KEYS:
        _fail("WRITE_SCOPE_SHAPE_MISMATCH")
    if tuple(write_scope.get("current_scope_outputs", ())) != EXPECTED_CURRENT_OUTPUTS:
        _fail("CURRENT_OUTPUT_SET_MISMATCH")
    if tuple(write_scope.get("future_candidate_outputs", ())) != EXPECTED_FUTURE_OUTPUTS:
        _fail("FUTURE_OUTPUT_SET_MISMATCH")
    if write_scope.get("modify_existing") != []:
        _fail("MODIFY_EXISTING_FORBIDDEN")
    if write_scope.get("prior_downstream_plan_status") != (
        "FROZEN_NONEXECUTABLE_DOWNSTREAM_DRAFT"
    ):
        _fail("DOWNSTREAM_PLAN_STATUS_MISMATCH")
    if tuple(write_scope.get("protected_path_patterns", ())) != (
        EXPECTED_PROTECTED_PATTERNS
    ):
        _fail("PROTECTED_PATH_SET_MISMATCH")

    decisions = target_map["decision_targets"]
    if not isinstance(decisions, list):
        _fail("DECISION_ID_SET_MISMATCH")
    ids = tuple(
        item.get("decision_id") if isinstance(item, dict) else None
        for item in decisions
    )
    if ids != EXPECTED_DECISION_IDS:
        _fail("DECISION_ID_SET_MISMATCH")

    registry_decisions = registry.get("decisions_by_id")
    if not isinstance(registry_decisions, dict) or tuple(sorted(registry_decisions)) != (
        EXPECTED_DECISION_IDS
    ):
        _fail("REGISTRY_DECISION_SET_MISMATCH")
    if registry.get("artifact_state") != "REVIEW_DECISION_INPUT_NOT_AUTHORITY":
        _fail("REGISTRY_STATE_PROMOTION")
    if registry.get("authority_amendment_status") != (
        "AUTHORITY_AMENDMENT_NOT_YET_REVIEWED"
    ):
        _fail("REGISTRY_STATE_PROMOTION")
    if registry.get("machine_stop_decision") != "STOP_BEFORE_AUTHORITY_IDL_AND_KATS":
        _fail("REGISTRY_STATE_PROMOTION")
    if registry.get("scope_boundary") != {
        "authority_idl_allowed": False,
        "kats_allowed": False,
    }:
        _fail("REGISTRY_STATE_PROMOTION")

    for target in decisions:
        if not isinstance(target, dict) or set(target) != EXPECTED_TARGET_KEYS:
            _fail("TARGET_SHAPE_MISMATCH")
        _require_nonblank_strings(target)
        decision_id = target["decision_id"]
        if target["registry_pointer"] != f"/decisions_by_id/{decision_id}":
            _fail("REGISTRY_POINTER_MISMATCH", decision_id)
        if (target["authority_anchor"], target["mode"]) != EXPECTED_DECISION_ROUTES[
            decision_id
        ]:
            _fail("DECISION_ROUTE_MISMATCH", decision_id)
        authoring_guard = {
            field: target[field] for field in EXPECTED_AUTHORING_GUARD_FIELDS
        }
        expected_guard_digest = EXPECTED_AUTHORING_GUARD_DIGESTS[decision_id]
        if target["authoring_guard_sha256"] != expected_guard_digest or _digest_bytes(
            canonical_json_bytes(authoring_guard)
        ) != expected_guard_digest:
            _fail("AUTHORING_GUARD_MISMATCH", decision_id)
        if target["pre_state"] != "REVIEW_DECISION_INPUT_NOT_AUTHORITY" or target[
            "post_state"
        ] != "SUCCESSOR_CANDIDATE_NOT_ADOPTED":
            _fail("TARGET_STATE_MISMATCH", decision_id)
        registry_decision = registry_decisions[decision_id]
        if registry_decision["payload"]["status"] != (
            "APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT"
        ):
            _fail("REGISTRY_DECISION_STATUS_MISMATCH", decision_id)
        expected_summary = registry_decision["payload"][
            "authority_amendment_text_summary"
        ]
        if target["normative_delta_summary"] != expected_summary:
            _fail("DECISION_SUMMARY_MISMATCH", decision_id)
        projection = {
            field: registry_decision["payload"][field]
            for field in EXPECTED_PROJECTION_FIELDS
        }
        if target["normative_projection_sha256"] != _digest_bytes(
            canonical_json_bytes(projection)
        ):
            _fail("NORMATIVE_PROJECTION_MISMATCH", decision_id)
        if predecessor_text.count(target["authority_anchor"]) != 1:
            _fail("AUTHORITY_ANCHOR_COUNT_MISMATCH", decision_id)


def validate_scope_package(repository_root: Path) -> dict[str, object]:
    repository_root = repository_root.resolve()
    baseline = load_baseline(repository_root / BASELINE_RELATIVE)
    verified_bytes = verify_baseline(repository_root, baseline)

    target_map = read_semantic_json_bytes(
        verified_bytes[str(TARGET_MAP_RELATIVE)], str(TARGET_MAP_RELATIVE)
    )
    schema = read_semantic_json_bytes(
        verified_bytes[str(TARGET_SCHEMA_RELATIVE)], str(TARGET_SCHEMA_RELATIVE)
    )
    review_inputs = validate_review_input_bytes(target_map, verified_bytes)
    registry = review_inputs[str(REGISTRY_RELATIVE)]
    predecessor_bytes = verified_bytes[str(PREDECESSOR_RELATIVE)]
    if len(predecessor_bytes) != 298339 or _digest_bytes(predecessor_bytes) != (
        "74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff"
    ):
        _fail("PREDECESSOR_BINDING_MISMATCH")
    try:
        predecessor_text = predecessor_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        _fail("PREDECESSOR_UTF8_INVALID", str(error))

    if schema.get("$id") != EXPECTED_SCHEMA_ID:
        _fail("TARGET_SCHEMA_ID_MISMATCH")
    validate_schema_instance(schema, target_map)

    validate_target_map(target_map, predecessor_text, registry)

    for binding in target_map["review_input_bindings"][1:]:
        attestation = review_inputs[binding["path"]]
        if attestation.get("verdict") != "PASS" or attestation.get("effect") != (
            "NO_AUTHORITY_PROMOTION"
        ):
            _fail("ATTESTATION_EFFECT_MISMATCH", binding["path"])
        if attestation.get("finding_counts") != {
            "blocker": 0,
            "major": 0,
            "minor": 0,
            "total": 0,
        }:
            _fail("ATTESTATION_FINDINGS_MISMATCH", binding["path"])

    return {
        "baseline_files": len(baseline["files"]),
        "decision_targets": len(target_map["decision_targets"]),
        "deny_by_default_files": baseline["deny_by_default_manifest"]["file_count"],
        "future_outputs_absent": len(baseline["expected_absent_outputs"]),
        "positive_package": "PASS",
        "protected_trees": len(baseline["protected_trees"]),
    }


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=None)
    arguments = parser.parse_args()
    repository_root = arguments.repository_root
    if repository_root is None:
        repository_root = Path(__file__).resolve().parents[7]
    result = validate_scope_package(repository_root)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
