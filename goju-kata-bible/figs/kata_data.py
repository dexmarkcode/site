"""Movement data for every kata in the book.

Each move:  n, facing, stance (figure), L arm, R arm, floor position (x, y in step units),
text (stance - technique), note (breath / tempo / detail), kiai flag, optional footprint key.
Positions are on a grid where the performer starts at (0, 0) facing north (shomen).

The same records drive the sequence strips, the embusen maps and the tables in the text,
so the diagrams and the written counts always agree.
"""

FP_OF = {
    "musubi": "musubi", "heiko": "heiko", "hachiji": "hachiji", "shiko": "shiko", "sanchin_f": "sanchin_R",
    "sagi_L": "sagi_L", "sagi_R": "sagi_R", "kosa_f": "kosa_L", "seiza": "heiko",
}
for _s in ("L", "R"):
    for _base in ("zenkutsu", "sanchin", "neko", "kokutsu", "kosa"):
        FP_OF[f"{_base}_{_s}"] = f"{_base}_{_s}"
    FP_OF[f"shiko_side_{_s}"] = "shiko"
    FP_OF[f"sagi_side_{_s}"] = f"sagi_{_s}"
    FP_OF[f"geri_{_s}"] = f"sagi_{_s}"
    FP_OF[f"kansetsu_{_s}"] = f"sagi_{_s}"
    FP_OF[f"hiza_{_s}"] = f"sagi_{_s}"
FP_OF["musubi_side"] = "musubi"


def M(n, d, st, L, R, pos, txt, note="", k=False, fp=None, fpd=None):
    return dict(n=n, d=d, st=st, L=L, R=R, pos=pos, txt=txt, note=note, k=k,
                fp=fp or FP_OF.get(st, "heiko"), fpd=fpd or d)


OPEN = [
    M("Rei", "N", "musubi", "side_down", "side_down", (0, 0), "Musubi dachi · bow (rei)", "Eyes stay on the examiner"),
    M("Yoi", "N", "musubi", "yoi_open", "yoi_open", (0, 0), "Musubi dachi · open hands, left over right", "Slow nasal breath in"),
]


def close(n, pos=(0, 0)):
    return [M(n, "N", "musubi", "yoi_open", "yoi_open", pos, "Naore · musubi dachi, open hands", "Zanshin; breathe out quietly")]


# ---------------------------------------------------------------- Gekisai Dai Ichi
GEKISAI1 = OPEN + [
    M(1, "N", "heiko", "yoi_fist", "yoi_fist", (0, 0), "Heiko dachi · fists in front of thighs", "Ready position"),
    M(2, "W", "zenkutsu_L", "age_uke", "hip", (-1.3, 0), "Left zenkutsu dachi · left jodan age uke", "Look first, then step"),
    M(3, "W", "zenkutsu_R", "hip", "jodan_tsuki", (-2.6, 0), "Step: right zenkutsu dachi · right jodan tsuki", "Fast; full hikite"),
    M(4, "N", "heiko", "yoi_fist", "yoi_fist", (0, 0), "Draw back to heiko dachi facing front", "Settle the breath"),
    M(5, "E", "zenkutsu_R", "hip", "age_uke", (1.3, 0), "Right zenkutsu dachi · right jodan age uke", "Mirror of count 2"),
    M(6, "E", "zenkutsu_L", "jodan_tsuki", "hip", (2.6, 0), "Step: left zenkutsu dachi · left jodan tsuki", "Fast"),
    M(7, "N", "heiko", "yoi_fist", "yoi_fist", (0, 0), "Draw back to heiko dachi facing front", ""),
    M(8, "N", "zenkutsu_L", "age_uke", "hip", (0, 1.3), "Left zenkutsu dachi · left jodan age uke", "Forward line"),
    M(9, "N", "sanchin_R", "hip", "chudan_uke", (0, 2.3), "Step: right sanchin dachi · right chudan uke", "Root the stance"),
    M(10, "N", "geri_R", "hip", "chudan_uke", (0, 2.8), "Right mae geri", "Chamber high; guard holds"),
    M(11, "N", "zenkutsu_R", "hip", "empi", (0, 3.5), "Land right zenkutsu dachi · right mae empi uchi", "Elbow on landing"),
    M(12, "W", "shiko", "hip", "uraken", (0, 3.5), "Turn hips to shiko dachi · right uraken uchi", "Snap and return", fpd="W"),
    M(13, "W", "shiko", "hip", "gedan_barai", (0, 3.5), "Shiko dachi · right gedan barai", "", fpd="W"),
    M(14, "N", "zenkutsu_R", "tsuki", "hip", (0, 3.5), "Right zenkutsu dachi · left gyaku tsuki", "Kiai", k=True),
    M(15, "S", "sanchin_L", "chudan_uke", "hip", (0, 3.0), "Turn: left sanchin dachi · left chudan uke", "Turn on the balls of the feet"),
    M(16, "S", "geri_L", "chudan_uke", "hip", (0, 2.5), "Left mae geri", ""),
    M(17, "S", "zenkutsu_L", "empi", "hip", (0, 1.8), "Land left zenkutsu dachi · left mae empi uchi", ""),
    M(18, "E", "shiko", "uraken", "hip", (0, 1.8), "Shiko dachi · left uraken uchi", "", fpd="E"),
    M(19, "E", "shiko", "gedan_barai", "hip", (0, 1.8), "Shiko dachi · left gedan barai", "", fpd="E"),
    M(20, "S", "zenkutsu_L", "hip", "tsuki", (0, 1.8), "Left zenkutsu dachi · right gyaku tsuki", ""),
    M(21, "N", "zenkutsu_L", "chudan_uke", "hip", (0, 1.0), "Turn: left zenkutsu dachi · left chudan uke", "Facing front again"),
    M(22, "N", "zenkutsu_L", "hip", "tsuki", (0, 1.0), "Right gyaku tsuki", ""),
    M(23, "N", "zenkutsu_R", "hip", "chudan_uke", (0, 0.9), "Step back: right zenkutsu dachi · right chudan uke", "Retreating line"),
    M(24, "N", "zenkutsu_R", "tsuki", "hip", (0, 0.9), "Left gyaku tsuki", ""),
    M(25, "N", "heiko", "cross_low", "cross_low", (0, 0), "Draw back to heiko dachi · open hands cross low", "Slow"),
] + close(26)

# ---------------------------------------------------------------- Gekisai Dai Ni
GEKISAI2 = OPEN + [g for g in GEKISAI1[2:9]] + [
    M(8, "N", "zenkutsu_L", "age_uke", "hip", (0, 1.3), "Left zenkutsu dachi · left jodan age uke", "Forward line"),
    M(9, "N", "neko_R", "hip", "kake_uke", (0, 2.2), "Step: right neko ashi dachi · right kake uke", "Open hand hooks and controls"),
    M(10, "N", "geri_R", "hip", "kake_uke", (0, 2.7), "Right mae geri", "Same as Dai Ichi"),
    M(11, "N", "zenkutsu_R", "hip", "empi", (0, 3.4), "Land right zenkutsu dachi · right mae empi uchi", ""),
    M(12, "W", "shiko", "hip", "uraken", (0, 3.4), "Shiko dachi · right uraken uchi", "", fpd="W"),
    M(13, "W", "shiko", "hip", "gedan_barai", (0, 3.4), "Shiko dachi · right gedan barai", "", fpd="W"),
    M(14, "N", "zenkutsu_R", "tsuki", "hip", (0, 3.4), "Right zenkutsu dachi · left gyaku tsuki", "Kiai", k=True),
    M(15, "S", "neko_L", "kake_uke", "hip", (0, 2.9), "Turn: left neko ashi dachi · left kake uke", ""),
    M(16, "S", "geri_L", "kake_uke", "hip", (0, 2.4), "Left mae geri", ""),
    M(17, "S", "zenkutsu_L", "empi", "hip", (0, 1.7), "Land left zenkutsu dachi · left mae empi uchi", ""),
    M(18, "E", "shiko", "uraken", "hip", (0, 1.7), "Shiko dachi · left uraken uchi", "", fpd="E"),
    M(19, "E", "shiko", "gedan_barai", "hip", (0, 1.7), "Shiko dachi · left gedan barai", "", fpd="E"),
    M(20, "S", "zenkutsu_L", "hip", "tsuki", (0, 1.7), "Left zenkutsu dachi · right gyaku tsuki", ""),
    M(21, "N", "neko_L", "tora_top", "tora_low", (0, 0.9), "Turn: left neko ashi dachi · mawashi uke", "Circle, then double palm push"),
    M(22, "N", "neko_L", "shotei", "shotei", (0, 0.9), "Morote shotei · tora guchi", "Exhale through the push"),
    M(23, "N", "neko_R", "shotei", "shotei", (0, 0.4), "Step back: right neko ashi dachi · mawashi uke", "Mirror"),
] + close(24)

# ---------------------------------------------------------------- Saifa
SAIFA = OPEN + [
    M(1, "N", "heiko", "yoi_fist", "yoi_fist", (0, 0), "Heiko dachi · yoi", ""),
    M(2, "NE", "heiko", "prayer", "prayer", (0.9, 0.9), "Step right to NE, left foot closes · right fist in left palm", "Pull up and across: the release"),
    M(3, "NE", "shiko", "osae", "uraken", (0.4, 0.4), "Left foot back to shiko dachi · right uraken, left palm presses", "Elbow drives out first", fpd="NE"),
    M(4, "NW", "heiko", "prayer", "prayer", (-0.9, 0.9), "Step left to NW, right closes · left fist in right palm", "Mirror"),
    M(5, "NW", "shiko", "uraken", "osae", (-0.4, 0.4), "Right foot back to shiko dachi · left uraken, right palm presses", "", fpd="NW"),
    M(6, "NE", "heiko", "prayer", "prayer", (0.9, 0.9), "Step right to NE, left closes · release again", "Third repetition"),
    M(7, "NE", "shiko", "osae", "uraken", (0.4, 0.4), "Shiko dachi · right uraken, left palm presses", "", fpd="NE"),
    M(8, "N", "sagi_R", "cross_high", "cross_high", (0, 0.5), "Left leg supports, right knee lifts · forearms rise and part", "Receive the two-hand push"),
    M(9, "N", "geri_R", "kamae", "kamae", (0, 1.0), "Right mae geri", ""),
    M(10, "N", "zenkutsu_R", "hip", "hammer_down", (0, 1.7), "Land right zenkutsu dachi · right gedan tettsui", "Kiai", k=True),
    M(11, "S", "sagi_L", "cross_high", "cross_high", (0, 1.4), "Turn to south: right leg supports, left knee lifts · forearms part", ""),
    M(12, "S", "geri_L", "kamae", "kamae", (0, 0.9), "Left mae geri", ""),
    M(13, "S", "zenkutsu_L", "hammer_down", "hip", (0, 0.2), "Land left zenkutsu dachi · left gedan tettsui", "Kiai", k=True),
    M(14, "W", "zenkutsu_L", "kake_uke", "hip", (-1.0, 0.2), "Turn west: left zenkutsu dachi · left kake uke", "Hand hooks and draws"),
    M(15, "W", "zenkutsu_L", "hip", "tettsui", (-1.0, 0.2), "Right tettsui uchi over the top", "Hips turn in"),
    M(16, "E", "zenkutsu_R", "hip", "kake_uke", (1.0, 0.2), "Turn east: right zenkutsu dachi · right kake uke", "Mirror"),
    M(17, "E", "zenkutsu_R", "tettsui", "hip", (1.0, 0.2), "Left tettsui uchi", ""),
    M(18, "N", "neko_L", "tora_top", "tora_low", (0, 0.2), "Turn front: left neko ashi dachi · mawashi uke", "Circle and push out"),
] + close(19)

# ---------------------------------------------------------------- Seiyunchin
SEIYUNCHIN = OPEN + [
    M(1, "N", "heiko", "yoi_open", "yoi_open", (0, 0), "Heiko dachi · open hands", ""),
    M(2, "NE", "shiko", "cross_high", "cross_high", (0.9, 0.9), "Step right to NE into shiko dachi · arms cross at chest", "Slow, breathe in", fpd="NE"),
    M(3, "NE", "shiko", "kakiwake_low", "kakiwake_low", (0.9, 0.9), "Shiko dachi · morote gedan uke (open hands part down)", "Slow, ibuki out", fpd="NE"),
    M(4, "NE", "shiko", "hiki_uke", "hip", (0.9, 0.9), "Left hiki uke rises, right fist to hip", "Grasp", fpd="NE"),
    M(5, "NE", "shiko", "grab_pull", "tsuki", (0.9, 0.9), "Left pulls to the hip, right chudan tsuki", "", fpd="NE"),
    M(6, "NW", "shiko", "cross_high", "cross_high", (-0.9, 0.9), "Step left to NW into shiko dachi · arms cross", "Mirror", fpd="NW"),
    M(7, "NW", "shiko", "kakiwake_low", "kakiwake_low", (-0.9, 0.9), "Morote gedan uke", "", fpd="NW"),
    M(8, "NW", "shiko", "hip", "hiki_uke", (-0.9, 0.9), "Right hiki uke, left fist to hip", "", fpd="NW"),
    M(9, "NW", "shiko", "tsuki", "grab_pull", (-0.9, 0.9), "Right pulls, left chudan tsuki", "", fpd="NW"),
    M(10, "NE", "shiko", "kakiwake_low", "kakiwake_low", (0.9, 1.8), "Step right to NE · morote gedan uke", "Third diagonal", fpd="NE"),
    M(11, "NE", "shiko", "grab_pull", "tsuki", (0.9, 1.8), "Hiki uke and chudan tsuki", "", fpd="NE"),
    M(12, "N", "zenkutsu_L", "nukite", "hip", (0, 2.6), "Step left: left zenkutsu dachi · left nukite", "Fast"),
    M(13, "W", "shiko", "hip", "yoko_empi", (0, 2.6), "Shiko dachi · right yoko empi", "Pull the opponent onto it", fpd="W"),
    M(14, "W", "shiko", "hip", "uraken", (0, 2.6), "Right uraken uchi", "", fpd="W"),
    M(15, "W", "shiko", "hip", "gedan_barai", (0, 2.6), "Right gedan barai", "", fpd="W"),
    M(16, "N", "zenkutsu_R", "hip", "nukite", (0, 3.4), "Step right: right zenkutsu dachi · right nukite", ""),
    M(17, "E", "shiko", "yoko_empi", "hip", (0, 3.4), "Shiko dachi · left yoko empi", "", fpd="E"),
    M(18, "E", "shiko", "uraken", "hip", (0, 3.4), "Left uraken uchi", "", fpd="E"),
    M(19, "E", "shiko", "gedan_barai", "hip", (0, 3.4), "Left gedan barai", "Kiai", k=True, fpd="E"),
    M(20, "S", "kosa_L", "osae", "tsuki", (0, 2.9), "Turn: kosa dachi · left osae, right shita tsuki", "Drop and press"),
    M(21, "S", "shiko_side_L", "uchi_uke_f", "hip", (0, 2.4), "Shiko dachi · left chudan uchi uke", ""),
    M(22, "S", "shiko_side_L", "hip", "tsuki", (0, 2.4), "Right chudan tsuki", ""),
    M(23, "N", "neko_L", "tora_top", "tora_low", (0, 1.4), "Turn: left neko ashi dachi · mawashi uke", "Close the kata"),
] + close(24)

# ---------------------------------------------------------------- Shisochin
SHISOCHIN = OPEN + [
    M(1, "N", "heiko", "yoi_open", "yoi_open", (0, 0), "Heiko dachi · open hands", ""),
    M(2, "N", "sanchin_R", "kamae", "kamae", (0, 0.9), "Step right: right sanchin dachi · kaishu morote chudan uke", "Slow, dynamic tension"),
    M(3, "N", "sanchin_R", "hip", "nukite", (0, 0.9), "Right yonhon nukite", "Slow, exhale"),
    M(4, "N", "sanchin_L", "nukite", "hip", (0, 1.8), "Step left: left sanchin dachi · left yonhon nukite", "Slow"),
    M(5, "N", "sanchin_R", "hip", "nukite", (0, 2.7), "Step right: right sanchin dachi · right yonhon nukite", "Slow"),
    M(6, "N", "sanchin_R", "kake_uke", "shotei", (0, 2.7), "Right kake uke · left shotei", "Fast"),
    M(7, "N", "sanchin_L", "shotei", "shotei", (0, 1.9), "Step back: left sanchin dachi · morote shotei oshi", "Double palm push"),
    M(8, "E", "shiko", "hip", "yoko_shotei", (0.6, 1.9), "Turn east: shiko dachi · right yoko shotei", "", fpd="N"),
    M(9, "W", "shiko", "yoko_shotei", "hip", (-0.6, 1.9), "Turn west: shiko dachi · left yoko shotei", "", fpd="N"),
    M(10, "NE", "zenkutsu_R", "hip", "kake_uke", (0.8, 2.6), "Step to NE: right zenkutsu dachi · right kake uke", ""),
    M(11, "NE", "kansetsu_R", "hip", "kake_uke", (1.1, 2.9), "Right kansetsu geri", "Stamp through the knee"),
    M(12, "NE", "zenkutsu_R", "hip", "empi", (1.4, 3.2), "Land · right empi uchi", ""),
    M(13, "NW", "zenkutsu_L", "kake_uke", "hip", (-0.8, 2.6), "Step to NW: left zenkutsu dachi · left kake uke", "Mirror"),
    M(14, "NW", "kansetsu_L", "kake_uke", "hip", (-1.1, 2.9), "Left kansetsu geri", ""),
    M(15, "NW", "zenkutsu_L", "empi", "hip", (-1.4, 3.2), "Land · left empi uchi", ""),
    M(16, "N", "shiko", "grab_pull", "uraken", (0, 3.5), "Shiko dachi · right uraken, left pulls", "", fpd="W"),
    M(17, "N", "shiko", "grab_pull", "gedan_barai", (0, 3.5), "Right gedan barai", "Kiai", k=True, fpd="W"),
    M(18, "S", "sanchin_L", "kake_uke", "hip", (0, 2.6), "Turn south: left sanchin dachi · left kake uke", ""),
    M(19, "S", "sanchin_L", "hip", "shotei", (0, 2.6), "Right shotei", ""),
    M(20, "N", "neko_L", "tora_top", "tora_low", (0, 1.6), "Turn: left neko ashi dachi · mawashi uke", ""),
] + close(21)

# ---------------------------------------------------------------- Seisan
SEISAN = OPEN + [
    M(1, "N", "heiko", "yoi_fist", "yoi_fist", (0, 0), "Heiko dachi · yoi", ""),
    M(2, "N", "sanchin_R", "chudan_uke", "chudan_uke", (0, 0.9), "Step right: right sanchin dachi · morote chudan uke", "Moderate speed"),
    M(3, "N", "sanchin_R", "hip", "tsuki", (0, 0.9), "Right chudan tsuki", ""),
    M(4, "N", "sanchin_R", "chudan_uke", "hip", (0, 0.9), "Right fist withdraws · left chudan uke", ""),
    M(5, "N", "sanchin_L", "tsuki", "hip", (0, 1.8), "Step left: left sanchin dachi · left tsuki", ""),
    M(6, "N", "sanchin_R", "hip", "tsuki", (0, 2.7), "Step right: right sanchin dachi · right tsuki", ""),
    M(7, "N", "sanchin_R", "tsuki", "hip", (0, 2.7), "Renzuki: left, right, left, right", "Fast, short breath"),
    M(8, "N", "sanchin_R", "hip", "kake_uke", (0, 2.7), "Right kake uke · nukite follow-up", "Open hand"),
    M(9, "S", "sanchin_L", "chudan_uke", "hip", (0, 2.1), "Turn south: left sanchin dachi · left chudan uke", ""),
    M(10, "S", "sanchin_L", "hip", "tsuki", (0, 2.1), "Right chudan tsuki", ""),
    M(11, "SE", "zenkutsu_R", "hip", "gedan_barai", (0.8, 1.4), "Step to SE: right zenkutsu dachi · right gedan barai", ""),
    M(12, "SE", "hiza_R", "grab_pull", "grab_pull", (1.0, 1.2), "Both hands draw down · right hiza geri", "Pull the head onto the knee"),
    M(13, "SW", "zenkutsu_L", "gedan_barai", "hip", (-0.8, 1.4), "Step to SW: left zenkutsu dachi · left gedan barai", "Mirror"),
    M(14, "SW", "hiza_L", "grab_pull", "grab_pull", (-1.0, 1.2), "Left hiza geri", ""),
    M(15, "N", "sanchin_L", "kake_uke", "hip", (0, 1.6), "Turn front: left sanchin dachi · left kake uke", ""),
    M(16, "N", "kansetsu_R", "kake_uke", "hip", (0, 2.0), "Right kansetsu geri", "Stamp low"),
    M(17, "N", "zenkutsu_R", "hip", "empi_up", (0, 2.5), "Land right zenkutsu dachi · right age empi", ""),
    M(18, "N", "zenkutsu_R", "hip", "uraken", (0, 2.5), "Right uraken uchi", ""),
    M(19, "N", "shiko", "grab_pull", "gedan_barai", (0, 2.5), "Shiko dachi · right gedan barai", "Kiai", k=True, fpd="W"),
    M(20, "N", "neko_L", "tora_top", "tora_low", (0, 1.4), "Step back: left neko ashi dachi · mawashi uke", ""),
] + close(21)

# ---------------------------------------------------------------- Seipai
SEIPAI = OPEN + [
    M(1, "N", "heiko", "yoi_open", "yoi_open", (0, 0), "Heiko dachi · open hands", ""),
    M(2, "NW", "shiko", "hiki_uke", "chest_guard", (-0.8, -0.8), "Right foot steps back to SE: shiko dachi facing NW · slow hiki uke", "Slow, dynamic", fpd="NW"),
    M(3, "NW", "shiko", "grab_pull", "hiji_up", (-0.8, -0.8), "Left pulls · right age hiji", "Fast", fpd="NW"),
    M(4, "NW", "shiko", "grab_pull", "uraken", (-0.8, -0.8), "Right uraken uchi", "", fpd="NW"),
    M(5, "NE", "shiko", "chest_guard", "hiki_uke", (0.8, -0.8), "Mirror to NE: shiko dachi · slow hiki uke", "", fpd="NE"),
    M(6, "NE", "shiko", "hiji_up", "grab_pull", (0.8, -0.8), "Left age hiji", "", fpd="NE"),
    M(7, "NE", "shiko", "uraken", "grab_pull", (0.8, -0.8), "Left uraken uchi", "", fpd="NE"),
    M(8, "N", "neko_L", "kake_uke", "hip", (0, 0), "Left neko ashi dachi · left kake uke", ""),
    M(9, "N", "neko_L", "hip", "shotei", (0, 0), "Right shotei uchi", ""),
    M(10, "N", "kosa_R", "hammer_down", "hip", (0, 0.6), "Drop into kosa dachi · left gedan tettsui", "Low and compact"),
    M(11, "S", "sagi_side_R", "hip", "kake_uke", (0, 0.6), "Spin 360°: right knee lifts · right kake uke", "Turn on the left foot"),
    M(12, "S", "kansetsu_R", "hip", "kake_uke", (0, 0.2), "Right fumikomi / kansetsu geri", ""),
    M(13, "S", "zenkutsu_R", "hip", "tsuki", (0, -0.3), "Right zenkutsu dachi · right chudan tsuki", ""),
    M(14, "N", "zenkutsu_L", "age_uke", "hip", (0, 0.3), "Turn: left zenkutsu dachi · left jodan age uke", ""),
    M(15, "N", "zenkutsu_L", "hip", "tsuki", (0, 0.3), "Right gyaku tsuki", ""),
    M(16, "E", "shiko", "uraken", "hip", (0, 0.3), "Shiko dachi · left uraken", "", fpd="E"),
    M(17, "E", "shiko", "gedan_barai", "hip", (0, 0.3), "Left gedan barai", "Kiai", k=True, fpd="E"),
    M(18, "N", "neko_L", "tora_top", "tora_low", (0, -0.3), "Step back: left neko ashi dachi · mawashi uke", ""),
] + close(19)

# ---------------------------------------------------------------- Kururunfa
KURURUNFA = OPEN + [
    M(1, "N", "heiko", "yoi_open", "yoi_open", (0, 0), "Heiko dachi · open hands", ""),
    M(2, "NE", "neko_R", "chest_guard", "kake_uke", (0.8, 0.8), "Step to NE: right neko ashi dachi · slow right kake uke", "Slow, breathe in"),
    M(3, "NE", "kansetsu_R", "chest_guard", "osae", (1.0, 1.0), "Right kansetsu geri · right hand presses down", "Sudden"),
    M(4, "NE", "neko_R", "hip", "shotei", (1.0, 1.0), "Right shotei uchi", ""),
    M(5, "NW", "neko_L", "kake_uke", "chest_guard", (-0.8, 0.8), "Step to NW: left neko ashi dachi · slow left kake uke", "Mirror"),
    M(6, "NW", "kansetsu_L", "osae", "chest_guard", (-1.0, 1.0), "Left kansetsu geri · left osae", ""),
    M(7, "NW", "neko_L", "shotei", "hip", (-1.0, 1.0), "Left shotei uchi", ""),
    M(8, "SE", "neko_R", "chest_guard", "kake_uke", (0.8, -0.8), "Turn SE: right neko ashi dachi · kake uke", "Third corner"),
    M(9, "SE", "kansetsu_R", "chest_guard", "osae", (1.0, -1.0), "Right kansetsu geri · osae", ""),
    M(10, "SW", "neko_L", "kake_uke", "chest_guard", (-0.8, -0.8), "Turn SW: left neko ashi dachi · kake uke", "Fourth corner"),
    M(11, "SW", "kansetsu_L", "osae", "chest_guard", (-1.0, -1.0), "Left kansetsu geri · osae", ""),
    M(12, "N", "sagi_L", "cross_high", "cross_high", (0, 0), "Turn front: left knee lifts · forearms cross high", "Hold"),
    M(13, "N", "shiko", "kakiwake_low", "kakiwake_low", (0, 0.7), "Step down into shiko dachi · open hands part downward", "", fpd="W"),
    M(14, "N", "zenkutsu_R", "hip", "sukui", (0, 1.4), "Right zenkutsu dachi · right sukui uke", "Scoop the leg"),
    M(15, "N", "zenkutsu_R", "hip", "empi", (0, 1.4), "Right mae empi uchi", ""),
    M(16, "W", "shiko", "hip", "uraken", (0, 1.4), "Shiko dachi · right uraken", "", fpd="W"),
    M(17, "W", "shiko", "hip", "tettsui", (0, 1.4), "Right tettsui", "Kiai", k=True, fpd="W"),
    M(18, "N", "neko_L", "tora_top", "tora_low", (0, 0.6), "Step back: left neko ashi dachi · mawashi uke", ""),
] + close(19)

# ---------------------------------------------------------------- Suparinpei
SUPARINPEI = OPEN + [
    M(1, "N", "heiko", "yoi_open", "yoi_open", (0, 0), "Heiko dachi · open hands", ""),
    M(2, "N", "sanchin_R", "kamae", "kamae", (0, 0.9), "Step right: right sanchin dachi · kaishu morote chudan uke", "Slow, like Sanchin"),
    M(3, "N", "sanchin_R", "nukite", "nukite", (0, 0.9), "Morote nihon nukite", "Slow, exhale"),
    M(4, "N", "sanchin_L", "nukite", "nukite", (0, 1.8), "Step left: left sanchin dachi · morote nukite", "Slow"),
    M(5, "N", "sanchin_R", "nukite", "nukite", (0, 2.7), "Step right: right sanchin dachi · morote nukite", "Slow"),
    M(6, "N", "sanchin_L", "shotei", "shotei", (0, 1.8), "Step back: left sanchin dachi · morote shotei", "Fast"),
    M(7, "N", "sanchin_R", "kake_uke", "kake_uke", (0, 0.9), "Step back: right sanchin dachi · morote kake uke", ""),
    M(8, "NE", "shiko", "hip", "yoko_empi", (0.8, 1.5), "Turn NE: shiko dachi · right yoko empi", "", fpd="NE"),
    M(9, "NE", "shiko", "hip", "uraken", (0.8, 1.5), "Right uraken", "", fpd="NE"),
    M(10, "NE", "shiko", "hip", "gedan_barai", (0.8, 1.5), "Right gedan barai", "", fpd="NE"),
    M(11, "NW", "shiko", "yoko_empi", "hip", (-0.8, 1.5), "Turn NW: shiko dachi · left yoko empi", "", fpd="NW"),
    M(12, "NW", "shiko", "uraken", "hip", (-0.8, 1.5), "Left uraken", "", fpd="NW"),
    M(13, "NW", "shiko", "gedan_barai", "hip", (-0.8, 1.5), "Left gedan barai", "", fpd="NW"),
    M(14, "SE", "shiko", "hip", "yoko_empi", (0.8, 0.3), "Turn SE: shiko dachi · right yoko empi", "", fpd="SE"),
    M(15, "SE", "shiko", "hip", "gedan_barai", (0.8, 0.3), "Right uraken · gedan barai", "", fpd="SE"),
    M(16, "SW", "shiko", "yoko_empi", "hip", (-0.8, 0.3), "Turn SW: shiko dachi · left yoko empi", "", fpd="SW"),
    M(17, "SW", "shiko", "gedan_barai", "hip", (-0.8, 0.3), "Left uraken · gedan barai", "", fpd="SW"),
    M(18, "N", "sagi_R", "chudan_uke", "chudan_uke", (0, 1.0), "Right knee lifts · morote chudan uke", ""),
    M(19, "N", "geri_R", "kamae", "kamae", (0, 1.5), "Right mae geri", ""),
    M(20, "N", "zenkutsu_R", "hip", "empi", (0, 2.2), "Right zenkutsu dachi · right empi", ""),
    M(21, "N", "zenkutsu_R", "hip", "uraken", (0, 2.2), "Right uraken", ""),
    M(22, "N", "zenkutsu_R", "tsuki", "hip", (0, 2.2), "Left gyaku tsuki", ""),
    M(23, "S", "sagi_L", "chudan_uke", "chudan_uke", (0, 1.8), "Turn south: left knee lifts · morote chudan uke", ""),
    M(24, "S", "geri_L", "kamae", "kamae", (0, 1.3), "Left mae geri", ""),
    M(25, "S", "zenkutsu_L", "empi", "hip", (0, 0.6), "Left zenkutsu dachi · left empi", ""),
    M(26, "S", "zenkutsu_L", "uraken", "hip", (0, 0.6), "Left uraken", ""),
    M(27, "S", "zenkutsu_L", "hip", "tsuki", (0, 0.6), "Right gyaku tsuki", ""),
    M(28, "N", "kosa_L", "hammer_down", "hip", (0, 1.1), "Turn front, drop into kosa dachi · left gedan tettsui", ""),
    M(29, "N", "neko_L", "kake_uke", "hip", (0, 1.5), "Rise: left neko ashi dachi · left kake uke", ""),
    M(30, "N", "kansetsu_R", "kake_uke", "hip", (0, 1.9), "Right kansetsu geri", ""),
    M(31, "N", "zenkutsu_R", "hip", "sukui", (0, 2.4), "Right zenkutsu dachi · right sukui uke", ""),
    M(32, "N", "shiko", "hip", "tettsui", (0, 2.4), "Shiko dachi · right tettsui", "", fpd="W"),
    M(33, "W", "zenkutsu_L", "kake_uke", "hip", (-1.0, 2.4), "Turn west: left zenkutsu dachi · kake uke", ""),
    M(34, "W", "zenkutsu_L", "hip", "shotei", (-1.0, 2.4), "Right shotei", ""),
    M(35, "E", "zenkutsu_R", "hip", "kake_uke", (1.0, 2.4), "Turn east: right zenkutsu dachi · kake uke", ""),
    M(36, "E", "zenkutsu_R", "shotei", "hip", (1.0, 2.4), "Left shotei", ""),
    M(37, "N", "sanchin_R", "tsuki", "tsuki", (0, 2.4), "Right sanchin dachi · morote tsuki", "Kiai", k=True),
    M(38, "N", "neko_L", "tora_top", "tora_low", (0, 1.4), "Step back: left neko ashi dachi · mawashi uke", ""),
    M(39, "N", "neko_R", "tora_low", "tora_top", (0, 0.7), "Step back: right neko ashi dachi · mawashi uke", ""),
] + close(40)

KATA = {
    "gekisai1": ("Gekisai Dai Ichi", GEKISAI1),
    "gekisai2": ("Gekisai Dai Ni", GEKISAI2),
    "saifa": ("Saifa", SAIFA),
    "seiyunchin": ("Seiyunchin", SEIYUNCHIN),
    "shisochin": ("Shisochin", SHISOCHIN),
    "seisan": ("Seisan", SEISAN),
    "seipai": ("Seipai", SEIPAI),
    "kururunfa": ("Kururunfa", KURURUNFA),
    "suparinpei": ("Suparinpei", SUPARINPEI),
}
