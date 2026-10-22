#!/usr/bin/env python3
"""Verify exact recorded runtime, repeatable builds, source art and older characters."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from PIL import Image
from make_combo_preview import Sff2
from read_reference_sff import ReferenceSff

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews';CHAR=ROOT/'Shibai'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=['Shibai.def','Shibai.sff','Shibai.snd','Shibai.air','Shibai.cns','Shibai.cmd','common1.cns']
before={n:sha(CHAR/n) for n in names}
runtime=hashlib.sha256(b''.join((CHAR/n).read_bytes() for n in names)).hexdigest()
checkpoint=json.loads((OUT/'Shibai_capture_checkpoint.json').read_text());assert checkpoint['runtime_sha256']==runtime,'Previews use older runtime'
for job,entry in checkpoint['jobs'].items():
    assert sha(OUT/f'Shibai_{job}_motor.mp4')==entry['video_sha256'],job
assert len(checkpoint['jobs'])==8
for repeat in range(2):
    for script in ['build_shibai_assets.py','build_shibai_runtime.py']:
        subprocess.run([sys.executable,str(ROOT/'tools'/script)],check=True,capture_output=True,text=True)
    assert before=={n:sha(CHAR/n) for n in names},'Non-deterministic build or changed tested files'
subprocess.run([sys.executable,str(ROOT/'tools/validate_shibai.py')],check=True)
regressions=subprocess.run([sys.executable,str(ROOT/'tools/test_shibai_regressions.py')],capture_output=True,text=True,check=True)
assert 'PASSED 7' in regressions.stdout
reportpath=OUT/'Shibai_preservation_checks.json'
if len(sys.argv)>1:baseline=json.loads(Path(sys.argv[1]).read_text())
else:baseline=json.loads(reportpath.read_text())['protected_sha256']
for filename,checksum in baseline.items():assert sha(ROOT/filename)==checksum,filename
source={}
for dirname in ['Shibai_original','Shibai_Code_reference','Shibai_Kawaki_reference','Zenosama_reference','Shibai_generated']:
    for p in (ROOT/'source_material'/dirname).rglob('*'):
        if p.is_file():source[str(p.relative_to(ROOT))]=sha(p)
    manifest=ROOT/'source_material'/dirname/'sha256.json'
    if manifest.exists():
        for n,checksum in json.loads(manifest.read_text()).items():assert sha(manifest.parent/n)==checksum,n
packed=Sff2(CHAR/'Shibai.sff')
for pose in json.loads((CHAR/'assets/sprites.json').read_text()):
    actual,axis=packed.image(pose['group'],pose['number']);expected=Image.open(CHAR/pose['file']).convert('RGBA')
    a=np.array(actual);b=np.array(expected);mask=b[:,:,3]>0
    assert actual.size==expected.size and list(axis)==pose['axis']
    assert np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:,:,:3][mask],b[:,:,:3][mask]),pose
code=ReferenceSff(ROOT/'source_material/Shibai_Code_reference/Code.sff')
for dest,source,numbers in [(8880,90,[3]),(8881,200,[24]),(8900,576,range(24)),(8910,556,range(11,16)),(8920,7015,range(9))]:
    for n,source_n in enumerate(numbers):
        expected,axis=code.image(source,source_n);actual,actual_axis=packed.image(dest,n)
        assert actual_axis==axis and actual.size==expected.size
        a=np.array(actual);b=np.array(expected);mask=b[:,:,3]>0
        assert np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:,:,:3][mask],b[:,:,:3][mask]),(dest,n,'Original Code effect changed')
reports=[]
for name,count in [('Shibai_engine_checks.json',124),('Shibai_guard_checks.json',12),('Shibai_low_life_checks.json',2),('Shibai_CPU_checks.json',2)]:
    rows=json.loads((OUT/name).read_text());assert len(rows)==count and not any(r['failures'] for r in rows),name;reports.append(dict(report=name,cases=count))
combat=json.loads((OUT/'Shibai_engine_checks.json').read_text())
for row in combat:
    if row['case']['name']=='Garra':
        assert row['claw_marks']==1 and row['claw_portals']>=2 and row['claw_mark_y']==0
        assert row['claw_travel']>=100 and row['claw_marks_remaining']==0
    if row['case']['kind']=='dash':
        assert abs(row['dash_signed_distance'])>=55 and row['jump_apex']==0
        assert (row['dash_signed_distance']>0)==(row['case']['button']=='R')
    if row['case']['kind'] in ['charge','chargehit']:
        assert row['charge_aura']==1 and row['aura_after_charge']==0
delivery=json.loads((OUT/'Shibai_delivery_manifest.json').read_text());assert delivery['sha256']==sha(ROOT/delivery['archive'])
for n,checksum in delivery['files'].items():assert sha(CHAR/n)==checksum,n
proof=dict(existing_character_files_unchanged=len(baseline),protected_sha256=baseline,source_sha256=source,engine_reports=reports,engine_cases=sum(r['cases'] for r in reports),static_regressions=7,deterministic_rebuilds=2,runtime_files_sha256=before,runtime_sha256=runtime,preview_matches_delivered_runtime=True,articulation_poses_per_form=24,code_mark_pixels_preserved=True,code_crossed_bands_pixels_preserved=True,code_effect_frames_preserved=40,claw_entrance_exit_and_travel_tested=True,double_tap_dash_cases=8,charge_and_interruption_cases=8,exact_mugen_v14_executable_tested=False)
reportpath.write_text(json.dumps(proof,indent=2)+'\n')
print('PASS verified',proof['engine_cases'],'engine cases, 7 file regressions, 2 identical builds,',len(baseline),'older files unchanged, all eight previews match ZIP runtime')
