import sys; sys.path.insert(0, '.')
from goju import *

def wheel(ax):
    ax.add_patch(Circle((0, 0), 0.52, fc="none", ec="black", lw=2.2))
    ax.add_patch(Circle((0, 0), 0.5, fc="none", ec="black", lw=0.6))
    ax.add_patch(Circle((0, 0), 0.15, fc="white", ec="black", lw=1.4, zorder=5))
    label(ax, (0, 0), "SANCHIN", size=7.5, weight="bold")
    names = ["Tensho", "Kaishu kata", "Hojo undo", "Kakie", "Bunkai"]
    for i, n in enumerate(names):
        a = math.radians(90 - i * 72)
        ax.plot([0.15 * math.cos(a), 0.5 * math.cos(a)], [0.15 * math.sin(a), 0.5 * math.sin(a)], c="black", lw=1.2)
        x, y = 0.33 * math.cos(a + 0.32), 0.33 * math.sin(a + 0.32)
        label(ax, (x, y), n, size=7)
    label(ax, (0, -0.6), "rim: daily practice", size=7, style="italic")
    return 1
diagram("fig15_1", wheel, w_in=3.0, h_in=3.0, xlim=(-0.65, 0.65), ylim=(-0.68, 0.62))

plate("fig15_2", [
    P(F("shiko", "hikite", "kentsui", drop=0.02)), P(F("shiko", "hikite", "hikite", drop=0.02)), P(F("shiko", "empi", "hikite", drop=0.02)),
    P(F("shiko", "hikite", ((-0.06, 0.06), (-0.1, -0.02), "fist", 180))), P(F("shiko", "hikite", "gedan_open", drop=0.02)),
    P(F("shiko", "shotei_low", "shotei_high", drop=0.02)), P(F("shiko", "hikite", "gedan_open")), P(F("shiko", "kentsui", "kentsui", drop=0.03)),
], cols=4, caption_labels=["Saifa", "Seiyunchin", "Shisochin", "Sanseru", "Sepai", "Kururunfa", "Seisan", "Suparinpei"])

def chi(fig):
    return with_tools(fig, [lambda ax, J: chi_ishi(ax, J["handF"], -90, 0.14)])
w = ((0.22, -0.06), -1, "open", 70)
plate("fig15_3", [
    P(F("heiko", "hira_side", "hira_side")), P(S("sanchin", "sanchin", "sanchin")), P(S("sanchin", "kake_uke", "shotei")),
    P(F("shiko", "hip", "hip")), P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])),
    P(D("sanchin", "guard", w), A("sanchin", "guard", w)),
    P(D("shiko", ((0.08, -0.1), +1, "open", 0), ((0.13, 0.0), +1, "fist", 90)), A("sanchin", "hikite", ((0.28, -0.08), -1, "open", 120), x=0.27)),
    chi(S("sanchin", "hikite", "chudan_uke")),
], cols=4, panel_w=1.15)

plate("fig15_4", [
    P(F("shiko", "hip", "hip")), P(F("shiko", "hip", "hip", drop=-0.06)), P(S("neko", "tora_down", "tora_up")), P(S("neko", "tora_down", "tora_up", drop=-0.04)),
    P(S("sanchin", "sanchin", "sanchin")), P(S((0.455, None, (-0.06, 0.08)), "sanchin", "sanchin")),
    P(S("sagi", "guard", "chamber", kick="mae")), P(S("sagi", "guard", "chamber", kick="kansetsu")),
], cols=4, caption_labels=["full depth", "raised", "full depth", "raised", "standard", "shorter", "middle kick", "knee-height kick"])
print(COUNT)
