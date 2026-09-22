# M6-P1 resource envelope v1.1 revision 8 formula and semantic-validator contract

> **Status:** `PROPOSAL / NOT APPROVED / NOT FROZEN / NOT IMPLEMENTED / M6 NOT EXECUTED`

> **Claim ceiling:** Revision 8 is a design repair only. It does not authorize an
> M6 run, change SelCal scientific behavior, approve any proposed cap, establish a
> runtime bound, release software, or change SoftwareX readiness.

## 1. Authority, identity, and non-replacement boundary

Revision 8 preserves revision 7 unchanged and supersedes it only as a proposed
design candidate. The revision-7 bytes independently rechecked before this file
was created were:

| Preserved predecessor | Bytes | SHA-256 | Disposition |
| --- | ---: | --- | --- |
| `docs/benchmarks/2026-09-08-m6-p1-resource-envelope-v1_1-revision7-formulas.md` | `69864` | `495e623a71af26cb3145baabc9d0fe85193e7e3c183f52383bbf7383dc2cd4e4` | adverse predecessor; unchanged |
| `docs/benchmarks/schemas/m6-p1-artifact-contract-v7-proposal.schema.json` | `394750` | `6e5123b3edfb80df0738f758f8cc06138347b6c7129e85706c7b885e75e12be9` | adverse predecessor; unchanged |

The exact revision-8 companion schema identity is frozen in section 18 after all
schema writes and read-only checks. This formula is not self-hashing. A future
external approval object must bind the formula, schema, budget profile, runtime
probe, and semantic-validator implementation as five separate byte identities.

Until that future approval and implementation verification exist:

```text
formulaStatus=REVISION8_PROPOSAL
schemaStatus=REVISION8_PROPOSAL_NOT_APPROVED
externalApprovalStatus=ABSENT
freezeStatus=NOT_FROZEN
semanticValidatorStatus=NOT_IMPLEMENTED
runtimeLayoutProbeStatus=NOT_EXECUTED
implementationStatus=NOT_AUTHORIZED
M6Status=NOT_EXECUTED
SoftwareXReadiness=UNCHANGED_HOLD
```

## 2. Deliberately thin architecture

Revision 8 has three non-substitutable layers:

| Layer | May decide | Must not decide |
| --- | --- | --- |
| Draft 2020-12 schema | local type/shape, closed objects, bounded arrays/strings/integers, discriminated unions, immutable constants and local discriminator coupling | dynamic arithmetic, source-file truth, complete comparison coverage, aggregate truth, prefix arithmetic, cross-artifact hashes, lifecycle authority |
| `selcal.m6-p1.semantic-validator.v8` | every dynamic equation and cross-artifact invariant in this document | repair, normalize, reorder, infer missing values, run scientific calculations, approve itself |
| external approval contract | exact approved byte identities, approver and UTC decision | alter formulas, forgive validation failures, manufacture runtime evidence |

There is exactly one dynamic authority: the versioned, future,
standard-library-only semantic validator. `x-semanticInvariant` annotations in the
schema are navigation aids, not executable proof. No second checker may silently
use different equations.

The validator contract is specified here but has status `NOT_IMPLEMENTED`.
Consequently, a schema-valid v8 artifact is only structurally admissible and is
not execution-authorized.

## 3. Scientific scope retained from the parent design

Revision 8 changes representation and resource proof, not scientific behavior.

### 3.1 Finite mode

Finite mode calls the production public API first. Only a completed production
replicate list may supply replay states. The reference side validates every
`replicate_id`, state, identity flag, order, membership, and multiplicity, then
applies the supplied state and independently recomputes the candidate vector.
It does not generate, predict, repair, deduplicate, or reorder a production RNG
schedule.

```text
production call
  -> NULL_BIND_DISABLED: no observed/state scan
  -> FINITE_OBSERVED_ANALYTIC_FAILURE: observed scan only
  -> FINITE_NORMAL or FINITE_REPLICATE_FAILURE:
       observed scan plus exactly B supplied states in production order
```

### 3.2 Exact component mode

Exact mode performs the null-applicability check before enumeration. If enabled,
the independent side enumerates the complete admitted labelled-state universe in
canonical order and compares production statistic/selector components on those
same states. It is not a public exact calibration run. If null binding is
disabled, no state or statistic scan occurs.

### 3.3 Retained scientific invariants

The reference never borrows production scores, selections, validity labels, tail
flags, failure labels, or aggregate arithmetic. Inclusive tails use exact Boolean
comparison without tolerance. No failure triggers an alternative algorithm. No
M6-P1 result can establish RNG correctness, distributional validity,
cross-runtime equivalence, or total-process resource bounds.

## 4. Proposed constants and closed vocabularies

Every value below is `PROPOSED / NOT APPROVED`:

```text
max_operand_bits = 256
max_exact_state_count = 100000
max_finite_replicates = 1000
max_block_count = 4096
max_live_candidate_records = 5000
max_ledger_candidate_records = 100000
max_chunk_rows = 256
max_chunk_count_per_stream = 1000000
max_edge_entries = 65536
max_counter_entries_upper = 250000
max_disagreement_diagnostics = 256
max_pending_diagnostic_jobs = 0
max_numerical_rows_per_diagnostic = 8
max_disagreement_codes_per_record = 32

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

max_input_sidecar_bytes = 67108864
max_primary_ledger_bytes = 268435456
max_comparison_ledger_bytes = 134217728
max_diagnostic_ledger_bytes = 67108864
max_terminal_root_bytes = 16777216
max_run_package_bytes = 536870912
failure_manifest_reserve_bytes = 16777216
max_reference_owned_peak_upper_bytes = 536870912
max_io_byte_visits = 4294967296
```

The three source roles each have a nontransferable cap of 256 files, 16,777,216
bytes per file, 67,108,864 bytes per source set, and 256 declared dependencies.
Reference code is standard-library-only. Production and comparison-driver source
sets require a closed transitive distribution manifest.

Closed identities and statuses are:

```text
budgetProfileId = m6-p1-reference-envelope-v1.1-revision8
runtimeLayoutProfileId = m6-p1-runtime-layout-v8
semanticValidatorContractId = selcal.m6-p1.semantic-validator.v8
comparisonProjectionContractId = selcal.m6-p1.comparison-projection.v8
canonicalizationVersion = selcal-m6-p1-jsonl-v1

calculationMode = ALL_STATE_EXACT | FINITE_B_COMPLETED_STATE_REPLAY
resolved executionBranch = ALL_STATE_EXACT_COMPONENT | FINITE_NORMAL
                         | FINITE_REPLICATE_FAILURE
                         | FINITE_OBSERVED_ANALYTIC_FAILURE
                         | NULL_BIND_DISABLED
unresolved executionBranch = EXACT_BRANCH_UNRESOLVED
                           | FINITE_BRANCH_UNRESOLVED
branchResolutionStatus = UNRESOLVED | RESOLVED
artifactStatus = PROPOSAL_UNAPPROVED | APPROVED_FROZEN
```

`EXACT_BRANCH_UNRESOLVED` is new and is required wherever exact mode has not yet
completed null binding. An unresolved branch has `primaryTerminalClass=null`; it
cannot predict `COMPLETE`, `NULL_DISABLED`, or an analytical failure.

## 5. Total guarded-arithmetic definitions

Booleans are not integers. `OPERAND_MAX=2**256-1`.

```python
def require_uint(x):
    if type(x) is not int or x < 0 or x > OPERAND_MAX:
        fail("INVALID_OR_OVERSIZE_UNSIGNED_INTEGER")
    return x

def I(predicate):
    if type(predicate) is not bool:
        fail("INVALID_INDICATOR_PREDICATE")
    return 1 if predicate else 0

def gadd(a, b):
    a, b = require_uint(a), require_uint(b)
    if a > OPERAND_MAX - b:
        fail("OPERAND_BITS_LIMIT")
    return a + b

def ginc(a):
    return gadd(require_uint(a), 1)

def gsub(a, b):
    a, b = require_uint(a), require_uint(b)
    if b > a:
        fail("INVALID_UNSIGNED_SUBTRACTION")
    return a - b

def gmul(a, b):
    a, b = require_uint(a), require_uint(b)
    if a != 0 and b > OPERAND_MAX // a:
        fail("OPERAND_BITS_LIMIT")
    return a * b

def gceil(a, b):
    a, b = require_uint(a), require_uint(b)
    if b == 0:
        fail("ZERO_DIVISOR")
    q0, r = divmod(a, b)
    return gadd(q0, I(r != 0))

def ceil_log2(x):
    x = require_uint(x)
    if x <= 1:
        return 0
    return gsub(x, 1).bit_length()

def decimal_digits(x):
    x = require_uint(x)
    if x == 0:
        return 1
    k = 0
    while x:
        x //= 10
        k = ginc(k)
    return k
```

All additions, products, subtractions, loop/index bounds, byte counts, row counts,
and aggregate integers use these functions. No exact-state cardinality algorithm
may linearly enumerate merely to discover an over-cap result.

## 6. Canonical bytes and normalized paths

Canonical JSON is UTF-8 with sorted keys, separators `,` and `:`, no ASCII
whitespace, no BOM, no NaN/Infinity, lowercase 64-hex digests, minimal decimal
integers, and binary64 represented by Python `float.hex()` strings. JSON objects
have no trailing LF; every JSONL row has exactly one LF.

For a resolved value-domain node:

```text
J(null)=4; J(false)=5; J(true)=4
J(uint[0..m])=decimal_digits(m)
J(hash256)=66
J(floatHex)=26
J(ASCII string of maximum k bytes)=2+k
J(array(item,0))=2
J(array(item,m>0))=2 + m*J(item) + (m-1)
J(object with zero fields)=2
J(object with k>0)=2 + (k-1) + sum(J(key_i)+1+J(value_i))
JL(node,env)=ginc(JUpper(node,env))
```

`JUpper` is defined in section 11. `ginc` therefore has one meaning and the LF is
never omitted.

A source path is ASCII and follows:

```text
segment = [A-Za-z0-9._-]+ except exactly "." and ".."
path = segment ("/" segment)*
1 <= ASCII bytes(path) <= 512
```

Leading/trailing slash, `//`, dot/parent segment, backslash, Unicode, NUL,
symlink, and realpath escape are rejected before file access. Entries are sorted
strictly by ASCII path bytes; ordinals are exactly `0..sourceCount-1`; paths are
unique independent of bytes/hash. An embedded source-set has no lifecycle field.
It inherits the unique terminal root lifecycle.

## 7. Closed base operands and branch arithmetic

Let:

```text
n = common input length, n>=1
h = greatest canonical candidate, 0<=h<n
N = n-h, N>=1
C = candidate count, 1<=C<=2500
T = exact labelled-state count when applicable, 1<=T<=100000
B = finite design replicate count when applicable, 1<=B<=1000
q = block count for BLOCK_SHUFFLE
WState = serialized/applied state width
Q = reference statistic scans
X = states generated or supplied states validated/applied
L = primary state rows
R = comparison records
D = diagnostic groups
Z = diagnostic rows
H = 9*C+16
J = 256
G = 32
```

### 7.1 Block derivation is exact

For `BLOCK_SHUFFLE`:

```text
require 1<=blockLength<=1250000
require n % blockLength == 0
q = n // blockLength
require 2<=q<=4096
WState=q
len(order)=q
sorted(order)==[0,1,...,q-1]
isIdentity == (order==[0,1,...,q-1])
```

For `CIRCULAR_SHIFT`, `blockLength=q=null` and `WState=1`. The state offset is
checked against the admitted state universe and its identity flag is recomputed.
The schema rejects q=4097 and order arrays longer than 4096; the semantic
validator rejects q inconsistent with `n//blockLength`, non-divisibility, missing
permutation members, and a false identity flag.

Exact-state cardinality and order are also closed:

```text
CIRCULAR_SHIFT with minimumShift=m:
  if 2*m>n: null binding is disabled and T=null
  otherwise states=(0,m,m+1,...,n-m) and T=n-2*m+2

BLOCK_SHUFFLE:
  T=q!, computed incrementally with a pre-cap recurrence
  states=itertools.permutations(range(q)) in lexical tuple order
```

The recurrence stops and raises `EXACT_STATE_LIMIT` before materializing any
state when the next product would exceed 100,000. It does not deduplicate labelled
states whose transformed numerical arrays happen to be equal.

### 7.2 Statistic operands

For Pearson, `bins=U=null`. For NetTE:

```text
2<=bins<=4096
u3=min(bins**3,N)
u2=min(bins**2,N)
u1=min(bins,N)
U=u3+2*u2+u1
```

Every power/product is guarded. Define:

```text
M=max(1,n,h,N,C,T if applicable,B if applicable,bins if applicable)
```

No null or unavailable operand is replaced by zero when computing M.

### 7.3 Resolved terminal count vectors

| Resolved branch | Q | X | L | R | observed record admitted |
| --- | ---: | ---: | ---: | ---: | ---: |
| exact complete or exact analytical failure | T | T | T | T+1 | 0 |
| finite normal or replicate failure | B+1 | B | B | B+2 | 1 |
| finite observed analytical failure | 1 | 0 | 0 | 2 | 1 |
| exact or finite null disabled | 0 | 0 | 0 | 1 | 0 |

Before exact null binding finishes, use `EXACT_BRANCH_UNRESOLVED`; before the
finite public call returns, use `FINITE_BRANCH_UNRESOLVED`. Static admission may
use a conservative mode upper, but an unresolved failure root does not carry a
resolved Q/X/L/R vector.

Closed predicates are:

```text
hasObservedAdmit = calculationMode==FINITE_B_COMPLETED_STATE_REPLAY
                   and executionBranch in {
                     FINITE_NORMAL,
                     FINITE_REPLICATE_FAILURE,
                     FINITE_OBSERVED_ANALYTIC_FAILURE}

observedRecordCompleted = completedObservedRecordCount==1
```

`QAdmit/QExecuted`, `XAdmit/XExecuted`, `LAdmit/LExecuted`, and
`RAdmit/RExecuted` use the table and the retained prefix. Every completed
non-null terminal has `RExecuted=QExecuted+1`.

### 7.4 Candidate cardinalities: persisted and transient are distinct

```text
candidateVectorLength = C
primaryLedgerCandidateRecordsAdmit = LAdmit*C
primaryLedgerCandidateRecordsExecuted = LExecuted*C
observedRecordCandidateRecordsAdmit = I(hasObservedAdmit)*C
observedRecordCandidateRecordsExecuted = I(observedRecordCompleted)*C

comparisonLedgerCandidateRecordsAdmit = QAdmit*C
comparisonLedgerCandidateRecordsExecuted = QExecuted*C

diagnosticReplayCandidateRecordsAdmit = DAdmit*C
diagnosticReplayCandidateRecordsExecuted = DStarted*C

simultaneousCandidateRecordsUpper = 2*C
```

The persisted comparison term is exactly `Q*C`, not `2*Q*C`: one comparison row
embeds the production projection and retains one FieldComparison projection; it
does not persist two CandidateRecord vectors. The comparison/diagnostic phase
does transiently hold the current reference and production candidate vectors,
hence exactly `2*C` live candidate records.

Revision 8 chooses unconditional pre-run admission for that phase. Therefore
`2*C<=5000` is checked before scientific execution, so `C<=2500`; C=2500 is the
boundary and C=2501 is rejected. This avoids a conditional memory loophole on an
early failure path.

Primary, observed, and persisted comparison candidate counts are each checked
against 100,000. Diagnostic replay is transient and is charged to compute and
memory rather than a diagnostic candidate ledger.

## 8. Exhaustive scientific comparison reconstruction

### 8.1 The submitted list is never authoritative

For each comparison row the semantic validator loads both located source
artifacts, verifies their hashes and record identities, and constructs the exact
ordered list:

```text
ExpectedProjection(recordKind, terminalClass, C, q,
                   referenceArtifact, productionArtifact)
```

The canonical traversal order is:

1. `projectionKind`, then `terminalStatus`;
2. for a state row: `state.kind`, the state payload in its declared order, then
   `state.isIdentity`;
3. for an observed/state row, for every `i=0..C-1`:
   `candidateRecords[i].candidateIndex`, `.candidate`, `.status`, `.estimateHex`,
   `.failureCode`;
4. selection status, selected index, then tied indices in stored order;
5. tail indicator;
6. for an aggregate row: `E`, `F`, `validReplicateCount`, `numerator`,
   `lowerNumerator`, `upperNumerator`, `denominator`, `pValueHex`,
   `lowerBoundHex`, `upperBoundHex`, `decision`.

Aggregate/null rows contain zero CandidateRecord objects. Candidate-bearing rows
contain exactly C records, and for every i:

```text
candidateRecords[i].candidateIndex == i
candidateRecords[i].candidate == referenceSpec.candidates[i]
```

The exact expected path sequence, not the author-submitted list, determines
cardinality. The validator requires equality of the entire sequence of
`fieldPath`, `pathClass`, and `comparisonRule`. It then verifies each copied raw
value and recomputes residual, tolerance and `matches`. It rejects:

```text
empty | removed | duplicate-path | reordered | extra | rule-substituted
```

`uniqueItems` and `minItems=1` are schema-level early rejects, but semantic
reconstruction is mandatory because two unequal objects can still repeat the
same path.

### 8.2 Closed rule registry

| Semantic leaf domain | pathClass | comparisonRule | Result |
| --- | --- | --- | --- |
| required finite scientific float | `APPROXIMATE_FLOAT` | `FLOAT_ABS_TOL` | residual=`production-reference`; tolerance exactly `0x1.0000000000000p-46`; match iff absolute residual is within tolerance |
| optional scientific float | `OPTIONAL_APPROXIMATE_FLOAT` | `OPTIONAL_FLOAT_ABS_TOL` | two nulls match with null residual; two floats use the same tolerance; a mixed null/float pair does not match and has null residual |
| canonical float identity field | `CANONICAL_FLOAT` | `FLOAT_HEX_EXACT` | hexadecimal strings equal |
| inclusive-tail indicator | `TAIL` | `TAIL_EXACT` | same Boolean/null type and value; no tolerance |
| integer, Boolean, ASCII enum/string, or null | `EXACT_SCALAR` | `EXACT` | same JSON type and value; no tolerance |

The registry is keyed by exact path plus resolved record branch. A caller cannot
choose a rule based on observed disagreement.

### 8.3 Record and root fold

```text
NOT_COMPARABLE iff the resolved adverse branch requires an absent side
AGREEMENT iff comparable and every reconstructed comparison matches
DISAGREEMENT iff comparable and at least one reconstructed comparison differs
```

Agreement has no disagreement code or diagnostic index. Not-comparable has its
closed adverse code and no diagnostic index. Disagreement has its deterministic
code set and exactly one diagnostic index.

Root agreement means every comparable record agrees. Root disagreement means at
least one record disagrees. Root not-comparable is limited to the corresponding
null/observed/replicate/exact analytical terminal.

### 8.4 Disagreement-to-diagnostic bijection

Revision 8 selects the preferred, simpler contract:

```text
one finalized DISAGREEMENT comparison record
    <-> exactly one completed diagnostic group
```

Diagnostic indices are assigned in comparison-discovery order and are exactly
`0..DCompleted-1`. A completed diagnostic group has one HEADER, zero or more
closed body rows, and one FOOTER. Header and footer carry the same diagnostic
index and target comparison index. No two groups target one comparison, no group
is orphaned, and agreement/not-comparable rows have no diagnostic index.

```text
DCompleted = finalized disagreement record count
DStarted = DCompleted + I(one current partial diagnostic group exists)
0 <= DCompleted <= DStarted <= DAdmit <= J=256
```

When the next disagreement would be group J+1, it is not started and its
comparison row is not finalized. A partial started group may appear only in a
failure root and is not counted as a completed bijection member.

## 9. Exact aggregate arithmetic

The validator independently recomputes both reference and production sides.

```text
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
  if observed valid and F==0:
      pValue=lowerBound=upperBound
      decision=(pValue<=alpha)
  else:
      pValue=null
      decision=null
```

E is the exact sum of non-null inclusive-tail indicators. Every stored fraction
is converted independently to the canonical binary64 hexadecimal value. A
one-field perturbation of a count, numerator, denominator, bound, p-value, or
decision is rejected. Analytical/null terminals use their explicit null branch;
zero is not a synonym for unavailable.

## 10. Raw progress and executed compute

### 10.1 Persist first-order progress, not invertible summaries

`RawComputeCounters` contains monotone first-order facts for:

- null-bind start;
- primary scan starts/completions, state generation/identity/application, each
  transform/support/Pearson/NetTE visit, successful selection, completed NetTE
  directions and forward/reverse pairs;
- completed and current comparison candidate/state/field/code/locator work;
- diagnostic group and replay starts/completions, each partial visit, successful
  selection, direction/pair completion, completed header/body/footer rows, and
  current partial record operations;
- an optional exact active-scan cursor identifying domain, scan, candidate,
  input/support offset, direction, and family ordinal.

There is no derivation from “successful rows” that erases work done by a failed
current scan.

### 10.2 Sort work is histogram-derived

For a unique, ascending occupancy histogram of pairs `(occupiedEntries,
familyCount)`:

```text
SortWork(hist) = sum(
  familyCount * occupiedEntries * ceil_log2(max(occupiedEntries,1))
)

OccupiedCells(hist) = sum(familyCount * occupiedEntries)
FamilyCount(hist) = sum(familyCount)
```

The semantic validator sorts no submitted histogram and performs no repair; the
submitted bucket order must already be strictly ascending and unique. This
distinguishes `[4]` from `[2,2]`: both have four occupied entries, but sort work is
8 versus 4.

```text
primaryNetteSortUnitsExecuted = SortWork(primarySortOccupancyHistogram)
diagnosticNetteSortUnitsExecuted = SortWork(diagnosticSortOccupancyHistogram)

primaryNetteCmiArithmeticUnitsExecuted =
    15*OccupiedCells(primary histogram)
  + 3*primaryCompletedDirections
  + 2*primaryCompletedForwardReverseCandidatePairs

diagnosticNetteCmiArithmeticUnitsExecuted =
    15*OccupiedCells(diagnostic histogram)
  + 3*diagnosticCompletedDirections
  + 2*diagnosticCompletedForwardReverseCandidatePairs
```

### 10.3 Other executed terms

Persisted visit counters directly determine their named executed terms. Selection
uses the single closed name `primarySuccessfulSelections`:

```text
selectionWorkUnitsExecuted = 3*primarySuccessfulSelections*C
diagnosticSelectionWorkUnitsExecuted = 3*diagnosticSuccessfulSelections*C

comparisonWorkExecuted = sum(
  completedComparisonCandidateRecordsCompared,
  completedComparisonStateComponentsCompared,
  completedComparisonFieldComparisonsPerformed,
  completedComparisonDisagreementCodesEmitted,
  completedComparisonLocatorStatusChecks,
  currentComparisonCandidateRecordsCompared,
  currentComparisonStateComponentsCompared,
  currentComparisonFieldComparisonsPerformed,
  currentComparisonDisagreementCodesEmitted,
  currentComparisonLocatorStatusChecks)

diagnosticRecordWorkExecuted =
    completedDiagnosticHeaderRows
  + completedDiagnosticBodyRows
  + completedDiagnosticFooterRows
  + currentPartialDiagnosticRecordOperations
```

All admitted components retain the revision-7 scientific equations, now using
the defined guarded functions and section-7 operands. All 20 canonical
`ComputeProjection.components` names occur exactly once in enum order. The
validator derives every executed value solely from raw counters, checks each
named cap, recomputes primary/diagnostic/grand totals, and rejects self-reported
totals that differ by one.

## 11. Parameterized canonical row and ledger uppers

### 11.1 No global-schema maximum

`RowUpper` is a function of the resolved row branch and current environment:

```text
env = {calculationMode, terminalClass, statisticFamily, nullFamily,
       C, q, candidateVectorLength, requiredFieldComparisonCount,
       disagreementCodeCountUpper, diagnosticIndexCountUpper,
       field-specific index/path/string domains}

JUpper(node,env):
  1. resolve local $ref;
  2. select the unique discriminator branch fixed by env;
  3. replace each dynamic array cardinality by its exact branch cardinality;
  4. use the field's declared maximum, never a generic M shortcut;
  5. apply section-6 scalar/container equations recursively;
  6. fail on an unresolved ref/branch, open property, unbounded domain,
     non-monotone recurrence, or an unused environment operand.

RowUpper(shape,env)=ginc(JUpper(shape,env))
```

The function consumes, rather than merely declares:

```text
CandidateUpper(C,branch)
SelectionUpper(C,branch)
StateUpper(q,nullFamily)
FieldComparisonUpper(required path/rule branch)
```

Every `RowShapeUpperOperand` stores the raw environment operands,
`canonicalJsonUpper`, `jsonlRowUpper`, and occurrence count. The validator
recomputes both values. For every candidate-bearing row shape, increasing C from
1 to 2 while keeping all other applicable operands fixed must strictly increase
the upper. Thus v8 cannot silently fall back to a global 45,016-element maximum.

### 11.2 Exact ledger composition

Primary rows retain separate exact/finite and complete/failure multiplicities.
Comparison rows retain the exact ordered record-branch sequence. Diagnostics
retain HEADER, EDGE, CODE, ABZ, AZ, BZ, Z, NUMERICAL, and FOOTER multiplicities.
Each ledger upper is the guarded sum of its actual resolved row uppers.

For an LF-inclusive row sequence `seq`:

```text
chunkCount(seq) = 0 if len(seq)==0 else gceil(len(seq),max_chunk_rows)
ChunkSliceUpper(seq,k) = sum(RowUpper(seq[i]) for i in the kth 256-row slice)
LedgerUpper(seq) = sum(ChunkSliceUpper(seq,k) for every admitted k)
```

The named hard caps are checked directly:

```text
primary <= 268435456
comparison <= 134217728
diagnostic <= 67108864
terminal root <= 16777216
final package <= 536870912
```

`cap+1` is always rejected.

## 12. Unified serial failure automaton

There is one stage namespace. A failure stores one `FailurePoint`; there is no
second root-level `failedStage` capable of contradicting it.

| stage | legal active node/cursor family | legal substage |
| --- | --- | --- |
| `PREFLIGHT` | `NONE / BEFORE_OPERAND_NORMALIZATION` | `BEFORE` |
| `SOURCE_IDENTITY` | `SOURCE_ENTRY / READING_SOURCE_IDENTITY` | `READ` |
| `SIDECAR_WRITE` | `ORIGINAL_INPUT` or `REFERENCE_SPEC` | `WRITE, VERIFY, FSYNC, INSTALL` |
| `NULL_BIND` | `NULL_BIND / NULL_BIND_CHECK` | `COMPUTE` |
| `PRODUCTION_CALL` | `PRODUCTION_CALL / WAITING_FOR_PRODUCTION_RESULT` | `WAIT` |
| `OBSERVED_SCAN` | `OBSERVED_RECORD` | `COMPUTE, WRITE, VERIFY, FSYNC, INSTALL` |
| `STATE_SCAN` | `PRIMARY_RECORD` for compute; `STATE_CHUNK` for writer | `COMPUTE, WRITE, VERIFY, FSYNC, INSTALL` |
| `PRIMARY_FINALIZE` | `PRIMARY_MANIFEST` | `WRITE, VERIFY, FSYNC, INSTALL` |
| `COMPARISON` | `COMPARISON_RECORD` for compute; `COMPARISON_CHUNK` for writer | `COMPUTE, WRITE, VERIFY, FSYNC, INSTALL` |
| `DIAGNOSTIC` | `DIAGNOSTIC_GROUP` for compute; diagnostic chunk/manifest for writer | `COMPUTE, WRITE, VERIFY, FSYNC, INSTALL` |
| `SUCCESS_ROOT_WRITE` | `COMPARISON_MANIFEST` | `WRITE, VERIFY, FSYNC` |
| `SUCCESS_ROOT_INSTALL` | `COMPARISON_MANIFEST / INSTALLING_NODE` | `INSTALL` |

Writer substages map exactly:

```text
WRITE   -> WRITING_NODE
VERIFY  -> VERIFYING_NODE
FSYNC   -> FSYNCING_NODE
INSTALL -> INSTALLING_NODE
```

Chunk progress allows `chunkRowsCompleted=256`: this represents a full chunk
after its last row but before verification/fsync/install. It is not collapsed
into the next chunk. Compute substages persist `currentRecordIndex`,
`currentFieldIndex`, `currentScanProgress`, and the raw active-scan object where
applicable. A stage, substage, cursor, active node, or progress field cannot be
changed independently without semantic rejection; locally impossible stage/node
and substage/cursor combinations are schema-invalid.

### 12.1 Branch-resolution timing

```text
PREFLIGHT, SOURCE_IDENTITY, SIDECAR_WRITE:
  branchResolutionStatus=UNRESOLVED
  exact -> EXACT_BRANCH_UNRESOLVED
  finite -> FINITE_BRANCH_UNRESOLVED
  primaryTerminalClass=null

NULL_BIND while computing:
  unresolved until the result is committed

after null disabled return:
  executionBranch=NULL_BIND_DISABLED; primaryTerminalClass=NULL_DISABLED

finite PRODUCTION_CALL while waiting:
  FINITE_BRANCH_UNRESOLVED; primaryTerminalClass=null

after a finite public return or exact bind-enable:
  branchResolutionStatus=RESOLVED with the unique branch/terminal mapping
```

The semantic validator owns the full transition table and rejects an early root
that predicts `COMPLETE` or any analytical terminal.

### 12.2 Prefix and partial-node proof

`FailurePrefixProof` retains every completed node/chunk count, bytes completed in
each ledger, current-node bytes written/read-for-verification, verification,
fsync and install flags, retained descriptor count, and retained package bytes.
The selected failure point determines the exact predecessor prefix and which
current partial is legal. The validator recomputes all counts and rejects every
one-field contradiction.

An active compute step can coexist with an already-open stream chunk. Therefore
the proof also contains `openStreamWriters`, rather than pretending
`activeNodeKind` is always the writer. It contains at most one state stream, or at
most the comparison plus diagnostic streams during interleaved discovery. Each
entry fixes stream kind, chunk index, writer state, rows completed `0..256`, bytes
written, and verification bytes read. Two entries with the same stream kind or
chunk identity are illegal. A nonempty entry must correspond to the current
branch prefix; an installed chunk is removed from this array and increments its
completed-chunk count.

The serial artifact plan is generated from resolved branch operands:

```text
source identity
original-input -> reference-spec
null bind
[finite production call]
[observed-record]
[state chunks in chunkIndex order] -> primary manifest
for each comparison index in order:
    compute comparison
    if disagreement: complete exactly one diagnostic group first
    append/finalize the comparison row
[diagnostic manifest when DCompleted>0]
comparison manifest write -> verify -> fsync -> install
```

For any writer node, the local sequence is `WRITE -> VERIFY -> FSYNC -> INSTALL`.
Nodes strictly before the selected point must be installed and counted; the
selected node uses its exact partial counters; nodes strictly after it must be
zero. Chunk k requires every lower chunk installed and no higher chunk started.
This generated plan, not a submitted stage label, determines the prefix.

`partialDisposition` and presence are closed:

```text
NOT_CREATED_BEFORE_FAILURE_ROOT or DELETED_BEFORE_FAILURE_ROOT -> partial absent
PRESERVED_VERIFIED_PARTIAL_EVIDENCE -> present, exact bytes, digest, full reread
PRESERVED_UNVERIFIED_PARTIAL_EVIDENCE -> present, exact bytes, digest null
```

Verification, fsync, and install are separate states. A successful write does not
imply any later state.

### 12.3 Source-identity row 01

`IN_PROGRESS` source identity has no completed embedded source sets. It instead
persists `activeRole`, entry ordinal/path/expected bytes, exact byte offset, total
source bytes read, completed-entry counts per role, and current-prefix SHA-256.
The validator derives source I/O from this object and the input source inventory.
`NOT_STARTED` has neither progress nor sets. `COMPLETE` has exactly three source
sets and no partial progress.

## 13. Pre-derivation failures are first-class

Terminal failures use a discriminated operand proof:

```text
PRE_DERIVATION_FAILURE:
  firstUnavailableOperand
  unavailableReason
  only already-normalized knownOperands

DERIVED_COMPLETE:
  complete BaseOperands
  raw compute counters
  candidate cardinality
  compute projection
  byte-upper proof
  I/O proof
  memory proof
```

A pre-derivation failure must not contain `DerivedCompleteProof`; a complete
proof must not contain “unavailable” fields. No required integer is filled with a
fabricated zero. Pre-derivation is legal only before scientific compute and only
when the named operand is genuinely the first unavailable value under the
validator's fixed normalization order.

Examples include invalid integer type/range, nonfinite input before normalized n,
`n%blockLength!=0`, or q outside 2..4096. A source-identity failure after all base
operands are normalized uses `DERIVED_COMPLETE`, even if source identity itself is
unfinished.

## 14. I/O: admission upper and selected execution are different objects

Revision 8 removes the ambiguous `*Admit` name from a selected failure row.

```text
ModeAdmissionIoUpper(mode, static operands) =
  componentwise conservative maximum over every legal success/failure path
  reachable from that mode before execution

SelectedExecutedIo(terminal, failure point, prefix, partial) =
  exact bytes actually read or written by the retained execution prefix
```

Both vectors use the same closed components:

```text
sourceIdentityBytesRead
scientificInputBytesRead
productionProjectionBytesRead
primaryLedgerBytesWritten / BytesReadForVerification
comparisonLedgerBytesWritten / BytesReadForVerification
diagnosticLedgerBytesWritten / BytesReadForVerification
terminalRootBytesWritten / BytesReadForVerification
totalIoByteVisits
```

For each vector, `totalIoByteVisits` is the guarded sum of exactly those eleven
preceding components. A rename/install and fsync add no byte visits by themselves;
any verification reread is charged explicitly. Source row 01 uses
`SourceIdentityProgress.sourceBytesReadTotal`. A partial node is charged once in
its matching ledger/root component and is never added again as a generic partial.

Admission must be checked before the production call and cannot be widened after
the observed branch is known. Executed must never exceed admission componentwise.

For reporting only, the validator derives but does not trust or persist:

```text
RemainingIoUpper[i] = gsub(ModeAdmissionIoUpper[i], SelectedExecutedIo[i])
```

for every component i after proving the componentwise ordering. It recomputes the
remaining total as the sum of remaining components; it does not subtract two
self-reported totals.

## 15. Phase memory and runtime identity

The runtime layout profile ID occurs exactly once inside a terminal lifecycle.
`MemoryProof` contains no free duplicate profile ID. The future external approval
contract names the expected profile ID once and binds the exact probe artifact;
the semantic validator checks equality across artifacts.

For phase p:

```text
MemoryUpper(p) = fixedPhaseOverheadBytes
  + containerCount*containerBasePeakBytes
  + floatValues*floatValuePeakBytes
  + integerValues*integerValuePeakBytes
  + candidateRecords*candidateRecordPeakBytes
  + selectionRecords*selectionRecordPeakBytes
  + fieldComparisons*fieldComparisonPeakBytes
  + failureCodes*failureCodeValuePeakBytes
  + counterEntries*counterEntryPeakBytes
  + sortEntries*sortEntryPeakBytes
  + sourceEntries*sourceEntryPeakBytes
  + dependencyPolicyObjects*dependencyPolicyPeakBytes
  + chunkDescriptors*chunkDescriptorPeakBytes
  + failureDescriptors*failureDescriptorPeakBytes
  + encoderFrames*encoderFramePeakBytes
  + streamWriteBuffers*streamWriteBufferBytes
  + streamReadBuffers*streamReadBufferBytes
  + hashScratchBuffers*hashScratchBytes
  + decoderScratchBuffers*decoderScratchBytes
  + incrementalEncoderBytesUpper
```

All terms and the sum are guarded. `containerCount` is independently recomputed
from the phase's actual owned structures. Exactly eight phase rows are required:

```text
admission, sourceIdentity, productionProjection, referenceReplay,
nette, comparisonDiagnostic, manifest, failure
```

The comparison/diagnostic row has exactly `candidateRecords=2*C`, at most two
selection records, and at most two writer buffers. Non-NetTE phases have zero
counter/sort entries; mode- or terminal-inapplicable phases use the specified zero
vector rather than an invented maximum. Peak bytes are the maximum of the eight
recomputed phase uppers; `peakPhase` is the first phase in the listed order that
attains it.

Proposal lifecycle requires:

```text
artifactStatus=PROPOSAL_UNAPPROVED
externalBindingId=null
runtime profileState=PROPOSAL
probeStatus=NOT_EXECUTED
runtimeIdentity=null
probeArtifact=null
```

Approved lifecycle is structurally distinct and requires a passed runtime probe,
runtime identity, and probe artifact. It has no nested external-binding ID; the
single lifecycle `externalBindingId` is the authority key.

## 16. Lifecycle and external approval

Only terminal roots and the budget profile carry `Lifecycle`. Sidecars, row
records, chunks, primary/diagnostic manifests, and embedded source sets do not
carry an independent `artifactStatus`; they inherit their unique terminal root.

The future external approval contract is the sole authority object and contains:

```text
externalBindingId
disposition=APPROVED_FOR_M6_P1_IMPLEMENTATION
approverId and approvedAtUtc
exact formula path/bytes/hash
exact schema path/bytes/hash
exact budget-profile path/bytes/hash
exact runtime-probe path/bytes/hash
exact semantic-validator path/bytes/hash
budgetProfileId
runtimeLayoutProfileId
semanticValidatorContractId
```

In approved-execution mode the semantic validator requires:

1. one and only one external approval artifact;
2. exact equality between its ID and every approved terminal/budget lifecycle;
3. exact current bytes and SHA-256 for all five bound artifacts;
4. the approved budget profile and runtime layout profile, with no proposal
   subobject anywhere below an approved lifecycle;
5. no approved subobject anywhere below a proposal lifecycle;
6. no outer-A/nested-B authority path, because nested binding IDs do not exist;
7. exact runtime and profile identities matching the approved probe.

A schema-valid approval-shaped object is not evidence that approval occurred.
Only an externally issued, current-byte-matching artifact can change status.

## 17. Versioned standard-library semantic-validator contract

### 17.1 Interface and purity

The future implementation identity is:

```text
contractId=selcal.m6-p1.semantic-validator.v8
language=Python standard library only
mode=PROPOSAL_AUDIT | APPROVED_EXECUTION
input=read-only artifact directory plus explicit formula/schema/profile paths
output=one canonical JSON validation report to stdout or an explicitly new path
exit=0 only when every applicable invariant passes
mutation=forbidden
scientific execution=forbidden
network=forbidden
```

It may use `argparse`, `dataclasses`, `decimal`, `hashlib`, `json`, `math`,
`os`, `pathlib`, `re`, `stat`, and `sys`. It must not import SelCal production
modules, NumPy, SciPy, a JSON-schema library, or any candidate scientific
implementation. Draft schema validation remains a preceding structural gate;
this validator is the sole authority for dynamic and cross-artifact semantics.

### 17.2 Fail-closed order

The implementation must execute in this order and retain all failures without
repair:

1. verify exact input bytes, canonical decoding, duplicate JSON keys, paths,
   hashes, and artifact-type uniqueness;
2. verify lifecycle mode and, when applicable, the one external authority;
3. verify source-set role, closure, ordinal, path order, bytes and hashes;
4. normalize operands with section-5 guarded operations; select pre-derivation or
   complete proof without zero substitution;
5. verify null/statistic parameters, q/divisibility/permutation, M and branch
   resolution timing;
6. reconstruct Q/X/L/R/D/Z, candidate cardinalities and diagnostic bijection;
7. reconstruct every comparison field and aggregate independently from source
   artifacts;
8. derive executed compute solely from raw counters and histograms;
9. recompute parameterized row/chunk/ledger/package uppers;
10. replay the unified failure point and prefix, then recompute both I/O vectors;
11. recompute all eight memory phases and the peak using the uniquely bound
    runtime profile;
12. check all named caps and emit deterministic findings.

No later check may excuse an earlier failure. Unknown artifact, field, enum,
failure code, interrupted cause, comparison path, or runtime identity is a hard
failure.

### 17.3 Validation report

The report records validator contract/implementation hash, every input
path/bytes/hash, mode, ordered check IDs, PASS/FAIL per check, exact adverse
mutations when used in tests, and final disposition. It cannot say `APPROVED`,
`FROZEN`, `IMPLEMENTED`, or `M6_EXECUTED` merely because validation succeeds.

## 18. TDD and counterexample matrix

The v7 counterexamples are the observed RED baseline. Revision 8 structural
probes may turn only schema-owned cases GREEN. All semantic rows remain
`DESIGN-RED / VALIDATOR NOT IMPLEMENTED` until an independently reviewed future
validator exists.

| ID | Mutation/probe | v7 RED | Required v8 authority and expected result |
| --- | --- | --- | --- |
| C1-01 | `fieldComparisons=[]` | accepted | schema rejects `minItems` |
| C1-02 | exact duplicate FieldComparison | accepted | schema rejects `uniqueItems` |
| C1-03 | same path twice with different payload | accepted | semantic rejects duplicate path |
| C1-04 | remove one required field | accepted | semantic reconstructed sequence mismatch |
| C1-05 | reorder two fields | accepted | semantic ordered-sequence mismatch |
| C1-06 | add legal-looking extra field | accepted | semantic reconstructed sequence mismatch |
| C1-07 | substitute rule/pathClass | accepted | schema rejects one-field rule mutation when class retained; semantic registry rejects coordinated substitution |
| C1-08 | candidate vector shorter/longer, index or candidate changed | accepted in relevant shapes | semantic rejects exact C/index/reference mapping |
| C1-09 | disagreement without exactly one completed target diagnostic | accepted | semantic rejects global bijection |
| C2-01 | change one stage while retaining cursor/node | accepted | schema or semantic rejects unified point |
| C2-02 | early exact failure predicts COMPLETE | accepted | schema rejects unresolved exact branch with non-null terminal |
| C2-03 | early finite failure predicts REPLICATE_FAILURE | accepted | schema rejects unresolved finite branch with non-null terminal |
| C2-04 | 256-row chunk written before verify/fsync/install | not representable | accepted with rows=256 and distinct VERIFY/FSYNC/INSTALL cursors |
| C2-05 | mutate VERIFY to FSYNC but leave progress flags | not closed | semantic rejects prefix contradiction |
| C3-01 | invalid n before derivation | required fabricated complete proof | pre-derivation branch accepted; complete zero-filled proof rejected |
| C3-02 | combine pre-derivation and complete fields | ambiguous | schema rejects union contamination |
| C4-01 | row upper with C=1 then C=2 | global ambiguity | semantic recomputation is dynamic, monotone, and strict for candidate-bearing shapes |
| C4-02 | global schema maximum used for small C | possible | semantic rejects unused/mismatched environment |
| C4-03 | selected failure vector mislabeled Admit | ambiguous | impossible under separate object names |
| C5-01 | sort families `[4]` | irrecoverable from total 4 | semantic yields 8 |
| C5-02 | sort families `[2,2]` | irrecoverable from total 4 | semantic yields 4 |
| C5-03 | mid-primary or diagnostic scan with zero successful rows | work erased | raw partial counters/cursor retained and executed total recomputed |
| B-01 | `q=4096`, order exact permutation | schema boundary | accepted structurally; semantic accepts only matching n/blockLength |
| B-02 | `q=4097` | accepted | schema rejects |
| B-03 | q legal but missing/duplicate/out-of-range order member | partly accepted | schema rejects duplicate/out-of-range; semantic rejects length/permutation mismatch |
| B-04 | n not divisible by blockLength | undefined | semantic rejects `BLOCK_LENGTH_NOT_DIVISOR` |
| CAP-01 | `C=2500`, `2*C=5000` | prose only | semantic accepts if all other constraints pass |
| CAP-02 | `C=2501`, `2*C=5002` | schema could accept | schema rejects C; semantic independently rejects 2*C |
| CAP-03 | named ledger exactly cap | boundary | schema and semantic accept |
| CAP-04 | named ledger cap+1 | boundary | schema rejects |
| AGG-01 | perturb E/F/numerator/denominator/bound/decision by one | accepted | semantic rejects |
| SRC-01 | row01 source identity with exact partial offset | not reconstructible | schema represents; semantic recomputes source I/O |
| SRC-02 | embedded source-set adds `artifactStatus` | accepted in v7 | schema rejects closed source set |
| LIFE-01 | proposal lifecycle embeds approved runtime | accepted via nested branch paths | schema rejects |
| LIFE-02 | approved outer ID A, nested ID B | accepted | nested ID removed; semantic requires single external ID across artifacts |
| LIFE-03 | bogus bound bytes/hash | accepted structurally | semantic recomputes and rejects |
| RUN-01 | memory outer runtime ID differs from nested runtime ID | accepted | outer duplicate removed; semantic binds sole lifecycle profile |
| INT-01 | INTERRUPTED without signal/cancellation/timeout cause | underdefined | schema rejects closed cause union |

Future TDD order is mandatory:

1. add one RED test against the absent or deliberately incomplete validator;
2. confirm the expected semantic failure, not a fixture/schema error;
3. implement the smallest validator rule;
4. rerun that test and all earlier tests GREEN;
5. only then add the next row.

No production scientific code may be changed during that sequence.

## 19. Failure-code and interruption registry

Failure codes are closed in the schema and partitioned by class. Resource limits
include operand, exact-state, compute, I/O, memory, ledger, and package caps.
Integrity failures include invalid inputs, block derivation/permutation, source
identity/dependency, production-state identity, comparison projection, diagnostic
bijection, aggregate arithmetic, canonical bytes/hash, and lifecycle binding.

`INTERRUPTED` requires exactly one cause:

```text
SIGNAL(SIGINT|SIGTERM|SIGHUP)
CANCELLATION(USER|ORCHESTRATOR)
TIMEOUT(MONOTONIC, limitMilliseconds>=1)
```

Free exception strings, hostnames, usernames, or platform-derived messages are
not canonical decision fields.

## 20. Open issues and approval ceiling

The following remain open and are not softened by schema self-checks:

1. `selcal.m6-p1.semantic-validator.v8` has not been implemented or independently
   reviewed; every dynamic/cross-artifact TDD row remains RED by design.
2. Runtime layout constants are proposed placeholders; no approved runtime probe
   or external binding exists.
3. Budget constants have not been scientifically or operationally approved.
4. No source-set closure, real package, production return, comparison ledger,
   diagnostic ledger, or failure prefix has been generated under v8.
5. No M6 scientific calculation or M6 execution has occurred.
6. Passing Draft schema checks would show only structural consistency, not
   scientific correctness, memory truth, lifecycle approval, release readiness,
   or SoftwareX submission readiness.

The only permissible design decision after the present write is an independent
revision-8 review. Until that review reports no Critical or Important issue, the
status remains:

```text
PROPOSAL / NOT APPROVED / NOT FROZEN / NOT IMPLEMENTED / M6 NOT EXECUTED
```

## 21. Exact companion identity and design-time self-audit

The final companion identity and executed design-time structural checks are
inserted only after all schema writes stop. They do not approve either file.

```text
schemaPath=docs/benchmarks/schemas/m6-p1-artifact-contract-v8-proposal.schema.json
schemaBytes=97692
schemaSha256=67d4c86414417445f276b95cf58d70980eb4c554d4478de264f2603c5fcce534
schemaDraftStatus=DRAFT_2020_12_METASCHEMA_PASS
localRefStatus=191_REFERENCES_0_MISSING
duplicateKeyStatus=PASS
definitionReachabilityStatus=86_OF_86_REACHABLE
boundedPrimitiveStatus=236_INTEGER_22_ARRAY_11_STRING_97_OBJECT_SCHEMAS;_1416_INTEGER_BOUNDARY_AND_BOOL_PROBES_PASS
representativeInstanceStatus=11_OF_11_TOP_LEVEL_ROOTS_PASS;_ALL_LISTED_LOCAL_UNION_BRANCHES_SATISFIABLE
adverseMutationStatus=DESIGN_TIME_STRUCTURAL_PROBES_PASS;_DYNAMIC_CASES_REMAIN_VALIDATOR_NOT_IMPLEMENTED
```

This section records exact bytes of the schema only. The formula's own bytes and
hash are reported externally after its final write, avoiding a self-hash cycle.
