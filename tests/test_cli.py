from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "examples" / "workflow" / "series.csv"
CONFIG = ROOT / "examples" / "workflow" / "pearson.json"


def cli(tmp_path, *args):
    return subprocess.run(
        [sys.executable, "-B", "-m", "selcal", *map(str, args)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


def test_actual_cli_run_verify_report_are_fresh_processes(tmp_path):
    checked = cli(tmp_path, "validate", INPUT, CONFIG)
    assert checked.returncode == 0, checked.stderr
    assert len(checked.stdout.splitlines()) == 1
    assert json.loads(checked.stdout)["data"]["sample_count"] == 100
    record = tmp_path / "run.sqlite"
    run = cli(tmp_path, "run", INPUT, CONFIG, record, "--max-bytes", 1048576)
    assert run.returncode == 0, run.stderr
    payload = json.loads(run.stdout)
    assert payload["data"]["p_value"] == 0.015
    assert payload["data"]["planned_replicates"] == 199
    assert payload["data"]["selected_candidate"] == 2
    before = record.read_bytes()
    for flags, expected in (([], "NOT_PERFORMED"), (["--replay"], "MATCH")):
        checked = cli(tmp_path, "verify", record, "--max-bytes", 1048576, *flags)
        assert checked.returncode == 0, checked.stderr
        assert json.loads(checked.stdout)["data"]["replay"] == expected
    report = tmp_path / "report.html"
    rendered = cli(tmp_path, "report", record, report, "--max-bytes", 1048576)
    assert rendered.returncode == 0, rendered.stderr
    assert report.is_file()
    assert record.read_bytes() == before


def test_cli_ne_exit_is_separate_and_record_is_preserved(tmp_path):
    cfg = json.loads(CONFIG.read_text())
    cfg["plan"]["null_params"] = {"min_shift": 51}
    config = tmp_path / "ne.json"
    config.write_text(json.dumps(cfg))
    record = tmp_path / "ne.sqlite"
    result = cli(tmp_path, "run", INPUT, config, record, "--max-bytes", 1048576)
    assert result.returncode == 7, result.stderr
    payload = json.loads(result.stdout)
    assert payload["outcome"] == "NOT_EVALUABLE"
    assert payload["data"]["p_value"] is None
    assert record.is_file()
    checked = cli(tmp_path, "verify", record, "--max-bytes", 1048576, "--replay")
    assert checked.returncode == 7
    assert json.loads(checked.stdout)["data"]["replay"] == "MATCH"


@pytest.mark.parametrize("argument", ["--help", "--version"])
def test_cli_informational_commands(tmp_path, argument):
    result = cli(tmp_path, argument)
    assert result.returncode == 0, result.stderr
    assert result.stdout and "Traceback" not in result.stderr


def test_doctor_does_not_claim_test_or_resume_success(tmp_path):
    result = cli(tmp_path, "doctor")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)["data"]
    assert data["checkpoint_resume"] == "NOT_IMPLEMENTED"
    assert data["scientific_validation"] == "NOT_EXECUTED"


@pytest.mark.parametrize("limit", ["0", "-1", "abc"])
def test_cli_bad_limits_reject_without_traceback_or_output_file(tmp_path, limit):
    record = tmp_path / "absent.sqlite"
    result = cli(tmp_path, "run", INPUT, CONFIG, record, "--max-bytes", limit)
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert not record.exists()


def test_cli_bad_config_and_missing_input_do_not_become_ne(tmp_path):
    config = tmp_path / "bad.json"
    config.write_text("{}")
    result = cli(tmp_path, "validate", INPUT, config)
    assert result.returncode == 2, result.stderr
    assert json.loads(result.stdout)["outcome"] == "INVALID_REQUEST"
    missing = cli(tmp_path, "validate", tmp_path / "missing.csv", CONFIG)
    assert missing.returncode == 4, missing.stderr
    assert json.loads(missing.stdout)["outcome"] == "FAIL"
    assert "Traceback" not in missing.stderr


def test_cli_refuses_to_replace_existing_record(tmp_path):
    record = tmp_path / "user.txt"
    record.write_text("user content")
    result = cli(tmp_path, "run", INPUT, CONFIG, record, "--max-bytes", 1048576)
    assert result.returncode == 4
    assert record.read_text() == "user content"
    assert json.loads(result.stdout)["outcome"] == "FAIL"


def test_cli_entrypoint_declared_in_package():
    import tomllib

    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert project["project"].get("scripts", {}).get("selcal") == "selcal.cli:main"
