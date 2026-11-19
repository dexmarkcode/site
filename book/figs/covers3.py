"""Three alternative premium front covers, 6 x 9 in at 300 dpi."""
from common import *
from matplotlib.patches import Wedge, Ellipse
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe

OUT = ROOT / "output" / "covers"
OUT.mkdir(parents=True, exist_ok=True)
TITLE1, TITLE2 = "Electric Vehicle", "Engineering"
SUB = "A Modern Textbook on EV Powertrains, Batteries,\nMotors, Charging, and Power Electronics"
AUTHOR = "MARCUS J. THORNTON, Ph.D."


def spaced(s, n=1):
    return (" " * n).join(s)


def new():
    fig = plt.figure(figsize=(6, 9), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 60); ax.set_ylim(0, 90); ax.axis("off")
    return fig, ax


def gradient(ax, cols, extent=(0, 60, 0, 90), horiz=False):
    g = np.linspace(0, 1, 600)
    g = g.reshape(1, -1) if horiz else g.reshape(-1, 1)
    ax.imshow(g, extent=extent, cmap=LinearSegmentedColormap.from_list("g", cols), aspect="auto", origin="lower", zorder=0)


def finish(fig, name):
    fig.savefig(OUT / f"{name}.jpg", dpi=300, pil_kwargs={"quality": 95})
    fig.savefig(OUT / f"{name}.png", dpi=300)
    plt.close(fig); print("saved", name)


# ---------------------------------------------------------------- Cover A: Ivory Prestige
def cover_a():
    fig, ax = new()
    ax.add_patch(Rectangle((0, 0), 60, 90, fc="#f4efe6", zorder=0))
    ink, cop, nav = "#14181c", "#b5702a", "#14304a"
    # large precise line-art motor cross-section, offset and cropped off the right edge
    cx, cy, f = 40, 20, 0.74
    for r, lw in ((26, 0.6), (24.2, 1.1), (17.5, 1.1), (16.6, 0.5), (4.2, 1.0)):
        ax.add_patch(Circle((cx, cy), r * f, fill=False, ec=nav, lw=lw, zorder=2))
    for i in range(48):
        a = 2 * np.pi * i / 48
        x1, y1 = cx + 17.8 * f * np.cos(a), cy + 17.8 * f * np.sin(a)
        x2, y2 = cx + 23.6 * f * np.cos(a), cy + 23.6 * f * np.sin(a)
        ax.plot([x1, x2], [y1, y2], color=cop if i % 8 in (0, 1) else nav, lw=2.2 if i % 8 in (0, 1) else 0.8, zorder=2)
    for k in range(8):
        c = 2 * np.pi * k / 8 + np.pi / 8
        for s in (-1, 1):
            p0 = cx + 7.5 * f * np.cos(c + s * 0.13), cy + 7.5 * f * np.sin(c + s * 0.13)
            p1 = cx + 15.2 * f * np.cos(c + s * 0.33), cy + 15.2 * f * np.sin(c + s * 0.33)
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=cop if k % 2 else nav, lw=3.4, solid_capstyle="butt", zorder=3)
    # thin construction lines like an engineering plate
    for ang in (0, 45, 90, 135):
        a = np.radians(ang)
        ax.plot([cx - 28 * f * np.cos(a), cx + 28 * f * np.cos(a)], [cy - 28 * f * np.sin(a), cy + 28 * f * np.sin(a)], color=nav, lw=0.3, alpha=0.5, zorder=1, ls=(0, (6, 4)))
    ax.text(5, 6.0, "FIG. 1  —  TRACTION MOTOR, SECTION A–A", fontsize=5.5, color=nav, family="Source Sans 3", alpha=0.8)
    # typography block, upper left
    ax.text(5, 84.5, spaced("FIRST EDITION", 2), fontsize=8.5, color=cop, family="Source Sans 3", fontweight="bold")
    ax.plot([5, 55], [82.8, 82.8], color=ink, lw=0.8)
    ax.text(4.6, 72.0, "Electric", fontsize=52, color=ink, family="EB Garamond", fontweight="semibold")
    ax.text(4.6, 61.8, "Vehicle", fontsize=52, color=ink, family="EB Garamond", fontweight="semibold")
    ax.text(4.6, 51.6, "Engineering", fontsize=52, color=ink, family="EB Garamond", style="italic")
    ax.text(5, 48.6, SUB,
            fontsize=10.5, color="#3a4249", family="Source Sans 3", va="top", linespacing=1.4)
    ax.plot([5, 13], [41.0, 41.0], color=cop, lw=2)
    # author band
    ax.add_patch(Rectangle((0, 0), 60, 4.2, fc=ink, zorder=4))
    ax.text(5, 1.7, spaced(AUTHOR.upper().replace("PH.D.", "PH.D."), 1), fontsize=11, color="#f4efe6", family="EB Garamond",
            fontweight="semibold", va="center", zorder=5)
    finish(fig, "Cover-A_Ivory-Prestige")


# ---------------------------------------------------------------- Cover B: Voltage (bold dark)
def cover_b():
    fig, ax = new()
    gradient(ax, ["#050607", "#0d1116", "#141a21"])
    orange, ice = "#ff7a1a", "#e9eef2"
    # dramatic three-phase light trails sweeping across the lower half
    x = np.linspace(-5, 65, 1400)
    for k, (col, amp) in enumerate([(orange, 11), ("#ffb347", 9.5), ("#4fd1ff", 10.5)]):
        y = 26 + amp * np.sin(2 * np.pi * x / 34 - k * 2 * np.pi / 3) * np.exp(-((x - 30) / 34) ** 2) + 0.12 * x
        for w, a in ((22, 0.03), (11, 0.06), (5, 0.14), (1.6, 1.0)):
            ax.plot(x, y, color=col, lw=w, alpha=a, solid_capstyle="round", zorder=3)
    # glowing core
    for r, a in ((9, 0.05), (6, 0.08), (3.5, 0.14)):
        ax.add_patch(Circle((30, 29.5), r, fc=orange, ec="none", alpha=a, zorder=2))
    # stacked heavy sans title
    for i, (w, size) in enumerate([("ELECTRIC", 50), ("VEHICLE", 50), ("ENGINEERING", 37)]):
        y = 76 - i * 9.4
        t = ax.text(30, y, spaced(w, 1), ha="center", va="center", fontsize=size, color=ice, family="Source Sans 3", fontweight="bold")
    ax.add_patch(Rectangle((22, 52.5), 16, 0.55, fc=orange, ec="none"))
    ax.text(30, 49.4, SUB, ha="center", va="top", fontsize=10.2, color="#aeb8c1", family="Source Sans 3", linespacing=1.45)
    ax.text(30, 86.6, spaced("THE COMPLETE ENGINEERING GUIDE", 2), ha="center", fontsize=7.8, color=orange, family="Source Sans 3", fontweight="semibold")
    ax.text(30, 6.2, AUTHOR, ha="center", fontsize=15, color=ice, family="EB Garamond", fontweight="semibold")
    ax.text(30, 3.0, spaced("FIRST EDITION", 2), ha="center", fontsize=6.8, color="#7d8790", family="Source Sans 3")
    finish(fig, "Cover-B_Voltage")


# ---------------------------------------------------------------- Cover C: Blueprint
def cover_c():
    fig, ax = new()
    gradient(ax, ["#0a2340", "#0f3358", "#123d68"])
    line_c, gold = "#d6e6f5", "#e0b25a"
    # blueprint grid
    for gx in np.arange(0, 61, 2.5):
        ax.plot([gx, gx], [0, 90], color="white", lw=0.35 if gx % 10 else 0.6, alpha=0.08 if gx % 10 else 0.14, zorder=1)
    for gy in np.arange(0, 91, 2.5):
        ax.plot([0, 60], [gy, gy], color="white", lw=0.35 if gy % 10 else 0.6, alpha=0.08 if gy % 10 else 0.14, zorder=1)
    # car side profile (technical drawing) with powertrain cutaway
    ox, oy, s = 3, 22, 1.0
    body_x = [2, 4, 9, 17, 23, 32, 41, 48, 53, 54, 54, 2, 2]
    body_y = [4, 7.5, 9, 10, 15, 16.2, 15.8, 11.5, 10.5, 8.5, 4, 4, 4]
    ax.plot([ox + s * x for x in body_x], [oy + s * y for y in body_y], color=line_c, lw=1.3, zorder=4)
    ax.plot([ox + 21.5, ox + 25, ox + 39, ox + 45.5], [oy + 10.2, oy + 14.6, oy + 14.6, oy + 10.6], color=line_c, lw=0.8, zorder=4)
    ax.plot([ox + 33, ox + 33], [oy + 10.2, oy + 15.6], color=line_c, lw=0.8, zorder=4)
    for wx in (12.5, 44):
        for r, lw in ((4.0, 1.3), (2.6, 0.7), (0.7, 0.8)):
            ax.add_patch(Circle((ox + wx, oy + 4), r, fill=False, ec=line_c, lw=lw, zorder=5))
        ax.add_patch(Circle((ox + wx, oy + 4), 4.0, fc="#0f3358", ec="none", zorder=4))
    # battery pack under floor
    ax.add_patch(Rectangle((ox + 17.5, oy + 3.2), 21, 2.4, fc=gold, alpha=0.18, ec=gold, lw=0.9, zorder=6))
    for i in range(12):
        ax.plot([ox + 18.5 + i * 1.7] * 2, [oy + 3.4, oy + 5.4], color=gold, lw=0.5, zorder=6)
    # rear drive unit
    ax.add_patch(Rectangle((ox + 40.5, oy + 5.0), 6, 3.8, fill=False, ec=gold, lw=0.9, zorder=6))
    ax.add_patch(Circle((ox + 42.6, oy + 6.9), 1.4, fill=False, ec=gold, lw=0.8, zorder=6))
    ax.plot([ox + 38.5, ox + 40.5], [oy + 4.4, oy + 6.2], color=gold, lw=1.0, zorder=6, ls=(0, (2, 1)))
    # dimension lines and callouts
    ax.annotate("", xy=(ox + 12.5, oy - 3.5), xytext=(ox + 44, oy - 3.5), arrowprops=dict(arrowstyle="<->", color=line_c, lw=0.6))
    ax.text(ox + 28.2, oy - 5.6, "WHEELBASE 2 900", fontsize=5.2, color=line_c, ha="center", family="Source Sans 3")
    for (tx, ty, px, py, lab) in [(10, 40.5, ox + 25, oy + 4.6, "TRACTION BATTERY"), (46, 39.5, ox + 43.5, oy + 8.8, "E-AXLE"),
                                  (6, 15.5, ox + 9, oy + 9, "CHARGE INLET")]:
        ax.plot([tx + 3, px], [ty - 0.6 if ty > 30 else ty + 1.3, py], color=line_c, lw=0.4, alpha=0.8, zorder=6)
        ax.text(tx, ty, lab, fontsize=5.2, color=gold, family="Source Sans 3", fontweight="semibold", zorder=6)
    # title block, framed like a drawing sheet
    ax.add_patch(Rectangle((3, 47), 54, 39.5, fill=False, ec=line_c, lw=0.8, zorder=3))
    ax.add_patch(Rectangle((4, 48), 52, 37.5, fill=False, ec=line_c, lw=0.35, alpha=0.6, zorder=3))
    ax.text(30, 81.2, spaced("THE COMPLETE ENGINEERING GUIDE", 2), ha="center", fontsize=8.3, color=gold, family="Source Sans 3", fontweight="semibold")
    ax.text(30, 72.5, TITLE1, ha="center", fontsize=40, color="white", family="EB Garamond", fontweight="semibold")
    ax.text(30, 63.0, TITLE2, ha="center", fontsize=46, color="white", family="EB Garamond", fontweight="semibold")
    ax.plot([24, 36], [60.0, 60.0], color=gold, lw=1.4)
    ax.text(30, 57.4, SUB, ha="center", va="top",
            fontsize=9.6, color="#c9dcee", family="Source Sans 3", linespacing=1.45)
    # bottom title strip, like a drawing's title block
    ax.add_patch(Rectangle((3, 3), 54, 8, fill=False, ec=line_c, lw=0.8))
    ax.plot([42, 42], [3, 11], color=line_c, lw=0.5)
    ax.text(5, 7, AUTHOR, fontsize=14, color="white", family="EB Garamond", fontweight="semibold", va="center")
    ax.text(49.5, 8.4, "EDITION", fontsize=4.8, color=line_c, ha="center", family="Source Sans 3")
    ax.text(49.5, 5.6, "FIRST", fontsize=8.5, color=gold, ha="center", family="Source Sans 3", fontweight="bold")
    finish(fig, "Cover-C_Blueprint")


if __name__ == "__main__":
    cover_a(); cover_b(); cover_c()
