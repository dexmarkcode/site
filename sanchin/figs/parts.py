"""Part-opener and title-page vignettes: a single figure inside an ensō-like ring."""
from common import *

VIGNETTES = {
    "title": (Pose("uke", "uke", "sanchin", "R"), -35),
    "part1": (Pose("yoi", "yoi", "musubi"), 0),
    "part2": (Pose("uke", "uke", "sanchin", "R"), 0),
    "part3": (Pose("palm_chest", "palm_chest", "sanchin", "L"), -30),
    "part4": (Pose("tsuki", "hikite", "sanchin", "L"), -90),
    "part5": (Pose("uke", "tsuki", "sanchin", "R"), -40),
    "part6": (Pose("uke", "uke", "sanchin", "R"), 30),
    "part7": (Pose("uke", "uke", "sanchin", "L"), -90),
    "part8": (Pose("side_fist", "side_fist", "shiko"), 0),
    "part9": (Pose("tora_up", "tora_down", "sanchin", "R"), -30),
}

for name, (pose, th) in VIGNETTES.items():
    fig, ax = canvas(2.2, 2.2, xlim=(-60, 60), ylim=(-60, 60))
    t = np.linspace(0.35, 2 * math.pi - 0.15, 300)
    r = 54 + 1.2 * np.sin(t * 3)
    wdt = 0.6 + 2.2 * np.sin((t - 0.35) / (2 * math.pi - 0.5) * math.pi) ** 1.5
    for k in range(len(t) - 1):
        ax.plot(r[k:k+2] * np.cos(t[k:k+2]), r[k:k+2] * np.sin(t[k:k+2]), color=K, lw=wdt[k], solid_capstyle="round")
    Figure(ax, pose, ox=0, oy=-45, sc=0.86, th=th)
    ax.plot([-30, 30], [-45, -45], color=K, lw=0.6)
    save(fig, name)
