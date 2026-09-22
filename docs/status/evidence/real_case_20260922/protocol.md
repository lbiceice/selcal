# Real-task re-analysis — frozen protocol (2026-09-22)

Frozen BEFORE any SelCal run on these data. The only prior look at the data was the search agent's
plain Pearson r per lag (to confirm the file matches the paper): max r = 0.356 at lag 2 on the
2006-06..2016-12 window. That look is disclosed here and cannot be undone.

## Case A (primary): Kerala monthly dengue vs Niño 3.4 SST

- Source analysis: Yacob S, Roxy MK, Vaisakh SB, Sreelakshmi PRN, Anish TS, Indu PS (2026). Climate
  Informed Dengue Prediction and Future Risk Under a Changing Monsoon Climate in Kerala, India.
  GeoHealth 10(9): e2026GH001893. doi 10.1029/2026GH001893 (VERIFIED via Crossref by the search agent).
- Claim re-examined (quoted): optimal lag of Niño 3.4 SST = 3 months, r = 0.38, "All correlations are
  statistically significant (p < 0.05)"; lag chosen as the maximum of a cross-correlation scan over the
  training set 2006–2016. No correction for autocorrelation or for the lag search is described.
- Data: authors' Zenodo deposit doi 10.5281/zenodo.20096919 (CC BY 4.0), file
  `Climate_dengue_data_Kerala_paper.csv`, SHA-256 91fac1a7f6c7b893c2065726f4b26aeb9301dd8aec7a6bbd8bcb68780074289b.
- Window: 2006-06 .. 2016-12 (the paper's cross-correlation window; also avoids the deposited 2017 rows,
  which duplicate 2016). n = 127.
- Series: source x = `nino0` (Niño 3.4 SST, °C, as deposited); target y = `dengue` (monthly cases).
- Consistency check before analysis (data only, no inference): `nino{k}[t] == nino0[t-k]` inside the
  window for k = 1..5; any mismatch is reported.

### Plans (all fixed now)

Common: lagged Pearson; candidate lags 1..5 (the authors scanned 0..5; SelCal lags start at 1, so lag 0
is excluded and this is stated); selection `max_absolute` (matches a two-sided "significant correlation"
claim); alpha .05; tie tolerance 0; null `circular_shift_exact_v1`, replicates n - 1 = 126;
root_seed 20260922. Run through the file workflow: validate -> run -> verify --replay -> report.
SelCal's common support uses t = 5..126 (122 pairs) for every lag; the authors' precomputed lag columns
used all 127 rows. This difference is reported.

- A0 (replication of the published practice): textbook two-sided Pearson p for lags 0..5 using the
  deposited `nino{k}` columns on 127 rows; report every r and p and the best lag.
- A1 (primary SelCal run): raw series as deposited (x = SST, y = counts).
- A2 (pre-declared assumption-respecting variant): y = log1p(counts), linear trend removed by OLS on the
  month index, then the 12 calendar-month means of the residuals removed; x = SST minus its 12
  calendar-month means (anomaly). Both computed on the window only. Same SelCal plan.
- A3 (common-practice comparators on the A1 and A2 series): best-lag textbook p over lags 1..5 and its
  Bonferroni x5 version.

### Interpretation rules (fixed now)

- A1 answers: does the published association between the deposited series survive a test that repeats
  the lag search and preserves each series' autocorrelation and seasonality?
- A2 answers the same after removing trend and shared seasonality, which the circular null otherwise
  keeps. If A1 is significant and A2 is not, the association is attributed to shared seasonality/trend
  and no ENSO-specific lag claim is supported by this test.
- Nothing here evaluates the paper's prediction models or dengue causation; only the cross-correlation
  significance statement. Deposit defects (2017 duplication, lag 2 vs 3 discrepancy, absolute SST) are
  reported whatever the results.

## Case B (guard demonstration, no data needed): US vs Australia influenza

- Source analysis: Choi, Kim & Ahn (2019), PLOS ONE, doi 10.1371/journal.pone.0220423 (VERIFIED by the
  search agent): weekly series, lags scanned over +/-30 weeks with Bonferroni; reported Australia leading
  the US by 22 weeks, r = 0.892; n = 418 weeks.
- Check: `attainability` for n = 418 with lags 1..30 in the reported lead direction (the most favourable
  one-directional representation of a +/-30 scan), exact null. Report status, floor, the minimum n that
  would pass (L/alpha) and the largest L that passes at n = 418. No FluNet data are redistributed.
