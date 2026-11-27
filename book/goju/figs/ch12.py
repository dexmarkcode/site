from body import *
from diag import *

O = dict(lhand="open", rhand="open")

# 12.1 Finger and hand exercises (close-ups)
def fingers(ax, i):
    if i == 0: hand_open(ax, 0, -8, s=1.2)
    elif i == 1: hand_open(ax, 0, -8, s=1.2, fingers_bent=0.5)
    elif i == 2: hand_open(ax, 0, -8, s=1.2, fingers_bent=0.9)
    elif i == 3: hand_side(ax, 0.35, 0, x=10, s=0.8)
    elif i == 4: hand_side(ax, 0.7, 0.3, x=10, s=0.8)
    elif i == 5: hand_side(ax, 1.0, 1.0, x=10, s=0.8)
    elif i == 6: hand_open(ax, 0, -8, s=1.2, ang=-25)
    else: hand_open(ax, 0, -8, s=1.2, ang=25)
multi("p12_1", 8, 4, fingers, pw=1.12, ph=0.95, xr=34,
      caps=["Spread wide", "Half claw", "Full claw", "Hook grip", "Roll in", "Squeeze", "Fan left", "Fan right"])

# 12.2 Wall push-ups: palms, knuckles, fingertips
wall = [("line", (78, -3), (78, 200), "-")]
def wp(lean, z, hand, y=-8):
    return pose("heiko", lean=lean, pelvis=(0, 99, -6), lh=(14, y, z), rh=(-14, y, z), lhand=hand, rhand=hand, lroll=90, rroll=-90, head_pitch=-lean * 0.3)
fr = [(wp(12, 46, "open"), "Palms on wall"), (wp(26, 34, "open"), "Lower"), (wp(12, 46, "open"), "Press away"),
      (wp(12, 44, "fist"), "Knuckles"), (wp(24, 32, "fist"), "Lower on knuckles"), (wp(12, 46, "open"), "Fingertips"),
      (wp(22, 36, "open"), "Lower on fingertips"), (wp(30, 40, "open", -30), "Lower angle")]
plate("p12_2", [dict(pose=p, view=90, cap=c, marks=[("line", (60, -3), (60, 200), "-")], cx=20, zoom=1.15) for p, c in fr])

# 12.3 Wrist strength with a short weighted stick
def ws(d, side="r", L=24):
    return ("chiishi", side, d, L)
fa = (-14, -24, 34)
fr = [(pose("heiko", lh=(16, -38, -10), rh=fa, props=(ws((0, 1, 0)),)), "Upright"),
      (pose("heiko", lh=(16, -38, -10), rh=fa, props=(ws((0, 0.4, 1)),)), "Lower forward"),
      (pose("heiko", lh=(16, -38, -10), rh=fa, props=(ws((0, -0.2, -1)),)), "Lower back"),
      (pose("heiko", lh=(16, -38, -10), rh=fa, props=(ws((1, 0.3, 0)),)), "Rotate in"),
      (pose("heiko", lh=(16, -38, -10), rh=fa, props=(ws((-1, 0.3, 0)),)), "Rotate out"),
      (pose("heiko", lh=(-10, -30, 24), rh=fa, lhand="open", props=(ws((0, 1, 0)),)), "Support the forearm"),
      (pose("heiko", lh=(14, -24, 34), rh=fa, props=(("tan",),)), "Wrist roller"),
      (pose("heiko", lh=(14, -24, 34), rh=fa, props=(("tan",),), chest_yaw=0), "Roll back")]
plate("p12_3", [dict(pose=p, view=60, cap=c) for p, c in fr])

# 12.4 The jari-bako (gravel box) finger thrusts
def jari(ax, i):
    palm = [40, 28, 22, 18, 22, 28, 34, 30][i]
    eq_jari_bako(ax)
    if i < 7:
        hand_open(ax, 0, palm, s=0.7, ang=180, fingers_bent=0 if i < 6 else 0.4)
    else:
        hand_fist(ax, 0, 14, s=0.8, view="front")
multi("p12_4", 8, 4, jari, pw=1.12, ph=1.05, xr=50,
      caps=["Above the box", "Fingers enter", "Thrust down", "Full depth", "Withdraw", "Rise", "Grip the grains", "Fist (advanced)"])

# 12.5 Shoulder care
sc = [(pose("heiko", lh=(12, 50, 6), rh=(-12, 50, 6), **O), 0, "Arms up"),
      (pose("heiko", lh=(44, -6, 6), rh=(-44, -6, 6), **O), 0, "Arms out"),
      (pose("heiko", lh=(16, -2, 44), rh=(-16, -2, 44)), 90, "Band: start"),
      (pose("heiko", lh=(44, -2, 10), rh=(-44, -2, 10)), 0, "Band: pull apart"),
      (pose("heiko", lh=(24, 10, 12), rh=(-24, 10, 12), **O, lel=(1, -1, -0.3), rel=(-1, -1, -0.3)), 180, "Wall slide: low"),
      (pose("heiko", lh=(16, 40, 4), rh=(-16, 40, 4), **O), 180, "Wall slide: high"),
      (pose("heiko", lh=(14, -26, 26), rh=(-16, -38, -10), lel=(0.2, -1, 0)), 0, "Rotation: in"),
      (pose("heiko", lh=(36, -26, 10), rh=(-16, -38, -10), lel=(0.2, -1, 0)), 0, "Rotation: out")]
plate("p12_5", [dict(pose=p, view=v, cap=c) for p, v, c in sc])

# 12.6 Hip strength
hs = [(pose("heiko", "kamae", ra=(-36, 26, 0), rknee=(-1, 0, 0.1)), 0, "Side leg raise"),
      (pose("heiko", "kamae", ra=(-10, 26, -30), rknee=(0, 0, -1)), 90, "Back leg raise"),
      (pose("zenkutsu_l", "kamae", pelvis=(0, 70, 8)), 90, "Split squat"),
      (pose("shiko", "kamae", pelvis=(0, 70, 0)), 0, "Shiko squat"),
      (pose("shiko", "kamae", pelvis=(10, 76, 0)), 0, "Side-to-side"),
      (pose("sagi_l", "kamae"), 90, "Knee hold"),
      (pose("heiko", "kamae", pelvis=(0, 78, -10), lean=20), 90, "Squat"),
      (pose("sanchin_r", "kamae", pelvis=(0, 86, 0)), 0, "Low Sanchin hold")]
plate("p12_6", [dict(pose=p, view=v, cap=c) for p, v, c in hs])

# 12.7 Spine care (standing)
sp = [(pose("heiko", "down", lean=35, lh=(10, -60, 30), rh=(-10, -60, 30), **O), 90, "Hip hinge"),
      (pose("heiko", lh=(10, -40, -10), rh=(-10, -40, -10), **O, lean=-10, head_pitch=-10), 90, "Gentle extension"),
      (pose("heiko", lh=(14, -20, 30), rh=(-14, -20, 30), **O, chest_yaw=40), 0, "Rotate left"),
      (pose("heiko", lh=(14, -20, 30), rh=(-14, -20, 30), **O, chest_yaw=-40), 0, "Rotate right"),
      (pose("heiko", lh=(10, 46, 4), rh=(-24, -58, 2), **O, bend=-18), 0, "Side bend"),
      (pose("heiko", lh=(24, -58, 2), rh=(-10, 46, 4), **O, bend=18), 0, "Other side"),
      (pose("heiko", lh=(12, -22, 30), rh=(-12, -22, 30), **O, pelvis=(0, 80, -16), la=(15, 8, 4), ra=(-15, 8, 4)), 90, "Wall sit"),
      (pose("heiko", "kamae"), 90, "Stand tall")]
plate("p12_7", [dict(pose=p, view=v, cap=c, marks=[("line", (-34, -3), (-34, 200), "-")] if c == "Wall sit" else []) for p, v, c in sp])

# 12.8 Single-leg strength
sl = [(pose("sagi_l", "kamae"), "Balance"), (pose("sagi_l", "kamae", pelvis=(0, 88, 0)), "Quarter squat"),
      (pose("sagi_l", "kamae", pelvis=(0, 80, -4), lean=10, la=(-2, 24, 40), lfp=0), "Half squat"),
      (pose("sagi_l", "kamae", pelvis=(0, 96, 0), la=(-2, 20, -26), lknee=(0, 0, -1)), "Leg behind"),
      (pose("sagi_l", "kamae", lean=40, la=(-2, 60, -50), lknee=(0, 0, -1), pelvis=(0, 95, 0)), "Single-leg hinge"),
      (pose("sagi_l", "kamae", pelvis=(0, 88, 0), la=(-2, 46, 30)), "Step-down"),
      (pose("sagi_l", "kamae", ra=(-8, 14, 0), rfp=-20, pelvis=(0, 101, 0)), "Heel raise"),
      (pose("sagi_l", lh=(30, -10, 20), rh=(-30, -10, 20), **O), "Arms wide")]
plate("p12_8", [dict(pose=p, view=90, cap=c) for p, c in sl], cols=4)

# 12.9 Adaptation rates chart
fig, ax = chart("p12_9", 4.5, 1.9)
wk = np.linspace(0, 52, 300)
for tau, lab, ls in ((4, "Muscle strength", "-"), (12, "Skin and bone", "--"), (30, "Tendon and ligament", ":")):
    ax.plot(wk, 1 - np.exp(-wk / tau), color=INK, lw=1.1, ls=ls, label=lab)
ax.set_xlabel("Weeks of consistent training", fontsize=6.5); ax.set_ylabel("Adaptation (relative)", fontsize=6.5)
ax.set_yticks([]); ax.legend(fontsize=5.8, frameon=False, loc="lower right")
ax.text(16, 0.35, "the danger gap:\nmuscle outruns tendon", fontsize=5.6)
save_chart(fig, "p12_9", 1)

# 12.10 Weekly plan chart
fig, ax = chart("p12_10", 4.5, 1.7)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
grid = [["Hands", "Hips"], ["Shoulders", "Spine"], ["Hands", "Legs"], ["Rest"], ["Shoulders", "Hips"], ["Spine", "Legs"], ["Rest"]]
for i, items in enumerate(grid):
    for j, it in enumerate(items):
        fc = "white" if it != "Rest" else "#d9d9d9"
        ax.add_patch(plt.Rectangle((i + 0.05, 1 - j * 0.5), 0.9, 0.42, fc=fc, ec=INK, lw=0.6))
        ax.text(i + 0.5, 1.21 - j * 0.5, it, ha="center", va="center", fontsize=6)
ax.set_xlim(0, 7); ax.set_ylim(0.4, 1.5); ax.set_xticks(np.arange(7) + 0.5, days); ax.set_yticks([])
ax.spines["left"].set_visible(False)
save_chart(fig, "p12_10", 1)

# 12.11 Neck strengthening (self-resisted)
nk = [(pose("heiko", lh=(4, 18, 14), rh=(-4, 18, 14), **O), 90, "Palms on forehead"),
      (pose("heiko", lh=(4, 18, 14), rh=(-4, 18, 14), **O), 0, "Press: hold"),
      (pose("heiko", lh=(6, 20, -10), rh=(-6, 20, -10), **O), 90, "Hands behind head"),
      (pose("heiko", lh=(6, 20, -10), rh=(-6, 20, -10), **O), 180, "Press back"),
      (pose("heiko", lh=(14, 20, 0), rh=(-23, -60, 2), lhand="open"), 0, "Hand to side"),
      (pose("heiko", rh=(-14, 20, 0), lh=(23, -60, 2), rhand="open"), 0, "Other side"),
      (pose("heiko", "down", head_pitch=20), 90, "Gentle nod"),
      (pose("heiko", "down", head_yaw=45), 0, "Gentle turn")]
plate("p12_11", [dict(pose=p, view=v, cap=c) for p, v, c in nk])

# 12.12 Towel and grip work
tw = [(pose("heiko", lh=(6, -20, 30), rh=(-6, -26, 30)), "Towel wring"), (pose("heiko", lh=(6, -26, 30), rh=(-6, -20, 30)), "Reverse"),
      (pose("heiko", lh=(4, -10, 34), rh=(-4, -26, 34)), "Hand over hand"), (pose("heiko", lh=(10, -60, 6), rh=(-10, -60, 6)), "Farmer's hold")]
plate("p12_12", [dict(pose=p, view=30, cap=c) for p, c in tw])

# 12.13 Feet and ankles
ft = [(pose("heiko", "kamae", pelvis=(0, 102, 0), la=(15, 12, 0), ra=(-15, 12, 0), lfp=-25, rfp=-25), 90, "Heel raise"),
      (pose("heiko", "kamae", la=(15, 10, 0), ra=(-15, 10, 0), lfp=20, rfp=20), 90, "Toe raise"),
      (pose("sagi_l", "kamae", ra=(-8, 12, 0), rfp=-25, pelvis=(0, 101, 0)), 90, "One-leg raise"),
      (pose("heiko", "kamae", pelvis=(0, 88, 0)), 90, "Toe spread hold")]
plate("p12_13", [dict(pose=p, view=v, cap=c) for p, v, c in ft])

write_count("ch12")
