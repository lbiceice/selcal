from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = REPOSITORY_ROOT / "docs/status/dependency_licence_evidence_20260831.json"
CURRENT_BINDING = REPOSITORY_ROOT / "docs/status/dependency_licence_binding_20260922.json"
CLI_ENTRYPOINT_ADDITION = '[project.scripts]\nselcal = "selcal.cli:main"\n\n'


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _payload() -> dict[str, object]:
    return json.loads(INVENTORY.read_text(encoding="utf-8"))


def _binding() -> dict[str, object]:
    assert CURRENT_BINDING.is_file(), "missing current dependency evidence binding"
    return json.loads(CURRENT_BINDING.read_text(encoding="utf-8"))


def test_inventory_binds_current_project_and_lock_bytes() -> None:
    payload = _payload()
    identity = payload["inputIdentity"]
    assert isinstance(identity, dict)
    binding = _binding()
    assert binding["priorInventorySha256"] == _sha256(INVENTORY)
    assert binding["priorInventoryPath"] == INVENTORY.relative_to(REPOSITORY_ROOT).as_posix()
    assert binding["currentPyprojectSha256"] == _sha256(REPOSITORY_ROOT / "pyproject.toml")
    assert binding["priorPyprojectSha256"] == identity["pyprojectSha256"]
    assert binding["priorLockSha256"] == identity["lockSha256"]
    assert binding["currentLockSha256"] == _sha256(REPOSITORY_ROOT / "uv.lock")


def test_current_binding_replays_every_recorded_pyproject_edit_back_to_the_prior_project() -> None:
    binding = _binding()
    edits = binding["pyprojectEdits"]
    assert edits[0] == {"kind": "added", "text": CLI_ENTRYPOINT_ADDITION, "date": "2026-09-08"}
    current = (REPOSITORY_ROOT / "pyproject.toml").read_bytes()
    prior = current
    for edit in reversed(edits):
        if edit["kind"] == "added":
            text = edit["text"].encode("utf-8")
            assert prior.count(text) == 1
            prior = prior.replace(text, b"", 1)
        else:
            assert edit["kind"] == "replaced"
            text = edit["to"].encode("utf-8")
            assert prior.count(text) == 1
            prior = prior.replace(text, edit["from"].encode("utf-8"), 1)
    assert hashlib.sha256(prior).hexdigest() == _payload()["inputIdentity"]["pyprojectSha256"]
    current_fields = tomllib.loads(current.decode("utf-8"))
    assert current_fields["project"]["scripts"] == {"selcal": "selcal.cli:main"}
    assert current_fields["project"]["dependencies"] == ["numpy>=1.26,<2.5"]
    assert current_fields["project"]["license"] == "BSD-3-Clause"


def test_current_binding_does_not_relabel_historical_metadata_or_close_licences() -> None:
    binding = _binding()
    payload = _payload()
    assert binding["schemaVersion"] == "selcal-dependency-evidence-binding-v2"
    assert binding["status"] == "CURRENT_INPUT_BINDING_ONLY_LICENCE_HOLD_UNCHANGED"
    assert binding["historicalMetadataGeneratedAt"] == payload["generatedAt"]
    assert binding["dependencyMetadataReextracted"] is False
    # 2026-09-22: the lock changed (numpy 2.5.2 removed) but no package or version was added.
    assert binding["dependencySurfacesUnchanged"] is False
    assert binding["newPackagesOrVersions"] is False
    assert binding["legalClearance"] is False
    # 2026-09-22: the author selected BSD-3-Clause for SelCal itself (not a dependency audit).
    assert binding["rootSourceLicenceSelected"] is True
    assert binding["rootSourceLicence"]["spdx"] == "BSD-3-Clause"
    for name in binding["rootSourceLicence"]["files"]:
        assert (REPOSITORY_ROOT / name).is_file()
    assert binding["currentReleaseArtifactLicenceAudit"] == "NOT_PERFORMED"
    assert binding["historicalInventoryImmutable"] is True


def test_inventory_canonical_payload_digest_is_self_consistent() -> None:
    payload = _payload()
    observed = payload["canonicalPayloadSha256"]
    payload["canonicalPayloadSha256"] = None
    assert observed == _canonical_sha256(payload)


def test_inventory_plus_recorded_delta_is_a_bijection_to_all_lock_records() -> None:
    payload = _payload()
    lock = tomllib.loads((REPOSITORY_ROOT / "uv.lock").read_text(encoding="utf-8"))
    packages = lock["package"]
    components = payload["components"]
    assert isinstance(packages, list)
    assert isinstance(components, list)
    assert len(components) == 51
    delta = _binding()["lockDelta"]
    # Only the project's own record may be added (its version changed); no new dependency.
    assert all(added["name"] == "selcal" for added in delta["addedRecords"])
    inventoried = {
        (component["canonicalName"], component["version"]): component["lockRecordSha256"]
        for component in components
    }
    for removed in delta["removedRecords"]:
        key = (removed["name"], removed["version"])
        assert inventoried.pop(key) == removed["lockRecordSha256"]
    for change in delta["sameVersionRecordDigestChanges"]:
        key = (change["name"], change["version"])
        assert inventoried[key] == change["priorLockRecordSha256"]
        inventoried[key] = change["currentLockRecordSha256"]
    for added in delta["addedRecords"]:
        inventoried[(added["name"], added["version"])] = added["lockRecordSha256"]
    current = {
        (package["name"], package["version"]): _canonical_sha256(package) for package in packages
    }
    assert len(current) == len(packages) == 50
    assert current == inventoried


def test_inventory_preserves_the_three_noncompensating_licence_gates() -> None:
    payload = _payload()
    assert payload["status"] == "HOLD_TECHNICAL_LICENCE_INVENTORY_NOT_CLOSED"
    assert payload["rootSourceLicence"] == {
        "expression": None,
        "licenceFiles": [],
        "pyprojectField": None,
        "releaseArtifactCoverage": "NOT_EVALUATED_NO_RELEASE_ARTIFACT",
        "rightsHolderAttestation": "NOT_OBTAINED",
        "status": "UNSELECTED_AUTHOR_RIGHTS_HOLDER_ACTION",
    }
    assert payload["articleOaLicence"]["status"] == "UNSELECTED_FUTURE_PUBLISHER_WORKFLOW"
    assert payload["claimCeiling"] == (
        "PACKAGE_METADATA_EVIDENCE_ONLY_NOT_LEGAL_CLEARANCE_OR_COMPATIBILITY"
    )


def test_inventory_keeps_unlocked_build_requirement_as_a_blocker() -> None:
    payload = _payload()
    build = payload["unresolvedBuildSystemRequirements"]
    assert build == [
        {
            "lockRecordPresent": False,
            "materializedArtifactAudited": False,
            "requirementRaw": "setuptools>=68",
            "status": "UNRESOLVED_UNPINNED_BUILD_DEPENDENCY",
        }
    ]
    assert any(
        finding["id"] == "LIC-BLOCKER-BUILD-CLOSURE"
        and finding["severity"] == "BLOCKER"
        for finding in payload["findings"]
    )


def test_inventory_does_not_misrepresent_metadata_as_spdx_or_platform_closure() -> None:
    payload = _payload()
    target_scope = payload["targetScope"]
    assert target_scope["status"] == "UNFROZEN"
    assert target_scope["closedTargetMatrix"] is False
    assert target_scope["markerEvaluationComplete"] is False
    assert payload["artifactAudit"]["wheelAndSdistSeparatelyAudited"] is False
    assert payload["artifactAudit"]["vendoredComponentLedgerComplete"] is False
    assert payload["environmentEvidencePolicy"]["sharedProjectVenvAuthoritative"] is False

    external = [
        component
        for component in payload["components"]
        if component["canonicalName"] != "selcal"
    ]
    assert len(external) == 50
    assert all(component["licenceEvidence"] is not None for component in external)
    assert all(
        component["licenceEvidence"]["legalCompatibilityConclusion"] is None
        for component in external
    )


def test_inventory_covers_every_declared_direct_dependency_surface() -> None:
    payload = _payload()
    assert payload["declaredDirectSurfaces"] == {
        "benchmark": ["matplotlib>=3.11.1,<4"],
        "buildSystem": ["setuptools>=68"],
        "dev": [
            "build>=1.2,<2",
            "mypy>=1.11,<2",
            "pip>=24,<27",
            "pytest>=8,<9",
            "pytest-cov>=5,<7",
            "ruff>=0.6,<1",
        ],
        "docs": ["sphinx>=8.2.3,<9"],
        "runtime": ["numpy>=1.26,<3"],
    }


def test_every_external_lock_record_has_exact_version_metadata_evidence() -> None:
    payload = _payload()
    for component in payload["components"]:
        if component["canonicalName"] == "selcal":
            assert component["licenceEvidence"] is None
            continue
        evidence = component["licenceEvidence"]
        assert evidence["metadataName"] == component["canonicalName"]
        assert evidence["metadataVersion"] == component["version"]
        assert len(evidence["metadataSha256"]) == 64
        assert evidence["evidenceState"] != "NO_EXACT_VERSION_METADATA"
