#!/usr/bin/env python3
"""Actual controls, two forms, original frame selection and collision in Ikemen GO."""
from pathlib import Path
import fcntl,hashlib,json,os,re,shutil,subprocess,uuid
from build_boruto_runtime import MOVES
ROOT=Path(__file__).resolve().parents[1];ENGINE=Path('/workspace/.eida-tools/ikemen-nightly');TICKS=int(os.environ.get('BORUTO_TICKS','660'));CAP=os.environ.get('BORUTO_CAPTURE');AUDIO=os.environ.get('BORUTO_AUDIO')
lock=open(ENGINE/'.native-character-check.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
cases=[]
for form in [0,1]:
 for face in [1,-1]:
  for name,b,d,n,cost in MOVES:cases.append(dict(name=name,kind='move',form=form,face=face,b=b,d=d,state=n+form*10000,cost=cost,distance=70 if (form and n==1010) or n in [1000,1030,1400,1410,1420,1440,1040] else 170 if n in [1010,1200,1020,1210,1430] else 105))
  for b,n in [('a',202),('b',212),('c',222)]:
   for kind in ['combo','air']:cases.append(dict(name=kind+' '+b,kind=kind,form=form,face=face,b=b,state=n+(400 if kind=='air' else 0)+form*10000,distance=40))
  for kind in ['ultimate','ultiblock','ultifar','ultimate_one_hp','ult_interrupt','empty','charge','guard','recovery','expire_attack','expire_hurt']:
   if kind.startswith('expire') and not form:continue
   cases.append(dict(name=kind,kind=kind,form=form,face=face,distance=430 if kind=='ultifar' else 35 if kind in ['guard','recovery','expire_hurt'] else 110))
for face in [1,-1]:
 for kind in ['awakening','no_awake']:cases.append(dict(name=kind,kind=kind,form=0,face=face,distance=110))
for c in cases:
 if c['kind']=='move':c['distance']=150 if c['name'] in ['Kunai','Disparo','Futon'] else 80
if os.environ.get('BORUTO_DEMO')=='showcase':
 names=['Rasengan','Shiden','Kenjutsu','Espiral','Caida','Disparo','Futon','ultimate']
 cases=[c for c in cases if c['face']==1 and c['form']==0 and c['name'] in names]+[c for c in cases if c['name']=='awakening' and c['face']==1]+[c for c in cases if c['face']==1 and c['form']==1 and c['name'] in ['Rasengan','Espiral','Caida','Disparo','Invocacion','Futon','ultimate']]
if os.environ.get('BORUTO_CASES'):cases=[c for c in cases if c['name'] in json.loads(os.environ['BORUTO_CASES'])]
if os.environ.get('BORUTO_FORM'):cases=[c for c in cases if c['form']==int(os.environ['BORUTO_FORM'])]
if os.environ.get('BORUTO_FACE'):cases=[c for c in cases if c['face']==int(os.environ['BORUTO_FACE'])]
if os.environ.get('BORUTO_DEMO')=='awake':cases=[c for c in cases if c['kind']=='awakening' and c['face']==1]+[c for c in cases if c['form']==1 and c['face']==1 and c['kind'] in ['move','ultimate']]
if os.environ.get('BORUTO_DEMO')=='all':cases=[c for c in cases if c['form']==0 and c['kind'] in ['move','ultimate']]+[c for c in cases if c['kind']=='awakening']+[c for c in cases if c['form']==1 and c['kind'] in ['move','ultimate']]
if os.environ.get('BORUTO_DISTANCE'):
 for case in cases:case['distance']=int(os.environ['BORUTO_DISTANCE'])
assert cases
char=ENGINE/'chars/BorutoCheck';dummy=ENGINE/'chars/BorutoDummy';shutil.copytree(ROOT/'BorutoKarmaJogan',char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True);shutil.copyfile(char/'BorutoKarmaJogan.def',char/'BorutoCheck.def');shutil.copyfile(dummy/'kfm.def',dummy/'BorutoDummy.def')
if os.environ.get('BORUTO_TARGET_SCALE'):
 p=dummy/'kfm.cns';text=p.read_text(encoding='latin1');scale=float(os.environ['BORUTO_TARGET_SCALE']);text=re.sub(r'(?im)^(xscale|yscale)\s*=.*$',lambda m:m[1]+'='+str(scale),text);text=re.sub(r'(?im)^height\s*=\s*([0-9.]+).*$',lambda m:'height='+str(float(m[1])*scale),text);p.write_text(text,encoding='latin1')
def ctl(typ,when,params):return f'\n[State -2, Disposable Boruto test]\ntype={typ}\ntriggerall=!IsHelper\ntriggerall=RoundState=2\ntrigger1={when}\nignorehitpause=1\n{params}\n'
def inject(p,s):
 t=p.read_text(encoding='latin1');t=t.replace('[Statedef -2]','[Statedef -2]\n'+s,1) if '[Statedef -2]' in t else t+'\n[Statedef -2]\n'+s;p.write_text(t,encoding='latin1')
p1=ctl('VarAdd','1','v=58\nvalue=1')+ctl('PlayerPush','1','value=0');p2=ctl('VarSet','NumEnemy>0','v=58\nvalue=EnemyNear,Var(58)')+ctl('PlayerPush','1','value=0')
for i,case in enumerate(cases):
 kind=case['kind'];face=case['face'];form=case['form'];dist=case['distance'];at=lambda t:f'Var(58)={i*TICKS+t}';win=lambda a,b:f'Var(58)>={i*TICKS+a} && Var(58)<={i*TICKS+b}'
 for side in [1,2]:
  block=ctl('PosSet',at(1),f'x={(-1 if side==1 else 1)*face*dist/2}\ny=0')+ctl('VelSet',at(1),'x=0\ny=0')+ctl('Turn',at(1)+f' && Facing!={face if side==1 else -face}','')
  block+=ctl('LifeSet',at(1),f'value={1 if side==1 and kind=="ultimate_one_hp" else 1200 if side==1 else 1000}')+ctl('PowerSet',at(1),f'value={0 if kind in ["charge","empty","no_awake"] else 3000}')+ctl('ChangeState',at(1),'value=0\nctrl=1')
  if kind=='ultifar' or dist>=400:block+=ctl('ScreenBound',win(2,TICKS-2),'value=0\nmovecamera=0,0')+ctl('PosSet',at(5),f'x={(-1 if side==1 else 1)*face*dist/2}\ny=0')
  if side==1:p1+=block
  else:p2+=block
 for v in [12,20,21,40,41,42]:p1+=ctl('VarSet',at(2),f'v={v}\nvalue={1 if v==42 and form else 900 if v==40 and form else 0}')
 def press(t,b):return ctl('AssertInput',at(t),'flag='+b)
 def motion(b,d,t=28):
  if d in ['F','B']:
   lr=('R' if face==1 else 'L') if d=='F' else ('L' if face==1 else 'R')
   return ctl('AssertInput',win(t-8,t-3),'flag=D')+ctl('AssertInput',win(t-5,t+1),'flag='+lr)+press(t,b)
  return (ctl('AssertInput',win(t-4,t+1),'flag=D') if d=='D' else '')+press(t,b)
 if kind=='move':p1+=motion(case['b'],case['d'])
 if kind=='move' and os.environ.get('BORUTO_SPECIAL_GUARD'):p2+=ctl('AssertInput',win(18,250),'flag='+('R' if face==1 else 'L'))
 if kind=='move' and os.environ.get('BORUTO_UZUHIKO_INTERRUPT'):p2+=ctl('Helper',at(10),'helpertype=Normal\nID=9705\nname="Real spiral interruption"\nstateno=9705\npostype=P2\npos=0,0\nownpal=1\nkeyctrl=0')
 if kind in ['combo','air']:
  if kind=='air':p1+=press(18,'U');p2+=ctl('PosSet',at(20),'y=-85')+ctl('ChangeState',at(20),'value=9702\nctrl=0')
  p1+=press(36 if kind=='air' else 26,case['b'])+ctl('AssertInput',win(30,150)+(' && StateNo%10000>=600 && StateNo%10000<=621' if kind=='air' else ' && StateNo%10000>=200 && StateNo%10000<=221')+' && Time>=6 && MoveHit && Var(58)%3=0','flag='+case['b'])
 elif kind in ['ultimate','ultiblock','ultifar','ultimate_one_hp','ult_interrupt','empty']:
  p1+=press(28,'x')
  if kind=='ultiblock':p2+=ctl('AssertInput',win(18,180),'flag='+('R' if face==1 else 'L'))
  if kind=='ultiblock':p2+=ctl('AssertInput',win(181,790),'flag='+('R' if face==1 else 'L'))
  if kind=='ult_interrupt':p2+=ctl('Helper',at(10),'helpertype=Normal\nID=9705\nname="Delayed real interruption probe"\nstateno=9705\npostype=P2\npos=0,0\nownpal=1\nkeyctrl=0')
 elif kind=='charge':p1+=ctl('AssertInput',win(20,105),'flag=s')
 elif kind in ['awakening','no_awake']:p1+=motion('s','D')
 elif kind=='expire_attack':p1+=ctl('VarSet',at(22),'v=40\nvalue=30')+motion('a','B')
 elif kind=='expire_hurt':p1+=ctl('VarSet',at(22),'v=40\nvalue=30');p2+=ctl('ChangeState',at(43),'value=9701\nctrl=0')
 elif kind=='guard':p1+=ctl('AssertInput',win(20,140),'flag='+('L' if face==1 else 'R'));p2+=ctl('ChangeState',at(43),'value=9700\nctrl=0')
 elif kind=='recovery':p2+=ctl('ChangeState',at(43),'value=9701\nctrl=0')
 if os.environ.get('BORUTO_CLONE_DAMAGE'):
  p1+=ctl('PosSet',at(80),f'x={-face*240}\ny=0')
  p2+=ctl('NotHitBy',win(75,210),'value=SCA\ntime=1')
  p2+=ctl('PosSet',at(85)+' && (EnemyNear,NumHelper(9700))>0','x=EnemyNear,Helper(9700),Pos X\ny=0')
  p2+=ctl('ChangeState',at(86),'value=9707\nctrl=0')
inject(char/'BorutoKarmaJogan.cns',p1);inject(dummy/'kfm.cns',p2)
with (dummy/'kfm.cns').open('a') as f:
 for n,fall in [(9700,0),(9701,1)]:
  f.write(f'\n[Statedef {n}]\ntype=S\nmovetype=A\nphysics=N\nctrl=0\nanim=9700\nvelset=0,0\n[State {n}, Real physical probe]\ntype=HitDef\ntrigger1=Time=0\nattr=S,NA\ndamage=60,0\nguardflag=MA\nhitflag=MAF\npausetime=3,5\nground.hittime=16\nground.velocity=-2,{"-7" if fall else "0"}\nair.velocity=-2,-6\nfall={fall}\nfall.recover=0\nhitonce=1\nsparkno=-1\n[State {n}, End]\ntype=ChangeState\ntrigger1=Time>=25\nvalue=0\nctrl=1\n')
 f.write('\n[Statedef 9702]\ntype=A\nmovetype=I\nphysics=N\nanim=41\nvelset=0,0\n[State 9702, Air target]\ntype=Null\ntrigger1=1\n')
 f.write('\n[Statedef 9705]\ntype=A\nmovetype=A\nphysics=N\nanim=9705\nvelset=0,0\n[State 9705, Follow the real opponent]\ntype=PosSet\ntrigger1=NumEnemy>0 && Time<=280\nx=EnemyNear,Pos X\ny=EnemyNear,Pos Y\n[State 9705, Real delayed projectile hit]\ntype=HitDef\ntrigger1=Time=170\nattr=A,NP\ndamage=60,0\nhitflag=MAF\nguardflag=MA\npausetime=0,5\nground.hittime=18\nground.velocity=-2,0\nsparkno=-1\n[State 9705, No push]\ntype=PlayerPush\ntrigger1=1\nvalue=0\n[State 9705, Invisible probe]\ntype=AssertSpecial\ntrigger1=1\nflag=Invisible\n[State 9705, Cleanup]\ntype=DestroySelf\ntrigger1=Time>=195\n')
with (dummy/'kfm.air').open('a') as f:f.write('\n[Begin Action 9700]\nClsn1Default: 1\nClsn1[0]=5,-75,95,-5\nLoopstart\n200,2,0,0,5\n\n[Begin Action 9705]\nClsn1Default: 1\nClsn1[0]=-35,-85,35,10\nLoopstart\n200,2,0,0,5\n')
with (dummy/'kfm.cns').open('a') as f:
 f.write('\n[Statedef 9707]\ntype=S\nmovetype=A\nphysics=N\nctrl=0\nanim=9707\nvelset=0,0\n[State 9707, Real physical attacks on Claw Grime]\ntype=HitDef\ntrigger1=Time=0 || Time=12 || Time=24\nattr=S,NA\ndamage=100,0\nhitflag=MAF\nguardflag=MA\npausetime=3,5\nground.hittime=10\nground.velocity=0,0\nair.velocity=0,0\nfall=0\nsparkno=-1\n[State 9707, Finish]\ntype=ChangeState\ntrigger1=Time>=45\nvalue=0\nctrl=1\n')
with (dummy/'kfm.air').open('a') as f:f.write('\n[Begin Action 9707]\nClsn1Default: 1\nClsn1[0]=-50,-80,50,5\nLoopstart\n200,2,0,0,5\n')
if os.environ.get('BORUTO_LATE_INTERRUPT'):
 p=dummy/'kfm.cns';p.write_text(p.read_text().replace('trigger1=Time=170\nattr=A,NP','trigger1=Time=260\nattr=A,NP').replace('trigger1=Time>=195','trigger1=Time>=290'))
if os.environ.get('BORUTO_UZUHIKO_INTERRUPT'):
 p=dummy/'kfm.cns';p.write_text(p.read_text().replace('trigger1=Time=170\nattr=A,NP','trigger1=Time=75\nattr=A,NP').replace('trigger1=Time>=195','trigger1=Time>=100'))
trace=ENGINE/'boruto_trace.tsv';trace.write_text('');module=ENGINE/'external/mods/boruto_checks.lua'
lua='''modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('boruto_trace.tsv','w'));local last=-1;local rows={};local frames=0
CAPSETUP
hook.add('loop','boruto_checks',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end;last=clock;frames=frames+1
 local case=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 if case>=COUNT then player(2);setLife(1);player(1);setTime(0);return end
 if rows[case]==nil then rows[case]={states={},life=9999,power=3000,maxpower=0,mode=0,timer=0,damage=0,hurt=false,guard=false,lastHP=1000,pulses=0,firstPulse=0,lastPulse=0,held=0,released=false,enemyPower=3000} end
 local r=rows[case];local st=stateNo()
 if tick>5 then
  r.states[st]=true;r.life=math.min(r.life,life());r.power=math.min(r.power,power());r.maxpower=math.max(r.maxpower,power());r.mode=math.max(r.mode,var(42));r.timer=math.max(r.timer,var(40));r.hurt=r.hurt or moveType()=='H';r.guard=r.guard or (st>=120 and st<=155)
  player(2);r.enemyPower=math.min(r.enemyPower,power());local hp=life();r.damage=math.max(r.damage,1000-hp)
  if hp<r.lastHP then r.pulses=r.pulses+1;if r.firstPulse==0 then r.firstPulse=tick end;r.lastPulse=tick end;r.lastHP=hp
  if stateNo()==3010 then r.held=r.held+1 end;if r.held>0 and ctrl() then r.released=true end;player(1)
 end
 if tick==TICKS-1 then local ss={};for n,_ in pairs(r.states) do ss[#ss+1]=tostring(n) end;table.sort(ss)
 f:write(case..'\\t'..table.concat(ss,',')..'\\t'..r.damage..'\\t'..r.life..'\\t'..r.power..'\\t'..r.maxpower..'\\t'..r.mode..'\\t'..r.timer..'\\t'..stateNo()..'\\t'..tostring(ctrl())..'\\t'..numHelper()..'\\t'..var(42)..'\\t'..tostring(r.hurt)..'\\t'..tostring(r.guard)..'\\t'..r.pulses..'\\t'..(r.lastPulse-r.firstPulse)..'\\t'..r.held..'\\t'..tostring(r.released)..'\\t'..(numHelper(9551)+numHelper(9560))..'\\t'..r.enemyPower..'\\n');f:flush() end
 CAPTURE
end)
'''.replace('TICKS',str(TICKS)).replace('COUNT',str(len(cases)))
if CAP:
 folder=Path(CAP);folder.mkdir(parents=True,exist_ok=True);assert not list(folder.glob('Ikemen_GO*.png'))
 lua=lua.replace('CAPSETUP',"modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(folder)+'/')+")\nlocal images=assert(io.open("+json.dumps(str(folder/'frames.tsv'))+",'w'));local cues=assert(io.open("+json.dumps(str(folder/'cues.tsv'))+",'w'));local cap={index=0,pending=nil,last=-1000}")
 lua=lua.replace('CAPTURE','''
 if cap.prev~=st and ((st%10000>=1000 and st%10000<=3000) or st==500 or st==520) then cues:write(frames..'\\t'..case..'\\t'..st..'\\n');cues:flush() end;cap.prev=st
 if cap.pending~=nil then local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb');if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\t'..case..'\\t'..tick..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end end
 if frames-cap.last>=6 and cap.pending==nil and tick>=12 and tick<=CAPEND then screenshot();cap.pending=frames;cap.last=frames end
 '''.replace('FOLDER',json.dumps(str(folder)+'/')).replace('CAPEND','790' if os.environ.get('BORUTO_LONG_CAPTURE') else '385'))
else:lua=lua.replace('CAPSETUP','').replace('CAPTURE','')
if os.environ.get('BORUTO_CLONE_TRACE'):
 clone_trace=Path('/tmp/boruto-review')/('clone-'+uuid.uuid4().hex+'.tsv');Path('/tmp/BorutoKarmaJogan_latest_clone_trace.json').write_text(json.dumps(dict(trace=str(clone_trace)))+'\n')
 lua+="""
local cf=assert(io.open(TRACE,'w'))
hook.add('loop','boruto_clone_observer',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);local ci=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 local values={ci,tick,stateNo(),tostring(ctrl()),life(),power(),numHelper(9700),posX(),facing(),time()}
 local hp,st,age,contact=-1,-1,-1,0
 if numHelper(9700)>0 and helper(9700) then hp=life();st=stateNo();age=var(5);contact=moveHit();player(1) end
 for _,v in ipairs({hp,st,age,contact}) do values[#values+1]=v end
 cf:write(table.concat(values,'\\t')..'\\n');cf:flush()
end)
""".replace('TRACE',json.dumps(str(clone_trace))).replace('TICKS',str(TICKS))
if os.environ.get('BORUTO_CONTACT_TRACE'):
 contact_trace=Path(os.environ['BORUTO_CONTACT_TRACE']);contact_trace.parent.mkdir(parents=True,exist_ok=True)
 lua+="""
local vf=assert(io.open(TRACE,'w'))
hook.add('loop','boruto_visual_contact_observer',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);local ci=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 local values={ci,tick,stateNo(),time(),spriteVar('group'),spriteVar('image'),posX(),posY(),facing(),var(22),tostring(ctrl())}
 player(2)
 for _,v in ipairs({posX(),posY(),life(),stateNo(),tostring(ctrl()),const('size.height')}) do values[#values+1]=v end
 player(1);values[#values+1]=numExplod(9570)
 for _,hid in ipairs({9501,9505,9540}) do
  local count=numHelper(hid);local st,g,n=-1,-1,-1
  if count>0 and helper(hid) then st=stateNo();g=spriteVar('group');n=spriteVar('image');player(1) end
  for _,v in ipairs({count,st,g,n}) do values[#values+1]=v end
 end
 vf:write(table.concat(values,'\\t')..'\\n');vf:flush();player(1)
end)
""".replace('TRACE',json.dumps(str(contact_trace))).replace('TICKS',str(TICKS))
module.write_text(lua);debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/boruto_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
if AUDIO:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=AUDIO,SDL_DISKAUDIODELAY='46')
try:r=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','BorutoCheck','-p1.ai','0','-p2','BorutoDummy','-p2.ai','0','-rounds','1','-time','9999']+(['-speed','0'] if CAP and not os.environ.get('BORUTO_CAPTURE_FAST') else ['-speedtest'])+([] if AUDIO else ['-nosound']),cwd=ENGINE,env=env,capture_output=True,text=True,timeout=300)
finally:debug.write_text(saved);module.rename(module.with_name('-boruto_checks.lua'))
print(r.stdout[-2200:]);print(r.stderr[-2200:]);assert r.returncode==0,'native engine failure'
assert not [l for l in (r.stdout+r.stderr).splitlines() if 'Unknown state controller parameter' in l and "Kung Fu Man's state 1027" not in l], 'Boruto controller warning'
rows=[l.split('\t') for l in trace.read_text().splitlines()];assert len(rows)==len(cases),(len(rows),len(cases));reports=[]
for case,row in zip(cases,rows):
 states=set(map(int,row[1].split(',')));damage=int(row[2]);life=int(row[3]);power=int(row[4]);kind=case['kind'];form=case['form'];bad=[]
 if kind=='move' and (case['state'] not in states or power!=3000-case['cost'] or (damage!=0 if os.environ.get('BORUTO_EXPECT_MISS') else damage<=0)):bad.append('input, cost or collision failed')
 if kind in ['combo','air'] and (case['state'] not in states or damage<100):bad.append('three-hit chain failed')
 if kind in ['ultimate','ultimate_one_hp'] and (damage!=(800 if form else 650) or power!=0 or life!=(1 if kind=='ultimate_one_hp' else 1200)):bad.append('finite ultimate or zero own-life cost failed')
 if kind in ['ultiblock','ultifar','empty'] and (damage or life!=1200):bad.append('guard, range or empty meter ultimate failed')
 if kind in ['ultimate','ultimate_one_hp'] and (row[17]!='true' or row[9]!='true'):bad.append('ultimate did not release the victim')
 if kind=='ult_interrupt' and not (0<damage<(800 if form else 650) and life<1200 and row[9]=='true' and row[17]=='true'):bad.append('real interruption did not stop damage and release the victim')
 if kind=='charge' and (500 not in states or int(row[5])<1000):bad.append('energy charge failed')
 if kind=='awakening' and (520 not in states or int(row[6])!=1 or int(row[7])<1100 or power!=1500):bad.append('Karma Jogan resonance failed')
 if kind=='no_awake' and int(row[6]):bad.append('awakening without power')
 if kind.startswith('expire') and int(row[11]):bad.append('awakening did not expire safely')
 if kind in ['recovery','expire_hurt'] and (life>=1200 or row[9]!='true' or not any(n in states for n in [5000,5010,5020,5030,5050])):bad.append('receiving damage or native recovery failed')
 if kind=='guard' and (life!=1200 or row[13]!='true'):bad.append('native standing guard failed')
 if int(row[10])>int(row[18]) or int(row[18])>2:bad.append('finite helper or aura cap failed')
 record=dict(case=case,states=sorted(states),damage=damage,minimum_life=life,min_power=power,max_power=int(row[5]),form_reached=int(row[6]),max_duration=int(row[7]),end_state=int(row[8]),ctrl=row[9],helpers=int(row[10]),end_form=int(row[11]),hurt=row[12],guard=row[13],damage_pulses=int(row[14]),pulse_span_ticks=int(row[15]),trapped_frames=int(row[16]),victim_released=row[17],aura=int(row[18]),target_minpower=int(row[19]),failures=bad);reports.append(record);print('FAIL' if bad else 'PASS',case['name'],form,case['face'],damage,life,power,bad)
files=['BorutoKarmaJogan.'+s for s in ['def','cns','cmd','air','sff','snd']]+['BorutoKarmaJogan_common.cns'];report=dict(runtime_sha256=hashlib.sha256(b''.join((ROOT/'BorutoKarmaJogan'/f).read_bytes() for f in files)).hexdigest(),cases=reports)
dest=ROOT/'previews'/os.environ.get('BORUTO_REPORT','BorutoKarmaJogan_capture_checks.json' if CAP else 'BorutoKarmaJogan_engine_checks.json');dest.write_text(json.dumps(report,indent=2)+'\n');assert not any(c['failures'] for c in reports),str(dest);print('PASS',len(reports),'actual input checks')
