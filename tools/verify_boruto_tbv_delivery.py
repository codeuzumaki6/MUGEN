#!/usr/bin/env python3
"""Check the independent TBV base release and exact public downloads."""
import argparse,json,subprocess,urllib.request,zipfile
from boruto_source import ROOT,sha
NAME='BorutoTBVBase';BASELINE='ade99b53f2b2d32bf0b5c1c974e023e10eac6938'
PREVIOUS=['Eida','PochitaTrueForm','Mamushi','Shibai','JuraShinju','MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju','DeltaKara','SaradaTBV','DeepaKara','OugaYatsume','JigenKara','CodeNoLimiter','SumireKakei','HimawariTBV','BorutoKarmaJogan']
def report(s):return json.loads((ROOT/'previews'/(NAME+'_'+s+'_checks.json')).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--commit');args=ap.parse_args()
 files=[NAME+'.'+s for s in ['def','cns','cmd','air','sff','snd']]+[NAME+'_common.cns'];runtime=sha(b''.join((ROOT/NAME/f).read_bytes() for f in files));core=report('engine');small=report('short_target');clone=report('clone');feature=report('feature');capture=report('capture');preview=report('preview')
 assert all(j['runtime_sha256']==runtime for j in [core,small,clone,feature,capture,preview])
 for j,count in [(core,120),(small,20),(capture,16)]:assert len(j['cases'])==count and all(not c['failures'] for c in j['cases'])
 for c in core['cases']:
  if c['case']['kind'] in ['ultimate','ultimate_one_hp']:assert c['damage']==(800 if c['case']['form'] else 650) and c['damage_pulses']==8 and c['pulse_span_ticks']==200 and c['victim_released']=='true'
 assert len(clone['cases'])==8 and len(feature['giant_sphere_contacts'])==8 and all(c['inside_source_rasengan'] for c in feature['giant_sphere_contacts'])
 rendering=report('rendering');assert rendering['runtime_sha256']==runtime and rendering['original_source_frames']==161 and rendering['indexed_release_sprites']==287 and rendering['png32_release_sprites']==0 and rendering['preserved_opaque_pixels']>10000 and rendering['source_light_layers']==77 and rendering['no_opaque_actor_in_light'] and rendering['movement_uses_movement_sprites'] and rendering['final_wave_separate_from_body']
 movement=report('movement');assert movement['runtime_sha256']==runtime and len(movement['cases'])==4 and all(c['actual_jump'] and c['correct_air_sprites'] and c['correct_crouch'] and c['correct_landing'] and c['control_returned'] for c in movement['cases'])
 assert len(feature['smooth_rasengan_motion'])==8 and all(c['maximum_vertical_step']<=13 for c in feature['smooth_rasengan_motion'])
 assert feature['blocked_uzuhiko']==4 and feature['interrupted_uzuhiko']==4 and feature['far_giant_misses']==4 and feature['late_ultimate_interruptions']==4 and feature['standard_mugen_additive_frames']==37
 receiving=json.loads((ROOT/'previews'/(NAME+'_receiving')/(NAME+'.json')).read_text());assert len(receiving)==112 and all(c['damage']>0 and c['hurt'] and c['recovered'] for c in receiving) and all(c['hits_received']==3 for c in receiving if c['attack']=='combo')
 dash=report('dash');assert len(dash)==16 and all(c['passed'] for c in dash)
 source=report('source');assert source['original_files']==45 and source['original_frames']==161 and source['original_rgba_preserved'] and source['indexed_release'] and source['png32_release_sprites']==0 and source['original_audio']==38 and source['total_sounds']==60
 package=report('package');archive=ROOT/package['archive'];assert sha(archive.read_bytes())==package['sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and set(z.namelist())=={NAME+'/'+f for f in package['files']}
  for f,digest in package['files'].items():assert sha((ROOT/NAME/f).read_bytes())==digest==sha(z.read(NAME+'/'+f))
 video=ROOT/'previews'/preview['video'];focus=ROOT/'previews'/preview['uzuhiko_excerpt']['video'];assert sha(video.read_bytes())==preview['sha256'] and sha(focus.read_bytes())==preview['uzuhiko_excerpt']['sha256'] and all(c['correlation']>=.20 for c in preview['activations'])
 assert subprocess.run(['git','diff','--quiet',BASELINE,'--']+PREVIOUS,cwd=ROOT).returncode==0,'An earlier playable character changed'
 result=dict(character=NAME,runtime_sha256=runtime,actual_inputs=120,short_target_cases=20,receiving_probes=112,clone_cases=8,dash_cases=16,source_sphere_contacts=8,mugen_additive_effect_frames=37,original_frames=161,original_audio_references=38,archive_sha256=package['sha256'],video_sha256=preview['sha256'],previous_characters_unchanged_from=BASELINE)
 result.update(indexed_release_sprites=rendering['indexed_release_sprites'],png32_release_sprites=0,preserved_opaque_pixels=rendering['preserved_opaque_pixels'],source_light_layers=rendering['source_light_layers'],no_opaque_actor_in_light=rendering['no_opaque_actor_in_light'],actual_movement_cases=4,smooth_rasengan_motion_cases=8)
 if args.write:(ROOT/'previews'/(NAME+'_delivery_checks.json')).write_text(json.dumps(result,indent=2)+'\n')
 if args.commit:
  assert subprocess.check_output(['git','rev-parse',args.commit],cwd=ROOT,text=True).strip()==args.commit;result['public']={}
  for p in [archive,video,focus]:
   url=f'https://raw.githubusercontent.com/codeuzumaki6/MUGEN/{args.commit}/{p.relative_to(ROOT).as_posix()}'
   with urllib.request.urlopen(url,timeout=60) as response:data=response.read()
   assert data==p.read_bytes();result['public'][p.name]=dict(url=url,bytes=len(data),sha256=sha(data))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
