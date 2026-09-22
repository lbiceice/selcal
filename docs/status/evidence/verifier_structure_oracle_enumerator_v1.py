"""Independent, evidence-only builder frontier enumerator.

The program prints one canonical JSON candidate and never writes repository files.
"""

from __future__ import annotations

import ast
import dis
import hashlib
import json
from collections import deque
from collections.abc import Mapping
from pathlib import Path
from types import FunctionType

import selcal.calibration_v2 as calibration_v2
import selcal.contracts_v2 as contracts_v2

ROOT = Path(__file__).resolve().parents[3]


def _normalized_source(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return raw.decode("utf-8", errors="strict")


def _declarations(tree: ast.Module) -> tuple[tuple[str, ast.AST], ...]:
    found: list[tuple[str, ast.AST]] = []

    def visit(body: list[ast.stmt], parent: str, function_scope: bool) -> None:
        for node in body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            prefix = f"{parent}.<locals>" if parent and function_scope else parent
            qualname = f"{prefix}.{node.name}" if prefix else node.name
            found.append((qualname, node))
            visit(node.body, qualname, isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))

    visit(tree.body, "", False)
    return tuple(found)


def _segment_digest(path: Path, qualname: str, first_line: int) -> str:
    text = _normalized_source(path)
    tree = ast.parse(text, filename=str(path))
    matches = tuple(
        node
        for name, node in _declarations(tree)
        if type(node) is ast.FunctionDef and name == qualname and node.lineno == first_line
    )
    if len(matches) != 1:
        raise AssertionError(f"ORACLE_SOURCE_MATCH_COUNT:{len(matches)}:{qualname}")
    node = matches[0]
    if any(
        getattr(node, name, None) is None
        for name in ("lineno", "col_offset", "end_lineno", "end_col_offset")
    ):
        raise AssertionError(f"ORACLE_SOURCE_POSITION:{qualname}")
    segment = ast.get_source_segment(text, node, padded=False)
    if segment is None:
        raise AssertionError(f"ORACLE_SOURCE_SEGMENT:{qualname}")
    return hashlib.sha256(segment.encode("utf-8", errors="strict")).hexdigest()


def _source_row(function: FunctionType) -> dict[str, object]:
    path = Path(function.__code__.co_filename).resolve()
    lexical_qualname = _qualname_at_line(path, function.__code__.co_firstlineno)
    return {
        "module": function.__module__,
        "qualname": lexical_qualname,
        "sourcePath": path.relative_to(ROOT).as_posix(),
        "sourceSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "firstLine": function.__code__.co_firstlineno,
        "sourceSegmentSha256": _segment_digest(
            path, lexical_qualname, function.__code__.co_firstlineno
        ),
    }


def _qualname_at_line(path: Path, first_line: int) -> str:
    tree = ast.parse(_normalized_source(path), filename=str(path))
    matches = tuple(
        qualname
        for qualname, node in _declarations(tree)
        if type(node) in (ast.FunctionDef, ast.AsyncFunctionDef) and node.lineno == first_line
    )
    if len(matches) != 1:
        raise AssertionError(f"ORACLE_SOURCE_LINE_MATCH_COUNT:{len(matches)}")
    return matches[0]


def _function_children(function: FunctionType) -> tuple[object, ...]:
    values: list[object] = list(function.__defaults__ or ())
    values.extend(value for _key, value in sorted((function.__kwdefaults__ or {}).items()))
    for _name, cell in zip(function.__code__.co_freevars, function.__closure__ or (), strict=True):
        try:
            values.append(cell.cell_contents)
        except ValueError:
            continue
    names = sorted(
        {
            instruction.argval
            for instruction in dis.get_instructions(function)
            if instruction.opname in {"LOAD_GLOBAL", "LOAD_NAME"}
            and isinstance(instruction.argval, str)
        }
    )
    values.extend(function.__globals__[name] for name in names if name in function.__globals__)
    return tuple(values)


def _children(value: object) -> tuple[object, ...]:
    if type(value) is FunctionType:
        if value is contracts_v2.verify_calibration_result:
            return ()
        if value is not calibration_v2.calibrate_selected_family and _is_project_function(value):
            return ()
        return _function_children(value)
    if isinstance(value, Mapping):
        children: list[object] = []
        for key, item in sorted(value.items(), key=lambda pair: _scalar_key(pair[0])):
            children.extend((key, item))
        return tuple(children)
    if type(value) in (tuple, list):
        return tuple(value)
    if type(value) in (set, frozenset):
        return tuple(sorted(value, key=_scalar_key))
    return ()


def _is_project_function(value: FunctionType) -> bool:
    path = Path(value.__code__.co_filename).resolve()
    try:
        path.relative_to(ROOT / "src/selcal")
    except ValueError:
        return False
    return True


def _scalar_key(value: object) -> tuple[str, str, str]:
    value_type = type(value)
    if value is None or value_type in (bool, int, float, str, bytes):
        return (value_type.__module__, value_type.__qualname__, repr(value))
    return (value_type.__module__, value_type.__qualname__, repr(value))


def _enumerate() -> dict[str, object]:
    queue = deque([(calibration_v2.calibrate_selected_family, 0)])
    seen: set[int] = set()
    rows: dict[tuple[object, ...], dict[str, object]] = {}
    edges = 0
    depth = 0
    while queue:
        value, item_depth = queue.popleft()
        if id(value) in seen:
            continue
        seen.add(id(value))
        depth = max(depth, item_depth)
        _record_project_function(value, rows)
        for child in _children(value):
            edges += 1
            if id(child) not in seen:
                queue.append((child, item_depth + 1))
    ordered = sorted(
        rows.values(),
        key=lambda row: (row["module"], row["qualname"], row["sourcePath"], row["firstLine"]),
    )
    return {
        "builderNeutralFrontier": ordered,
        "builderNeutralFrontierCount": len(ordered),
        "observed": {"nodes": len(seen), "edges": edges, "depth": depth},
    }


def _record_project_function(
    value: object, rows: dict[tuple[object, ...], dict[str, object]]
) -> None:
    if type(value) is not FunctionType or value in {
        calibration_v2.calibrate_selected_family,
        contracts_v2.verify_calibration_result,
    }:
        return
    path = Path(value.__code__.co_filename).resolve()
    try:
        path.relative_to(ROOT / "src/selcal")
    except ValueError:
        return
    row = _source_row(value)
    key = tuple(row[name] for name in sorted(row))
    rows[key] = row


def main() -> None:
    print(json.dumps(_enumerate(), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
