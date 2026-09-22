# Task 10 Cross-Module Operation Capsules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** replace the incomplete single-module behavior guard with three
definition-time capsule families, prove the complete bounded `selcal.*` Python
call graph, and repair the lexical dispatch audit without changing scientific
semantics or public signatures.

**Architecture:** Build the verifier, random, and execution capsules in five
strictly serial RED/GREEN slices. Runtime roots capture sealed leaf operations
and perform zero import, inspect, disassembly, AST, or graph discovery; a
separate bounded CI proof traverses only project-owned Python functions and
records external built-in/NumPy/C leaves.

**Tech Stack:** Python 3.11+, NumPy PCG64 raw words, frozen dataclasses and
exact tuples, pytest/pytest-cov, `ast`, `dis`, `inspect`, Ruff, strict mypy, and
setuptools build.

---

**Design authority:**
`docs/superpowers/specs/2026-08-28-task10-cross-module-operation-capsules-design.md`

**Slice 2 auxiliary-proof correction authority and HOLD:**
`docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md`.
The current Task 5 `_random_behavior_graph_v2.py` helper-proof and commit steps
are stale and must not be executed. After the user approves the correction
specification, a dedicated `writing-plans` output must replace those steps and
be linked here before implementation resumes. Completed Slice 1 and the Task 5
production random-capsule requirements remain authoritative.

**Starting code:** `4d9b736f8b7839caec37f9a408ed455e1e72488a`

**Execution invariant:** complete each RED commit, preserve its intended
failure, then make only that slice GREEN. Do not begin a later slice while an
earlier focused or regression command fails. Do not squash the ten RED/GREEN
commits into one implementation commit.

## File map

**Production files that may change during implementation:**

- `src/selcal/contracts_v2.py`: sealed result-verifier capsule and public exact
  verifier closure.
- `src/selcal/randomness.py`: sealed random capsule, private stream state, and
  compatibility wrappers.
- `src/selcal/selection_v2.py`: sealed selector execution leaf.
- `src/selcal/support.py`: sealed common-support operation used by statistic
  capsules.
- `src/selcal/statistics/lagged_pearson.py`: lagged-Pearson execution capsule.
- `src/selcal/statistics/binned_nette.py`: binned-NetTE execution capsule.
- `src/selcal/nulls/executable_base.py`: public/scripted callable-resolution
  compatibility only; production sampling must leave this path.
- `src/selcal/nulls/owned_transform_v2.py`: sealed ownership/token/transform
  support operations.
- `src/selcal/nulls/circular_shift_v2.py`: circular-null execution capsule.
- `src/selcal/nulls/block_shuffle_v2.py`: block-null execution capsule.
- `src/selcal/resolution_v2.py`: bind canonical algorithm capsules into sealed
  resolution snapshots.
- `src/selcal/calibration_v2.py`: consume all three capsule families, retain
  the guarded full-body executor and exact terminal order, and remove the old
  behavior guard as a security dependency.

**Test files that may change:**

- `tests/test_contracts_v2.py`
- `tests/test_calibration_v2_integrity.py`
- `tests/test_calibration_v2_finalization.py`
- `tests/test_randomness_v2.py`
- `tests/test_randomness_v2_subprocess.py`
- `tests/test_scientific_plan_v2_vectors.py`
- `tests/test_statistic_lagged_pearson.py`
- `tests/test_statistic_binned_nette.py`
- `tests/test_null_circular_shift_v2.py`
- `tests/test_null_block_shuffle_v2.py`
- `tests/test_owned_transform_v2.py`
- `tests/test_resolution_v2.py`
- `tests/test_calibration_v2_replicates.py`
- `tests/test_calibration_v2_failures.py`
- `tests/test_calibration_v2_observed.py`
- `tests/test_in_memory_execution_budget_v2.py`
- `tests/test_exact_oracle_independence.py`
- `tests/test_plan_migration_v1_to_v2.py`
- `tests/test_system_boundary_v2.py`
- `tests/test_public_api_v2.py`
- Create `tests/_random_behavior_graph_v2.py`: bounded RNG-independence graph
  traversal used by the exact-oracle and migration tests; it is test-only and
  not packaged.
- Create `tests/_task10_trusted_graph_v2.py`: bounded project-owned graph
  traversal and external-leaf manifest helper; it is test-only and not packaged.
- Create `tests/_task10_dispatch_ast_v2.py`: lexical-scope abstract interpreter;
  it is test-only and not packaged.

No architecture/status/filter-net document is changed during the code slices.
Those evidence updates require a later explicit parent action.

## Old-test migration principles

1. Preserve tests that specify public signatures, exact results, KAT vectors,
   NULL_BIND/observed failure priority, exact-B retention, q=4096 allocation,
   callback frame/history, public-hook count, and frozen internal attestation.
2. A post-seal monkeypatch of a production helper or descriptor becomes an
   adversarial test. Its expected outcome is byte/equality-identical output or
   a typed integrity failure before return; the replacement bomb must not run.
3. A test that monkeypatches a production adapter/RNG method only to manufacture
   a branch moves to the owning pure capsule unit. Integration tests use real
   deterministic fixtures and committed seed vectors.
4. Direct descriptor-shape tests for `uniform_randbelow` remain valid, but they
   must not be cited as coverage of production null sampling.
5. Do not delete an adverse test merely because its old injection seam is gone.
   First replace it with an equal-or-stronger capsule-level or real-fixture test,
   run both where possible, then remove only the obsolete seam assertion in the
   same GREEN commit.
6. Test helpers may call private pure leaves. They may not add an injection
   parameter/default/environment toggle to the public calibrator, private
   executor, public verifier, terminal attestor, or canonical resolver.

### Task 1: Freeze the fourth-round baseline and test identities

**Files:**

- Read: all production and test files in the file map
- Do not modify production files

- [ ] **Step 1: Confirm the exact starting identity and cleanliness**

Run:

```bash
git rev-parse HEAD^
git status --short --untracked-files=all
```

Expected: the first command prints
`4d9b736f8b7839caec37f9a408ed455e1e72488a`; the second prints nothing. The
separately approved design/plan commit must already be part of `HEAD` and
therefore must not appear as a worktree change.
If the code parent differs, stop and rebase the plan against the actual reviewed
code before writing tests.

- [ ] **Step 2: Record the existing trusted signatures and terminal paths**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_public_api_v2.py::test_only_resolution_v2_is_directly_executable_and_v1_is_typed_rejection \
  tests/test_calibration_v2_replicates.py::test_execute_is_one_full_body_guarded_closure_without_injectable_defaults \
  tests/test_calibration_v2_integrity.py::test_every_public_terminal_path_verifies_exactly_once_before_return \
  tests/test_in_memory_execution_budget_v2.py::test_budget_does_not_preempt_null_disabled_or_observed_failure_paths \
  -q
```

Expected: all selected nodes pass. Save the node IDs and exact output in the
implementation log; do not change their assertions to make later work easier.

- [ ] **Step 3: Establish the pre-slice regression command**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_contracts_v2.py \
  tests/test_randomness_v2.py \
  tests/test_statistic_lagged_pearson.py \
  tests/test_statistic_binned_nette.py \
  tests/test_null_circular_shift_v2.py \
  tests/test_null_block_shuffle_v2.py \
  tests/test_owned_transform_v2.py \
  tests/test_resolution_v2.py \
  tests/test_calibration_v2_integrity.py \
  tests/test_calibration_v2_replicates.py \
  tests/test_calibration_v2_failures.py \
  tests/test_in_memory_execution_budget_v2.py \
  tests/test_system_boundary_v2.py \
  -q
```

Expected: zero failures on the starting code. Any unrelated failure is a stop
condition; preserve it rather than hiding it in the capsule work.

### Task 2: Slice 1 RED — verifier kernel

**Files:**

- Modify: `tests/test_contracts_v2.py`
- Modify: `tests/test_calibration_v2_integrity.py`
- Modify: `tests/test_calibration_v2_finalization.py`

- [ ] **Step 1: Add the dynamic-import and cross-module verifier attacks**

Add exact nodes with these contracts:

```python
def test_trusted_verifier_has_no_recursive_runtime_import_instructions() -> None:
    opnames = recursive_instruction_names(contracts_v2.verify_calibration_result)
    assert "IMPORT_NAME" not in opnames
    assert "IMPORT_FROM" not in opnames


@pytest.mark.parametrize(
    "target",
    (
        "selcal.contracts_v2._verify_result_vector_against_plan",
        "selcal.canonical_v2.scientific_plan_v2_sha256",
        "selcal.resolution_v2._snapshot_result_verification_context_v2",
        "selcal.randomness.ReplicateRandomSource",
    ),
)
def test_post_seal_cross_module_verifier_rebinding_cannot_accept_forgery(
    monkeypatch: pytest.MonkeyPatch,
    target: str,
) -> None:
    result, resolution = _complete_result()
    forged = _constructor_valid_but_resolution_inconsistent_copy(result)
    monkeypatch.setattr(target, lambda *args, **kwargs: None)
    with pytest.raises(V2IntegrityError):
        contracts_v2.verify_calibration_result(forged, resolution)
```

The real test helper must split the dotted target into its imported module and
attribute so `monkeypatch.setattr` receives a valid target. The forged value
must be created through the ordinary public constructor with internally valid
fields that contradict the sealed resolution; direct `object.__setattr__`,
`__code__`, closure-cell, frame, trace, or native-memory mutation is outside
the approved threat model and is not valid RED evidence. Add a second attack
where the dynamic public hook replaces, invokes, and restores the same helper;
the frozen internal verifier must still reject the forged result.

- [ ] **Step 2: Preserve terminal counts and four-path ordering**

Extend the existing parameterized terminal test to count one dynamic hook call
and one captured-real-verifier call for `complete`, `null_bind`,
`observed_statistic_scan`, and `replicate_execution`. The expected sequence is
`["public", "sealed"]` for each path.

- [ ] **Step 3: Run RED**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_contracts_v2.py::test_trusted_verifier_has_no_recursive_runtime_import_instructions \
  tests/test_calibration_v2_integrity.py -k 'cross_module_verifier or terminal_path' \
  tests/test_calibration_v2_finalization.py -q
```

Expected on the pre-fix code: at least the runtime-import test and ordinary
cross-module attacks fail for the reviewed reason. Collection, fixture, or
signature failures do not count as RED.

- [ ] **Step 4: Commit only RED evidence**

```bash
git add tests/test_contracts_v2.py tests/test_calibration_v2_integrity.py tests/test_calibration_v2_finalization.py
git commit -m "test: expose cross-module verifier drift"
```

### Task 3: Slice 1 GREEN — sealed result-verifier capsule

**Files:**

- Modify: `src/selcal/contracts_v2.py`
- Modify: `src/selcal/canonical_v2.py`
- Modify: `src/selcal/resolution_v2.py`
- Modify: `src/selcal/calibration_v2.py`
- Modify only as required by migration: the three Slice 1 test files

- [ ] **Step 1: Build the exact verifier capsule interface**

In `contracts_v2.py`, define a private construction record and immediately
unpack the canonical verifier leaf. The exact public construction types are:

```python
class _ResultVerifierCapsuleV2(NamedTuple):
    verify: Callable[[object, object], None]
    external_leaves: tuple[object, ...]


_PlanSha256V2 = Callable[[object], str]
_ResolutionContextV2 = Callable[[object], object]
_SeedDigestV2 = Callable[[str, int, int], str]
_ResultVerifierFactoryV2 = Callable[
    [_PlanSha256V2, _ResolutionContextV2, _SeedDigestV2],
    _ResultVerifierCapsuleV2,
]
```

Implement `_freeze_result_verifier_capsule_v2(plan_sha256,
resolution_context, seed_digest, /)` with that callable contract and the
complete existing verification logic. Freeze original
result/outcome/token/selection slot descriptors and read through them directly.
Delete `_freeze_result_verifier_capsule_v2` after constructing the canonical
capsule.

- [ ] **Step 2: Remove function-local imports and bind the terminal gate**

Do not add a top-level `contracts_v2 -> resolution_v2` import: it would create
an initialization cycle. Use the design's one-shot bootstrap. `contracts_v2`
defines the private local factory; after `resolution_v2` has defined its sealed
context reader it supplies that reader plus the already-sealed canonical plan
hash and random seed-oracle leaves exactly once, installs the returned closure
as `contracts_v2.verify_calibration_result`, and deletes the bootstrap/factory
surface. Reorder `calibration_v2` imports so it captures the installed verifier
only after this bootstrap has completed. There must never be a permissive or
callable placeholder verifier. A second bootstrap or premature verifier read
must fail typed. Add fresh-process tests for `import selcal`,
`import selcal.contracts_v2`, and `import selcal.calibration_v2` order.

Remove the current verifier's function-local imports. In `calibration_v2.py`,
retain the dynamic public hook but capture the real capsule verifier
separately. Do not add a callable default or attestor parameter.

- [ ] **Step 3: Run Slice 1 GREEN and regression**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_contracts_v2.py \
  tests/test_calibration_v2_integrity.py \
  tests/test_calibration_v2_finalization.py \
  tests/test_result_invariants_v2.py \
  tests/test_system_boundary_v2.py -q
```

Expected: zero failures; all four terminal paths retain exact status/failure
stage and public-hook counts.

- [ ] **Step 4: Commit Slice 1 GREEN**

```bash
git add src/selcal/contracts_v2.py src/selcal/canonical_v2.py src/selcal/resolution_v2.py src/selcal/calibration_v2.py tests/test_contracts_v2.py tests/test_calibration_v2_integrity.py tests/test_calibration_v2_finalization.py
git commit -m "fix: seal task10 verifier kernel"
```

### Task 4: Slice 2 RED — random kernel and descriptor attacks

**Files:**

- Modify: `tests/test_randomness_v2.py`
- Modify: `tests/test_scientific_plan_v2_vectors.py`
- Modify: `tests/test_calibration_v2_replicates.py`
- Modify: `tests/test_calibration_v2_integrity.py`

- [ ] **Step 1: Add module-helper and class-descriptor attacks**

Add parameterized tests for these exact targets:

```python
RANDOM_MODULE_TARGETS = (
    "_require_plan_digest",
    "_require_planned_replicates",
    "_require_replicate_id",
    "_require_raw64_word",
    "_uniform_randbelow_from_next",
    "hashlib",
    "np",
)

RANDOM_CLASS_TARGETS = (
    "__init__",
    "randbelow",
    "_next_raw64",
    "seed_digest_sha256",
)
```

For each module target, compute a committed baseline vector, install a bomb,
and require the sealed production seed/vector to remain equal without executing
the bomb. For each class target, replace the descriptor after sealing and run a
real COMPLETE calibration; require equality with the baseline or a typed
integrity error before return.

- [ ] **Step 2: Add replace-use-restore and shared-oracle tests**

Inside a real null callback, replace `ReplicateRandomSource.randbelow`, run the
callback body, then restore it before return. Assert the replacement never
executes. Add:

```python
def test_executor_and_verifier_share_one_sealed_seed_oracle_identity() -> None:
    executor_random = frozen_random_capsule_from_executor()
    verifier_random = frozen_random_capsule_from_verifier()
    assert executor_random is verifier_random
```

The helper must inspect already-created closure/capsule values only; it must not
introduce a production accessor.

- [ ] **Step 3: Run RED**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_randomness_v2.py -k 'post_seal or descriptor or shared' \
  tests/test_scientific_plan_v2_vectors.py \
  tests/test_calibration_v2_replicates.py -k 'random or descriptor' \
  tests/test_calibration_v2_integrity.py -k 'seed or random' -q
```

Expected: the current class-descriptor and transitive randomness attacks fail
for the reviewed reason; KAT failures caused by test corruption do not count.

- [ ] **Step 4: Commit only RED evidence**

```bash
git add tests/test_randomness_v2.py tests/test_scientific_plan_v2_vectors.py tests/test_calibration_v2_replicates.py tests/test_calibration_v2_integrity.py
git commit -m "test: expose random capsule descriptor drift"
```

### Task 5: Slice 2 GREEN — sealed random capsule

**Files:**

- Modify: `src/selcal/randomness.py`
- Modify: `src/selcal/calibration_v2.py`
- Modify: `src/selcal/nulls/executable_base.py`
- Modify: `src/selcal/resolution_v2.py`
- Inspect, but do not modify unless the one-shot bootstrap contract itself must
  change: `src/selcal/contracts_v2.py`
- Create: `tests/_random_behavior_graph_v2.py`
- Modify only as required by migration:
  `tests/test_randomness_v2.py`,
  `tests/test_randomness_v2_subprocess.py`,
  `tests/test_calibration_v2_replicates.py`,
  `tests/test_calibration_v2_integrity.py`,
  `tests/test_calibration_v2_finalization.py`,
  `tests/test_in_memory_execution_budget_v2.py`,
  `tests/test_calibration_v2_observed.py`,
  `tests/test_calibration_v2_failures.py`,
  `tests/test_exact_oracle_independence.py`,
  `tests/test_plan_migration_v1_to_v2.py`, and
  `tests/test_contracts_v2.py`

- [ ] **Step 1: Build private exact stream operations**

Use this interface in `randomness.py`:

```python
class _RandomCapsuleV2(NamedTuple):
    create_stream: Callable[[str, int, int], object]
    seed_digest: Callable[[object], str]
    randbelow: Callable[[object, int], int]
    seed_digest_for_replicate: Callable[[str, int, int], str]
    external_leaves: tuple[object, ...]
```

The stream is exact private state containing captured PCG64 state and the seed
hex. Build it without invoking `ReplicateRandomSource.__init__`. Bind and call
the captured PCG64 raw-word descriptor directly. Make all validation and
rejection-sampling helpers nested zero-global closures.

Pass the exact capsule seed-oracle leaf through the existing one-shot verifier
bootstrap in `resolution_v2.py`. Delete the independently copied seed-digest
implementation there so execution and verification cannot drift onto two
algorithms.

- [ ] **Step 2: Make compatibility APIs delegate without becoming trust roots**

Keep the public class signature and `uniform_randbelow(source, bound, /)` tests.
The public class may delegate to frozen random leaves, but production
calibration and verification receive the capsule leaves directly and never
perform live `ReplicateRandomSource` method/property lookup.

Until Slice 3 replaces the null API with
`sample_token_from_randbelow(randbelow, /)`, use one sealed private capability
bridge in `nulls/executable_base.py` to carry only a bound `randbelow` leaf into
the existing sampler. This bridge is transitional production debt: Slice 3
must delete it and production null sampling must then stop reaching
`_resolve_static_callable`.

- [ ] **Step 3: Run Slice 2 GREEN and budget regressions**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_randomness_v2.py \
  tests/test_randomness_v2_subprocess.py \
  tests/test_scientific_plan_v2_vectors.py \
  tests/test_calibration_v2_replicates.py \
  tests/test_calibration_v2_integrity.py \
  tests/test_calibration_v2_finalization.py \
  tests/test_in_memory_execution_budget_v2.py \
  tests/test_calibration_v2_observed.py \
  tests/test_calibration_v2_failures.py \
  tests/test_exact_oracle_independence.py \
  tests/test_plan_migration_v1_to_v2.py \
  tests/test_contracts_v2.py -q
```

Expected: zero failures; committed PCG64 vectors are unchanged, the million-B
guard still rejects before RNG creation, and q=4096/allocation tests retain
their prior ordering.

- [ ] **Step 4: Commit Slice 2 GREEN**

```bash
git add src/selcal/randomness.py src/selcal/calibration_v2.py src/selcal/nulls/executable_base.py src/selcal/resolution_v2.py tests/_random_behavior_graph_v2.py tests/test_randomness_v2.py tests/test_randomness_v2_subprocess.py tests/test_calibration_v2_replicates.py tests/test_calibration_v2_integrity.py tests/test_calibration_v2_finalization.py tests/test_in_memory_execution_budget_v2.py tests/test_calibration_v2_observed.py tests/test_calibration_v2_failures.py tests/test_exact_oracle_independence.py tests/test_plan_migration_v1_to_v2.py tests/test_contracts_v2.py docs/superpowers/plans/2026-08-28-task10-cross-module-operation-capsules-implementation.md
git commit -m "fix: seal task10 random kernel"
```

### Task 6: Slice 3 RED — statistic and null operation kernels

**Files:**

- Modify: `tests/test_statistic_lagged_pearson.py`
- Modify: `tests/test_statistic_binned_nette.py`
- Modify: `tests/test_null_circular_shift_v2.py`
- Modify: `tests/test_null_block_shuffle_v2.py`
- Modify: `tests/test_owned_transform_v2.py`
- Modify: `tests/test_resolution_v2.py`
- Modify: `tests/test_calibration_v2_replicates.py`
- Modify: `tests/test_calibration_v2_failures.py`

- [ ] **Step 1: Add the exhaustive owner-module rebinding matrix**

Parameterize owner and helper targets at minimum as follows:

```python
SCIENTIFIC_HELPER_TARGETS = (
    "selcal.support.common_support",
    "selcal.statistics.lagged_pearson._centered_unit_vector",
    "selcal.statistics.lagged_pearson._lagged_pearson",
    "selcal.statistics.lagged_pearson._clamp_correlation",
    "selcal.statistics.binned_nette._observed_edges",
    "selcal.statistics.binned_nette._code_with_edges",
    "selcal.statistics.binned_nette.conditional_mutual_information",
    "selcal.nulls.owned_transform_v2.parameter_digest",
    "selcal.nulls.owned_transform_v2.owner_digest",
    "selcal.nulls.owned_transform_v2.snapshot_common_token",
    "selcal.nulls.circular_shift_v2._apply_state",
    "selcal.nulls.block_shuffle_v2._ascending_labels",
    "selcal.nulls.block_shuffle_v2._apply_state",
)
```

For every target, resolve and seal a real plan first, then replace the target
with a bomb. Run both statistic-by-null combinations represented by the target;
require exact baseline equality or typed fail-closed behavior, and prove the
bomb did not execute.

- [ ] **Step 2: Add descriptor, callback, and resolver capsule tests**

After resolution sealing, replace each bound operation descriptor:
`evaluate_all`, `identity_token`, `sample_token`, `snapshot_token`, and `apply`.
Repeat one replacement from inside an untrusted callback and restore it before
return. Assert the resolution snapshot carries an `_ExecutionCapsuleV2` leaf,
not only `_FrozenOperationV2(descriptor, callable)`.

Add a production-path bomb on
`selcal.nulls.executable_base._resolve_static_callable`; a real COMPLETE
calibration must not reach it.

- [ ] **Step 3: Run RED**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_statistic_lagged_pearson.py -k 'post_seal or capsule' \
  tests/test_statistic_binned_nette.py -k 'post_seal or capsule' \
  tests/test_null_circular_shift_v2.py -k 'post_seal or capsule or production' \
  tests/test_null_block_shuffle_v2.py -k 'post_seal or capsule or production' \
  tests/test_owned_transform_v2.py -k 'post_seal or capsule' \
  tests/test_resolution_v2.py -k 'execution and capsule' \
  tests/test_calibration_v2_replicates.py -k 'cross_module or descriptor' -q
```

Expected: current transitive helpers or descriptor calls execute at least one
bomb, and the resolution-capsule assertion fails. All failures must point to the
missing seal rather than changed scientific expectations.

- [ ] **Step 4: Commit only RED evidence**

```bash
git add tests/test_statistic_lagged_pearson.py tests/test_statistic_binned_nette.py tests/test_null_circular_shift_v2.py tests/test_null_block_shuffle_v2.py tests/test_owned_transform_v2.py tests/test_resolution_v2.py tests/test_calibration_v2_replicates.py tests/test_calibration_v2_failures.py
git commit -m "test: expose statistic and null operation drift"
```

### Task 7: Slice 3 GREEN — sealed execution capsules

**Files:**

- Modify: `src/selcal/selection_v2.py`
- Modify: `src/selcal/support.py`
- Modify: `src/selcal/statistics/lagged_pearson.py`
- Modify: `src/selcal/statistics/binned_nette.py`
- Modify: `src/selcal/nulls/owned_transform_v2.py`
- Modify: `src/selcal/nulls/circular_shift_v2.py`
- Modify: `src/selcal/nulls/block_shuffle_v2.py`
- Modify: `src/selcal/nulls/executable_base.py`
- Modify: `src/selcal/resolution_v2.py`
- Modify: `src/selcal/calibration_v2.py`
- Modify only as required by migration: Slice 3 test files

- [ ] **Step 1: Define and bind the execution-capsule shapes**

Use private immutable construction records equivalent to:

```python
class _StatisticExecutionCapsuleV2(NamedTuple):
    evaluate_all: Callable[[SeriesPair], tuple[StatisticResult, ...]]
    identity_evidence: tuple[object, ...]


class _NullExecutionCapsuleV2(NamedTuple):
    identity_token: Callable[[], NullTransformToken]
    sample_token_from_randbelow: Callable[[Callable[[int], int]], NullTransformToken]
    snapshot_token: Callable[[object], tuple[object, ...]]
    apply: Callable[[NullTransformToken], NullTransformResult]
    identity_evidence: tuple[object, ...]
```

These are the statistic/null shapes of the single `_ExecutionCapsuleV2`
family. Each owner module creates its own leaf closures from exact copied state
or captured slot descriptors and frozen helper/external leaves.

- [ ] **Step 2: Replace ordinary operation snapshots as execution authority**

In `resolution_v2.py`, retain descriptor identities only as evidence. Store and
reverify the sealed execution leaves as the callable authority. In
`calibration_v2.py`, call only those leaves and the random capsule's bound
`randbelow` capability. Keep the live selector check as identity-only; invoke
the sealed selector leaf.

- [ ] **Step 3: Preserve failure taxonomy and test seams**

Do not translate `V2IntegrityError` into an analytical failure. Preserve real
numeric/analytic failures. Move scripted method-monkeypatch cases to direct
owner-kernel units, and retain callback-frame/history assertions on the actual
`_execute_replicates` frame with `history` present.

- [ ] **Step 4: Run Slice 3 GREEN and scientific regression**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_selection_v2.py \
  tests/test_support.py \
  tests/test_statistic_lagged_pearson.py \
  tests/test_statistic_binned_nette.py \
  tests/test_null_circular_shift_v2.py \
  tests/test_null_block_shuffle_v2.py \
  tests/test_null_token_vectors_v2.py \
  tests/test_owned_transform_v2.py \
  tests/test_resolution_v2.py \
  tests/test_calibration_v2_replicates.py \
  tests/test_calibration_v2_failures.py \
  tests/test_system_boundary_v2.py -q
```

Expected: zero failures and no KAT/result-vector changes.

- [ ] **Step 5: Commit Slice 3 GREEN**

```bash
git add src/selcal/selection_v2.py src/selcal/support.py src/selcal/statistics/lagged_pearson.py src/selcal/statistics/binned_nette.py src/selcal/nulls/owned_transform_v2.py src/selcal/nulls/circular_shift_v2.py src/selcal/nulls/block_shuffle_v2.py src/selcal/nulls/executable_base.py src/selcal/resolution_v2.py src/selcal/calibration_v2.py tests/test_statistic_lagged_pearson.py tests/test_statistic_binned_nette.py tests/test_null_circular_shift_v2.py tests/test_null_block_shuffle_v2.py tests/test_owned_transform_v2.py tests/test_resolution_v2.py tests/test_calibration_v2_replicates.py tests/test_calibration_v2_failures.py
git commit -m "fix: seal task10 statistic and null kernels"
```

### Task 8: Slice 4 RED — bounded cross-module graph proof

**Files:**

- Create: `tests/_task10_trusted_graph_v2.py`
- Modify: `tests/test_calibration_v2_replicates.py`
- Modify: `tests/test_calibration_v2_integrity.py`
- Modify: `tests/test_system_boundary_v2.py`
- Modify: `tests/test_in_memory_execution_budget_v2.py`

- [ ] **Step 1: Add a bounded graph helper with hard limits**

Create exact constants and result records:

```python
MAX_TRUSTED_GRAPH_DEPTH = 32
MAX_TRUSTED_GRAPH_NODES = 512
MAX_TRUSTED_GRAPH_EDGES = 4096


class TrustedGraphResult(NamedTuple):
    project_functions: tuple[FunctionType, ...]
    external_leaves: tuple[ExternalLeaf, ...]
    edges: tuple[tuple[str, str], ...]
```

The helper resolves the installed `selcal` root, follows closure cells,
capsule tuples, properties, static/class methods, nested code, and diagnostic
`LOAD_GLOBAL` targets only for project-owned `selcal.*` functions. It stops at
enumerated external leaves, cuts cycles by identity, and raises
`AssertionError` on an unknown leaf or any hard-limit hit.

- [ ] **Step 2: Add exact proof tests**

Add nodes with these exact names:

```python
REQUIRED_GRAPH_TEST_NAMES = (
    "test_trusted_graph_crosses_every_project_owned_module_boundary",
    "test_trusted_graph_has_zero_dynamic_import_and_uncontrolled_global_loads",
    "test_trusted_graph_records_external_leaves_without_traversing_numpy",
    "test_trusted_graph_limits_fail_closed_instead_of_truncating",
    "test_runtime_execution_never_calls_graph_inspect_or_discovery",
)
```

The module-boundary assertion must include `contracts_v2`, `randomness`, both
statistics, both v2 nulls, `owned_transform_v2`, `support`, `selection_v2`,
`resolution_v2`, and `calibration_v2`. The import assertion recursively checks
nested code objects. Explicitly assert the only live mapping observations are
the public verifier hook and selector drift sentinel.

- [ ] **Step 3: Run RED against the prior graph logic**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_calibration_v2_replicates.py -k 'trusted_graph' \
  tests/test_calibration_v2_integrity.py -k 'trusted_graph or runtime_execution_never' \
  tests/test_system_boundary_v2.py -k 'trusted_graph' \
  tests/test_in_memory_execution_budget_v2.py -k 'runtime_execution_never' -q
```

Expected: at least one cross-module edge/import/global assertion fails until
all previous capsule roots are registered with the proof helper. A test that
silently stops at an external `selcal.*` function is itself a RED failure.

- [ ] **Step 4: Commit only RED evidence and the test helper**

```bash
git add tests/_task10_trusted_graph_v2.py tests/test_calibration_v2_replicates.py tests/test_calibration_v2_integrity.py tests/test_system_boundary_v2.py tests/test_in_memory_execution_budget_v2.py
git commit -m "test: require bounded cross-module trusted graph"
```

### Task 9: Slice 4 GREEN — close the graph and runtime-cost boundary

**Files:**

- Modify only the production files identified by the failing graph frontier
- Modify: `tests/_task10_trusted_graph_v2.py`
- Modify: `tests/test_calibration_v2_replicates.py`
- Modify: `tests/test_calibration_v2_integrity.py`
- Modify: `tests/test_system_boundary_v2.py`
- Modify: `tests/test_in_memory_execution_budget_v2.py`

- [ ] **Step 1: Eliminate every reported project-owned global/import edge**

For each graph failure, move the named behavior dependency into its owner
factory closure or immutable local constant. Do not add a module allowlist to
hide the edge. An external leaf may be added only when its provider is outside
the installed `selcal` root and its exact provider/category/version is asserted.

- [ ] **Step 2: Prove zero runtime discovery and bounded proof cost**

After importing SelCal, monkeypatch the graph builder plus `inspect`/`dis`
entrypoints used by the proof helper to bombs, then execute B greater than one
and verify a COMPLETE result. Assert zero bomb calls. Measure the test-only graph
with `time.perf_counter`; require completion below 2 seconds, 512 nodes, and
4096 edges, while treating the time as a generous hang guard rather than a
performance comparison.

- [ ] **Step 3: Re-run resource and graph gates**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_calibration_v2_replicates.py \
  tests/test_calibration_v2_integrity.py \
  tests/test_system_boundary_v2.py \
  tests/test_in_memory_execution_budget_v2.py -q
```

Expected: zero failures; the existing B/C/N/S/work, q=4096, callback-history,
and terminal-memory tests remain unchanged.

- [ ] **Step 4: Commit Slice 4 GREEN**

```bash
git add src/selcal/contracts_v2.py src/selcal/randomness.py src/selcal/selection_v2.py src/selcal/support.py src/selcal/statistics/lagged_pearson.py src/selcal/statistics/binned_nette.py src/selcal/nulls/executable_base.py src/selcal/nulls/owned_transform_v2.py src/selcal/nulls/circular_shift_v2.py src/selcal/nulls/block_shuffle_v2.py src/selcal/resolution_v2.py src/selcal/calibration_v2.py tests/_task10_trusted_graph_v2.py tests/test_calibration_v2_replicates.py tests/test_calibration_v2_integrity.py tests/test_system_boundary_v2.py tests/test_in_memory_execution_budget_v2.py
git commit -m "fix: close bounded task10 operation graph"
```

Before committing, inspect `git diff --cached --name-only`; if `src/selcal`
stages any file not named by the actual graph frontier, unstage it and explain
the unexpected dependency rather than broadening the slice silently.

### Task 10: Slice 5 RED — lexical AST analyzer

**Files:**

- Create: `tests/_task10_dispatch_ast_v2.py`
- Modify: `tests/test_system_boundary_v2.py`

- [ ] **Step 1: Add the exact adverse and harmless cases**

Add test IDs and expected findings for:

```python
LEXICAL_CASES = {
    "module_qualified_call": "catalog.choose_adapter(name)",
    "dict_value_subscript_call": "OPS['active'](name)",
    "factory_result_call": "BUILDERS['active']()(name)",
    "nested_inherits_origin": "inner(name)",
    "sibling_scope_isolation": "same local alias in two sibling functions",
    "harmless_logger_literal": "logger.info('circular_shift_v2')",
}
```

The first four must produce imported/indirect dispatch findings. Sibling scope
isolation and the logger literal must produce no false finding.

- [ ] **Step 2: Run RED against the current flattened analyzer**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_system_boundary_v2.py -k 'module_qualified_call or dict_value_subscript_call or factory_result_call or nested_inherits_origin or sibling_scope_isolation or harmless_logger_literal' -q
```

Expected: module-qualified/container/factory cases are missed or sibling scope
is falsely contaminated. A changed expected set that merely matches the old
analyzer is not valid RED.

- [ ] **Step 3: Commit only RED evidence**

```bash
git add tests/_task10_dispatch_ast_v2.py tests/test_system_boundary_v2.py
git commit -m "test: expose lexical dispatch analysis gaps"
```

### Task 11: Slice 5 GREEN — scope-correct bounded analyzer

**Files:**

- Modify: `tests/_task10_dispatch_ast_v2.py`
- Modify: `tests/test_system_boundary_v2.py`

- [ ] **Step 1: Implement lexical scopes and the finite abstract domain**

Implement `Scope(parent, bindings)`, nearest-binding lookup, and child scopes
for functions, lambdas, classes, and comprehensions. Implement abstract values
for finite strings, import origins, exact-key containers plus value union,
call-result origin, and selector-input taint. Evaluate `Name`, `Attribute`,
`Dict`, `List`, `Tuple`, exact-key `Subscript`, and straightforward `Call`.

- [ ] **Step 2: Restrict findings to dispatch sinks**

Emit findings only for comparison/match/membership/prefix operations,
tainted-key mapping selection, or invocation of an imported/container-derived
callable with tainted selector input. Do not inspect arbitrary call arguments
for concrete-name literals. Replace the old flattened helper in
`test_system_boundary_v2.py` with the new utility; retain all previous positive
and harmless cases.

- [ ] **Step 3: Run Slice 5 GREEN**

Run:

```bash
.venv/bin/python -m pytest tests/test_system_boundary_v2.py -q
```

Expected: zero failures across old and new static cases, including the harmless
logger literal.

- [ ] **Step 4: Commit Slice 5 GREEN**

```bash
git add tests/_task10_dispatch_ast_v2.py tests/test_system_boundary_v2.py
git commit -m "test: make task10 dispatch audit scope aware"
```

### Task 12: Full verification, packaging, and same-commit evidence

**Files:**

- Do not modify files during verification

- [ ] **Step 1: Run the focused Task 10 and Task 8B/8C gate**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_contracts_v2.py \
  tests/test_randomness_v2.py \
  tests/test_randomness_v2_subprocess.py \
  tests/test_selection_v2.py \
  tests/test_support.py \
  tests/test_statistic_lagged_pearson.py \
  tests/test_statistic_binned_nette.py \
  tests/test_null_circular_shift_v2.py \
  tests/test_null_block_shuffle_v2.py \
  tests/test_null_token_vectors_v2.py \
  tests/test_owned_transform_v2.py \
  tests/test_resolution_v2.py \
  tests/test_calibration_v2_observed.py \
  tests/test_calibration_v2_replicates.py \
  tests/test_calibration_v2_integrity.py \
  tests/test_calibration_v2_finalization.py \
  tests/test_calibration_v2_failures.py \
  tests/test_in_memory_execution_budget_v2.py \
  tests/test_result_invariants_v2.py \
  tests/test_system_boundary_v2.py \
  tests/test_public_api_v2.py -q
```

Expected: zero failures. Any unexpected skip in a new capsule/graph/AST test is
a failure.

- [ ] **Step 2: Run the complete suite and exact branch-coverage gate**

Run serially:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest --cov=selcal --cov-branch --cov-report=term-missing --cov-fail-under=95
```

Expected: both exit zero; coverage is at least 95%. The fresh-wheel child must
not add a temporary installed source tree to coverage.

- [ ] **Step 3: Run static, type, whitespace, and build gates**

Run:

```bash
.venv/bin/python -m ruff check src tests
.venv/bin/python -m mypy src
git diff --check
selcal_capsule_dist=$(mktemp -d)
.venv/bin/python -m build --outdir "$selcal_capsule_dist"
```

Expected: every command exits zero and the temporary directory contains one
sdist and one wheel. Do not build into or rewrite the repository `dist/`.

- [ ] **Step 4: Run fresh-wheel and package-document checks**

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_public_api_v2.py::test_readme_v2_example_is_self_contained_and_executable \
  tests/test_public_api_v2.py::test_readme_example_test_uses_fresh_installed_artifact_with_timeout \
  tests/test_public_api_v2.py::test_readme_fresh_install_subprocess_scrubs_parent_coverage_controls \
  tests/test_public_api_v2.py::test_package_data_includes_both_boundary_and_approved_v2_architecture \
  -q
```

Expected: zero failures with the imported `selcal.__file__` under the temporary
install target.

- [ ] **Step 5: Freeze the implementation commit identity**

Run:

```bash
git status --short --untracked-files=all
git log --oneline -12
git rev-parse HEAD
```

Expected: clean worktree, the ten serial RED/GREEN commits in order, and one
exact final code hash. Do not call the hash Task 10 completion evidence yet.

### Task 13: Independent dual review and stop decision

**Files:**

- Read only: exact final code commit and this design/plan

- [ ] **Step 1: Obtain an independent specification review**

Give the reviewer the exact final hash, design, plan, five RED commits, five
GREEN commits, and full command outputs. Require separate findings for capsule
coverage, external boundary, runtime imports/discovery, signatures/failure
priority, graph limits, AST scopes, resources, and claim ceiling.

Expected acceptance: `0 BLOCKER / 0 MAJOR / 0 MINOR`. A reviewer request for
clarification is not a PASS.

- [ ] **Step 2: Obtain an independent code-quality review**

Use a different fresh reviewer. Require inspection of production diff,
test-strength/migration, closure contents, descriptor handling, external-leaf
manifest, algorithmic complexity, and the absence of hidden injection seams.

Expected acceptance: `0 BLOCKER / 0 MAJOR / 0 MINOR`.

- [ ] **Step 3: Apply the stop gate**

Stop and open another RED/GREEN correction slice if either review finds a
semantic change, missed `selcal.*` edge, unlisted external leaf, reachable
runtime import, runtime inspect/discovery, mutable test seam, graph truncation,
false-negative AST case, resource regression, or overbroad claim.

Only when both reviews and every same-commit verification pass may the parent
consider a separate evidence update. Do not check Task 10, edit the filter net,
or claim M6/release/SoftwareX readiness in this implementation sequence.
