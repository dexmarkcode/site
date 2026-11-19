"""Front cover (6 x 9 in, 300 dpi) and part-opener illustrations."""
from common import *
from matplotlib.patches import Wedge
import textwrap

GLOW = "#7fd3dc"


def glow_line(ax, xs, ys, c=GLOW, lw=1.5, alpha=1.0, z=3):
    for w, a in ((lw * 6, 0.05), (lw * 3, 0.12), (lw, 1.0)):
        ax.plot(xs, ys, color=c, lw=w, alpha=a * alpha, solid_capstyle="round", zorder=z)


def cover():
    fig = plt.figure(figsize=(6, 9), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 60); ax.set_ylim(0, 90); ax.axis("off")
    grad = np.linspace(0, 1, 512).reshape(-1, 1)
    from matplotlib.colors import LinearSegmentedColormap
    cm = LinearSegmentedColormap.from_list("bg", ["#06111c", "#0d2134", "#12304a"])
    ax.imshow(grad, extent=(0, 60, 0, 90), cmap=cm, aspect="auto", origin="lower", zorder=0)
    # motor cross-section, centre
    cx, cy = 30, 35.5
    for r, a in ((19, 0.10), (17.2, 0.25)):
        ax.add_patch(Circle((cx, cy), r, fill=False, ec=GLOW, lw=0.8, alpha=a, zorder=2))
    n = 48
    for i in range(n):
        ang = 360 * i / n
        ax.add_patch(Wedge((cx, cy), 16.6, ang - 2.1, ang + 2.1, width=3.4, fc="#c9861a" if i % 8 in (0, 1) else "#1d4a66",
                           ec=GLOW, lw=0.3, alpha=0.95, zorder=3))
    ax.add_patch(Circle((cx, cy), 12.8, fill=False, ec=GLOW, lw=1.2, zorder=4))
    ax.add_patch(Circle((cx, cy), 12.4, fc="#0f2a40", ec="none", zorder=3))
    for k in range(8):
        c = np.radians(k * 45 + 22.5)
        for s in (-1, 1):
            p0 = cx + 6.5 * np.cos(c + s * 0.12), cy + 6.5 * np.sin(c + s * 0.12)
            p1 = cx + 11.3 * np.cos(c + s * 0.32), cy + 11.3 * np.sin(c + s * 0.32)
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#e3a43a" if k % 2 else GLOW, lw=4.2, solid_capstyle="butt", zorder=5)
    ax.add_patch(Circle((cx, cy), 3.2, fc="#06111c", ec=GLOW, lw=1.0, zorder=6))
    # three-phase waves sweeping through
    x = np.linspace(-2, 62, 600)
    for k, col in enumerate([GLOW, "#e3a43a", "#ffffff"]):
        y = cy + 9.5 * np.sin(2 * np.pi * x / 30 - k * 2 * np.pi / 3) * (0.6 + 0.4 * np.exp(-((x - 30) / 25) ** 2))
        glow_line(ax, x, y, c=col, lw=0.9, alpha=0.75, z=7)
    # battery cell row at bottom
    for i in range(14):
        ax.add_patch(FancyBboxPatch((4.2 + i * 3.8, 10.2), 2.6, 4.6, boxstyle="round,pad=0,rounding_size=0.35",
                                    fc="#0f2a40", ec=GLOW, lw=0.6, alpha=0.9, zorder=3))
        ax.add_patch(Rectangle((4.2 + i * 3.8 + 0.9, 14.8), 0.8, 0.5, fc=GLOW, alpha=0.8, zorder=3))
    # text
    ax.text(30, 83.2, "FIRST EDITION", ha="center", fontsize=9, color=GLOW, family="Source Sans 3", fontweight="semibold")
    ax.plot([24, 36], [81.6, 81.6], color="#c9861a", lw=1.2)
    ax.text(30, 75.0, "Electric Vehicle", ha="center", fontsize=33, color="white", family="EB Garamond", fontweight="semibold")
    ax.text(30, 67.6, "Engineering", ha="center", fontsize=40, color="white", family="EB Garamond", fontweight="semibold")
    sub = "A Modern Textbook on EV Powertrains,\nBatteries, Motors, Charging,\nand Power Electronics"
    ax.text(30, 62.4, sub, ha="center", va="top", fontsize=10.5, color="#cfe3ea", family="Source Sans 3", linespacing=1.35)
    ax.plot([22, 38], [7.2, 7.2], color="#c9861a", lw=1.2)
    ax.text(30, 3.6, "MARCUS J. THORNTON, Ph.D.", ha="center", fontsize=13, color="white", family="EB Garamond", fontweight="semibold")
    fig.savefig(FIG / "cover.png", dpi=300, facecolor="#06111c")
    fig.savefig(FIG / "cover.jpg", dpi=300, facecolor="#06111c", pil_kwargs={"quality": 92})
    plt.close(fig)
    print("cover")


def part_art(k):
    fig = plt.figure(figsize=(6, 2.6), dpi=250)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 60); ax.set_ylim(0, 26); ax.axis("off")
    a = 0.55
    if k == 1:  # car outline with energy flow
        xs = [6, 10, 18, 24, 38, 46, 52, 54, 54, 6, 6]
        ys = [6, 10, 11, 16, 16, 11, 10, 8, 6, 6, 6]
        glow_line(ax, xs, ys, alpha=a)
        for wx in (14, 46):
            th = np.linspace(0, 2 * np.pi, 80); glow_line(ax, wx + 3 * np.cos(th), 6 + 3 * np.sin(th), alpha=a)
        for i, x0 in enumerate(np.linspace(18, 40, 4)):
            glow_line(ax, [x0, x0 + 4], [8.2, 8.2], c="#e3a43a", lw=2, alpha=0.8)
    elif k == 2:  # cells
        for i in range(12):
            for j in range(2):
                x0, y0 = 4 + i * 4.4, 3 + j * 10
                glow_line(ax, [x0, x0 + 3.2, x0 + 3.2, x0, x0], [y0, y0, y0 + 8, y0 + 8, y0], alpha=a)
                glow_line(ax, [x0 + 1.1, x0 + 2.1], [y0 + 8.6, y0 + 8.6], c="#e3a43a", lw=2, alpha=0.8)
    elif k == 3:  # motor quarter sections
        for cx in (12, 30, 48):
            th = np.linspace(0, 2 * np.pi, 120)
            for r in (9, 6.5, 2):
                glow_line(ax, cx + r * np.cos(th), 13 + r * np.sin(th), alpha=a, lw=1.0)
            for i in range(24):
                t = 2 * np.pi * i / 24
                glow_line(ax, [cx + 6.8 * np.cos(t), cx + 8.6 * np.cos(t)], [13 + 6.8 * np.sin(t), 13 + 8.6 * np.sin(t)], alpha=a, lw=0.8)
    elif k == 4:  # PWM and sine
        x = np.linspace(0, 60, 3000)
        ref = np.sin(2 * np.pi * x / 30)
        car = 2 * np.abs(2 * ((x / 1.6) % 1) - 1) - 1
        pw = np.where(ref > car, 1, -1)
        glow_line(ax, x, 13 + 7 * pw, alpha=0.35, lw=0.7)
        glow_line(ax, x, 13 + 7 * ref, c="#e3a43a", lw=1.6, alpha=0.9)
    else:  # charging plug and grid
        for xx in (8, 20, 32):
            glow_line(ax, [xx, xx - 3, xx + 3, xx], [24, 4, 4, 24], alpha=a, lw=1)
            glow_line(ax, [xx - 4, xx + 4], [18, 18], alpha=a, lw=1)
        x = np.linspace(8, 44, 200)
        glow_line(ax, x, 18 - 2 * np.sin((x - 8) / 12 * np.pi) ** 2, alpha=a, lw=0.8)
        th = np.linspace(0, 2 * np.pi, 100)
        glow_line(ax, 50 + 6 * np.cos(th), 12 + 6 * np.sin(th), alpha=0.8, lw=1.4)
        for px, py in [(48, 14), (52, 14), (50, 10.5), (47.5, 10.5), (52.5, 10.5)]:
            ax.add_patch(Circle((px, py), 0.7, fc="none", ec="#e3a43a", lw=1.2))
    fig.savefig(FIG / f"part{k}.png", dpi=250, transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    cover()
    for k in range(1, 6):
        part_art(k)
    print("parts done")
