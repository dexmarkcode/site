from body import *
from diag import *

S = pose("sanchin_r", "kamae")
H = pose("heiko", "kamae")


def front_push(stance_pose, y=128, z=12, **kw):
    return pose("zenkutsu_l", offset=(0, 0, 70), yaw=180, rh=(0, y, 70 - z), rworld=True, rhand="open", **kw)


# 7.1 Ground force and the line of support
pl = [dict(pose=S, view=90, cap="Floor pushes up", marks=[("arrow2", (0, -14), (0, 30)), ("root", "la", "ra")]),
      dict(pose=S, view=0, cap="Through both legs", marks=[("arrow2", ("la"), ("la")), ("wave", "la", "lk", "P"), ("wave", "ra", "rk", "P")]),
      dict(pose=S, view=90, cap="To the centre", marks=[("wave", "la", "lk", "P"), ("dantien",)]),
      dict(pose=S, view=90, cap="On to the hands", marks=[("wave", "la", "lk", "P", "N", "rw")]),
      dict(figs=[S, front_push(S)], view=90, cap="A push arrives"),
      dict(figs=[S, front_push(S)], view=90, cap="Line to rear foot", marks=[("jline", "chest", "la")]),
      dict(figs=[S, front_push(S)], view=90, cap="Absorbed by floor", marks=[("jline", "chest", "la"), ("root", "la")]),
      dict(figs=[dict(S, lean=-8), front_push(S)], view=90, cap="Fault: lean back", marks=[("x", "P")])]
# 'arrow2' with joint names is not supported; replace panel (b) mark
pl[1]["marks"] = [("wave", "la", "lk", "P"), ("wave", "ra", "rk", "P")]
for d in pl:
    if "figs" in d: d["zoom"] = 1.45
plate("p7_1", pl, pw=1.2)

# 7.2 Sinking
st = pose("heiko", "kamae", pelvis=(0, 98, 0))
lo = pose("heiko", "kamae", pelvis=(0, 88, 0))
fr = seq(st, lo, 6)
cp = ["Standing", "Knees soften", "Hips settle", "Weight drops", "Feet spread", "Rooted"]
mk = [[], [], [], [("dantien",)], [("dantien",)], [("dantien",), ("root", "la", "ra")]]
plate("p7_2", [dict(pose=f, view=90, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)] +
      [dict(pose=lo, view=0, cap="Front: rooted", marks=[("root", "la", "ra")]), dict(pose=st, view=0, cap="Front: perched")])

# 7.3 Weight shifting
L = pose("heiko", "kamae", pelvis=(12, 90, 0), la=(18, 8, 0), ra=(-18, 8, 0))
R = pose("heiko", "kamae", pelvis=(-12, 90, 0), la=(18, 8, 0), ra=(-18, 8, 0))
C = pose("heiko", "kamae", pelvis=(0, 90, 0), la=(18, 8, 0), ra=(-18, 8, 0))
fr = [C, mix(C, L, 0.5), L, mix(L, C, 0.5), C, mix(C, R, 0.5), R, C]
cp = ["Centre 50/50", "Shift left", "Left 90%", "Return", "Centre", "Shift right", "Right 90%", "Centre"]
plate("p7_3", [dict(pose=f, view=0, cap=c, marks=[("plumb", "P")]) for f, c in zip(fr, cp)])

# 7.4 Footprint weight shifts
def ww(a, b):
    sa = "heavy" if a >= 70 else "solid"
    sb = "heavy" if b >= 70 else "solid"
    return [(-18, 0, -4, "r", sb, b), (18, 0, 4, "l", sa, a)]
FP = [dict(feet=ww(50, 50), cap="50 / 50"), dict(feet=ww(70, 30), cap="70 left"), dict(feet=ww(90, 10), cap="90 left"),
      dict(feet=ww(50, 50), cap="Back to centre"), dict(feet=ww(30, 70), cap="70 right"), dict(feet=ww(10, 90), cap="90 right"),
      dict(feet=[(-16, 11, 24, "r", "solid", 50), (16, -10, -12, "l", "solid", 50)], cap="Sanchin 50/50"),
      dict(feet=[(-6, -14, -30, "r", "heavy", 90), (6, 22, 0, "l", "ball", 10)], cap="Neko 90/10")]
footplate("p7_4", FP, ph=1.3)

# 7.5 Standing practice (rooting holds)
hug = pose("heiko", lh=(12, -18, 34), rh=(-12, -18, 34), lhand="open", rhand="open", lroll=-60, rroll=60, pelvis=(0, 90, 0))
low = pose("heiko", lh=(14, -44, 26), rh=(-14, -44, 26), lhand="open", rhand="open", pelvis=(0, 88, 0))
pl = [dict(pose=hug, view=0, cap="Holding the ball"), dict(pose=hug, view=90, cap="Side"),
      dict(pose=low, view=0, cap="Hands low"), dict(pose=low, view=90, cap="Side", marks=[("dantien",)]),
      dict(pose=S, view=0, cap="Sanchin hold"), dict(pose=S, view=90, cap="Side", marks=[("root", "la", "ra")]),
      dict(pose=pose("shiko", "kamae"), view=0, cap="Shiko hold"), dict(pose=pose("shiko", lh=(14, -20, 36), rh=(-14, -20, 36), lhand="open", rhand="open"), view=30, cap="Shiko, open")]
plate("p7_5", pl)

# 7.6 Push tests across stances
stances = [(pose("heiko", "kamae"), "Heiko"), (S, "Sanchin"), (pose("shiko", "kamae"), "Shiko (front)"),
           (pose("zenkutsu_l", "kamae"), "Zenkutsu"), (pose("neko_l", "kamae"), "Neko ashi"),
           (pose("shiko", "kamae", yaw=90), "Shiko (side)"), (pose("musubi", "kamae"), "Musubi"), (pose("kiba", "kamae"), "Kiba")]
pl = []
for p, c in stances:
    y = p["pelvis"][1] + 38
    pl.append(dict(figs=[p, front_push(p, y=y)], view=90, cap=c, zoom=1.45))
plate("p7_6", pl, pw=1.2)

# 7.7 Absorbing and grounding a push
P0 = pose("zenkutsu_l", offset=(0, 0, 80), yaw=180, rh=(-4, -10, 46), rhand="open")
P1 = front_push(S)
fr = [(S, P0), (S, P1), (dict(S, pelvis=(0, 90, -2)), P1), (dict(S, pelvis=(0, 89, -1)), P1), (S, P1), (S, P1), (S, P1), (S, P0)]
cp = ["Push coming", "Contact", "Sink slightly", "Align", "Ground it", "Hold", "Partner tires", "Release"]
mk = [[], [], [("dantien",)], [("jline", "chest", "la")], [("jline", "chest", "la"), ("root", "la")], [("root", "la", "ra")], [], []]
plate("p7_7", [dict(figs=[a, b], view=90, cap=c, marks=m, zoom=1.45) for (a, b), c, m in zip(fr, cp, mk)], pw=1.2)

# 7.8 Single-leg balance
sg = pose("sagi_l", "kamae")
pl = [dict(pose=pose("heiko", "kamae"), view=90, cap="Stand"), dict(pose=mix(pose("heiko", "kamae"), sg, 0.5), view=90, cap="Lift slowly"),
      dict(pose=sg, view=90, cap="Knee high"), dict(pose=sg, view=0, cap="Front"),
      dict(pose=dict(sg, lh=(30, -10, 20), rh=(-30, -10, 20), lhand="open", rhand="open"), view=0, cap="Arms wide"),
      dict(pose=dict(sg, head_pitch=0), view=90, cap="Eyes closed", marks=[("x", (999, 999))]),
      dict(pose=dict(sg, pelvis=(0, 88, 0)), view=90, cap="Sink on one leg", marks=[("root", "ra")]),
      dict(pose=dict(sg, la=(-2, 30, 36), lfp=0), view=90, cap="Slow kick")]
plate("p7_8", pl)

# 7.9 Rooting faults
pl = [dict(pose=dict(S, pelvis=(0, 98, 0)), view=90, cap="Perched high", marks=[("x", "P")]),
      dict(pose=dict(S, lean=12), view=90, cap="Leaning in", marks=[("x", "N")]),
      dict(pose=dict(S, la=(16, 8, -10), lfp=0, ra=(-16, 10, 11), rfp=18), view=90, cap="Toes lifted", marks=[("x", "ra")]),
      dict(pose=dict(S, la=(16, 11, -10), ra=(-16, 11, 11), lfp=-18, rfp=-18), view=90, cap="On the toes", marks=[("x", "la")]),
      dict(pose=dict(S, lknee=(1, 0, .4), rknee=(-1, 0, .4)), view=0, cap="Knees out", marks=[("x", "lk")]),
      dict(pose=dict(S, pelvis=(8, 91, 0)), view=0, cap="Weight to one side", marks=[("plumb", "P")]),
      dict(pose=dict(S, head_pitch=-20, lean=-4), view=90, cap="Chest lifted", marks=[("x", "chest")]),
      dict(pose=dict(S, pelvis=(0, 80, 0)), view=90, cap="Sunk too low", marks=[("x", "rk")])]
plate("p7_9", pl)

# 7.10 Push force over time
fig, ax = chart("p7_10", 4.5, 1.9)
t = np.linspace(0, 6, 600)
push = np.interp(t, [0, 0.5, 3.0, 4.0, 4.6, 6], [0, 0, 1, 1, 0, 0])
lean = np.where(t < 4.0, push, np.interp(t, [4.0, 4.2, 6], [1, 0.0, 0.0]))
root_sway = 0.05 * push
lean_sway = np.where(t < 4.0, 0.08 * push, np.interp(t, [4.0, 4.3, 4.8, 6], [0.08, 0.7, 0.4, 0.4]))
ax.plot(t, push, color=INK, lw=1.2, label="Partner's push")
ax.plot(t, root_sway, color=INK, lw=1.0, ls="--", label="Movement of rooted student")
ax.plot(t, lean_sway, color=INK, lw=0.9, ls=":", label="Movement of leaning student")
ax.annotate("push removed", xy=(4.0, 1.0), xytext=(4.6, 1.15), fontsize=5.6, arrowprops=dict(arrowstyle="-", lw=0.5))
ax.annotate("falls forward", xy=(4.3, 0.7), xytext=(5.0, 0.8), fontsize=5.6, arrowprops=dict(arrowstyle="-", lw=0.5))
ax.set_ylim(0, 1.3); ax.set_xlabel("Seconds", fontsize=6.5); ax.set_yticks([])
ax.legend(fontsize=5.8, frameon=False, loc="upper left")
save_chart(fig, "p7_10", 1)

# 7.11 Feeling the floor (top views)
def dot(x, y, sz=8): return (x, y, "●", sz)
FP = [dict(feet=[(0, 0, 0, "l")], cap="Toes spread", texts=[(0, 18.5, "↔", 11)]),
      dict(feet=[(0, 0, 0, "l")], cap="Heel weighted", texts=[dot(0, -3.5, 11)]),
      dict(feet=[(0, 0, 0, "l")], cap="Ball weighted", texts=[dot(0.5, 10, 11)]),
      dict(feet=[(0, 0, 0, "l")], cap="Outer edge", texts=[dot(3.2, 3, 9)]),
      dict(feet=[(0, 0, 0, "l")], cap="Inner edge (rolled)", texts=[dot(-2.2, 3, 9)]),
      dict(feet=[(0, 0, 0, "l", "heavy")], cap="Even, whole foot"),
      dict(feet=[(0, 0, 0, "l")], cap="Bubbling spring", texts=[dot(0.3, 7.5, 6), (0.3, 7.5, "( )", 11)]),
      dict(feet=[(0, 0, 0, "l")], cap="Circle the weight", paths=[((0, -3), (7, 5), (0, 13)), ((0, 13), (-6, 5), (0, -3))])]
for f in FP:
    f.update(grid=False, fwd=False, xr=15, cz=5)
footplate("p7_11", FP, ph=1.2)

write_count("ch07")
