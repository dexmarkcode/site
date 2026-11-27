from body import *
from diag import *

S = pose("sanchin_r", "kamae")
D = pose("sanchin_r", "down")

# 5.1 Building the Sanchin guard
g1 = pose("sanchin_r", lh=(18, -52, 14), rh=(-18, -52, 14))
g2 = pose("sanchin_r", lh=(20, -36, 22), rh=(-20, -36, 22), lhand="open", rhand="open")
g3 = pose("sanchin_r", lh=(20, -12, 28), rh=(-20, -12, 28), lhand="open", rhand="open")
fr = [D, g1, g2, g3, dict(S, lhand="open", rhand="open"), S, S, S]
cp = ["Arms down", "Elbows bend", "Forearms rise", "Elbows settle", "Hands open", "Fists close", "Guard set", "Check width"]
mk = [[], [], [], [], [], [], [("tension", "le"), ("tension", "re")], [("jline", "le", "lw"), ("jline", "re", "rw")]]
plate("p5_1", [dict(pose=f, view=0, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])

# 5.2 Guard measurements and faults
pl = [dict(pose=S, view=90, cap="Fist at shoulder height", marks=[("line", (-30, 147), (50, 147))]),
      dict(pose=S, view=0, cap="Fist-width from ribs", marks=[("ring", "le", 8), ("ring", "re", 8)]),
      dict(pose=S, view=90, cap="Forearm angle", marks=[("jline", "le", "lw")]),
      dict(pose=S, view=35, cap="Three-quarter"),
      dict(pose=dict(S, lel=(1.8, -0.3, 0), rel=(-1.8, -0.3, 0)), view=0, cap="Elbows flared", marks=[("x", "le"), ("x", "re")]),
      dict(pose=dict(S, lh=(20, 16, 24), rh=(-20, 16, 24)), view=0, cap="Fists too high", marks=[("x", "lw")]),
      dict(pose=dict(S, lh=(20, -26, 30), rh=(-20, -26, 30)), view=90, cap="Fists too low", marks=[("x", "rw")]),
      dict(pose=dict(S, lh=(8, -6, 30), rh=(-8, -6, 30)), view=0, cap="Fists too close", marks=[("x", "lw")])]
plate("p5_2", pl)

# 5.3 Chains of tension
C = [
    ([("jline", "lw", "le"), ("jline", "le", "ls"), ("jline", "ls", "lhip"), ("jline", "rw", "re"), ("jline", "re", "rs"), ("jline", "rs", "rhip")], 0, "Arm–back line"),
    ([("jline", "N", "P"), ("jline", "P", "lk"), ("jline", "P", "rk")], 90, "Front line"),
    ([("jline", "head", "N"), ("jline", "N", "P"), ("jline", "P", "ra")], 180, "Back line"),
    ([("jline", "lw", "le"), ("jline", "le", "ls"), ("jline", "ls", "rhip"), ("jline", "rhip", "rk"), ("jline", "rk", "ra")], 0, "Left spiral"),
    ([("jline", "rw", "re"), ("jline", "re", "rs"), ("jline", "rs", "lhip"), ("jline", "lhip", "lk"), ("jline", "lk", "la")], 0, "Right spiral"),
    ([("jline", "lk", "rk"), ("jline", "lk", "la"), ("jline", "rk", "ra"), ("jline", "lhip", "lk"), ("jline", "rhip", "rk")], 0, "Inner leg line"),
    ([("dantien",), ("ring", "P", 16)], 90, "Deep core"),
    ([("jline", "lw", "le"), ("jline", "le", "ls"), ("jline", "ls", "rhip"), ("jline", "rhip", "rk"), ("jline", "rk", "ra"),
      ("jline", "rw", "re"), ("jline", "re", "rs"), ("jline", "rs", "lhip"), ("jline", "lhip", "lk"), ("jline", "lk", "la"), ("dantien",)], 0, "Whole connection"),
]
plate("p5_3", [dict(pose=S, view=v, cap=c, marks=m) for m, v, c in C])

# 5.4 / 5.5 The Sanchin punch
K = S
ch = pose("sanchin_r", "kamae", rh=(-16, -38, -10))
mid = pose("sanchin_r", "kamae", rh=(-10, -26, 26))
ext = pose("sanchin_r", "kamae", rh=(-3, -16, 56))
opn = dict(ext, rhand="open", rroll=90)
grab = pose("sanchin_r", "kamae", rh=(-6, -18, 44))
fr = [K, ch, mid, ext, opn, grab, ch, K]
cp = ["Guard", "Pull to chamber", "Fist travels", "Full extension", "Hand opens", "Grasp", "Pull back", "Guard"]
mk = [[], [("breath_in",)], [("breath_out",)], [("tension", "re"), ("tension", "P")], [], [], [("arrow", "rw", -14, 0)], []]
plate("p5_4", [dict(pose=f, view=35, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])
plate("p5_5", [dict(pose=f, view=90, cap=c, marks=m, cx=8) for f, c, m in zip(fr, cp, mk)])

# 5.6 Closing sequence: double open-hand push and circle
o1 = pose("sanchin_r", lh=(14, -32, 4), rh=(-14, -32, 4), lhand="open", rhand="open")
o2 = pose("sanchin_r", lh=(12, -16, 22), rh=(-12, -16, 22), lhand="open", rhand="open", lroll=90, rroll=-90)
o3 = pose("sanchin_r", lh=(10, -14, 50), rh=(-10, -14, 50), lhand="open", rhand="open", lroll=90, rroll=-90)
o4 = pose("sanchin_r", lh=(16, 2, 36), rh=(-12, -30, 34), lhand="open", rhand="open")
o5 = pose("sanchin_r", lh=(10, -34, 36), rh=(-14, 0, 34), lhand="open", rhand="open")
o6 = pose("sanchin_r", lh=(10, -18, 48), rh=(-10, -28, 48), lhand="open", rhand="open", lroll=90, rroll=-90)
fr = [o1, o2, o3, o4, o5, o6, mix(o6, o1, 0.5), o1]
cp = ["Hands draw back", "Palms forward", "Push out", "Circle begins", "Circle", "Double push", "Return", "Close"]
plate("p5_6", [dict(pose=f, view=40, cap=c) for f, c in zip(fr, cp)])

# 5.7 Tension over time chart
fig, ax = chart("p5_7", 4.5, 1.9)
t = np.linspace(0, 12, 1200)
ten = np.interp(t, [0, 1.5, 2, 6.5, 7, 7.6, 8.5, 9, 12], [0.25, 0.25, 0.55, 0.85, 1.0, 0.45, 0.25, 0.25, 0.25])
br = np.interp(t, [0, 1.5, 6.8, 8.5, 12], [-0.6, 0.6, -0.4, 0.6, 0.6])
ax.plot(t, ten, color=INK, lw=1.3, label="Muscle tension (share of maximum)")
ax.plot(t, br * 0.4 + 0.5, color=INK, lw=0.8, ls=(0, (3, 2)), label="Breath (rising = inhale)")
ax.axvspan(6.6, 7.4, color="#dcdcdc", lw=0)
ax.text(7.0, 1.06, "peak", ha="center", fontsize=5.8)
ax.text(0.7, 0.18, "base tone", fontsize=5.6)
ax.set_ylim(0, 1.15); ax.set_xlabel("Seconds", fontsize=6.5); ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25%", "50%", "75%", "100%"])
ax.legend(fontsize=5.8, frameon=False, loc="upper left")
save_chart(fig, "p5_7", 1)

# 5.8 Tension release and re-tension
fr = [S, S, ch, mid, ext, ext, mix(ext, K, 0.5), K]
cp = ["Base tone", "Settle", "Soften to move", "Travel: 50%", "Lock: 100%", "Release to 75%", "Return: 50%", "Base tone"]
mk = [[("tension", "P")], [("tension", "P")], [], [("tension", "P")], [("tension", "P"), ("tension", "re"), ("tension", "rk"), ("tension", "lk")],
      [("tension", "P"), ("tension", "re")], [("tension", "P")], [("tension", "P")]]
plate("p5_8", [dict(pose=f, view=0, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])

# 5.9 Shoulder blade setting, back view
pl = [dict(pose=S, view=180, cap="Blades set down"), dict(pose=S, view=150, cap="Back, angled"),
      dict(pose=dict(S, chest_yaw=0, lean=-3), view=180, cap="Blades pinched", marks=[("x", "N")]),
      dict(pose=dict(S, lean=8, head_pitch=10), view=150, cap="Back rounded", marks=[("x", "N")]),
      dict(pose=dict(S, lel=(1.6, -0.2, 0), rel=(-1.6, -0.2, 0)), view=180, cap="Elbows lifted", marks=[("x", "le")]),
      dict(pose=S, view=180, cap="Lats engaged", marks=[("jline", "le", "lhip"), ("jline", "re", "rhip")]),
      dict(pose=S, view=90, cap="Side: shoulder low", marks=[("ring", "rs", 9)]),
      dict(pose=dict(S, head_pitch=-14), view=90, cap="Shoulder hunched", marks=[("x", "rs")])]
plate("p5_9", pl)

# 5.10 Isometric holds
wall_marks = [("line", (62, -3), (62, 200), "-")]
w1 = pose("sanchin_r", lh=(12, -10, 50), rh=(-12, -10, 50), lhand="open", rhand="open", lroll=90, rroll=-90)
w2 = pose("sanchin_r", lh=(12, 24, 40), rh=(-12, 24, 40), lhand="open", rhand="open", lroll=90, rroll=-90)
pt = pose("sanchin_r", "kamae", offset=(0, 0, 70), yaw=180, lh=(10, 132, 38), rh=(-10, 132, 38), lworld=True, rworld=True, lhand="open", rhand="open")
pl = [dict(pose=w1, view=90, cap="Wall press", marks=wall_marks, cx=10), dict(pose=dict(w1, pelvis=(0, 91, -6), lean=6), view=90, cap="Lean into it", marks=wall_marks, cx=10),
      dict(pose=w2, view=90, cap="High press", marks=[("line", (54, -3), (54, 200), "-")], cx=10),
      dict(pose=pose("sanchin_r", lh=(26, -30, 20), rh=(-26, -30, 20)), view=0, cap="Door-frame press", marks=[("line", (-42, -3), (-42, 200), "-"), ("line", (42, -3), (42, 200), "-")]),
      dict(figs=[S, pt], view=90, cap="Partner presses"),
      dict(pose=S, view=0, cap="Self-resisted", marks=[("push", "lw", 4, 0), ("push", "rw", -4, 0)]),
      dict(pose=pose("shiko", "kamae"), view=0, cap="Shiko hold"),
      dict(pose=S, view=90, cap="Sanchin hold", marks=[("dantien",), ("root", "la", "ra")])]
plate("p5_10", pl)

# 5.11 Forming the fist (close-up, side view)
STEPS = [(0, 0), (0.35, 0), (0.7, 0), (1.0, 0), (1.0, 1.0)]
def fist_draw(ax, i):
    if i < 5:
        hand_side(ax, *STEPS[i], x=10, y=0, s=0.8)
    else:
        hand_fist(ax, 0, 0, s=1.2, view="front")
multi("p5_11", 6, 3, fist_draw, pw=1.5, ph=0.9, caps=["Open hand", "Fingertips curl", "Fingers roll in", "Rolled tight", "Thumb locks across", "Striking knuckles (front)"], xr=34)

write_count("ch05")
