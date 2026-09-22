"""Fig. 5: real-case re-analysis (Kerala dengue vs Nino 3.4 SST, Yacob et al. 2026).

(a) the two deposited series over the paper's window 2006-06..2016-12 (two panels,
    one y-scale each; no dual axis);
(b) p-value of the same lag-scan claim under four procedures, raw series (A1) and
    deseasonalised series (A2), read from results.json.
Run: <python> docs/manuscript/figures/fig5_real_case.py
"""
import csv
import json
from datetime import date

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

import _style as S

CASE = S.REPO / "docs" / "status" / "evidence" / "real_case_20260922"
RESULTS_JSON = CASE / "results.json"
DATA_CSV = CASE / "data" / "Climate_dengue_data_Kerala_paper.csv"
DATA_SHA = "91fac1a7f6c7b893c2065726f4b26aeb9301dd8aec7a6bbd8bcb68780074289b"

# Uncorrected textbook Pearson p (published practice and best lag) share one hue
# (dataviz slot 7, violet) and differ by marker; Bonferroni and SelCal keep the
# colours of Figs. 2-4. Palette violet/orange/blue checked with validate_palette.js
# (light, all pairs: worst CVD dE 13.0, normal-vision dE 16.3, all >= 3:1).
VIOLET = "#4a3aa7"
PROCS = [
    ("A0", dict(color=VIOLET, marker="D", filled=False,
                label="Published practice: best lag, textbook p (lags 0–5, 127 rows)")),
    ("TB", dict(color=VIOLET, marker="v", filled=True,
                label="Best lag, textbook p (lags 1–5, 122 pairs)")),
    ("BF", dict(color=S.METHODS["C2"]["color"], marker=S.METHODS["C2"]["marker"], filled=True,
                label="Bonferroni ×5 (best lag)")),
    ("SC", dict(color=S.METHODS["C0"]["color"], marker=S.METHODS["C0"]["marker"], filled=True,
                label="SelCal exact circular enumeration (B = 126)")),
]


def load_series():
    if S.sha256(DATA_CSV) != DATA_SHA:
        raise ValueError("deposit checksum mismatch")
    rows = [r for r in csv.DictReader(DATA_CSV.open()) if "2006-06-30" <= r["index"] <= "2016-12-31"]
    if len(rows) != 127:
        raise ValueError("unexpected window length")
    t = [date.fromisoformat(r["index"]) for r in rows]
    return t, [float(r["nino0"]) for r in rows], [float(r["dengue"]) for r in rows]


def points(res):
    out = {}
    a0 = res["A0_published_practice"]["best"]
    out[("A1", "A0")] = (a0["p_two_sided"], a0["lag"])
    for grp, k in (("A1", "A1_raw"), ("A2", "A2_deseasonalised")):
        c, s = res[k]["comparators"], res[k]["selcal"]
        lag = c["best_lag_textbook"]["lag"]
        out[(grp, "TB")] = (c["best_lag_textbook"]["p_two_sided"], lag)
        out[(grp, "BF")] = (c["bonferroni_p"], lag)
        out[(grp, "SC")] = (s["p_value"], s["selected_lag"])
    return out


def fmt_p(p):
    if p >= 0.01:
        return f"{p:.3f}".lstrip("0") if p < 0.1 else f"{p:.2f}".lstrip("0")
    m, e = f"{p:.1e}".split("e")
    return f"{m}×10$^{{{int(e)}}}$"


def panel_series(ax_x, ax_y, t, x, y):
    for ax, v, lab in ((ax_x, x, "Niño 3.4 SST (°C)"), (ax_y, y, "dengue cases / month")):
        ax.plot(t, v, color=S.INK2, lw=1.0, solid_joinstyle="round")
        ax.set_ylabel(lab)
        ax.grid(axis="y")
        ax.set_xlim(t[0], t[-1])
    for yr in range(2007, 2017):
        for ax in (ax_x, ax_y):
            ax.axvline(date(yr, 1, 1), color=S.GRID, lw=0.5, zorder=0)
    ax_x.tick_params(axis="x", labelbottom=False)
    ax_y.xaxis.set_major_locator(mdates.YearLocator(2))
    ax_y.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax_y.set_ylim(bottom=0)
    ax_x.set_title("(a) Deposited series, 2006-06 to 2016-12 (n = 127)", loc="left")


# protocol.md designates A1 as the primary SelCal run and A2 as the pre-declared
# assumption-respecting variant; the group title follows the frozen protocol.
A2_TITLE = "A2  detrended, deseasonalised (pre-declared variant)"
MAX_LAG = 5  # SelCal and comparator lag set 1..5; lag 5 is its upper edge

SHORT = {"A0": "Published practice\n(lags 0–5, 127 rows)", "TB": "Best lag, textbook p",
         "BF": "Bonferroni ×5", "SC": "SelCal exact"}


def panel_p(ax, pts):
    """Horizontal dot plot: one row per procedure, grouped by series; direct labels."""
    groups = [("A2", A2_TITLE), ("A1", "A1  series as deposited")]
    xmin, xmax = 1e-5, 1.0
    ax.set_xscale("log")
    rows, heads, y = [], [], 0.0
    for g, head in groups:
        heads.append((y, head))
        y += 1.0
        for code, spec in PROCS:
            rows.append((y, g, code, spec))
            y += 1.0
        y += 0.5
    # alpha reference drawn per group, across the data rows only, so headers stay clear
    for yy, _ in heads:
        ax.plot([S.ALPHA, S.ALPHA], [yy + 0.5, yy + len(PROCS) + 0.5], color=S.INK2, lw=0.7,
                ls=(0, (3, 2)), zorder=1)
    ax.text(S.ALPHA, y - 0.2, "α = .05", ha="center", va="bottom", fontsize=6, color=S.INK2)
    for yy, head in heads:
        ax.text(xmin, yy, head, ha="left", va="center", fontsize=6.8, color=S.INK, weight="bold")
    for yy, g, code, spec in rows:
        if (g, code) not in pts:
            ax.text(xmin * 1.3, yy, "not defined (no lag columns)",
                    ha="left", va="center", fontsize=5.8, color=S.MUTED)
            continue
        p, lag = pts[(g, code)]
        ax.plot([xmin, p], [yy, yy], color=spec["color"], lw=0.6, alpha=0.35, zorder=1,
                solid_capstyle="butt")
        ax.plot([p], [yy], marker=spec["marker"], ms=5 if spec["marker"] != "D" else 4.3,
                mfc=spec["color"] if spec["filled"] else "white",
                mec="white" if spec["filled"] else spec["color"],
                mew=0.6 if spec["filled"] else 1.0, ls="none", zorder=3)
        edge = " (edge)" if lag == MAX_LAG else ""
        txt = f"lag {lag}{edge},  p = {fmt_p(p)}"
        if 1e-3 < p <= S.ALPHA:  # left of the marker, over its own stem, clear of the alpha line
            ax.text(p / 1.45, yy, txt, ha="right", va="center", fontsize=6, color=S.INK, zorder=4,
                    bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
        else:  # right of the marker; above alpha this runs past p = 1 into the right margin
            ax.text(p * 1.45, yy, txt, ha="left", va="center", fontsize=6, color=S.INK, zorder=4,
                    clip_on=False)
    ax.set_yticks([r[0] for r in rows])
    ax.set_yticklabels([SHORT[r[2]] for r in rows], linespacing=1.0)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(y - 0.2, -1.5)
    ax.set_xlim(xmin, xmax)
    ax.set_xticks([1e-5, 1e-4, 1e-3, 1e-2, 0.05, 1.0])
    ax.set_xticklabels(["10$^{-5}$", "10$^{-4}$", "10$^{-3}$", ".01", ".05", "1"])
    ax.minorticks_off()
    ax.grid(False)
    ax.grid(axis="x")
    ax.set_xlabel("p-value (log scale)")
    ax.set_title("(b) p-value for the best-lag correlation", loc="left")


def main():
    S.setup()
    res = json.loads(RESULTS_JSON.read_text())
    t, x, y = load_series()
    fig = plt.figure(figsize=(S.DOUBLE_W, 8.2 * S.CM))
    gs = fig.add_gridspec(2, 2, width_ratios=[0.8, 1.2], wspace=0.42, hspace=0.12,
                          right=0.84)
    ax_x = fig.add_subplot(gs[0, 0])
    ax_y = fig.add_subplot(gs[1, 0], sharex=ax_x)
    panel_series(ax_x, ax_y, t, x, y)
    ax_p = fig.add_subplot(gs[:, 1])
    panel_p(ax_p, points(res))
    S.save(fig, "fig5_real_case")


if __name__ == "__main__":
    main()
