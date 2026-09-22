"""Fig. 3: false-positive rate (size) with 95% Clopper-Pearson intervals.

Reads results_stage2_analysis.json and results_idtxl_analysis.json directly.
Run: <python> docs/manuscript/figures/fig3_size.py
"""
import matplotlib.pyplot as plt

import _style as S


def main():
    S.setup()
    cells = S.load_cells()
    ymax = max(c["cp95_high"] for k, c in cells.items() if "|alt|" not in k) * 100
    ylim = (0, (int(ymax / 5) + 1) * 5)
    fig, axes = plt.subplots(2, 3, figsize=(S.DOUBLE_W, 9.0 * S.CM), sharey=True)
    for r, L in enumerate(S.LS):
        for c, (cell, cname) in enumerate(S.NULLS):
            ax = axes[r, c]
            ax.axhline(S.ALPHA * 100, color=S.INK2, lw=0.7, ls=(0, (3, 2)), zorder=1)
            S.dot_interval_panel(ax, cells, cell, "rho-", L, ylim=ylim, refused_label_y=1.4)
            if r == 0:
                ax.set_title(cname)
            if c == 0:
                ax.set_ylabel(f"L = {L} lags searched\nfalse-positive rate (%)")
            if r == 0 and c == 0:
                ax.text(1.5, S.ALPHA * 100 + 0.4, "nominal 5%", ha="right", va="bottom",
                        fontsize=6, color=S.INK2)
    fig.legend(handles=S.method_legend_handles(), loc="lower center", ncol=3,
               bbox_to_anchor=(0.5, 1.0), frameon=False, handlelength=1.8, columnspacing=1.4)
    fig.tight_layout(h_pad=0.8, w_pad=0.6)
    S.save(fig, "fig3_size")


if __name__ == "__main__":
    main()
