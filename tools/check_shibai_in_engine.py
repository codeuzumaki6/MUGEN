#!/usr/bin/env python3
"""Run raw Xbox-equivalent inputs and observe actual collisions in disposable copies."""
from pathlib import Path
import json,os,re,shutil,subprocess,sys
from build_shibai_runtime import MOVES

ROOT=Path(__file__).resolve().parents[1];ENGINE=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly').resolve()
CAP=os.environ.get('SHIBAI_CAPTURE');AUDIO=os.environ.get('SHIBAI_AUDIO');TICKS=int(os.environ.get('SHIBAI_TICKS','850'));LOW=os.environ.get('SHIBAI_LOW_LIFE')=='1';CPU=os.environ.get('SHIBAI_CPU')=='1';GUARD=os.environ.get('SHIBAI_GUARD')=='1'
cases=[]
for form in [0,1]:
 for face in [1,-1]:
  for name,button,d,n,cost in MOVES:cases.append(dict(name=name,kind='move',form=form,face=face,button=button,d=d,state=n,cost=round(cost*.6) if form else cost,distance=45 if name in ['Reflejo','Senrigan','Descarga'] else 180 if name=='Garra' else 90 if name=='SalidaGarra' else 120))
  for button,base in [('a',200),('b',210),('c',220)]:
   cases.append(dict(name='Combo '+button,kind='combo',form=form,face=face,button=button,state=base+2,distance=90))
   cases.append(dict(name='Aire '+button,kind='air',form=form,face=face,button=button,state=600+['a','b','c'].index(button)*10+2,distance=60))
  for kind in ['ultimate','ultiblock','ultijump','ultifar','empty','recovery']:
   cases.append(dict(name=kind,kind=kind,form=form,face=face,distance=370 if kind=='ultifar' else 120))
for face in [1,-1]:
 for kind in ['walk','jump','diagonal','charge','awakening']:
  cases.append(dict(name=kind,kind=kind,form=0,face=face,distance=220))
if LOW:cases=[dict(name='low_life',kind='ultimate',form=form,face=1,distance=120) for form in [0,1]]
if CPU:cases=[dict(name='CPU',kind='cpu',form=form,face=1,distance=220) for form in [0,1]]
if GUARD:cases=[dict(name=kind,kind=kind,form=form,face=face,distance=60) for form in [0,1] for face in [1,-1] for kind in ['guard','crouchguard','airguard']]
if os.environ.get('SHIBAI_CASES'):
 wanted=json.loads(os.environ['SHIBAI_CASES']);cases=[c for c in cases if c['name'] in wanted and (not CAP or c['face']==1)]
if os.environ.get('SHIBAI_FORM'):cases=[c for c in cases if c['form']==int(os.environ['SHIBAI_FORM'])]
assert cases
char=ENGINE/'chars/ShibaiCheck';dummy=ENGINE/'chars/ShibaiDummy'
shutil.copytree(ROOT/'Shibai',char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(char/'Shibai.def',char/'ShibaiCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'ShibaiDummy.def')
def fctl(kind,when,params):return f'\n[State -2, Test fixture]\ntype={kind}\ntriggerall=!IsHelper\ntriggerall=RoundState=2\ntrigger1={when}\nignorehitpause=1\n{params}\n'
p1=fctl('VarAdd','1','v=58\nvalue=1');p2=fctl('VarSet','NumEnemy>0','v=58\nvalue=EnemyNear,Var(58)')
for index,case in enumerate(cases):
 base=index*TICKS;face=case['face'];kind=case['kind'];distance=case['distance'];at=lambda t:f'Var(58)={base+t}';window=lambda a,b:f'Var(58)>={base+a} && Var(58)<={base+b}'
 for side in [1,2]:
  block=fctl('PosSet',at(1),f'x={(-1 if side==1 else 1)*face*distance/2}\ny=0')+fctl('VelSet',at(1),'x=0\ny=0')+fctl('Turn',at(1)+f' && Facing!={face if side==1 else -face}','')
  block+=fctl('LifeSet',at(1),f'value={1300 if side==1 else 500 if LOW else 10000}')+fctl('PowerSet',at(1),f'value={0 if kind in ["charge","empty"] else 3000}')
  for v in [12,20,22,40,41]:block+=fctl('VarSet',at(1),f'v={v}\nvalue={800 if v==40 and case["form"] else 0}')
  block+=fctl('ChangeState',at(1),'value=0\nctrl=1')
  if side==1:p1+=block
  else:p2+=block
 def press(t,b):return fctl('AssertInput',at(t),'flag='+b)
 def motion(b,d,t=28):
  if d in ['F','B']:
   direction=('R' if face==1 else 'L') if d=='F' else ('L' if face==1 else 'R')
   return fctl('AssertInput',window(t-8,t-3),'flag=D')+fctl('AssertInput',window(t-5,t+1),'flag='+direction)+press(t,b)
  return (fctl('AssertInput',window(t-4,t+1),'flag=D') if d=='D' else '')+press(t,b)
 if kind=='move':
  p1+=motion(case['button'],case['d'])
  if case['name']=='Garra':p1+=press(78,'z')
  if case['name'] in ['Reflejo','Senrigan']:p2+=fctl('ChangeState',at(43),'value=9700\nctrl=0')
 elif kind in ['combo','air']:
  if kind=='air':p1+=press(18,'U');p2+=fctl('PosSet',at(20),'y=-95')+fctl('ChangeState',at(20),'value=9702\nctrl=0')
  p1+=press(36 if kind=='air' else 26,case['button'])
  rng='StateNo>=600 && StateNo<=621' if kind=='air' else 'StateNo>=200 && StateNo<=221'
  p1+=fctl('AssertInput',f'{window(30,180)} && ({rng}) && Time>=8 && ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<9 && Var(58)%3=0','flag='+case['button'])
 elif kind=='walk':p1+=fctl('AssertInput',window(20,55),'flag='+('R' if face==1 else 'L'))
 elif kind in ['jump','diagonal']:
  if kind=='diagonal':p1+=fctl('AssertInput',window(20,55),'flag='+('R' if face==1 else 'L'))
  p1+=press(23,'U')
 elif kind=='charge':p1+=fctl('AssertInput',window(20,80),'flag=s')
 elif kind=='awakening':p1+=motion('s','D')
 elif kind=='recovery':p2+=fctl('PosSet',window(19,35),f'x={(-distance/2+32)*face}\ny=0')+fctl('ChangeState',at(22),'value=9701\nctrl=0')
 elif kind in ['guard','crouchguard','airguard']:
  height=-55 if kind=='airguard' else 0
  p1+=fctl('PosSet',window(30,70),f'x={-face*30}\ny={height}')+fctl('AssertInput',window(20,100),'flag='+('L' if face==1 else 'R'))
  if kind=='airguard':p1+=fctl('PosSet',at(19),'y=-55')+fctl('ChangeState',at(19),'value=50\nctrl=1')
  if kind=='crouchguard':p1+=fctl('AssertInput',window(20,100),'flag=D')
  p2+=fctl('PosSet',window(30,70),f'x=0\ny={height}')+fctl('ChangeState',at(43),f'value={9703 if kind=="airguard" else 9700}\nctrl=0')
 elif kind in ['ultimate','ultiblock','ultijump','ultifar','empty']:
  p1+=press(28,'x')
  if kind=='ultiblock':p2+=fctl('AssertInput',window(18,170),'flag='+('R' if face==1 else 'L'))
  if kind=='ultijump':p2+=fctl('PosSet',at(20),'y=-170')+fctl('ChangeState',at(20),'value=9702\nctrl=0')
for path,fixture in [(char/'Shibai.cns',p1),(dummy/'kfm.cns',p2)]:
 text=path.read_text(encoding='latin-1')
 text=text.replace('[Statedef -2]','[Statedef -2]\n'+fixture,1) if '[Statedef -2]' in text else text+'\n[Statedef -2]\n'+fixture
 if path==dummy/'kfm.cns':text=re.sub(r'(?im)^life\s*=.*$',f'life={500 if LOW else 10000}',text,count=1)
 path.write_text(text,encoding='latin-1')
with (dummy/'kfm.cns').open('a') as f:
 for n,fall in [(9700,0),(9701,1),(9703,0)]:
  f.write(f'\n[Statedef {n}]\ntype={"A" if n==9703 else "S"}\nmovetype=A\nphysics={"N" if n==9703 else "S"}\nanim=400\nctrl=0\nvelset=0,0\n[State {n}, Actual strike]\ntype=HitDef\ntrigger1=Time=0\nattr={"A" if n==9703 else "S"},NA\ndamage=60,0\nhitflag=MAF\nguardflag=MA\npausetime=5,8\nground.hittime=18\nground.velocity=-2,{-6 if fall else 0}\nair.velocity=-2,-4\nfall={fall}\nfall.recover=0\nsparkno=-1\n[State {n}, Done]\ntype=ChangeState\ntrigger1=Time>=24\nvalue=0\nctrl=1\n')
 f.write('\n[Statedef 9702]\ntype=A\nmovetype=I\nphysics=N\nanim=41\nvelset=0,0\nctrl=0\n[State 9702, Stay]\ntype=Null\ntrigger1=1\n')
trace=ENGINE/'shibai_trace.tsv';trace.write_text('');module=ENGINE/'external/mods/shibai_checks.lua'
lua="""modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('shibai_trace.tsv','w'));local last=-1;local rows={};local frames=0
CAPSETUP
hook.add('loop','shibai_checks',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end
 last=clock;frames=frames+1
 local case=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 if case>=CASECOUNT then player(2);setLife(1);player(1);setTime(0);return end
 if rows[case]==nil then rows[case]={states={},damage=0,received=0,move=0,apex=0,minPower=3000,maxPower=0,awake=0,blue=0} end
 local r=rows[case];local st=stateNo()
 if tick>4 then
  r.states[st]=true;r.received=math.max(r.received,1300-life());r.minPower=math.min(r.minPower,power());r.maxPower=math.max(r.maxPower,power());r.apex=math.min(r.apex,posY());r.awake=math.max(r.awake,var(40))
  if anim()>=10000 then r.blue=r.blue+1 end
  if tick==8 then r.startX=posX() end
  if tick>8 and tick<100 then r.move=math.max(r.move,math.abs(posX()-(r.startX or posX()))) end
  player(2);r.damage=math.max(r.damage,DUMMYLIFE-life());r.victim=stateNo();player(1)
 end
 if tick==TICKS-1 then
  local ss={};for n,_ in pairs(r.states) do table.insert(ss,n) end;table.sort(ss);for i,v in ipairs(ss) do ss[i]=tostring(v) end
  f:write(case..'\\t'..table.concat(ss,',')..'\\t'..r.damage..'\\t'..r.received..'\\t'..r.move..'\\t'..r.apex..'\\t'..r.minPower..'\\t'..r.maxPower..'\\t'..r.awake..'\\t'..r.blue..'\\t'..var(40)..'\\t'..anim()..'\\t'..stateNo()..'\\t'..r.victim..'\\t'..tostring(ctrl())..'\\n');f:flush()
 end
 CAPTURE
end)
""".replace('TICKS',str(TICKS)).replace('CASECOUNT',str(len(cases))).replace('DUMMYLIFE',str(500 if LOW else 10000))
if CAP:
 folder=Path(CAP).resolve();folder.mkdir(parents=True,exist_ok=True)
 lua=lua.replace('CAPSETUP',"modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(folder)+'/')+")\nlocal images=assert(io.open("+json.dumps(str(folder/'frames.tsv'))+",'w'));local cues=assert(io.open("+json.dumps(str(folder/'audio.tsv'))+",'w'));local cap={index=0,last=-1000,pending=nil}")
 lua=lua.replace('CAPTURE',"""
 if cap.pending~=nil then local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb');if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\t'..case..'\\t'..tick..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end end
 local sounds={[1000]=true,[1010]=true,[1020]=true,[1030]=true,[1040]=true,[1050]=true,[1200]=true,[1210]=true,[1211]=true,[1400]=true,[1410]=true,[1420]=true,[1430]=true,[1440]=true,[3000]=true,[520]=true}
 if cap.prev~=st and sounds[st] then cues:write(frames..'\\t'..case..'\\n');cues:flush() end;cap.prev=st
 if frames-cap.last>=4 and cap.pending==nil and tick>=12 and tick<=CAPEND then screenshot();cap.pending=frames;cap.last=frames end
 """.replace('FOLDER',json.dumps(str(folder)+'/')).replace('CAPEND','790' if any(c['kind']=='awakening' for c in cases) else '300'))
else:lua=lua.replace('CAPSETUP','').replace('CAPTURE','')
module.write_text(lua);debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/shibai_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
if AUDIO:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=AUDIO,SDL_DISKAUDIODELAY='46')
try:
 run=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','ShibaiCheck','-p1.ai','8' if CPU else '0','-p2','ShibaiDummy','-p2.ai','0','-rounds','1','-time','300' if CAP else '9999']+(['-speed','0'] if CAP else ['-speedtest'])+([] if AUDIO else ['-nosound'])+['-log','shibai_engine.log'],cwd=ENGINE,env=env,capture_output=True,text=True,timeout=180 if CAP else 110)
 print(run.stdout);print(run.stderr);assert run.returncode==0,f'Engine returned {run.returncode}'
finally:
 debug.write_text(saved)
 if module.exists():module.rename(module.with_name('-shibai_checks.lua'))
rows={int(line.split('\t')[0]):line.split('\t') for line in trace.read_text().splitlines()};assert sorted(rows)==list(range(len(cases))),('missing traces',sorted(rows))
report=[]
for i,case in enumerate(cases):
 row=rows[i];ss=set(map(int,row[1].split(',')));damage=int(row[2]);received=int(row[3]);movement=float(row[4]);apex=float(row[5]);lowpower=int(row[6]);highpower=int(row[7]);awake=int(row[8]);blue=int(row[9]);endawake=int(row[10]);endanim=int(row[11]);endstate=int(row[12]);victim=int(row[13]);bad=[];kind=case['kind']
 if kind=='move':
  if case['state'] not in ss:bad.append('requested raw input did not enter technique')
  if damage<=0:bad.append('no actual collision damage')
  if case['name'] in ['Reflejo','Senrigan'] and 1202 not in ss:bad.append('incoming strike did not trigger counter')
  if lowpower>3000-case['cost']:bad.append('energy was not spent')
 if kind in ['combo','air'] and (case['state'] not in ss or damage<180):bad.append('three-stage wind chain did not land')
 if kind=='cpu' and damage<=0:bad.append('CPU did no damage')
 if kind=='walk' and movement<40:bad.append('walk failed')
 if kind in ['jump','diagonal'] and not -110<apex<-60:bad.append('jump apex outside calibrated range')
 if kind=='charge' and (500 not in ss or highpower<900):bad.append('charge did not gain real energy')
 if kind=='awakening' and (520 not in ss or blue<500 or awake<700 or endawake!=0 or endanim>=10000):bad.append('awakening did not transform and expire back to base')
 if kind=='recovery' and (5120 not in ss or endstate!=0):bad.append('knockdown/getup failed')
 if kind in ['guard','crouchguard','airguard'] and (received!=0 or {'guard':150,'crouchguard':152,'airguard':154}[kind] not in ss):bad.append('manual guard failed against real physical contact')
 if kind=='ultimate' and (3001 not in ss or damage!=(210 if LOW else 420) or victim in [3010,3011]):bad.append('ultimate confirmation / bounded damage / safe release failed')
 if kind in ['ultiblock','ultijump','ultifar','empty'] and (damage>0 or 3001 in ss):bad.append('ultimate hit when it should fail')
 if case['form'] and blue<20:bad.append('awakened form never rendered')
 result=dict(case=case,states=sorted(ss),damage=damage,received=received,movement=movement,jump_apex=apex,min_power=lowpower,max_power=highpower,max_awakening=awake,blue_frames=blue,end_awakening=endawake,end_animation=endanim,end_state=endstate,victim_end=victim,failures=bad);report.append(result)
 print('FAIL' if bad else 'PASS',case['name'],case['form'],case['face'],bad,damage)
out=ROOT/'previews'/('Shibai_guard_checks.json' if GUARD else 'Shibai_CPU_checks.json' if CPU else 'Shibai_low_life_checks.json' if LOW else 'Shibai_capture_checks.json' if CAP else 'Shibai_engine_checks.json');out.write_text(json.dumps(report,indent=2)+'\n')
assert not any(r['failures'] for r in report),str(out)
print('PASSED',len(report),'Shibai raw-input and collision cases')
