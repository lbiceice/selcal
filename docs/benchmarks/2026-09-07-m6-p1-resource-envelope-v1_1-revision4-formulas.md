# M6-P1 resource envelope v1.1 revision 4 formula attachment

> **Status:** `PROPOSAL / NOT APPROVED / NOT FROZEN / NOT IMPLEMENTATION AUTHORITY / M6 NOT EXECUTED`

> **Scope:** This attachment specifies a proposed resource-accounting model,
> artifact graph, bounded-integer discipline, streamed diagnostic layout, and
> failure-custody contract. It does not authorize implementation or tests, alter a
> scientific threshold, establish numerical agreement, complete M6, or establish
> SoftwareX readiness.

## 1. Authority, adverse predecessors, and supersession boundary

This revision is a new proposal. It preserves the following rejected or incomplete
preimages without modifying them:

| Item | Current-byte identity used by this proposal |
| --- | --- |
| Parent independent-reference design | `docs/benchmarks/2026-09-06-m6-p1-independent-reference-design.md`; 34,234 bytes; SHA-256 `ab6e40cc57eb5e4272451ebcb227eab45bf45f1ca66795530adb8d9957490064` |
| Revision 2 proposal | `docs/benchmarks/2026-09-07-m6-p1-resource-envelope-v1_1-revision2-proposal.md`; 25,755 bytes; SHA-256 `4dd1c160bd89ce03530d173d580ffdbaf4f58953b1579496223804b2ebc5e609` |
| Revision 3 formula attachment | `docs/benchmarks/2026-09-07-m6-p1-resource-envelope-v1_1-revision3-formulas.md`; 26,990 bytes; SHA-256 `db25f8a8c12e7d34a0241ae0b691ce7ef2bfb07fc4d4cfe7bb44c90c28e94cc6` |
| Revision 3 schema proposal | `docs/benchmarks/schemas/m6-p1-artifact-contract-v3-proposal.schema.json`; 67,817 bytes; SHA-256 `b0ae1742bb672979400b12e3ef5489ee26d660dcf391ff4d9052b7f491251acd` |

The identities above are provenance labels, not approvals. If any bytes differ at
review time, this proposal must be rebound before approval.

If and only if a specification owner later approves revision 4 and records the
external binding described in section 14, revision 4 replaces only these parts of
the parent design:

1. retained-state and retained-transformed-source materialization;
2. resource preflight, work, byte-I/O, and memory accounting;
3. the physical result/diagnostic/comparison artifact graph and its failure custody;
4. the finite observed-failure execution schedule.

All parent scientific and algorithmic semantics not explicitly named above survive,
including state membership and multiplicity, candidate ordering, independent
statistics and selection, failure precedence, inclusive tails, E/F definitions for
an actually executed finite schedule, and the claim ceiling. Until approval, this
file replaces nothing.

## 2. Closed constant registry

There are no implicit imports from revision 2 or revision 3. Every constant used in
an executable formula in this attachment appears below.

### 2.1 Inherited, not newly approved here

| Name | Value | Status and meaning |
| --- | ---: | --- |
| `max_exact_state_count` | `100000` | inherited necessary parent cap; not sufficient by itself |
| `retained_transformed_source_entries` | `0` | inherited structural invariant; transformed values are never retained in a completed row |

No other numeric resource constant is inherited. In particular, a proposed value
repeated from an earlier rejected proposal remains proposed here.

### 2.2 Proposed request, work, and artifact caps

| Name | Proposed value | Status |
| --- | ---: | --- |
| `max_operand_bits` | `256` | `PROPOSED / NOT APPROVED` |
| `max_schedule_rows` | `1000` | `PROPOSED / NOT APPROVED` |
| `max_transform_value_visits` | `2500000` | `PROPOSED / NOT APPROVED` |
| `max_candidate_support_visits` | `2500000` | `PROPOSED / NOT APPROVED` |
| `max_pearson_value_visits` | `15000000` | `PROPOSED / NOT APPROVED` |
| `max_nette_edge_work_units` | `2500000` | `PROPOSED / NOT APPROVED` |
| `max_nette_directional_support_visits` | `5000000` | `PROPOSED / NOT APPROVED` |
| `max_nette_counter_update_visits` | `20000000` | `PROPOSED / NOT APPROVED` |
| `max_nette_sort_units` | `25000000` | `PROPOSED / NOT APPROVED` |
| `max_selection_work_units` | `1000000` | `PROPOSED / NOT APPROVED` |
| `max_primary_compute_work_units` | `30000000` | `PROPOSED / NOT APPROVED` |
| `max_comparison_compute_work_units` | `10000000` | `PROPOSED / NOT APPROVED` |
| `max_diagnostic_compute_work_units` | `30000000` | `PROPOSED / NOT APPROVED` |
| `max_total_compute_work_units` | `60000000` | `PROPOSED / NOT APPROVED`; individual maxima are not jointly spendable beyond this cap |
| `max_io_byte_visits` | `4294967296` | `PROPOSED / NOT APPROVED` |
| `max_ledger_candidate_records` | `100000` | `PROPOSED / NOT APPROVED` |
| `max_live_candidate_records` | `5000` | `PROPOSED / NOT APPROVED` |
| `max_chunk_rows` | `256` | `PROPOSED / NOT APPROVED` |
| `max_chunk_count_per_stream` | `1000000` | `PROPOSED / NOT APPROVED`; permits indices `000000` through `999999` only |
| `max_edge_entries` | `65536` | `PROPOSED / NOT APPROVED` |
| `max_counter_entries_upper` | `250000` | `PROPOSED / NOT APPROVED`; one reference direction at a time |
| `max_diagnostic_recomputations` | `256` | `PROPOSED / NOT APPROVED` |
| `max_numerical_rows_per_diagnostic` | `8` | `PROPOSED / NOT APPROVED` |
| `max_input_sidecar_bytes` | `67108864` | `PROPOSED / NOT APPROVED` |
| `max_schedule_spool_bytes` | `16777216` | `PROPOSED / NOT APPROVED` |
| `max_primary_ledger_bytes` | `268435456` | `PROPOSED / NOT APPROVED`; primary data rows only |
| `max_comparison_ledger_bytes` | `134217728` | `PROPOSED / NOT APPROVED`; comparison rows only |
| `max_diagnostic_ledger_bytes` | `67108864` | `PROPOSED / NOT APPROVED`; streamed diagnostic rows only |
| `max_run_package_bytes` | `536870912` | `PROPOSED / NOT APPROVED`; final retained bytes |
| `max_reference_owned_peak_upper_bytes` | `536870912` | `PROPOSED / NOT APPROVED`; conditional reference-owned memory only |
| `FAILURE_MANIFEST_RESERVE_BYTES` | `16777216` | `PROPOSED / NOT APPROVED`; transient filesystem reservation, never a retained artifact |
| `max_implementation_path_bytes` | `512` | `PROPOSED / NOT APPROVED`; printable ASCII only |
| `max_disagreement_codes_per_record` | `32` | `PROPOSED / NOT APPROVED`; values must come from a closed enum |

### 2.3 Proposed canonical byte-shape constants

The constants below exclude the explicitly added dynamic path, array, integer-digit,
hash, and scalar terms in section 7. Maximum-shape tests are required after approval;
these values are not validated measurements yet.

```text
FLOAT_HEX_JSON_BYTES = 32
FAILURE_CODE_JSON_BYTES = 66
HASH_JSON_BYTES = 66
NULL_JSON_BYTES = 4
SCALAR_COMPARISON_JSON_BYTES = 130

FIXED_ORIGINAL_INPUT_JSON_BYTES = 512
FIXED_REFERENCE_SPEC_JSON_BYTES = 2048
FIXED_SCHEDULE_SPOOL_ROW_JSON_BYTES = 512
FIXED_STATE_JSON_BYTES = 128
FIXED_CANDIDATE_JSON_BYTES = 512
FIXED_SELECTION_JSON_BYTES = 512
FIXED_STATE_ROW_JSON_BYTES = 1024
FIXED_OBSERVED_ROW_JSON_BYTES = 1024

FIXED_ARTIFACT_DESCRIPTOR_JSON_BYTES = 512
FIXED_FAILURE_DESCRIPTOR_JSON_BYTES = 768
FIXED_CHUNK_DESCRIPTOR_JSON_BYTES = 768
FIXED_ROW_LOCATOR_JSON_BYTES = 768
FIXED_FILE_LOCATOR_JSON_BYTES = 512
FIXED_PRIMARY_MANIFEST_JSON_BYTES = 32768
FIXED_COMPARISON_FIELD_JSON_BYTES = 1024
FIXED_PRODUCTION_PROJECTION_JSON_BYTES = 2048
FIXED_COMPARISON_ROW_JSON_BYTES = 2048
FIXED_DIAGNOSTIC_HEADER_JSON_BYTES = 2048
FIXED_DIAGNOSTIC_EDGE_JSON_BYTES = 512
FIXED_DIAGNOSTIC_CODE_JSON_BYTES = 512
FIXED_DIAGNOSTIC_COUNTER_JSON_BYTES = 768
FIXED_DIAGNOSTIC_NUMERICAL_JSON_BYTES = 1024
FIXED_DIAGNOSTIC_FOOTER_JSON_BYTES = 2048
MIN_DIAGNOSTIC_ROW_BYTES = 128
FIXED_DIAGNOSTIC_MANIFEST_JSON_BYTES = 16384
FIXED_COMPARISON_MANIFEST_JSON_BYTES = 32768
FIXED_FAILURE_MANIFEST_JSON_BYTES = 32768
FIXED_IMPLEMENTATION_IDENTITY_JSON_BYTES = 256
FIXED_RUNTIME_IDENTITY_JSON_BYTES = 1024
FIXED_APPROVED_BINDING_JSON_BYTES = 512
```

Every JSONL-row formula adds exactly one LF byte. JSON-file formulas do not.

### 2.4 Proposed runtime-layout constants

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
CHUNK_DESCRIPTOR_PEAK_BYTES = 1024
FAILURE_DESCRIPTOR_PEAK_BYTES = 1024
ENCODER_FRAME_PEAK_BYTES = 4096
MAX_CANONICAL_TOKEN_BYTES = 1024
STREAM_WRITE_BUFFER_BYTES = 1048576
STREAM_READ_BUFFER_BYTES = 1048576
HASH_SCRATCH_BYTES = 65536
DECODER_SCRATCH_BYTES = 262144
FIXED_PHASE_OVERHEAD_BYTES = 8388608
```

These constants are CPython/runtime-profile proposals. A successful layout probe is
required before statistics. It does not make this a total-process bound.

### 2.5 Fixed identifiers and closed vocabularies

The profile identifier is
`m6-p1-reference-envelope-v1.1-revision4-proposal`; canonicalization is
`selcal-m6-p1-jsonl-v1`. Proposed v4 schema discriminators use the prefix
`selcal.m6-p1`, the artifact role, and suffix `.v4-proposal`. The only modes are
`ALL_STATE_EXACT` and `FINITE_B_SCHEDULE`. Media types are exactly
`application/json` and `application/x-ndjson`. Failure codes, disagreement codes,
diagnostic numerical kinds, and unavailable-production reasons must each be a closed
ASCII enum in the companion schema; no arbitrary error or exception text is legal.

Every fixed path is listed in section 5. Every axis vocabulary is listed in section
13. These identifiers and vocabularies are part of the proposed budget-profile
projection used by section 14; none is imported implicitly from an earlier revision.

## 3. Symbols, modes, branches, and row counts

All request and derived counts are nonnegative exact built-in integers; booleans are
rejected. Every arithmetic operation uses section 4. Let:

| Symbol | Meaning |
| --- | --- |
| `n` | common source/target length |
| `h` | maximum canonical candidate |
| `N` | common support `n-h` |
| `C` | number of canonical candidates |
| `T` | exact labelled-state count |
| `B` | planned finite schedule row count |
| `bins` | NetTE bin count; absent for Pearson |
| `q` | block count `n/block_length` for applicable block null |
| `W_state` | maximum live state-payload integer count: `q` for block null, otherwise `1` |
| `U` | one-direction NetTE Counter-entry upper, defined in section 7.4 |
| `Q_admit` | static admitted statistic-scan upper |
| `Q_exec` | actual executed statistic scans |
| `X_admit` | static transformed-row upper |
| `X_exec` | actual transformed rows |
| `L_admit` | static state-row upper |
| `L_exec` | actual retained state rows |
| `R_admit` | static comparison-record upper |
| `R_exec` | actual comparison records |
| `D_exec` | actual diagnostic recomputations |
| `Z_admit` | admitted upper on streamed diagnostic rows under the byte cap |
| `Z_exec` | actual streamed diagnostic rows |
| `H` | per-comparison-record field-comparison upper |
| `J` | per-comparison-record diagnostic-index upper |
| `G` | per-comparison-record disagreement-code upper |
| `M` | `max(n,h,N,C,T when known,B when known,bins when known,1)` |

The exact row accounting is:

| Branch | `Q_admit` | `Q_exec` | `X_admit`/`X_exec` | `L_admit`/`L_exec` | `R_admit` | `R_exec` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ALL_STATE_EXACT`, any analytic outcome | `T` | `T` | `T` / `T` | `T` / `T` | `T+1` | `T+1` |
| `FINITE_B_SCHEDULE`, observed valid | `B+1` | `B+1` | `B` / `B` | `B` / `B` | `B+2` | `B+2` |
| `FINITE_B_SCHEDULE`, observed analytical failure | `B+1` | `1` | `B` / `0` | `B` / `0` | `B+2` | `2` |

Thus the required `R` rule is exact `T+1`, ordinary finite `B+2`, and observed-failure
actual `2` while the preflight upper remains `B+2`. The two observed-failure
comparison records are `OBSERVED` then `AGGREGATE`; no scheduled-state comparison
record exists.

For every applicable comparison record:

```text
candidateRecords count = C for OBSERVED and STATE; 0 for AGGREGATE
H = 9*C + 16
fieldComparisons count <= H
J = max_diagnostic_recomputations
diagnosticIndices count <= J
G = max_disagreement_codes_per_record
disagreementCodes count <= G
```

`implementationIdentities` occurs only in the terminal comparison manifest and has
exactly three members with exactly one each of `REFERENCE_SOURCE`,
`PRODUCTION_SOURCE`, and `COMPARISON_DRIVER`.

Chunking always follows the number of rows in its own stream:

```text
K_primary = min(max(L,1), max_chunk_rows)
K_comparison = min(max(R,1), max_chunk_rows)
K_diagnostic = max_chunk_rows

primary_chunk_count(L) = 0 if L=0 else ceil_div(L,K_primary)
comparison_chunk_count(R) = ceil_div(R,K_comparison)
diagnostic_chunk_count(Z) = 0 if Z=0 else ceil_div(Z,K_diagnostic)
```

Every count must be no greater than `max_chunk_count_per_stream` before a six-digit
chunk path is generated.

## 4. Guarded integer contract

### 4.1 Entry and operator guards

Set `OPERAND_MAX = 2**max_operand_bits - 1` during fixed profile construction. No
request-derived value is used to construct that constant. The executable contract is:

```python
def require_uint(x):
    if type(x) is not int or x < 0:
        fail("INVALID_INTEGER_OPERAND")
    if x > OPERAND_MAX:
        fail("OPERAND_BITS_LIMIT")
    return x

def gadd(a, b):
    a = require_uint(a)
    b = require_uint(b)
    if a > OPERAND_MAX - b:
        fail("OPERAND_BITS_LIMIT")
    return a + b

def gmul(a, b):
    a = require_uint(a)
    b = require_uint(b)
    if a != 0 and b > OPERAND_MAX // a:
        fail("OPERAND_BITS_LIMIT")
    return a * b

def gceil(a, b):
    a = require_uint(a)
    b = require_uint(b)
    if b == 0:
        fail("INVALID_INTEGER_OPERAND")
    whole, remainder = divmod(a, b)
    return gadd(whole, int(remainder != 0))

def ginc(a):
    return gadd(a, 1)
```

Every input, loop bound, array length, chunk count, index, index-plus-one,
denominator-plus-one, and recurrence operand passes `require_uint` before use.
Executable formulas use `gadd`, `gmul`, `gceil`, and `ginc`; mathematical `+` and
`*` below are notation for those guarded operations. No `(a+b-1)//b` is permitted.

### 4.2 Digits and logarithms

```python
def decimal_digits(x):
    x = require_uint(x)
    if x == 0:
        return 1
    count = 0
    while x != 0:
        x //= 10
        count = ginc(count)
    return count

def ceil_log2_positive(x):
    x = require_uint(x)
    if x < 1:
        fail("INVALID_INTEGER_OPERAND")
    return (x - 1).bit_length()
```

String conversion and floating logarithms are forbidden in byte/work ceilings.

### 4.3 Bounded power in `O(log exponent)`

```python
def mul_clamped(a, b, cap):
    a = require_uint(a)
    b = require_uint(b)
    cap = require_uint(cap)
    if cap == 0 or a == 0 or b == 0:
        return 0
    if a >= cap or b >= cap or a > cap // b:
        return cap
    return gmul(a, b)

def min_power_cap(base, exponent, cap):
    base = require_uint(base)
    exponent = require_uint(exponent)
    cap = require_uint(cap)
    if cap == 0:
        return 0
    result = 1
    factor = min(base, cap)
    remaining = exponent
    while remaining != 0:
        if remaining & 1:
            result = mul_clamped(result, factor, cap)
        remaining //= 2
        if remaining != 0:
            factor = mul_clamped(factor, factor, cap)
    return min(result, cap)
```

This never loops `exponent` times and never constructs an over-cap power.

### 4.4 Cap-stopped factorial

Block-state counting is state-cap bounded, not `q`-iteration bounded:

```python
q = require_uint(q)
state_cap = require_uint(max_exact_state_count)
state_count = 1
factor = 2
while factor <= q:
    if state_count > state_cap // factor:
        fail(
            "EXACT_STATE_COUNT_LIMIT",
            observed=None,
            observedAtLeast=ginc(state_cap),
        )
    state_count = gmul(state_count, factor)
    if factor == q:
        break
    factor = ginc(factor)
```

Because `state_count` must remain at most 100,000, a huge `q` stops after a small
number of iterations; it is never traversed to completion. Every later `range`
creation occurs only after its length has passed its own cap.

## 5. Canonical encoding and generated paths

Canonicalization is `selcal-m6-p1-jsonl-v1`: UTF-8; `ensure_ascii=True`;
`allow_nan=False`; lexicographically sorted object keys; separators `,` and `:`;
minimal decimal integers; binary64 values as `float.hex()` strings; lowercase
64-hex SHA-256; no BOM or CRLF. A JSON file has no trailing LF. Every JSONL row has
exactly one terminating LF, including the final row.

The implementation must use an incremental canonical encoder. It may never call a
whole-object `json.dumps`/`.encode` for a row, manifest, or sidecar. Array elements
and object members are emitted token by token into a bounded write buffer while the
file digest and byte count update. No encoded full-row `str` or `bytes` object may
exist. The largest live encoded token is checked against
`MAX_CANONICAL_TOKEN_BYTES`; a violation is `CANONICAL_TOKEN_LIMIT`.

Allowed retained paths are printable ASCII and are generated internally:

```text
original-input.json
reference-spec.json
schedule-spool.jsonl
observed-record.json
state-chunks/state-{chunkIndex:06d}.jsonl
exact-manifest.json
finite-b-manifest.json
comparison-chunks/comparison-{chunkIndex:06d}.jsonl
diagnostic-chunks/diagnostic-{chunkIndex:06d}.jsonl
diagnostic-manifest.json
comparison-manifest.json
failure-manifest.json
```

The only temporary names are the corresponding name plus `.partial` and the fixed
`.failure-manifest.reserve`. The reserve is not an artifact. No caller path,
absolute path, `..`, separator alias, Unicode, NUL, or symlink target is admitted.

For stream kind `s` with ASCII prefix `prefix_s`, suffix `.jsonl`, and a checked
`chunkIndex < max_chunk_count_per_stream`:

```text
chunk_index_path_digits = 6
chunk_path_bytes(s) = ascii_bytes(prefix_s) + 6 + ascii_bytes(".jsonl")
partial_chunk_path_bytes(s) = chunk_path_bytes(s) + ascii_bytes(".partial")
```

For an implementation identity only, the normalized printable-ASCII relative path
has `pathBytes <= max_implementation_path_bytes`; its byte upper is that cap. Thus
path character counts and UTF-8 byte counts cannot diverge.

## 6. Descriptor formulae and verification states

Let `d(x)=decimal_digits(x)` and let `P_art` be the maximum allowed retained artifact
path bytes from section 5. More exactly:

```text
ascii_bytes(s) = number of bytes in s after proving every character is ASCII

P_art = max(
    ascii_bytes(each fixed retained path),
    chunk_path_bytes("state"),
    chunk_path_bytes("comparison"),
    chunk_path_bytes("diagnostic"),
)

P_failure = max(P_art, P_art + ascii_bytes(".partial"))
```

All additions are guarded; `ascii_bytes` rejects rather than escapes non-ASCII.

Success descriptors are always verified:

```text
artifact_descriptor_upper(P_art) =
    FIXED_ARTIFACT_DESCRIPTOR_JSON_BYTES
    + P_art
    + d(max_run_package_bytes)
    + HASH_JSON_BYTES
```

A chunk descriptor additionally carries `chunkIndex`, `firstIndex`, `lastIndex`,
`rowCount`, and its fixed index-domain token:

```text
chunk_descriptor_upper(P_art, row_limit) =
    FIXED_CHUNK_DESCRIPTOR_JSON_BYTES
    + P_art
    + 4*d(max(max_chunk_count_per_stream,row_limit,max_run_package_bytes,1))
    + HASH_JSON_BYTES
```

Failure-manifest retained descriptors have exactly two legal branches:

```text
VERIFIED:
  verification="VERIFIED", bytes=nonnegative built-in int, sha256=lowercase 64hex

UNVERIFIED:
  verification="UNVERIFIED", bytes=nonnegative built-in int or null, sha256=null
```

An unverified `bytes` integer is only the writer-observed count and is never called
an exact byte count. The bound is:

```text
failure_descriptor_upper(P_art) =
    FIXED_FAILURE_DESCRIPTOR_JSON_BYTES
    + P_art
    + max(d(OPERAND_MAX), NULL_JSON_BYTES)
    + max(HASH_JSON_BYTES, NULL_JSON_BYTES)
```

The failure manifest may preserve either branch. The success-path primary,
diagnostic, and comparison manifests may reference only verified ordinary artifact
descriptors. Incremental writer digests do not upgrade `UNVERIFIED` after a failed
re-read.

Reference locators are distinct from artifact/chunk descriptors:

```text
file_locator_upper(P_art) =
    FIXED_FILE_LOCATOR_JSON_BYTES
    + P_art
    + d(max_run_package_bytes)
    + HASH_JSON_BYTES

row_locator_upper(P_art,row_limit) =
    FIXED_ROW_LOCATOR_JSON_BYTES
    + P_art
    + 5*d(max(max_chunk_count_per_stream,row_limit,max_run_package_bytes,1))
    + HASH_JSON_BYTES
```

## 7. Closed row and manifest byte upper bounds

All products and sums in this section are guarded. A schema field addition, wider
enum, free text, arbitrary path, or wider array invalidates these formulae and the
schema/profile version.

### 7.1 Input, state, candidate, and primary rows

```text
original_input_json_upper =
    FIXED_ORIGINAL_INPUT_JSON_BYTES + 2*n*FLOAT_HEX_JSON_BYTES

reference_spec_json_upper =
    FIXED_REFERENCE_SPEC_JSON_BYTES
    + C*(d(h)+1)
    + 6*d(M)
    + 5*FLOAT_HEX_JSON_BYTES
    + FIXED_APPROVED_BINDING_JSON_BYTES
    + 3*HASH_JSON_BYTES

circular_state_json_upper = FIXED_STATE_JSON_BYTES + d(max(n-1,0))
block_state_json_upper =
    FIXED_STATE_JSON_BYTES + q*(d(max(q-1,0))+1)
state_json_upper = applicable maximum above

candidate_record_json_upper =
    FIXED_CANDIDATE_JSON_BYTES
    + 6*d(M)
    + 4*FLOAT_HEX_JSON_BYTES
    + FAILURE_CODE_JSON_BYTES

selection_json_upper =
    FIXED_SELECTION_JSON_BYTES
    + 6*d(M)
    + C*(d(max(C-1,0))+1)
    + 3*FLOAT_HEX_JSON_BYTES

schedule_spool_row_upper =
    FIXED_SCHEDULE_SPOOL_ROW_JSON_BYTES
    + d(max(B-1,0))
    + state_json_upper
    + 1

state_row_json_upper =
    FIXED_STATE_ROW_JSON_BYTES
    + state_json_upper
    + C*candidate_record_json_upper
    + selection_json_upper
    + 8*d(M)
    + 3*HASH_JSON_BYTES
    + 2*FAILURE_CODE_JSON_BYTES
    + 1

observed_record_json_upper =
    FIXED_OBSERVED_ROW_JSON_BYTES
    + C*candidate_record_json_upper
    + selection_json_upper
    + 5*d(M)
    + 3*HASH_JSON_BYTES
    + 2*FAILURE_CODE_JSON_BYTES
```

`selection_json_upper` is included even on an analytic-failure branch because the
maximum of the complete and failed schema branches is used; null is shorter.

### 7.2 Comparison records by record kind

The arrays are bounded before encoding:

```text
H = 9*C + 16
J = max_diagnostic_recomputations
G = max_disagreement_codes_per_record

field_comparison_json_upper =
    FIXED_COMPARISON_FIELD_JSON_BYTES
    + 2*SCALAR_COMPARISON_JSON_BYTES
    + 2*FLOAT_HEX_JSON_BYTES
    + 2*FAILURE_CODE_JSON_BYTES

production_observed_projection_upper =
    FIXED_PRODUCTION_PROJECTION_JSON_BYTES
    + C*candidate_record_json_upper
    + selection_json_upper
    + 2*FAILURE_CODE_JSON_BYTES

production_state_projection_upper =
    FIXED_PRODUCTION_PROJECTION_JSON_BYTES
    + state_json_upper
    + C*candidate_record_json_upper
    + selection_json_upper
    + 4*d(M)
    + 2*FAILURE_CODE_JSON_BYTES

production_exact_aggregate_projection_upper =
    FIXED_PRODUCTION_PROJECTION_JSON_BYTES
    + 6*d(M)
    + 2*FLOAT_HEX_JSON_BYTES

production_finite_aggregate_projection_upper =
    FIXED_PRODUCTION_PROJECTION_JSON_BYTES
    + 10*d(M)
    + 4*FLOAT_HEX_JSON_BYTES
```

Let `row_common(projection, locator)` be:

```text
FIXED_COMPARISON_ROW_JSON_BYTES
+ projection
+ locator
+ H*field_comparison_json_upper
+ J*(d(max_diagnostic_recomputations)+1)
+ G*FAILURE_CODE_JSON_BYTES
+ 6*d(M)
+ 3*HASH_JSON_BYTES
+ 1 LF
```

The explicit record-kind maxima are:

```text
comparison_observed_row_upper = row_common(
    production_observed_projection_upper,
    file_locator_upper(ascii_bytes("observed-record.json")),
)

comparison_state_row_upper = row_common(
    production_state_projection_upper,
    row_locator_upper(P_art,max(T,B,1)),
)

comparison_exact_aggregate_row_upper = row_common(
    production_exact_aggregate_projection_upper,
    file_locator_upper(ascii_bytes("exact-manifest.json")),
)

comparison_finite_aggregate_row_upper = row_common(
    production_finite_aggregate_projection_upper,
    file_locator_upper(ascii_bytes("finite-b-manifest.json")),
)
```

There is no single untyped comparison-row multiplier. Ledger bounds use the maximum
for each actual record kind:

```text
comparison_rows_upper_exact =
    T*comparison_state_row_upper
    + comparison_exact_aggregate_row_upper

comparison_rows_upper_finite_normal =
    comparison_observed_row_upper
    + B*comparison_state_row_upper
    + comparison_finite_aggregate_row_upper

comparison_rows_upper_finite_observed_failure_actual =
    comparison_observed_row_upper
    + comparison_finite_aggregate_row_upper

comparison_rows_admission_upper_finite =
    comparison_rows_upper_finite_normal
```

The schema and semantic verifier must enforce `candidateRecords=C` wherever that
array exists, `fieldComparisons<=9*C+16`,
`diagnosticIndices<=max_diagnostic_recomputations`, and the exact `R` sequence.

### 7.3 Streamed diagnostic rows

One diagnostic recomputation is encoded as an ordered group:

1. exactly one `DIAGNOSTIC_HEADER`;
2. zero or more small body rows, each exactly one of `EDGE`, `CODE`, `COUNTER`, or
   `NUMERICAL`;
3. exactly one `DIAGNOSTIC_FOOTER`.

Every row carries a global `diagnosticRowIndex=0..Z-1`. Every group carries
`diagnosticIndex=0..D_exec-1`; body rows additionally carry a consecutive
`bodyIndex`, and comparison records refer to these group-level diagnostic indices.
The footer binds the exact header identity, body-row count, and SHA-256 of the
canonical body rows only. The diagnostic manifest binds all chunk bytes, including
headers and footers, so neither footer nor manifest hashes itself.

No diagnostic row may contain an array of edges, codes, Counter entries, or numerical
records. The header declares expected counts and
`productionCounterAvailability=AVAILABLE|UNAVAILABLE`. If unavailable, it includes a
closed reason code and production Counter row counts must be zero. If available,
both production `FORWARD` and `REVERSE` directions and all four Counter kinds must be
complete. One available direction without the other is an integrity failure.

Reference diagnostics always emit both `FORWARD` and `REVERSE` Counter directions.
Counters within a direction are ordered by Counter kind and then lexicographic key;
production Counter rows, when available, add two more directions.
Each `COUNTER` row carries exactly one entry and the closed fields
`implementationRole`, `direction`, `counterKind`, and the applicable integer key
components plus count. Each `EDGE` or `CODE` row likewise carries exactly one scalar
entry. This is a physical streaming rule, not merely a logical array projection.

Small-row byte bounds are:

```text
diagnostic_header_row_upper =
    FIXED_DIAGNOSTIC_HEADER_JSON_BYTES
    + 12*d(M)
    + 4*HASH_JSON_BYTES
    + FAILURE_CODE_JSON_BYTES
    + 1

diagnostic_edge_row_upper =
    FIXED_DIAGNOSTIC_EDGE_JSON_BYTES
    + 5*d(M)
    + FLOAT_HEX_JSON_BYTES
    + 1

diagnostic_code_row_upper =
    FIXED_DIAGNOSTIC_CODE_JSON_BYTES
    + 6*d(M)
    + 1

diagnostic_counter_row_upper =
    FIXED_DIAGNOSTIC_COUNTER_JSON_BYTES
    + 9*d(M)
    + 1

diagnostic_numerical_row_upper =
    FIXED_DIAGNOSTIC_NUMERICAL_JSON_BYTES
    + 6*d(M)
    + 8*FLOAT_HEX_JSON_BYTES
    + 1

diagnostic_footer_row_upper =
    FIXED_DIAGNOSTIC_FOOTER_JSON_BYTES
    + 12*d(M)
    + 2*HASH_JSON_BYTES
    + 1
```

### 7.4 Diagnostic row counts

For NetTE:

```text
edge_entries = 2*(bins+1)
u3 = min_power_cap(bins,3,N)
u2 = min_power_cap(bins,2,N)
u1 = min(N,bins)
U = u3 + 2*u2 + u1
```

`U` is one direction's four Counter tables. Preflight requires
`U<=max_counter_entries_upper` and `edge_entries<=max_edge_entries`.

For one NetTE diagnostic recomputation:

```text
header_rows = 1
edge_rows = 2*(bins+1)
code_rows = 2*n
reference_counter_rows = 2*U
production_counter_rows_upper = 2*U
numerical_rows_upper = max_numerical_rows_per_diagnostic
footer_rows = 1

diagnostic_rows_one_upper =
    header_rows + edge_rows + code_rows
    + reference_counter_rows + production_counter_rows_upper
    + numerical_rows_upper + footer_rows
```

If production counters are unavailable, actual production Counter rows are zero, but
admission retains the `2*U` upper. For Pearson, edge/code/Counter counts are zero and
only header, at most `max_numerical_rows_per_diagnostic` numerical rows, and footer
exist.

```text
diagnostic_rows_total_upper =
    max_diagnostic_recomputations * diagnostic_rows_one_upper

Z_admit = min(
    diagnostic_rows_total_upper,
    max_diagnostic_ledger_bytes // MIN_DIAGNOSTIC_ROW_BYTES,
)

diagnostic_group_bytes_upper =
    diagnostic_header_row_upper
    + edge_rows*diagnostic_edge_row_upper
    + code_rows*diagnostic_code_row_upper
    + reference_counter_rows*diagnostic_counter_row_upper
    + production_counter_rows_upper*diagnostic_counter_row_upper
    + numerical_rows_upper*diagnostic_numerical_row_upper
    + diagnostic_footer_row_upper

diagnostic_rows_bytes_upper =
    max_diagnostic_recomputations * diagnostic_group_bytes_upper
```

`diagnostic_rows_bytes_upper` is a shape proof, not a requirement to reserve every
possible discrepancy at once. Diagnostics are data-dependent: the admitted retained
ledger account is `max_diagnostic_ledger_bytes`, and the writer may terminate with a
resource failure before the next complete row/group. Because every JSONL row has at
least `MIN_DIAGNOSTIC_ROW_BYTES` under the closed schema, `Z_admit` safely bounds the
number of row paths/indices that can exist under that ledger account. Approval
requires a minimum-shape proof as well as each maximum-shape proof; if any legal row
is shorter, this formula/version is invalid. Actual complete comparison requires all
required groups to fit; a runtime cap does not authorize truncation.

This replaces revision 3's impossible giant `single_diagnostic_json_upper`. Every
write checks the next complete small row before append; no partial row is retained as
valid JSONL.

### 7.5 Manifest bounds

Let `A_desc` be `artifact_descriptor_upper(P_art)`, `S_desc` the maximum state-chunk
descriptor, `C_desc` the maximum comparison-chunk descriptor, and `D_desc` the
maximum diagnostic-chunk descriptor. Then:

```text
A_desc = artifact_descriptor_upper(P_art)
S_desc = chunk_descriptor_upper(chunk_path_bytes("state"),max(T,B,1))
C_desc = chunk_descriptor_upper(chunk_path_bytes("comparison"),R_admit)
D_desc = chunk_descriptor_upper(chunk_path_bytes("diagnostic"),Z_admit)

primary_manifest_upper_exact =
    FIXED_PRIMARY_MANIFEST_JSON_BYTES
    + 2*A_desc
    + primary_chunk_count(T)*S_desc
    + 16*d(M)
    + 3*HASH_JSON_BYTES
    + FIXED_APPROVED_BINDING_JSON_BYTES

primary_manifest_upper_finite =
    FIXED_PRIMARY_MANIFEST_JSON_BYTES
    + 4*A_desc
    + primary_chunk_count(B)*S_desc
    + 20*d(M)
    + 4*HASH_JSON_BYTES
    + FIXED_APPROVED_BINDING_JSON_BYTES

diagnostic_manifest_upper =
    FIXED_DIAGNOSTIC_MANIFEST_JSON_BYTES
    + A_desc
    + diagnostic_chunk_count(Z_admit)*D_desc
    + 8*d(M)
    + 3*HASH_JSON_BYTES

implementation_identity_upper =
    FIXED_IMPLEMENTATION_IDENTITY_JSON_BYTES
    + max_implementation_path_bytes
    + d(max_run_package_bytes)
    + HASH_JSON_BYTES

comparison_manifest_upper =
    FIXED_COMPARISON_MANIFEST_JSON_BYTES
    + 2*A_desc
    + comparison_chunk_count(R_admit)*C_desc
    + 3*implementation_identity_upper
    + FIXED_RUNTIME_IDENTITY_JSON_BYTES
    + FIXED_APPROVED_BINDING_JSON_BYTES
    + 16*d(M)
    + 5*HASH_JSON_BYTES
```

`implementationIdentities` is not merely `minItems=3`; schema and semantic
verification require exactly three and the three unique roles stated in section 3.

The maximum number of artifacts that a failure manifest may describe excludes both
the reserve and the failure manifest itself:

```text
retained_descriptor_count_upper =
    2                                      # original + spec
    + (2 if finite else 0)                 # spool + observed
    + primary_chunk_count(L_admit)
    + 1                                    # one primary manifest
    + comparison_chunk_count(R_admit)
    + diagnostic_chunk_count(Z_admit)
    + 1                                    # optional diagnostic manifest upper
```

```text
failure_manifest_upper =
    FIXED_FAILURE_MANIFEST_JSON_BYTES
    + retained_descriptor_count_upper*failure_descriptor_upper(P_failure)
    + 48*d(M)
    + 8*HASH_JSON_BYTES
```

The failure manifest does not hash itself. It may name only artifacts that actually
exist; the count above is an upper, not a requirement to fabricate descriptors.

## 8. The only legal artifact graph

The graph contains only these nodes:

```text
original-input.json
reference-spec.json
  [FINITE only] schedule-spool.jsonl
  [FINITE only] observed-record.json
state-chunks/state-*.jsonl
exact-manifest.json OR finite-b-manifest.json
comparison-chunks/comparison-*.jsonl
  [only when required and complete]
  diagnostic-chunks/diagnostic-*.jsonl -> diagnostic-manifest.json
comparison-manifest.json                 # success terminal root
OR
failure-manifest.json                    # resource/integrity/interruption terminal root
```

There is no artifact index and no success manifest. `comparison-manifest.json` is the
only success root. `failure-manifest.json` is the only failure root. They are mutually
exclusive. A primary analytic failure is an adverse scientific result, not by itself
a package failure; it can still end in a complete comparison manifest with overall
status `NOT_COMPARABLE`.

The exact branch has no spool or separate observed record; its identity state is in
the state stream. A finite observed-failure branch has spool and observed record,
zero state chunks, a finite primary manifest, exactly two comparison records, and a
comparison manifest. No empty state chunk is invented.

The `.failure-manifest.reserve` allocation is transient filesystem safety space. It
is never named by a manifest, never counted as a retained artifact, and is removed
after a verified success root. On failure, it is used to install the failure manifest
without allocating a second reserve-sized file; after atomic installation only the
actual failure-manifest bytes remain.

## 9. Package and ledger byte accounting

Accounts are disjoint:

```text
I_formula_u = original_input_json_upper + reference_spec_json_upper
I = exact verified bytes(original-input.json) + exact verified bytes(reference-spec.json)
S = exact verified spool bytes in finite mode; 0 in exact mode
O_u = observed_record_json_upper in finite mode; 0 in exact mode

P_rows_u = L_admit*state_row_json_upper
P_manifest_u = applicable primary_manifest_upper
C_rows_u = applicable record-kind comparison row upper from section 7.2
D_rows_u = max_diagnostic_ledger_bytes
D_manifest_u = diagnostic_manifest_upper
Root_success_u = comparison_manifest_upper
Root_failure_u = failure_manifest_upper
```

Before any artifact is written, admission uses `I_formula_u` and requires
`I_formula_u<=max_input_sidecar_bytes`. Only after the two sidecars are
incrementally written, fsynced, re-read, and hashed may the tighter exact `I`
replace it. `I>I_formula_u` is an integrity contradiction, not an ordinary resource
rejection. The same formula-first, exact-after-verification rule applies to `S`.

The named hard ledgers mean rows only:

```text
require P_rows_u <= max_primary_ledger_bytes
require C_rows_u <= max_comparison_ledger_bytes
require every next complete diagnostic row and group <= remaining D_rows_u
```

Manifests, sidecars, spool, and roots are not smuggled into those names. They are
included in the run-package bound:

```text
nonterminal_u =
    I + S + O_u + P_rows_u + P_manifest_u
    + C_rows_u + D_rows_u + D_manifest_u

success_package_u = nonterminal_u + Root_success_u
failure_package_u = nonterminal_u + Root_failure_u
final_retained_package_u = max(success_package_u,failure_package_u)

require final_retained_package_u <= max_run_package_bytes
require Root_failure_u <= FAILURE_MANIFEST_RESERVE_BYTES
```

The first preflight evaluation substitutes `I=I_formula_u` and, in finite mode,
`S=spool_formula_u`. Later exact values may only tighten the admitted upper.

Before a one-shot finite schedule is consumed, use its formula upper:

```text
spool_formula_u = B*schedule_spool_row_upper
require spool_formula_u <= max_schedule_spool_bytes
```

The static package admission substitutes `S=spool_formula_u`. Before each complete
spool row, enforce the remaining spool cap. After close, fsync, re-read, row-order
validation, and SHA-256 verification, set `S` to the exact verified spool bytes and
recompute the tighter package upper. A contradiction between admitted formula and
actual bytes is `REFERENCE_INTEGRITY_FAILURE`, not an ordinary resource rejection.

The maximum write-time occupancy is:

```text
run_directory_transient_upper =
    final_retained_package_u
    + FAILURE_MANIFEST_RESERVE_BYTES
    + max(Root_success_u,Root_failure_u)
```

The last term conservatively covers the terminal root's `.partial` file immediately
before same-directory atomic rename. Copy-and-replace is forbidden. Admission also
requires that this actual reservation can be made as a non-sparse allocation and
fsynced. A request whose closed failure-manifest upper cannot fit the fixed reserve
is rejected before artifact production with `FAILURE_MANIFEST_RESERVE_LIMIT`. The
transient upper is not called final package size.

## 10. Finite observed analytical failure: fixed fail-fast branch

The finite schedule is completely spooled and verified before any statistic. Then:

1. execute the observed scan;
2. if it is analytically failed, retain the complete candidate failure vector in
   `observed-record.json`;
3. do not scan any of the `B` scheduled states;
4. emit no state chunks;
5. write `finite-b-manifest.json` with the fixed nullability below;
6. compare the observed terminal result and aggregate terminal shape only;
7. emit exactly two comparison rows and a success-root comparison manifest whose
   overall status is `NOT_COMPARABLE`, unless a resource/integrity/interruption
   failure instead requires the failure root.

The primary manifest carries:

```text
plannedB = B
plannedDenominator = B+1
plannedDenominatorStatus = "DESIGN_CONSTANT"
executedStatisticScans = 1
executedScheduledScans = 0
validReplicateCount = null
E = null
F = null
lowerNumerator = null
upperNumerator = null
lowerBoundHex = null
upperBoundHex = null
pValueHex = null
decision = null
```

`plannedDenominator` is not an executed denominator, evidence of coverage, or a
p-value denominator. `F` is null because none of the planned rows was executed; it is
not `0` and not `B`. The static admission still uses `Q_admit=B+1`, `L_admit=B`, and
`R_admit=B+2`; the actual receipt records `Q_exec=1`, `L_exec=0`, and `R_exec=2`.

## 11. Separate compute-work and byte-I/O axes

A compute-work unit is one declared primitive operation below. A byte-I/O visit is
one byte passed through one declared read, write, or hash operation. Neither is
elapsed time, CPU cycles, process memory, or a scientific threshold.

### 11.1 Compute work

Use `sort_units(m)=0` for `m<=1`, else
`2*m*ceil_log2_positive(m)`, with guarded operations.

For the admitted branch:

```text
transform_units = X_admit*n
candidate_support_units = Q_admit*C*N
selection_units = 3*Q_admit*C

pearson_value_units = 6*Q_admit*C*N

nette_edge_units = 2*n + 2*(bins+1)
nette_coding_units = 2*Q_admit*n
nette_directional_units = 2*Q_admit*C*N
nette_counter_units = 8*Q_admit*C*N
nette_sort_units = 2*Q_admit*C*sort_units(u3)

comparison_units_upper = R_admit*(C + H + J + G + 1)
```

Pearson primary compute is:

```text
primary_compute_units_pearson =
    transform_units + candidate_support_units
    + pearson_value_units + selection_units
```

NetTE primary compute is:

```text
primary_compute_units_nette =
    transform_units + candidate_support_units
    + nette_edge_units + nette_coding_units
    + nette_directional_units + nette_counter_units
    + nette_sort_units + selection_units

primary_compute_units =
    primary_compute_units_pearson if Pearson
    else primary_compute_units_nette
```

Preflight checks the following exact mappings rather than treating the total as a
substitute for its components:

```text
B <= max_schedule_rows                                      # finite only
T <= max_exact_state_count                                  # exact only
L_admit*C <= max_ledger_candidate_records
C <= max_live_candidate_records
transform_units <= max_transform_value_visits
candidate_support_units <= max_candidate_support_visits
selection_units <= max_selection_work_units
pearson_value_units <= max_pearson_value_visits              # Pearson only
nette_edge_units <= max_nette_edge_work_units                # NetTE only
nette_directional_units <= max_nette_directional_support_visits
nette_counter_units <= max_nette_counter_update_visits
nette_sort_units <= max_nette_sort_units
primary_compute_units <= max_primary_compute_work_units
comparison_units_upper <= max_comparison_compute_work_units
```

One NetTE diagnostic recomputation upper is:

```text
diagnostic_compute_one_nette =
    n                              # transform
    + 2*n                          # coding
    + 2*(bins+1)                   # edge traversal/emission
    + 2*N                          # two reference directions
    + 8*N                          # four counters, two directions
    + 2*sort_units(u3)
    + 4*sort_units(u2)
    + 2*sort_units(u1)
    + 2*U                          # admitted traversal of available production counters
    + diagnostic_rows_one_upper    # bounded record assembly
```

The `2*U` term is charged at admission whether or not production counters ultimately
prove available. At execution, unavailable production counters contribute zero
actual traversal/emission units and the receipt records that absence. Production
Counter construction cost belongs to the production envelope, not this reference-
owned compute claim.

For Pearson, one diagnostic upper is:

```text
diagnostic_compute_one_pearson =
    n + 6*C*N + 3*C
    + 2 + max_numerical_rows_per_diagnostic
```

Static diagnostic and total admission use the full allowed discrepancy count:

```text
diagnostic_compute_one_upper =
    diagnostic_compute_one_pearson if Pearson
    else diagnostic_compute_one_nette

diagnostic_compute_potential_upper =
    max_diagnostic_recomputations * diagnostic_compute_one_upper

diagnostic_compute_budget_admit = min(
    diagnostic_compute_potential_upper,
    max_diagnostic_compute_work_units,
)

total_compute_work_units_admit =
    primary_compute_units
    + comparison_units_upper
    + diagnostic_compute_budget_admit
```

At runtime:

```text
diagnostic_compute_units = sum(actual bounded recomputations)
total_compute_work_units =
    primary_compute_units
    + comparison_compute_units
    + diagnostic_compute_units
```

Admission and runtime checks additionally require
`diagnostic_compute_budget_admit<=max_diagnostic_compute_work_units`,
`total_compute_work_units_admit<=max_total_compute_work_units`, and the analogous
actual counters at runtime. Before each recomputation, its full admitted upper must
fit the remaining diagnostic and total budgets; otherwise diagnostics stop before
that recomputation and the failure root preserves the partial state. This axis covers transform,
support, Pearson arithmetic or NetTE coding/edges/directions/Counters/sort,
selection, comparison, and diagnostics. It is never labelled total CPU or total
process work.

For observed-failure actual receipts, recompute the same expressions with
`Q_exec=1`, `X_exec=0` for scheduled transformations, `R_exec=2`, and actual
diagnostics. Admission remains based on the larger static operands.

### 11.2 Byte-I/O visits

Define:

```text
emit_verify(x) = 4*x
    # one write + one incremental-hash pass + one verification read
    # + one verification-hash pass

dependency_reread(x) = 2*x
    # one read + one simultaneous verification-hash pass
```

Let `P=P_rows_actual+P_manifest_actual`, `Cio=comparison_rows_actual`,
`D=diagnostic_rows_actual+diagnostic_manifest_actual`, and `Root` be the actual
terminal-root bytes. The success-path upper is:

```text
io_sidecars = emit_verify(I)
io_spool = emit_verify(S)
io_primary = emit_verify(O_actual + P)
io_comparison_dependencies = dependency_reread(I + S + O_actual + P)
io_comparison_rows = emit_verify(Cio)
io_diagnostics = emit_verify(D)
io_terminal_root = emit_verify(Root)

io_byte_visits_success = sum(all seven terms)
```

The failure path substitutes actual complete or partial bytes visited before failure,
adds any best-effort verification re-reads actually performed, and adds
`emit_verify(actual failure-manifest bytes)` when custody succeeds. Static admission
uses these closed conservative bounds:

```text
Dependency_u = I_formula_u + spool_formula_u + O_u + P_rows_u + P_manifest_u
Nonroot_emit_u =
    I_formula_u + spool_formula_u + O_u + P_rows_u + P_manifest_u
    + C_rows_u + D_rows_u + D_manifest_u

io_success_u =
    emit_verify(Nonroot_emit_u + Root_success_u)
    + dependency_reread(Dependency_u)

io_failure_u =
    emit_verify(Nonroot_emit_u + Root_failure_u)
    + dependency_reread(Nonroot_emit_u)

io_byte_visits_u = max(io_success_u,io_failure_u)
require io_byte_visits_u <= max_io_byte_visits
```

Exact mode substitutes `spool_formula_u=0`. The failure upper allows every
nonterminal byte to have been emitted, then best-effort re-read, before installing
the failure root. An actual receipt reports the sum of actual stage counters and it
must not exceed the admitted upper. A hash pass is never hidden inside compute work,
and byte-I/O is never presented as CPU work.

## 12. Conditional reference-owned memory upper

### 12.1 Primitive-count-first rule

Memory is derived first from simultaneously live primitive counts and then from the
bounded incremental encoder. Serialized row size is not used as a proxy for Python
object memory, and a complete encoded row is forbidden.

Define the following primitive-count functions:

```text
sequence_values(k,value_bytes) =
    CONTAINER_BASE_PEAK_BYTES + k*value_bytes

state_payload(W_state) =
    2*CONTAINER_BASE_PEAK_BYTES
    + W_state*INTEGER_VALUE_PEAK_BYTES
    + RECORD_BASE_PEAK_BYTES

enumerator_workspace(W_state) =
    4*CONTAINER_BASE_PEAK_BYTES
    + 3*W_state*INTEGER_VALUE_PEAK_BYTES
    + RECORD_BASE_PEAK_BYTES

ENUMERATOR_LIVE =
    enumerator_workspace(W_state) if ALL_STATE_EXACT else 0

candidate_vector(C) =
    CONTAINER_BASE_PEAK_BYTES
    + C*CANDIDATE_RECORD_PEAK_BYTES
    + SELECTION_RECORD_PEAK_BYTES

field_comparison_vector(H,J,G) =
    3*CONTAINER_BASE_PEAK_BYTES
    + H*FIELD_COMPARISON_PEAK_BYTES
    + J*INTEGER_VALUE_PEAK_BYTES
    + G*FAILURE_CODE_VALUE_PEAK_BYTES

counter_direction(U) =
    4*CONTAINER_BASE_PEAK_BYTES
    + U*COUNTER_ENTRY_PEAK_BYTES

sort_workspace(U) =
    CONTAINER_BASE_PEAK_BYTES + U*SORT_ENTRY_PEAK_BYTES

encoder_live =
    ENCODER_FRAME_PEAK_BYTES
    + 2*MAX_CANONICAL_TOKEN_BYTES       # at most one str token and one bytes token
    + STREAM_WRITE_BUFFER_BYTES
    + HASH_SCRATCH_BYTES
```

`failure_descriptor_stream_live` is one
`FAILURE_DESCRIPTOR_PEAK_BYTES`; `chunk_descriptor_stream_live` is one
`CHUNK_DESCRIPTOR_PEAK_BYTES`. Manifest descriptor arrays are never materialized;
descriptors are regenerated in canonical order and streamed one at a time.

### 12.2 Exact simultaneous-live inventories

Common inputs are:

```text
INPUT_LIVE =
    2*sequence_values(n,FLOAT_VALUE_PEAK_BYTES)
    + sequence_values(C,INTEGER_VALUE_PEAK_BYTES)
    + 4*RECORD_BASE_PEAK_BYTES
```

The phase inventories are:

```text
peak_input_canonicalization =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + encoder_live

peak_schedule_spool =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + state_payload(W_state)
    + 2*RECORD_BASE_PEAK_BYTES
    + encoder_live

peak_primary_pearson =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + sequence_values(n,FLOAT_VALUE_PEAK_BYTES)      # transformed source
    + 6*sequence_values(N,FLOAT_VALUE_PEAK_BYTES)    # Pearson workspace
    + candidate_vector(C)
    + state_payload(W_state)
    + ENUMERATOR_LIVE
    + 4*RECORD_BASE_PEAK_BYTES                       # state/row/scalars
    + encoder_live

peak_primary_nette =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + sequence_values(n,FLOAT_VALUE_PEAK_BYTES)      # transformed source
    + 2*sequence_values(n,INTEGER_VALUE_PEAK_BYTES)  # source/target codes
    + 2*sequence_values(bins+1,FLOAT_VALUE_PEAK_BYTES)
    + counter_direction(U)                           # one direction only
    + sort_workspace(U)
    + candidate_vector(C)
    + state_payload(W_state)
    + ENUMERATOR_LIVE
    + 6*RECORD_BASE_PEAK_BYTES
    + encoder_live

peak_comparison =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + 2*candidate_vector(C)             # one reference, one bounded projection
    + 2*state_payload(W_state)           # reference and production state payloads
    + field_comparison_vector(H,J,G)
    + 6*RECORD_BASE_PEAK_BYTES
    + encoder_live

peak_diagnostic_nette =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + sequence_values(n,FLOAT_VALUE_PEAK_BYTES)
    + 2*sequence_values(n,INTEGER_VALUE_PEAK_BYTES)
    + 2*sequence_values(bins+1,FLOAT_VALUE_PEAK_BYTES)
    + counter_direction(U)              # reference forward or reverse, never both
    + sort_workspace(U)
    + state_payload(W_state)
    + COUNTER_ENTRY_PEAK_BYTES           # one streamed production entry
    + 8*RECORD_BASE_PEAK_BYTES
    + encoder_live

peak_manifest =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + max(CHUNK_DESCRIPTOR_PEAK_BYTES,FAILURE_DESCRIPTOR_PEAK_BYTES)
    + 8*RECORD_BASE_PEAK_BYTES
    + encoder_live

peak_verification_reread =
    FIXED_PHASE_OVERHEAD_BYTES
    + INPUT_LIVE
    + STREAM_READ_BUFFER_BYTES
    + DECODER_SCRATCH_BYTES
    + max(
        candidate_vector(C) + state_payload(W_state) + 4*RECORD_BASE_PEAK_BYTES,
        2*candidate_vector(C) + 2*state_payload(W_state)
            + field_comparison_vector(H,J,G),
        8*RECORD_BASE_PEAK_BYTES,
      )
    + HASH_SCRATCH_BYTES
```

The reference-owned conditional bound is the maximum applicable phase. Each phase
lists every simultaneously live container, record, `str` token, `bytes` token,
buffer, and hash scratch region. Primary and diagnostic NetTE process directions
sequentially; keeping two directions simultaneously violates the model.

Admission requires the maximum to be no greater than
`max_reference_owned_peak_upper_bytes`. Layout probes on the exact supported runtime
must independently show that every primitive constant is conservative. `read()`,
`readlines()`, whole-ledger `json.loads()`, whole-object `json.dumps()`, full-row
`.encode()`, retention of prior chunks, materialized manifest descriptor arrays, or
more simultaneous objects than listed is `MEMORY_MODEL_VIOLATION`.

### 12.3 Explicit exclusion

This is not a total-process upper. It excludes arbitrary external schedule-generator
memory, production API/third-party temporary allocations, interpreter/import
baseline, allocator fragmentation, OS accounting, and other processes. A total-
process claim requires a separately approved bounded adapter and enforced subprocess
limit. If required but unavailable, return
`TOTAL_PROCESS_RESOURCE_BOUND_UNAVAILABLE`; do not rename this conditional bound.

## 13. Three-axis truth table and failure custody

Every terminal root has exactly:

```text
axisStates = {
  primary: {custodyStatus, semanticStatus},
  diagnostic: {custodyStatus, semanticStatus},
  comparison: {custodyStatus, semanticStatus}
}
```

`custodyStatus = NONE | PARTIAL | COMPLETE` describes retained and reverified bytes.
The only legal pairs are:

| Axis | Custody | Semantic | Legal circumstance |
| --- | --- | --- | --- |
| primary | `NONE` | `NOT_STARTED` | stopped before any primary artifact |
| primary | `COMPLETE` | `COMPLETE` | all required primary bytes reverified; all scans evaluable |
| primary | `COMPLETE` | `ANALYTICALLY_UNEVALUABLE` | complete adverse primary result, including finite observed fail-fast |
| primary | `NONE` or `PARTIAL` | `RESOURCE_LIMIT` | resource stop before/within primary custody |
| primary | `NONE` or `PARTIAL` | `INTEGRITY_FAILURE` | primary bytes cannot be verified |
| primary | `NONE` or `PARTIAL` | `INTERRUPTED` | interrupted before primary completion |
| diagnostic | `NONE` | `NOT_REQUIRED` | no discrepancy requires diagnostics |
| diagnostic | `COMPLETE` | `COMPLETE` | every required diagnostic group/footer and manifest reverified |
| diagnostic | `NONE` or `PARTIAL` | `RESOURCE_LIMIT` | diagnostic resource stop |
| diagnostic | `NONE` or `PARTIAL` | `INTEGRITY_FAILURE` | diagnostic verification failure |
| diagnostic | `NONE` or `PARTIAL` | `INTERRUPTED` | diagnostic interruption |
| comparison | `NONE` | `NOT_STARTED` | no comparison began |
| comparison | `COMPLETE` | `COMPLETE_AGREEMENT` | closed comparison set agrees |
| comparison | `COMPLETE` | `COMPLETE_DISAGREEMENT` | closed mismatch plus all required diagnostics |
| comparison | `COMPLETE` | `NOT_COMPARABLE` | closed comparison set legitimately lacks comparable inferential quantities, including observed fail-fast |
| comparison | `PARTIAL` | `NOT_COMPARABLE` | comparison rows exist but required diagnostic characterization did not complete |
| comparison | `NONE` or `PARTIAL` | `RESOURCE_LIMIT` | comparison construction resource stop |
| comparison | `NONE` or `PARTIAL` | `INTEGRITY_FAILURE` | comparison custody or linkage failure |
| comparison | `NONE` or `PARTIAL` | `INTERRUPTED` | comparison interruption |

No other pair is valid. The word `INDETERMINATE` is forbidden; the common semantic
term is `NOT_COMPARABLE`. A later-axis failure does not erase a previously complete
primary axis. A diagnostic failure leaves comparison
`PARTIAL/NOT_COMPARABLE` and requires a failure root.

Analytical failure uses a comparison success root only when all bytes appropriate to
that adverse branch are complete and verified. Resource limit, integrity failure, or
interruption always uses the failure root.

Before artifact production, reserve the non-sparse failure allocation. On failure:

1. stop before a partial next JSONL row;
2. close and fsync every existing partial artifact where possible;
3. re-read and hash each retained artifact where possible;
4. encode it as `VERIFIED` or `UNVERIFIED` exactly as section 6 requires;
5. stream the closed failure manifest through the reserve, fsync, and atomically
   install `failure-manifest.json`;
6. do not install or retain `comparison-manifest.json`.

Failure descriptors preserve adverse evidence; they never transform unverified data
into verified custody.

## 14. Non-cyclic approved-contract binding

Revision 4 uses three independent digests:

1. `formulaSha256`: raw bytes of this formula file after review;
2. `schemaSha256`: raw bytes of
   `docs/benchmarks/schemas/m6-p1-artifact-contract-v4-proposal.schema.json` after
   review;
3. `budgetProfileSha256`: canonical JSON bytes of the exact constants registry
   projection, with no LF.

None of those three objects contains its own digest. They are bound only by a fourth,
external approval record created after explicit owner approval. That record is
outside the run artifact graph and contains the three digests, approval identity,
time, and disposition. It also does not contain its own digest.

Every approved `reference-spec.json`, primary manifest, and terminal root copies the
external record's stable binding identifier and the same three component digests.
The semantic verifier resolves the external record and checks equality. A draft run
cannot substitute current working-tree hashes for an approved binding. There is no
formula/schema/profile self-hash cycle and no terminal-manifest self-hash.

## 15. Validation and execution order after approval

No step below has run and no implementation is authorized by this proposal.

1. validate closed primitive request types, rejecting booleans and nonfinite values;
2. validate every integer and `+1` through section 4;
3. validate null applicability and determine `T` with the cap-stopped algorithm;
4. derive `Q_admit/X_admit/L_admit/R_admit` and all array bounds;
5. validate component and total compute-work caps;
6. validate edge, Counter, diagnostic-row, chunk-count, and path bounds;
7. derive input/spec formula uppers and all record-kind byte, ledger, package,
   byte-I/O, and primitive-memory uppers; reject before any write if a cap fails;
8. reserve failure-manifest space and prove same-directory fsync/atomic-rename
   semantics before producing an artifact;
9. incrementally canonicalize input/spec, fsync, re-read, and verify exact sidecar
   bytes; tighten but never widen the admitted upper;
10. finite only: spool, close, fsync, re-read, validate `B` ordered rows, verify hash,
    and tighten the package bound;
11. run observed first in finite mode and take section 10's fail-fast branch if it
    fails analytically;
12. otherwise stream primary rows, then comparison rows, then required diagnostic
    groups, checking each next complete row and each runtime work/byte counter;
13. re-read and semantically verify all required artifacts;
14. atomically install exactly one terminal root; remove the transient reserve only
    after verified success installation.

No rejection may truncate an accepted schedule, discard repeated or identity states,
widen a numerical tolerance, convert a failed indicator to false, or fall back to
Monte Carlo.

## 16. Review-defect closure matrix

This matrix makes the revision-3 adverse review actionable. Closure here means only
that revision 4 states a proposed design disposition; independent review is still
required.

| Finding | Revision-4 disposition |
| --- | --- |
| `C01` comparison row count omitted aggregate | section 3 fixes exact `T+1`, finite `B+2`, observed-failure actual `2` |
| `C02` observed failure contradicted scheduled scanning | sections 3 and 10 freeze fail-fast after verified spool |
| `C03` one giant diagnostic row defeated streaming | sections 7.3–7.4 require header/body/footer small rows |
| `C04` reference/production Counter directions were ambiguous | section 7.3 requires two reference directions and availability-gated two production directions |
| `C05` artifact graph invented index/success files | section 8 removes both and fixes mutually exclusive terminal roots |
| `C06` comparison arrays were unbounded | sections 3 and 7.2 close all four array counts |
| `C07` failure descriptor could not truthfully retain unreadable data | sections 6 and 13 add `VERIFIED`/`UNVERIFIED`, with null SHA for the latter |
| `C08` work proxy omitted required operations | section 11.1 covers transform/support/statistic/edge/coding/directional/Counter/sort/selection/comparison/diagnostic |
| `C09` arithmetic could loop or overflow before guard | section 4 guards entries, loops, `+1`, power, and factorial |
| `C10` memory bound mixed serialization and object memory | section 12 derives primitive live counts first and prohibits whole-row encoding |
| `C11` axis states were internally contradictory | section 13 supplies a closed custody/semantic truth table and one `NOT_COMPARABLE` term |
| `I01` actual and admission counts were conflated | section 3 separates `_admit` and `_exec` operands |
| `I02` comparison used a generic row estimate | section 7.2 uses each record-kind maximum |
| `I03` chunking did not follow comparison `R` | section 3 defines stream-specific chunking by `R` |
| `I04` dynamic path bytes were not derived | section 5 defines fixed ASCII path generation and six-digit cap |
| `I05` integer digits were not fully charged | sections 6–7 add explicit guarded digit terms |
| `I06` descriptor sizes were not closed | section 6 separates artifact, chunk, and failure descriptors |
| `I07` package accounts overlapped | section 9 defines disjoint row/manifests/sidecar/root accounts |
| `I08` computation and I/O were conflated | section 11 gives two axes with distinct units and caps |
| `I09` simultaneous live strings/bytes/containers were unstated | section 12 lists each phase and incremental-encoder objects |
| `I10` approval digests created potential cycles | section 14 defines an external non-self-hashing binding |
| `M01` supersession claim was ambiguous | section 1 limits any future replacement to four named parent areas |
| `M02` reserve was treated as retained output | sections 8–9 make it transient only |
| `M03` finite failure metrics used misleading zeros | section 10 makes all unexecuted scheduled metrics null |
| `M04` status vocabulary drifted | section 13 forbids `INDETERMINATE` and uses `NOT_COMPARABLE` |

## 17. Symbol and artifact audit

Every formula symbol is defined in sections 2–7. In particular, `R`, `H`, `J`, `G`,
`U`, path lengths, digit counts, descriptor sizes, and all fixed constants have an
explicit source. `actual` variables are measured only after a complete write or
declared writer observation; `upper` variables are preflight bounds. They may not be
interchanged.

Every generated retained file maps to exactly one node in section 8. Every node has
a row/file/descriptor formula in sections 5–9. The reserve and `.partial` names are
transient custody mechanisms, not graph nodes. No artifact index, success manifest,
or predicted future hash exists.

## 18. Approval questions and claim ceiling

Before implementation, a specification owner must explicitly approve, revise, or
reject:

1. every proposed numeric constant in section 2;
2. the finite fail-fast and nullability contract;
3. the streamed diagnostic row vocabulary and production-Counter availability rule;
4. the exact artifact graph and terminal-root semantics;
5. the comparison array and record-count bounds;
6. the compute and byte-I/O unit definitions;
7. the runtime-profile scope of the conditional memory constants;
8. the companion v4 schema and external approved-contract binding.

Even after approval, implementation, and passing tests, this envelope can establish
only bounded, fail-closed execution and reproducible custody for admitted M6-P1
reference comparisons. It cannot establish statistical validity, Type-I-error
control, power, external validity, real-use usefulness, M6 scientific completion,
release approval, upload readiness, submission, acceptance, or SoftwareX readiness.

The controlling state remains:

```text
RESOURCE_ENVELOPE_REVISION_REQUIRED
NOT APPROVED
NOT FROZEN
NOT IMPLEMENTED
M6 NOT EXECUTED
```
