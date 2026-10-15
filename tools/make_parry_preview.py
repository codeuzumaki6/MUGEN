#!/usr/bin/env python3
"""Render Daemon's two-second unblockable parry preview."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from make_combo_preview import KFM_SFF, ROOT, Sff2, background, load, place


OUT = ROOT / "previews/Daemon_parry_RB.gif"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = ImageFont.truetype(FONT_PATH, 12) if Path(FONT_PATH).exists() else ImageFont.load_default()
SMALL = ImageFont.truetype(FONT_PATH, 8) if Path(FONT_PATH).exists() else ImageFont.load_default()


def text_center(canvas: Image.Image, text: str, y: int, color=(255, 255, 255, 255)):
    draw = ImageDraw.Draw(canvas, "RGBA")
    box = draw.textbbox((0, 0), text, font=FONT, stroke_width=1)
    draw.text(((320 - box[2] + box[0]) // 2, y), text, font=FONT, fill=color, stroke_width=1, stroke_fill=(8, 16, 35, 255))


def hud(canvas: Image.Image, enemy_life=1000, power=1000):
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((7, 7, 147, 18), fill=(13, 16, 26, 240), outline=(230, 240, 255, 255))
    draw.rectangle((10, 10, 143, 15), fill=(55, 205, 230, 255))
    draw.text((8, 20), "EIDA", font=SMALL, fill="white")
    draw.rectangle((173, 7, 313, 18), fill=(13, 16, 26, 240), outline=(230, 240, 255, 255))
    width = round(133 * enemy_life / 1000)
    draw.rectangle((310 - width, 10, 310, 15), fill=(225, 72, 68, 255))
    draw.text((286, 20), "KFM", font=SMALL, fill="white")
    for index in range(3):
        x = 9 + index * 46
        draw.rectangle((x, 226, x + 41, 233), fill=(12, 17, 25, 240), outline=(195, 225, 255, 255))
        if power >= (index + 1) * 1000:
            draw.rectangle((x + 2, 228, x + 39, 231), fill=(65, 178, 255, 255))


def spark(canvas: Image.Image, x: int, y: int, radius: int):
    draw = ImageDraw.Draw(canvas, "RGBA")
    for angle in range(0, 360, 30):
        ex = x + round(math.cos(math.radians(angle)) * radius * 2)
        ey = y + round(math.sin(math.radians(angle)) * radius * 2)
        draw.line((x, y, ex, ey), fill=(120, 225, 255, 235), width=2)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(250, 250, 255, 235))


def main():
    kfm = Sff2(KFM_SFF)
    idle = kfm.image(0, 0)[0]
    attack = [kfm.image(210, i)[0] for i in range(5)]
    hit = kfm.image(5000, 20)[0]
    eida = [load("eida", f"idle_{i}") for i in range(6)]
    eida_power = [load("eida_extra", f"power_{i}") for i in range(4)]
    daemon = [load("daemon", f"daemon_{i}") for i in range(16)]
    frames: list[Image.Image] = []
    durations: list[int] = []

    # Hold Start/Pause to fill the first power bar.
    for i in range(10):
        canvas = background()
        place(canvas, eida_power[(i // 3) % 4], 66, 190)
        place(canvas, idle, 255, 190)
        hud(canvas, power=(i + 1) * 100)
        text_center(canvas, "MANTEN START / PAUSA", 198, (120, 230, 255, 255))
        frames.append(canvas)
        durations.append(95)

    for i in range(6):
        canvas = background()
        place(canvas, eida[(i // 2) % 6], 66, 190)
        place(canvas, idle, 255, 190)
        hud(canvas, power=1000)
        text_center(canvas, "↙  +  RB", 198, (255, 232, 100, 255))
        frames.append(canvas)
        durations.append(95)

    # Exactly two seconds of active guard in the preview.
    for i in range(20):
        canvas = background()
        place(canvas, eida[2], 66, 190)
        daemon_frame = daemon[12 + (i // 3) % 4]
        place(canvas, daemon_frame, 108, 190)
        if i < 12:
            opponent = idle
            opponent_x = 255 - i * 4
        else:
            opponent = attack[min(4, (i - 12) // 2)]
            opponent_x = 205
        place(canvas, opponent, opponent_x, 190)
        hud(canvas, power=0)
        remaining = max(0, 2.0 - i * 0.1)
        text_center(canvas, f"PARRY ACTIVO  {remaining:.1f}s", 38, (120, 230, 255, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        pulse = round(4 * math.sin(i * math.pi / 3))
        draw.arc((76 - pulse, 91 - pulse, 142 + pulse, 195 + pulse), 245, 115, fill=(80, 220, 255, 210), width=3)
        if i == 18:
            spark(canvas, 140, 130, 8)
            text_center(canvas, "PARRY!", 57, (255, 245, 110, 255))
        frames.append(canvas)
        durations.append(100)

    counter_frames = (8, 9, 10, 11, 9, 10, 11, 10, 11, 15)
    for i, daemon_index in enumerate(counter_frames):
        canvas = background()
        place(canvas, eida[3], 66, 190)
        dx = min(214, 110 + i * 13)
        place(canvas, daemon[daemon_index], dx, 190)
        target_x = 230 + max(0, i - 5) * 7
        place(canvas, hit if i >= 3 else attack[4], target_x, 190 - max(0, i - 5) * 3)
        hud(canvas, 860 if i >= 5 else 1000, 0)
        text_center(canvas, "CONTRAATAQUE IMBLOQUEABLE", 38, (255, 226, 95, 255))
        if i in (3, 5):
            spark(canvas, 226, 128, 10 + i)
        frames.append(canvas)
        durations.append(85)

    for i in range(7):
        canvas = background()
        place(canvas, eida[(i // 2) % 6], 66, 190)
        place(canvas, hit, 276, 181)
        hud(canvas, 860, 0)
        if i < 4:
            text_center(canvas, "140 DAMAGE", 47, (255, 226, 95, 255))
        frames.append(canvas)
        durations.append(95)

    paletted = [f.resize((640, 480), Image.Resampling.NEAREST).convert("P", palette=Image.Palette.ADAPTIVE, colors=255) for f in frames]
    paletted[0].save(OUT, save_all=True, append_images=paletted[1:], duration=durations, loop=0, disposal=2)
    print(OUT)


if __name__ == "__main__":
    main()
