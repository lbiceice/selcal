# SoftwareX figures (Figs. 1-5)

Rendered 2026-09-22. Each script reads the evidence JSON directly (via `_style.load_cells`); no numbers are
hand-copied. The only analytic quantities are the lag-collision grid in Fig. 2a and the floor L/n in Fig. 2b and in
the "refused" labels (the guard rule is L/n > alpha, alpha = .05). Fig. 5 reads `results.json` of the real-case
re-analysis and, for panel (a), the authors' deposited CSV (window 2006-06..2016-12, checksum-checked). Fig. 1 is a
schematic; its names and exit codes follow the source files listed below.

## Inputs (SHA-256 at render time)

| File | SHA-256 |
|---|---|
| `docs/status/evidence/remedy_confirm_20260920/results_stage2_analysis.json` | `ffd1d8c84e57cb5341ea94416c22ed1acc2c2df5154eb7b41fc86816ad82b90f` |
| `docs/status/evidence/remedy_confirm_20260920/results_idtxl_analysis.json` | `d0074e144ef16aa723f5bcab69ffcd3cb26d899db541a13068b4dfb5630c00dd` |

Check: `shasum -a 256 docs/status/evidence/remedy_confirm_20260920/results_{stage2,idtxl}_analysis.json`

Fig. 5 (real case; the script refuses to run if the deposit checksum differs):

| File | SHA-256 |
|---|---|
| `docs/status/evidence/real_case_20260922/results.json` | `7b0aca1c817456853669fe7adcbce73057aeda676b60a940506a65199497989d` |
| `docs/status/evidence/real_case_20260922/data/Climate_dengue_data_Kerala_paper.csv` | `91fac1a7f6c7b893c2065726f4b26aeb9301dd8aec7a6bbd8bcb68780074289b` |

Fig. 1 is a schematic with no data input. Its names were checked against these sources at render time:

| File | SHA-256 |
|---|---|
| `src/selcal/cli.py` | `3dc1eda90492b6a30d064f3c9eb594a4003f14a6191d043bdaeb5ebcc6bccb36` |
| `src/selcal/workflow.py` | `4d8642f975ca5e8f7f593f5da5ac64bf356f6b3251013f61bbf4a802aabeeebb` |
| `src/selcal/resolution_v2.py` | `d9c89b728dba95882c9572ca162508f2e14d828d368f431a02908532ff7c8b56` |
| `src/selcal/calibration_v2.py` | `d93c527645fbb0d43bd9dec7301b9d03337a0a4e412af767952f6ae55a03187b` |
| `src/selcal/contracts_v2.py` | `136eb961bdc6ecf34f1381676c59b5919a540cdf65136ad0c6de9eecb04ccae9` |
| `src/selcal/workflow_store.py` | `d802e7fcfd5bbfbd76fc9319552b5995205016d6c89c8c722ae58e89df954393` |

## Environment

Python 3.13.12, matplotlib 3.11.1, numpy 2.5.2 (scratchpad env, not the project `.venv`). Font: Arial
(falls back to Helvetica / DejaVu Sans). PDFs embed TrueType (fonttype 42); PNGs are 300 dpi.

## Command (from the repository root)

```sh
for f in fig1_architecture fig2_guard fig3_size fig4_power fig5_real_case; do
  PYTHONDONTWRITEBYTECODE=1 python docs/manuscript/figures/$f.py
done
```

## Files

- `_style.py` (refused-plan label is horizontal, right of the marker; height set per figure): shared rcParams, method colours and markers, JSON loaders, grouped dot-and-interval panel.
- `fig1_architecture.py` -> `fig1_architecture.pdf`, `fig1_architecture.png` (double column, 17.5 x 8.9 cm; schematic)
- `fig2_guard.py` -> `fig2_guard.pdf`, `fig2_guard.png` (double column, 17.5 x 11 cm)
- `fig3_size.py` -> `fig3_size.pdf`, `fig3_size.png` (double column, 17.5 x 9 cm plus legend)
- `fig4_power.py` -> `fig4_power.pdf`, `fig4_power.png` (double column, 17.5 x 9 cm plus legend)
- `fig5_real_case.py` -> `fig5_real_case.pdf`, `fig5_real_case.png` (double column, 17.5 x 8.2 cm)

Colours: categorical slots 1-4 of the dataviz reference palette in fixed order (SelCal exact blue, Bonferroni
orange, IDTxl Gaussian aqua, IDTxl KSG yellow) plus neutral grey hollow circles for block shuffle; checked with
`validate_palette.js` (light, adjacent pairs: pass, worst CVD dE 9.1). Each method also has its own marker shape,
so identity never rests on colour alone (needed for print and for the three slots below 3:1 contrast on white).
Fig. 2b uses an ordinal one-hue blue ramp for L. Fig. 5 keeps SelCal blue and Bonferroni orange and adds
dataviz slot 7 (violet) for uncorrected textbook p, with a hollow diamond for the published-practice replication and
a filled triangle for best-lag textbook p (violet/orange/blue, all pairs: pass, worst CVD dE 13.0, normal-vision
dE 16.3, all >= 3:1). Fig. 1 uses the SelCal blue for the calibration core and the dataviz status "critical" red
only for exit-code badges, each carrying its code as text (filled = exit 2, outlined = exit 7).

## Captions (drafts)

**Fig. 1.** SelCal architecture and data flow. A series file (CSV or NPZ) and a JSON plan are checked by
`selcal validate`, which answers three separate questions: is the input valid, is the plan executable (resource
budget; smallest attainable p-value at most alpha), and which scientific assumptions does the plan declare (these
are reported, not verified). `selcal run` repeats this preflight, resolves the plan to registered components
(`resolve_plan_v2`) and calibrates: the observed data are scanned over every candidate lag and the maximum is
selected; each of B null replicates is transformed, scanned over every lag and reselected, so the selection is
repeated inside the null; p = (1 + E)/(B + 1). The verified result is saved with the input, the plan and the
software identity in one SQLite record, which `selcal verify`, `verify --replay` (full recomputation) and
`selcal report` read back. The guard stops before calibration with exit code 2 (invalid input, or plan not
executable; a run of an unattainable plan requires `--allow-unattainable-plan`). A failure during null binding,
the observed scan or any replicate is kept in the result, which is then NOT_EVALUABLE (exit code 7) and carries no
p-value.

**Fig. 5.** Re-analysis of one cross-correlation statement from Yacob et al. (2026, GeoHealth), using the
authors' deposited data (Zenodo, CC BY 4.0), window 2006-06 to 2016-12 (n = 127). (a) The deposited Niño 3.4 SST
(absolute, not anomaly) and monthly dengue counts share a seasonal cycle and trend. (b) p-value for the best-lag
correlation under four procedures; labels give the selected lag and p, and "(edge)" marks lag 5, the upper end of
the searched range. The deseasonalised analysis (A2) is shown first. Published practice (lags 0-5, textbook two-sided
Pearson p on the deposited lag columns) is defined only for the raw series. The other procedures use lags 1-5 on
122 common-support pairs: textbook p at the best lag, Bonferroni x5, and SelCal with exact circular-shift
enumeration (B = 126, selection repeated in every null state; preflight floor 5/127 = .039). A1: series as deposited
(the protocol's primary SelCal run); A2: log1p counts detrended and deseasonalised, SST as monthly anomaly (the
pre-declared assumption-respecting variant; both fixed in a protocol frozen before any SelCal run). Every conventional procedure is below alpha = .05 on both series; SelCal gives p = .18 (A1) and
.37 (A2). SelCal's lag set excludes lag 0, which the authors scanned. Non-significance here does not show that
ENSO has no effect on dengue: at n = 127 with strong autocorrelation the test has little power, and the
prediction models of the source study are not evaluated.

**Fig. 2.** Why SelCal refuses some circular-shift plans. (a) With lags 1..L searched, the circular shift
s = c* - c (mod n) maps searched lag c onto the selected lag c*, so L of the n shift states reproduce the observed
maximum (n = 16, L = 4, c* = 3 shown). (b) The smallest attainable p-value is therefore L/n; the shaded region,
where L/n > alpha = .05, is where the guard refuses the plan (dots mark n = L/alpha). (c) Measured rejection rate
of SelCal's exact enumeration at rho = 0.6 (R = 1,000 per cell; bars with 95% Clopper-Pearson intervals). At
n = 64, L = 8 the floor is 8/64 = .125, so the plan cannot reject and is refused; at n = 256, L = 8 it is attainable.

**Fig. 3.** False-positive rate under three null processes (i.i.d.; circular MA(2); non-circular AR(1)) with 95%
Clopper-Pearson intervals (R = 4,000 per cell; IDTxl KSG + circular shift R = 1,000, n = 64 only). Dashed line:
nominal 5%. SelCal exact enumeration at n = 64, L = 8 records no rejections because the guard refuses that plan
(floor 8/64 > .05); this is not evidence of calibration. Block shuffle was tested as a fallback and not adopted
(pre-registered size criterion missed in 3 of 12 rows). The IDTxl result concerns the default Gaussian
estimator path of IDTxl 1.6.0 (analytic surrogates) only; IDTxl's own circular-shift path (KSG) is approximately
calibrated.

**Fig. 4.** Rejection rate under the lagged-coupling alternative (independent noise, signal at the last searched
lag L; rho = 0.3 and 0.6; R = 1,000 per cell; 95% Clopper-Pearson intervals). SelCal exact enumeration is refused at n = 64, L = 8 and records 0% by design; where
refused, IDTxl's circular KSG path keeps some power (no lag-collision floor), a difference confounded with its
estimator. Power of Bonferroni and IDTxl's default Gaussian path is not usable under autocorrelation because their
size exceeds nominal there (Fig. 3). Block shuffle: tested, not adopted.
