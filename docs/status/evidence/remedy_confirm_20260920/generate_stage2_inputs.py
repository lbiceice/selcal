"""Generate and digest the Stage 2 inputs (protocol_stage2.md) before any arm runs."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "stage2_inputs"
NS = (64, 256)
LS = (2, 8)
R_NULL, R_ALT = 4000, 1000
BURN = 500


def rng(*parts: object) -> np.random.Generator:
    tag = "SelCal/remedy-confirm-v1|stage2|" + "|".join(str(p) for p in parts)
    return np.random.Generator(np.random.PCG64(int(hashlib.sha256(tag.encode()).hexdigest()[:16], 16)))


def ma2(e: np.ndarray) -> np.ndarray:
    return (e + 0.6 * np.roll(e, 1) + 0.3 * np.roll(e, 2)) / math.sqrt(1.45)


def ar1(e: np.ndarray, n: int) -> np.ndarray:
    out = np.empty(e.size)
    out[0] = e[0]
    for t in range(1, e.size):
        out[t] = 0.6 * out[t - 1] + e[t]
    return out[-n:]


def null_pair(cell: str, n: int, index: int) -> tuple[np.ndarray, np.ndarray]:
    if cell == "iid":
        return (rng(cell, n, "-", "-", index, "x").standard_normal(n),
                rng(cell, n, "-", "-", index, "y").standard_normal(n))
    if cell == "ma2":
        return (ma2(rng(cell, n, "-", "-", index, "x").standard_normal(n)),
                ma2(rng(cell, n, "-", "-", index, "y").standard_normal(n)))
    return (ar1(rng(cell, n, "-", "-", index, "x").standard_normal(n + BURN), n),
            ar1(rng(cell, n, "-", "-", index, "y").standard_normal(n + BURN), n))


def alt_pair(n: int, rho: float, L: int, index: int) -> tuple[np.ndarray, np.ndarray]:
    long_x = rng("alt", n, rho, L, index, "x").standard_normal(n + L)
    e = rng("alt", n, rho, L, index, "e").standard_normal(n)
    x = long_x[L:]
    lagged = long_x[:n]  # lagged[t] = x[t - L]
    return x, rho * lagged + math.sqrt(1 - rho * rho) * e


def main() -> None:
    OUT.mkdir(exist_ok=False)
    manifest = {}
    for n in NS:
        for cell in ("iid", "ma2", "ar1"):
            pairs = [null_pair(cell, n, i) for i in range(R_NULL)]
            name = f"{cell}_n{n}.npz"
            np.savez(OUT / name, source=np.stack([p[0] for p in pairs]),
                     target=np.stack([p[1] for p in pairs]))
            manifest[name] = hashlib.sha256((OUT / name).read_bytes()).hexdigest()
        for rho in (0.3, 0.6):
            for L in LS:
                pairs = [alt_pair(n, rho, L, i) for i in range(R_ALT)]
                name = f"alt_rho{rho}_L{L}_n{n}.npz"
                np.savez(OUT / name, source=np.stack([p[0] for p in pairs]),
                         target=np.stack([p[1] for p in pairs]))
                manifest[name] = hashlib.sha256((OUT / name).read_bytes()).hexdigest()
    manifest["_generator_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest["_protocol_sha256"] = hashlib.sha256((HERE / "protocol_stage2.md").read_bytes()).hexdigest()
    manifest["_numpy"] = np.__version__
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
