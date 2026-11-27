from body import *
from diag import *

# 3.1 Schematic torso: diaphragm and pelvic floor
modes = ["neutral", "in", "out", "reverse", "in", "out", "neutral", "reverse"]
caps = ["At rest", "Inhale: dome lowers", "Exhale: dome rises", "Reverse breath", "Belly widens", "Abdomen firm", "Tanden", "Pressure held"]
arrs = [[], [((0, 30), (0, 14))], [((0, 0), (0, 18))], [((-26, -14), (-18, -14)), ((26, -14), (18, -14))],
        [((-14, -12), (-24, -12)), ((14, -12), (24, -12))], [((-24, -12), (-17, -12)), ((24, -12), (17, -12))], [],
        [((0, 30), (0, 14)), ((0, -44), (0, -34))]]
multi("p3_1", 8, 4, lambda ax, i: torso_schematic(ax, modes[i], arrows=arrs[i]), pw=1.12, ph=1.45, caps=caps, xr=38)

# 3.2 Breath waveforms
fig, axs = plt.subplots(4, 1, figsize=(4.5, 3.9), sharex=True)
t = np.linspace(0, 20, 2000)
def env(t, pts):
    return np.interp(t, [p[0] for p in pts], [p[1] for p in pts])
waves = [
    ("Natural breathing", np.sin(2 * np.pi * t / 5) * 0.5),
    ("Sanchin (ibuki): short inhale, long tensed exhale", env(t % 6.6, [(0, -1), (1.6, 1), (6.4, -1), (6.6, -1)])),
    ("Tensho (soft breath): slow, even, unbroken", env(t % 8, [(0, -0.8), (3.5, 0.8), (8, -0.8)])),
    ("Nogare: quiet in, quiet controlled release", env(t % 5, [(0, -0.6), (1.5, 0.6), (2, 0.6), (5, -0.6)])),
]
for ax, (ttl, y) in zip(axs, waves):
    ax.plot(t, y, color=INK, lw=1.0)
    ax.axhline(0, color=INK, lw=0.3, ls=":")
    ax.set_yticks([]); ax.set_ylim(-1.3, 1.5)
    ax.text(0.2, 1.25, ttl, fontsize=6.3, va="center")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
axs[1].fill_between(t, -1.3, 1.5, where=((t % 6.6) > 1.6) & ((t % 6.6) < 6.4), color="#e2e2e2", lw=0)
axs[1].text(4.3, -1.05, "tension held", fontsize=5.4)
axs[-1].set_xlabel("Time (seconds)  —  rising line = inhalation, falling line = exhalation", fontsize=6.3)
axs[-1].tick_params(labelsize=6)
save_chart(fig, "p3_2", 4)

# 3.3 Abdominal breathing, hands on the belly
BI = pose("heiko", lh=(8, -42, 18), rh=(-8, -44, 18), lhand="open", rhand="open")
BO = dict(BI, lean=3)
SZ = pose(dict(lh=(8, -40, 20), rh=(-8, -42, 20), lhand="open", rhand="open"), pelvis=(0, 38, 0), la=(6, 6, -6), ra=(-6, 6, -6),
          lfy=180, rfy=180, lknee=(0, 0.2, 1), rknee=(0, 0.2, 1))
pl = [dict(pose=BI, view=90, cap="Hands on belly"), dict(pose=BI, view=90, cap="Inhale: belly fills", marks=[("breath_in",)]),
      dict(pose=BO, view=90, cap="Exhale: belly draws", marks=[("breath_out",)]), dict(pose=BI, view=0, cap="Front view"),
      dict(pose=SZ, view=90, cap="In seiza"), dict(pose=SZ, view=90, cap="Seiza: inhale", marks=[("breath_in",)]),
      dict(pose=SZ, view=90, cap="Seiza: exhale", marks=[("breath_out",)]), dict(pose=SZ, view=0, cap="Seiza front")]
plate("p3_3", pl)

# 3.4 Ibuki in Sanchin
K0 = pose("sanchin_r", "kamae", rh=(-16, -38, -10))
K1 = pose("sanchin_r", "kamae", rh=(-2, -16, 56))
fr = [K0, K0, mix(K0, K1, 0.35), mix(K0, K1, 0.7), K1, K1, mix(K1, K0, 0.5), K0]
cp = ["Chamber", "Inhale (nose)", "Begin exhale", "Push out slowly", "Full extension", "Finish breath", "Return: inhale", "Guard"]
mk = [[], [("breath_in",)], [("breath_out",)], [("breath_out",), ("tension", "P")], [("tension", "P"), ("tension", "re")],
      [("tension", "P")], [("breath_in",)], []]
plate("p3_4", [dict(pose=f, view=90, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])

# 3.5 Nogare with a soft hand
T0 = pose("sanchin_r", lh=(16, -38, -10), rh=(-14, -30, 16), rhand="open", rroll=90)
T1 = pose("sanchin_r", lh=(16, -38, -10), rh=(-8, -10, 42), rhand="open", rroll=90)
T2 = pose("sanchin_r", lh=(16, -38, -10), rh=(-14, -34, 38), rhand="open", rroll=0)
fr = [T0, mix(T0, T1, 0.33), mix(T0, T1, 0.66), T1, mix(T1, T2, 0.5), T2, mix(T2, T0, 0.5), T0]
cp = ["Soft hand at side", "Quiet inhale", "Palm rises", "Palm forward", "Turning", "Pressing down", "Return", "Rest"]
plate("p3_5", [dict(pose=f, view=60, cap=c) for f, c in zip(fr, cp)])

# 3.6 Breathing with arm raises
A0 = pose("heiko", "down", lhand="open", rhand="open")
A1 = pose("heiko", lh=(44, -10, 6), rh=(-44, -10, 6), lhand="open", rhand="open")
A2 = pose("heiko", lh=(12, 46, 6), rh=(-12, 46, 6), lhand="open", rhand="open")
fr = [A0, mix(A0, A1, 0.5), A1, mix(A1, A2, 0.5), A2, mix(A2, A1, 0.5), A1, A0]
cp = ["Begin", "Inhale", "Arms level", "Inhale fully", "Top", "Exhale", "Exhale", "Settle"]
plate("p3_6", [dict(pose=f, view=0, cap=c) for f, c in zip(fr, cp)])

# 3.7 Hand checks for breathing
H1 = pose("heiko", lh=(20, -26, 4), rh=(-20, -26, 4), lhand="open", rhand="open", lroll=90, rroll=-90)
H2 = pose("heiko", lh=(8, -42, 18), rh=(-8, -44, 18), lhand="open", rhand="open")
H3 = pose("heiko", lh=(10, -46, -16), rh=(-10, -46, -16), lhand="open", rhand="open")
pl = [dict(pose=H1, view=0, cap="Hands on lower ribs"), dict(pose=H1, view=90, cap="Ribs, side"),
      dict(pose=H2, view=0, cap="Hands on belly"), dict(pose=H2, view=90, cap="Belly, side"),
      dict(pose=H3, view=180, cap="Hands on back"), dict(pose=H3, view=90, cap="Back, side")]
plate("p3_7", pl, cols=3, pw=1.5)

# 3.8 Breathing faults
S = pose("sanchin_r", "kamae")
pl = [dict(pose=dict(S, head_pitch=-15), view=90, cap="Chest heaves", marks=[("x", "N")]),
      dict(pose=S, view=90, cap="Breath held", marks=[("x", "head")]),
      dict(pose=dict(S, lean=-8), view=90, cap="Belly pushed out", marks=[("x", "navel")]),
      dict(pose=dict(S, lean=14, head_pitch=16), view=90, cap="Collapse on exhale", marks=[("x", "chest")]),
      dict(pose=dict(S, pelvis=(0, 97, 0)), view=90, cap="Rises on inhale", marks=[("x", "P")]),
      dict(pose=dict(S, head_pitch=-20), view=90, cap="Jaw clenched, chin up", marks=[("x", "head")]),
      dict(pose=dict(S, lel=(1.6, -0.2, 0), rel=(-1.6, -0.2, 0)), view=0, cap="Shoulders lift", marks=[("x", "ls"), ("x", "rs")]),
      dict(pose=S, view=90, cap="Correct", marks=[("dantien",)])]
plate("p3_8", pl)

# 3.9 Breath ladder chart
fig, ax = chart("p3_9", 4.5, 1.8)
weeks = np.arange(1, 13)
inh = [3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
exh = [3, 4, 5, 5, 6, 7, 8, 8, 9, 10, 11, 12]
ax.bar(weeks - 0.18, inh, 0.34, color="white", edgecolor=INK, hatch="////", lw=0.6, label="Inhale (seconds)")
ax.bar(weeks + 0.18, exh, 0.34, color="#8c8c8c", edgecolor=INK, lw=0.6, label="Exhale (seconds)")
ax.set_xticks(weeks); ax.set_xlabel("Week", fontsize=6.5); ax.set_ylabel("Seconds", fontsize=6.5)
ax.legend(fontsize=6, frameon=False)
save_chart(fig, "p3_9", 1)

# 3.10 Kiai and the short exhalation
Z0 = pose("zenkutsu_l", lh=(16, -38, -10), rh=(-16, -38, -10), hip_yaw=-10)
Z1 = pose("zenkutsu_l", lh=(16, -38, -10), rh=(-2, -14, 56), hip_yaw=-25)
fr = seq(Z0, Z1, 5) + [Z1, mix(Z1, Z0, 0.5), Z0]
cp = ["Ready", "Drive", "Accelerate", "Close", "Kiai: sharp exhale", "Short hold", "Release", "Recover"]
mk = [[], [], [], [], [("breath_out",), ("tension", "P")], [("tension", "P")], [], []]
plate("p3_10", [dict(pose=f, view=90, cap=c, marks=m) for f, c, m in zip(fr, cp, mk)])

# 3.11 Mokuso
SZ2 = pose(dict(lh=(6, -42, 22), rh=(-6, -42, 22), lhand="open", rhand="open"), pelvis=(0, 38, 0), la=(6, 6, -6), ra=(-6, 6, -6),
           lfy=180, rfy=180, lknee=(0, 0.2, 1), rknee=(0, 0.2, 1), head_pitch=8)
pl = [dict(pose=SZ2, view=0, cap="Mokuso"), dict(pose=SZ2, view=90, cap="Side", marks=[("dantien",)]),
      dict(pose=dict(SZ2, lean=-2), view=90, cap="Inhale"), dict(pose=dict(SZ2, lean=2), view=90, cap="Exhale")]
plate("p3_11", pl)

# 3.12 Partner check of breathing
st = pose("heiko", "kamae")
pt = pose("heiko", "down", offset=(0, 0, 66), yaw=180, rh=(0, 104, 48), rworld=True, rhand="open")
pt2 = pose("heiko", "down", offset=(0, 0, 66), yaw=180, rh=(0, 136, 46), rworld=True, rhand="open")
pt3 = pose("heiko", "down", offset=(0, 0, 66), yaw=180, rh=(0, 104, 48), lh=(0, 104, -14), rworld=True, lworld=True, rhand="open", lhand="open",
           pelvis=(0, 99, -40))
pl = [dict(figs=[st, pt], view=90, cap="Hand on abdomen"), dict(figs=[st, pt], view=90, cap="Inhale: hand moves"),
      dict(figs=[st, pt2], view=90, cap="Hand on chest: still"), dict(figs=[st, pt], view=40, cap="Three-quarter")]
plate("p3_12", pl, cols=4, pw=1.12)

# 3.13 Pressure schematics
modes2 = ["in", "out", "reverse", "neutral"]
caps2 = ["Diaphragm down", "Abdominals in", "Pelvic floor lifts", "Balanced pressure"]
arr2 = [[((0, 30), (0, 14))], [((-26, -12), (-17, -12)), ((26, -12), (17, -12))], [((0, -46), (0, -34))],
        [((0, 30), (0, 14)), ((0, -46), (0, -34)), ((-26, -12), (-17, -12)), ((26, -12), (17, -12))]]
multi("p3_13", 4, 4, lambda ax, i: torso_schematic(ax, modes2[i], arrows=arr2[i]), pw=1.12, ph=1.45, caps=caps2, xr=38)

write_count("ch03")
