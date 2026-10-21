#!/usr/bin/env python3
"""Use the user's exact two hug poses, at native scale, within the stage."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Eida'

def install():
    source=ROOT/'design/Eida_omnipotencia/original/Eida_sprites_en_captura.png'
    sheet=Image.open(source).convert('RGBA')
    folder=CHAR/'assets/omni_hug';folder.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for i,box in enumerate([(8,624,64,709),(66,622,118,707)]):
        pic=sheet.crop(box);pixels=np.array(pic)
        r,g,b=[pixels[:,:,j].astype(float) for j in range(3)]
        green=(g>55)&(g>r*1.38)&(g>b*1.18)
        pixels[green,3]=0
        pic=Image.fromarray(pixels);bounds=pic.getbbox();assert bounds
        assert min(bounds[:2])>0 and bounds[2]<pic.width and bounds[3]<pic.height,(i,bounds)
        pic=pic.crop(bounds)
        # No resizing, repainting, color replacement or invented poses.
        feet=pic.getchannel('A').crop((0,pic.height-5,pic.width,pic.height)).getbbox();assert feet
        x=round(48-(feet[0]+feet[2])/2);y=86-pic.height
        assert x>=0 and y>=0 and x+pic.width<96
        canvas=Image.new('RGBA',(96,88));canvas.alpha_composite(pic,(x,y));path=folder/f'embrace_{i}.png';canvas.save(path)
        manifest.append(dict(group=8600,number=i,file=str(path.relative_to(CHAR)),axis=[48,86],source_box=box,trim_box=bounds,native_scale=1,ai_redrawn=False,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source='User reference ZIP, Sheet Eida by Vaydra',processing='Green background alpha key only; all visible RGB pixels preserved'))
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    airpath=CHAR/'Eida.air';air=airpath.read_text()
    sequence=list(zip([0,1,0,1,0,1,0,1,1],[8,8,8,8,8,8,8,8,34]))
    action='[Begin Action 8600]\n'+''.join(f'8600,{i},0,0,{ticks}\n' for i,ticks in sequence)+'\n'
    pattern=r'(?ims)^\[Begin Action 8600\].*?(?=^\[Begin Action|\Z)'
    air=re.sub(pattern,lambda _:action,air,count=1) if re.search(pattern,air) else air.rstrip()+'\n\n'+action
    airpath.write_text(air.rstrip()+'\n')
    path=CHAR/'Omnipotencia.cns';text=path.read_text()
    scene='''[Statedef 3001]
type = S
movetype = A
physics = N
anim = 1100
ctrl = 0
velset = 0,0
[State 3001, Freeze confirmed scene only]
type = Pause
trigger1 = Time = 0
time = 130
movetime = 130
pausebg = 1
endcmdbuftime = 0
[State 3001, Protect the confirmed scene]
type = NotHitBy
trigger1 = 1
value = SCA
time = 1
[State 3001, Keep foreground clear during the compact scene]
type = AssertSpecial
trigger1 = Time < 130
flag = NoFG
flag2 = NoMusic
[State 3001, Replace Eida with her original paired pose briefly]
type = AssertSpecial
trigger1 = Time = [12,109]
flag = Invisible
[State 3001, Authentic Japanese Eida voice]
type = PlaySnd
trigger1 = Time = 0
value = S0,2
channel = 0
[State 3001, Stage stays visible at natural combat scale]
type = BGPalFX
trigger1 = Time = 0
time = 130
mul = 165,180,205
[State 3001, Original two-frame hug beside the fighter]
type = Explod
trigger1 = Time = 12
anim = 8600
ID = 8600
postype = P1
pos = 0,0
facing = 1
vfacing = 1
bindtime = -1
scale = 1,1
removetime = 98
sprpriority = 3
ownpal = 1
pausemovetime = 999
supermovetime = 999
[State 3001, Brief arrival of the original hug]
type = ModifyExplod
trigger1 = Time = [12,17]
ID = 8600
trans = AddAlpha
alpha = IfElse((Time-12)*64<256,(Time-12)*64,256),256-IfElse((Time-12)*64<256,(Time-12)*64,256)
[State 3001, Embrace sound accent]
type = PlaySnd
trigger1 = Time = 28
value = S1,12
channel = 6
[State 3001, Small eye cue during the embrace]
type = Explod
trigger1 = Time = 34
trigger2 = Time = 66
anim = 8520
ID = 8620
postype = P1
pos = -5,-54
scale = .35,.35
bindtime = -1
removetime = 14
sprpriority = 5
ownpal = 1
pausemovetime = 999
supermovetime = 999
trans = AddAlpha
alpha = 150,256
[State 3001, Memory change accents]
type = PlaySnd
trigger1 = Time = 66
value = S1,18
channel = 6
[State 3001, Omnipotence release burst]
type = Explod
trigger1 = Time = 106
anim = 8510
ID = 8621
postype = P1
pos = 0,-38
scale = 1.1,.9
removetime = 14
sprpriority = 6
ownpal = 1
pausemovetime = 999
supermovetime = 999
trans = AddAlpha
alpha = 230,256
[State 3001, Omnipotence release flash]
type = EnvColor
trigger1 = Time = 108
value = 245,248,255
time = 3
under = 0
[State 3001, Clear the cinematic]
type = RemoveExplod
trigger1 = Time = 130
[State 3001, Release sound]
type = PlaySnd
trigger1 = Time = 106
value = S1,13
channel = 6
[State 3001, Confirmed finite damage]
type = TargetLifeAdd
trigger1 = Time = 122
trigger1 = NumTarget(3000) > 0
ID = 3000
value = -350
kill = 1
absolute = 1
[State 3001, Release victim]
type = TargetState
trigger1 = Time = 126
trigger1 = NumTarget(3000) > 0
ID = 3000
value = 3011
[State 3001, Release impact]
type = EnvShake
trigger1 = Time = 106
time = 6
freq = 80
ampl = -1
[State 3001, Recovery]
type = ChangeState
trigger1 = Time >= 160
value = 0
ctrl = 1

'''
    text,count=re.subn(r'(?ims)^\[Statedef 3001\].*?(?=^\[Statedef|\Z)',lambda _:scene,text,count=1);assert count
    # Use the same unmistakable activation SE for A's existing ten-tick focus.
    text=text.replace('[State 3000, Telegraph sound]\ntype = PlaySnd\ntrigger1 = Time = 2\nvalue = S1,10','[State 3000, Telegraph sound]\ntype = PlaySnd\ntrigger1 = Time = 2\nvalue = S1,21\nchannel = 4\nvolumescale = 100')
    path.write_text(text)
    print('Installed the two original hug poses at scale 1; compact 160-tick scene, 350 damage and evadible opener')

if __name__=='__main__':install()
