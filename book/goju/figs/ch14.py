from body import *
from diag import *

HK = (16, -38, -10)
D = 76
PUSH = (0, -10, 44); MID = (-4, -10, 36); YIELD = (-8, -12, 26)
HI = (-6, 0, 34); LO = (-4, -22, 34)


def A(rh, lh=(14, -24, 20), hy=0, st="sanchin_r", **kw):
    kw = {**dict(rhand="open", lhand="open"), **kw}
    return pose(st, rh=rh, lh=lh, hip_yaw=hy, **kw)


def B(rh, lh=(14, -24, 20), hy=0, st="sanchin_r", **kw):
    kw = {**dict(rhand="open", lhand="open"), **kw}
    return pose(st, rh=rh, lh=lh, hip_yaw=hy, offset=(0, 0, D), yaw=180, **kw)


cyc = [(MID, MID, 0, 0, "Contact"), (PUSH, YIELD, -10, 12, "A pushes, B yields"), (PUSH, YIELD, -10, 18, "B turns waist"),
       (HI, HI, 0, 8, "B circles over"), (YIELD, PUSH, 12, -10, "B pushes, A yields"), (YIELD, PUSH, 18, -10, "A turns"),
       (LO, LO, 8, 0, "A circles under"), (MID, MID, 0, 0, "Contact again")]
plate("p14_1", [dict(figs=[A(a, hy=ha), B(b, hy=hb)], view=90, cap=c, zoom=1.4) for a, b, ha, hb, c in cyc])
plate("p14_2", [dict(figs=[A(a, hy=ha), B(b, hy=hb)], view=55, cap=c, zoom=1.4) for a, b, ha, hb, c in cyc])

# 14.3 Footwork from above
FP = [dict(feet=[(-16, -27, 24, "r"), (16, -48, -12, "l"), (16, 27, 204, "r", "ghost"), (-16, 48, 168, "l", "ghost")], cap="Right foot forward", xr=56),
      dict(feet=[(-16, -27, 24, "r"), (16, -48, -12, "l"), (16, 27, 204, "r", "ghost"), (-16, 48, 168, "l", "ghost")], cap="Contact at centre", xr=56, texts=[(0, 0, "×", 12)]),
      dict(feet=[(-16, -17, 24, "r"), (16, -38, -12, "l"), (16, 37, 204, "r", "ghost"), (-16, 58, 168, "l", "ghost")], cap="A steps in, B back", xr=56),
      dict(feet=[(16, -27, -24, "l"), (-16, -48, 12, "r"), (-16, 27, 156, "l", "ghost"), (16, 48, 192, "r", "ghost")], cap="Left side", xr=56)]
footplate("p14_3", FP, ph=1.4)

# 14.4 Listening and yielding to a push
fr = [(MID, MID, 0, 0, "Listening"), (YIELD, PUSH, 0, -6, "Push arrives"), (YIELD, PUSH, 15, -6, "Waist turns"),
      ((-14, -12, 22), PUSH, 25, -6, "Push slides past"), ((-10, -6, 30), (4, -10, 50), 20, -12, "B over-extends"),
      ((-6, -10, 40), (4, -10, 50), 0, -12, "A takes the line"), (PUSH, YIELD, -10, 10, "A returns push"), (MID, MID, 0, 0, "Reset")]
plate("p14_4", [dict(figs=[A(a, hy=ha), B(b, hy=hb, lean=6 if "over" in c else 0)], view=90, cap=c, zoom=1.4) for a, b, ha, hb, c in fr])

# 14.5 From kakie to control
fr = [(MID, MID, "Contact"), (YIELD, PUSH, "Feel the push"), ((-10, -16, 26), PUSH, "Hand turns"),
      ((-8, -20, 20), (0, -16, 40), "Grasp wrist"), ((-8, -26, 6), (0, -20, 30), "Draw in"),
      ((-8, -26, 6), (0, -20, 30), "Other hand to elbow"), ((-10, -36, 14), (0, -30, 30), "Press down"), ((-10, -36, 14), (0, -30, 30), "Control")]
pl = []
for i, (a, b, c) in enumerate(fr):
    lh = (6, -16, 34) if i >= 5 else (14, -24, 20)
    pl.append(dict(figs=[A(a, lh=lh), B(b, lean=10 if i >= 6 else 0)], view=90, cap=c, zoom=1.4))
plate("p14_5", pl)

# 14.6 Faults
pl = [dict(figs=[A(PUSH, lean=14), B(YIELD)], view=90, cap="Leaning in", marks=[("x", "N")], zoom=1.4),
      dict(figs=[A((-2, 0, 30), lel=(-1.5, 0.2, 0)), B(MID)], view=55, cap="Elbow lifted", marks=[("x", "re")], zoom=1.4),
      dict(figs=[A(MID, lhand="fist", rhand="fist"), B(MID)], view=90, cap="Hands clenched", marks=[("x", "rw")], zoom=1.4),
      dict(figs=[A((0, -10, 54)), B(YIELD)], view=90, cap="Arm locked", marks=[("x", "re")], zoom=1.4),
      dict(figs=[A(MID, pelvis=(0, 98, 0)), B(MID)], view=90, cap="Standing tall", marks=[("x", "rk")], zoom=1.4),
      dict(figs=[A(YIELD, lean=-10), B(PUSH)], view=90, cap="Bending back", marks=[("x", "P")], zoom=1.4),
      dict(figs=[A(MID, head_pitch=26), B(MID)], view=90, cap="Watching hands", marks=[("x", "head")], zoom=1.4),
      dict(figs=[A((-30, -10, 30)), B(MID)], view=55, cap="Losing contact", marks=[("x", "rw")], zoom=1.4)]
plate("p14_6", pl)

# 14.7 Sensitivity progression chart
fig, ax = chart("p14_7", 4.5, 1.9)
stages = ["Fixed\npattern", "Slow\nfree", "Eyes\nclosed", "Steps\nadded", "Two\nhands", "Light\napplication", "Free\nkakie"]
months = [1, 3, 5, 8, 11, 15, 20]
ax.step(range(len(stages)), months, where="mid", color=INK, lw=1.1)
ax.plot(range(len(stages)), months, "o", color=INK, ms=3.5)
ax.set_xticks(range(len(stages)), stages, fontsize=5.6); ax.set_ylabel("Approx. month begun", fontsize=6.5)
save_chart(fig, "p14_7", 1)

# 14.8 Eyes-closed sticking
fr = [(MID, MID, "Contact"), (HI, HI, "Partner leads up"), (LO, LO, "Down"), ((-14, -10, 30), (-14, -10, 30), "Out"),
      ((4, -10, 30), (4, -10, 30), "In"), (PUSH, YIELD, "Forward"), (YIELD, PUSH, "Back"), (MID, MID, "Still: listen")]
plate("p14_8", [dict(figs=[A(a, head_pitch=10), B(b)], view=55, cap=c, zoom=1.4) for a, b, c in fr])

# 14.9 Two-hand kakie
TL = (10, -12, 34); TR = (-10, -12, 34)
fr = [((TL, TR), (TL, TR), "Both wrists touch"), (((10, -12, 44), (-10, -20, 28)), ((10, -20, 28), (-10, -12, 44)), "Alternate push"),
      (((10, -20, 28), (-10, -12, 44)), ((10, -12, 44), (-10, -20, 28)), "Reverse"), (((12, 0, 32), (-10, -24, 30)), ((12, 0, 32), (-10, -24, 30)), "High and low"),
      (((10, -24, 30), (-12, 0, 32)), ((10, -24, 30), (-12, 0, 32)), "Change"), (((4, -10, 30), (-4, -10, 30)), ((4, -10, 30), (-4, -10, 30)), "Hands close"),
      (((16, -12, 30), (-16, -12, 30)), ((16, -12, 30), (-16, -12, 30)), "Hands wide"), ((TL, TR), (TL, TR), "Settle")]
plate("p14_9", [dict(figs=[A(a[1], lh=a[0]), B(b[1], lh=b[0])], view=55, cap=c, zoom=1.4) for a, b, c in fr])

# 14.10 Off-balancing from above
FP = [dict(feet=[(-16, -27, 24, "r", "solid", 50), (16, -48, -12, "l", "solid", 50), (16, 27, 204, "r", "ghost"), (-16, 48, 168, "l", "ghost")], cap="Both balanced", xr=56),
      dict(feet=[(-16, -27, 24, "r", "heavy", 80), (16, -48, -12, "l", "solid", 20), (16, 27, 204, "r", "ghost"), (-16, 48, 168, "l", "ghost")], cap="A over front foot", xr=56),
      dict(feet=[(-16, -27, 24, "r"), (16, -48, -12, "l"), (16, 27, 204, "r", "ghost"), (-16, 48, 168, "l", "ghost")], cap="B leads forward", xr=56,
           paths=[((-6, -10), (-20, 0), (-36, -4))]),
      dict(feet=[(-16, -27, 24, "r"), (16, -48, -12, "l"), (16, 27, 204, "r", "ghost"), (-16, 48, 168, "l", "ghost")], cap="Weak line (arrow)", xr=56,
           paths=[((0, 0), (-10, -30), (-34, -40))])]
footplate("p14_10", FP, ph=1.4)

# 14.11 From kakie to strike
fr = [(MID, MID, "Contact"), (YIELD, PUSH, "Absorb"), ((-12, -14, 22), PUSH, "Redirect"), ((-12, -14, 22), PUSH, "Trap"),
      ((-12, -14, 22), PUSH, "Strike begins"), ((-12, -14, 22), PUSH, "Palm strike"), ((-12, -14, 22), PUSH, "Hold"), (MID, MID, "Reset")]
pl = []
for i, (a, b, c) in enumerate(fr):
    lh = (14, -24, 20) if i < 4 else ((6, -4, 40) if i == 4 else (4, 2, 52))
    pl.append(dict(figs=[A(a, lh=lh, hy=-10 if i >= 4 else 0), B(b)], view=90, cap=c, zoom=1.4))
plate("p14_11", pl)

# 14.12 Kakie with steps
fr = []
for i, t in enumerate(np.linspace(0, 1, 8)):
    off = 14 * math.sin(math.pi * t)
    a = A(PUSH if i < 4 else YIELD, pelvis=(0, 91, off))
    b = B(YIELD if i < 4 else PUSH, pelvis=(0, 91, -off))
    fr.append(dict(figs=[a, b], view=90, cap=["Start", "A advances", "B gives way", "Furthest", "Turn", "B advances", "A gives", "Centre"][i], zoom=1.45))
plate("p14_12", fr)

write_count("ch14")
