"""Black-and-white technical figure library for the Goju-Ryu close-combat book.

Figures are side-view articulated mannequins built with simple inverse kinematics.
Figure A ("you", the defender) is drawn solid black; Figure B (the opponent) is drawn
white with a black outline. Far-side limbs are drawn in grey so depth reads clearly.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Ellipse, Polygon, Rectangle, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "..", "figures")
os.makedirs(OUTDIR, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
FONT = {"family": "DejaVu Sans"}

# segment lengths (metres-ish)
L = dict(thigh=0.44, shin=0.43, torso=0.52, neck=0.07, head=0.115, uarm=0.29, farm=0.27, foot=0.2)

BLACK, DARK, MID, LIGHT, WHITE = "#000000", "#4a4a4a", "#8c8c8c", "#cfcfcf", "#ffffff"


def _ik(a, t, l1, l2, bend):
    """Two-link IK from root a to target t. bend=+1/-1 picks the elbow side."""
    ax, ay = a
    dx, dy = t[0] - ax, t[1] - ay
    d = math.hypot(dx, dy)
    d = max(min(d, l1 + l2 - 1e-4), abs(l1 - l2) + 1e-4)
    ang = math.atan2(dy, dx)
    c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    c = max(-1, min(1, c))
    off = math.acos(c) * bend
    jx, jy = ax + l1 * math.cos(ang + off), ay + l1 * math.sin(ang + off)
    ex, ey = ax + (l1 + l2) * math.cos(ang) if d >= l1 + l2 - 1e-3 else t[0], 0
    end = (ax + d * math.cos(ang), ay + d * math.sin(ang))
    return (jx, jy), end


class Person:
    """A side-view mannequin.

    hip: pelvis centre. face: +1 faces right, -1 faces left. lean: torso lean in degrees
    (positive = towards facing direction). hands/feet: dicts with 'near' and 'far' targets
    in absolute coordinates. Use relative helpers for convenience.
    """

    def __init__(self, hip=(0, 0.9), face=1, lean=5, head=0, hands=None, feet=None,
                 style="A", fist=("near", "far"), open_hand=(), elbow=None, knee=None,
                 toes=None, label=None, crouch=0.0, shoulder_shift=0.0):
        self.hip = hip
        self.face = face
        self.lean = lean
        self.headtilt = head
        self.style = style
        self.label = label
        self.fist = fist
        self.open_hand = open_hand
        f = face
        hx, hy = hip
        self.hands = hands or {"near": (hx + f * 0.42, hy + 0.42), "far": (hx + f * 0.28, hy + 0.5)}
        self.feet = feet or {"near": (hx + f * 0.3, 0.06), "far": (hx - f * 0.3, 0.06)}
        self.elbow = elbow or {"near": -1, "far": -1}   # -1 = elbow below the line (natural)
        self.knee = knee or {"near": 1, "far": 1}       # +1 = knee forward
        self.toes = toes or {"near": 0, "far": 0}       # foot angle offset degrees
        self.shoulder_shift = shoulder_shift

    # geometry ---------------------------------------------------------
    def joints(self):
        f = self.face
        hx, hy = self.hip
        a = math.radians(self.lean)
        sx = hx + f * L["torso"] * math.sin(a) + f * self.shoulder_shift
        sy = hy + L["torso"] * math.cos(a)
        nx = sx + f * L["neck"] * math.sin(a + math.radians(self.headtilt))
        ny = sy + L["neck"] * math.cos(a)
        hcx = nx + f * (L["head"] * 0.9) * math.sin(a + math.radians(self.headtilt))
        hcy = ny + L["head"] * 0.95 * math.cos(a + math.radians(self.headtilt))
        j = {"hip": (hx, hy), "sh": (sx, sy), "neck": (nx, ny), "head": (hcx, hcy)}
        for side in ("near", "far"):
            tgt = self.hands[side]
            e1, h = _ik((sx, sy), tgt, L["uarm"], L["farm"], 1)
            e2, _ = _ik((sx, sy), tgt, L["uarm"], L["farm"], -1)
            pref = self.elbow[side]
            if pref in (-1, 1):   # -1 elbow low, +1 elbow high
                e = min((e1, e2), key=lambda p: p[1] * -pref) if True else e1
                e = e1 if (e1[1] - e2[1]) * pref > 0 else e2
            else:                 # 'out' = elbow away from facing (behind), 'in' = in front
                e = e1 if (e1[0] - e2[0]) * f * (1 if pref == "in" else -1) > 0 else e2
            j[side + "_el"], j[side + "_hand"] = e, h
            ft = self.feet[side]
            k1, an = _ik((hx, hy), ft, L["thigh"], L["shin"], 1)
            k2, _ = _ik((hx, hy), ft, L["thigh"], L["shin"], -1)
            kb = self.knee[side]
            k = k1 if (k1[0] - k2[0]) * f * kb > 0 else k2
            j[side + "_kn"], j[side + "_an"] = k, an
        return j

    # drawing ----------------------------------------------------------
    def _seg(self, ax, p, q, w, depth, z):
        if self.style == "A":
            col = BLACK if depth == "near" else DARK
            ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=w, solid_capstyle="round", zorder=z)
        else:
            ax.plot([p[0], q[0]], [p[1], q[1]], color=BLACK, lw=w, solid_capstyle="round", zorder=z)
            fill = WHITE if depth == "near" else LIGHT
            ax.plot([p[0], q[0]], [p[1], q[1]], color=fill, lw=max(w - 2.2, w * 0.55), solid_capstyle="round", zorder=z + 0.01)

    def _hand(self, ax, side, j, w, z):
        e, h = j[side + "_el"], j[side + "_hand"]
        ang = math.atan2(h[1] - e[1], h[0] - e[0])
        r = 0.045
        cx, cy = h[0] + r * 0.6 * math.cos(ang), h[1] + r * 0.6 * math.sin(ang)
        depth = side
        if side in self.open_hand:
            q = (h[0] + 0.1 * math.cos(ang), h[1] + 0.1 * math.sin(ang))
            self._seg(ax, h, q, w * 0.62, depth, z)
            return
        if self.style == "A":
            col = BLACK if depth == "near" else DARK
            ax.add_patch(Circle((cx, cy), r, fc=col, ec=col, zorder=z + 0.02))
        else:
            fill = WHITE if depth == "near" else LIGHT
            ax.add_patch(Circle((cx, cy), r, fc=fill, ec=BLACK, lw=1.1, zorder=z + 0.02))

    def _foot(self, ax, side, j, w, z):
        an = j[side + "_an"]
        a = math.radians(self.toes[side])
        q = (an[0] + self.face * L["foot"] * math.cos(a), an[1] + L["foot"] * math.sin(a) * 1)
        q = (an[0] + self.face * L["foot"] * math.cos(a), an[1] + L["foot"] * math.sin(a))
        self._seg(ax, (an[0] - self.face * 0.03, an[1]), q, w * 0.8, side, z)

    def draw(self, ax, scale=1.0, zbase=10):
        j = self.joints()
        fig = ax.figure
        x0, x1 = ax.get_xlim()
        ppu = ax.get_position().width * fig.get_figwidth() * 72 / (x1 - x0)  # points per data unit
        W = 0.085 * ppu * scale   # limb thickness
        TW = 0.2 * ppu * scale    # torso thickness
        self._ppu = ppu
        zf, zt, zn = zbase, zbase + 1, zbase + 2
        # far limbs
        self._seg(ax, j["hip"], j["far_kn"], W * 1.15, "far", zf)
        self._seg(ax, j["far_kn"], j["far_an"], W, "far", zf)
        self._foot(ax, "far", j, W, zf)
        self._seg(ax, j["sh"], j["far_el"], W * 0.95, "far", zf)
        self._seg(ax, j["far_el"], j["far_hand"], W * 0.88, "far", zf)
        self._hand(ax, "far", j, W, zf)
        # torso + head
        self._seg(ax, j["hip"], j["sh"], TW, "near", zt)
        self._seg(ax, j["sh"], j["neck"], W * 0.8, "near", zt)
        hc = j["head"]
        if self.style == "A":
            ax.add_patch(Circle(hc, L["head"], fc=BLACK, ec=BLACK, zorder=zt + 0.05))
        else:
            ax.add_patch(Circle(hc, L["head"], fc=WHITE, ec=BLACK, lw=1.1, zorder=zt + 0.05))
        # belt mark
        bx, by = j["hip"]
        a = math.radians(self.lean)
        bx2, by2 = bx + self.face * 0.09 * math.sin(a), by + 0.09 * math.cos(a)
        perp = (math.cos(a) * 0.075, -self.face * math.sin(a) * 0.075)
        col = WHITE if self.style == "A" else BLACK
        ax.plot([bx2 - perp[0], bx2 + perp[0]], [by2 - perp[1], by2 + perp[1]], color=col, lw=1.3 * scale, zorder=zt + 0.03)
        # near limbs
        self._seg(ax, j["hip"], j["near_kn"], W * 1.15, "near", zn)
        self._seg(ax, j["near_kn"], j["near_an"], W, "near", zn)
        self._foot(ax, "near", j, W, zn)
        self._seg(ax, j["sh"], j["near_el"], W * 0.95, "near", zn + 0.1)
        self._seg(ax, j["near_el"], j["near_hand"], W * 0.88, "near", zn + 0.1)
        self._hand(ax, "near", j, W, zn + 0.1)
        if self.label:
            ax.text(hc[0], hc[1] + 0.2, self.label, ha="center", va="bottom", fontsize=7.5,
                    fontweight="bold", zorder=40)
        return j


# ------------------------------------------------------------------ helpers
def stance(x=0.0, face=1, style="A", width=0.62, lean=4, guard="high", hip_h=0.86, **kw):
    """Sanchin-ish / fighting stance with guard. Returns Person."""
    f = face
    hx = x
    feet = {"near": (hx + f * width * 0.55, 0.06), "far": (hx - f * width * 0.45, 0.06)}
    sx = hx + f * 0.05
    if guard == "high":
        hands = {"near": (hx + f * 0.42, hip_h + 0.62), "far": (hx + f * 0.24, hip_h + 0.52)}
    elif guard == "mid":
        hands = {"near": (hx + f * 0.44, hip_h + 0.42), "far": (hx + f * 0.22, hip_h + 0.38)}
    elif guard == "fence":
        hands = {"near": (hx + f * 0.48, hip_h + 0.56), "far": (hx + f * 0.36, hip_h + 0.5)}
    else:
        hands = {"near": (hx + f * 0.12, hip_h + 0.12), "far": (hx - f * 0.02, hip_h + 0.14)}
    p = dict(hip=(hx, hip_h), face=f, lean=lean, hands=hands, feet=feet, style=style)
    p.update(kw)
    return Person(**p)


def arrow(ax, p, q, rad=0.0, lw=1.4, dashed=False, head=9, col=BLACK, z=50):
    ls = (0, (3, 2)) if dashed else "-"
    a = FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}", arrowstyle=f"-|>,head_length={head/20},head_width={head/36}",
                        lw=lw, color=col, linestyle=ls, zorder=z, shrinkA=0, shrinkB=0, mutation_scale=12)
    ax.add_patch(a)


def tag(ax, x, y, s, size=7, box=True, z=60, ha="center"):
    if box:
        ax.text(x, y, s, ha=ha, va="center", fontsize=size, zorder=z,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="black", lw=0.6))
    else:
        ax.text(x, y, s, ha=ha, va="center", fontsize=size, zorder=z)


def numdot(ax, x, y, n, z=61, size=6.5):
    ax.add_patch(Circle((x, y), 0.055, fc="black", ec="black", zorder=z))
    ax.text(x, y - 0.002, str(n), ha="center", va="center", fontsize=size, color="white", fontweight="bold", zorder=z + 1)


def impact(ax, x, y, r=0.09, n=8, z=55):
    for i in range(n):
        a = 2 * math.pi * i / n
        ax.plot([x + r * 0.45 * math.cos(a), x + r * math.cos(a)], [y + r * 0.45 * math.sin(a), y + r * math.sin(a)],
                color="black", lw=0.9, zorder=z)


def ground(ax, x0=-1.6, x1=1.6):
    ax.plot([x0, x1], [0.0, 0.0], color="black", lw=0.9, zorder=1)
    for i in range(int((x1 - x0) / 0.12)):
        x = x0 + i * 0.12
        ax.plot([x, x - 0.07], [0.0, -0.06], color=MID, lw=0.5, zorder=1)


def panel_axes(fig, rect, xlim=(-1.25, 1.25), ylim=(-0.12, 2.05), frame=True):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(frame)
        s.set_linewidth(0.6)
    return ax


def sequence(name, panels, cols=None, width=4.5, panel_h=None, xlim=(-1.25, 1.25), ylim=(-0.12, 2.05),
             captions=True, frame=True):
    """panels: list of callables f(ax) each drawing one panel, with optional .title attribute."""
    n = len(panels)
    cols = cols or min(n, 3)
    rows = math.ceil(n / cols)
    pw = width / cols
    ar = (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
    ph = panel_h or pw * ar
    cap_h = 0.2 if captions else 0.0
    H = rows * (ph + cap_h)
    fig = plt.figure(figsize=(width, H))
    for i, fn in enumerate(panels):
        r, c = divmod(i, cols)
        left = c * pw / width + 0.008
        bottom = 1 - ((r + 1) * (ph + cap_h)) / H + cap_h / H
        ax = panel_axes(fig, [left, bottom, pw / width - 0.016, ph / H - 0.01], xlim, ylim, frame)
        ground(ax, xlim[0], xlim[1])
        fn(ax)
        t = getattr(fn, "title", None)
        if captions and t:
            fig.text(left + (pw / width - 0.016) / 2, bottom - 0.012, t, ha="center", va="top", fontsize=7)
        if n > 1:
            ax.text(xlim[0] + 0.08, ylim[1] - 0.1, str(i + 1), fontsize=9, fontweight="bold", va="top", ha="left", zorder=70)
    save(fig, name)


def titled(title):
    def deco(fn):
        fn.title = title
        return fn
    return deco


def save(fig, name):
    path = os.path.join(OUTDIR, name + ".png")
    fig.savefig(path, dpi=300, facecolor="white")
    plt.close(fig)
    # convert to pure greyscale
    from PIL import Image
    im = Image.open(path).convert("L")
    im.save(path, dpi=(300, 300))
    print("wrote", path)


# ------------------------------------------------------------------ top-down footwork diagrams
def footprint(ax, x, y, ang, side="L", fill="black", label=True, s=1.0, z=10, ec="black"):
    """Draw a footprint at (x,y) pointing in direction ang (deg, 90 = up)."""
    a = math.radians(ang - 90)
    def rot(px, py):
        return (x + (px * math.cos(a) - py * math.sin(a)) * s, y + (px * math.sin(a) + py * math.cos(a)) * s)
    mirror = -1 if side == "L" else 1
    sole = Ellipse(rot(0, 0.02), 0.11 * s, 0.24 * s, angle=ang - 90, fc=fill, ec=ec, lw=0.8, zorder=z)
    heel = Ellipse(rot(0, -0.13), 0.085 * s, 0.1 * s, angle=ang - 90, fc=fill, ec=ec, lw=0.8, zorder=z)
    ax.add_patch(sole)
    ax.add_patch(heel)
    if label:
        tx, ty = rot(0, 0.0)
        ax.text(tx, ty, side, ha="center", va="center", fontsize=5.5, color="white" if fill == "black" else "black",
                fontweight="bold", zorder=z + 1, rotation=0)


def plan_axes(fig, rect, lim=1.0):
    ax = fig.add_axes(rect)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(0.6)
    return ax


# ------------------------------------------------------------------ front-view body outline
def front_body(ax, cx=0.0, scale=1.0, fill="white", z=5):
    """Simple front-facing silhouette outline for target maps."""
    s = scale
    def P(x, y):
        return (cx + x * s, y * s)
    ax.add_patch(Circle(P(0, 1.68), 0.12 * s, fc=fill, ec="black", lw=1.2, zorder=z))
    body = [P(-0.05, 1.55), P(-0.2, 1.5), P(-0.24, 1.42), P(-0.33, 1.05), P(-0.36, 0.82), P(-0.3, 0.82),
            P(-0.24, 1.2), P(-0.2, 1.0), P(-0.19, 0.84), P(-0.21, 0.45), P(-0.2, 0.06), P(-0.08, 0.06),
            P(-0.06, 0.45), P(-0.02, 0.8), P(0.02, 0.8), P(0.06, 0.45), P(0.08, 0.06), P(0.2, 0.06),
            P(0.21, 0.45), P(0.19, 0.84), P(0.2, 1.0), P(0.24, 1.2), P(0.3, 0.82), P(0.36, 0.82),
            P(0.33, 1.05), P(0.24, 1.42), P(0.2, 1.5), P(0.05, 1.55)]
    ax.add_patch(Polygon(body, closed=True, fc=fill, ec="black", lw=1.2, zorder=z, joinstyle="round"))
    ax.plot([cx - 0.19 * s, cx + 0.19 * s], [0.86 * s, 0.86 * s], color="black", lw=0.8, zorder=z + 1)
