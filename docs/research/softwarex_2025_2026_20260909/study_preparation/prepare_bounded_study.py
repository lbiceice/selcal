"""Prepare fixed bounded-study inputs; importing this module executes no study."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np

CELL_BUDGETS = {"iid_null": 400, "circular_ma2_null": 400, "lag2_rho03": 200, "lag2_rho06": 200}
ROLES = ("z", "w", "epsilon", "null")
DOMAIN = "SelCal/bounded-pearson/preparation-v1"
ROOT = Path(__file__).absolute().parents[4]


def seed_hex(phase: str, cell_id: str, dataset_index: int, role: str) -> str:
    """Domain-separated provenance; unequal seeds do not prove independence."""
    if type(phase) is not str or phase not in ("development", "study"):
        raise ValueError("phase must be development or study")
    if type(cell_id) is not str or cell_id not in CELL_BUDGETS:
        raise ValueError("unknown cell_id")
    if type(role) is not str or role not in ROLES:
        raise ValueError("unknown role")
    if type(dataset_index) is not int or not 0 <= dataset_index < CELL_BUDGETS[cell_id]:
        raise ValueError("dataset_index must be a built-in int within the cell budget")
    return hashlib.sha256(
        f"{DOMAIN}|{phase}|{cell_id}|{dataset_index}|{role}".encode("ascii")
    ).hexdigest()


def make_pair(
    cell_id: str, dataset_index: int, *, phase: str = "development"
) -> tuple[np.ndarray, np.ndarray]:
    """Draw one fixed pair. The preparation CLI never calls this function."""

    def innovation(role: str) -> np.ndarray:
        seed = int(seed_hex(phase, cell_id, dataset_index, role), 16)
        return np.random.Generator(np.random.PCG64(seed)).standard_normal(64)

    z = innovation("z")
    if cell_id == "iid_null":
        return z, innovation("w")
    if cell_id == "circular_ma2_null":
        w = innovation("w")
        x = (z + 0.6 * np.roll(z, 1) + 0.3 * np.roll(z, 2)) / math.sqrt(1.45)
        y = (w + 0.6 * np.roll(w, 1) + 0.3 * np.roll(w, 2)) / math.sqrt(1.45)
        return x, y
    rho = 0.3 if cell_id == "lag2_rho03" else 0.6
    return z, rho * np.roll(z, 2) + math.sqrt(1 - rho * rho) * innovation("epsilon")


def _identities() -> dict:
    source_root = ROOT / "src"
    if source_root.is_symlink() or not source_root.is_dir():
        raise ValueError("src must be a regular directory")
    source_entries = sorted(source_root.rglob("*"))
    if any(path.is_symlink() for path in source_entries):
        raise ValueError("source identities must not contain symlinks")
    sources = [path for path in source_entries if path.suffix == ".py"]
    if len(sources) != 39:
        raise ValueError("expected all 39 production Python source files")
    script = Path(__file__).absolute()
    paths = [
        script,
        script.parent.parent / "bounded_study_criterion_amendment.md",
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        *sources,
    ]
    identities = {}
    for path in paths:
        lineage = [
            path,
            *(parent for parent in path.parents if parent == ROOT or ROOT in parent.parents),
        ]
        if any(part.is_symlink() for part in lineage) or not path.is_file():
            raise ValueError(
                f"identity must be a regular non-symlink file: {path.relative_to(ROOT)}"
            )
        raw = path.read_bytes()
        identities[path.relative_to(ROOT).as_posix()] = {
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
    return identities


def build_schedule() -> dict:
    """Build provenance only: no normal draws, calibration, or evaluation."""
    identities = _identities()
    rows, digests, roots = [], set(), set()
    for cell_id, budget in CELL_BUDGETS.items():
        for dataset_index in range(budget):
            streams = {role: seed_hex("study", cell_id, dataset_index, role) for role in ROLES}
            root_seed = int(streams["null"][:16], 16)
            for digest in streams.values():
                if digest in digests:
                    raise ValueError("stream digest collision; preparation stopped")
                digests.add(digest)
            if root_seed in roots:
                raise ValueError("root_seed collision; preparation stopped")
            roots.add(root_seed)
            rows.append(
                {
                    "cell_id": cell_id,
                    "dataset_index": dataset_index,
                    "stream_sha256": streams,
                    "root_seed": root_seed,
                }
            )
    formulas = [
        "x = z; y = w",
        "x_t = (z_t + 0.6*z_((t-1)%64) + 0.3*z_((t-2)%64))/sqrt(1.45); y uses w",
        "x = z; y_t = 0.3*z_((t-2)%64) + sqrt(1-0.3*0.3)*epsilon_t",
        "x = z; y_t = 0.6*z_((t-2)%64) + sqrt(1-0.6*0.6)*epsilon_t",
    ]
    return {
        "schema": "selcal.bounded-study-preparation.v1",
        "status": "PREPARED_NOT_EXECUTED",
        "study_executed": False,
        "execution_authorized": False,
        "study_data_generated": False,
        "parameters": {
            "n": 64,
            "candidates": [1, 2],
            "common_target_window": [2, 63],
            "statistic_name": "lagged_pearson_v1",
            "statistic_params": {},
            "selection_rule": "max_upper",
            "null_name": "circular_shift_v2",
            "null_params": {"min_shift": 1},
            "replicates": 199,
            "alpha": 0.05,
            "tie_tolerance": 0.0,
            "tail_comparison": ">=",
            "p_formula": "(1 + E) / 200",
            "rejection_rule": "p <= 0.05",
        },
        "cells": [
            {"cell_id": cell, "budget": budget, "formula": formula}
            for (cell, budget), formula in zip(CELL_BUDGETS.items(), formulas, strict=True)
        ],
        "generation": {
            "bit_generator": "PCG64",
            "distribution": "standard_normal",
            "draw_shape": [64],
            "dtype": "float64",
            "innovation_order_by_cell": {
                "iid_null": ["z", "w"],
                "circular_ma2_null": ["z", "w"],
                "lag2_rho03": ["z", "epsilon"],
                "lag2_rho06": ["z", "epsilon"],
            },
            "seed_derivation": (
                "sha256(ascii('SelCal/bounded-pearson/preparation-v1|{phase}|{cell_id}|"
                "{dataset_index}|{role}')).hexdigest()"
            ),
            "root_seed_derivation": "int(null_digest[:16], 16)",
            "null_digest_role": "preparation provenance, not production replicate seed",
            "independence_claim": "domain separation does not prove independence",
        },
        "environment": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "numpy_version": np.__version__,
            "platform": platform.platform(),
        },
        "identities": identities,
        "rows": rows,
    }


def write_schedule(output: Path) -> None:
    """Validate fully before exclusive creation; never create a missing parent."""
    payload = json.dumps(build_schedule(), sort_keys=True, indent=2, allow_nan=False) + "\n"
    with output.open("x", encoding="utf-8") as stream:
        stream.write(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        write_schedule(args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Preparation refused: {exc}\n")
    print("PREPARED_NOT_EXECUTED rows=1200")


if __name__ == "__main__":
    main()
