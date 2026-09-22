# Task 10 cross-module operation capsules correction

**Status:** fourth-round correction design approved for implementation planning;
implementation has not started and Task 10 is not closed
**Reviewed baseline:** `4d9b736f8b7839caec37f9a408ed455e1e72488a`
**Scope:** ordinary post-seal Python rebinding at the SelCal v2 execution and
verification boundary. This document does not close Task 10, M6, release, UI,
manuscript, SoftwareX, scientific-validity, or external-validation gates.

## 1. Adverse finding and decision

The third-round behavior guard is incomplete for three independent reasons.

1. `_freeze_behavior_global_guard` follows only functions whose `__globals__`
   object is `calibration_v2`'s globals dictionary. A captured function defined
   in `randomness.py`, `statistics/*.py`, `nulls/*.py`, `contracts_v2.py`,
   `canonical_v2.py`, or `resolution_v2.py` remains free to resolve its own
   module globals after sealing. Rebinding one of those helpers can therefore
   change a COMPLETE result, a seed identity, or terminal verification.
2. Capturing the `ReplicateRandomSource` class object does not capture its
   `__init__`, `randbelow`, `_next_raw64`, or `seed_digest_sha256` descriptors.
   Attribute dispatch through the captured class or an instance remains a live
   class-dictionary lookup.
3. The current AST audit flattens bindings collected by `ast.walk`. It can miss
   module-qualified calls and values reached through containers/subscripts, and
   it can merge unrelated bindings from sibling lexical scopes.

The selected correction is **definition-time operation capsules plus a bounded
test-time cross-module proof**. The running scientific path receives only
already-sealed leaf operations. It performs no graph discovery, bytecode
inspection, dynamic import, or live descriptor resolution.

A wider runtime scan of `sys.modules` is rejected. It would either stop before
the relevant behavior, walk an effectively unbounded third-party graph, or
remain vulnerable to replace-use-restore attacks between checkpoints.

## 2. Threat model

### 2.1 In scope

The correction must make the result invariant, or fail with a typed
`V2IntegrityError` before returning a result, under ordinary post-seal:

- rebinding of attributes in every project-owned `selcal.*` module reached by
  calibration, statistic, null, randomness, selection, or verification;
- rebinding of the `ReplicateRandomSource` class and its `__init__`,
  `randbelow`, `_next_raw64`, and `seed_digest_sha256` descriptors;
- rebinding of registered statistic/null class operation descriptors after the
  resolver has sealed the operation;
- replacement followed by restoration inside an untrusted callback;
- replacement of imported aliases used by canonical, support, ownership,
  token, resolution-context, and verifier helpers;
- ordinary inspection and direct invocation of a closure-reachable callable.

No closure-reachable callable other than the guarded `_execute_replicates`
itself may accept a prepared graph and perform B-scale work. Capsule leaves may
perform one bounded primitive operation only.

### 2.2 Deliberate live observations

Only two live module observations remain:

1. the public `verify_calibration_result` hook is called exactly once on every
   terminal path, before the frozen internal verifier; and
2. the executor may compare the live `select_family_v2` alias with the frozen
   selector identity as a drift sentinel, but it must invoke only the frozen
   selector.

Neither observation supplies scientific behavior. A changed selector alias
causes a typed integrity failure. A changed public verifier hook cannot replace
or bypass the frozen internal attestation.

### 2.3 Out of scope

The design does not claim protection against a hostile initial interpreter or
pre-seal import compromise; direct mutation of function `__code__` or closure
cells; direct `object.__setattr__` abuse; equivalent host-interpreter compromise
through frames, tracing, `ctypes`, or native-memory writes; concurrent
C-extension mutation; compromised Python/NumPy binaries; or arbitrary
third-party plugins. These are explicit exclusions, not implied guarantees.

## 3. Capsule model

There are exactly three capsule families. A capsule is an immutable construction
record whose callable fields are captured once and then unpacked into consumer
closures. Runtime code does not repeatedly look up a capsule through a module
attribute or a replaceable class descriptor.

Every trusted Python callable inside a capsule must satisfy all of the following:

- all behavior dependencies are closure cells or local constants;
- recursively nested code has no `LOAD_GLOBAL`, `IMPORT_NAME`, or `IMPORT_FROM`;
- it does not read a live project module dictionary;
- its direct operation is bounded independently of B, except for the single
  guarded `_execute_replicates(prepared, /)` body;
- captured external leaves are listed in the external-boundary manifest.

Factories are private, execute only during module initialization or resolver
binding, and are deleted after their canonical capsule is built. There is no
public, defaulted, closure-reachable, or module-global factory that accepts a
guard, executor, verifier, RNG, attestor, or arbitrary operation bundle.

### 3.1 Result-verifier capsule

`contracts_v2.py` owns `_ResultVerifierCapsuleV2`. Its only executable field is
the real two-positional-argument verifier. The factory captures:

- exact result, outcome, token, selection, plan, enum, and error types;
- their original slot/member descriptors used for reads;
- exact diagnostic, vector, selection, token-owner, arithmetic, and status
  validators;
- a sealed resolution-context reader;
- a sealed plan-digest operation; and
- the random capsule's seed-digest oracle, not
  construction of a live `ReplicateRandomSource` followed by property lookup.

The verifier body contains no function-local imports. The current imports from
`canonical_v2`, `randomness`, and `resolution_v2` move to module initialization,
and the captured operations are passed into the verifier factory before the
factory is deleted.

The exported `verify_calibration_result(result, resolution, /)` is the capsule's
sealed closure with the exact positional-only signature. The terminal gate
captures this real closure separately from the deliberately dynamic public
hook. The order on all four terminal paths is:

1. check expected input and plan digests;
2. call the current public hook exactly once;
3. call the captured real verifier exactly once;
4. re-read the result through captured descriptors and confirm the expected
   digests and sealed plan identity;
5. return the original result object.

`contracts_v2.py` cannot import `resolution_v2.py` while its own contract
types are still initializing. The verifier therefore uses a one-shot,
fail-closed bootstrap rather than a placeholder verifier or a function-local
import. `contracts_v2.py` defines the private capsule factory and local
contract leaves. After `resolution_v2.py` has finished defining its sealed
context reader, it supplies that reader together with the already-sealed plan
hash and random seed-oracle leaves to the factory exactly once. The returned
closure is then installed as the public verifier before `calibration_v2.py`
captures it, and the bootstrap/factory names are deleted. A second bootstrap,
an uninitialized verifier read, or an import order that exposes a placeholder
is a typed initialization failure. Tests must exercise direct package and
submodule import orders in fresh processes.

### 3.2 Random capsule

`randomness.py` owns `_RandomCapsuleV2` with three operations:

- `create_stream(plan_sha256, replicate_id, planned_replicates, /)`;
- `seed_digest(stream, /)`; and
- `randbelow(stream, bound, /)`.

The production stream is private exact state, for example an exact two-item
tuple containing the PCG64 bit-generator and seed hex digest. It is not created
by calling `ReplicateRandomSource.__init__`, and its digest is not read through
the class property. `randbelow` calls the definition-time-captured PCG64
`random_raw` descriptor (or equivalently captured native callable) and the
sealed rejection sampler; it never resolves `stream.randbelow` or
`stream.random_raw` dynamically.

The capsule captures the SHA-256 constructor, `bytes.fromhex`, `int.from_bytes`,
the PCG64 constructor, the PCG64 raw-word descriptor, exact validators, and the
frozen domain constants. The seed oracle used by the verifier shares this
capsule, so execution and verification cannot drift onto different seed
implementations.

`ReplicateRandomSource` and `uniform_randbelow` remain compatibility/test
surfaces with their existing contracts. They may delegate to the capsule, but
the production calibration and verifier paths do not call their live class or
method descriptors.

### 3.3 Execution capsules

The `_ExecutionCapsuleV2` family covers bounded scientific operations. It has
three concrete shapes within one family:

- selector operation: frozen `select_family_v2` behavior;
- statistic operation: frozen `evaluate_all(pair, /)` for the bound lagged
  Pearson or binned NetTE instance; and
- null operations: frozen `identity_token()`,
  `sample_token_from_randbelow(randbelow, /)`, `snapshot_token(token, /)`, and
  `apply(token, /)` for the bound circular-shift or block-shuffle instance.

The null sampler receives only a per-stream `randbelow(bound, /)` capability.
It never invokes `_resolve_static_callable` in production. Scripted objects and
descriptor-shape behavior remain unit-test surfaces in
`uniform_randbelow`; they are not the production scientific seam.

Each algorithm module builds its own capsule while it still owns the semantic
implementation:

| Owner module | Sealed behavior included |
| --- | --- |
| `selection_v2.py` | rule classification, tolerance handling, tie set, selected candidate, scored-vector rebuild |
| `support.py` | exact common-support construction and frozen vector reads used by both statistics |
| `statistics/lagged_pearson.py` | normalization, zero-variance/numeric failure classification, dot product, clamp, result construction |
| `statistics/binned_nette.py` | observed-edge coding, CMI, role direction, analytic failure classification, result construction |
| `nulls/owned_transform_v2.py` | ownership digests, token snapshots, safe observed/transform pair construction, content guard |
| `nulls/circular_shift_v2.py` | state sampling, token construction/snapshot, source rotation, exact postconditions |
| `nulls/block_shuffle_v2.py` | block labels/permutation, state sampling, token construction/snapshot, source reorder, exact postconditions |
| `resolution_v2.py` | exact bound-state reads and construction of the correct algorithm capsule from canonical registration identity |
| `calibration_v2.py` | preparation, observed scan, transform/result validation, guarded replicate loop, terminal construction |

`resolution_v2._FrozenOperationV2` is only an ordinary descriptor/callable
snapshot and cannot be treated as the new capsule. The resolution snapshot must
carry the algorithm capsule leaf callable plus immutable identity evidence. The
resolver reads bound state through definition-time-captured slot descriptors;
the execution leaf likewise uses captured descriptors or copied frozen state,
not `bound.method` lookup after sealing.

The public calibrator remains exactly
`calibrate_selected_family(pair, resolution, /)`. The private executor remains
exactly `_execute_replicates(prepared, /)`, retains the real `history` local for
Task 8B callback/history tests, and applies the prepared-budget guard before RNG,
token, outcome, or B-sized allocation. NULL_BIND and observed-statistic failure
continue to terminate before the executor and therefore retain their current
priority over the execution budget.

## 4. Cross-module bounded proof

The proof is a test/build-time structural verifier, not a runtime defense. Its
roots are the exact public calibrator, private executor, terminal gate, sealed
real verifier, random capsule leaves, selector leaf, and the statistic/null
capsule leaves reachable from every canonical v2 registration.

### 4.1 Project-owned traversal

A Python function is project-owned only when both conditions hold:

- `function.__module__` begins with `selcal.`; and
- its resolved source file is under the installed `selcal` package root.

For project-owned nodes, traverse:

- closure-cell values;
- exact tuple/NamedTuple capsule fields;
- `staticmethod` and `classmethod` underlying functions;
- property `fget`, `fset`, and `fdel` when a trusted root captures the property;
- nested code objects in `co_consts`; and
- values resolved by a project-owned function's `LOAD_GLOBAL` while a RED is
  being diagnosed.

The accepted graph must ultimately contain no behavior-bearing
`LOAD_GLOBAL`, `IMPORT_NAME`, or `IMPORT_FROM`. The diagnostic resolution of
`LOAD_GLOBAL` exists to produce a complete failure path; it is not an
allowance. The only live observations named in section 2.2 are represented as
explicit, exact sentinels and separately asserted.

Traversal limits are fixed at depth 32, 512 unique nodes, and 4096 edges. A
limit hit is a proof failure with the root and frontier reported; traversal must
never silently truncate. Cycles are cut by object identity.

### 4.2 External leaves

The proof stops at, and records, non-project leaves:

- built-in types/functions/descriptors;
- CPython/stdlib C-extension callables such as SHA-256 leaves;
- NumPy constructors, ufuncs, ndarray/PCG64 descriptors, and other NumPy
  callables captured by identity; and
- explicitly enumerated pure-Python stdlib or NumPy wrappers.

Each record contains provider module, qualified name, object identity category
(built-in, method descriptor, C callable, or external Python callable), and
Python/NumPy version. The proof does not recurse through NumPy, the standard
library, or arbitrary third-party packages. An unlisted external leaf fails.
Changing a `selcal.*` alias to an external object after capsule construction is
inert or fail-closed; mutating the external provider's own internals is outside
the claim.

## 5. Runtime and resource contract

- Capsule construction occurs once at module import or once per canonical
  adapter/null binding. The replicate loop performs zero `inspect`, `dis`, AST,
  source-file, import, or graph-walk calls.
- Runtime imports inside all trusted roots are zero.
- RNG state is O(1) per active replicate. The correction adds no B-by-C,
  B-by-N, or B-by-S mirror and no second exact-B outcome/history collection.
- Existing q=4096 preallocation ordering, B/C/N/S/work caps, exact-B outcome
  retention, and callback frame/history contracts remain unchanged.
- Graph proof is CI-only and must complete within 2 seconds on the supported
  development interpreter. A timeout or a node/edge cap hit fails the gate.
- Performance acceptance is structural and allocation-based. Wall-clock
  measurements may be reported descriptively, but a tight timing ratio is not
  a portable PASS criterion.

## 6. Permitted test seams and migration rule

Permitted seams are:

- direct unit calls to a pure rejection sampler with a scripted raw-word
  callable;
- direct unit calls to a null sampler leaf with a scripted
  `randbelow(bound, /)` callable;
- direct unit calls to statistic/null capsule builders in their owner-module
  tests before the canonical consumer is sealed;
- committed deterministic seeds and real canonical kernels for integration,
  KAT, subprocess, and public API tests; and
- post-seal monkeypatches used only as attacks, where the expected result is
  unchanged output or typed fail-closed behavior.

There is no permitted public calibrator/executor/verifier injection parameter,
callable default, environment toggle, mutable registry override, or hidden
production factory retained only for tests. Existing tests that monkeypatch a
production class method to manufacture a scientific outcome must move to the
owning pure-kernel unit or use a real deterministic fixture. Existing callback
frame/history tests remain integration tests and may not be weakened to mere
call-count assertions.

## 7. Required RED matrix

### 7.1 Verifier

- Rebind `contracts_v2` plan-hash, resolution-context, slot-reader, diagnostic,
  vector, selection, token-owner, and seed-oracle helpers after sealing.
- Rebind the same helpers inside the dynamic public hook, use them, then restore
  them before the hook returns.
- Require forged p-values, token owners, seed digests, result vectors, and plan
  identities to remain rejected by the frozen internal verifier.
- Assert one public-hook call and one frozen-verifier call on COMPLETE,
  NULL_BIND, OBSERVED_STATISTIC_SCAN, and REPLICATE_EXECUTION.

### 7.2 Randomness

- Rebind randomness validators, SHA-256 alias, PCG64 alias, raw-word helper, and
  rejection-sampler helper after sealing.
- Replace `ReplicateRandomSource.__init__`, `randbelow`, `_next_raw64`, and
  `seed_digest_sha256`; also perform replace-use-restore from a callback.
- Require identical committed stream vectors and COMPLETE results, or a typed
  integrity failure before a result; no bomb may execute.
- Prove the verifier seed oracle and executor stream factory come from the same
  random capsule identity.

### 7.3 Statistics and nulls

- Rebind `support.common_support`; Pearson centering/clamp/lag helper; binned
  edge/code/CMI helpers; ownership digest/content/token helpers; circular state,
  token, and apply helpers; and block label/permutation/apply helpers.
- Rebind bound class method descriptors after resolution sealing and from an
  untrusted callback.
- Exercise both statistic-by-null combinations and analytical-failure paths;
  require stable exact results or typed fail-closed behavior.
- Prove production null sampling never reaches `_resolve_static_callable`.

### 7.4 Graph and imports

- Show the old same-module walker omits at least one reachable function from
  each of `randomness`, `contracts_v2`, `statistics`, and `nulls`.
- Show the new proof reaches every project-owned capsule leaf, records every
  external boundary, and does not recurse into NumPy.
- Assert recursive `IMPORT_NAME`/`IMPORT_FROM` and uncontrolled `LOAD_GLOBAL`
  sets are empty for all trusted roots.
- Make graph depth/node/edge caps fail closed and prove graph construction is
  never called during calibration or verification.

### 7.5 Lexical AST analyzer

- Catch `catalog.choose_adapter(name)` and a renamed module-qualified chooser.
- Catch an imported callable stored as a dictionary value and invoked through
  an exact-key subscript.
- Catch a factory-call result stored in a container and later invoked.
- Keep sibling functions with the same local name independent.
- Let a nested closure inherit the enclosing imported origin and input taint.
- Keep `logger.info("circular_shift_v2")` and a plain descriptive constant
  finding-free.

## 8. Lexical AST analysis contract

The analyzer uses a scope stack for module, function, lambda, class, and
comprehension scopes. Assignments update only the current scope; lookup walks to
the nearest enclosing binding. Function parameters are bound in the child
scope, and sibling functions never share local bindings.

Its bounded abstract values are:

- finite static-string sets;
- exact import origins, including module aliases and attribute chains;
- container values with exact literal-key entries plus a conservative value
  union;
- call-result origins; and
- input/selector taint propagated through assignments and exact subscripts.

It evaluates `Name`, `Attribute`, `Dict`, `List`, `Tuple`, exact-key
`Subscript`, and straightforward `Call` results. Findings are emitted only at
dispatch sinks: comparison/match/membership/prefix tests, mapping get/subscript
selected by tainted input, or invocation of an imported/container-derived
callable with tainted selector input. Arbitrary call arguments are not searched
for concrete names, which keeps logging and documentation literals out of the
finding set. Dynamic reflection, decoded strings, arbitrary interprocedural
flow, and runtime-generated code remain outside this bounded source audit.

## 9. Claim ceiling

After all RED/GREEN slices and independent reviews pass, the maximum permitted
claim is:

> Within a trusted initial Python interpreter, the enumerated SelCal v2
> capsules provide bounded deterministic integrity against ordinary post-seal
> rebinding of project-owned module and class attributes. Trusted runtime roots
> contain no dynamic imports or runtime inspect/discovery, and external
> built-in/NumPy/C leaves are captured and explicitly bounded.

This is not a sandbox, tamper-proofing result, security proof, validation of
NumPy internals, scientific validation, release qualification, or SoftwareX
readiness statement.

## 10. Unacceptable shortcuts

- extending the current runtime globals guard across `sys.modules`;
- traversing unlimited stdlib, NumPy, plugin, or third-party graphs;
- treating a captured class identity as proof that its methods/properties are
  frozen;
- keeping dynamic imports inside the verifier or any trusted callable;
- running `inspect`, `dis`, source parsing, or graph traversal per replicate;
- cloning Python functions into a mutable private globals dictionary and
  treating obscurity as a seal;
- concrete adapter-name branches or per-adapter allowlists in the generic
  calibrator;
- hidden guard/executor/verifier/RNG/attestor injection seams for tests;
- weakening callback-frame/history, NULL_BIND priority, observed-failure
  priority, exact signatures, or q=4096 allocation tests;
- translating integrity drift into an ordinary analytical failure or
  `NOT_EVALUABLE`; or
- describing the result as secure, tamper-proof, M6-complete, or submission
  ready.

## 11. Acceptance and stop gate

Implementation may be considered a Task 10 engineering candidate only after
five serial RED/GREEN slices—verifier, random, statistic/null execution, graph
proof, and lexical AST analyzer—are individually committed and reviewed. The
complete suite, branch coverage at least 95%, Ruff, strict mypy, build,
fresh-wheel execution, package-document checks, memory/resource checks, and
`git diff --check` must pass on the same final code commit.

A fresh specification review and a separate code-quality review must each
report `0 BLOCKER / 0 MAJOR / 0 MINOR`. Any semantic drift, missing project-owned
edge, unlisted external leaf, trusted dynamic import, graph-cap failure,
resource regression, or review finding stops the sequence. Passing this gate
still does not authorize marking Task 10 complete until the parent plan is
updated in a separate evidence-backed action.
