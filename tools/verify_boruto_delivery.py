#!/usr/bin/env python3
"""Native evidence, standalone ZIP and exact public downloads for Boruto."""
from pathlib import Path
import argparse,hashlib,json,subprocess,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1];NAME='BorutoKarmaJogan';BASELINE='1d4788747397dd88b1130f082cb31cd85a710e51'
PREVIOUS=['Eida','PochitaTrueForm','Mamushi','Shibai','JuraShinju','MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju','DeltaKara','SaradaTBV','DeepaKara','OugaYatsume','JigenKara','CodeNoLimiter','SumireKakei','HimawariTBV']
def sha(b):return hashlib.sha256(b).hexdigest()
def report(n):return json.loads((ROOT/'previews'/n).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--commit');args=ap.parse_args()
 files=[NAME+'.'+s for s in ['def','cns','cmd','air','sff','snd']]+[NAME+'_common.cns'];runtime=sha(b''.join((ROOT/NAME/f).read_bytes() for f in files))
 core=report(NAME+'_engine_checks.json');capture=report(NAME+'_capture_checks.json');preview=report(NAME+'_preview_checks.json');small=report(NAME+'_short_target_checks.json');clone=report(NAME+'_clone_checks.json')
 assert all(r['runtime_sha256']==runtime for r in [core,capture,preview,small,clone])
 for data,count in [(core,120),(capture,16),(small,20)]:assert len(data['cases'])==count and all(not c['failures'] for c in data['cases'])
 for c in core['cases']:
  if c['case']['kind'] in ['ultimate','ultimate_one_hp']:assert c['damage']==(800 if c['case']['form'] else 650) and c['damage_pulses']==8 and c['pulse_span_ticks']==200 and c['victim_released']=='true'
 assert len(clone['cases'])==8 and {c['kind'] for c in clone['cases']}=={'expiry','defeat'} and clone['clone_health']==120 and clone['clone_ticks']==180
 contact=report(NAME+'_visual_contact_checks.json');assert contact['runtime_sha256']==runtime and contact['contacts']==28 and all(c['inside_visible_effect'] for c in contact['sphere_contacts'])
 kit=report(NAME+'_original_kit_checks.json');assert kit['runtime_sha256']==runtime and len(kit['cases'])==32 and kit['blue_double_shot_cases']==8 and kit['green_futon_cases']==8 and kit['contact_tornado_cases']==8 and kit['awakened_mokuton_cases']==4
 assert contact['far_misses']==8 and contact['blocked_spirals']==4 and contact['interrupted_spirals']==4 and contact['late_ultimate_interruptions']==4
 receiving=report(NAME+'_receiving/'+NAME+'.json');assert len(receiving)==112 and all(c['damage']>0 and c['hurt'] and c['recovered'] for c in receiving);assert all(c['hits_received']==3 for c in receiving if c['attack']=='combo')
 dash=report(NAME+'_dash_checks.json');assert len(dash)==16 and all(c['passed'] for c in dash) and {c['form'] for c in dash}=={0,1}
 video=ROOT/'previews'/preview['video'];assert sha(video.read_bytes())==preview['sha256'] and all(c['correlation']>=.20 for c in preview['activations'])
 package=report(NAME+'_package_checks.json');archive=ROOT/package['archive'];assert archive.stat().st_size==package['bytes'] and sha(archive.read_bytes())==package['sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and set(z.namelist())=={NAME+'/'+f for f in package['files']}
  for f,digest in package['files'].items():assert sha((ROOT/NAME/f).read_bytes())==digest==sha(z.read(NAME+'/'+f)),f
 source=report(NAME+'_source_checks.json');assert source['original_rgba_preserved'] and source['indexed_rle8_lossless'] and source['original_files']==618 and source['original_frames']==663 and source['selected_original_audio']==67 and source['wind_frames_visible'] and source['additive_wind_frames']==58 and source['exact_original_crops']==4
 assert subprocess.run(['git','diff','--quiet',BASELINE,'--']+PREVIOUS,cwd=ROOT).returncode==0,'Previous playable character changed'
 result=dict(character=NAME,runtime_sha256=runtime,actual_inputs=120,receiving_probes=112,clone_checks=8,short_target_checks=20,dash_checks=16,visible_sphere_contacts=28,original_technique_checks=32,additive_wind_frames=58,original_files=618,original_frames=663,selected_original_audio=67,awakening='Karma Jogan resonance, 20 seconds',previous_characters_unchanged_from=BASELINE,archive_sha256=package['sha256'],video_sha256=preview['sha256'])
 if args.write:(ROOT/'previews'/f'{NAME}_delivery_checks.json').write_text(json.dumps(result,indent=2)+'\n')
 if args.commit:
  assert subprocess.check_output(['git','rev-parse',args.commit],cwd=ROOT,text=True).strip()==args.commit;result['public']={}
  for p in [archive,video]:
   url=f'https://raw.githubusercontent.com/codeuzumaki6/MUGEN/{args.commit}/{p.relative_to(ROOT).as_posix()}'
   with urllib.request.urlopen(url,timeout=60) as response:data=response.read()
   assert data==p.read_bytes(),url;result['public'][p.name]=dict(url=url,bytes=len(data),sha256=sha(data))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
