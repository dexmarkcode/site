from common import *
from matplotlib.patches import FancyBboxPatch


def rbox(ax, x, y, w, h, text, fs=5.8, fill=WH, lw=0.8, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fill, ec=K, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=4, linespacing=1.1,
            fontweight="bold" if bold else "normal")


def flowchart(name, symptoms, faults, links, h=3.0):
    fig, ax = canvas(W, h, xlim=(0, 150), ylim=(0, 100 * h / 3.0))
    top = 100 * h / 3.0
    ns, nf = len(symptoms), len(faults)
    ys = [top - 8 - i * (top - 12) / ns for i in range(ns)]
    yf = [top - 6 - i * (top - 8) / nf for i in range(nf)]
    for y, s in zip(ys, symptoms):
        rbox(ax, 2, y - 5, 50, 10, s, fill=G1, bold=True)
    for y, f in zip(yf, faults):
        rbox(ax, 92, y - 3.6, 56, 7.2, f)
    for a, bs in links.items():
        for b in bs:
            ax.plot([52, 92], [ys[a], yf[b]], color=K, lw=0.5, zorder=1)
    ax.text(27, top - 1, "SYMPTOM", ha="center", fontsize=5.6, fontweight="bold")
    ax.text(120, top + 1.5, "LIKELY FAULT", ha="center", fontsize=5.6, fontweight="bold")
    save(fig, name)


flowchart("fig19_1",
          ["Sways when pushed\nsideways", "Rocks back when\npushed from front", "Knees ache\nafter practice",
           "Calves or feet\ncramp", "Head bobs\nwhen stepping", "Stance changes\nby end of kata"],
          ["19.1 Stance too long", "19.3 Stance too narrow", "19.4 Front foot angle", "19.6 Toes curling",
           "19.7 Outer edges / arches", "19.8 Rear heel lifting", "19.9 Knees too straight", "19.10 Stance too deep",
           "19.12 Knees collapsing in", "19.13 Uneven weight", "19.14 Stance drifting", "19.15 Stepping faults"],
          {0: [0, 1], 1: [5, 9, 6], 2: [2, 7, 8, 4], 3: [3, 4], 4: [11, 6], 5: [10, 7]})

# Figure 19.2 top views
L, WD = 15.0, 20.0
fig, ax = canvas(W, 1.7, xlim=(0, 200), ylim=(-12, 50))
cfg = [("Too long", 1.8 * L, WD, False), ("Too wide", L, 1.9 * WD, False), ("Too narrow", L, 0.35 * WD, False), ("Correct", L, WD, True)]
for i, (cap, ln, wd, ok) in enumerate(cfg):
    cx = 25 + i * 50
    fh = (cx + wd / 2, 2 + ln); rh = (cx - wd / 2, 2)
    foot_top(ax, fh, -25, L, left=False, toes=False, lw=0.8)
    foot_top(ax, rh, 6, L, left=True, toes=False, lw=0.8)
    for h in (fh, rh):
        ax.plot([h[0], h[0]], [-2, 46], color=K, lw=0.4, ls=(0, (2, 2)))
    ax.plot([cx - 24, cx + 24], [2 + L, 2 + L], color=K, lw=0.4, ls=(0, (1, 1.5)))
    (tick_mark if ok else cross_mark)(ax, cx - 20, 44, r=3)
    sub_label(ax, cx, -4, cap, fs=6.2)
save(fig, "fig19_2")

# Figure 19.3 side faults
fig, ax = canvas(W, 2.1, xlim=(0, 200), ylim=(-12, 104))
floor(ax, 2, 198)
heel = Pose("tsuki", "uke", "sanchin", "R", lean=3)
heel.j["lank"] = heel.j["lank"] + v(0, 2, 4)
cfg = [(Pose("uke", "uke", "sanchin_straight", "R"), "Knees too straight", False),
       (Pose("uke", "uke", "sanchin_deep", "R"), "Too deep", False),
       (heel, "Rear heel lifting", False),
       (Pose("uke", "uke", "sanchin", "R"), "Correct", True)]
for i, (pp, cap, ok) in enumerate(cfg):
    x = 25 + i * 50
    Figure(ax, pp, ox=x, th=-90, sc=0.95)
    (tick_mark if ok else cross_mark)(ax, x - 20, 96, r=3.2)
    sub_label(ax, x, -3, cap, fs=6.2)
save(fig, "fig19_3")
