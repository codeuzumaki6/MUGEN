#!/usr/bin/env python3
"""Prove source artwork/frame fidelity, base preservation and native evidence."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,tempfile
import numpy as np
from PIL import Image
from hidari_susanoo_source import ensure_source,recolor,actions,frames,ACTION_IDS
from read_sff_v1 import Sff1
from make_combo_preview import Sff2
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'HidariShinju';OUT=ROOT/'previews'
NAMES=[f'HidariShinju.{x}' for x in ['def','cns','cmd','air','sff','snd']]+['HidariShinju_common.cns']
CHIDORI_BASELINE='ebf75215e6845d6436ae5618b0ae944663cb2b82'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def chidori_revision():
 """Prove only base Chidori changes; Susanoo and all other moves stay exact."""
 def old(name):return subprocess.check_output(['git','show',f'{CHIDORI_BASELINE}:HidariShinju/{name}'],cwd=ROOT)
 for name in NAMES:
  before=old(name);after=(CHAR/name).read_bytes()
  if name=='HidariShinju.cns':
   a,b=states(before.decode()),states(after.decode())
   assert before.split(b'[Statedef',1)[0]==after.split(b'[Statedef',1)[0]
   assert b.keys()-a.keys()=={1001,1002,9460} and not a.keys()-b.keys()
   assert {n for n in a if a[n]!=b[n]}=={1000},'Another attack or global controller changed'
  elif name=='HidariShinju.air':
   def blocks(data):
    heads=list(re.finditer(rb'(?im)^\[Begin Action (\d+)\]',data))
    return {int(m[1]):data[m.start():heads[i+1].start() if i+1<len(heads) else len(data)].strip() for i,m in enumerate(heads)}
   a,b=blocks(before),blocks(after)
   assert b.keys()-a.keys()=={1001,1002} and not a.keys()-b.keys()
   assert {n for n in a if a[n]!=b[n]}=={1000},'Another animation changed'
  else:assert before==after,('Chidori revision changed another runtime file',name)
 return hashlib.sha256(b''.join(old(n) for n in NAMES)).hexdigest()
def unpack(s,g,n):
 v=s.sprites[g,n];base=s.tdata_offset if v[-1]&1 else s.ldata_offset;indices=np.frombuffer(s.data,dtype=np.uint8,count=v[2]*v[3],offset=base+v[9]).reshape(v[3],v[2]);return np.array(s.palette(v[11]),dtype=np.uint8)[indices],(v[4],v[5])
def states(s):
 h=list(re.finditer(r'(?im)^\[Statedef (-?\d+)\]',s));return {int(m[1]):s[m.start():h[i+1].start() if i+1<len(h) else len(s)].strip() for i,m in enumerate(h)}
def main():
 baseline=json.loads((OUT/'HidariShinju_sasuke_protected_baseline.json').read_text())
 for n,h in baseline.items():assert sha(ROOT/n)==h,('Unrelated resource changed',n)
 oldrev='708e7fe5e6318e97012e856acced840a8412c99b'
 def old(path):return subprocess.check_output(['git','show',f'{oldrev}:{path}'],cwd=ROOT)
 packed=Sff2(CHAR/'HidariShinju.sff')
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp)/'before.sff';p.write_bytes(old('HidariShinju/HidariShinju.sff'));before=Sff2(p)
  for n in range(63):
   a,ax=unpack(before,0,n);b,bx=unpack(packed,0,n);mask=a[:,:,3]>0;assert ax==bx and a.shape==b.shape and np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:,:,:3][mask],b[:,:,:3][mask]),('Hidari body or blue iris changed',n)
 original=states(old('HidariShinju/HidariShinju.cns').decode());current=states((CHAR/'HidariShinju.cns').read_text());preserved=[]
 for n,s in original.items():
  if 0<=n<10000 and n not in [520,1000,9500,9470,9471,9472,9473]:assert current[n]==s,('Base combat changed',n);preserved.append(n)
 assert old('HidariShinju/HidariShinju_common.cns')==(CHAR/'HidariShinju_common.cns').read_bytes();assert old('HidariShinju/HidariShinju.snd')==(CHAR/'HidariShinju.snd').read_bytes()
 assert all(g not in [8630,8645] for g,n in packed.sprites)
 source=Sff1(ensure_source());data=json.loads((CHAR/'assets/susanoo_source.json').read_text());count=0
 for row in data['sprites']:
  g,n=row['source'];im,axis=source.image(g,n);want=np.array(recolor(im));got,actual_axis=unpack(packed,g+10000,n);mask=want[:,:,3]>0
  assert got.shape==want.shape and axis==actual_axis and np.array_equal(got[:,:,3],want[:,:,3]) and np.array_equal(got[:,:,:3][mask],want[:,:,:3][mask]),('Source artwork changed beyond palette',g,n);count+=1
 air=(CHAR/'HidariShinju.air').read_text();heads=list(re.finditer(r'(?im)^\[Begin Action (\d+)\]',air));acts={int(m[1]):air[m.end():heads[i+1].start() if i+1<len(heads) else len(air)] for i,m in enumerate(heads)}
 for a in ACTION_IDS:
  expected=[(g+10000,n,t,tail.strip()) for g,n,x,y,t,tail in frames(actions()[a]) if g>=0];actual=[(g,n,t,tail.strip()) for g,n,x,y,t,tail in frames(acts[20000+a])];assert expected==actual,('Source sequence/timing changed',a)
 runtime=hashlib.sha256(b''.join((CHAR/n).read_bytes() for n in NAMES)).hexdigest()
 if '--assets-only' in sys.argv:print('PASS source frames,',count,'source sprites, 63 unchanged bodies,',len(preserved),'unchanged base states',runtime);return
 prior_runtime=chidori_revision()
 expected={'chidori_input':2,'chidori_range':12,'chidori_short':10,'chidori_capture':5};total=0
 for name,size in expected.items():
  path=OUT/f'HidariShinju_{name}_checks.json';report=json.loads(path.read_text())
  assert report['runtime_sha256']==runtime,('Stale report',name)
  assert len(report['cases'])==size and all(not c['failures'] for c in report['cases']),('Native failures',name)
  assert all(c['chidori_hand_bad_frames']<=2 and c['max_chidori_hand_helpers']==1 and c['hidden_base_frames']==0 for c in report['cases'])
  total+=size
 # Susanoo's video and reports belong to the preceding build. Its states,
 # animation, graphics, sounds, commands and visibility controller stay exact.
 for name in ['sasuke_verification','sasuke_demo_checks','sasuke_engine_checks','sasuke_expiry_checks','sasuke_capture_checks','sasuke_scale_checks']:
  path=OUT/f'HidariShinju_{name}.json'
  assert path.read_bytes()==subprocess.check_output(['git','show',f'{CHIDORI_BASELINE}:{path.relative_to(ROOT)}'],cwd=ROOT),('Unchanged Susanoo evidence was altered',name)
 previous=json.loads((OUT/'HidariShinju_sasuke_verification.json').read_text());assert previous['runtime_sha256']==prior_runtime and not previous['failures']
 susanoo=json.loads((OUT/'HidariShinju_sasuke_demo_checks.json').read_text())
 assert sha(OUT/susanoo['video'])==susanoo['video_sha256'] and sha(OUT/susanoo['indra_clip'])==susanoo['indra_sha256']
 demo=json.loads((OUT/'HidariShinju_chidori_demo_checks.json').read_text());assert demo['runtime_sha256']==runtime and demo['native_audio_cues_matched']==5 and not demo['failures']
 assert sha(OUT/demo['video'])==demo['video_sha256']
 archive=ROOT/'HidariShinju.zip';prior=sha(archive);subprocess.run([sys.executable,str(ROOT/'tools/package_hidari.py')],check=True);assert sha(archive)==prior
 result=dict(runtime_sha256=runtime,source_sprite_frames_verified=count,source_action_sequences_verified=len(ACTION_IDS),source_author='Shingeki No Mugen; sprites credited to Vovan99',base_chidori_source_action=1030,base_chidori_native_inputs_and_collision_tested=True,base_chidori_damage=185,base_chidori_cost=350,base_chidori_hits=6,same_three_normals_and_six_specials=True,palette_only_yellow=True,no_ai_susanoo_art=True,original_hidari_body_and_blue_iris_preserved=63,original_base_states_preserved_except_chidori=len(preserved),common_states_and_sounds_unchanged=True,unrelated_files_preserved=len(baseline),native_cases=expected,total_native_cases=total,unchanged_susanoo_evidence=dict(commit=CHIDORI_BASELINE,runtime_sha256=prior_runtime,verification='HidariShinju_sasuke_verification.json',applicability='All prior states except base Chidori 1000 and all prior AIR actions except 1000 remain exact; only states 1001,1002,9460 and AIR 1001,1002 added. Sprite, sound, commands, DEF, common states and global controllers remain byte-identical.'),awakening_only_susanoo_visible=True,real_engine_video_and_audio=True,standalone_archive=True,failures=[])
 (OUT/'HidariShinju_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result)
if __name__=='__main__':main()
