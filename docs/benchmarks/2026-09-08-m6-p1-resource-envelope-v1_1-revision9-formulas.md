# M6-P1 resource envelope v1.1 revision 9: explanatory formulas and local shapes

Document ID: `selcal.m6-p1.resource-envelope.formulas.v9`.

Status: **UNFROZEN DESIGN PROPOSAL; LOCAL SHAPE COMPANIONS COMPLETED;
SEMANTIC VALIDATOR ABSENT; RESOURCE ADMISSION HOLD; M6 NOT EXECUTED**.

Internal design repair and local fixture validation are authorized in this
continuation. This document does not grant external approval, establish resource
measurements, execute the scientific engine, or change release/submission status.

## 1. Authority and the exact change boundary

The sole dynamic specification is
[`contracts/m6-p1-semantic-contract-v9-proposal.json`](contracts/m6-p1-semantic-contract-v9-proposal.json).
Its future interpreter is `selcal.m6-p1.semantic-validator.v9`, currently absent.
This document explains that specification. The companion
[`schemas/m6-p1-artifact-contract-v9-proposal.schema.json`](schemas/m6-p1-artifact-contract-v9-proposal.schema.json)
governs local shape only. Neither prose nor a schema pass replaces dynamic
validation. No v7 or v8 document is a normative dependency of v9.

The interrupted v9 semantic preimage had SHA-256
`e0b8854c6ba1de2a0c8b78404f328a901f25be30ce7323e7ff4344d7ffd0ad39`.
The v9 schema preimage was the permissive object `{}`. The formula companion did
not exist. The following immutable predecessors were hashed before edits:

| Preserved file | SHA-256 |
| --- | --- |
| revision 8 formulas | `65c29a3baeecda76edf8043ce66fa472e11dbc63cf5c5196950d087f2e57c552` |
| revision 8 artifact schema | `67d4c86414417445f276b95cf58d70980eb4c554d4478de264f2603c5fcce534` |

Explicit v9 semantic changes in this continuation:

| Interrupted draft issue | Current bounded repair |
| --- | --- |
| Declared 8-byte magic contained 7 ASCII bytes | Exact magic is hex `53434636344c3100`, including one terminal NUL. |
| Ambiguous escaped domain separators | Hash prefixes are expressed as exact hexadecimal bytes. |
| Decimal subtraction depended on ambient precision | Finite comparisons use exact `Fraction.from_float` subtraction and tolerance. |
| Candidate lag indices described as FloatHex | Candidates and record `candidate` are positive integers; comparison uses EXACT. |
| D/Z accounting was implicit | The semantic count registry explicitly defines admitted, started, completed, partial-row and replay-event counts. |
| Raw stat/hash failure demanded unavailable hashes | Raw source and failed value evidence have closed available/unavailable unions. Expected identity never becomes a measured digest. |
| Graph could not label binary sidecars | Declared graph admits explicit materialized sidecar/source/dependency slots, without adding JSON artifact roots. |
| Local validator work marked unauthorized | The open issue now says `OPEN_NOT_IMPLEMENTED`; actual absence remains unchanged. |

The changes do not assert the entire semantic design is sufficient. Section 10
lists the remaining implementability and verification gaps.

## 2. Local shapes and artifact graph

The schema has 19 distinct top-level roots, matching the semantic root registry:
source inventory, declared run graph, input pair, reference specification,
observed record, production replay row, production manifest, primary record,
primary manifest, comparison record, comparison manifest, diagnostic record,
diagnostic manifest, success manifest, failure manifest, budget profile, runtime
probe, external approval envelope and validation report.

`ObservedRecord` is the immutable production observation and has no state.
`PrimaryRecord` can carry the independent observed projection, a finite replay
projection, an exact-state projection or a summary. Production replay rows carry
`productionOrderIndex` and exactly one of `replicateId`/`exactStateIndex`.
Production manifests retain the observed locator when required and all replay
locators in order. The finite mapping must be exactly `productionOrderIndex ==
replicateId == i` for `i=0..B-1`; schema shape alone does not prove this equality.

A comparison retains immutable reference/production locators and scalar field
comparisons. It contains **zero full candidate vectors**. The q-aware required
field plan is retained for audit but must be regenerated from source artifacts;
the submitted plan is never the dynamic authority.

Both terminal roots bind the same declared graph and ordered three source
inventories. The graph declares immutable IDs, artifact types, paths and edges,
without output hashes. This avoids a terminal self-hash cycle. Materialized
sidecars and source files have explicit graph slots. Verification must reject
cycles, duplicate IDs, unreachable retained/emitted outputs, misplaced types,
and source inventories that differ from the declaration. None of those file and
graph checks is implemented by the local schema.

Every schema object is closed at its declared branch. Arrays, strings and integer
domains are bounded. `FloatHex` is a lexical envelope; actual finiteness and
`float.fromhex(token).hex() == token` remain semantic checks. JSON Schema's
mathematical integer type also does not establish a Python built-in int; a
future canonical parser must reject numeric float tokens such as `1.0` for lags.

## 3. Scalars, modes and count vectors

Let `n` be common vector length, `C` the candidate count, `B` the planned finite
replicate count, `T` the complete exact labelled-state count, and `q` the block
count. Candidates are positive, strictly ascending built-in integer lags and
`max(candidates) < n`. Selection rule is exactly `max_upper` or `max_absolute`.
`alphaHex` decodes to `0 < alpha < 1`; `tieToleranceHex` is finite and nonnegative.
The fixed comparison tolerance is `0x1.0000000000000p-46`.

For block shuffle, `n % blockLength == 0`, `q=n//blockLength`, `2<=q<=4096`, and
the state order is an exact permutation of `0..q-1`. Identity is the equality
test against that ordered sequence, not an input assertion to trust. For
circular shift, q and the block order are absent. Exact mode includes identity
exactly once. The detailed admissible circular universe and factorial admission
recurrence still require an explicit v9 semantic operator before execution;
historical v8 formulas are not silently inherited.

Here `Q` counts reference scans, `X` state-generation/validation/application
occurrences, `L` primary state rows, and `R` comparisons including summary:

| Resolved branch | Q | X | L | R | Production observed records |
| --- | ---: | ---: | ---: | ---: | ---: |
| Exact complete/analytic failure | T | T | T | T+1 | 0 |
| Finite normal/replicate failure | B+1 | B | B | B+2 | 1 |
| Finite observed analytic failure | 1 | 0 | 0 | 2 | 1 |
| Null binding disabled | 0 | 0 | 0 | 1 | 0 |

Unresolved branches have no resolved terminal class. Admission uses conservative
mode bounds; executed work uses actual committed events and the active cursor.
No completed-row count can reconstruct a failed partial scan.

## 4. Required comparison field counts and exact arithmetic

The semantic `requiredFieldPlanRegistry` determines the ordered plans. For a
candidate-bearing record its non-state field count is:

```text
fieldPlanLength = 2 + 5*C + 4 = 5*C + 6
statePlanLength = 0             for observed/no-state records
                 3             for circular-shift state records
                 q + 3         for block-shuffle state records
H = statePlanLength + fieldPlanLength
summary fieldPlanLength = 11; summary statePlanLength = 0
```

The `5*C` fields are index, integer candidate, status, estimate and analytic
failure code. The prefix is record role/terminal class; the suffix is selection
status, selected index, tied indices and tail indicator. State and field arrays
are separate. Every generated path, type, rule and ordering position must match;
missing, duplicated, reordered, extra or substituted fields are failures.
Closed comparison codes are severity-ordered after deduplication. Analytic
candidate failure codes, disagreement codes and terminal emitter/code pairs
are separate domains.

Exact complete-case arithmetic is:

```text
E = count of NONIDENTITY states with inclusive-tail indicator true
0 <= E < T
numerator = 1 + E
denominator = T
p = (1 + E) / T
decision = (p <= alpha)
```

Identity is not counted twice. `T=1,E=0` gives p=1; `T=2,E=1` also gives p=1.
For finite mode, `validReplicateCount+F=B`, `0<=E<=validReplicateCount`, denominator
is `B+1`, and bound numerators are `1+E` and `1+E+F`. A valid observation and F=0
permit a point p and decision; otherwise they remain null. The exact-mode
analytic-failure aggregate policy still needs explicit semantic closure before
an exact execution is admissible.

For two finite values p/r, compare exact rational representations:

```text
delta = Fraction.from_float(p) - Fraction.from_float(r)
matches = abs(delta) <= Fraction.from_float(tolerance)
native = p-r
finite native:   residualStatus=FINITE;   residualHex=native.hex()
overflow native: residualStatus=OVERFLOW; residualHex=null
```

An overflow diagnostic never changes the exact comparison into undefined or a
match. Optional-float comparisons with a null operand have no residual fields.
Tail comparison is exact Boolean-or-null comparison, without tolerance.

## 5. D/Z and candidate accounting

The self-contained definitions are in
`comparisonAndDiagnosticRegistry.countDefinitions`; no v8 lookup is needed:

```text
DAdmitUpper = min(RAdmit, 256)
DStarted = number of committed diagnostic headers
DCompleted = number of started groups with committed footers
ZAdmitUpper = 12*DAdmitUpper
ZExecuted = sum(committed rows in every started group)
completed group rows = 2 + bodyRows, 0<=bodyRows<=10
```

Committed rows of the active partial group contribute to Z. Uncommitted row
bytes remain in writer byte custody, without becoming committed rows. Diagnostic
groups and finalized disagreement records must be in bijection. Attempting a
257th group terminates with the registered failure and preserves the prefix;
truncating the evidence and reporting success is forbidden.

Primary state candidate objects are `LExecuted*C`; production observed and replay
projections retain their own actual vectors. Comparisons persist zero candidate
vectors. Each persisted candidate ledger is separately capped at 100,000 and
comparison/replay may hold `2*C<=5000` live candidate objects. The independent
observed projection must be included in the physical ledger accounting: the
current semantic registry does not yet disambiguate both observed ledgers, so
that admission proof remains open.

Diagnostic candidate execution is the sum of actual committed replay-candidate
events, including the partial group, capped at 640,000. `DStarted*C` is forbidden
as an executed-work estimate. The cap is an admission limit, not a measured
runtime cost or an assertion that every admitted group finishes.

## 6. Bytes, streaming and resource formulas

Every integer operation uses the closed nonnegative 256-bit domain. Guarded
addition checks `a<=MAX-b`; multiplication checks `a==0 or b<=MAX//a`; subtraction
checks `b<=a`. Ceiling division uses quotient/remainder, not overflowing `a+b-1`.
`ceil_log2(x)` is 0 for x<=1 and `(x-1).bit_length()` otherwise.

Canonical JSON uses ASCII field names, sorted keys, UTF-8, `ensure_ascii=True`,
no insignificant whitespace/BOM, minimal integer tokens, no numeric float tokens
or nonfinite literals, and one LF per JSONL row. Duplicate keys are rejected
before constructing a dictionary. A parser cannot prove byte canonicality after
discarding duplicate-key or whitespace evidence.

For an admitted string s, an escape-safe upper is `2 + sum(escape_cost(ch))`.
Quote/backslash cost 2; short control escapes cost 2 and other escaped controls
cost 6; other admitted ASCII costs 1. Thus `2+maxCharacters` is valid only for
an explicitly nonescaping alphabet. Dependency version fields admit quotes and
backslashes, so their bounds must include escaping.

The binary sidecar is exactly:

| Offset | Width | Encoding/value |
| --- | ---: | --- |
| 0 | 8 | exact hex `53434636344c3100` |
| 8 | 2 | unsigned little-endian version 1 |
| 10 | 2 | unsigned little-endian flags 1; all other bits zero |
| 12 | 4 | unsigned little-endian element count n |
| 16 | 8*n | finite IEEE 754 binary64, little-endian |

Total bytes are `gadd(16,gmul(8,n))`; no trailing bytes are accepted. Stat/type/
symlink/path/byte-limit checks precede streaming hash verification, which precedes
header parsing. Finite validation streams at most 1,048,576 bytes per read.
No whole-payload buffer is admitted. A four-field descriptor does not establish
that an external sidecar has actually been checked.

For a resolved environment, the proposed byte and memory equations are:

```text
RowUpper(shape,env) = ginc(canonicalJsonUpper(shape,env))
LedgerUpper = guarded sum of all admitted RowUpper occurrences
PackageUpper = fixed point of all nonmanifest uppers + manifest upper
               + failureManifestReserveBytes
PhasePeakUpper = sum(named component uppers in that phase)
GlobalPeakUpper = max(PhasePeakUpper)
sortWork = sum(familyCount * occupiedEntries * ceil_log2(occupiedEntries))
```

Manifest iteration starts at zero, recomputes decimal digit widths, is monotone,
and must converge within 32 iterations. Reserve 16,777,216 failure bytes exactly
once, in addition to success-path admission. Named caps are primary 268,435,456;
comparison 134,217,728; diagnostic 67,108,864; terminal 16,777,216; package and
reference-owned peak each 536,870,912 bytes. The byte visitor cap is 4,294,967,296.
These are proposed caps, not observed peaks. `ioByteVisitsAdmitUpper` and
`ioByteVisitsExecuted` are separate; the ambiguous alias `ioBytes` is prohibited.

The phase inventories explicitly include raw hash buffers, JSON parsing and
duplicate-key tracking, binary decoding, schema validation, scientific windows,
two transient comparison vectors, field plans and diagnostic counters. Their
numeric component bounds and compute coefficients have not been measured or
implemented. The fixed-point and row-upper descriptions are contracts for future
work, not evidence that admission can currently calculate a sound bound.

## 7. Failure operands and actual progress

The normalization DAG commits a prefix from N00 through N15. A failed node must
retain exactly the successfully committed predecessor operands, in DAG order,
with raw encoded-value identity. The failed/current/later node is not a committed
predecessor. Known values must be carried or immutably located; counts cannot
stand in for their provenance.

Raw source evidence is VERIFIED only after actual byte/hash verification.
UNAVAILABLE preserves the declared path, expected identity if supplied, observed
size only if known, null actual digest, and one of STAT_FAILED, HASH_INCOMPLETE or
RAW_BYTES_NOT_RETAINED. Failed operand evidence separately records AVAILABLE or
UNAVAILABLE with a closed reason. A failed initial stat can therefore retain an
honest failure record without inventing a raw hash or parsed operand.

Operator cursors are discriminated: source identity, sidecar, Pearson, NetTE,
state, comparison, diagnostic and writer cursors carry different counters and
next-event coordinates. Source hashing can stop at an entry/byte/hash-block;
NetTE can stop within a direction/counter family. No generic active scan object
or fabricated moment/entropy values substitutes for these positions.

Raw counters use AVAILABLE(value, null reason) or UNAVAILABLE(null value, closed
reason). Sort occupancy buckets retain the distribution: `(4,1)` costs 8 sort
units; `(2,2)` costs 4. Losing that distribution cannot be repaired by total
entry counts. Event counters increment only after the named event commits.

Each writer preserves its own disposition and bytes. Durability order is WRITE,
FILE_FSYNC, RENAME, DIRECTORY_FSYNC, INSTALLED. Rename alone is not installation.
A zero-byte retained partial is valid; an unverified partial has null digest.
Only a verified read of the actual empty file permits the empty-file hash.

## 8. Source identity and external trust

The source-set preimage is the exact decoded hex domain prefix, role ASCII, one
NUL byte and canonical JSON for `{inventoryVersion,role,entries,dependencies}`.
Entries are strictly ASCII-path sorted, ordinals are `0..len(entries)-1`, paths
are unique, and the three source roles have fixed order. Source inventories
contain no mutable lifecycle field. Source-file stat/hash/path checks and
dependency identity checks are needed before the claimed inventory is trusted.

External approval requires an independently provided pinned approval SHA-256,
trust-store ID and trust-store byte digest. A local envelope remains
UNTRUSTED_CLAIM_ONLY even if it says APPROVED_FROZEN. Its ten bindings have fixed
roles/order: formula, schema, semantic contract, budget, runtime probe, semantic
validator, three source inventories, declared graph. Actual binding equality,
approver authenticity and lifecycle containment are dynamic checks. A proposal
root cannot smuggle an approved child; a claimed approved root cannot use a
different nested runtime/source identity. This is separate from authorization
to carry out local design development in this session.

## 9. Reproducible local verification

Run from this worktree:

```text
uv run --no-project --with jsonschema==4.26.0 python docs/benchmarks/verification/check_m6_v9_local_shapes.py
```

The verification fixture uses real Draft 2020-12 validation and an explicit UTC
calendar checker. It checks metaschema validity, local reference reachability,
one representative per root, local oneOf satisfiability, malformed artifacts,
and named union/boundary cases. In-memory fixtures contain synthetic placeholder
identities and are expressly not a valid materialized run package, an approval,
measurements or a validation report produced by the absent semantic validator.

The test also reruns the same malformed artifacts against `{}`. Their acceptance
demonstrates the interrupted placeholder's failure to constrain anything. It
includes a descending-candidate fixture that remains schema-valid, making the
unimplemented sorting check visible instead of falsely claiming semantic PASS.

The binary-header and Fraction examples are representation checks in the fixture
only. They do not test a production streaming path, finite-value scanner, exact
oracle, execution counter, package builder or external trust store.

## 10. Precise remaining HOLDs

The following validators and semantic contracts are absent or incomplete:

1. A single implemented semantic interpreter with canonical byte parsing,
   positive built-in lag validation, real file stat/hash/symlink checks, ordinal
   and input count reconciliation, complete source inventories and graph closure.
2. Exact circular-state universe/factorial guard definitions in v9; exact-mode
   analytic-failure aggregation; independently observed-vector physical ledger
   accounting; an explicit record-role/terminal-state transition mapping.
3. Required-plan regeneration and exhaustive value comparison, selection/tie
   recomputation, inclusive tails, exact/finite aggregate checks, diagnostic
   bijection, failed-prefix reconstruction, stage/cursor coupling and writer
   durability verification. Local shapes deliberately do not prove these.
4. Fully specified shape-to-byte algorithms and environment use, monotonicity,
   fixed-point convergence and all-branch package accounting; compute component
   coefficients; runtime layout/probe measurements; named phase liveness proof.
5. Independently pinned external authority and measured runtime identity, followed
   by actual approved M6 execution. These facts cannot be supplied by fixtures.

The achieved scope is a nonpermissive, inhabitable local-shape proposal plus an
explanatory formula companion. Resource and scientific execution readiness remain
HOLD. No test count here is evidence of scientific validity, calibration quality,
independent replication, release approval, SoftwareX readiness or submission.
