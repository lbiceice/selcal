"""Portable, fail-closed helpers for the verifier structure gate v1."""

from __future__ import annotations

import ast
import dis
import hashlib
import json
from collections import deque
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from pathlib import Path
from types import FunctionType, ModuleType
from typing import NamedTuple

IDENTITY_KEYS = (
    "byteNormalization",
    "decode",
    "digest",
    "segment",
    "segmentTransforms",
    "selector",
)
FIXTURE_KEYS = (
    "builderNeutralFrontier",
    "builderNeutralFrontierCount",
    "frontier",
    "graphBudgets",
    "identityAlgorithm",
    "legacyDeclarations",
    "schema",
    "structureGatePythonFiles",
    "version",
)
R3_KEYS = (
    "artifacts",
    "claimCeiling",
    "commands",
    "date",
    "environmentCells",
    "findingToFix",
    "inputs",
    "priorReceipts",
    "regressions",
    "repository",
    "schema",
    "status",
    "triState",
    "version",
)
R3_INPUT_PATHS = (
    "docs/status/evidence/verifier_structure_oracle_enumerator_v1.py",
    "docs/superpowers/plans/2026-09-01-verifier-complexity-slice-v1-implementation.md",
    "docs/superpowers/specs/2026-09-01-verifier-complexity-slice-v1-design.md",
    "tests/_verifier_structure_gate_v1.py",
    "tests/fixtures/verifier_structure_gate_v1.json",
    "tests/test_verifier_complexity_slice_v1.py",
    "tests/test_verifier_integration_v2.py",
)
R3_COMMAND_RETURN_CODES = (
    ("prefixedPy314", 1),
    ("prefixedPy311", 1),
    ("oracle", 0),
    ("py311Full", 1),
    ("py311Portable", 0),
    ("py311Environment", 0),
    ("py311Ruff", 0),
    ("py312Full", 1),
    ("py312Portable", 0),
    ("py312Environment", 0),
    ("py312Ruff", 0),
    ("py313Full", 1),
    ("py313Portable", 0),
    ("py313Environment", 0),
    ("py313Ruff", 0),
    ("py314Full", 1),
    ("py314Portable", 0),
    ("py314Environment", 0),
    ("py314Ruff", 0),
    ("integration102", 0),
    ("regression588", 0),
    ("related690", 0),
    ("ordinaryRuff", 0),
    ("selfC901", 0),
    ("strictMypy", 0),
    ("diffCheck", 0),
    ("gitStatus", 0),
    ("inputHashes", 0),
)
R3_JUNIT_COMMANDS = (
    "prefixedPy314",
    "prefixedPy311",
    "py311Full",
    "py311Portable",
    "py312Full",
    "py312Portable",
    "py313Full",
    "py313Portable",
    "py314Full",
    "py314Portable",
)
R3_FINDING_NODE_IDS = (
    "test_portable_frontier_identity_does_not_depend_on_co_code",
    "test_portable_legacy_identity_does_not_depend_on_ast_dump",
    "test_structure_gate_implementation_has_zero_self_c901_findings",
    "test_runtime_graph_rejects_direct_custom_callable_object",
    "test_static_gate_rejects_direct_dunder_import",
    "test_static_gate_rejects_nested_writable_singleton",
    "test_runtime_graph_terminates_pure_self_cycle",
    "test_builder_rejects_unknown_reachable_project_helper",
)
R3_ARTIFACT_PATHS = (
    "docs/status/evidence/verifier_structure_oracle_enumerator_v1.py",
    "tests/_verifier_structure_gate_v1.py",
    "tests/fixtures/verifier_structure_gate_v1.json",
    "tests/test_verifier_complexity_slice_v1.py",
)


@dataclass(frozen=True)
class FunctionShape:
    qualname: str
    line: int
    end_line: int
    parameters: tuple[str, ...]
    variadic: tuple[str, ...]

    @property
    def span(self) -> int:
        return self.end_line - self.line + 1


@dataclass(frozen=True)
class GraphBudgets:
    nodes: int
    edges: int
    depth: int


@dataclass(frozen=True)
class GraphPolicy:
    repository_root: Path
    project_manifest: tuple[Mapping[str, object], ...] = ()
    frontier_manifest: tuple[Mapping[str, object], ...] = ()
    terminal_identities: frozenset[int] = frozenset()
    approved_record_types: tuple[type[object], ...] = ()
    approved_schema_types: tuple[type[object], ...] = ()
    stop_identities: frozenset[int] = frozenset()
    root_project_identities: frozenset[int] = frozenset()


@dataclass(frozen=True)
class GraphResult:
    nodes: int
    edges: int
    depth: int
    project_rows: tuple[dict[str, object], ...]


class _QueueItem(NamedTuple):
    value: object
    depth: int


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def normalized_source(path: Path) -> tuple[bytes, str]:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return raw, raw.decode("utf-8", errors="strict")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _child_qualname(parent: str, child: ast.AST, name: str) -> str:
    if not parent:
        return name
    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return f"{parent}.{name}"
    raise AssertionError("unreachable lexical scope")


def lexical_declarations(tree: ast.Module) -> tuple[tuple[str, ast.AST], ...]:
    found: list[tuple[str, ast.AST]] = []

    def visit(body: Sequence[ast.stmt], parent: str, function_scope: bool) -> None:
        for node in body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            prefix = f"{parent}.<locals>" if function_scope and parent else parent
            qualname = _child_qualname(prefix, node, node.name)
            found.append((qualname, node))
            visit(
                node.body,
                qualname,
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)),
            )

    visit(tree.body, "", False)
    return tuple(found)


def _top_level_target(node: ast.AST) -> str | None:
    if isinstance(node, ast.Assign) and len(node.targets) == 1:
        return node.targets[0].id if isinstance(node.targets[0], ast.Name) else None
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return node.target.id
    return getattr(node, "name", None)


def _complete_position(node: ast.AST) -> bool:
    return all(
        getattr(node, name, None) is not None
        for name in ("lineno", "col_offset", "end_lineno", "end_col_offset")
    )


def source_segment_digest(
    path: Path,
    *,
    kind: str,
    qualname_or_target: str,
    first_line: int,
    legacy: bool = False,
) -> str:
    _raw, text = normalized_source(path)
    tree = ast.parse(text, filename=str(path))
    node_type = getattr(ast, kind, None)
    if not isinstance(node_type, type) or not issubclass(node_type, ast.AST):
        raise AssertionError(f"SOURCE_IDENTITY_UNKNOWN_KIND:{kind}")
    if legacy:
        candidates = _legacy_candidates(tree, node_type, qualname_or_target, first_line)
    else:
        candidates = _frontier_candidates(tree, node_type, qualname_or_target, first_line)
    if len(candidates) != 1:
        raise AssertionError(f"SOURCE_IDENTITY_MATCH_COUNT:{len(candidates)}")
    node = candidates[0]
    if not _complete_position(node):
        raise AssertionError("SOURCE_IDENTITY_INCOMPLETE_POSITION")
    segment = ast.get_source_segment(text, node, padded=False)
    if segment is None:
        raise AssertionError("SOURCE_IDENTITY_NONE_SEGMENT")
    return hashlib.sha256(segment.encode("utf-8", errors="strict")).hexdigest()


def _frontier_candidates(
    tree: ast.Module, node_type: type[ast.AST], qualname: str, first_line: int
) -> tuple[ast.AST, ...]:
    allowed = (ast.FunctionDef, ast.AsyncFunctionDef)
    if node_type not in allowed:
        return ()
    return tuple(
        node
        for candidate, node in lexical_declarations(tree)
        if type(node) is node_type and candidate == qualname and node.lineno == first_line
    )


def _legacy_candidates(
    tree: ast.Module, node_type: type[ast.AST], target: str, first_line: int
) -> tuple[ast.AST, ...]:
    return tuple(
        node
        for node in tree.body
        if type(node) is node_type
        and _top_level_target(node) == target
        and node.lineno == first_line
    )


def source_identity_row(function: FunctionType, repository_root: Path) -> dict[str, object]:
    path = Path(function.__code__.co_filename).resolve()
    relative = path.relative_to(repository_root).as_posix()
    lexical_qualname = lexical_qualname_at_line(path, function.__code__.co_firstlineno)
    return {
        "module": function.__module__,
        "qualname": lexical_qualname,
        "sourcePath": relative,
        "sourceSha256": sha256_file(path),
        "firstLine": function.__code__.co_firstlineno,
        "sourceSegmentSha256": source_segment_digest(
            path,
            kind="FunctionDef",
            qualname_or_target=lexical_qualname,
            first_line=function.__code__.co_firstlineno,
        ),
    }


def lexical_qualname_at_line(path: Path, first_line: int) -> str:
    _raw, text = normalized_source(path)
    matches = tuple(
        qualname
        for qualname, node in lexical_declarations(ast.parse(text, filename=str(path)))
        if type(node) in (ast.FunctionDef, ast.AsyncFunctionDef) and node.lineno == first_line
    )
    if len(matches) != 1:
        raise AssertionError(f"SOURCE_IDENTITY_LINE_MATCH_COUNT:{len(matches)}")
    return matches[0]


def _canonical_scalar(value: object) -> tuple[str, str, bytes] | None:
    value_type = type(value)
    prefix = (value_type.__module__, value_type.__qualname__)
    if value is None:
        return (*prefix, b"none")
    if value_type is bool:
        return (*prefix, b"true" if value else b"false")
    if value_type is int:
        return (*prefix, str(value).encode("ascii"))
    if value_type is float:
        return (*prefix, value.hex().encode("ascii"))
    if value_type is str:
        return (*prefix, value.encode("utf-8"))
    if value_type is bytes:
        return (*prefix, value)
    if isinstance(value, Enum):
        marker = f"{value_type.__module__}:{value_type.__qualname__}:{value.name}"
        return (*prefix, marker.encode("utf-8"))
    return None


def _loaded_global_values(function: FunctionType) -> tuple[object, ...]:
    names = sorted(
        {
            instruction.argval
            for instruction in dis.get_instructions(function)
            if instruction.opname in {"LOAD_GLOBAL", "LOAD_NAME"}
            and isinstance(instruction.argval, str)
        }
    )
    return tuple(function.__globals__[name] for name in names if name in function.__globals__)


def _function_children(function: FunctionType) -> tuple[object, ...]:
    values: list[object] = list(function.__defaults__ or ())
    values.extend(value for _key, value in sorted((function.__kwdefaults__ or {}).items()))
    closure = function.__closure__ or ()
    for _name, cell in zip(function.__code__.co_freevars, closure, strict=True):
        try:
            values.append(cell.cell_contents)
        except ValueError:
            continue
    values.extend(_loaded_global_values(function))
    return tuple(values)


def _record_children(value: object, policy: GraphPolicy) -> tuple[object, ...] | None:
    if type(value) not in policy.approved_record_types:
        return None
    marker = getattr(type(value), "_fields", None)
    if type(marker) is tuple:
        return tuple(getattr(value, name) for name in marker)
    if is_dataclass(value):
        return tuple(getattr(value, field.name) for field in fields(value))
    raise AssertionError("APPROVED_RECORD_HAS_NO_DECLARED_FIELDS")


def _sortable_marker(row: tuple[object, ...]) -> object:
    return row[0]


def _builder_row_key(row: Mapping[str, object]) -> tuple[object, ...]:
    return row["module"], row["qualname"], row["sourcePath"], row["firstLine"]


def _mapping_children(value: Mapping[object, object]) -> tuple[object, ...]:
    sortable: list[tuple[tuple[str, str, bytes], object, object]] = []
    for key, item in value.items():
        marker = _canonical_scalar(key)
        if marker is None:
            raise AssertionError("GRAPH_NONCANONICAL_MAPPING_KEY_V1")
        sortable.append((marker, key, item))
    children: list[object] = []
    for _marker, key, item in sorted(sortable, key=_sortable_marker):
        children.extend((key, item))
    return tuple(children)


def _set_children(value: set[object] | frozenset[object]) -> tuple[object, ...]:
    sortable: list[tuple[tuple[str, str, bytes], object]] = []
    for item in value:
        marker = _canonical_scalar(item)
        if marker is None:
            raise AssertionError("GRAPH_NONCANONICAL_SET_ELEMENT_V1")
        sortable.append((marker, item))
    return tuple(item for _marker, item in sorted(sortable, key=_sortable_marker))


def _manifest_match(row: Mapping[str, object], expected: Mapping[str, object]) -> bool:
    keys = (
        "module",
        "qualname",
        "sourcePath",
        "sourceSha256",
        "firstLine",
        "sourceSegmentSha256",
    )
    return all(row.get(key) == expected.get(key) for key in keys)


def _adjudicate_function(function: FunctionType, policy: GraphPolicy) -> dict[str, object] | None:
    path = Path(function.__code__.co_filename).resolve()
    try:
        path.relative_to(policy.repository_root / "src/selcal")
    except ValueError:
        return None
    if id(function) in policy.root_project_identities:
        return None
    row = source_identity_row(function, policy.repository_root)
    manifests = (*policy.project_manifest, *policy.frontier_manifest)
    if not any(_manifest_match(row, expected) for expected in manifests):
        label = f"{function.__module__}.{function.__qualname__}"
        raise AssertionError(f"UNKNOWN_PROJECT_FUNCTION_V1:{label}")
    return row


def _function_or_record_children(value: object, policy: GraphPolicy) -> tuple[object, ...] | None:
    if type(value) is FunctionType:
        row = _adjudicate_function(value, policy)
        return () if row is not None else _function_children(value)
    if type(value) is type and any(value is approved for approved in policy.approved_schema_types):
        return ()
    return _record_children(value, policy)


def _container_children(value: object) -> tuple[object, ...] | None:
    if isinstance(value, Mapping):
        return _mapping_children(value)
    if type(value) in (tuple, list):
        return tuple(value)
    if type(value) in (set, frozenset):
        return _set_children(value)
    return None


def _children(value: object, policy: GraphPolicy) -> tuple[object, ...]:
    if id(value) in policy.terminal_identities or id(value) in policy.stop_identities:
        return ()
    if _canonical_scalar(value) is not None:
        return ()
    projected = _function_or_record_children(value, policy)
    if projected is not None:
        return projected
    projected = _container_children(value)
    if projected is not None:
        return projected
    if isinstance(value, ModuleType):
        raise AssertionError("GRAPH_FORBIDDEN_MODULE_V1")
    if callable(value):
        raise AssertionError("GRAPH_FORBIDDEN_CALLABLE_V1")
    raise AssertionError(
        f"GRAPH_FORBIDDEN_OBJECT_V1:{type(value).__module__}.{type(value).__qualname__}"
    )


def _budget_error(metric: str, limit: int, observed: int) -> AssertionError:
    return AssertionError(
        f"GRAPH_BUDGET_EXCEEDED_V1 metric={metric} limit={limit} observed_at_least={observed}"
    )


def _seed_roots(
    roots: Iterable[object], budgets: GraphBudgets
) -> tuple[deque[_QueueItem], set[int]]:
    queue: deque[_QueueItem] = deque()
    ledger: set[int] = set()
    for root in roots:
        if id(root) in ledger:
            continue
        prospective = len(ledger) + 1
        if prospective > budgets.nodes:
            raise _budget_error("nodes", budgets.nodes, prospective)
        ledger.add(id(root))
        queue.append(_QueueItem(root, 0))
    return queue, ledger


def walk_identity_graph(
    roots: Iterable[object], budgets: GraphBudgets, policy: GraphPolicy
) -> GraphResult:
    queue, ledger = _seed_roots(roots, budgets)
    edges = 0
    max_depth = 0
    rows: dict[tuple[object, ...], dict[str, object]] = {}
    while queue:
        value, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        if type(value) is FunctionType:
            row = _adjudicate_function(value, policy)
            if row is not None:
                key = tuple(row[key] for key in sorted(row))
                rows[key] = row
        for child in _children(value, policy):
            edges = _enqueue_child(child, depth, edges, queue, ledger, budgets)
    ordered = tuple(sorted(rows.values(), key=_builder_row_key))
    return GraphResult(len(ledger), edges, max_depth, ordered)


def _enqueue_child(
    child: object,
    parent_depth: int,
    edges: int,
    queue: deque[_QueueItem],
    ledger: set[int],
    budgets: GraphBudgets,
) -> int:
    prospective_edges = edges + 1
    if prospective_edges > budgets.edges:
        raise _budget_error("edges", budgets.edges, prospective_edges)
    if id(child) in ledger:
        return prospective_edges
    child_depth = parent_depth + 1
    if child_depth > budgets.depth:
        raise _budget_error("depth", budgets.depth, child_depth)
    prospective_nodes = len(ledger) + 1
    if prospective_nodes > budgets.nodes:
        raise _budget_error("nodes", budgets.nodes, prospective_nodes)
    ledger.add(id(child))
    queue.append(_QueueItem(child, child_depth))
    return prospective_edges


def ceil_pow2(value: int) -> int:
    if value <= 1:
        return 1
    return 1 << (value - 1).bit_length()


def freeze_budgets(observed: Mapping[str, int]) -> dict[str, int]:
    caps = {"nodes": 4096, "edges": 16384, "depth": 128}
    frozen = {key: ceil_pow2(4 * observed[key]) for key in ("nodes", "edges", "depth")}
    if any(frozen[key] > caps[key] for key in caps):
        raise AssertionError("STRUCTURE_GATE_BUDGET_DESIGN_HOLD")
    return frozen


def function_inventory(source: str) -> tuple[FunctionShape, ...]:
    tree = ast.parse(source)
    found: list[FunctionShape] = []
    for qualname, node in lexical_declarations(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        parameters = tuple(
            item.arg for item in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)
        )
        variadic = tuple(
            item
            for item in (
                node.args.vararg.arg if node.args.vararg else "",
                node.args.kwarg.arg if node.args.kwarg else "",
            )
            if item
        )
        found.append(
            FunctionShape(
                qualname, node.lineno, node.end_lineno or node.lineno, parameters, variadic
            )
        )
    return tuple(found)


def _module_assignment_value(node: ast.AST) -> ast.AST | None:
    if isinstance(node, ast.Assign):
        return node.value
    if isinstance(node, ast.AnnAssign):
        return node.value
    return None


def _contains_writable(node: ast.AST) -> bool:
    return any(
        isinstance(child, (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp))
        for child in ast.walk(node)
    )


def _shape_violations(source: str) -> tuple[str, ...]:
    violations: list[str] = []
    for shape in function_inventory(source):
        if shape.span > 120:
            violations.append(f"oversized-function:{shape.qualname}:{shape.span}")
        if len(shape.parameters) > 8:
            violations.append(f"too-many-parameters:{shape.qualname}:{len(shape.parameters)}")
        if shape.variadic:
            violations.append(f"variadic-parameters:{shape.qualname}")
    return tuple(violations)


def _syntax_violations(tree: ast.Module) -> tuple[str, ...]:
    violations: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Lambda):
            violations.append(f"lambda:{node.lineno}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"__import__", "eval", "exec", "compile"}:
                violations.append(f"dynamic-call:{node.func.id}:{node.lineno}")
    return tuple(violations)


def _runtime_scope_violations(tree: ast.Module) -> tuple[str, ...]:
    violations: list[str] = []
    for _qualname, declaration in lexical_declarations(tree):
        if not isinstance(declaration, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for node in ast.walk(declaration):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                violations.append(f"runtime-import:{node.lineno}")
            if isinstance(node, ast.Global):
                violations.extend(
                    f"behavior-global:{name}:{node.lineno}" for name in node.names
                )
    return tuple(violations)


def _singleton_violations(tree: ast.Module) -> tuple[str, ...]:
    violations: list[str] = []
    for statement in tree.body:
        value = _module_assignment_value(statement)
        if value is not None and _contains_writable(value):
            violations.append(f"nested-writable-singleton:{statement.lineno}")
    return tuple(violations)


def static_source_violations(source: str) -> tuple[str, ...]:
    tree = ast.parse(source)
    violations = (
        *_shape_violations(source),
        *_syntax_violations(tree),
        *_runtime_scope_violations(tree),
        *_singleton_violations(tree),
    )
    return tuple(sorted(set(violations)))


def gate_implementation_closure(entry: Path, tests_root: Path) -> tuple[Path, ...]:
    queue = deque([entry.resolve()])
    seen: set[Path] = set()
    while queue:
        path = queue.popleft()
        if path in seen:
            continue
        seen.add(path)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        _reject_dynamic_test_loads(tree)
        queue.extend(_local_imports(tree, tests_root))
    return tuple(sorted(seen))


def _reject_dynamic_test_loads(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        rendered = ast.unparse(node.func)
        if rendered in {"__import__", "importlib.import_module", "spec_from_file_location"}:
            raise AssertionError(f"DYNAMIC_TEST_LOCAL_LOAD_V1:{rendered}")


def _local_imports(tree: ast.Module, tests_root: Path) -> tuple[Path, ...]:
    found: list[Path] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.level:
            raise AssertionError("RELATIVE_TEST_IMPORT_AMBIGUITY_V1")
        names = _import_names(node)
        for name in names:
            candidate = (tests_root / name.replace(".", "/")).with_suffix(".py")
            if candidate.is_file():
                found.append(candidate.resolve())
    return tuple(found)


def _import_names(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)
    if isinstance(node, ast.ImportFrom) and node.module:
        return (node.module,)
    return ()


def _assert_exact_keys(value: Mapping[str, object], expected: tuple[str, ...], label: str) -> None:
    if tuple(sorted(value)) != expected:
        raise AssertionError(f"{label}_KEYS_V1")


def _frontier_row_key(row: Mapping[str, object]) -> object:
    return row["role"]


def _legacy_row_key(row: Mapping[str, object]) -> tuple[object, ...]:
    return row["kind"], row["name"], row["sourcePath"], row["firstLine"]


def validate_fixture_bytes(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8", errors="strict"))
    if canonical_json_bytes(value) != raw:
        raise AssertionError("FIXTURE_NOT_CANONICAL_JSON_V1")
    if not isinstance(value, dict):
        raise AssertionError("FIXTURE_NOT_OBJECT_V1")
    _assert_exact_keys(value, FIXTURE_KEYS, "FIXTURE")
    _validate_fixture_header(value)
    _validate_fixture_rows(value)
    _validate_fixture_budgets(value)
    return value


def _validate_fixture_header(value: Mapping[str, object]) -> None:
    if value["schema"] != "selcal.verifier-structure-gate-fixture.v1" or value["version"] != 1:
        raise AssertionError("FIXTURE_IDENTITY_V1")
    expected_files = [
        "tests/_verifier_structure_gate_v1.py",
        "tests/test_verifier_complexity_slice_v1.py",
    ]
    if value["structureGatePythonFiles"] != expected_files:
        raise AssertionError("FIXTURE_GATE_FILES_V1")
    algorithm = value["identityAlgorithm"]
    if not isinstance(algorithm, dict):
        raise AssertionError("FIXTURE_IDENTITY_ALGORITHM_V1")
    _assert_exact_keys(algorithm, IDENTITY_KEYS, "FIXTURE_IDENTITY_ALGORITHM")
    expected_algorithm = {
        "byteNormalization": "CRLF_CR_TO_LF_ONLY",
        "decode": "UTF8_STRICT",
        "digest": "SHA256_UTF8",
        "segment": "AST_GET_SOURCE_SEGMENT_PADDED_FALSE",
        "segmentTransforms": [],
        "selector": "AST_KIND_QUALNAME_OR_TOP_LEVEL_TARGET_AND_FIRST_LINE_EXACTLY_ONE",
    }
    if algorithm != expected_algorithm:
        raise AssertionError("FIXTURE_IDENTITY_ALGORITHM_VALUE_V1")


def _validate_fixture_rows(value: Mapping[str, object]) -> None:
    frontier = value["frontier"]
    legacy = value["legacyDeclarations"]
    builder = value["builderNeutralFrontier"]
    if not all(isinstance(rows, list) for rows in (frontier, legacy, builder)):
        raise AssertionError("FIXTURE_ROWS_NOT_LIST_V1")
    if len(frontier) != 5 or value["builderNeutralFrontierCount"] != len(builder):
        raise AssertionError("FIXTURE_ROW_COUNT_V1")
    _validate_fixture_row_keys(frontier, legacy, builder)
    if frontier != sorted(frontier, key=_frontier_row_key):
        raise AssertionError("FIXTURE_FRONTIER_ORDER_V1")
    if legacy != sorted(legacy, key=_legacy_row_key) or builder != sorted(
        builder, key=_builder_row_key
    ):
        raise AssertionError("FIXTURE_ROW_ORDER_V1")
    if len({canonical_json_bytes(row) for row in builder}) != len(builder):
        raise AssertionError("FIXTURE_DUPLICATE_BUILDER_ROW_V1")
    if len({canonical_json_bytes(row) for row in frontier}) != len(frontier):
        raise AssertionError("FIXTURE_DUPLICATE_FRONTIER_ROW_V1")
    if len({canonical_json_bytes(row) for row in legacy}) != len(legacy):
        raise AssertionError("FIXTURE_DUPLICATE_LEGACY_ROW_V1")


def _validate_fixture_row_keys(
    frontier: list[object], legacy: list[object], builder: list[object]
) -> None:
    frontier_keys = (
        "firstLine",
        "module",
        "qualname",
        "role",
        "sourcePath",
        "sourceSegmentSha256",
        "sourceSha256",
    )
    legacy_keys = (
        "firstLine",
        "kind",
        "name",
        "sourcePath",
        "sourceSegmentSha256",
        "sourceSha256",
    )
    builder_keys = (
        "firstLine",
        "module",
        "qualname",
        "sourcePath",
        "sourceSegmentSha256",
        "sourceSha256",
    )
    _validate_fixture_row_group(frontier, frontier_keys, "FIXTURE_FRONTIER_ROW")
    _validate_fixture_row_group(legacy, legacy_keys, "FIXTURE_LEGACY_ROW")
    _validate_fixture_row_group(builder, builder_keys, "FIXTURE_BUILDER_ROW")


def _validate_fixture_row_group(
    rows: list[object], expected_keys: tuple[str, ...], label: str
) -> None:
    for row in rows:
        if not isinstance(row, dict) or tuple(sorted(row)) != expected_keys:
            raise AssertionError(f"{label}_KEYS_V1")
        if type(row["firstLine"]) is not int or row["firstLine"] < 1:
            raise AssertionError(f"{label}_FIRST_LINE_V1")
        if not _is_sha256(row["sourceSha256"]) or not _is_sha256(row["sourceSegmentSha256"]):
            raise AssertionError(f"{label}_SHA256_V1")
        for key in expected_keys:
            if key not in {"firstLine", "sourceSha256", "sourceSegmentSha256"}:
                if type(row[key]) is not str or not row[key]:
                    raise AssertionError(f"{label}_VALUE_V1")


def _validate_fixture_budgets(value: Mapping[str, object]) -> None:
    budgets = value["graphBudgets"]
    if not isinstance(budgets, dict):
        raise AssertionError("FIXTURE_BUDGETS_V1")
    expected = ("formula", "frozen", "hardCaps", "metricPriority", "observed")
    _assert_exact_keys(budgets, expected, "FIXTURE_BUDGETS")
    observed = budgets["observed"]
    frozen = budgets["frozen"]
    hard_caps = budgets["hardCaps"]
    if not all(isinstance(item, dict) for item in (observed, frozen, hard_caps)):
        raise AssertionError("FIXTURE_BUDGET_METRICS_V1")
    metric_keys = ("depth", "edges", "nodes")
    if any(tuple(sorted(item)) != metric_keys for item in (observed, frozen, hard_caps)):
        raise AssertionError("FIXTURE_BUDGET_METRIC_KEYS_V1")
    if any(
        type(item[key]) is not int or item[key] < 0
        for item in (observed, frozen)
        for key in metric_keys
    ):
        raise AssertionError("FIXTURE_BUDGET_METRICS_V1")
    if hard_caps != {"nodes": 4096, "edges": 16384, "depth": 128}:
        raise AssertionError("FIXTURE_BUDGET_HARD_CAPS_V1")
    if budgets["formula"] != "CEIL_POW2_FOUR_TIMES_OBSERVED_NO_TRUNCATION":
        raise AssertionError("FIXTURE_BUDGET_FORMULA_LABEL_V1")
    if budgets["metricPriority"] != ["edges", "depth", "nodes"]:
        raise AssertionError("FIXTURE_BUDGET_PRIORITY_V1")
    if frozen != freeze_budgets(observed):
        raise AssertionError("FIXTURE_BUDGET_FORMULA_V1")


def validate_durable_r3_receipt_v1(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8", errors="strict"))
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise AssertionError("R3_NOT_CANONICAL_V1")
    _assert_exact_keys(value, R3_KEYS, "R3")
    _validate_r3_identity(path, value)
    _validate_r3_repository(value)
    _validate_r3_hash_mapping(value["inputs"], R3_INPUT_PATHS, "R3_INPUT")
    _validate_r3_environment(value)
    _validate_r3_tristate(value)
    _validate_r3_commands(value)
    _validate_r3_prior(value)
    _validate_r3_findings(value)
    _validate_r3_regressions(value)
    _validate_r3_hash_mapping(value["artifacts"], R3_ARTIFACT_PATHS, "R3_ARTIFACT")
    return value


def _validate_r3_identity(path: Path, value: Mapping[str, object]) -> None:
    if path.as_posix() != "docs/status/verifier_structure_red_r3_20260902.json":
        raise AssertionError("R3_NON_DURABLE_PATH_V1")
    if value["schema"] != "selcal.verifier-structure-red-receipt.v3" or value["version"] != 3:
        raise AssertionError("R3_IDENTITY_V1")
    if value["status"] != "EXPECTED_RED_CURRENT_PRODUCTION_UNMODIFIED":
        raise AssertionError("R3_STATUS_V1")
    if value["date"] != "2026-09-02":
        raise AssertionError("R3_DATE_V1")
    ceiling = value["claimCeiling"]
    if ceiling != "LOCAL_ADVERSE_STRUCTURE_INSTRUMENT_EVIDENCE_ONLY_NO_PRODUCTION_CLOSURE":
        raise AssertionError("R3_CLAIM_CEILING_V1")


def _is_sha256(value: object) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _validate_r3_repository(value: Mapping[str, object]) -> None:
    repository = value["repository"]
    if not isinstance(repository, dict):
        raise AssertionError("R3_REPOSITORY_V1")
    expected = ("baseCommit", "branch", "dirtyPaths", "productionSha256")
    _assert_exact_keys(repository, expected, "R3_REPOSITORY")
    if repository["baseCommit"] != "94f993bfd5240739f23dd5f5309a51e51034b962":
        raise AssertionError("R3_BASE_COMMIT_V1")
    if repository["branch"] != "codex/contract-resolution-pearson":
        raise AssertionError("R3_BRANCH_V1")
    dirty_paths = repository["dirtyPaths"]
    if not isinstance(dirty_paths, list) or dirty_paths != sorted(set(dirty_paths)):
        raise AssertionError("R3_DIRTY_PATHS_V1")
    production_hash = repository["productionSha256"]
    if production_hash != "9e4cb4a945602c3ca8e299aefa73b01e753d3b90bdaa465b849d81bcc2b80ef5":
        raise AssertionError("R3_PRODUCTION_HASH_V1")


def _validate_r3_hash_mapping(
    candidate: object, expected_paths: tuple[str, ...], label: str
) -> None:
    if not isinstance(candidate, dict):
        raise AssertionError(f"{label}_MAPPING_V1")
    if tuple(sorted(candidate)) != expected_paths:
        raise AssertionError(f"{label}_SET_V1")
    if not all(_is_sha256(candidate[path]) for path in expected_paths):
        raise AssertionError(f"{label}_SHA256_V1")


def _validate_r3_environment(value: Mapping[str, object]) -> None:
    cells = value["environmentCells"]
    if not isinstance(cells, list) or len(cells) != 4:
        raise AssertionError("R3_ENVIRONMENT_CELLS_V1")
    expected_labels = ("py311", "py312", "py313", "py314")
    if tuple(row.get("label") for row in cells if isinstance(row, dict)) != expected_labels:
        raise AssertionError("R3_ENVIRONMENT_LABELS_V1")
    for row, requested in zip(cells, ("3.11", "3.12", "3.13", "3.14"), strict=True):
        _validate_r3_environment_row(row, requested)


def _validate_r3_environment_row(row: object, requested: str) -> None:
    if not isinstance(row, dict):
        raise AssertionError("R3_ENVIRONMENT_ROW_V1")
    keys = (
        "architecture",
        "label",
        "machine",
        "numpy",
        "os",
        "pytest",
        "requestedPython",
        "resolvedPython",
        "ruff",
    )
    _assert_exact_keys(row, keys, "R3_ENVIRONMENT_ROW")
    if row["requestedPython"] != requested or not str(row["resolvedPython"]).startswith(requested):
        raise AssertionError("R3_ENVIRONMENT_PYTHON_V1")
    if row["pytest"] != "8.4.2" or row["ruff"] != "0.16.5":
        raise AssertionError("R3_ENVIRONMENT_TOOL_V1")
    for key in ("numpy", "os", "architecture", "machine"):
        if type(row[key]) is not str or not row[key]:
            raise AssertionError("R3_ENVIRONMENT_VALUE_V1")


def _validate_r3_tristate(value: Mapping[str, object]) -> None:
    state = value["triState"]
    expected_failed = {
        "test_verifier_primitives_module_exists",
        "test_verifier_slice_has_no_c901_findings",
        "test_verifier_slice_function_inventory_meets_span_and_parameter_gates",
    }
    expected_deferred = {
        "test_primitive_static_inventory_has_no_hidden_dispatch_or_state",
        "test_verifier_typed_topology_is_exact_and_complete",
        "test_public_verifier_runtime_graph_has_exact_primitive_ops_topology",
        "test_runtime_verifier_slot_schema_covers_every_dataclass_field",
        "test_builder_runtime_graph_stops_only_at_exact_public_terminal_boundary",
    }
    keys = ("collected", "deferred", "deferredNodeIds", "failed", "failedNodeIds", "passed")
    if not isinstance(state, dict):
        raise AssertionError("R3_TRISTATE_V1")
    _assert_exact_keys(state, keys, "R3_TRISTATE")
    failed_ids = set(state["failedNodeIds"])
    deferred_ids = set(state["deferredNodeIds"])
    if failed_ids & deferred_ids:
        raise AssertionError("R3_TRISTATE_OVERLAP_V1")
    if failed_ids != expected_failed:
        raise AssertionError("R3_FAILED_SET_V1")
    if deferred_ids != expected_deferred:
        raise AssertionError("R3_DEFERRED_SET_V1")
    counts = tuple(state[key] for key in ("collected", "passed", "failed", "deferred"))
    if any(type(count) is not int for count in counts):
        raise AssertionError("R3_TRISTATE_COUNT_TYPES_V1")
    if counts != (50, 42, 3, 5) or sum(counts[1:]) != counts[0]:
        raise AssertionError("R3_TRISTATE_COUNTS_V1")


def _validate_r3_commands(value: Mapping[str, object]) -> None:
    commands = value["commands"]
    if not isinstance(commands, list) or not commands:
        raise AssertionError("R3_COMMANDS_V1")
    required = (
        "argv",
        "cwd",
        "junitSha256",
        "name",
        "returnCode",
        "stderrSha256",
        "stdoutSha256",
    )
    for command in commands:
        if not isinstance(command, dict) or tuple(sorted(command)) != required:
            raise AssertionError("R3_COMMAND_FIELDS_V1")
    names = tuple(command["name"] for command in commands)
    if names != tuple(name for name, _return_code in R3_COMMAND_RETURN_CODES):
        raise AssertionError("R3_COMMAND_SET_V1")
    for command, expected in zip(commands, R3_COMMAND_RETURN_CODES, strict=True):
        _validate_r3_command(command, expected)


def _validate_r3_command(command: Mapping[str, object], expected: tuple[str, int]) -> None:
    name, return_code = expected
    if command["name"] != name or type(command["returnCode"]) is not int:
        raise AssertionError("R3_COMMAND_RETURN_CODE_V1")
    if command["returnCode"] != return_code:
        raise AssertionError("R3_COMMAND_RETURN_CODE_V1")
    argv = command["argv"]
    if not isinstance(argv, list) or not argv or not all(type(item) is str for item in argv):
        raise AssertionError("R3_COMMAND_ARGV_V1")
    cwd = command["cwd"]
    if type(cwd) is not str or not Path(cwd).is_absolute():
        raise AssertionError("R3_COMMAND_CWD_V1")
    if not _is_sha256(command["stdoutSha256"]) or not _is_sha256(command["stderrSha256"]):
        raise AssertionError("R3_COMMAND_STREAM_HASH_V1")
    junit = command["junitSha256"]
    if name in R3_JUNIT_COMMANDS and not _is_sha256(junit):
        raise AssertionError("R3_COMMAND_JUNIT_HASH_V1")
    if name not in R3_JUNIT_COMMANDS and junit is not None:
        raise AssertionError("R3_COMMAND_JUNIT_ABSENCE_V1")


def _validate_r3_prior(value: Mapping[str, object]) -> None:
    prior = value["priorReceipts"]
    if not isinstance(prior, list) or len(prior) != 3:
        raise AssertionError("R3_PRIOR_RECEIPTS_V1")
    r2 = next((row for row in prior if row.get("name") == "R2"), None)
    if r2 is None or r2.get("bytesVerified") is not False:
        raise AssertionError("R3_R2_BYTES_VERIFIED_V1")
    if r2.get("availability") != "HISTORICAL_REPORTED_IDENTITY_CURRENT_BYTES_UNAVAILABLE":
        raise AssertionError("R3_R2_AVAILABILITY_V1")
    if prior != _expected_prior_receipts():
        raise AssertionError("R3_PRIOR_RECEIPTS_V1")


def _expected_prior_receipts() -> list[dict[str, object]]:
    unavailable = "HISTORICAL_TEMPORARY_BYTES_AND_EXACT_IDENTITY_UNAVAILABLE"
    return [
        {
            "name": "R1",
            "reportedSha256": None,
            "path": None,
            "bytesVerified": False,
            "availability": unavailable,
        },
        {
            "name": "R2",
            "reportedSha256": "d2ad226b818c156c7651717c2658b58043fbd35dff4729758c15f6d72fab637b",
            "path": None,
            "bytesVerified": False,
            "availability": "HISTORICAL_REPORTED_IDENTITY_CURRENT_BYTES_UNAVAILABLE",
        },
        {
            "name": "Task1A",
            "reportedSha256": None,
            "path": None,
            "bytesVerified": False,
            "availability": unavailable,
        },
    ]


def _validate_r3_findings(value: Mapping[str, object]) -> None:
    findings = value["findingToFix"]
    if not isinstance(findings, dict):
        raise AssertionError("R3_FINDINGS_V1")
    node_ids = tuple(findings.values())
    if len(node_ids) != len(set(node_ids)) or set(node_ids) != set(R3_FINDING_NODE_IDS):
        raise AssertionError("R3_FINDING_NODE_SET_V1")


def _validate_r3_regressions(value: Mapping[str, object]) -> None:
    regressions = value["regressions"]
    expected = (("integration102", 102), ("regression588", 588), ("related690", 690))
    if not isinstance(regressions, list) or len(regressions) != len(expected):
        raise AssertionError("R3_REGRESSIONS_V1")
    for row, (name, passed) in zip(regressions, expected, strict=True):
        _validate_r3_regression_row(row, name, passed)


def _validate_r3_regression_row(row: object, name: str, passed: int) -> None:
    if not isinstance(row, dict):
        raise AssertionError("R3_REGRESSION_ROW_V1")
    _assert_exact_keys(row, ("failed", "name", "passed", "skipped"), "R3_REGRESSION_ROW")
    if row != {"name": name, "passed": passed, "failed": 0, "skipped": 0}:
        raise AssertionError("R3_REGRESSION_VALUE_V1")
