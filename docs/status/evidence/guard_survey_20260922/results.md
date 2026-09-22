# Guard survey results: L/n in published lag-scan analyses

Run: 2026-09-22 (UTC), following `protocol.md` (frozen 09:51 UTC, before any search).
Extraction table: `extraction.csv` (21 included papers, one row each, with the supporting quotes).
Extraction was done by a single AI reviewer with no second coder.

## Headline

Guard: refuse when L/n > 0.05. L = number of lags searched in one direction; the full count is
every lag evaluated. "Uncorrected claim" means the paper called the selected lag significant
without correcting for lag selection or autocorrelation.

| Group | N | (a) refused, by L | (b) near floor, by L | (c) room, by L | (a) by full count | (b) by full count | (c) by full count | Uncorrected claim |
|---|---|---|---|---|---|---|---|---|
| **All** | 21 | 11/21 = 52% [32%, 72%] | 2/21 = 10% [3%, 29%] | 8/21 = 38% [21%, 59%] | 13/21 = 62% [41%, 79%] | 4/21 = 19% [8%, 40%] | 4/21 = 19% [8%, 40%] | 12/21 = 57% [37%, 76%] |
| EPI (query field) | 14 | 7/14 = 50% [27%, 73%] | 2/14 = 14% [4%, 40%] | 5/14 = 36% [16%, 61%] | 9/14 = 64% [39%, 84%] | 2/14 = 14% [4%, 40%] | 3/14 = 21% [8%, 48%] | 9/14 = 64% [39%, 84%] |
| CLIM (query field) | 5 | 2/5 = 40% [12%, 77%] | 0/5 = 0% [0%, 43%] | 3/5 = 60% [23%, 88%] | 2/5 = 40% [12%, 77%] | 2/5 = 40% [12%, 77%] | 1/5 = 20% [4%, 62%] | 2/5 = 40% [12%, 77%] |
| FISH (query field) | 2 | 2/2 [34%, 100%] | 0/2 | 0/2 | 2/2 | 0/2 | 0/2 | 1/2 |
| Substantively epidemiological | 16 | 7/16 = 44% [23%, 67%] | 2/16 = 12% [3%, 36%] | 7/16 = 44% [23%, 67%] | 9/16 = 56% [33%, 77%] | 4/16 = 25% [10%, 49%] | 3/16 = 19% [7%, 43%] | 11/16 = 69% [44%, 86%] |
| Substantively environmental/ecological | 5 | 4/5 = 80% [38%, 96%] | 0/5 | 1/5 = 20% [4%, 62%] | 4/5 | 0/5 | 1/5 | 1/5 |

95% Wilson intervals are in brackets. The median L/n is 0.051, so the typical published scan
sits right at the guard's floor. Among the 14 papers that claimed significance, 12 made no
correction (86%, Wilson [60%, 96%]). The 2 corrected papers used a permutation null
(PMC12677548) and differencing plus BH-FDR (PMC13582498). No included paper prewhitened. The two
screened papers that did (PMC11358154, PMC9105987) were excluded under E3.

Plain reading: in this sample, about half of published lag-scan analyses would be refused by an
n >= 20L guard. About 1 in 10 sit near the floor. Roughly 4 in 10 have comfortable room.
Counting every lag evaluated (for example 2K+1) raises the refused share to about 60%.

### Boundary and uncertain cases (these change the counts by at most +/-1)

- PMC12922325 has L/n = 3/60 = 0.050 exactly, so it is (b) under a strict ">" guard.
  PMC13183819 has 8/156 = 0.051 (a), and PMC13266879 has 3/52 = 0.058 (a).
- PMC12639167 was read as monthly correlations computed per calendar month (n = 58 years), which
  gives (a). If the correlations were computed on the full monthly series (n = 696), it would be (c).
- PMC7822256 was read with n = 522 weekly points (c). The text allows the CCF to have run on
  the aggregated 52-week climatology (n = 52), which would give (a).
- These two uncertain readings pull in opposite directions, so the (a) count stays at 11/21
  under either pair of readings.
- In some cases the lag direction or one-sidedness is assumed; the CSV marks these "(assumed)".
  None of them changes the class under L. For PMC13183819, changing it changes only the
  full-count ratio, and the class stays the same.

## Sensitivity: records excluded because n or the lag range was not stated (E3)

E3 was the largest exclusion reason among topical records, with 26 records (EPI 6, CLIM 20). This matters because a
missing search range is itself a reporting gap. For some E3 records, the lag the paper selected
plus the stated window already fixes a lower bound on L/n, since the range searched must be at
least as long as the lag selected:

| PMCID | Evidence | Lower bound on L/n | Implied class |
|---|---|---|---|
| PMC12654024 | weekly, weeks 28-45 (n=18), selected lag -2 | >= 0.11 | (a) |
| PMC11286066 | about 30 weeks, lag about 3 weeks | >= 0.10 | (a) |
| PMC13350980 | daily, 1 year (n about 365), selected lag 49 days | >= 0.13 | (a) |
| PMC13547326 | monthly 2023-2025 (n <= 36), lag up to 263 days (about 9 months) | >= 0.24 | (a) |
| PMC11358154 | monthly 1987-2016 (n=360), significant lag at 21 months | >= 0.058 | (a) |
| PMC12302875 | n <= 96 months (2013-2020), lags searched up to 12 months | >= 0.125 | (a) |
| PMC9105987 | monthly 2015-2018 (n=48), selected lag 11 months | >= 0.23 | (a) |
| PMC12217918 | weekly to 2019 (n <= 313), selected lag 15 weeks | >= 0.048 | at least (b) |
| PMC7973231 | monthly, n=29, selected lag -1 month | >= 0.034 | at least (b) |

The other 17 E3 records cannot be bounded. Adding the 7 bounded (a) records and 2 bounded
"at least (b)" records, counted as (b), to the main sample gives (a) 18/30 = 60%
[42%, 75%], (b) 4/30 = 13%, and (c) 8/30 = 27%. The exclusion rule therefore probably
understates the refused share. It does not inflate it.

## Search and screening flow

| Query | Run (UTC) | Hits | Used | Screened | Eligible |
|---|---|---|---|---|---|
| EPI | 2026-09-22 09:51:30 | 39 | yes | 22 (stopped at 14 eligible) | 14 |
| CLIM (strict) | 09:52:04 | 16 | no, fewer than 20 hits, so the fallback was triggered | - | - |
| CLIM_FB | 09:52:08 | 45 | yes (all 16 strict hits are inside it) | 45 (all) | 5 |
| FISH (strict) | 09:52:12 | 9 | no, fewer than 20 hits, so the fallback was triggered | - | - |
| FISH_FB | 09:52:18 | 167 | yes | 80 (cap) | 2 |

Exact query strings are in `protocol.md`. Every query also carried
`AND OPEN_ACCESS:y AND HAS_FT:y AND PUB_YEAR:[2019 TO 2026] AND SRC:MED`.

Exclusions among the 147 screened records:

- E1 (no correlation lag scan): 6
- E3 (n or lag range not recoverable): 26
- E5 (off-topic): 76. Almost all of these come from FISH_FB, where "cross-correlation" plus
  "recruitment" or "catch" mostly matches EMG, neuroscience and biophysics papers.
- E6 (CLIM record that duplicates an EPI query record): 18
- E4 (full text unavailable): 0

## Deviations and clarifications (made after searching)

1. **Shortfall.** The target was 14 eligible records per field. CLIM (5) and FISH (2) ran out of
   records or hit the screening cap. Per the protocol, EPI was not used to back-fill. N = 21,
   well under the planned 40, and the field comparisons are too small to interpret.
2. **Fallback scope.** "ABSTRACT: removed from the topic block" was applied to the
   field-specific term groups only. The cross-correlation and lag groups stayed
   abstract-restricted.
3. **Duplicates.** A CLIM record that also appeared anywhere in the EPI query result set
   was logged as E6 and left to the EPI field. Several disease papers (leptospirosis, COVID-19)
   that appeared only in CLIM_FB stayed in CLIM, so the table also reports a
   substantive-field split.
4. **Non-contiguous lag grids.** PMC13371377 evaluated lags {0, 4, 8, 12, 16} weeks, so L
   counts the 4 nonzero lags searched rather than K = 16. The class is (a) either way.
5. **Interpolated daily data.** PMC11219297 used daily data spline-interpolated from weekly
   data. L/n is the same at weekly resolution.
6. **Resolution invariance.** L/n equals (maximum lag in time units) / (window length in time
   units). It therefore does not depend on sampling resolution, which is how PMC12340766 was
   handled despite its ambiguous resolution.
7. **Sensitivity analysis.** The E3 lower-bound analysis above was not pre-registered and
   is reported only as a sensitivity analysis.

## Limitations

- **Small sample.** With n = 21, the 95% interval for the refused share runs from 32% to
  72%. By field, only EPI (14) says anything.
- **Source restrictions.** `SRC:MED` open-access full text strongly under-represents
  fisheries, oceanography and hydrology. Most of that literature is in journals outside
  PubMed Central or behind paywalls, so FISH contributed 2 papers, both of them (a). A follow-up
  should use Crossref/OpenAlex full text or journal-specific sources such as ICES JMS, CJFAS and
  Fisheries Oceanography.
- **Relevance order.** Europe PMC's relevance ranking favours recent papers (2024-2026),
  so the sample is skewed toward recent surveillance papers, including wastewater and
  search-index studies with short windows. It is not a random sample.
- **Extraction.** Many n values are *derived* from dates and frequency (20 of 21). "n" is the
  per-series length of the first lag scan reported. Papers that scanned several regions or
  years each got one row. When a paper ran the CCF per year or season, n is that per-year or
  per-season length, which is what the scan used.
- **Single coder.** The direction of some scans was assumed, and there was no second coder.
- **Reporting gaps.** 26 otherwise-relevant records did not state the searched lag range or n
  in the main text. This is itself a finding: a plan-time guard needs L and n, and many
  papers never state them.
- **Significance coding.** Coding is based on the main text. A correction described only in
  supplements would be missed.

## Screening log (all 147 screened records, in API relevance order)

| Field | Rank | PMCID | DOI | Title | Decision |
|---|---|---|---|---|---|
| EPI | 1 | PMC13299343 | 10.3390/idr18030055 | Climate Variability Drives Dengue Transmission in Bangladesh. | INCLUDED |
| EPI | 2 | PMC13371377 | 10.1186/s12879-026-13643-6 | Climate variability and dengue incidence in southern Ecuador: an ecological analysis in two con | INCLUDED |
| EPI | 3 | PMC12677548 | 10.1371/journal.pgph.0005598 | Spatiotemporal co-distribution and time lagged cross correlation of malaria and dengue in Loret | INCLUDED |
| EPI | 4 | PMC13495405 | 10.1186/s13071-026-07507-w | Divergent urban-rural drivers of malaria vector ecology: a 6-year One Health longitudinal study | E1 CCF used only for model-vs-observation agreement, not a lead-lag scan |
| EPI | 5 | PMC12851297 | 10.1016/j.joclim.2025.100546 | Climatic thresholds associated with increased dengue incidence across climate zones in Peru (20 | INCLUDED |
| EPI | 6 | PMC13446735 | 10.1371/journal.pgph.0006960 | Understanding malaria dynamics in Benin through time series, and environmental correlation: Imp | E3 lag range only in supplementary figures (selected lags 1-2 months, n=96 monthly) |
| EPI | 7 | PMC13551350 | 10.1111/irv.70313 | Assessing the Utility of Over-The-Counter Medication to Track Influenza Season Timing in a Sout | INCLUDED |
| EPI | 8 | PMC12922325 | 10.1186/s12936-026-05824-0 | Climate variability and malaria incidence trends in Yumbe District, West Nile Sub-region of Uga | INCLUDED |
| EPI | 9 | PMC13183819 | 10.3389/fmed.2026.1820896 | Analysis of influenza surveillance results in Sichuan Province in China, 2023-2025. | INCLUDED |
| EPI | 10 | PMC12830810 | 10.1038/s41598-025-33072-w | Nationwide population-level influenza cycle threshold values and trends in influenza incidence: | INCLUDED |
| EPI | 11 | PMC13483624 | 10.1186/s12879-026-14153-1 | SALGINTR: development and early evaluation of a low-cost cloud-based digital participatory surv | INCLUDED |
| EPI | 12 | PMC12217918 | 10.1186/s12936-025-05428-0 | Modelling the effects of precipitation and temperature on malaria incidence in coastal and west | E3 searched lag range not stated (selected 7-15 weeks; weekly 2014-2019) |
| EPI | 13 | PMC12586018 | 10.3389/fpubh.2025.1662775 | Improving influenza prediction in Quanzhou, China: an ARIMAX model integrated with meteorologic | INCLUDED |
| EPI | 14 | PMC12565952 | 10.3390/microorganisms13102268 | Long-Term Sewage Survey of SARS-CoV-2, Influenza A and Respiratory Syncytial Virus (RSV), and C | E3 searched lag range not stated (daily; selected 5-10 days) |
| EPI | 15 | PMC13266879 | 10.21037/jtd-2025-1-2454 | Monitoring pneumonia onset and severe respiratory infectious diseases using quantitative comput | INCLUDED |
| EPI | 16 | PMC12654024 | 10.3390/microorganisms13112526 | Harnessing a Surface Water-Based Multifaceted Approach to Combat Zoonotic Viruses: A Rural Pers | E3 searched lag range not stated (weekly, weeks 28-45 2023, n=18; selected lag -2) |
| EPI | 17 | PMC11219297 | 10.46234/ccdcw2024.084 | Exploring the Lagged Correlation Between Baidu Index and Influenza-Like Illness - China, 2014-2 | INCLUDED |
| EPI | 18 | PMC13582498 | 10.3389/fpubh.2026.1856514 | Fusing meteorological factors and baidu search index with an adapted deformtime model to predic | INCLUDED |
| EPI | 19 | PMC12338964 | 10.2196/71786 | A Deep Learning Framework for Using Search Engine Data to Predict Influenza-Like Illness and Di | E1 lags 1-3 reported as fixed forecast horizons for keyword screening; no lag selected by scan |
| EPI | 20 | PMC11286066 | 10.3201/eid3008.240225 | Wastewater Surveillance to Confirm Differences in Influenza A Infection between Michigan, USA,  | E3 searched lag range not stated (Sep 2022-Mar 2023, about 30 weeks; lag about 3 weeks) |
| EPI | 21 | PMC9779123 | 10.3390/ijerph192417048 | Early Detection of the Start of the Influenza Epidemic Using Surveillance Systems in Catalonia  | E3 searched lag range not stated (weekly per season wk40-wk20 and pooled; lags up to 3 weeks reported) |
| EPI | 22 | PMC11121319 | 10.3390/ijerph21050558 | The Impact of Climatic Factors on Temporal Mosquito Distribution and Population Dynamics in an  | INCLUDED |
| CLIM | 1 | PMC13371377 | 10.1186/s12879-026-13643-6 | Climate variability and dengue incidence in southern Ecuador: an ecological analysis in two con | E6 duplicate of EPI query record |
| CLIM | 2 | PMC12875516 | 10.1371/journal.pone.0339023 | Spatiotemporal patterns of soil moisture in Shandong Province, China: An analysis using ERA5-La | E3 searched lag range not stated (monthly; selected 0-2 months) |
| CLIM | 3 | PMC12639167 | 10.1038/s41598-025-25396-4 | Integrated use of meteorological and hydrological indices for drought early warning in the moun | INCLUDED |
| CLIM | 4 | PMC13350980 | 10.1038/s41598-026-44533-1 | Hydrometric assessment of Himalayan springs using classical hydrological methods for springshed | E3 searched lag range not stated (daily Jul 2021-Jul 2022; selected lags 1-49 days) |
| CLIM | 5 | PMC13547326 | 10.1038/s41598-026-58032-w | Revealing the lagged relationship between groundwater changes and land subsidence in Tianjin ba | E3 searched lag range not stated (monthly GRACE 2023-2025; selected lags 41-263 days) |
| CLIM | 6 | PMC13299343 | 10.3390/idr18030055 | Climate Variability Drives Dengue Transmission in Bangladesh. | E6 duplicate of EPI query record |
| CLIM | 7 | PMC13495405 | 10.1186/s13071-026-07507-w | Divergent urban-rural drivers of malaria vector ecology: a 6-year One Health longitudinal study | E6 duplicate of EPI query record |
| CLIM | 8 | PMC13120146 | 10.3390/plants15081175 | Differential Responses and Temporal Lags of Heterotrophic and Autotrophic Respiration to Plant  | E3 n and lag range not stated in text (hourly Apr-Nov; selected 13 h) |
| CLIM | 9 | PMC11358154 | 10.1038/s41598-024-67736-w | A thirty-year time series analyses identifies coherence between oscillations in Anthrax outbrea | E3 searched lag range not stated (monthly 1987-2016, n=360, prewhitened; significant lags up to 21 months) |
| CLIM | 10 | PMC13446735 | 10.1371/journal.pgph.0006960 | Understanding malaria dynamics in Benin through time series, and environmental correlation: Imp | E6 duplicate of EPI query record |
| CLIM | 11 | PMC12922325 | 10.1186/s12936-026-05824-0 | Climate variability and malaria incidence trends in Yumbe District, West Nile Sub-region of Uga | E6 duplicate of EPI query record |
| CLIM | 12 | PMC10933480 | 10.1038/s41598-024-56526-z | Spatiotemporal heterogeneity in meteorological and hydrological drought patterns and propagatio | E1 scan over SPEI accumulation scales 1-24 months, not time shifts |
| CLIM | 13 | PMC11982564 | 10.1038/s41598-025-96644-w | Time lag effect of precipitation on groundwater level based on wavelet analysis in the People's | E3 searched lag range not stated (monthly 1993-2021; selected 6-8 months) |
| CLIM | 14 | PMC12851297 | 10.1016/j.joclim.2025.100546 | Climatic thresholds associated with increased dengue incidence across climate zones in Peru (20 | E6 duplicate of EPI query record |
| CLIM | 15 | PMC11356426 | 10.1371/journal.pone.0307376 | Relationship of litterfall anomalies with climatic anomalies in a mangrove swamp of the Yucatan | E3 searched lag range not stated (monthly 1999-2010; selected 2 months) |
| CLIM | 16 | PMC12496220 | 10.1016/j.isci.2025.113321 | High-resolution modeling of glacier meltwater contributions to lake water level fluctuations in | E3 n not stated (hourly; lags up to 24 h) |
| CLIM | 17 | PMC12217918 | 10.1186/s12936-025-05428-0 | Modelling the effects of precipitation and temperature on malaria incidence in coastal and west | E6 duplicate of EPI query record |
| CLIM | 18 | PMC11207421 | 10.3390/plants13121702 | Influence of Time-Lag Effects between Winter-Wheat Canopy Temperature and Atmospheric Temperatu | E3 searched lag range not stated (2-min data; lags 32-97 min) |
| CLIM | 19 | PMC12677548 | 10.1371/journal.pgph.0005598 | Spatiotemporal co-distribution and time lagged cross correlation of malaria and dengue in Loret | E6 duplicate of EPI query record |
| CLIM | 20 | PMC12340766 | 10.1021/acsestair.5c00126 | Effect of Long-Range Transported Aerosol on Urban Air Quality in Eastern Germany. | INCLUDED |
| CLIM | 21 | PMC13211277 | 10.3390/toxics14050378 | Spatiotemporal Variability Analysis of PM&lt;sub&gt;2.5&lt;/sub&gt; and O&lt;sub&gt;3&lt;/sub&g | E1 spatio-temporal CCF across cities, not a two-series lag scan |
| CLIM | 22 | PMC10638002 | 10.1016/j.heliyon.2023.e21574 | Reversal in the drought stress response of the Scots pine forest ecosystem: Local soil water re | E3 series length not stated (annual tree-ring; lags up to 5 years) |
| CLIM | 23 | PMC7007072 | 10.1029/2019gh000186 | Spatial-Temporal Assessment of Environmental Factors Related to Dengue Outbreaks in São Paulo,  | E6 duplicate of EPI query record |
| CLIM | 24 | PMC12302875 | 10.1186/s13071-025-06805-z | Diversity and seasonality of ectoparasite burden on two species of Madagascar fruit bat, Eidolo | E3 n not stated (6-weekly captures 2013-2020 binned monthly; lags up to 12 months) |
| CLIM | 25 | PMC12654024 | 10.3390/microorganisms13112526 | Harnessing a Surface Water-Based Multifaceted Approach to Combat Zoonotic Viruses: A Rural Pers | E6 duplicate of EPI query record |
| CLIM | 26 | PMC11121319 | 10.3390/ijerph21050558 | The Impact of Climatic Factors on Temporal Mosquito Distribution and Population Dynamics in an  | E6 duplicate of EPI query record |
| CLIM | 27 | PMC12391079 | 10.3389/fpubh.2025.1640581 | Temporal dynamics of SARS-CoV-2 detection in wastewater and population infection trends in Mexi | E3 searched lag range not stated (daily, time blocks; selected 6-8 days) |
| CLIM | 28 | PMC9415847 | 10.3390/tropicalmed7080170 | Epidemiological Profile of a Human Hepatitis E Virus Outbreak in 2018, Chattogram, Bangladesh. | E3 n and lag range not stated (daily env. data 3 months before exposure; selected 24 days) |
| CLIM | 29 | PMC12565952 | 10.3390/microorganisms13102268 | Long-Term Sewage Survey of SARS-CoV-2, Influenza A and Respiratory Syncytial Virus (RSV), and C | E6 duplicate of EPI query record |
| CLIM | 30 | PMC12474395 | 10.3390/tropicalmed10090264 | Wastewater-Based Surveillance of SARS-CoV-2 and Modeling of COVID-19 Infection Trends. | E3 n and searched range not stated (daily; peaks 0 and 21-23 days) |
| CLIM | 31 | PMC8145696 | 10.3390/e23050559 | The Vegetation-Climate System Complexity through Recurrence Analysis. | INCLUDED |
| CLIM | 32 | PMC9177473 | 10.1007/s10653-021-00864-8 | Temperature and discharge variations in natural mineral water springs due to climate variabilit | E3 searched lag range not stated (monthly 2001-2018; selected 0-3 months) |
| CLIM | 33 | PMC7822256 | 10.1371/journal.pone.0245366 | The interrelationship between meteorological parameters and leptospirosis incidence in Hambanto | INCLUDED |
| CLIM | 34 | PMC8906134 | 10.1016/j.crpvbd.2021.100014 | Modeling the association between Aedes aegypti ovitrap egg counts, multi-scale remotely sensed  | E6 duplicate of EPI query record |
| CLIM | 35 | PMC7973231 | 10.3389/fpsyt.2021.653390 | Meteorological Variables and Suicidal Behavior: Air Pollution and Apparent Temperature Are Asso | E3 searched lag range not stated (monthly Mar 2016-Jul 2018, n=29; selected -1 month) |
| CLIM | 36 | PMC9040212 | 10.1186/s12879-022-07393-4 | Prototypes virus of hand, foot and mouth disease infections and severe cases in Gansu, China: a | E3 n and lag range not stated (weekly; selected 4 weeks) |
| CLIM | 37 | PMC7994810 | 10.1038/s41598-021-86403-y | Temporal and spatial lags between wind, coastal upwelling, and blue whale occurrence. | E3 n and searched lag range not stated (weekly; lags 0-3 weeks) |
| CLIM | 38 | PMC7893867 | 10.1186/s12936-021-03641-1 | Effects of rainfall, temperature and topography on malaria incidence in elimination targeted di | E6 duplicate of EPI query record |
| CLIM | 39 | PMC9105987 | 10.3390/ijerph19095385 | Modeling and Predicting Pulmonary Tuberculosis Incidence and Its Association with Air Pollution | E3 searched lag range not stated (monthly 2015-2018, n=48, prewhitened; selected lags up to 11 months) |
| CLIM | 40 | PMC6936853 | 10.1371/journal.pone.0226841 | A dengue fever predicting model based on Baidu search index data and climate data in South Chin | E6 duplicate of EPI query record |
| CLIM | 41 | PMC6466923 | 10.1155/2019/7314129 | Malaria Risk Stratification and Modeling the Effect of Rainfall on Malaria Incidence in Eritrea | E6 duplicate of EPI query record |
| CLIM | 42 | PMC7489993 | 10.1016/j.heliyon.2020.e04858 | A decade of arbovirus emergence in the temperate southern cone of South America: dengue, Aedes  | E6 duplicate of EPI query record |
| CLIM | 43 | PMC8586838 | 10.1007/s11356-021-17268-x | Effect of meteorological factors on the COVID-19 cases: a case study related to three major cit | INCLUDED |
| CLIM | 44 | PMC7164191 | 10.1186/s12889-020-08599-4 | Effect of climatic factors on the seasonal fluctuation of human brucellosis in Yulin, northern  | E3 CCF lag range only in figure (monthly 2005-2018) |
| CLIM | 45 | PMC6396465 | 10.1186/s12889-019-6565-z | Socioeconomic and environmental factors associated with malaria hotspots in the Nanoro demograp | E6 duplicate of EPI query record |
| FISH | 1 | PMC13468714 | 10.3390/s26154914 | How Stable Are Temporal EMG Parameters in Rowing? A Seven-Day Test-Retest Reliability Study Usi | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 2 | PMC12894980 | 10.1038/s41598-026-36897-1 | Climate-driven reproductive decline in Southern right whales. | INCLUDED |
| FISH | 3 | PMC13499156 | 10.1016/j.jbc.2026.113353 | Oncogenic EGFR mutants differentially alter dimerization, adaptor protein engagement, and clath | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 4 | PMC12722886 | 10.3389/fspor.2025.1657944 | Exploring the relationship between movement and breathing regulation in Tai Chi practice among  | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 5 | PMC13320635 | 10.14814/phy2.70994 | Networks of respiratory-muscular coupling in exercise and fatigue in young adults. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 6 | PMC13242970 | 10.1111/acps.70094 | Trajectories of Suicidal Risk Impact Mood Regulation Differently in Patients With a Diagnosis o | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 7 | PMC13539395 | 10.1002/epi4.70348 | Bilateral detection, prediction, and lateralization of seizures using white matter. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 8 | PMC13584328 | 10.1111/irv.70323 | What Different Surveillance Systems Tell Us About Winter Respiratory Illness in England: A Time | E5 not fisheries (epidemiology/entomology) |
| FISH | 9 | PMC13447594 | 10.1177/0271678x261473390 | Cerebrovascular reactivity delay measured by blood oxygen level dependent magnetic resonance im | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 10 | PMC13469408 | 10.3389/fnhum.2026.1757743 | Exploring motor speech patterns in adults with minimally verbal autism spectrum disorder throug | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 11 | PMC13361764 | 10.3390/ijms27136068 | Loss of Neuropeptide Y Signaling Accompanies the Neural-to-Mesenchymal Transcriptional Transiti | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 12 | PMC13483624 | 10.1186/s12879-026-14153-1 | SALGINTR: development and early evaluation of a low-cost cloud-based digital participatory surv | E5 not fisheries (epidemiology/entomology) |
| FISH | 13 | PMC13337042 | 10.1002/advs.76217 | Wearable-Derived Diurnal Alignment Between Physical Activity and Device Temperature Predicts Fu | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 14 | PMC13473279 | 10.3389/fnmol.2026.1875988 | Dynamic structural profiling of PINK1 mutations (T313M and L347P) reveals a vital molecular per | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 15 | PMC13091187 | 10.1158/2159-8290.cd-25-0775 | Same-Slide Spatial Multiomics Integration with IN-DEPTH Reveals Tumor Virus-Linked Spatial Reor | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 16 | PMC13158002 | 10.1111/adb.70164 | Reduced Coupling of Global Brain Activity and Cerebrospinal Fluid Flow in Individuals With Bete | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 17 | PMC12845269 | 10.3390/ph19010124 | The Allosteric Regulation of the DNA-Binding Domain of p53 by the Intrinsically Disordered C-Te | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 18 | PMC13365045 | 10.3389/fnins.2026.1798238 | SMILE: neural signal acquisition and intra-body transmission for facial nerve bypass-An acute f | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 19 | PMC13236768 | 10.1007/s00421-025-06083-8 | Reduced knee extensor torque steadiness and increased motor unit discharge rate variability in  | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 20 | PMC12948821 | 10.1007/s00421-025-05953-5 | Independent neural drives and distinct motor unit discharge characteristics in hamstring muscle | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 21 | PMC13111922 | 10.14814/phy2.70884 | Cardiorespiratory coupling tightens with workload during graded exercise: A pilot study with ad | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 22 | PMC12568204 | 10.3390/s25206395 | Application of Wireless EMG Sensors for Assessing Agonist-Antagonist Muscle Activity During 50- | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 23 | PMC11737280 | 10.1186/s13071-024-06655-1 | Identification of Southeast Asian Anopheles mosquito species with matrix-assisted laser desorpt | E5 not fisheries (epidemiology/entomology) |
| FISH | 24 | PMC13486289 | 10.3389/fpsyg.2026.1862323 | Emotional resonance in the digital society: narrative mediation, platform hierarchy, and virtua | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 25 | PMC13046454 | 10.26603/001c.158518 | Effects of Lower-Leg Fascial Flossing on Flexibility and Performance in Collegiate Distance Run | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 26 | PMC13471506 | 10.1186/s13075-026-03834-6 | Site-level cutaneous phenotyping framework for anti-MDA5-positive dermatomyositis: exploratory  | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 27 | PMC13526343 | 10.2147/nss.s618511 | Associations Between Obstructive Sleep Apnea, Macro-Scale Glymphatic Coupling, and Episodic Mem | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 28 | PMC12451173 | 10.1016/j.isci.2025.113333 | Improved positioning criterion and imaging scheme of deep UV planar laser-induced fluorescence  | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 29 | PMC11627008 | 10.1111/bdi.13504 | Mood regulation in euthymic patients with a history of antidepressant-induced mania. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 30 | PMC12824988 | 10.1021/acs.analchem.5c05327 | Orthogonal Investigation at Single-Particle and Ensemble Levels Uncovers Lipoprotein-Extracellu | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 31 | PMC12494029 | 10.1126/sciadv.adw6425 | Mechanochemical waves in focal adhesions during cell migration. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 32 | PMC12746092 | 10.1016/j.yjsbx.2025.100136 | DiameTR: A cryo-EM tool for diameter sorting of tubular samples. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 33 | PMC11767648 | 10.3390/mi16010061 | Distance Measurement and Error Compensation of High-Speed Coaxial Rotor Blades Based on Coded U | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 34 | PMC12565952 | 10.3390/microorganisms13102268 | Long-Term Sewage Survey of SARS-CoV-2, Influenza A and Respiratory Syncytial Virus (RSV), and C | E5 not fisheries (epidemiology/entomology) |
| FISH | 35 | PMC13058645 | 10.1017/s0033291725102754 | Reduced interpersonal head synchrony in youth at clinical high risk for psychosis. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 36 | PMC12411523 | 10.3389/fninf.2025.1628538 | A correlation-based tool for quantifying membrane periodic skeleton associated periodicity. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 37 | PMC12614549 | 10.1371/journal.pone.0336503 | Early adherence to biofeedback training predicts long-term improvement in stroke patients: A ma | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 38 | PMC12551884 | 10.1371/journal.pone.0334177 | Feasibility study of a sensor-to-segment calibration method to enhance upper limb motion analys | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 39 | PMC11316813 | 10.1038/s41598-024-69050-x | Eccentric exercise-induced delayed onset trunk muscle soreness alters high-density surface EMG- | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 40 | PMC12609384 | 10.3390/s25216754 | Electro-Oculography and Proprioceptive Calibration Enable Horizontal and Vertical Gaze Estimati | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 41 | PMC12635726 | 10.3389/fnetp.2025.1686723 | Case Report: network physiology markers of inter-muscular interactions indicate reversal of age | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 42 | PMC12474724 | 10.1007/s10548-025-01148-5 | Lag-structure in fMRI across Three Psychiatric Groups: State-dependency and Clinical-behavioral | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 43 | PMC12153640 | 10.3390/ani15111632 | Improving Mobility: A Case Report on the Rehabilitation of a Gait Anomaly in an Asian Elephant  | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 44 | PMC12473605 | 10.3390/s25185918 | Continuous Vibration-Driven Virtual Tactile Motion Perception Across Fingertips. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 45 | PMC12598106 | 10.17179/excli2025-8672 | Bilateral force control and coordination patterns across upper and lower limbs. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 46 | PMC12624510 | 10.3389/fpsyt.2025.1670602 | Mapping neural effects of mindfulness-based cognitive therapy in ADHD using EEG microstates and | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 47 | PMC12537830 | 10.1002/brb3.70963 | Cortical Intra-Layer Hypersynchronization in Levodopa-Induced Dyskinesia Mouse Model. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 48 | PMC11494524 | 10.1016/j.bpj.2024.08.017 | The minimal membrane requirements for BAX-induced pore opening upon exposure to oxidative stres | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 49 | PMC11595894 | 10.3390/life14111433 | Characteristics, Relationships, and Differences in Muscle Activity and Impact Load Attenuation  | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 50 | PMC12857484 | 10.1113/ep092890 | Microelectrode recordings from the human cervical vagus nerve during maximal breath-holds. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 51 | PMC11875027 | 10.1167/jov.25.2.12 | Temporal dynamics of human color processing measured using a continuous tracking task. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 52 | PMC11436203 | 10.3390/s24186091 | Research on Signal Noise Reduction and Leakage Localization in Urban Water Supply Pipelines Bas | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 53 | PMC11846298 | 10.1186/s12938-025-01353-0 | Cross-evaluation of wearable data for use in Parkinson's disease research: a free-living observ | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 54 | PMC11792532 | 10.1186/s12958-024-01329-0 | Continuous overnight monitoring of body temperature during embryo transfer cycles as a proxy fo | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 55 | PMC10694166 | 10.1016/j.heliyon.2023.e22207 | Unsupervised deep network for image texture transformation: Improving the quality of cross-corr | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 56 | PMC12061428 | 10.1371/journal.pone.0320519 | Anatomically distinct cortical tracking of music and speech by slow (1-8Hz) and fast (70-120Hz) | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 57 | PMC11314729 | 10.3390/s24154954 | Muscle Network Connectivity Study in Diabetic Peripheral Neuropathy Patients. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 58 | PMC12021142 | 10.1371/journal.pone.0321902 | Molecular activity of bioactive phytocompounds for inhibiting host cell attachment and membrane | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 59 | PMC10189551 | 10.1016/j.nicl.2023.103422 | Single-trial neuromagnetic analysis reveals somatosensory dysfunction in chronic Minamata disea | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 60 | PMC11495179 | 10.1152/jn.00391.2023 | Achilles tendon morpho-mechanical parameters are related to triceps surae motor unit firing pro | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 61 | PMC12128296 | 10.1186/s13054-025-05403-w | The value of dynamic cerebral compliance monitoring after pediatric traumatic brain injury: a S | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 62 | PMC7522274 | 10.1038/s41598-020-73079-z | Impact of unequal distances among acoustic sensors on cross-correlation based fisheries stock a | E1 acoustic signal-processing cross-correlation |
| FISH | 63 | PMC10552112 | 10.1021/acsomega.3c06078 | Deubiquitination Detection of p53 Protein in Living Cells by Fluorescence Cross-Correlation Spe | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 64 | PMC11329853 | 10.2196/57953 | Preliminary Validity and Acceptability of Motion Tape for Measuring Low Back Movement: Mixed Me | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 65 | PMC11849118 | 10.1016/j.jbc.2025.108186 | Lipid droplet targeting of the lipase coactivator ABHD5 and the fatty liver disease-causing var | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 66 | PMC11436235 | 10.3390/s24185954 | Development of Surface EMG for Gait Analysis and Rehabilitation of Hemiparetic Patients. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 67 | PMC12087215 | 10.1186/s12936-025-05353-2 | Spatial and temporal variation of malaria incidence in children under 10 years in a pyrethroid- | E5 not fisheries (epidemiology/entomology) |
| FISH | 68 | PMC10849019 | 10.1523/eneuro.0384-23.2023 | Afferents to Action: Cortical Proprioceptive Processing Assessed with Corticokinematic Coherenc | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 69 | PMC11126011 | 10.3390/v16050722 | Gut Microbiome and Cytokine Profiles in Post-COVID Syndrome. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 70 | PMC11912730 | 10.1186/s12891-025-08506-1 | Motion analysis of 3D multi-segmental spine during gait in symptom remission people with low ba | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 71 | PMC10707141 | 10.3390/ma16237390 | Investigation of Different Features for Baseline-Free RAPID Damage-Imaging Algorithm Using Guid | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 72 | PMC9320664 | 10.3390/plants11141791 | Fruit Phenolic and Triterpenic Composition of Progenies of Olea europaea subsp. cuspidata, an I | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 73 | PMC11717918 | 10.1038/s41598-025-85621-y | The importance of trunk motion in wearable based infant spontaneous movement analysis. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 74 | PMC7364117 | 10.1016/j.dib.2020.106006 | Airfreight data from Memanbetsu airport correlated to fish and scallop catch in okhotsk subpref | INCLUDED |
| FISH | 75 | PMC9555664 | 10.1371/journal.pone.0275569 | Interspecific synchrony on breeding performance and the role of anthropogenic food subsidies. | E1 zero-lag synchrony correlation; no lag scan |
| FISH | 76 | PMC10952824 | 10.1113/jp284503 | Two motor neuron synergies, invariant across ankle joint angles, activate the triceps surae dur | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 77 | PMC11445581 | 10.1038/s44318-024-00194-2 | Spatial control of the APC/C ensures the rapid degradation of cyclin B1. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 78 | PMC12021880 | 10.3389/fpsyg.2025.1509396 | Feasibility and preliminary outcomes of compassion-focused acceptance and commitment therapy de | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 79 | PMC11414908 | 10.1371/journal.pone.0308146 | Packet information encoding in a cerebellum-like circuit. | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
| FISH | 80 | PMC11076110 | 10.1098/rsos.230590 | Effects of passive ankle exoskeletons on neuromuscular function during exaggerated standing swa | E5 off-topic for field (biomedical/engineering/other use of cross-correlation) |
