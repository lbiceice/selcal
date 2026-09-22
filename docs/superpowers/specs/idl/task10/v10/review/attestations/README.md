# Task 10 detached review attestations

Status: `APPEND_ONLY`

This directory records exact-byte review verdicts without changing the reviewed
registry or promoting it to scientific authority. Every record has effect
`NO_AUTHORITY_PROMOTION`.

## Roles

- The independent, read-only reviewer inspects frozen subject bytes and returns
  its identity, role, scope, verdict, finding counts, and independence statement.
  Identity, role, scope entries, and independence statement must each contain a
  non-whitespace character; blank provenance cannot close a PASS gate.
- The persistent implementation writer may materialize that returned result
  field-for-field. The writer must not reinterpret the verdict, alter counts,
  substitute reviewer identity, or widen scope.
- A writer self-check must use reviewer type `IMPLEMENTER_SELF_CHECK`; it cannot
  be represented as an independent PASS.

## Path and identity contract

Each attestation is stored at:

`sha256-<exact-registry-sha256>/review-<attestation-id>.json`

The record must bind the exact registry path/SHA-256 and exact registry-schema
path/SHA-256. It must also bind the complete reviewed package: the v1 registry
and matrix, v2 registry, both schemas, migrator, validator, concise index,
this README, and the focused test file. The fixed role set and repository-local
logical paths are closed by schema and rechecked against current file bytes.
A file that already exists is immutable. Never edit or overwrite it in place.

Validation has two explicit modes. `PREWRITE` requires the target not to exist
and prevents overwrite. After the writer creates the canonical JSON exactly
once, `READBACK` requires the target to exist and verifies that its bytes are
the canonical serialization of the same validated record. `READBACK` never
writes or replaces the file.

## Supersession

A later review creates a new file. If it supersedes an earlier verdict, its
optional `supersedes` binding names the exact prior repository-local attestation
path and SHA-256. Validation requires that prior file to exist, match the bound
digest, differ from the new attestation path, contain canonical schema-valid
attestation JSON, and bind the same exact registry subject. The prior file
remains present and unchanged.

## PASS rule

`PASS` requires zero blocker, major, minor, and total findings plus a non-empty
independence declaration. Review success closes only the stated review scope;
it does not amend authority, authorize IDL or KAT work, approve a release, or
make the software or manuscript submission-ready.

`created_at` is a real calendar timestamp in canonical UTC
`YYYY-MM-DDTHH:MM:SSZ` form; matching the textual shape alone is insufficient.
