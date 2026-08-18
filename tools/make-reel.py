"""Render a 9:16 Instagram reel for Dental Zone.

Original motion graphic — not a copy of anyone's footage. Carries the
"I AM SUFFERING / list of problems" ad structure (an idea, not protected)
and resolves onto the real Dental Zone brand.

1080x1920, 30fps, ~9s, H.264 yuv420p so Instagram accepts it directly.
"""
import io, os, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/Users/aryanbasantani/Desktop/dentalzone"
SP   = "/private/tmp/claude-501/-Users-aryanbasantani/2c8baff4-8010-4d99-ba99-a1c065cb88c8/scratchpad"
FRM  = os.path.join(SP, "reel_frames")
FF   = os.path.join(SP, "venv3/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1")

W, H, FPS = 1080, 1920, 30
DUR = 9.0
N = int(DUR * FPS)

INK   = (7, 12, 24)
NAVY2 = (18, 41, 79)
WHITE = (255, 255, 255)
RED   = (217, 43, 43)
BLUE  = (22, 96, 255)
SKY   = (79, 179, 232)
MUTED = (150, 168, 194)

DIN    = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
HELV_B = "/System/Library/Fonts/Helvetica.ttc"

def f_din(sz):  return ImageFont.truetype(DIN, sz)
def f_helv(sz, idx=1):
    fo = ImageFont.truetype(HELV_B, sz, index=idx)
    return fo

PROBLEMS = ["MISSING TEETH", "DENTAL PAIN", "CROOKED TEETH",
            "CROWDED SMILE", "BIG CAVITY", "BLEEDING GUMS"]

# ---------- logo, framed as a rounded badge ----------
# Deliberately NOT colour-keyed: keying the sky-blue field ate the anti-aliased
# edges of the white tooth and left a cyan halo. The real logo is composited
# intact inside a rounded card with a soft shadow.
def load_badge(size, radius_frac=0.24):
    src = Image.open(os.path.join(ROOT, "icon-512.png")).convert("RGB").resize(
        (size, size), Image.LANCZOS)
    r = int(size * radius_frac)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size-1, size-1], r, fill=255)
    pad = int(size * 0.16)
    card = Image.new("RGBA", (size + pad*2, size + pad*2), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [pad, pad + int(size*0.05), pad + size, pad + size + int(size*0.05)],
        r, fill=(11, 18, 32, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(size * 0.055))
    card = Image.alpha_composite(card, sh)
    logo = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    logo.paste(src, (0, 0), mask)
    card.paste(logo, (pad, pad), logo)
    return card

MARK = load_badge(300)

def ease_out(t):   return 1 - (1 - t) ** 3
def ease_io(t):    return 3*t*t - 2*t*t*t

def vgrad(top, bot):
    g = Image.new("RGB", (1, H))
    d = ImageDraw.Draw(g)
    for y in range(H):
        k = y / H
        d.point((0, y), fill=(int(top[0]+(bot[0]-top[0])*k),
                              int(top[1]+(bot[1]-top[1])*k),
                              int(top[2]+(bot[2]-top[2])*k)))
    return g.resize((W, H))

BG_DARK = vgrad(INK, NAVY2)
BG_LITE = vgrad((246, 248, 252), (226, 236, 250))

def centred(d, text, font, y, fill, spacing=0):
    if spacing == 0:
        w = d.textlength(text, font=font)
        d.text(((W - w) / 2, y), text, font=font, fill=fill)
        return w
    total = sum(d.textlength(c, font=font) + spacing for c in text) - spacing
    x = (W - total) / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill)
        x += d.textlength(c, font=font) + spacing
    return total

def star(d, cx, cy, r, fill):
    pts = []
    for k in range(10):
        ang = -math.pi/2 + k * math.pi/5
        rad = r if k % 2 == 0 else r * 0.42
        pts.append((cx + math.cos(ang)*rad, cy + math.sin(ang)*rad))
    d.polygon(pts, fill=fill)

os.makedirs(FRM, exist_ok=True)
for old in os.listdir(FRM):
    os.remove(os.path.join(FRM, old))

for i in range(N):
    t = i / FPS

    # ============ ACT 1: the problem list (0 - 5.2s) ============
    if t < 5.2:
        img = BG_DARK.copy()
        d = ImageDraw.Draw(img, "RGBA")

        # slow drifting glow so the frame is never static
        gx = int(W*0.5 + math.sin(t*0.5)*90)
        gy = int(H*0.32 + math.cos(t*0.4)*60)
        glow = Image.new("RGBA", (W, H), (0,0,0,0))
        ImageDraw.Draw(glow).ellipse([gx-470, gy-470, gx+470, gy+470], fill=(40, 110, 220, 46))
        glow = glow.filter(ImageFilter.GaussianBlur(150))
        img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
        d = ImageDraw.Draw(img, "RGBA")

        # headline
        a = ease_out(min(1, max(0, (t - 0.15) / 0.7)))
        if a > 0:
            fh = f_din(150)
            y = 300 + (1 - a) * 40
            col = (255, 255, 255, int(255 * a))
            centred(d, "I AM", fh, y, col)
            centred(d, "SUFFERING", fh, y + 132, col)
            # rule under the headline, wiping outward
            rw = ease_out(min(1, max(0, (t - 0.75) / 0.6))) * 620
            if rw > 2:
                d.rounded_rectangle([(W-rw)/2, y+300, (W+rw)/2, y+308], 4,
                                    fill=(255, 255, 255, int(220 * a)))

        # problem lines, staggered
        fp = f_din(96)
        y0 = 760
        for k, line in enumerate(PROBLEMS):
            st = 1.25 + k * 0.34
            la = ease_out(min(1, max(0, (t - st) / 0.5)))
            if la <= 0:
                continue
            yy = y0 + k * 118 + (1 - la) * 26
            centred(d, line, fp, yy, (232, 240, 252, int(255 * la)))

        # fade to the brand card
        if t > 4.75:
            k = (t - 4.75) / 0.45
            d.rectangle([0, 0, W, H], fill=(7, 12, 24, int(255 * min(1, k))))

    # ============ ACT 2: the brand answer (5.2 - 9s) ============
    else:
        tt = t - 5.2
        img = BG_LITE.copy()
        d = ImageDraw.Draw(img, "RGBA")

        # open from black
        # (drawn last, below)

        # mark drops in
        ma = ease_out(min(1, tt / 0.6))
        ms = 0.82 + 0.18 * ma
        sz = int(300 * ms)
        m = MARK.resize((sz, sz), Image.LANCZOS)
        img.paste(m, (int((W - sz) / 2), int(330 - (1 - ma) * 40)), m)
        d = ImageDraw.Draw(img, "RGBA")

        # wordmark
        wa = ease_out(min(1, max(0, (tt - 0.28) / 0.55)))
        if wa > 0:
            fw = f_din(132)
            dental_w = d.textlength("DENTAL", font=fw)
            zone_w   = d.textlength("ZONE", font=fw)
            gap = 26
            total = dental_w + gap + zone_w
            x = (W - total) / 2
            yy = 690 + (1 - wa) * 22
            d.text((x, yy), "DENTAL", font=fw, fill=(RED[0], RED[1], RED[2], int(255*wa)))
            d.text((x + dental_w + gap, yy), "ZONE", font=fw,
                   fill=(BLUE[0], BLUE[1], BLUE[2], int(255*wa)))
            fs = f_din(40)
            centred(d, "SUPER SPECIALITY DENTAL HOSPITAL", fs, yy + 150,
                    (95, 107, 129, int(230*wa)), spacing=5)

        # the promise
        pa = ease_out(min(1, max(0, (tt - 0.75) / 0.6)))
        if pa > 0:
            fq = f_din(118)
            yy = 1010 + (1 - pa) * 20
            centred(d, "WE FIX ALL OF IT.", fq, yy, (11, 18, 32, int(255*pa)))

        # credentials strip
        ca = ease_out(min(1, max(0, (tt - 1.05) / 0.6)))
        if ca > 0:
            fc = f_din(58)
            yy = 1190
            centred(d, "DR. MUKESH BASANTANI, BDS", fc, yy, (60, 74, 95, int(255*ca)))
            fc2 = f_din(50)
            line = "23 YEARS  •  50,000+ PROCEDURES  •  4.6"
            tail = " ON GOOGLE"
            lw = d.textlength(line, font=fc2); tw2 = d.textlength(tail, font=fc2)
            sx = 34; x0 = (W - (lw + sx + tw2)) / 2
            d.text((x0, yy + 74), line, font=fc2, fill=(95,107,129,int(255*ca)))
            star(d, x0 + lw + sx/2, yy + 104, 17, (200,145,42,int(255*ca)))
            d.text((x0 + lw + sx, yy + 74), tail, font=fc2, fill=(95,107,129,int(255*ca)))

        # phone pill
        ba = ease_out(min(1, max(0, (tt - 1.4) / 0.6)))
        if ba > 0:
            fb = f_din(86)
            label = "CALL 094506 29270"
            tw = d.textlength(label, font=fb)
            pw, ph = tw + 130, 150
            px_, py_ = (W - pw) / 2, 1400 + (1 - ba) * 24
            pulse = 1 + 0.02 * math.sin(tt * 5)
            pw2, ph2 = pw * pulse, ph * pulse
            px2, py2 = (W - pw2) / 2, py_ - (ph2 - ph) / 2
            d.rounded_rectangle([px2, py2, px2 + pw2, py2 + ph2], ph2/2,
                                fill=(BLUE[0], BLUE[1], BLUE[2], int(255*ba)))
            d.text(((W - tw) / 2, py_ + 26), label, font=fb,
                   fill=(255, 255, 255, int(255*ba)))

        # address
        aa = ease_out(min(1, max(0, (tt - 1.7) / 0.6)))
        if aa > 0:
            fa = f_din(50)
            centred(d, "GRAND TRUNK ROAD, LUKARGANJ", fa, 1620, (95,107,129,int(255*aa)))
            centred(d, "PRAYAGRAJ (ALLAHABAD)", fa, 1678, (95,107,129,int(255*aa)))

        if tt < 0.32:
            k = 1 - tt / 0.32
            d.rectangle([0, 0, W, H], fill=(7, 12, 24, int(255 * k)))

    img.save(os.path.join(FRM, f"f{i:04d}.png"))

print(f"rendered {N} frames")

out = "/Users/aryanbasantani/Desktop/dental-zone-reel.mp4"
subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", os.path.join(FRM, "f%04d.png"),
                "-c:v", "libx264", "-preset", "slow", "-crf", "19",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
               check=True, capture_output=True)
print("wrote", out, os.path.getsize(out) // 1024, "KB")
