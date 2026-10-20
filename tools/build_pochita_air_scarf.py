#!/usr/bin/env python3
"""Finite mixed aerial routes and two physical, confirmed intestinal-scarf grabs."""
from pathlib import Path
import json,re

def apply_air_scarf_runtime(char):
 cns=(char/'PochitaTrueForm.cns').read_text();air=(char/'PochitaTrueForm.air').read_text();cmd=(char/'PochitaTrueForm.cmd').read_text()
 geo={(r['group'],r['number']):r for rows in json.loads((char/'assets/sprites.json').read_text()).values() for r in rows}
 def replace_state(n,block):
  nonlocal cns
  cns,count=re.subn(rf'(?ims)^\[Statedef {n}\].*?(?=^\[Statedef|\Z)',lambda m:block+'\n',cns,count=1);assert count,n
 def animation(n,group,indices,times,active=(),scarf=False):
  out=f'[Begin Action {n}]\nClsn2Default: 1\n Clsn2[0] = -17,-72,17,0\n'
  for e,(i,t) in enumerate(zip(indices,times),1):
   if e in active:
    extent=geo[group,i]['scarf_extent' if scarf else 'attack_extent']
    out+=f'Clsn1: 1\n Clsn1[0] = 12,-66,{max(24,extent)},-12\n'
   out+=f'{group},{i},0,0,{t}\n'
  return out+'\n'
 def effect(n,condition,anim,ident,pos='36,-36',scale='.7,.7'):
  return f'''[State {n}, Effect {ident}]
type = Explod
{condition}
anim = {anim}
ID = {ident}
postype = p1
pos = {pos}
bindtime = 0
removetime = 16
sprpriority = 4
scale = {scale}
ownpal = 1
removeongethit = 1
ignorehitpause = 1
'''
 # Eighteen is the per-flight attack budget; nineteen is a fresh buffered press.
 passive='''[State -2, Reset air route on landing or injury]
type = VarSet
trigger1 = StateType != A
trigger2 = MoveType = H
trigger3 = RoundState != 2
v = 18
value = 0
ignorehitpause = 1
'''
 cns=cns.replace('[Statedef -2]','[Statedef -2]\n'+passive,1)
 cns=cns.replace('triggerall = StateNo = [600,620]','triggerall = (StateNo = [600,620]) || (StateNo = [660,672])',1)
 # Remove the former two fixed air links. All three buttons now work at each stage.
 for label in ['Hit confirmed 600 to 610','Hit confirmed 610 to 620']:
  cmd,count=re.subn(rf'(?ims)^\[State -1, {label}\].*?(?=^\[State |\Z)','',cmd,count=1);assert count
 for label in ['AI air cut','Air a','Air b','Air c']:
  pattern=rf'(?ims)^\[State -1, {label}\].*?(?=^\[State |\Z)'
  cmd,count=re.subn(pattern,lambda m:m[0].replace('trigger1 = Ctrl','triggerall = Var(18) < 3\ntrigger1 = Ctrl'),cmd,count=1);assert count
 route='''[State -1, Mixed aerial continuation]
type = ChangeState
triggerall = (StateNo = 600) || (StateNo = 610) || (StateNo = 620) || (StateNo = [660,662])
triggerall = MoveHit
triggerall = Time > 0
triggerall = Var(18) < 3
trigger1 = Var(19) > 0
value = IfElse(Var(18) = 1,660,670)+Var(19)-1
ignorehitpause = 1

'''
 cmd=cmd.replace('[State -1, Normal a]',route+'[State -1, Normal a]',1)
 def hit(n,e,damage,final=False,button=0):
  vx=-6 if final and button==0 else -4.5 if final and button==1 else -2 if final else -.65
  vy=7 if final and button==2 else -3 if final else -2.4
  return f'''[State {n}, Saw collision {e}]
type = HitDef
trigger1 = AnimElem = {e}
attr = A, NA
damage = {damage},2
animtype = {'Heavy' if final else 'Medium'}
guardflag = MA
hitflag = MAF
priority = 4,Hit
pausetime = {8 if final else 6},{12 if final else 10}
sparkno = 1
sparkxy = -10,-38
guardsound = S1,6
hitsound = S1,{9 if final and button==2 else 7 if final else 4}
ground.type = High
ground.hittime = 28
ground.velocity = {vx},{vy if final else -3}
air.hittime = 30
air.velocity = {vx},{vy}
fall = {int(final)}
fall.recover = 1
fall.recovertime = 32
getpower = 30,5
givepower = 12,4
envshake.time = {7 if final else 3}
envshake.ampl = {-3 if final else -1}
'''
 for stage,numbers in enumerate([[600,610,620],[660,661,662],[670,671,672]]):
  for button,n in enumerate(numbers):
   final=stage==2
   if button==0:group,indices=600,list(range(7))
   elif button==1:group,indices=610,list(range(5))
   else:group,indices=3200,[8,9,10,11]
   times=[3]*len(indices);active=(2,3)
   if final and button==1:indices=[0,1,2,3,2,3,2,3,4];times=[3]*len(indices);active=(3,4,5,6,7,8)
   anim=animation(n,group,indices,times,active)
   if stage==0:air,count=re.subn(rf'(?ims)^\[Begin Action {n}\].*?(?=^\[Begin Action|\Z)',lambda m:anim,air,count=1);assert count
   else:air+=anim
   damage=([50,52,70] if stage==0 else [45,55,55] if stage==1 else [85,95,100])[button]
   block=f'''[Statedef {n}]
type = A
movetype = A
physics = A
anim = {n}
ctrl = 0
[State {n}, Count air attack]
type = VarAdd
trigger1 = Time = 0
v = 18
value = 1
persistent = 0
[State {n}, Clear fresh press]
type = VarSet
trigger1 = Time = 0
v = 19
value = 0
ignorehitpause = 1
[State {n}, Clear contact gate]
type = VarSet
trigger1 = Time = 0
v = 20
value = 0
ignorehitpause = 1
[State {n}, Motor]
type = PlaySnd
trigger1 = Time = 0
value = S1,{7 if final and button==1 else 8 if final else 0}
channel = 1
'''
   if final and button==1:
    for e,d in [(3,20),(5,20),(7,55)]:block+=hit(n,e,d,e==7,button)
   else:block+=hit(n,2,damage,final,button)
   if not final:
    block+=f'''[State {n}, Buffer next air button]
type = VarSet
triggerall = Time > 0
trigger1 = command = "a"
trigger2 = command = "b"
trigger3 = command = "c"
v = 19
value = IfElse(command = "a",1,IfElse(command = "b",2,3))
ignorehitpause = 1
[State {n}, CPU next air button]
type = VarSet
triggerall = AILevel > 0
trigger1 = MoveHit
v = 19
value = IfElse(Var(18) = 1,2,3)
ignorehitpause = 1
[State {n}, Physical follow through]
type = VelSet
triggerall = MoveHit
trigger1 = Var(20) = 0
x = 1.2
y = -2.4
ignorehitpause = 1
'''
   if final and button==1:
    block+=f'''[State {n}, Follow the grinding contacts]
type = VelSet
triggerall = MoveHit
trigger1 = HitCount > Var(20)
x = .65
y = -2.4
ignorehitpause = 1
'''
   condition='triggerall = MoveHit\ntrigger1 = HitCount > Var(20)'
   block+=effect(n,condition,9200,9400,scale='.9,.9' if final else '.65,.65')+effect(n,condition,9201,9401)
   block+=f'''[State {n}, Latch physical contact]
type = VarSet
{condition}
v = 20
value = HitCount
ignorehitpause = 1
'''
   if final:
    block+=f'''[State {n}, Trail]
type = AfterImage
trigger1 = Time = 1
time = 14
length = 4
timegap = 1
framegap = 2
trans = add
'''
    if button==2:block+=f'''[State {n}, Dive with confirmed finisher]
type = VelSet
trigger1 = MoveHit
trigger1 = HitPauseTime = 0
x = 1
y = 5
'''
   block+=f'''[State {n}, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 50
ctrl = 1
'''
   if stage==0:replace_state(n,block)
   else:cns+='\n'+block
 # Scarf actions use actual rendered red reach, not the arm-saw extent.
 for n in [1200,1210]:air+=animation(n,3400,[0,1,2,3,4,5,7],[5,7,5,7,5,6,8],(3,4,5),True)
 air+=animation(1201,3400,[4,4,4,5,7],[8,8,8,4,4])
 air+=animation(1211,3400,[4,5,6,5,6,5,6,7],[8,4,6,4,6,4,8,8])
 definitions=''
 for name,button in [('LazoIntestinal','y'),('SujetarYDesgarrar','z')]:definitions+=f'[Command]\nname = "{name}"\ncommand = /$D,{button}\ntime = 1\nbuffer.time = 3\n\n'
 cmd=cmd.replace('[Statedef -1]',definitions+'[Statedef -1]',1)
 entries=''
 for name,n,cost in [('LazoIntestinal',1200,350),('SujetarYDesgarrar',1210,600)]:
  entries+=f'''[State -1, {name}]
type = ChangeState
triggerall = command = "{name}"
triggerall = StateType != A
triggerall = Power >= {cost}
trigger1 = Ctrl
trigger2 = StateNo = 100
'''
  for index,normal in enumerate([200,201,202,210,211,212,220,221,222],3):entries+=f'trigger{index} = StateNo = {normal}\ntrigger{index} = MoveHit\n'
  entries+=f'value = {n}\n\n'
 cmd=cmd.replace('[State -1, Xbox A Ultimate]',entries+'[State -1, Xbox A Ultimate]',1)
 for label in ['Asalto','RB Chainsaw guard']:
  pattern=rf'(?ims)^\[State -1, {label}\].*?(?=^\[State |\Z)'
  cmd,count=re.subn(pattern,lambda m:m[0].replace('triggerall = Power >=','triggerall = command != "holddown"\ntriggerall = Power >=',1),cmd,count=1);assert count,label
 for n,cost in [(1200,350),(1210,600)]:
  ident=n;follow=n+1
  cns+=f'''\n[Statedef {n}]
type = S
movetype = A
physics = S
anim = {n}
ctrl = 0
velset = 0,0
poweradd = -{cost}
[State {n}, Activation]
type = PlaySnd
trigger1 = Time = 0
value = S1,10
channel = 3
[State {n}, Organic whip]
type = PlaySnd
trigger1 = AnimElem = 3
value = S1,6
channel = 1
[State {n}, Physical loop contact]
type = HitDef
trigger1 = AnimElem = 3
attr = S, SA
damage = {40 if n==1200 else 30},0
animtype = Heavy
guardflag = MA
hitflag = M
priority = 4,Hit
pausetime = 6,9
sparkno = 1
sparkxy = -10,-38
hitsound = S1,4
guardsound = S1,6
ground.type = High
ground.hittime = 22
ground.velocity = 0,0
air.velocity = -2,-3
fall = 0
getpower = 0,0
givepower = 10,5
ID = {ident}
p1stateno = {follow}
p2stateno = 1220
[State {n}, Recover after missed loop]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1
'''
  cns+=f'''[Statedef {follow}]
type = S
movetype = A
physics = S
anim = {follow}
ctrl = 0
velset = 0,0
[State {follow}, Ground the confirmed victim]
type = TargetBind
triggerall = NumTarget({ident}) > 0
trigger1 = Time < {24 if n==1200 else 38}
ID = {ident}
pos = 68,0
[State {follow}, Face the victim]
type = TargetFacing
trigger1 = NumTarget({ident}) > 0
ID = {ident}
value = -1
'''
  if n==1210:
   for t,d in [(12,35),(24,35),(36,90)]:
    condition=f'trigger1 = Time = {t}\ntrigger1 = NumTarget({ident}) > 0'
    cns+=f'''[State {follow}, Confirmed cut {t}]
type = TargetLifeAdd
{condition}
ID = {ident}
value = -{d}
kill = 1
absolute = 1
[State {follow}, Cut sound {t}]
type = PlaySnd
{condition}
value = S1,{9 if t==36 else 8}
channel = 1
[State {follow}, Cut shake {t}]
type = EnvShake
{condition}
time = {8 if t==36 else 4}
ampl = {-4 if t==36 else -2}
'''
    cns+=effect(follow,condition,9200,9400,'68,-38','.9,.9')+effect(follow,condition,9201,9401,'68,-38','.8,.8')
   cns+=f'''[State {follow}, Release launch velocity]
type = TargetVelSet
trigger1 = Time = 38
trigger1 = NumTarget({ident}) > 0
ID = {ident}
x = -5
y = -5
'''
  end=24 if n==1200 else 38
  cns+=f'''[State {follow}, Release victim]
type = TargetState
trigger1 = Time = {end}
trigger1 = NumTarget({ident}) > 0
ID = {ident}
value = {1221 if n==1200 else 1222}
[State {follow}, End confirmed hold]
type = ChangeState
trigger1 = Time >= {end+4}
trigger2 = NumTarget({ident}) = 0
value = 0
ctrl = 1
'''
 cns+='''[Statedef 1220]
type = S
movetype = H
physics = N
ctrl = 0
velset = 0,0
[State 1220, Victim own hurt pose]
type = ChangeAnim
trigger1 = Time = 0
value = 5000
[State 1220, Ground position]
type = PosSet
trigger1 = 1
y = 0
[State 1220, Release if attacker interrupted]
type = SelfState
trigger1 = Time > 4
trigger1 = (EnemyNear,StateNo) != 1201
trigger1 = (EnemyNear,StateNo) != 1211
trigger2 = Time >= 65
value = 0
ctrl = 1

[Statedef 1221]
type = S
movetype = H
physics = S
ctrl = 0
velset = 0,0
[State 1221, Victim own brief stagger]
type = ChangeAnim
trigger1 = Time = 0
value = 5000
[State 1221, Recover from stagger]
type = SelfState
trigger1 = Time >= 20
trigger2 = !Alive
value = 0
ctrl = 1

[Statedef 1222]
type = A
movetype = H
physics = N
ctrl = 0
[State 1222, Fall marker]
type = HitFallSet
trigger1 = Time = 0
value = 1
[State 1222, Return to own airborne hurt states]
type = SelfState
trigger1 = Time = 0
value = 5050
ctrl = 0
'''

 (char/'PochitaTrueForm.cns').write_text(cns.rstrip()+'\n');(char/'PochitaTrueForm.air').write_text(air.rstrip()+'\n');(char/'PochitaTrueForm.cmd').write_text(cmd.rstrip()+'\n')
 print('Integrated 27 finite aerial routes and down-RB/down-RT physical scarf captures')

def append_scarf_assets(metadata,review):
 from PIL import Image
 import numpy as np
 from scipy.ndimage import label,find_objects
 root=Path(__file__).resolve().parents[1];char=root/'PochitaTrueForm';im=Image.open(root/'design/Pochita_bufanda/scarf_poses.png').convert('RGBA')
 mask=np.array(im.getchannel('A'))>=128;labels,_=label(mask,np.ones((3,3)));objects=find_objects(labels);areas=np.bincount(labels.ravel())
 bodies=[i+1 for i,obj in enumerate(objects) if areas[i+1]>3000]
 bodies.sort(key=lambda i:(int((objects[i-1][0].start+objects[i-1][0].stop)/2)//(im.height//4),objects[i-1][1].start));assert len(bodies)==8,len(bodies)
 reference=objects[bodies[0]-1][0];factor=72/(reference.stop-reference.start);records=[];metadata['scarf']=[]
 for index,body in enumerate(bodies):
  obj=objects[body-1];members=[body]
  for j,small in enumerate(objects,1):
   if j in bodies:continue
   y=(small[0].start+small[0].stop)/2;x=(small[1].start+small[1].stop)/2
   if obj[0].start-5<=y<=obj[0].stop+5 and obj[1].start-5<=x<=obj[1].stop+5:members.append(j)
  alpha=Image.fromarray(np.isin(labels,members).astype('uint8')*255);box=alpha.getbbox();assert box and min(box[:2])>0 and box[2]<im.width and box[3]<im.height,box
  pic=im.copy();pic.putalpha(alpha);pic=pic.crop(box);pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
  feet=pic.getchannel('A').crop((0,pic.height-5,pic.width,pic.height)).getbbox();assert feet
  axis=((feet[0]+feet[2])//2+2,pic.height+2);out=Image.new('RGBA',(pic.width+4,pic.height+4));out.alpha_composite(pic,(2,2))
  folder=char/'assets/sprites/scarf';folder.mkdir(parents=True,exist_ok=True);path=folder/f'{index}.png';out.save(path);pixels=np.array(out)
  opaque=pixels[:,:,3]>=128;nonred=opaque&~((pixels[:,:,0]>70)&(pixels[:,:,0]>pixels[:,:,1]*1.3))
  metadata['scarf'].append(dict(group=3400,number=index,file=str(path.relative_to(char)),size=out.size,axis=axis,attack_extent=int(np.where(nonred)[1].max())-axis[0],scarf_extent=int(np.where(opaque)[1].max())-axis[0],source_sheet='scarf_poses',source_cell=index,source_box=box))
  records.append((3400,index,path,axis));review.append(('scarf',index,out))
 return records
