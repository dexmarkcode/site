from common import *

# Figure 15.1 hand shapes (schematic, from the side of the thumb)
fig, ax = canvas(W, 1.5, xlim=(0, 160), ylim=(0, 52))
# spear hand
x0, y0 = 6, 26
ax.add_patch(Polygon([(x0, y0 - 4), (x0 + 30, y0 - 3.6), (x0 + 30, y0 + 3.6), (x0, y0 + 4)], closed=True, fc=WH, ec=K, lw=1.0))
ax.add_patch(Polygon([(x0 + 30, y0 - 4.4), (x0 + 44, y0 - 4.2), (x0 + 46, y0 - 2), (x0 + 62, y0 - 1.6), (x0 + 64, y0),
                      (x0 + 62, y0 + 1.8), (x0 + 44, y0 + 2.2), (x0 + 36, y0 + 4.6), (x0 + 30, y0 + 4.4)], closed=True, fc=WH, ec=K, lw=1.0, joinstyle="round"))
for k in (-0.6, 0.6):
    ax.plot([x0 + 46, x0 + 63], [y0 + k, y0 + k], color=K, lw=0.4)
ax.add_patch(Ellipse((x0 + 38, y0 + 4.6), 9, 3.2, angle=8, fc=WH, ec=K, lw=0.9))
ax.plot([x0 - 3, x0 + 70], [y0, y0], color=K, lw=0.5, ls=(0, (3, 2)))
callout(ax, x0 + 63, y0, x0 + 58, 44, "fingertips level", fs=5.6)
callout(ax, x0 + 38, y0 + 5.5, x0 + 18, 44, "thumb tucked", fs=5.6)
label(ax, x0 + 32, 6, "Spear-hand (nukite)", fs=6.2, style="italic", family=SERIF)
# palm
x0 = 92
ax.add_patch(Polygon([(x0, y0 - 4), (x0 + 30, y0 - 3.6), (x0 + 30, y0 + 3.6), (x0, y0 + 4)], closed=True, fc=WH, ec=K, lw=1.0))
pts = [(x0 + 30, y0 - 5), (x0 + 36, y0 - 7), (x0 + 38, y0 - 2), (x0 + 38, y0 + 4), (x0 + 37, y0 + 8),
       (x0 + 40, y0 + 18), (x0 + 37, y0 + 20), (x0 + 33, y0 + 9), (x0 + 30, y0 + 5)]
ax.add_patch(Polygon(pts, closed=True, fc=WH, ec=K, lw=1.0, joinstyle="round"))
ax.add_patch(Circle((x0 + 38, y0), 1.6, fc=K, zorder=5))
callout(ax, x0 + 38, y0, x0 + 52, y0 - 10, "heel of palm\nleads", fs=5.6)
callout(ax, x0 + 39, y0 + 17, x0 + 52, 44, "fingers curved,\nfirm", fs=5.6)
label(ax, x0 + 30, 6, "Palm (shotei), as in the tiger's mouth", fs=6.2, style="italic", family=SERIF)
save(fig, "fig15_1")

# Figure 15.2 double spear-hand side and front
fig, ax = canvas(W, 2.5, xlim=(0, 140), ylim=(-10, 104))
floor(ax, 2, 138)
p = Pose("nukite", "nukite", "sanchin", "R")
f1 = Figure(ax, p, ox=34, th=-90)
Figure(ax, Pose("nukite_chamber", "nukite_chamber", "sanchin", "R"), ox=34, th=-90, ghost=True, zorder=1)
f2 = Figure(ax, p, ox=104, th=-15)
hd = f1.joint("lhd")
ax.plot([hd[0] - 50, hd[0] + 4], [hd[1], hd[1]], color=K, lw=0.5, ls=(0, (2, 1.5)), zorder=20)
label(ax, hd[0] - 52, hd[1] + 5, "solar-plexus height", fs=5.4, ha="left")
callout(ax, *f1.P(p.j["lsh"]), 60, 98, "shoulders down", fs=5.6)
sub_label(ax, 34, -2, "Side: chamber (dashed) to thrust", fs=6.2)
sub_label(ax, 104, -2, "Front three-quarter", fs=6.2)
save(fig, "fig15_2")

# Figure 15.3 hand paths
fig, ax = canvas(W, 2.4, xlim=(0, 140), ylim=(0, 80))
cx, cy = 70, 42
ax.add_patch(Ellipse((cx, cy), 80, 64, fc="none", ec=G2, lw=0.5, ls=(0, (1, 2))))
label(ax, cx, 77, "performer's view (looking out over the hands)", fs=5.6, style="italic", family=SERIF)
th = np.linspace(0, 2 * np.pi, 200)
# right hand clockwise circle centred slightly right-up; left anticlockwise slightly left-down
rc = (cx + 6, cy + 3); lc = (cx - 6, cy - 3); R = 20
ax.plot(rc[0] + R * np.cos(th), rc[1] + R * np.sin(th), color=K, lw=1.4)
ax.plot(lc[0] + R * np.cos(th), lc[1] + R * np.sin(th), color=K, lw=1.1, ls=(0, (3, 2)))
for ang in (60, 240):
    a = math.radians(ang); a2 = a - 0.25
    arrow(ax, rc[0] + R * math.cos(a), rc[1] + R * math.sin(a), rc[0] + R * math.cos(a2), rc[1] + R * math.sin(a2), lw=1.2, ms=7)
    b = math.radians(ang + 180); b2 = b + 0.25
    arrow(ax, lc[0] + R * math.cos(b), lc[1] + R * math.sin(b), lc[0] + R * math.cos(b2), lc[1] + R * math.sin(b2), lw=1.0, ms=6)
for i, ang in enumerate((90, 0, 270, 180)):
    a = math.radians(ang)
    numdot(ax, rc[0] + R * math.cos(a), rc[1] + R * math.sin(a), i + 1, r=2.6, fs=5.2)
    b = math.radians(270 - (ang - 90) if True else 0)
    b = math.radians({90: 270, 0: 180 + 0, 270: 90, 180: 0}[ang])
    b = math.radians({90: 270, 0: 0, 270: 90, 180: 180}[ang])
    numdot(ax, lc[0] + R * math.cos(b), lc[1] + R * math.sin(b), i + 1, r=2.6, fs=5.2, inv=False)
label(ax, 120, 60, "right hand:\nclockwise\n(solid, black numbers)", fs=5.6, ha="left")
label(ax, 4, 18, "left hand:\nanticlockwise\n(dashed, white numbers)", fs=5.6, ha="left")
save(fig, "fig15_3")

# Figure 15.4 tiger's mouth
fig, ax = canvas(W, 2.5, xlim=(0, 140), ylim=(-10, 104))
floor(ax, 2, 138)
p = Pose("tora_down", "tora_up", "sanchin", "R")
f1 = Figure(ax, p, ox=34, th=-90)
f2 = Figure(ax, p, ox=116, th=0)
callout(ax, *f1.joint("rhd"), 62, 98, "upper hand: chin to\nupper-chest height", fs=5.6)
callout(ax, *f1.joint("lhd"), 62, 38, "lower hand:\nlower abdomen", fs=5.6)
sub_label(ax, 34, -2, "Side", fs=6.4); sub_label(ax, 116, -2, "Front", fs=6.4)
save(fig, "fig15_4")
