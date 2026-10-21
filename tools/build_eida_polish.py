#!/usr/bin/env python3
"""Import reviewed body/FX sheets and install repeatable Eida presentation.

Only presentation changes: the established costs, damage, collisions, controls,
voices, awakening body and original manga panels are retained.
"""
from pathlib import Path
import hashlib, json, re, wave
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects
from build_eida_activation import remove_activation, install as install_activation

ROOT = Path(__file__).resolve().parents[1]
CHAR = ROOT/'Eida'
SOURCE = ROOT/'design/Eida_acabado'
ASSETS = CHAR/'assets/polish'


def import_art():
    ASSETS.mkdir(parents=True, exist_ok=True)
    manifest = []
    shared_scale = None
    for name, group in [('charge_victory',350),('locomotion',351)]:
        im = Image.open(SOURCE/(name+'.png')).convert('RGBA')
        mask = np.array(im.getchannel('A')) >= 128
        labels, _ = label(mask, np.ones((3,3)))
        objects = find_objects(labels); areas = np.bincount(labels.ravel())
        bodies = [i+1 for i,s in enumerate(objects) if areas[i+1] > 2000]
        bodies.sort(key=lambda i:(int((objects[i-1][0].start+objects[i-1][0].stop)/2)//(im.height//4),objects[i-1][1].start))
        assert len(bodies) == 8, (name,len(bodies))
        crops = []
        for body in bodies:
            obj = objects[body-1]; members = [body]
            for j,s in enumerate(objects,1):
                if j in bodies: continue
                y=(s[0].start+s[0].stop)/2; x=(s[1].start+s[1].stop)/2
                if obj[0].start-6 <= y <= obj[0].stop+6 and obj[1].start-6 <= x <= obj[1].stop+6: members.append(j)
            alpha = Image.fromarray(np.isin(labels,members).astype('uint8')*255)
            box = alpha.getbbox()
            assert box and min(box[:2])>0 and box[2]<im.width and box[3]<im.height, (name,box)
            pic=im.copy();pic.putalpha(alpha);crops.append((pic.crop(box),box))
        # A relaxed standing pose calibrates both sheets. Crouches stay lower;
        # never stretch each frame independently to the same height.
        scale = 68/crops[7 if name=='charge_victory' else 5][0].height
        for i,(pic,box) in enumerate(crops):
            pic=pic.resize((round(pic.width*scale),round(pic.height*scale)),Image.Resampling.NEAREST)
            feet=pic.getchannel('A').crop((0,pic.height-4,pic.width,pic.height)).getbbox();assert feet
            anchor=(feet[0]+feet[2])/2
            out=Image.new('RGBA',(128,80));x=round(64-anchor);y=78-pic.height
            assert x>=0 and y>=0 and x+pic.width<128,(name,i,pic.size)
            out.alpha_composite(pic,(x,y));path=ASSETS/f'{group}_{i}.png';out.save(path)
            manifest.append(dict(group=group,number=i,file=str(path.relative_to(CHAR)),axis=[64,78],source=name,source_box=box,scale=scale,opaque_box=out.getbbox()))
    im=Image.open(SOURCE/'motion_fx.png').convert('RGBA')
    for row,group in enumerate([8500,8510,8520]):
        poses=[]
        for col in range(4):
            box=(im.width*col//4,im.height*row//3,im.width*(col+1)//4,im.height*(row+1)//3)
            pic=im.crop(box);pic.putalpha(pic.getchannel('A').point(lambda a:255 if a>=128 else 0));bounds=pic.getbbox();assert bounds
            assert min(bounds[:2])>0 and bounds[2]<pic.width and bounds[3]<pic.height,(group,col,bounds)
            poses.append((pic.crop(bounds),box))
        scale=min(90/max(p.width for p,_ in poses),(24 if row==0 else 70)/max(p.height for p,_ in poses))
        for i,(pic,box) in enumerate(poses):
            pic=pic.resize((max(1,round(pic.width*scale)),max(1,round(pic.height*scale))),Image.Resampling.NEAREST)
            out=Image.new('RGBA',(128,96));axis=[64,94] if row==0 else [64,48]
            out.alpha_composite(pic,(64-pic.width//2,axis[1]-pic.height if row==0 else 48-pic.height//2))
            path=ASSETS/f'{group}_{i}.png';out.save(path)
            manifest.append(dict(group=group,number=i,file=str(path.relative_to(CHAR)),axis=axis,source='motion_fx',source_box=box,scale=scale))
    (ASSETS/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')


def make_sounds():
    fs=22050;rng=np.random.default_rng(18432);manifest=[]
    for number,name,duration in [(17,'senrigan_charge_loop',1.2),(18,'senrigan_release',.42),(19,'daemon_impact_finish',.36),(20,'soft_footfall',.18)]:
        t=np.arange(round(fs*duration))/fs;p=t/duration
        noise=np.convolve(rng.uniform(-1,1,len(t)),np.ones(9)/9,mode='same')
        if number==17:
            out=(.42*np.sin(2*np.pi*220*t)+.2*np.sin(2*np.pi*330*t)+.16*noise)*(.7+.3*np.sin(np.pi*p)**2)
            out*=np.minimum(1,t/.015)*np.minimum(1,(duration-t)/.015)
        elif number==18:
            out=(.45*np.sin(2*np.pi*(480*t-210*t*t))+.25*noise)*np.sin(np.pi*p)*np.exp(-3*p)
        elif number==19:
            out=(.5*np.sin(2*np.pi*(110*t-75*t*t))+.75*noise)*np.exp(-18*t)*np.minimum(1,t/.003)
        else:out=noise*np.exp(-32*t)*np.minimum(1,t/.003)
        out*=min({17:.08,18:.12,19:.19,20:.075}[number]/max(np.sqrt(np.mean(out*out)),1e-9),.85/max(abs(out)))
        path=CHAR/'assets/sound'/f'{name}.wav'
        with wave.open(str(path),'wb') as f:f.setparams((1,2,fs,0,'NONE','not compressed'));f.writeframes((out*32767).astype('<i2').tobytes())
        manifest.append(dict(group=1,number=number,file=path.name,duration=duration,voice=False,source='Original nonverbal oscillators and filtered noise',sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (ASSETS/'sounds.json').write_text(json.dumps(manifest,indent=2)+'\n')


def apply_runtime():
    paths={name:CHAR/name for name in ['Eida.cns','Specials.cns','Eida.air']}
    texts={name:re.sub(r'(?ms)^; EIDA POLISH BEGIN.*?^; EIDA POLISH END\n?','',remove_activation(p.read_text())).rstrip()+'\n' for name,p in paths.items()}
    # State 106 is owned by this module. Keep it outside controller markers:
    # the preceding state's end must never swallow another marker's opening.
    texts['Eida.cns']=re.sub(r'(?ims)^\[Statedef 106\].*?(?=^\[Statedef|\Z)','',texts['Eida.cns'])
    texts['Eida.cns']=re.sub(r'(?m)^; EIDA POLISH END\n?','',texts['Eida.cns'])
    texts['Eida.cns']=texts['Eida.cns'].rstrip()+'\n'
    def marked(text):return '; EIDA POLISH BEGIN\n'+text.rstrip()+'\n; EIDA POLISH END\n'
    def add(file,state,text,first=False):
        source=texts[file];m=re.search(rf'(?ims)^\[Statedef {state}\].*?(?=^\[Statedef|\Z)',source);assert m,(file,state)
        block=m[0];at=re.search(r'(?m)^\[State ',block).start() if first else len(block)
        texts[file]=source[:m.start()]+block[:at]+marked(text)+block[at:]+source[m.end():]
    def action(n,group,indices,times,loop=False):
        header=f'[Begin Action {n}]\n'
        if group<1000:header+='Clsn2Default: 1\n Clsn2[0] = -15,-70,15,0\n'
        if loop:header+='Loopstart\n'
        value=header+''.join(f'{group},{i},0,0,{t}\n' for i,t in zip(indices,times))+'\n'
        air=texts['Eida.air'];pattern=rf'(?ims)^\[Begin Action {n}\].*?(?=^\[Begin Action|\Z)'
        texts['Eida.air']=re.sub(pattern,lambda m:value,air,count=1) if re.search(pattern,air) else air+'\n'+value
    def fx(state,label,condition,anim,ident,pos,scale='.6,.6',bind=0,priority=4):
        return f'''[State {state}, {label}]
type = Explod
{condition}
anim = {anim}
ID = {ident}
postype = P1
pos = {pos}
bindtime = {bind}
removetime = 14
scale = {scale}
sprpriority = {priority}
ownpal = 1
trans = addalpha
alpha = 210,256
removeongethit = 1
ignorehitpause = 1
'''
    action(100,351,[0,1,2,3],[3,3,3,3],True)
    action(106,351,[4,5],[4,5])
    action(47,351,[6,7],[4,5])
    action(500,350,[0,1,2,3],[6,6,6,6],True)
    action(180,350,[4,5,6,7],[12,12,24,-1])
    for group in [8500,8510,8520]:action(group,group,range(4),[2,3,4,5])
    # The body stays at scale 1 in awakening and the dedicated idle is intact.
    source=texts['Eida.cns']
    source=source.replace('; Reuses Eida\'s existing movement poses until a dedicated run cycle is drawn.','; Dedicated four-pose run cycle, followed by a cancellable braking pose.')
    source=source.replace('[State 100, Stop released dash]\ntype = ChangeState\ntrigger1 = command != "holdfwd"\ntrigger2 = Time >= 40\nvalue = 0','[State 100, Stop released dash]\ntype = ChangeState\ntrigger1 = command != "holdfwd"\ntrigger2 = Time >= 40\nvalue = 106')
    # Replace the obsolete shared MoveHit latch with per-state contact counters.
    source=re.sub(r'(?ims)^\[State -2, (?:Reset normal impact presentation|Normal impact sparkle|Small camera accent on heavy normals|Emit normal impact only once during hitpause)\].*?(?=^\[State|\Z)','',source)
    source=source.replace('value = S1,4\nchannel = 7\nloop = 1','value = S1,17\nchannel = 7\nloop = 1')
    win='''[Statedef 180]
type = S
movetype = I
physics = S
anim = 180
ctrl = 0
velset = 0,0
[State 180, Keep winner in view]
type = ScreenBound
trigger1 = 1
value = 1
movecamera = 1,0
[State 180, Back margin]
type = PosAdd
trigger1 = BackEdgeBodyDist < 48
x = 48-BackEdgeBodyDist
[State 180, Front margin]
type = PosAdd
trigger1 = FrontEdgeBodyDist < 48
x = -(48-FrontEdgeBodyDist)
[State 180, Finish the gesture]
type = AssertSpecial
trigger1 = Time < 110
flag = RoundNotOver
flag2 = NoKOSlow
[State 180, Authentic Eida voice]
type = PlaySnd
trigger1 = Time = 0
value = S0,1
channel = 0
[State 180, Senrigan close]
type = PlaySnd
trigger1 = Time = 12
value = S1,18
channel = 3
[State 180, Brief stage emphasis]
type = BGPalFX
trigger1 = Time = 0
time = 44
mul = 200,212,235

'''
    source=re.sub(r'(?ims)^\[Statedef 180\].*?(?=^\[Statedef|\Z)',lambda m:win,source,count=1)
    texts['Eida.cns']=source
    braking='''[Statedef 106]
type = S
movetype = I
physics = S
anim = 106
ctrl = 1
velset = 0,0
[State 106, Settled]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1
'''
    passive='''[State -2, Charge release accent]
type = PlaySnd
triggerall = IsHelper = 0
triggerall = PrevStateNo = 500
triggerall = StateNo != 500
trigger1 = Time = 1
value = S1,18
channel = 3
[State -2, Clear charge motes]
type = RemoveExplod
triggerall = IsHelper = 0
trigger1 = StateNo != 500
ID = 8552
ignorehitpause = 1
'''
    passive+=fx(-2,'Footwork dust','triggerall = IsHelper = 0\ntriggerall = RoundState = 2\ntriggerall = NumExplod(8550) < 2\ntrigger1 = StateNo = 100\ntrigger1 = Time%12 = 0\ntrigger2 = StateNo = 106\ntrigger2 = Time = 1\ntrigger3 = StateNo = 52\ntrigger3 = Time = 1',8500,8550,'0,0','.7,.6',priority=-1)
    passive+='''[State -2, Soft boot step]
type = PlaySnd
triggerall = IsHelper = 0
triggerall = RoundState = 2
trigger1 = StateNo = 100
trigger1 = Time%12 = 0
trigger2 = StateNo = 52
trigger2 = Time = 1
value = S1,20
channel = 5
volumescale = 50
'''
    add('Eida.cns',-2,passive,True)
    add('Eida.cns',500,fx(500,'Small Senrigan motes','triggerall = NumExplod(8552) = 0\ntrigger1 = Time%16 = 0',8520,8552,'0,-44','.6,.6',1,2),True)
    add('Eida.cns',180,fx(180,'Fading eye accent','trigger1 = Time = 12',8520,8555,'4,-56','.45,.45',1,3))
    add('Specials.cns',1501,fx(1501,'Boot dust follows travelled distance','triggerall = NumExplod(8550) < 2\ntrigger1 = Time%8 = 0',8500,8550,'-8,0','.45,.45',priority=-1))
    for filename,states in [('Eida.cns',[200,201,202,210,211,220,221,600,610,620]),('Specials.cns',list(range(1520,1526)))]:
        for n in states:
            m=re.search(rf'(?ims)^\[Statedef {n}\].*?(?=^\[Statedef|\Z)',texts[filename]);assert m
            elements=[int(x) for x in re.findall(r'(?ims)type = HitDef\ntrigger1 = Animelem = (\d+)',m[0])]
            if not elements:continue
            animation=int(re.search(r'(?m)^anim = (\d+)',m[0])[1])
            a=re.search(rf'(?ims)^\[Begin Action {animation}\].*?(?=^\[Begin Action|\Z)',texts['Eida.air']);assert a,n
            times=[int(x) for x in re.findall(r'(?m)^\d+,\d+,-?\d+,-?\d+,(-?\d+)',a[0])]
            first=sum(times[:elements[0]-1]);last=sum(times[:elements[-1]-1])
            reset=''.join(f'[State {n}, Fresh presentation latch {v}]\ntype = VarSet\ntrigger1 = Time = 0\nv = {v}\nvalue = 0\nignorehitpause = 1\n' for v in [33,34,35])
            add(filename,n,reset,True)
            contact=f'triggerall = Time >= {first}\ntriggerall = MoveHit\ntrigger1 = HitCount > Var(33)'
            low=n in [220,221,1524];pos='30,-18' if low else ('30,-30' if n>=1500 else '32,-40')
            text=fx(n,'Confirmed contact fragments',contact,8510,8551,pos,'.5,.5')
            if n in [211,221,620] or n>=1500:
                final=f'triggerall = Time >= {last}\ntriggerall = MoveHit\ntriggerall = HitCount > Var(33)\ntrigger1 = Var(34) = 0'
                text+=fx(n,'Confirmed finishing burst',final,8510,8553,pos,'.9,.8')
                text+=f'''[State {n}, Weight on confirmed finisher]
type = PlaySnd
{final}
value = S1,19
channel = 5
volumescale = 75
ignorehitpause = 1
[State {n}, Latch finishing presentation]
type = VarSet
{final}
v = 34
value = 1
ignorehitpause = 1
'''
            text+=f'''[State {n}, Remember emitted contact]
type = VarSet
{contact}
v = 33
value = HitCount
ignorehitpause = 1
'''
            guard=f'triggerall = Time >= {first}\ntriggerall = MoveGuarded\ntrigger1 = Var(35) = 0'
            text+=fx(n,'Small guarded contact',guard,8510,8554,pos,'.3,.3')
            text+=f'''[State {n}, Remember guard contact]
type = VarSet
{guard}
v = 35
value = 1
ignorehitpause = 1
'''
            add(filename,n,text)
    texts['Eida.cns']=texts['Eida.cns'].rstrip()+'\n\n'+braking
    for name,path in paths.items():path.write_text(texts[name].rstrip()+'\n')


if __name__ == '__main__':
    import_art(); make_sounds(); apply_runtime(); install_activation()
    print('Imported 16 body poses / 12 FX and 4 nonverbal sounds; installed Eida presentation')
