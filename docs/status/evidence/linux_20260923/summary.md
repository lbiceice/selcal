# Linux verification of the SelCal 0.1.0 release tree (2026-09-23)

Tree: public release tree built by `scripts/build_public_release.py` (GitHub `lbiceice/selcal`
commit `0138406`). Containers: official `python:*-slim` images under OrbStack on an Apple arm64 host;
x86_64 runs under emulation. Dependencies: the exact versions of `uv.lock`, exported with
`uv export --locked --all-extras` (`requirements_exported_from_lock.txt`) and installed with pip from
a PyPI mirror, because direct PyPI downloads timed out. Script: `run_suite_in_container.sh`.

## Full test suite

| Platform | Python | NumPy (BLAS) | Passed | Failed | Skipped |
|---|---|---|---|---|---|
| Linux aarch64, glibc 2.41 | 3.11.16 | 2.4.6 (OpenBLAS 0.3.31) | 3,547 | 25 | 53 |
| Linux aarch64 | 3.12.14 | 2.4.6 | 3,547 | 25 | 53 |
| Linux aarch64 | 3.13.15 | 2.4.6 | 3,547 | 25 | 53 |
| Linux x86_64 | 3.12.14 | 2.4.6 | 3,567 | 5 | 53 |

macOS arm64 (reference): 3,572 passed, 0 failed.

The failures have three causes; none is a different random stream or a different decision.

1. **Floating-point values recorded on macOS** (20 tests on aarch64, one shared assertion at
   `tests/test_calibration_v2_integrity.py:296`). The expected production vector was recorded on macOS.
   On Linux aarch64 the plan digest, every seed digest, every shift and every selected lag are equal;
   the selection scores differ by at most 1 ULP (checked directly in the container).
2. **Orbit-trace values recorded on macOS** (4 tests, both architectures,
   `tests/test_m6_pearson_orbit_trace.py:71`): `1.0 == 0.9999999999999996`, a correlation of exactly
   collinear windows that Linux computes 2-4 ULP below 1.
3. **Missing tool** (1 test, all platforms): `test_pressure_harness_runs_read_only_with_fresh_workers`
   calls the `uv` binary, which the plain Python image does not contain.

The tests were not changed. Whether they should compare with a tolerance, or record platform-specific
expected values, is an open decision.

## Replay across platforms

Records made on macOS (Python 3.11.12, NumPy 2.4.6) with the shipped example, once with the sampling
null and once with exact enumeration:

| Where `verify` ran | `verify` (consistency) | `verify --replay` |
|---|---|---|
| Linux aarch64, Python 3.13 | COMPLETE, exit 0 | `environment_mismatch`, exit 4 (Python version differs) |
| Linux aarch64 and x86_64, Python 3.11.12, NumPy 2.4.6 | COMPLETE, exit 0 | `replay_mismatch`, exit 4 |
| Linux x86_64, records made there | COMPLETE | MATCH |

Linux and macOS results agree in p-value, E, selected lag, decision statistic and reject decision
(`mac_*.json`, `lin_*.json`); the only differing summary field is the advisory Monte Carlo power cap
(difference about 2e-14). The byte-level replay mismatch comes from last-bit differences in the
retained surrogate statistics.

**Consequence.** `verify --replay` is exact on the platform that made the record. On another
platform it fails closed even when all conclusions agree, and its error (`replay_mismatch`) does not
distinguish platform arithmetic from a modified record. The software identity stored in the record
contains the SelCal, Python and NumPy versions and source digests, but not the operating system,
architecture or BLAS. Options (author decision): add platform identity so that cross-platform replay is
reported as `environment_mismatch`; and/or add a decision-level replay that compares seeds, shifts,
selections, E and p exactly and statistics within a stated tolerance.

## Follow-up (same day): platform identity and decision replay

Author decision: implement both options, and split the macOS-recorded tests into exact and tolerant
parts. Changes (test-first, `tests/test_workflow_decision_replay.py`):

- Records use schema `selcal.workflow-record.v2`, whose software identity adds `platform`
  (`system`, `machine`, `libc`, `blas`). Version 1 records stay readable. Byte replay on another
  platform now reports `environment_mismatch`.
- `verify --replay-decision` (API `verify_record(..., replay_decision=True)`) needs the same SelCal
  version and source files. Seeds, states, selections, counts, p-value, decision, diagnostics and
  statistic identities must be equal (a NumPy version inside a backend identity may differ); statistic
  values may differ by at most 64 units in the last place of max(|a|, |b|, 1). A first version used
  plain ULPs of the value and failed on Linux: a correlation of 4.3e-4 differed by 149 of its own ULPs
  but only 8e-18 absolute. Rounding error of a correlation scales with its range, so the scale is
  bounded below by 1.
- Tests: `tests/test_calibration_v2_integrity.py` compares seeds, shifts and selections exactly and
  statistic values within 4 ULP; `tests/test_m6_pearson_orbit_trace.py` checks reference and
  production within 4 ULP of 1 (the decision-level agreement check is unchanged).

Result on Linux aarch64 and x86_64 (Python 3.11.12, NumPy 2.4.6) with records made on macOS by the same
code: `--replay` gives `environment_mismatch`; `--replay-decision` gives `DECISION_MATCH`, largest
statistic difference 1 unit, p = 0.015 (sampling null) and 0.03 (exact enumeration), as on macOS.

Full suite after the change, locked dependencies plus `uv` (so the pressure harness can run):

| Platform | Python | Passed | Failed | Skipped |
|---|---|---|---|---|
| macOS arm64 | 3.11.12 | 3,599 | 0 | 53 |
| Linux aarch64 | 3.11.16 | 3,600 | 0 | 52 |
| Linux aarch64 | 3.13.15 | 3,600 | 0 | 52 |
| Linux x86_64 | 3.12.14 | 3,600 | 0 | 52 |

Linux runs one more test than macOS (`tests/test_inputs.py:725` needs an extended floating dtype, which
macOS arm64 NumPy does not provide).
