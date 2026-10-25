#!/usr/bin/env python3
"""Check the final runtime, evidence and standalone ZIP, optionally public bytes."""
from pathlib import Path
import argparse, hashlib, json, subprocess, urllib.request, zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'DeepaKara'
BASELINE = 'e77970c80b6e8b748f60b48a3f56134f24effd1b'
PREVIOUS = ['Eida','PochitaTrueForm','Mamushi','Shibai','JuraShinju',
            'MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju','DeltaKara','SaradaTBV']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def report(name):
    return json.loads((ROOT / 'previews' / name).read_text())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--commit')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    files = [NAME+'.'+s for s in ['def','cns','cmd','air','sff','snd']] + [NAME+'_common.cns']
    runtime = sha(b''.join((ROOT/NAME/f).read_bytes() for f in files))
    checks = report(NAME+'_engine_checks.json')
    capture = report(NAME+'_capture_checks.json')
    preview = report(NAME+'_preview_checks.json')
    assert all(r['runtime_sha256'] == runtime for r in [checks, capture, preview])
    assert len(checks['cases']) == 120 and all(not c['failures'] for c in checks['cases'])
    assert all(not c['failures'] for c in capture['cases'])
    receiving = report(NAME+'_receiving/'+NAME+'.json')
    assert len(receiving) == 112 and all(c['damage'] > 0 and c['hurt'] and c['recovered'] for c in receiving)
    assert all(c['hits_received'] == 3 for c in receiving if c['attack'] == 'combo')
    dash = report(NAME+'_dash_checks.json')
    assert len(dash) == 8 and all(c['passed'] for c in dash)
    video = ROOT / 'previews' / preview['video']
    assert sha(video.read_bytes()) == preview['sha256']
    package = report(NAME+'_package_checks.json')
    archive = ROOT / package['archive']
    assert archive.stat().st_size == package['bytes'] and sha(archive.read_bytes()) == package['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == {NAME+'/'+f for f in package['files']}
        for f, digest in package['files'].items():
            assert sha((ROOT/NAME/f).read_bytes()) == digest == sha(z.read(NAME+'/'+f)), f
    unchanged = subprocess.run(['git','diff','--quiet',BASELINE,'--']+PREVIOUS, cwd=ROOT)
    assert unchanged.returncode == 0, 'Previous playable character changed'
    source = report(NAME+'_source_checks.json')
    assert source['original_rgba_preserved'] and source['original_frames'] == 134
    result = dict(character=NAME, runtime_sha256=runtime, actual_inputs=120,
                  receiving_probes=112, dash_checks=8, original_frames=134,
                  previous_characters_unchanged_from=BASELINE,
                  archive_sha256=package['sha256'], video_sha256=preview['sha256'])
    if args.write:
        (ROOT/'previews'/f'{NAME}_delivery_checks.json').write_text(json.dumps(result, indent=2)+'\n')
    if args.commit:
        assert subprocess.check_output(['git','rev-parse',args.commit], cwd=ROOT, text=True).strip() == args.commit
        result['public'] = {}
        for local in [archive, video]:
            url = f'https://raw.githubusercontent.com/codeuzumaki6/MUGEN/{args.commit}/{local.relative_to(ROOT).as_posix()}'
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
            assert data == local.read_bytes(), url
            result['public'][local.name] = dict(url=url, bytes=len(data), sha256=sha(data))
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
