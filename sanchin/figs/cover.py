"""Black-and-white EPUB cover (1600 x 2560 px)."""
from common import *
from PIL import Image

fig = plt.figure(figsize=(6.25, 10), dpi=256)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 160); ax.axis("off")
ax.add_patch(Rectangle((0, 0), 100, 160, fc=K))
ax.add_patch(Rectangle((4, 4), 92, 152, fc="none", ec=WH, lw=1.2))
ax.text(50, 146, "GOJU-RYU KARATE", ha="center", fontsize=15, color=WH, family="Source Sans 3", fontweight="light")
ax.text(50, 130, "SANCHIN", ha="center", fontsize=58, color=WH, family=SERIF, fontweight="semibold")
ax.text(50, 116, "MASTERCLASS", ha="center", fontsize=31, color=WH, family=SERIF)
ax.plot([30, 70], [110, 110], color=WH, lw=1.0)
sub = ("Illustrated Textbook With Frame-by-Frame Diagrams,\nTesting Drills, Posture Corrections, and Strength\n"
       "Progressions for the Foundational Form")
ax.text(50, 101, sub, ha="center", va="center", fontsize=10.5, color=WH, family=SERIF, style="italic", linespacing=1.35)
# vignette: white circle with figure
ax.add_patch(Circle((50, 55), 31, fc=WH, ec=WH))
t = np.linspace(0.35, 2 * math.pi - 0.15, 300)
for k in range(len(t) - 1):
    w = 1.0 + 5.0 * np.sin((t[k] - 0.35) / (2 * math.pi - 0.5) * math.pi) ** 1.5
    ax.plot(50 + 28 * np.cos(t[k:k+2]), 55 + 28 * np.sin(t[k:k+2]), color=K, lw=w, solid_capstyle="round")
Figure(ax, Pose("uke", "uke", "sanchin", "R"), ox=50, oy=31, sc=0.43, th=-35, lw=1.6)
ax.plot([36, 64], [31, 31], color=K, lw=1.2)
ax.text(50, 12, "DR BEVERLY J. STIVERS", ha="center", fontsize=17, color=WH, family=SERIF, fontweight="semibold")
fig.savefig(FIG / "cover.png", facecolor=K)
plt.close(fig)
Image.open(FIG / "cover.png").convert("L").convert("RGB").resize((1600, 2560)).save(FIG / "cover.jpg", quality=92)
print("cover saved")
