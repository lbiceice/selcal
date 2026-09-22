# M6-P1 resource envelope v1.1 revision 7 formula attachment

> **Status:** `PROPOSAL / NOT APPROVED / NOT FROZEN / PROVISIONAL SCHEMA BINDING / NOT IMPLEMENTATION AUTHORITY / M6 NOT EXECUTED`

> **Purpose:** Repair the independent integrated revision-6 formula/schema review without
> changing SelCal's statistic, selector, null semantics, tail rule, or tolerance.
> Revision 7 restores the parent scientific scope: finite reference work replays
> only the ordered state identities already emitted by a completed production
> result. It neither generates nor validates a production RNG schedule.

## 1. Authority and replacement boundary

Revision 7 is a new proposal. Revision 6 remains an adverse predecessor and is
not edited:

| Item | Bytes | SHA-256 | Status here |
| --- | ---: | --- | --- |
| Parent design, `2026-09-06-m6-p1-independent-reference-design.md` | `34234` | `ab6e40cc57eb5e4272451ebcb227eab45bf45f1ca66795530adb8d9957490064` | surviving scientific scope |
| Revision-6 formula | `50363` | `2b0bd1085a22dbb0b315c5c69cbbfc279f363877967303dccd2ac179058fca26` | preserved adverse predecessor |
| Revision-6 schema | `318128` | `6137f391e557adcd1d84dd85a5b581d4632efba90d9a0041ce83af38de89be58` | preserved adverse predecessor |
| Revision-7 companion schema | `394750` | `6e5123b3edfb80df0738f758f8cc06138347b6c7129e85706c7b885e75e12be9` | exact proposal bytes bound here; not approved |

This attachment binds the exact companion v7 schema bytes above. The formula
attachment, deterministic budget projection, and any future external approval
record remain separately non-self-hashing objects. This document does not approve
any of them.

Only after that approval may revision 7 replace the parent's retained-state,
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
profileId = m6-p1-reference-envelope-v1.1-revision7-proposal
canonicalizationVersion = selcal-m6-p1-jsonl-v1
calculationMode = ALL_STATE_EXACT | FINITE_B_COMPLETED_STATE_REPLAY
executionBranch = ALL_STATE_EXACT_COMPONENT
                | FINITE_NORMAL
                | FINITE_REPLICATE_FAILURE
                | FINITE_OBSERVED_ANALYTIC_FAILURE
                | NULL_BIND_DISABLED
                | FINITE_BRANCH_UNRESOLVED   # failure before public return only
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
unbounded array/string/integer, open additional property, unresolved reference,
or non-terminating/non-monotone size recurrence is `CANONICAL_BYTE_BOUND_HOLD`.

Comparison scalar values have only the v7 legal branches: null, Boolean, bounded
nonnegative integer, bounded finite-hex string, or bounded ASCII string. Its
integer branch has `minimum=0`; a negative value is schema-invalid and never
passed to `J(uint)`. Future mechanical verification must include:

```text
{}                         -> valid where an empty object is legal; exact bytes 2
-1                         -> invalid comparison-scalar integer
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
blockCount = q
WState = W
M = max(1,n,h,N,C, T if known, B if known, bins if known)
```

The known-set operation for M excludes a mode-inapplicable null; it never replaces
a field-specific digit domain. q/blockCount are null for circular shift and equal
the guarded block count for block shuffle. W/WState equal q for a block state and
1 for a circular state. A finite branch before the public return uses
executionBranch=FINITE_BRANCH_UNRESOLVED and static worst-case admission operands;
it may not be mislabeled FINITE_NORMAL.

Diagnostic admission is deterministic:

~~~text
DAdmit =
  0, for NULL_BIND_DISABLED or a resolved analytically unevaluable primary;
  min(J,RAdmit), otherwise.
DStarted increments immediately before a diagnostic HEADER attempt.
DCompleted increments only after the matching FOOTER is closed and verified.
Before starting a disagreement group when DStarted=J, fail RESOURCE_LIMIT;
the J+1 group is not started and its comparison record is not emitted.
ZAdmit is the exact sum of the admitted nine diagnostic row-kind multiplicities.
ZExecuted is the exact sum of emitted row-kind multiplicities, including a
started partial group; 0<=DCompleted<=DStarted<=DAdmit<=J.
~~~

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
RESOURCE_LIMIT|INTEGRITY_FAILURE|INTERRUPTED and the closed failedStage set
PREFLIGHT|SOURCE_IDENTITY|SIDECAR_WRITE|NULL_BIND|PRODUCTION_CALL|
OBSERVED_SCAN|STATE_SCAN|PRIMARY_FINALIZE|COMPARISON|DIAGNOSTIC|
SUCCESS_ROOT_INSTALL. Their custody can only
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


### 7.4 Scientific comparison and aggregate closure

FieldComparison is a discriminator union, not a bag of optional scalars:

| comparisonRule | reference/production | residual | tolerance | matches |
| --- | --- | --- | --- | --- |
| FLOAT_ABS_TOL | canonical FloatHex / FloatHex | canonical FloatHex of production-reference | exactly 0x1.0000000000000p-46 | abs(decoded residual)<=decoded tolerance |
| FLOAT_HEX_EXACT | canonical FloatHex / FloatHex | null | null | strings equal |
| TAIL_EXACT | each boolean or null | null | null | same validity and exact value |
| EXACT | same scalar domain: nonnegative integer, boolean, safe ASCII, or both null | null | null | type and value equal |

Bogus strings, cross-domain exact pairs, a tail tolerance, and a boolean/null
FLOAT_ABS_TOL value are structurally invalid. The fixed absolute budget is the
parent design's proposed 64*ulp(1.0), not a scientific threshold and not
widenable after seeing a discrepancy.

Per comparison record:

~~~text
NOT_COMPARABLE iff the branch's required reference or production value is absent
AGREEMENT iff comparable and every FieldComparison.matches=true
DISAGREEMENT iff comparable and at least one FieldComparison.matches=false
~~~

AGREEMENT requires empty disagreementCodes and diagnosticIndices. DISAGREEMENT
requires stable code consequences and a synchronously completed diagnostic index
for each required diagnostic group before the comparison row is finalized.
NOT_COMPARABLE requires its exact adverse code and zero diagnostic indices. Root
AGREEMENT means every comparable record agrees; root DISAGREEMENT means at least
one disagrees; root NOT_COMPARABLE is legal only for the branch-specific adverse
primary terminal. The verifier recomputes this fold.

Aggregate arithmetic is exact and independently derived on reference and
production sides:

~~~text
exact complete:
  denominator=T
  numerator=1+E
  p=numerator/denominator
  decision=(p<=alpha)

finite:
  validReplicateCount+F=B
  denominator=B+1
  lowerNumerator=1+E
  upperNumerator=1+E+F
  lowerBound=lowerNumerator/denominator
  upperBound=upperNumerator/denominator
  if observed valid and F=0:
      pValue=lowerBound=upperBound
      decision=(pValue<=alpha)
  else:
      pValue=null
      decision=null
~~~

E is the exact sum of non-null inclusive-tail indicators in that side's ordered
rows. Null/observed-failure aggregate fields follow their closed null branch.
Production finite aggregate projections persist lowerNumerator, upperNumerator,
and denominator; hexadecimal bounds alone are insufficient. A one-field
perturbation of any count, numerator, denominator, bound, p-value, or decision
must fail semantic verification.


## 8. Executable canonical-byte, package, failure-path, and I/O equations

### 8.1 Resolved canonical row and ledger formulae

Let J(x) be section 4.2 canonical JSON bytes without a line terminator and define
JL(x)=ginc(J(x)) for one JSONL row including its mandatory LF. JSON object files
use J(x), never JL(x). Every named upper below means the maximum over the exact
resolved schema branch after applying field-specific integer, string, hash, and
array domains; an unresolved $ref or oneOf is a verification failure.

~~~text
CandidateUpper = max J(CandidateRecordValid),J(CandidateRecordFailed)
SelectionUpper = J(Selection with exactly C tied indices)
StateUpper = max J(CircularState),J(BlockState with exactly q indices)

ExactStateCompleteRowUpper = JL(ExactStateRowComplete)
ExactStateFailureRowUpper  = JL(ExactStateRowAnalyticFailure)
FiniteStateCompleteRowUpper = JL(FiniteStateRowComplete)
FiniteStateFailureRowUpper  = JL(FiniteStateRowAnalyticFailure)

PrimaryRowsUpperExact =
  exactStateCompleteRows*ExactStateCompleteRowUpper
  + exactStateFailureRows*ExactStateFailureRowUpper
PrimaryRowsUpperFinite =
  finiteStateCompleteRows*FiniteStateCompleteRowUpper
  + finiteStateFailureRows*FiniteStateFailureRowUpper
~~~

The four primary multiplicities are persisted. Exact requires
exactStateCompleteRows+exactStateFailureRows=L; finite requires
finiteStateCompleteRows+finiteStateFailureRows=L; the inapplicable pair is zero.
This prevents T*one-generic-row from hiding branch composition.

Comparison rows use seven resolved shapes, each with its own LF:

~~~text
ComparisonObservedUpper = JL(ComparisonObservedRecord)
ComparisonExactStateUpper(i) = JL(the resolved ComparisonExactStateRecord branch i)
ComparisonFiniteStateUpper(i) = JL(the resolved ComparisonFiniteStateRecord branch i)
ComparisonExactAggregateUpper = JL(the resolved ComparisonExactAggregateRecord)
ComparisonFiniteAggregateUpper = JL(the resolved ComparisonFiniteAggregateRecord)
ComparisonFiniteObservedFailureAggregateUpper =
  JL(ComparisonFiniteAggregateObservedFailureRecord)
ComparisonNullAggregateUpper = JL(ComparisonNullBindDisabledRecord)

ComparisonRowsUpperExact =
  sum(i=0..T-1,ComparisonExactStateUpper(i))
  + ComparisonExactAggregateUpper
ComparisonRowsUpperFiniteCompleted =
  ComparisonObservedUpper
  + sum(i=0..B-1,ComparisonFiniteStateUpper(i))
  + ComparisonFiniteAggregateUpper
ComparisonRowsUpperObservedFailure =
  ComparisonObservedUpper+ComparisonFiniteObservedFailureAggregateUpper
ComparisonRowsUpperNull = ComparisonNullAggregateUpper
~~~

The ordered sequence of resolved row-branch identifiers is persisted by the
ledger itself; the verifier derives the sum from that sequence and checks the
RowMultiplicityOperands totals. No generic maximum-row multiplier is legal.

Diagnostics are heterogeneous. Define one LF-inclusive upper for every branch:

~~~text
DH=JL(DiagnosticHeaderRecord)
DE=JL(DiagnosticEdgeRecord)
DC=JL(DiagnosticCodeRecord)
DABZ=JL(DiagnosticCounterRecord with counterFamily=ABZ)
DAZ =JL(DiagnosticCounterRecord with counterFamily=AZ)
DBZ =JL(DiagnosticCounterRecord with counterFamily=BZ)
DZ  =JL(DiagnosticCounterRecord with counterFamily=Z)
DN=JL(DiagnosticNumericalBoundaryRecord)
DF=JL(DiagnosticFooterRecord)

DiagnosticRowsBytesUpper =
  headerRows*DH + edgeRows*DE + codeRows*DC
  + counterABZRows*DABZ + counterAZRows*DAZ
  + counterBZRows*DBZ + counterZRows*DZ
  + numericalRows*DN + footerRows*DF
~~~

Admission and executed diagnostic multiplicities are separately persisted. Each
completed group has one header and footer. NetTE reference counters include both
directions; production adds both directions only when productionCountersStatus is
AVAILABLE. NOT_EXPOSED adds none and requires its reason. Pearson has no edge,
code, or Counter rows. Z equals the guarded sum of the nine row-kind counts.

For any ordered LF-inclusive row-upper sequence seq:

~~~text
ChunkSliceUpper(seq,k) =
  sum(i=k*max_chunk_rows .. min(len(seq),(k+1)*max_chunk_rows)-1, seq[i])
ChunkPrefixUpper(seq,j) = sum(k=0..j-1,ChunkSliceUpper(seq,k))
chunkCount(seq) = 0 if len(seq)=0 else gceil(len(seq),max_chunk_rows)
~~~

These equations define every state/comparison/diagnostic chunk and explicitly
include the final LF of every row.

### 8.2 Exhaustive serial failure automaton

Codes used only in this table are E=ALL_STATE_EXACT_COMPONENT,
F=FINITE_NORMAL, R=FINITE_REPLICATE_FAILURE,
O=FINITE_OBSERVED_ANALYTIC_FAILURE, N=NULL_BIND_DISABLED, and
U=FINITE_BRANCH_UNRESOLVED. U is legal only before the production return selects
F, R, or O. Primary terminal class is one of COMPLETE, NULL_DISABLED,
OBSERVED_ANALYTICAL_FAILURE, REPLICATE_FAILURE,
EXACT_ANALYTICAL_FAILURE, or UNRESOLVED.

N means NOT_CREATED_BEFORE_FAILURE_ROOT. A means the three active-writer choices
DELETED_BEFORE_FAILURE_ROOT, PRESERVED_VERIFIED_PARTIAL_EVIDENCE, or
PRESERVED_UNVERIFIED_PARTIAL_EVIDENCE. Each table row expands once per listed
execution branch and, for A, once per listed disposition. No other Cartesian
combination is legal. j/k/l are completed state/comparison/diagnostic chunk counts
in the stated closed ranges; r is a current record index. The persisted cursor
also contains activeStreamChunkIndex, currentRecordIndex,
currentWriterRowsCompleted, and writer-observed/read byte counters.

| id | branches | failedStage | writerCursor | source identity | completed ordinary nodes before current writer | currentWriter | disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00 | E,U,N | PREFLIGHT | BEFORE_SOURCE_IDENTITY | NOT_COMPLETED | none | NONE | N |
| 01 | E,U,N | SOURCE_IDENTITY | READING_SOURCE_IDENTITY | NOT_COMPLETED | none | NONE | N |
| 02 | E,U,N | SIDECAR_WRITE | AFTER_SOURCE_IDENTITY_BEFORE_ORIGINAL_INPUT | COMPLETE | none | NONE | N |
| 03 | E,U,N | SIDECAR_WRITE | WRITING_ORIGINAL_INPUT | COMPLETE | none | ORIGINAL_INPUT | A |
| 04 | E,U,N | SIDECAR_WRITE | AFTER_ORIGINAL_INPUT_BEFORE_REFERENCE_SPEC | COMPLETE | original | NONE | N |
| 05 | E,U,N | SIDECAR_WRITE | WRITING_REFERENCE_SPEC | COMPLETE | original | REFERENCE_SPEC | A |
| 06 | E,U,N | NULL_BIND | AFTER_SIDECARS_BEFORE_NULL_BIND | COMPLETE | original,spec | NONE | N |
| 07 | E,U,N | NULL_BIND | NULL_BIND_CHECK | COMPLETE | original,spec | NONE | N |
| 08 | U | PRODUCTION_CALL | WAITING_FOR_PRODUCTION_RESULT | COMPLETE | original,spec | NONE | N |
| 09 | F,R,O | OBSERVED_SCAN | AFTER_BRANCH_INPUT_BEFORE_OBSERVED_RECORD | COMPLETE | original,spec | NONE | N |
| 10 | F,R,O | OBSERVED_SCAN | WRITING_OBSERVED_RECORD | COMPLETE | original,spec | OBSERVED_RECORD | A |
| 11 | E,F,R | STATE_SCAN | COMPUTING_PRIMARY_RECORD | COMPLETE | original,spec,[observed],j state chunks | NONE | N |
| 12 | E,F,R | STATE_SCAN | WRITING_STATE_CHUNK | COMPLETE | original,spec,[observed],j state chunks | STATE_CHUNK | A |
| 13 | E,F,R,O,N | PRIMARY_FINALIZE | AFTER_PRIMARY_ROWS_BEFORE_PRIMARY_MANIFEST | COMPLETE | original,spec,[observed],Kp state chunks | NONE | N |
| 14 | E,F,R,O,N | PRIMARY_FINALIZE | WRITING_PRIMARY_MANIFEST | COMPLETE | original,spec,[observed],Kp state chunks | PRIMARY_MANIFEST | A |
| 15 | E,F,R,O,N | COMPARISON | AFTER_PRIMARY_BEFORE_COMPARISON_DISCOVERY | COMPLETE | row 14 predecessors + primary manifest | NONE | N |
| 16 | E,F,R,O,N | COMPARISON | COMPARING_CURRENT_RECORD | COMPLETE | row 15 predecessors + k comparison + l diagnostic chunks | NONE | N |
| 17 | E,F | DIAGNOSTIC | COMPUTING_DIAGNOSTIC_GROUP | COMPLETE | row 16 completed nodes; current comparison record is not emitted | NONE | N |
| 18 | E,F | DIAGNOSTIC | WRITING_DIAGNOSTIC_CHUNK | COMPLETE | row 17 completed nodes | DIAGNOSTIC_CHUNK | A |
| 19 | E,F,R,O,N | COMPARISON | WRITING_COMPARISON_CHUNK | COMPLETE | primary family + k comparison + l diagnostic chunks | COMPARISON_CHUNK | A |
| 20 | E,F | DIAGNOSTIC | AFTER_COMPARISON_DISCOVERY_BEFORE_DIAGNOSTIC_MANIFEST | COMPLETE | primary family + Kc comparison + Kd diagnostic chunks | NONE | N |
| 21 | E,F | DIAGNOSTIC | WRITING_DIAGNOSTIC_MANIFEST | COMPLETE | row 20 nodes | DIAGNOSTIC_MANIFEST | A |
| 22 | E,F,R,O,N | SUCCESS_ROOT_INSTALL | AFTER_LEDGERS_BEFORE_COMPARISON_MANIFEST | COMPLETE | complete primary/comparison families and applicable diagnostic family | NONE | N |
| 23 | E,F,R,O,N | SUCCESS_ROOT_INSTALL | WRITING_COMPARISON_MANIFEST | COMPLETE | row 22 nodes | COMPARISON_MANIFEST | A |
| 24 | E,F,R,O,N | SUCCESS_ROOT_INSTALL | AFTER_COMPARISON_MANIFEST_BEFORE_INSTALL | COMPLETE | row 22 nodes | COMPARISON_MANIFEST | A |

Rows 17,18,20,21 additionally require primaryTerminalClass=COMPLETE and an actual
disagreement. Rows 20/21 exist only if at least one diagnostic group completed.
For analytical/non-comparable primary classes, DStarted=DCompleted=ZExecuted=0.
The exact branch E may carry COMPLETE or EXACT_ANALYTICAL_FAILURE; F carries
COMPLETE; R/O/N carry only their matching adverse class. U carries UNRESOLVED.
Source sets are null in rows 00/01 and exactly three complete embedded manifests in
rows 02-24.

Let persisted counters be o,s,v,kp,pm,kc,kd,dm. They obey o,s,v,pm,dm in {0,1},
0<=kp<=Kp, 0<=kc<=Kc, 0<=kd<=Kd, and are fixed by the selected table row.
Let O,S,V,PM,DM be exact resolved JSON object uppers and let SP,CP,DP be the exact
ordered LF-inclusive row-upper sequences. CM is the least-fixed-point upper of
the applicable success comparison manifest, including its complete
DerivedOperands. SourceBytesPrefix is zero at row 00, the guarded bytes actually
read so far at row 01, and the guarded sum of the three complete role source sets
at rows 02-24. Then:

~~~text
inputSidecarFormulaUpper = O+S
completedStateChunkBytesUpper = ChunkPrefixUpper(SP,kp)
completedComparisonChunkBytesUpper = ChunkPrefixUpper(CP,kc)
completedDiagnosticChunkBytesUpper = ChunkPrefixUpper(DP,kd)

completedArtifactCount = o+s+v+kp+pm+kc+kd+dm
Completed =
  o*O+s*S+v*V
  +completedStateChunkBytesUpper+pm*PM
  +completedComparisonChunkBytesUpper
  +completedDiagnosticChunkBytesUpper+dm*DM
~~~

The active node upper is a total function:

~~~text
NodeUpper(NONE)=0
NodeUpper(ORIGINAL_INPUT)=O
NodeUpper(REFERENCE_SPEC)=S
NodeUpper(OBSERVED_RECORD)=V
NodeUpper(STATE_CHUNK)=ChunkSliceUpper(SP,kp)
NodeUpper(PRIMARY_MANIFEST)=PM
NodeUpper(COMPARISON_CHUNK)=ChunkSliceUpper(CP,kc)
NodeUpper(DIAGNOSTIC_CHUNK)=ChunkSliceUpper(DP,kd)
NodeUpper(DIAGNOSTIC_MANIFEST)=DM
NodeUpper(COMPARISON_MANIFEST)=CM
NextPartialUpper=NodeUpper(currentWriter)
~~~

For a NONE cursor all writer-progress fields are null/zero as specified and
NextPartialUpper=0. For a chunk writer activeStreamChunkIndex equals its completed
chunk count, currentWriterRowsCompleted is 0..255, and currentRecordIndex is the
first not-yet-closed record. For a nonchunk writer activeStreamChunkIndex is null.
These are semantic equalities, not descriptive hints.

~~~text
preserve = I(disposition is PRESERVED_VERIFIED_* or PRESERVED_UNVERIFIED_*)
preservedPartialUpper = preserve*NextPartialUpper
retainedDescriptorCountUpper = completedArtifactCount+preserve
artifactCountUpper = retainedDescriptorCountUpper+1
~~~

The +1 is the failure-manifest root. It is never listed in retainedArtifacts.
Failure-manifest size is the least fixed point of its own decimal size fields:

~~~text
f0=0
f(t+1)=J(resolved failure-manifest branch with
         terminalRootBytesUpper=f(t),
         failureManifestUpper=f(t),
         failurePackageUpper=Completed+preservedPartialUpper+f(t))
stop at first f(t+1)=f(t), or fail if t or arithmetic exceeds guarded caps
failureManifestUpper=f(t)
terminalRootBytesUpper=failureManifestUpper
failurePackageUpper=Completed+preservedPartialUpper+failureManifestUpper
finalRetainedPackageUpper=failurePackageUpper
runDirectoryTransientUpper =
  failurePackageUpper+failure_manifest_reserve_bytes
  +(1-preserve)*NextPartialUpper
~~~

Success-root byte size uses the same monotone least-fixed-point construction for
its embedded DerivedOperands/package fields. The reserve is transient quota and
not an artifact. There is no planned schedule or state-projection artifact.
For success, retainedDescriptorCountUpper=successDescriptorCount and
artifactCountUpper=successDescriptorCount+1, where +1 is the installed comparison
manifest root.

### 8.3 Mechanically recomputable I/O

For a selected failure-table row define exact closed-category byte uppers:

~~~text
IB=o*O+s*S
PB=v*V+completedStateChunkBytesUpper+pm*PM
CB=completedComparisonChunkBytesUpper
DB=completedDiagnosticChunkBytesUpper+dm*DM
SR=sourceBytesReadForIdentityUpper=SourceBytesPrefix
PCMP=PB if writerCursor is at or after AFTER_PRIMARY_BEFORE_COMPARISON_DISCOVERY
     else 0
PW=NextPartialUpper if currentWriter != NONE else 0
PR=NextPartialUpper if disposition is either PRESERVED_* else 0
FW=failureManifestUpper
FR=failureManifestUpper
~~~

The persisted failure-path admit vector for that row is exactly:

~~~text
inputSidecarBytesWritten=IB
inputSidecarBytesReadForVerification=IB
sourceBytesReadForIdentity=SR
primaryBytesWritten=PB
primaryBytesReadForVerification=PB
primaryBytesReadForComparison=PCMP
comparisonBytesWritten=CB
comparisonBytesReadForVerification=CB
diagnosticBytesWritten=DB
diagnosticBytesReadForVerification=DB
currentWriterPartialBytesWritten=PW
currentWriterPartialBytesReadForVerification=PR
comparisonManifestPartialBytesWritten =
  PW if currentWriter=COMPARISON_MANIFEST else 0
comparisonManifestPartialBytesReadForVerification =
  PR if currentWriter=COMPARISON_MANIFEST else 0
failureManifestBytesWritten=FW
failureManifestBytesReadForVerification=FR
~~~

For a success case, IB=O+S; PB is the complete observed/state/primary-manifest
family; CB and DB are the complete comparison and applicable diagnostic families;
SR is the complete three-role source byte sum; PCMP=PB; both generic current-writer
and failure-manifest terms are zero; and both comparison-manifest partial terms
equal CM.

On a failure path, comparisonManifestPartial fields mirror the generic current
writer fields and are not added again. On success, generic current-writer fields
are zero and comparisonManifestPartial write/reread each equal CM. Executed fields
use exact descriptor/custody byte observations in the same equations, including
current-unemitted/partial work; they are not rounded to an upper.

For either suffix x in {Admit,Executed}, terminal kind t in {SUCCESS,FAILURE}:

~~~text
RootWrite_x(t) =
  comparisonManifestPartialBytesWritten_x if t=SUCCESS
  else currentWriterPartialBytesWritten_x
RootRead_x(t) =
  comparisonManifestPartialBytesReadForVerification_x if t=SUCCESS
  else currentWriterPartialBytesReadForVerification_x

totalIoByteVisits_x =
  inputSidecarBytesWritten_x+inputSidecarBytesReadForVerification_x
  +sourceBytesReadForIdentity_x
  +primaryBytesWritten_x+primaryBytesReadForVerification_x
  +primaryBytesReadForComparison_x
  +comparisonBytesWritten_x+comparisonBytesReadForVerification_x
  +diagnosticBytesWritten_x+diagnosticBytesReadForVerification_x
  +RootWrite_x(t)+RootRead_x(t)
  +failureManifestBytesWritten_x+failureManifestBytesReadForVerification_x
~~~

Success sets both failure-manifest terms to zero; failure sets the success-root
terms to the mirror-only values above. Before execution, each Admit field is the
componentwise maximum over the finite legal success cases and all expanded table
rows for the requested calculation mode; this finite maximum is deterministic.
Executed counters are monotone and may not exceed Admit. Fsync, rename, and
directory-fsync counts are separate zero-byte metadata counters. Every sum and
maximum is guarded and totalIoByteVisitsAdmit must not exceed
max_io_byte_visits.


## 9. Phase-specific incremental memory proof

This bounds incremental reference/comparison-driver allocations only. It excludes
production-call internals and the production-owned returned object, so it is not
RSS or a total-process claim. The exclusion is a required schema field.

### 9.1 Closed runtime layout profile

Every used constant is embedded in RuntimeLayoutProfile. There is deliberately no
RECORD_BASE constant: each live record is charged exactly once by its typed count.

~~~text
CONTAINER_BASE_PEAK_BYTES=512
FLOAT_VALUE_PEAK_BYTES=64
INTEGER_VALUE_PEAK_BYTES=64
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
~~~

The proposal profile has probeStatus=NOT_EXECUTED, null runtime identity/digest,
and artifactStatus=PROPOSAL_UNAPPROVED. An approved profile requires a concrete
RuntimeIdentity, PASSED probe, positive probe bytes and digest, matching external
binding ID, and APPROVED_FROZEN. Proposal constants are not approved merely
because they are structurally present.

### 9.2 Executable phase function and exact container ownership

For a PhaseMemoryOperands record p:

~~~text
MemoryUpper(p)=FIXED_PHASE_OVERHEAD_BYTES
 +p.floatValues*FLOAT_VALUE_PEAK_BYTES
 +p.integerValues*INTEGER_VALUE_PEAK_BYTES
 +p.candidateRecords*CANDIDATE_RECORD_PEAK_BYTES
 +p.selectionRecords*SELECTION_RECORD_PEAK_BYTES
 +p.fieldComparisons*FIELD_COMPARISON_PEAK_BYTES
 +p.failureCodes*FAILURE_CODE_VALUE_PEAK_BYTES
 +p.counterEntries*COUNTER_ENTRY_PEAK_BYTES
 +p.sortEntries*SORT_ENTRY_PEAK_BYTES
 +p.sourceEntries*SOURCE_ENTRY_PEAK_BYTES
 +p.dependencyPolicyObjects*DEPENDENCY_POLICY_PEAK_BYTES
 +p.chunkDescriptors*CHUNK_DESCRIPTOR_PEAK_BYTES
 +p.failureDescriptors*FAILURE_DESCRIPTOR_PEAK_BYTES
 +p.encoderFrames*ENCODER_FRAME_PEAK_BYTES
 +p.streamWriteBuffers*STREAM_WRITE_BUFFER_BYTES
 +p.streamReadBuffers*STREAM_READ_BUFFER_BYTES
 +p.hashScratchBuffers*HASH_SCRATCH_BYTES
 +p.decoderScratchBuffers*DECODER_SCRATCH_BYTES
 +p.incrementalEncoderBytesUpper
 +p.containerCount*CONTAINER_BASE_PEAK_BYTES

p.incrementalEncoderBytesUpper =
  p.encoderFrames*MAX_CANONICAL_TOKEN_BYTES
~~~

Whole-row/manifest str or bytes materialization is forbidden. The exact container
model has three mandatory control containers (guard registry, phase counter map,
and scalar operand map), one owner container for each nonempty typed group, and
one wrapper for each live encoder/buffer/scratch object:

~~~text
containerCount(p)=3
 +I(p.floatValues>0)+I(p.integerValues>0)
 +I(p.candidateRecords>0)+I(p.selectionRecords>0)
 +I(p.fieldComparisons>0)+I(p.failureCodes>0)
 +I(p.counterEntries>0)+I(p.sortEntries>0)
 +I(p.sourceEntries>0)+I(p.dependencyPolicyObjects>0)
 +I(p.chunkDescriptors>0)+I(p.failureDescriptors>0)
 +p.encoderFrames+p.streamWriteBuffers+p.streamReadBuffers
 +p.hashScratchBuffers+p.decoderScratchBuffers
~~~

No fixed +32 or inferred nonzero-group prose is permitted.

### 9.3 Exact simultaneous phase counts

Let Sfiles be the guarded sum of the three role-specific source counts and
K=Kp+Kc+Kd. Fields not shown as symbolic in a row are exactly zero.

| phase | floats | integers | candidates | selections | fields | failure codes | counters | sort | source/policy | chunk/failure descriptors | encoder/write/read/hash/decoder |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| admission | 2*n | C+64 | 0 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0/0 | 0/0/0/0/1 |
| sourceIdentity | 2*n | C+Sfiles+64 | 0 | 0 | 0 | 0 | 0 | 0 | Sfiles/3 | 0/0 | 1/0/1/1/1 |
| productionProjection | 2*n+C | W+C+64 | C | 1 | 0 | G | 0 | 0 | 0/0 | 0/0 | 1/0/0/1/1 |
| referenceReplay | 3*n+C | W+C+64 | C | 1 | 0 | G | 0 | 0 | 0/0 | 1/0 | 1/1/1/1/1 |
| nette | 3*n+2*(bins+1)+C | W+6*N+C+64 | C | 1 | 0 | G | U | U | 0/0 | 1/0 | 1/1/1/1/1 |
| comparisonDiagnostic | 3*n+2*(bins+1)+2*C | W+6*N+C+Z+64 | 2*C | 2 | H | G | U | U | 0/0 | 2/0 | 2/2/1/1/1 |
| manifest | 2*n | C+Sfiles+K+128 | 0 | 0 | 0 | 0 | 0 | 0 | Sfiles/3 | successDescriptorCount/0 | 1/1/1/1/1 |
| failure | 2*n | C+retainedDescriptorCountUpper+128 | 0 | 0 | 0 | 0 | 0 | 0 | Sfiles*I(sourceIdentityStatus=COMPLETE)/3*I(sourceIdentityStatus=COMPLETE) | 0/retainedDescriptorCountUpper | 1/1/1/1/1 |

For Pearson phases, bins/U/counter/sort terms are zero. Before entering
comparisonDiagnostic, guarded arithmetic must prove 2*C<=5000; C itself remains
bounded by 5000 and is not raised to 10000. The only phase with
selectionRecords=2, encoderFrames=2, or streamWriteBuffers=2 is
comparisonDiagnostic. Values in the last column are exact, not maxima chosen after
execution. containerCount and incrementalEncoderBytesUpper are then determined by
section 9.2, and phaseUpperBytes must equal MemoryUpper(p).

~~~text
referenceOwnedPeakUpperBytes=max(MemoryUpper(the eight rows))
peakPhase=first phase in table order attaining the maximum
~~~

All primitive counts, each phase upper, and the peak are guarded before the
production call. The proposal schema persists RuntimeLayoutProfile and all eight
PhaseMemoryOperands. A future approved runtime-layout probe must bind exact bytes,
hash, runtime identity, and external binding before these constants authorize a
run.


## 10. Complete persisted resource projection

Every terminal comparison-manifest success branch and every failure-manifest
branch contains one complete DerivedOperands object. Failure roots additionally
contain FailurePathAccounting. A success root without DerivedOperands, or a
failure root without either object, is invalid. Inapplicable scientific quantities
are null; an applicable operation executed zero times is integer zero.

Required scientific/resource fields are:

~~~text
n,h,N,C,T,B,bins,blockCount,WState,U,M
QAdmit,QExecuted,XAdmit,XExecuted,LAdmit,LExecuted,RAdmit,RExecuted
DAdmit,DStarted,DCompleted,ZAdmit,ZExecuted,H,J,G
executionBranch
package,comparison,diagnostic,candidateCardinality,rowMultiplicities
diagnosticRowMultiplicities,rawComputeCounters,compute,io,memory
~~~

FINITE_BRANCH_UNRESOLVED is legal only on a failure before the public return.
blockCount=q, WState=W, and M follow section 5 exactly.

### 10.1 Candidate and row cardinality

CandidateCardinalityOperands is exact:

~~~text
primaryLedgerCandidateRecordsAdmit=LAdmit*C
primaryLedgerCandidateRecordsExecuted=LExecuted*C
observedRecordCandidateRecordsAdmit=I(hasObservedAdmit)*C
observedRecordCandidateRecordsExecuted=I(observedRecordCompleted)*C
comparisonLedgerCandidateRecordsAdmit=QAdmit*C
comparisonLedgerCandidateRecordsExecuted=QExecuted*C
diagnosticReplayCandidateRecordsAdmit=DAdmit*C
diagnosticReplayCandidateRecordsExecuted=DStarted*C
~~~

Only the first three persisted surfaces are checked separately against
max_ledger_candidate_records=100000. Diagnostic replay is transient compute, not a
diagnostic-ledger candidate array. All products are guarded before allocation.
The cap and cap+1 are mandatory probes.

RowMultiplicityOperands persists exact complete/failure state-row counts and
comparison record-kind counts. DiagnosticRowMultiplicityOperands persists admit
and executed counts for HEADER, EDGE, CODE, ABZ, AZ, BZ, Z, NUMERICAL, and FOOTER.
Their guarded sums must equal L, R, and Z as applicable and reproduce section 8.1
without a generic row-size multiplier.

### 10.2 Raw counters and executed compute

RawComputeCounters contains every primitive used by an executed compute equation,
including work that occurred before a current comparison record was emitted and
work inside a started diagnostic group whose footer was not completed.

~~~text
selectionWorkUnitsExecuted =
  3*successfulPrimarySelections*C

netteSortUnitsExecuted =
  guarded occupied-family sum using primaryOccupiedFamilyEntries
netteCmiArithmeticUnitsExecuted =
  15*primaryOccupiedFamilyEntries
  +3*primaryCompletedDirections
  +2*primaryCompletedForwardReverseCandidatePairs

comparisonComputeWorkUnitsExecuted =
  completedComparisonCandidateRecordsCompared
 +completedComparisonStateComponentsCompared
 +completedComparisonFieldComparisonsPerformed
 +completedComparisonDisagreementCodesEmitted
 +completedComparisonLocatorStatusChecks
 +currentUnemittedComparisonCandidateRecordsCompared
 +currentUnemittedComparisonStateComponentsCompared
 +currentUnemittedComparisonFieldComparisonsPerformed
 +currentUnemittedComparisonDisagreementCodesEmitted
 +currentUnemittedComparisonLocatorStatusChecks

diagnosticRecordWorkExecuted =
  completedDiagnosticHeaderRowsEmitted
 +completedDiagnosticEdgeRowsEmitted
 +completedDiagnosticCodeRowsEmitted
 +completedDiagnosticCounterRowsEmitted
 +completedDiagnosticNumericalRowsEmitted
 +completedDiagnosticFooterRowsEmitted
 +currentPartialDiagnosticRecordOperations

diagnosticReplaySelectionWorkUnitsExecuted =
  3*successfulDiagnosticSelections*C
diagnosticReplayNetteSortUnitsExecuted =
  guarded diagnosticOccupiedFamilyEntries sum
diagnosticReplayNetteCmiArithmeticUnitsExecuted =
  15*diagnosticOccupiedFamilyEntries
  +3*diagnosticCompletedDirections
  +2*diagnosticCompletedForwardReverseCandidatePairs
~~~

The remaining ComputeOperands fields are the admitted equations of section 7 or
guarded exact executed sums over these persisted primitives. Raw counters are
monotone, never exceed their branch caps, and are zero outside their applicable
branch/cursor. In particular, current-unemitted comparison counters are nonzero
only at COMPARING_CURRENT_RECORD or a synchronous diagnostic cursor, and
currentPartialDiagnosticRecordOperations is nonzero only after DStarted advances
and before that group's footer closes.

### 10.3 Closed subobjects

ComputeOperands retains every named primary, Pearson/NetTE, comparison, diagnostic
replay, record-emission, and total admitted/executed field from section 7.
IoOperands retains every section 8.3 field plus:

~~~text
currentWriterPartialBytesWrittenAdmit
currentWriterPartialBytesWrittenExecuted
currentWriterPartialBytesReadForVerificationAdmit
currentWriterPartialBytesReadForVerificationExecuted
~~~

Comparison-manifest partial fields mirror these on a failure at that writer and
are not double-counted. PackageOperands contains:

~~~text
artifactCountUpper
inputSidecarFormulaUpper,inputSidecarBytesObserved
primaryRowsBytesUpper,primaryManifestBytesUpper
comparisonRowsBytesUpper,diagnosticRowsBytesUpper
diagnosticManifestBytesUpper,terminalRootBytesUpper
successPackageUpper,failurePackageUpper,finalRetainedPackageUpper
finalRetainedPackageBytesObserved
failureManifestReserveBytes,runDirectoryTransientUpper
retainedDescriptorCountUpper,retainedDescriptorCountObserved
~~~

FailurePathAccounting contains the table key and every operand needed for the
selected row:

~~~text
executionBranch,primaryTerminalClass,failedStage,writerCursor,currentWriter
sourceIdentityStatus,partialDisposition,currentWriterPartialPresent
activeStreamChunkIndex,currentRecordIndex,currentWriterRowsCompleted
completedOriginalInputCount,completedReferenceSpecCount
completedObservedRecordCount,completedStateChunkCount
completedPrimaryManifestCount,completedComparisonChunkCount
completedDiagnosticChunkCount,completedDiagnosticManifestCount
completedComparisonManifestCount,completedArtifactCount
originalInputBytesUpper,referenceSpecBytesUpper,observedRecordBytesUpper
completedStateChunkBytesUpper,completedComparisonChunkBytesUpper
completedDiagnosticChunkBytesUpper,sourceBytesReadForIdentityUpper
artifactCountUpper,inputSidecarFormulaUpper
primaryRowsBytesUpper,primaryManifestBytesUpper
comparisonRowsBytesUpper,diagnosticRowsBytesUpper
diagnosticManifestBytesUpper,terminalRootBytesUpper
retainedDescriptorCountUpper,completedBytesUpper,nextPartialUpper
preservedPartialUpper,failureManifestUpper,failurePackageUpper
currentWriterPartialBytesWritten,currentWriterPartialBytesReadForVerification
~~~

The selected table row must reproduce PackageOperands, IoOperands,
retainedArtifacts, and sourceIdentityStatus/implementationSourceSets.
partialSuccessRootCustody mirrors the generic current-partial custody only when
currentWriter=COMPARISON_MANIFEST; for every other writer it is the closed
NOT_CREATED success-root branch even if a different ordinary-node partial is
retained. A VERIFIED current partial has a digest and exact full reread;
UNVERIFIED has sha256=null. No schedule, planned-schedule, RNG, or
state-projection-file operand exists. plannedDenominator remains only
{source:DESIGN_CONSTANT,value:B+1} inside finite scientific manifests.

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
paths satisfy normalized-segment grammar and are strictly increasing and unique in ASCII byte order
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

Before approval, a standard-library-only verifier must bind the exact v7 formula,
schema, and proposal-profile bytes and run all of the following:

1. Parse JSON, validate the metaschema under Draft 2020-12, resolve every local
   $ref, and prove no unreachable definition or required-property mismatch.
2. Enumerate every oneOf/conditional branch and generate canonical minimum and
   maximum instances for every object, row, manifest, Counter family, media type,
   VERIFIED/UNVERIFIED descriptor, proposal/approved lifecycle branch, success
   terminal, and all 25 expanded failure-cursor rows.
3. Assert J({})=2; reject -1 and -(2**max_operand_bits) in every nonnegative
   integer union before arithmetic.
4. For every bounded integer, string, array, ledger byte field, and numeric cap,
   accept min and max and reject cap+1. In particular probe primary 268435456/
   268435457, comparison 134217728/134217729, diagnostic 67108864/67108865,
   C live 2500 for 2*C=5000 and reject 2501 for the simultaneous phase, and
   candidate-ledger 100000/100001.
5. Probe candidates [1,2] versus [2,1] and duplicates; alpha inside (0,1) versus
   0,1,outside; nonnegative tie tolerance versus a negative value.
6. Probe normalized strictly increasing unique source paths and reject duplicate
   paths with different bytes/hashes, //, /./, /../, leading/trailing slash,
   backslash, Unicode, symlink, and realpath escape.
7. Generate every FieldComparison branch and reject bogus FLOAT_ABS_TOL strings,
   wrong tolerance, cross-domain EXACT values, tail tolerance, and deliberately
   inverted matches. Mutate comparisonStatus/codes/diagnosticIndices and every
   aggregate arithmetic field one at a time.
8. Recompute M, blockCount/WState, all branch Q/X/L/R/D/Z values, the 0/J/J+1
   diagnostic transition, row-kind multiplicities, candidate cardinalities,
   descriptor cardinalities, and the exact +1 LF row bytes.
9. Expand executionBranch x primaryTerminalClass x failedStage x writerCursor x
   currentWriter x partialDisposition. For each legal row recompute predecessors,
   Completed, NextPartialUpper, retained descriptors, artifactCountUpper,
   failure-root least fixed point, PackageOperands, and every admit/executed I/O
   field. Reject every one-field cursor/progress/count/disposition contradiction.
10. Recompute RawComputeCounters-derived executed work including an unemitted
    comparison row and a partial diagnostic group. Recompute all eight memory
    phases, exact encoder frames, stream buffers, indicator containerCount,
    incremental encoder bytes, phase upper, and peak. Reject 2*C>5000.
11. Require source sets null before closure and exactly three embedded source sets
    on every post-closure failure and success root. Require DerivedOperands in
    every terminal root.
12. Accept proposal profile only with PROPOSAL_UNAPPROVED and no external binding.
    Reject standalone APPROVED_FROZEN; accept approved projection only inside a
    matching external approved contract/binding with runtime probe evidence.
13. Scan property names, enums, paths, formulas, and descriptions for forbidden
    planned-schedule/schedule-artifact/state-projection-file vocabulary.
14. Emit a read-only report containing input bytes/hashes, generated instance
    hash, measured min/max bytes, recursive upper, formula equality, and every
    adverse mutation result.

The current design-time schema/probe checks reported in section 15 do not replace
this future independent implementation verifier. Until a separately reviewed
report passes after approval, CANONICAL_BOUND_AND_RESOURCE_BINDING_HOLD remains.

## 13. Deterministic external binding and claim ceiling

No formula, schema, profile, manifest, or approval object includes its own digest.
The external approved projection, if later authorized, binds exact formula and
schema paths/bytes/SHA-256, canonical budget projection/SHA-256, stable binding ID,
approver ID, UTC approval time, and
`disposition=APPROVED_FOR_M6_P1_IMPLEMENTATION`. Proposal artifacts use
`artifactStatus=PROPOSAL_UNAPPROVED`; only an exact external binding may permit
`APPROVED_FROZEN`. Either value without the other is an integrity failure.
Streaming leaf rows and sidecars carry no independent artifactStatus; they inherit
the lifecycle of their unique terminal manifest, preventing an unbound leaf from
asserting APPROVED_FROZEN.

```text
formulaPath=docs/benchmarks/2026-09-08-m6-p1-resource-envelope-v1_1-revision7-formulas.md
schemaPath=docs/benchmarks/schemas/m6-p1-artifact-contract-v7-proposal.schema.json
schemaBytes=394750
schemaSha256=6e5123b3edfb80df0738f758f8cc06138347b6c7129e85706c7b885e75e12be9
profileId=m6-p1-reference-envelope-v1.1-revision7-proposal
```

Current status is exactly:

```text
formulaStatus=REVISION7_PROPOSAL_WRITTEN
schemaStatus=REVISION7_PROPOSAL_WRITTEN_NOT_APPROVED
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

## 14. Revision-7 repair matrix

Addressed means represented in this unapproved proposal, not independently
accepted, implemented, or executed.

| Review finding | Revision-7 disposition |
| --- | --- |
| failure I/O depended on prose stage placeholders | section 8.2 gives the exhaustive 25-row cursor automaton, completed prefixes, active writer/progress, partial disposition, descriptor/artifact counts, byte equations, and root fixed point |
| I/O admit/executed totals were not reproducible | section 8.3 defines every component and a nonduplicating terminal-kind sum |
| finite pre-call failures fabricated a resolved branch | FINITE_BRANCH_UNRESOLVED is restricted to pre-return failure rows |
| failure roots lost source identity | rows 00/01 require null NOT_COMPLETED; every later failure embeds all three complete source sets |
| successful roots lacked DerivedOperands | section 10 and schema require it on all eight concrete success roots |
| executed compute used unpersisted counters | RawComputeCounters includes completed and current/unemitted comparison plus partial diagnostic work |
| undefined M/q/W mappings and D admission | sections 5 and 10 define M, blockCount=q, WState=W, DAdmit, DStarted/DCompleted, and J+1 stop |
| decorative ledger-candidate cap | CandidateCardinalityOperands consumes the cap for primary, observed sidecar, and embedded comparison projections |
| generic row uppers omitted LF and failure multiplicity | section 8.1 defines resolved JL branches, multiplicities, ordered chunk slices, and heterogeneous diagnostics |
| candidate memory and buffers contradicted schema | section 9 keeps candidateRecords<=5000, requires 2*C<=5000, permits exact selection/write-buffer value 2 only in comparisonDiagnostic |
| container/encoder memory was heuristic | section 9 removes RECORD_BASE, fixes encoder/buffer counts, indicator container ownership, and exact encoder bytes |
| layout constants lacked evidence binding | RuntimeLayoutProfile separates unexecuted proposal constants from externally bound approved probe/runtime evidence |
| ledger byte fields exceeded named caps | direct primary/comparison/diagnostic fields are 268435456/134217728/67108864 with cap+1 probes |
| proposal profile could claim approval | separate proposal/approved projections; approved is non-standalone and needs an external binding ID |
| source paths were only lexically suggested | entries are structurally unique and semantically strictly increasing unique normalized ASCII paths |
| FieldComparison/status arithmetic was uncoupled | section 7.4 closes four rule branches, record/root folds, and exact aggregate arithmetic |
| planned schedule had re-entered scope | no schedule artifact exists; finite work only replays ordered completed actual.replicates states |

## 15. Current self-audit and status ceiling

- v6 files are unchanged; both v7 files are new.
- All numeric caps remain PROPOSED / NOT APPROVED.
- The finite scientific path only conditionally replays ordered state identities
  emitted by completed production actual.replicates; no RNG or schedule validation
  is claimed.
- Null and observed-failure paths have no state rows; finite unresolved is confined
  to a pre-production-return failure.
- Every schema integer/property symbol named by the v7 formula is subject to the
  fresh closure scan; unresolved mismatches keep HOLD.
- Primary/comparison/diagnostic direct ledgers use the three tightened caps.
- Proposal and approved profile projections are distinct; no proposal object can
  assert approved status.
- Failure reserve is transient; exactly one success or failure root is retained.
- No science code, test suite, production execution, M6 closure, release approval,
  or SoftwareX readiness is claimed.

Current state:

~~~text
artifactStatus=PROPOSAL_UNAPPROVED
budgetProfileStatus=PROPOSED_NOT_APPROVED
externalApprovalStatus=ABSENT
runtimeLayoutProbeStatus=NOT_EXECUTED
implementationStatus=NOT_AUTHORIZED
M6Status=NOT_EXECUTED
SoftwareXReadiness=UNCHANGED_HOLD
~~~
