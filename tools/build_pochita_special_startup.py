#!/usr/bin/env python3
"""Special startup presentation inspired by the user's Goku recording."""
from pathlib import Path
import hashlib,io,json,re,subprocess,wave
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'design/Pochita_especiales';CHAR=ROOT/'PochitaTrueForm'
SPECIALS={1000:(250,3100,1),1010:(350,3100,2),1030:(350,3100,3),1040:(250,3200,0),1060:(500,3200,4),1070:(750,3100,0)}

def append_startup_assets(metadata,review):
 im=Image.open(SOURCE/'activation_fx.png').convert('RGBA');records=[]
 for row,(name,group,factor,size,axis) in enumerate([('startup_flash',9300,.27,(144,84),(72,42)),('startup_ring',9301,.22,(128,120),(64,60))]):
  metadata[name]=[];folder=CHAR/'assets/sprites'/name;folder.mkdir(parents=True,exist_ok=True)
  for i in range(4):
   # The flare grows left of its nominal cell; use inspected transparent
   # gutters, rather than clipping it or including pixels of the next frame.
   xs=[0,375 if row==0 else 450,900,1340,im.width]
   box=(xs[i],round(im.height*row/2),xs[i+1],round(im.height*(row+1)/2))
   pic=im.crop(box);pic.putalpha(pic.getchannel('A').point(lambda v:255 if v>=128 else 0));bbox=pic.getchannel('A').getbbox();assert bbox
   assert bbox[0]>1 and bbox[1]>1 and bbox[2]<pic.width-1 and bbox[3]<pic.height-1,(name,i,bbox)
   pic=pic.crop(bbox);pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
   out=Image.new('RGBA',size);pos=(axis[0]-pic.width//2,axis[1]-pic.height//2);assert pos[0]>=0 and pos[1]>=0 and pos[0]+pic.width<=size[0] and pos[1]+pic.height<=size[1]
   out.alpha_composite(pic,pos);path=folder/f'{i}.png';out.save(path)
   metadata[name].append(dict(group=group,number=i,file=str(path.relative_to(CHAR)),size=size,axis=axis,source_sheet='activation_fx',source_cell=row*4+i,source_box=box))
   records.append((group,i,path,axis));review.append((name,i,out))
 return records

def append_startup_sound(records,manifest):
 # The supplied Code uses 950,2 as "PlaySnd - Super Charge". Convert the
 # original nonverbal SE instead of lifting a mixed music/voice video excerpt.
 original=SOURCE/'Code_950_2_original.wav';path=CHAR/'assets/sound/special_activation.wav'
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(original),'-ac','1','-ar','22050','-c:a','pcm_s16le',str(path)],check=True)
 with wave.open(str(path),'rb') as wav:
  samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)/32768
 rms=float(np.sqrt(np.mean(samples*samples)));samples*=min(.18/max(rms,1e-12),.92/max(float(np.max(np.abs(samples))),1e-12))
 with wave.open(str(path),'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(22050);wav.writeframes((samples*32767).astype('<i2').tobytes())
 payload=path.read_bytes();records.append((1,10,payload));manifest.append(dict(group=1,number=10,filename=path.name,source_character='Code_FUNCIONAL supplied by user',source_group=950,source_number=2,source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),duration=len(samples)/22050,voice=False,note='Nonverbal Super Charge SE; level adjusted, not extracted from Goku video'))

def apply_startup_runtime(char):
 cns=(char/'PochitaTrueForm.cns').read_text();cmd=(char/'PochitaTrueForm.cmd').read_text();air=(char/'PochitaTrueForm.air').read_text()
 for group,times in [(9300,[2,4,3,3]),(9301,[3,4,4,4])]:
  air+=f'\n[Begin Action {group}]\n'+''.join(f'{group},{i},0,0,{t}\n' for i,t in enumerate(times))
 for state,(cost,group,pose) in SPECIALS.items():
  startup=state+10000
  cmd=re.sub(rf'(?m)^value = {state}\s*$',f'value = {startup}',cmd)
  match=re.search(rf'(?is)\[Statedef {state}\].*?(?=\[Statedef|\Z)',cns);assert match
  block=match[0];assert f'poweradd = -{cost}' in block;block=block.replace(f'poweradd = -{cost}','poweradd = 0',1)
  block+=f'''[State {state}, Saw ground pulse]
type = Explod
trigger1 = Time = 0
anim = 9301
ID = 9451
postype = p1
pos = 0,-6
bindtime = 0
removetime = 15
scale = .75,.25
sprpriority = -1
ownpal = 1
removeongethit = 1
ignorehitpause = 1
persistent = 0
'''
  cns=cns[:match.start()]+block+cns[match.end():]
  air+=f'\n[Begin Action {startup}]\nClsn2Default: 1\n Clsn2[0] = -17,-72,17,0\n{group},{pose},0,0,12\n'
  cns+=f'''\n[Statedef {startup}]
type = S
movetype = I
physics = S
anim = {startup}
ctrl = 0
velset = 0,0
poweradd = -{cost}
[State {startup}, Activation SE]
type = PlaySnd
trigger1 = Time = 0
value = S1,10
channel = 4
volumescale = 100
persistent = 0
ignorehitpause = 1
[State {startup}, Special focus]
type = SuperPause
trigger1 = Time = 0
time = IfElse(Var(32) > 0,6,12)
movetime = IfElse(Var(32) > 0,6,12)
anim = -1
sound = -1
darken = 1
unhittable = 0
p2defmul = 1
poweradd = 0
persistent = 0
ignorehitpause = 1
[State {startup}, Horizontal activation flash]
type = Explod
trigger1 = Time = 0
anim = 9300
ID = 9450
postype = p1
pos = 26,-48
facing = 1
bindtime = -1
removetime = 12
scale = .85,.85
sprpriority = 6
ownpal = 1
supermovetime = 16
pausemovetime = 16
removeongethit = 1
persistent = 0
ignorehitpause = 1
[State {startup}, Release blades]
type = ChangeState
trigger1 = Time >= IfElse(Var(32) > 0,6,12)
value = {state}
ctrl = 0
'''
 (char/'PochitaTrueForm.cns').write_text(cns.rstrip()+'\n');(char/'PochitaTrueForm.cmd').write_text(cmd.rstrip()+'\n');(char/'PochitaTrueForm.air').write_text(air.rstrip()+'\n')
 print('Integrated six metered special startups with independent activation audio and finite effects')
