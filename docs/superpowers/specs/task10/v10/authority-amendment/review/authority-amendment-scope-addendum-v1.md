# Task 10 G18 authority-amendment scope addendum v1

Status: `SCOPE_CANDIDATE_PENDING_INDEPENDENT_REVIEW`

Effect: `AUTHORING_SCOPE_ONLY_NO_AUTHORITY_PROMOTION`

## Decision

The current Task 10 prose authority is an uncommitted, hash-bound input to the
completed v2 registry review. It must not be edited in place. The only eligible
route is a new full successor whose first `298339` bytes reproduce the current
prose exactly and whose appended Section 12 is independently reviewable.

This scope package does not create that successor. It freezes only the
predecessor/input identities, the 23-decision target map, the future write
allowlist, and the validation sequence required before successor authoring may
begin.

## Exact predecessor and reviewed inputs

- predecessor prose: SHA-256 `74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff`,
  `298339` bytes;
- v2 decision registry: SHA-256 `77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5`;
- registry schema: SHA-256 `81f8e1e68fc1a8cecf964a542feaeb601431b7c2e74726f4e0940f163b23b967`;
- specification-review attestation: SHA-256 `1c986a5d8e0325d93f2888bd4f3a8d773c102dc399519c32f32bfe09845ffd7f`;
- data/code-quality attestation: SHA-256 `4d5391d89974850e22caad046fbc30274f4aa31c0c40b3893d52f558e44388d8`.

Both attestations have effect `NO_AUTHORITY_PROMOTION`. They prove the exact
registry review package passed; they do not approve successor prose.

## Scope boundary

The current scope has no `MODIFY_EXISTING` paths. Its seven `CREATE_OR_UPDATE`
paths are exactly the scope-review files named in the paired plan and target
map. No successor file may exist at the scope-review gate.

The baseline additionally freezes a repository-wide deny-by-default inventory
of every Git tracked or non-ignored file outside those seven current outputs.
Every protected identity binds ordinary-file kind, permission mode, and byte
digest. A symbolic link at the leaf or any repository-relative ancestor fails
before a linked target can be treated as evidence. The validator walks each
repository-relative component with no-follow descriptors, reads from the same
file descriptor checked by `fstat`, rejects identity change during the read,
and then confirms through a fresh no-follow walk that the path still maps to
the same inode. Any path-set, kind, mode, identity, or byte drift in that
inventory fails before semantic reads.

After two independent scope reviews return `0/0/0` on the same seven hashes,
only five future candidate-authoring paths may be created. They are enumerated
in the target map. Their prewrite absence uses `lexists` semantics and therefore
rejects dangling links and linked ancestors. Every other existing path is
protected.

The prior combined IDL/KAT plan is frozen as
`FROZEN_NONEXECUTABLE_DOWNSTREAM_DRAFT`; its order may not be executed.

## Normative transfer rule

Each of the 23 decision records must be transferred exactly once into
self-contained successor prose. The successor must restate the operative wire,
field, owner, discriminator, presence, cardinality, ordering, invariant, and
negative constraints needed to implement the decision. A decision ID, registry
path, registry hash, `PCR-*` rule ID, or count may serve only as provenance or
derived conformance evidence.

The registry remains `REVIEW_DECISION_INPUT_NOT_AUTHORITY`. Its 570 rules and
the exact `509 + 9 + 52` partition are conformance evidence that the prose
candidate compiles to the reviewed closure; they cannot replace the prose
semantics.

## Review timing clarification

An `AUTHORITY_AMENDMENT_EXACT_BYTE_REVIEW` may occur before IDL and KAT solely
to review the proposed prose amendment. It is not the final composite machine-
authority review and does not satisfy the existing requirement for full KATs
before final implementation-readiness acceptance.

## Preserved stop boundary

Throughout this scope and successor-authoring sequence:

- `authority_idl_allowed=false`;
- `kats_allowed=false`;
- `implementation_allowed=false`;
- `machine_stop_decision=STOP_BEFORE_AUTHORITY_IDL_AND_KATS`.

No M0-M2, M6, UI, release, manuscript, or SoftwareX readiness state changes.

## Gate sequence

1. Build and test this seven-file scope package.
2. Freeze its hashes and obtain two independent `0/0/0` scope reviews.
3. Only then TDD the successor builder and independent validator.
4. Freeze the successor candidate without modifying the predecessor.
5. Obtain new exact-byte authority-content reviews.
6. Require a separately scoped explicit adoption record before any IDL-scope
   work is considered.
