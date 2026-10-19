#!/usr/bin/env python3
"""Mixed-button routes, one special follow-up, and a physical aerial pursuit."""
from pathlib import Path
import json,re

def apply_flow_runtime(char):
 cns=(char/'PochitaTrueForm.cns').read_text();air=(char/'PochitaTrueForm.air').read_text();cmd=(char/'PochitaTrueForm.cmd').read_text()
 geometry={(r['group'],r['number']):r for rows in json.loads((char/'assets/sprites.json').read_text()).values() for r in rows}
 def insert_state(state,text):
  nonlocal cns
  match=re.search(rf'(?is)\[Statedef {state}\].*?(?=\[Statedef|\Z)',cns);assert match,state
  pos=match[0].find(f'[State {state}, End]');pos=len(match[0]) if pos<0 else pos
  cns=cns[:match.start()]+match[0][:pos]+text+match[0][pos:]+cns[match.end():]
 def replace_state(state,func):
  nonlocal cns
  match=re.search(rf'(?is)\[Statedef {state}\].*?(?=\[Statedef|\Z)',cns);assert match;cns=cns[:match.start()]+func(match[0])+cns[match.end():]
 def animation(number,indices,times,active=()):
  result=f'[Begin Action {number}]\nClsn2Default: 1\n Clsn2[0] = -17,-72,17,0\n'
  for frame,(index,time) in enumerate(zip(indices,times),1):
   if frame in active:result+=f'Clsn1: 1\n Clsn1[0] = 12,-66,{max(24,geometry[3200,index]["attack_extent"]+1)},-12\n'
   result+=f'3200,{index},0,0,{time}\n'
  return result+'\n'
 def replace_animation(number,text):
  nonlocal air
  air,n=re.subn(rf'(?ims)^\[Begin Action {number}\].*?(?=^\[Begin Action|\Z)',lambda m:text,air,count=1);assert n
 air+=animation(650,[0,1,2,3],[2,3,3,4])
 replace_animation(620,animation(620,[8,9,10,11],[3,4,5,6],(2,3)))
 # Same five real contacts and cost, using a forward-driving rush silhouette.
 replace_animation(1100,animation(1100,[4,5,6,7,5,6,7,5,6,7,5,6,7,7,7,11,11],[3]*17,tuple(range(2,14))))
 routes=''
 for state in [200,210,220,201,211,221]:
  first=state in [200,210,220];targets=[201,211,221] if first else [202,212,222]
  insert_state(state,f'''[State {state}, Clear route press]
type = VarSet
trigger1 = Time = 0
v = 31
value = 0
ignorehitpause = 1
[State {state}, Buffer route press]
type = VarSet
triggerall = Time > 0
triggerall = command != "holddown"
trigger1 = command = "a"
trigger2 = command = "b"
trigger3 = command = "c"
v = 31
value = IfElse(command = "a",{targets[0]},IfElse(command = "b",{targets[1]},{targets[2]}))
ignorehitpause = 1
''')
  routes+=f'''[State -1, Mixed route from {state}]
type = ChangeState
triggerall = StateNo = {state}
triggerall = Time > 0
triggerall = MoveHit
trigger1 = Var(31) > 0
value = Var(31)
ignorehitpause = 1

'''
 # Higher priority than normal chain buffers, but after directional specials.
 marker='[State -1, Hit confirmed 200 to 201]';assert marker in cmd;cmd=cmd.replace(marker,routes+marker,1)
 pursuit='''[State -1, Pursue launcher]
type = ChangeState
triggerall = StateNo = 202
triggerall = MoveHit
triggerall = NumTarget > 0
triggerall = command = "holdup"
triggerall = Time >= 9
trigger1 = HitPauseTime = 0
value = 650

'''
 for button,state in [('a',600),('b',610),('c',620)]:
  pursuit+=f'''[State -1, Pursuit air attack {button}]
type = ChangeState
triggerall = StateNo = 650
triggerall = Time >= 3
trigger1 = command = "{button}"
value = {state}

'''
 cmd=cmd.replace(marker,pursuit+marker,1)
 # The extension pushes the opponent away. A real step keeps its short-range
 # launcher follow-up connected without inflating the attack box.
 insert_state(202,'''[State 202, Step into launcher]
type = VelSet
trigger1 = Time < 6
x = 4
[State 202, Plant feet]
type = VelSet
trigger1 = Time >= 6
x = 0
''')
 cns+='''\n[Statedef 650]
type = A
movetype = I
physics = A
anim = 650
ctrl = 0
velset = 3.8,-6
[State 650, Rising motors]
type = PlaySnd
trigger1 = Time = 0
value = S1,6
channel = 3
[State 650, Trail]
type = AfterImage
trigger1 = Time = 0
time = 10
length = 4
timegap = 1
framegap = 2
palcolor = 256
palbright = 5,-20,-20
palmul = .8,.7,.7
trans = add
[State 650, Return to air control]
type = ChangeState
trigger1 = AnimTime = 0
value = 50
ctrl = 1
'''
 replace_state(620,lambda block:block.replace('ground.velocity = -3.2,-5','ground.velocity = -2,5').replace('air.velocity = -3.2,-5','air.velocity = -2,7'))
 insert_state(620,'''[State 620, Dive momentum]
type = VelSet
trigger1 = MoveHit
trigger1 = HitPauseTime = 0
x = .8
y = 4.5
''')
 specials=[1000,1010,1020,1030,1040,1050,1060,1070,1080,1100]
 # Reset only once a sequence ends; never reset on entering a linked special.
 insert_state(-2,'''[State -2, Reset special chain budget]
type = VarSet
trigger1 = Ctrl
trigger2 = MoveType = H
trigger3 = RoundState != 2
v = 32
value = 0
ignorehitpause = 1
''')
 for state in specials:
  insert_state(state,f'''[State {state}, Count special in sequence]
type = VarAdd
trigger1 = Time = 0
v = 32
value = 1
persistent = 0
''')
 # Add one follow-up to each command, only from another confirmed special.
 names=['Desgarro','CuatroBrazos','Ascenso','Estocada','Barrido','Guillotina','Embestida','Carniceria','Rasante','Asalto']
 for dest,name in zip(specials,names):
  pattern=rf'(?ims)^\[State -1, {name}\].*?(?=^\[State |\Z)';match=re.search(pattern,cmd);assert match,name
  block=match[0]
  for index,source in enumerate([s for s in specials if s!=dest],10):
   block+=f'trigger{index} = StateNo = {source}\ntrigger{index} = MoveHit\ntrigger{index} = Time > 0\ntrigger{index} = Var(32) < 2\n'
  cmd=cmd[:match.start()]+block+'\n'+cmd[match.end():]
 (char/'PochitaTrueForm.cns').write_text(cns.rstrip()+'\n');(char/'PochitaTrueForm.air').write_text(air.rstrip()+'\n');(char/'PochitaTrueForm.cmd').write_text(cmd.rstrip()+'\n')
 print('Integrated mixed routes, physical pursuit, dive finisher and a two-special sequence limit')
