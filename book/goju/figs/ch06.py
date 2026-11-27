from body import *
from diag import *

S = pose("sanchin_r", "kamae")
PUNCH = pose("sanchin_r", "kamae", rh=(-3, -16, 56))


def behind(l, r, dist=60, stance="hachiji", **kw):
    """Tester standing behind the student, hands at world points l and r."""
    L = (l[0], l[1], l[2] + dist) if l else (23, -60, 2)
    R = (r[0], r[1], r[2] + dist) if r else (-23, -60, 2)
    kw = {**dict(lhand="open", rhand="open"), **kw}
    return pose(stance, offset=(0, 0, -dist), yaw=0, lh=L, rh=R, lworld=bool(l), rworld=bool(r), **kw)


def front(l, r, dist=68, stance="hachiji", **kw):
    L = (-l[0], l[1], dist - l[2]) if l else (23, -60, 2)
    R = (-r[0], r[1], dist - r[2]) if r else (-23, -60, 2)
    kw = {**dict(lhand="open", rhand="open"), **kw}
    return pose(stance, offset=(0, 0, dist), yaw=180, lh=L, rh=R, lworld=bool(l), rworld=bool(r), **kw)


def side(l, r, dist=62, **kw):
    """Tester at the student's left side, facing the student (yaw -90)."""
    G = ry(90)  # inverse of yaw -90
    def loc(p):
        return tuple(G @ (np.array(p, float) - np.array([dist, 0, 0])))
    return pose("hachiji", offset=(dist, 0, 0), yaw=-90, lh=loc(l) if l else (23, -60, 2), rh=loc(r) if r else (-23, -60, 2),
                lworld=bool(l), rworld=bool(r), lhand="open", rhand="open", **kw)


SH_L, SH_R = (19, 140, 0), (-19, 140, 0)
# 6.1 Tester positions
pl = [dict(figs=[S, behind(SH_L, SH_R)], view=90, cap="Behind (side view)"),
      dict(figs=[S, behind(SH_L, SH_R)], view=180, cap="Behind (rear view)"),
      dict(figs=[S, front(None, None)], view=90, cap="In front"),
      dict(figs=[S, side(None, None)], view=0, cap="At the side"),
      dict(figs=[S, behind(SH_L, SH_R)], view=45, cap="Three-quarter"),
      dict(figs=[S, front((6, 104, 12), None)], view=90, cap="Front, hand ready"),
      dict(figs=[S, side((20, 125, 2), None)], view=0, cap="Side, hand on ribs"),
      dict(figs=[S, behind((16, 124, -8), (-16, 124, -8))], view=150, cap="Hands on back")]
plate("p6_1", pl, pw=1.25)

# 6.2 Shoulder press
up = behind((19, 152, 0), (-19, 152, 0))
on = behind(SH_L, SH_R)
dn = behind((19, 137, 0), (-19, 137, 0), pelvis=(0, 94, 0))
pl = [dict(figs=[S, up], view=90, cap="Hands above"), dict(figs=[S, on], view=90, cap="Rest on shoulders"),
      dict(figs=[S, dn], view=90, cap="Press down"), dict(figs=[S, dn], view=90, cap="Student holds", marks=[("root", "la", "ra")]),
      dict(figs=[S, on], view=180, cap="Rear view"), dict(figs=[S, dn], view=180, cap="Press, rear"),
      dict(figs=[dict(S, lean=8), dn], view=90, cap="Fault: folding", marks=[("x", "N")]),
      dict(figs=[dict(S, pelvis=(0, 85, 0)), dn], view=90, cap="Fault: knees give", marks=[("x", "rk")])]
plate("p6_2", pl, pw=1.25)

# 6.3 Back and latissimus checks
pl = [dict(figs=[PUNCH, behind((17, 124, -10), (-17, 124, -10))], view=150, cap="Palms on lats"),
      dict(figs=[PUNCH, behind((17, 124, -6), (-17, 124, -6))], view=150, cap="Slap as punch lands"),
      dict(figs=[S, behind((17, 124, -8), None)], view=180, cap="One side"),
      dict(figs=[S, behind(None, (-17, 124, -8))], view=180, cap="Other side"),
      dict(figs=[S, behind((6, 138, -10), (-6, 138, -10))], view=180, cap="Between blades"),
      dict(figs=[S, behind((14, 104, -10), (-14, 104, -10))], view=180, cap="Lower back muscles"),
      dict(figs=[PUNCH, behind((17, 124, -6), (-17, 124, -6))], view=90, cap="Side view"),
      dict(figs=[S, behind((16, 98, -12), (-16, 98, -12))], view=180, cap="Buttocks")]
plate("p6_3", pl, pw=1.25)

# 6.4 Abdominal checks
pl = [dict(figs=[S, front((0, 104, 12), None)], view=90, cap="Fingertip touch"),
      dict(figs=[S, front((0, 104, 12), None)], view=60, cap="Flat palm press"),
      dict(figs=[S, front((0, 104, 14), None, rhand="fist")], view=90, cap="Light palm strike"),
      dict(figs=[S, front((0, 112, 14), None)], view=90, cap="Upper abdomen"),
      dict(figs=[S, front((10, 102, 12), None)], view=0, cap="Side of belly"),
      dict(figs=[S, front((0, 104, 14), None, lhand="fist")], view=90, cap="Fist (advanced)"),
      dict(figs=[dict(S, lean=10), front((0, 104, 14), None)], view=90, cap="Fault: doubling up", marks=[("x", "N")]),
      dict(figs=[S, front((0, 104, 14), None)], view=90, cap="Strike on exhale", marks=[("breath_out",)])]
plate("p6_4", pl, pw=1.25)

# 6.5 Leg checks
crouch = dict(pelvis=(0, 70, 0), lknee=(0.3, 0, 1), rknee=(-0.3, 0, 1))
pl = [dict(figs=[S, front((-16, 70, 14), (16, 70, 0), **crouch)], view=60, cap="Hands on thighs"),
      dict(figs=[S, front((-14, 58, 20), (14, 56, 2), **crouch)], view=60, cap="Knees outward"),
      dict(figs=[S, front((-24, 58, 20), (24, 56, 2), **crouch)], view=60, cap="Knees inward"),
      dict(figs=[S, front((-16, 72, 16), None, **crouch)], view=90, cap="Slap front thigh"),
      dict(figs=[S, side((20, 72, -8), None, **crouch)], view=0, cap="Slap outer thigh"),
      dict(figs=[S, behind((16, 66, -14), (-16, 66, -14), **crouch)], view=120, cap="Back of thighs"),
      dict(figs=[S, front((-10, 40, 22), None, **crouch)], view=90, cap="Calf / shin check"),
      dict(figs=[dict(S, lknee=(1, 0, .5), rknee=(-1, 0, .5)), front((-14, 58, 20), (14, 56, 2), **crouch)], view=60, cap="Fault: knees open", marks=[("x", "lk")])]
plate("p6_5", pl, pw=1.25)

# 6.6 Arm checks
pl = [dict(figs=[S, front((-20, 140, 26), None)], view=90, cap="Press the fist back"),
      dict(figs=[S, front((-20, 128, 20), None)], view=90, cap="Forearm strike"),
      dict(figs=[S, side((22, 126, 16), None)], view=0, cap="Elbow inward test"),
      dict(figs=[S, front((-20, 128, 20), (20, 128, 20))], view=60, cap="Both forearms"),
      dict(figs=[PUNCH, front((-3, 136, 52), None)], view=90, cap="Press extended fist"),
      dict(figs=[PUNCH, front((-3, 132, 40), None)], view=90, cap="Strike extended arm"),
      dict(figs=[PUNCH, side((-6, 134, 36), None)], view=0, cap="Side push on arm"),
      dict(figs=[dict(PUNCH, rh=(-3, -10, 44)), front((-3, 136, 40), None)], view=90, cap="Fault: arm folds", marks=[("x", "re")])]
plate("p6_6", pl, pw=1.25)

# 6.7 Push tests
pl = [dict(figs=[S, front((0, 136, 12), None, stance="zenkutsu_l")], view=90, cap="Push to chest"),
      dict(figs=[S, front((10, 134, 12), (-10, 134, 12), stance="zenkutsu_l")], view=90, cap="Two-hand push"),
      dict(figs=[S, side((20, 134, 0), None)], view=0, cap="Side push"),
      dict(figs=[S, behind((16, 138, -8), (-16, 138, -8))], view=90, cap="Pull from behind"),
      dict(figs=[S, front((0, 100, 12), None, stance="zenkutsu_l", pelvis=(0, 76, 8))], view=90, cap="Low push (hips)"),
      dict(figs=[S, side((20, 100, 0), None, pelvis=(0, 90, 0))], view=0, cap="Side push (hips)"),
      dict(figs=[dict(S, lean=-8), front((0, 136, 12), None, stance="zenkutsu_l")], view=90, cap="Fault: lean back", marks=[("x", "P")]),
      dict(figs=[S, front((0, 136, 12), None, stance="zenkutsu_l")], view=90, cap="Push goes to ground", marks=[("root", "la", "ra")])]
plate("p6_7", pl, pw=1.25)

# 6.8 Targets
safe = [("ring", "ls", 7), ("ring", "rs", 7), ("ring", "navel", 9), ("ring", "rk", 7), ("ring", "lk", 7)]
pl = [dict(pose=S, view=0, cap="Front: safe areas", marks=[("ring", "ls", 8), ("ring", "rs", 8), ("ring", "navel", 10), ("ring", "chest", 9)]),
      dict(pose=S, view=180, cap="Back: safe areas", marks=[("ring", "le", 9), ("ring", "re", 9), ("ring", "ls", 8), ("ring", "rs", 8)]),
      dict(pose=S, view=0, cap="Front: never strike", marks=[("x", "head"), ("x", "N"), ("x", (0, 86))]),
      dict(pose=S, view=180, cap="Back: never strike", marks=[("x", "head"), ("x", "N"), ("x", (12, 108)), ("x", (-12, 108))])]
plate("p6_8", pl)

# 6.9 Shime progression chart
fig, ax = chart("p6_9", 4.5, 1.9)
m = np.arange(1, 13)
press = np.clip(np.linspace(1, 3.5, 12), 0, 5)
slap = np.clip(np.linspace(-1, 3.2, 12), 0, 5)
strike = np.clip(np.linspace(-3, 2.6, 12), 0, 5)
ax.plot(m, press, color=INK, lw=1.2, marker="o", ms=3, label="Pressing and pushing")
ax.plot(m, slap, color=INK, lw=1.0, ls="--", marker="s", ms=3, label="Open-hand slaps")
ax.plot(m, strike, color=INK, lw=0.9, ls=":", marker="^", ms=3, label="Light fist strikes (trunk only)")
ax.set_xticks(m); ax.set_xlabel("Month of training", fontsize=6.5)
ax.set_yticks([0, 1, 2, 3, 4], ["none", "very light", "light", "moderate", "firm"])
ax.legend(fontsize=5.8, frameon=False, loc="upper left")
save_chart(fig, "p6_9", 1)

# 6.10 Self-shime
pl = [dict(pose=pose("sanchin_r", lh=(8, -44, 18), rh=(-8, -46, 18), lhand="open", rhand="open"), view=90, cap="Palms on belly"),
      dict(pose=pose("sanchin_r", lh=(8, -44, 22), rh=(-8, -46, 22)), view=90, cap="Fists tap belly"),
      dict(pose=pose("sanchin_r", lh=(18, -26, 4), rh=(-18, -26, 4), lhand="open", rhand="open"), view=0, cap="Hands on ribs"),
      dict(pose=pose("sanchin_r", lh=(22, -66, 10), rh=(-22, -66, 16), lhand="open", rhand="open"), view=0, cap="Slap thighs"),
      dict(pose=pose("sanchin_r", lh=(-16, -6, 14), rh=(-20, -5, 28), lhand="open"), view=0, cap="Check opposite arm"),
      dict(pose=pose("sanchin_r", lh=(-16, -2, 4), rh=(-20, -5, 28), lhand="open"), view=0, cap="Squeeze shoulder"),
      dict(pose=pose("sanchin_r", lh=(10, -46, -16), rh=(-10, -46, -16), lhand="open", rhand="open"), view=180, cap="Back of waist"),
      dict(pose=S, view=0, cap="Recheck guard")]
plate("p6_10", pl)

# 6.11 Tester faults
pl = [dict(figs=[S, front((0, 104, 14), (0, 104, 14))], view=90, cap="Straight-arm jab", marks2=[("x", "re")]),
      dict(figs=[S, behind((12, 108, -10), None)], view=180, cap="Strikes kidneys", marks=[("x", (12, 108))]),
      dict(figs=[S, front((0, 104, 14), None)], view=90, cap="Strike on inhale", marks=[("breath_in",), ("x", "navel")]),
      dict(figs=[S, front((0, 168, 8), None)], view=90, cap="Near the head", marks=[("x", "head")]),
      dict(figs=[S, front((0, 84, 10), None, pelvis=(0, 80, 0))], view=90, cap="Low to groin", marks=[("x", (14, 86))]),
      dict(figs=[S, behind((0, 140, -10), None)], view=180, cap="On the spine", marks=[("x", "N")]),
      dict(figs=[S, front((-16, 46, 18), None, pelvis=(0, 70, 0))], view=90, cap="On the kneecap", marks=[("x", "rk")]),
      dict(figs=[S, front((0, 104, 14), (0, 120, 14))], view=90, cap="Without warning", marks=[("x", "head")])]
plate("p6_11", pl, pw=1.25)

# 6.12 Walk-around (top view)
def walk(ang):
    a = math.radians(ang)
    x, z = 60 * math.sin(a), 60 * math.cos(a)
    return [(-16, 11, 24, "r"), (16, -10, -12, "l"),
            (x - 8 * math.cos(a), z + 8 * math.sin(a), ang + 180, "r", "ghost"), (x + 8 * math.cos(a), z - 8 * math.sin(a), ang + 180, "l", "ghost")]
FP = [dict(feet=walk(a), cap=c, xr=78, texts=[(0, -78 * 1.2 * 0.85, "")]) for a, c in ((0, "Front"), (-90, "Left side"), (180, "Behind"), (90, "Right side"))]
footplate("p6_12", FP, ph=1.3)

write_count("ch06")
