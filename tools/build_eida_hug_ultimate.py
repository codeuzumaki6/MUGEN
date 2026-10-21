#!/usr/bin/env python3
"""Stage the Kawaki embrace as game sprites; never repaint manga panels."""
from pathlib import Path
import json,re
from PIL import Image
import numpy as np
from scipy.ndimage import label,find_objects
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Eida'

def install():
    sheet=Image.open(ROOT/'design/Eida_omnipotencia/embrace_sheet.png').convert('RGBA')
    folder=CHAR/'assets/omni_hug';folder.mkdir(parents=True,exist_ok=True)
    # Hair crosses nominal grid lines. Isolate connected figures instead of
    # clipping their silhouettes at cell edges. Pose zero has two figures.
    labels,_=label(np.array(sheet.getchannel('A'))>=128,np.ones((3,3)))
    objects=find_objects(labels);areas=np.bincount(labels.ravel());groups={i:[] for i in range(8)}
    for j,obj in enumerate(objects,1):
        if areas[j]<1000:continue
        row=int((obj[0].start+obj[0].stop)/2)//(sheet.height//4)
        col=int((obj[1].start+obj[1].stop)/2)//(sheet.width//2)
        groups[row*2+col].append(j)
    crops=[]
    for i in range(8):
        assert groups[i],i
        alpha=Image.fromarray(np.isin(labels,groups[i]).astype('uint8')*255);box=alpha.getbbox();assert box
        assert min(box[:2])>0 and box[2]<sheet.width and box[3]<sheet.height,(i,box)
        pic=sheet.copy();pic.putalpha(alpha);crops.append((pic.crop(box),box))
    # Retain facial detail for the cinematic close-up. These sprites are
    # displayed at a controlled screen size, never used for Eida's combat body.
    factor=180/crops[3][0].height;manifest=[]
    for i,(pic,box) in enumerate(crops):
        pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
        feet=pic.getchannel('A').crop((0,pic.height-5,pic.width,pic.height)).getbbox();assert feet
        x=round(160-(feet[0]+feet[2])/2);y=216-pic.height;assert x>=0 and y>=0 and x+pic.width<320
        canvas=Image.new('RGBA',(320,224));canvas.alpha_composite(pic,(x,y));path=folder/f'embrace_{i}.png';canvas.save(path)
        manifest.append(dict(group=8600,number=i,file=str(path.relative_to(CHAR)),axis=[160,216],source_box=box,shared_scale=factor))
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    airpath=CHAR/'Eida.air';air=airpath.read_text()
    sequence=list(zip([0,1,2],[10,10,12]))
    for _ in range(6):sequence+=list(zip([3,4,5,6,7],[10,8,8,10,10]))
    sequence+=list(zip([6,5,6,7],[12,12,12,74]))
    action='[Begin Action 8600]\n'+''.join(f'8600,{i},0,0,{ticks}\n' for i,ticks in sequence)+'\n'
    pattern=r'(?ims)^\[Begin Action 8600\].*?(?=^\[Begin Action|\Z)'
    air=re.sub(pattern,lambda _:action,air,count=1) if re.search(pattern,air) else air.rstrip()+'\n\n'+action
    airpath.write_text(air.rstrip()+'\n')
    path=CHAR/'Omnipotencia.cns';text=path.read_text()
    scene='''[Statedef 3001]
type = S
movetype = A
physics = N
anim = 3000
ctrl = 0
velset = 0,0
[State 3001, Freeze confirmed scene only]
type = Pause
trigger1 = Time = 0
time = 430
movetime = 430
pausebg = 1
endcmdbuftime = 0
[State 3001, Protect the confirmed scene]
type = NotHitBy
trigger1 = 1
value = SCA
time = 1
[State 3001, Quiet cinematic interface]
type = AssertSpecial
trigger1 = Time < 440
flag = NoBarDisplay
flag2 = NoFG
flag3 = NoMusic
[State 3001, Authentic Japanese Eida voice]
type = PlaySnd
trigger1 = Time = 0
value = S0,2
channel = 0
[State 3001, Memory sound bed]
type = PlaySnd
trigger1 = Time = 3
value = S1,11
channel = 5
[State 3001, Black cinematic backdrop]
type = Explod
trigger1 = Time = 8
anim = 8090
ID = 8090
space = Screen
postype = Left
pos = 0,0
bindtime = -1
scale = GameWidth/1280.0,GameHeight/720.0
removetime = 429
sprpriority = 19
ownpal = 1
pausemovetime = 999
supermovetime = 999
[State 3001, Original manga world behind embrace]
type = Explod
trigger1 = Time = 12
anim = 8001
ID = 8611
space = Screen
postype = Left
pos = 0,(GameHeight-GameWidth*9.0/16.0)/2.0
scale = GameWidth/1280.0,GameWidth/1280.0
bindtime = -1
removetime = 425
sprpriority = 20
ownpal = 1
pausemovetime = 999
supermovetime = 999
trans = AddAlpha
alpha = 56,200
[State 3001, Original world becomes visible]
type = ModifyExplod
trigger1 = Time = [12,431]
ID = 8611
trans = AddAlpha
alpha = 48+IfElse(Time<340,Time/8,42),208-IfElse(Time<340,Time/8,42)
[State 3001, Eida cradles Kawaki animated sprites]
type = Explod
trigger1 = Time = 12
anim = 8600
ID = 8600
space = Screen
postype = Left
pos = GameWidth*.5,GameHeight*.91
facing = 1
vfacing = 1
bindtime = -1
scale = GameHeight/180.0*.566667,GameHeight/180.0*.566667
removetime = 425
sprpriority = 23
ownpal = 1
pausemovetime = 999
supermovetime = 999
trans = AddAlpha
alpha = 0,256
[State 3001, Smooth approach to the embrace]
type = ModifyExplod
trigger1 = Time = [12,431]
ID = 8600
pos = GameWidth*.5,GameHeight*.91
scale = GameHeight/180.0*(.566667+Time*.00008311),GameHeight/180.0*(.566667+Time*.00008311)
trans = AddAlpha
alpha = IfElse((Time-12)*24<256,(Time-12)*24,256),256-IfElse((Time-12)*24<256,(Time-12)*24,256)
[State 3001, Embrace sound accent]
type = PlaySnd
trigger1 = Time = 44
value = S1,12
channel = 6
[State 3001, Senrigan pulse over the pair]
type = Explod
trigger1 = Time = 80
trigger2 = Time = 180
trigger3 = Time = 280
trigger4 = Time = 380
anim = 8520
ID = 8620
space = Screen
postype = Left
pos = GameWidth*.5,GameHeight*.4
scale = GameHeight/180.0*.75,GameHeight/180.0*.75
bindtime = -1
removetime = 14
sprpriority = 24
ownpal = 1
pausemovetime = 999
supermovetime = 999
trans = AddAlpha
alpha = 150,256
[State 3001, Memory change accents]
type = PlaySnd
trigger1 = Time = 180
trigger2 = Time = 280
trigger3 = Time = 380
value = S1,12
channel = 6
[State 3001, Omnipotence release flash]
type = EnvColor
trigger1 = Time = 432
value = 245,248,255
time = 5
under = 0
[State 3001, Clear the cinematic]
type = RemoveExplod
trigger1 = Time = 437
[State 3001, Release sound]
type = PlaySnd
trigger1 = Time = 435
value = S1,13
channel = 6
[State 3001, Confirmed finite damage]
type = TargetLifeAdd
trigger1 = Time = 436
trigger1 = NumTarget(3000) > 0
ID = 3000
value = -350
kill = 1
absolute = 1
[State 3001, Release victim]
type = TargetState
trigger1 = Time = 438
trigger1 = NumTarget(3000) > 0
ID = 3000
value = 3011
[State 3001, Release impact]
type = EnvShake
trigger1 = Time = 438
time = 12
freq = 80
ampl = -3
[State 3001, Recovery]
type = ChangeState
trigger1 = Time >= 462
value = 0
ctrl = 1

'''
    text,count=re.subn(r'(?ims)^\[Statedef 3001\].*?(?=^\[Statedef|\Z)',lambda _:scene,text,count=1);assert count
    # Use the same unmistakable activation SE for A's existing ten-tick focus.
    text=text.replace('[State 3000, Telegraph sound]\ntype = PlaySnd\ntrigger1 = Time = 2\nvalue = S1,10','[State 3000, Telegraph sound]\ntype = PlaySnd\ntrigger1 = Time = 2\nvalue = S1,21\nchannel = 4\nvolumescale = 100')
    path.write_text(text)
    print('Installed eight paired embrace poses; original manga/voice and missable 350-damage opener retained')

if __name__=='__main__':install()
