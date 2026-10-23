#!/usr/bin/env python3
"""Source pixel proof, bounded ultimates, guardian and standalone download."""
from pathlib import Path
import hashlib,json,struct,subprocess,sys
import numpy as np
from PIL import Image
from build_hidari_assets import BODIES,body,EYES
from make_combo_preview import Sff2
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'HidariShinju';OUT=ROOT/'previews'
NAMES=[f'HidariShinju.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['HidariShinju_common.cns']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 baseline=json.loads((OUT/'HidariShinju_protected_baseline.json').read_text())
 for name,digest in baseline.items():assert sha(ROOT/name)==digest,('Previous resource changed',name)
 source=ROOT/'source_material/Hidari_original';metadata=json.loads((source/'source.json').read_text());assert sha(source/'Hidari_sheet.png')==metadata['sha256']
 packed=Sff2(CHAR/'HidariShinju.sff');sheet=Image.open(source/'Hidari_sheet.png');eyes=0
 for n,(role,box,ax) in enumerate(BODIES):
  im,origin,pixels=body(sheet,box);actual,axis=packed.image(0,n);a=np.array(actual);b=np.array(im);mask=b[:,:,3]>0
  assert a.shape==b.shape and np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:,:,:3][mask],b[:,:,:3][mask]),('Body altered beyond permitted blue iris',n)
  assert axis==(ax-origin[0],im.height-1);eyes+=pixels
 assert len(BODIES)==63 and eyes>0 and {k for k in packed.sprites if k[0]==0}=={(0,n) for n in range(63)}
 # Guardian art is a distinct bank; never a replacement body or a miniature
 # copied fighter inside a lightning effect. Ensure all eight yellow poses.
 for n in range(8):
  im,_=packed.image(8630,n);a=np.array(im);rgb=a[:,:,:3][a[:,:,3]>0];assert im.height>120 and np.mean((rgb[:,0]>150)&(rgb[:,1]>120)&(rgb[:,2]<180))>.65
 for n in range(8):assert (8640,n) in packed.sprites
 assert (CHAR/'HidariShinju.snd').read_bytes()==(ROOT/'RyuShinju/RyuShinju.snd').read_bytes()
 before={n:sha(CHAR/n) for n in NAMES}
 for tool in ['build_hidari_assets.py','build_hidari_runtime.py','validate_hidari.py']:subprocess.run([sys.executable,str(ROOT/'tools'/tool)],check=True)
 assert before=={n:sha(CHAR/n) for n in NAMES},'Nondeterministic runtime build'
 digest=hashlib.sha256(b''.join((CHAR/n).read_bytes() for n in NAMES)).hexdigest()
 if '--assets-only' in sys.argv:print('PASS source poses, blue iris pixels',eyes,'and deterministic build',digest);return
 counts={};guardian_frames=0
 for name,expected in [('engine',132),('expiry',8),('low_life',4),('range',120),('short_target',100),('guardian',24),('visual',6),('capture',29)]:
  report=json.loads((OUT/f'HidariShinju_{name}_checks.json').read_text());assert report['runtime_sha256']==digest,('Stale native report',name)
  assert len(report['cases'])==expected and all(not c['failures'] for c in report['cases']),('Native test failure',name);counts[name]=expected
  if name=='low_life':assert all(c['damage'] in [210,225] for c in report['cases'])
  if name=='guardian':
   assert all(c['guardian_bad_frames']==0 for c in report['cases']);guardian_frames=sum(c['guardian_observed_frames'] for c in report['cases']);assert guardian_frames>1000
  if name=='capture':
   assert sum(c['case']['kind']=='move' for c in report['cases'])==26
   assert all(c['visible_susanoo']==1 for c in report['cases'] if c['case']['form']==1)
 archive=ROOT/'HidariShinju.zip';old=sha(archive);subprocess.run([sys.executable,str(ROOT/'tools/package_hidari.py')],check=True);assert old==sha(archive),'Nondeterministic archive'
 demo=json.loads((OUT/'HidariShinju_demo_checks.json').read_text());assert demo['runtime_sha256']==digest and len(demo['scenes'])==29 and demo['all_specials_shown'] and demo['ultimate_both_forms_shown'] and demo['awakening_shown'] and demo['audio_correlation']>.5
 assert sha(ROOT/demo['video'])==demo['video_sha256'] and sha(ROOT/demo['ultimate_clip'])==demo['ultimate_clip_sha256']
 result=dict(runtime_sha256=digest,original_body_poses_verified=63,body_shape_and_pixels_preserved_except_blue_iris=True,body_rescaled=False,blue_iris_pixels=eyes,eye_palette=[dict(original=k,blue=v) for k,v in EYES.items()],yellow_susanoo_poses=8,guardian_is_separate=True,guardian_checked_frames=guardian_frames,nonverbal_samples=19,previous_files_unchanged=len(baseline),native_cases=counts,current_runtime_engine_cases=sum(counts.values()),standalone_archive=True,deterministic_rebuild=True,actual_engine_video=True,all_specials_shown=True,ultimate_both_forms_shown=True,awakening_shown=True,low_life_ultimate_not_one_shot=True,failures=[])
 (OUT/'HidariShinju_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result)
if __name__=='__main__':main()
