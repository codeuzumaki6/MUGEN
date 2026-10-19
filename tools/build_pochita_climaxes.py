#!/usr/bin/env python3
"""Add physical triple-chain finishers and a hit-confirmed four-saw ultimate."""
from pathlib import Path
import re,json

def apply_climax_runtime(char):
 air=(char/'PochitaTrueForm.air').read_text();cns=(char/'PochitaTrueForm.cns').read_text();cmd=(char/'PochitaTrueForm.cmd').read_text()
 metadata=json.loads((char/'assets/sprites.json').read_text());geo={(r['group'],r['number']):r for rows in metadata.values() for r in rows}
 def anim(n,group,indices,times,active=()):
  s=f'[Begin Action {n}]\nClsn2Default: 1\n Clsn2[0] = -17,-72,17,0\n'
  for e,(i,t) in enumerate(zip(indices,times),1):
   if e in active:s+=f'Clsn1: 1\n Clsn1[0] = 12,-66,{min(100,max(24,geo[group,i]["attack_extent"]+1))},-12\n'
   s+=f'{group},{i},0,0,{t}\n'
  return s+'\n'
 air+=anim(212,220,[2,3,4,5,4,5,8,9,10,11,12,13],[3]*12,(3,4,5,6,7,8,9,10))
 air+=anim(222,250,[0,1,2,3,4,5,6,7],[3]*8,(3,4,5,6))
 sequence=anim(3001,3100,[0,1,2,3,4,5,2,6,6,7],[8,10,12,12,12,12,10,8,10,24])
 air=re.sub(r'(?is)\[Begin Action 3001\].*?(?=\[Begin Action)',sequence,air,count=1)
 for n,group,times in [(9200,9200,[2,3,3,3]),(9201,9201,[2,3,4,5]),(9202,9202,[2,3,4,6])]:air+=f'[Begin Action {n}]\n'+''.join(f'{group},{i},0,0,{t}\n' for i,t in enumerate(times))+'\n'
 def add_to_state(n,text):
  nonlocal cns
  m=re.search(rf'(?is)\[Statedef {n}\].*?(?=\[Statedef|\Z)',cns);assert m,n;block=m[0];marker=f'[State {n}, End]';pos=block.find(marker)
  if pos<0:pos=len(block)
  cns=cns[:m.start()]+block[:pos]+text+'\n'+block[pos:]+cns[m.end():]
 def effect(n,label,condition,animno,identifier,pos='42,-36',scale='.7,.7',angle=0,extra=''):
  return f'''[State {n}, {label}]
type = Explod
{condition}
anim = {animno}
ID = {identifier}
postype = p1
pos = {pos}
facing = 1
bindtime = 0
removetime = 16
sprpriority = 5
scale = {scale}
ownpal = 1
removeongethit = 1
ignorehitpause = 1
supermovetime = 8
{extra}
'''
 def hitfx(n,dust=False,big=False):
  cond='triggerall = Time >= 3\ntriggerall = MoveHit\ntrigger1 = HitCount > Var(26)'
  s=f'[State {n}, Reset impact gate]\ntype = VarSet\ntrigger1 = Time = 0\nv = 26\nvalue = 0\nignorehitpause = 1\n'
  s+=effect(n,'Contact slash',cond,9200,9400,scale='.95,.95' if big else '.65,.65',angle=-35 if n==202 else 0)
  s+=effect(n,'Contact blood',cond,9201,9401,scale='.85,.85' if big else '.65,.65')
  if dust:s+=effect(n,'Ground burst',cond,9202,9402,pos='40,-Pos Y',scale='.85,.85')
  s+=f'[State {n}, Latch impact]\ntype = VarSet\n{cond}\nv = 26\nvalue = HitCount\nignorehitpause = 1\n'
  return s
 def strike(n,element,damage,last=False,slam=False):
  return f'''[State {n}, Blade contact {element}]
type = HitDef
trigger1 = AnimElem = {element}
attr = {'A' if slam else 'S'}, NA
damage = {damage},2
animtype = {'Heavy' if last else 'Medium'}
guardflag = MA
hitflag = MAF
priority = 5,Hit
pausetime = {9 if last else 4},{12 if last else 7}
sparkno = 1
hitsound = S1,{9 if slam else 7}
guardsound = S1,6
ground.type = High
ground.hittime = 28
ground.slidetime = 16
ground.velocity = {-5.8 if last and not slam else -2 if slam else -.4},{4 if slam else -2 if last else 0}
air.hittime = 28
air.velocity = {-5.8 if last and not slam else -2 if slam else -.4},{6 if slam else -2 if last else -.5}
fall = {int(last)}
fall.yvelocity = 0
fall.recover = 1
fall.recovertime = 30
getpower = 40,8
givepower = 15,5
envshake.time = {8 if last else 3}
envshake.ampl = {-4 if last else -1}
'''
 cns+='''[Statedef 212]
type = S
movetype = A
physics = S
anim = 212
ctrl = 0
velset = 1.1,0
[State 212, Motor grind]
type = PlaySnd
trigger1 = Time = 0
value = S1,7
channel = 1
'''
 for e,d,last in [(3,18,False),(6,18,False),(9,54,True)]:cns+=strike(212,e,d,last)
 cns+=hitfx(212,big=True)+'''[State 212, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 222]
type = A
movetype = A
physics = A
anim = 222
ctrl = 0
velset = .8,-3.8
[State 222, Cleave motor]
type = PlaySnd
trigger1 = Time = 0
value = S1,8
channel = 1
'''+strike(222,3,105,True,True)+hitfx(222,dust=True,big=True)+'''[State 222, Land]
type = ChangeState
trigger1 = Pos Y >= 0
trigger1 = Vel Y > 0
value = 52
ctrl = 0
[State 222, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 50
ctrl = 1
'''
 for state,button,nextstate in [(211,'b',212),(221,'c',222)]:
  add_to_state(state,f'''[State {state}, Reset press]
type = VarSet
trigger1 = Time = 0
v = 25
value = 0
ignorehitpause = 1
[State {state}, Buffer third press]
type = VarSet
trigger1 = Time > 0
trigger1 = command = "{button}"
trigger2 = AILevel > 0
trigger2 = MoveHit
v = 25
value = 1
ignorehitpause = 1
''')
  header=f'''[State -1, Hit confirmed {state} to {nextstate}]
type = ChangeState
value = {nextstate}
triggerall = StateNo = {state}
triggerall = MoveHit
triggerall = Time > 0
trigger1 = Var(25) = 1
ignorehitpause = 1

''';cmd=cmd.replace('[State -1, Normal a]',header+'[State -1, Normal a]')
 for state in [200,201,202,210,211,220,221,600,610,620,1000,1010,1020,1030,1040,1050,1060,1070,1080,1100,1401]:
  add_to_state(state,hitfx(state,dust=state in [1040,1050,1080],big=state in [202,620,1070,1100]))
 for state in [202,212,222,620]:
  add_to_state(state,f'''[State {state}, Blade afterimages]
type = AfterImage
trigger1 = Time = 3
time = 14
length = 6
timegap = 1
framegap = 2
palcolor = 256
palbright = 10,-20,-20
palcontrast = 210,210,210
palmul = .8,.8,.8
trans = add
''')
 # The cinematic exists ONLY in the successful opening's state.
 begin=cns.index('[Statedef 3001]');end=cns.index('[Statedef 3011]',begin)
 ultimate='''[Statedef 3001]
type = S
movetype = A
physics = N
anim = 3001
ctrl = 0
velset = 0,0
[State 3001, Damage ceiling]
type = VarSet
trigger1 = Time = 0
trigger1 = NumTarget(3000) > 0
v = 28
value = IfElse((Target(3000),LifeMax) > 1000,500,Floor((Target(3000),LifeMax)*.5))
[State 3001, Damage applied]
type = VarSet
trigger1 = Time = 0
v = 29
value = 0
[State 3001, Confirm freeze]
type = SuperPause
trigger1 = Time = 0
time = 8
movetime = 8
anim = -1
darken = 1
[State 3001, Confirm protection]
type = NotHitBy
trigger1 = 1
value = SCA
time = 1
[State 3001, Scene shade]
type = BGPalFX
trigger1 = Time = 0
time = 116
mul = 100,70,75
[State 3001, Victim position]
type = TargetBind
trigger1 = Time < 100
trigger1 = NumTarget(3000) > 0
ID = 3000
pos = 64,0
[State 3001, Motors]
type = PlaySnd
trigger1 = Time = 8
trigger2 = Time = 40
trigger3 = Time = 72
value = S1,7
channel = 1
'''
 for t,damage in [(30,60),(42,60),(54,70),(66,70),(92,240)]:
  condition=f'trigger1 = Time = {t}\ntrigger1 = NumTarget(3000) > 0'
  amount='Var(28)-Var(29)' if t==92 else f'Floor(Var(28)*{damage}/500.0)'
  ultimate+=f'''[State 3001, Actual cut {t}]
type = TargetLifeAdd
{condition}
ID = 3000
value = -({amount})
kill = {int(t==92)}
absolute = 1
[State 3001, Record damage {t}]
type = VarAdd
{condition}
v = 29
value = {amount}
[State 3001, Cut sound {t}]
type = PlaySnd
{condition}
value = S1,{9 if t==92 else 8}
channel = 2
persistent = 0
[State 3001, Impact shake {t}]
type = EnvShake
{condition}
time = {10 if t==92 else 4}
freq = 95
ampl = {-4 if t==92 else -2}
'''
  ultimate+=effect(3001,'Four saw trail '+str(t),condition,9200,9400,pos='64,-38',scale='1.15,1.15' if t==92 else '.85,.85',angle=-20 if t in [42,66] else 15,extra='persistent = 0')
  ultimate+=effect(3001,'Blood cut '+str(t),condition,9201,9401,pos='64,-38',scale='1.2,1.2' if t==92 else '.9,.9',extra='persistent = 0')
 ultimate+='''[State 3001, Final flash]
type = EnvColor
trigger1 = Time = 92
time = 2
value = 255,235,220
under = 0
[State 3001, Finish emphasis]
type = Pause
trigger1 = Time = 92
time = 6
movetime = 6
[State 3001, Release]
type = TargetState
trigger1 = Time = 100
ID = 3000
value = 3011
[State 3001, End]
type = ChangeState
trigger1 = Time >= 118
value = 0
ctrl = 1

[Statedef 3010]
type = S
movetype = H
physics = N
ctrl = 0
velset = 0,0
[State 3010, Own hurt]
type = ChangeAnim
trigger1 = Time = 0
value = 5000
[State 3010, Cut recoil]
type = ChangeAnim
trigger1 = Time = 25
trigger2 = Time = 48
trigger3 = Time = 72
value = IfElse(SelfAnimExist(5001),5001,5000)
[State 3010, Contact tint]
type = PalFX
trigger1 = Time = 20
time = 70
mul = 256,180,180
[State 3010, Emergency release]
type = SelfState
trigger1 = Time >= 170
trigger2 = NumEnemy > 0
trigger2 = EnemyNear,StateNo != 3000
trigger2 = EnemyNear,StateNo != 3001
value = 0
ctrl = 1
'''
 cns=cns[:begin]+ultimate+cns[end:]
 cns=cns.replace('velset = -5,-6','velset = -6,-4.5')
 (char/'PochitaTrueForm.air').write_text(air.rstrip()+'\n');(char/'PochitaTrueForm.cns').write_text(cns.rstrip()+'\n');(char/'PochitaTrueForm.cmd').write_text(cmd.rstrip()+'\n')
