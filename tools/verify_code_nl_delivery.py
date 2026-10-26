#!/usr/bin/env python3
"""Standalone resources, actual native evidence and optional public downloads."""
from pathlib import Path
import argparse,hashlib,json,subprocess,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1];NAME='CodeNoLimiter';BASELINE='84264f97d95ce166b32ac1649e051895788b0eb7'
PREVIOUS=['Eida','PochitaTrueForm','Mamushi','Shibai','JuraShinju','MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju','DeltaKara','SaradaTBV','DeepaKara','OugaYatsume','JigenKara']
def sha(b):return hashlib.sha256(b).hexdigest()
def report(n):return json.loads((ROOT/'previews'/n).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--commit');args=ap.parse_args()
 files=[NAME+'.'+s for s in ['def','cns','cmd','air','sff','snd']]+[NAME+'_common.cns'];runtime=sha(b''.join((ROOT/NAME/p).read_bytes() for p in files))
 core=report(NAME+'_engine_checks.json');capture=report(NAME+'_capture_checks.json');preview=report(NAME+'_preview_checks.json');feature=report(NAME+'_feature_checks.json');small=report(NAME+'_short_target_checks.json');beam=report(NAME+'_beam_interruption_checks.json')
 assert all(r['runtime_sha256']==runtime for r in [core,capture,preview,feature,small,beam])
 for r,n in [(core,120),(capture,13),(small,20),(beam,4)]:assert len(r['cases'])==n and all(not c['failures'] for c in r['cases'])
 assert len(feature['cases'])==16 and {c['kind'] for c in feature['cases']}=={'expiry','defeat','cap','travel'}
 for c in core['cases']:
  if c['case']['kind'] in ['ultimate','ultimate_one_hp']:
   assert c['damage']==(800 if c['case']['form'] else 650) and c['damage_pulses']==8 and c['pulse_span_ticks']==220 and c['victim_released']=='true'
 receiving=report(NAME+'_receiving/'+NAME+'.json');assert len(receiving)==112 and all(c['damage']>0 and c['hurt'] and c['recovered'] for c in receiving);assert all(c['hits_received']==3 for c in receiving if c['attack']=='combo')
 dash=report(NAME+'_dash_checks.json');assert len(dash)==8 and all(c['passed'] for c in dash)
 assert all(p['anchor']=='Original Code startup voice' and p['correlation']>=.20 for p in preview['activations'])
 video=ROOT/'previews'/preview['video'];assert sha(video.read_bytes())==preview['sha256']
 package=report(NAME+'_package_checks.json');archive=ROOT/package['archive'];assert archive.stat().st_size==package['bytes'] and sha(archive.read_bytes())==package['sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and set(z.namelist())=={NAME+'/'+f for f in package['files']}
  for f,digest in package['files'].items():assert sha((ROOT/NAME/f).read_bytes())==digest==sha(z.read(NAME+'/'+f)),f
 assert subprocess.run(['git','diff','--quiet',BASELINE,'--']+PREVIOUS,cwd=ROOT).returncode==0,'Previous playable character changed'
 source=report(NAME+'_source_checks.json');assert source['original_rgba_preserved'] and source['original_frames']==241 and source['reused_code_samples']==13 and not source['uploaded_zip_has_audio']
 result=dict(character=NAME,runtime_sha256=runtime,actual_inputs=120,receiving_probes=112,feature_checks=16,beam_interruption_checks=4,small_target_checks=20,dash_checks=8,original_frames=241,reused_code_audio=13,base='Code without limiters, white hair',awakening='Karma reinforcement and two Claw Grimes, 20 seconds',previous_characters_unchanged_from=BASELINE,archive_sha256=package['sha256'],video_sha256=preview['sha256'])
 if args.write:(ROOT/'previews'/f'{NAME}_delivery_checks.json').write_text(json.dumps(result,indent=2)+'\n')
 if args.commit:
  assert subprocess.check_output(['git','rev-parse',args.commit],cwd=ROOT,text=True).strip()==args.commit
  result['public']={}
  for p in [archive,video]:
   url=f'https://raw.githubusercontent.com/codeuzumaki6/MUGEN/{args.commit}/{p.relative_to(ROOT).as_posix()}'
   with urllib.request.urlopen(url,timeout=60) as response:data=response.read()
   assert data==p.read_bytes(),url
   result['public'][p.name]=dict(url=url,bytes=len(data),sha256=sha(data))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
