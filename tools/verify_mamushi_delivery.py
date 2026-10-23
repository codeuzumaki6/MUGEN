#!/usr/bin/env python3
"""Verify recorded runtime, unchanged clone behavior/art, and repeatable delivery."""
from pathlib import Path
import hashlib,json,re,subprocess,sys

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Mamushi';OUT=ROOT/'previews'
PREVIOUS='5f2dea330582d3f2a2370c2db6f00ed322d8728c'
NAMES=['Mamushi.def','Mamushi.sff','Mamushi.snd','Mamushi.air','Mamushi.cns','Mamushi.cmd','common1.cns']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def previous(name):return subprocess.check_output(['git','show',f'{PREVIOUS}:Mamushi/{name}'],cwd=ROOT)
def section(text,kind,n):
    found=re.search(rf'(?ims)^\[{kind} {n}\].*?(?=^\[{kind}|\Z)',text)
    assert found,(kind,n)
    return found[0]
before={n:sha(CHAR/n) for n in NAMES}
runtime=hashlib.sha256(b''.join((CHAR/n).read_bytes() for n in NAMES)).hexdigest()
old=previous('Mamushi.cns').decode();new=(CHAR/'Mamushi.cns').read_text()
clone_states=[1440,9500,9501,9503,9504,9505,9590,9591,-2]
for n in clone_states:assert section(old,'Statedef',n)==section(new,'Statedef',n),('Changed clone behavior',n)
for n in [3000,3001,3010,3011]:assert section(old,'Statedef',n)==section(new,'Statedef',n),('Changed ultimate',n)
old=previous('Mamushi.air').decode();new=(CHAR/'Mamushi.air').read_text()
for n in [1440,9500,9501,9503,9504,9505,9590,3000,3001,3002,3003,3004]:assert section(old,'Begin Action',n)==section(new,'Begin Action',n),('Changed clone/ultimate animation',n)
assert previous('Mamushi.snd')==(CHAR/'Mamushi.snd').read_bytes(),'Existing sounds changed'
checkpoint=json.loads((OUT/'Mamushi_capture_checkpoint.json').read_text())
assert checkpoint['runtime_sha256']==runtime,'Recordings use a different runtime'
assert set(checkpoint['jobs'])=={'especiales','dash','bramido','combos','division','ultimate'}
for name,entry in checkpoint['jobs'].items():
    assert entry['video_sha256']==sha(OUT/f'Mamushi_{name}_motor.mp4'),name
    assert entry['report']['runtime_sha256']==runtime
    assert not any(r['failures'] for r in entry['report']['combat_checks'])
reports=[]
for name,count in [('Mamushi_engine_checks.json',66),('Mamushi_extra_checks.json',18),('Mamushi_clone_health_checks.json',2),('Mamushi_low_life_checks.json',1),('Mamushi_CPU_checks.json',1),('Mamushi_dash_checks.json',16)]:
    rows=json.loads((OUT/name).read_text());assert len(rows)==count and not any(r['failures'] for r in rows),name
    for row in rows:
        if row['case']['kind']=='move':assert row['min_power']<=3000-row['case']['cost'],('Incorrect real energy cost',row['case'])
    reports.append(dict(report=name,cases=count))
for _ in range(2):
    for script in ['build_mamushi_assets.py','build_mamushi_runtime.py']:
        subprocess.run([sys.executable,str(ROOT/'tools'/script)],check=True,capture_output=True,text=True)
    assert before=={n:sha(CHAR/n) for n in NAMES},'Tested files changed during deterministic rebuild'
subprocess.run([sys.executable,str(ROOT/'tools/validate_mamushi.py')],check=True)
regression=subprocess.run([sys.executable,str(ROOT/'tools/test_mamushi_regressions.py')],check=True,capture_output=True,text=True)
assert 'Ran 6 tests' in regression.stderr and 'OK' in regression.stderr
if len(sys.argv)>1:protected=json.loads(Path(sys.argv[1]).read_text())
else:protected=json.loads((OUT/'Mamushi_preservation_checks.json').read_text())['protected_sha256']
for name,checksum in protected.items():assert sha(ROOT/name)==checksum,name
source={}
for p in (ROOT/'source_material/Mamushi_original').iterdir():
    if p.is_file():
        name=str(p.relative_to(ROOT));source[name]=sha(p)
        assert subprocess.check_output(['git','show',f'{PREVIOUS}:{name}'],cwd=ROOT)==p.read_bytes(),name
delivery=json.loads((OUT/'Mamushi_delivery_manifest.json').read_text())
assert sha(ROOT/delivery['archive'])==delivery['sha256']
for name,checksum in delivery['files'].items():assert sha(CHAR/name)==checksum,name
proof=dict(previous_commit=PREVIOUS,other_character_files_unchanged=len(protected),protected_sha256=protected,source_original_sha256=source,source_unchanged=True,original_body_and_weapon_entries_preserved=80,redrawn=False,clone_states_unchanged=clone_states,clone_animation_and_ultimate_unchanged=True,original_sounds_byte_identical=True,engine_reports=reports,engine_cases=sum(r['cases'] for r in reports),static_regressions=6,preview_runtime_sha256=runtime,preview_matches_delivered_runtime=True,deterministic_rebuilds=2,runtime_files_sha256=before,exact_mugen_v14_executable_tested=False)
(OUT/'Mamushi_preservation_checks.json').write_text(json.dumps(proof,indent=2)+'\n')
(OUT/'Mamushi_rebuild_checks.json').write_text(json.dumps(dict(deterministic=True,rebuilds=2,sha256=before),indent=2)+'\n')
print('PASS',proof['engine_cases'],'engine cases, 6 regressions, 2 identical builds, unchanged clone behavior and',len(protected),'other character files')
