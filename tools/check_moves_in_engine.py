#!/usr/bin/env python3
"""Exercise real command parsing and hit collisions in a TEMPORARY Ikemen copy.

Fixture-only AssertInput/PrintToConsole controllers are never added to Eida's
delivered files. Raw directional/button input goes through the real CMD parser.
Usage: python3 tools/check_moves_in_engine.py /tmp/ikemen-nightly
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
from build_moveset import MOVES, ROOT

engine = Path(sys.argv[1]).resolve()
char = engine/'chars/EidaCheck'
dummy = engine/'chars/EidaDummy'
shutil.copytree(ROOT/'Eida',char,dirs_exist_ok=True)
shutil.copytree(engine/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(char/'Eida.def',char/'EidaCheck.def')
shutil.copy2(dummy/'kfm.def',dummy/'EidaDummy.def')
scenarios=[]
for facing in (1,-1):
    for name,button,direction,state,cost,mode,description in MOVES:
        scenarios.append(dict(name=name,button=button,direction=direction,state=state,cost=cost,mode=mode,facing=facing,distance=42 if state in (1200,1300,1350) else 120,kind='move'))
scenarios += [
    dict(name='X chain',button='a',direction='N',state=203,cost=0,mode=2,facing=1,distance=40,kind='combo'),
    dict(name='Charm blocked',button='b',direction='D',state=1100,cost=500,mode=None,facing=1,distance=120,kind='block'),
    dict(name='Assist finite miss',button='a',direction='F',state=1000,cost=500,mode=0,facing=1,distance=120,kind='miss'),
    dict(name='Insufficient energy',button='z',direction='N',state=1060,cost=1500,mode=5,facing=1,distance=120,kind='empty'),
    dict(name='Awakening',button='s',direction='D',state=4000,cost=3000,mode=None,facing=1,distance=120,kind='aura'),
]
for case in list(scenarios[:22]):
    if case['direction'] in ('F','B'):
        scenarios.append({**case,'name':case['name']+' diagonal shortcut','shortcut':True})
for button,state in [('b',211),('c',221)]:
    scenarios.append(dict(name=f'{button} normal chain',button=button,direction='N',state=state,cost=0,mode=None,facing=1,distance=40,kind='combo'))
scenarios.append({**scenarios[10],'name':'RT during awakening','kind':'awakened'})
for facing in (1,-1):
    scenarios.append(dict(name='Forward dash and attack',button='a',direction='N',state=100,cost=0,mode=None,facing=facing,distance=160,kind='dash'))
    scenarios.append(dict(name='Aerial X Y B during hitpause',button='a',direction='N',state=620,cost=0,mode=None,facing=facing,distance=36,kind='aircombo'))
scenarios.append(dict(name='Charm finite miss',button='b',direction='D',state=1100,cost=500,mode=None,facing=1,distance=120,kind='charmmiss'))
capture_dir=os.environ.get('EIDA_CAPTURE')
if capture_dir:
    requested=os.environ.get('EIDA_CAPTURE_CASES')
    if requested:
        names=json.loads(requested)
        selected=[next(c for c in scenarios if c['name']==name and c['facing']==1) for name in names]
        scenarios=selected
    else:
        scenarios=[scenarios[0],scenarios[26]]
    Path(capture_dir).mkdir(parents=True,exist_ok=True)


def ctrl(label,typ,trigger,body):
    return f'\n[State -2, CHECK {label}]\ntype = {typ}\ntriggerall = IsHelper = 0\ntriggerall = RoundState = 2\ntrigger1 = {trigger}\nignorehitpause = 1\n{body}\n'


clock=ctrl('clock','VarAdd','1','v = 58\nvalue = 1')
fixture=clock
other=clock
for idx,case in enumerate(scenarios):
    base=idx*180
    at=lambda tick:f'Var(58) = {base+tick}'
    face=case['facing']; distance=case['distance'];root_x=-face*distance/2; target_x=face*distance/2
    for who,text,x,desired in [('root',fixture,root_x,face),('dummy',other,target_x,-face)]:
        text+=ctrl(f'case {idx}','VarSet',at(1),f'v = 59\nvalue = {idx}')
        text+=ctrl('reset pos','PosSet',at(1),f'x = {x}\ny = 0')
        text+=ctrl('reset vel','VelSet',at(1),'x = 0\ny = 0')
        text+=ctrl('reset face','Turn',at(1)+f' && Facing != {desired}','')
        text+=ctrl('reset life','LifeSet',at(1),'value = 1000')
        text+=ctrl('reset power','PowerSet',at(1),f'value = {0 if case["kind"]=="empty" else 3000}')
        text+=ctrl('reset awakening','VarSet',at(1),'v = 40\nvalue = 0')
        if who=='root' and case['kind']=='awakened':
            text+=ctrl('set awakening','VarSet',at(1),'v = 40\nvalue = 1')
            text+=ctrl('timer awakening','VarSet',at(1),'v = 41\nvalue = 900')
        text+=ctrl('reset state','ChangeState',at(1),'value = 0\nctrl = 1')
        if who=='root':fixture=text
        else:other=text

    # Motion inputs are world-relative; mirror left/right when facing reverses.
    d=case['direction'];button=case['button']
    if d in ('F','B'):
        side='R' if (d=='F')==(face==1) else 'L'
        fixture+=ctrl('down input','AssertInput',f'Var(58) = [{base+20},{base+(30 if case.get("shortcut") else 25)}]','flag = D')
        fixture+=ctrl('side input','AssertInput',f'Var(58) = [{base+24},{base+30}]',f'flag = {side}')
        press=28
    elif d=='D':
        fixture+=ctrl('down input','AssertInput',f'Var(58) = [{base+20},{base+24}]','flag = D')
        press=22
    else:press=22
    presses=[22,32,46,60] if case['kind']=='combo' else [press]
    for tick in presses:
        fixture+=ctrl('button input','AssertInput',at(tick),f'flag = {button}')
    if case['state'] in (1200,1300,1350):
        other+=ctrl('place incoming strike','PosSet',at(36),f'x = (P2,Pos X) + {face*36}\ny = 0')
        other+=ctrl('incoming strike','ChangeState',at(38),'value = 210\nctrl = 0')
    if case['kind']=='block':
        other+=ctrl('hold guard','AssertInput',f'Var(58) = [{base+15},{base+120}]',f'flag = {"R" if face==1 else "L"}')
    if case['kind'] in ('miss','charmmiss'):
        other+=ctrl('evade','PosSet',f'Var(58) = [{base+18},{base+150}]','y = -160')
        other+=ctrl('hold evade','VelSet',f'Var(58) = [{base+18},{base+150}]','x = 0\ny = 0')
        other+=ctrl('airborne evade','ChangeState',at(18),'value = 50\nctrl = 0')
    if case['kind']=='dash':
        side='R' if face==1 else 'L'
        for start,end in [(12,14),(18,34)]:
            fixture+=ctrl('forward dash input','AssertInput',f'Var(58) = [{base+start},{base+end}]',f'flag = {side}')
    if case['kind']=='aircombo':
        for who,text in [('root',fixture),('dummy',other)]:
            # Keep both fighters at contact height to isolate input buffering.
            text+=ctrl('airborne contact height','PosSet',f'Var(58) = [{base+15},{base+110}]','y = -55')
            text+=ctrl('airborne fixture velocity','VelSet',f'Var(58) = [{base+15},{base+110}]','y = 0')
            text+=ctrl('airborne setup','ChangeState',at(15),'value = 50\nctrl = '+('1' if who=='root' else '0'))
            if who=='root':fixture=text
            else:other=text
        for state,button in [(600,'b'),(610,'c')]:
            fixture+=ctrl('press next button inside hitpause','AssertInput',f'StateNo = {state} && MoveContact && HitPauseTime = 5',f'flag = {button}')

# Dismiss any helper left over across fixture resets.
fixture+='''\n[State -2, CHECK helper cleanup]
type = DestroySelf
triggerall = IsHelper
trigger1 = Root,Var(58) % 180 = [1,3]
ignorehitpause = 1
'''
for directory,text,filename in [(char,fixture,'Eida.cns'),(dummy,other,'kfm.cns')]:
    if directory==dummy:
        # One authoritative timeline: the defender can spend ticks in a
        # foreign custom state, so its own counter must not schedule inputs.
        text=text.replace('Var(58)', '(EnemyNear,Var(58))')
    p=directory/filename;s=p.read_text(encoding='latin-1')
    import re
    if re.search(r'(?im)^\[Statedef -2\]',s):
        s=re.sub(r'(?im)^(\[Statedef -2\])',lambda m:m[1]+'\n'+text,s,count=1)
    else:s+='\n[Statedef -2]\n'+text
    p.write_text(s,encoding='latin-1')

module=engine/'external/mods/eida_checks.lua'
module.parent.mkdir(exist_ok=True)
module_text='''local last = -1
local rows = {}
local frameSeen = -1
local f = assert(io.open('eida_checks.tsv','a'))
hook.add('loop','eida_checks',function()
  if not player(1) or roundState() ~= 2 then return end
  local clock = var(58)
  if clock == frameSeen or clock < 1 then return end
  frameSeen = clock
  local case = math.floor((clock-1)/180)
  local tick = (clock-1)%180+1
  if case >= CASECOUNT then player(2); setLife(100); player(1); setTime(0); return end
  if rows[case] == nil then rows[case] = {states={}, damage=0, charm=false, spawn=-1, helperDistance=0, helpers=0, power=3000, aura=false, marker=false, invalidMarker=false, lateMarker=false, dashTravel=0} end
  local r=rows[case]
  if tick > 4 then
    r.states[stateNo()]=true
    r.power=math.min(r.power,power())
    local x=posX()
    if stateNo()==100 then r.dashTravel=math.max(r.dashTravel, math.abs(x-(STARTPOSITIONS)[case+1])) end
    r.helpers=math.max(r.helpers,numHelper(1001))
    if helper(1001) then
      if r.spawn<0 then r.spawn=math.abs(posX()-x) end
      r.helperDistance=math.max(r.helperDistance,math.abs(posX()-x))
      player(1)
    end
    if helper(8301) then r.aura=true; player(1) end
    if helper(1101) then
      if stateNo()==1130 then
        r.marker=true
        player(2)
        if stateNo()~=1105 then r.invalidMarker=true end
      end
      player(1)
    end
    if tick>130 and numHelper(1101)>0 then r.lateMarker=true end
    player(2)
    r.damage=math.max(r.damage,1000-life())
    if stateNo()==1105 then r.charm=true end
    player(1)
  end
  if tick==179 and not r.logged then
    r.logged=true
    local states={}
    for k,_ in pairs(r.states) do table.insert(states,k) end
    table.sort(states)
    f:write(case..'\\t'..table.concat(states,',')..'\\t'..r.damage..'\\t'..tostring(r.charm)..'\\t'..r.spawn..'\\t'..r.helperDistance..'\\t'..r.helpers..'\\t'..r.power..'\\t'..tostring(r.aura)..'\\t'..tostring(r.marker)..'\\t'..tostring(r.invalidMarker)..'\\t'..tostring(r.lateMarker)..'\\t'..r.dashTravel..'\\n')
    f:flush()
  end
end)
'''.replace('CASECOUNT',str(len(scenarios)))
module_text=module_text.replace('STARTPOSITIONS', '{'+','.join(str(-c['facing']*c['distance']/2) for c in scenarios)+'}')
if capture_dir:
    module_text="modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(Path(capture_dir).resolve())+'/')+")\n"+module_text
    module_text=module_text.replace('if tick==179 and not r.logged then', 'if tick >= 10 and tick <= 150 and tick % 4 == 0 and not r.logged then screenshot() end\n  if tick==179 and not r.logged then')
module.write_text(module_text)
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
(engine/'eida_checks.tsv').write_text('')
debug_path=engine/'external/script/debug.lua'
debug_original=debug_path.read_text()
debug_path.write_text(debug_original+"\ndofile('external/mods/eida_checks.lua')\n")
try:
    run=subprocess.run([str(engine/'Ikemen_GO_Linux'),'-p1','EidaCheck','-p1.ai','0','-p2','EidaDummy','-p2.ai','0','-p1.power','3000','-rounds','1','-time','300']+(['-speed','0'] if capture_dir else ['-speedtest'])+['-nosound','-log','eida_moveset_engine.log'],cwd=engine,env=env,capture_output=True,text=True,timeout=60)
    print(run.stdout);print(run.stderr)
    if run.returncode:raise RuntimeError(f'engine exited {run.returncode}')
finally:
    debug_path.write_text(debug_original)
    # Disable the module while keeping the fixture and its logs for inspection.
    if module.exists():module.rename(module.with_name('-eida_checks.lua'))

lines=(engine/'eida_checks.tsv').read_text().splitlines()
# Quick-VS may replay the fixture after a drawn round; retain the first
# completed record of every numbered scenario, requiring the full set.
first_records={}
for line in lines:
    first_records.setdefault(int(line.split('\t',1)[0]),line)
assert sorted(first_records)==list(range(len(scenarios))),sorted(first_records)
lines=[first_records[i] for i in range(len(scenarios))]
failures=[];report=[]
for line,case in zip(lines,scenarios):
    idx,states,damage,charm,spawn,distance,helpers,power,aura,marker,invalid_marker,late_marker,dash_travel=line.split('\t')
    states=set(map(int,states.split(',')));damage=int(damage);spawn=float(spawn);distance=float(distance);power=int(power)
    failures_here=[]
    if case['kind']=='empty':
        if case['state'] in states:failures_here.append('spent unavailable energy')
    else:
        if case['state'] not in states:failures_here.append('command failed')
        if power > 3000-case['cost']:failures_here.append('energy was not spent')
    if case['kind']=='move' and case['mode'] is not None:
        if damage<=0:failures_here.append('assist did not hit')
        if not 0<=spawn<=28:failures_here.append('assist did not emerge beside Eida')
        if case['distance']>70 and distance<45:failures_here.append('assist did not travel')
    if case['kind']=='move' and case['state'] in (1200,1300,1350) and damage<=0:
        failures_here.append('counter did not trigger on an incoming collision')
    if case['kind']=='move' and case['state'] in (1100,1120) and charm!='true':
        # Anti-air is tested against a standing dummy separately: a miss is valid.
        if case['state']==1100:failures_here.append('heart did not charm on contact')
    if case['kind']=='block' and charm=='true':failures_here.append('charm bypassed block')
    if case['kind']=='move' and case['state']==1100 and marker!='true':failures_here.append('confirmed charm marker absent')
    if case['kind'] in ('block','charmmiss') and marker=='true':failures_here.append('charm marker appeared without a hit')
    if invalid_marker=='true':failures_here.append('charm marker outlived stun')
    if late_marker=='true':failures_here.append('charm helper did not expire')
    if case['kind']=='dash' and (float(dash_travel)<10 or 200 not in states):failures_here.append('dash failed to move or cancel into attack')
    if case['kind']=='aircombo' and not {600,610,620}.issubset(states):failures_here.append('aerial hitpause chain failed')
    if case['kind']=='charmmiss' and charm=='true':failures_here.append('heart charmed outside its collision')
    if case['kind']=='miss' and damage>0:failures_here.append('assist hit airborne target outside collision')
    if case['kind']=='combo' and (case['state'] not in states or damage<100):failures_here.append('normal chain failed')
    if case['kind']=='aura' and aura!='true':failures_here.append('aura absent')
    row=dict(case=case,states=sorted(states),damage=damage,spawn_distance=spawn,travel_distance=distance,minimum_power=power,charm_marker=marker=='true',dash_travel=float(dash_travel),failures=failures_here)
    report.append(row)
    print(('FAIL' if failures_here else 'PASS'),case['name'],case['facing'],row)
    failures+=failures_here
out=ROOT/'previews'/('engine_visual_checks.json' if capture_dir else 'engine_moveset_checks.json');out.write_text(json.dumps(report,indent=2)+'\n')
assert not failures,failures
print(f'PASSED: {len(scenarios)} raw-input/collision scenarios. Report: {out}')
