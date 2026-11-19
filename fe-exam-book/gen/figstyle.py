"""Shared visual style for every illustration in the book."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

GYRE = "/usr/share/texmf/fonts/opentype/public/tex-gyre/"
for f in ["texgyrepagella-regular.otf", "texgyrepagella-bold.otf", "texgyrepagella-italic.otf", "texgyrepagella-bolditalic.otf"]:
    p = os.path.join(GYRE, f)
    if os.path.exists(p):
        font_manager.fontManager.addfont(p)

INK = "#14284B"      # deep navy
COPPER = "#B5651D"   # copper accent
TEAL = "#2E6B4F"
RED = "#9E2B25"
GREY = "#6B6B6B"
LIGHT = "#F3F1EC"
PALETTE = [INK, COPPER, TEAL, RED, "#5B4B8A", GREY]

plt.rcParams.update({
    "font.family": "TeX Gyre Pagella",
    "mathtext.fontset": "stix",
    "font.size": 10.5,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8,
    "axes.labelcolor": "#222222",
    "axes.titlesize": 11.5,
    "axes.titleweight": "bold",
    "axes.titlecolor": INK,
    "axes.prop_cycle": matplotlib.cycler(color=PALETTE),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.6,
    "legend.frameon": False,
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "lines.linewidth": 1.8,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06,
    "figure.facecolor": "white",
})

import schemdraw
schemdraw.use("matplotlib")
schemdraw.config(font="TeX Gyre Pagella", fontsize=11, lw=1.4, color="#1a1a1a")
