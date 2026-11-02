#!/usr/bin/env python3
"""Compare actual native damage with the previous published Naruto build."""
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASELINE='567f81b698454f352e97cc0f6bfc16829fee7c96'

def main():
 old=json.loads(subprocess.check_output(['git','show',BASELINE+':previews/NarutoBTM_engine_checks.json'],cwd=ROOT))
 new=json.loads((ROOT/'previews/NarutoBTM_engine_checks.json').read_text())
 key=lambda c:(c['case']['name'],c['case']['kind'],c['case']['form'],c['case']['face'])
 previous={key(c):c for c in old['cases']};rows=[]
 for c in new['cases']:
  if c['case']['kind'] not in ['move','combo','air','ultimate','ultimate_one_hp']:continue
  before=previous[key(c)]['damage'];after=c['damage'];form=c['case']['form'];kind=c['case']['kind']
  assert not c['failures'] and 0<after<before,(c['case'],before,after)
  if kind=='move':assert after<=(210 if form else 180),(c['case'],after)
  elif kind in ['combo','air']:assert after<=(260 if form else 200) and c['damage_pulses']>=3
  else:assert after==(360 if form else 300) and c['damage_pulses']==8 and c['victim_released']=='true'
  if kind!='ultimate_one_hp':assert c['minimum_life']==1200
  rows.append(dict(name=c['case']['name'],kind=kind,form=form,face=c['case']['face'],before=before,after=after))
 assert len(rows)==84
 guard=json.loads((ROOT/'previews/NarutoBTM_rasengan_guard_checks.json').read_text())
 assert guard['runtime_sha256']==new['runtime_sha256'] and len(guard['cases'])==8
 assert all(c['damage']==0 and not c['failures'] for c in guard['cases'])
 cns=(ROOT/'NarutoBTM/NarutoBTM.cns').read_text();air=(ROOT/'NarutoBTM/NarutoBTM.air').read_text()
 # Damage remains tied to real contact. The throw uses a sphere, while the
 # close Rasengan has no travelling helper or punch impact artwork.
 block=cns.split('[Statedef 1420]',1)[1].split('[Statedef ',1)[0]
 assert 'type=Helper' not in block and block.count('type=HitDef')==2
 sprites={r['key']:r for r in json.loads((ROOT/'NarutoBTM/assets/sprites.json').read_text())}
 byid={(r['group'],r['number']):r['key'] for r in sprites.values()}
 for n in [1200,1420,11200,11420]:
  action=air.split(f'[Begin Action {n}]',1)[1].split('[Begin Action ',1)[0]
  poses=[byid[int(m[1]),int(m[2])] for line in action.splitlines() if (m:=re.match(r'\s*(\d+),(\d+),',line))]
  assert poses and all(k.startswith('NarutoNew_RS_') or k=='NarutoNew_Idle_01' for k in poses),'Punch pose returned to a Rasengan technique'
 assert all(sprites[f'RasenganSphere_{i:02}']['source_parent']==f'NarutoNew_RS_Hit_{i:02}' for i in range(1,6))
 result=dict(runtime_sha256=new['runtime_sha256'],baseline_commit=BASELINE,target_life=1000,ultimate_damage=[300,360],rasengan_guard_cases=8,cases=rows)
 (ROOT/'previews/NarutoBTM_balance_checks.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS: 84 native damage comparisons and eight blocked Rasengan cases')
 for row in rows:
  if row['face']==1 and row['kind'] in ['move','ultimate']:print(row['name'],row['form'],row['before'],'->',row['after'])

if __name__=='__main__':main()
