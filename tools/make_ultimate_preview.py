#!/usr/bin/env python3
"""Render the Omnipotence cinematic preview from the packaged manga panels."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from make_combo_preview import KFM_SFF, ROOT, Sff2, background, load, place


OUT = ROOT / "previews/Omnipotencia_A_Xbox.gif"
PANEL_DIR = ROOT / "Eida/assets/cinematic"
W, H = 320, 240


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SMALL = font(8, True)
MEDIUM = font(13, True)
TITLE = font(21, True)


def centered(draw: ImageDraw.ImageDraw, y: int, text: str, face, fill, stroke=0):
    box = draw.textbbox((0, 0), text, font=face, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=face, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))


def hud(canvas: Image.Image, enemy_life: int = 1000, power: int = 3000):
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((7, 7, 147, 18), fill=(13, 16, 26, 240), outline=(230, 240, 255, 255))
    draw.rectangle((10, 10, 143, 15), fill=(55, 205, 230, 255))
    draw.text((8, 20), "EIDA", font=SMALL, fill="white")
    draw.rectangle((173, 7, 313, 18), fill=(13, 16, 26, 240), outline=(230, 240, 255, 255))
    life_width = round(133 * max(0, enemy_life) / 1000)
    draw.rectangle((310 - life_width, 10, 310, 15), fill=(225, 72, 68, 255))
    draw.text((286, 20), "KFM", font=SMALL, fill="white")
    for index in range(3):
        x = 9 + index * 46
        draw.rectangle((x, 226, x + 41, 233), fill=(12, 17, 25, 240), outline=(195, 225, 255, 255))
        if power >= (index + 1) * 1000:
            draw.rectangle((x + 2, 228, x + 39, 231), fill=(65, 178, 255, 255))


def stage_frame(eida: Image.Image, kfm: Image.Image, enemy_life=1000, power=3000) -> Image.Image:
    canvas = background()
    place(canvas, eida, 66, 190)
    place(canvas, kfm, 257, 190)
    hud(canvas, enemy_life, power)
    return canvas


def button_prompt(canvas: Image.Image, pulse: float):
    draw = ImageDraw.Draw(canvas, "RGBA")
    radius = round(12 + pulse * 2)
    draw.ellipse((160 - radius, 202 - radius, 160 + radius, 202 + radius), fill=(42, 178, 78, 245), outline=(225, 255, 230, 255), width=2)
    box = draw.textbbox((0, 0), "A", font=MEDIUM)
    draw.text((160 - (box[2] - box[0]) // 2, 194), "A", font=MEDIUM, fill="white", stroke_width=1, stroke_fill=(10, 65, 24, 255))
    centered(draw, 174, "PULSA A: OMNIPOTENCIA", SMALL, (255, 255, 255, 255), 1)


def zoom_panel(panel: Image.Image, zoom: float, center: tuple[float, float]) -> Image.Image:
    crop_w = W / zoom
    crop_h = H / zoom
    cx, cy = center
    left = max(0, min(W - crop_w, cx - crop_w / 2))
    top = max(0, min(H - crop_h, cy - crop_h / 2))
    return panel.crop((round(left), round(top), round(left + crop_w), round(top + crop_h))).resize((W, H), Image.Resampling.LANCZOS).convert("RGBA")


def cinematic_frame(panel: Image.Image, progress: float, panel_no: int) -> Image.Image:
    centers = ((160, 125), (174, 116), (150, 128), (174, 108))
    canvas = zoom_panel(panel, 1.0 + progress * (0.13 if panel_no != 3 else 0.2), centers[panel_no])
    canvas = ImageEnhance.Contrast(canvas).enhance(1.05)
    overlay = Image.new("RGBA", (W, H), (25, 25, 80, round(28 + 28 * math.sin(progress * math.pi))))
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas, "RGBA")
    # Soft edge flashes keep the transition readable without covering the art.
    if progress < 0.14:
        alpha = round(210 * (1 - progress / 0.14))
        draw.rectangle((0, 0, W, H), fill=(235, 245, 255, alpha))
    draw.rectangle((0, 0, W - 1, H - 1), outline=(155, 190, 255, 220), width=2)
    centered(draw, 214, "ALTERACION DE RECUERDOS", SMALL, (235, 242, 255, 235), 1)
    return canvas


def main():
    kfm_sff = Sff2(KFM_SFF)
    kfm_idle = kfm_sff.image(0, 0)[0]
    kfm_hit = kfm_sff.image(5000, 20)[0]
    eida_idle = [load("eida", f"idle_{i}") for i in range(6)]
    eida_power = [load("eida_extra", f"power_{i}") for i in range(4)]
    panels = [Image.open(PANEL_DIR / f"panel_{i}.png").convert("RGBA") for i in range(4)]
    frames: list[Image.Image] = []
    durations: list[int] = []

    # Ready: full power and the physical Xbox A prompt.
    for i in range(12):
        canvas = stage_frame(eida_idle[(i // 2) % 6], kfm_idle)
        button_prompt(canvas, (math.sin(i * math.pi / 3) + 1) / 2)
        frames.append(canvas)
        durations.append(85)

    # Activation: power is consumed, Eida casts and the super pause darkens the fight.
    for i in range(10):
        canvas = stage_frame(eida_power[min(3, i // 3)], kfm_idle, power=max(0, 3000 - (i + 1) * 300))
        dark = Image.new("RGBA", (W, H), (2, 5, 25, 95 + i * 10))
        canvas = Image.alpha_composite(canvas, dark)
        draw = ImageDraw.Draw(canvas, "RGBA")
        for ring in range(3):
            radius = 15 + ring * 12 + i * 2
            draw.ellipse((66 - radius, 142 - radius, 66 + radius, 142 + radius), outline=(75, 200, 255, max(20, 190 - ring * 45)), width=2)
        centered(draw, 46, "OMNIPOTENCIA", TITLE, (225, 240, 255, 255), 2)
        frames.append(canvas)
        durations.append(75)

    # Four original manga panels, cropped and moved as allowed for the cinematic.
    for panel_no, panel in enumerate(panels):
        count = 13 if panel_no in (1, 3) else 11
        for i in range(count):
            frames.append(cinematic_frame(panel, i / (count - 1), panel_no))
            durations.append(95)

    # White memory flash, damage and release.
    for i in range(4):
        alpha = 255 - i * 48
        canvas = Image.new("RGBA", (W, H), (230, 240, 255, alpha))
        draw = ImageDraw.Draw(canvas, "RGBA")
        centered(draw, 103, "OMNIPOTENCIA", TITLE, (15, 25, 60, 255), 1)
        frames.append(canvas)
        durations.append(70)
    for i in range(10):
        enemy_life = 1000 - round(350 * min(1, (i + 1) / 5))
        canvas = stage_frame(eida_power[3] if i < 4 else eida_idle[(i - 4) % 6], kfm_hit, enemy_life, 0)
        draw = ImageDraw.Draw(canvas, "RGBA")
        if i < 6:
            radius = 28 + i * 6
            draw.ellipse((252 - radius, 137 - radius, 252 + radius, 137 + radius), outline=(175, 210, 255, max(25, 230 - i * 35)), width=3)
            centered(draw, 48, "350 DAMAGE", MEDIUM, (255, 226, 95, 255), 2)
        frames.append(canvas)
        durations.append(90)

    paletted = [frame.resize((640, 480), Image.Resampling.NEAREST).convert("P", palette=Image.Palette.ADAPTIVE, colors=255) for frame in frames]
    paletted[0].save(OUT, save_all=True, append_images=paletted[1:], duration=durations, loop=0, disposal=2)
    print(OUT)


if __name__ == "__main__":
    main()
