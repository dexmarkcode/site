from body import *
from diag import *

HK = (16, -38, -10)
D = 82  # distance between partners


def pair(a_rh, b_rh, a_lh=HK, b_lh=HK, a="sanchin_r", b="sanchin_r", **kw):
    A = pose(a, lh=a_lh, rh=a_rh, **kw)
    B = pose(b, lh=b_lh, rh=b_rh, offset=(0, 0, D), yaw=180)
    return [A, B]


low = (-2, -40, 40); mid = (-4, -14, 40); high = (-6, 6, 36)
# 11.1 / 11.2 Three-point forearm conditioning (sanbon kote kitae)
seqA = [HK, low, low, mid, mid, high, high, HK]
seqB = [HK, low, low, mid, mid, high, high, HK]
cp = ["Ready", "Swing down", "Contact: low", "Swing up", "Contact: middle", "Swing over", "Contact: high", "Reset"]
plate("p11_1", [dict(figs=pair((-16, -38, -10) if a == HK else a, (-16, -38, -10) if b == HK else b), view=90, cap=c, zoom=1.4)
                for a, b, c in zip(seqA, seqB, cp)])
plate("p11_2", [dict(figs=pair((-16, -38, -10) if a == HK else a, (-16, -38, -10) if b == HK else b), view=55, cap=c, zoom=1.4)
                for a, b, c in zip(seqA, seqB, cp)])

# 11.3 Leg conditioning (light partner contact to thighs)
A0 = pose("sanchin_r", "kamae")
B0 = pose("sanchin_r", "kamae", offset=(0, 0, 80), yaw=180)
B1 = dict(B0, ra=(-6, 30, 40), rknee=(0, 0, 1), rfp=-20)
B2 = dict(B0, ra=(-20, 34, 54), rknee=(-1, 0, .3), rfp=-10)
B3 = dict(B0, ra=(-2, 14, 50), rknee=(0, 0, 1))
pl = [dict(figs=[A0, B0], view=90, cap="Ready"), dict(figs=[A0, B1], view=90, cap="Knee lifts"),
      dict(figs=[A0, B3], view=90, cap="Shin to thigh (light)"), dict(figs=[A0, B0], view=90, cap="Reset"),
      dict(figs=[A0, B2], view=60, cap="Outer thigh"), dict(figs=[A0, B3], view=60, cap="Front thigh"),
      dict(figs=[dict(A0, ra=(-6, 30, 40), rknee=(0, 0, 1)), B0], view=90, cap="Swap roles"),
      dict(figs=[A0, B0], view=60, cap="Bow and change")]
for d in pl: d["zoom"] = 1.45
plate("p11_3", pl)

# 11.4 Solo forearm conditioning on a post
M = (("makiwara", 52, -6),)
s = [pose("sanchin_r", lh=HK, rh=(-30, -10, 10), props=M), pose("sanchin_r", lh=HK, rh=(-16, -10, 40), props=M),
     pose("sanchin_r", lh=HK, rh=(-24, -26, 20), props=M), pose("sanchin_r", lh=HK, rh=(-14, -36, 42), props=M),
     pose("sanchin_r", lh=HK, rh=(-10, 0, 18), props=M), pose("sanchin_r", lh=HK, rh=(-16, -6, 42), props=M),
     pose("sanchin_r", lh=HK, rh=(-30, -10, 10), props=M), pose("sanchin_r", "kamae", props=M)]
plate("p11_4", [dict(pose=f, view=90, cap=c, cx=18, zoom=1.2) for f, c in zip(s, ["Arm draws back", "Outer forearm", "Draw back", "Lower forearm",
                                                                  "Rising", "Inner forearm", "Repeat", "Guard"])])

# 11.5 Self-conditioning by slapping and tapping
O = dict(lhand="open", rhand="open")
sp = [pose("heiko", lh=(-18, -6, 12), rh=(-20, -5, 28), lhand="open"), pose("heiko", lh=(20, -5, 28), rh=(18, -6, 12), rhand="open"),
      pose("heiko", lh=(-8, -28, 16), rh=(8, -28, 16), **O), pose("heiko", lh=(8, -44, 18), rh=(-8, -46, 18)),
      pose("heiko", lh=(20, -26, 4), rh=(-20, -26, 4), **O, lroll=90, rroll=-90), pose("heiko", lh=(22, -66, 10), rh=(-22, -66, 10), **O),
      pose("heiko", lh=(12, -46, -16), rh=(-12, -46, -16), **O), pose("heiko", lean=40, lh=(12, -78, 30), rh=(-12, -78, 30), **O)]
plate("p11_5", [dict(pose=f, view=20, cap=c) for f, c in zip(sp, ["Slap forearm", "Other arm", "Chest", "Fists to belly", "Ribs", "Thighs", "Lower back (light)", "Shins"])])

# 11.6 Abdominal conditioning with a partner
S = pose("sanchin_r", "kamae")
def presser(y, z=12, hand="open", dist=70):
    return pose("zenkutsu_l", offset=(0, 0, dist), yaw=180, rh=(0, y, dist - z), rworld=True, rhand=hand)
pl = [dict(figs=[S, presser(100)], view=90, cap="Palm rests"), dict(figs=[S, presser(100)], view=90, cap="Press on exhale", marks=[("breath_out",)]),
      dict(figs=[S, presser(100, 14, "fist")], view=90, cap="Fist rests"), dict(figs=[S, presser(100, 14, "fist")], view=90, cap="Light push"),
      dict(figs=[S, presser(108, 14, "fist")], view=90, cap="Upper abdomen"), dict(figs=[S, presser(100, 16, "fist")], view=90, cap="Light tap"),
      dict(figs=[S, presser(100, 16)], view=55, cap="Obliques (palm)"), dict(figs=[S, presser(160)], view=90, cap="Recover: breathe")]
for d in pl: d["zoom"] = 1.35
plate("p11_6", pl)

# 11.7 Makiwara progression
MK = (("makiwara", 70, 0),)
m0 = pose("zenkutsu_l", lh=(14, -20, 36), rh=(-16, -38, -10), props=MK)
m1 = dict(m0, rh=(0, -10, 58), lh=(16, -38, -10), hip_yaw=-28)
pl = [dict(pose=dict(m0, rh=(0, -10, 54), lh=HK), view=90, cap="Touch: alignment"), dict(pose=dict(m0, rh=(0, -10, 54), lh=HK), view=90, cap="Press: hold 3 s"),
      dict(pose=m1, view=90, cap="Light strike"), dict(pose=m1, view=90, cap="Medium strike"),
      dict(pose=dict(m1, rhand="open", rroll=90), view=90, cap="Palm heel"), dict(pose=dict(m1, rh=(-2, -12, 52)), view=90, cap="Close range"),
      dict(pose=dict(m0, rh=(-6, 10, 50), hip_yaw=-20), view=90, cap="Rising strike"), dict(pose=m0, view=90, cap="Rest the hand")]
for d in pl: d.update(cx=24, zoom=1.3)
plate("p11_7", pl)

# 11.8 Conditioning intensity over a year
fig, ax = chart("p11_8", 4.5, 1.9)
mth = np.arange(0, 13)
ax.plot(mth, np.clip(0.5 + mth * 0.28, 0, 3.6), color=INK, lw=1.2, marker="o", ms=3, label="Forearm (kote kitae)")
ax.plot(mth, np.clip(-0.5 + mth * 0.26, 0, 3.2), color=INK, lw=1.0, ls="--", marker="s", ms=3, label="Makiwara")
ax.plot(mth, np.clip(-1.2 + mth * 0.25, 0, 2.6), color=INK, lw=0.9, ls=":", marker="^", ms=3, label="Legs and body")
ax.set_xticks(mth); ax.set_xlabel("Months", fontsize=6.5)
ax.set_yticks([0, 1, 2, 3], ["none", "light", "moderate", "firm"])
ax.legend(fontsize=5.8, frameon=False, loc="upper left")
save_chart(fig, "p11_8", 1)

# 11.9 After-care
cr = [pose("heiko", lh=(-14, -24, 18), rh=(-20, -26, 30), lhand="open"), pose("heiko", lh=(20, -26, 30), rh=(14, -24, 18), rhand="open"),
      pose("heiko", lh=(30, -50, 10), rh=(-30, -50, 10), **O), pose("heiko", lh=(14, 10, 20), rh=(-14, 10, 20), **O),
      pose("heiko", lh=(4, -20, 26), rh=(-4, -20, 26), **O, lroll=90, rroll=-90), pose("heiko", lh=(14, -24, 30), rh=(-14, -24, 30), **O, lroll=180, rroll=-180),
      pose("heiko", lh=(10, -40, 18), rh=(-10, -40, 18)), pose("heiko", "down", **O)]
plate("p11_9", [dict(pose=f, view=25, cap=c) for f, c in zip(cr, ["Stroke forearm", "Other arm", "Shake out", "Arms up", "Palms press", "Wrist stretch", "Gentle fists", "Rest"])])

# 11.10 Conditioning faults
pl = [dict(figs=pair((-6, 6, 36), (-6, 6, 36), a_lh=HK), view=90, cap="Wrist bone contact", marks=[("x", "rw")], zoom=1.4),
      dict(figs=pair((-2, -40, 40), (-2, -40, 40)), view=90, cap="Elbow contact", marks=[("x", "re")], zoom=1.4),
      dict(figs=[dict(S, lean=14), presser(100, 14, "fist")], view=90, cap="Flinching forward", marks=[("x", "N")], zoom=1.35),
      dict(figs=[S, presser(100, 14, "fist")], view=90, cap="Struck on inhale", marks=[("breath_in",), ("x", "navel")], zoom=1.35),
      dict(pose=dict(m1, rh=(0, -18, 50)), view=90, cap="Bent wrist", marks=[("x", "rw")], cx=24, zoom=1.3),
      dict(pose=dict(m1, lean=16), view=90, cap="Leaning into post", marks=[("x", "N")], cx=24, zoom=1.3),
      dict(figs=[A0, dict(B0, ra=(-2, 40, 56), rknee=(0, 0, 1))], view=90, cap="Kick to knee", marks=[("x", "rk")], zoom=1.45),
      dict(pose=pose("heiko", lh=(12, -20, 30), rh=(-12, -20, 30)), view=20, cap="Training when bruised", marks=[("x", "rw"), ("x", "lw")])]
plate("p11_10", pl)

# 11.11 Conditioning surfaces
pl = [dict(pose=dict(pose("sanchin_r", "kamae")), view=0, cap="Forearms: muscle", marks=[("ring", "le", 9), ("ring", "re", 9)]),
      dict(pose=pose("sanchin_r", "kamae"), view=90, cap="Thighs: muscle", marks=[("ring", "rk", 10)]),
      dict(pose=pose("sanchin_r", "kamae"), view=0, cap="Abdomen", marks=[("ring", "navel", 11)]),
      dict(pose=pose("sanchin_r", "kamae"), view=0, cap="Avoid joints", marks=[("x", "lk"), ("x", "rk"), ("x", "lw"), ("x", "rw")])]
plate("p11_11", pl)

# 11.12 Footwork for partner conditioning (top view)
FP = [dict(feet=[(-16, -20, 24, "r"), (16, -41, -12, "l"), (16, 20, 204, "r", "ghost"), (-16, 41, 168, "l", "ghost")], cap="Facing, right fwd", xr=50),
      dict(feet=[(-16, -20, 24, "r"), (16, -41, -12, "l"), (16, 20, 204, "r", "ghost"), (-16, 41, 168, "l", "ghost")], cap="Arms meet centre", xr=50, texts=[(0, 0, "×", 12)]),
      dict(feet=[(16, -20, -24, "l"), (-16, -41, 12, "r"), (-16, 20, 156, "l", "ghost"), (16, 41, 192, "r", "ghost")], cap="Change sides", xr=50),
      dict(feet=[(16, -10, -24, "l"), (-16, -31, 12, "r"), (-16, 10, 156, "l", "ghost"), (16, 31, 192, "r", "ghost")], cap="Step in closer", xr=50)]
footplate("p11_12", FP, ph=1.4)

write_count("ch11")
