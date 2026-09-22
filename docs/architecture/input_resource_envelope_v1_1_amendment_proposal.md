# SelCal input resource envelope v1.1 amendment proposal

Status: `APPROVED_FOR_TDD_IMPLEMENTATION / VERIFICATION_PENDING`

Proposal date: 2026-08-31

Approval: `批准输入资源 envelope v1.1 修订案，开始 TDD 实现`

Approval date: 2026-09-01

Parent specification: `docs/architecture/input_resource_envelope_v1_design.md`

## 1. Decision requested

Replace the NPZ member-decompression implementation route in v1 with a SelCal-owned,
single-pass bounded reader using only public `zlib` state for deflate and exact byte-range reads for
stored members.

This proposal changes an internal architecture choice. It does not change the public `load_npz`
API, the accepted NPZ/NPY grammar, any v1 resource limit, the exception-priority contract, input or
semantic hashes, or the scientific calibration result.

Approval authorizes test-first implementation only. Task 3 may not claim code-quality closure until
the amendment is implemented and independently re-reviewed.

## 2. Reason for amendment

The first Task 3 candidate passed its functional specification but required a copied and modified
`ZipInfo` plus CPython-private `ZipExtFile` state (`_compress_left`, `_compress_type`, and
`_decompressor`) to detect output hidden beyond a false declared size and to prove exact deflate
EOF. The package currently declares Python `>=3.11` without an upper bound. A future Python release
or another conforming implementation could therefore reject a legal archive, or change the meaning
of those private fields, while the package metadata still claims support.

Restricting SelCal to a short CPython version window would preserve the v1 implementation wording
but create a recurring compatibility-review burden and weaken SoftwareX portability. The proposed
route retains the security and resource semantics using public, documented decompressor state.

## 3. Normative replacement

The following text replaces the v1 requirement that `ZipFile.open()`/`ZipExtFile` be the single
decompressor.

1. SelCal's manual EOCD, central-directory, local-header, ZIP64, member-range, flag, method, CRC,
   name and size validation remains the authoritative security preflight over the one immutable raw
   snapshot.
2. Production code must not construct or call `ZipFile`, call `ZipFile.open()`, copy or mutate
   `ZipInfo`, inspect `ZipExtFile`, or access private `zipfile` fields. The manual bounded preflight
   is the one ZIP parser and the only source of member ranges supplied to extraction.
3. A stored member is read from its already validated exact `[data_offset, data_end)` range. After
   the declared-uncompressed-size gates have run, a stored compressed range reaching
   `NPZ_MEMBER_UNCOMPRESSED_BYTES + 1` raises the resource error before compressed/uncompressed
   equality, CRC or NPY checks. A within-limit stored member is then required to have equal
   compressed, declared-uncompressed and actual byte lengths before CRC or NPY parsing.
4. A deflate member creates exactly one `zlib.decompressobj(wbits=-15)`. Its validated compressed
   range is obtained once, in order, in chunks of at most 65,536 bytes. No second decompressor,
   archive reread or fallback route is permitted.
5. For each raw chunk, call `decompress(pending, max_length)` with a positive
   `max_length <= NPZ_MEMBER_UNCOMPRESSED_BYTES + 1 - observed`. If the call leaves
   `unconsumed_tail`, that exact tail becomes the next `pending` input and must be drained before a
   new raw chunk is obtained. A no-output/no-input-progress state is structural failure. No raw
   byte may be reread from the immutable snapshot, although bytes reported as not consumed by zlib
   are resubmitted from `unconsumed_tail`.
6. Reaching `NPZ_MEMBER_UNCOMPRESSED_BYTES + 1` raises the resource error immediately. CRC and NPY
   parsing are forbidden afterwards. Production code must never call `decompressor.flush()`;
   `flush(length)` does not impose a maximum returned-output length and is therefore not an
   accepted bounded operation.
7. A within-limit deflate member is accepted only when all bytes in the exact compressed range have
   been offered in order, no pending input remains, `eof` is true, `unused_data` and
   `unconsumed_tail` are empty, actual output length equals the validated declared length, and
   CRC-32 matches. Reaching `eof` before the exact compressed range ends, including through
   `unused_data`, is structural failure.
8. Existing rejection of data descriptors, encryption, archive-level ZIP64, ambiguous local ZIP64,
   unsupported methods, overlapping ranges, trailing archive bytes and malformed NPY members is
   unchanged.
9. `MemoryError` and `ResourceLimitError` continue to propagate unchanged. `zlib.error` remains a
   stable structural `ValueError`. Resource-limit priority over CRC, NPY and scientific validation
   is unchanged.

## 4. Required RED tests before implementation

The revised implementation must begin with tests that fail against the current candidate:

- a legal stored and compressed NPZ load when construction of `ZipFile` is forbidden;
- production source contains no private `ZipExtFile` state access and no copied or modified
  `ZipInfo`;
- one and only one public deflate decompressor is created for each deflated member;
- no compressed input chunk exceeds 65,536 bytes and no output request can cross `limit + 1`;
- a spy fails if `flush()` is called, new raw input is obtained before `unconsumed_tail` is drained,
  or a decompression output request is zero, negative or larger than the remaining allowance;
- high-ratio output stops exactly at `limit + 1`, before CRC and NPY work;
- missing true deflate EOF and bytes after a complete deflate stream are rejected before CRC/NPY;
- stored and deflate actual/declared length disagreements are rejected before CRC/NPY;
- a stored member whose compressed range reaches `limit + 1` while its declared uncompressed size
  is within limit raises the resource error, not structural `ValueError`;
- `zlib.error` maps to stable `ValueError`, while `MemoryError` propagates;
- valid `savez` and `savez_compressed` fixtures preserve values, raw hashes and semantic hashes;
- the existing hidden-output regression remains effective without asserting `ZipInfo` mutation.

## 5. Verification and claim boundary

After RED-to-GREEN implementation, run the full input suite, repository suite excluding the
separately held Task-10 scope-v1 route, Ruff, strict mypy, package build, clean installation, and
the finite Task 3 compatibility matrix below. Retain adverse failures and rerun the exact
source-bound audit.

The finite interpreter/library matrix is:

- CPython 3.11 with NumPy 1.26.4 and the locked NumPy 2.4.6;
- CPython 3.12 with NumPy 1.26.4 and the locked NumPy 2.4.6;
- CPython 3.13 with the newest installable NumPy 2.x observed at the verification checkpoint;
- CPython 3.14 with the newest installable NumPy 2.x observed at the verification checkpoint.

Each environment must record exact Python, NumPy, operating-system and architecture identity. An
unavailable combination remains `UNVERIFIED`; it is not converted to a pass by narrowing the test.
This finite matrix is Task 3 compatibility evidence only. The package's broad dependency metadata
does not imply that future Python or NumPy releases have been tested, and same-machine runs do not
establish cross-platform support. A release support matrix remains a later explicit gate.

Passing this amendment closes only the NPZ implementation-quality issue. It is not M6 scientific
evidence, a cross-platform result until the matrix actually runs, release approval, SoftwareX
manuscript readiness, or submission evidence.
