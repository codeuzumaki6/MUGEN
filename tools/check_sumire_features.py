#!/usr/bin/env python3
"""Real small Nue autonomy, physical defeat and fusion into the controlled beast."""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 proof=[]
 for kind in ['expiry','defeat','fusion']:
  env=os.environ.copy();env.update(SUMIRE_HELPER_TRACE='1',SUMIRE_CASES='["Nue"]',SUMIRE_FORM='0',SUMIRE_REPORT=f'SumireKakei_{kind}_checks.json')
  if kind=='defeat':env['SUMIRE_MINION_DAMAGE']='1'
  if kind=='fusion':env['SUMIRE_FUSION']='1'
  subprocess.run([sys.executable,str(ROOT/'tools/check_sumire_in_engine.py')],cwd=ROOT,env=env,check=True)
  p=Path(json.loads(Path('/tmp/SumireKakei_latest_trace.json').read_text())['trace']);rows=[l.split() for l in p.read_text().splitlines()];report=json.loads((ROOT/'previews'/env['SUMIRE_REPORT']).read_text())
  for i,c in enumerate(report['cases']):
   data=[r for r in rows if int(r[0])==i and int(r[1])>5];small=[r for r in data if int(r[11])>=0];assert small
   assert c['minimum_life']==1200 and c['helpers']==0 and max(int(r[6]) for r in data)==1
   entry=dict(kind=kind,face=c['case']['face'],root_life=1200,damage=c['damage'],maximum_age=max(int(r[13]) for r in small),minimum_health=min(int(r[11]) for r in small))
   if kind=='expiry':
    assert entry['maximum_age']==419 and c['damage']>0
    assert any(float(r[14])>0 and int(r[2])==0 and r[3]=='true' for r in small),'Nue did not attack independently'
   elif kind=='defeat':assert any(int(r[12])==9790 for r in small) and entry['minimum_health']<100 and entry['maximum_age']<250
   else:
    assert 520 in c['states'] and c['form_reached']==1 and c['end_form']==1 and entry['maximum_age']<250
    assert all(int(r[6])==0 for r in data if int(r[1])>250),'Small Nue remained beside controlled giant Nue'
   proof.append(entry)
 result=dict(runtime_sha256=report['runtime_sha256'],familiar_health=180,familiar_ticks=420,cases=proof)
 (ROOT/'previews/SumireKakei_feature_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: six native familiar autonomy, defeat and transformation cases')
if __name__=='__main__':main()
