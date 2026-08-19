# -*- coding: utf-8 -*-
"""Instagram carousel for Dental Zone — 3 slides, 1080x1350 (4:5).

The fact is chosen because it has a real clinical punchline rather than being
throwaway trivia: enamel genuinely is the hardest tissue in the body, and it
genuinely cannot regenerate, because it contains no living cells. That second
half is what makes a checkup matter, so the carousel earns its call to action
instead of bolting one on.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/Users/aryanbasantani/Desktop/dentalzone"
SP   = "/private/tmp/claude-501/-Users-aryanbasantani/2c8baff4-8010-4d99-ba99-a1c065cb88c8/scratchpad"
OUT  = os.path.expanduser("~/Desktop/dentalzone-carousel")
W, H = 1080, 1350

INK   = (7, 12, 24)
NAVY2 = (18, 41, 79)
RED   = (217, 43, 43)
BLUE  = (22, 96, 255)
SKY   = (124, 196, 255)

DIN = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
RYE = os.path.join(SP, "fonts/Rye-Regular.ttf")

def f(sz):  return ImageFont.truetype(DIN, sz)
def fr(sz): return ImageFont.truetype(RYE, sz)

def vgrad(c0, c1, w=W, h=H):
    g = Image.new("RGB", (1, h)); d = ImageDraw.Draw(g)
    for y in range(h):
        k = (y / h) ** 0.92
        d.point((0, y), fill=tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3)))
    return g.resize((w, h))

def tooth(d, cx, cy, s, col, wdt=9):
    d.line([(cx-40*s, cy-46*s), (cx-46*s, cy+10*s)], fill=col, width=int(wdt*s), joint="curve")
    pts = [(cx-46*s,cy-30*s),(cx-30*s,cy-52*s),(cx,cy-42*s),(cx+30*s,cy-52*s),(cx+46*s,cy-30*s),
           (cx+44*s,cy+14*s),(cx+28*s,cy+58*s),(cx+16*s,cy+18*s),(cx,cy+8*s),
           (cx-16*s,cy+18*s),(cx-28*s,cy+58*s),(cx-44*s,cy+14*s)]
    d.line(pts + [pts[0]], fill=col, width=int(wdt*s), joint="curve")

def arrow(d, x, y, size, col, wdt=5):
    """DIN Condensed has no arrow glyph — U+2192 came out as a tofu box."""
    d.line([(x, y), (x + size, y)], fill=col, width=wdt)
    d.line([(x + size - size*0.34, y - size*0.26), (x + size, y)], fill=col, width=wdt)
    d.line([(x + size - size*0.34, y + size*0.26), (x + size, y)], fill=col, width=wdt)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def draw_block(d, text, font, x, y, maxw, fill, lh=1.02):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += int(font.size * lh)
    return y

def glow(img, cx, cy, r, col, a=52, blur=140):
    g = Image.new("RGBA", (W, H), (0,0,0,0))
    ImageDraw.Draw(g).ellipse([cx-r, cy-r, cx+r, cy+r], fill=col + (a,))
    return Image.alpha_composite(img, g.filter(ImageFilter.GaussianBlur(blur)))

def brand_strip(d, dark=True, accent=None):
    """Small consistent footer on every slide so any single one is attributable.
       accent follows the slide palette — sky blue on the red slide clashed."""
    col = (255,255,255,150) if dark else (95,107,129,230)
    if accent is None:
        accent = (SKY + (255,)) if dark else (BLUE + (255,))
    d.text((78, H-108), "DENTAL ZONE  ·  LUKARGANJ, PRAYAGRAJ", font=f(34), fill=col)
    d.text((78, H-66),  "094506 29270", font=f(34), fill=accent)

def dots(d, active, dark=True):
    base = (255,255,255,70) if dark else (11,18,32,60)
    on   = (255,255,255,235) if dark else (11,18,32,220)
    x0 = W - 78 - (3*20 + 2*12)
    for i in range(3):
        x = x0 + i*(20+12)
        d.ellipse([x, H-84, x+20, H-64], fill=on if i == active else base)

os.makedirs(OUT, exist_ok=True)

# ─────────────────────────── SLIDE 1 — the hook
img = vgrad(INK, NAVY2).convert("RGBA")
img = glow(img, int(W*0.86), int(H*0.24), 470, (40,110,220), 60)
d = ImageDraw.Draw(img, "RGBA")
tooth(d, int(W*0.78), int(H*0.735), 2.35, SKY + (34,), 11)

d.text((78, 300), "DID YOU KNOW", font=f(44), fill=SKY + (255,))
d.line([(78, 356), (78+240, 356)], fill=SKY + (200,), width=4)
y = draw_block(d, "ENAMEL IS THE HARDEST SUBSTANCE IN YOUR BODY.",
               f(122), 78, 430, W-156, (255,255,255,255), 0.96)
d.text((78, y+34), "Harder than bone. Harder than steel,", font=f(46), fill=(190,208,232,255))
d.text((78, y+90), "by hardness.", font=f(46), fill=(190,208,232,255))
d.text((78, H-190), "SWIPE", font=f(40), fill=SKY + (235,))
arrow(d, 190, H-172, 46, SKY + (235,))
brand_strip(d); dots(d, 0)
img.convert("RGB").save(f"{OUT}/dentalzone-carousel-1.jpg", "JPEG", quality=92, optimize=True)

# ─────────────────────────── SLIDE 2 — the twist
img = vgrad((28,10,14), (96,26,32)).convert("RGBA")
img = glow(img, int(W*0.20), int(H*0.80), 430, (255,90,90), 44)
d = ImageDraw.Draw(img, "RGBA")
tooth(d, int(W*0.80), int(H*0.125), 1.75, (255,170,170,40), 11)

d.text((78, 250), "BUT HERE IS THE CATCH", font=f(44), fill=(255,170,160,255))
d.line([(78, 306), (78+300, 306)], fill=(255,170,160,190), width=4)
y = draw_block(d, "IT IS THE ONLY PART THAT NEVER GROWS BACK.",
               f(126), 78, 370, W-156, (255,255,255,255), 0.94)
y += 40
for ln in ["Bone heals. Skin heals. Enamel does not —",
           "it has no living cells to repair itself.",
           "",
           "So a cavity is permanent damage. We can",
           "repair it. Nobody can regrow it."]:
    if ln:
        d.text((78, y), ln, font=f(48), fill=(240,214,214,255))
    y += 62
d.text((78, H-190), "SWIPE", font=f(40), fill=(255,170,160,235))
arrow(d, 190, H-172, 46, (255,170,160,235))
brand_strip(d, accent=(255,170,160,255)); dots(d, 1)
img.convert("RGB").save(f"{OUT}/dentalzone-carousel-2.jpg", "JPEG", quality=92, optimize=True)

# ─────────────────────────── SLIDE 3 — the ask
img = vgrad((246,248,252), (222,233,248)).convert("RGBA")
d = ImageDraw.Draw(img, "RGBA")

y = draw_block(d, "WHICH IS WHY THE CHECKUP BEATS THE CURE.",
               f(112), 78, 240, W-156, (11,18,32,255), 0.94)
y += 34
for ln in ["Six months is the interval that keeps a filling",
           "from becoming a root canal.",
           "",
           "23 years. 50,000+ procedures. 4.6 on Google."]:
    if ln:
        d.text((78, y), ln, font=f(46), fill=(95,107,129,255))
    y += 60

# logo badge + wordmark
badge = Image.open(os.path.join(ROOT, "icon-512.png")).convert("RGB").resize((190,190), Image.LANCZOS)
mask = Image.new("L", (190,190), 0)
ImageDraw.Draw(mask).rounded_rectangle([0,0,189,189], 46, fill=255)
img.paste(badge, (78, H-430), mask)

wm = Image.open(os.path.join(ROOT, "images/wordmark.png")).convert("RGBA")
wm.thumbnail((520, 200), Image.LANCZOS)
img.paste(wm, (300, H-430 + (190-wm.height)//2 - 14), wm)
d = ImageDraw.Draw(img, "RGBA")
# sits clear beneath the wordmark art rather than on its baseline
d.text((302, H-292), "SUPER SPECIALITY DENTAL HOSPITAL",
       font=f(30), fill=(95,107,129,255))

d.rounded_rectangle([78, H-196, 78+560, H-196+96], 48, fill=BLUE + (255,))
d.text((118, H-172), "BOOK  ·  094506 29270", font=f(56), fill=(255,255,255,255))
d.text((78, H-72), "GRAND TRUNK ROAD, LUKARGANJ, PRAYAGRAJ", font=f(32), fill=(95,107,129,255))
dots(d, 2, dark=False)
img.convert("RGB").save(f"{OUT}/dentalzone-carousel-3.jpg", "JPEG", quality=92, optimize=True)

for i in (1,2,3):
    p = f"{OUT}/dentalzone-carousel-{i}.jpg"
    print(f"  slide {i}: {Image.open(p).size}  {os.path.getsize(p)//1024} KB")
print("\nwritten to", OUT)
