#!/usr/bin/env python3
"""Author Mamushi's combat around the supplied poses, with autonomous clones."""
from pathlib import Path
import json,re,shutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Mamushi'
CLONE_LIMIT=6;CLONE_LIFE=180;CLONE_TICKS=480
MOVES=[('Brazo','a','F',1000,350),('Latigo','a','B',1010,500),
       ('Mandibula','b','F',1020,500),('Taladro','b','B',1030,650),
       ('Maza','c','F',1040,650),('Espinas','c','B',1050,500),
       ('Barrido','a','D',1400,250),('Perforacion','b','D',1410,400),
       ('TaladroAscendente','c','D',1420,500),('Guardia','y','N',1200,500),
       ('Asalto','z','N',1210,1000),('Retirada','y','D',1430,350),
       ('Division','z','D',1440,750)]
meta={m['number']:m for m in json.loads((CHAR/'assets/sprites.json').read_text())}
air=[];states=[]

def ctl(st,label,kind,triggers,params,extra=''):
    return f'\n[State {st}, {label}]\ntype = {kind}\n{triggers}\n{params}\n{extra}'
def condition(value):return 'trigger1 = '+value
def c(st,label,kind,when,params,extra=''):return ctl(st,label,kind,condition(when),params,extra)
def state(n,anim,typ='S',move='I',physics='S',cost=0,velocity=None):
    text=f'\n[Statedef {n}]\ntype = {typ}\nmovetype = {move}\nphysics = {physics}\nanim = {anim}\nctrl = 0\n'
    if velocity is not None:text+=f'velset = {velocity}\n'
    if cost:text+=f'poweradd = -{cost}\n'
    return text

def animation(n,poses,hits=None,kind='body',hurt=True,loop=False):
    hits=hits or {};text=f'\n[Begin Action {n}]\n'
    if hurt:text+='Clsn2Default: 1\n Clsn2[0] = -15,-64,15,-1\n'
    if loop:text+='Loopstart\n'
    for element,(sprite,duration) in enumerate(poses,1):
        if element in hits:
            if isinstance(sprite,tuple):g,no=sprite
            else:g,no=0,sprite
            if g==0:
                p=meta[no];w,h=Image.open(CHAR/p['file']).size;x,y=p['axis'];right=max(5,w-x-1)
                y0,y1=(-min(y,110),-3) if kind=='maza' else (-min(y,55),-17) if kind!='low' else (-27,-2)
                x0=min(18,right-4)
            else:x0,y0,right,y1=-13,-12,13,1
            text+=f'Clsn1: 1\n Clsn1[0] = {x0},{y0},{right},{y1}\n'
        g,no=sprite if isinstance(sprite,tuple) else (0,sprite)
        text+=f'{g},{no},0,0,{duration}'+(',,A' if g>=8700 else '')+'\n'
    air.append(text)

def startup(n):
    return c(n,'Audible special activation','PlaySnd','Time = 0','value = S1,21\nchannel = 4\nvolumescale = 100', 'persistent = 0\nignorehitpause = 1\n')+c(n,'Brief focus','SuperPause','Time = 0','time = 10\nmovetime = 0\nanim = -1\nsound = -1\ndarken = 1\nunhittable = 0\np2defmul = 1\npoweradd = 0','persistent = 0\nignorehitpause = 1\n')+c(n,'Small chakra flash','Explod','Time = 0','anim = 8710\nID = 8710\npostype = P1\npos = 12,-32\nscale = .8,.8\nremovetime = 10\nownpal = 1\nsprpriority = 4\nsupermovetime = 10\npausemovetime = 10\nremoveongethit = 1')

def hit(n,element,damage,fin=False,kind='body',airborne=False,attr='NA',special_sound=None):
    return c(n,f'Swing {element}','PlaySnd',f'AnimElem = {element}',f'value = S1,{special_sound or 0}\nchannel = 1')+c(n,f'Contact {element}','HitDef',f'AnimElem = {element}',f'''attr = {'A' if airborne else 'C' if kind=='low' else 'S'}, {attr}
damage = {damage},{max(1,damage//20) if attr!='NA' else 0}
animtype = {'Up' if fin else 'Medium'}
guardflag = {'L' if kind=='low' else 'MA'}
hitflag = MAF
priority = 4,Hit
pausetime = {8 if fin else 5},{11 if fin else 8}
sparkno = S8700
guard.sparkno = -1
sparkxy = 0,-36
hitsound = S1,{33 if kind=='maza' else 31 if special_sound==31 else 7 if fin else 5}
guardsound = S1,9
ground.type = {'Low' if kind=='low' else 'High'}
ground.hittime = {24 if fin else 21}
ground.slidetime = 14
ground.velocity = {-7 if fin else -.7},{-6 if fin else 0}
air.hittime = 26
air.velocity = {-6 if fin else -.6},{5 if fin and airborne else -6 if fin else -1.5}
fall = {int(fin)}
fall.recover = 1
fall.recovertime = 40
getpower = {35 if attr=='NA' else 0},0
givepower = 12,8
envshake.time = {8 if fin else 3}
envshake.ampl = {-3 if fin else -1}''')

def attack(n,poses,hits,kind='body',cost=0,airborne=False,speed=0,fin=False,sound=None,helper=False):
    animation(n,poses,hits,kind)
    text=state(n,n,'A' if airborne else 'C' if kind=='low' else 'S','A','A' if airborne else 'N',cost,None if airborne else f'{speed},0')
    if cost:text+=startup(n)
    if airborne and not helper:text+=c(n,'Count attacks this jump','VarAdd','Time = 0','v = 12\nvalue = 1')
    if speed:text+=c(n,'Finite advance','VelSet','Time >= 22','x = 0')
    for j,(element,damage) in enumerate(hits.items()):
        final=fin and j==len(hits)-1
        text+=hit(n,element,damage,final,kind,airborne,'SA' if cost or helper else 'NA',sound)
        if final:
            text+=c(n,'Finisher sound on contact','PlaySnd',f'MoveHit = 1 && AnimElemNo(0) >= {element}','value = S1,19\nchannel = 5','persistent = 0\nignorehitpause = 1\n')
            text+=c(n,'Finisher dust','Explod',f'MoveHit = 1 && AnimElemNo(0) >= {element}','anim = 8720\npostype = P1\npos = 35,0\nremovetime = -2\nownpal = 1\nsprpriority = 3','persistent = 0\nignorehitpause = 1\n')
    if airborne:
        text+=c(n,'Brief lift on aerial contact','VelSet','MoveHit = 1','y = -1.8','persistent = 0\nignorehitpause = 1\n')
        text+=c(n,'Land safely','ChangeState','Pos Y >= 0 && Vel Y > 0','value = 52\nctrl = 1')
    text+=c(n,'Recovery','ChangeState','AnimTime = 0',f'value = {9500 if helper else 50 if airborne else 0}\nctrl = {0 if helper else 1}')
    states.append(text)

def common_animations():
    source=(ROOT/'source_material/Mamushi_original/AC_Mamushi.air').read_text()
    # Retain all original hit reactions, replace unfinished neutral/guard poses.
    for match in re.finditer(r'(?ims)^\[Begin Action (\d+)\].*?(?=^\[Begin Action|\Z)',source):
        if int(match[1])>=5000 and int(match[1])!=5300:air.append(match[0].rstrip()+'\n')
    animation(0,[(4,10),(5,10),(6,10)])
    for n in [5,6,120,121,122,130,131,132,140,141,142,150,151,152]:animation(n,[(18 if n in [6,121,131,141,151] else 29,5)])
    for n in [10,11,12]:animation(n,[(18,5)])
    animation(20,[(i,5) for i in [8,9,10,11,12,13]],loop=True)
    animation(21,[(i,6) for i in [13,12,11,10,9,8]],loop=True)
    animation(100,[(i,3) for i in [8,9,10,11,12,13]],loop=True)
    for n in [40,41,42,43,44,45,46,47,52,105,106,170]:animation(n,[(76 if n in [40,41,42,43,44,45,46,105] else 18,4)])
    animation(180,[(4,12),(5,12),(41,10),(4,25)])
    animation(190,[(18,8),(46,8),(4,10)])
    animation(500,[(70,6),(71,6),(72,6)],loop=True)
    animation(520,[(46,6),(41,12),(4,12)])
    animation(5140,[(21,8)])
    animation(5500,[(4,1)])
    animation(5300,[(4,8),(5,8)])
    for g,count in [(8700,4),(8710,4),(8720,6)]:animation(g,[((g,i),2) for i in range(count)],hurt=False)

def main_attacks():
    sequences=[
      (200,[(4,2),(22,3),(23,5),(22,3),(4,5)],{3:32},'body',False),
      (201,[(22,3),(24,3),(25,5),(23,3),(4,5)],{3:44},'body',False),
      (202,[(59,3),(60,3),(61,4),(62,6),(63,6)],{4:76},'maza',True),
      (210,[(29,3),(30,4),(31,4),(32,6),(29,4)],{3:42},'body',False),
      (211,[(29,3),(31,4),(32,5),(30,4),(29,4)],{3:48},'body',False),
      (212,[(29,3),(42,5),(43,6),(42,5),(29,5)],{3:82},'body',True),
      (220,[(59,3),(60,3),(61,4),(62,5),(63,5)],{4:40},'maza',False),
      (221,[(60,3),(61,4),(62,5),(63,4),(59,4)],{3:52},'maza',False),
      (222,[(65,4),(66,4),(67,5),(68,5),(69,6),(4,5)],{3:84},'maza',True)]
    for n,poses,hits,kind,fin in sequences:attack(n,poses,hits,kind,fin=fin,sound=31 if 210<=n<=211 else None)
    for family,base in [(0,600),(1,610),(2,620)]:
        for stage in range(3):
            sprites=([74,75,77,78,76] if family==0 else [74,79,80,78,76] if family==1 else [65,66,67,68,76])
            attack(base+stage,[(s,4) for s in sprites],{3:36+stage*14},'maza' if family==2 else 'body',airborne=True,fin=stage==2)
    attack(1000,[(22,5),(23,5),(24,4),(25,5),(22,4),(23,5),(25,6),(4,7)],{2:32,4:36,7:64},cost=350,speed=2.6,fin=True,sound=30)
    attack(1020,[(29,6),(30,5),(31,5),(32,6),(30,5),(31,5),(32,6),(29,8)],{3:38,4:40,7:80},cost=500,speed=2.2,fin=True,sound=31)
    attack(1030,[(29,6),(42,5),(43,5),(42,5),(43,6),(42,6),(29,8)],{2:24,3:24,4:24,5:24,6:70},cost=650,speed=5,fin=True,sound=32)
    attack(1040,[(59,4),(60,4),(61,4),(62,5),(63,4),(65,5),(66,5),(67,5),(68,5),(69,8)],{4:42,7:42,8:96},'maza',650,speed=2.8,fin=True,sound=33)
    attack(1210,[(22,4),(23,4),(25,4),(29,3),(30,4),(32,4),(42,4),(43,4),(60,4),(62,6),(63,8)],{2:20,3:20,5:26,6:26,7:28,8:28,10:70},cost=1000,speed=2.7,fin=True,sound=30)
    attack(1400,[(47,4),(60,4),(62,5),(63,5),(47,6)],{3:65},'low',250,fin=True,sound=33)
    attack(1430,[(76,4),(74,4),(75,5),(78,5),(76,7)],{3:75},cost=350,speed=-3.5,fin=True,sound=31)

def projectiles_and_whip():
    animation(1010,[(46,6),(41,8),(41,10),(46,12),(4,8)])
    animation(9100,[(50,4),(51,5),(53,5),(54,5),(55,4),(56,4),(57,3)],{2:1,3:1,4:1},hurt=False)
    s=state(1010,1010,cost=500,velocity='0,0')+startup(1010)
    s+=c(1010,'Visible arm emerges beside Mamushi','Helper','Time = 6','helpertype = Normal\nname = "Brazo latigo"\nID = 9100\nstateno = 9100\npostype = P1\npos = 18,0\nfacing = 1\nownpal = 1\nkeyctrl = 0')
    s+=c(1010,'Recover','ChangeState','AnimTime = 0','value = 0\nctrl = 1');states.append(s)
    s=state(9100,9100,physics='N',move='A',velocity='0,0')+c(9100,'Bind to living arm','BindToRoot','1','pos = 18,0\ntime = 1')
    s+=hit(9100,2,115,True,attr='SA',special_sound=30)
    s+=ctl(9100,'Finite physical extension','DestroySelf','trigger1 = AnimTime = 0\ntrigger2 = Root,StateNo != 1010\ntrigger3 = Root,MoveType = H\ntrigger4 = RoundState != 2','', 'ignorehitpause = 1\n');states.append(s)
    animation(9200,[(34,3),(35,3),(36,3),(37,3),(38,3),(39,3)],{i:1 for i in range(1,7)},hurt=False,loop=True)
    animation(9201,[(44,4),(45,4)],{1:1,2:1},hurt=False,loop=True)
    for n,number,cost,ticks,damage,anim in [(1050,33,500,[9,17,25],38,9200),(1410,33,400,[9,15],44,9200),(1420,47,500,[13],85,9201)]:
        animation(n,[(number,6),(number,6),(number,6),(number,6),(number,6),(4,8)])
        s=state(n,n,cost=cost,velocity='0,0')+startup(n)
        for j,tick in enumerate(ticks):
            s+=c(n,f'Physical projectile {j+1}','Projectile',f'Time = {tick}',f'''projID = {n}
projanim = {anim}
projhitanim = 8700
projremanim = 8720
projremove = 1
projremovetime = 50
projmisstime = 1
projhits = 1
projedgebound = 20
offset = {35 if anim==9200 else 46},{-36-j*8 if anim==9200 else 0}
velocity = {6.5 if anim==9200 else 4},0
projpriority = 1
attr = S, SP
damage = {damage},3
guardflag = MA
hitflag = MAF
priority = 4,Hit
pausetime = 0,8
sparkno = S8700
hitsound = S1,5
guardsound = S1,9
ground.type = High
ground.hittime = 20
ground.velocity = -3,{-6 if anim==9201 else 0}
air.velocity = -3,-4
fall = {int(anim==9201)}
getpower = 0,0''')
            s+=c(n,f'Launch sound {j}','PlaySnd',f'Time = {tick}','value = S1,30\nchannel = 1')
        s+=c(n,'Recover','ChangeState','AnimTime = 0','value = 0\nctrl = 1');states.append(s)

def clones():
    animation(1440,[(46,5),(41,7),(4,8),(5,8),(4,8)])
    s=state(1440,1440,cost=750,velocity='0,0')+startup(1440)
    s+=c(1440,'Next independent generation','VarAdd','Time = 0','v = 35\nvalue = 1')
    s+=c(1440,'Independent biological duplicate','Helper','Time = 6',f'helpertype = Normal\nname = "Division Mamushi"\nID = 9500\nstateno = 9500\npostype = P1\npos = -22,0\nfacing = 1\nownpal = 1\nkeyctrl = 0\nsize.ground.back = 14\nsize.ground.front = 14\nsize.height = 67')
    s+=c(1440,'Recover control while clone fights','ChangeState','AnimTime = 0','value = 0\nctrl = 1');states.append(s)
    animation(9500,[(4,10),(5,10),(6,10)],loop=True)
    # Clone lifetime/health are independent of its original's hit reactions.
    s=state(9500,9500,physics='N',velocity='0,0')
    for kind,params in [('VarSet','v = 1\nvalue = GameTime'),('VarSet','v = 2\nvalue = Parent,Var(35)'),('VarSet',f'v = 3\nvalue = {CLONE_LIFE}'),('VarSet','v = 4\nvalue = 1')]:
        s+=c(9500,'Initialize exactly once',kind,'Var(4) = 0',params)
    s+=c(9500,'Split sound','PlaySnd','Time = 0 && Var(4) = 0','value = S1,8\nchannel = 1')
    s+=c(9500,'Decision delay grows with generation','ChangeState','Time >= 10 + IfElse(Var(2)>5,5,Var(2))*6 && (EnemyNear,StateType != L) && (Root,StateNo != 3001)','value = IfElse(P2BodyDist X > 44,9501,9503+Random%3)');states.append(s)
    animation(9501,[(i,4) for i in [8,9,10,11,12,13]],loop=True)
    s=state(9501,9501,physics='N',velocity='5.8,0')
    s+=c(9501,'Turn toward actual enemy','Turn','P2Dist X < -10','')
    s+=c(9501,'Stop in physical range','ChangeState','P2BodyDist X < 44 && P2Dist X >= 0','value = 9503+Random%3')
    s+=c(9501,'Reassess instead of permanent running','ChangeState','Time > 50 || Root,StateNo = 3001','value = 9500');states.append(s)
    for n,poses,hits,kind in [(9503,[(22,4),(23,5),(25,4),(4,6)],{2:32},'body'),(9504,[(29,4),(30,5),(32,5),(29,7)],{3:42},'body'),(9505,[(59,4),(61,5),(62,6),(63,7)],{3:40},'maza')]:
        attack(n,poses,hits,kind,helper=True,sound=31 if n==9504 else 30)
    animation(9590,[(16,5),(17,5),(18,4)])
    s=state(9590,9590,physics='S',velocity='-2,0')
    s+=c(9590,'Real incoming damage to clone health','VarAdd','Time = 0','v = 3\nvalue = -GetHitVar(damage)')
    s+=c(9590,'Impact flash','PalFX','Time = 0','time = 5\nadd = 80,0,0')
    s+=c(9590,'Recover without deleting other clones','ChangeState','Time >= 14','value = 9500');states.append(s)
    states.append(state(9591,9500,physics='N',velocity='0,0')+c(9591,'No lingering hurt state while departing','NotHitBy','1','value = SCA\ntime = 1')+c(9591,'Depart cleanly','Trans','1','trans = AddAlpha\nalpha = 256-Time*32,Time*32')+c(9591,'Done','DestroySelf','Time >= 8',''))

def cinematic():
    animation(3000,[(74,5),(76,4),(75,4),(77,5),(78,6),(76,6),(4,8)],{3:1,4:1,5:1})
    s=state(3000,3000,move='A',physics='N',cost=3000,velocity='0,0')+startup(3000)
    s+=c(3000,'Finite opening rush','VelSet','Time = 6','x = 6')+c(3000,'End rush','VelSet','Time >= 27','x = 0')
    s+=c(3000,'Opening must collide','HitDef','Time = 9','attr = S, HA\ndamage = 0,0\nguardflag = MA\nhitflag = M\npriority = 5,Hit\npausetime = 0,0\nsparkno = S8700\nhitsound = S1,31\nguardsound = S1,9\nground.hittime = 180\nground.velocity = 0,0\np1stateno = 3001\np2stateno = 3010\nID = 3000\ngetpower = 0,0\ngivepower = 0,0')
    s+=c(3000,'Miss or block recovery','ChangeState','AnimTime = 0','value = 0\nctrl = 1');states.append(s)
    animation(3001,[(41,20),(29,20),(30,12),(32,12),(60,12),(62,12),(65,12),(67,12),(68,12),(81,20),(78,12),(29,12),(4,20)])
    animation(3002,[(22,5),(23,4),(25,5),(4,8)])
    animation(3003,[(29,5),(30,5),(32,5),(29,8)])
    animation(3004,[(60,4),(61,4),(62,5),(63,8)])
    s=state(3001,3001,physics='N',velocity='0,0')
    s+=c(3001,'Confirmed sequence','Pause','Time = 0','time = 158\nmovetime = 158\npausebg = 1')
    s+=c(3001,'Protect confirmed animation','NotHitBy','1','value = SCA\ntime = 1')
    s+=c(3001,'Dim stage briefly','BGPalFX','Time = 0','time = 158\nmul = 150,180,200')
    s+=c(3001,'Hold only the struck opponent','TargetBind','Time < 148 && NumTarget(3000)>0','ID = 3000\ntime = 1\npos = 65,0')
    s+=c(3001,'Bounded damage budget','VarSet','Time = 0 && NumTarget(3000)>0','v = 20\nvalue = IfElse((Target(3000),LifeMax)>=1000,350,Floor((Target(3000),LifeMax)*.35))')
    for i,(tick,x,anim,flip) in enumerate([(18,-25,3002,1),(48,100,3003,-1),(78,10,3004,1),(108,110,3002,-1)]):
        s+=c(3001,f'Division strike {i+1}','Explod',f'Time = {tick}',f'anim = {anim}\nID = {9300+i}\npostype = P1\npos = {x},0\nfacing = {flip}\nbindtime = -1\nremovetime = -2\nownpal = 1\nsprpriority = 3\npausemovetime = 999\nsupermovetime = 999')
    for i,tick in enumerate([30,60,90,120,144]):
        damage='Var(20)-Floor(Var(20)/5)*4' if i==4 else 'Floor(Var(20)/5)'
        s+=c(3001,f'Confirmed finite impact {i+1}','TargetLifeAdd',f'Time = {tick} && NumTarget(3000)>0',f'ID = 3000\nvalue = -({damage})\nabsolute = 1\nkill = 1')
        s+=c(3001,f'Impact sound {i+1}','PlaySnd',f'Time = {tick}',f'value = S1,{33 if i in [2,4] else 31}\nchannel = 5')
        s+=c(3001,f'Impact feedback {i+1}','EnvShake',f'Time = {tick}','time = 6\nfreq = 70\nampl = -3')
        s+=c(3001,f'Impact spark {i+1}','Explod',f'Time = {tick}','anim = 8700\npostype = P1\npos = 60,-35\nremovetime = -2\nownpal = 1\nsprpriority = 6\npausemovetime = 999')
    s+=c(3001,'Release chosen victim','TargetState','Time = 150 && NumTarget(3000)>0','ID = 3000\nvalue = 3011')
    s+=c(3001,'Clear all cinematic copies','RemoveExplod','Time = 160','')
    s+=c(3001,'Return to actual combat','ChangeState','Time >= 180','value = 0\nctrl = 1');states.append(s)
    s=state(3010,5000,move='H',physics='N',velocity='0,0')
    # ChangeAnim uses the victim's own sprites, never Mamushi's SFF.
    s+=c(3010,'Own hurt pose','ChangeAnim','Time = 0 && SelfAnimExist(5000)','value = 5000')
    s+=c(3010,'Other clones cannot add cinematic damage','NotHitBy','1','value = SCA\ntime = 1')
    s+=ctl(3010,'Safety release','SelfState','trigger1 = Time >= 210\ntrigger2 = NumEnemy > 0 && EnemyNear,StateNo != 3001','value = 5050\nctrl = 0');states.append(s)
    states.append(state(3011,5050,move='H',physics='N',velocity='-5,-6')+c(3011,'Own fall states','SelfState','1','value = 5050\nctrl = 0'))

def utility():
    for n,anim,ticks in [(106,106,7),(170,170,999999),(180,180,999999),(190,190,26)]:
        s=state(n,anim,velocity='0,0')
        if n==190:s+=c(n,'Intro','AssertSpecial','Time < 25','flag = Intro')
        if n in [106,190]:s+=c(n,'Return','ChangeState',f'Time >= {ticks}','value = 0\nctrl = 1')
        else:s+=c(n,'Round pose','NotHitBy','1','value = SCA\ntime = 1')
        states.append(s)
    s=state(500,500,velocity='0,0')
    s+=c(500,'Real chakra charge','PowerAdd','1','value = 18')
    s+=c(500,'Hum','PlaySnd','Time = 0','value = S1,4\nchannel = 3\nloop = 1')
    s+=c(500,'Small dust pulse','Explod','Time % 12 = 0','anim = 8720\npostype = P1\npos = 0,0\nremovetime = -2\nownpal = 1\nsprpriority = -1')
    s+=ctl(500,'Release / full / AI charge end','ChangeState','trigger1 = AILevel = 0 && command != "hold_s"\ntrigger2 = Power >= PowerMax\ntrigger3 = AILevel > 0 && Time >= 90','value = 0\nctrl = 1');states.append(s)
    s=state(520,520,cost=1000,velocity='0,0')+startup(520)
    s+=c(520,'Temporary chakra focus','VarSet','Time = 0','v = 40\nvalue = 360')
    s+=c(520,'Cooldown','VarSet','Time = 0','v = 41\nvalue = 900')
    s+=c(520,'Recover','ChangeState','AnimTime = 0','value = 0\nctrl = 1');states.append(s)
    animation(1200,[(41,6),(46,6),(41,6),(46,6),(41,6),(4,6)])
    air[-1]=air[-1].replace('Clsn2Default: 1','Clsn1Default: 1\n Clsn1[0] = -20,-67,33,0\nClsn2Default: 1',1)
    s=state(1200,1200,cost=500,velocity='0,0')+startup(1200)
    s+=c(1200,'Short physical counter window','ReversalDef','Time = [6,29]','reversal.attr = SCA, NA, SA, HA\npausetime = 6,8\nsparkno = S8700\nhitsound = S1,9\np1stateno = 1202')
    s+=c(1200,'Counter must be triggered','ChangeState','AnimTime = 0','value = 0\nctrl = 1');states.append(s)
    attack(1202,[(29,3),(30,4),(31,4),(32,6),(29,7)],{3:95},cost=0,fin=True,sound=31)

def commands():
    text='[Remap]\na = a\nb = b\nc = c\nx = x\ny = y\nz = z\ns = s\n\n[Defaults]\ncommand.time = 20\ncommand.buffer.time = 4\n'
    def command(name,keys,time=20,buffer=None):return f'\n[Command]\nname = "{name}"\ncommand = {keys}\ntime = {time}\nbuffer.time = {buffer if buffer is not None else 1 if keys.startswith("/") and "," not in keys else 4}\n'
    for name,button,d,n,cost in MOVES:
        if d in ['F','B']:
            for keys in [f'~D,D{d},{d},{button}',f'~D,{d},{button}',f'/D{d},{button}']:text+=command(name,keys)
        else:text+=command(name,f'/D,{button}' if d=='D' else button,buffer=1 if d=='N' else 4)
    for button in ['a','b','c','x','y','z','s']:text+=command(button,button)+command('hold_'+button,'/'+button,1)
    for name,keys in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D'),('FF','F,F'),('BB','B,B'),('recovery','a+b')]:text+=command(name,keys)
    text+='\n[Statedef -1]\n'
    for name,button,d,n,cost in MOVES:
        if n==1440:continue
        extra='\ntriggerall = command != "holddown"' if d=='N' else ''
        text+=ctl(-1,name,'ChangeState',f'triggerall = AILevel = 0\ntriggerall = command = "{name}"\ntriggerall = StateType != A\ntriggerall = Power >= {cost}{extra}\ntrigger1 = ctrl\ntrigger2 = StateNo = [200,222]\ntrigger2 = MoveHit',f'value = {n}', 'ignorehitpause = 1\n')
    text+=ctl(-1,'Independent Division','ChangeState',f'triggerall = AILevel = 0\ntriggerall = command = "Division"\ntriggerall = StateType != A\ntriggerall = Power >= 750\ntriggerall = NumHelper(9500) < {CLONE_LIMIT}\ntrigger1 = ctrl','value = 1440')
    text+=ctl(-1,'Chakra focus with down and LB','ChangeState','triggerall = AILevel = 0\ntriggerall = command = "s"\ntriggerall = command = "holddown"\ntriggerall = Power >= 3000\ntriggerall = Var(40) = 0\ntriggerall = Var(41) = 0\ntrigger1 = ctrl\ntrigger1 = StateType != A','value = 520')
    text+=ctl(-1,'Xbox A ultimate','ChangeState','triggerall = AILevel = 0\ntriggerall = command = "x"\ntriggerall = StateType != A\ntriggerall = Power >= 3000\ntrigger1 = ctrl','value = 3000')
    text+=ctl(-1,'LB charge','ChangeState','triggerall = AILevel = 0\ntriggerall = command = "hold_s"\ntriggerall = command != "holddown"\ntriggerall = StateType != A\ntriggerall = Power < PowerMax\ntrigger1 = ctrl','value = 500')
    for name,n in [('FF',100),('BB',105)]:text+=ctl(-1,name,'ChangeState',f'triggerall = AILevel = 0\ntriggerall = command = "{name}"\ntriggerall = StateType = S\ntrigger1 = ctrl',f'value = {n}')
    for button,base,airbase in [('a',200,600),('b',210,610),('c',220,620)]:
        text+=ctl(-1,'Ground mixed three-stage chain','ChangeState',f'triggerall = AILevel = 0\ntriggerall = command = "{button}"\ntriggerall = StateType != A\ntriggerall = command != "holddown"\ntrigger1 = ctrl\ntrigger2 = StateNo = 200 || StateNo = 210 || StateNo = 220\ntrigger2 = MoveHit\ntrigger2 = Time >= 4\ntrigger3 = StateNo = 201 || StateNo = 211 || StateNo = 221\ntrigger3 = MoveHit\ntrigger3 = Time >= 4',f'value = {base}+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))','ignorehitpause = 1\n')
        text+=ctl(-1,'Mixed aerial chain capped per jump','ChangeState',f'triggerall = AILevel = 0\ntriggerall = command = "{button}"\ntriggerall = StateType = A\ntriggerall = Var(12) < 3\ntrigger1 = ctrl\ntrigger2 = StateNo = [600,622]\ntrigger2 = MoveHit\ntrigger2 = Time >= 4',f'value = {airbase}+Var(12)','ignorehitpause = 1\n')
    # CPU uses the same real states, costs and collisions as the player.
    for n,cost,dist in [(3000,3000,150),(1440,750,250),(1030,650,160),(1000,350,100)]:
        more=f'\ntriggerall = NumHelper(9500) < {CLONE_LIMIT}' if n==1440 else ''
        text+=ctl(-1,'CPU legal technique','ChangeState',f'triggerall = AILevel > 0\ntriggerall = RoundState = 2\ntriggerall = ctrl\ntriggerall = StateType != A\ntriggerall = Power >= {cost}{more}\ntrigger1 = P2BodyDist X < {dist}\ntrigger1 = Random < 8+AILevel*2',f'value = {n}')
    text+=ctl(-1,'CPU normal / follow-up','ChangeState','triggerall = AILevel > 0\ntriggerall = RoundState = 2\ntriggerall = StateType != A\ntriggerall = P2BodyDist X < 45\ntrigger1 = ctrl\ntrigger2 = (StateNo=200 || StateNo=201) && MoveHit\ntrigger2 = Time >= 4','value = IfElse(ctrl,200,StateNo+1)','ignorehitpause = 1\n')
    text+=ctl(-1,'CPU approach','ChangeState','triggerall = AILevel > 0\ntriggerall = RoundState = 2\ntriggerall = ctrl\ntriggerall = StateType != A\ntrigger1 = P2BodyDist X >= 45','value = 20\nctrl = 1')
    (CHAR/'Mamushi.cmd').write_text(text)

def system():
    text='\n[Statedef -2]\n'
    for var,when in [(40,'Var(40)>0'),(41,'Var(41)>0')]:text+=ctl(-2,'Finite chakra timer','VarAdd',f'triggerall = !IsHelper\ntrigger1 = {when}',f'v = {var}\nvalue = -1')
    text+=ctl(-2,'Normal body size during focus','AttackMulSet','triggerall = !IsHelper\ntrigger1 = 1','value = IfElse(Var(40)>0,1.15,1)')
    text+=ctl(-2,'Subtle chakra tint only','PalFX','triggerall = !IsHelper\ntrigger1 = Var(40)>0','time = 1\nmul = 220,245,255\nadd = 0,8,15')
    text+=ctl(-2,'Aerial limit resets after landing','VarSet','triggerall = !IsHelper\ntrigger1 = StateType != A','v = 12\nvalue = 0')
    text+=ctl(-2,'Charge hum only during charge','StopSnd','triggerall = !IsHelper\ntrigger1 = StateNo != 500','channel = 3')
    text+=ctl(-2,'Keep root controls out of helper AI','HitOverride','triggerall = IsHelper(9500)\ntriggerall = StateNo != 9591\ntrigger1 = 1','attr = SCA, AA, AP, AT\nstateno = 9590\ntime = 1\nforceair = 0','ignorehitpause = 1\n')
    text+=ctl(-2,'Clone health tracked independently','LifeSet','triggerall = IsHelper(9500)\ntrigger1 = StateNo != 9591','value = 1000','ignorehitpause = 1\n')
    text+=ctl(-2,'Clones face the actual opponent','Turn','triggerall = IsHelper(9500)\ntriggerall = StateNo = 9500\ntrigger1 = P2Dist X < -5','','ignorehitpause = 1\n')
    text+=ctl(-2,'Independent finite clone cleanup','ChangeState',f'triggerall = IsHelper(9500)\ntriggerall = Var(4)=1\ntriggerall = StateNo != 9591\ntrigger1 = Var(3)<=0\ntrigger2 = GameTime-Var(1)>={CLONE_TICKS}\ntrigger3 = RoundState != 2','value = 9591','ignorehitpause = 1\n')
    text+=ctl(-2,'Mature clones pause during confirmed cinema','ChangeState','triggerall = IsHelper(9500)\ntriggerall = StateNo = 9501 || StateNo = [9503,9505]\ntrigger1 = Root,StateNo = 3001','value = 9500','ignorehitpause = 1\n')
    return text

def main():
    air.clear();states.clear();common_animations();main_attacks();projectiles_and_whip();clones();cinematic();utility();commands()
    # Helpers do not execute the root's -2 in MUGEN. Their health, orientation
    # and cleanup must run in each actual helper state, not only in -2.
    for index,text in enumerate(states):
        match=re.search(r'\[Statedef (9500|9501|9503|9504|9505|9590)\]',text)
        if not match:continue
        n=int(match[1]);start=text.index('\n[State ',match.end())
        life=c(n,'Own hit override','HitOverride','1','attr = SCA, AA, AP, AT\nstateno = 9590\ntime = 1','ignorehitpause = 1\n')
        life+=c(n,'Manual clone health system','LifeSet','1','value = 1000','ignorehitpause = 1\n')
        life+=ctl(n,'Independent expiration','ChangeState',f'triggerall = Var(4)=1\ntrigger1 = Var(3)<=0\ntrigger2 = GameTime-Var(1)>={CLONE_TICKS}\ntrigger3 = RoundState != 2','value = 9591','ignorehitpause = 1\n')
        if n==9500:life+=c(n,'Turn toward actual opponent','Turn','P2Dist X < -5','')
        states[index]=text[:start]+life+text[start:]
    constants='''[Data]
life = 1100
power = 3000
attack = 100
defence = 105
fall.defence_up = 20
liedown.time = 28
airjuggle = 15
sparkno = 2
guard.sparkno = 40
KO.echo = 0
volume = 0
IntPersistIndex = 60
FloatPersistIndex = 40
[Size]
xscale = 1
yscale = 1
ground.back = 15
ground.front = 16
air.back = 12
air.front = 12
height = 67
attack.dist = 100
proj.attack.dist = 160
head.pos = 0,-59
mid.pos = 0,-34
shadowoffset = 0
draw.offset = 0,0
[Velocity]
walk.fwd = 2.4
walk.back = -2.2
run.fwd = 6.2,0
run.back = -4.2,-3.5
jump.neu = 0,-8.4
jump.back = -2.8
jump.fwd = 3
runjump.back = -2.8,-8.4
runjump.fwd = 4.5,-8.4
airjump.neu = 0,-7
airjump.back = -2.8
airjump.fwd = 3
[Movement]
airjump.num = 1
airjump.height = 35
yaccel = .48
stand.friction = .85
crouch.friction = .82
stand.friction.threshold = 2
crouch.friction.threshold = .05
'''
    (CHAR/'Mamushi.cns').write_text('; Built from the supplied sprite moves. MUGEN 1.1 controllers only.\n'+constants+''.join(states)+system())
    (CHAR/'Mamushi.air').write_text('; Original sprites retained at scale 1. Authored timing and collisions.\n'+''.join(air))
    shutil.copy2(ROOT/'source_material/Mamushi_support/common1.cns',CHAR/'common1.cns')
    (CHAR/'Mamushi.def').write_text('''[Info]
name = "Mamushi"
displayname = "Mamushi Shinju"
versiondate = 10,21,2026
mugenversion = 1.1
author = "misterioso924 (source), Vahidras (sprites), Codex (combat rebuild)"
localcoord = 320,240
[Files]
sprite = Mamushi.sff
sound = Mamushi.snd
anim = Mamushi.air
cmd = Mamushi.cmd
cns = Mamushi.cns
st = Mamushi.cns
stcommon = common1.cns
''')
    shutil.copy2(CHAR/'Mamushi.def',CHAR/'AC_Mamushi.def')
    (CHAR/'assets/moves.json').write_text(json.dumps(dict(techniques=MOVES,clone_limit=CLONE_LIMIT,clone_life=CLONE_LIFE,clone_ticks=CLONE_TICKS,clone_generation_decision_delay='10+6*min(generation,5)',ultimate_damage='min(350, floor(enemy_lifemax*.35))',ultimate_cost=3000,original_art_changed=False),indent=2)+'\n')
    print(f'Mamushi combat authored: 9 ground normals, 9 aerial stages, {len(MOVES)} techniques, independent clones and collision-confirmed ultimate')

if __name__=='__main__':main()
