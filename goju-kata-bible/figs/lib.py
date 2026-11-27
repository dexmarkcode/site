"""Black-and-white illustration engine for the Goju-Ryu Karate Kata Bible.

Draws a clean, outlined karateka mannequin (side or front view), top-down
footprints, embusen floor maps and numbered sequence strips. Everything is
pure black, white and neutral greys so it prints well on a black-ink interior.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, Ellipse, Polygon, FancyArrowPatch, Rectangle, FancyBboxPatch, Arc
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
for f in (ROOT / "fonts").glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))

INK = "#000000"
DARK = "#3a3a3a"
MID = "#8a8a8a"
FAR = "#c9c9c9"      # far-side limbs
PALE = "#ececec"
WHITE = "#ffffff"

plt.rcParams.update({
    "font.family": "Source Sans 3", "font.size": 8, "savefig.dpi": 300,
    "axes.linewidth": 0.6,
})
W = 4.5  # text block width (inches)


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", pad_inches=0.03, facecolor="white", dpi=300)
    plt.close(fig)


def canvas(w=W, h=2.6, xlim=(0, 100), ylim=None):
    fig, ax = plt.subplots(figsize=(w, h))
    if ylim is None:
        ylim = (0, 100 * h / w)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def arrow(ax, x1, y1, x2, y2, c=INK, lw=1.0, ms=7, ls="-", both=False, rad=0.0, z=20):
    st = "<|-|>" if both else "-|>"
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=st, mutation_scale=ms, color=c, lw=lw,
                        linestyle=ls, shrinkA=0, shrinkB=0, connectionstyle=f"arc3,rad={rad}", zorder=z)
    ax.add_patch(a)


def label(ax, x, y, s, fs=7, c=INK, ha="center", va="center", **kw):
    kw.setdefault("zorder", 25)
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va, **kw)


def box(ax, x, y, w, h, text="", fc=WHITE, ec=INK, tc=INK, fs=7, bold=False, lw=0.8, r=0.8, z=5):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(p)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, zorder=z + 1,
                fontweight="semibold" if bold else "normal", linespacing=1.15)


# ======================================================================
#  MANNEQUIN
# ======================================================================
THIGH, SHIN = 2.65, 2.55

# Stances. Side view: performer faces +x. Feet given as (x, y) relative to hip x.
# 'front' names which foot is forward (L or R). Front view: performer faces the reader;
# performer's left is the reader's right (+x).
STANCES = {
    # ---- front view
    "musubi":   dict(view="front", hip=5.1, feet={"L": (0.35, 0), "R": (-0.35, 0)}, knee="straight", toe="out"),
    "heiko":    dict(view="front", hip=5.05, feet={"L": (0.75, 0), "R": (-0.75, 0)}, knee="straight", toe="fwd"),
    "hachiji":  dict(view="front", hip=5.05, feet={"L": (0.8, 0), "R": (-0.8, 0)}, knee="straight", toe="out"),
    "shiko":    dict(view="front", hip=3.55, feet={"L": (2.75, 0), "R": (-2.75, 0)}, knee="out", toe="out"),
    "sanchin_f": dict(view="front", hip=4.75, feet={"L": (0.9, 0), "R": (-0.9, 0)}, knee="in", toe="in"),
    "sagi_L":   dict(view="front", hip=5.0, feet={"L": (0.25, 3.0), "R": (-0.45, 0)}, knee="lift", toe="fwd", lift="L"),
    "sagi_R":   dict(view="front", hip=5.0, feet={"L": (0.45, 0), "R": (-0.25, 3.0)}, knee="lift", toe="fwd", lift="R"),
    "kosa_f":   dict(view="front", hip=4.0, feet={"L": (0.9, 0), "R": (-0.4, 0.5)}, knee="in", toe="out"),
    "seiza":    dict(view="front", hip=2.2, feet={"L": (0.7, 0), "R": (-0.7, 0)}, knee="kneel", toe="fwd"),
    # ---- side view
    "zenkutsu_L": dict(view="side", hip=4.25, front="L", feet={"L": (2.55, 0), "R": (-2.45, 0)}),
    "zenkutsu_R": dict(view="side", hip=4.25, front="R", feet={"R": (2.55, 0), "L": (-2.45, 0)}),
    "sanchin_L":  dict(view="side", hip=4.8, front="L", feet={"L": (1.05, 0), "R": (-0.95, 0)}),
    "sanchin_R":  dict(view="side", hip=4.8, front="R", feet={"R": (1.05, 0), "L": (-0.95, 0)}),
    "neko_L":     dict(view="side", hip=4.3, front="L", feet={"L": (1.55, 0.0), "R": (-0.55, 0)}, tiptoe=True),
    "neko_R":     dict(view="side", hip=4.3, front="R", feet={"R": (1.55, 0.0), "L": (-0.55, 0)}, tiptoe=True),
    "kokutsu_L":  dict(view="side", hip=4.15, front="L", feet={"L": (2.0, 0), "R": (-1.5, 0)}),
    "kokutsu_R":  dict(view="side", hip=4.15, front="R", feet={"R": (2.0, 0), "L": (-1.5, 0)}),
    "shiko_side_L": dict(view="side", hip=3.6, front="L", feet={"L": (2.1, 0), "R": (-2.1, 0)}),
    "shiko_side_R": dict(view="side", hip=3.6, front="R", feet={"R": (2.1, 0), "L": (-2.1, 0)}),
    "sagi_side_L": dict(view="side", hip=5.0, front="L", feet={"R": (0.0, 0)}, lift="L"),
    "sagi_side_R": dict(view="side", hip=5.0, front="R", feet={"L": (0.0, 0)}, lift="R"),
    "kosa_L":     dict(view="side", hip=3.9, front="L", feet={"L": (1.0, 0), "R": (-0.6, 0)}, backheel=True),
    "kosa_R":     dict(view="side", hip=3.9, front="R", feet={"R": (1.0, 0), "L": (-0.6, 0)}, backheel=True),
    "geri_L":     dict(view="side", hip=5.0, front="L", feet={"R": (-0.2, 0)}, kick="L"),
    "geri_R":     dict(view="side", hip=5.0, front="R", feet={"L": (-0.2, 0)}, kick="R"),
    "kansetsu_L": dict(view="side", hip=4.9, front="L", feet={"R": (-0.3, 0)}, stamp="L"),
    "kansetsu_R": dict(view="side", hip=4.9, front="R", feet={"L": (-0.3, 0)}, stamp="R"),
    "hiza_L":     dict(view="side", hip=5.0, front="L", feet={"R": (-0.2, 0)}, knee_strike="L"),
    "hiza_R":     dict(view="side", hip=5.0, front="R", feet={"L": (-0.2, 0)}, knee_strike="R"),
    "musubi_side": dict(view="side", hip=5.1, front="L", feet={"L": (0.15, 0), "R": (-0.05, 0)}),
}

# Arm presets: (elbow, hand, hand-type) relative to the shoulder.
# Side view: +x forward, +y up.  Front view: +x outward from the body for that arm.
ARMS_SIDE = {
    "hip":       ((-0.95, -1.35), (-0.15, -2.15), "fist"),
    "tsuki":     ((1.65, -0.15), (3.25, -0.35), "fist"),
    "jodan_tsuki": ((1.6, 0.35), (3.2, 0.75), "fist"),
    "gedan_tsuki": ((1.3, -1.0), (2.6, -2.0), "fist"),
    "ura_tsuki": ((1.15, -1.25), (2.55, -0.85), "fist"),
    "age_uke":   ((1.05, 1.95), (0.05, 2.65), "fist"),
    "chudan_uke": ((1.05, -1.0), (1.55, 0.55), "fist"),
    "gedan_barai": ((0.95, -1.2), (2.0, -2.55), "fist"),
    "empi":      ((1.6, 0.05), (0.25, -0.1), "fist"),
    "empi_up":   ((0.9, 1.45), (0.15, 0.2), "fist"),
    "uraken":    ((1.05, 0.0), (2.4, 1.0), "fist"),
    "tettsui":   ((1.3, -0.4), (2.6, -0.9), "fist"),
    "tettsui_high": ((0.6, 1.4), (1.2, 2.8), "fist"),
    "kake_uke":  ((1.1, -0.45), (1.75, 1.0), "open"),
    "kamae":     ((1.0, -0.8), (1.95, 0.15), "open"),
    "shotei":    ((1.55, -0.25), (3.05, -0.25), "palm"),
    "shotei_high": ((1.5, 0.3), (2.95, 0.7), "palm"),
    "shotei_low": ((1.2, -1.0), (2.4, -1.85), "palm"),
    "nukite":    ((1.6, -0.2), (3.3, -0.35), "open"),
    "tora_top":  ((1.15, 0.0), (2.2, 0.7), "palm"),
    "tora_low":  ((1.05, -1.1), (2.15, -1.25), "palm"),
    "hiki_uke":  ((0.6, -1.1), (1.25, 0.15), "claw"),
    "kakiwake":  ((0.8, -0.9), (1.1, 0.8), "open"),
    "shuto":     ((1.25, 0.3), (2.6, 0.15), "open"),
    "haito":     ((1.25, -0.25), (2.55, -0.05), "open"),
    "yoi_open":  ((0.25, -1.65), (0.75, -2.75), "open"),
    "yoi_fist":  ((0.15, -1.7), (0.35, -2.9), "fist"),
    "osae":      ((1.0, -1.3), (1.9, -1.75), "palm"),
    "sukui":     ((1.05, -1.5), (2.1, -1.1), "open"),
    "chest_guard": ((0.8, -1.0), (1.2, 0.0), "open"),
    "hiji_ate":  ((1.5, 0.35), (0.35, 0.1), "fist"),
    "hammer_down": ((1.2, -0.9), (2.1, -2.0), "fist"),
    "grab_pull": ((-0.6, -1.3), (0.3, -1.6), "fist"),
    "back_open": ((-1.0, -1.25), (-1.2, -2.5), "open"),
    "uchi_uke_f": ((1.05, -1.0), (1.55, 0.55), "fist"),
    "yoko_empi": ((1.6, 0.05), (0.25, -0.1), "fist"),
    "yoko_shotei": ((1.55, -0.25), (3.05, -0.25), "palm"),
    "cross_high": ((1.1, 0.2), (1.3, 1.6), "open"),
    "cross_low": ((0.6, -1.4), (1.2, -2.5), "open"),
    "kakiwake_low": ((0.8, -1.3), (1.6, -2.5), "open"),
    "prayer": ((0.9, -1.0), (1.0, -0.2), "fist"),
    "side_down": ((0.0, -1.6), (0.1, -3.1), "open"),
    "hiji_up": ((0.9, 1.45), (0.15, 0.2), "fist"),
}
ARMS_FRONT = {
    "hip":       ((1.05, -1.3), (0.75, -2.15), "fist"),
    "tsuki":     ((0.6, -0.55), (0.35, -0.1), "fistbig"),
    "jodan_tsuki": ((0.55, -0.2), (0.3, 0.45), "fistbig"),
    "yoko_tsuki": ((1.7, -0.1), (3.3, -0.15), "fist"),
    "age_uke":   ((1.45, 1.2), (-0.6, 2.15), "fist"),
    "chudan_uke": ((1.05, -1.0), (1.25, 0.45), "fist"),
    "uchi_uke_f": ((1.15, -1.0), (0.95, 0.45), "fist"),
    "gedan_barai": ((1.05, -1.05), (1.9, -2.6), "fist"),
    "gedan_uke_x": ((0.75, -1.25), (-0.2, -2.6), "open"),
    "empi":      ((1.65, -0.1), (0.25, -0.1), "fist"),
    "yoko_empi": ((1.75, 0.0), (0.3, 0.0), "fist"),
    "uraken":    ((1.4, 0.1), (2.7, 1.0), "fist"),
    "tettsui":   ((1.5, 0.3), (2.6, -0.8), "fist"),
    "kake_uke":  ((1.1, -0.9), (1.35, 0.6), "open"),
    "kamae":     ((0.9, -1.0), (0.75, 0.15), "open"),
    "shotei":    ((0.65, -0.6), (0.4, -0.15), "palmbig"),
    "yoko_shotei": ((1.65, -0.1), (3.1, -0.1), "palm"),
    "nukite":    ((0.6, -0.6), (0.4, -0.1), "openbig"),
    "kakiwake":  ((1.0, -1.0), (1.45, 0.5), "open"),
    "kakiwake_low": ((1.0, -1.3), (1.9, -2.3), "open"),
    "cross_high": ((1.2, 0.6), (-0.4, 1.8), "open"),
    "cross_low": ((0.8, -1.2), (-0.35, -2.2), "open"),
    "yoi_open":  ((0.55, -1.55), (-0.15, -2.6), "open"),
    "yoi_fist":  ((0.95, -1.5), (0.95, -2.95), "fist"),
    "side_down": ((0.75, -1.6), (0.85, -3.1), "open"),
    "hiki_uke":  ((1.2, -1.1), (1.0, 0.2), "claw"),
    "tora_top":  ((1.1, -0.2), (0.45, 0.55), "palm"),
    "tora_low":  ((1.0, -1.25), (0.35, -1.5), "palm"),
    "hiji_up":   ((1.5, 1.3), (0.35, 0.5), "fist"),
    "osae":      ((0.95, -1.35), (0.3, -1.9), "palm"),
    "shuto_out": ((1.5, 0.4), (2.8, 0.55), "open"),
    "grab_pull": ((1.4, -1.1), (0.9, -1.75), "fist"),
    "prayer":    ((0.85, -1.0), (0.1, -0.2), "open"),
    "chest_guard": ((0.95, -1.1), (0.2, -0.45), "open"),
    "hiji_up_f": ((1.5, 1.3), (0.35, 0.5), "fist"),
    "sukui":     ((0.9, -1.4), (0.6, -2.4), "open"),
    "hammer_down": ((1.2, -1.0), (1.4, -2.4), "fist"),
    "empi_up":   ((1.4, 1.2), (0.3, 0.4), "fist"),
    "jodan_tsuki_f": ((0.55, -0.2), (0.3, 0.45), "fistbig"),
    "shotei_high": ((0.6, -0.2), (0.35, 0.4), "palmbig"),
    "nukite_f": ((0.6, -0.6), (0.4, -0.1), "openbig"),
    "back_open": ((0.75, -1.6), (0.85, -3.1), "open"),
    "ura_tsuki": ((0.7, -1.1), (0.4, -0.7), "fistbig"),
}


def _ik(hip, ankle, bend):
    """Two-link IK. bend = (bx, by) unit preference for knee side."""
    hx, hy = hip; ax_, ay = ankle
    dx, dy = ax_ - hx, ay - hy
    d = math.hypot(dx, dy)
    L = THIGH + SHIN
    if d >= L * 0.995:
        k = THIGH / L
        return (hx + dx * k, hy + dy * k)
    a = (THIGH ** 2 - SHIN ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(max(THIGH ** 2 - a ** 2, 0))
    mx, my = hx + dx * a / d, hy + dy * a / d
    px, py = -dy / d, dx / d
    c1 = (mx + px * h, my + py * h)
    c2 = (mx - px * h, my - py * h)
    s1 = (c1[0] - mx) * bend[0] + (c1[1] - my) * bend[1]
    s2 = (c2[0] - mx) * bend[0] + (c2[1] - my) * bend[1]
    return c1 if s1 >= s2 else c2


def _seg(ax, pts, lw, fill, z, ol=1.25):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=INK, lw=lw + ol * 2, solid_capstyle="round", solid_joinstyle="round", zorder=z)
    return (xs, ys, lw, fill, z)


def _fill(ax, s):
    xs, ys, lw, fill, z = s
    ax.plot(xs, ys, color=fill, lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=z + 0.5)


def _hand(ax, elbow, hand, kind, fill, z, scale, g=1.0):
    ex, ey = elbow; hx, hy = hand
    ang = math.degrees(math.atan2(hy - ey, hx - ex))
    r = 0.36 * g
    if kind in ("fist",):
        ax.add_patch(Circle(hand, r, fc=fill, ec=INK, lw=1.0 * scale, zorder=z + 1))
    elif kind == "fistbig":
        ax.add_patch(Circle(hand, r * 1.35, fc=fill, ec=INK, lw=1.0 * scale, zorder=z + 1))
        ax.add_patch(Arc(hand, r * 1.6, r * 1.2, angle=0, theta1=200, theta2=340, color=INK, lw=0.6 * scale, zorder=z + 2))
    elif kind in ("open", "openbig"):
        k = 1.25 if kind == "openbig" else 1.0
        ax.add_patch(Ellipse((hx + 0.18 * g * math.cos(math.radians(ang)), hy + 0.18 * g * math.sin(math.radians(ang))),
                             0.95 * k * g, 0.42 * k * g, angle=ang, fc=fill, ec=INK, lw=1.0 * scale, zorder=z + 1))
    elif kind in ("palm", "palmbig"):
        k = 1.3 if kind == "palmbig" else 1.0
        ax.add_patch(Ellipse(hand, 0.5 * k * g, 0.8 * k * g, angle=ang, fc=fill, ec=INK, lw=1.0 * scale, zorder=z + 1))
    elif kind == "claw":
        ax.add_patch(Circle(hand, r * 1.05, fc=fill, ec=INK, lw=1.0 * scale, zorder=z + 1))
        for da in (-35, 0, 35):
            a = math.radians(ang + da)
            ax.plot([hx + r * math.cos(a), hx + (r + 0.28 * g) * math.cos(a)],
                    [hy + r * math.sin(a), hy + (r + 0.28 * g) * math.sin(a)], color=INK, lw=1.0 * scale, zorder=z + 2)


def _foot(ax, ankle, direction, fill, z, scale, tiptoe=False, view="side", toe="fwd", side=1, g=1.0):
    ax_, ay = ankle
    if view == "side":
        d = direction
        if tiptoe:
            pts = [(ax_, ay + 0.45 * g), (ax_ + 0.55 * d * g, ay + 0.05 * g)]
        else:
            pts = [(ax_ - 0.15 * d * g, ay + 0.12 * g), (ax_ + 0.85 * d * g, ay + 0.1 * g)]
        s = _seg(ax, pts, 4.2 * scale, fill, z, ol=1.0 * scale)
        _fill(ax, s)
    else:
        off = {"fwd": 0.0, "out": 0.35, "in": -0.25}[toe] * side
        ax.add_patch(Ellipse((ax_ + off * 0.6 * g, ay + 0.1 * g), (0.95 + abs(off)) * g, 0.42 * g, angle=0,
                             fc=fill, ec=INK, lw=1.0 * scale, zorder=z + 1))


def figure(ax, x0, y0, stance="heiko", L="hip", R="hip", s=1.0, lean=0.0, facing=1, head_turn=0,
           ghost=False, belt=True):
    """Draw a karateka with hips at x0, feet on y0. s = scale (1 unit = s)."""
    st = STANCES[stance]
    view = st["view"]
    ax.apply_aspect()
    bb = ax.get_position(); fw = ax.figure.get_size_inches()[0]
    xl = ax.get_xlim(); ppu = bb.width * fw * 72 / abs(xl[1] - xl[0])
    k = s * ppu / 7.0          # line-width scale so drawings look identical at any size
    s_geom = s
    lwL = 4.6 * k
    lwT = 13.5 * k
    hip_y = st["hip"]
    f = facing
    Tq = lambda p: (x0 + p[0] * s * f, y0 + p[1] * s)
    z0 = 10
    near_fill = WHITE if not ghost else PALE
    far_fill = FAR if not ghost else PALE

    # torso geometry
    hip = (0.0, hip_y)
    neck = (lean * 0.9, hip_y + 3.15)
    head = (neck[0] + 0.12, neck[1] + 1.02)
    if view == "side":
        shoulder = (neck[0] - 0.05, neck[1] - 0.25)
        near, far = "L", "R"  # facing +x shows the performer's left side
        if f < 0:
            near, far = "R", "L"
        legs = {}
        for side, foot in st["feet"].items():
            legs[side] = (foot, _ik(hip, foot, (1, 0.2)))
        if "lift" in st:
            sd = st["lift"]
            legs[sd] = ((0.35, hip_y - 1.9), (1.75, hip_y - 0.6))
            legs[sd] = (legs[sd][0], (1.6, hip_y - 0.35))
        if "kick" in st:
            sd = st["kick"]
            legs[sd] = ((4.6, hip_y + 0.3), (2.35, hip_y + 0.5))
        if "stamp" in st:
            sd = st["stamp"]
            legs[sd] = ((2.9, 1.3), (1.7, hip_y - 0.8))
        if "knee_strike" in st:
            sd = st["knee_strike"]
            legs[sd] = ((1.6, hip_y - 2.1), (2.1, hip_y + 0.35))

        def draw_leg(side, fill, z):
            foot, knee = legs[side]
            hp = hip
            seg = _seg(ax, [Tq(hp), Tq(knee), Tq(foot)], lwL * 1.15, fill, z, ol=1.1 * k)
            return seg, foot, knee

        def draw_arm(side, fill, z):
            preset = L if side == "L" else R
            e, h, kind = ARMS_SIDE[preset]
            sh = shoulder
            ep = (sh[0] + e[0], sh[1] + e[1]); hp = (sh[0] + h[0], sh[1] + h[1])
            seg = _seg(ax, [Tq(sh), Tq(ep), Tq(hp)], lwL, fill, z, ol=1.1 * k)
            return seg, ep, hp, kind

        # far arm, far leg
        for side, fill, zz in ((far, far_fill, z0), (near, near_fill, z0 + 6)):
            if side in legs:
                seg, foot, knee = draw_leg(side, fill, zz)
                _fill(ax, seg)
                kicked = side == st.get("kick") or side == st.get("lift") or side == st.get("knee_strike")
                if kicked:
                    d = 1
                    fx, fy = foot
                    seg2 = _seg(ax, [Tq((fx - 0.1, fy - 0.05)), Tq((fx + 0.55, fy + 0.35))], 4.2 * k, fill, zz, ol=1.0 * k)
                    _fill(ax, seg2)
                else:
                    tip = st.get("tiptoe") and side == st.get("front")
                    _foot(ax, Tq(foot), f, fill, zz, k, tiptoe=tip, g=s)
            seg, ep, hp, kind = draw_arm(side, fill, zz + 1 if side == near else zz)
            _fill(ax, seg)
            _hand(ax, Tq(ep), Tq(hp), kind if not kind.endswith("big") else kind[:-3], fill, zz + 1, k, s)
            if side == far:
                # torso drawn between far and near layers
                tseg = _seg(ax, [Tq(hip), Tq(neck)], lwT, near_fill, z0 + 3, ol=1.1 * k)
                _fill(ax, tseg)
                # gi lapel line
                ax.plot(*zip(Tq((neck[0] + 0.35, neck[1] - 0.15)), Tq((hip[0] + 0.55, hip[1] + 1.1))),
                        color=INK, lw=0.6 * k, zorder=z0 + 4)
                if belt:
                    bx = [Tq((hip[0] - 0.6, hip[1] + 0.45))[0], Tq((hip[0] + 0.65, hip[1] + 0.45))[0]]
                    by = [Tq((0, hip[1] + 0.45))[1]] * 2
                    ax.plot(bx, by, color=INK, lw=4.0 * k, solid_capstyle="butt", zorder=z0 + 4)
                    ax.plot(*zip(Tq((0.55, hip[1] + 0.45)), Tq((0.85, hip[1] - 0.35))), color=INK, lw=1.6 * k, zorder=z0 + 4)
                # head
                ax.add_patch(Circle(Tq(head), 0.78 * s, fc=near_fill, ec=INK, lw=1.2 * k, zorder=z0 + 5))
                hx, hy = Tq(head)
                ax.add_patch(Arc((hx, hy), 1.56 * s, 1.56 * s, angle=0,
                                 theta1=60 if f > 0 else 0, theta2=180 if f > 0 else 120,
                                 color=INK, lw=2.6 * k, zorder=z0 + 5.5))
                ax.add_patch(Circle((hx + 0.42 * s * f, hy + 0.08 * s), 0.07 * s, fc=INK, ec=INK, zorder=z0 + 6))
    else:
        # front view: performer faces the reader. Performer's left = +x.
        sides = {"L": 1, "R": -1}
        legs = {}
        for side, foot in st["feet"].items():
            sg = sides[side]
            hp = (0.5 * sg, hip_y)
            fx, fy = foot
            if st["knee"] == "out":
                bend = (sg, 0.3)
            elif st["knee"] == "in":
                bend = (-sg, 0)
            elif st["knee"] == "kneel":
                bend = (sg * 0.2, -1)
            else:
                bend = (sg * 0.3, 0)
            if st.get("lift") == side:
                knee = (0.9 * sg, hip_y - 0.3)
                legs[side] = (hp, knee, (fx, fy))
            elif st["knee"] == "kneel":
                knee = (0.75 * sg, 0.3)
                legs[side] = (hp, knee, (0.7 * sg, 0.15))
            else:
                legs[side] = (hp, _ik(hp, (fx, fy), bend), (fx, fy))
        segs = []
        for side in ("R", "L"):
            hp, knee, foot = legs[side]
            segs.append(_seg(ax, [Tq(hp), Tq(knee), Tq(foot)], lwL * 1.1, near_fill, z0, ol=1.1 * k))
        for sseg in segs:
            _fill(ax, sseg)
        for side in ("R", "L"):
            hp, knee, foot = legs[side]
            if st.get("lift") == side:
                ax.add_patch(Ellipse(Tq((foot[0], foot[1])), 0.55 * s, 0.7 * s, fc=near_fill, ec=INK, lw=1.0 * k, zorder=z0 + 1))
            elif st["knee"] != "kneel":
                _foot(ax, Tq(foot), 1, near_fill, z0, k, view="front", toe=st["toe"], side=sides[side] * f, g=s)
        # torso: trapezoid gi
        sw = 1.05
        tp = [(-0.75, hip_y + 0.1), (0.75, hip_y + 0.1), (sw, neck[1] - 0.2), (-sw, neck[1] - 0.2)]
        ax.add_patch(Polygon([Tq(p) for p in tp], closed=True, fc=near_fill, ec=INK, lw=1.2 * k, zorder=z0 + 3,
                             joinstyle="round"))
        ax.plot(*zip(Tq((-0.35, neck[1] - 0.2)), Tq((0.25, hip_y + 1.2))), color=INK, lw=0.6 * k, zorder=z0 + 3.2)
        ax.plot(*zip(Tq((0.35, neck[1] - 0.2)), Tq((0.0, hip_y + 1.45))), color=INK, lw=0.6 * k, zorder=z0 + 3.2)
        if belt:
            ax.add_patch(Rectangle(Tq((-0.8, hip_y + 0.12)), 1.6 * s * f, 0.38 * s, fc=INK, ec=INK, zorder=z0 + 3.5))
            ax.plot(*zip(Tq((0.1, hip_y + 0.2)), Tq((0.35, hip_y - 0.75))), color=INK, lw=1.8 * k, zorder=z0 + 3.5)
            ax.plot(*zip(Tq((0.1, hip_y + 0.2)), Tq((-0.2, hip_y - 0.7))), color=INK, lw=1.8 * k, zorder=z0 + 3.5)
        ax.add_patch(Circle(Tq((0, neck[1] + 0.95)), 0.8 * s, fc=near_fill, ec=INK, lw=1.2 * k, zorder=z0 + 4))
        hx, hy = Tq((0, neck[1] + 0.95))
        ax.add_patch(Arc((hx, hy), 1.6 * s, 1.6 * s, theta1=20, theta2=160, color=INK, lw=2.8 * k, zorder=z0 + 4.5))
        for side in ("R", "L"):
            preset = L if side == "L" else R
            e, h, kind = ARMS_FRONT[preset]
            sg = sides[side]
            sh = (0.98 * sg, neck[1] - 0.35)
            ep = (sh[0] + e[0] * sg, sh[1] + e[1]); hp = (sh[0] + h[0] * sg, sh[1] + h[1])
            zz = z0 + 5 if preset in ("tsuki", "jodan_tsuki", "shotei", "nukite", "age_uke", "cross_high", "cross_low",
                                        "yoi_open", "prayer", "tora_top", "tora_low", "osae", "gedan_uke_x",
                                        "chudan_uke", "kake_uke", "kakiwake", "hiki_uke", "kamae", "uchi_uke_f") else z0 + 2
            seg = _seg(ax, [Tq(sh), Tq(ep), Tq(hp)], lwL, near_fill, zz, ol=1.1 * k)
            _fill(ax, seg)
            _hand(ax, Tq(ep), Tq(hp), kind, near_fill, zz, k, s)


def ground(ax, x1, x2, y, lw=0.6):
    ax.plot([x1, x2], [y, y], color=MID, lw=lw, zorder=1)


# ======================================================================
#  FOOTPRINTS / EMBUSEN
# ======================================================================
FOOT = np.array([(0.0, -0.5), (0.18, -0.46), (0.24, -0.2), (0.22, 0.1), (0.28, 0.32), (0.22, 0.5),
                 (0.05, 0.56), (-0.12, 0.5), (-0.2, 0.25), (-0.18, -0.05), (-0.2, -0.3), (-0.14, -0.48)])


def footprint(ax, x, y, ang_deg, side="L", size=1.0, fill=INK, ec=INK, lw=0.7, z=8, ls="-"):
    """ang_deg: direction the toes point, 90 = up the page (north)."""
    pts = FOOT.copy() * size
    if side == "R":
        pts[:, 0] *= -1
    th = math.radians(ang_deg - 90)
    R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    pts = pts @ R.T + np.array([x, y])
    ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=ec, lw=lw, zorder=z, linestyle=ls))


# Stance footprint templates in the performer's frame: x = right, y = forward. Values in foot-lengths.
FOOTPRINTS = {
    "heiko":    {"L": (-0.45, 0, 0), "R": (0.45, 0, 0)},
    "musubi":   {"L": (-0.2, 0, 25), "R": (0.2, 0, -25)},
    "hachiji":  {"L": (-0.45, 0, 25), "R": (0.45, 0, -25)},
    "sanchin_L": {"L": (-0.45, 0.55, -22), "R": (0.45, -0.55, 0)},
    "sanchin_R": {"R": (0.45, 0.55, 22), "L": (-0.45, -0.55, 0)},
    "zenkutsu_L": {"L": (-0.45, 1.25, 0), "R": (0.45, -1.25, -25)},
    "zenkutsu_R": {"R": (0.45, 1.25, 0), "L": (-0.45, -1.25, 25)},
    "neko_L":   {"L": (-0.05, 0.75, 0), "R": (0.25, -0.35, -40)},
    "neko_R":   {"R": (0.05, 0.75, 0), "L": (-0.25, -0.35, 40)},
    "kokutsu_L": {"L": (-0.1, 1.0, 0), "R": (0.25, -0.8, -80)},
    "kokutsu_R": {"R": (0.1, 1.0, 0), "L": (-0.25, -0.8, 80)},
    "shiko":    {"L": (-1.4, 0, 45), "R": (1.4, 0, -45)},
    "sagi_L":   {"R": (0.2, 0, 0)},
    "sagi_R":   {"L": (-0.2, 0, 0)},
    "kosa_L":   {"L": (-0.1, 0.4, 30), "R": (0.25, -0.35, 0)},
    "kosa_R":   {"R": (0.1, 0.4, -30), "L": (-0.25, -0.35, 0)},
}

DIRS = {"N": 90, "NE": 45, "E": 0, "SE": -45, "S": -90, "SW": -135, "W": 180, "NW": 135}


def place_stance(ax, cx, cy, stance, facing, size=1.0, fill=INK, ec=INK, ls="-", z=8, fp=None):
    """Draw a stance's footprints centred at cx, cy facing `facing` (compass or degrees)."""
    ang = DIRS[facing] if isinstance(facing, str) else facing
    tpl = fp or FOOTPRINTS[stance]
    th = math.radians(ang - 90)
    c, s_ = math.cos(th), math.sin(th)
    for side, (px, py, rot) in tpl.items():
        X = cx + (px * c - py * s_) * size
        Y = cy + (px * s_ + py * c) * size
        footprint(ax, X, Y, ang + rot, side=side, size=size, fill=fill, ec=ec, z=z, ls=ls)


def compass(ax, x, y, r=3.0, fs=6):
    ax.add_patch(Circle((x, y), r, fc=WHITE, ec=INK, lw=0.6, zorder=30))
    arrow(ax, x, y - r * 0.55, x, y + r * 0.75, lw=0.8, ms=5, z=31)
    label(ax, x, y + r + 1.6, "N", fs=fs, fontweight="bold", zorder=31)


def direction_icon(ax, x, y, facing, r=2.2):
    ang = math.radians(DIRS[facing])
    ax.add_patch(Circle((x, y), r, fc=WHITE, ec=INK, lw=0.5, zorder=30))
    for a in (0, 90, 180, 270):
        aa = math.radians(a)
        ax.plot([x + r * 0.8 * math.cos(aa), x + r * math.cos(aa)], [y + r * 0.8 * math.sin(aa), y + r * math.sin(aa)],
                color=INK, lw=0.4, zorder=31)
    arrow(ax, x - math.cos(ang) * r * 0.5, y - math.sin(ang) * r * 0.5,
          x + math.cos(ang) * r * 0.85, y + math.sin(ang) * r * 0.85, lw=0.9, ms=4.5, z=32)
