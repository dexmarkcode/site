from body import *
from diag import *
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OPEN_THIGH = dict(lh=(12, -60, 9), rh=(-12, -60, 9), lhand="open", rhand="open", lroll=90, rroll=-90)

# 1.1 Rei — standing bow
a = pose("musubi", OPEN_THIGH)
b = pose("musubi", OPEN_THIGH, lean=30, head_pitch=12, lh=(11, -58, 14), rh=(-11, -58, 14))
frames = seq(a, b, 4) + seq(b, a, 5)[1:]
caps = ["Attention", "Begin the bow", "Hinge at hips", "Lowest point", "Pause", "Rise", "Rise", "Upright"]
plate("p1_1", [dict(pose=f, view=80, cap=c) for f, c in zip(frames, caps)])

# 1.2 Formal opening
s0 = pose("musubi", OPEN_THIGH)
s1 = pose("musubi", lh=(-6, -46, 20), rh=(6, -48, 18), lhand="open", rhand="open")
s2 = pose("musubi", lh=(-4, -30, 24), rh=(4, -32, 22), lhand="open", rhand="open")
s3 = pose("musubi", lh=(-6, -46, 20), rh=(6, -48, 18), lhand="open", rhand="open")
s4 = pose("hachiji", "ready")
s5 = pose("hachiji", lh=(14, -58, 14), rh=(-14, -58, 14))
pl = [dict(pose=s0, cap="Musubi dachi"), dict(pose=s1, cap="Hands cross"), dict(pose=s2, cap="Lift, inhale"),
      dict(pose=s3, cap="Lower, exhale"), dict(pose=mix(s3, s4, 0.5), cap="Step out"), dict(pose=s4, cap="Fists close"),
      dict(pose=s5, cap="Yoi"), dict(pose=s5, view=90, cap="Yoi, side")]
plate("p1_2", pl)

# 1.3 Go and Ju contrasts
G1 = pose("sanchin_r", "kamae", marks=None) if False else pose("sanchin_r", "kamae")
pl = [
    dict(pose=pose("sanchin_r", "kamae"), cap="Go: closed guard", marks=[("tension", "le"), ("tension", "re")]),
    dict(pose=pose("sanchin_r", "kamae", lhand="open", rhand="open"), cap="Ju: open guard"),
    dict(pose=pose("sanchin_r", rh=(-2, -16, 56), lh=(16, -38, -10)), view=90, cap="Go: straight punch",
         marks=[("arrow", "rw", 25, 0)]),
    dict(pose=pose("sanchin_r", rh=(-6, -12, 42), lh=(16, -38, -10), rhand="open", rroll=90), view=90, cap="Ju: palm heel",
         marks=[("arrow", "rw", 18, -8, -0.4)]),
    dict(pose=pose("zenkutsu_l", lh=(16, 4, 30), rh=(-16, -38, -10), hip_yaw=-15), view=45, cap="Go: forearm block"),
    dict(pose=pose("neko_l", lh=(14, 0, 34), rh=(-12, -30, 22), lhand="open", rhand="open", hip_yaw=-20), view=45, cap="Ju: hooking hand"),
    dict(pose=pose("shiko", "kamae"), cap="Go: rooted"),
    dict(pose=pose("neko_l", lh=(10, -10, 30), rh=(-10, -20, 26), lhand="open", rhand="open"), view=90, cap="Ju: evasive"),
]
plate("p1_3", pl)

# 1.4 Representative postures of the Goju-Ryu kata
K = [
    (pose("sanchin_r", "kamae"), 0, "Sanchin"),
    (pose("sanchin_r", rh=(-8, -8, 40), lh=(16, -38, -10), rhand="open", rroll=90), 30, "Tensho"),
    (pose("zenkutsu_l", lh=(4, 22, 24), rh=(-16, -38, -10), lel=(1, 0.3, 0.2), hip_yaw=-10), 60, "Gekisai Dai Ichi"),
    (pose("neko_l", lh=(14, 0, 34), rh=(-16, -38, -8), lhand="open", hip_yaw=-15), 60, "Gekisai Dai Ni"),
    (pose("shiko", rh=(-6, -30, 30), lh=(0, -22, 26), lhand="open"), 20, "Saifa"),
    (pose("shiko", lh=(22, -34, 22), rh=(-22, -8, 18), rhand="open"), 0, "Seiyunchin"),
    (pose("sanchin_l", lh=(6, -12, 52), rh=(-16, -38, -10), lhand="open"), 70, "Shisochin"),
    (pose("sagi_l", "kamae"), 70, "Sanseru"),
    (pose("neko_r", lh=(16, 10, 30), rh=(-10, -30, 30), lhand="open", rhand="open"), 40, "Seipai"),
    (pose("neko_l", lh=(8, -2, 36), rh=(-8, -26, 36), lhand="open", rhand="open"), 50, "Kururunfa"),
    (pose("sanchin_l", lh=(4, -14, 52), rh=(-16, -38, -10)), 80, "Seisan"),
    (pose("shiko", lh=(8, -14, 50), rh=(-8, -14, 50), lhand="open", rhand="open"), 30, "Suparinpei"),
]
plate("p1_4", [dict(pose=p, view=v, cap=c) for p, v, c in K])

# 1.5 Equipment of hojo undo
names = list(EQUIP)
multi("p1_5", len(names), 3, lambda ax, i: EQUIP[names[i]](ax), pw=1.5, ph=1.1, caps=names, xr=45)

# 1.6 Lineage diagram
fig, ax = plt.subplots(figsize=(4.5, 3.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 76); ax.axis("off")
def bx(x, y, w, h, t, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc="white", ec=INK, lw=1.2 if bold else 0.7))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=6.3, fontweight="semibold" if bold else "normal", linespacing=1.15)
def ln(x1, y1, x2, y2, dash=False):
    ax.plot([x1, x2], [y1, y2], color=INK, lw=0.7, ls=(0, (2, 1.5)) if dash else "-")
bx(30, 66, 40, 8, "Fujian (Fuzhou) boxing traditions\n(teachers recorded in oral history)")
ln(50, 66, 50, 61, True)
bx(32, 53, 36, 8, "Higaonna Kanryō\n(1853–1915)", True)
ln(50, 53, 50, 48); ln(16, 48, 84, 48)
ln(16, 48, 16, 45); ln(50, 48, 50, 45); ln(84, 48, 84, 45)
bx(2, 37, 28, 8, "Kyoda Jūhatsu\n(Tōon-ryū)")
bx(34, 37, 32, 8, "Miyagi Chōjun\n(1888–1953)", True)
bx(70, 37, 28, 8, "Higa Seikō\n(also under Miyagi)")
ln(50, 37, 50, 31); ln(10, 31, 90, 31)
for x, t in ((10, "Yagi Meitoku"), (30, "Miyazato Ei'ichi"), (50, "Toguchi Seikichi"), (70, "Higa Seikō"), (90, "Yamaguchi Gōgen\n(mainland Japan)")):
    ln(x, 31, x, 27)
    bx(x - 9.5, 18, 19, 9, t)
ln(10, 18, 10, 13, True); ln(90, 18, 90, 13, True); ln(50, 18, 50, 13, True)
ax.text(50, 7, "Modern associations in Okinawa, Japan and worldwide\n(only a selection of lines is shown)", ha="center", va="center", fontsize=6.0, style="italic")
save_chart(fig, "p1_6", 1)

# 1.7 How to read the plates
base = pose("sanchin_r", "kamae")
pl = [dict(pose=base, view=0, cap="Front view"), dict(pose=base, view=90, cap="Side view"),
      dict(pose=base, view=40, cap="Three-quarter"), dict(pose=base, view=180, cap="Back view"),
      dict(pose=base, view=0, cap="Root lines", marks=[("root", "la", "ra")]),
      dict(pose=base, view=90, cap="Centre (tanden)", marks=[("dantien",)]),
      dict(pose=base, view=0, cap="Held tension", marks=[("tension", "le"), ("tension", "re"), ("tension", "P")]),
      dict(pose=pose("sanchin_r", rh=(-2, -16, 56), lh=(16, -38, -10)), view=90, cap="Motion arrow",
           marks=[("arrow", "rw", 22, 0)])]
plate("p1_7", pl)

# 1.8 Seiza and za-rei
st = pose("musubi", OPEN_THIGH)
k1 = pose(OPEN_THIGH, pelvis=(0, 60, -6), la=(8, 8, 18), ra=(-8, 7, -42), lfy=-5, rfy=180,
          lknee=(0, 0, 1), rknee=(0, -1, 0.6), lh=(12, -38, 22), rh=(-12, -44, 14))
k2 = pose(OPEN_THIGH, pelvis=(0, 52, -4), la=(8, 7, -40), ra=(-8, 7, -40), lfy=180, rfy=180,
          lknee=(0, -1, 0.7), rknee=(0, -1, 0.7), lh=(10, -36, 26), rh=(-10, -36, 26))
sz = pose(OPEN_THIGH, pelvis=(0, 38, 0), la=(6, 6, -6), ra=(-6, 6, -6), lfy=180, rfy=180,
          lknee=(0, 0.2, 1), rknee=(0, 0.2, 1), lh=(12, -32, 30), rh=(-12, -32, 30))
bw = dict(sz, lean=38, head_pitch=10, lh=(10, -58, 46), rh=(-10, -58, 46))
pl = [dict(pose=st, view=90, cap="Stand"), dict(pose=k1, view=90, cap="Left knee down"),
      dict(pose=k2, view=90, cap="Both knees"), dict(pose=sz, view=90, cap="Seiza"),
      dict(pose=sz, view=0, cap="Seiza, front"), dict(pose=mix(sz, bw, 0.5), view=90, cap="Hands forward"),
      dict(pose=bw, view=90, cap="Za-rei"), dict(pose=sz, view=90, cap="Return")]
plate("p1_8", pl)

# 1.9 Hard and soft inside one punch
h0 = pose("sanchin_r", "kamae", rh=(-16, -38, -10))
h1 = pose("sanchin_r", "kamae", rh=(-8, -26, 24))
h2 = pose("sanchin_r", "kamae", rh=(-2, -16, 56))
caps = ["Chamber", "Relaxed travel", "Travel", "Impact: tense", "Hold", "Release", "Return", "Guard"]
frames = [h0, mix(h0, h1, 0.5), h1, h2, h2, mix(h2, h1, 0.3), h1, h0]
marks = [[], [], [], [("tension", "rw"), ("tension", "P")], [("tension", "re")], [], [("arrow", "rw", -16, -6)], []]
plate("p1_9", [dict(pose=f, view=90, cap=c, marks=m) for f, c, m in zip(frames, caps, marks)])

# 1.10 Common beginner faults
S = pose("sanchin_r", "kamae")
F = [(dict(S, lean=16), 90, "Leaning forward"), (dict(S, lean=-10), 90, "Leaning back"),
     (dict(S, pelvis=(0, 99, 0)), 90, "Knees locked"), (dict(S, la=(30, 8, -10), ra=(-30, 8, 11)), 0, "Feet too wide"),
     (dict(S, head_pitch=28), 90, "Head dropped"), (dict(S, head_pitch=-22), 90, "Chin lifted"),
     (dict(S, hip_yaw=28), 0, "Hips twisted"), (dict(S, lel=(1.6, -0.3, 0), rel=(-1.6, -0.3, 0)), 0, "Elbows flared")]
plate("p1_10", [dict(pose=p, view=v, cap=c) for p, v, c in F])

# 1.11 Shape of a balanced training week
fig, ax = chart("p1_11", 4.5, 1.9)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
kata = [25, 15, 25, 15, 25, 35, 0]; hojo = [10, 25, 10, 25, 10, 15, 0]; partner = [0, 20, 0, 20, 0, 30, 0]; breath = [10, 10, 10, 10, 10, 10, 15]
x = np.arange(7)
b1 = ax.bar(x, breath, 0.62, color="white", edgecolor=INK, hatch="....", lw=0.6, label="Breath and Sanchin")
b2 = ax.bar(x, kata, 0.62, bottom=breath, color="#d0d0d0", edgecolor=INK, lw=0.6, label="Kata and basics")
bot = np.array(breath) + np.array(kata)
b3 = ax.bar(x, hojo, 0.62, bottom=bot, color="white", edgecolor=INK, hatch="////", lw=0.6, label="Hojo undo")
b4 = ax.bar(x, partner, 0.62, bottom=bot + np.array(hojo), color="#6a6a6a", edgecolor=INK, lw=0.6, label="Partner work")
ax.set_xticks(x, days); ax.set_ylabel("Minutes", fontsize=6.5)
ax.legend(fontsize=5.8, frameon=False, ncol=2, loc="upper left")
ax.set_ylim(0, 100)
save_chart(fig, "p1_11", 1)

write_count("ch01")
