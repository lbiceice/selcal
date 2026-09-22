# remedy-confirm-v1, Stage 2 — frozen protocol (2026-09-22)

Frozen after the Stage 1 verdict (`verdict_stage1.md`, PASS S1) and BEFORE any Stage 2 data is
generated. Supersedes `protocol_stage2_DRAFT.md`. Internal evidence, not a manuscript.

## Question

Can block shuffle (`block_shuffle_v2`) be adopted as the documented fallback for plans the attainable-p
guard refuses under the circular null, i.e. is its size controlled at a resolution that separates 5% from
6.5%, including a non-circular autocorrelated null, while keeping its power?

## Data (new, generated and digested before any arm runs)

| Cell | Definition | n | R |
|---|---|---|---|
| iid | x, y independent N(0,1) | 64, 256 | 4,000 |
| ma2 | both circular MA(2): (e_t + .6 e_{t-1} + .3 e_{t-2})/sqrt(1.45), as in the sealed study | 64, 256 | 4,000 |
| ar1 | both AR(1), phi = .6, unit innovation variance, burn-in 500, not circular | 64, 256 | 4,000 |
| alt | x iid; y_t = rho x_{t-L} + sqrt(1 - rho^2) e_t, non-circular (x drawn with L extra leading values, then trimmed); rho in {.3, .6}; signal at the LAST searched lag L | 64, 256 | 1,000 per rho per L |

Null cells are shared by both L values. Seeds: every innovation vector uses PCG64 seeded with
`int(sha256("SelCal/remedy-confirm-v1|stage2|{cell}|{n}|{rho_or_-}|{L_or_-}|{index}|{role}").hexdigest()[:16], 16)`.
Inputs are written to `stage2_inputs/` as `.npz` with a manifest of SHA-256 digests before any run.

## Plan

Candidates lags 1..L, L in {2, 8}; lagged Pearson; max_upper; alpha .05; tie tolerance 0.

## Arms (production unless marked)

| Arm | Definition |
|---|---|
| C0 | `circular_shift_exact_v1`, B = n - 1 (reference; exact under circular exchangeability) |
| C1 | `block_shuffle_v2`, B = 199, block length d = smallest divisor of n with d >= max(L, ceil(sqrt(n))): d = 8 at n = 64, d = 16 at n = 256, for both L |
| C2 | best lag by one-sided textbook Pearson p, Bonferroni over L lags (re-implementation, comparator) |

Production root_seed per input: `int(sha256("SelCal/remedy-confirm-v1|stage2|root|{cell}|{n}|{rho_or_-}|{L}|{index}").hexdigest()[:16], 16) >> 1`
(kept below 2^63). Runs are executed in parallel worker processes; every run's decision is stored by key
and index, and every production result passes `verify_calibration_result`.

## Pre-registered decision

ADOPT block shuffle as the fallback iff BOTH:
- A1. C1 size: 95% Clopper-Pearson UPPER bound <= .065 in every null cell x n x L (12 rows).
- A2. C1 power at rho .6, L = 8, n = 64 >= 80%.

Otherwise REFUSE-ONLY: the guard keeps refusing unattainable circular plans, the limitation is
documented, and randomized ties are offered only as the exact-but-capped option.

Reported but not deciding: C0 size in every null cell (circular exchangeability does not hold for AR(1);
expected approximate), C0 power at n = 256, L = 8 (the guard predicts it is attainable, floor 8/256),
C2 size and power, and McNemar C1 vs C2 in alternative cells.

## Rules

No production code change during Stage 2; if one is found necessary Stage 2 stops. No cell, n, L, arm or
seed may be added or dropped after seeing results. Adverse results are reported as they come out.
Non-complete production runs are counted as non-rejections and listed; they are never dropped.
