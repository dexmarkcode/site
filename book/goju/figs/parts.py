from body import *
P = [pose("sanchin_r", "kamae"), pose("sanchin_l", lh=(4, -14, 52), rh=(-16, -38, -10)), pose("shiko", lh=(16, -38, -10), rh=(-8, -40, 36)),
     pose("shiko", lh=(16, -38, -10), rh=(-16, -20, 44), props=(("chiishi", "r", (0, 1, 0), 40),)),
     pose("neko_l", lh=(8, -2, 36), rh=(-8, -26, 36), lhand="open", rhand="open")]
V = [0, 70, 25, 60, 50]
for i, (p, v) in enumerate(zip(P, V), 1):
    fig = plt.figure(figsize=(3.3, 2.6))
    ax = fig.add_axes([0, 0, 1, 1])
    render_panel(ax, dict(pose=p, view=v), xr=82)
    fig.savefig(FIG / f"part{i}.png", dpi=300, facecolor="white")
    plt.close(fig)
