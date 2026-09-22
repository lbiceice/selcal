"""Fig. 1: SelCal architecture and data flow (schematic, no data).

Names follow the code: CLI commands in src/selcal/cli.py; validate_files / preflight /
attainability / run_files / verify_record / report_record in workflow.py; resolve_plan_v2
in resolution_v2.py; calibrate_selected_family in calibration_v2.py;
verify_calibration_result in contracts_v2.py; SQLite record in workflow_store.py.
Exit codes: 2 = invalid request or plan not executable (validate) / unattainable plan
refused (run); 7 = NOT_EVALUABLE result (run, verify, report).
Run: <python> docs/manuscript/figures/fig1_architecture.py
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

import _style as S

W, H = 17.5, 8.9  # cm; axes in cm units
BLUE = S.METHODS["C0"]["color"]
BLUE_TINT = "#e8f1fc"
CRIT = "#d03b3b"  # dataviz status "critical"; always paired with an exit-code label


def box(ax, x, y, w, h, *, fc="white", ec=S.AXIS, lw=0.7, r=0.12, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def txt(ax, x, y, s, *, size=6.2, color=S.INK, ha="left", va="top", mono=False, bold=False, z=5, **kw):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=z,
            fontweight="bold" if bold else "normal", linespacing=1.25,
            **({"fontfamily": "monospace"} if mono else {}), **kw)


def arrow(ax, p0, p1, *, color=S.INK2, lw=0.8, ls="-", z=3, rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=6, color=color, lw=lw,
                                 ls=ls, zorder=z, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))


def badge(ax, x, y, label, *, filled):
    """Exit-code badge: filled = guard refusal (exit 2); outlined = NOT_EVALUABLE (exit 7)."""
    ax.text(x, y, label, fontsize=5.8, ha="center", va="center", zorder=7, fontweight="bold",
            color="white" if filled else CRIT,
            bbox=dict(boxstyle="round,pad=0.25,rounding_size=0.35",
                      fc=CRIT if filled else "white", ec=CRIT, lw=0.8))


def stage_header(ax, x, y, title, *, mono=True):
    txt(ax, x, y, title, size=7, bold=True, mono=mono, va="baseline")


def elbow(ax, pts, *, color=S.INK2, lw=0.8):
    """Orthogonal connector through pts; arrowhead on the last segment."""
    xs, ys = zip(*pts[:-1])
    ax.plot(xs, ys, color=color, lw=lw, zorder=3, solid_joinstyle="miter")
    arrow(ax, pts[-2], pts[-1], color=color, lw=lw)


def main():
    S.setup()
    fig = plt.figure(figsize=(W * S.CM, H * S.CM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    hy, top = H - 0.45, H - 0.75  # header baseline, content top

    # ------------------------------------------------------------------ A: inputs
    ax0, aw = 0.1, 2.6
    stage_header(ax, ax0, hy, "Inputs", mono=False)
    box(ax, ax0, top - 1.3, aw, 1.3)
    txt(ax, ax0 + 0.15, top - 0.15, "Series file", bold=True)
    txt(ax, ax0 + 0.15, top - 0.53, "CSV or NPZ\nsource x, target y", color=S.INK2)
    p_top = top - 1.75
    box(ax, ax0, p_top - 2.3, aw, 2.3)
    txt(ax, ax0 + 0.15, p_top - 0.15, "Plan file (JSON)", bold=True)
    txt(ax, ax0 + 0.15, p_top - 0.53, "statistic, lag set\nselection rule\nnull model\nα, replicates B, seed",
        color=S.INK2)

    # ------------------------------------------------------ B: validate (preflight)
    bx, bw = 3.25, 3.6
    stage_header(ax, bx, hy, "selcal validate")
    rows = [  # (title, body, top, height)
        ("1  Input valid?", "series loads, passes checks", top, 1.2),
        ("2  Plan executable?", "resource budget within caps\nsmallest attainable p ≤ α", top - 1.45, 2.3),
        ("3  Scientific assumptions", "declared, not verified;\nthe analyst must justify them", top - 4.0, 1.3),
    ]
    for title, body, y_top, h in rows:
        box(ax, bx, y_top - h, bw, h)
        txt(ax, bx + 0.15, y_top - 0.15, title, bold=True)
        txt(ax, bx + 0.15, y_top - 0.53, body, color=S.INK2)
    badge(ax, bx + bw - 0.45, rows[0][2] - 0.3, "exit 2", filled=True)
    badge(ax, bx + bw - 0.45, rows[1][2] - 0.3, "exit 2", filled=True)
    txt(ax, bx + 0.15, rows[1][2] - 1.45, "else NOT_EXECUTABLE, e.g.\nREFUSE_NULL_STATES_TOO_FEW",
        size=5.2, color=CRIT, mono=True)
    arrow(ax, (ax0 + aw, top - 0.65), (bx, top - 0.65))
    elbow(ax, [(ax0 + aw, p_top - 1.15), (ax0 + aw + 0.27, p_top - 1.15),
               (ax0 + aw + 0.27, rows[1][2] - 1.15), (bx, rows[1][2] - 1.15)])
    elbow(ax, [(ax0 + aw + 0.27, p_top - 1.15), (ax0 + aw + 0.27, rows[2][2] - 0.65),
               (bx, rows[2][2] - 0.65)])

    # key for the exit-code badges (bottom left)
    ky = 1.45
    txt(ax, ax0, ky + 0.45, "Where SelCal stops", bold=True)
    badge(ax, ax0 + 0.42, ky - 0.05, "exit 2", filled=True)
    txt(ax, ax0 + 0.95, ky - 0.05, "guard refuses before any calibration: invalid input, or plan\n"
        "not executable (budget, unattainable p); nothing is recorded", va="center", color=S.INK2, size=5.8)
    badge(ax, ax0 + 0.42, ky - 0.85, "exit 7", filled=False)
    txt(ax, ax0 + 0.95, ky - 0.85, "NOT_EVALUABLE: a failure (null binding, observed scan or any\n"
        "replicate) is kept in the result; no p-value is reported", va="center", color=S.INK2, size=5.8)

    # ---------------------------------------------------------------------- C: run
    cx, cw = 7.4, 5.6
    ix, iw = cx + 0.15, cw - 0.3
    stage_header(ax, cx, hy, "selcal run")
    box(ax, cx, 0.15, cw, top - 0.15)
    txt(ax, ix, top - 0.12, "reads the same files and repeats preflight;\n"
        "an unattainable plan is refused unless\n--allow-unattainable-plan", size=5.6, color=S.INK2)
    badge(ax, cx + cw - 0.5, top - 0.4, "exit 2", filled=True)
    arrow(ax, (bx + bw, rows[1][2] - 0.4), (cx, rows[1][2] - 0.4))

    r_top = top - 0.95
    box(ax, ix, r_top - 1.7, iw, 1.7)
    txt(ax, ix + 0.15, r_top - 0.12, "resolve_plan_v2", mono=True, bold=True)
    txt(ax, ix + 0.15, r_top - 0.48,
        "statistic  lagged_pearson_v1\n"
        "           equal_width_binned_nette_v1\n"
        "null       circular_shift_exact_v1 (exact)\n"
        "           circular_shift_v2 (sampled)\n"
        "           block_shuffle_v2", size=5.0, mono=True, color=S.INK2)

    c_top = r_top - 1.95
    c_bot = 1.6
    arrow(ax, (cx + cw / 2, r_top - 1.7), (cx + cw / 2, c_top))
    box(ax, ix, c_bot, iw, c_top - c_bot, fc=BLUE_TINT, ec=BLUE, lw=0.9)
    txt(ax, ix + 0.15, c_top - 0.12, "calibrate_selected_family", mono=True, bold=True)
    txt(ax, ix + 0.15, c_top - 0.5, "bind null; observed data: scan every lag,\nselect c*, keep T_obs")
    rx, rw, rh = ix + 0.3, iw - 0.9, 1.3
    ry = c_top - 1.35 - 0.24 - rh
    for k in (2, 1):
        box(ax, rx + 0.12 * k, ry + 0.12 * k, rw, rh, fc="white", ec=BLUE, lw=0.5, z=2)
    box(ax, rx, ry, rw, rh, fc="white", ec=BLUE, lw=0.8, z=3)
    txt(ax, rx + 0.15, ry + rh - 0.12, "each replicate b = 1 … B", bold=True, z=6)
    txt(ax, rx + 0.15, ry + rh - 0.48, "transform series → scan all lags\n→ reselect → T_b; failures kept",
        color=S.INK2, z=6)
    txt(ax, ix + 0.15, ry - 0.12, "E = #{b : T_b ≥ T_obs},   p = (1 + E) / (B + 1)")

    res_top = c_bot - 0.25
    arrow(ax, (cx + cw / 2, c_bot), (cx + cw / 2, res_top))
    box(ax, ix, 0.3, iw, res_top - 0.3)
    txt(ax, ix + 0.15, res_top - 0.1, "CalibrationResult → verify_calibration_result", mono=True,
        bold=True, size=5.2)
    txt(ax, ix + 0.15, res_top - 0.42, "COMPLETE: p and decision\nor NOT_EVALUABLE: no p",
        color=S.INK2, size=5.8)
    badge(ax, cx + cw - 0.5, 0.62, "exit 7", filled=False)

    # ------------------------------------------------------------- D: record, checks
    dx, dw = 13.55, 3.85
    stage_header(ax, dx, hy, "SQLite record", mono=False)
    rec_bot = top - 2.85
    box(ax, dx, rec_bot, dw, 2.85, fc=S.REFUSED_FILL)
    txt(ax, dx + 0.15, top - 0.12, "one file, four members", bold=True)
    for i, m in enumerate(["input (raw bytes)", "request (plan)", "result", "software identity"]):
        yy = top - 0.55 - i * 0.55
        box(ax, dx + 0.15, yy - 0.42, dw - 0.3, 0.42, fc="white", lw=0.5)
        txt(ax, dx + 0.3, yy - 0.21, m, va="center", size=6)
    gx = (cx + cw + dx) / 2
    elbow(ax, [(ix + iw, 0.95), (gx, 0.95), (gx, rec_bot + 1.4), (dx, rec_bot + 1.4)])

    outs = [
        ("selcal verify", "consistency check"),
        ("selcal verify --replay", "recompute; must MATCH"),
        ("selcal report", "HTML report"),
    ]
    vx, ox, ow, oh = dx + 0.2, dx + 0.45, dw - 0.45, 0.95
    o_top = rec_bot - 0.3
    mids = []
    for i, (cmd, body) in enumerate(outs):
        y0 = o_top - i * (oh + 0.22)
        box(ax, ox, y0 - oh, ow, oh)
        txt(ax, ox + 0.15, y0 - 0.12, cmd, mono=True, bold=True)
        txt(ax, ox + 0.15, y0 - 0.48, body, color=S.INK2, size=6)
        mids.append(y0 - oh / 2)
    ax.plot([vx, vx], [rec_bot, mids[-1]], color=S.INK2, lw=0.8, zorder=3)
    for m in mids:
        arrow(ax, (vx, m), (ox, m))
    y_note = mids[-1] - oh / 2 - 0.4
    badge(ax, ox + 0.35, y_note, "exit 7", filled=False)
    txt(ax, ox + 0.8, y_note, "if the stored result\nis NOT_EVALUABLE", size=5.6, color=S.INK2, va="center")

    S.save(fig, "fig1_architecture")


if __name__ == "__main__":
    main()
