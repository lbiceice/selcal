# Task 10 reference-schema v10 draft manifest

## Verdict

`task10-reference-schema-v10.json` is a bounded, machine-readable gap
artifact. It is **not** a complete RL-leaf registry, a policy fixture, or a
specification authority. It records only the reference aliases and reciprocal
splits that can be closed from the frozen specification plus the confirmed
G14/G15 decisions. Unknown target universes and discriminator encodings remain
`null` and are not replaced with `ANY_TABLE`, the 66-table universe, a label
prefix, an observed target owner, or a policy value.

## Byte identity

- Authoritative specification:
  `docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md`
- Authoritative specification SHA-256:
  `c263646e5b64c0aa3eb52e33fc31a0f5b87e2e08492e38cc884bebdf55c8e137`
- Reference-schema draft:
  `docs/superpowers/specs/fixtures/task10-reference-schema-v10.json`
- Reference-schema draft SHA-256:
  `8f3326145154860bc64c99835c90eded014fd89ba764d9b3903d48508929090d`
- This manifest's SHA-256 is intentionally not self-embedded; it belongs in
  the delivery report after the final read-only verification.

## Machine-readable IDL boundary

The draft defines an artifact-local `ClosedReferenceAlias` with exactly three
fields: `alias`, `allowed_target_tables`, and `evidence`. Every alias expands to
a non-empty proper exact subset of `ClosedOwnerTable`. Eleven singleton aliases
are present. No catch-all alias exists.

Each `ReferenceLeafRuleDraft` records owner table, containing record, exact or
`ANY` record discriminator, field path, cardinality, exact target alias/table
set or `null`, kind, local schema order, full nested schema-order path, any
explicit reference-ordinal binding, closure status, blockers, and evidence.
Schema positions are an artifact-local zero-based transcription of the
declared record field sequence. They are not represented as an already-frozen
G18 authority.

## Closed draft coverage

Fourteen RL leaf-rule variants have an exact target-table subset and are
recorded as `CLOSED_DRAFT_BLOCKED_BY_G18_AUTHORITY`; each row carries
`blocked_by=["G18"]` rather than presenting the draft IDL as current authority:

| Owner / record | Discriminator and field path | Cardinality | Exact target table | Kind |
|---|---|---:|---|---|
| `project_classes` / `ProjectClassBinding` | `ANY` · `behavior_slot_manifest_label` | `SCALAR` | `behavior_slot_manifests` | `AUTH_REQUIRES` |
| `behavior_slot_manifests` / `BehaviorSlotManifest` | `ANY` · `project_class_label` | `SCALAR` | `project_classes` | `VALIDATES` |
| `behavior_slot_manifests` / `BehaviorSlotEntry` | `state=OWN` · `entries[*].defining_class_label` | `OPTIONAL` | `project_classes` | `VALIDATES` |
| `external_classes` / `ExternalClassBinding` | `ANY` · `abc_state_binding_label` | `OPTIONAL` | `external_abc_states` | `AUTH_REQUIRES` |
| `external_abc_states` / `ExternalAbcStateBinding` | `ANY` · `external_class_label` | `SCALAR` | `external_classes` | `VALIDATES` |
| `external_abc_states` / `ExternalAbcStateBinding` | `ANY` · `bootstrap_recipe_label` | `SCALAR` | `external_abc_bootstrap_recipes` | `AUTH_REQUIRES` |
| `external_abc_bootstrap_recipes` / `ExternalAbcBootstrapRecipe` | `ANY` · `external_class_label` | `SCALAR` | `external_classes` | `VALIDATES` |
| `generated_artifacts` / `GeneratedProjectArtifactBinding` | `ANY` · `generated_method_labels[*]` | `ORDERED_TUPLE` | `generated_methods` | `AUTH_REQUIRES` |
| `generated_methods` / `GeneratedMethodRecord` | `ANY` · `owner_artifact_label` | `SCALAR` | `generated_artifacts` | `VALIDATES` |
| `generated_artifacts` / `GeneratedProjectArtifactBinding` | `ANY` · `field_accessor_labels[*]` | `ORDERED_TUPLE` | `generated_field_accessors` | `AUTH_REQUIRES` |
| `generated_field_accessors` / `GeneratedFieldAccessorRecord` | `ANY` · `owner_artifact_label` | `SCALAR` | `generated_artifacts` | `VALIDATES` |
| `generated_stdlib_callbacks` / `GeneratedStdlibCallbackBinding` | `ANY` · `transfer_label` | `SCALAR` | `generated_callback_transfers` | `AUTH_REQUIRES` |
| `generated_callback_transfers` / `GeneratedStdlibCallbackTransfer` | `ANY` · `callback_binding_label` | `SCALAR` | `generated_stdlib_callbacks` | `VALIDATES` |
| `project_descriptors` / `ProjectDescriptorBinding` | `ANY` · `project_class_label` | `SCALAR` | `project_classes` | `VALIDATES` |

This closes the requested draft representation of class↔manifest, ABC
class/state/recipe, artifact↔method/accessor, callback↔transfer, and descriptor
backlink groups. The descriptor's forward class-member branch is retained
separately as a gap because the present schema has no target-kind discriminator
that makes `project_descriptors` the exhaustive target set for every
`ClassMemberRecord.binding_label`.

## Blocked or conflicting RL leaves

Four requested leaf-rule variants preserve a confirmed kind or target fragment
but do not claim a closed rule:

| Owner / record | Discriminator and field path | Preserved fact | Missing closure |
|---|---|---|---|
| `behavior_slot_manifests` / `BehaviorSlotEntry` | `state=INHERITED` · `entries[*].defining_class_label` | `AUTH_REQUIRES` | Exact inherited defining-class target alias is absent from the authority. |
| `project_classes` / `ClassMemberRecord` | `state=PRESENT;value_kind=BINDING` · `class_member_records[*].binding_label` | Project-descriptor branch is `AUTH_REQUIRES`; `project_descriptors` is a confirmed subset. | The generic leaf's exhaustive target union and a schema discriminator for the descriptor branch are absent. |
| `runtime_state_reference_bindings` / `RuntimeStateReferenceBinding` | `ANY` · `source_label` | Confirmed split says `VALIDATES`; it does not bind `reference_ordinal`. | Exact runtime-bearing target alias is absent; current authority lines 2659–2661 still say `RUNTIME_REF`. |
| `runtime_state_reference_bindings` / `RuntimeStateReferenceBinding` | `ANY` · `target_label` | `RUNTIME_REF`; `reference_ordinal` binds this leaf only. | Exact runtime-bearing target alias is absent. |

## Open gaps and conflicts

1. `G14_REFERENCE_RULE_TARGET_TABLE_AND_DISCRIMINATOR_DERIVATION_MISSING`
   is only partially reduced. The four rows above retain `null` rather than an
   invented target universe or discriminator.
2. `G15_DEFAULT_AUTH_REQUIRES_FORCES_MANDATORY_CYCLES` is represented by the
   confirmed forward/backlink splits, but the frozen authority still says that
   every unlisted RL leaf defaults to `AUTH_REQUIRES`. It also still lists both
   runtime binding labels as `RUNTIME_REF`. Thus the draft and current authority
   intentionally expose, rather than conceal, this conflict.
3. `G16_RUNTIME_BEARING_OWNER_ENUM_MISSING` prevents an exact runtime-source or
   runtime-target alias.
4. `G18_CLOSED_REFERENCE_ALIAS_AND_LEAF_IDL_NOT_IN_AUTHORITY` remains open.
   The artifact-local IDL, discriminator spelling, and schema-order convention
   cannot become normative until they are frozen into new authority bytes.
5. The specification is prose schemas plus incremental replacements, not one
   bare machine schema. Therefore an exhaustive all-record RL traversal cannot
   be certified from this artifact.

## Authority decision

This draft is **not sufficient to become specification authority**. Its useful
scope is narrower: it gives a reviewable candidate encoding for 14 closed leaf
variants, preserves four unresolved variants without fabrication, and makes
the minimum authority changes needed for G14/G15/G16/G18 visible. A future
authority revision must freeze the full `ClosedReferenceAlias` enum, every
owner/record/discriminator/field-path row, exact target subsets, discriminator
syntax, schema-order basis, runtime-bearing owner enum, and the corrected kind
exception list before exhaustive fixtures or policy digests are legitimate.
