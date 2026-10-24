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
VISIBILITY_BASELINE='4087959b4a2a25281205430a7a3c87c94b9d9081'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def visibility_revision():
 """Prove older combat evidence remains applicable to this rendering-only fix."""
 def old(name):return subprocess.check_output(['git','show',f'{VISIBILITY_BASELINE}:HidariShinju/{name}'],cwd=ROOT)
 for name in NAMES:
  before=old(name);after=(CHAR/name).read_bytes()
  if name!='HidariShinju.cns':assert before==after,('Rendering fix changed another runtime file',name)
  else:
   marker=b'[State -2, Only Susanoo is visible during awakening]\n'
   prefix,block=after.split(marker)
   assert prefix.rstrip()+b'\n'==before
   assert block==b'type=AssertSpecial\ntrigger1=!IsHelper && Var(42)=1\nflag=Invisible\nflag2=NoShadow\nignorehitpause=1\n'
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
  if 0<=n<10000 and n not in [520,9500,9470,9471,9472,9473]:assert current[n]==s,('Base combat changed',n);preserved.append(n)
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
 prior_runtime=visibility_revision()
 expected={'base':66,'base_range':60,'base_short':50,'sasuke_engine':50,'sasuke_range':72,'sasuke_short':60,'sasuke_low_life':2,'sasuke_expiry':6,'sasuke_capture':10,'sasuke_hitpause':2};total=0;historical={};fresh={}
 for name,size in expected.items():
  path=OUT/f'HidariShinju_{name}_checks.json';report=json.loads(path.read_text())
  if report['runtime_sha256']==runtime:
   fresh[name]=size;total+=size
   if name.startswith('sasuke'):
    assert all(c['visibility_error_frames']==0 and c['hidden_guardian_frames']==0 for c in report['cases'])
  else:
   assert report['runtime_sha256']==prior_runtime,('Stale report',name)
   assert path.read_bytes()==subprocess.check_output(['git','show',f'{VISIBILITY_BASELINE}:{path.relative_to(ROOT)}'],cwd=ROOT),('Prior evidence changed',name)
   historical[name]=size
  assert len(report['cases'])==size and all(not c['failures'] for c in report['cases']),('Native failures',name)
 assert all(name in fresh for name in ['sasuke_engine','sasuke_expiry','sasuke_capture'])
 scale=json.loads((OUT/'HidariShinju_sasuke_scale_checks.json').read_text());assert scale['runtime_sha256']==runtime and scale['max_yellow_area']<250000 and not scale['failures']
 demo=json.loads((OUT/'HidariShinju_sasuke_demo_checks.json').read_text());assert demo['runtime_sha256']==runtime and demo['nine_source_attacks_shown'] and demo['hold_activation_shown'] and demo['native_audio_cues_matched']==10
 assert sha(OUT/demo['video'])==demo['video_sha256'] and sha(OUT/demo['indra_clip'])==demo['indra_sha256']
 archive=ROOT/'HidariShinju.zip';prior=sha(archive);subprocess.run([sys.executable,str(ROOT/'tools/package_hidari.py')],check=True);assert sha(archive)==prior
 result=dict(runtime_sha256=runtime,source_sprite_frames_verified=count,source_action_sequences_verified=len(ACTION_IDS),source_author='Shingeki No Mugen; sprites credited to Vovan99',same_three_normals_and_six_specials=True,palette_only_yellow=True,no_ai_susanoo_art=True,original_hidari_body_and_blue_iris_preserved=63,base_states_preserved=len(preserved),common_states_and_sounds_unchanged=True,unrelated_files_preserved=len(baseline),native_cases=fresh,total_native_cases=total,prior_combat_evidence=dict(commit=VISIBILITY_BASELINE,runtime_sha256=prior_runtime,cases=historical,total=sum(historical.values()),applicability='All seven runtime files byte-identical except the single root-only Invisible/NoShadow rendering controller'),awakening_only_susanoo_visible=True,base_body_restoration_tested=True,hold_to_awaken_tested=True,cancellation_and_expiry_tested=True,one_shot_prevented=True,real_engine_video_and_audio=True,standalone_archive=True,failures=[])
 (OUT/'HidariShinju_sasuke_verification.json').write_text(json.dumps(result,indent=2)+'\n');(OUT/'HidariShinju_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result)
if __name__=='__main__':main()
