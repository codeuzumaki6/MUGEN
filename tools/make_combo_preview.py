#!/usr/bin/env python3
"""Render an animated combo preview from the exact packaged sprites."""

from __future__ import annotations

import math
import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/workspace/MUGEN")
KFM_SFF = Path("/tmp/ikemen-nightly/chars/kfm/kfm.sff")


def lz5_decode(data: bytes, output_size: int) -> bytes:
    if not data:
        return data
    out = bytearray(output_size)
    i = j = cts = rb = rbc = 0
    control = data[i]
    i += 1
    while j < output_size:
        value = data[i]
        i += 1
        if control & (1 << cts):
            if value & 0x3F == 0:
                distance = ((value << 2) | data[i]) + 1
                i += 1
                count = data[i] + 2
                i += 1
            else:
                rb |= (value & 0xC0) >> rbc
                rbc += 2
                count = value & 0x3F
                if rbc < 8:
                    distance = data[i] + 1
                    i += 1
                else:
                    distance = rb + 1
                    rb = rbc = 0
            while count >= 0 and j < output_size:
                out[j] = out[j - distance]
                j += 1
                count -= 1
        else:
            if value & 0xE0 == 0:
                count = data[i] + 8
                i += 1
                color = value
            else:
                count = value >> 5
                color = value & 0x1F
            for _ in range(count):
                if j < output_size:
                    out[j] = color
                    j += 1
        cts += 1
        if cts >= 8:
            control = data[i]
            i += 1
            cts = 0
    return bytes(out)


class Sff2:
    def __init__(self, path: Path):
        self.data = path.read_bytes()
        (
            self.sprite_headers,
            self.sprite_count,
            self.palette_headers,
            self.palette_count,
            self.ldata_offset,
            _,
            self.tdata_offset,
            _,
        ) = struct.unpack_from("<IIIIIIII", self.data, 36)
        self.sprites = {}
        for index in range(self.sprite_count):
            values = struct.unpack_from(
                "<HHHHhhHBBIIHH", self.data, self.sprite_headers + index * 28
            )
            self.sprites[(values[0], values[1])] = values

    def palette(self, index: int) -> list[tuple[int, int, int, int]]:
        group, number, colors, link, offset, size = struct.unpack_from(
            "<HHHHII", self.data, self.palette_headers + index * 16
        )
        if size == 0:
            return self.palette(link)
        raw = self.data[self.ldata_offset + offset : self.ldata_offset + offset + size]
        palette = [tuple(raw[i : i + 4]) for i in range(0, len(raw), 4)]
        palette.extend([(0, 0, 0, 0)] * (256 - len(palette)))
        return palette

    def image(self, group: int, number: int) -> tuple[Image.Image, tuple[int, int]]:
        values = self.sprites[(group, number)]
        _, _, width, height, axis_x, axis_y, link, fmt, depth, offset, size, pal_index, flags = values
        block = self.tdata_offset if flags & 1 else self.ldata_offset
        raw = self.data[block + offset : block + offset + size]
        if fmt == 4:
            pixels = lz5_decode(raw[4:], width * height)
        elif fmt == 0:
            pixels = raw
        else:
            raise ValueError(f"Unsupported preview sprite format {fmt}")
        palette = self.palette(pal_index)
        rgba = bytearray()
        for pixel in pixels:
            rgba.extend(palette[pixel])
        return Image.frombytes("RGBA", (width, height), bytes(rgba)), (axis_x, axis_y)


def place(canvas: Image.Image, sprite: Image.Image, origin_x: int, ground_y: int, alpha: int = 255):
    if alpha != 255:
        sprite = sprite.copy()
        channel = sprite.getchannel("A").point(lambda value: value * alpha // 255)
        sprite.putalpha(channel)
    canvas.alpha_composite(sprite, (origin_x - sprite.width // 2, ground_y - sprite.height + 2))


def hit_spark(canvas: Image.Image, x: int, y: int, phase: int, strong: bool = False):
    draw = ImageDraw.Draw(canvas)
    radius = (10 if strong else 7) + phase * 2
    color = (255, 245, 120, max(0, 255 - phase * 55))
    for angle in range(0, 360, 45):
        length = radius + (8 if strong else 4)
        ex = x + int(math.cos(math.radians(angle)) * length)
        ey = y + int(math.sin(math.radians(angle)) * length)
        draw.line((x, y, ex, ey), fill=color, width=2)
    draw.ellipse((x - radius // 2, y - radius // 2, x + radius // 2, y + radius // 2), fill=(255, 110, 45, 230))


def background() -> Image.Image:
    image = Image.new("RGBA", (320, 240), (0, 0, 0, 255))
    draw = ImageDraw.Draw(image)
    for y in range(190):
        t = y / 190
        draw.line((0, y, 319, y), fill=(int(26 + 30 * t), int(49 + 37 * t), int(88 + 48 * t), 255))
    draw.ellipse((18, 18, 102, 102), fill=(230, 235, 255, 45))
    draw.rectangle((0, 188, 319, 239), fill=(35, 40, 52, 255))
    draw.rectangle((0, 188, 319, 192), fill=(99, 113, 135, 255))
    for x in range(0, 320, 32):
        draw.line((x, 193, x - 25, 239), fill=(47, 54, 68, 255))
    draw.line((0, 218, 319, 218), fill=(47, 54, 68, 255))
    return image


def load(folder: str, name: str) -> Image.Image:
    return Image.open(ROOT / "Eida/assets" / folder / f"{name}.png").convert("RGBA")


def main():
    kfm = Sff2(KFM_SFF)
    kfm_idle = [kfm.image(0, i)[0] for i in range(6)]
    # These three reactions decode cleanly from KFM's compressed SFF and give
    # the target a readable light/medium/heavy hit progression.
    kfm_hit = [kfm.image(5000, i)[0] for i in (11, 20, 21)]
    eida_idle = [load("eida", f"idle_{i}") for i in range(6)]
    eida_cast = [load("eida", f"cast_{i}") for i in range(3)]
    charm = load("eida_extra", "power_0")
    daemon = [load("daemon", f"daemon_{i}") for i in range(16)]
    font = ImageFont.load_default()

    sequence = []
    sequence += [("idle", i % 6, None, 0, False) for i in range(10)]
    sequence += [("cast", i, None, 0, False) for i in (0, 0, 1, 1, 2, 2)]
    sequence += [("charm", 0, None, 0, False)] * 3
    sequence += [("idle", 2, i, n, False) for n, i in enumerate((0, 4, 5, 6, 7))]
    sequence += [("idle", 3, i, n, False) for n, i in enumerate((5, 6, 7, 8, 5, 6, 7, 8), 5)]
    sequence += [("idle", 4, i, n, True) for n, i in enumerate((9, 10, 11, 10, 9, 10), 13)]
    sequence += [("idle", 5, i, n, n >= 21) for n, i in enumerate((12, 13, 14, 15), 19)]
    sequence += [("idle", i % 6, None, 0, False) for i in range(8)]

    frames = []
    durations = []
    hits = 0
    for frame_no, (emode, eindex, dindex, attack_step, strong) in enumerate(sequence):
        canvas = background()
        draw = ImageDraw.Draw(canvas)

        # HUD
        draw.rectangle((8, 8, 146, 17), fill=(20, 20, 25, 235), outline=(225, 225, 235, 255))
        draw.rectangle((10, 10, 142, 15), fill=(65, 210, 230, 255))
        draw.text((8, 20), "EIDA", font=font, fill="white")
        draw.rectangle((174, 8, 312, 17), fill=(20, 20, 25, 235), outline=(225, 225, 235, 255))
        remaining = max(22, 132 - hits * 13)
        draw.rectangle((310 - remaining, 10, 310, 15), fill=(225, 78, 65, 255))
        draw.text((280, 20), "KFM", font=font, fill="white")

        eida_sprite = eida_idle[eindex] if emode == "idle" else eida_cast[eindex] if emode == "cast" else charm
        place(canvas, eida_sprite, 66, 190)

        target = kfm_idle[(frame_no // 2) % len(kfm_idle)]
        if dindex is not None and attack_step >= 7:
            target = kfm_hit[min(2, attack_step % 3)]
        place(canvas, target, 260 + (2 if attack_step % 2 else 0), 190)

        if emode in {"cast", "charm"}:
            aura = 9 + frame_no % 5
            draw.ellipse((66 - aura, 114 - aura, 66 + aura, 114 + aura), outline=(80, 225, 255, 170), width=2)

        if dindex is not None:
            daemon_x = min(230, 92 + attack_step * 8)
            opacity = 255 if dindex != 15 else 120
            if attack_step > 4:
                ghost = daemon[dindex].copy()
                place(canvas, ghost, daemon_x - 8, 190, 70)
            place(canvas, daemon[dindex], daemon_x, 190, opacity)
            if attack_step in (7, 9, 11, 14, 16, 21):
                hits += 1
                hit_spark(canvas, 247, 132 if not strong else 121, attack_step % 3, strong)

        if hits:
            draw.text((238, 52), f"{hits} HITS", font=font, fill=(255, 232, 85, 255), stroke_width=1, stroke_fill=(70, 20, 10, 255))

        if frame_no < 3:
            draw.text((101, 218), "DAEMON: COMBO RAPIDO", font=font, fill=(230, 235, 255, 255))

        frames.append(canvas.resize((640, 480), Image.Resampling.NEAREST).convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
        durations.append(85 if dindex is not None else 100)

    output = ROOT / "previews/Eida_combo_Daemon.gif"
    frames[0].save(output, save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)
    print(output)


if __name__ == "__main__":
    main()
