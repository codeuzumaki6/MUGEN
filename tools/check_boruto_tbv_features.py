#!/usr/bin/env python3
"""Real sprite positions, short targets, safe Uzuhiko capture and MUGEN wind."""
from pathlib import Path
import json,math,os,subprocess,sys,tempfile,re
from boruto_source import ROOT
from boruto_tbv_sff import read_sff
NAME='BorutoTBVBase';CHAR=ROOT/NAME;TMP=Path(tempfile.mkdtemp(prefix='boruto-tbv-feature-',dir='/tmp'))
def run(label,**flags):
 env={k:v for k,v in os.environ.items() if not k.startswith('BORUTOTBV_')};trace=TMP/(label+'.tsv');report=NAME+'_'+label+'_checks.json';env.update(BORUTOTBV_CONTACT_TRACE=str(trace),BORUTOTBV_REPORT=report,**flags)
 with (TMP/(label+'.log')).open('w') as out:r=subprocess.run([sys.executable,str(ROOT/'tools/check_boruto_tbv_in_engine.py')],cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT)
 assert r.returncode==0,(TMP/(label+'.log')).read_text()[-4000:]
 return json.loads((ROOT/'previews'/report).read_text()),[r.split() for r in trace.read_text().splitlines()]
def main():
 poses={(r['group'],r['number']):r for r in json.loads((CHAR/'assets/sprites.json').read_text())};proof=[];contacts=[];landings=[]
 for scale in [1,.5]:
  report,rows=run('giant_full' if scale==1 else 'giant_short',BORUTOTBV_CASES='["Futon"]',BORUTOTBV_TARGET_SCALE=str(scale));proof.append(report);hp={}
  for ci in range(len(report['cases'])):
   yy=[float(r[7]) for r in rows if int(r[0])==ci and int(r[2])%10000==1440];step=max(abs(a-b) for a,b in zip(yy,yy[1:]));assert step<=13,(ci,step,'Rasengan snaps vertically');landings.append(dict(scale=scale,case=ci,maximum_vertical_step=step))
  for r in rows:
   ci,tick=int(r[0]),int(r[1]);life=int(r[13]);prev=hp.get(ci,1000);hp[ci]=life
   if tick<=5:continue
   if life>=prev:continue
   cell=poses[int(r[4]),int(r[5])];assert cell['key'].startswith('Hiruzen_04Hit_'),cell
   x,y,face=float(r[6]),float(r[7]),int(r[8]);tx,ty,height=float(r[11]),float(r[12]),float(r[16]);cx=x+face*(105-cell['axis'][0]);cy=y+205-cell['axis'][1];rect=(tx-14*scale,ty-height*.85,tx+14*scale,ty-10*scale);distance=math.hypot(cx-min(max(cx,rect[0]),rect[2]),cy-min(max(cy,rect[1]),rect[3]));assert y<0 and distance<=75
   contacts.append(dict(scale=scale,form=report['cases'][ci]['case']['form'],face=face,tick=tick,frame=cell['key'],inside_source_rasengan=True,distance_to_sphere=distance))
 assert len(contacts)==8
 far,_=run('far_giant',BORUTOTBV_CASES='["Futon"]',BORUTOTBV_DISTANCE='600',BORUTOTBV_EXPECT_MISS='1');proof.append(far)
 guard,rows=run('uzuhiko_guard',BORUTOTBV_CASES='["Espiral"]',BORUTOTBV_SPECIAL_GUARD='1',BORUTOTBV_EXPECT_MISS='1');proof.append(guard);assert not any(int(r[14])==3020 or int(r[17]) for r in rows)
 interrupted,rows=run('uzuhiko_interruption',BORUTOTBV_CASES='["Espiral"]',BORUTOTBV_UZUHIKO_INTERRUPT='1');proof.append(interrupted)
 for i,c in enumerate(interrupted['cases']):
  rr=[r for r in rows if int(r[0])==i];assert any(int(r[14])==3020 for r in rr) and c['minimum_life']<1200 and c['damage']<(304 if c['case']['form'] else 215) and rr[-1][15]=='true'
 late,_=run('late_ultimate_interrupt',BORUTOTBV_CASES='["ult_interrupt"]',BORUTOTBV_LATE_INTERRUPT='1');proof.append(late)
 current=None;effects=[]
 for line in (CHAR/(NAME+'.air')).read_text().splitlines():
  m=re.match(r'\[Begin Action (\d+)\]',line)
  if m:current=int(m[1])
  elif re.match(r'\s*\d+,\d+,',line):
   f=line.split(',');pose=poses.get((int(f[0]),int(f[1])))
   if pose and pose['kind']=='effect' and pose['group']==31000:assert len(f)>=7 and f[6].strip()=='A';effects.append([current,pose['key']])
 assert all(r['runtime_sha256']==proof[0]['runtime_sha256'] for r in proof)
 result=dict(runtime_sha256=proof[0]['runtime_sha256'],giant_sphere_contacts=contacts,smooth_rasengan_motion=landings,far_giant_misses=4,blocked_uzuhiko=4,interrupted_uzuhiko=4,late_ultimate_interruptions=4,standard_mugen_additive_frames=len(effects))
 (ROOT/'previews'/(NAME+'_feature_checks.json')).write_text(json.dumps(result,indent=2)+'\n');print('PASS: eight actual Rasengan contacts; range, guard, interruptions and standard MUGEN AIR effects')
if __name__=='__main__':main()
