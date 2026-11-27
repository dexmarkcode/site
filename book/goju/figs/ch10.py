from body import *
from diag import *

def ci(side, d, L=40):
    return ("chiishi", side, d, L)

HK = (16, -38, -10)
# 10.1 Chi-ishi: basic forward raises and wrist turns (right hand)
f0 = pose("shiko", lh=HK, rh=(-16, -60, 10), props=(ci("r", (0, -1, 0.15)),))
f1 = pose("shiko", lh=HK, rh=(-16, -20, 44), props=(ci("r", (0, 1, 0)),))
f2 = pose("shiko", lh=HK, rh=(-16, -20, 44), props=(ci("r", (0, 0.3, 1)),))
f3 = pose("shiko", lh=HK, rh=(-16, -20, 44), props=(ci("r", (0, -0.2, 1)),))
f4 = pose("shiko", lh=HK, rh=(-16, -20, 44), props=(ci("r", (-1, 0.4, 0)),))
f5 = pose("shiko", lh=HK, rh=(-16, -20, 44), props=(ci("r", (1, 0.4, 0)),))
fr = [f0, mix(f0, f1, .5), f1, f2, f3, f1, f4, f5]
cp = ["Hang", "Raise", "Vertical", "Lower forward", "Level", "Back to vertical", "Turn out", "Turn in"]
plate("p10_1", [dict(pose=f, view=60, cap=c) for f, c in zip(fr, cp)])

# 10.2 Chi-ishi: shoulder and punch work
g0 = pose("shiko", lh=HK, rh=(-16, -38, -10), props=(ci("r", (0, 0, 1)),))
g1 = pose("shiko", lh=HK, rh=(-4, -16, 54), props=(ci("r", (0, 1, 0)),))
g2 = pose("shiko", lh=HK, rh=(-14, 20, -4), props=(ci("r", (0, -1, -0.3)),))
g3 = pose("shiko", lh=HK, rh=(-22, -10, 10), props=(ci("r", (0, -1, 0.2)),))
g4 = pose("shiko", lh=HK, rh=(-40, -10, 0), props=(ci("r", (0, 1, 0)),))
g5 = pose("shiko", lh=HK, rh=(-40, -10, 0), props=(ci("r", (-1, 0, 0)),))
fr = [g0, g1, pose("shiko", lh=HK, rh=(-16, 8, 26), props=(ci("r", (0, 0.2, -1)),)), g2, g3, g4, g5, g0]
cp = ["Chamber", "Slow punch", "Lift behind", "Down the back", "Return", "Arm to side", "Lower out", "Chamber"]
plate("p10_2", [dict(pose=f, view=40, cap=c) for f, c in zip(fr, cp)])

# 10.3 Nigiri-game: walking in Sanchin
jars = (("jar", "l"), ("jar", "r"))
J0 = pose("sanchin_r", lh=(22, -54, 14), rh=(-22, -54, 14), props=jars)
CR = []
for i, t in enumerate(np.linspace(0, 1, 6)):
    p = dict(J0)
    path = [(16, -10), (8, -4), (4, 6), (8, 18), (13, 28), (16, 32)]
    x, z = path[i]
    p["la"] = (x, 8 + (3 if 0 < i < 5 else 0), z)
    p["pelvis"] = (0, 91, 21 * t)
    CR.append(p)
fr = [J0] + CR + [dict(CR[-1], lh=(22, -50, 22), rh=(-22, -50, 22))]
cp = ["Jars held", "Begin step", "Draw in", "Pass", "Arc out", "Reach", "Land", "Settle"]
plate("p10_3", [dict(pose=f, view=90, cap=c, cx=10) for f, c in zip(fr, cp)])

# 10.4 Nigiri-game arm positions
pos = [((22, -56, 6), "Sides"), ((14, -30, 36), "Forward low"), ((14, -6, 44), "Forward level"), ((40, -10, 4), "Out to sides"),
       ((14, 26, 20), "Overhead"), ((20, -46, -14), "Behind"), ((20, -30, 22), "Sanchin arms"), ((8, -50, 22), "Hug front")]
plate("p10_4", [dict(pose=pose("sanchin_r", lh=p, rh=(-p[0], p[1], p[2]), props=jars), view=30, cap=c) for p, c in pos])

# 10.5 Kongoken
k = [((24, -60, 20), "Grip low"), ((24, -30, 30), "Lift"), ((24, 0, 30), "Chest"), ((22, 30, 10), "Overhead"),
     ((22, 0, 22), "Lower behind head"), ((24, -20, 24), "Press out"), ((24, -10, 30), "Twist left"), ((24, -10, 30), "Twist right")]
pl = []
for i, (p, c) in enumerate(k):
    extra = {}
    if "left" in c:
        extra = dict(chest_yaw=30)
    if "right" in c:
        extra = dict(chest_yaw=-30)
    pl.append(dict(pose=pose("shiko", lh=p, rh=(-p[0], p[1], p[2]), lhand="fist", rhand="fist", props=(("kongoken",),), **extra), view=25, cap=c))
plate("p10_5", pl)

# 10.6 Tan (stone barbell)
t = [((16, -40, 26), "Grip"), ((16, -30, 32), "Wrist roll"), ((16, -6, 34), "Curl"), ((16, 0, 18), "To chest"),
     ((16, 30, 10), "Press up"), ((16, -6, 34), "Front hold"), ((16, -6, 34), "Twist"), ((16, -40, 26), "Lower")]
pl = []
for p, c in t:
    ex = dict(chest_yaw=35) if c == "Twist" else {}
    pl.append(dict(pose=pose("shiko", lh=p, rh=(-p[0], p[1], p[2]), props=(("tan",),), **ex), view=30, cap=c))
plate("p10_6", pl)

# 10.7 Ishi-sashi (stone padlock) - short handle stone
def isa(side): return ("chiishi", side, (0, -1, 0), 6)
ii = [pose("sanchin_r", lh=HK, rh=(-16, -38, -10), props=(isa("r"),)),
      pose("sanchin_r", lh=HK, rh=(-4, -16, 54), props=(isa("r"),)),
      pose("sanchin_r", lh=HK, rh=(-16, -38, -10), props=(isa("r"),)),
      pose("sanchin_r", lh=HK, rh=(-10, 4, 30), props=(("chiishi", "r", (0, 1, 0), 6),)),
      pose("sanchin_r", lh=HK, rh=(-30, -12, 22), props=(isa("r"),)),
      pose("sanchin_r", lh=(4, -16, 54), rh=HK, props=(isa("l"),)),
      pose("sanchin_r", lh=(20, -5, 28), rh=(-20, -5, 28), props=(isa("l"), isa("r"))),
      pose("sanchin_r", lh=(22, -58, 4), rh=(-22, -58, 4), props=(isa("l"), isa("r")))]
plate("p10_7", [dict(pose=f, view=50, cap=c) for f, c in zip(ii, ["Chamber", "Slow punch", "Return", "Rising block", "Side block", "Other hand", "Sanchin guard", "Rest"])])

# 10.8 Tetsu-geta
G = (("geta", "r"),)
q0 = pose("heiko", "kamae", props=G)
q1 = pose("heiko", "kamae", ra=(-8, 46, 22), rfp=0, rknee=(0, 0, 1), props=G)
q2 = pose("heiko", "kamae", ra=(-8, 70, 70), rfp=-60, rknee=(0, 0, 1), props=G)
q3 = pose("heiko", "kamae", ra=(-40, 50, 0), rknee=(0, 0, 1), props=G)
q4 = pose("heiko", "kamae", ra=(-10, 40, -30), rknee=(0, -1, 0), props=G)
fr = [q0, mix(q0, q1, .5), q1, q2, q1, q3, q4, q0]
cp = ["Stand", "Lift knee", "Knee high", "Slow kick", "Re-chamber", "Leg to side", "Leg back", "Lower"]
plate("p10_8", [dict(pose=f, view=70, cap=c) for f, c in zip(fr, cp)])

# 10.9 Construction of the tools
names = ["chi-ishi", "nigiri-game", "ishi-sashi", "tan", "kongoken", "tetsu-geta", "makiwara", "sand bag"]
notes = ["handle ~45 cm; head 1–4 kg", "jar 1–3 kg; add sand", "stone or iron 2–5 kg", "bar 1–1.5 m; 5–20 kg",
         "oval iron ring 10–30 kg", "iron sandal 1–3 kg each", "tapered board; padded top", "canvas, sand or beans"]
def con(ax, i):
    EQUIP[names[i]](ax)
    ax.text(0, -44, notes[i], ha="center", fontsize=5.0, style="italic")
multi("p10_9", 8, 4, con, pw=1.12, ph=1.15, caps=names, xr=46)

# 10.10 Load progression chart
fig, ax = chart("p10_10", 4.5, 1.9)
w = np.arange(0, 53, 1)
load = np.minimum(1.0 + 0.06 * w - 0.25 * ((w % 4) == 3), 4.0)
ax.step(w, load, where="post", color=INK, lw=1.1, label="Chi-ishi head weight (kg)")
reps = np.minimum(8 + w // 4, 20)
ax2 = ax.twinx(); ax2.plot(w, reps, color=INK, lw=0.8, ls="--", label="Repetitions per set")
ax2.spines["top"].set_visible(False); ax2.tick_params(labelsize=6.5)
ax.set_xlabel("Week", fontsize=6.5); ax.set_ylabel("kg", fontsize=6.5); ax2.set_ylabel("reps", fontsize=6.5)
ax.text(14.5, 1.25, "every fourth week lighter", fontsize=5.6)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=5.8, frameon=False, loc="upper left")
save_chart(fig, "p10_10", 1)

# 10.11 Chi-ishi faults and safe practice
pl = [dict(pose=dict(f1, lean=12), view=60, cap="Leaning back to lift", marks=[("x", "N")]),
      dict(pose=pose("shiko", lh=HK, rh=(-16, -20, 44), props=(ci("r", (0, 0.6, -1)),)), view=60, cap="Wrist over-bent", marks=[("x", "rw")]),
      dict(pose=dict(f2, pelvis=(0, 96, 0)), view=60, cap="Stance lost", marks=[("x", "rk")]),
      dict(pose=dict(f1, lel=(-1.5, -.1, 0)), view=0, cap="Elbow flaring", marks=[("x", "re")]),
      dict(pose=f1, view=60, cap="Correct: elbow low"),
      dict(pose=f2, view=60, cap="Correct: slow lower"),
      dict(pose=pose("shiko", lh=HK, rh=(-16, -20, 44), props=(ci("r", (0, 1, 0), 26),)), view=60, cap="Choke up (lighter)"),
      dict(pose=pose("shiko", lh=(14, -20, 44), rh=(-16, -20, 44), props=(ci("r", (0, 1, 0)),)), view=60, cap="Spotting hand ready")]
plate("p10_11", pl)

write_count("ch10")
