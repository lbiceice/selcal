# Stage 1 verdict (2026-09-22)

Protocol `protocol_stage1.md` (sha256 6e02dd9c…, frozen 2026-09-20 before any Stage 1 run).
Raw: `results_stage1_production.json` (production C0, C1; 7,200 runs, 0 non-complete, 902 s),
`results_stage1_reimplementation.json` (C1r, C2, C3), analysis `results_stage1_analysis.json`.

## PASS S1 — all four pre-registered rules met, no kill condition

| Rule | Result |
|---|---|
| 1. C1 null size: CP lower <= .05 and rate <= .075, every cell and L | met; rates 4.25-7.0% |
| 2. C1 power rho .6, L = 8 >= 80% | met; 100% |
| 3. C1 beats C0 at rho .6, L = 4 and 8 (McNemar) | met; 200 vs 0 at both L, p = 1.2e-60 |
| 4. C1 and C1r null intervals overlap | met; all 6 rows |

## What the table shows

| Arm | L | iid null | MA(2) null | rho .3 | rho .6 |
|---|---|---|---|---|---|
| C0 exact enumeration | 2 | 3.5% | 3.5% | 58.5% | 99.5% |
| C0 exact enumeration | 4 / 8 | 0% | 0% | 0% | 0% |
| C1 block shuffle (production) | 2 | 5.5% | 4.25% | 66.5% | 100% |
| C1 block shuffle (production) | 4 | 6.5% | 4.75% | 55.5% | 100% |
| C1 block shuffle (production) | 8 | 7.0% | 5.25% | 46.0% | 100% |
| C2 Bonferroni | 2 / 4 / 8 | 6.0 / 7.25 / 7.5% | **8.5 / 10.0 / 10.75%** | 69.5 / 58.5 / 48.5% | 100% |
| C3 randomized ties | 4 / 8 | 6.25 / 6.75% | 5.0 / 4.25% | 42.5 / 20.5% | 81.5 / 40.0% |

- C0 at L = 4 and 8 rejects nothing, including the strong signal: the proven floor L/64 > .05,
  reproduced by production code. C0 at L = 2 reproduces the earlier production exact check exactly.
- C3 power at rho .6 equals the proven cap min(1, alpha*n/L): 80% at L = 4, 40% at L = 8.
- C1 has no ceiling and comparable weak-signal power to Bonferroni, which is not size-valid under MA(2).

## Caveat carried into Stage 2

C1's iid-null point estimate climbs with L (5.5, 6.5, 7.0%); C1r shows the same (6.75, 7.25, 7.0%) on
the same 400 inputs. Block permutation of an i.i.d. source is an exact randomization test, so a true size
above 5% is not expected; a shared draw of these 400 inputs is the likely cause, but R = 400 cannot
separate 5% from 7%. PASS S1 therefore means "not killed", not "adopted". Stage 2 decides adoption.
