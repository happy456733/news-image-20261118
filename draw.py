#!/usr/bin/env python3
"""Draw a one-page newspaper front page summing up 18 November 2026.

Every word on the poster is rendered here in code with DejaVu fonts.
No AI-generated text, no copied images: all pictograms are drawn with
Pillow primitives. Output is deterministic: fixed palette, fixed layout,
no timestamps, no randomness.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (176, 30, 36)
BLUE = (31, 68, 120)
TEAL = (18, 110, 105)
GOLD = (176, 124, 22)
GREY = (110, 104, 92)
LIGHT = (233, 226, 210)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def masthead(draw):
    draw_center(draw, W // 2, 22, "THE WORLD IN ONE DAY",
                font(SERIF_B, 62), INK)
    rule(draw, 48, W - 48, 100, INK, 3)
    draw_center(draw, W // 2, 112, "WEDNESDAY,  18 NOVEMBER 2026",
                font(SANS_B, 34), RED)
    rule(draw, 48, W - 48, 158, INK, 3)
    draw_center(draw, W // 2, 168, "ONE DAY  ·  ONE PAGE  ·  SEVEN STORIES",
                font(SANS, 17), GREY)


def burst(draw, cx, cy, r, fill):
    """Starburst explosion: alternating long/short spikes."""
    import math
    pts = []
    for i in range(24):
        ang = math.pi * 2 * i / 24
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def pic_lead(draw, x, y, s):
    """Gulf strikes: explosion over waves."""
    draw.rectangle([x, y, x + s, y + s], fill=BLUE)
    draw.ellipse([x + s * 0.08, y + s * 0.10, x + s * 0.42, y + s * 0.44],
                 fill=(240, 214, 120))
    burst(draw, x + s * 0.62, y + s * 0.42, s * 0.30, (232, 90, 32))
    burst(draw, x + s * 0.62, y + s * 0.42, s * 0.17, (250, 200, 60))
    for i, wy in enumerate((0.72, 0.82, 0.92)):
        draw.arc([x + s * 0.05, y + s * wy, x + s * 0.95, y + s * (wy + 0.16)],
                 0, 180, fill=WHITE, width=6)


def lead_story(draw):
    x0, y0, x1, y1 = 48, 200, W - 48, 410
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=3)
    draw.rectangle([x0, y0, x1, y0 + 30], fill=RED)
    draw.text((x0 + 14, y0 + 4), "LEAD STORY — MIDDLE EAST",
              font=font(SANS_B, 18), fill=WHITE)
    pic_lead(draw, x0 + 14, y0 + 44, 138)
    tx = x0 + 170
    draw.text((tx, y0 + 42), "GULF IN FLAMES: U.S. STRIKES IRAN;",
              font=font(SERIF_B, 30), fill=INK)
    draw.text((tx, y0 + 82), "TEHRAN HITS BACK AT GULF BASES",
              font=font(SERIF_B, 30), fill=INK)
    body = ("U.S. jets hit a missile site on Qeshm Island. Iran answered "
            "with strikes on bases in Kuwait and Bahrain hosting U.S. forces.")
    for i, ln in enumerate(wrap(draw, body, font(SANS, 18), x1 - tx - 14)):
        draw.text((tx, y0 + 132 + i * 23), ln, font=font(SANS, 18), fill=INK)


def pic_bridge(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(214, 228, 240))
    draw.rectangle([x, y + s * 0.78, x + s, y + s], fill=BLUE)
    draw.arc([x + s * 0.08, y + s * 0.30, x + s * 0.92, y + s * 0.95],
             180, 360, fill=INK, width=8)
    draw.rectangle([x + s * 0.05, y + s * 0.52, x + s * 0.95, y + s * 0.60],
                   fill=INK)
    draw.line([(x + s * 0.52, y + s * 0.52), (x + s * 0.58, y + s * 0.66),
               (x + s * 0.50, y + s * 0.74)], fill=RED, width=6)
    draw.line([(x + s * 0.10, y + s * 0.60), (x + s * 0.10, y + s * 0.80)],
              fill=INK, width=6)
    draw.line([(x + s * 0.90, y + s * 0.60), (x + s * 0.90, y + s * 0.80)],
              fill=INK, width=6)


def pic_summit(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(232, 222, 196))
    cols = [(176, 30, 36), (31, 68, 120), (176, 124, 22)]
    for i, c in enumerate(cols):
        fx = x + s * (0.16 + i * 0.34)
        draw.line([(fx, y + s * 0.18), (fx, y + s * 0.88)], fill=INK, width=5)
        draw.polygon([(fx, y + s * 0.18), (fx + s * 0.26, y + s * 0.28),
                      (fx, y + s * 0.38)], fill=c)
        draw.ellipse([fx - 4, y + s * 0.86, fx + 4, y + s * 0.94], fill=INK)


def pic_ballot(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(222, 232, 222))
    draw.rectangle([x + s * 0.18, y + s * 0.45, x + s * 0.82, y + s * 0.90],
                   fill=BLUE)
    draw.rectangle([x + s * 0.38, y + s * 0.40, x + s * 0.62, y + s * 0.50],
                   fill=INK)
    draw.rectangle([x + s * 0.30, y + s * 0.12, x + s * 0.66, y + s * 0.42],
                   fill=WHITE, outline=INK, width=2)
    draw.line([(x + s * 0.36, y + s * 0.28), (x + s * 0.44, y + s * 0.36),
               (x + s * 0.60, y + s * 0.18)], fill=RED, width=5)
    draw.line([(x + s * 0.30, y + s * 0.66), (x + s * 0.44, y + s * 0.78),
               (x + s * 0.68, y + s * 0.56)], fill=WHITE, width=7)


def virus(draw, cx, cy, r, fill):
    import math
    for i in range(10):
        ang = math.pi * 2 * i / 10
        x1 = cx + r * 0.9 * math.cos(ang)
        y1 = cy + r * 0.9 * math.sin(ang)
        x2 = cx + r * 1.35 * math.cos(ang)
        y2 = cy + r * 1.35 * math.sin(ang)
        draw.line([(x1, y1), (x2, y2)], fill=fill, width=5)
        draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=fill)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    draw.ellipse([cx - r * 0.35, cy - r * 0.45, cx - r * 0.05, cy - r * 0.15],
                 fill=WHITE)
    draw.ellipse([cx + r * 0.15, cy + r * 0.10, cx + r * 0.40, cy + r * 0.35],
                 fill=WHITE)


def pic_measles(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 226, 226))
    virus(draw, x + s * 0.5, y + s * 0.5, s * 0.26, RED)


def pic_ebola(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(232, 226, 240))
    virus(draw, x + s * 0.5, y + s * 0.52, s * 0.28, (96, 32, 96))
    draw.rectangle([x + s * 0.72, y + s * 0.08, x + s * 0.80, y + s * 0.24],
                   fill=RED)
    draw.rectangle([x + s * 0.68, y + s * 0.12, x + s * 0.84, y + s * 0.20],
                   fill=RED)


def pic_voyager(draw, x, y, s):
    import math
    draw.rectangle([x, y, x + s, y + s], fill=(16, 22, 48))
    for sx, sy in ((0.15, 0.2), (0.8, 0.15), (0.3, 0.12), (0.65, 0.3),
                   (0.9, 0.55), (0.12, 0.55), (0.5, 0.08)):
        draw.ellipse([x + s * sx - 2, y + s * sy - 2,
                      x + s * sx + 2, y + s * sy + 2], fill=WHITE)
    draw.arc([x + s * 0.02, y + s * 0.55, x + s * 0.98, y + s * 1.05],
             200, 340, fill=(120, 160, 220), width=3)
    cx, cy = x + s * 0.55, y + s * 0.45
    draw.polygon([(cx, cy - s * 0.22), (cx + s * 0.20, cy + s * 0.05),
                  (cx - s * 0.02, cy + s * 0.02)], fill=(200, 200, 210))
    draw.line([(cx + s * 0.02, cy), (cx + s * 0.34, cy + s * 0.30)],
              fill=(200, 200, 210), width=4)
    draw.ellipse([cx + s * 0.30, cy + s * 0.26, cx + s * 0.38, cy + s * 0.34],
                 fill=GOLD)


STORIES = [
    ("EUROPE — UKRAINE WAR", "BRIDGE TO CRIMEA HIT AGAIN",
     "Ukrainian drones and missiles partly collapse the Kerch bridge; "
     "a road span falls into the strait.", pic_bridge, RED),
    ("ASIA — DIPLOMACY", "XI AND PUTIN MEET AHEAD OF SUMMIT",
     "The two leaders meet in Shenzhen, denouncing protectionism and "
     "sanctions ahead of Thursday's three-way summit with Trump.",
     pic_summit, BLUE),
    ("U.S. — POLITICS", "PELTOLA WINS ALASKA SENATE RACE",
     "Mary Peltola beats Dan Sullivan; Democrats now hold a 56–44 "
     "majority in the Senate.", pic_ballot, TEAL),
    ("U.S. — HEALTH", "U.S. MEASLES-FREE STATUS ENDS",
     "After 26 years: 5,412 cases in 2026, the most since 1991, end "
     "the country's elimination status.", pic_measles, RED),
    ("AFRICA — HEALTH", "EBOLA IN CONGO PASSES 11,000 CASES",
     "The outbreak more than doubles in three months; children under "
     "five bear the heaviest toll.", pic_ebola, (96, 32, 96)),
    ("SCIENCE — SPACE", "VOYAGER 1, ONE LIGHT-DAY AWAY",
     "NASA's probe reaches 16 billion miles from Earth — farther "
     "than any human-made object has travelled.", pic_voyager, BLUE),
]


def card(draw, x, y, w, h, kicker, headline, body, pic, accent):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x, y, x + 6, y + h], fill=accent)
    pic(draw, x + 16, y + 16, 118)
    tx = x + 148
    tw = w - 148 - 14
    draw.text((tx, y + 12), kicker, font=font(SANS_B, 14), fill=accent)
    hl = wrap(draw, headline, font(SERIF_B, 23), tw)
    hy = y + 34
    for ln in hl[:2]:
        draw.text((tx, hy), ln, font=font(SERIF_B, 23), fill=INK)
        hy += 28
    by = hy + 4
    for ln in wrap(draw, body, font(SANS, 16), tw)[:3]:
        draw.text((tx, by), ln, font=font(SANS, 16), fill=INK)
        by += 21


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead_story(draw)
    gx, gy = 48, 426
    cw, ch, gap = 456, 180, 16
    for i, (kicker, headline, body, pic, accent) in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        card(draw, cx, cy, cw, ch, kicker, headline, body, pic, accent)
    rule(draw, 48, W - 48, 1000, INK, 2)
    draw_center(draw, W // 2, 1006,
                "Sources: Reuters · AP · BBC · Al Jazeera · NASA  —  18 November 2026",
                font(SANS, 13), GREY)
    img.save(out_path, "PNG", optimize=True)


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
