#!/usr/bin/env python3
"""Raw-input and collision tests in disposable Ikemen character copies."""
from pathlib import Path
import json,os,re,shutil,subprocess,sys
from build_mamushi_runtime import MOVES

ROOT=Path(__file__).resolve().parents[1];ENGINE=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly').resolve()
CAP=os.environ.get('MAMUSHI_CAPTURE');AUDIO=os.environ.get('MAMUSHI_AUDIO');LOW=os.environ.get('MAMUSHI_LOW_LIFE')=='1';TICKS=int(os.environ.get('MAMUSHI_TICKS','640' if CAP else '1040'))
cases=[]
for face in [1,-1]:
    for name,button,d,state,cost in MOVES:cases.append(dict(name=name,kind='move',face=face,button=button,d=d,state=state,cost=cost,distance=50 if name in ['Guardia','Barrido','Retirada'] else 120 if d in ['F','B'] else 110))
    for button,base in [('a',200),('b',210),('c',220)]:
        cases.append(dict(name='Combo '+button,kind='combo',face=face,button=button,state=base+2,distance=44))
        cases.append(dict(name='Aire '+button,kind='air',face=face,button=button,state=600+['a','b','c'].index(button)*10+2,distance=36))
    for kind in ['walk','jump','diagonal','charge','focus','clone_auto','clone_independent','clone_limit','recovery','ultimate','ultiblock','ultimiss','ultifar','empty']:
        cases.append(dict(name=kind,kind=kind,face=face,distance=370 if kind=='ultifar' else 220 if kind in ['walk','jump','diagonal','charge','focus','clone_limit'] else 120))
if LOW:cases=[dict(name='low life ultimate',kind='ultimate',face=1,distance=120)]
HEALTH=os.environ.get('MAMUSHI_CLONE_HEALTH_CHECK')=='1'
if HEALTH:cases=[dict(name='clone_damage',kind='clone_damage',face=face,distance=120) for face in [1,-1]]
EXTRA=os.environ.get('MAMUSHI_EXTRA_CHECKS')=='1';CPU=os.environ.get('MAMUSHI_CPU_CHECK')=='1'
if EXTRA:
    cases=[]
    for face in [1,-1]:
        for name,button,d,state,cost in MOVES:
            if d in ['F','B']:cases.append(dict(name=name+' shortcut',kind='move',face=face,button=button,d=d,state=state,cost=cost,distance=120,shortcut=True))
        for route,final,damage in [('abc',222,164),('bca',202,170),('cab',212,166)]:cases.append(dict(name='Mixed '+route,kind='mixed',face=face,route=route,button=route[0],state=final,distance=44,expected=damage))
if CPU:cases=[dict(name='CPU',kind='cpu',face=1,distance=200)]
if os.environ.get('MAMUSHI_CASES'):
    wanted=json.loads(os.environ['MAMUSHI_CASES']);cases=[c for c in cases if c['name'] in wanted and (not CAP or c['face']==1)]
assert cases
char=ENGINE/'chars/MamushiCheck';dummy=ENGINE/'chars/MamushiDummy'
shutil.copytree(ROOT/'Mamushi',char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(char/'Mamushi.def',char/'MamushiCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'MamushiDummy.def')

def fctl(kind,when,params,helper=False):
    return f'\n[State -2, Fixture only]\ntype = {kind}\ntriggerall = {"IsHelper != 0" if helper else "IsHelper = 0"}\ntriggerall = RoundState = 2\ntrigger1 = {when}\nignorehitpause = 1\n{params}\n'
p1=fctl('VarAdd','1','v = 58\nvalue = 1')
p1+=fctl('DestroySelf',f'Root,Var(58) % {TICKS} = 1','',True)
p2=fctl('VarSet','NumEnemy > 0','v = 58\nvalue = EnemyNear,Var(58)')
for idx,case in enumerate(cases):
    base=idx*TICKS;face=case['face'];kind=case['kind'];distance=case['distance'];at=lambda x:f'Var(58) = {base+x}';window=lambda a,b:f'Var(58) = [{base+a},{base+b}]'
    for side in [1,2]:
        block=fctl('PosSet',at(1),f'x = {(-1 if side==1 else 1)*face*distance/2}\ny = 0')
        block+=fctl('VelSet',at(1),'x = 0\ny = 0')+fctl('Turn',at(1)+f' && Facing != {face if side==1 else -face}','')
        block+=fctl('LifeSet',at(1),f'value = {1000 if side==1 else 500 if LOW else 10000}')
        block+=fctl('PowerSet',at(1),f'value = {0 if kind in ["charge","empty"] else 3000}')
        for var in [12,35,40,41]:block+=fctl('VarSet',at(1),f'v = {var}\nvalue = 0')
        block+=fctl('ChangeState',at(1),'value = 0\nctrl = 1')
        if side==1:p1+=block
        else:p2+=block
    def press(tick,button):return fctl('AssertInput',at(tick),'flag = '+button)
    def motion(button,d,tick=28):
        forward='R' if face==1 else 'L';back='L' if face==1 else 'R'
        if d in ['F','B']:
            side=forward if d=='F' else back
            return fctl('AssertInput',window(tick-8,tick+1 if case.get('shortcut') else tick-3),'flag = D')+fctl('AssertInput',window(tick-5,tick+1),'flag = '+side)+press(tick,button)
        if d=='D':return fctl('AssertInput',window(tick-4,tick+1),'flag = D')+press(tick,button)
        return press(tick,button)
    if kind=='move':
        p1+=motion(case['button'],case['d'])
        if case['name']=='Guardia':p2+=fctl('ChangeState',at(43),'value = 9700\nctrl = 0')
    elif kind in ['combo','air','mixed']:
        if kind=='air':
            p1+=press(18,'U');p2+=fctl('ChangeState',at(20),'value = 9702\nctrl = 0')+fctl('PosSet',at(20),'y = -60')
        p1+=press(36 if kind=='air' else 26,case['button'])
        allowed='StateNo = [600,622]' if kind=='air' else 'StateNo = [200,221]'
        if kind=='mixed':
            first,second,last=case['route'];bases={'a':200,'b':210,'c':220}
            p1+=fctl('AssertInput',f'{window(30,160)} && StateNo={bases[first]} && Time>=4 && MoveHit && HitPauseTime=3','flag = '+second)
            p1+=fctl('AssertInput',f'{window(30,160)} && StateNo={bases[second]+1} && Time>=4 && MoveHit && HitPauseTime=3','flag = '+last)
        else:p1+=fctl('AssertInput',f'{window(30,160)} && ({allowed}) && Time >= 4 && MoveHit && HitPauseTime = 3','flag = '+case['button'])
    elif kind in ['walk','diagonal']:
        p1+=fctl('AssertInput',window(20,55),'flag = '+('R' if face==1 else 'L'))
        if kind=='diagonal':p1+=press(23,'U')
    elif kind=='jump':p1+=press(23,'U')
    elif kind=='charge':p1+=fctl('AssertInput',window(20,80),'flag = s')
    elif kind=='focus':p1+=motion('s','D')
    elif kind in ['clone_auto','clone_independent','clone_damage']:
        p1+=motion('z','D')
        if kind=='clone_independent':p2+=fctl('PosSet',at(99),f'x = (EnemyNear,Pos X)+{face*30}\ny = 0')+fctl('ChangeState',at(100),'value = 9700\nctrl = 0')
        if kind=='clone_damage':
            for tick in [95,135,175,215,255]:
                guard=at(tick)+' && (EnemyNear,NumHelper(9500))>0'
                p2+=fctl('PosSet',guard,f'x = (EnemyNear,Helper(9500),Pos X)+{face*25}\ny = 0')+fctl('ChangeState',at(tick+1),'value = 9700\nctrl = 0')
        else:p1+=fctl('AssertInput',window(60,90),'flag = '+('L' if face==1 else 'R'))
    elif kind=='clone_limit':
        for tick in [28,82,136,190,244,298,352,406]:
            p1+=fctl('PowerSet',at(tick-6),'value = 3000')+motion('z','D',tick)
    elif kind=='recovery':p2+=fctl('ChangeState',at(22),'value = 9701\nctrl = 0')+fctl('PosSet',window(19,35),f'x = {(-distance/2+36)*face}\ny = 0')
    elif kind in ['ultimate','ultiblock','ultimiss','ultifar','empty']:
        p1+=press(28,'x')
        if kind=='ultiblock':p2+=fctl('AssertInput',window(18,160),'flag = '+('R' if face==1 else 'L'))
        if kind=='ultimiss':p2+=fctl('ChangeState',at(20),'value = 9702\nctrl = 0')+fctl('PosSet',at(20),'y = -170')

for path,fixture in [(char/'Mamushi.cns',p1),(dummy/'kfm.cns',p2)]:
    text=path.read_text(encoding='latin-1')
    if '[Statedef -2]' in text:text=text.replace('[Statedef -2]','[Statedef -2]\n'+fixture,1)
    else:text+='\n[Statedef -2]\n'+fixture
    if path==dummy/'kfm.cns':text=re.sub(r'(?im)^life\s*=.*$',f'life = {500 if LOW else 10000}',text,count=1)
    path.write_text(text,encoding='latin-1')
with (dummy/'kfm.cns').open('a') as out:
    for n,fall in [(9700,False),(9701,True)]:
        out.write(f'''\n[Statedef {n}]
type = S
movetype = A
physics = S
anim = 400
ctrl = 0
velset = 0,0
[State {n}, Real strike]
type = HitDef
trigger1 = Time = 0
attr = S, NA
damage = 60,0
hitflag = MAF
guardflag = MA
pausetime = 5,8
ground.hittime = 18
ground.velocity = -2,{-6 if fall else 0}
air.velocity = -2,-4
fall = {int(fall)}
fall.recover = 0
sparkno = -1
[State {n}, Recover]
type = ChangeState
trigger1 = Time >= 24
value = 0
ctrl = 1
''')
    out.write('\n[Statedef 9702]\ntype = A\nmovetype = I\nphysics = N\nanim = 41\nvelset = 0,0\nctrl = 0\n[State 9702, Stay]\ntype = Null\ntrigger1 = 1\n')

module=ENGINE/'external/mods/mamushi_checks.lua';module.parent.mkdir(exist_ok=True)
trace=ENGINE/'mamushi_trace.jsonl';trace.write_text('')
lua="""modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('mamushi_trace.jsonl','w'));local last=-1;local rows={};local frames=0
CAPSETUP
hook.add('loop','mamushi_checks',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58)
 if clock<1 or clock==last then return end
 last=clock;frames=frames+1
 local case=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 if case>=CASECOUNT then player(2);setLife(1);player(1);setTime(0);return end
 if rows[case]==nil then rows[case]={states={},damage=0,received=0,clones=0,afterhit=0,cloneHits=0,control=false,move=0,apex=0,minPower=3000,health=0} end
 local r=rows[case];local st=stateNo()
 if tick>4 then
  r.states[st]=true;r.received=math.max(r.received,1000-life());r.minPower=math.min(r.minPower,power());r.maxPower=math.max(r.maxPower or 0,power());r.apex=math.min(r.apex,posY());r.clones=math.max(r.clones,numHelper(9500))
  if tick==8 then r.startX=posX() end
  if tick>8 and tick<100 then r.move=math.max(r.move,math.abs(posX()-(r.startX or posX()))) end
  if tick>90 and numHelper(9500)>0 and ctrl() then r.control=true end
  if r.received>0 and tick>115 then r.afterhit=math.max(r.afterhit,numHelper(9500)) end
  if helper(9500) then if moveHit()>0 then r.cloneHits=r.cloneHits+1 end;r.health=var(3);if stateNo()==9590 then r.hurtSamples=(r.hurtSamples or 0)+1;r.minHP=math.min(r.minHP or 180,var(3)) end;player(1) end
  player(2);r.damage=math.max(r.damage,DUMMYLIFE-life());r.victim=stateNo();player(1)
 end
 if tick==TICKS-1 then
  local states={};for n,_ in pairs(r.states) do table.insert(states,n) end;table.sort(states)
  local ss={};for _,n in ipairs(states) do table.insert(ss,tostring(n)) end
  f:write(case..'\\t'..table.concat(ss,',')..'\\t'..r.damage..'\\t'..r.received..'\\t'..r.clones..'\\t'..r.afterhit..'\\t'..r.cloneHits..'\\t'..tostring(r.control)..'\\t'..r.move..'\\t'..r.apex..'\\t'..r.minPower..'\\t'..numHelper(9500)..'\\t'..stateNo()..'\\t'..r.victim..'\\t'..r.maxPower..'\\t'..(r.hurtSamples or 0)..'\\t'..(r.minHP or 180)..'\\n');f:flush()
 end
 CAPTURE
end)
""".replace('TICKS',str(TICKS)).replace('CASECOUNT',str(len(cases))).replace('DUMMYLIFE',str(500 if LOW else 10000))
if CAP:
    folder=Path(CAP).resolve();folder.mkdir(parents=True,exist_ok=True)
    lua=lua.replace('CAPSETUP',"modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(folder)+'/')+")\nlocal images=assert(io.open("+json.dumps(str(folder/'frames.tsv'))+",'w'));local cap={index=0,last=-1000,pending=nil};local cues=assert(io.open("+json.dumps(str(folder/'audio.tsv'))+",'w'));local seen={};local observed=assert(io.open("+json.dumps(str(folder/'observed.tsv'))+",'w'))")
    lua=lua.replace('CAPTURE',"""
  if cap.pending~=nil then
   local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb')
   if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\t'..case..'\\t'..tick..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end
  end
  observed:write(frames..'\\t'..case..'\\t'..tick..'\\t'..st..'\\t'..time()..'\\t'..numHelper(9500)..'\\n');observed:flush()
  local sounds={[1000]=true,[1010]=true,[1020]=true,[1030]=true,[1040]=true,[1050]=true,[1200]=true,[1210]=true,[1400]=true,[1410]=true,[1420]=true,[1430]=true,[1440]=true,[3000]=true,[520]=true}
  if cap.prevState~=st and sounds[st] then cues:write(frames..'\\t'..case..'\\n');cues:flush() end
  cap.prevState=st
  if frames-cap.last>=4 and cap.pending==nil and tick>=12 and tick<=CAPEND then screenshot();cap.pending=frames;cap.last=frames end
""".replace('FOLDER',json.dumps(str(folder)+'/')).replace('CAPEND','450' if any(c['kind']=='clone_limit' for c in cases) else '310' if any(c['kind']=='ultimate' for c in cases) else '240'))
else:lua=lua.replace('CAPSETUP','').replace('CAPTURE','')
if os.environ.get('MAMUSHI_DEBUG'):
    lua=lua.replace("local f=assert(io.open('mamushi_trace.jsonl','w'));","local hf=assert(io.open('mamushi_helper_debug.tsv','w'));local f=assert(io.open('mamushi_trace.jsonl','w'));")
    lua=lua.replace('r.health=var(3);player(1)',"r.health=var(3);if tick%10==0 then hf:write(clock..'\\t'..stateNo()..'\\t'..time()..'\\t'..var(1)..'\\t'..var(2)..'\\t'..var(3)..'\\t'..var(4)..'\\t'..posX()..'\\t'..p2DistX()..'\\n');hf:flush() end;player(1)")
module.write_text(lua);debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/mamushi_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
if AUDIO:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=AUDIO,SDL_DISKAUDIODELAY='46')
try:
    run=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','MamushiCheck','-p1.ai','8' if CPU else '0','-p2','MamushiDummy','-p2.ai','0','-rounds','1','-time','300' if CAP else '9999']+(['-speed','0'] if CAP else ['-speedtest'])+([] if AUDIO else ['-nosound'])+['-log','mamushi_engine.log'],cwd=ENGINE,env=env,capture_output=True,text=True,timeout=180 if CAP else 90)
    print(run.stdout);print(run.stderr);assert run.returncode==0,f'Engine returned {run.returncode}'
finally:
    debug.write_text(saved)
    if module.exists():module.rename(module.with_name('-mamushi_checks.lua'))
rows={}
for line in trace.read_text().splitlines():rows.setdefault(int(line.split('\t')[0]),line.split('\t'))
assert sorted(rows)==list(range(len(cases))),('missing cases',sorted(rows))
report=[]
for i,case in enumerate(cases):
    row=rows[i];stateset=set(map(int,row[1].split(',')));damage=int(row[2]);received=int(row[3]);peak=int(row[4]);afterhit=int(row[5]);clonehits=int(row[6]);control=row[7]=='true';movement=float(row[8]);apex=float(row[9]);power=int(row[10]);endclones=int(row[11]);endstate=int(row[12]);victim=int(row[13]);bad=[];kind=case['kind']
    if kind=='move':
        if case['state'] not in stateset:bad.append('input did not execute requested technique')
        if case['name']=='Division':
            if peak<1 or clonehits<1 or damage<=0:bad.append('clone did not attack independently')
        elif case['name']=='Guardia':
            if 1202 not in stateset:bad.append('physical counter did not trigger')
        elif damage<=0:bad.append('technique caused no collision damage')
    if kind in ['combo','air'] and (case['state'] not in stateset or damage<85):bad.append('three-stage chain did not connect')
    if kind=='combo' and damage!={'a':152,'b':172,'c':176}[case['button']]:bad.append('a combo stage was skipped instead of dealing all three real contacts')
    if kind=='mixed' and (case['state'] not in stateset or damage!=case['expected']):bad.append('mixed chain did not complete all three contacts')
    if kind=='cpu' and damage<=0:bad.append('CPU did not approach and damage the opponent')
    if kind=='walk' and movement<35:bad.append('walking input failed')
    if kind in ['jump','diagonal'] and not -110<apex<-45:bad.append('jump height outside intended range')
    if kind=='charge' and (500 not in stateset or int(row[14])<700):bad.append('LB charge state / actual energy gain failed')
    if kind=='focus' and 520 not in stateset:bad.append('down LB focus failed')
    if kind.startswith('clone_'):
        if not 1<=peak<=6 or clonehits<1 or damage<=0:bad.append('autonomous clone attack failed')
        if not control:bad.append('root did not remain controllable with living clone')
        if kind=='clone_limit' and peak!=6:bad.append('six-clone stress limit not reached')
        if kind=='clone_limit' and 1210 in stateset:bad.append('full clone budget incorrectly triggered neutral RT as fallback')
        if kind=='clone_independent' and (received<=0 or afterhit<=0):bad.append('clones disappeared when root was struck / strike never connected')
        if endclones:bad.append('expired clones did not clean up')
    if kind=='clone_damage' and (int(row[15])<1 or int(row[16])>=180):bad.append('clone did not receive its own collision damage')
    if kind=='recovery' and (5120 not in stateset or endstate!=0):bad.append('knockdown failed to recover automatically')
    if kind=='ultimate' and (3001 not in stateset or damage!=(175 if LOW else 350) or victim in [3010,3011]):bad.append('confirmed ultimate damage/release failed')
    if kind in ['ultiblock','ultimiss','ultifar','empty'] and (3001 in stateset or damage>0):bad.append('ultimate confirmed without a valid hit')
    result=dict(case=case,states=sorted(stateset),damage=damage,received=received,max_clones=peak,clones_after_root_hit=afterhit,clone_contact_samples=clonehits,clone_hurt_samples=int(row[15]),clone_min_health=int(row[16]),root_control_while_clone_alive=control,movement=movement,jump_apex=apex,min_power=power,max_power=int(row[14]),end_clones=endclones,end_state=endstate,victim_end=victim,failures=bad);report.append(result)
    print('FAIL' if bad else 'PASS',case['name'],case['face'],result)
out=ROOT/'previews'/('Mamushi_CPU_checks.json' if CPU else 'Mamushi_extra_checks.json' if EXTRA else 'Mamushi_clone_health_checks.json' if HEALTH else 'Mamushi_low_life_checks.json' if LOW else 'Mamushi_capture_checks.json' if CAP else 'Mamushi_engine_checks.json');out.write_text(json.dumps(report,indent=2)+'\n')
assert not any(c['failures'] for c in report),str(out)
print('PASSED',len(report),'Mamushi raw-input / collision scenarios')
