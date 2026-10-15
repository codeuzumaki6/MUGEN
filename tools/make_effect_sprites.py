#!/usr/bin/env python3
"""Generate the ranged charm projectile sprites. The aura uses extracted reference effects."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path("/workspace/MUGEN/Eida/assets/effects")


def downsample(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)


def make_heart(frame: int) -> Image.Image:
    scale = 4
    size = 48
    canvas = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    pulse = 1 + (frame % 3) * 0.06
    radius = int(17 * scale * pulse)
    cx = cy = size * scale // 2
    gd.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(255, 45, 190, 150))
    glow = glow.filter(ImageFilter.GaussianBlur(7 * scale))
    canvas.alpha_composite(glow)

    points = []
    for step in range(101):
        t = 2 * math.pi * step / 100
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        points.append((cx + x * scale * pulse, cy - y * scale * pulse + 2 * scale))
    draw = ImageDraw.Draw(canvas)
    draw.polygon(points, fill=(255, 45, 155, 255), outline=(120, 12, 95, 255), width=2 * scale)
    draw.ellipse((cx - 5 * scale, cy - 8 * scale, cx, cy - 3 * scale), fill=(255, 225, 250, 235))

    angle = 2 * math.pi * frame / 6
    for offset in (0, math.pi):
        sx = cx + math.cos(angle + offset) * 20 * scale
        sy = cy + math.sin(angle + offset) * 16 * scale
        r = 2 * scale
        draw.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(255, 210, 250, 230))
    return downsample(canvas, (size, size))


def main() -> None:
    charm_dir = ROOT / "charm"
    charm_dir.mkdir(parents=True, exist_ok=True)
    for frame in range(6):
        make_heart(frame).save(charm_dir / f"heart_{frame}.png")


if __name__ == "__main__":
    main()
