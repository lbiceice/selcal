# Power check for the Kerala re-analysis (A2 setting) — frozen protocol (2026-09-22)

Written after the A1/A2 results and the draft-v1 review (which asked for power at the observed
autocorrelation), BEFORE running any power simulation. Descriptive: it qualifies the interpretation of a
non-significant result; it cannot change A1/A2.

## Question

With series as autocorrelated as the A2 (log-detrended-deseasonalised dengue, SST anomaly) series, n = 127,
lags 1-5 declared, exact circular enumeration, max_absolute, alpha .05: what is the rejection rate as a
function of the true lagged correlation rho, and what rho gives 80% power?

## Generation

- Fit AR(2) by Yule-Walker to the A2 source x (SST anomaly) and to the A2 target y (dengue anomaly), each
  standardised; record coefficients and innovation variances.
- For each replicate: x from the fitted source AR(2) (burn-in 500, then 127 values, standardised);
  w from the fitted target AR(2) (independent, standardised);
  y_t = rho * x_{t-3} + sqrt(1 - rho^2) * w_t (x drawn with 3 extra leading values; lag 3 = the
  published lag). rho in {0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6}; R = 1,000 per rho.
- Seeds: PCG64, int(sha256("SelCal/kerala-power-v1|{rho}|{index}|{role}")[:16], 16).

## Test

Exact circular enumeration with full reselection over lags 1-5, statistic max |Pearson(x[t-k], y[t])|
on t = 5..126, p = #{s: T_s >= T_0}/127, reject iff p <= .05 (float arithmetic as SelCal). Implemented as
an independent NumPy re-implementation of `circular_shift_exact_v1`, whose equivalence to production was
established on 1,200 sealed inputs (0 mismatches). A random 50 replicates per rho are also run through the
production API and must match the re-implementation's p exactly; any mismatch stops the analysis.

## Report

Rejection rate with 95% Clopper-Pearson per rho; smallest rho in the grid with rate >= 80%; the rho = 0
rate as the size under this autocorrelation. Compare with the observed |r| in A2 (0.261) and A1 (0.367)
only as context; no post hoc test.
