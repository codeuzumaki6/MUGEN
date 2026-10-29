#!/usr/bin/env python3
"""Native proof of the four original techniques requested in the references."""
from pathlib import Path
import json
from check_boruto_visual_contact import ROOT,NAME,OUT,run
def main():
 manifest=json.loads((ROOT/NAME/'assets/sprites.json').read_text());names={(r['group'],r['number']):r['key'] for r in manifest};cases=[];runtime=None
 for scale in [1,.5]:
  data,rows=run('original_kit_full' if scale==1 else 'original_kit_short',BORUTO_CASES='["Disparo","Espiral","Futon","Invocacion"]',BORUTO_TARGET_SCALE=str(scale))
  runtime=runtime or data['runtime_sha256'];assert data['runtime_sha256']==runtime
  for i,c in enumerate(data['cases']):
   ci=c['case'];rs=[r for r in rows if int(r[0])==i];name=ci['name'];form=ci['form'];record=dict(scale=scale,name=name,form=form,face=ci['face'],damage=c['damage'],damage_pulses=c['damage_pulses'])
   if name=='Disparo':
    flight={names.get((int(r[20]),int(r[21])), '') for r in rs if int(r[19])==9501};burst={names.get((int(r[20]),int(r[21])), '') for r in rs if int(r[19])==9511}
    assert c['damage']==250 and c['damage_pulses']==2 and flight and burst,c
    assert all(x in {f'Pain_Skill03_{n:02}' for n in range(56,60)} for x in flight) and all(x in {f'Pain_Skill03_{n:02}' for n in range(60,67)} for x in burst)
    record.update(blue_spheres_landed=2,original_flight=sorted(flight),original_burst=sorted(burst))
   elif name=='Espiral':
    body={names.get((int(r[4]),int(r[5])), '') for r in rs};assert any(x.startswith('Pain_Skill04_') and 82<=int(x.rsplit('_',1)[-1])<=94 for x in body)
    assert 'Pain_Skill01_60' in body and max(int(r[17]) for r in rs)==1
    assert all(int(r[13])<1000 for r in rs if int(r[17])>0),'Tornado appeared before contact'
    assert rs[-1][15]=='true' and int(rs[-1][17])==0
    record.update(original_body_wrap=True,original_lunge=True,tornado_after_contact=True,victim_released=True)
   elif name=='Futon':
    flight={names.get((int(r[24]),int(r[25])), '') for r in rs if int(r[23])==9505};burst={names.get((int(r[24]),int(r[25])), '') for r in rs if int(r[23])==9512}
    assert c['damage']==(240 if form else 205) and c['damage_pulses']==1 and flight and burst,c
    assert all(x in {f'Pain_Skill01_{n:02}' for n in range(17,20)} for x in flight) and all(x in {f'Pain_Skill01_{n:02}' for n in range(20,32)} for x in burst)
    record.update(original_green_projectile=sorted(flight),original_green_impact=sorted(burst))
   elif form:
    wood={names.get((int(r[28]),int(r[29])), '') for r in rs if int(r[26])>0};assert c['damage_pulses']==3 and c['damage']==345 and wood,c
    assert all(x in {f'Pain_Skill05_{n:02}' for n in range(5,23)} for x in wood) and int(rs[-1][26])==0
    record.update(original_mokuton_creatures=sorted(wood),finite_creatures=True)
   else:assert not any(int(r[26]) for r in rs),'Mokuton enabled outside awakening'
   cases.append(record)
 assert len(cases)==32
 proof=dict(runtime_sha256=runtime,cases=cases,blue_double_shot_cases=8,green_futon_cases=8,contact_tornado_cases=8,awakened_mokuton_cases=4,original_assets='Mon/RasenShot.xml, Mon/FutonRasen.xml, main skill04 uzu sequence, Mon/MonsterTanah.xml')
 (OUT/(NAME+'_original_kit_checks.json')).write_text(json.dumps(proof,indent=2)+'\n');print('PASS: two original blue Rasengan, green Futon, wrap/impact/tornado Uzuhiko and awakened Mokuton; 32 native cases')
if __name__=='__main__':main()
