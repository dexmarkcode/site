from body import *
from diag import *

N0 = pose("heiko", "down")
# 2.1 Plumb line and faults
pl = [dict(pose=N0, view=90, cap="Plumb line", marks=[("plumb", "la")]),
      dict(pose=N0, view=0, cap="Front: level", marks=[("line", (-30, 97), (30, 97)), ("line", (-30, 148), (30, 148))]),
      dict(pose=N0, view=90, cap="Ear over hip", marks=[("jline", "head", "P"), ("jline", "P", "la")]),
      dict(pose=N0, view=180, cap="Back view", marks=[("plumb", "P")]),
      dict(pose=dict(N0, head_pitch=24), view=90, cap="Head forward", marks=[("plumb", "la"), ("x", "head")]),
      dict(pose=dict(N0, lean=-8, pelvis=(0, 99, 5)), view=90, cap="Sway-back", marks=[("plumb", "la"), ("x", "P")]),
      dict(pose=dict(N0, lean=12, head_pitch=14), view=90, cap="Slumped", marks=[("plumb", "la"), ("x", "N")]),
      dict(pose=dict(N0, lean=-4, head_pitch=-12), view=90, cap="Rigid 'parade'", marks=[("plumb", "la"), ("x", "head")])]
plate("p2_1", pl)

# 2.2 Natural stances
ST = [("musubi", "Musubi dachi"), ("heiko", "Heiko dachi"), ("hachiji", "Hachiji dachi"),
      (dict(pelvis=(0, 98, 0), la=(15, 8, 0), ra=(-15, 8, 0), lfy=-18, rfy=18), "Uchi-hachiji")]
pl = []
for st, cap in ST:
    p = pose(st, "ready") if isinstance(st, str) else pose(st, "ready")
    pl.append(dict(pose=p, view=0, cap=cap))
for st, cap in ST:
    p = pose(st, "ready")
    pl.append(dict(pose=p, view=25, cap=cap + " (¾)"))
plate("p2_2", pl)

# 2.3 Footprints of the main stances
FP = [
    dict(feet=[(-5, 0, -30, "r"), (5, 0, 30, "l")], cap="Musubi"),
    dict(feet=[(-15, 0, 0, "r"), (15, 0, 0, "l")], cap="Heiko"),
    dict(feet=[(-15, 0, -22, "r"), (15, 0, 22, "l")], cap="Hachiji"),
    dict(feet=[(-16, 11, 24, "r"), (16, -10, -12, "l")], cap="Sanchin (right fwd)", lines=[((-30, 4), (30, 4))]),
    dict(feet=[(-36, 0, -45, "r"), (36, 0, 45, "l")], cap="Shiko", xr=55),
    dict(feet=[(-14, -40, -25, "r"), (14, 40, -5, "l")], cap="Zenkutsu (left fwd)", xr=42, cz=0),
    dict(feet=[(-6, -14, -30, "r", "heavy"), (6, 22, 0, "l", "ball")], cap="Neko ashi", xr=42),
    dict(feet=[(4, 0, -30, "r", "heavy"), (-6, -8, 10, "l", "ball")], cap="Kosa dachi"),
]
for f in FP:
    f.setdefault("xr", 46)
footplate("p2_3", FP, ph=1.5)

# 2.4 Shiko dachi
SK = pose("shiko", "kamae")
high = pose("hachiji", "kamae")
wide = pose(STANCES["shiko"], "kamae", pelvis=(0, 95, 0))
pl = [dict(pose=high, cap="Start"), dict(pose=wide, cap="Step wide"), dict(pose=mix(wide, SK, 0.5), cap="Sink"),
      dict(pose=SK, cap="Shiko dachi", marks=[("root", "la", "ra")]), dict(pose=SK, view=90, cap="Side: upright"),
      dict(pose=SK, view=40, cap="Three-quarter"), dict(pose=SK, view=0, cap="Knees over toes", marks=[("jline", "lk", "la"), ("jline", "rk", "ra")]),
      dict(pose=dict(SK, pelvis=(0, 66, 0)), cap="Deep training")]
plate("p2_4", pl)

# 2.5 Zenkutsu dachi
Z = pose("zenkutsu_l", "kamae", hip_yaw=-10)
h = pose("heiko", "kamae")
mid = mix(h, Z, 0.5)
pl = [dict(pose=h, view=90, cap="Heiko"), dict(pose=mid, view=90, cap="Step"), dict(pose=Z, view=90, cap="Zenkutsu"),
      dict(pose=Z, view=90, cap="Back leg firm", marks=[("jline", "rhip", "ra")]),
      dict(pose=Z, view=0, cap="Front"), dict(pose=Z, view=180, cap="Behind"),
      dict(pose=dict(Z, lean=18), view=90, cap="Fault: lean", marks=[("x", "N")]),
      dict(pose=dict(Z, la=(14, 8, 30)), view=90, cap="Fault: too short", marks=[("x", "lk")])]
plate("p2_5", pl)

# 2.6 Neko ashi dachi
NK = pose("neko_l", "kamae")
pl = [dict(pose=pose("heiko", "kamae"), view=90, cap="Natural stance"),
      dict(pose=mix(pose("heiko", "kamae"), NK, 0.4), view=90, cap="Weight back"),
      dict(pose=mix(pose("heiko", "kamae"), NK, 0.75), view=90, cap="Slide front foot"),
      dict(pose=NK, view=90, cap="Neko ashi dachi"),
      dict(pose=NK, view=0, cap="Front view"),
      dict(pose=NK, view=50, cap="Three-quarter"),
      dict(pose=NK, view=90, cap="Weight 90/10", marks=[("plumb", "ra")]),
      dict(pose=dict(NK, la=(6, 8, 22), lfp=0), view=90, cap="Fault: heavy front", marks=[("x", "la")])]
plate("p2_6", pl)

# 2.7 Knee tracking
pl = [dict(pose=SK, cap="Shiko: correct", marks=[("jline", "lk", "la"), ("jline", "rk", "ra")]),
      dict(pose=dict(SK, lknee=(-0.6, 0, 1), rknee=(0.6, 0, 1)), cap="Shiko: knees fall in", marks=[("x", "lk"), ("x", "rk")]),
      dict(pose=pose("sanchin_r", "kamae"), cap="Sanchin: correct"),
      dict(pose=pose("sanchin_r", "kamae", lknee=(1, 0, 0.5), rknee=(-1, 0, 0.5)), cap="Sanchin: knees out", marks=[("x", "lk"), ("x", "rk")]),
      dict(pose=Z, view=0, cap="Zenkutsu: correct", marks=[("jline", "lk", "la")]),
      dict(pose=dict(Z, lknee=(-1, 0, 0.6)), view=0, cap="Zenkutsu: knee in", marks=[("x", "lk")]),
      dict(pose=pose("heiko", "kamae", pelvis=(0, 78, 0), lknee=(0.2, 0, 1), rknee=(-0.2, 0, 1)), cap="Squat: correct"),
      dict(pose=pose("heiko", "kamae", pelvis=(0, 78, 0), lknee=(-0.8, 0, 1), rknee=(0.8, 0, 1)), cap="Squat: valgus", marks=[("x", "lk")])]
plate("p2_7", pl)

# 2.8 Junbi undo warm-up
D = pose("heiko", "down")
pl = [dict(pose=dict(D, head_yaw=-55), cap="Neck turn"),
      dict(pose=dict(D, head_pitch=30), view=90, cap="Neck bow"),
      dict(pose=dict(D, lh=(10, 52, 6), rh=(-10, 52, 6)), view=90, cap="Arm swing up"),
      dict(pose=dict(D, lh=(40, -4, 0), rh=(-40, -4, 0), lhand="open", rhand="open"), cap="Arms wide"),
      dict(pose=dict(D, hip_yaw=-15, chest_yaw=-45, lh=(-10, -20, 30), rh=(-40, -20, -10)), cap="Trunk twist"),
      dict(pose=dict(D, lean=55, lh=(6, -60, 30), rh=(-6, -60, 30), lhand="open", rhand="open"), view=90, cap="Forward fold"),
      dict(pose=pose("heiko", "down", pelvis=(0, 66, -14), lean=25, lh=(8, -30, 50), rh=(-8, -30, 50)), view=90, cap="Squat"),
      dict(pose=pose("heiko", pelvis=(0, 86, 0), lh=(14, -50, 26), rh=(-14, -50, 26), lhand="open", rhand="open", lean=22), view=40, cap="Knee circles"),
      dict(pose=pose("sagi_l", "down", la=(4, 40, 50), lfp=0), view=90, cap="Leg swing"),
      dict(pose=pose(STANCES["shiko"], "down", pelvis=(0, 74, 0), lean=10, lh=(18, -66, 30), rh=(-18, -66, 30), lhand="open", rhand="open"), cap="Hip opener"),
      dict(pose=pose("zenkutsu_l", "down", pelvis=(0, 70, 14), lh=(14, -70, 20), rh=(-14, -70, 10), lhand="open", rhand="open"), view=90, cap="Lunge stretch"),
      dict(pose=dict(D, pelvis=(0, 99, 0), la=(9, 14, 0), lfp=40), view=90, cap="Ankle rolls")]
plate("p2_8", pl)

# 2.9 Wall test
W = pose("heiko", "down")
pl = [dict(pose=W, view=90, cap="Heels 5 cm away", marks=[("line", (-20, -3), (-20, 192), "-")], cx=0),
      dict(pose=W, view=90, cap="Touch points", marks=[("line", (-20, -3), (-20, 192), "-"), ("ring", "P", 8), ("ring", "N", 8), ("ring", "head", 13)]),
      dict(pose=dict(W, pelvis=(0, 88, 0)), view=90, cap="Soften knees", marks=[("line", (-20, -3), (-20, 192), "-")]),
      dict(pose=dict(W, pelvis=(0, 88, 0)), view=90, cap="Step away, keep it", marks=[("plumb", "la")])]
plate("p2_9", pl, cols=4)

# 2.10 Turning from shiko to zenkutsu
A = pose("shiko", "kamae")
B = pose(STANCES["zenkutsu_l"], "kamae", la=(40, 8, 30), ra=(-38, 8, -30), lfy=50, rfy=-10, hip_yaw=50, pelvis=(0, 82, 0))
frames = seq(A, B, 6)
caps = ["Shiko", "Weight shifts", "Rear foot pivots", "Hips turn", "Front knee bends", "Zenkutsu"]
plate("p2_10", [dict(pose=f, view=0, cap=c) for f, c in zip(frames, caps)] +
      [dict(pose=A, view=90, cap="Shiko (side)"), dict(pose=B, view=90, cap="Zenkutsu (side)")])

write_count("ch02")
