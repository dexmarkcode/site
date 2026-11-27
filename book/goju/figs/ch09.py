from body import *
from diag import *

HK = (16, -38, -10)
O = dict(rhand="open", lhand="open")

# 9.1 Rising palm sequence (Tensho opening hand)
t0 = pose("sanchin_r", lh=HK, rh=(-14, -30, 12), lhand="fist", rhand="open", rroll=0)
t1 = pose("sanchin_r", lh=HK, rh=(-12, -14, 24), lhand="fist", rhand="open", rroll=60)
t2 = pose("sanchin_r", lh=HK, rh=(-10, -4, 34), lhand="fist", rhand="open", rroll=90)
t3 = pose("sanchin_r", lh=HK, rh=(-8, -8, 44), lhand="fist", rhand="open", rroll=90)
t4 = pose("sanchin_r", lh=HK, rh=(-12, -30, 40), lhand="fist", rhand="open", rroll=0)
fr = [t0, mix(t0, t1, .5), t1, t2, t3, mix(t3, t4, .5), t4, mix(t4, t0, .5)]
cp = ["Hand at side", "Rises", "Wrist bends back", "Palm vertical", "Press forward", "Turn down", "Press down", "Return"]
plate("p9_1", [dict(pose=f, view=45, cap=c) for f, c in zip(fr, cp)])

# 9.2 / 9.3 Mawashi uke
m0 = pose("sanchin_r", lh=(14, 2, 30), rh=(-14, -30, 30), **O)
m1 = pose("sanchin_r", lh=(4, -4, 34), rh=(-4, -24, 34), **O)
m2 = pose("sanchin_r", lh=(-6, -20, 32), rh=(6, -6, 32), **O)
m3 = pose("sanchin_r", lh=(10, -34, 28), rh=(-12, 4, 30), **O)
m4 = pose("sanchin_r", lh=(12, -20, 16), rh=(-12, -4, 16), **O, lroll=90, rroll=-90)
m5 = pose("sanchin_r", lh=(10, -26, 50), rh=(-10, -6, 50), **O, lroll=90, rroll=-90)
fr = [m0, m1, m2, m3, mix(m3, m4, .5), m4, m5, m5]
cp = ["Hands apart", "Circle begins", "Hands cross", "Circle completes", "Draw in", "At the chest", "Double push", "Tiger's mouth"]
plate("p9_2", [dict(pose=f, view=0, cap=c) for f, c in zip(fr, cp)])
plate("p9_3", [dict(pose=f, view=90, cap=c, cx=8) for f, c in zip(fr, cp)])

# 9.4 Kake uke (hooking block)
k0 = pose("neko_l", lh=(16, -38, -8), rh=(-16, -38, -10))
k1 = pose("neko_l", lh=(-4, -10, 24), rh=HK, lhand="open")
k2 = pose("neko_l", lh=(10, 0, 36), rh=HK, lhand="open", lroll=-60)
k3 = pose("neko_l", lh=(22, -2, 30), rh=HK, lhand="open", lroll=-90)
k4 = pose("neko_l", lh=(16, -10, 20), rh=(-4, -16, 50), lhand="open", lroll=-90)
fr = [k0, k1, mix(k1, k2, .5), k2, k3, mix(k3, k4, .5), k4, k4]
cp = ["Ready", "Hand rises inside", "Meets the arm", "Wrist hooks", "Leads outward", "Draws in", "Counter punch", "Hold"]
plate("p9_4", [dict(pose=f, view=45, cap=c) for f, c in zip(fr, cp)])

# 9.5 Hand shapes
def shapes(ax, i):
    if i == 0:
        hand_side(ax, 0, 0, x=10, s=0.8)
    elif i == 1:
        hand_side(ax, 0.25, 0.2, x=10, s=0.8)
    elif i == 2:
        hand_open(ax, 0, -8, s=1.2, ang=0)
    elif i == 3:
        hand_open(ax, 0, -8, s=1.2, ang=0, fingers_bent=0.35)
    elif i == 4:
        hand_side(ax, 0.55, 0.6, x=10, s=0.8)
    elif i == 5:
        hand_side(ax, 0.9, 0.3, x=10, s=0.8)
    elif i == 6:
        hand_open(ax, 0, -8, s=1.2, ang=-90)
    else:
        hand_side(ax, 0.6, 1.0, x=10, s=0.8)
multi("p9_5", 8, 4, shapes, pw=1.12, ph=0.95, caps=["Open (kaishu)", "Soft hand", "Palm heel (shotei)", "Tiger's mouth", "Crane's beak", "Bear hand", "Knife edge", "Half fist (hiraken)"], xr=34)

# 9.6 Paths of the hands
def paths(ax, i):
    th = np.linspace(0, 2 * np.pi, 200)
    if i == 0:
        ax.plot(20 * np.cos(th), 26 * np.sin(th), color=INK, lw=1.0)
        arrow(ax, (20 * np.cos(1.0), 26 * np.sin(1.0)), (20 * np.cos(1.2), 26 * np.sin(1.2)))
        arrow(ax, (-20 * np.cos(1.0), -26 * np.sin(1.0)), (-20 * np.cos(1.2), -26 * np.sin(1.2)))
        ax.text(0, 0, "mawashi uke\n(front view)", ha="center", va="center", fontsize=5.6)
    elif i == 1:
        ax.plot(np.linspace(-26, 26, 100), 14 * np.sin(np.linspace(0, np.pi, 100)), color=INK, lw=1.0)
        arrow(ax, (20, 6), (26, 0))
        ax.text(0, -10, "rising palm\n(side view)", ha="center", fontsize=5.6)
    elif i == 2:
        x = np.linspace(-26, 26, 100)
        ax.plot(x, 10 * np.sin(x / 26 * 2 * np.pi), color=INK, lw=1.0)
        arrow(ax, (22, -8), (26, 0))
        ax.text(0, -22, "hooking hand\n(top view)", ha="center", fontsize=5.6)
    else:
        r = np.linspace(4, 26, 300); a = np.linspace(0, 4 * np.pi, 300)
        ax.plot(r * np.cos(a), r * np.sin(a), color=INK, lw=0.9)
        ax.text(0, -32, "spiral of the wrist", ha="center", fontsize=5.6)
multi("p9_6", 4, 4, paths, pw=1.12, ph=1.0, caps=["Circle", "Arc", "Wave", "Spiral"], xr=34)

# 9.7 Tension wave in Tensho
fig, ax = chart("p9_7", 4.5, 1.9)
t = np.linspace(0, 16, 1600)
ten = 0.45 + 0.4 * np.sin(2 * np.pi * t / 8 - np.pi / 2) ** 2 * np.sign(np.sin(2 * np.pi * t / 8 - np.pi / 2) + 1.5)
ten = 0.3 + 0.55 * (0.5 - 0.5 * np.cos(2 * np.pi * t / 8))
br = 0.5 - 0.35 * np.cos(2 * np.pi * t / 8 + 0.4)
san = np.interp(t % 6.6, [0, 1.6, 2.0, 6.4, 6.6], [0.25, 0.25, 0.6, 0.95, 0.25])
ax.plot(t, ten, color=INK, lw=1.3, label="Tensho: tension rises and falls smoothly")
ax.plot(t, san, color=INK, lw=0.8, ls=":", label="Sanchin, for comparison")
ax.set_ylim(0, 1.15); ax.set_yticks([0, 0.5, 1.0], ["low", "half", "high"]); ax.set_xlabel("Seconds", fontsize=6.5)
ax.legend(fontsize=5.8, frameon=False, loc="upper left")
save_chart(fig, "p9_7", 1)

# 9.8 Double downward palm press
d0 = pose("sanchin_r", lh=(14, -16, 22), rh=(-14, -16, 22), **O, lroll=90, rroll=-90)
d1 = pose("sanchin_r", lh=(14, -30, 30), rh=(-14, -30, 30), **O)
d2 = pose("sanchin_r", lh=(16, -50, 30), rh=(-16, -50, 30), **O)
d3 = pose("sanchin_r", lh=(18, -60, 24), rh=(-18, -60, 24), **O)
fr = [d0, mix(d0, d1, .5), d1, mix(d1, d2, .5), d2, d3, d3, d0]
cp = ["Palms at chest", "Turn down", "Begin press", "Sink", "Press", "Full press", "Hold", "Rise"]
mk = [[], [], [("breath_out",)], [("arrow", "P", 0, -10)], [], [("tension", "lw"), ("tension", "rw")], [("root", "la", "ra")], [("breath_in",)]]
plate("p9_8", [dict(pose=f, view=30, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])

# 9.9 Soft hand receiving a punch
att0 = pose("zenkutsu_r", offset=(0, 0, 100), yaw=180, rh=(-16, -38, -10), lh=(16, -20, 30), hip_yaw=-10)
att1 = pose("zenkutsu_r", offset=(0, 0, 100), yaw=180, rh=(-2, -16, 56), lh=(16, -38, -10), hip_yaw=-25)
d_0 = pose("neko_l", "kamae", lhand="open")
d_1 = pose("neko_l", lh=(6, -6, 40), rh=(-16, -30, 20), lhand="open", lroll=-60)
d_2 = pose("neko_l", lh=(22, -6, 34), rh=(-16, -30, 20), lhand="open", lroll=-90, hip_yaw=-15)
d_3 = pose("neko_l", lh=(20, -10, 30), rh=(-4, -14, 52), lhand="open", lroll=-90, hip_yaw=-25)
pairs = [(d_0, att0), (d_1, mix(att0, att1, .5)), (d_1, att1), (d_2, att1), (d_2, att1), (d_3, att1), (d_3, att1), (d_0, att0)]
cp = ["Facing", "Punch comes", "Contact", "Stick and turn", "Lead it past", "Counter", "Check", "Reset"]
plate("p9_9", [dict(figs=[a, b], view=90, cap=c, zoom=1.45) for (a, b), c in zip(pairs, cp)])

# 9.10 Tensho faults
T = t3
pl = [dict(pose=dict(T, rroll=0), view=45, cap="Palm not vertical", marks=[("x", "rw")]),
      dict(pose=dict(T, rh=(-30, -6, 34)), view=0, cap="Hand off centre", marks=[("x", "rw")]),
      dict(pose=dict(T, rel=(-1.6, -.2, 0)), view=0, cap="Elbow lifts", marks=[("x", "re")]),
      dict(pose=dict(T, lean=12), view=90, cap="Leaning after hand", marks=[("x", "N")]),
      dict(pose=dict(T, rh=(-8, -8, 56)), view=90, cap="Arm locked straight", marks=[("x", "re")]),
      dict(pose=dict(T, head_pitch=24), view=90, cap="Watching the hand", marks=[("x", "head")]),
      dict(pose=dict(T, pelvis=(0, 98, 0)), view=90, cap="Stance lost", marks=[("x", "rk")]),
      dict(pose=T, view=45, cap="Correct", marks=[("dantien",)])]
plate("p9_10", pl)

# 9.11 Wrist and hand mobility
w = [pose("heiko", lh=(14, -20, 30), rh=(-14, -20, 30), **O, lroll=r, rroll=-r) for r in (0, 45, 90, 135)]
w += [pose("heiko", lh=(14, -20 + dy, 30), rh=(-14, -20 + dy, 30), **O, lroll=90, rroll=-90) for dy in (-10, 0, 10)]
w += [pose("heiko", lh=(10, -20, 30), rh=(-10, -20, 30))]
plate("p9_11", [dict(pose=f, view=30, cap=c) for f, c in zip(w, ["Palms down", "Turning", "Palms in", "Palms up", "Flex down", "Neutral", "Flex up", "Gentle fists"])])

# 9.12 Wrist-top (koken) block
c0 = pose("neko_l", "kamae")
c1 = pose("neko_l", lh=(8, -40, 30), rh=HK, lhand="open", lroll=180)
c2 = pose("neko_l", lh=(14, -16, 34), rh=HK, lhand="open", lroll=180)
c3 = pose("neko_l", lh=(18, 0, 30), rh=HK, lhand="open", lroll=180)
plate("p9_12", [dict(pose=f, view=45, cap=c) for f, c in zip([c0, c1, c2, c3], ["Ready", "Wrist bends", "Rising arc", "Wrist top lifts"])])

write_count("ch09")
