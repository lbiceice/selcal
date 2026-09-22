"""Clean-install acceptance: build, install from the artifact only, run the full file workflow.

For each requested Python version: fresh venv, install the built wheel (dependencies from the
index), then outside the repository run validate -> run -> verify -> verify --replay -> report ->
doctor on the published example (sampling null) and on an exact-enumeration variant, plus one
refused plan. The sdist is installed once as well. Writes a JSON receipt next to this script.
"""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PYTHONS = ("3.11", "3.12", "3.13")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sh(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)


def cli(python: Path, work: Path, *args: str) -> dict:
    done = sh([str(python), "-m", "selcal", *args], cwd=work)
    try:
        payload = json.loads(done.stdout.strip().splitlines()[-1]) if done.stdout.strip() else None
    except json.JSONDecodeError:
        payload = None
    return {"args": list(args), "exit": done.returncode, "outcome": payload and payload["outcome"],
            "error": payload and payload["error"], "data": payload and payload["data"],
            "stderr_tail": done.stderr.strip()[-300:]}


def workflow_checks(python: Path, work: Path) -> dict:
    example = ROOT / "examples" / "workflow"
    shutil.copy(example / "series.csv", work / "series.csv")
    shutil.copy(example / "pearson.json", work / "pearson.json")
    exact = json.loads((example / "pearson.json").read_text())
    exact["plan"].update(null_name="circular_shift_exact_v1", replicates=99)
    (work / "exact.json").write_text(json.dumps(exact))
    refused = json.loads((example / "pearson.json").read_text())
    refused["plan"].update(candidates=list(range(1, 9)), replicates=199)
    (work / "refused.json").write_text(json.dumps(refused))
    mb = "1048576"
    steps = {}
    for label, config in (("sampling", "pearson.json"), ("exact", "exact.json")):
        record, report = f"{label}.sqlite", f"{label}.html"
        steps[label] = [
            cli(python, work, "validate", "series.csv", config),
            cli(python, work, "run", "series.csv", config, record, "--max-bytes", mb),
            cli(python, work, "verify", record, "--max-bytes", mb),
            cli(python, work, "verify", record, "--max-bytes", mb, "--replay"),
            cli(python, work, "report", record, report, "--max-bytes", mb),
        ]
        steps[label].append({"report_exists": (work / report).is_file(),
                             "report_bytes": (work / report).stat().st_size
                             if (work / report).is_file() else 0})
    steps["refused"] = [
        cli(python, work, "validate", "series.csv", "refused.json"),
        cli(python, work, "run", "series.csv", "refused.json", "refused.sqlite", "--max-bytes", mb),
        {"record_absent": not (work / "refused.sqlite").exists()},
    ]
    steps["doctor"] = cli(python, work, "doctor")
    return steps


def expectations(steps: dict) -> list[str]:
    problems = []
    for label in ("sampling", "exact"):
        validate, run, verify, replay, report, files = steps[label]
        if validate["exit"] != 0 or validate["data"]["preflight"]["plan"]["status"] != "EXECUTABLE":
            problems.append(f"{label}: validate")
        if run["exit"] != 0 or run["outcome"] != "COMPLETE":
            problems.append(f"{label}: run")
        if verify["exit"] != 0 or replay["exit"] != 0 or replay["data"]["replay"] != "MATCH":
            problems.append(f"{label}: verify/replay")
        if report["exit"] != 0 or not files["report_exists"]:
            problems.append(f"{label}: report")
    validate, run, absent = steps["refused"]
    if validate["exit"] != 2 or validate["outcome"] != "PLAN_NOT_EXECUTABLE":
        problems.append("refused: validate")
    if run["exit"] != 2 or run["error"] != "unattainable_plan" or not absent["record_absent"]:
        problems.append("refused: run")
    if steps["doctor"]["exit"] != 0:
        problems.append("doctor")
    return problems


def main() -> None:
    scratch = Path(tempfile.mkdtemp(prefix="selcal-acceptance-"))
    dist = scratch / "dist"
    build = sh(["uv", "build", "--out-dir", str(dist)], cwd=ROOT)
    if build.returncode != 0:
        raise SystemExit(build.stderr)
    wheel = next(dist.glob("*.whl"))
    sdist = next(dist.glob("*.tar.gz"))
    receipt: dict = {
        "schema": "selcal.clean-install-acceptance.v1",
        "script_sha256": sha256(Path(__file__)),
        "host": {"platform": platform.platform(), "machine": platform.machine()},
        "artifacts": {wheel.name: sha256(wheel), sdist.name: sha256(sdist)},
        "runs": [],
    }
    installs = [(version, wheel) for version in PYTHONS] + [("3.13", sdist)]
    for version, artifact in installs:
        env = scratch / f"env-{version}-{artifact.suffix.strip('.')}"
        created = sh(["uv", "venv", "-q", "--python", version, str(env)])
        installed = sh(["uv", "pip", "install", "-q", "--python", str(env / "bin" / "python"),
                        str(artifact)])
        python = env / "bin" / "python"
        entry = {"python_requested": version, "artifact": artifact.name,
                 "venv_exit": created.returncode, "install_exit": installed.returncode,
                 "install_stderr_tail": installed.stderr.strip()[-300:]}
        if installed.returncode == 0:
            probe = sh([str(python), "-c",
                        "import sys, numpy, selcal; print(sys.version.split()[0], numpy.__version__,"
                        " selcal.__version__, 'site-packages' in selcal.__file__)"])
            python_version, numpy_version, selcal_version, from_site = probe.stdout.split()
            entry["runtime"] = {"python": python_version, "numpy": numpy_version,
                                "selcal": selcal_version}
            entry["imports_from_site_packages"] = from_site == "True"
            work = scratch / f"work-{version}-{artifact.suffix.strip('.')}"
            work.mkdir()
            steps = workflow_checks(python, work)
            entry["problems"] = expectations(steps)
            entry["summary"] = {
                label: [(s.get("args", [""])[0], s.get("exit"), s.get("outcome"), s.get("error"))
                        for s in steps[label] if "args" in s]
                for label in ("sampling", "exact", "refused")
            }
            entry["p_values"] = {label: steps[label][1]["data"] and steps[label][1]["data"]["p_value"]
                                 for label in ("sampling", "exact")}
        receipt["runs"].append(entry)
        print(version, artifact.name, entry.get("runtime"), entry.get("problems"), flush=True)
    receipt["all_passed"] = all(run.get("problems") == [] for run in receipt["runs"])
    (HERE / "clean_install_acceptance_receipt.json").write_text(json.dumps(receipt, indent=1) + "\n")
    print("ALL_PASSED" if receipt["all_passed"] else "PROBLEMS_FOUND")


if __name__ == "__main__":
    main()
