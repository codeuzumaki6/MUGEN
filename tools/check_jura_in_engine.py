#!/usr/bin/env python3
"""Run raw Xbox-equivalent inputs and observe actual collisions in disposable copies."""
from pathlib import Path
import json,os,re,shutil,subprocess,sys
from build_jura_runtime import MOVES

ROOT=Path(__file__).resolve().parents[1];ENGINE=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly').resolve()
CAP=os.environ.get('JURA_CAPTURE');AUDIO=os.environ.get('JURA_AUDIO');TICKS=int(os.environ.get('JURA_TICKS','850'));LOW=os.environ.get('JURA_LOW_LIFE')=='1';CPU=os.environ.get('JURA_CPU')=='1';GUARD=os.environ.get('JURA_GUARD')=='1'
DUMMYLIFE=500 if LOW else 1000 if CAP else 10000
cases=[]
for form in [0,1]:
 for face in [1,-1]:
  for name,button,d,n,cost in MOVES:cases.append(dict(name=name,kind='move',form=form,face=face,button=button,d=d,state=n,cost=round(cost*.75) if form else cost,distance=50 if name in ['Barrido','Lanzador'] else 180 if name=='Marca' else 90 if name=='SalidaGarra' else 120))
  for button,base in [('a',200),('b',210),('c',220)]:
   cases.append(dict(name='Combo '+button,kind='combo',form=form,face=face,button=button,state=base+2,distance=50))
   cases.append(dict(name='Aire '+button,kind='air',form=form,face=face,button=button,state=600+['a','b','c'].index(button)*10+2,distance=60))
  for kind in ['ultimate','ultiblock','ultijump','ultifar','empty','recovery']:
   cases.append(dict(name=kind,kind=kind,form=form,face=face,distance=370 if kind=='ultifar' else 120))
  for button,name in [('L','Dash izquierda'),('R','Dash derecha')]:
   cases.append(dict(name=name,kind='dash',form=form,face=face,button=button,state=100 if (button=='R')==(face==1) else 105,distance=100))
  cases.append(dict(name='chargehit',kind='chargehit',form=form,face=face,distance=60))
for face in [1,-1]:
 for kind in ['walk','jump','diagonal','charge','awakening']:
  cases.append(dict(name=kind,kind=kind,form=0,face=face,distance=220))
 cases.append(dict(name='charge',kind='charge',form=1,face=face,distance=220))
if LOW:cases=[dict(name='low_life',kind='ultimate',form=form,face=1,distance=120) for form in [0,1]]
if CPU:cases=[dict(name='CPU',kind='cpu',form=form,face=1,distance=220) for form in [0,1]]
if GUARD:cases=[dict(name=kind,kind=kind,form=form,face=face,distance=60) for form in [0,1] for face in [1,-1] for kind in ['guard','crouchguard','airguard']]
REGEN=os.environ.get('JURA_REGEN')=='1'
if REGEN:cases=[dict(name=kind,kind=kind,form=0,face=face,distance=220) for face in [1,-1] for kind in ['regen','regen_cap']]
if os.environ.get('JURA_CASES'):
 wanted=json.loads(os.environ['JURA_CASES']);cases=[c for c in cases if c['name'] in wanted and (not CAP or c['face']==1)]
if os.environ.get('JURA_FORM'):cases=[c for c in cases if c['form']==int(os.environ['JURA_FORM'])]
assert cases
char=ENGINE/'chars/JuraCheck';dummy=ENGINE/'chars/JuraDummy'
shutil.copytree(ROOT/'Jura',char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(char/'Jura.def',char/'JuraCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'JuraDummy.def')
def fctl(kind,when,params):return f'\n[State -2, Test fixture]\ntype={kind}\ntriggerall=!IsHelper\ntriggerall=RoundState=2\ntrigger1={when}\nignorehitpause=1\n{params}\n'
p1=fctl('VarAdd','1','v=58\nvalue=1');p2=fctl('VarSet','NumEnemy>0','v=58\nvalue=EnemyNear,Var(58)')
for index,case in enumerate(cases):
 base=index*TICKS;face=case['face'];kind=case['kind'];distance=case['distance'];at=lambda t:f'Var(58)={base+t}';window=lambda a,b:f'Var(58)>={base+a} && Var(58)<={base+b}'
 for side in [1,2]:
  block=fctl('PosSet',at(1),f'x={(-1 if side==1 else 1)*face*distance/2}\ny=0')+fctl('VelSet',at(1),'x=0\ny=0')+fctl('Turn',at(1)+f' && Facing!={face if side==1 else -face}','')
  block+=fctl('LifeSet',at(1),f'value={(800 if kind=="regen" else 1295 if kind=="regen_cap" else 1300) if side==1 else DUMMYLIFE}')+fctl('PowerSet',at(1),f'value={0 if kind in ["charge","chargehit","empty"] else 3000}')
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
  if case['name']=='Marca':p1+=press(78,'z')
  if case['name'] in ['Reflejo','Senrigan']:p2+=fctl('ChangeState',at(43),'value=9700\nctrl=0')
 elif kind in ['combo','air']:
  if kind=='air':p1+=press(18,'U');p2+=fctl('PosSet',at(20),'y=-95')+fctl('ChangeState',at(20),'value=9702\nctrl=0')
  p1+=press(36 if kind=='air' else 26,case['button'])
  rng='StateNo>=600 && StateNo<=621' if kind=='air' else 'StateNo>=200 && StateNo<=221'
  p1+=fctl('AssertInput',f'{window(30,180)} && ({rng}) && Time>=6 && MoveHit && Var(58)%3=0','flag='+case['button'])
 elif kind=='walk':p1+=fctl('AssertInput',window(20,55),'flag='+('R' if face==1 else 'L'))
 elif kind=='dash':p1+=press(20,case['button'])+press(27,case['button'])
 elif kind in ['jump','diagonal']:
  if kind=='diagonal':p1+=fctl('AssertInput',window(20,55),'flag='+('R' if face==1 else 'L'))
  p1+=press(23,'U')
 elif kind=='charge':p1+=fctl('AssertInput',window(20,80),'flag=s')
 elif kind=='chargehit':p1+=fctl('AssertInput',window(20,60),'flag=s');p2+=fctl('ChangeState',at(43),'value=9700\nctrl=0')
 elif kind in ['awakening','regen','regen_cap']:p1+=motion('s','D')
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
for path,fixture in [(char/'Jura.cns',p1),(dummy/'kfm.cns',p2)]:
 text=path.read_text(encoding='latin-1')
 text=text.replace('[Statedef -2]','[Statedef -2]\n'+fixture,1) if '[Statedef -2]' in text else text+'\n[Statedef -2]\n'+fixture
 if path==dummy/'kfm.cns':text=re.sub(r'(?im)^life\s*=.*$',f'life={DUMMYLIFE}',text,count=1)
 path.write_text(text,encoding='latin-1')
with (dummy/'kfm.cns').open('a') as f:
 for n,fall in [(9700,0),(9701,1),(9703,0)]:
  f.write(f'\n[Statedef {n}]\ntype={"A" if n==9703 else "S"}\nmovetype=A\nphysics={"N" if n==9703 else "S"}\nanim=400\nctrl=0\nvelset=0,0\n[State {n}, Actual strike]\ntype=HitDef\ntrigger1=Time=0\nattr={"A" if n==9703 else "S"},NA\ndamage=60,0\nhitflag=MAF\nguardflag=MA\npausetime=5,8\nground.hittime=18\nground.velocity=-2,{-6 if fall else 0}\nair.velocity=-2,-4\nfall={fall}\nfall.recover=0\nsparkno=-1\n[State {n}, Done]\ntype=ChangeState\ntrigger1=Time>=24\nvalue=0\nctrl=1\n')
 f.write('\n[Statedef 9702]\ntype=A\nmovetype=I\nphysics=N\nanim=41\nvelset=0,0\nctrl=0\n[State 9702, Stay]\ntype=Null\ntrigger1=1\n')
trace=ENGINE/'jura_trace.tsv';trace.write_text('');module=ENGINE/'external/mods/jura_checks.lua'
lua="""modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('jura_trace.tsv','w'));local last=-1;local rows={};local frames=0
CAPSETUP
hook.add('loop','jura_checks',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end
 last=clock;frames=frames+1
 local case=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 if case>=CASECOUNT then player(2);setLife(1);player(1);setTime(0);return end
 if rows[case]==nil then rows[case]={states={},damage=0,received=0,move=0,apex=0,minPower=3000,maxPower=0,awake=0,blue=0,marks=0,portals=0,markY=0,travel=0,dash=0,aura=0,auraAfter=0,chargeStopped=false} end
 local r=rows[case];local st=stateNo()
 if tick>4 then
  r.states[st]=true;r.received=math.max(r.received,1300-life());r.minPower=math.min(r.minPower,power());r.maxPower=math.max(r.maxPower,power());r.apex=math.min(r.apex,posY());r.awake=math.max(r.awake,var(40))
  if anim()>=10000 then r.blue=r.blue+1 end
  if tick==8 then r.startX=posX();r.startScreenX=screenPosX() end
  if tick>8 and tick<100 then r.move=math.max(r.move,math.abs(posX()-(r.startX or posX()))) end
  r.marks=math.max(r.marks,numHelper(9600));r.portals=math.max(r.portals,numHelper(9601))
  if numHelper(9600)>0 and helper(9600) then r.markY=posY();player(1) end
  if st==1211 then r.travel=math.max(r.travel,math.abs(posX()-(r.startX or posX()))) end
  if st==100 or st==105 then r.dash=screenPosX()-(r.startScreenX or screenPosX()) end
  if st==500 then r.aura=math.max(r.aura,numHelper(9550)) end
  if tick>100 then r.auraAfter=math.max(r.auraAfter,numHelper(9550));r.chargeStopped=r.chargeStopped or st==0 end
  player(2);r.damage=math.max(r.damage,DUMMYLIFE-life());r.victim=stateNo();player(1)
 end
 if tick==TICKS-1 then
  local ss={};for n,_ in pairs(r.states) do table.insert(ss,n) end;table.sort(ss);for i,v in ipairs(ss) do ss[i]=tostring(v) end
  f:write(case..'\\t'..table.concat(ss,',')..'\\t'..r.damage..'\\t'..r.received..'\\t'..r.move..'\\t'..r.apex..'\\t'..r.minPower..'\\t'..r.maxPower..'\\t'..r.awake..'\\t'..r.blue..'\\t'..var(40)..'\\t'..anim()..'\\t'..stateNo()..'\\t'..r.victim..'\\t'..tostring(ctrl())..'\\t'..r.marks..'\\t'..r.portals..'\\t'..r.markY..'\\t'..r.travel..'\\t'..numHelper(9600)..'\\t'..r.dash..'\\t'..r.aura..'\\t'..r.auraAfter..'\\t'..tostring(r.chargeStopped)..'\\t'..life()..'\\t'..numHelper()..'\\n');f:flush()
 end
 CAPTURE
end)
""".replace('TICKS',str(TICKS)).replace('CASECOUNT',str(len(cases))).replace('DUMMYLIFE',str(DUMMYLIFE))
if os.environ.get('JURA_DEBUG'):
 lua=lua.replace('local f=assert(',"local dashlog=assert(io.open('/tmp/jura_dash_positions.tsv','w'));local f=assert(",1)
 lua=lua.replace('local clock=var(58);',"""local clock=var(58);
 if stateNo()==100 or stateNo()==105 then
  local x=posX();local sx=screenPosX();local vx=velX();local st=stateNo();local tm=time()
  player(2);local other=posX();player(1)
  dashlog:write(clock..'\\t'..st..'\\t'..tm..'\\t'..x..'\\t'..sx..'\\t'..vx..'\\t'..other..'\\n');dashlog:flush()
 end
 """,1)
if CAP:
 folder=Path(CAP).resolve();folder.mkdir(parents=True,exist_ok=True)
 lua=lua.replace('CAPSETUP',"modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(folder)+'/')+")\nlocal images=assert(io.open("+json.dumps(str(folder/'frames.tsv'))+",'w'));local cues=assert(io.open("+json.dumps(str(folder/'audio.tsv'))+",'w'));local cap={index=0,last=-1000,pending=nil}")
 lua=lua.replace('CAPTURE',"""
 if cap.pending~=nil then local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb');if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\t'..case..'\\t'..tick..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end end
 local sounds={[1000]=true,[1010]=true,[1020]=true,[1030]=true,[1040]=true,[1050]=true,[1200]=true,[1210]=true,[1211]=true,[1400]=true,[1410]=true,[1420]=true,[1430]=true,[1440]=true,[3000]=true,[520]=true,[500]=true}
 if cap.prev~=st and sounds[st] then cues:write(frames..'\\t'..case..'\\n');cues:flush() end;cap.prev=st
 if frames-cap.last>=4 and cap.pending==nil and tick>=12 and tick<=CAPEND then screenshot();cap.pending=frames;cap.last=frames end
 """.replace('FOLDER',json.dumps(str(folder)+'/')).replace('CAPEND','790' if any(c['kind']=='awakening' for c in cases) else '300'))
else:lua=lua.replace('CAPSETUP','').replace('CAPTURE','')
module.write_text(lua);debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/jura_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
if AUDIO:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=AUDIO,SDL_DISKAUDIODELAY='46')
try:
 run=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','JuraCheck','-p1.ai','8' if CPU else '0','-p2','JuraDummy','-p2.ai','0','-rounds','1','-time','300' if CAP else '9999']+(['-speed','0'] if CAP else ['-speedtest'])+([] if AUDIO else ['-nosound'])+['-log','jura_engine.log'],cwd=ENGINE,env=env,capture_output=True,text=True,timeout=180 if CAP else 110)
 print(run.stdout);print(run.stderr);assert run.returncode==0,f'Engine returned {run.returncode}'
 assert not re.search(r"WARNING: Jura's[^\n]*Unknown state controller parameter",run.stdout+run.stderr),'Jura controller parameter ignored by the engine'
finally:
 debug.write_text(saved)
 if module.exists():module.rename(module.with_name('-jura_checks.lua'))
rows={int(line.split('\t')[0]):line.split('\t') for line in trace.read_text().splitlines()};assert sorted(rows)==list(range(len(cases))),('missing traces',sorted(rows))
report=[]
for i,case in enumerate(cases):
 row=rows[i];ss=set(map(int,row[1].split(',')));damage=int(row[2]);received=int(row[3]);movement=float(row[4]);apex=float(row[5]);lowpower=int(row[6]);highpower=int(row[7]);awake=int(row[8]);blue=int(row[9]);endawake=int(row[10]);endanim=int(row[11]);endstate=int(row[12]);victim=int(row[13]);bad=[];kind=case['kind']
 if kind!='cpu' and int(row[25])!=0:bad.append('finite helper remained after recovery')
 if kind=='move':
  if case['state'] not in ss:bad.append('requested raw input did not enter technique')
  if damage<=0 and case['name']!='Levitar':bad.append('no actual collision damage')
  if case['name']=='Levitar' and (apex>=-45 or endstate!=0):bad.append('finite flight or landing failed')
  if case['name'] in ['Reflejo','Senrigan'] and 1202 not in ss:bad.append('incoming strike did not trigger counter')
  if case['name']=='Marca' and (1211 not in ss or int(row[15])!=1 or int(row[16])<2 or float(row[17])!=0 or float(row[18])<100 or int(row[19])!=0):bad.append('claw placement, crossed-band entry/exit, travel or consumed mark failed')
  if case['name']=='SalidaGarra' and int(row[16])<2:bad.append('claw retreat did not display both portals')
  if lowpower>3000-case['cost']:bad.append('energy was not spent')
 if kind in ['combo','air'] and (case['state'] not in ss or damage<155):bad.append('three-stage physical chain did not land')
 if kind=='cpu' and damage<=0:bad.append('CPU did no damage or did not use claw placement and travel')
 if kind=='walk' and movement<40:bad.append('walk failed')
 if kind=='dash' and (case['state'] not in ss or abs(float(row[20]))<55 or (float(row[20])>0)!=(case['button']=='R') or apex!=0 or endstate!=0 or lowpower!=3000):bad.append('double-tap ground dash direction, movement, recovery or free cost failed')
 if kind in ['jump','diagonal'] and not -110<apex<-60:bad.append('jump apex outside calibrated range')
 if kind=='charge' and (500 not in ss or highpower<900 or int(row[21])!=1 or int(row[22])!=0 or row[23].strip()!='true'):bad.append('charge energy, visible aura or cleanup on release failed')
 if kind=='chargehit' and (500 not in ss or received<=0 or int(row[21])!=1 or int(row[22])!=0 or endstate!=0):bad.append('charge was not hittable or aura survived interruption')
 if kind=='awakening' and (520 not in ss or awake<700 or endawake!=0 or endanim>=10000):bad.append('awakening did not activate and expire')
 if kind in ['regen','regen_cap'] and (520 not in ss or awake<700 or endawake!=0 or (not 965<=int(row[24])<=980 if kind=='regen' else int(row[24])!=1300)):bad.append('regeneration amount, cap or expiry failed')
 if kind=='recovery' and (5120 not in ss or endstate!=0):bad.append('knockdown/getup failed')
 if kind in ['guard','crouchguard','airguard'] and (received!=0 or {'guard':150,'crouchguard':152,'airguard':154}[kind] not in ss):bad.append('manual guard failed against real physical contact')
 if kind=='ultimate' and (3001 not in ss or damage!=(225 if LOW else 450) or victim in [3010,3011]):bad.append('ultimate confirmation / bounded damage / safe release failed')
 if kind in ['ultiblock','ultijump','ultifar','empty'] and (damage>0 or 3001 in ss):bad.append('ultimate hit when it should fail')

 result=dict(case=case,states=sorted(ss),damage=damage,received=received,movement=movement,jump_apex=apex,min_power=lowpower,max_power=highpower,max_awakening=awake,blue_frames=blue,end_awakening=endawake,end_animation=endanim,end_state=endstate,victim_end=victim,claw_marks=int(row[15]),claw_portals=int(row[16]),claw_mark_y=float(row[17]),claw_travel=float(row[18]),claw_marks_remaining=int(row[19]),dash_signed_distance=float(row[20]),charge_aura=int(row[21]),aura_after_charge=int(row[22]),end_life=int(row[24]),end_helpers=int(row[25]),failures=bad);report.append(result)
 print('FAIL' if bad else 'PASS',case['name'],case['form'],case['face'],bad,damage)
base_rows={(r['case']['name'],r['case']['face']):r for r in report if not r['case']['form']}
comparisons=0
for result in report:
 case=result['case'];base=base_rows.get((case['name'],case['face']))
 if case['form'] and base and case['kind'] in ['move','combo','air']:
  comparisons+=1
  if result['damage']<base['damage']*1.23:result['failures'].append('awakening did not increase real damage by at least 23 percent')
  if result['damage']>=950:result['failures'].append('one technique exceeds intended versus damage budget')
out=ROOT/'previews'/('Jura_regen_checks.json' if REGEN else 'Jura_guard_checks.json' if GUARD else 'Jura_CPU_checks.json' if CPU else 'Jura_low_life_checks.json' if LOW else 'Jura_capture_checks.json' if CAP else 'Jura_engine_checks.json');out.write_text(json.dumps(report,indent=2)+'\n')
assert not any(r['failures'] for r in report),str(out)
if comparisons:print('PASS',comparisons,'awakened techniques and chains: greater collision damage, below full-life knockout')
print('PASSED',len(report),'Jura raw-input and collision cases')
