from common import *

# Figure 16.1 four levels
fig, ax = canvas(W, 2.1, xlim=(0, 160), ylim=(0, 76))
lv = [("1", "TOUCH", "check position;\ndirect attention", "everyone,\nfrom day one"),
      ("2", "PRESSURE", "steady push,\nbuilt over 2–3 s", "after basic\nstance is learned"),
      ("3", "PAT AND SLAP", "open hand on\nlarge muscles", "settled in kata;\nbreathing correct"),
      ("4", "FIRM STRIKING", "conditioning;\nmind under stress", "experienced only;\nsenior supervision")]
for i, (n, t, what, who) in enumerate(lv):
    x = 4 + i * 39
    h = 40 + i * 5
    ax.add_patch(Rectangle((x, 6), 36, h, fc=G1 if i < 2 else WH, ec=K, lw=0.9))
    numdot(ax, x + 18, 6 + h + 5, n, r=3.8, fs=6.5)
    ax.text(x + 18, 6 + h - 4, t, ha="center", va="top", fontsize=5.9, fontweight="bold")
    ax.text(x + 18, 6 + h - 11, what, ha="center", va="top", fontsize=5.2, linespacing=1.05)
    ax.text(x + 18, 9, who, ha="center", va="bottom", fontsize=5.0, style="italic", linespacing=1.05)
label(ax, 4, 73, "Shaded: where most testing should happen", fs=5.6, ha="left", style="italic", family=SERIF)
save(fig, "fig16_1")

# Figure 16.2 no-go zones
fig, ax = canvas(W, 2.9, xlim=(0, 140), ylim=(-10, 106))
floor(ax, 2, 138)
p = Pose("uke", "uke", "sanchin", "R")
ff = Figure(ax, p, ox=36, th=0)
fb = Figure(ax, p, ox=104, th=180)
from matplotlib.patches import Ellipse as E


def zone(f, pt3, w, h, ang=0):
    c = f.P(pt3)
    e = E(c, w, h, angle=ang, fc=G2, ec=K, lw=0.6, alpha=0.85, zorder=40, hatch="////")
    ax.add_patch(e)


# front: head/neck, solar plexus, lower abdomen, groin, knees, elbows
zone(ff, v(0, 6, 92), 14, 15); zone(ff, v(0, 6, 85), 6, 5)
zone(ff, v(0, 7, 70), 6, 5); zone(ff, v(0, 7, 57), 9, 5); zone(ff, v(0, 6, 47), 7, 5)
for s in (-1, 1):
    zone(ff, v(s * 7.5, 12, 27), 6, 6); zone(ff, v(s * 14, 8, 64), 4.5, 4.5)
    zone(ff, v(s * 10, 7, 64), 4, 3)
# back: head/neck, spine, kidneys
zone(fb, v(0, -6, 90), 14, 18); zone(fb, v(0, -7, 68), 4, 26)
for s in (-1, 1):
    zone(fb, v(s * 5.5, -7, 58), 5, 6)
    zone(fb, v(s * 7.5, -3, 27), 6, 6)
sub_label(ax, 36, -2, "Front", fs=6.4); sub_label(ax, 104, -2, "Back", fs=6.4)
ax.add_patch(E((66, 100), 8, 5, fc=G2, ec=K, lw=0.6, hatch="////"))
label(ax, 72, 100, "never strike", fs=5.6, ha="left")
save(fig, "fig16_2")

# Figure 16.3 tester behind student
fig, ax = canvas(W, 2.5, xlim=(10, 120), ylim=(-6, 106))
floor(ax, 12, 118)
student = Pose("uke", "uke", "sanchin", "R")
tester = Pose("nukite", "nukite", "sanchin", "L")
for s in ("l", "r"):
    tester.j[s + "el"] = tester.j[s + "el"] + v(0, -2, 3)
    tester.j[s + "wr"] = v(tester.j[s + "wr"][0] * 1.6, 16, 84)
    tester.j[s + "hd"] = v(tester.j[s + "hd"][0] * 1.6, 23, 84)
ft = Figure(ax, tester, ox=46, th=-90, zorder=1)
fs_ = Figure(ax, student, ox=72, th=-90, zorder=2)
a = ft.joint("rhd")
arrow(ax, a[0] - 3, a[1] + 14, a[0] - 3, a[1] + 4, lw=1.3, ms=8, z=40)
label(ax, 46, 102, "tester", fs=6, style="italic", family=SERIF)
label(ax, 76, 102, "student", fs=6, style="italic", family=SERIF)
label(ax, 100, 60, "pressure builds\non the out-breath,\nreleases smoothly", fs=5.6, ha="left")
save(fig, "fig16_3")
