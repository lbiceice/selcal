"""Replay public commands using a fresh non-editable installation from a real sdist."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
EXPECTED_SOURCE_SHA256 = "4eca1dae0f0a261a5bf3bc2632ad261fd460a09de712ddf65e4c8bd6ddff205e"
BASE_PYTHON = Path("/tmp/selcal-result-wire-check.xwPfjz/audit-env/bin/python")
UV = "/opt/homebrew/bin/uv"


def identity(package: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    rows = []
    for path in sorted(package.rglob("*.py")):
        relative = path.relative_to(package).as_posix()
        name, content = relative.encode(), path.read_bytes()
        digest.update(len(name).to_bytes(8, "big"))
        digest.update(name)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
        rows.append({"path": relative, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
    return {"scheme": "installed_python_sources_v1", "file_count": len(rows), "sha256": digest.hexdigest(), "files": rows}


def artifact(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> int:
    workspace, sdist = map(lambda value: Path(value).resolve(strict=True), sys.argv[1:3])
    wheel = next(sdist.parent.glob("*.whl"))
    assert workspace.parent == Path("/tmp").resolve() and workspace.name.startswith("selcal-product-installed-")
    assert not list(workspace.iterdir()), "A fresh empty temporary workspace is required"
    receipt_name = sys.argv[3] if len(sys.argv) > 3 else "installed_check.json"
    assert Path(receipt_name).name == receipt_name and receipt_name.startswith("installed_")
    receipt_path = EVIDENCE / receipt_name
    expected_source_sha256 = sys.argv[4] if len(sys.argv) > 4 else EXPECTED_SOURCE_SHA256
    existing_environment = Path(sys.argv[5]).resolve(strict=True) if len(sys.argv) > 5 else None
    environment_root = existing_environment or (workspace / "venv")
    if existing_environment is not None:
        assert existing_environment.parent.parent == Path("/tmp").resolve()
        assert existing_environment.parent.name.startswith("selcal-product-installed-")
        assert existing_environment.name == "venv"
    artifact_prefix = receipt_path.stem.removeprefix("installed_check")
    assert not receipt_path.exists(), "Prior evidence is immutable; choose a new receipt name"
    records: list[dict[str, object]] = []
    receipt: dict[str, object] = {
        "schema": "selcal.installed-sdist-user-flow-check.v1",
        "scope": "LOCAL_SYNTHETIC_INSTALLED_SDIST_NOT_SCIENTIFIC_LICENCE_RELEASE_OR_SUBMISSION_VALIDATION",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "checkout": str(ROOT),
        "driver": artifact(Path(__file__)),
        "status": "IN_PROGRESS",
        "expected_source_identity_sha256": expected_source_sha256,
        "reused_isolated_dependency_environment": str(existing_environment) if existing_environment else None,
        "results": records,
        "artifacts": [artifact(sdist), artifact(wheel)],
    }
    environment = os.environ.copy()
    removed = {key: key in environment for key in ("PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV")}
    for key in removed:
        environment.pop(key, None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONNOUSERSITE"] = "1"
    environment["UV_CACHE_DIR"] = str(workspace / "uv-cache")
    receipt["environment_isolation"] = {"removed_environment_variables": removed, "effective_pythonpath": None, "user_site_disabled": True}

    def run(label: str, argv: list[str], *, expected: int = 0) -> dict[str, object]:
        started = time.monotonic()
        completed = subprocess.run(argv, cwd=workspace, env=environment, capture_output=True, text=True, timeout=180)
        row: dict[str, object] = {"label": label, "argv": argv, "cwd": str(workspace), "returncode": completed.returncode, "expected_returncode": expected, "stdout": completed.stdout, "stderr": completed.stderr, "elapsed_seconds": time.monotonic() - started}
        records.append(row)
        if completed.stdout.strip():
            try:
                row["stdout_json"] = json.loads(completed.stdout)
            except json.JSONDecodeError:
                pass
        assert completed.returncode == expected, f"{label}: exit {completed.returncode}; expected {expected}"
        return row

    try:
        checkout_before = identity(ROOT / "src/selcal")
        assert checkout_before["file_count"] == 39
        assert checkout_before["sha256"] == expected_source_sha256
        receipt["checkout_source_before"] = checkout_before
        # Only regular source-package members are inspected; copy public examples,
        # not the package source tree, into the execution workspace.
        with tarfile.open(sdist, "r:gz") as archive:
            members = archive.getmembers()
            assert all(member.isfile() or member.isdir() for member in members)
            archive_files = {}
            for member in members:
                if not member.isfile():
                    continue
                relative = member.name.partition("/")[2]
                assert relative and not Path(relative).is_absolute() and ".." not in Path(relative).parts
                assert relative not in archive_files
                stream = archive.extractfile(member)
                assert stream is not None
                archive_files[relative] = stream.read()
            assert {name.removeprefix("src/selcal/") for name in archive_files if name.startswith("src/selcal/") and name.endswith(".py")} == {row["path"] for row in checkout_before["files"]}
            for row in checkout_before["files"]:
                relative = row["path"]
                assert archive_files["src/selcal/" + relative] == (ROOT / "src/selcal" / relative).read_bytes()
            for relative, content in archive_files.items():
                if relative.startswith("examples/"):
                    target = workspace / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
        with zipfile.ZipFile(wheel) as archive:
            assert {name.removeprefix("selcal/") for name in archive.namelist() if name.startswith("selcal/") and name.endswith(".py")} == {row["path"] for row in checkout_before["files"]}
            for row in checkout_before["files"]:
                relative = row["path"]
                assert archive.read("selcal/" + relative) == (ROOT / "src/selcal" / relative).read_bytes()
        receipt["archive_source_comparison"] = {"sdist": "39_OF_39_BYTE_IDENTICAL", "sibling_wheel": "39_OF_39_BYTE_IDENTICAL"}
        if existing_environment is None:
            run("create_fresh_venv", [UV, "venv", "--python", str(BASE_PYTHON), str(environment_root)])
        python = str(environment_root / "bin/python")
        if existing_environment is None:
            install_args = [str(sdist), "numpy==2.4.6"]
        else:
            install_args = ["--no-deps", "--reinstall-package", "selcal", str(sdist)]
        run("install_from_real_sdist", [UV, "pip", "install", "--python", python, "--no-cache", *install_args])
        environment["PATH"] = str(environment_root / "bin") + os.pathsep + environment.get("PATH", "")
        probe = run("installed_import_and_dependency_identity", [python, "-I", "-c", "import importlib.metadata as m,json,os,platform,sys,selcal; d=m.distribution('selcal'); print(json.dumps({'module':selcal.__file__,'executable':sys.executable,'sys_path':sys.path,'python':sys.version,'platform':platform.platform(),'pythonpath':os.environ.get('PYTHONPATH'),'direct_url':json.loads(d.read_text('direct_url.json')),'dependencies':{x.metadata['Name']:x.version for x in m.distributions()}},sort_keys=True))"])["stdout_json"]
        installed = Path(probe["module"]).resolve().parent
        assert installed.is_relative_to(environment_root)
        assert not any(path and Path(path).resolve().is_relative_to(ROOT) for path in probe["sys_path"])
        assert probe["pythonpath"] is None
        assert "dir_info" not in probe["direct_url"]
        assert probe["direct_url"]["url"] == sdist.as_uri()
        assert artifact(sdist) == receipt["artifacts"][0]
        receipt["installation_provenance"] = {"actual_url_matches_hashed_sdist": True, "archive_info_as_returned": probe["direct_url"]["archive_info"], "hash_provenance": "Independent SHA-256 of installed source archive; not inferred from absent uv metadata."}
        installed_identity = identity(installed)
        assert installed_identity == checkout_before
        for row in installed_identity["files"]:
            assert (installed / row["path"]).read_bytes() == (ROOT / "src/selcal" / row["path"]).read_bytes()
        receipt["installed_source"] = installed_identity
        receipt["installed_environment"] = probe
        cli = str(environment_root / "bin/selcal")
        csv, config = "examples/workflow/series.csv", "examples/workflow/pearson.json"
        commands = [
            ("readme_validate", ["validate", csv, config]),
            ("readme_run", ["run", csv, config, "run.sqlite", "--max-bytes", "1048576"]),
            ("readme_verify", ["verify", "run.sqlite", "--max-bytes", "1048576"]),
            ("readme_replay", ["verify", "run.sqlite", "--max-bytes", "1048576", "--replay"]),
            ("readme_report", ["report", "run.sqlite", "report.html", "--max-bytes", "1048576"]),
            ("readme_doctor", ["doctor"]),
        ]
        for label, arguments in commands:
            row = run(label, [cli, *arguments])
            payload = row["stdout_json"]
            assert payload["exit_code"] == 0 and payload["error"] is None
            if label in {"readme_run", "readme_verify", "readme_replay", "readme_report"}:
                assert payload["data"]["p_value"] == 0.2
                assert payload["data"]["retained_replicates"] == 9
            if label == "readme_replay":
                assert payload["data"]["replay"] == "MATCH"
        for example in ("basic_selection_aware_calibration", "fail_closed_not_evaluable", "binned_nette_block_shuffle"):
            row = run("example_" + example, [python, "examples/" + example + ".py"])
            if example == "fail_closed_not_evaluable":
                assert row["stdout_json"]["status"] == "not_evaluable"
                assert row["stdout_json"]["failure_stage"] == "null_bind"
                assert row["stdout_json"]["p_value"] is None
        for action in ("save", "read"):
            row = run("example_result_" + action, [python, "examples/save_and_read_result.py", action, "result.json", "--max-bytes", "65536"])
            assert row["stdout_json"]["p_value"] == 0.2
            assert row["stdout_json"]["retained_replicates"] == 9
            assert row["stdout_json"]["verification_scope"] == "content_only_not_replay"
        # Re-express the shipped fail_closed_not_evaluable.py example as public
        # workflow input/config; no additional scientific case is introduced.
        (workspace / "not_evaluable.csv").write_text("x,y\n0,4\n1,3\n2,2\n3,1\n4,0\n", encoding="utf-8")
        not_evaluable = json.loads((workspace / config).read_text())
        not_evaluable["plan"].update({"candidates": [1, 3], "selection_rule": "max_upper", "null_params": {"min_shift": 3}, "replicates": 7})
        (workspace / "not_evaluable.json").write_text(json.dumps(not_evaluable, indent=2) + "\n", encoding="utf-8")
        receipt["not_evaluable_fixture_provenance"] = {"derived_from_shipped_example": "examples/fail_closed_not_evaluable.py", "source_example": artifact(workspace / "examples/fail_closed_not_evaluable.py"), "change": "Same arrays and PlanRequestV2 values expressed as CSV and workflow JSON."}
        ne_commands = [
            ("not_evaluable_run", ["run", "not_evaluable.csv", "not_evaluable.json", "not_evaluable.sqlite", "--max-bytes", "1048576"]),
            ("not_evaluable_verify", ["verify", "not_evaluable.sqlite", "--max-bytes", "1048576"]),
            ("not_evaluable_replay", ["verify", "not_evaluable.sqlite", "--max-bytes", "1048576", "--replay"]),
            ("not_evaluable_report", ["report", "not_evaluable.sqlite", "not_evaluable.html", "--max-bytes", "1048576"]),
        ]
        for label, arguments in ne_commands:
            row = run(label, [cli, *arguments], expected=7)
            payload = row["stdout_json"]
            assert payload["outcome"] == "NOT_EVALUABLE" and payload["error"] is None
            data = payload["data"]
            assert data["status"] == "not_evaluable" and data["failure_stage"] == "null_bind"
            assert data["p_value"] is None and data["reject_null"] is None
            assert data["retained_replicates"] == 0
            if label == "not_evaluable_replay":
                assert data["replay"] == "MATCH"
        assert identity(ROOT / "src/selcal") == checkout_before, "Checkout source changed during verification"
        receipt["checkout_source_after"] = identity(ROOT / "src/selcal")
        preserved = [(sdist, "installed_source_sdist.tar.gz"), (wheel, "installed_sibling_wheel.whl")]
        for name in ("run.sqlite", "report.html", "result.json", "not_evaluable.csv", "not_evaluable.json", "not_evaluable.sqlite", "not_evaluable.html"):
            preserved.append((workspace / name, "installed_" + name))
        for origin, name in preserved:
            destination = EVIDENCE / name.replace("installed_", "installed" + artifact_prefix + "_", 1)
            assert not destination.exists(), "Existing evidence must not be overwritten"
            shutil.copyfile(origin, destination)
            assert destination.read_bytes() == origin.read_bytes()
            receipt["artifacts"].append({**artifact(destination), "copied_from": str(origin)})
        receipt["input_artifacts"] = [artifact(path) for path in sorted((workspace / "examples").rglob("*")) if path.is_file()]
        receipt["summary"] = {"readme_commands_passed": 6, "python_example_files_passed": 4, "python_example_processes_passed": 5, "not_evaluable_expected_exit_7_commands": 4, "installed_sources_byte_identical": 39, "full_pytest_executed": False}
        receipt["status"] = "PASS_LOCAL_INSTALLED_SDIST_USER_FLOWS"
    except Exception as error:
        receipt["status"] = "FAIL"
        receipt["failure"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        receipt["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "receipt": str(receipt_path), "failure": receipt.get("failure"), "summary": receipt.get("summary")}, ensure_ascii=False))
    return 0 if receipt["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
