# Exact-enumeration null — implementation receipt (2026-09-20)

Spec: `docs/superpowers/specs/2026-09-20-exact-enumeration-null-design.md`. Author approved the
production-code change on 2026-09-19. TDD, one RED->GREEN per step.

## Stage 0 first (no code change): why this was worth building

`run_stage0_exact_enumeration.py` / `results_stage0.json`, read-only over the sealed 1,200 inputs,
re-computed exact enumeration without importing SelCal: 0/1,200 numerator mismatches against the sealed
`reference_exact` tables; size 3.5% in both null cells; power 58.5% (rho .3) and 99.5% (rho .6) versus the
sealed 57.0% / 91.0%. Pass rule P-f met.

## What was built

- `src/selcal/nulls/circular_shift_exact_v1.py` (new): null `circular_shift_exact_v1`, parameters
  `{"min_shift": 1}` only (the complete group is the only group), `enumerate_token(index)` for shifts
  1..n-1, `sample_token` refuses, shares the frozen right-shift equation with `circular_shift_v2`.
- `contracts_v2.py`: the new null name is accepted on tokens; both circular nulls require
  `CircularShiftStateV2`.
- `resolution_v2.py`: registration (factory, identity snapshot, bound snapshot, result-token verifier,
  both in the module and in the frozen result-verifier leaves), pure-snapshot branch, and
  `enumerate_token` frozen as an optional bound operation with drift checks.
- `calibration_v2.py`: the replicate executor uses `enumerate_token(replicate_id)` when the bound null
  enumerates; the per-replicate random stream is still created and its seed digest still checked. Fail
  closed before any replicate when `replicates != total_state_count - 1`: NOT_EVALUABLE at stage
  `null_bind`, diagnostic `enumeration_replicate_count_mismatch_v1`.
- `workflow.py`: `attainability` branch — Monte Carlo floor 1/n, power cap 1.0 when the state floor is
  attainable, new refusal `REFUSE_ENUMERATION_REPLICATE_COUNT`.
- README: new section documenting the null, its B rule and the measured effect.
- Unchanged: the p-value formula, finalization, bounds, record format, the verifier's arithmetic, and the
  sampling null `circular_shift_v2` (still the default for existing plans). Sealed study untouched.

## Verification

- New tests: 15 (null unit) + 7 (calibration) + 19 (workflow guard, incl. 2 enumeration cases).
- Production end-to-end on all 1,200 sealed inputs (`run_production_exact_check.py`,
  `results_production_exact.json`): **0 mismatches** against the independent Stage 0 p-values; every run
  used exactly the 63 distinct non-identity states; `verify_calibration_result` passed on all 1,200.
  Rates: iid 3.5%, circular MA(2) 3.5%, rho .3 58.5%, rho .6 99.5%.
- Full suite: 3587 passed, 14 failed. Baseline before today: 3547 passed, 13 failed (12 task10
  scope-manifest drift from the pre-existing uncommitted tree, 1 missing Sphinx). The single new failure
  is the 2026-09-08 in-memory benchmark receipt, which binds source-file hashes and is now HISTORICAL;
  it was not overwritten.
- ruff check and mypy clean.

## Evidence artifacts refreshed because production bytes changed

- `tests/fixtures/verifier_structure_gate_v1.json`: builder frontier, runtime frontier and legacy
  declaration rows regenerated against current source (line numbers and segment digests only; graph
  budgets unchanged at nodes 21 / edges 20 / depth 1).
- `docs/status/scientific_code_smell_binding_20260920.json` (new, supersedes the 2026-09-08 binding,
  which is retained unchanged): schema v2 records several changed sources instead of one. Three cited
  sources changed (calibration_v2, contracts_v2, resolution_v2), ten unchanged. The 2026-08-31 audit and
  its adverse findings stay historical; no finding was promoted and no new audit is claimed.

## Scope note

A `ruff format` pass over the whole package also reformatted seven modules unrelated to this change.
Those files were restored to their pre-change bytes from the session snapshot, so the diff contains only
intentional edits.

## Not done

Blueprint Stages 1-2 (block-shuffle fallback, randomized ties, n=256 and AR(1) cells), the version-pinned
IDTxl comparator run, any change of default null for existing plans, and the manuscript. Nothing was
committed, pushed or released.
