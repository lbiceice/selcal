# SelCal Input Resource Envelope v1

Status: `APPROVED_FOR_TDD_IMPLEMENTATION`

Approval: `批准输入资源上限方案1，继续设计并TDD实现`

Approval date: 2026-08-31

NPZ decompression amendment: `docs/architecture/input_resource_envelope_v1_1_amendment_proposal.md`

Amendment approval: `批准输入资源 envelope v1.1 修订案，开始 TDD 实现`

Amendment approval date: 2026-09-01

## 1. Purpose and claim boundary

This design adds a deterministic resource envelope before SelCal constructs CSV or NPZ
scientific inputs. It closes one engineering failure mode: a large or adversarial input must not
reach unbounded whole-file parsing, unbounded CSV field construction, or unbounded NPZ member
allocation before a resource decision is made.

This is an engineering and reproducibility contract. It does not establish statistical validity,
M6 scientific impact, platform-wide performance, security against a hostile operating system,
release readiness, licence compatibility, or SoftwareX submission readiness.

The public call signatures remain unchanged:

```python
load_csv(path, *, source_column, target_column, candidates)
load_npz(path, *, candidates)
```

There is no user-supplied limit override in v1. A later limit revision requires a new versioned
contract rather than silent mutation of these values.

## 2. Evidence for the envelope

The pre-change loader at `src/selcal/inputs.py` had SHA-256
`258f1cfe0e50feacbec54d63ce2039e797f8c9fb0a9d98023bd7947ca89eabf5`.
On CPython 3.11.12, Darwin arm64, NumPy 2.4.6, a local single-process pressure observation found:

| Format | Rows/elements per series | Raw bytes | Python allocation peak | Sampled RSS increase |
|---|---:|---:|---:|---:|
| CSV | 1,000,000 | 11,778,030 | 175,590,700 | 351,928,320 |
| NPZ | 1,000,000 | 16,000,510 | 56,054,307 | 57,163,776 |

These figures select a bounded product envelope and identify avoidable CSV amplification. They are
not portable performance guarantees. The CSV design therefore removes the full decoded string,
`splitlines()` list, and two Python-float lists. The NPZ design does not infer safety from compressed
archive size alone.

## 3. Exact limits

All integers below are normative.

| Reason code | Exact limit | Meaning |
|---|---:|---|
| `CSV_RAW_BYTES` | 67,108,864 | Maximum raw CSV snapshot bytes (64 MiB) |
| `CSV_RECORD_CHARACTERS` | 1,024 | Maximum Unicode code points in one record, excluding its normalized terminator |
| `CSV_FIELD_CHARACTERS` | 256 | Maximum parsed Unicode code points in one header or data field |
| `CSV_DATA_ROWS` | 1,000,000 | Maximum logical data records, excluding the header |
| `NPZ_RAW_BYTES` | 33,554,432 | Maximum raw NPZ snapshot bytes (32 MiB) |
| `NPZ_CENTRAL_DIRECTORY_BYTES` | 16,384 | Maximum declared central-directory bytes |
| `NPY_HEADER_BYTES` | 4,096 | Maximum declared NPY header bytes |
| `NPY_ELEMENTS` | 1,000,000 | Maximum elements in each source or target array |
| `NPZ_MEMBER_UNCOMPRESSED_BYTES` | 8,004,108 | Maximum complete NPY member bytes |
| `NPZ_TOTAL_UNCOMPRESSED_BYTES` | 16,008,216 | Maximum declared bytes across both NPY members |

`8,004,108 = 8 + 4 + 4,096 + (1,000,000 * 8)`: eight magic/version bytes, the
largest supported four-byte header-length field, the header limit, and the largest permitted
numeric payload. The total is exactly twice the per-member limit.

## 4. One-open bounded snapshot contract

Both loaders use one shared reader with this order:

1. Validate loader arguments and candidates exactly as before.
2. Open the path once with a non-blocking read flag where the platform exposes it.
3. Apply `fstat` to that open descriptor and reject anything that is not a regular file.
4. Read from the same descriptor in bounded chunks until EOF or `raw_limit + 1` bytes.
5. If `raw_limit + 1` bytes are observed, raise `ResourceLimitError` without reading further.
6. Compare a platform-defined descriptor identity before and after the read. On POSIX this is size,
   modification time, and metadata-change time (`st_ctime_ns`). On Windows, where Python documents
   `st_ctime_ns` as creation time rather than POSIX change time, v1 compares size and modification
   time and does not mislabel creation time as mutation evidence. Reject every change visible in the
   applicable identity as malformed input.
7. Close the descriptor. Hashing, format preflight, parsing, and array construction consume only
   the returned immutable `bytes`; they never reopen the path.

An atomic filesystem snapshot is not claimed. Path replacement after the descriptor is opened does
not redirect the descriptor to replacement bytes. If replacement or mutation changes any applicable
frozen identity field, loading fails closed with `ValueError`; link-count changes do not waive that
comparison. On POSIX, same-size writes that evade both `mtime` and `ctime` cannot be detected. On
Windows, same-size writes that restore `mtime` cannot be detected by this v1 contract because
creation time is not a change-time substitute. Callers must not mutate an input during loading.
Regardless, a successful raw hash and parser consume the same returned byte buffer and the loader
never reopens the path.

The reader returns immutable `bytes`. During final chunk joining, Python may temporarily retain both
the bounded chunk storage and the joined result, so the snapshot layer alone can approach twice the
raw cap plus allocator overhead (about 128 MiB for CSV or 64 MiB for NPZ). This is a fixed bound, not
streaming or an out-of-core claim, and it must be included in the post-change pressure observation.

## 5. CSV accepted grammar and order

CSV v1 is a deliberately restricted, reproducible two-field UTF-8 format:

- decoding is strict UTF-8;
- `newline=None` normalizes `LF`, `CRLF`, and `CR` to one `\n` terminator;
- each physical line is exactly one logical CSV record;
- quoted fields are allowed within a record, but CR or LF inside a quoted field is forbidden;
- the first record is the header and every later record is a data row;
- every parsed record has exactly two fields;
- the header fields are nonempty and unique;
- blank physical rows, repeated headers, missing fields, extra fields, blank cells, nonnumeric
  cells, nonfinite values, and nonzero values that underflow float64 remain errors.

The loader calls `TextIOWrapper.readline(CSV_RECORD_CHARACTERS + 1)` on an in-memory `BytesIO`
snapshot. For the header, it checks record length before calling `csv.reader`. For data, a non-EOF
read that would be data record `CSV_DATA_ROWS + 1` raises `CSV_DATA_ROWS` immediately, before the
buffer is tested for blankness, length, CSV structure, field length, or numeric content. For every
admitted data record, length is then checked before `csv.reader`, so a comma bomb cannot make the
CSV module construct an unbounded field list. `csv.reader((record,), strict=True)` parses only that
bounded record. Parsed field length is checked before float or `Decimal` conversion.

This priority is normative at intersections: `CSV_RAW_BYTES` precedes UTF-8 decoding; for an
admitted physical record `CSV_RECORD_CHARACTERS` precedes blank-row and CSV-structure errors; the
first non-EOF data read beyond `CSV_DATA_ROWS` precedes all record-local checks. The row reader may
therefore not reject a blank or overlong record before the caller has applied the data-row gate.
Valid numeric values are appended to two `array('d')` buffers, not Python-float lists, before
`SeriesPair` performs its existing immutable float64 normalization.

## 6. NPZ and NPY accepted grammar

NPZ v1 accepts a strict subset sufficient for NumPy-generated source/target archives:

- one conventional, single-disk ZIP archive with one unambiguous EOCD ending at the raw snapshot;
- no archive-level ZIP64 EOCD or ZIP64 locator;
- a central directory no larger than the exact limit and ending immediately before the EOCD;
- exactly two non-directory members whose logical names normalize from `source` or `source.npy`
  and `target` or `target.npy`;
- no duplicate logical name, path separator, NUL, encryption, or data descriptor;
- compression method `stored` or `deflate` only;
- local header and central-directory name, flags, method, CRC, compressed size, and uncompressed
  size must agree;
- NumPy's small-member local ZIP64 size extension is accepted only when a local 32-bit size is the
  ZIP64 sentinel and the extension resolves exactly to the ordinary central-directory size;
- member byte ranges must not overlap each other or the central directory.

The implementation uses one frozen ZIP route as amended by input-envelope v1.1. SelCal parses and
cross-checks EOCD, central and local headers itself. Stored members use their exact validated byte
ranges; deflate members use one public `zlib.decompressobj(wbits=-15)` with bounded output. A
second parser/decompressor route, `ZipFile` construction, `ZipExtFile`, private `zipfile` state,
`ZipInfo` mutation, and `decompressor.flush()` are forbidden.

EOCD and ZIP64 decisions are byte-exact:

- a conventional EOCD is the 22-byte fixed record plus its declared comment and must end exactly at
  the raw snapshot; exactly one such candidate may exist in the final 65,557 bytes;
- the 20 bytes immediately before the accepted EOCD must not carry the ZIP64 locator signature;
  any EOCD disk/count field equal to `0xffff` or size/offset field equal to `0xffffffff` is an
  archive-level ZIP64 sentinel and is rejected;
- every central and local extra area is a complete sequence of little-endian `header_id:uint16,
  data_size:uint16, data` fields; truncation or duplicate ZIP64 field `0x0001` is invalid;
- central-directory ZIP64 field `0x0001` is forbidden because all accepted central sizes and
  offsets are ordinary non-sentinel values under this envelope;
- a local ZIP64 field `0x0001` is present if and only if at least one local 32-bit size is
  `0xffffffff`. Its payload contains only the sentinel-backed values, in APPNOTE order:
  uncompressed size first when that field is sentinel, then compressed size when that field is
  sentinel. The payload length is therefore exactly 8 or 16 bytes. Each resolved value must equal
  the corresponding ordinary central-directory size. Offset and disk-start values are forbidden.

These rules accept the local ZIP64 size form emitted by the frozen NumPy 2.4.6 `savez` and
`savez_compressed` paths without admitting archive-level ZIP64 or ambiguous alternate layouts.

For each member:

1. A declared per-member or total uncompressed limit violation raises immediately.
2. Otherwise the exact stored range or one deflate state machine is consumed in bounded chunks
   under the approved v1.1 tail-first algorithm. Actual output reaching `limit + 1` raises a
   resource error and stops; CRC completion is not claimed for that rejected member.
3. A member that stays within the limit must reach EOF, match its declared size, and pass CRC.
4. NPY magic, version, and declared header length are checked before NumPy constructs an array.
5. Supported NPY versions are exactly 1.0 and 2.0. Version 3.0 is outside this simple numeric-array
   grammar and is rejected as a structural error.
6. The parsed shape must be one-dimensional with a nonnegative built-in integer length. The element
   limit is checked before array construction.
7. The original dtype kind must be signed integer, unsigned integer, or real float, with itemsize at
   most eight bytes. Object, pickle, boolean, complex, string, structured, and extended-float arrays
   remain forbidden.
8. Bytes after the header must equal `element_count * itemsize` exactly.
9. Independent NPY parsing starts at byte zero with `read_magic`; after it consumes the six magic
   bytes and two version bytes, `read_array_header_1_0` or `read_array_header_2_0` is called with the
   cursor exactly at offset eight, where the header-length field begins. Its final cursor must equal
   the independently calculated header end. Header-parser `ValueError`, `EOFError`, `struct.error`,
   `SyntaxError`, and Unicode decoding failures map to the stable structural `ValueError` class.
10. `np.load(BytesIO(member_bytes), allow_pickle=False, max_header_size=4096)` may run only after
    the independent preflight above. Its documented malformed-input exceptions map to stable
    structural `ValueError`; `MemoryError` and `ResourceLimitError` always propagate unchanged. This
    is a second header interpretation of the same bounded member, not a second decompression.

## 7. Exception and error-priority contract

Resource messages are path-free and have one of these exact forms:

```text
INPUT_RESOURCE_LIMIT_EXCEEDED_V1 reason=<CODE> limit=<INTEGER> observed=<INTEGER>
INPUT_RESOURCE_LIMIT_EXCEEDED_V1 reason=<CODE> limit=<INTEGER> observed_at_least=<INTEGER>
```

The exception matrix is normative:

| Condition | Exception |
|---|---|
| Invalid API argument or candidates | Existing `TypeError`/`ValueError` |
| Missing, unreadable, or permission-denied path | Original filesystem exception |
| FIFO, device, directory, or other non-regular input | `ValueError` |
| Detectable in-place mutation while reading | `ValueError` |
| Any exact resource ceiling exceeded | `ResourceLimitError` |
| UTF-8, CSV, ZIP, CRC, NPY, dtype, shape, or length structure invalid | `UnicodeDecodeError` or stable `ValueError` |
| `MemoryError` from Python, NumPy, or the operating system | Original `MemoryError` |

Resource checks intentionally precede deeper validity checks when both are true. A declared NPZ
member that is already over limit is rejected as a resource violation without decompression or CRC
work. If declared metadata is within limits but actual expansion reaches `limit + 1`, the resource
error wins and reading stops without claiming CRC completion. Only a member that stays within the
limit is read through EOF and must pass size and CRC checks. NPY preflight and `np.load` are forbidden
after a CRC/size failure. `MemoryError` and an already-raised `ResourceLimitError` are never caught by
the structural-exception mapping.

Resource failure is an execution-boundary failure. It must never be converted into an analytic
failure, `NOT_EVALUABLE`, a replicate failure, or a calibration result.

## 8. Module boundaries

```text
src/selcal/input_resources.py
    exact v1 limits, stable resource errors, one-open regular-file snapshot

src/selcal/npz_safe.py
    bounded ZIP metadata validation, one-pass member extraction, NPY preflight

src/selcal/inputs.py
    public LoadedInput orchestration, bounded CSV parsing, existing scientific validation
```

`input_resources.py` may depend on `contracts_v2.ResourceLimitError`; `contracts_v2.py` does not
import input modules, so no cycle is introduced. Moving the existing exception class would alter a
previously frozen v2 identity and is outside this change.

## 9. Test and verification gates

The TDD suite must cover real production paths for:

- all ten exact constants and both `8,004,108`/`16,008,216` derivation formulae;
- `limit - 1`, `limit`, and `limit + 1` helpers for each numeric limit, plus at least one real public
  `load_npz` path at each NPZ/NPY boundary class rather than helper-only proof;
- regular-file enforcement, a nonblocking FIFO rejection where supported, fail-closed detectable
  path replacement, and detectable in-place mutation; the FIFO case runs under an external timeout
  guard;
- multi-chunk success and a `limit + 1` failure reached on the second chunk, with exact read-request
  sizes and no read after the limit decision;
- POSIX-only ctime-change tests guarded from Windows, plus explicit platform-identity unit tests so
  creation time is never presented as Windows mutation evidence;
- comma bombs, overlong records, 256/257-character data fields, quoted embedded newlines, and
  LF/CRLF/CR/no-final-terminator boundaries at exactly 1,024 and 1,025 code points;
- exact data-row overflow competing with blank and overlong final rows, proving row-limit priority;
- false EOCD signatures in comments, ambiguous EOCD, excessive central directory, multi-disk and
  archive-level ZIP64 markers;
- duplicate, disguised, and traversal member names; encryption, unsupported compression, local and
  central header mismatch, overlap, truncation, and CRC damage;
- NPY header overflow, unsupported version, exact header-parser cursor placement, oversized declared
  shape, invalid dtype, wrong dimensionality, truncated data, trailing data, and the complete
  structural-exception/`MemoryError` classification matrix;
- CRC-damaged within-limit members proving that NPY preflight and `np.load` are not called, plus an
  actual-output `limit + 1` case proving that resource failure stops before CRC completion;
- unchanged raw and semantic hashes for equivalent valid inputs;
- propagation of filesystem errors and `MemoryError`;
- absence of any public limit override parameter.

Acceptance requires fresh focused tests, the existing input suite, the full non-Task10 core suite,
coverage, locked Ruff, strict mypy, repository hygiene, `git diff --check`, and a post-change local
pressure observation. The twelve known Task10 authority-amendment scope-v1 path-set failures remain
separate adverse evidence and are not modified by this scope.

## 10. Downstream status

Passing this design closes only the open code-smell item “CSV/NPZ input loading has no resource
caps.” It does not increase SoftwareX readiness by itself. Task10 scope-v2, hidden runtime state,
dependency/licence closure, M6 comparators and real-data evidence, UI, release, DOI, manuscript, and
submission remain separately gated.
