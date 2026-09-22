"""Inspect real build outputs without writing build metadata into the checkout.

Repository review tests remain collected in a checkout; their exact exclusions
and dependency reasons are declared in MANIFEST.in and checked against the sdist.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tarfile
import tomllib
import zipfile
from pathlib import Path

import pytest

from scripts.audit_repository_hygiene import _release_surface_paths, audit_repository

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ONLY_TEST_FILES = {
    "tests/test_dependency_licence_evidence.py": "internal dependency evidence and binding",
    "tests/test_scientific_code_smell_audit.py": "internal historical receipts and readiness",
    "tests/test_verifier_complexity_slice_v1.py": "historical verifier receipt and design hashes",
    "tests/_verifier_structure_gate_v1.py": "helper for the historical verifier receipt gate",
    "tests/fixtures/verifier_structure_gate_v1.json": "fixture for the historical verifier gate",
    "tests/test_internal_design_review.py": "internal trusted-call design assertions",
    "tests/task10/test_authority_amendment_scope_v1.py": "internal authority amendment package",
    "tests/task10/test_authority_review_package_v2.py": "internal authority review package v2",
    "tests/task10/test_authority_review_package_v3.py": "internal authority review package v3",
    "tests/task10/test_registry_cross_representation_v1.py": "internal authority registry review",
}


@pytest.fixture(scope="module")
def distributions(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path, Path]:
    workspace = tmp_path_factory.mktemp("distribution-assets")
    source = workspace / "source"
    shutil.copytree(
        ROOT,
        source,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            "__pycache__",
            "*.pyc",
            "*.egg-info",
            ".pytest_cache",
            ".ruff_cache",
            ".mypy_cache",
            "build",
            "dist",
            "_build",
        ),
    )
    output = workspace / "dist"
    completed = subprocess.run(
        [sys.executable, "-m", "build", "--outdir", str(output), str(source)],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    sdists = list(output.glob("*.tar.gz"))
    wheels = list(output.glob("*.whl"))
    assert len(sdists) == len(wheels) == 1
    return source, sdists[0], wheels[0]


def _sdist_files(path: Path) -> dict[str, bytes]:
    with tarfile.open(path, "r:gz") as archive:
        files = {}
        for member in archive.getmembers():
            assert member.isfile() or member.isdir(), f"nonregular sdist member: {member.name}"
            if member.isfile():
                content = archive.extractfile(member)
                assert content is not None
                files[member.name.partition("/")[2]] = content.read()
        return files


def test_sdist_contains_documented_user_assets(distributions: tuple[Path, Path, Path]) -> None:
    source, sdist, _ = distributions
    required = {
        ".gitignore",
        "README.md",
        "pyproject.toml",
        "uv.lock",
        "examples/basic_selection_aware_calibration.py",
        "examples/binned_nette_block_shuffle.py",
        "examples/fail_closed_not_evaluable.py",
        "examples/save_and_read_result.py",
        "scripts/benchmark_in_memory.py",
        "scripts/plot_in_memory_benchmark.py",
        "scripts/m6_pearson_diagnostic.py",
        "scripts/compare_pearson_diagnostic.py",
        "tests/test_public_quality_commands.py",
        "docs/api/conf.py",
        "docs/api/index.rst",
        "docs/api/architecture.rst",
        "docs/api/performance.rst",
        "docs/api/public_api.rst",
        "docs/api/usage.rst",
        "docs/benchmarks/in_memory_standard_20260831.json",
        "docs/benchmarks/in_memory_standard_20260831_figure.svg",
        "docs/benchmarks/in_memory_standard_20260908.json",
        "docs/benchmarks/in_memory_standard_20260908_figure.svg",
        "docs/benchmarks/in_memory_standard_20260908_figure.png",
        "docs/benchmarks/in_memory_standard_20260922.json",
        "docs/benchmarks/in_memory_standard_20260922_figure.svg",
        "docs/benchmarks/in_memory_standard_20260922_figure.png",
    }
    readme = (source / "README.md").read_text(encoding="utf-8")
    required.update(re.findall(r"(?:examples|scripts)/[A-Za-z0-9_./-]+\.py", readme))
    required.update(
        path.relative_to(source).as_posix()
        for path in (source / "examples" / "workflow").glob("*")
        if path.suffix in {".csv", ".json"} and path.is_file()
    )
    files = _sdist_files(sdist)
    assert not (missing := required - files.keys()), f"sdist missing user assets: {sorted(missing)}"
    for name in required:
        assert files[name] == (source / name).read_bytes(), name


def test_sdist_preserves_source_and_test_inputs(distributions: tuple[Path, Path, Path]) -> None:
    source, sdist, _ = distributions
    required = {
        path.relative_to(source).as_posix()
        for directory in (source / "src" / "selcal", source / "tests")
        for path in directory.rglob("*")
        if path.is_file() and path.suffix in {".py", ".json", ".csv"}
    } - REPOSITORY_ONLY_TEST_FILES.keys()
    files = _sdist_files(sdist)
    assert not (missing := required - files.keys()), (
        f"sdist missing source/test files: {sorted(missing)}"
    )
    for name in required:
        assert files[name] == (source / name).read_bytes(), name


def test_distributions_exclude_internal_reviews_and_generated_outputs(
    distributions: tuple[Path, Path, Path],
) -> None:
    _, sdist, wheel = distributions
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist()) | _sdist_files(sdist).keys()
    for name in names:
        assert "docs/superpowers/" not in name, name
        assert "docs/status/" not in name, name
        assert "docs/api/_build/" not in name, name
        assert "__pycache__/" not in name, name
        assert not name.endswith((".pyc", ".pyo", ".DS_Store")), name


def test_repository_only_tests_have_explicit_exclusions_and_remain_in_checkout(
    distributions: tuple[Path, Path, Path],
) -> None:
    source, sdist, _ = distributions
    manifest = (source / "MANIFEST.in").read_text()
    files = _sdist_files(sdist)
    for name, reason in REPOSITORY_ONLY_TEST_FILES.items():
        assert f"# {reason}\nexclude {name}\n" in manifest, name
        assert name not in files, name
        if not (ROOT / name).exists():
            assert not (ROOT / "docs/status").exists(), f"missing checkout evidence: {name}"
        else:
            assert (source / name).read_bytes() == (ROOT / name).read_bytes(), name


def test_sdist_file_inventory_exactly_matches_audited_release_surface(
    distributions: tuple[Path, Path, Path],
) -> None:
    source, sdist, _ = distributions
    files = _sdist_files(sdist)
    # Setuptools-generated metadata is validated by the build and wheel checks.
    generated = {"PKG-INFO", "setup.cfg"} | {
        "src/selcal.egg-info/" + name
        for name in (
            "PKG-INFO",
            "SOURCES.txt",
            "dependency_links.txt",
            "entry_points.txt",
            "requires.txt",
            "top_level.txt",
        )
    }
    selected = {path.relative_to(source).as_posix() for path in _release_surface_paths(source)}
    assert files.keys() - generated == selected
    assert audit_repository(source) == ()


@pytest.mark.parametrize("fault", ["machine_path", "credential", "symlink", "symlink_directory"])
def test_real_sdist_public_asset_faults_are_rejected(
    distributions: tuple[Path, Path, Path],
    tmp_path: Path,
    fault: str,
) -> None:
    _, sdist, _ = distributions
    files = _sdist_files(sdist)
    for name, content in files.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    assert audit_repository(tmp_path) == ()
    public = tmp_path / "docs/api/usage.rst"
    assert public.read_bytes() == files["docs/api/usage.rst"]
    expected_path = "docs/api/usage.rst"
    if fault == "symlink_directory":
        public.parent.rename(tmp_path / "private-api-copy")
        public.parent.symlink_to(tmp_path / "private-api-copy", target_is_directory=True)
        expected = "SYMLINK_IN_RELEASE_SURFACE"
        expected_path = "docs/api"
    elif fault == "symlink":
        public.unlink()
        public.symlink_to(tmp_path / "README.md")
        expected = "SYMLINK_IN_RELEASE_SURFACE"
    else:
        payload = (
            "/" + "Users/example/private/checkout" if fault == "machine_path" else "sk-" + "X" * 32
        )
        public.write_text(payload + "\n", encoding="utf-8")
        expected = "ABSOLUTE_MACHINE_PATH" if fault == "machine_path" else "CREDENTIAL_MATERIAL"
    assert [(row.rule, row.path) for row in audit_repository(tmp_path)] == [
        (expected, expected_path),
    ]


@pytest.mark.parametrize("link_type", [tarfile.SYMTYPE, tarfile.LNKTYPE])
def test_sdist_member_inventory_rejects_archive_links(
    distributions: tuple[Path, Path, Path],
    tmp_path: Path,
    link_type: bytes,
) -> None:
    _, sdist, _ = distributions
    linked = tmp_path / "linked.tar.gz"
    with tarfile.open(sdist, "r:gz") as original, tarfile.open(linked, "w:gz") as mutated:
        for member in original.getmembers():
            mutated.addfile(member, original.extractfile(member) if member.isfile() else None)
        link = tarfile.TarInfo("selcal-0.1.0.dev0/docs/api/linked.rst")
        link.type = link_type
        link.linkname = "usage.rst"
        mutated.addfile(link)
    with pytest.raises(AssertionError, match="nonregular sdist member"):
        _sdist_files(linked)


def test_wheel_from_sdist_preserves_runtime_and_declared_documentation(
    distributions: tuple[Path, Path, Path],
) -> None:
    source, _, wheel = distributions
    pyproject = tomllib.loads((source / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    data_prefix = f"{project['name']}-{project['version']}.data/data/"
    with zipfile.ZipFile(wheel) as archive:
        for path in (source / "src" / "selcal").rglob("*.py"):
            name = path.relative_to(source / "src").as_posix()
            assert archive.read(name) == path.read_bytes(), name
        for destination, paths in pyproject["tool"]["setuptools"]["data-files"].items():
            for relative in paths:
                name = data_prefix + destination + "/" + Path(relative).name
                assert archive.read(name) == (source / relative).read_bytes(), name
