# Comparator arms + exploratory E1/E2 — results note (2026-09-19)

Protocol `protocol.md` (sha256 986769a3…), Amendment 1 (gate criterion; disclosed), E2 plan registered
before E2 ran. Raw: `results.json`, `results_E2.json`. Isolated env: Python 3.11.12, numpy 2.4.6,
scipy 1.16.2. No SelCal module imported, no production code changed, sealed study untouched.

## Primary (pre-registered, sealed 1,200 inputs, L=2, n=64)

| Arm | iid null | circular MA(2) null | rho .3 | rho .6 |
|---|---|---|---|---|
| A0 SelCal (sealed) | 4.00% | 3.75% | 57.0% | 91.0% |
| A1 best lag + textbook p | **10.0% MISCAL** | **13.0% MISCAL** | 80.5% | 100% |
| A2 + Bonferroni | 6.0% | **8.5% MISCAL** | 69.5% | 100% |
| A3 circular null, lag fixed | **10.25% MISCAL** | 6.5% | 74.0% | 100% |
| A4 SciPy shuffle, reselection | 6.0% | **8.75% MISCAL** | 68.5% | 100% |
| A5 re-implementation of A0 | 4.0% | 2.5% | 57.5% | 85.5% |

D1: every common-practice arm is miscalibrated in at least one null cell; A0 in none. D3 sanity passes.
D2 (paired vs A2): A2 rejects more in both alternative cells (rho .3: 29 vs 4 discordant, p=1.1e-5;
rho .6: 18 vs 0, p=7.6e-6). CORRECTED after audit: the alternative cells use i.i.d.-type noise where A2 is
size-valid, so this IS a like-for-like power loss for SelCal; most of it comes from the finite-B / 64-state
floor below. A4 note: SciPy "pairings" shuffles both series independently (still an i.i.d. null).

## Exploratory (post hoc, not confirmatory)

E1/E2 show a structural power ceiling in the current circular-shift default (min_shift=1, 64 states incl.
identity) when lags are searched. CORRECTED after adversarial audit: small positive AND small negative
shifts collide, so exactly L states always reproduce the observed maximum, whatever lag is selected.
Exact floor: p >= L/n. Exact enumeration can reject at alpha only if n >= L/alpha (n >= 20L at .05).
With B=199 Monte Carlo draws the power caps are about 90.4% (L=2), 19.8% (L=4), ~0% (L=8).

| L | null inputs that can never reject (exact, audited) | A5 power rho .6 | Bonferroni power rho .6 |
|---|---|---|---|
| 2 | 0/800 | 88% | 100% |
| 4 | 800/800 | 20% | 100% |
| 8 | 800/800 | 0% | 100% |

(The first version reported 418/609 because run_exploratory_E2.py checked only states 0..L and missed
negative shifts.) Sealed rho .6 had 18 nonrejections; 17 sit at the 2/64 floor, #141 does not.

Naive fix rejected: sampling shifts only from [L, n-L] restores power but breaks the group structure and
inflates size (audited fresh-seed size 6.1-6.4% at L=2, ~13% at L=8). Mechanism: when the observed max is
the global max (prob. L/n) its tied neighbours are exactly the excluded shifts. SelCal's OWN min_shift=L
option has the same defect (13.2% size at L=8, audit). A valid remedy must keep a group-valid null.

## Consequences

1. The value claim now has evidence: selection-aware, autocorrelation-preserving calibration is the
   only arm that controls size in both null cells. It is a claim vs common practice, not vs a correct script.
2. SelCal must not ship with the silent power ceiling. Candidate remedy (needs its own frozen
   confirmation): a plan-time attainable-p check that computes the minimum attainable p for (n, L, null)
   before running and refuses or flags plans that cannot reach alpha; document n >= L/alpha guidance, and flag or remove the invalid min_shift > 1 usage.
3. The manuscript must report the power cost and ceiling as limitations, not hide them.
