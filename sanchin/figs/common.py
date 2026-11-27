"""Shared drawing toolkit for every illustration in the Sanchin book.

Pure black-and-white line art. A simple 3D mannequin (height = 100 units) is posed in
3D and projected to any view angle, so the frame-by-frame diagrams stay consistent.

Coordinates: x = figure's left (+) / right (-), y = forward (the way the figure faces),
z = up. View angle th: 0 = front view (figure faces the reader), -90 = side view from the
figure's right (figure faces the right of the page), 180 = back view.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon, Circle, FancyArrowPatch, Rectangle, Ellipse, Arc, PathPatch
from matplotlib.path import Path as MPath
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
for f in (ROOT / "fonts").glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))

K = "#000000"; G1 = "#d9d9d9"; G2 = "#9a9a9a"; G3 = "#555555"; WH = "#ffffff"
plt.rcParams.update({
    "font.family": "Source Sans 3", "font.size": 8, "savefig.dpi": 300,
    "axes.edgecolor": K, "axes.linewidth": 0.7, "xtick.color": K, "ytick.color": K,
    "axes.labelcolor": K, "text.color": K, "lines.color": K,
})
SERIF = "EB Garamond"
W = 4.5  # text block width, inches


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("saved", name)


def canvas(w=W, h=2.6, xlim=(0, 100), ylim=None):
    fig, ax = plt.subplots(figsize=(w, h))
    if ylim is None:
        ylim = (0, (xlim[1] - xlim[0]) * h / w)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


# ------------------------------------------------------------------ geometry
def v(*a):
    return np.array(a, dtype=float)


def unit(a):
    n = np.linalg.norm(a)
    return a / n if n else a


def hull(pts):
    pts = sorted(map(tuple, pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def capsule(p, q, w, n=10):
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    L = np.hypot(*d)
    if L < 1e-6:
        d = np.array([0, 1.0]); L = 1e-6
    a = math.atan2(d[1], d[0])
    pts = []
    for t in np.linspace(a + math.pi/2, a + 3*math.pi/2, n):
        pts.append(p + w/2*np.array([math.cos(t), math.sin(t)]))
    for t in np.linspace(a - math.pi/2, a + math.pi/2, n):
        pts.append(q + w/2*np.array([math.cos(t), math.sin(t)]))
    return np.array(pts)


def taper(p, q, w1, w2, n=8):
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    a = math.atan2(d[1], d[0])
    pts = []
    for t in np.linspace(a + math.pi/2, a + 3*math.pi/2, n):
        pts.append(p + w1/2*np.array([math.cos(t), math.sin(t)]))
    for t in np.linspace(a - math.pi/2, a + math.pi/2, n):
        pts.append(q + w2/2*np.array([math.cos(t), math.sin(t)]))
    return np.array(pts)


# ------------------------------------------------------------------ sole outline (local: heel at 0, toe at +1 along y)
def _sole_local(n=40):
    """Outline of a left sole, x>0 = outer (little-toe) side, y 0 heel -> 1 tip of sole (ball end ~0.78)."""
    ys = np.linspace(0, 1, n)
    def outer(y):
        return 0.10 + 0.10 * math.sin(min(1, y / 0.8) * math.pi / 2) ** 0.7 + (0.02 if y > 0.55 else 0) * min(1, (y-0.55)/0.2)
    def inner(y):
        base = 0.10 + 0.11 * math.sin(min(1, y / 0.82) * math.pi / 2) ** 1.2
        arch = 0.06 * math.exp(-((y - 0.45) / 0.13) ** 2)
        return base - arch
    pts = []
    # heel cap
    xo, xi = outer(0.08), inner(0.08)
    cx, rx = (xo - xi) / 2, (xo + xi) / 2
    for t in np.linspace(math.pi, 2 * math.pi, 14):
        pts.append((cx + rx * math.cos(t), 0.08 + 0.08 * math.sin(t)))
    for y in np.linspace(0.08, 0.86, n):
        pts.append((outer(y), y))
    # ball cap (rounded front, tilted: big toe side longer)
    for t in np.linspace(0, math.pi, 16):
        x = 0.21 * math.cos(t) + 0.0
        y = 0.86 + (0.10 + 0.04 * (1 - math.cos(t)) / 2) * math.sin(t)
        pts.append((x * (outer(0.86) / 0.21 if x > 0 else inner(0.86) / 0.21), y))
    for y in np.linspace(0.86, 0.08, n):
        pts.append((-inner(y), y))
    return np.array(pts)


_SOLE = _sole_local()
_TOES = [(-0.13, 1.07, 0.062, 0.075), (-0.025, 1.065, 0.035, 0.045), (0.05, 1.045, 0.032, 0.04),
         (0.115, 1.015, 0.029, 0.036), (0.17, 0.975, 0.026, 0.032)]


def sole_points(heel_xy, direction, length=15.0, left=True):
    d = unit(np.asarray(direction, float)[:2])
    perp = np.array([d[1], -d[0]])  # to the right of direction
    sgn = -1 if left else 1          # left foot: outer side is to the left of travel
    pts = [np.asarray(heel_xy, float) + d * sy * length * 0.86 + perp * sx * sgn * length for sx, sy in _SOLE]
    return np.array(pts)


def toe_points(heel_xy, direction, length=15.0, left=True):
    d = unit(np.asarray(direction, float)[:2])
    perp = np.array([d[1], -d[0]])
    sgn = -1 if left else 1
    return [(np.asarray(heel_xy, float) + d * ty * length * 0.86 + perp * tx * sgn * length, rx * length, ry * length, d)
            for tx, ty, rx, ry in _TOES]


# ------------------------------------------------------------------ poses
SH_Z, HIP_Z = 81.0, 51.0


def arm(kind, s):
    """Return (elbow, wrist, hand_end, hand_type) for arm on side s (+1 left, -1 right)."""
    A = {
        "uke":      ((14, 8, 64), (12, 14, 78), (11.5, 15.5, 82), "fist"),
        "uke_low":  ((14, 9, 63), (12, 16, 74), (11.5, 17.5, 77), "fist"),
        "tsuki":    ((6, 18, 73), (1.5, 33, 71), (1, 37, 71), "fist"),
        "tsuki_mid": ((11, 9, 66), (7, 21, 67), (6, 25, 67.5), "fist"),
        "hikite":   ((13, -12, 63), (11, 0, 57), (10.5, 3, 57), "fist"),
        "hikite_open": ((13, -12, 63), (11, 0, 57), (10, 6, 57), "open"),
        "side":     ((13, 0, 63), (14, 1, 47), (14, 1, 41), "open"),
        "side_fist": ((13, 0, 63), (14, 1, 47), (14, 1, 44), "fist"),
        "yoi":      ((13, 5, 63), (-1, 12, 50), (-5, 13, 46.5), "open"),
        "cross":    ((10, 13, 64), (-3, 20, 73), (-4.5, 21, 76), "fist"),
        "cross_low": ((12, 10, 62), (-2, 17, 56), (-4, 18, 54), "fist"),
        "nukite":   ((8, 18, 72), (5, 33, 72), (5, 41, 72), "open"),
        "nukite_chamber": ((13, -11, 63), (10, 1, 59), (9, 7, 59), "open"),
        "tora_up":  ((10, 15, 68), (5, 26, 76), (5, 27, 84), "open"),
        "tora_down": ((10, 14, 61), (5, 26, 62), (5, 27, 55), "open"),
        "circle_a": ((12, 10, 65), (2, 20, 74), (-1, 22, 79), "open"),
        "circle_b": ((12, 10, 63), (4, 21, 60), (1, 23, 57), "open"),
        "palm_chest": ((12, 4, 64), (5, 10, 72), (2, 12, 76), "open"),
    }
    e, w, h, t = A[kind]
    f = lambda p: v(s * p[0], p[1], p[2])
    return f(e), f(w), f(h), t


def legs(kind, lead="R"):
    """Return dict with knees, ankles, foot dirs and hip height."""
    s = 1 if lead == "L" else -1   # lead side sign
    if kind == "sanchin":
        lw, rw = 10, 10
        lead_ank = v(s * lw, 8, 4); rear_ank = v(-s * rw, -8, 4)
        lead_kn = v(s * 7, 12, 27); rear_kn = v(-s * 7, -3, 27)
        lead_dir = v(-s * math.sin(math.radians(22)), math.cos(math.radians(22)), 0)
        rear_dir = v(-s * math.sin(math.radians(10)), math.cos(math.radians(10)), 0)
        hz = 50
    elif kind == "sanchin_wide":   # fault: too long and wide
        lead_ank = v(s * 15, 16, 4); rear_ank = v(-s * 14, -14, 4)
        lead_kn = v(s * 12, 17, 27); rear_kn = v(-s * 11, -6, 27)
        lead_dir = v(0, 1, 0); rear_dir = v(-s * 0.4, 0.92, 0)
        hz = 47
    elif kind == "sanchin_kneesout":
        lead_ank = v(s * 10, 8, 4); rear_ank = v(-s * 10, -8, 4)
        lead_kn = v(s * 13, 12, 27); rear_kn = v(-s * 13, -3, 27)
        lead_dir = v(s * 0.3, 0.95, 0); rear_dir = v(-s * 0.35, 0.94, 0)
        hz = 50
    elif kind == "sanchin_straight":   # fault: locked knees
        lead_ank = v(s * 10, 8, 4); rear_ank = v(-s * 10, -8, 4)
        lead_kn = v(s * 9, 6, 29); rear_kn = v(-s * 9, -5, 29)
        lead_dir = v(-s * 0.37, 0.93, 0); rear_dir = v(-s * 0.17, 0.98, 0)
        hz = 53
    elif kind == "musubi":
        lead_ank = v(s * 3, 0, 4); rear_ank = v(-s * 3, 0, 4)
        lead_kn = v(s * 5, 1, 28); rear_kn = v(-s * 5, 1, 28)
        lead_dir = v(s * 0.5, 0.87, 0); rear_dir = v(-s * 0.5, 0.87, 0)
        hz = 52
    elif kind == "heisoku":
        lead_ank = v(s * 3, 0, 4); rear_ank = v(-s * 3, 0, 4)
        lead_kn = v(s * 4.5, 1, 28); rear_kn = v(-s * 4.5, 1, 28)
        lead_dir = v(0, 1, 0); rear_dir = v(0, 1, 0)
        hz = 52
    elif kind == "step_mid":   # moving foot drawn in beside the standing foot
        lead_ank = v(s * 4, 0, 6); rear_ank = v(-s * 10, -8, 4)
        lead_kn = v(s * 5, 6, 28); rear_kn = v(-s * 7, -3, 27)
        lead_dir = v(-s * 0.1, 1, 0); rear_dir = v(-s * 0.17, 0.98, 0)
        hz = 50
    elif kind == "parallel":   # heiko-like, shoulder width
        lead_ank = v(s * 10, 0, 4); rear_ank = v(-s * 10, 0, 4)
        lead_kn = v(s * 10, 2, 28); rear_kn = v(-s * 10, 2, 28)
        lead_dir = v(0, 1, 0); rear_dir = v(0, 1, 0)
        hz = 52
    elif kind == "shiko":
        lead_ank = v(s * 22, 0, 4); rear_ank = v(-s * 22, 0, 4)
        lead_kn = v(s * 22, 6, 24); rear_kn = v(-s * 22, 6, 24)
        lead_dir = v(s * 0.7, 0.7, 0); rear_dir = v(-s * 0.7, 0.7, 0)
        hz = 38
    else:
        raise KeyError(kind)
    out = {}
    if lead == "L":
        out.update(lkn=lead_kn, lank=lead_ank, ldir=lead_dir, rkn=rear_kn, rank=rear_ank, rdir=rear_dir)
    else:
        out.update(rkn=lead_kn, rank=lead_ank, rdir=lead_dir, lkn=rear_kn, lank=rear_ank, ldir=rear_dir)
    out["hz"] = hz
    return out


class Pose:
    def __init__(self, larm="side", rarm="side", stance="musubi", lead="R", lean=0.0, tuck=0.0,
                 shrug=0.0, chin=0.0, hipshift=0.0, gaze=0.0):
        L = legs(stance, lead)
        hz = L["hz"]
        dz = hz - HIP_Z
        self.j = {}
        j = self.j
        lean_y = lean   # positive = upper body forward
        j["lhip"], j["rhip"] = v(7.5, hipshift - tuck, hz), v(-7.5, hipshift - tuck, hz)
        j["lsh"], j["rsh"] = v(11, lean_y, SH_Z + dz + shrug), v(-11, lean_y, SH_Z + dz + shrug)
        j["neck"] = v(0, lean_y + 0.5 + chin, SH_Z + dz + 4 + shrug * 0.6)
        j["head"] = v(0, lean_y + 1.5 + chin * 1.6, SH_Z + dz + 12.5 + shrug * 0.4)
        self.gaze = gaze
        for side, kind in (("l", larm), ("r", rarm)):
            s = 1 if side == "l" else -1
            e, w, h, t = arm(kind, s)
            off = v(0, lean_y, dz + shrug)
            j[side + "el"], j[side + "wr"], j[side + "hd"] = e + off, w + off, h + off
            j[side + "ht"] = t
        for k in ("lkn", "lank", "rkn", "rank"):
            j[k] = L[k]
        j["ldir"], j["rdir"] = L["ldir"], L["rdir"]
        self.tuck, self.lean = tuck, lean

    def copy(self):
        import copy
        return copy.deepcopy(self)


def _rot(th):
    t = math.radians(th)
    r = v(math.cos(t), -math.sin(t), 0)
    c = v(math.sin(t), math.cos(t), 0)
    return r, c


class Figure:
    """Draw a Pose on an axes at screen offset (ox, oy) with scale sc (units per 100 height)."""

    def __init__(self, ax, pose, ox=50, oy=0, sc=1.0, th=0, elev=0, ghost=False, lw=0.8,
                 fill=WH, edge=K, belt=True, zorder=2):
        self.ax, self.p, self.ox, self.oy, self.sc, self.th = ax, pose, ox, oy, sc, th
        self.elev = math.radians(elev)
        self.r, self.c = _rot(th)
        self.ghost = ghost
        self.lw = lw
        self.fill = G1 if ghost and fill == WH else fill
        self.edge = G2 if ghost else edge
        self.ls = (0, (3, 2)) if ghost else "solid"
        self.belt = belt and not ghost
        self.z0 = zorder
        self.draw()

    def P(self, p):
        p = np.asarray(p, float)
        x = p @ self.r
        d = p @ self.c
        y = p[2] * math.cos(self.elev) - d * math.sin(self.elev) * 0.6
        return np.array([self.ox + x * self.sc, self.oy + y * self.sc])

    def depth(self, p):
        return float(np.asarray(p, float) @ self.c)

    def joint(self, name):
        return self.P(self.p.j[name])

    def _poly(self, pts, z, fc=None, lw=None):
        poly = Polygon(pts, closed=True, fc=fc or self.fill, ec=self.edge, lw=lw or self.lw,
                       ls=self.ls, joinstyle="round", zorder=z)
        self.ax.add_patch(poly)
        return poly

    def draw(self):
        j, sc = self.p.j, self.sc
        items = []  # (depth, kind, data)
        # torso: stacked elliptical rings projected; outline = left/right extremes per ring
        lean = self.p.lean
        shz = j["lsh"][2]
        rings = ((shz + 2.0, 8.5, 4.5, lean), (shz - 1.5, 11.6, 5.8, lean), (shz - 9, 11.0, 6.6, lean * 0.85),
                 (64, 9.2, 6.0, lean * 0.45), (57, 9.0, 5.6, lean * 0.15 - self.p.tuck * 0.3),
                 (j["lhip"][2] + 0.5, 10.2, 6.4, j["lhip"][1]), (j["lhip"][2] - 5, 7.5, 5.5, j["lhip"][1] * 0.8))
        left, right = [], []
        for zz, half, dep, yoff in rings:
            pr = [self.P(v(half * math.cos(t), yoff + dep * math.sin(t), zz)) for t in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
            pr = sorted(pr, key=lambda q: q[0])
            left.append(pr[0]); right.append(pr[-1])
        torso2d = [right[0]] + left + right[::-1]
        torso2d = hull(torso2d) if self.th not in (0, 180) and abs(abs(self.th) - 90) > 1e-6 and False else torso2d
        items.append((0.0, "torso", torso2d))
        # limbs
        segs = []
        for s in ("l", "r"):
            segs += [(j[s + "hip"], j[s + "kn"], 7.6, 6.4), (j[s + "kn"], j[s + "ank"], 6.2, 4.8)]
            segs += [(j[s + "sh"], j[s + "el"], 5.6, 4.8), (j[s + "el"], j[s + "wr"], 4.8, 3.9)]
        for a, b, w1, w2 in segs:
            dmean = (self.depth(a) + self.depth(b)) / 2
            items.append((dmean, "seg", (self.P(a), self.P(b), w1 * sc, w2 * sc)))
        # hands
        for s in ("l", "r"):
            items.append((self.depth(j[s + "hd"]) + 0.5, "hand", (s, j[s + "ht"])))
        # feet
        for s in ("l", "r"):
            items.append((self.depth(j[s + "ank"]) - 0.3, "foot", s))
        # head
        items.append((self.depth(j["head"]), "head", None))
        items.sort(key=lambda t: t[0])
        z = self.z0
        for dep, kind, data in items:
            z += 0.01
            if kind == "torso":
                poly = self._poly(data, z)
                if self.belt:
                    # belt band clipped to torso
                    bz = j["lhip"][2] + 4.0
                    a = self.P(v(-20, 0, bz)); b = self.P(v(20, 0, bz))
                    lo, hi = min(a[0], b[0]) - 40 * sc, max(a[0], b[0]) + 40 * sc
                    band = Rectangle((lo, a[1] - 1.3 * sc), hi - lo, 2.8 * sc, fc=K, ec="none", zorder=z + 0.001)
                    self.ax.add_patch(band); band.set_clip_path(poly)
                    fwd = float(v(0, 1, 0) @ self.c)
                    if fwd > 0.3:
                        shz = j["lsh"][2]; hz2 = j["lhip"][2] + 4.0
                        for sx in (-1, 1):
                            a1 = self.P(v(sx * 3.5, lean + 6, shz + 1.5)); b1 = self.P(v(-sx * 0.8, lean * 0.2 + 6, hz2 + 3))
                            self.ax.plot([a1[0], b1[0]], [a1[1], b1[1]], color=self.edge, lw=self.lw * 0.7, zorder=z + 0.002)
            elif kind == "seg":
                p, q, w1, w2 = data
                self._poly(taper(p, q, w1, w2), z)
            elif kind == "hand":
                s, t = data
                wr, hd = self.P(j[s + "wr"]), self.P(j[s + "hd"])
                if t == "fist":
                    c = hd
                    self._poly(taper(wr, c, 4.4 * sc, 5.6 * sc), z)
                    self.ax.add_patch(Circle(c, 2.9 * sc, fc=self.fill, ec=self.edge, lw=self.lw, ls=self.ls, zorder=z + 0.002))
                else:
                    self._poly(taper(wr, hd, 4.2 * sc, 2.4 * sc), z)
            elif kind == "foot":
                s = data
                ank = j[s + "ank"]; d = unit(j[s + "dir"])
                heel = ank[:2] - d[:2] * 3.2
                sole = sole_points(heel, d, 15, left=(s == "l"))
                pts3 = [v(px, py, 0) for px, py in sole]
                ridge = [v(*(heel + d[:2] * t * 15), 1.5 + 5 * max(0, 1 - abs(t - 0.25) / 0.6)) for t in np.linspace(0.05, 0.95, 8)]
                pts3 += ridge + [ank + v(0, 0, 1.5)]
                f2 = hull([self.P(p) for p in pts3])
                self._poly(f2, z)
            elif kind == "head":
                c = self.P(j["head"])
                self.ax.add_patch(Circle(c, 6.3 * sc, fc=self.fill, ec=self.edge, lw=self.lw, ls=self.ls, zorder=z))
                # neck
                n0 = self.P(j["neck"] + v(0, 0, -4))
                # face direction marker: eye dot and nose tick
                fwd = v(0, 1, 0)
                sx = float(fwd @ self.r)
                if abs(sx) > 0.25 and not self.ghost:
                    eye = c + np.array([sx * 3.4 * sc, 0.8 * sc])
                    self.ax.add_patch(Circle(eye, 0.65 * sc, fc=K, ec="none", zorder=z + 0.002))
                elif not self.ghost:
                    for ex in (-2.2, 2.2):
                        self.ax.add_patch(Circle(c + np.array([ex * sc, 0.8 * sc]), 0.55 * sc, fc=K, ec="none", zorder=z + 0.002))
        # neck drawn under head, over torso
        n_top, n_bot = self.P(j["neck"] + v(0, 0, 2)), self.P(j["neck"] + v(0, 0, -3))
        self._poly(capsule(n_bot, n_top, 5.2 * sc), self.z0 + 0.005)

    # convenience
    def top(self):
        return self.P(self.p.j["head"]) + np.array([0, 7 * self.sc])


# ------------------------------------------------------------------ annotation helpers
def arrow(ax, x1, y1, x2, y2, c=K, lw=1.0, ms=7, ls="-", rad=0.0, both=False, z=5):
    st = "<|-|>" if both else "-|>"
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=st, mutation_scale=ms, color=c, lw=lw, linestyle=ls,
                        shrinkA=0, shrinkB=0, connectionstyle=f"arc3,rad={rad}", zorder=z)
    ax.add_patch(a)
    return a


def line(ax, xs, ys, c=K, lw=0.8, ls="-", z=4, **kw):
    ax.plot(xs, ys, color=c, lw=lw, ls=ls, solid_capstyle="round", zorder=z, **kw)


def label(ax, x, y, s, fs=7, ha="center", va="center", c=K, weight="normal", style="normal", z=6, family=None, **kw):
    return ax.text(x, y, s, fontsize=fs, ha=ha, va=va, color=c, fontweight=weight, fontstyle=style, zorder=z,
                   family=family or "Source Sans 3", **kw)


def callout(ax, x, y, tx, ty, s, fs=6.6, ha=None, z=6):
    """Leader line from point (x,y) to text at (tx,ty)."""
    ax.plot([x, tx], [y, ty], color=K, lw=0.45, zorder=z)
    ax.add_patch(Circle((x, y), 0.7, fc=K, ec="none", zorder=z))
    if ha is None:
        ha = "left" if tx >= x else "right"
    off = 0.8 if ha == "left" else -0.8
    ax.text(tx + off, ty, s, fontsize=fs, ha=ha, va="center", zorder=z + 1, linespacing=1.1,
            bbox=dict(fc=WH, ec="none", pad=0.4, alpha=0.9))


def numdot(ax, x, y, n, r=2.6, fs=6.2, inv=True, z=7):
    ax.add_patch(Circle((x, y), r, fc=K if inv else WH, ec=K, lw=0.7, zorder=z))
    ax.text(x, y - 0.1, str(n), fontsize=fs, ha="center", va="center", color=WH if inv else K, fontweight="bold", zorder=z + 0.1)


def tick_mark(ax, x, y, r=3.2, z=8):
    ax.add_patch(Circle((x, y), r, fc=WH, ec=K, lw=0.9, zorder=z))
    ax.plot([x - r*0.5, x - r*0.12, x + r*0.55], [y, y - r*0.45, y + r*0.5], color=K, lw=1.2, zorder=z + 0.1, solid_capstyle="round")


def cross_mark(ax, x, y, r=3.2, z=8):
    ax.add_patch(Circle((x, y), r, fc=K, ec=K, lw=0.9, zorder=z))
    d = r * 0.42
    ax.plot([x - d, x + d], [y - d, y + d], color=WH, lw=1.3, zorder=z + 0.1, solid_capstyle="round")
    ax.plot([x - d, x + d], [y + d, y - d], color=WH, lw=1.3, zorder=z + 0.1, solid_capstyle="round")


def dim(ax, x1, y1, x2, y2, s="", off=0, fs=6.2, z=6):
    """Dimension line with end ticks."""
    p, q = np.array([x1, y1]), np.array([x2, y2])
    d = unit(q - p); n = np.array([-d[1], d[0]])
    p2, q2 = p + n * off, q + n * off
    arrow(ax, *p2, *q2, lw=0.5, ms=5, both=True, z=z)
    for a in (p2, q2):
        ax.plot([a[0] - n[0] * 1.5, a[0] + n[0] * 1.5], [a[1] - n[1] * 1.5, a[1] + n[1] * 1.5], color=K, lw=0.5, zorder=z)
    if s:
        m = (p2 + q2) / 2 + n * 2.6
        ax.text(*m, s, fontsize=fs, ha="center", va="center", zorder=z,
                bbox=dict(fc=WH, ec="none", pad=0.6))


def plumb(ax, x, y1, y2, z=1.5):
    ax.plot([x, x], [y1, y2], color=K, lw=0.5, ls=(0, (4, 2.5)), zorder=z)


def floor(ax, x1, x2, y=0, z=1):
    ax.plot([x1, x2], [y, y], color=K, lw=0.6, zorder=z)
    for xx in np.arange(x1, x2, 3):
        ax.plot([xx, xx - 1.8], [y, y - 1.8], color=K, lw=0.3, zorder=z)


def frame_label(ax, x, y, s, fs=6.5):
    ax.text(x, y, s, fontsize=fs, ha="center", va="top", fontweight="bold", zorder=6)


def sub_label(ax, x, y, s, fs=6.2):
    ax.text(x, y, s, fontsize=fs, ha="center", va="top", zorder=6, style="italic", family=SERIF)


def breath_tag(ax, x, y, s, fs=5.6):
    ax.text(x, y, s, fontsize=fs, ha="center", va="center", zorder=7, color=K,
            bbox=dict(boxstyle="round,pad=0.25", fc=WH, ec=K, lw=0.5))


def curved(ax, p, q, rad=0.3, lw=0.9, ms=6, ls="-", c=K):
    return arrow(ax, p[0], p[1], q[0], q[1], rad=rad, lw=lw, ms=ms, ls=ls, c=c)


# ------------------------------------------------------------------ top-view feet
def foot_top(ax, heel, ang_deg, length=15, left=True, fill=WH, ls="solid", lw=0.9, z=3, ec=K, toes=True):
    """Footprint seen from above. heel = heel point. ang_deg: 0 = toes up the page; + = turned clockwise."""
    a = math.radians(ang_deg)
    d = np.array([math.sin(a), math.cos(a)])
    pts = sole_points(heel, d, length, left=left)
    ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=ec, lw=lw, ls=ls, zorder=z, joinstyle="round"))
    if toes:
        for c, rx, ry, dd in toe_points(heel, d, length, left=left):
            ax.add_patch(Ellipse(c, 2 * rx, 2 * ry, angle=math.degrees(math.atan2(dd[1], dd[0])) - 90,
                                 fc=fill, ec=ec, lw=lw * 0.7, ls=ls, zorder=z))
    return pts


def foot_axis(heel, ang_deg, length=15):
    a = math.radians(ang_deg)
    d = np.array([math.sin(a), math.cos(a)])
    return np.asarray(heel, float), np.asarray(heel, float) + d * length
