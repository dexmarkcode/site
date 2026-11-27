"""Top-down footwork diagrams, equipment drawings, schematic anatomy and charts (black and white)."""
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, FancyArrowPatch, Rectangle, FancyBboxPatch, Arc
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from body import FIG, INK, COUNT, arrow

FOOT = np.array([(0, -1), (2.6, -0.4), (3.6, 2.5), (3.7, 7), (4.3, 11.5), (4.9, 15.5), (4.6, 18.5), (3.4, 20.6),
                 (1.6, 22.0), (-0.6, 22.6), (-2.4, 22.0), (-3.6, 20.2), (-4.0, 17.0), (-3.4, 13.0), (-2.4, 9.5),
                 (-2.5, 5.0), (-2.6, 1.6), (-1.6, -0.6)])


def foot_poly(x, z, yaw, side="l"):
    pts = FOOT.copy()
    if side == "r":
        pts[:, 0] *= -1
    pts[:, 1] -= 6  # ankle roughly at origin
    a = math.radians(-yaw)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return pts @ R.T + np.array([x, z])


def draw_foot(ax, x, z, yaw, side="l", style="solid", label=None, weight=None):
    pts = foot_poly(x, z, yaw, side)
    if style == "ghost":
        ax.add_patch(Polygon(pts, closed=True, fc="none", ec=INK, lw=0.7, ls=(0, (2, 1.5))))
    elif style == "heavy":
        ax.add_patch(Polygon(pts, closed=True, fc="#9e9e9e", ec=INK, lw=0.9))
    elif style == "ball":
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.9))
        c = pts[[8, 9, 10, 4, 5, 6, 7]].mean(axis=0)
        ax.add_patch(Circle(c, 3.2, fc="#9e9e9e", ec=INK, lw=0.5))
    else:
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.9))
    if label:
        ax.text(x, z - 13, label, ha="center", va="top", fontsize=5.6)
    if weight is not None:
        ax.text(x, z + 1, f"{weight}%", ha="center", va="center", fontsize=5.2)


def curve_arrow(ax, p0, p1, p2, lw=0.9, ls="-"):
    verts = [p0, p1, p2]
    path = MPath(verts, [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3])
    ax.add_patch(PathPatch(path, fc="none", ec=INK, lw=lw, ls=ls))
    d = np.array(p2) - np.array(p1)
    d = d / (np.linalg.norm(d) + 1e-9)
    arrow(ax, np.array(p2) - d * 4, p2, lw=lw, ms=6)


def footplate(name, panels, cols=4, pw=1.12, ph=1.35, letters=True, start=0):
    """panels: list of dict(feet=[(x,z,yaw,side,style)], paths=[((x0,z0),(cx,cz),(x1,z1))], cap, lines=[...])"""
    n = len(panels)
    rows = math.ceil(n / cols)
    capg = 0.24
    fig = plt.figure(figsize=(cols * pw, rows * (ph + capg)))
    for i, sp in enumerate(panels):
        r, c = divmod(i, cols)
        x0 = c / cols; y0 = 1 - (r + 1) / rows
        ax = fig.add_axes([x0 + 0.01, y0 + capg / (rows * (ph + capg)), 1 / cols - 0.02, ph / (rows * (ph + capg))])
        xr = sp.get("xr", 42)
        yr = xr * ph / pw
        cz = sp.get("cz", 0)
        ax.set_xlim(-xr, xr); ax.set_ylim(cz - yr, cz + yr); ax.set_aspect("equal"); ax.axis("off")
        if sp.get("grid", True):
            ax.plot([0, 0], [cz - yr * 0.95, cz + yr * 0.95], color=INK, lw=0.4, ls=(0, (1, 2)))
        for ln in sp.get("lines", []):
            ax.plot([ln[0][0], ln[1][0]], [ln[0][1], ln[1][1]], color=INK, lw=0.6, ls=(0, (3, 2)))
        for f in sp.get("feet", []):
            x, z, yaw, side = f[:4]
            style = f[4] if len(f) > 4 else "solid"
            w = f[5] if len(f) > 5 else None
            draw_foot(ax, x, z, yaw, side, style, weight=w)
        for pth in sp.get("paths", []):
            curve_arrow(ax, *pth)
        for t in sp.get("texts", []):
            ax.text(t[0], t[1], t[2], ha="center", va="center", fontsize=t[3] if len(t) > 3 else 5.6)
        if sp.get("fwd", True):
            arrow(ax, (xr * 0.8, cz - yr * 0.6), (xr * 0.8, cz - yr * 0.25), lw=0.6, ms=4)
            ax.text(xr * 0.8, cz - yr * 0.7, "fwd", ha="center", va="top", fontsize=4.8)
        lab = f"({chr(97 + start + i)}) " if letters else ""
        fig.text(x0 + 0.5 / cols, y0 + capg / (rows * (ph + capg)) * 0.5, lab + sp.get("cap", ""),
                 ha="center", va="center", fontsize=6.2)
    fig.savefig(FIG / f"{name}.png", facecolor="white", dpi=300)
    plt.close(fig)
    COUNT[name] = n
    print("footplate", name, n)


# ------------------------------------------------------------------ generic small-multiples canvas
def multi(name, n, cols, draw_fn, pw=1.12, ph=1.3, caps=None, letters=True, xr=50, yr=None):
    """Generic grid where draw_fn(ax, i) draws panel i in a (-xr..xr) box."""
    rows = math.ceil(n / cols)
    capg = 0.24 if caps else 0.06
    fig = plt.figure(figsize=(cols * pw, rows * (ph + capg)))
    yr = yr or xr * ph / pw
    for i in range(n):
        r, c = divmod(i, cols)
        x0 = c / cols; y0 = 1 - (r + 1) / rows
        ax = fig.add_axes([x0 + 0.01, y0 + capg / (rows * (ph + capg)), 1 / cols - 0.02, ph / (rows * (ph + capg))])
        ax.set_xlim(-xr, xr); ax.set_ylim(-yr, yr); ax.set_aspect("equal"); ax.axis("off")
        draw_fn(ax, i)
        if caps:
            lab = f"({chr(97 + i)}) " if letters else ""
            fig.text(x0 + 0.5 / cols, y0 + capg / (rows * (ph + capg)) * 0.5, lab + caps[i],
                     ha="center", va="center", fontsize=6.2)
    fig.savefig(FIG / f"{name}.png", facecolor="white", dpi=300)
    plt.close(fig)
    COUNT[name] = n
    print("multi", name, n)


# ------------------------------------------------------------------ hands (close-up line drawings)
def hand_fist(ax, x=0, y=0, s=1.0, view="side", ang=0):
    """Close-up fist. view: side (thumb side), front (knuckles), top."""
    R = np.array([[math.cos(math.radians(ang)), -math.sin(math.radians(ang))], [math.sin(math.radians(ang)), math.cos(math.radians(ang))]])
    T = lambda pts: (np.array(pts) * s) @ R.T + np.array([x, y])
    if view == "side":
        outline = [(-30, -9), (-12, -12), (4, -13), (14, -12), (20, -8), (22, 0), (20, 9), (12, 13), (-2, 13), (-12, 11), (-30, 9)]
        ax.add_patch(Polygon(T(outline), closed=True, fc="white", ec=INK, lw=0.9))
        for yy in (-6, 0, 6):
            ax.plot(*T([(10, yy + 3), (20, yy + 2)]).T, color=INK, lw=0.6)
        thumb = [(-4, 4), (6, 6), (14, 4), (15, 0), (8, -1), (-2, 0)]
        ax.add_patch(Polygon(T(thumb), closed=True, fc="white", ec=INK, lw=0.8))
        ax.plot(*T([(-30, 9), (-34, 9)]).T, color=INK, lw=0.6)
    elif view == "front":
        for i, xx in enumerate((-12, -4, 4, 12)):
            ax.add_patch(FancyBboxPatch(tuple(T([(xx - 4, -6)])[0]), 8 * s, 14 * s, boxstyle=f"round,pad=0,rounding_size={3*s}",
                                        fc="white", ec=INK, lw=0.8))
        ax.add_patch(FancyBboxPatch(tuple(T([(-14, -14)])[0]), 22 * s, 8 * s, boxstyle=f"round,pad=0,rounding_size={3*s}",
                                    fc="white", ec=INK, lw=0.8))
        for xx in (-8, 8):
            ax.add_patch(Circle(T([(xx * 1.0, 8)])[0], 2.2 * s, fc=INK, ec=INK))


def hand_open(ax, x=0, y=0, s=1.0, ang=0, fingers_bent=0.0):
    R = np.array([[math.cos(math.radians(ang)), -math.sin(math.radians(ang))], [math.sin(math.radians(ang)), math.cos(math.radians(ang))]])
    T = lambda pts: (np.array(pts) * s) @ R.T + np.array([x, y])
    palm = [(-10, -16), (10, -16), (12, 0), (11, 6), (-11, 6), (-12, 0)]
    ax.add_patch(Polygon(T(palm), closed=True, fc="white", ec=INK, lw=0.9))
    for i, (xx, L) in enumerate(((-8, 15), (-2.6, 18), (2.8, 17), (8, 13))):
        bend = fingers_bent
        p0 = np.array([xx, 6]); p1 = p0 + np.array([0, L * 0.55])
        p2 = p1 + np.array([0, L * 0.45 * (1 - bend)]) + np.array([0, 0])
        if bend > 0:
            p2 = p1 + np.array([0, -L * 0.25 * bend + L * 0.45 * (1 - bend)])
        from body import capsule2d
        ax.add_patch(Polygon(T(capsule2d(p0, p1, 2.6, 2.4, 6)), fc="white", ec=INK, lw=0.7))
        ax.add_patch(Polygon(T(capsule2d(p1, p2, 2.4, 2.2, 6)), fc="white", ec=INK, lw=0.7))
    from body import capsule2d
    ax.add_patch(Polygon(T(capsule2d(np.array([-10, -8]), np.array([-19, 2]), 3.2, 2.6, 6)), fc="white", ec=INK, lw=0.8))


# ------------------------------------------------------------------ equipment (stand-alone)
def eq_chiishi(ax, s=1.0):
    ax.add_patch(Rectangle((-1.8, -30), 3.6, 52, fc="white", ec=INK, lw=0.9))
    ax.add_patch(FancyBboxPatch((-11, -42), 22, 14, boxstyle="round,pad=0,rounding_size=3", fc="#bdbdbd", ec=INK, lw=0.9))
    for y in (-37, -33):
        ax.plot([-9, 9], [y, y], color=INK, lw=0.3)


def eq_nigirigame(ax):
    body = [(-6, 22), (-7, 18), (-15, 8), (-16, -6), (-12, -20), (12, -20), (16, -6), (15, 8), (7, 18), (6, 22)]
    ax.add_patch(Polygon(body, closed=True, fc="white", ec=INK, lw=0.9))
    ax.add_patch(Ellipse((0, 22), 13, 3.4, fc="white", ec=INK, lw=0.9))
    ax.plot([-15.5, 15.5], [2, 2], color=INK, lw=0.4)
    for i in range(-14, 15, 3):
        ax.plot([i, i + 1.5], [-2, -14], color=INK, lw=0.3)


def eq_makiwara(ax):
    ax.add_patch(Polygon([(-5, -40), (5, -40), (3, 34), (-3, 34)], closed=True, fc="white", ec=INK, lw=0.9))
    ax.add_patch(Rectangle((-4, 20), 8, 13, fc="#9a9a9a", ec=INK, lw=0.9))
    for y in range(21, 33, 2):
        ax.plot([-4, 4], [y, y], color="white", lw=0.4)
    ax.plot([-30, 30], [-40, -40], color=INK, lw=0.8)
    for x in range(-28, 30, 5):
        ax.plot([x, x - 3], [-40, -44], color=INK, lw=0.4)


def eq_ishisashi(ax):
    ax.add_patch(Rectangle((-4, -12), 8, 18, fc="white", ec=INK, lw=0.9))
    ax.add_patch(Polygon([(-14, -12), (14, -12), (12, -26), (-12, -26)], closed=True, fc="#bdbdbd", ec=INK, lw=0.9))
    ax.add_patch(Rectangle((-5, 6), 10, 6, fc="white", ec=INK, lw=0.9))


def eq_tan(ax):
    ax.add_patch(Rectangle((-36, -1.5), 72, 3, fc="white", ec=INK, lw=0.9))
    for x in (-34, 28):
        ax.add_patch(FancyBboxPatch((x, -10), 6, 20, boxstyle="round,pad=0,rounding_size=2", fc="#bdbdbd", ec=INK, lw=0.9))


def eq_kongoken(ax):
    ax.add_patch(Ellipse((0, 0), 46, 66, fc="none", ec=INK, lw=2.6))
    ax.add_patch(Ellipse((0, 0), 46, 66, fc="none", ec="white", lw=1.0))


def eq_tetsugeta(ax):
    ax.add_patch(Polygon([(-24, -4), (24, -4), (22, 4), (-22, 4)], closed=True, fc="#8a8a8a", ec=INK, lw=0.9))
    ax.add_patch(Rectangle((-16, -14), 8, 10, fc="#8a8a8a", ec=INK, lw=0.9))
    ax.add_patch(Rectangle((8, -14), 8, 10, fc="#8a8a8a", ec=INK, lw=0.9))
    ax.plot([-6, 0, 6], [4, 9, 4], color=INK, lw=1.4)


def eq_kame_sack(ax):
    ax.add_patch(FancyBboxPatch((-12, -30), 24, 56, boxstyle="round,pad=0,rounding_size=8", fc="white", ec=INK, lw=0.9))
    ax.plot([0, 0], [26, 40], color=INK, lw=0.9)
    for y in range(-24, 22, 6):
        ax.plot([-10, 10], [y, y + 2], color=INK, lw=0.3)


def eq_jari_bako(ax):
    ax.add_patch(Polygon([(-20, -10), (20, -10), (24, 8), (-24, 8)], closed=True, fc="white", ec=INK, lw=0.9))
    for i in range(40):
        rng = np.random.default_rng(i)
        ax.add_patch(Circle((rng.uniform(-20, 20), rng.uniform(3, 9)), 1.0, fc=INK, ec=INK))


def eq_sashi(ax):
    eq_ishisashi(ax)


EQUIP = {"chi-ishi": eq_chiishi, "nigiri-game": eq_nigirigame, "makiwara": eq_makiwara, "ishi-sashi": eq_ishisashi,
         "tan": eq_tan, "kongoken": eq_kongoken, "tetsu-geta": eq_tetsugeta, "sand bag": eq_kame_sack, "jari-bako": eq_jari_bako}


# ------------------------------------------------------------------ charts
def chart(name, w=4.5, h=2.0):
    fig, ax = plt.subplots(figsize=(w, h))
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(labelsize=6.5, color=INK)
    return fig, ax


def save_chart(fig, name, n=1):
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", pad_inches=0.04, facecolor="white", dpi=300)
    plt.close(fig)
    COUNT[name] = n
    print("chart", name, n)


# ------------------------------------------------------------------ schematic torso (breathing / internal)
def torso_schematic(ax, mode="neutral", label=True, dian=True, arrows=None):
    """Front-on schematic torso outline with diaphragm, pelvic floor and dantien."""
    outline = [(-16, -38), (-20, -30), (-18, -10), (-16, 5), (-19, 20), (-24, 30), (-26, 36), (-10, 40), (-6, 46), (6, 46), (10, 40),
               (26, 36), (24, 30), (19, 20), (16, 5), (18, -10), (20, -30), (16, -38)]
    ax.add_patch(Polygon(outline, closed=True, fc="white", ec=INK, lw=0.9))
    ax.add_patch(Ellipse((0, 54), 14, 17, fc="white", ec=INK, lw=0.9))
    dy = {"neutral": 0, "in": -5, "out": 4, "reverse": 3}[mode]
    th = np.linspace(math.pi, 0, 40)
    ax.plot(15 * np.cos(th), 6 + dy + 7 * np.sin(th) * (0.7 if mode == "in" else 1), color=INK, lw=1.2)
    pf = {"neutral": 0, "in": -2, "out": 2, "reverse": 3}[mode]
    ax.plot(np.linspace(-13, 13, 20), -32 + pf - 3 * np.sin(np.linspace(0, math.pi, 20)), color=INK, lw=1.0, ls=(0, (2, 1)))
    belly = {"neutral": 0, "in": 3, "out": -2, "reverse": -2}[mode]
    ax.plot([-16 - belly * 0.3, -17 - belly, -16 - belly * 0.3], [5, -12, -30], color=INK, lw=0.5, ls=(0, (1, 1.4)))
    ax.plot([16 + belly * 0.3, 17 + belly, 16 + belly * 0.3], [5, -12, -30], color=INK, lw=0.5, ls=(0, (1, 1.4)))
    if dian:
        ax.add_patch(Circle((0, -20), 3.6, fc="white", ec=INK, lw=0.8))
        ax.add_patch(Circle((0, -20), 1.2, fc=INK))
    for a in arrows or []:
        arrow(ax, a[0], a[1], lw=0.9, ms=5)
