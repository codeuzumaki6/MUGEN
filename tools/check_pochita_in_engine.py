#!/usr/bin/env python3
"""Raw Xbox-equivalent input and real collision QA in temporary character copies."""
from pathlib import Path
from itertools import product
import os,json,shutil,subprocess,sys,tempfile,re
ROOT=Path(__file__).resolve().parents[1];ENGINE=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly')
DUMMY_LIFE=int(os.environ.get('POCHITA_DUMMY_LIFE','1000'))
character=ENGINE/'chars/PochitaCheck';dummy=ENGINE/'chars/PochitaDummy';shutil.copytree(ROOT/'PochitaTrueForm',character,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(character/'PochitaTrueForm.def',character/'PochitaCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'PochitaDummy.def')
p=dummy/'kfm.cns';base=p.read_text(encoding='latin-1');base=re.sub(r'(?im)^(life\s*=\s*)1000',lambda m:m[1]+str(DUMMY_LIFE),base,count=1);p.write_text(base,encoding='latin-1')
# name, button, relative direction, expected state, cost, kind, distance
specs=[('Desgarro','a','F',1000,250),('Cuatro brazos','a','B',1010,350),('Ascenso','a','D',1020,250),('Estocada','b','F',1030,350),('Barrido','b','B',1040,250),('Guillotina','b','D',1050,500),('Embestida','c','F',1060,500),('Carniceria','c','B',1070,750),('Rasante','c','D',1080,250),('Asalto RT','z','N',1100,750)]
cases=[]
for face in [1,-1]:
 for name,button,direction,state,cost in specs:cases.append(dict(name=name,button=button,direction=direction,state=state,cost=cost,kind='special',facing=face,distance=50 if state in [1020,1040,1080] else 70))
 for name,button,direction,state,cost in specs:cases.append(dict(name=name+' exact budget',button=button,direction=direction,state=state,cost=cost,power=cost,kind='special',facing=face,distance=50 if state in [1020,1040,1080] else 70))
 for name,button,direction,state,cost in specs:
  if state in [1020,1040,1080]:cases.append(dict(name=name+' outside blade reach',button=button,direction=direction,state=state,cost=cost,kind='reachwhiff',facing=face,distance=105))
 for name,button,direction,state,cost in specs:
  if direction in ['F','B']:cases.append(dict(name=name+' diagonal shortcut',button=button,direction=direction,state=state,cost=cost,kind='shortcut',facing=face,distance=50 if state==1040 else 70))
 for button,state in [('a',400),('b',410),('c',420)]:cases.append(dict(name='Low power crouch '+button,button=button,direction='D',state=state,cost=0,kind='crouch',facing=face,distance=42))
 for direction in ['F','B']:
  cases.append(dict(name='Walk '+direction,button='a',direction=direction,state=20,cost=0,kind='walk',facing=face,distance=180))
  cases.append(dict(name='Diagonal jump '+direction,button='U',direction=direction,state=50,cost=0,kind='jump',facing=face,distance=180))
 cases.append(dict(name='Guard incoming strike',button='a',direction='N',state=150,cost=0,kind='guard',facing=face,distance=42))
 for name,button,state in [('Combo X','a',202),('Combo Y','b',212),('Combo B','c',222)]:cases.append(dict(name=name,button=button,direction='N',state=state,cost=0,kind='combo',facing=face,distance=42))
 for sequence in product('abc',repeat=3):
  if len(set(sequence))==1:continue
  states=[{'a':200,'b':210,'c':220}[sequence[0]],{'a':201,'b':211,'c':221}[sequence[1]],{'a':202,'b':212,'c':222}[sequence[2]]]
  expected={'a':32,'b':48,'c':55}[sequence[0]]+{'a':40,'b':42,'c':45}[sequence[1]]+{'a':80,'b':90,'c':105}[sequence[2]]
  cases.append(dict(name='Mixed '+''.join({'a':'X','b':'Y','c':'B'}[b] for b in sequence),button=sequence[0],sequence=sequence,route=states,expected=expected,direction='N',state=states[-1],cost=0,kind='mixedcombo',facing=face,distance=42))
 cases.append(dict(name='Launcher aerial pursuit',button='a',direction='N',state=620,cost=0,kind='pursuit',facing=face,distance=42))
 for kind in ['specialchain','chaincap']:
  cases.append(dict(name='Mixed into two specials'+(' capped' if kind=='chaincap' else ''),button='a',direction='N',state=1010,cost=600,kind=kind,facing=face,distance=42))
 for kind,distance in [('comboblock',42),('combowhiff',220)]:cases.append(dict(name='Mixed XYB '+kind,button='a',sequence=['a','b','c'],direction='N',state=200,finish=222,cost=0,kind=kind,facing=face,distance=distance))
 for kind,distance in [('specialblock',42),('specialwhiff',220)]:cases.append(dict(name=kind,button='a',direction='N',state=200,cost=0,kind=kind,facing=face,distance=distance))
 for button,first,final in [('a',200,202),('b',210,212),('c',220,222)]:
  for kind,distance in [('comboblock',42),('combowhiff',220)]:cases.append(dict(name=kind+' '+button,button=button,direction='N',state=first,finish=final,cost=0,kind=kind,facing=face,distance=distance))
 cases.append(dict(name='Aerial XYZ',button='a',direction='N',state=620,cost=0,kind='aircombo',facing=face,distance=40))
 cases.append(dict(name='RB physical counter',button='y',direction='N',state=1401,cost=250,kind='counter',facing=face,distance=42))
 for variant in ['sweep','bounce','airbounce']:cases.append(dict(name='Get up '+variant,button='a',direction='N',state=5120,cost=0,kind='recovery',variant=variant,facing=face,distance=40))
 for kind,dist in [('ultihit',90),('ultiblock',90),('ultijump',90),('ultifar',320)]:cases.append(dict(name=kind,button='x',direction='N',state=3000,cost=2000,kind=kind,facing=face,distance=dist))
 cases.append(dict(name='Ultimate exact budget',button='x',direction='N',state=3000,cost=2000,power=2000,kind='ultihit',facing=face,distance=90))
 cases.append(dict(name='Neutral jump',button='U',direction='N',state=50,cost=0,kind='jump',facing=face,distance=120))
 cases.append(dict(name='Dash into X',button='a',direction='N',state=200,cost=0,kind='dash',facing=face,distance=140))
cases.extend([dict(name='Insufficient ultimate power',button='x',direction='N',state=3000,cost=2000,kind='empty',facing=1,distance=90),dict(name='LB charge and release',button='s',direction='N',state=500,cost=0,kind='charge',facing=1,distance=120)])
cases.append(dict(name='LB full charge',button='s',direction='N',state=500,cost=0,kind='fullcharge',facing=1,distance=120))
if os.environ.get('POCHITA_AI'):
 cases=[dict(name='CPU offense',button='s',direction='N',state=0,cost=0,kind='ai',facing=1,distance=55)]
if os.environ.get('POCHITA_CASES'):
 names=json.loads(os.environ['POCHITA_CASES']);cases=[c for c in cases if c['name'] in names]
capture=os.environ.get('POCHITA_CAPTURE');TICKS=240
if capture:
 cases=[next(c for c in cases if c['name']==name and c['facing']==1) for name in json.loads(os.environ.get('POCHITA_CAPTURE_CASES','["Combo X"]'))];Path(capture).mkdir(parents=True,exist_ok=True)

def ctl(typ,trig,params):return f'\n[State -2, QA only]\ntype = {typ}\ntriggerall = RoundState = 2\ntrigger1 = {trig}\nignorehitpause = 1\n{params}\n'
clock=ctl('VarAdd','1','v = 58\nvalue = 1');p1=clock;p2=ctl('VarSet','NumEnemy > 0','v = 58\nvalue = EnemyNear,Var(58)')
for variable,effect in [(52,9401),(53,9400),(54,9402)]:p1+=ctl('VarSet','1',f'v = {variable}\nvalue = NumExplod({effect})')
p1+=ctl('VarSet','1','v = 55\nvalue = Time')
if os.environ.get('POCHITA_TRACE'):
 p1+=ctl('VarSet','1','v = 46\nvalue = HitCount')+ctl('VarSet','1','v = 44\nvalue = command = "CuatroBrazos"')
for i,c in enumerate(cases):
 base=i*TICKS;at=lambda t:f'Var(58) = {base+t}';window=lambda a,b:f'Var(58) = [{base+a},{base+b}]';face=c['facing'];kind=c['kind']
 for side in [1,2]:
  x=(-1 if side==1 else 1)*face*c['distance']/2;direction=face if side==1 else -face
  block=ctl('VarSet',at(1),f'v = 59\nvalue = {i}')+ctl('LifeSet',at(1),'value = 1250' if side==1 else f'value = {DUMMY_LIFE}')+ctl('PowerSet',at(1),f'value = {1999 if kind=='empty' else 0 if kind in ['charge','crouch','fullcharge'] else c.get('power',3000)}')+ctl('PosSet',at(1),f'x = {x}\ny = 0')+ctl('VelSet',at(1),'x = 0\ny = 0')+ctl('Turn',at(1)+f' && Facing != {direction}','')+ctl('HitFallSet',at(1),'value = 0')+ctl('ChangeState',at(1),'value = 0\nctrl = 1')
  if side==1:p1+=block
  else:p2+=block
 if kind in ['specialchain','chaincap','specialblock','specialwhiff']:
  # ChangeState at tick 1 stops the -2 pass; clear fixture clocks on tick 2.
  for variable in [42,47,48,49]:p1+=ctl('VarSet',at(2),f'v = {variable}\nvalue = 0')
  if kind=='chaincap':p1+=ctl('VarSet',f'Var(59) = {i} && StateNo = 1010 && Var(32) = 2 && command = "Estocada"','v = 42\nvalue = 1')
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
 if kind in ['charge','fullcharge']:p1+=ctl('AssertInput',window(22,225 if kind=='fullcharge' else 85),'flag = s')
 elif kind=='mixedcombo':
  p1+=ctl('AssertInput',at(press),'flag = '+c['button'])
  for state,button in zip(c['route'][:2],c['sequence'][1:]):p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
 elif kind in ['pursuit','specialchain','chaincap','specialblock','specialwhiff']:
  p1+=ctl('AssertInput',at(press),'flag = a')
  for state,button in ([(200,'a'),(201,'a')] if kind=='pursuit' else [(200,'b')]):p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
  if kind=='pursuit':
   p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = 202 && MoveHit','flag = U')
   p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = 650 && Time = 4','flag = a')
   for state,button in [(600,'b'),(610,'c')]:p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
  else:
   def motion_after_hit(state,variable,direction,button,hits=1):
    condition=f'Var(59) = {i} && StateNo = {state} && Time >= {16 if hits==2 else 6} && MoveHit && Var({variable}) = 0'
    block=ctl('VarSet',condition,f'v = {variable}\nvalue = Var(58)')
    active=f'Var(59) = {i} && Var({variable}) > 0 && '
    side='R' if (direction=='F')==(face==1) else 'L'
    block+=ctl('AssertInput',active+f'Var(58)-Var({variable}) = [0,4]','flag = D')
    block+=ctl('AssertInput',active+f'Var(58)-Var({variable}) = [3,9]','flag = '+side)
    block+=ctl('AssertInput',active+f'Var(58)-Var({variable}) = 8','flag = '+button)
    return block
   p1+=motion_after_hit(211,49,'F','a')+motion_after_hit(1000,48,'B','a',2)
   if kind=='chaincap':p1+=motion_after_hit(1010,47,'F','b')
 elif kind=='combo':
  p1+=ctl('AssertInput',at(press),'flag = '+c['button'])
  for state in [200,201] if c['button']=='a' else [210,211] if c['button']=='b' else [220,221]:p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+c['button'])
 elif kind in ['comboblock','combowhiff']:
  for tick,button in zip([22,44,66],c.get('sequence',[c['button']]*3)):p1+=ctl('AssertInput',at(tick),'flag = '+button)
  if kind=='comboblock':p2+=ctl('AssertInput',window(10,150),'flag = '+('R' if face==1 else 'L'))
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
 if kind=='specialblock':p2+=ctl('AssertInput',window(10,150),'flag = '+('R' if face==1 else 'L'))
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
 if not rows[case] then rows[case]={states={},damage=0,received=0,minpower=3000,maxpower=0,apex=0,vapex=0,last=0,final=0,dx=0,blood=0,slashes=0,ground=0,endfx=0,cancelattempt=0} end
 local r=rows[case]
 r.blood=math.max(r.blood,var(52));r.slashes=math.max(r.slashes,var(53));r.ground=math.max(r.ground,var(54));r.endfx=var(52)+var(53)+var(54)
 if tick>4 then r.cancelattempt=math.max(r.cancelattempt,var(42)) end
 if tick>4 then
  r.states[stateNo()]=true;r.last=stateNo();r.received=math.max(r.received,1250-life());r.minpower=math.min(r.minpower,power());r.maxpower=math.max(r.maxpower,power());r.apex=math.min(r.apex,posY())
  if stateNo()==100 or stateNo()==20 or stateNo()==50 then r.dx=math.max(r.dx,math.abs(posX()-(STARTS)[case+1])) end
  player(2);r.damage=math.max(r.damage,DUMMYMAX-life());r.final=stateNo();r.vapex=math.min(r.vapex,posY());player(1)
 end
 CAPTURE
 if tick==239 and not r.saved then
  r.saved=true;local states={};for k,_ in pairs(r.states) do table.insert(states,k) end;table.sort(states)
  f:write(case..'\\t'..table.concat(states,',')..'\\t'..r.damage..'\\t'..r.received..'\\t'..r.minpower..'\\t'..r.maxpower..'\\t'..r.apex..'\\t'..r.last..'\\t'..r.final..'\\t'..r.dx..'\\t'..r.vapex..'\\t'..r.blood..'\\t'..r.slashes..'\\t'..r.ground..'\\t'..r.endfx..'\\t'..r.cancelattempt..'\\n');f:flush()
 end
end)
'''.replace('DUMMYMAX',str(DUMMY_LIFE)).replace('COUNT',str(len(cases))).replace('STARTS','{'+','.join(str(-c['facing']*c['distance']/2) for c in cases)+'}')
if os.environ.get('POCHITA_TRACE'):
 module="local tracefile=assert(io.open("+json.dumps(os.environ['POCHITA_TRACE'])+",'w'))\n"+module
 module=module.replace(' CAPTURE'," tracefile:write(t..','..stateNo()..','..var(55)..','..var(32)..','..var(49)..','..var(48)..','..var(46)..','..var(44)..string.char(10));tracefile:flush()\n CAPTURE",1)
if capture:
 module="modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(Path(capture).resolve())+'/')+")\n"+module
if capture:
 directory=json.dumps(str(Path(capture).resolve())+'/')
 prefix="local cap={index=0,last=-1000,pending=nil,state=-1,hp=1000,lastut=-1}\nlocal capdir="+directory+"\nlocal framefile=assert(io.open(capdir..'frames.tsv','w'))\nlocal audiofile=assert(io.open(capdir..'audio.tsv','w'))\nlocal function cue(t,n) audiofile:write(t..string.char(9)..n..string.char(10));audiofile:flush() end\n"
 module=prefix+module
 capturecode="""
 local st=stateNo();local stime=var(55)
 if st~=cap.state then
  local sounds={[200]=0,[201]=0,[202]=1,[210]=0,[211]=1,[212]=7,[220]=0,[221]=1,[222]=8,[600]=0,[610]=0,[620]=0,[3000]=3,[1000]=1,[1010]=1,[1020]=1,[1030]=1,[1040]=1,[1050]=1,[1060]=1,[1070]=3,[1080]=1,[1100]=3}
  if sounds[st]~=nil then cue(t,sounds[st]) end
  cap.state=st;cap.lastut=-1
 end
 if st==3001 and stime~=cap.lastut then
  if stime==8 or stime==40 or stime==72 then cue(t,7) end
  if stime==30 or stime==42 or stime==54 or stime==66 then cue(t,8) end
  if stime==92 then cue(t,9) end
  cap.lastut=stime
 end
 player(2);local hp=life();player(1)
 if hp<cap.hp and st~=3001 then cue(t,st==212 and 7 or st==222 and 9 or 5) end
 cap.hp=hp
 if cap.pending~=nil then
  local png=io.open(capdir..string.format('Ikemen_GO%03d.png',cap.index),'rb')
  if png~=nil then png:close();framefile:write(cap.index..string.char(9)..cap.pending..string.char(10));framefile:flush();cap.index=cap.index+1;cap.pending=nil end
 end
 if tick>=12 and tick<=228 and tick-cap.last>=4 and cap.pending==nil then
  screenshot();cap.pending=tick;cap.last=tick
 end
 """
 module=module.replace('CAPTURE',capturecode)
else:module=module.replace('CAPTURE','')
(ENGINE/'external/mods/pochita_checks.lua').write_text(module);(ENGINE/'pochita_checks.tsv').write_text('')
debug=ENGINE/'external/script/debug.lua';original=debug.read_text();debug.write_text(original+"\ndofile('external/mods/pochita_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
try:
 r=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','PochitaCheck','-p2','PochitaDummy','-p1.ai',os.environ.get('POCHITA_AI','0'),'-p2.ai','0','-rounds','1','-time',str(max(600,len(cases)*4+30)),'-nosound']+(['-speed','0'] if capture else ['-speedtest']),cwd=ENGINE,env=env,capture_output=True,text=True,timeout=90)
 print(r.stdout);print(r.stderr);assert r.returncode==0,r.returncode
finally:
 debug.write_text(original);(ENGINE/'external/mods/pochita_checks.lua').rename(ENGINE/'external/mods/-pochita_checks.lua')
raw={}
for line in (ENGINE/'pochita_checks.tsv').read_text().splitlines():raw.setdefault(int(line.split('\t')[0]),line)
assert sorted(raw)==list(range(len(cases))),sorted(raw)
report=[];errors=[]
for i,c in enumerate(cases):
 _,states,damage,received,minimum,maximum,apex,last,final,dx,vapex,blood,slashes,ground,endfx,attempt=raw[i].split('\t');states=set(map(int,states.split(',')));damage=int(damage);minimum=int(minimum);kind=c['kind'];fail=[]
 if kind=='empty':
  if 3000 in states:fail.append('ultimate spent unavailable power')
 else:
  if c['state'] not in states:fail.append('expected state not reached')
  if c['cost'] and minimum!=c.get('power',3000)-c['cost']:fail.append('power cost differs from advertised reduced cost')
 if kind=='ai' and (damage<=0 or not {200,201,202,210,211,220,221,1030,3000}.intersection(states)):fail.append('CPU did not use its real offensive states')
 if kind in ['combo','special','shortcut','crouch','aircombo','counter'] and damage<=0:fail.append('no collision damage')
 if kind in ['comboblock','combowhiff'] and (c['finish'] in states or damage>40):fail.append('third combo hit occurred without confirming earlier hits')
 if kind=='combowhiff' and damage!=0:fail.append('missed normal caused damage')
 if kind=='aircombo' and (not {600,610,620}.issubset(states) or damage<172):fail.append('air links failed')
 if kind=='combo' and damage<{'a':152,'b':180,'c':205}[c['button']]:fail.append('not every normal actually hit')
 if kind=='mixedcombo' and (not set(c['route']).issubset(states) or damage!=c['expected']):fail.append('mixed route failed to connect every physical hit')
 if kind=='pursuit' and (not {200,201,202,650,600,610,620}.issubset(states) or damage<324 or int(last)!=0):fail.append('physical launcher/pursuit/air finisher failed')
 if kind in ['specialchain','chaincap'] and (not {200,211,1000,1010}.issubset(states) or damage<200):fail.append('mixed normal into two paid specials failed')
 if kind=='chaincap' and 1030 in states:fail.append('third special bypassed the two-special sequence limit')
 if kind=='chaincap' and int(attempt)!=1:fail.append('third-special input was not recognized during the cap test')
 if kind in ['specialblock','specialwhiff'] and ({1000,1010}.intersection(states) or minimum!=3000 or int(blood)>0):fail.append('special cancel occurred without a real hit')
 if kind=='specialwhiff' and damage!=0:fail.append('missed cancel route caused damage')
 if kind=='combo' and c['button']=='a' and not 20<=-float(vapex)<=80:fail.append('launcher height outside the intended camera range')
 if kind=='charge' and (int(maximum)<1000 or int(last)==500):fail.append('charge failed or did not release')
 if kind=='fullcharge' and (int(maximum)!=3000 or int(last)==500):fail.append('full charge failed to cap/release')
 if kind=='recovery' and (int(received)<=0 or not {5110,5120,200}.issubset(states)):fail.append('actual knockdown/get-up/new attack failed')
 if kind in ['combo','aircombo','ultihit'] and (int(blood)==0 or int(slashes)==0):fail.append('confirmed finisher has no slash/blood effects')
 if kind!='ai' and int(endfx)!=0:fail.append('visual effects failed to expire')
 if kind=='ai' and int(endfx)>6:fail.append('ongoing CPU combat accumulated too many effects')
 if kind in ['ultiblock','ultijump','ultifar','combowhiff','comboblock'] and int(blood)>0:fail.append('blood emitted without a real hit')
 if kind=='ultihit' and (damage!=min(500,DUMMY_LIFE//2) or 3001 not in states or int(final) in [3010,3011]):fail.append('confirmed ultimate damage/release failed')
 if kind in ['ultiblock','ultijump','ultifar'] and (damage>0 or 3001 in states):fail.append('ultimate could not be avoided')
 if kind=='reachwhiff' and (damage!=0 or int(last)!=0):fail.append('short blade hit outside visible reach or failed to recover')
 if kind=='jump' and not 45<=-float(apex)<=75:fail.append('neutral jump height outside intended range')
 if kind=='jump' and (int(last)!=0 or (c['direction']!='N' and float(dx)<15)):fail.append('jump landing or diagonal travel failed')
 if kind=='walk' and (float(dx)<20 or int(last)!=0):fail.append('walk/release failed')
 if kind=='guard' and (int(received)!=0 or 150 not in states):fail.append('incoming strike not blocked')
 if kind=='dash' and (100 not in states or float(dx)<10):fail.append('dash failed to move/cancel')
 row=dict(case=c,states=sorted(states),damage=damage,received=int(received),minimum_power=minimum,maximum_power=int(maximum),apex=float(apex),victim_apex=float(vapex),blood_effects=int(blood),slash_effects=int(slashes),ground_effects=int(ground),effects_at_end=int(endfx),third_special_input_recognized=int(attempt),last=int(last),victim_final=int(final),dash_travel=float(dx),failures=fail);report.append(row);errors+=fail;print('FAIL' if fail else 'PASS',c['name'],c['facing'],row)
path=ROOT/'previews'/(('Pochita_flow_visual_checks.json' if os.environ.get('POCHITA_PREVIEW_SET')=='flow' else 'Pochita_engine_visual_checks.json') if capture else 'Pochita_low_life_ultimate_checks.json' if DUMMY_LIFE!=1000 else 'Pochita_AI_checks.json' if os.environ.get('POCHITA_AI') else 'Pochita_engine_checks.json');path.write_text(json.dumps(report,indent=2)+'\n');assert not errors,errors
print('PASSED',len(report),'raw-input/collision scenarios')
