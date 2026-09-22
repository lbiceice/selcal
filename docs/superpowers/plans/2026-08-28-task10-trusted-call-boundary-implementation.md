# Task 10 trusted call-boundary correction implementation plan

> **Execution rule:** strict RED before production edits; one implementer; fresh
> specification and code-quality reviews after every correction round.

**Goal:** remove every ordinary-call path to unbudgeted replicate execution,
freeze the real terminal attestor, restore the exact Task 12B coverage gate, and
make the static/diagnostic claims match their evidence.

**Design authority:**
`docs/superpowers/specs/2026-08-28-task10-trusted-call-boundary-design.md`
at commit `184fd26`.

## Task 1: Freeze adversarial RED evidence

**Files:**

- Modify: `tests/test_in_memory_execution_budget_v2.py`
- Modify: `tests/test_calibration_v2_integrity.py`
- Modify: `tests/test_calibration_v2_replicates.py`
- Modify: `tests/test_public_api_v2.py`
- Modify: `tests/test_system_boundary_v2.py`

- [ ] Add recursive ordinary-introspection tests proving that neither module
  globals nor closure-reachable callables expose an unguarded B-scale executor
  or an orchestration core accepting injected guard/executor/attestor callables.
- [ ] Add all-four-terminal-path tests proving replacement of the module terminal
  helper cannot substitute a foreign result, while the public verifier hook is
  still called exactly once and the frozen real verifier rejects drift.
- [ ] Add the exact Task 12B coverage command as an adverse reproduction and
  identify the temporary installed source tree in the pre-fix report.
- [ ] Add bounded static-audit cases for lowercase imported mappings, local
  aliases, ordinary dispatch calls, static f-strings/joins, and harmless
  non-dispatch literals.
- [ ] Add a packaged-design test requiring the oversized-integer diagnostic
  exception.
- [ ] Run the focused tests on `184fd26`; require failures for these missing
  guarantees, not collection, syntax, or fixture errors.
- [ ] Commit as `test: expose task10 trusted boundary gaps`.

## Task 2: Replace wrappers with guarded full-body closures

**Files:**

- Modify: `src/selcal/calibration_v2.py`
- Modify: `tests/test_calibration_v2_replicates.py`
- Modify: `tests/test_calibration_v2_integrity.py`

- [ ] Construct the complete Task 8B loop inside the returned
  `_execute_replicates(prepared, /)` closure. The frozen budget guard is the first
  semantic action; retain the real `_execute_replicates` frame and `history`
  locals. Leave no raw executor in a module global or closure nonlocal.
- [ ] Construct the complete public orchestration inside the returned
  `calibrate_selected_family(pair, resolution, /)` closure. Leave no injectable
  calibration core.
- [ ] Construct the terminal-return helper as a closure over the real verifier;
  remove the injectable `_attest_result` default. Capture this helper in the
  public calibrator while preserving one dynamic public verifier-hook call.
- [ ] Delete construction factories after initialization and preserve exact
  public/private signatures, NULL_BIND/observed-failure priority, q=4096
  allocation order, callback-frame tests, and every Task 8B/8C invariant.
- [ ] Run the new security tests plus all Task 8B/8C suites; require zero
  failures.
- [ ] Commit as `fix: seal task10 execution and attestation paths`.

## Task 3: Restore coverage isolation and truthful lint contracts

**Files:**

- Modify: `tests/test_public_api_v2.py`
- Modify: `tests/test_system_boundary_v2.py`
- Modify: `docs/architecture/null_reselection_v2_design.md`

- [ ] Remove `COVERAGE_PROCESS_START`, every `COV_CORE_*`, and other inherited
  coverage-control variables from the fresh-wheel example subprocess without
  weakening its installed-path and timeout assertions.
- [ ] Implement the bounded intra-module constant/import-alias propagation named
  in the design, or narrow the audit name/docstring to exactly the patterns it
  proves. It must pass every adverse and harmless case without claiming whole-
  program analysis.
- [ ] Document the greater-than-256-bit abbreviated diagnostic exception while
  retaining the detailed ordinary overflow message contract.
- [ ] Run focused tests and the exact Task 12B coverage command; require at least
  95% total and no duplicate temporary installed source tree.
- [ ] Commit as `fix: align task10 verification contracts`.

## Task 4: Reverify and review

- [ ] Run the complete Task 10 focused set, all Task 8B/8C suites, v1/KAT,
  migration, oracle, and the complete suite.
- [ ] Run the exact branch-coverage command, Ruff, strict mypy,
  `git diff --check`, wheel/sdist build, and fresh-wheel example.
- [ ] Confirm clean worktree and package-facing M6/UI/release/manuscript HOLDs.
- [ ] Obtain a fresh specification review and fresh code-quality review, each
  reporting `0 BLOCKER / 0 MAJOR / 0 MINOR`.
- [ ] Only then update the parent implementation plan and close Task 10.
