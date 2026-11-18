"""Shared helpers for drawing the book's illustrations.

Every figure is saved twice: as SVG (vector, for the print PDF) and as a
high-resolution PNG (for the EPUB, where some readers handle SVG poorly).
"""
import glob
import os

import matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
for f in glob.glob(os.path.join(HERE, "fonts", "*.ttf")):
    font_manager.fontManager.addfont(f)

import matplotlib.pyplot as plt  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402,F401

FONT = "Source Sans 3"
plt.rcParams.update({
    "font.family": FONT,
    "font.size": 11,
    "svg.fonttype": "path",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#33415c",
    "axes.labelcolor": "#1b263b",
    "xtick.color": "#33415c",
    "ytick.color": "#33415c",
})

schemdraw.use("matplotlib")
schemdraw.config(fontsize=12, font=FONT, lw=1.5, inches_per_unit=0.5)

NAVY = "#1d3557"
COPPER = "#c0602a"
TEAL = "#2a7f62"
GREY = "#6c757d"
LIGHT = "#e9eef5"
RED = "#b23a48"

FIGDIR = os.path.join(HERE, "fig")
os.makedirs(FIGDIR, exist_ok=True)


def save_drawing(d, name):
    d.save(os.path.join(FIGDIR, name + ".svg"), transparent=False)
    d.save(os.path.join(FIGDIR, name + ".png"), dpi=220, transparent=False)


def save_fig(fig, name):
    fig.savefig(os.path.join(FIGDIR, name + ".svg"), bbox_inches="tight", facecolor="white")
    fig.savefig(os.path.join(FIGDIR, name + ".png"), dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def drawing():
    return schemdraw.Drawing(show=False)
