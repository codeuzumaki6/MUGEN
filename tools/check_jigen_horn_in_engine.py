#!/usr/bin/env python3
"""Observe the actual horn helper while Jigen attacks, shrinks, guards and falls."""
from pathlib import Path
import hashlib,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
os.environ.update(JIGEN_FORM='1',JIGEN_CASES=json.dumps(['Embestida','CorteCubo','Rodilla','Patada','Sukunahikona','guard','recovery','expire_attack']),JIGEN_REPORT='JigenKara_horn_input_checks.json')
trace=Path('/workspace/.eida-tools/ikemen-nightly/jigen_horn_trace.tsv');trace.write_text('')
source=(ROOT/'tools/check_jigen_in_engine.py').read_text()
extra='''local ht=assert(io.open('jigen_horn_trace.tsv','w'))
hook.add('loop','jigen_horn_observation',function()
 if not player(1) or roundState()~=2 or var(42)~=1 then return end
 local tick=(var(58)-1)%TICKS+1
 if tick<12 then return end
 local root={var(58),stateNo(),anim(),animElemNo(0),spriteVar('group'),spriteVar('image'),posX(),posY(),facing(),time()}
 if numHelper(9560)>0 and helper(9560) then
  local vals={var(0),spriteVar('group'),spriteVar('image'),posX(),posY()}
  for _,v in ipairs(vals) do root[#root+1]=v end
  ht:write(table.concat(root,'\\t')..'\\n');ht:flush();player(1)
 end
end)
'''
source=source.replace('module.write_text(lua);debug=',"lua+='\\n'+"+repr(extra)+".replace('TICKS',str(TICKS));module.write_text(lua);debug=")
exec(compile(source,str(ROOT/'tools/check_jigen_in_engine.py'),'exec'),{'__file__':str(ROOT/'tools/check_jigen_in_engine.py'),'__name__':'__main__'})
inputs=json.loads((ROOT/'previews/JigenKara_horn_input_checks.json').read_text());assert len(inputs['cases'])==16
manifest=json.loads((ROOT/'JigenKara/assets/sprites.json').read_text());byid={(r['group'],r['number']):r for r in manifest};anchors={r['key']:r for r in json.loads((ROOT/'JigenKara/assets/horn_anchors.json').read_text())}
rows=[list(map(float,l.split())) for l in trace.read_text().splitlines()];checked=0;native=0;seen=set();cases=set();errors=[]
for r in rows:
 clock,st,anim,elem,g,n,x,y,face,time,pose,hg,hn,hx,hy=r
 if time<2:continue # transitions settle before the debug loop observes the helper
 cell=byid[int(g),int(n)];key=cell['key'];cases.add((int(clock)-1)//480)
 if key not in anchors:
  assert key.startswith(('Jiraiya_Skill05_','Jiraiya_Ulti_','Caster_')),key
  native+=1;continue
 assert pose>0 and (hg,hn)==(30004,0),(key,r)
 a=anchors[key];dx,dy=a['relative'];scale=.55 if int(st)%10000==1420 and time<18 else 1
 error=max(abs(hx-(x+face*dx*scale)),abs(hy-(y+dy*scale)))
 # Bound positions and physics are observed on adjacent engine phases.
 if error>12:errors.append((key,error,r))
 checked+=1;seen.add(key)
assert checked>500 and native>100 and len(seen)>20,(checked,native,seen)
assert not errors,errors[:8]
proof=dict(runtime_sha256=inputs['runtime_sha256'],input_cases=16,observed_rows=len(rows),attached_horn_samples=checked,native_horn_samples=native,original_horn_sprite=[30004,0],body_poses=sorted(seen),maximum_allowed_phase_offset=12,position_failures=errors)
(ROOT/'previews/JigenKara_horn_checks.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
