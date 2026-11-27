"""Posable line-drawing karateka for the Goju-Ryu textbook.

Every figure in the book is drawn by this module: a simple 3D skeleton in a karate gi,
posed by stance and hand targets, projected orthographically from any viewing angle and
rendered as black ink on white paper. No colour is used anywhere.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon, FancyArrowPatch, Ellipse, Circle, Arc

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
for f in (ROOT / "fonts").glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({"font.family": "Source Sans 3", "font.size": 7, "savefig.dpi": 300,
                     "mathtext.fontset": "stix"})

INK = "#000000"
FAR = "#e4e4e4"     # far-side limbs: pale grey wash, still pure greyscale
LW = 0.85

# ------------------------------------------------------------------ linear algebra
def ry(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rx(deg):
    """Positive = lean forward (top of the body moves toward +z)."""
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rz(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else v


def two_bone(a, c, l1, l2, pole):
    d = c - a
    dist = np.linalg.norm(d)
    dn = unit(d)
    dist = min(max(dist, 1e-3), l1 + l2 - 0.01)
    c = a + dn * dist
    x = (l1 * l1 - l2 * l2 + dist * dist) / (2 * dist)
    h = math.sqrt(max(l1 * l1 - x * x, 0))
    p = pole - np.dot(pole, dn) * dn
    if np.linalg.norm(p) < 1e-6:
        p = np.array([0, 0, 1.0]) - np.dot([0, 0, 1.0], dn) * dn
    p = unit(p)
    return a + dn * x + p * h, c


def hull(pts):
    pts = sorted(set(map(tuple, np.round(pts, 3))))
    if len(pts) < 3:
        return np.array(pts)
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return np.array(lo[:-1] + up[:-1])


def capsule2d(p1, p2, r1, r2, n=10):
    d = p2 - p1
    L = np.linalg.norm(d)
    ang = math.atan2(d[1], d[0]) if L > 1e-6 else 0.0
    pts = []
    for t in np.linspace(math.pi / 2, 3 * math.pi / 2, n):
        pts.append(p1 + r1 * np.array([math.cos(ang + t), math.sin(ang + t)]))
    for t in np.linspace(-math.pi / 2, math.pi / 2, n):
        pts.append(p2 + r2 * np.array([math.cos(ang + t), math.sin(ang + t)]))
    return np.array(pts)


# ------------------------------------------------------------------ pose
NEUTRAL = dict(
    pelvis=(0, 99, 0), hip_yaw=0, chest_yaw=0, lean=0, head_yaw=0, head_pitch=0,
    la=(9, 8, 0), ra=(-9, 8, 0), lfy=8, rfy=-8, lfp=0, rfp=0, lflift=0, rflift=0,
    lknee=(0.15, 0, 1), rknee=(-0.15, 0, 1),
    lh=(23, -60, 2), rh=(-23, -60, 2), lel=None, rel=None,
    lhand="fist", rhand="fist", lroll=0, rroll=0, lworld=False, rworld=False,
    offset=(0, 0, 0), yaw=0, props=(), belt="black", bend=0,
)

STANCES = {
    "musubi":  dict(pelvis=(0, 99, 0), la=(5, 8, 0), ra=(-5, 8, 0), lfy=30, rfy=-30),
    "heiko":   dict(pelvis=(0, 98, 0), la=(15, 8, 0), ra=(-15, 8, 0), lfy=-4, rfy=4),
    "hachiji": dict(pelvis=(0, 98, 0), la=(15, 8, 0), ra=(-15, 8, 0), lfy=22, rfy=-22),
    # right foot forward Sanchin: toes in, knees squeezed toward the centre
    "sanchin_r": dict(pelvis=(0, 91, 0), la=(16, 8, -10), ra=(-16, 8, 11), lfy=-12, rfy=24,
                      lknee=(-0.22, 0, 1), rknee=(0.3, 0, 1)),
    "sanchin_l": dict(pelvis=(0, 91, 0), la=(16, 8, 11), ra=(-16, 8, -10), lfy=-24, rfy=12,
                      lknee=(-0.3, 0, 1), rknee=(0.22, 0, 1)),
    "shiko":   dict(pelvis=(0, 74, 0), la=(39, 8, 0), ra=(-39, 8, 0), lfy=45, rfy=-45,
                    lknee=(1, 0, 0.6), rknee=(-1, 0, 0.6)),
    "zenkutsu_l": dict(pelvis=(0, 83, 8), la=(14, 8, 44), ra=(-14, 8, -44), lfy=-5, rfy=-25,
                       lknee=(0.1, 0, 1), rknee=(-0.2, 0, 1)),
    "zenkutsu_r": dict(pelvis=(0, 83, 8), la=(14, 8, -44), ra=(-14, 8, 44), lfy=25, rfy=5,
                       lknee=(0.2, 0, 1), rknee=(-0.1, 0, 1)),
    "neko_l":  dict(pelvis=(0, 84, -10), la=(6, 12, 22), ra=(-6, 8, -14), lfy=0, rfy=-30,
                    lfp=-25, lknee=(0.1, 0, 1), rknee=(-0.4, 0, 1)),
    "neko_r":  dict(pelvis=(0, 84, -10), la=(6, 8, -14), ra=(-6, 12, 22), lfy=30, rfy=0,
                    rfp=-25, lknee=(0.4, 0, 1), rknee=(-0.1, 0, 1)),
    "kiba":    dict(pelvis=(0, 80, 0), la=(36, 8, 0), ra=(-36, 8, 0), lfy=0, rfy=0,
                    lknee=(1, 0, 0.8), rknee=(-1, 0, 0.8)),
    "sagi_l":  dict(pelvis=(0, 96, 0), la=(-2, 50, 12), ra=(-8, 8, 0), lfy=0, rfy=-10, lfp=-30,
                    lknee=(0, 0, 1), rknee=(0, 0, 1)),
}

ARMS = {
    "down":     dict(lh=(23, -60, 2), rh=(-23, -60, 2)),
    "ready":    dict(lh=(9, -58, 16), rh=(-9, -58, 16)),           # fists in front of the belt
    "hikite":   dict(lh=(16, -38, -10), rh=(-16, -38, -10)),
    "kamae":    dict(lh=(20, -5, 28), rh=(-20, -5, 28)),          # Sanchin double guard
    "cross":    dict(lh=(-8, -48, 18), rh=(8, -46, 20)),           # crossed in front of groin
    "prayer":   dict(lh=(2, -22, 22), rh=(-2, -22, 22), lhand="open", rhand="open"),
}

ARM_KEYS = ("lh", "rh", "lhand", "rhand", "lel", "rel", "lroll", "rroll", "lworld", "rworld")


def pose(*parts, **kw):
    """Build a pose from named stance / arm presets plus overrides."""
    p = dict(NEUTRAL)
    for part in parts:
        if isinstance(part, str):
            p.update(STANCES.get(part, {}))
            p.update(ARMS.get(part, {}))
        else:
            p.update(part)
    p.update(kw)
    return p


def mix(a, b, t):
    out = {}
    for k in a:
        va, vb = a[k], b.get(k, a[k])
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)) and not isinstance(va, bool):
            out[k] = va + (vb - va) * t
        elif isinstance(va, tuple) and isinstance(vb, tuple) and len(va) == len(vb) and all(isinstance(x, (int, float)) for x in va + vb):
            out[k] = tuple(x + (y - x) * t for x, y in zip(va, vb))
        else:
            out[k] = va if t < 0.5 else vb
    return out


def seq(a, b, n):
    return [mix(a, b, i / (n - 1)) for i in range(n)]


# ------------------------------------------------------------------ skeleton
L_TH, L_SH, L_UA, L_FA = 45, 44, 30, 26


def skeleton(p):
    G = ry(p["yaw"]); off = np.array(p["offset"], float)
    W = lambda v: G @ np.asarray(v, float) + off
    P = np.array(p["pelvis"], float)
    Rh = ry(p["hip_yaw"])
    def Rt(t):
        return ry(p["hip_yaw"] + t * p["chest_yaw"]) @ rx(p["lean"]) @ rz(t * p.get("bend", 0))
    Rc = Rt(1.0)
    N = P + Rc @ np.array([0, 52, 0])
    J = {"P": P, "N": N}
    J["ls"] = N + Rc @ np.array([19, -4, 0]); J["rs"] = N + Rc @ np.array([-19, -4, 0])
    J["lhip"] = P + Rh @ np.array([9, -3, 0]); J["rhip"] = P + Rh @ np.array([-9, -3, 0])
    hd = Rc @ ry(p["head_yaw"]) @ rx(p["head_pitch"])
    J["head"] = N + Rc @ np.array([0, 7, 1]) + hd @ np.array([0, 12, 0])
    J["face"] = hd @ np.array([0, 0, 1])
    # arms
    for side, sg in (("l", 1), ("r", -1)):
        tgt = np.array(p[side + "h"], float)
        S = J[side + "s"]
        Wt = tgt if p[side + "world"] else N + Rc @ tgt
        pole = p[side + "el"]
        pole = Rc @ np.array([0.55 * sg, -1, -0.25]) if pole is None else Rc @ np.array(pole, float)
        E, Wr = two_bone(S, Wt, L_UA, L_FA, pole)
        J[side + "e"], J[side + "w"] = E, Wr
    # legs
    for side in ("l", "r"):
        A = np.array(p[side + "a"], float)
        H = J[side + "hip"]
        K, A2 = two_bone(H, A, L_TH, L_SH, np.array(p[side + "knee"], float))
        J[side + "k"], J[side + "a"] = K, A2
        f = ry(p[side + "fy"]) @ rx(p[side + "fp"]) @ np.array([0, 0, 1.0])
        J[side + "fdir"] = f
    J["Rc"], J["Rh"], J["Rt"] = Rc, Rh, Rt
    # global transform
    for k in list(J):
        if k in ("Rc", "Rh", "Rt"):
            continue
        if k in ("face", "lfdir", "rfdir"):
            J[k] = G @ J[k]
        else:
            J[k] = W(J[k])
    J["G"], J["off"] = G, off
    return J


# ------------------------------------------------------------------ renderer
class View:
    def __init__(self, yaw=0.0):
        a = math.radians(yaw)
        self.c = np.array([-math.sin(a), 0, math.cos(a)])
        self.r = np.cross(-self.c, [0, 1, 0])

    def xy(self, v):
        v = np.asarray(v, float)
        return np.array([np.dot(v, self.r), v[1]])

    def depth(self, v):
        return float(np.dot(np.asarray(v, float), self.c))


def ring(J, h, w, d, frame_t, n=18, center=None):
    R = J["G"] @ J["Rt"](frame_t)
    base = J["P"] if center is None else center
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        pts.append(base + R @ np.array([w * math.sin(a), h, d * math.cos(a)]))
    return pts


def draw_figure(ax, p, view, prims=None, zbias=0.0, scale=1.0):
    """Queue drawing primitives for one figure; returns projected joint dictionary."""
    J = skeleton(p)
    own = prims is None
    prims = [] if own else prims
    v = view
    cdepth = v.depth(J["P"] + J["G"] @ J["Rt"](1) @ np.array([0, 30, 0]))

    def add(depth, fn):
        prims.append((depth + zbias, len(prims), fn))

    def poly(pts2, fc="white", lw=LW, z=0):
        def fn(ax=ax, pts2=pts2, fc=fc, lw=lw):
            ax.add_patch(Polygon(pts2, closed=True, fc=fc, ec=INK, lw=lw, joinstyle="round"))
        return fn

    def seg(a, b, r1, r2, fc="white"):
        return poly(capsule2d(v.xy(a), v.xy(b), r1, r2), fc=fc)

    def far(side):
        sg = 1 if side == "l" else -1
        sp = J[side + "s"] - J["N"]
        return v.depth(J[side + "s"]) < v.depth(J["N"]) - 2

    # --- torso silhouette (gi jacket)
    Pw = J["P"]
    rings = []
    rings += ring(J, -13, 18.5, 13, 0.0)
    rings += ring(J, 2, 16, 11, 0.0)
    rings += ring(J, 18, 15, 10.5, 0.35)
    rings += ring(J, 36, 17, 12, 0.85)
    rings += ring(J, 47, 20, 9.5, 1.0)
    torso_pts = hull([v.xy(q) for q in rings])

    # --- legs (trousers + bare feet)
    leg_prims = []
    for side in ("l", "r"):
        H, K, A = J[side + "hip"], J[side + "k"], J[side + "a"]
        f = J[side + "fdir"]
        fc = FAR if v.depth(H) < v.depth(Pw) - 3 else "white"
        down = np.array([0, -1.0, 0])
        G = J["G"]
        flat = G @ ry(p[side + "fy"]) @ np.array([1.0, 0, 0])
        heel = A - f * 6 + down * 5
        ball = A + f * 13 + down * 6
        toe = A + f * 18 + down * 6
        fpts = [A + down * 1 + f * 1, A - f * 4 + down * 2]
        for q, w in ((heel, 3.5), (ball, 5), (toe, 3)):
            fpts += [q + flat * w, q - flat * w, q + np.array([0, 2.5, 0]) + flat * w * 0.8,
                     q + np.array([0, 2.5, 0]) - flat * w * 0.8]
        foot = hull([v.xy(q) for q in fpts])
        hem = A + (K - A) * 0.18
        dk = v.depth(K)
        front = dk > cdepth + 22
        th0 = H + (K - H) * (0.42 if front else 0.12)
        dep = (v.depth(H) + dk) / 2
        leg_prims.append((dep, front, [poly(foot, fc=fc), seg(hem, K, 7.2, 8.0, fc), seg(K, th0, 8.0, 10.0, fc)]))

    # --- arms
    arm_prims = []
    for side in ("l", "r"):
        S, E, Wr = J[side + "s"], J[side + "e"], J[side + "w"]
        fc = FAR if far(side) else "white"
        fa = unit(Wr - E)
        cuff = E + (Wr - E) * 0.7
        hand = p[side + "hand"]
        if hand == "open":
            ax2 = unit(np.cross(fa, unit(E - S) + 1e-3)) if np.linalg.norm(np.cross(fa, E - S)) > 1e-3 else np.array([1.0, 0, 0])
            ax2 = rz(0) @ ax2
            if p[side + "roll"]:
                ang = math.radians(p[side + "roll"])
                ax2 = ax2 * math.cos(ang) + np.cross(fa, ax2) * math.sin(ang)
            th = unit(np.cross(fa, ax2))
            hp = []
            for along in (0, 9, 17):
                for wv in (-4.2, 4.2):
                    for tv in (-1.6, 1.6):
                        hp.append(Wr + fa * along + ax2 * wv * (0.75 if along == 17 else 1) + th * tv)
        else:
            tmp = np.array([0, 1.0, 0]) if abs(fa[1]) < 0.9 else np.array([1.0, 0, 0])
            a2 = unit(np.cross(fa, tmp)); a3 = unit(np.cross(fa, a2))
            hp = []
            for along in (-1, 8.5):
                for s2 in (-4.3, 4.3):
                    for s3 in (-3.8, 3.8):
                        hp.append(Wr + fa * along + a2 * s2 + a3 * s3)
        hand2 = hull([v.xy(q) for q in hp])
        dep_hand = v.depth(Wr + fa * 4)
        dep_fore = (v.depth(E) + v.depth(Wr)) / 2
        dep_up = (v.depth(S) + v.depth(E)) / 2
        arm_prims.append((dep_up, [seg(S, E, 7.0, 6.2, fc)]))
        arm_prims.append((dep_fore + 0.3, [seg(E, cuff, 6.2, 5.4, fc), seg(cuff, Wr, 3.6, 3.4, fc)]))
        arm_prims.append((dep_hand + 0.6, [poly(hand2, fc=fc)]))

    # depth composition: far legs, near legs, torso, then arms by depth
    order = []
    for dep, front, fns in leg_prims:
        base = dep + (40 if front else -60)
        for i, fn in enumerate(fns):
            order.append((base + i * 0.01, fn))
    # neck behind head, both after torso
    torso_fn = poly(torso_pts)

    def details(ax=ax):
        # belt band and knot, lapels: draw only points facing the viewer
        R0 = J["G"] @ J["Rt"](0.12)
        Pc = J["P"]
        nrm_front = lambda a: np.dot(R0 @ np.array([math.sin(a) / 15.5, 0, math.cos(a) / 10.5]), v.c) > 0
        for h in (6, 11):
            seg_pts = []
            for i in range(73):
                a = 2 * math.pi * i / 72
                q = Pc + R0 @ np.array([15.6 * math.sin(a), h, 10.6 * math.cos(a)])
                if nrm_front(a):
                    seg_pts.append(v.xy(q))
                else:
                    if len(seg_pts) > 1:
                        arr = np.array(seg_pts); ax.plot(arr[:, 0], arr[:, 1], color=INK, lw=LW * 0.9)
                    seg_pts = []
            if len(seg_pts) > 1:
                arr = np.array(seg_pts); ax.plot(arr[:, 0], arr[:, 1], color=INK, lw=LW * 0.9)
        # fill belt band (black belt) where visible: approximate with thick line between
        fill_pts = []
        for i in range(73):
            a = 2 * math.pi * i / 72
            if nrm_front(a):
                q = Pc + R0 @ np.array([15.6 * math.sin(a), 8.5, 10.6 * math.cos(a)])
                fill_pts.append(v.xy(q))
        if len(fill_pts) > 1 and p["belt"] == "black":
            arr = np.array(fill_pts)
            ax.plot(arr[:, 0], arr[:, 1], color=INK, lw=3.0 * (1.0), solid_capstyle="butt")
        if nrm_front(0):
            knot = Pc + R0 @ np.array([0, 8.5, 11])
            k2 = v.xy(knot)
            ax.add_patch(Ellipse(k2, 4.5, 4.5, fc=INK, ec=INK, lw=0.5))
            for dx in (-2.5, 3.0):
                t1 = v.xy(Pc + R0 @ np.array([dx, 8.5, 11.2]))
                t2 = v.xy(Pc + R0 @ np.array([dx * 1.8, -8, 12.5]))
                ax.plot([t1[0], t2[0]], [t1[1], t2[1]], color=INK, lw=2.2, solid_capstyle="butt")
        # lapel lines
        Rch = J["G"] @ J["Rt"](0.9)
        Rmd = J["G"] @ J["Rt"](0.45)
        def surf(R, h, w, d, a):
            return Pc + R @ np.array([w * math.sin(a), h, d * math.cos(a)]), np.dot(R @ np.array([math.sin(a) / w, 0, math.cos(a) / d]), v.c)
        for sgn in (1, -1):
            pts = [surf(Rch, 50, 9, 7, -0.5 * sgn), surf(Rch, 38, 17, 12, -0.05 * sgn), surf(Rmd, 24, 15, 10.8, 0.22 * sgn), surf(R0, 12.5, 15.6, 10.6, 0.42 * sgn)]
            vis = [q for q, nd in pts if nd > 0.01]
            if len(vis) >= 2:
                arr = np.array([v.xy(q) for q in vis])
                ax.plot(arr[:, 0], arr[:, 1], color=INK, lw=LW * 0.75)
        # jacket hem flap line at the side seams
    order.append((-1e-3 + 0.0, None))  # marker for torso position

    head2 = v.xy(J["head"])
    neck_fn = seg(J["N"], J["N"] + (J["head"] - J["N"]) * 0.55, 5.6, 5.6)

    def head_fn(ax=ax):
        ax.add_patch(Ellipse(head2, 20, 24, angle=0, fc="white", ec=INK, lw=LW))
        # hair line and ear give the head a facing direction
        fdir = J["face"]
        side = np.dot(fdir, v.r)
        toward = np.dot(fdir, v.c)
        # hair: dark cap on back/top of head
        ang0 = 90 + math.degrees(math.atan2(0, 1))
        th = np.linspace(0, 2 * math.pi, 60)
        cap = []
        for t in th:
            x, y = 10 * math.cos(t), 12 * math.sin(t)
            # point direction in view plane
            if y > 3 - 6 * max(0, -toward) - 2 * abs(side) or (x * side < -3 and y > -6):
                cap.append(head2 + np.array([x, y]))
        if len(cap) > 3:
            cap = hull(cap)
            ax.add_patch(Polygon(cap, closed=True, fc=INK, ec=INK, lw=0.4))
        if abs(side) > 0.35 and toward > -0.6:
            ex = head2 + np.array([-3.5 * np.sign(side), -1])
            ax.add_patch(Ellipse(ex, 3.2, 4.8, fc="white", ec=INK, lw=0.6))

    final = []
    for dep, front, fns in leg_prims:
        base = dep + (40 if front else -60)
        for i, fn in enumerate(fns):
            final.append(((0 if front else -2), base + i * 0.01, fn))
    final.append((-1, 0, torso_fn))
    final.append((-1, 0.001, details))
    final.append((-1, 0.002, neck_fn))
    final.append((-1, 0.003, head_fn))
    for dep, fns in arm_prims:
        rel = dep - cdepth
        lay = 1 if rel > -6 else -1.5
        for i, fn in enumerate(fns):
            final.append((lay, rel + i * 0.01, fn))
    # props
    for pr in p["props"]:
        final.append(prop_prims(ax, pr, J, v, cdepth))
    final.sort(key=lambda t: (t[0], t[1]))
    if own:
        for _, _, fn in final:
            fn()
    else:
        for lay, dep, fn in final:
            prims.append((zbias + lay * 1000 + dep, len(prims), fn))
    proj = {k: v.xy(J[k]) for k in J if isinstance(J[k], np.ndarray) and J[k].shape == (3,) and k not in ("face", "lfdir", "rfdir")}
    proj["dantien"] = v.xy(J["P"] + J["G"] @ J["Rt"](0) @ np.array([0, 2, 6]))
    proj["chest"] = v.xy(J["P"] + J["G"] @ J["Rt"](0.8) @ np.array([0, 34, 12]))
    proj["navel"] = v.xy(J["P"] + J["G"] @ J["Rt"](0.2) @ np.array([0, 14, 11]))
    proj["_J"] = J
    return proj


def prop_prims(ax, pr, J, v, cdepth):
    kind = pr[0]
    if kind == "chiishi":
        side = pr[1]; dirv = np.array(pr[2], float); Lr = pr[3] if len(pr) > 3 else 42
        Wr = J[side + "w"]
        fa = unit(J[side + "w"] - J[side + "e"])
        grip = Wr + fa * 4
        d = unit(J["G"] @ dirv)
        end = grip + d * Lr
        def fn(ax=ax):
            a, b = v.xy(grip - d * 6), v.xy(end)
            ax.add_patch(Polygon(capsule2d(a, b, 1.6, 1.6, 6), fc="white", ec=INK, lw=LW))
            # stone block at end
            tmp = np.array([0, 0, 1.0]) if abs(d[2]) < 0.9 else np.array([1.0, 0, 0])
            u1 = unit(np.cross(d, tmp)); u2 = unit(np.cross(d, u1))
            pts = [end + d * s + u1 * a1 + u2 * a2 for s in (-2, 8) for a1 in (-7, 7) for a2 in (-7, 7)]
            ax.add_patch(Polygon(hull([v.xy(q) for q in pts]), fc="#bdbdbd", ec=INK, lw=LW))
        dep = v.depth(end) - cdepth
        return (1 if dep > -6 else -1.5, dep + 1, fn)
    if kind == "jar":
        side = pr[1]
        Wr = J[side + "w"]
        c = v.xy(Wr + np.array([0, -9, 0]))
        def fn(ax=ax, c=c):
            x, y = c
            body = [(x - 4.5, y), (x - 5.5, y - 3), (x - 9, y - 9), (x - 9.5, y - 17), (x - 7, y - 24), (x + 7, y - 24),
                    (x + 9.5, y - 17), (x + 9, y - 9), (x + 5.5, y - 3), (x + 4.5, y)]
            ax.add_patch(Polygon(body, closed=True, fc="#d6d6d6", ec=INK, lw=LW))
            ax.plot([x - 5, x + 5], [y - 0.6, y - 0.6], color=INK, lw=LW)
            ax.plot([x - 8.5, x + 8.5], [y - 10, y - 10], color=INK, lw=0.4)
        dep = v.depth(Wr) - cdepth
        return (1 if dep > -6 else -1.5, dep - 0.2, fn)
    if kind == "makiwara":
        z = pr[1]; x = pr[2] if len(pr) > 2 else 0
        base = J["G"] @ np.array([x, 0, z], float) + J["off"]
        def fn(ax=ax):
            pts = []
            for yy in (0, 118):
                for dx in (-5, 5):
                    for dz in (-2.5, 2.5):
                        pts.append(base + J["G"] @ np.array([dx * (1 if yy == 0 else 0.6), yy, dz * (1 if yy == 0 else 0.5)]))
            ax.add_patch(Polygon(hull([v.xy(q) for q in pts]), fc="white", ec=INK, lw=LW))
            pad = []
            for yy in (96, 114):
                for dx in (-4, 4):
                    for dz in (-3.2, 3.2):
                        pad.append(base + J["G"] @ np.array([dx, yy, dz]))
            ax.add_patch(Polygon(hull([v.xy(q) for q in pad]), fc="#9a9a9a", ec=INK, lw=LW))
            g1, g2 = v.xy(base + J["G"] @ np.array([-18, 0, 0])), v.xy(base + J["G"] @ np.array([18, 0, 0]))
        dep = v.depth(base) - cdepth
        return (1 if dep > 0 else -3, dep, fn)
    if kind == "tan":
        a, b = J["lw"], J["rw"]
        d = unit(a - b)
        def fn(ax=ax):
            p1, p2 = v.xy(b - d * 22), v.xy(a + d * 22)
            ax.add_patch(Polygon(capsule2d(p1, p2, 1.8, 1.8, 6), fc="white", ec=INK, lw=LW))
            for end in (a + d * 16, b - d * 16):
                tmp = np.array([0, 1.0, 0]) if abs(d[1]) < 0.9 else np.array([0, 0, 1.0])
                u1 = unit(np.cross(d, tmp)); u2 = unit(np.cross(d, u1))
                pts = [end + d * s + u1 * a1 + u2 * a2 for s in (-3, 3) for a1 in (-9, 9) for a2 in (-9, 9)]
                ax.add_patch(Polygon(hull([v.xy(q) for q in pts]), fc="#bdbdbd", ec=INK, lw=LW))
        dep = v.depth((a + b) / 2) - cdepth
        return (1 if dep > -6 else -1.5, dep + 2, fn)
    if kind == "kongoken":
        a, b = J["lw"], J["rw"]
        mid = (a + b) / 2
        d = unit(a - b)
        up = np.array([0, 1.0, 0])
        def fn(ax=ax):
            pts_o, pts_i = [], []
            for i in range(40):
                t = 2 * math.pi * i / 40
                q = mid + d * (np.linalg.norm(a - b) / 2 + 4) * math.cos(t) + up * 34 * math.sin(t) + up * 10
                pts_o.append(v.xy(q))
                q2 = mid + d * (np.linalg.norm(a - b) / 2 - 1) * math.cos(t) + up * 29 * math.sin(t) + up * 10
                pts_i.append(v.xy(q2))
            ax.plot(*np.array(pts_o + pts_o[:1]).T, color=INK, lw=LW)
            ax.plot(*np.array(pts_i + pts_i[:1]).T, color=INK, lw=LW)
        dep = v.depth(mid) - cdepth
        return (1, dep + 3, fn)
    if kind == "geta":
        side = pr[1]
        A = J[side + "a"]
        def fn(ax=ax):
            pts = []
            f = J[side + "fdir"]
            fl = np.cross([0, 1.0, 0], f)
            for s in (-8, 20):
                for w in (-6, 6):
                    for h in (-9, -6):
                        pts.append(A + f * s + fl * w + np.array([0, h + 3, 0]))
            ax.add_patch(Polygon(hull([v.xy(q) for q in pts]), fc="#8a8a8a", ec=INK, lw=LW))
        return (-2, v.depth(A) - cdepth + 50, fn)
    raise ValueError(kind)


# ------------------------------------------------------------------ overlays
def arrow(ax, p1, p2, lw=1.0, ms=6, ls="-", style="-|>", rad=0.0, c=INK):
    ax.add_patch(FancyArrowPatch(tuple(p1), tuple(p2), arrowstyle=style, mutation_scale=ms, color=c, lw=lw,
                                 linestyle=ls, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))


def overlay(ax, proj, marks):
    for m in marks:
        kind = m[0]
        if kind == "arrow":          # ("arrow", joint, dx, dy[, rad])
            j, dx, dy = m[1], m[2], m[3]
            p1 = proj[j] if isinstance(j, str) else np.array(j)
            rad = m[4] if len(m) > 4 else 0.0
            arrow(ax, p1 + np.array([0, 0]), p1 + np.array([dx, dy]), rad=rad)
        elif kind == "arrow2":       # ("arrow2", (x1,y1), (x2,y2)[, rad])
            arrow(ax, m[1], m[2], rad=m[3] if len(m) > 3 else 0)
        elif kind == "push":         # opposed tension arrows at a joint: ("push", joint, dx, dy)
            p1 = proj[m[1]]; d = np.array([m[2], m[3]])
            arrow(ax, p1 + d * 1.6, p1 + d * 0.4, lw=1.1)
        elif kind == "root":         # dashed lines into the floor under a foot
            for j in m[1:]:
                a = proj[j]
                for dx in (-6, 0, 6):
                    ax.plot([a[0] + dx, a[0] + dx * 1.6], [-1, -16], color=INK, lw=0.6, ls=(0, (2, 1.6)))
        elif kind == "ground":
            ax.plot([-200, 200], [-1, -1], color=INK, lw=0.6)
        elif kind == "dantien":
            c = proj["dantien"]
            ax.add_patch(Circle(c, 4.2, fc="white", ec=INK, lw=0.9, zorder=50))
            ax.add_patch(Circle(c, 1.4, fc=INK, ec=INK, lw=0.4, zorder=51))
        elif kind == "line":         # plumb or alignment: ("line", (x1,y1), (x2,y2), style)
            ax.plot([m[1][0], m[2][0]], [m[1][1], m[2][1]], color=INK, lw=0.7,
                    ls=m[3] if len(m) > 3 else (0, (3, 2)), zorder=60)
        elif kind == "plumb":        # vertical dotted line through a joint
            a = proj[m[1]]
            ax.plot([a[0], a[0]], [-4, 192], color=INK, lw=0.6, ls=(0, (1, 1.8)), zorder=60)
        elif kind == "jline":        # dotted line between two joints
            a, b = proj[m[1]], proj[m[2]]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=0.7, ls=(0, (2.4, 1.6)), zorder=60)
        elif kind == "ring":         # circle highlight on a joint
            a = proj[m[1]]; r = m[2] if len(m) > 2 else 9
            ax.add_patch(Circle(a, r, fc="none", ec=INK, lw=0.8, ls=(0, (2, 1.5)), zorder=60))
        elif kind == "tension":      # radiating tick marks round a joint
            a = proj[m[1]]
            for t in np.linspace(0, 2 * math.pi, 9)[:-1]:
                d = np.array([math.cos(t), math.sin(t)])
                ax.plot(*np.array([a + d * 9, a + d * 13]).T, color=INK, lw=0.8, zorder=60)
        elif kind == "x":            # mark of a fault
            a = proj[m[1]] if isinstance(m[1], str) else np.array(m[1])
            ax.plot([a[0] - 5, a[0] + 5], [a[1] - 5, a[1] + 5], color=INK, lw=1.3, zorder=61)
            ax.plot([a[0] - 5, a[0] + 5], [a[1] + 5, a[1] - 5], color=INK, lw=1.3, zorder=61)
        elif kind == "breath_in":
            c = proj["navel"]
            arrow(ax, c + np.array([0, 40]), c + np.array([0, 8]), lw=1.0)
        elif kind == "breath_out":
            c = proj["navel"]
            arrow(ax, c + np.array([0, 4]), c + np.array([0, -16]), lw=1.0)
        elif kind == "text":         # ("text", (x,y), "s")
            ax.text(m[1][0], m[1][1], m[2], fontsize=m[3] if len(m) > 3 else 5.6, ha="center", va="center",
                    color=INK, zorder=70)
        elif kind == "wave":         # spiral arrow up the body: ground -> hip -> hand
            pts = [proj[j] for j in m[1:]]
            for a, b in zip(pts[:-1], pts[1:]):
                arrow(ax, a, b, lw=0.8, ls=(0, (3, 1.6)), rad=0.25)


# ------------------------------------------------------------------ plates
def _panel_bounds(proj):
    pts = np.array([v for k, v in proj.items() if not k.startswith("_")])
    return pts[:, 0].min(), pts[:, 0].max()


def render_panel(ax, spec, xr=62):
    view = View(spec.get("view", 0))
    prims = []
    figs = spec["figs"] if "figs" in spec else [spec["pose"]]
    projs = []
    for i, fp in enumerate(figs):
        projs.append(draw_figure(ax, fp, view, prims, zbias=view.depth(fp["offset"]) * 100))
    prims.sort(key=lambda t: (t[0], t[1]))
    for _, _, fn in prims:
        fn()
    lo, hi = zip(*[_panel_bounds(pj) for pj in projs])
    cx = spec.get("cx", (min(lo) + max(hi)) / 2)
    ax.set_xlim(cx - xr, cx + xr)
    ax.set_ylim(spec.get("ylo", -6), spec.get("yhi", 196))
    ax.set_aspect("equal", adjustable="datalim", anchor="S")
    ax.axis("off")
    overlay(ax, projs[0], [("ground",)] + list(spec.get("marks", [])))
    if len(projs) > 1:
        overlay(ax, projs[1], spec.get("marks2", []))


def plate(name, panels, cols=4, pw=1.12, ph=2.0, letters=True, start=0):
    """Render a multi-panel plate. Each panel = dict(pose|figs, view, cap, marks)."""
    n = len(panels)
    rows = math.ceil(n / cols)
    capg = 0.26 if any(p.get("cap") for p in panels) else 0.12
    fig = plt.figure(figsize=(cols * pw, rows * (ph + capg)))
    for i, sp in enumerate(panels):
        r, c = divmod(i, cols)
        x0 = c / cols
        y0 = 1 - (r + 1) / rows
        ax = fig.add_axes([x0 + 0.004, y0 + capg / (rows * (ph + capg)), 1 / cols - 0.008, ph / (rows * (ph + capg))])
        xr = 216 * (pw / ph) / 2 * sp.get("zoom", 1.0)
        if any(m[0] == "root" for m in sp.get("marks", [])):
            sp.setdefault("ylo", -20)
        render_panel(ax, sp, xr=xr)
        lab = ""
        if letters:
            lab = f"({chr(97 + start + i)})"
        cap = sp.get("cap", "")
        fig.text(x0 + 0.5 / cols, y0 + capg / (rows * (ph + capg)) * 0.55,
                 (lab + " " + cap).strip(), ha="center", va="center", fontsize=6.4, color=INK, linespacing=1.1,
                 wrap=True)
    fig.savefig(FIG / f"{name}.png", facecolor="white", dpi=300)
    plt.close(fig)
    COUNT[name] = n
    print("plate", name, n)
    return n


COUNT = {}


def record(name, n):
    COUNT[name] = n


def write_count(chapter):
    import json
    f = ROOT / "build_counts.json"
    data = json.loads(f.read_text()) if f.exists() else {}
    data[chapter] = COUNT.copy()
    f.write_text(json.dumps(data, indent=1))
