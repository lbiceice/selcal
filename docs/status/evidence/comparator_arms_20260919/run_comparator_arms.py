"""Common-practice comparator arms on the sealed 1,200 study inputs (see protocol.md).

Reads sealed inputs/results read-only; imports no SelCal module; writes only into this directory.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy import stats

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent / "bounded_study_execution_20260909" / "study_v1"
CELLS = ("iid_null", "circular_ma2_null", "lag2_rho03", "lag2_rho06")
NULL_CELLS = ("iid_null", "circular_ma2_null")
B, ALPHA, N = 199, 0.05, 64


def seed(cell: str, index: int, arm: str) -> int:
    tag = f"SelCal/comparator-arms-v1|{cell}|{index}|{arm}"
    return int(hashlib.sha256(tag.encode("ascii")).hexdigest()[:16], 16)


def lagged_r(x: np.ndarray, y: np.ndarray, lags: tuple[int, ...]) -> np.ndarray:
    """r_lag = Pearson(x[t-lag], y[t]) on the common window t = max(lags)..N-1."""
    lo = max(lags)
    fut = y[lo:]
    out = np.empty(len(lags))
    for i, lag in enumerate(lags):
        past = x[lo - lag : N - lag]
        out[i] = np.corrcoef(past, fut)[0, 1]
    return out


def circular_states(x: np.ndarray) -> np.ndarray:
    """Row s is source right-shifted by s: out[t] = x[(t - s) % N]; s = 0..N-1 (0 = identity)."""
    idx = (np.arange(N)[None, :] - np.arange(N)[:, None]) % N
    return x[idx]


def cp(k: int, n: int) -> tuple[float, float]:
    lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
    return float(lo), float(hi)


def mcnemar(a: list[bool], b: list[bool]) -> dict:
    only_a = sum(1 for u, v in zip(a, b) if u and not v)
    only_b = sum(1 for u, v in zip(a, b) if v and not u)
    n = only_a + only_b
    p = 1.0 if n == 0 else float(stats.binomtest(only_a, n, 0.5).pvalue)
    return {"only_first": only_a, "only_second": only_b, "exact_two_sided_p": p}


def load(cell: str, index: int) -> tuple[np.ndarray, np.ndarray, dict]:
    name = f"{cell}_{index:04d}"
    raw = json.loads((STUDY / "inputs" / f"{name}.json").read_text())
    x = np.array([float.fromhex(v) for v in raw["source_hex"]])
    y = np.array([float.fromhex(v) for v in raw["target_hex"]])
    with gzip.open(STUDY / "results" / f"{name}.json.gz") as fh:
        sealed = json.load(fh)
    return x, y, sealed


def ulp_distance(a: float, b: float) -> int:
    ia = np.float64(a).view(np.int64)
    ib = np.float64(b).view(np.int64)
    return abs(int(ia) - int(ib))


def main() -> None:
    lags = (1, 2)
    rows: dict[str, dict[str, list[bool]]] = {c: {} for c in CELLS}
    gate_failures = []
    max_ulp = 0
    for cell in CELLS:
        budget = 400 if cell in NULL_CELLS else 200
        dec = {a: [] for a in ("A0", "A1", "A2", "A3", "A4", "A5")}
        for i in range(budget):
            x, y, sealed = load(cell, i)
            r = lagged_r(x, y, lags)
            sel = int(np.argmax(r))  # first max -> smallest lag
            obs = float(r[sel])
            ref = sealed["comparison"]["observed"]["reference_selection"]
            d = ulp_distance(obs, ref["decision_statistic"])
            max_ulp = max(max_ulp, d)
            if d > 64 or lags[sel] != ref["selected_candidate"]:
                gate_failures.append((cell, i, obs, ref["decision_statistic"], lags[sel]))
            dec["A0"].append(bool(sealed["reject_null"]))

            lo = max(lags)
            p1 = float(stats.pearsonr(x[lo - lags[sel] : N - lags[sel]], y[lo:],
                                      alternative="greater").pvalue)
            dec["A1"].append(p1 <= ALPHA)
            dec["A2"].append(min(1.0, len(lags) * p1) <= ALPHA)

            states = circular_states(x)
            rng3 = np.random.Generator(np.random.PCG64(seed(cell, i, "A3")))
            s3 = rng3.integers(0, N, size=B)
            null3 = np.array([lagged_r(states[s], y, lags)[sel] for s in s3])
            dec["A3"].append((1 + int(np.sum(null3 >= obs))) / (B + 1) <= ALPHA)

            res = stats.permutation_test(
                (x, y), lambda a, b: float(np.max(lagged_r(a, b, lags))),
                permutation_type="pairings", n_resamples=B, alternative="greater",
                vectorized=False, rng=np.random.Generator(np.random.PCG64(seed(cell, i, "A4"))),
            )
            dec["A4"].append(float(res.pvalue) <= ALPHA)

            rng5 = np.random.Generator(np.random.PCG64(seed(cell, i, "A5")))
            s5 = rng5.integers(0, N, size=B)
            null5 = np.array([np.max(lagged_r(states[s], y, lags)) for s in s5])
            dec["A5"].append((1 + int(np.sum(null5 >= obs))) / (B + 1) <= ALPHA)
        rows[cell] = dec
        print(cell, {a: sum(v) for a, v in dec.items()}, file=sys.stderr)

    gate = {"max_ulp": max_ulp, "failures": gate_failures[:20], "n_failures": len(gate_failures)}
    table = []
    for cell in CELLS:
        for arm, v in rows[cell].items():
            k, n = sum(v), len(v)
            lo, hi = cp(k, n)
            table.append({"cell": cell, "arm": arm, "K": k, "R": n, "rate": k / n,
                          "cp95_low": lo, "cp95_high": hi,
                          "miscalibrated": (cell in NULL_CELLS and lo > ALPHA)})
    paired = {c: mcnemar(rows[c]["A0"], rows[c]["A2"]) for c in ("lag2_rho03", "lag2_rho06")}

    # Exploratory E1: null cells only, re-implementation only.
    e1 = []
    for L in (2, 4, 8):
        ls = tuple(range(1, L + 1))
        for cell in NULL_CELLS:
            cnt = {"A1": 0, "A2": 0, "A3": 0, "A5": 0}
            for i in range(400):
                x, y, _ = load(cell, i)
                r = lagged_r(x, y, ls)
                sel = int(np.argmax(r))
                obs = float(r[sel])
                p1 = float(stats.pearsonr(x[L - ls[sel] : N - ls[sel]], y[L:],
                                          alternative="greater").pvalue)
                cnt["A1"] += p1 <= ALPHA
                cnt["A2"] += min(1.0, L * p1) <= ALPHA
                states = circular_states(x)
                rng = np.random.Generator(np.random.PCG64(seed(cell, i, f"E1-L{L}")))
                s = rng.integers(0, N, size=B)
                allr = np.array([lagged_r(states[j], y, ls) for j in s])
                cnt["A3"] += (1 + int(np.sum(allr[:, sel] >= obs))) / (B + 1) <= ALPHA
                cnt["A5"] += (1 + int(np.sum(allr.max(axis=1) >= obs))) / (B + 1) <= ALPHA
            for arm, k in cnt.items():
                lo, hi = cp(int(k), 400)
                e1.append({"L": L, "cell": cell, "arm": arm, "K": int(k), "R": 400,
                           "rate": k / 400, "cp95_low": lo, "cp95_high": hi})
        print("E1 done L", L, file=sys.stderr)

    out = {
        "schema": "selcal.comparator-arms.v1",
        "protocol_sha256": hashlib.sha256((HERE / "protocol.md").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                        "scipy": scipy.__version__},
        "gate": gate,
        "primary": table,
        "paired_A0_vs_A2": paired,
        "exploratory_E1": e1,
        "per_dataset_decisions": {c: rows[c] for c in CELLS},
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("gate", "paired_A0_vs_A2")}, indent=1))


if __name__ == "__main__":
    main()
