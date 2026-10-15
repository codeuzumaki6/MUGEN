#!/usr/bin/env python3
"""Build MUGEN 1.1-compatible SFFv2 and SND archives for Eida."""

from __future__ import annotations

import struct
from pathlib import Path

from PIL import Image


ROOT = Path("/workspace/MUGEN")
CHAR = ROOT / "Eida"
ASSETS = CHAR / "assets"


def sequence(group: int, pattern: str, count: int):
    return [(group, index, ASSETS / pattern.format(index=index)) for index in range(count)]


SPRITES = [
    *sequence(0, "eida/idle_{index}.png", 6),
    *sequence(10, "eida/air_{index}.png", 3),
    *sequence(20, "eida/walk_{index}.png", 8),
    *sequence(40, "eida/low_{index}.png", 2),
    (41, 0, ASSETS / "eida/low_0.png"),
    (42, 0, ASSETS / "eida/low_1.png"),
    (43, 0, ASSETS / "eida/low_1.png"),
    *sequence(44, "eida/hit_{index}.png", 4),
    (47, 0, ASSETS / "eida/air_1.png"),
    *sequence(120, "eida/cast_{index}.png", 3),
    *sequence(140, "eida/hit_{index}.png", 4),
    *sequence(170, "eida/down_{index}.png", 1),
    *sequence(171, "eida/recover_{index}.png", 2),
    *sequence(180, "eida/senrigan_{index}.png", 2),
    *sequence(181, "eida/win_{index}.png", 2),
    *sequence(190, "eida/idle_{index}.png", 3),
    *sequence(200, "eida/punch_{index}.png", 6),
    *sequence(210, "eida/kick_{index}.png", 4),
    *sequence(220, "eida/low_{index}.png", 6),
    *sequence(230, "eida/cast_{index}.png", 3),
    *sequence(600, "eida/air_{index}.png", 10),
    *sequence(1000, "daemon/daemon_{index}.png", 16),
    *sequence(300, "eida_extra/turn_{index}.png", 4),
    *sequence(310, "eida_extra/jump_{index}.png", 4),
    *sequence(320, "eida_extra/land_{index}.png", 4),
    *sequence(330, "eida_extra/power_{index}.png", 4),
    *sequence(8000, "cinematic/panel_{index}.png", 4),
    (9000, 0, ASSETS / "portrait/portrait_small.png"),
    (9000, 1, ASSETS / "portrait/portrait_big.png"),
]


def png_to_indexed(path: Path) -> tuple[bytes, bytes, int, int, int, int]:
    rgba = Image.open(path).convert("RGBA")
    alpha = rgba.getchannel("A")
    rgb = rgba.convert("RGB")
    quant = rgb.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    source = quant.tobytes()
    mask = alpha.tobytes()
    indices = bytes(0 if a < 128 else value + 1 for value, a in zip(source, mask))
    rgb_palette = quant.getpalette()[: 255 * 3]
    palette = bytearray((0, 0, 0, 0))
    for i in range(255):
        base = i * 3
        palette.extend(rgb_palette[base : base + 3])
        palette.append(255)
    return indices, bytes(palette), rgba.width, rgba.height, rgba.width // 2, max(0, rgba.height - 2)


def build_sff(destination: Path) -> None:
    records = []
    for group, number, path in SPRITES:
        if not path.exists():
            raise FileNotFoundError(path)
        pixels, palette, width, height, axis_x, axis_y = png_to_indexed(path)
        if group in (8000, 9000):
            axis_x = axis_y = 0
        records.append((group, number, width, height, axis_x, axis_y, pixels, palette))

    # SFF v2.0.1.0, matching the working Code.sff supplied by the user.
    # Each sprite has its own 256-color RGBA palette and uses raw indexed data
    # (format 0), avoiding the PCX decoding differences of legacy MUGEN builds.
    palette_header_offset = 512
    sprite_header_offset = palette_header_offset + len(records) * 16
    ldata_offset = sprite_header_offset + len(records) * 28

    palette_headers = []
    sprite_headers = []
    data_chunks = []
    data_offset = 0
    for index, (group, number, width, height, axis_x, axis_y, pixels, palette) in enumerate(records):
        palette_offset = data_offset
        data_chunks.append(palette)
        data_offset += len(palette)
        pixel_offset = data_offset
        data_chunks.append(pixels)
        data_offset += len(pixels)

        palette_headers.append(
            struct.pack("<HHHHII", 1, index + 1, 256, 0, palette_offset, len(palette))
        )
        sprite_headers.append(
            struct.pack(
                "<HHHHhhHBBIIHH",
                group,
                number,
                width,
                height,
                axis_x,
                axis_y,
                0,       # no linked sprite
                0,       # raw indexed pixels
                8,       # 8-bit color depth
                pixel_offset,
                len(pixels),
                index,   # palette table index
                0,       # local-data flag
            )
        )

    header = bytearray(512)
    header[:12] = b"ElecbyteSpr\0"
    header[12:16] = bytes((0, 1, 0, 2))
    header[24:28] = bytes((0, 1, 0, 2))
    struct.pack_into(
        "<IIIIIIII",
        header,
        36,
        sprite_header_offset,
        len(records),
        palette_header_offset,
        len(records),
        ldata_offset,
        data_offset,
        ldata_offset + data_offset,
        0,
    )
    comment = b"Eida TBV for Jump Force MUGEN 1.1"
    header[76 : 76 + len(comment)] = comment
    destination.write_bytes(
        bytes(header)
        + b"".join(palette_headers)
        + b"".join(sprite_headers)
        + b"".join(data_chunks)
    )


def build_snd(destination: Path) -> None:
    sounds = [
        (0, 0, ASSETS / "sound/voice_attack.wav"),
        (0, 1, ASSETS / "sound/voice_senrigan.wav"),
        (0, 2, ASSETS / "sound/voice_ultimate.wav"),
        (1, 0, ASSETS / "sound/swing.wav"),
        (1, 1, ASSETS / "sound/hit.wav"),
        (1, 2, ASSETS / "sound/charm.wav"),
        (1, 3, ASSETS / "sound/omnipotence.wav"),
        (1, 4, ASSETS / "sound/charge.wav"),
        # Generic movement/get-up aliases used by the proven Code common-state
        # implementation retained for MUGEN 1.1 compatibility.
        (100, 0, ASSETS / "sound/swing.wav"),
        (142, 0, ASSETS / "sound/swing.wav"),
        (400, 18, ASSETS / "sound/hit.wav"),
        (1180, 5, ASSETS / "sound/swing.wav"),
        (5120, 0, ASSETS / "sound/hit.wav"),
        (5120, 1, ASSETS / "sound/hit.wav"),
    ]
    records = []
    for group, number, path in sounds:
        if not path.exists():
            raise FileNotFoundError(path)
        records.append((group, number, path.read_bytes()))

    offset = 512
    chunks = []
    for index, (group, number, wave) in enumerate(records):
        next_offset = 0 if index == len(records) - 1 else offset + 16 + len(wave)
        chunks.append(struct.pack("<IIii", next_offset, len(wave), group, number) + wave)
        offset = next_offset

    header = bytearray(512)
    header[:12] = b"ElecbyteSnd\0"
    # Match the version fields used by the working Code.snd reference.
    struct.pack_into("<HHII", header, 12, 1, 1, len(records), 512)
    comment = b"Eida TBV Japanese voice and original SFX"
    header[24 : 24 + len(comment)] = comment
    destination.write_bytes(bytes(header) + b"".join(chunks))


if __name__ == "__main__":
    CHAR.mkdir(parents=True, exist_ok=True)
    build_sff(CHAR / "Eida.sff")
    build_snd(CHAR / "Eida.snd")
    print(f"Built {CHAR / 'Eida.sff'} with {len(SPRITES)} sprites")
    print(f"Built {CHAR / 'Eida.snd'}")
