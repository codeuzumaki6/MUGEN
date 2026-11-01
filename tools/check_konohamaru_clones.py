#!/usr/bin/env python3
"""Real clone attacks, independent player control, expiry and physical defeat."""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 proof=[]
 for kind in ['expiry','defeat']:
  env={k:v for k,v in os.environ.items() if not k.startswith('KONOHAMARU_')};env.update(KONOHAMARU_CLONE_TRACE='1',KONOHAMARU_CASES='["Clones"]',KONOHAMARU_REPORT=f'KonohamaruTBV_clone_{kind}_checks.json')
  if kind=='defeat':env['KONOHAMARU_CLONE_DAMAGE']='1'
  subprocess.run([sys.executable,str(ROOT/'tools/check_konohamaru_in_engine.py')],cwd=ROOT,env=env,check=True)
  trace=Path(json.loads(Path('/tmp/KonohamaruTBV_latest_clone_trace.json').read_text())['trace']);rows=[l.split() for l in trace.read_text().splitlines()];report=json.loads((ROOT/'previews'/env['KONOHAMARU_REPORT']).read_text())
  for i,c in enumerate(report['cases']):
   data=[r for r in rows if int(r[0])==i and int(r[1])>5];clone=[r for r in data if int(r[10])>=0];assert clone
   assert c['minimum_life']==1200 and max(int(r[6]) for r in data)==1 and int(data[-1][6])==0
   e=dict(kind=kind,form=c['case']['form'],face=c['case']['face'],root_life=1200,damage=c['damage'],maximum_age=max(int(r[12]) for r in clone),last_seen_tick=int(clone[-1][1]),minimum_health=min(int(r[10]) for r in clone))
   if kind=='expiry':
    assert e['maximum_age']==70 and e['damage']==(230 if c['case']['form'] else 170),e
    assert any(float(r[13])>0 and int(r[2])==0 and r[3]=='true' for r in clone),'Player did not regain control while the clone attacked'
   else:
    # Real jabs start at tick 86. Dispersal must occur during that probe,
    # before the unstruck clone's normal expiry, without harming the owner.
    assert e['maximum_age']<70 and 85<=e['last_seen_tick']<100,e
   proof.append(e)
 result=dict(runtime_sha256=report['runtime_sha256'],clone_health=120,clone_ticks=70,cases=proof)
 (ROOT/'previews/KonohamaruTBV_clone_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: eight real clone attacks, player control, expiry and physical defeat cases')
if __name__=='__main__':main()
