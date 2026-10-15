#!/usr/bin/env python3
"""Render the physical-X four-hit chain and Daemon launcher."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from make_combo_preview import KFM_SFF, ROOT, Sff2, background, hit_spark, load, place


OUT = ROOT / "previews/Eida_combo_X_launcher.gif"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = ImageFont.truetype(FONT_PATH, 10) if Path(FONT_PATH).exists() else ImageFont.load_default()


def main() -> None:
    kfm = Sff2(KFM_SFF)
    idle_target = kfm.image(0, 0)[0]
    hit_target = [kfm.image(5000, index)[0] for index in (11, 20, 21)]
    eida_idle = [load("eida", f"idle_{i}") for i in range(6)]
    punch = [load("eida", f"punch_{i}") for i in range(6)]
    kick = [load("eida", f"kick_{i}") for i in range(4)]
    cast = [load("eida", f"cast_{i}") for i in range(3)]
    daemon = [load("daemon", f"daemon_{i}") for i in range(16)]

    timeline: list[tuple[str, int, int]] = []
    timeline += [("idle", i % 6, 0) for i in range(8)]
    timeline += [("punch", i, 1 if i in (2, 3) else 0) for i in range(6)]
    timeline += [("reverse", i, 2 if i in (1, 2) else 0) for i in (1, 2, 3, 4)]
    timeline += [("kick", i, 3 if i in (1, 2) else 0) for i in range(4)]
    timeline += [("cast", min(2, i // 2), 0) for i in range(6)]
    timeline += [("daemon", i, 4 if i in (9, 10) else 0) for i in (8, 8, 9, 9, 10, 10, 11, 11)]
    timeline += [("finish", i % 6, 0) for i in range(12)]

    frames: list[Image.Image] = []
    durations: list[int] = []
    target_x = 250
    target_y = 190
    hits = 0
    for frame_no, (kind, index, impact) in enumerate(timeline):
        canvas = background()
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rectangle((8, 8, 146, 17), fill=(20, 20, 25, 235), outline="white")
        draw.rectangle((10, 10, 142, 15), fill=(65, 210, 230, 255))
        draw.text((8, 20), "EIDA", font=FONT, fill="white")
        draw.rectangle((174, 8, 312, 17), fill=(20, 20, 25, 235), outline="white")
        remaining = max(18, 132 - hits * 19)
        draw.rectangle((310 - remaining, 10, 310, 15), fill=(225, 78, 65, 255))
        draw.text((282, 20), "KFM", font=FONT, fill="white")
        draw.text((105, 215), "X  X  X  X", font=FONT, fill=(255, 235, 100, 255))

        if kind == "idle" or kind == "finish":
            eida = eida_idle[index]
        elif kind in ("punch", "reverse"):
            eida = punch[index]
            if kind == "reverse":
                eida = eida.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        elif kind == "kick":
            eida = kick[index]
        else:
            eida = cast[index] if kind == "cast" else eida_idle[2]
        place(canvas, eida, 95, 190)

        if kind == "daemon":
            place(canvas, daemon[index], 185, 190)

        if impact:
            hits = max(hits, impact)
            hit_spark(canvas, target_x - 15, target_y - 58, frame_no % 3, strong=impact == 4)
        if kind == "finish":
            target_x = min(305, target_x + 5)
            target_y = max(116, target_y - 7 if frame_no < len(timeline) - 5 else target_y + 6)
        target_sprite = hit_target[min(2, max(0, hits - 1))] if impact or kind == "finish" else idle_target
        place(canvas, target_sprite, target_x, target_y)

        if hits:
            draw.text((238, 46), f"{hits} HITS", font=FONT, fill=(255, 225, 75, 255), stroke_width=1, stroke_fill=(70, 20, 10, 255))
        if hits == 4:
            draw.text((194, 62), "LAUNCHER", font=FONT, fill=(105, 225, 255, 255), stroke_width=1, stroke_fill=(5, 20, 50, 255))

        frames.append(canvas.resize((640, 480), Image.Resampling.NEAREST).convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
        durations.append(80)

    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)
    print(OUT)


if __name__ == "__main__":
    main()
