"""Blueprint Stage 0 / endpoint E-C0: exact-enumeration decisions on the sealed 1,200 inputs.

Read-only over sealed evidence. Imports no SelCal module. Two independent paths per input:
(1) the sealed `comparison.reference_exact` table, (2) a fresh re-computation from the float-hex
input. p_exact = #{s in 0..n-1 : T_s >= T_0} / n, which equals SelCal's (1 + E)/(B + 1) when every
non-identity state is used exactly once.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import stats

from run_comparator_arms import CELLS, NULL_CELLS, circular_states, cp, lagged_r, load

HERE = Path(__file__).resolve().parent
ALPHA, LAGS = 0.05, (1, 2)


def main() -> None:
    rows, mismatches, sealed_vs_exact = [], [], []
    for cell in CELLS:
        budget = 400 if cell in NULL_CELLS else 200
        exact_reject, sealed_reject, both = [], [], 0
        for i in range(budget):
            x, y, sealed = load(cell, i)
            obs = float(np.max(lagged_r(x, y, LAGS)))
            states = circular_states(x)
            mine = int(sum(np.max(lagged_r(states[s], y, LAGS)) >= obs for s in range(64)))
            ref = sealed["comparison"]["reference_exact"]
            if mine != ref["numerator"] or ref["denominator"] != 64:
                mismatches.append({"cell": cell, "index": i, "mine": mine, "sealed": ref})
            decision = mine / 64 <= ALPHA
            exact_reject.append(decision)
            sealed_reject.append(bool(sealed["reject_null"]))
            both += decision and bool(sealed["reject_null"])
        k_exact, k_sealed = sum(exact_reject), sum(sealed_reject)
        lo, hi = cp(k_exact, budget)
        slo, shi = cp(k_sealed, budget)
        rows.append({
            "cell": cell, "R": budget,
            "exact_K": k_exact, "exact_rate": k_exact / budget,
            "exact_cp95": [lo, hi],
            "sealed_K": k_sealed, "sealed_rate": k_sealed / budget, "sealed_cp95": [slo, shi],
            "sealed_only": sum(1 for a, b in zip(exact_reject, sealed_reject) if b and not a),
            "exact_only": sum(1 for a, b in zip(exact_reject, sealed_reject) if a and not b),
        })
        sealed_vs_exact.append(
            {"cell": cell,
             "mcnemar_exact_two_sided_p": float(
                 stats.binomtest(rows[-1]["exact_only"],
                                 rows[-1]["exact_only"] + rows[-1]["sealed_only"], 0.5).pvalue
             ) if rows[-1]["exact_only"] + rows[-1]["sealed_only"] else 1.0}
        )
        print(cell, rows[-1], flush=True)

    out = {
        "schema": "selcal.stage0-exact-enumeration.v1",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "E_C0_numerator_mismatches": mismatches,
        "primary": rows,
        "paired_exact_vs_sealed": sealed_vs_exact,
        "pass_P_f": all(
            row["exact_cp95"][0] <= ALPHA for row in rows if row["cell"] in NULL_CELLS
        ) and next(r["exact_rate"] for r in rows if r["cell"] == "lag2_rho06") >= 0.95,
    }
    (HERE / "results_stage0.json").write_text(json.dumps(out, indent=1) + "\n")
    print("mismatches", len(mismatches), "pass_P_f", out["pass_P_f"])


if __name__ == "__main__":
    main()
