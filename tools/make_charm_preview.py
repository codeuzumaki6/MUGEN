#!/usr/bin/env python3
"""Render the finite-range charm projectile using packaged sprites."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from make_combo_preview import KFM_SFF, ROOT, Sff2, background, load, place


OUT = ROOT / "previews/Eida_encantamiento_proyectil.gif"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = ImageFont.truetype(FONT_PATH, 10) if Path(FONT_PATH).exists() else ImageFont.load_default()


def tint(sprite: Image.Image) -> Image.Image:
    image = sprite.copy()
    overlay = Image.new("RGBA", image.size, (255, 45, 180, 0))
    overlay.putalpha(image.getchannel("A").point(lambda value: value * 90 // 255))
    image.alpha_composite(overlay)
    return image


def main() -> None:
    kfm = Sff2(KFM_SFF)
    target_idle = kfm.image(0, 0)[0]
    target_hit = tint(kfm.image(5000, 20)[0])
    eida_idle = [load("eida", f"idle_{i}") for i in range(6)]
    cast = [load("eida", f"cast_{i}") for i in range(3)]
    hearts = [Image.open(ROOT / "Eida/assets/effects/charm" / f"heart_{i}.png").convert("RGBA") for i in range(6)]
    frames: list[Image.Image] = []
    durations: list[int] = []
    for frame in range(38):
        canvas = background()
        draw = ImageDraw.Draw(canvas, "RGBA")
        connected = frame >= 25
        eida = cast[min(2, max(0, (frame - 5) // 3))] if 5 <= frame < 15 else eida_idle[(frame // 3) % 6]
        place(canvas, eida, 70, 190)
        place(canvas, target_hit if connected else target_idle, 255, 190)
        if 11 <= frame < 25:
            x = 94 + (frame - 11) * 11
            heart = hearts[(frame - 11) % 6]
            canvas.alpha_composite(heart, (x - heart.width // 2, 139 - heart.height // 2))
        if connected:
            for n in range(3):
                heart = hearts[(frame + n * 2) % 6].resize((20, 20), Image.Resampling.LANCZOS)
                canvas.alpha_composite(heart, (238 + n * 12, 92 - (n % 2) * 12))
            draw.text((217, 48), "ENCANTADO", font=FONT, fill=(255, 125, 220, 255), stroke_width=1, stroke_fill=(55, 5, 45, 255))
        draw.text((69, 215), "ABAJO, ATRAS + BOTON", font=FONT, fill=(255, 225, 245, 255))
        if frame < 25:
            draw.text((180, 34), "PROYECTIL CON COLISION", font=FONT, fill=(160, 235, 255, 255))
        frames.append(canvas.resize((640, 480), Image.Resampling.NEAREST).convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
        durations.append(85)
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)
    print(OUT)


if __name__ == "__main__":
    main()
