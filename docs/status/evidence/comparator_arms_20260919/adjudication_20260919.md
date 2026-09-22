# P3 / SelCal — 2026-09-19 adjudication (comparator arms + audit + remedy + literature)

Inputs: results_note.md (audit-corrected), audit_adversarial_20260919.md, remedy_blueprint_20260919.md,
literature_nearest_tools_20260919.md. Internal decision record; not a manuscript. No production code changed.

## What is now established

1. Common practice is miscalibrated on the sealed inputs: best lag + textbook p, a circular null with the
   lag fixed after selection, Bonferroni, and SciPy shuffle each exceed 5% in at least one null cell.
   Full reselection with the circular null does not.
2. The current SelCal default has a structural power ceiling, p >= L/n, plus a finite-B loss. At n=64 with
   L >= 4 no input can ever reject. min_shift > 1 is invalid (13% size at L=8).
3. No valid circular-null test removes the ceiling uniformly (blueprint, proven).

## Adverse literature fact

The method is NOT new. Cannistra, Hoang, Yuan & Shou (eLife reviewed preprint 2025,
doi 10.7554/eLife.108198.1) already show "fixed lag" nulls give unacceptable false positives and
"tailored lags" with all circular surrogates are calibrated; Yuan & Shou (PLOS Biol 2024) warn against
data-selected lags and note that longer series are needed for wider lag ranges. Any claim of a new
method, or of being first to show selection inflation, is withdrawn.

## What SelCal can still honestly claim (candidate, pending the confirmation study)

- Software, not method: a frozen-plan implementation of the published tailored-lag circular test with
  exact full-group enumeration, retained failures and replayable evidence.
- A plan-time attainable-p guard (refuse L/n > alpha; refuse min_shift > 1; report the power cap).
  None of IDTxl, TRENTOOL, JIDT, Tigramite, statsmodels or SciPy warns about lag-overlapping shifts
  (literature report, source-level). This is the most distinctive, testable software increment.
- Executed common-practice comparison (this study), reported with SelCal's power cost.

## Decision

- GO for a bounded fix: exact enumeration + guard, by TDD, then the frozen confirmation study in the blueprint.
- HOLD on block-shuffle fallback until its study passes the pre-set kill rules.
- HOLD manuscript until the fix is confirmed. The manuscript must cite Cannistra et al. and Yuan & Shou as
  the method source.

## Next actions (ordered)

1. Check whether Cannistra et al. released reusable code. If a maintained package already does full-group
   tailored-lag testing, the SoftwareX increment shrinks to the guard + evidence retention; decide then.
2. Author approval to change production code (this run touched none).
3. Implement exact enumeration + guard (TDD); mark prior receipts that depend on changed bytes as historical.
4. Freeze and run blueprint Stages 0–2; then a version-pinned IDTxl run on the same inputs as the executed
   nearest-tool comparator.
5. Only then: paper skeleton (Motivation = selection inflation evidence; Impact = guard + evidence;
   Limitations = ceiling and power cost).

## Update: action 1 done (2026-09-19)

Cannistra et al. code check: the eLife reviewed-preprint XML (elifesciences/elife-article-xml,
preprints/elife-preprint-108198-v1.xml, 87,680 bytes) contains no code/data availability statement and no
GitHub/Zenodo/GitLab/OSF/figshare/Dryad link; it only cites SciPy and statsmodels. Web and GitHub search
found no released package. Result: no located reusable implementation of the tailored-lag circular test.
The SoftwareX increment (reusable, frozen-plan implementation + attainable-p guard + retained evidence)
stands as a candidate. Caveat: absence of a located repository is not proof none exists; re-check the
eLife Version of Record before submission.
