#!/usr/bin/env python3
"""Build MUGEN 1.1-compatible SFFv2 and SND archives for Eida."""

from __future__ import annotations

import struct
import json
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
    (8100, 0, ASSETS / "effects/senrigan_logo.png"),
    *sequence(8200, "effects/charm/heart_{index}.png", 6),
    *sequence(8300, "effects/reference/8300_{index}.png", 13),
    *sequence(8400, "effects/reference/8400_{index}.png", 4),
    *sequence(8410, "effects/reference/8410_{index}.png", 14),
    *sequence(8420, "effects/reference/8420_{index}.png", 6),
    *sequence(8000, "cinematic/panel_{index}.png", 4),
    (9000, 0, ASSETS / "portrait/portrait_small.png"),
    # Standard MUGEN portraits: 9000,0 is the 25x25 fight icon and 9000,1
    # is the 120x140 select portrait. Use the same clean face source so the
    # lifebar can never display the 320x240 manga reference at full size.
    (9000, 1, ASSETS / "portrait/portrait_small.png"),
]


def png_to_indexed(
    path: Path,
    target_size: tuple[int, int] | None = None,
    target_height: int | None = None,
) -> tuple[bytes, bytes, int, int, int, int]:
    rgba = Image.open(path).convert("RGBA")
    if target_size is not None:
        rgba = rgba.resize(target_size, Image.Resampling.LANCZOS)
    elif target_height is not None and rgba.height != target_height:
        width = max(1, round(rgba.width * target_height / rgba.height))
        rgba = rgba.resize((width, target_height), Image.Resampling.LANCZOS)
    alpha = rgba.getchannel("A")
    rgb = rgba.convert("RGB")
    quant = rgb.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    source = quant.tobytes()
    mask = alpha.tobytes()
    indices = bytes(0 if a < 128 else value + 1 for value, a in zip(source, mask))
    rgb_palette = quant.getpalette()[: 255 * 3]
    rgb_palette += [0] * (255 * 3 - len(rgb_palette))
    palette = bytearray((0, 0, 0, 0))
    for i in range(255):
        base = i * 3
        palette.extend(rgb_palette[base : base + 3])
        palette.append(255)
    return indices, bytes(palette), rgba.width, rgba.height, rgba.width // 2, max(0, rgba.height - 2)


def build_sff(destination: Path) -> None:
    records = []
    effect_axes = json.loads((ASSETS / 'effects/reference/axes.json').read_text())
    for group, number, path in SPRITES:
        if not path.exists():
            raise FileNotFoundError(path)
        target_size = (25, 25) if (group, number) == (9000, 0) else None
        factor = .68 if group == 1000 else .11 if group == 8400 else 1
        target_height = max(1, round(Image.open(path).height * factor)) if factor != 1 else None
        pixels, palette, width, height, axis_x, axis_y = png_to_indexed(
            path, target_size=target_size, target_height=target_height
        )
        if group in (8000, 9000):
            axis_x = axis_y = 0
        elif group in (8100, 8200):
            axis_x, axis_y = width // 2, height // 2
        elif f'{group},{number}' in effect_axes:
            axis_x, axis_y = (round(v * factor) for v in effect_axes[f'{group},{number}'])
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
        # Non-verbal hit effects selected from the Nezuko reference character
        # supplied by the user. Eida's voice groups remain exclusively Japanese Eida.
        (1, 5, ASSETS / "sound/hit_light.wav"),
        (1, 6, ASSETS / "sound/hit_medium.wav"),
        (1, 7, ASSETS / "sound/hit_launcher.wav"),
        (1, 8, ASSETS / "sound/appear.wav"),
        (1, 9, ASSETS / "sound/guard.wav"),
        (1, 10, ASSETS / "sound/charm_cast.wav"),
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
