#!/usr/bin/env python3
"""Remove green-screen spill from the supplied Eida sprite crops.

The source sheet is JPEG-like antialiased pixel art over a flat green field.
ImageMagick removes the main field, while this pass removes the green fringe
without touching Eida's cyan/blue hair or repainting the source artwork.
"""

from pathlib import Path

from PIL import Image


SPRITES = Path("/workspace/MUGEN/Eida/assets/eida")


def clean(path: Path) -> None:
    image = Image.open(path).convert("RGBA")
    cleaned = []
    for red, green, blue, alpha in image.getdata():
        # Bright, strongly green pixels are remnants of the source backdrop.
        if alpha and green > 55 and green > red * 1.38 and green > blue * 1.18:
            cleaned.append((0, 0, 0, 0))
        # Very dark fringe belongs to the outline; neutralize its green cast.
        elif alpha and green < 56 and green > red * 1.5 and green > blue * 1.25:
            value = max(red, blue)
            cleaned.append((value, value, value, alpha))
        else:
            cleaned.append((red, green, blue, alpha))
    image.putdata(cleaned)
    image.save(path)


for sprite in sorted(SPRITES.glob("*.png")):
    clean(sprite)

print(f"Cleaned chroma spill from {len(list(SPRITES.glob('*.png')))} Eida sprites")
