"""House style for every illustration in the book."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import glob

for f in glob.glob('/usr/share/texlive/texmf-dist/fonts/opentype/public/libertinus-fonts/*.otf') + \
         glob.glob('/usr/share/texlive/texmf-dist/fonts/opentype/public/fira/FiraSans-*.otf'):
    try:
        fm.fontManager.addfont(f)
    except Exception:
        pass

NAVY = '#1d3557'
RUST = '#b5523b'
TEAL = '#2a7f8e'
GOLD = '#c99a2e'
GREY = '#8d99ae'
LIGHT = '#e9eef4'
INK = '#222831'

plt.rcParams.update({
    'font.family': 'Fira Sans',
    'font.size': 9,
    'mathtext.fontset': 'stix',
    'axes.edgecolor': INK,
    'axes.linewidth': 0.7,
    'axes.labelcolor': INK,
    'axes.titlesize': 9.5,
    'axes.titleweight': 'medium',
    'xtick.color': INK,
    'ytick.color': INK,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.color': '#d9dee5',
    'grid.linewidth': 0.5,
    'legend.frameon': False,
    'legend.fontsize': 8,
    'lines.linewidth': 1.6,
    'figure.dpi': 100,
    'savefig.facecolor': 'white',
})


def axes_through_origin(ax):
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')


def stem(ax, nn, vals, color=NAVY, label=None):
    m, st, b = ax.stem(nn, vals, linefmt='-', markerfmt='o', basefmt=' ', label=label)
    plt.setp(st, color=color, linewidth=1.3)
    plt.setp(m, color=color, markersize=4.5, markerfacecolor='white', markeredgewidth=1.3)
    ax.axhline(0, color=INK, lw=0.7)
    return m
