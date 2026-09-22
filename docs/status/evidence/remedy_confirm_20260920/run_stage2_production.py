"""Stage 2 production arms C0 and C1 in parallel worker processes (protocol_stage2.md).

Each chunk writes its own JSON under stage2_results/, so an interrupted run resumes without
recomputing finished chunks. Inputs are checked against stage2_inputs/manifest.json first.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "stage2_inputs"
RESULTS = HERE / "stage2_results"
CHUNK = 250
WORKERS = 10
BLOCK = {64: 8, 256: 16}


def root_seed(cell: str, n: int, rho: str, L: int, index: int) -> int:
    tag = f"SelCal/remedy-confirm-v1|stage2|root|{cell}|{n}|{rho}|{L}|{index}"
    return int(hashlib.sha256(tag.encode()).hexdigest()[:16], 16) >> 1


def jobs() -> list[dict]:
    out = []
    for n in (64, 256):
        for cell in ("iid", "ma2", "ar1"):
            for L in (2, 8):
                for arm in ("C0", "C1"):
                    for start in range(0, 4000, CHUNK):
                        out.append({"file": f"{cell}_n{n}.npz", "cell": cell, "n": n, "rho": "-",
                                    "L": L, "arm": arm, "start": start, "stop": start + CHUNK})
        for rho in ("0.3", "0.6"):
            for L in (2, 8):
                for arm in ("C0", "C1"):
                    for start in range(0, 1000, CHUNK):
                        out.append({"file": f"alt_rho{rho}_L{L}_n{n}.npz", "cell": "alt", "n": n,
                                    "rho": rho, "L": L, "arm": arm, "start": start,
                                    "stop": start + CHUNK})
    return out


def chunk_path(job: dict) -> Path:
    return RESULTS / (
        f"{job['arm']}_{job['cell']}_rho{job['rho']}_L{job['L']}_n{job['n']}_{job['start']:04d}.json"
    )


def run_chunk(job: dict) -> str:
    from selcal import calibrate_selected_family, resolve_plan_v2, verify_calibration_result
    from selcal.contracts import RunStatus, SeriesPair
    from selcal.contracts_v2 import PlanRequestV2

    data = np.load(INPUTS / job["file"])
    n, L = job["n"], job["L"]
    if job["arm"] == "C0":
        null_name, null_params, replicates = "circular_shift_exact_v1", {"min_shift": 1}, n - 1
    else:
        null_name, null_params, replicates = "block_shuffle_v2", {"block_length": BLOCK[n]}, 199
    decisions, notes = [], []
    for index in range(job["start"], job["stop"]):
        pair = SeriesPair(source=np.array(data["source"][index], dtype=np.float64),
                          target=np.array(data["target"][index], dtype=np.float64))
        resolution = resolve_plan_v2(PlanRequestV2(
            candidates=tuple(range(1, L + 1)), statistic_name="lagged_pearson_v1",
            statistic_params={}, selection_rule="max_upper", null_name=null_name,
            null_params=null_params, replicates=replicates, alpha=0.05, tie_tolerance=0.0,
            root_seed=root_seed(job["cell"], n, job["rho"], L, index)))
        result = calibrate_selected_family(pair, resolution)
        verify_calibration_result(result, resolution)
        if result.status is not RunStatus.COMPLETE:
            notes.append({"index": index, "status": result.status.value,
                          "failure_stage": None if result.failure_stage is None
                          else result.failure_stage.value})
            decisions.append(False)
        else:
            decisions.append(bool(result.reject_null))
    chunk_path(job).write_text(json.dumps({**job, "decisions": decisions, "non_complete": notes}))
    return chunk_path(job).name


def main() -> None:
    manifest = json.loads((INPUTS / "manifest.json").read_text())
    for name, digest in manifest.items():
        if not name.startswith("_"):
            assert hashlib.sha256((INPUTS / name).read_bytes()).hexdigest() == digest, name
    RESULTS.mkdir(exist_ok=True)
    pending = [job for job in jobs() if not chunk_path(job).exists()]
    print(f"chunks total {len(jobs())}, pending {len(pending)}", flush=True)
    started = time.monotonic()
    with ProcessPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(run_chunk, job) for job in pending]
        for done, future in enumerate(as_completed(futures), start=1):
            name = future.result()
            if done % 20 == 0 or done == len(futures):
                print(f"{done}/{len(futures)} {name} {time.monotonic() - started:.0f}s", flush=True)
    (HERE / "stage2_run_meta.json").write_text(json.dumps({
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "protocol_sha256": hashlib.sha256((HERE / "protocol_stage2.md").read_bytes()).hexdigest(),
        "python": sys.version.split()[0], "numpy": np.__version__, "workers": WORKERS,
        "cpu_count": os.cpu_count(), "elapsed_seconds_this_invocation": time.monotonic() - started,
    }, indent=1) + "\n")
    print("ALL_CHUNKS_DONE", flush=True)


if __name__ == "__main__":
    main()
