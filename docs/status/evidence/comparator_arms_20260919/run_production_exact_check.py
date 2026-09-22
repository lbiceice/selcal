"""E-C0 with production code: run `circular_shift_exact_v1` on the sealed inputs.

Compares the production p-value against the independent Stage 0 enumeration
(`results_stage0.json` was produced without importing SelCal) on every sealed input.
Read-only over sealed evidence; writes only this directory.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

from selcal import calibrate_selected_family, resolve_plan_v2, verify_calibration_result
from selcal.contracts import RunStatus, SeriesPair
from selcal.contracts_v2 import PlanRequestV2

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent / "bounded_study_execution_20260909" / "study_v1"
CELLS = {"iid_null": 400, "circular_ma2_null": 400, "lag2_rho03": 200, "lag2_rho06": 200}
N, ALPHA = 64, 0.05


def plan(root_seed: int) -> object:
    return resolve_plan_v2(
        PlanRequestV2(
            candidates=(1, 2),
            statistic_name="lagged_pearson_v1",
            statistic_params={},
            selection_rule="max_upper",
            null_name="circular_shift_exact_v1",
            null_params={"min_shift": 1},
            replicates=N - 1,
            alpha=ALPHA,
            tie_tolerance=0.0,
            root_seed=root_seed,
        )
    )


def main() -> None:
    rows, mismatches = [], []
    started = time.monotonic()
    for cell, budget in CELLS.items():
        rejects = 0
        for index in range(budget):
            name = f"{cell}_{index:04d}"
            raw = json.loads((STUDY / "inputs" / f"{name}.json").read_text())
            pair = SeriesPair(
                source=np.array([float.fromhex(v) for v in raw["source_hex"]]),
                target=np.array([float.fromhex(v) for v in raw["target_hex"]]),
            )
            resolution = plan(int(raw["root_seed"]))
            result = calibrate_selected_family(pair, resolution)
            verify_calibration_result(result, resolution)
            if result.status is not RunStatus.COMPLETE:
                mismatches.append({"case": name, "reason": "not_complete"})
                continue
            shifts = sorted(o.transform_token.state.shift for o in result.replicates)
            with gzip.open(STUDY / "results" / f"{name}.json.gz") as fh:
                sealed = json.load(fh)
            exact = sealed["comparison"]["reference_exact"]
            expected_p = exact["numerator"] / exact["denominator"]
            if shifts != list(range(1, N)) or result.p_value != expected_p:
                mismatches.append(
                    {
                        "case": name,
                        "production_p": result.p_value,
                        "sealed_exact_p": expected_p,
                        "distinct_states": len(set(shifts)),
                    }
                )
            rejects += bool(result.reject_null)
        rows.append({"cell": cell, "R": budget, "K": rejects, "rate": rejects / budget})
        print(rows[-1], flush=True)

    payload = {
        "schema": "selcal.production-exact-enumeration-check.v1",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "elapsed_seconds": time.monotonic() - started,
        "mismatches": mismatches,
        "primary": rows,
    }
    (HERE / "results_production_exact.json").write_text(json.dumps(payload, indent=1) + "\n")
    print("mismatches", len(mismatches))


if __name__ == "__main__":
    main()
