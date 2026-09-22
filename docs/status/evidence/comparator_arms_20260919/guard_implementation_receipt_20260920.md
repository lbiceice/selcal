# Attainable-p guard — implementation receipt (2026-09-19/20)

Author approved production-code change (2026-09-19). TDD: tests/test_workflow_attainability.py written first; RED = ImportError (function absent); GREEN = 17/17.

## What changed

- `src/selcal/workflow.py`: new public `attainability(request, sample_count)`; `validate` output gains `attainability`; `run_files(..., allow_unattainable=False)` refuses plans with status `REFUSE_*` (WorkflowConfigError `unattainable_plan`, CLI exit 2, no record written); `verify` and `report` recompute and show it (not stored in records; record format unchanged).
- Refusal rules: 1/(B+1) > alpha; min_shift > 1 with >1 candidate (non-group null); circular/lagged-Pearson state floor = min over selected lag of colliding states / null states > alpha. Reports Monte Carlo power cap under strongest signal.
- `src/selcal/cli.py`: `run --allow-unattainable-plan`.
- `examples/workflow`: old 6-row, B=9 example could never reject (floor 1/10 from B, 3/6 from states). Replaced by 100-row synthetic lag-2 series, B=199 (floor .03, PASS): selects lag 2, p=0.015. README updated.
- Tests: toy plumbing fixtures in tests/test_workflow.py now pass `allow_unattainable=True` explicitly (golden values unchanged); tests/test_cli.py updated to the new example; NE fixture min_shift 10 -> 51 (empty shift space).

## Not changed

Calibration core (calibration_v2, nulls, contracts, verifier), in-memory API behaviour, record format,
sealed study. The core API is NOT guarded; only the file workflow is. Exact enumeration (blueprint remedy f)
NOT implemented yet: it touches plan schema, result wire and verifier — next task.

## Verification

- Full suite (excluding matplotlib plot test): 3563 passed, 14 failed. Baseline before change: 3547 passed,
  13 failed (12 task10 scope-manifest drift from pre-existing uncommitted tree, 1 Sphinx missing).
- One new failure, expected: tests/test_benchmark_in_memory.py::test_recorded_standard_receipt_is_bound_to_current_source_harness_and_contract.
  The 2026-09-08 benchmark receipt is bound to source-file hashes; it is now HISTORICAL. Not overwritten; a new
  receipt requires a fresh benchmark run.
- ruff check/format clean on touched files; mypy clean on workflow.py and cli.py.
- Floor claim tested as a true lower bound on random data (4 candidate sets x 20 draws, n=32).
- Pre-change snapshot: scratchpad selcal_pre_fix_snapshot_20260919.tgz (session-local; not a backup).
- Nothing committed, pushed or released.
