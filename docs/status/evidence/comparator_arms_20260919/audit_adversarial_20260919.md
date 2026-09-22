# Adversarial audit: comparator arms and E1/E2 (2026-09-19)

Scope: protocol.md, amendment 1, run_comparator_arms.py, run_exploratory_E2.py, results*.json and results_note.md, checked against circular_shift_v2.py and the sealed study. No existing file was modified. The scratch scripts a1–a8.py are in the session scratchpad `audit/`. They use the cmpenv venv (numpy 2.4.6, scipy 1.16.2).

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | The arms A1–A5 are implemented as described | CONFIRMED, with one nuance about A4 |
| 2 | A5 matches SelCal's null semantics | CONFIRMED |
| 3 | The p-floor is (L−lag*+1)/64 and the rule is n ≥ 20L | PARTLY REFUTED: the count formula and the "never reject" numbers are wrong, but n ≥ 20L holds |
| 4 | The [L, n−L] variant inflates size | CONFIRMED: the inflation is genuine and is not caused by the RNG |
| 5 | The size comparison is fair and the MISCAL flags are correct | CONFIRMED for the arithmetic, with caveats (A3 under MA(2) is understated) |
| 6 | results_note.md has no overclaims | Several misstatements, listed below |

## 1. Arm implementations — CONFIRMED
- **A1.** It calls `pearsonr(..., alternative="greater")` at the selected lag on window t=2..63 (62 pairs). Because every lag uses the same window, the lag with the largest r is also the lag with the smallest one-sided p, so A1 is the min-p rule.
- **A2.** It is exactly `min(1, L·p1)`.
- **A3.** It uses the same 64 identity-inclusive states and the null r at the fixed selected lag. It matches the protocol.
- **A4 nuance.** SciPy's `pairings` with 2 samples and `n_resamples=199 < 64!²` draws independent permutations of both x and y (checked by instrumenting the statistic and reading `_calculate_null_pairings`). It does not "permute one series relative to the other". Under full i.i.d. exchangeability this is an equivalent and valid null. It still destroys the lag alignment: only 0–3% of lag-1 pairs survive. The protocol wording "SciPy's default i.i.d. permutation null" is correct.
- **Fresh-simulation sizes (L=2, 6,000 reps).** In these reps A4 is re-implemented with independent permutations.

| Arm | iid null | MA(2) null |
|---|---|---|
| A1 | 9.97% | 15.0% |
| A2 | 5.08% | 10.0% |
| A3 | 8.93% | 7.12% |
| A4 | 4.97% | 9.63% |
| A5 | 3.68% | 3.97% |

  Monte Carlo SE is ≈0.28 percentage points. No arm is handicapped by a bug. A2 and A4 are exact under iid, as theory predicts.

## 2. A5 matches SelCal null semantics — CONFIRMED
- **State space.** `circular_shift_v2` has `total_state_count = n − 2·min_shift + 2` states and maps index 0 to identity and index i≥1 to shift `min_shift+i−1`. It applies `source[(t − shift) % n]`, a right shift. With min_shift=1 this gives 64 states {0..63} drawn uniformly with replacement, which equals A5's `x[(t−s)%N]`.
- **Estimates.** Over all 1,200 inputs × 64 states × 2 lags, A5's estimates match the sealed `reference_exact` table to within 4.4e-16.
- **Tie rule.** The sealed plan uses tie_tolerance 0.0 and counts null ≥ obs. The exact numerator (#states ≥ obs) matches the sealed `reference_exact.numerator` in 1,200/1,200 inputs.

## 3. p-floor — mechanism CONFIRMED, formula REFUTED, E2 "never-reject" metric has a bug
- **Analysis.** Under a right shift s, null lag l equals observed lag l+s whenever l+s ≤ L, with no wrap on window t=L..63. Under a left shift (s = 64−k), null lag l equals observed lag l−k whenever l−k ≥ 1. The observed r at lag* is therefore reproduced bitwise in exactly two sets of states:
  - s = 0..lag*−1 (identity plus positive shifts), and
  - s = 64−1..64−(L−lag*) (negative shifts).

  That is **L states in total, independent of lag***. Negative shifts do collide. The E2 plan's "s = 0..(L−lag*)" has the direction wrong: those are the negative shifts. The note's "(L−lag*+1)" count is wrong whenever lag* > 1. It happens to equal L only when lag* = 1.
- **Numerical check.** In all 1,200 inputs at each of L=2, 4, 8, every predicted colliding state reproduced obs bitwise, with 0 failures. The minimum exact p is L/64 (0.03125, 0.0625, 0.125). results_E2.json's own `min_exact_p` field shows the same values.
- **Consequence.** At L=4 and L=8 the exact p exceeds .05 for **every** input: 1,200/1,200, including all alternatives. The note's "418/800" (L=4) and "609/800" (L=8) are wrong. The bug is that `floor_i` only inspects states 0..L (`allmax[:L+1]`), which misses the negative-shift collisions and counts chance exceedances. The same bug gives "1/200 never" for rho .6 at L=4, where the true figure is 200/200.
- **Rule of thumb.** L/n ≤ α ⇔ n ≥ L/α = 20L at α=.05. The rule is correct, but only as the condition for the exact (enumerated) test.
- **Finite B.** With B=199 the Monte Carlo test rejects iff E ≤ 9, where E ≥ Binomial(199, L/64) because the L colliding states always count. This gives a power ceiling of:

| L | Power ceiling | Observed power at rho .6 |
|---|---|---|
| 2 | 90.4% | sealed A0 91.0%, A5 85.5–88% |
| 4 | 19.8% | A5 20% |
| 8 | 0.01% | A5 0% |

  All observed rho .6 powers sit at this ceiling. The 20% at L=4 is pure Monte Carlo luck: with exact enumeration the power would be 0.
- **"Requires n ≥ 20L".** This is therefore not literally true for the shipped Monte Carlo test, which can reject when n < 20L. The statement should be framed as the exact-test condition plus the Binomial ceiling.
- **Sealed rho .6 nonrejections.** There are **18**, not 17. Seventeen have an exact numerator of 2/64 and one (index 141) has 4/64. So the claim "explains the 17" is correct only for those 17.

## 4. [L, n−L] variant inflates size — CONFIRMED genuine
- **The RNG reuse is harmless.** `s_new` continues the same PCG64 stream after `s_old`, and those draws are still i.i.d. uniform. Rerunning V on the sealed nulls with an independent seed gives:

| L | iid null | MA(2) null |
|---|---|---|
| 2 | 32/400 | 24/400 |
| 4 | 36/400 | 29/400 |
| 8 | 60/400 | 46/400 |

  These are within noise of the reported 30/22, 35/27 and 58/45.
- **Fresh iid simulation (20,000 reps).**

| L | V, exact enumeration | V, B=199 | A2 (control) |
|---|---|---|---|
| 2 | 6.09% | 6.35% | 5.05% |
| 4 | 6.49% | 7.27% | 5.02% |
| 8 | 13.0% | 13.4% | 4.9% |

- **Mechanism.** The null statistics are sliding-window maxima of circular cross-correlations. The observed window is the global maximum over all 64 states with probability exactly L/64 (simulated 0.0309, 0.0624 and 0.1255). When that happens, the other L−1 tied states are precisely the excluded shifts |s| < L. V then returns p ≈ 1/(66−2L) and rejects. So V's size is at least about L/64, from a truncated, non-group reference set.
- **The sealed-sample figure overstates L=2.** The note's 7.5% at L=2 is partly sampling noise: the sealed iid cell runs hot, with A2 at 6.0% on the sealed data against a true 5.05%. The true inflation at L=2 is about 6.1–6.4%.
- **Production implication, not in the note.** `circular_shift_v2(min_shift=L)` itself draws from {0} ∪ {L..n−L}. In simulation its size is:

| L | B=199 | Exact enumeration |
|---|---|---|
| 2 | 4.8% | 6.3% |
| 4 | 6.6% | 6.4% |
| 8 | 13.2% | 13.2% |

  SelCal's own min_shift > 1 option is therefore anti-conservative under lag search. It should be documented, or guarded against, next to the floor issue.

## 5. Fairness and MISCAL flags — CONFIRMED arithmetic, with caveats
- **Flag arithmetic.** The CP lower bounds recompute identically for all 24 rows (A1 iid 40/400 → lower .0724, and so on), and the flags follow the rule as frozen. The p ≤ α rule is used consistently across arms.
- **A3 under MA(2) is understated.** Its true size is about 7.1% (fresh simulation), but n=400 was too few to flag it (26/400, lower .043). The note shows A3 as passing the MA(2) cell, which reflects a power limitation, not calibration.
- **A2 and A4 under iid.** Both are exactly valid (5.1% and 5.0% true). Their 6.0% on the sealed data is sampling noise.
- **D2 caveat is misplaced.** The alternative cells use iid z and an iid innovation, a setting where A2 is exactly size-valid. So the A0-vs-A2 power comparison is essentially like-for-like. Most of A0's loss at rho .6 is the B=199 floor ceiling (90.4%), not selection calibration. At L=2, exact enumeration (p = 2/64) or a larger B would largely remove the loss.

## 6. Overclaims and errors in results_note.md
1. The floor formula "(L−lag*+1)" and "about L−lag*+1 states" are wrong. The count is exactly L, via positive shifts < lag* plus negative shifts ≤ L−lag*.
2. The table column "can never reject (exact)" gives 418/800 and 609/800. The true figure is 800/800 at both L=4 and L=8, caused by the `floor_i` bug. The severity is understated.
3. "Rejection requires n ≥ 20L" holds only for exact enumeration. With B=199 the ceiling is Binomial(199, L/n) ≤ 9 (for example 90.4% at L=2).
4. "17 sealed nonrejections" should read 18 nonrejections, of which 17 are at floor 2/64.
5. "Only arm that controls size in both null cells" is true on the true sizes as well (A3 fails both). The note's table, however, implies A3 is fine under MA(2).
6. "Not a like-for-like power win for A2" is wrong for these alternatives, where A2 is valid. SelCal's power deficit at rho .6 is mostly a B/floor artifact, and fixing it is a design choice, not an inherent cost.
7. V's "7.5% at L=2" is inflated by sample noise (true ≈6.1–6.4%). The conclusion (invalid) stands. The note also omits that the production parameter min_shift ≥ 2 has the same defect.
