#!/usr/bin/env python3
"""Prove this revision only changes the victory body/prop presentation."""
from pathlib import Path
import hashlib,json,re,subprocess,tempfile
from make_combo_preview import Sff2

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'JuraShinju';OUT=ROOT/'previews'
PREVIOUS='7bdf90b35e744483b8c7b6c784036a126ad45d98'
NAMES=['JuraShinju.def','JuraShinju.sff','JuraShinju.snd','JuraShinju.air','JuraShinju.cns','JuraShinju.cmd','JuraShinju_common.cns']
def sha(data):return hashlib.sha256(data).hexdigest()
def omit(text,kind,numbers):
    for n in numbers:text=re.sub(rf'(?ims)^\[{kind} {n}\].*?(?=^\[{kind}|\Z)','',text)
    return '\n'.join(line.rstrip() for line in text.splitlines() if line.strip())
old={n:subprocess.check_output(['git','show',f'{PREVIOUS}:JuraShinju/{n}'],cwd=ROOT) for n in NAMES}
current={n:(CHAR/n).read_bytes() for n in NAMES}
for n in ['JuraShinju.def','JuraShinju.snd','JuraShinju.cmd','JuraShinju_common.cns']:assert old[n]==current[n],n
assert omit(old['JuraShinju.cns'].decode(),'Statedef',[180])==omit(current['JuraShinju.cns'].decode(),'Statedef',[180,9570]),'Combat controller changed'
assert omit(old['JuraShinju.air'].decode(),'Begin Action',[180])==omit(current['JuraShinju.air'].decode(),'Begin Action',[180,8960]),'Combat animation changed'
packed=Sff2(CHAR/'JuraShinju.sff');preserved=0
with tempfile.TemporaryDirectory(prefix='jura-book-identity-') as temp:
    path=Path(temp)/'old.sff';path.write_bytes(old['JuraShinju.sff']);previous=Sff2(path)
    assert set(packed.sprites)==set(previous.sprites)
    for key in previous.sprites:
        if key[0]==3:
            image,axis=packed.image(*key);assert image.size==(32,24) and axis==(16,18)
            continue
        a,aa=packed.image(*key);b,ba=previous.image(*key)
        assert a.size==b.size and aa==ba and a.tobytes()==b.tobytes(),('Non-book sprite changed',key)
        preserved+=1
victory=re.search(r'(?ims)^\[Begin Action 180\].*?(?=^\[Begin Action|\Z)',current['JuraShinju.air'].decode())[0]
poses={tuple(map(int,m.groups())) for m in re.finditer(r'(?m)^(\d+),(\d+),',victory)}
assert poses=={(0,24),(0,19),(0,20)},poses
helper=re.search(r'(?ims)^\[Statedef 9570\].*?(?=^\[Statedef|\Z)',current['JuraShinju.cns'].decode())[0]
assert 'type = HitDef' not in helper and 'type = DestroySelf' in helper and 'Root,StateNo!=180' in helper
runtime=sha(b''.join(current[n] for n in NAMES));previous_runtime=sha(b''.join(old[n] for n in NAMES))
for name,facing in [('Jura_victory_checks.json',1),('Jura_victory_left_checks.json',-1)]:
    report=json.loads((OUT/name).read_text())
    assert report['runtime_sha256']==runtime and report['facing']==facing and not report['failures']
    assert {tuple(p) for p in report['original_body_poses']}==poses
    video=OUT/('Jura_victoria_motor.mp4' if facing==1 else 'Jura_victoria_izquierda_motor.mp4')
    assert sha(video.read_bytes())==report['video_sha256']
proof=dict(previous_commit=PREVIOUS,previous_runtime_sha256=previous_runtime,runtime_sha256=runtime,only_victory_presentation_changed=True,combat_states_and_animations_unchanged=True,commands_sounds_identity_common_unchanged=True,non_book_sprites_pixel_identical=preserved,original_body_sprites_pixel_identical=36,victory_body_poses=sorted([list(p) for p in poses]),victory_body_redrawn=False,book_only_sprite_group=3,book_prop_sprite_count=4,book_helper_is_visual_only=True,victory_facings_tested=[1,-1])
(OUT/'Jura_book_fix_checks.json').write_text(json.dumps(proof,indent=2)+'\n')
print('PASS victory uses original Jura body pixels;',preserved,'non-book sprites, all combat and all sounds unchanged; both facings tested')
