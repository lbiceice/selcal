# SelCal

**Selection-aware calibration of scanned-lag dependence tests between two time series.**

Analysts who scan several lags and report the strongest cross-correlation often test that winner as if
its lag had been fixed in advance, and often ignore autocorrelation; both inflate false positives.
SelCal implements the published remedy (repeat the whole lag search inside every circular-shift
surrogate; Cannistra et al., eLife 2025; Yuan & Shou, PLoS Biology 2024) as reusable software, and adds:

- **a frozen analysis plan**: candidate lags, statistic, selection rule, null model, number of
  surrogates and alpha are fixed before any data-dependent step and stored with every result;
- **exact enumeration** of the complete circular group (`circular_shift_exact_v1`), removing Monte Carlo
  loss;
- **an attainable-p guard**: with a circular null and L searched lags, L of the n circular states tie with
  the observed maximum, so the exact p-value cannot fall below L/n; `selcal validate` reports this and
  `selcal run` refuses plans that can never reach alpha;
- **a three-level preflight** separating input validity, plan executability and the scientific
  assumptions the analyst must justify;
- **verifiable, replayable records**: one SQLite file with input, plan, full result and software
  identity; `selcal verify --replay` recomputes it byte for byte.

SelCal tests one pair of series over a small, pre-declared lag set. It does not perform causal
discovery, estimate effect sizes, align or detrend series, or correct across many pairs.

## Quick start

```console
git clone https://github.com/lbiceice/selcal.git && cd selcal
python -m pip install .
selcal validate examples/workflow/series.csv examples/workflow/pearson.json
selcal run examples/workflow/series.csv examples/workflow/pearson.json run.sqlite --max-bytes 1048576
selcal verify run.sqlite --max-bytes 1048576 --replay
selcal report run.sqlite report.html --max-bytes 1048576
```

Requirements: Python 3.11-3.13 and NumPy (`numpy>=1.26,<2.5`). Tested on macOS arm64 with CPython 3.11,
3.12 and 3.13 (clean wheel and sdist installs); Linux and Windows are not yet tested.

## Citation, licence and support

- Cite the software with `CITATION.cff` (GitHub "Cite this repository"); the archived release has a
  Zenodo DOI (see the release page).
- Licence: BSD 3-Clause (`LICENSE.txt`; `Licence.txt` is an identical copy required by SoftwareX).
- Questions and bug reports: open a GitHub issue; the maintainer contact is listed in `CITATION.cff`.

## Reproduction package

`docs/status/evidence/` contains the frozen protocols, scripts and results behind the accompanying
SoftwareX manuscript (figure scripts in `docs/manuscript/figures/`): the common-practice comparison, the confirmation study (R = 4,000 per
null condition), the IDTxl 1.6.0 comparison, the guard survey of published lag scans, the clean-install
acceptance, and the re-analysis of a published dengue-climate correlation using the original authors'
CC BY 4.0 data. Adverse and non-adopted results are kept.

## Project status

Version 0.1.0 is the first public release. The internal milestone label of the calibration core is
`M0-M2 IMPLEMENTATION CANDIDATE / FINAL VERIFICATION PENDING`: the core passes about 3,600 automated
tests and the acceptance checks above, while items such as cross-platform continuous integration and
an independent user evaluation are still open.

## Install the development snapshot

SelCal currently requires Python 3.11 or newer. From an activated, isolated Python
environment at the repository root, install the exact checked-out snapshot with:

```console
python -m pip install .
```

This installs the checked-out release from source. SelCal 0.1.0 is not published on PyPI.

### Reproduce the locked development environment

The checked-in `uv.lock` resolves the runtime, development, documentation, and benchmark
dependency surfaces declared in `pyproject.toml`. With `uv` installed, create or update an
exact project environment from that lock without changing it:

```console
uv sync --locked --all-extras
```

Verify that `pyproject.toml` and the lock remain synchronized before running release-facing
checks:

```console
uv lock --check
```

Run the test suite through the locked project environment with:

```console
uv run python -m pytest
```

The lock makes dependency resolution repeatable for the declared Python dependency range;
it does not prove that every interpreter or operating-system combination in that range is
supported. It is not a cross-platform test result, a public release, or an open-source
licence grant.

### Separate verifier memory measurement from coverage

The following are targeted verifier checks, not a whole-product coverage result.
From an activated project environment at the repository root, run the resource
measurement without coverage, profiling, a debugger, or other active tracing:

```console
python -m pytest tests/test_verifier_integration_v2.py -k test_public_verifier_scratch_peak
```

Run coverage separately, excluding only the two resource-measurement tests from
this verifier file:

```console
python -m pytest tests/test_verifier_integration_v2.py --cov=src -k 'not test_public_verifier_scratch_peak'
```

Both resource tests remain in the default unfiltered suite. Coverage can start
tracing in child processes; it must not be combined with the memory-measurement
lane. The worker fails with `measurement environment is dirty` when a trace or
profile callback is active, or tracemalloc is already running. It does not clear
instrumentation or raise the frozen memory limits to make a measurement pass.
The check detects those CPython trace/profile/tracemalloc states, not every form
of external instrumentation. These tests measure Python-tracked allocations, not process RSS or native allocations,
and do not establish asymptotic memory bounds or scientific validity. Coverage
results do not substitute for a clean resource measurement.

## Build the API reference

Install the documentation dependency group from the repository root:

```console
python -m pip install ".[docs]"
```

Build the HTML reference with warnings treated as errors:

```console
python -m sphinx --fail-on-warning --keep-going -b html docs/api docs/api/_build/html
```

Open `docs/api/_build/html/index.html` in a browser after the command succeeds. The
generated reference describes the current pre-release public API; it is not evidence of
M6 scientific validity, a public release, or SoftwareX submission readiness.

## Run a file-to-report workflow

After installation, run these commands from the source snapshot. Every command
uses the same application service as the Python API:

```console
selcal validate examples/workflow/series.csv examples/workflow/pearson.json
selcal run examples/workflow/series.csv examples/workflow/pearson.json run.sqlite --max-bytes 1048576
selcal verify run.sqlite --max-bytes 1048576
selcal verify run.sqlite --max-bytes 1048576 --replay
selcal report run.sqlite report.html --max-bytes 1048576
selcal doctor
```

`python -m selcal` is equivalent to `selcal`. The input is a fixed synthetic
100-row example (y depends on x at lag 2), not research validation; its result has
199 retained replicates, selects lag 2 and gives p=0.015. Replace the input and
configuration to analyse your own supported data.

`validate` also reports `attainability`, computed from the plan and the sample count
with the same float comparison the calibrator uses (`p = (1 + E)/(B + 1)`, reject iff
`p <= alpha`). No run can reach p below `1/(B+1)`. For the circular-shift nulls with
lagged Pearson, shifts that move one searched lag onto another reproduce the observed
maximum, so a share (number of searched lags)/(number of null states) of the states is
always an exceedance: 0.03 for 3 lags and 100 samples. With exact enumeration
(`circular_shift_exact_v1`) that share is a hard floor on p. With the sampling null
(`circular_shift_v2`) a single run can fall below it when the draws happen to miss those
states (the example above gives p = 0.015), so there it caps power instead; the reported
`monte_carlo_power_cap` is the best rejection rate B draws allow even for a very strong
signal. `run` refuses plans whose share exceeds alpha, plans that search several lags with
`min_shift` > 1 (not a group of shifts), and exact-enumeration plans whose `replicates` is
not `n - 1`, with exit 2 and error `unattainable_plan`, unless `--allow-unattainable-plan`
is given.

`validate` reports a three-level `preflight` so that different questions are not merged:
`input` (the file loaded and passed the input limits; loader errors are reported earlier with
their own codes), `plan` (`EXECUTABLE` or `NOT_EXECUTABLE`, with every reason listed:
`resource_budget_exceeded` when the executor's in-memory caps would refuse the run, or a
`REFUSE_*` attainability status; `warnings` flag plans that will end NOT_EVALUABLE because the
null has no states), and `scientific_assumptions` (the assumptions this plan relies on, e.g. lags
declared before seeing the data, circular-shift exchangeability; marked
`DECLARED_NOT_VERIFIED` because SelCal cannot check them from the data). When the plan is not
executable, `validate` exits 2 with outcome `PLAN_NOT_EXECUTABLE` and the first reason as its
error, and `run` refuses before any calibration (`resource_budget_exceeded` or
`unattainable_plan`). The resource check runs first, so an oversized replicate count is refused
without plan-time arithmetic that grows with it.
The record captures complete raw input, normalized request, full result and
recorded software identity. Reports and records must use new output paths.

`verify` checks byte, actual input, plan and result consistency; it does not
recompute by default. `--replay` explicitly recomputes the complete calibration
and compares exact result bytes under matching recorded versions/source files.
Neither check authenticates past execution. The saved record can be read without
the original input paths, but this is **not checkpoint/resume**. Interrupted
writes can leave a rejected partial file; no cross-platform power-loss durability
guarantee is made.

The JSON config schema is `selcal.workflow-config.v1` with exactly `input` and
`plan` in addition to `schema`. All ten plan parameters are explicit in the example.
For NPZ use `"input": {"format": "npz"}`. CSV requires two distinct named columns.
Both the incoming config and its normalized encoding plus LF must fit 65,536
bytes, with nesting depth at most 8. Duplicate keys and nonfinite values reject.
`--max-bytes` bounds stored payload/database and report bytes, not process memory;
the example's 1 MiB cap is a caller choice. Existing scientific input/execution
limits remain unchanged.

Normal commands emit one JSON line. Exit 0 means the requested operation completed
(or validation/inspection passed); **exit 7 means scientific NOT_EVALUABLE** with
null p/decision, not an I/O failure or evidence of no effect. Exit 2 is invalid
request, exit 4 operation/integrity failure, and exit 130 an observed interruption.
Help/argument syntax diagnostics use the standard command-line parser. Runtime
record reading requires SQLite serialize/deserialize and no-follow file opening;
unsupported capabilities fail explicitly. Thin UI, checkpoint recovery, CI and
containers remain separate unfinished deliverables.

## Load bounded CSV and NPZ inputs

The candidate loaders use a fixed input resource envelope with no user override. `load_csv`
accepts a strict UTF-8 two-field CSV: one nonempty unique two-name header, exactly two numeric
fields per later physical record, and no blank, repeated-header, missing, extra, nonfinite, or
float64-underflowing data cells. Quoted fields are accepted within one physical record, but
quoted fields cannot contain CR or LF. `LF`, `CRLF`, and `CR` terminators normalize to the same
record boundary.

`load_npz` accepts one conventional single-disk ZIP with exactly two non-directory numeric NPY
members named `source`/`source.npy` and `target`/`target.npy`. Member compression is limited to
stored or deflate. Encryption, data descriptors, archive-level ZIP64, path-like or duplicate
names, overlapping ranges, unsupported NPY versions, multidimensional arrays, and non-real or
object dtypes are rejected. The supported NPY versions are 1.0 and 2.0; arrays must be
one-dimensional signed integer, unsigned integer, or real float with item size at most 8 bytes.

The exact envelope-v1 limits are:

| Reason code | Exact limit |
|---|---:|
| `CSV_RAW_BYTES` | 67,108,864 |
| `CSV_RECORD_CHARACTERS` | 1,024 |
| `CSV_FIELD_CHARACTERS` | 256 |
| `CSV_DATA_ROWS` | 1,000,000 |
| `NPZ_RAW_BYTES` | 33,554,432 |
| `NPZ_CENTRAL_DIRECTORY_BYTES` | 16,384 |
| `NPY_HEADER_BYTES` | 4,096 |
| `NPY_ELEMENTS` | 1,000,000 |
| `NPZ_MEMBER_UNCOMPRESSED_BYTES` | 8,004,108 |
| `NPZ_TOTAL_UNCOMPRESSED_BYTES` | 16,008,216 |

Resource failures use a path-free stable prefix followed by an exact observation:

```text
INPUT_RESOURCE_LIMIT_EXCEEDED_V1 reason=<CODE> limit=<INTEGER> observed=<INTEGER>
INPUT_RESOURCE_LIMIT_EXCEEDED_V1 reason=<CODE> limit=<INTEGER> observed_at_least=<INTEGER>
```

These input-loading limits are independent of and not interchangeable with the `B`, `C`, `N`,
and `S` in-memory execution budget. The loading envelope bounds construction of a `SeriesPair`;
the execution budget separately bounds calibration work after an input has been accepted. This
is not streaming or out-of-core support, a security certification, M6 scientific evidence,
release readiness, or SoftwareX submission readiness.

## Characterize in-memory performance

Run the bounded standard benchmark from an isolated development installation:

```console
python scripts/benchmark_in_memory.py --preset standard > benchmark.json
```

The JSON records the benchmark contract hash, environment identity, B/C/N case matrix,
repeat-level wall times, result statuses, scientific-plan hashes, and maximum Python
allocation peaks reported by `tracemalloc`. Input construction, process startup, native
allocations, parallel scaling, GPU execution, and cross-machine comparisons are outside the
measurement boundary. This is single-process characterization, not a cross-platform performance guarantee or M6 scientific evidence.

## Run the deterministic example

The repository includes a small end-to-end example that resolves a v2 plan, performs
selection-aware surrogate calibration, verifies the returned result, and emits stable JSON:

```console
python examples/basic_selection_aware_calibration.py
```

The example selects candidate lag 2 and reports a full-reselection global `p_value` of
`0.2` for its fixed synthetic input and seed. This example is an executable contract demonstration, not M6 scientific evidence.

## Inspect fail-closed behavior

The second example deliberately supplies a series and null-model constraint for which no
admissible circular shift exists:

```console
python examples/fail_closed_not_evaluable.py
```

SelCal returns `status="not_evaluable"`, `failure_stage="null_bind"`, and null decision
fields without executing any surrogate replicates. `NOT_EVALUABLE is not evidence of no effect or non-significance.`

## Exercise binned NetTE with block shuffle

The third example uses the other registered statistic/null combination: three-bin
equal-width NetTE with strict length-two block shuffling.

```console
python examples/binned_nette_block_shuffle.py
```

It runs exact-B full reselection, verifies the result, and emits deterministic JSON for
the fixed synthetic input. This broadens executable feature coverage; it is not a comparator or M6 result.

## Save and read complete result content

Save all candidate results, transformation tokens, retained failures and decisions
from the small synthetic example, then read the record in a separate process:

```console
python examples/save_and_read_result.py save result.json --max-bytes 65536
python examples/save_and_read_result.py read result.json --max-bytes 65536
```

The destination must not exist. The explicit byte budget is for this example;
oversized or malformed records are rejected rather than truncated. The read
summary is labelled `content_only_not_replay`: strict content reconstruction is
not authenticated execution, checkpoint recovery or a calibration replay.
Interrupted writes can leave a partial file; this example is not an atomic
evidence-bundle exporter. The API reference documents the direct development
imports from `selcal.result_wire` and their verification limits.

## Python API

The historical v1 public path remains available for plan identity and migration. It is
not executable calibration semantics:

```python
from selcal import PlanRequest, resolve_plan
from selcal.canonical import scientific_plan_sha256

request = PlanRequest(
    candidates=(1, 2, 3),
    statistic_name="lagged_pearson_v1",
    statistic_params={},
    selection_rule="max_absolute",
    null_name="circular_shift_v1",
    null_params={"min_shift": 1},
    replicates=999,
    alpha=0.05,
    tie_tolerance=1e-12,
    root_seed=17,
    failure_policy="fail_closed_v1",
)
resolution = resolve_plan(request)
print(scientific_plan_sha256(resolution.plan))
```

The candidate v2 in-memory execution path is:

```python
import numpy as np

from selcal import PlanRequestV2, calibrate_selected_family, resolve_plan_v2
from selcal.contracts import SeriesPair

pair = SeriesPair(
    source=np.asarray((0.0, 3.0, 1.0, 2.0, 4.0, 5.0), dtype=np.float64),
    target=np.asarray((0.0, 1.0, 3.0, 2.0, 5.0, 4.0), dtype=np.float64),
)

request_v2 = PlanRequestV2(
    candidates=(1, 2, 3),
    statistic_name="lagged_pearson_v1",
    statistic_params={},
    selection_rule="max_absolute",
    null_name="circular_shift_v2",
    null_params={"min_shift": 1},
    replicates=9,
    alpha=0.05,
    tie_tolerance=1e-12,
    root_seed=17,
)
resolution_v2 = resolve_plan_v2(request_v2)
result = calibrate_selected_family(pair, resolution_v2)
```

A v2 plan with up to 1,000,000 replicates may resolve successfully because that is a
plan-representability cap. Resolution does not imply that the current in-memory executor budget
admits the plan. The versioned candidate executor requires `B <= 1000`,
`B*C <= 5000`, `B*S <= 25000`, and `B*(C*N + S + N) <= 2500000`, where `S=1` for
circular shift and `S=N/block_length` for block shuffle. An over-budget call raises
`ResourceLimitError` before replicate allocation and returns no calibration result.

### Exact enumeration instead of Monte Carlo draws

`null_name="circular_shift_exact_v1"` (with `null_params={"min_shift": 1}`) uses every
non-identity circular state exactly once instead of drawing `B` states with replacement.
Set `replicates` to `n - 1`. Through the file workflow any other value is refused by `run`
(`unattainable_plan`); through the Python API it yields a NOT_EVALUABLE result at stage
`null_bind` with diagnostic `enumeration_replicate_count_mismatch_v1`. `verify` checks from the
retained tokens alone that replicate `i` used shift `i + 1`, so a record with repeated, missing
or reordered states is rejected even without `--replay`.
The p-value formula is unchanged, and with the complete group `(1 + E)/(B + 1)` equals the
exact share `#{s : T_s >= T_0}/n`, so the Monte Carlo loss disappears. On the sealed 1,200-input
study (n=64, lags 1-2) this changes nothing in the two null cells (3.5% each) and raises
rho=.6 power from 91.0% to 99.5%; see
`docs/status/evidence/comparator_arms_20260919/results_production_exact.json`.
The sampling null `circular_shift_v2` is unchanged, so existing plans and records keep their
behaviour.

**Recommended for new circular-shift plans:** `circular_shift_exact_v1` with `replicates = n - 1`,
whenever `selcal validate` reports `attainability.status` `PASS`. In the 2026-09-22 confirmation study
(R = 4,000 per null cell; i.i.d., circular MA(2) and non-circular AR(1) series; n = 64 and 256) its
false-positive rate stayed at 3.0-4.4%, and at n = 256 with 8 searched lags it detected the stronger and
weaker signals in 100% and 96.7% of datasets. When the guard refuses a plan (fewer than
`L / alpha` samples for `L` searched lags), SelCal offers no calibrated fallback: block shuffle was tested
as one and not adopted, because at n = 64 under autocorrelation its false-positive rate reached 6.0%
against a pre-registered bound. Use a longer series or search fewer lags. Evidence:
`docs/status/evidence/remedy_confirm_20260920/verdict_stage2.md`.

Current implementation candidate: immutable inputs, v1/v2 plan resolution, explicit
v1-to-v2 migration, common support, selection rules, binned NetTE, lagged Pearson,
owned circular-shift (sampled or exactly enumerated) and strict block-shuffle
transformations, exact-B full reselection, fail-closed Monte Carlo calibration, result
verification, and an internal finite-state algorithm oracle.

This is local algorithm-contract implementation, not scientific validation. Exact-oracle
agreement does not establish exchangeability, Type-I-error control, power, or validity
for a particular data-generating process.

`M6 SCIENTIFIC IMPACT: HOLD / NOT EXECUTED`

`PERSISTENCE, EVIDENCE BUNDLES, UI, RELEASE, LICENSE, DOI, MANUSCRIPT, SOFTWAREX
READINESS, SUBMISSION: HOLD / NOT DUE / NOT READY`

SelCal is not a causal-edge inference product. No persistence, resume/evidence-bundle,
UI, or release surface is public.

No license has been selected, so redistribution is not authorized by this development snapshot.
