#!/usr/bin/env python3
"""Native sphere positions versus victim torso, misses, guards and interruption."""
from pathlib import Path
import hashlib,json,math,os,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];NAME='BorutoKarmaJogan';OUT=ROOT/'previews';TMP=Path(tempfile.mkdtemp(prefix='boruto-contact-',dir='/tmp'))
def run(label,**flags):
 env={k:v for k,v in os.environ.items() if not k.startswith('BORUTO_')};trace=TMP/(label+'.tsv');report=NAME+'_'+label+'_checks.json'
 env.update(BORUTO_CONTACT_TRACE=str(trace),BORUTO_REPORT=report,**flags)
 with (TMP/(label+'.log')).open('w') as log:r=subprocess.run([sys.executable,str(ROOT/'tools/check_boruto_in_engine.py')],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
 assert r.returncode==0,(TMP/(label+'.log')).read_text()[-5000:]
 return json.loads((OUT/report).read_text()),[l.split('\t') for l in trace.read_text().splitlines()]
def main():
 sprites={(r['group'],r['number']):r for r in json.loads((ROOT/NAME/'assets/sprites.json').read_text())};contacts=[];native=[]
 for scale in [1,.5]:
  report,rows=run('contact_full' if scale==1 else 'contact_short',BORUTO_CASES=json.dumps(['Rasengan','Caida','Futon']),BORUTO_TARGET_SCALE=str(scale));native.append(report);hp={};represented=set()
  for row in rows:
   ci,tick,st,tm,g,n=map(int,row[:6])
   if ci>=len(report['cases']):continue
   x,y,face=float(row[6]),float(row[7]),int(row[8]);tx,ty,life=float(row[11]),float(row[12]),int(row[13]);height=float(row[16]);previous=hp.get(ci,1000);hp[ci]=life
   case=report['cases'][ci]['case'];s=case['state'];single=s==1420 or s==11000;double=s in [11420,11440]
   if life>=previous or not (single or double):continue
   cell=sprites[g,n];key=cell['key'];ax,ay=cell['axis'];chest=(tx,ty-height*.5)
   if single:
    assert key.startswith('Pain_Skill02_') and 49<=int(key.rsplit('_',1)[-1])<=54,(case,key,'damage before visible Rasengan')
    cx,cy=x+face*(155-ax),y+160-ay;rect=(tx-14*scale,ty-height*.85,tx+14*scale,ty-10*scale);distance=math.hypot(cx-min(max(cx,rect[0]),rect[2]),cy-min(max(cy,rect[1]),rect[3]));inside=distance<=75
   else:
    assert key.startswith('Pain_Skill05_') and 149<=int(key.rsplit('_',1)[-1])<=173,(case,key,'damage outside sphere/field phase')
    index=int(key.rsplit('_',1)[-1])
    if index<=163:
     # Independently inspect the bright centers in the supplied artwork,
     # rather than retesting the rectangular collision boxes from AIR.
     centers=[(x+face*(cx-ax),y+165-ay) for cx in [125,315]];distance=min(math.hypot(chest[0]-cx,chest[1]-cy) for cx,cy in centers);inside=distance<=70
    else:
     cx,cy=x+face*(265-ax),y+155-ay;distance=((chest[0]-cx)/190)**2+((chest[1]-cy)/110)**2;inside=distance<=1
   assert inside,(case,key,x,y,tx,ty,distance,'victim outside visible effect')
   contacts.append(dict(scale=scale,case=case,tick=tick,source_frame=key,caster=[x,y],victim=[tx,ty],damage=previous-life,inside_visible_effect=inside));represented.add(ci)
  assert len(represented)==8,(scale,represented)
 misses=[]
 for label,flags in [('far_descent',dict(BORUTO_CASES='["Caida"]')),('far_awake',dict(BORUTO_FORM='1',BORUTO_CASES='["Rasengan","Futon"]'))]:
  report,_=run(label,BORUTO_DISTANCE='500',BORUTO_EXPECT_MISS='1',**flags);native.append(report);assert all(c['damage']==0 and c['ctrl']=='true' for c in report['cases']);misses+=report['cases']
 guard,rows=run('uzuhiko_guard',BORUTO_CASES='["Espiral"]',BORUTO_SPECIAL_GUARD='1',BORUTO_EXPECT_MISS='1');native.append(guard);assert len(guard['cases'])==4 and all(c['damage']==0 for c in guard['cases']);assert not any(int(r[14])==3020 for r in rows)
 interrupted,rows=run('uzuhiko_interruption',BORUTO_CASES='["Espiral"]',BORUTO_UZUHIKO_INTERRUPT='1');native.append(interrupted)
 for i,c in enumerate(interrupted['cases']):
  rr=[r for r in rows if int(r[0])==i];assert any(int(r[14])==3020 for r in rr),'Spiral never connected';assert c['minimum_life']<1200 and c['ctrl']=='true' and rr[-1][15]=='true' and c['damage']<(304 if c['case']['form'] else 215),(c,'Interruption did not release both players')
 late,_=run('late_ultimate_interruption',BORUTO_CASES='["ult_interrupt"]',BORUTO_LATE_INTERRUPT='1');native.append(late)
 assert all(r['runtime_sha256']==native[0]['runtime_sha256'] for r in native)
 proof=dict(runtime_sha256=native[0]['runtime_sha256'],sphere_contacts=contacts,contacts=len(contacts),far_misses=len(misses),blocked_spirals=len(guard['cases']),interrupted_spirals=len(interrupted['cases']),late_ultimate_interruptions=len(late['cases']),source='Actual engine positions and HP changes; torso lies in source-art sphere cores')
 (OUT/(NAME+'_visual_contact_checks.json')).write_text(json.dumps(proof,indent=2)+'\n');print('PASS',len(contacts),'visible sphere contacts,',len(misses),'range misses, four spiral guards and interruptions, four late cinematic interruptions')
if __name__=='__main__':main()
