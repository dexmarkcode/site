from common import *
from matplotlib.patches import FancyBboxPatch


def rbox(ax, x, y, w, h, text, fs=6.4, fill=WH, lw=0.8, bold=False, ls="solid"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.4", fc=fill, ec=K, lw=lw, ls=ls, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=4, linespacing=1.12,
            fontweight="bold" if bold else "normal")


# Figure 2.1 timeline (vertical)
events = [
    ("1853", "Kanryo Higaonna born in Naha"),
    ("c. 1870s", "Higaonna studies in Fuzhou (dates vary between sources)"),
    ("c. 1880s", "Higaonna returns to Naha and teaches Naha-te"),
    ("1888", "Chojun Miyagi born in Naha"),
    ("c. 1902", "Miyagi begins training with Higaonna"),
    ("1915", "Higaonna dies; Miyagi travels to Fuzhou"),
    ("early 1920s", "Miyagi composes Tensho"),
    ("c. 1930", "The name Goju-Ryu is chosen"),
    ("1940", "Gekisai kata composed for teaching in schools"),
    ("1953", "Miyagi dies; senior students found their own dojos"),
    ("1970s on", "International Goju-Ryu federations spread worldwide"),
]
n = len(events)
fig, ax = canvas(W, 2.9, xlim=(0, 150), ylim=(0, 97))
x0 = 34
ax.plot([x0, x0], [3, 94], color=K, lw=1.3)
for i, (yr, txt) in enumerate(events):
    y = 91 - i * 8.4
    ax.add_patch(Circle((x0, y), 1.5, fc=K if i not in (0, 3) else WH, ec=K, lw=0.9, zorder=5))
    ax.text(x0 - 4, y, yr, ha="right", va="center", fontsize=6.6, fontweight="bold")
    ax.text(x0 + 5, y, txt, ha="left", va="center", fontsize=6.6)
save(fig, "fig2_1")

# Figure 2.2 family tree
fig, ax = canvas(W, 3.2, xlim=(0, 150), ylim=(0, 106))
H = 11
rbox(ax, 45, 92, 60, H, "Fujian boxing\n(san zhan forms)", fill=G1, bold=True, fs=5.9)
rbox(ax, 18, 74, 50, H, "Kanryo Higaonna\nNaha-te", bold=True, fs=5.9)
rbox(ax, 92, 74, 50, H, "Kanbun Uechi\nUechi-Ryu", fs=5.9)
line(ax, [75, 75, 43, 43], [92, 89, 89, 85]); line(ax, [75, 117, 117], [89, 89, 85])
rbox(ax, 2, 57, 44, H, "Chojun Miyagi\nGoju-Ryu", bold=True, lw=1.3, fs=5.9)
rbox(ax, 54, 57, 44, H, "Kenwa Mabuni\nShito-Ryu", fs=5.9)
rbox(ax, 106, 57, 42, H, "Gogen Yamaguchi\nGoju-kai (Japan)", fs=5.7)
line(ax, [43, 43, 24, 24], [74, 71, 71, 68]); line(ax, [43, 76, 76], [71, 71, 68], ls=(0, (3, 2)))
line(ax, [40, 40, 127, 127], [57, 54, 54, 57], ls=(0, (3, 2)))
students = [("Seiko Higa", 2), ("Meitoku Yagi\nMeibukan", 30), ("Eiichi Miyazato\nJundokan", 58), ("Seikichi Toguchi\nShoreikan", 86), ("An'ichi Miyagi", 114)]
line(ax, [14, 14], [57, 49]); line(ax, [14, 127], [49, 49])
for name, x in students:
    rbox(ax, x, 35, 26, H, name, fs=5.4)
    line(ax, [x + 13, x + 13], [49, 46])
rbox(ax, 56, 13, 44, H, "Morio Higaonna\nIOGKF", fs=5.9)
line(ax, [127, 127, 78, 78], [35, 30, 30, 24]); line(ax, [71, 71, 78], [35, 30, 30], ls=(0, (3, 2)))
rbox(ax, 108, 13, 40, H, "Masutatsu Oyama\nKyokushin", fs=5.7)
line(ax, [145, 145], [57, 24], ls=(0, (3, 2)))
ax.text(2, 4, "Solid line: teacher to student.  Dashed line: influence or partial training.  Only a few lines are shown.",
        fontsize=5.6, ha="left", style="italic", family=SERIF)
save(fig, "fig2_2")

# Figure 2.3 hands and floor patterns
fig, ax = canvas(W, 2.7, xlim=(0, 170), ylim=(-14, 100))


def open_hands(p):
    for s in ("l", "r"):
        wr, hd = p.j[s + "wr"], p.j[s + "hd"]
        p.j[s + "hd"] = wr + unit(hd - wr) * 9
        p.j[s + "ht"] = "open"
    return p


pa = open_hands(Pose("uke", "uke", "sanchin", "R"))
pb = Pose("uke", "uke", "sanchin", "R")
floor(ax, 2, 92)
Figure(ax, pa, ox=22, th=-20)
Figure(ax, pb, ox=68, th=-20)
sub_label(ax, 22, -4, "Open hands (older form)", fs=6.6)
sub_label(ax, 68, -4, "Closed fists (Miyagi)", fs=6.6)
ax.plot([100, 100], [-10, 98], color=K, lw=0.4)
# floor patterns
x0 = 112
ax.text(x0 + 6, 96, "Straight line", fontsize=6.2, ha="center", fontweight="bold")
ax.plot([x0 + 6, x0 + 6], [10, 88], color=K, lw=0.6, ls=(0, (2, 2)))
for i, yy in enumerate((16, 34, 52, 70)):
    numdot(ax, x0 + 6, yy, i + 1, r=3.2)
arrow(ax, x0 + 13, 20, x0 + 13, 74, lw=0.8)
arrow(ax, x0 - 1, 74, x0 - 1, 20, lw=0.8, ls=(0, (3, 2)))
ax.text(x0 + 6, 3, "forward and back", fontsize=5.6, ha="center", style="italic", family=SERIF)
x1 = 150
ax.text(x1 + 4, 96, "With turns", fontsize=6.2, ha="center", fontweight="bold")
ax.plot([x1 + 4, x1 + 4], [10, 88], color=K, lw=0.6, ls=(0, (2, 2)))
for i, yy in enumerate((16, 34, 52, 70)):
    numdot(ax, x1 + 4, yy, i + 1, r=3.2)
arrow(ax, x1 + 11, 20, x1 + 11, 72, lw=0.8)
ax.add_patch(Arc((x1 + 4, 80), 14, 10, theta1=0, theta2=180, color=K, lw=0.8))
arrow(ax, x1 - 3, 80, x1 - 3, 77, lw=0.8)
ax.text(x1 + 15, 84, "turn", fontsize=5.6, ha="left", style="italic", family=SERIF)
ax.text(x1 + 4, 3, "turn and return", fontsize=5.6, ha="center", style="italic", family=SERIF)
save(fig, "fig2_3")
