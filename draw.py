#!/usr/bin/env python3
"""Draw the news-image-20261124 collage: 'THE WORLD TODAY — TUESDAY 24 NOVEMBER 2026'.

Deterministic PIL drawing (no network, no randomness). 1024x1024, saves entry.png
beside the repo files. Headlines are the day's sourced stories (see README.md).

This is the single source of the bundled picture: run `python3 draw.py` to
regenerate entry.png byte-for-byte, then `node main.ts` copies it to the
grader's output directory. No network is touched at any point.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (244, 239, 227)
INK = (18, 24, 32)
NAVY = (18, 58, 92)
ORANGE = (240, 120, 48)
TEAL = (31, 122, 109)
RED = (185, 28, 28)
CREAM = (250, 246, 236)
GOLD = (212, 160, 32)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center_text(draw, cx, y, text, fnt, fill, tracking=0):
    if tracking:
        # manual letter-spacing
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


def panel(draw, img, x, y, w, h, scene, tag, tag_color, headline, sub):
    """A panel: drawn scene on top, caption bar at the bottom."""
    scene(img, x, y, w, h - 64)
    # caption bar
    draw.rectangle([x, y + h - 64, x + w, y + h], fill=CREAM, outline=INK, width=3)
    f_head = font(SANS_B, 26)
    lines = wrap(draw, headline, f_head, w - 24)
    ly = y + h - 60
    for ln in lines[:2]:
        center_text(draw, x + w / 2, ly, ln, f_head, INK)
        ly += 30
    # tag chip on the scene
    f_tag = font(SANS_B, 20)
    tw = draw.textlength(tag, font=f_tag) + 20
    draw.rounded_rectangle([x + 10, y + 10, x + 10 + tw, y + 38], radius=14,
                           fill=tag_color, outline=INK, width=2)
    draw.text((x + 20, y + 14), tag, font=f_tag, fill=(255, 255, 255))


# ---------------- scenes ----------------

def scene_cop31(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(178, 216, 205))
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(120, 160, 120))
    # globe
    cx, cy, r = x + w // 2, y + 92, 66
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 190), outline=INK, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(200, 230, 240), width=3)
    d.line([cx - r, cy, cx + r, cy], fill=(200, 230, 240), width=3)
    d.line([cx - r + 12, cy - 40, cx + r - 12, cy - 40], fill=(200, 230, 240), width=2)
    d.line([cx - r + 12, cy + 40, cx + r - 12, cy + 40], fill=(200, 230, 240), width=2)
    # crack across the globe
    d.line([cx - 52, cy - 30, cx - 18, cy + 2, cx - 38, cy + 26, cx + 6, cy + 52],
           fill=RED, width=6)
    # factory with smoke, bottom left
    d.rectangle([x + 26, y + h - 96, x + 76, y + h - 46], fill=(90, 90, 96), outline=INK, width=3)
    d.rectangle([x + 84, y + h - 116, x + 128, y + h - 46], fill=(110, 110, 116), outline=INK, width=3)
    d.rectangle([x + 34, y + h - 128, x + 44, y + h - 96], fill=(70, 70, 76), outline=INK, width=2)
    for i, (bx, by, br) in enumerate([(x + 44, y + h - 146, 12), (x + 58, y + h - 162, 15), (x + 76, y + h - 176, 18)]):
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(120, 120, 126))
    # red X stamp
    d.line([x + w - 108, y + 52, x + w - 48, y + 112], fill=RED, width=12)
    d.line([x + w - 48, y + 52, x + w - 108, y + 112], fill=RED, width=12)


def scene_warship(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(252, 196, 120))
    d.rectangle([x, y + h - 70, x + w, y + h], fill=(38, 98, 150))
    for i in range(5):
        wx = x + 20 + i * 90
        d.arc([wx, y + h - 78, wx + 60, y + h - 46], 0, 180, fill=(220, 235, 245), width=4)
    # warship silhouette
    sx, sy = x + 70, y + h - 96
    d.polygon([(sx, sy + 26), (sx + 330, sy + 26), (sx + 300, sy), (sx + 30, sy)],
              fill=(52, 58, 66), outline=INK)
    d.rectangle([sx + 90, sy - 26, sx + 190, sy], fill=(52, 58, 66), outline=INK, width=3)
    d.rectangle([sx + 130, sy - 44, sx + 150, sy - 26], fill=(52, 58, 66), outline=INK, width=3)
    # explosion burst above the ship's bow
    ex, ey = sx + 120, sy - 42
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 22, 46
        a = math.radians(ang)
        d.line([ex + r1 * math.cos(a), ey + r1 * math.sin(a),
                ex + r2 * math.cos(a), ey + r2 * math.sin(a)], fill=(240, 90, 30), width=9)
    d.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], fill=(255, 190, 60), outline=INK, width=3)
    # dark smoke above the blast
    d.ellipse([ex - 40, ey - 66, ex - 8, ey - 34], fill=(70, 70, 76))
    d.ellipse([ex + 6, ey - 74, ex + 42, ey - 40], fill=(90, 90, 96))
    # naval drone, top right
    dx, dy = x + 330, y + 26
    d.line([dx, dy, dx + 90, dy], fill=INK, width=5)
    d.ellipse([dx + 30, dy - 8, dx + 60, dy + 8], fill=(40, 40, 48), outline=INK, width=2)
    d.ellipse([dx - 12, dy - 6, dx + 12, dy + 6], fill=(120, 120, 130), outline=INK, width=2)
    d.ellipse([dx + 78, dy - 6, dx + 102, dy + 6], fill=(120, 120, 130), outline=INK, width=2)
    d.line([dx + 45, dy + 8, dx + 45, dy + 30], fill=INK, width=4)


def scene_iran(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(210, 225, 235))
    d.rectangle([x, y + h - 64, x + w, y + h], fill=(30, 80, 130))
    # aircraft carrier
    cx, cy = x + 40, y + h - 100
    d.polygon([(cx, cy + 36), (cx + 380, cy + 36), (cx + 350, cy + 10), (cx + 30, cy + 10)],
              fill=(70, 76, 84), outline=INK)
    d.rectangle([cx + 240, cy - 22, cx + 300, cy + 10], fill=(70, 76, 84), outline=INK, width=3)
    d.line([cx + 270, cy - 22, cx + 270, cy - 52], fill=INK, width=5)
    # warning triangle
    tx, ty = x + w - 150, y + 26
    d.polygon([(tx + 55, ty), (tx + 110, ty + 96), (tx, ty + 96)],
              fill=(255, 200, 40), outline=INK, width=4)
    d.text((tx + 44, ty + 30), "!", font=font(SANS_B, 52), fill=INK)
    # jets
    for jx, jy in [(x + 46, y + 30), (x + 150, y + 62)]:
        d.polygon([(jx, jy + 10), (jx + 62, jy + 10), (jx + 78, jy + 18), (jx + 62, jy + 26), (jx, jy + 26)],
                  fill=(52, 58, 66), outline=INK)
        d.polygon([(jx + 24, jy), (jx + 40, jy + 10), (jx + 24, jy + 26)], fill=(52, 58, 66), outline=INK)


def scene_nvidia(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 20))
    # rising chart line
    pts = [(x + 30, y + h - 70), (x + 110, y + h - 100), (x + 170, y + h - 84),
           (x + 250, y + h - 130), (x + 330, y + h - 108), (x + 420, y + h - 148)]
    d.line(pts, fill=(118, 185, 0), width=7)
    d.polygon([(x + 420, y + h - 160), (x + 452, y + h - 160), (x + 436, y + h - 132)],
              fill=(118, 185, 0))
    # chip
    cx, cy, s = x + w - 150, y + 96, 52
    for i in range(3):
        d.line([cx - s - 16, cy - 30 + i * 30, cx - s, cy - 30 + i * 30], fill=(180, 190, 200), width=5)
        d.line([cx + s, cy - 30 + i * 30, cx + s + 16, cy - 30 + i * 30], fill=(180, 190, 200), width=5)
        d.line([cx - 30 + i * 30, cy - s - 16, cx - 30 + i * 30, cy - s], fill=(180, 190, 200), width=5)
        d.line([cx - 30 + i * 30, cy + s, cx - 30 + i * 30, cy + s + 16], fill=(180, 190, 200), width=5)
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=12,
                        fill=(30, 130, 60), outline=INK, width=4)
    d.rounded_rectangle([cx - 28, cy - 28, cx + 28, cy + 28], radius=8,
                        fill=(16, 24, 20), outline=(118, 185, 0), width=3)
    d.text((cx - 14, cy - 16), "AI", font=font(SANS_B, 30), fill=(118, 185, 0))
    # stars
    for sx, sy in [(x + 60, y + 40), (x + 200, y + 26), (x + 330, y + 44)]:
        d.polygon([(sx, sy - 8), (sx + 3, sy - 3), (sx + 8, sy), (sx + 3, sy + 3),
                   (sx, sy + 8), (sx - 3, sy + 3), (sx - 8, sy), (sx - 3, sy - 3)],
                  fill=(255, 220, 120))


def scene_dead(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(40, 36, 40))
    # faint bar chart of rising losses along the bottom
    bars = [18, 28, 24, 38, 32, 48, 42, 54]
    bw = (w - 60) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 30 + i * bw
        d.rectangle([bx, y + h - 20 - bh, bx + bw - 8, y + h - 20],
                    fill=(120, 40, 44), outline=INK, width=2)
    # the number
    f_big = font(SANS_B, 70)
    center_text(d, x + w // 2, y + 38, "700,000", f_big, (240, 235, 220))


def scene_bangladesh(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(190, 225, 200))
    # shield
    sx, sy = x + 70, y + 30
    d.polygon([(sx, sy), (sx + 120, sy), (sx + 120, sy + 70), (sx + 60, sy + 120), (sx, sy + 70)],
              fill=(30, 130, 90), outline=INK, width=4)
    d.line([sx + 28, sy + 58, sx + 52, sy + 84, sx + 96, sy + 32], fill=(255, 255, 255), width=9)
    # vaccine vial, right edge
    vx, vy = x + 404, y + 100
    d.rectangle([vx, vy, vx + 44, vy + 66], fill=(220, 235, 245), outline=INK, width=4)
    d.rectangle([vx + 12, vy - 14, vx + 32, vy], fill=(150, 160, 170), outline=INK, width=3)
    d.line([vx + 22, vy - 14, vx + 22, vy - 34], fill=INK, width=5)
    d.rectangle([vx + 6, vy + 24, vx + 38, vy + 44], fill=(30, 130, 90))
    # children dots row
    for i in range(5):
        cx = x + 50 + i * 68
        d.ellipse([cx, y + h - 62, cx + 34, y + h - 28], fill=(255, 205, 150), outline=INK, width=3)
        d.arc([cx - 6, y + h - 30, cx + 40, y + h + 6], 180, 360, fill=(60, 90, 160), width=16)
    # big 50M
    f_big = font(SANS_B, 76)
    center_text(d, x + w - 110, y + 22, "50M", f_big, (20, 90, 60))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=4)
    # masthead
    d.rectangle([24, 24, W - 24, 128], fill=NAVY, outline=INK, width=3)
    f_mast = font(SERIF_B, 74)
    center_text(d, W // 2, 30, "THE WORLD TODAY", f_mast, ORANGE)
    # date line
    f_date = font(SANS_B, 34)
    center_text(d, W // 2, 146, "TUESDAY 24 NOVEMBER 2026", f_date, TEAL, tracking=4)
    d.line([24, 196, W - 24, 196], fill=INK, width=3)

    panels = [
        (scene_cop31, "CLIMATE", (31, 122, 109), "COP31 COLLAPSES", ""),
        (scene_warship, "WAR", (185, 28, 28), "UKRAINE SINKS RUSSIAN WARSHIP", ""),
        (scene_iran, "U.S.–IRAN", (18, 58, 92), "TRUMP WARNS IRAN OF 'VERY TRAUMATIC' END", ""),
        (scene_nvidia, "TECH", (30, 130, 60), "HUANG IS BACK AT NVIDIA", ""),
        (scene_dead, "THE TOLL", (120, 40, 44), "700,000 RUSSIAN WAR DEAD", ""),
        (scene_bangladesh, "HEALTH", (30, 130, 90), "50M CHILDREN IN TYPHOID DRIVE", ""),
    ]
    px, py = 24, 210
    pw, ph = 480, 236
    gx, gy = 16, 14
    for i, (scene, tag, tc, head, sub) in enumerate(panels):
        x = px + (i % 2) * (pw + gx)
        y = py + (i // 2) * (ph + gy)
        panel(d, img, x, y, pw, ph, scene, tag, tc, head, sub)

    # sports strip
    sy = 210 + 3 * ph + 2 * gy + 12
    d.rectangle([24, sy, W - 24, sy + 52], fill=NAVY, outline=INK, width=3)
    f_sport = font(SANS_B, 21)
    center_text(d, W // 2, sy + 12,
                "SPORT  •  BRENTFORD 4–0 EVERTON  •  COMMANDERS 22–20 BENGALS",
                f_sport, (255, 255, 255))
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    im = build()
    im.save(out, optimize=True)
    import os
    print(out, os.path.getsize(out), "bytes", im.size)
