#!/usr/bin/env python3
"""Render Eida's timed Awakening state from the packaged sprites."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from make_combo_preview import KFM_SFF, ROOT, Sff2, background, load, place


OUT = ROOT / "previews/Eida_Despertar_Start.gif"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = ImageFont.truetype(FONT_PATH, 13) if Path(FONT_PATH).exists() else ImageFont.load_default()
SMALL = ImageFont.truetype(FONT_PATH, 8) if Path(FONT_PATH).exists() else ImageFont.load_default()


def center(canvas: Image.Image, text: str, y: int, color=(255, 255, 255, 255), size="normal"):
    face = FONT if size == "normal" else SMALL
    draw = ImageDraw.Draw(canvas, "RGBA")
    box = draw.textbbox((0, 0), text, font=face, stroke_width=1)
    draw.text(((320 - box[2] + box[0]) // 2, y), text, font=face, fill=color, stroke_width=1, stroke_fill=(5, 12, 32, 255))


def hud(canvas: Image.Image, enemy_life=1000, power=0, awakened=0.0):
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((7, 7, 147, 18), fill=(13, 16, 26, 240), outline=(230, 240, 255, 255))
    draw.rectangle((10, 10, 143, 15), fill=(55, 205, 230, 255))
    draw.text((8, 20), "EIDA", font=SMALL, fill="white")
    draw.rectangle((173, 7, 313, 18), fill=(13, 16, 26, 240), outline=(230, 240, 255, 255))
    life_w = round(133 * enemy_life / 1000)
    draw.rectangle((310 - life_w, 10, 310, 15), fill=(225, 72, 68, 255))
    draw.text((286, 20), "KFM", font=SMALL, fill="white")
    for index in range(3):
        x = 9 + index * 46
        draw.rectangle((x, 226, x + 41, 233), fill=(12, 17, 25, 240), outline=(195, 225, 255, 255))
        if power >= (index + 1) * 1000:
            draw.rectangle((x + 2, 228, x + 39, 231), fill=(65, 178, 255, 255))
    if awakened > 0:
        draw.rectangle((174, 226, 312, 233), fill=(12, 17, 25, 240), outline=(195, 225, 255, 255))
        draw.rectangle((176, 228, 176 + round(134 * awakened), 231), fill=(80, 220, 255, 255))
        draw.text((174, 214), "DESPERTAR", font=SMALL, fill=(205, 245, 255, 255))


def logo_behind(canvas: Image.Image, logo: Image.Image, size: int, opacity: int):
    effect = logo.resize((size, size), Image.Resampling.LANCZOS)
    effect.putalpha(effect.getchannel("A").point(lambda a: a * opacity // 255))
    canvas.alpha_composite(effect, (66 - size // 2, 140 - size // 2))


def main():
    kfm = Sff2(KFM_SFF)
    kfm_idle = kfm.image(0, 0)[0]
    kfm_hit = kfm.image(5000, 20)[0]
    normal = [load("eida", f"idle_{i}") for i in range(6)]
    charge = [load("eida_extra", f"power_{i}") for i in range(4)]
    awakened = [Image.open(ROOT / "Eida/assets/eida_awaken" / f"awaken_{i:02d}.png").convert("RGBA") for i in range(16)]
    logo = Image.open(ROOT / "Eida/assets/effects/senrigan_logo.png").convert("RGBA")
    frames: list[Image.Image] = []
    durations: list[int] = []

    # Fill all three bars by holding Start/Pause.
    for i in range(15):
        canvas = background()
        place(canvas, charge[(i // 4) % 4], 66, 190)
        place(canvas, kfm_idle, 255, 190)
        hud(canvas, power=min(3000, (i + 1) * 200))
        center(canvas, "MANTEN START / PAUSA", 196, (125, 230, 255, 255), "small")
        frames.append(canvas)
        durations.append(80)

    # Release and press Start once at maximum power.
    for i in range(5):
        canvas = background()
        place(canvas, normal[(i // 2) % 6], 66, 190)
        place(canvas, kfm_idle, 255, 190)
        hud(canvas, power=3000)
        center(canvas, "PULSA START: DESPERTAR", 194, (255, 232, 95, 255))
        frames.append(canvas)
        durations.append(90)

    # Four transformation keyframes, with Eida always in front of the emblem.
    for i in range(12):
        idx = min(3, i // 3)
        canvas = background()
        dark = Image.new("RGBA", (320, 240), (2, 7, 28, 105 + i * 5))
        canvas = Image.alpha_composite(canvas, dark)
        logo_behind(canvas, logo, 110 + i * 4, 180)
        place(canvas, awakened[idx], 66, 190)
        place(canvas, kfm_idle, 255, 190)
        hud(canvas, power=max(0, 3000 - (idx + 1) * 750))
        center(canvas, "DESPERTAR DE EIDA", 40, (220, 247, 255, 255))
        frames.append(canvas)
        durations.append(80)

    # Flowing awakened stance.
    for i in range(12):
        canvas = background()
        place(canvas, awakened[4 + (i // 3) % 4], 66, 190)
        place(canvas, kfm_idle, 255, 190)
        hud(canvas, power=0, awakened=1 - i / 180)
        center(canvas, "ATAQUE +25%   DEFENSA +15%", 39, (170, 235, 255, 255), "small")
        frames.append(canvas)
        durations.append(85)

    # Burst movement into Eida's awakened strike.
    for i in range(8):
        canvas = background()
        idx = 8 + min(3, i // 2)
        place(canvas, awakened[idx], 66 + i * 14, 190)
        place(canvas, kfm_idle, 255, 190)
        hud(canvas, power=0, awakened=.92)
        frames.append(canvas)
        durations.append(70)
    for i in range(10):
        canvas = background()
        idx = 12 + min(3, i // 3)
        place(canvas, awakened[idx], 166, 190)
        place(canvas, kfm_hit if i >= 6 else kfm_idle, 257, 190)
        hud(canvas, enemy_life=915 if i >= 6 else 1000, power=0, awakened=.88)
        if i in (6, 7):
            draw = ImageDraw.Draw(canvas, "RGBA")
            r = 14 + (i - 6) * 8
            draw.ellipse((241 - r, 128 - r, 241 + r, 128 + r), fill=(225, 250, 255, 215), outline=(65, 215, 255, 255), width=3)
        frames.append(canvas)
        durations.append(80)

    for i in range(8):
        canvas = background()
        place(canvas, awakened[4 + (i // 2) % 4], 66, 190)
        place(canvas, kfm_hit, 273, 185)
        hud(canvas, enemy_life=915, power=0, awakened=.84)
        frames.append(canvas)
        durations.append(90)

    paletted = [f.resize((640, 480), Image.Resampling.NEAREST).convert("P", palette=Image.Palette.ADAPTIVE, colors=255) for f in frames]
    paletted[0].save(OUT, save_all=True, append_images=paletted[1:], duration=durations, loop=0, disposal=2)
    print(OUT)


if __name__ == "__main__":
    main()
