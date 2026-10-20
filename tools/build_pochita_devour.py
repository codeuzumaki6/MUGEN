#!/usr/bin/env python3
"""Metered regeneration and a finite, hit-confirmed representation of erasure."""
from pathlib import Path
import hashlib,io,json,re,wave
import numpy as np
from PIL import Image
from scipy.ndimage import label,find_objects
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'design/Pochita_devour'

def append_devour_assets(metadata,review):
 char=ROOT/'PochitaTrueForm';records=[];im=Image.open(SOURCE/'devour_poses.png').convert('RGBA')
 labels,_=label(np.array(im.getchannel('A'))>=128,np.ones((3,3)));objects=find_objects(labels);areas=np.bincount(labels.ravel())
 ids=[i+1 for i,s in enumerate(objects) if areas[i+1]>4000]
 ids.sort(key=lambda i:(int(objects[i-1][0].start>im.height*.45),objects[i-1][1].start));assert len(ids)==8,len(ids)
 poses=[]
 for i in ids:
  mask=Image.fromarray((labels==i).astype('uint8')*255);box=mask.getbbox()
  assert box[0]>0 and box[1]>0 and box[2]<im.width and box[3]<im.height,box
  pic=im.copy();pic.putalpha(mask);poses.append((pic.crop(box),box))
 factor=72/poses[0][0].height;metadata['devour']=[]
 for i,(pic,box) in enumerate(poses):
  pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
  feet=pic.getchannel('A').crop((0,pic.height-6,pic.width,pic.height)).getbbox();axis=((feet[0]+feet[2])//2+2,pic.height+2)
  out=Image.new('RGBA',(pic.width+4,pic.height+4));out.alpha_composite(pic,(2,2))
  folder=char/'assets/sprites/devour';folder.mkdir(parents=True,exist_ok=True);path=folder/f'{i}.png';out.save(path)
  pixels=np.array(out);body=(pixels[:,:,3]>=128)&~((pixels[:,:,0]>70)&(pixels[:,:,0]>pixels[:,:,1]*1.3))
  extent=int(np.where(body)[1].max())-axis[0]
  metadata['devour'].append(dict(group=3300,number=i,file=str(path.relative_to(char)),size=out.size,axis=axis,attack_extent=extent,source_sheet='devour_poses',source_cell=i,source_box=box))
  records.append((3300,i,path,axis));review.append(('devour',i,out))
 fx=Image.open(SOURCE/'devour_fx.png').convert('RGBA')
 for row,name in enumerate(['regeneration','erasure','bite']):
  key=name+'_fx';metadata[key]=[];poses=[]
  for col in range(4):
   box=(col*fx.width//4,row*fx.height//3,(col+1)*fx.width//4,(row+1)*fx.height//3)
   pic=fx.crop(box);pic.putalpha(pic.getchannel('A').point(lambda a:255 if a>=128 else 0));bounds=pic.getbbox();assert bounds
   assert bounds[0]>0 and bounds[1]>0 and bounds[2]<pic.width and bounds[3]<pic.height,(name,col,bounds)
   poses.append((pic.crop(bounds),box))
  factor=min(128/max(p.width for p,_ in poses),100/max(p.height for p,_ in poses));axis=(72,110 if row==0 else 60)
  for i,(pic,box) in enumerate(poses):
   pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST);out=Image.new('RGBA',(144,120))
   pos=(72-pic.width//2,axis[1]-pic.height if row==0 else 60-pic.height//2);assert min(pos)>=0;out.alpha_composite(pic,pos)
   folder=char/'assets/sprites'/key;folder.mkdir(parents=True,exist_ok=True);path=folder/f'{i}.png';out.save(path)
   metadata[key].append(dict(group=9700+row,number=i,file=str(path.relative_to(char)),size=out.size,axis=axis,source_sheet='devour_fx',source_cell=row*4+i,source_box=box))
   records.append((9700+row,i,path,axis));review.append((key,i,out))
 return records

def append_devour_sounds(records,manifest):
 folder=ROOT/'PochitaTrueForm/assets/sound';fs=22050
 def read(name):
  with wave.open(str(folder/name),'rb') as f:return np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768
 cut=read('chainsaw_cut.wav');impact=read('impact_heavy.wav');motor=read('chainsaw_long.wav')
 for number,name,duration in [(11,'devour_bite',.55),(12,'erasure_collapse',1.15),(13,'regeneration_pulse',.65)]:
  t=np.arange(round(fs*duration))/fs;out=np.zeros(len(t))
  def layer(sample,gain,start=0,rate=1):
   source=np.interp(np.arange(0,len(sample)-1,rate),np.arange(len(sample)),sample);at=round(start*fs);n=min(len(source),len(out)-at);out[at:at+n]+=source[:n]*gain
  if number==11:layer(impact,.65);layer(cut,.65,.04,.8)
  elif number==12:layer(cut[::-1],.55,0,.65);layer(impact,.5,.48,.7);out+=np.sin(2*np.pi*(100*t-32*t*t))*np.exp(-4*t)*.18
  else:layer(motor,.38,0,.72);out+=np.sin(2*np.pi*(65*t+12*t*t))*np.exp(-5*t)*.13
  out*=np.minimum(1,t/.01)*np.minimum(1,(duration-t)/.08);out*=.9/max(.9,np.max(abs(out)))
  stream=io.BytesIO()
  with wave.open(stream,'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(fs);f.writeframes((out*32767).astype('<i2').tobytes())
  payload=stream.getvalue();path=folder/(name+'.wav');path.write_bytes(payload);records.append((1,number,payload))
  manifest.append(dict(group=1,number=number,filename=path.name,type='nonverbal original effect mix',sources=['chainsaw_cut.wav','impact_heavy.wav','chainsaw_long.wav'],duration=duration,sha256=hashlib.sha256(payload).hexdigest(),voice=False))

def apply_devour_runtime(char):
 cns=(char/'PochitaTrueForm.cns').read_text();air=(char/'PochitaTrueForm.air').read_text();cmd=(char/'PochitaTrueForm.cmd').read_text()
 # Retain the previous five-cut animation as down + physical A, at a lower price.
 begin=cns.index('[Statedef 3000]');end=cns.index('[Statedef 212]',begin)
 old=cns[begin:end];mapping={3000:1500,3001:1501,3010:1510,3011:1511}
 old=re.sub(r'(?<!\d)(3000|3001|3010|3011)(?!\d)',lambda m:str(mapping[int(m[0])]),old)
 old=old.replace('poweradd = -2000','poweradd = -1000').replace('> 1000,500,Floor((Target(1500),LifeMax)*.5)','> 1000,250,Floor((Target(1500),LifeMax)*.25)')
 cns=cns[:begin]+old+cns[end:]
 for source,dest in [(3000,1500),(3001,1501)]:air=air.replace(f'[Begin Action {source}]',f'[Begin Action {dest}]',1)
 commands='''[Command]
name = "Devastacion"
command = /$D,x
time = 1
buffer.time = 3

[Command]
name = "Despertar"
command = /$D,s
time = 1
buffer.time = 1

'''
 cmd=cmd.replace('[Statedef -1]',commands+'[Statedef -1]',1)
 marker='[State -1, Xbox A Ultimate]'
 entries='''[State -1, Down charge regeneration]
type = ChangeState
value = 520
triggerall = command = "Despertar"
triggerall = Power >= 3000
triggerall = Var(36) = 0
triggerall = Var(37) = 0
triggerall = Alive
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 500

[State -1, Down A former ultimate]
type = ChangeState
value = 1500
triggerall = command = "Devastacion"
triggerall = Power >= 1000
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100

'''
 cmd=cmd.replace(marker,entries+marker,1)
 cmd=cmd.replace('triggerall = command = "x"\ntriggerall = Power >= 2000','triggerall = command = "x"\ntriggerall = command != "holddown"\ntriggerall = Power >= 2000',1)
 cmd=cmd.replace('triggerall = command = "holdcharge"\ntriggerall = Power < 3000','triggerall = command = "holdcharge"\ntriggerall = command != "holddown"\ntriggerall = Power < 3000',1)
 # Healing is bounded, never revives, never changes body animation or scale.
 passive='''[State -2, Awakening attack multiplier]
type = AttackMulSet
trigger1 = 1
value = IfElse(Var(36) > 0 && Alive && RoundState = 2,1.2,1)
ignorehitpause = 1
[State -2, Reset awakening at round end or KO]
type = VarSet
trigger1 = RoundState != 2
trigger2 = !Alive
v = 36
value = 0
ignorehitpause = 1
[State -2, Reset awakening cooldown between rounds]
type = VarSet
trigger1 = RoundState != 2
v = 37
value = 0
ignorehitpause = 1
[State -2, Regeneration restored health counter]
type = VarAdd
triggerall = Alive
triggerall = RoundState = 2
triggerall = Var(36) > 0
triggerall = Var(36)%6 = 0
trigger1 = Life < Const(data.life)
v = 33
value = IfElse(Life <= Const(data.life)-4,4,Const(data.life)-Life)
ignorehitpause = 1
[State -2, Regeneration health]
type = LifeAdd
triggerall = Alive
triggerall = RoundState = 2
triggerall = Var(36) > 0
triggerall = Var(36)%6 = 0
trigger1 = Life < Const(data.life)
value = IfElse(Life <= Const(data.life)-4,4,Const(data.life)-Life)
absolute = 1
ignorehitpause = 1
[State -2, Regeneration red embers]
type = Explod
triggerall = Alive
triggerall = Var(36) > 0
trigger1 = NumExplod(9470) = 0
anim = 9700
ID = 9470
postype = p1
pos = 0,0
bindtime = -1
removetime = 24
scale = .9,.9
sprpriority = -1
ownpal = 1
trans = addalpha
alpha = 220,100
ignorehitpause = 1
[State -2, Remove ended aura]
type = RemoveExplod
trigger1 = Var(36) <= 0
ID = 9470
ignorehitpause = 1
[State -2, Awakening countdown]
type = VarAdd
trigger1 = Var(36) > 0
v = 36
value = -1
ignorehitpause = 1
[State -2, Awakening cooldown]
type = VarAdd
trigger1 = Var(37) > 0
v = 37
value = -1
ignorehitpause = 1
'''
 cns=cns.replace('[Statedef -2]','[Statedef -2]\n'+passive,1)
 air+='''\n[Begin Action 520]
Clsn2Default: 1
 Clsn2[0] = -17,-72,17,0
0,0,0,0,6
0,1,0,0,6
0,2,0,0,6
0,3,0,0,6
'''
 for number,times in [(9700,[6,6,6,6]),(9701,[4,6,6,8]),(9702,[3,4,4,5])]:air+=f'\n[Begin Action {number}]\n'+''.join(f'{number},{i},0,0,{t}\n' for i,t in enumerate(times))
 geo={r['number']:r for r in json.loads((char/'assets/sprites.json').read_text())['devour']}
 for number,poses,times,active in [(3000,[0,1,2,3,2,1],[6,6,6,6,16,12],[3,4]),(3001,[1,2,3,4,5,3,4,5,6,7],[10,10,12,12,10,6,8,24,36,26],[])]:
  air+=f'\n[Begin Action {number}]\nClsn2Default: 1\n Clsn2[0] = -17,-72,17,0\n'
  for index,(pose,t) in enumerate(zip(poses,times),1):
   if index in active:air+=f'Clsn1: 1\n Clsn1[0] = 12,-66,{max(24,min(85,geo[pose]["attack_extent"]+1))},-12\n'
   air+=f'3300,{pose},0,0,{t}\n'
 cns+='''
[Statedef 520]
type = S
movetype = I
physics = S
anim = 520
ctrl = 0
velset = 0,0
poweradd = -1000
[State 520, Regeneration duration]
type = VarSet
trigger1 = Time = 0
v = 36
value = 360
[State 520, Regeneration cooldown]
type = VarSet
trigger1 = Time = 0
v = 37
value = 900
[State 520, Clear restored health]
type = VarSet
trigger1 = Time = 0
v = 33
value = 0
[State 520, Awakening pulse]
type = PlaySnd
trigger1 = Time = 0
value = S1,13
channel = 4
[State 520, Return to combat]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 3000]
type = S
movetype = A
physics = N
anim = 3000
ctrl = 0
velset = 0,0
poweradd = -2000
[State 3000, Devour tell]
type = PlaySnd
trigger1 = Time = 0
value = S1,10
channel = 4
[State 3000, Rush]
type = VelSet
trigger1 = Time = 8
x = 7
[State 3000, Stop]
type = VelSet
trigger1 = Time = 24
x = 0
[State 3000, Physical opening]
type = HitDef
trigger1 = AnimElem = 3
attr = S, HA
damage = 0,0
animtype = Heavy
guardflag = MA
hitflag = MAF
priority = 4,Hit
pausetime = 7,10
sparkno = 1
guard.sparkno = -1
hitsound = S1,5
guardsound = S1,6
ground.type = High
ground.hittime = 22
ground.velocity = -1,0
air.hittime = 24
air.velocity = -1,-2
fall = 0
getpower = 0,0
givepower = 0,0
p1stateno = 3001
p2stateno = 3010
ID = 3000
kill = 0
[State 3000, Recover after missed opening]
type = ChangeState
trigger1 = Time >= 52
value = 0
ctrl = 1

[Statedef 3001]
type = S
movetype = A
physics = N
anim = 3001
ctrl = 0
velset = 0,0
[State 3001, Victim health ceiling]
type = VarSet
trigger1 = Time = 0
trigger1 = NumTarget(3000) > 0
v = 28
value = IfElse((Target(3000),LifeMax) > 1000,450,Floor((Target(3000),LifeMax)*.45))
[State 3001, Clear damage account]
type = VarSet
trigger1 = Time = 0
v = 29
value = 0
[State 3001, Protect confirmed cinematic]
type = NotHitBy
trigger1 = 1
value = SCA
time = 1
[State 3001, Hold bitten opponent only after confirmation]
type = TargetBind
triggerall = NumTarget(3000) > 0
trigger1 = Time < 128
ID = 3000
pos = 46,0
[State 3001, Dim scene]
type = BGPalFX
trigger1 = Time = 0
time = 138
mul = 90,60,65
[State 3001, Chainsaw chew]
type = PlaySnd
trigger1 = Time = 18
trigger2 = Time = 46
value = S1,7
channel = 1
[State 3001, White erasure space]
type = EnvColor
trigger1 = Time = 66
time = 44
value = 242,242,242
under = 1
[State 3001, Erase victim representation]
type = TargetState
trigger1 = Time = 66
trigger1 = NumTarget(3000) > 0
ID = 3000
value = 3012
[State 3001, Drain a bounded amount of energy]
type = TargetPowerAdd
trigger1 = Time = 92
trigger1 = NumTarget(3000) > 0
ID = 3000
value = -500
[State 3001, Erasure collapse sound]
type = PlaySnd
trigger1 = Time = 66
value = S1,12
channel = 2
'''
 for tick,weight in [(34,60),(58,100),(92,120),(116,170)]:
  condition=f'trigger1 = Time = {tick}\ntrigger1 = NumTarget(3000) > 0'
  amount='Var(28)-Var(29)' if tick==116 else f'Floor(Var(28)*{weight}/450.0)'
  cns+=f'''[State 3001, Devour damage {tick}]
type = TargetLifeAdd
{condition}
ID = 3000
value = -({amount})
kill = {int(tick==116)}
absolute = 1
[State 3001, Account damage {tick}]
type = VarAdd
{condition}
v = 29
value = {amount}
[State 3001, Bite impact {tick}]
type = PlaySnd
{condition}
value = S1,{11 if tick<66 else 12}
channel = 3
[State 3001, Bite or erasure particles {tick}]
type = Explod
{condition}
anim = {9702 if tick<66 else 9701}
ID = {9472 if tick<66 else 9471}
postype = p1
pos = 46,-40
bindtime = 0
removetime = {16 if tick<66 else 24}
sprpriority = 5
ownpal = 1
scale = .85,.85
removeongethit = 1
[State 3001, Impact vibration {tick}]
type = EnvShake
{condition}
time = 6
freq = 90
ampl = -3
'''
  if tick<66:cns+=f'''[State 3001, Physical bite blood {tick}]
type = Explod
{condition}
anim = 9201
ID = 9401
postype = p1
pos = 46,-40
bindtime = 0
removetime = 14
sprpriority = 4
ownpal = 1
scale = .7,.7
'''
 cns+='''[State 3001, Restore opponent to combat]
type = TargetState
trigger1 = Time = 128
trigger1 = NumTarget(3000) > 0
ID = 3000
value = 3011
[State 3001, Lost opponent safety]
type = ChangeState
trigger1 = NumTarget(3000) = 0
value = 0
ctrl = 1
[State 3001, End]
type = ChangeState
trigger1 = Time >= 154
value = 0
ctrl = 1

[Statedef 3010]
type = S
movetype = H
physics = N
ctrl = 0
velset = 0,0
[State 3010, Opponent own hurt sprite]
type = ChangeAnim
trigger1 = Time = 0
value = 5000
[State 3010, Safety release]
type = SelfState
trigger1 = Time >= 180
trigger2 = NumEnemy = 0
trigger3 = NumEnemy > 0
trigger3 = EnemyNear,StateNo != 3000
trigger3 = EnemyNear,StateNo != 3001
value = 0
ctrl = 1

[Statedef 3012]
type = S
movetype = H
physics = N
ctrl = 0
velset = 0,0
[State 3012, Shrink into erasure]
type = AngleDraw
trigger1 = Time < 8
scale = 1-Time*.11,1-Time*.11
[State 3012, Brief absence]
type = AssertSpecial
trigger1 = Time = [8,43]
flag = invisible
flag2 = noshadow
[State 3012, Reappear]
type = AngleDraw
trigger1 = Time = [44,51]
scale = .12+(Time-44)*.11,.12+(Time-44)*.11
[State 3012, Safety release]
type = SelfState
trigger1 = Time >= 80
trigger2 = NumEnemy = 0
trigger3 = NumEnemy > 0
trigger3 = EnemyNear,StateNo != 3001
value = 0
ctrl = 1

[Statedef 3011]
type = A
movetype = H
physics = N
ctrl = 0
velset = -5,-4
[State 3011, Fall in own states]
type = SelfState
trigger1 = 1
value = 5050
ctrl = 0
'''
 for ext,text in [('cns',cns),('air',air),('cmd',cmd)]: (char/f'PochitaTrueForm.{ext}').write_text(text.rstrip()+'\n')
 print('Built six-second bounded regeneration, down-A five-cut special and hit-confirmed conceptual-erasure adaptation')
