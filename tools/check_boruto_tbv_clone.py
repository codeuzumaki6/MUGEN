#!/usr/bin/env python3
"""Real eight-second clone pursuit, repeated attacks and physical defeat."""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 proof=[]
 for kind in ['expiry','defeat']:
  env={k:v for k,v in os.environ.items() if not k.startswith('BORUTOTBV_')};env.update(BORUTOTBV_CLONE_TRACE='1',BORUTOTBV_CASES='["Bunshin"]',BORUTOTBV_REPORT=f'BorutoTBVBase_clone_{kind}_checks.json')
  if kind=='defeat':env['BORUTOTBV_CLONE_DAMAGE']='1'
  subprocess.run([sys.executable,str(ROOT/'tools/check_boruto_tbv_in_engine.py')],cwd=ROOT,env=env,check=True)
  path=Path(json.loads(Path('/tmp/BorutoTBVBase_latest_clone_trace.json').read_text())['trace']);rows=[l.split() for l in path.read_text().splitlines()];report=json.loads((ROOT/'previews'/env['BORUTOTBV_REPORT']).read_text())
  for i,c in enumerate(report['cases']):
   data=[r for r in rows if int(r[0])==i and int(r[1])>5];clone=[r for r in data if int(r[10])>=0];assert clone
   assert c['minimum_life']==1200 and max(int(r[6]) for r in data)==1 and int(data[-1][6])==0
   cycles=sum(int(r[11])==9701 and (j==0 or int(clone[j-1][11])!=9701) for j,r in enumerate(clone))
   late=any(int(r[12])>180 and float(r[13])>0 for r in clone)
   e=dict(kind=kind,form=c['case']['form'],face=c['case']['face'],root_life=1200,damage=c['damage'],maximum_age=max(int(r[12]) for r in clone),minimum_health=min(int(r[10]) for r in clone),attack_cycles=cycles,late_independent_hits=late)
   if kind=='expiry':
    assert e['maximum_age']==479 and cycles>=3 and late,e
    assert any(float(r[13])>0 and int(r[2])==0 and r[3]=='true' for r in clone),'Clone did not attack independently'
   else:assert any(int(r[11])==9790 for r in clone) and e['minimum_health']<120 and e['maximum_age']<479
   proof.append(e)
 result=dict(runtime_sha256=report['runtime_sha256'],clone_health=120,clone_ticks=480,cases=proof)
 (ROOT/'previews/BorutoTBVBase_clone_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: eight clone pursuit, repeated attacks, expiry and defeat cases')
if __name__=='__main__':main()
