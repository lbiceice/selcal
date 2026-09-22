"""Deterministic semantic correction of the frozen Task 10 v2 review input.

This builder creates another review input.  It does not amend authority, create
IDL/KATs, or authorize production implementation.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import stat
from collections import defaultdict
from collections.abc import Mapping
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
V2_BYTES = 4_282_426
V3_BASELINE_PATH = (
    "docs/superpowers/specs/idl/task10/v10/review/v3/"
    "authority-review-package-v3-baseline.json"
)
EXPECTED_V3_BASELINE_SHA256 = (
    "d040bd9ff1377d41e6202a1483662bd9f9a03e04263f5897e1bd4e750bd35de0"
)
V3_SCHEMA_PATH = (
    "docs/superpowers/specs/idl/task10/v10/review/v3/schema/"
    "authority-design-decision-registry-v3.schema.json"
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
DD004_ROLE_OWNER = {
    "PROCESS_LOCAL_IDENTITY_TOKEN": "process_local_identity_tokens",
    "PROJECT_FUNCTION_BINDING": "project_function_bindings",
    "PROJECT_RUNTIME_VALUE": "runtime_values",
    "VALUE_CONTRACT": "value_contracts",
}
DD009_VALUE_ROLE_OWNER = {
    "BOUND_TYPE_MEMBER": "bound_type_members",
    "EXTERNAL_IDENTITY": "external_identities",
    "GENERATED_CALLBACK": "generated_stdlib_callbacks",
    "PROJECT_RUNTIME_VALUE": "runtime_values",
    "VALUE_CONTRACT": "value_contracts",
}
DD009_LOAD_KIND_OWNER = {
    "ATTRIBUTE_BOUND_MEMBER": "bound_type_members",
    "ATTRIBUTE_EXTERNAL_MEMBER": "external_type_members",
    "ATTRIBUTE_GENERATED_ACCESSOR": "generated_field_accessors",
    "ATTRIBUTE_PROJECT_DESCRIPTOR": "project_descriptors",
    "BUILTIN": "external_identities",
    "CLOSURE_CONTRACT": "value_contracts",
    "CLOSURE_VALUE": "runtime_values",
    "EXTERNAL_GLOBAL": "external_identities",
    "PROJECT_GLOBAL": "project_function_bindings",
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
DD009_VALUE_RECORD_PATHS = {
    "CallbackClosureBinding": "closure_cells[*].target_label",
    "CallbackDefaultBinding": "positional_defaults[*].target_label",
    "CallbackKeywordDefaultBinding": "keyword_defaults[*].target_label",
}
PROVIDER_ROLE_OWNER = {
    "EXTERNAL_PYTHON_INTRINSIC": "external_python_intrinsics",
    "EXTERNAL_TYPE_MEMBER": "external_type_members",
    "GENERATED_METHOD": "generated_methods",
    "GENERATED_STDLIB_CALLBACK": "generated_stdlib_callbacks",
    "PROJECT_DESCRIPTOR": "project_descriptors",
    "PROJECT_FUNCTION_BINDING": "project_function_bindings",
}


def _reject_non_finite(value: str) -> NoReturn:
    raise ValueError(f"NON_FINITE_JSON_NUMBER:{value}")


def canonical_json_bytes(value: object) -> bytes:
    text = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    )
    return (text + "\n").encode("utf-8")


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


def _atomic_write_regular_0644(path: Path, data: bytes) -> None:
    absolute = path.absolute()
    parent = absolute.parent
    _assert_no_symlink_ancestry(parent)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(
        os, "O_NOFOLLOW", 0
    )
    directory_fd = os.open(parent, directory_flags)
    temporary_name: str | None = None
    descriptor: int | None = None
    try:
        try:
            existing = os.stat(absolute.name, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        if existing is not None:
            if stat.S_ISLNK(existing.st_mode):
                raise ValueError(f"OUTPUT_PATH_SYMLINK:{path}")
            if not stat.S_ISREG(existing.st_mode):
                raise ValueError(f"OUTPUT_PATH_KIND_MISMATCH:{path}")

        flags = (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        for _ in range(100):
            candidate = f".{absolute.name}.tmp-{secrets.token_hex(12)}"
            try:
                descriptor = os.open(candidate, flags, 0o600, dir_fd=directory_fd)
            except FileExistsError:
                continue
            temporary_name = candidate
            break
        if descriptor is None or temporary_name is None:
            raise ValueError(f"OUTPUT_TEMP_NAME_EXHAUSTED:{path}")

        os.fchmod(descriptor, 0o644)
        remaining = memoryview(data)
        while remaining:
            written = os.write(descriptor, remaining)
            if written <= 0:
                raise ValueError(f"OUTPUT_SHORT_WRITE:{path}")
            remaining = remaining[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        os.replace(
            temporary_name,
            absolute.name,
            src_dir_fd=directory_fd,
            dst_dir_fd=directory_fd,
        )
        temporary_name = None
        os.fsync(directory_fd)
        final = os.stat(absolute.name, dir_fd=directory_fd, follow_symlinks=False)
        if not stat.S_ISREG(final.st_mode) or stat.S_IMODE(final.st_mode) != 0o644:
            raise ValueError(f"OUTPUT_IDENTITY_MISMATCH:{path}")
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=directory_fd)
            except FileNotFoundError:
                pass
        os.close(directory_fd)


def verify_baseline_inputs(repository_root: Path) -> dict[str, bytes]:
    try:
        baseline_bytes = _read_exact_regular_0644(
            repository_root / V3_BASELINE_PATH
        )
    except (OSError, ValueError) as exc:
        raise ValueError("V3_BASELINE_IDENTITY_DRIFT") from exc
    if sha256(baseline_bytes).hexdigest() != EXPECTED_V3_BASELINE_SHA256:
        raise ValueError("V3_BASELINE_IDENTITY_DRIFT")
    baseline = json.loads(
        baseline_bytes.decode("utf-8"), parse_constant=_reject_non_finite
    )
    if canonical_json_bytes(baseline) != baseline_bytes:
        raise ValueError("V3_BASELINE_IDENTITY_DRIFT")
    records = baseline.get("files", [])
    if len(records) != 8:
        raise ValueError("V3_BASELINE_IDENTITY_DRIFT")
    verified: dict[str, bytes] = {}
    for record in records:
        relative = Path(record["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("PREDECESSOR_IDENTITY_DRIFT:unsafe_path")
        try:
            data = _read_exact_regular_0644(repository_root / relative)
        except (OSError, ValueError) as exc:
            raise ValueError(f"PREDECESSOR_IDENTITY_DRIFT:{relative}") from exc
        if (
            record.get("mode") != "0644"
            or len(data) != record.get("bytes")
            or sha256(data).hexdigest() != record.get("sha256")
        ):
            raise ValueError(f"PREDECESSOR_IDENTITY_DRIFT:{relative}")
        verified[relative.as_posix()] = data
    if len(verified) != 8:
        raise ValueError("V3_BASELINE_IDENTITY_DRIFT")
    return verified


def _verify_registry_source_bindings(
    repository_root: Path, registry: dict[str, Any]
) -> None:
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


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label}_NOT_OBJECT")
    return value


def _decision(registry: dict[str, Any], decision_id: str) -> dict[str, Any]:
    return _mapping(registry["decisions_by_id"][decision_id], decision_id)


def _payload(registry: dict[str, Any], decision_id: str) -> dict[str, Any]:
    return _mapping(_decision(registry, decision_id)["payload"], f"{decision_id}_PAYLOAD")


def _exact(registry: dict[str, Any], decision_id: str) -> dict[str, Any]:
    return _mapping(
        _payload(registry, decision_id)["exact_chosen_wire_or_matrix"],
        f"{decision_id}_EXACT",
    )


def _owner(registry: dict[str, Any], owner_table: str) -> dict[str, Any]:
    matches = [
        value
        for value in registry["owners_by_id"].values()
        if value["owner_table"] == owner_table
    ]
    if len(matches) != 1:
        raise ValueError(f"OWNER_LOOKUP_NOT_SINGLETON:{owner_table}")
    return matches[0]


def _discriminator(path: str, value: str) -> dict[str, object]:
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


def _rule_by_target(
    registry: dict[str, Any], rule_ids: list[str], target: str
) -> dict[str, Any]:
    matches = [
        registry["compiled_rules_by_id"][rule_id]
        for rule_id in rule_ids
        if registry["compiled_rules_by_id"][rule_id]["payload"][
            "allowed_target_tables"
        ]
        == [target]
    ]
    if len(matches) != 1:
        raise ValueError(f"RULE_TARGET_LOOKUP_NOT_SINGLETON:{target}")
    return deepcopy(matches[0])


def _replace_strings(value: object, replacements: Mapping[str, str]) -> object:
    if isinstance(value, dict):
        return {
            replacements.get(key, key): _replace_strings(child, replacements)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [_replace_strings(child, replacements) for child in value]
    if isinstance(value, str):
        return replacements.get(value, value)
    return value


def _patch_dd001(registry: dict[str, Any]) -> None:
    payload = _payload(registry, "T10-G18-DD-001")
    payload["authority_amendment_text_summary"] = (
        "Retype ten unique exact paths represented by eleven census rows; the "
        "behavior-slot path occurs in two distinct inventory rows."
    )
    payload["current_fact"] = (
        "Eleven census rows cover ten unique paths because two rows share the "
        "behavior-slot raw-member-identity path."
    )
    payload["neutral_verdict"] = (
        "Preserve all eleven census rows while retyping exactly ten unique paths."
    )


def _patch_dd004(registry: dict[str, Any]) -> None:
    decision = _decision(registry, "T10-G18-DD-004")
    payload = decision["payload"]
    exact = payload["exact_chosen_wire_or_matrix"]
    old_rule_ids = list(decision["compiled_rule_ids"])
    new_rules: list[dict[str, Any]] = []
    source_rules = [
        deepcopy(registry["compiled_rules_by_id"][rule_id])
        for rule_id in old_rule_ids
    ]
    if len(source_rules) != 5:
        raise ValueError("DD004_PREDECESSOR_RULE_COUNT")
    for sequence, (role, target) in enumerate(DD004_ROLE_OWNER.items(), start=1):
        # The v2 collision omitted VALUE_CONTRACT and admitted two forbidden
        # roles, so target lookup is not a sound migration primitive here.
        # All five predecessor rules carry the same evidence and provenance;
        # use one structural seed and replace the complete semantic payload.
        rule = deepcopy(source_rules[0])
        temporary_id = f"TMP-DD004-{sequence:02d}"
        rule["rule_id"] = temporary_id
        rule_payload = rule["payload"]
        rule_payload.update(
            {
                "allowed_target_tables": [target],
                "branch_instance_id": f"TMP-DD004-BR-{sequence:02d}",
                "cardinality": "SCALAR",
                "containing_record": "CapturedEnvironmentRef",
                "field_path": (
                    "comprehension_mappings[*].captured_environment_labels[*].label"
                ),
                "record_discriminator": _discriminator("capture_kind", role),
                "replacement_wire_type": "tuple[R[CapturedEnvironmentRef]]",
                "schema_field_order": 2,
            }
        )
        rule_payload["schema_order_key"].update(
            {"branch_ordinal": sequence, "field_ordinal": 2, "template_ordinal": 1}
        )
        new_rules.append(rule)

    for rule_id in old_rule_ids:
        del registry["compiled_rules_by_id"][rule_id]
    for rule in new_rules:
        registry["compiled_rules_by_id"][rule["rule_id"]] = rule
    decision["compiled_rule_ids"] = [rule["rule_id"] for rule in new_rules]
    decision["design_payload"]["branch_instance_ids"] = [
        rule["payload"]["branch_instance_id"] for rule in new_rules
    ]
    payload["reference_contract"]["owner_tuple"] = list(
        dict.fromkeys(DD004_ROLE_OWNER.values())
    )
    exact["CapturedEnvironmentRef"] = deepcopy(DD004_ROLE_OWNER)
    exact["containing_wire"] = "tuple[R[CapturedEnvironmentRef]]"
    exact["fields"] = ["capture_kind", "capture_name", "label"]
    exact["field_wires"] = {
        "capture_kind": "E[CapturedEnvironmentKind]",
        "capture_name": "S",
        "label": "RL",
    }
    exact["ordering"] = "capture_name strict UTF-8; unique"
    manifest = exact["coverage_compilation_manifest"][0]
    manifest["compiled_rule_ids"] = list(decision["compiled_rule_ids"])
    manifest["compiled_field_paths"] = [
        "comprehension_mappings[*].captured_environment_labels[*].label"
    ] * 4
    payload["expected_rl_universe_effect"]["emitted_reference_rules"] = 4


def _patch_owner_tuples_and_name(registry: dict[str, Any]) -> None:
    dd006 = _payload(registry, "T10-G18-DD-006")
    if "runtime_values" not in dd006["reference_contract"]["owner_tuple"]:
        dd006["reference_contract"]["owner_tuple"].append("runtime_values")
    dd007 = _payload(registry, "T10-G18-DD-007")
    for owner in ("semantic_models", "outcome_contracts"):
        if owner not in dd007["reference_contract"]["owner_tuple"]:
            dd007["reference_contract"]["owner_tuple"].append(owner)
    for key in ("authority_amendment_text_summary", "neutral_verdict"):
        dd007[key] = dd007[key].replace("ProjectAccessRef", "RootFieldAccessRef")


def _patch_value_rules(registry: dict[str, Any]) -> None:
    rules = registry["compiled_rules_by_id"]
    decision = _decision(registry, "T10-G18-DD-009")
    for record, field_path in DD009_VALUE_RECORD_PATHS.items():
        selected = [
            rules[rule_id]
            for rule_id in decision["compiled_rule_ids"]
            if rules[rule_id]["payload"]["containing_record"] == record
        ]
        if len(selected) != len(DD009_VALUE_ROLE_OWNER):
            raise ValueError(f"DD009_VALUE_RULE_COUNT:{record}")
        selected.sort(key=lambda rule: rule["rule_id"])
        for rule, (role, target) in zip(
            selected, DD009_VALUE_ROLE_OWNER.items(), strict=True
        ):
            payload = rule["payload"]
            payload["allowed_target_tables"] = [target]
            payload["field_path"] = field_path
            payload["record_discriminator"] = _discriminator("binding_kind", role)
            payload["branch_instance_id"] = (
                f"TMP-DD009-{record}-{role}"
            )


def _patch_dd009(registry: dict[str, Any]) -> None:
    decision = _decision(registry, "T10-G18-DD-009")
    payload = decision["payload"]
    exact = payload["exact_chosen_wire_or_matrix"]
    _patch_value_rules(registry)
    rules = registry["compiled_rules_by_id"]
    load_rules = [
        rules[rule_id]
        for rule_id in decision["compiled_rule_ids"]
        if rules[rule_id]["payload"]["containing_record"] == "CallbackLoadBinding"
    ]
    if len(load_rules) != 8:
        raise ValueError("DD009_LEGACY_LOAD_RULE_COUNT")
    load_rules.sort(key=lambda rule: rule["rule_id"])
    ninth = deepcopy(load_rules[-1])
    ninth["rule_id"] = "TMP-DD009-LOAD-09"
    ninth["payload"]["branch_instance_id"] = "TMP-DD009-LOAD-BR-09"
    rules[ninth["rule_id"]] = ninth
    load_rules.append(ninth)
    for rule, (kind, target) in zip(
        load_rules, DD009_LOAD_KIND_OWNER.items(), strict=True
    ):
        rule_payload = rule["payload"]
        rule_payload["allowed_target_tables"] = [target]
        rule_payload["cardinality"] = "SCALAR"
        rule_payload["field_path"] = "load_bindings[*].target_label"
        rule_payload["record_discriminator"] = _discriminator("source_kind", kind)
        rule_payload["branch_instance_id"] = f"TMP-DD009-LOAD-{kind}"
    decision["compiled_rule_ids"].append(ninth["rule_id"])
    decision["design_payload"]["branch_instance_ids"].append(
        ninth["payload"]["branch_instance_id"]
    )
    exact["CallbackTarget"] = deepcopy(DD009_VALUE_ROLE_OWNER)
    exact["CallbackLoad"] = deepcopy(DD009_LOAD_KIND_OWNER)
    exact["CallbackLoadSourceKinds"] = deepcopy(DD009_SOURCE_KINDS)
    exact["CallbackLoadPresence"] = {
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
    for manifest in exact["coverage_compilation_manifest"]:
        inventory_path = manifest["inventory_field_path"]
        if inventory_path in set(DD009_VALUE_RECORD_PATHS.values()):
            record = next(
                record
                for record, field_path in DD009_VALUE_RECORD_PATHS.items()
                if field_path == inventory_path
            )
            ids = [
                rule_id
                for rule_id in decision["compiled_rule_ids"]
                if rules[rule_id]["payload"]["containing_record"] == record
            ]
            manifest["compiled_rule_ids"] = ids
            manifest["compiled_field_paths"] = [inventory_path] * len(ids)
        if inventory_path == "load_bindings[*].target_label":
            ids = [rule["rule_id"] for rule in load_rules]
            manifest["compiled_rule_ids"] = ids
            manifest["compiled_field_paths"] = [inventory_path] * len(ids)
    payload["expected_rl_universe_effect"]["emitted_reference_rules"] = 33

    # The old load wrapper admitted project_modules and omitted generated
    # field accessors.  Recompute the closed owner set from the corrected
    # complete rule bodies rather than retaining either stale list.
    owner_union = {
        target
        for rule_id in decision["compiled_rule_ids"]
        for target in rules[rule_id]["payload"]["allowed_target_tables"]
    }
    payload["reference_contract"]["owner_tuple"] = sorted(owner_union)


def _patch_provider_maps(registry: dict[str, Any]) -> None:
    for decision_id in ("T10-G18-DD-011", "T10-G18-DD-016"):
        _exact(registry, decision_id)["ProviderReference"] = deepcopy(
            PROVIDER_ROLE_OWNER
        )


def _sync_changed_coverage_rows(registry: dict[str, Any]) -> None:
    rows_by_key = {
        row["payload"]["row_key"]: row
        for row in registry["coverage_rows_by_id"].values()
    }
    for decision_id in ("T10-G18-DD-004", "T10-G18-DD-009"):
        exact = _exact(registry, decision_id)
        for manifest in exact["coverage_compilation_manifest"]:
            row_key = manifest["row_key"]
            try:
                row = rows_by_key[row_key]
            except KeyError as exc:
                raise ValueError(f"COVERAGE_ROW_KEY_MISSING:{row_key}") from exc
            rule_ids = list(manifest["compiled_rule_ids"])
            row["compiled_rule_ids"] = rule_ids
            target_union = sorted(
                {
                    target
                    for rule_id in rule_ids
                    for target in registry["compiled_rules_by_id"][rule_id]["payload"][
                        "allowed_target_tables"
                    ]
                }
            )
            payload = row["payload"]
            payload["allowed_target_tables"] = target_union
            payload["owner_tuple"] = target_union
            payload["compile_action"]["compiled_rule_count"] = len(rule_ids)

    capture_row = rows_by_key[
        "02:001:project_source_indexes:"
        "comprehension_mappings[*].captured_environment_labels[*]"
    ]["payload"]
    capture_row["compile_action"]["replacement_wire_type"] = (
        "tuple[R[CapturedEnvironmentRef]]"
    )
    capture_row["inventory_discriminator_source"] = "capture_kind"

    for row_key in (
        "29:002:generated_stdlib_callbacks:positional_defaults[*].target_label",
        "29:003:generated_stdlib_callbacks:keyword_defaults[*].target_label",
        "29:004:generated_stdlib_callbacks:closure_cells[*].target_label",
    ):
        payload = rows_by_key[row_key]["payload"]
        payload["compile_action"]["replacement_wire_type"] = (
            "DIRECT_EMBEDDED_BINDING"
        )
        payload["inventory_discriminator_source"] = "binding_kind exact matrix"
    load_payload = rows_by_key[
        "29:005:generated_stdlib_callbacks:load_bindings[*].target_label"
    ]["payload"]
    load_payload["compile_action"]["replacement_wire_type"] = (
        "DIRECT_EMBEDDED_BINDING"
    )
    load_payload["inventory_discriminator_source"] = "source_kind exact matrix"


def _template_rank(kind: str) -> int:
    ranks = {
        "OWNER_RECORD": 0,
        "EMBEDDED_RECORD": 1,
        "CLOSED_REFERENCE_RECORD": 2,
    }
    try:
        return ranks[kind]
    except KeyError as exc:
        raise ValueError(f"UNKNOWN_TEMPLATE_KIND:{kind}") from exc


def _reindex_owner_templates(owner: dict[str, Any]) -> None:
    templates = owner["payload"]["template_ordinals"]
    templates.sort(
        key=lambda value: (
            _template_rank(value["template_kind"]),
            value["record_type"].encode("utf-8"),
            value["branch_tag_value"].encode("utf-8"),
            value["template_key"].encode("utf-8"),
        )
    )
    ordinal_by_key: dict[str, int] = {}
    for ordinal, template in enumerate(templates):
        template["template_ordinal"] = ordinal
        template["branch_ordinal"] = 0
        key = template["template_key"]
        if key in ordinal_by_key:
            raise ValueError(f"DUPLICATE_TEMPLATE_KEY:{owner['owner_table']}:{key}")
        ordinal_by_key[key] = ordinal
    for field in owner["payload"]["field_ordinals"]:
        try:
            field["template_ordinal"] = ordinal_by_key[field["template_key"]]
        except KeyError as exc:
            raise ValueError(
                f"FIELD_TEMPLATE_MISSING:{owner['owner_table']}:{field['template_key']}"
            ) from exc


def _patch_schema_shapes(registry: dict[str, Any]) -> None:
    project_source = _owner(registry, "project_source_indexes")
    source_payload = project_source["payload"]
    parent_matches = [
        field
        for field in source_payload["field_ordinals"]
        if field["record_type"] == "ComprehensionMapping"
        and field["field_name"] == "captured_environment_labels"
    ]
    if len(parent_matches) != 1:
        raise ValueError("CAPTURE_PARENT_FIELD_NOT_SINGLETON")
    parent_matches[0]["wire_type"] = "tuple[R[CapturedEnvironmentRef]]"

    source_payload["template_ordinals"] = [
        template
        for template in source_payload["template_ordinals"]
        if template["record_type"] != "CapturedEnvironmentRef"
    ]
    source_payload["template_ordinals"].append(
        {
            "branch_ordinal": 0,
            "branch_tag_value": "ANY",
            "record_type": "CapturedEnvironmentRef",
            "template_key": "EMBEDDED:CapturedEnvironmentRef:ANY",
            "template_kind": "EMBEDDED_RECORD",
            "template_ordinal": -1,
        }
    )
    source_payload["field_ordinals"] = [
        field
        for field in source_payload["field_ordinals"]
        if field["record_type"] != "CapturedEnvironmentRef"
    ]
    for field_ordinal, (name, wire) in enumerate(
        (
            ("capture_kind", "E[CapturedEnvironmentKind]"),
            ("capture_name", "S"),
            ("label", "RL"),
        )
    ):
        source_payload["field_ordinals"].append(
            {
                "branch_tag_value": "ANY",
                "cardinality": "SCALAR",
                "field_name": name,
                "field_ordinal": field_ordinal,
                "record_type": "CapturedEnvironmentRef",
                "template_key": "EMBEDDED:CapturedEnvironmentRef:ANY",
                "template_ordinal": -1,
                "wire_type": wire,
            }
        )

    callback_owner = _owner(registry, "generated_stdlib_callbacks")
    callback_payload = callback_owner["payload"]
    forbidden_records = {"CallbackLoadRef", "CallbackValueRef"}
    callback_payload["template_ordinals"] = [
        template
        for template in callback_payload["template_ordinals"]
        if template["record_type"] not in forbidden_records
    ]
    callback_payload["field_ordinals"] = [
        field
        for field in callback_payload["field_ordinals"]
        if field["record_type"] not in forbidden_records
    ]

    for owner in registry["owners_by_id"].values():
        _reindex_owner_templates(owner)


def _rebuild_schema_templates(registry: dict[str, Any]) -> None:
    templates: dict[str, dict[str, Any]] = {}
    sequence = 1
    for owner in sorted(
        registry["owners_by_id"].values(), key=lambda value: value["ordinal"]
    ):
        for template in sorted(
            owner["payload"]["template_ordinals"],
            key=lambda value: value["template_ordinal"],
        ):
            template_id = f"TPL-{sequence:04d}"
            semantic_key = "|".join(
                (
                    str(owner["ordinal"]),
                    template["template_key"],
                    template["branch_tag_value"],
                    template["record_type"],
                )
            )
            templates[template_id] = {
                "template_id": template_id,
                "semantic_key": semantic_key,
                "payload": {"owner_id": owner["owner_id"], **deepcopy(template)},
            }
            sequence += 1
    registry["schema_templates_by_id"] = templates


def _rebuild_reference_fields(registry: dict[str, Any]) -> None:
    fields = [
        deepcopy(value) for value in registry["reference_fields_by_id"].values()
    ]
    capture = [
        value
        for value in fields
        if value["payload"]["owner_table"] == "project_source_indexes"
        and value["payload"]["field_path"]
        == "comprehension_mappings[*].captured_environment_labels[*]"
    ]
    if len(capture) != 1:
        raise ValueError("CAPTURE_REFERENCE_FIELD_NOT_SINGLETON")
    capture_payload = capture[0]["payload"]
    capture_payload.update(
        {
            "containing_record": "CapturedEnvironmentRef",
            "field_ordinal": 2,
            "field_path": (
                "comprehension_mappings[*].captured_environment_labels[*].label"
            ),
            "template_ordinal": next(
                value["template_ordinal"]
                for value in _owner(registry, "project_source_indexes")["payload"][
                    "template_ordinals"
                ]
                if value["record_type"] == "CapturedEnvironmentRef"
            ),
        }
    )
    fields.sort(
        key=lambda value: (
            value["payload"]["owner_ordinal"],
            value["payload"]["template_ordinal"],
            value["payload"]["field_ordinal"],
            value["payload"]["containing_record"].encode("utf-8"),
            value["payload"]["field_path"].encode("utf-8"),
        )
    )
    rebuilt: dict[str, dict[str, Any]] = {}
    for sequence, field in enumerate(fields, start=1):
        field_id = f"FLD-{sequence:04d}"
        field["field_id"] = field_id
        payload = field["payload"]
        field["order_key"] = [
            payload["owner_ordinal"],
            payload["template_ordinal"],
            payload["field_ordinal"],
            0,
        ]
        rebuilt[field_id] = field
    registry["reference_fields_by_id"] = rebuilt


def _changed_branch_record(rule: dict[str, Any]) -> dict[str, Any]:
    payload = rule["payload"]
    discriminator = deepcopy(payload["record_discriminator"])
    terms = discriminator.get("terms")
    if not isinstance(terms, list) or len(terms) != 1:
        raise ValueError("CHANGED_BRANCH_DISCRIMINATOR_NOT_SINGLETON")
    term = terms[0]
    selector = term["selector"]
    path = selector["path"]
    if selector["namespace"] != "OWNER_RECORD" or len(path) != 1:
        raise ValueError("CHANGED_BRANCH_SELECTOR_INVALID")
    branch_id = payload["branch_instance_id"]
    return {
        "branch_id": branch_id,
        "consumer_rule_ids": [rule["rule_id"]],
        "payload": {
            "branch_domain": "OWNER_SCHEMA_DISCRIMINATOR",
            "branch_ordinal": -1,
            "exact_consumer": {
                "containing_record": payload["containing_record"],
                "field_path": payload["field_path"],
                "owner_table": payload["owner_table"],
            },
            "tag_fields": [path[0]],
            "validator_only": False,
        },
        "predicate": discriminator,
    }


def _replace_changed_branches(registry: dict[str, Any]) -> None:
    changed_decisions = {"T10-G18-DD-004", "T10-G18-DD-009"}
    changed_rule_ids = {
        rule_id
        for decision_id in changed_decisions
        for rule_id in _decision(registry, decision_id)["compiled_rule_ids"]
    }
    predecessor_branch_ids = {
        branch_id
        for decision_id in changed_decisions
        for branch_id in _payload(registry, decision_id)[
            "legacy_discriminator_branch_instance_ids"
        ]
    }
    retained = {
        branch_id: branch
        for branch_id, branch in registry["discriminator_branches_by_id"].items()
        if branch_id not in predecessor_branch_ids
    }
    branched_rule_ids = {
        rule_id
        for rule_id in changed_rule_ids
        if registry["compiled_rules_by_id"][rule_id]["payload"].get(
            "branch_instance_id"
        )
        is not None
    }
    for rule_id in sorted(branched_rule_ids):
        rule = registry["compiled_rules_by_id"][rule_id]
        branch = _changed_branch_record(rule)
        branch_id = branch["branch_id"]
        if branch_id in retained:
            raise ValueError(f"CHANGED_BRANCH_ID_COLLISION:{branch_id}")
        retained[branch_id] = branch
    registry["discriminator_branches_by_id"] = retained
    for decision_id in changed_decisions:
        decision = _decision(registry, decision_id)
        decision["design_payload"]["branch_instance_ids"] = [
            registry["compiled_rules_by_id"][rule_id]["payload"][
                "branch_instance_id"
            ]
            for rule_id in decision["compiled_rule_ids"]
            if registry["compiled_rules_by_id"][rule_id]["payload"].get(
                "branch_instance_id"
            )
            is not None
        ]
    # DD-018 is the global branch catalog.  Its normative list is rebuilt from
    # the corrected catalog rather than retaining the deleted v2 wrapper IDs.
    _decision(registry, "T10-G18-DD-018")["design_payload"][
        "branch_instance_ids"
    ] = list(retained)


def _branch_semantic_key(
    branch: dict[str, Any], registry: dict[str, Any]
) -> tuple[object, ...]:
    rank = {"OWNER_SCHEMA_DISCRIMINATOR": 0, "CLOSED_REFERENCE_RECORD": 1}
    domain = branch["payload"]["branch_domain"]
    consumer_signatures = []
    for rule_id in branch["consumer_rule_ids"]:
        rule = deepcopy(registry["compiled_rules_by_id"][rule_id])
        rule.pop("rule_id", None)
        rule.pop("ordinal", None)
        rule["payload"].pop("branch_instance_id", None)
        rule["payload"]["schema_order_key"].pop("branch_ordinal", None)
        consumer_signatures.append(canonical_json_bytes(rule))
    return (
        rank[domain],
        canonical_json_bytes(branch["predicate"]),
        canonical_json_bytes(branch["payload"]["exact_consumer"]),
        tuple(sorted(consumer_signatures)),
    )


def _rebuild_branch_ids(registry: dict[str, Any]) -> dict[str, str]:
    source = list(registry["discriminator_branches_by_id"].values())
    semantic_keys = [_branch_semantic_key(value, registry) for value in source]
    if len(semantic_keys) != len(set(semantic_keys)):
        raise ValueError("DUPLICATE_BRANCH_SEMANTIC_KEY")
    ordered = sorted(source, key=lambda value: _branch_semantic_key(value, registry))
    if len(ordered) != 461:
        raise ValueError(f"GLOBAL_BRANCH_COUNT:{len(ordered)}")
    identifier_map: dict[str, str] = {}
    rebuilt: dict[str, dict[str, Any]] = {}
    for ordinal, branch in enumerate(ordered, start=1):
        old_id = branch["branch_id"]
        new_id = f"BR-{ordinal:04d}"
        identifier_map[old_id] = new_id
        record = deepcopy(branch)
        record["branch_id"] = new_id
        record["payload"]["branch_ordinal"] = ordinal
        rebuilt[new_id] = record
    registry["discriminator_branches_by_id"] = rebuilt
    return identifier_map


def _rebuild_rule_ids(registry: dict[str, Any]) -> dict[str, str]:
    branch_ordinals = {
        branch_id: branch["payload"]["branch_ordinal"]
        for branch_id, branch in registry["discriminator_branches_by_id"].items()
    }
    for rule in registry["compiled_rules_by_id"].values():
        branch_id = rule["payload"].get("branch_instance_id")
        rule["payload"]["schema_order_key"]["branch_ordinal"] = (
            0 if branch_id is None else branch_ordinals[branch_id]
        )
    ordered = sorted(
        registry["compiled_rules_by_id"].values(),
        key=lambda value: (
            value["payload"]["schema_order_key"]["owner_ordinal"],
            value["payload"]["schema_order_key"]["template_ordinal"],
            value["payload"]["schema_order_key"]["field_ordinal"],
            value["payload"]["schema_order_key"]["branch_ordinal"],
            value["rule_id"].encode("utf-8"),
        ),
    )
    if len(ordered) != 570:
        raise ValueError(f"GLOBAL_RULE_COUNT:{len(ordered)}")
    keys = [
        tuple(rule["payload"]["schema_order_key"].values()) for rule in ordered
    ]
    if len(keys) != len(set(keys)):
        raise ValueError("DUPLICATE_COMPLETE_RULE_ORDER_KEY")
    identifier_map: dict[str, str] = {}
    rebuilt: dict[str, dict[str, Any]] = {}
    for ordinal, rule in enumerate(ordered):
        old_id = rule["rule_id"]
        new_id = f"PCR-{ordinal + 1:04d}"
        identifier_map[old_id] = new_id
        record = deepcopy(rule)
        record["rule_id"] = new_id
        record["ordinal"] = ordinal
        rebuilt[new_id] = record
    registry["compiled_rules_by_id"] = rebuilt
    return identifier_map


def _apply_branch_identifier_map(
    registry: dict[str, Any], identifier_map: Mapping[str, str]
) -> None:
    for rule in registry["compiled_rules_by_id"].values():
        branch_id = rule["payload"].get("branch_instance_id")
        if branch_id is not None:
            rule["payload"]["branch_instance_id"] = identifier_map[branch_id]
    for decision in registry["decisions_by_id"].values():
        decision["design_payload"]["branch_instance_ids"] = [
            identifier_map[branch_id]
            for branch_id in decision["design_payload"]["branch_instance_ids"]
        ]


def _replace_identifier_values(
    value: object, identifier_map: Mapping[str, str]
) -> object:
    if isinstance(value, dict):
        return {
            key: _replace_identifier_values(child, identifier_map)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [_replace_identifier_values(child, identifier_map) for child in value]
    if isinstance(value, str):
        return identifier_map.get(value, value)
    return value


def _apply_rule_identifier_map(
    registry: dict[str, Any], identifier_map: Mapping[str, str]
) -> None:
    for branch in registry["discriminator_branches_by_id"].values():
        branch["consumer_rule_ids"] = [
            identifier_map[rule_id] for rule_id in branch["consumer_rule_ids"]
        ]
    for decision in registry["decisions_by_id"].values():
        decision["compiled_rule_ids"] = [
            identifier_map[rule_id] for rule_id in decision["compiled_rule_ids"]
        ]
        replaced_payload = _replace_identifier_values(
            decision["payload"], identifier_map
        )
        if not isinstance(replaced_payload, dict):
            raise ValueError("DECISION_PAYLOAD_REPLACEMENT_INVALID")
        decision["payload"] = replaced_payload
    for row in registry["coverage_rows_by_id"].values():
        row["compiled_rule_ids"] = [
            identifier_map[rule_id] for rule_id in row["compiled_rule_ids"]
        ]


def _patch_invariants(registry: dict[str, Any]) -> None:
    template_invariants = [
        invariant
        for invariant in registry["invariants_by_id"].values()
        if invariant["assertion"].get("collection") == "schema_templates_by_id"
        and invariant["kind"] == "COUNT_EQUALS"
    ]
    if len(template_invariants) != 1:
        raise ValueError("TEMPLATE_COUNT_INVARIANT_NOT_SINGLETON")
    template_invariants[0]["assertion"]["expected"] = 207
    template_invariants[0]["description"] = "Schema-template count is 207."
    stop_invariants = [
        invariant
        for invariant in registry["invariants_by_id"].values()
        if invariant["kind"] == "ALL_MATCH"
        and "STOP and no-promotion" in invariant["description"]
    ]
    if len(stop_invariants) != 1:
        raise ValueError("STOP_INVARIANT_NOT_SINGLETON")
    checks = stop_invariants[0]["assertion"]["checks"]
    implementation_check = {
        "path": ["scope_boundary", "implementation_allowed"],
        "equals": False,
    }
    if implementation_check not in checks:
        checks.append(implementation_check)


def _rebuild_dd020_ordering(registry: dict[str, Any]) -> None:
    ordering = _exact(registry, "T10-G18-DD-020")["schema_ordering"]
    ordering["owner_count"] = len(registry["owners_by_id"])
    ordering["owner_ordinals"] = [
        {
            "owner_ordinal": owner["ordinal"],
            "owner_table": owner["owner_table"],
        }
        for owner in sorted(
            registry["owners_by_id"].values(), key=lambda value: value["ordinal"]
        )
    ]
    ordering["owner_schemas"] = [
        {
            "owner_ordinal": owner["ordinal"],
            "owner_table": owner["owner_table"],
            **deepcopy(owner["payload"]),
        }
        for owner in sorted(
            registry["owners_by_id"].values(), key=lambda value: value["ordinal"]
        )
    ]
    ordering["reference_field_ordinals"] = [
        deepcopy(field["payload"])
        for field in registry["reference_fields_by_id"].values()
    ]
    ordering["branch_ordinals"] = [
        {
            "branch_instance_id": branch["branch_id"],
            "branch_ordinal": branch["payload"]["branch_ordinal"],
        }
        for branch in registry["discriminator_branches_by_id"].values()
    ]
    ordering["branch_ordinal_derivation"] = (
        "Canonical sort by branch domain rank, canonical predicate JSON, "
        "canonical exact-consumer JSON, and canonical consumer-rule semantic "
        "fingerprints; predecessor IDs and collection order are forbidden."
    )
    ordering["compiled_reference_rule_order"] = [
        {
            "complete_key": deepcopy(rule["payload"]["schema_order_key"]),
            "containing_record": rule["payload"]["containing_record"],
            "field_path": rule["payload"]["field_path"],
            "owner_table": rule["payload"]["owner_table"],
            "rule_id": rule["rule_id"],
        }
        for rule in registry["compiled_rules_by_id"].values()
    ]
    ordering["final_post_decision_distinct_rl_field_count"] = len(
        registry["reference_fields_by_id"]
    )
    ordering["final_post_decision_rl_rule_count"] = len(
        registry["compiled_rules_by_id"]
    )
    provenance_counts = defaultdict(int)
    for rule in registry["compiled_rules_by_id"].values():
        provenance_counts[rule["provenance"]["class"]] += 1
    ordering["rule_provenance_counts"] = {
        "authority_closed_inventory_rules": provenance_counts[
            "AUTHORITY_CLOSED_INVENTORY"
        ],
        "coverage_derived_rules": provenance_counts["COVERAGE_DERIVED"],
        "post_schema_extra_rules": provenance_counts["POST_SCHEMA_EXTRA"],
        "total_compiled_rules": len(registry["compiled_rules_by_id"]),
    }


def _semantic_rule_projection(
    registry: dict[str, Any], rule_id: str
) -> dict[str, Any]:
    rule = deepcopy(registry["compiled_rules_by_id"][rule_id])
    rule.pop("rule_id", None)
    rule.pop("ordinal", None)
    rule["payload"].pop("branch_instance_id", None)
    rule["payload"]["schema_order_key"].pop("branch_ordinal", None)
    return rule


def _semantic_branch_projection(
    registry: dict[str, Any], branch_id: str
) -> dict[str, Any]:
    branch = deepcopy(registry["discriminator_branches_by_id"][branch_id])
    branch.pop("branch_id", None)
    branch["payload"].pop("branch_ordinal", None)
    consumer_ids = branch.pop("consumer_rule_ids")
    branch["consumer_rules"] = sorted(
        (
            _semantic_rule_projection(registry, rule_id)
            for rule_id in consumer_ids
        ),
        key=canonical_json_bytes,
    )
    return branch


def _semantic_decision_projection(
    registry: dict[str, Any], decision_id: str
) -> dict[str, Any]:
    decision = registry["decisions_by_id"][decision_id]
    value = deepcopy(decision)
    compiled_rule_ids = list(value.pop("compiled_rule_ids"))
    branch_ids = list(value["design_payload"].pop("branch_instance_ids"))
    value.pop("compiled_rule_ids", None)
    value["design_payload"].pop("branch_instance_ids", None)

    def strip_derived(node: object) -> object:
        if isinstance(node, dict):
            return {
                key: strip_derived(child)
                for key, child in node.items()
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
        if isinstance(node, list):
            return [strip_derived(child) for child in node]
        return node

    projected = strip_derived(value)
    if not isinstance(projected, dict):
        raise ValueError("DECISION_PROJECTION_INVALID")
    projected["resolved_rules"] = sorted(
        (
            _semantic_rule_projection(registry, rule_id)
            for rule_id in compiled_rule_ids
        ),
        key=canonical_json_bytes,
    )
    # DD-018 is the global catalog view.  Its member semantics belong to the
    # owning decisions; resolving all 461 branches here would misclassify a
    # permitted DD-004 or DD-009 correction as a DD-018 semantic change.
    if decision_id != "T10-G18-DD-018":
        projected["resolved_branches"] = sorted(
            (
                _semantic_branch_projection(registry, branch_id)
                for branch_id in branch_ids
            ),
            key=canonical_json_bytes,
        )
    return projected


def changed_decision_ids(
    v2: dict[str, Any], v3: dict[str, Any]
) -> set[str]:
    identifiers = set(v2["decisions_by_id"]) | set(v3["decisions_by_id"])
    return {
        identifier
        for identifier in identifiers
        if _semantic_decision_projection(v2, identifier)
        != _semantic_decision_projection(v3, identifier)
    }


def semantic_diff_outside_allowlist(
    v2: dict[str, Any], v3: dict[str, Any]
) -> list[str]:
    return sorted(changed_decision_ids(v2, v3) - ALLOWED_DECISION_DELTAS)


def _normative_projection_digests(registry: dict[str, Any]) -> dict[str, str]:
    return {
        decision_id: sha256(
            canonical_json_bytes(
                _semantic_decision_projection(registry, decision_id)
            )
        ).hexdigest()
        for decision_id in sorted(ALLOWED_DECISION_DELTAS)
    }


def build_v3(
    v2: dict[str, Any], *, registry_schema_sha256: str
) -> dict[str, Any]:
    """Build the corrected review input without file-system side effects."""

    if v2.get("format") != V2_FORMAT:
        raise ValueError("PREDECESSOR_FORMAT_MISMATCH")
    if sha256(canonical_json_bytes(v2)).hexdigest() != V2_SHA256:
        raise ValueError("PREDECESSOR_IDENTITY_DRIFT")
    if re.fullmatch(r"[0-9a-f]{64}", registry_schema_sha256) is None:
        raise ValueError("V3_SCHEMA_SHA256_INVALID")

    registry = deepcopy(v2)
    registry.update(
        {
            "format": V3_FORMAT,
            "correction_class": (
                "NORMATIVE_REVIEW_INPUT_CORRECTION_NOT_REPRESENTATION_ONLY"
            ),
            "predecessor_v2_attestations_inherited": False,
            "authority_amendment_scope_v1_authoring_authority": False,
            "predecessor_binding": {
                "bytes": V2_BYTES,
                "format": V2_FORMAT,
                "mode": "0644",
                "path": V2_PATH,
                "sha256": V2_SHA256,
            },
        }
    )
    registry["scope_boundary"]["implementation_allowed"] = False
    registry["schema_binding"] = {
        "path": V3_SCHEMA_PATH,
        "sha256": registry_schema_sha256,
    }

    _patch_dd001(registry)
    _patch_dd004(registry)
    _patch_owner_tuples_and_name(registry)
    _patch_dd009(registry)
    _patch_provider_maps(registry)
    _sync_changed_coverage_rows(registry)
    _patch_schema_shapes(registry)
    _rebuild_schema_templates(registry)
    _rebuild_reference_fields(registry)
    _replace_changed_branches(registry)

    branch_map = _rebuild_branch_ids(registry)
    _apply_branch_identifier_map(registry, branch_map)
    rule_map = _rebuild_rule_ids(registry)
    _apply_rule_identifier_map(registry, rule_map)

    _patch_invariants(registry)
    _rebuild_dd020_ordering(registry)
    registry["normative_projection_digests_by_decision"] = (
        _normative_projection_digests(registry)
    )
    registry["normative_projection_digests_by_collection"] = {
        "coverage_rows_by_id": sha256(
            canonical_json_bytes(registry["coverage_rows_by_id"])
        ).hexdigest()
    }
    outside = semantic_diff_outside_allowlist(v2, registry)
    if outside:
        raise ValueError(f"SEMANTIC_DIFF_OUTSIDE_ALLOWLIST:{','.join(outside)}")
    registry_projection = deepcopy(registry)
    registry_projection.pop("normative_registry_projection_sha256", None)
    registry["normative_registry_projection_sha256"] = sha256(
        canonical_json_bytes(registry_projection)
    ).hexdigest()
    return registry


def write_v3_registry(repository_root: Path) -> Path:
    review = repository_root / "docs/superpowers/specs/idl/task10/v10/review"
    schema_path = repository_root / V3_SCHEMA_PATH
    output_path = review / "v3/authority-design-decision-registry-v3.json"
    verified = verify_baseline_inputs(repository_root)
    predecessor_bytes = verified[V2_PATH]
    if sha256(predecessor_bytes).hexdigest() != V2_SHA256:
        raise ValueError("PREDECESSOR_IDENTITY_DRIFT")
    predecessor = json.loads(
        predecessor_bytes.decode("utf-8"), parse_constant=_reject_non_finite
    )
    if not isinstance(predecessor, dict):
        raise ValueError("PREDECESSOR_ROOT_NOT_OBJECT")
    _verify_registry_source_bindings(repository_root, predecessor)
    try:
        schema_bytes = _read_exact_regular_0644(schema_path)
    except (OSError, ValueError) as exc:
        raise ValueError("V3_SCHEMA_IDENTITY_DRIFT") from exc
    registry = build_v3(
        predecessor,
        registry_schema_sha256=sha256(schema_bytes).hexdigest(),
    )
    _atomic_write_regular_0644(output_path, canonical_json_bytes(registry))
    return output_path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[8]
    print(write_v3_registry(root))
