"""IDTxl 1.6.0 comparator arms I1/I2 on the Stage 2 inputs (protocol_idtxl.md).

Runs in the dedicated IDTxl environment. Chunked and resumable under idtxl_results/.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.metadata as metadata
import io
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "stage2_inputs"
RESULTS = HERE / "idtxl_results"
CHUNK = 250
WORKERS = 3


def jobs() -> list[dict]:
    out = []
    for arm, ns in (("I1", (64, 256)), ("I2", (64,))):
        for n in ns:
            r_null = 4000 if arm == "I1" else 1000
            for cell in ("iid", "ma2", "ar1"):
                for L in (2, 8):
                    for start in range(0, r_null, CHUNK):
                        out.append({"arm": arm, "file": f"{cell}_n{n}.npz", "cell": cell, "n": n,
                                    "rho": "-", "L": L, "start": start, "stop": start + CHUNK})
            for rho in ("0.3", "0.6"):
                for L in (2, 8):
                    for start in range(0, 1000, CHUNK):
                        out.append({"arm": arm, "file": f"alt_rho{rho}_L{L}_n{n}.npz", "cell": "alt",
                                    "n": n, "rho": rho, "L": L, "start": start,
                                    "stop": start + CHUNK})
    return out


def chunk_path(job: dict) -> Path:
    return RESULTS / (
        f"{job['arm']}_{job['cell']}_rho{job['rho']}_L{job['L']}_n{job['n']}_{job['start']:04d}.json"
    )


def run_chunk(job: dict) -> str:
    from idtxl.bivariate_mi import BivariateMI
    from idtxl.data import Data
    from idtxl.estimators_jidt import JidtGaussianCMI, JidtKraskovCMI

    data = np.load(INPUTS / job["file"])
    n, L = job["n"], job["L"]
    decisions, failures = [], []
    for index in range(job["start"], job["stop"]):
        settings = {"max_lag_sources": L, "min_lag_sources": 1, "n_perm_max_stat": 199,
                    "n_perm_min_stat": 199, "n_perm_omnibus": 199, "n_perm_max_seq": 199,
                    "permute_in_time": True, "verbose": False}
        if job["arm"] == "I1":
            settings["cmi_estimator"] = JidtGaussianCMI
        else:
            settings.update(cmi_estimator=JidtKraskovCMI, perm_type="circular",
                            max_shift=n - L - 1)
        tag = f"SelCal/remedy-confirm-v1|idtxl|{job['arm']}|{job['cell']}|{n}|{job['rho']}|{L}|{index}"
        np.random.seed(int(hashlib.sha256(tag.encode()).hexdigest()[:8], 16))
        series = np.vstack([data["source"][index], data["target"][index]])
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = BivariateMI().analyse_single_target(
                    settings=settings, data=Data(series, dim_order="ps", normalise=False),
                    target=1, sources=[0])
            decisions.append(len(result.get_single_target(1, fdr=False)["selected_vars_sources"]) > 0)
        except Exception as error:  # recorded, counted as no link
            failures.append({"index": index, "error": f"{type(error).__name__}: {error}"[:300]})
            decisions.append(False)
    chunk_path(job).write_text(json.dumps({**job, "decisions": decisions, "failures": failures}))
    return chunk_path(job).name


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    pending = [job for job in jobs() if not chunk_path(job).exists()]
    print(f"chunks total {len(jobs())}, pending {len(pending)}", flush=True)
    started = time.monotonic()
    with ProcessPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(run_chunk, job) for job in pending]
        for done, future in enumerate(as_completed(futures), start=1):
            name = future.result()
            if done % 10 == 0 or done == len(futures):
                print(f"{done}/{len(futures)} {name} {time.monotonic() - started:.0f}s", flush=True)
    (HERE / "idtxl_run_meta.json").write_text(json.dumps({
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "protocol_sha256": hashlib.sha256((HERE / "protocol_idtxl.md").read_bytes()).hexdigest(),
        "python": sys.version.split()[0],
        "versions": {p: metadata.version(p) for p in
                     ("idtxl", "numpy", "scipy", "statsmodels", "jpype1", "h5py")},
        "java_home": __import__("os").environ.get("JAVA_HOME"),
        "elapsed_seconds_this_invocation": time.monotonic() - started,
    }, indent=1) + "\n")
    print("ALL_CHUNKS_DONE", flush=True)


if __name__ == "__main__":
    main()
