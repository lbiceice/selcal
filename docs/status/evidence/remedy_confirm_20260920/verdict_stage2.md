# Stage 2 verdict (2026-09-22)

Protocol `protocol_stage2.md` (sha256 a56da079…, frozen before data generation). Inputs digested in
`stage2_inputs/manifest.json`. Production: 448 chunks, 0 non-complete runs, every result passed
`verify_calibration_result`. Analysis: `results_stage2_analysis.json`.

## Decision: REFUSE_ONLY (block shuffle is NOT adopted as the fallback)

- A2 met: C1 power at rho .6, L = 8, n = 64 = 99.3% (>= 80%).
- A1 failed in 3 of 12 rows (CP upper must be <= .065):

| Row | rate | CP95 upper |
|---|---|---|
| C1, MA(2), L = 2, n = 64 | 5.78% | 6.54% |
| C1, AR(1), L = 2, n = 64 | 6.02% | 6.81% |
| C1, AR(1), L = 8, n = 64 | 5.92% | 6.70% |

The miss is small and confined to n = 64 under autocorrelation; the rule was fixed in advance and is
applied as written. The guard therefore keeps refusing unattainable circular plans; the documentation
states the limitation; randomized ties stay the only exact option, with its proven cap.

## What Stage 2 established (R = 4,000 per null cell)

| Arm | iid | MA(2) | AR(1), non-circular | notes |
|---|---|---|---|---|
| C0 exact enumeration | 3.0-4.2% | 3.2-4.1% | 3.8-4.4% | 0% at n = 64, L = 8 (refused plan, floor 8/64) |
| C1 block shuffle | 4.4-5.4% | 5.0-5.8% | 5.2-6.0% | liberal by about one point at n = 64 under autocorrelation |
| C2 Bonferroni | 4.4-5.2% | **8.8-12.7%** | **12.0-15.2%** | false positives more than double under autocorrelation |

- C0 stays conservative even for non-circular AR(1), where circular exchangeability does not hold.
- The guard's prediction holds: at n = 256, L = 8 (floor 8/256 = .031) C0 is attainable, with power 96.7%
  (rho .3) and 100% (rho .6); at n = 64, L = 8 it is 0%.
- The Stage 1 caveat is resolved: with R = 4,000, C1's iid size is 4.4-5.4%, so the 7% seen on the sealed
  400 inputs was sampling variation.
- C1 vs Bonferroni at rho .3, n = 64: Bonferroni rejects more (L = 2: 75 vs 29 discordant, p = 7e-6;
  L = 8: 37 vs 19, p = .022), but Bonferroni is not size-valid under autocorrelation, so that power is not
  usable there. At n = 256 the two are indistinguishable.

## Consequences for the software and the paper

1. Default recommendation: `circular_shift_exact_v1` when n >= L/alpha (guard PASS). It is calibrated in
   every null tested, including non-circular AR(1), and has full power at n = 256.
2. When the guard refuses (n < L/alpha): no calibrated fallback is offered. Options to state honestly:
   collect a longer series, search fewer lags, or accept randomized ties with power <= alpha*n/L.
3. Block shuffle remains available as an ordinary null but is not recommended as a remedy; if revisited,
   it needs a new frozen study (e.g. longer blocks at n = 64), not a relaxed threshold.
