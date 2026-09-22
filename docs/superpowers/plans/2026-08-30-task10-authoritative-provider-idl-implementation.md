# Task 10 authoritative provider IDL and full-KAT closure plan

> **Execution rule:** this is a documentation-and-fixture correction. Production
> source and repository test files remain frozen. One implementer edits the
> shared authority bundle serially; fresh specification, data-quality, and
> mutation reviews follow every correction round.

**Goal:** close
`G18_CLOSED_REFERENCE_ALIAS_AND_LEAF_IDL_NOT_IN_AUTHORITY` without guessing by
freezing one machine-readable authority for all 66 owner tables, every embedded
record and every `RL` leaf, then build and independently verify the two full,
non-empty known-answer fixtures required by Task 10.

**Current prose authority:**
`docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md`
with ordinary SHA-256
`74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff`.
Section 5.6 replacements win over imported Section 5.5 shapes. If that SHA
changes before Task 1 starts, stop and rebind this plan rather than mixing
identities.

**Current measured gap:** the bound coverage artifact reports 66 blocked owner
tables, `0/66` actual typed records, `0/2` full KAT files, null policy/report
digests, and one unresolved gap (`G18`). The old reference-schema JSON is a
partial artifact bound to a superseded specification and is not an input.

**Authority topology:** the prose specification names a fixed authority-index
path but does not embed a future digest. The IDL manifest binds the final prose
SHA and every module SHA. The authority index binds the prose SHA and manifest
SHA and has no self-digest field. This removes the prose/manifest self-hash
cycle while leaving one externally hashable logical authority.

## Task 1: Freeze three independent owner inventories

**Files:**

- Read:
  `docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md`
- Create:
  `docs/superpowers/specs/idl/task10/v10/review/owner-inventory-00-20.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/review/owner-inventory-21-44.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/review/owner-inventory-45-65.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/review/inventory-gap-ledger.json`

- [ ] Verify the current prose SHA before reading any imported or replacement
  schema.
- [ ] For each of the 66 owners, record the exact top-level collection and
  record type, field sequence, cardinality, ordering rule, discriminator,
  subject label, nested records, enums, anchors, digests, and cross-record
  invariants with source-line provenance.
- [ ] Enumerate every `RL` leaf as a separate row containing owner table,
  containing record, exact or `ANY` discriminator, field path, cardinality,
  non-empty static target-owner subset, reference kind, and schema order.
- [ ] Mark unresolved target unions or branch semantics as `GAP`; do not infer
  them from field names, observed label values, or the stale partial fixture.
- [ ] Compare all three inventories for boundary overlap, missing ordinals,
  duplicate record names, missing imported records, and inconsistent target
  aliases.
- [ ] Stop before Task 2 if any prose ambiguity prevents a single exact row;
  amend the prose authority first and rerun all three inventories.

## Task 2: Define the modular IDL meta-contract

**Files:**

- Create:
  `docs/superpowers/specs/idl/task10/v10/meta-schema.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/owner-tables.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/enums.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/reference-aliases.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/README.md`

- [ ] Freeze JSON lexical key ordering, UTF-8 encoding, terminal newline,
  integer domain, tuple/list distinction, optional-field representation,
  union/discriminator syntax, schema-order rules, and digest preimages.
- [ ] Define exactly 66 `ClosedOwnerTable` literals in normative ordinal order.
- [ ] Define each enum once; reject undeclared values and aliases.
- [ ] Define every reference alias as a non-empty, duplicate-free subset of the
  66 owner tables. No alias may depend on observed fixture values.
- [ ] State that prose wins only for explanatory text; the final IDL modules
  win for machine field sequence, discriminator, target aliases, and schema
  order after the prose amendment in Task 6.

## Task 3: Encode every owner and embedded record

**Files:**

- Create:
  `docs/superpowers/specs/idl/task10/v10/records-bootstrap-project.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/records-runtime-state.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/records-contracts-semantics.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/records-capabilities-sites.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/reference-field-rules.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/cross-record-invariants.json`

- [ ] Encode at least one exact top-level typed record for every owner table;
  no owner may remain a prose-only import.
- [ ] Encode all nested records recursively and assign one stable schema name
  per distinct wire shape.
- [ ] Encode every union branch with an exact discriminator and reject ambiguous
  or overlapping branches.
- [ ] Encode one `ReferenceFieldRule` for every `RL` leaf from Task 1. Require
  exact owner, containing record, discriminator, path, cardinality, target
  alias or explicit target subset, kind, and unique schema order.
- [ ] Keep anchor backlinks and top-level validating copies outside the
  66-owner classification array while validating them independently.
- [ ] Encode the 14 canonical literal base kinds, legacy-sixteen lowering,
  recursive budgets, runtime-reference binding split, authorization backlinks,
  runtime-bearing owner matrix, opcode/site groups, root syntax inventory, and
  external-state filter exactly as the current replacement sections require.
- [ ] Preserve adverse, optional, and empty branches explicitly. Do not make a
  fixture easier by weakening a non-empty, reciprocal, or closure invariant.

## Task 4: Build a standard-library validator and mutation self-test

**Files:**

- Create:
  `docs/superpowers/specs/idl/task10/v10/validate_task10_provider_idl_v10.py`
- Create:
  `docs/superpowers/specs/idl/task10/v10/validation-mutations.json`

- [ ] Use only the Python standard library; do not add a project dependency.
- [ ] Validate module syntax, canonical bytes, owner ordinals, record-name
  uniqueness, field order, type references, enum references, discriminator
  totality, reference-alias closure, and invariant references.
- [ ] Recompute the complete `RL` leaf universe from record schemas and require
  a bijection with `reference-field-rules.json`; reject missing, extra,
  duplicate, discriminator-mismatched, empty-target, and invalid-target rows.
- [ ] Require all 66 owners to have at least one typed record and reject any
  stale spec SHA or mismatched module hash.
- [ ] Add deterministic negative mutations for each validation class and
  require the exact failure code. A validator that accepts its own mutations
  is a hard failure.
- [ ] Run:

  ```bash
  .venv/bin/python \
    docs/superpowers/specs/idl/task10/v10/validate_task10_provider_idl_v10.py \
    --self-test
  ```

  Expected: exit `0`, `66/66` owners, full `RL`-rule bijection, and every
  negative mutation rejected for its frozen code.

## Task 5: Generate and independently verify the full KATs

**Files:**

- Create:
  `docs/superpowers/specs/idl/task10/v10/build_task10_full_kats_v10.py`
- Create:
  `docs/superpowers/specs/idl/task10/v10/verify_task10_full_kats_v10.py`
- Create:
  `docs/superpowers/specs/fixtures/task10-provider-audit-policy-full-nonempty-v10.kat.json`
- Create:
  `docs/superpowers/specs/fixtures/task10-provider-audit-report-stable-full-wire-v10.kat.json`

- [ ] Build a policy fixture in which all 66 owner tables are non-empty and
  every legal discriminator/reference family is exercised at least once.
- [ ] Build a stable full-wire report bound to the exact policy, registries,
  graph manifests, site manifests, runtime anchors, findings, and all required
  digests.
- [ ] Keep construction and verification algorithms independent: the verifier
  parses the IDL and recomputes canonical bytes, reference closure, graphs,
  ordinals, digests, and report bindings without importing builder functions.
- [ ] Run the builder once, then make the output files read-only for the
  verification sequence.
- [ ] Run:

  ```bash
  .venv/bin/python \
    docs/superpowers/specs/idl/task10/v10/build_task10_full_kats_v10.py
  .venv/bin/python \
    docs/superpowers/specs/idl/task10/v10/verify_task10_full_kats_v10.py
  ```

  Expected: exit `0`; `66/66` non-empty owners; no dangling reference; policy
  and report canonical round-trip equality; non-null policy/report domain
  digests.
- [ ] Mutate at least one owner ordinal, discriminator, target alias, graph
  edge, registry digest, finding detail, and report digest. Require independent
  verification to fail for the intended reason.

## Task 6: Freeze the composite authority without a digest cycle

**Files:**

- Create:
  `docs/superpowers/specs/idl/task10/v10/manifest.json`
- Create:
  `docs/superpowers/specs/idl/task10/v10/authority-index.json`
- Modify:
  `docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md`
- Modify:
  `docs/superpowers/specs/fixtures/task10-provider-audit-full-kat-coverage.json`
- Modify:
  `docs/superpowers/specs/fixtures/2026-08-30-task10-provider-audit-full-kat-manifest.md`
- Modify:
  `docs/superpowers/plans/2026-08-28-task10-cross-module-operation-capsules-implementation.md`

- [ ] Amend the prose once to name the fixed authority-index path, declare the
  IDL precedence boundary, close G18, and preserve every M0–M2/M6/UI/release/
  manuscript HOLD.
- [ ] Freeze the amended prose SHA; do not edit it again during this sequence.
- [ ] Write the manifest with that final prose SHA and every normative module
  SHA. Do not include the manifest's own digest.
- [ ] Write the authority index with the final prose SHA, manifest SHA, KAT
  SHA values, validator SHA, and independent-verifier SHA. Do not include the
  authority index's own digest.
- [ ] Rebuild coverage from current bytes. Require one closed G18, zero open
  gaps, `66/66` actual typed records, `2/2` KATs, and non-null domain digests.
- [ ] Mark the old partial reference-schema artifact `SUPERSEDED_NON_AUTHORITY`;
  retain it as adverse provenance and never silently rewrite it into the new
  authority.
- [ ] Link this plan from the parent Task 10 plan without checking Task 10 or
  promoting filter-net rules.

## Task 7: Same-byte verification and independent review

- [ ] Finish every file-writing step before hashing or reviewing.
- [ ] Run the IDL validator self-test, independent KAT verifier, canonical JSON
  round trips, SHA checks, and `git diff --check` serially on unchanged bytes.
- [ ] Run the unchanged repository baseline:

  ```bash
  .venv/bin/python -m pytest -q
  ```

  Expected: the previously observed `2435 passed, 1 skipped` or a higher count
  with zero failures; this docs-only task must not alter production behavior.
- [ ] Confirm with `git status --short` that no production or repository test
  path changed during this IDL sequence.
- [ ] Obtain a fresh specification-compliance review against the exact
  authority-index SHA. Require `0 BLOCKER / 0 MAJOR / 0 MINOR`.
- [ ] Obtain a fresh data/code-quality review of canonicalization, validator
  independence, mutation strength, and false-green risks. Require
  `0 BLOCKER / 0 MAJOR / 0 MINOR`.
- [ ] Obtain a fresh mutation/adversarial review of the two KATs and every
  reference branch. Require `0 BLOCKER / 0 MAJOR / 0 MINOR`.
- [ ] After any correction, invalidate all three reviews, rerun Tasks 4–7, and
  review the new exact hashes.

## Task 8: Docs-only closure and implementation authorization gate

- [ ] Prepare a docs-only diff inventory and SHA table. Exclude every existing
  dirty production/test path from staging.
- [ ] Record exact commands, exit codes, environment versions, counts,
  non-null domain digests, adverse mutations, and review dispositions.
- [ ] Present the same-byte docs-only candidate for user approval.
- [ ] Only after explicit approval may the separate production TDD plan resume
  RED/GREEN work. This plan never authorizes UI, persistence, M6, public
  release, manuscript drafting, or submission.

## Stop conditions

Stop and return to specification work if any of the following occurs:

- an `RL` leaf requires a guessed target owner or guessed discriminator;
- the validator and KAT builder share decision code that could false-green the
  same defect;
- fewer than 66 owners are non-empty or fewer than two full KATs exist;
- a canonical or domain digest is null, unstable, or computed after a writer
  has changed its input;
- the amended prose, manifest, authority index, fixtures, coverage, or reviews
  do not bind one exact byte set;
- production source or repository tests must change to make this docs-only
  gate pass; or
- any review reports a blocker, major, or minor finding.

Passing this plan closes only G18 and authorizes consideration of the next
Task 10 TDD slice. It does not close Task 10, M0–M2, M6, UI, release, the
SoftwareX manuscript, or submission readiness.
