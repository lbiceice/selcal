# Task 10 full provider-audit KAT manifest

Status: `DONE_WITH_CONCERNS`

This is a narrow rebind audit of authoritative specification SHA-256
`74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff`.
The newly added registry, anchor/top-level, finding, and canonical-literal rules
are closed. The complete machine reference IDL remains absent, so the two full
literal KATs were not attempted or fabricated.

## Authority and profile

- Sole authoritative specification:
  `docs/superpowers/specs/2026-08-29-task10-deny-by-default-provider-proof-design.md`
- Specification ordinary SHA-256 at audit start and final verification:
  `74891e7b1a5190d64da5d2fd74e8ef0d74e671fc81600875995c2dbc7ee057ff`
- Repository starting and ending HEAD:
  `94f993bfd5240739f23dd5f5309a51e51034b962`
- Normative and locally observed profile: CPython `3.12.10`; NumPy `2.2.6`.
- `task10-reference-schema-v10.json` remains excluded: it binds an older
  specification and declares itself a partial gap artifact, not authority.
- No production serializer, future implementation, test serializer, or policy
  value was used to fill an unspecified target table or discriminator.
- Domain envelope when a valid preimage exists:
  `SHA256(b"SELCAL-PROVIDER-AUDIT-V2\\0" + domain_utf8 + b"\\0" + canonical_bytes)`.

## Artifact identities

| Artifact | State | Exact byte length | Ordinary SHA-256 | Domain digest |
| --- | --- | ---: | --- | --- |
| `task10-provider-audit-policy-full-nonempty-v10.kat.json` | not created; blocked | `null` | `null` | policy: `null` |
| `task10-provider-audit-report-stable-full-wire-v10.kat.json` | not created; blocked | `null` | `null` | report: `null` |
| `task10-provider-audit-full-kat-coverage.json` | present; canonical single-line UTF-8 JSON plus final LF | `28063` | `7f1b5112f400ad2fa8f8c9191a2cdcda3141a2cc99760d343a35031dff38fb01` | not applicable |

Policy/report ordinary hashes and domain digests remain explicit `null`, not
placeholders. This manifest does not self-embed its mutable length or hash; they
are reported after final read-only verification.

## Real coverage state

- closed owner tables enumerated: 66/66;
- policy/report top-level keys enumerated: 84/84 and 75/75;
- actual typed fixture records: 0/66;
- blocked owner tables: 66/66;
- required full KAT files present: 0/2;
- prior/new gap codes fully closed: 19;
- partially closed/refined code: G14;
- unique open blocker: G18.

## Newly closed items

1. `G19_LABEL_DEFINITION_66_OWNER_CLOSURE` — closed. Sections 5.6.8 and
   5.6.8.1 freeze the exact 66-literal `ClosedOwnerTable`,
   `LabelDefinition(label,owner_table,record_ordinal,record_digest)`, complete
   table-manifest binding, and record label/digest equality.
2. `G20_ANCHOR_AND_TOP_LEVEL_RL_VALIDATION_MISSING` — closed. Section 5.6.1
   validates identity-anchor binding labels/owners/digests, root-function
   backlinks, and top-level copies independently. They do not enter the
   66-owner classification array or create authorization edges.
3. `G21_FINDING_SEMANTIC_AUTHORITY_MISSING` — closed. Section 5.4 is
   authoritative for full-wire and stable finding records, stable-key-only
   sorting and duplicate rejection, detail exclusion, and stable/detail
   mutation behavior; Section 5.6.10 repeats the same projection.
4. `G22_CANONICAL_LITERAL_RECURSION_BUDGETS_MISSING` — closed. Section 5.6.1
   freezes CL depth 32, 256 immediate members, 4096 total nodes, 1,048,576
   canonical UTF-8 bytes, cycle detection, iterative preflight, and focused
   failure categories for every CL occurrence.

## Unique open blocker

`G18_CLOSED_REFERENCE_ALIAS_AND_LEAF_IDL_NOT_IN_AUTHORITY` remains open.

The authority requires one pre-value `ReferenceFieldRule` for every RL leaf,
including owner table, containing branch/discriminator, field path,
cardinality, exact non-empty `allowed_target_tables` subset, kind, and schema
order. It supplies exact `Ref[...]` annotations only for value-normal-form and
selected site-manifest leaves, plus isolated prose targets. Many imported
migration-ledger and replacement records still contain bare RL/LS leaves with no
complete normative target-owner union or branch-discriminator row.

The complete 66-owner `LabelDefinition` registry validates ownership of labels
already present in a policy; it cannot define the reference schema before
policy values are read. Inferring targets from field names, discriminator
values, observed labels, or the registry would let policy values select schema
authority. Therefore an independent encoder cannot emit the complete
classification array, prove the derived graphs, or compute valid policy/report
bytes and digests without guessing.

Minimum closure: add to the authoritative specification a complete,
machine-readable reference alias/leaf catalog covering every RL leaf with all
`ReferenceFieldRule` fields and exact schema order.

## Independent method

The audit scanned only the authoritative Markdown, compared its exact owner and
top-level key lists with the coverage JSON, and independently checked the
accepted Python/NumPy profile. The coverage document was serialized as
recursively lexicographically sorted UTF-8 JSON with no insignificant whitespace
and exactly one final LF. No generator remains in the repository.

## Anti-false-green expectations retained

- omit, empty, or move any owner-table record after self-consistent redigestion:
  RED;
- mutate a reference target set, discriminator, kind, or ordinal: RED;
- derive a reference target from a policy value or label registry: RED;
- alter an anchor backlink, owner, record digest, or top-level RL copy: RED;
- exceed any CL cycle/depth/member/node/byte budget: focused RED;
- mutate finding detail: wire bytes change and stable digest does not;
- mutate a stable finding field: stable digest changes;
- duplicate stable key: construction error;
- bind a report to another policy/table/registry digest: RED;
- mutate any literal byte: ordinary hash and applicable domain digest change.

## Verification boundary

JSON parsing, canonical round-trip, 66/84/75 list extraction, profile checks,
ordinary hashing, absence checks, and whitespace checks validate this gap
artifact only. They do not close G18, create either KAT, or establish a
policy/report domain digest.
