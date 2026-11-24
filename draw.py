#!/usr/bin/env python3
"""Paint the news-image-20261124 collage: "THE WORLD TODAY — TUESDAY 24 NOVEMBER 2026".

A from-scratch Pillow program that draws the whole front page with vector
shapes and DejaVu type: a navy masthead, six illustrated news panels in two
columns, and a sports strip along the bottom. No network, no randomness, no
photographs — every pixel is computed here, so the result is reproducible
(the same command always yields the same bytes):
running `python3 draw.py` regenerates entry.png byte-for-byte (1024x1024,
inside the 1 MiB limit). `main.ts` then hands the bundled picture to the
grader's output directory.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
# page furniture and accent colours, one unpacked row
PAPER, INK, NAVY, ORANGE, TEAL, RED, CREAM, GOLD = (
    (244, 239, 227), (18, 24, 32), (18, 58, 92), (240, 120, 48),
    (31, 122, 109), (185, 28, 28), (250, 246, 236), (212, 160, 32),
)

SERIF_B, SANS_B, SANS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap: pack words into lines no wider than max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred_text(draw, cx, y, text, fnt, fill, tracking=0):
    """Draw text centred on cx; with tracking, space the letters by hand."""
    if tracking:
        widths = [draw.textlength(ch, font=fnt) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = cx - total / 2
        for ch, wch in zip(text, widths):
            draw.text((x, y), ch, font=fnt, fill=fill)
            x += wch + tracking
        return total
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def draw_panel(draw, img, x, y, w, h, scene, tag, tag_color, headline, sub):
    """One panel: the painted scene up top, a caption bar along the bottom."""
    scene(img, x, y, w, h - 64)
    # caption bar
    draw.rectangle([x, y + h - 64, x + w, y + h], fill=CREAM, outline=INK, width=3)
    head_font = load_font(SANS_B, 26)
    lines = wrap_text(draw, headline, head_font, w - 24)
    ly = y + h - 60
    for ln in lines[:2]:
        centred_text(draw, x + w / 2, ly, ln, head_font, INK)
        ly += 30
    # coloured tag chip floating on the scene
    tag_font = load_font(SANS_B, 20)
    tw = draw.textlength(tag, font=tag_font) + 20
    draw.rounded_rectangle(
        [x + 10, y + 10, x + 10 + tw, y + 38],
        radius=14, fill=tag_color, outline=INK, width=2,
    )
    draw.text((x + 20, y + 14), tag, font=tag_font, fill=(255, 255, 255))


# ---------------- scenes ----------------

def paint_climate(img, x, y, w, h):
    pen = ImageDraw.Draw(img)
    pen.rectangle([x, y, x + w, y + h], fill=(178, 216, 205))
    pen.rectangle([x, y + h - 46, x + w, y + h], fill=(120, 160, 120))
    # globe
    cx, cy, r = x + w // 2, y + 92, 66
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 190), outline=INK, width=4)
    pen.ellipse(
        [cx - r // 2, cy - r, cx + r // 2, cy + r],
        outline=(200, 230, 240), width=3,
    )
    pen.line([cx - r, cy, cx + r, cy], fill=(200, 230, 240), width=3)
    pen.line([cx - r + 12, cy - 40, cx + r - 12, cy - 40], fill=(200, 230, 240), width=2)
    pen.line([cx - r + 12, cy + 40, cx + r - 12, cy + 40], fill=(200, 230, 240), width=2)
    # crack across the globe
    pen.line(
        [cx - 52, cy - 30, cx - 18, cy + 2, cx - 38, cy + 26, cx + 6, cy + 52],
        fill=RED, width=6,
    )
    # factory with smoke, bottom left
    pen.rectangle([x + 26, y + h - 96, x + 76, y + h - 46], fill=(90, 90, 96), outline=INK, width=3)
    pen.rectangle([x + 84, y + h - 116, x + 128, y + h - 46], fill=(110, 110, 116), outline=INK, width=3)
    pen.rectangle([x + 34, y + h - 128, x + 44, y + h - 96], fill=(70, 70, 76), outline=INK, width=2)
    smoke = [(x + 44, y + h - 146, 12), (x + 58, y + h - 162, 15), (x + 76, y + h - 176, 18)]
    for bx, by, br in smoke:
        pen.ellipse([bx - br, by - br, bx + br, by + br], fill=(120, 120, 126))
    # red X stamp
    pen.line([x + w - 108, y + 52, x + w - 48, y + 112], fill=RED, width=12)
    pen.line([x + w - 48, y + 52, x + w - 108, y + 112], fill=RED, width=12)


def paint_warship(img, x, y, w, h):
    pen = ImageDraw.Draw(img)
    pen.rectangle([x, y, x + w, y + h], fill=(252, 196, 120))
    pen.rectangle([x, y + h - 70, x + w, y + h], fill=(38, 98, 150))
    for i in range(5):
        wx = x + 20 + i * 90
        pen.arc([wx, y + h - 78, wx + 60, y + h - 46], 0, 180, fill=(220, 235, 245), width=4)
    # warship silhouette
    sx, sy = x + 70, y + h - 96
    pen.polygon(
        [(sx, sy + 26), (sx + 330, sy + 26), (sx + 300, sy), (sx + 30, sy)],
        fill=(52, 58, 66), outline=INK,
    )
    pen.rectangle([sx + 90, sy - 26, sx + 190, sy], fill=(52, 58, 66), outline=INK, width=3)
    pen.rectangle([sx + 130, sy - 44, sx + 150, sy - 26], fill=(52, 58, 66), outline=INK, width=3)
    # explosion burst above the ship's bow
    ex, ey = sx + 120, sy - 42
    for ang in range(0, 360, 30):
        r1, r2 = 22, 46
        a = math.radians(ang)
        pen.line(
            [ex + r1 * math.cos(a), ey + r1 * math.sin(a),
             ex + r2 * math.cos(a), ey + r2 * math.sin(a)],
            fill=(240, 90, 30), width=9,
        )
    pen.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], fill=(255, 190, 60), outline=INK, width=3)
    # dark smoke above the blast
    pen.ellipse([ex - 40, ey - 66, ex - 8, ey - 34], fill=(70, 70, 76))
    pen.ellipse([ex + 6, ey - 74, ex + 42, ey - 40], fill=(90, 90, 96))
    # naval drone, top right
    dx, dy = x + 330, y + 26
    pen.line([dx, dy, dx + 90, dy], fill=INK, width=5)
    pen.ellipse([dx + 30, dy - 8, dx + 60, dy + 8], fill=(40, 40, 48), outline=INK, width=2)
    pen.ellipse([dx - 12, dy - 6, dx + 12, dy + 6], fill=(120, 120, 130), outline=INK, width=2)
    pen.ellipse([dx + 78, dy - 6, dx + 102, dy + 6], fill=(120, 120, 130), outline=INK, width=2)
    pen.line([dx + 45, dy + 8, dx + 45, dy + 30], fill=INK, width=4)


def paint_iran(img, x, y, w, h):
    pen = ImageDraw.Draw(img)
    pen.rectangle([x, y, x + w, y + h], fill=(210, 225, 235))
    pen.rectangle([x, y + h - 64, x + w, y + h], fill=(30, 80, 130))
    # aircraft carrier
    cx, cy = x + 40, y + h - 100
    pen.polygon(
        [(cx, cy + 36), (cx + 380, cy + 36), (cx + 350, cy + 10), (cx + 30, cy + 10)],
        fill=(70, 76, 84), outline=INK,
    )
    pen.rectangle([cx + 240, cy - 22, cx + 300, cy + 10], fill=(70, 76, 84), outline=INK, width=3)
    pen.line([cx + 270, cy - 22, cx + 270, cy - 52], fill=INK, width=5)
    # warning triangle
    tx, ty = x + w - 150, y + 26
    pen.polygon(
        [(tx + 55, ty), (tx + 110, ty + 96), (tx, ty + 96)],
        fill=(255, 200, 40), outline=INK, width=4,
    )
    pen.text((tx + 44, ty + 30), "!", font=load_font(SANS_B, 52), fill=INK)
    # jets
    for jx, jy in [(x + 46, y + 30), (x + 150, y + 62)]:
        pen.polygon(
            [(jx, jy + 10), (jx + 62, jy + 10), (jx + 78, jy + 18), (jx + 62, jy + 26), (jx, jy + 26)],
            fill=(52, 58, 66), outline=INK,
        )
        pen.polygon(
            [(jx + 24, jy), (jx + 40, jy + 10), (jx + 24, jy + 26)],
            fill=(52, 58, 66), outline=INK,
        )


def paint_nvidia(img, x, y, w, h):
    pen = ImageDraw.Draw(img)
    pen.rectangle([x, y, x + w, y + h], fill=(16, 24, 20))
    # rising chart line
    pts = [(x + 30, y + h - 70), (x + 110, y + h - 100), (x + 170, y + h - 84),
           (x + 250, y + h - 130), (x + 330, y + h - 108), (x + 420, y + h - 148)]
    pen.line(pts, fill=(118, 185, 0), width=7)
    pen.polygon(
        [(x + 420, y + h - 160), (x + 452, y + h - 160), (x + 436, y + h - 132)],
        fill=(118, 185, 0),
    )
    # chip
    cx, cy, s = x + w - 150, y + 96, 52
    for i in range(3):
        off = i * 30
        pen.line([cx - s - 16, cy - 30 + off, cx - s, cy - 30 + off], fill=(180, 190, 200), width=5)
        pen.line([cx + s, cy - 30 + off, cx + s + 16, cy - 30 + off], fill=(180, 190, 200), width=5)
        pen.line([cx - 30 + off, cy - s - 16, cx - 30 + off, cy - s], fill=(180, 190, 200), width=5)
        pen.line([cx - 30 + off, cy + s, cx - 30 + off, cy + s + 16], fill=(180, 190, 200), width=5)
    pen.rounded_rectangle(
        [cx - s, cy - s, cx + s, cy + s],
        radius=12, fill=(30, 130, 60), outline=INK, width=4,
    )
    pen.rounded_rectangle(
        [cx - 28, cy - 28, cx + 28, cy + 28],
        radius=8, fill=(16, 24, 20), outline=(118, 185, 0), width=3,
    )
    pen.text((cx - 14, cy - 16), "AI", font=load_font(SANS_B, 30), fill=(118, 185, 0))
    # stars
    for sx, sy in [(x + 60, y + 40), (x + 200, y + 26), (x + 330, y + 44)]:
        pen.polygon(
            [(sx, sy - 8), (sx + 3, sy - 3), (sx + 8, sy), (sx + 3, sy + 3),
             (sx, sy + 8), (sx - 3, sy + 3), (sx - 8, sy), (sx - 3, sy - 3)],
            fill=(255, 220, 120),
        )


def paint_toll(img, x, y, w, h):
    pen = ImageDraw.Draw(img)
    pen.rectangle([x, y, x + w, y + h], fill=(40, 36, 40))
    # faint bar chart of rising losses along the bottom
    bars = [18, 28, 24, 38, 32, 48, 42, 54]
    bw = (w - 60) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 30 + i * bw
        pen.rectangle(
            [bx, y + h - 20 - bh, bx + bw - 8, y + h - 20],
            fill=(120, 40, 44), outline=INK, width=2,
        )
    # the number
    big = load_font(SANS_B, 70)
    centred_text(pen, x + w // 2, y + 38, "700,000", big, (240, 235, 220))


def paint_health(img, x, y, w, h):
    pen = ImageDraw.Draw(img)
    pen.rectangle([x, y, x + w, y + h], fill=(190, 225, 200))
    # shield
    sx, sy = x + 70, y + 30
    pen.polygon(
        [(sx, sy), (sx + 120, sy), (sx + 120, sy + 70), (sx + 60, sy + 120), (sx, sy + 70)],
        fill=(30, 130, 90), outline=INK, width=4,
    )
    pen.line([sx + 28, sy + 58, sx + 52, sy + 84, sx + 96, sy + 32], fill=(255, 255, 255), width=9)
    # vaccine vial, right edge
    vx, vy = x + 404, y + 100
    pen.rectangle([vx, vy, vx + 44, vy + 66], fill=(220, 235, 245), outline=INK, width=4)
    pen.rectangle([vx + 12, vy - 14, vx + 32, vy], fill=(150, 160, 170), outline=INK, width=3)
    pen.line([vx + 22, vy - 14, vx + 22, vy - 34], fill=INK, width=5)
    pen.rectangle([vx + 6, vy + 24, vx + 38, vy + 44], fill=(30, 130, 90))
    # children dots row
    for i in range(5):
        cx = x + 50 + i * 68
        pen.ellipse([cx, y + h - 62, cx + 34, y + h - 28], fill=(255, 205, 150), outline=INK, width=3)
        pen.arc([cx - 6, y + h - 30, cx + 40, y + h + 6], 180, 360, fill=(60, 90, 160), width=16)
    # big 50M
    big = load_font(SANS_B, 76)
    centred_text(pen, x + w - 110, y + 22, "50M", big, (20, 90, 60))


def build_collage():
    img = Image.new("RGB", (W, H), PAPER)
    pen = ImageDraw.Draw(img)
    # outer border
    pen.rectangle([10, 10, W - 11, H - 11], outline=INK, width=4)
    # masthead
    pen.rectangle([24, 24, W - 24, 128], fill=NAVY, outline=INK, width=3)
    mast_font = load_font(SERIF_B, 74)
    centred_text(pen, W // 2, 30, "THE WORLD TODAY", mast_font, ORANGE)
    # date line
    date_font = load_font(SANS_B, 34)
    centred_text(pen, W // 2, 146, "TUESDAY 24 NOVEMBER 2026", date_font, TEAL, tracking=4)
    pen.line([24, 196, W - 24, 196], fill=INK, width=3)

    panels = [
        (paint_climate, "CLIMATE", (31, 122, 109), "COP31 COLLAPSES", ""),
        (paint_warship, "WAR", (185, 28, 28), "UKRAINE SINKS RUSSIAN WARSHIP", ""),
        (paint_iran, "U.S.–IRAN", (18, 58, 92), "TRUMP WARNS IRAN OF 'VERY TRAUMATIC' END", ""),
        (paint_nvidia, "TECH", (30, 130, 60), "HUANG IS BACK AT NVIDIA", ""),
        (paint_toll, "THE TOLL", (120, 40, 44), "700,000 RUSSIAN WAR DEAD", ""),
        (paint_health, "HEALTH", (30, 130, 90), "50M CHILDREN IN TYPHOID DRIVE", ""),
    ]
    px, py = 24, 210
    pw, ph = 480, 236
    gx, gy = 16, 14
    for i, (scene, tag, tc, head, sub) in enumerate(panels):
        x = px + (i % 2) * (pw + gx)
        y = py + (i // 2) * (ph + gy)
        draw_panel(pen, img, x, y, pw, ph, scene, tag, tc, head, sub)

    # sports strip
    sy = 210 + 3 * ph + 2 * gy + 12
    pen.rectangle([24, sy, W - 24, sy + 52], fill=NAVY, outline=INK, width=3)
    sport_font = load_font(SANS_B, 21)
    centred_text(
        pen, W // 2, sy + 12,
        "SPORT  •  BRENTFORD 4–0 EVERTON  •  COMMANDERS 22–20 BENGALS",
        sport_font, (255, 255, 255),
    )
    return img


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    image = build_collage()
    image.save(target, optimize=True)
    import os
    print(target, os.path.getsize(target), "bytes", image.size)
