"""Line-drawing engine for Goju-Ryu Karate Kyohan, Volume Two.

Draws a karateka in a gi as clean black outlines on white, in front view or
side view, from named stance and arm presets (or explicit joint targets).
Every figure plate is a strip of numbered panels; each panel is one drawing.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle, FancyArrowPatch, Ellipse
from shapely.geometry import Point, LineString, MultiPolygon, Polygon
from shapely.ops import unary_union

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)
LW = 0.85
COUNT = {"drawings": 0}

# ---------------------------------------------------------------- body sizes
HEAD_R = 0.062
NECK = 0.035
TORSO = 0.29        # shoulder line to hip line
SH_W = 0.115        # half shoulder width (front)
HIP_W = 0.075       # half hip width (front)
UA, FA = 0.165, 0.150
TH, SN = 0.235, 0.235
R_UA, R_FA = 0.032, 0.026
R_TH, R_SN = 0.046, 0.036


def capsule(a, b, ra, rb):
    """Tapered capsule from point a (radius ra) to point b (radius rb)."""
    return unary_union([Point(a).buffer(ra, 24), Point(b).buffer(rb, 24)]).convex_hull


def ik(root, target, l1, l2, bend):
    """Planar two-bone IK. bend=+1 / -1 chooses the side of the middle joint."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    d = math.hypot(dx, dy)
    d = max(min(d, l1 + l2 - 1e-6), abs(l1 - l2) + 1e-6)
    a = math.atan2(dy, dx)
    cos_ = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    b = math.acos(max(-1, min(1, cos_)))
    ang = a + bend * b
    mid = (root[0] + l1 * math.cos(ang), root[1] + l1 * math.sin(ang))
    end = (mid[0] + l2 * math.cos(a - bend * 0) * 0 + (target[0] - mid[0]), 0)  # placeholder
    # end point: along direction mid->target at length l2
    ex, ey = target[0] - mid[0], target[1] - mid[1]
    e = math.hypot(ex, ey) or 1
    end = (mid[0] + l2 * ex / e, mid[1] + l2 * ey / e)
    return mid, end


def add(p, q, s=1.0):
    return (p[0] + q[0] * s, p[1] + q[1] * s)


# ---------------------------------------------------------------- hand shapes
def hand_shape(pos, direction, kind, scale=1.0):
    """Return a shapely polygon for a hand at pos, pointing along direction (radians)."""
    x, y = pos
    c, s = math.cos(direction), math.sin(direction)
    def T(px, py):
        return (x + (px * c - py * s) * scale, y + (px * s + py * c) * scale)
    if kind == "fist":
        pts = [T(-0.012, -0.026), T(0.030, -0.026), T(0.040, -0.014), T(0.040, 0.016), T(0.028, 0.027), T(-0.012, 0.027)]
        return Polygon(pts).buffer(0.006, 8)
    if kind in ("open", "nukite", "shuto"):
        pts = [T(-0.010, -0.022), T(0.050, -0.016), T(0.075, -0.008), T(0.078, 0.004), T(0.050, 0.014), T(-0.010, 0.022)]
        poly = Polygon(pts).buffer(0.004, 6)
        thumb = capsule(T(0.004, 0.018), T(0.030, 0.034), 0.008, 0.006)
        return unary_union([poly, thumb]) if kind == "open" else poly
    if kind == "palm":   # shotei / teisho: wrist bent back, fingers up
        pts = [T(-0.012, -0.024), T(0.022, -0.026), T(0.030, -0.010), T(0.040, 0.040), T(0.020, 0.052), T(0.004, 0.030), T(-0.012, 0.024)]
        return Polygon(pts).buffer(0.004, 6)
    if kind == "claw":   # tora guchi / kumade fingers curled
        pts = [T(-0.012, -0.025), T(0.040, -0.028), T(0.055, -0.010), T(0.040, 0.006), T(0.052, 0.020), T(0.030, 0.030), T(-0.012, 0.025)]
        return Polygon(pts).buffer(0.004, 6)
    if kind == "hook":   # kake / koken: wrist bent forward
        pts = [T(-0.012, -0.022), T(0.026, -0.024), T(0.034, -0.050), T(0.050, -0.048), T(0.044, 0.012), T(0.020, 0.024), T(-0.012, 0.022)]
        return Polygon(pts).buffer(0.004, 6)
    return Point(pos).buffer(0.024 * scale)


# ---------------------------------------------------------------- stances
# Each stance gives, for front view and side view, the hip-centre height and
# foot positions.  Side view: x is forward (figure faces +x).
STANCES = {
    #            hip_h  front feet (L,R)        side feet (back, front)   knee_bend side
    "musubi":   (0.47, (-0.035, 0.035),       (-0.005, 0.005)),
    "heiko":    (0.47, (-0.080, 0.080),       (-0.005, 0.005)),
    "sanchin":  (0.445, (-0.085, 0.085),      (-0.080, 0.100)),
    "seisan":   (0.44, (-0.095, 0.095),       (-0.150, 0.150)),
    "zenkutsu": (0.405, (-0.090, 0.090),      (-0.300, 0.150)),
    "shiko":    (0.355, (-0.235, 0.235),      (-0.030, 0.030)),
    "neko":     (0.40, (-0.060, 0.070),       (-0.040, 0.150)),
    "kosa":     (0.40, (-0.040, 0.050),       (-0.090, 0.060)),
    "sagi":     (0.45, (-0.050, 0.020),       (-0.010, 0.020)),
    "moto":     (0.43, (-0.085, 0.085),       (-0.200, 0.140)),
    "kokutsu":  (0.40, (-0.070, 0.090),       (-0.200, 0.120)),
}


# ---------------------------------------------------------------- arm presets
# Front view presets: (elbow, hand) offsets from the RIGHT shoulder, x positive
# = outward to the figure's right (viewer's left is flipped in drawing).
# Values in body units.  Mirrored automatically for the left arm.
FRONT_ARMS = {
    "hikite":      ((0.040, -0.150), (0.000, -0.255), "fist", -90),
    "hip":         ((0.040, -0.150), (0.000, -0.255), "fist", -90),
    "sanchin":     ((0.030, -0.175), (-0.025, -0.035), "fist", 100),
    "chudan_tsuki": ((-0.030, -0.090), (-0.115, -0.060), "fist", 200),
    "jodan_tsuki": ((-0.040, -0.050), (-0.110, 0.030), "fist", 160),
    "gedan_tsuki": ((-0.020, -0.130), (-0.090, -0.210), "fist", 230),
    "age_uke":     ((0.080, 0.100), (-0.085, 0.205), "fist", 160),
    "chudan_uke":  ((0.060, -0.165), (0.005, -0.010), "fist", 100),
    "uchi_uke":    ((0.020, -0.150), (-0.060, -0.020), "fist", 110),
    "gedan_barai": ((0.050, -0.150), (0.150, -0.300), "fist", -60),
    "gedan_open":  ((0.050, -0.150), (0.150, -0.300), "open", -60),
    "kake_uke":    ((0.040, -0.150), (0.020, -0.010), "open", 95),
    "shuto_uke":   ((0.050, -0.140), (0.020, 0.000), "shuto", 95),
    "nukite":      ((-0.030, -0.100), (-0.110, -0.070), "nukite", 200),
    "nukite_up":   ((-0.020, -0.130), (-0.060, -0.030), "nukite", 100),
    "shotei":      ((-0.020, -0.110), (-0.090, -0.060), "palm", 100),
    "shotei_high": ((-0.010, -0.060), (-0.080, 0.020), "palm", 100),
    "shotei_low":  ((0.010, -0.140), (-0.050, -0.230), "palm", -80),
    "tora_up":     ((0.030, -0.120), (-0.030, 0.010), "claw", 95),
    "tora_down":   ((0.030, -0.150), (-0.030, -0.170), "claw", -95),
    "empi":        ((-0.120, -0.020), (-0.010, -0.010), "fist", 0),
    "uraken":      ((0.060, -0.040), (0.020, 0.100), "fist", 90),
    "kentsui":     ((0.060, -0.020), (0.000, -0.140), "fist", -90),
    "cross_low":   ((-0.010, -0.150), (-0.140, -0.240), "fist", 200),
    "cross_high":  ((0.010, -0.030), (-0.120, 0.120), "open", 150),
    "yoi_open":    ((0.000, -0.150), (-0.100, -0.260), "open", 200),
    "chamber_side": ((0.090, -0.060), (-0.050, -0.080), "fist", 180),
    "hira_side":   ((0.170, -0.020), (0.320, 0.000), "fist", 0),
    "open_side":   ((0.160, -0.060), (0.290, -0.120), "open", -20),
    "koken":       ((0.040, -0.140), (0.000, 0.000), "hook", 90),
    "down":        ((0.020, -0.165), (0.025, -0.310), "open", -90),
    "tensho_up":   ((0.030, -0.140), (-0.040, -0.020), "palm", 90),
    "tensho_down": ((0.030, -0.150), (-0.040, -0.190), "open", -90),
    "tensho_out":  ((0.040, -0.140), (0.060, -0.040), "palm", 70),
}

# Side view presets: (hand target relative to shoulder, bend sign, hand kind, hand angle)
# Figure faces +x. bend: -1 elbow below the line (natural), +1 above.
SIDE_ARMS = {
    "hikite":       ((-0.040, -0.250), +1, "fist", -90),
    "hip":          ((-0.040, -0.250), +1, "fist", -90),
    "chudan_tsuki": ((0.310, -0.060), -1, "fist", 0),
    "jodan_tsuki":  ((0.300, 0.040), -1, "fist", 5),
    "gedan_tsuki":  ((0.260, -0.200), -1, "fist", -30),
    "sanchin":      ((0.150, -0.020), -1, "fist", 90),
    "chudan_uke":   ((0.150, 0.000), -1, "fist", 90),
    "kake_uke":     ((0.170, 0.000), -1, "open", 90),
    "age_uke":      ((0.110, 0.150), -1, "fist", 120),
    "gedan_barai":  ((0.220, -0.250), -1, "fist", -60),
    "gedan_open":   ((0.220, -0.250), -1, "open", -60),
    "nukite":       ((0.315, -0.070), -1, "nukite", 0),
    "nukite_low":   ((0.270, -0.200), -1, "nukite", -30),
    "shotei":       ((0.290, -0.040), -1, "palm", 90),
    "shotei_low":   ((0.250, -0.210), -1, "palm", -80),
    "tora_up":      ((0.200, -0.010), -1, "claw", 80),
    "tora_down":    ((0.200, -0.170), -1, "claw", -80),
    "empi":         ((0.080, -0.100), +1, "fist", 180),
    "empi_rear":    ((-0.150, -0.130), +1, "fist", 0),
    "uraken":       ((0.270, 0.050), -1, "fist", 70),
    "kentsui":      ((0.250, -0.120), -1, "fist", -60),
    "chamber":      ((0.020, -0.030), -1, "fist", 180),
    "guard":        ((0.180, -0.060), -1, "open", 80),
    "grab_pull":    ((0.050, -0.170), +1, "fist", -10),
    "down":         ((0.010, -0.300), +1, "open", -90),
    "koken":        ((0.170, 0.000), -1, "hook", 80),
    "tensho_up":    ((0.170, -0.040), -1, "palm", 90),
    "tensho_down":  ((0.180, -0.180), -1, "open", -40),
}


class Figure:
    """A single karateka.  view='front' or 'side'.  facing=+1 (right) or -1."""

    def __init__(self, stance="heiko", view="front", left="hip", right="hip",
                 facing=1, x=0.0, kick=None, lean=0.0, label=None, front_leg="L",
                 head_turn=0, drop=0.0, partner=False, knee=0.0, back=False):
        self.stance, self.view, self.left, self.right = stance, view, left, right
        self.facing, self.x, self.kick, self.lean = facing, x, kick, lean
        self.front_leg, self.head_turn, self.drop = front_leg, head_turn, drop
        self.belt = "white" if partner else "black"
        self.knee_adj = knee
        self.back = back

    # ---------------------------------------------------------- geometry
    def joints(self):
        hip_h, ffeet, sfeet = STANCES[self.stance] if isinstance(self.stance, str) else self.stance
        hip_h -= self.drop
        J = {}
        if self.view == "front":
            hc = (self.x, hip_h)
            J["hipL"], J["hipR"] = (self.x + HIP_W, hip_h), (self.x - HIP_W, hip_h)  # figure's left is viewer's right
            sh_y = hip_h + TORSO
            J["shL"], J["shR"] = (self.x + SH_W + self.lean, sh_y), (self.x - SH_W + self.lean, sh_y)
            J["neck"] = (self.x + self.lean, sh_y + NECK * 0.6)
            J["head"] = (self.x + self.lean, sh_y + NECK + HEAD_R)
            fl, fr = ffeet
            J["footL"], J["footR"] = (self.x - fl, 0.03), (self.x - fr, 0.03)
            for side in "LR":
                hip, foot = J["hip" + side], J["foot" + side]
                out = (1 if side == "L" else -1)
                spread = abs(foot[0] - hip[0])
                bend = {"shiko": 0.07, "sanchin": -0.025, "seisan": -0.02, "neko": -0.01}.get(self.stance, 0.0)
                J["knee" + side] = ((hip[0] + foot[0]) / 2 + out * bend + out * spread * 0.05 + out * self.knee_adj, (hip[1] + foot[1]) / 2 + 0.01)
            if self.kick:
                self._front_kick(J)
            # arms
            for side, preset in (("L", self.left), ("R", self.right)):
                sh = J["sh" + side]
                sgn = -1 if side == "R" else 1   # mirror: right arm is on viewer's left
                if isinstance(preset, tuple):
                    el, hd, kind, ang = preset
                else:
                    el, hd, kind, ang = FRONT_ARMS[preset]
                # presets are written for the right arm with +x outward; outward for the
                # right arm in screen space is -x.
                J["elbow" + side] = (sh[0] - sgn * -el[0] * -1 if False else sh[0] + (-sgn) * -el[0], sh[1] + el[1])
                J["elbow" + side] = (sh[0] + sgn * el[0], sh[1] + el[1])
                J["hand" + side] = (sh[0] + sgn * hd[0], sh[1] + hd[1])
                a = math.radians(ang)
                J["hang" + side] = math.atan2(math.sin(a), sgn * math.cos(a))
                J["hkind" + side] = kind
        else:
            f = self.facing
            back, front = sfeet
            hip = (self.x + f * (back + front) / 2 * 0.25 + f * self.lean * 0.3, hip_h)
            if self.stance in ("neko", "kokutsu"):
                hip = (self.x + f * (back + 0.03), hip_h)
            if self.stance == "zenkutsu":
                hip = (self.x + f * (front - 0.17), hip_h)
            J["hip"] = hip
            sh = (hip[0] + f * self.lean, hip[1] + TORSO)
            J["sh"] = sh
            J["neck"] = (sh[0] + f * 0.008, sh[1] + NECK * 0.6)
            J["head"] = (sh[0] + f * 0.012, sh[1] + NECK + HEAD_R)
            J["footB"] = (self.x + f * back, 0.03)
            J["footF"] = (self.x + f * front, 0.03)
            # knees forward (towards facing)
            for k in "BF":
                bend = f
                knee, foot = ik(hip, J["foot" + k], TH, SN, bend)
                J["knee" + k], J["foot" + k] = knee, foot
            if self.kick:
                self._side_kick(J)
            for side, preset in (("F", self.right), ("B", self.left)):
                if isinstance(preset, tuple) and len(preset) == 4 and isinstance(preset[0], tuple):
                    tgt, bend, kind, ang = preset
                else:
                    tgt, bend, kind, ang = SIDE_ARMS[preset]
                shp = (sh[0] + (0.0 if side == "F" else -f * 0.012), sh[1] + (0 if side == "F" else 0.004))
                target = (shp[0] + f * tgt[0], shp[1] + tgt[1])
                elbow, hand = ik(shp, target, UA, FA, bend * f)
                J["sh" + side] = shp
                J["elbow" + side], J["hand" + side] = elbow, hand
                a = math.radians(ang)
                J["hang" + side] = math.atan2(math.sin(a), f * math.cos(a))
                J["hkind" + side] = kind
        return J

    def _front_kick(self, J):
        k = self.kick
        leg = "R" if self.front_leg == "R" else "L"
        hip = J["hip" + leg]
        if k == "knee":
            J["knee" + leg] = (hip[0] + (0.01 if leg == "L" else -0.01), hip[1] + 0.03)
            J["foot" + leg] = (hip[0] + (0.035 if leg == "L" else -0.035), hip[1] - 0.2)
        elif k == "mae":
            J["knee" + leg] = (hip[0], hip[1] + 0.05)
            J["foot" + leg] = (hip[0], hip[1] + 0.02)
        other = "L" if leg == "R" else "R"
        J["foot" + other] = (J["foot" + other][0] * 0.4 + self.x * 0.6, 0.03)
        oh = J["hip" + other]
        J["knee" + other] = ((oh[0] + J["foot" + other][0]) / 2, (oh[1] + 0.03) / 2 + 0.01)

    def _side_kick(self, J):
        f, hip, k = self.facing, J["hip"], self.kick
        if k == "knee":
            J["kneeF"] = (hip[0] + f * 0.20, hip[1] + 0.09)
            J["footF"] = (hip[0] + f * 0.10, hip[1] - 0.10)
        elif k == "mae":
            J["kneeF"] = (hip[0] + f * 0.20, hip[1] + 0.06)
            J["footF"] = (hip[0] + f * 0.42, hip[1] + 0.04)
        elif k == "kansetsu":
            J["kneeF"] = (hip[0] + f * 0.18, hip[1] - 0.06)
            J["footF"] = (hip[0] + f * 0.38, 0.14)
        elif k == "chamber":
            J["kneeF"] = (hip[0] + f * 0.20, hip[1] + 0.07)
            J["footF"] = (hip[0] + f * 0.05, hip[1] - 0.14)
        elif k == "stamp":
            J["kneeF"] = (hip[0] + f * 0.16, hip[1] - 0.10)
            J["footF"] = (hip[0] + f * 0.20, 0.03)
        # support leg under the hip
        J["footB"] = (hip[0] - f * 0.03, 0.03)
        J["kneeB"], J["footB"] = ik(hip, J["footB"], TH, SN, f)

    # ---------------------------------------------------------- drawing
    def draw(self, ax):
        J = self.joints()
        layers = []
        if self.view == "front":
            legs = [capsule(J["hip" + s], J["knee" + s], R_TH, R_TH * 0.92).union(
                    capsule(J["knee" + s], J["foot" + s], R_TH * 0.92, R_SN)) for s in "LR"]
            feet = [self._foot_front(J["foot" + s], s) for s in "LR"]
            torso = Polygon([add(J["shL"], (0.012, 0.0)), add(J["shR"], (-0.012, 0.0)),
                             add(J["hipR"], (-0.022, -0.04)), add(J["hipL"], (0.022, -0.04))]).buffer(0.012, 8)
            pelvis = Polygon([add(J["hipR"], (-0.045, 0.03)), add(J["hipL"], (0.045, 0.03)),
                              add(J["hipL"], (0.04, -0.07)), add(J["hipR"], (-0.04, -0.07))]).buffer(0.008)
            layers += [("w", f) for f in feet] + [("w", l) for l in legs] + [("w", pelvis), ("w", torso)]
            self._render(ax, layers)
            self._gi_front(ax, J)
            self._head(ax, J["head"], front=True)
            for s in "LR":
                upper, lower = self._arm(J, s, split=True)
                self._render(ax, [("w", upper), ("w", lower)], z=5)
        else:
            f = self.facing
            legB = capsule(J["hip"], J["kneeB"], R_TH, R_TH * 0.9).union(capsule(J["kneeB"], J["footB"], R_TH * 0.9, R_SN))
            legF = capsule(J["hip"], J["kneeF"], R_TH, R_TH * 0.9).union(capsule(J["kneeF"], J["footF"], R_TH * 0.9, R_SN))
            footB, footF = self._foot_side(J["footB"], f, J["kneeB"]), self._foot_side(J["footF"], f, J["kneeF"], kick=self.kick)
            hip, sh = J["hip"], J["sh"]
            torso = Polygon([add(sh, (-f * 0.055, 0.01)), add(sh, (f * 0.06, 0.005)),
                             add(hip, (f * 0.07, 0.0)), add(hip, (-f * 0.065, -0.02))]).buffer(0.014, 8)
            armB, armF = self._arm(J, "B"), self._arm(J, "F")
            layers = [("w", armB), ("w", footB), ("w", legB), ("w", torso), ("w", footF), ("w", legF), ("w", armF)]
            self._render(ax, layers)
            self._gi_side(ax, J, f)
            self._head(ax, J["head"], front=False, f=f)
        return J

    def _arm(self, J, s, split=False):
        sh, el, hd = J["sh" + s], J["elbow" + s], J["hand" + s]
        upper = capsule(sh, el, R_UA, R_UA * 0.88)
        sleeve = capsule(el, add(el, ((hd[0]-el[0]) * 0.72, (hd[1]-el[1]) * 0.72)), R_UA * 0.85, R_FA)
        fore = capsule(el, hd, R_FA * 0.9, R_FA * 0.75)
        hand = hand_shape(hd, J["hang" + s], J["hkind" + s])
        lower = unary_union([sleeve, fore, hand])
        if split:
            return upper, lower
        return unary_union([upper, lower])

    def _foot_front(self, p, s):
        dx = 0.022 if s == "L" else -0.022
        if self.stance == "shiko":
            dx *= 1.8
        if self.stance in ("sanchin", "seisan") and s == "L":
            dx = 0.004
        if self.stance in ("sanchin", "seisan") and s == "R":
            dx = -0.004
        return Polygon([(p[0] - 0.03, p[1] - 0.03), (p[0] + 0.03, p[1] - 0.03), (p[0] + 0.03 + dx, p[1] - 0.008),
                        (p[0] - 0.02 + dx, p[1] + 0.01)]).buffer(0.008)

    def _foot_side(self, p, f, knee, kick=None):
        heel = (p[0] - f * 0.03, p[1] - 0.025)
        toe = (p[0] + f * 0.085, p[1] - 0.028)
        if kick in ("mae", "kansetsu") :
            toe = (p[0] + f * 0.03, p[1] + 0.07) if kick == "mae" else (p[0] + f * 0.02, p[1] - 0.08)
            heel = (p[0] + f * 0.02, p[1] - 0.025)
        return unary_union([capsule(heel, toe, 0.022, 0.014), Point(p).buffer(0.028)])

    def _render(self, ax, layers, z=2):
        for _, geom in layers:
            geoms = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
            for g in geoms:
                ax.add_patch(MPoly(list(g.exterior.coords), closed=True, fc="white", ec="black", lw=LW, joinstyle="round", zorder=z))
                for interior in g.interiors:
                    ax.add_patch(MPoly(list(interior.coords), closed=True, fc="white", ec="black", lw=LW, zorder=z))

    def _head(self, ax, c, front=True, f=1):
        ax.add_patch(Ellipse(c, HEAD_R * 1.75, HEAD_R * 2.1, fc="white", ec="black", lw=LW, zorder=3))
        # hair line
        if front and self.back:
            th = [math.radians(a) for a in range(200, -21, -10)]
            ax.add_patch(MPoly([(c[0] + HEAD_R * 0.86 * math.cos(t), c[1] + HEAD_R * 1.04 * math.sin(t)) for t in th], closed=True, fc="black", ec="black", lw=0.5, zorder=4))
        elif front:
            ax.plot([c[0] - HEAD_R * 0.8, c[0] - HEAD_R * 0.3, c[0] + HEAD_R * 0.3, c[0] + HEAD_R * 0.8],
                    [c[1] + HEAD_R * 0.45, c[1] + HEAD_R * 0.7, c[1] + HEAD_R * 0.7, c[1] + HEAD_R * 0.45], c="black", lw=LW * 0.8, zorder=4)
        else:
            ax.plot([c[0] + f * HEAD_R * 0.55, c[0] - f * 0.1 * HEAD_R, c[0] - f * HEAD_R * 0.85],
                    [c[1] + HEAD_R * 0.65, c[1] + HEAD_R * 0.78, c[1] + HEAD_R * 0.1], c="black", lw=LW * 0.8, zorder=4)
            ax.plot([c[0] + f * HEAD_R * 0.86, c[0] + f * HEAD_R * 0.98, c[0] + f * HEAD_R * 0.84],
                    [c[1] + 0.004, c[1] - 0.012, c[1] - 0.02], c="black", lw=LW * 0.7, zorder=4)

    def _gi_front(self, ax, J):
        nk = J["neck"]
        hipy = J["hipL"][1]
        if self.back:
            bx0, bx1 = J["hipR"][0] - 0.03, J["hipL"][0] + 0.03
            by = hipy + 0.015
            ax.add_patch(MPoly([(bx0, by), (bx1, by), (bx1, by - 0.022), (bx0, by - 0.022)], fc=self.belt, ec="black", lw=LW * 0.9, zorder=3))
            ax.plot([nk[0], nk[0]], [nk[1] - 0.04, hipy + 0.03], c="black", lw=LW * 0.4, zorder=3)
            return
        # lapels
        ax.plot([nk[0] - 0.035, nk[0] + 0.012, nk[0] + 0.03], [nk[1] - 0.005, hipy + 0.02, hipy + 0.02], c="black", lw=LW * 0.8, zorder=3)
        ax.plot([nk[0] + 0.035, nk[0] + 0.004], [nk[1] - 0.005, hipy + 0.11], c="black", lw=LW * 0.8, zorder=3)
        # belt
        bx0, bx1 = J["hipR"][0] - 0.03, J["hipL"][0] + 0.03
        by = hipy + 0.015
        ax.add_patch(MPoly([(bx0, by), (bx1, by), (bx1, by - 0.022), (bx0, by - 0.022)], fc=self.belt, ec="black", lw=LW * 0.9, zorder=3))
        kx = self.x + self.lean * 0.4 + 0.01
        ax.add_patch(MPoly([(kx - 0.012, by - 0.004), (kx + 0.012, by - 0.004), (kx + 0.01, by - 0.022), (kx - 0.01, by - 0.022)], fc=self.belt, ec="black", lw=LW * 0.8, zorder=4))
        ax.add_patch(MPoly([(kx - 0.006, by - 0.02), (kx - 0.03, by - 0.085), (kx - 0.018, by - 0.088), (kx + 0.002, by - 0.024)], fc=self.belt, ec="black", lw=LW * 0.8, zorder=4))
        ax.add_patch(MPoly([(kx + 0.004, by - 0.02), (kx + 0.03, by - 0.08), (kx + 0.042, by - 0.075), (kx + 0.012, by - 0.02)], fc=self.belt, ec="black", lw=LW * 0.8, zorder=4))
        # trouser crease
        for s in "LR":
            k = J["knee" + s]
            ax.plot([k[0] - 0.01, k[0] + 0.01], [k[1] + 0.012, k[1] - 0.004], c="black", lw=LW * 0.5, zorder=3)

    def _gi_side(self, ax, J, f):
        nk, hip = J["neck"], J["hip"]
        ax.plot([nk[0] + f * 0.01, hip[0] + f * 0.055], [nk[1] - 0.01, hip[1] + 0.05], c="black", lw=LW * 0.8, zorder=3)
        by = hip[1] + 0.02
        ax.add_patch(MPoly([(hip[0] - f * 0.075, by), (hip[0] + f * 0.08, by), (hip[0] + f * 0.08, by - 0.022), (hip[0] - f * 0.078, by - 0.022)],
                           fc=self.belt, ec="black", lw=LW * 0.9, zorder=3))
        kx = hip[0] + f * 0.075
        ax.add_patch(MPoly([(kx, by - 0.02), (kx + f * 0.02, by - 0.08), (kx + f * 0.032, by - 0.075), (kx + f * 0.008, by - 0.02)], fc=self.belt, ec="black", lw=LW * 0.8, zorder=4))


# ---------------------------------------------------------------- annotation
def arrow(ax, a, b, curve=0.0, lw=0.9, style="-|>", ls="-"):
    p = FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={curve}", arrowstyle=style, mutation_scale=5,
                        lw=lw, color="black", zorder=6, linestyle=ls)
    ax.add_patch(p)


def label(ax, xy, text, size=6.2, ha="center", va="center", **kw):
    ax.text(xy[0], xy[1], text, fontsize=size, ha=ha, va=va, family="DejaVu Sans", zorder=7, **kw)


def floor(ax, x0, x1, y=0.0):
    ax.plot([x0, x1], [y, y], c="black", lw=0.6, zorder=1)


# ---------------------------------------------------------------- plates
def plate(name, panels, cols=None, caption_labels=None, panel_w=1.0, height=1.05, width_in=4.6,
          numbered=True, row_h_in=None, pad=0.06):
    """Render a strip/grid of panels.  Each panel is a function f(ax) that draws
    into body-unit coordinates centred on x=0, floor at y=0."""
    n = len(panels)
    cols = cols or min(n, 4)
    rows = math.ceil(n / cols)
    pw_in = width_in / cols
    ph_in = row_h_in or pw_in * height / panel_w
    fig = plt.figure(figsize=(width_in, ph_in * rows))
    for i, fn in enumerate(panels):
        r, c = divmod(i, cols)
        ax = fig.add_axes([c / cols, 1 - (r + 1) / rows, 1 / cols, 1 / rows])
        ax.set_xlim(-panel_w / 2, panel_w / 2)
        ax.set_ylim(-0.08, height - 0.08)
        ax.set_aspect("equal", adjustable="datalim")
        ax.axis("off")
        fn(ax)
        COUNT["drawings"] += 1
        if numbered:
            ax.text(-panel_w / 2 + 0.03, height - 0.13, str(i + 1), fontsize=7, family="DejaVu Sans",
                    weight="bold", ha="left", va="top")
        if caption_labels and i < len(caption_labels) and caption_labels[i]:
            ax.text(0, -0.065, caption_labels[i], fontsize=5.6, family="DejaVu Sans", ha="center", va="center", style="italic")
    fig.savefig(OUT / f"{name}.png", dpi=300, facecolor="white")
    plt.close(fig)


def P(*figs, ground=True, extra=None, xlim=None):
    """Panel helper: draw one or more Figure objects plus optional extra(ax)."""
    def fn(ax):
        for fg in figs:
            fg.draw(ax)
        if ground:
            x0, x1 = ax.get_xlim()
            floor(ax, x0 + 0.02, x1 - 0.02)
        if extra:
            extra(ax)
    return fn


def F(stance="heiko", left="hip", right="hip", **kw):
    return Figure(stance=stance, view="front", left=left, right=right, **kw)


def S(stance="sanchin", left="hip", right="chudan_tsuki", **kw):
    return Figure(stance=stance, view="side", left=left, right=right, **kw)


# ---------------------------------------------------------------- diagrams
def footprint(ax, x, y, ang, side="L", s=1.0, filled=False, ls="-"):
    """Top-view footprint centred on (x,y), toes pointing at ang degrees."""
    a = math.radians(ang)
    c, sn = math.cos(a), math.sin(a)
    mir = 1 if side == "L" else -1
    pts = []
    base = [(-0.5, 0.0), (-0.42, 0.18), (-0.1, 0.24), (0.25, 0.26), (0.47, 0.18), (0.55, 0.0),
            (0.47, -0.17), (0.2, -0.2), (-0.1, -0.16), (-0.42, -0.15)]
    for px, py in base:
        py *= mir
        pts.append((x + (px * c - py * sn) * s, y + (px * sn + py * c) * s))
    ax.add_patch(MPoly(pts, closed=True, fc="black" if filled else "white", ec="black", lw=0.9, ls=ls, zorder=3,
                       joinstyle="round"))
    # big toe
    tx, ty = 0.62, 0.15 * mir
    ax.add_patch(Circle((x + (tx * c - ty * sn) * s, y + (tx * sn + ty * c) * s), 0.07 * s,
                        fc="black" if filled else "white", ec="black", lw=0.8, zorder=3))


def diagram(name, draw_fn, w_in=4.6, h_in=2.6, xlim=(-1, 1), ylim=(-0.6, 0.6)):
    fig = plt.figure(figsize=(w_in, h_in))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")
    n = draw_fn(ax) or 1
    COUNT["drawings"] += n
    fig.savefig(OUT / f"{name}.png", dpi=300, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- helpers for sequences
def lerp_arm(a, b, t):
    """Interpolate two front-view arm specs (preset name or tuple)."""
    A = FRONT_ARMS[a] if isinstance(a, str) else a
    B = FRONT_ARMS[b] if isinstance(b, str) else b
    el = (A[0][0] + (B[0][0] - A[0][0]) * t, A[0][1] + (B[0][1] - A[0][1]) * t)
    hd = (A[1][0] + (B[1][0] - A[1][0]) * t, A[1][1] + (B[1][1] - A[1][1]) * t)
    kind = A[2] if t < 0.5 else B[2]
    return (el, hd, kind, A[3] + (B[3] - A[3]) * t)


def lerp_side(a, b, t):
    A = SIDE_ARMS[a] if isinstance(a, str) else a
    B = SIDE_ARMS[b] if isinstance(b, str) else b
    tg = (A[0][0] + (B[0][0] - A[0][0]) * t, A[0][1] + (B[0][1] - A[0][1]) * t)
    return (tg, A[1] if t < 0.5 else B[1], A[2] if t < 0.5 else B[2], A[3] + (B[3] - A[3]) * t)


def embusen(ax, pts, cx=0, cy=0, s=1.0, start=True, arrows=True, ls="-", lw=0.9):
    """Draw a floor path through pts (list of (x,y)), with a start circle and arrowheads."""
    P_ = [(cx + x * s, cy + y * s) for x, y in pts]
    for i in range(len(P_) - 1):
        if arrows:
            arrow(ax, P_[i], P_[i + 1], lw=lw, ls=ls)
        else:
            ax.plot([P_[i][0], P_[i + 1][0]], [P_[i][1], P_[i + 1][1]], c="black", lw=lw, ls=ls)
    if start:
        ax.add_patch(Circle(P_[0], 0.028 * max(s, 0.6), fc="white", ec="black", lw=0.9, zorder=8))


def panel_embusen(pts, title=None, s=0.9):
    def fn(ax):
        embusen(ax, pts, cx=0, cy=0.07, s=s)
        if title:
            label(ax, (0, -0.02), title, size=6.5)
    return fn


def mawashi_frames(n=8):
    """Front-view keyframes of mawashi uke for the right (upper) and left (lower) hands."""
    R = [((0.03, -0.15), (-0.02, -0.03), "open", 100),   # right hand up in front
         ((0.07, -0.10), (0.06, 0.05), "open", 80),
         ((0.10, -0.08), (0.12, -0.03), "open", 10),
         ((0.07, -0.15), (0.10, -0.18), "open", -60),
         ((0.03, -0.17), (0.00, -0.22), "open", -100),
         ((0.03, -0.16), (-0.03, -0.16), "hook", -90),
         ((0.04, -0.15), (-0.01, -0.21), "claw", -95),
         ((0.03, -0.14), (-0.04, -0.20), "claw", -95)]
    L = [((0.03, -0.16), (-0.04, -0.20), "open", -100),
         ((0.05, -0.17), (0.02, -0.25), "open", -80),
         ((0.08, -0.15), (0.10, -0.18), "open", -40),
         ((0.09, -0.10), (0.11, 0.00), "open", 40),
         ((0.05, -0.12), (0.03, 0.02), "open", 90),
         ((0.04, -0.13), (-0.01, 0.00), "hook", 90),
         ((0.03, -0.12), (-0.02, 0.00), "claw", 95),
         ((0.03, -0.11), (-0.03, 0.02), "claw", 95)]
    return R[:n], L[:n]


def D(stance="sanchin", left="hip", right="chudan_tsuki", x=-0.24, **kw):
    """Defender in side view, facing right, on the left of the panel."""
    return Figure(stance=stance, view="side", left=left, right=right, x=x, facing=1, **kw)


def A(stance="sanchin", left="hip", right="chudan_tsuki", x=0.28, **kw):
    """Partner (attacker) in side view, facing left, on the right of the panel; white belt."""
    return Figure(stance=stance, view="side", left=left, right=right, x=x, facing=-1, partner=True, **kw)


def feet_panel(feet, title=None, s=0.2, lines=None, arrows_=None, k=1.3, cy=0.32):
    """feet: list of (x, y, ang, side, style) where style in 'solid','ghost','filled'."""
    def fn(ax):
        for x, y, ang, side, *st in feet:
            style = st[0] if st else "solid"
            footprint(ax, x * k, y * k + cy, ang, side, s=s, filled=(style == "filled"), ls=(0, (3, 2)) if style == "ghost" else "-")
        for a, b in (lines or []):
            ax.plot([a[0] * k, b[0] * k], [a[1] * k + cy, b[1] * k + cy], c="black", lw=0.5, ls=(0, (2, 2)))
        for a, b, *c in (arrows_ or []):
            arrow(ax, (a[0] * k, a[1] * k + cy), (b[0] * k, b[1] * k + cy), curve=c[0] if c else 0.0, lw=0.8)
        if title:
            label(ax, (0, -0.03), title, size=6.3)
    return fn


def marked(fig, marks, ground=True):
    """marks: list of (joint_key, (dx,dy) offset of arrow tail from joint, (dx,dy) of head offset)."""
    def fn(ax):
        J = fig.draw(ax)
        if ground:
            x0, x1 = ax.get_xlim()
            floor(ax, x0 + 0.02, x1 - 0.02)
        for key, t, h in marks:
            p = J[key]
            arrow(ax, (p[0] + t[0], p[1] + t[1]), (p[0] + h[0], p[1] + h[1]), lw=1.0)
    return fn


def hand_panel(kind, ang, fore_ang=None, title=None, s=3.4):
    """A large close-up drawing of one hand with forearm."""
    def fn(ax):
        fa = math.radians(fore_ang if fore_ang is not None else ang)
        a = math.radians(ang)
        wrist = (0.06 - 0.10 * math.cos(fa), 0.30 - 0.06 * math.sin(fa))
        elbow = (wrist[0] - 0.26 * math.cos(fa), wrist[1] - 0.26 * math.sin(fa))
        sleeve_end = (wrist[0] - 0.12 * math.cos(fa), wrist[1] - 0.12 * math.sin(fa))
        fore = capsule(elbow, wrist, 0.05, 0.042)
        sleeve = capsule((elbow[0] - 0.02 * math.cos(fa), elbow[1] - 0.02 * math.sin(fa)), sleeve_end, 0.072, 0.066)
        hand = hand_shape(wrist, a, kind, scale=s)
        for g in (fore, hand, sleeve):
            geoms = g.geoms if isinstance(g, MultiPolygon) else [g]
            for gg in geoms:
                ax.add_patch(MPoly(list(gg.exterior.coords), closed=True, fc="white", ec="black", lw=1.0, zorder=3))
        c_, s_ = math.cos(a), math.sin(a)
        def T(px, py):
            return (wrist[0] + (px * c_ - py * s_) * s, wrist[1] + (px * s_ + py * c_) * s)
        if kind == "fist":
            for t in (-0.012, 0.001, 0.014):
                p1, p2 = T(0.026, t), T(0.044, t)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c="black", lw=0.7, zorder=4)
        if kind in ("open", "nukite", "shuto"):
            for t in (-0.008, 0.0, 0.008):
                p1, p2 = T(0.045, t), T(0.072, t * 0.6)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c="black", lw=0.6, zorder=4)
        if kind == "palm":
            for t in (0.012, 0.022, 0.032):
                p1, p2 = T(0.008 + t * 0.4, t), T(0.03 + t * 0.2, t + 0.012)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c="black", lw=0.6, zorder=4)
        if title:
            label(ax, (0, -0.03), title, size=6.3)
    return fn


# ---------------------------------------------------------------- implements
def _poly(ax, pts, fc="white", lw=0.9, z=6):
    ax.add_patch(MPoly(pts, closed=True, fc=fc, ec="black", lw=lw, zorder=z, joinstyle="round"))


def chi_ishi(ax, hand, ang, L=0.22, z=6):
    a = math.radians(ang)
    end = (hand[0] + L * math.cos(a), hand[1] + L * math.sin(a))
    g = capsule((hand[0] - 0.03 * math.cos(a), hand[1] - 0.03 * math.sin(a)), end, 0.008, 0.008)
    _poly(ax, list(g.exterior.coords), z=z - 1)
    w = Point(end).buffer(0.045, 16)
    cyl = capsule((end[0] - 0.02 * math.cos(a), end[1] - 0.02 * math.sin(a)), (end[0] + 0.035 * math.cos(a), end[1] + 0.035 * math.sin(a)), 0.045, 0.045)
    _poly(ax, list(cyl.exterior.coords), z=z)


def jar(ax, hand, z=6, s=1.0):
    x, y = hand
    pts = [(x - 0.02, y), (x + 0.02, y), (x + 0.025, y - 0.02), (x + 0.055, y - 0.06), (x + 0.06, y - 0.13),
           (x + 0.045, y - 0.17), (x - 0.045, y - 0.17), (x - 0.06, y - 0.13), (x - 0.055, y - 0.06), (x - 0.025, y - 0.02)]
    pts = [(x + (px - x) * s, y + (py - y) * s) for px, py in pts]
    _poly(ax, pts, z=z)
    ax.plot([x - 0.028 * s, x + 0.028 * s], [y - 0.012 * s, y - 0.012 * s], c="black", lw=0.6, zorder=z + 1)


def ishi_sashi(ax, hand, z=6, s=1.0, ang=0):
    x, y = hand
    g = Polygon([(x - 0.045, y - 0.03), (x + 0.045, y - 0.03), (x + 0.05, y - 0.11), (x - 0.05, y - 0.11)]).buffer(0.01)
    from shapely import affinity
    g = affinity.rotate(g, ang, origin=(x, y))
    g = affinity.scale(g, s, s, origin=(x, y))
    _poly(ax, list(g.exterior.coords), z=z)
    ring = affinity.rotate(Point(x, y - 0.01).buffer(0.028).difference(Point(x, y - 0.01).buffer(0.016)), ang, origin=(x, y))
    for gg in (ring.geoms if hasattr(ring, "geoms") else [ring]):
        _poly(ax, list(gg.exterior.coords), z=z)
        for i_ in gg.interiors:
            _poly(ax, list(i_.coords), z=z + 0.1)


def kongoken(ax, c, w=0.36, h=0.2, z=6, ang=0):
    from matplotlib.patches import Ellipse as E
    ax.add_patch(E(c, w, h, angle=ang, fc="none", ec="black", lw=2.6, zorder=z))
    ax.add_patch(E(c, w, h, angle=ang, fc="none", ec="white", lw=1.2, zorder=z + 0.1))


def makiwara(ax, x, top=0.62, flex=0.0):
    _poly(ax, [(x - 0.035, 0.0), (x + 0.035, 0.0), (x + 0.012 + flex, top), (x - 0.012 + flex, top)], z=1)
    _poly(ax, [(x - 0.03 + flex * 0.85, top - 0.17), (x + 0.026 + flex * 0.85, top - 0.17), (x + 0.024 + flex, top - 0.02), (x - 0.028 + flex, top - 0.02)], z=1.5)
    for k in range(1, 6):
        yy = top - 0.17 + k * 0.025
        ax.plot([x - 0.028 + flex * 0.9, x + 0.025 + flex * 0.9], [yy, yy], c="black", lw=0.5, zorder=1.6)
    ax.plot([x - 0.12, x + 0.12], [0, 0], c="black", lw=0.8)


def with_tools(fig, tools):
    """tools: list of callables f(ax, J)."""
    def fn(ax):
        J = fig.draw(ax)
        x0, x1 = ax.get_xlim()
        floor(ax, x0 + 0.02, x1 - 0.02)
        for t in tools:
            t(ax, J)
    return fn
