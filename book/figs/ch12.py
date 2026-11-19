from common import *


def fig12_1():
    fig, ax = canvas(h=2.6, ylim=(0, 58))
    ax.add_patch(Rectangle((5, 27), 90, 4, fc=TEAL, ec="none"))
    label(ax, 50, 29, "high-voltage DC bus (400 V or 800 V)", fs=6.8, c="white", fontweight="semibold")
    box(ax, 2, 38, 18, 12, "Traction\nbattery", fc="white", ec=TEAL, fs=6.8)
    items_up = [(24, "On-board\ncharger\n(AC→DC)"), (46, "DC charge\ninlet"), (68, "400→800 V\nboost\n(optional)")]
    for x, t in items_up:
        box(ax, x, 38, 18, 12, t, fs=6, fc=PALE if "boost" in t else LIGHT, ec=AMBER if "boost" in t else NAVY)
        arrow(ax, x + 9, 38, x + 9, 31, c=TEAL, lw=1.3, ms=6)
    arrow(ax, 11, 38, 11, 31, c=TEAL, lw=1.3, ms=6, both=True)
    label(ax, 33, 54, "AC mains", fs=6.3, c=GREY); arrow(ax, 33, 52.5, 33, 50, c=GREY, lw=1, ms=5)
    label(ax, 55, 54, "DC charger", fs=6.3, c=GREY); arrow(ax, 55, 52.5, 55, 50, c=GREY, lw=1, ms=5)
    items_dn = [(2, "Traction\ninverter\n+ motor"), (24, "HV→LV\nDC-DC"), (46, "Compressor\ninverter"), (68, "HV heater\n(PTC)")]
    for x, t in items_dn:
        box(ax, x, 9, 18, 12, t, fs=6)
        arrow(ax, x + 9, 27, x + 9, 21, c=TEAL, lw=1.3, ms=6, both=(x == 2))
    box(ax, 24, 0.5, 18, 6, "12 V / 48 V net", fs=5.6, fc=PALE, ec=AMBER)
    arrow(ax, 33, 9, 33, 6.5, c=AMBER, lw=1.2, ms=5)
    box(ax, 89, 38, 10, 12, "V2L /\nV2H", fs=5.8, fc="white", ec=GREY)
    save(fig, "fig12_1")


def bridge(ax, x, y, h=16, label_=""):
    ax.add_patch(Rectangle((x, y), 12, h, fc=LIGHT, ec=NAVY, lw=0.9))
    for k in range(2):
        xx = x + 3 + k * 6
        line(ax, [xx, xx], [y + 2, y + h - 2], c=NAVY, lw=0.8)
        for yy in (y + h * 0.72, y + h * 0.28):
            ax.add_patch(Rectangle((xx - 1.3, yy - 1.5), 2.6, 3, fc="white", ec=NAVY, lw=0.6))
    label(ax, x + 6, y - 2.2, label_, fs=6, c=NAVY)


def xfmr(ax, x, y):
    for k in range(4):
        ax.add_patch(Arc((x, y + 2 + k * 3), 3, 3, theta1=90, theta2=270, color=NAVY, lw=1))
        ax.add_patch(Arc((x + 4, y + 2 + k * 3), 3, 3, theta1=-90, theta2=90, color=NAVY, lw=1))
    line(ax, [x + 1.6, x + 1.6], [y, y + 14], c=NAVY, lw=0.8); line(ax, [x + 2.4, x + 2.4], [y, y + 14], c=NAVY, lw=0.8)


def ind(ax, x, y, w=8):
    for k in range(4):
        ax.add_patch(Arc((x + 1 + k * 2, y), 2, 2.4, theta1=0, theta2=180, color=NAVY, lw=1))


def fig12_2():
    fig, axs = plt.subplots(2, 1, figsize=(W, 3.0))
    for a in axs:
        a.set_xlim(0, 100); a.set_ylim(-4, 27); a.set_aspect("equal"); a.axis("off")
    a = axs[0]
    bridge(a, 4, 2, label_="half/full bridge")
    line(a, [16, 22], [14, 14], c=NAVY); ind(a, 22, 14); a.text(26, 17, "$L_r$", fontsize=7, color=NAVY, ha="center")
    line(a, [30, 34], [14, 14], c=NAVY); line(a, [34, 34], [12, 16], c=NAVY, lw=1.4); line(a, [35.5, 35.5], [12, 16], c=NAVY, lw=1.4)
    a.text(34.8, 18, "$C_r$", fontsize=7, color=NAVY, ha="center")
    line(a, [35.5, 44, 44], [14, 14, 12], c=NAVY); line(a, [16, 44, 44], [6, 6, 4], c=NAVY)
    xfmr(a, 44, 3); a.text(40, 9, "$L_m$", fontsize=7, color=NAVY)
    bridge(a, 56, 2, label_="rectifier"); line(a, [48.5, 56], [14, 14], c=NAVY); line(a, [48.5, 56], [6, 6], c=NAVY)
    line(a, [68, 76], [14, 14], c=NAVY); line(a, [68, 76], [6, 6], c=NAVY)
    box(a, 76, 4, 14, 12, "Battery", fs=6.3, fc="white", ec=TEAL)
    a.text(0, 24, "(a) LLC resonant", fontsize=7.5, color=NAVY, fontweight="bold")
    a = axs[1]
    bridge(a, 4, 2, label_="active bridge 1")
    line(a, [16, 24], [14, 14], c=NAVY); ind(a, 24, 14); a.text(28, 17, "$L$", fontsize=7, color=NAVY, ha="center")
    line(a, [32, 44, 44], [14, 14, 12], c=NAVY); line(a, [16, 44, 44], [6, 6, 4], c=NAVY)
    xfmr(a, 44, 3)
    bridge(a, 56, 2, label_="active bridge 2"); line(a, [48.5, 56], [14, 14], c=NAVY); line(a, [48.5, 56], [6, 6], c=NAVY)
    line(a, [68, 76], [14, 14], c=NAVY); line(a, [68, 76], [6, 6], c=NAVY)
    box(a, 76, 4, 14, 12, "Battery", fs=6.3, fc="white", ec=TEAL)
    arrow(a, 20, 20, 70, 20, c=AMBER, lw=1.2, both=True, ms=6); a.text(45, 21.5, "power flow set by phase shift φ", fontsize=6.3, color=AMBER, ha="center")
    a.text(0, 24, "(b) Dual active bridge", fontsize=7.5, color=NAVY, fontweight="bold")
    save(fig, "fig12_2")


def fig12_3():
    fn = np.linspace(0.3, 2.2, 500); Ln = 5
    fig, ax = plt.subplots(figsize=(W, 2.3))
    for Q, c in [(0.2, NAVY), (0.5, TEAL), (1.0, AMBER), (2.0, RED)]:
        num = Ln * fn ** 2
        den = np.sqrt(((Ln + 1) * fn ** 2 - 1) ** 2 + (fn ** 2 - 1) ** 2 * (fn * Q * Ln) ** 2)
        ax.plot(fn, num / den, color=c, lw=1.4, label=f"Q = {Q}")
    ax.axvline(1, color=GREY, lw=0.7, ls=":"); ax.text(1.02, 2.6, "resonance", fontsize=6.6, color=GREY)
    ax.set_xlabel("Normalised switching frequency $f_{sw}/f_r$"); ax.set_ylabel("Voltage gain")
    ax.set_ylim(0, 2.9); ax.set_xlim(0.3, 2.2); ax.legend(loc="upper right", fontsize=6.6)
    save(fig, "fig12_3")


def fig12_4():
    fig = plt.figure(figsize=(W, 2.6))
    ax = fig.add_axes([0, 0.38, 1, 0.62]); ax.set_xlim(0, 100); ax.set_ylim(0, 30); ax.set_aspect("equal"); ax.axis("off")
    box(ax, 1, 9, 13, 12, "AC mains\n230 V / 400 V", fs=5.8, fc="white", ec=GREY)
    box(ax, 20, 7, 18, 16, "EMI filter", fs=6.2)
    box(ax, 44, 7, 16, 16, "PFC stage\n(totem-pole)", fs=6.2, fc=PALE, ec=AMBER)
    ax.add_patch(Rectangle((63, 9), 4, 12, fc=NAVY)); ax.text(65, 24.5, "DC link", fontsize=5.8, color=NAVY, ha="center")
    box(ax, 70, 7, 17, 16, "Isolated\nDC-DC\n(LLC / DAB)", fs=6.2)
    box(ax, 90, 9, 9.5, 12, "Battery", fs=5.8, fc="white", ec=TEAL)
    for x1, x2 in [(14, 20), (38, 44), (60, 63), (67, 70), (87, 90)]:
        arrow(ax, x1, 15, x2, 15, c=TEAL, lw=1.3, ms=6)
    ax2 = fig.add_axes([0.1, 0.06, 0.85, 0.3])
    t = np.linspace(0, 0.04, 800)
    ax2.plot(t * 1000, np.sin(2 * np.pi * 50 * t), color=NAVY, lw=1, label="mains voltage")
    ax2.plot(t * 1000, 0.8 * np.sin(2 * np.pi * 50 * t) + 0.04 * np.sin(2 * np.pi * 2000 * t), color=TEAL, lw=1.2, label="PFC input current")
    pulses = np.where(np.abs(np.sin(2 * np.pi * 50 * t)) > 0.93, np.sign(np.sin(2 * np.pi * 50 * t)) * 1.0, 0) * 1.6
    ax2.plot(t * 1000, pulses, color=RED, lw=0.9, ls="--", label="plain rectifier current")
    ax2.set_xlabel("Time (ms)", fontsize=7); ax2.set_yticks([]); ax2.legend(loc="upper right", ncol=3, fontsize=6, bbox_to_anchor=(1, 1.35))
    ax2.set_ylim(-1.8, 1.8)
    save(fig, "fig12_4")


if __name__ == "__main__":
    fig12_1(); fig12_2(); fig12_3(); fig12_4()
