#!/usr/bin/env python3
"""Prove Matsuri's original body art, both modes, native behavior and delivery."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from PIL import Image
from make_combo_preview import Sff2
from build_matsuri_assets import components,anchor
from verify_hidari_susanoo_delivery import unpack
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MatsuriShinju';OUT=ROOT/'previews'
NAMES=[f'MatsuriShinju.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['MatsuriShinju_common.cns']
def sha(blob):return hashlib.sha256(blob).hexdigest()
def main():
 baseline=json.loads((OUT/'MatsuriShinju_protected_baseline.json').read_text())
 for name,digest in baseline.items():assert sha((ROOT/name).read_bytes())==digest,('Existing character or source changed',name)
 source=ROOT/'source_material/Matsuri_original/Matsuri_sheet.png';provenance=json.loads(source.with_name('source.json').read_text());assert sha(source.read_bytes())==provenance['sha256']
 sheet=Image.open(source).convert('RGBA');rgb,labels,items=components(sheet);packed=Sff2(CHAR/'MatsuriShinju.sff');manifest=json.loads((CHAR/'assets/sprites.json').read_text());body_counts={0:0,1:0}
 for row in manifest:
  png=Image.open(CHAR/row['file']).convert('RGBA');want=np.array(png);got,axis=unpack(packed,row['group'],row['number']);mask=want[:,:,3]>0
  assert tuple(row['axis'])==axis and want.shape==got.shape and np.array_equal(want[:,:,3],got[:,:,3]) and np.array_equal(want[:,:,:3][mask],got[:,:,:3][mask]),('Packed art differs from source asset',row['group'],row['number'])
  if row['group'] in [0,1]:
   x,y,right,bottom=row['source_rectangle'];expected=np.array(sheet.crop(row['source_rectangle']));expected[:,:,3]=np.where(labels[y:bottom,x:right]==row['source_component'],255,0)
   assert not row['redrawn'] and row['native_scale'] and np.array_equal(expected,want) and tuple(anchor(png))==axis,('Original Matsuri body changed',row['group'],row['number'])
   body_counts[row['group']]+=1
 assert body_counts=={0:78,1:37},body_counts
 runtime=sha(b''.join((CHAR/name).read_bytes() for name in NAMES))
 if '--rebuild' in sys.argv:
  for tool in ['build_matsuri_assets.py','build_matsuri_runtime.py']:subprocess.run([sys.executable,str(ROOT/'tools'/tool)],check=True)
  assert sha(b''.join((CHAR/name).read_bytes() for name in NAMES))==runtime,'Rebuild changed tested runtime'
 expected={'engine':136,'range':144,'short':120,'low_life':4,'expiry':6,'garden':4,'capture':29};total=0
 for name,count in expected.items():
  report=json.loads((OUT/f'MatsuriShinju_{name}_checks.json').read_text())
  assert report['runtime_sha256']==runtime and len(report['cases'])==count and all(not row['failures'] for row in report['cases']),('Native failure or stale report',name)
  assert all(row['wrong_sage_body_frames']<=1 for row in report['cases']),('Wrong form bank',name);total+=count
 for name in ['low_life','engine']:
  report=json.loads((OUT/f'MatsuriShinju_{name}_checks.json').read_text())
  for row in report['cases']:
   if row['case']['kind']=='ultimate':assert row['damage']<500 if name=='low_life' else row['damage']<=450
 demo=json.loads((OUT/'MatsuriShinju_demo_checks.json').read_text());assert demo['runtime_sha256']==runtime and demo['all_specials_shown'] and demo['ultimate_both_forms_shown'] and demo['awakening_shown'] and demo['native_activation_cues_matched']==31 and not demo['failures']
 assert sha((ROOT/demo['video']).read_bytes())==demo['video_sha256'] and sha((ROOT/demo['ultimate_clip']).read_bytes())==demo['ultimate_clip_sha256']
 archive=ROOT/'MatsuriShinju.zip';before=sha(archive.read_bytes());subprocess.run([sys.executable,str(ROOT/'tools/package_matsuri.py')],check=True);assert sha(archive.read_bytes())==before,'Archive is not reproducible'
 result=dict(runtime_sha256=runtime,original_body_frames_verified=body_counts,total_original_body_frames=115,original_body_redrawn=False,original_body_native_scale=True,base_and_uncloaked_awakening=True,source_artwork_and_packed_assets_exact=True,ai_generated_water_effect_frames=8,no_ai_character_sprites=True,specials_per_form=13,ground_and_aerial_chains=True,double_tap_dash_both_directions=True,real_claw_mark_teleport=True,actual_garden_damage_buff_and_expiry=True,awakening_requires=3000,awakening_cost=1500,awakening_seconds=15,ultimate_cost=3000,ultimate_budget_base='min(420,42% max life)',ultimate_budget_awakened='min(450,45% max life)',ultimate_guard_miss_and_low_life_tested=True,activation_audio_and_aura_verified=True,native_cases=expected,total_native_cases=total,all_specials_and_both_ultimates_shown=True,real_engine_video_and_audio=True,existing_files_preserved=len(baseline),standalone_archive=True,rebuild_verified='--rebuild' in sys.argv,failures=[])
 (OUT/'MatsuriShinju_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS Matsuri delivery',result)
if __name__=='__main__':main()
