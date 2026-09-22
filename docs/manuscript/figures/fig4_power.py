"""Fig. 4: power (rejection rate under the alternative) with 95% CP intervals.

Reads results_stage2_analysis.json and results_idtxl_analysis.json directly.
Run: <python> docs/manuscript/figures/fig4_power.py
"""
import matplotlib.pyplot as plt

import _style as S

RHOS = [("rho0.3", "ρ = 0.3"), ("rho0.6", "ρ = 0.6")]


def main():
    S.setup()
    cells = S.load_cells()
    fig, axes = plt.subplots(2, 2, figsize=(S.DOUBLE_W, 9.0 * S.CM), sharey=True)
    for r, (rho, rname) in enumerate(RHOS):
        for c, L in enumerate(S.LS):
            ax = axes[r, c]
            S.dot_interval_panel(ax, cells, "alt", rho, L, ylim=(-3, 103), refused_label_y=22)
            ax.set_yticks([0, 25, 50, 75, 100])
            if r == 0:
                ax.set_title(f"L = {L} lags searched")
            if c == 0:
                ax.set_ylabel(f"{rname}\nrejection rate (%)")
    fig.legend(handles=S.method_legend_handles(), loc="lower center", ncol=3,
               bbox_to_anchor=(0.5, 1.0), frameon=False, handlelength=1.8, columnspacing=1.4,
               title="alternatives: independent noise, signal at the last searched lag",
               title_fontproperties={"size": 6.3, "style": "italic"})
    fig.tight_layout(h_pad=0.8, w_pad=1.0)
    S.save(fig, "fig4_power")


if __name__ == "__main__":
    main()
