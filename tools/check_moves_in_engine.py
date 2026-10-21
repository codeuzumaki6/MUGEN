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
base_moves=list(scenarios)
scenarios += [
    dict(name='X chain',button='a',direction='N',state=203,cost=0,mode=2,facing=1,distance=40,kind='combo'),
    dict(name='Charm blocked',button='b',direction='D',state=1100,cost=500,mode=None,facing=1,distance=120,kind='block'),
    dict(name='Assist finite miss',button='a',direction='F',state=1000,cost=500,mode=0,facing=1,distance=120,kind='miss'),
    dict(name='Insufficient energy',button='z',direction='N',state=1060,cost=1500,mode=5,facing=1,distance=120,kind='empty'),
    dict(name='Awakening',button='s',direction='D',state=4000,cost=3000,mode=None,facing=1,distance=120,kind='aura'),
]
for case in base_moves:
    if case['direction'] in ('F','B'):
        scenarios.append({**case,'name':case['name']+' diagonal shortcut','shortcut':True})
for button,state in [('b',211),('c',221)]:
    scenarios.append(dict(name=f'{button} normal chain',button=button,direction='N',state=state,cost=0,mode=None,facing=1,distance=40,kind='combo'))
scenarios.append({**scenarios[10],'name':'RT during awakening','kind':'awakened'})
for facing in (1,-1):
    scenarios.append(dict(name='Forward dash and attack',button='a',direction='N',state=100,cost=0,mode=None,facing=facing,distance=160,kind='dash'))
    scenarios.append(dict(name='Aerial X Y B during hitpause',button='a',direction='N',state=620,cost=0,mode=None,facing=facing,distance=36,kind='aircombo'))
scenarios.append(dict(name='Charm finite miss',button='b',direction='D',state=1100,cost=500,mode=None,facing=1,distance=120,kind='charmmiss'))
for face in (1,-1):
    for button,state in [('b',211),('c',221)]:
        scenarios.append(dict(name='Mixed X '+button,button='a',follow_button=button,direction='N',state=state,cost=0,mode=None,facing=face,distance=36,kind='mixed'))
scenarios.append(dict(name='Higher neutral jump',button='U',direction='N',state=50,cost=0,mode=None,facing=1,distance=120,kind='jump'))
for follow,state,cost in [('b',1100,500),('z',1160,1500)]:
    scenarios.append(dict(name='X into Down '+follow,button='a',follow_button=follow,direction='N',state=state,cost=cost,mode=None,facing=1,distance=36,kind='specialcancel'))
for face in (1,-1):
    for button,follow,state in [('b','a',231),('c','b',232)]:
        scenarios.append(dict(name='Daemon branch '+button+' '+follow,button=button,follow_button=follow,
            direction='N',state=state,cost=0,mode=None,facing=face,distance=36,kind='daemonbranch'))
    scenarios.append(dict(name='Charm into Daemon',button='b',direction='D',state=234,cost=750,
                          mode=None,facing=face,distance=120,kind='charmfollow'))
    scenarios.append(dict(name='Natural launcher pursuit',button='a',direction='D',state=600,cost=500,
                          mode=None,facing=face,distance=100,kind='pursuit'))
    for button,follow,state in [('b','a',210),('c','b',220)]:
        scenarios.append(dict(name='Guard stops Daemon branch '+button,button=button,follow_button=follow,
            direction='N',state=state,cost=0,mode=None,facing=face,distance=36,kind='branchblocked'))
    for kind in ('followblocked','followmiss'):
        scenarios.append(dict(name='Charm '+kind,button='b',direction='D',state=1100,cost=500,
            mode=None,facing=face,distance=120,kind=kind))
    scenarios.append(dict(name='Interrupt assist at Eida',button='a',direction='F',state=1000,cost=500,
        mode=None,facing=face,distance=120,kind='interrupted'))
    scenarios.append(dict(name='Strike Daemon without Eida',button='a',direction='F',state=1000,cost=500,
        mode=None,facing=face,distance=120,kind='assistonlyhit'))
ultimate_only=os.environ.get('EIDA_ULTIMATE_CHECK')=='1'
recovery_only=os.environ.get('EIDA_RECOVERY_CHECK')=='1'
CASE_TICKS=560 if ultimate_only else 280 if recovery_only else 180
if ultimate_only:
    scenarios=[]
    for face in (1,-1):
        for kind in ('ultimatehit','ultiblock','ultimiss','ultifar'):
            scenarios.append(dict(name=kind,button='x',direction='N',state=3000,cost=3000,mode=None,facing=face,distance=340 if kind=='ultifar' else 120,kind=kind))
    scenarios.append(dict(name='Ultimate empty',button='x',direction='N',state=3000,cost=3000,mode=None,facing=1,distance=120,kind='empty'))
if recovery_only:
    scenarios=[]
    for face in (1,-1):
        for variant in ('sweep','bounce','airbounce'):
            scenarios.append(dict(name='Recovery '+variant,button='a',direction='N',state=5120,
                cost=0,mode=None,facing=face,distance=40,kind='knockdown',variant=variant))
if os.environ.get('EIDA_SENRIGAN_IDLE_CHECK')=='1':
    scenarios=[dict(name='Senrigan sin ataque',button='b',direction='B',state=1200,cost=1000,mode=None,facing=face,distance=120,kind='counterwait') for face in (1,-1)]
if os.environ.get('EIDA_TEST_CASES'):
    names=json.loads(os.environ['EIDA_TEST_CASES'])
    scenarios=[c for c in scenarios if c['name'] in names]
if os.environ.get('EIDA_REVIEW_FACING'):
    scenarios=[c for c in scenarios if c['facing']==int(os.environ['EIDA_REVIEW_FACING'])]
capture_dir=os.environ.get('EIDA_CAPTURE')
if capture_dir:
    requested=os.environ.get('EIDA_CAPTURE_CASES')
    if requested:
        names=json.loads(requested)
        selected=[next(c for c in scenarios if c['name']==name and c['facing']==1) for name in names]
        scenarios=selected
    else:
        scenarios=[scenarios[0],next(c for c in scenarios if c['kind']=='aura')]
    Path(capture_dir).mkdir(parents=True,exist_ok=True)


def ctrl(label,typ,trigger,body):
    return f'\n[State -2, CHECK {label}]\ntype = {typ}\ntriggerall = IsHelper = 0\ntriggerall = RoundState = 2\ntrigger1 = {trigger}\nignorehitpause = 1\n{body}\n'


clock=ctrl('clock','VarAdd','1','v = 58\nvalue = 1')
fixture=clock
other=clock
for idx,case in enumerate(scenarios):
    base=idx*CASE_TICKS
    at=lambda tick:f'Var(58) = {base+tick}'
    face=case['facing']; distance=case['distance'];root_x=-face*distance/2; target_x=face*distance/2
    for who,text,x,desired in [('root',fixture,root_x,face),('dummy',other,target_x,-face)]:
        text+=ctrl(f'case {idx}','VarSet',at(1),f'v = 59\nvalue = {idx}')
        text+=ctrl('reset pos','PosSet',at(1),f'x = {x}\ny = 0')
        text+=ctrl('reset vel','VelSet',at(1),'x = 0\ny = 0')
        text+=ctrl('reset fall flag','HitFallSet',at(1),'value = 0')
        text+=ctrl('reset face','Turn',at(1)+f' && Facing != {desired}','')
        text+=ctrl('reset life','LifeSet',at(1),'value = 1000')
        text+=ctrl('reset power','PowerSet',at(1),f'value = {0 if case["kind"]=="empty" else 3000}')
        text+=ctrl('reset awakening','VarSet',at(1),'v = 40\nvalue = 0')
        text+=ctrl('reset pursuit input flag','VarSet',at(1),'v = 57\nvalue = 0')
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
    presses=[220] if case['kind']=='knockdown' else [22,32,46,60] if case['kind']=='combo' else [press]
    for tick in presses:
        fixture+=ctrl('button input','AssertInput',at(tick),f'flag = {button}')
    if case['kind']=='knockdown':
        if case['variant']=='airbounce':
            fixture+=ctrl('airborne victim position','PosSet',at(15),'y = -70')
            fixture+=ctrl('airborne victim velocity','VelSet',at(15),'y = -2')
            fixture+=ctrl('airborne victim state','ChangeState',at(15),'value = 50\nctrl = 0')
        other+=ctrl('real incoming knockdown','ChangeState',at(20),
                    f'value = {9700 if case["variant"]=="sweep" else 9701}\nctrl = 0')
    if case['kind']=='mixed':
        follow=case['follow_button']
        fixture+=ctrl('mixed branch in hitpause','AssertInput',f'Var(59) = {idx} && StateNo = 200 && MoveHit && HitPauseTime = 4',f'flag = {follow}')
        fixture+=ctrl('mixed finisher in hitpause','AssertInput',f'Var(59) = {idx} && StateNo = {210 if follow=="b" else 220} && MoveContact && HitPauseTime = 4',f'flag = {follow}')
    if case['kind']=='specialcancel':
        trigger=f'Var(59) = {idx} && StateNo = 200 && MoveHit && HitPauseTime = 4'
        fixture+=ctrl('special down in hitpause','AssertInput',trigger,'flag = D')
        fixture+=ctrl('special button in hitpause','AssertInput',trigger,f'flag = {case["follow_button"]}')
    if case['kind']=='daemonbranch':
        starter=210 if case['button']=='b' else 220
        trigger=f'Var(59) = {idx} && StateNo = {starter} && MoveHit && HitPauseTime = 4'
        fixture+=ctrl('confirmed Daemon branch','AssertInput',trigger,f'flag = {case["follow_button"]}')
    if case['kind']=='branchblocked':
        starter=case['state']
        trigger=f'Var(59) = {idx} && StateNo = {starter} && MoveGuarded && HitPauseTime = 4'
        fixture+=ctrl('try Daemon branch on guard','AssertInput',trigger,f'flag = {case["follow_button"]}')
    if case['kind'] in ('charmfollow','followblocked','followmiss'):
        fixture+=ctrl('queue confirmed charm followup','AssertInput',f'Var(59) = {idx} && StateNo = 1100 && Time = 12','flag = a')
    if case['kind'] in ('interrupted','assistonlyhit'):
        incoming_distance=70 if case['kind']=='assistonlyhit' else 36
        other+=ctrl('approach exposed assist','PosSet',at(32),f'x = (P2,Pos X) + {face*incoming_distance}\ny = 0')
        other+=ctrl('interrupt with an actual punch','ChangeState',at(34),'value = 9702\nctrl = 0')
    if case['kind']=='pursuit':
        fixture+=ctrl('up after helper hit','AssertInput',f'Var(59) = {idx} && NumHelper(1001)>0 && (Helper(1001),MoveHit)','flag = U')
        trigger=f'Var(59) = {idx} && StateNo = 50 && Time = 2 && Var(57) = 0'
        fixture+=ctrl('natural aerial attack','AssertInput',trigger,'flag = a')
        fixture+=ctrl('only one pursuit attack','VarSet',trigger,'v = 57\nvalue = 1')
    if case['state'] in (1200,1300,1350) and case['kind']!='counterwait':
        other+=ctrl('place incoming strike','PosSet',at(36),f'x = (P2,Pos X) + {face*36}\ny = 0')
        other+=ctrl('incoming strike','ChangeState',at(38),'value = 210\nctrl = 0')
    if case['kind'] in ('block','ultiblock','branchblocked','followblocked'):
        other+=ctrl('hold guard','AssertInput',f'Var(58) = [{base+15},{base+120}]',f'flag = {"R" if face==1 else "L"}')
        if case['kind']=='branchblocked' and case['button']=='c':
            other+=ctrl('crouch to guard the low starter','AssertInput',f'Var(58) = [{base+15},{base+120}]','flag = D')
    if case['kind'] in ('miss','charmmiss','ultimiss','followmiss'):
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
            fixture+=ctrl('press next button inside hitpause','AssertInput',f'Var(59) = {idx} && StateNo = {state} && MoveContact && HitPauseTime = 5',f'flag = {button}')

# Dismiss any helper left over across fixture resets.
fixture+='''\n[State -2, CHECK helper cleanup]
type = DestroySelf
triggerall = IsHelper
trigger1 = Root,Var(58) % CASE_TICKS = [1,3]
ignorehitpause = 1
'''
fixture=fixture.replace('CASE_TICKS',str(CASE_TICKS))
if os.environ.get('EIDA_DEBUG_INPUT'):
    fixture+=ctrl('trace mixed inputs','PrintToConsole','StateNo = [200,202]', 'text = "INPUT %d var=%d a=%d b=%d c=%d"\nparams = Var(58),Var(27),command = "a",command = "b",command = "c"')
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

if recovery_only:
    # Test-only attacks collide normally. Never force Eida into a get-hit or
    # get-up state; that would hide a broken transition in her recovery path.
    attacks=''
    for state,animation,bounce,ground_type in [(9700,440,0,'Trip'),(9701,210,-4,'High')]:
        attacks+=f'''\n[Statedef {state}]
type = S
movetype = A
physics = S
anim = {animation}
ctrl = 0
velset = 0,0
[State {state}, Real knockdown collision]
type = HitDef
trigger1 = Time = 0
attr = S, NA
damage = 60,0
hitflag = MAF
guardflag = MA
pausetime = 6,8
ground.type = {ground_type}
animtype = Hard
ground.hittime = 18
ground.velocity = -2,-5
air.velocity = -2,-5
fall = 1
fall.recover = 0
fall.yvelocity = {bounce}
sparkno = -1
hitsound = 5,2
[State {state}, Finish]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 0
'''
    with (dummy/'kfm.cns').open('a') as file:file.write(attacks)

if any(c['kind'] in ('interrupted','assistonlyhit') for c in scenarios):
    # Fast fixture strike: real visible hitbox collision, never a forced Eida state.
    with (dummy/'kfm.air').open('a') as file:file.write('''
[Begin Action 9702]
Clsn2Default: 1
 Clsn2[0] = -12,-90,12,0
Clsn1Default: 1
 Clsn1[0] = 8,-65,50,-20
200,2,0,0,6
''')
    with (dummy/'kfm.cns').open('a') as file:file.write('''
[Statedef 9702]
type = S
movetype = A
physics = S
anim = 9702
ctrl = 0
velset = 0,0
[State 9702, Actual interruption collision]
type = HitDef
trigger1 = Time = 0
attr = S, NA
damage = 50,0
guardflag = MA
hitflag = MAF
pausetime = 6,8
ground.hittime = 16
ground.velocity = -2
air.velocity = -2,-3
sparkno = -1
[State 9702, Recover]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 0
''')

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
  local case = math.floor((clock-1)/CASE_TICKS)
  local tick = (clock-1)%CASE_TICKS+1
  if case >= CASECOUNT then player(2); setLife(100); player(1); setTime(0); return end
  if rows[case] == nil then rows[case] = {states={}, damage=0, received=0, previousHelpers=0, activeAtHit=false, lingered=false, latestHelperTick=0, charm=false, spawn=-1, helperDistance=0, helpers=0, power=3000, aura=false, marker=false, invalidMarker=false, lateMarker=false, dashTravel=0, apex=0, victimEnd=0} end
  local r=rows[case]
  if tick > 4 then
    r.states[stateNo()]=true
    r.received=math.max(r.received,1000-life())
    if r.received>0 and r.interruptedTick==nil then
      r.interruptedTick=tick
      r.activeAtHit=r.previousHelpers>0
    end
    if r.interruptedTick~=nil and tick>r.interruptedTick+1 and numHelper(1001)>0 then r.lingered=true end
    r.previousHelpers=numHelper(1001)
    r.power=math.min(r.power,power())
    local x=posX()
    r.apex=math.min(r.apex,posY())
    if stateNo()==100 then r.dashTravel=math.max(r.dashTravel, math.abs(x-(STARTPOSITIONS)[case+1])) end
    r.helpers=math.max(r.helpers,numHelper(1001))
    if numHelper(1001)>0 then r.latestHelperTick=tick end
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
        -- Hit resolution can follow the marker's update in this same frame.
        if stateNo()~=1105 then
          r.markerLag=(r.markerLag or 0)+1
          if r.markerLag>1 then r.invalidMarker=true end
        else r.markerLag=0 end
      end
      player(1)
    end
    if tick>130 and numHelper(1101)>0 then r.lateMarker=true end
    player(2)
    r.damage=math.max(r.damage,1000-life())
    if stateNo()==1105 then r.charm=true end
    player(1)
  end
  if tick==CASE_TICKS-1 and not r.logged then
    r.logged=true
    player(2); r.victimEnd=stateNo(); player(1)
    local states={}
    for k,_ in pairs(r.states) do table.insert(states,k) end
    table.sort(states)
    f:write(case..'\\t'..table.concat(states,',')..'\\t'..r.damage..'\\t'..tostring(r.charm)..'\\t'..r.spawn..'\\t'..r.helperDistance..'\\t'..r.helpers..'\\t'..r.power..'\\t'..tostring(r.aura)..'\\t'..tostring(r.marker)..'\\t'..tostring(r.invalidMarker)..'\\t'..tostring(r.lateMarker)..'\\t'..r.dashTravel..'\\t'..r.apex..'\\t'..r.victimEnd..'\\t'..r.received..'\\t'..numHelper(1001)..'\\t'..tostring(r.activeAtHit)..'\\t'..tostring(r.lingered)..'\\t'..r.latestHelperTick..'\\n')
    f:flush()
  end
end)
'''.replace('CASECOUNT',str(len(scenarios)))
module_text=module_text.replace('CASE_TICKS',str(CASE_TICKS))
if recovery_only:
    module_text=module_text.replace('player(2)\n    r.damage=', 'player(1)\n    r.damage=')
module_text=module_text.replace('STARTPOSITIONS', '{'+','.join(str(-c['facing']*c['distance']/2) for c in scenarios)+'}')
if capture_dir:
    module_text="modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(Path(capture_dir).resolve())+'/')+")\n"+module_text
    module_text="local cues=assert(io.open('eida_capture_cues.tsv','w'))\n"+module_text
    module_text=module_text.replace('local r=rows[case]', "local r=rows[case]\n  if stateNo()~=r.lastState then cues:write(case..'\\t'..tick..'\\t'..stateNo()..'\\n'); cues:flush(); r.lastState=stateNo() end")
    log_marker=f'if tick=={CASE_TICKS}-1 and not r.logged then'
    capture_end=548 if ultimate_only else 260 if recovery_only else 150
    module_text=module_text.replace(log_marker, f'if tick >= 10 and tick <= {capture_end} and tick % 4 == 0 and not r.logged then screenshot() end\n  '+log_marker)
live_capture=os.environ.get('EIDA_LIVE_CAPTURE')
record_audio=os.environ.get('EIDA_RECORD_AUDIO')
if live_capture:
    directory=str(Path(live_capture).resolve())+'/'
    Path(directory).mkdir(parents=True,exist_ok=True)
    observer="modifyGameOption('Config.ScreenshotFolder',"+json.dumps(directory)+")\nlocal folder="+json.dumps(directory)+"\n"
    observer+='''
local live=assert(io.open(folder..'trace.tsv','w'))
local images=assert(io.open(folder..'frames.tsv','w'))
local sound=assert(io.open(folder..'audio.tsv','w'))
local rendered=0;local cap={index=0,pending=nil,last=-1000};local entered={}
local expected=EXPECTED
hook.add('loop','eida_live_review',function()
 if not player(1) or roundState()~=2 or var(58)<1 then return end
 rendered=rendered+1
 local case=math.floor((var(58)-1)/CASETICKS)
 if case>=#expected then return end
 local st=stateNo();local tm=time()-1
 local vals={rendered,case,var(58),st,tm,numExplod(8560),numExplod(8561),numExplod(8600),numExplod(8100)+numExplod(8101)+numExplod(8102),numHelper(1001),power()}
 for i,v in ipairs(vals) do live:write(tostring(v)..(i==#vals and string.char(10) or string.char(9))) end;live:flush()
 if not entered[case] and st==expected[case+1] and (st~=3000 or tm>=2) then sound:write(rendered..string.char(9)..case..string.char(9)..tostring(21)..string.char(10));sound:flush();entered[case]=true end
 if cap.pending~=nil then
  local png=io.open(folder..string.format('Ikemen_GO%03d.png',cap.index),'rb')
  if png then png:close();images:write(cap.index..string.char(9)..cap.pending..string.char(10));images:flush();cap.index=cap.index+1;cap.pending=nil end
 end
 if rendered>=12 and rendered-cap.last>=4 and cap.pending==nil then screenshot();cap.pending=rendered;cap.last=rendered end
end)
'''.replace('EXPECTED','{'+','.join(str(c['state']) for c in scenarios)+'}').replace('CASETICKS',str(CASE_TICKS))
    module_text+=observer
module_text="modifyGameOption('Debug.RetryLoadOnError',false)\n"+module_text
module.write_text(module_text)
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
if record_audio:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=record_audio,SDL_DISKAUDIODELAY='46')
(engine/'eida_checks.tsv').write_text('')
if capture_dir:(engine/'eida_capture_cues.tsv').write_text('')
debug_path=engine/'external/script/debug.lua'
debug_original=debug_path.read_text()
debug_path.write_text(debug_original+"\ndofile('external/mods/eida_checks.lua')\n")
try:
    run=subprocess.run([str(engine/'Ikemen_GO_Linux'),'-p1','EidaCheck','-p1.ai','0','-p2','EidaDummy','-p2.ai','0','-p1.power','3000','-rounds','1','-time','300']+(['-speed','0'] if capture_dir or record_audio else ['-speedtest'])+([] if record_audio else ['-nosound'])+['-log','eida_moveset_engine.log'],cwd=engine,env=env,capture_output=True,text=True,timeout=120 if live_capture else 60)
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
    idx,states,damage,charm,spawn,distance,helpers,power,aura,marker,invalid_marker,late_marker,dash_travel,apex,victim_end,received,helpers_end,active_at_hit,lingered,latest_helper_tick=line.split('\t')
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
    if case['kind']=='move' and case['state'] in (1200,1300) and not 0<=spawn<=28:
        failures_here.append('physical counter did not summon Daemon beside Eida')
    if case['kind']=='counterwait' and (damage!=0 or int(helpers)!=0 or 1201 in states):failures_here.append('Senrigan attacked without an incoming hit')
    if case['kind']=='move' and case['state'] in (1100,1120) and charm!='true':
        # Anti-air is tested against a standing dummy separately: a miss is valid.
        if case['state']==1100:failures_here.append('heart did not charm on contact')
    if case['kind']=='move' and case['state'] in (1140,1150) and marker!='true':failures_here.append('new travelling charm did not connect')
    if case['kind']=='move' and case['state']==1160 and (damage<=0 or not 0<=spawn<=28):failures_here.append('combined opening did not approach and hit')
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
    if case['kind']=='mixed' and (case['state'] not in states or damage<100):failures_here.append('mixed hitpause route failed')
    if case['kind']=='specialcancel' and 200 not in states:failures_here.append('special skipped initial normal')
    if case['kind']=='specialcancel' and case['state']==1100 and marker!='true':failures_here.append('normal into charm failed to collide')
    if case['kind']=='specialcancel' and case['state']==1160 and damage<60:failures_here.append('normal into combined opening failed')
    if case['kind']=='aura' and aura!='true':failures_here.append('aura absent')
    if case['kind']=='ultimatehit' and (3001 not in states or damage!=350):failures_here.append('ultimate did not confirm and deal its finite damage')
    if case['kind']=='ultimatehit' and int(victim_end) in (3010,3011):failures_here.append('ultimate did not release victim')
    if case['kind'] in ('ultiblock','ultimiss','ultifar') and (3001 in states or damage!=0):failures_here.append('ultimate hit was guaranteed or cinematic started without contact')
    if case['kind']=='jump' and not 40<=-float(apex)<=55:failures_here.append('jump height outside intended range')
    if case['kind']=='knockdown':
        if damage<=0:failures_here.append('fixture did not actually hit Eida')
        if 5110 not in states:failures_here.append('did not reach lying-down state')
        if 5120 not in states:failures_here.append('never started getting up')
        if 200 not in states:failures_here.append('could not attack after getting up')
    if case['kind']=='daemonbranch':
        if damage<100 or not 0<=spawn<=28:failures_here.append('Daemon combo branch failed to connect')
    if case['kind']=='charmfollow':
        if marker!='true' or damage<=0 or not 0<=spawn<=28:failures_here.append('confirmed charm followup failed')
    if case['kind']=='pursuit':
        if 204 not in states or 600 not in states or damage<=68:failures_here.append('natural aerial pursuit did not connect after launcher')
    if case['kind']=='branchblocked':
        if {231,232}&states or int(helpers)!=0:failures_here.append('Daemon followup bypassed normal guard')
        if damage>8:failures_here.append('normal guard did not prevent full damage')
    if case['kind'] in ('followblocked','followmiss'):
        if 234 in states or int(helpers)!=0 or marker=='true':failures_here.append('charm followup activated without a confirmed hit')
        if power!=2500:failures_here.append('unconfirmed followup spent extra energy')
    if case['kind']=='interrupted':
        if int(received)<=0:failures_here.append('fixture did not actually hit exposed Eida')
        if int(helpers)==0 or int(helpers_end)!=0:failures_here.append('offensive Daemon did not disappear after Eida was hit')
        if active_at_hit!='true' or lingered=='true':failures_here.append('active assist was not interrupted within one tick of the hit')
    if case['kind']=='assistonlyhit':
        if int(received)!=0:failures_here.append('fixture also hit Eida')
        if int(helpers)==0 or not 32<=int(latest_helper_tick)<=36:failures_here.append('struck helper failed to terminate at impact')
    row=dict(case=case,states=sorted(states),damage=damage,received_damage=int(received),helpers_end=int(helpers_end),active_assist_on_hit=active_at_hit=='true',assist_lingered_after_hit=lingered=='true',latest_helper_tick=int(latest_helper_tick),spawn_distance=spawn,travel_distance=distance,minimum_power=power,charm_marker=marker=='true',dash_travel=float(dash_travel),jump_apex=float(apex),victim_end_state=int(victim_end),failures=failures_here)
    report.append(row)
    print(('FAIL' if failures_here else 'PASS'),case['name'],case['facing'],row)
    failures+=failures_here
out=ROOT/'previews'/('Eida_live_review_checks.json' if live_capture else 'Eida_Senrigan_idle_checks.json' if os.environ.get('EIDA_SENRIGAN_IDLE_CHECK') else 'engine_visual_checks.json' if capture_dir else 'engine_recovery_checks.json' if recovery_only else 'engine_ultimate_checks.json' if ultimate_only else 'engine_moveset_checks.json');out.write_text(json.dumps(report,indent=2)+'\n')
assert not failures,failures
print(f'PASSED: {len(scenarios)} raw-input/collision scenarios. Report: {out}')
