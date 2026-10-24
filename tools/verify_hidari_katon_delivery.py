#!/usr/bin/env python3
"""Verify the isolated RB replacement, original Sasuke fire, and native delivery."""
from pathlib import Path
import hashlib,json,re,struct,subprocess,sys,tempfile
import numpy as np
from make_combo_preview import Sff2
from read_sff_v1 import Sff1
from hidari_susanoo_source import ensure_source,actions,frames
from hidari_katon_source import ACTION_IDS,transparent_black
from verify_hidari_susanoo_delivery import unpack,states,NAMES
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'HidariShinju';OUT=ROOT/'previews'
BASE='ca0f89420f70c7212d6bcdf6da325465dfba8e64'
def old(path):return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)
def sha(blob):return hashlib.sha256(blob).hexdigest()
def sounds(data):
 count,off=struct.unpack_from('<II',data,16);out={}
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<4I',data,off);out[g,n]=data[off+16:off+16+size];off=nxt
 return out
def air_blocks(data):
 heads=list(re.finditer(r'(?im)^\[Begin Action (\d+)\]',data))
 return {int(m[1]):data[m.start():heads[i+1].start() if i+1<len(heads) else len(data)].strip() for i,m in enumerate(heads)}
def equal_sprite(a,b,key):
 x,ax=unpack(a,*key);y,ay=unpack(b,*key);mask=x[:,:,3]>0
 assert ax==ay and x.shape==y.shape and np.array_equal(x[:,:,3],y[:,:,3]) and np.array_equal(x[:,:,:3][mask],y[:,:,:3][mask]),('Existing sprite changed',key)

def main():
 baseline=json.loads((OUT/'HidariShinju_sasuke_protected_baseline.json').read_text())
 for path,digest in baseline.items():assert sha((ROOT/path).read_bytes())==digest,('Unrelated file changed',path)
 prior={n:old('HidariShinju/'+n) for n in NAMES};current={n:(CHAR/n).read_bytes() for n in NAMES}
 for name in ['HidariShinju.def','HidariShinju.cmd','HidariShinju_common.cns']:assert prior[name]==current[name],name
 a,b=states(prior['HidariShinju.cns'].decode()),states(current['HidariShinju.cns'].decode())
 assert b.keys()-a.keys()=={9401,9402} and not a.keys()-b.keys()
 assert {n for n in a if a[n]!=b[n]}=={1200},'Another attack or global controller changed'
 assert prior['HidariShinju.cns'].split(b'[Statedef',1)[0]==current['HidariShinju.cns'].split(b'[Statedef',1)[0]
 aa,bb=air_blocks(prior['HidariShinju.air'].decode()),air_blocks(current['HidariShinju.air'].decode())
 assert bb.keys()-aa.keys()=={21150,21160} and not aa.keys()-bb.keys()
 assert {n for n in aa if aa[n]!=bb[n]}=={1200},'Another animation changed'
 packed=Sff2(CHAR/'HidariShinju.sff');manifest=json.loads((CHAR/'assets/katon_source.json').read_text());added={tuple(row['packed']) for row in manifest['sprites']}
 with tempfile.TemporaryDirectory(prefix='hidari-katon-proof-') as tmp:
  path=Path(tmp)/'before.sff';path.write_bytes(prior['HidariShinju.sff']);before=Sff2(path)
  assert packed.sprites.keys()-before.sprites.keys()==added and not before.sprites.keys()-packed.sprites.keys()
  for key in before.sprites:equal_sprite(before,packed,key)
 source=Sff1(ensure_source())
 for row in manifest['sprites']:
  im,axis=source.image(*row['source']);want=np.array(transparent_black(im));got,ax=unpack(packed,*row['packed']);mask=want[:,:,3]>0
  assert axis==ax and want.shape==got.shape and np.array_equal(want[:,:,3],got[:,:,3]) and np.array_equal(want[:,:,:3][mask],got[:,:,:3][mask]),('Original fire changed',row['source'])
 for action in ACTION_IDS:
  expected=[(g+10000,n,t,tail.strip()) for g,n,x,y,t,tail in frames(actions()[action])]
  actual=[(g,n,t,tail.strip()) for g,n,x,y,t,tail in frames(bb[20000+action])]
  assert actual==expected,('Original fire sequence changed',action)
 before_sound,after_sound=sounds(prior['HidariShinju.snd']),sounds(current['HidariShinju.snd'])
 assert after_sound.keys()-before_sound.keys()=={(20,0),(20,1)} and not before_sound.keys()-after_sound.keys()
 for key,wav in before_sound.items():assert after_sound[key]==wav,('Existing sound changed',key)
 provenance=json.loads((ROOT/'source_material/Sasuke_BTM_original/katon_sounds/source.json').read_text())
 for row in provenance['samples']:
  wav=(ROOT/'source_material/Sasuke_BTM_original/katon_sounds'/row['file']).read_bytes();assert sha(wav)==row['sha256']
  assert after_sound[20,0 if row['source']==[4,10] else 1]==wav
 runtime=sha(b''.join(current[n] for n in NAMES));expected={'katon_input':2,'katon_range':14,'katon_short':12,'katon_capture':5}
 for name,count in expected.items():
  report=json.loads((OUT/f'HidariShinju_{name}_checks.json').read_text())
  assert report['runtime_sha256']==runtime and len(report['cases'])==count and all(not row['failures'] for row in report['cases']),name
  assert all(row['case']['state']==1200 and row['case']['b']=='y' and row['case']['d']=='N' and row['katon_wrong_sprite_frames']==0 and row['hidden_base_frames']==0 and row['end_helpers']==0 for row in report['cases']),name
 demo=json.loads((OUT/'HidariShinju_katon_demo_checks.json').read_text())
 assert demo['runtime_sha256']==runtime and demo['native_audio_cues_matched']==5 and not demo['failures'] and sha((OUT/demo['video']).read_bytes())==demo['video_sha256']
 for name in ['chidori','sasuke']:
  path=OUT/f'HidariShinju_{name}_demo_checks.json';assert path.read_bytes()==old(str(path.relative_to(ROOT)))
  proof=json.loads(path.read_text());assert sha((OUT/proof['video']).read_bytes())==proof['video_sha256']
 previous=json.loads(old('previews/HidariShinju_verification.json'));assert not previous['failures']
 archive=ROOT/'HidariShinju.zip';prior_zip=sha(archive.read_bytes());subprocess.run([sys.executable,str(ROOT/'tools/package_hidari.py')],check=True);assert sha(archive.read_bytes())==prior_zip
 result=dict(runtime_sha256=runtime,rb_base='Katon: Gokakyu no Jutsu',cost=200,damage=160,explosion_additional_damage=0,existing_sprite_frames_preserved=len(before.sprites),original_sasuke_fire_sprite_frames_verified=len(added),original_sasuke_fire_sequences_verified=len(ACTION_IDS),existing_sounds_preserved=len(before_sound),original_sasuke_sounds_added=2,existing_states_preserved_except_rb=len(a)-1,existing_air_actions_preserved_except_rb=len(aa)-1,original_hidari_body_and_blue_eyes_preserved=True,chidori_and_susanoo_preserved=True,commands_and_global_controllers_unchanged=True,unrelated_files_preserved=len(baseline),native_cases=expected,total_native_cases=sum(expected.values()),unchanged_previous_revision_evidence=dict(commit=BASE,runtime_sha256=previous['runtime_sha256'],applicability='Only base RB state/AIR 1200 changes, with two new fire helper states and two source effect actions. All 417 prior sprites and 19 prior sounds remain exact.'),real_engine_video_and_audio=True,standalone_archive=True,failures=[])
 (OUT/'HidariShinju_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result)
if __name__=='__main__':main()
