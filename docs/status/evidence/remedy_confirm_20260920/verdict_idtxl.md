# IDTxl 1.6.0 comparator — verdict (2026-09-22)

Protocol `protocol_idtxl.md` (sha256 61066622…, frozen before the run). Raw chunks `idtxl_results/`
(264/264, 0 failed analyses); run metadata `idtxl_run_meta.json`; analysis `results_idtxl_analysis.json`.
Descriptive comparison of the tool as a user runs it; no adopt/refuse decision depends on it.

## I1 — Gaussian estimator, default single-series path (analytic independent-sample surrogates)

Identical Stage 2 inputs, R = 4,000 per null cell.

| Null | n = 64, L = 2 / 8 | n = 256, L = 2 / 8 | SelCal exact enumeration (same inputs) |
|---|---|---|---|
| i.i.d. | 5.6 / 5.6% | 4.5 / 5.0% | 3.0-4.2% |
| MA(2) | **13.8 / 18.8%** | **11.8 / 16.9%** | 3.2-4.1% |
| AR(1) | **17.4 / 23.4%** | **17.0 / 23.1%** | 3.8-4.4% |

Power (R = 1,000): comparable to SelCal where SelCal's plan is attainable (rho .6: 99-100%); at n = 64,
L = 8 I1 detects 99% at rho .6 where SelCal's exact plan is refused (0%). I1's power is not usable under
autocorrelation because its size is 3-5 times nominal there.

## I2 — KSG estimator with IDTxl's circular shift (`perm_type="circular"`), n = 64, R = 1,000

| Null | L = 2 | L = 8 |
|---|---|---|
| i.i.d. | 5.2% | 5.4% |
| MA(2) | 5.3% | 6.1% (CP upper 7.8%) |
| AR(1) | 4.1% | 4.6% |

| Power | L = 2 | L = 8 |
|---|---|---|
| rho .3 | 12.9% (SelCal exact 52.8%, block 61.7%) | 9.6% (SelCal exact 0%, block 42.0%) |
| rho .6 | 74.2% (SelCal exact 99.5%, block 99.8%) | 44.4% (SelCal exact 0%, block 99.3%) |

## Findings to carry into the paper, including the adverse ones

1. IDTxl's default Gaussian path inflates false links 3-5x under autocorrelation on these inputs. This is
   the path a user gets with `JidtGaussianCMI` and one replication; IDTxl's own circular-shift path (I2)
   is approximately calibrated. The claim is about that path, not about IDTxl in general.
2. Adverse for SelCal: at n = 64, L = 8 IDTxl's circular path keeps power (44% at rho .6) where SelCal's
   exact plan cannot reject. IDTxl shifts each candidate independently, so it has no lag-collision floor;
   the cost is that its surrogate maximum ignores the dependence between candidates. The difference is
   confounded with the estimator (KSG vs Pearson) and must be reported as such, not as a SelCal advantage.
3. Where both are attainable (L = 2), SelCal's exact enumeration is far more powerful than IDTxl's KSG
   circular path on these Gaussian linear signals (99.5% vs 74.2% at rho .6). The estimator is the likely
   reason; this is not a like-for-like algorithm comparison.
4. Gaussian MI is two-sided in r; SelCal's plan is one-sided. Null-cell rates compare each tool's own false
   link rate.

## Environment note

IDTxl 1.6.0 needed NumPy < 2 (numpy 1.26.4, scipy 1.13.1), a portable Temurin 21 JRE for JIDT, and direct
estimator classes (string lookup imports unrelated optional modules). Versions are in
`idtxl_run_meta.json`.
