#!/usr/bin/env python3
"""Rebuild identity, original sprite/voice proof, native traces and protected files."""
from pathlib import Path
import hashlib,json,struct,subprocess,sys
from PIL import Image
from build_mitsuki_assets import B,S,cut
from make_combo_preview import Sff2
import numpy as np
from scipy.ndimage import label
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MitsukiTBV'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 baseline=json.loads((ROOT/'previews/MitsukiTBV_protected_baseline.json').read_text())
 for name,digest in baseline.items():assert sha(ROOT/name)==digest,('Modified another character',name)
 packed=Sff2(CHAR/'MitsukiTBV.sff');sheet=Image.open(ROOT/'source_material/Mitsuki_TBV_original/Mitsuki_TBV_sheet.png').convert('RGBA')
 bodies=0
 for g,poses in [(0,B),(1,S)]:
  for n,(role,box,ax) in enumerate(poses):
   im,origin=cut(sheet,box);v=np.array(im);lab,count=label(v[:,:,3]>0,np.ones((3,3)));sz=np.bincount(lab.ravel());sz[0]=0;v[:,:,3]=np.where(lab==sz.argmax(),255,0);im=Image.fromarray(v);bb=im.getbbox();im=im.crop(bb);origin=(origin[0]+bb[0],origin[1]+bb[1])
   real,axis=packed.image(g,n);a=np.array(real);b=np.array(im);assert a.shape==b.shape and np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:,:,:3][b[:,:,3]>0],b[:,:,:3][b[:,:,3]>0]),('Source body pixels changed',g,n)
   assert axis==(ax-origin[0],im.height-1);bodies+=1
 def snd(path):
  data=path.read_bytes();num,off=struct.unpack_from('<II',data,16);out={}
  for _ in range(num):nxt,size,g,n=struct.unpack_from('<IIII',data,off);out[g,n]=data[off+16:off+16+size];off=nxt
  return out
 source=snd(ROOT/'source_material/Mitsuki_CobraG6_voice_reference/Mitsuki.snd');runtime=snd(CHAR/'MitsukiTBV.snd')
 for n in range(1,24):assert runtime[0,n]==source[0,n],('Changed original voice',n)
 names=[f'MitsukiTBV.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['MitsukiTBV_common.cns'];before={n:sha(CHAR/n) for n in names}
 for tool in ['build_mitsuki_assets.py','build_mitsuki_runtime.py','validate_mitsuki.py']:subprocess.run([sys.executable,str(ROOT/'tools'/tool)],check=True)
 assert {n:sha(CHAR/n) for n in names}==before,'Runtime rebuild differs'
 digest=hashlib.sha256(b''.join((CHAR/n).read_bytes() for n in names)).hexdigest();total=0;historical=0
 subprocess.run([sys.executable,str(ROOT/'tools/verify_mitsuki_orochi_revision.py')],check=True)
 revision=json.loads((ROOT/'previews/MitsukiTBV_orochi_revision_checks.json').read_text());assert revision['runtime_sha256']==digest and revision['combat_mechanics_and_collision_unchanged']
 historical_reports=['MitsukiTBV_engine_checks.json','MitsukiTBV_low_life_checks.json','MitsukiTBV_rays_1.0_0_checks.json','MitsukiTBV_rays_0.5_1_checks.json']
 for report in historical_reports+['MitsukiTBV_capture_checks.json','MitsukiTBV_orochi_engine_checks.json','MitsukiTBV_orochi_short_target_checks.json']:
  x=json.loads((ROOT/'previews'/report).read_text());expected=revision['previous_runtime_sha256'] if report in historical_reports else digest
  assert x['runtime_sha256']==expected,('Unverified native test runtime',report);assert all(not c['failures'] for c in x['cases'])
  if report in historical_reports:historical+=len(x['cases'])
  else:total+=len(x['cases'])
  if 'orochi_' in report:
   assert len(x['cases'])==(10 if 'short_target' in report else 12)
   assert {c['case']['face'] for c in x['cases']}=={-1,1}
   assert {c['case']['distance'] for c in x['cases']} >= {60,210,400}
   assert all(c['case']['state']==11020 and c['orochi_serpent_frames']>0 and c['wrong_orochi_sprite_frames']==0 for c in x['cases'])
 archive=ROOT/'MitsukiTBV.zip';archive_before=sha(archive);subprocess.run([sys.executable,str(ROOT/'tools/package_mitsuki.py')],check=True);assert sha(archive)==archive_before,'Nondeterministic ZIP'
 demo=json.loads((ROOT/'previews/MitsukiTBV_demo_checks.json').read_text());assert demo['runtime_sha256']==digest and demo['audio_correlation']>.24 and demo['all_specials_shown'] and len(demo['scenes'])==26 and sha(ROOT/demo['video'])==demo['video_sha256']
 assert sha(ROOT/demo['orochi_clip'])==demo['orochi_clip_sha256']
 # Check the rendered projectile, not just its source palette: pure additive
 # light can turn a green asset cyan against this blue engine stage.
 native=ROOT/'previews/MitsukiTBV_Orochi_Ikazuchi_motor.png';pixels=np.array(Image.open(native).convert('RGB'),dtype=int)[360:660,400:1050]
 r,g,b=[pixels[:,:,i] for i in range(3)];green=int(np.count_nonzero((g>160)&(g>r+50)&(g>b+40)))
 assert green>5000,('Orochi does not render visibly green against the blue stage',green)
 result=dict(runtime_sha256=digest,original_body_poses_verified=bodies,original_voices_verified=23,unchanged_other_files=len(baseline),current_runtime_engine_cases=total,historical_unchanged_mechanics_engine_cases=historical,historical_reports=historical_reports,historical_evidence_basis='Published previous runtime; controller, collision, timing, old sprite and sound identity proved by MitsukiTBV_orochi_revision_checks.json',deterministic_rebuild=True,standalone_archive=True,actual_engine_video=True,all_26_specials_shown=True,green_orochi_native_animation_verified=True,native_green_projectile_pixels=green,native_orochi_image_sha256=sha(native),donor_body_effect_frames_removed=True,ranged_lightning_verified=True,distinct_kick_slide_uppercut=True,failures=[])
 (ROOT/'previews/MitsukiTBV_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result)
if __name__=='__main__':main()
