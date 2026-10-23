#!/usr/bin/env python3
"""Original pixel proof, reproducible standalone archive, and native evidence."""
from pathlib import Path
import hashlib,json,struct,subprocess,sys
import numpy as np
from PIL import Image
from scipy.ndimage import label
from build_ryu_assets import BODIES,cut
from make_combo_preview import Sff2

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'RyuShinju';OUT=ROOT/'previews'
NAMES=[f'RyuShinju.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['RyuShinju_common.cns']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 baseline=json.loads((OUT/'RyuShinju_protected_baseline.json').read_text())
 for name,digest in baseline.items():assert sha(ROOT/name)==digest,('Another character changed',name)
 source=ROOT/'source_material/Ryu_original';metadata=json.loads((source/'source.json').read_text());assert sha(source/'Ryu_sheet.png')==metadata['sha256']
 packed=Sff2(CHAR/'RyuShinju.sff');sheet=Image.open(source/'Ryu_sheet.png');bodies=0
 for n,(role,box,ax) in enumerate(BODIES):
  im,origin=cut(sheet,box)
  if not role.startswith('iron_'):
   v=np.array(im);lab,_=label(v[:,:,3]>0,np.ones((3,3)));sizes=np.bincount(lab.ravel());sizes[0]=0;v[:,:,3]=np.where(lab==sizes.argmax(),255,0);im=Image.fromarray(v);bb=im.getbbox();im=im.crop(bb);origin=(origin[0]+bb[0],origin[1]+bb[1])
  actual,axis=packed.image(0,n);a=np.array(actual);b=np.array(im);mask=b[:,:,3]>0
  assert a.shape==b.shape and np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:,:,:3][mask],b[:,:,:3][mask]),('Original body pixels changed',n)
  assert axis==(ax-origin[0],im.height-1);bodies+=1
 assert bodies==81 and {k for k in packed.sprites if k[0]==0}=={(0,n) for n in range(81)}
 def sounds(path):
  data=path.read_bytes();count,off=struct.unpack_from('<II',data,16);out={}
  for _ in range(count):nxt,size,g,n=struct.unpack_from('<IIII',data,off);out[g,n]=data[off+16:off+16+size];off=nxt
  return out
 original=sounds(ROOT/'JuraShinju/JuraShinju.snd');runtime=sounds(CHAR/'RyuShinju.snd')
 assert len(runtime)==19 and all(g==1 and payload==original[g,n] for (g,n),payload in runtime.items())
 before={n:sha(CHAR/n) for n in NAMES}
 for tool in ['build_ryu_assets.py','build_ryu_runtime.py','validate_ryu.py']:subprocess.run([sys.executable,str(ROOT/'tools'/tool)],check=True)
 assert before=={n:sha(CHAR/n) for n in NAMES},'Nondeterministic runtime build'
 digest=hashlib.sha256(b''.join((CHAR/n).read_bytes() for n in NAMES)).hexdigest();count=0
 if '--assets-only' in sys.argv:
  print('PASS original body pixels and colors:',bodies,'; unchanged previous files:',len(baseline),'; deterministic runtime:',digest);return
 for name,expected in [('engine',132),('expiry',8),('low_life',4),('range',120),('short_target',100),('capture',29)]:
  report=json.loads((OUT/f'RyuShinju_{name}_checks.json').read_text());assert report['runtime_sha256']==digest,('Stale native report',name)
  assert len(report['cases'])==expected and all(not c['failures'] for c in report['cases']),('Native test failure',name);count+=expected
  if name=='low_life':assert all(c['damage'] in [210,225] for c in report['cases'])
  if name=='capture':
   assert sum(c['case']['kind']=='move' for c in report['cases'])==26
   assert all(c['visible_iron_wings']==1 and c['jump_apex']<-50 and c['victim_end'] not in [3010,3011] for c in report['cases'] if c['case']['kind']=='ultimate')
 archive=ROOT/'RyuShinju.zip';old=sha(archive);subprocess.run([sys.executable,str(ROOT/'tools/package_ryu.py')],check=True);assert old==sha(archive),'Nondeterministic archive'
 demo=json.loads((OUT/'RyuShinju_demo_checks.json').read_text());assert demo['runtime_sha256']==digest and len(demo['scenes'])==29 and demo['all_specials_shown'] and demo['ultimate_both_forms_shown'] and demo['awakening_shown'] and demo['audio_correlation']>.24
 assert sha(ROOT/demo['video'])==demo['video_sha256'] and sha(ROOT/demo['ultimate_clip'])==demo['ultimate_clip_sha256']
 result=dict(runtime_sha256=digest,original_body_poses_verified=bodies,original_body_pixels_and_colors_unchanged=True,original_bodies_rescaled=False,nonverbal_sound_payloads_verified=19,unchanged_other_files=len(baseline),current_runtime_engine_cases=count,standalone_archive=True,deterministic_rebuild=True,actual_engine_video=True,all_26_specials_shown=True,ultimate_both_forms_shown=True,awakening_shown=True,low_life_ultimate_is_not_one_shot=True,claw_mark_travel_and_both_dashes_tested=True,failures=[])
 (OUT/'RyuShinju_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result)
if __name__=='__main__':main()
