# Guard novelty check: L/n floor for lag-scan + circular-shift null (2026-09-22)

Claim tested: "With a circular-shift null and a scan over L lags, L of the n circular
states always tie with the observed maximum (shift s = c* - c maps each searched lag c
onto the selected lag c*), so the exact p-value cannot fall below L/n; plans with
L/n > alpha can never reach significance."

**Verdict.** None of the sources checked states this bound or the tie argument behind
it. The closest is Yuan & Shou (2024), which states a bound of the **same arithmetic
form** for a **different procedure**: a multi-lag TTS test with m lags, Bonferroni-corrected,
"requires a truncation radius of at least m/alpha - 1". So the paper can claim the
tie-based floor for a max-over-lags statistic under the full circular group, and the
enforced plan-time check. It should not claim to be the first to note that wider lag
ranges need longer series, or that permutation resolution must beat alpha. That second
point is also already enforced in software by IDTxl (`check_n_perm`).

## Sources read (full text)

| # | Source | Material read | Retrieved from |
|---|---|---|---|
| 1 | Cannistra, Hoang, Yuan & Shou, eLife RP 108198 v1 (bioRxiv 10.1101/2024.10.11.617506) | Full JATS XML: main text, Methods, Tables 1–3 (Table 3 as image), eLife assessment, reviews; full 15-page Appendix PDF (`617506_file02.pdf`) | github elife-article-xml `preprints/elife-preprint-108198-v1.xml`; appendix from `prod--epp.elifesciences.org/api/files/108198/v1/content/supplements/617506_file02.pdf` (bioRxiv direct links blocked by bot protection; same file) |
| 2 | Yuan & Shou, PLoS Biol 22:e3002758 (2024) | Full main-text XML (all sections and Methods); S1 Text appendix PDF (55 pp.): TOC, section 2 proof, sections 3, 4.3–4.5, 6, 7, 8.3, 11 read closely, remainder checked by keyword (lag, cyclic, tie, minimum, p-value, 1/alpha, r+1) | journals.plos.org manuscript XML and supplementary file s010 |
| 3 | Harris, arXiv:2012.06862 (v1 only, 12 Dec 2020) | Full PDF including appendix proofs | arxiv.org |
| 4a | Cliff, Novelli, Fulcher, Shine & Lizier, Phys Rev Res 3:013145 (2021) | Full PDF; checked by keyword, and the surrogate section (App. A.3) read | journals.aps.org |
| 4b | IDTxl `idtxl/stats.py` (master @ c7eacfd) | `check_n_perm`, `_find_pvalue`, `max_statistic` setup | github pwollstadt/IDTxl |

Note: PDF math extraction for Harris lost some symbols. Harris formulas below are
restored from context and marked [reconstructed].

---

## 1. Cannistra et al. (eLife RP 2025 / bioRxiv 2024): classification **B (weak)**

Relevant setup:
- Circular-shift null uses **every** shift. Methods, "Benchmarking statistical tests":
  > "For all surrogate methods except truncated time shift, the p-value was calculated as (1 + n larger )/(1 + n surr ) where n larger is the number of surrogate correlations that are as large as or larger than the original correlation, and n surr is the total number of surrogate correlations. For surrogates produced by the random shuffle, stationary bootstrap, random phase, and twin methods, we used n surr = 99 surrogates. For the circular time shift method, we used all possible surrogates (see Appendix)."
- Appendix, "Circular time shift":
  > "if the original time series is {1, 2, 3, 4}, then this method would produce three surrogates: {2, 3, 4, 1}, {3, 4, 1, 2}, and {4, 1, 2, 3}."
- Resolution ingredient, Fig. 2 caption (B-iii):
  > "An asterisk (*) indicates detection of a significant correlation with p = 1/6 (in practice, at least 19 surrogates are needed to achieve p = 0.05)."
- Tailored lags, Results, "Different methods of accounting for lagged correlation...":
  > "Alternatively, one can optimize the lag for the original correlation and then independently optimize the lag for surrogate correlations ("tailored lags"). Since the tailored lag approach applies the same pre-processing steps to both the original and surrogate data, it seems more likely to produce valid tests"
- Lag grid, Fig. 2C caption:
  > "Lags, when used, were chosen from between −10 and 10 in steps of size 2."

  That is L = 11. Table 3 gives 250 time points for Fig. 2.
- Truncated time shift, Appendix:
  > "we use an adjusted p-value calculated as (N≥ + 1)/(r + 1)"

  This cites Yuan & Shou.

What is **absent**: the paper never mentions a minimum p-value for circular shift combined
with tailored lags, ties between surrogates and the observed maximum, the shift-maps-lag
(group) argument, or any L/n or lag-range-versus-length constraint. The appendix trims
series for circularization but does not discuss how this changes n. The tailored-lag
discussion is only about validity (fixed versus tailored), not resolution.

Observation, not a claim of theirs: for Fig. 2, L/n = 11/250 = 0.044, just under 0.05.
Circularization trimming shortens n, so after trimming the design could sit near or over
the floor. This is exact only if their lagged statistic is circular. Their Fig. 2A
definition, "Pearson correlation between x_i and y_{i−l}", does not say whether it
wraps. We did not verify this in their code; no code link appears in the XML.

## 2. Yuan & Shou (PLoS Biol 2024): classification **B, with an explicit same-form bound for a different procedure (Bonferroni multi-lag TTS)**

Main text, "Strategies to achieve high statistical power with the TTS test":
> "If r is exactly 19, significance will be detected at the α = 0.05 level only when B = 1, meaning that the unshifted correlation would need to exceed all shifted correlations. If 20≤r≤38, significance at the 0.05 level still requires B = 1 ... Generalizing this reasoning, for a significance level α, power is maximized when r = j/α − 1 (4) where j is a positive integer"

Main text, "Strategies for increasing power in the presence of a coupling lag", multi-lag paragraph:
> "we can perform a "multi-lag" test (Fig 3C): test for dependence between {xt+l} and {yt} for several different values of l and perform a Bonferroni correction. More precisely, if m different lags are tested, then dependence may be reported if any of the m tests is significant at the α/m level. Parallel to Eq 4, for m tests and a significance level of α, the optimal truncation radius r values are r = jm/α − 1 (5) where j is a positive integer (Fig 3C). With a larger range of possible lags, the minimum r value increases and longer series may be needed."

Discussion, "Limitations of this study and the TTS test", the most explicit sentence:
> "Similarly, the TTS test has limited power when we do not have sufficient data to handle an unknown and potentially large coupling delay, which would require the multi-lag procedure. Recall that per Eq 5, a multi-lag TTS test with m lags requires a truncation radius of at least m/α−1 and thus requires a time series longer than 2(m/α−1)."

This is equivalent to "the minimum corrected u, which is m/(r+1), must be ≤ alpha", the
same form as L/n ≤ alpha. It comes from Bonferroni times per-test resolution 1/(r+1). It
does not come from ties, the circular group, or a max-over-lags statistic.

Main text, lag selection:
> "We stress that l should not be selected based on the data themselves, since this way, dependence will always be declared."

Adjacent shifts, main text around Eq 2:
> "As Bartlett [40] noted, pnaive is not a valid p-value because the surrogate y series are not independent of each other (e.g., 2 consecutive shifts are nearly identical)."

Cyclic permutation, main text and Methods:
> "One way to achieve this is to use cyclic permutations [24,32] ... However, these surrogates artificially force the first and final points of the original {yt} series to become neighbors, which can distort the dynamics"

> "If the original time series was of length n, then n-1 cyclic permutation surrogate were produced."

The cyclic-permutation arm in their benchmark uses no lag scan.

S1 Text section 3, "naive TTS test with an expected coupling delay". This is a
single fixed Δ, compared with all shifts, p = B_Δ/(2r+1). It is not a max over lags. The
section shows the variant can be miscalibrated:
> "strongly negative values of ∆ result in a false positive rate as high as 30%"

S1 Text section 7.3:
> "we used the lowest value of r that would enable significance at the 0.05 level after the Bonferroni correction (i.e. r = 59 for 3 lags, r = 99 for 5 lags, and so on)." ... "We used 1499 IAAFT surrogates rather than 99, to account for the lower p-values demanded by the Bonferroni correction."

S1 Text section 11 gives a structural-tie floor, the closest in spirit:
> "if {yt} is periodic, then the shifted correlation between {yt} and {xt} will also be periodic, resulting in a many-way tie for the highest shifted correlation (Fig A-23B)." Fig A-23 caption: "we have u = 15/(79 + 1) > 0.05 and so no detection can be made at the 0.05 level."

The accompanying theorem (section 11.1) says any nonrandom test valid under stationarity has
no power when y has period k < 1/α, via P(...) ≥ 1/k > α.

This is a tie-induced floor, but it comes from periodicity of the **data**. Our floor
comes from the **procedure**: lag scan plus circular group. It holds for any data.

What is **absent**: no statement that a max-over-lags statistic under circular shifts
produces L exact ties, and no L/n floor for circular or cyclic nulls.

## 3. Harris (arXiv:2012.06862, 2020): classification **B**

Abstract:
> "If the series are independent, the unshifted value is in the top m shifted values with probability at most m/(N+1). For large N, the probability approaches m/(2N+1). A conservative test rejects independence at significance α if the unshifted value is in the top α(N+1)"

Main text, Example:
> "we took N = 19, allowing the null to be conservatively rejected at p=0.05 if m = 1." [reconstructed; symbols lost in extraction]

This is the resolution ingredient: minimum attainable level 1/(N+1).

Discussion:
> "If the time series are expected to exhibit less temporally precise correlations, then V might measure the error of predicting Y from several neighboring timesteps of X; in this case a larger value of N may be required, allowing the null to be rejected if the peak is near but not exactly at s = 0." [reconstructed]

This is qualitative: temporal imprecision means more shifts are needed. It gives no bound.

Ties, Example:
> "A small jump at m = 39 indicated an excess fraction of cases where V_s = V_0 for all s, due to occasional ties." [reconstructed]

These are data ties, not structural ones.

Harris uses non-circular shifts (−N..N) and has no minimum-shift or exclusion concept.
There is no lag scan and no circular group.

## 4a. Cliff et al. (Phys Rev Res 2021): classification **C**

The paper covers analytic tests (F, χ², exact finite-sample) for linear dependence. Its
surrogate section, App. A.3 "Surrogate-distribution tests", sets empirical surrogates
aside:
> "As such, we consider a comparison to these empirical approaches outside the scope of our paper."

It has nothing on minimum p-values, surrogate counts or lag ranges.

## 4b. IDTxl `stats.py`: classification **B (software precedent for resolution check)**

```python
def check_n_perm(n_perm, alpha):
    """Check if no. permutations is big enough to obtain the requested alpha.
    Note:
        The no. permutations must be big enough to theoretically allow for the
        detection of a p-value that is smaller than the critical alpha level.
        Otherwise the permutation test is pointless. The smalles possible
        p-value is 1/n_perm.
    """
    if not 1.0 / n_perm < alpha:
        raise RuntimeError(... "The number of permutations must be greater than 1/alpha.")
```

It is called inside `_find_pvalue`, i.e. at test time on the realized null distribution.
This is the enforced 1/n check. It does not account for lag scans, structural ties, or the
circular group.

---

## Summary table

| Source | L/n floor for lag scan plus circular null? | Closest statement | Class |
|---|---|---|---|
| Cannistra et al. 2025 | No | "at least 19 surrogates are needed to achieve p = 0.05"; all circular shifts plus tailored lags used, floor not discussed | B (weak) |
| Yuan & Shou 2024 | No; same-form bound for Bonferroni multi-lag TTS | "a multi-lag TTS test with m lags requires a truncation radius of at least m/α−1"; periodic many-way-tie floor (S1 section 11) | B+ (explicit same-form bound, different mechanism) |
| Harris 2020 | No | reject iff m ≤ α(N+1); larger N for imprecise timing | B |
| Cliff et al. 2021 | No | — | C |
| IDTxl | No | enforces 1/n_perm < alpha | B (software) |

No source is class A.

## Caveat for our own claim

The "exactly L ties" statement needs two conditions:

1. The lagged statistic is computed on the **same cyclic group** as the null, meaning a circular lag. With truncated-overlap lags, the shifted copies are only approximately equal. The floor is then approximate, and the realized p-value can occasionally fall below L/n.
2. The L lags are distinct mod n.

If ties are counted with `>=`, the realized p-value is ≥ L/n when the null is all n
rotations with the identity included. With (1 + #≥)/(1 + n_surr), n_surr = n − 1, this
gives L/n. State the check in exactly these terms.

## Recommended wording for the paper

> Two ingredients of this check are established. Permutation and shift tests cannot resolve p-values below one over the number of null states (e.g., Harris 2020; Cannistra et al. 2025, who note that at least 19 surrogates are needed for p = 0.05), and toolkits such as IDTxl refuse runs with fewer than 1/α permutations. Yuan & Shou (2024) showed that testing m lags with a Bonferroni-corrected truncated time-shift test requires a truncation radius of at least m/α − 1, so wider lag ranges demand longer series. They also showed that structural many-way ties among shifted statistics (for periodic data) can make significance unattainable. [Tool] enforces the analogous constraint for the lag-scan design used with circular-shift nulls. When the statistic is the maximum over an L-element lag set C, computed on the same cyclic group as the n-state circular null, every searched lag c is mapped onto the selected lag c* by the rotation s = c* − c. At least L of the n null states therefore tie with the observed maximum, whatever the data, and the exact p-value is bounded below by L/n. [Tool] evaluates this bound when the plan is compiled and rejects any plan with L/n > α before data are touched. To our knowledge this tie-based bound for a max-over-lags statistic under the full circular group has not been stated before. We claim the bound and its enforcement, not the general observation that lag ranges and permutation resolution constrain attainable significance.

If space is tight, drop the "to our knowledge" sentence and keep the last sentence.
