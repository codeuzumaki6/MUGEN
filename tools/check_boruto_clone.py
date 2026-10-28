#!/usr/bin/env python3
"""Real clone autonomy, lifetime and physical defeat in both modes/facings."""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 proof=[]
 for kind in ['expiry','defeat']:
  env=os.environ.copy();env.update(BORUTO_CLONE_TRACE='1',BORUTO_CASES='["Bunshin"]',BORUTO_REPORT=f'BorutoKarmaJogan_clone_{kind}_checks.json')
  if kind=='defeat':env['BORUTO_CLONE_DAMAGE']='1'
  subprocess.run([sys.executable,str(ROOT/'tools/check_boruto_in_engine.py')],cwd=ROOT,env=env,check=True)
  path=Path(json.loads(Path('/tmp/BorutoKarmaJogan_latest_clone_trace.json').read_text())['trace']);rows=[l.split() for l in path.read_text().splitlines()];report=json.loads((ROOT/'previews'/env['BORUTO_REPORT']).read_text())
  for i,c in enumerate(report['cases']):
   data=[r for r in rows if int(r[0])==i and int(r[1])>5];clone=[r for r in data if int(r[10])>=0];assert clone
   assert c['minimum_life']==1200 and max(int(r[6]) for r in data)==1 and int(data[-1][6])==0
   e=dict(kind=kind,form=c['case']['form'],face=c['case']['face'],root_life=1200,damage=c['damage'],maximum_age=max(int(r[12]) for r in clone),minimum_health=min(int(r[10]) for r in clone))
   if kind=='expiry':
    assert e['maximum_age']==179 and e['damage']>0
    assert any(float(r[13])>0 and int(r[2])==0 and r[3]=='true' for r in clone),'Clone did not attack independently'
   else:assert any(int(r[11])==9790 for r in clone) and e['minimum_health']<120 and e['maximum_age']<179
   proof.append(e)
 result=dict(runtime_sha256=report['runtime_sha256'],clone_health=120,clone_ticks=180,cases=proof)
 (ROOT/'previews/BorutoKarmaJogan_clone_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: eight clone autonomy, expiry and defeat cases')
if __name__=='__main__':main()
