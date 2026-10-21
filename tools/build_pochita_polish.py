#!/usr/bin/env python3
"""Presentation-only engine revving, scarf locomotion, contact readability and win."""
from pathlib import Path
import hashlib,io,json,re,wave
import numpy as np
from PIL import Image
from scipy.ndimage import label,find_objects
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'PochitaTrueForm';SOURCE=ROOT/'design/Pochita_acabado'

def append_polish_assets(metadata,review):
 records=[];body_factor=None;reference_width=None
 for name,group in [('charge_victory',3500),('locomotion',3501)]:
  im=Image.open(SOURCE/(name+'.png')).convert('RGBA');labels,_=label(np.array(im.getchannel('A'))>=128,np.ones((3,3)));objects=find_objects(labels);areas=np.bincount(labels.ravel())
  bodies=[i+1 for i,s in enumerate(objects) if areas[i+1]>2000]
  bodies.sort(key=lambda i:(int((objects[i-1][0].start+objects[i-1][0].stop)/2)//(im.height//4),objects[i-1][1].start));assert len(bodies)==8,(name,len(bodies))
  crops=[]
  for body in bodies:
   obj=objects[body-1];members=[body]
   for j,small in enumerate(objects,1):
    if j in bodies:continue
    y=(small[0].start+small[0].stop)/2;x=(small[1].start+small[1].stop)/2
    if obj[0].start-5<=y<=obj[0].stop+5 and obj[1].start-5<=x<=obj[1].stop+5:members.append(j)
   alpha=Image.fromarray(np.isin(labels,members).astype('uint8')*255);box=alpha.getbbox();assert box and min(box[:2])>0 and box[2]<im.width and box[3]<im.height,(name,box)
   pic=im.copy();pic.putalpha(alpha);crops.append((pic.crop(box),box))
  # One relaxed victory frame calibrates both new body sheets at the same
  # pixel density. Crouches and run strides retain their natural lower height.
  if body_factor is None:body_factor=72/crops[7][0].height;reference_width=im.width
  factor=body_factor*reference_width/im.width;metadata[name]=[]
  for index,(pic,box) in enumerate(crops):
   pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
   feet=pic.getchannel('A').crop((0,pic.height-5,pic.width,pic.height)).getbbox();assert feet
   axis=((feet[0]+feet[2])//2+2,pic.height+2);out=Image.new('RGBA',(pic.width+4,pic.height+4));out.alpha_composite(pic,(2,2))
   folder=CHAR/'assets/sprites'/name;folder.mkdir(parents=True,exist_ok=True);path=folder/f'{index}.png';out.save(path);pixels=np.array(out)
   body=(pixels[:,:,3]>=128)&~((pixels[:,:,0]>70)&(pixels[:,:,0]>pixels[:,:,1]*1.3))
   metadata[name].append(dict(group=group,number=index,file=str(path.relative_to(CHAR)),size=out.size,axis=axis,attack_extent=int(np.where(body)[1].max())-axis[0],source_sheet=name,source_cell=index,source_box=box,shared_scale=factor))
   records.append((group,index,path,axis));review.append((name,index,out))
 im=Image.open(SOURCE/'motion_fx.png').convert('RGBA')
 for row,(key,group) in enumerate([('foot_dust',9900),('metal_sparks',9901),('finish_edge',9902)]):
  poses=[];metadata[key]=[]
  for col in range(4):
   box=(round(im.width*col/4),[0,360,650,im.height][row],round(im.width*(col+1)/4),[0,360,650,im.height][row+1]);pic=im.crop(box)
   pic.putalpha(pic.getchannel('A').point(lambda a:255 if a>=128 else 0));bounds=pic.getbbox();assert bounds
   assert min(bounds[:2])>0 and bounds[2]<pic.width and bounds[3]<pic.height,(key,col,bounds)
   poses.append((pic.crop(bounds),box))
  factor=min(110/max(p.width for p,_ in poses),(35 if row==0 else 90)/max(p.height for p,_ in poses));axis=(64,70 if row==0 else 48)
  for i,(pic,box) in enumerate(poses):
   pic=pic.resize((max(1,round(pic.width*factor)),max(1,round(pic.height*factor))),Image.Resampling.NEAREST);out=Image.new('RGBA',(128,96));pos=(64-pic.width//2,axis[1]-pic.height if row==0 else 48-pic.height//2);assert min(pos)>=0;out.alpha_composite(pic,pos)
   folder=CHAR/'assets/sprites'/key;folder.mkdir(parents=True,exist_ok=True);path=folder/f'{i}.png';out.save(path)
   metadata[key].append(dict(group=group,number=i,file=str(path.relative_to(CHAR)),size=out.size,axis=axis,source_sheet='motion_fx',source_cell=row*4+i,source_box=box))
   records.append((group,i,path,axis));review.append((key,i,out))
 return records

def append_polish_sounds(records,manifest):
 folder=CHAR/'assets/sound';fs=22050
 def read(name):
  with wave.open(str(folder/name),'rb') as f:return np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768
 motor=read('chainsaw_long.wav');cut=read('chainsaw_cut.wav');heavy=read('impact_heavy.wav');light=read('impact_light.wav')
 for no,name,duration in [(14,'motor_rev_loop',1.2),(15,'motor_spindown',.9),(16,'serrated_finish',.6),(17,'footfall_dust',.22)]:
  t=np.arange(round(duration*fs))/fs
  if no==14:
   pos=(np.arange(len(t))*1.08+len(motor)*.2)%len(motor);out=np.interp(pos,np.arange(len(motor)),motor)*.7
   # A very short fade at the loop boundary avoids a discontinuous motor click.
   envelope=np.minimum(1,t/.012)*np.minimum(1,(duration-t)/.012);out*=envelope
  elif no==15:
   pos=fs*(t-.35*t*t/duration);out=np.interp(pos%len(motor),np.arange(len(motor)),motor)*np.power(1-t/duration,1.5)*np.minimum(1,t/.012)
  elif no==16:
   out=np.zeros(len(t))
   for sample,start,gain,rate in [(heavy,0,.75,.85),(cut,.025,.65,1),(motor,.06,.25,1.2)]:
    data=np.interp(np.arange(0,len(sample)-1,rate),np.arange(len(sample)),sample);at=round(start*fs);n=min(len(data),len(out)-at);out[at:at+n]+=gain*data[:n]
   out*=np.minimum(1,t/.004)*np.minimum(1,(duration-t)/.06)
  else:
   data=np.interp(np.arange(len(t))*.75,np.arange(len(light)),light);out=np.convolve(data,np.ones(9)/9,mode='same')*np.exp(-t*16)*.7
  peak=max(float(np.max(np.abs(out))),1e-9);rms=max(float(np.sqrt(np.mean(out*out))),1e-9);out*=min({14:.12,15:.2,16:.18,17:.08}[no]/rms,.9/peak)
  stream=io.BytesIO()
  with wave.open(stream,'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(fs);f.writeframes((out*32767).astype('<i2').tobytes())
  payload=stream.getvalue();path=folder/(name+'.wav');path.write_bytes(payload);records.append((1,no,payload));manifest.append(dict(group=1,number=no,filename=path.name,type='original nonverbal edit/mix',sources=['chainsaw_long.wav','chainsaw_cut.wav','impact_heavy.wav','impact_light.wav'],duration=duration,sha256=hashlib.sha256(payload).hexdigest(),voice=False))

def apply_polish_runtime(char):
 cns=(char/'PochitaTrueForm.cns').read_text();air=(char/'PochitaTrueForm.air').read_text();common=(char/'common1.cns').read_text()
 def anim(n,group,indices,times,loop=False,low=False):
  result=f'[Begin Action {n}]\nClsn2Default: 1\n Clsn2[0] = -17,{-44 if low else -72},17,0\n'
  if loop:result+='Loopstart\n'
  return result+''.join(f'{group},{i},0,0,{t}\n' for i,t in zip(indices,times))+'\n'
 def replace_anim(n,value):
  nonlocal air
  air,count=re.subn(rf'(?ims)^\[Begin Action {n}\].*?(?=^\[Begin Action|\Z)',lambda m:value,air,count=1);assert count,n
 def add(n,text,before=None):
  nonlocal cns
  match=re.search(rf'(?ims)^\[Statedef {n}\].*?(?=^\[Statedef|\Z)',cns);assert match,n;block=match[0]
  marker=before or f'[State {n}, End]';at=block.find(marker)
  if at<0:at=len(block)
  cns=cns[:match.start()]+block[:at]+text+'\n'+block[at:]+cns[match.end():]
 def fx(n,name,condition,animation,ident,pos='32,-38',scale='.6,.6',bind='0',priority=4,alpha=220):
  return f'''[State {n}, {name}]
type = Explod
{condition}
anim = {animation}
ID = {ident}
postype = p1
pos = {pos}
facing = 1
bindtime = {bind}
removetime = 14
scale = {scale}
sprpriority = {priority}
ownpal = 1
trans = addalpha
alpha = {alpha},256
removeongethit = 1
ignorehitpause = 1
'''
 replace_anim(500,anim(500,3500,[0,1,2,3],[5,4,5,4],True))
 replace_anim(100,anim(100,3501,[0,1,2,3],[3,3,3,3],True))
 replace_anim(52,anim(52,3501,[6,7,7],[3,3,3],low=True))
 replace_anim(180,anim(180,3500,[4,5,6,7],[14,8,26,-1]))
 air+=anim(106,3501,[4,5],[4,5])
 for group,times in [(9900,[2,3,4,5]),(9901,[2,2,3,3]),(9902,[2,2,3,3])]:air+='\n'+f'[Begin Action {group}]\n'+''.join(f'{group},{i},0,0,{t}\n' for i,t in enumerate(times))
 # The charge retains precisely 18/tick and immediate release/full-bar control.
 match=re.search(r'(?ims)^\[Statedef 500\].*?(?=^\[Statedef|\Z)',cns);block=match[0].replace('value = S1,3','value = S1,14',1).replace('volume = -160','volumescale = 75',1);cns=cns[:match.start()]+block+cns[match.end():]
 add(500,'''[State 500, Accelerate motors]
type = PlaySnd
trigger1 = Time = 0
value = S1,0
channel = 1
[State 500, Small engine vibration]
type = Offset
trigger1 = 1
x = IfElse(Time%4 < 2,-1,1)
y = 0
'''+fx(500,'Low motor embers','triggerall = NumExplod(9491) = 0\ntrigger1 = Time%12 = 0',9901,9491,'22,-28','.3,.3','0',3,170)+fx(500,'Boot pressure dust','triggerall = NumExplod(9490) < 2\ntrigger1 = Time%22 = 0',9900,9490,'0,0','.7,.6','0',-1,160),before='[State 500, Power]')
 # Stop the charge channel globally as before; add a short one-shot deceleration.
 passive='''[State -2, Restore drawing offset outside charge]
type = Offset
trigger1 = StateNo != 500
x = 0
y = 0
ignorehitpause = 1
[State -2, Charge exit motor deceleration]
type = PlaySnd
triggerall = PrevStateNo = 500
triggerall = StateNo != 500
trigger1 = Time = 1
value = S1,15
channel = 2
volumescale = 70
[State -2, Clear charge embers after release or injury]
type = RemoveExplod
trigger1 = StateNo != 500
trigger2 = MoveType = H
ID = 9491
ignorehitpause = 1
'''
 passive+=fx(-2,'Footwork dust','triggerall = RoundState = 2\ntriggerall = NumExplod(9490) < 2\ntrigger1 = StateNo = 100\ntrigger1 = Time%10 = 0\ntrigger2 = StateNo = 20\ntrigger2 = Time%18 = 0\ntrigger3 = StateNo = 52\ntrigger3 = Time <= 1\ntrigger4 = StateNo = 106\ntrigger4 = Time = 1',9900,9490,'0,0','.65,.65','0',-1,170)
 passive+='''[State -2, Grounded footstep]
type = PlaySnd
triggerall = RoundState = 2
trigger1 = StateNo = 100
trigger1 = Time%12 = 0
trigger2 = StateNo = 52
trigger2 = Time <= 1
trigger3 = StateNo = 106
trigger3 = Time = 1
value = S1,17
channel = 7
volumescale = 45
'''
 cns=cns.replace('[Statedef -2]','[Statedef -2]\n'+passive,1)
 # A cancellable braking pose adds no travel, lockout or new input mapping.
 common,count=re.subn(r'(?ims)(\[State 100, Stop\].*?value = )0',r'\g<1>106',common,count=1);assert count
 cns+='''\n[Statedef 106]
type = S
movetype = I
physics = S
anim = 106
ctrl = 1
velset = 0,0
[State 106, End braking pose]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1
'''
 # Add readable paths without extending any hitbox or changing hit damage.
 states=[200,201,202,210,211,212,220,221,222,400,410,420,600,610,620,660,661,662,670,671,672,1000,1010,1020,1030,1040,1050,1060,1070,1080,1100,1401]
 finishers=[202,212,222,670,671,672,1000,1010,1030,1040,1060,1070,1100]
 for n in states:
  m=re.search(rf'(?ims)^\[Statedef {n}\].*?(?=^\[Statedef|\Z)',cns);block=m[0]
  hits=re.findall(r'(?ims)^\[State[^\]]+\]\ntype = HitDef\n(.*?)(?=^\[State|\Z)',block);elements=[int(re.search(r'AnimElem = (\d+)',h)[1]) for h in hits]
  if not elements:continue
  action=re.search(rf'(?ims)^\[Begin Action {n}\].*?(?=^\[Begin Action|\Z)',air)[0]
  durations=[int(x) for x in re.findall(r'(?m)^\d+,\d+,-?\d+,-?\d+,(-?\d+)',action)]
  first_time=sum(durations[:elements[0]-1]);last_time=sum(durations[:elements[-1]-1]);low=n in [400,410,420,1040,1080]
  reset=''
  for variable in [12,14,15]:reset+=f'[State {n}, Reset presentation latch {variable}]\ntype = VarSet\ntrigger1 = Time = 0\nv = {variable}\nvalue = 0\nignorehitpause = 1\n'
  first_header=re.search(r'(?m)^\[State[^\]]+\]',block)[0];add(n,reset,first_header)
  condition='triggerall = NumExplod(9493) < 2\n'+'\n'.join(f'trigger{i} = AnimElem = {e}' for i,e in enumerate(elements,1))
  add(n,fx(n,'Visible serrated blade path',condition,9902,9493,'28,-18' if low else '30,-42','.42,.32' if low else '.5,.5','0',3,145))
  condition=f'triggerall = Time >= {first_time}\ntriggerall = MoveHit\ntriggerall = NumExplod(9492) < 2\ntrigger1 = HitCount > Var(14)'
  add(n,fx(n,'Metal contact sparks',condition,9901,9492,'36,-18' if low else '38,-40','.48,.48')+f'''[State {n}, Latch metal contact]
type = VarSet
{condition}
v = 14
value = HitCount
ignorehitpause = 1
''')
  condition=f'triggerall = Time >= {first_time}\ntriggerall = MoveGuarded\ntrigger1 = Var(12) = 0'
  add(n,fx(n,'Guard sparks without blood',condition,9901,9492,'36,-18' if low else '38,-40','.35,.35',alpha=170)+f'''[State {n}, Latch guard contact]
type = VarSet
{condition}
v = 12
value = 1
ignorehitpause = 1
''')
  if n in finishers:
   last=elements[-1];m=re.search(rf'(?ims)^\[Statedef {n}\].*?(?=^\[Statedef|\Z)',cns);block=m[0]
   parts=re.split(r'(?im)(?=^\[State )',block)
   for i,part in enumerate(parts):
    if 'type = HitDef\n' in part and f'AnimElem = {last}\n' in part:
     parts[i]=re.sub(r'(?m)^pausetime = (\d+),(\d+)',lambda x:f'pausetime = {int(x[1])+2},{int(x[2])+2}',part)
   cns=cns[:m.start()]+''.join(parts)+cns[m.end():]
   if n not in [1000,1010,1030,1040,1060,1070,1100]:
    condition=f'triggerall = Time >= {last_time}\ntriggerall = MoveHit\ntriggerall = HitCount >= {len(elements)}\ntrigger1 = Var(15) = 0'
    add(n,fx(n,'Confirmed final edge',condition,9902,9494,'40,-18' if low else '42,-38','.8,.65','0',5,235)+f'''[State {n}, Finisher weight]
type = PlaySnd
{condition}
value = S1,16
channel = 5
volumescale = 70
ignorehitpause = 1
[State {n}, Latch final presentation]
type = VarSet
{condition}
v = 15
value = 1
ignorehitpause = 1
''')
 # Character-owned sparks replace the engine's generic colored hit burst.
 cns=re.sub(r'(?m)^sparkno = 1$','sparkno = -1',cns)
 # Tint body afterimages charcoal/red instead of the engine's default ghost hue.
 def tint_afterimage(match):
  block=match[0]
  for key,value in [('palcolor','256'),('palbright','20,-30,-30'),('palcontrast','200,140,140'),('paladd','10,0,0'),('palmul','.75,.45,.45')]:
   pattern=rf'(?im)^{key} = [^\n]*'
   if re.search(pattern,block):block=re.sub(pattern,key+' = '+value,block)
   else:block+=key+' = '+value+'\n'
  block=re.sub(r'(?m)^trans = [^\n]*','trans = none',block)
  return block
 cns=re.sub(r'(?ims)^\[State[^\]]+\]\ntype = AfterImage\n.*?(?=^\[State|\Z)',tint_afterimage,cns)
 # Real win state: new poses and sound, no combat effects on a loss or draw.
 m=re.search(r'(?ims)^\[Statedef 180\].*?(?=^\[Statedef|\Z)',cns);assert m
 win='''[Statedef 180]
type = S
movetype = I
physics = S
anim = 180
ctrl = 0
velset = 0,0
[State 180, Keep winner within view]
type = ScreenBound
trigger1 = 1
value = 1
movecamera = 1,0
[State 180, Left victory margin]
type = PosAdd
trigger1 = BackEdgeBodyDist < 54
x = 54-BackEdgeBodyDist
[State 180, Right victory margin]
type = PosAdd
trigger1 = FrontEdgeBodyDist < 54
x = -(54-FrontEdgeBodyDist)
[State 180, Let victory sequence finish]
type = AssertSpecial
trigger1 = Time < 110
flag = RoundNotOver
flag2 = NoKOSlow
[State 180, Victory rev]
type = PlaySnd
trigger1 = Time = 0
value = S1,0
channel = 1
volumescale = 65
[State 180, Shake saws clean]
type = PlaySnd
trigger1 = Time = 14
value = S1,8
channel = 1
volumescale = 65
[State 180, Motors wind down]
type = PlaySnd
trigger1 = Time = 38
value = S1,15
channel = 1
volumescale = 80
[State 180, Dim stage for victory]
type = BGPalFX
trigger1 = Time = 0
time = 90
add = -25,-25,-25
mul = 225,225,225
'''+fx(180,'Blood shaken off saws','trigger1 = Time = 14',9201,9495,'28,-24','.35,.35','0',3,200)
 cns=cns[:m.start()]+win+'\n'+cns[m.end():]
 (char/'PochitaTrueForm.cns').write_text(cns.rstrip()+'\n');(char/'PochitaTrueForm.air').write_text(air.rstrip()+'\n');(char/'common1.cns').write_text(common.rstrip()+'\n')
 print('Integrated rev poses, scarf run/brake/landing, finite saw contacts and a real victory sequence')
