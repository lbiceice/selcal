"""Summarise the IDTxl comparator (protocol_idtxl.md) next to SelCal on identical inputs."""

from __future__ import annotations

import json
from pathlib import Path

from scipy import stats

HERE = Path(__file__).resolve().parent


def cp(k: int, n: int) -> tuple[float, float]:
    lo = 0.0 if k == 0 else float(stats.beta.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(0.975, k + 1, n - k))
    return lo, hi


def mcnemar(a: list[bool], b: list[bool]) -> dict:
    only_a = sum(1 for u, v in zip(a, b, strict=True) if u and not v)
    only_b = sum(1 for u, v in zip(a, b, strict=True) if v and not u)
    m = only_a + only_b
    return {"first_only": only_a, "second_only": only_b,
            "exact_two_sided_p": 1.0 if m == 0 else float(stats.binomtest(only_a, m, 0.5).pvalue)}


def collect(folder: str) -> tuple[dict[str, list[bool]], list, dict[str, int]]:
    grouped: dict[str, dict[int, list[bool]]] = {}
    failures, chunks = [], {}
    for path in sorted((HERE / folder).glob("*.json")):
        chunk = json.loads(path.read_text())
        key = f"{chunk['arm']}|{chunk['cell']}|rho{chunk['rho']}|L{chunk['L']}|n{chunk['n']}"
        grouped.setdefault(key, {})[chunk["start"]] = chunk["decisions"]
        failures += [{**f, "key": key} for f in chunk.get("failures", chunk.get("non_complete", []))]
    out = {}
    for key, parts in grouped.items():
        out[key] = [d for start in sorted(parts) for d in parts[start]]
        chunks[key] = len(parts)
    return out, failures, chunks


def main() -> None:
    idtxl, failures, _ = collect("idtxl_results")
    selcal, _, _ = collect("stage2_results")
    expected = {"I1": 4000, "I2": 1000}
    rows, paired = [], {}
    for key, values in sorted(idtxl.items()):
        arm, cell = key.split("|")[:2]
        complete = cell == "alt" and len(values) == 1000 or len(values) == expected[arm]
        k, r = sum(values), len(values)
        lo, hi = cp(k, r)
        rows.append({"key": key, "K": k, "R": r, "rate": k / r, "cp95_low": lo, "cp95_high": hi,
                     "complete": complete})
        if complete:
            for selcal_arm in ("C0", "C1"):
                other = selcal.get(selcal_arm + key[2:])
                if other is not None:
                    paired[f"{arm}_vs_{selcal_arm}|{key[3:]}"] = {
                        **mcnemar(values, other[: len(values)]),
                        "selcal_rate_same_inputs": sum(other[: len(values)]) / len(values)}
    out = {"schema": "selcal.idtxl-comparator-analysis.v1", "rows": rows, "paired": paired,
           "failures": failures}
    (HERE / "results_idtxl_analysis.json").write_text(json.dumps(out, indent=1) + "\n")
    for row in rows:
        flag = "" if row["complete"] else "  (INCOMPLETE)"
        print(f"{row['key']:28} {row['K']:>5}/{row['R']:<5} {row['rate']:.4f} "
              f"{row['cp95_low']:.4f}-{row['cp95_high']:.4f}{flag}")
    print("failures:", len(failures))


if __name__ == "__main__":
    main()
