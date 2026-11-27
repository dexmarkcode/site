from body import *
from diag import *

# 4.1 Measuring Sanchin dachi (top view)
FP = [
    dict(feet=[(-15, 0, 0, "r"), (15, 0, 0, "l")], cap="Heiko dachi"),
    dict(feet=[(-17, 0, 0, "r"), (17, 0, 0, "l")], cap="Shoulder width", lines=[((-24, -16), (24, -16))]),
    dict(feet=[(-17, 0, 24, "r", "ghost"), (17, 0, 0, "l")], paths=[((-17, 16), (-6, 26), (-10, 14))], cap="Right foot slides"),
    dict(feet=[(-16, 11, 24, "r"), (16, -10, 0, "l")], cap="Front heel = back toes", lines=[((-30, 4), (30, 4))]),
    dict(feet=[(-16, 11, 24, "r"), (16, -10, -12, "l")], cap="Back toes turn in"),
    dict(feet=[(-16, 11, 24, "r"), (16, -10, -12, "l")], cap="Width check", lines=[((-16, -26), (-16, 30)), ((16, -26), (16, 30))]),
    dict(feet=[(-16, 11, 24, "r", "solid", 50), (16, -10, -12, "l", "solid", 50)], cap="Weight 50/50"),
    dict(feet=[(16, 11, -24, "l"), (-16, -10, 12, "r")], cap="Left Sanchin"),
]
footplate("p4_1", FP, ph=1.45)

# 4.2 Entering Sanchin dachi from yoi
Y = pose("hachiji", "ready")
S = pose("sanchin_r", "kamae")
cross = pose("hachiji", "cross")
st1 = pose(STANCES["sanchin_r"], "cross", pelvis=(0, 96, 0), ra=(-17, 8, 0), rfy=0)
fr = [Y, cross, st1, mix(st1, pose(STANCES["sanchin_r"], "cross"), 0.6), pose(STANCES["sanchin_r"], "cross"),
      mix(pose(STANCES["sanchin_r"], "cross"), S, 0.5), S, S]
cp = ["Yoi", "Arms cross", "Right foot moves", "Crescent in", "Settle", "Arms rise", "Kamae", "Hold, breathe"]
mk = [[]] * 7 + [[("root", "la", "ra"), ("dantien",)]]
plate("p4_2", [dict(pose=f, view=0, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])

# 4.3 Views of Sanchin dachi
SL = pose("sanchin_l", "kamae")
pl = [dict(pose=S, view=0, cap="Front"), dict(pose=S, view=90, cap="Right side"), dict(pose=S, view=-90, cap="Left side"),
      dict(pose=S, view=180, cap="Back"), dict(pose=S, view=35, cap="Three-quarter"), dict(pose=S, view=-35, cap="Other ¾"),
      dict(pose=SL, view=0, cap="Left foot forward"), dict(pose=SL, view=90, cap="Left fwd, side")]
plate("p4_3", pl)

# 4.4 The crescent step from above
FP = [
    dict(feet=[(-16, 11, 24, "r"), (16, -10, -12, "l")], cap="Start: right fwd"),
    dict(feet=[(-16, 11, 24, "r", "heavy"), (16, -10, -12, "l")], cap="Weight settles"),
    dict(feet=[(-16, 11, 24, "r", "heavy"), (16, -10, -12, "l", "ghost"), (4, 4, 0, "l")], paths=[((16, -6), (10, -6), (6, 0))], cap="Foot draws in"),
    dict(feet=[(-16, 11, 24, "r", "heavy"), (4, 6, 0, "l")], cap="Passes close"),
    dict(feet=[(-16, 11, 24, "r", "heavy"), (4, 6, 0, "l", "ghost"), (12, 22, -10, "l")], paths=[((5, 12), (6, 22), (11, 26))], cap="Arcs out"),
    dict(feet=[(-16, 11, 24, "r"), (16, 32, -24, "l")], cap="Lands, toes in", cz=12),
    dict(feet=[(-16, 11, 12, "r"), (16, 32, -24, "l")], cap="Back foot adjusts", cz=12),
    dict(feet=[(-16, 11, 12, "r"), (16, 32, -24, "l")], cap="Left Sanchin", cz=12, paths=[((16, -10), (0, 6), (16, 26))]),
]
footplate("p4_4", FP, ph=1.45)

# helper: crescent step frames for the figure, left foot moving from back to front


def crescent(n=8, start=None):
    start = start or pose("sanchin_r", "kamae")
    path = [(16, -10), (11, -6), (6, 0), (4, 8), (7, 16), (11, 24), (14, 30), (16, 32)]
    lift = [0, 2, 4, 5, 5, 4, 2, 0]
    out = []
    for i in range(n):
        t = i / (n - 1)
        k = int(round(t * (len(path) - 1)))
        x, z = path[k]
        p = dict(start)
        p["la"] = (x, 8 + lift[k], z)
        p["pelvis"] = (0, 91 + (2 if 0 < k < 7 else 0) * 0.5, 21 * t)
        p["lfy"] = -12 + (-24 + 12) * t
        p["rfy"] = 24 - 12 * t
        p["lknee"] = (-0.22 - 0.08 * t, 0, 1)
        out.append(p)
    return out


CR = crescent()
cps = ["Right Sanchin", "Weight steady", "Foot draws in", "Passes the knee", "Arcs outward", "Reaching", "Landing", "Left Sanchin"]
plate("p4_5", [dict(pose=f, view=90, cap=c, cx=10) for f, c in zip(CR, cps)])
plate("p4_6", [dict(pose=f, view=0, cap=c) for f, c in zip(CR, cps)])

# 4.7 The Sanchin turn (top view)
FP = [
    dict(feet=[(-16, 11, 24, "r"), (16, -10, -12, "l")], cap="Left foot behind"),
    dict(feet=[(-16, 11, 24, "r"), (16, -10, -12, "l", "ghost"), (-14, -18, 140, "l")], paths=[((16, -14), (4, -30), (-10, -22))], cap="Left foot crosses"),
    dict(feet=[(-16, 11, 24, "r"), (-14, -18, 160, "l")], cap="Toes point back"),
    dict(feet=[(-16, 11, 200, "r", "ghost"), (-14, -18, 160, "l"), (-16, 11, 192, "r")], cap="Pivot on both"),
    dict(feet=[(-16, 11, 192, "r"), (-14, -18, 160, "l")], cap="Now facing back"),
    dict(feet=[(-16, 11, 192, "r"), (-14, -18, 168, "l")], cap="Adjust width"),
    dict(feet=[(-16, 11, 192, "r", "heavy", 50), (-14, -18, 168, "l", "heavy", 50)], cap="Settle"),
    dict(feet=[(-16, 11, 192, "r"), (-14, -18, 168, "l")], cap="Sanchin, turned", texts=[(0, -32, "now facing this way", 5)]),
]
footplate("p4_7", FP, ph=1.45)

# 4.8 The turn with the figure
T0 = pose("sanchin_r", "kamae")
T1 = pose("sanchin_r", "kamae", la=(-14, 8, -18), lfy=160, hip_yaw=60, chest_yaw=20)
T2 = pose("sanchin_r", "kamae", yaw=180, offset=(-2, 0, -4), la=(14, 8, 18), ra=(-16, 8, -11), lfy=-24, rfy=12, hip_yaw=0)
fr = [T0, mix(T0, T1, 0.5), T1, mix(T1, dict(T1, hip_yaw=120, chest_yaw=40), 0.5), dict(T1, hip_yaw=150, chest_yaw=30),
      mix(dict(T1, hip_yaw=150), T2, 0.5), T2, T2]
cp = ["Ready", "Foot moves", "Foot crosses", "Hips begin", "Hips turn", "Arms follow", "Facing back", "Settled"]
plate("p4_8", [dict(pose=f, view=0, cap=c) for f, c in zip(fr, cp)])

# 4.9 Faults in Sanchin dachi (figure)
F = [(dict(S, la=(16, 8, -26), ra=(-16, 8, 26), pelvis=(0, 88, 0)), 90, "Too long"),
     (dict(S, la=(28, 8, -10), ra=(-28, 8, 11)), 0, "Too wide"),
     (dict(S, la=(6, 8, -10), ra=(-6, 8, 11)), 0, "Too narrow"),
     (dict(S, lfy=25), 0, "Back foot turned out"),
     (dict(S, pelvis=(0, 91, -8)), 90, "Weight back"),
     (dict(S, pelvis=(0, 91, 8), lean=6), 90, "Weight forward"),
     (dict(S, lknee=(1, 0, 0.5), rknee=(-1, 0, 0.5)), 0, "Knees pushed out"),
     (dict(S, pelvis=(0, 98, 0)), 0, "Standing too tall")]
plate("p4_9", [dict(pose=p, view=v, cap=c, marks=[("x", "P")] if c in ("Weight back", "Weight forward") else []) for p, v, c in F])

# 4.10 Faults from above
FP = [
    dict(feet=[(-16, 22, 24, "r"), (16, -20, -12, "l")], cap="Too long"),
    dict(feet=[(-28, 11, 24, "r"), (28, -10, -12, "l")], cap="Too wide", xr=48),
    dict(feet=[(-6, 11, 24, "r"), (6, -10, -12, "l")], cap="Feet in one line"),
    dict(feet=[(-16, 11, 24, "r"), (16, -10, 25, "l")], cap="Back toes out"),
    dict(feet=[(-16, 11, 0, "r"), (16, -10, -12, "l")], cap="Front toes straight"),
    dict(feet=[(-16, 11, 50, "r"), (16, -10, -40, "l")], cap="Toes over-turned"),
    dict(feet=[(-16, 0, 24, "r"), (16, 0, -12, "l")], cap="No front-back gap"),
    dict(feet=[(-16, 11, 24, "r", "ball"), (16, -10, -12, "l", "ball")], cap="Heels lifted"),
]
footplate("p4_10", FP, ph=1.45)

# 4.11 Weight distribution under the foot
FP = [
    dict(feet=[(0, 0, 0, "l", "heavy")], cap="Whole foot (correct)", grid=False, fwd=False, xr=26),
    dict(feet=[(0, 0, 0, "l", "ball")], cap="Balls only", grid=False, fwd=False, xr=26),
    dict(feet=[(0, 0, 0, "l")], cap="Heels only", grid=False, fwd=False, xr=26, texts=[(0, -10, "●", 9)]),
    dict(feet=[(0, 0, 0, "l")], cap="Tripod", grid=False, fwd=False, xr=26, texts=[(0, -9, "●", 7), (-3.5, 9.5, "●", 7), (4, 8, "●", 7)]),
]
footplate("p4_11", FP, ph=1.2)

write_count("ch04")
