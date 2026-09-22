"""Build the public SelCal release tree (GitHub + Zenodo) from the working tree.

Usage: python scripts/build_public_release.py OUTPUT_DIR

Copies every git-tracked or explicitly listed release file, minus internal process
material (planning notes, internal review registries, retired gates, unpublished
manuscript drafts, correspondence drafts). Writes RELEASE_MANIFEST.tsv (path, bytes,
sha256) and EXCLUDED.tsv (pattern, reason) into OUTPUT_DIR.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXTRA_FILES = ("LICENSE.txt", "Licence.txt", "CITATION.cff", ".zenodo.json")

# Paths inside excluded areas that tests read. All are English registries, gate documents or
# code, with no local paths or correspondence (same pattern syntax as EXCLUDE).
KEEP = (
    "docs/superpowers/specs/task10/*",
    "docs/superpowers/specs/idl/*",
    "docs/superpowers/specs/fixtures/*",
    "docs/superpowers/*/*task10*",
    "docs/research/softwarex_2025_2026_20260909/study_preparation/prepare_bounded_study.py",
    "docs/status/softwarex_readiness_20260831.md",
)

EXCLUDE: tuple[tuple[str, str], ...] = (
    ("docs/superpowers/*", "internal design and implementation plans"),
    ("docs/research/*", "internal literature notes; third-party PDFs are not redistributable"),
    ("docs/status/p3_*", "internal project status notes"),
    ("docs/status/softwarex_*", "internal submission-readiness notes"),
    ("docs/status/parallel_module_*", "internal work-dispatch notes"),
    ("docs/status/retired_task10_gate_*", "internal note on the retired gate"),
    ("docs/status/evidence/authorship_*", "internal authorship planning"),
    ("docs/status/evidence/continuation_*", "internal milestone evidence, superseded"),
    ("docs/status/evidence/issue_closure_*", "internal milestone evidence, superseded"),
    ("docs/status/evidence/value_replay_*", "internal milestone evidence, superseded"),
    ("docs/status/evidence/real_task_entry_*", "internal milestone evidence, superseded"),
    ("docs/status/evidence/study_preparation_*", "internal milestone evidence, superseded"),
    ("docs/status/evidence/bounded_study_execution_*", "internal milestone evidence, superseded"),
    ("docs/status/evidence/real_case_search_*", "internal search log with local paths"),
    ("docs/status/evidence/real_case_*/author_contact_DRAFT.md", "private correspondence draft"),
    ("docs/manuscript/*.md", "unpublished manuscript drafts and internal reviews"),
    ("docs/manuscript/check_numbers_v*.py", "checks the unpublished draft text"),
)


def _regex(pattern: str) -> re.Pattern[str]:
    """``*`` matches within one path segment; a match on a directory covers its contents."""
    return re.compile("[^/]*".join(re.escape(part) for part in pattern.split("*")))


def _matches(pattern: str, path: str) -> bool:
    parts = path.split("/")
    rx = _regex(pattern.removesuffix("/*"))
    return any(rx.fullmatch("/".join(parts[: i + 1])) for i in range(len(parts)))


def excluded(path: str) -> str | None:
    if any(_matches(keep, path) for keep in KEEP):
        return None
    for pattern, _reason in EXCLUDE:
        if _matches(pattern, path):
            return pattern
    return None


def main() -> None:
    out = Path(sys.argv[1]).resolve()
    if out.exists():
        raise SystemExit(f"refusing to overwrite existing {out}")
    tracked = (
        subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
        .stdout.decode()
        .split("\0")
    )
    paths = sorted({p for p in tracked if p} | set(EXTRA_FILES))
    kept, dropped = [], {}
    for rel in paths:
        if not (ROOT / rel).is_file():
            continue
        hit = excluded(rel)
        if hit:
            dropped[hit] = dropped.get(hit, 0) + 1
            continue
        kept.append(rel)
    for rel in kept:
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    with (out / "RELEASE_MANIFEST.tsv").open("w", encoding="utf-8") as fh:
        fh.write("path\tbytes\tsha256\n")
        for rel in kept:
            data = (ROOT / rel).read_bytes()
            fh.write(f"{rel}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}\n")
    with (out / "EXCLUDED.tsv").open("w", encoding="utf-8") as fh:
        fh.write("pattern\tfiles\treason\n")
        for pattern, reason in EXCLUDE:
            fh.write(f"{pattern}\t{dropped.get(pattern, 0)}\t{reason}\n")
    print(f"kept {len(kept)} files; excluded {sum(dropped.values())}")


if __name__ == "__main__":
    main()
