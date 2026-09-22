"""Stage 1 re-implementation arms C1r (block sanity), C2 (Bonferroni), C3 (randomized ties).

Imports no SelCal module. See protocol_stage1.md.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from math import factorial
from pathlib import Path

import numpy as np
import scipy
from scipy import stats

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent / "bounded_study_execution_20260909" / "study_v1"
CELLS = {"iid_null": 400, "circular_ma2_null": 400, "lag2_rho03": 200, "lag2_rho06": 200}
N, ALPHA, LS, B, BLOCK = 64, 0.05, (2, 4, 8), 199, 8


def seed(cell: str, index: int, arm: str, L: int) -> int:
    tag = f"SelCal/remedy-confirm-v1|{cell}|{index}|{arm}|L{L}"
    return int(hashlib.sha256(tag.encode("ascii")).hexdigest()[:16], 16)


def load(cell: str, index: int) -> tuple[np.ndarray, np.ndarray]:
    raw = json.loads((STUDY / "inputs" / f"{cell}_{index:04d}.json").read_text())
    return (
        np.array([float.fromhex(v) for v in raw["source_hex"]]),
        np.array([float.fromhex(v) for v in raw["target_hex"]]),
    )


def max_stat(x: np.ndarray, y: np.ndarray, lags: tuple[int, ...]) -> float:
    top = max(lags)
    fut = y[top:]
    return max(float(np.corrcoef(x[top - c : N - c], fut)[0, 1]) for c in lags)


def block_shuffled(x: np.ndarray, order: np.ndarray) -> np.ndarray:
    return np.concatenate([x[i * BLOCK : (i + 1) * BLOCK] for i in order])


def main() -> None:
    decisions: dict[str, list[bool]] = {}
    started = time.monotonic()
    blocks = N // BLOCK
    assert factorial(blocks) > B
    for L in LS:
        lags = tuple(range(1, L + 1))
        for cell, budget in CELLS.items():
            c1r, c2, c3 = [], [], []
            for index in range(budget):
                x, y = load(cell, index)
                observed = max_stat(x, y, lags)

                rng = np.random.Generator(np.random.PCG64(seed(cell, index, "C1r", L)))
                exceed = 0
                for _ in range(B):
                    order = rng.permutation(blocks)
                    exceed += max_stat(block_shuffled(x, order), y, lags) >= observed
                c1r.append((1 + exceed) / (B + 1) <= ALPHA)

                top = max(lags)
                per_lag = [
                    float(
                        stats.pearsonr(
                            x[top - c : N - c], y[top:], alternative="greater"
                        ).pvalue
                    )
                    for c in lags
                ]
                c2.append(min(1.0, L * min(per_lag)) <= ALPHA)

                states = np.array(
                    [max_stat(x[(np.arange(N) - s) % N], y, lags) for s in range(N)]
                )
                greater = int(np.sum(states > observed))
                equal = int(np.sum(states == observed))
                draw = np.random.Generator(
                    np.random.PCG64(seed(cell, index, "C3", L))
                ).uniform(0.0, 1.0)
                u = 1.0 - draw  # Unif(0, 1]
                c3.append((greater + u * equal) / N <= ALPHA)
            for arm, values in (("C1r", c1r), ("C2", c2), ("C3", c3)):
                decisions[f"{arm}|L{L}|{cell}"] = values
                print(f"{arm}|L{L}|{cell}", sum(values), "/", budget, flush=True)
    payload = {
        "schema": "selcal.remedy-confirm-stage1-reimplementation.v1",
        "protocol_sha256": hashlib.sha256((HERE / "protocol_stage1.md").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "elapsed_seconds": time.monotonic() - started,
        "decisions": decisions,
    }
    (HERE / "results_stage1_reimplementation.json").write_text(json.dumps(payload, indent=1) + "\n")


if __name__ == "__main__":
    main()
