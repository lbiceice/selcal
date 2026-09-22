from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DOCS_SOURCE = REPOSITORY_ROOT / "docs" / "api"


def test_sphinx_documentation_builds_without_warnings_and_lists_public_api(
    tmp_path: Path,
) -> None:
    pyproject = tomllib.loads((REPOSITORY_ROOT / "pyproject.toml").read_text("utf-8"))
    assert pyproject["project"]["optional-dependencies"]["docs"] == ["sphinx>=8.2.3,<9"]

    output = tmp_path / "html"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "--fail-on-warning",
            "--keep-going",
            "-b",
            "html",
            str(DOCS_SOURCE),
            str(output),
        ],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert (output / "index.html").is_file()
    assert (output / "architecture.html").is_file()
    assert (output / "performance.html").is_file()
    assert (output / "usage.html").is_file()

    architecture = (output / "architecture.html").read_text(encoding="utf-8")
    for architecture_marker in (
        "Component boundaries",
        "selcal.contracts_v2",
        "selcal.calibration_v2",
        "Terminal persistence and a thin CLI are implemented",
    ):
        assert architecture_marker in architecture

    performance = (output / "performance.html").read_text(encoding="utf-8")
    for performance_marker in (
        "Benchmark contract",
        "benchmark_in_memory.py --preset standard",
        "in_memory_standard_20260922_figure.svg",
        "single-process characterization",
        "tracemalloc",
    ):
        assert performance_marker in performance

    usage = (output / "usage.html").read_text(encoding="utf-8")
    for usage_marker in (
        "basic_selection_aware_calibration.py",
        "binned_nette_block_shuffle.py",
        "fail_closed_not_evaluable.py",
        "NOT_EVALUABLE",
        "not scientific validation",
    ):
        assert usage_marker in usage

    public_api = (output / "public_api.html").read_text(encoding="utf-8")
    for public_name in (
        "PlanMigrationV1ToV2",
        "PlanRequest",
        "PlanRequestV2",
        "PlanResolution",
        "PlanResolutionV2",
        "ResolvedScientificPlan",
        "ResolvedScientificPlanV2",
        "calibrate_selected_family",
        "migrate_plan_v1_to_v2",
        "resolve_plan",
        "resolve_plan_v2",
        "verify_calibration_result",
        "run_files",
        "read_workflow",
        "report_record",
    ):
        assert public_name in public_api


def test_readme_documents_reproducible_api_reference_build() -> None:
    readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")

    assert 'python -m pip install ".[docs]"' in readme
    assert (
        "python -m sphinx --fail-on-warning --keep-going -b html "
        "docs/api docs/api/_build/html"
    ) in readme
    assert "docs/api/_build/html/index.html" in readme


def test_generated_api_reference_is_excluded_from_version_control() -> None:
    ignore_rules = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

    assert "/docs/api/_build/" in ignore_rules
