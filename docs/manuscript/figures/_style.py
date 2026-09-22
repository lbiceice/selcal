"""Shared style, colours and data loaders for the SelCal SoftwareX figures.

Every number plotted is read from the evidence JSON files below; nothing is
hand-copied. Colours are the dataviz reference categorical slots 1-5 in fixed
order (validated with validate_palette.js, light mode, white surface, adjacent
pairs: worst CVD dE 9.1, worst normal-vision dE 19.6). Because three slots are
below 3:1 contrast on white and the dot-plot methods are not all adjacent,
every method also carries its own marker shape (secondary encoding) and a
legend; block shuffle (not adopted) is a neutral grey hollow marker.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib as mpl

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVID = REPO / "docs" / "status" / "evidence" / "remedy_confirm_20260920"
STAGE2_JSON = EVID / "results_stage2_analysis.json"
IDTXL_JSON = EVID / "results_idtxl_analysis.json"

CM = 1 / 2.54
SINGLE_W = 8.5 * CM
DOUBLE_W = 17.5 * CM

# Ink (dataviz reference chrome, light)
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
REFUSED_FILL = "#f0efec"

ALPHA = 0.05

# Method identity: colour, marker, filled?, label. Order = plotting order.
METHODS = {
    "C0": dict(color="#2a78d6", marker="o", filled=True, label="SelCal exact enumeration"),
    "C2": dict(color="#eb6834", marker="s", filled=True, label="Bonferroni (best lag)"),
    "I1": dict(color="#1baf7a", marker="^", filled=True, label="IDTxl Gaussian (analytic surrogates)"),
    "I2": dict(color="#eda100", marker="D", filled=True, label="IDTxl KSG + circular (n = 64)"),
    "C1": dict(color=MUTED, marker="o", filled=False, label="Block shuffle (tested, not adopted)"),
}
METHOD_ORDER = ["C0", "C2", "I1", "I2", "C1"]

NULLS = [("iid", "i.i.d."), ("ma2", "MA(2), circular"), ("ar1", "AR(1), non-circular")]
NS = [64, 256]
LS = [2, 8]


def setup() -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7,
        "axes.titlesize": 7.5,
        "axes.labelsize": 7,
        "xtick.labelsize": 6.5,
        "ytick.labelsize": 6.5,
        "legend.fontsize": 6.5,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.6,
        "axes.labelcolor": INK2,
        "axes.titlecolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": INK2,
        "ytick.labelcolor": INK2,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.5,
        "grid.linestyle": "-",
        "axes.axisbelow": True,
        "text.color": INK,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.dpi": 300,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cells() -> dict[str, dict]:
    """Return {key: {K,R,rate,cp95_low,cp95_high}} merging Stage 2 and IDTxl."""
    cells = dict(json.loads(STAGE2_JSON.read_text())["table"])
    for row in json.loads(IDTXL_JSON.read_text())["rows"]:
        if not row.get("complete", False):
            raise ValueError(f"incomplete IDTxl row {row['key']}")
        cells[row["key"]] = {k: row[k] for k in ("K", "R", "rate", "cp95_low", "cp95_high")}
    return cells


def key(method: str, cell: str, rho: str, L: int, n: int) -> str:
    return f"{method}|{cell}|{rho}|L{L}|n{n}"


def refused(L: int, n: int) -> bool:
    """Guard rule: circular exact plan refused when floor L/n exceeds alpha."""
    return L / n > ALPHA


def save(fig, stem: str) -> None:
    for ext in ("pdf", "png"):
        fig.savefig(HERE / f"{stem}.{ext}", dpi=300, bbox_inches="tight", pad_inches=0.02)


def dot_interval_panel(ax, cells, cell, rho, L, *, ylim, pct_fmt=True, refused_label_y=None):
    """Grouped dot-and-interval plot: groups = n, dots = methods."""
    offsets = {m: (i - 2) * 0.15 for i, m in enumerate(METHOD_ORDER)}
    for gi, n in enumerate(NS):
        for m in METHOD_ORDER:
            k = key(m, cell, rho, L, n)
            if k not in cells:
                continue
            c = cells[k]
            x = gi + offsets[m]
            spec = METHODS[m]
            if m == "C0" and refused(L, n):
                ax.axvspan(x - 0.07, x + 0.07, color=REFUSED_FILL, lw=0, zorder=0)
                ax.plot([x], [c["rate"] * 100], marker="x", ms=4.5, mew=1.0,
                        color=spec["color"], ls="none", zorder=3, clip_on=False)
                # Horizontal label right of the refused marker, at a height chosen per figure
                # so that it clears the other methods' intervals.
                y_lab = refused_label_y if refused_label_y is not None else ylim[1] * 0.5
                ax.text(x + 0.1, y_lab, f"SelCal refused ({L}/{n} > α)",
                        ha="left", va="center", fontsize=5.8, color=INK2, zorder=4)
                continue
            lo, hi = c["cp95_low"] * 100, c["cp95_high"] * 100
            ax.plot([x, x], [lo, hi], color=spec["color"], lw=1.2, solid_capstyle="round", zorder=2)
            ax.plot([x], [c["rate"] * 100], marker=spec["marker"], ms=4.2 if spec["marker"] != "D" else 3.6,
                    mfc=spec["color"] if spec["filled"] else "white", mec=spec["color"] if not spec["filled"] else "white",
                    mew=0.9 if not spec["filled"] else 0.6, ls="none", zorder=3)
    ax.set_xticks(range(len(NS)))
    ax.set_xticklabels([f"n = {n}" for n in NS])
    ax.set_xlim(-0.55, len(NS) - 0.45)
    ax.set_ylim(*ylim)
    ax.tick_params(axis="x", length=0)


def method_legend_handles(methods=METHOD_ORDER):
    from matplotlib.lines import Line2D
    hs = []
    for m in methods:
        s = METHODS[m]
        hs.append(Line2D([0], [0], color=s["color"], lw=1.2, marker=s["marker"],
                         ms=4.2 if s["marker"] != "D" else 3.6,
                         mfc=s["color"] if s["filled"] else "white",
                         mec=s["color"] if not s["filled"] else "white",
                         mew=0.9 if not s["filled"] else 0.6, label=s["label"]))
    hs.append(Line2D([0], [0], color=METHODS["C0"]["color"], marker="x", ms=4.5, mew=1.0, ls="none",
                     label="SelCal plan refused by guard (0 by design)"))
    return hs
