# remedy-confirm-v1, Stage 2 — DRAFT (not frozen, 2026-09-20)

DRAFT only. It is frozen (own sha256 file) after the Stage 1 verdict is written, and only the arms that
Stage 1 leaves alive are carried over. Nothing here licenses a run.

## Why Stage 2 is required even if Stage 1 passes

The sealed null cells have R = 400, which cannot separate a true size of 6-7% from 5%. Stage 1 can
therefore reject block shuffle but cannot adopt it. Stage 2 adds resolution and two conditions the sealed
data does not contain.

## Generation (new data, prospectively frozen seeds)

| Cell | n | Definition | Budget |
|---|---|---|---|
| S2-iid | 64, 256 | x, y independent standard normal | 4,000 each |
| S2-ma2 | 64, 256 | both series circular MA(2), weights 1, .6, .3 / sqrt(1.45), as in the sealed study | 4,000 each |
| S2-ar1 | 64, 256 | both series AR(1), phi = .6, burn-in 500, NOT circular; the honest stress case for a circular null | 4,000 each |
| S2-alt | 64, 256 | y_t = rho * x_{t-L} + sqrt(1-rho^2) * e_t, rho .3 and .6, signal at the LAST searched lag | 2,000 each |

Seeds: `int(sha256("SelCal/remedy-confirm-v1|stage2|{cell}|{n}|{index}|{role}").hexdigest()[:16], 16)`,
PCG64. Inputs are written to disk and digested before any arm runs.

## Arms and L

L in {2, 8}. Arms carried over from Stage 1 (survivors only) plus C0 (exact enumeration) as the
reference. Production runs every arm it can run; re-implementation arms are labelled as such.

## Endpoints and decision rules (to fix at freeze time)

- Size per arm x cell x n x L with 95% Clopper-Pearson. At R = 4,000 the half-width near 5% is about
  0.7 points, which does separate 5% from 6.5%.
- ADOPT a fallback only if its size CP upper bound is <= .065 in every null cell at both n, including
  AR(1), and its rho .6 power at L = 8, n = 64 is >= 80%.
- REFUSE-ONLY outcome: if no fallback qualifies, the guard keeps refusing unattainable plans and the
  documentation states the limitation, with randomized ties offered as the exact-but-capped option.
- C0's AR(1) size is reported. A circular null on non-circular data is expected to be approximate; this
  is a limitation to publish, not a pass/fail gate.

## Rules

Frozen before generation. No arm, cell, n, L or seed may be added or dropped after seeing results.
Adverse results are reported. Any production-code change found necessary during Stage 2 stops Stage 2
until it has its own RED->GREEN receipt and the affected evidence is re-verified.
