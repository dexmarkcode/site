"""Cover C, version 2: large capitalised title, large car drawing, premium finish."""
from covers3 import *
import matplotlib.patheffects as pe

GOLD, GOLD2, LINE = "#e3b45c", "#f6d68f", "#dcebf8"


def fit_text(fig, ax, x, y, s, width, **kw):
    """Place centred text and scale its font size so it spans exactly `width` data units."""
    t = ax.text(x, y, s, ha="center", va="baseline", fontsize=40, **kw)
    fig.canvas.draw()
    bb = t.get_window_extent().transformed(ax.transData.inverted())
    t.set_fontsize(40 * width / (bb.x1 - bb.x0))
    return t


def glow(ax, xs, ys, c=LINE, lw=1.6, z=5):
    for w, a in ((lw * 5, 0.06), (lw * 2.5, 0.14), (lw, 1.0)):
        ax.plot(xs, ys, color=c, lw=w, alpha=a, solid_capstyle="round", solid_joinstyle="round", zorder=z)


def cover_c2():
    fig, ax = new()
    gradient(ax, ["#06182e", "#0c2b4d", "#103a66"])
    # soft radial light behind the car
    for r, a in ((34, 0.05), (24, 0.06), (15, 0.07)):
        ax.add_patch(Ellipse((30, 27), r * 2, r * 1.1, fc="#4f8fd0", ec="none", alpha=a, zorder=1))
    # blueprint grid
    for gx in np.arange(0, 60.1, 2.5):
        ax.plot([gx, gx], [0, 90], color="white", lw=0.3 if gx % 10 else 0.55, alpha=0.06 if gx % 10 else 0.11, zorder=1)
    for gy in np.arange(0, 90.1, 2.5):
        ax.plot([0, 60], [gy, gy], color="white", lw=0.3 if gy % 10 else 0.55, alpha=0.06 if gy % 10 else 0.11, zorder=1)
    # premium double frame
    ax.add_patch(Rectangle((1.6, 1.6), 56.8, 86.8, fill=False, ec=GOLD, lw=1.1, zorder=8))
    ax.add_patch(Rectangle((2.4, 2.4), 55.2, 85.2, fill=False, ec=GOLD, lw=0.4, alpha=0.7, zorder=8))

    # tagline
    ax.text(30, 83.6, spaced("THE COMPLETE ENGINEERING GUIDE", 2), ha="center", fontsize=9.5, color=GOLD,
            family="Source Sans 3", fontweight="bold", zorder=9)
    ax.plot([12, 48], [82.2, 82.2], color=GOLD, lw=0.6, alpha=0.8)

    # BIG capitalised title, each line fitted to the same width (justified block)
    shadow = [pe.withSimplePatchShadow(offset=(1.6, -1.6), shadow_rgbFace="#020a14", alpha=0.6)]
    W = 50
    for txt, y in (("ELECTRIC", 70.8), ("VEHICLE", 60.2), ("ENGINEERING", 53.6)):
        t = fit_text(fig, ax, 30, y, txt, W, color="white", family="EB Garamond", fontweight="bold", zorder=9)
        t.set_path_effects(shadow)
    # gold rule with diamond
    ax.plot([10, 27.6], [51.0, 51.0], color=GOLD, lw=1.4); ax.plot([32.4, 50], [51.0, 51.0], color=GOLD, lw=1.4)
    ax.add_patch(Polygon([[30, 52.1], [31.1, 51.0], [30, 49.9], [28.9, 51.0]], fc=GOLD2, ec="none", zorder=9))
    # subtitle, larger and bold
    ax.text(30, 48.3, "A Modern Textbook on EV Powertrains, Batteries,\nMotors, Charging, and Power Electronics", ha="center", va="top",
            fontsize=12.2, color="#e4eef8", family="Source Sans 3", fontweight="semibold", linespacing=1.4, zorder=9)

    # LARGE car blueprint
    s, ox, oy = 1.06, 0.9, 16.2
    X = lambda v: ox + s * v
    Y = lambda v: oy + s * v
    bx = [2, 4, 9, 17, 23, 32, 41, 48, 53, 54, 54, 2, 2]
    by = [4, 7.5, 9, 10, 15, 16.2, 15.8, 11.5, 10.5, 8.5, 4, 4, 4]
    glow(ax, [X(v) for v in bx], [Y(v) for v in by], lw=1.9)
    glow(ax, [X(21.5), X(25), X(39), X(45.5)], [Y(10.2), Y(14.6), Y(14.6), Y(10.6)], lw=1.1)
    glow(ax, [X(33), X(33)], [Y(10.2), Y(15.6)], lw=1.0)
    glow(ax, [X(46.5), X(50.5)], [Y(9.8), Y(9.8)], lw=0.9)  # rear light line
    glow(ax, [X(4.2), X(9)], [Y(7.2), Y(7.6)], lw=0.9)  # front light line
    for wx in (12.5, 44):
        ax.add_patch(Circle((X(wx), Y(4)), 4.3 * s, fc="#0b2746", ec="none", zorder=5))
        for r, lw in ((4.3, 1.9), (2.9, 0.9), (0.8, 1.0)):
            ax.add_patch(Circle((X(wx), Y(4)), r * s, fill=False, ec=LINE, lw=lw, zorder=6))
        for k in range(5):
            a = 2 * np.pi * k / 5
            ax.plot([X(wx) + 0.9 * np.cos(a), X(wx) + 2.8 * s * np.cos(a)], [Y(4) + 0.9 * np.sin(a), Y(4) + 2.8 * s * np.sin(a)], color=LINE, lw=0.6, zorder=6)
    # battery pack (gold) and e-axle
    ax.add_patch(Rectangle((X(17.5), Y(3.1)), 21.5 * s, 2.6 * s, fc=GOLD, alpha=0.22, ec=GOLD, lw=1.2, zorder=7))
    for i in range(13):
        ax.plot([X(18.4 + i * 1.6)] * 2, [Y(3.4), Y(5.4)], color=GOLD2, lw=0.6, zorder=7)
    ax.add_patch(Rectangle((X(40.3), Y(5.0)), 6.2 * s, 4 * s, fc=GOLD, alpha=0.15, ec=GOLD, lw=1.2, zorder=7))
    ax.add_patch(Circle((X(42.5), Y(7.0)), 1.5 * s, fill=False, ec=GOLD2, lw=1.0, zorder=7))
    ax.plot([X(39), X(40.3)], [Y(4.4), Y(6.0)], color=GOLD2, lw=1.1, ls=(0, (2, 1)), zorder=7)
    # callouts, larger and bold
    def callout(tx, ty, px, py, lab, ha="left"):
        ax.plot([px, tx], [py, ty], color=LINE, lw=0.6, alpha=0.9, zorder=7)
        ax.add_patch(Circle((px, py), 0.35, fc=GOLD2, ec="none", zorder=8))
        ax.text(tx + (0.6 if ha == "left" else -0.6), ty, lab, fontsize=7.4, color=GOLD2, family="Source Sans 3",
                fontweight="bold", ha=ha, va="center", zorder=8)
    callout(5, 38.5, X(26), Y(4.4), "TRACTION BATTERY")
    callout(55, 38.5, X(43.4), Y(8.6), "E-AXLE", ha="right")
    callout(5, 34.5, X(8), Y(8.4), "CHARGE INLET")
    ax.annotate("", xy=(X(12.5), Y(-2.6)), xytext=(X(44), Y(-2.6)), arrowprops=dict(arrowstyle="<->", color=LINE, lw=0.7))
    ax.text(X(28.2), Y(-4.3), "WHEELBASE 2 900 mm", fontsize=6.4, color=LINE, ha="center", family="Source Sans 3", fontweight="semibold")

    # author strip, big and bold
    ax.add_patch(Rectangle((2.4, 2.4), 55.2, 6.6, fc="#04101f", ec="none", alpha=0.75, zorder=8))
    ax.plot([2.4, 57.6], [9.0, 9.0], color=GOLD, lw=0.9, zorder=9)
    fit_text(fig, ax, 30, 4.25, spaced("MARCUS J. THORNTON, PH.D.", 1), 44, color="white", family="EB Garamond", fontweight="bold", zorder=9)
    finish(fig, "Cover-C2_Blueprint-Premium")


if __name__ == "__main__":
    cover_c2()
