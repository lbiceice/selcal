# M6-P1 resource envelope v1.1 revision 5 formula attachment

> **Status:** `PROPOSAL / NOT APPROVED / NOT FROZEN / PROVISIONAL SCHEMA BINDING / NOT IMPLEMENTATION AUTHORITY / M6 NOT EXECUTED`

> **Scope:** This attachment repairs the rejected revision-4 resource and
> artifact contract. It defines a proposed branch model, recursive canonical-byte
> upper, guarded work and I/O accounts, bounded source-set identity, streamed
> diagnostics, and terminal-root-specific state triples. It does not authorize
> code or tests, report an execution, establish numerical agreement, complete M6,
> or establish SoftwareX readiness.

## 1. Authority, adverse evidence, and replacement boundary

Revision 5 is a new proposal. The following current-byte identities are retained
as provenance and adverse-review inputs; none is approval authority:

| Item | Bytes | SHA-256 |
| --- | ---: | --- |
| Parent independent-reference design, `2026-09-06-m6-p1-independent-reference-design.md` | `34234` | `ab6e40cc57eb5e4272451ebcb227eab45bf45f1ca66795530adb8d9957490064` |
| Revision 2 proposal, `2026-09-07-m6-p1-resource-envelope-v1_1-revision2-proposal.md` | `25755` | `4dd1c160bd89ce03530d173d580ffdbaf4f58953b1579496223804b2ebc5e609` |
| Revision 3 formula attachment, `2026-09-07-m6-p1-resource-envelope-v1_1-revision3-formulas.md` | `26990` | `db25f8a8c12e7d34a0241ae0b691ce7ef2bfb07fc4d4cfe7bb44c90c28e94cc6` |
| Revision 4 formula attachment, preserved unchanged | `62556` | `e856b12ae4f0acba7f4cf3f7e4164f852523760b5eafccbc4c4d42733a26b3f4` |
| Revision 4 schema proposal, adverse predecessor only | `141394` | `7ee984c561a13bffe08ff2d5161a208493b0cdc9065e5598059a63b9195efe46` |
| Revision 5 companion schema proposal, provisional cross-audit target | `283163` | `1c2bc7c6b8f14ac907627a7ae3e5728b1a76db2e766ee036df96f0c42d9388c6` |

The companion revision-5 schema is not yet an approved binding at the time this
file is written. Any later schema must be checked against the field/domain ledger
in sections 6 and 7. Until that check and an external approval record both exist,
the controlling state is `PROVISIONAL_SCHEMA_BINDING_HOLD`.

If and only if revision 5, its companion schema, and its budget profile are later
approved together under section 17, revision 5 replaces only these parent-design
parts:

1. retained-state and retained-transformed-source materialization;
2. resource admission, work, byte-I/O, memory, and source-identity accounting;
3. physical primary/comparison/diagnostic artifacts and failure custody;
4. finite terminal branch sequencing, including null bind and observed failure.

All scientific semantics not expressly named survive: state membership and
multiplicity, canonical candidate order, independent statistic and selection
logic, error precedence, inclusive tails, separate reference/production failure
ledgers, and the parent claim ceiling. Revision 5 changes no statistic, tolerance,
tail rule, or scientific threshold.

## 2. Production facts and branch order

This proposal is constrained by current production behavior, not by a desired
artifact layout:

1. `NULL_BIND` returns no observed results, no selection, no replicates, zero
   exceedance and failure counts, and null decision fields. It is a zero-statistic-
   scan terminal branch.
2. `OBSERVED_STATISTIC_SCAN` evaluates the observed candidate vector once and,
   when any candidate is an analytical failure, returns that full vector before
   selection, random-stream creation, token sampling/application, or replicates.
3. Only a finite production result that reaches the replicate phase can expose
   `actual.replicates`. A planned count `B` is not a replicate sequence, and
   production replicates are never an input to the reference schedule.

Therefore the finite comparison driver executes and projects the production public
call before deciding whether a schedule artifact exists. The exact component path
has no public complete-enumeration call and instead binds the production component
only after a zero-scan null-applicability check. The only legal order is:

```text
primitive admission and static worst-case admission
  -> FINITE: production public call (outside the reference-owned compute claim)
     -> inspect exact production terminal branch
        -> NULL_BIND_DISABLED:
          independent null-applicability check; zero statistic scans/states;
          no reference planned schedule
        -> FINITE_OBSERVED_ANALYTIC_FAILURE:
          independently scan observed once; no reference planned schedule;
          never replay B
        -> FINITE_NORMAL_OR_REPLICATE_FAILURE:
          after independent observed success, independently generate and validate
          a B-row reference plan; replay it independently and compare production
          state identities separately
  -> EXACT COMPONENT:
     -> independent and production null applicability checks
        -> NULL_BIND_DISABLED: zero scans/states, one adverse aggregate comparison
        -> APPLICABLE: independently enumerate and compare the admitted universe
```

The only finite schedule artifact is `reference-planned-schedule.jsonl`, whose
schema family is `ReferencePlannedSchedule*`. It is generated only after both the
production projection and the independent reference observed scan are successful.
Reference-owned logic uses solely frozen primitive inputs, the frozen null
specification, and the frozen random-stream specification. It is never a projection
of production/public output and never receives `actual.replicates`, production
states, production scores, or production selections as input. Production state
identities are merely comparison targets after both sides are fixed. The
observed-failure and null-bind branches both omit the plan. No document, manifest,
or formula may call the reference plan `actual.replicates` or infer from the plan
that production generated a replicate. The up-front package cap may reserve a
finite-normal worst case; reservation is not evidence that a schedule or replicate
was produced.

Two production concepts must not be conflated. The public API does not expose a
pre-execution planned state schedule, so the reference plan cannot be copied from
one. A completed normal production result does expose completed replicate outcomes,
including their state identities; those are comparison outputs only, observed after
the independent plan is frozen. In the production observed-failure branch no
replicate outcome exists at all. Any schema vocabulary saying simply “the public API
does not return states” is too broad and must be revised before binding.

## 3. Closed profile constants and vocabularies

### 3.1 Inherited constants

| Name | Value | Meaning |
| --- | ---: | --- |
| `max_exact_state_count` | `100000` | inherited exact-enumeration state cap |
| `retained_transformed_source_entries` | `0` | transformed sample arrays are never retained after a row |

### 3.2 Proposed resource constants

Every value below is `PROPOSED / NOT APPROVED`.

| Name | Value |
| --- | ---: |
| `max_operand_bits` | `256` |
| `max_schedule_rows` | `1000` |
| `max_transform_value_visits` | `2500000` |
| `max_candidate_support_visits` | `2500000` |
| `max_pearson_value_visits` | `15000000` |
| `max_nette_edge_work_units` | `2500000` |
| `max_nette_coding_value_visits` | `15000000` |
| `max_nette_directional_support_visits` | `5000000` |
| `max_nette_counter_update_visits` | `20000000` |
| `max_nette_sort_units` | `25000000` |
| `max_nette_cmi_arithmetic_units` | `30000000` |
| `max_selection_work_units` | `1000000` |
| `max_primary_compute_work_units` | `50000000` |
| `max_comparison_compute_work_units` | `10000000` |
| `max_diagnostic_compute_work_units` | `50000000` |
| `max_total_compute_work_units` | `90000000` |
| `max_io_byte_visits` | `4294967296` |
| `max_ledger_candidate_records` | `100000` |
| `max_live_candidate_records` | `5000` |
| `max_chunk_rows` | `256` |
| `max_chunk_count_per_stream` | `1000000` |
| `max_edge_entries` | `65536` |
| `max_counter_entries_upper` | `250000` |
| `max_diagnostic_recomputations` | `256` |
| `max_numerical_rows_per_diagnostic` | `8` |
| `max_input_sidecar_bytes` | `67108864` |
| `max_reference_planned_schedule_bytes` | `16777216` |
| `max_primary_ledger_bytes` | `268435456` |
| `max_comparison_ledger_bytes` | `134217728` |
| `max_diagnostic_ledger_bytes` | `67108864` |
| `max_run_package_bytes` | `536870912` |
| `max_reference_owned_peak_upper_bytes` | `536870912` |
| `FAILURE_MANIFEST_RESERVE_BYTES` | `16777216` |
| `max_disagreement_codes_per_record` | `32` |
| `max_ascii_runtime_string_bytes` | `256` |
| `max_ascii_reason_bytes` | `96` |
| `max_source_path_bytes` | `512` |
| `max_source_files_reference` | `256` |
| `max_source_files_production` | `256` |
| `max_source_files_comparison` | `256` |
| `max_source_file_bytes_reference` | `16777216` |
| `max_source_file_bytes_production` | `16777216` |
| `max_source_file_bytes_comparison` | `16777216` |
| `max_source_set_bytes_reference` | `67108864` |
| `max_source_set_bytes_production` | `67108864` |
| `max_source_set_bytes_comparison` | `67108864` |
| `max_declared_dependencies_reference` | `256` |
| `max_declared_dependencies_production` | `256` |
| `max_declared_dependencies_comparison` | `256` |
| `maxPendingDiagnosticJobs` | `0` |

The three four-tuples `(file count, one-file bytes, total-set bytes, declared
dependency count)` are deliberately independent admission accounts even where
their proposed numeric values coincide. `reference` bounds the clean-room reference
closure, `production` bounds the imported SelCal closure, and `comparison` bounds
the driver closure. Unused capacity in one role cannot be transferred to another.
Individual component maxima are also not jointly spendable beyond their parent and
total caps.

### 3.3 Proposed runtime-layout constants

These are conditional CPython-profile proposals, not total-process bounds:

```text
CONTAINER_BASE_PEAK_BYTES = 512
FLOAT_VALUE_PEAK_BYTES = 64
INTEGER_VALUE_PEAK_BYTES = 64
RECORD_BASE_PEAK_BYTES = 512
CANDIDATE_RECORD_PEAK_BYTES = 2048
SELECTION_RECORD_PEAK_BYTES = 4096
FIELD_COMPARISON_PEAK_BYTES = 1024
FAILURE_CODE_VALUE_PEAK_BYTES = 128
COUNTER_ENTRY_PEAK_BYTES = 512
SORT_ENTRY_PEAK_BYTES = 64
SOURCE_ENTRY_PEAK_BYTES = 1024
DEPENDENCY_POLICY_PEAK_BYTES = 1024
CHUNK_DESCRIPTOR_PEAK_BYTES = 1024
FAILURE_DESCRIPTOR_PEAK_BYTES = 1024
ENCODER_FRAME_PEAK_BYTES = 4096
MAX_CANONICAL_TOKEN_BYTES = 4096
STREAM_WRITE_BUFFER_BYTES = 1048576
STREAM_READ_BUFFER_BYTES = 1048576
HASH_SCRATCH_BYTES = 65536
DECODER_SCRATCH_BYTES = 262144
FIXED_PHASE_OVERHEAD_BYTES = 8388608
CMI_ARITHMETIC_UNITS_PER_OCCUPIED = 15
CMI_FINAL_UNITS_PER_DIRECTION = 3
NETTE_FINAL_UNITS_PER_CANDIDATE = 2
NULL_BIND_SCALAR_UNITS = 16
```

### 3.4 Closed identifiers and exact vocabularies

```text
profileId = "m6-p1-reference-envelope-v1.1-revision5-proposal"
canonicalizationVersion = "selcal-m6-p1-jsonl-v1"
calculationMode = ALL_STATE_EXACT | FINITE_B_SCHEDULE
executionBranch = ALL_STATE_EXACT_COMPONENT
                | FINITE_NORMAL
                | FINITE_REPLICATE_FAILURE
                | FINITE_OBSERVED_ANALYTIC_FAILURE
                | NULL_BIND_DISABLED
productionCountersStatus = AVAILABLE | NOT_EXPOSED
productionCountersNotExposedReason = null
                                   | PRODUCTION_API_NOT_EXPOSED
                                   | PRODUCTION_COUNTER_TRACE_NOT_AVAILABLE
                                   | PRODUCTION_COUNTER_SCHEMA_INCOMPATIBLE
counterKey.counterFamily = ABZ | AZ | BZ | Z
locatorIndexDomain = PRIMARY_ROW_INDEX | COMPARISON_ROW_INDEX
                   | DIAGNOSTIC_ROW_INDEX
mediaType = application/json | application/x-ndjson
          | application/octet-stream
verification = VERIFIED | UNVERIFIED
artifactStatus = PROPOSAL_UNAPPROVED | APPROVED_FROZEN
diagnosticPolicy = INTERLEAVED_WITH_COMPARISON_DISCOVERY
productionPreExecutionPlannedScheduleStatus = NOT_EXPOSED
productionPreExecutionPlannedScheduleReason =
    PUBLIC_API_DOES_NOT_EXPOSE_PREEXECUTION_PLANNED_SCHEDULE
terminalPartialDisposition = NOT_CREATED_BEFORE_FAILURE_ROOT
                           | DELETED_BEFORE_FAILURE_ROOT
                           | PRESERVED_VERIFIED_PARTIAL_EVIDENCE
                           | PRESERVED_UNVERIFIED_PARTIAL_EVIDENCE
```

`productionCountersNotExposedReason` must be null exactly when
`productionCountersStatus=AVAILABLE`; it must be one closed reason exactly when
the status is `NOT_EXPOSED`. Free exception text, hostnames, usernames, environment
values, and arbitrary labels are forbidden from canonical artifacts.
`diagnosticPolicy` is a constant and `maxPendingDiagnosticJobs=0`.

## 4. Guarded integer and finite-loop contract

Set `OPERAND_MAX = 2**max_operand_bits - 1` from the approved profile constant, not
from a request. Booleans are rejected. The following pseudocode is normative:

```python
def require_uint(x):
    if type(x) is not int or x < 0:
        fail("INVALID_INTEGER_OPERAND")
    if x > OPERAND_MAX:
        fail("OPERAND_BITS_LIMIT")
    return x

def gadd(a, b):
    a, b = require_uint(a), require_uint(b)
    if a > OPERAND_MAX - b:
        fail("OPERAND_BITS_LIMIT")
    return a + b

def gmul(a, b):
    a, b = require_uint(a), require_uint(b)
    if a != 0 and b > OPERAND_MAX // a:
        fail("OPERAND_BITS_LIMIT")
    return a * b

def ginc(a):
    return gadd(a, 1)

def gsub(a, b):
    a, b = require_uint(a), require_uint(b)
    if b > a:
        fail("INVALID_INTEGER_OPERAND")
    return a - b

def gpred0(a):
    a = require_uint(a)
    return 0 if a == 0 else gsub(a, 1)

def gceil(a, b):
    a, b = require_uint(a), require_uint(b)
    if b == 0:
        fail("INVALID_INTEGER_OPERAND")
    whole, remainder = divmod(a, b)
    return gadd(whole, int(remainder != 0))

def decimal_digits(x):
    x = require_uint(x)
    if x == 0:
        return 1
    digits = 0
    while x:
        x //= 10
        digits = ginc(digits)
    return digits

def ceil_log2_positive(x):
    x = require_uint(x)
    if x < 1:
        fail("INVALID_INTEGER_OPERAND")
    return gpred0(x).bit_length()

def mul_clamped(a, b, cap):
    a, b, cap = require_uint(a), require_uint(b), require_uint(cap)
    if cap == 0 or a == 0 or b == 0:
        return 0
    if a >= cap or b >= cap or a > cap // b:
        return cap
    return gmul(a, b)

def min_power_cap(base, exponent, cap):
    base, exponent, cap = map(require_uint, (base, exponent, cap))
    if cap == 0:
        return 0
    result, factor, remaining = 1, min(base, cap), exponent
    while remaining:
        if remaining & 1:
            result = mul_clamped(result, factor, cap)
        remaining //= 2
        if remaining:
            factor = mul_clamped(factor, factor, cap)
    return min(result, cap)
```

Exact state counting uses an iterative factorial/product recurrence that stops as
soon as the next multiplication would exceed `max_exact_state_count+1`; it never
constructs an unbounded factorial. `min_power_cap` is `O(log exponent)`. Every
request integer, derived integer, loop bound, index, `index+1`, byte counter,
array length, chunk count, numerator, and denominator passes `require_uint` before
use. Every executable sum/product/ceiling uses `gadd`, `gmul`, or `gceil`. The
ordinary symbols `+`, `-`, `*`, and `ceil` below mean those guarded operations;
`x-1` at a zero-admitting boundary means `gpred0(x)`.

## 5. Symbols, exact domains, paths, and branch counts

### 5.1 Symbols

| Symbol | Definition |
| --- | --- |
| `n` | common source/target length |
| `h` | largest canonical candidate |
| `N` | common support `n-h` |
| `C` | canonical candidate count |
| `T` | exact labelled-state count |
| `B` | finite plan's design count |
| `bins` | NetTE bin count, otherwise null |
| `q` | block count for a divisible block-null request, otherwise null |
| `W_state` | live state payload integers: `q` for block state, otherwise `1` |
| `Q_admit/Q_actual` | admitted/actually executed reference statistic scans |
| `X_admit/X_actual` | admitted/actual transformed rows |
| `L_admit/L_actual` | admitted/actual primary state rows |
| `R_admit/R_actual` | admitted/actual comparison records |
| `D_admit/D_started/D_completed` | admitted, actually started, and completely retained diagnostic recomputations; `D_actual=D_started` for resource accounting |
| `Z_admit/Z_actual` | admitted/actual diagnostic JSONL rows |
| `E/F` | finite exceedance/failure counts only after scheduled work exists |
| `U` | one-direction total occupied Counter-entry upper |
| `H` | `9*C+16`, field-comparison array upper |
| `J` | `max_diagnostic_recomputations`, diagnostic-index array upper |
| `G` | `max_disagreement_codes_per_record` |
| `M` | `max(n,h,N,C,T when known,B when known,bins when known,1)`; a reported scientific-operand maximum, not a substitute digit domain |
| `MinDiagnosticRowBytes` | mechanically measured minimum canonical bytes across every legal diagnostic row branch after schema binding; unavailable before section 6.8 passes |

### 5.2 Exact digit domains

Let `d(x)=decimal_digits(x)`. Each dynamic integer field is charged against its own
domain; there is no generic `d(M)` shortcut.

| Domain name | Inclusive maximum | Digit upper |
| --- | ---: | ---: |
| `NATURAL_OPERAND` | `OPERAND_MAX` | `d(OPERAND_MAX)` |
| `SAMPLE_COUNT` | `n` | `d(n)` |
| `SAMPLE_INDEX` | `gpred0(n)` | `d(gpred0(n))` |
| `CANDIDATE_VALUE` | `h` | `d(h)` |
| `CANDIDATE_COUNT` | `C` | `d(C)` |
| `CANDIDATE_INDEX` | `gpred0(C)` | `d(gpred0(C))` |
| `SUPPORT_COUNT` | `N` | `d(N)` |
| `SCAN_COUNT` | `max(T,ginc(B))` | `d(max(T,ginc(B)))` |
| `STATE_ROW_COUNT` | `max(T,B)` | `d(max(T,B))` |
| `COMPARISON_RECORD_COUNT` | `max(ginc(T),gadd(B,2))` | `d(max(ginc(T),gadd(B,2)))` |
| `EXACT_STATE_INDEX` | `gpred0(T)` | `d(gpred0(T))` |
| `FINITE_REPLICATE_INDEX` | `gpred0(B)` | `d(gpred0(B))` |
| `PRIMARY_ROW_INDEX` | `gpred0(L_admit)` | `d(gpred0(L_admit))` |
| `COMPARISON_ROW_INDEX` | `gpred0(R_admit)` | `d(gpred0(R_admit))` |
| `DIAGNOSTIC_COUNT` | `D_admit` | `d(D_admit)` |
| `DIAGNOSTIC_INDEX` | `gpred0(D_admit)` | `d(gpred0(D_admit))` |
| `DIAGNOSTIC_ROW_COUNT` | `Z_admit` | `d(Z_admit)` |
| `DIAGNOSTIC_ROW_INDEX` | `gpred0(Z_admit)` | `d(gpred0(Z_admit))` |
| `DIAGNOSTIC_BODY_INDEX` | `gpred0(Z_admit)` | `d(gpred0(Z_admit))` |
| `CHUNK_INDEX` | `gpred0(max_chunk_count_per_stream)` | `d(gpred0(max_chunk_count_per_stream))` |
| `CHUNK_ROW_COUNT` | `max_chunk_rows` | `d(max_chunk_rows)` |
| `LEDGER_BYTES` | applicable ledger byte cap | `d(applicable cap)` |
| `PACKAGE_BYTES` | `max_run_package_bytes` | `d(max_run_package_bytes)` |
| `ROW_BYTE_OFFSET` | applicable ledger byte cap | `d(applicable cap)` |
| `ROW_BYTE_LENGTH` | applicable recursively derived row upper | `d(applicable row upper)` |
| `SOURCE_FILE_COUNT` | role-specific `max_source_files` | role-specific digits |
| `SOURCE_FILE_INDEX` | `gpred0(role-specific max_source_files)` | role-specific digits |
| `SOURCE_FILE_BYTES` | role-specific single-file cap | role-specific digits |
| `SOURCE_SET_BYTES` | role-specific set cap | role-specific digits |
| `DECLARED_DEPENDENCY_COUNT` | role-specific `max_declared_dependencies` | corresponding digits |
| `EDGE_COUNT` | `max_edge_entries` | `d(max_edge_entries)` |
| `EDGE_INDEX` | `gpred0(max_edge_entries)` | `d(gpred0(max_edge_entries))` |
| `CODE_VALUE` | `gpred0(bins)` | `d(gpred0(bins))` |
| `COUNTER_KEY_COMPONENT` | `gpred0(bins)` | `d(gpred0(bins))` |
| `COUNTER_COUNT` | `N` | `d(N)` |
| `COUNTER_ENTRY_COUNT` | `U` | `d(U)` |
| `E_OR_F` | `B` | `d(B)` |
| `PLANNED_DENOMINATOR` | `B+1` | `d(ginc(B))` |

Negative integers are absent. Exact zero has one digit. Signed values are encoded
only as fixed-width `float.hex()` strings, never as decimal JSON numbers.

### 5.3 Literal path prefixes

All generated variable strings and paths are restricted to the JSON-safe ASCII
alphabet `[A-Za-z0-9._/+:-]`; it excludes quote, reverse solidus, controls, and
non-ASCII. Their JSON string size is therefore exactly `2+payloadBytes`.

```text
STATE_CHUNK_PREFIX       = "state-chunks/state-"
COMPARISON_CHUNK_PREFIX  = "comparison-chunks/comparison-"
DIAGNOSTIC_CHUNK_PREFIX  = "diagnostic-chunks/diagnostic-"
CHUNK_SUFFIX             = ".jsonl"
PARTIAL_SUFFIX           = ".partial"
ORIGINAL_INPUT_PATH      = "original-input.json"
REFERENCE_SPEC_PATH      = "reference-spec.json"
REFERENCE_PLANNED_SCHEDULE_PATH = "reference-planned-schedule.jsonl"
OBSERVED_RECORD_PATH     = "observed-record.json"
EXACT_MANIFEST_PATH      = "exact-manifest.json"
FINITE_MANIFEST_PATH     = "finite-b-manifest.json"
NULL_BIND_DISABLED_MANIFEST_PATH = "null-bind-disabled-manifest.json"
DIAGNOSTIC_MANIFEST_PATH = "diagnostic-manifest.json"
COMPARISON_MANIFEST_PATH = "comparison-manifest.json"
FAILURE_MANIFEST_PATH    = "failure-manifest.json"
RESERVE_PATH             = ".failure-manifest.reserve"
```

The measured ASCII literal byte lengths, frozen as part of the profile projection,
are:

```text
len(STATE_CHUNK_PREFIX)=19
len(COMPARISON_CHUNK_PREFIX)=29
len(DIAGNOSTIC_CHUNK_PREFIX)=29
len(CHUNK_SUFFIX)=6
len(PARTIAL_SUFFIX)=8
len(ORIGINAL_INPUT_PATH)=19
len(REFERENCE_SPEC_PATH)=19
len(REFERENCE_PLANNED_SCHEDULE_PATH)=32
len(OBSERVED_RECORD_PATH)=20
len(EXACT_MANIFEST_PATH)=19
len(FINITE_MANIFEST_PATH)=22
len(NULL_BIND_DISABLED_MANIFEST_PATH)=32
len(DIAGNOSTIC_MANIFEST_PATH)=24
len(COMPARISON_MANIFEST_PATH)=24
len(FAILURE_MANIFEST_PATH)=21
len(RESERVE_PATH)=25
```

Chunk paths use exactly six zero-padded digits because the allowed indices are
`0..999999`:

```text
path_state(i)      = STATE_CHUNK_PREFIX + zpad6(i) + CHUNK_SUFFIX
path_comparison(i) = COMPARISON_CHUNK_PREFIX + zpad6(i) + CHUNK_SUFFIX
path_diagnostic(i) = DIAGNOSTIC_CHUNK_PREFIX + zpad6(i) + CHUNK_SUFFIX
path_partial(p)    = p + PARTIAL_SUFFIX

len(path_state(i)) = 19+6+6 = 31
len(path_comparison(i)) = 29+6+6 = 41
len(path_diagnostic(i)) = 29+6+6 = 41
len(path_partial(p)) = len(p)+8
```

`zpad6` rejects out-of-domain indices. Caller-controlled paths, absolute paths,
`..`, NUL, symlinks, Unicode, and separator aliases are rejected before opening.

### 5.4 Branch counts and actual/admit formulae

The up-front finite admission is allowed to use the normal worst case, but actual
operands are selected only after the production terminal branch is known:

| Branch | `Q_admit/Q_actual` | `X_admit/X_actual` | `L_admit/L_actual` | `R_admit/R_actual` | reference planned schedule |
| --- | --- | --- | --- | --- | --- |
| `ALL_STATE_EXACT_COMPONENT` | `T/T` | `T/T` | `T/T` | `(T+1)/(T+1)` | absent |
| `FINITE_NORMAL` | `(B+1)/(B+1)` | `B/B` | `B/B` | `(B+2)/(B+2)` | independent reference plan, `B` rows |
| `FINITE_REPLICATE_FAILURE` | `(B+1)/(B+1)` | `B/B` | `B/B` | `(B+2)/(B+2)` | independent reference plan, `B` rows |
| `FINITE_OBSERVED_ANALYTIC_FAILURE` | `(B+1)/1` before branch; tightened to `1/1` after projection | `B/0` before branch; tightened to `0/0` | `B/0` before branch; tightened to `0/0` | `(B+2)/2` before branch; tightened to `2/2` | absent |
| exact `NULL_BIND_DISABLED` | `max_exact_state_count/0` before applicability; tightened to `0/0` | same | same | `ginc(max_exact_state_count)/1` before applicability; tightened to `1/1` | absent |
| finite `NULL_BIND_DISABLED` | `(B+1)/0` before branch; tightened to `0/0` | `B/0` before branch; tightened to `0/0` | `B/0` before branch; tightened to `0/0` | `(B+2)/1` before branch; tightened to `1/1` | absent |

The null-disabled comparison stream contains exactly one `AGGREGATE` terminal
record. The observed-failure stream contains `OBSERVED, AGGREGATE`. Normal finite
contains `OBSERVED, B ordered STATE, AGGREGATE`. Exact contains `T ordered STATE,
AGGREGATE`. Thus comparison chunking is always by `R`, never by `T` or `B` by
accident.

```text
K_primary(L)    = min(max(L,1),max_chunk_rows)
K_comparison(R) = min(max(R,1),max_chunk_rows)
K_diagnostic    = max_chunk_rows

primaryChunkCount(L) = 0 if L=0 else gceil(L,K_primary(L))
comparisonChunkCount(R) = gceil(R,K_comparison(R))
diagnosticChunkCount(Z) = 0 if Z=0 else gceil(Z,K_diagnostic)
```

Every result is checked against `max_chunk_count_per_stream` before a path is
generated.

Finite terminal projections use a nested denominator object, never parallel fields:

```json
{"plannedDenominator":{"source":"DESIGN_CONSTANT","value":"B+1"}}
```

The quotation marks around `B+1` above denote a formula placeholder only; the
artifact value is the integer `ginc(B)`. In the observed-failure branch,
`executedStatisticScans=1`, `executedScheduledScans=0`, and each of `E`, `F`,
`lowerNumerator`, `upperNumerator`, `denominator`, `lowerBoundHex`, `upperBoundHex`,
`pValueHex`, and `decision` is null. In the null-bind branch those same metrics are
null and both executed scan counts are zero. `plannedDenominator` records a design
constant only; it is not an executed denominator or evidence of replicate coverage.

## 6. Recursive canonical-byte upper over the schema

### 6.1 Canonical encoder and scalar byte functions

Canonicalization is UTF-8, `ensure_ascii=True`, `allow_nan=False`, sorted object
keys, separators `,` and `:`, minimal decimal nonnegative integers, binary64 values
as `float.hex()` strings, lowercase 64-hex SHA-256, no BOM/CRLF. JSON files have no
trailing LF; each JSONL row has exactly one LF.

The implementation must use an incremental token encoder. It may not create a
whole-row or whole-manifest `str`/`bytes` through `json.dumps`. The following byte
functions include all punctuation and escaping:

```text
B(null)  = 4
B(false) = 5
B(true)  = 4
B(constant) = exact length of its canonical JSON literal
B(uint[0..m]) = d(m)
B(hash256) = 66                       # quotes + 64 lowercase hex
B(floatHex) = 26                     # quotes + max 24-byte finite float.hex text
B(safeAscii[k]) = 2+k                # alphabet excludes JSON escapables
B(asciiAny[k]) = 2+6*k               # only where arbitrary ASCII is unavoidable
B(array(item,m)) = 2 if m=0 else 2 + m*B(item) + (m-1)
B(object branch) =
    2 + (coPresentFieldCount-1)
      + sum(B(exact key string) + 1 + B(field value))
B(oneOf branches) = max(B(each complete legal branch))
B($ref) = B(the resolved target)
```

For an object, `coPresentFieldCount` includes every optional property that can
legally coexist in the selected branch, because adding a member always increases
canonical length. `if/then/else`, `dependentSchemas`, `allOf`, `contains`,
`uniqueItems`, and mutually exclusive constraints are enumerated rather than
ignored. An array without a finite `maxItems`, a nonconstant string without a
finite byte-domain rule, an integer without a finite maximum or named semantic
domain, an open `additionalProperties`, an unresolved `$ref`, or recursion without
a decreasing bound is immediate `BYTE_BOUND_BINDING_HOLD`.

No unbounded runtime string is admitted. Runtime/compiler/platform values are
restricted to printable ASCII and capped by `max_ascii_runtime_string_bytes`;
because printable ASCII includes quote and reverse solidus, their upper uses
`asciiAny`. Closed reason codes use their longest fixed literal. If a later schema
admits a free string, non-ASCII, or another alphabet, the profile is invalid until
its escaping rule is explicitly bounded.

The companion schema currently admits printable ASCII in a few runtime/scalar
fields, so the conservative escaping-aware charges are normative even when a
producer normally emits a JSON-safe value:

| Scalar field/domain | Payload maximum | Canonical JSON upper |
| --- | ---: | ---: |
| SHA-256 | `64` lowercase hex | `66` |
| finite `float.hex()` | `24` safe ASCII | `26` |
| failure/disagreement code | `64` safe ASCII | `66` |
| `ScalarComparisonValue` string | `128` printable ASCII | `2+6*128=770` |
| `FieldComparison.fieldPath` | `160` safe ASCII | `162` |
| runtime Python implementation/version/NumPy | `64` printable ASCII each | `386` each |
| runtime platform | `256` printable ASCII | `1538` |
| source path | `512` JSON-safe ASCII | `514` |
| source-set ID | `64` lowercase hex | `66` |
| external binding ID / approver ID | `128` JSON-safe ASCII | `130` |
| approved UTC timestamp | `32` JSON-safe ASCII | `34` |

`386=2+6*64` and `1538=2+6*256`. This table charges the schema language, not only
today's friendly examples. A schema restriction to the safe alphabet could later
tighten the bound only through a new approved profile.

### 6.2 Complete integer/hash field-domain inventory

The companion v5 schema must generate this inventory mechanically. The names below
are normative; a missing field, extra required field, wider domain, or moved field
invalidates the provisional binding.

| Shape/branch | Required integer fields and domains | Required SHA-256 fields |
| --- | --- | --- |
| `OriginalInput` | none; length is the cardinality of each `sourceHex`/`targetHex` array | none inside the file |
| `ReferenceSpecExact` | candidate values, statistic `bins` when NetTE, and null parameters (`minShift` or block length/max blocks) | only hashes nested in the approved `contractBinding`; proposal binding hashes are null |
| `ReferenceSpecFinite` | exact fields above plus `plannedB:B` | same contract-binding rule |
| `ReferencePlannedScheduleRow` | `rowIndex:FINITE_REPLICATE_INDEX`; state payload indices | none |
| `ObservedRecordComplete/Failure` | `candidateCount:C`, candidate and support fields, `executedStatisticScans` | `originalInputSha256`, `referenceSpecSha256` |
| `ExactStateRowComplete/Failure` | `rowIndex,exactStateIndex,candidateCount`; state/candidate/support fields | `originalInputSha256`, `referenceSpecSha256` |
| `FiniteStateRowComplete/Failure` | `rowIndex,replicateIndex,candidateCount`; state/candidate/support fields | `originalInputSha256`, `referenceSpecSha256`, `referencePlannedScheduleSha256` |
| `CandidateRecordValid` | `candidateIndex:CANDIDATE_INDEX`, `candidate:CANDIDATE_VALUE`, `supportCount:SUPPORT_COUNT` | none |
| `CandidateRecordFailed` | same three | none |
| `Selection` | `selectedIndex:CANDIDATE_INDEX`, `selectedCandidate:CANDIDATE_VALUE`, every `tiedCandidateIndex:CANDIDATE_INDEX` | none |
| `ExactPrimaryManifest` | `totalStateCount:T`, `identityRowIndex`, failure/exceedance/numerator/denominator counts, primary ledger/chunk byte operands | hashes in original/spec descriptors, `primaryLedgerSha256`, and approved binding component hashes |
| `FinitePrimaryManifestNormal/ReplicateFailure` | `observedRecordCount=1`, `stateRecordCount:B`, `executedStatisticScans=B+1`, `executedScheduledScans=B`, `B,E,F`, byte/count operands | previous hashes plus `referencePlannedScheduleSha256` and `observedRecordSha256` |
| `FinitePrimaryManifestObservedFailure` | `observedRecordCount=1`, `stateRecordCount=0`, `executedStatisticScans=1`, `executedScheduledScans=0`, `unexecutedReplicateCount=B` | input/spec/observed hashes; no planned-schedule hash |
| `NullBindDisabledPrimaryManifestExact` | zero executed scan/state counts; planned B/denominator are null | hashes in original/spec descriptors and approved binding only |
| `NullBindDisabledPrimaryManifestFinite` | `plannedB:B`, nested planned denominator `B+1`, `unexecutedReplicateCount:B`, zero executed scans/states | hashes in original/spec descriptors and approved binding only |
| every success file descriptor (`OriginalInputDescriptor`, `ReferenceSpecDescriptor`, `ReferencePlannedScheduleDescriptor`, `ObservedRecordDescriptor`, `ExactManifestDescriptor`, `FiniteManifestDescriptor`, `NullBindDisabledManifestDescriptor`, `DiagnosticManifestDescriptor`) | `bytes:<descriptor-specific byte cap>` | `sha256` |
| `ChunkDescriptor` | exactly five dynamic integers: `chunkIndex:CHUNK_INDEX`, `firstIndex:<stream row domain>`, `lastIndex:<stream row domain>`, `rowCount:CHUNK_ROW_COUNT`, `bytes:<ledger cap>` | `sha256` |
| `RowLocator` | `chunkIndex`, `rowIndex:<declared locatorIndexDomain>`, `byteOffset:<ledger cap>`, `byteLength:<row upper>` | `chunkSha256`, `rowSha256` |
| `FileLocator` | `bytes:PACKAGE_BYTES` | `sha256` |
| `ComparisonObservedRecord` | `comparisonIndex:COMPARISON_ROW_INDEX`, candidate/field/diagnostic indices | `referenceRecordSha256`, `productionProjectionSha256` |
| `ComparisonStateRecord` | `comparisonIndex`, `rowIndex:PRIMARY_ROW_INDEX`, candidate/field/diagnostic indices | same two |
| `ComparisonAggregateRecord` | `comparisonIndex`; `B,E,F`, scan/count fields applicable to branch; field/diagnostic indices | same two |
| `DiagnosticHeader` | `diagnosticRowIndex:DIAGNOSTIC_ROW_INDEX`, `diagnosticIndex`, `comparisonIndex`, six expected row counts | `referenceRecordSha256`, `productionProjectionSha256` |
| `DiagnosticEdge` | diagnostic/global/body indices, `edgeIndex` | none |
| `DiagnosticCode` | diagnostic/global/body indices, `sampleIndex`, `codeIndex`, `code` | none |
| `DiagnosticCounter` | diagnostic/global/body indices, `count`, and key components admitted by `counterKey.counterFamily` | none |
| `DiagnosticNumerical` | diagnostic/global/body indices | none; numerical scalars are floatHex/null |
| `DiagnosticFooter` | diagnostic/global indices, actual body-kind counts | `headerSha256`, `bodyRowsSha256` |
| `DiagnosticManifest` | record/chunk/count/byte operands | `diagnosticLedgerSha256`, descriptor hashes, binding component hashes |
| `SourceSetEntry` | `ordinal:SOURCE_FILE_INDEX`, `bytes:SOURCE_FILE_BYTES` | `sha256` |
| `TransitiveDependencyPolicy` | `declaredDependencyCount:DECLARED_DEPENDENCY_COUNT`, `unresolvedDependencyCount=0` | `dependencyManifestSha256` for closed non-stdlib branch; null for stdlib-only |
| `SourceSetManifestObject` | `sourceCount:SOURCE_FILE_COUNT`, `totalSourceBytes:SOURCE_SET_BYTES` | `sourceSetId` is the 64-hex digest of the canonical source-set projection with `sourceSetId` omitted |
| `ComparisonManifest` | `comparisonRecordCount:R`, ledger/chunk/agreement/disagreement/notComparable counts, every `DerivedOperands` integer | primary/diagnostic/comparison ledger hashes, three source-set hashes, binding component hashes |
| `VerifiedRetainedArtifactDescriptor` | `bytes:PACKAGE_BYTES` | `sha256` |
| `UnverifiedRetainedArtifactDescriptor` | `bytes:PACKAGE_BYTES or null` | `sha256=null` |
| `FailureManifest` | stage/count/byte operands, writer/read observed counts, terminal-partial byte count if known | binding hashes and each VERIFIED retained artifact hash only |

`SAMPLE_COUNT` has maximum `n`. In a mode where `T`, `B`, or `bins` is null, a
multi-mode maximum above excludes that null operand and uses the applicable
admission cap before the branch-specific value is known. Exact/finite inapplicable
operands are null, not zero. Every hash listed is one quoted 64-hex digest. No
object contains its own digest. Every hash not listed is forbidden unless this
inventory and profile are versioned again.

### 6.3 Arrays and nested shapes

```text
candidateRecords = exactly C for OBSERVED and STATE; exactly 0 for AGGREGATE
tiedCandidateIndices <= C
fieldComparisons <= H = 9*C+16
diagnosticIndices <= J = max_diagnostic_recomputations
disagreementCodes <= G = max_disagreement_codes_per_record
implementationSourceSets = exactly 3, one per unique role
sourceEntries(role) <= max_source_files_role
declaredDependencyCount(role) <= max_declared_dependencies_role
diagnostic body scalar arrays = forbidden; one scalar per body row
```

The recursive `B(node)` formula is applied to each complete `oneOf` branch. This
is stronger than a fixed guessed base: all key names, commas, colons, brackets,
nulls, booleans, enums, hashes, integers, and string quotes are included by
construction.

### 6.4 Descriptor and locator expansions

Let `P(x)=2+ascii_bytes(x)` for safe generated paths and `H256=66`. Ordinary
success descriptors are schema-specific because their byte caps and fixed paths
differ:

```text
successFileDescriptorUpper(type) = B(the complete resolved descriptor type)
SuccessFileDescriptorMax = max(successFileDescriptorUpper(each of the eight
                               named descriptor types in section 6.2))

chunkDescriptorUpper(path,rowDomain,ledgerCap) =
  B({mediaType:"application/x-ndjson",path:path,
     locatorIndexDomain:<stream-specific fixed literal>,
     chunkIndex:[0..999999],firstIndex:rowDomain,lastIndex:rowDomain,
     rowCount:[0..max_chunk_rows],bytes:[0..ledgerCap],sha256:hash})
```

The second formula has exactly five dynamic integers; `bytes` is not hidden in a
fixed base. Locator domain is explicit:

```text
rowLocatorUpper(path,indexDomain,ledgerCap,rowUpper) =
  B({locatorIndexDomain:<literal>,path:path,chunkIndex:CHUNK_INDEX,
     rowIndex:indexDomain,byteOffset:[0..ledgerCap],
     byteLength:[0..rowUpper],chunkSha256:hash,rowSha256:hash})

fileLocatorUpper(path,byteCap) =
  B({path:path,bytes:[0..byteCap],sha256:hash})
```

A diagnostic locator must use `locatorIndexDomain="DIAGNOSTIC_ROW_INDEX"` and
charge `d(max(Z_admit-1,0))`. Reusing the primary or comparison digit domain is an
integrity failure.

Failure-only retained descriptors, which are distinct from ordinary success file
descriptors, have two complete schema branches:

```text
VERIFIED   => bytes is exact uint; sha256 is hash; fsyncStatus is closed enum
UNVERIFIED => bytes is writer-observed uint or null; sha256 is null;
              fsyncStatus is FAILED or NOT_ATTEMPTED
```

The latter never becomes VERIFIED from an in-memory writer hash alone.

### 6.5 Row-shape formulae

Define reusable recursive uppers from the exact proposed schema shapes:

```text
CandidateUpper = max(B(CandidateRecordValid),B(CandidateRecordFailed))
SelectionUpper = B(Selection with C tiedCandidateIndices)
StateUpper = max(B(CircularState),B(BlockState with q permutation indices))
FieldComparisonUpper = max(B(each legal FieldComparison oneOf branch))

OriginalInputUpper = B(OriginalInput with 2*n floatHex elements)
ReferenceSpecExactUpper = B(ReferenceSpecExact with all section-6.2 fields)
ReferenceSpecFiniteUpper = B(ReferenceSpecFinite with all section-6.2 fields)
ReferencePlannedScheduleRowUpper =
  B(ReferencePlannedScheduleRow with StateUpper) + 1 LF
ObservedRowUpper = max(B(ObservedRecordComplete),B(ObservedRecordFailure))
ExactStateRowUpper = max(B(ExactStateRowComplete),B(ExactStateRowFailure)) + 1 LF
FiniteStateRowUpper = max(B(FiniteStateRowComplete),B(FiniteStateRowFailure)) + 1 LF
```

For comparison records, `Proj*` means the recursive upper of the complete
production projection branch and `Loc*` the appropriate locator upper:

```text
ComparisonObservedUpper =
  B(ComparisonObservedRecord with C candidateRecords,
    H fieldComparisons,J diagnosticIndices,G disagreementCodes,
    ProjObserved,LocObserved) + 1 LF

ComparisonStateUpper =
  max(B(ComparisonExactStateRecord),B(ComparisonFiniteStateRecord))
  with C candidateRecords,H fieldComparisons,J diagnosticIndices,
  G disagreementCodes,ProjState,LocState + 1 LF

ComparisonExactAggregateUpper =
  B(ComparisonExactAggregateRecord with H fieldComparisons,
    J diagnosticIndices,G disagreementCodes,ProjExactAggregate,
    LocExactManifest) + 1 LF

ComparisonFiniteAggregateUpper =
  max(B(normal),B(replicateFailure),B(observedFailure),B(nullBind))
  with H fieldComparisons,J diagnosticIndices,G disagreementCodes,
  applicable complete ProjFiniteAggregate and LocFiniteManifest + 1 LF
```

Per-record-kind ledger formulae are mandatory:

```text
ComparisonRowsUpperExact =
  T*ComparisonStateUpper + ComparisonExactAggregateUpper

ComparisonRowsUpperFiniteNormal =
  ComparisonObservedUpper
  + B*ComparisonStateUpper
  + ComparisonFiniteAggregateUpper

ComparisonRowsUpperFiniteObservedFailure =
  ComparisonObservedUpper + ComparisonFiniteAggregateUpper

ComparisonRowsUpperNullBind = ComparisonFiniteAggregateUpper
```

There is no generic comparison-row multiplier. Runtime checks use the actual
branch formula; static pre-product admission uses the finite-normal maximum.

### 6.6 Diagnostic row and byte formulae

For NetTE:

```text
edgeEntries = 2*ginc(bins)
u3 = min_power_cap(bins,3,N)
u2 = min_power_cap(bins,2,N)
u1 = min(N,bins)
U  = u3 + 2*u2 + u1
```

`U` is the four Counter families in one direction. Reference diagnostics contain
both directions, hence `2*U`. Production contributes another `2*U` only when
`productionCountersStatus=AVAILABLE`; otherwise it contributes zero and supplies a
non-null `productionCountersNotExposedReason`.

```text
NetTEBodyRowsUpperAvailable =
  2*(bins+1)                # EDGE
  + 2*n                     # CODE
  + 2*U                     # reference FORWARD + REVERSE Counter rows
  + 2*U                     # production, only for admission upper
  + max_numerical_rows_per_diagnostic

NetTEGroupRowsUpper = 1 + NetTEBodyRowsUpperAvailable + 1
PearsonGroupRowsUpper = 1 + max_numerical_rows_per_diagnostic + 1
GroupRowsUpper = applicable maximum
D_admit = max_diagnostic_recomputations
DiagnosticRowsShapeUpper = D_admit*GroupRowsUpper
Z_admit = min(DiagnosticRowsShapeUpper,
              max_diagnostic_ledger_bytes // MinDiagnosticRowBytes)
```

`MinDiagnosticRowBytes` is not hand asserted. It is the minimum over mechanically
generated legal minimum instances in section 6.8. Until that report exists,
`Z_admit` and any formula depending on it are provisional and cannot admit a run.

The row byte upper is computed separately for header, edge, code, each of four
`counterKey.counterFamily` branches, numerical, and footer. In particular:

```text
CounterUpper = max(
  B(counterKey={counterFamily:"ABZ",a:max,b:max,z:max}),
  B(counterKey={counterFamily:"AZ",a:max,z:max}),
  B(counterKey={counterFamily:"BZ",b:max,z:max}),
  B(counterKey={counterFamily:"Z",z:max})
)

DiagnosticGroupBytesUpper =
  HeaderUpper
  + edgeRows*EdgeUpper
  + codeRows*CodeUpper
  + referenceCounterRows*CounterUpper
  + productionCounterRowsUpper*CounterUpper
  + numericalRowsUpper*NumericalUpper
  + FooterUpper

DiagnosticRowsBytesUpper = D_admit*DiagnosticGroupBytesUpper
```

Every diagnostic JSONL body row contains one edge, code, counter, or numerical
payload; no unbounded array is legal.

### 6.7 Manifest, source-set, ledger, and package uppers

Let descriptors be recursively calculated, not assigned guessed base sizes:

```text
SDesc = chunkDescriptorUpper(max state path,PRIMARY_ROW_INDEX,
                             max_primary_ledger_bytes)
CDesc = chunkDescriptorUpper(max comparison path,COMPARISON_ROW_INDEX,
                             max_comparison_ledger_bytes)
DDesc = chunkDescriptorUpper(max diagnostic path,DIAGNOSTIC_ROW_INDEX,
                             max_diagnostic_ledger_bytes)
```

Source-set object uppers are defined in section 7. Primary, diagnostic,
comparison, and failure manifest uppers are `B(complete legal branch)` with maximum
descriptor array cardinalities, the exact required hash/integer inventory in
section 6.2, and the branch-specific nested projection. In expanded cardinality
form:

```text
ExactPrimaryManifestUpper =
  B(fixed scalar members and hashes)
  expanded with primaryChunkCount(T) elements each <= SDesc

FinitePrimaryManifestUpper(branch) =
  B(fixed branch members and hashes)
  expanded with primaryChunkCount(L_admit(branch)) elements each <= SDesc

DiagnosticManifestUpper =
  B(fixed members and hashes)
  expanded with diagnosticChunkCount(Z_admit) elements each <= DDesc

ComparisonManifestUpper(branch) =
  B(fixed members, all DerivedOperands, runtime identity,
    exactly three bounded source-set identities and hashes)
  expanded with comparisonChunkCount(R_admit(branch)) elements each <= CDesc

FailureManifestUpper(branch) =
  B(fixed failure/custody/operand members and hashes)
  expanded with at most RetainedDescriptorCountUpper(branch)
  complete VERIFIED-or-UNVERIFIED descriptors
```

The maximum retained descriptor count excludes the reserve and the failure
manifest itself:

```text
hasReferencePlannedSchedule(branch) =
  1 for FINITE_NORMAL or FINITE_REPLICATE_FAILURE; otherwise 0
hasObserved(branch) =
  1 for FINITE_NORMAL, FINITE_REPLICATE_FAILURE, or
  FINITE_OBSERVED_ANALYTIC_FAILURE; otherwise 0

RetainedDescriptorCountUpper(branch) =
  2                                      # original + spec
  + hasReferencePlannedSchedule(branch)
  + hasObserved(branch)
  + primaryChunkCount(L_admit(branch))
  + 1                                    # primary manifest
  + comparisonChunkCount(R_admit(branch))
  + diagnosticArtifactCountUpper(result)
  + 1                                    # at most one serial writer .partial, if preserved
```

Here `diagnosticArtifactCountUpper(result)=diagnosticChunkCount(Z_admit)+1` only
for a result branch in which disagreement diagnostics are legal; it is `0` for
null bind, observed analytical failure, replicate analytical failure, exact-state
analytical failure, and agreement. Static pre-result admission may use the larger
legal disagreement branch, but a tightened branch upper may not retain impossible
diagnostic nodes.

Ledger byte uppers are sums of their exact record-kind uppers. Retained package
upper is the disjoint sum of actual branch nodes in section 8, including manifest
bytes exactly once. `runDirectoryTransientUpper` adds the failure reserve and at
most one current `.partial`; it is not the retained package upper.

### 6.8 Mechanical maximum/minimum canonical-instance plan

No byte formula is approved by prose inspection. After a companion v5 schema is
available, a standard-library-only verifier must:

1. enumerate every schema `oneOf` branch and every closed enum discriminator;
2. derive every integer maximum from the named domain registry above;
3. generate one canonical minimum and one canonical maximum legal instance for
   every object/row/manifest branch, including all four Counter keys, both
   production Counter statuses, VERIFIED/UNVERIFIED descriptors, every terminal
   manifest branch, and all three media types;
4. validate both instances against the exact companion schema;
5. encode incrementally and measure exact canonical bytes;
6. assert `measuredMax <= recursiveUpper` and
   `measuredMin >= MinDiagnosticRowBytes` where applicable;
7. mutate each bounded integer to its maximum and maximum+1, each array to its
   maximum and maximum+1, and each safe string to its maximum bytes and one byte
   beyond; maximum instances must pass and over-cap instances must fail;
8. independently parse the schema to list all required integer/hash/string/array
   fields and byte-compare that generated list with section 6.2's profile
   projection; no orphan or uncharged field is allowed;
9. write a read-only verification report containing formula/schema/profile input
   hashes, branch name, measured min/max, recursive upper, and mutation result.

This is a future verification plan, not an executed test. Missing report, a single
under-bound instance, a schema field not in the inventory, or a profile field not
in the schema is `BYTE_BOUND_BINDING_HOLD`.

## 7. Bounded canonical source-set identities

Three single-file identities are insufficient because imports are transitive.
`implementationSourceSets` therefore contains exactly three embedded canonical
source-set manifest objects, one each for `REFERENCE_SOURCE`, `PRODUCTION_SOURCE`,
and `COMPARISON_DRIVER`.

Each object contains:

```text
schemaVersion
sourceSetRole
sourceSetId                       # 64 lowercase hex
ordering=ORDINAL_CONTIGUOUS_PATH_ASCII_LEXICOGRAPHIC
entries[]                         # sorted by path
  {ordinal,path,mediaType,bytes,sha256}
sourceCount
totalSourceBytes
transitiveDependencyPolicy
  STANDARD_LIBRARY_ONLY:
    {mode,dependencyManifestSha256=null,
     declaredDependencyCount=0,unresolvedDependencyCount=0}
  CLOSED:
    {mode=LOCKFILE_CLOSED|DECLARED_EXTERNAL_SET,
     dependencyManifestSha256,declaredDependencyCount,
     unresolvedDependencyCount=0}
artifactStatus
```

`sourceSetId` is the lowercase SHA-256 of the canonical object projection with only
`sourceSetId` omitted. The semantic verifier enforces the digest even though the
schema's string pattern alone cannot. It is not self-hashing. For a closed external
dependency policy, `dependencyManifestSha256` must equal the SHA-256 of exactly one
included source entry that is the frozen lockfile/distribution manifest; a dangling
digest is invalid. The containing comparison manifest embeds the complete object.

The role-specific recursive upper is:

```text
SourceEntryUpper(role) =
  B({ordinal:[0..gpred0(max_source_files_role)],
     path:safeAscii[max_source_path_bytes],
     mediaType:<longest of exactly 3>,
     bytes:[1..max_source_file_bytes_role],sha256:hash})

DependencyPolicyUpper(role) = max(
  B(STANDARD_LIBRARY_ONLY branch),
  B(CLOSED branch with dependencyManifestSha256=hash and
    declaredDependencyCount=max_declared_dependencies_role)
)

SourceSetUpper(role) =
  B({schemaVersion:<fixed v5 literal>,sourceSetRole:<fixed role>,
     sourceSetId:safeAscii[64],
     ordering:"ORDINAL_CONTIGUOUS_PATH_ASCII_LEXICOGRAPHIC",
     entries:array(SourceEntryUpper(role),max_source_files_role),
     sourceCount:[1..max_source_files_role],
     totalSourceBytes:[1..max_source_set_bytes_role],
     transitiveDependencyPolicy:DependencyPolicyUpper(role),
     artifactStatus:<longest of the two status literals>})
```

Admission requires, separately per role:

```text
sourceCount <= max_source_files_role
each source file bytes <= max_source_file_bytes_role
totalSourceBytes == sum entry bytes <= max_source_set_bytes_role
declaredDependencyCount <= max_declared_dependencies_role
unresolvedDependencyCount == 0
ordinals == 0..sourceCount-1
```

Transitive closure policy:

1. begin at every root entrypoint actually imported/executed for the run;
2. statically resolve every owned local import recursively, including package
   initializers and data files whose bytes influence execution;
3. record every reachable owned file exactly once by normalized relative path;
4. include the exact lockfile, wheel RECORD, or installed-distribution manifest as
   a source entry and bind its digest/count in `transitiveDependencyPolicy`;
5. record the interpreter/runtime separately in `runtimeIdentity`;
6. reject unresolved relative imports, namespace ambiguity, generated-but-unbound
   modules, path injection, editable dependencies without a closed byte set, and
   any runtime/dynamic import not present in the closure;
7. after execution, instrumented import observations must be a subset of the frozen
   closure; an extra observed file is an integrity failure, not an auto-update.

Role constraints are not interchangeable: the clean-room `REFERENCE_SOURCE` must
use `STANDARD_LIBRARY_ONLY`; the NumPy-dependent `PRODUCTION_SOURCE` must use a
closed dependency branch; and `COMPARISON_DRIVER` must use a closed branch whenever
it imports either non-stdlib surface. Standard-library bytes are represented by the
exact interpreter/runtime identity, not silently counted as owned reference source.

Git commits, package versions, or three root-file hashes alone do not establish a
source identity. The three source sets remain logically independent even if a file
is byte-identical across roles.

## 8. The only legal artifact graph

Ordinary retained artifacts are exactly:

```text
original-input.json
reference-spec.json
  [FINITE_NORMAL or FINITE_REPLICATE_FAILURE only]
  reference-planned-schedule.jsonl
  [finite except NULL_BIND_DISABLED]
  observed-record.json
state-chunks/state-*.jsonl
exact-manifest.json OR finite-b-manifest.json
OR null-bind-disabled-manifest.json
comparison-chunks/comparison-*.jsonl
  [only when at least one diagnostic completed]
  diagnostic-chunks/diagnostic-*.jsonl -> diagnostic-manifest.json
comparison-manifest.json                     # sole success root
OR
failure-manifest.json                        # sole failure root
  [optional adverse leaf]
  one currently written ordinary-node path plus .partial
```

The source-set manifests are embedded objects in `comparison-manifest.json`; they
are not additional files. There is no artifact index, success manifest, or
predicted hash. A `.partial` is never a success artifact. Because writes are
strictly serial, at most one current partial can exist; on failure it may be
preserved as an adverse leaf under `failure-manifest.json` with a
VERIFIED/UNVERIFIED descriptor. `comparison-manifest.json.partial` additionally
uses section 11's mandatory four-way custody disposition. Success and failure roots
are mutually exclusive.

Branch graph specializations:

| Branch | reference planned schedule | observed | state chunks | primary manifest | `R_actual` |
| --- | --- | --- | --- | --- | ---: |
| exact | no | no separate file | `T` rows | exact | `T+1` |
| finite normal/replicate failure | yes, independently generated | yes | `B` rows | finite | `B+2` |
| finite observed failure | no | yes | none | finite observed-failure branch | `2` |
| null bind disabled, exact or finite | no | no | none | null-bind-disabled | `1` |

No empty chunk is fabricated. An analytical result may still reach a success root
with semantic status `NOT_COMPARABLE`; analytical unevaluability is not an I/O or
integrity failure.

## 9. Compute-work axis

Compute work counts declared semantic operations. It is not CPU time, process work,
or byte I/O. Production execution is reported separately and is not claimed bounded
by this reference-owned envelope.

For each branch, with `Q=Q_admit` for admission and `Q=Q_actual` for actuals:

```text
nullBindWorkUnits_admit  = NULL_BIND_SCALAR_UNITS
nullBindWorkUnits_actual = NULL_BIND_SCALAR_UNITS if the independent bind check
                          starts, otherwise 0

stateGenerationUnits_admit  = X_admit*W_state
stateGenerationUnits_actual = X_actual*W_state

transformValueVisits_admit  = X_admit*n
transformValueVisits_actual = X_actual*n

candidateSupportVisits_admit  = Q_admit*C*N
candidateSupportVisits_actual = Q_actual*C*N

pearsonValueVisits_admit  = 6*Q_admit*C*N
pearsonValueVisits_actual = 6*Q_actual*C*N

netteEdgeWorkUnits_admit  = 2*n + 2*bins
netteEdgeWorkUnits_actual = 0 if null bind else applicable observed edge bind work

netteCodingValueVisits_admit  = 6*Q_admit*C*N
netteCodingValueVisits_actual = 6*Q_actual*C*N

netteDirectionalSupportVisits_admit  = 6*Q_admit*C*N
netteDirectionalSupportVisits_actual = 6*Q_actual*C*N

netteCounterUpdateVisits_admit  = 8*Q_admit*C*N
netteCounterUpdateVisits_actual = 8*Q_actual*C*N

netteSortUnits_admit  = 2*Q_admit*C*U*ceil_log2_positive(max(U,1))
netteSortUnits_actual = sum over both directions, four Counter families, and all
                        scans of u_family*ceil_log2_positive(max(u_family,1))

netteCmiArithmeticUnits_admit =
  2*Q_admit*C*(U*CMI_ARITHMETIC_UNITS_PER_OCCUPIED
               + CMI_FINAL_UNITS_PER_DIRECTION)
  + Q_admit*C*NETTE_FINAL_UNITS_PER_CANDIDATE
netteCmiArithmeticUnits_actual =
  sum across both directions and all scans of
  occupiedTriples*CMI_ARITHMETIC_UNITS_PER_OCCUPIED
  + completedDirections*CMI_FINAL_UNITS_PER_DIRECTION
  + completedCandidatePairs*NETTE_FINAL_UNITS_PER_CANDIDATE

selectionWorkUnits_admit  = 3*Q_admit*C
selectionWorkUnits_actual = 3*successfulSelections*C
```

`CMI_ARITHMETIC_UNITS_PER_OCCUPIED=15` charges, per occupied joint cell, four
Counter lookups, four integer-to-binary64 conversions, two
numerator/denominator products, two divisions, one logarithm, one term
multiplication, and one `fsum` feed. Each completed direction additionally charges
one final `fsum`, one finite check, and one negative/clamp classification. A
completed forward/reverse candidate pair adds one subtraction and one final finite
check. Thus NetTE CMI arithmetic is neither hidden in Counter/sort work nor omitted
after the Counter tables are built.

Comparison work:

```text
comparisonCandidateUnits_admit  = (number of OBSERVED/STATE rows)*C
comparisonFieldUnits_admit      = R_admit*H
comparisonCodeUnits_admit       = R_admit*G
comparisonLocatorUnits_admit    = R_admit
comparisonComputeUpper          = sum above

comparisonCandidateUnits_actual = sum actual candidateRecords lengths
comparisonFieldUnits_actual     = sum actual fieldComparisons lengths
comparisonCodeUnits_actual      = sum actual disagreementCodes lengths
comparisonLocatorUnits_actual   = R_actual
comparisonComputeActual         = guarded sum above
```

Diagnostics are executed at discovery time under section 10:

```text
diagnosticComputeUpper = D_admit*(
  applicable statistic replay work
  + edgeEntries + 2*n + 4*U
  + max_numerical_rows_per_diagnostic
)

diagnosticComputeActual = guarded sum of every actually performed diagnostic
                          statistic/coding/Counter/sort/CMI/numerical operation,
                          including an incomplete final group on a failure root
```

When production counters are `NOT_EXPOSED`, actual diagnostic Counter work excludes
the production `2*U`; the admission upper retains it. Source-set traversal and
canonical encoding are separately recorded as `identityTraversalUnits` and
`canonicalTokenUnits`; they are included in `totalComputeWorkUnits` even though
they are not scientific statistic operations.

```text
identityTraversalUnits_admit =
  referenceSourceSetBytesUpper + productionSourceSetBytesUpper
  + comparisonSourceSetBytesUpper
  + referenceSourceCountUpper + productionSourceCountUpper
  + comparisonSourceCountUpper
  + declaredDependencyCountUpper across the three roles

identityTraversalUnits_actual = the same sum with verified actual values
canonicalTokenUnits_admit = max(successPackageUpper,failurePackageUpper)
canonicalTokenUnits_actual = total canonical bytes actually fed to encoders,
                             including a failed final partial
```

```text
primaryComputeWorkUnits = guarded sum of transform, support, statistic,
                          null-bind, state-generation, selection, identity,
                          and canonical-token components
totalComputeWorkUnits = primary + comparison + diagnostic
```

Every component cap, each parent cap, and `max_total_compute_work_units` must pass.
A resource rejection changes no scientific value and creates no fallback result.

## 10. Bounded diagnostic/comparison interleaving

There is no deferred unbounded diagnostic queue. For comparison index `r`:

1. hold at most one provisional comparison record in memory;
2. discover its comparison status and closed disagreement codes;
3. if no diagnostic is required, append the comparison record immediately;
4. if one or more closed diagnostic kinds are required, synchronously take the next
   kind without enqueuing it, check `D_started+1<=D_admit`, assert
   `maxPendingDiagnosticJobs=0`, and write one diagnostic group in the order
   `HEADER, zero or more scalar BODY rows, FOOTER`;
5. validate/hash that completed group, append its `diagnosticIndex` to the bounded
   provisional record, and repeat step 4 until no required kind remains; only then
   append the comparison record;
6. release the provisional record and advance to `r+1`.

If diagnostic production fails, the pending comparison record is not appended.
Previously completed comparison rows and diagnostic rows remain adverse evidence,
and the failure root records the stage. This gives a hard live queue bound of one
comparison record and one active diagnostic group writer, with exactly zero pending
diagnostic jobs; no reread/recompute queue exists. One comparison may reference at
most `J` completed groups, and all records together may start at most `D_admit`
groups.

Every diagnostic row has global `diagnosticRowIndex` in the
`DIAGNOSTIC_ROW_INDEX` domain. A group also has `diagnosticIndex`; body rows have a
consecutive `bodyIndex`. The header uses exactly:

```text
productionCountersStatus = AVAILABLE | NOT_EXPOSED
productionCountersNotExposedReason = null | one closed NOT_EXPOSED reason
```

Reference Counter rows always include both `FORWARD` and `REVERSE` directions and
all actually occupied families. Production Counter rows are emitted for both
directions only when status is `AVAILABLE`. A single exposed direction, missing
family entry, or `AVAILABLE` with a non-null reason is an integrity failure.
Each Counter row contains nested `counterKey`, whose first discriminator is
`counterKey.counterFamily` (`ABZ`, `AZ`, `BZ`, or `Z`).

The footer records exact body-kind counts, `headerSha256`, and `bodyRowsSha256`.
It does not hash itself. The diagnostic manifest binds chunk bytes after all
required groups have completed.

## 11. Byte-I/O axis and terminal partial custody

Byte-I/O counts bytes read from or written to file descriptors. It is not compute
work, CPU time, encoder work, or in-memory hashing. Writer hashing performed while
bytes are written does not add an I/O visit; a validation hash from a reread does.

For a completed ordinary JSON/JSONL file of `b` bytes:

```text
writeVisits = b
verificationReadAndHashVisits = b
ordinaryClosedFileIoVisits = 2*b
```

Additional semantic passes are charged explicitly:

```text
inputIo = inputWrite + inputVerifyRead
specIo = specWrite + specVerifyRead
plannedScheduleIo(normal finite only) =
  plannedScheduleWrite + plannedScheduleValidateHashRead
  + plannedScheduleReplayRead
primaryIo = primaryWrites + primaryVerifyHashReads
comparisonIo = comparisonWrites + comparisonVerifyHashReads
diagnosticIo = diagnosticWrites + diagnosticVerifyHashReads
manifestIo = each manifest write + its verify/hash reread
sourceIdentityIo = referenceSourceSetBytesActual
                 + productionSourceSetBytesActual
                 + comparisonSourceSetBytesActual
                   # exactly one read-and-hash pass over every source entry;
                   # a bound lock/RECORD entry is already one of those entries
```

The approved algorithm may not reread a source entry during admission. If a future
implementation adds any byte reread, that pass must be added to both the profile
upper and the observed I/O counter before it is legal.

The normal finite independent plan therefore costs
`3*referencePlannedScheduleBytesActual`, not two. Null bind and observed failure
have `referencePlannedScheduleBytesActual=null` and all planned-schedule I/O
operands zero.

`comparison-manifest.json` is first written as
`comparison-manifest.json.partial`. Success costs its partial write plus one full
verification/hash reread, followed by same-directory atomic rename; rename/fsync
metadata operations are recorded but have zero byte-visit charge.

If comparison-manifest installation fails:

1. a nonempty partial is preserved by default as the only optional adverse leaf;
2. if a complete reread succeeds, it receives a VERIFIED descriptor with exact
   bytes/hash; otherwise it receives UNVERIFIED, `sha256=null`, and bytes equal to
   the writer-observed count or null;
3. a partial may be deleted only when a read-only check proves its exact length is
   zero and it contains no evidence. The failure manifest then records
   `terminalPartialDisposition="DELETED_BEFORE_FAILURE_ROOT"` and no retained
   descriptor;
4. every nonzero partial uses
   `terminalPartialDisposition="PRESERVED_VERIFIED_PARTIAL_EVIDENCE"` or
   `"PRESERVED_UNVERIFIED_PARTIAL_EVIDENCE"` according to descriptor
   verification; deletion of nonzero bytes is forbidden;
5. the failure manifest records `partialBytesWritten`,
   `partialBytesReadForVerification`, and exactly one disposition from
   `NOT_CREATED_BEFORE_FAILURE_ROOT|DELETED_BEFORE_FAILURE_ROOT|
   PRESERVED_VERIFIED_PARTIAL_EVIDENCE|
   PRESERVED_UNVERIFIED_PARTIAL_EVIDENCE`. The actual I/O adds both observed
   counts; the admission upper charges `2*comparisonManifestUpper`.

The failure manifest itself is written through its own partial, fsynced, atomically
installed, and reread once; it never hashes itself. The reserve is a quota/space
reservation with no payload write. It is allocated before ordinary output, removed
only after one verified terminal root is installed, and is never an artifact or
retained package byte. A platform that can reserve only by writing bytes is outside
this profile until those reserve writes are added to the I/O upper.

```text
ioByteVisitsUpper = guarded sum of every branch-applicable write/read term,
                    including source-set reads, planned-schedule third pass,
                    comparison-manifest.partial failure reserve path,
                    and failure-root write/read worst case
```

Admission requires `ioByteVisitsUpper<=max_io_byte_visits`. Runtime counters are
monotone and fail before the next read/write would exceed the admitted amount.

## 12. Conditional reference-owned memory upper

Memory is derived from primitive live counts before bytes are encoded. It excludes
production internals, interpreter/module baseline, OS cache, allocator
fragmentation, and other-process memory and therefore may only be described as a
conditional reference-owned upper.

Simultaneously live containers are bounded phase by phase:

| Phase | Maximum simultaneous live objects |
| --- | --- |
| admission | primitive request scalars, guarded operands, no state table |
| source identity | one traversal frontier bounded by source-file count, one source entry, one dependency-policy object, three source-set containers only at final comparison manifest |
| production projection | one bounded projected result plus no reference state table |
| planned schedule | one independently generated reference state, encoder frames/buffers; no `B`-row list and no production result as generator input |
| primary statistic | original two source arrays, one transformed source array, support views, one candidate vector of `C`, one selection, one row encoder |
| NetTE | two edge arrays, bounded code vectors, one direction's four Counters and sort keys at a time; direction released before the next except the scalar directional result |
| comparison/diagnostic | one provisional comparison record, one reference row, one production projection, one diagnostic scalar body row, at most one direction's Counters, two open bounded stream buffers |
| manifest | bounded descriptor arrays, three bounded source-set objects, incremental encoder frames; no full JSON string/bytes |
| failure | existing descriptor metadata plus one failure descriptor and incremental failure-manifest encoder |

Primitive upper terms include:

```text
originalFloatCount = 2*n
transformedFloatCount = n
supportFloatViewCount = 6*C*N
candidateRecordCountLive <= max_live_candidate_records
statePayloadIntegerCount = W_state
counterEntryCountLive <= U
sortEntryCountLive <= U
sourceEntryCountLive <= max(max_source_files_reference,
                           max_source_files_production,
                           max_source_files_comparison)
dependencyPolicyCountLive = 1
descriptorCountLive <= RetainedDescriptorCountUpper(branch)
```

Each count is multiplied by its declared runtime-layout constant, then fixed
buffers/scratch/phase overhead are added with guarded arithmetic. The maximum across
phases, not the sum of mutually exclusive phases, is
`referenceOwnedPeakUpperBytes`. A runtime layout probe after approval must prove
each constant for the exact interpreter/runtime identity before any statistic runs.
Whole-object serialization is prohibited; incremental encoding is part of the
memory proof, not an implementation preference.

## 13. Legal cross-axis triples by terminal root and stage

Axes are not independently composable. A terminal record carries exactly one
triple `(primary,diagnostic,comparison)` selected from the table below. Each axis is
an object `{custodyStatus,semanticStatus}`. Unlisted triples are schema-invalid.

Abbreviations used only in this table:

```text
P0 = {NONE,NOT_STARTED}
PN = {COMPLETE,NULL_DISABLED}
PO = {COMPLETE,OBSERVED_ANALYTICAL_FAILURE}
PC = {COMPLETE,COMPLETE}
PR = {COMPLETE,REPLICATE_FAILURE}
PE = {COMPLETE,EXACT_ANALYTICAL_FAILURE}
D0 = {NONE,NOT_REQUIRED}
DC = {COMPLETE,COMPLETE}
C0 = {NONE,NOT_STARTED}
CA = {COMPLETE,COMPLETE_AGREEMENT}
CD = {COMPLETE,COMPLETE_DISAGREEMENT}
CN = {COMPLETE,NOT_COMPARABLE}

For failure class K in the closed set
K = RESOURCE_LIMIT | INTEGRITY_FAILURE | INTERRUPTED:
PK(custody) = {custody,K}
DK(custody) = {custody,K}
CK(custody) = {custody,K}
```

| Terminal root | Failure class/stage | Branch/result condition | Legal triple(s) |
| --- | --- | --- | --- |
| `comparison-manifest.json` | none | null bind disabled adverse terminal | `(PN,D0,CN)` |
| success root | none | observed analytical failure adverse terminal | `(PO,D0,CN)` |
| success root | none | finite replicate failure adverse terminal | `(PR,D0,CN)` |
| success root | none | exact state analytical failure adverse terminal | `(PE,D0,CN)` |
| success root | none | exact/finite complete agreement | `(PC,D0,CA)` |
| success root | none | exact/finite complete disagreement | `(PC,DC,CD)` |
| `failure-manifest.json` | `K/PRIMARY`, including preflight, input/spec, source binding, planned schedule, primary row/manifest | no completed primary root | `(PK(NONE|PARTIAL),D0,C0)` |
| failure root | `K/DIAGNOSTIC` | normal complete primary; diagnostic failed before pending comparison row finalization | `(PC,DK(NONE|PARTIAL),{PARTIAL,NOT_COMPARABLE})` |
| failure root | `K/COMPARISON` | completed primary; comparison row/chunk failure | `(P,D,{NONE|PARTIAL,K})`, where `P` is exactly the branch's one of `PC|PN|PO|PR|PE`, and `D=DC` only if a prior complete diagnostic exists, otherwise `D0` |
| failure root | `K/SUCCESS_ROOT_INSTALL` | comparison partial was created | `(P,D,CK(PARTIAL))` with the same branch-specific `P/D` restriction; partial disposition cannot be `NOT_CREATED_BEFORE_FAILURE_ROOT` |

`custodyStatus` vocabulary is exactly `NONE|PARTIAL|COMPLETE`.
`semanticStatus` vocabulary is axis-specific and includes exactly
`NOT_COMPARABLE`, never `INDETERMINATE`. A complete comparison manifest cannot
contain a PARTIAL axis. A failure root cannot claim agreement/disagreement. The
schema implements the table as terminal-root/failure-stage discriminated branches
rather than three independent enums. `NULL_BIND_DISABLED` is the execution branch;
its primary semantic status is the distinct literal `NULL_DISABLED`. The other
adverse success-root primary semantic statuses are exactly
`OBSERVED_ANALYTICAL_FAILURE`, `REPLICATE_FAILURE`, and
`EXACT_ANALYTICAL_FAILURE`; none may collapse to a generic analytical status.

## 14. Complete companion-schema `DerivedOperands` projection

The exact companion-schema projection is closed below. This is the persisted
projection, not a second formula language: every field maps to a formula already
defined in sections 5--13. Admission and executed values are separate wherever
both can differ; an inapplicable value is null, never a fabricated zero. The source
sets, runtime identity, memory proof, terminal axes, and `plannedDenominator` live
in their own schema objects and are not duplicated here.

```text
DerivedOperands = {
  n,h,N,C,T,B,bins,blockCount,WState,U,
  QAdmit,QExecuted,XAdmit,XExecuted,LAdmit,LExecuted,
  RAdmit,RExecuted,DExecuted,ZAdmit,ZExecuted,H,J,G,M,
  package,comparison,diagnostic,compute,io
}

PackageOperands = {
  artifactCountUpper,
  inputSidecarFormulaUpper,inputSidecarBytesObserved,
  referencePlannedScheduleFormulaUpper,
  referencePlannedScheduleAdmissionBytes,
  referencePlannedScheduleBytesVerified,
  primaryRowsBytesUpper,primaryManifestBytesUpper,
  comparisonRowsBytesUpper,diagnosticRowsBytesUpper,
  diagnosticManifestBytesUpper,terminalRootBytesUpper,
  successPackageUpper,failurePackageUpper,finalRetainedPackageUpper,
  finalRetainedPackageBytesObserved,failureManifestReserveBytes,
  runDirectoryTransientUpper
}

ComparisonOperands = {
  RAdmit,RExecuted,
  exactRecordCountExpected,finiteRecordCountExpected,
  nullBindRecordCountExpected,
  candidateRecordsMax,tiedCandidateIndicesMax,fieldComparisonsMax,
  diagnosticIndicesMax,disagreementCodesMax,
  comparisonChunkCount,comparisonLedgerBytesUpper,
  comparisonLedgerBytesObserved
}

DiagnosticOperands = {
  executionMode,maxPendingDiagnosticJobs,U,edgeEntries,
  DAdmit,DExecuted,ZAdmit,ZExecuted,
  diagnosticChunkCount,diagnosticRowsOneUpper,
  diagnosticRecordCountObserved,diagnosticLedgerBytesUpper,
  diagnosticLedgerBytesObserved,
  productionCountersStatus,productionCountersNotExposedReason
}

ComputeOperands = {
  transformValueVisits,candidateSupportVisits,pearsonValueVisits,
  netteEdgeWorkUnits,netteCodingValueVisits,
  netteDirectionalSupportVisits,netteCounterUpdateVisits,
  netteSortUnits,netteCmiArithmeticUnits,selectionWorkUnits,
  primaryComputeWorkUnits,comparisonComputeWorkUnits,
  diagnosticComputeWorkUnits,totalComputeWorkUnits
}

IoOperands = {
  inputSidecarByteVisits,referencePlannedScheduleByteVisits,
  primaryByteVisits,comparisonByteVisits,diagnosticByteVisits,
  terminalRootByteVisits,totalIoByteVisits,
  fsyncCallsObserved,atomicRenamesObserved,directoryFsyncCallsObserved
}
```

Name mapping is exact: schema `blockCount` is formula `q`; every schema
`*Executed` value is the corresponding formula `*_actual`; and schema
`netteSortUnits` is the applicable admitted or executed NetTE sort formula for the
record being emitted. `M` is the maximum field-specific dynamic integer domain
required by the recursive encoder; it is diagnostic metadata only and never
replaces the field-specific digit domains in section 5.2.

`candidateRecordsMax=C`, `tiedCandidateIndicesMax=C`,
`fieldComparisonsMax=9*C+16`,
`diagnosticIndicesMax=max_diagnostic_recomputations`,
`disagreementCodesMax=max_disagreement_codes_per_record`, and the source-set array
has exactly three role-distinct members outside `DerivedOperands`.

For `FINITE_OBSERVED_ANALYTIC_FAILURE`, the manifest's nested
`plannedDenominator` remains present with `source=DESIGN_CONSTANT` and
`value=B+1`; reference-planned-schedule fields are null/zero as required by their
schema branch, and all scheduled scientific metrics are null. For
`NULL_BIND_DISABLED`, observed and planned-schedule artifacts/scans are absent.
`productionCountersStatus` and `productionCountersNotExposedReason` are null only
when no diagnostic header exists; once a diagnostic exists they obey the paired
truth rule in section 3.4.

## 15. Package admission and fail-closed sequencing

Before any artifact write:

1. validate primitive types, finite floats, exact enums, and guarded integers;
2. freeze and validate all three transitive source sets and runtime identity;
3. determine null applicability without executing a statistic; if exact applicability
   survives, determine `T` with the cap-stopped recurrence; before that decision,
   exact admission uses `max_exact_state_count` rather than an unknown `T`;
4. compute static worst-case branch operands, recursive byte uppers, chunk counts,
   compute work, I/O visits, and conditional memory;
5. reject if any component, role-specific, aggregate, or package cap fails;
6. reserve failure-manifest space and verify same-directory atomic rename/fsync
   support;
7. incrementally write and reread input/spec sidecars;
8. for finite mode only, execute the production call, project its terminal branch,
   and tighten but never widen actual branch operands; the exact component skips
   this step and uses the separate component-binding path from section 2;
9. null bind: perform independent null-applicability comparison with zero statistic
   scans and no planned schedule/observed file;
10. observed failure: independently scan observed only, retain full failure vector,
    create no planned schedule, and compare two records;
11. finite normal/replicate failure: after independent observed success, generate
    the reference plan from frozen primitive inputs only, reread/validate exact IDs
    and states, replay independently, then compare production states as outputs;
12. exact component: enumerate without materializing a full table and stream rows;
13. interleave each diagnostic at comparison discovery as section 10 specifies;
14. close/reread/verify all required manifests and chunks;
15. install exactly one terminal root, then remove the transient reserve.

At every step, a resource/integrity failure preserves completed adverse evidence
and installs a failure root if the reserve permits. No failure may truncate an
accepted schedule, discard repeated/identity states, widen tolerance, turn null
indicators into false, change a statistic, or fall back to Monte Carlo.

## 16. Artifact and I/O branch equations

Let `bytes(x)` be the verified actual bytes of retained artifact `x`, and
`upper(x)` its section-6 recursive upper.

```text
RunPackageUpper(exact) =
  upper(original)+upper(spec)+upper(exact state chunks)
  +upper(exact primary manifest)+upper(comparison chunks)
  +optional upper(diagnostic chunks+manifest only for disagreement)
  +upper(comparison manifest)

RunPackageUpper(finite normal/replicate failure) =
  upper(original)+upper(spec)+upper(reference planned schedule)+upper(observed)
  +upper(finite state chunks)+upper(finite primary manifest)
  +upper(comparison chunks)
  +optional upper(diagnostic chunks+manifest only for disagreement)
  +upper(comparison manifest)

RunPackageUpper(observed failure) =
  upper(original)+upper(spec)+upper(observed)+upper(finite primary manifest)
  +upper(two comparison records/chunks)
  +upper(comparison manifest)

RunPackageUpper(null bind) =
  upper(original)+upper(spec)+upper(null-bind-disabled primary manifest)
  +upper(one aggregate comparison record/chunk)
  +upper(comparison manifest)
```

Failure package replaces `comparison-manifest.json` with
`failure-manifest.json` and may add the single preserved comparison-manifest
partial; no success root coexists.

`RunPackageBytesActual` is the sum of verified retained file sizes only. An
UNVERIFIED partial with unknown bytes prevents an exact package actual and records
that field as null while the bounded writer count remains in transient/I/O
operands. Package, compute, I/O, and memory axes never substitute for one another.

## 17. Deterministic external approval and profile projection

No contract object hashes itself. The external binding uses four independent
objects:

1. `formulaSha256`: raw revision-5 formula bytes;
2. `schemaSha256`: raw approved companion v5 schema bytes;
3. `budgetProfileSha256`: canonical bytes of the deterministic profile projection;
4. external approval record: binds the three digests and contains disposition,
   approver identity, UTC time, and a stable binding identifier.

The profile projection is the exact closed companion-schema object below; canonical
sorting, rather than presentation order, determines its byte identity:

```text
BudgetProfileProjection = {
  schemaVersion="selcal.m6-p1.budget-profile-projection.v5",
  profileId="m6-p1-reference-envelope-v1.1-revision5-proposal",
  canonicalizationVersion="selcal-m6-p1-jsonl-v1",
  diagnosticExecutionMode="INTERLEAVED_WITH_COMPARISON_DISCOVERY",
  constants=BudgetProfileConstants,
  artifactStatus=PROPOSAL_UNAPPROVED | APPROVED_FROZEN
}
```

`BudgetProfileConstants` contains every inherited/proposed numeric profile constant
listed in sections 3.1--3.2, using the companion schema's camelCase field names;
runtime-layout constants remain formula-bound rather than silently entering this
projection. Approval identity/time, formula and schema digests, measured results,
and the projection's own digest are excluded. Consequently regeneration from the
same formula/schema decisions is deterministic and non-cyclic.

Every schema-bound artifact carries `artifactStatus`. Proposal fixtures and the
future mechanical min/max report must use `PROPOSAL_UNAPPROVED`. An executable run
is legal only when `artifactStatus=APPROVED_FROZEN` and the resolved
`ExternalApprovedContractProjection` has
`disposition="APPROVED_FOR_M6_P1_IMPLEMENTATION"` with exact formula bytes/hash,
schema bytes/hash, profile projection/hash, path, binding ID, approver, and UTC-time
equality. Either value without the other is a
cross-contract integrity failure. No in-artifact status can approve itself.

Current post-document status is exactly:

```text
formulaStatus = REVISION5_PROPOSAL_WRITTEN
schemaStatus = PROVISIONAL_NOT_BOUND
budgetProfileStatus = PROPOSED_NOT_APPROVED
externalApprovalStatus = ABSENT
implementationStatus = NOT_AUTHORIZED
executionStatus = NOT_EXECUTED
```

After an explicit owner approval and only after max/min canonical-instance
verification succeeds, the external record may use
`disposition="APPROVED_FOR_M6_P1_IMPLEMENTATION"`. This document itself can never
set that disposition.

## 18. Revision-4 adverse-review closure matrix

“Disposition” below means proposed repair coverage, not reviewer acceptance.

| Finding | Revision-5 disposition |
| --- | --- |
| `C1` zero-scan null branch and pre-replicate observed failure | sections 2, 5.4, 8, and 15 add `NULL_BIND_DISABLED`, omit a plan on both early exits, prohibit any `actual.replicates` input claim, and generate `reference-planned-schedule.jsonl` independently only after observed success |
| `C2` byte uppers were not actual schema uppers | section 6 defines recursive punctuation/escaping-aware algebra, exact digit domains, all required integer/hash fields, five-int chunk descriptors, a complete operand ledger, and mechanical max/min instances |
| `C3` independent axis tables allowed illegal combinations | section 13 enumerates root-, class-, stage-, and branch-specific legal triples; every unlisted triple is invalid |
| `C4` three single-file identities omitted transitive code | section 7 replaces them with three independently capped canonical transitive source-set objects and external dependency identities |
| `C5` diagnostic queue/I/O partial custody was open | sections 10 and 11 interleave one diagnostic at discovery, bound live queue to one, and account for preserved/deleted comparison-manifest partials |
| `I1` vocabulary drift | sections 3.4, 6.2, 10, and 14 use `productionCountersStatus`, `AVAILABLE|NOT_EXPOSED`, nullable reason, nested `counterKey.counterFamily`, and nested `plannedDenominator` |
| `I2` media types incomplete | section 3.4 closes exactly three media types; octet-stream is limited to unclassified failure bytes |
| `I3` NetTE CMI arithmetic absent | section 9 adds occupied-cell arithmetic plus final directional/check work |
| `I4` `gceil` and actual/admit ambiguity | sections 4, 5.4, 9, and 14 define guarded ceiling and distinct upper/actual operands for every axis |
| `I5` diagnostic index/path domain vague | sections 5.2, 6.4, and 10 fix `DIAGNOSTIC_ROW_INDEX` and exact digits |
| `M1` approval/profile projection ambiguous | section 17 fixes a deterministic, non-self-hashing external approval projection and explicit current/postapproval states |

## 19. Self-audit and claim ceiling

Self-audit checklist for this proposal:

- every formula symbol is defined in sections 3–7 or locally next to its use;
- `gceil`, each `_admit`/`Upper`, and each `_actual`/`Actual` value are distinct;
- every integer field maps to an exact digit domain; zero has one digit;
- every required hash is either charged as 66 bytes or explicitly null/inapplicable;
- every JSON key, delimiter, quote, enum, and escape is charged recursively;
- chunk descriptors charge five dynamic integers including `bytes`;
- max/min instance generation is a mandatory future schema-binding gate, not a
  claimed execution;
- null bind performs zero statistic scans; observed failure performs one reference
  observed scan and zero scheduled scans; neither has a planned schedule;
- only normal/replicate-failure finite branches create an independent reference
  planned schedule, never a projection of `actual.replicates`;
- every retained ordinary file appears in section 8; the source-set objects are
  embedded; reserve is transient; only the comparison-manifest partial may survive
  as an adverse failure leaf;
- every diagnostic is completed before its referring comparison row, leaving no
  unbounded queue;
- both reference Counter directions are mandatory; production directions are both
  present only when `AVAILABLE`;
- compute, byte-I/O, retained package, and conditional memory remain separate;
- terminal state is chosen by the closed section-13 triple table, not independent
  axis composition;
- formula/schema/profile digests are bound externally without a self-hash cycle;
- revision 4 is preserved and no code or tests are authorized or modified here.

Even after later approval, implementation, and passing tests, this envelope could
establish only bounded fail-closed custody and reproducible comparison execution
for admitted M6-P1 cases. It cannot establish statistical validity, Type-I-error
control, power, external validity, user benefit, scientific novelty, M6 completion,
release approval, upload readiness, submission, acceptance, or SoftwareX readiness.

The controlling state remains:

```text
RESOURCE_ENVELOPE_REVISION5_PROPOSAL
PROVISIONAL SCHEMA BINDING HOLD
NOT APPROVED
NOT FROZEN
NOT IMPLEMENTED
M6 NOT EXECUTED
```
