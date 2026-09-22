# Task 10 authority-prose amendment exact-review plan

> **Current state:** `SCOPE_PACKAGE_CANDIDATE / NO AUTHORITY PROMOTION`.
> This plan does not authorize IDL, KAT, production, UI, release, manuscript,
> or submission work.

**Goal:** create and independently review one append-only full successor of the
current Task 10 prose authority without modifying the exact predecessor bytes,
without treating the reviewed decision registry as authority, and without
crossing the existing `STOP_BEFORE_AUTHORITY_IDL_AND_KATS` boundary.

## Frozen facts

- Current prose predecessor SHA-256:
  `74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff`.
- Current predecessor length: `298339` bytes.
- Reviewed v2 decision registry SHA-256:
  `77229b74bf07a75793bb8dd142312f83e682325977474db3637fcb84d80cc8f5`.
- The two registry attestations are `PASS 0/0/0`, but both have effect
  `NO_AUTHORITY_PROMOTION`.
- The earlier IDL/KAT plan at
  `docs/superpowers/plans/2026-08-30-task10-authoritative-provider-idl-implementation.md`
  is a `FROZEN_NONEXECUTABLE_DOWNSTREAM_DRAFT`: it creates IDL/KAT before the
  enabling prose amendment and may not be executed in that order.

## Task 0: Freeze the scope-review package

Allowed current writes are exactly seven files:

1. this plan;
2. `docs/superpowers/specs/task10/v10/authority-amendment/review/authority-amendment-scope-addendum-v1.md`;
3. `docs/superpowers/specs/task10/v10/authority-amendment/review/authority-amendment-baseline-v1.json`;
4. `docs/superpowers/specs/task10/v10/authority-amendment/review/authority-amendment-target-map-v1.json`;
5. `docs/superpowers/specs/task10/v10/authority-amendment/review/schema/authority-amendment-target-map-v1.schema.json`;
6. `docs/superpowers/specs/task10/v10/authority-amendment/review/validate_authority_amendment_scope_v1.py`;
7. `tests/task10/test_authority_amendment_scope_v1.py`.

- [ ] Write target-map tests before the validator and observe RED.
- [ ] Implement baseline-first validation and make the focused tests GREEN.
- [ ] Freeze exact hashes only after all six non-baseline files stop changing.
- [ ] Create the baseline last; it must not contain its own digest.
- [ ] Require predecessor, decision registry, two attestations, adverse
  provenance, and source/test tree digests to match before semantic reads.
- [ ] Freeze a repository-wide deny-by-default digest over every Git tracked or
  non-ignored file except the exact seven current outputs. The identity record
  must bind ordinary-file kind, permission mode, and content hash; any leaf or
  ancestor symbolic link is forbidden. Evidence bytes must be read from the
  same no-follow descriptor whose identity is checked with `fstat`, followed by
  a fresh no-follow path-to-inode confirmation. Require the five future outputs
  to be absent under `lexists` semantics so a dangling link cannot count as
  absent.

## Task 1: Independent scope review

- [ ] Obtain one independent specification/authority review of the exact seven
  scope-package files.
- [ ] Obtain one independent data/code-quality review of baseline ordering,
  target-map completeness, mutation strength, and protected-tree coverage.
- [ ] Require `0 BLOCKER / 0 MAJOR / 0 MINOR` from both reviewers on the same
  hashes.
- [ ] Any correction invalidates both reviews and requires a new exact-byte
  round.

No successor-authoring output may be created before Task 1 passes.

## Task 2: TDD the successor authoring tools

After Task 1 passes, the only newly authorized candidate-authoring paths are:

- `docs/superpowers/specs/task10/v10/authority-amendment/build_authority_prose_candidate_v1.py`;
- `docs/superpowers/specs/task10/v10/authority-amendment/validate_authority_prose_candidate_v1.py`;
- `tests/task10/test_authority_prose_amendment_v1.py`;
- `docs/superpowers/specs/2026-08-30-task10-deny-by-default-provider-proof-design-g18-authority-candidate.md`;
- `docs/superpowers/specs/task10/v10/authority-amendment/authority-prose-amendment-result-v1.json`.

- [ ] First write RED tests for exact predecessor prefix, append offset,
  23-decision completeness, self-contained normative restatement, forbidden
  path drift, and STOP preservation.
- [ ] Implement one deterministic builder and a logically independent
  validator. The validator may not import the builder.
- [ ] The successor must begin with the exact `298339` predecessor bytes and
  may add content only after that offset.
- [ ] Every decision must be restated as operative prose. Decision IDs and
  `PCR-*` IDs are provenance only and cannot carry `MUST` or `SHALL` by
  reference.

## Task 3: Freeze the successor candidate

- [ ] Finish every writer before hashing.
- [ ] Prove predecessor bytes are unchanged.
- [ ] Freeze successor, appended-section, tools, test, and result-manifest
  hashes.
- [ ] Preserve the old adverse coverage, old KAT manifest, partial schema,
  inventories, review package, production source, and existing tests exactly.
- [ ] Keep lifecycle state `AUTHORITY_CANDIDATE_NOT_ADOPTED` and
  `authority_idl_allowed=false`, `kats_allowed=false`.

## Task 4: Exact-byte authority-content review

- [ ] Obtain fresh independent specification and data/code-quality reviews of
  the exact successor candidate.
- [ ] These reviews are new authority-content reviews; the registry review
  attestations cannot be reused.
- [ ] Require `0/0/0` on the same successor hash. A correction invalidates all
  downstream reviews.
- [ ] Record review evidence in a later, separately scoped detached-attestation
  package.

## Task 5: Adoption boundary

Even a reviewed successor remains a candidate until an explicit adoption
record binds its exact hash and the new review evidence. Adoption may permit a
separate IDL-scope design; it does not itself create an IDL or KAT and does not
close M0-M2, M6, UI, release, manuscript, or SoftwareX readiness.

## Hard stops

Stop immediately if the predecessor changes, an existing file is overwritten,
a decision is incorporated only by registry reference, one of the 23 decision
targets is missing or duplicated, a protected tree drifts, IDL/KAT output is
created, or any reviewer reports a finding.
