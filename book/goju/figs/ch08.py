from body import *
from diag import *
from matplotlib.patches import Ellipse as _E

# 8.1 The kinetic chain in a reverse punch (zenkutsu)
A = pose("zenkutsu_l", lh=(18, -6, 34), rh=(-16, -38, -10), hip_yaw=10, chest_yaw=10)
B = pose("zenkutsu_l", lh=(18, -20, 20), rh=(-12, -32, 6), hip_yaw=-10, chest_yaw=5)
C = pose("zenkutsu_l", lh=(16, -38, -8), rh=(-6, -22, 34), hip_yaw=-25, chest_yaw=-5)
D = pose("zenkutsu_l", lh=(16, -38, -10), rh=(2, -16, 56), hip_yaw=-30, chest_yaw=-10)
fr = [A, mix(A, B, 0.5), B, mix(B, C, 0.5), C, D, D, mix(D, A, 0.5)]
cp = ["Set", "Rear foot drives", "Knee and hip", "Hip turns", "Chest follows", "Arm extends", "Impact: lock", "Recover"]
mk = [[], [("wave", "ra", "rk")], [("wave", "ra", "rk", "rhip")], [("wave", "ra", "rk", "P")], [("wave", "ra", "rk", "P", "N")],
      [("wave", "ra", "rk", "P", "N", "rw")], [("tension", "P"), ("tension", "rw")], []]
plate("p8_1", [dict(pose=f, view=90, cap=c, marks=m, cx=8) for f, c, m in zip(fr, cp, mk)])

# 8.2 Hip and shoulder lines from above
angs = [(10, 20), (0, 15), (-10, 5), (-25, -5), (-30, -20), (-30, -40), (-30, -40), (0, 0)]
cps = ["Set", "Hips begin", "Hips lead", "Hips at 25°", "Hips stop", "Shoulders catch up", "Impact", "Square"]
def hips(ax, i):
    h, s = angs[i]
    for ang, w, lw, lab in ((h, 34, 2.4, "hips"), (s, 44, 1.0, "shoulders")):
        a = math.radians(ang)
        ax.plot([-w / 2 * math.cos(a), w / 2 * math.cos(a)], [-w / 2 * math.sin(a), w / 2 * math.sin(a)], color=INK, lw=lw,
                ls="-" if lab == "hips" else (0, (3, 1.6)))
    ax.add_patch(_E((0, 0), 12, 10, fc="white", ec=INK, lw=0.8))
    arrow(ax, (0, 6), (0, 30), lw=0.6, ms=4)
    if i == 7:
        ax.text(0, -26, "solid = hips\ndashed = shoulders", ha="center", fontsize=5.2)
multi("p8_2", 8, 4, hips, pw=1.12, ph=1.0, caps=cps, xr=30)

# 8.3 Hip rotation punch in Sanchin (front)
s0 = pose("sanchin_r", "kamae", rh=(-16, -38, -10), hip_yaw=12)
s1 = pose("sanchin_r", "kamae", rh=(-3, -16, 56), hip_yaw=-12)
fr = seq(s0, s1, 6) + [s1, s0]
cp = ["Chamber", "Hip starts", "Hip turns", "Fist follows", "Extending", "Impact", "Hold", "Return"]
plate("p8_3", [dict(pose=f, view=0, cap=c) for f, c in zip(fr, cp)])

# 8.4 Downward hammer fist in shiko dachi
h0 = pose("hachiji", lh=(16, -38, -10), rh=(-14, 30, 10))
h1 = pose("shiko", lh=(16, -38, -10), rh=(-14, 30, 10), pelvis=(0, 92, 0))
h2 = pose("shiko", lh=(16, -38, -10), rh=(-10, -20, 30))
h3 = pose("shiko", lh=(16, -38, -10), rh=(-8, -40, 36))
fr = [h0, mix(h0, h1, 0.5), h1, mix(h1, h2, 0.5), h2, h3, h3, pose("shiko", "kamae")]
cp = ["Arm rises", "Step out", "Begin to drop", "Body sinks", "Fist falls", "Strike", "Root", "Guard"]
mk = [[], [], [], [("arrow", "P", 0, -14)], [("arrow", "rw", 0, -16)], [("tension", "rw")], [("root", "la", "ra")], []]
plate("p8_4", [dict(pose=f, view=30, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])

# 8.5 Elbow strike
e0 = pose("sanchin_r", "kamae", hip_yaw=20)
e1 = pose("sanchin_r", lh=(16, -38, -10), rh=(4, 0, 4), rel=(0, 0, 1), hip_yaw=0)
e2 = pose("sanchin_r", lh=(16, -38, -10), rh=(12, -4, 6), rel=(0, 0, 1), hip_yaw=-25)
fr = [e0, mix(e0, e1, 0.5), e1, mix(e1, e2, 0.5), e2, e2, mix(e2, e0, 0.5), e0]
cp = ["Guard", "Arm folds", "Elbow forward", "Hip drives", "Elbow strike", "Lock", "Release", "Guard"]
plate("p8_5", [dict(pose=f, view=30, cap=c) for f, c in zip(fr, cp)])

# 8.6 Front kick
k0 = pose("sanchin_l", "kamae")
k1 = pose("sanchin_l", "kamae", ra=(-6, 46, 22), rfp=-20, rknee=(0, 0, 1), pelvis=(0, 93, 0))
k2 = pose("sanchin_l", "kamae", ra=(-6, 76, 72), rfp=-70, rknee=(0, 0, 1), pelvis=(0, 93, -4))
fr = [k0, mix(k0, k1, 0.5), k1, mix(k1, k2, 0.5), k2, k1, mix(k1, k0, 0.5), k0]
cp = ["Stance", "Knee rises", "Chamber", "Hip pushes", "Kick lands", "Re-chamber", "Lower", "Stance"]
plate("p8_6", [dict(pose=f, view=90, cap=c, cx=14) for f, c in zip(fr, cp)])

# 8.7 Stepping punch
z0 = pose("zenkutsu_l", lh=(14, -16, 48), rh=(-16, -38, -10))
mid = pose(dict(pelvis=(0, 86, 30)), lh=(14, -16, 48), rh=(-16, -38, -10), la=(14, 8, 44), ra=(0, 12, 30), lfy=-5, rfy=0,
           lknee=(0.1, 0, 1), rknee=(0, 0, 1))
z1 = pose(dict(pelvis=(0, 83, 52)), lh=(16, -38, -10), rh=(-2, -16, 56), la=(14, 8, 0), ra=(-14, 8, 88), lfy=25, rfy=5,
          lknee=(0.2, 0, 1), rknee=(-0.1, 0, 1), hip_yaw=-25)
fr = [z0, mix(z0, mid, 0.5), mid, mix(mid, z1, 0.33), mix(mid, z1, 0.66), z1, z1, z1]
cp = ["Stance", "Push off", "Foot passes", "Reach", "Land", "Punch arrives", "Hold", "Check"]
mk = [[], [("arrow", "P", 18, 0)], [], [], [], [("tension", "rw")], [("root", "la")], [("jline", "rw", "la")]]
plate("p8_7", [dict(pose=f, view=90, cap=c, marks=m, cx=36, zoom=1.35) for f, c, m in zip(fr, cp, mk)])

# 8.8 Makiwara striking
m0 = pose("zenkutsu_l", lh=(14, -20, 36), rh=(-16, -38, -10), props=(("makiwara", 70, 0),))
m1 = dict(m0, rh=(-6, -22, 30), lh=(16, -38, -8), hip_yaw=-15)
m2 = dict(m0, rh=(0, -10, 58), lh=(16, -38, -10), hip_yaw=-28)
fr = [m0, mix(m0, m1, 0.5), m1, m2, m2, mix(m2, m1, 0.5), m0, m0]
cp = ["Distance set", "Hip starts", "Fist travels", "Contact", "Drive through", "Recover", "Reset", "Next strike"]
plate("p8_8", [dict(pose=f, view=90, cap=c, cx=24, zoom=1.3) for f, c in zip(fr, cp)])

# 8.9 Power faults
P = D
pl = [dict(pose=dict(P, hip_yaw=0, chest_yaw=0), view=90, cap="Arm only", marks=[("x", "P")], cx=8),
      dict(pose=dict(P, lean=18), view=90, cap="Leaning in", marks=[("x", "N")], cx=8),
      dict(pose=dict(P, ra=(-14, 14, -44), rfp=-30), view=90, cap="Heel lifts", marks=[("x", "ra")], cx=8),
      dict(pose=dict(P, hip_yaw=-55, chest_yaw=-30), view=0, cap="Over-rotation", marks=[("x", "P")]),
      dict(pose=dict(P, rh=(-12, -4, 48)), view=90, cap="Elbow flares", marks=[("x", "re")], cx=8),
      dict(pose=dict(P, rh=(0, -14, 40)), view=90, cap="Short, bent arm", marks=[("x", "re")], cx=8),
      dict(pose=dict(P, pelvis=(0, 95, 8)), view=90, cap="Rising up", marks=[("x", "P")], cx=8),
      dict(pose=dict(P, head_pitch=-20, lean=-6), view=90, cap="Pulling back", marks=[("x", "head")], cx=8)]
plate("p8_9", pl)

# 8.10 Proximal-to-distal timing chart
fig, ax = chart("p8_10", 4.5, 2.0)
t = np.linspace(0, 0.5, 500)
def bump(c, w, h): return h * np.exp(-((t - c) / w) ** 2)
for c, w, h, lab, ls in ((0.10, 0.06, 0.45, "Legs and hips", "-"), (0.17, 0.055, 0.65, "Trunk", "--"),
                         (0.24, 0.05, 0.85, "Shoulder and upper arm", "-."), (0.30, 0.045, 1.0, "Forearm and fist", ":")):
    ax.plot(t, bump(c, w, h), color=INK, lw=1.1, ls=ls, label=lab)
ax.axvline(0.32, color=INK, lw=0.5)
ax.text(0.325, 1.02, "impact", fontsize=5.8)
ax.set_xlabel("Time (seconds)", fontsize=6.5); ax.set_ylabel("Speed (relative)", fontsize=6.5); ax.set_ylim(0, 1.12); ax.set_yticks([])
ax.legend(fontsize=5.8, frameon=False, loc="upper left")
save_chart(fig, "p8_10", 1)

# 8.11 Short-range power
c0 = pose("sanchin_r", "kamae", rh=(-4, -16, 44), hip_yaw=8, pelvis=(0, 92, 0))
c1 = pose("sanchin_r", "kamae", rh=(-3, -16, 54), hip_yaw=-10, pelvis=(0, 89, 1))
pt = pose("heiko", offset=(0, 0, 82), yaw=180, lh=(14, -20, 30), rh=(-14, -20, 30), lhand="open", rhand="open")
fr = [c0, mix(c0, c1, 0.25), mix(c0, c1, 0.5), mix(c0, c1, 0.75), c1, c1, mix(c1, c0, 0.5), c0]
cp = ["Fist touching", "Sink", "Feet press", "Hip snaps", "Wave arrives", "Partner moves", "Relax", "Reset"]
mk = [[], [("arrow", "P", 0, -10)], [("root", "la", "ra")], [], [("wave", "ra", "P", "rw")], [], [], []]
plate("p8_11", [dict(figs=[f, pt], view=90, cap=c, marks=m, zoom=1.3) for f, c, m in zip(fr, cp, mk)])

write_count("ch08")
