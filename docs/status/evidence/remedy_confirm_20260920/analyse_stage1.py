"""Apply the frozen Stage 1 decision rules to the two results files. No new computation."""

from __future__ import annotations

import json
from pathlib import Path

from scipy import stats

HERE = Path(__file__).resolve().parent
NULL_CELLS = ("iid_null", "circular_ma2_null")
ALPHA, LIBERAL = 0.05, 0.075


def cp(k: int, n: int) -> tuple[float, float]:
    lo = 0.0 if k == 0 else float(stats.beta.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(0.975, k + 1, n - k))
    return lo, hi


def mcnemar(a: list[bool], b: list[bool]) -> dict:
    only_a = sum(1 for u, v in zip(a, b) if u and not v)
    only_b = sum(1 for u, v in zip(a, b) if v and not u)
    n = only_a + only_b
    return {
        "first_only": only_a,
        "second_only": only_b,
        "exact_two_sided_p": 1.0 if n == 0 else float(stats.binomtest(only_a, n, 0.5).pvalue),
    }


def main() -> None:
    decisions: dict[str, list[bool]] = {}
    for name in ("results_stage1_production.json", "results_stage1_reimplementation.json"):
        decisions.update(json.loads((HERE / name).read_text())["decisions"])

    table = []
    for key, values in sorted(decisions.items()):
        arm, level, cell = key.split("|")
        k, n = sum(values), len(values)
        lo, hi = cp(k, n)
        table.append({"arm": arm, "L": int(level[1:]), "cell": cell, "K": k, "R": n,
                      "rate": k / n, "cp95_low": lo, "cp95_high": hi})

    def rate(arm: str, L: int, cell: str) -> dict:
        return next(r for r in table if r["arm"] == arm and r["L"] == L and r["cell"] == cell)

    rule1 = [
        {"L": L, "cell": cell, "rate": r["rate"], "cp95_low": r["cp95_low"],
         "ok": r["cp95_low"] <= ALPHA and r["rate"] <= LIBERAL}
        for L in (2, 4, 8) for cell in NULL_CELLS for r in [rate("C1", L, cell)]
    ]
    rule2 = {"power_rho06_L8": rate("C1", 8, "lag2_rho06")["rate"],
             "ok": rate("C1", 8, "lag2_rho06")["rate"] >= 0.80}
    rule3 = {}
    for L in (4, 8):
        test = mcnemar(decisions[f"C1|L{L}|lag2_rho06"], decisions[f"C0|L{L}|lag2_rho06"])
        rule3[f"L{L}"] = {**test, "ok": test["exact_two_sided_p"] < 0.05
                          and test["first_only"] > test["second_only"]}
    rule4 = []
    for L in (2, 4, 8):
        for cell in NULL_CELLS:
            a, b = rate("C1", L, cell), rate("C1r", L, cell)
            rule4.append({"L": L, "cell": cell,
                          "ok": a["cp95_low"] <= b["cp95_high"] and b["cp95_low"] <= a["cp95_high"]})
    killed = [row for row in rule1 if row["cp95_low"] > ALPHA or row["rate"] > LIBERAL]
    k3 = rate("C1", 8, "lag2_rho06")["rate"] < 0.50
    verdict = {
        "rule1_C1_null_size": {"rows": rule1, "ok": all(r["ok"] for r in rule1)},
        "rule2_C1_power_rho06_L8": rule2,
        "rule3_C1_beats_C0_rho06": rule3,
        "rule4_C1_vs_C1r_overlap": {"rows": rule4, "ok": all(r["ok"] for r in rule4)},
        "kill_K1_K2_rows": killed,
        "kill_K3": k3,
        "PASS_S1": (
            all(r["ok"] for r in rule1) and rule2["ok"]
            and all(v["ok"] for v in rule3.values())
            and all(r["ok"] for r in rule4) and not killed and not k3
        ),
    }
    paired = {
        f"C1_vs_C2|L{L}|{cell}": mcnemar(decisions[f"C1|L{L}|{cell}"], decisions[f"C2|L{L}|{cell}"])
        for L in (2, 4, 8) for cell in ("lag2_rho03", "lag2_rho06")
    }
    out = {"schema": "selcal.remedy-confirm-stage1-analysis.v1", "table": table,
           "paired_C1_vs_C2": paired, "verdict": verdict}
    (HERE / "results_stage1_analysis.json").write_text(json.dumps(out, indent=1) + "\n")
    for row in table:
        print(f"{row['arm']:4}L{row['L']} {row['cell']:18}{row['K']:>4}/{row['R']:<4}"
              f"{row['rate']:7.4f}  {row['cp95_low']:.4f}-{row['cp95_high']:.4f}")
    print(json.dumps(verdict, indent=1))


if __name__ == "__main__":
    main()
