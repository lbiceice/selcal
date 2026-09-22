"""Execute power_protocol.md. argv[1] = project interpreter (for the production cross-check)."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
N, LAGS, TOP, ALPHA, R = 127, (1, 2, 3, 4, 5), 5, 0.05, 1000
RHOS = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
CHECK_PER_RHO = 50


def rng(*parts: object) -> np.random.Generator:
    tag = "SelCal/kerala-power-v1|" + "|".join(str(p) for p in parts)
    return np.random.Generator(np.random.PCG64(int(hashlib.sha256(tag.encode()).hexdigest()[:16], 16)))


def yule_walker_ar2(series: np.ndarray) -> tuple[np.ndarray, float]:
    z = (series - series.mean()) / series.std()
    r = np.array([np.mean(z[: len(z) - k] * z[k:]) for k in range(3)])
    toeplitz = np.array([[r[0], r[1]], [r[1], r[0]]])
    phi = np.linalg.solve(toeplitz, r[1:])
    return phi, float(r[0] - phi @ r[1:])


def simulate_ar2(phi: np.ndarray, sigma2: float, length: int, gen: np.random.Generator) -> np.ndarray:
    e = gen.standard_normal(length + 500) * np.sqrt(sigma2)
    out = np.zeros(length + 500)
    for t in range(2, length + 500):
        out[t] = phi[0] * out[t - 1] + phi[1] * out[t - 2] + e[t]
    v = out[500:]
    return (v - v.mean()) / v.std()


def exact_p(x: np.ndarray, y: np.ndarray) -> float:
    fut = y[TOP:]
    idx = (np.arange(N)[None, :] - np.arange(N)[:, None]) % N
    states = x[idx]
    stat = np.max(np.abs(np.stack([
        [np.corrcoef(state[TOP - k : N - k], fut)[0, 1] for k in LAGS] for state in states
    ])), axis=1)
    return int(np.sum(stat >= stat[0])) / N


def production_p(python: str, pairs: list[tuple[np.ndarray, np.ndarray]]) -> list[float]:
    payload = json.dumps([[x.tolist(), y.tolist()] for x, y in pairs])
    code = (
        "import json,sys,numpy as np\n"
        "from selcal import calibrate_selected_family, resolve_plan_v2\n"
        "from selcal.contracts import SeriesPair\n"
        "from selcal.contracts_v2 import PlanRequestV2\n"
        "res=resolve_plan_v2(PlanRequestV2(candidates=(1,2,3,4,5),statistic_name='lagged_pearson_v1',"
        "statistic_params={},selection_rule='max_absolute',null_name='circular_shift_exact_v1',"
        "null_params={'min_shift':1},replicates=126,alpha=0.05,tie_tolerance=0.0,root_seed=1))\n"
        "out=[]\n"
        "for x,y in json.loads(sys.stdin.read()):\n"
        "    r=calibrate_selected_family(SeriesPair(source=np.array(x),target=np.array(y)),res)\n"
        "    out.append(r.p_value)\n"
        "print(json.dumps(out))\n"
    )
    done = subprocess.run([python, "-c", code], input=payload, capture_output=True, text=True, check=True)
    return json.loads(done.stdout)


def main() -> None:
    case = json.loads((HERE / "results.json").read_text())
    import csv
    rows = [r for r in csv.DictReader((HERE / "A2_anom_input.csv").open())]
    x_obs = np.array([float(r["x"]) for r in rows])
    y_obs = np.array([float(r["y"]) for r in rows])
    phi_x, s2_x = yule_walker_ar2(x_obs)
    phi_y, s2_y = yule_walker_ar2(y_obs)
    table, mismatches = [], 0
    for rho in RHOS:
        rejects, pvals, pairs = 0, [], []
        for i in range(R):
            gx, gw = rng(rho, i, "x"), rng(rho, i, "w")
            x_long = simulate_ar2(phi_x, s2_x, N + 3, gx)
            w = simulate_ar2(phi_y, s2_y, N, gw)
            x = x_long[3:]
            y = rho * x_long[:N] + np.sqrt(1 - rho * rho) * w
            p = exact_p(x, y)
            pvals.append(p)
            rejects += p <= ALPHA
            if i < CHECK_PER_RHO:
                pairs.append((x, y))
        prod = production_p(sys.argv[1], pairs)
        mismatches += sum(1 for a, b in zip(prod, pvals[:CHECK_PER_RHO]) if a != b)
        lo = 0.0 if rejects == 0 else float(stats.beta.ppf(0.025, rejects, R - rejects + 1))
        hi = 1.0 if rejects == R else float(stats.beta.ppf(0.975, rejects + 1, R - rejects))
        table.append({"rho": rho, "rejects": rejects, "R": R, "rate": rejects / R, "cp95": [lo, hi]})
        print(rho, rejects / R, flush=True)
    min_rho_80 = next((row["rho"] for row in table if row["rate"] >= 0.8), None)
    out = {
        "schema": "selcal.kerala-power.v1",
        "protocol_sha256": hashlib.sha256((HERE / "power_protocol.md").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "ar2": {"source_phi": phi_x.tolist(), "source_sigma2": s2_x,
                "target_phi": phi_y.tolist(), "target_sigma2": s2_y},
        "production_crosscheck": {"per_rho": CHECK_PER_RHO, "mismatches": mismatches},
        "table": table,
        "smallest_rho_with_80pct_power": min_rho_80,
        "observed_context": {"A1_r": case["A1_raw"]["selcal"]["decision_statistic"],
                             "A2_r": case["A2_deseasonalised"]["selcal"]["decision_statistic"]},
    }
    (HERE / "results_power.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("ar2", "production_crosscheck", "smallest_rho_with_80pct_power")}))


if __name__ == "__main__":
    main()
