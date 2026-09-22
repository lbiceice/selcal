# Task 10 trusted call-boundary correction

**Status:** approved correction design; implementation not yet accepted
**Input under review:** `ddb804bcc8a1a62063e126281f7948bf540ecfbb`
**Scope:** Task 10 engineering boundary only. M6, UI, persistence, release,
license, DOI, manuscript, and SoftwareX readiness remain `HOLD / NOT DUE`.

## 1. Problem statement

The first budget correction froze module-level names but retained two unsafe
escape paths:

1. an injectable module-level calibration core accepted caller-supplied budget
   and executor callables;
2. the exported private executor closed over a raw loop callable that performed
   no budget check of its own.

The public calibration path also looked up the terminal-return helper through a
module global, so ordinary replacement of that helper could return a result for
a different input. Separately, the fresh-wheel README subprocess inherited
pytest-cov variables and made the exact Task 12B coverage command measure a
second temporary source tree. The static concrete-name audit and the oversized
integer diagnostic contract also overstated what the current bytes proved.

These are engineering-integrity defects. They do not imply a scientific result,
release defect, or SoftwareX decision.

## 2. Alternatives considered

### A. Full-body sealed closures — selected

Construct the complete replicate loop as the body of the returned
`_execute_replicates(prepared, /)` closure. Its first operation is the frozen
prepared-budget guard. Construct the complete public calibration path as the
body of the returned `calibrate_selected_family(pair, resolution, /)` closure.
It captures the budgeted executor and the exact terminal-return helper at
definition time. Delete the construction factories after initialization.

There is no raw loop callable, no injectable calibration core, and no callable
capable of B-scale work that omits the budget gate. Closure inspection may reveal
only guarded callables and immutable/frozen operations; direct invocation of any
revealed executor remains fail-closed.

### B. Immutable runtime object — rejected

A frozen runtime instance could own the same operations, but its class,
constructor, bound methods, and class attributes would add new mutation and
inspection surfaces. It also changes more of the existing callback-frame shape.

### C. Secret seal or token — rejected

A process-local token cannot provide a meaningful same-process boundary because
ordinary introspection can recover it. This would hide, rather than remove, the
unguarded core.

## 3. Trusted execution architecture

### 3.1 Budgeted private executor

The final module contains one callable named `_execute_replicates` with the
exact signature `(prepared, /)`. Its own code frame contains the complete loop,
including `history`, so the existing Task 8B callback and terminal-history tests
continue to inspect the real execution frame.

The first semantic action is:

1. verify preparer ownership;
2. derive frozen `B`, `C`, `N`, and generic `S`;
3. apply the definition-time-frozen integer budget;
4. only then touch RNG, tokens, transformations, outcomes, history, or
   signatures.

No separately callable unguarded loop remains in a module global or closure
cell. Extracting any callable from `_execute_replicates` through ordinary
inspection must not yield a path to B-scale work without the same budget check.

All behavior-critical module globals used directly by the executor are frozen
at factory definition, including constructors, contract types, validators,
snapshotters, numeric operations, casts, and builtins. A recursive identity
manifest also covers same-module globals reached through captured helper and
bundle callables, including globals loaded by nested generator/comprehension
code. It is checked before and after untrusted callback boundaries. The
captured module globals mapping is used at runtime only for that fail-closed
identity manifest and the intentional live selector identity check; replacing
the frozen direct module aliases cannot change a verified result.

### 3.2 Public calibrator

The final public callable keeps the exact signature `(pair, resolution, /)` and
contains the complete public flow. Its security-relevant closure captures at
definition time:

- the exact prepared-budget guard;
- the already budgeted private executor;
- the exact terminal-return helper;
- the canonical preparation and identity operations needed by the flow.

It must not capture or expose an injectable core accepting a guard, executor, or
attestor argument. The terminal helper is itself a closure containing only the
definition-time real verifier as its security-relevant nonlocal; it has no
`_attest_result` parameter or callable default. It continues to call the public
`verify_calibration_result` hook exactly once, then runs the captured real
verifier and rechecks the real semantic-input and plan digests.
Replacing the module attribute `_verify_terminal_result_before_return` must not
change the helper used by the public calibrator on COMPLETE, NULL_BIND,
OBSERVED_STATISTIC_SCAN, or REPLICATE_EXECUTION paths.

The public and terminal closures likewise contain no direct `LOAD_GLOBAL`
operations. The public closure freezes preparation, type guards, constructors,
`sum`, casts, plan/input hashing, and the guarded executor. The terminal closure
freezes its error type, resolution validator, plan hash, and real verifier. Its
captured module globals mapping retains only the intentional public verifier hook
plus the recursive fail-closed identity manifest; the dynamic
hook is called exactly once before the frozen real verifier.

### 3.3 Threat boundary

Required coverage includes ordinary module attribute replacement, callback
replacement, registry/field drift, and ordinary inspection followed by direct
invocation of a revealed callable. The design does not claim protection against
in-place `__code__` mutation, closure-cell mutation, direct
`object.__setattr__` abuse, C-extension memory writes, or equivalent host
interpreter compromise.

## 4. Coverage-isolated installed-artifact test

The README example continues to build and install a fresh wheel into a temporary
target, run outside the repository, assert that `selcal.__file__` is under that
target, and use explicit timeouts. Before launching that subprocess, the test
removes `COV_CORE_*` and `COVERAGE_PROCESS_START` from the child environment.
The exact Task 12B command must again report only the canonical source tree and
meet `--cov-fail-under=95`.

## 5. Bounded static architecture audit

The concrete-name test is a bounded intra-module audit, not a proof against
arbitrary Python reflection. It must:

- evaluate literal concatenation, static f-strings, and static `join` forms;
- track imported symbols, module-qualified attributes, and local aliases;
- propagate import origins through straightforward assignments and containers;
- inspect compare, match, membership, `get`, subscript, prefix/suffix, and
  ordinary dispatch-call contexts;
- reject the routine lowercase imported mapping and local-alias examples from
  the adverse review;
- avoid describing a harmless literal outside a dispatch context as a branch.

The test name and docstring must state this bounded scope. Dynamic reflection,
runtime decoding, arbitrary interprocedural data flow, and hostile code-object
construction remain outside the claim.

## 6. Oversized integer diagnostic

For positive built-in integer operands of at most 256 bits, the existing stable
message retains `B,C,N,S,BC,BS,work` and all caps. If any operand exceeds 256
bits, the gate must reject before product or decimal materialization with the
stable abbreviated `integer magnitude exceeds safe diagnostic envelope`
message and all four caps. The architecture document must record this explicit
exception to the ordinary detailed-message contract.

## 7. Required RED tests

1. Direct module-level or closure-reachable invocation of any calibration core
   with injected guard or executor is impossible because no such callable
   remains.
2. Ordinary recursive inspection of the public and private closures reveals no
   unguarded executor; every revealed executor-like callable rejects an
   over-budget prepared graph before an RNG bomb.
3. The terminal gate has no injectable attestor parameter or callable default,
   and rebinding `_verify_terminal_result_before_return` cannot substitute a
   foreign result on any of the four terminal paths.
4. The exact Task 12B coverage command fails on the pre-fix bytes because of the
   temporary installed source tree, then passes after child coverage variables
   are removed.
5. Lowercase imported mappings, local aliases, generic dispatch calls, static
   f-strings/joins, and harmless non-dispatch literals establish the bounded
   static-audit behavior.
6. The packaged architecture text states the oversized-integer exception.

## 8. Acceptance gate

The correction is eligible for review only after all new RED tests fail on the
pre-fix target for the intended reasons, pass after one coherent implementation,
and the following return zero:

- Task 10 focused suites;
- all Task 8B/8C integrity and failure suites;
- the complete test suite;
- the exact Task 12B branch-coverage command with `--cov-fail-under=95`;
- Ruff, strict mypy, and `git diff --check`;
- wheel and sdist build;
- fresh-wheel README execution and packaged-document checks.

A new independent specification review and a new independent code-quality review
must both report `0 BLOCKER / 0 MAJOR / 0 MINOR`. Passing this correction closes
only the Task 10 engineering candidate. Task 11, Task 12A/B, M6, and every
downstream product/submission gate remain open.
