"""Shared drawing helpers so every illustration in the book has one visual language."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon, Arc, Wedge
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
for f in (ROOT / "fonts").glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))

NAVY = "#12263a"; TEAL = "#0b7a8a"; AMBER = "#c9861a"; GREY = "#7c8a92"; LIGHT = "#eef5f6"
RED = "#b8433a"; GREEN = "#3c8d4f"; SKY = "#7fd3dc"; PALE = "#fbf5ea"; INK = "#1c1c1c"
SERIES = [TEAL, AMBER, NAVY, RED, GREEN, GREY]

plt.rcParams.update({
    "font.family": "Source Sans 3", "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
    "axes.edgecolor": "#55636b", "axes.linewidth": 0.7, "axes.labelcolor": INK,
    "xtick.color": "#3d4a51", "ytick.color": "#3d4a51", "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": "#dfe6ea", "grid.linewidth": 0.5, "legend.fontsize": 7.5, "legend.frameon": False,
    "lines.linewidth": 1.6, "mathtext.fontset": "stix", "savefig.dpi": 300,
})
W = 4.5  # text block width in inches


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", pad_inches=0.04, facecolor="white")
    plt.close(fig)
    print("saved", name)


def canvas(w=W, h=2.6, xlim=(0, 100), ylim=None):
    fig, ax = plt.subplots(figsize=(w, h))
    if ylim is None:
        ylim = (0, 100 * h / w)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text="", fc=LIGHT, ec=NAVY, tc=NAVY, fs=7.5, bold=True, r=1.2, lw=0.9, **kw):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, **kw)
    ax.add_patch(p)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
                fontweight="semibold" if bold else "normal", linespacing=1.15)
    return p


def arrow(ax, x1, y1, x2, y2, c=TEAL, lw=1.6, style="-|>", ms=8, ls="-", both=False, **kw):
    st = "<|-|>" if both else style
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=st, mutation_scale=ms, color=c, lw=lw, linestyle=ls,
                        shrinkA=0, shrinkB=0, **kw)
    ax.add_patch(a)
    return a


def line(ax, xs, ys, c=NAVY, lw=1.0, **kw):
    ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round", **kw)


def label(ax, x, y, s, fs=7, c=INK, ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va, **kw)
