#!/usr/bin/env python3
"""Check the user's archive against every imported original Deepa cell."""
from pathlib import Path
import argparse, hashlib, json, plistlib, re, zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source_material/Deepa_original'
CHAR = ROOT / 'DeepaKara'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('archive', type=Path)
    ap.add_argument('video', type=Path)
    args = ap.parse_args()
    preserved = {}
    with zipfile.ZipFile(args.archive) as z:
        assert z.testzip() is None
        for info in z.infolist():
            if info.is_dir():
                continue
            path = SOURCE / info.filename
            assert path.read_bytes() == z.read(info), info.filename
            preserved[info.filename] = sha(path.read_bytes())
    manifest = json.loads((CHAR / 'assets/sprites.json').read_text())
    originals = [p for p in manifest if p['group'] in [28000, 28001]]
    assert len(originals) == 134
    for cell in originals:
        plist = ROOT / cell['source_plist']
        data = plistlib.loads(plist.read_bytes())
        sheet = Image.open(plist.parent / data['metadata']['textureFileName']).convert('RGBA')
        frame = data['frames'][cell['key']]
        x, y, w, h = map(int, re.findall(r'-?\d+', frame['frame']))
        image = sheet.crop((x, y, x+w, y+h))
        if frame.get('rotated'):
            image = image.transpose(Image.Transpose.ROTATE_90)
        imported = Image.open(CHAR / cell['file']).convert('RGBA')
        assert image.size == imported.size and image.tobytes() == imported.tobytes(), cell['key']
        assert sha(image.tobytes()) == cell['rgba_sha256']
        assert not cell['redrawn'] and not cell['ai_generated']
    excluded = json.loads((CHAR / 'assets/excluded_donor_frames.json').read_text())
    keys = json.loads((CHAR / 'assets/keys.json').read_text())
    assert len(excluded) == 16 and not any(k.startswith('KakashiFlog_') for k in keys)
    sounds = json.loads((CHAR / 'assets/sounds.json').read_text())['source_audio']
    assert len(sounds) == 29
    for item in sounds:
        assert sha((ROOT / item['source']).read_bytes()) == item['source_sha256']
    # Every declared original body is anchored inside its own canvas.
    for cell in originals:
        if cell['kind'] == 'body':
            image = Image.open(CHAR / cell['file'])
            x, y = cell['axis']
            assert 0 <= x < image.width and 0 <= y < image.height, cell['key']
    receiving = json.loads((ROOT / 'previews/DeepaKara_receiving/DeepaKara.json').read_text())
    assert len(receiving) == 112
    assert all(c['damage'] > 0 and c['recovered'] for c in receiving)
    idle = [c for c in receiving if c['pose'] == 'idle' and c['face'] == 1 and c['attack'] == 'combo']
    normal, armored = (next(c for c in idle if c['form'] == form) for form in [0, 1])
    assert 0 < armored['damage'] < normal['damage']
    proof = dict(
        archive=dict(name=args.archive.name, bytes=args.archive.stat().st_size, sha256=sha(args.archive.read_bytes())),
        gameplay_reference=dict(name=args.video.name, sha256=sha(args.video.read_bytes())),
        original_files=preserved, original_frames=134, original_audio=29,
        original_rgba_preserved=True, unrelated_frames_excluded=excluded,
        armor_combo_damage=dict(normal=normal['damage'], armored=armored['damage']),
    )
    (ROOT / 'previews/DeepaKara_source_checks.json').write_text(json.dumps(proof, indent=2)+'\n')
    (SOURCE / 'source.json').write_text(json.dumps({k:v for k,v in proof.items() if k != 'armor_combo_damage'}, indent=2)+'\n')
    print(f'PASS: {len(preserved)} source files, 134 unchanged RGBA cells, 29 original audio sources; armor reduces combo damage')

if __name__ == '__main__':
    main()
