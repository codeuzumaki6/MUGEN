#!/usr/bin/env python3
"""Raw Xbox-equivalent input and real collision QA in temporary character copies."""
from pathlib import Path
import os,json,shutil,subprocess,sys,tempfile,re
ROOT=Path(__file__).resolve().parents[1];ENGINE=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly')
character=ENGINE/'chars/PochitaCheck';dummy=ENGINE/'chars/PochitaDummy';shutil.copytree(ROOT/'PochitaTrueForm',character,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(character/'PochitaTrueForm.def',character/'PochitaCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'PochitaDummy.def')
# name, button, relative direction, expected state, cost, kind, distance
specs=[('Desgarro','a','F',1000,500),('Cuatro brazos','a','B',1010,750),('Ascenso','a','D',1020,500),('Estocada','b','F',1030,750),('Barrido','b','B',1040,500),('Guillotina','b','D',1050,1000),('Embestida','c','F',1060,1000),('Carniceria','c','B',1070,1500),('Rasante','c','D',1080,500),('Asalto RT','z','N',1100,1500)]
cases=[]
for face in [1,-1]:
 for name,button,direction,state,cost in specs:cases.append(dict(name=name,button=button,direction=direction,state=state,cost=cost,kind='special',facing=face,distance=70))
 for name,button,direction,state,cost in specs:
  if direction in ['F','B']:cases.append(dict(name=name+' diagonal shortcut',button=button,direction=direction,state=state,cost=cost,kind='shortcut',facing=face,distance=70))
 for button,state in [('a',400),('b',410),('c',420)]:cases.append(dict(name='Low power crouch '+button,button=button,direction='D',state=state,cost=0,kind='crouch',facing=face,distance=42))
 for direction in ['F','B']:
  cases.append(dict(name='Walk '+direction,button='a',direction=direction,state=20,cost=0,kind='walk',facing=face,distance=180))
  cases.append(dict(name='Diagonal jump '+direction,button='U',direction=direction,state=50,cost=0,kind='jump',facing=face,distance=180))
 cases.append(dict(name='Guard incoming strike',button='a',direction='N',state=150,cost=0,kind='guard',facing=face,distance=42))
 for name,button,state in [('Combo X','a',202),('Combo Y','b',211),('Combo B','c',221)]:cases.append(dict(name=name,button=button,direction='N',state=state,cost=0,kind='combo',facing=face,distance=42))
 cases.append(dict(name='Aerial XYZ',button='a',direction='N',state=620,cost=0,kind='aircombo',facing=face,distance=40))
 cases.append(dict(name='RB physical counter',button='y',direction='N',state=1401,cost=500,kind='counter',facing=face,distance=42))
 for variant in ['sweep','bounce','airbounce']:cases.append(dict(name='Get up '+variant,button='a',direction='N',state=5120,cost=0,kind='recovery',variant=variant,facing=face,distance=40))
 for kind,dist in [('ultihit',90),('ultiblock',90),('ultijump',90),('ultifar',320)]:cases.append(dict(name=kind,button='x',direction='N',state=3000,cost=3000,kind=kind,facing=face,distance=dist))
 cases.append(dict(name='Neutral jump',button='U',direction='N',state=50,cost=0,kind='jump',facing=face,distance=120))
 cases.append(dict(name='Dash into X',button='a',direction='N',state=200,cost=0,kind='dash',facing=face,distance=140))
cases.extend([dict(name='Insufficient ultimate power',button='x',direction='N',state=3000,cost=3000,kind='empty',facing=1,distance=90),dict(name='LB charge and release',button='s',direction='N',state=500,cost=0,kind='charge',facing=1,distance=120)])
if os.environ.get('POCHITA_AI'):
 cases=[dict(name='CPU offense',button='s',direction='N',state=0,cost=0,kind='ai',facing=1,distance=55)]
if os.environ.get('POCHITA_CASES'):
 names=json.loads(os.environ['POCHITA_CASES']);cases=[c for c in cases if c['name'] in names]
capture=os.environ.get('POCHITA_CAPTURE');TICKS=240
if capture:
 cases=[next(c for c in cases if c['name']==name and c['facing']==1) for name in json.loads(os.environ.get('POCHITA_CAPTURE_CASES','["Combo X"]'))];Path(capture).mkdir(parents=True,exist_ok=True)

def ctl(typ,trig,params):return f'\n[State -2, QA only]\ntype = {typ}\ntriggerall = RoundState = 2\ntrigger1 = {trig}\nignorehitpause = 1\n{params}\n'
clock=ctl('VarAdd','1','v = 58\nvalue = 1');p1=clock;p2=clock
for i,c in enumerate(cases):
 base=i*TICKS;at=lambda t:f'Var(58) = {base+t}';window=lambda a,b:f'Var(58) = [{base+a},{base+b}]';face=c['facing'];kind=c['kind']
 for side in [1,2]:
  x=(-1 if side==1 else 1)*face*c['distance']/2;direction=face if side==1 else -face
  block=ctl('VarSet',at(1),f'v = 59\nvalue = {i}')+ctl('LifeSet',at(1),'value = 1100' if side==1 else 'value = 1000')+ctl('PowerSet',at(1),f'value = {0 if kind in ["empty","charge","crouch"] else 3000}')+ctl('PosSet',at(1),f'x = {x}\ny = 0')+ctl('VelSet',at(1),'x = 0\ny = 0')+ctl('Turn',at(1)+f' && Facing != {direction}','')+ctl('HitFallSet',at(1),'value = 0')+ctl('ChangeState',at(1),'value = 0\nctrl = 1')
  if side==1:p1+=block
  else:p2+=block
 d=c['direction']
 if d in ['F','B'] and kind in ['walk','shortcut','jump']:
  side='R' if (d=='F')==(face==1) else 'L';p1+=ctl('AssertInput',window(18,55 if kind=='walk' else 24),'flag = '+side);press=22
  if kind=='shortcut':p1+=ctl('AssertInput',window(18,24),'flag = D')
 elif d in ['F','B']:
  side='R' if (d=='F')==(face==1) else 'L';p1+=ctl('AssertInput',window(18,24),'flag = D')+ctl('AssertInput',window(22,29),'flag = '+side);press=27
 elif d=='D':p1+=ctl('AssertInput',window(18,24),'flag = D');press=22
 else:press=22
 if kind=='recovery':
  if c['variant']=='airbounce':p1+=ctl('PosSet',at(12),'y = -70')+ctl('VelSet',at(12),'y = -2')+ctl('ChangeState',at(12),'value = 50\nctrl = 0')
  p2+=ctl('ChangeState',at(20),f'value = {9700 if c["variant"]=="sweep" else 9701}\nctrl = 0');press=200
 if kind=='counter':p2+=ctl('ChangeState',at(28),'value = 9701\nctrl = 0')
 if kind=='guard':
  p1+=ctl('AssertInput',window(24,70),'flag = '+('L' if face==1 else 'R'));p2+=ctl('ChangeState',at(28),'value = 9701\nctrl = 0')
 if kind=='charge':p1+=ctl('AssertInput',window(22,85),'flag = s')
 elif kind=='combo':
  p1+=ctl('AssertInput',at(press),'flag = '+c['button'])
  for state in [200,201] if c['button']=='a' else [210] if c['button']=='b' else [220]:p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+c['button'])
 elif kind=='aircombo':
  for side in [1,2]:
   b=ctl('PosSet',window(12,115),'y = -60')+ctl('VelSet',window(12,115),'y = 0')+ctl('ChangeState',at(12),'value = 50\nctrl = '+('1' if side==1 else '0'))
   if side==1:p1+=b
   else:p2+=b
  p1+=ctl('AssertInput',at(22),'flag = a')
  for state,button in [(600,'b'),(610,'c')]:p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
 elif kind=='dash':
  for a,b in [(12,14),(18,32)]:p1+=ctl('AssertInput',window(a,b),'flag = '+('R' if face==1 else 'L'))
  p1+=ctl('AssertInput',at(30),'flag = a')
 elif kind not in ['walk','guard']:p1+=ctl('AssertInput',at(press),'flag = '+c['button'])
 if kind=='ultiblock':p2+=ctl('AssertInput',window(10,150),'flag = '+('R' if face==1 else 'L'))
 if kind=='ultijump':p2+=ctl('ChangeState',at(12),'value = 50\nctrl = 0')+ctl('PosSet',window(12,150),'y = -180')+ctl('VelSet',window(12,150),'y = 0')
# Real test strikes: do not put the tested character into a get-up state.
for state,anim,yvel,typ in [(9700,440,0,'Trip'),(9701,210,-4,'High')]:
 with (dummy/'kfm.cns').open('a') as f:f.write(f'''\n[Statedef {state}]
type = S
movetype = A
physics = S
anim = {anim}
ctrl = 0
[State {state}, Collision]
type = HitDef
trigger1 = Time = 0
attr = S, NA
damage = 60,0
hitflag = MAF
guardflag = MA
pausetime = 5,8
ground.type = {typ}
ground.hittime = 18
ground.velocity = -2,-5
air.velocity = -2,-5
fall = 1
fall.yvelocity = {yvel}
fall.recover = 0
sparkno = -1
[State {state}, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 0
''')
for path,block in [(character/'PochitaTrueForm.cns',p1),(dummy/'kfm.cns',p2)]:
 text=path.read_text(encoding='latin-1');marker=re.search(r'(?im)^\[statedef -2\]',text)
 if marker:text=text[:marker.end()]+'\n'+block+'\n'+text[marker.end():]
 else:text+='\n[Statedef -2]\n'+block
 path.write_text(text,encoding='latin-1')
module='''local f=assert(io.open('pochita_checks.tsv','w'))
local rows={};local frame=-1
hook.add('loop','pochita_qa',function()
 if not player(1) or roundState()~=2 then return end
 local t=var(58);if t==frame or t<1 then return end;frame=t
 local case=math.floor((t-1)/240);local tick=(t-1)%240+1
 if case>=COUNT then player(2);setLife(100);player(1);setTime(0);return end
 if not rows[case] then rows[case]={states={},damage=0,received=0,minpower=3000,maxpower=0,apex=0,last=0,final=0,dx=0} end
 local r=rows[case]
 if tick>4 then
  r.states[stateNo()]=true;r.last=stateNo();r.received=math.max(r.received,1100-life());r.minpower=math.min(r.minpower,power());r.maxpower=math.max(r.maxpower,power());r.apex=math.min(r.apex,posY())
  if stateNo()==100 or stateNo()==20 or stateNo()==50 then r.dx=math.max(r.dx,math.abs(posX()-(STARTS)[case+1])) end
  player(2);r.damage=math.max(r.damage,1000-life());r.final=stateNo();player(1)
 end
 CAPTURE
 if tick==239 and not r.saved then
  r.saved=true;local states={};for k,_ in pairs(r.states) do table.insert(states,k) end;table.sort(states)
  f:write(case..'\\t'..table.concat(states,',')..'\\t'..r.damage..'\\t'..r.received..'\\t'..r.minpower..'\\t'..r.maxpower..'\\t'..r.apex..'\\t'..r.last..'\\t'..r.final..'\\t'..r.dx..'\\n');f:flush()
 end
end)
'''.replace('COUNT',str(len(cases))).replace('STARTS','{'+','.join(str(-c['facing']*c['distance']/2) for c in cases)+'}')
if capture:
 module="modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(Path(capture).resolve())+'/')+")\n"+module
module=module.replace('CAPTURE','if tick>=12 and tick<=228 and tick%4==0 then screenshot() end' if capture else '')
(ENGINE/'external/mods/pochita_checks.lua').write_text(module);(ENGINE/'pochita_checks.tsv').write_text('')
debug=ENGINE/'external/script/debug.lua';original=debug.read_text();debug.write_text(original+"\ndofile('external/mods/pochita_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
try:
 r=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','PochitaCheck','-p2','PochitaDummy','-p1.ai',os.environ.get('POCHITA_AI','0'),'-p2.ai','0','-rounds','1','-time','600','-nosound']+(['-speed','0'] if capture else ['-speedtest']),cwd=ENGINE,env=env,capture_output=True,text=True,timeout=60)
 print(r.stdout);print(r.stderr);assert r.returncode==0,r.returncode
finally:
 debug.write_text(original);(ENGINE/'external/mods/pochita_checks.lua').rename(ENGINE/'external/mods/-pochita_checks.lua')
raw={}
for line in (ENGINE/'pochita_checks.tsv').read_text().splitlines():raw.setdefault(int(line.split('\t')[0]),line)
assert sorted(raw)==list(range(len(cases))),sorted(raw)
report=[];errors=[]
for i,c in enumerate(cases):
 _,states,damage,received,minimum,maximum,apex,last,final,dx=raw[i].split('\t');states=set(map(int,states.split(',')));damage=int(damage);minimum=int(minimum);kind=c['kind'];fail=[]
 if kind=='empty':
  if 3000 in states:fail.append('ultimate spent unavailable power')
 else:
  if c['state'] not in states:fail.append('expected state not reached')
  if c['cost'] and minimum>3000-c['cost']:fail.append('power cost missing')
 if kind=='ai' and (damage<=0 or not {200,201,202,210,211,220,221,1030,3000}.intersection(states)):fail.append('CPU did not use its real offensive states')
 if kind in ['combo','special','shortcut','crouch','aircombo','counter'] and damage<=0:fail.append('no collision damage')
 if kind=='aircombo' and (not {600,610,620}.issubset(states) or damage<139):fail.append('air links failed')
 if kind=='combo' and damage<{'a':126,'b':104,'c':118}[c['button']]:fail.append('not every normal actually hit')
 if kind=='charge' and (int(maximum)<500 or int(last)==500):fail.append('charge failed or did not release')
 if kind=='recovery' and (int(received)<=0 or not {5110,5120,200}.issubset(states)):fail.append('actual knockdown/get-up/new attack failed')
 if kind=='ultihit' and (damage!=350 or 3001 not in states or int(final) in [3010,3011]):fail.append('confirmed ultimate damage/release failed')
 if kind in ['ultiblock','ultijump','ultifar'] and (damage>0 or 3001 in states):fail.append('ultimate could not be avoided')
 if kind=='jump' and not 45<=-float(apex)<=75:fail.append('neutral jump height outside intended range')
 if kind=='jump' and (int(last)!=0 or (c['direction']!='N' and float(dx)<15)):fail.append('jump landing or diagonal travel failed')
 if kind=='walk' and (float(dx)<20 or int(last)!=0):fail.append('walk/release failed')
 if kind=='guard' and (int(received)!=0 or 150 not in states):fail.append('incoming strike not blocked')
 if kind=='dash' and (100 not in states or float(dx)<10):fail.append('dash failed to move/cancel')
 row=dict(case=c,states=sorted(states),damage=damage,received=int(received),minimum_power=minimum,maximum_power=int(maximum),apex=float(apex),last=int(last),victim_final=int(final),dash_travel=float(dx),failures=fail);report.append(row);errors+=fail;print('FAIL' if fail else 'PASS',c['name'],c['facing'],row)
path=ROOT/'previews'/('Pochita_engine_visual_checks.json' if capture else 'Pochita_AI_checks.json' if os.environ.get('POCHITA_AI') else 'Pochita_engine_checks.json');path.write_text(json.dumps(report,indent=2)+'\n');assert not errors,errors
print('PASSED',len(report),'raw-input/collision scenarios')
