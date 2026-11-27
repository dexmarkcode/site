"""Non-sequence illustrations: lineage, stances, techniques, bunkai pairs, charts, part openers, cover."""
import math
from lib import *


def lineage():
    fig, ax = canvas(w=4.5, h=5.4, ylim=(0, 120))
    nodes = [
        (50, 112, "Fujian (Fuzhou) boxing\nwhite crane & related southern systems", 62),
        (50, 96, "Higaonna Kanryō (1853–1915)\nNaha-te", 44),
        (50, 80, "Miyagi Chōjun (1888–1953)\nnames the system Gōjū-ryū (c. 1929–30)", 56),
    ]
    for x, y, t, w in nodes:
        box(ax, x - w / 2, y - 5.5, w, 11, t, fs=6.6, bold=True, lw=0.9)
    for y1, y2 in ((106.5, 101.5), (90.5, 85.5)):
        arrow(ax, 50, y1, 50, y2, lw=0.9, ms=6)
    kids = [
        (12, "Yagi Meitoku\nMeibukan"), (31, "Higa Seikō\nShōdōkan line"), (50, "Miyazato Ei'ichi\nJundōkan"),
        (69, "Toguchi Seikichi\nShōreikan"), (88, "Yamaguchi Gōgen\nGōjū-kai (Japan)"),
    ]
    ax.plot([12, 88], [68, 68], color=INK, lw=0.9)
    ax.plot([50, 50], [74.5, 68], color=INK, lw=0.9)
    for x, t in kids:
        ax.plot([x, x], [68, 63], color=INK, lw=0.9)
        box(ax, x - 9.3, 52, 18.6, 11, t, fs=5.6, lw=0.8)
    box(ax, 50 - 17, 31, 34, 10, "Higaonna Morio\nIOGKF (founded 1979)", fs=6.0, lw=0.8)
    arrow(ax, 50, 52, 50, 41, lw=0.8, ms=5)
    label(ax, 50, 47, "trained at the Yoyogi dojo and Jundōkan", fs=5.4, c=DARK, style="italic")
    box(ax, 6, 6, 88, 18, "", fc=PALE, ec=INK, lw=0.6)
    label(ax, 50, 19, "Every line above teaches Sanchin and Tenshō plus the twelve kaishu kata,", fs=6.2)
    label(ax, 50, 14, "but counts, embusen details and some techniques differ from dojo to dojo.", fs=6.2)
    label(ax, 50, 9, "This book shows one consistent teaching version and flags the main variations.", fs=6.2, style="italic")
    save(fig, "fig_lineage")


def timeline():
    fig, ax = canvas(w=4.5, h=2.2)
    y = 20
    ax.plot([4, 96], [y, y], color=INK, lw=1.4)
    ev = [(1853, "Higaonna Kanryō\nborn, Naha"), (1867, "Travels to\nFuzhou (trad. date)"), (1888, "Miyagi Chōjun\nborn"),
          (1915, "Miyagi travels\nto Fujian"), (1930, "Name Gōjū-ryū\nin use"), (1940, "Gekisai kata\ncreated"),
          (1953, "Miyagi dies"), (1979, "IOGKF\nfounded")]
    x0, x1 = 1850, 1985
    for i, (yr, t) in enumerate(ev):
        x = 4 + (yr - x0) / (x1 - x0) * 92
        ax.add_patch(Circle((x, y), 1.1, fc=WHITE, ec=INK, lw=0.9, zorder=5))
        up = i % 2 == 0
        ax.plot([x, x], [y + (1.1 if up else -1.1), y + (7 if up else -7)], color=INK, lw=0.6)
        label(ax, x, y + (13 if up else -13), f"{yr}\n{t}", fs=5.4, linespacing=1.1)
    save(fig, "fig_timeline")


STANCE_INFO = [
    ("musubi", "musubi_side", "Musubi dachi", "Heels together, toes\nopen about 45°"),
    ("heiko", "heiko", "Heiko dachi", "Feet parallel,\nshoulder width"),
    ("sanchin_R", "sanchin_R", "Sanchin dachi", "Heel–toe line one\nfoot-length; front foot in"),
    ("zenkutsu_R", "zenkutsu_R", "Zenkutsu dachi", "Long stance, front\nknee over the toes"),
    ("shiko", "shiko", "Shiko dachi", "Wide, knees out over\nthe toes, hips low"),
    ("neko_R", "neko_R", "Neko ashi dachi", "Weight on the back leg,\nfront heel raised"),
    ("sagi_R", "sagi_R", "Sagi ashi dachi", "One-leg stance, raised\nfoot at the knee"),
    ("kosa_R", "kosa_R", "Kōsa dachi", "Crossed, low stance;\nrear knee behind"),
]


def stances(part, items):
    n = len(items)
    fig, ax = canvas(w=4.5, h=4.5 * 92 / 100, ylim=(0, 92))
    cw = 100 / 2
    for i, (fp, st, name, desc) in enumerate(items):
        r, c = divmod(i, 2)
        x = c * cw; y = 92 - (r + 1) * 46
        ax.add_patch(Rectangle((x + 0.4, y + 0.4), cw - 0.8, 45.2, fc=WHITE, ec=INK, lw=0.6))
        label(ax, x + cw / 2, y + 41.5, name, fs=8, fontweight="bold")
        fst = st if st in STANCES else ("sagi_R" if st.startswith("sagi") else "kosa_R")
        figst = {"sanchin_R": "sanchin_R", "neko_R": "neko_R", "zenkutsu_R": "zenkutsu_R", "kosa_R": "kosa_R",
                 "sagi_R": "sagi_R", "musubi_side": "musubi", "heiko": "heiko", "shiko": "shiko"}[st]
        arms = {"musubi": ("yoi_open", "yoi_open"), "heiko": ("yoi_fist", "yoi_fist"), "shiko": ("hip", "hip"),
                "sagi_R": ("hip", "hip")}.get(figst, ("chudan_uke", "hip"))
        gy = y + 9
        ground(ax, x + 3, x + 28, gy)
        figure(ax, x + 15 - (2 if STANCES[figst]["view"] == "side" else 0), gy, figst, L=arms[0], R=arms[1], s=2.6)
        # footprints, top view
        place_stance(ax, x + 38, y + 21, fp, "N", size=6.2, fill=WHITE, ec=INK)
        ax.plot([x + 30, x + 46], [y + 21, y + 21], color=MID, lw=0.4, ls=(0, (2, 2)))
        label(ax, x + 38, y + 5.5, desc, fs=5.6, c=DARK, linespacing=1.1)
    save(fig, f"fig_stances_{part}")


def sanchin_detail():
    fig, ax = canvas(w=4.5, h=2.8)
    place_stance(ax, 30, 30, "sanchin_R", "N", size=17, fill=WHITE)
    ax.plot([15, 45], [21, 21], color=MID, lw=0.5, ls=(0, (3, 2)))
    ax.plot([15, 45], [39.5, 39.5], color=MID, lw=0.5, ls=(0, (3, 2)))
    arrow(ax, 48, 21, 48, 39.5, both=True, lw=0.7, ms=5)
    label(ax, 52, 30, "about one\nfoot-length\n(heel of front\nto toes of rear)", fs=5.8, ha="left")
    arrow(ax, 22, 8, 38, 8, both=True, lw=0.7, ms=5)
    label(ax, 30, 4, "shoulder width", fs=5.8)
    label(ax, 80, 46, "Common faults", fs=7.5, fontweight="bold")
    for i, t in enumerate(["Front foot turned in too far:\nknee collapses", "Rear heel lifts:\nroot is lost", "Stance too long:\nbecomes zenkutsu",
                           "Hips push back:\nspine loses its line"]):
        label(ax, 80, 37 - i * 9.5, t, fs=5.8, linespacing=1.1)
    save(fig, "fig_sanchin_detail")


def levels():
    fig, ax = canvas(w=4.5, h=3.0, ylim=(0, 66.7))
    gy = 4
    ground(ax, 10, 50, gy)
    figure(ax, 30, gy, "heiko", L="hip", R="hip", s=5.7)
    zones = [("JŌDAN", "head and neck", 49, 63), ("CHŪDAN", "chest to belt", 30, 49), ("GEDAN", "below the belt", 4, 30)]
    for name, d, y0, y1 in zones:
        ax.plot([50, 60], [y0, y0], color=INK, lw=0.5)
        ax.plot([55, 55], [y0, y1], color=INK, lw=0.7)
        label(ax, 62, (y0 + y1) / 2 + 2, name, fs=7.5, ha="left", fontweight="bold")
        label(ax, 62, (y0 + y1) / 2 - 2.5, d, fs=6.4, ha="left", c=DARK)
    ax.plot([50, 60], [63, 63], color=INK, lw=0.5)
    save(fig, "fig_levels")


def breathing():
    fig, ax = canvas(w=4.5, h=2.4)
    t = np.linspace(0, 1, 300)
    # ibuki: long slow inhale, strong exhale
    def plot(y0, f, name, note):
        ax.plot([8, 95], [y0, y0], color=MID, lw=0.4)
        ys = [f(tt) for tt in t]
        ax.plot(8 + t * 87, y0 + np.array(ys) * 9, color=INK, lw=1.2)
        label(ax, 6, y0 + 2, name, fs=7, ha="right", fontweight="bold")
        label(ax, 6, y0 - 2.5, note, fs=5.6, ha="right", c=DARK)
    def ibuki(x):
        c = (x * 2) % 1
        return c / 0.45 if c < 0.45 else max(1 - (c - 0.45) / 0.5, 0)
    def nogare(x):
        c = (x * 4) % 1
        return min(c / 0.4, 1) * 0.6 if c < 0.5 else 0.6 * max(1 - (c - 0.5) / 0.4, 0)
    plot(30, ibuki, "Ibuki", "power breath")
    plot(8, nogare, "Nogare", "escape breath")
    label(ax, 52, 44, "in ↑      out ↓      Volume of air in the lungs over two to four movements", fs=5.6, c=DARK)
    save(fig, "fig_breathing")


def techniques(part):
    items = [
        [("age_uke", "Jōdan age uke"), ("chudan_uke", "Chūdan uke"), ("gedan_barai", "Gedan barai"), ("kake_uke", "Kake uke"),
         ("tsuki", "Chūdan tsuki"), ("uraken", "Uraken uchi")],
        [("empi", "Mae empi uchi"), ("tettsui", "Tettsui uchi"), ("shotei", "Shōtei"), ("nukite", "Nukite"),
         ("hiki_uke", "Hiki uke"), ("sukui", "Sukui uke")],
    ][part - 1]
    fig, ax = canvas(w=4.5, h=4.5 * 76 / 100, ylim=(0, 76))
    for i, (preset, name) in enumerate(items):
        r, c = divmod(i, 3)
        x = c * 33.3; y = 76 - (r + 1) * 38
        ax.add_patch(Rectangle((x + 0.4, y + 0.4), 32.5, 37.2, fc=WHITE, ec=INK, lw=0.6))
        gy = y + 4.0
        figure(ax, x + 14, gy, "sanchin_L", L=preset, R="hip", s=2.45)
        ground(ax, x + 3, x + 30, gy)
        label(ax, x + 16.6, y + 34.5, name, fs=6.8, fontweight="bold")
    save(fig, f"fig_tech_{part}")


def mawashi():
    fig, ax = canvas(w=4.5, h=1.9, ylim=(0, 42))
    phases = [("kamae", "chest_guard", "1  Hands open, guard"), ("kake_uke", "osae", "2  Upper hand hooks,\nlower hand presses"),
              ("tora_top", "tora_low", "3  Hands rotate\n(tora guchi)"), ("shotei", "shotei", "4  Double palm\npush out")]
    for i, (Lp, Rp, t) in enumerate(phases):
        x = 12.5 + i * 25
        gy = 9
        ground(ax, x - 10, x + 10, gy)
        figure(ax, x - 2, gy, "neko_L", L=Lp, R=Rp, s=2.6)
        label(ax, x, 3.3, t, fs=5.6, linespacing=1.1)
        if i < 3:
            arrow(ax, x + 10, 26, x + 14, 26, lw=0.7, ms=5)
    save(fig, "fig_mawashi")


def pair(name, d_st, d_L, d_R, a_st, a_L, a_R, caption, gap=10.5, s=3.2):
    fig, ax = canvas(w=4.5, h=1.9, ylim=(0, 42))
    gy = 6
    ground(ax, 10, 90, gy)
    figure(ax, 50 - gap, gy, d_st, L=d_L, R=d_R, s=s)
    figure(ax, 50 + gap, gy, a_st, L=a_L, R=a_R, s=s, facing=-1, ghost=True)
    label(ax, 50 - gap - 1, 40, "Tori (you)", fs=6, c=INK, fontweight="bold")
    label(ax, 50 + gap + 1, 40, "Uke (partner)", fs=6, c=DARK)
    save(fig, name)


def kakie():
    pair("fig_kakie", "sanchin_L", "kake_uke", "chest_guard", "sanchin_L", "kake_uke", "chest_guard", "", gap=7.5)


def bunkai():
    B = {
        "gekisai1": [("zenkutsu_L", "age_uke", "tsuki", "zenkutsu_R", "hip", "jodan_tsuki"),
                     ("zenkutsu_R", "hip", "empi", "zenkutsu_R", "hip", "tsuki")],
        "gekisai2": [("neko_R", "hip", "kake_uke", "zenkutsu_R", "hip", "tsuki"),
                     ("neko_L", "tora_top", "tora_low", "zenkutsu_L", "tsuki", "hip")],
        "saifa": [("heiko", "prayer", "prayer", "zenkutsu_L", "kamae", "grab_pull"),
                  ("zenkutsu_R", "hip", "hammer_down", "kosa_R", "osae", "hip")],
        "seiyunchin": [("shiko", "kakiwake_low", "kakiwake_low", "zenkutsu_R", "hip", "gedan_tsuki"),
                       ("shiko", "hip", "yoko_empi", "zenkutsu_L", "kamae", "hip")],
        "shisochin": [("sanchin_R", "hip", "nukite", "sanchin_L", "kamae", "hip"),
                      ("sanchin_L", "shotei", "shotei", "zenkutsu_R", "hip", "tsuki")],
        "seisan": [("sanchin_R", "chudan_uke", "chudan_uke", "zenkutsu_R", "hip", "tsuki"),
                   ("hiza_R", "grab_pull", "grab_pull", "kosa_L", "osae", "osae")],
        "seipai": [("shiko", "hiki_uke", "chest_guard", "zenkutsu_R", "hip", "tsuki"),
                   ("kosa_R", "hammer_down", "hip", "zenkutsu_L", "kamae", "hip")],
        "kururunfa": [("neko_R", "chest_guard", "kake_uke", "zenkutsu_R", "hip", "tsuki"),
                      ("kansetsu_R", "chest_guard", "osae", "zenkutsu_R", "hip", "tsuki")],
        "suparinpei": [("sanchin_R", "nukite", "nukite", "sanchin_L", "kamae", "kamae"),
                       ("sagi_side_R", "chudan_uke", "kake_uke", "zenkutsu_R", "hip", "tsuki")],
    }
    for k, pairs in B.items():
        for i, (ds, dl, dr, as_, al, ar) in enumerate(pairs, 1):
            # front-view stances cannot face the partner; swap to side equivalents
            sub = {"heiko": "sanchin_L", "shiko": "shiko_side_L"}
            ds2 = sub.get(ds, ds)
            if STANCES[ds2]["view"] == "side":
                conv = {"prayer": "chest_guard", "kakiwake_low": "kakiwake_low", "yoko_empi": "empi"}
                dl2, dr2 = conv.get(dl, dl), conv.get(dr, dr)
            pair(f"bk_{k}_{i}", ds2, dl2, dr2, as_, al, ar, "")


def notation():
    fig, ax = canvas(w=4.5, h=3.2, ylim=(0, 71))
    # sample cell
    ax.add_patch(Rectangle((2, 20), 40, 48, fc=WHITE, ec=INK, lw=0.6))
    ax.add_patch(Rectangle((2, 62.8), 5.2, 5.2, fc=INK))
    label(ax, 4.6, 65.4, "9", fs=7, c=WHITE, fontweight="bold")
    direction_icon(ax, 38, 64.4, "N", r=2.4)
    gy = 33
    ground(ax, 6, 38, gy)
    figure(ax, 20, gy, "sanchin_R", L="hip", R="chudan_uke", s=2.6)
    label(ax, 22, 27, "Right sanchin dachi · right chudan uke", fs=5.8)
    label(ax, 22, 23, "Root the stance", fs=5.2, style="italic", c=DARK)
    notes = [(64.5, "Count number, as called in the dojo"), (58, "Facing: arrow shows the compass\ndirection the chest faces"),
             (47, "White limbs = the performer's left side\nGrey limbs = the right side, further away"),
             (33, "Ground line: weight and knee bend"), (24, "Stance · technique, then the coaching cue")]
    targets = [(6, 64.5), (38, 61.5), (24, 47), (36, 33), (40, 25)]
    for (yy, t), (tx, ty) in zip(notes, targets):
        label(ax, 50, yy, t, fs=6.0, ha="left", linespacing=1.1)
        ax.plot([tx + 1, 49], [ty, yy], color=MID, lw=0.5)
    # station legend
    ax.add_patch(Circle((8, 9), 2, fc=INK, ec=INK)); label(ax, 8, 9, "A", fs=6, c=WHITE, fontweight="bold")
    ax.add_patch(Circle((14, 9), 2, fc=WHITE, ec=INK, lw=0.8)); label(ax, 14, 9, "B", fs=6, fontweight="bold")
    label(ax, 19, 9, "Embusen maps: black station = start and finish; lettered stations list every count performed there.",
          fs=5.8, ha="left")
    save(fig, "fig_notation")


def embusen_shapes():
    fig, ax = canvas(w=4.5, h=1.7, ylim=(0, 38))
    shapes = [("I  (ichi)", [((0, -1), (0, 1))]), ("T", [((-1, 1), (1, 1)), ((0, 1), (0, -1))]),
              ("+  (jūji)", [((-1, 0), (1, 0)), ((0, -1), (0, 1))]), ("X  (diagonal)", [((-1, -1), (1, 1)), ((-1, 1), (1, -1))]),
              ("Box / square", [((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))])]
    for i, (name, segs) in enumerate(shapes):
        cx = 10 + i * 20; cy = 21
        for (a, b) in segs:
            ax.plot([cx + a[0] * 7, cx + b[0] * 7], [cy + a[1] * 9, cy + b[1] * 9], color=INK, lw=1.6, solid_capstyle="round")
        ax.add_patch(Circle((cx, cy - (9 if name.startswith(("I", "T")) else 0)), 1.3, fc=INK))
        label(ax, cx, 4, name, fs=6.2)
    save(fig, "fig_embusen_shapes")


def practice_cycle():
    fig, ax = canvas(w=4.5, h=3.0, ylim=(0, 66.7))
    items = ["Kihon\n(basics)", "Kata\n(form)", "Bunkai\n(analysis)", "Kakie\n(pushing hands)", "Kumite\n(applied)", "Hojo undō\n(conditioning)"]
    cx, cy, R = 50, 33, 23
    for i, t in enumerate(items):
        a = math.radians(90 - i * 60)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        ax.add_patch(Circle((x, y), 7.4, fc=WHITE, ec=INK, lw=0.9, zorder=5))
        label(ax, x, y, t, fs=5.8, zorder=6, linespacing=1.05)
        a2 = math.radians(90 - (i + 1) * 60)
        a_s, a_e = a - math.radians(18), a2 + math.radians(18)
        arrow(ax, cx + R * math.cos(a_s), cy + R * math.sin(a_s), cx + R * math.cos(a_e), cy + R * math.sin(a_e),
              lw=0.8, ms=5, rad=-0.25)
    ax.add_patch(Circle((cx, cy), 8, fc=INK, ec=INK))
    label(ax, cx, cy, "Sanchin\n& Tenshō", fs=6.2, c=WHITE, fontweight="bold")
    save(fig, "fig_cycle")


def grading_ladder():
    fig, ax = canvas(w=4.5, h=4.6, ylim=(0, 102))
    rows = [("10th–9th kyū", "Gekisai Dai Ichi", "Sanchin (introduction)"),
            ("8th–7th kyū", "Gekisai Dai Ni", "Sanchin, Tenshō intro"),
            ("6th–5th kyū", "Saifa", "Gekisai bunkai"),
            ("4th–3rd kyū", "Seiyunchin", "Saifa bunkai, Tenshō"),
            ("2nd–1st kyū", "Shisochin", "Seiyunchin bunkai, kakie"),
            ("Shodan", "Sanseiru* / Seisan", "free choice of a lower kata"),
            ("Nidan", "Seisan / Seipai", "bunkai of grading kata"),
            ("Sandan", "Seipai / Kururunfa", "bunkai, teaching assessment"),
            ("Yondan +", "Kururunfa / Suparinpei", "thesis or demonstration")]
    label(ax, 3, 98, "GRADE", fs=6.4, ha="left", fontweight="bold")
    label(ax, 33, 98, "TYPICAL KATA", fs=6.4, ha="left", fontweight="bold")
    label(ax, 66, 98, "ALSO EXAMINED", fs=6.4, ha="left", fontweight="bold")
    ax.plot([2, 98], [95.5, 95.5], color=INK, lw=0.9)
    for i, (g, k, a) in enumerate(rows):
        y = 89 - i * 9.4
        fill = PALE if i % 2 == 0 else WHITE
        ax.add_patch(Rectangle((2, y - 4.4), 96, 8.8, fc=fill, ec="none"))
        w = 4 + i * 2.3
        ax.add_patch(Rectangle((3, y - 1.5), w, 3, fc=INK if i >= 5 else WHITE, ec=INK, lw=0.6))
        label(ax, 3 + w + 1.5, y, g, fs=6.4, ha="left", fontweight="bold")
        label(ax, 33, y, k, fs=6.4, ha="left")
        label(ax, 66, y, a, fs=5.9, ha="left", c=DARK)
    ax.plot([2, 98], [3.6, 3.6], color=INK, lw=0.9)
    label(ax, 50, 1.0, "*Sanseiru is outside the scope of this book. Syllabuses vary: always check your association's.", fs=5.4, style="italic")
    save(fig, "fig_ladder")


def scoring():
    fig, ax = plt.subplots(figsize=(4.5, 2.4))
    crit = ["Stances", "Breathing", "Kime / focus", "Rhythm & speed", "Embusen accuracy", "Eyes (chakugan)", "Bunkai"]
    w = [20, 12, 18, 14, 12, 8, 16]
    ax.barh(crit[::-1], w[::-1], color=WHITE, edgecolor=INK, hatch="////", lw=0.8)
    for i, v in enumerate(w[::-1]):
        ax.text(v + 0.4, i, f"{v}%", va="center", fontsize=6.6)
    ax.set_xlim(0, 25); ax.set_xlabel("Typical share of the examiner's attention (illustrative)", fontsize=6.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=6.8)
    save(fig, "fig_scoring")


def kata_families():
    fig, ax = canvas(w=4.5, h=2.6, ylim=(0, 58))
    cols = [("Heishugata\n(closed hand)", ["Sanchin", "Tenshō"]),
            ("Fukyūgata\n(promotional)", ["Gekisai Dai Ichi", "Gekisai Dai Ni"]),
            ("Kaishugata\n(open hand)", ["Saifa", "Seiyunchin", "Shisochin", "Sanseiru", "Seisan", "Seipai", "Kururunfa", "Suparinpei"])]
    for i, (h, ks) in enumerate(cols):
        x = 2 + i * 33
        box(ax, x, 45, 30, 11, h, fs=6.6, bold=True, fc=INK, tc=WHITE)
        for j, k in enumerate(ks):
            yy = 39 - j * 4.9
            ax.add_patch(Rectangle((x, yy - 2.1), 30, 4.3, fc=WHITE if k != "Sanseiru" else PALE, ec=INK, lw=0.5))
            label(ax, x + 15, yy, k + (" (not covered)" if k == "Sanseiru" else ""), fs=5.9)
    save(fig, "fig_families")


def part_openers():
    poses = [("heiko", "yoi_fist", "yoi_fist"), ("zenkutsu_L", "age_uke", "hip"), ("shiko", "uraken", "gedan_barai"),
             ("neko_L", "tora_top", "tora_low")]
    for i, (st, l, r) in enumerate(poses, 1):
        fig, ax = canvas(w=4.5, h=2.6, ylim=(0, 57.8))
        ax.plot([5, 95], [6, 6], color=INK, lw=1.2)
        figure(ax, 50, 6, st, L=l, R=r, s=4.6)
        for k in range(5):
            ax.add_patch(Circle((50, 30), 24 + k * 6, fc="none", ec=PALE, lw=0.8, zorder=0))
        save(fig, f"part{i}")


def cover():
    fig = plt.figure(figsize=(6, 9))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 60); ax.set_ylim(0, 90); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 60, 90, fc=INK))
    ax.add_patch(Rectangle((2.2, 2.2), 55.6, 85.6, fc="none", ec=WHITE, lw=1.0))
    ax.add_patch(Rectangle((3.0, 3.0), 54, 84, fc="none", ec=WHITE, lw=0.4))
    ax.text(30, 80.5, "GŌJŪ-RYŪ", color=WHITE, fontsize=40, ha="center", va="center", fontweight="bold", family="EB Garamond")
    ax.text(30, 72.8, "KARATE KATA BIBLE", color=WHITE, fontsize=24, ha="center", va="center", family="EB Garamond",
            fontweight="semibold")
    ax.plot([18, 42], [68.6, 68.6], color=WHITE, lw=1.0)
    sub = ("Illustrated Textbook With Full Diagram Sequences for\nGekisai, Saifa, Seiyunchin, Shisochin, Seisan,\n"
           "Seipai, Kururunfa, and Suparinpei With Grading Notes")
    ax.text(30, 63.0, sub, color=WHITE, fontsize=10.5, ha="center", va="center", family="Source Sans 3", linespacing=1.35)
    # emblem: white disc with figure
    ax.add_patch(Circle((30, 34), 19, fc=WHITE, ec=WHITE))
    ax.add_patch(Circle((30, 34), 17.8, fc="none", ec=INK, lw=0.8))
    ax.plot([16.5, 43.5], [19.5, 19.5], color=INK, lw=1.2)
    figure(ax, 31, 19.5, "neko_L", L="tora_top", R="tora_low", s=3.0)
    ax.text(30, 9.0, "DR BEVERLY J. STIVERS", color=WHITE, fontsize=15, ha="center", va="center", family="EB Garamond",
            fontweight="semibold")
    fig.savefig(FIG / "cover.png", dpi=300, facecolor=INK)
    plt.close(fig)


if __name__ == "__main__":
    lineage(); timeline()
    stances(1, STANCE_INFO[:4]); stances(2, STANCE_INFO[4:])
    sanchin_detail(); levels(); breathing(); techniques(1); techniques(2); mawashi(); kakie(); bunkai()
    notation(); embusen_shapes(); practice_cycle(); grading_ladder(); scoring(); kata_families(); part_openers(); cover()
    print("done")
