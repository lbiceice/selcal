# Real-task re-analysis — verdict (2026-09-22)

Protocol `protocol.md` (sha256 de375f22…, frozen before any SelCal run). Raw results `results.json`;
inputs, configs, records and HTML reports for A1/A2 are in this folder. Data: authors' deposit
(CC BY 4.0, SHA-256 matches), window 2006-06..2016-12, n = 127. Consistency check: `nino{k}[t]` equals
`nino0[t-k]` in all 635 checked cells (0 mismatches).

## Case A — Kerala dengue vs Niño 3.4 (Yacob et al. 2026, GeoHealth)

| Analysis | Lag | r | p | Verdict at .05 |
|---|---|---|---|---|
| A0 published practice (lag columns, 127 rows, textbook two-sided) | 2 | 0.356 | 4.1e-5 | significant |
| A1 SelCal, raw deposited series, lags 1-5, exact circular enumeration | 2 | 0.367 | **0.181** (E = 22, B = 126) | not significant |
| A1 comparators on the same series: best-lag textbook / Bonferroni x5 | 2 | 0.367 | 3.2e-5 / 1.6e-4 | significant |
| A2 SelCal, log1p-detrended-deseasonalised dengue vs SST anomaly | 5 | 0.261 | **0.370** (E = 46) | not significant |
| A2 comparators: best-lag textbook / Bonferroni x5 | 5 | 0.261 | 0.0037 / 0.018 | significant |

All SelCal runs: preflight EXECUTABLE (floor 5/127 = .039), exit 0 for validate/run/verify/report,
`verify --replay` MATCH.

### What this shows

- The published significance of the Niño 3.4–dengue cross-correlation is not supported once the test
  repeats the lag search in every surrogate and keeps each series' autocorrelation and seasonality:
  p = 0.18 on the deposited series, p = 0.37 after removing trend and shared seasonality.
- Common practice reports significance on every variant, including Bonferroni after deseasonalising
  (p = 0.018). This is the failure mode SelCal targets, observed on a real, sourced analysis.
- The deposited data put the best lag at 2 months, not the published 3 (r at lag 3 = 0.341); the
  deposited Niño column is absolute SST, whose seasonal cycle aligns with dengue's; the 2017 counts
  duplicate 2016. These are properties of the deposit, reported regardless of the results.

### What it does not show

- Not evidence that ENSO has no effect on dengue. Non-significance at n = 127 with strong
  autocorrelation can reflect low effective sample size; the test answers whether this correlation is
  distinguishable from what shifted, equally autocorrelated series produce.
- The raw-series circular null is approximate under a strong trend (declared assumption); A2 is the
  assumption-respecting variant and agrees.
- The paper's prediction models and other predictors are not evaluated.
- Lag 0 (scanned by the authors) is outside SelCal's lag set; SelCal's common support uses 122 pairs.
- This is an author-side re-analysis, not a user study: it shows a concrete analysis step SelCal changes
  (significance of a scanned lag) with verifiable evidence, not time saved or usability.

## Case B — US vs Australia influenza (Choi, Kim & Ahn 2019, PLOS ONE)

The published plan (+/-30-week scan, n = 418) is refused by the guard even in its most favourable
one-directional form: lags 1-30 give a floor of 30/418 = 0.072 > .05 (`REFUSE_NULL_STATES_TOO_FEW`).
A circular-shift test of that plan needs n >= 600, or at most 20 searched lags at n = 418. No data were
used or redistributed; this is plan arithmetic only and says nothing about whether the reported lead is
real.

## Before any public use

- Good scholarly practice: inform the corresponding authors of Case A (data-deposit issues and this
  re-analysis) before publication, and phrase the paper text as a re-analysis of one statement, not a
  refutation of their study. Author decision.
- An independent review of the interpretation has not happened yet.

## Correction note (2026-09-22, after checking the PLOS full text)

The protocol attributes n = 418 weeks to Choi, Kim & Ahn (2019). The article states a 2010-2018 weekly
analysis with lags of +/-30 weeks and Bonferroni correction, and Australia leading by 22 weeks
(r = 0.892 for total influenza), but it does not state 418. That length is the search agent's estimate of
the weekly window. The refusal does not depend on it: lags 1-30 need n >= 600, and nine full years of
weekly data (about 470 weeks) also fall short. The frozen protocol is left unchanged.

## Power at the observed autocorrelation (power_protocol.md, frozen before running; results_power.json)

AR(2) fits to the A2 series: SST anomaly phi = (1.91, -0.967), a near-unit-root quasi-periodic process
(ENSO-like cycle of about two years); dengue anomaly phi = (0.93, -0.13). With n = 127, lags 1-5 and
exact enumeration (re-implementation; 350 production cross-checks, 0 mismatches):

| true rho at lag 3 | 0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 |
|---|---|---|---|---|---|---|---|
| rejection rate (R = 1,000) | 5.3% | 6.8% | 11.8% | 18.7% | 34.2% | 51.4% | 70.4% |

No rho in the grid reaches 80% power. Interpretation (replaces a stronger reading of A1/A2): these data
carry too little independent information to decide whether a lagged Niño 3.4-dengue correlation of the
reported size exists. The published textbook p-value (about 4e-5) treated them as if they could; the
calibrated test shows they cannot. SelCal's non-significance is therefore "not supported by these data",
not "no association".
