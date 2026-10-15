#!/usr/bin/env python3
"""Render the Senrigan observation/counter using the user's emblem."""

from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_combo_preview import KFM_SFF, ROOT, Sff2, background, load, place


OUT = ROOT / "previews/Senrigan_logo_animacion.gif"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = ImageFont.truetype(FONT_PATH, 13) if Path(FONT_PATH).exists() else ImageFont.load_default()
SMALL = ImageFont.truetype(FONT_PATH, 8) if Path(FONT_PATH).exists() else ImageFont.load_default()


def title(canvas: Image.Image, text: str, y: int = 35):
    draw = ImageDraw.Draw(canvas, "RGBA")
    box = draw.textbbox((0, 0), text, font=FONT, stroke_width=1)
    draw.text(((320 - box[2] + box[0]) // 2, y), text, font=FONT, fill=(220, 247, 255, 255), stroke_width=1, stroke_fill=(5, 25, 55, 255))


def hud(canvas: Image.Image, power=0):
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((7, 7, 147, 18), fill=(13, 16, 26, 240), outline=(230, 240, 255, 255))
    draw.rectangle((10, 10, 143, 15), fill=(55, 205, 230, 255))
    draw.text((8, 20), "EIDA", font=SMALL, fill="white")
    draw.rectangle((173, 7, 313, 18), fill=(13, 16, 26, 240), outline=(230, 240, 255, 255))
    draw.rectangle((177, 10, 310, 15), fill=(225, 72, 68, 255))
    draw.text((286, 20), "KFM", font=SMALL, fill="white")
    for index in range(3):
        x = 9 + index * 46
        draw.rectangle((x, 226, x + 41, 233), fill=(12, 17, 25, 240), outline=(195, 225, 255, 255))
        if power >= (index + 1) * 1000:
            draw.rectangle((x + 2, 228, x + 39, 231), fill=(65, 178, 255, 255))


def logo_layer(canvas: Image.Image, logo: Image.Image, size: int, opacity: int):
    sprite = logo.resize((size, size), Image.Resampling.LANCZOS)
    alpha = sprite.getchannel("A").point(lambda value: value * opacity // 255)
    sprite.putalpha(alpha)
    canvas.alpha_composite(sprite, (66 - size // 2, 142 - size // 2))


def main():
    kfm = Sff2(KFM_SFF)
    kfm_idle = kfm.image(0, 0)[0]
    kfm_hit = kfm.image(5000, 20)[0]
    eida_idle = [load("eida", f"idle_{i}") for i in range(6)]
    eida_senrigan = [load("eida", f"senrigan_{i}") for i in range(2)]
    eida_cast = [load("eida", f"cast_{i}") for i in range(3)]
    logo = Image.open(ROOT / "Eida/assets/effects/senrigan_logo.png").convert("RGBA")
    frames: list[Image.Image] = []
    durations: list[int] = []

    # Neutral stance.
    for i in range(8):
        canvas = background()
        place(canvas, eida_idle[(i // 2) % 6], 66, 190)
        place(canvas, kfm_idle, 255, 190)
        hud(canvas, 1000)
        title(canvas, "↙ + RT   SENRIGAN", 198)
        frames.append(canvas)
        durations.append(90)

    # Senrigan opens: the logo pulses behind Eida, never covering her sprite.
    for i in range(22):
        canvas = background()
        pulse = (math.sin(i * math.pi / 5) + 1) / 2
        size = round(92 + 28 * pulse + i * 1.2)
        logo_layer(canvas, logo, size, round(145 + 75 * pulse))
        place(canvas, eida_senrigan[(i // 5) % 2], 66, 190)
        place(canvas, kfm_idle, 255, 190)
        hud(canvas, 0)
        title(canvas, "SENRIGAN")
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rectangle((0, 0, 319, 239), outline=(80, 205, 255, 70 + round(80 * pulse)), width=2)
        frames.append(canvas)
        durations.append(80)

    # Successful observation triggers Eida's own counter; Daemon is reserved
    # for combo attacks and his dedicated parry jutsu.
    for i in range(8):
        canvas = background()
        logo_layer(canvas, logo, 128 + i * 3, max(45, 175 - i * 16))
        place(canvas, eida_cast[min(2, i // 3)], 66, 190)
        place(canvas, kfm_hit if i >= 3 else kfm_idle, 255, 190)
        hud(canvas, 0)
        title(canvas, "CONTRAATAQUE SENRIGAN")
        draw = ImageDraw.Draw(canvas, "RGBA")
        wave_x = 104 + i * 19
        wave_r = 11 + i
        draw.ellipse((wave_x - wave_r, 127 - wave_r, wave_x + wave_r, 127 + wave_r), outline=(80, 220, 255, max(45, 230 - i * 20)), width=3)
        if i in (3, 5):
            radius = 9 + i
            draw.ellipse((245 - radius, 130 - radius, 245 + radius, 130 + radius), fill=(245, 250, 255, 225), outline=(55, 205, 255, 255), width=2)
        frames.append(canvas)
        durations.append(85)

    for i in range(7):
        canvas = background()
        place(canvas, eida_idle[(i // 2) % 6], 66, 190)
        place(canvas, kfm_hit, 255, 190)
        hud(canvas, 0)
        frames.append(canvas)
        durations.append(90)

    paletted = [frame.resize((640, 480), Image.Resampling.NEAREST).convert("P", palette=Image.Palette.ADAPTIVE, colors=255) for frame in frames]
    paletted[0].save(OUT, save_all=True, append_images=paletted[1:], duration=durations, loop=0, disposal=2)
    print(OUT)


if __name__ == "__main__":
    main()
