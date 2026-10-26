#!/usr/bin/env python3
"""Verify final Jigen resources, native evidence, package and optional public bytes."""
from pathlib import Path
import argparse,hashlib,json,subprocess,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1];NAME='JigenKara';BASELINE='8300bbbaca54d0e91d19fd199bb85f0bbf5f03c0'
PREVIOUS=['Eida','PochitaTrueForm','Mamushi','Shibai','JuraShinju','MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju','DeltaKara','SaradaTBV','DeepaKara','OugaYatsume']
def sha(b):return hashlib.sha256(b).hexdigest()
def report(n):return json.loads((ROOT/'previews'/n).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--commit');ap.add_argument('--write',action='store_true');args=ap.parse_args()
 files=[NAME+'.'+s for s in ['def','cns','cmd','air','sff','snd']]+[NAME+'_common.cns'];runtime=sha(b''.join((ROOT/NAME/f).read_bytes() for f in files))
 checks=report(NAME+'_engine_checks.json');capture=report(NAME+'_capture_checks.json');preview=report(NAME+'_preview_checks.json');feature=report(NAME+'_feature_checks.json');small=report(NAME+'_short_target_checks.json');horn=report(NAME+'_horn_checks.json');horninputs=report(NAME+'_horn_input_checks.json')
 assert all(r['runtime_sha256']==runtime for r in [checks,capture,preview,feature,small,horn,horninputs])
 for data,count in [(checks,120),(capture,16),(feature,36),(small,20),(horninputs,16)]:assert len(data['cases'])==count and all(not c['failures'] for c in data['cases'])
 for c in checks['cases']:
  if c['case']['kind'] in ['ultimate','ultimate_one_hp']:
   assert c['damage_pulses']==8 and c['pulse_span_ticks']==98 and c['victim_released']=='true'
   assert c['damage']==(800 if c['case']['form'] else 650)
  if c['end_form']==1:assert c['horn_layers']==1
  else:assert c['horn_layers']==0
 assert horn['input_cases']==16 and horn['attached_horn_samples']>500 and not horn['position_failures']
 receiving=report(NAME+'_receiving/'+NAME+'.json');assert len(receiving)==112 and all(c['damage']>0 and c['hurt'] and c['recovered'] for c in receiving)
 assert all(c['hits_received']==3 for c in receiving if c['attack']=='combo')
 dash=report(NAME+'_dash_checks.json');assert len(dash)==8 and all(c['passed'] for c in dash)
 video=ROOT/'previews'/preview['video'];assert sha(video.read_bytes())==preview['sha256']
 package=report(NAME+'_package_checks.json');archive=ROOT/package['archive'];assert archive.stat().st_size==package['bytes'] and sha(archive.read_bytes())==package['sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and set(z.namelist())=={NAME+'/'+f for f in package['files']}
  for f,digest in package['files'].items():assert sha((ROOT/NAME/f).read_bytes())==digest==sha(z.read(NAME+'/'+f)),f
 assert subprocess.run(['git','diff','--quiet',BASELINE,'--']+PREVIOUS,cwd=ROOT).returncode==0,'Previous playable character changed'
 source=report(NAME+'_source_checks.json');assert source['original_rgba_preserved'] and source['original_frames']==154 and source['derived_crops']==21
 result=dict(character=NAME,runtime_sha256=runtime,actual_inputs=120,feature_checks=36,receiving_probes=112,small_target_checks=20,horn_input_checks=16,dash_checks=8,original_frames=154,derived_crops=21,original_audio=44,awakening='Horn transformation and stronger attacks, 20 seconds',previous_characters_unchanged_from=BASELINE,archive_sha256=package['sha256'],video_sha256=preview['sha256'])
 if args.write:(ROOT/'previews'/f'{NAME}_delivery_checks.json').write_text(json.dumps(result,indent=2)+'\n')
 if args.commit:
  assert subprocess.check_output(['git','rev-parse',args.commit],cwd=ROOT,text=True).strip()==args.commit
  result['public']={}
  for local in [archive,video]:
   url=f'https://raw.githubusercontent.com/codeuzumaki6/MUGEN/{args.commit}/{local.relative_to(ROOT).as_posix()}'
   with urllib.request.urlopen(url,timeout=60) as response:data=response.read()
   assert data==local.read_bytes(),url
   result['public'][local.name]=dict(url=url,bytes=len(data),sha256=sha(data))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
