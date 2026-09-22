"""Stage 2: C2 Bonferroni comparator (re-implementation) and the frozen decision rules.

`c2` computes the comparator; `analyse` merges it with the production chunks and applies the
pre-registered ADOPT / REFUSE-ONLY rule. Imports no SelCal module.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy import stats

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "stage2_inputs"
RESULTS = HERE / "stage2_results"
NULL_CELLS = ("iid", "ma2", "ar1")


def cp(k: int, n: int) -> tuple[float, float]:
    lo = 0.0 if k == 0 else float(stats.beta.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(0.975, k + 1, n - k))
    return lo, hi


def bonferroni(x: np.ndarray, y: np.ndarray, L: int) -> bool:
    n = x.size
    ps = [float(stats.pearsonr(x[L - c : n - c], y[L:], alternative="greater").pvalue)
          for c in range(1, L + 1)]
    return min(1.0, L * min(ps)) <= 0.05


def c2() -> None:
    out = {}
    for n in (64, 256):
        for cell in NULL_CELLS:
            data = np.load(INPUTS / f"{cell}_n{n}.npz")
            for L in (2, 8):
                out[f"C2|{cell}|rho-|L{L}|n{n}"] = [
                    bonferroni(x, y, L) for x, y in zip(data["source"], data["target"], strict=True)
                ]
        for rho in ("0.3", "0.6"):
            for L in (2, 8):
                data = np.load(INPUTS / f"alt_rho{rho}_L{L}_n{n}.npz")
                out[f"C2|alt|rho{rho}|L{L}|n{n}"] = [
                    bonferroni(x, y, L) for x, y in zip(data["source"], data["target"], strict=True)
                ]
    (HERE / "results_stage2_c2.json").write_text(json.dumps({
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                        "scipy": scipy.__version__},
        "decisions": out}) + "\n")
    print("C2 done", len(out))


def mcnemar(a: list[bool], b: list[bool]) -> dict:
    only_a = sum(1 for u, v in zip(a, b, strict=True) if u and not v)
    only_b = sum(1 for u, v in zip(a, b, strict=True) if v and not u)
    m = only_a + only_b
    return {"first_only": only_a, "second_only": only_b,
            "exact_two_sided_p": 1.0 if m == 0 else float(stats.binomtest(only_a, m, 0.5).pvalue)}


def analyse() -> None:
    decisions: dict[str, list[bool]] = {}
    non_complete = []
    chunks = sorted(RESULTS.glob("*.json"))
    assert len(chunks) == 448, len(chunks)
    grouped: dict[str, dict[int, list[bool]]] = {}
    for path in chunks:
        chunk = json.loads(path.read_text())
        key = f"{chunk['arm']}|{chunk['cell']}|rho{chunk['rho']}|L{chunk['L']}|n{chunk['n']}"
        grouped.setdefault(key, {})[chunk["start"]] = chunk["decisions"]
        non_complete += [{**note, "key": key} for note in chunk["non_complete"]]
    for key, parts in grouped.items():
        decisions[key] = [d for start in sorted(parts) for d in parts[start]]
    decisions.update(json.loads((HERE / "results_stage2_c2.json").read_text())["decisions"])

    table = {}
    for key, values in sorted(decisions.items()):
        k, r = sum(values), len(values)
        lo, hi = cp(k, r)
        table[key] = {"K": k, "R": r, "rate": k / r, "cp95_low": lo, "cp95_high": hi}

    a1 = [{"key": f"C1|{cell}|rho-|L{L}|n{n}", **table[f"C1|{cell}|rho-|L{L}|n{n}"]}
          for n in (64, 256) for cell in NULL_CELLS for L in (2, 8)]
    a1_ok = all(row["cp95_high"] <= 0.065 for row in a1)
    a2 = table["C1|alt|rho0.6|L8|n64"]
    a2_ok = a2["rate"] >= 0.80
    paired = {
        f"C1_vs_C2|rho{rho}|L{L}|n{n}": mcnemar(decisions[f"C1|alt|rho{rho}|L{L}|n{n}"],
                                               decisions[f"C2|alt|rho{rho}|L{L}|n{n}"])
        for n in (64, 256) for rho in ("0.3", "0.6") for L in (2, 8)
    }
    verdict = {"A1_C1_size_cp_upper_le_065": {"rows": a1, "ok": a1_ok},
               "A2_C1_power_rho06_L8_n64": {**a2, "ok": a2_ok},
               "decision": "ADOPT_BLOCK_SHUFFLE_FALLBACK" if a1_ok and a2_ok else "REFUSE_ONLY",
               "non_complete_runs": non_complete}
    (HERE / "results_stage2_analysis.json").write_text(json.dumps(
        {"table": table, "paired_C1_vs_C2": paired, "verdict": verdict}, indent=1) + "\n")
    for key, row in table.items():
        print(f"{key:28} {row['K']:>5}/{row['R']:<5} {row['rate']:.4f} "
              f"{row['cp95_low']:.4f}-{row['cp95_high']:.4f}")
    print(json.dumps({k: v for k, v in verdict.items() if k != "A1_C1_size_cp_upper_le_065"}, indent=1))
    print("A1 ok:", a1_ok, [(r["key"], round(r["cp95_high"], 4)) for r in a1 if r["cp95_high"] > 0.065])


if __name__ == "__main__":
    {"c2": c2, "analyse": analyse}[sys.argv[1]]()
