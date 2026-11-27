from body import *
from diag import *

O = dict(lhand="open", rhand="open")
H = pose("heiko", "down")
SZ = pose(dict(lh=(6, -42, 22), rh=(-6, -42, 22), **O), pelvis=(0, 38, 0), la=(6, 6, -6), ra=(-6, 6, -6),
          lfy=180, rfy=180, lknee=(0, 0.2, 1), rknee=(0, 0.2, 1))
S = pose("sanchin_r", "kamae")

# 13.1 The tanden in different postures
pl = [dict(pose=H, view=0, cap="Standing, front", marks=[("dantien",)]), dict(pose=H, view=90, cap="Standing, side", marks=[("dantien",)]),
      dict(pose=SZ, view=0, cap="Seiza, front", marks=[("dantien",)]), dict(pose=SZ, view=90, cap="Seiza, side", marks=[("dantien",)]),
      dict(pose=S, view=0, cap="Sanchin, front", marks=[("dantien",)]), dict(pose=S, view=90, cap="Sanchin, side", marks=[("dantien",)]),
      dict(pose=pose("shiko", "kamae"), view=0, cap="Shiko", marks=[("dantien",)]), dict(pose=pose("neko_l", "kamae"), view=90, cap="Neko ashi", marks=[("dantien",)])]
plate("p13_1", pl)

# 13.2 The extended arm test
ext = pose("heiko", lh=(16, -38, -10), rh=(-10, -12, 50), rhand="open", pelvis=(0, 94, 0))
ten = dict(ext, rhand="fist")
def bender(push_y=134):
    return pose("heiko", offset=(-34, 0, 40), yaw=-90, lh=(-6, push_y - 4, 24), rh=(6, 126, 24), lworld=False, rworld=False, **O,
                lel=None)
P2 = pose("heiko", offset=(-46, 0, 34), yaw=90, **O)
# partner hands on student's forearm: world approx (-10, 130, 40) and elbow (-14, 120, 20)
def partner():
    G = ry(-90)
    off = np.array([-62.0, 0, 40])
    loc = lambda p: tuple(G @ (np.array(p, float) - off))
    return pose("heiko", offset=tuple(off), yaw=90, lh=loc((-10, 134, 46)), rh=loc((-14, 122, 24)), lworld=True, rworld=True, **O)
pt = partner()
pl = [dict(pose=ext, view=25, cap="Arm extended, soft"), dict(figs=[ext, pt], view=25, cap="Partner tests"),
      dict(figs=[dict(ten, rh=(-10, -4, 30)), pt], view=25, cap="Muscle: arm bends", marks=[("x", "re")]),
      dict(figs=[ext, pt], view=25, cap="Relaxed, connected"),
      dict(figs=[ext, pt], view=25, cap="Attention beyond hand", marks=[("arrow", "rw", -24, 0)]),
      dict(pose=ext, view=90, cap="Side view", marks=[("arrow", "rw", 26, 0)]),
      dict(pose=ext, view=90, cap="Line from foot", marks=[("wave", "la", "P", "N", "rw")]),
      dict(pose=ext, view=25, cap="Breathe out, settle", marks=[("breath_out",)])]
for d in pl:
    d["zoom"] = 1.3
plate("p13_2", pl)

# 13.3 Body scan
joints = ["head", "N", "chest", "le", "navel", "P", "rk", "la"]
caps = ["Crown and face", "Neck and shoulders", "Chest", "Arms and hands", "Belly", "Pelvis", "Knees", "Feet"]
plate("p13_3", [dict(pose=H, view=0, cap=c, marks=[("ring", j, 13 if j == "head" else 10)]) for j, c in zip(joints, caps)])

# 13.4 Opening and closing
c0 = pose("heiko", lh=(4, -40, 22), rh=(-4, -40, 22), **O)
c1 = pose("heiko", lh=(14, -22, 26), rh=(-14, -22, 26), **O, lroll=-90, rroll=90)
c2 = pose("heiko", lh=(34, -16, 14), rh=(-34, -16, 14), **O, lroll=-90, rroll=90)
fr = [c0, mix(c0, c1, .5), c1, mix(c1, c2, .5), c2, mix(c2, c1, .5), c1, c0]
cp = ["Hands gathered", "Inhale", "Hands open", "Opening", "Fully open", "Exhale", "Closing", "Gathered"]
mk = [[("dantien",)], [("breath_in",)], [], [], [], [("breath_out",)], [], [("dantien",)]]
plate("p13_4", [dict(pose=f, view=0, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])

# 13.5 Schematic: breath, centre, intent
def sch(ax, i):
    torso_schematic(ax, ["neutral", "in", "out", "neutral"][i], arrows=[[], [((0, 30), (0, 14))], [((0, -20), (0, -20))], []][i])
    if i == 2:
        for a in np.linspace(0, 2 * np.pi, 9)[:-1]:
            arrow(ax, (0 + 6 * np.cos(a), -20 + 6 * np.sin(a)), (0 + 13 * np.cos(a), -20 + 13 * np.sin(a)), lw=0.6, ms=4)
    if i == 3:
        arrow(ax, (0, -20), (0, 34), lw=0.7, ms=4); arrow(ax, (0, -20), (24, 30), lw=0.7, ms=4); arrow(ax, (0, -20), (-24, 30), lw=0.7, ms=4)
multi("p13_5", 4, 4, sch, pw=1.12, ph=1.45, xr=38, caps=["Settled centre", "Breath sinks", "Pressure spreads", "Intent rises"])

# 13.6 Slow breathing chart
fig, ax = chart("p13_6", 4.5, 1.9)
t = np.linspace(0, 10, 500)
hr = 78 - 12 * (1 - np.exp(-np.clip(t - 2, 0, None) / 2.5))
hr_noise = hr + 1.2 * np.sin(2 * np.pi * t / 0.9)
ax.plot(t, hr_noise, color=INK, lw=0.9)
ax.axvline(2, color=INK, lw=0.5, ls=":")
ax.text(2.1, 79.5, "slow breathing begins (about 6 breaths a minute)", fontsize=5.6)
ax.set_xlabel("Minutes", fontsize=6.5); ax.set_ylabel("Heart rate (beats/min)", fontsize=6.5)
ax.set_ylim(60, 82)
ax.text(6.5, 64, "illustrative pattern", fontsize=5.6, style="italic")
save_chart(fig, "p13_6", 1)

# 13.7 Heavy arm relaxation test
def lifter(hy):
    G = ry(-90); off = np.array([-48.0, 0, 6])
    loc = lambda p: tuple(G @ (np.array(p, float) - off))
    return pose("heiko", offset=tuple(off), yaw=90, lh=loc((-24, hy, 12)), rh=loc((-23, hy - 22, 6)), lworld=True, rworld=True, **O)
h_up = pose("heiko", "down", rh=(-26, -40, 14), rhand="open")
pl = [dict(figs=[H, lifter(96)], view=0, cap="Partner supports arm"), dict(figs=[h_up, lifter(110)], view=0, cap="Lifts gently"),
      dict(figs=[h_up, lifter(110)], view=0, cap="Lets go: arm drops?"), dict(figs=[H, lifter(96)], view=0, cap="Heavy, relaxed arm")]
for d in pl: d["zoom"] = 1.35
plate("p13_7", pl)

# 13.8 Zanshin after a technique
z0 = pose("zenkutsu_l", lh=(16, -38, -10), rh=(-2, -16, 56), hip_yaw=-25)
z1 = pose("zenkutsu_l", "kamae")
fr = [z0, z0, mix(z0, z1, .3), mix(z0, z1, .6), z1, z1, dict(z1, head_yaw=-30), dict(z1, head_yaw=30)]
cp = ["Technique lands", "Hold intent", "Withdraw slowly", "Guard reforms", "Zanshin", "Breathe", "Awareness left", "Awareness right"]
plate("p13_8", [dict(pose=f, view=60, cap=c) for f, c in zip(fr, cp)])

# 13.9 From sitting to standing practice
k1 = pose(dict(lh=(12, -38, 22), rh=(-12, -44, 14), **O), pelvis=(0, 60, -6), la=(8, 8, 18), ra=(-8, 7, -42), lfy=-5, rfy=180,
          lknee=(0, 0, 1), rknee=(0, -1, 0.6))
fr = [SZ, dict(SZ, head_pitch=14), k1, mix(k1, pose("heiko", "down", **O), .5), pose("heiko", "down", **O),
      pose("heiko", lh=(14, -44, 26), rh=(-14, -44, 26), **O, pelvis=(0, 90, 0)), S, S]
cp = ["Mokuso", "Eyes lowered", "Rise to one knee", "Stand", "Stand quietly", "Hands to centre", "Sanchin dachi", "Begin kata"]
plate("p13_9", [dict(pose=f, view=90, cap=c) for f, c in zip(fr, cp)])

# 13.10 The "unliftable" body: sinking explained
def lifter_b(y):
    return pose("heiko", offset=(0, 0, -52), yaw=0, lh=(15, y, 52), rh=(-15, y, 52), lworld=True, rworld=True, **O, pelvis=(0, 90, 0))
up = pose("heiko", "down", pelvis=(0, 99, 0))
sunk = pose("heiko", "down", pelvis=(0, 88, 0), lh=(24, -60, 6), rh=(-24, -60, 6))
pl = [dict(figs=[up, lifter_b(124)], view=90, cap="Hands under arms"), dict(figs=[dict(up, pelvis=(0, 102, 0)), lifter_b(128)], view=90, cap="Tense: easy to lift"),
      dict(figs=[up, lifter_b(124)], view=90, cap="Reset"), dict(figs=[sunk, lifter_b(118)], view=90, cap="Relax, sink", marks=[("dantien",)]),
      dict(figs=[sunk, lifter_b(118)], view=90, cap="Weight drops", marks=[("root", "la")]), dict(figs=[sunk, lifter_b(118)], view=180, cap="From behind"),
      dict(figs=[dict(sunk, lean=6), lifter_b(118)], view=90, cap="Hips slightly back"), dict(figs=[sunk, lifter_b(118)], view=90, cap="Partner strains")]
for d in pl: d["zoom"] = 1.3
plate("p13_10", pl)

# 13.11 Slow walking in Sanchin with attention
CR = []
path = [(16, -10), (11, -6), (6, 0), (4, 8), (7, 16), (11, 24), (14, 30), (16, 32)]
for i, t in enumerate(np.linspace(0, 1, 8)):
    p = dict(S); x, z = path[i]
    p["la"] = (x, 8 + (3 if 0 < i < 7 else 0), z); p["pelvis"] = (0, 91, 21 * t)
    CR.append(p)
plate("p13_11", [dict(pose=f, view=90, cap=c, cx=10, marks=[("dantien",)]) for f, c in
                 zip(CR, ["Feel both feet", "Weight settles", "Foot lightens", "Draws in", "Arcs out", "Feels the floor", "Lands", "Weight shared"])])

# 13.12 Sensing between the palms
gaps = [2, 6, 12, 20, 12, 6, 2, 30]
pl = []
for g, c in zip(gaps, ["Palms touching", "Small gap", "Opening", "Wide", "Closing", "Near", "Touch", "Arms apart"]):
    pl.append(dict(pose=pose("heiko", lh=(g / 2 + 2, -24, 30), rh=(-g / 2 - 2, -24, 30), **O, lroll=-90, rroll=90, pelvis=(0, 94, 0)), view=0, cap=c))
plate("p13_12", pl)

write_count("ch13")
