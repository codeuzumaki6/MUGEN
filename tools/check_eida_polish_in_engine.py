#!/usr/bin/env python3
"""Exercise raw inputs, presentation lifetimes and a real KO in engine copies."""
from pathlib import Path
import json,os,re,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
ENGINE=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly').resolve()
CAPTURE=os.environ.get('EIDA_POLISH_CAPTURE')
WIN=os.environ.get('EIDA_WIN_CHECK')=='1'
TICKS=int(os.environ.get('EIDA_POLISH_TICKS','260'))
cases=[]
for face in [1,-1]:
    for kind,dist in [('charge',180),('fullcharge',180),('charge_hit',36),('run',280),('run_attack',220),('land',180),('finisher',36),('daemon',120),('guard',36),('miss',220),('awakening',180)]:
        cases.append(dict(kind=kind,face=face,distance=dist))
if WIN:cases=[dict(kind='win',face=int(os.environ.get('EIDA_WIN_FACING','1')),distance=36)]
if os.environ.get('EIDA_POLISH_CASES'):
    wanted=json.loads(os.environ['EIDA_POLISH_CASES']);cases=[c for c in cases if c['kind'] in wanted]
if CAPTURE:cases=[c for c in cases if c['face']==1];Path(CAPTURE).mkdir(parents=True,exist_ok=True)
assert cases
char=ENGINE/'chars/EidaPolishCheck';dummy=ENGINE/'chars/EidaPolishDummy'
shutil.copytree(ROOT/'Eida',char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(char/'Eida.def',char/'EidaPolishCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'EidaPolishDummy.def')

def ctl(typ,condition,params):
    return f'\n[State -2, Fixture only]\ntype = {typ}\ntriggerall = IsHelper = 0\ntriggerall = RoundState = 2\ntrigger1 = {condition}\nignorehitpause = 1\n{params}\n'

p1=ctl('VarAdd','1','v = 58\nvalue = 1')
p2=ctl('VarSet','NumEnemy > 0','v = 58\nvalue = EnemyNear,Var(58)')
for idx,c in enumerate(cases):
    base=idx*TICKS;at=lambda n:f'Var(58) = {base+n}';window=lambda a,b:f'Var(58) = [{base+a},{base+b}]'
    kind=c['kind'];face=c['face']
    for side in [1,2]:
        block=ctl('PosSet',at(1),f'x = {(-1 if side==1 else 1)*face*c["distance"]/2}\ny = 0')
        block+=ctl('VelSet',at(1),'x = 0\ny = 0')+ctl('HitFallSet',at(1),'value = 0')
        block+=ctl('Turn',at(1)+f' && Facing != {face if side==1 else -face}','')
        block+=ctl('LifeSet',at(1),f'value = {24 if side==2 and WIN else 1000}')
        block+=ctl('PowerSet',at(1),f'value = {2900 if kind=="fullcharge" else 0 if kind.startswith("charge") else 3000}')
        block+=ctl('VarSet',at(1),'v = 40\nvalue = 0')
        block+=ctl('ChangeState',at(1),'value = 0\nctrl = 1')
        if side==1:p1+=block
        else:p2+=block
    if kind in ['charge','charge_hit','fullcharge']:
        p1+=ctl('AssertInput',window(20,92),'flag = s')
        if kind=='charge_hit':p2+=ctl('ChangeState',at(40),'value = 9700\nctrl = 0')
    elif kind in ['run','run_attack']:
        forward='R' if face==1 else 'L'
        p1+=ctl('AssertInput',at(20),f'flag = {forward}')+ctl('AssertInput',window(23,48),f'flag = {forward}')
        if kind=='run_attack':p1+=ctl('AssertInput',at(38),'flag = a')
    elif kind=='land':p1+=ctl('AssertInput',at(20),'flag = U')
    elif kind=='daemon':p1+=ctl('AssertInput',at(22),'flag = z')
    elif kind=='awakening':p1+=ctl('AssertInput',window(20,24),'flag = D')+ctl('AssertInput',at(22),'flag = s')
    else:
        p1+=ctl('AssertInput',at(22),f'flag = {"a" if WIN else "b"}')
        if kind in ['finisher','guard']:
            p1+=ctl('AssertInput',f'Var(58) > {base+22} && Var(58) < {base+100} && StateNo = 210 && MoveContact && HitPauseTime = 4','flag = b')
        if kind=='guard':p2+=ctl('AssertInput',window(15,150),f'flag = {"R" if face==1 else "L"}')
    if not WIN:p2+=ctl('LifeSet',window(2,TICKS-1),'value = IfElse(Life < 10,10,Life)')
for path,fixture in [(char/'Eida.cns',p1),(dummy/'kfm.cns',p2)]:
    text=path.read_text(encoding='latin-1')
    if '[Statedef -2]' in text:text=text.replace('[Statedef -2]','[Statedef -2]\n'+fixture,1)
    else:text+='\n[Statedef -2]\n'+fixture
    path.write_text(text,encoding='latin-1')
with (dummy/'kfm.cns').open('a') as f:f.write('''
[Statedef 9700]
type = S
movetype = A
physics = S
anim = 210
ctrl = 0
velset = 0,0
[State 9700, Collision]
type = HitDef
trigger1 = Time = 0
attr = S,NA
damage = 50,0
hitflag = MAF
guardflag = MA
pausetime = 6,8
ground.hittime = 14
ground.velocity = -2
air.velocity = -2,-3
sparkno = -1
[State 9700, End]
type = ChangeState
trigger1 = Time >= 24
value = 0
ctrl = 0
''')

out=ENGINE/'eida_polish_trace.tsv';out.write_text('')
module='''modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('eida_polish_trace.tsv','w'))
local seen=-1;local frame=0;local lastState=-1;local lasttm=-1
CAPSETUP
hook.add('loop','eida_polish',function()
 if not player(1) or roundState()<2 then return end
 local clock=var(58)
 if not WINMODE and (roundState()~=2 or clock<1 or clock==seen) then return end
 if WINMODE and roundState()==2 and clock==seen then return end
 seen=clock;frame=frame+1
 local idx=WINMODE and 0 or math.floor((clock-1)/TICKS)
 local tick=WINMODE and frame or (clock-1)%TICKS+1
 if idx>=COUNT then player(2);setLife(100);player(1);setTime(0);return end
 local st=stateNo();local tm=time()-1
 local vals={idx,tick,roundState(),st,tm,spriteVar('group'),spriteVar('image'),numExplod(8550),numExplod(8552),numExplod(8551),numExplod(8553),power(),life(),posY(),numHelper(1001),numHelper(8301),screenPosX(),var(34)}
 local helperFinish=0
 if numHelper(1001)>0 and helper(1001) then helperFinish=numExplod(8553);player(1) end
 table.insert(vals,helperFinish)
 player(2);table.insert(vals,life());player(1);table.insert(vals,numExplod(8555))
 for i,v in ipairs(vals) do f:write(tostring(v)..(i==#vals and string.char(10) or string.char(9))) end;f:flush()
 CAPTURE
 lastState=st;lasttm=tm
end)
'''.replace('WINMODE','true' if WIN else 'false').replace('TICKS',str(TICKS)).replace('COUNT',str(len(cases)))
if CAPTURE:
    capdir=str(Path(CAPTURE).resolve())+'/'
    setup="modifyGameOption('Config.ScreenshotFolder',"+json.dumps(capdir)+")\nlocal capdir="+json.dumps(capdir)+"\nlocal cap={index=0,pending=nil,last=-1000}\nlocal frames=assert(io.open(capdir..'frames.tsv','w'))\nlocal cues=assert(io.open(capdir..'audio.tsv','w'))\nlocal function cue(t,n) cues:write(t..string.char(9)..n..string.char(10));cues:flush() end\n"
    capture='''
 if st~=lastState and st==500 then cue(tick,17) end
 if st~=lastState and st==210 then cue(tick,0) end
 if st==180 and tm==12 and tm~=lasttm then cue(tick,18) end
 if st==100 and tm>0 and tm%12==0 and tm~=lasttm then cue(tick,20) end
 if st==52 and tm==1 and tm~=lasttm then cue(tick,20) end
 if vals[19]>0 and (cap.hfinish or 0)==0 then cue(tick,19) end
 cap.hfinish=vals[19]
 if vals[18]>0 and (cap.finish or 0)==0 then cue(tick,19) end
 cap.finish=vals[18]
 if cap.pending~=nil then
  local png=io.open(capdir..string.format('Ikemen_GO%03d.png',cap.index),'rb')
  if png then png:close();frames:write(cap.index..string.char(9)..cap.pending..string.char(10));frames:flush();cap.index=cap.index+1;cap.pending=nil end
 end
 if tick>=12 and tick<CAPTUREEND and tick-cap.last>=4 and cap.pending==nil then screenshot();cap.pending=tick;cap.last=tick end
'''.replace('CAPTUREEND','420' if WIN else str(TICKS-12))
    module=module.replace('CAPSETUP',setup).replace('CAPTURE',capture)
else:module=module.replace('CAPSETUP','').replace('CAPTURE','')
path=ENGINE/'external/mods/eida_polish_checks.lua';path.write_text(module)
debug=ENGINE/'external/script/debug.lua';original=debug.read_text();debug.write_text(original+"\ndofile('external/mods/eida_polish_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
audio=os.environ.get('EIDA_RECORD_AUDIO')
if audio:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=audio,SDL_DISKAUDIODELAY='46')
args=[str(ENGINE/'Ikemen_GO_Linux'),'-p1','EidaPolishCheck','-p1.ai','0','-p2','EidaPolishDummy','-p2.ai','0','-rounds','1','-time','300']
args+=['-speed','0'] if CAPTURE else ['-speedtest']
if not audio:args+=['-nosound']
try:
    run=subprocess.run(args,cwd=ENGINE,env=env,capture_output=True,text=True,timeout=100)
    if run.returncode:raise RuntimeError(run.stdout+run.stderr)
finally:
    debug.write_text(original);path.rename(path.with_name('-eida_polish_checks.lua'))
rows=[list(map(float,line.split())) for line in out.read_text().splitlines()]
reports=[]
for idx,c in enumerate(cases):
    data=[r for r in rows if int(r[0])==idx];assert data,c
    states={int(r[3]) for r in data};poses={(int(r[5]),int(r[6])) for r in data};bad=[];kind=c['kind']
    if kind.startswith('charge') or kind=='fullcharge':
        if not all((350,i) in poses for i in range(4)) and kind!='fullcharge':bad.append('charge cycle incomplete')
        if 500 not in states:bad.append('charge input failed')
        if any(r[8]>0 and r[3]!=500 and r[4]>2 for r in data):bad.append('charge motes outlived release/injury')
        if kind=='charge_hit' and min(r[12] for r in data)>=1000:bad.append('charge did not receive actual hit')
        if kind=='fullcharge' and max(r[11] for r in data)!=3000:bad.append('charge failed at full power')
        if data[-1][3]!=0:bad.append('charge did not release to idle')
    if kind in ['run','run_attack']:
        if 100 not in states or not any(r[7]>0 for r in data):bad.append('run or footwork dust absent')
        if kind=='run' and not {(351,i) for i in range(6)}<=poses:bad.append('run/brake poses incomplete')
        if kind=='run_attack' and 200 not in states:bad.append('could not cancel run into attack')
    if kind=='land':
        if not {40,50,52}<=states or not {(351,6),(351,7)}<=poses:bad.append('jump landing incomplete')
        if not any(r[3]==52 and r[7]>0 for r in data):bad.append('landing dust absent')
    if kind=='finisher':
        if 211 not in states or not any(r[10]>0 for r in data):bad.append('confirmed finisher absent')
        if min(r[19] for r in data)>900:bad.append('combo did not deal expected damage')
    if kind=='daemon':
        if 1060 not in states or not any(r[18]>0 for r in data):bad.append('Daemon final accent absent')
        if min(r[19] for r in data)>830:bad.append('Daemon assault incomplete')
        if data[-1][14]!=0:bad.append('Daemon did not expire')
    if kind in ['guard','miss'] and any(r[10]>0 for r in data):bad.append('finisher appeared without a hit')
    if kind=='miss' and min(r[19] for r in data)!=1000:bad.append('out-of-range attack hit')
    if kind=='awakening':
        if 4000 not in states or not any(r[15]>0 for r in data):bad.append('awakening absent')
        if not any(r[3]==0 and r[5]==0 for r in data):bad.append('awakening changed idle body')
    if kind=='win':
        win=[r for r in data if r[3]==180 and r[2]==4]
        if not win or min(r[19] for r in data)!=0:bad.append('no actual KO/victory')
        if not {(350,i) for i in range(4,8)}<=poses:bad.append('victory poses incomplete')
        if win and max(r[4] for r in win)<110:bad.append('victory ended early')
        if not any(r[20]>0 for r in win) or any(r[20]>0 and r[4]>30 for r in win):bad.append('victory accent missing or did not expire')
        # screenPosX uses the engine's 320-unit logical coordinate system.
        if any(not 42<=r[16]<=278 for r in win):bad.append('winner clipped outside viewport')
    report=dict(case=c,states=sorted(states),new_poses=sorted([list(p) for p in poses if p[0] in [350,351]]),damage=(24 if WIN else 1000)-min(r[19] for r in data),received_damage=1000-min(r[12] for r in data),max_foot_fx=max(r[7] for r in data),max_finish_fx=max(max(r[10],r[18]) for r in data),failures=bad)
    reports.append(report);print('FAIL' if bad else 'PASS',report)
destination=ROOT/'previews'/('Eida_polish_win_visual_checks.json' if CAPTURE and WIN else 'Eida_polish_visual_checks.json' if CAPTURE else 'Eida_polish_win_checks.json' if WIN else 'Eida_polish_checks.json')
destination.write_text(json.dumps(reports,indent=2)+'\n')
assert not any(r['failures'] for r in reports),reports
print('PASSED',len(reports),'presentation cases')
