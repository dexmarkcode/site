"""Three further cover options with no figures: typography, brush art and texture. 6 x 9 in, 300 dpi."""
from covers import new, fit, spaced, enso, hanko, save_cover, BLACK_FONT, JP_FONT, TITLE, AUTHOR, OUT, glow, gradient
from common import *
import matplotlib.colors as mc
from PIL import Image, ImageDraw, ImageFont

SUB = ("Illustrated Textbook With Frame-by-Frame Diagrams, Testing Drills,\nPosture Corrections, and Strength Progressions\n"
       "for the Foundational Form")
g = np.random.default_rng(11)


def texture(ax, base, amount=0.05, zorder=0.6, grain=600):
    """Paper / canvas grain over the whole cover."""
    n = g.normal(0, 1, (grain * 3 // 2, grain))
    from scipy.ndimage import gaussian_filter
    n = gaussian_filter(n, 1.2) + 0.5 * gaussian_filter(g.normal(0, 1, n.shape), 12)
    n = (n - n.min()) / (n.max() - n.min())
    rgba = np.zeros(n.shape + (4,))
    rgba[..., :3] = mc.to_rgb(base)
    rgba[..., :3] = np.clip(rgba[..., :3] * (1 - amount) + amount * n[..., None], 0, 1)
    rgba[..., 3] = 1
    ax.imshow(rgba, extent=(0, 60, 0, 90), origin="lower", aspect="auto", zorder=zorder, interpolation="bicubic")


def splatter(ax, cx, cy, color, n=60, spread=14, zorder=4):
    for _ in range(n):
        a = g.uniform(0, 2 * math.pi); r = abs(g.normal(spread * 0.8, spread * 0.35))
        s = g.uniform(0.08, 0.55) * (1.2 - min(r / (spread * 2), 1))
        ax.add_patch(Circle((cx + r * math.cos(a), cy + r * math.sin(a)), max(s, 0.06), fc=color, ec="none", zorder=zorder))


def gold_text(fig, ax, x, y, s, width, **kw):
    """Text with a subtle darker drop shadow for a foil-like effect."""
    t2 = fit(fig, ax, x + 0.18, y - 0.18, s, width, color="#5A4216", **{k: v for k, v in kw.items() if k != "color"})
    t = fit(fig, ax, x, y, s, width, **kw)
    t2.set_zorder(t.get_zorder() - 0.01)
    return t


GOLD = "#C9A24E"; LGOLD = "#E3C37A"; CRIMSON = "#8F1620"; DEEP = "#1A0608"; INK = "#141416"
CREAM = "#F2EADB"; NAVY = "#0D1B33"; EMER = "#0E3B34"

# ---------------------------------------------------------------- D: Kanji Monument (crimson to black, gold)
fig, ax = new()
gradient(ax, "#060203", "#7A121B", zorder=0.4)
glow(ax, 30, 58, 34, 30, "#B3242E", 0.5, zorder=0.5)
ax.text(30.6, 47.4 - 0, "", zorder=1.9)
ax.text(30, 67, "三", fontproperties=JP_FONT, fontsize=150, color=GOLD, alpha=0.92, ha="center", va="center", zorder=2)
ax.text(30, 46.5, "戦", fontproperties=JP_FONT, fontsize=150, color=GOLD, alpha=0.92, ha="center", va="center", zorder=2)
ax.add_patch(Rectangle((0, 20), 60, 70, fc="none", ec="none"))
ax.add_patch(Rectangle((3, 3), 54, 84, fc="none", ec=GOLD, lw=0.8, zorder=3))
fit(fig, ax, 30, 84.0, spaced("GOJU-RYU KARATE", 1), 26, color=LGOLD, family="Source Sans 3", fontweight="bold", zorder=5)
# title on a dark band
ax.add_patch(Rectangle((3, 14.8), 54, 15.4, fc="#0B0304", ec="none", alpha=0.88, zorder=4))
fit(fig, ax, 30, 25.3, TITLE, 46, color="#FFFFFF", fontproperties=BLACK_FONT, zorder=5)
gold_text(fig, ax, 30, 18.4, spaced("MASTERCLASS", 2), 40, color=LGOLD, family="Source Sans 3", fontweight="semibold", zorder=5)
ax.text(30, 10.0, SUB, ha="center", va="center", fontsize=8.6, color="#EAD9C0", family=SERIF, style="italic", linespacing=1.3, zorder=5)
fit(fig, ax, 30, 4.9, AUTHOR, 30, color=LGOLD, family="Source Sans 3", fontweight="bold", zorder=5)
save_cover(fig, "cover_D_kanji_monument")

# ---------------------------------------------------------------- E: Ink and Paper (cream, black ink, red seal)
fig, ax = new()
texture(ax, CREAM, 0.07, zorder=0.4)
glow(ax, 30, 44, 34, 40, "#FFFFFF", 0.35, zorder=0.5)
enso(ax, 30, 44, 20.5, color=INK, max_w=34, seed=9, start=1.05, sweep=2 * math.pi - 0.55)
splatter(ax, 45, 60, INK, n=70, spread=6)
splatter(ax, 16, 32, INK, n=30, spread=4)
fit(fig, ax, 30, 84.0, spaced("GOJU-RYU KARATE", 1), 26, color=CRIMSON, family="Source Sans 3", fontweight="bold")
fit(fig, ax, 30, 47.6, TITLE, 27, color=INK, fontproperties=BLACK_FONT, zorder=6)
fit(fig, ax, 30, 41.4, spaced("MASTERCLASS", 1), 24, color=CRIMSON, family=SERIF, fontweight="semibold", zorder=6)
hanko(ax, 47.0, 66.0, 3.8, bg=CRIMSON, fg=CREAM)
ax.text(30, 15.6, SUB, ha="center", va="center", fontsize=10.0, color="#2A2A2E", family=SERIF, style="italic", linespacing=1.35)
ax.plot([24, 36], [10.2, 10.2], color=CRIMSON, lw=1.0)
fit(fig, ax, 30, 6.0, AUTHOR, 38, color=INK, family=SERIF, fontweight="bold")
save_cover(fig, "cover_E_ink_and_paper")

# ---------------------------------------------------------------- F: Bold Type (navy, gold, crimson)
fig, ax = new()
gradient(ax, "#08111F", "#16294A", zorder=0.4)
# large geometric "3" motif: three gold bars (three battles)
for k, (w, y) in enumerate(((44, 62.0), (44, 57.6), (44, 53.2))):
    ax.add_patch(Rectangle((8, y), w, 1.6, fc=GOLD if k != 1 else "#B3242E", ec="none", zorder=2))
fit(fig, ax, 30, 84.6, spaced("GOJU-RYU KARATE", 1), 26, color=LGOLD, family="Source Sans 3", fontweight="bold", zorder=5)
fit(fig, ax, 30, 74.5, "SAN", 42, color="#FFFFFF", fontproperties=BLACK_FONT, zorder=5)
fit(fig, ax, 30, 38.4, "CHIN", 50, color="#FFFFFF", fontproperties=BLACK_FONT, zorder=5)
gold_text(fig, ax, 30, 27.0, spaced("MASTERCLASS", 2), 46, color=LGOLD, family="Source Sans 3", fontweight="semibold", zorder=5)
ax.text(30, 48.6, spaced("THE THREE BATTLES", 1), ha="center", va="center", fontsize=9.5, fontweight="semibold", color="#D8C9A6", family="Source Sans 3", zorder=5)
ax.plot([10, 50], [23.6, 23.6], color=GOLD, lw=0.7, zorder=5)
ax.text(30, 17.4, SUB, ha="center", va="center", fontsize=9.4, color="#E7DECB", family=SERIF, style="italic", linespacing=1.3, zorder=5)
ax.add_patch(Rectangle((0, 0), 60, 10.5, fc="#B3242E", zorder=4))
ax.plot([0, 60], [10.5, 10.5], color=GOLD, lw=1.6, zorder=5)
fit(fig, ax, 30, 5.2, AUTHOR, 40, color="#FFFFFF", family=SERIF, fontweight="bold", zorder=6)
save_cover(fig, "cover_F_bold_type")

# ---------------------------------------------------------------- preview
names = ["cover_D_kanji_monument.jpg", "cover_E_ink_and_paper.jpg", "cover_F_bold_type.jpg"]
ims = [Image.open(OUT / f).resize((600, 900)) for f in names]
sheet = Image.new("RGB", (600 * 3 + 80, 980), "#3b3b40")
dr = ImageDraw.Draw(sheet)
f = ImageFont.truetype(str(ROOT / "fonts/SourceSans3-Bold.ttf"), 34)
for k, im in enumerate(ims):
    sheet.paste(im, (20 + k * 620, 20))
    dr.text((20 + k * 620 + 300, 950), f"OPTION {'DEF'[k]}", fill="white", font=f, anchor="mm")
sheet.save(OUT / "covers_preview_DEF.jpg", quality=90)
print("preview saved")
