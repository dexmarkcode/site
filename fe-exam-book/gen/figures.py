"""All chapter illustrations. Run: python3 figures.py [name ...]"""
import os
import sys
import numpy as np
import figstyle
from figstyle import INK, COPPER, TEAL, RED, GREY, LIGHT
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon, Arc
import schemdraw
import schemdraw.elements as elm
import schemdraw.logic as logic

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
FIGS = {}


def fig(name):
    def deco(f):
        FIGS[name] = f
        return f
    return deco


def save(f, name):
    f.savefig(os.path.join(OUT, name + ".png"))
    plt.close("all")


def sch_save(d, name):
    d.save(os.path.join(OUT, name + ".png"), dpi=260)
    plt.close("all")


def box(ax, x, y, w, h, text, fc=LIGHT, ec=INK, fs=10, tc="#1a1a1a", bold=False, rs=0.08):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={rs}", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold" if bold else "normal")


def arrow(ax, p, q, color=INK, lw=1.3, style="-|>", ms=12, cs="arc3"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, connectionstyle=cs))


def blank(w, h):
    f, ax = plt.subplots(figsize=(w, h))
    ax.axis("off")
    ax.grid(False)
    return f, ax


# ------------------------------------------------------------------ Chapter 1
@fig("fig01_blueprint")
def _():
    areas = [("Mathematics", 11, 17), ("Probability and Statistics", 4, 6), ("Ethics and Professional Practice", 3, 5),
             ("Engineering Economics", 3, 5), ("Properties of Electrical Materials", 4, 6), ("Circuit Analysis (DC and AC)", 15, 23),
             ("Linear Systems", 5, 8), ("Signal Processing", 5, 8), ("Electronics", 7, 11), ("Power Systems", 8, 12),
             ("Electromagnetics", 5, 8), ("Control Systems", 6, 9), ("Communications", 5, 8), ("Computer Networks", 3, 5),
             ("Digital Systems", 8, 12), ("Computer Systems", 5, 8), ("Software Engineering", 4, 6)]
    f, ax = plt.subplots(figsize=(6.6, 5.4))
    names = [a[0] for a in areas][::-1]
    lo = np.array([a[1] for a in areas][::-1])
    hi = np.array([a[2] for a in areas][::-1])
    mid = (lo + hi) / 2
    comp = {"Computer Networks", "Digital Systems", "Computer Systems", "Software Engineering"}
    gen = {"Mathematics", "Probability and Statistics", "Ethics and Professional Practice", "Engineering Economics"}
    cols = [TEAL if n in comp else (GREY if n in gen else INK) for n in names]
    cols = [COPPER if n.startswith("Circuit") else c for c, n in zip(cols, names)]
    y = np.arange(len(names))
    ax.barh(y, mid, color=cols, height=0.66, alpha=0.92)
    ax.errorbar(mid, y, xerr=[mid - lo, hi - mid], fmt="none", ecolor="#333333", elinewidth=0.9, capsize=2.5)
    for yi, m, l, h in zip(y, mid, lo, hi):
        ax.text(h + 0.4, yi, f"{l}–{h}", va="center", fontsize=8.5, color="#333333")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9.5)
    ax.set_xlabel("Number of questions (bar = midpoint; whiskers = NCEES range)")
    ax.set_xlim(0, 26)
    ax.grid(axis="y", visible=False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=GREY, label="General"), Patch(color=COPPER, label="Circuits"), Patch(color=INK, label="Electrical"),
                       Patch(color=TEAL, label="Computing")], loc="lower right", fontsize=9)
    save(f, "fig01_blueprint")


@fig("fig01_studyplan")
def _():
    tasks = [("Part I  Foundations, maths, prob/econ/ethics", 0, 2, GREY), ("Part II  Circuits, AC power, transients", 2, 2.5, COPPER),
             ("Part III  Signals, electronics, EM & materials", 4.5, 2, INK), ("Part IV  Power, control, communications", 6.5, 2, INK),
             ("Part V  Digital, computer systems, networks, software", 8.5, 1.5, TEAL), ("Mixed review (20 min, twice weekly)", 3, 7, "#8FA9D6"),
             ("Chapter 16 strategy and timed drill", 9.5, 0.5, RED), ("Mock exam 1 and repair", 10, 1, RED), ("Mock exam 2, error log, rest", 11, 1, RED)]
    f, ax = plt.subplots(figsize=(6.8, 3.4))
    for i, (t, s, d, c) in enumerate(tasks):
        y = len(tasks) - i
        ax.barh(y, d, left=s, color=c, height=0.62, alpha=0.9)
        ax.text(s + 0.08 if s < 7 else s - 0.08, y, t, va="center", ha="left" if s < 7 else "right", fontsize=8.6,
                color="white" if (d > 3.5) else "#1a1a1a")
    ax.set_xlim(0, 12)
    ax.set_xticks(np.arange(0, 13))
    ax.set_xticklabels([""] + [f"Wk {i}" for i in range(1, 13)], fontsize=8)
    ax.set_yticks([])
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    for t, s, d, c in tasks:
        pass
    # fix labels that do not fit inside bars
    save(f, "fig01_studyplan")


if __name__ == "__main__":
    names = sys.argv[1:] or list(FIGS)
    for n in names:
        FIGS[n]()
        print("made", n)
