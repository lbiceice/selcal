# Task 10 Slice 2 deny-by-default provider proof correction

**Status:** eleventh written revision resolving the tenth-revision fixture,
reference-typing, value-wire, provider-graph, mutation, and implementability findings; pending
exact-fixture closure, exact-hash rereview, and user review;
implementation is not authorized
**Parent design:**
`docs/superpowers/specs/2026-08-28-task10-cross-module-operation-capsules-design.md`
**Repository base commit:**
`94f993bfd5240739f23dd5f5309a51e51034b962`; the Slice 2 production/test
candidate remains uncommitted, and this design does not treat the base commit
as its source identity. Exact current source hashes are frozen later by each
root policy and same-byte verification.
**Scope:** the Slice 2 auxiliary RNG-independence proof for the exact oracle and
v1-to-v2 migration entry points. This document does not replace or close the
parent design's Section 4 whole-production-root proof, which remains assigned
to Slice 4.

## 1. Status and scope correction

The existing `_random_behavior_graph_v2.py` is an auxiliary Slice 2 test
helper. Its two roots are:

- the exact finite-state reference oracle; and
- the v1-to-v2 migration entry point.

It does not root the public calibrator, private executor, terminal gate, sealed
verifier, random/selector/statistic/null leaves, or every canonical
registration. Those production roots remain governed by the parent design and
the future `_task10_trusted_graph_v2.py` Slice 4 proof.

Accordingly, this correction proves a frozen-current-byte RNG-independence
property for two reference/migration roots. It does not independently prove the
parent post-seal rebinding property, recursive production zero-global property,
or whole-graph external-leaf closure. Those stronger gates are neither waived
nor inferred from this auxiliary PASS.

## 2. Adverse evidence and selected direction

The current helper repeatedly returned an empty finding set while a mutation
made a production entry point execute non-canonical random behavior. Confirmed
carriers include:

- alternate capsules and opaque builders;
- partials, bound methods, callable instances, class attributes, slots,
  properties, instance/class/static methods, metaclasses, and constructors;
- exact and custom containers, `UserDict`, list/dict subclasses,
  object-dtype arrays, and `GenericAlias` factories;
- NumPy ufunc/C-state callbacks, private PCG64 providers, and
  `random.Random().random`;
- literal, aliased, and dynamically named `getattr`; and
- `vars`, `__import__`, `eval`, and `exec` resolution paths.

The candidate nevertheless passed 1,254 Task 5 tests and 2,435 repository tests
with 95.06% branch coverage. Those green results cannot carry the helper's
absolute test names.

The selected correction is a **closed-world, deny-by-default, root-specific
capability proof**. It traverses project-owned Python behavior and accepts an
external call only when an independently bootstrapped exact identity is
authorized for one frozen callsite and one frozen argument/outcome contract.
Every other behavior-bearing value fails closed.

Continuing to add carrier-type cases is rejected. Runtime monkeypatching and
profiling remain supplemental attacks because Python profiling misses native
and C-state behavior. This correction includes a two-root, fail-closed AST
value-provenance analyzer only to verify callsite receiver and argument
contracts. It is not the Slice 5 selector/dispatch taint analyzer: it has no
adapter-name lattice, no dispatch-sink model, no general interprocedural
promise, and every unsupported syntax/value becomes `UNKNOWN` and fails.

## 3. Temporal boundary and claim ceiling

The proof report binds one audit run to:

- exact root function identities and source hashes;
- exact trusted project module objects, globals dictionaries, origins, and
  source hashes;
- a clean external-identity bootstrap hash;
- exact root-input and callsite-capability manifests;
- Python and NumPy versions; and
- the graph/abstract-interpreter limits, audit implementation hash, and one-use
  parent challenge nonce.

Changing a bound source file, module object, globals dictionary, default,
descriptor, manifest, container, or external identity invalidates the report
and requires a fresh audit. The child recomputes every referenced binding,
root-state, namespace, generated-artifact, and external-state digest after
traversal, emits one nonce-bound report, and exits. The parent consumes the
report immediately in the same test transaction. Only hashes,
counts, findings, versions, and exit evidence may be persisted; a prior report
is never a reusable PASS for later process state.

Ordinary post-seal rebinding resistance remains established by the production
capsule attack tests and, later, the Slice 4 whole-root proof. Direct mutation
of function code or closure cells, `ctypes`, native memory, a hostile initial
interpreter, and compromised Python/NumPy binaries remain outside the parent
threat model.

The maximum Slice 2 auxiliary claim is:

> For the exact frozen source graph and reviewed root abstract contracts,
> including every syntactic branch admitted by the closed transfer table and
> the exact structured-root identities named by those contracts, every
> behavior-bearing provider frontier reachable from the exact-oracle and
> migration roots is either project-owned and recursively audited or
> authorized by one root-specific, callsite-specific external capability. No
> forbidden or unapproved random provider is present in that bounded graph.

This claim does not cover a same-valued replacement structured instance, an
input state outside the declared atomic/container/array domains, a future
source version, or every legal runtime value accepted by a public API. It is
not a sandbox, security proof, whole-production graph proof, scientific
validation, release qualification, or SoftwareX readiness statement.

## 4. Two-phase trust bootstrap

### 4.1 External identity bootstrap

A small test-only bootstrap module is imported in a fresh subprocess before
any `selcal` module. Under the trusted-initial-interpreter assumption it freezes
literal object references for:

- approved built-in, standard-library, and NumPy identities;
- forbidden random-provider identities;
- forbidden dynamic-resolver identities; and
- Python/NumPy version metadata, distribution roots, and exact source/binary
  digests for approved external providers.

The bootstrap accepts no root, project module, callable bundle, module export
sweep, `vars`, `dir`, or discovery callback. It cannot derive permissions from
the candidate under audit. Its canonical metadata serialization is hashed; raw
`id()` values are process-local evidence and are not serialized as stable
identifiers.

Fresh-process tests prove the bootstrap precedes every `selcal` import. A
provider already compromised before this bootstrap is a hostile initial
interpreter and remains explicitly out of scope.

All stable audit digests use `AUDIT-CANONICAL-JSON-V2`: UTF-8 JSON with
`ensure_ascii=False`, `allow_nan=False`, `sort_keys=True`, and separators
`(',', ':')`. The accepted value grammar is `null`, exact `bool`, bounded exact
`int`, exact `str`, `{"$float":"<float.hex()>"}`, finite
`{"$complex":["<real.hex()>","<imag.hex()>"]}`,
`{"$bytes":"<lowercase hex>"}`, `{"$label":"<literal manifest label>"}`,
`{"$ellipsis":true}`, `{"$tuple":[...]}`,
`{"$list":[...]}`, `{"$frozenset":[...]}` with members ordered by their
canonical bytes, `{"$dict":[["<exact string key>",value],...]}` with keys
ordered by UTF-8 bytes, and
`{"$ndarray":{"dtype":"<dtype.str>","shape":[...],"strides":[...],
"hasobject":<bool>,"writeable":<bool>,"content":"<digest>"}}`. Bare JSON
arrays are used only as ordered fields inside these tags or normative schema
records, never to encode a Python container. Bare JSON maps are used only for
normatively named schema fields. `$`-prefixed user keys and duplicate map keys
are rejected so tags cannot collide. Strings must encode with strict UTF-8;
unpaired surrogates fail and Unicode is not normalized. Every digest is
`SHA256(b"SELCAL-PROVIDER-AUDIT-V2\0" + domain_utf8 + b"\0" +
canonical_bytes)`. Raw object ids, `repr`, unordered iteration, absolute
temporary paths, and provider-controlled names are excluded. Cycles are not
recursively serialized: every permitted non-atomic value must already have one
literal manifest label, and the canonical form uses that label. Duplicate or
unlabelled referents fail bootstrap.

`domain_utf8` is exactly one of `bootstrap`, `runtime-binary-anchor`,
`external-state`, `code-record`, `project-module`, `project-source-index`,
`project-class`, `generated-artifact`, `generated-method`,
`generated-field-accessor`, `project-descriptor`, `external-type-member`,
`external-class`, `external-abc-state`, `external-python-intrinsic`,
`behavior-slot-manifest`,
`value-contract`, `value-contract-table`, `argument-contract`,
`result-contract`, `iterable-contract`, `root-input-contract`,
`project-function-manifest`, `callsite-manifest`, `capability-manifest`,
`root-syntax-inventory`, `runtime-locator`, `located-bound-callable`,
`runtime-value`, `state-field`, `process-local-identity-source`,
`process-local-identity-token`,
`runtime-state-scc`, `authorization-dependency-graph`,
`runtime-state-reference-graph`, `generated-callback`, `bound-member`,
`state-operation-transfer`,
`outcome-contract`, `exception-contract`, `exception-manifest`,
`semantic-guard`, `semantic-normal-transfer`, `semantic-exception-transfer`,
`semantic-model`, `semantic-model-manifest`, `intrinsic-effect`,
`protocol-manifest`, `operator-manifest`, `site-pairing-manifest`,
`interpreter-opcode-profile`, `provider-opmap`, `audit-state-read`, `array-content`,
`label-registry`, `identity-anchor-registry`, `root-scope-registry`,
`package-root-registry`, `policy-record`, `policy-table`,
`policy-table-manifest`, `site-key-table`, `value-expression`,
`provenance-requirement`, `cross-record-reference-classifications`,
`project-code-analysis`, `mutation-rebaseline`, `attack-recipe`,
`safe-control-recipe`, `attack-spec`, `root-invocation-trace`, `attack-witness`,
`source-bundle`, `fixture`, `attack-spec-core`, `trace-nonce-commitment`,
`patch-blob`, `patch-operation`, `patch-set`, `process-identifier-token`,
`python-call-trace`, `native-transition`, `performance-sample`,
`performance-characterization`,
`implementation`, `policy`, `root-state`, or `report`. Any
other domain label is a schema error. A repository file/source SHA-256 remains the ordinary digest
of its exact bytes and is inserted as a lowercase-hex field; it is not silently
re-domain-hashed.

`RuntimeBinaryAnchor` freezes two candidate installation roots in order:
`PREFIX = Path(sys.prefix).resolve(strict=True)` and
`BASE_PREFIX = Path(sys.base_prefix).resolve(strict=True)`, collapsing equal
roots while retaining the first label. The resolved regular file at
`sys.executable` is mandatory. A reported `LIBRARY`/`LDLIBRARY` is included
only when joining the exact `sysconfig` library-directory field and literal
library name resolves to an existing regular file. Each file is assigned to
the longest candidate root that contains it; equal-length ties use the root
order above. A file outside both roots fails bootstrap. Duplicate resolved
files are collapsed in executable-then-library order. Each canonical record is
exactly `(file_kind, installation_root_kind, relative_posix_path, size,
sha256)`; absolute roots, symlink spellings, and temporary paths are omitted.
A built-in provider binds this complete anchor, not an
implementation-selected binary.

An external callable with Python-visible or C-state behavior is not rejected
merely because state exists, and is not trusted merely because it is a NumPy
object. Its literal entry selects one normative `ExternalStatePolicy`:

- `IMMUTABLE_BUILTIN`: exact built-in identity and provider binary digest;
- `PYTHON_FUNCTION`: code, defaults, keyword defaults, closure, and referenced
  binding digests;
- `NUMPY_DISPATCHER`: exact literal module export, wrapped-function digest,
  dispatcher implementation digest, and full bootstrap-visible state digest;
- `NUMPY_UFUNC_EXPORT`: exact literal module export, NumPy extension-binary
  digest, and canonical `nin/nout/nargs/ntypes/types/identity/signature`
  digest;
- `BINARY_EXPORT`: exact literal module export, distribution version, extension
  binary digest, and entry-specific public-state digest;
- `TYPE_MEMBER`: exact owner external type, exact literal class-dictionary
  member name/identity/kind, owner source-or-binary anchor, and member
  code/state digest;
- `STRUCTURED_INSTANCE`: exact already-labelled external instance/type,
  complete literal instance-dictionary/slot state, exact type-member bindings,
  and for weak references exact referent/callback identities;
- `EXTERNAL_CLASS`: exact external class/type-operand identity, literal
  module/export source, metaclass, bases/MRO, complete class-namespace snapshot,
  and exact `__instancecheck__`/`__subclasscheck__` dependencies; it grants only
  a type operand and never construction;
- `MODULE_NAMESPACE`: exact module identity, `__spec__.name`, resolved
  source-or-extension origin, source/binary digest, and only the ordered
  literal attribute-name to already-labelled-identity mappings referenced by
  `NamespaceAttributeCapability`; or
- `NOT_APPLICABLE`: permitted only for a forbidden-only identity and carrying
  no trusted state.

Every state field used by an entry is named literally in that entry; discovery
by `dir`, an export sweep, or iteration of an object/module dictionary is
forbidden. Static lookup first uses `inspect.getattr_static` for Python objects
or an exact module-dictionary lookup for `MODULE_NAMESPACE`. A descriptor is
invoked only in the clean bootstrap when its exact type/identity and the
entry's `StateFieldAccessor` match; module `__getattr__`, a candidate
descriptor, equality, or hashing is never executed. The policy-specific
schemas are closed:

- `IMMUTABLE_BUILTIN`: identity label plus the complete
  `RuntimeBinaryAnchor`; `state_fields=()`;
- `PYTHON_FUNCTION`: canonical code record, positional defaults, keyword
  defaults sorted by literal keyword, closure cells in `co_freevars` order,
  the literal referenced-binding name list, and the exact literal sorted key
  set/content of the function's exact built-in `__dict__`. A canonical code
  record holds Python version, positional-only/positional/keyword-only counts,
  flags, stack size, bytecode hex, exception-table and line-table hex,
  first line, name/qualname, names, variable/free/cell names, and recursively
  encoded constants; nested code is
  encoded by the same rule, while every other non-atomic constant must already
  have a label. A code/default/closure cycle becomes
  `EXTERNAL_STATE_DRIFT`, not a back-reference invented by the implementation.
  The literal referenced-binding list must equal every `LOAD_GLOBAL`,
  `LOAD_NAME`, and `LOAD_DEREF` in the function and all nested code, recorded as
  `(code_digest, instruction_offset, opcode, literal_name, ordinal)` in
  bytecode order. There is no "provider-relevant" semantic filter; an
  independent bytecode scan rejects omissions, extras, aliases, or order drift;
- `NUMPY_DISPATCHER`: the exact literal export with mandatory intrinsic fields
  `('__module__','__name__','__qualname__','__wrapped__','_implementation')`;
  callable fields require an already-labelled identity and code/state digest,
  and an exact built-in `__dict__` requires its literal complete sorted key
  set/content to match. `__wrapped__ is _implementation` is mandatory for the
  current approved dispatchers; the implementation callable's complete
  `PYTHON_FUNCTION`/`BINARY_EXPORT` state and all recursive `LOAD_GLOBAL`,
  `LOAD_NAME`, and `LOAD_DEREF` bindings are frozen by the exact record above;
- `NUMPY_UFUNC_EXPORT`: the exact literal export and the fixed ordered fields
  `nin,nout,nargs,ntypes,types,identity,signature`, followed by the NumPy
  extension-binary anchor. The `types` field uses the bounded canonical-by-value
  container-snapshot accessor below because current NumPy returns a fresh exact
  `list[str]` on each read; object identity is neither expected nor authorized;
- `BINARY_EXPORT`: the exact literal export, literal public field list,
  distribution name/version, and resolved extension file size/SHA-256;
- `TYPE_MEMBER`: exact owner-type identity and module/export binding, exact
  class-dictionary lookup of one literal member, exact descriptor kind
  (`PYTHON_FUNCTION`, `PROPERTY`, `METHOD_DESCRIPTOR`, `WRAPPER_DESCRIPTOR`,
  `MEMBER_DESCRIPTOR`, or `GETSET_DESCRIPTOR`), and either the complete Python
  function state or owner extension-binary anchor;
- `STRUCTURED_INSTANCE`: exact instance/type identity, literal complete
  built-in `__dict__` key set/content and declared slots, exact bound member
  labels, and no undeclared mutation. A weakref additionally freezes exact
  referent/callback labels and schedules a non-`None` callback as behavior; and
- `EXTERNAL_CLASS`: exact module dictionary lookup of the literal export,
  exact class/metaclass identities, ordered base and MRO labels, a complete
  canonical class-namespace key/content snapshot, one mandatory
  `ExternalAbcStateBinding` whenever the metaclass is exact `ABCMeta`,
  and separately labelled instance/subclass-check semantic models and outcomes;
  no constructor, attribute, subclass mutation, registration, or factory
  permission follows from this state policy; and
- `MODULE_NAMESPACE`: the fixed module fields and the ordered capability-used
  literal attribute mapping only. It does not hash or authorize any other
  export.

`IMMUTABLE_BUILTIN`, `PYTHON_FUNCTION`, and `NOT_APPLICABLE` require empty
`state_accessors`; their intrinsic fields and exact built-in state dictionary,
when specified above, are read by the fixed policy logic.
For `NUMPY_DISPATCHER`, `NUMPY_UFUNC_EXPORT`, `BINARY_EXPORT`, `TYPE_MEMBER`,
`STRUCTURED_INSTANCE`, `EXTERNAL_CLASS`, and `MODULE_NAMESPACE`,
`state_accessors` must have the
same names and order as the policy's exact field list, with no duplicates. This
is a construction-time matrix check, not best-effort runtime behavior.
Every safe or namespace entry has a non-null 64-hex `state_digest`, including
the canonical empty-state digest when its closed policy has no mutable fields.
Only `FORBIDDEN_ONLY/NOT_APPLICABLE` has `state_digest=null`; an empty string is
never legal. This is checked before disposition use.

Bootstrap state serialization accepts only canonical atomic values, identities
already labelled in the bootstrap, or one explicitly bounded canonical-by-
value container snapshot accessor. Missing, extra, unlabelled, or
changed declared state fails. An implementation may not add a field after
observing candidate state; any required field is a specification change.
"Extra" here means an unexpected key in an exact state dictionary or an
unexpected field in a fixed policy schema. `MODULE_NAMESPACE` deliberately
does not assert that unrelated module exports are absent; it proves only the
authorized literal attribute mappings and forbids every bare/dynamic module
use.
`numpy.frompyfunc` results and arbitrary instances cannot qualify because they
are not the frozen literal export identity. Unobservable mutation of a trusted
external binary's internal memory is external-provider compromise and remains
out of scope; broad type or metadata-only exemptions remain forbidden.

For an `ABCMeta` class, `_abc_impl` is not serialized by introspecting the
opaque `_abc._abc_data` object. The bootstrap performs an exact class-dictionary
lookup of `_abc_impl`, verifies its exact `_abc._abc_data` type and live
identity, and binds one `ExternalAbcStateBinding`. That record freezes the
resolved `_abc` extension-binary anchor and the canonical projection of exact
`_abc._get_dump(cls)`: registry, positive cache, and negative cache are ordered
arrays of already-labelled live weak-reference referents; dead or unlabelled
weakrefs fail; the cache-version integer is bounded and exact. The `_abc_impl`
identity itself is represented only by its bootstrap label. The dump is read
before and after every instance/subclass-check model and must match. There is
no generic opaque-member serializer and no permission to call `_abc` mutation
functions such as `register` or cache reset. For a non-`ABCMeta` class the ABC
binding field is exactly `null`; for exact `ABCMeta` it is mandatory and
non-null, so a legal `collections.abc.Mapping` entry cannot omit the state that
controls `isinstance`.

### 4.2 Project binding

After `selcal` imports, every trusted project module is bound by a literal
`ProjectModuleBinding`. A project function is owned only when all of these hold:

- its exact module object is in the root's project-module manifest;
- `function.__globals__ is binding.globals_dict`;
- `binding.globals_dict is binding.module.__dict__`;
- the module spec origin and resolved function source realpath are under the
  frozen package root; and
- the current source SHA-256 equals the literal expected hash.

Origins and source paths use `resolve(strict=True)`, must be regular files, and
must be relative to the frozen package root. For an ordinary project-owned
function, the resolved source file equals its defining module's resolved spec
origin.

Generated dataclass, named-tuple, and enum-class methods, slot/member
descriptors, tuple getters, and metaclass-generated member maps are not
ordinary project functions and are never accepted by type
alone. One literal `GeneratedProjectArtifactBinding` may bind an exact project
dataclass, named-tuple class, or enum class only when its defining class is in
a bound project module and every artifact-kind-specific identity, source hash,
Python version, class recipe, field recipe, generated code digest, and
descriptor/getter record in Section 5.1 matches. A matched generated
dataclass init is interpreted as ordered field transfer and, for frozen
classes, the exact `object.__setattr__` operation. A matched named-tuple
`__new__` is interpreted as its exact finite field/index transfer. Neither is
trusted as opaque code. A matched enum uses only its frozen member recipe and
separate metaclass capabilities. A matched slot descriptor or tuple getter may read
only its literal field/index from an exact receiver covered by the declared
structured-value contract. `__post_init__`, validators, factories, default
factories, custom tuple-subclass behavior, and every undeclared generated
method remain separately traversed project/external behavior.

`function.__module__`, `__qualname__`, and `co_filename` are diagnostic data,
not sufficient trust evidence.

## 5. Frozen schemas

The implementation uses frozen, slot-based records. The following fields are
normative; an implementation plan may choose `NamedTuple` or
`dataclass(frozen=True, slots=True)` without changing them.

### 5.1 External identity and project module records

`ExternalDisposition` is the closed enum `SAFE_VALUE | SAFE_CALLABLE |
SAFE_FACTORY | SAFE_TYPE_OPERAND | NAMESPACE_ROOT | FORBIDDEN_RANDOM |
FORBIDDEN_DYNAMIC`.
`ExternalRole` is the closed enum `READONLY_VALUE | PURE_CALL |
CONSTRAINED_FACTORY | TYPE_CHECK_ONLY | NAMESPACE_ONLY | FORBIDDEN_ONLY`.
`ExternalStatePolicy` is the closed enum `IMMUTABLE_BUILTIN |
PYTHON_FUNCTION | NUMPY_DISPATCHER | NUMPY_UFUNC_EXPORT | BINARY_EXPORT |
TYPE_MEMBER | STRUCTURED_INSTANCE | EXTERNAL_CLASS | MODULE_NAMESPACE |
NOT_APPLICABLE`.

`ExternalIdentityEntry` contains:

- `label: str`;
- `value: object`;
- `disposition: SAFE_VALUE | SAFE_CALLABLE | SAFE_FACTORY | SAFE_TYPE_OPERAND |
  NAMESPACE_ROOT | FORBIDDEN_RANDOM | FORBIDDEN_DYNAMIC`;
- `role: READONLY_VALUE | PURE_CALL | CONSTRAINED_FACTORY | TYPE_CHECK_ONLY |
  NAMESPACE_ONLY | FORBIDDEN_ONLY`;
- `reason: str`;
- `reference_token: str`;
- `provider_module: str`;
- `qualified_name: str`;
- `identity_category: str`;
- `state_policy: ExternalStatePolicy`;
- `state_fields: tuple[str, ...]`;
- `state_accessors: tuple[StateFieldAccessor, ...]`;
- `state_digest: str | None` (`None` only for a forbidden-only
  `NOT_APPLICABLE` entry; every safe/namespace entry has a 64-hex digest);
- `python_version: str`;
- `numpy_version: str | None`;
- `source_sha256: str | None`;
- `binary_sha256: str | None`; and
- `root_scope: tuple[str, ...]`.

`StateFieldAccessor` contains one literal field name, one `EXACT_DICT_LOOKUP |
EXACT_INSTANCE_DICT_LOOKUP | EXACT_MEMBER_DESCRIPTOR |
EXACT_GETSET_DESCRIPTOR | EXACT_BOUNDED_CANONICAL_CONTAINER_SNAPSHOT` mode,
optional exact descriptor identity label, and exactly one expected canonical
atomic/manifest-label result or expected value-contract label.
`EXACT_DICT_LOOKUP` is legal only for an exact Python function dictionary,
external-class namespace, or `MODULE_NAMESPACE`; `EXACT_INSTANCE_DICT_LOOKUP`
is legal only for the already-labelled exact external instance/type named by
the entry. `EXACT_BOUNDED_CANONICAL_CONTAINER_SNAPSHOT` accepts only an exact
built-in tuple/list/dict with an independently declared maximum length and
atomic item/key/value contracts, canonicalizes by value without retaining
identity, and requires identical pre/post canonical bytes. It is mandatory for
`NUMPY_UFUNC_EXPORT.types`; a fresh equal list is valid, while a changed item,
order, type, length, or oversized snapshot is drift.
Descriptor modes require the literal exact
external type and descriptor identity to match before the trusted bootstrap
invokes that descriptor. No generic `getattr` or fallback lookup is permitted.

`ProjectModuleBinding` contains:

- `label: str`;
- `module: ModuleType`;
- `globals_dict: dict[str, object]`;
- `resolved_origin: str`;
- `source_sha256: str`; and
- `root_scope: tuple[str, ...]`.

`ProjectSourceIndex` contains one literal label, one project-module label, the
full parsed-module AST digest, and ordered mappings from exact function/code
digest to lexical qualified path plus
`(lineno,col_offset,end_lineno,end_col_offset)`. It is
built by parsing the already hash-verified complete module source, never by
`inspect.getsource(function)`. Ordinary and nested functions, lambdas, and the
implicit code objects of every `ListComp`, `SetComp`, `DictComp`, and
`GeneratorExp` must map one-to-one by code digest, `co_firstlineno`, lexical
nesting, AST kind/ordinal, and bytecode name. A comprehension record also
freezes its outer iterable expression, ordered generator targets/filters,
captured-environment labels, and nested-code digest. Zero or multiple matches
are `PROJECT_BINDING_DRIFT`. Generated `<string>` code is excluded from this
index and must use a generated-artifact or generated-callback binding below.

`ProjectClassBinding` contains literal label/root scope, project-module and
source-index labels, exact class-statement AST digest and lexical path, exact
class identity, `ORDINARY | EXCEPTION | RUNTIME_PROTOCOL` kind, ordered exact
base-class labels, exact metaclass label, the complete literal set of
class-dictionary members read by the audited roots, member values as atomic or
binding labels, one complete `BehaviorSlotManifest` label, and constructor/
instance-check semantic-model and outcome labels. `EXCEPTION` additionally
freezes the exact exception MRO and inherited
constructor provider. `RUNTIME_PROTOCOL` additionally freezes runtime-checkable
state and the exact metaclass `__instancecheck__` dependencies. Ordinary
project classes, project exception classes such as `PlanMigrationRefusal`, and
runtime Protocol classes cannot be represented as external safe terminals or
as an unbound `PROJECT_CLASS`. A changed base, metaclass, class member, MRO,
behavior slot, protocol flag, or constructor dependency is
`PROJECT_CLASS_BINDING_DRIFT`.

`BehaviorSlotManifest` contains a literal label, project-class label, exact
Python version, and one ordered `BehaviorSlotEntry` for every name in the
closed slot universe
`__new__,__init__,__getattribute__,__getattr__,__setattr__,__delattr__,
__get__,__set__,__delete__,__del__,__call__,__iter__,__next__,__len__,
__length_hint__,__reversed__,__bool__,__hash__,__eq__,__ne__,__lt__,__le__,
__gt__,__ge__,__contains__,__getitem__,__setitem__,__delitem__,__missing__,
__pos__,__neg__,__invert__,__index__,__int__,__float__,__complex__,
__add__,__radd__,__iadd__,__sub__,__rsub__,__isub__,__mul__,__rmul__,
__imul__,__matmul__,__rmatmul__,__imatmul__,__truediv__,__rtruediv__,
__itruediv__,__floordiv__,__rfloordiv__,__ifloordiv__,__mod__,__rmod__,
__imod__,__pow__,__rpow__,__ipow__,__lshift__,__rlshift__,__ilshift__,
__rshift__,__rrshift__,__irshift__,__or__,__ror__,__ior__,__xor__,__rxor__,
__ixor__,__and__,__rand__,__iand__,__enter__,__exit__,__instancecheck__,
__subclasscheck__,__class_getitem__,__mro_entries__,__array__,__array_ufunc__,
__array_function__,__format__,__str__,__repr__`. Each entry freezes
`ABSENT | INHERITED | OWN`, the exact defining
MRO-class label when present, raw class-dictionary identity label, and exact
project/external member-model label. The current two roots require a literal
`ABSENT` non-trivial `__del__` for every constructible result class and forbid
`weakref.finalize`; therefore no implicit finalizer is executed or silently
ignored. A runtime-added `__del__`, changed inherited slot, or undeclared
protocol hook fails preflight. Future support for a non-trivial finalizer
requires a `FINALIZE` intrinsic effect and separate design revision.

`ExternalClassBinding` contains a literal label/root scope, exact external
identity-entry label using `SAFE_TYPE_OPERAND/TYPE_CHECK_ONLY/EXTERNAL_CLASS`,
literal provider-module and export name, exact class and metaclass identities,
ordered base/MRO identity labels, complete canonical class-namespace snapshot,
mandatory `ExternalAbcStateBinding` for exact `ABCMeta` (otherwise null), and
exact instance/subclass-check semantic-model and
outcome labels. It is the sole type-operand route for real calls such as
`isinstance(value, collections.abc.Mapping)` and cannot be consumed by a call,
constructor, attribute, or factory capability.

`GeneratedMethodRecord` contains a literal label, owner-artifact label,
class-dictionary name,
`PYTHON_FUNCTION | STATICMETHOD | CLASSMETHOD | DATACLASS_INIT |
NAMEDTUPLE_NEW | NAMEDTUPLE_METHOD | ENUM_GENERATED` kind, exact raw
class-dictionary identity, exact unwrapped function identity when applicable,
canonical code digest/signature, and the exact generator/runtime source or
binary anchor. It never obtains a method through ordinary attribute lookup.

`GeneratedFieldAccessorRecord` contains a literal label, owner-artifact label,
exact owner-class identity, literal
class-dictionary field name, field position from the independently frozen
ordered field recipe, exact raw accessor identity, exact accessor type
identity, and runtime source/binary anchor. For a named tuple, the field name
and index are derived solely from the literal `_fields` tuple and its position;
the `_tuplegetter` is not required to expose `__objclass__`, `__name__`,
`field`, or `index`, and the audit never calls the getter or `__reduce__`.

`GeneratedProjectArtifactBinding` contains:

- literal label, `artifact_kind: DATACLASS | NAMEDTUPLE | ENUM_CLASS`, root scope,
  project-module label, class qualified name, exact class identity, class
  module-source SHA-256, and exact Python version;
- for `DATACLASS`, exact parameters
  `(init,repr,eq,order,unsafe_hash,frozen,match_args,kw_only,slots,weakref_slot)`,
  ordered field recipes `(name,init,kw_only,has_default,default_contract,
  has_default_factory,default_factory_label)`, exact `__slots__`, generated
  method labels, and member-descriptor/accessor labels;
- for `NAMEDTUPLE`, exact direct `tuple` base, literal `_fields`, literal
  `_field_defaults`, exact empty `__slots__`, generated `__new__` identity/code
  digest/signature, exact generated method labels, and one generated-field-
  accessor label per `_fields` position;
- for `ENUM_CLASS`, exact project class statement/source binding, exact base
  and `EnumType` metaclass identities, ordered literal member names, one exact
  member identity/name/canonical atomic value per name, literal aliases,
  generated method labels, and exact `__members__`, `_member_map_`,
  `_member_names_`, `_value2member_map_`, `_unhashable_values_`,
  `_unhashable_values_map_`, `_missing_`, `__new__`, and every other
  exact-Python-version dependency read by the bound `EnumType.__call__` model;
  absent version-specific fields are recorded as literal absent rather than
  omitted;
  `EnumType.__call__` and iteration remain separate type-member/protocol
  capabilities; and
- one exact constructor/formal/result value-contract transfer label.

The record is literal policy data. It is verified by exact class-dictionary
lookups of the literal dataclass names or the literal named-tuple names above,
each declared field, and each declared method/descriptor, using exact
standard-library generator/metadata identities frozen by the clean bootstrap.
It does not call `dataclasses.fields`, accepts no other tuple subclass, and is
never generated by sweeping the candidate class. An unexpected generated
method, field, slot, base, default factory, or descriptor is
`GENERATED_ARTIFACT_DRIFT`.

`ProjectDescriptorBinding` contains literal label/root scope, exact project
module/class/source binding, literal attribute name, exact descriptor identity,
`PROPERTY | CLASSMETHOD | STATICMETHOD | CLASS_CONSTANT` kind, exact
`fget/fset/fdel` or `__func__` project-function labels when applicable, and
receiver/result value-contract labels. `CLASS_CONSTANT` requires one exact atomic or
manifest-labelled class-dictionary value and executes no descriptor. No
project descriptor is an external safe terminal.

`ExternalTypeMemberBinding` contains literal label/root scope, exact
already-labelled external owner type, literal class-dictionary member name,
exact member identity/kind, owner source-or-binary digest, exact Python
function state when applicable, and receiver/result value-contract labels.
This is the only route for `numpy.ndarray.size`, `shape`,
`dtype`, `ndim`, `strides`, `flags`, `flat`, `tobytes`, `all`,
`__getitem__`, `__setitem__`, and analogous reviewed native members; being a
C descriptor or member of `numpy.ndarray` is not sufficient.

`RuntimeValueLocator` has a literal label and is a closed literal derivation in
the authorization-dependency DAG. It references one top-level
`RuntimeLocatorRootNode` followed by zero or more ordered top-level
`RuntimeLocatorAccessStep` records. The root node is
exactly one of:

- `MODULE_GLOBAL(project_module_label, literal_global_name)`;
- `CLOSURE_CELL(project_function_label, code_digest, literal_freevar_name,
  freevar_ordinal)`;
- `CALLABLE_DEFAULT(project-function/external-function/generated-callback
  binding label, positional_default_ordinal)`; or
- `CALLABLE_KWDEFAULT(project-function/external-function/generated-callback
  binding label, literal_keyword)`.

Each access step is exactly one of
`STATE_FIELD(state_field_binding_label)`,
`CONTAINER_ENTRY(audit_state_read_primitive_label, exact tuple-index contract
label, exact dict-key value-contract label, or process-local-identity-token
label)`,
`BOUND_CALLABLE_RECEIVER(located_bound_callable_handle_label,
audit_state_read_primitive_label)`,
`GENERATED_FIELD_RESULT(generated_field_accessor_label,
audit_state_read_primitive_label)`, or
`TYPE_MEMBER_RESULT(audit_state_read_primitive_label)`. Each step freezes the
parent label, exact accessor/capability label, expected result identity or
value-contract label, and result type. Authorization dependencies must refer to
an earlier node in the frozen DAG. Actual runtime referents may instead form
only one declared `RuntimeStateSccBinding`; a default discovered at runtime,
an unlabelled result, or an undeclared reference cycle is a policy error.

The locator is literal reviewed policy. It resolves only through exact module
dictionaries, code/freevar/default positions, exact instance fields, bound
member getsets, generated field accessors, trusted audit state reads, and exact
built-in container operations already bound by an audit-state-read primitive.
A runtime-derived identity such as `id(resolution)` must use one
`ProcessLocalIdentityToken` produced from one literal
`ProcessLocalIdentitySource`. A `LIVE_LOCATED_IDENTITY` source resolves an
already-held root/closure/default/runtime value through a frozen locator; the
audit TCB computes `id()` exactly once inside the child and places only that
integer in a non-serializable child-local side table keyed by token label. A
`SYMBOLIC_FRESH_IDENTITY` source is created by one exact audited factory or
constructor result at a paired allocation site and frame key; it has no live
integer in the static analyzer and is represented by the canonical tuple
`(root, allocation_site, frame_key, allocation_ordinal)`. The paired source
`id` transfer must produce the same token label in either case. A locator may
consume only a live token; abstract set/dict membership, insertion, deletion,
snapshot-tuple construction, hashing, equality, and identity comparisons may
consume either kind only at the token's literal allowed-consumer sites. No
consumer receives a policy integer or serializes an address. Resolution holds
every live intermediate strongly, validates the whole path in order, and may
verify a live identity after project import but may not discover a new field,
path, kind, consumer, or permission from that value. The `records_get` path is frozen as
closure cell -> exact bound `dict.get` -> exact `__self__` -> hidden dict;
later tuplegetter, weakref, native callback, or default paths are separate
predeclared steps rather than one broad receiver exemption.

`ProcessLocalIdentitySource` contains a literal label/root scope, kind
`LIVE_LOCATED_IDENTITY | SYMBOLIC_FRESH_IDENTITY`, exactly one live locator or
producing callsite/result-transfer label set, source value-contract label,
frame-key digest for a symbolic source, allocation ordinal, and the complete
ordered allowed-consumer site labels. `ProcessLocalIdentityToken` contains a
literal label/root scope, the source label, exact source `id` callsite key,
exact `id` external-identity and semantic-model labels, exact source value-
contract label, optional auditor `PROCESS_LOCAL_IDENTITY` primitive label, and
the same ordered consumer labels plus allowed operations `LOCATOR_KEY |
HASH | EQUALITY | SET_CONTAINS | SET_ADD | SET_REMOVE | DICT_LOOKUP |
TUPLE_SNAPSHOT | IDENTITY_COMPARE`. The audit primitive is mandatory only for
`LIVE_LOCATED_IDENTITY` and forbidden for `SYMBOLIC_FRESH_IDENTITY`. Its live
integer, when present, is never a record field, canonical value, digest input,
report detail, or cross-process authority. Source, token, id transfer, every
state/collection transfer, and every consumer must resolve to the same token
label and source provenance. A different source, unlisted consumer, second
allocation ordinal, recomputed live id outside the primitive, or persisted
integer is `RUNTIME_VALUE_BINDING_DRIFT`.

The first-GREEN literal inventory must include every currently reached `id`
flow rather than only the hidden-record locator: `parameters.py`'s exact
container parameter through active-set contains/add/remove;
`nulls/executable_base.py`'s exact list/tuple and Mapping parameters through
the same active-set protocol; both null implementations' token and original-
state identity entries through ordered tuple construction and later exact
snapshot comparison; the migration lookup parameter through hidden-dict
lookup; and the factory-owned newly constructed `PlanResolutionV2` through
symbolic allocation, hidden-dict insertion, callback-closure capture, lookup,
and deletion. For each source the table freezes exact source hash, paired id
site, source kind, allocation/frame identity, every consumer site and operation,
and the final lifetime boundary. A missing consumer or a token used across two
allocation ordinals is a policy error before traversal.

`LocatedBoundCallableHandle` contains a literal label/root scope, one locator
that yields the exact bound callable, exact callable identity/type labels,
exact external owner-type and raw class-dictionary member labels, and exact
`BOUND_METHOD_RECEIVER` audit-read label. It does not reference a receiver
runtime-value or a finalized `BoundTypeMemberBinding`. A receiver locator may
read through this handle; only after that receiver is bound may the finalized
bound-member record refer to both. This one-way sequence is
`bound-callable locator -> located handle -> receiver locator -> receiver
runtime binding -> finalized bound member` and prevents mutual authorization.

A named-tuple `GENERATED_FIELD_RESULT` uses the independently frozen `_fields`
position and an exact auditor-TCB `tuple.__getitem__` primitive. The
`GeneratedFieldAccessorRecord` validates the class layout and raw tuplegetter
identity, but the auditor still never invokes that getter or `__reduce__`.

`ProjectStateFieldBinding` contains literal label, parent runtime-value label,
literal field name, `EXACT_INSTANCE_DICT_LOOKUP | EXACT_SLOT_LOOKUP` mode,
exact slot descriptor identity when applicable, and exactly one nested
value-contract label or exact child identity/type anchor held by this field
record. It never references a child `ProjectRuntimeValueBinding`; that child
may later locate itself through this state-field label. Missing/extra
instance-dictionary keys, undeclared slots, or a child at another path is
`STRUCTURED_STATE_DRIFT`.

`GeneratedStdlibCallbackBinding` contains literal label, parent runtime-value
label and source-state-field binding label, exact generated function identity in the current child,
stdlib module/source realpath and SHA-256, canonical code digest, positional
and keyword defaults, closure recipe, complete all-`LOAD_*` binding record,
one semantic-model label, one outcome-contract label, and pre/post state
digest. Its dedicated transfer points to this callback; the callback does not
point back to the transfer. For
`WeakKeyDictionary.__init__.<locals>.remove`, the default self weakref must
refer to the exact parent dictionary and its own callback must be exact
`None`. This phase-2 binding validates a predeclared recipe after
project import; it cannot create an `ExternalIdentityEntry` or widen policy
from the observed callback.

`GeneratedStdlibCallbackTransfer` contains literal label, callback-binding
label, exact callback code/source digest, exact key/input contract labels, and
a closed ordered intrinsic-effect-label graph. The sole initial supported graph is the
exact-version `WeakKeyDictionary.remove` behavior: call the exact default
self-weakref, compare its result with `None`, return normally on `None`, read
`_iterating` otherwise; on the truthy branch append the weakref key to
`_pending_removals`; otherwise delete the exact key from `data`; catch only
exact `KeyError`; and expose the exact normal/exception outcome. Each weakref
call, identity comparison, truth, append, delete, hash, equality, and exception
edge references an independently frozen intrinsic semantic model.
The analyzer does not need general `Delete` syntax for this one generated
callback, but it independently verifies that the bound callback code digest
matches this transfer. Any other generated callback or code digest is
unsupported and fails closed.

`BoundTypeMemberBinding` contains literal label, one located-bound-callable
handle label, exact bound callable identity, exact receiver
`ProjectRuntimeValueBinding` label, exact
`__self__` identity verified through the bootstrapped built-in-method
getset descriptor, exact external owner type and literal class-dictionary
member identity, receiver-contract label, semantic-model label, and one
outcome-contract label. It is
the only route for a closure-held value such as the exact `dict.get` bound to a
private receiver removed from its module dictionary.

`ProjectRuntimeValueBinding` contains literal label/root scope, one
`RuntimeValueLocator` label, exact current-child identity, exact external/project
type binding, construction provenance `IMPORT_TIME | FACTORY_OWNED |
CLOSURE_CAPTURED | NESTED_STATE`, one of `BUILTIN_CONTAINER | REGEX_PATTERN |
TYPING_FORM | ENUM_CLASS | STRUCTURED_INSTANCE | WEAK_KEY_DICTIONARY |
WEAK_REFERENCE | GENERATED_STDLIB_CALLBACK | BOUND_TYPE_MEMBER`, complete
pre/post state digest, complete literal state-field-name set, contained
identity/value-contract labels, and optional exact generated-artifact or
external-type label. It does not list child state-field, callback, bound-member,
or receiver labels; those child records point to the parent. A derived
non-authorizing ownership index may be reported but is not canonical authority.

Kind-specific state is closed. `REGEX_PATTERN` freezes exact pattern text,
flags, groups, exact bounded built-in `dict[str,int]` `groupindex` container
contract, exact accessor/type identity, complete canonical ordered content,
pre/post digest, exact pattern type, and `re` source/binary anchor;
`.fullmatch` requires a separate type-member call.
`TYPING_FORM` distinguishes exact `GenericAlias | UnionType |
_CallableGenericAlias` types and freezes origin, ordered arguments, parameters,
and complete instance state recursively by existing labels, without `repr`,
equality, or hashing. It is legal only for an import/default/closure-owned form
reachable through a frozen locator; an instruction-created `UnionType` is an
`EXTERNAL_RESULT`. `ENUM_CLASS` requires one
`GeneratedProjectArtifactBinding`. `STRUCTURED_INSTANCE` freezes a literal
complete instance dictionary/slot recipe. `WEAK_KEY_DICTIONARY` freezes its
literal complete instance fields, nested data dict, pending-removal state, and
the exact generated callback binding. `WEAK_REFERENCE` freezes exact referent
and callback labels. A non-`None` callback is scheduled and audited. A nested
weakref or dict is owned through its literal parent locator rather than being
misstated as a module global.

Two different graphs are normative and must not be conflated:

- `AuthorizationDependencyGraph` contains labelled policy records and only
  `AUTH_REQUIRES` edges. It is built after all labels are pre-registered, must
  be a DAG, and determines construction order and minimum authority. A cycle
  here is always a policy error.
- `RuntimeStateReferenceGraph` contains exact located runtime identities and
  `STATE_FIELD | RECEIVER | REFERENT | CALLBACK | DEFAULT | CLOSURE |
  CONTAINER_ENTRY` edges. It may contain a cycle only when the exact member set
  and edge multiset match one literal `RuntimeStateSccBinding`. Canonical
  records retain label references and never recursively expand this graph.

Every cross-record label is classified as exactly `OWNS | AUTH_REQUIRES |
VALIDATES | RUNTIME_REF`. `OWNS` has one direction and one owner;
`AUTH_REQUIRES` alone enters the authorization DAG; `VALIDATES` is a
non-authorizing equality/cross-check between pre-registered labels and may not
create a permission; `RUNTIME_REF` alone enters the runtime-state graph. A
field cannot be classified twice. Parent records never list child records
whose child already names the parent. This classification prevents a
validation backlink from becoming authority while allowing exact same-object
cross-checks.

`RuntimeStateSccBinding` contains literal label/root scope, one closed shape
`WEAK_KEY_DICTIONARY_REMOVE_SELFREF | RESOLUTION_RECORDS_WEAKREF_CALLBACK`,
the canonically ordered member labels, and the exact ordered edge tuples
`(source_label,edge_kind,target_label,ordinal)`. The first shape is exactly
`WeakKeyDictionary -> remove callback -> positional-default weakref -> same
WeakKeyDictionary`; the second is exactly `records dict -> identity record ->
weakref -> discard callback -> closure records dict`. No extra member, extra
edge, substituted referent, wrong callback, or overlapping SCC is legal. Label
registration precedes reference/SCC validation, so these runtime cycles do not
create authorization cycles.

### 5.2 Root and callsite capabilities

`ValueContractKind` is the closed enum `EXACT_ATOMIC | ATOMIC_DOMAIN |
BOUNDED_BYTES | DIGESTED_BYTES | EXACT_IDENTITY | EXACT_TYPE_TERMINAL |
STRUCTURED | CONTAINER | ARRAY | ITERABLE | ITERATOR | DICT_VIEW |
PROJECT_CALLABLE | PROCESS_LOCAL_IDENTITY_TOKEN | EXTERNAL_RESULT | UNION`.

`IterableContract` contains literal label, `ITERABLE | ITERATOR | DICT_VIEW`,
one exact producer capability or project-generator code label, exact
receiver/source value-contract label, exact item value-contract label, exact or
bounded non-negative cardinality, `reiterable: bool`, `single_pass: bool`,
`view_kind: KEYS | VALUES | ITEMS | NOT_APPLICABLE`, and ordered
protocol-dispatch capability labels.
`ITERATOR` is symbolic and single-pass; the audit never obtains or advances a
live candidate iterator. `DICT_VIEW` binds an exact built-in dict or runtime
value plus its view kind. A generator expression binds its exact nested code,
captured abstract environment, item contract, and finite source contract.

`ValueContract` is the sole argument, field, local, and result contract. It has
a literal unique `label`. Its normative fields are `label`, `kind`,
`atomic_type_label`, `atomic_value`,
`atomic_literals`, `lower_bound`, `upper_bound`, `identity_label`,
`byte_length`, `maximum_byte_length`, `bytes_sha256`, `audit_only`,
`type_label`, `exact_type`, `provenance_label`, `structured_fields`,
`container_type_label`, `exact_length`, `minimum_length`, `maximum_length`,
`range_start`, `range_stop`, `range_step`, `element_contracts`, `key_contract`,
`mapped_value_contract`, `array_dtype`,
`array_ndim`, `array_shape_bounds`, `array_hasobject`, `array_writeable`,
`array_c_contiguous`, `array_identity_label`, `array_content_digest`,
`iterable_contract_label`, `callable_binding_label`,
`process_local_identity_token_label`, `producing_capability_label`,
`external_result_contract_label`, and
`alternative_labels`. Optional scalar fields use
`None`; collection fields use empty tuples. It contains one kind and the
matching closed payload:

- `EXACT_ATOMIC`: exact atomic type and canonical value;
- `ATOMIC_DOMAIN`: exact atomic type plus either an ordered literal set or one
  inclusive integer/finite-float interval; no unconstrained "atomic allowed"
  bit exists;
- `BOUNDED_BYTES`: exact built-in `bytes`, `audit_only=true`, and one finite
  `maximum_byte_length`; content need not be a literal and the contract is legal
  only as an auditor-TCB read result after a separately checked allocation
  bound;
- `DIGESTED_BYTES`: exact built-in `bytes`, `audit_only=true`, exact
  `byte_length`, `maximum_byte_length`, and ordinary lowercase SHA-256 of the
  bytes; it is legal only when the expected digest is independent policy data;
- `EXACT_IDENTITY`: one manifest label and exact current-process identity, only
  for an opaque non-traversed value that is not eligible for a structured,
  container, array, iterable, or callable kind;
- `EXACT_TYPE_TERMINAL`: one exact built-in immutable type, with no attribute,
  call, subscript, iteration, or protocol use permitted;
- `STRUCTURED`: optional exact identity label, exact project/external type
  label, construction-provenance
  label, and ordered `(attribute, slot/tuplegetter/descriptor/class-constant
  access-binding label, value-contract label)` values;
- `CONTAINER`: optional exact identity label, exact
  tuple/list/dict/set/frozenset/`MappingProxyType` or `range`, exact or bounded
  length, and ordered element/key/value contract labels;
  `range` instead carries exact bounded built-in integer start/stop/step and is
  never materialized; unordered containers may contain only validated exact
  atomics and are canonicalized by their canonical atomic bytes;
- `ARRAY`: exact `numpy.ndarray` type, exact dtype string, exact ndim,
  per-dimension exact value or inclusive bound, exact `hasobject` and
  writeability/C-contiguous flags, and for a root array an exact identity plus
  content digest;
- `ITERABLE`, `ITERATOR`, or `DICT_VIEW`: one matching closed
  `IterableContract` label; item access, iteration, consumption, and callback
  behavior require its exact `ProtocolDispatchCapability` values;
- `PROJECT_CALLABLE`: exact project function/class binding and its formal
  contract label;
- `PROCESS_LOCAL_IDENTITY_TOKEN`: one exact token label; it can be produced
  only by the paired source `id` model or, for a live source, the token's
  auditor-TCB primitive. It may be consumed only by the token's literal
  allowed-consumer sites and operation kinds; symbolic fresh tokens are valid
  abstract hash/equality/set/dict/snapshot operands but never locator keys;
- `EXTERNAL_RESULT`: exact producing capability plus one explicit closed nested
  value-contract label; recursive self-reference is forbidden and cycles fail
  policy construction;
- `UNION`: two or more distinct, canonically ordered non-`UNION` contract
  labels.

Canonical serialization normalizes all `ValueContract` records into the
top-level `value_contracts` table ordered by label. A reference serializes only
the literal label. Each table entry has exactly `label`, `kind`, and `payload`;
`payload` contains only the selected kind's field names above, with optional
selected scalars as explicit `null` and selected collections as arrays. Fields
from other kinds are absent from `payload`, while the in-memory constructor
still requires their neutral `None`/empty values. This is the sole canonical
projection and prevents a short ad hoc `value` field from replacing
`atomic_type_label`/`atomic_value`.

The array-content digest preimage is exact. A numeric array uses
`{"schema":"selcal.array-content.v2","kind":"numeric","dtype":<dtype.str>,
"shape":[...],"strides":[...],"writeable":false,"c_contiguous":true,
"order":"C","content_hex":<lowercase hex>}`. The content bytes are read only
after the size/shape/flag checks through the exact `numpy.ndarray.tobytes`
`ExternalTypeMemberBinding` with one `AuditStateReadPrimitive` whose receiver
is the exact array and whose outcome is a `BOUNDED_BYTES` audit-only contract
with maximum length 8,388,608; ordinary exact-atomic `bytes` retains its
65,536-byte ceiling. There is no
unbound "buffer interface" exemption. An object array uses the same keys with
`kind:"object"` and replaces `content_hex` by `items`, an ordered array of
canonical atomics or predeclared identity labels read through the exact
auditor-TCB `flat`/indexed-item state-read primitives and their intrinsic
models, not a project `ProtocolDispatchCapability`. Raw pointer bytes are
forbidden. Before either read, exact `dtype.itemsize` and `ndarray.nbytes`
audit-state reads must agree with checked integer arithmetic. Numeric content
is limited to 8,388,608 bytes and the complete canonical object-array preimage
to 1,048,576 UTF-8 bytes; the audit checks the bound before allocation or
serialization. Exceeding either is `ARRAY_BOUND_EXCEEDED`. The digest domain is
`array-content`.

Fields not selected by the kind must be empty. Nested union, empty union,
overlapping alternatives, NaN/infinite bounds, subclass matching, and any
protocol-bearing `EXACT_TYPE_TERMINAL` are policy errors. Contract matching
uses kind-specific exact identity/type and canonical bounded values; it never
uses candidate equality, hashing, ordering, iteration, or `repr`.

Contract classification, intersection, and ordering are normative. Every
runtime value has exactly one canonical kind: structural/container/array/
iterable/callable classifications take precedence over `EXACT_IDENTITY`, and
an identity requirement for such a value resides inside that canonical kind.
Policy construction rejects one value labelled under two canonical kinds. The
kind rank is exactly
`EXACT_ATOMIC, ATOMIC_DOMAIN, BOUNDED_BYTES, DIGESTED_BYTES, EXACT_IDENTITY,
EXACT_TYPE_TERMINAL, STRUCTURED, CONTAINER, ARRAY, ITERABLE, ITERATOR,
DICT_VIEW, PROJECT_CALLABLE, PROCESS_LOCAL_IDENTITY_TOKEN,
EXTERNAL_RESULT, UNION`. Equal-kind intersection is computed structurally:
atomic values/domains use exact type plus literal/range intersection;
bounded/digested bytes require exact built-in `bytes`, true audit-only state,
the minimum maximum length, compatible exact length, and equal digest when
both specify one;
identities and exact type terminals require the same labels; structured values require the same exact type,
compatible absent/exact identity labels, and provenance then recursively
intersect corresponding fields; containers require the same exact built-in
type, compatible absent/exact identity labels and length bounds, and recursive
element/key/value intersection; arrays require identical exact type/dtype/
ndim/flags, compatible absent/exact identity and content-digest values, plus
intersecting shape bounds; iterable kinds require the same
producer/view/single-pass identity and intersecting cardinality/item contracts;
callables and process-local tokens require the same binding label; and external results first require the
same producing capability then recurse. For identity/content fields, absent
intersected with exact yields exact, two equal exact values yield that value,
and two different exact values are disjoint. Different canonical kinds are
disjoint except: (a) `EXACT_ATOMIC` versus a same-type containing
`ATOMIC_DOMAIN`; (b) exact built-in atomic `bytes` versus `BOUNDED_BYTES`,
which intersects iff the exact length is within the bound and yields exact
bytes with `audit_only=true`; (c) exact built-in atomic `bytes` versus
`DIGESTED_BYTES`, which additionally requires its ordinary SHA-256 and exact
length to match; (d) `BOUNDED_BYTES` versus `DIGESTED_BYTES`, which uses the
same length/bound/digest rules; and (e) `EXTERNAL_RESULT`, which delegates
value-set operations to its nested contract while retaining producer
provenance. These are the complete byte cross-kind rows.

Every contract expression has two independent lattice components: a value-set
constraint and an ordered set of provenance requirements. A bare contract has
an empty provenance set; `EXTERNAL_RESULT(p,B)` has B's value set plus
`PRODUCED_BY(p)`. Value-set containment never removes provenance. A bare `B`
and `EXTERNAL_RESULT(p,B)` therefore remain distinct union alternatives even
when their value sets overlap. Intersecting expressions unions their
provenance requirements; incompatible producer requirements are disjoint only
when the policy explicitly declares their producing sites mutually exclusive.

The result type is the closed algebra `EMPTY | REGISTERED(label) |
DERIVED(DerivedValueContract) | NORMALIZED_UNION(items)`; it has no
indeterminate case. `DerivedValueContract` is a canonical immutable,
non-authorizing transient record containing derived kind/payload, ordered
provenance requirements, operand labels/digests, and derivation-rule version.
It is never added to a policy table and cannot be referenced by a capability.
Before a derived value can match an argument/result/outcome boundary, its
canonical value-set and provenance bytes must equal one already registered
literal `ValueContract`; otherwise it remains derived and the boundary fails
`UNKNOWN_VALUE_PROVENANCE`. Thus `[0,10] intersect [5,15]` deterministically
produces the transient `[5,10]` without inventing a label or authority.
`AbstractValue` stores this contract expression. For `UNION x X`, intersection distributes over every alternative; for
`UNION x UNION`, it distributes over the Cartesian product, removes `EMPTY`,
then normalizes. Normalization recursively flattens unions, merges touching or
overlapping same-type atomic intervals, removes exact duplicate canonical
records, removes an alternative strictly contained by another only when its
provenance requirements are byte-identical, collapses zero
alternatives to `EMPTY` and one alternative to that contract, checks the
32-alternative bound, and sorts by `(kind_rank, canonical value-contract
bytes)`. Remaining incomparable overlapping structured alternatives are a
policy-construction error; the analyzer widens that join to `UNKNOWN` instead
of inventing authority.

Value-set containment `A >=v B` means every value admitted by `B` is admitted
by `A`; authorization containment `A >=a B` additionally requires identical
provenance requirements. Both are total: exact atom/domain and byte cases use their trusted literal/range/
length/digest sets; equal canonical identity, callable, producer, type, field,
container, array, iterable, and provenance constraints recurse structurally;
`UNION >= B` holds only when normalized intersections cover all of `B`, while
`A >= UNION` holds only when it contains every alternative; an
`EXTERNAL_RESULT(p,B) >=v B` follows the nested set, but
`EXTERNAL_RESULT(p,B) >=a B` is false; one external result authorization
contains another only when producer and nested authorization match. All
unlisted cross-kind pairs are false. `producing_capability_label` may
reference only one declared `CallsiteCapability`, `AttributeAccessCapability`,
`StateOperationCapability`, `ProtocolDispatchCapability`, or
`BinaryOperatorCapability` in the same root;
project-generated iterators instead use their exact nested-code label.
Construction KATs exhaust the closed kind-by-kind table and require
intersection symmetry and commutativity, idempotence, both containment
relations' reflexivity/transitivity/antisymmetry on canonical records,
disjointness agreement, union
distribution/flattening/deduplication/collapse, and identical canonical bytes
in both operand orders. They include `UNION x non-UNION`, `UNION x UNION`,
exact-identity versus structured/container/array classification
counterexamples, exact-bytes/bounded/digested cross-kind cases, raw-versus-
produced provenance preservation, derived-interval materialization and failed
unregistered-boundary cases, and array identity/content absent,
equal, and conflicting triples.

`RootInputContract` contains the root label and one ordered
`RootArgumentContract` per positional/keyword input. Atomic inputs reference
one exact value-contract label. Every non-atomic root input uses
`RootStructuredStateContract`, containing:

- `parameter_name`, exact `runtime_identity`, `project_type_binding_label`, and
  `construction_provenance: AUDITOR_CONSTRUCTED |
  PROJECT_FACTORY_OWNED`;
- `constructor_or_factory_label` and `validator_or_ownership_gate_label`;
- complete ordered `field_contracts: tuple[(field_name,
  slot_descriptor_label, value_contract_label), ...]`;
- `pre_audit_state_digest` and required `post_audit_state_digest`; and
- ordered nested identity/content-digest bindings for arrays or mutable
  containers.

The child constructs approved fixtures from literal test vectors only after
the external bootstrap and before policy freeze, or obtains an exact
factory-owned object through a separately audited project factory. The policy
verifies the literal contract; it never discovers fields from the instance.
The root object and all nested identities are held strongly. A forged exact
type made by `object.__new__`, a different same-valued instance, a missing or
extra field, or post-freeze mutation fails before callsite authorization. Root
attribute reads resolve only through this contract and its exact slot binding,
not through annotations or ordinary `getattr`.

`RootArgumentContract` contains `parameter_name`, `POSITIONAL_ONLY |
POSITIONAL_OR_KEYWORD | KEYWORD_ONLY`, non-negative position or exact keyword,
and exactly one of `atomic_value_contract_label` or
`structured_state_contract`. Variadic root arguments are forbidden for these
two roots.

`ArgumentContract` contains literal label, an exact positional index or
keyword name, one value-contract label, and an empty-by-default ordered tuple
of separately labelled protocol dispatch capabilities. `ResultContract`
contains literal label, one value-contract label, whether the result may be
discarded, and the exact independently frozen producing semantic-model label.
These named schemas
replace prose result alternatives.

`ExceptionContract` contains exactly `label`, exact project/external
`exception_class_label`, ordered exact `mro_identity_labels` used for handler
matching, ordered `constructor_argument_contract_labels`, and optional
`cause_exception_label` and `context_exception_label`. Cause/context references
must form an acyclic graph and may not self-reference. `OperationOutcomeContract`
contains exactly `label`, `normal_result_contract_label: str |
NO_NORMAL_RETURN`, and `exception_contract_labels: tuple[str, ...]`. The
normal result is always a label reference to the top-level `result_contracts`
table, never an embedded record. Empty exceptions are
allowed; an outcome with neither a normal return nor an exception is a policy
error. `NO_NORMAL_RETURN` is a literal enum value, not `None` or `UNKNOWN`.
Exception labels are ordered by canonical exception-class label, constructor
contract bytes, cause label, and context label. An undeclared or wrong-MRO
exception is `EXCEPTION_CONTRACT_MISMATCH`; a wrong normal result is
`RESULT_CONTRACT_MISMATCH`.

The exact atomic universe is `None`, `bool`, `int`, finite `float`, finite
`complex`, `str`, and `bytes`, each by exact type. Integers are limited to
4,096 bits; strings are limited to 4,096 UTF-8 bytes; bytes are limited to
65,536 bytes. `bytearray`, `range`, `slice`, Enum values, `GenericAlias`,
subclasses, and user protocol objects are not atomic. They require an explicit
container/value/capability contract or fail.

`SemanticGuardKind` is the closed enum `EXACT_TYPE | EXACT_IDENTITY |
BOUNDED_COMPARE | LENGTH_BOUND | CONTAINS_LITERAL | STATE_PREDICATE |
CALLBACK_PREDICATE`. `SemanticGuard` contains exactly `label`, `kind`, ordered
`operand_contract_labels`, one exact comparison/operator or state-operation
label, one expected canonical boolean, and ordered intrinsic-effect labels.
It evaluates only trusted abstract contracts and labelled state; it never calls
candidate equality, ordering, length, truth, containment, or callbacks.

`SemanticNormalTransferKind` is the closed enum `EXACT_VALUE |
PROCESS_LOCAL_IDENTITY_TOKEN | BOUNDED_ARITHMETIC | CONTAINER_CONSTRUCTION |
VIEW_CONSTRUCTION | ITERATOR_CONSTRUCTION | STATE_RESULT | CALLBACK_RESULT |
NO_NORMAL_RETURN`. `SemanticNormalTransfer` contains exactly `label`, `kind`,
ordered `input_contract_labels`, ordered `guard_labels`, one discriminated
`SemanticNormalPayload`, ordered `intrinsic_effect_labels`, and one optional
state-operation-transfer label. It does **not** contain an expected or target
result-contract label. Payloads are closed:

- `EXACT_VALUE(source_kind:LITERAL|INPUT|RECEIVER,
  literal_value:optional canonical V,input_ordinal:optional bounded int,
  projection_path:ordered literal field/index steps)`; exactly one source form
  is present and the evaluator derives the exact value/type;
- `PROCESS_LOCAL_IDENTITY_TOKEN(identity_source_label,
  allocation_site_label,allocation_ordinal,allowed_consumer_site_labels)`;
- `BOUNDED_ARITHMETIC(operator,operand_ordinals,integer_overflow_policy,
  finite_float_policy,maximum_result_bits)`; interval/literal arithmetic is
  performed by the fixed trusted evaluator, not copied from policy output;
- `CONTAINER_CONSTRUCTION(container_type_label,ordered_input_projections,
  duplicate_key_policy,ordering_policy,maximum_length)`;
- `VIEW_CONSTRUCTION(source_input_ordinal,view_kind,maximum_cardinality)`;
- `ITERATOR_CONSTRUCTION(source_input_ordinal,item_projection,
  cardinality_rule,reiterable=false,single_pass=true)`;
- `STATE_RESULT(state_operation_transfer_label,
  selector_kind,selector_path)`;
- `CALLBACK_RESULT(callback_model_label,callback_output_ordinal,
  projection_path)`; and
- `NO_NORMAL_RETURN()` with no fields.

The evaluator derives a transient contract expression, provenance, and effects
from payload plus input abstract values. It then requires exact equality with
an independently registered result contract. Changing the expected outcome
while holding model, payload, and inputs fixed must fail a counterfactual KAT.

`SemanticExceptionTransfer` contains exactly `label`, ordered non-empty
`guard_labels`, a discriminated `SemanticExceptionPayload`, and ordered
`intrinsic_effect_labels`; it has no expected exception-contract label. The
payload is exactly `(trigger_kind,operation_label,operand_ordinals,
exception_constructor_model_label,constructor_argument_projections,
cause_rule,context_rule)`. The fixed evaluator must first derive exact class,
MRO, constructor arguments, cause, and context and only then compare with the
capability's named expected exception. Guards and transfers form a DAG.
Expected outcomes never appear as a transfer input or payload.

`OperationSemanticModel` contains exactly `label`, `kind: PROJECT_CODE |
PINNED_EXTERNAL_PYTHON_INTRINSIC | BUILTIN_INTRINSIC | TYPE_MEMBER_INTRINSIC |
PROTOCOL_INTRINSIC | BINARY_OPERATOR_INTRINSIC |
GENERATED_CALLBACK_TRANSFER`, `implementation_identity_label`,
`source_or_binary_digest`, `receiver_contract_label`, ordered
`argument_contract_labels`, ordered `intrinsic_effect_labels`, one
`normal_transfer_label`, and ordered `exception_transfer_labels`.
`PROJECT_CODE` derives outcomes from its verified project AST/bytecode and
called models. General `EXTERNAL_PYTHON_CODE` is intentionally unsupported in
this auxiliary proof. The two current external-Python paths use literal
`ExternalPythonIntrinsicBinding` records: exact `typing.cast` is an identity
projection and exact `json.dumps` is pinned to its provider module/export,
resolved source/binary digest, code digest, exact receiver/argument domains,
complete recursively referenced external binding digest, and one reviewed
semantic transfer/effect graph. A changed provider version/source, extra
keyword/default hook, custom encoder/default, unsupported input contract, or
unindexed nested code fails closed. Each binding has an independent normal and
exception counterfactual KAT; it is not a reusable permission for arbitrary
external Python. Every intrinsic model is a
literal implementation record reviewed for one exact operation, receiver
domain, and argument domain; it cannot be generated from the capability or
its expected outcome. Missing, broader, or cyclic semantics produce
`UNKNOWN_VALUE_PROVENANCE` and fail closed.

`IntrinsicEffectStep` has a literal label and is the closed enum-bearing record
`LENGTH | TRUTH | HASH
| EQUALITY | ORDER | ITER | NEXT | ARRAY_COERCE | INSTANCE_CHECK | BINARY_OR | STATE_READ |
STATE_WRITE | CALLBACK | FINALIZE`, with exact input/output contract labels and an exact
project-function, external-type-member, protocol, operator, or generated-
callback model label. The built-in consumer matrix is literal: `len` schedules
`LENGTH`; `any` schedules `ITER/NEXT` and `TRUTH` for every possible item;
`sorted(key=...)` schedules the key callback and `ORDER` on every possible key
result; dict/set/WeakKeyDictionary insertion schedules `HASH` and possible
`EQUALITY`; `np.asarray` schedules `ARRAY_COERCE`; `isinstance` schedules
`INSTANCE_CHECK` for each exact type, union component, or runtime Protocol
metaclass dependency; and container constructors
schedule their iterator effects. For the current roots, a consumer lacking a
complete intrinsic model accepts only exact built-in atomic/container operands
whose model proves no user dispatch. WeakKeyDictionary insertion and removal
explicitly schedule weakref/referent hash and equality effects. A semantic
outcome is never copied from the capability being checked.

`ProjectFunctionContract` contains literal label, exact function/code binding,
exact receiver-contract label, ordered formal-parameter value-contract labels including defaults,
`*args`/`**kwargs` prohibition or exact finite expansion, and one declared
outcome-contract label. The analyzer computes the return contract from
every normal return and the exact exception contracts from every raise/call
edge and requires both to equal the declaration; annotations do not grant
authority. `_integrity`, `_refuse`, `_cap_exceeded`, and every other
raise-only helper must declare `NO_NORMAL_RETURN`, so its successor environment
is unreachable.

`CallsiteCapability` contains:

- `label` and `root_label`;
- exact project owner module label and function qualified name;
- literal owner source SHA-256;
- exact owner function and code identity in the current child process plus the
  canonical code digest;
- exact paired `StructuralCallsiteKey` label;
- exact external identity label;
- receiver-contract label;
- ordered positional and keyword argument-contract labels;
- one independently frozen semantic-model label and one expected
  outcome-contract label; and
- reason and reference token.

An exact callable identity is not safe by itself. `len`, `tuple`, `dict`,
`int`, NumPy functions, ufuncs, and descriptors may dispatch into user code
through their arguments. They are permitted only through a matching
`CallsiteCapability`. If argument or receiver safety cannot be statically
bound to the root-input contract, the callsite is unapproved.

`SAFE_FACTORY` additionally freezes exact input contracts and one exact result
type. A project or external factory with unknown result behavior is
unapproved.

`NamespaceAttributeCapability` contains literal label, root label, exact paired
`StructuralAttributeSiteKey`, exact namespace binding label, literal attribute
name, and resolved external identity label. A namespace permission without
this exact instruction-level record cannot resolve an attribute.

`AttributeAccessCapability` contains literal label, root label, exact paired
`StructuralAttributeSiteKey`, `READ | WRITE | DELETE`, literal attribute name,
exact receiver-contract label, one exact project-descriptor/generated-slot/
generated-tuplegetter/external-type-member binding label, optional assigned
argument-contract label, semantic-model label, and outcome-contract label. A property read schedules its
exact `fget`; class/static methods schedule the exact `__func__` with their
specified receiver; a native descriptor schedules its exact member binding.

`StateOperationCapability` contains literal label, root label, exact paired
`StructuralStateSiteKey`, exact `ProjectRuntimeValueBinding` label,
`GET_ITEM | SET_ITEM | DELETE_ITEM | METHOD_CALL`, exact key/value argument
contract labels, semantic-model and outcome-contract labels, one
state-operation-transfer label, and
ordered type-member/provider labels that
implement the operation. It describes source semantics only: the audit does
not execute the mutation, and the bound state object must have identical
pre/post audit digest. For `WEAK_KEY_DICTIONARY.SET_ITEM`, the capability must
schedule the exact `WeakKeyDictionary.__setitem__` Python function, weakref
factory/type members, and any callback provider; a generic custom-mapping
permission is forbidden.

`StateOperationTransfer` contains literal label and ordered dependencies from receiver/key/value
contracts to nested state-field, weakref referent/callback, internal-dict key/
value, and normal/exception outcome contracts. It is the closed relation for
`ref(key, self._remove)` and the WeakKeyDictionary internal data update; prose
about a callback does not authorize an unlisted dependency.

`ProtocolDispatchCapability` contains literal label, root label, exact paired
`StructuralProtocolSiteKey`, `ITER | NEXT | DICT_KEYS | DICT_VALUES |
DICT_ITEMS | CONSUME | KEY_CALLBACK | LENGTH | TRUTH | HASH | EQUALITY | ORDER
| ARRAY_COERCE | INSTANCE_CHECK`, exact receiver/source and item/input contract labels, optional
`external_class_binding_label` required only for an external
`INSTANCE_CHECK`, optional
project callback binding, ordered external type-member/provider labels,
semantic-model label, and outcome-contract label. `enumerate`, `zip`,
`itertools.permutations`, generator expressions, dict views, `sorted(key=...)`,
`any`, and container constructors consuming an iterator each require literal
protocol records; a consumer permission never implicitly authorizes the
iterable's callbacks.

`BinaryOperatorCapability` contains literal label, root label, exact paired
`StructuralOperatorSiteKey`, operator `TYPE_UNION_OR | DICT_KEYS_UNION_OR`,
exact left/right contract labels, ordered provider/member and intrinsic-effect
labels, one semantic-model label, and one outcome-contract label.
`TYPE_UNION_OR` requires exact type operands plus `type.__or__`; its fresh
`UnionType` result is a provenance-bound `EXTERNAL_RESULT`, never an import-
time `ProjectRuntimeValueBinding`. `DICT_KEYS_UNION_OR` requires two exact
`DICT_VIEW(KEYS)` contracts backed by exact built-in dictionaries, schedules
bounded `ITER/NEXT/HASH/EQUALITY` for all possible keys, and constructs an
exact bounded built-in set result through an independent normal transfer. The
real migration sites at source lines 484 and 519 require the latter capability;
a generic `BINARY_OR` effect alone does not authorize either site.

`AuditStateReadPrimitive` contains literal label, operation `NDARRAY_FIELD |
NDARRAY_TOBYTES | NDARRAY_FLAT_ITEM | BUILTIN_CONTAINER_ENTRY | TUPLE_ITEM |
BOUND_METHOD_RECEIVER | WEAKREF_REFERENT_CALL |
WEAKREF_CALLBACK_DESCRIPTOR | PROCESS_LOCAL_IDENTITY`, audit-implementation
digest, exact external type-member/model labels, exact receiver-contract label,
ordered precondition contract labels, and outcome-contract label. It is part of the
auditor TCB, not a project callsite capability. The only initial uses are the
literal ndarray `size`, `shape`, `strides`, `flags`, `dtype.itemsize`, `nbytes`,
exact built-in container-entry/tuple-item, `flat`, bounded flat-item, and
`tobytes` reads, exact bound-method `__self__`, process-local root identity, and
weakref operations needed by predeclared runtime locators. A weakref referent
uses exact `ReferenceType.__call__`, whose current raw member is a
`wrapper_descriptor`; only `ReferenceType.__callback__` is read through its
exact `member_descriptor`. Neither is described or implemented as a getset.
Every read is
bound to the implementation digest, rechecks pre/post state, and has an
independent intrinsic semantic model; an unlisted auditor descriptor call is a
policy error.

### 5.3 Callsite value provenance

`AbstractValueKind` is the closed enum `BOTTOM | UNKNOWN | CONTRACT_VALUE |
SYMBOLIC_RECEIVER | PROJECT_FUNCTION | PROJECT_CLASS |
EXTERNAL_CLASS | PROCESS_LOCAL_IDENTITY_TOKEN | PROJECT_RUNTIME_VALUE |
BOUND_TYPE_MEMBER | NAMESPACE`.

`BOTTOM` means no reachable normal value during SCC initialization; it cannot
match a callsite or escape into a local after convergence. `AbstractValue`
contains the kind, one `REGISTERED(label) | DERIVED(record) |
NORMALIZED_UNION(items)` contract expression when it is a contract value,
exact project/namespace binding when applicable, originating root/capability
label, and a deterministic provenance path. Only a registered expression may
cross a named capability boundary; derived intermediates must equal a frozen
registered contract first. No value is
represented by a type name or annotation alone.

`RootArgumentBinding` contains exact parameter name, exact runtime identity
when applicable, exact runtime type, and the matching root-input
`AbstractValue`. `GlobalsEnvironment` contains project-module binding label,
exact globals-dictionary identity, the ordered referenced-name set, and one
post-traversal binding-state digest. Binding-state serialization uses literal
source names and bootstrap/project identity labels; it never serializes raw
process ids or provider representations.

`CallFrameBinding` contains exact owner function/code identity, project-function
binding label, code digest, receiver binding, root-argument bindings,
immutable formal/local-name to `AbstractValue` environment, exact
default/keyword-default/closure digest, exact referenced-globals environment
digest, and `frame_key_digest`. The frame key is the canonical digest of the
function binding label, owner code, receiver value-contract label, ordered
formal value-contract labels, defaults, keyword defaults, closure values, and
referenced-globals digest. Two functions with the same code object but
different closures/defaults/globals therefore cannot share an SCC summary. The
key is not the Python identity of a newly allocated frame record.

Site pairing is not a shared key populated by two cooperative characterizers.
One literal `InterpreterOpcodeProfile` first freezes exact Python version,
`dis.opmap` canonical digest, cache-opcode exclusion set, and the complete
source-kind lowering table. For the current CPython 3.12 policy that table is
exactly: `CALL -> (optional KW_NAMES immediately followed by exactly one
CALL or CALL_FUNCTION_EX)`, `ATTRIBUTE_READ -> (LOAD_ATTR)`,
`ATTRIBUTE_WRITE -> (STORE_ATTR)`, `ATTRIBUTE_DELETE -> (DELETE_ATTR)`,
`SUBSCRIPT_READ -> (BINARY_SUBSCR or BINARY_SLICE)`,
`SUBSCRIPT_WRITE -> (STORE_SUBSCR or STORE_SLICE)`,
`SUBSCRIPT_DELETE -> (DELETE_SUBSCR)`, `ITERATION -> (GET_ITER,FOR_ITER)`,
`COMPARE -> (COMPARE_OP,CONTAINS_OP,IS_OP)`, `UNARY -> (UNARY_POSITIVE,
UNARY_NEGATIVE,UNARY_NOT,UNARY_INVERT)`, `BINARY_OPERATOR -> (BINARY_OP)`
with exact numeric operation argument/name, `TRUTH ->
(POP_JUMP_IF_FALSE,POP_JUMP_IF_TRUE,JUMP_IF_FALSE_OR_POP,
JUMP_IF_TRUE_OR_POP)`, `CONTEXT_ENTER -> (BEFORE_WITH)`,
`CONTEXT_EXIT_NORMAL -> (the compiler-generated CALL at the exact With
context-expression span after three exact None loads)`, and
`CONTEXT_EXIT_EXCEPTION -> (WITH_EXCEPT_START,POP_JUMP_IF_TRUE)`.
`CONTEXT_EXIT_NORMAL` and `CONTEXT_EXIT_EXCEPTION` are synthetic AST subsites
of the `With` node with fixed role ordinals; they are not required to have an
AST `Call`. `TRUTH` binds the exact predicate AST span and short-circuit role.
The exception table and the surrounding `PUSH_EXC_INFO/RERAISE/POP_EXCEPT`
shape are frozen in the context bytecode group but are control scaffolding, not
separate provider sites. `CACHE`, `RESUME`, line markers, and jumps not assigned
to a `TRUTH` or context group are non-site instructions but retain their
positions in the code digest. Another Python minor version requires a separately reviewed
profile and KAT; a fallback “CALL family” is forbidden.

The AST characterizer first freezes an `AstSiteKey` containing
`(project_source_digest, lexical_code_path, owner_code_digest, site_kind,
ast_preorder_ordinal, ast_lineno, ast_col, ast_end_lineno, ast_end_col,
evaluation_ordinal_within_kind)`. `ast_preorder_ordinal` is assigned by a
fixed source-only visitor that visits fields in `ast.iter_fields` order but
does not descend into a nested function/lambda/comprehension code body from
its parent owner. `evaluation_ordinal_within_kind` is assigned by the closed
Python evaluation-order table: receiver/callee, positional arguments left to
right, keyword values in source order, then the enclosing operation; Boolean,
comparison, conditional, and comprehension subexpressions retain syntactic
order even when runtime short-circuiting is possible. Independently, the bytecode characterizer
freezes a `BytecodeSiteKey` containing `(owner_code_digest, site_kind, opcode,
instruction_offset, pep657_start_line, pep657_end_line, pep657_start_col,
pep657_end_col, instruction_ordinal_within_kind)`. Each manifest is
canonicalized and digested before either is exposed to the pairing step.

The bytecode characterizer groups one or more keys into a
`BytecodeSiteGroup(label,owner_code_digest,site_kind,ordered_key_labels)` by
the exact opcode-profile row and shared PEP 657 position. The pairing predicate
is fixed: owner code and exact site kind must be
equal; the bytecode position must equal the AST span or be contained by that
AST node with no smaller compatible AST descendant; and the independent
evaluation ordinal among exact-kind sites must agree. The opcode profile,
rather than prose compatibility, determines the required one- or multi-opcode
group. The pairing algorithm computes a bijection from the AST manifest to
bytecode groups from the two already frozen manifests. Zero, multiple, cross-kind,
ordinal-inconsistent, or position-ambiguous candidates are
`CALLSITE_MISMATCH`; no implementation may pair arbitrarily and copy the other
side's fields afterward.

`StructuralCallsiteKey`, `StructuralAttributeSiteKey`,
`StructuralStateSiteKey`, and `StructuralOperatorSiteKey` each contain exactly
one paired AST-key label and one paired bytecode-site-group label.
`StructuralProtocolSiteKey` is a closed union: `BYTECODE_PROTOCOL` contains the
same independent AST/bytecode-group pair for `GET_ITER`, `FOR_ITER`, and other
source-lowered protocol opcodes including `TRUTH`, `CONTEXT_ENTER`, and both
context-exit roles; `INTRINSIC_SUBSITE` contains one already
paired parent callsite/operator key, independently frozen semantic-model label,
and intrinsic-effect ordinal for behavior executed inside C/native code where
no separate project bytecode instruction exists. A capability cannot invent
the subsite because the semantic model fixes the complete effect sequence.
Comprehension nested code has its own lexical path/code digest; consumer
callbacks receive protocol keys rather than being disguised as explicit calls.

`AstSiteManifest` and `BytecodeSiteManifest` each contain literal label/root,
exact project-source-index/code digests, and the complete ordered records from
their own characterizer. `SitePairingManifest` contains literal label/root,
the interpreter-opcode-profile digest, two input manifest digests, complete
ordered bytecode groups, the complete ordered bijection, paired-site
kind, the complete intrinsic-subsite derivations from already frozen semantic
models, and pairing-algorithm version. The two input manifests are immutable
before pairing, and their characterizers share no mutable record objects.
KATs include two calls sharing one source span, chained attributes, one AST
site lowering to multiple opcodes, `If`/`While` truth jumps, a real `With`
normal exit plus its exceptional `WITH_EXCEPT_START` path and implicit exit
`CALL`, nested comprehensions with identical line numbers, and intrinsic effects with no separate opcode; each has one unique
expected pairing or one exact `CALLSITE_MISMATCH`.

`StructuralCallsiteRecord` contains that exact key, resolved callee abstract
value, receiver abstract value, ordered positional/keyword abstract values,
one normal result abstract value or bottom, and ordered exact exception
abstract values.

The two-root analyzer is a conservative, interprocedural forward abstract
interpreter over the following closed transfer table. Any AST node/operator or
semantic case not listed here is `UNKNOWN` at its first provider-relevant
frontier and fails the audit.

| Family | Supported transfer |
| --- | --- |
| literals and names | `Constant`, `Name`, `Tuple`, `List`, `Set`, `Dict`; exact literals create `ValueContract` values and container construction checks every element before use |
| attributes/subscripts | statically named `Attribute`, exact-key/index `Subscript`, and `Slice`; root/project structured fields require an exact slot/state binding, bound members require `BoundTypeMemberBinding`, namespaces require one instruction capability, and every other descriptor/protocol is a separate capability |
| operators | `UnaryOp(UAdd,USub,Not,Invert)`, `BinOp(Add,Sub,Mult,MatMult,Div,FloorDiv,Mod,Pow,LShift,RShift,BitOr,BitXor,BitAnd)`, `BoolOp(And,Or)`, and `Compare(Eq,NotEq,Lt,LtE,Gt,GtE,In,NotIn)` only for exact built-in atomic/container contracts under literal intrinsic models; the two non-atomic `BitOr` forms are exact `type | type` and exact built-in `dict_keys | dict_keys`, each requiring its own `BinaryOperatorCapability`; the type result is a provenance-bound `EXTERNAL_RESULT`, while the keys-view result is an exact bounded set after explicit iteration/hash/equality effects; `Is/IsNot` is additionally allowed for any resolved exact-identity, project-runtime-value, or singleton-atomic contract and performs no protocol dispatch; truth, membership, equality, ordering, hashing, and every other possible user dispatch schedule explicit intrinsic/protocol effects or fail |
| conditional expressions | `IfExp` and `NamedExpr`; both arms are analyzed and joined |
| strings | `JoinedStr` and `FormattedValue` only when formatting exact built-in atomics with a literal conversion/spec; custom formatting is an external call |
| calls | positional/keyword `Call` with no uncontracted star expansion; callee, receiver, every argument, and result must match a project or external capability |
| starred expansion | `Starred` only when its source is an exact finite tuple/list or a finite symbolic iterable with exact cardinality no greater than the abstract-container bound; expansion preserves item order and each element contract, otherwise it is `UNSUPPORTED_SYNTAX` |
| assignment | `Assign`, `AnnAssign`, destructuring of exact finite containers, and `AugAssign`; augmented assignment is operator transfer plus assignment, never an implicit in-place protocol exemption |
| decisions | `If` and `Assert`; both feasible arms are retained, with exact `is None`, exact-type, literal-membership, and bounded numeric comparisons refining contracts |
| loops | `For`/`While`, `Break`, `Continue`, and loop `else`; `For` requires an exact `IterableContract` and literal `ITER/NEXT` protocol capabilities, then uses a deterministic least fixpoint over the item contract and finite lattice rather than executing or value-unrolling the iterator |
| comprehensions | `ListComp`, `SetComp`, `DictComp`, and `GeneratorExp` over an exact finite container/range or `IterableContract`; a generator expression creates a symbolic single-pass `ITERATOR` bound to its nested code/environment, and consumption remains tied to explicit protocol capabilities |
| exceptions | `Try`, ordered `ExceptHandler`, `Raise`, and `finally`; normal and every exact-MRO-compatible `ExceptionContract` edge from project, external, attribute, state, and protocol outcomes are analyzed, a raise/`NO_NORMAL_RETURN` call terminates only that path, and exception construction/formatting follows ordinary call/operator rules |
| contexts | `With` only when each exact context factory, `__enter__`, and `__exit__` has its own capability and the exceptional/normal exit paths are both analyzed |
| functions | nested `FunctionDef`/`Lambda` bind their exact nested code and closure contracts; decorators and defaults are ordinary calls/values and are audited |
| simple statements | `Expr`, `Return`, `Pass`; every reachable normal return participates in the function result join |

`AsyncFunctionDef`, `Await`, `AsyncFor`, `AsyncWith`, `Yield`, `YieldFrom`,
`Match`, `TryStar`, dynamic import, `Global`, `Nonlocal` mutation, `Delete`,
unknown mutation, unbounded starred arguments, and dynamic keyword names are not
supported by this auxiliary analyzer. If the current roots acquire one, the
specification returns to design rather than silently adding a rule.

The lattice order is exact value -> bounded domain/structured union ->
`UNKNOWN`; joins keep an identical contract, form a canonical finite `UNION`,
or widen numeric bounds. Containers have a maximum abstract length of 256 and
unions a maximum of 32 alternatives. Loops iterate to a stable environment for
at most 32 passes. Interprocedural recursion is solved per strongly connected
component in deterministic source order using `frame_key_digest`; recursive
return contracts start at bottom and widen monotonically for at most 32 SCC
passes. Failure to converge produces `ABSTRACT_FIXPOINT_EXCEEDED` with
`completed=False`. No concrete candidate loop, context manager, descriptor, or
call is executed by this analysis.

Provider reachability is syntax-conservative rather than fixture-coverage
driven: both arms of every branch, the body and `else` of every loop, and every
type-compatible exception handler are analyzed even when a particular exact
fixture would make one path false or execute zero iterations. Refinement may
narrow a `ValueContract` but may not discard a syntactic provider frontier.
Thus exact root identities prevent forged-state authorization without turning
the fixture into a branch-coverage substitute.

Project-function formal contracts are bound from the actual caller abstract
values, checked against `ProjectFunctionContract`, and the computed normal and
exception outcomes must match its named outcome-contract label; annotations
are diagnostic only. An external call is accepted only when its independent
semantic model first produces a complete `StructuralCallsiteRecord` and that
record then exactly matches one `CallsiteCapability`. If the external model is
missing or returns unknown, the capability's expected outcome cannot fill the
gap. This
analysis is the machine link between a literal capability and the actual
receiver/arguments; a capability declaration alone never authorizes a call.

The 2026-08-29 read-only planning probe on the current Slice 2 candidate gives
the following non-acceptance characterization. It uses the legacy walker only
to size and enumerate syntax; it is not proof evidence:

| Root | occurrences | unique identities | project functions found | legacy per-function extraction failures | full-module source-index mappings |
| --- | ---: | ---: | ---: | ---: | ---: |
| exact oracle | 1,631 | 726 | 111 | 34 | 111/111 |
| migration | 1,811 | 808 | 127 | 38 | 127/127 |

The union of directly observed statement families is `AnnAssign, Assert,
Assign, AugAssign, Continue, Expr, For, FunctionDef, If, Raise, Return, Try,
While, With`; expression families are `Attribute, BinOp, BoolOp, Call, Compare,
Constant, Dict, DictComp, FormattedValue, GeneratorExp, IfExp, JoinedStr,
Lambda, List, ListComp, Name, Set, Starred, Subscript, Tuple, UnaryOp`.
Observed operators are `Add, And, BitOr, Div, Eq, FloorDiv, Gt, GtE, In, Is,
IsNot, Lt, LtE, Mod, Mult, Not, NotEq, NotIn, Or, Pow, Sub, USub` (the oracle
contains `Div`; migration contains `Pow`).
`Starred` is supported only by the exact finite-expansion transfer in Section
5.3; every other starred source remains intentionally unsupported.
`SeriesPair`, `ExactOracleResultV0`, and `PlanMigrationV1ToV2` are mandatory
generated-dataclass/slot probes. `_AdapterRegistrationV2`,
`_AdapterRegistryIdentityV2`, `_ResolutionOwnershipSnapshotV2`, and
`_ResolutionIdentityRecordV2` are mandatory generated-named-tuple probes.
`PlanMigrationRefusal`, `V2IntegrityError`, and `ResourceLimitError` are
mandatory `ProjectClassBinding(kind=EXCEPTION)` probes; every reached runtime
Protocol class uses `kind=RUNTIME_PROTOCOL`.
`collections.abc.Mapping` at the real `isinstance` sites is a mandatory
`ExternalClassBinding`/`SAFE_TYPE_OPERAND` probe.
`_MIGRATION_OWNED`, its exact `WeakKeyDictionary` type operations, and every
reachable `ReferenceType` referent/callback are mandatory project-runtime-state
probes, including the exact-version generated remove transfer. `_VERSIONED_NAME`
and its exact built-in-dict `groupindex`, every reached `GenericAlias`,
`UnionType`, or typing
alias, every reached project enum class including `SelectionRule` and
`MigrationFieldStatus`, and the exact closure-held `records.get` receiver/member
pair and its full derived ownership path through hidden dict, process-local
identity-token entry,
named-tuple field, weakref, callback, and defaults are mandatory
`ProjectRuntimeValueBinding` probes. The real `list | tuple` expression and
both real `source_fields.keys() | target_fields.keys()` expressions are
mandatory binary-operator probes; the latter require bounded keys-view union
effects and exact set outcomes. The oracle's
`itertools.permutations` iterator and every reached `enumerate`, `zip`, dict
view, generator consumer, and key callback are mandatory iterable/protocol
probes.

Before the first GREEN implementation, a literal `RootSyntaxInventory` for
each root must bind the exact project source hashes, code digests, AST node and
operator enums, project/external classes and behavior slots, generated
artifacts/callback transfers, process-local tokens, runtime SCCs, semantic
guards/transfers/intrinsic models, interpreter opcode profile,
AST/bytecode/pairing manifests, project-call SCCs, both graph manifests, and
counts. A machine
test independently (a) parses the complete verified module sources through
`ProjectSourceIndex` and resolves statically named call edges and (b)
disassembles the exact code objects and follows literal object-identity
global/closure/default/class edges. Both code-digest/callsite sets must equal
the reviewed inventory and each other. A missing or extra reachable node,
unmapped nested function, generated artifact, unsupported provider-relevant
frontier, or uncontracted SCC fails. This inventory is reviewed policy data,
not a manifest produced and trusted during the audit itself; neither
characterizer may add an authorization.

### 5.4 Provider graph records and results

`ReceiverBinding` contains:

- `kind: NONE | SELF | CLS | INSTANCE_OF`;
- exact owner identity; and
- exact instance identity when one already exists.

`INSTANCE_OF(cls)` is symbolic. It may be used to inspect project-owned
`__new__`/`__init__` dependencies, but it does not authorize reading unknown
instance state. An instance-field read without a prior exact binding is an
`UNRESOLVED_INSTANCE_STATE` finding. `__new__` returning a different or unknown
type is an `UNAPPROVED_FACTORY_RESULT` finding.

For a matched `GeneratedProjectArtifactBinding`, the generated init transfer
promotes `INSTANCE_OF(cls)` to a `STRUCTURED` result only after every constructor
argument/default, exact field transfer, optional project-owned `__post_init__`,
and declared result contract match. It does not read symbolic receiver state.
An existing root instance is never reconstructed: its exact
`RootStructuredStateContract` supplies the only permitted field state.

`ProviderRecord` contains:

- a tuple of structured `EdgeStep` values;
- exact value;
- depth;
- `ReceiverBinding`;
- exact globals-environment identity;
- exact root argument bindings;
- current `CallFrameBinding` and abstract local environment when the record is
  a project-owned function; and
- the edge kind that scheduled it.

The expansion key is `(value identity, receiver kind, receiver owner identity,
receiver instance identity, globals-environment digest, root-argument-contract
digest, frame_key_digest)`. It contains no newly allocated record identity. The
queue holds strong references for its full lifetime so process-local identity
values cannot be reused.

`EdgeKind` is the closed enum `ROOT | CODE | NESTED_CODE | NONLOCAL | GLOBAL |
BUILTIN | DEFAULT | KWDEFAULT | ATTRIBUTE | ATTRIBUTE_ACCESS | CALL_TARGET |
CALL_RECEIVER | CALL_ARGUMENT | CALL_KEYWORD | CALL_RESULT | CALL_EXCEPTION |
RAISE | EXCEPTION_HANDLER | PROJECT_EDGE | PROJECT_CLASS | DESCRIPTOR |
EXTERNAL_CLASS | TYPE_MEMBER |
BOUND_TYPE_MEMBER | RUNTIME_VALUE | STATE_FIELD | STATE_OPERATION |
PROCESS_LOCAL_IDENTITY | RUNTIME_STATE_REFERENCE |
STATE_EXCEPTION | CONTAINER_KEY | CONTAINER_VALUE | ARRAY_ELEMENT |
ARRAY_CONTENT_READ | NAMESPACE_ATTRIBUTE | FACTORY_RESULT | ITERATOR_FACTORY |
ITER | NEXT | ITERATOR_ITEM | DICT_VIEW | PROTOCOL_CALLBACK |
PROTOCOL_EXCEPTION | BINARY_OPERATOR | SEMANTIC_MODEL | INTRINSIC_EFFECT |
FINALIZE |
AUDIT_STATE_READ |
ROOT_STRUCTURED_FIELD | GENERATED_METHOD | GENERATED_SLOT |
NAMEDTUPLE_FIELD | WEAKREF_REFERENT | WEAKREF_CALLBACK`.
`EdgeStep` contains one `EdgeKind`, one trusted source or manifest label, and
one non-negative ordinal.

`FindingCategory` is the closed enum `FORBIDDEN_RANDOM |
FORBIDDEN_DYNAMIC_RESOLVER | RUNTIME_IMPORT | PROJECT_BINDING_DRIFT |
PROJECT_CLASS_BINDING_DRIFT | SOURCE_HASH_DRIFT | EXTERNAL_STATE_DRIFT |
RUNTIME_VALUE_BINDING_DRIFT |
STRUCTURED_STATE_DRIFT |
GENERATED_ARTIFACT_DRIFT | DESCRIPTOR_BINDING_DRIFT |
BINARY_ANCHOR_DRIFT | UNRESOLVED_CALL |
UNRESOLVED_ATTRIBUTE | UNKNOWN_VALUE_PROVENANCE | UNSUPPORTED_SYNTAX |
ABSTRACT_FIXPOINT_EXCEEDED | CALLSITE_MISMATCH | STATE_OPERATION_MISMATCH |
PROTOCOL_DISPATCH_MISMATCH | ARGUMENT_CONTRACT_MISMATCH |
RESULT_CONTRACT_MISMATCH | EXCEPTION_CONTRACT_MISMATCH |
UNAPPROVED_EXTERNAL_CALLABLE | UNAPPROVED_FACTORY |
UNAPPROVED_FACTORY_RESULT | UNAPPROVED_DESCRIPTOR |
UNAPPROVED_NAMESPACE_ESCAPE | UNAPPROVED_CARRIER |
UNRESOLVED_INSTANCE_STATE | EXCESS_AUTHORITY | ARRAY_BOUND_EXCEEDED |
ITERATOR_BOUND_EXCEEDED |
ABSTRACT_CONTAINER_BOUND_EXCEEDED | UNION_BOUND_EXCEEDED |
PROJECT_CODE_OBJECTS_EXCEEDED | STRUCTURAL_CALLSITES_EXCEEDED |
GRAPH_DEPTH_EXCEEDED | GRAPH_OBJECTS_EXCEEDED | GRAPH_RECORDS_EXCEEDED |
POLICY_RECORDS_EXCEEDED |
GRAPH_EDGES_EXCEEDED | PROJECT_CLASSES_EXCEEDED | RUNTIME_VALUES_EXCEEDED |
EXTERNAL_CLASSES_EXCEEDED | BEHAVIOR_SLOT_MANIFESTS_EXCEEDED |
PROCESS_IDENTITY_SOURCES_EXCEEDED | PROCESS_IDENTITY_TOKENS_EXCEEDED |
LOCATED_BOUND_HANDLES_EXCEEDED |
RUNTIME_STATE_SCCS_EXCEEDED | AUTHORIZATION_DEPENDENCY_NODES_EXCEEDED |
AUTHORIZATION_DEPENDENCY_EDGES_EXCEEDED |
RUNTIME_STATE_REFERENCE_EDGES_EXCEEDED |
STATE_FIELDS_EXCEEDED | GENERATED_CALLBACKS_EXCEEDED |
BOUND_MEMBERS_EXCEEDED | STATE_OPERATION_CAPABILITIES_EXCEEDED |
PROTOCOL_CAPABILITIES_EXCEEDED | BINARY_OPERATOR_CAPABILITIES_EXCEEDED |
AUDIT_STATE_READS_EXCEEDED | SEMANTIC_GUARDS_EXCEEDED |
SEMANTIC_NORMAL_TRANSFERS_EXCEEDED |
SEMANTIC_EXCEPTION_TRANSFERS_EXCEEDED | SEMANTIC_MODELS_EXCEEDED |
INTRINSIC_EFFECTS_EXCEEDED | OPERATION_OUTCOMES_EXCEEDED |
EXCEPTION_CONTRACTS_EXCEEDED`.

`AuditFinding` contains one `FindingCategory`, structured path, frontier edge,
trusted target label when one exists, and stable detail. An unmanifested target
uses the fixed label `UNLABELLED` plus its trusted edge ordinal; provider names
cannot become sort keys.

`ProviderAuditPolicy` contains the schema/version label, one exact root
function and code identity/digest, one exact root-input contract, package-root
label, one exact `LabelRegistry`, the complete cross-record-reference
classification table, and the normalized labelled tables listed by the
canonical key list below. These tables include project modules/source indexes/
function bindings/classes and
behavior-slot manifests, generated artifacts/methods/accessors/callback
transfers, external classes and runtime bindings, located-bound-callable
handles, process-local identity sources/tokens, runtime-state SCCs and both graph
manifests, value/argument/result/iterable/exception/outcome contracts,
semantic guards/normal transfers/exception transfers/models, intrinsic
effects, state transfers, all source/protocol/operator/auditor
capabilities, independently frozen AST/bytecode site manifests and their
pairing manifest plus interpreter-opcode profile, the literal root-syntax inventory, all graph/abstract-
interpreter limits, expected bootstrap digest, audit implementation source
digest, Python/NumPy versions, and a 256-bit parent challenge nonce supplied
after the child ready frame.

Every reusable entity in a top-level table has exactly one non-empty literal
`label`; every parent or capability serializes only label references. Embedded
duplicate definitions are forbidden. A label occurs in exactly one table,
and the object observed in memory must project byte-for-byte to that sole
definition. All labels are registered before validation. References in the
authorization dependency graph must then resolve and form a DAG; references
in the runtime-state graph may be cyclic only under one exact SCC record. The
exact field names/types/nullability/discriminators and order are the closed
registry in Section 5.5; optional scalars are explicit `null`, selected
collections are arrays, and no extra/default-invented fields are legal. This
normalization rule resolves nested-versus-top-level and forward-reference
ambiguity.

The `audit implementation digest` is the canonical digest of the ordered
literal path labels and current byte SHA-256 values for
`_provider_audit_bootstrap_v2.py`, `_provider_callsite_provenance_v2.py`, and
`_random_behavior_graph_v2.py`. Paths are repository-relative labels; file
discovery is forbidden. The child hashes these three regular files before the
ready frame and again after traversal. A mismatch is
`PROJECT_BINDING_DRIFT` and prevents a completed PASS.

`AuditReport` contains:

- schema/version, root label, child challenge nonce, bootstrap digest, policy
  digest, audit implementation digest, root-input-contract and normalized
  value-contract-table digests, complete capability/semantic-transfer/model/
  graph/opcode-profile/site-pairing,
  project-function/outcome/exception/protocol/operator, and
  root-syntax-inventory manifest digests;
- Python/NumPy/platform versions, runtime-binary-anchor digest, ordered project
  module/source-index/project-class/external-class/behavior-slot digests,
  process-local-token and runtime-SCC manifests, generated-artifact/method/accessor/
  project-descriptor/external-type-member/project-runtime-value/state-field/
  generated-callback/located-bound-handle/bound-member/audit-state-read digests,
  pre/post root-state
  digests, referenced
  binding/external-state pre/post digests, and the complete limits record;
- sorted findings, `completed: bool`, and the complete exact counts record for
  every finite resource dimension in Section 8, including project classes,
  runtime/state/callback/bound members, capabilities, semantic/effect models,
  outcomes/exceptions, code/callsite/object/record/edge, maximum observed
  graph/container/iterable/union/content-byte dimensions, and loop/SCC
  iterations;
- audit elapsed time as diagnostic-only data; and
- `stable_report_digest: str`, an exact lowercase SHA-256.

The normative `policy_digest` preimage is the label-based canonical form of
every `ProviderAuditPolicy` field above except live object identities, which
are represented by their unique literal labels plus verified source/state
digests. The normative stable report preimage is the canonical report record
with `stable_report_digest` and elapsed time omitted and with the `findings`
array projected from full wire records to exact `FindingStableKey` records;
its domain is `report`. No other field or nested value changes between the
wire and stable projections.

The canonical policy JSON object has exactly these keys and no others:
`schema,root_label,root_function_label,root_code_digest,root_input_contract,
package_root_label,label_registry,cross_record_reference_classifications,
project_modules,project_source_indexes,project_function_bindings,
project_classes,behavior_slot_manifests,external_classes,external_abc_states,
external_python_intrinsics,generated_artifacts,generated_methods,
generated_field_accessors,generated_callback_transfers,
external_identities,project_descriptors,external_type_members,
runtime_locator_root_nodes,runtime_locator_access_steps,
runtime_value_locators,located_bound_callable_handles,
process_local_identity_sources,process_local_identity_tokens,runtime_values,
state_fields,runtime_state_sccs,authorization_dependency_graph,
runtime_state_reference_graph,generated_stdlib_callbacks,bound_type_members,
value_contracts,root_argument_contracts,root_structured_state_contracts,
argument_contracts,result_contracts,iterable_contracts,exception_contracts,
outcome_contracts,semantic_guards,semantic_normal_transfers,
semantic_exception_transfers,semantic_models,intrinsic_effect_steps,
state_operation_transfers,project_functions,callsite_capabilities,
namespace_capabilities,attribute_capabilities,state_operation_capabilities,
protocol_capabilities,binary_operator_capabilities,audit_state_reads,
interpreter_opcode_profile,ast_site_keys,bytecode_site_keys,
bytecode_site_groups,structural_callsite_keys,structural_attribute_site_keys,
structural_state_site_keys,structural_operator_site_keys,
structural_protocol_site_keys,ast_site_manifest,bytecode_site_manifest,
site_pairing_manifest,root_syntax_inventory,limits,bootstrap_digest,
implementation_digest,runtime_binary_anchor_digest,python_version,
numpy_version,challenge_nonce`. Every plural value is an ordered JSON array;
top-level labelled tables are sorted by literal-label UTF-8 bytes, while
semantically ordered fields inside a record retain their specified order;
every optional scalar is explicit JSON `null`; empty collections are `[]`;
all nested records use exactly the normative field names in Sections 4–5.

The canonical report JSON object has exactly these keys and no others:
`schema,root_label,challenge_nonce,bootstrap_digest,policy_digest,
implementation_digest,label_registry_digest,
cross_record_reference_classifications_digest,root_input_contract_digest,
root_argument_contract_digests,root_structured_state_contract_digests,
value_contract_table_digest,
callsite_manifest_digest,capability_manifest_digest,
semantic_guard_manifest_digest,semantic_normal_transfer_manifest_digest,
semantic_exception_transfer_manifest_digest,semantic_model_manifest_digest,
authorization_dependency_graph_digest,runtime_state_reference_graph_digest,
runtime_state_scc_manifest_digest,process_local_identity_source_manifest_digest,
process_local_identity_token_manifest_digest,
interpreter_opcode_profile_digest,site_pairing_manifest_digest,
project_function_manifest_digest,outcome_manifest_digest,
exception_manifest_digest,protocol_manifest_digest,operator_manifest_digest,
root_syntax_inventory_digest,python_version,
numpy_version,platform,runtime_binary_anchor_digest,project_module_digests,
project_source_index_digests,project_class_digests,
behavior_slot_manifest_digests,external_class_digests,
external_abc_state_digests,external_python_intrinsic_digests,
generated_artifact_digests,generated_method_digests,
generated_field_accessor_digests,project_descriptor_digests,
external_type_member_digests,runtime_value_locator_digests,
located_bound_callable_handle_digests,runtime_value_digests,
state_field_digests,generated_callback_transfer_digests,
generated_callback_digests,bound_member_digests,state_operation_transfer_digests,
audit_state_read_digests,site_key_table_digest,
root_state_pre_digests,
root_state_post_digests,referenced_binding_pre_digests,
referenced_binding_post_digests,external_state_pre_digests,
external_state_post_digests,limits,findings,completed,counts,
elapsed_seconds,stable_report_digest`. Digest preimages retain all keys; only
`elapsed_seconds` and `stable_report_digest` are omitted, and every full
`FindingReportRecord` is replaced by its exact `FindingStableKey`, in the
stable-report preimage. Missing, extra, renamed, or implementation-defaulted
keys fail KATs.
The wire frame is exactly
`b"PROVIDER_AUDIT_REPORT_V2 " + AUDIT_CANONICAL_JSON_V2(full_report) + b"\n"`.
No alternate whitespace, key order, prefix, encoding, or second frame is
accepted. The parent accepts a failure report as valid transport evidence only
when its nonce equals the one-use challenge and its schema/stable digest
recompute; this is not PASS. `audit_pass` is true only when transport is valid,
`completed=True`, `findings == ()`, and every bootstrap/policy/implementation
and pre/post state digest matches. Replaying a report from another child/run
fails even if its source hashes are unchanged.

Eight exact known-answer vectors prevent the implementation from selecting a
different serializer or report projection. The first canonical
`value-contract` bytes are exactly:

```text
{"kind":"EXACT_ATOMIC","label":"kat.float.half","payload":{"atomic_type_label":"builtin.float","atomic_value":{"$float":"0x1.0000000000000p-1"}}}
```

Their domain-separated SHA-256 is exactly
`21402bf058b883ade1408dcf131eeb8da5b940f146d5cb0fcf3b1509808688bb`.

The following second vector is the seventh-revision serialization-only policy
fixture retained as a negative KAT. It omits eighth-revision graph, transfer,
type-operand, token, SCC, opcode-profile, byte-limit, and count keys and must be
rejected as an incomplete policy. Its historical bytes are exactly:

```text
{"argument_contracts":[],"ast_site_manifest":null,"attribute_capabilities":[],"audit_state_reads":[],"binary_operator_capabilities":[],"bootstrap_digest":"0000000000000000000000000000000000000000000000000000000000000000","bound_type_members":[],"bytecode_site_manifest":null,"callsite_capabilities":[],"challenge_nonce":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","exception_contracts":[],"external_identities":[],"external_type_members":[],"generated_artifacts":[],"generated_callback_transfers":[],"generated_field_accessors":[],"generated_methods":[],"generated_stdlib_callbacks":[],"implementation_digest":"0000000000000000000000000000000000000000000000000000000000000000","intrinsic_effect_steps":[],"iterable_contracts":[],"limits":{"abstract_container_length":256,"abstract_iterable_cardinality":256,"audit_state_reads":128,"binary_operator_capabilities":256,"bound_type_members":128,"exception_contracts":2048,"generated_stdlib_callbacks":64,"graph_depth":32,"graph_edges":6144,"intrinsic_effect_steps":4096,"loop_fixpoint_passes":32,"operation_outcome_contracts":2048,"project_classes":256,"project_code_objects":224,"project_runtime_values":256,"protocol_capabilities":1024,"provider_records":3072,"scc_fixpoint_passes":32,"semantic_models":2048,"state_fields":768,"state_operation_capabilities":1024,"structural_callsites":1400,"symbolic_iterator_views":256,"union_alternatives":32,"unique_object_identities":1024},"namespace_capabilities":[],"numpy_version":null,"outcome_contracts":[],"package_root_label":"KAT_PACKAGE","project_classes":[],"project_descriptors":[],"project_functions":[],"project_modules":[],"project_source_indexes":[],"protocol_capabilities":[],"python_version":"3.12.11","result_contracts":[],"root_code_digest":"0000000000000000000000000000000000000000000000000000000000000000","root_function_label":"KAT_FUNCTION","root_input_contract":null,"root_label":"KAT_ROOT","root_syntax_inventory":null,"runtime_binary_anchor_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_value_locators":[],"runtime_values":[],"schema":"selcal.provider-audit-policy.v2","semantic_models":[],"site_pairing_manifest":null,"state_fields":[],"state_operation_capabilities":[],"state_operation_transfers":[],"value_contracts":[]}
```

With domain `policy`, its digest is exactly
`53067a68fb5057aca0a0ed15c64906ec2349c3c716590a9a7417e84a411d41b4`.

The following third vector is the seventh-revision serialization-only report
fixture retained as a negative KAT. It omits the new manifests, complete limits,
and observed-maximum counts and must be rejected before transport/PASS.
`elapsed_seconds` and `stable_report_digest` are absent. Its historical bytes
are exactly:

```text
{"audit_state_read_digests":[],"bootstrap_digest":"0000000000000000000000000000000000000000000000000000000000000000","bound_member_digests":[],"callsite_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","capability_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","challenge_nonce":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","completed":false,"counts":{"audit_state_reads":0,"binary_operator_capabilities":0,"bound_type_members":0,"code_objects":0,"edges":0,"exception_contracts":0,"generated_stdlib_callbacks":0,"intrinsic_effect_steps":0,"operation_outcome_contracts":0,"project_classes":0,"project_runtime_values":0,"protocol_capabilities":0,"provider_records":0,"scc_iterations":0,"semantic_models":0,"state_fields":0,"state_operation_capabilities":0,"structural_callsites":0,"symbolic_iterator_views":0,"unique_objects":0},"exception_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","external_state_post_digests":[],"external_state_pre_digests":[],"external_type_member_digests":[],"findings":[],"generated_artifact_digests":[],"generated_callback_digests":[],"generated_field_accessor_digests":[],"generated_method_digests":[],"implementation_digest":"0000000000000000000000000000000000000000000000000000000000000000","limits":{"abstract_container_length":256,"abstract_iterable_cardinality":256,"audit_state_reads":128,"binary_operator_capabilities":256,"bound_type_members":128,"exception_contracts":2048,"generated_stdlib_callbacks":64,"graph_depth":32,"graph_edges":6144,"intrinsic_effect_steps":4096,"loop_fixpoint_passes":32,"operation_outcome_contracts":2048,"project_classes":256,"project_code_objects":224,"project_runtime_values":256,"protocol_capabilities":1024,"provider_records":3072,"scc_fixpoint_passes":32,"semantic_models":2048,"state_fields":768,"state_operation_capabilities":1024,"structural_callsites":1400,"symbolic_iterator_views":256,"union_alternatives":32,"unique_object_identities":1024},"numpy_version":null,"operator_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","outcome_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","platform":"KAT","policy_digest":"0000000000000000000000000000000000000000000000000000000000000000","project_class_digests":[],"project_descriptor_digests":[],"project_function_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","project_module_digests":[],"project_source_index_digests":[],"protocol_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","python_version":"3.12.11","referenced_binding_post_digests":[],"referenced_binding_pre_digests":[],"root_input_contract_digest":"0000000000000000000000000000000000000000000000000000000000000000","root_label":"KAT_ROOT","root_state_post_digests":[],"root_state_pre_digests":[],"root_syntax_inventory_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_binary_anchor_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_value_digests":[],"schema":"selcal.provider-audit-report.v2","semantic_model_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","site_pairing_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","state_field_digests":[],"value_contract_table_digest":"0000000000000000000000000000000000000000000000000000000000000000"}
```

With domain `report`, its digest is exactly
`01763b95fac46f0cba4c2b55fa31412d156734bcb3f65fcca05a2fb86b7f4fa0`.

The fourth vector is the eighth-revision incomplete-policy serialization
fixture retained as a negative KAT. It has the former 60 canonical policy keys
but omits the ninth-revision registry, explicit reusable-record tables,
identity-source, ABC, external-Python, site-key, and edge-budget keys. Its exact
historical bytes are:

```text
{"argument_contracts":[],"ast_site_manifest":null,"attribute_capabilities":[],"audit_state_reads":[],"authorization_dependency_graph":null,"behavior_slot_manifests":[],"binary_operator_capabilities":[],"bootstrap_digest":"0000000000000000000000000000000000000000000000000000000000000000","bound_type_members":[],"bytecode_site_manifest":null,"callsite_capabilities":[],"challenge_nonce":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","exception_contracts":[],"external_classes":[],"external_identities":[],"external_type_members":[],"generated_artifacts":[],"generated_callback_transfers":[],"generated_field_accessors":[],"generated_methods":[],"generated_stdlib_callbacks":[],"implementation_digest":"0000000000000000000000000000000000000000000000000000000000000000","interpreter_opcode_profile":null,"intrinsic_effect_steps":[],"iterable_contracts":[],"limits":{"abstract_container_length":256,"abstract_iterable_cardinality":256,"audit_state_reads":128,"authorization_dependency_nodes":8192,"behavior_slot_manifests":256,"binary_operator_capabilities":256,"bound_type_members":128,"exception_contracts":2048,"external_classes":64,"generated_stdlib_callbacks":64,"graph_depth":32,"graph_edges":6144,"intrinsic_effect_steps":4096,"located_bound_callable_handles":128,"loop_fixpoint_passes":32,"numeric_array_content_bytes":8388608,"object_array_canonical_bytes":1048576,"operation_outcome_contracts":2048,"policy_table_records":16384,"process_local_identity_tokens":64,"project_classes":256,"project_code_objects":224,"project_runtime_values":256,"protocol_capabilities":1024,"provider_records":3072,"runtime_state_reference_edges":2048,"runtime_state_sccs":64,"scc_fixpoint_passes":32,"semantic_exception_transfers":2048,"semantic_guards":4096,"semantic_models":2048,"semantic_normal_transfers":2048,"state_fields":768,"state_operation_capabilities":1024,"structural_callsites":1400,"symbolic_iterator_views":256,"union_alternatives":32,"unique_object_identities":1024},"located_bound_callable_handles":[],"namespace_capabilities":[],"numpy_version":null,"outcome_contracts":[],"package_root_label":"KAT_PACKAGE","process_local_identity_tokens":[],"project_classes":[],"project_descriptors":[],"project_functions":[],"project_modules":[],"project_source_indexes":[],"protocol_capabilities":[],"python_version":"3.12.11","result_contracts":[],"root_code_digest":"0000000000000000000000000000000000000000000000000000000000000000","root_function_label":"KAT_FUNCTION","root_input_contract":null,"root_label":"KAT_ROOT","root_syntax_inventory":null,"runtime_binary_anchor_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_state_reference_graph":null,"runtime_state_sccs":[],"runtime_value_locators":[],"runtime_values":[],"schema":"selcal.provider-audit-policy.v2","semantic_exception_transfers":[],"semantic_guards":[],"semantic_models":[],"semantic_normal_transfers":[],"site_pairing_manifest":null,"state_fields":[],"state_operation_capabilities":[],"state_operation_transfers":[],"value_contracts":[]}
```

With domain `policy`, its digest is exactly
`b7dbbf9f0b2a8bc61aae1709368d60208d631207abf6a92d56284838a9bb0ea4`.

The fifth vector is the eighth-revision stable-report preimage retained as a
negative KAT. It has the former 59 stable keys and must now fail the current
schema for its exact missing-key and missing-count sets. Its exact historical
bytes are:

```text
{"audit_state_read_digests":[],"authorization_dependency_graph_digest":"0000000000000000000000000000000000000000000000000000000000000000","behavior_slot_manifest_digests":[],"bootstrap_digest":"0000000000000000000000000000000000000000000000000000000000000000","bound_member_digests":[],"callsite_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","capability_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","challenge_nonce":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","completed":false,"counts":{"audit_state_reads":0,"authorization_dependency_nodes":0,"behavior_slot_manifests":0,"binary_operator_capabilities":0,"bound_type_members":0,"code_objects":0,"edges":0,"exception_contracts":0,"external_classes":0,"generated_stdlib_callbacks":0,"intrinsic_effect_steps":0,"located_bound_callable_handles":0,"loop_fixpoint_iterations":0,"max_abstract_container_length":0,"max_abstract_iterable_cardinality":0,"max_graph_depth":0,"max_numeric_array_content_bytes":0,"max_object_array_canonical_bytes":0,"max_union_alternatives":0,"operation_outcome_contracts":0,"policy_table_records":0,"process_local_identity_tokens":0,"project_classes":0,"project_runtime_values":0,"protocol_capabilities":0,"provider_records":0,"runtime_state_reference_edges":0,"runtime_state_sccs":0,"scc_fixpoint_iterations":0,"semantic_exception_transfers":0,"semantic_guards":0,"semantic_models":0,"semantic_normal_transfers":0,"state_fields":0,"state_operation_capabilities":0,"structural_callsites":0,"symbolic_iterator_views":0,"unique_objects":0},"exception_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","external_class_digests":[],"external_state_post_digests":[],"external_state_pre_digests":[],"external_type_member_digests":[],"findings":[],"generated_artifact_digests":[],"generated_callback_digests":[],"generated_callback_transfer_digests":[],"generated_field_accessor_digests":[],"generated_method_digests":[],"implementation_digest":"0000000000000000000000000000000000000000000000000000000000000000","interpreter_opcode_profile_digest":"0000000000000000000000000000000000000000000000000000000000000000","limits":{"abstract_container_length":256,"abstract_iterable_cardinality":256,"audit_state_reads":128,"authorization_dependency_nodes":8192,"behavior_slot_manifests":256,"binary_operator_capabilities":256,"bound_type_members":128,"exception_contracts":2048,"external_classes":64,"generated_stdlib_callbacks":64,"graph_depth":32,"graph_edges":6144,"intrinsic_effect_steps":4096,"located_bound_callable_handles":128,"loop_fixpoint_passes":32,"numeric_array_content_bytes":8388608,"object_array_canonical_bytes":1048576,"operation_outcome_contracts":2048,"policy_table_records":16384,"process_local_identity_tokens":64,"project_classes":256,"project_code_objects":224,"project_runtime_values":256,"protocol_capabilities":1024,"provider_records":3072,"runtime_state_reference_edges":2048,"runtime_state_sccs":64,"scc_fixpoint_passes":32,"semantic_exception_transfers":2048,"semantic_guards":4096,"semantic_models":2048,"semantic_normal_transfers":2048,"state_fields":768,"state_operation_capabilities":1024,"structural_callsites":1400,"symbolic_iterator_views":256,"union_alternatives":32,"unique_object_identities":1024},"located_bound_callable_handle_digests":[],"numpy_version":null,"operator_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","outcome_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","platform":"KAT","policy_digest":"0000000000000000000000000000000000000000000000000000000000000000","process_local_identity_token_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","project_class_digests":[],"project_descriptor_digests":[],"project_function_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","project_module_digests":[],"project_source_index_digests":[],"protocol_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","python_version":"3.12.11","referenced_binding_post_digests":[],"referenced_binding_pre_digests":[],"root_input_contract_digest":"0000000000000000000000000000000000000000000000000000000000000000","root_label":"KAT_ROOT","root_state_post_digests":[],"root_state_pre_digests":[],"root_syntax_inventory_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_binary_anchor_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_state_reference_graph_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_state_scc_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_value_digests":[],"runtime_value_locator_digests":[],"schema":"selcal.provider-audit-report.v2","semantic_exception_transfer_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","semantic_guard_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","semantic_model_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","semantic_normal_transfer_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","site_pairing_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","state_field_digests":[],"state_operation_transfer_digests":[],"value_contract_table_digest":"0000000000000000000000000000000000000000000000000000000000000000"}
```

With domain `report`, its digest is exactly
`a7d8781fd0083716f7ce6b84b40678f1bc94a20e9258a948b318bcdc18440536`.
The sixth vector is the authoritative ninth-revision incomplete-policy key
projection. It has all 78 current policy keys and all 40 limit keys; null/empty
mandatory records make it non-authorizing. Its exact bytes are:

```text
{"argument_contracts":[],"ast_site_keys":[],"ast_site_manifest":null,"attribute_capabilities":[],"audit_state_reads":[],"authorization_dependency_graph":null,"behavior_slot_manifests":[],"binary_operator_capabilities":[],"bootstrap_digest":"0000000000000000000000000000000000000000000000000000000000000000","bound_type_members":[],"bytecode_site_groups":[],"bytecode_site_keys":[],"bytecode_site_manifest":null,"callsite_capabilities":[],"challenge_nonce":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","cross_record_reference_classifications":[],"exception_contracts":[],"external_abc_states":[],"external_classes":[],"external_identities":[],"external_python_intrinsics":[],"external_type_members":[],"generated_artifacts":[],"generated_callback_transfers":[],"generated_field_accessors":[],"generated_methods":[],"generated_stdlib_callbacks":[],"implementation_digest":"0000000000000000000000000000000000000000000000000000000000000000","interpreter_opcode_profile":null,"intrinsic_effect_steps":[],"iterable_contracts":[],"label_registry":null,"limits":{"abstract_container_length":256,"abstract_iterable_cardinality":256,"audit_state_reads":128,"authorization_dependency_edges":16384,"authorization_dependency_nodes":8192,"behavior_slot_manifests":256,"binary_operator_capabilities":256,"bound_type_members":128,"exception_contracts":2048,"external_classes":64,"generated_stdlib_callbacks":64,"graph_depth":32,"graph_edges":6144,"intrinsic_effect_steps":4096,"located_bound_callable_handles":128,"loop_fixpoint_passes":32,"numeric_array_content_bytes":8388608,"object_array_canonical_bytes":1048576,"operation_outcome_contracts":2048,"policy_table_records":16384,"process_local_identity_sources":64,"process_local_identity_tokens":64,"project_classes":256,"project_code_objects":224,"project_runtime_values":256,"protocol_capabilities":1024,"provider_records":3072,"runtime_state_reference_edges":2048,"runtime_state_sccs":64,"scc_fixpoint_passes":32,"semantic_exception_transfers":2048,"semantic_guards":4096,"semantic_models":2048,"semantic_normal_transfers":2048,"state_fields":768,"state_operation_capabilities":1024,"structural_callsites":1400,"symbolic_iterator_views":256,"union_alternatives":32,"unique_object_identities":1024},"located_bound_callable_handles":[],"namespace_capabilities":[],"numpy_version":null,"outcome_contracts":[],"package_root_label":"KAT_PACKAGE","process_local_identity_sources":[],"process_local_identity_tokens":[],"project_classes":[],"project_descriptors":[],"project_function_bindings":[],"project_functions":[],"project_modules":[],"project_source_indexes":[],"protocol_capabilities":[],"python_version":"3.12.11","result_contracts":[],"root_argument_contracts":[],"root_code_digest":"0000000000000000000000000000000000000000000000000000000000000000","root_function_label":"KAT_FUNCTION","root_input_contract":null,"root_label":"KAT_ROOT","root_structured_state_contracts":[],"root_syntax_inventory":null,"runtime_binary_anchor_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_locator_access_steps":[],"runtime_locator_root_nodes":[],"runtime_state_reference_graph":null,"runtime_state_sccs":[],"runtime_value_locators":[],"runtime_values":[],"schema":"selcal.provider-audit-policy.v2","semantic_exception_transfers":[],"semantic_guards":[],"semantic_models":[],"semantic_normal_transfers":[],"site_pairing_manifest":null,"state_fields":[],"state_operation_capabilities":[],"state_operation_transfers":[],"structural_attribute_site_keys":[],"structural_callsite_keys":[],"structural_operator_site_keys":[],"structural_protocol_site_keys":[],"structural_state_site_keys":[],"value_contracts":[]}
```

With domain `policy`, its digest is exactly
`f89aa32e2b7c0337961f8118d7e7e44c98b010dccb89a862bd35115599a6a4c1`.

The seventh vector is the authoritative ninth-revision stable-report preimage.
It has all 67 stable keys and all 40 count keys; the two wire-only fields are
absent. Its exact bytes are:

```text
{"audit_state_read_digests":[],"authorization_dependency_graph_digest":"0000000000000000000000000000000000000000000000000000000000000000","behavior_slot_manifest_digests":[],"bootstrap_digest":"0000000000000000000000000000000000000000000000000000000000000000","bound_member_digests":[],"callsite_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","capability_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","challenge_nonce":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","completed":false,"counts":{"audit_state_reads":0,"authorization_dependency_edges":0,"authorization_dependency_nodes":0,"behavior_slot_manifests":0,"binary_operator_capabilities":0,"bound_type_members":0,"code_objects":0,"edges":0,"exception_contracts":0,"external_classes":0,"generated_stdlib_callbacks":0,"intrinsic_effect_steps":0,"located_bound_callable_handles":0,"loop_fixpoint_iterations":0,"max_abstract_container_length":0,"max_abstract_iterable_cardinality":0,"max_graph_depth":0,"max_numeric_array_content_bytes":0,"max_object_array_canonical_bytes":0,"max_union_alternatives":0,"operation_outcome_contracts":0,"policy_table_records":0,"process_local_identity_sources":0,"process_local_identity_tokens":0,"project_classes":0,"project_runtime_values":0,"protocol_capabilities":0,"provider_records":0,"runtime_state_reference_edges":0,"runtime_state_sccs":0,"scc_fixpoint_iterations":0,"semantic_exception_transfers":0,"semantic_guards":0,"semantic_models":0,"semantic_normal_transfers":0,"state_fields":0,"state_operation_capabilities":0,"structural_callsites":0,"symbolic_iterator_views":0,"unique_objects":0},"cross_record_reference_classifications_digest":"0000000000000000000000000000000000000000000000000000000000000000","exception_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","external_abc_state_digests":[],"external_class_digests":[],"external_python_intrinsic_digests":[],"external_state_post_digests":[],"external_state_pre_digests":[],"external_type_member_digests":[],"findings":[],"generated_artifact_digests":[],"generated_callback_digests":[],"generated_callback_transfer_digests":[],"generated_field_accessor_digests":[],"generated_method_digests":[],"implementation_digest":"0000000000000000000000000000000000000000000000000000000000000000","interpreter_opcode_profile_digest":"0000000000000000000000000000000000000000000000000000000000000000","label_registry_digest":"0000000000000000000000000000000000000000000000000000000000000000","limits":{"abstract_container_length":256,"abstract_iterable_cardinality":256,"audit_state_reads":128,"authorization_dependency_edges":16384,"authorization_dependency_nodes":8192,"behavior_slot_manifests":256,"binary_operator_capabilities":256,"bound_type_members":128,"exception_contracts":2048,"external_classes":64,"generated_stdlib_callbacks":64,"graph_depth":32,"graph_edges":6144,"intrinsic_effect_steps":4096,"located_bound_callable_handles":128,"loop_fixpoint_passes":32,"numeric_array_content_bytes":8388608,"object_array_canonical_bytes":1048576,"operation_outcome_contracts":2048,"policy_table_records":16384,"process_local_identity_sources":64,"process_local_identity_tokens":64,"project_classes":256,"project_code_objects":224,"project_runtime_values":256,"protocol_capabilities":1024,"provider_records":3072,"runtime_state_reference_edges":2048,"runtime_state_sccs":64,"scc_fixpoint_passes":32,"semantic_exception_transfers":2048,"semantic_guards":4096,"semantic_models":2048,"semantic_normal_transfers":2048,"state_fields":768,"state_operation_capabilities":1024,"structural_callsites":1400,"symbolic_iterator_views":256,"union_alternatives":32,"unique_object_identities":1024},"located_bound_callable_handle_digests":[],"numpy_version":null,"operator_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","outcome_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","platform":"KAT","policy_digest":"0000000000000000000000000000000000000000000000000000000000000000","process_local_identity_source_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","process_local_identity_token_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","project_class_digests":[],"project_descriptor_digests":[],"project_function_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","project_module_digests":[],"project_source_index_digests":[],"protocol_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","python_version":"3.12.11","referenced_binding_post_digests":[],"referenced_binding_pre_digests":[],"root_argument_contract_digests":[],"root_input_contract_digest":"0000000000000000000000000000000000000000000000000000000000000000","root_label":"KAT_ROOT","root_state_post_digests":[],"root_state_pre_digests":[],"root_structured_state_contract_digests":[],"root_syntax_inventory_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_binary_anchor_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_state_reference_graph_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_state_scc_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","runtime_value_digests":[],"runtime_value_locator_digests":[],"schema":"selcal.provider-audit-report.v2","semantic_exception_transfer_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","semantic_guard_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","semantic_model_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","semantic_normal_transfer_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","site_key_table_digest":"0000000000000000000000000000000000000000000000000000000000000000","site_pairing_manifest_digest":"0000000000000000000000000000000000000000000000000000000000000000","state_field_digests":[],"state_operation_transfer_digests":[],"value_contract_table_digest":"0000000000000000000000000000000000000000000000000000000000000000"}
```

With domain `report`, its digest is exactly
`2cb1ebdc5b42547cf90dd170f495635612b106055f8296bd476e83cb3a73a0dd`.

The eighth vector is a non-empty label/reference closure KAT spanning a root
input and argument, value contract, AST/bytecode/group/structural site, semantic
transfer/model, outcome, and call capability. Its exact bytes are:

```text
{"authorization_edges":[{"ordinal":0,"source_label":"root.arg","target_label":"value.scalar"},{"ordinal":1,"source_label":"root.input","target_label":"root.arg"},{"ordinal":3,"source_label":"site.call","target_label":"ast.call"},{"ordinal":4,"source_label":"site.call","target_label":"bc.group"},{"ordinal":5,"source_label":"model.call","target_label":"transfer.normal"},{"ordinal":6,"source_label":"cap.call","target_label":"site.call"},{"ordinal":7,"source_label":"cap.call","target_label":"model.call"}],"definitions":[{"label":"ast.call","owner_table":"ast_site_keys","record_digest":"cfc988cec0eb47b36bc90d45c91c4d89c59ebc2df1444059db866201e2e01339","record_ordinal":0},{"label":"bc.call","owner_table":"bytecode_site_keys","record_digest":"63838cbc8ba1011885910e2edc5913b6738f36a26d84648d8d4cc0d20fce308b","record_ordinal":0},{"label":"bc.group","owner_table":"bytecode_site_groups","record_digest":"b1071b2a1e307e29f807b2c185a8c77850a7eccea9a1451794913245bc7ea0fa","record_ordinal":0},{"label":"cap.call","owner_table":"callsite_capabilities","record_digest":"fb67e7639f26cde59dec0be25fc83ab3738a82c2500cb8db4f9a0dfead894f31","record_ordinal":0},{"label":"model.call","owner_table":"semantic_models","record_digest":"99b5b0598b8796ff837c59be4e34758b14765ef560df916392949251eb00eabd","record_ordinal":0},{"label":"outcome.call","owner_table":"outcome_contracts","record_digest":"580563ad04030d423c45e5eb49209e5e91a1cb264c91b2e3303784bfcd106f9b","record_ordinal":0},{"label":"root.arg","owner_table":"root_argument_contracts","record_digest":"b09e85f1d9bdec879d046bfc45eb7b09f75604424d8eba0dddc9516033d06006","record_ordinal":0},{"label":"root.input","owner_table":"root_input_contract","record_digest":"b64e2b8db12c1c9311700f123641695bfb94697bdcd76da4bf2c3d63ae1c8467","record_ordinal":0},{"label":"site.call","owner_table":"structural_callsite_keys","record_digest":"d13625eb2986f9d1c4037641c8eecb5830eb7b92ad0d68456e55083da11d751a","record_ordinal":0},{"label":"transfer.normal","owner_table":"semantic_normal_transfers","record_digest":"6bf4a6ffe58e61fb960db443e674458f71fc30e83c646b93648b6e35262bea35","record_ordinal":0},{"label":"value.scalar","owner_table":"value_contracts","record_digest":"586be268191df0317b465116626afd8bf070c49529b64b0682b2e19ecf0376e1","record_ordinal":0}],"reference_classifications":[{"field_name":"atomic_value_contract_label","field_ordinal":0,"kind":"AUTH_REQUIRES","source_label":"root.arg","target_label":"value.scalar"},{"field_name":"argument_labels","field_ordinal":0,"kind":"AUTH_REQUIRES","source_label":"root.input","target_label":"root.arg"},{"field_name":"ordered_key_labels","field_ordinal":0,"kind":"OWNS","source_label":"bc.group","target_label":"bc.call"},{"field_name":"ast_key_label","field_ordinal":0,"kind":"AUTH_REQUIRES","source_label":"site.call","target_label":"ast.call"},{"field_name":"bytecode_site_group_label","field_ordinal":0,"kind":"AUTH_REQUIRES","source_label":"site.call","target_label":"bc.group"},{"field_name":"normal_transfer_label","field_ordinal":0,"kind":"AUTH_REQUIRES","source_label":"model.call","target_label":"transfer.normal"},{"field_name":"site_key_label","field_ordinal":0,"kind":"AUTH_REQUIRES","source_label":"cap.call","target_label":"site.call"},{"field_name":"semantic_model_label","field_ordinal":0,"kind":"AUTH_REQUIRES","source_label":"cap.call","target_label":"model.call"},{"field_name":"outcome_contract_label","field_ordinal":0,"kind":"VALIDATES","source_label":"cap.call","target_label":"outcome.call"}],"runtime_edges":[],"topological_order":["value.scalar","root.arg","root.input","ast.call","bc.call","bc.group","site.call","transfer.normal","model.call","outcome.call","cap.call"]}
```

With domain `label-registry`, its digest is exactly
`91fb1fa75093efac06324edaa7973409c285b7ab64cdc16b79592489987bf76f`. Validation must reject each one-at-a-time orphan,
duplicate definition, wrong owner ordinal/digest, missing or duplicate reference
classification, authorization edge mismatch, runtime-edge mismatch, and invalid
topological order mutation of this fixture.
The implementation test recomputes all eight vectors from literal expected
bytes. Vectors 1, 6, 7, and 8 must match; vectors 2 and 3 fail their historical
missing-key sets; vectors 4 and 5 match their historical digest bytes but fail
the ninth-revision schema for their exact missing-key/count sets. The test does
not regenerate any expected bytes through the function under test.

Finding sorting never calls candidate equality, hashing, ordering, or `repr`.
Membership in live identity manifests uses only `is`-based linear checks.
Value-contract intersection and containment instead use the closed canonical
policy-data algebra in Section 5.2, including trusted literal/range arithmetic;
they never call an operation on a candidate value. Provider-controlled
module/type names may appear in diagnostics only
after the finding category is decided.

The normative trigger mapping is exhaustive and rows are mutually exclusive by
their written exclusions. `Priority` selects the category
when one frontier satisfies multiple rows; lower numbers win and table order
breaks a remaining equal-priority tie. Drift preflight order is exactly binary
anchor, source bytes, project ownership, project-class/behavior-slot binding,
external-class binding, runtime-value locator/token/identity/SCC, generated
artifact, descriptor/member binding, external callable state, then
structured/root state. Each later drift row applies only
after all earlier
binding layers match. Drift discovered only in the post-traversal recheck is
appended after already-recorded findings but still makes `completed=False`.

| Category | Unique first-frontier trigger | completed | Priority |
| --- | --- | --- | ---: |
| `BINARY_ANCHOR_DRIFT` | runtime executable/library or approved extension path/size/byte digest differs | false | 0 |
| `SOURCE_HASH_DRIFT` | any bound project/module/implementation/stdlib/external regular-file byte SHA differs after the binary anchor matches | false | 0 |
| `PROJECT_BINDING_DRIFT` | exact project module/globals/origin/source-index or implementation-file pre/post identity differs after all source byte hashes match, excluding a matched project-class record | false | 0 |
| `PROJECT_CLASS_BINDING_DRIFT` | exact project class statement/identity/base/metaclass/MRO/class-member/behavior-slot/finalizer/protocol/constructor dependency differs after module/source-index ownership matches | false | 0 |
| `RUNTIME_VALUE_BINDING_DRIFT` | a literal runtime-value locator, process-local identity token, located bound-callable handle, runtime-SCC shape, located identity/type/kind/provenance, closure owner/freevar, or parent containment path differs after project ownership matches | false | 0 |
| `GENERATED_ARTIFACT_DRIFT` | an exact generated dataclass, named-tuple, or enum parameter/field/member/default/method/code/slot/tuplegetter record differs after its module source and owner binding match | false | 0 |
| `DESCRIPTOR_BINDING_DRIFT` | an exact project descriptor/class constant, external type member, or bound type-member owner/name/kind/identity/receiver/outcome binding differs after its source/binary and runtime locator match | false | 0 |
| `EXTERNAL_STATE_DRIFT` | a non-binary external intrinsic field, declared accessor or canonical container snapshot, external-class namespace/MRO/metaclass/ABC state, callable/member implementation state, state-dictionary key set/content, generated-stdlib-callback code/default/closure recipe, or pre/post external state digest differs after identity metadata matches | false | 0 |
| `STRUCTURED_STATE_DRIFT` | a root structured input, project runtime-value field/content, nested identity/container, weakref referent/callback, array content, or pre/post structured state digest differs after all binding metadata matches | false | 0 |
| `PROJECT_CODE_OBJECTS_EXCEEDED` | scheduling the next project code object beyond the active policy limit (acceptance limit 224) | false | 1 |
| `STRUCTURAL_CALLSITES_EXCEEDED` | registering the next structural callsite beyond the active policy limit (acceptance limit 1,400) | false | 1 |
| `GRAPH_DEPTH_EXCEEDED` | scheduling a record beyond the active depth limit (acceptance limit 32) | false | 1 |
| `GRAPH_OBJECTS_EXCEEDED` | registering the next unique identity beyond the active policy limit (acceptance limit 1,024) | false | 1 |
| `GRAPH_RECORDS_EXCEEDED` | registering the next provider-context record beyond the active policy limit (acceptance limit 3,072) | false | 1 |
| `POLICY_RECORDS_EXCEEDED` | registering the next labelled top-level policy-table record beyond the active policy limit (acceptance limit 16,384) | false | 1 |
| `GRAPH_EDGES_EXCEEDED` | scheduling the next graph edge beyond the active policy limit (acceptance limit 6,144) | false | 1 |
| `PROJECT_CLASSES_EXCEEDED` | registering the next project-class binding beyond its active limit | false | 1 |
| `BEHAVIOR_SLOT_MANIFESTS_EXCEEDED` | registering the next behavior-slot manifest beyond its active limit | false | 1 |
| `EXTERNAL_CLASSES_EXCEEDED` | registering the next external-class/type-operand binding beyond its active limit | false | 1 |
| `RUNTIME_VALUES_EXCEEDED` | registering the next project runtime-value binding beyond its active limit | false | 1 |
| `PROCESS_IDENTITY_SOURCES_EXCEEDED` | before resolving a locator, calling `id`, constructing a projection, allocating a token, or adding a graph edge, registering the next process-local identity source would exceed its active limit | false | 1 |
| `PROCESS_IDENTITY_TOKENS_EXCEEDED` | registering the next process-local identity token beyond its active limit | false | 1 |
| `LOCATED_BOUND_HANDLES_EXCEEDED` | registering the next located bound-callable handle beyond its active limit | false | 1 |
| `RUNTIME_STATE_SCCS_EXCEEDED` | registering the next runtime-state SCC binding beyond its active limit | false | 1 |
| `AUTHORIZATION_DEPENDENCY_NODES_EXCEEDED` | registering the next authorization-dependency node beyond its active limit | false | 1 |
| `AUTHORIZATION_DEPENDENCY_EDGES_EXCEEDED` | registering the next authorization-dependency edge beyond its active limit, checked before materializing or sorting that edge | false | 1 |
| `RUNTIME_STATE_REFERENCE_EDGES_EXCEEDED` | registering the next runtime-state-reference edge beyond its active limit | false | 1 |
| `STATE_FIELDS_EXCEEDED` | registering the next state-field binding beyond its active limit | false | 1 |
| `GENERATED_CALLBACKS_EXCEEDED` | registering the next generated callback/transfer beyond its active limit | false | 1 |
| `BOUND_MEMBERS_EXCEEDED` | registering the next bound-member binding beyond its active limit | false | 1 |
| `STATE_OPERATION_CAPABILITIES_EXCEEDED` | registering the next state-operation capability beyond its active limit | false | 1 |
| `PROTOCOL_CAPABILITIES_EXCEEDED` | registering the next protocol capability beyond its active limit | false | 1 |
| `BINARY_OPERATOR_CAPABILITIES_EXCEEDED` | registering the next binary-operator capability beyond its active limit | false | 1 |
| `AUDIT_STATE_READS_EXCEEDED` | registering the next audit-state-read primitive beyond its active limit | false | 1 |
| `SEMANTIC_GUARDS_EXCEEDED` | registering the next semantic guard beyond its active limit | false | 1 |
| `SEMANTIC_NORMAL_TRANSFERS_EXCEEDED` | registering the next semantic normal transfer beyond its active limit | false | 1 |
| `SEMANTIC_EXCEPTION_TRANSFERS_EXCEEDED` | registering the next semantic exception transfer beyond its active limit | false | 1 |
| `SEMANTIC_MODELS_EXCEEDED` | registering the next operation semantic model beyond its active limit | false | 1 |
| `INTRINSIC_EFFECTS_EXCEEDED` | registering the next intrinsic effect step beyond its active limit | false | 1 |
| `OPERATION_OUTCOMES_EXCEEDED` | registering the next operation-outcome contract beyond its active limit | false | 1 |
| `EXCEPTION_CONTRACTS_EXCEEDED` | registering the next exception contract beyond its active limit | false | 1 |
| `ARRAY_BOUND_EXCEEDED` | exact ndarray size, checked nbytes, or canonical object-array preimage bytes exceeds its array/content contract or remaining record/edge capacity before reading or allocating content | false | 1 |
| `ITERATOR_BOUND_EXCEEDED` | an iterable/iterator cardinality, distinct symbolic iterator source, or finite starred expansion exceeds its active bound before item/callback scheduling | false | 1 |
| `ABSTRACT_CONTAINER_BOUND_EXCEEDED` | an abstract container would exceed its active bound before construction/expansion (acceptance bound 256) | false | 1 |
| `UNION_BOUND_EXCEEDED` | a join would exceed the active distinct-alternative bound (acceptance bound 32) | false | 1 |
| `ABSTRACT_FIXPOINT_EXCEEDED` | loop or SCC requires a pass beyond its active bound (acceptance bound 32) | false | 1 |
| `FORBIDDEN_RANDOM` | scheduled value is `is` one literal `FORBIDDEN_RANDOM` identity | true | 2 |
| `FORBIDDEN_DYNAMIC_RESOLVER` | scheduled value is `is` one literal `FORBIDDEN_DYNAMIC` identity | true | 2 |
| `RUNTIME_IMPORT` | reachable AST import or `IMPORT_NAME`/`IMPORT_FROM` instruction, before attempting resolution | true | 2 |
| `UNSUPPORTED_SYNTAX` | first reachable AST node/operator is outside the closed transfer table | true | 3 |
| `UNRESOLVED_CALL` | a `Call` callee remains `UNKNOWN` after supported name/attribute/value transfer | true | 4 |
| `UNRESOLVED_ATTRIBUTE` | the attribute name is dynamic, or static lookup finds no raw member/field/namespace entry at all; a raw descriptor that exists but lacks binding is excluded | true | 4 |
| `UNKNOWN_VALUE_PROVENANCE` | a non-call/non-attribute/non-factory-product value needed at a provider frontier remains `UNKNOWN` after join/transfer and no more-specific unresolved category applies | true | 4 |
| `UNRESOLVED_INSTANCE_STATE` | a field read targets symbolic `INSTANCE_OF` without a generated transfer or exact structured-state contract | true | 4 |
| `CALLSITE_MISMATCH` | independently frozen AST/bytecode site manifests do not pair bijectively, or an existing uniquely labelled capability is attached to the wrong paired site; absence of a capability is excluded | true | 5 |
| `STATE_OPERATION_MISMATCH` | after the site and capability exist and arguments validate, the resolved state object, operation kind, receiver, or ordered implementation-provider/semantic-model labels differ; normal/exception payload differences are excluded | true | 5 |
| `PROTOCOL_DISPATCH_MISMATCH` | after the site and capability exist and inputs validate, iteration/view/consumption/intrinsic-effect source, callback, provider order, or cardinality differs; normal/exception payload differences are excluded | true | 5 |
| `ARGUMENT_CONTRACT_MISMATCH` | matched callsite/callee has one positional/keyword/protocol value outside its named `ArgumentContract` | true | 5 |
| `RESULT_CONTRACT_MISMATCH` | joined normal project/external result differs from its named `ResultContract` | true | 5 |
| `EXCEPTION_CONTRACT_MISMATCH` | an external/project/attribute/state/protocol call exposes an undeclared exception, wrong exact class/MRO/constructor contract, or missing declared exception edge | true | 5 |
| `UNAPPROVED_EXTERNAL_CALLABLE` | exact resolved external callable has no matching call capability; a present but structurally wrong capability is excluded | true | 6 |
| `UNAPPROVED_FACTORY` | exact external/project class, `GenericAlias`, or other factory is called without a matching factory/class capability; a present but structurally wrong capability is excluded | true | 6 |
| `UNAPPROVED_FACTORY_RESULT` | a project/generated `__new__` or constructor transfer with no named external outcome yields unknown, wrong-type, or wrong-structure abstract provenance; ordinary named normal outcomes are excluded and use `RESULT_CONTRACT_MISMATCH` | true | 6 |
| `UNAPPROVED_DESCRIPTOR` | static lookup resolved an exact raw descriptor, but no matching descriptor/receiver capability or generated-slot binding exists; dynamic/missing attributes are excluded | true | 6 |
| `UNAPPROVED_NAMESPACE_ESCAPE` | bare namespace is returned/stored/passed/subscripted/dynamically inspected or used outside its exact attribute capability | true | 6 |
| `UNAPPROVED_CARRIER` | exact non-callable behavior-bearing container/object does not match any terminal/structured/container/array/iterable/runtime-value contract | true | 6 |
| `EXCESS_AUTHORITY` | a consumable authority record is unused, or a support record is not reachable from at least one consumed authority under the authorization DAG, using the exact table partition below | true | 7 |

The category table has a construction-time reachability KAT for every row and
must contain exactly 66 unique enum values and 66 unique trigger rows with a
bijective name set in this revision. It also has
pairwise overlap KATs for the dangerous boundaries: absent capability versus
wrong-site capability; wrong argument versus wrong normal result versus wrong
exception; state/protocol structure versus their outcomes; unknown provenance
versus generated factory product; and forbidden identity versus unapproved
call; and dynamic/missing attribute versus statically resolved raw descriptor
without a binding. Exactly one category must be selected. A state/protocol row may not
consume a result/exception mismatch, and `CALLSITE_MISMATCH` may not consume an
absent-capability case.

The `EXCESS_AUTHORITY` partition is closed. Consumable authority tables are
safe (not forbidden-only) external identities, external classes, project
classes/functions, generated artifacts/methods/accessors/callbacks/transfers,
project descriptors, external/bound type members, runtime locator roots/steps/
locators/handles/values/state fields/identity sources/tokens/SCCs,
external ABC states/pinned Python intrinsics,
value/argument/result/iterable/exception/
outcome contracts, semantic guards/normal/exception transfers/models,
intrinsic effects, state-operation transfers, and every callsite/namespace/
attribute/state/protocol/operator/audit-read capability. Each must be consumed
at least once by a reachable root site or state proof; instruction-level
capabilities are consumed by exactly one paired site. Non-consumable support
records are project modules/source indexes, behavior-slot manifests, root
input/state contracts, opcode/site/pairing/syntax manifests, both graph
manifests, runtime binary anchor, limits, forbidden-only identities, and
transport fields. Each support record must be reachable from a consumed
authority or mandatory preflight root; an unreachable support record is also
excess authority. No other table is silently exempt.

`FindingReportRecord` is the full wire record
`(category,path,frontier_edge,target_label,detail)`. `FindingStableKey` is the
separate canonical record `(category,path,frontier_edge,target_label)` with
the same field order and no `detail`. Full findings are sorted solely by the
canonical bytes of `FindingStableKey`; duplicate stable keys are a report
construction error, not resolved by detail. The wire `findings` array contains
full report records; the stable-report preimage contains the corresponding
stable-key records. Free-form detail is therefore diagnostic wire data and is
never a sort, digest, or PASS input. KATs mutate detail while requiring an
identical stable digest and mutate each stable field while requiring a
different stable digest.

The sole audit entry point is positional-only:

```python
audit_provider_graph(policy, /) -> AuditReport
```

An invalid bootstrap raises exact test-only `ProviderBootstrapError`; invalid
policy/schema construction raises `ProviderPolicyError`. Candidate behavior,
state drift, and graph/resource bounds are represented as focused findings.
A bound sets `completed=False`; the report cannot be treated as PASS. The audit
does not otherwise translate candidate behavior into an exception.

### 5.5 Ninth-revision schema registry retained as a migration ledger

This registry records the ninth-revision surface names so an implementation
cannot silently drop a former field. It is **not** the tenth-revision machine
schema: Section 5.6 replaces every `OBJ`, `V`, label namespace, identity
source, reference-classification, runtime-reference, value-expression,
callback, root-state, opcode-lowering, ABC-state, digest, and finding
definition named here. A generator must first lower this migration ledger to
Section 5.6 and may not serialize a Section 5.5 record directly. Earlier prose
defines semantics and constraints but cannot add, rename, embed, or omit a
field after that lowering. Type notation in this retained ledger is
closed: `L` is one non-empty literal label, `LS` an ordered tuple of labels,
`S` exact string, `I` bounded non-negative integer unless a signed range is
stated, `B` exact bool, `H` 64-character lowercase SHA-256, `V` one canonical
value from Section 4.1, `OBJ` one live exact identity omitted from canonical
JSON and represented there by its `L`, `O[T]` explicit nullable `T`, and
`E[...]` one listed enum literal. `R[T]` is an ordered embedded non-reusable
record. Every field appears in the order shown; all non-applicable `O` fields
are explicit `null`, all empty tuples are `[]`, and no mapping has extra keys.

`LabelRegistry` is the single pre-validation index and has no label of its own:
`LabelRegistry(definitions:tuple[R[LabelDefinition]],
reference_classifications_digest:H,digest:H)`, where
`LabelDefinition(label:L,owner_table:E[root_input_contract,project_modules,
project_source_indexes,project_function_bindings,project_classes,
behavior_slot_manifests,external_classes,external_abc_states,
external_python_intrinsics,generated_artifacts,generated_methods,
generated_field_accessors,generated_callback_transfers,external_identities,
project_descriptors,external_type_members,runtime_locator_root_nodes,
runtime_locator_access_steps,runtime_value_locators,
located_bound_callable_handles,process_local_identity_sources,
process_local_identity_tokens,runtime_values,state_fields,runtime_state_sccs,
authorization_dependency_graph,runtime_state_reference_graph,
generated_stdlib_callbacks,bound_type_members,value_contracts,
root_argument_contracts,root_structured_state_contracts,argument_contracts,
result_contracts,iterable_contracts,exception_contracts,outcome_contracts,
semantic_guards,semantic_normal_transfers,semantic_exception_transfers,
semantic_models,intrinsic_effect_steps,state_operation_transfers,
project_functions,callsite_capabilities,namespace_capabilities,
attribute_capabilities,state_operation_capabilities,protocol_capabilities,
binary_operator_capabilities,audit_state_reads,interpreter_opcode_profile,
ast_site_keys,bytecode_site_keys,bytecode_site_groups,
structural_callsite_keys,structural_attribute_site_keys,
structural_state_site_keys,structural_operator_site_keys,
structural_protocol_site_keys,ast_site_manifest,bytecode_site_manifest,
site_pairing_manifest,root_syntax_inventory],
record_ordinal:I,record_digest:H)`. Definitions are sorted by label UTF-8 bytes;
`record_ordinal` is the position in the already-canonical owner table; singleton
record keys use ordinal zero. `LabelDefinition.label` is the subject record's
label value, not a label belonging to the embedded definition record, so it
does not itself enter the registry. Every
label-bearing top-level record has exactly one definition, every definition
resolves to one record whose label and digest match, and embedded `R[...]`
records may not bear labels. The complete
`CrossRecordReferenceClassification` array is separately domain-hashed and its
digest is bound by the registry. The registry `digest` is the
`label-registry` domain hash of exactly
`{"definitions":<definitions>,"reference_classifications_digest":<H>}`;
the digest field itself is excluded, so no self-hash exists. Validation order is: validate typed record
shape without following references; construct and compare the registry;
validate every reference classification; derive the authorization/runtime
graphs; then validate semantic invariants. A manifest containing only labels
therefore cannot hide an orphan definition.

Bootstrap/project records are exactly:

- `ExternalIdentityEntry(label:L,value:OBJ,disposition:E[SAFE_VALUE,
  SAFE_CALLABLE,SAFE_FACTORY,SAFE_TYPE_OPERAND,NAMESPACE_ROOT,
  FORBIDDEN_RANDOM,FORBIDDEN_DYNAMIC],role:E[READONLY_VALUE,PURE_CALL,
  CONSTRAINED_FACTORY,TYPE_CHECK_ONLY,NAMESPACE_ONLY,FORBIDDEN_ONLY],
  reason:S,reference_token:S,provider_module:S,qualified_name:S,
  identity_category:S,state_policy:E[IMMUTABLE_BUILTIN,PYTHON_FUNCTION,
  NUMPY_DISPATCHER,NUMPY_UFUNC_EXPORT,BINARY_EXPORT,TYPE_MEMBER,
  STRUCTURED_INSTANCE,EXTERNAL_CLASS,MODULE_NAMESPACE,NOT_APPLICABLE],
  state_fields:tuple[S],
  state_accessors:tuple[R[StateFieldAccessor]],state_digest:O[H],
  python_version:S,numpy_version:O[S],source_sha256:O[H],
  binary_sha256:O[H],root_scope:LS)`.
- `StateFieldAccessor(field_name:S,mode:E[EXACT_DICT_LOOKUP,
  EXACT_INSTANCE_DICT_LOOKUP,EXACT_MEMBER_DESCRIPTOR,
  EXACT_GETSET_DESCRIPTOR,EXACT_BOUNDED_CANONICAL_CONTAINER_SNAPSHOT],
  descriptor_identity_label:O[L],expected_atomic_or_identity:O[V],
  expected_value_contract_label:O[L],maximum_items:O[I])` with exactly one
  expected-result field non-null.
- `ProjectModuleBinding(label:L,module:OBJ,globals_dict:OBJ,
  resolved_origin:S,source_sha256:H,root_scope:LS)`.
- `ProjectSourceIndex(label:L,project_module_label:L,module_ast_digest:H,
  code_mappings:tuple[R[SourceCodeMapping]],comprehension_mappings:
  tuple[R[ComprehensionMapping]])`; `SourceCodeMapping` is exactly
  `(code_digest:H,lexical_path:S,ast_kind:E[FUNCTION,LAMBDA,COMPREHENSION],
  ast_ordinal:I,co_firstlineno:I,bytecode_name:S,lineno:I,col_offset:I,
  end_lineno:I,end_col_offset:I)`, and `ComprehensionMapping` is exactly
  `(code_digest:H,lexical_path:S,ast_kind:E[LIST,SET,DICT,GENERATOR],
  ast_ordinal:I,span:R[SourceSpan],outer_iterable_ast_digest:H,
  generator_records:tuple[R[ComprehensionGenerator]],
  captured_environment_labels:LS,nested_code_digest:H)`; `SourceSpan` is
  exactly four integer coordinates and `ComprehensionGenerator` exactly
  `(target_ast_digest:H,iterable_ast_digest:H,filter_ast_digests:tuple[H],
  is_async:false)`.
- `ProjectFunctionBinding(label:L,root_scope:LS,project_module_label:L,
  source_index_label:L,function_identity:OBJ,globals_identity:OBJ,
  code_identity:OBJ,code_digest:H,lexical_path:S,defaults_digest:H,
  keyword_defaults_digest:H,closure_digest:H,
  referenced_globals_digest:H)`; its identity/global/module invariants are the
  exact project-binding predicates in Section 4.2.
- `ProjectClassBinding(label:L,root_scope:LS,project_module_label:L,
  source_index_label:L,class_ast_digest:H,lexical_path:S,class_identity:OBJ,
  kind:E[ORDINARY,EXCEPTION,RUNTIME_PROTOCOL],base_class_labels:LS,
  metaclass_label:L,class_member_records:tuple[R[ClassMemberRecord]],
  behavior_slot_manifest_label:L,constructor_semantic_model_label:O[L],
  constructor_outcome_label:O[L],instancecheck_semantic_model_label:O[L],
  instancecheck_outcome_label:O[L],exception_mro_labels:LS,
  inherited_constructor_provider_label:O[L],runtime_checkable:O[B],
  protocol_dependency_labels:LS)`.
- `ClassMemberRecord(name:S,state:E[ABSENT,PRESENT],
  value_kind:E[ATOMIC,BINDING],atomic_value:O[V],binding_label:O[L])` has both
  value fields null when absent and exactly one non-null when present.
- `BehaviorSlotManifest(label:L,project_class_label:L,python_version:S,
  entries:tuple[R[BehaviorSlotEntry]])` and
  `BehaviorSlotEntry(name:E[closed-slot-universe],state:E[ABSENT,INHERITED,
  OWN],defining_class_label:O[L],raw_member_identity_label:O[L],
  member_model_label:O[L])`.
- `ExternalClassBinding(label:L,root_scope:LS,external_identity_label:L,
  provider_module:S,export_name:S,class_identity:OBJ,metaclass_identity:OBJ,
  base_identity_labels:LS,mro_identity_labels:LS,
  class_namespace_snapshot:tuple[R[ClassMemberRecord]],
  abc_state_binding_label:O[L],
  instancecheck_semantic_model_label:L,instancecheck_outcome_label:L,
  subclasscheck_semantic_model_label:L,subclasscheck_outcome_label:L)`.
- `ExternalAbcStateBinding(label:L,root_scope:LS,external_class_label:L,
  abcmeta_identity_label:L,abc_impl_member_name:S,
  abc_impl_identity:OBJ,abc_impl_type_label:L,abc_binary_anchor_digest:H,
  get_dump_identity_label:L,registry_referent_labels:LS,
  positive_cache_referent_labels:LS,negative_cache_referent_labels:LS,
  negative_cache_version:I,pre_state_digest:H,post_state_digest:H)`.
  The three referent arrays are sorted by already-labelled referent label, not
  by weakref hash, equality, or representation. Exact `ABCMeta` requires this
  record; every other metaclass requires `abc_state_binding_label=null`.
- `ExternalPythonIntrinsicBinding(label:L,root_scope:LS,
  provider_module:S,export_name:S,external_identity_label:L,
  resolved_origin:S,source_or_binary_digest:H,code_digest:O[H],
  referenced_binding_digest:H,receiver_contract_label:O[L],
  argument_contract_labels:LS,keyword_names:tuple[S],
  semantic_model_label:L,normal_transfer_label:L,
  exception_transfer_labels:LS,kat_digest:H)`. The only initial records are
  exact `typing.cast` and exact `json.dumps`; the table is not populated by
  scanning external modules or source.
- `GeneratedMethodRecord(label:L,owner_artifact_label:L,
  class_dictionary_name:S,kind:E[PYTHON_FUNCTION,STATICMETHOD,CLASSMETHOD,
  DATACLASS_INIT,NAMEDTUPLE_NEW,NAMEDTUPLE_METHOD,ENUM_GENERATED],
  raw_member_identity:OBJ,
  unwrapped_function_identity:O[OBJ],code_digest:O[H],signature:S,
  runtime_anchor_label:L)`.
- `GeneratedFieldAccessorRecord(label:L,owner_artifact_label:L,
  owner_class_identity:OBJ,field_name:S,field_position:I,
  raw_accessor_identity:OBJ,accessor_type_identity:OBJ,
  runtime_anchor_label:L)`.
- `GeneratedProjectArtifactBinding(label:L,artifact_kind:E[DATACLASS,
  NAMEDTUPLE,ENUM_CLASS],root_scope:LS,project_module_label:L,
  class_qualified_name:S,class_identity:OBJ,class_source_sha256:H,
  python_version:S,dataclass_recipe:O[R[DataclassRecipe]],
  namedtuple_recipe:O[R[NamedTupleRecipe]],enum_recipe:O[R[EnumRecipe]],
  generated_method_labels:LS,field_accessor_labels:LS,
  transfer_label:L)` with exactly one kind recipe non-null.
- `DataclassRecipe` is exactly `(init:B,repr:B,eq:B,order:B,unsafe_hash:B,
  frozen:B,match_args:B,kw_only:B,slots:B,weakref_slot:B,
  fields:tuple[R[DataclassFieldRecipe]],slot_names:tuple[S])`, with each field
  exactly `(name:S,init:B,kw_only:B,has_default:B,default_contract_label:O[L],
  has_default_factory:B,default_factory_label:O[L])`.
- `NamedTupleRecipe` is exactly `(direct_tuple_base_label:L,fields:tuple[S],
  field_defaults:tuple[R[NamedDefault]],slots:tuple[S],new_identity_label:L,
  new_code_digest:H,new_signature:S)`; `NamedDefault` is exactly
  `(name:S,value_contract_label:L)`.
- `EnumRecipe` is exactly `(base_labels:LS,metaclass_label:L,
  member_names:tuple[S],members:tuple[R[EnumMember]],aliases:
  tuple[R[EnumAlias]],members_mapping:V,member_map:V,member_names_state:V,
  value2member_map:V,unhashable_values:V,unhashable_values_map:V,
  missing_label:O[L],new_label:L,version_dependency_records:
  tuple[R[ClassMemberRecord]])`; `EnumMember` is exactly
  `(name:S,identity:OBJ,value:V)` and `EnumAlias` exactly
  `(alias_name:S,target_member_name:S)`.
- `ProjectDescriptorBinding(label:L,root_scope:LS,project_module_label:L,
  project_class_label:L,source_index_label:L,attribute_name:S,
  descriptor_identity:OBJ,kind:E[PROPERTY,CLASSMETHOD,STATICMETHOD,
  CLASS_CONSTANT],function_labels:LS,receiver_contract_label:O[L],
  result_value_contract_label:L)`.
- `ExternalTypeMemberBinding(label:L,root_scope:LS,owner_type_label:L,
  member_name:S,member_identity:OBJ,member_kind:E[PYTHON_FUNCTION,PROPERTY,
  METHOD_DESCRIPTOR,WRAPPER_DESCRIPTOR,MEMBER_DESCRIPTOR,GETSET_DESCRIPTOR],
  owner_anchor_digest:H,python_function_state_digest:O[H],
  receiver_contract_label:L,result_value_contract_label:L)`.

Runtime-location/state records are exactly:

- `RuntimeLocatorRootNode(label:L,kind:E[MODULE_GLOBAL,CLOSURE_CELL,
  CALLABLE_DEFAULT,CALLABLE_KWDEFAULT],source_binding_label:L,
  literal_name:O[S],code_digest:O[H],ordinal:O[I])`.
- `RuntimeLocatorAccessStep(label:L,kind:E[STATE_FIELD,CONTAINER_ENTRY,
  BOUND_CALLABLE_RECEIVER,GENERATED_FIELD_RESULT,TYPE_MEMBER_RESULT],
  parent_node_label:L,operation_binding_label:L,key_contract_label:O[L],
  identity_token_label:O[L],expected_identity_label:O[L],
  result_value_contract_label:O[L],result_type_label:L)`.
- `RuntimeValueLocator(label:L,root_scope:LS,
  root_node_label:L,access_step_labels:LS)`.
- `ProcessLocalIdentitySource(label:L,root_scope:LS,
  kind:E[LIVE_LOCATED_IDENTITY,SYMBOLIC_FRESH_IDENTITY],
  live_locator_label:O[L],producing_callsite_key_label:O[L],
  producing_result_transfer_label:O[L],source_value_contract_label:L,
  frame_key_digest:O[H],allocation_ordinal:I,
  allowed_consumer_site_labels:LS)`; the live locator alone is present for
  `LIVE_LOCATED_IDENTITY`, while producing callsite/result and frame key are
  present for `SYMBOLIC_FRESH_IDENTITY`.
- `ProcessLocalIdentityToken(label:L,root_scope:LS,identity_source_label:L,
  source_id_callsite_key_label:L,
  id_external_identity_label:L,id_semantic_model_label:L,
  source_value_contract_label:L,audit_primitive_label:O[L],
  allowed_consumer_site_labels:LS,allowed_operations:tuple[E[LOCATOR_KEY,
  HASH,EQUALITY,SET_CONTAINS,SET_ADD,SET_REMOVE,DICT_LOOKUP,TUPLE_SNAPSHOT,
  IDENTITY_COMPARE]])`.
- `LocatedBoundCallableHandle(label:L,root_scope:LS,locator_label:L,
  callable_identity:OBJ,callable_type_label:L,owner_type_label:L,
  raw_member_label:L,receiver_read_primitive_label:L)`.
- `ProjectStateFieldBinding(label:L,parent_runtime_value_label:L,
  field_name:S,mode:E[EXACT_INSTANCE_DICT_LOOKUP,EXACT_SLOT_LOOKUP],
  slot_descriptor_label:O[L],nested_value_contract_label:O[L],
  child_identity:O[OBJ],child_type_label:O[L])` with exactly one nested value
  or the complete child-identity/type pair present.
- `GeneratedStdlibCallbackBinding(label:L,parent_runtime_value_label:L,
  source_state_field_binding_label:L,function_identity:OBJ,stdlib_relative_source:S,
  source_sha256:H,code_digest:H,positional_default_labels:LS,
  keyword_default_records:V,closure_recipe:V,load_binding_records:V,
  semantic_model_label:L,outcome_contract_label:L,
  pre_state_digest:H,post_state_digest:H)`.
- `GeneratedStdlibCallbackTransfer(label:L,callback_binding_label:L,
  callback_code_digest:H,callback_source_sha256:H,key_contract_label:L,
  input_contract_labels:LS,intrinsic_effect_labels:LS,
  normal_transfer_label:L,exception_transfer_labels:LS)`.
- `BoundTypeMemberBinding(label:L,located_handle_label:L,
  bound_callable_identity:OBJ,receiver_runtime_value_label:L,
  self_identity:OBJ,owner_type_label:L,raw_member_label:L,
  receiver_contract_label:L,semantic_model_label:L,outcome_contract_label:L)`.
- `ProjectRuntimeValueBinding(label:L,root_scope:LS,locator_label:L,
  current_identity:OBJ,type_binding_label:L,
  construction_provenance:E[IMPORT_TIME,FACTORY_OWNED,CLOSURE_CAPTURED,
  NESTED_STATE],kind:E[BUILTIN_CONTAINER,REGEX_PATTERN,TYPING_FORM,
  ENUM_CLASS,STRUCTURED_INSTANCE,WEAK_KEY_DICTIONARY,WEAK_REFERENCE,
  GENERATED_STDLIB_CALLBACK,BOUND_TYPE_MEMBER],pre_state_digest:H,
  post_state_digest:H,state_field_names:tuple[S],contained_contract_labels:LS,
  artifact_or_external_type_label:O[L],kind_payload:R[RuntimeKindPayload])`.
- `RuntimeKindPayload` is the closed union: `BUILTIN_CONTAINER` has exactly
  `(container_value_contract_label:L)`; `REGEX_PATTERN` has exactly
  `(pattern:S,flags:I,groups:I,groupindex_contract_label:L,
  pattern_type_label:L,anchor_digest:H)`; `TYPING_FORM` has exactly
  `(form_kind:E[GENERIC_ALIAS,UNION_TYPE,CALLABLE_GENERIC_ALIAS],
  origin_contract_label:L,argument_contract_labels:LS,parameter_labels:LS,
  instance_state_digest:H)`; `ENUM_CLASS` has exactly
  `(generated_artifact_label:L)`; `STRUCTURED_INSTANCE` has exactly
  `(complete_field_records:tuple[R[ClassMemberRecord]])`;
  `WEAK_KEY_DICTIONARY` has exactly `(data_field_name:S,
  iterating_field_name:S,pending_field_name:S,remove_field_name:S,
  complete_state_digest:H)` and contains no child-record label;
  `WEAK_REFERENCE` has exactly
  `(referent_identity_label:L,callback_identity_label:O[L])`;
  `GENERATED_STDLIB_CALLBACK` has exactly `(callback_binding_label:L)`; and
  `BOUND_TYPE_MEMBER` has exactly `(located_handle_label:L)`.
- `RuntimeStateSccBinding(label:L,root_scope:LS,
  shape:E[WEAK_KEY_DICTIONARY_REMOVE_SELFREF,
  RESOLUTION_RECORDS_WEAKREF_CALLBACK],member_labels:LS,
  edges:tuple[R[RuntimeStateReferenceEdge]])`, where each edge is exactly
  `(source_label:L,kind:E[STATE_FIELD,RECEIVER,REFERENT,CALLBACK,DEFAULT,
  CLOSURE,CONTAINER_ENTRY],target_label:L,ordinal:I)`.
- `AuthorizationDependencyGraph(label:L,root_label:L,node_labels:LS,
  edges:tuple[R[AuthorizationEdge]],topological_order:LS)` and
  `RuntimeStateReferenceGraph(label:L,root_label:L,node_labels:LS,
  edges:tuple[R[RuntimeStateReferenceEdge]],scc_binding_labels:LS)`.
- `AuthorizationEdge(source_label:L,target_label:L,ordinal:I)` and
`CrossRecordReferenceClassification(source_label:L,field_name:S,
  field_ordinal:I,target_label:L,kind:E[OWNS,AUTH_REQUIRES,VALIDATES,
  RUNTIME_REF])`. Every label-bearing scalar or array element in every
  semantic/source canonical record has exactly one classification entry. The
  registry definitions, classification records themselves, and the derived
  graph's node/edge/topological/SCC label views are meta-indexes and are not
  recursively classified; each must instead be recomputed exactly from the
  classified source fields. The derived
  authorization graph contains exactly the `AUTH_REQUIRES` entries; the
  derived runtime graph contains exactly the `RUNTIME_REF` entries; `OWNS` and
  `VALIDATES` enter neither graph. Counts and sorted tuples must agree in both
  directions, so an omitted or multiply classified reference is a schema
  failure.
  `source_label -> target_label` means “source requires target”; the stored
  construction order is valid iff `position(target) < position(source)` for
  every authorization edge. Ties among simultaneously ready nodes use label
  UTF-8 order. Graph derivation checks the edge budget before appending each
  edge and before topological sorting.

Contract/semantic records are exactly:

- `IterableContract(label:L,kind:E[ITERABLE,ITERATOR,DICT_VIEW],
  producer_label:L,source_value_contract_label:L,item_value_contract_label:L,
  exact_cardinality:O[I],minimum_cardinality:O[I],maximum_cardinality:O[I],
  reiterable:B,single_pass:B,view_kind:E[KEYS,VALUES,ITEMS,NOT_APPLICABLE],
  protocol_capability_labels:LS)`.
- `ValueContract(label:L,kind:E[closed ValueContractKind],payload:V)` in
  canonical JSON; the in-memory neutral-field record is exactly the complete
  ordered field list in Section 5.2.
- `RootInputContract(label:L,root_label:L,argument_labels:LS)`,
  `RootStructuredStateContract(label:L,parameter_name:S,runtime_identity:OBJ,
  project_type_binding_label:L,construction_provenance:E[AUDITOR_CONSTRUCTED,
  PROJECT_FACTORY_OWNED],constructor_or_factory_label:L,
  validator_or_ownership_gate_label:L,field_contracts:V,
  pre_state_digest:H,post_state_digest:H,nested_binding_records:V)`, and
  `RootArgumentContract(label:L,parameter_name:S,kind:E[POSITIONAL_ONLY,
  POSITIONAL_OR_KEYWORD,KEYWORD_ONLY],position:O[I],keyword:O[S],
  atomic_value_contract_label:O[L],structured_state_contract_label:O[L])`.
- `ArgumentContract(label:L,position:O[I],keyword:O[S],
  value_contract_label:L,protocol_capability_labels:LS)`,
  `ResultContract(label:L,value_contract_label:L,may_discard:B,
  producing_semantic_model_label:L)`,
  `ExceptionContract(label:L,exception_class_label:L,mro_identity_labels:LS,
  constructor_argument_contract_labels:LS,cause_exception_label:O[L],
  context_exception_label:O[L])`, and
  `OperationOutcomeContract(label:L,normal_result_contract_label:O[L] |
  NO_NORMAL_RETURN,exception_contract_labels:LS)`.
- `SemanticGuard(label:L,kind:E[closed SemanticGuardKind],
  operand_contract_labels:LS,operation_label:L,expected_boolean:B,
  intrinsic_effect_labels:LS)`,
  `SemanticNormalTransfer(label:L,kind:E[closed
  SemanticNormalTransferKind],input_contract_labels:LS,guard_labels:LS,
  payload:R[SemanticNormalPayload],intrinsic_effect_labels:LS,
  state_operation_transfer_label:O[L])`,
  `SemanticExceptionTransfer(label:L,guard_labels:LS,
  payload:R[SemanticExceptionPayload],intrinsic_effect_labels:LS)`, and
  `OperationSemanticModel(label:L,kind:E[PROJECT_CODE,
  PINNED_EXTERNAL_PYTHON_INTRINSIC,BUILTIN_INTRINSIC,
  TYPE_MEMBER_INTRINSIC,PROTOCOL_INTRINSIC,BINARY_OPERATOR_INTRINSIC,
  GENERATED_CALLBACK_TRANSFER],
  implementation_identity_label:L,source_or_binary_digest:H,
  receiver_contract_label:O[L],argument_contract_labels:LS,
  intrinsic_effect_labels:LS,normal_transfer_label:L,
  exception_transfer_labels:LS)`.
- `SemanticNormalPayload` is the discriminated closed union defined in
  Section 5.2: `EXACT_VALUE` has
  `(source_kind:E[LITERAL,INPUT,RECEIVER],literal_value:O[V],
  input_ordinal:O[I],projection_path:tuple[R[ProjectionStep]])`;
  `PROCESS_LOCAL_IDENTITY_TOKEN` has `(identity_source_label:L,
  allocation_site_label:L,allocation_ordinal:I,
  allowed_consumer_site_labels:LS)`; `BOUNDED_ARITHMETIC` has
  `(operator:E[ADD,SUB,MUL,MATMUL,DIV,FLOORDIV,MOD,POW,LSHIFT,RSHIFT,
  BIT_OR,BIT_XOR,BIT_AND,UNARY_POSITIVE,UNARY_NEGATIVE,UNARY_NOT,
  UNARY_INVERT],operand_ordinals:tuple[I],integer_overflow_policy:E[FAIL],
  finite_float_policy:E[FINITE_ONLY],maximum_result_bits:I)`;
  `CONTAINER_CONSTRUCTION` has `(container_type_label:L,
  input_projections:tuple[R[InputProjection]],duplicate_key_policy:E[
  PRESERVE_ALL,REJECT_DUPLICATES,LAST_VALUE_EXACT],ordering_policy:E[
  INPUT_ORDER,KEY_UTF8_ORDER,CANONICAL_ATOMIC_ORDER],maximum_length:I)`;
  `VIEW_CONSTRUCTION` has
  `(source_input_ordinal:I,view_kind:E[KEYS,VALUES,ITEMS],
  maximum_cardinality:I)`; `ITERATOR_CONSTRUCTION` has
  `(source_input_ordinal:I,item_projection:R[InputProjection],
  cardinality_rule:R[CardinalityRule],reiterable:false,single_pass:true)`;
  `STATE_RESULT` has `(state_operation_transfer_label:L,selector_kind:E[
  RETURN_RECEIVER,RETURN_VALUE,LOOKUP_RESULT,DELETION_RESULT,SNAPSHOT_FIELD],
  selector_path:tuple[R[ProjectionStep]])`; `CALLBACK_RESULT` has
  `(callback_model_label:L,callback_output_ordinal:I,
  projection_path:tuple[R[ProjectionStep]])`; and `NO_NORMAL_RETURN` is an
  empty record. `ProjectionStep` is exactly
  `(kind:E[FIELD,TUPLE_INDEX,DICT_KEY,RESULT_COMPONENT],field_name:O[S],
  index:O[I],key_value:O[V])` with exactly the discriminator-selected selector
  non-null. `InputProjection` is exactly
  `(input_ordinal:I,steps:tuple[R[ProjectionStep]])`.
  `CardinalityRule` is exactly `(kind:E[EXACT_FROM_SOURCE,SUM_INPUTS,
  MIN_INPUTS,BOUNDED_RANGE],source_input_ordinals:tuple[I],
  literal_lower:O[I],literal_upper:O[I])`; source-derived kinds require nonempty
  source ordinals and null literals, while `BOUNDED_RANGE` requires empty
  sources and both finite literals. None contains an expected contract label.
- `SemanticExceptionPayload(trigger_kind:E[GUARD_FALSE,BOUNDS,TYPE,
  KEY_MISSING,CALLBACK_RAISE,PROVIDER_RAISE],operation_label:L,
  operand_ordinals:tuple[I],exception_constructor_model_label:L,
  constructor_argument_projections:tuple[R[InputProjection]],
  cause_rule:E[NONE,PROPAGATE_EXACT],context_rule:E[NONE,PROPAGATE_EXACT])`.
- `IntrinsicEffectStep(label:L,kind:E[closed effect kind],
  input_contract_labels:LS,output_value_contract_label:O[L],
  provider_model_label:L)`, `StateOperationTransfer(label:L,
  receiver_contract_label:L,key_contract_label:O[L],value_contract_label:O[L],
  dependency_labels:LS,normal_transfer_label:L,exception_transfer_labels:LS)`,
  and `ProjectFunctionContract(label:L,function_binding_label:L,
  receiver_contract_label:O[L],formal_contract_labels:LS,
  variadic_policy:E[FORBIDDEN,EXACT_FINITE],outcome_contract_label:L)`.

Every capability record begins exactly with `(label:L,root_label:L,
site_key_label:L)` and then uses these ordered suffixes:

- `CallsiteCapability(...,owner_module_label:L,owner_function_qualified_name:S,
  owner_source_sha256:H,owner_function_identity:OBJ,owner_code_identity:OBJ,
  owner_code_digest:H,external_identity_label:L,receiver_contract_label:O[L],
  positional_argument_contract_labels:LS,keyword_argument_contract_labels:LS,
  semantic_model_label:L,outcome_contract_label:L,reason:S,
  reference_token:S)`.
- `NamespaceAttributeCapability(...,namespace_binding_label:L,
  attribute_name:S,resolved_identity_label:L)`.
- `AttributeAccessCapability(...,operation:E[READ,WRITE,DELETE],
  attribute_name:S,receiver_contract_label:L,binding_label:L,
  assigned_argument_contract_label:O[L],semantic_model_label:L,
  outcome_contract_label:L)`.
- `StateOperationCapability(...,runtime_value_binding_label:L,
  operation:E[GET_ITEM,SET_ITEM,DELETE_ITEM,METHOD_CALL],
  key_contract_label:O[L],value_contract_label:O[L],semantic_model_label:L,
  outcome_contract_label:L,state_operation_transfer_label:L,
  provider_labels:LS)`.
- `ProtocolDispatchCapability(...,operation:E[closed protocol kind],
  receiver_contract_label:L,input_contract_labels:LS,
  external_class_binding_label:O[L],project_callback_label:O[L],
  provider_labels:LS,semantic_model_label:L,outcome_contract_label:L)`.
- `BinaryOperatorCapability(...,operator:E[TYPE_UNION_OR,
  DICT_KEYS_UNION_OR],left_contract_label:L,right_contract_label:L,
  provider_labels:LS,intrinsic_effect_labels:LS,semantic_model_label:L,
  outcome_contract_label:L)`.
- `AuditStateReadPrimitive(label:L,operation:E[closed audit-read kind],
  implementation_digest:H,type_member_labels:LS,semantic_model_label:L,
  receiver_contract_label:L,precondition_contract_labels:LS,
  outcome_contract_label:L)`; it has no source site and therefore does not use
  the three-field capability prefix.

Site/graph/result records are exactly:

- `AstSiteKey(label:L,project_source_digest:H,lexical_code_path:S,
  owner_code_digest:H,site_kind:E[CALL,ATTRIBUTE_READ,ATTRIBUTE_WRITE,
  ATTRIBUTE_DELETE,SUBSCRIPT_READ,SUBSCRIPT_WRITE,SUBSCRIPT_DELETE,ITERATION,
  COMPARE,UNARY,BINARY_OPERATOR,TRUTH,CONTEXT_ENTER,CONTEXT_EXIT_NORMAL,
  CONTEXT_EXIT_EXCEPTION],ast_preorder_ordinal:I,lineno:I,
  col_offset:I,end_lineno:I,end_col_offset:I,evaluation_ordinal:I)`,
  `BytecodeSiteKey(label:L,owner_code_digest:H,site_kind:E[CALL,
  ATTRIBUTE_READ,ATTRIBUTE_WRITE,ATTRIBUTE_DELETE,SUBSCRIPT_READ,
  SUBSCRIPT_WRITE,SUBSCRIPT_DELETE,ITERATION,COMPARE,UNARY,BINARY_OPERATOR,
  TRUTH,CONTEXT_ENTER,CONTEXT_EXIT_NORMAL,CONTEXT_EXIT_EXCEPTION],opcode:S,
  instruction_offset:I,start_line:O[I],end_line:O[I],start_col:O[I],
  end_col:O[I],instruction_ordinal:I)`, and
  `BytecodeSiteGroup(label:L,owner_code_digest:H,site_kind:E[CALL,
  ATTRIBUTE_READ,ATTRIBUTE_WRITE,ATTRIBUTE_DELETE,SUBSCRIPT_READ,
  SUBSCRIPT_WRITE,SUBSCRIPT_DELETE,ITERATION,COMPARE,UNARY,BINARY_OPERATOR,
  TRUTH,CONTEXT_ENTER,CONTEXT_EXIT_NORMAL,CONTEXT_EXIT_EXCEPTION],
  ordered_key_labels:LS)`.
- Each `Structural*SiteKey` contains exactly `(label:L,ast_key_label:L,
  bytecode_site_group_label:L)`; `StructuralProtocolSiteKey` instead contains
  `(label:L,kind:E[BYTECODE_PROTOCOL,INTRINSIC_SUBSITE],ast_key_label:O[L],
  bytecode_site_group_label:O[L],parent_site_key_label:O[L],
  semantic_model_label:O[L],intrinsic_effect_ordinal:O[I])`.
- `InterpreterOpcodeProfile(label:L,python_version:S,opmap_digest:H,
  ignored_opcodes:tuple[S],lowering_rows:V)`, `AstSiteManifest(label:L,
  root_label:L,source_index_digests:tuple[H],site_records:LS)`,
  `BytecodeSiteManifest(label:L,root_label:L,code_digests:tuple[H],
  site_records:LS)`, and `SitePairingManifest(label:L,root_label:L,
  opcode_profile_digest:H,ast_manifest_digest:H,bytecode_manifest_digest:H,
  bytecode_group_labels:LS,pairs:tuple[R[SitePair]],
  intrinsic_subsites:tuple[R[IntrinsicSubsite]],
  algorithm_version:S)`.
- `SitePair` is exactly `(site_kind:E[CALL,ATTRIBUTE_READ,ATTRIBUTE_WRITE,
  ATTRIBUTE_DELETE,SUBSCRIPT_READ,SUBSCRIPT_WRITE,SUBSCRIPT_DELETE,ITERATION,
  COMPARE,UNARY,BINARY_OPERATOR,TRUTH,CONTEXT_ENTER,CONTEXT_EXIT_NORMAL,
  CONTEXT_EXIT_EXCEPTION],ast_key_label:L,
  bytecode_site_group_label:L,evaluation_ordinal:I)` and
  `IntrinsicSubsite` exactly `(label:L,parent_site_key_label:L,
  semantic_model_label:L,intrinsic_effect_ordinal:I,protocol_site_kind:E[ITER,
  NEXT,DICT_KEYS,DICT_VALUES,DICT_ITEMS,CONSUME,KEY_CALLBACK,LENGTH,TRUTH,HASH,
  EQUALITY,ORDER,ARRAY_COERCE,INSTANCE_CHECK,CONTEXT_ENTER,
  CONTEXT_EXIT_NORMAL,CONTEXT_EXIT_EXCEPTION])`.
- `ReceiverBinding(kind:E[NONE,SELF,CLS,INSTANCE_OF],owner_identity_label:O[L],
  instance_identity_label:O[L])`, `EdgeStep(kind:E[closed EdgeKind],
  trusted_label:L,ordinal:I)`, `ProviderRecord(path:tuple[R[EdgeStep]],
  value_identity_label:L,depth:I,receiver:R[ReceiverBinding],
  globals_environment_digest:H,root_argument_digest:H,frame_key_digest:O[H],
  scheduling_edge_kind:E[closed EdgeKind])`, and
  `FindingReportRecord(category:E[closed FindingCategory],
  path:tuple[R[EdgeStep]],frontier_edge:E[closed EdgeKind],target_label:L,
  detail:S)` and `FindingStableKey(category:E[closed FindingCategory],
  path:tuple[R[EdgeStep]],frontier_edge:E[closed EdgeKind],target_label:L)`.

`ProviderAuditPolicy` and `AuditReport` use exactly the top-level key sequences
in Sections 5.4 and the literal KATs below. `RootSyntaxInventory`,
`ProjectFunctionManifest`, and capability/outcome/protocol/operator manifests
are exact labelled records of `(label:L,root_label:L,input_digests:tuple[H],
ordered_member_labels:LS,digest:H)`. No implementation-defined record,
discriminator, nullable field, or key order remains after the mandatory
Section 5.6 lowering.

### 5.6 Tenth-revision sole machine schema and closure rules

This section is the sole machine authority for the tenth revision. Where it
does not restate a Section 5.5 record, that record is imported field-for-field
after the global type substitutions below. A conflict is a specification
error; Section 5.6 wins and the conflicting Section 5.5 surface record cannot
be serialized. The acceptance profile is exactly CPython `3.12.10` and NumPy
`2.2.6`. A different interpreter or NumPy version requires a separately
reviewed opcode/external-state profile and new literal KAT bytes; a version
string substitution is forbidden.

#### 5.6.1 Closed literal and label universes

The four label namespaces are disjoint lexical types:

- `RL = rec:<token>` for ordinary labelled records;
- `IA = id:<token>` for live identity anchors;
- `RS = root:<token>` for a root scope; and
- `PR = pkg:<token>` for one package root.

`token` matches `[a-z0-9][a-z0-9._-]{0,127}`. A field typed as one namespace
cannot accept a value from another. `LS` henceforth means `tuple[RL]`; an
ordered tuple of another namespace is written explicitly. `OBJ` is legal only
as the private in-memory `value` field of `IdentityAnchor`; it never appears in
canonical JSON.

`A` is the exact canonical atomic union `None | bool | bounded int | finite
float | finite complex | str | bytes | Ellipsis`. `CL` is the closed
discriminated `CanonicalLiteral` union:

- `ATOMIC(value:A)`;
- `IDENTITY(identity_anchor:IA)`;
- `TUPLE(items:tuple[R[CL]])`;
- `LIST(items:tuple[R[CL]])`;
- `FROZENSET(items:tuple[R[CL]])`, sorted by canonical item bytes;
- `DICT(entries:tuple[R[LiteralDictEntry]])`, where
  `LiteralDictEntry(key:S,value:R[CL])` has exact-string keys sorted by UTF-8;
  and
- `NDARRAY(value:R[CanonicalArrayLiteral])`, whose fields are exactly
  `dtype:S,shape:tuple[I],strides:tuple[I],hasobject:B,writeable:B,
  content_digest:H`.

No arbitrary JSON object or untagged container belongs to `CL`. Every former
Section 5.5 `V` is replaced either by `R[CL]` or by one of the dedicated
records below.

The tenth-revision `CL` wire projection is total and injective. It supersedes
the legacy `$label` alternative in Section 4.1:

```text
ATOMIC(None)       -> null
ATOMIC(bool)       -> bare JSON boolean
ATOMIC(int)        -> bare JSON integer
ATOMIC(str)        -> bare JSON string
ATOMIC(float)      -> {"$float":value.hex()}
ATOMIC(complex)    -> {"$complex":[real.hex(),imag.hex()]}
ATOMIC(bytes)      -> {"$bytes":lowercase_hex}
ATOMIC(Ellipsis)   -> {"$ellipsis":true}
IDENTITY(anchor)   -> {"$identity_anchor":anchor}
TUPLE(items)       -> {"$tuple":[canonical_literal(item),...]}
LIST(items)        -> {"$list":[canonical_literal(item),...]}
FROZENSET(items)   -> {"$frozenset":[canonical_literal(item),...]}
DICT(entries)      -> {"$dict":[[exact_string_key,
                         canonical_literal(value)],...]}
NDARRAY(value)     -> {"$ndarray":{"dtype":S,"shape":[I,...],
                         "strides":[I,...],"hasobject":B,
                         "writeable":B,"content":H}}
```

Exact-type dispatch tests `bool` before `int`. Integers have at most 4096
bits, strings at most 4096 strict-UTF-8 bytes, bytes at most 65,536 bytes, and
float/complex components are finite. Tuple/list preserve order and may be
empty. Frozenset members sort by full canonical bytes and duplicate bytes
fail. A `LiteralDictEntry` remains an in-memory record, but its wire form is
the two-element pair above; keys are exact strings sorted by strict UTF-8,
unique, and cannot begin with `$`. NDARRAY shape and strides have equal
length; shape entries are non-negative; content is the `array-content` domain
digest. Every tag object has exactly one top-level tag and no extra field.
`$label` is a reserved negative legacy form, ordinary `RL` references are bare
validated `rec:<token>` strings, and only `$identity_anchor` represents a live
identity in `CL`.

Every `CL` is an acyclic tree with maximum nesting depth 32 (the root has
depth zero), at most 256 immediate members in any container, at most 4096
literal nodes over the complete tree, and at most 1,048,576 canonical UTF-8
bytes. Shared but non-cyclic source objects are legal and are tree-expanded at
each occurrence, which counts again against both node and byte budgets. Before
sorting, allocating output arrays, or hashing, an iterative preflight walk
checks exact types, the active-path identity set, depth, per-container count,
and total nodes; a bounded streaming size pass then checks canonical bytes.
The walk invokes no candidate protocol. Depth failure is
`GRAPH_DEPTH_EXCEEDED`; item/node/byte failure is
`ABSTRACT_CONTAINER_BOUND_EXCEEDED`. These rules apply to every CL occurrence,
including runtime source keys, callback literals, root-state path keys, and
value expressions.

The anchor tables are exact:

```text
IdentityAnchor(label:IA,value:OBJ,
  acquisition:E[EXTERNAL_BOOTSTRAP,PROJECT_IMPORT,RUNTIME_LOCATED,
  RUNTIME_FACTORY_RESULT,AUDITOR_TCB],binding_record_label:O[RL],
  binding_owner_table:O[E[ClosedOwnerTable]],
  root_scope_anchor:RS,binding_digest:H)
RootScopeAnchor(label:RS,root_function_label:RL,
  root_function_identity_anchor:IA,root_code_digest:H)
PackageRootAnchor(label:PR,resolved_realpath:S,
  package_relative_prefix:S,source_bundle_digest:H)
```

Two former Section 5.5 records are explicitly replaced because their raw
objects were not named `...identity` and therefore cannot be covered by a
suffix rewrite:

```text
ExternalIdentityEntry(label:RL,value_identity_anchor:IA,
  disposition:E[SAFE_VALUE,SAFE_CALLABLE,SAFE_FACTORY,SAFE_TYPE_OPERAND,
  NAMESPACE_ROOT,FORBIDDEN_RANDOM,FORBIDDEN_DYNAMIC],
  role:E[READONLY_VALUE,PURE_CALL,CONSTRAINED_FACTORY,TYPE_CHECK_ONLY,
  NAMESPACE_ONLY,FORBIDDEN_ONLY],reason:S,reference_token:S,
  provider_module:S,qualified_name:S,identity_category:S,
  state_policy:E[IMMUTABLE_BUILTIN,PYTHON_FUNCTION,NUMPY_DISPATCHER,
  NUMPY_UFUNC_EXPORT,BINARY_EXPORT,TYPE_MEMBER,STRUCTURED_INSTANCE,
  EXTERNAL_CLASS,MODULE_NAMESPACE,NOT_APPLICABLE],state_fields:tuple[S],
  state_accessors:tuple[R[StateFieldAccessor]],state_digest:O[H],
  python_version:S,numpy_version:O[S],source_sha256:O[H],
  binary_sha256:O[H],root_scope_anchor:RS)
StateFieldAccessor(field_name:S,mode:E[EXACT_DICT_LOOKUP,
  EXACT_INSTANCE_DICT_LOOKUP,EXACT_MEMBER_DESCRIPTOR,
  EXACT_GETSET_DESCRIPTOR,EXACT_BOUNDED_CANONICAL_CONTAINER_SNAPSHOT],
  descriptor_identity_anchor:O[IA],expected_literal:O[R[CL]],
  expected_value_contract_label:O[RL],maximum_items:O[I])
ProjectModuleBinding(label:RL,module_identity_anchor:IA,
  globals_dict_identity_anchor:IA,resolved_origin:S,source_sha256:H,
  root_scope_anchor:RS)
```

`StateFieldAccessor` has exactly one of `expected_literal` and
`expected_value_contract_label` non-null. Descriptor modes require the
descriptor anchor; dictionary/container modes require it null. No raw object
from either replacement enters canonical JSON.

Canonical identity references are exactly
`{"$identity_anchor":"id:<token>"}`. Every former `...identity:OBJ` field is
replaced by `..._identity_anchor:IA`; every `root_scope:LS` and capability
`root_label:L` becomes `root_scope_anchor:RS`; and
`package_root_label:L` becomes `package_root_anchor:PR`. Every `IA` binds one
live object in one `RS`; two anchors in the same policy may not be `is` the
same object. `LabelRegistry` registers only `RL`. `IdentityAnchorRegistry`,
`RootScopeRegistry`, and `PackageRootRegistry` are separate canonical tables
with their own table digests.

Every scope-like `root_label` in `RootInputContract`,
`AuthorizationDependencyGraph`, `RuntimeStateReferenceGraph`,
`AstSiteManifest`, `BytecodeSiteManifest`, `SitePairingManifest`, and
`RootSyntaxInventory` is exactly renamed and retyped as
`root_scope_anchor:RS`; the old field is absent. The same substitution applies
to the manifest and capability records already covered above. Only
`RootScopeAnchor.root_function_label` remains an `RL`, and its target owner is
exactly `project_functions`.

Anchor and top-level metadata references do not enter the 66-owner
cross-record classification array. `IdentityAnchor.binding_record_label` and
`binding_owner_table` are either both null or both non-null; when non-null,
the label registry must resolve the label to exactly that owner and
`binding_digest` must equal its `H_record`. `RootScopeAnchor.root_function_label`
must resolve to `project_functions`, and the top-level policy
`root_function_label` must equal it byte-for-byte. These are validating anchor
backlinks, not authorization edges. All other top-level/registry RL values are
either subject definitions or exact copies of already validated record labels;
no unlisted top-level RL is legal.

#### 5.6.2 Identity sources, tokens, and exact dict operations

```text
ProcessLocalIdentitySource(label:RL,root_scope_anchor:RS,
  kind:E[LIVE_LOCATED,FRAME_OR_PROVIDER_PROJECTION,SYMBOLIC_FRESH],
  source_value_contract_label:RL,live_locator_label:O[RL],
  producer_frame_binding_label:O[RL],producer_input_ordinal:O[I],
  producer_site_key_label:O[RL],producer_transfer_label:O[RL],
  projection_steps:tuple[R[ProjectionStep]],
  projects_to_source_label:O[RL],frame_key_digest:O[H],
  allocation_ordinal:O[I],lifetime_end_site_key_label:RL,
  allowed_consumer_site_labels:LS)
ProcessLocalIdentityToken(label:RL,root_scope_anchor:RS,
  canonical_identity_source_label:RL,projection_source_labels:LS,
  source_id_callsite_key_labels:LS,id_external_identity_label:RL,
  id_semantic_model_label:RL,source_value_contract_label:RL,
  audit_primitive_label:O[RL],allowed_consumer_site_labels:LS,
  allowed_operations:tuple[E[LOCATOR_KEY,HASH,EQUALITY,SET_CONTAINS,
  SET_ADD,SET_REMOVE,DICT_LOOKUP,DICT_SET,DICT_DELETE,DICT_POP,
  TUPLE_SNAPSHOT,IDENTITY_COMPARE]])
```

For `LIVE_LOCATED`, only `live_locator_label` is non-null among source
provenance fields and no allocation ordinal exists. A
`FRAME_OR_PROVIDER_PROJECTION` has exactly one of
`(producer_frame_binding_label,producer_input_ordinal)` or
`(producer_site_key_label,producer_transfer_label)`, a frame digest, optional
projection steps, and an optional predecessor source that must reduce through
an acyclic chain to `LIVE_LOCATED` or `SYMBOLIC_FRESH`. `SYMBOLIC_FRESH`
requires site, transfer, frame digest, and allocation ordinal and has no live
locator or predecessor. Distinct fresh ordinals never merge.

`StateOperationCapability.operation` is exactly `GET_ITEM | SET_ITEM |
DELETE_ITEM | POP_ITEM | METHOD_CALL`. `dict.get`, assignment, `del`, and
`dict.pop` respectively require `DICT_LOOKUP`, `DICT_SET`, `DICT_DELETE`, and
`DICT_POP`; they cannot be represented by generic `METHOD_CALL`. `POP_ITEM`
has separately declared default-present, default-absent, key-missing, normal,
and exact `KeyError` outcomes.

#### 5.6.3 Derived reference classification and runtime graph

The policy cannot declare a reference kind. The audit TCB derives the closed
matrix only from the field trees of the 66 `ClosedOwnerTable` records. Anchor
registries, label/table registries, and top-level policy metadata are outside
this classification domain and use the independent validations in Section
5.6.1. Within the 66-record domain the following rule is exhaustive:

1. a record's subject `label` is a definition, not a reference;
2. `IA`, `RS`, and `PR` fields are anchor references and never enter the RL
   classification array;
3. every remaining `RL`, `O[RL]`, or tuple-of-RL leaf defaults to
   `AUTH_REQUIRES`;
4. only the literal exceptions below override that default; and
5. embedded records are traversed preorder and cannot carry subject labels.

The exception set is exact:

```text
VALIDATES:
  behavior_slot_manifests.project_class_label
  behavior_slot_manifests.entries[*].defining_class_label when state=OWN
  external_abc_states.external_class_label
  external_abc_bootstrap_recipes.external_class_label
  generated_methods.owner_artifact_label
  generated_field_accessors.owner_artifact_label
  generated_stdlib_callbacks.transfer_label
  project_descriptors.project_class_label
  runtime_state_reference_bindings.source_label
  authorization_dependency_graph.node_labels[*]
  authorization_dependency_graph.edges[*].source_label
  authorization_dependency_graph.edges[*].target_label
  authorization_dependency_graph.topological_order[*]
  runtime_state_reference_graph.node_labels[*]
  runtime_state_reference_graph.edges[*].source_label
  runtime_state_reference_graph.edges[*].target_label
  runtime_state_reference_graph.scc_binding_labels[*]
  runtime_state_sccs.member_labels[*]
  runtime_state_sccs.edges[*].source_label
  runtime_state_sccs.edges[*].target_label
  ast_site_manifest.site_records[*]
  bytecode_site_manifest.site_records[*]
  site_pairing_manifest.bytecode_group_labels[*]
  site_pairing_manifest.pairs[*].ast_key_label
  site_pairing_manifest.pairs[*].bytecode_site_group_label
  site_pairing_manifest.intrinsic_subsite_labels[*]
RUNTIME_REF:
  runtime_state_reference_bindings.target_label
```

The reciprocal directions are exact. A project class requires its behavior
manifest, while the manifest and an `OWN` slot validate the owning class; an
`INHERITED` slot still authorizes its distinct defining class. An external
class requires its ABC state, the state requires its bootstrap recipe, and
both state and recipe only validate their external-class backlink. A generated
artifact requires its generated methods/accessors; each child only validates
its owner-artifact backlink. A generated callback transfer requires the
callback binding; `GeneratedStdlibCallbackBinding.transfer_label` only
validates that unique inverse. A class-member binding may require a project
descriptor; `ProjectDescriptorBinding.project_class_label` is the backlink.
Any other bidirectional pair is a schema error until both directions are
explicitly classified. This replaces the over-broad claim that no parent may
ever name a child whose child names the parent.

No tenth-revision field has kind `OWNS`; the literal is retained only to reject
a ninth-revision classification row during migration. Adding an exception,
changing a field path, or classifying one field twice is a schema-version
change requiring new fixtures. The TCB materializes one
`ReferenceFieldRule` per discovered RL leaf from the default plus this exact
exception set before it sees policy values:

```text
ReferenceFieldRule(owner_table:E[closed-owner-table],
  record_discriminator:E[ANY|exact-discriminator],field_path:S,
  cardinality:E[SCALAR,OPTIONAL,ORDERED_TUPLE],
  allowed_target_tables:tuple[E[closed-owner-table]],
  kind:E[OWNS,AUTH_REQUIRES,VALIDATES,RUNTIME_REF],
  schema_field_order:I)
```

The key `(owner_table,record_discriminator,field_path)` is unique and covers
every `RL` field in the closed schema. Construction order is policy key order,
owner-table record ordinal, schema field order, nested-record preorder, then
tuple index. Every reference receives one global zero-based uninterrupted
`reference_ordinal`; derived graph edges reuse it without renumbering after
`OWNS` or `VALIDATES` are filtered. The serialized
`CrossRecordReferenceClassification` is a byte-for-byte derived audit output,
not policy input.

The only runtime-reference source record is:

```text
RuntimeStateReferenceBinding(label:RL,source_label:RL,
  source_owner_table:E[RuntimeBearingOwnerTable],
  source_path:R[RuntimeSourcePath],kind:E[STATE_FIELD,RECEIVER,REFERENT,
  CALLBACK,DEFAULT,CLOSURE,CONTAINER_ENTRY],target_label:RL,
  source_identity_anchor:IA,target_identity_anchor:IA,
  reference_ordinal:I)
RuntimeSourcePath(kind:E[STATE_FIELD_NAME,POSITIONAL_DEFAULT,
  KEYWORD_DEFAULT,CLOSURE_CELL,WEAK_REFERENT,WEAK_CALLBACK,BOUND_RECEIVER,
  CONTAINER_ENTRY],field_name:O[S],ordinal:O[I],keyword:O[S],
  freevar_name:O[S],key_literal:O[R[CL]])
```

`RuntimeBearingOwnerTable` is exactly `runtime_values |
generated_stdlib_callbacks | project_function_bindings |
bound_type_members`. The accepted source-owner/edge/target-owner matrix is
exactly:

| edge kind | source owner | target owner |
| --- | --- | --- |
| `STATE_FIELD` | `runtime_values` | `runtime_values \| generated_stdlib_callbacks` |
| `RECEIVER` | `bound_type_members` | `runtime_values` |
| `REFERENT` | `runtime_values` | `runtime_values` |
| `CALLBACK` | `runtime_values` | `project_function_bindings` |
| `DEFAULT` | `generated_stdlib_callbacks` | `runtime_values` |
| `CLOSURE` | `project_function_bindings` | `runtime_values` |
| `CONTAINER_ENTRY` | `runtime_values` | `runtime_values` |

All unlisted cells fail. The source label resolves to the declared source
owner; the target label resolves to one allowed target owner. `STATE_FIELD`
selects only `STATE_FIELD_NAME(field_name)` declared by the source runtime
value. `DEFAULT` selects exactly one positional ordinal or keyword;
`CLOSURE` selects one `co_freevars` name and ordinal; `REFERENT`, `CALLBACK`,
and `RECEIVER` respectively select the empty-selector `WEAK_REFERENT`,
`WEAK_CALLBACK`, and `BOUND_RECEIVER` forms. `CONTAINER_ENTRY` selects one
canonical key literal. Every other selector field is null. The path must
resolve uniquely in the already frozen source record and its exact state;
unknown, ambiguous, or kind-inconsistent paths fail.

`RuntimeStateReferenceBinding.source_label` is `VALIDATES` and never creates a
runtime edge. `target_label` alone is `RUNTIME_REF`; `reference_ordinal` equals
that target leaf's global classification ordinal. The graph edge source is the
validated `source_label` value. This removes the former two-classification/
one-ordinal ambiguity.

`RuntimeStateReferenceGraph` is derived only from these records.
`RuntimeStateSccBinding` is a validating view and never creates an edge. Two
mandatory non-empty literal SCC fixtures are:

1. `WeakKeyDictionary -> remove callback -> self weakref ->
   WeakKeyDictionary`, with `STATE_FIELD`, `DEFAULT`, and `REFERENT` edges;
   and
2. `resolution records dict -> identity record -> weakref -> discard callback
   -> records dict`, with `CONTAINER_ENTRY`, `STATE_FIELD`, `CALLBACK`, and
   `CLOSURE` edges. The weakref-to-resolution referent and
   identity-record-to-ownership-snapshot edges remain non-SCC edges.

The WDK fixture proves the callback's exact stdlib source/code/default weakref,
same-object referent, null weakref callback, and `DICT_DELETE`; the resolution
fixture proves closure identity, referent identity, and distinct get/set/pop
operations. Same-code/different-default callbacks, copied dicts, wrong
referents, missing/extra members, and wrong edge kinds are RED mutations.

#### 5.6.4 ABC bootstrap stabilization

```text
ExternalAbcBootstrapRecipe(label:RL,external_class_label:RL,
  ordered_probe_records:tuple[R[AbcProbe]])
AbcProbe(operation:E[INSTANCE_CHECK,SUBCLASS_CHECK],
  operand_type_identity_anchor:IA,expected_boolean:B)
AbcDump(registry_referent_identity_anchors:tuple[IA],
  positive_cache_referent_identity_anchors:tuple[IA],
  negative_cache_referent_identity_anchors:tuple[IA],
  negative_cache_version:I)
ExternalAbcStateBinding(label:RL,root_scope_anchor:RS,
  external_class_label:RL,abcmeta_identity_anchor:IA,
  abc_impl_identity_anchor:IA,abc_impl_type_label:RL,
  abc_binary_anchor_digest:H,bootstrap_recipe_label:RL,
  prewarm_dump:R[AbcDump],warm_dump:R[AbcDump],stable_dump:R[AbcDump],
  warm_digest:H,stable_digest:H)
```

After anchors and the literal recipe exist but before final policy freeze, the
bootstrap reads PREWARM, executes the complete probe schedule, reads WARM,
executes the same schedule again, and reads STABLE. Results must equal the
literal booleans and `WARM == STABLE`; only the stable digest enters policy.
`ABC_DUMP` is a bootstrap-only accessor mode. `_abc._get_dump` cannot be an
external safe identity, callsite capability, audit-state primitive, or
traversal provider. Registration/reset, probe reordering, one-pass warmup, dead
or unanchored referents, or post-warm mutation fail.
Each `AbcDump` tuple is sorted by identity-anchor UTF-8 bytes after every live
weakref referent is resolved and anchor-checked; dead, duplicate, unanchored,
or same-object/different-anchor entries fail. The version is an exact bounded
non-negative integer. Dump canonical bytes contain only anchor strings and the
version, never weakref objects, raw ids, hashes, or representations.

#### 5.6.5 Label-free value expressions

The former sixteen surface constructors remain accepted only as migration
inputs. `UNION` and `EXTERNAL_RESULT` are wrappers and are absent from the
stored base-kind enum. The sole stored record is:

```text
ValueContract(label:RL,expression:R[ValueExpressionNormalForm])
ValueExpressionNormalForm(clauses:tuple[R[ValueClause]])
ValueClause(value:R[LabelFreeValueNormalForm],
  provenance:R[ProvenanceRequirement])
ProvenanceRequirement(kind:E[ANY_PRODUCER,EXACT_PRODUCER],
  producer_capability_label:O[Ref[callsite_capabilities,
  attribute_capabilities,state_operation_capabilities,
  protocol_capabilities,binary_operator_capabilities]])
```

`Ref[T1,...,Tn;K]` is a machine-schema annotation over one bare `RL` wire
string, where the listed target owner tables are a non-empty proper subset of
`ClosedOwnerTable` and `K` is the static reference kind (default
`AUTH_REQUIRES`). It adds no wrapper or authority. Before policy values are
read, the schema compiler emits the corresponding reference rule from the
owner table, exact branch discriminator, field path, cardinality, target set,
kind, and schema order. A policy value can only prove that the named record
exists in the predeclared set; it cannot select or widen that set.

`AtomicCL` is `CL` restricted to `ATOMIC`; `IntAtomicCL` further restricts it
to exact `int`. `LabelFreeValueNormalForm` is exactly:

```text
LabelFreeValueNormalForm(kind:E[EXACT_ATOMIC,ATOMIC_DOMAIN,BOUNDED_BYTES,
  DIGESTED_BYTES,EXACT_IDENTITY,EXACT_TYPE_TERMINAL,STRUCTURED,CONTAINER,
  ARRAY,ITERABLE,ITERATOR,DICT_VIEW,PROJECT_CALLABLE,
  PROCESS_LOCAL_IDENTITY_TOKEN],payload:R[discriminator-selected record])

ExactAtomicPayload(atomic_type_label:Ref[external_classes],
  atomic_value:R[AtomicCL])
AtomicDomainPayload(atomic_type_label:Ref[external_classes],
  atomic_literals:tuple[R[AtomicCL]],lower_bound:O[R[AtomicCL]],
  upper_bound:O[R[AtomicCL]])
BoundedBytesPayload(atomic_type_label:Ref[external_classes],
  maximum_byte_length:I,audit_only:true)
DigestedBytesPayload(atomic_type_label:Ref[external_classes],byte_length:I,
  maximum_byte_length:I,bytes_sha256:H,audit_only:true)
ExactIdentityPayload(identity_anchor:IA)
ExactTypeTerminalPayload(type_label:Ref[external_classes],
  exact_type_identity_anchor:IA)
StructuredPayload(identity_anchor:O[IA],
  type_label:Ref[project_classes,external_classes],
  fields:tuple[R[StructuredFieldNormalForm]])
StructuredFieldNormalForm(attribute:S,
  access_binding_label:Ref[generated_field_accessors,project_descriptors,
  external_type_members],value:R[ValueExpressionNormalForm])
ArrayShapeBound(minimum:I,maximum:I)
ArrayPayload(type_label:Ref[external_classes],array_dtype:S,array_ndim:I,
  array_shape_bounds:tuple[R[ArrayShapeBound]],array_hasobject:B,
  array_writeable:B,array_c_contiguous:B,array_identity_anchor:O[IA],
  array_content_digest:O[H])
IterablePayload(iterable_contract_label:Ref[iterable_contracts])
ProjectCallablePayload(callable_kind:E[FUNCTION,CLASS],
  callable_binding_label:Ref[project_function_bindings,project_classes],
  project_function_contract_label:O[Ref[project_functions]])
ProcessLocalIdentityTokenPayload(
  process_local_identity_token_label:Ref[process_local_identity_tokens])
ContainerPayload(container_kind:E[TUPLE,LIST,DICT,SET,FROZENSET,
  MAPPING_PROXY,RANGE],identity_anchor:O[IA],
  container_type_label:Ref[external_classes],exact_length:O[I],
  minimum_length:O[I],maximum_length:O[I],
  range_start:O[R[IntAtomicCL]],range_stop:O[R[IntAtomicCL]],
  range_step:O[R[IntAtomicCL]],
  element_contracts:tuple[R[ValueExpressionNormalForm]],
  key_contract:O[R[ValueExpressionNormalForm]],
  mapped_value_contract:O[R[ValueExpressionNormalForm]])
```

The selected payload record is, in base-kind order: `ExactAtomicPayload`,
`AtomicDomainPayload`, `BoundedBytesPayload`, `DigestedBytesPayload`,
`ExactIdentityPayload`, `ExactTypeTerminalPayload`, `StructuredPayload`,
`ContainerPayload`, `ArrayPayload`, `IterablePayload`, `IterablePayload`,
`IterablePayload`, `ProjectCallablePayload`, and
`ProcessLocalIdentityTokenPayload`. Canonical JSON is exactly
`{"kind":<literal>,"payload":<selected-record>}`. Selected optional fields
are explicit null, selected tuple fields are arrays even when empty, and
unselected payload fields are absent.

Atomic-domain literal form has a non-empty canonical-byte-sorted unique
`atomic_literals` tuple and null bounds. Interval form has an empty literal
tuple and two same-exact-type inclusive bounds, limited to int or finite
float. Byte lengths are finite, non-negative, and a digested length does not
exceed its maximum. Structured fields sort by unique attribute UTF-8 bytes;
legacy `provenance_label` must be null and is not stored because producer
provenance is represented only by `ProvenanceRequirement`.

Container length uses exactly one of non-negative `exact_length` or a
non-negative inclusive `(minimum_length,maximum_length)` pair. `TUPLE` and
`LIST` require exact length equal to the ordered element-expression count;
keys, mapped value, and range fields are null. `SET` and `FROZENSET` use
canonical-byte-sorted unique element expressions and null key/range fields;
an empty element tuple is legal only when maximum length is zero. `DICT` and
`MAPPING_PROXY` have non-null key and mapped-value expressions, empty element
tuple, and null range fields. `RANGE` has non-null exact start/stop/step,
non-zero step, exact length equal to bounded built-in range arithmetic, empty
element tuple, and null key/mapped fields. The external class referenced by
`container_type_label` must be the exact built-in type selected by
`container_kind`.

Array bounds have `0 <= minimum <= maximum`, their count equals ndim, and
identity/content are either both null or both non-null. Iterable, iterator,
and dict-view base kinds respectively require an `IterableContract` with the
same kind. A FUNCTION project callable requires a project-function binding
and a non-null `ProjectFunctionContract` that names that binding; CLASS
requires a project-class binding, null function contract, and non-null
constructor semantic/outcome records on the class binding.

Stored expressions contain `1..32` clauses, have recursive depth at most the
active `graph_depth` limit (32 in the acceptance profile), are tree-expanded,
and contain no cycle. Shared semantic subexpressions therefore repeat their
canonical bytes rather than introduce an untyped reference.

A plain surface base kind lowers to one `ANY_PRODUCER` clause.
`EXTERNAL_RESULT(p,B)` lowers every clause of `B` and intersects provenance
with exact producer `p`. `UNION` recursively lowers and concatenates its two
or more distinct alternatives. Legacy identity-bearing fields require an
external one-to-one `LegacyIdentityMigrationAlias(legacy_label:RL,
identity_anchor:IA)` map validated against the identity-anchor registry before
lowering; it is migration input, not canonical policy authority. A missing,
duplicate, or same-object/different-anchor alias fails. A v10 policy and its
KAT contain only the lowered anchor form.

`ProvenanceRequirement.producer_capability_label` is null for
`ANY_PRODUCER`; for `EXACT_PRODUCER` it is a
`Ref[callsite_capabilities,attribute_capabilities,
state_operation_capabilities,protocol_capabilities,
binary_operator_capabilities]`. This same target set applies to the legacy
`EXTERNAL_RESULT.producing_capability_label` migration input.

Producer intersection is `ANY∩ANY=ANY`, `ANY∩P=P`, `P∩P=P`, and
`P∩Q=EMPTY` for `P != Q`; containment is `ANY>=ANY`, `ANY>=P`, and `P>=P`
only. Policy cannot declare producer exclusivity. Normalization recursively
normalizes values, sorts clauses by `(base-kind rank,canonical value bytes,
provenance rank,producer label bytes)`, removes byte-identical clauses, merges
exactly expressible same-provenance values, then removes clauses strictly
contained in value×provenance product space. An unrepresentable overlap is a
policy error and an analyzer `UNKNOWN_VALUE_PROVENANCE`. The 32-clause limit is
checked before insertion. Two policy labels with equal expression bytes are a
construction error. Commutative derived evidence stores sorted operand
expression digests, never labels or call order.

The literal 16×16 ordered-cell KAT contains left/right surface bytes, optional
expected normalized bytes, disjointness, and both containment booleans. It
tests both operand orders, normalization idempotence, union distribution,
external-result lowering, duplicate semantic labels, raw versus produced,
different producers, interval intersection, bytes variants, and identity
classification. Expected bytes are literals produced by an independent
reference worksheet, never by the implementation under test.

#### 5.6.6 Closed replacements for former open records

`EnumRecipe` replaces its six open values with ordered
`EnumNameBinding(name:S,member_name:S)`,
`EnumValueMemberBinding(value_contract_label:RL,member_name:S)`, and
`EnumUnhashableValueMapEntry(member_name:S,value_contract_labels:LS)` tuples;
`EnumMember` contains `value_contract_label:RL`. It separately freezes
`members_mapping_entries`, `member_map_entries`, `member_names_state`,
`value2member_entries`, `unhashable_value_contract_labels`, and
`unhashable_value_map_entries`; each must reproduce the exact generated Enum
state and cross-close names, aliases, members, and values.

```text
EnumRecipe(base_labels:LS,metaclass_label:RL,member_names:tuple[S],
  members:tuple[R[EnumMember]],aliases:tuple[R[EnumAlias]],
  members_mapping_entries:tuple[R[EnumNameBinding]],
  member_map_entries:tuple[R[EnumNameBinding]],member_names_state:tuple[S],
  value2member_entries:tuple[R[EnumValueMemberBinding]],
  unhashable_value_contract_labels:LS,
  unhashable_value_map_entries:tuple[R[EnumUnhashableValueMapEntry]],
  missing_label:O[RL],new_label:RL,
  version_dependency_records:tuple[R[ClassMemberRecord]])
EnumMember(name:S,identity_anchor:IA,value_contract_label:RL)
EnumAlias(alias_name:S,target_member_name:S)
EnumNameBinding(name:S,member_name:S)
EnumValueMemberBinding(value_contract_label:RL,member_name:S)
EnumUnhashableValueMapEntry(member_name:S,value_contract_labels:LS)
```

`GeneratedStdlibCallbackBinding` replaces open defaults/closure/load fields by
`CallbackDefaultBinding`, `CallbackKeywordDefaultBinding`,
`CallbackClosureBinding`, and `CallbackLoadBinding`. Each default/closure
record has a closed binding-kind discriminator and one target `RL`;
`CallbackLoadBinding` fixes offset, ordinal, a closed target-profile
`CallbackLoadOpcode`, source kind, and discriminator-selected literal/source/
target fields. Independent bytecode scanning must cover every actual `LOAD_*`
exactly once. The binding now contains `transfer_label`, and the transfer
contains `callback_binding_label`; these are a strict one-to-one inverse.
`generated_stdlib_callbacks` is a callback/transfer-pair budget, checked
atomically before inserting the two policy records.

```text
GeneratedStdlibCallbackBinding(label:RL,parent_runtime_value_label:RL,
  source_state_field_binding_label:RL,function_identity_anchor:IA,
  stdlib_relative_source:S,source_sha256:H,code_digest:H,
  positional_defaults:tuple[R[CallbackDefaultBinding]],
  keyword_defaults:tuple[R[CallbackKeywordDefaultBinding]],
  closure_cells:tuple[R[CallbackClosureBinding]],
  load_bindings:tuple[R[CallbackLoadBinding]],transfer_label:RL,
  semantic_model_label:RL,outcome_contract_label:RL,
  pre_state_digest:H,post_state_digest:H)
CallbackDefaultBinding(parameter_name:S,default_ordinal:I,
  binding_kind:E[VALUE_CONTRACT,EXTERNAL_IDENTITY,PROJECT_RUNTIME_VALUE,
  GENERATED_CALLBACK,BOUND_TYPE_MEMBER],target_label:RL)
CallbackKeywordDefaultBinding(keyword:S,
  binding_kind:E[VALUE_CONTRACT,EXTERNAL_IDENTITY,PROJECT_RUNTIME_VALUE,
  GENERATED_CALLBACK,BOUND_TYPE_MEMBER],target_label:RL)
CallbackClosureBinding(freevar_name:S,freevar_ordinal:I,
  binding_kind:E[VALUE_CONTRACT,EXTERNAL_IDENTITY,PROJECT_RUNTIME_VALUE,
  GENERATED_CALLBACK,BOUND_TYPE_MEMBER],target_label:RL)
CallbackLoadBinding(instruction_offset:I,instruction_ordinal:I,
  opcode:E[CallbackLoadOpcode],source_kind:E[CONSTANT,
  POSITIONAL_PARAMETER,KEYWORD_PARAMETER,DERIVED_LOCAL,GLOBAL,BUILTIN,
  CLOSURE_CELL,ATTRIBUTE_SITE],literal_name:O[S],source_ordinal:O[I],
  target_label:O[RL],literal_value:O[R[CL]])
```

For `CONSTANT`, only `literal_value` is non-null; for positional/keyword/
derived-local sources only `source_ordinal` is non-null; for GLOBAL, BUILTIN,
CLOSURE_CELL, and ATTRIBUTE_SITE, `literal_name` and `target_label` are
non-null and the other selector fields are null. Defaults preserve positional
order, keyword defaults sort by keyword UTF-8, closures follow `co_freevars`,
and load bindings follow instruction offset then ordinal. Independent bytecode
scanning covers every matching `LOAD_*` exactly once.

`RootStructuredStateContract` replaces open fields with ordered
`RootFieldContract` and `RootNestedBinding` records. A field declares one of
`SLOT_DESCRIPTOR | GENERATED_FIELD_ACCESSOR | PROJECT_DESCRIPTOR |
CLASS_CONSTANT`, its access binding, and value contract. A nested binding has a
non-empty, canonical path of FIELD/TUPLE_INDEX/LIST_INDEX/DICT_KEY steps, one
of `IDENTITY | ARRAY_CONTENT | MUTABLE_CONTAINER_CONTENT`, its value contract,
and discriminator-selected pre/post content digests. Paths are unique, sorted,
and must begin at a declared root field.

```text
RootStructuredStateContract(label:RL,parameter_name:S,
  runtime_identity_anchor:IA,project_type_binding_label:RL,
  construction_provenance:E[AUDITOR_CONSTRUCTED,PROJECT_FACTORY_OWNED],
  constructor_or_factory_label:RL,validator_or_ownership_gate_label:RL,
  field_contracts:tuple[R[RootFieldContract]],pre_state_digest:H,
  post_state_digest:H,nested_bindings:tuple[R[RootNestedBinding]])
RootFieldContract(field_name:S,access_kind:E[SLOT_DESCRIPTOR,
  GENERATED_FIELD_ACCESSOR,PROJECT_DESCRIPTOR,CLASS_CONSTANT],
  access_binding_label:RL,value_contract_label:RL)
RootStatePathStep(kind:E[FIELD,TUPLE_INDEX,LIST_INDEX,DICT_KEY],
  field_name:O[S],index:O[I],key_literal:O[R[CL]])
RootNestedBinding(path:tuple[R[RootStatePathStep]],
  kind:E[IDENTITY,ARRAY_CONTENT,MUTABLE_CONTAINER_CONTENT],
  value_contract_label:RL,pre_content_digest:O[H],post_content_digest:O[H])
```

Each path is non-empty and each step has exactly its discriminator-selected
field. `IDENTITY` has both content digests null; the two content kinds have
both non-null. Field names and canonical paths are unique, and every nested
path starts at one declared field.

`InterpreterOpcodeProfile.lowering_rows` is
`tuple[R[OpcodeLoweringRow]]`. Each row has closed site kind, grouping rule,
position rule, and canonical alternatives of ordered `OpcodePattern` records.
`BytecodeSiteKey.opcode` is the same closed `ProviderOpcode` enum. There is
exactly one row per site kind and every opcode must exist in the frozen opmap.

```text
InterpreterOpcodeProfile(label:RL,python_version:S,opmap_digest:H,
  ignored_opcodes:tuple[E[ProviderOpcode]],
  lowering_rows:tuple[R[OpcodeLoweringRow]])
OpcodeLoweringRow(site_kind:E[SiteKind],grouping_rule:E[ONE_OF_SINGLE,
  OPTIONAL_PREFIX_THEN_ONE,ORDERED_SEQUENCE,ITERATION_PAIR,
  CONTEXT_NORMAL_SHAPE,CONTEXT_EXCEPTION_SHAPE],position_rule:E[
  EXACT_AST_SPAN,CONTAINED_NO_SMALLER_DESCENDANT,SYNTHETIC_WITH_SPAN],
  alternatives:tuple[R[OpcodeAlternative]])
OpcodeAlternative(steps:tuple[R[OpcodePattern]])
OpcodePattern(opcode:E[ProviderOpcode],argument_rule:E[NONE,ANY,EXACT_INT,
  EXACT_STRING,CONST_NONE],exact_int:O[I],exact_string:O[S],repeat_count:I)
```

`NONE`, `ANY`, and `CONST_NONE` have both exact selector fields null;
`EXACT_INT` selects only `exact_int`; `EXACT_STRING` selects only
`exact_string`. Rows follow SiteKind enum rank, alternatives sort by canonical
bytes without duplicates, steps retain execution order, and every SiteKind
appears exactly once.

#### 5.6.7 Exact CPython lowering and JSON semantics

The following enums and records are closed. `SiteKind` is exactly
`CALL | ATTRIBUTE_READ | ATTRIBUTE_WRITE | ATTRIBUTE_DELETE |
SUBSCRIPT_READ | SUBSCRIPT_WRITE | SUBSCRIPT_DELETE | ITERATION | COMPARE |
UNARY | BINARY_OPERATOR | TRUTH | CONTEXT_ENTER | CONTEXT_EXIT_NORMAL |
CONTEXT_EXIT_EXCEPTION`. `CallbackLoadOpcode` is exactly the subset
`LOAD_ASSERTION_ERROR | LOAD_ATTR | LOAD_BUILD_CLASS | LOAD_CLOSURE |
LOAD_CONST | LOAD_DEREF | LOAD_FAST | LOAD_FAST_AND_CLEAR | LOAD_FAST_CHECK |
LOAD_FROM_DICT_OR_DEREF | LOAD_FROM_DICT_OR_GLOBALS | LOAD_GLOBAL |
LOAD_LOCALS | LOAD_METHOD | LOAD_NAME | LOAD_SUPER_ATTR |
LOAD_SUPER_METHOD | LOAD_ZERO_SUPER_ATTR | LOAD_ZERO_SUPER_METHOD`.

`ProviderOpcode` is exactly the following CPython `3.12.10` `dis.opmap`
name set; no specialized, quickened, private, or later-version name may be
inserted:

```text
BEFORE_ASYNC_WITH, BEFORE_WITH, BINARY_OP, BINARY_SLICE, BINARY_SUBSCR,
BUILD_CONST_KEY_MAP, BUILD_LIST, BUILD_MAP, BUILD_SET, BUILD_SLICE,
BUILD_STRING, BUILD_TUPLE, CACHE, CALL, CALL_FUNCTION_EX, CALL_INTRINSIC_1,
CALL_INTRINSIC_2, CHECK_EG_MATCH, CHECK_EXC_MATCH, CLEANUP_THROW, COMPARE_OP,
CONTAINS_OP, COPY, COPY_FREE_VARS, DELETE_ATTR, DELETE_DEREF, DELETE_FAST,
DELETE_GLOBAL, DELETE_NAME, DELETE_SUBSCR, DICT_MERGE, DICT_UPDATE,
END_ASYNC_FOR, END_FOR, END_SEND, EXTENDED_ARG, FORMAT_VALUE, FOR_ITER,
GET_AITER, GET_ANEXT, GET_AWAITABLE, GET_ITER, GET_LEN, GET_YIELD_FROM_ITER,
IMPORT_FROM, IMPORT_NAME, INSTRUMENTED_CALL, INSTRUMENTED_CALL_FUNCTION_EX,
INSTRUMENTED_END_FOR, INSTRUMENTED_END_SEND, INSTRUMENTED_FOR_ITER,
INSTRUMENTED_INSTRUCTION, INSTRUMENTED_JUMP_BACKWARD,
INSTRUMENTED_JUMP_FORWARD, INSTRUMENTED_LINE,
INSTRUMENTED_LOAD_SUPER_ATTR, INSTRUMENTED_POP_JUMP_IF_FALSE,
INSTRUMENTED_POP_JUMP_IF_NONE, INSTRUMENTED_POP_JUMP_IF_NOT_NONE,
INSTRUMENTED_POP_JUMP_IF_TRUE, INSTRUMENTED_RESUME,
INSTRUMENTED_RETURN_CONST, INSTRUMENTED_RETURN_VALUE,
INSTRUMENTED_YIELD_VALUE, INTERPRETER_EXIT, IS_OP, JUMP, JUMP_BACKWARD,
JUMP_BACKWARD_NO_INTERRUPT, JUMP_FORWARD, JUMP_NO_INTERRUPT, KW_NAMES,
LIST_APPEND, LIST_EXTEND, LOAD_ASSERTION_ERROR, LOAD_ATTR, LOAD_BUILD_CLASS,
LOAD_CLOSURE, LOAD_CONST, LOAD_DEREF, LOAD_FAST, LOAD_FAST_AND_CLEAR,
LOAD_FAST_CHECK, LOAD_FROM_DICT_OR_DEREF, LOAD_FROM_DICT_OR_GLOBALS,
LOAD_GLOBAL, LOAD_LOCALS, LOAD_METHOD, LOAD_NAME, LOAD_SUPER_ATTR,
LOAD_SUPER_METHOD, LOAD_ZERO_SUPER_ATTR, LOAD_ZERO_SUPER_METHOD, MAKE_CELL,
MAKE_FUNCTION, MAP_ADD, MATCH_CLASS, MATCH_KEYS, MATCH_MAPPING,
MATCH_SEQUENCE, NOP, POP_BLOCK, POP_EXCEPT, POP_JUMP_IF_FALSE,
POP_JUMP_IF_NONE, POP_JUMP_IF_NOT_NONE, POP_JUMP_IF_TRUE, POP_TOP,
PUSH_EXC_INFO, PUSH_NULL, RAISE_VARARGS, RERAISE, RESERVED, RESUME,
RETURN_CONST, RETURN_GENERATOR, RETURN_VALUE, SEND, SETUP_ANNOTATIONS,
SETUP_CLEANUP, SETUP_FINALLY, SETUP_WITH, SET_ADD, SET_UPDATE, STORE_ATTR,
STORE_DEREF, STORE_FAST, STORE_FAST_MAYBE_NULL, STORE_GLOBAL, STORE_NAME,
STORE_SLICE, STORE_SUBSCR, SWAP, UNARY_INVERT, UNARY_NEGATIVE, UNARY_NOT,
UNPACK_EX, UNPACK_SEQUENCE, WITH_EXCEPT_START, YIELD_VALUE
```

The profile additionally freezes the numeric mapping rather than only that
name set:

```text
opmap_digest = DH("provider-opmap",{
  "schema":"selcal.provider-opmap.v2",
  "python_version":"3.12.10",
  "entries":[{"name":name,"opcode":exact_int}
             for name in ProviderOpcode enum order]})
```

`ProviderOpcode` enum order is the UTF-8 lexical order displayed above.
Every numeric value is obtained independently from the accepted interpreter's
`dis.opmap`; names, values, count, Python version, and digest must all match.
The exact lowering structures are:

```text
Pep657Position(start_line:O[I],end_line:O[I],start_col:O[I],end_col:O[I])
OpcodeAnchor(offset:I,opcode:E[ProviderOpcode],arg:O[I],
  argval_literal:O[R[CL]],positions:R[Pep657Position])
BytecodeLoweringRole(role_ordinal:I,site_kind:E[SiteKind],
  ast_key_label:RL,ordered_bytecode_key_labels:LS)
BytecodeSiteGroup(label:RL,owner_code_digest:H,
  lowering_kind:E[SIMPLE,FUSED_COMPARE_TRUTH,FUSED_NONE_COMPARE_TRUTH,
  SUPER_ATTRIBUTE,SUPER_METHOD_CALL],
  roles:tuple[R[BytecodeLoweringRole]],
  context_instructions:tuple[R[OpcodeAnchor]])
SitePair(site_kind:E[SiteKind],ast_key_label:Ref[ast_site_keys;VALIDATES],
  bytecode_site_group_label:Ref[bytecode_site_groups;VALIDATES],
  role_ordinal:I,evaluation_ordinal:I)
AstSiteManifest(label:RL,root_scope_anchor:RS,
  source_index_digests:tuple[H],
  site_records:tuple[Ref[ast_site_keys;VALIDATES]])
BytecodeSiteManifest(label:RL,root_scope_anchor:RS,code_digests:tuple[H],
  site_records:tuple[Ref[bytecode_site_keys;VALIDATES]])
SitePairingManifest(label:RL,root_scope_anchor:RS,opcode_profile_digest:H,
  ast_manifest_digest:H,bytecode_manifest_digest:H,
  bytecode_group_labels:tuple[Ref[bytecode_site_groups;VALIDATES]],
  pairs:tuple[R[SitePair]],
  intrinsic_subsite_labels:tuple[
    Ref[structural_protocol_site_keys;VALIDATES]],algorithm_version:S)
```

The former embedded labelled `IntrinsicSubsite` record is absent. Its exact
top-level representation is a `StructuralProtocolSiteKey` in
`structural_protocol_site_keys`; the pairing manifest carries only the
validating label tuple above. Pair AST/group labels are likewise `VALIDATES`
references to `ast_site_keys` and `bytecode_site_groups`.

`Pep657Position` preserves the four interpreter values exactly; it does not
fill an absent component from an AST span. `OpcodeAnchor.arg` is null exactly
when `dis.Instruction.arg` is null. `argval_literal` is non-null only when the
independent scanner can encode the exact `argval` in `CanonicalLiteral`;
otherwise it is null and no display string or `repr` substitutes for it.
Context instructions sort by offset, then opcode enum rank, have unique
offsets, and are not themselves provider site keys.

Role ordinals are exactly `0..n-1`; each role has at least one ordered
bytecode-key label. Every bytecode key belongs to exactly one group, although
two roles in that same fused group may reference the same key. Every
`SitePair` resolves to one group role whose `site_kind` and `ast_key_label`
match the pair exactly. Its evaluation ordinal equals the corresponding AST
site ordinal. No pair may refer directly to a context instruction.

`BytecodeSiteGroup` contains `lowering_kind:E[SIMPLE,
FUSED_COMPARE_TRUTH,FUSED_NONE_COMPARE_TRUTH,SUPER_ATTRIBUTE,
SUPER_METHOD_CALL]`, ordered `BytecodeLoweringRole` records, and exact context
opcode anchors. `SitePair` references a group plus role ordinal. A bytecode key
belongs to exactly one group but may be referenced by two roles in that group.
Ordinary conditions bind `COMPARE_OP` plus the following truth jump;
`x is None` and `x is not None` respectively use the single fused
`POP_JUMP_IF_NOT_NONE` and `POP_JUMP_IF_NONE` key for both source compare and
truth roles. Both opcodes enter the TRUTH profile.

`LOAD_SUPER_ATTR` decodes `name_index=arg>>2`, `method_flag=bool(arg&1)`, and
`two_argument_super_flag=bool(arg&2)`. Super groups freeze the `super` load,
zero-argument `__class__`/self loads or two explicit operands, flags/name/span,
and the required adjacent `CALL` for a method. Attribute resolution uses an
independent `SUPER_ATTRIBUTE_INTRINSIC` model; the method call retains its own
capability. Exact KATs cover zero/two-argument attribute and method forms,
fused compare/truth, and every flag/span/role mutation.

`CANONICAL_JSON_DUMPS` is a distinct semantic normal-transfer kind with:

```text
CanonicalJsonDumpsPayload(input_ordinal:I,
  output_kind:E[EXACT_STR,UTF8_BYTES],ensure_ascii:false,allow_nan:false,
  sort_keys:true,item_separator:",",key_separator:":",skipkeys:false,
  check_circular:true,indent:null,cls:null,default:null,
  encoding:E[NOT_APPLICABLE,UTF8],errors:E[NOT_APPLICABLE,STRICT],
  maximum_depth:I,maximum_container_items:I,
  maximum_string_utf8_bytes:I,maximum_output_utf8_bytes:I)
```

Its input grammar is exact `null/bool/int/finite-float/str/list/tuple/dict`
with exact-string keys, finite bounds, no subclasses, no cycles, and no
protocol/custom encoder. It implements exact escaping, key ordering,
finite-float formatting, separators, and output-byte limits independently of
the expected result. The actual `json.dumps` capability yields only
`EXACT_STR`; exact UTF-8 encoding is a separate model. Literal normal,
non-finite/cycle/surrogate/type rejection, and option/escaping/order/output
mutations are mandatory KATs.

#### 5.6.8 Policy-record, table, registry, and site digests

The tenth-revision `RootSyntaxInventory` removes the former untyped digest
tuple and self digest. It is exactly:

```text
RootSyntaxInventory(label:RL,root_scope_anchor:RS,
  entries:tuple[R[RootSyntaxInventoryEntry]])
RootSyntaxInventoryEntry(kind:E[PROJECT_SOURCE,CODE_OBJECT,AST_NODE,
  OPERATOR,PROJECT_CLASS,EXTERNAL_CLASS,BEHAVIOR_SLOT,GENERATED_ARTIFACT,
  GENERATED_CALLBACK_TRANSFER,PROCESS_LOCAL_IDENTITY_TOKEN,
  RUNTIME_STATE_SCC,SEMANTIC_MODEL,INTERPRETER_OPCODE_PROFILE,
  AST_SITE_MANIFEST,BYTECODE_SITE_MANIFEST,SITE_PAIRING_MANIFEST,
  PROJECT_CALL_GRAPH,AUTHORIZATION_GRAPH,RUNTIME_REFERENCE_GRAPH],
  count:I,digests:tuple[H])
```

There is exactly one entry for every enum literal in enum order.
`count` is non-negative and equals the number of reviewed members represented
by the canonical digest tuple, which is empty exactly when count is zero;
member digests sort by their source manifest's
normative order, not by discovery. Singleton manifest/graph/profile entries
have count one and one digest. Project-source, code, AST, operator, class,
artifact, token, SCC, semantic, and call-graph entries bind the independently
reviewed inventories named in Section 5.3 and their exact member counts. The
record has no `digest` field; its only authoritative digest is
`H_record(root_syntax_inventory,record)`, so no self-preimage exists.

The digest allowlist additionally contains `policy-record`, `policy-table`,
`policy-table-manifest`, `site-key-table`, `value-expression`, and
`provenance-requirement`. Exact preimages are:

```text
H_record(table,r) = DH("policy-record",{
  "schema":"selcal.policy-record.v2","owner_table":table,
  "record":canonical(r)})
H_table(table,records) = DH("policy-table",{
  "schema":"selcal.policy-table.v2","owner_table":table,
  "record_count":len(records),
  "record_digests":[H_record(table,r) for r in canonical_table_order]})
```

`PolicyTableManifest` contains every owner table, including empty ones, in
closed owner-enum order. `LabelDefinition.record_digest` equals the exact
owner-table record digest at its ordinal and its label must match. The label
registry preimage binds the complete table manifest. `site-key-table` binds,
in fixed order, the AST, bytecode, bytecode-group, and five structural-site
tables, each with owner name, record count, and ordered record digests; no
empty table can be omitted.

##### 5.6.8.1 Exact owner, registry, policy, and report closure

`ClosedOwnerTable` has exactly these 66 literals in this order:

```text
root_input_contract,project_modules,project_source_indexes,
project_function_bindings,project_classes,behavior_slot_manifests,
external_classes,external_abc_states,external_abc_bootstrap_recipes,
external_python_intrinsics,generated_artifacts,generated_methods,
generated_field_accessors,generated_callback_transfers,external_identities,
project_descriptors,external_type_members,runtime_locator_root_nodes,
runtime_locator_access_steps,runtime_value_locators,
located_bound_callable_handles,process_local_identity_sources,
process_local_identity_tokens,runtime_values,state_fields,runtime_state_sccs,
authorization_dependency_graph,runtime_state_reference_graph,
runtime_state_reference_bindings,generated_stdlib_callbacks,
bound_type_members,value_contracts,root_argument_contracts,
root_structured_state_contracts,argument_contracts,result_contracts,
iterable_contracts,exception_contracts,outcome_contracts,semantic_guards,
semantic_normal_transfers,semantic_exception_transfers,semantic_models,
intrinsic_effect_steps,state_operation_transfers,project_functions,
callsite_capabilities,namespace_capabilities,attribute_capabilities,
state_operation_capabilities,protocol_capabilities,
binary_operator_capabilities,audit_state_reads,interpreter_opcode_profile,
ast_site_keys,bytecode_site_keys,bytecode_site_groups,
structural_callsite_keys,structural_attribute_site_keys,
structural_state_site_keys,structural_operator_site_keys,
structural_protocol_site_keys,ast_site_manifest,bytecode_site_manifest,
site_pairing_manifest,root_syntax_inventory
```

The four registries and table manifest have these exact records:

```text
IdentityAnchorRegistry(anchors:tuple[R[IdentityAnchor]],digest:H)
RootScopeRegistry(anchors:tuple[R[RootScopeAnchor]],digest:H)
PackageRootRegistry(anchors:tuple[R[PackageRootAnchor]],digest:H)
OwnerTableDigest(owner_table:E[ClosedOwnerTable],record_count:I,
  table_digest:H)
PolicyTableManifest(entries:tuple[R[OwnerTableDigest]],digest:H)
LabelDefinition(label:RL,owner_table:E[ClosedOwnerTable],
  record_ordinal:I,record_digest:H)
LabelRegistry(definitions:tuple[R[LabelDefinition]],
  policy_table_manifest_digest:H,
  reference_classifications_digest:H,digest:H)
```

Each registry digest omits its own digest field and hashes exactly
`{"schema":"selcal.<registry-name>.v2","anchors":[...]}` under the
matching `identity-anchor-registry`, `root-scope-registry`, or
`package-root-registry` domain. The canonical IdentityAnchor projection omits
the live `OBJ`; the PackageRootAnchor projection omits `resolved_realpath`.
Those process-only fields are checked against binding/source-bundle evidence
before hashing. `PolicyTableManifest.digest` omits itself and hashes exactly
`{"schema":"selcal.policy-table-manifest.v2","entries":[...]}` under
`policy-table-manifest`. It has exactly 66 entries, ordinally equal to
`ClosedOwnerTable`, including non-zero table-specific empty-table digests.
`LabelRegistry.digest` hashes exactly
`{"definitions":[...],"policy_table_manifest_digest":H,
"reference_classifications_digest":H}` under `label-registry`.

The tenth serialized derived classification is exactly:

```text
CrossRecordReferenceClassification(
  source_owner_table:E[ClosedOwnerTable],source_record_label:RL,
  source_record_ordinal:I,field_path:S,field_reference_ordinal:I,
  global_reference_ordinal:I,target_record_label:RL,
  target_owner_table:E[ClosedOwnerTable],
  kind:E[OWNS,AUTH_REQUIRES,VALIDATES,RUNTIME_REF])
```

`field_reference_ordinal` is the zero-based occurrence within that field;
`global_reference_ordinal` is the uninterrupted ordinal defined in 5.6.3.
The array is sorted only by that global ordinal and must equal the TCB-derived
array byte-for-byte. No policy field can supply, override, or reclassify a row.

The exact `site-key-table` preimage is:

```json
{"schema":"selcal.site-key-table.v2","tables":[{"owner_table":"ast_site_keys","record_count":0,"record_digests":[]},{"owner_table":"bytecode_site_keys","record_count":0,"record_digests":[]},{"owner_table":"bytecode_site_groups","record_count":0,"record_digests":[]},{"owner_table":"structural_callsite_keys","record_count":0,"record_digests":[]},{"owner_table":"structural_attribute_site_keys","record_count":0,"record_digests":[]},{"owner_table":"structural_state_site_keys","record_count":0,"record_digests":[]},{"owner_table":"structural_operator_site_keys","record_count":0,"record_digests":[]},{"owner_table":"structural_protocol_site_keys","record_count":0,"record_digests":[]}]}
```

The zeros are schema examples; a real preimage substitutes exact counts and
ordered `H_record` values without changing field names or the eight-table
order. Its domain is `site-key-table`.

The tenth policy schema has exactly these 84 keys, presented below in schema
order for human review:

```text
schema,root_scope_anchor,root_function_label,root_code_digest,
root_input_contract,package_root_anchor,label_registry,
identity_anchor_registry,root_scope_registry,package_root_registry,
policy_table_manifest,cross_record_reference_classifications,
project_modules,project_source_indexes,project_function_bindings,
project_classes,behavior_slot_manifests,external_classes,external_abc_states,
external_abc_bootstrap_recipes,external_python_intrinsics,
generated_artifacts,generated_methods,generated_field_accessors,
generated_callback_transfers,external_identities,project_descriptors,
external_type_members,runtime_locator_root_nodes,runtime_locator_access_steps,
runtime_value_locators,located_bound_callable_handles,
process_local_identity_sources,process_local_identity_tokens,runtime_values,
state_fields,runtime_state_sccs,authorization_dependency_graph,
runtime_state_reference_graph,runtime_state_reference_bindings,
generated_stdlib_callbacks,bound_type_members,value_contracts,
root_argument_contracts,root_structured_state_contracts,argument_contracts,
result_contracts,iterable_contracts,exception_contracts,outcome_contracts,
semantic_guards,semantic_normal_transfers,semantic_exception_transfers,
semantic_models,intrinsic_effect_steps,state_operation_transfers,
project_functions,callsite_capabilities,namespace_capabilities,
attribute_capabilities,state_operation_capabilities,protocol_capabilities,
binary_operator_capabilities,audit_state_reads,interpreter_opcode_profile,
ast_site_keys,bytecode_site_keys,bytecode_site_groups,
structural_callsite_keys,structural_attribute_site_keys,
structural_state_site_keys,structural_operator_site_keys,
structural_protocol_site_keys,ast_site_manifest,bytecode_site_manifest,
site_pairing_manifest,root_syntax_inventory,limits,bootstrap_digest,
implementation_digest,runtime_binary_anchor_digest,python_version,
numpy_version,challenge_nonce
```

The tenth report schema has exactly these 75 keys, presented below in schema
order for human review:

```text
schema,root_scope_anchor,challenge_nonce,bootstrap_digest,policy_digest,
implementation_digest,label_registry_digest,identity_anchor_registry_digest,
root_scope_registry_digest,package_root_registry_digest,
policy_table_manifest_digest,cross_record_reference_classifications_digest,
root_input_contract_digest,root_argument_contract_digests,
root_structured_state_contract_digests,value_contract_table_digest,
callsite_manifest_digest,capability_manifest_digest,
semantic_guard_manifest_digest,semantic_normal_transfer_manifest_digest,
semantic_exception_transfer_manifest_digest,semantic_model_manifest_digest,
authorization_dependency_graph_digest,runtime_state_reference_graph_digest,
runtime_state_reference_binding_digests,runtime_state_scc_manifest_digest,
process_local_identity_source_manifest_digest,
process_local_identity_token_manifest_digest,interpreter_opcode_profile_digest,
site_pairing_manifest_digest,project_function_manifest_digest,
outcome_manifest_digest,exception_manifest_digest,protocol_manifest_digest,
operator_manifest_digest,root_syntax_inventory_digest,python_version,
numpy_version,platform,runtime_binary_anchor_digest,project_module_digests,
project_source_index_digests,project_class_digests,
behavior_slot_manifest_digests,external_class_digests,
external_abc_state_digests,external_abc_bootstrap_recipe_digests,
external_python_intrinsic_digests,generated_artifact_digests,
generated_method_digests,generated_field_accessor_digests,
project_descriptor_digests,external_type_member_digests,
runtime_value_locator_digests,located_bound_callable_handle_digests,
runtime_value_digests,state_field_digests,
generated_callback_transfer_digests,generated_callback_digests,
bound_member_digests,state_operation_transfer_digests,
audit_state_read_digests,site_key_table_digest,root_state_pre_digests,
root_state_post_digests,referenced_binding_pre_digests,
referenced_binding_post_digests,external_state_pre_digests,
external_state_post_digests,limits,findings,completed,counts,elapsed_seconds,
stable_report_digest
```

`AUDIT-CANONICAL-JSON-V2` always serializes objects with `sort_keys=True`, so
wire and digest object-key order is lexicographic UTF-8 order regardless of
construction/insertion order. Schema order is not serialized authority and an
input mapping reordered before canonicalization must produce identical bytes.
The policy and report sequences in Section 5.4 are historical ninth-revision
negative fixtures only. Missing, extra, renamed, or duplicate logical keys
fail before digest comparison; a raw-byte fixture with noncanonical key order
fails because it is not equal to the canonical serializer output, not because
the source mapping insertion order carried authority.

Report manifest digests use one exact constructor and no field-specific hidden
preimage:

```text
M(name,owner_tables) = DH("policy-table-manifest",{
  "schema":"selcal.report-manifest.v2",
  "manifest_name":name,
  "tables":[{"owner_table":t,"table_digest":H_table(t)}
            for t in the literal order below]})
```

The mapping is exact:

| Report field | Preimage authority |
| --- | --- |
| `callsite_manifest_digest` | `M("callsite", [ast_site_manifest,bytecode_site_manifest,site_pairing_manifest])` |
| `capability_manifest_digest` | `M("capability", [callsite_capabilities,namespace_capabilities,attribute_capabilities,state_operation_capabilities,protocol_capabilities,binary_operator_capabilities,audit_state_reads])` |
| `semantic_guard_manifest_digest` | `M("semantic-guard", [semantic_guards])` |
| `semantic_normal_transfer_manifest_digest` | `M("semantic-normal-transfer", [semantic_normal_transfers])` |
| `semantic_exception_transfer_manifest_digest` | `M("semantic-exception-transfer", [semantic_exception_transfers])` |
| `semantic_model_manifest_digest` | `M("semantic-model", [semantic_models])` |
| `runtime_state_scc_manifest_digest` | `M("runtime-state-scc", [runtime_state_sccs])` |
| `process_local_identity_source_manifest_digest` | `M("process-local-identity-source", [process_local_identity_sources])` |
| `process_local_identity_token_manifest_digest` | `M("process-local-identity-token", [process_local_identity_tokens])` |
| `project_function_manifest_digest` | `M("project-function", [project_functions])` |
| `outcome_manifest_digest` | `M("outcome", [outcome_contracts])` |
| `exception_manifest_digest` | `M("exception", [exception_contracts])` |
| `protocol_manifest_digest` | `M("protocol", [protocol_capabilities])` |
| `operator_manifest_digest` | `M("operator", [binary_operator_capabilities])` |

Singleton report digests
`root_input_contract_digest,authorization_dependency_graph_digest,
runtime_state_reference_graph_digest,interpreter_opcode_profile_digest,
site_pairing_manifest_digest,root_syntax_inventory_digest` equal the exact
`H_record` of the sole record in their named owner table; the table must have
cardinality one. `value_contract_table_digest` equals
`H_table(value_contracts)`. Every report field ending `_digests` and naming a
policy owner table is the canonical record-digest array from that table in its
table order. In particular, `runtime_state_reference_binding_digests` and
`external_abc_bootstrap_recipe_digests` are not aggregate manifests.

`root_state_pre_digests` and `root_state_post_digests` follow
`root_structured_state_contracts` table order and contain those records'
literal pre/post state digests. `referenced_binding_*` is derived by scanning
the classification array in global-reference order, retaining the first
occurrence of each `AUTH_REQUIRES` target that has a declared pre/post state,
and then emitting that target's state digest. `external_state_*` follows
`external_identities` table order after filtering to entries whose
`state_policy != NOT_APPLICABLE` **and** whose `state_digest` is non-null, and
emits the independently re-read pre/post state digest. A `FORBIDDEN_ONLY`
entry with `NOT_APPLICABLE` is excluded and a KAT mutating that exclusion is
RED. A non-`NOT_APPLICABLE` entry with null state digest is a policy error. The
filtered label lists are included in the stable report preimage as part of the
corresponding digest-array element record
`{"label":RL,"digest":H}`; report JSON therefore stores these arrays as
records, not unlabeled hash strings. Root state arrays use the same labelled
element shape. Omission, reorder, duplicate label, or value-only hash arrays
fail.

#### 5.6.9 Observation, mutation, and performance evidence

`AttackWitness.observation_kind` is exactly `PYTHON_CALL_TRACE |
PCG64_STATE_OUTPUT_TRANSITION | NUMPY_UFUNC_OUTPUT_TRANSITION`. Python call
traces alone may claim nested provider calls. PCG64 evidence binds exact
instance token/member/no-argument contract, complete pre/post state, output,
root outcome, nonce-derived fixture, and an independent transition oracle.
Ufunc evidence binds exact export/state, inputs/kwargs, pre/post input/out-array
state, result type/dtype/shape/strides/content, root outcome, fixture, and an
independent operation oracle that cannot call the witnessed ufunc. Native
records support only the bounded state/output-transition claim, not a profiler
claim of directly observing a native call.

The digest allowlist also contains `source-bundle`, `fixture`,
`attack-spec-core`, `trace-nonce-commitment`, `patch-blob`,
`patch-operation`, `patch-set`, `process-identifier-token`,
`python-call-trace`, `native-transition`, and `performance-sample`.
`SourceBundle` contains sorted repository-relative regular-file path/size/SHA
records. `FixtureRecord` binds root, recipe, argument contract/value digests,
structured-state digests, and expected outcome. `AttackSpecCore` is every
attack field except its own digest and nonce commitment; the commitment is
`SHA256(prefix("trace-nonce-commitment") + bytes.fromhex(core_digest) +
nonce_32_raw)` and the final AttackSpec is then domain-hashed. The audit
challenge nonce is independent and cannot be reused.

`PatchBlob` embeds bounded content hex, length, and SHA. Each patch operation
binds repository-relative path, baseline coordinates, whole-file and range
preimages, replacement blob, and postimage. Operations are already sorted by
path/start/end/label, non-overlapping in baseline coordinates, and applied per
file in descending start order; duplicate zero-width insertions are forbidden.
Every attack has exactly one pre-frozen safe counterpart.

`ProcessIdentifierRecord` binds positive PID, process start monotonic time,
runtime-binary anchor, nonce commitment, and a domain-separated token. It is
diagnostic transaction identity, not cross-process authority.

`PerformanceSampleRecord` has stratum/root/cache/role/ordinal and a
discriminated status `PASS | CHILD_NONZERO | PROTOCOL_FAILURE | TIMEOUT`,
elapsed time, optional report/exit/signal/failure-stage fields, and its digest.
Each root×cache stratum contains measured ordinals 0..19; WARM also has one
priming ordinal and COLD does not. P99 exists only if all twenty measured
samples PASS; otherwise `p99=null` and `completed=false`. Failure samples keep
their original ordinal and diagnostic reruns never authorize.

#### 5.6.10 Findings and anti-false-green KATs

`PROCESS_IDENTITY_SOURCES_EXCEEDED` is a distinct focused finding checked
before locator resolution, `id()`, projection, token allocation, or graph-edge
insertion. The finding enum/trigger table therefore contains 67 rows before
any other tenth-revision resource categories are added. Callback budget is the
pair budget above and needs no separate transfer finding.

Wire findings are `FindingReportRecord(...,detail)`; stable findings are
`FindingStableKey(...)`. Stable projection deletes only detail. Sorting and
duplicate rejection use stable-key canonical bytes. Detail changes wire bytes
but cannot affect stable digest or PASS; equal stable keys are an error.

The former eighth KAT is replaced, not extended. Its authorization topo order
is exactly `ast.call,bc.call,bc.group,outcome.call,site.call,
transfer.normal,model.call,cap.call,value.scalar,root.arg,root.input`. Four
additional literal fixtures bind anchor namespaces, all three identity-source
kinds with dict get/set/pop, the WDK SCC, and the resolution-record SCC.

The full non-empty policy KAT contains at least one **actual typed record** in
every owner table and hard-codes every record byte/digest, table digest,
registry, classification, graph, site manifest, policy byte string, and policy
digest. Its stable-report KAT binds all of those digests, non-zero counts, and
two wire findings with different stable keys/details. Expected bytes are
independent literals. Per-table emptying, all-table emptying even after
self-consistent redigestion, wrong-table moves, ordinal/digest substitution,
site-table omission/reorder, and detail/stable projection mutations are RED.

The tenth revision is not eligible for exact-hash review until the two full
literal fixture files and their independently recomputed hashes are present;
descriptions, record counts, opaque digests, or a fixture produced at test time
do not satisfy this gate.

## 6. Policy construction invariants

The normative tenth-revision `ProviderAuditPolicy` schema is defined by
Sections 5.6 and 5.6.8.1. Only Section 5.4's legacy policy/report record
shapes, key sequences, and literal KAT bytes are superseded migration
surfaces. Its finding-category universe, exact trigger conditions, count keys,
and other semantic constraints remain normative unless a specific Section
5.6 rule replaces them. The policy is
root-specific; oracle and migration cannot share a union permission set.

Policy construction fails before graph traversal unless all invariants hold:

1. labels are non-empty and unique;
2. one exact identity has at most one label and disposition per root;
3. safe and forbidden identity sets have zero `is`-intersection;
4. forbidden identities are checked before any safe/capability terminal;
5. project-owned or unknown-origin objects cannot be external safe terminals;
   an external stateful object is eligible only under one exact
   `ExternalStatePolicy` whose source/binary and state digests validate;
6. every callable permission has one exact paired site, named
   argument/outcome contracts, and an independent semantic model; every
   atomic range, structured field,
   iterable/protocol transfer, generated artifact, descriptor/bound/type
   member, runtime value/state operation, project formal, and normal/exception
   outcome is closed and literal;
7. every capability matches exactly one independently paired structural call,
   attribute, state, protocol, or operator site in its declared root,
   irrespective of how many times that site executes;
8. unused consumable authority and unreachable support records fail the audit
   under the exact Section 5.6 partition;
9. the policy factory accepts no root object or discovery callback while
   constructing the external bootstrap;
10. `root_scope` is exactly one declared root for every permission; SHA-256 is
    lowercase hexadecimal; versions and reference tokens are non-empty literal
    strings; disposition/role/state-policy combinations are validated by a
    closed matrix; and canonical metadata and source hashes match their literal
    reviewed values;
11. external identities/classes/ABC states/pinned Python intrinsics, project
    classes/behavior slots, process-local identity sources/tokens,
    locator roots/steps/handles, state fields/SCCs, namespace attributes,
    generated artifacts/transfers, project descriptors/class constants,
    external/bound type members, project runtime values, root fields,
    value/iterable/protocol/exception/outcome contracts, semantic guards/
    transfers/models, intrinsic effects, opcode/site/graph manifests, and
    capabilities come only from the literal reviewed manifest; a
    runtime-observed object may verify one entry but may not create or widen
    it; and
12. no expected outcome, capability, or runtime-observed result may create or
    widen its own semantic model; an unsupported native/builtin/protocol
    operation is `UNKNOWN` and fails closed; and
13. the policy digest, audit implementation digest, runtime-binary anchor,
    parent challenge, root structured-state digests, and every resource limit
    are present and use the single canonical recipe in Sections 4 and 5; and
14. all labels are pre-registered with no orphan or duplicate definition,
    every label reference has exactly one field-level classification, the
    authorization-dependency graph is a bounded DAG, every runtime reference
    cycle matches one exact allowed SCC, each process-local identity token
    binds the same live or symbolic source and its complete consumer set,
    every exact `ABCMeta` type operand has a non-null verified ABC-state
    binding, every external type operand is `TYPE_CHECK_ONLY`, and every
    constructible project class passes the complete behavior-slot/finalizer
    preflight.

The legal disposition matrix is:

- `SAFE_VALUE` with `READONLY_VALUE`, no callable/factory/namespace
  capability, and `IMMUTABLE_BUILTIN`; or `STRUCTURED_INSTANCE` only when an
  exact `ProjectRuntimeValueBinding` or declared structured field consumes the
  identity and every read/mutation is separately authorized. A structured
  instance is never a bare protocol-capable terminal;
- `SAFE_CALLABLE` with `PURE_CALL`, one of `IMMUTABLE_BUILTIN |
  PYTHON_FUNCTION | NUMPY_DISPATCHER | NUMPY_UFUNC_EXPORT | BINARY_EXPORT |
  TYPE_MEMBER`, and one or more exact callsite capabilities in the same root.
  This is the route for exact `len`, `type`, `id`, and other reviewed built-ins;
  `TYPE_MEMBER`
  additionally requires one exact `ExternalTypeMemberBinding` and matching
  attribute/call capability;
- `SAFE_FACTORY` with `CONSTRAINED_FACTORY`, one of `IMMUTABLE_BUILTIN |
  PYTHON_FUNCTION | BINARY_EXPORT | TYPE_MEMBER | STRUCTURED_INSTANCE`, and
  exact callsite/outcome capabilities in the same root. An immutable built-in
  type such as `tuple`, `dict`, or `int` is a factory only at its literal
  callsite and cannot reuse a `PURE_CALL` permission;
- `SAFE_TYPE_OPERAND` with `TYPE_CHECK_ONLY`, `EXTERNAL_CLASS`, one exact
  `ExternalClassBinding`, and one or more exact `INSTANCE_CHECK` protocol
  capabilities. It cannot be a callee, factory, value terminal, namespace,
  generic class allowlist, or constructor permission;
- `NAMESPACE_ROOT` with `NAMESPACE_ONLY`, `MODULE_NAMESPACE`, and at least one
  exact `NamespaceAttributeCapability`, with no bare value/call/factory use;
  and
- `FORBIDDEN_RANDOM` or `FORBIDDEN_DYNAMIC` with `FORBIDDEN_ONLY`,
  `NOT_APPLICABLE`, empty `state_fields/state_accessors`, exact
  `state_digest=null`, and no
  callsite, result, or namespace capability. Source/binary metadata on such an entry is
  diagnostic only and does not enter trusted-state authorization.

No other combination is representable. In particular, `NOT_APPLICABLE` is not
a wildcard, `MODULE_NAMESPACE` cannot authorize a callable or value terminal,
`TYPE_MEMBER` cannot authorize every member of its owner type, and
`EXTERNAL_CLASS` cannot authorize construction or arbitrary members, and
`STRUCTURED_INSTANCE` cannot authorize undeclared attribute, item, iteration,
hashing, equality, or mutation behavior.

`ReceiverBinding.NONE` has no owner or instance; `SELF` has one exact owner and
instance; `CLS` has one exact class owner and no instance; `INSTANCE_OF` has one
exact class owner and no instance. Any other field combination is a policy
error.

The safe manifest is therefore minimum-per-root capability, not a convenience
allowlist.

## 7. Traversal semantics

### 7.1 Project-owned functions

For a project-owned function, the proof traverses code and nested code,
referenced closure nonlocals, referenced globals, referenced built-ins,
defaults, keyword defaults, statically resolvable attribute chains, and exact
call targets. The AST value-provenance pass and object-identity graph must agree
on the owner code digest, callsite coordinates, callee identity, receiver, and
argument/outcome contracts. A disagreement is `CALLSITE_MISMATCH`. A global
edge may be followed for this auxiliary RNG proof, but it never proves
post-seal invariance. The future Slice 4 production proof still requires the
parent design's behavior-bearing `LOAD_GLOBAL` and runtime-import closure.

Any runtime import instruction, unresolved call target, unresolved dynamic
attribute name, or unmanifested runtime-generated code in these two auxiliary
roots is an explicit finding. The only manifested generated-code cases are the
exact dataclass, named-tuple, enum, and code-digest-bound generated-stdlib-
callback transfers in Sections 4.2 and 5.1. Resolver
objects such as
`getattr`, `setattr`, `vars`,
`globals`, `locals`, `__import__`, `eval`, `exec`, and `compile` are rejected by
exact identity even when aliased or stored in a container.

### 7.2 Receivers, classes, and descriptors

Receiver/environment context propagates through every hop. An ordinary
project method follows its exact `ProjectFunctionContract`. A project
property, class method, static method, or class constant resolves only through
one exact `ProjectDescriptorBinding` plus one instruction-specific
`AttributeAccessCapability`. A property read/write/delete schedules its exact
`fget`/`fset`/`fdel`; a class method schedules its exact `__func__` with `cls`;
a static method schedules its exact `__func__` without a receiver; and a class
constant transfers only its declared atomic/identity contract. An external
native member requires one exact `ExternalTypeMemberBinding` and matching
attribute/call capability. Any custom or unmatched descriptor is
`UNAPPROVED_DESCRIPTOR`; no descriptor is authorized merely because its owner
class or result type is known.

A callable ordinary project class first requires one exact
`ProjectClassBinding`, then schedules its bound metaclass `__call__`, `__new__`, and
`__init__` with symbolic receiver records. It is not instantiated by the
audit. Before authorizing construction, its complete `BehaviorSlotManifest`
must match and the current roots require an absent non-trivial `__del__`; a
runtime-added finalizer or implicit slot drift fails before traversal. If and only if the class has an exact
`GeneratedProjectArtifactBinding`, the generated dataclass-init and slot
transfers or generated named-tuple `__new__`/tuplegetter transfers replace
opaque generated traversal. An enum class uses its literal member recipe and
separate `EnumType` type-member/protocol capabilities. A named-tuple instance is traversed by its literal
field/index recipe, never by the general tuple-subclass branch. Custom
`__new__`, `__init__`, `__post_init__`, methods, metaclass behavior, validators,
and factories remain ordinary audited call edges. Project exceptions and
runtime Protocol classes use their class binding's constructor/instance-check
semantic model. An external class used as a constructor or a `GenericAlias`
requires a callsite-specific `SAFE_FACTORY` capability. An external class used
only as an `isinstance`/`issubclass` operand instead requires
`SAFE_TYPE_OPERAND`, one `ExternalClassBinding`, and an exact `INSTANCE_CHECK`
protocol capability; neither route authorizes the other.

### 7.3 Native callables and module namespaces

Built-ins, extension functions, bound native methods, ufuncs, wrappers, and
C-state callables are accepted only through an exact callsite capability and
an independently frozen `OperationSemanticModel`.
Their type and empty object state carry no trust. Before a callsite can match,
the exact bootstrap identity, external-state policy, source/binary digest, and
state digest are revalidated. The analyzer derives receiver, normal,
exception, and callback effects from the semantic model and then compares them
with the capability's expected contracts; it never obtains actual semantics
from that expectation. A literal approved NumPy dispatcher or ufunc may
therefore pass; an equal-looking `frompyfunc` result, private provider, or
operation without an independent model cannot.

A module is never a value terminal. An exact `NAMESPACE_ROOT` may be used only
to resolve a statically named attribute at one project-owned instruction.
Returning, storing, subscripting, dynamically inspecting, or passing the bare
module is an `UNAPPROVED_NAMESPACE_ESCAPE` finding. Attribute resolution uses
the exact module dictionary captured by its namespace binding and does not
execute module `__getattr__`. Before and after traversal, the auditor rechecks
the exact module identity, origin/source-or-binary digest, and only the literal
attribute-to-identity mappings named by that root's namespace capabilities;
it neither scans nor implicitly permits other exports.

### 7.4 Containers and arrays

Only exact tuple, list, dict, set, frozenset, `MappingProxyType`, and `range`
objects are recognized as built-in containers. Outside the two literal
exceptions below, subclasses and custom mappings are unapproved carriers.
Every operation schedules its intrinsic-effect model: length, truth, hashing,
equality, ordering, iteration, and callbacks are never inferred safe from the
container type alone.
Tuple/list/dict/mapping-proxy traversal preserves exact
index or insertion order. An exact range uses its bounded start/stop/step
contract and is never expanded merely to prove size. Sets and frozensets may terminate only when every
member is an already validated atomic value; a behavior-bearing member makes
the container itself an unapproved carrier, avoiding unstable set paths.

The first exception is an exact named-tuple instance whose class has one
matching `GeneratedProjectArtifactBinding`. Traversal uses only its literal
field/index recipe and emits `NAMEDTUPLE_FIELD` edges; it never falls through
to generic tuple-subclass behavior. The second exception is an exact project
runtime value named by one `ProjectRuntimeValueBinding`, whether located at a
module global, closure cell, nested state field, or exact built-in container
entry. Every item access or method
call requires one instruction-specific `StateOperationCapability`. For
`WEAK_KEY_DICTIONARY`, `SET_ITEM` schedules the exact
`WeakKeyDictionary.__setitem__` project/stdlib implementation, weakref factory
and type-member operations, referent hash/equality, and any non-`None` callback using
`STATE_OPERATION`, `WEAKREF_REFERENT`, and `WEAKREF_CALLBACK` edges. An exact
weak reference may expose only its declared referent/callback labels. The
audit never executes these mutations and requires identical pre/post state
digests. Every other tuple subclass, custom mapping, weak container, or
weakref behavior remains an `UNAPPROVED_CARRIER` or
`STATE_OPERATION_MISMATCH`.

For an exact object-dtype ndarray, the walker reads exact `size` first. If the
size exceeds either remaining edge capacity or conservative remaining record
capacity, the audit fails at the array node before reading an element. It then
reads exact `dtype.itemsize` and `nbytes` through fixed audit-state primitives,
checks integer arithmetic and the content-byte limits, and only then permits a
content read. A
per-element iterator then schedules values without `tuple(array.flat)` or
another eager copy. Numeric ndarrays terminate only after exact dtype
inspection succeeds. A contracted numeric root array must be exact ndarray,
C-contiguous, and read-only; its `root-state` content digest uses the exact
`array-content` JSON recipe and bound `ndarray.tobytes` or `flat` protocol in
Section 5.2 after the size check. An object-array content preimage uses ordered
already-labelled identities/canonical atomics and never hashes raw pointer
bytes. Any shape/stride/flag/content change is
`STRUCTURED_STATE_DRIFT`.

## 8. Resource contract

This auxiliary proof has limits distinct from the parent Slice 4 full graph:

- graph depth: 32;
- project code objects: 224;
- project-class bindings: 256;
- behavior-slot manifests: 256;
- external-class bindings: 64;
- structural callsites: 1,400;
- unique object identities: 1,024;
- provider records including receiver/environment contexts: 3,072;
- total labelled policy-table records: 16,384;
- graph edges: 6,144;
- abstract container length: 256;
- abstract iterable cardinality: 256;
- simultaneously live symbolic iterator/view contracts: 256;
- project runtime-value bindings: 256;
- process-local identity sources: 64;
- process-local identity tokens: 64;
- located bound-callable handles: 128;
- runtime-state SCC bindings: 64;
- authorization-dependency nodes: 8,192;
- authorization-dependency edges: 16,384;
- runtime-state-reference edges: 2,048;
- state-field bindings: 768;
- generated stdlib callback bindings: 64;
- bound type-member bindings: 128;
- state-operation capabilities: 1,024;
- protocol-dispatch capabilities: 1,024;
- binary-operator capabilities: 256;
- audit-state-read primitives: 128;
- semantic guards: 4,096;
- semantic normal transfers: 2,048;
- semantic exception transfers: 2,048;
- operation semantic models: 2,048;
- intrinsic effect steps: 4,096;
- operation-outcome contracts: 2,048;
- exception contracts: 2,048;
- union alternatives: 32;
- numeric-array content bytes: 8,388,608;
- object-array canonical preimage bytes: 1,048,576; and
- loop/SCC fixpoint passes: 32 each.

The canonical `limits` record has exactly these keys:
`graph_depth,project_code_objects,project_classes,behavior_slot_manifests,
external_classes,structural_callsites,unique_object_identities,provider_records,
policy_table_records,graph_edges,abstract_container_length,
abstract_iterable_cardinality,symbolic_iterator_views,project_runtime_values,
process_local_identity_sources,process_local_identity_tokens,
located_bound_callable_handles,runtime_state_sccs,
authorization_dependency_nodes,authorization_dependency_edges,
runtime_state_reference_edges,state_fields,generated_stdlib_callbacks,
bound_type_members,state_operation_capabilities,protocol_capabilities,
binary_operator_capabilities,audit_state_reads,semantic_guards,
semantic_normal_transfers,semantic_exception_transfers,semantic_models,
intrinsic_effect_steps,operation_outcome_contracts,exception_contracts,
union_alternatives,numeric_array_content_bytes,object_array_canonical_bytes,
loop_fixpoint_passes,scc_fixpoint_passes`. No synonym or omitted byte limit is
valid.

The canonical report `counts` record has exactly these keys:
`code_objects,project_classes,behavior_slot_manifests,external_classes,
structural_callsites,unique_objects,provider_records,policy_table_records,
edges,project_runtime_values,process_local_identity_sources,
process_local_identity_tokens,located_bound_callable_handles,
runtime_state_sccs,authorization_dependency_nodes,
authorization_dependency_edges,runtime_state_reference_edges,state_fields,
generated_stdlib_callbacks,bound_type_members,state_operation_capabilities,
protocol_capabilities,binary_operator_capabilities,audit_state_reads,
semantic_guards,semantic_normal_transfers,semantic_exception_transfers,
semantic_models,intrinsic_effect_steps,operation_outcome_contracts,
exception_contracts,symbolic_iterator_views,max_graph_depth,
max_abstract_container_length,max_abstract_iterable_cardinality,
max_union_alternatives,max_numeric_array_content_bytes,
max_object_array_canonical_bytes,loop_fixpoint_iterations,
scc_fixpoint_iterations`. Counts are exact non-negative integers; each `max_*`
is the maximum actually observed, zero only when the dimension was never
entered. They are never inferred from limits or omitted from a zero-use report.
The name mapping is identity for same-named dimensions and is otherwise
exactly: `project_code_objects -> code_objects`, `unique_object_identities ->
unique_objects`, `graph_edges -> edges`, `graph_depth -> max_graph_depth`,
`abstract_container_length -> max_abstract_container_length`,
`abstract_iterable_cardinality -> max_abstract_iterable_cardinality`,
`union_alternatives -> max_union_alternatives`,
`numeric_array_content_bytes -> max_numeric_array_content_bytes`,
`object_array_canonical_bytes -> max_object_array_canonical_bytes`,
`loop_fixpoint_passes -> loop_fixpoint_iterations`, and
`scc_fixpoint_passes -> scc_fixpoint_iterations`. Limits without a direct
simultaneous cardinality count are still checked before use and reported by
their mapped maximum/iteration field; no implementation-defined alias exists.

The earlier 591/677-identity and 1,351/1,537-occurrence observation is
superseded for sizing by the current read-only characterization in Section
5.3: 726/808 unique identities and 1,631/1,811 occurrences. Neither legacy
count includes the newly specified project-class, runtime-value, state-field,
generated-callback, bound-member, process-local-source/token, runtime-SCC,
external-class/behavior-slot, iterator/view, protocol/operator,
audit-state-read, semantic-transfer/model/effect, or outcome records,
so neither is acceptance evidence for those dimensions. The higher auxiliary
bounds are a reviewed design correction, not a silent runtime raise, and do
not alter the parent Slice 4 limits. Before the first GREEN, a read-only
characterizer must report every limit above for both roots and commit those
counts beside the literal inventories. If either root exceeds 210 project code
objects, 240 project classes, 240 behavior-slot manifests, 56 external classes,
1,325 structural callsites, 900 unique identities, 2,800 provider
records, 15,000 labelled policy records, 5,600 edges, 220 project runtime-value
bindings, 56 process-local identity sources, 56 process-local tokens, 112
located bound-callable handles, 48 runtime-state SCCs, 7,500 authorization-
dependency nodes, 15,000 authorization-dependency edges, 1,800 runtime-state-
reference edges, 700 state-field
bindings, 48 generated stdlib callbacks, 112 bound type-members, 900 protocol
capabilities, 900 state-operation capabilities, 220 binary-operator
capabilities, 112 audit-state-read primitives, 3,600 semantic guards, 1,800
semantic normal transfers, 1,800 semantic exception transfers, 1,800 semantic models, 3,600
intrinsic effect steps, 1,800 operation-outcome contracts, 1,800 exception
contracts, 220 simultaneously live symbolic
iterator/view contracts, or any other abstract limit under the new normalized
policy, implementation stops and returns to design. Tests may lower a limit to
exercise failure but may not raise an acceptance limit.

Deterministic graph limits are checked before scheduling or materializing
candidate-sized state and report the exact frontier. Wall-clock time is a
separate external hang guard, not an in-graph finding or performance claim. A
fresh subprocess is used for exactly one root. The parent allows ten seconds
for import/bootstrap and requires the exact flushed frame
`PROVIDER_AUDIT_BOOTSTRAP_READY_V2 <bootstrap_sha256>`. Only after validating
that one frame does the parent write one canonical JSON challenge frame
`{"nonce":"<64 lowercase hex>"}` and close child stdin. The nonce is generated
from the parent OS CSPRNG and is not present in a file, environment variable,
argv, or policy before the ready frame. The child accepts exactly one valid
frame, inserts the nonce into the policy/report binding, and then starts the
audit. After sending the challenge, the parent allows thirty seconds for exactly
one report frame. On timeout it sends `TERM`, waits 0.5 seconds, then sends
`KILL`; timeout, missing/duplicate ready or report frame, unexpected pre-ready
output, trailing output, malformed challenge/report, nonce mismatch, non-zero
exit, or digest mismatch fails the test. Exact object identities are used only
inside the child and are never serialized as cross-process authority.
Interpreter, NumPy, platform, counts, and elapsed time are recorded. Before
the first GREEN, each real root is measured in at least twenty fresh cold-child
and twenty warm-cache child runs on the supported development environment; the
literal `PerformanceCharacterizationRecord` records all observations and requires its measured
P99 to remain at or below five seconds. Every timed audit child is a new
interpreter and uses `time.perf_counter_ns` around challenge-write through
validated report-frame receipt. A cold-child sample uses a unique empty audit-
cache directory and no prior in-process audit; a warm-cache series begins with
one excluded priming child on identical immutable bytes and then measures
twenty further fresh children using the same read-only application cache
directory and exact immutable source/policy/runtime bytes. OS page-cache state
is uncontrolled and is recorded as such; the specification does not claim it
is identical or observable.
Root order alternates deterministically. P99 is the nearest-rank estimator
`sorted(samples)[ceil(0.99*n)-1]`; with `n=20` it is the maximum. A value above
5.000000000 seconds is a stop condition; equality passes. No rerun may replace
an adverse characterization, although a diagnostic repeat is retained beside
it and cannot authorize GREEN. The fixed thirty-second deadline is a
functional hang guard with margin, not a performance result or cross-platform
SLA. If characterization violates the five-second design ceiling, the
implementation returns to design instead of raising the deadline.

`PerformanceCharacterizationRecord` is an evidence artifact, not policy
authority, and contains exactly `(schema,environment_fingerprint_digest,
source_bundle_digest,policy_digest,runtime_binary_anchor_digest,
application_cache_protocol_digest,os_page_cache_controlled:false,
strata,adverse_run_indices,p99_rule,threshold_ns,completed,digest)`. `strata`
contains exactly four ordered records `(root_label,cache_mode:COLD|WARM,
excluded_priming_elapsed_ns:optional int,samples_ns:exactly 20 positive ints,
nearest_rank_p99_ns:int,run_report_digests:exactly 20 digests)`. The record is
domain-hashed as `performance-characterization`; its digest and exact bytes are
committed beside the real-root inventory. Failed/timed-out/adverse runs remain
in their original ordinal as explicit failure records and in
`adverse_run_indices`; a later diagnostic repeat is appended to a separate
non-authorizing diagnostic log and cannot replace a stratum sample.

## 9. TDD and mutation corpus

Temporary mutation trees are evidence sources, not permanent dependencies.
Their minimal counterexamples are copied into deterministic repository tests.

The implementation file scope is frozen as:

- create `tests/_provider_audit_bootstrap_v2.py`;
- create `tests/_provider_callsite_provenance_v2.py`;
- rewrite `tests/_random_behavior_graph_v2.py`;
- create `tests/test_random_behavior_graph_v2.py`;
- modify `tests/test_exact_oracle_independence.py`;
- modify `tests/test_plan_migration_v1_to_v2.py`;
- modify `tests/test_calibration_v2_integrity.py` only for the existing bridge
  mutation boundary;
- modify `tests/test_randomness_v2_subprocess.py` for bootstrap-order and hang
  guard tests;
- create
  `docs/superpowers/plans/2026-08-29-task10-deny-by-default-provider-proof-implementation.md`;
- update the parent Task 10 plan link/authority without changing production
  code.

If this correction requires a production-file edit, implementation stops and
returns to design.

The RED corpus includes canonical-decoy builders; Python and native callable
forms; multi-hop receivers and descriptors; class factories and
`GenericAlias`; exact/custom containers and arrays; NumPy/stdlib/private random
providers; all dynamic resolver forms; forged metadata; safe-leaf argument
protocol attacks such as `len.__len__` and `np.asarray.__array__`; bootstrap
pollution; wrong-root and unused capabilities; generated dataclass init,
named-tuple `__new__`/tuplegetter, ordinary/exception/runtime-Protocol project
classes, project descriptor/class constant, native type-member, the full
closure-held bound method -> receiver -> runtime-key -> named-tuple field ->
weakref/callback/default locator chain, regex exact built-in-dict groupindex,
typing-form/enum complete call-state/runtime value, WeakKeyDictionary nested-
state/generated-callback remove transfer/state-operation, weakref callback,
iterator/view/generator consumer, `len` length, `any` truth, dict/set/weak-key
hash/equality, `np.asarray` coercion, sorted-key callback and key-result order,
`type | type` and `dict_keys | dict_keys` results, process-local identity-token
substitution/persistence, authorization-cycle substitution, each allowed
runtime-SCC shape plus extra-member/wrong-referent/wrong-callback variants,
external `Mapping` type-operand drift, and
slot-descriptor/finalizer drift including runtime `__del__` injection;
`object.__new__`/`object.__setattr__` forged exact
instances; changed root fields/nested arrays; missing project formal/normal/
exception outcomes and dishonest native outcome declarations; recursive SCCs
including safe/unsafe same-code closures
with different defaults/globals; every supported AST family; every
intentionally unsupported AST family; digest-cycle and field-discovery
attacks; complete-`LOAD_*` dispatcher rebinding; namespace extra-export drift;
stale/replayed nonce reports; AST/bytecode arbitrary-pair self-certification;
array state-read substitution; `size=1` large-itemsize/nbytes arrays; object-
array canonical-byte overflow; bounded/digested byte substitution;
pre-frozen attack-spec versus post-hoc witness/decoy mismatch; changed function
analysis without authority transfer; raw-resolved descriptor without binding
versus truly unresolved/dynamic attribute; and every graph/
abstract/iterator/class/runtime/capability/model/outcome resource bound.

`ProjectCodeAnalysisRecord` is test-only, non-authorizing, canonical, and has
exact fields `(label,mutated_source_digests,root_code_digests,
project_code_digests,project_source_index_digest,root_syntax_inventory_digest,
ast_site_manifest_digest,bytecode_site_manifest_digest,
site_pairing_manifest_digest,function_analysis_summary_digests)`. It may
recompute only the explicitly enumerated mutated **production project** source,
code, index, inventory, site, pairing, and function-analysis digests needed to
expose the mutated graph. It may not read, rebuild, replace, or recompute the
three audit-TCB implementation files, bootstrap/runtime-binary anchor, policy
schema, serializer, or expected KAT bytes. It contains no implementation digest,
permission, capability, authority semantic model, or expected outcome and is
domain-hashed as `project-code-analysis`.

`MutationRebaselineRecord` has exact fields `(label,baseline_source_digests,
mutated_source_digests,project_code_analysis_digest,unchanged_site_mappings,
authority_projection_digest_before,authority_projection_digest_after,
tcb_implementation_digest_before,tcb_implementation_digest_after,
bootstrap_digest_before,bootstrap_digest_after,policy_schema_digest_before,
policy_schema_digest_after)`.
Its one-to-one site mapping is allowed only for AST
subtrees whose canonical subtree digest, enclosing function digest, lexical
context digest, semantic role, and independently paired opcode group are all
unchanged, plus pre/post `authority_projection_digest`. Only those unchanged
sites retain their already frozen authority labels. A changed function body,
new helper, changed enclosing context, new or changed site receives no
capability, authority semantic model, or permission even though its
non-authorizing analysis record is recomputed. The authority projection keeps
all model kinds, external/intrinsic/generated dependencies, contracts,
permissions, capabilities, guards and transfers while removing only source/
code/position labels; it must be byte-identical. This resolves the distinction
between recomputable function analysis and non-rebaselined authorization. The
record is built outside the auditor and domain-hashed as `mutation-rebaseline`.
Construction requires equality of each before/after TCB, bootstrap, and policy-
schema digest pair before any mutation run. These fields are validations of
fixed evidence, not writable rebaseline outputs. A mismatch aborts the harness
before baseline/unsafe/safe execution.

Before the baseline, unsafe run, or paired safe run, the harness freezes one
`AttackRecipe` is frozen before any run and contains exactly
`(label,baseline_source_bundle_digest,unsafe_source_bundle_digest,
ordered_patch_operations,patch_digest,root_identity_label,
root_callsite_label,carrier_locator_or_identity_label,
provider_identity_label,fixture_digest)`. A patch operation fixes one
repository-relative production path, preimage SHA-256, exact byte range,
replacement bytes digest, and postimage SHA-256. `SafeControlRecipe` contains
exactly `(label,baseline_source_bundle_digest,safe_source_bundle_digest,
ordered_patch_operations,patch_digest,root_identity_label,
root_callsite_label,fixture_digest,derivation_rule)` and must be the unique
reviewed safe counterpart to the attack recipe; it cannot be selected after
observing the unsafe result.

Before the baseline, unsafe run, or paired safe run, the harness generates one
256-bit `trace_nonce` from the parent OS CSPRNG, keeps it outside policy/auditor
inputs, and freezes only its domain-separated `trace_nonce_commitment` in
`AttackSpec(label,baseline_source_bundle_digest,unsafe_source_bundle_digest,
safe_source_bundle_digest,root_identity_label,root_callsite_label,
carrier_locator_or_identity_label,provider_identity_label,
expected_complete_finding_key,attack_recipe_label,attack_recipe_digest,
safe_control_recipe_label,safe_control_recipe_digest,
trace_nonce_commitment)`. The audit challenge nonce is generated later and is
independent; the two nonces may not be equal or reused. Neither the auditor nor
any execution result can modify or regenerate the expected key, recipes, source
bundles, or commitment.

The provider-specific trap is created from exact frozen object references and
the hidden trace nonce; it accepts no carrier/provider/root labels from the
mutation or adapter. It is armed immediately before calling the exact frozen
root and disarmed immediately after that root returns or raises. It records
only events observed while the root invocation is active. `RootInvocationTrace`
contains exactly `(label,attack_spec_digest,trace_nonce,root_identity_label,
root_callsite_label,fixture_digest,root_enter_ns,root_exit_ns,
root_exit_kind,carrier_identity_label,provider_identity_label,
ordered_events,provider_call_count)`, where every event freezes enter/exit,
call ordinal, exact live `is` checks, and monotonic timestamps. It is invalid
unless `provider_call_count >= 1`, every event is nested inside the exact root
interval, and the root-to-carrier-to-provider call ordinal/path matches the
pre-frozen recipe.

`AttackWitness` contains exactly `label,attack_spec_digest,
observed_unsafe_source_bundle_digest,root_invocation_trace_digest,
trace_nonce,process_identifier_token,monotonic_start_ns,monotonic_end_ns,
identity_is_trace`. Verification first checks the revealed nonce against the
frozen commitment, then independently recomputes the trace digest and exact
root/carrier/provider identities. It is domain-hashed as `attack-witness` and
carries no expected finding or caller-supplied label. Directly calling a
provider outside the root interval, a zero-call carrier, a decoy provider,
different root/source/fixture, post-hoc recipe, mismatched commitment, or trace
adapter that imports auditor decisions cannot satisfy the witness.

Every passing test node whose name states the auxiliary absence claim must end
with or contain `for_frozen_contracts_v2`. An unqualified name such as
`entrypoint_has_no_reachable_random_behavior` is forbidden because it implies
coverage of arbitrary legal runtime inputs and future instances that this
proof does not establish.

Each attack uses a frozen clean baseline finding multiset and must satisfy all
four assertions:

1. the baseline finishes with `audit_pass=True`, `completed=True`, and an empty
   finding multiset for the same frozen contracts;
2. outside the audit, the unsafe carrier produces a valid `AttackWitness`
   whose revealed nonce matches the pre-run commitment and whose exact
   `RootInvocationTrace` proves at least one nested
   `root -> carrier -> provider` call for the pre-frozen unsafe source bundle,
   fixture, identities, and callsite;
3. the unsafe finding multiset is exactly the baseline multiset plus one
   expected `(category,path,frontier_edge,target)` stable key frozen in the
   `AttackSpec`, with no unrelated finding; and
4. the paired safe control finishes with a finding multiset exactly equal to
   the baseline multiset and the same completion state, and its bytes are
   reconstructed uniquely from the pre-frozen `SafeControlRecipe` and exact
   safe source-bundle digest. The expected
   `completed` value is asserted for all three runs.

When an attack changes project source, the isolated mutation harness applies
the complete `MutationRebaselineRecord`; merely substituting source or
implementation SHA fields is forbidden. The recomputed source index, root/code
digests, syntax inventory, and site manifests prevent drift findings from
masking the intended semantic category, while the unchanged authority
projection prevents the rebaseline from authorizing the mutation. The
audit-TCB implementation, bootstrap, and policy-schema before/after digests
must be byte-identical; no rebaseline field can change them. The
unfrozen mismatch remains a separate source-drift KAT. An unrelated opaque
finding, witness/finding mismatch, missing expected finding, additional
finding, changed authority projection, or non-PASS safe control cannot make a
mutation GREEN.

The implementation plan written after user approval must preserve this serial
evidence order:

1. commit specification-identity and bootstrap RED;
2. commit policy/schema and capability-validation GREEN;
3. commit carrier/callsite RED without weakening prior attacks;
4. commit traversal GREEN;
5. run same-byte Task 5 and repository verification; and
6. obtain same-hash specification, quality, and mutation reviews.

## 10. Verification commands and acceptance

The focused RED command is:

```bash
.venv/bin/python -m pytest \
  tests/test_random_behavior_graph_v2.py \
  tests/test_exact_oracle_independence.py \
  tests/test_plan_migration_v1_to_v2.py \
  tests/test_calibration_v2_integrity.py \
  tests/test_randomness_v2_subprocess.py -q
```

After focused GREEN, the existing Task 5 12-file command, full branch-coverage
suite, Ruff, strict mypy, recursive zero-global production check, build/package
checks due at the parent gate, and `git diff --check` run serially on unchanged
bytes.

The correction may enter a Slice 2 code commit only when:

1. every saved mutation produces its exact focused finding;
2. both real roots have zero findings with independent root-specific policies;
3. every safe capability is consumed once and no unused authority remains;
4. no decision invokes provider-controlled equality, hashing, ordering,
   unordered iteration, or `repr`;
5. every unknown callable, factory, descriptor, namespace, container, or
   native state fails closed;
6. the two literal root syntax inventories exactly cover the verified module
   AST/code graph and independently paired site manifests, every project
   class/formal/outcome, authorization DAG, and declared runtime SCC converges
   under the frozen table, and no
   reachable supported node falls through to a generic implementation rule;
7. ordinary/exception/runtime-Protocol project classes, generated-dataclass/
   slot, named-tuple/tuplegetter, project enum complete call-state,
   descriptor/class constant, external type-member/class type operand,
   complete behavior-slot/finalizer absence, regex groupindex dict and
   canonical ufunc `types` snapshot, project runtime-value and full derived
   locator/located-handle/process-local-token chain, state-field/runtime-SCC,
   generated-stdlib-callback transfer, bound-member, weakref, iterable/view/
   protocol and C-consumer intrinsic effects, both type-union and dict-keys-
   union operators, exact opcode/site grouping, bounded/digested byte reads,
   audit-state read, independently evaluated guard/normal/exception transfers, and
   root-structured-state bindings pass for the exact real fixtures while
   forged, mutated, same-valued replacement, wrong-receiver, wrong-operation,
   dishonest-outcome, and wrong-result cases fail for the intended category;
8. canonical serialization has committed exact-byte and digest known-answer
   vectors for every external state policy, the complete canonical policy and
   report key projections and normalized labelled tables, value-contract kind
   projections/intersections, array-content and byte-limit preimages,
   project/external-class/behavior-slot/runtime-locator/located-handle/token/
   value/state/SCC/generated-callback/bound-member/semantic-guard/normal/
   exception-transfer/model/intrinsic-effect/operator/audit-read records,
   both graph manifests and opcode profile, namespace
   mapping, runtime binary anchor, code-cycle failure, and challenge/replay
   protocol;
9. every mutation asserts the exact clean, unsafe, and paired-safe finding
   multisets, pre-frozen `AttackSpec`, independently observed `AttackWitness`,
   complete stable frontier key, and unchanged non-authorizing mutation
   authority projection; argument-protocol and
   bootstrap-pollution attacks fail for their single intended reason rather
   than an earlier drift category;
10. code/callsite/object/record/edge/depth/array/container/union/iterable/
   iterator/view/project/external-class/behavior-slot/runtime-value/locator/
   token/SCC/state-field/callback/bound-member/state-operation/protocol/operator/
   audit-read/semantic-guard/transfer/model/intrinsic-effect/outcome/exception/
   fixpoint/content-byte and external hang guards pass
   without raising an acceptance limit;
11. Task 5, full coverage of at least 95%, Ruff, strict mypy, recursive
   production zero-global checks, and diff hygiene pass on the same bytes;
12. the new implementation plan lists every changed path and exact command;
   and
13. independent specification, code-quality, and mutation reviews each report
    `0 BLOCKER / 0 MAJOR / 0 MINOR` on the exact candidate hashes.

Passing this gate closes only the Slice 2 auxiliary proof and random-capsule
commit candidate. It does not close Task 10, Slice 4, M0-M2, M6, UI, release,
external validation, manuscript, or SoftwareX submission readiness.

## 11. Plan authority and stop conditions
The existing Task 10 plan remains authoritative for completed Slice 1 and the
production random-capsule requirements. Its current Task 5 helper-proof and
commit steps are stale and must not be executed after this revision. After the
user approves this written specification, the `writing-plans` workflow must
create a dedicated implementation plan and then link it from the parent plan
before any implementation begins.

Implementation stops and returns to design if:

- the external bootstrap receives or discovers the audited root;
- a permission is generated from candidate globals or module exports;
- a state field, source node, generated artifact, project formal/outcome,
  project/external class, behavior-slot manifest, iterable/protocol/operator
  contract, semantic guard/transfer/intrinsic model, runtime-value/locator/
  token/SCC/handle binding, or
  namespace mapping is added by runtime discovery rather than literal review;
- a safe rule depends on a provider-controlled string or broad type category;
- one capability authorizes multiple roots or unvalidated argument domains;
- an unknown native/stateful object is accepted because its state appears
  empty;
- a module is accepted as a bare value terminal;
- candidate-sized state is materialized before its bound check;
- ndarray content is read before checked `size/itemsize/nbytes` and canonical-
  byte limits;
- an external/native outcome is taken from its expected capability rather than
  independently derived;
- a source `id` call or runtime container lookup uses a serialized/recomputed
  integer instead of the same child-local identity token;
- the authorization dependency graph has a cycle, a runtime reference cycle
  lacks one exact allowed SCC, or one parent/child record owns the other in
  both directions;
- an external class/type operand lacks the closed type-check-only binding, a
  constructible project class has a non-trivial/changed finalizer, or a ufunc
  canonical container snapshot changes;
- a `dict_keys | dict_keys` site lacks its exact keys-view/effect/result model,
  or an audit byte result cannot be represented within the separate byte limit;
- an AST/bytecode site is paired before both input manifests are frozen or by
  a non-bijective/ambiguous rule;
- a mutation passes for an unrelated finding, a post-hoc/mismatched attack
  spec or witness, incomplete code-analysis/rebaseline separation, or changed
  authority projection;
- the real-root syntax inventory has an unsupported frontier, unmapped source
  code, or non-convergent SCC;
- the new roots exceed the pre-GREEN characterization ceiling; or
- the repair weakens the parent design, test name, or claim ceiling.
