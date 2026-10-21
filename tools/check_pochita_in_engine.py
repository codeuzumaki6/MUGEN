#!/usr/bin/env python3
"""Raw Xbox-equivalent input and real collision QA in temporary character copies."""
from pathlib import Path
from itertools import product
import os,json,shutil,subprocess,sys,tempfile,re
ROOT=Path(__file__).resolve().parents[1];ENGINE=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly')
DUMMY_LIFE=int(os.environ.get('POCHITA_DUMMY_LIFE','1000'))
EXTENSION=bool(os.environ.get('POCHITA_DEVOUR_CHECK'))
KO_CHECK=bool(os.environ.get('POCHITA_KO_CHECK'))
AIR_SCARF=bool(os.environ.get('POCHITA_AIR_SCARF_CHECK'))
POLISH=bool(os.environ.get('POCHITA_POLISH_CHECK'))
VICTORY=bool(os.environ.get('POCHITA_WIN_CHECK'))
CHOREOGRAPHY=json.loads((ROOT/'PochitaTrueForm/assets/special_choreography.json').read_text())
character=ENGINE/'chars/PochitaCheck';dummy=ENGINE/'chars/PochitaDummy';shutil.copytree(ROOT/'PochitaTrueForm',character,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(character/'PochitaTrueForm.def',character/'PochitaCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'PochitaDummy.def')
p=dummy/'kfm.cns';base=p.read_text(encoding='latin-1');base=re.sub(r'(?im)^(life\s*=\s*)1000',lambda m:m[1]+str(DUMMY_LIFE),base,count=1);p.write_text(base,encoding='latin-1')
# name, button, relative direction, expected state, cost, kind, distance
specs=[('Desgarro','a','F',1000,250),('Cuatro brazos','a','B',1010,350),('Ascenso','a','D',1020,250),('Estocada','b','F',1030,350),('Barrido','b','B',1040,250),('Guillotina','b','D',1050,500),('Embestida','c','F',1060,500),('Carniceria','c','B',1070,750),('Rasante','c','D',1080,250),('Asalto RT','z','N',1100,750),('Devastacion','x','D',1500,1000)]
cases=[]
for face in [1,-1]:
 for name,button,direction,state,cost in specs:cases.append(dict(name=name,button=button,direction=direction,state=state,cost=cost,kind='special',facing=face,distance=50 if state in [1020,1040,1080] else 70))
 for name,button,direction,state,cost in specs:cases.append(dict(name=name+' exact budget',button=button,direction=direction,state=state,cost=cost,power=cost,kind='special',facing=face,distance=50 if state in [1020,1040,1080] else 70))
 for name,button,direction,state,cost in specs:
  if state in [1000,1010,1030,1040,1060,1070]:
   cases.append(dict(name=name+' insufficient power',button=button,direction=direction,state={'a':200,'b':210,'c':220}[button],forbidden=state+10000,cost=0,power=cost-1,kind='emptyspecial',facing=face,distance=220))
   cases.append(dict(name=name+' startup whiff',button=button,direction=direction,state=state,cost=cost,kind='startupwhiff',facing=face,distance=300))
   cases.append(dict(name=name+' guarded sequence',button=button,direction=direction,state=state,cost=cost,kind='specialguard',facing=face,distance=50 if state==1040 else 70))
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
 cases.append(dict(name='Launcher aerial pursuit',button='a',direction='N',state=672,cost=0,kind='pursuit',facing=face,distance=42))
 for kind in ['specialchain','chaincap']:
  cases.append(dict(name='Mixed into two specials'+(' capped' if kind=='chaincap' else ''),button='a',direction='N',state=1010,cost=600,kind=kind,facing=face,distance=42))
 for kind,distance in [('comboblock',42),('combowhiff',220)]:cases.append(dict(name='Mixed XYB '+kind,button='a',sequence=['a','b','c'],direction='N',state=200,finish=222,cost=0,kind=kind,facing=face,distance=distance))
 for kind,distance in [('specialblock',42),('specialwhiff',220)]:cases.append(dict(name=kind,button='a',direction='N',state=200,cost=0,kind=kind,facing=face,distance=distance))
 for button,first,final in [('a',200,202),('b',210,212),('c',220,222)]:
  for kind,distance in [('comboblock',42),('combowhiff',220)]:cases.append(dict(name=kind+' '+button,button=button,direction='N',state=first,finish=final,cost=0,kind=kind,facing=face,distance=distance))
 cases.append(dict(name='Aerial XYZ',button='a',direction='N',state=672,cost=0,kind='aircombo',facing=face,distance=40))
 cases.append(dict(name='RB physical counter',button='y',direction='N',state=1401,cost=250,kind='counter',facing=face,distance=42))
 for variant in ['sweep','bounce','airbounce']:cases.append(dict(name='Get up '+variant,button='a',direction='N',state=5120,cost=0,kind='recovery',variant=variant,facing=face,distance=40))
 for kind,dist in [('ultihit',90),('ultiblock',90),('ultijump',90),('ultifar',320)]:cases.append(dict(name=kind,button='x',direction='N',state=3000,cost=2000,kind=kind,facing=face,distance=dist))
 cases.append(dict(name='Ultimate exact budget',button='x',direction='N',state=3000,cost=2000,power=2000,kind='ultihit',facing=face,distance=90))
 cases.append(dict(name='Neutral jump',button='U',direction='N',state=50,cost=0,kind='jump',facing=face,distance=120))
 cases.append(dict(name='Dash into X',button='a',direction='N',state=200,cost=0,kind='dash',facing=face,distance=140))
cases.extend([dict(name='Insufficient ultimate power',button='x',direction='N',state=3000,cost=2000,kind='empty',facing=1,distance=90),dict(name='LB charge and release',button='s',direction='N',state=500,cost=0,kind='charge',facing=1,distance=120)])
cases.append(dict(name='LB full charge',button='s',direction='N',state=500,cost=0,kind='fullcharge',facing=1,distance=120))
if EXTENSION:
 cases=[]
 for face in [1,-1]:
  for kind,hp,power in [('awake_wounded',800,3000),('awake_cap',1240,3000),('awake_full',1250,3000),('awake_empty',800,2999),('awake_held',800,3000),('awake_attack',800,3000),('awake_special',800,3000),('awake_counterhit',800,3000),('awake_cooldown',800,3000),('awake_again',800,3000)]:
   cases.append(dict(name=kind,button='s',direction='D',state=520,cost=0 if kind=='awake_empty' else 1250 if kind=='awake_special' else 1000,life=hp,power=power,kind=kind,facing=face,distance=42 if kind in ['awake_attack','awake_counterhit'] else 70 if kind=='awake_special' else 140))
  for name,kind,button,direction,state,cost,dist in [('Estocada con avance','rangeapproach','b','F',1030,350,200),('Estocada bloqueada','approachblock','b','F',1030,350,200),('Estocada fuera de alcance','approachmiss','b','F',1030,350,280),('Estocada interrumpida','approachbreak','b','F',1030,350,42),('RT lejano','rangerush','z','N',1100,750,180),('Embestida lejana','rangerush','c','F',1060,500,170),('Desgarro lejano','rangerush','a','F',1000,250,150)]:
   cases.append(dict(name=name,button=button,direction=direction,state=state,cost=cost,kind=kind,facing=face,distance=dist))
  for kind,dist,power in [('devour_interrupted',42,3000),('devour_escape',90,3000)]:cases.append(dict(name=kind,button='x',direction='N',state=3000,cost=2000,power=power,kind=kind,facing=face,distance=dist))
  for kind,dist,power in [('oldhit',90,3000),('oldblock',90,3000),('oldfar',320,3000),('oldempty',90,999)]:cases.append(dict(name=kind,button='x',direction='D',state=1500,cost=1000 if kind!='oldempty' else 0,power=power,kind=kind,facing=face,distance=dist))
if AIR_SCARF:
 cases=[]
 for face in [1,-1]:
  for sequence in product('abc',repeat=3):
   route=[{'a':600,'b':610,'c':620}[sequence[0]],660+'abc'.index(sequence[1]),670+'abc'.index(sequence[2])]
   expected={'a':50,'b':52,'c':70}[sequence[0]]+{'a':45,'b':55,'c':55}[sequence[1]]+{'a':85,'b':95,'c':100}[sequence[2]]
   cases.append(dict(name='Air '+''.join({'a':'X','b':'Y','c':'B'}[b] for b in sequence),button=sequence[0],sequence=sequence,route=route,expected=expected,direction='N',state=route[-1],cost=0,kind='airmixed',facing=face,distance=40))
  for kind,dist in [('airmiss',260),('airguard',40),('aircap',40),('airlate',40)]:
   cases.append(dict(name=kind,button='a',sequence=['a','b','c'],route=[600,661,672],expected=205,direction='N',state=600,cost=0,kind=kind,facing=face,distance=dist))
if AIR_SCARF:
 for face in [1,-1]:
  for button,state,cost in [('y',1200,350),('z',1210,600)]:
   for variant in ['hit','block','miss','jump','empty','exact','break','escape']+(['followup'] if state==1200 else []):
    cases.append(dict(name=('Lazo RB ' if state==1200 else 'Agarre RT ')+variant,button=button,direction='D',state=state,cost=0 if variant=='empty' else cost,power=cost-1 if variant=='empty' else cost if variant=='exact' else 3000,kind='scarf_'+variant,facing=face,distance=250 if variant=='miss' else 90))
if POLISH:
 cases=[]
 for face in [1,-1]:
  for name,kind,state,button,dist in [('Carga con motores','charge',500,'s',180),('Carga completa','fullcharge',500,'s',180),('Carga interrumpida','charge_interrupted',500,'s',42),('Carrera frenado','polishdash',106,'a',300),('Salto aterrizaje','jump',50,'U',180),('Remate X','combo',202,'a',42),('Remate bloqueado','comboblock',200,'a',42),('Remate fallado','combowhiff',200,'a',220)]:
   cases.append(dict(name=name,kind=kind,state=state,button=button,direction='N',distance=dist,finish=202,cost=0,facing=face))
if VICTORY:cases=[dict(name='Victoria real',kind='victory',state=180,button='a',direction='N',distance=42,cost=0,facing=int(os.environ.get('POCHITA_WIN_FACING','1')))]
if KO_CHECK:cases=[dict(name='awakening KO',button='s',direction='D',state=520,cost=1000,life=800,power=3000,kind='awake_ko',facing=1,distance=140)]
if os.environ.get('POCHITA_AI'):
 cases=[dict(name='CPU offense',button='s',direction='N',state=0,cost=0,kind='ai',facing=1,distance=55)]
if os.environ.get('POCHITA_CASES'):
 names=json.loads(os.environ['POCHITA_CASES']);cases=[c for c in cases if c['name'] in names]
capture=os.environ.get('POCHITA_CAPTURE');TICKS=int(os.environ.get('POCHITA_TICKS',1200 if EXTENSION else 240))
if capture:
 cases=[next(c for c in cases if c['name']==name and c['facing']==1) for name in json.loads(os.environ.get('POCHITA_CAPTURE_CASES','["Combo X"]'))];Path(capture).mkdir(parents=True,exist_ok=True)

def ctl(typ,trig,params):return f'\n[State -2, QA only]\ntype = {typ}\ntriggerall = RoundState = 2\ntrigger1 = {trig}\nignorehitpause = 1\n{params}\n'
clock=ctl('VarAdd','1','v = 58\nvalue = 1');p1=clock;p2=ctl('VarSet','NumEnemy > 0','v = 58\nvalue = EnemyNear,Var(58)')
for variable,effect in [(52,9401),(53,9400),(54,9402)]:p1+=ctl('VarSet','1',f'v = {variable}\nvalue = NumExplod({effect})')
for variable,effect in [(51,9450),(50,9451)]:p1+=ctl('VarSet','1',f'v = {variable}\nvalue = NumExplod({effect})')
for variable,effect in [(39,9460),(38,9461),(34,9471),(30,9472),(27,9470),(21,9480)]:p1+=ctl('VarSet','1',f'v = {variable}\nvalue = NumExplod({effect})')
p1+=ctl('VarSet','1','v = 41\nvalue = HitCount')
p1+=ctl('VarSet','1','v = 55\nvalue = Time')
if os.environ.get('POCHITA_TRACE'):
 p1+=ctl('VarSet','1','v = 46\nvalue = HitCount')+ctl('VarSet','1','v = 44\nvalue = command = "CuatroBrazos"')
for i,c in enumerate(cases):
 base=i*TICKS;at=lambda t:f'Var(58) = {base+t}';window=lambda a,b:f'Var(58) = [{base+a},{base+b}]';face=c['facing'];kind=c['kind']
 for side in [1,2]:
  x=(-1 if side==1 else 1)*face*c['distance']/2;direction=face if side==1 else -face
  block=ctl('VarSet',at(1),f'v = 59\nvalue = {i}')+ctl('LifeSet',at(1),f'value = {c.get("life",1250)}' if side==1 else f'value = {32 if VICTORY else DUMMY_LIFE}')+ctl('PowerSet',at(1),f'value = {1999 if kind=='empty' else 0 if kind in ['charge','crouch','fullcharge','charge_interrupted'] else c.get('power',3000)}')+ctl('PosSet',at(1),f'x = {x}\ny = 0')+ctl('VelSet',at(1),'x = 0\ny = 0')+ctl('Turn',at(1)+f' && Facing != {direction}','')+ctl('HitFallSet',at(1),'value = 0')+ctl('ChangeState',at(1),'value = 0\nctrl = 1')
  if side==1:p1+=block
  else:p2+=block
 for variable in [18,19,20,33,36,37,42,49]:p1+=ctl('VarSet',at(2),f'v = {variable}\nvalue = 0')
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
 if kind in ['charge','fullcharge','charge_interrupted']:p1+=ctl('AssertInput',window(22,225 if kind=='fullcharge' else 85),'flag = s')
 elif kind=='mixedcombo':
  p1+=ctl('AssertInput',at(press),'flag = '+c['button'])
  for state,button in zip(c['route'][:2],c['sequence'][1:]):p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
 elif kind in ['pursuit','specialchain','chaincap','specialblock','specialwhiff']:
  p1+=ctl('AssertInput',at(press),'flag = a')
  for state,button in ([(200,'a'),(201,'a')] if kind=='pursuit' else [(200,'b')]):p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
  if kind=='pursuit':
   p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = 202 && MoveHit','flag = U')
   p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = 650 && Time = 4','flag = a')
   for state,button in [(600,'b'),(661,'c')]:p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
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
  if kind=='comboblock':p2+=ctl('AssertInput',window(22 if POLISH else 10,150),'flag = '+('R' if face==1 else 'L'))
 elif kind in ['airmixed','airmiss','airguard','aircap','airlate']:
  p1+=ctl('AssertInput',at(22),'flag = U')
  p2+=ctl('AssertInput',at(22),'flag = U')
  p1+=ctl('AssertInput',at(30 if kind!='airlate' else 52),'flag = '+c['button'])
  for state,button in zip(c['route'][:2],c['sequence'][1:]):p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
  if kind=='airguard':p2+=ctl('AssertInput',window(29,140),'flag = '+('R' if face==1 else 'L'))
  if kind=='aircap':
   p1+=ctl('AssertInput',f'Var(59) = {i} && StateType = A && Ctrl && Var(18) >= 3','flag = a')
   p1+=ctl('VarSet',f'Var(59) = {i} && StateType = A && Ctrl && Var(18) >= 3 && command = "a"','v = 42\nvalue = 1')
 elif kind=='aircombo':
  for side in [1,2]:
   b=ctl('PosSet',window(12,115),'y = -60')+ctl('VelSet',window(12,115),'y = 0')+ctl('ChangeState',at(12),'value = 50\nctrl = '+('1' if side==1 else '0'))
   if side==1:p1+=b
   else:p2+=b
  p1+=ctl('AssertInput',at(22),'flag = a')
  for state,button in [(600,'b'),(661,'c')]:p1+=ctl('AssertInput',f'Var(59) = {i} && StateNo = {state} && MoveHit && HitPauseTime = 4','flag = '+button)
 elif kind=='polishdash':
  for a,b in [(12,14),(18,45)]:p1+=ctl('AssertInput',window(a,b),'flag = '+('R' if face==1 else 'L'))
 elif kind=='dash':
  for a,b in [(12,14),(18,32)]:p1+=ctl('AssertInput',window(a,b),'flag = '+('R' if face==1 else 'L'))
  p1+=ctl('AssertInput',at(30),'flag = a')
 elif kind not in ['walk','guard']:p1+=ctl('AssertInput',at(press),'flag = '+c['button'])
 if kind.startswith('awake_'):
  if kind=='awake_held':p1+=ctl('AssertInput',window(18,650),'flag = D')+ctl('AssertInput',window(22,650),'flag = s')
  if kind=='awake_attack':p1+=ctl('AssertInput',at(80),'flag = a')+ctl('AssertInput',at(500),'flag = a')
  if kind=='awake_special':p1+=ctl('AssertInput',window(70,76),'flag = D')+ctl('AssertInput',window(74,82),'flag = '+('R' if face==1 else 'L'))+ctl('AssertInput',at(80),'flag = a')
  if kind=='awake_ko':p1+=ctl('LifeSet',at(80),'value = 0')
  if kind=='awake_counterhit':p2+=ctl('ChangeState',at(24),'value = 9701\nctrl = 0')
  if kind in ['awake_cooldown','awake_again']:
   p1+=ctl('PowerSet',at(450),'value = 3000')+ctl('AssertInput',window(480,490),'flag = D')+ctl('AssertInput',at(485),'flag = s')
  if kind=='awake_again':p1+=ctl('AssertInput',window(980,990),'flag = D')+ctl('AssertInput',at(985),'flag = s')
 if kind=='charge_interrupted':p2+=ctl('ChangeState',at(33),'value = 9702\nctrl = 0')
 if kind=='scarf_block':p2+=ctl('AssertInput',window(10,160),'flag = '+('R' if face==1 else 'L'))
 if kind=='scarf_jump':p2+=ctl('AssertInput',at(20),'flag = U')
 if kind=='scarf_break':p2+=ctl('PosAdd',at(23),'x = 58')+ctl('ChangeState',at(24),'value = 9702\nctrl = 0')
 if kind=='scarf_escape':p1+=ctl('ChangeState',f'Var(59) = {i} && StateNo = {c["state"]+1} && Time = 8','value = 0\nctrl = 1')
 if kind=='scarf_followup':
  gate=f'Var(59) = {i} && StateNo = 0 && (EnemyNear,StateNo) = 1221 && Var(49) = 0'
  p1+=ctl('AssertInput',gate,'flag = a')+ctl('VarSet',gate,'v = 49\nvalue = 1')
 if kind=='devour_interrupted':p2+=ctl('ChangeState',at(24),'value = 9701\nctrl = 0')
 if kind=='devour_escape':p1+=ctl('ChangeState',at(85),'value = 0\nctrl = 1')
 if kind=='approachblock':p2+=ctl('AssertInput',window(10,220),'flag = '+('R' if face==1 else 'L'))
 if kind=='approachbreak':p2+=ctl('ChangeState',f'Var(59) = {i} && (EnemyNear,StateNo) = 1030 && (EnemyNear,Time) = 2','value = 9702\nctrl = 0')
 if kind=='oldblock':p2+=ctl('AssertInput',window(10,200),'flag = '+('R' if face==1 else 'L'))
 if kind=='ultiblock':p2+=ctl('AssertInput',window(10,150),'flag = '+('R' if face==1 else 'L'))
 if kind=='specialblock':p2+=ctl('AssertInput',window(10,150),'flag = '+('R' if face==1 else 'L'))
 if kind=='specialguard':p2+=ctl('AssertInput',window(10,220),'flag = '+('R' if face==1 else 'L'))+ctl('AssertInput',window(10,220),'flag = D')
 if kind=='ultijump':p2+=ctl('ChangeState',at(12),'value = 50\nctrl = 0')+ctl('PosSet',window(12,150),'y = -180')+ctl('VelSet',window(12,150),'y = 0')
# Real test strikes: do not put the tested character into a get-up state.
for state,anim,yvel,typ in [(9700,440,0,'Trip'),(9701,210,-4,'High'),(9702,400,-4,'Low')]:
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
local extra=assert(io.open('pochita_extension.tsv','w'))
local rows={};local frame=-1
hook.add('loop','pochita_qa',function()
 if not player(1) or roundState()~=2 then return end
 local t=var(58);if t==frame or t<1 then return end;frame=t
 local case=math.floor((t-1)/TICKCOUNT);local tick=(t-1)%TICKCOUNT+1
 if case>=COUNT then player(2);setLife(100);player(1);setTime(0);return end
 if not rows[case] then rows[case]={states={},damage=0,received=0,minpower=3000,maxpower=0,apex=0,vapex=0,last=0,final=0,dx=0,blood=0,slashes=0,ground=0,endfx=0,cancelattempt=0,flare=0,ring=0,trails=0,finishes=0,maxhits=0,attacktime=0} end
 local r=rows[case]
 if not r.extension then r.extension={timer=0,healed=0,hpmax=0,hpmin=1250,aura=0,erase=0,bite=0,awakenings=0,previous=-1,victimstates={},endtimer=0,endcooldown=0,hplast=0,victimpower=0} end
 local e=r.extension
 if tick>4 then
  e.timer=math.max(e.timer,var(36));e.healed=math.max(e.healed,var(33));e.hpmax=math.max(e.hpmax,life());e.hpmin=math.min(e.hpmin,life());e.hplast=life();e.endtimer=var(36);e.endcooldown=var(37)
  e.aura=math.max(e.aura,var(27));e.erase=math.max(e.erase,var(34));e.bite=math.max(e.bite,var(30))
  if stateNo()==520 and e.previous~=520 then e.awakenings=e.awakenings+1 end;e.previous=stateNo()
  player(2);e.victimstates[stateNo()]=true;e.victimpower=power();player(1)
 end
 r.blood=math.max(r.blood,var(52));r.slashes=math.max(r.slashes,var(53));r.ground=math.max(r.ground,var(54));r.endfx=var(52)+var(53)+var(54)
 r.flare=math.max(r.flare,var(51));r.ring=math.max(r.ring,var(50));r.endfx=r.endfx+var(51)+var(50)
 r.trails=math.max(r.trails,var(39));r.finishes=math.max(r.finishes,var(38));r.endfx=r.endfx+var(39)+var(38)+var(34)+var(30)+var(27)+var(21)
 if tick>4 then
  r.maxhits=math.max(r.maxhits,var(41))
  local st=stateNo();if st==1000 or st==1010 or st==1030 or st==1040 or st==1060 or st==1070 then r.attacktime=math.max(r.attacktime,var(55)) end
 end
 if tick>4 then r.cancelattempt=math.max(r.cancelattempt,var(42)) end
 if tick>4 then
  r.states[stateNo()]=true;r.last=stateNo();r.received=math.max(r.received,(INITIALS)[case+1]-life());r.minpower=math.min(r.minpower,power());r.maxpower=math.max(r.maxpower,power());r.apex=math.min(r.apex,posY())
  if stateNo()==100 or stateNo()==20 or stateNo()==50 then r.dx=math.max(r.dx,math.abs(posX()-(STARTS)[case+1])) end
  player(2);r.damage=math.max(r.damage,DUMMYMAX-life());r.final=stateNo();r.vapex=math.min(r.vapex,posY());player(1)
 end
 CAPTURE
 if tick==TICKLAST and not r.saved then
  local vst={};for k,_ in pairs(e.victimstates) do table.insert(vst,k) end;table.sort(vst)
  extra:write(case..'\\t'..e.timer..'\\t'..e.healed..'\\t'..e.hpmax..'\\t'..e.hpmin..'\\t'..e.hplast..'\\t'..e.endtimer..'\\t'..e.endcooldown..'\\t'..e.aura..'\\t'..e.erase..'\\t'..e.bite..'\\t'..e.awakenings..'\\t'..e.victimpower..'\\t'..table.concat(vst,',')..'\\n');extra:flush()
  r.saved=true;local states={};for k,_ in pairs(r.states) do table.insert(states,k) end;table.sort(states)
  f:write(case..'\\t'..table.concat(states,',')..'\\t'..r.damage..'\\t'..r.received..'\\t'..r.minpower..'\\t'..r.maxpower..'\\t'..r.apex..'\\t'..r.last..'\\t'..r.final..'\\t'..r.dx..'\\t'..r.vapex..'\\t'..r.blood..'\\t'..r.slashes..'\\t'..r.ground..'\\t'..r.endfx..'\\t'..r.cancelattempt..'\\t'..r.flare..'\\t'..r.ring..'\\t'..r.trails..'\\t'..r.finishes..'\\t'..r.maxhits..'\\t'..r.attacktime..'\\n');f:flush()
 end
end)
'''.replace('TICKCOUNT',str(TICKS)).replace('TICKLAST',str(TICKS-1)).replace('DUMMYMAX',str(DUMMY_LIFE)).replace('COUNT',str(len(cases))).replace('INITIALS','{'+','.join(str(c.get('life',1250)) for c in cases)+'}').replace('STARTS','{'+','.join(str(-c['facing']*c['distance']/2) for c in cases)+'}')
if POLISH:
 module+="""
local polish=assert(io.open('pochita_polish.tsv','w'))
hook.add('loop','pochita_polish',function()
 if not player(1) or roundState()~=2 then return end
 local t=var(58);if t<1 then return end
 local vals={t,stateNo(),spriteVar('group'),spriteVar('image'),numExplod(9490),numExplod(9491),numExplod(9492),numExplod(9493),numExplod(9494),posY(),life()}
 for i,v in ipairs(vals) do polish:write(tostring(v)..(i==#vals and string.char(10) or string.char(9))) end;polish:flush()
end)
"""
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
  local sounds={[500]=0,[200]=0,[201]=0,[202]=1,[210]=0,[211]=1,[212]=7,[220]=0,[221]=1,[222]=8,[600]=0,[610]=0,[620]=0,[660]=0,[661]=0,[662]=0,[670]=8,[671]=7,[672]=8,[1200]=10,[1210]=10,[3000]=10,[1500]=3,[520]=13,[1000]=1,[1010]=1,[1020]=1,[1030]=1,[1040]=1,[1050]=1,[1060]=1,[1070]=3,[1080]=1,[1100]=3}
  if st==11000 or st==11010 or st==11030 or st==11040 or st==11060 or st==11070 then sounds[st]=10 end
  if sounds[st]~=nil then cue(t,sounds[st]) end
  if cap.state==500 and st~=500 then cue(t,15) end
  cap.state=st;cap.lastut=-1;cap.finish=0
 end
 if (st==202 or st==212 or st==222 or st==670 or st==671 or st==672) and var(15)>0 and cap.finish==0 then cue(t,16);cap.finish=1 end
 if st==100 and stime>0 and stime%12==0 and stime~=cap.lastut then cue(t,17);cap.lastut=stime end
 if st==52 and stime==1 and stime~=cap.lastut then cue(t,17);cap.lastut=stime end
 if st==1501 and stime~=cap.lastut then
  if stime==8 or stime==40 or stime==72 then cue(t,7) end
  if stime==30 or stime==42 or stime==54 or stime==66 then cue(t,8) end
  if stime==92 then cue(t,9) end
  cap.lastut=stime
 end
 player(2);local hp=life();player(1)
 if st==3001 and stime~=cap.lastut then
  if stime==34 or stime==58 then cue(t,11) end
  if stime==66 or stime==92 or stime==116 then cue(t,12) end
  cap.lastut=stime
 end
 if hp<cap.hp and st~=3001 and st~=1501 then cue(t,st==212 and 7 or st==222 and 9 or 5) end
 cap.hp=hp
 if cap.pending~=nil then
  local png=io.open(capdir..string.format('Ikemen_GO%03d.png',cap.index),'rb')
  if png~=nil then png:close();framefile:write(cap.index..string.char(9)..cap.pending..string.char(10));framefile:flush();cap.index=cap.index+1;cap.pending=nil end
 end
 if tick>=12 and tick<=CAPTURELAST and tick-cap.last>=4 and cap.pending==nil then
  screenshot();cap.pending=tick;cap.last=tick
 end
 """
 module=module.replace('CAPTURE',capturecode.replace('CAPTURELAST',str(min(TICKS-12,560))))
else:module=module.replace('CAPTURE','')
if KO_CHECK:
 module+="\nlocal kofile=assert(io.open('pochita_ko.tsv','w'))\nlocal died=false\nhook.add('loop','pochita_ko',function()\n if not player(1) then return end\n if life()<=0 then died=true end\n if died then kofile:write(life()..string.char(9)..var(36)..string.char(9)..roundState()..string.char(10));kofile:flush() end\nend)\n"
if VICTORY:
 module="""
local winlog=assert(io.open('pochita_win.tsv','w'))
local frame=0;local previous=-1;local lasttime=-1
local cap={index=0,last=-1000,pending=nil}
WINCAPSETUP
hook.add('loop','pochita_real_win',function()
 if not player(1) or roundState()<2 then return end
 frame=frame+1;local st=stateNo();local tm=time()-1
 local vals={frame,roundState(),st,tm,anim(),spriteVar('group'),spriteVar('image'),numExplod(9495),life()}
 player(2);table.insert(vals,life());player(1);table.insert(vals,math.floor(screenPosX()))
 for i,v in ipairs(vals) do winlog:write(tostring(v)..(i==#vals and string.char(10) or string.char(9))) end;winlog:flush()
 WINCAPTURE
 previous=st;lasttime=tm
end)
"""
 if capture:
  capdir=str(Path(capture).resolve())+'/'
  setup="modifyGameOption('Config.ScreenshotFolder',"+json.dumps(capdir)+")\nlocal framefile=assert(io.open("+json.dumps(capdir+'frames.tsv')+",'w'))\nlocal audiofile=assert(io.open("+json.dumps(capdir+'audio.tsv')+",'w'))\n"
  code="""
 if st~=previous and (st==200 or st==180) then audiofile:write(frame..string.char(9)..tostring(0)..string.char(10));audiofile:flush() end
 if st==180 and tm~=lasttime and (tm==14 or tm==38) then audiofile:write(frame..string.char(9)..(tm==14 and 8 or 15)..string.char(10));audiofile:flush() end
 if cap.pending~=nil then
  local png=io.open(CAPDIR..string.format('Ikemen_GO%03d.png',cap.index),'rb')
  if png then png:close();framefile:write(cap.index..string.char(9)..cap.pending..string.char(10));framefile:flush();cap.index=cap.index+1;cap.pending=nil end
 end
 if frame>=12 and frame<420 and frame-cap.last>=4 and cap.pending==nil then screenshot();cap.pending=frame;cap.last=frame end
""".replace('CAPDIR',json.dumps(capdir))
  module=module.replace('WINCAPSETUP',setup).replace('WINCAPTURE',code)
 else:module=module.replace('WINCAPSETUP','').replace('WINCAPTURE','')
 (ENGINE/'pochita_win.tsv').write_text('')
module="modifyGameOption('Debug.RetryLoadOnError',false)\n"+module
(ENGINE/'external/mods/pochita_checks.lua').write_text(module);(ENGINE/'pochita_checks.tsv').write_text('');(ENGINE/'pochita_extension.tsv').write_text('');(ENGINE/'pochita_ko.tsv').write_text('')
debug=ENGINE/'external/script/debug.lua';original=debug.read_text();debug.write_text(original+"\ndofile('external/mods/pochita_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
record_audio=os.environ.get('POCHITA_RECORD_AUDIO')
if record_audio:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=str(Path(record_audio).resolve()),SDL_DISKAUDIODELAY='46')
try:
 r=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','PochitaCheck','-p2','PochitaDummy','-p1.ai',os.environ.get('POCHITA_AI','0'),'-p2.ai','0','-rounds','1','-time',str(max(600,len(cases)*TICKS//60+30))]+([] if record_audio else ['-nosound'])+(['-speed','0'] if capture or record_audio else ['-speedtest']),cwd=ENGINE,env=env,capture_output=True,text=True,timeout=90)
 print(r.stdout);print(r.stderr);assert r.returncode==0,r.returncode
finally:
 debug.write_text(original);(ENGINE/'external/mods/pochita_checks.lua').rename(ENGINE/'external/mods/-pochita_checks.lua')
if VICTORY:
 rows=[list(map(int,line.split())) for line in (ENGINE/'pochita_win.tsv').read_text().splitlines()]
 poses={row[6] for row in rows if row[2]==180 and row[5]==3500};assert {4,5,6,7}<=poses,poses
 assert any(row[9]==0 for row in rows) and all(row[8]==1250 for row in rows),rows[-3:]
 assert any(row[2]==180 and row[3]>=110 for row in rows),'victory sequence ended before motor slowdown'
 assert max(row[7] for row in rows)>0 and rows[-1][7]==0,'victory blood failed to show or expire'
 result=dict(winner_min_screen_x=min(row[10] for row in rows if row[2]==180 and row[3]>2),passed=True,facing=cases[0]['facing'],real_KO=True,victory_poses=sorted(poses),last_victory_time=max(row[3] for row in rows if row[2]==180),final_victim_life=rows[-1][9],capture=bool(capture))
 path=ROOT/'previews'/('Pochita_polish_win_visual_checks.json' if capture else 'Pochita_polish_win_checks.json');prior=json.loads(path.read_text()) if path.exists() else [];prior=[x for x in prior if x['facing']!=result['facing']];prior.append(result);path.write_text(json.dumps(prior,indent=2)+'\n')
 print('PASS actual normal-hit KO and complete motor-down victory',result);raise SystemExit(0)
if KO_CHECK:
 rows=[list(map(int,line.split())) for line in (ENGINE/'pochita_ko.tsv').read_text().splitlines()]
 assert len(rows)>=30 and all(row[0]==0 for row in rows) and all(row[1]==0 for row in rows[2:]),rows
 (ROOT/'previews/Pochita_no_revive_checks.json').write_text(json.dumps(dict(passed=True,frames_after_KO=len(rows),life_after_KO=sorted({r[0] for r in rows}),awakening_timer_after_two_frames=sorted({r[1] for r in rows[2:]})),indent=2)+'\n')
 print('PASS awakening stops on KO and never revives the character');raise SystemExit(0)
raw={}
for line in (ENGINE/'pochita_checks.tsv').read_text().splitlines():raw.setdefault(int(line.split('\t')[0]),line)
assert sorted(raw)==list(range(len(cases))),sorted(raw)
extension={}
for line in (ENGINE/'pochita_extension.tsv').read_text().splitlines():
 values=line.split('\t');extension[int(values[0])]=dict(zip(['peak_timer','healed','maximum_life','minimum_life','final_life','final_timer','final_cooldown','aura','erasure','bite','awakenings','victim_power'],map(int,values[1:13])));extension[int(values[0])]['victim_states']=list(map(int,values[13].split(',')))
assert sorted(extension)==list(range(len(cases))),sorted(extension)
polishrows=[]
if POLISH:polishrows=[list(map(float,line.split())) for line in (ENGINE/'pochita_polish.tsv').read_text().splitlines()]
report=[];errors=[]
for i,c in enumerate(cases):
 _,states,damage,received,minimum,maximum,apex,last,final,dx,vapex,blood,slashes,ground,endfx,attempt,flare,ring,trails,finishes,maxhits,attacktime=raw[i].split('\t');states=set(map(int,states.split(',')));damage=int(damage);minimum=int(minimum);kind=c['kind'];fail=[]
 if kind in ['empty','oldempty','awake_empty','scarf_empty']:
  if c['state'] in states:fail.append('technique spent unavailable power')
 else:
  if c['state'] not in states:fail.append('expected state not reached')
  if c['cost'] and kind not in ['awake_attack','awake_again'] and minimum!=c.get('power',3000)-c['cost']:fail.append('power cost differs from advertised reduced cost')
 if kind=='ai' and (damage<=0 or not {200,201,202,210,211,212,220,221,222,600,610,620,1000,1010,1020,1030,1040,1050,1060,1070,1080,1100,1500,3000}.intersection(states)):fail.append('CPU did not use its real offensive states')
 if {11000,11010,11030,11040,11060,11070}.intersection(states) and (int(flare)==0 or int(ring)==0):fail.append('activated special missing startup flash or ground ring')
 if kind=='startupwhiff' and damage!=0:fail.append('startup presentation dealt damage without an attack collision')
 if kind=='emptyspecial' and (c['forbidden'] in states or int(flare)>0 or minimum!=c['power']):fail.append('special presentation activated without enough energy')
 if kind=='special' and str(c['state']) in CHOREOGRAPHY:
  choreography=CHOREOGRAPHY[str(c['state'])]
  if damage!=choreography['damage'] or int(maxhits)!=choreography['contacts']:fail.append('extended special failed to connect all its physical contacts')
  if int(attacktime)<choreography['animation_ticks']-3:fail.append('extended special animation ended before the intended recovery')
  if int(trails)==0 or int(finishes)!=1:fail.append('extended special missing its unique trails or confirmed finish')
 if kind in ['startupwhiff','specialguard'] and (int(trails)==0 or int(finishes)>0):fail.append('missed/guarded special lost its trails or emitted a confirmed finish')
 if kind=='specialguard' and (int(blood)>0 or int(maxhits)>0 or damage>40):fail.append('guarded extended sequence became unblockable or emitted blood')
 if kind in ['combo','special','shortcut','crouch','aircombo','counter'] and damage<=0:fail.append('no collision damage')
 if kind in ['comboblock','combowhiff'] and (c['finish'] in states or damage>40):fail.append('third combo hit occurred without confirming earlier hits')
 if kind=='combowhiff' and damage!=0:fail.append('missed normal caused damage')
 if kind=='aircombo' and (not {600,661,672}.issubset(states) or damage<205):fail.append('air links failed')
 if kind in ['airmixed','aircap'] and (not set(c['route']).issubset(states) or damage!=c['expected']):fail.append('free-physics airborne chain lost a real contact or exceeded its damage budget')
 if kind in ['airmixed','airmiss','airguard','aircap','airlate'] and (int(last)!=0 or int(final) in [1220,1221,1222]):fail.append('air route failed to land or release control')
 if kind=='airmiss' and (damage!=0 or {661,672}.intersection(states)):fail.append('whiffed aerial attack chained or damaged at distance')
 if kind=='airguard' and (damage>10 or {661,672}.intersection(states) or int(blood)>0):fail.append('aerial guard failed to stop the chain')
 if kind=='aircap' and int(attempt)!=1:fail.append('fourth airborne button was never attempted')
 if kind.startswith('scarf_'):
  if int(last)!=0 or int(final) in [1220,1221,1222]:fail.append('scarf attack left attacker or victim trapped')
  if kind in ['scarf_hit','scarf_exact'] and (c['state']+1 not in states or damage!=(40 if c['state']==1200 else 190) or 1220 not in extension[i]['victim_states']):fail.append('physical scarf failed to connect, hold and release its victim')
  if kind in ['scarf_block','scarf_miss','scarf_jump','scarf_empty','scarf_break'] and (damage!=0 or c['state']+1 in states or 1220 in extension[i]['victim_states']):fail.append('scarf grabbed or damaged a blocked, distant, airborne or interrupted target')
  if kind=='scarf_empty' and minimum!=c['power']:fail.append('scarf spent unavailable power')
  if kind=='scarf_break' and int(received)<=0:fail.append('scarf opening could not be interrupted')
  if kind=='scarf_followup' and (damage!=72 or 200 not in states):fail.append('brief scarf stun did not allow a normal follow-up')
 if kind=='combo' and damage<{'a':152,'b':180,'c':205}[c['button']]:fail.append('not every normal actually hit')
 if kind=='mixedcombo' and (not set(c['route']).issubset(states) or damage!=c['expected']):fail.append('mixed route failed to connect every physical hit')
 if kind=='pursuit' and (not {200,201,202,650,600,661,672}.issubset(states) or damage<357 or int(last)!=0):fail.append('physical launcher/pursuit/air finisher failed')
 if kind in ['specialchain','chaincap'] and (not {200,211,1000,1010}.issubset(states) or damage<200):fail.append('mixed normal into two paid specials failed')
 if kind=='chaincap' and 1030 in states:fail.append('third special bypassed the two-special sequence limit')
 if kind=='chaincap' and int(attempt)!=1:fail.append('third-special input was not recognized during the cap test')
 if kind in ['specialblock','specialwhiff'] and ({1000,1010}.intersection(states) or minimum!=3000 or int(blood)>0):fail.append('special cancel occurred without a real hit')
 if kind=='specialwhiff' and damage!=0:fail.append('missed cancel route caused damage')
 if kind=='combo' and c['button']=='a' and not 20<=-float(vapex)<=80:fail.append('launcher height outside the intended camera range')
 if kind=='charge' and (int(maximum)<1000 or int(last)==500):fail.append('charge failed or did not release')
 if kind=='fullcharge' and (int(maximum)!=3000 or int(last)==500):fail.append('full charge failed to cap/release')
 if kind=='recovery' and (int(received)<=0 or not {5110,5120,200}.issubset(states)):fail.append('actual knockdown/get-up/new attack failed')
 if kind in ['combo','aircombo'] and (int(blood)==0 or int(slashes)==0):fail.append('confirmed finisher has no slash/blood effects')
 if kind not in ['ai','awake_again'] and int(endfx)!=0:fail.append('visual effects failed to expire')
 if kind=='ai' and int(endfx)>9:fail.append('ongoing CPU combat accumulated too many effects')
 if kind in ['ultiblock','ultijump','ultifar','combowhiff','comboblock'] and int(blood)>0:fail.append('blood emitted without a real hit')
 if kind=='ultihit' and (damage!=min(450,int(DUMMY_LIFE*.45)) or 3001 not in states or int(final) in [3010,3011,3012] or extension[i]['erasure']==0 or extension[i]['bite']==0 or 3012 not in extension[i]['victim_states'] or extension[i]['victim_power']!=max(0,c.get('power',3000)-500)):fail.append('confirmed ultimate damage/release failed')
 if kind in ['ultiblock','ultijump','ultifar'] and (damage>0 or 3001 in states):fail.append('ultimate could not be avoided')
 if kind=='reachwhiff' and (damage!=0 or int(last)!=0):fail.append('short blade hit outside visible reach or failed to recover')
 if kind=='jump' and not 45<=-float(apex)<=75:fail.append('neutral jump height outside intended range')
 if kind=='jump' and (int(last)!=0 or (c['direction']!='N' and float(dx)<15)):fail.append('jump landing or diagonal travel failed')
 if kind=='walk' and (float(dx)<20 or int(last)!=0):fail.append('walk/release failed')
 if kind=='guard' and (int(received)!=0 or 150 not in states):fail.append('incoming strike not blocked')
 if kind=='dash' and (100 not in states or float(dx)<10):fail.append('dash failed to move/cancel')
 e=extension[i]
 if kind=='special' and c['state']==1500 and (damage!=min(250,DUMMY_LIFE//4) or 1501 not in states or int(final) in [1510,1511]):fail.append('relocated former ultimate damage or release failed')
 if kind.startswith('awake_'):
  expected=0 if kind=='awake_empty' else 10 if kind=='awake_cap' else 0 if kind=='awake_full' else 240
  if kind!='awake_again' and e['healed']!=expected:fail.append('regeneration healing cap differs from intended budget')
  if e['maximum_life']>1250:fail.append('regeneration exceeded maximum life')
  if kind not in ['awake_empty','awake_again'] and (e['peak_timer'] not in [359,360] or e['final_timer']!=0 or e['awakenings']!=1 or e['aura']==0):fail.append('awakening did not start once, expire, or display its aura')
  if kind in ['awake_wounded','awake_held','awake_cooldown'] and e['final_life']!=1040:fail.append('regeneration did not restore exactly 240 health')
  if kind=='awake_empty' and (e['healed']!=0 or e['awakenings']!=0 or minimum!=2999):fail.append('awakening activated below a full bar')
  if kind=='awake_attack' and (200 not in states or damage!=70):fail.append('awakening prevented normal combat')
  if kind=='awake_counterhit' and int(received)<=0:fail.append('awakening accidentally granted invulnerability')
  if kind=='awake_again' and (e['awakenings']!=2 or e['final_timer']<=0 or int(endfx)!=1):fail.append('awakening failed to re-enable after the cooldown')
 if kind=='rangeapproach' and (not 0<damage<=126 or int(maxhits)<1 or int(last)!=0):fail.append('physical approach failed to connect at distance 200')
 if kind=='approachmiss' and damage!=0:fail.append('normal-size saws hit past the approach distance')
 if kind=='approachblock' and (damage>40 or int(blood)>0 or int(finishes)>0):fail.append('approaching thrust bypassed guard')
 if kind=='approachbreak' and (int(received)<=0 or damage!=0):fail.append('approaching thrust did not remain interruptible')
 if kind=='rangerush' and damage<=0:fail.append('forward physical move failed at its advertised test distance')
 if kind=='awake_special' and (1000 not in states or not 125<=damage<=128):fail.append('awakening failed to boost physical special contacts')
 if kind=='devour_interrupted' and (3001 in states or damage!=0 or int(received)<=0):fail.append('unconfirmed devour opening could not be interrupted')
 if kind=='devour_escape' and int(final) in [3010,3011,3012]:fail.append('opponent trapped after the attacker left the cinematic')
 if kind=='oldhit' and (1501 not in states or damage!=min(250,DUMMY_LIFE//4)):fail.append('down-A five-cut special failed')
 if kind in ['oldblock','oldfar','oldempty'] and (1501 in states or 3000 in states or damage>0):fail.append('down-A missed or blocked move triggered automatic damage or ultimate')
 presentation={}
 if POLISH:
  pr=[r for r in polishrows if i*TICKS+5<r[0]<(i+1)*TICKS]
  presentation=dict(dust=max(r[4] for r in pr),charge_embers=max(r[5] for r in pr),metal=max(r[6] for r in pr),paths=max(r[7] for r in pr),finish=max(r[8] for r in pr),final_effects=sum(pr[-1][4:9]),charge_poses=sorted({int(r[3]) for r in pr if r[1]==500 and r[2]==3500}),run_poses=sorted({int(r[3]) for r in pr if r[1]==100 and r[2]==3501}),land_poses=sorted({int(r[3]) for r in pr if r[1]==52 and r[2]==3501}))
  if presentation['dust']>2 or presentation['paths']>2 or presentation['final_effects']!=0:fail.append('presentation effects accumulated or failed to expire')
  if kind in ['charge','fullcharge'] and (presentation['charge_poses']!=[0,1,2,3] or presentation['charge_embers']<=0 or presentation['dust']<=0):fail.append('new motor poses, sparks or boot dust absent during charge')
  if kind=='charge_interrupted' and (int(received)<=0 or int(last)==500):fail.append('rev charge became invulnerable or trapped control')
  if kind=='polishdash' and (presentation['run_poses']!=[0,1,2,3] or presentation['dust']<=0 or int(last)!=0):fail.append('scarf run, braking or dust failed')
  if kind=='jump' and (presentation['land_poses']!=[6,7] or presentation['dust']<=0):fail.append('landing pose/dust absent after real jump')
  if kind=='combo' and (presentation['metal']<=0 or presentation['paths']<=0 or presentation['finish']<=0):fail.append('connected finisher lacks its new readable metal/path/finish effects')
  if kind in ['comboblock','combowhiff'] and presentation['finish']>0:fail.append('missed or guarded attacks emitted a confirmed finish')
  if kind=='comboblock' and presentation['metal']<=0:fail.append('guard contact has no metal sparks')
 row=dict(presentation=presentation,extension=e,case=c,states=sorted(states),damage=damage,received=int(received),minimum_power=minimum,maximum_power=int(maximum),apex=float(apex),victim_apex=float(vapex),blood_effects=int(blood),slash_effects=int(slashes),ground_effects=int(ground),effects_at_end=int(endfx),third_special_input_recognized=int(attempt),activation_flash=int(flare),ground_ring=int(ring),distinct_trails=int(trails),confirmed_finish=int(finishes),max_hitcount=int(maxhits),attack_time=int(attacktime),last=int(last),victim_final=int(final),dash_travel=float(dx),failures=fail);report.append(row);errors+=fail;print('FAIL' if fail else 'PASS',c['name'],c['facing'],row)
path=ROOT/'previews'/(('Pochita_polish_visual_checks.json' if os.environ.get('POCHITA_PREVIEW_SET')=='polish' else 'Pochita_air_scarf_visual_checks.json' if os.environ.get('POCHITA_PREVIEW_SET')=='air_scarf' else 'Pochita_devour_visual_checks.json' if os.environ.get('POCHITA_PREVIEW_SET')=='devour' else 'Pochita_long_visual_checks.json' if os.environ.get('POCHITA_PREVIEW_SET')=='long' else 'Pochita_special_visual_checks.json' if os.environ.get('POCHITA_PREVIEW_SET')=='special' else 'Pochita_flow_visual_checks.json' if os.environ.get('POCHITA_PREVIEW_SET')=='flow' else 'Pochita_engine_visual_checks.json') if capture else 'Pochita_low_life_ultimate_checks.json' if DUMMY_LIFE!=1000 else 'Pochita_AI_checks.json' if os.environ.get('POCHITA_AI') else 'Pochita_devour_checks.json' if EXTENSION else 'Pochita_polish_checks.json' if POLISH else 'Pochita_air_scarf_checks.json' if AIR_SCARF else 'Pochita_engine_checks.json');path.write_text(json.dumps(report,indent=2)+'\n');assert not errors,errors
print('PASSED',len(report),'raw-input/collision scenarios')
