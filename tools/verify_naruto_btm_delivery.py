#!/usr/bin/env python3
"""Verify the standalone Naruto BTM release and exact public downloads."""
import argparse,json,subprocess,urllib.request,zipfile
from boruto_source import ROOT,sha
from verify_boruto_tbv_delivery import PREVIOUS as EARLIER
NAME='NarutoBTM';BASELINE='06c85c6907a7ec47963e8dda3d625bc1d53fa4bf';PREVIOUS=EARLIER+['BorutoTBVBase','KonohamaruTBV']
def report(s):return json.loads((ROOT/'previews'/(NAME+'_'+s+'_checks.json')).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--commit');args=ap.parse_args()
 files=[NAME+'.'+s for s in ['def','cns','cmd','air','sff','snd']]+[NAME+'_common.cns'];runtime=sha(b''.join((ROOT/NAME/f).read_bytes() for f in files));core=report('engine');small=report('short_target');clone=report('clone');capture=report('capture');preview=report('preview')
 assert all(j['runtime_sha256']==runtime for j in [core,small,clone,capture,preview])
 for j,count in [(core,120),(small,24),(capture,21)]:assert len(j['cases'])==count and all(not c['failures'] for c in j['cases'])
 for c in core['cases']:
  if c['case']['kind'] in ['ultimate','ultimate_one_hp']:assert c['damage']==(800 if c['case']['form'] else 650) and c['damage_pulses']==8 and c['pulse_span_ticks']==200 and c['victim_released']=='true'
 assert len(clone['cases'])==8 and clone['clone_ticks']==70 and all(c['root_life']==1200 for c in clone['cases'])
 for c in clone['cases']:
  if c['kind']=='expiry':assert c['maximum_age']==70 and c['damage']==(310 if c['form'] else 230)
  else:assert c['maximum_age']<70 and 85<=c['last_seen_tick']<100
 receiving=json.loads((ROOT/'previews'/(NAME+'_receiving')/(NAME+'.json')).read_text());assert len(receiving)==112 and all(c['damage']>0 and c['hurt'] and c['recovered'] for c in receiving) and all(c['hits_received']==3 for c in receiving if c['attack']=='combo')
 dash=report('dash');assert len(dash)==16 and all(c['passed'] for c in dash)
 source=report('source');assert source['original_files']==73 and source['original_frames']==source['used_source_frames']==160 and source['original_rgba_preserved'] and source['indexed_sprites']==294 and source['png32_sprites']==0 and source['source_audio_references']==59 and source['total_sounds']==81
 package=report('package');archive=ROOT/package['archive'];assert sha(archive.read_bytes())==package['sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and set(z.namelist())=={NAME+'/'+f for f in package['files']}
  for f,digest in package['files'].items():assert sha((ROOT/NAME/f).read_bytes())==digest==sha(z.read(NAME+'/'+f))
 video=ROOT/'previews'/preview['video'];focus=ROOT/'previews'/preview['ultimate_excerpt']['video'];assert sha(video.read_bytes())==preview['sha256'] and sha(focus.read_bytes())==preview['ultimate_excerpt']['sha256'] and len(preview['activations'])==21 and all(c['correlation']>=.20 for c in preview['activations'])
 assert subprocess.run(['git','diff','--quiet',BASELINE,'--']+PREVIOUS,cwd=ROOT).returncode==0,'An earlier playable character changed'
 result=dict(character=NAME,runtime_sha256=runtime,actual_inputs=120,short_target_cases=24,receiving_probes=112,clone_cases=8,dash_cases=16,original_frames=160,used_source_frames=160,original_files=73,source_audio_references=59,indexed_release_sprites=294,png32_release_sprites=0,archive_sha256=package['sha256'],video_sha256=preview['sha256'],previous_characters_unchanged_from=BASELINE)
 if args.write:(ROOT/'previews'/(NAME+'_delivery_checks.json')).write_text(json.dumps(result,indent=2)+'\n')
 if args.commit:
  assert subprocess.check_output(['git','rev-parse',args.commit],cwd=ROOT,text=True).strip()==args.commit;result['public']={}
  for p in [archive,video,focus]:
   url=f'https://raw.githubusercontent.com/codeuzumaki6/MUGEN/{args.commit}/{p.relative_to(ROOT).as_posix()}'
   with urllib.request.urlopen(url,timeout=60) as response:data=response.read()
   assert data==p.read_bytes();result['public'][p.name]=dict(url=url,bytes=len(data),sha256=sha(data))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
