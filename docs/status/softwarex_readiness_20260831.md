# SelCal SoftwareX readiness ledger - 2026-08-31

Declared overall readiness: **42.00%** (`42.00 / 100`; rounded display: **42%**).

This is a weighted delivery-maturity estimate, not an acceptance probability or a
journal-issued score. Engineering checks, scientific evidence, release evidence and
submission evidence remain separate and cannot compensate for one another.

## Current evidence identity

- Worktree: current local SelCal checkout; machine-local absolute path intentionally omitted.
- Branch: `codex/contract-resolution-pearson`; tracked base `94f993b`.
- State: uncommitted implementation candidate; not a release or immutable submitted version.
- Core suite excluding historical Task-10 authority routes: expected final Task-4 module
  acceptance identity `2851 passed, 1 skipped`; the exact post-receipt rerun remains the
  controlling evidence.
- Package branch-aware combined-opportunity coverage (covered statements plus covered
  branches divided by total statements plus total branches): `95.14908256880734%`
  (`6532` statements, `238` missed;
  `2188` branches, `185` missed and `165` partial). This exceeds both the 80% acceptance
  threshold and the frozen pre-change `95.07%` floor. The 30 newly covered opportunities
  come from public CSV/NPZ boundary and rejection-path characterization, not exclusions or
  production-code changes. Separately, line coverage is `96.35639926515616%` and pure
  branch coverage is `91.54478976234003%`.
- Locked Ruff 0.16.5: exit 0 across `src`, `tests`, `scripts`, `examples` and the
  Sphinx configuration. This supersedes the earlier same-day check with Ruff 0.6.9,
  which did not exercise the newer default rules.
- Strict mypy: exit 0 across all 32 `src/selcal` source files.
- Release-surface hygiene audit: `PASS`, zero findings.
- Three deterministic examples: lagged-Pearson/circular-shift complete,
  binned-NetTE/block-shuffle complete, and fail-closed not-evaluable routes all produced
  byte-identical JSON in repeated subprocess runs.
- Sphinx 8.2.3 documentation: warning-free HTML build covering all 12 intentionally
  exported public objects plus architecture, usage and performance guides; generated
  output is excluded from version control.
- Universal dependency lock: `uv.lock` format version 1, revision 2, 51 resolved
  packages, SHA-256
  `4ccc4c47ede6fd04ef436fac56d8e1f9d91284c82b30b18b87044015f7227067`;
  `uv lock --check` passes and the runtime, benchmark, development and documentation
  dependency surfaces are represented.
- Dependency-licence evidence inventory: all 51 lock records are bound one-to-one and
  all 50 third-party records have exact-name/exact-version Core Metadata evidence from
  isolated materialisations. The inventory remains
  `HOLD_TECHNICAL_LICENCE_INVENTORY_NOT_CLOSED`: the root source licence is unselected,
  `setuptools>=68` is an unresolved build-system dependency, the supported-target matrix
  is unfrozen, selected wheel/sdist hashes are not yet bound to the extracted metadata,
  and licence files plus vendored components are not audited. This is metadata evidence,
  not a legal compatibility conclusion.
- Fresh isolated local installation: CPython 3.11.12 completed
  `uv sync --locked --all-extras`, then passed the current `2483` core tests with `1` skip,
  warning-as-error documentation and wheel/sdist construction. A separate CPython
  3.12.10 environment installed the built wheel, passed its dependency check and ran
  all three deterministic examples. Both environments were Darwin arm64; the build
  outputs were temporary verification artifacts, not a release.
- Current-byte Task-4 package checkpoint: a fresh serial CPython 3.11.12 build produced
  `selcal-0.1.0.dev0-py3-none-any.whl` (execution-time SHA-256 `d70aa2ed...`) and
  `selcal-0.1.0.dev0.tar.gz` (execution-time SHA-256 `f189694e...`). The replayable
  harness SHA-256 is `e929699d...`. A new temporary venv installed only
  that wheel, resolved NumPy 2.4.6, verified package name/version outside the repository
  path, and passed public CSV, stored-NPZ and deflated-NPZ smoke; the deflated smoke forbade
  `zipfile.ZipFile`, observed two public-zlib decompressor constructions for two members,
  and checked wheel `RECORD` plus the three input source modules. The exact current artifacts
  and clean venv were deleted, so their hashes are execution-time observations and are not
  independently re-inspectable. The pre-existing `dist/` wheel remains untouched at
  `41ff1ea7...`; it is superseded, not current, and was not installed. This is local package
  evidence only, not release, licence, cross-platform, M6 or submission closure.
- Standard single-process benchmark: seven B/C/N cases and 21 measured repeats, all
  verified `complete`; contract SHA-256 `c3786267...`, installed-source SHA-256
  `91ac8ae2...` across 32 Python source files, and harness SHA-256 `d266fd4d...`.
  The current receipt SHA-256 is `9b1752ce...`; the exact JSON receipt and
  deterministic SVG/300-dpi PNG figure are retained. This is one Darwin arm64 local run,
  not a portability, speedup or M6 result.
- Input-resource envelope v1.1 focused verification: `314 passed, 1 skipped`. All six
  finite CPython/NumPy cells ran the complete 150-test NPZ-limit file on one Darwin arm64
  machine: CPython 3.11.12 and 3.12.10 with NumPy 1.26.4/2.4.6, CPython 3.13.12 with the
  checkpoint-resolved NumPy 2.4.3, and CPython 3.14.3 with checkpoint-resolved NumPy 2.5.2.
  The canonical input receipt SHA-256 is `abcdc55c...`. This is not cross-platform or an
  open-ended support matrix.
- Local serial input pressure observation: all eight CSV/NPZ cases at 10,000, 100,000,
  250,000 and 1,000,000 rows/elements loaded in fresh measurement subprocesses. At one
  million, CSV observed 14,333,349 raw bytes, 13.585475332991336 s wall time, 54,777,465
  traced peak bytes and 55,771,136 sampled-RSS delta; NPZ observed 16,000,510 raw bytes,
  0.01957420801045373 s, 56,009,165 traced peak bytes and 47,529,984 sampled-RSS delta.
  The retained replayable harness SHA-256 is `37626e07...`; it fixes float64,
  `NPZ_STORED`, repeat count one and a 0.001 s RSS interval. Loads shorter than that interval
  may miss a transient RSS peak. These are `LOCAL_DESIGN_PRESSURE_OBSERVATION_ONLY`, not
  performance guarantees.
- Current Task-10 aggregate: `176 passed, 12 failed`.
- All 12 Task-10 failures arise in the superseded authority-amendment scope-v1 route:
  it freezes 109 non-allowlisted paths while the current worktree contains 168
  (path-set SHA-256
  `6d630c3942ea79d7396d6e1144c99ab45ea63e499b1cacb7fdff488db08e6cca`).
- Read-only scientific code-smell audit v3: zero blockers, two open majors, two majors
  resolved in the current candidate and two open minors. Lagged Pearson now preserves
  unexpected `TypeError`, `ValueError` and `OverflowError` instead of misreporting them
  as analytic failure. The versioned CSV/NPZ caps, stable resource errors, bounded
  one-descriptor snapshot, public-zlib extraction and NPY preflight close the input-resource
  major at the local implementation-candidate level. Open majors remain verifier complexity
  and hidden process-level ownership/API state. Both v1 and v2 adverse receipts are retained
  by exact SHA-256 rather than overwritten. This closes only the bounded input-loading
  implementation major; it does not close the other audit findings or downstream gates.
- Current official OSP DOCX: Version 6 (March 2026), 44,823 bytes, four rendered pages,
  SHA-256 `9fcf40ede96a2f188ee4ef77134e0596d01e1b65fd9db63f2874d29f2ecb916d`.
- Current official-source refresh: the SoftwareX Guide was re-read in a real browser on
  2026-08-31; the OSP DOCX, OSP TeX and reviewer-form PDF were re-downloaded and retained
  their frozen hashes. The current machine-readable contract is
  `docs/official_contract/softwarex_product_contract_20260831.json`; its structural
  validator returns `HOLD` with zero errors and zero warnings.

## Scoring rule

Each row uses a fixed weight and a completion value restricted to `0`, `25`, `50`,
`75` or `100` percent. Weighted points equal `weight * completion / 100`.

- `0`: absent or not executed.
- `25`: narrow scaffold exists but the main deliverable is absent.
- `50`: material implementation exists but a decisive internal gate remains open.
- `75`: intended local deliverable is substantially present and locally verified, while
  approval, portability, release or external evidence remains open.
- `100`: the current-scope deliverable and every required checkpoint evidence item are closed.

## Weighted ledger

| Row | Weight | Completion | Points | Current evidence and limiting fact |
| --- | ---: | ---: | ---: | --- |
| Product identity, architecture and official contract | 10 | 75 | 7.50 | SelCal is separated from the rejected Entropy paper and P3-NetTE-repro; the M0-M8 architecture and current SoftwareX product contract are frozen. OSP remains conditional pending formal no-prior-SoftwareX product genealogy, and Task-10 authority scope-v2 remains unapproved and unimplemented. |
| M0 contracts, inputs and scientific identity | 8 | 75 | 6.00 | Immutable v1/v2 contracts, migration, canonical serialization, scientific hashes, golden vectors and versioned CSV/NPZ resource limits are implemented and locally tested. Final authority closure and release identity remain open; the loading limits do not establish M6 validity or streaming. |
| M1 statistics and null adapters | 8 | 75 | 6.00 | Binned NetTE, lagged Pearson, circular shift and strict block shuffle are executable and locally tested. Lagged Pearson's unexpected-exception collapse is closed in the current candidate with a retained red/green test trail. Scientific exchangeability and domain validity are M6 questions, not implied by these tests. |
| M2 selection-aware full-reselection calibration | 10 | 75 | 7.50 | Exact-B surrogate rescanning and reselection, fail-closed outcomes, plus-one calibration, result verification and an internal finite-state oracle are implemented. Final authority closure and scientific error-control evidence remain open. |
| M3 execution, state and resume | 7 | 0 | 0.00 | No immutable event log, checkpoint, resume or crash-recovery implementation. Existing hidden process-level ownership registries and dynamic verifier installation must be resolved or explicitly bounded before M3 can claim cross-process semantics. |
| M4 evidence bundle and reporting | 7 | 0 | 0.00 | No run manifest, evidence-bundle verifier, report builder or failure-report product. |
| M5 stable Python API and CLI | 6 | 50 | 3.00 | The versioned Python API is executable and the basic example uses only its intended public path. No CLI, command contract or CLI/API equivalence evidence exists. |
| M6 scientific impact, comparator and real-case validation | 16 | 0 | 0.00 | No prospective strict-null, alternative, comparator, negative-control or independent real-case study has been executed. This is the largest SoftwareX scientific blocker. |
| Packaging, installation and dependency declaration | 5 | 75 | 3.75 | `pyproject.toml`, a current universal lock, two local exact-lock materialisations and a 51-record dependency-licence evidence inventory exist. The inventory is HOLD: no supported-platform matrix, selected-artifact/licence-file/vendored-component audit, independent external installation, resolved build-system closure, release metadata or author-selected licence exists. |
| Automated tests, static quality and portability | 5 | 75 | 3.75 | The expected final module identity is 2851 passing tests with one platform skip; focused input tests, locked Ruff 0.16.5, strict mypy, hygiene, lock and diff checks pass. Branch-aware combined-opportunity coverage is 95.14908256880734% (line 96.35639926515616%; pure branch 91.54478976234003%), above both the 80% threshold and frozen 95.07% combined-opportunity floor. The smell audit retains two open majors and two open minors; same-machine compatibility evidence is not a supported-platform matrix. |
| README, API/manual documentation and examples | 5 | 75 | 3.75 | README provides truthful installation, bounded CSV/NPZ grammar and limits, example, documentation and benchmark routes; three deterministic examples cover both registered statistic/null pairs plus fail-closed behavior; Sphinx builds warning-free API, architecture, usage and performance pages. Hosted/versioned documentation, a supported-platform docs matrix and independent usability evidence remain absent. |
| Public GitHub, licence, release, data and persistent identity | 6 | 0 | 0.00 | No public remote, author-selected code licence, frozen release, DOI/PID or research-data deposit. |
| CI, container and performance benchmark | 3 | 25 | 0.75 | A tested smoke/standard benchmark harness, exact local JSON receipt, reproducible vector/raster plotter and visually inspected figure now exist. No CI workflow, Dockerfile, cross-platform lock verification, CI environment matrix, controlled cross-platform runs, parallel-scaling implementation or comparator benchmark exists. |
| M7 thin UI | 2 | 0 | 0.00 | Not due before M6; no UI exists. |
| M8 SoftwareX manuscript and portal closure | 2 | 0 | 0.00 | The current template has been reverified, but no manuscript, figures, declarations, live portal draft or submission receipt exists. |
| **Total** | **100** |  | **42.00** | **Rounded display: 42%.** |

## Delta from the previous live estimate

The immediately preceding live estimate was `40.75 / 100`. This checkpoint adds `1.25`
weighted points only because the packaging, installation and dependency-declaration row
moved from 50% to 75% after all of the following became current, executable evidence:

1. a current `uv.lock` covering runtime plus all optional dependency surfaces;
2. a successful exact-lock check and fresh CPython 3.11 locked source-environment sync;
3. `2463` passing core tests at the original lock checkpoint, one skip,
   warning-as-error documentation and wheel/sdist builds inside that isolated
   environment; the current exact-lock rerun is `2483 passed, 1 skipped` after adding
   the source-bound audit receipts and the Lagged-Pearson exception-classification repair;
4. a separate CPython 3.12 wheel installation with compatible dependencies and all three
   deterministic examples passing;
5. a machine-readable receipt preserving tool, interpreter, platform, hash and adverse
   compatibility findings.

No additional credit was assigned for CI, containerization, public release or portability.
Both verified environments are on the same Darwin arm64 machine; the Docker daemon was
unavailable. These omissions cap packaging at 75% and leave the combined
CI/container/performance row at 25%.

The third example adds the previously undocumented binned-NetTE/block-shuffle route and
strengthens feature coverage inside the existing 75% documentation band. It adds no points
because hosted documentation, cross-platform builds and independent usability evidence
remain open.

No credit was added for M3, M4, M6, CLI, CI execution, containerization, public release,
licence, DOI, manuscript or submission. The official contract was refreshed without a
rule delta and its stale project-status prose was reconciled; that factual correction
does not add maturity points or close a product gate.

The dependency-licence inventory and scientific code-smell receipt also add no maturity
points. They improve traceability and expose work still required; they do not select a
licence, establish compatibility, freeze a support matrix, validate science or create a
release.

The input-resource major closure, finite same-machine compatibility matrix, local pressure
observation and benchmark refresh also add no maturity points. They close one bounded-loading
engineering risk but do not provide streaming, hostile-OS security certification, M6 evidence,
release approval or submission readiness. Closing the aggregate coverage floor through public
resource-boundary characterization also does not change the readiness score.

## Strongest adverse case

The project is still more incomplete than complete. The current 95.14908256880734%
branch-aware combined-opportunity coverage applies to the
implemented in-memory M0-M2 surface, not the intended full SoftwareX product. There is no
evidence that SelCal controls error under relevant data-generating processes, improves a
research workflow relative to credible alternatives, or can be independently installed
and reused outside the current machine. A polished README, deterministic synthetic example
and same-machine isolated installation cannot close those gaps.
The new benchmark is a descriptive local characterization with only three repeats per case;
it cannot establish portability, speedup, parallel scaling or comparative workflow benefit.

The stale Task-10 scope-v1 route is also a real failure, not cosmetic noise. It proves the
current authority package no longer binds the current worktree. Refreezing the old 109-file
manifest would be brittle and would not establish dependency closure.
The new licence inventory additionally shows that exact-version package metadata is not a
release licence closure: the isolated build backend, selected distribution artifacts,
licence files, bundled components and target-specific marker evaluation remain open. The
code audit still shows two open major risks. Passing the branch-aware coverage floor does not
waive those adverse findings or establish science, portability, release or submission readiness.

## Strongest supporting case

The implemented scientific core is unusually well defended for this maturity level:
contracts are fail-closed, full reselection is executable, deterministic identities are
checked, adverse outcomes are retained, coverage is high, and the user-facing examples and
generated documentation are tested and filtered for local paths, debug calls and credential
material. The benchmark adds an exact source/harness/contract-bound receipt and reproducible
paper figure without raising the scientific claim ceiling.
This justifies continuing development, but not drafting impact claims.

## Neutral decision

Continue the SelCal route. The next controlling gate is an explicitly approved
scope-v2 dependency-closure design followed by TDD implementation and fresh exact-byte
review. While that approval remains absent, the safe independent sequence is to freeze the
hidden-runtime-state boundary before M3.
After authority closure, implement
M3-M5 before executing the prospective M6 comparison and real-case protocol. UI, public
release and the SoftwareX manuscript remain downstream.

Largest reversal variable: if a properly frozen M6 study fails to show valid calibration
or credible research-workflow benefit over relevant alternatives, the SoftwareX claim must
be narrowed or the route stopped regardless of engineering quality.
