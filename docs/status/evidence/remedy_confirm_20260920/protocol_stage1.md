# remedy-confirm-v1, Stage 1 — frozen protocol (2026-09-20)

Frozen BEFORE any Stage 1 computation. Internal evidence, not a manuscript. Derived from
`../comparator_arms_20260919/remedy_blueprint_20260919.md` §7 Stage 1, with the deviations below
stated up front.

## Inputs

The sealed 1,200 study inputs (`../bounded_study_execution_20260909/study_v1/inputs`), unchanged:
iid null 400, circular MA(2) null 400, lag2 rho .3 200, lag2 rho .6 200; n = 64.
Candidate sets: L in {2, 4, 8} = lags 1..L; window t = L..63; statistic max over lags of
Pearson(x[t-lag], y[t]); selection max_upper; alpha = .05; one-sided upper tail, `>=`, tie tolerance 0.

## Arms

| Arm | Definition | Who runs it |
|---|---|---|
| C0 | circular shift, exact enumeration of all 64 states, p = #{s : T_s >= T_0}/64 | production `circular_shift_exact_v1`, B = 63 |
| C1 | `block_shuffle_v2`, block_length 8 (8 blocks), B = 199, full reselection | production |
| C1r | block shuffle re-implementation, same plan, independent seeds | re-implementation (sanity) |
| C2 | best lag by textbook Pearson p, Bonferroni over L lags | re-implementation (comparator) |
| C3 | randomized ties on the exact enumeration: p = (E_> + U * E_=)/64, U ~ Unif(0,1] | re-implementation (descriptive only) |

Seeds: production arms use the sealed per-input `root_seed`; re-implementation arms use
`int(sha256("SelCal/remedy-confirm-v1|{cell}|{index}|{arm}|L{L}").hexdigest()[:16], 16)` with PCG64.
Environment: production arms on the project environment (Python 3.11.12, numpy 2.4.6); re-implementation
arms in the isolated comparator env (numpy 2.4.6, scipy 1.16.2). Both recorded in the results file.

## Endpoints

Per arm x cell x L: K/R, rate, 95% Clopper-Pearson interval. Exact two-sided McNemar for C1 vs C0 and
C1 vs C2 in the alternative cells.

## Pre-registered decision rules (unchanged from the blueprint)

PASS S1 requires ALL of:
1. C1 in both null cells at every L: CP lower bound <= .05 AND point estimate <= .075.
2. C1 power at rho .6, L = 8 is >= 80%.
3. C1 beats C0 at rho .6 by exact McNemar (two-sided p < .05) at L = 4 and L = 8.
4. C1 and C1r null-cell intervals overlap at every L.

KILL (block shuffle is not offered as the fallback; refused plans get randomized ties plus the
documented limitation):
- K1/K2: any C1 null cell has CP lower bound > .05 or point estimate > .075.
- K3: C1 power at rho .6, L = 8 is below 50%.

C0's role here is the ceiling reference; its size decides nothing. C3 is descriptive.
The sealed null cells (R = 400) cannot resolve true sizes near 6-7%, so PASS S1 does NOT adopt block
shuffle; Stage 2 (new data, n in {64, 256}, AR(1) null) remains required.

## Deviations from the blueprint text, fixed now

- The blueprint allowed re-implementation for production plans that cannot run; production can now run
  every C0 and C1 plan here, so C1 is production at all three L values.
- C0 at L = 4 and L = 8 is expected to be powerless by the proven floor L/64 > .05. It is still executed
  and reported rather than skipped, so the ceiling is visible in the same table.

## Rules

No production code change during Stage 1. No re-running or editing of the sealed study. Adverse and
null results are reported as they come out; no cell, seed, L value or arm may be added or dropped after
seeing results. Stage 2 gets its own frozen protocol.
