"""Design-only fixtures, never scientific data, measurements, or approval evidence.

Run with an isolated jsonschema 4.26.0 environment. This is not the future
selcal.m6-p1.semantic-validator.v9 and never emits a VALIDATION_REPORT artifact.
"""

from __future__ import annotations

import copy
from datetime import datetime
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import struct

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "docs/benchmarks/schemas/m6-p1-artifact-contract-v9-proposal.schema.json"
CONTRACT_PATH = ROOT / "docs/benchmarks/contracts/m6-p1-semantic-contract-v9-proposal.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text())
CONTRACT = json.loads(CONTRACT_PATH.read_text())
FORMAT = FormatChecker()
HEX = "0x1.0000000000000p-1"


@FORMAT.checks("date-time", raises=(ValueError, TypeError))
def real_utc_instant(value):
    if not isinstance(value, str):
        return True
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M:%SZ") == value


def validator(schema=SCHEMA):
    return Draft202012Validator(schema, format_checker=FORMAT)


def resolve(ref):
    assert ref.startswith("#/$defs/"), ref
    return SCHEMA["$defs"][ref.rsplit("/", 1)[1]]


def witness(shape):
    """Produce explicit in-memory synthetic local-shape witnesses, not run data."""
    if "$ref" in shape:
        name = shape["$ref"].rsplit("/", 1)[1]
        if name == "Sha256":
            return "0" * 64
        if name in {"FloatHex", "PositiveFloatHex", "StrictProbabilityHex", "NonnegativeToleranceHex"}:
            return HEX
        if name == "UTCInstant":
            return "2026-09-08T00:00:00Z"
        if name == "FieldPath":
            return "/aggregate/E"
        if name == "OperatorCursor":
            return witness(resolve(shape["$ref"])["oneOf"][0])
        return witness(resolve(shape["$ref"]))
    if "const" in shape:
        return copy.deepcopy(shape["const"])
    if "enum" in shape:
        return shape["enum"][0]
    if "oneOf" in shape:
        return witness(shape["oneOf"][0])
    if shape.get("type") == "object":
        result = {k: witness(shape["properties"][k]) for k in shape["required"]}
        if "finiteReplicateCount" in result:
            result.update(commonLength=2, finiteReplicateCount=None, replicateMappingLocator=None)
        if result.get("artifactType") == "FAILURE_MANIFEST":
            result.update(primaryTerminalClass=None, operatorCursor=None,
                          preDerivationEvidence=None, interruptedCause=None)
        if "diagnosticIndex" in result and result.get("outcome") == "MATCH":
            result["diagnosticIndex"] = None
        if result.get("artifactType") == "RUNTIME_PROBE":
            result["measuredAtUtc"] = None
        if result.get("disposition") == "NOT_OPENED":
            result["retainedArtifact"] = None
        if result.get("rule") == "OPTIONAL_FLOAT_ABS_TOL" and "residualStatus" not in result:
            result["referenceValue"] = None
        return result
    if shape.get("type") == "array":
        if "prefixItems" in shape:
            return [witness(item) for item in shape["prefixItems"]]
        values = [witness(shape["items"]) for _ in range(shape.get("minItems", 0))]
        if shape.get("uniqueItems") and values and isinstance(values[0], int):
            first = shape["items"].get("minimum", 0)
            values = list(range(first, first + len(values)))
        return values
    if shape.get("type") == "integer":
        return shape.get("minimum", 0)
    if shape.get("type") == "boolean":
        return False
    if shape.get("type") == "null":
        return None
    if shape.get("type") == "string":
        if shape.get("format") == "date-time":
            return "2026-09-08T00:00:00Z"
        return "x"
    if "allOf" in shape:
        return witness(shape["allOf"][0])
    raise AssertionError(f"Unbounded or unsupported witness shape: {shape}")


def check_refs():
    visited = set()
    refs = set()

    def walk(node):
        if isinstance(node, dict):
            if "$ref" in node:
                refs.add(node["$ref"])
                definition = resolve(node["$ref"])
                if node["$ref"] not in visited:
                    visited.add(node["$ref"])
                    walk(definition)
            for key, value in node.items():
                if key != "$defs":
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(SCHEMA)
    assert visited == {"#/$defs/" + name for name in SCHEMA["$defs"]}
    return len(refs)


def check():
    Draft202012Validator.check_schema(SCHEMA)
    ref_count = check_refs()
    v = validator()
    specimens = {}
    for branch in SCHEMA["oneOf"]:
        value = witness(branch)
        assert v.is_valid(value), (value["artifactType"], value)
        matches = sum(v.evolve(schema=option).is_valid(value) for option in SCHEMA["oneOf"])
        assert matches == 1, (value["artifactType"], matches)
        specimens[value["artifactType"]] = value
    assert set(specimens) == set(CONTRACT["artifactRootRegistry"]["topLevelArtifactTypesInOrder"])
    union_count = 0

    def visit_unions(node, path=""):
        nonlocal union_count
        if isinstance(node, dict):
            if "oneOf" in node:
                for branch in node["oneOf"]:
                    value = witness(branch)
                    assert v.evolve(schema=node).is_valid(value), (path, value)
                    union_count += 1
            for key, child in node.items():
                visit_unions(child, path + "/" + key)
        elif isinstance(node, list):
            for i, child in enumerate(node):
                visit_unions(child, path + "/" + str(i))

    visit_unions(SCHEMA)
    budget_constants = SCHEMA["$defs"]["BudgetProfile"]["properties"]["constants"]["properties"]
    assert {k: value["const"] for k, value in budget_constants.items()} == CONTRACT["closedConstants"]
    assert SCHEMA["$defs"]["DisagreementCode"]["enum"] == CONTRACT["failureRegistries"]["ComparisonDisagreementCode"]["codesInSeverityOrder"]

    bad = [("empty artifact", {})]

    def mutation(name, root, change):
        value = copy.deepcopy(specimens[root])
        change(value)
        bad.append((name, value))

    mutation("missing selection rule", "REFERENCE_SPEC", lambda x: x.pop("selectionRule"))
    mutation("missing tie tolerance", "REFERENCE_SPEC", lambda x: x.pop("tieToleranceHex"))
    mutation("alpha zero", "REFERENCE_SPEC", lambda x: x.update(alphaHex="0x0.0p+0"))
    mutation("alpha one", "REFERENCE_SPEC", lambda x: x.update(alphaHex="0x1.0000000000000p+0"))
    mutation("negative tolerance", "REFERENCE_SPEC", lambda x: x.update(tieToleranceHex="-" + HEX))
    mutation("candidate zero", "REFERENCE_SPEC", lambda x: x.update(candidates=[0]))
    mutation("candidate duplicate", "REFERENCE_SPEC", lambda x: x.update(candidates=[1, 1]))
    mutation("candidate float string", "REFERENCE_SPEC", lambda x: x.update(candidates=[HEX]))
    mutation("candidate fractional number", "REFERENCE_SPEC", lambda x: x.update(candidates=[1.5]))
    mutation("boolean length", "REFERENCE_SPEC", lambda x: x.update(commonLength=True))
    mutation("finite mapping absent", "REFERENCE_SPEC", lambda x: x.update(calculationMode="FINITE_B_COMPLETED_STATE_REPLAY", finiteReplicateCount=1))
    mutation("observed illegally has state", "OBSERVED_RECORD", lambda x: x.update(state=witness({"$ref":"#/$defs/State"})))
    mutation("replicateId absent", "PRODUCTION_REPLAY_ROW", lambda x: x.pop("replicateId"))
    mutation("candidate code domain leak", "OBSERVED_RECORD", lambda x: x["candidateRecords"][0].update(status="ANALYTIC_FAILURE", estimateHex=None, failureCode="JSON_DECODE_FAILED"))
    mutation("duplicated comparison vector", "COMPARISON_RECORD", lambda x: x.update(candidateRecords=[]))
    mutation("empty field plan", "COMPARISON_RECORD", lambda x: x["requiredFieldPlan"].update(fieldComparisonPlan=[]))
    mutation("q over cap", "COMPARISON_RECORD", lambda x: x["requiredFieldPlan"].update(q=4097))
    mutation("source lifecycle field forbidden", "DECLARED_SOURCE_INVENTORY", lambda x: x.update(lifecycle=witness({"$ref":"#/$defs/Lifecycle"})))
    mutation("graph missing edges", "DECLARED_RUN_GRAPH", lambda x: x["graphProjection"].pop("edges"))
    mutation("terminal missing source inventories", "FAILURE_MANIFEST", lambda x: x.pop("sourceInventories"))
    mutation("failure emitter mismatch", "FAILURE_MANIFEST", lambda x: x["failure"].update(code="CANDIDATE_ESTIMATE_MISMATCH"))
    mutation("unavailable raw counter missing reason", "FAILURE_MANIFEST", lambda x: x["rawCounters"].update(pearsonValueVisits={"status":"UNAVAILABLE", "value":None}))
    mutation("validation report missing identity", "VALIDATION_REPORT", lambda x: x.pop("schemaIdentity"))
    mutation("invalid real UTC date", "VALIDATION_REPORT", lambda x: x.update(startedAtUtc="2026-02-30T00:00:00Z"))
    mutation("local approval claims trusted", "EXTERNAL_APPROVAL_ENVELOPE", lambda x: x.update(trustStatus="TRUSTED"))
    mutation("approval missing binding", "EXTERNAL_APPROVAL_ENVELOPE", lambda x: x["bindings"].pop())
    mutation("runtime unexecuted carries measurement", "RUNTIME_PROBE", lambda x: x.update(measuredAtUtc="2026-09-08T00:00:00Z"))
    for name, value in bad:
        assert not v.is_valid(value), name

    # Regression RED: the interrupted empty schema accepts every malformed artifact.
    placeholder_accepts = sum(validator({}).is_valid(value) for _, value in bad)
    assert placeholder_accepts == len(bad)
    assert not (not validator({}).is_valid({})), "The real empty-object rejection must fail under {}"

    branch_checks = 0

    def definition_check(name, value, expected):
        nonlocal branch_checks
        actual = v.evolve(schema=SCHEMA["$defs"][name]).is_valid(value)
        assert actual is expected, (name, expected, value)
        branch_checks += 1

    block = {"kind":"BLOCK_SHUFFLE", "q":4096, "order":list(range(4096)), "isIdentity":True}
    definition_check("State", block, True)
    definition_check("State", dict(block, q=4097), False)
    overflow = {"path":"/candidateRecords/0/estimateHex", "pathClass":"APPROXIMATE_FLOAT_OR_NULL", "rule":"OPTIONAL_FLOAT_ABS_TOL", "disagreementCode":"CANDIDATE_ESTIMATE_MISMATCH", "matches":False, "referenceValue":"-0x1.fffffffffffffp+1023", "productionValue":"0x1.fffffffffffffp+1023", "toleranceHex":CONTRACT["closedConstants"]["floatAbsoluteToleranceHex"], "residualStatus":"OVERFLOW", "residualHex":None}
    definition_check("FieldComparison", overflow, True)
    definition_check("FieldComparison", dict(overflow, residualHex="inf"), False)
    definition_check("FieldComparison", dict(overflow, residualHex=HEX), False)
    retained = {"artifactId":"partial", "relativePath":"partial.jsonl", "bytes":0, "digestStatus":"UNVERIFIED", "sha256":None, "verificationBytesRead":0, "disposition":"RETAINED_PARTIAL"}
    definition_check("RetainedArtifact", retained, True)
    definition_check("RetainedArtifact", dict(retained, sha256="0"*64), False)
    definition_check("RetainedArtifact", dict(retained, digestStatus="VERIFIED"), False)
    source_cursor = witness(SCHEMA["$defs"]["OperatorCursor"]["oneOf"][0])
    source_cursor.update(operation="HASH", byteOffset=64, hashBlockIndex=1)
    definition_check("OperatorCursor", source_cursor, True)
    definition_check("OperatorCursor", dict(source_cursor, genericActiveScanProgress=0), False)
    candidate_spec = copy.deepcopy(specimens["REFERENCE_SPEC"])
    candidate_spec.update(commonLength=2502, candidates=list(range(1, 2501)))
    definition_check("ReferenceSpec", candidate_spec, True)
    candidate_spec["candidates"].append(2501)
    definition_check("ReferenceSpec", candidate_spec, False)
    counter = {"status":"AVAILABLE", "value":2**256-1, "reason":None}
    definition_check("Counter", counter, True)
    definition_check("Counter", dict(counter, value=2**256), False)
    unavailable = {"status":"UNAVAILABLE", "relativePath":"raw.json", "expectedIdentity":None, "observedBytes":None, "observedSha256":None, "reason":"STAT_FAILED"}
    definition_check("RawSourceEvidence", unavailable, True)
    definition_check("RawSourceEvidence", dict(unavailable, observedSha256="0"*64), False)
    definition_check("FailedValueEvidence", {"status":"UNAVAILABLE", "reason":"NOT_DECODED"}, True)
    definition_check("FailedValueEvidence", {"status":"UNAVAILABLE", "reason":"NOT_DECODED", "valueDigest":"0"*64}, False)
    failure = copy.deepcopy(specimens["FAILURE_MANIFEST"])
    failure.update(failureStage="N00_PREFLIGHT", preDerivationEvidence={"rawSourceEvidence":unavailable, "failedNodeId":"N00_PREFLIGHT", "location":None, "failedValueEvidence":{"status":"UNAVAILABLE", "reason":"NOT_DECODED"}, "completeKnownPrefix":[]})
    definition_check("FailureManifest", failure, True)
    failure["preDerivationEvidence"].pop("completeKnownPrefix")
    definition_check("FailureManifest", failure, False)

    # Known remaining dynamic gaps: these must not be described as schema rejection.
    dynamic_only = copy.deepcopy(specimens["REFERENCE_SPEC"])
    dynamic_only["commonLength"] = 8
    dynamic_only["candidates"] = [2, 1]
    assert v.is_valid(dynamic_only), "Ordering intentionally belongs to semantic validation"

    header = CONTRACT["binary64SidecarRegistry"]["headerLayout"][0]
    magic = bytes.fromhex(header["valueHex"])
    assert magic == b"SCF64L1\0" and len(magic) == 8
    encoded = magic + struct.pack("<HHI", 1, 1, 1) + struct.pack("<d", 0.5)
    assert len(encoded) == 24 and struct.unpack("<d", encoded[16:])[0] == 0.5
    assert bytes.fromhex(CONTRACT["sourceInventoryRegistry"]["sourceSetIdDefinition"]["domainPrefixHex"]) == b"selcal:m6:p1:v9:source-set\0"
    p = float.fromhex("0x1.fffffffffffffp+1023")
    r = -p
    tolerance = float.fromhex(CONTRACT["closedConstants"]["floatAbsoluteToleranceHex"])
    assert not (abs(Fraction.from_float(p)-Fraction.from_float(r)) <= Fraction.from_float(tolerance))
    assert not math.isfinite(p-r)

    result = {
        "scope":"DESIGN_ONLY_LOCAL_SHAPE_FIXTURES",
        "metaschema":"PASS",
        "reachable_definitions":ref_count,
        "unique_root_witnesses":len(specimens),
        "local_oneOf_branch_witnesses":union_count,
        "malformed_artifacts_rejected":len(bad),
        "placeholder_schema_accepts_same_malformed_artifacts":placeholder_accepts,
        "additional_branch_checks":branch_checks,
        "semantic_checks_not_implemented":True,
        "scientific_execution":False,
        "schema_sha256":hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest(),
        "semantic_contract_sha256":hashlib.sha256(CONTRACT_PATH.read_bytes()).hexdigest(),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    check()
