# Task 10 authority review package v3 correction specification

Status: `EXECUTABLE_REVIEW_INPUT_SPECIFICATION_NOT_AUTHORITY`

This specification governs one deterministic semantic correction of the exact
v2 registry identified in `authority-review-package-v3-baseline.json`. It does
not amend prose authority, create authority IDL or KATs, authorize production
implementation, close M0--M2, or establish SoftwareX readiness.

## Identity and lifecycle

Every reader and writer must verify the eight baseline records before consuming
semantic content. The v3 registry retains
`REVIEW_DECISION_INPUT_NOT_AUTHORITY`,
`AUTHORITY_AMENDMENT_NOT_YET_REVIEWED`, and
`STOP_BEFORE_AUTHORITY_IDL_AND_KATS`. Authority IDL, KATs, and implementation
remain false. The registry additionally records that this is a normative review
input correction, that v2 attestations are not inherited, and that the former
scope-v1 package grants no authoring authority.

The baseline file is not self-authenticating. Both the migrator and independent
validator hard-code its exact canonical SHA-256
`d040bd9ff1377d41e6202a1483662bd9f9a03e04263f5897e1bd4e750bd35de0`
before accepting any descriptor from it. They then require all eight exact
role/path/byte/mode/digest records to resolve to regular `0644` files through a
no-follow, same-descriptor reader. Missing, substituted, or synchronized
baseline edits fail before semantic migration.

The registry itself must bind its exact predecessor as format
`selcal.task10.g18.authority-design-decision-registry.v2`, path
`docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v2.json`,
length `4282426`, regular mode `0644`, and SHA-256
`77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5`.
The independent validator cross-checks that record against the baseline and
the same-descriptor bytes before reading semantic content.

Path-level validation and the writer additionally resolve all six frozen
`source_bindings_by_id` paths through the same hardened reader and compare the
actual bytes with their registry digests. A missing source fails with
`SOURCE_FILE_MISSING`; changed bytes fail with `SOURCE_DIGEST_MISMATCH`. This
executes the source-digest invariant rather than treating its declarative row
as evidence of completion.

The writer emits the registry through a same-directory exclusive temporary
regular file, uses no-follow directory and file descriptors, explicitly sets
mode `0644`, completes and synchronizes the bytes, and atomically replaces the
destination. Existing destination symlinks and non-regular files are rejected;
the process umask cannot change the final mode.

## Closed semantic change set

Only DD-001, DD-004, DD-006, DD-007, DD-009, DD-011, DD-016, plus DD-020's
derived ordering projection may change.

- DD-001 distinguishes eleven census rows from ten unique retyped paths.
- DD-004 uses an embedded `CapturedEnvironmentRef` with the exact field order
  `capture_kind, capture_name, label`, strict UTF-8 `capture_name` ordering,
  and four direct `OWNER_RECORD` discriminator branches.
- DD-006 adds `runtime_values` to its closed owner set.
- DD-007 adds `semantic_models` and `outcome_contracts` and uses
  `RootFieldAccessRef` rather than `ProjectAccessRef` in both summaries.
- DD-009 binds defaults, keyword defaults, and closure cells directly through
  `binding_kind`; its load records use the thirteen-value closed `source_kind`
  universe and the exact literal/source/target presence partition.
- DD-011 and DD-016 expose the same six-role `ProviderReference` union and
  forbid `GENERATED_FIELD_ACCESSOR`.
- The forward transfer rule keeps the semantic projection of v2 `PCR-0530`
  under v3 `PCR-0111`; the inverse transfer rule keeps the semantic projection
  of v2 `PCR-0550` under v3 `PCR-0252`. The IDs are not stable identities; only
  the complete semantic projections are unchanged.

All other decision payload semantics, evidence, sources, aliases, coverage-row
membership, invariants, and lifecycle boundaries are preserved.

## Deterministic derived reconstruction

The migrator rebuilds templates, reference fields, discriminator branches,
compiled rules, all consumer lists, coverage links, manifests, DD-020 ordering,
and complete-key ordinals from semantic bodies. Predecessor IDs, JSON insertion
order, and review order are forbidden ordering inputs. Two independent
in-memory builds from the same exact v2 object and v3 schema digest must produce
identical canonical UTF-8 bytes with one trailing LF.

The exact global counts are 66 owners, 23 decisions, 264 coverage rows, 570
compiled rules, 461 discriminator branches, 312 reference fields, 207 schema
templates, 149 evidence references, 23 invariants, 6 source bindings, 146
evidence-binding expectations, and 16 legacy aliases. Rule provenance is the
disjoint partition 509 coverage-derived, 9 post-schema-extra, and 52
authority-closed rules. The owner-schema field-ordinal total is 1064.

After every derived collection and DD-020 ordering projection is rebuilt, the
migrator computes SHA-256 over canonical JSON for each allowed decision's
resolved semantic projection. The projection excludes the digest map itself,
derived rule and branch IDs, branch ordinals, branch links, and DD-020's
derived ID lists. It retains the decision ordinal and owner, template, and
field ordinals because those are normative ordering content. The exact
adjudicated digest map is:

| Decision | SHA-256 |
| --- | --- |
| DD-001 | `33734cc6dae5cee24754f73c31b01f81e941a7172f5fab6484bb3167749a8aca` |
| DD-004 | `41da7253e189dab7446f42180a517758f07aa975a78bd3b1024fb5888c607765` |
| DD-006 | `a1269dace56fef1babd331a3907b940380896d1244606ef9e4b1455407f4b291` |
| DD-007 | `73d7b9743182edc7921eddaf2939d4c029bcdcc5a5adc81eab738ce1c034b24e` |
| DD-009 | `306491c0c80714a386989536866e93913d2feea078d87359abc73485f4fef624` |
| DD-011 | `62f14d83340b7b1a2e15e18946899da1260ed2beccae69295b91017992f1172a` |
| DD-016 | `0e826100af9a6e9e706fb718651bbaf29e582b897ba0c8dcbc2c59b68c1a78cd` |
| DD-020 | `7b7b4660043c81a46fd227f82a639ed7c9e703f2140c817cced09a597254e58b` |

The complete `coverage_rows_by_id` collection is separately bound by canonical
projection digest
`1077a5f73e45b0b622a415a0ca2bb7867d7a2d32c3bbe8e6a0a92b426fdaf5e6`.
The migrator records this under
`normative_projection_digests_by_collection.coverage_rows_by_id`; the
validator freezes and independently recomputes it, so synchronized alteration
of a coverage row and its self-reported digest still fails.

The entire normative registry is additionally bound by canonical projection
digest
`1c342b39aef04dd8d6b664833b9a1b5e222b4d1ec1618d681ed35b17a665e7c1`.
That projection excludes only its own
`normative_registry_projection_sha256` field. The validator freezes and
independently recomputes this digest, so synchronized alteration of any nested
open payload and its self-reported digest fails with
`NORMATIVE_REGISTRY_PROJECTION_DIGEST_MISMATCH`.

## Independent validation

The independent validator may not import, execute, or derive expectations from
the migrator. It validates the frozen predecessor, JSON Schema, collection and
provenance counts, exact lifecycle, semantic allowlist, rule/branch/field
foreign keys, complete-key uniqueness, DD-001/004/006/007/009/011/016
contracts, transfer directions, ProviderReference role consumption, and
deterministic branch/rule ordering. It independently recomputes the eight
projection digests and rejects both an altered projection and an altered stored
digest, even when they agree with each other but differ from the adjudicated
constants.

For all 312 reference fields, the validator also requires map-key/internal-ID
identity, exact complete keys
`[owner_ordinal, template_ordinal, field_ordinal, 0]`, uniqueness of all
complete keys, and exact equality between the field payload projection and
DD-020's `schema_ordering.reference_field_ordinals`. Failures are respectively
`REFERENCE_FIELD_IDENTITY_MISMATCH`,
`REFERENCE_FIELD_COMPLETE_KEY_MISMATCH`, and
`REFERENCE_FIELD_DD020_PROJECTION_MISMATCH`.

The v3 schema has an independent validator-side digest anchor. Path validation
must execute the exact schema against the registry, including its closed
top-level and nested property sets; hashing a schema or accepting the
registry's own schema binding is insufficient. The dependency-free executor
supports every assertion keyword used by this frozen Draft 2020-12 schema and
fails on unsupported schema keywords. Exact source readers require a regular
file with `stat.S_IMODE(mode) == 0644`, rejecting symlinks, FIFO/device kinds,
and setuid, setgid, or sticky bits.

The validator fails closed with stable codes, including
`PREDECESSOR_IDENTITY_DRIFT`, `SEMANTIC_DIFF_OUTSIDE_ALLOWLIST`,
`DECISION_CENSUS_PATH_COUNT_MISMATCH`, `EXACT_ROLE_OWNER_MATRIX_MISMATCH`,
`EXACT_RECORD_FIELD_SEQUENCE_MISMATCH`, `CROSS_FIELD_MATRIX_NOT_COMPILED`,
`REFERENCE_OWNER_TUPLE_MISMATCH`, `ORPHAN_EXACT_ROLE`,
`REFERENCE_TYPE_NAME_MISMATCH`, `TRANSFER_DIRECTION_RULE_LINK_MISMATCH`,
`BRANCH_CANONICAL_ORDER_MISMATCH`, `RULE_CANONICAL_ORDER_MISMATCH`,
`NORMATIVE_PROJECTION_DIGEST_MISMATCH`,
`COVERAGE_PROJECTION_DIGEST_MISMATCH`, `V3_SCHEMA_IDENTITY_DRIFT`,
`JSON_SCHEMA_VALIDATION_FAILED`,
`GLOBAL_COLLECTION_COUNT_MISMATCH`, `STALE_V2_ATTESTATION_INHERITED`,
`STALE_SCOPE_V1_REUSED`, and `STOP_BOUNDARY_VIOLATION`.

## Completion boundary

A passing v3 package restores only eligibility to design and independently
review a new authority-amendment scope v2. Fresh exact-byte specification and
data/code-quality attestations must bind the final v3 subject. No downstream
authority, implementation, release, UI, manuscript, or submission permission
is implied.
