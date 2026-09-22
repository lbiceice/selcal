"""Execute protocol.md: Kerala dengue vs Nino 3.4 (A0-A3) and the influenza guard check (B).

SelCal runs go through the installed CLI file workflow (validate -> run -> verify --replay -> report)
with the project interpreter given as argv[1]. Comparators use scipy (argv[2] interpreter runs this
script). Writes results.json and the derived inputs/configs/records in this folder.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "Climate_dengue_data_Kerala_paper.csv"
EXPECTED_SHA = "91fac1a7f6c7b893c2065726f4b26aeb9301dd8aec7a6bbd8bcb68780074289b"
LAGS = (1, 2, 3, 4, 5)
MB = "4194304"


def load_window() -> list[dict[str, str]]:
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == EXPECTED_SHA
    rows = list(csv.DictReader(DATA.open()))
    window = [r for r in rows if "2006-06-30" <= r["index"] <= "2016-12-31"]
    assert len(window) == 127 and window[0]["index"] == "2006-06-30"
    return window


def consistency(window: list[dict[str, str]]) -> dict:
    nino0 = [float(r["nino0"]) for r in window]
    mismatches = []
    for k in LAGS:
        for t in range(k, len(window)):
            if abs(float(window[t][f"nino{k}"]) - nino0[t - k]) > 1e-9:
                mismatches.append({"lag": k, "month": window[t]["index"]})
    return {"checked": "nino{k}[t] == nino0[t-k] for t >= k", "mismatches": len(mismatches),
            "first": mismatches[:5]}


def replication(window: list[dict[str, str]]) -> dict:
    y = np.array([float(r["dengue"]) for r in window])
    rows = []
    for k in range(0, 6):
        x = np.array([float(r[f"nino{k}"]) for r in window])
        res = stats.pearsonr(x, y)
        rows.append({"lag": k, "r": float(res.statistic), "p_two_sided": float(res.pvalue)})
    best = max(rows, key=lambda row: abs(row["r"]))
    return {"n": len(y), "by_lag": rows, "best": best}


def transform(window: list[dict[str, str]]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x_raw = np.array([float(r["nino0"]) for r in window])
    y_raw = np.array([float(r["dengue"]) for r in window])
    month = np.array([int(r["month"]) for r in window])
    t = np.arange(len(window), dtype=float)
    y_log = np.log1p(y_raw)
    slope, intercept = np.polyfit(t, y_log, 1)
    resid = y_log - (slope * t + intercept)
    y_anom = resid - np.array([resid[month == m].mean() for m in month])
    x_anom = x_raw - np.array([x_raw[month == m].mean() for m in month])
    return x_raw, y_raw, x_anom, y_anom


def comparators(x: np.ndarray, y: np.ndarray) -> dict:
    n, top = len(x), max(LAGS)
    per = []
    for k in LAGS:
        res = stats.pearsonr(x[top - k : n - k], y[top:])
        per.append({"lag": k, "r": float(res.statistic), "p_two_sided": float(res.pvalue)})
    best = max(per, key=lambda row: abs(row["r"]))
    return {"common_support_pairs": n - top, "by_lag": per, "best_lag_textbook": best,
            "bonferroni_p": min(1.0, len(LAGS) * best["p_two_sided"])}


def selcal(python: str, label: str, x: np.ndarray, y: np.ndarray) -> dict:
    csv_path = HERE / f"{label}_input.csv"
    csv_path.write_text("x,y\n" + "".join(f"{float(a)!r},{float(b)!r}\n" for a, b in zip(x, y, strict=True)))
    config = {
        "schema": "selcal.workflow-config.v1",
        "input": {"format": "csv", "source_column": "x", "target_column": "y"},
        "plan": {"candidates": list(LAGS), "statistic_name": "lagged_pearson_v1",
                 "statistic_params": {}, "selection_rule": "max_absolute",
                 "null_name": "circular_shift_exact_v1", "null_params": {"min_shift": 1},
                 "replicates": len(x) - 1, "alpha": 0.05, "tie_tolerance": 0.0,
                 "root_seed": 20260922},
    }
    config_path = HERE / f"{label}_config.json"
    config_path.write_text(json.dumps(config, indent=1) + "\n")
    record, report = HERE / f"{label}.sqlite", HERE / f"{label}_report.html"
    for stale in (record, report):
        if stale.exists():
            raise SystemExit(f"refusing to overwrite {stale.name}")

    def call(*args: str) -> dict:
        done = subprocess.run([python, "-m", "selcal", *args], cwd=HERE, capture_output=True,
                              text=True, check=False)
        payload = json.loads(done.stdout.strip().splitlines()[-1])
        return {"exit": done.returncode, "outcome": payload["outcome"], "error": payload["error"],
                "data": payload["data"]}

    steps = {
        "validate": call("validate", csv_path.name, config_path.name),
        "run": call("run", csv_path.name, config_path.name, record.name, "--max-bytes", MB),
    }
    steps["verify_replay"] = call("verify", record.name, "--max-bytes", MB, "--replay")
    steps["report"] = call("report", record.name, report.name, "--max-bytes", MB)
    run = steps["run"]["data"] or {}
    return {
        "input_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "preflight": steps["validate"]["data"]["preflight"]["plan"]["status"],
        "exits": {k: v["exit"] for k, v in steps.items()},
        "replay": (steps["verify_replay"]["data"] or {}).get("replay"),
        "selected_lag": run.get("selected_candidate"),
        "decision_statistic": run.get("decision_statistic"),
        "exceedance_count": run.get("exceedance_count"),
        "planned_replicates": run.get("planned_replicates"),
        "p_value": run.get("p_value"),
        "reject_null": run.get("reject_null"),
    }


def guard_case_b(python: str) -> dict:
    code = (
        "import json; from selcal.contracts_v2 import PlanRequestV2; from selcal.workflow import "
        "attainability; r=PlanRequestV2(candidates=tuple(range(1,31)),statistic_name='lagged_pearson_v1',"
        "statistic_params={},selection_rule='max_absolute',null_name='circular_shift_exact_v1',"
        "null_params={'min_shift':1},replicates=417,alpha=0.05,tie_tolerance=0.0,root_seed=1);"
        "print(json.dumps(attainability(r,418)))"
    )
    done = subprocess.run([python, "-c", code], capture_output=True, text=True, check=True)
    report = json.loads(done.stdout)
    return {"n": 418, "lags": "1..30", "attainability": report,
            "minimum_n_for_30_lags": 30 * 20, "largest_L_at_n_418": int(0.05 * 418)}


def main() -> None:
    project_python = sys.argv[1]
    window = load_window()
    x_raw, y_raw, x_anom, y_anom = transform(window)
    results = {
        "schema": "selcal.real-case-reanalysis.v1",
        "protocol_sha256": hashlib.sha256((HERE / "protocol.md").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "consistency": consistency(window),
        "A0_published_practice": replication(window),
        "A1_raw": {"selcal": selcal(project_python, "A1_raw", x_raw, y_raw),
                   "comparators": comparators(x_raw, y_raw)},
        "A2_deseasonalised": {"selcal": selcal(project_python, "A2_anom", x_anom, y_anom),
                              "comparators": comparators(x_anom, y_anom)},
        "B_guard": guard_case_b(project_python),
    }
    (HERE / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    print(json.dumps({k: results[k] for k in ("consistency", "A0_published_practice")}, indent=1))
    for key in ("A1_raw", "A2_deseasonalised"):
        print(key, json.dumps(results[key]["selcal"]), json.dumps(results[key]["comparators"]["best_lag_textbook"]),
              "bonferroni", results[key]["comparators"]["bonferroni_p"])
    print("B", json.dumps(results["B_guard"]["attainability"]))


if __name__ == "__main__":
    main()
