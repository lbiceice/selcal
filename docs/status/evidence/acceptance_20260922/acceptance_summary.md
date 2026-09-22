# Regression, installation and reproduction acceptance — 2026-09-22

Source state: commit `c08b785` plus this round's uncommitted changes (preflight, fast attainability,
refreshed benchmark receipt). No test was deleted, skipped or weakened to reach this ledger.

## 1. Full regression

| Environment | passed | failed | failures, classified |
|---|---|---|---|
| Python 3.11.12, project .venv (numpy 2.4.6, no docs extra) | 3,607 (+3 benchmark after receipt refresh) | 13 | 12 governance gate + 1 docs build (extra not installed) |
| Python 3.12.10, locked env (numpy 2.5.2, Sphinx 8.2.3) | 3,608 | 15 after receipt refresh | 12 governance gate + 3 portability |
| Python 3.13.12, locked env | 3,608 | 15 after receipt refresh | 12 governance gate + 3 portability |

Benchmark receipt: regenerated at the final source state (`in_memory_standard_20260922.json`); its test
and the plot/docs tests pass (3 + 6).

### Ledger of remaining failures (kept, not deleted)

| Class | Tests | Status | Owner decision needed |
|---|---|---|---|
| Historical governance gate | 12 in `tests/task10/test_authority_amendment_scope_v1.py` | By design fails on any drift from the 2026-08-30 review baseline (git HEAD `94f993b`, file digests). Not a product defect. | Retire the historical gate, or run its successor-baseline procedure. Rewriting its baseline here would rubber-stamp that review. |
| Environment (3.11 dev env only) | `test_documentation.py::test_sphinx_...` | Passes where the declared `docs` extra is installed (3.12/3.13 locked envs). | None; install `.[docs]` to run it. |
| Portability, pre-existing | 3 on Python >= 3.12 (mypy target 3.11 vs numpy 2.5 stubs; `TypeAliasType` in the structure gate) | Fails identically on pre-round commit `724ac6f`. | Constrain numpy < 2.5 and relock, or amend the gate and mypy target (`docs/status/portability_and_hygiene_20260922.md`). |

## 2. Clean installation and end-to-end reproduction

`run_clean_install_acceptance.py` -> `clean_install_acceptance_receipt.json` (`all_passed: true`).
Built wheel and sdist with `uv build`; fresh environments installed from the artifact only (imports
from site-packages, not the source tree); run outside the repository:

| Install | Python / numpy | Sampling example | Exact-enumeration example | Refused plan |
|---|---|---|---|---|
| wheel | 3.11.12 / 2.4.6 | validate, run, verify, replay MATCH, report: all exit 0 | same | validate exit 2 PLAN_NOT_EXECUTABLE; run exit 2 `unattainable_plan`; no record |
| wheel | 3.12.10 / 2.5.3 | pass | pass | pass |
| wheel | 3.13.12 / 2.5.3 | pass | pass | pass |
| sdist | 3.13.12 / 2.5.3 | pass | pass | pass |

Environments not covered: Linux and Windows (no host available here); a CI matrix is still needed for a
cross-platform claim.

## 3. M0/M5 preflight and error messages (item 2)

- `validate` separates `input` / `plan` / `scientific_assumptions`; plan reasons are specific
  (`resource_budget_exceeded`, `REFUSE_*`), warnings mark plans that will end NOT_EVALUABLE, and the
  assumptions are listed as `DECLARED_NOT_VERIFIED`.
- Non-executable plans: `validate` exit 2 with the first reason; `run` refuses before any calibration.
- Oversized replicate counts: the guard added on 2026-09-19 did expensive exact-rational arithmetic
  before the resource check (6.4 s at B = 19,999; unbounded near the 1,000,000 representability cap).
  Fixed: resource check first, power cap in log space. Tests: B = 1,000,000 preflight < 2 s; the core API
  rejects the same plan before any replicate (ResourceLimitError for the sampling null; NOT_EVALUABLE for
  the exact null with B != n - 1).

## 4. Real-task evidence (item 1, author-side)

See `../real_case_20260922/verdict.md`: a published lead-lag significance claim (Yacob et al. 2026,
GeoHealth) re-examined on the authors' CC BY deposit, and a published influenza plan refused by the guard.
This is author-side evidence, not a user study.

## 5. Update after the author's decisions (2026-09-22, later the same day)

- Task10 scope gate retired: `tests/task10/test_authority_amendment_scope_v1.py` is skipped by default
  with a stated reason (52 tests: 12 failing, 40 passing); it still runs unchanged with
  `SELCAL_RUN_RETIRED_GATES=1`. Record: `docs/status/retired_task10_gate_20260922.md`.
- numpy constrained to `>=1.26,<2.5` and relocked. The only lock changes: numpy 2.5.2 removed and
  same-version digest changes for numpy 2.4.6, contourpy 1.3.3, matplotlib 3.11.1 and selcal (markers).
  New licence binding `docs/status/dependency_licence_binding_20260922.json` (v2) replays every lock and
  pyproject change against the immutable 2026-08-31 inventory; no licence metadata re-extracted because
  no package or version was added.
- Regression after the change: Python 3.11 3,568 passed, 1 failed (Sphinx, docs extra absent), 53
  skipped; Python 3.12 and 3.13 3,571 passed, 0 failed after updating one test that pinned the old
  runtime constraint string, 53 skipped. The three numpy-2.5 portability failures are gone.
- Clean-install acceptance re-run: all four installs pass (numpy 2.4.6 everywhere).

## 6. Release 0.1.0 (2026-09-22, evening)

Version set to 0.1.0 (BSD-3-Clause, `LICENSE.txt`/`Licence.txt`, `CITATION.cff`, `.zenodo.json`); lock
relocked (only the project's own version changed); licence binding extended with the metadata edits.
Benchmark receipt and its figure regenerated at this state. Results:

- Development tree: 3,572 passed, 53 skipped, 0 failed (Python 3.11.12).
- Public release tree built by `scripts/build_public_release.py` (internal process material excluded,
  list in its `EXCLUDED.tsv`): 3,572 passed, 53 skipped, 0 failed, in its own locked environment. No
  test was removed; files that tests read were kept.
- Clean install of `selcal-0.1.0` wheel on 3.11/3.12/3.13 and sdist on 3.13: ALL_PASSED (receipt
  regenerated).
