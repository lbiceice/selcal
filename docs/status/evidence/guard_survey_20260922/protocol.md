# Guard survey protocol: L/n in published lag-scan analyses

Frozen: 2026-09-22 09:51 UTC, before any search was run. Any deviation made after searching
is recorded in results.md under "Deviations"; this file is not edited afterwards.

## Question

Among published empirical lead-lag analyses that pick a lag by scanning a stated range with
cross-correlation or lagged correlation, what share would a plan-time guard that refuses
L/n > alpha (alpha = 0.05, i.e. requires n >= 20L) have:

- (a) refused: L/n > 0.05
- (b) put near the floor: 0.025 < L/n <= 0.05
- (c) allowed with room: L/n <= 0.025

## Definitions

- n: number of time points in the analysed window of one series (per-series length; for a
  panel of regions each with T points, n = T). If only start/end dates and frequency are
  given, n is computed and marked `derived`.
- K: the maximum absolute lag searched.
- L (primary, favourable): number of nonzero lags in one direction = K. For a one-sided
  scan 0..K, L = K. For a symmetric scan -K..+K, L = K.
- Full scan count (secondary): number of lags actually evaluated: 2K+1 for -K..+K, K+1 for
  0..K (K if lag 0 is excluded). Classification is reported under both L and the full count.
- Significance claim: the paper says the correlation at the selected / peak lag is
  significant, reports a p-value or CI for it, or relies on confidence bands to call it
  significant.
- Correction: any of multiple-testing adjustment across lags (Bonferroni, FDR, max-statistic),
  surrogate / permutation / block-bootstrap null that preserves autocorrelation,
  prewhitening (ARIMA filtering before CCF), effective-degrees-of-freedom adjustment.
  "Uncorrected claim" = significance claim with none of these.

## Source and search

Database: Europe PMC REST API
`https://www.ebi.ac.uk/europepmc/webservices/rest/search`, `format=json`,
`resultType=core`, `pageSize=100`, default sort (relevance). Open-access full text via
`https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML`.

Common filters appended to every query:
`AND OPEN_ACCESS:y AND HAS_FT:y AND PUB_YEAR:[2019 TO 2026] AND SRC:MED`

Three field queries (exact strings, before the common filters):

- EPI (epidemiology):
  `(ABSTRACT:"cross-correlation" OR ABSTRACT:"cross correlation") AND (ABSTRACT:"lag" OR ABSTRACT:"time lag" OR ABSTRACT:"lagged") AND (ABSTRACT:dengue OR ABSTRACT:malaria OR ABSTRACT:influenza)`
- CLIM (climate-ecology):
  `(ABSTRACT:"cross-correlation" OR ABSTRACT:"cross correlation") AND (ABSTRACT:"lag" OR ABSTRACT:"time lag" OR ABSTRACT:"lagged") AND (ABSTRACT:ENSO OR ABSTRACT:"sea surface temperature" OR ABSTRACT:rainfall OR ABSTRACT:precipitation) AND (ABSTRACT:vegetation OR ABSTRACT:NDVI OR ABSTRACT:ecolog* OR ABSTRACT:species OR ABSTRACT:drought OR ABSTRACT:streamflow OR ABSTRACT:groundwater)`
- FISH (fisheries):
  `(ABSTRACT:"cross-correlation" OR ABSTRACT:"cross correlation" OR ABSTRACT:"lagged correlation") AND (ABSTRACT:fisheries OR ABSTRACT:fishery OR ABSTRACT:recruitment OR ABSTRACT:catch OR ABSTRACT:"fish stock")`

If a query returns fewer than 20 hits, the fallback is the same query with `ABSTRACT:` removed
from the topic block (i.e. searched across full text); the fallback is logged.

The UTC timestamp and hit count of every query are logged in `queries.log`.

## Screening order and target sample

Records are screened in API relevance order, one field at a time. Target: the first 14
eligible records per field (42 total, at least 40), with a screening cap of 80 records per
field. If a field reaches the cap first, the shortfall is reported and not back-filled from
other fields.

## Inclusion

1. Primary empirical analysis of at least two observed time series (exposure/driver and
   response), in the original paper.
2. A lag is chosen or reported by scanning a stated range of lags with cross-correlation or
   lagged (Pearson/Spearman) correlation. The scan must be of the correlation itself; a
   distributed-lag model fitted at a fixed lag set counts only if lags are also screened by
   correlation.
3. n (or dates + frequency) and the lag range (K) can be recovered from the full text,
   tables or figure captions available in the Europe PMC full-text XML.

## Exclusion (reason logged)

- E1 no lag scan by correlation (e.g. only DLNM/regression, wavelet coherence, Granger only,
  spatial cross-correlation, signal-processing / imaging / neuro / engineering uses)
- E2 not two empirical time series (simulation, method paper without applied data,
  review, meta-analysis, protocol)
- E3 n or lag range not recoverable
- E4 full text not retrievable from Europe PMC
- E5 off-topic (term matched incidentally)
- E6 duplicate

## Extraction (one row per included paper)

When a paper contains several lag scans, the first lag scan reported in the Results is the
analysis unit. If several series of that scan share the lag range but differ in length, the
longest analysed length is used (favourable to the paper) and the range is noted.

Fields: field, PMCID, DOI, year, title, frequency, n, n_derived (y/n), lag_min, lag_max,
direction (one-sided/symmetric), K, L, full_count, L_over_n, full_over_n, class_L,
class_full, sig_claim (y/n/unclear), test_used, corrected (y/n/na), quote_n, quote_lag,
notes.

## Analysis

- Shares of (a)/(b)/(c) under L (primary) and full count (secondary), overall and by field,
  each with a Wilson 95% interval.
- Share of included papers that made a significance claim on a selected lag without any
  correction for selection or autocorrelation (Wilson 95% interval), overall and by field.
- Extraction was done by one reviewer (an AI agent) with no second coder; this is a stated
  limitation.
