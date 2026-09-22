# Adversarial code review: exact enumeration null + attainability guard (2026-09-22)

Scope: (A) `circular_shift_exact_v1` + `enumerate_token` wiring; (B) `workflow.attainability` guard and
`--allow-unattainable-plan`. No file under `src/` or `tests/` was modified. Scratch scripts:
`/private/tmp/claude-501/-Users-vincent/c06ce93c-0819-478c-9b9b-68eaafcc9993/scratchpad/review2/`
(`forge.py`, `guard.py`, `e2e.sh`, `tamper_record.py`, `tamper.sh`, `budget.sh`).

Caveat: the pre-change snapshot directory (`.../scratchpad/snap/`) **did not exist**, so the review could not
use `diff` against it. `git diff HEAD` mixes in many unrelated uncommitted changes. Instead the review read
every call site of `enumerate_token`, `circular_shift_exact_v1`, `enumeration_replicate_count_mismatch_v1`
and `attainability` directly.

Test baseline: the new tests plus the neighbours (exact null, enumeration, attainability, circular v2, workflow,
CLI, resolution) gave **225 passed**. The full suite without `test_benchmark_plot.py` (matplotlib absent) gave
**3587 passed, 14 failed, 1 skipped**. The failures are all hash, manifest or environment gates:
- 12 x `tests/task10/test_authority_amendment_scope_v1.py`: `DENY_BY_DEFAULT_PATH_SET_MISMATCH`, 3917 vs 109 files.
- `test_benchmark_in_memory.py::test_recorded_standard_receipt_is_bound_to_current_source_harness_and_contract`: source digest drift.
- `test_documentation.py`: sphinx is not installed.

None is behavioural, but see R-6.

## Verdict summary

| # | Item | Verdict |
|---|------|---------|
| 1 | Forged or tampered exact-null results vs `verify_calibration_result` | **DEFECT** (integrity gap) |
| 2 | Sampling-null regression from the executor, fingerprint or descriptor changes | CONFIRMED-OK |
| 3 | Fail-closed B check bypasses; replay through the file workflow | CONFIRMED-OK (with RISK R-3, R-4) |
| 4 | Guard math | Formulas CONFIRMED-OK; **DEFECT** in float-vs-`Fraction` alpha comparison; **DEFECT** (minor) in the cap reported under B-mismatch |
| 5 | End-to-end CLI | CONFIRMED-OK for B=99 and B=50 paths (RISK R-1, R-2) |
| 6 | Docs vs behaviour | **DEFECT** (README floor claim false for the sampling null); RISK spec drift, budget ceiling |

---

## 1. Forgery or tampering of exact-null results: DEFECT

Neither result-token verifier checks the enumeration contract. That covers the module one,
`resolution_v2._verify_exact_circular_result_token` (l.~1233), and the frozen leaf inside the verifier factory (l.~1745-1768).
Both check each token **in isolation**: ownership digests, `0 <= shift < n`, and `is_identity == (shift == 0)`. The verifier
loop in `contracts_v2.verify_calibration_result` (l.~1414) passes each token to the leaf with no replicate id. It keeps
no cross-replicate state. Nothing therefore enforces:
- `shift == replicate_id + 1`,
- that shifts are distinct, or that every non-identity state is used exactly once,
- that the identity state (shift 0) never appears as a replicate (the generator can never emit it),
- `planned_replicates == n - 1` for an enumerating null (the B check lives only in `_prepare_calibration`).

Reproduction: `.venv/bin/python <scratch>/review2/forge.py` from the repo root. It uses n=12 and genuine data from
`tests/test_calibration_v2_enumeration.py`. Genuine run: p=1/6, E=1.

| Forgery | Result |
|---|---|
| F1 one non-exceeding outcome copied into the exceeding slot (state 1 missing, another state twice) | **ACCEPTED**, p 0.167 -> 0.083 |
| F2 all 11 replicates reuse one non-exceeding state | **ACCEPTED**, p=0.083 |
| F3 identity state (shift 0) as replicate 0, carrying the observed statistics | **ACCEPTED** |
| F6 states permuted (`shift != id+1`, multiset intact) | **ACCEPTED** |
| F7 COMPLETE result for an exact-null plan with B=5 (< n-1), shifts 1..5, genuine per-shift statistics | **ACCEPTED** (the real calibrator returns NOT_EVALUABLE for this plan) |
| F4 shift == n | rejected ("outside its bound state universe") |
| F5 one token renamed to `circular_shift_v2` | rejected (mixed null contract); an all-renamed record fails the ownership check |

Through the file workflow (`bash <scratch>/review2/tamper.sh`, run after `e2e.sh`), the genuine B=99 record
(p=0.03, exceeding shifts [1, 99]) was rewritten so all 99 replicates reuse one non-exceeding state (p=0.01):
- `selcal verify rec --max-bytes 50000000` gives exit 0, COMPLETE, p=0.01, reject_null=true.
- `selcal report ...` gives exit 0, and the HTML reports p=0.01.
- `selcal verify ... --replay` gives exit 4, `replay_mismatch`. **Only replay catches it.**

The forged p=0.01 sits below the `null_state_p_floor` 0.03 that the same `verify` output prints. For the exact null
that value is mathematically impossible.

Is this a real gap? The honest calibrator is sound: its tokens come from `enumerate_token(replicate_id)` under frozen
descriptor and fingerprint checks. Also, without the pair the verifier cannot recompute statistics for any null, so
forging statistic values is an old, documented limitation ("not input provenance"; `historical_execution_authenticated: false`).
The new part is different. "Exact" is a **structural** claim that can be checked from retained tokens alone, at O(B) cost, and it is
not checked. So a result with repeated or missing states, or a partial enumeration, carries every genuine per-shift
statistic, passes verification, and reports a wrong "exact" p. The in-calibrator `terminal_verifier` reuses the same
leaf, so it would not catch a future executor bug that repeats states either.

Suggested fix: in the verifier, when the null is `circular_shift_exact_v1`, require `planned_replicates == observed_length - 1`
and `outcome.transform_token.state.shift == replicate_id + 1` for every outcome. That also excludes identity and duplicates. Add
F1/F2/F3/F6/F7 as RED tests.

## 2. Sampling-null regression: CONFIRMED-OK

- Executor (`calibration_v2.py` l.~2574): `enumerate_token is None` goes to `sample_token(random_capability)`, the original call.
  The random stream and seed digest are created identically on both branches.
- Light fingerprint (l.~1497) appends `None` for non-enumerating nulls. The operation-object and descriptor tuples
  (l.~1962, l.~1994) splat an empty tuple. Both are deterministic per prepared object, so the checkpoint equality is unaffected.
- `resolution_v2` freezes `enumerate_token` only if `hasattr(type(bound), "enumerate_token")`. The drift check (l.~2088)
  requires None-ness to match and, when present, identical descriptor and callable. Registered types are exact-type checked,
  so a sampling bound cannot gain the attribute.
- Evidence: the documented example (`examples/workflow/pearson.json`, `circular_shift_v2`, B=199) still gives p=0.015,
  lag 2, 199 replicates, and `verify --replay` gives MATCH. `test_null_circular_shift_v2.py`, `test_examples.py` and the
  full suite show no behavioural failures.

## 3. Fail-closed B check: CONFIRMED-OK

- `_prepare_calibration` is the only preparation path (`calibrate_selected_family` l.~2909). The check sits after
  bind/snapshot and before observed evaluation, the budget check and any replicate.
- Block null: no `enumerate_token`, unaffected. v1 migration maps only `circular_shift_v1 -> circular_shift_v2`
  (`migration_v1_to_v2.py` l.597), so it cannot reach the exact null. The workflow calls the same public calibrator.
- Replay: the B=50 run with `--allow-unattainable-plan` gives NOT_EVALUABLE (exit 7), and `verify --replay` gives exit 7, MATCH. The B=99 run gives MATCH.
- The gap is on the verification side, not execution. Item 1 F7 shows a forged B != n-1 COMPLETE result verifies.

## 4. Guard math

Confirmed correct (`bash`/`guard.py`):
- State count `n - 2m + 2` equals `CircularShiftNullV2.total_state_count` for (n,m) = (10,1), (10,3), (11,5), (30,7).
- Collision argument: shift `s = (c* - c) mod n` makes the shifted source at lag c equal the source at lag c* on the
  same window, including the wrap for c > c*, so the decision statistic is at least the observed one. It holds bitwise for
  `max_upper` and `max_absolute`. For m=1 the collision count is K (the number of lags) whatever the spacing. Over 45 exact runs
  (n=40; lags (1,2,3), (1,4,9), (2,7); weak and strong signal) the minimum exact p equalled the floor (0.075, 0.075, 0.05). There were no violations.
- Sampling cap `P(Bin(B, floor) <= floor(alpha(B+1)) - 1)`: the sampling null draws identity among the `n-2m+2` states, so
  `floor` is the per-draw collision probability. n=100, K=3, B=99: guard 0.8229, simulation 0.8247 (2e5 draws).
- alpha=0.05 with floor exactly 1/20 (n=20 K=1, n=40 K=2, n=60 K=3) gives PASS. `Fraction(0.05)` is slightly above 1/20, and runtime
  `0.05 <= 0.05` rejects, so they agree.
- Precedence: the enumeration-count check comes first. For the exact null, `min_shift != 1` fails at resolve, before the guard.
  No precedence bug found.

**DEFECT 4a: exact `Fraction(alpha)` vs runtime float comparison.** Runtime rejects when `float((1+E)/(B+1)) <= alpha`.
The guard compares exact rationals. For alphas whose binary float is below the decimal value, the guard refuses plans that
runtime can reject:
- alpha=0.3, n=10, lags (1,2,3), exact null, B=9: guard `REFUSE_NULL_STATES_TOO_FEW`, cap 0.0. Runtime with a strong lag-2
  signal: **40/40 runs reject with p=0.3**.
- alpha=1/3, B=2, sampling: guard `REFUSE_REPLICATES_TOO_FEW`, but `(1+0)/3 <= 1/3` is True at runtime.
- alpha=0.3, B=19: the cap allows E <= 4, but runtime allows E <= 5, so the cap is understated.

The impact is low: 0.05 is safe, and the flag overrides. Fix: compare the same floats runtime uses
(`colliding/states <= alpha`, `1/(B+1) <= alpha`, and allowed E = max E with `(1+E)/(B+1) <= alpha`).

**DEFECT 4b (minor):** for the exact null with B != n-1, the report says `REFUSE_ENUMERATION_REPLICATE_COUNT` but also
`monte_carlo_power_cap: 1.0` (seen in the B=50 validate/verify/report output). That run is guaranteed NOT_EVALUABLE, so the cap should be 0 or null.

## 5. End-to-end (`bash <scratch>/review2/e2e.sh`)

Config: `examples/workflow/pearson.json` with `null_name=circular_shift_exact_v1` (max_absolute, lags [1,2,3], alpha 0.05)
on `examples/workflow/series.csv` (100 rows).

| Step | B=99 | B=50 |
|---|---|---|
| validate | exit 0, PASS, attainability PASS, floor 0.03, cap 1.0 | exit 0, **outcome PASS**, attainability `REFUSE_ENUMERATION_REPLICATE_COUNT`, cap 1.0 |
| run | exit 0, COMPLETE, p=0.03, E=2, lag 2, reject true, 99 replicates | exit 2 `INVALID_REQUEST`/`unattainable_plan` |
| run --allow-unattainable-plan | n/a | exit 7 NOT_EVALUABLE, failure_stage null_bind, 0 replicates |
| verify | exit 0, replay NOT_PERFORMED | exit 7 |
| verify --replay | exit 0, MATCH | exit 7, MATCH |
| report | exit 0 | exit 7 |

- R-1 (RISK): `validate` exits 0 with outcome PASS even when attainability refuses. Scripts that gate on the exit code miss it.
- R-2 (RISK): `result_summary` omits `diagnostics`, so `enumeration_replicate_count_mismatch_v1` never appears in CLI output.
  The user sees only a bare NOT_EVALUABLE at null_bind.

## 6. Docs and other

- **DEFECT 6a (README l.114-117):** "the smallest p-value the plan can ever produce ... it also cannot go below (number of
  searched lags)/(number of null states)". That is false for the sampling null. The README's own example (`circular_shift_v2`, B=199) gives
  **p=0.015 < floor 0.03**, and the verify output shows both numbers side by side. The floor bounds the *exact* p, not the Monte Carlo p. The
  `attainability` docstring states this correctly.
- R-3 (RISK, budget ceiling): the README recommends `circular_shift_exact_v1` "whenever validate reports PASS". But B=n-1 hits the
  in-memory caps (B<=1000, BC<=5000, work<=2.5e6, roughly n^2(C+1) <= 2.5e6). Example (`budget.sh`): n=700, 8 lags gives `validate` PASS, then
  `run` exit 2 `invalid_request` (`ResourceLimitError ... BC=5592, work=4404399`). The ceiling is about n~527 at 8 lags and n~790 at 3 lags.
  Neither the guard nor the README mentions it, and the CLI error is generic.
- R-4 (RISK, doc wording): README l.330 says a wrong B "is refused before the run, as a NOT_EVALUABLE result". In the file
  workflow it is refused with exit 2 `unattainable_plan`. NOT_EVALUABLE happens only in the Python API or with the override flag.
- R-5 (spec drift): `docs/superpowers/specs/2026-09-20-exact-enumeration-null-design.md` says the parameters are `{}` (the code
  requires `{"min_shift": 1}`), registration is in `registry.py` (it is in `resolution_v2.py`), and `monte_carlo_p_floor` = 1/n
  (the code uses 1/(B+1), for example 0.0196 at B=50).
- R-6 (evidence staleness): `test_benchmark_in_memory` receipt and the task10 deny-by-default manifest no longer bind the
  current tree. This change contributes by editing `calibration_v2.py` and adding files, though other uncommitted work does too.
  Any claim that rests on those receipts needs re-recording.
