# Portability and test hygiene — 2026-09-22

Internal record. Commits at time of check: `c08b785` (+ uncommitted benchmark refresh).

## Portability: full suite on locked environments for Python 3.12 and 3.13

Environments built from `uv.lock` without changing it (`UV_PROJECT_ENVIRONMENT=<scratch>/envX
uv sync --locked --all-extras --python X`); the lock resolves numpy 2.5.2 and Sphinx 8.2.3 there
(the project's development environment is Python 3.11.12 with numpy 2.4.6).

| Python | passed | failed | failures beyond the known set |
|---|---|---|---|
| 3.11.12 (project .venv) | 3,596 | 14 | none (13 pre-existing + historical benchmark receipt, now refreshed) |
| 3.12.10 (locked) | 3,597 | 16 | 3 |
| 3.13.12 (locked) | 3,597 | 16 | 3 |

The Sphinx documentation-build test passes on 3.12/3.13: its 3.11 failure was only the missing
optional `docs` extra in the development environment.

The three extra failures on 3.12/3.13 are pre-existing: they fail identically on the pre-round commit
`724ac6f` (checked out with `git archive`, run with the same 3.13 environment).

| Test | Cause |
|---|---|
| test_calibration_v2_integrity::test_bound_snapshot_entrypoints_have_exact_static_call_contracts | runs mypy with `python_version = 3.11` over numpy 2.5.2 stubs, which use the PEP 695 `type` statement (3.12+) |
| test_exact_oracle_independence::...no_reachable_random_behavior_surface | numpy 2.5 makes `NDArray` a `typing.TypeAliasType`; the random-behaviour graph walker classifies it as an opaque carrier |
| test_plan_migration_v1_to_v2::...no_reachable_random_behavior_surface | same as above |

Options (author decision; each changes a release policy):
- constrain numpy below 2.5 in `pyproject.toml` and relock: fixes both, but invalidates the
  dependency-lock and licence evidence digests, which then need a new dated receipt;
- keep numpy 2.5 and teach the structure gate that `TypeAliasType` annotations are inert, plus make the
  mypy check target the running interpreter: changes a deny-by-default gate's rule and needs its own
  reviewed amendment.

## Task10 scope-baseline tests (12 failures, pre-existing)

`tests/task10/test_authority_amendment_scope_v1.py` binds a 2026-08-30 review baseline to git HEAD
`94f993b` and to file digests, with `machine_stop_decision = STOP_ON_ANY_BASELINE_HASH_DRIFT`. It failed
before these rounds (README/pyproject drift) and now also on HEAD. Making it pass means writing a
successor baseline, which would rubber-stamp that review; left untouched for an author decision
(retire the historical gate, or run its successor-baseline procedure).

## Benchmark receipt refreshed

`docs/benchmarks/in_memory_standard_20260922.json` (+ figure) measured on the same environment as the
2026-09-08 receipt (Darwin arm64, CPython 3.11.12, numpy 2.4.6); 7 cases, all `complete: 3`. References
moved to the new receipt in tests, MANIFEST.in, the hygiene audit and `docs/api/performance.rst`; the
20260831 and 20260908 receipts stay as historical files.

## Resolution (2026-09-22, author decision)

numpy constrained to `<2.5` and relocked; the three Python >= 3.12 failures no longer occur (3.12 and
3.13: 0 failures). The task10 gate was retired (`retired_task10_gate_20260922.md`). See
`evidence/acceptance_20260922/acceptance_summary.md` section 5.
