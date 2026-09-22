# M6-P1 resource envelope v1.1 revision 3 formula attachment

> **Status:** `PROPOSAL / NOT APPROVED / NOT FROZEN / NOT IMPLEMENTATION AUTHORITY / M6 NOT EXECUTED`

> **Scope:** This attachment contains only resource-accounting, bounded-integer,
> artifact-state, and failure-custody contracts. It does not change statistical
> semantics, establish a scientific threshold, authorize implementation, or establish
> M6 or SoftwareX readiness.

## 1. Bound inputs and authority

This proposal binds the following current bytes, measured on 2026-09-07:

| Item | Bytes authority |
| --- | --- |
| Revision 2 proposal | `docs/benchmarks/2026-09-07-m6-p1-resource-envelope-v1_1-revision2-proposal.md`, SHA-256 `4dd1c160bd89ce03530d173d580ffdbaf4f58953b1579496223804b2ebc5e609` |
| Parent independent-reference design | `docs/benchmarks/2026-09-06-m6-p1-independent-reference-design.md`, SHA-256 `ab6e40cc57eb5e4272451ebcb227eab45bf45f1ca66795530adb8d9957490064` |

Revision 2 remains a proposal. This attachment replaces no parent text and grants no
authority. The inherited `max_exact_state_count=100000` remains a necessary parent
limit, not approval of any new number in this attachment.

## 2. Symbols and dimensional rule

All byte formulae return bytes. All visit and work formulae return dimensionless
accounted work units. Counts are nonnegative exact built-in integers; booleans are
rejected. Let:

```text
n      = common input-series length
h      = max(candidates)
N      = n-h
C      = candidate count
T      = exact labelled-state count
B      = planned schedule row count
Q      = T for ALL_STATE_EXACT; B+1 for FINITE_B_SCHEDULE
X      = T for ALL_STATE_EXACT; B for FINITE_B_SCHEDULE
L      = T for ALL_STATE_EXACT; B for FINITE_B_SCHEDULE
q      = n/block_length for an applicable block null
M      = max(n, h, C, T if exact else B, 1)
K      = min(max(L, 1), max_chunk_rows)
```

The exact mode has no schedule spool and no separate observed row. The schedule mode
has `B` scheduled primary rows and one separate observed row. Every addition,
multiplication, ceiling, power, factorial, and byte total below uses section 3's
guarded integer algorithms.

## 3. Guarded pure-integer algorithms

Set:

```text
OPERAND_MAX = 2**max_operand_bits - 1
```

Constructing `OPERAND_MAX` is profile setup. Request-derived arithmetic must use the
following algorithms or an extensionally identical implementation:

```python
def require_nonnegative_builtin_int(value):
    if type(value) is not int or value < 0:
        fail("INVALID_INTEGER_OPERAND")


def guarded_add(a, b):
    require_nonnegative_builtin_int(a)
    require_nonnegative_builtin_int(b)
    if a > OPERAND_MAX or b > OPERAND_MAX or a > OPERAND_MAX - b:
        fail("OPERAND_BITS_LIMIT")
    return a + b


def guarded_mul(a, b):
    require_nonnegative_builtin_int(a)
    require_nonnegative_builtin_int(b)
    if a > OPERAND_MAX or b > OPERAND_MAX:
        fail("OPERAND_BITS_LIMIT")
    if a != 0 and b > OPERAND_MAX // a:
        fail("OPERAND_BITS_LIMIT")
    return a * b


def ceil_div_nonnegative(a, b):
    require_nonnegative_builtin_int(a)
    if type(b) is not int or b <= 0:
        fail("INVALID_INTEGER_OPERAND")
    quotient, remainder = divmod(a, b)
    return guarded_add(quotient, int(remainder != 0))


def ceil_log2_positive(value):
    if type(value) is not int or value < 1:
        fail("INVALID_INTEGER_OPERAND")
    if value > OPERAND_MAX:
        fail("OPERAND_BITS_LIMIT")
    return (value - 1).bit_length()


def decimal_digits_nonnegative(value):
    require_nonnegative_builtin_int(value)
    if value > OPERAND_MAX:
        fail("OPERAND_BITS_LIMIT")
    if value == 0:
        return 1
    digits = 0
    while value:
        value //= 10
        digits += 1
    return digits
```

`(a+b-1)//b`, floating logarithms, and string conversion are forbidden in resource
ceilings. To calculate `min(cap, base**exponent)` without constructing an unsafe
power:

```python
def min_power_cap(base, exponent, cap):
    require_nonnegative_builtin_int(base)
    require_nonnegative_builtin_int(exponent)
    require_nonnegative_builtin_int(cap)
    if cap > OPERAND_MAX:
        fail("OPERAND_BITS_LIMIT")
    if cap == 0:
        return 0
    value = 1
    for _ in range(exponent):
        if base != 0 and value > cap // base:
            return cap
        value = guarded_mul(value, base)
    return min(value, cap)
```

For block enumeration, do not construct an over-limit factorial:

```python
state_count = 1
for factor in range(2, q + 1):
    if state_count > max_exact_state_count // factor:
        fail(
            "EXACT_STATE_COUNT_LIMIT",
            observed=None,
            observedAtLeast=max_exact_state_count + 1,
        )
    state_count = guarded_mul(state_count, factor)
```

Every relevant limit must be strictly below `OPERAND_MAX`, so `limit+1` is safe.
When an exact unsafe value is deliberately not constructed, populate
`observedAtLeast=limit+1` and leave `observed=null`.

## 4. Closed-schema byte upper bounds

The canonicalization remains the revision 2 canonical UTF-8 JSON/JSONL contract.
All rows have exact keys, fixed enums, bounded ASCII failure codes, bounded generated
relative paths, and no free text. A schema field addition, wider enum, caller-supplied
path, or free-text exception invalidates these formulae until the schema version and
maximum-shape proof are revised.

State and primary-row bounds remain:

```text
circular_state_json_upper = 128 + digits(n)
block_state_json_upper = 128 + q*(digits(max(q-1, 0))+1)
state_json_upper = applicable bound above

candidate_record_json_upper =
    FIXED_CANDIDATE_JSON_BYTES
    + 6*digits(M)
    + 4*FLOAT_HEX_JSON_BYTES
    + FAILURE_CODE_JSON_BYTES

selection_json_upper =
    FIXED_SELECTION_JSON_BYTES
    + 6*digits(M)
    + C*(digits(max(C-1, 0))+1)
    + 3*FLOAT_HEX_JSON_BYTES

state_row_json_upper =
    FIXED_STATE_ROW_JSON_BYTES
    + state_json_upper
    + C*candidate_record_json_upper
    + selection_json_upper
    + 1

observed_row_json_upper =
    FIXED_OBSERVED_ROW_JSON_BYTES
    + C*candidate_record_json_upper
    + selection_json_upper
    + 1
```

Schedule and comparison bounds are newly explicit:

```text
schedule_spool_row_upper =
    FIXED_SCHEDULE_SPOOL_ROW_JSON_BYTES
    + digits(max(B-1, 0))
    + state_json_upper
    + 1

comparison_cell_json_upper =
    FIXED_COMPARISON_CELL_JSON_BYTES
    + 8*digits(M)
    + 4*FLOAT_HEX_JSON_BYTES
    + 2*FAILURE_CODE_JSON_BYTES

comparison_row_json_upper =
    FIXED_COMPARISON_ROW_JSON_BYTES
    + state_json_upper
    + C*comparison_cell_json_upper
    + 1
```

The comparison row schema must be a bounded projection. It may contain stable codes,
hexadecimal binary64 values, residuals, and exact candidate/state identities. It may
not embed production exception text, arbitrary diagnostics, or a caller-owned result
object.

Chunk and index bounds are:

```text
primary_chunk_count = ceil_div_nonnegative(L, K)
comparison_chunk_count = ceil_div_nonnegative(Q, max_chunk_rows)
diagnostic_chunk_count_upper =
    ceil_div_nonnegative(max_diagnostic_recomputations, max_chunk_rows)

primary_index_json_upper =
    FIXED_MANIFEST_JSON_BYTES
    + primary_chunk_count*FIXED_CHUNK_MANIFEST_ENTRY_BYTES

comparison_index_json_upper =
    FIXED_MANIFEST_JSON_BYTES
    + comparison_chunk_count*FIXED_CHUNK_MANIFEST_ENTRY_BYTES

diagnostic_index_json_upper =
    FIXED_MANIFEST_JSON_BYTES
    + diagnostic_chunk_count_upper*FIXED_CHUNK_MANIFEST_ENTRY_BYTES
```

For NetTE:

```text
edge_entries = 2*(bins+1)
u3 = min_power_cap(bins, 3, N)
u2 = min_power_cap(bins, 2, N)
u1 = min(N, bins)
counter_entries_one_direction_upper = u3 + 2*u2 + u1
counter_entries_upper = 2*counter_entries_one_direction_upper

counter_key_json_upper = 128 + 4*digits(max(bins-1, N, 1))
single_diagnostic_json_upper =
    FIXED_DIAGNOSTIC_ROW_JSON_BYTES
    + counter_entries_upper*counter_key_json_upper
    + 1
```

Preflight requires `single_diagnostic_json_upper <=
max_single_diagnostic_bytes`. Every maximum-shape schema must be constructed in a
bounded test and its actual canonical length shown not to exceed its formula.

## 5. Two-stage schedule run-package upper bound

The primary, diagnostic, comparison, sidecar, and top-level artifacts are separate
accounts. Define:

```text
I = exact bytes(original-input.json) + exact bytes(reference-spec.json)

P_u =
    L*state_row_json_upper
    + (observed_row_json_upper if schedule else 0)
    + primary_index_json_upper

C_u = Q*comparison_row_json_upper + comparison_index_json_upper

D_u = max_diagnostic_ledger_bytes + diagnostic_index_json_upper

artifact_count_upper =
    2
    + (1 if schedule else 0)
    + primary_chunk_count + 1
    + comparison_chunk_count + 1
    + diagnostic_chunk_count_upper + 1
    + 1

success_manifest_json_upper =
    FIXED_SUCCESS_MANIFEST_JSON_BYTES

failure_manifest_json_upper =
    FIXED_FAILURE_MANIFEST_JSON_BYTES
    + artifact_count_upper*FIXED_FAILURE_ARTIFACT_ENTRY_BYTES

artifact_index_json_upper =
    FIXED_ARTIFACT_INDEX_JSON_BYTES
    + artifact_count_upper*FIXED_ARTIFACT_INDEX_ENTRY_BYTES

A_u =
    artifact_index_json_upper
    + max(success_manifest_json_upper, failure_manifest_json_upper)

BASE_u = I + P_u + C_u + D_u + A_u
```

`P_u` excludes `I`, the schedule spool, diagnostics, comparison rows, and the
top-level manifest. Before consuming a supplied one-shot schedule:

```text
require I <= max_input_sidecar_bytes
require P_u <= max_primary_ledger_bytes
require C_u <= max_comparison_ledger_bytes

if BASE_u > max_run_package_bytes:
    fail RUN_PACKAGE_BYTE_UPPER_LIMIT

schedule_spool_formula_upper = B*schedule_spool_row_upper

schedule_spool_admission_bytes = min(
    schedule_spool_formula_upper,
    max_schedule_spool_bytes,
    max_run_package_bytes - BASE_u,
)

run_package_pre_spool_upper =
    BASE_u + schedule_spool_admission_bytes
```

Before appending a complete next spool row, require:

```text
spool_actual_so_far + exact_next_row_bytes
    <= schedule_spool_admission_bytes
```

No partial row may be appended. An overrun is
`REFERENCE_RESOURCE_LIMIT / SCHEDULE_SPOOL_BYTE_LIMIT`; no statistic starts. After
close, fsync, exact B-row re-read, schema validation, and SHA-256 verification:

```text
S_exact = exact verified schedule-spool bytes

run_package_post_spool_upper = BASE_u + S_exact

require S_exact <= schedule_spool_admission_bytes
require run_package_post_spool_upper <= run_package_pre_spool_upper
require run_package_post_spool_upper <= max_run_package_bytes
```

A failed requirement is `REFERENCE_INTEGRITY_FAILURE /
PACKAGE_BOUND_CONTRADICTION`, not an ordinary resource rejection. Exact mode uses
`S_exact=0` and `run_package_upper=BASE_u`.

Primary and comparison writers likewise check the exact complete next row before
append. Their running data bytes plus their admitted index upper must remain within
`P_u` or `C_u`, respectively, and within the corresponding hard ledger cap. Because
those rows already have admitted static upper bounds, an actual overrun is
`REFERENCE_INTEGRITY_FAILURE / ACTUAL_PRIMARY_LEDGER_BYTE_LIMIT` or
`REFERENCE_INTEGRITY_FAILURE / ACTUAL_COMPARISON_LEDGER_BYTE_LIMIT`, never a
successful resource rejection.

`max_run_package_bytes` bounds final retained bytes. Write-time directory occupancy
is separately bounded:

```text
run_directory_transient_upper =
    run_package_pre_spool_upper
    + FAILURE_MANIFEST_RESERVE_BYTES
    + max(success_manifest_json_upper, failure_manifest_json_upper)
```

This transient formula requires same-directory atomic rename and forbids
copy-and-replace. If the filesystem cannot provide the required reservation, fsync,
and atomic rename semantics, artifact-producing execution fails before statistics.

## 6. Phase-separated conditional memory bound

This section bounds reference-owned live objects only under the exact streaming and
runtime-layout conditions stated below. Define:

```text
INPUT_LIVE =
    2*n*SEQUENCE_VALUE_PEAK_BYTES
    + REQUEST_OBJECT_PEAK_BYTES

STATE_LIVE =
    FIXED_STATE_OBJECT_PEAK_BYTES
    + (q*INTEGER_VALUE_PEAK_BYTES if block else INTEGER_VALUE_PEAK_BYTES)

CANDIDATE_VECTOR_LIVE =
    C*CANDIDATE_RECORD_PEAK_BYTES
    + SELECTION_RECORD_PEAK_BYTES

PRIMARY_ENCODED_ROW = max(state_row_json_upper, observed_row_json_upper)

VERIFY_OBJECT_PEAK = max(
    I + 2*n*SEQUENCE_VALUE_PEAK_BYTES,
    exact_reference_spec_bytes + REQUEST_OBJECT_PEAK_BYTES,
    schedule_spool_row_upper + STATE_LIVE,
    PRIMARY_ENCODED_ROW + STATE_LIVE + CANDIDATE_VECTOR_LIVE,
    single_diagnostic_json_upper
        + counter_entries_upper*COUNTER_ENTRY_PEAK_BYTES,
    comparison_row_json_upper + 2*CANDIDATE_VECTOR_LIVE,
    artifact_index_json_upper,
    success_manifest_json_upper,
    failure_manifest_json_upper,
)
```

Each phase is the sum of objects that can be live simultaneously:

```text
peak_input_canonicalization =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + I
    + CANONICAL_ENCODER_SCRATCH_BYTES
    + STREAM_WRITE_BUFFER_BYTES
    + HASH_SCRATCH_BYTES

peak_schedule_spool =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + 2*STATE_LIVE
    + schedule_spool_row_upper
    + CANONICAL_ENCODER_SCRATCH_BYTES
    + STREAM_WRITE_BUFFER_BYTES
    + HASH_SCRATCH_BYTES

peak_primary_pearson =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + n*SEQUENCE_VALUE_PEAK_BYTES
    + 6*N*SEQUENCE_VALUE_PEAK_BYTES
    + 2*CANDIDATE_VECTOR_LIVE
    + STATE_LIVE
    + PRIMARY_ENCODED_ROW
    + comparison_row_json_upper
    + CANONICAL_ENCODER_SCRATCH_BYTES
    + STREAM_WRITE_BUFFER_BYTES
    + HASH_SCRATCH_BYTES

peak_primary_nette =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + n*SEQUENCE_VALUE_PEAK_BYTES
    + 2*n*INTEGER_CODE_PEAK_BYTES
    + edge_entries*SEQUENCE_VALUE_PEAK_BYTES
    + counter_entries_upper*COUNTER_ENTRY_PEAK_BYTES
    + counter_entries_upper*SORT_ENTRY_PEAK_BYTES
    + 2*CANDIDATE_VECTOR_LIVE
    + STATE_LIVE
    + PRIMARY_ENCODED_ROW
    + comparison_row_json_upper
    + CANONICAL_ENCODER_SCRATCH_BYTES
    + STREAM_WRITE_BUFFER_BYTES
    + HASH_SCRATCH_BYTES

peak_diagnostic_recompute_encoding =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + n*SEQUENCE_VALUE_PEAK_BYTES
    + 2*n*INTEGER_CODE_PEAK_BYTES
    + edge_entries*SEQUENCE_VALUE_PEAK_BYTES
    + counter_entries_upper*COUNTER_ENTRY_PEAK_BYTES
    + counter_entries_upper*SORT_ENTRY_PEAK_BYTES
    + single_diagnostic_json_upper
    + CANONICAL_ENCODER_SCRATCH_BYTES
    + STREAM_WRITE_BUFFER_BYTES
    + HASH_SCRATCH_BYTES

peak_verification_reread =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + VERIFY_OBJECT_PEAK
    + STREAM_READ_BUFFER_BYTES
    + CANONICAL_DECODER_SCRATCH_BYTES
    + HASH_SCRATCH_BYTES

reference_owned_peak_upper_bytes = max(
    peak_input_canonicalization,
    peak_schedule_spool if schedule else 0,
    peak_primary_pearson if Pearson else peak_primary_nette,
    peak_diagnostic_recompute_encoding if NetTE else 0,
    peak_verification_reread,
)
```

Admission requires `reference_owned_peak_upper_bytes <=
max_reference_owned_peak_upper_bytes`. The implementation must process one JSONL row
and one candidate at a time. `read()`, `readlines()`, whole-ledger `json.loads()`,
retention of prior chunks, or retention of more objects than a phase formula lists
invalidates admission and fails `REFERENCE_INTEGRITY_FAILURE /
MEMORY_MODEL_VIOLATION`.

Before artifact-producing work, recursive maximum-shape layout probes on the exact
declared CPython/runtime matrix must show that each proposed object constant is not
exceeded. Otherwise return `REFERENCE_RESOURCE_LIMIT /
RUNTIME_LAYOUT_UNSUPPORTED`.

### 6.1 Total-process boundary

The following are not statically bounded by the formula above:

- memory retained inside an arbitrary external schedule iterable or generator;
- production API result objects and third-party-library temporary allocations;
- interpreter/import baseline, allocator fragmentation, garbage-collector timing,
  and operating-system accounting;
- another process's concurrent use of memory or storage.

Therefore this proposal authorizes no `total_process_peak_upper` claim. If such a
claim is required, execution must use a separately approved bounded adapter for the
external producer and production result, plus an enforced subprocess memory limit.
If any required mechanism is unavailable, fail closed with
`TOTAL_PROCESS_RESOURCE_BOUND_UNAVAILABLE`; do not relabel the conditional
reference-owned bound as a process bound. A comparison may not become
`COMPLETE_VERIFIED` under a contract that requires a total-process bound while this
blocker remains.

## 7. NetTE primary and diagnostic CPU work

A work unit is one explicitly counted transform value, coding value, directional
support row, Counter update, bounded merge-sort unit, or emitted canonical byte. It
is not elapsed time and is not a scientific success threshold.

Use an explicitly bounded stable merge sort or an extensionally identical sorter:

```text
sort_units(m) = 0                              if m <= 1
sort_units(m) = 2*m*ceil_log2_positive(m)      if m >= 2
```

If built-in sorting is retained without an instrumented, reviewed comparison bound,
`sort_units` is only a proxy and a strict CPU-work claim is blocked.

Primary NetTE work is:

```text
transform_value_visits = X*n
nette_coding_value_visits = 2*Q*n
nette_directional_support_visits = 2*Q*C*N
nette_counter_update_visits = 8*Q*C*N
nette_primary_sort_units = 2*Q*C*sort_units(u3)

nette_primary_work_units =
    transform_value_visits
    + nette_coding_value_visits
    + nette_directional_support_visits
    + nette_counter_update_visits
    + nette_primary_sort_units
```

Thus the directional count may not be defined and then omitted from the total.
For one discrepant state/candidate diagnostic recomputation:

```text
diagnostic_recompute_one_upper =
    n
    + 2*n
    + 2*N
    + 8*N
    + 2*sort_units(u3)
    + 4*sort_units(u2)
    + 2*sort_units(u1)
    + single_diagnostic_json_upper
    + FIXED_DIAGNOSTIC_WORK_UNITS
```

The already sorted triple-key order must be reused for diagnostic emission. If the
triple tables are sorted again, add another `2*sort_units(u3)`.

The discrepancy count is data-dependent and must not be estimated from an expected
agreement rate. Before each next diagnostic recomputation and before its row append,
require:

```text
diagnostic_count + 1 <= max_diagnostic_recomputations

diagnostic_work_so_far + diagnostic_recompute_one_upper
    <= max_diagnostic_work_units

diagnostic_bytes_so_far + exact_next_diagnostic_row_bytes
    <= max_diagnostic_ledger_bytes
```

The failing row is not partially written. Any failure sets diagnostics and
comparison to `PARTIAL`; it cannot yield complete agreement/disagreement
characterization. Executed work is bounded by:

```text
total_reference_work_upper =
    nette_primary_work_units + max_diagnostic_work_units
```

Admission separately requires the primary operands and
`total_reference_work_upper` to fit their approved caps. Pearson's existing primary
formula remains `transform_value_visits + 6*Q*C*N`; no NetTE diagnostic term may be
silently reused as a Pearson scientific criterion.

## 8. Independent artifact axes and failure custody

The three artifact axes are:

```text
primaryStatus =
    NOT_STARTED | PARTIAL | COMPLETE_VERIFIED

diagnosticStatus =
    NOT_STARTED | NOT_REQUIRED | PARTIAL | COMPLETE_VERIFIED

comparisonStatus =
    NOT_STARTED | PARTIAL | COMPLETE_VERIFIED

comparisonOutcome =
    null | AGREEMENT | DISAGREEMENT | INDETERMINATE

packageStatus =
    FAILED | COMPLETE_VERIFIED
```

Rules are fixed:

1. `primaryStatus=COMPLETE_VERIFIED` means that every expected primary row, byte
   count, schema, order, and digest reverified. It may still contain retained
   analytical failures.
2. If a complete comparison finds no discrepancy,
   `diagnosticStatus=NOT_REQUIRED`. If any discrepancy exists, diagnostics become
   `COMPLETE_VERIFIED` only when every required diagnostic row reverifies.
3. A fully characterized mismatch is
   `comparisonStatus=COMPLETE_VERIFIED` and
   `comparisonOutcome=DISAGREEMENT`. Disagreement is not an execution failure and
   does not depend on a scientific threshold.
4. A diagnostic resource or integrity failure forces
   `diagnosticStatus=PARTIAL`, `comparisonStatus=PARTIAL`, and
   `comparisonOutcome=INDETERMINATE`, even if comparison rows had already been
   emitted.
5. `packageStatus=COMPLETE_VERIFIED` requires all required sidecars,
   `primaryStatus=COMPLETE_VERIFIED`, `comparisonStatus=COMPLETE_VERIFIED`, and
   `diagnosticStatus` in `{NOT_REQUIRED, COMPLETE_VERIFIED}`. It does not imply
   agreement, scientific validity, M6 completion, or readiness.

Before any sidecar, spool, primary, diagnostic, or comparison artifact is written,
reserve and fsync a real,
non-sparse `FAILURE_MANIFEST_RESERVE_BYTES` allocation on the destination
filesystem. If reliable reservation is unavailable, artifact-producing execution
fails before statistics. On failure:

1. stop before a partial next row;
2. close and fsync each existing `.partial` artifact where possible;
3. re-read each artifact and record exact bytes and SHA-256;
4. when re-read fails, record `sha256:null` and `verification:UNVERIFIED`; a writer's
   incremental digest is not a substitute;
5. write a closed-schema failure manifest from the reserved allocation, fsync it,
   and atomically rename it in the same directory;
6. set top-level `E`, `F`, p-value, and decision to null for resource or integrity
   failure.

A failure manifest may reference `PARTIAL` artifacts with their actual custody
state. A success manifest may never reference a partial or unverified artifact. If
even reserved failure-manifest installation fails, return
`FAILURE_MANIFEST_CUSTODY_UNAVAILABLE` and do not claim a reproducible run package.
Resume is outside this proposal.

## 9. Proposed constants

Every number in this table is an engineering proposal, not an observed scientific
threshold. Every row remains `PROPOSED / NOT APPROVED` until a specification owner
approves it and its maximum-shape/runtime proof.

| Constant | Proposed value | Authority status |
| --- | ---: | --- |
| `max_operand_bits` | `256` | **PROPOSED / NOT APPROVED** |
| `max_schedule_rows` | `1000` | **PROPOSED / NOT APPROVED** |
| `max_chunk_rows` | `256` | **PROPOSED / NOT APPROVED** |
| `max_run_package_bytes` | `536870912` | **PROPOSED / NOT APPROVED** |
| `max_input_sidecar_bytes` | `67108864` combined | **PROPOSED / NOT APPROVED** |
| `max_schedule_spool_bytes` | `16777216` | **PROPOSED / NOT APPROVED** |
| `max_primary_ledger_bytes` | `268435456` | **PROPOSED / NOT APPROVED** |
| `max_comparison_ledger_bytes` | `134217728` | **PROPOSED / NOT APPROVED** |
| `max_single_diagnostic_bytes` | `16777216` | **PROPOSED / NOT APPROVED** |
| `max_diagnostic_ledger_bytes` | `67108864` | **PROPOSED / NOT APPROVED** |
| `max_diagnostic_recomputations` | `256` | **PROPOSED / NOT APPROVED** |
| `max_diagnostic_work_units` | `30000000` | **PROPOSED / NOT APPROVED** |
| `max_total_reference_work_units` | `60000000` | **PROPOSED / NOT APPROVED** |
| `max_reference_owned_peak_upper_bytes` | `536870912` | **PROPOSED / NOT APPROVED** |
| `FAILURE_MANIFEST_RESERVE_BYTES` | `1048576` | **PROPOSED / NOT APPROVED** |
| `FIXED_SCHEDULE_SPOOL_ROW_JSON_BYTES` | `512` | **PROPOSED / NOT APPROVED** |
| `FIXED_COMPARISON_CELL_JSON_BYTES` | `1024` | **PROPOSED / NOT APPROVED** |
| `FIXED_COMPARISON_ROW_JSON_BYTES` | `2048` | **PROPOSED / NOT APPROVED** |
| `FIXED_DIAGNOSTIC_ROW_JSON_BYTES` | `2048` | **PROPOSED / NOT APPROVED** |
| `FIXED_ARTIFACT_INDEX_JSON_BYTES` | `16384` | **PROPOSED / NOT APPROVED** |
| `FIXED_ARTIFACT_INDEX_ENTRY_BYTES` | `256` | **PROPOSED / NOT APPROVED** |
| `FIXED_SUCCESS_MANIFEST_JSON_BYTES` | `16384` | **PROPOSED / NOT APPROVED** |
| `FIXED_FAILURE_MANIFEST_JSON_BYTES` | `16384` | **PROPOSED / NOT APPROVED** |
| `FIXED_FAILURE_ARTIFACT_ENTRY_BYTES` | `512` | **PROPOSED / NOT APPROVED** |
| `FIXED_PHASE_OVERHEAD_BYTES` | `8388608` | **PROPOSED / NOT APPROVED** |
| `STREAM_WRITE_BUFFER_BYTES` | `1048576` | **PROPOSED / NOT APPROVED** |
| `STREAM_READ_BUFFER_BYTES` | `1048576` | **PROPOSED / NOT APPROVED** |
| `CANONICAL_ENCODER_SCRATCH_BYTES` | `262144` | **PROPOSED / NOT APPROVED** |
| `CANONICAL_DECODER_SCRATCH_BYTES` | `262144` | **PROPOSED / NOT APPROVED** |
| `HASH_SCRATCH_BYTES` | `65536` | **PROPOSED / NOT APPROVED** |
| `REQUEST_OBJECT_PEAK_BYTES` | `8192` | **PROPOSED / NOT APPROVED** |
| `FIXED_STATE_OBJECT_PEAK_BYTES` | `1024` | **PROPOSED / NOT APPROVED** |
| `INTEGER_VALUE_PEAK_BYTES` | `64` | **PROPOSED / NOT APPROVED** |
| `INTEGER_CODE_PEAK_BYTES` | `64` | **PROPOSED / NOT APPROVED** |
| `CANDIDATE_RECORD_PEAK_BYTES` | `2048` | **PROPOSED / NOT APPROVED** |
| `SELECTION_RECORD_PEAK_BYTES` | `4096` | **PROPOSED / NOT APPROVED** |
| `SEQUENCE_VALUE_PEAK_BYTES` | `64` | **PROPOSED / NOT APPROVED** |
| `COUNTER_ENTRY_PEAK_BYTES` | `512` | **PROPOSED / NOT APPROVED** |
| `SORT_ENTRY_PEAK_BYTES` | `64` | **PROPOSED / NOT APPROVED** |
| `FIXED_DIAGNOSTIC_WORK_UNITS` | `4096` | **PROPOSED / NOT APPROVED** |

Revision 2's other work, record-count, edge, Counter, and byte caps also remain
`PROPOSED / NOT APPROVED`; this attachment does not silently approve or delete them.
`max_exact_state_count=100000` is inherited from the parent. The invariant
`retained_transformed_source_entries=0` is structural rather than a tunable number.

## 10. Fail-closed blockers

The following conditions prevent the named claim rather than inviting an estimated
substitute:

| Unbounded or unsupported quantity | Fail-closed result |
| --- | --- |
| Arbitrary iterable producer memory | Require an approved bounded adapter, or `TOTAL_PROCESS_RESOURCE_BOUND_UNAVAILABLE` |
| Production result/third-party temporary memory | Require a production-side envelope and subprocess hard limit, or no total-process/comparison-complete claim |
| Interpreter/allocator/OS process overhead | No static total-process upper; require enforced subprocess limit or retain the blocker |
| Uninstrumented built-in sort cost | No strict CPU-work upper; use an approved bounded sorter or `SORT_WORK_BOUND_UNAVAILABLE` |
| Free text, arbitrary paths, or unclosed record schema | `CANONICAL_BYTE_BOUND_UNAVAILABLE` before artifact production |
| Runtime object larger than its proposed constant | `RUNTIME_LAYOUT_UNSUPPORTED` before statistics |
| Diagnostic count/bytes/work exceeds a hard cap | diagnostics and comparison `PARTIAL`; outcome `INDETERMINATE` |
| Disk reservation, fsync, atomic rename, or failure-manifest custody unavailable | no reproducible package claim |
| Any actual primary/comparison byte count exceeds an admitted static bound | `REFERENCE_INTEGRITY_FAILURE`, never successful resource rejection |

The controlling state remains:

```text
PROPOSAL
NOT APPROVED
NOT FROZEN
NOT IMPLEMENTATION AUTHORITY
M6 NOT EXECUTED
```
