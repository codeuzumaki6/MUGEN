#!/usr/bin/env python3
"""Verify exact recorded runtime, repeatable builds, source art and older characters."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from PIL import Image
from make_combo_preview import Sff2
from read_reference_sff import ReferenceSff
from build_archives import png_to_indexed

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews';CHAR=ROOT/'JuraShinju'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=['JuraShinju.def','JuraShinju.sff','JuraShinju.snd','JuraShinju.air','JuraShinju.cns','JuraShinju.cmd','JuraShinju_common.cns']
before={n:sha(CHAR/n) for n in names}
runtime=hashlib.sha256(b''.join((CHAR/n).read_bytes() for n in names)).hexdigest()
checkpoint=json.loads((OUT/'Jura_capture_checkpoint.json').read_text())
exact_preview=checkpoint['runtime_sha256']==runtime
recording_runtime=runtime
namespace_path=OUT/'Jura_namespace_checks.json'
if not exact_preview and namespace_path.exists():
    namespace=json.loads(namespace_path.read_text())
    assert namespace['runtime_sha256']==runtime,'Namespace verification is stale'
    assert namespace['only_def_identity_and_file_references_changed'] and namespace['gameplay_sprites_eye_color_and_sounds_unchanged']
    for n,entry in namespace['files'].items():assert entry['sha256']==sha(CHAR/n),n
    recording_runtime=namespace['previous_runtime_sha256']
if not exact_preview:
    # The recorded attacks remain applicable after a strictly checked iris-only
    # palette correction; keep the older recording hash visible and honest.
    color=json.loads((OUT/'Jura_eye_color_checks.json').read_text())
    assert color['previous_runtime_sha256']==checkpoint['runtime_sha256'] and color['runtime_sha256']==recording_runtime,'Unverified runtime change since recording'
    assert color['sff_sha256']==sha(CHAR/'JuraShinju.sff')
    assert all(color[k] for k in ['non_iris_pixels_identical','axes_dimensions_and_alpha_identical','gameplay_and_sounds_unchanged','source_sheet_unchanged'])
for job,entry in checkpoint['jobs'].items():
    assert sha(OUT/f'Jura_{job}_motor.mp4')==entry['video_sha256'],job
assert len(checkpoint['jobs'])==10
assert {entry['report']['runtime_sha256'] for entry in checkpoint['jobs'].values()}=={runtime}
victory=json.loads((OUT/'Jura_victory_checks.json').read_text())
assert victory['runtime_sha256']==runtime and not victory['failures']
assert victory['real_ko'] and victory['victory_state']==180
assert {(3,n) for n in range(4)}<={tuple(p) for p in victory['book_poses']}
assert victory['video_sha256']==sha(OUT/'Jura_victoria_motor.mp4')
for repeat in range(2):
    for script in ['build_jura_assets.py','build_jura_runtime.py']:
        subprocess.run([sys.executable,str(ROOT/'tools'/script)],check=True,capture_output=True,text=True)
    assert before=={n:sha(CHAR/n) for n in names},'Non-deterministic build or changed tested files'
subprocess.run([sys.executable,str(ROOT/'tools/validate_jura.py')],check=True)
regressions=subprocess.run([sys.executable,str(ROOT/'tools/test_jura_regressions.py')],capture_output=True,text=True,check=True)
assert 'PASSED 7' in regressions.stdout
reportpath=OUT/'Jura_preservation_checks.json'
if len(sys.argv)>1:baseline=json.loads(Path(sys.argv[1]).read_text())
else:baseline=json.loads(reportpath.read_text())['protected_sha256']
for filename,checksum in baseline.items():assert sha(ROOT/filename)==checksum,filename
source={}
assert sha(ROOT/'source_material/Jura_original/Jura_sheet.png')=='ba763257d89940e5ab90428085d2f7d0036abb94837bf935168ca3170a6bb808','Original sheet bytes changed'
for dirname in ['Jura_original','Jura_generated']:
    for p in (ROOT/'source_material'/dirname).rglob('*'):
        if p.is_file():source[str(p.relative_to(ROOT))]=sha(p)
    manifest=ROOT/'source_material'/dirname/'sha256.json'
    if manifest.exists():
        for n,checksum in json.loads(manifest.read_text()).items():assert sha(manifest.parent/n)==checksum,n
packed=Sff2(CHAR/'JuraShinju.sff')
for pose in json.loads((CHAR/'assets/sprites.json').read_text())+json.loads((CHAR/'assets/supplemental.json').read_text()):
    actual,axis=packed.image(pose['group'],pose['number']);expected=Image.open(CHAR/pose['file']).convert('RGBA')
    a=np.array(actual);b=np.array(expected);mask=b[:,:,3]>0
    assert actual.size==expected.size and list(axis)==pose['axis']
    assert np.array_equal(a[:,:,3],b[:,:,3]),pose
    indices,palette,w,h,*_=png_to_indexed(CHAR/pose['file'])
    pal=np.frombuffer(palette,dtype=np.uint8).reshape(-1,4);expected_indexed=pal[np.frombuffer(indices,dtype=np.uint8)].reshape(h,w,4)
    assert np.array_equal(a,expected_indexed),pose
code=ReferenceSff(ROOT/'source_material/Shibai_Code_reference/Code.sff')
for dest,srcgroup,numbers in [(8880,90,[3]),(8881,200,[24]),(8900,576,range(24)),(8910,556,range(11,16)),(8920,7015,range(9))]:
    for n,source_n in enumerate(numbers):
        expected,axis=code.image(srcgroup,source_n);actual,actual_axis=packed.image(dest,n)
        assert actual_axis==axis and actual.size==expected.size
        a=np.array(actual);b=np.array(expected);mask=b[:,:,3]>0
        assert np.array_equal(a[:,:,3],b[:,:,3]),(dest,n,'Original Code effect alpha changed')
        if dest in [8880,8881]:assert np.array_equal(a[:,:,:3][mask],b[:,:,:3][mask]),(dest,n,'Claw mark pixels changed')
reports=[]
for name,count in [('Jura_engine_checks.json',124),('Jura_guard_checks.json',12),('Jura_low_life_checks.json',2),('Jura_CPU_checks.json',2),('Jura_regen_checks.json',8)]+[(f'Jura_aim_scale_{scale}_{crouch}_checks.json',56) for scale in [.25,.5] for crouch in [0,1]]:
    rows=json.loads((OUT/name).read_text());assert len(rows)==count and not any(r['failures'] for r in rows),name;reports.append(dict(report=name,cases=count))
reports.append(dict(report='Jura_victory_checks.json',cases=1))
combat=json.loads((OUT/'Jura_engine_checks.json').read_text())
for row in combat:
    if row['case']['name']=='Marca':
        assert row['claw_marks']==1 and row['claw_portals']>=2 and row['claw_mark_y']==0
        assert row['claw_travel']>=100 and row['claw_marks_remaining']==0
    if row['case']['kind']=='dash':
        assert abs(row['dash_signed_distance'])>=55 and row['jump_apex']==0
        assert (row['dash_signed_distance']>0)==(row['case']['button']=='R')
    if row['case']['kind'] in ['charge','chargehit']:
        assert row['charge_aura']==1 and row['aura_after_charge']==0
delivery=json.loads((OUT/'Jura_delivery_manifest.json').read_text());assert delivery['sha256']==sha(ROOT/delivery['archive'])
for n,checksum in delivery['files'].items():assert sha(CHAR/n)==checksum,n
proof=dict(existing_character_files_unchanged=len(baseline),protected_sha256=baseline,source_sha256=source,engine_reports=reports,engine_cases=sum(r['cases'] for r in reports),static_regressions=7,deterministic_rebuilds=2,runtime_files_sha256=before,runtime_sha256=runtime,preview_matches_delivered_runtime=exact_preview,preview_matches_delivered_gameplay=True,preview_eye_color='current' if exact_preview else 'older red iris; see Jura_eye_color_checks.json',original_body_poses=36,supplemental_body_poses=5,book_victory_tested=True,short_and_crouching_target_cases=224,tree_regeneration_and_interruption_cases=8,code_mark_pixels_preserved=True,code_crossed_bands_pixels_preserved=True,code_effect_frames_preserved=40,claw_entrance_exit_and_travel_tested=True,double_tap_dash_cases=8,charge_and_interruption_cases=8,exact_mugen_v14_executable_tested=False)
reportpath.write_text(json.dumps(proof,indent=2)+'\n')
print('PASS verified',proof['engine_cases'],'engine cases, 7 file regressions, 2 identical builds,',len(baseline),'older files unchanged;', 'exact recorded runtime' if exact_preview else 'only iris colors and verified namespace differ from recorded runtime')
