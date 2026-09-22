"""Exploratory E2 (see exploratory_E2_plan.md). Re-implementation only; imports no SelCal module."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

from run_comparator_arms import ALPHA, B, CELLS, N, NULL_CELLS, circular_states, cp, lagged_r, load, seed

HERE = Path(__file__).resolve().parent


def main() -> None:
    out = {"floor": [], "variant": []}
    for L in (2, 4, 8):
        ls = tuple(range(1, L + 1))
        for cell in CELLS:
            budget = 400 if cell in NULL_CELLS else 200
            never, min_p = 0, 1.0
            k = {"A2": 0, "A5": 0, "V": 0}
            for i in range(budget):
                x, y, _ = load(cell, i)
                r = lagged_r(x, y, ls)
                sel = int(np.argmax(r))
                obs = float(r[sel])
                states = circular_states(x)
                allmax = np.array([np.max(lagged_r(states[s], y, ls)) for s in range(N)])
                # Exact min_shift=1 enumeration: all 64 states incl. identity, >= tail.
                p_exact = int(np.sum(allmax >= obs)) / N
                floor_i = int(np.sum(allmax[: L + 1] >= obs)) / N
                min_p = min(min_p, p_exact)
                never += floor_i > ALPHA
                p1 = float(stats.pearsonr(x[L - ls[sel] : N - ls[sel]], y[L:],
                                          alternative="greater").pvalue)
                k["A2"] += min(1.0, L * p1) <= ALPHA
                rng = np.random.Generator(np.random.PCG64(seed(cell, i, f"E2-L{L}")))
                s_old = rng.integers(0, N, size=B)
                k["A5"] += (1 + int(np.sum(allmax[s_old] >= obs))) / (B + 1) <= ALPHA
                s_new = rng.integers(L, N - L + 1, size=B)
                k["V"] += (1 + int(np.sum(allmax[s_new] >= obs))) / (B + 1) <= ALPHA
            out["floor"].append({"L": L, "cell": cell, "R": budget,
                                 "inputs_that_can_never_reject_exact": never,
                                 "min_exact_p": min_p})
            for arm, kk in k.items():
                lo, hi = cp(int(kk), budget)
                out["variant"].append({"L": L, "cell": cell, "arm": arm, "K": int(kk),
                                       "R": budget, "rate": kk / budget,
                                       "cp95_low": lo, "cp95_high": hi})
            print(L, cell, k, "never", never, file=sys.stderr)
    out["plan_sha256"] = hashlib.sha256((HERE / "exploratory_E2_plan.md").read_bytes()).hexdigest()
    out["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE / "results_E2.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
