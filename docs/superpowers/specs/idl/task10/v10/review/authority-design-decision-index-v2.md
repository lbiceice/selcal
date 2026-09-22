# Task 10 authority design decision index v2

Status: `NON_NORMATIVE_DERIVED_VIEW`

This file is a concise navigation surface derived from the canonical v2 
registry. It is not authority, not an IDL, not a KAT, and not a substitute 
for the normative JSON review input.

## Exact subject bindings

| Artifact | Path | SHA-256 |
|---|---|---|
| Registry | `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v2.json` | `77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5` |
| Registry schema | `docs/superpowers/specs/idl/task10/v10/review/schema/authority-design-decision-registry-v2.schema.json` | `81f8e1e68fc1a8cecf964a542feaeb601431b7c2e74726f4e0940f163b23b967` |

## Boundary

- Artifact state: `REVIEW_DECISION_INPUT_NOT_AUTHORITY`
- Authority amendment: `AUTHORITY_AMENDMENT_NOT_YET_REVIEWED`
- Machine stop: `STOP_BEFORE_AUTHORITY_IDL_AND_KATS`
- Authority IDL allowed: `false`
- KATs allowed: `false`

## Counts

| Surface | Count |
|---|---:|
| Owners | 66 |
| Decisions | 23 |
| Coverage rows | 264 |
| Compiled rules | 570 |
| Reference fields | 312 |
| Schema templates | 209 |
| Discriminator branches | 461 |

Rule provenance remains `509 COVERAGE_DERIVED + 9 POST_SCHEMA_EXTRA + 
52 AUTHORITY_CLOSED_INVENTORY = 570`.

## Decision index

| Decision | Title | Status | Reference kinds | Rules | Branches |
|---|---|---|---|---:|---:|
| T10-G18-DD-001 | Identity-anchor retyping | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | ANCHOR_NOT_RL | 0 | 0 |
| T10-G18-DD-002 | ClassBinding, inheritance, ProjectClass, and ABC | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 52 | 35 |
| T10-G18-DD-003 | ClassMemberBindingRef | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 38 | 36 |
| T10-G18-DD-004 | CapturedEnvironmentRef | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 5 | 5 |
| T10-G18-DD-005 | Intrinsic receiver and argument contracts | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 99 | 26 |
| T10-G18-DD-006 | Generated artifact, default, Enum, and provider refs | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 32 | 28 |
| T10-G18-DD-007 | Project access, slot, and ProjectDescriptor | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 28 | 31 |
| T10-G18-DD-008 | RuntimeLocator root and access | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 26 | 24 |
| T10-G18-DD-009 | Generated callback default, load, and transfer matrices | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 32 | 23 |
| T10-G18-DD-010 | SiteRef | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 25 | 17 |
| T10-G18-DD-011 | ProviderReference | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 83 | 82 |
| T10-G18-DD-012 | Authorization graph derivation | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | DERIVED_META_INDEX_NOT_CLASSIFIED | 0 | 0 |
| T10-G18-DD-013 | Structural-site direction | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 18 | 8 |
| T10-G18-DD-014 | Capability outcomes, iterable backlinks, and OperationOutcome | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES, VALIDATES | 16 | 8 |
| T10-G18-DD-015 | POP_ITEM branch matrix | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 11 | 8 |
| T10-G18-DD-016 | Context enter and exit protocol branches | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 7 | 7 |
| T10-G18-DD-017 | SourceSpan | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | NO_ASSIGNED_NULL_ROW | 0 | 0 |
| T10-G18-DD-018 | Structured discriminator grammar | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | NO_ASSIGNED_NULL_ROW | 0 | 461 |
| T10-G18-DD-019 | Enum rank and rankless semantics | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | NO_ASSIGNED_NULL_ROW | 0 | 0 |
| T10-G18-DD-020 | Explicit schema_field_order compiler | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | NO_ASSIGNED_NULL_ROW | 52 | 27 |
| T10-G18-DD-021 | Finite ValueExpression template recursion | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | NO_ASSIGNED_NULL_ROW | 0 | 0 |
| T10-G18-DD-022 | Root constructor, gate, and iterable producer | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 21 | 16 |
| T10-G18-DD-023 | Guard, exception operation, implementation, and state dependency refs | APPROVED_DECISION_INPUT_FOR_AUTHORITY_AMENDMENT | AUTH_REQUIRES | 25 | 25 |

## v1 to v2 representation changes

| v1 review surface | v2 representation | Scientific effect |
|---|---|---|
| Repeated rule objects in decisions and coverage rows | One canonical rule map plus ordered ID references | None |
| Scalar/list reference-kind overload | Arrays only | None |
| String/object branch-instance overload | Typed branch IDs and case-label arrays | None |
| Unbound authority line strings | Content-addressed source plus locator references | None |
| Review result inside reviewed bytes | Detached exact-hash attestation | None |
| Full JSON mirror in Markdown | Concise index only | None |

## Quality finding closure targets

| Prior finding | v2 control | Current local evidence |
|---|---|---|
| Oversized Markdown mirror | Size and forbidden-dump test | Implemented, pending independent review |
| 509 repeated rule bodies | Single-definition rule map | Implemented, pending independent review |
| No enforceable schema | Closed versioned schema and validator | Implemented, pending independent review |
| Lines not bound to sources | Source IDs bind logical path and SHA-256 | Implemented, pending independent review |
| Self-invalidating embedded verdict | Detached attestation topology | Specified, no PASS attestation yet |
| Prose-only invariants | Executable invariant records and mutations | Implemented, pending independent review |
| Open invariant assertion controls | Kind-discriminated closed assertion schemas | Implemented, pending independent review |
| Validator-local normalized drift | Independent rule/semantic projections plus exact deterministic regeneration | Implemented, pending independent review |
| Partial review-byte binding | Ten fixed-role exact-hash package bindings | Implemented, pending independent review |
| Persisted attestation verification gap | Separate PREWRITE and exact-byte READBACK modes | Implemented, pending independent review |

## Detached review location

After these registry bytes are frozen, reviewer verdicts are recorded under 
`attestations/sha256-77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5/review-<attestation-id>.json`. 
A detached attestation does not promote this package to authority and must 
not alter the registry or schema bytes.

## Stop warning

`STOP_BEFORE_AUTHORITY_IDL_AND_KATS` remains binding. No authority prose, 
authority IDL, KAT, production implementation, UI, release, or manuscript 
work is authorized by this index.
