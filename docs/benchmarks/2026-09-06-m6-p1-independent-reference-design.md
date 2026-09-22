# M6-P1 independent reference Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development or executing-plans to implement this plan task by task. Checkboxes below describe future work, not completed work.

**Status:** `IMPLEMENTATION-DESIGN DRAFT / NOT A FROZEN SCIENTIFIC PROTOCOL / M6 PROGRESS UNCHANGED`.

**Goal:** Independently recompute the current Pearson and binned NetTE candidate vectors, selection, finite transformation tables, and the arithmetic of actual public calibration outputs.

**Architecture:** A small standard-library-only reference package receives primitive inputs and performs its own support construction, statistics, selection, and transformations. A separate comparison driver imports SelCal, runs the actual public API, and compares its results with the reference. The existing V0 oracle is a secondary comparison target; it is not the expected-answer generator.

**Tech stack:** Existing CPython, `math`, `collections.Counter`, `bisect`, `itertools`, JSON, and existing pytest. NumPy remains on the production/driver side. No dependency or public API change is proposed.

## 1. Decision and evidence boundary

The strongest objection to extending the existing oracle is shared failure: `exact_oracle_v0.py` imports `select_family_v2` and binds the production statistic. Independent transforms cannot detect a statistic or selector defect shared by both paths. The strongest case for this work is narrower and concrete: the formulas, support, state identities, and retained public outputs already permit an independent calculation without redesigning SelCal.

Proceed with the small independent implementation below. Do not build a new symbolic mathematics system, reference framework, sampler, or research benchmark. Passing its cases would establish scoped algorithm agreement. It would not establish exchangeability, Type-I-error control, power, external replication, real-case usefulness, or SoftwareX readiness.

The local inventory and architecture sections 4–9 and 15 are the contract sources. The inspected implementation determines current numerical behavior where those sections do not specify the arithmetic. The existing tests supply disclosed regression cases, not blind confirmation. No external literature claim is added here.

## 2. Files and dependency boundary

All paths in this document are relative to `/Users/vincent/.cache/selcal-worktrees/contract-resolution-pearson`.

| Proposed file | Responsibility |
| --- | --- |
| `scripts/m6_p1_reference/__init__.py` | Empty package marker; no public SelCal export. |
| `scripts/m6_p1_reference/core.py` | Primitive validation, support indices, scalar Pearson, observed edges, coding, dictionary CMI/NetTE, and selection. |
| `scripts/m6_p1_reference/enumerate.py` | Labelled state enumeration/application; complete table and supplied-schedule summaries. |
| `scripts/compare_m6_p1_reference.py` | Production imports, construction of the real request/pair, result projection, comparisons and bounded comparison output. |
| `tests/test_m6_p1_reference_core.py` | Algebraic formula, support, bin, selection and failure tests. |
| `tests/test_m6_p1_reference_enumeration.py` | State membership, identity, multiplicity, exact count, cap and shortcut tests. |
| `tests/test_m6_p1_reference_public_api.py` | Actual public API comparison and import-independence tests. |

Reference modules may import one another and the standard library only. They must not import `selcal`, NumPy, SciPy, the existing oracle, production support/helpers, existing test-oracle helpers, or the comparison driver. Expected scores may not be copied out of a production run. Driver-to-reference inputs are only the original primitive fixture specification and, for the explicitly conditional comparison, labelled sampled states. Production scores, selected labels and p-values never become reference inputs.

Keep this package outside `src/selcal`. Do not replace the existing oracle or refactor production paths to make this work easier. This document proposes only these later files; the present task creates only this Markdown document.

## 3. Input and output contract

The reference request is a plain dictionary with exact fields:

```text
source, target: tuples of finite built-in floats, equal nonzero length n
candidates: strictly increasing tuple of positive built-in ints
statistic_name: lagged_pearson_v1 | equal_width_binned_nette_v1
statistic_params: {} | {bins: built-in int >= 2}
selection_rule: max_upper | max_absolute
tie_tolerance: finite built-in float >= 0
null_name: circular_shift_v2 | block_shuffle_v2
null_params: {min_shift: positive built-in int} | {block_length: positive built-in int}
```

Accept all bin counts and finite float64 inputs admitted by the current production execution boundary; dyadic fixtures are the first test cases, not the final supported domain. Reject booleans where integers are required. Do not silently canonicalize, impute, standardize, shorten support, or drop nonfinite values. Input-conversion tests belong to the driver; the reference compares the same float64 values actually supplied to `SeriesPair`, represented with `float.hex()` in retained comparisons.

`enumerate_reference(spec)` returns plain records containing:

- `status`, `failure_reason`, `n`, canonical candidates, `support_n`, independently bound source/target edges for NetTE, and `total_state_count`;
- an ordered `states` tuple: `state_id`, labelled state payload, `is_identity`, transformed source, complete candidate records, selection, and `exceeds_observed`;
- each candidate record: `candidate_id`, signed `estimate` or null, unscored/scored value as appropriate, support count, validity and semantic failure reason;
- each selection: selected index, selected candidate, complete tied-candidate tuple, true family maximum, and selected signed estimate;
- integer `nonidentity_exceedance_count`, unreduced `(numerator, denominator)`, and `p_exact`, or null aggregate fields when any required scan is unevaluable.

Reference statuses are local to this package: `COMPLETE_TABLE`, `NULL_DISABLED`, `ANALYTICALLY_UNEVALUABLE`, or `REFERENCE_RESOURCE_LIMIT`. They are not new SelCal run statuses. Keep the full candidate vector on analytical failure; do not select the valid subset. A failed exact table has no exact p-value. Do not imitate the existing oracle's wrapping of analytical failures into an integrity exception; record that difference when comparing error behavior.

`summarize_schedule(spec, states)` accepts an ordered tuple of labelled states, one per planned replicate ID. It returns every retained scan, `B`, `E`, `F`, and the finite-B result described in section 6. It validates membership and identity independently. It does not generate seeds, tokens or random states.

## 4. Independent calculations

### Common support and Pearson

Set `h=max(candidates)` and use `t=h,...,n-1` for every candidate and both directions. Pearson requires `n-h >= 2`; NetTE requires `n-h >= 1`.

For lag `c`, Pearson correlates `u=(source[t-c])` with `v=(target[t])`. Forward NetTE uses `(source[t-c], target[t], target[t-1])`; reverse uses `(target[t-c], source[t], source[t-1])`. In particular, the conditioning history is lag **one**, not lag `c`.

Implement `pearson(u, v)` with Python scalar arithmetic and `math.fsum`: scale each vector by its own maximum absolute value, center by `fsum(values)/len(values)`, then calculate `fsum(uc[i]*vc[i]) / (sqrt(fsum(uc[i]**2))*sqrt(fsum(vc[i]**2)))`. This is the same Pearson estimand with a separate summation implementation. It does not call `np.corrcoef`, `np.dot`, `np.linalg.norm` or a production helper.

Check source variance before target variance, matching the current failure precedence; preserve per-candidate source/target-zero failures. Check finite intermediates and correlation bounds. The current production clamp permits overshoot only within `32 * 2**-52` of ±1; reproduce that declared boundary explicitly, not by importing its constant. Differences caused by independent summation remain visible under section 7. Arbitrary-precision certificates are optional diagnostics for an actual ambiguous case, not a dependency of this implementation.

### Observed equal-width edges and codes

Bind edges once from each **complete observed series**, before any support slicing or transformation. Use the following scalar construction for the currently inspected NumPy 2.4.6 float64 behavior. This is source-observed numerical behavior, not an asserted cross-version NumPy guarantee:

```python
def scalar_edges(values: tuple[float, ...], bins: int) -> tuple[float, ...]:
    import math

    lo, hi = min(values), max(values)
    delta = hi - lo
    step = delta / bins
    if step == 0.0:
        edges = [((float(i) / bins) * delta) + lo for i in range(bins + 1)]
    else:
        edges = [(float(i) * step) + lo for i in range(bins + 1)]
    edges[-1] = hi
    if not all(math.isfinite(value) for value in edges):
        fraction_step = 1.0 / bins
        fractions = [float(i) * fraction_step for i in range(bins + 1)]
        fractions[-1] = 1.0
        edges = [(1.0 - f) * lo + f * hi for f in fractions]
        edges[0], edges[-1] = lo, hi
    return tuple(edges)
```

After construction classify constant source, unusable source edges, constant target and unusable target edges in that order. Unusable means nonfinite or not strictly increasing. Preserve both role diagnostics where applicable. Reject out-of-observed-range evaluation values with the corresponding semantic role failure. Code each value using `bisect_right(edges[1:-1], value)`: a value exactly on an interior edge belongs to the upper bin; the maximum stays in the last bin. Never add pseudocounts or discard empty cells.

Required edge tests cover bins 2, 3 and another non-power-of-two bin count; exact edges and their adjacent floats; constant ranges; distinct adjacent floats with too many bins; subnormal steps; and finite opposite-sign extrema that trigger the overflow fallback. These are small arithmetic fixtures, not a scientific sample grid. General bins and these branches are required for the full P1 scope even if the first RED uses bins 2.

### Discrete CMI and NetTE

For integer-code triples `(a,b,z)` on `N=n-h` rows, use four independently constructed `Counter` objects. Let `n_abz`, `n_az`, `n_bz`, and `n_z` be their counts. Then:

```text
I(A;B|Z) = sum_(occupied a,b,z) (n_abz/N) * ln(n_abz*n_z/(n_az*n_bz))
NetTE_c  = I(source[t-c]; target[t] | target[t-1])
           - I(target[t-c]; source[t] | source[t-1])
```

Use lexicographically sorted occupied triples and `math.fsum` with natural logarithms. Retain the integer tables as diagnostics for a disagreement. Every occupied count is positive; do not evaluate zero-probability log terms. Match the current CMI rule: values in `[-1e-15,0)` become zero; materially negative or nonfinite CMI is analytical failure. Any NetTE candidate analytical failure yields the full failure vector, matching current adapter behavior. Signed NetTE is retained; absolute values enter only the selection rule.

### Selection

Implement `select(estimates, candidates, rule, tolerance)` independently. Require an entire valid canonical vector; calculate signed or absolute scores, normalize score signed zero, set `A=max(scores)`, form **all** ties satisfying `A-score <= tolerance`, and select the first canonical tied candidate. Return the selected signed estimate separately. No approximate comparator or rounded display value may enter `A`, ties or tail comparisons.

## 5. State enumeration and restrictions

For circular shifting use the complete ordered list `(0,m,m+1,...,n-m)`, cardinality `n-2*m+2`, and `source_prime[j]=source[(j-k)%n]`. `2*m>n` disables the null; equality permits one nonidentity state. Zero is the labelled identity, even when another shift gives identical values.

For blocks require `n % L == 0`, `q=n//L >= 2`, and the current production `q <= 4096` restriction. Count `q!` incrementally. Enumerate `itertools.permutations(range(q))`, retaining all labelled orders; identity is the ascending order. Concatenate each labelled block in its original internal order. Keep the target unchanged in both nulls.

Use the existing exact-enumeration cap of 100,000 states and fail before materializing states or calculating statistics when it is exceeded. That count cap alone is NOT an adequate resource envelope for the retained table specified in section 3; the independent review requirement below must be closed before implementation. Do not switch to Monte Carlo, truncate, deduplicate arrays, fix a tail, exclude sampled identities, or divide by the number of unique arrays. A state-count mismatch prevents aggregate comparison.

Evaluate identity once and each other labelled state once with full candidate scans and reselection. For complete tables:

```text
E_exact = count(nonidentity states with A_state >= A_observed)
p_exact = (1 + E_exact) / total_state_count
```

The state set for `min_shift>1` is not promoted to a group. Even where a transformation group is available, table agreement does not prove the invariance or exchangeability of a data-generating mechanism. Block permutations do not establish exchangeability of real nonstationary series.

## 6. Compare the actual public API without replacing it

The driver uses the real exports `PlanRequestV2`, `resolve_plan_v2`, and `calibrate_selected_family`; `SeriesPair` is imported from `selcal.contracts`. Convert the original fixture to NumPy only on this side. The current entry point takes the exact resolved plan, with no injected statistic, candidate subset or external schedule.

```python
from selcal import PlanRequestV2, resolve_plan_v2, calibrate_selected_family
from selcal.contracts import SeriesPair
import numpy as np

request = PlanRequestV2(
    candidates=(1, 2), statistic_name="lagged_pearson_v1", statistic_params={},
    selection_rule="max_upper", null_name="circular_shift_v2",
    null_params={"min_shift": 1}, replicates=9, alpha=0.05,
    tie_tolerance=1e-12, root_seed=17,
)
pair = SeriesPair(source=np.asarray([0, 3, 1, 2, 4, 5], dtype=np.float64),
                  target=np.asarray([0, 1, 3, 2, 5, 4], dtype=np.float64))
resolution = resolve_plan_v2(request)
actual = calibrate_selected_family(pair, resolution)
```

Those B/alpha/seed literals reuse a disclosed local request pattern; they are regression controls, not study design choices. Add the binary NetTE fixture from section 8 using its own candidate tuple and bins. Do not monkeypatch the sampler/statistic or disable integrity checks in this main comparison.

Compare `actual.observed_results` and `actual.observed_selection` with the independent observed scan. For every member of `actual.replicates`, retain its `replicate_id`, status, `transform_token.state`, identity flag, full `statistic_results` and `selection`. Independently validate the token's mathematical state, transform the original inputs by that state, and recompute the entire reference vector. Verify IDs are exactly `0..B-1` and identities and repeated states are retained. A sampled identity must give exactly the observed production family maximum; compare that without tolerance.

This conditional replay checks what the real API did **given its emitted states**. It does not independently verify seed framing, token ownership digests, PCG64 or sampling uniformity, and it must not be described as independent RNG validation. Existing RNG tests remain a separate evidence stream.

Keep two finite-B tail calculations. The reference computes `I_reference[b] = (A_reference_state[b] >= A_reference_observed)` from its own independently calculated vectors, then `E_reference = sum(I_reference)`. Separately, the driver reconstructs each maximum from the production-reported estimate vector and computes `I_report[b] = (A_report_recomputed[b] >= A_report_observed_recomputed)`, then `E_report_recomputed = sum(I_report)`. Compare every paired indicator and both integer counts **exactly**. A different indicator is a `NUMERICAL_BOUNDARY_DISAGREEMENT` when caused by numerical boundary crossing, even if every estimate passes the score tolerance; it denies whole-case agreement, including when opposing indicator differences leave the total counts equal.

Checking the reported `exceedance_count` against `E_report_recomputed` and its `(1+E_report_recomputed)/(B+1)` arithmetic is a separate production-output internal-consistency check. It never substitutes for independent statistic or tail validation. For complete runs also calculate the reference `(1+E_reference)/(B+1)` and its `p<=alpha` decision, and compare them exactly with the production result. Use neither candidate tie tolerance nor score-comparison tolerance in either tail calculation.

Retain separate reference and production coverage/failure ledgers for every planned ID, including each side's candidate validity, failure stage and reason. Derive each side's `F` from its own calculation; do not borrow production failure labels as reference truth or compare only the jointly successful subset. An unevaluable state has a null tail indicator, not `False`; compare validity first and keep any disagreement unresolved. When the observed scan is valid but a side has `F>0`, its `E` counts exceedances only among its own valid replicates, all planned `B` rows remain, p-value/decision stay null, and its bounds are `(1+E)/(B+1)` and `(1+E+F)/(B+1)`. Compare paired validity, valid-state indicators, `E`, `F` and bounds exactly; mismatched coverage prevents whole-case agreement. Observed analytical failure or null disablement is compared independently as its own terminal stage, not a non-rejection.

For **all-state** coverage, the driver separately binds the real statistic once on the observed pair, calls `evaluate_all` and `select_family_v2` on every independently generated state, and compares each row with the independent table. This is a component comparison; it does not pass through the public calibrator. The old `exact_state_oracle_v0` may also be compared for its three aggregate fields. The reference remains free of those imports.

Do not require finite-B p-values to equal enumeration p-values. The public API has no complete-enumeration schedule parameter, and sampling all states by searching seeds would add a different experiment. State explicitly which of component all-state coverage and public-API sampled-state coverage was obtained.

## 7. Numerical comparison and actual unresolved choices

Separate numerical estimates from discrete decisions:

| Field | Proposed comparison rule |
| --- | --- |
| Candidate/state IDs, support, validity, labelled multiplicity, counts | Exact equality. |
| NetTE bin edges/codes and count tables | Exact equality of edges/codes/counts on the inspected runtime; never accept a bin change because edges are numerically close. |
| Signed estimates and score magnitudes | Fixture-level scalar comparison with `rel_tol=0.0`, initial `abs_tol=64*math.ulp(1.0)`; retain raw hexadecimal values and residuals. This is a proposed engineering budget, not a scientific success threshold. A failure is retained, not repaired by widening the budget. |
| Label, selected index, complete tie set | Exact equality; a numerical score pass cannot excuse disagreement. |
| True family maximum within production outputs | Exactly recompute `max(e)` or `max(abs(e))` from the reported estimates on the driver side; compare exactly with the reported maximum. This is only production-output internal consistency, never independent statistic or tail validation. |
| Independent tail agreement | Compare every `I_reference[b]` with `I_report[b]` and `E_reference` with `E_report_recomputed` exactly; a score-tolerance pass or equal aggregate count cannot excuse an indicator mismatch. Each side uses its own observed/state maxima and literal inclusive `>=`. |
| Coverage, failures and p-value arithmetic | Independently retain each side's full validity/failure ledger and planned B. Compare coverage before indicators; null indicators are not non-exceedances. Check production arithmetic against its reconstructed E separately from independent reference E/F, bounds, p-value and decision comparison. No tie or score-comparison tolerance enters these checks. |

Two limitations need an explicit disposition in the later comparison result, not more framework work now:

1. **Independent arithmetic near a decision boundary.** Scalar summation can differ from NumPy by a few ulps. If that changes a tie set or a tail indicator, preserve a `NUMERICAL_BOUNDARY_DISAGREEMENT` with both vectors, difference-to-tolerance/tail boundary, and any simple hand derivation. The current contract fixes binary64 inclusive comparison; it does not authorize treating mathematically equal but numerically unequal outputs as an exceedance. Do not silently add a tail tolerance or claim whole-case exact agreement. A production semantic change, if later desired, needs its own concrete review. No such change is necessary to implement and expose the disagreement.
2. **Dependency-specific edge construction.** The scalar construction above was derived from the installed NumPy 2.4.6 implementation, including its subnormal branch. Verify edges/codes against each actually claimed supported runtime before calling that matrix covered. A mismatch in another version is an explicit numerical-contract question, not permission to narrow the final deliverable to bins 2 or dyadic data. Current-runtime implementation can proceed without resolving hypothetical differences.

The lack of a public complete-enumeration parameter is a coverage boundary, not a blocker for conditional public comparison. New sampling theory, precision certificates for every value, a new CLI product and additional scientific grids are optional expansions and are not in this design.

## 8. Disclosed algebraic fixtures and negative controls

All fixtures below are public design/regression cases. None is a holdout or scientific outer replication.

| Fixture | Explicit input/expected result | Defect exposed |
| --- | --- | --- |
| Pearson basic formula | Mathematical values: `pearson((0.,1.,2.),(0.,1.,2.))=1`; reversed second vector gives `-1`; second vector `(1.,0.,1.)` gives `0`; constant first vector fails source variance. Compare numerical estimates under section 7; do not demand bitwise ±1 from a normalized floating-point calculation. | Sign, covariance, constant-input and absolute-score confusion. |
| Existing six-state Pearson case | The pair and candidates in section 6; shifts 0–5; selected candidates `(1,2,1,2,2,1)`; identity plus shifts 4 and 5 exceed; `p_exact=3/6`. | Shift orientation, common support, reselection and omitted states. Compare full signed rows, not only p. |
| CMI copy | `a=b=(0,0,1,1)`, `z=(0,0,0,0)`: `ln(2)`. With `a=(0,0,1,1)`, `b=(0,1,0,1)`, `z=a`: zero. | Marginal information substituted for conditional information; wrong log base. |
| End-to-end binary NetTE | `source=(0,0,1,1,0)`, `target=(0,0,0,1,1)`, candidates `(1,)`, bins 2, observed edges `(0,.5,1)`, support 4. Forward CMI `ln(27/4)/4`; reverse CMI `ln(4)/4`; NetTE `ln(27/16)/4`. Swapping roles negates it. | Reverse indexing, conditioning lag, sign and subtraction. The exact integer count products are 27/4 and 4. |
| Bin-edge boundary | Edges `(0.,.5,1.)`, values `(0., nextafter(.5,0.), .5, nextafter(.5,1.), 1.)` have codes `(0,0,1,1,1)`. | Replacing upper-edge inclusion with lower-edge inclusion. |
| Repeated labelled blocks | Existing source `(0,1,0,1,2,3)`, target `(0,2,1,4,3,5)`, L=2: six labelled permutations, three numerical arrays each appearing twice. | Deduplicating arrays changes the denominator. |
| Selection label/max separation | Estimates `(7/8,1)`, candidates `(1,2)`, tau `1/8`: ties `(1,2)`, label 1, A=1. With `(-1,.5)`, absolute rule, A=1 and signed selected estimate=-1. | Using the representative's score as the family maximum; losing sign. |
| Inclusive tail without tolerance | A_observed=1, state maxima `(1,1-2**-52)`: only the first exceeds even with candidate tau `1/8`. | `>` tail or applying candidate tolerance to the tail. |
| Existing reselection control | Scripted score rows `(3,1),(2,4),(3,0),(1,2)` yield full-family `3/4`, fixed observed candidate `1/2`. Selector/aggregation-only fixture; these are not Pearson values. | Fixed-candidate shortcut. |
| Finite-B separation | For those scripted rows, sampled state IDs `(0,1,1,2,3)` give B=5, E=4, MC p=`5/6`; full enumeration remains `3/4`. | Deduplicating samples, excluding identity, or equating finite-B and full enumeration. |

Additional required controls: candidate-specific rather than max-lag support; empty shift space; nondivisible blocks; state cap before iteration; missing/duplicate candidate records; and one failed scan with retained planned B. For edge freezing, a direct bound-adapter fixture may evaluate a narrower-range pair of the same length: observed edges from `(0,1,2,3)` with bins 2 must still code evaluation values `(0,0,1,1)` as all zero. This off-orbit case is a preprocessing contract test. Rebinding edges on the valid permutation orbit is not a discriminating negative control because these nulls preserve the full source multiset.

## 9. Minimal TDD sequence

Use the existing worktree interpreter. These are commands to run during implementation; none was run as a new test in this design task. Each task begins with an explicit assertion failure for the absent behavior, then the smallest implementation, then the same test and existing affected tests. Use an import probe that reports an assertion about missing behavior, so a misspelled import is not mistaken for useful RED.

- [ ] **1 — Core formulas and support.** Create the core test file first. Assert the Pearson basic cases, support `n-max(candidates)`, the CMI copy/conditional-zero cases, and the binary NetTE count products. Implement the index formulas, scalar Pearson and Counter CMI in `core.py`. Run `.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_m6_p1_reference_core.py` and retain the actual RED/GREEN commands and returns.
- [ ] **2 — Complete bin semantics and failures.** Add failing assertions for the explicit edge/coding fixture, bins 3 and another non-power-of-two count, subnormal and overflow-fallback branches, constant/unusable edges and frozen-edge reuse. Add `scalar_edges`, coding, bound observed edges and full NetTE scans. Run the same targeted command plus `tests/test_statistic_binned_nette.py`. Passing only bins 2 does not complete this task.
- [ ] **3 — Independent selector.** Add failing literal assertions for `(7/8,1)` at tau `1/8`, the adjacent float below `7/8`, signed absolute selection, canonical ties and malformed vectors. Implement `select` directly from section 4. Run the core test file plus `tests/test_selection_v2.py`.
- [ ] **4 — Labelled states and exact tables.** Add the six-state Pearson, block multiplicity, restricted circular membership, cap-before-iteration and scripted reselection assertions to `tests/test_m6_p1_reference_enumeration.py`. Implement the section-5 loops and complete table. Run that file plus `tests/test_exact_oracle_v0.py`. The scripted table must kill the fixed-candidate control; repeated blocks must kill the deduplicating control.
- [ ] **5 — Public API comparison.** Write the driver test against the actual section-6 call before implementing the driver. Require full observed and retained-replicate vector/label/max comparisons for both statistics and both legal null types on the disclosed small fixtures. Implement primitive state projection, independent replay and the section-7 mismatch categories. Run `tests/test_m6_p1_reference_public_api.py`. Add the all-state component comparison separately; do not claim it is a public full-enumeration run.
- [ ] **6 — Finite B, failures and independence.** Add literal `5/6` versus `3/4` schedule assertions and failure-bound assertions before implementing `summarize_schedule`. In a fresh subprocess, import and run the reference after blocking imports whose top-level name is `selcal`, `numpy` or `scipy`; inspect reference imports for production/test-helper dependencies. Run all three new test files together with existing `tests/test_calibration_v2_finalization.py` and `tests/test_calibration_v2_failures.py`. A production-exported expected value is forbidden even if tests pass.

For each negative control, alter a local control calculation or projected comparison record, not production code: wrong shift sign, missing identity, deduplicated labels, fixed candidate, representative maximum, `>` tail, wrong conditioning lag and lower-edge inclusion must produce the corresponding concrete mismatch. Record the control that a fixture actually detects. Do not claim a control was killed merely because it was listed.

After these targeted checks, run the repository's existing lint/type checks on new files and inspect the diff. Separate source-changing operations from hashes and receipts. The later comparison output must identify current source files and hashes, reference files and hashes, runtime, fixture literals, exact commands/exit codes, coverage scope and every adverse or unresolved result. No status percentage, M6 completion or publication label is authorized by this plan.

## 10. Inspected identity and present-task verification

Read at `2026-09-06T12:39:58Z`; worktree HEAD `94f993bfd5240739f23dd5f5309a51e51034b962`, with existing dirty and untracked work preserved. HEAD alone does not identify those bytes. Directly measured source identities:

| Path | SHA-256 |
| --- | --- |
| `docs/benchmarks/2026-09-05-m6-existing-evidence-inventory.md` | `c0efe42b2815cd3a8d12fab432ffdc5cd29454fd367d577f23fc0647a9e4ace5` |
| `docs/architecture/null_reselection_v2_design.md` | `18d568d3c48f8f1eee9ef73e2c9b5771f7d6948b33301939f2f8a55829809554` |
| `src/selcal/exact_oracle_v0.py` | `ffbf002949a9a7530fa4a99aa62bd6125515866533c176f9306754d93b9aade7` |
| `src/selcal/selection_v2.py` | `4361292a9f75db3c28f22a557ce03631210b8af21a5c7ce28d91410c95d51c1e` |
| `src/selcal/statistics/lagged_pearson.py` | `8da53359f3dcbeba0f64648444b435f6773a218265f6c719111cdc6c9804426f` |
| `src/selcal/statistics/binned_nette.py` | `d99f4e4e2767dd10efafe8a84073b72cd827eff0510cb8b400f98c349877efa9` |
| `src/selcal/support.py` | `f54ded5df407a585938bdfb2357977958d513c8523673a27d6a2c9f1e3cda421` |
| `src/selcal/__init__.py` | `8b20c571b3fcc58db16b967e6461bc962bc095aa5268795188d9907c2ad981a7` |

The installed NumPy source read was `.venv/lib/python3.11/site-packages/numpy/_core/function_base.py`, `linspace`, version 2.4.6; source-file SHA-256 `b8b8f508410c567b0ea4b44db18e28eb09c62e9ec33680fcefdea7de82eeb9c1`. Direct inspection initially raised `TypeError` because its dispatcher is not a Python function; retrying with `inspect.unwrap` returned the implementation. No environment was changed.

Only the new binary NetTE fixture's integer arithmetic was checked in a short standard-library calculation: forward product `27/4`, reverse product `4`, ratio `27/16`, support 4, value `0.13081203594113697`. This verifies the disclosed algebra in the draft; it is not a new scientific experiment or an executed P1 comparison. No new tests, scientific run, protocol freeze, source/test edit, dependency change, filter writeback or shared status edit occurred in the present task.

## 11. Independent resource-capacity review — 2026-09-06

`M6-P1-R01 / IMPORTANT / OPEN`: the original 100,000-state cap does not bound the new retained table's size or reference work. Reviewer `/root/m6_reference_design_review` inspected the 31,302-byte preimage, SHA-256 `1fd23424434c170c39d1a3def56f4cc7188dd5820ef94b19b8451637a395fc4d`. Root independently read sections 3/5 and the current product budget formula in `calibration_v2.py` and confirmed this counterexample: `n=100000, C=1, B=1, circular min_shift=1` has product work `B*(C*n+S+n)=200001` with `S=1`, and reference cardinality `n-2*m+2=100000`. Retaining a length-n transformed source for every state requires 10,000,000,000 entries: approximately 80 GB of 64-bit references alone, excluding containers, records and numerical objects. This is a proved capacity-contract gap, not an observed crash; that allocation was not performed. The older streaming V0 enumeration does not justify the new retained-table capacity.

Before reference implementation, specify separate, explicit preflight bounds for retained elements/estimated bytes and total reference work, covering state count times n, full candidate scans, state payloads, and bin/edge allocation. Apply the same admission principle to `summarize_schedule`, including planned B and retained repeated-state records; do not merely protect exhaustive enumeration. Run admission before constructing bin edges, materializing state tables or starting statistic scans. Exceeding any bound must return `REFERENCE_RESOURCE_LIMIT` with the violated bound and null aggregate comparison fields; it is not analytical invalidity, a numerical-domain exclusion, or a successful complete comparison. Preserve the intended finite-float/bin numerical semantics separately from the capacity-limited coverage. Never silently truncate, deduplicate or fall back to Monte Carlo.

Exact new limits and their resource accounting remain to be specified and reviewed; no arbitrary numeric cap is authorized by this addendum. The existing state cap remains necessary but insufficient. This draft is therefore `RESOURCE_ENVELOPE_REVISION_REQUIRED / NOT FROZEN / NOT EXECUTED`, not an approved implementation specification. Product input contracts and product source remain unchanged.

The independent model review reported no other Critical/Important issue in the inspected independent-reference/count/multiplicity/RNG boundaries, and reported 48 small NumPy 2.4.6 edge-arithmetic probes without hexadecimal disagreement. Those are attributed finite diagnostic observations, not root-executed M6 experiments, full-domain proof, blind confirmation, or human-expert evidence. Root has not upgraded M6 completion, SoftwareX readiness or submission status.
