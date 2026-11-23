#!/usr/bin/env python3
"""Render the WORLD NEWS front page for Monday, 23 November 2026.

Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width: 952
BLACK = (0, 0, 0)
RED = (178, 0, 0)
GREY = (90, 90, 90)
LIGHT = (235, 235, 235)
BLUE = (28, 84, 150)
GREEN = (46, 125, 62)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text(draw, x, y, lines, fnt, fill=BLACK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=1, fill=BLACK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    rule(d, M, 26, W - M, 3)
    mast = font(SERIF_B, 92)
    d.text((W // 2, 34), "WORLD NEWS", font=mast, fill=BLACK, anchor="ma")
    rule(d, M, 140, W - M, 2)
    # date line, red
    date_f = font(SANS_B, 24)
    d.text((W // 2, 152), "MONDAY, 23 NOVEMBER 2026", font=date_f,
           fill=RED, anchor="ma")
    rule(d, M, 192, W - M, 2)

    # ---- lead story: COP31 ----
    y = 210
    kick = font(SANS_B, 17)
    d.text((M, y), "CLIMATE  —  ANTALYA", font=kick, fill=RED)
    y += 30
    lead_head = font(SERIF_B, 44)
    lead_lines = wrap(d, "COP31 collapses as summit ends with no deal",
                      lead_head, 700)
    y = draw_text(d, M, y, lead_lines, lead_head, leading=52)
    y += 8
    lead_body = font(SERIF, 19)
    body = ("The UN summit in Antalya collapsed without a deal after the "
            "EU and allies rejected a draft silent on fossil fuels. "
            "Australia's PM called it a sign of 'difficult geopolitical "
            "times'.")
    body_lines = wrap(d, body, lead_body, 700)[:3]
    y = draw_text(d, M, y, body_lines, lead_body, leading=26)

    # lead illustration: a cracked globe
    gx, gy, gr = 830, 268, 70
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=BLUE,
              outline=BLACK, width=3)
    # meridians
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 90, 270, fill=WHITE, width=2)
    d.arc([gx - gr // 2, gy - gr, gx + gr // 2, gy + gr], 90, 270,
          fill=WHITE, width=2)
    d.line([(gx - gr, gy), (gx + gr, gy)], fill=WHITE, width=2)
    d.line([(gx, gy - gr), (gx, gy + gr)], fill=WHITE, width=2)
    # landmass blobs
    d.polygon([(gx - 55, gy - 30), (gx - 10, gy - 48), (gx + 5, gy - 20),
               (gx - 25, gy - 5)], fill=GREEN)
    d.polygon([(gx + 10, gy + 15), (gx + 55, gy + 5), (gx + 48, gy + 42),
               (gx + 15, gy + 50)], fill=GREEN)
    # crack (kept inside the globe)
    crack = [(gx - 48, gy - 38), (gx - 22, gy - 16), (gx - 40, gy + 4),
             (gx - 8, gy + 24), (gx - 20, gy + 48)]
    d.line(crack, fill=RED, width=5, joint="curve")
    d.text((gx, gy + gr + 12), "ANTALYA", font=font(SANS_B, 14),
           fill=GREY, anchor="ma")

    rule(d, M, 442, W - M, 2)

    # ---- grid stories: 2 columns x 3 rows ----
    stories = [
        ("LIBYA  —  BENGHAZI",
         "Sea drones hit Russian warship at Benghazi base",
         "Ukrainian sea drones struck the Russian corvette Merkury at "
         "Benghazi naval base on Sunday. The warship was badly damaged "
         "and later capsized; 10 people were hurt."),
        ("GULF  —  STRAIT OF HORMUZ",
         "Three tankers struck near Strait of Hormuz",
         "Three oil tankers were hit near the Strait of Hormuz on Friday "
         "and Saturday, and two more caught fire on Sunday after hitting "
         "mines."),
        ("FOOTBALL  —  ZURICH",
         "FIFA confirms UK as host of 2035 Women's World Cup",
         "FIFA confirmed on Monday that the United Kingdom will host the "
         "2035 Women's World Cup — the first World Cup in Britain since "
         "1966."),
        ("SOUTH SUDAN",
         "24 civilians killed in fresh SPLA-IO attack",
         "At least 24 civilians were killed in a fresh attack by SPLA-IO "
         "forces, officials said, in the latest violence to hit the "
         "country."),
        ("INDONESIA  —  BANTEN",
         "Factory fire toll rises as more bodies recovered",
         "Rescuers have recovered 24 body bags from the Cikande candy "
         "factory after Sunday's fire, and dozens of workers are still "
         "missing."),
        ("JAPAN",
         "Magnitude 6.1 quake jolts northern Japan",
         "A magnitude 6.1 earthquake jolted northern Japan on Monday. "
         "There were no reports of major damage and no tsunami warning "
         "was issued."),
    ]
    col_w = (CW - 24) // 2
    row_h = 150
    y0 = 452
    for i, (kicker, head, body) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = M + col * (col_w + 24)
        y = y0 + row * row_h
        d.text((x, y), kicker, font=font(SANS_B, 15), fill=RED)
        y += 24
        head_lines = wrap(d, head, font(SERIF_B, 23), col_w)[:2]
        y = draw_text(d, x, y, head_lines, font(SERIF_B, 23), leading=28)
        y += 4
        body_lines = wrap(d, body, font(SERIF, 17), col_w)[:3]
        draw_text(d, x, y, body_lines, font(SERIF, 17), leading=22)
        if col == 0:
            d.line([(x + col_w + 12, y0 + row * row_h),
                    (x + col_w + 12, y0 + row * row_h + row_h - 14)],
                   fill=LIGHT, width=1)
        if row < 2:
            rule(d, M, y0 + (row + 1) * row_h - 12, W - M, 1, fill=LIGHT)

    # ---- bottom strip ----
    strip_y = 918
    d.rectangle([M, strip_y, W - M, strip_y + 72], fill=BLACK)
    strip_f = font(SANS_B, 19)
    strip_lines = wrap(d, "ALSO TODAY:  India and China hold border talks  •  "
                          "Liverpool beat ten-man Manchester United in "
                          "Pochettino's debut", strip_f, CW - 40)
    sy = strip_y + 14
    for line in strip_lines[:2]:
        d.text((W // 2, sy), line, font=strip_f, fill=WHITE, anchor="ma")
        sy += 24
    d.text((W // 2, 998), "WORLD NEWS  •  MONDAY, 23 NOVEMBER 2026",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
