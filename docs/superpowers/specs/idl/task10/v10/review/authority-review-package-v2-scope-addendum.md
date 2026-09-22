# Task 10 authority review package v2 scope addendum

Status: `APPROVED_RECOMMENDED_SUCCESSOR_ROUTE`

This addendum authorizes a representation-only successor to the exact v1
decision-review package. It does not amend the Task 10 prose authority, create
authority IDL, create KATs, alter production software, or promote any review
input into current authority.

## Approval and reason

The author instructed the active P3/SelCal task to continue by the recommended
route and to use subagent-driven, high-specification execution. The exact v1
registry subsequently obtained an independent specification-compliance verdict
of `0 BLOCKER / 0 MAJOR / 0 MINOR`, but an independent data/code-quality review
returned `0 BLOCKER / 5 MAJOR / 1 MINOR`. The quality findings require a
normalized successor package rather than further mutation of the reviewed v1
bytes.

## Frozen predecessor

The following predecessor artifacts are immutable historical evidence for this
migration and must never be reformatted, regenerated, overwritten, or described
as scientific authority:

- `authority-design-decision-registry-v1.json`
  - SHA-256 `047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398`
- `authority-design-decision-matrix-v1.md`
  - SHA-256 `8b75baf1db9425daddcfd150f0f3c4638684e42e15fa717c2c2044fb3a8f3287`

The repository is intentionally dirty. Git cleanliness or a new commit is not
used as a substitute for content identity. Every v2 generator and validator
must first verify the exact seven paths and SHA-256 values in
`authority-review-package-v2-baseline.json`; any mismatch is an immediate
`BASELINE_HASH_DRIFT` stop. This preserves user-owned unrelated changes while
making the migration input deterministic.

## Allowed outputs

Only the following successor-package paths may be created or modified during
the v2 quality-closure sequence:

- `docs/superpowers/plans/2026-08-30-task10-authority-review-package-v2-quality-closure.md`
- `docs/superpowers/specs/idl/task10/v10/review/authority-review-package-v2-scope-addendum.md`
- `docs/superpowers/specs/idl/task10/v10/review/authority-review-package-v2-baseline.json`
- `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v2.json`
- `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-index-v2.md`
- `docs/superpowers/specs/idl/task10/v10/review/schema/authority-design-decision-registry-v2.schema.json`
- `docs/superpowers/specs/idl/task10/v10/review/schema/authority-design-decision-review-attestation-v1.schema.json`
- `docs/superpowers/specs/idl/task10/v10/review/migrate_authority_decision_registry_v1_to_v2.py`
- `docs/superpowers/specs/idl/task10/v10/review/validate_authority_review_package_v2.py`
- `docs/superpowers/specs/idl/task10/v10/review/attestations/README.md`
- `docs/superpowers/specs/idl/task10/v10/review/attestations/sha256-*/review-*.json`
- `tests/task10/test_authority_review_package_v2.py`

The hash-named attestation directory is instantiated only after the v2 registry
bytes are frozen. An independent reviewer remains read-only and returns a
verdict. The persistent implementation writer may materialize that verdict as a
new append-only attestation without changing reviewer identity, scope, verdict,
finding counts, or effect; no prior attestation may be edited.

## Required invariants

The migration is permitted only if all of the following remain true:

1. `v1 -> v2 -> legacy-v1` reproduces the exact v1 registry bytes.
2. The v2 package retains 66 owners, 23 decisions, 264 coverage rows, 570
   compiled rules, 312 reference fields, 209 schema templates, and 461
   discriminator branches.
3. Rule provenance remains the exact disjoint partition
   `509 COVERAGE_DERIVED + 9 POST_SCHEMA_EXTRA +
   52 AUTHORITY_CLOSED_INVENTORY = 570`.
4. Every rule object is defined exactly once in v2; decisions, coverage rows,
   branches, manifests, and indexes reference IDs only.
5. Every evidence locator names one exact source binding. Decision-only design
   evidence must remain decision-only and cannot acquire an authority line.
6. The v2 JSON is the sole normative successor review artifact. Markdown is a
   concise `NON_NORMATIVE_DERIVED_VIEW` and must not embed the registry.
7. Review verdicts are detached attestations bound to exact subject and schema
   hashes. No mutable review result is stored inside the reviewed registry.
8. The following states remain unchanged:
   `REVIEW_DECISION_INPUT_NOT_AUTHORITY`,
   `AUTHORITY_AMENDMENT_NOT_YET_REVIEWED`,
   `STOP_BEFORE_AUTHORITY_IDL_AND_KATS`,
   `authority_idl_allowed=false`, and `kats_allowed=false`.

## Forbidden actions

This addendum does not authorize:

- editing the seven hash-bound baseline inputs;
- editing production source or existing production tests;
- changing any scientific decision, target table, reference kind,
  discriminator meaning, nullability, cardinality, or schema order;
- creating or amending authority prose, authority IDL, KATs, fixtures, M3-M8
  product code, UI, release artifacts, or manuscript content;
- selecting a licence, publishing a repository, creating a DOI, uploading to a
  portal, or making a SoftwareX readiness claim;
- committing unrelated dirty-worktree changes.

## Gate sequence

1. Independently review this addendum, the baseline manifest, and the v2
   implementation plan against their exact hashes.
2. Execute the reviewed plan with test-first development and one persistent
   implementation writer for all writable v2 artifacts. All review subagents
   are read-only.
3. Finish every reviewed-subject, generator, validator, index, and focused-test
   write before freezing v2 subject hashes. Detached attestations and plan
   checkbox updates occur afterward and never alter the reviewed subject bytes.
4. Obtain fresh exact-byte specification and data/code-quality reviews.
5. Create detached attestations only from those actual review results.
6. Advance to the prose-authority amendment only after both v2 reviews return
   `0 BLOCKER / 0 MAJOR / 0 MINOR` on the same registry bytes.
