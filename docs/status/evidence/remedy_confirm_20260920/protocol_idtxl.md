# Nearest-tool comparator: IDTxl 1.6.0 on the Stage 2 inputs — frozen protocol (2026-09-22)

Frozen before any IDTxl comparator run. Descriptive comparison of a tool as a user runs it; no
adopt/refuse decision depends on it. Internal evidence, not a manuscript.

## Tool identity and environment

- IDTxl v1.6.0 installed from `git+https://github.com/pwollstadt/IDTxl@v1.6.0` (not on PyPI).
- IDTxl 1.6.0 calls `np.issubclass_`, removed in NumPy 2, so its environment pins numpy 1.26.4,
  scipy 1.13.1, statsmodels 0.14.2, h5py < 3.12, setuptools < 81, jpype1, mpmath; JIDT runs on a portable
  Eclipse Temurin 21 JRE placed in the session scratchpad (no system install). SelCal arms keep their own
  environment (numpy 2.4.6). The exact versions are written into the results file.
- The estimator class is passed directly (`JidtGaussianCMI`, `JidtKraskovCMI`), because IDTxl's string
  lookup imports every estimator module and fails on unrelated optional dependencies.

## What IDTxl actually does here (read from source before running)

`BivariateMI.analyse_single_target` with one replication and `permute_in_time=True`:
(1) greedy inclusion of source candidates with `max_statistic` (surrogates generated separately for each
remaining candidate, maximum taken across candidates), (2) pruning with `min_statistic`, (3) omnibus and
sequential max statistics. With `JidtGaussianCMI` (an analytic-null estimator) and `permute_in_time=True`,
`_create_surrogate_table` draws surrogates ANALYTICALLY under an independent-samples null; `perm_type` is
not used on this path. With `JidtKraskovCMI` the surrogates are real permutations of the candidate
realisations, and `perm_type="circular"` shifts them by a uniform 1..max_shift.

## Arms

| Arm | Estimator / surrogates | Inputs |
|---|---|---|
| I1 | `JidtGaussianCMI`, `permute_in_time=True` (analytic surrogates) | every Stage 2 input, n 64 and 256, L 2 and 8 |
| I2 | `JidtKraskovCMI` (defaults), `permute_in_time=True`, `perm_type="circular"`, `max_shift = n - L - 1` | n = 64 only, first 1,000 inputs of each null cell and all 1,000 of each alternative cell, L 2 and 8 |

Common settings: `min_lag_sources=1`, `max_lag_sources=L`, `n_perm_max_stat = n_perm_min_stat =
n_perm_omnibus = n_perm_max_seq = 199`, all alphas at IDTxl defaults (.05), `normalise=False`,
`verbose=False`. Decision = IDTxl declares a link (`selected_vars_sources` non-empty).
Seed: `np.random.seed(int(sha256("SelCal/remedy-confirm-v1|idtxl|{arm}|{cell}|{n}|{rho}|{L}|{index}").hexdigest()[:8], 16))`
before each analysis. Any exception is recorded as a failed run, counted as no link, and listed.

## Endpoints

Per arm x cell x n x L: link rate with 95% Clopper-Pearson; in alternative cells, exact McNemar against
SelCal C1 and C0 on the same inputs (paired by index).

## Interpretation limits fixed now

- Gaussian MI is two-sided in r; SelCal's plan is one-sided max_upper. Null-cell rates compare each tool's
  own false-link rate; alternative-cell power compares tools, not identical hypotheses.
- IDTxl's procedure has several sequential tests; its link decision is not a single max-statistic p-value.
- I2 uses a different estimator (KSG), so it is not Pearson-matched; it is the IDTxl route that preserves
  autocorrelation through circular shifts.
- Nothing here is a claim about IDTxl in general or other settings.
