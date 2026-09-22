# Task 10 authority review package v2 quality-closure implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans with one persistent implementation writer for Tasks 1–8. Subagents may perform read-only specification and quality reviews but must not edit package artifacts. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the exact, specification-compliant Task 10 v1 decision registry into a normalized, schema-bound, reviewable v2 package without changing any scientific or authority decision and close the independent `0 BLOCKER / 5 MAJOR / 1 MINOR` quality hold.

**Architecture:** Preserve the v1 JSON and Markdown byte-for-byte as immutable historical evidence. Generate one canonical, two-space-indented v2 JSON in which each compiled rule exists once, bind it to a versioned JSON Schema, derive a concise non-normative Markdown index, and store review verdicts in separate hash-bound attestations. A standard-library migrator and validator must prove `v1 -> v2 -> legacy-v1` exact-byte round-trip, the `509 + 9 + 52 = 570` rule partition, all foreign keys, evidence-source bindings, declarative invariants, and the unchanged STOP boundary.

**Tech Stack:** Python 3 standard library, JSON Schema 2020-12 documents, SHA-256, deterministic UTF-8/LF JSON, pytest for test-first development, Markdown generated from canonical JSON.

---

## Frozen identities and non-goals

- v1 registry: `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v1.json`
  - SHA-256: `047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398`
- v1 matrix: `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-matrix-v1.md`
  - SHA-256: `8b75baf1db9425daddcfd150f0f3c4638684e42e15fa717c2c2044fb3a8f3287`
- Frozen authority/inventory/ledger inputs remain at their current five hashes.
- This work is representation-only. It must retain:
  - `REVIEW_DECISION_INPUT_NOT_AUTHORITY`
  - `AUTHORITY_AMENDMENT_NOT_YET_REVIEWED`
  - `STOP_BEFORE_AUTHORITY_IDL_AND_KATS`
  - `authority_idl_allowed=false`
  - `kats_allowed=false`
- It must retain exactly 66 owners, 23 decisions, 264 coverage rows, 570 compiled rules, 312 reference fields, 209 templates, 461 discriminator branches, and provenance partition `509 + 9 + 52 = 570`.
- It must not edit the prose authority, inventories, ledger, fixtures, production source, repository tests, IDL, KATs, UI, release files, or manuscript.

## File map

**Preserve without modification**

- `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v1.json`
- `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-matrix-v1.md`

**Create**

- `docs/superpowers/specs/idl/task10/v10/review/authority-review-package-v2-scope-addendum.md`
  - Explicit successor authorization, allowed outputs, forbidden actions, and gate order.
- `docs/superpowers/specs/idl/task10/v10/review/authority-review-package-v2-baseline.json`
  - Exact seven-file dirty-worktree identity manifest; a hash gate, not an authority or commit substitute.
- `docs/superpowers/specs/idl/task10/v10/review/schema/authority-design-decision-registry-v2.schema.json`
  - Normative v2 data-shape contract.
- `docs/superpowers/specs/idl/task10/v10/review/schema/authority-design-decision-review-attestation-v1.schema.json`
  - Normative detached-review contract.
- `docs/superpowers/specs/idl/task10/v10/review/migrate_authority_decision_registry_v1_to_v2.py`
  - Exact-hash-bound, deterministic, semantics-preserving migrator and legacy rehydrator.
- `docs/superpowers/specs/idl/task10/v10/review/validate_authority_review_package_v2.py`
  - Standard-library package, schema-subset, invariant, mutation, and attestation validator.
- `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v2.json`
  - Single canonical normative review input.
- `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-index-v2.md`
  - Concise, non-normative human index; no embedded full JSON.
- `docs/superpowers/specs/idl/task10/v10/review/attestations/README.md`
  - Append-only attestation and supersession rules.
- `tests/task10/test_authority_review_package_v2.py`
  - Test-first unit, round-trip, and mutation gates for the real package.

**Create only after exact-byte independent review**

- `docs/superpowers/specs/idl/task10/v10/review/attestations/sha256-<registry-sha256>/review-<attestation-id>.json`
  - One immutable file per exact reviewer/scope/verdict. The final directory name uses the actual v2 registry SHA produced by Task 6.

## Writer topology

- One persistent implementation writer owns every writable path in this plan
  from the first RED test through the final frozen subject bytes.
- Review subagents are read-only. They return findings to the persistent writer;
  they do not patch tests, schemas, generators, registries, indexes, plans, or
  attestations.
- Tasks are sequential checkpoints for one writer, not fresh-writer handoffs.
  This prevents hidden generator/schema/test drift across shared artifacts.

### Task 0: Approve successor scope and freeze a hash-bound dirty-worktree baseline

**Files:**

- Create: `docs/superpowers/specs/idl/task10/v10/review/authority-review-package-v2-scope-addendum.md`
- Create: `docs/superpowers/specs/idl/task10/v10/review/authority-review-package-v2-baseline.json`
- Read: the seven exact files named in the baseline manifest

- [ ] **Step 1: Confirm the scope addendum authorizes every planned output and nothing broader**

The allowed-output set must include this plan, the scope addendum, the baseline
manifest, two schemas, migrator, validator, v2 registry, concise index,
attestation README/files, and one new focused test file. The forbidden set must
retain the prose authority, inventories, ledger, v1 pair, fixtures, existing
production tests, source code, IDL, KATs, UI, release, and manuscript.

- [ ] **Step 2: Parse the baseline manifest and require seven unique exact paths**

Run:

```bash
jq -e '
  .artifact_status == "HASH_BOUND_DIRTY_WORKTREE_BASELINE_NOT_AUTHORITY" and
  .machine_stop_decision == "STOP_ON_ANY_BASELINE_HASH_DRIFT" and
  (.files | length) == 7 and
  ([.files[].path] | unique | length) == 7 and
  ([.files[].sha256 | test("^[0-9a-f]{64}$")] | all)
' docs/superpowers/specs/idl/task10/v10/review/authority-review-package-v2-baseline.json
```

Expected: exit `0` and output `true`.

- [ ] **Step 3: Recompute every baseline hash from current bytes**

Use one read-only script that loads the manifest, resolves paths relative to
the repository root, and compares SHA-256. Expected output:

```text
BASELINE_FILES=7
BASELINE_HASH_DRIFT=0
BASELINE_STATUS=PASS_DIRTY_WORKTREE_HASH_BOUND
```

The disclosed `MODIFIED_TRACKED`/`UNTRACKED_EXACT_BYTES` states must match
`git status --short` for these paths. A clean-tree claim is forbidden.

- [ ] **Step 4: Freeze and report exact addendum, baseline, and plan hashes**

No file may include its own digest. Review binds the three paths and external
SHA-256 values, avoiding a self-hash cycle.

- [ ] **Step 5: Obtain an independent read-only plan/scope/baseline review**

Require `0 BLOCKER / 0 MAJOR / 0 MINOR`. Any correction invalidates the three
hashes and requires this Task 0 review to be repeated. No v2 implementation may
start before this pass.

### Task 1: Freeze v1 history and write failing identity tests

**Files:**

- Preserve: `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v1.json`
- Preserve: `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-matrix-v1.md`
- Create: `tests/task10/test_authority_review_package_v2.py`
- Create: `docs/superpowers/specs/idl/task10/v10/review/migrate_authority_decision_registry_v1_to_v2.py`

- [ ] **Step 1: Add the exact v1 byte-identity test**

```python
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "docs/superpowers/specs/idl/task10/v10/review"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_v1_review_evidence_is_immutable() -> None:
    assert digest(REVIEW / "authority-design-decision-registry-v1.json") == (
        "047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398"
    )
    assert digest(REVIEW / "authority-design-decision-matrix-v1.md") == (
        "8b75baf1db9425daddcfd150f0f3c4638684e42e15fa717c2c2044fb3a8f3287"
    )
```

- [ ] **Step 2: Add a failing test for the missing migrator identity contract**

```python
def test_migrator_binds_exact_v1_hashes() -> None:
    module = load_migrator()
    assert module.V1_REGISTRY_SHA256 == (
        "047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398"
    )
    assert module.V1_MATRIX_SHA256 == (
        "8b75baf1db9425daddcfd150f0f3c4638684e42e15fa717c2c2044fb3a8f3287"
    )
```

- [ ] **Step 3: Run the focused test and observe RED**

Run:

```bash
.venv/bin/python -m pytest \
  tests/task10/test_authority_review_package_v2.py::test_migrator_binds_exact_v1_hashes -q
```

Expected: `FAIL` because the migrator module does not yet exist. The v1 identity
test must pass independently.

- [ ] **Step 4: Record the immutable v1 pair in the migration module constants without writing v2 output**

The module must expose:

```python
V1_REGISTRY_SHA256 = "047c53aed2250790f403c1aa57563fa1c933c0294dda8d2b5f6fb535b097a398"
V1_MATRIX_SHA256 = "8b75baf1db9425daddcfd150f0f3c4638684e42e15fa717c2c2044fb3a8f3287"
```

- [ ] **Step 5: Run the two Task 1 tests**

Expected: `2 passed`; no v2 registry, schema, index, or attestation output is
allowed yet.

### Task 2: Define and test deterministic serialization and source bindings

**Files:**

- Modify: `docs/superpowers/specs/idl/task10/v10/review/migrate_authority_decision_registry_v1_to_v2.py`
- Modify: `tests/task10/test_authority_review_package_v2.py`

- [ ] **Step 1: Write failing tests for canonical pretty JSON**

```python
def test_canonical_json_is_diffable_and_idempotent() -> None:
    module = load_migrator()
    value = {"z": 1, "a": {"d": 4, "b": 2}}
    expected = '{\n  "a": {\n    "b": 2,\n    "d": 4\n  },\n  "z": 1\n}\n'
    assert module.canonical_json_bytes(value).decode("utf-8") == expected
    assert module.parse_canonical_json(module.canonical_json_bytes(value)) == value
```

- [ ] **Step 2: Run the test and observe RED because the API is absent**

- [ ] **Step 3: Implement the minimal serializer**

```python
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


def parse_canonical_json(data: bytes) -> object:
    value = json.loads(data.decode("utf-8"), parse_constant=_reject_non_finite)
    if canonical_json_bytes(value) != data:
        raise ValueError("NON_CANONICAL_JSON_BYTES")
    return value
```

- [ ] **Step 4: Add a failing test that every evidence locator has a source binding ID**

```python
def test_migrated_evidence_is_source_bound() -> None:
    module = load_migrator()
    v1 = module.parse_v1_bytes(
        (REVIEW / "authority-design-decision-registry-v1.json").read_bytes()
    )
    normalized = module.normalize_evidence_bindings(v1)
    source_ids = set(normalized["source_bindings_by_id"])
    for evidence in normalized["evidence_refs_by_id"].values():
        assert evidence["source_binding_id"] in source_ids
        assert "authority_lines" not in evidence
        assert evidence["locator"]["kind"] in {"LINE_RANGE", "JSON_POINTER", "DECISION_ONLY"}
```

- [ ] **Step 5: Run the evidence-binding test and observe RED**

Expected: `FAIL` because `normalize_evidence_bindings` does not exist yet.

- [ ] **Step 6: Implement content-addressed source bindings and evidence interning**

`source_binding_id` must be derived from logical source plus bound SHA, never
array order. `evidence_ref_id` must include the exact `source_binding_id`,
canonical locator, and claim role. Freeze a declarative
`legacy_locator_claim_to_source_binding` map; any locator/claim role paired with
a different but otherwise valid source binding must fail
`EVIDENCE_WRONG_VALID_SOURCE`. The three decision-only evidence cells remain
`DECISION_ONLY`; they must not gain an authority line.

- [ ] **Step 7: Run the focused serializer and evidence tests**

Expected: both pass before Task 3 begins. No RED test may remain open across a
task boundary.

### Task 3: Freeze versioned schemas and validate their closed shapes

**Files:**

- Create: `docs/superpowers/specs/idl/task10/v10/review/schema/authority-design-decision-registry-v2.schema.json`
- Create: `docs/superpowers/specs/idl/task10/v10/review/schema/authority-design-decision-review-attestation-v1.schema.json`
- Create: `docs/superpowers/specs/idl/task10/v10/review/validate_authority_review_package_v2.py`
- Modify: `tests/task10/test_authority_review_package_v2.py`

- [ ] **Step 1: Write all positive and negative schema tests before implementation**

```python
def test_v2_binds_exact_schema_and_normalizes_overloaded_shapes() -> None:
    validator = load_validator()
    schema_path = REVIEW / "schema/authority-design-decision-registry-v2.schema.json"
    schema = json.loads(schema_path.read_text("utf-8"))
    fixture = minimal_valid_v2_registry_fixture(schema_path, digest(schema_path))
    validator.validate_schema_document(schema)
    validator.validate_instance(schema, fixture)
    assert isinstance(fixture["decisions_by_id"]["T10-G18-DD-001"]["reference_kinds"], list)
    assert "branch_instances" not in fixture["decisions_by_id"]["T10-G18-DD-001"]["design_payload"]
```

The hand-written fixture contains one minimal member in each required
collection and uses only IDs declared inside the fixture. It is not generated
from v1 and does not require the production v2 registry to exist.

In the same RED batch, require exact failure codes for scalar
`reference_kinds`, a string Boolean, string/object branch overload, an unknown
instance property, a wrong schema hash, and an unknown schema keyword. The
schema-document self-check and the minimal valid fixture are the positive
controls.

- [ ] **Step 2: Run the complete schema batch and observe RED**

Expected: `FAIL` because both schemas and the validator module are absent.

- [ ] **Step 3: Write the registry schema header and closed top-level contract**

The schema must use:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "selcal.task10.g18.authority-design-decision-registry.v2",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "format",
    "artifact_state",
    "scope_boundary",
    "source_bindings_by_id",
    "evidence_refs_by_id",
    "owners_by_id",
    "schema_templates_by_id",
    "reference_fields_by_id",
    "discriminator_branches_by_id",
    "decisions_by_id",
    "coverage_rows_by_id",
    "compiled_rules_by_id",
    "legacy_aliases_by_id",
    "invariants_by_id"
  ]
}
```

- [ ] **Step 4: Normalize the previously overloaded fields in the schemas**

Use `reference_kinds: [string, ...]` everywhere. Replace string/object `branch_instances` with:

```json
{
  "branch_instance_ids": ["T10-G18-DD-..."],
  "case_labels": ["POP_ITEM_NO_DEFAULT", "POP_ITEM_WITH_DEFAULT"]
}
```

Decision payloads are selected by a 23-way `oneOf` whose discriminator is `decision_id`. Boolean literals require JSON booleans; enum literals require strings.

- [ ] **Step 5: Write the attestation schema**

It must require exact subject path/SHA, registry schema path/SHA, reviewer identity/type/role, scope, verdict, finding counts, immutable effect `NO_AUTHORITY_PROMOTION`, creation timestamp, and optional superseded attestation path/SHA. It must forbid editing a prior attestation in place.

- [ ] **Step 6: Implement only the JSON-Schema subset used by these two schemas**

The standard-library validator must enforce `$ref`, `$defs`, `type`,
`required`, `properties`, `patternProperties`, `additionalProperties`, `oneOf`,
`const`, `enum`, `items`, `minItems`, `uniqueItems`, `pattern`, `minimum`, and
`minLength`. It must explicitly accept the non-asserting metadata/annotation
keywords `$schema`, `$id`, `title`, `description`, `$comment`, `default`, and
`examples`. Every other keyword must fail with
`UNSUPPORTED_SCHEMA_KEYWORD`, not be ignored.

- [ ] **Step 7: Run schema tests**

Expected: each valid sample passes; every named mutation fails with its exact code.

### Task 4: Migrate, deduplicate, and prove exact semantic round-trip

**Files:**

- Modify: `docs/superpowers/specs/idl/task10/v10/review/migrate_authority_decision_registry_v1_to_v2.py`
- Create: `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v2.json`
- Modify: `tests/task10/test_authority_review_package_v2.py`

- [ ] **Step 1: Write RED tests for single-definition rules and exact counts**

```python
def test_v2_has_one_rule_definition_and_exact_partitions() -> None:
    package = load_generated_v2()
    rules = package["compiled_rules_by_id"]
    assert len(rules) == 570
    assert list(rules) == [f"PCR-{index:04d}" for index in range(1, 571)]
    assert Counter(rule["provenance"]["class"] for rule in rules.values()) == {
        "COVERAGE_DERIVED": 509,
        "POST_SCHEMA_EXTRA": 9,
        "AUTHORITY_CLOSED_INVENTORY": 52,
    }
    assert all("compiled_rules" not in row for row in package["coverage_rows_by_id"].values())
    assert all("compilation_rules" not in decision for decision in package["decisions_by_id"].values())
```

- [ ] **Step 2: Observe RED before migration output exists**

- [ ] **Step 3: Implement the minimal normalized v2 projection and make the count test GREEN**

Rules live only in `compiled_rules_by_id`. Decisions and coverage rows keep ordered `compiled_rule_ids`. Branch consumers keep ordered `consumer_rule_ids`. Owners, templates, fields, branches, decisions, rows, evidence, and invariants are first-class ID maps with explicit semantic ordinals; map iteration order is never a compiler input.

- [ ] **Step 4: Write RED exact-round-trip, isolation, and metamorphic tests**

Require exact `v1 -> v2 -> legacy-v1` bytes, then run rehydration in an isolated
temporary directory containing only the migrator module and v2 JSON; the v1
pair is absent and repository access is disabled. Also apply at least three
type-preserving mutations to a parsed v1 object, migrate each through the pure
in-memory API, and require rehydration to restore the corresponding mutated
canonical v1 bytes. A cached baseline rehydrator must fail these tests.

- [ ] **Step 5: Run the rehydration batch and observe RED**

Expected: `FAIL` because the rehydrator does not exist yet.

- [ ] **Step 6: Implement legacy rehydration**

```python
def rehydrate_legacy_v1(v2: dict[str, object]) -> dict[str, object]:
    """Restore every v1 field and duplicate rule body exactly for byte comparison."""
```

The rehydrator is a pure function of the supplied v2 object. It may not accept
a v1 path/bytes argument, read the repository, use a module-level cached v1
object, or contain a raw/base64/compressed v1 payload. It must restore the v1
object, including `NOT_RUN_AFTER_THIS_REVISION`, without adding v2 schema,
source-binding, or attestation fields.

- [ ] **Step 7: Run the exact-round-trip, isolation, and metamorphic batch GREEN**

```python
def test_v1_v2_v1_is_exact_bytes() -> None:
    module = load_migrator()
    v1_bytes = (REVIEW / "authority-design-decision-registry-v1.json").read_bytes()
    v2 = module.migrate_v1_bytes(v1_bytes)
    assert module.legacy_v1_bytes(v2) == v1_bytes
```

- [ ] **Step 8: Write RED tests for two independently computed semantic projections**

Tests require `semantic_projection_from_v1(v1)` and
`semantic_projection_from_v2(v2)` as separate functions. Both must return exactly:

```text
artifact states and STOP permissions
66 owner identities and ordinals
23 decision identities, payloads, reasons, verdicts, and ordered rule IDs
264 coverage identities, categories, actions, and ordered rule IDs
570 rule identities and complete rule bodies
312 reference-field order keys
209 template semantic keys
461 branch identities and predicates
source/evidence semantics expanded to path, SHA, locator, and claim role
legacy aliases and declarative invariant meanings
```

Serialize both projections using `canonical_json_bytes`; require byte equality
and SHA equality. Implement `rule_projection_from_v1` and
`rule_projection_from_v2` separately and require equality after sorting only by
explicit rule ID. Do not freeze a digest whose field-selection algorithm is not
present in executable code.

- [ ] **Step 9: Run the semantic-projection tests and observe RED**

Expected: `FAIL` because the independent projection functions are absent.

- [ ] **Step 10: Implement both projections separately and make the batch GREEN**

Neither projection may call the other or compare against a frozen expected
digest. The test oracle is their independently computed canonical byte equality.

- [ ] **Step 11: Generate v2 twice and require byte identity**

Run the migrator twice into separate temporary directories. `cmp` and SHA-256 must match exactly.

### Task 5: Add declarative invariants and adversarial mutations

**Files:**

- Modify: `docs/superpowers/specs/idl/task10/v10/review/validate_authority_review_package_v2.py`
- Modify: `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v2.json`
- Modify: `tests/task10/test_authority_review_package_v2.py`

- [ ] **Step 1: Write all positive invariant and adverse-mutation tests before implementation**

```python
def test_every_normative_invariant_is_declarative() -> None:
    package = load_generated_v2()
    allowed = {
        "COUNT_EQUALS", "UNIQUE_KEY", "FOREIGN_KEY", "SET_EQUALS",
        "EXACT_PARTITION", "PARTITION_COUNTS", "ALL_MATCH", "SUM_EQUALS",
        "SOURCE_DIGEST_MATCH", "CANONICAL_ORDER",
    }
    assert package["invariants_by_id"]
    for invariant in package["invariants_by_id"].values():
        assert invariant["kind"] in allowed
        assert "description" in invariant
        assert "assertion" in invariant
```

The same RED batch must cover duplicated rule body, dangling rule ID, wrong rule
partition, removed coverage row, missing source binding, another valid but wrong
source binding, changed evidence locator, `DECISION_ONLY` promoted to line
evidence, scalar reference kind, string Boolean, changed ordered tuple,
duplicate template key, embedded full registry in Markdown, review verdict
inside registry, and changed v1 SHA.

- [ ] **Step 2: Run the invariant/mutation batch and observe RED**

Expected: `FAIL` because the declarative invariant engine and complete mutation
catalogue are absent.

- [ ] **Step 3: Encode the exact gates as data and implement the mutation catalogue**

Include executable assertions for the 66/23/264/570/312/209/461 counts, `509+9+52`, all foreign keys, schema-order-key uniqueness, source-digest equality, STOP states, rule/row/decision partitions, no orphan branches, no duplicate rule definitions, and canonical order.

- [ ] **Step 4: Run validator self-test**

```bash
.venv/bin/python \
  docs/superpowers/specs/idl/task10/v10/review/validate_authority_review_package_v2.py \
  --registry docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-registry-v2.json \
  --self-test
```

Expected: exit `0`, all positive invariants pass, and each mutation fails with its intended code.

### Task 6: Generate a concise human index

**Files:**

- Create: `docs/superpowers/specs/idl/task10/v10/review/authority-design-decision-index-v2.md`
- Modify: `docs/superpowers/specs/idl/task10/v10/review/migrate_authority_decision_registry_v1_to_v2.py`
- Modify: `tests/task10/test_authority_review_package_v2.py`

- [ ] **Step 1: Write RED tests for index size and content boundaries**

```python
def test_markdown_index_is_concise_and_non_normative() -> None:
    text = (REVIEW / "authority-design-decision-index-v2.md").read_text("utf-8")
    assert "NON_NORMATIVE_DERIVED_VIEW" in text
    assert "STOP_BEFORE_AUTHORITY_IDL_AND_KATS" in text
    assert text.count("| T10-G18-DD-") == 23
    assert "```json" not in text
    assert len(text.encode("utf-8")) < 100_000
```

- [ ] **Step 2: Run the index test and observe RED**

Expected: `FAIL` because the index has not been generated.

- [ ] **Step 3: Generate only the human review surfaces**

The index contains registry and schema path/SHA, status/count table, 23-row decision index, v1→v2 representation-change table, quality-finding closure table, attestation directory rule, and explicit no-authority/no-IDL/no-KAT warning. It contains no rule, row, template, branch, or full JSON dump.

- [ ] **Step 4: Run the index test GREEN, then regenerate twice and compare exact bytes**

Expected: identical bytes and registry SHA references.

### Task 7: Define detached review attestations

**Files:**

- Create: `docs/superpowers/specs/idl/task10/v10/review/attestations/README.md`
- Modify: `docs/superpowers/specs/idl/task10/v10/review/validate_authority_review_package_v2.py`
- Modify: `tests/task10/test_authority_review_package_v2.py`

- [ ] **Step 1: Write all detached-attestation tests before implementation**

```python
def test_review_results_are_detached_from_subject_bytes() -> None:
    package = load_generated_v2()
    serialized = json.dumps(package, sort_keys=True)
    assert "independent_review_result" not in serialized
    assert "review_verdict" not in serialized
```

In the same RED batch, require valid attestation acceptance and rejection of a
wrong subject SHA, wrong schema SHA, mismatched finding totals, `PASS` with
nonzero findings, missing independence declaration, mutable overwrite target,
or authority-promotion effect.

- [ ] **Step 2: Run the attestation batch and observe RED**

Expected: `FAIL` because the README contract and attestation validator are not
implemented.

- [ ] **Step 3: Write the append-only rules and implement validation**

`README.md` must require one new attestation file per review, subject and schema hashes, reviewer scope and independence declaration, exact finding counts, effect `NO_AUTHORITY_PROMOTION`, no in-place edits, and explicit `supersedes` path/SHA for later reviews.

- [ ] **Step 4: Run the detached-attestation batch GREEN**

- [ ] **Step 5: Do not invent PASS attestations during implementation**

Only an actual independent reviewer verdict obtained after Task 8 may be
represented as PASS. The reviewer remains read-only and returns the verdict;
the persistent implementation writer may then materialize it field-for-field as
an attestation without changing reviewer identity, scope, verdict, finding
counts, or effect. Implementer-generated evidence may use verdict
`REPRESENTATION_EQUIVALENT_ONLY` and must say it is not independent review.

### Task 8: Same-byte verification and two independent reviews

**Files:**

- Read all v2 package files.
- Create exact-hash attestation files only after reviewer verdicts.

- [ ] **Step 1: Finish all reviewed-subject and generator file-writing operations**

No generator, formatter, schema writer, or test that rewrites the registry,
schemas, migrator, validator, index, or focused test may run after this point.
Detached `review-<attestation-id>.json` files and this plan's checkbox state are
written only after review and are not part of the reviewed registry subject.

- [ ] **Step 2: Freeze exact hashes**

Hash v1, v2 registry, both schemas, migrator, validator, Markdown index, and tests. Confirm v1 hashes are unchanged.

- [ ] **Step 3: Run the focused v2 suite**

```bash
.venv/bin/python -m pytest tests/task10/test_authority_review_package_v2.py -q
```

Expected: zero failures.

- [ ] **Step 4: Run the validator self-test**

Expected: exit `0` and all adverse mutations rejected for their intended code.

- [ ] **Step 5: Run the unchanged repository baseline**

```bash
.venv/bin/python -m pytest -q
```

Expected: `2435 passed, 1 skipped` or a larger passing count; no production behavior may regress.

- [ ] **Step 6: Obtain exact-byte specification review**

Require `0 BLOCKER / 0 MAJOR / 0 MINOR`. The reviewer must confirm v2 is representation-equivalent only and preserves all STOP states.

- [ ] **Step 7: Obtain fresh data/code-quality review**

Require `0 BLOCKER / 0 MAJOR / 0 MINOR`. The reviewer must test deduplication, schema enforcement, evidence binding, Markdown size, detached-attestation topology, mutation strength, and false-green risks.

- [ ] **Step 8: Create detached attestations from the exact reviewer outputs**

The persistent implementation writer, not the read-only reviewer, materializes
each reviewer output field-for-field. Each attestation binds the frozen
registry/schema paths and hashes and records the actual reviewer identity,
scope, verdict, and finding counts. The writer may not reinterpret or alter any
of those fields. Writing an attestation does not change the reviewed registry
bytes.

- [ ] **Step 9: Revalidate attestations without rebuilding the registry**

Expected: both attestations validate and target the same exact v2 registry SHA.

- [ ] **Step 10: Update this v2 plan's checkboxes only after both reviews pass**

Mark only the v2 review-package quality gate complete in this plan. Updating
the parent Task 10 plan requires a separate exact-byte scope decision after the
v2 attestations exist. Keep authority amendment, IDL, KAT, M6/UI, release, and
manuscript gates pending.

## Self-review checklist

- Every one of the five MAJOR quality findings maps to Tasks 2–7.
- The one MINOR declarative-invariant finding maps to Task 5.
- v1 exact bytes are never written, formatted, renamed, or superseded scientifically.
- The plan uses test-first RED/GREEN steps before every new behavior.
- The plan does not rely on JSON/map/Markdown order for scientific compilation.
- Detached review removes the self-hash review cycle.
- Task 0 explicitly authorizes the successor outputs and binds the dirty
  predecessor/input bytes without committing unrelated user changes.
- No placeholder implementation, authority promotion, IDL work, KAT work, production-code edit, UI work, release claim, or manuscript claim is present.
