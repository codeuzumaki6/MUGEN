#!/usr/bin/env python3
"""Remove green-screen spill from the supplied Eida sprite crops.

The source sheet is JPEG-like antialiased pixel art over a flat green field.
ImageMagick removes the main field, while this pass removes the green fringe
without touching Eida's cyan/blue hair or repainting the source artwork.
"""

from pathlib import Path
from collections import deque

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
    width, height = image.size
    pixels = image.load()
    unseen = {(x, y) for y in range(height) for x in range(width) if pixels[x, y][3]}
    components: list[list[tuple[int, int]]] = []
    while unseen:
        start = unseen.pop()
        queue = deque((start,))
        component = [start]
        while queue:
            x, y = queue.popleft()
            for ny in range(max(0, y - 1), min(height, y + 2)):
                for nx in range(max(0, x - 1), min(width, x + 2)):
                    point = (nx, ny)
                    if point in unseen:
                        unseen.remove(point)
                        queue.append(point)
                        component.append(point)
        components.append(component)

    if components:
        components.sort(key=len, reverse=True)
        main = components[0]
        left = min(x for x, _ in main)
        top = min(y for _, y in main)
        right = max(x for x, _ in main)
        bottom = max(y for _, y in main)
        keep = set(main)
        for component in components[1:]:
            c_left = min(x for x, _ in component)
            c_top = min(y for _, y in component)
            c_right = max(x for x, _ in component)
            c_bottom = max(y for _, y in component)
            if (
                len(component) >= 2
                and c_left >= left - 3
                and c_right <= right + 3
                and c_top >= top - 3
                and c_bottom <= bottom + 3
            ):
                keep.update(component)
        for y in range(height):
            for x in range(width):
                if pixels[x, y][3] and (x, y) not in keep:
                    pixels[x, y] = (0, 0, 0, 0)

    bbox = image.getbbox()
    if bbox:
        trimmed = image.crop(bbox)
        image = Image.new("RGBA", (trimmed.width + 4, trimmed.height + 4))
        image.alpha_composite(trimmed, (2, 2))
    image.save(path)


for sprite in sorted(SPRITES.glob("*.png")):
    clean(sprite)

print(f"Cleaned chroma spill from {len(list(SPRITES.glob('*.png')))} Eida sprites")
