"""Fig. 2: why the attainability guard exists.

(a) lag-collision schematic (analytic, n = 16, L = 4);
(b) attainable p floor L/n versus n (analytic);
(c) measured power of SelCal exact enumeration (C0) at rho = 0.6, read from
    results_stage2_analysis.json.
Run: <python> docs/manuscript/figures/fig2_guard.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import _style as S

# Ordinal blue ramp (dataviz reference sequential blue, steps 250/450/650)
L_COLORS = {2: "#86b6ef", 4: "#2a78d6", 8: "#104281"}
HILITE = "#2a78d6"
SCHEM_N, SCHEM_L, SCHEM_CSTAR = 16, 4, 3


def panel_a(ax):
    n, L, cstar = SCHEM_N, SCHEM_L, SCHEM_CSTAR
    hits = 0
    for c in range(1, L + 1):
        for s in range(n):
            eff = (c + s - 1) % n + 1  # lag of the original series that shift s maps searched lag c onto
            hit = eff == cstar
            hits += hit
            ax.add_patch(Rectangle((s + 0.06, c - 0.44), 0.88, 0.88,
                                   facecolor=HILITE if hit else S.REFUSED_FILL, lw=0))
            ax.text(s + 0.5, c, str(eff), ha="center", va="center", fontsize=5,
                    color="white" if hit else S.INK2)
    assert hits == L
    ax.set_xlim(0, n)
    ax.set_ylim(L + 0.6, 0.4)
    ax.set_xticks(np.arange(n) + 0.5)
    ax.set_xticklabels([str(s) if s % 3 == 0 or s == n - 1 else "" for s in range(n)])
    ax.set_yticks(range(1, L + 1))
    ax.set_xlabel(f"circular shift s (n = {n})")
    ax.set_ylabel("searched lag c")
    ax.grid(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(f"(a) Lag collision (n = {n}, L = {L}, c* = {cstar})", loc="left")
    ax.set_aspect("equal")
    ax.text(n + 0.8, 0.55,
            "Cell = lag of the original series that\n"
            "searched lag c reaches after shift s.\n\n"
            "Blue: s = c* − c (mod n). Each of these\n"
            f"{L} shifts reproduces the observed\n"
            "maximum, so at least "
            f"{L} of {n} null states\n"
            f"tie it: p ≥ {L}/{n} = {L / n:.2f}, whatever the data.",
            fontsize=6.3, color=S.INK2, va="top", ha="left")


def panel_b(ax):
    n = np.geomspace(16, 512, 200)
    ymin, ymax = 2 / 512 * 0.7, 0.8
    ax.axhspan(S.ALPHA, ymax, color=S.REFUSED_FILL, lw=0, zorder=0)
    ax.text(500, 0.62, "floor > α: guard refuses", ha="right", va="top", fontsize=6, color=S.INK2)
    ax.axhline(S.ALPHA, color=S.INK2, lw=0.7, ls=(0, (3, 2)), zorder=1)
    ax.text(17, S.ALPHA * 0.88, "α = .05", ha="left", va="top", fontsize=6, color=S.INK2)
    for L, col in L_COLORS.items():
        ax.plot(n, L / n, color=col, lw=1.6, solid_capstyle="round", zorder=2)
        ax.text(512 * 1.08, L / 512, f"L = {L}", va="center", ha="left", fontsize=6, color=S.INK)
        nc = L / S.ALPHA
        ax.plot([nc], [S.ALPHA], marker="o", ms=3.5, mfc=col, mec="white", mew=0.8, zorder=3)
    for nn in S.NS:
        ax.axvline(nn, color=S.GRID, lw=0.6, zorder=0)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlim(16, 512)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([16, 32, 64, 128, 256, 512])
    ax.set_xticklabels(["16", "32", "64", "128", "256", "512"])
    ax.set_yticks([0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5])
    ax.set_yticklabels([".005", ".01", ".02", ".05", ".1", ".2", ".5"])
    ax.minorticks_off()
    ax.grid(axis="y")
    ax.set_xlabel("series length n")
    ax.set_ylabel("smallest attainable p = L/n")
    ax.set_title("(b) Attainable p floor", loc="left")


def panel_c(ax, cells):
    col = S.METHODS["C0"]["color"]
    xs, labels = [], []
    i = 0
    for n in S.NS:
        for L in S.LS:
            c = cells[S.key("C0", "alt", "rho0.6", L, n)]
            x = i
            xs.append(x)
            labels.append(f"n={n}\nL={L}")
            rate = c["rate"] * 100
            if S.refused(L, n):
                ax.axvspan(x - 0.4, x + 0.4, color=S.REFUSED_FILL, lw=0, zorder=0)
                ax.plot([x], [rate], marker="x", ms=4.5, mew=1.0, color=col, zorder=3, clip_on=False)
                ax.text(x, 50, f"refused\nfloor {L}/{n}\n= {L / n:.3f} > α", ha="center",
                        va="center", fontsize=5.8, color=S.INK2)
                ax.text(x, rate + 6, f"{rate:.0f}%", ha="center", va="bottom", fontsize=6, color=S.INK)
            else:
                ax.bar(x, rate, width=0.32, color=col, zorder=2)
                lo, hi = c["cp95_low"] * 100, c["cp95_high"] * 100
                ax.plot([x, x], [lo, hi], color=S.INK, lw=0.8, zorder=3)
                txt = f"{rate:.0f}%" if c["K"] == c["R"] else f"{rate:.1f}%"
                ax.text(x, hi + 2, txt, ha="center", va="bottom", fontsize=6, color=S.INK)
            i += 1
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("rejection rate at ρ = 0.6 (%)")
    ax.set_xlim(-0.6, len(xs) - 0.4)
    ax.set_title("(c) Measured power, SelCal exact", loc="left")


def main():
    S.setup()
    cells = S.load_cells()
    fig = plt.figure(figsize=(S.DOUBLE_W, 11.0 * S.CM))
    gs = fig.add_gridspec(2, 2, height_ratios=[0.62, 1.0], hspace=0.55, wspace=0.42)
    ax_a = fig.add_subplot(gs[0, :])
    panel_a(ax_a)
    ax_a.set_anchor("W")
    panel_b(fig.add_subplot(gs[1, 0]))
    panel_c(fig.add_subplot(gs[1, 1]), cells)
    S.save(fig, "fig2_guard")


if __name__ == "__main__":
    main()
