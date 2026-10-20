#!/usr/bin/env python3
"""Longer physical special sequences with six distinct animated trail families."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'PochitaTrueForm';SOURCE=ROOT/'design/Pochita_especiales_largos'
def seq(group,indices):return [(group,n) for n in indices]
# Contacts redistribute the previous total damage; extra length is not extra reach.
SPECS={
1000:dict(poses=seq(200,range(7))+seq(210,range(6))+seq(240,range(6)),ticks=3,hits=[3,9,16],damage=[28,32,46],reach=80,family=0),
1010:dict(poses=seq(230,range(17))+seq(3100,[2,3,5,6,7]),ticks=3,hits=[3,6,9,13,18],damage=[20,20,24,24,44],reach=85,family=1),
1030:dict(poses=seq(220,range(7,17))+seq(3100,[3,4,5,7]),ticks=4,hits=[3,7,11],damage=[30,34,62],reach=150,family=2),
1040:dict(poses=seq(250,range(8))+seq(250,[5,4,3,2,1,0]),ticks=4,hits=[4,10],damage=[34,62],reach=82,family=3),
1060:dict(poses=seq(200,range(7))+seq(210,range(6))+seq(3200,[4,5,6,7])+seq(240,[3,4,5]),ticks=3,hits=[3,10,18],damage=[35,40,70],reach=90,family=4),
1070:dict(poses=seq(230,range(17))+seq(200,range(7))+seq(3100,[1,2,3,5,6,7]),ticks=3,hits=[3,6,9,13,18,23,28],damage=[18,18,20,22,26,34,80],reach=90,family=5),
}
FAMILIES=['crescent','four_saws','thrust','ground_sweep','rush_wake','carnage']

def append_spectacle_assets(metadata,review):
 im=Image.open(SOURCE/'special_trails.png').convert('RGBA');records=[]
 # The generated rows have different heights; inspected transparent gutters
 # prevent the wake and final cleave from being split at nominal grid lines.
 ycuts=[0,171,342,500,660,795,im.height]
 for row,name in enumerate(FAMILIES):
  key='special_'+name;metadata[key]=[];folder=CHAR/'assets/sprites'/key;folder.mkdir(parents=True,exist_ok=True)
  poses=[]
  for column in range(4):
   box=(round(im.width*column/4),ycuts[row],round(im.width*(column+1)/4),ycuts[row+1])
   pic=im.crop(box);pic.putalpha(pic.getchannel('A').point(lambda v:255 if v>=128 else 0));bbox=pic.getchannel('A').getbbox();assert bbox,(row,column)
   assert bbox[0]>0 and bbox[1]>0 and bbox[2]<pic.width and bbox[3]<pic.height,('source crop reaches cell edge',row,column,bbox)
   poses.append((pic.crop(bbox),box))
  factor=min(132/max(pic.width for pic,_ in poses),104/max(pic.height for pic,_ in poses));size=(144,120);axis=(72,110 if row==3 else 60)
  for index,(pic,box) in enumerate(poses):
   pic=pic.resize((max(1,round(pic.width*factor)),max(1,round(pic.height*factor))),Image.Resampling.NEAREST)
   pos=(axis[0]-pic.width//2,axis[1]-pic.height if row==3 else axis[1]-pic.height//2)
   out=Image.new('RGBA',size);assert min(pos)>=0;out.alpha_composite(pic,pos);path=folder/f'{index}.png';out.save(path)
   metadata[key].append(dict(group=9600+row,number=index,file=str(path.relative_to(CHAR)),size=size,axis=axis,source_sheet='special_trails',source_cell=row*4+index,source_box=box));records.append((9600+row,index,path,axis));review.append((key,index,out))
 return records

def apply_spectacle_runtime(char):
 air=(char/'PochitaTrueForm.air').read_text();cns=(char/'PochitaTrueForm.cns').read_text();meta=json.loads((char/'assets/sprites.json').read_text());geo={(r['group'],r['number']):r for rows in meta.values() for r in rows}
 for row in range(6):air+=f'\n[Begin Action {9600+row}]\n'+''.join(f'{9600+row},{i},0,0,{t}\n' for i,t in enumerate([2,3,3,4]))
 for state,spec in SPECS.items():
  low=state==1040;active={i for hit in spec['hits'] for i in [hit,hit+1]};anim=f'[Begin Action {state}]\nClsn2Default: 1\n Clsn2[0] = -17,{-44 if low else -72},17,0\n'
  for i,(group,number) in enumerate(spec['poses'],1):
   if i in active:anim+=f'Clsn1: 1\n Clsn1[0] = 12,{-38 if low else -66},{min(spec["reach"],max(24,geo[group,number]["attack_extent"]+1))},{-2 if low else -18}\n'
   anim+=f'{group},{number},0,0,{spec["ticks"]}\n'
  air,n=re.subn(rf'(?ims)^\[Begin Action {state}\].*?(?=^\[Begin Action|\Z)',lambda m:anim+'\n',air,count=1);assert n
  m=re.search(rf'(?is)\[Statedef {state}\].*?(?=\[Statedef|\Z)',cns);assert m;block=m[0]
  parts=re.split(r'(?im)(?=^\[State\s)',block);hitdefs=[p for p in parts if re.search(r'(?im)^type\s*=\s*HitDef\s*$',p)];assert hitdefs
  fresh=''
  for i,(element,damage) in enumerate(zip(spec['hits'],spec['damage'])):
   template=hitdefs[-1] if i==len(spec['hits'])-1 else hitdefs[0]
   template=re.sub(r'^\[State[^\]]+\]',f'[State {state}, Choreographed blade contact {element}]',template,count=1)
   template=re.sub(r'(?im)^trigger1\s*=\s*AnimElem\s*=\s*\d+',f'trigger1 = AnimElem = {element}',template,count=1)
   template=re.sub(r'(?im)^damage\s*=.*$',f'damage = {damage},{max(1,damage//12)}',template,count=1)
   if i<len(spec['hits'])-1:
    template=re.sub(r'(?im)^fall\s*=.*$','fall = 0',template)
    template=re.sub(r'(?im)^ground.velocity\s*=.*$','ground.velocity = -.4,0',template)
    template=re.sub(r'(?im)^ground.hittime\s*=.*$','ground.hittime = 28',template)
   fresh+=template
  replaced=False;rebuilt=''
  for part in parts:
   if part in hitdefs:
    if not replaced:rebuilt+=fresh;replaced=True
   else:rebuilt+=part
  block=rebuilt
  # Insert before the transition out, so terminal-state effects can execute.
  at=block.find(f'[State {state}, End]');assert at>=0
  visual=f'''[State {state}, Clear final impact latch]
type = VarSet
trigger1 = Time = 0
v = 35
value = 0
ignorehitpause = 1
'''
  for i,element in enumerate(spec['hits']):
   visual+=f'''[State {state}, Animated saw path {element}]
type = Explod
triggerall = NumExplod(9460) < 2
trigger1 = AnimElem = {element}
anim = {9600+spec['family']}
ID = 9460
postype = p1
pos = {26 if low else 34},{0 if low else -36}
facing = 1
bindtime = {0 if low else -1}
removetime = 12
scale = {'.85,.75' if low else '.8,.8' if state!=1030 else '.9,.65'}
sprpriority = {-1 if state==1060 else 3}
ownpal = 1
trans = addalpha
alpha = 200,256
removeongethit = 1
persistent = 0
ignorehitpause = 1
'''
  finaltime=(spec['hits'][-1]-1)*spec['ticks']
  condition=f'triggerall = Time >= {finaltime}\ntriggerall = MoveHit\ntriggerall = HitCount >= {len(spec["hits"])}\ntrigger1 = Var(35) = 0'
  visual+=f'''[State {state}, Confirmed finish sparks]
type = Explod
{condition}
anim = {9600+spec['family']}
ID = 9461
postype = p1
pos = {38 if not low else 30},{-34 if not low else 0}
facing = 1
bindtime = 0
removetime = 12
scale = .95,.95
sprpriority = 5
ownpal = 1
trans = addalpha
alpha = 224,256
removeongethit = 1
ignorehitpause = 1
[State {state}, Finish impact sound]
type = PlaySnd
{condition}
value = S1,{9 if state in [1040,1060,1070] else 8}
channel = 5
volumescale = 80
ignorehitpause = 1
[State {state}, Finish stage vibration]
type = EnvShake
{condition}
time = 7
freq = 90
ampl = -3
ignorehitpause = 1
[State {state}, Latch finish]
type = VarSet
{condition}
v = 35
value = 1
ignorehitpause = 1
'''
  if state in [1000,1030,1060]:
   visual+=f'''[State {state}, Moving blade afterimages]
type = AfterImage
trigger1 = Time = 3
time = {min(40,len(spec['poses'])*spec['ticks']-6)}
length = 5
timegap = 1
framegap = 3
palcolor = 256
palbright = 10,-15,-15
palmul = .8,.7,.7
trans = add
'''
  # Follow with ground velocity rather than snapping the enemy into the attack.
  if state in [1010,1070]:
   visual+=f'''[State {state}, Step into the opening cut]
type = VelSet
triggerall = Time < 8
trigger1 = P2Dist X > 38
x = 4
'''
  if state in [1000,1010,1040,1060,1070]:
   visual+=f'''[State {state}, Physical follow-through]
type = VelSet
triggerall = Time >= 10
triggerall = Time < {finaltime}
triggerall = MoveHit
trigger1 = P2Dist X > 34
x = 2.4
[State {state}, Plant feet for the last cut]
type = VelSet
trigger1 = Time >= {finaltime}
x = 0
'''
  block=block[:at]+visual+'\n'+block[at:];cns=cns[:m.start()]+block+cns[m.end():]
 (char/'PochitaTrueForm.air').write_text(air.rstrip()+'\n');(char/'PochitaTrueForm.cns').write_text(cns.rstrip()+'\n')
 (char/'assets/special_choreography.json').write_text(json.dumps({str(state):dict(frames=len(s['poses']),ticks_per_frame=s['ticks'],contacts=len(s['hits']),damage=sum(s['damage']),family=FAMILIES[s['family']],animation_ticks=len(s['poses'])*s['ticks']) for state,s in SPECS.items()},indent=2)+'\n')
 print('Built six extended physical sequences with distinct saw trails and confirmed finishers')
