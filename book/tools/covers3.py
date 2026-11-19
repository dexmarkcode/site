"""Three premium cover options, 6 x 9 in at 300 dpi (1800 x 2700 px)."""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gen'))
import figstyle as fs  # registers Libertinus and Fira fonts
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
from matplotlib import patheffects as pe

W, H = 6, 9
OUT = os.path.join(os.path.dirname(__file__), '..', 'output', 'covers')
os.makedirs(OUT, exist_ok=True)
SUB = '600 Practice Problems on Fourier, Laplace,\nand Z-Transform With Step-by-Step Solutions'
AUTHOR = 'MARCUS J. THORNTON PH.D'


def canvas(bg):
    fig = plt.figure(figsize=(W, H), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), W, H, color=bg, zorder=0))
    return fig, ax


def fit(ax, fig, x, y, text, width, **kw):
    """Draw text scaled so that it is exactly `width` inches wide."""
    t = ax.text(x, y, text, fontsize=100, **kw)
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    w_in = bb.width / fig.dpi
    t.set_fontsize(100 * width / w_in)
    return t


def gradient(ax, c1, c2, y0=0, y1=H, n=300, alpha=1.0, z=0.5):
    c1, c2 = np.array(plt.matplotlib.colors.to_rgb(c1)), np.array(plt.matplotlib.colors.to_rgb(c2))
    ys = np.linspace(y0, y1, n + 1)
    for i in range(n):
        f = i / (n - 1)
        ax.add_patch(Rectangle((0, ys[i]), W, ys[i + 1] - ys[i] + 0.002, color=c1 * (1 - f) + c2 * f, lw=0, alpha=alpha, zorder=z))


def badge(ax, x, y, r, fill, ink):
    ax.add_patch(Circle((x, y), r, color=fill, zorder=20))
    ax.add_patch(Circle((x, y), r * 0.88, fill=False, ec=ink, lw=1.0, zorder=21))
    ax.text(x, y + r * 0.18, '600', ha='center', va='center', fontsize=r * 34, color=ink, family='Fira Sans', weight='heavy', zorder=22)
    ax.text(x, y - r * 0.38, 'PROBLEMS', ha='center', va='center', fontsize=r * 10.5, color=ink, family='Fira Sans', weight='bold', zorder=22)


# ------------------------------------------------------------------ Option A
def cover_a():
    """Midnight & Gold: huge bold sans title on deep navy with glowing waveforms."""
    fig, ax = canvas('#0b1626')
    gradient(ax, '#0b1626', '#16294a', 0, H)
    x = np.linspace(0, W, 3000)
    # glowing waves across the lower-middle
    for k, (amp, col, lw, a) in enumerate([(1.05, '#e0a93b', 3.2, 0.95), (0.75, '#5fc3d6', 1.8, 0.8), (0.45, '#e0a93b', 1.0, 0.45)]):
        y = 2.65 + amp * np.exp(-0.18 * abs(x - 3)) * np.sin(6.2 * (x - 3) + k)
        ax.plot(x, y, color=col, lw=lw * 3.5, alpha=0.10, zorder=3, solid_capstyle='round')
        ax.plot(x, y, color=col, lw=lw, alpha=a, zorder=4)
    for nn in np.arange(0.25, W, 0.25):
        v = 0.55 * np.cos(1.7 * nn) * np.exp(-0.1 * nn)
        ax.plot([nn, nn], [1.25, 1.25 + v], color='#c4553d', lw=1.6, alpha=0.85, zorder=4)
        ax.add_patch(Circle((nn, 1.25 + v), 0.04, color='#e2735a', zorder=5))
    ax.plot([0, W], [1.25, 1.25], color='white', alpha=0.15, lw=0.8)
    # title block
    ax.text(0.5, 8.35, 'THE COMPLETE PROBLEM-SOLVING GUIDE', color='#e0a93b', fontsize=10.5, family='Fira Sans', weight='bold', va='center')
    fit(ax, fig, 0.47, 7.45, 'SIGNALS', 5.06, color='white', family='Fira Sans', weight='heavy', va='center')
    fit(ax, fig, 0.47, 6.35, '& SYSTEMS', 5.06, color='white', family='Fira Sans', weight='heavy', va='center')
    fit(ax, fig, 0.5, 5.35, 'WORKBOOK', 5.0, color='#e0a93b', family='Fira Sans', weight='heavy', va='center')
    ax.add_patch(Rectangle((0.5, 4.63), 1.4, 0.06, color='#e0a93b', zorder=6))
    ax.text(0.5, 4.15, SUB, color='#d8e1ec', fontsize=13, family='Libertinus Serif', style='italic', va='center', linespacing=1.35)
    badge(ax, 4.95, 0.62 + 0.0, 0.0001, '#0b1626', '#0b1626')
    ax.add_patch(Rectangle((0, 0), W, 0.72, color='#07101c', zorder=10))
    ax.text(0.5, 0.36, AUTHOR, color='white', fontsize=17, family='Fira Sans', weight='bold', va='center', zorder=11)
    badge(ax, 5.05, 1.95, 0.52, '#e0a93b', '#0b1626')
    return fig


# ------------------------------------------------------------------ Option B
def cover_b():
    """Ivory Classic: academic prestige, black bold serif title, rust and navy line art."""
    fig, ax = canvas('#f4efe4')
    ax.add_patch(Rectangle((0.28, 0.28), W - 0.56, H - 0.56, fill=False, ec='#1d3557', lw=1.6, zorder=2))
    ax.add_patch(Rectangle((0.36, 0.36), W - 0.72, H - 0.72, fill=False, ec='#1d3557', lw=0.6, zorder=2))
    ax.text(W / 2, 8.25, 'A  W O R K B O O K  F O R  E N G I N E E R S', ha='center', color='#b5523b', fontsize=10, family='Fira Sans', weight='bold', va='center')
    fit(ax, fig, W / 2, 7.35, 'SIGNALS', 4.9, ha='center', color='#111827', family='EB Garamond', weight='bold', va='center')
    fit(ax, fig, W / 2, 6.4, 'AND SYSTEMS', 4.9, ha='center', color='#111827', family='EB Garamond', weight='bold', va='center')
    ax.plot([1.1, 2.55], [5.72, 5.72], color='#b5523b', lw=1.4); ax.plot([3.45, 4.9], [5.72, 5.72], color='#b5523b', lw=1.4)
    ax.add_patch(Polygon([[3.0, 5.62], [3.1, 5.72], [3.0, 5.82], [2.9, 5.72]], color='#b5523b'))
    fit(ax, fig, W / 2, 5.12, 'WORKBOOK', 3.9, ha='center', color='#1d3557', family='Fira Sans', weight='heavy', va='center')
    ax.text(W / 2, 4.35, SUB, ha='center', color='#374151', fontsize=12.5, family='Libertinus Serif', style='italic', va='center', linespacing=1.35)
    # line-art panel: s-plane with poles and a damped response
    px0, py0, pw, ph = 0.95, 1.35, 4.1, 2.15
    ax.add_patch(Rectangle((px0, py0), pw, ph, fc='#ebe4d4', ec='#1d3557', lw=0.8, zorder=2))
    xs = np.linspace(px0 + 0.1, px0 + pw - 0.1, 1200)
    tt = (xs - xs[0]) / (xs[-1] - xs[0]) * 10
    ax.plot(xs, py0 + 0.95 + 0.75 * np.exp(-0.3 * tt) * np.cos(3.2 * tt), color='#1d3557', lw=2.0, zorder=3)
    ax.plot(xs, py0 + 0.95 + 0.75 * np.exp(-0.3 * tt), color='#b5523b', lw=1.0, ls='--', zorder=3)
    ax.plot(xs, py0 + 0.95 - 0.75 * np.exp(-0.3 * tt), color='#b5523b', lw=1.0, ls='--', zorder=3)
    ax.plot([px0 + 0.1, px0 + pw - 0.1], [py0 + 0.95, py0 + 0.95], color='#1d3557', lw=0.5, alpha=0.5, zorder=3)
    cx, cy = px0 + pw - 0.55, py0 + ph - 0.48
    ax.add_patch(Circle((cx, cy), 0.32, fill=False, ec='#1d3557', lw=0.8, ls='--', zorder=4))
    for (dx, dy) in [(-0.12, 0.2), (-0.12, -0.2)]:
        ax.plot([cx + dx - 0.05, cx + dx + 0.05], [cy + dy - 0.05, cy + dy + 0.05], color='#b5523b', lw=1.6, zorder=5)
        ax.plot([cx + dx - 0.05, cx + dx + 0.05], [cy + dy + 0.05, cy + dy - 0.05], color='#b5523b', lw=1.6, zorder=5)
    ax.add_patch(Circle((cx + 0.2, cy), 0.04, fill=False, ec='#1d3557', lw=1.2, zorder=5))
    ax.text(W / 2, 0.85, 'MARCUS J. THORNTON', ha='center', color='#111827', fontsize=19, family='EB Garamond', weight='bold', va='center')
    ax.text(W / 2, 0.55, 'Ph.D', ha='center', color='#b5523b', fontsize=11, family='EB Garamond', style='italic', va='center')
    badge(ax, 5.05, 3.62, 0.46, '#b5523b', '#f4efe4')
    return fig


# ------------------------------------------------------------------ Option C
def cover_c():
    """Electric Teal: modern tech look, oversized title over an s-plane grid with neon pulses."""
    fig, ax = canvas('#06222a')
    gradient(ax, '#031418', '#0b3b45', 0, H)
    for xv in np.arange(0, W + 0.01, 0.3):
        ax.plot([xv, xv], [0, H], color='#5fe0d0', alpha=0.05, lw=0.6, zorder=1)
    for yv in np.arange(0, H + 0.01, 0.3):
        ax.plot([0, W], [yv, yv], color='#5fe0d0', alpha=0.05, lw=0.6, zorder=1)
    # big diagonal colour band
    ax.add_patch(Polygon([[0, 3.2], [W, 4.4], [W, 5.0], [0, 3.8]], color='#f2b134', alpha=0.95, zorder=2))
    # neon spectrum
    x = np.linspace(0, W, 2500)
    for k in range(1, 8):
        xc = 0.75 * k - 0.1
        y = 1.0 + 1.6 * np.exp(-((x - xc) / 0.08) ** 2) * (1 / k ** 0.5)
        ax.plot(x, y, color='#5fe0d0', lw=1.4, alpha=0.9, zorder=3)
        ax.plot(x, y, color='#5fe0d0', lw=6, alpha=0.08, zorder=3)
    sinc = 1.0 + 1.25 * np.abs(np.sinc((x - 0.65) / 0.75))
    ax.plot(x, sinc, color='#f2b134', lw=1.0, ls='--', alpha=0.7, zorder=3)
    ax.plot([0, W], [1.0, 1.0], color='white', alpha=0.25, lw=0.8, zorder=3)
    # title
    shadow = [pe.withSimplePatchShadow(offset=(3, -3), shadow_rgbFace='black', alpha=0.45)]
    fit(ax, fig, 0.42, 7.95, 'SIGNALS', 5.16, color='white', family='Fira Sans', weight='heavy', va='center', path_effects=shadow, zorder=6)
    fit(ax, fig, 0.42, 6.88, 'AND SYSTEMS', 5.16, color='white', family='Fira Sans', weight='heavy', va='center', path_effects=shadow, zorder=6)
    fit(ax, fig, 0.42, 5.8, 'WORKBOOK', 5.16, color='#5fe0d0', family='Fira Sans', weight='heavy', va='center', path_effects=shadow, zorder=6)
    t = ax.text(0.55, 3.61, 'FOURIER  ·  LAPLACE  ·  Z-TRANSFORM', color='#06222a', fontsize=19, family='Fira Sans', weight='bold', va='center', ha='left', rotation=11.31, rotation_mode='anchor', transform_rotates_text=True, zorder=6)
    ax.text(0.45, 3.0, '600 practice problems with\nstep-by-step solutions', color='white', fontsize=14, family='Libertinus Serif', style='italic', va='center', linespacing=1.3, zorder=6)
    ax.add_patch(Rectangle((0, 0), W, 0.7, color='#031418', zorder=10))
    ax.text(W / 2, 0.35, AUTHOR, ha='center', color='white', fontsize=17, family='Fira Sans', weight='bold', va='center', zorder=11)
    badge(ax, 5.0, 2.95, 0.5, '#f2b134', '#06222a')
    return fig


if __name__ == '__main__':
    for name, f in (('A', cover_a), ('B', cover_b), ('C', cover_c)):
        fig = f()
        fig.savefig(os.path.join(OUT, f'cover-option-{name}.jpg'), dpi=300, pil_kwargs={'quality': 93})
        plt.close(fig)
        print('made', name)
