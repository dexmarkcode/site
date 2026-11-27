from body import *
from diag import *

O = dict(lhand="open", rhand="open")
HK = (16, -38, -10)
S = pose("sanchin_r", "kamae")
SZ = pose(dict(lh=(6, -42, 22), rh=(-6, -42, 22), **O), pelvis=(0, 38, 0), la=(6, 6, -6), ra=(-6, 6, -6),
          lfy=180, rfy=180, lknee=(0, 0.2, 1), rknee=(0, 0.2, 1))

# 15.1 A twenty-minute daily routine
R = [(pose("musubi", lh=(12, -60, 9), rh=(-12, -60, 9), **O), 0, "Bow"),
     (pose("heiko", "down", head_yaw=-50), 0, "Neck"),
     (pose("heiko", lh=(10, 52, 6), rh=(-10, 52, 6), **O), 90, "Arms"),
     (pose("heiko", lh=(14, -20, 30), rh=(-14, -20, 30), **O, chest_yaw=40), 0, "Trunk"),
     (pose("heiko", "down", pelvis=(0, 70, -12), lean=22, lh=(8, -30, 46), rh=(-8, -30, 46)), 90, "Squats"),
     (pose("heiko", lh=(8, -42, 18), rh=(-8, -44, 18), **O), 90, "Belly breath"),
     (S, 0, "Sanchin"),
     (pose("sanchin_r", lh=HK, rh=(-8, -8, 44), rhand="open", rroll=90), 45, "Tensho"),
     (pose("shiko", lh=HK, rh=(-16, -20, 44), props=(("chiishi", "r", (0, 1, 0), 40),)), 60, "Chi-ishi"),
     (pose("heiko", lh=(-18, -6, 12), rh=(-20, -5, 28), lhand="open"), 20, "Self-conditioning"),
     (pose("heiko", "down", lean=50, lh=(6, -60, 30), rh=(-6, -60, 30), **O), 90, "Stretch"),
     (SZ, 90, "Mokuso")]
plate("p15_1", [dict(pose=p, view=v, cap=c) for p, v, c in R])

# 15.2 Adapting for older students
wall = [("line", (-36, -3), (-36, 200), "-")]
OL = [(pose("sanchin_r", "kamae", pelvis=(0, 96, 0)), 0, "Higher Sanchin"),
      (pose("sanchin_r", lh=(20, -22, 26), rh=(-20, -22, 26), pelvis=(0, 96, 0)), 0, "Lower guard"),
      (pose("sagi_l", lh=(26, -30, 4), rh=(-23, -60, 2), lhand="open"), 0, "Balance by wall", ),
      (pose("heiko", lh=(12, -22, 30), rh=(-12, -22, 30), **O, pelvis=(0, 84, -16), la=(15, 8, 4), ra=(-15, 8, 4)), 90, "Wall sit (short)"),
      (pose("heiko", lh=(8, -42, 18), rh=(-8, -44, 18), **O), 90, "Nogare breathing"),
      (pose("sanchin_r", lh=HK, rh=(-8, -8, 40), rhand="open", rroll=90, pelvis=(0, 96, 0)), 45, "Gentle Tensho"),
      (pose("heiko", lh=(14, -24, 34), rh=(-14, -24, 34), props=(("tan",),)), 30, "Light wrist roll"),
      (pose("heiko", "down", **O, lean=20), 90, "Hinge, not bend")]
pl = [dict(pose=p, view=v, cap=c) for p, v, c in OL]
pl[2]["marks"] = [("line", (40, -3), (40, 200), "-")]
pl[3]["marks"] = wall
plate("p15_2", pl)

# 15.3 Weekly programmes for three levels
fig, axs = plt.subplots(1, 3, figsize=(4.6, 1.9), sharey=True)
days = ["M", "T", "W", "T", "F", "S", "S"]
progs = {"Beginner": [30, 0, 30, 0, 30, 20, 0], "Intermediate": [45, 30, 45, 20, 45, 60, 10], "Advanced": [60, 45, 60, 30, 60, 90, 20]}
for ax, (k, v) in zip(axs, progs.items()):
    ax.bar(range(7), v, 0.65, color="#cfcfcf", edgecolor=INK, lw=0.6)
    ax.set_xticks(range(7), days, fontsize=6); ax.set_title(k, fontsize=7)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
axs[0].set_ylabel("Minutes", fontsize=6.5)
save_chart(fig, "p15_3", 3)

# 15.4 A twelve-week programme
fig, ax = chart("p15_4", 4.5, 2.0)
wk = np.arange(1, 13)
blocks = [("Foundation", 1, 4), ("Build", 5, 8), ("Consolidate", 9, 11), ("Review", 12, 12)]
for name, a, b in blocks:
    ax.axvspan(a - 0.5, b + 0.5, color="#ededed" if name in ("Build", "Review") else "white", lw=0)
    ax.text((a + b) / 2, 3.25, name, ha="center", fontsize=6)
vol = [1, 1.2, 1.4, 1.0, 1.5, 1.7, 1.9, 1.2, 2.0, 2.2, 2.3, 1.3]
ints = [1, 1.1, 1.2, 1.0, 1.3, 1.5, 1.6, 1.1, 1.8, 2.0, 2.1, 1.2]
ax.plot(wk, vol, color=INK, lw=1.2, marker="o", ms=3, label="Volume")
ax.plot(wk, ints, color=INK, lw=0.9, ls="--", marker="s", ms=3, label="Intensity")
ax.set_xticks(wk); ax.set_xlabel("Week", fontsize=6.5); ax.set_yticks([]); ax.set_ylim(0.5, 3.5)
ax.legend(fontsize=5.8, frameon=False, loc="upper left")
save_chart(fig, "p15_4", 1)

# 15.5 Working around injuries
INJ = [(pose("sanchin_r", "kamae", pelvis=(0, 96, 0)), 90, "Knee: higher stance"),
       (pose("heiko", "kamae", pelvis=(0, 94, 0)), 0, "Knee: natural stance"),
       (pose("sanchin_r", lh=(20, -26, 26), rh=(-20, -26, 26)), 0, "Shoulder: lower guard"),
       (pose("sanchin_r", lh=HK, rh=(-16, -30, 30)), 90, "Shoulder: short punch"),
       (pose("heiko", lh=(12, -22, 30), rh=(-12, -22, 30), **O, pelvis=(0, 84, -16), la=(15, 8, 4), ra=(-15, 8, 4)), 90, "Back: supported"),
       (pose("heiko", "kamae"), 90, "Back: no deep shiko"),
       (pose("sanchin_r", lh=(20, -5, 28), rh=(-20, -5, 28), lhand="open", rhand="open"), 0, "Wrist: open hands"),
       (pose("heiko", lh=(8, -42, 18), rh=(-8, -44, 18), **O), 90, "Any injury: breathe")]
plate("p15_5", [dict(pose=p, view=v, cap=c, marks=[("line", (-36, -3), (-36, 200), "-")] if "supported" in c else []) for p, v, c in INJ])

# 15.6 Cool-down stretches
CD = [(pose("heiko", "down", lean=55, lh=(6, -60, 30), rh=(-6, -60, 30), **O), 90, "Hamstrings"),
      (pose("zenkutsu_l", "down", pelvis=(0, 70, 14), lh=(14, -70, 20), rh=(-14, -70, 10), **O), 90, "Hip flexors"),
      (pose(STANCES["shiko"], "down", pelvis=(0, 74, 0), lean=10, lh=(18, -66, 30), rh=(-18, -66, 30), **O), 0, "Inner thighs"),
      (pose("heiko", lh=(10, 46, 4), rh=(-24, -58, 2), **O, bend=-18), 0, "Side"),
      (pose("heiko", lh=(-30, -10, 4), rh=(-23, -60, 2), lhand="open"), 0, "Shoulder"),
      (pose("heiko", lh=(14, -24, 30), rh=(-14, -24, 30), **O, lroll=180, rroll=-180), 25, "Wrists"),
      (pose("heiko", "down", head_pitch=24), 90, "Neck"),
      (SZ, 90, "Rest in seiza")]
plate("p15_6", [dict(pose=p, view=v, cap=c) for p, v, c in CD])

# 15.7 Self-assessment tests
def pusher():
    return pose("zenkutsu_l", offset=(0, 0, 70), yaw=180, rh=(0, 128, 58), rworld=True, rhand="open")
AS = [dict(pose=pose("sagi_l", "kamae"), view=90, cap="One-leg balance"),
      dict(pose=pose("heiko", "down"), view=90, cap="Wall test", marks=[("line", (-20, -3), (-20, 192), "-")]),
      dict(pose=S, view=90, cap="Sanchin hold", marks=[("dantien",)]),
      dict(figs=[S, pusher()], view=90, cap="Push test", zoom=1.4),
      dict(pose=pose("heiko", lh=(10, -60, 6), rh=(-10, -60, 6)), view=30, cap="Grip hold"),
      dict(pose=pose("heiko", lh=(12, -22, 30), rh=(-12, -22, 30), **O, pelvis=(0, 80, -16), la=(15, 8, 4), ra=(-15, 8, 4)), view=90, cap="Wall sit", marks=[("line", (-34, -3), (-34, 200), "-")]),
      dict(pose=pose("heiko", "down", lean=55, lh=(6, -66, 30), rh=(-6, -66, 30), **O), view=90, cap="Forward reach"),
      dict(pose=pose("heiko", lh=(8, -42, 18), rh=(-8, -44, 18), **O), view=90, cap="Breath count")]
plate("p15_7", AS)

# 15.8 A lifetime of practice
fig, ax = chart("p15_8", 4.5, 1.9)
age = np.linspace(15, 85, 300)
power = np.exp(-((age - 32) / 22) ** 2)
skill = 1 / (1 + np.exp(-(age - 38) / 9))
cond = np.exp(-((age - 38) / 26) ** 2) * 0.85
ax.plot(age, power, color=INK, lw=1.0, ls="--", label="Raw power and speed")
ax.plot(age, cond, color=INK, lw=0.9, ls=":", label="Impact conditioning volume")
ax.plot(age, skill, color=INK, lw=1.4, label="Skill, sensitivity, internal quality")
ax.set_xlabel("Age (years)", fontsize=6.5); ax.set_yticks([])
ax.legend(fontsize=5.8, frameon=False, loc="lower right")
ax.text(16, 1.04, "illustrative only", fontsize=5.6, style="italic")
save_chart(fig, "p15_8", 1)

# 15.9 The kata as a curriculum (12 postures)
K = [
    (pose("sanchin_r", "kamae"), 0, "Sanchin"),
    (pose("zenkutsu_l", lh=(4, 22, 24), rh=(-16, -38, -10), lel=(1, 0.3, 0.2), hip_yaw=-10), 60, "Gekisai Dai Ichi"),
    (pose("neko_l", lh=(14, 0, 34), rh=(-16, -38, -8), lhand="open", hip_yaw=-15), 60, "Gekisai Dai Ni"),
    (pose("sanchin_r", rh=(-8, -8, 40), lh=(16, -38, -10), rhand="open", rroll=90), 30, "Tensho"),
    (pose("shiko", rh=(-6, -30, 30), lh=(0, -22, 26), lhand="open"), 20, "Saifa"),
    (pose("shiko", lh=(22, -34, 22), rh=(-22, -8, 18), rhand="open"), 0, "Seiyunchin"),
    (pose("sanchin_l", lh=(6, -12, 52), rh=(-16, -38, -10), lhand="open"), 70, "Shisochin"),
    (pose("sagi_l", "kamae"), 70, "Sanseru"),
    (pose("neko_r", lh=(16, 10, 30), rh=(-10, -30, 30), **O), 40, "Seipai"),
    (pose("neko_l", lh=(8, -2, 36), rh=(-8, -26, 36), **O), 50, "Kururunfa"),
    (pose("sanchin_l", lh=(4, -14, 52), rh=(-16, -38, -10)), 80, "Seisan"),
    (pose("shiko", lh=(8, -14, 50), rh=(-8, -14, 50), **O), 30, "Suparinpei")]
plate("p15_9", [dict(pose=p, view=v, cap=c) for p, v, c in K])

# 15.10 Training while travelling (no equipment)
TR = [(pose("heiko", lh=(8, -42, 18), rh=(-8, -44, 18), **O), 90, "Breathing"),
      (S, 0, "Sanchin in place"),
      (pose("sanchin_r", lh=(12, -10, 50), rh=(-12, -10, 50), **O, lroll=90, rroll=-90), 90, "Wall press"),
      (pose("shiko", "kamae"), 0, "Shiko hold"),
      (pose("heiko", lh=(6, -20, 30), rh=(-6, -26, 30)), 30, "Towel wring"),
      (pose("sagi_l", "kamae"), 90, "Balance"),
      (pose("heiko", lh=(12, -22, 30), rh=(-12, -22, 30), **O, pelvis=(0, 80, -16), la=(15, 8, 4), ra=(-15, 8, 4)), 90, "Wall sit"),
      (SZ, 0, "Mokuso")]
plate("p15_10", [dict(pose=p, view=v, cap=c) for p, v, c in TR])

# 15.11 A five-minute morning routine
MR = [(pose("heiko", "down"), 0, "Stand, scan"), (pose("heiko", lh=(10, 52, 6), rh=(-10, 52, 6), **O), 0, "Reach up"),
      (pose("heiko", "down", lean=40, **O), 90, "Hinge"), (pose("heiko", lh=(14, -20, 30), rh=(-14, -20, 30), **O, chest_yaw=-35), 0, "Twist"),
      (pose("heiko", "kamae", pelvis=(0, 88, 0)), 90, "Sink"), (S, 90, "Three Sanchin breaths"),
      (pose("heiko", lh=(34, -16, 14), rh=(-34, -16, 14), **O, lroll=-90, rroll=90), 0, "Open"),
      (pose("heiko", lh=(4, -40, 22), rh=(-4, -40, 22), **O), 0, "Close")]
plate("p15_11", [dict(pose=p, view=v, cap=c) for p, v, c in MR])

write_count("ch15")
