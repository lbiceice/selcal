# M6-P1 independent reference resource envelope v1.1 — proposal

> **Status:** `PROPOSAL / NOT APPROVED / NOT FROZEN / NOT IMPLEMENTATION AUTHORITY / M6 NOT EXECUTED`

> **Decision boundary:** This document proposes a bounded, streaming materialization contract for the independent M6-P1 reference implementation. It does not authorize source or test implementation, does not set a scientific success threshold, and does not change SelCal's public input contract.

## 1. Bound authority and current evidence

This proposal supplements, but does not modify or supersede, the following parent design as currently measured:

| Item | Current identity |
| --- | --- |
| Parent design | `docs/benchmarks/2026-09-06-m6-p1-independent-reference-design.md` |
| Parent bytes | `34234` |
| Parent SHA-256 | `ab6e40cc57eb5e4272451ebcb227eab45bf45f1ca66795530adb8d9957490064` |
| Existing streaming oracle | `src/selcal/exact_oracle_v0.py`, SHA-256 `ffbf002949a9a7530fa4a99aa62bd6125515866533c176f9306754d93b9aade7` |
| Current production calibration | `src/selcal/calibration_v2.py`, SHA-256 `a5249d5facfbcfa8f28b98a70115dbd5ae197e9c1743796fb2fe7e32371e3900` |
| Checked date | `2026-09-07` |

The parent design currently requires an ordered in-memory `states` tuple whose rows retain the complete transformed source and candidate vector. Its existing `max_exact_state_count=100000` does not bound the product of state count and series length. The following counterexample is a capacity proof, not an executed allocation:

```text
n = 100000
candidates = (1,)
null = circular_shift_v2(min_shift=1)
R = n - 2*min_shift + 2 = 100000
retained transformed-source entries = R*n = 10,000,000,000
lower-bound payload at 8 bytes per entry = 80,000,000,000 bytes
```

That lower bound excludes Python containers, state records, candidate records, statistics and serialized output. Therefore the parent design remains `RESOURCE_ENVELOPE_REVISION_REQUIRED / NOT FROZEN / NOT EXECUTED` until a replacement output contract and its numerical limits are approved.

## 2. Design decision proposed for approval

Replace the retained all-state tuple with an ordered streaming calculation and a canonical chunked JSONL ledger. The implementation would materialize at most one transformed source and one chunk of result records at a time. It would retain every labelled state, including repeated numerical arrays and sampled identities, without retaining the transformed source in completed rows.

This changes materialization only. It must preserve all scientific and algorithmic invariants of the parent design:

1. enumerate every admitted labelled state in the specified order;
2. preserve state identity, multiplicity and original labels without deduplication;
3. construct each transformed source independently from the original source and state label;
4. complete the candidate vector for one state before selection so ties and the true family maximum remain observable;
5. compare reference and production values state by state without using production values as reference inputs;
6. accumulate `E`, `F`, inclusive tail indicators and their exact denominators online;
7. keep analytical failures and null/resource failures distinct;
8. make a completed transformed source exactly reconstructable from original-input identity, transformation specification and state label;
9. never truncate, deduplicate, silently downgrade to Monte Carlo, or reinterpret a resource rejection as scientific evidence.

The existing V0 oracle supports the feasibility of single-state streaming, but it remains scientifically insufficient for M6-P1 because it reuses production statistics and selection. It is not an expected-answer generator.

## 3. Symbols and derived operands

All resource admission is pure integer arithmetic performed before bin-edge construction, state materialization, statistic scans or output-file creation.

| Symbol | Meaning |
| --- | --- |
| `n` | length of each input series |
| `h` | `max(candidates)` |
| `N` | common support length `n-h` |
| `C` | candidate count |
| `R` | all-state count `T`, or explicitly planned schedule row count `B` |
| `S` | null-side work term: `1` for circular shift, block count `q=n/L` for block shuffle |
| `K` | proposed chunk row count, at most `max_chunk_rows` |
| `bins` | NetTE bin count; not applicable to Pearson |

Derived operands proposed for every request:

```text
transform_value_visits = R*n
candidate_support_visits = R*C*N
reference_work_units = R*(C*N + n + S)
ledger_candidate_records = R*C
live_candidate_records = min(R, K)*C
edge_entries = 2*(bins+1)                         # NetTE only
counter_entries_upper =
    2 * (min(N, bins**3) + 2*min(N, bins**2) + min(N, bins))
                                                    # NetTE only
```

The NetTE bound is deliberately conservative: it covers forward and reverse diagnostic counters retained at the same time. A lower bound may be proposed later only after observed peak-memory evidence and a new review; implementation may not silently lower or reinterpret this formula.

## 4. Proposed budget profile

Profile identifier: `m6-p1-reference-envelope-v1.1-proposal`.

| Field | Proposed value | Authority status | What it limits |
| --- | ---: | --- | --- |
| `max_exact_state_count` | `100000` | Existing parent-design limit | All-state cardinality |
| `retained_transformed_source_entries` | exactly `0` | Required design invariant | Completed ledger rows may not embed transformed series |
| `max_schedule_rows` | `1000` | **PROPOSED** | Supplied finite schedule rows |
| `max_operand_bits` | `256` | **PROPOSED** | Integer-arithmetic denial-of-service guard |
| `max_transform_value_visits` | `2500000` | **PROPOSED** | `R*n` |
| `max_candidate_support_visits` | `2500000` | **PROPOSED** | `R*C*N` |
| `max_reference_work_units` | `2500000` | **PROPOSED** | `R*(C*N+n+S)` |
| `max_ledger_candidate_records` | `100000` | **PROPOSED** | Complete serialized candidate rows |
| `max_live_candidate_records` | `5000` | **PROPOSED** | In-memory candidate records in one chunk |
| `max_chunk_rows` | `256` | **PROPOSED** | In-memory completed state rows |
| `max_edge_entries` | `65536` | **PROPOSED** | Two NetTE edge vectors |
| `max_counter_entries_upper` | `250000` | **PROPOSED** | Conservative NetTE counter occupancy |
| `max_final_ledger_bytes` | `268435456` | **PROPOSED** | Completed canonical JSONL, 256 MiB |
| `max_reference_owned_peak_estimated_bytes` | `536870912` | **PROPOSED** | Reference-owned estimated peak, 512 MiB |

The three `2500000` work-related values are intentionally aligned with the current production total-work guard only as an initial engineering proposal. That alignment is not evidence that the limit is adequate for the standard-library Pearson or NetTE reference path. Approval authorizes TDD implementation of the guard, not a claim that every scientifically important case fits under it.

No Type-I-error, power, minimum coverage, acceptable disagreement or external-validity threshold is set here. Those remain separate M6 scientific-design decisions.

## 5. Fixed preflight order and fail-closed result

Admission must use this exact observable order so expensive or ambiguous work cannot precede a simpler rejection:

1. reject wrong primitive types, booleans in integer fields, negative values and invalid structural shapes;
2. reject any integer operand exceeding `max_operand_bits` before products, factorials or powers are fully expanded;
3. validate null applicability and calculate the state count incrementally under the existing exact-state cap;
4. validate schedule/state rows and candidate products;
5. validate transform, candidate-support and total-work operands;
6. validate NetTE edge and conservative counter bounds, when applicable;
7. validate the reference-owned estimated peak-memory bound;
8. validate the estimated final-ledger byte bound;
9. only then bind edges, construct counters, enumerate states, evaluate statistics or create a temporary ledger.

Every limit rejection must return a typed result with at least:

```json
{
  "status": "REFERENCE_RESOURCE_LIMIT",
  "limit_code": "<stable machine code>",
  "limit": 0,
  "observed": 0,
  "observed_at_least": null,
  "budget_profile_id": "m6-p1-reference-envelope-v1.1-proposal",
  "derived_operands": {},
  "states": null,
  "E": null,
  "F": null,
  "p_exact": null,
  "decision": null
}
```

Exactly one of `observed` and `observed_at_least` is populated. The latter is used when an incremental guard stops before an exact larger operand is safely computed. A resource rejection must not write a `COMPLETE` ledger manifest and must not be categorized as `ANALYTICALLY_UNEVALUABLE`.

Stable proposed `limit_code` values are:

```text
OPERAND_BITS_LIMIT
EXACT_STATE_COUNT_LIMIT
SCHEDULE_ROW_LIMIT
TRANSFORM_VALUE_VISIT_LIMIT
CANDIDATE_SUPPORT_VISIT_LIMIT
REFERENCE_WORK_UNIT_LIMIT
LEDGER_CANDIDATE_RECORD_LIMIT
LIVE_CANDIDATE_RECORD_LIMIT
EDGE_ENTRY_LIMIT
COUNTER_ENTRY_LIMIT
ESTIMATED_PEAK_BYTE_LIMIT
ESTIMATED_LEDGER_BYTE_LIMIT
```

## 6. Streaming result and custody contract

### 6.1 Completed state row

Each canonical JSONL state row retains only bounded/reconstructable fields:

```text
schema_version
row_index
state_id
labelled_state_payload
is_identity
candidate_records                 # complete for this state
selection
exceeds_observed                  # true, false or null
failure_stage
failure_reason
original_input_identity_sha256
transformation_spec_sha256
```

It must not contain the transformed source, a base64 copy of it, an alias to a retained mutable buffer, or a lossy digest substituted for the labelled state payload. `retained_transformed_source_entries == 0` is verified structurally over the completed ledger.

### 6.2 Chunk and final manifest

Each chunk contains no more than both `max_chunk_rows` and `max_live_candidate_records/C` rows. Rows are written in canonical sequence. The final manifest is created atomically only after all planned rows are durable and re-readable, and contains:

```text
schema_version
budget_profile_id
request_identity_sha256
original_input_identity_sha256
transformation_spec_sha256
planned_row_count
completed_row_count
first_row_index
last_row_index
ledger_bytes
ledger_sha256
ordered_chunk_sha256s
completion_status = COMPLETE
E
F
tail_bounds
p_value_or_null
decision_or_null
```

An interrupted or over-limit writer may leave a named temporary/partial artifact only if it carries `completion_status=PARTIAL` and cannot be mistaken for a final ledger. It must not create or retain a `COMPLETE` manifest. Resume behavior is outside this proposal unless separately specified; rerunning may start from scratch.

### 6.3 Schedule API correction

The parent signature `summarize_schedule(spec, states)` must not convert the supplied rows to a tuple. The proposed replacement is conceptually:

```text
summarize_schedule(spec, planned_B, state_iterable, ledger_sink)
```

It verifies exact row IDs `0..planned_B-1`, premature EOF, extra rows, state membership, labelled duplicates and identities while consuming the iterable once. Every admitted planned row is retained. A repeated state is not a duplicate record and must not be removed.

## 7. Minimum TDD authorization sequence after approval

No item below has been run. Approval of this proposal would authorize this order only:

- [ ] **R1 — Pure integer preflight RED/GREEN.** Test the `10^10` transformed-entry counterexample without allocation; test `limit-1`, `limit`, `limit+1`, booleans, negatives and over-256-bit operands for every relevant field. Replace edge/statistic/enumerator/writer calls with bombs to prove rejection precedes them.
- [ ] **R2 — Single-state streaming RED/GREEN.** Use the disclosed six-state Pearson fixture. Require exact state order, identity, multiplicity, reselection and `p_exact=3/6`; assert completed rows contain no transformed source and do contain reconstruction identities.
- [ ] **R3 — NetTE capacity RED/GREEN.** Test edge and conservative Counter limits before edge/table construction. Retain the disclosed small binary NetTE integer-table result.
- [ ] **R4 — Chunk-ledger RED/GREEN.** Test both chunk limits, exact JSONL order, repeated labelled states, final digest recomputation and atomic completion. Force a writer to encounter the byte cap and prove it cannot produce `COMPLETE`.
- [ ] **R5 — One-pass schedule RED/GREEN.** Test explicit `planned_B`, duplicate labels, sampled identities, membership, early/late EOF, exact E/F accounting and resource rejection without tuple materialization.
- [ ] **R6 — Independence and regression.** In a fresh subprocess block `selcal`, `numpy` and `scipy` imports for the reference package; then run existing exact-oracle, selection and calibration finalization/failure regressions. Peak-memory characterization is last and uses admitted bounded fixtures only.

Every RED must fail for the absent intended behavior, not for an import typo or fixture error. Every GREEN must rerun the same test. Source-changing operations finish before hashes, ledger verification or receipts are frozen.

## 8. Required review and approval decisions

Before implementation, a specification owner must explicitly decide all of the following:

1. approve, revise or reject each **PROPOSED** numerical value in section 4;
2. approve replacement of the in-memory `states` tuple with canonical JSONL plus final manifest;
3. approve the one-pass schedule signature and its exact planned-row failure behavior;
4. approve the NetTE conservative counter formula and whether simultaneous forward/reverse diagnostic retention is required;
5. decide whether ledger and reference-owned peak estimates are admission bounds only or require measured post-run attestation as well;
6. confirm that cases rejected by this envelope are excluded only from the current implementation coverage, not silently removed from the scientific target population.

If the approved resource limits exclude difficult or substantively important M6 cases, the comparison coverage and claim ceiling must be narrowed in the later manuscript and evidence ledger. Passing all admitted cases cannot establish behavior outside the approved envelope.

## 9. Claim ceiling

Even after approval and successful implementation, this envelope could establish only that the independent reference path fails closed before known resource hazards and preserves the enumerated/scheduled rows of admitted cases under a documented streaming contract. It cannot establish:

- M6 scientific validation or M6 completion;
- independent empirical superiority over comparator software;
- exchangeability, Type-I-error control, power or external validity;
- real-research usefulness or usability;
- complete platform, operating-system or dependency coverage;
- SoftwareX readiness, upload readiness, submission, acceptance or likely review outcome.

Until the section-8 decisions are approved and recorded, the controlling state remains:

```text
RESOURCE_ENVELOPE_REVISION_REQUIRED
NOT APPROVED
NOT FROZEN
NOT IMPLEMENTED
M6 NOT EXECUTED
```
