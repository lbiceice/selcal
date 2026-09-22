# Remedy blueprint: circular-shift power ceiling under lag search (2026-09-19)

Status: DESIGN ONLY. Written after E1/E2 and after `audit_adversarial_20260919.md`. No code, no
computation and no production change come from this document. Section 7 becomes a frozen protocol
only when its sha256 is recorded in a separate commit, before any Stage-0 computation.

Each claim is labelled **[PROVEN]**, **[AUDIT-VERIFIED]** or **[CONJECTURE]**:
- **[PROVEN]** means an elementary argument is given here.
- **[AUDIT-VERIFIED]** means the claim was checked numerically in the adversarial audit.
- **[CONJECTURE]** means a simulation has to settle it.

Inputs read: `results_note.md`, `protocol.md`, `exploratory_E2_plan.md`,
`audit_adversarial_20260919.md`, `src/selcal/nulls/circular_shift_v2.py`,
`src/selcal/nulls/block_shuffle_v2.py`.

---

## 0. Methodology framing

- **Paradigm:** positivist and design-based. The question is whether a test has exact or asymptotic
  size and what power it can reach. Validity comes from randomization and group invariance.
  Simulation covers only what the proofs cannot.
- **Method:** analytical derivation plus a frozen Monte Carlo study, reported under ADEMP (Morris,
  White & Crowther 2019, *Stat Med*). No EQUATOR guideline applies.
- **Human-subjects administrative status:** not applicable. The study uses synthetic series only.
- **Preregistration:** the frozen Section 7 is the internal preregistration, following the
  `protocol.md` convention. An OSF deposit is optional. Completed-artifact declaration:
  `not_provided`.
- **Cross-model checkpoint:** not run.

## 1. Setting and the profile identity

**Setting.**
- x and y have length n. W is the candidate lag set, with |W| = L (here W = {1..L}).
- The target window is fixed: τ = {L, ..., n-1}.
- Rotation is a right shift, (rot^s x)[i] = x[(i - s) mod n], as in `_apply_state` of
  `circular_shift_v2.py`.

The circular lag profile is g(u) = Pearson over t in τ of (x[(t - u) mod n], y[t]), for u in Z_n.

**P1 [PROVEN]: profile identity.** r_l(rot^s x, y) = g(l + s mod n). The pairs used are
x[(t - l - s) mod n] with y[t] over the same τ, and those depend only on l + s. So

    T_s := T(rot^s x, y) = max_{l in W} g(l + s)   (the sliding-window maximum of one profile)

The whole circular null is the rank of one window-maximum among the n cyclic window-maxima of g. A
different fixed window or padding choice leaves this structure unchanged.

**Engineering corollary.** The exact null over all n states costs n profile correlations and one
sliding max. That is cheaper than B = 199 replicates of L correlations. The profile can be computed
in O(n log n) with an FFT and running sums, so large n is not a problem. The results have no Monte
Carlo noise, and ties are canonical by construction.

## 2. Why the full cyclic group is exact and the restricted set is not

### 2.1 Full group [PROVEN]

**H0_circ:** x is independent of y and the law of x is rotation-invariant, so
(rot^s x, y) =d (x, y) for all s. The sealed iid and circular MA(2) cells satisfy H0_circ exactly.
An ordinary stationary x satisfies it only approximately, with one wrap junction.

- **Exact enumeration.** p = #{s : T_s >= T_0}/n. G is a group, so the reference multiset
  {T(g h z)} equals {T(g z)} for every h. Every point of an orbit therefore sees the same
  reference set, and at most ⌊αn⌋ points per orbit can have p <= α. Averaging over orbits by
  invariance gives P(p <= α) <= α (Lehmann & Romano, *Testing Statistical Hypotheses*, Thm 15.2.1).
- **Monte Carlo with replacement.** p = (1+E)/(B+1), with g_i drawn iid uniform on G, is valid
  (Hemerik & Goeman 2018, JRSS-B). The step that needs closure is this: g_i g_0^{-1} is again iid
  uniform on G, which makes (T_0, T_{g_1}, ..., T_{g_B}) exchangeable.

### 2.2 Restricted shifts [PROVEN invalid; AUDIT-VERIFIED magnitude]

**Why S is not a group.**
- S = {0} ∪ [m, n-m]. This covers E2 variant V (m = L) and production `circular_shift_v2(min_shift=m)`,
  whose state count is n - 2m + 2.
- S is not closed under composition. For example, L + (n - 2L + 1) = n - L + 1 is not in S. The
  only subgroups of Z_n are dZ_n with d | n.
- Without closure, g_i g_0^{-1} is not uniform on S, and the exchangeability step fails.

**Mechanism.**
1. If the global maximum of g is unique (almost surely for continuous data), exactly L of the n
   windows contain it.
2. Under H0_circ, averaging over the orbit therefore gives
   P(observed window holds the global max) = L/n exactly. The audit simulated 0.0309, 0.0624 and
   0.1255.
3. In that event, the other L - 1 tied windows are exactly the excluded shifts |s| < L.
4. So the observed statistic is the unique maximum of its reference set,
   p = 1/(n - 2L + 2) (or 1/(B+1) with Monte Carlo), and the test rejects.

Size is therefore at least L/n whenever 1/(n - 2L + 2) <= α.

**Audit sizes (iid).**

| L | Size |
|---|---|
| 2 | 6.1–6.4% |
| 4 | 6.5–7.3% |
| 8 | 13.0–13.4% |

**`min_shift > 1` is invalid in production [PROVEN, AUDIT-VERIFIED].**
- Under lag search the size of `circular_shift_v2(min_shift=L)` is 13.2% at L = 8.
- The same argument applies even at L = 1: a cluster of m adjacent top profile values gives size
  m/n, because each cluster point excludes the others from its reference set.
- Treat every `min_shift > 1` as currently invalid.
- The sealed study used min_shift = 1, so it is unaffected.

## 3. The ceiling: exact form, finite-B form, and an impossibility result

**P2 [PROVEN, AUDIT-VERIFIED 0/1,200 failures at L = 2, 4, 8].** g(lag*) lies in window W + s
exactly when lag* - s is in W. There are |W| = L such values of s, whatever lag* is:
- s = 0..lag*-1: identity plus positive shifts;
- s = n-1..n-(L-lag*): negative shifts.

Each of these states reproduces the observed r bitwise, so

    p_exact >= L/n   for every input.

At n = 64 the exact test cannot reject at L = 4 or L = 8 for any input (1,200/1,200). The
results note's L - lag* + 1 and 418/800 / 609/800 are superseded (audit §3).

**Finite-B ceiling [PROVEN].** For B = 199, the test rejects iff E <= 9. The L tied states count
in every replicate that draws them, so E stochastically dominates Bin(B, L/n). The maximum
rejection probability is

    π_max(n, L, B, α) = P(Bin(B, L/n) <= ⌊α(B+1)⌋ - 1)

With B = 199 this gives 90.4% (L = 2), 19.8% (L = 4) and about 0.01% (L = 8). The observed rho .6
powers sit at these ceilings [AUDIT-VERIFIED].

**P3 [PROVEN]: no test escapes the ceiling uniformly under H0_circ.** Take a random-phase law
x = rot^U v with U uniform. This law is in H0_circ, and on it any level-α test rejects at most
⌊αn⌋ of the n orbit points. For a single-peak profile, the L peak-in-window points are the ones an
analyst wants to reject. If L > αn, some of them must be accepted. Power gained at some true-lag
positions is paid for at others. So under H0_circ a remedy can only:
- quantify the ceiling,
- remove the finite-B part of it,
- move it between lags by a prior preference, or
- randomize.

Removing the n-state ceiling itself needs a larger invariance group, which means a stronger null
assumption.

## 4. B choice, mid-p and randomized ties: the three questions raised in audit item (4)

### 4.1 B choice / exact enumeration [PROVEN]
- **When n >= L/α.** Here L/n <= α, and B = 199 wastes power: π_max = 90.4% at L = 2, n = 64.
  - Exact enumeration makes π_max = 1 in the strong-signal limit and costs nothing in validity,
    because it is the exact test.
  - Increasing B also works in this regime: B = 999 gives π_max ≈ 99.9% (normal approximation).
    Enumeration dominates, though. It is cheaper, has no Monte Carlo noise, and needs no B in the
    plan.
  - Sealed evidence: 17 of the 18 sealed rho .6 nonrejections have exact numerator 2/64 <= .05.
    Under exact enumeration those would reject, taking power from 91.0% to 99.5% (199/200) at
    L = 2. This follows from the sealed `reference_exact` table and is AUDIT-VERIFIED for the
    numerators. It is still to be recomputed as endpoint E-C0 in Section 7.
  - Most of the like-for-like deficit against Bonferroni at L = 2 is therefore a B artifact, and
    it can be fixed.
- **When n < L/α.** Here a larger B makes power worse. π_max → 0 as B → ∞, because the Monte Carlo
  test converges to the exact test, which cannot reject. The 19.8% at L = 4 is Monte Carlo luck,
  not evidence.
- **Conclusion.** The choice of B is not a remedy for the n-state ceiling. It only fixes the
  finite-B ceiling.

### 4.2 Mid-p [PROVEN invalid exactly where it would help]
p_mid = (E_> + ½E_=)/n, with the identity counted in E_=.

In the global-max event (probability L/n under H0), E_> = 0 and E_= = L, so p_mid = L/(2n):
- If L <= 2αn, that event alone rejects, so size >= L/n. At n = 64, L = 4 this is 6.25% > 5%.
- If L > 2αn (for example L = 8), mid-p still cannot reject.

Mid-p therefore gains power only in the band αn < L <= 2αn, and it is invalid there. At L <= αn
(L = 2), whether mid-p inflates size is [CONJECTURE]; standard theory says mid-p is not guaranteed
valid. It is rejected as an option.

### 4.3 Randomized tie-breaking [PROVEN exact; power capped]
p_rand = (E_> + U·E_=)/n, with U ~ Unif(0,1] and exact enumeration. Its size is exactly α.

In the global-max event, p_rand = U·L/n, so the test rejects with probability min(1, αn/L). For
strong single-lag signals the power cap is therefore:

| L | Power cap at n = 64 |
|---|---|
| 2 | 100% |
| 4 | 80% |
| 8 | 40% |

**Costs.**
- The decision depends on an auxiliary coin. It is reproducible only through a seed bound to the
  plan hash, and two analysts with the same data can disagree.
- A Monte Carlo variant needs care. Keep it to exact enumeration.

**Deterministic counterpart [PROVEN exact].** A pre-specified lag priority uses the statistic
(max value, −argmax position) compared lexicographically. Its floor is lag*/n. It has full power at
preferred lags and none at lag L. Averaged over a uniform true lag, its power is about αn/L, the
same as the randomized test. That is P3 in action.

## 5. Candidate remedies (summary)

| Remedy | Validity | Ceiling effect | Cost | Contract change |
|---|---|---|---|---|
| (a) Attainable-p guard | none needed; the test is unchanged [PROVEN] | quantifies p_floor = L/n and π_max; refuses when p_floor > α and flags when α/4 < p_floor <= α | lives in the plan compiler/runner, because the null class does not know W | add `attainable_p_floor`, `max_attainable_rejection`, `guard_outcome` {PASS, FLAG_POWER_LIMITED, REFUSE_UNATTAINABLE, REFUSE_NON_GROUP}; add disabled reason `ATTAINABLE_P_ABOVE_ALPHA` |
| (b) Window, padding or segments | padding breaks invariance; subgroups dZ_n are exact | no uniform gain: worst-case floor is ⌈L/d⌉·d/n >= L/n [PROVEN] | fewer states | none; dZ_n is the valid substitute for min_shift if near-identity avoidance is wanted |
| (c) Quotient of coincident states | INVALID: the global-max event gives size >= L/n [PROVEN] | — | — | forbid |
| (d) `block_shuffle_v2`, d >= L | exact under block-exchangeable x, including iid x with any y [PROVEN]; approximate under dependent x, with K−1 junctions [CONJECTURE: size acceptable at d = 8] | removes the n-state ceiling: floor max(1/K!, 1/(B+1)); no systematic ties | weaker guarantee in the autocorrelation cell behind SelCal's value claim; requires d \| n and K >= 4 | no new null code; plan records d, K, the d-rule and a validity label |
| (e) Randomized tie-break (exact enumeration) | exact size α [PROVEN] | recovers up to min(1, αn/L) | decision depends on an auxiliary coin | new `tie_mode = randomized`, with a seed derived from the plan hash |
| (e′) Lag-priority statistic | exact [PROVEN] | floor lag*/n | power only at preferred lags | `decision_statistic` becomes a pair |
| (f) Exact enumeration, circular group | exact [PROVEN] | removes the finite-B ceiling; the exact n-state ceiling L/n remains | none; cheaper than Monte Carlo | `p_mode = exact_enumeration`, no B; the sealed plan already stores `reference_exact` |

**Frozen d-rule for (d) [CONJECTURE]:** d is the smallest divisor of n with
d >= max(L, ⌈√n⌉), and K >= 4. This gives d = 8 at n = 64 and d = 16 at n = 256.

## 6. Recommendation

1. **Primary remedy: (f), exact enumeration of the full cyclic group with canonical ties.** It is
   proven valid, needs no new null assumption, and removes the finite-B share of the power loss.
   That share is most of the deficit against Bonferroni at L = 2: power goes to about 99.5%
   instead of 91%. It also makes the guard's floor an exact statement.
2. **Guard: (a), mandatory.** It REFUSES plans with L/n > α (n < 20L at α = .05). It refuses
   `min_shift > 1` as non-group (REFUSE_NON_GROUP). It reports π_max whenever a Monte Carlo mode
   is still used.
3. **Route for refused plans (not auto-switched).** The refusal message offers:
   - (d) `block_shuffle_v2` with the d-rule, **only if Section 7 passes**, labelled as approximate
     under dependent x;
   - or (e) randomized ties as an exact opt-in with the stated cap.

   The user adopts either one as a new explicit, hash-bound frozen plan. The route depends only on
   (n, L, α), so the choice is ancillary.
4. **Manuscript.** Report P2, the ceiling table, P3 (the impossibility result), the `min_shift`
   defect, and that block-shuffle validity under dependence is empirical.

## 7. Minimal confirmation study (to be frozen): `remedy-confirm-v1`

**Common settings.**
- Test: one-sided upper, max_upper with ties to the smallest lag, α = .05, reject iff p <= .05.
- Lags and window: W = {1..L}, τ = L..n-1.
- Seed: int(sha256("SelCal/remedy-confirm-v1|{stage}|{cell}|{index}|{arm}|L{L}")[:16], 16), PCG64.
- No reruns and no added cells.

### Stage 0: deterministic, sealed inputs
- **G0.** The `protocol.md` gate: observed T and lag match the sealed values within 64 ulp.
- **G1 (P1).** For all 1,200 inputs and L in {2,4,8}, T_s from explicit rotation equals the
  profile sliding max in all 64 states, within 4 ulp.
- **G2 (P2).** The canonical tie count is L for all inputs. This repeats the audit and is expected
  to pass.
- **E-C0.** Exact-enumeration decisions at L = 2 from the profile must reproduce the sealed
  `reference_exact.numerator` in 1,200/1,200 inputs. Report the exact-enumeration power at rho .3
  and rho .6.
- **G3.** π_max(64, L, 199, .05) must equal 90.4%, 19.8% and about 0%, and every A5/A0 power must
  be <= π_max + its 95% Clopper–Pearson half-width.
- **Kill K0.** Any G failure stops the study.
- **Pass P-f (primary remedy).** Exact-enumeration size in both sealed null cells has a
  Clopper–Pearson lower bound <= .05, and rho .6 power at L = 2 is >= 95%.

### Stage 1: sealed n = 64 inputs
Cells: iid null (400), circular MA(2) null (400), rho .3 (200), rho .6 (200); L in {2,4,8}.

| Arm | Definition | Role |
|---|---|---|
| C0 | circular, exact enumeration | primary remedy |
| C1 | production `block_shuffle_v2(d=8)`, B = 199 | if production cannot run L = 4/8 plans: production at L = 2 plus re-implementation at 4/8, labelled |
| C1r | block re-implementation | sanity |
| C3 | randomized ties, exact enumeration | descriptive only; exact by proof |
| C2 | Bonferroni-parametric (A2) | comparator |

**Endpoints.** K/R, rate and 95% Clopper–Pearson interval per arm and cell; exact McNemar tests of
C1 vs C0 and C1 vs C2.

**PASS S1** requires all of the following:
- C1 in both null cells at every L has CP lower bound <= .05 and point estimate <= .075
  (Bradley's liberal bound).
- C1 rho .6 power is >= 80% at L = 8.
- C1 beats C0 at rho .6 by McNemar (two-sided p < .05) at L = 4 and L = 8.
- C1 and C1r null-cell intervals overlap.

**Power note.** The sealed null cells (R = 400) cannot detect true sizes around 6–7%. The audit
showed this for A3. Stage 2 is therefore required before (d) is adopted, not optional.

### Stage 2: new generation, only if S1 passes
**Why it is needed.** The sealed nulls are circular, the sealed signal is at lag 1 only, and
R = 400 is underpowered for size.

**Design.** n in {64, 256}; L in {2, 8}; d = 8 and d = 16 respectively; arms C0, C1, C2 and C3.

**Null cells, R = 2,000 each** (CP half-width about ±1 percentage point):
- iid
- non-circular AR(1) with φ = .5 in both x and y
- circular MA(2), at n = 256 only

**Alternative cells, R = 400 each.** The true lag is 1 or L. rho = .6 at n = 64 and rho = .3 at
n = 256.

**PASS S2** requires:
- the same size rule for C1 in every null cell;
- C1 power at true lag L (n = 64, L = 8) >= 50%;
- C0 power > 0 at n = 256, L = 8, where the guard predicts PASS because 8/256 < .05.

### Kill criteria and budget
**Kill criteria.**
- **K1/K2.** Any C1 null cell has CP lower bound > .05 or point estimate > .075. Then (d) is not
  offered; refused plans get only (e) and the documented limitation.
- **K3.** C1 power at rho .6, L = 8, n = 64 is below 50%. Same consequence as K1/K2.

C0's size under AR(1) is reported but decides nothing.

**Budget.** Both stages are trivial on one core:
- Stage 1: 1,200 × 3 L × (199 + 64) evaluations.
- Stage 2: 10,000 series pairs × 2 L.

## 8. Proven vs conjectured ledger

**PROVEN (plus AUDIT-VERIFIED where marked):**
- P1, the profile identity.
- P2, the tie count L and floor L/n (audit-verified).
- π_max (audit-verified).
- Full-group exactness.
- Invalidity of restricted-set, `min_shift > 1`, quotient and mid-p (band αn < L <= 2αn) tests,
  with the restricted-set and `min_shift` sizes audit-verified.
- Subgroups give no uniform gain.
- P3, no uniform escape under H0_circ.
- Exactness of the randomized and lag-priority tests.
- Exactness of block shuffle under block-exchangeable x.
- The effect of B in both regimes.

**CONJECTURE/EMPIRICAL:**
- Block-shuffle size under MA(2)/AR(1) at the d-rule.
- Adequacy of the d-rule.
- Asymptotic validity of block shuffle for a max-over-lags statistic.
- Mid-p size at L <= αn.
- All power magnitudes other than the π_max caps.
