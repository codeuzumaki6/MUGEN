#!/usr/bin/env python3
"""Actual minion autonomy, defeat, population cap and persistent mark travel."""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 proof=[]
 for kind in ['expiry','defeat','cap','travel']:
  env=os.environ.copy();env.update(CODE_NL_HELPER_TRACE='1',CODE_NL_CASES=json.dumps(['Marca' if kind=='travel' else 'Cerco' if kind=='cap' else 'Grime']),CODE_NL_REPORT=f'CodeNoLimiter_{kind}_checks.json')
  if kind=='defeat':env['CODE_NL_MINION_DAMAGE']='1'
  if kind=='travel':env['CODE_NL_MARK_TRAVEL']='1'
  subprocess.run([sys.executable,str(ROOT/'tools/check_code_nl_in_engine.py')],cwd=ROOT,env=env,check=True)
  trace=Path(json.loads(Path('/tmp/CodeNoLimiter_latest_trace.json').read_text())['trace']);rows=[l.split() for l in trace.read_text().splitlines()];report=json.loads((ROOT/'previews'/env['CODE_NL_REPORT']).read_text())
  for i,c in enumerate(report['cases']):
   data=[r for r in rows if int(r[0])==i and int(r[1])>5];assert c['minimum_life']==1300 and c['helpers']==c['aura']
   entry=dict(kind=kind,form=c['case']['form'],face=c['case']['face'],root_life=1300,damage=c['damage'])
   cap=max(int(r[6]) for r in data);assert cap<=(2 if c['case']['form'] else 1)
   if kind=='travel':
    assert 1210+10000*c['case']['form'] in c['states'] and c['min_power']==2600
    used=[r for r in data if int(r[2])%10000==1210 and 20<=int(r[10])<=25]
    assert used and all(abs(float(r[17])-float(r[8])-30*float(r[9]))<1 for r in used)
    assert min(int(r[16]) for r in used)>60,'The original placed mark was replaced instead of used'
    entry.update(original_mark_age_at_travel=min(int(r[16]) for r in used),actual_exit_offset=30,mark_count=max(int(r[7]) for r in data))
   else:
    minions=[r for r in data if int(r[11])>=0];assert minions
    hits=[r for r in minions if float(r[14])>0];assert hits and c['damage']>0
    autonomous=[r for r in hits if int(r[2])==0 and r[3]=='true'];assert autonomous
    entry.update(maximum_minions=cap,maximum_age=max(int(r[13]) for r in minions),minimum_health=min(int(r[11]) for r in minions),autonomous_hit_samples=len(autonomous))
    if kind=='defeat':assert any(int(r[12])==9790 for r in minions) and entry['minimum_health']<100 and entry['maximum_age']<250
    if kind=='expiry':assert entry['maximum_age']==419
    if kind=='cap':assert cap==(2 if c['case']['form'] else 1)
   proof.append(entry)
 result=dict(runtime_sha256=report['runtime_sha256'],cases=proof,minion_health=180,lifetime_ticks=420,mark_ticks=480)
 (ROOT/'previews/CodeNoLimiter_feature_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: 16 native minion and claw mark feature checks')
if __name__=='__main__':main()
