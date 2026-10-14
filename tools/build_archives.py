#!/usr/bin/env python3
"""Build MUGEN 1.1-compatible SFFv1 and SNDv1 archives for Eida."""

from __future__ import annotations

import io
import struct
import tempfile
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
    *sequence(180, "eida/senrigan_{index}.png", 2),
    *sequence(190, "eida/idle_{index}.png", 3),
    *sequence(200, "eida/punch_{index}.png", 6),
    *sequence(210, "eida/kick_{index}.png", 4),
    *sequence(220, "eida/low_{index}.png", 6),
    *sequence(230, "eida/cast_{index}.png", 3),
    *sequence(600, "eida/air_{index}.png", 10),
    *sequence(1000, "daemon/daemon_{index}.png", 16),
    *sequence(8000, "cinematic/panel_{index}.png", 4),
    (9000, 0, ASSETS / "portrait/portrait_small.png"),
    (9000, 1, ASSETS / "portrait/portrait_big.png"),
]


def png_to_pcx(path: Path) -> tuple[bytes, int, int]:
    rgba = Image.open(path).convert("RGBA")
    alpha = rgba.getchannel("A")
    rgb = rgba.convert("RGB")
    quant = rgb.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    source = quant.tobytes()
    mask = alpha.tobytes()
    indices = bytes(0 if a < 128 else value + 1 for value, a in zip(source, mask))
    pal = quant.getpalette()[: 255 * 3]
    palette = [0, 0, 0] + pal
    palette.extend([0] * (768 - len(palette)))
    indexed = Image.frombytes("P", rgba.size, indices)
    indexed.putpalette(palette)
    stream = io.BytesIO()
    indexed.save(stream, format="PCX")
    return stream.getvalue(), rgba.width // 2, max(0, rgba.height - 2)


def build_sff(destination: Path) -> None:
    records = []
    for group, number, path in SPRITES:
        if not path.exists():
            raise FileNotFoundError(path)
        pcx, axis_x, axis_y = png_to_pcx(path)
        if group in (8000, 9000):
            axis_x = axis_y = 0
        records.append((group, number, axis_x, axis_y, pcx))

    offset = 512
    chunks = []
    for index, (group, number, axis_x, axis_y, pcx) in enumerate(records):
        next_offset = 0 if index == len(records) - 1 else offset + 32 + len(pcx)
        header = struct.pack(
            "<IIhhHHHBB12s",
            next_offset,
            len(pcx),
            axis_x,
            axis_y,
            group,
            number,
            0,
            0,
            0,
            b"\0" * 12,
        )
        chunks.append(header + pcx)
        offset = next_offset

    groups = len({group for group, *_ in records})
    header = bytearray(512)
    header[:12] = b"ElecbyteSpr\0"
    # SFF v1 stores the version as four individual bytes (high to low), not
    # as a little-endian integer.  Ikemen accepts the reversed form, while
    # Elecbyte MUGEN 1.1 can abort while loading it.
    header[12:16] = bytes((1, 0, 0, 0))
    struct.pack_into("<IIII", header, 16, groups, len(records), 512, 32)
    header[32] = 0
    comment = b"Eida TBV for Jump Force MUGEN 1.1"
    header[36 : 36 + len(comment)] = comment
    destination.write_bytes(bytes(header) + b"".join(chunks))


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
    # As with SFF, SND's version is four literal bytes.  Writing two uint16
    # values reverses each pair and produces an invalid legacy header.
    header[12:16] = bytes((1, 0, 0, 0))
    struct.pack_into("<II", header, 16, len(records), 512)
    comment = b"Eida TBV Japanese voice and original SFX"
    header[24 : 24 + len(comment)] = comment
    destination.write_bytes(bytes(header) + b"".join(chunks))


if __name__ == "__main__":
    CHAR.mkdir(parents=True, exist_ok=True)
    build_sff(CHAR / "Eida.sff")
    build_snd(CHAR / "Eida.snd")
    print(f"Built {CHAR / 'Eida.sff'} with {len(SPRITES)} sprites")
    print(f"Built {CHAR / 'Eida.snd'}")
