import sys; sys.path.insert(0, '.')
from goju import *
from PIL import Image, ImageDraw, ImageFont
# large figure drawing for the cover
plate("cover_fig", [P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7]))], cols=1, numbered=False, width_in=4.0)
W, H = 1800, 2700
im = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(im)
F_ = lambda n, s: ImageFont.truetype(f"../fonts/{n}.ttf", s)
def center(y, text, font):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill="black")
d.rectangle([60, 60, W - 60, H - 60], outline="black", width=6)
d.rectangle([84, 84, W - 84, H - 84], outline="black", width=2)
center(210, "G O J U - R Y U", F_("EBGaramond-Regular", 78))
center(320, "Karate Kyohan", F_("EBGaramond-Regular", 190))
center(560, "Volume Two", F_("EBGaramond-Italic", 96))
d.line([(W/2 - 220, 720), (W/2 + 220, 720)], fill="black", width=3)
sub = ["Illustrated Textbook With 800 Line Drawings", "for Kaishu Kata, Tension Drills,", "and Classical Applications", "Beyond the First Textbook"]
for i, s in enumerate(sub):
    center(780 + i * 72, s, F_("EBGaramond-Regular", 58))
fig = Image.open("../figures/cover_fig.png").convert("RGB")
fw = 1150
fig = fig.resize((fw, int(fig.height * fw / fig.width)))
im.paste(fig, ((W - fw) // 2, 1100))
center(2420, "DR BEVERLY J. STIVERS", F_("EBGaramond-Regular", 80))
im.save("../figures/cover.png")
print("cover ok")
