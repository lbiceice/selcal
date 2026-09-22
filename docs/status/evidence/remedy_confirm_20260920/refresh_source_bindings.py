"""Refresh source-identity evidence after an intentional, reviewed production-code change.

Rewrites only derived identities (line numbers, segment digests, file digests) in:
- tests/fixtures/verifier_structure_gate_v1.json (builder frontier, runtime frontier, legacy rows)
- docs/status/scientific_code_smell_binding_20260920.json (changed/added source digests)
Graph budgets are recomputed and must not grow silently: the script prints old -> new.
Run from the repository root with the project interpreter. It never changes scientific content.
"""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tests"))

import _verifier_structure_gate_v1 as gate  # noqa: E402
import test_verifier_complexity_slice_v1 as slice_tests  # noqa: E402

import selcal.calibration_v2 as calibration_v2  # noqa: E402


def refresh_structure_fixture() -> None:
    path = ROOT / "tests/fixtures/verifier_structure_gate_v1.json"
    fixture = json.loads(path.read_text())
    old_budget = dict(fixture["graphBudgets"]["observed"])
    strict_match = gate._manifest_match
    gate._manifest_match = lambda row, expected: True  # regenerate rows from current source
    try:
        result = gate.walk_identity_graph(
            (calibration_v2.calibrate_selected_family,),
            slice_tests._budgets(fixture["graphBudgets"]["frozen"]),
            slice_tests._builder_policy(fixture),
        )
    finally:
        gate._manifest_match = strict_match
    fixture["builderNeutralFrontier"] = [dict(row) for row in result.project_rows]
    fixture["builderNeutralFrontierCount"] = len(result.project_rows)
    observed = {"nodes": result.nodes, "edges": result.edges, "depth": result.depth}
    fixture["graphBudgets"]["observed"] = observed
    fixture["graphBudgets"]["frozen"] = gate.freeze_budgets(observed)
    path.write_bytes(gate.canonical_json_bytes(fixture))

    fixture = json.loads(path.read_text())
    fixture["frontier"] = [
        {**row, **gate.source_identity_row(function, slice_tests.REPOSITORY_ROOT)}
        for row, function in slice_tests._frontier_functions()
    ]
    legacy = []
    for row in fixture["legacyDeclarations"]:
        source = slice_tests.REPOSITORY_ROOT / row["sourcePath"]
        _raw, text = gate.normalized_source(source)
        kind = getattr(ast, row["kind"])
        found = [
            node
            for node in ast.parse(text, filename=str(source)).body
            if type(node) is kind and gate._top_level_target(node) == row["name"]
        ]
        if len(found) != 1:
            raise SystemExit(f"legacy declaration not unique: {row['name']}")
        line = found[0].lineno
        legacy.append(
            {
                **row,
                "firstLine": line,
                "sourceSegmentSha256": gate.source_segment_digest(
                    source,
                    kind=row["kind"],
                    qualname_or_target=row["name"],
                    first_line=line,
                    legacy=True,
                ),
                "sourceSha256": gate.sha256_file(source),
            }
        )
    fixture["legacyDeclarations"] = legacy
    path.write_bytes(gate.canonical_json_bytes(fixture))
    print("structure fixture: graph", old_budget, "->", observed)


def refresh_audit_binding() -> None:
    def sha(relative: str) -> str:
        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

    path = ROOT / "docs/status/scientific_code_smell_binding_20260920.json"
    doc = json.loads(path.read_text())
    audit = json.loads((ROOT / doc["priorAuditPath"]).read_text())
    cited = {source["path"]: source["sha256"] for source in audit["sourceIdentity"]}
    changed = [
        {"path": name, "auditSha256": digest, "currentSha256": sha(name)}
        for name, digest in sorted(cited.items())
        if sha(name) != digest
    ]
    doc["changedSincePriorAudit"] = changed
    doc["unchangedPriorSourceCount"] = len(cited) - len(changed)
    doc["preimageBoundSource"]["currentSha256"] = sha(doc["preimageBoundSource"]["path"])
    doc["addedSources"] = [{**added, "sha256": sha(added["path"])} for added in doc["addedSources"]]
    path.write_text(json.dumps(doc, indent=2) + "\n")
    print("audit binding: changed", [row["path"] for row in changed])


if __name__ == "__main__":
    refresh_structure_fixture()
    refresh_audit_binding()
