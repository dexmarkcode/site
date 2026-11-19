"""Premium textbook-style covers with rendered imagery (1600 x 2286 px)."""
import os
import random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
G = "/usr/share/texmf/fonts/opentype/public/tex-gyre/"
EBG = "/usr/share/fonts/truetype/ebgaramond/"
W, H = 1600, 2286


def font(name, size):
    paths = {"cn": G + "texgyreheroscn-bold.otf", "cnr": G + "texgyreheroscn-regular.otf", "hb": G + "texgyreheros-bold.otf",
             "hr": G + "texgyreheros-regular.otf", "pb": G + "texgyrepagella-bold.otf", "pr": G + "texgyrepagella-regular.otf",
             "pi": G + "texgyrepagella-italic.otf", "gi": EBG + "EBGaramond12-Italic.ttf", "gb": EBG + "EBGaramond12-Bold.ttf"}
    return ImageFont.truetype(paths[name], size)


def render(fn, w, h, bg="black"):
    """Render a matplotlib drawing function into a PIL image of w x h pixels."""
    dpi = 100
    fig = plt.figure(figsize=(w / dpi, h / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    fig.patch.set_facecolor(bg)
    fn(ax, w, h)
    fig.canvas.draw()
    img = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB")
    plt.close(fig)
    return img


def glow(img, radius=18, strength=1.2):
    b = img.filter(ImageFilter.GaussianBlur(radius))
    b = ImageEnhance.Brightness(b).enhance(strength)
    return ImageChops.screen(img, b)


def vgrad(w, h, stops):
    """Vertical gradient image from a list of (pos, (r,g,b)) stops, pos 0=top."""
    ys = np.linspace(0, 1, h)
    arr = np.zeros((h, w, 3))
    for c in range(3):
        arr[:, :, c] = np.interp(ys, [s[0] for s in stops], [s[1][c] for s in stops])[:, None]
    return Image.fromarray(arr.astype(np.uint8))


# ------------------------------------------------------------------ SCENE 1: power grid at dusk
def pylon(ax, x, yb, hgt, col, lw):
    w0, w1 = hgt * 0.22, hgt * 0.06
    top = yb + hgt
    L = [(x - w0, yb), (x - w1, top - hgt * 0.12)]
    R = [(x + w0, yb), (x + w1, top - hgt * 0.12)]
    ax.plot(*zip(*L), color=col, lw=lw * 1.5); ax.plot(*zip(*R), color=col, lw=lw * 1.5)
    ax.plot([x - w1, x, x + w1], [top - hgt * 0.12, top, top - hgt * 0.12], color=col, lw=lw * 1.3)
    # lattice
    n = 9
    for i in range(n):
        f0, f1 = i / n, (i + 1) / n
        def edge(f):
            yy = yb + f * (hgt * 0.88)
            ww = w0 + (w1 - w0) * f
            return yy, ww
        y0, ww0 = edge(f0); y1, ww1 = edge(f1)
        ax.plot([x - ww0, x + ww1], [y0, y1], color=col, lw=lw * 0.6)
        ax.plot([x + ww0, x - ww1], [y0, y1], color=col, lw=lw * 0.6)
        ax.plot([x - ww1, x + ww1], [y1, y1], color=col, lw=lw * 0.5)
    arms = []
    for k, (fy, span) in enumerate([(0.62, 0.55), (0.78, 0.45), (0.93, 0.32)]):
        yy = yb + hgt * fy
        sp = hgt * span
        ax.add_patch(Polygon([(x - sp, yy), (x + sp, yy), (x + w1 * 1.2, yy + hgt * 0.045), (x - w1 * 1.2, yy + hgt * 0.045)],
                             closed=True, fc="none", ec=col, lw=lw * 0.9))
        for s in (-1, 1):
            ax.plot([x + s * sp, x + s * sp], [yy, yy - hgt * 0.05], color=col, lw=lw * 0.8)
            arms.append((x + s * sp, yy - hgt * 0.05))
    return arms


def scene_grid(w, h):
    sky = vgrad(w, h, [(0, (8, 14, 38)), (0.35, (34, 34, 82)), (0.62, (122, 62, 92)), (0.78, (232, 120, 64)), (0.86, (250, 196, 112)), (1, (250, 210, 140))])
    arr = np.array(sky).astype(float)
    # sun glow
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w * 0.62, h * 0.84
    d = np.sqrt(((xx - cx) / (w * 0.55)) ** 2 + ((yy - cy) / (h * 0.25)) ** 2)
    g = np.clip(1 - d, 0, 1) ** 2.2
    arr += g[:, :, None] * np.array([90, 60, 20])
    # stars
    rnd = np.random.default_rng(3)
    for _ in range(260):
        sx, sy = rnd.integers(0, w), rnd.integers(0, int(h * 0.42))
        b = rnd.uniform(90, 255) * (1 - sy / (h * 0.45))
        arr[sy, sx] = np.maximum(arr[sy, sx], b)
    sky = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    def draw(ax, W_, H_):
        pass

    # silhouettes via matplotlib with transparent background
    dpi = 100
    fig = plt.figure(figsize=(w / dpi, h / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    fig.patch.set_alpha(0)
    hor = h * 0.2
    # distant hills
    xs = np.linspace(0, w, 400)
    hills = hor + 18 * np.sin(xs / 140) + 10 * np.sin(xs / 53 + 1)
    ax.fill_between(xs, 0, hills, color="#140F22", zorder=2)
    near = hor - 70 + 22 * np.sin(xs / 260 + 2) + 10 * np.sin(xs / 90)
    ax.fill_between(xs, 0, near, color="#07060C", zorder=4)
    # towers receding to the right
    col = "#06050B"
    towers = []
    for i, (x, hh) in enumerate([(230, 640), (760, 400), (1060, 250), (1235, 160), (1345, 104), (1415, 68)]):
        yb = hor - 60 if i == 0 else hor - 8 - 30 / (i + 1)
        towers.append(pylon(ax, x, yb, hh, col, max(1.0, 3.2 - i * 0.45)))
    # catenary wires
    for k in range(6):
        for a, b in zip(towers[:-1], towers[1:]):
            (x0, y0), (x1, y1) = a[k], b[k]
            t = np.linspace(0, 1, 60)
            sag = 0.12 * (x1 - x0) * 0.35
            ax.plot(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t - sag * 4 * t * (1 - t), color=col, lw=1.1, zorder=3)
        # wires leaving left edge from first tower
        (x1, y1) = towers[0][k]
        t = np.linspace(0, 1, 40)
        ax.plot(-40 + (x1 + 40) * t, (y1 - 60) + (60) * t - 25 * 4 * t * (1 - t), color=col, lw=1.4, zorder=3)
    # city lights
    rnd2 = random.Random(5)
    for _ in range(140):
        lx = rnd2.uniform(w * 0.35, w)
        ly = hor + rnd2.uniform(-12, 12) - 6
        ax.add_patch(Circle((lx, ly), rnd2.uniform(1.2, 3.0), color=rnd2.choice(["#FFD27A", "#FFE9B0", "#FFB45A"]), zorder=2.5, alpha=0.9))
    fig.canvas.draw()
    sil = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba())
    plt.close(fig)
    lights = sil.split()[3]
    base = sky.copy()
    base.paste(sil, (0, 0), sil)
    # bloom only on bright parts
    bright = base.point(lambda v: 255 if v > 200 else 0).filter(ImageFilter.GaussianBlur(10))
    base = ImageChops.screen(base, ImageEnhance.Brightness(bright).enhance(0.6))
    return base


# ------------------------------------------------------------------ SCENE 2: circuit board macro
def scene_pcb(w, h):
    rnd = random.Random(11)

    def draw(ax, W_, H_):
        # board
        g = np.linspace(0, 1, 256).reshape(-1, 1)
        ax.imshow(g, extent=[0, W_, 0, H_], origin="lower", aspect="auto",
                  cmap=matplotlib.colors.LinearSegmentedColormap.from_list("b", ["#04140F", "#0B3B2E", "#0E4A39"]), zorder=0)
        gold = "#C9A24A"
        # traces: orthogonal + 45 degree routes
        step = 40
        for _ in range(115):
            x, y = rnd.randrange(0, W_, step), rnd.randrange(0, H_, step)
            pts = [(x, y)]
            for _ in range(rnd.randint(3, 7)):
                d = rnd.choice([(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1)])
                L = rnd.randrange(step, step * 6, step)
                x, y = x + d[0] * L, y + d[1] * L
                pts.append((x, y))
            xs, ys = zip(*pts)
            lw = rnd.choice([1.6, 2.2, 3.0, 4.2])
            ax.plot(xs, ys, color="#7A6128", lw=lw + 1.6, zorder=1, solid_capstyle="round", solid_joinstyle="round")
            ax.plot(xs, ys, color=gold, lw=lw, zorder=2, solid_capstyle="round", solid_joinstyle="round")
            ax.plot(xs, ys, color="#F3DE9C", lw=lw * 0.25, zorder=2.1, alpha=0.7)
            for p in (pts[0], pts[-1]):
                ax.add_patch(Circle(p, lw * 2.2 + 3, fc=gold, ec="#7A6128", lw=1, zorder=3))
                ax.add_patch(Circle(p, lw * 0.9 + 1.5, fc="#061A13", ec="none", zorder=3.1))
        # chips
        for (cx, cy, cw, ch, lab) in [(W_ * 0.5, H_ * 0.52, 360, 360, "FE-2026"), (W_ * 0.17, H_ * 0.78, 200, 120, "U3"),
                                      (W_ * 0.82, H_ * 0.25, 240, 150, "U7"), (W_ * 0.8, H_ * 0.8, 150, 150, "U5"), (W_ * 0.2, H_ * 0.2, 180, 110, "U2")]:
            pins = int(cw / 26)
            for i in range(pins):
                px = cx - cw / 2 + (i + 0.5) * cw / pins
                for s in (-1, 1):
                    ax.add_patch(Rectangle((px - 5, cy + s * ch / 2 - (0 if s > 0 else 26)), 10, 26, fc="#D7D9DE", ec="#8A8E96", lw=0.8, zorder=4))
            if cw == ch:
                for i in range(pins):
                    py = cy - ch / 2 + (i + 0.5) * ch / pins
                    for s in (-1, 1):
                        ax.add_patch(Rectangle((cx + s * cw / 2 - (0 if s > 0 else 26), py - 5), 26, 10, fc="#D7D9DE", ec="#8A8E96", lw=0.8, zorder=4))
            ax.add_patch(FancyBboxPatch((cx - cw / 2, cy - ch / 2), cw, ch, boxstyle="round,pad=0,rounding_size=8", fc="#141619", ec="#3C4048", lw=2, zorder=5))
            ax.add_patch(FancyBboxPatch((cx - cw / 2 + 6, cy + ch / 2 - 30), cw - 12, 22, boxstyle="round,pad=0,rounding_size=6", fc="#2A2D33", ec="none", alpha=0.6, zorder=5.1))
            ax.add_patch(Circle((cx - cw / 2 + 22, cy - ch / 2 + 22), 7, fc="#2A2D33", ec="none", zorder=5.2))
            ax.text(cx, cy, lab, color="#9AA0A8", fontsize=14 if cw > 300 else 9, ha="center", va="center", zorder=6, family="DejaVu Sans Mono")
        # SMD parts
        for _ in range(60):
            x, y = rnd.uniform(0, W_), rnd.uniform(0, H_)
            vert = rnd.random() < 0.5
            ww, hh = (22, 44) if vert else (44, 22)
            col = rnd.choice(["#1E1E1E", "#3B2A1A", "#B88A3A"])
            ax.add_patch(Rectangle((x, y), ww, hh, fc=col, ec="#555", lw=0.6, zorder=4.5))
            if vert:
                ax.add_patch(Rectangle((x, y), ww, 9, fc="#D7D9DE", zorder=4.6)); ax.add_patch(Rectangle((x, y + hh - 9), ww, 9, fc="#D7D9DE", zorder=4.6))
            else:
                ax.add_patch(Rectangle((x, y), 9, hh, fc="#D7D9DE", zorder=4.6)); ax.add_patch(Rectangle((x + ww - 9, y), 9, hh, fc="#D7D9DE", zorder=4.6))
        # glowing current paths (cyan)
        for _ in range(9):
            x, y = rnd.randrange(0, W_, step), rnd.randrange(0, H_, step)
            pts = [(x, y)]
            for _ in range(rnd.randint(4, 8)):
                d = rnd.choice([(1, 0), (0, 1), (1, 1), (-1, 1)])
                L = rnd.randrange(step * 2, step * 7, step)
                x, y = x + d[0] * L, y + d[1] * L
                pts.append((x, y))
            xs, ys = zip(*pts)
            ax.plot(xs, ys, color="#7FF6FF", lw=2.6, zorder=7, solid_capstyle="round")
            ax.add_patch(Circle(pts[-1], 7, fc="#E0FDFF", zorder=7.1))

    img = render(draw, w, h)
    # glow the cyan paths
    arr = np.array(img).astype(int)
    mask = ((arr[:, :, 2] > 220) & (arr[:, :, 0] < 200)).astype(np.uint8) * 255
    m = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(14))
    cy = Image.new("RGB", img.size, (60, 220, 255))
    glowl = Image.composite(cy, Image.new("RGB", img.size, 0), m)
    img = ImageChops.screen(img, glowl)
    img = ImageChops.screen(img, ImageEnhance.Brightness(glowl.filter(ImageFilter.GaussianBlur(30))).enhance(0.8))
    # lighting sweep + vignette
    yy, xx = np.mgrid[0:h, 0:w]
    light = np.clip(1 - np.abs((xx / w + yy / h) - 0.9) / 0.6, 0, 1) ** 2 * 45
    vig = np.clip(((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2) * 2.2, 0, 1) * 120
    a = np.array(img).astype(float) + light[:, :, None] * np.array([1.0, 0.9, 0.7]) - vig[:, :, None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    # tilt-shift depth of field
    blur = img.filter(ImageFilter.GaussianBlur(9))
    dof = np.clip(np.abs(yy / h - 0.5) * 3.2 - 0.45, 0, 1)
    dm = Image.fromarray((dof * 255).astype(np.uint8))
    return Image.composite(blur, img, dm)


# ------------------------------------------------------------------ SCENE 3: oscilloscope
def scene_scope(w, h):
    def draw(ax, W_, H_):
        ax.add_patch(Rectangle((0, 0), W_, H_, fc="#05080D"))
        nx, ny = 10, 8
        for i in range(nx + 1):
            x = W_ * i / nx
            ax.plot([x, x], [0, H_], color="#1F3D4A", lw=1.2 if i != nx // 2 else 1.8)
        for j in range(ny + 1):
            y = H_ * j / ny
            ax.plot([0, W_], [y, y], color="#1F3D4A", lw=1.2 if j != ny // 2 else 1.8)
        t = np.linspace(0, W_, 1200)
        for amp, ph, col in [(0.32, 0.0, "#FFE36A"), (0.24, 2.094, "#5CF2FF"), (0.24, 4.189, "#FF6AD5")]:
            ax.plot(t, H_ / 2 + amp * H_ * np.sin(2 * np.pi * t / (W_ / 2.2) + ph), color=col, lw=3.2)
    img = render(draw, w, h)
    return glow(img, 10, 1.4)


# ------------------------------------------------------------------ SCENE 4: electric arc
def bolt(p0, p1, disp, depth, rnd):
    if depth == 0:
        return [p0, p1]
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = np.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    off = rnd.uniform(-disp, disp)
    m = (mx + nx * off, my + ny * off)
    return bolt(p0, m, disp / 2, depth - 1, rnd)[:-1] + bolt(m, p1, disp / 2, depth - 1, rnd)


def scene_arc(w, h):
    rnd = random.Random(21)

    def draw(ax, W_, H_):
        yy = np.linspace(0, 1, 256).reshape(-1, 1)
        ax.imshow(yy, extent=[0, W_, 0, H_], origin="lower", aspect="auto",
                  cmap=matplotlib.colors.LinearSegmentedColormap.from_list("a", ["#05030F", "#120A2E", "#05030F"]))
        # electrodes
        for x0, s in [(W_ * 0.08, 1), (W_ * 0.92, -1)]:
            ax.add_patch(Polygon([(x0 - s * 120, H_ * 0.5 - 70), (x0, H_ * 0.5 - 18), (x0, H_ * 0.5 + 18), (x0 - s * 120, H_ * 0.5 + 70)],
                                 fc="#8C929C", ec="#C9CED6", lw=2))
            ax.add_patch(Rectangle((x0 - s * 120 - (60 if s > 0 else 0), H_ * 0.5 - 70), 60, 140, fc="#5A606A", ec="#9AA0AA", lw=2))
        a, b = (W_ * 0.08, H_ * 0.5), (W_ * 0.92, H_ * 0.5)
        for k in range(5):
            pts = bolt(a, b, H_ * 0.32 * (0.6 + 0.4 * rnd.random()), 9, rnd)
            xs, ys = zip(*pts)
            ax.plot(xs, ys, color="#D9C8FF", lw=3.4 if k == 0 else 1.4, alpha=1.0 if k == 0 else 0.7)
            # branches
            for _ in range(3):
                i = rnd.randrange(10, len(pts) - 10)
                p = pts[i]
                q = (p[0] + rnd.uniform(-160, 160), p[1] + rnd.uniform(-200, 200))
                bp = bolt(p, q, 60, 6, rnd)
                ax.plot(*zip(*bp), color="#B9A2FF", lw=1.0, alpha=0.7)
    img = render(draw, w, h)
    g1 = img.filter(ImageFilter.GaussianBlur(8)); g2 = img.filter(ImageFilter.GaussianBlur(28))
    tint = Image.new("RGB", img.size, (120, 80, 255))
    g2 = ImageChops.multiply(ImageEnhance.Brightness(g2).enhance(2.2), tint)
    return ImageChops.screen(ImageChops.screen(img, ImageEnhance.Brightness(g1).enhance(1.6)), g2)


# ------------------------------------------------------------------ typography helpers
def draw_text(img, xy, s, f, fill, anchor="mm", spacing=0, shadow=None):
    d = ImageDraw.Draw(img)
    if spacing:
        total = sum(d.textlength(c, font=f) for c in s) + spacing * (len(s) - 1)
        x, y = xy
        if anchor[0] == "m":
            x -= total / 2
        elif anchor[0] == "r":
            x -= total
        for c in s:
            if shadow:
                sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
                ImageDraw.Draw(sh).text((x, y), c, font=f, fill=shadow, anchor="l" + anchor[1])
            d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
            x += d.textlength(c, font=f) + spacing
        return
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + 4, xy[1] + 6), s, font=f, fill=shadow, anchor=anchor)
        sh = sh.filter(ImageFilter.GaussianBlur(8))
        img.paste(sh, (0, 0), sh)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def fit_font(name, s, width, start=300):
    size = start
    while size > 10:
        f = font(name, size)
        if f.getlength(s) <= width:
            return f
        size -= 2
    return font(name, size)


def badge_row(img, y, items, col_big, col_small, f_big, f_small, x0=200, x1=W - 200):
    d = ImageDraw.Draw(img)
    n = len(items)
    for i, (big, small) in enumerate(items):
        cx = x0 + (x1 - x0) * (i + 0.5) / n
        d.text((cx, y), big, font=f_big, fill=col_big, anchor="mm")
        d.text((cx, y + 62), small, font=f_small, fill=col_small, anchor="mm")
        if i:
            xx = x0 + (x1 - x0) * i / n
            d.line([(xx, y - 40), (xx, y + 80)], fill=col_small, width=2)


def save(img, name):
    img.save(os.path.join(OUT, name), dpi=(228.6, 228.6))


# ================================================================== COVER P1: GRID AT DUSK
def cover_p1(grid):
    img = Image.new("RGB", (W, H), (8, 14, 38))
    img.paste(grid.resize((W, 1560)), (0, 250))
    # darken top for type legibility
    ov = vgrad(W, 1560, [(0, (0, 0, 0)), (0.5, (0, 0, 0)), (1, (0, 0, 0))])
    mask = vgrad(W, 1560, [(0, (150, 150, 150)), (0.42, (40, 40, 40)), (0.6, (0, 0, 0)), (1, (0, 0, 0))]).convert("L")
    img.paste(ov, (0, 0), mask)
    # bottom navy panel with copper rule
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1560, W, H], fill=(11, 22, 48))
    d.rectangle([0, 1556, W, 1566], fill=(201, 129, 58))
    draw_text(img, (W / 2, 120), "THE COMPLETE STUDY GUIDE  ·  2026–2027 EDITION", font("hb", 34), (240, 210, 160), spacing=3)
    d.line([(560, 168), (1040, 168)], fill=(240, 210, 160), width=2)
    f1 = fit_font("cn", "ELECTRICAL", W - 220)
    draw_text(img, (W / 2, 330), "ELECTRICAL", f1, (255, 255, 255), shadow=(0, 0, 0, 200))
    draw_text(img, (W / 2, 560), "ENGINEERING", fit_font("cn", "ENGINEERING", W - 220), (255, 255, 255), shadow=(0, 0, 0, 200))
    draw_text(img, (W / 2, 790), "FE EXAM PREP", fit_font("cn", "FE EXAM PREP", W - 220), (247, 186, 92), shadow=(0, 0, 0, 220))
    draw_text(img, (W / 2, 1650), "800 Practice Questions, Formulas, and Mock Exams", font("gi", 64), (240, 236, 226))
    draw_text(img, (W / 2, 1725), "to Pass First Time", font("gi", 64), (240, 236, 226))
    badge_row(img, 1850, [("800", "PRACTICE QUESTIONS"), ("2", "FULL MOCK EXAMS"), ("100%", "WORKED SOLUTIONS")],
              (247, 186, 92), (200, 210, 228), font("cn", 92), font("hb", 26), 160, W - 160)
    d.line([(560, 2045), (1040, 2045)], fill=(201, 129, 58), width=3)
    draw_text(img, (W / 2, 2150), "MARCUS J. THORNTON, PH.D.", fit_font("cn", "MARCUS J. THORNTON, PH.D.", 1180, 110), (255, 255, 255))
    return img


# ================================================================== COVER P2: CIRCUIT TEXTBOOK
def cover_p2(pcb):
    img = Image.new("RGB", (W, H), (250, 248, 243))
    d = ImageDraw.Draw(img)
    # top colour band
    band = vgrad(W, 880, [(0, (12, 28, 64)), (1, (20, 52, 112))])
    img.paste(band, (0, 0))
    d.rectangle([0, 880, W, 892], fill=(201, 129, 58))
    draw_text(img, (W / 2, 105), "2026–2027 EDITION", font("hb", 36), (247, 186, 92), spacing=8)
    draw_text(img, (W / 2, 300), "ELECTRICAL ENGINEERING", fit_font("cn", "ELECTRICAL ENGINEERING", W - 200), (255, 255, 255))
    draw_text(img, (W / 2, 560), "FE EXAM PREP", fit_font("cn", "FE EXAM PREP", W - 200), (247, 186, 92))
    draw_text(img, (W / 2, 770), "The Complete Study Guide", font("gi", 78), (235, 238, 245))
    # image panel
    img.paste(pcb.resize((W, 900)), (0, 892))
    d.rectangle([0, 1792, W, 1804], fill=(201, 129, 58))
    # bottom
    draw_text(img, (W / 2, 1890), "800 PRACTICE QUESTIONS  ·  2 FULL MOCK EXAMS  ·  EVERY FORMULA", font("hb", 34), (12, 28, 64), spacing=2)
    draw_text(img, (W / 2, 1960), "to Pass First Time", font("gi", 56), (90, 90, 90))
    d.line([(560, 2040), (1040, 2040)], fill=(201, 129, 58), width=3)
    draw_text(img, (W / 2, 2150), "MARCUS J. THORNTON, PH.D.", fit_font("cn", "MARCUS J. THORNTON, PH.D.", 1180, 110), (12, 28, 64))
    return img


# ================================================================== COVER P3: COLLAGE
def cover_p3(grid, pcb, scope, arc):
    img = Image.new("RGB", (W, H), (246, 242, 234))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 28], fill=(12, 28, 64))
    draw_text(img, (W / 2, 120), "THE COMPLETE STUDY GUIDE  ·  2026–2027 EDITION", font("hb", 32), (160, 60, 40), spacing=3)
    draw_text(img, (W / 2, 300), "ELECTRICAL ENGINEERING", fit_font("cn", "ELECTRICAL ENGINEERING", W - 180), (12, 28, 64))
    draw_text(img, (W / 2, 520), "FE EXAM PREP", fit_font("cn", "FE EXAM PREP", W - 180), (178, 38, 30))
    # 2x2 image grid
    gx, gy, gw, gh, gut = 70, 660, (W - 140 - 20) // 2, 470, 20
    tiles = [grid.crop((0, 300, grid.width, grid.height - 120)), pcb, scope, arc]
    for i, t in enumerate(tiles):
        r, c = divmod(i, 2)
        tw, th = gw, gh
        src = t
        ar = tw / th
        if src.width / src.height > ar:
            nw = int(src.height * ar); x0 = (src.width - nw) // 2; src = src.crop((x0, 0, x0 + nw, src.height))
        else:
            nh = int(src.width / ar); y0 = (src.height - nh) // 2; src = src.crop((0, y0, src.width, y0 + nh))
        img.paste(src.resize((tw, th), Image.LANCZOS), (gx + c * (gw + gut), gy + r * (gh + gut)))
    y = gy + 2 * gh + gut + 70
    draw_text(img, (W / 2, y + 10), "800 Practice Questions, Formulas, and Mock Exams to Pass First Time", font("gi", 50), (40, 40, 40))
    badge_row(img, y + 130, [("800", "PRACTICE QUESTIONS"), ("2", "FULL MOCK EXAMS"), ("100%", "WORKED SOLUTIONS")],
              (178, 38, 30), (60, 60, 60), font("cn", 80), font("hb", 24), 220, W - 220)
    d.line([(560, y + 240), (1040, y + 240)], fill=(178, 38, 30), width=3)
    draw_text(img, (W / 2, 2160), "MARCUS J. THORNTON, PH.D.", fit_font("cn", "MARCUS J. THORNTON, PH.D.", 1180, 110), (12, 28, 64))
    d.rectangle([0, H - 28, W, H], fill=(12, 28, 64))
    return img


if __name__ == "__main__":
    grid = scene_grid(1600, 1560)
    pcb = scene_pcb(1600, 900)
    scope = scene_scope(1000, 700)
    arc = scene_arc(1100, 700)
    for nm, im in [("scene_grid.png", grid), ("scene_pcb.png", pcb), ("scene_scope.png", scope), ("scene_arc.png", arc)]:
        im.save(os.path.join(OUT, nm))
    p1, p2, p3 = cover_p1(grid), cover_p2(pcb), cover_p3(grid, pcb, scope, arc)
    save(p1, "cover_P1_power_grid.png"); save(p2, "cover_P2_circuit.png"); save(p3, "cover_P3_collage.png")
    ims = [im.resize((560, 800), Image.LANCZOS) for im in (p1, p2, p3)]
    sheet = Image.new("RGB", (560 * 3 + 80, 880), (232, 232, 232))
    f = font("hb", 24)
    dd = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(ims, ["P1  Power Grid at Dusk", "P2  Circuit Board", "P3  Engineering Collage"])):
        sheet.paste(im, (20 + i * 580, 20))
        dd.text((20 + i * 580 + 280, 848), lab, fill=(30, 30, 30), font=f, anchor="mm")
    sheet.save(os.path.join(OUT, "cover_premium_comparison.png"))
    print("done")
