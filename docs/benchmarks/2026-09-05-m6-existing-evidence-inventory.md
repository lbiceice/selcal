# M6 existing evidence inventory — 2026-09-05

Status: `INTERNAL_INVENTORY_ONLY / M6_NOT_EXECUTED`.

This inventory separates executable regression evidence from the unexecuted scientific studies required by `docs/architecture/null_reselection_v2_design.md` section 15. The current ledger still declares **42.00%**, with M6 at **0% / 0 weighted points**. That percentage is a delivery estimate, not a probability of acceptance.

## 1. Identity and scope

- Worktree: `/Users/vincent/.cache/selcal-worktrees/contract-resolution-pearson`.
- Branch/base: `codex/contract-resolution-pearson`, HEAD `94f993bfd5240739f23dd5f5309a51e51034b962`.
- Inspected state: dirty, uncommitted user candidate. HEAD alone does not identify the current implementation. Existing modifications and untracked files were preserved.
- Runtime observation: `2026-09-05T05:50:18.114669+00:00`; test execution timestamp is recorded in section 5.
- Scope: architecture section 15 and its oracle/failure contracts; current readiness ledger; actual oracle, selection and calibration sources/tests; retained local benchmark receipt; benchmark/script/example file inventory. This is not an exhaustive search of external storage, other tasks or unpublished investigator records.
- Only this new Markdown file was authored. Source, tests, shared status/filter documents, contracts and permissions were not edited. No new scientific experiment, dataset, threshold, protocol freeze or official receipt was produced.
- Current journal rules were not researched in this internal inventory. Runtime and memory measurements cannot substitute for scientific accuracy, validity or usefulness evidence. Nothing here supports the claim that SoftwareX only values computational performance.

## 2. Strongest adverse evidence

Section 15 requires strict-null calibration, alternatives, stress/failure envelopes, multi-statistic checks, matched comparisons and real-data usability. The current ledger at line 133 records these scientific studies as unexecuted. No corresponding executed study receipt was located in the scoped benchmark/script/example inventory. This is a bounded absence finding, not proof that no evidence exists anywhere.

The exact oracle is independent of the production sampler and transform implementation, but not of every computation whose correctness matters. `src/selcal/exact_oracle_v0.py:22` imports the production selector; lines 107–124 call the bound statistic adapter and `select_family_v2`; lines 224–228 bind the statistic through the production resolution. A shared statistic, preprocessing or selector defect can therefore affect both paths. The small hard-coded and scripted tests constrain particular outputs; they do not remove all shared-path risk.

The design itself limits interpretation: circular `min_shift > 1` enumeration is an algorithm oracle because the restricted set is not a group; block permutations do not establish exchangeability of real nonstationary series (`null_reselection_v2_design.md:640`). Accurate enumeration and plus-one arithmetic do not establish scientific Type-I-error control or causal identification.

## 3. Source-bound evidence matrix

Paths below are relative to the worktree in section 1. Their current hashes are in section 7. `INSPECTED_NOT_RERUN` means executable tests exist and were read; this inventory makes no fresh passing claim for them.

| Evidence question | Current source and actual content | Current evidence class | What it supports / what remains open |
| --- | --- | --- | --- |
| Finite-state circular reference | `src/selcal/exact_oracle_v0.py:127`, `:153`; `tests/test_exact_oracle_v0.py:101`. Explicit integer-index transforms; fixed six-state Pearson fixture expects `3/6 = 0.5`. | `EXISTING_TEST_RERUN_PASS` | Supports the fixed fixture and enumeration path. Does not establish that its series satisfy a shift-exchangeability null. |
| Reselection matters | `tests/test_exact_oracle_v0.py:125`. Scripted complete score vectors yield `3/4`; retaining the observed candidate yields `1/2`. | `EXISTING_TEST_RERUN_PASS` | Detects the specified shortcut in the oracle. This is synthetic operator evidence, not an observed scientific performance improvement. |
| State multiplicity | `src/selcal/exact_oracle_v0.py:168`; `tests/test_exact_oracle_v0.py:166`. Enumerates labelled block permutations; six evaluations include numerically repeated arrays. | `EXISTING_TEST_RERUN_PASS` | Supports counting mathematical states rather than unique arrays. Does not establish block exchangeability in any application. |
| Sampler/transform independence | `tests/test_exact_oracle_independence.py:114`, `:159`, `:181`. Production RNG, null bind/token/apply paths and PCG64 are replaced with raising functions; canonical RNG operation calls are traced and must be empty. | `EXISTING_TEST_RERUN_PASS` | Two checked toy cases survive disabled production sampling/transform paths. This is internal code-path independence, not an independent research team, external replication, or independent statistic implementation. |
| Broader independence instrumentation | `tests/test_exact_oracle_independence.py:203` and `tests/_random_behavior_graph_v2.py`. Reachability checks and adversarial graph fixtures exist. | `INSPECTED_NOT_RERUN` | Additional executable safeguards exist. No current full graph-suite pass or general completeness theorem is claimed here. |
| Exact-B finalization and failure bounds | `src/selcal/calibration_v2.py:2832`; `tests/test_calibration_v2_finalization.py:142`, `:172`, `:214`. Scripted finalization uses inclusive exceedance, `(1+E)/(B+1)`, all planned IDs and full reselection. One failed replicate retains `B=3`, gives bounds `0.5`/`0.75`, and leaves p-value and decision null. | `INSPECTED_NOT_RERUN` | Tests exercise the public calibrator with controlled sampler/statistic seams. They support a testable implementation contract, not an empirical failure-rate envelope or calibration study. |
| Observed analytical failure | `tests/test_calibration_v2_failures.py:169`, `:276`, `:291`. Constant-series failure retains the complete raw candidate vector, no selection/p-value/decision and no RNG/replicate execution; generic runtime errors propagate; malformed vectors are integrity failures. | `INSPECTED_NOT_RERUN` | Supports explicit separation of analytical, infrastructure and integrity outcomes. `NOT_EVALUABLE` is not nonsignificance, a null effect or a successful scientific run. |
| Label versus family statistic | `src/selcal/selection_v2.py:83`; `tests/test_selection_v2.py:46`, `:72`, `:100`. Tolerance may choose the first canonical candidate while the decision statistic retains the true family maximum; signed estimates and candidate identities are preserved. | `INSPECTED_NOT_RERUN` | A defined selection contract exists. Empirical selection behavior, lag recovery and alternative power remain unmeasured M6 outcomes. A selected lag alone is not evidence of a direct causal edge. |
| Runtime and memory | `docs/benchmarks/in_memory_standard_20260831.json`. Seven B/C/N cases, three repeats per case, recorded complete outcomes, wall time and traced-memory measurements; one Darwin arm64 single-process environment. | `RETAINED_PRIOR_PERFORMANCE_RECEIPT_READ` | Documents a historical local computational observation. Its receipt/source scheme is not a current scientific-validation identity; the workload was not rerun. No Type-I error, power, comparator benefit, portability or real-case usefulness follows. |
| Strict null, alternatives and stress conditions | `docs/architecture/null_reselection_v2_design.md:1059`; `docs/status/softwarex_readiness_20260831.md:133`. Required scientific studies are listed, but no executed study evidence is recorded there. | `NUMERICAL_SCIENTIFIC_STUDY_NOT_EXECUTED` | No present error-control, power, multi-statistic scientific validity or matched comparator claim. Unit tests and performance repeats are not outer scientific replications. |
| Independent real-case usefulness | Same section-15 requirement and ledger row; scoped scripts/examples provide deterministic demonstrations and benchmarks. | `REAL_CASE_EVIDENCE_NOT_LOCATED_IN_SCOPE` | No located independent reference, practitioner task outcome or adverse-case analysis establishes usefulness. Data provenance, rights/ethics as applicable, task reference and independent assessment remain prerequisites. |

## 4. Strongest supporting evidence and neutral decision

The reusable asset is the executable algorithmic core: separate enumeration/transformation loops, retained state multiplicity, and a scripted counterexample distinguishing full reselection from fixed-candidate reuse. The inspected finalization and selection tests also preserve denominators, incomplete outcomes and the distinction between a selected label and the family maximum.

The adverse side is stronger for any claim that M6 is complete or that scientific validity is established. The supporting side is stronger only for a narrower conclusion: the current implementation provides reusable fixtures and a defined interface on which a prospective M6 study could be built. **M6 remains `NOT_EXECUTED`.** The existing delivery estimate is retained, not recomputed here; no submission-readiness percentage is asserted.

The largest unknown is whether eligible, explicitly justified null mechanisms yield acceptable scientific error behavior while the intended alternatives and real tasks show useful incremental value. Prospective results with retained failures and matched comparisons could change that conclusion. Correct toy outputs, more structural tests, faster runtime or a clean package alone cannot.

## 5. Fresh bounded regression observation

Runtime: CPython **3.11.12**, NumPy **2.4.6**, pytest **8.4.2**, `macOS-26.6.2-arm64-arm-64bit`. Import origin was checked as the current worktree's `src/selcal/__init__.py`; this was not an installed-release evaluation.

Working directory: the exact worktree in section 1. Actual ordered command:

```text
/Users/vincent/.cache/selcal-worktrees/contract-resolution-pearson/.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_exact_oracle_v0.py::test_normative_circular_pearson_table_is_one_half_with_explicit_index_loops tests/test_exact_oracle_v0.py::test_scripted_full_reselection_is_three_quarters_not_fixed_candidate_half tests/test_exact_oracle_v0.py::test_block_oracle_uses_labelled_permutations_and_retains_numeric_multiplicity tests/test_exact_oracle_independence.py::test_circular_oracle_survives_all_production_paths_raising tests/test_exact_oracle_independence.py::test_block_oracle_survives_all_production_paths_raising
```

The direct execution returned `5 passed in 0.07s`, exit 0. The same five tests were replayed once solely to capture stdout and stderr separately; this is not ten distinct tests. That capture began at `2026-09-05T05:52:12.986392+00:00`, returned exit **0**, and measured **0.163389 s** around the subprocess. Actual stdout:

```text
.....                                                                    [100%]
5 passed in 0.07s
```

Actual stderr was the empty string. The quoted duration is pytest's observed regression duration; it is not a scientific runtime benchmark. No long Monte Carlo, new data generation or study execution occurred. Calibration/failure/selection suites were inspected but not rerun. The 14 listed file hashes agreed before and after the first selected run. No immutable source snapshot or independent human review was created, and this inventory is not an official gate receipt.

## 6. Proposed next scientific work packages

Every row is `PROPOSED / NOT_EXECUTED / NOT_A_FROZEN_PROTOCOL`. Sample sizes, grids, effect strengths, alpha choices, uncertainty methods and acceptance thresholds remain **unset**. Previously disclosed toy cases remain regression/design cases, not blind confirmation.

`B` is the planned within-dataset surrogate count; `R` is the independent outer dataset/task count. Keep these denominators separate. Preserve all attempts, evaluability and failure classes; do not convert unevaluable cases into non-rejections or silently discard infrastructure/integrity failures.

| Package | Proposed estimands and denominators | Negative controls and falsification | Prerequisites / interpretation boundary |
| --- | --- | --- | --- |
| M6-P1 — Independent exact references | Disagreement in score vectors, labels, maxima and exact exceedance counts over eligible cases/states, retaining multiplicity. Finite-B p-values need a separate sampling comparison. | Fixed-candidate reuse, omitted identity/states, array deduplication and using the tie representative as maximum. | Independent statistic/selector calculations, source identity and matched support. Algorithm agreement is not exchangeability evidence. |
| M6-P2 — Eligible strict-null calibration | With `E` evaluable datasets and `K` rejections, report `E/R`, conditional `K/E`, failures and uncertainty over independent outer datasets; retain each planned `B`. | Deliberate identity exclusion/fixed-candidate reuse; justified valid reference. Keep non-group and confounded stress cases outside strict-null cells. | Explicit null/transform invariance justification and prospective grid, seeds, uncertainty and decision rules. |
| M6-P3 — Alternatives and comparison | Paired family-level rejection/power and evaluability differences over the same `R` datasets; lag recovery only where truth is identifiable. Proposed comparator: Bonferroni-adjusted per-candidate surrogate testing at matched family endpoint/support. | Zero-effect, tie and sign cases; fixed-candidate reuse labelled a flawed control. | Independent comparator, matched transformation distribution/estimand and known alternative truth. No current superiority or power result. |
| M6-P4 — Stress, failures, multiple statistics | Failure/evaluability frequencies over `R`; observed versus replicate failure stages; retained-B and orchestration invariants for Pearson and binned NetTE. | Common driver, bidirectionality, mixing, feedback, nonstationarity, constant inputs and transform-ineligibility. | Explicit claim per condition, justified generators, preserved vectors/tokens and adverse results. These are not automatically strict-null or causal-validity tests. |
| M6-P5 — Real-case usefulness | Practitioner task success/failure and effort on independent cases/users/tasks; actual endpoint/reference remains unset. | Unsupported/insufficient cases, blinded comparison where feasible, and cases with no added benefit. | Authentic data/rights, ethics or consent where applicable, independent task/reference authority and usable report route. Demonstrations and model review are not external usefulness evidence. |

P1/P2 are prerequisites to stronger calibration claims. M3/M4 persistence and evidence interfaces remain dependencies to assess with their owners. This inventory authorizes no execution and freezes no protocol.

## 7. Current file identities and replay limits

SHA-256 values below were measured from current local files, not copied from old chat status. They are inventory identities, not immutable release identities. Numeric fixture outputs cited above belong to those existing tests/design examples.

| Relative path | SHA-256 |
| --- | --- |
| `docs/architecture/null_reselection_v2_design.md` | `18d568d3c48f8f1eee9ef73e2c9b5771f7d6948b33301939f2f8a55829809554` |
| `docs/status/softwarex_readiness_20260831.md` | `c79ae0dacecda8a3c2db41a2e1d05840852c10b8c8a975927002ccc5e3c53e0c` |
| `src/selcal/exact_oracle_v0.py` | `ffbf002949a9a7530fa4a99aa62bd6125515866533c176f9306754d93b9aade7` |
| `src/selcal/selection_v2.py` | `4361292a9f75db3c28f22a557ce03631210b8af21a5c7ce28d91410c95d51c1e` |
| `src/selcal/statistics/lagged_pearson.py` | `8da53359f3dcbeba0f64648444b435f6773a218265f6c719111cdc6c9804426f` |
| `src/selcal/statistics/binned_nette.py` | `d99f4e4e2767dd10efafe8a84073b72cd827eff0510cb8b400f98c349877efa9` |
| `src/selcal/calibration_v2.py` | `a5249d5facfbcfa8f28b98a70115dbd5ae197e9c1743796fb2fe7e32371e3900` |
| `tests/test_exact_oracle_v0.py` | `8d851e83e2616dda5b4110275f927720c4c7f5558617a10a477f01ac339bfd33` |
| `tests/test_exact_oracle_independence.py` | `717b854ba68d8f2fe9beca82d981caf14b0d55354cbe0c2d15fcb36f00d57b43` |
| `tests/_random_behavior_graph_v2.py` | `2f6229bbc696f6d27ee534ea944f69fe9614bcad67347a805b2ea1fca3055374` |
| `tests/test_calibration_v2_failures.py` | `493b4302510f3af63ffd18c2f6f15447c2df02ea29e18414b7be69390810a03b` |
| `tests/test_calibration_v2_finalization.py` | `99c9ffdee4ccc77ee7c5b0c5336fd487ecac212e43e54a308d905381fe220287` |
| `tests/test_selection_v2.py` | `9b4289d5deaa2ddb702e9ca826c3b76a7f06cc538600a0481d481ec17a5dde77` |
| `docs/benchmarks/in_memory_standard_20260831.json` | `9b1752cef5301e9a799488981b5d08c4f64b2be0c059b38d4e585611944dacd9` |

A supplemental fingerprint covered the current **32** `src/selcal/**/*.py` paths: `1f9e51e65a3edd9ba58278efd10f74622261b47eec252f64c0e256ca083e1ff1`. Its scheme is exactly the final SHA-256 of the textual output of the following command, executed at the worktree root:

```text
rg --files src/selcal -g '*.py' | sort | xargs shasum -a 256 | shasum -a 256
```

This fingerprint scheme differs from the retained benchmark's `installed_python_sources_v1` scheme; their digest strings must not be compared as proof of drift or equivalence. The supplemental fingerprint is reproducible only with the same path-list/text formatting; the per-file identities above remain the direct evidence bindings. No current full-suite, cross-platform, clean-install, immutable-source, official-review or scientific-study closure follows from this inventory.
