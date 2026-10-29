#!/usr/bin/env python3
"""Check the packed wind with standard MUGEN AIR blending, without extensions."""
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

from boruto_source import ROOT, read_sff

NAME = 'BorutoKarmaJogan'
CHAR = ROOT / NAME


def main():
    animations = {}
    current = None
    for line in (CHAR / (NAME + '.air')).read_text().splitlines():
        match = re.match(r'\[Begin Action (\d+)\]', line, re.I)
        if match:
            current = int(match[1])
            animations[current] = []
        elif re.match(r'\s*\d+,\s*\d+,', line):
            animations[current].append([s.strip() for s in line.split(',')])

    sff = read_sff(CHAR / (NAME + '.sff'))
    manifest = json.loads((CHAR / 'assets/sprites.json').read_text())
    by_id = {(r['group'], r['number']): r for r in manifest}
    frames = []
    for action in [8815, 8816, 8817]:
        for fields in animations[action]:
            assert len(fields) >= 7 and fields[6].upper() == 'A', (
                action, fields, 'Wind must use MUGEN AIR additive blending')
            key = tuple(map(int, fields[:2]))
            w, h, _, _, pixels, palette = sff[key]
            rgb = np.frombuffer(palette, dtype=np.uint8).reshape(256, 4)[
                np.frombuffer(pixels, dtype=np.uint8).reshape(h, w), :3]
            assert rgb.max() >= 60, (key, 'Wind became invisible')
            # Under AIR A, black in a premultiplied sprite adds zero instead
            # of covering the stage. Test both light and dark stage colours.
            for background in [np.array([12, 25, 40]), np.array([185, 205, 220])]:
                blended = np.minimum(255, rgb.astype(np.int16) + background)
                assert np.all(blended >= background), (key, 'Stage darkened')
            record = by_id[key]
            image = Image.open(CHAR / record['file']).convert('RGBA')
            assert hashlib.sha256(image.tobytes()).hexdigest() == record['rgba_sha256']
            frames.append(dict(action=action, sprite=list(key), key=record['key'],
                               air_additive=True, light_and_dark_backgrounds=True))

    borders = []
    for record in manifest:
        if not record['key'].startswith('AnginRibut_'):
            continue
        w, h, _, _, pixels, palette = sff[record['group'], record['number']]
        rgb = np.frombuffer(palette, dtype=np.uint8).reshape(256, 4)[
            np.frombuffer(pixels, dtype=np.uint8).reshape(h, w), :3]
        outer = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
        assert outer.max() <= 2, (record['key'], 'Visible rectangular canvas edge')
        borders.append(dict(key=record['key'], maximum_canvas_edge_rgb=int(outer.max())))
    assert len(frames) == 20 and len(borders) == 9
    cns = (CHAR / (NAME + '.cns')).read_text()
    for body in re.split(r'(?im)^\[State ', cns)[1:]:
        if re.search(r'(?im)^type\s*=\s*Explod\s*$', body) and re.search(
                r'(?im)^anim\s*=\s*881[67]\s*$', body):
            assert not re.search(r'(?im)^trans\s*=', body), 'CNS extension masks missing AIR blend'
    files = [NAME + '.' + s for s in ['def', 'cns', 'cmd', 'air', 'sff', 'snd']] + [NAME + '_common.cns']
    proof = dict(runtime_sha256=hashlib.sha256(b''.join((CHAR / f).read_bytes() for f in files)).hexdigest(),
                 standard_air_actions=[8815, 8816, 8817], additive_frames=frames,
                 feathered_canvas_frames=borders, original_rgba_preserved=True,
                 method='Packed SFF + standard MUGEN AIR A; software blend on light and dark backgrounds',
                 native_engine_validation='BorutoKarmaJogan_original_kit_checks.json')
    (ROOT / 'previews' / (NAME + '_uzuhiko_rendering_checks.json')).write_text(json.dumps(proof, indent=2) + '\n')
    print('PASS: 20 wind/tornado frames use standard AIR blending; nine canvases have invisible edges')


if __name__ == '__main__':
    main()
