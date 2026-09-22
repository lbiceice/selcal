"""Stage 1, production arms C0 (exact enumeration) and C1 (block shuffle d=8), sealed inputs.

See protocol_stage1.md (frozen first). Read-only over sealed evidence; writes only this directory.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

from selcal import calibrate_selected_family, resolve_plan_v2, verify_calibration_result
from selcal.contracts import RunStatus, SeriesPair
from selcal.contracts_v2 import PlanRequestV2
from selcal.workflow import attainability

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent / "bounded_study_execution_20260909" / "study_v1"
CELLS = {"iid_null": 400, "circular_ma2_null": 400, "lag2_rho03": 200, "lag2_rho06": 200}
N, ALPHA, LS = 64, 0.05, (2, 4, 8)


def request(arm: str, lags: tuple[int, ...], root_seed: int) -> PlanRequestV2:
    if arm == "C0":
        null_name, null_params, replicates = "circular_shift_exact_v1", {"min_shift": 1}, N - 1
    else:
        null_name, null_params, replicates = "block_shuffle_v2", {"block_length": 8}, 199
    return PlanRequestV2(
        candidates=lags,
        statistic_name="lagged_pearson_v1",
        statistic_params={},
        selection_rule="max_upper",
        null_name=null_name,
        null_params=null_params,
        replicates=replicates,
        alpha=ALPHA,
        tie_tolerance=0.0,
        root_seed=root_seed,
    )


def load(cell: str, index: int) -> SeriesPair:
    raw = json.loads((STUDY / "inputs" / f"{cell}_{index:04d}.json").read_text())
    return SeriesPair(
        source=np.array([float.fromhex(v) for v in raw["source_hex"]]),
        target=np.array([float.fromhex(v) for v in raw["target_hex"]]),
    ), int(raw["root_seed"])


def main() -> None:
    decisions: dict[str, list[bool]] = {}
    notes, guard = [], {}
    started = time.monotonic()
    for L in LS:
        lags = tuple(range(1, L + 1))
        for arm in ("C0", "C1"):
            guard[f"{arm}_L{L}"] = attainability(request(arm, lags, 1), N)
            for cell, budget in CELLS.items():
                key = f"{arm}|L{L}|{cell}"
                rejects: list[bool] = []
                for index in range(budget):
                    pair, seed = load(cell, index)
                    resolution = resolve_plan_v2(request(arm, lags, seed))
                    result = calibrate_selected_family(pair, resolution)
                    verify_calibration_result(result, resolution)
                    if result.status is not RunStatus.COMPLETE:
                        notes.append({"key": key, "index": index, "status": result.status.value,
                                      "failure_stage": None if result.failure_stage is None
                                      else result.failure_stage.value})
                        rejects.append(False)
                        continue
                    rejects.append(bool(result.reject_null))
                decisions[key] = rejects
                print(key, sum(rejects), "/", budget, flush=True)
    payload = {
        "schema": "selcal.remedy-confirm-stage1-production.v1",
        "protocol_sha256": hashlib.sha256((HERE / "protocol_stage1.md").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__},
        "elapsed_seconds": time.monotonic() - started,
        "attainability": guard,
        "non_complete_runs": notes,
        "decisions": decisions,
    }
    (HERE / "results_stage1_production.json").write_text(json.dumps(payload, indent=1) + "\n")


if __name__ == "__main__":
    main()
