"""Three alternative 6 x 9 inch front covers (1800 x 2700 px at 300 dpi)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
from matplotlib.colors import LinearSegmentedColormap

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "options")
os.makedirs(OUT, exist_ok=True)
W, H = 6.0, 9.0
SANS, SERIF, DISPLAY = "Source Sans 3", "Crimson Text", "EB Garamond"
TITLE1, TITLE2, TITLE3 = "CIRCUIT", "ANALYSIS", "MADE SIMPLE"
SUB_A = "A Modern Textbook for Beginners"
SUB_B = "Ohm’s Law to Thévenin, Norton, and Mesh Analysis\nExplained Clearly"
AUTHOR = "MARCUS J. THORNTON, PH.D."


def canvas(bg):
    fig = plt.figure(figsize=(W, H), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, fc=bg, ec="none", zorder=0))
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=300)
    fig.savefig(os.path.join(OUT, name + ".jpg"), dpi=300, pil_kwargs={"quality": 95})
    plt.close(fig)


def resistor(ax, x, y, horiz=True, L=0.62, Wd=0.2, ec="k", fc="none", lw=3, z=4):
    if horiz:
        ax.add_patch(Rectangle((x - L / 2, y - Wd / 2), L, Wd, fc=fc, ec=ec, lw=lw, zorder=z))
    else:
        ax.add_patch(Rectangle((x - Wd / 2, y - L / 2), Wd, L, fc=fc, ec=ec, lw=lw, zorder=z))


# ------------------------------------------------------------------ Cover A
# "Classic Prestige": warm ivory, elegant serif, single copper circuit line.
IVORY, INK, COPPER, NAVY = "#f5f0e6", "#1c2333", "#b5562a", "#1d3557"
fig, ax = canvas(IVORY)
ax.add_patch(Rectangle((0.32, 0.32), W - 0.64, H - 0.64, fc="none", ec=INK, lw=1.1, zorder=1))
ax.add_patch(Rectangle((0.40, 0.40), W - 0.80, H - 0.80, fc="none", ec=INK, lw=0.5, zorder=1))
ax.text(W / 2, 8.05, SUB_A.upper(), ha="center", fontsize=10.5, family=SANS, color=COPPER, fontweight="semibold")
ax.plot([2.3, 3.7], [7.83, 7.83], color=COPPER, lw=1.2)
ax.text(W / 2, 7.05, "Circuit", ha="center", va="center", fontsize=64, family=DISPLAY, color=INK)
ax.text(W / 2, 6.0, "Analysis", ha="center", va="center", fontsize=64, family=DISPLAY, color=INK)
ax.text(W / 2, 5.08, "Made Simple", ha="center", va="center", fontsize=40, family=DISPLAY, color=COPPER, style="italic")
# single continuous copper circuit line running across the page
y, cx = 4.15, W / 2
ax.plot([0.4, 1.3], [y, y], color=COPPER, lw=2.6)
resistor(ax, 1.62, y, ec=COPPER, fc=IVORY, lw=2.6)
ax.plot([1.93, 4.07], [y, y], color=COPPER, lw=2.6)
ax.add_patch(Circle((cx, y), 0.07, color=COPPER, zorder=5))
ax.plot([cx, cx], [y, y - 0.35], color=COPPER, lw=2.6)
resistor(ax, cx, y - 0.66, horiz=False, ec=COPPER, fc=IVORY, lw=2.6)
ax.plot([cx, cx], [y - 0.97, y - 1.25], color=COPPER, lw=2.6)
for k, w_ in enumerate([0.36, 0.24, 0.12]):
    ax.plot([cx - w_ / 2, cx + w_ / 2], [y - 1.25 - k * 0.08] * 2, color=COPPER, lw=2.2)
resistor(ax, 4.38, y, ec=COPPER, fc=IVORY, lw=2.6)
ax.plot([4.69, 5.6], [y, y], color=COPPER, lw=2.6)
ax.text(W / 2, 1.95, SUB_B, ha="center", va="center", fontsize=13.5, family=SERIF, color=INK, style="italic", linespacing=1.35)
ax.plot([2.6, 3.4], [1.35, 1.35], color=INK, lw=0.8)
ax.text(W / 2, 0.92, AUTHOR, ha="center", va="center", fontsize=15, family=SANS, color=INK, fontweight="semibold")
save(fig, "cover_A_classic")

# ------------------------------------------------------------------ Cover B
# "Bold Bestseller": near-black, massive stacked sans title, glowing waveform.
BG, GLOW, WHITE, AMBER = "#0e1116", "#ff8a3d", "#f4f1ea", "#ffb36b"
fig, ax = canvas(BG)
grad = np.linspace(0, 1, 256).reshape(-1, 1)
cmap = LinearSegmentedColormap.from_list("v", ["#0e1116", "#151b26", "#1b2333"])
ax.imshow(grad, extent=[0, W, 0, H], cmap=cmap, aspect="auto", origin="lower", zorder=0)
# faint grid like an oscilloscope screen
for gx in np.arange(0, W + 0.01, 0.5):
    ax.plot([gx, gx], [2.2, 4.6], color="#2a3446", lw=0.6, zorder=1)
for gy in np.arange(2.2, 4.61, 0.4):
    ax.plot([0, W], [gy, gy], color="#2a3446", lw=0.6, zorder=1)
ax.text(W / 2, 8.45, AUTHOR, ha="center", va="center", fontsize=15, family=SANS, color=AMBER, fontweight="bold")
ax.text(0.45, 7.35, TITLE1, ha="left", va="center", fontsize=78, family=SANS, color=WHITE, fontweight="bold")
ax.text(0.45, 6.3, TITLE2, ha="left", va="center", fontsize=78, family=SANS, color=WHITE, fontweight="bold")
ax.text(0.47, 5.38, TITLE3, ha="left", va="center", fontsize=46, family=SANS, color=GLOW, fontweight="bold")
# glowing step/wave: a square pulse turning into a damped sine (signal through a circuit)
t = np.linspace(0, W, 1200)
sig = 3.4 + 0.8 * np.exp(-((t - 1.2) % 6) * 0.35) * np.sin(2 * np.pi * (t - 1.2) / 1.1)
sig[t < 1.2] = 3.4 + 0.8 * ((t[t < 1.2] > 0.4) & (t[t < 1.2] < 0.9))
for lw, al in [(14, 0.05), (9, 0.09), (5, 0.18), (2.4, 1.0)]:
    ax.plot(t, sig, color=GLOW, lw=lw, alpha=al, zorder=3, solid_capstyle="round")
ax.plot([0.45, 1.6], [1.85, 1.85], color=GLOW, lw=3)
ax.text(0.45, 1.25, "Ohm’s Law to Thévenin, Norton, and Mesh Analysis — Explained Clearly",
        ha="left", va="center", fontsize=11.3, family=SANS, color=WHITE, wrap=True)
ax.text(0.45, 0.72, "A MODERN TEXTBOOK FOR BEGINNERS", ha="left", va="center", fontsize=10.5, family=SANS,
        color="#9aa6b8", fontweight="semibold")
save(fig, "cover_B_bold")

# ------------------------------------------------------------------ Cover C
# "Graphic Modern": teal colour field with bold geometric circuit art, white title panel.
TEAL, DEEP, CORAL, PAPER = "#0f6e6e", "#0a4a4a", "#f2785c", "#fbfaf7"
fig, ax = canvas(PAPER)
ax.add_patch(Rectangle((0, 4.5), W, 4.5, fc=TEAL, ec="none", zorder=1))
# big geometric circuit: a two-mesh network drawn chunky in white with coral accents
lw = 7
x0, x1, x2, yb, yt = 0.9, 3.0, 5.1, 5.25, 8.2
ax.plot([x0, x2, x2, x0, x0], [yt, yt, yb, yb, yt], color=PAPER, lw=lw, solid_joinstyle="miter", zorder=2)
ax.plot([x1, x1], [yb, yt], color=PAPER, lw=lw, zorder=2)
ax.add_patch(Circle((x0, (yb + yt) / 2), 0.42, fc=TEAL, ec=PAPER, lw=lw, zorder=3))
ax.text(x0, (yb + yt) / 2 + 0.13, "+", ha="center", va="center", color=PAPER, fontsize=26, family=SANS, fontweight="bold", zorder=4)
ax.text(x0, (yb + yt) / 2 - 0.17, "–", ha="center", va="center", color=PAPER, fontsize=26, family=SANS, fontweight="bold", zorder=4)
for (cx, cy, h) in [((x0 + x1) / 2, yt, True), ((x1 + x2) / 2, yt, True), (x1, (yb + yt) / 2, False), (x2, (yb + yt) / 2, False)]:
    resistor(ax, cx, cy, horiz=h, L=0.95, Wd=0.34, ec=PAPER, fc=CORAL, lw=lw * 0.75, z=4)
for c in [(x1, yt), (x1, yb)]:
    ax.add_patch(Circle(c, 0.14, color=PAPER, zorder=5))
# loop-current arcs
for cx in [(x0 + x1) / 2 + 0.05, (x1 + x2) / 2]:
    th = np.linspace(np.pi * 0.9, -np.pi * 0.6, 80)
    ax.plot(cx + 0.5 * np.cos(th), (yb + yt) / 2 + 0.5 * np.sin(th), color=CORAL, lw=4, zorder=3)
    ax.annotate("", xy=(cx + 0.5 * np.cos(th[-1]), (yb + yt) / 2 + 0.5 * np.sin(th[-1])),
                xytext=(cx + 0.5 * np.cos(th[-4]), (yb + yt) / 2 + 0.5 * np.sin(th[-4])),
                arrowprops=dict(arrowstyle="-|>,head_width=0.5,head_length=0.8", color=CORAL, lw=4), zorder=3)
ax.add_patch(Rectangle((0, 4.36), W, 0.14, fc=CORAL, ec="none", zorder=2))
ax.text(0.5, 3.75, "Circuit Analysis", ha="left", va="center", fontsize=46, family=SANS, color=DEEP, fontweight="bold")
ax.text(0.5, 3.0, "Made Simple", ha="left", va="center", fontsize=46, family=SANS, color=CORAL, fontweight="bold")
ax.text(0.52, 2.3, SUB_A, ha="left", va="center", fontsize=14, family=SERIF, color=DEEP, style="italic")
ax.text(0.52, 1.72, "Ohm’s Law to Thévenin, Norton, and Mesh Analysis\nExplained Clearly", ha="left", va="center",
        fontsize=12, family=SANS, color="#3b4a4a", linespacing=1.3)
ax.plot([0.52, W - 0.5], [1.12, 1.12], color=DEEP, lw=1)
ax.text(0.52, 0.72, AUTHOR, ha="left", va="center", fontsize=15, family=SANS, color=DEEP, fontweight="bold")
save(fig, "cover_C_graphic")

# ------------------------------------------------------------------ comparison sheet
from PIL import Image, ImageDraw, ImageFont
ims = [Image.open(os.path.join(OUT, f"cover_{n}.png")).convert("RGB").resize((600, 900)) for n in ["A_classic", "B_bold", "C_graphic"]]
sheet = Image.new("RGB", (3 * 600 + 4 * 50, 900 + 140), "white")
font = ImageFont.truetype(os.path.join(os.path.dirname(OUT), "..", "fonts", "SourceSans3-Semibold.ttf"), 34)
d = ImageDraw.Draw(sheet)
for i, (im, lab) in enumerate(zip(ims, ["Option A — Classic", "Option B — Bold", "Option C — Graphic"])):
    x = 50 + i * 650
    sheet.paste(im, (x, 40))
    d.rectangle([x - 1, 39, x + 600, 940], outline="#cccccc")
    d.text((x + 300, 990), lab, fill="#1d3557", font=font, anchor="mm")
sheet.save(os.path.join(OUT, "cover_options_comparison.png"))
print("done")
