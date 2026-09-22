# M6-P1 independent reference resource envelope v1.1 — revision 2 proposal

> **Status:** `REVISED PROPOSAL / NOT APPROVED / NOT FROZEN / NOT IMPLEMENTATION AUTHORITY / M6 NOT EXECUTED`

> **Predecessor:** The 15,105-byte first proposal, SHA-256 `e26bd921656e636b33e67fbe98f0cea0e4c67e382b51c69a4045707c9b65a7eb`, was independently rejected for two critical capacity-contract defects. This revision preserves it as an audit preimage and does not treat it as authority.

> **Decision boundary:** This document proposes a bounded, streaming materialization contract for M6-P1. It does not authorize source or test implementation, set a scientific success threshold, change SelCal's public input contract, or establish M6/SoftwareX readiness.

## 1. Bound authority and current evidence

This proposal supplements, but does not modify or supersede, the following current bytes:

| Item | Current identity |
| --- | --- |
| Parent design | `docs/benchmarks/2026-09-06-m6-p1-independent-reference-design.md` |
| Parent bytes / SHA-256 | `34234` / `ab6e40cc57eb5e4272451ebcb227eab45bf45f1ca66795530adb8d9957490064` |
| Existing streaming oracle | `src/selcal/exact_oracle_v0.py`, SHA-256 `ffbf002949a9a7530fa4a99aa62bd6125515866533c176f9306754d93b9aade7` |
| Current production calibration | `src/selcal/calibration_v2.py`, SHA-256 `a5249d5facfbcfa8f28b98a70115dbd5ae197e9c1743796fb2fe7e32371e3900` |
| Checked date | `2026-09-07` |

The parent design currently asks for an ordered in-memory `states` tuple whose rows retain complete transformed sources. Its existing `max_exact_state_count=100000` does not bound state count times series length. This is a capacity proof, not an executed allocation:

```text
n = 100000
candidates = (1,)
null = circular_shift_v2(min_shift=1)
T = n - 2*min_shift + 2 = 100000
retained transformed-source entries = T*n = 10,000,000,000
lower-bound payload at 8 bytes per entry = 80,000,000,000 bytes
```

The lower bound excludes Python containers, records, statistics and serialized output. The parent state remains `RESOURCE_ENVELOPE_REVISION_REQUIRED / NOT FROZEN / NOT EXECUTED` until this replacement contract and all proposed numbers are approved.

## 2. Proposed architectural decision

Replace the retained all-state tuple with ordered row streaming and canonical JSONL artifacts. Retain at most one transformed source, one complete candidate vector and one serialized result row in memory at a time. Rotate output files after a deterministic row count; do not buffer a whole chunk in memory.

For a supplied finite-B schedule, use **two passes**:

1. consume the external iterable exactly once without running any statistic;
2. validate every `rowIndex`, state payload, membership rule and planned row count;
3. write only canonical compact state-label rows to a byte-capped schedule spool;
4. close, re-read and verify the spool's row count and SHA-256;
5. only after the complete spool passes, scan observed data and replay the spool for statistics.

This resolves the conflict between a one-shot iterable and pre-statistic validation. The schedule spool becomes a retained, hash-bound input sidecar for the run; it is not a result ledger and contains no estimates.

The materialization change must preserve these invariants:

1. enumerate or replay every admitted labelled state in its specified order;
2. preserve identity, repeated numerical arrays and repeated mathematical state labels at different row indices;
3. reject only missing, duplicate or noncanonical `rowIndex` values; repeated state labels are valid and retained;
4. construct each transformed source independently from the original source and state label;
5. finish the full candidate vector for one state before selection;
6. compare reference and production rows without using production values as reference inputs;
7. accumulate exact denominators, `E`, `F` and inclusive tail indicators online under the mode-specific rules in section 7;
8. never truncate, deduplicate, silently use Monte Carlo, or recast a resource rejection as analytical failure;
9. never retain transformed source values in a completed row.

The existing V0 oracle demonstrates only that single-state streaming is feasible. It remains scientifically non-independent because it reuses production statistics and selection.

## 3. Modes, symbols and scan accounting

The request has an exact discriminator:

```text
calculationMode = ALL_STATE_EXACT | FINITE_B_SCHEDULE
```

Let:

| Symbol | Meaning |
| --- | --- |
| `n` | common input-series length |
| `h` | `max(candidates)` |
| `N` | common support length `n-h` |
| `C` | candidate count |
| `T` | exact labelled-state count |
| `B` | explicitly planned finite schedule rows |
| `Q` | total statistic scans, including observed where separately required |
| `X` | transformed state rows |
| `L` | completed result-ledger rows |
| `S` | null-side work: `1` for circular shift, block count `q=n/block_length` for block shuffle |
| `bins` | NetTE bin count; not applicable to Pearson |
| `K` | rows per on-disk chunk; derived, never caller supplied |

Mode accounting is fixed:

| Mode | `Q` statistic scans | `X` transformed rows | `L` result rows | Observed record |
| --- | ---: | ---: | ---: | --- |
| `ALL_STATE_EXACT` | `T` | `T` conservatively, including identity | `T` | identity result row; no second scan |
| `FINITE_B_SCHEDULE` | `B+1` | `B` | `B` plus one separate observed record | required before scheduled rows |

The exact identity state is evaluated once. The schedule observed scan is an additional scan and is never omitted from candidate or statistic work.

## 4. Request-derived resource operands

All products use guarded integer arithmetic. `bit_length()` checks occur before multiplication, exponentiation or incremental factorial work can exceed the operand boundary.

Common operands:

```text
transform_value_visits = X*n
candidate_support_visits = Q*C*N
ledger_candidate_records = L*C
live_candidate_records = C
edge_entries = 2*(bins+1)                              # NetTE only
u3 = min(N, bins**3)                                   # guarded power
u2 = min(N, bins**2)
u1 = min(N, bins)
counter_entries_upper = 2*(u3 + 2*u2 + u1)             # NetTE, one candidate scan
```

Statistic-specific CPU proxies are deliberately separated:

```text
pearson_value_visits = 6*Q*C*N

nette_directional_support_visits = 2*Q*C*N
nette_counter_update_visits = 8*Q*C*N
nette_sort_key_visits = 2*Q*C*u3*ceil_log2(max(2, u3))

reference_work_units =
    transform_value_visits + pearson_value_visits                  # Pearson
    transform_value_visits + 2*Q*n
        + nette_counter_update_visits + nette_sort_key_visits      # NetTE
```

`2*Q*n` conservatively includes source/target coding work for NetTE. `counter_entries_upper` bounds simultaneously live forward/reverse diagnostic tables for one candidate; it is not a substitute for CPU work.

## 5. Canonical bytes and reconstructability

Canonicalization version: `selcal-m6-p1-jsonl-v1`.

Every JSON object is encoded by the functional equivalent of:

```python
json.dumps(
    value,
    ensure_ascii=True,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
```

Every JSONL row is exactly those bytes plus one LF byte (`0x0a`), with no BOM or CRLF. JSON integers use minimal decimal form. Scientific binary64 values are never emitted as JSON numbers: they are strings from `float.hex()`, preserving signed zero. Hashes are lowercase 64-hex. All record types have exact-key schemas; unknown keys fail.

The primary ledger SHA-256 is updated over every canonical row byte sequence in global `rowIndex` order, independent of file rotation. A chunk SHA-256 covers exactly its consecutive row bytes. `orderedChunkSha256s` binds chunk order. The verifier concatenates chunk bytes in that order and reproduces both row count and primary digest.

### 5.1 Retained input sidecars

Hash values alone are not reconstruction data. A complete run package retains:

- `original-input.json`: both complete input series encoded as ordered `float.hex()` strings;
- `reference-spec.json`: the complete primitive reference request and canonicalization version;
- for schedule mode, `schedule-spool.jsonl`: validated `rowIndex` plus complete state payload.

The manifest binds each sidecar with exact relative path, media type, byte count, SHA-256 and canonicalization version. A transformed source is reconstructable only **given these retained sidecar bytes after their identities reverify**. Loss of a required sidecar makes the package incomplete.

Schedule spool rows are exactly:

```text
{rowIndex: built-in int, state: {kind, exact state payload}}
```

Circular payload is `{kind:"circular_shift",offset:int}`. Block payload is `{kind:"block_permutation",order:[int,...]}`. The first pass requires `rowIndex=0..B-1` exactly. Equal `state` objects at different row indices are accepted and preserved.

## 6. Executable byte upper bounds

These constants are conservative engineering proposals, not measurements of scientific validity:

```text
FLOAT_HEX_JSON_BYTES = 32
FAILURE_CODE_JSON_BYTES = 66             # quotes plus <=64 ASCII [A-Z0-9_]
HASH_JSON_BYTES = 66
SEQUENCE_VALUE_PEAK_BYTES = 64
COUNTER_ENTRY_PEAK_BYTES = 512
SORT_ENTRY_PEAK_BYTES = 64
FIXED_RUNTIME_OVERHEAD_BYTES = 1048576
FIXED_CANDIDATE_JSON_BYTES = 512
FIXED_SELECTION_JSON_BYTES = 512
FIXED_STATE_ROW_JSON_BYTES = 1024
FIXED_OBSERVED_ROW_JSON_BYTES = 1024
FIXED_MANIFEST_JSON_BYTES = 16384
FIXED_CHUNK_MANIFEST_ENTRY_BYTES = 256
```

`digits(x)` is the count of minimal decimal digits of nonnegative integer `x`, calculated by guarded integer division. Let `M=max(n,C,h,T if exact else B,1)`.

```text
candidate_record_json_upper =
    FIXED_CANDIDATE_JSON_BYTES + 6*digits(M) + 4*FLOAT_HEX_JSON_BYTES
    + FAILURE_CODE_JSON_BYTES

selection_json_upper =
    FIXED_SELECTION_JSON_BYTES + 6*digits(M)
    + C*(digits(max(C-1,0))+1) + 3*FLOAT_HEX_JSON_BYTES

circular_state_json_upper = 128 + digits(n)
block_state_json_upper = 128 + q*(digits(max(q-1,0))+1)
state_json_upper = the applicable value above

state_row_json_upper =
    FIXED_STATE_ROW_JSON_BYTES + state_json_upper
    + C*candidate_record_json_upper + selection_json_upper + 1 LF byte

observed_row_json_upper =
    FIXED_OBSERVED_ROW_JSON_BYTES
    + C*candidate_record_json_upper + selection_json_upper + 1 LF byte

K = min(max(L,1), max_chunk_rows)
chunk_count = ceil(L/K)
manifest_json_upper =
    FIXED_MANIFEST_JSON_BYTES
    + chunk_count*FIXED_CHUNK_MANIFEST_ENTRY_BYTES

primary_ledger_bytes_upper =
    L*state_row_json_upper + manifest_json_upper
    + (observed_row_json_upper if schedule else 0)
    + exact canonical byte counts of original-input.json and reference-spec.json
    + (exact verified schedule-spool bytes if schedule else 0)
```

Exact-key schemas, bounded failure-code tokens and the absence of free-text messages are prerequisites for this formula. The first TDD task must construct every maximum-shape schema instance and prove its canonical length is no larger than the formula. Adding a field or widening an enum invalidates that proof and requires a formula/version change.

The primary ledger has both guards:

1. reject before statistics when `primary_ledger_bytes_upper` exceeds `max_primary_ledger_bytes`;
2. count actual emitted bytes online. Exceeding the cap despite an admitted upper bound is `REFERENCE_INTEGRITY_FAILURE / ACTUAL_PRIMARY_LEDGER_BYTE_LIMIT`, not a successful resource rejection; retain only a clearly named `PARTIAL` temporary artifact and never issue `COMPLETE`.

### 6.1 Reference-owned peak estimate

The implementation must evaluate one state and one candidate's Counter set at a time. It writes each row immediately; chunk rotation does not buffer K rows.

```text
transformed_buffer_peak = n*SEQUENCE_VALUE_PEAK_BYTES
candidate_vector_peak = C*candidate_record_json_upper
active_row_peak = state_row_json_upper

pearson_workspace_peak = 6*N*SEQUENCE_VALUE_PEAK_BYTES

nette_workspace_peak =
    4*n*SEQUENCE_VALUE_PEAK_BYTES
    + edge_entries*SEQUENCE_VALUE_PEAK_BYTES
    + counter_entries_upper*COUNTER_ENTRY_PEAK_BYTES
    + counter_entries_upper*SORT_ENTRY_PEAK_BYTES

reference_owned_peak_estimated_bytes =
    FIXED_RUNTIME_OVERHEAD_BYTES + transformed_buffer_peak
    + candidate_vector_peak + active_row_peak
    + (pearson_workspace_peak or nette_workspace_peak)
```

Before statistics, current-runtime layout probes must show that a representative sequence element, Counter entry and sort reference do not exceed their proposed constants. Otherwise return `REFERENCE_RESOURCE_LIMIT / RUNTIME_LAYOUT_UNSUPPORTED`. A bounded `tracemalloc` characterization after implementation is corroborating evidence, not a replacement for preflight.

### 6.2 Disagreement diagnostics

Full NetTE integer tables are produced only after a comparison discrepancy, by independently recomputing that state/candidate under the same inputs. They are written to a separate canonical diagnostic JSONL and cannot alter the already computed estimate or comparison.

For one candidate:

```text
counter_key_json_upper = 128 + 4*digits(max(bins-1,N,1))
single_diagnostic_json_upper =
    2048 + counter_entries_upper*counter_key_json_upper + 1 LF byte
```

Preflight requires one complete diagnostic row to fit `max_single_diagnostic_bytes`. Actual discrepancy count is data-dependent, so diagnostic bytes are separately counted at runtime. Before appending a whole next diagnostic row, its exact canonical bytes must fit the remaining `max_diagnostic_ledger_bytes`; otherwise the run ends as `REFERENCE_RESOURCE_LIMIT / DIAGNOSTIC_LEDGER_BYTE_LIMIT_RUNTIME`, marks diagnostics `PARTIAL`, and cannot claim complete agreement/disagreement characterization. A partial diagnostic ledger is never referenced by a `COMPLETE` comparison manifest.

## 7. Mode-specific result contracts

Common row fields are exact and closed:

```text
schemaVersion, canonicalizationVersion, calculationMode, rowIndex,
state, isIdentity, candidateRecords, selection, tailIndicator,
failureStage, failureCode, originalInputSha256, referenceSpecSha256
```

Candidate records are exact and closed:

```text
candidateIndex, candidate, estimateHex, unscoredValueHex, scoreHex,
supportCount, valid, failureCode
```

Selection is exact and closed:

```text
selectedIndex, selectedCandidate, tiedCandidateIndices,
familyMaximumHex, selectedSignedEstimateHex
```

Failure codes are null or ASCII `[A-Z0-9_]{1,64}`; no free-text exception message enters a canonical row. Nullability is fixed by validity in the schema. Disagreement residuals are `float.hex()` strings in the comparison record. Diagnostic Counter entries are sorted lexicographically and encoded as arrays of integer key components followed by their integer count.

### 7.1 `ALL_STATE_EXACT`

The manifest discriminator is `calculationMode=ALL_STATE_EXACT` and contains:

```text
terminalStatus
totalStateCount = T
identityRowIndex
failureStateCount
nonidentityExceedanceCount
unreducedNumerator
unreducedDenominator
pExactHex
decision
```

Identity is in the table and scanned once, but excluded from `nonidentityExceedanceCount`. If every required scan is valid, `unreducedNumerator=1+E`, `unreducedDenominator=T`, and `pExactHex=float.hex((1+E)/T)`. If any required scan fails, `terminalStatus=ANALYTICALLY_UNEVALUABLE`; `failureStateCount` remains an exact integer, while `nonidentityExceedanceCount`, numerator, denominator, p-value and decision are null as required by the parent design.

### 7.2 `FINITE_B_SCHEDULE`

The manifest discriminator is `calculationMode=FINITE_B_SCHEDULE` and contains:

```text
terminalStatus
plannedB = B
observedRecordIdentity
validReplicateCount
E
F
lowerNumerator
upperNumerator
denominator = B+1
pValueHex
decision
```

The observed vector is retained in a separate closed observed record. Every planned schedule row remains in the ledger; sampled identities and repeated state labels count as separate rows. `E` counts inclusive exceedances among that side's valid scheduled rows. `F` counts analytically failed scheduled rows. The bounds are `(1+E)/(B+1)` and `(1+E+F)/(B+1)`. `pValueHex` and decision are non-null only when the observed scan is valid and `F=0`; otherwise the terminal status and nullability follow the parent failure contract. Resource failure has no E/F or inferential fields and uses the common fail-closed record in section 9.

Exact and finite-B manifests are distinct schemas under the discriminator; fields from the other mode are forbidden.

## 8. Proposed budget profile

Profile identifier: `m6-p1-reference-envelope-v1.1-revision2-proposal`.

| Field | Proposed value | Authority status |
| --- | ---: | --- |
| `max_exact_state_count` | `100000` | Existing parent limit |
| `retained_transformed_source_entries` | exactly `0` | Required invariant |
| `max_schedule_rows` | `1000` | **PROPOSED** |
| `max_operand_bits` | `256` | **PROPOSED** |
| `max_transform_value_visits` | `2500000` | **PROPOSED** |
| `max_candidate_support_visits` | `2500000` | **PROPOSED** |
| `max_pearson_value_visits` | `15000000` | **PROPOSED** |
| `max_nette_directional_support_visits` | `5000000` | **PROPOSED** |
| `max_nette_counter_update_visits` | `20000000` | **PROPOSED** |
| `max_nette_sort_key_visits` | `25000000` | **PROPOSED** |
| `max_reference_work_units` | `30000000` | **PROPOSED** |
| `max_ledger_candidate_records` | `100000` | **PROPOSED** |
| `max_live_candidate_records` | `5000` | **PROPOSED** |
| `max_chunk_rows` | `256` | **PROPOSED**, deterministic rotation only |
| `max_edge_entries` | `65536` | **PROPOSED** |
| `max_counter_entries_upper` | `250000` | **PROPOSED** |
| `max_input_sidecar_bytes` | `67108864` | **PROPOSED**, 64 MiB |
| `max_schedule_spool_bytes` | `16777216` | **PROPOSED**, 16 MiB |
| `max_primary_ledger_bytes` | `268435456` | **PROPOSED**, 256 MiB |
| `max_reference_owned_peak_estimated_bytes` | `536870912` | **PROPOSED**, 512 MiB |
| `max_single_diagnostic_bytes` | `16777216` | **PROPOSED**, 16 MiB |
| `max_diagnostic_ledger_bytes` | `67108864` | **PROPOSED**, 64 MiB |

If `C>max_live_candidate_records`, no single complete candidate vector can be admitted and the request fails. `K=min(max(L,1),max_chunk_rows)` is internal and cannot trigger a caller-facing chunk-row error.

These are engineering coverage caps. They do not set Type-I error, power, acceptable disagreement, minimum coverage or external validity. Values require explicit approval before implementation. If they exclude substantively important cases, the scientific claim ceiling must narrow.

## 9. Fixed validation and rejection order

The global request path is:

1. validate primitive types, closed shapes, booleans, signs and finite values;
2. apply the 256-bit operand guard before products, powers or factorial expansion;
3. validate null applicability and incrementally determine exact T where needed;
4. derive mode-specific Q/X/L and validate state/schedule/candidate counts;
5. validate transform, support, statistic-specific work and total-work caps;
6. validate NetTE edge/Counter/sort bounds where applicable;
7. canonicalize input/spec sidecars and validate their exact bytes;
8. derive and validate static primary-ledger and peak-memory upper bounds;
9. for schedule mode only, consume and validate the complete iterable into the bounded canonical spool, then re-read its count/hash;
10. only after steps 1–9 pass may statistic scans and primary result-ledger creation begin.

A schedule row that fails during step 9 causes no statistic scan and no primary ledger. A spool overrun produces no `COMPLETE` spool. The bounded spool is the explicit exception to “no file before statistics”: it is a validated input sidecar, not a result.

Every ordinary resource rejection returns at least:

```json
{
  "status": "REFERENCE_RESOURCE_LIMIT",
  "limitCode": "<stable code>",
  "limit": 0,
  "observed": 0,
  "observedAtLeast": null,
  "budgetProfileId": "m6-p1-reference-envelope-v1.1-revision2-proposal",
  "calculationMode": "ALL_STATE_EXACT",
  "derivedOperands": {},
  "resultLedger": null,
  "E": null,
  "F": null,
  "pValue": null,
  "decision": null
}
```

Exactly one of `observed` and `observedAtLeast` is populated. The latter is used for an incremental stop before an exact unsafe operand is calculated.

Stable proposed codes are:

```text
OPERAND_BITS_LIMIT
RUNTIME_LAYOUT_UNSUPPORTED
EXACT_STATE_COUNT_LIMIT
SCHEDULE_ROW_LIMIT
SCHEDULE_SPOOL_BYTE_LIMIT
TRANSFORM_VALUE_VISIT_LIMIT
CANDIDATE_SUPPORT_VISIT_LIMIT
PEARSON_VALUE_VISIT_LIMIT
NETTE_DIRECTIONAL_SUPPORT_VISIT_LIMIT
NETTE_COUNTER_UPDATE_VISIT_LIMIT
NETTE_SORT_KEY_VISIT_LIMIT
REFERENCE_WORK_UNIT_LIMIT
LEDGER_CANDIDATE_RECORD_LIMIT
LIVE_CANDIDATE_RECORD_LIMIT
EDGE_ENTRY_LIMIT
COUNTER_ENTRY_LIMIT
INPUT_SIDECAR_BYTE_LIMIT
PRIMARY_LEDGER_BYTE_UPPER_LIMIT
ESTIMATED_PEAK_BYTE_LIMIT
SINGLE_DIAGNOSTIC_BYTE_LIMIT
DIAGNOSTIC_LEDGER_BYTE_LIMIT_RUNTIME
```

`ACTUAL_PRIMARY_LEDGER_BYTE_LIMIT` is reserved for `REFERENCE_INTEGRITY_FAILURE`, because an admitted static upper bound should make it unreachable. No rejection may truncate states, remove identities/repeats, widen a numerical tolerance or fall back to Monte Carlo.

## 10. Atomic custody

Sidecars, spool, chunks, diagnostics and manifests are first written under explicit `.partial` names. The final comparison manifest is installed atomically only after:

1. all expected rows and sidecars re-read successfully;
2. exact schemas and modes validate;
3. row indices are continuous and counts match;
4. per-artifact bytes and SHA-256 reproduce;
5. primary ledger byte count is within its admitted upper bound and hard cap;
6. no diagnostic resource failure or integrity failure remains.

An interruption, schedule error, runtime limit or integrity mismatch leaves at most clearly named `PARTIAL` artifacts and never a `COMPLETE` manifest. Resume behavior is not authorized by this proposal; a later run may restart from immutable sidecars.

## 11. Minimum TDD sequence after explicit approval

Nothing in this section has been run. Approval would authorize only this order:

- [ ] **R1 — Canonical schema and byte-bound RED/GREEN.** Test exact keys, float hex/signed zero, LF framing, hash concatenation and maximum-shape instances against every formula. Mutating a schema without a formula/version change must fail.
- [ ] **R2 — Guarded integer preflight RED/GREEN.** Test the `10^10` counterexample without allocation; every `limit-1/limit/limit+1`; booleans, negatives and oversized operands. Bomb all edge/statistic/enumerator/writer functions.
- [ ] **R3 — Two-pass schedule spool RED/GREEN.** Use a one-shot generator. Test early/late EOF, membership and duplicate/missing `rowIndex` before any statistic; accept equal state labels at different row indices; test byte cap, re-read count and digest.
- [ ] **R4 — Mode accounting RED/GREEN.** Prove exact scans T rows once and schedule scans B+1; observed schedule work and record cannot be omitted. Test distinct exact/schedule schemas, identity handling, E/F, denominators and nullability.
- [ ] **R5 — Single-row streaming RED/GREEN.** Use the disclosed six-state Pearson fixture; require exact order, multiplicity, reselection and `p_exact=3/6`; assert no completed row contains transformed values and no chunk buffers prior rows.
- [ ] **R6 — NetTE resource and diagnostic RED/GREEN.** Test two-direction/eight-Counter/sort formulas, peak estimate, single diagnostic and cumulative diagnostic cap before/while writing. Small disclosed NetTE arithmetic must remain unchanged.
- [ ] **R7 — Atomic ledger RED/GREEN.** Test chunk rotation, global concatenated hash, final byte count, sidecar identities and every partial-failure point. No failure may issue `COMPLETE`.
- [ ] **R8 — Independence and regression.** In a fresh subprocess block `selcal`, `numpy` and `scipy` imports for the reference package; then run existing oracle, selection and calibration finalization/failure regressions. Bounded peak-memory characterization runs last.

Each RED must fail for absent intended behavior, not an import or fixture mistake. Source-changing operations finish before hashes and receipts freeze.

## 12. Decisions required before implementation

A specification owner must explicitly:

1. approve, revise or reject every **PROPOSED** number and byte-size constant;
2. approve the two-pass retained schedule spool;
3. approve the byte canonicalization and exact row/manifest schemas;
4. approve mode-specific scan, identity, E/F, denominator and failure semantics;
5. approve NetTE CPU/Counter/sort formulas and diagnostic recomputation;
6. decide whether the proposed CPython layout constants are supported only on the tested runtime or across a declared version matrix;
7. confirm that envelope-excluded cases narrow implementation coverage rather than disappearing from the scientific target population.

## 13. Claim ceiling

Even after approval and successful implementation, this envelope could show only that the independent reference fails closed before documented resource hazards and preserves admitted state/schedule rows under a reproducible streaming contract. It cannot establish:

- M6 scientific validation or completion;
- empirical superiority over comparator software;
- exchangeability, Type-I-error control, power or external validity;
- real-research usefulness or usability;
- complete runtime/platform coverage;
- SoftwareX readiness, upload readiness, submission, acceptance or likely review outcome.

Until section 12 is explicitly approved and recorded, the controlling state remains:

```text
RESOURCE_ENVELOPE_REVISION_REQUIRED
NOT APPROVED
NOT FROZEN
NOT IMPLEMENTED
M6 NOT EXECUTED
```
