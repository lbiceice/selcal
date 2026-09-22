# P3 / SelCal: common-practice comparator arms — frozen protocol

Written 2026-09-19 (Asia/Shanghai) BEFORE any comparator computation. Internal evidence, not a manuscript.

## Why this study

The 2026-09-10 value replay compared SelCal with a *correct* author script and found zero coverage
increment. That comparison cannot show value by construction: a correct script is correct.
The SoftwareX question is the increment over what analysts **commonly do** when they search lags and
report the winner. This study measures that on the sealed 1,200 study inputs, with no new data, no
production-code change and no change to the sealed SelCal results.

## Fixed inputs and plan (identical to the sealed study)

- Inputs: `../bounded_study_execution_20260909/study_v1/inputs/*.json` (1,200 files; float-hex decoded exactly).
- Candidates {1,2}; common target window t = 2..63 (62 pairs); statistic r_lag = Pearson(x[t-lag], y[t]).
- Selection max_upper (largest r, ties -> smallest lag); one-sided upper; alpha = .05; reject iff p <= .05.

## Arms

| Arm | What it represents | p-value |
|---|---|---|
| A0 SELCAL | sealed production result (read only) | sealed `p`, `reject_null` |
| A1 NAIVE_PARAM | pick best lag, report its textbook Pearson p | one-sided t-test p at selected lag (scipy.stats.pearsonr, alternative="greater") |
| A2 BONF_PARAM | A1 plus Bonferroni over the searched lags | min(1, 2 * A1 p) |
| A3 FIXED_CIRC | correct circular-shift null but lag fixed after selection (no reselection) | circular shift of source, 64 states incl. identity, uniform with replacement, B=199; r at selected lag only; p=(1+E)/200, E=#{null >= obs} |
| A4 SCIPY_SHUFFLE | full reselection but SciPy's default i.i.d. permutation null | scipy.stats.permutation_test((x,y), max_lag_r, permutation_type="pairings", n_resamples=199, alternative="greater") |
| A5 CIRC_RESEL | independent re-implementation of SelCal's procedure (circular + reselection), fresh draws | as A3 but statistic = max over lags in every replicate |

Randomness for A3/A4/A5: seed = int(sha256("SelCal/comparator-arms-v1|{cell}|{index}|{arm}").hexdigest()[:16], 16), numpy PCG64.
Environment: isolated venv, Python 3.11.12, numpy 2.4.6, scipy 1.16.2 (not the project environment).

## Pre-computation gate

For all 1,200 inputs the re-implemented observed max statistic must match SelCal's sealed
`decision_statistic` within 64 ulp and the selected lag must match. Any mismatch stops the study
before arm comparison.

## Endpoints and decision rules (fixed now)

- Per arm x cell: K/R, rejection rate, pointwise 95% Clopper–Pearson interval.
- D1 miscalibration: in a null cell, an arm is MISCALIBRATED if its CP lower bound > .05.
- D2 paired power vs A2 (the strongest simple alternative) in each alternative cell: exact two-sided McNemar on discordant pairs, A0 vs A2.
- D3 A5 is a sanity arm: its null-cell rates should be consistent with A0 (CP intervals overlap). If not, stop and diagnose before interpreting anything.

Interpretation fixed in advance:
- If A1/A2/A4 are MISCALIBRATED in the circular MA(2) null cell and A0 is not: supports the claim
  "SelCal's plan prevents the autocorrelation false-positive of common parametric / shuffle practice".
- If A3 is MISCALIBRATED in a null cell: supports "reselection inside every surrogate is necessary".
- If no common-practice arm is MISCALIBRATED and A0 has no power gain over A2: the common-practice
  increment is NOT supported at this plan (L=2, n=64); record it and do not search for a favourable cell.
- In every case the increment is against common practice, not against a correct script; A5 existing
  shows a competent analyst can reproduce the procedure, so the software claim remains about packaging,
  plan freezing and retained evidence — not a new method.

## Exploratory E1 (labelled exploratory, never a primary result)

Selection inflation grows with the number of searched lags, and L=2 is small. On the SAME null-cell
series only, repeat A1, A2, A3, A5 (re-implementation, not SelCal production) for candidate sets
{1..L}, L in {2, 4, 8}, window t = L..63. Report rates only; no decision rule, no claim that SelCal
production was executed at L=4/8.
