# M6-P1 resource envelope v1.1 revision 6 formula attachment

> **Status:** `PROPOSAL / NOT APPROVED / NOT FROZEN / PROVISIONAL SCHEMA BINDING / NOT IMPLEMENTATION AUTHORITY / M6 NOT EXECUTED`

> **Purpose:** Repair the integrated revision-5 formula/schema review without
> changing SelCal's statistic, selector, null semantics, tail rule, or tolerance.
> Revision 6 restores the parent scientific scope: finite reference work replays
> only the ordered state identities already emitted by a completed production
> result. It neither generates nor validates a production RNG schedule.

## 1. Authority and replacement boundary

Revision 6 is a new proposal. Revision 5 remains an adverse predecessor and is
not edited:

| Item | Bytes | SHA-256 | Status here |
| --- | ---: | --- | --- |
| Parent design, `2026-09-06-m6-p1-independent-reference-design.md` | `34234` | `ab6e40cc57eb5e4272451ebcb227eab45bf45f1ca66795530adb8d9957490064` | surviving scientific scope |
| Revision-5 formula | `85029` | `dcb994f561fc62cf76b478cbc8135c4086550e6b8b16fa2d7ab71373da94e6b8` | preserved adverse predecessor |
| Revision-5 schema | `283163` | `1c2bc7c6b8f14ac907627a7ae3e5728b1a76db2e766ee036df96f0c42d9388c6` | preserved adverse predecessor |
| Revision-6 companion schema | `318128` | `6137f391e557adcd1d84dd85a5b581d4632efba90d9a0041ce83af38de89be58` | provisional cross-audit target, not approved |

The companion v6 schema is provisional until its exact bytes, this attachment,
the deterministic budget projection, and a future external approval record are
cross-bound. This document does not approve any of them.

Only after that approval may revision 6 replace the parent's retained-state,
artifact, resource-admission, source-identity, diagnostic-custody, and output
sections. The following parent requirements survive unchanged:

1. independent scalar statistic and selector logic;
2. canonical candidates, support, state membership, order, identity flags, and
   repeated-state multiplicity;
3. separate reference and production failure ledgers;
4. inclusive tails without tolerance and exact integer count comparisons;
5. no truncation, deduplication, fallback, borrowed production score, or borrowed
   production failure label;
6. exact mode remains a component comparison, not a public full-enumeration run;
7. the parent claim ceiling and every external/release/submission HOLD.

## 2. Scientific execution scope and terminal order

### 2.1 Finite mode

The production public call is executed before reference replay. Its terminal
projection selects exactly one branch:

```text
production public call
  -> NULL_BIND_DISABLED
       no observed result; no replicate; zero reference statistic scans/states
  -> FINITE_OBSERVED_ANALYTIC_FAILURE
       observed vector exists; no replicate; reference scans observed once only
  -> FINITE_NORMAL or FINITE_REPLICATE_FAILURE
       completed actual.replicates exists in production order
       validate IDs/states/identity/multiplicity from that completed output
       independently apply and rescan each supplied state
```

There is no reference-planned-schedule artifact, policy, path, descriptor, hash,
I/O term, or failure stage. There is also no replacement schedule/projection file.
For the two completed-replicate branches, the only state source is:

```text
actual.replicates[b].replicate_id
actual.replicates[b].transform_token.state
actual.replicates[b].transform_token.is_identity
```

The driver requires IDs exactly `0..B-1`, retains repeated states, validates every
state against the frozen null, applies the state to the original input, and
recomputes the full candidate vector independently. The associated production
result projection is embedded in that state's comparison record. Production
scores, selections, validity labels, tail indicators, or failure reasons are
comparison operands only; none enters the reference calculation.

This is conditional replay of completed output, not validation of the generator
that produced it. RNG stream conformance, pre-execution state prediction, seed
search, token-generation equivalence, and distributional sampling validation are
outside M6-P1 and remain possible future designs. The manuscript may not claim
them from this comparison.

### 2.2 Exact component mode

Exact mode first checks null applicability without a statistic scan. If enabled,
the independent side enumerates the complete admitted labelled-state universe in
canonical order and applies every state. The production statistic and selector are
bound separately on those same states. No public calibration call or public exact
schedule is claimed. Null disablement performs zero state/statistic scans.

### 2.3 Branch order is causal

Before any scientific scan, validate primitive types, finite inputs, null
parameters, guarded integer operands, source-set closure, the branch's static
resource upper, and failure-root reserve support. In finite mode, the production
call then identifies the branch. Reference work can tighten a static upper but may
never widen it. In particular:

- null bind creates no observed or state record;
- observed analytical failure creates the independent observed record but never
  examines `B` state identities;
- completed finite branches replay exactly `B` production-emitted states;
- a missing, duplicate, out-of-order, malformed, nonmember, or extra production
  state is an integrity failure, not permission to synthesize a state;
- no analytical/resource/integrity failure may trigger an alternative RNG path.

## 3. Closed constants, strings, and source policies

Every numeric value in this section is `PROPOSED / NOT APPROVED`.

### 3.1 Scientific/resource constants

```text
max_operand_bits = 256
max_exact_state_count = 100000                 # inherited
retained_transformed_source_entries = 0        # inherited
max_finite_replicates = 1000
max_transform_value_visits = 2500000
max_candidate_support_visits = 2500000
max_pearson_value_visits = 15000000
max_nette_edge_work_units = 2500000
max_nette_coding_value_visits = 15000000
max_nette_directional_support_visits = 5000000
max_nette_counter_update_visits = 20000000
max_nette_sort_units = 25000000
max_nette_cmi_arithmetic_units = 30000000
max_selection_work_units = 1000000
max_state_generation_units = 2500000
max_state_identity_validation_units = 10000000
max_state_application_units = 2500000
max_null_bind_work_units = 16
max_primary_compute_work_units = 50000000
max_comparison_compute_work_units = 10000000
max_diagnostic_compute_work_units = 50000000
max_total_compute_work_units = 90000000
max_io_byte_visits = 4294967296
max_live_candidate_records = 5000
max_ledger_candidate_records = 100000
max_chunk_rows = 256
max_chunk_count_per_stream = 1000000
max_edge_entries = 65536
max_counter_entries_upper = 250000
max_diagnostic_recomputations = 256
max_pending_diagnostic_jobs = 0
max_numerical_rows_per_diagnostic = 8
max_disagreement_codes_per_record = 32
max_input_sidecar_bytes = 67108864
max_primary_ledger_bytes = 268435456
max_comparison_ledger_bytes = 134217728
max_diagnostic_ledger_bytes = 67108864
max_run_package_bytes = 536870912
failure_manifest_reserve_bytes = 16777216
max_reference_owned_peak_upper_bytes = 536870912
max_ascii_runtime_string_bytes = 256
max_ascii_reason_bytes = 96
max_source_path_bytes = 512
```

### 3.2 Role-specific source caps

The same numbers do not create a shared pool:

| Role | files | one file bytes | source-set bytes | declared dependencies |
| --- | ---: | ---: | ---: | ---: |
| `REFERENCE_SOURCE` | `256` | `16777216` | `67108864` | `256` |
| `PRODUCTION_SOURCE` | `256` | `16777216` | `67108864` | `256` |
| `COMPARISON_DRIVER` | `256` | `16777216` | `67108864` | `256` |

Unused capacity is nontransferable. Reference code is standard-library-only.
Production and comparison closures must bind every non-standard transitive
dependency through an included lockfile, wheel `RECORD`, or equivalent closed
distribution manifest. Unresolved or dynamically discovered code outside a frozen
set is an integrity failure.

Every source path is a normalized relative POSIX path. Its full grammar is:

```text
segment = [A-Za-z0-9._-]+ except exactly "." or ".."
path = segment ("/" segment)*
1 <= ASCII bytes(path) <= max_source_path_bytes
```

Thus a leading slash, trailing slash, empty segment (`//`), dot segment (`/./`),
parent segment (`/../`), NUL, backslash, Unicode, or separator alias is illegal.
Lexical regex acceptance alone is insufficient; the segment predicate is applied
after the regex and before filesystem access. Symlinks and realpath escape are
rejected.

### 3.3 Closed vocabularies

```text
profileId = m6-p1-reference-envelope-v1.1-revision6-proposal
canonicalizationVersion = selcal-m6-p1-jsonl-v1
calculationMode = ALL_STATE_EXACT | FINITE_B_COMPLETED_STATE_REPLAY
executionBranch = ALL_STATE_EXACT_COMPONENT
                | FINITE_NORMAL
                | FINITE_REPLICATE_FAILURE
                | FINITE_OBSERVED_ANALYTIC_FAILURE
                | NULL_BIND_DISABLED
artifactStatus = PROPOSAL_UNAPPROVED | APPROVED_FROZEN
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
diagnosticExecutionMode = INTERLEAVED_WITH_COMPARISON_DISCOVERY
terminalPartialDisposition = NOT_CREATED_BEFORE_FAILURE_ROOT
                           | DELETED_BEFORE_FAILURE_ROOT
                           | PRESERVED_VERIFIED_PARTIAL_EVIDENCE
                           | PRESERVED_UNVERIFIED_PARTIAL_EVIDENCE
```

The production-counter reason is null exactly for `AVAILABLE` and non-null exactly
for `NOT_EXPOSED`. Free exception text, hostnames, usernames, and environment
values are not canonical artifact fields.

## 4. Guarded integers and canonical bytes

### 4.1 Integer primitives

`OPERAND_MAX=2**max_operand_bits-1`. Boolean values are not integers here. Every
request integer, schema integer, loop bound, array length, index, `index+1`, byte
counter, numerator, denominator, and intermediate uses the following checked
operations before allocation or iteration:

```python
def require_uint(x):
    if type(x) is not int or x < 0 or x > OPERAND_MAX:
        fail("INVALID_OR_OVERSIZE_UNSIGNED_INTEGER")
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

def gsub(a, b):
    a, b = require_uint(a), require_uint(b)
    if b > a:
        fail("INVALID_UNSIGNED_SUBTRACTION")
    return a - b

def gpred0(a):
    a = require_uint(a)
    return 0 if a == 0 else gsub(a, 1)

def gceil(a, b):
    a, b = require_uint(a), require_uint(b)
    if b == 0:
        fail("ZERO_DIVISOR")
    q, r = divmod(a, b)
    return gadd(q, int(r != 0))

def decimal_digits(x):
    x = require_uint(x)
    if x == 0:
        return 1
    k = 0
    while x:
        x //= 10
        k = gadd(k, 1)
    return k
```

Bounded powers use exponentiation by squaring and stop at `cap`; exact factorial
or product recurrences stop before exceeding `max_exact_state_count+1`. No request
can cause a linear loop merely to discover that its exponent/result is too large.

### 4.2 Canonical scalar and container bytes

Canonical JSON uses UTF-8, sorted keys, separators `,` and `:`, no NaN/Infinity,
minimal nonnegative decimal integers, lowercase 64-hex hashes, finite binary64 as
`float.hex()` strings, no BOM/CRLF, and no trailing LF for JSON. Each JSONL row has
one LF. Encoding is incremental; whole-object `json.dumps` into a complete
`str`/`bytes` is forbidden.

Let `d(x)=decimal_digits(x)`:

```text
J(null)=4; J(false)=5; J(true)=4
J(uint[0..m])=d(m)
J(hash256)=66
J(floatHex)=26
J(safeAscii[k])=2+k
J(printableAscii[k])=2+6*k

J(array(item,0))=2
J(array(item,m>0))=2 + m*J(item) + (m-1)

J(object with k=0)=2
J(object with k>0)=2 + (k-1)
                    + sum(J(exactKey_i)+1+J(value_i), i=1..k)
```

The object formula is explicitly piecewise. It never evaluates `k-1` when `k=0`.
Optional fields are enumerated by legal co-presence branch. `$ref`, `oneOf`,
`allOf`, conditionals, and dependent constraints are resolved recursively. An
unbounded array/string/integer, open additional property, unresolved reference, or
nondecreasing recursion is `CANONICAL_BYTE_BOUND_HOLD`.

`ScalarComparisonValue` has only the v6 legal branches: null, Boolean, bounded
nonnegative integer, bounded finite-hex string, or bounded ASCII string. Its
integer branch has `minimum=0`; a negative value is schema-invalid and never
passed to `J(uint)`. Future mechanical verification must include:

```text
{}                         -> valid where an empty object is legal; exact bytes 2
-1                         -> invalid ScalarComparisonValue integer
-(2**max_operand_bits)     -> invalid before digit/byte calculation
```

These are required future verification cases, not tests executed by this proposal.

### 4.3 Field-specific integer domains

There is no generic digit shortcut. Each field uses its own maximum:

| Domain | Maximum |
| --- | ---: |
| sample/candidate/support count | `n / C / N` respectively |
| sample/candidate index | `gpred0(n) / gpred0(C)` |
| exact state count/index | `T / gpred0(T)` |
| finite replicate count/index | `B / gpred0(B)` |
| primary/comparison row index | `gpred0(L_admit) / gpred0(R_admit)` |
| diagnostic count/index | `D_admit / gpred0(D_admit)` |
| diagnostic row count/index | `Z_admit / gpred0(Z_admit)` |
| chunk index/row count | `999999 / max_chunk_rows` |
| byte offset | applicable ledger byte cap |
| byte length | recursively derived row upper |
| source ordinal/bytes/count/total | role-specific caps |
| dependency count | role-specific dependency cap |
| edge index/count | `gpred0(max_edge_entries) / max_edge_entries` |
| Counter component/count | `gpred0(bins) / N` |
| `E`, `F`, valid replicate count | `B` |
| planned denominator | `B+1` |
| artifact/package bytes | applicable artifact cap / `max_run_package_bytes` |

Zero has one digit. A null mode operand is excluded from a multi-mode maximum; the
static mode cap is used until the branch-specific value exists.

## 5. Branch counts and terminal-axis truth table

Symbols:

```text
n = common input length
h = greatest canonical candidate
N = n-h
C = candidate count
T = admitted exact labelled-state count
B = design replicate count
q = block-state payload length when applicable
W = q for block state, otherwise 1
Q = reference statistic scans
X = states independently generated or production-supplied states validated/replayed
L = retained primary state rows
R = comparison records
D = diagnostic groups
Z = diagnostic JSONL rows
H = 9*C+16
J = max_diagnostic_recomputations
G = max_disagreement_codes_per_record
```

The exact admission/execution vectors are:

| Mode/terminal | `Q_admit/Q_executed` | `X_admit/X_executed` | `L_admit/L_executed` | `R_admit/R_executed` | production state identities consumed |
| --- | --- | --- | --- | --- | ---: |
| exact complete or exact analytical failure | `T/T` | `T/T` | `T/T` | `(T+1)/(T+1)` | `0` |
| finite normal | `(B+1)/(B+1)` | `B/B` | `B/B` | `(B+2)/(B+2)` | `B` |
| finite replicate analytical failure | `(B+1)/(B+1)` | `B/B` | `B/B` | `(B+2)/(B+2)` | `B` |
| finite observed analytical failure | `(B+1)/1`, then tightened to `1/1` | `B/0`, then `0/0` | `B/0`, then `0/0` | `(B+2)/2`, then `2/2` | `0` |
| finite null disabled | `(B+1)/0`, then `0/0` | `B/0`, then `0/0` | `B/0`, then `0/0` | `(B+2)/1`, then `1/1` | `0` |
| exact null disabled | `max_exact_state_count/0`, then `0/0` | same | same | `(max_exact_state_count+1)/1`, then `1/1` | `0` |

For every non-null branch, `R_executed=Q_executed+1`. Null disablement has one
aggregate comparison record. Observed failure has `OBSERVED,AGGREGATE`. Completed
finite branches have `OBSERVED,B ordered STATE,AGGREGATE`. Exact has `T ordered
STATE,AGGREGATE`. Chunking is always by the stream's own row count:

```text
chunkCount(rows)=0 if rows=0 else gceil(rows,min(rows,max_chunk_rows))
```

Every chunk count is checked against `max_chunk_count_per_stream` before path
construction. Dynamic paths are six-digit zero-padded, normalized ASCII paths:

```text
state-chunks/state-NNNNNN.jsonl
comparison-chunks/comparison-NNNNNN.jsonl
diagnostic-chunks/diagnostic-NNNNNN.jsonl
```

The terminal-axis object is discriminator-coupled; axes are not independent enums:

```text
PC={COMPLETE,COMPLETE}
PN={COMPLETE,NULL_DISABLED}
PO={COMPLETE,OBSERVED_ANALYTICAL_FAILURE}
PR={COMPLETE,REPLICATE_FAILURE}
PE={COMPLETE,EXACT_ANALYTICAL_FAILURE}
D0={NONE,NOT_REQUIRED}
DC={COMPLETE,COMPLETE}
CA={COMPLETE,COMPLETE_AGREEMENT}
CD={COMPLETE,COMPLETE_DISAGREEMENT}
CN={COMPLETE,NOT_COMPARABLE}
```

| Success branch | Legal `(primary,diagnostic,comparison)` |
| --- | --- |
| null disabled | `(PN,D0,CN)` |
| observed analytical failure | `(PO,D0,CN)` |
| replicate analytical failure | `(PR,D0,CN)` |
| exact analytical failure | `(PE,D0,CN)` |
| complete agreement | `(PC,D0,CA)` |
| complete disagreement | `(PC,DC,CD)` |

For null/observed/replicate/exact analytical failure, every diagnostic operand and
manifest descriptor is null or zero according to its schema type; no diagnostic
header/group/file exists. Failure roots additionally discriminate failure class
`RESOURCE_LIMIT|INTEGRITY_FAILURE|INTERRUPTED` and stage
`PRIMARY|DIAGNOSTIC|COMPARISON|SUCCESS_ROOT_INSTALL`. Their custody can only
describe artifacts actually completed or the one current partial. No failure root
may claim agreement/disagreement, and no success root may contain PARTIAL custody.

## 6. Exact artifact graph and semantic cardinality

The only ordinary artifact nodes are:

```text
original-input.json
reference-spec.json
[finite, observed scan executed] observed-record.json
state-chunks/state-*.jsonl
exact-manifest.json OR finite-b-manifest.json
OR null-bind-disabled-manifest.json
comparison-chunks/comparison-*.jsonl
[complete disagreement diagnostics only]
  diagnostic-chunks/diagnostic-*.jsonl
  diagnostic-manifest.json
comparison-manifest.json                 # sole success root
OR
failure-manifest.json                    # sole failure root
  [at most one retained ordinary-node .partial adverse leaf]
```

There is no schedule/projection artifact, artifact index, success manifest,
predicted hash, or source-set sidecar. The three source-set identities are bounded
embedded objects. The failure reserve is transient quota, not an artifact.

Define branch predicates:

```text
hasObserved = 1 for finite normal, finite replicate failure, or observed failure;
              otherwise 0
hasStateChunks = 1 iff L>0
hasDiagnostics = 1 only for complete disagreement with D_completed>0
Kp=chunkCount(L); Kc=chunkCount(R); Kd=chunkCount(Z)
```

Success descriptor cardinality is derived before any schema maximum is applied:

```text
successDescriptorCount =
  2                                      # original + spec
  + hasObserved
  + Kp
  + 1                                    # primary manifest
  + Kc
  + hasDiagnostics*(Kd+1)                # chunks + diagnostic manifest
```

The success root itself is not one of its own descriptors. A failure stage derives
`completedDescriptorCount(stage,branch)` from the strict node order above, then:

```text
failureRetainedDescriptorCount =
  completedDescriptorCount(stage,branch)
  + preservedCurrentPartialIndicator
```

Only after deriving that semantic count may a recursive manifest byte extremum be
calculated. A generic maximum-sized descriptor array that ignores branch/stage
co-presence is forbidden. An UNVERIFIED partial has `sha256=null`; VERIFIED requires
an independently completed reread/hash. Empty partial deletion and nonempty
preservation use the four exact disposition literals from section 3.3.

## 7. Executable compute equations

Compute units are declared semantic operation counts, not wall time, CPU cycles,
total-process work, or byte I/O. Production-call internals are outside this
conditional reference/driver envelope and must be reported separately.

All equations are evaluated twice: once with branch admission operands and once
with monotone executed counters. In the equations below, suffix `a/e` means select
the admitted/executed value respectively.

### 7.1 Primary work

```text
nullBindWorkUnits_a = max_null_bind_work_units
nullBindWorkUnits_e = max_null_bind_work_units if bind check started else 0

stateGenerationUnits_a/e =
  X_a/e*W for exact mode; 0 for finite mode

stateIdentityValidationUnits_a/e =
  X_a/e*(2*W+4) for finite completed-replicate branches;
  X_a/e*(W+2) for exact mode;
  0 for null/observed-failure finite branches

stateApplicationUnits_a/e = X_a/e*n
transformValueVisits_a/e = X_a/e*n
candidateSupportVisits_a/e = Q_a/e*C*N
selectionWorkUnits_a = 3*Q_a*C
selectionWorkUnits_e = 3*successfulSelectionCount*C
```

Only the applicable statistic family contributes:

```text
Pearson:
  pearsonValueVisits_a/e = 6*Q_a/e*C*N
  every NetTE component = 0 or null as schema requires

NetTE:
  edgeEntries = 2*(bins+1)
  u3=min(bins**3,N); u2=min(bins**2,N); u1=min(bins,N)
  U=u3+2*u2+u1
  netteEdgeWorkUnits_a = 2*n+2*bins when Q_a>0 else 0
  netteEdgeWorkUnits_e = actually completed edge operations
  netteCodingValueVisits_a/e = 6*Q_a/e*C*N
  netteDirectionalSupportVisits_a/e = 6*Q_a/e*C*N
  netteCounterUpdateVisits_a/e = 8*Q_a/e*C*N
  netteSortUnits_a =
      2*Q_a*C*U*ceil_log2(max(U,1))
  netteSortUnits_e = guarded sum over actual directions/families of
      occupiedFamilyEntries*ceil_log2(max(occupiedFamilyEntries,1))
  netteCmiArithmeticUnits_a =
      2*Q_a*C*(15*U+3) + 2*Q_a*C
  netteCmiArithmeticUnits_e = guarded sum of
      15*occupiedJointCells + 3*completedDirections
      + 2*completedForwardReverseCandidatePairs
```

The 15 occupied-cell units cover four Counter lookups, four integer conversions,
two products, two divisions, one logarithm, one multiplication, and one summation
feed. The three direction-final units cover final summation, finite check, and
negative/clamp classification; the pair-final two cover subtraction and finite
check.

```text
primaryComputeWorkUnits_a/e = guarded sum of
  nullBind + stateGeneration + stateIdentityValidation + stateApplication
  + transform + support + applicable statistic components + selection
```

Each component and parent is checked against its named cap. Null/observed-failure
execution uses its tightened vector from section 5, so no `B` replay work is
reported as executed.

### 7.2 Comparison work

Let `candidateBearingRows=Q`, and let actual array lengths be read from each
completed comparison record:

```text
comparisonComputeWorkUnits_a =
    Q_a*C                         # candidate-record comparisons
  + L_a*(W+4)                     # state/identity/order comparisons
  + R_a*H                         # field-comparison upper
  + R_a*G                         # disagreement-code upper
  + R_a                           # locator/status checks

comparisonComputeWorkUnits_e = guarded sum over emitted records of
  candidateRecordsCompared
  + stateComponentsCompared
  + fieldComparisonsPerformed
  + disagreementCodesEmitted
  + locatorStatusChecks
```

Array contracts remain `candidateRecords=C` for observed/state and zero for
aggregate; `tiedCandidateIndices<=C`; `fieldComparisons<=9*C+16`;
`diagnosticIndices<=256`; `disagreementCodes<=32`.

### 7.3 Diagnostic replay work

Diagnostics are synchronous at comparison discovery with
`max_pending_diagnostic_jobs=0`. Each diagnostic targets one disputed comparison
record and may replay at most one full candidate scan; no unbounded queue or later
reconstruction is permitted.

For admission, one diagnostic replay uses the conservative state-row case
`x_d=1`, `q_d=1`; executed counters use `x_d=0` for an observed row and record
partial work if a group fails:

```text
diagnosticReplayStatisticScans_a = D_a
diagnosticReplayStatisticScans_e = completed/started replay scans
diagnosticReplayStateApplicationUnits_a = D_a*n
diagnosticReplayStateApplicationUnits_e = sum(x_d*n)
diagnosticReplayTransformValueVisits_a = D_a*n
diagnosticReplayTransformValueVisits_e = sum(x_d*n)
diagnosticReplayCandidateSupportVisits_a = D_a*C*N
diagnosticReplayCandidateSupportVisits_e = sum(q_d*C*N)

Pearson diagnostic:
  diagnosticReplayPearsonValueVisits_a = 6*D_a*C*N
  diagnosticReplayPearsonValueVisits_e = sum(6*q_d*C*N)

NetTE diagnostic:
  diagnosticReplayNetteEdgeWorkUnits_a = D_a*(2*n+2*bins)
  diagnosticReplayNetteCodingValueVisits_a = 6*D_a*C*N
  diagnosticReplayNetteDirectionalSupportVisits_a = 6*D_a*C*N
  diagnosticReplayNetteCounterUpdateVisits_a = 8*D_a*C*N
  diagnosticReplayNetteSortUnits_a =
      2*D_a*C*U*ceil_log2(max(U,1))
  diagnosticReplayNetteCmiArithmeticUnits_a =
      2*D_a*C*(15*U+3)+2*D_a*C
```

Every NetTE diagnostic executed field is the same guarded actual-family sum as
section 7.1, restricted to the replayed diagnostic scans. Admission additionally
charges diagnostic emission/validation:

```text
diagnosticRecordWork_a = D_a*(edgeEntries+2*n+4*U
                              +max_numerical_rows_per_diagnostic+2)
diagnosticRecordWork_e = exact emitted header/body/footer scalar-row operations
diagnosticReplaySelectionWorkUnits_a = 3*D_a*C
diagnosticReplaySelectionWorkUnits_e = 3*successfulDiagnosticSelections*C

diagnosticComputeWorkUnits_a/e = guarded sum of all applicable
  diagnosticReplay* fields + diagnosticRecordWork_a/e
```

If no disagreement diagnostics are legal, `D_a=D_started=D_completed=Z_a=Z_e=0`
after terminal tightening, execution mode/reason fields are null as prescribed,
and all diagnostic replay fields are zero or null. A failure root retains the
executed partial counters rather than rounding them to a completed group.

```text
totalComputeWorkUnits_a/e =
  primaryComputeWorkUnits_a/e
  + comparisonComputeWorkUnits_a/e
  + diagnosticComputeWorkUnits_a/e
```

## 8. Executable canonical-byte, package, and I/O equations

### 8.1 Recursive row and manifest bytes

Apply section 4's `J(node)` to every resolved v6 schema branch. Required dynamic
integer/hash domains include all candidate/state/selection fields, every descriptor
integer (`chunkIndex,firstIndex,lastIndex,rowCount,bytes`), every row locator, all
diagnostic indices and four Counter-key shapes, source-set ordinals/counts/bytes,
every derived operand below, and every failure partial counter. Hash fields cost 66
bytes only when non-null.

Record-kind byte sums, never a generic maximum-row multiplier, are:

```text
PrimaryRowsUpper_exact = T*ExactStateRowUpper
PrimaryRowsUpper_finite_completed = B*FiniteStateRowUpper
PrimaryRowsUpper_observed_failure = 0
PrimaryRowsUpper_null = 0

ComparisonRowsUpper_exact = T*ComparisonStateRowUpper
                            +ComparisonExactAggregateUpper
ComparisonRowsUpper_finite_completed = ComparisonObservedUpper
                            +B*ComparisonStateRowUpper
                            +ComparisonFiniteAggregateUpper
ComparisonRowsUpper_observed_failure = ComparisonObservedUpper
                            +ComparisonFiniteAggregateUpper
ComparisonRowsUpper_null = ComparisonNullAggregateUpper
```

Diagnostic rows are streamed as HEADER, scalar EDGE/CODE/COUNTER/NUMERICAL body
rows, FOOTER. Reference Counters include both directions. Production Counter rows
exist in both directions only for `productionCountersStatus=AVAILABLE`.

```text
edgeEntries=2*(bins+1)
DiagnosticBodyRowsOneUpper = edgeEntries+2*n+4*U
                              +max_numerical_rows_per_diagnostic
DiagnosticRowsOneUpper = DiagnosticBodyRowsOneUpper+2
Z_admit = D_admit*DiagnosticRowsOneUpper
DiagnosticRowsBytesUpper = D_admit*DiagnosticGroupBytesUpper
```

Both row count and recursive byte upper must independently fit their caps.
`DIAGNOSTIC_ROW_INDEX` is the locator domain; primary/comparison digits may not be
substituted.

### 8.2 Success and failure package uppers

Let `O,S,V,P,Cmp,Diag,Root` be the recursive byte uppers for original input,
reference spec, optional observed record, completed primary family, comparison
chunks, optional diagnostic chunks+manifest, and comparison manifest. State chunks
are included in `P`. Then:

```text
successPackageUpper(branch,result) =
  O+S + hasObserved*V + P(branch) + Cmp(branch)
  + hasDiagnostics(result)*Diag(branch) + Root(branch,result)
```

This contains no schedule/projection-file term. The production projection carried
inside each comparison row is already charged by that record's recursive upper.

For a failure at a particular stage, let `Completed(stage,branch)` be the sum of
only fully closed, reread, verified legal predecessors in section 6. Let
`NextPartialUpper(stage,branch)` be the recursive upper of the single legal node
whose serial writer was active, or zero if none. Then:

```text
preservedPartialUpper =
  NextPartialUpper when disposition is either PRESERVED_*; otherwise 0

failureManifestUpper = J(the exact failure-class/stage branch with
  failureRetainedDescriptorCount descriptors)

failurePackageUpper(stage,branch) =
  Completed(stage,branch)+preservedPartialUpper+failureManifestUpper

finalRetainedPackageUpper =
  successPackageUpper for a success root;
  failurePackageUpper for a failure root

runDirectoryTransientUpper =
  finalRetainedPackageUpper+failure_manifest_reserve_bytes
  + currentWriterPartialUpperNotAlreadyRetained
```

The reserve is a no-payload quota/space reservation and vanishes only after one
verified terminal root. A platform that reserves space by writing payload bytes is
outside this profile until those writes are charged.

### 8.3 I/O visits

For each completed ordinary file of `b` bytes, write plus independent verification
reread costs `2*b`. Source-set identity reads each included source file exactly
once; a lock/`RECORD` is already an entry and is not double-counted. Primary rows
are reread once for comparison after their chunks close, so their normal cost is
three visits: write, verification read, comparison read.

For admission/execution suffix `a/e`:

```text
inputSidecarBytesWritten_a/e
inputSidecarBytesReadForVerification_a/e
sourceBytesReadForIdentity_a/e
primaryBytesWritten_a/e
primaryBytesReadForVerification_a/e
primaryBytesReadForComparison_a/e
comparisonBytesWritten_a/e
comparisonBytesReadForVerification_a/e
diagnosticBytesWritten_a/e
diagnosticBytesReadForVerification_a/e
```

`comparison-manifest.json` is written through its `.partial`. Success charges the
exact partial write and one complete verification reread before atomic rename:

```text
comparisonManifestPartialBytesWritten_a/e
comparisonManifestPartialBytesReadForVerification_a/e
```

If installation fails, actual fields retain writer-observed bytes and bytes reread
before verification failure. A nonempty partial is preserved; zero-byte deletion
requires a read-only size check. VERIFIED requires full reread/hash; UNVERIFIED has
`sha256=null` and `bytes` equal to the writer-observed count or null.

The failure root uses:

```text
failureManifestBytesWritten_a/e
failureManifestBytesReadForVerification_a/e
partialBytesWritten
partialBytesReadForVerification
terminalPartialDisposition
```

The first two fields charge the failure-manifest writer and full reread. The generic
partial counters identify the interrupted ordinary-node writer; when that node is
the comparison manifest, they equal the corresponding comparison-manifest partial
executed counters rather than being added a second time.

```text
totalIoByteVisits_a/e = guarded sum of every applicable, nonduplicated field above
```

Admission uses the maximum legal success/failure path after semantic cardinality;
execution uses monotone observed counters and fails before the next operation would
exceed `totalIoByteVisits_a`. Metadata operations are recorded separately as
`fsyncCallsExecuted`, `atomicRenamesExecuted`, and
`directoryFsyncCallsExecuted`; they carry zero byte-visit charge.

## 9. Phase-specific incremental memory proof

This is an incremental reference/comparison-driver allocation bound. It explicitly
excludes production-call internals and the memory of the returned production object;
therefore it is not a process-RSS, system, or production memory bound. The public
result remains owned by production; the driver projects one replicate at a time.
That exclusion must be persisted, not hidden in prose.

### 9.1 Runtime-layout constants

```text
CONTAINER_BASE_PEAK_BYTES=512
FLOAT_VALUE_PEAK_BYTES=64
INTEGER_VALUE_PEAK_BYTES=64
RECORD_BASE_PEAK_BYTES=512
CANDIDATE_RECORD_PEAK_BYTES=2048
SELECTION_RECORD_PEAK_BYTES=4096
FIELD_COMPARISON_PEAK_BYTES=1024
FAILURE_CODE_VALUE_PEAK_BYTES=128
COUNTER_ENTRY_PEAK_BYTES=512
SORT_ENTRY_PEAK_BYTES=64
SOURCE_ENTRY_PEAK_BYTES=1024
DEPENDENCY_POLICY_PEAK_BYTES=1024
CHUNK_DESCRIPTOR_PEAK_BYTES=1024
FAILURE_DESCRIPTOR_PEAK_BYTES=1024
ENCODER_FRAME_PEAK_BYTES=4096
MAX_CANONICAL_TOKEN_BYTES=4096
STREAM_WRITE_BUFFER_BYTES=1048576
STREAM_READ_BUFFER_BYTES=1048576
HASH_SCRATCH_BYTES=65536
DECODER_SCRATCH_BYTES=262144
FIXED_PHASE_OVERHEAD_BYTES=8388608
```

A postapproval runtime-layout probe must validate these constants for the exact
interpreter/runtime identity before a scientific scan.

### 9.2 Executable phase function

For phase record `p`, every multiplication/addition is guarded:

```text
MemoryUpper(p) = FIXED_PHASE_OVERHEAD_BYTES
  + p.floatValues*FLOAT_VALUE_PEAK_BYTES
  + p.integerValues*INTEGER_VALUE_PEAK_BYTES
  + p.candidateRecords*CANDIDATE_RECORD_PEAK_BYTES
  + p.selectionRecords*SELECTION_RECORD_PEAK_BYTES
  + p.fieldComparisons*FIELD_COMPARISON_PEAK_BYTES
  + p.failureCodes*FAILURE_CODE_VALUE_PEAK_BYTES
  + p.counterEntries*COUNTER_ENTRY_PEAK_BYTES
  + p.sortEntries*SORT_ENTRY_PEAK_BYTES
  + p.sourceEntries*SOURCE_ENTRY_PEAK_BYTES
  + p.dependencyPolicyObjects*DEPENDENCY_POLICY_PEAK_BYTES
  + p.chunkDescriptors*CHUNK_DESCRIPTOR_PEAK_BYTES
  + p.failureDescriptors*FAILURE_DESCRIPTOR_PEAK_BYTES
  + p.encoderFrames*ENCODER_FRAME_PEAK_BYTES
  + p.streamWriteBuffers*STREAM_WRITE_BUFFER_BYTES
  + p.streamReadBuffers*STREAM_READ_BUFFER_BYTES
  + p.hashScratchBuffers*HASH_SCRATCH_BYTES
  + p.decoderScratchBuffers*DECODER_SCRATCH_BYTES
  + p.incrementalEncoderBytesUpper
  + p.containerCount*CONTAINER_BASE_PEAK_BYTES
```

`incrementalEncoderBytesUpper <= encoderFrames*MAX_CANONICAL_TOKEN_BYTES`.
Whole-row/manifest strings and bytes are forbidden.

### 9.3 Phase primitive-count uppers

Let `Sfiles` be the sum of the three role-specific source counts and `K=Kp+Kc+Kd`.
The table lists simultaneous maxima; absent quantities are zero:

| Phase | floats | integers | candidates | selection | fields/codes | counters/sort | source/policy | descriptors | buffers/scratch |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: | --- |
| `admission` | `2*n` | `C+64` | `0` | `0` | `0/0` | `0/0` | `0/0` | `0` | encoder `1`, hash `0`, decoder `1` |
| `sourceIdentity` | `2*n` | `C+Sfiles+64` | `0` | `0` | `0/0` | `0/0` | `Sfiles/1` | `0` | read `1`, hash `1`, decoder `1` |
| `productionProjection` | `2*n+C` | `W+C+64` | `C` | `1` | `0/G` | `0/0` | `0/0` | `0` | encoder `1`, decoder `1` |
| `referenceReplay` | `3*n+C` | `W+C+64` | `C` | `1` | `0/G` | `0/0` | `0/0` | `1` | write `1`, read `1`, hash `1`, decoder `1` |
| `nette` | `3*n+2*(bins+1)+C` | `W+6*N+C+64` | `C` | `1` | `0/G` | `U/U` | `0/0` | `1` | write `1`, hash `1`, decoder `1` |
| `comparisonDiagnostic` | `3*n+2*(bins+1)+2*C` | `W+6*N+C+Z+64` | `2*C` | `2` | `H/G` | `U/U` | `0/0` | `2` | write `2`, read `1`, hash `1`, decoder `1` |
| `manifest` | `2*n` | `C+Sfiles+K+128` | `0` | `0` | `0/0` | `0/0` | `Sfiles/3` | `successDescriptorCount` | write `1`, read `1`, hash `1`, decoder `1` |
| `failure` | `2*n` | `C+failureRetainedDescriptorCount+128` | `0` | `0` | `0/0` | `0/0` | `0/0` | `failureRetainedDescriptorCount` | write `1`, read `1`, hash `1`, decoder `1` |

For a non-NetTE phase, the edge/code/Counter terms are zero. `containerCount` is
the sum of the explicitly nonzero record/array/source/descriptor/buffer groups in
that row plus a fixed 32 control containers; it is persisted rather than inferred
from host heap sampling. In the `manifest` row, the descriptor column means
`chunkDescriptors=successDescriptorCount` and `failureDescriptors=0`; the
post-binding size verifier must show the selected per-entry layout constant covers
every ordinary descriptor kind, not only chunks. In the `failure` row it means
`chunkDescriptors=0` and
`failureDescriptors=failureRetainedDescriptorCount`. In the replay/NetTE/
comparison rows it is the stated number of active ordinary descriptors with
`failureDescriptors=0`; all earlier phases use zero for both. The maximum, not the
sum of mutually exclusive phases, is:

```text
referenceOwnedPeakUpperBytes=max(MemoryUpper(each of eight phases))
peakPhase=first phase in the fixed table order attaining that maximum
```

Admission fails before production execution if any primitive-count guard, phase
upper, or peak upper exceeds its cap. Observed heap/RSS may be reported separately
but cannot replace this static proof.

### 9.4 Persisted memory proof

`MemoryProofOperands` contains:

```text
scope=INCREMENTAL_REFERENCE_AND_DRIVER_ALLOCATION_ONLY
productionCallAndReturnedObjectStatus=EXCLUDED_NOT_BOUNDED
runtimeLayoutProfileId
phases{admission,sourceIdentity,productionProjection,referenceReplay,
       nette,comparisonDiagnostic,manifest,failure}
  each PhaseMemoryOperands contains every primitive count in MemoryUpper,
  incrementalEncoderBytesUpper,containerCount,phaseUpperBytes
referenceOwnedPeakUpperBytes
peakPhase
wholeObjectSerializationAllowed=false
```

The exact production-memory exclusion prevents this conditional proof from being
misreported as a total-process guarantee.

## 10. Complete derived-resource projection

The companion v6 schema must persist all operands needed to reproduce admission
and observed accounting. Inapplicable metric fields are null; applicable work that
executed zero times is zero. Required top-level scientific fields are:

```text
n,h,N,C,T,B,bins,blockCount,WState,U
QAdmit,QExecuted,XAdmit,XExecuted,LAdmit,LExecuted,RAdmit,RExecuted
DAdmit,DStarted,DCompleted,ZAdmit,ZExecuted,H,J,G,M
executionBranch,package,comparison,diagnostic,compute,io,memory
```

The closed `ComputeOperands` field set is:

```text
nullBindWorkUnitsAdmit,nullBindWorkUnitsExecuted
stateGenerationUnitsAdmit,stateGenerationUnitsExecuted
stateIdentityValidationUnitsAdmit,stateIdentityValidationUnitsExecuted
stateApplicationUnitsAdmit,stateApplicationUnitsExecuted
transformValueVisitsAdmit,transformValueVisitsExecuted
candidateSupportVisitsAdmit,candidateSupportVisitsExecuted
pearsonValueVisitsAdmit,pearsonValueVisitsExecuted
netteEdgeWorkUnitsAdmit,netteEdgeWorkUnitsExecuted
netteCodingValueVisitsAdmit,netteCodingValueVisitsExecuted
netteDirectionalSupportVisitsAdmit,netteDirectionalSupportVisitsExecuted
netteCounterUpdateVisitsAdmit,netteCounterUpdateVisitsExecuted
netteSortUnitsAdmit,netteSortUnitsExecuted
netteCmiArithmeticUnitsAdmit,netteCmiArithmeticUnitsExecuted
selectionWorkUnitsAdmit,selectionWorkUnitsExecuted
comparisonComputeWorkUnitsAdmit,comparisonComputeWorkUnitsExecuted
diagnosticReplayStatisticScansAdmit,diagnosticReplayStatisticScansExecuted
diagnosticReplayStateApplicationUnitsAdmit,
  diagnosticReplayStateApplicationUnitsExecuted
diagnosticReplayTransformValueVisitsAdmit,
  diagnosticReplayTransformValueVisitsExecuted
diagnosticReplayCandidateSupportVisitsAdmit,
  diagnosticReplayCandidateSupportVisitsExecuted
diagnosticReplayPearsonValueVisitsAdmit,
  diagnosticReplayPearsonValueVisitsExecuted
diagnosticReplayNetteEdgeWorkUnitsAdmit,
  diagnosticReplayNetteEdgeWorkUnitsExecuted
diagnosticReplayNetteCodingValueVisitsAdmit,
  diagnosticReplayNetteCodingValueVisitsExecuted
diagnosticReplayNetteDirectionalSupportVisitsAdmit,
  diagnosticReplayNetteDirectionalSupportVisitsExecuted
diagnosticReplayNetteCounterUpdateVisitsAdmit,
  diagnosticReplayNetteCounterUpdateVisitsExecuted
diagnosticReplayNetteSortUnitsAdmit,diagnosticReplayNetteSortUnitsExecuted
diagnosticReplayNetteCmiArithmeticUnitsAdmit,
  diagnosticReplayNetteCmiArithmeticUnitsExecuted
diagnosticReplaySelectionWorkUnitsAdmit,
  diagnosticReplaySelectionWorkUnitsExecuted
diagnosticComputeWorkUnitsAdmit,diagnosticComputeWorkUnitsExecuted
primaryComputeWorkUnitsAdmit,primaryComputeWorkUnitsExecuted
totalComputeWorkUnitsAdmit,totalComputeWorkUnitsExecuted
```

The closed `IoOperands` field set is:

```text
inputSidecarBytesWrittenAdmit,inputSidecarBytesWrittenExecuted
inputSidecarBytesReadForVerificationAdmit,
  inputSidecarBytesReadForVerificationExecuted
sourceBytesReadForIdentityAdmit,sourceBytesReadForIdentityExecuted
primaryBytesWrittenAdmit,primaryBytesWrittenExecuted
primaryBytesReadForVerificationAdmit,primaryBytesReadForVerificationExecuted
primaryBytesReadForComparisonAdmit,primaryBytesReadForComparisonExecuted
comparisonBytesWrittenAdmit,comparisonBytesWrittenExecuted
comparisonBytesReadForVerificationAdmit,
  comparisonBytesReadForVerificationExecuted
diagnosticBytesWrittenAdmit,diagnosticBytesWrittenExecuted
diagnosticBytesReadForVerificationAdmit,
  diagnosticBytesReadForVerificationExecuted
comparisonManifestPartialBytesWrittenAdmit,
  comparisonManifestPartialBytesWrittenExecuted
comparisonManifestPartialBytesReadForVerificationAdmit,
  comparisonManifestPartialBytesReadForVerificationExecuted
failureManifestBytesWrittenAdmit,failureManifestBytesWrittenExecuted
failureManifestBytesReadForVerificationAdmit,
  failureManifestBytesReadForVerificationExecuted
totalIoByteVisitsAdmit,totalIoByteVisitsExecuted
fsyncCallsExecuted,atomicRenamesExecuted,directoryFsyncCallsExecuted
```

The closed `ComparisonOperands` and `DiagnosticOperands` fields are:

```text
ComparisonOperands = {
  RAdmit,RExecuted,exactRecordCountExpected,finiteRecordCountExpected,
  nullBindRecordCountExpected,candidateRecordsMax,tiedCandidateIndicesMax,
  fieldComparisonsMax,diagnosticIndicesMax,disagreementCodesMax,
  comparisonChunkCount,comparisonLedgerBytesUpper,
  comparisonLedgerBytesObserved
}
DiagnosticOperands = {
  executionMode,maxPendingDiagnosticJobs,U,edgeEntries,
  DAdmit,DStarted,DCompleted,ZAdmit,ZExecuted,diagnosticChunkCount,
  diagnosticRowsOneUpper,diagnosticRecordCountObserved,
  diagnosticLedgerBytesUpper,diagnosticLedgerBytesObserved,
  productionCountersStatus,productionCountersNotExposedReason
}
```

`MemoryProofOperands` and each `PhaseMemoryOperands` are exactly section 9.4,
including `containerCount`. The closed package object is:

```text
artifactCountUpper
inputSidecarFormulaUpper,inputSidecarBytesObserved
primaryRowsBytesUpper,primaryManifestBytesUpper
comparisonRowsBytesUpper,diagnosticRowsBytesUpper
diagnosticManifestBytesUpper,terminalRootBytesUpper
successPackageUpper,failurePackageUpper,finalRetainedPackageUpper
finalRetainedPackageBytesObserved
failureManifestReserveBytes,runDirectoryTransientUpper
retainedDescriptorCountUpper,retainedDescriptorCountObserved
```

`partialBytesWritten`, `partialBytesReadForVerification`, and
`terminalPartialDisposition` are persisted in the applicable failure-root custody
branch, not duplicated in `PackageOperands`.

No field with `Schedule`, `PlannedSchedule`, or state-projection-file semantics is
permitted. `plannedDenominator={source:DESIGN_CONSTANT,value:B+1}` remains a
scientific denominator declaration in finite primary manifests; it is not an
artifact or evidence that a replicate executed.

## 11. Source-set identity and dependency closure

`implementationSourceSets` has exactly three embedded objects, one per role. Each
has sorted normalized entries `{ordinal,path,mediaType,bytes,sha256}`, count, total
bytes, transitive dependency policy, artifact status, and `sourceSetId`.
`sourceSetId` is SHA-256 of the canonical projection with only `sourceSetId`
omitted; no object hashes itself.

Admission independently verifies per role:

```text
sourceCount == len(entries) <= role file cap
ordinals == 0..sourceCount-1
paths satisfy normalized-segment grammar and ASCII lexical order
each bytes <= role one-file cap
totalSourceBytes == guarded sum(entry.bytes) <= role set cap
declaredDependencyCount <= role dependency cap
unresolvedDependencyCount == 0
dependencyManifestSha256 points to exactly one included closure entry when closed
```

The closure begins at every executed role entrypoint and recursively includes
owned imports, initializers, and behavior-affecting data. Instrumented imports
after execution must be a subset of the frozen closure. A commit/version/root-file
hash alone is not a source-set identity.

## 12. Mandatory future mechanical verification

Before approval, a standard-library-only verifier must use the exact v6 formula,
schema, and budget-profile bytes to:

1. enumerate every `oneOf`/conditional branch and legal field co-presence set;
2. generate and schema-validate canonical minimum and maximum instances for every
   object, row, manifest, source policy, Counter key, terminal triple, VERIFIED/
   UNVERIFIED descriptor, and three media types;
3. include an empty legal object and assert exact canonical bytes `2`;
4. try `-1` and a huge negative `-(2**max_operand_bits)` in every nonnegative
   integer union, including `ScalarComparisonValue`, and require schema rejection
   before byte calculation;
5. mutate every bounded integer/string/array/path segment to its maximum and one
   step beyond, including `//`, `/./`, `/../`, leading slash, and trailing slash;
6. compare measured incremental bytes with the recursive upper;
7. recompute every branch count, descriptor cardinality, compute field, I/O field,
   phase memory field, package upper, and terminal-axis triple;
8. assert no schema property or formula operand contains schedule/projection-file
   vocabulary;
9. output a read-only report binding formula/schema/profile hashes and every
   adverse/min/max result.

This plan has not been implemented or run. Until it passes independently,
`CANONICAL_BOUND_AND_RESOURCE_BINDING_HOLD` remains open.

## 13. Deterministic external binding and claim ceiling

No formula, schema, profile, manifest, or approval object includes its own digest.
The external approved projection, if later authorized, binds exact formula and
schema paths/bytes/SHA-256, canonical budget projection/SHA-256, stable binding ID,
approver ID, UTC approval time, and
`disposition=APPROVED_FOR_M6_P1_IMPLEMENTATION`. Proposal artifacts use
`artifactStatus=PROPOSAL_UNAPPROVED`; only an exact external binding may permit
`APPROVED_FROZEN`. Either value without the other is an integrity failure.

```text
formulaPath=docs/benchmarks/2026-09-08-m6-p1-resource-envelope-v1_1-revision6-formulas.md
schemaPath=docs/benchmarks/schemas/m6-p1-artifact-contract-v6-proposal.schema.json
profileId=m6-p1-reference-envelope-v1.1-revision6-proposal
```

Current status is exactly:

```text
formulaStatus=REVISION6_PROPOSAL_WRITTEN
schemaStatus=PROVISIONAL_NOT_BOUND
budgetProfileStatus=PROPOSED_NOT_APPROVED
externalApprovalStatus=ABSENT
implementationStatus=NOT_AUTHORIZED
verificationStatus=NOT_EXECUTED
M6Status=NOT_EXECUTED
SoftwareXReadiness=UNCHANGED_HOLD
```

The maximum supportable future claim remains narrow: within admitted fixtures and
the explicitly bound runtime/source identities, an independent implementation can
replay production-emitted completed finite states or a complete admitted exact
state universe and compare retained public outputs. It cannot establish production
RNG correctness, distributional validity, cross-runtime equivalence, total-process
resource bounds, external validation, release readiness, or publication readiness.

## 14. Integrated-review repair matrix

“Addressed” means present in this unapproved proposal, not reviewer acceptance.

| Finding | Revision-6 repair |
| --- | --- |
| `C1` empty-object formula and signed integer | section 4.2 makes object bytes piecewise, constrains scalar integers to nonnegative, and mandates `{}`/negative/huge-negative future cases |
| `C2` scientific scope drifted to independent RNG plan | sections 2, 5, 6, 8, and 10 remove all schedule artifacts and conditionally replay completed production state identities only |
| `C3` axes/diagnostic null were under-specified | section 5 gives six branch-specific success triples and forces null diagnostics for every NOT_COMPARABLE analytical terminal |
| `C4` resource formulas were not executable/persisted | sections 7--10 give admitted/executed compute, explicit diagnostic replay, byte-I/O/partial/failure equations, eight memory phases, and persisted proof fields |
| `I1` source-role/path boundaries | sections 3.2 and 11 keep independent role caps and reject empty/dot/parent/alias path segments |
| `I2` descriptor maxima preceded semantics | section 6 derives branch/stage descriptor cardinality before recursive extrema |

## 15. Self-audit

- revision 5 is preserved; this is a new file;
- no schedule or state-projection file exists in the artifact graph or resource
  equations;
- null/observed failure executes no state replay; completed finite replay is
  conditional on ordered production-emitted identities;
- object bytes handle `k=0` without unsigned underflow;
- every executable arithmetic operation is guarded and every loop is bounded;
- exact/finite counts give `R=T+1`, `R=B+2`, observed failure `R=2`, null `R=1`;
- exact adverse terminal axes remain distinct; diagnostic null is branch-forced;
- compute, I/O, memory, partial custody, and package bytes remain separate axes;
- semantic descriptor cardinality precedes byte maximization;
- role-specific source capacities are nontransferable and paths are normalized;
- failure reserve is transient and one terminal root is exclusive;
- no approval, implementation, test, execution, M6 completion, or SoftwareX
  readiness is claimed.
