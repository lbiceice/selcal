# Task 10 authority review package v3 semantic correction plan

> **Lifecycle:** approved execution plan for an append-only review-input
> correction. It is not authority, an authority amendment, IDL, a KAT,
> implementation authorization, M0--M2 closure, or SoftwareX readiness.

**Goal:** replace the false-green v2 cross-representation projection with one
deterministically rebuilt v3 review input whose decision payload, owner tuples,
record fields, discriminators, compiled rules, branches, templates, and field
ordinals express the same adjudicated semantics.

**Why this route exists:** the exact-byte v2 review and the authority-amendment
scope v1 proved identity and structural closure, but an independent semantic
join found six major and two minor collisions. The v2 registry and both v2
attestations remain immutable adverse evidence. They do not authorize successor
authoring.

## 1. Fixed writer scope

The writer may create exactly these eight files and must modify no existing
file:

1. `docs/superpowers/plans/2026-08-31-task10-authority-review-package-v3-correction.md`
2. `docs/superpowers/specs/idl/task10/v10/review/v3/authority-review-package-v3-correction-spec.md`
3. `docs/superpowers/specs/idl/task10/v10/review/v3/authority-review-package-v3-baseline.json`
4. `docs/superpowers/specs/idl/task10/v10/review/v3/authority-design-decision-registry-v3.json`
5. `docs/superpowers/specs/idl/task10/v10/review/v3/schema/authority-design-decision-registry-v3.schema.json`
6. `docs/superpowers/specs/idl/task10/v10/review/v3/migrate_authority_decision_registry_v2_to_v3.py`
7. `docs/superpowers/specs/idl/task10/v10/review/v3/validate_authority_review_package_v3.py`
8. `tests/task10/test_authority_review_package_v3.py`

Fresh review attestations are reviewer outputs created only after the writer
scope has frozen. They are not writer outputs and must bind the final v3 SHA.

## 2. Frozen predecessor identities

- prose authority SHA-256:
  `74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff`
- prose authority length: `298339` bytes
- v2 registry SHA-256:
  `77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5`
- v2 registry length: `4282426` bytes, regular mode `0644`
- v2 schema SHA-256:
  `81f8e1e68fc1a8cecf964a542feaeb601431b7c2e74726f4e0940f163b23b967`
- v2 schema length: `22075` bytes, regular mode `0644`
- v2 review baseline SHA-256:
  `24d52f573f566317c973cd74e3e52779b987e2055c8df90a92a09040ca0bf7ea`

The two v2 attestations are historical/superseded evidence only. No v2 PASS
status may be inherited by v3.

## 3. Lifecycle and stop contract

The v3 registry must retain:

```text
artifact_state=REVIEW_DECISION_INPUT_NOT_AUTHORITY
authority_amendment_status=AUTHORITY_AMENDMENT_NOT_YET_REVIEWED
machine_stop_decision=STOP_BEFORE_AUTHORITY_IDL_AND_KATS
authority_idl_allowed=false
kats_allowed=false
implementation_allowed=false
```

It must add:

```text
correction_class=NORMATIVE_REVIEW_INPUT_CORRECTION_NOT_REPRESENTATION_ONLY
predecessor_v2_attestations_inherited=false
authority_amendment_scope_v1_authoring_authority=false
```

## 4. Adjudicated semantic deltas

### DD-001: row count is not unique-path count

- Keep `10` affected owner paths and `10` exact retyped paths.
- Keep `11` coverage census rows, assigned-null rows, and removed-RL rows.
- State explicitly that the eleven rows represent ten unique paths.
- Preserve the two distinct census rows for
  `behavior_slot_manifests.entries[*].raw_member_identity_label`.

### DD-004: CapturedEnvironmentRef

The only legal role-to-owner map is:

```text
VALUE_CONTRACT               -> value_contracts
PROJECT_RUNTIME_VALUE        -> runtime_values
PROCESS_LOCAL_IDENTITY_TOKEN -> process_local_identity_tokens
PROJECT_FUNCTION_BINDING     -> project_function_bindings
```

The embedded record field sequence is exactly:

```text
capture_kind, capture_name, label
```

`capture_name` is non-empty, unique, and strictly UTF-8 ordered. The containing
wire is `tuple[R[CapturedEnvironmentRef]]`. Four rules discriminate on the
nested `capture_kind`. `EXTERNAL_IDENTITY`, `GENERATED_STDLIB_CALLBACK`, and the
closed-reference `$ref_kind/role/target_label` projection are forbidden.

### DD-006: owner tuple

Append `runtime_values` to the owner tuple. PCR-0510 and PCR-0511 are validating
backlinks to that owner; no other semantic delta is permitted.

### DD-007: owner tuple and type name

Append `semantic_models` and `outcome_contracts` to the owner tuple. Replace the
two summary occurrences of `ProjectAccessRef` with `RootFieldAccessRef`. No
record shape, target, or cardinality change is permitted.

### DD-009: direct callback binding discriminators

Default, keyword-default, and closure records use their own `binding_kind` with
this exact map:

```text
VALUE_CONTRACT        -> value_contracts
EXTERNAL_IDENTITY     -> external_identities
PROJECT_RUNTIME_VALUE -> runtime_values
GENERATED_CALLBACK    -> generated_stdlib_callbacks
BOUND_TYPE_MEMBER     -> bound_type_members
```

The complete load-kind universe is:

```text
CONSTANT
POSITIONAL_PARAMETER
KEYWORD_PARAMETER
DERIVED_LOCAL
PROJECT_GLOBAL
EXTERNAL_GLOBAL
BUILTIN
CLOSURE_CONTRACT
CLOSURE_VALUE
ATTRIBUTE_BOUND_MEMBER
ATTRIBUTE_EXTERNAL_MEMBER
ATTRIBUTE_GENERATED_ACCESSOR
ATTRIBUTE_PROJECT_DESCRIPTOR
```

The nine target-bearing branches are:

```text
PROJECT_GLOBAL               -> project_function_bindings
EXTERNAL_GLOBAL              -> external_identities
BUILTIN                      -> external_identities
CLOSURE_CONTRACT             -> value_contracts
CLOSURE_VALUE                -> runtime_values
ATTRIBUTE_BOUND_MEMBER       -> bound_type_members
ATTRIBUTE_EXTERNAL_MEMBER    -> external_type_members
ATTRIBUTE_GENERATED_ACCESSOR -> generated_field_accessors
ATTRIBUTE_PROJECT_DESCRIPTOR -> project_descriptors
```

Presence is mutually exclusive: `CONSTANT` has only `literal_value`; the three
parameter/local kinds have only `source_ordinal`; the nine target kinds have
only `literal_name + target_label`. `CallbackValueRef`, `CallbackLoadRef`,
`PROJECT_MODULE`, and a generated-callback load target are forbidden. Forward
PCR-0530 and inverse PCR-0550 transfer directions remain unchanged.

### DD-011 and DD-016: ProviderReference

Delete `GENERATED_FIELD_ACCESSOR -> generated_field_accessors` from both exact
ProviderReference maps. Do not add that role to any operation matrix. The
remaining global type is the exact six-role union already consumed by the
operation matrices and global branches.

## 5. Deterministic global rebuild

The migrator must rebuild, not hand-retain, all derived IDs and ordinals:

- compiled rules;
- discriminator branches;
- schema templates;
- reference/schema fields;
- DD-020 schema ordering;
- coverage rule/field links;
- per-decision branch/rule lists; and
- all normative projection digests.

Expected counts after rebuilding:

| Collection | v2 | v3 |
| --- | ---: | ---: |
| owners | 66 | 66 |
| decisions | 23 | 23 |
| coverage rows | 264 | 264 |
| compiled rules | 570 | 570 |
| discriminator branches | 461 | 461 |
| reference fields | 312 | 312 |
| schema templates | 209 | 207 |
| evidence refs | 149 | 149 |
| invariants | 23 | 23 |
| source bindings | 6 | 6 |
| evidence-binding expectations | 146 | 146 |
| legacy aliases | 16 | 16 |

Rule provenance remains `509 coverage + 9 post-schema + 52 authority-closed`.
DD-004 changes from five to four rules and DD-009 from 32 to 33 rules.
The six removed `$ref_kind/role/target_label` wrapper rows belong to
`owners_by_id[*].payload.field_ordinals`, whose total changes from `1070` to
`1064`; they are not entries in `reference_fields_by_id` and must not be used
to force that collection from 312 to 306.

## 6. TDD sequence

1. Write RED tests for exact predecessor path, bytes, mode, kind, and SHA.
2. Write a semantic-diff allowlist test: no decision outside
   DD-001/004/006/007/009/011/016 may change.
3. Write negative tests for all eight frozen collision codes.
4. Write independent count, role-union, owner-tuple, field-sequence,
   discriminator, presence, transfer-direction, and STOP gates.
5. Implement the migrator without importing the independent validator.
6. Generate v3 twice in separate temporary directories and require identical
   canonical bytes and SHA.
7. Validate v3 without importing the migrator.
8. Freeze the final eight writer files only after every writer has stopped.
9. Obtain fresh exact-byte specification and quality reviews; any correction
   invalidates both.

## 7. Required negative failure codes

At minimum:

```text
PREDECESSOR_IDENTITY_DRIFT
SEMANTIC_DIFF_OUTSIDE_ALLOWLIST
DECISION_CENSUS_PATH_COUNT_MISMATCH
EXACT_ROLE_OWNER_MATRIX_MISMATCH
EXACT_RECORD_FIELD_SEQUENCE_MISMATCH
CROSS_FIELD_MATRIX_NOT_COMPILED
REFERENCE_OWNER_TUPLE_MISMATCH
ORPHAN_EXACT_ROLE
REFERENCE_TYPE_NAME_MISMATCH
TRANSFER_DIRECTION_RULE_LINK_MISMATCH
GLOBAL_COLLECTION_COUNT_MISMATCH
STALE_V2_ATTESTATION_INHERITED
STALE_SCOPE_V1_REUSED
STOP_BOUNDARY_VIOLATION
```

## 8. Completion boundary

Passing v3 restores only eligibility to design and review a new
authority-amendment scope v2. It does not authorize successor prose, authority
IDL, KAT construction, production implementation, M0--M2 closure, UI, release,
manuscript drafting, or SoftwareX submission.
