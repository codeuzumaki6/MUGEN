#!/usr/bin/env python3
"""Shibai's own state machine: wind chains, divine techniques, two real forms."""
from pathlib import Path
import json,re
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Shibai'
MOVES=[('Vendaval','a','F',1000,300),('Ciclon','a','B',1010,450),
       ('RafagaCortante','b','F',1020,400),('TruenoDoble','b','B',1030,550),
       ('Tormenta','c','F',1040,550),('Repulsion','c','B',1050,650),
       ('RafagaBaja','a','D',1400,250),('RemolinoBajo','b','D',1410,350),
       ('Descarga','c','D',1420,400),('Reflejo','y','N',1200,450),
       ('Garra','z','N',1210,300),('Senrigan','y','D',1430,500),
       ('SalidaGarra','z','D',1440,650)]
AWAKENED_SHOTS={
    1000:[(36,8800,75,80,0,6.8,0)],
    1010:[(40,8800,80,190,0,1.6,0)],
    1020:[(34,8830,60,45,-28,12,0),(42,8830,75,45,-48,12,0)],
    1030:[(44,8810,80,230,0,0,0)],
    1040:[(50,8810,60,255,0,0,0),(58,8810,75,300,0,0,0)],
    1050:[(25,8850,60,0,-38,6.2,0),(25,8850,60,0,-38,-6.2,0)],
    1400:[(19,8830,55,32,-13,9,0)],
    1410:[(32,8830,70,35,-13,11,0)],
    1420:[(24,8810,70,110,0,0,0)]}
air=[];states=[];body_actions={}

def ctl(n,label,kind,triggers,params='',extra=''):
    return f'\n[State {n}, {label}]\ntype = {kind}\n{triggers}\n{params}\n{extra}'
def c(n,label,kind,when,params='',extra=''):return ctl(n,label,kind,'trigger1 = '+when,params,extra)
def costexpr(cost):return f'IfElse(Var(40)>0,{round(cost*.6)},{cost})'
def state(n,anim=None,typ='S',move='I',physics='N',cost=0,velocity='0,0',control=0,body=True):
    out=f'\n[Statedef {n}]\ntype = {typ}\nmovetype = {move}\nphysics = {physics}\nctrl = {control}\n'
    if anim is not None:out+=f'anim = {anim}'+(' + IfElse(Var(40)>0,10000,0)' if body else '')+'\n'
    if velocity is not None:out+='velset = '+velocity+'\n'
    if cost:out+='poweradd = -'+costexpr(cost)+'\n'
    return out
def animation(n,poses,hurt=True,hitbox=None,loop=False):
    body_actions[n]=(poses,hurt,hitbox,loop)
def fxaction(n,g,count=6,ticks=3,hitbox=None,loop=False,add=True):
    out=f'\n[Begin Action {n}]\n'
    if hitbox:out+=f'Clsn1Default: 1\n Clsn1[0] = {hitbox}\n'
    if loop:out+='Loopstart\n'
    for i in range(count):out+=f'{g},{i},0,0,{ticks}'+(',,A' if add else '')+'\n'
    air.append(out)
def effect(n,when,anim,x=0,y=0,scale=1,seconds=-2,priority=3):
    return c(n,'Visible technique effect','Explod',when,f'anim = {anim}\npostype = P1\npos = {x},{y}\nscale = {scale},{scale}\nremovetime = {seconds}\nownpal = 1\nsprpriority = {priority}\npausemovetime = 999\nsupermovetime = 999\nremoveongethit = 0')
def startup(n,sound=21):
    return c(n,'Audible special activation','PlaySnd','Time = 0',f'value = S1,{sound}\nchannel = 4','persistent = 0\nignorehitpause = 1\n')+c(n,'Divine focus','SuperPause','Time = 0','time = 10\nmovetime = 0\nanim = -1\nsound = -1\ndarken = 1\nunhittable = 0\np2defmul = 1\npoweradd = 0','persistent = 0\nignorehitpause = 1\n')+effect(n,'Time = 0',8710,10,-42,.8,10)
def recover(n,when='AnimTime = 0',aerial=False):
    return c(n,'Return to movement','ChangeState',when,f'value = {50 if aerial else 0}\nctrl = 1')
def awakened(controller):
    return controller.replace('trigger1 = ', 'triggerall = Var(40)>0\ntrigger1 = ',1)
def divine_cast(n):
    return (awakened(effect(n,'Time = 4',8850,0,-40,.85,18,-2))
            +awakened(c(n,'Divine storm contrast','BGPalFX','Time = 4','time = 10\nmul = 100,135,190'))
            +awakened(c(n,'Divine pressure','EnvShake','Time = 6','time = 8\nfreq = 65\nampl = -3')))
def claw_portal(n,when,x=0):
    return c(n,'Crossed Code bands at entrance or exit','Helper',when,f'helpertype = Normal\nname = "Garras cruzadas"\nID = 9601\nstateno = 9601\npostype = P1\npos = {x},0\nfacing = 1\nkeyctrl = 0\nownpal = 1')
def projectile(n,tick,anim,damage,x=30,y=-36,vx=6,vy=0,fin=False,low=False,pid=None,lifetime=65,scale=1,normal=False):
    pid=n if pid is None else pid
    return c(n,'Physical visible attack','Projectile',f'Time = {tick}',f'''projID = {pid}
projanim = {anim}
projhitanim = {8801 if anim==8800 else 8811 if anim==8810 else 8700}
projremanim = {8801 if anim==8800 else 8700}
projremove = 1
projremovetime = {lifetime}
projhits = 1
projmisstime = 1
projedgebound = 30
projpriority = 2
projscale = {scale}*IfElse(Var(40)>0,1.65,1),{scale}*IfElse(Var(40)>0,1.65,1)
offset = {x},{y}
velocity = {vx}*IfElse(Var(40)>0,1.15,1),{vy}
attr = {'A' if 600<=n<=622 else 'S'}, {'NP' if normal else 'SP'}
damage = {damage},{0 if normal else 4}
guardflag = {'L' if low else 'MA'}
hitflag = MAF
priority = 5,Hit
pausetime = 0,{12 if fin else 9}
sparkno = S8700
guard.sparkno = -1
hitsound = S1,{19 if fin else 7}
guardsound = S1,9
ground.type = {'Low' if low else 'High'}
ground.hittime = {34 if not fin else 26}
ground.slidetime = 22
ground.velocity = {-6 if fin else -1},{-7 if fin else 0}
air.hittime = 30
air.velocity = {-5 if fin else -.7},{-4.5 if fin else -1.5}
fall = {int(fin)}
fall.recover = 1
fall.recovertime = 45
getpower = {40 if normal else 0},0
givepower = 12,8
envshake.time = {8 if fin else 3}
envshake.ampl = IfElse(Var(40)>0,{-6 if fin else -2},{-4 if fin else -1})''')

def animations():
    animation(0,[(0,10),(1,10),(2,10)])
    for n in [5,120,122,130,132,140,142,150,152]:animation(n,[(19,6)])
    for n in [6,10,11,12,121,131,141,151]:animation(n,[(9,5)])
    animation(20,[(3,5),(4,5),(5,5)],loop=True);animation(21,[(5,6),(4,6),(3,6)],loop=True)
    animation(100,[(3,3),(4,3),(5,3)],loop=True)
    animation(40,[(6,4)]);animation(105,[(5,3),(4,3),(3,3)],loop=True)
    for n in [41,42,43,44,45,46,47]:animation(n,[(7 if n<44 else 8,6)])
    animation(52,[(6,3),(22,3),(0,3)])
    animation(170,[(0,10),(1,10)],loop=True);animation(180,[(20,10),(21,10),(0,20)],loop=True)
    animation(190,[(20,6),(0,12)]);animation(500,[(18,8),(20,8),(18,8)],loop=True)
    animation(520,[(18,8),(20,8),(21,8),(0,8)])
    for n in [5000,5001,5002,5005,5006,5007,5010,5011,5012,5015,5016,5017,5020,5021,5022,5025,5026,5027,5030,5035,5040,5050,5051,5052,5060,5061,5062,5070,5080,5090,5200,5210]:animation(n,[(10,5),(11,5)])
    for n in [5100,5110,5140,5150,5160,5170]:animation(n,[(23,6)])
    animation(5120,[(23,4),(22,8),(6,5),(0,3)]);animation(5300,[(11,6),(0,6)]);animation(5500,[(0,1)])
    for g,count in [(8700,4),(8710,4),(8720,6)]:fxaction(g,g,count,2)
    fxaction(8800,8800,6,4,hitbox='-29,-100,29,-4',loop=True)
    fxaction(8810,8810,6,3,hitbox='-18,-151,18,-2')
    fxaction(8801,8800,6,3)
    fxaction(8811,8810,6,2)
    fxaction(8820,8820,6,4,add=False)
    fxaction(8830,8830,6,3,hitbox='-25,-20,25,20',loop=True)
    fxaction(8840,8840,6,3)
    fxaction(8850,8850,6,3,hitbox='-58,-58,58,58')
    air.append('\n[Begin Action 8880]\n8880,0,0,0,6\nLoopstart\n8880,0,0,0,6\n')
    fxaction(8881,8881,1,6,loop=True,add=False)
    fxaction(8900,8900,24,2,loop=True)
    fxaction(8910,8910,5,2)
    fxaction(8920,8920,9,2)

def normals():
    for family,base in enumerate([200,210,220]):
        for stage in range(3):
            n=base+stage;last=stage==2
            poses=[(12,3),(13 if family==0 else 15 if family==1 else 14,5),(16 if last else 13,8),(0,10)]
            animation(n,poses)
            s=state(n,n,move='A',physics='S')
            s+=c(n,'Wind sweep sound','PlaySnd','Time = 4','value = S1,30\nchannel = 1')
            s+=projectile(n,5,8800 if last else 8830,[48,62,94][stage],x=38,y=0 if last else -39,vx=7 if family==0 else 5.5,fin=last,scale=.78 if last else .8,normal=True)
            s+=recover(n);states.append(s)
    for family,base in enumerate([600,610,620]):
        for stage in range(3):
            n=base+stage;animation(n,[(12,3),(13 if family==0 else 15 if family==1 else 14,5),(16,8),(8,6)])
            s=state(n,n,'A','A','A',velocity=None)
            s+=c(n,'Finite aerial chain','VarAdd','Time = 0','v = 12\nvalue = 1')
            s+=c(n,'Wind sound','PlaySnd','Time = 4','value = S1,30\nchannel = 1')
            s+=projectile(n,5,8830,42+stage*14,x=32,y=-32,vx=6,fin=stage==2,normal=True)
            s+=c(n,'One brief air lift','VelSet',f'ProjHitTime({n}) = 0','y = -1.5','persistent = 0\n')
            s+=c(n,'Land correctly','ChangeState','Pos Y >= 0 && Vel Y > 0','value = 52\nctrl = 1')+recover(n,aerial=True);states.append(s)

def specials():
    # Every cast has a tell and finite projectiles; positions do not home to the enemy.
    specs={1000:(300,16,[(9,8800,58,40,0,5,0),(24,8800,82,48,0,5.8,0)]),
      1010:(450,20,[(12,8800,92,80,0,1.2,0),(28,8800,92,130,0,1,0)]),
      1020:(400,13,[(10,8830,48,35,-28,10,0),(18,8830,48,35,-48,10,0),(26,8830,75,35,-35,11,0)]),
      1030:(550,17,[(16,8810,90,100,0,0,0),(32,8810,90,175,0,0,0)]),
      1040:(550,17,[(12,8810,70,90,0,0,0),(27,8810,70,145,0,0,0),(42,8810,90,200,0,0,0)]),
      1050:(650,16,[(12,8850,145,0,-38,5.3,0),(12,8850,145,0,-38,-5.3,0)]),
      1400:(250,14,[(8,8830,90,32,-13,7,0)]),
      1410:(350,13,[(10,8830,52,35,-13,11,0),(22,8830,75,35,-13,11,0)]),
      1420:(400,17,[(12,8810,110,48,0,0,0)])}
    for n,(cost,pose,shots) in specs.items():
        last_base=max(t[0] for t in shots);last_divine=max(t[0] for t in AWAKENED_SHOTS[n])
        duration=last_divine+25;animation(n,[(12,6),(pose,8),(pose,duration-22),(0,8)])
        s=state(n,n,move='A',physics='S',cost=cost)+startup(n)+divine_cast(n)
        if n==1050:s+=effect(n,'Time = 4',8840,0,-68,.32,12)
        sound=31 if n in [1030,1040,1420] else 30
        for i,(tick,anim,damage,x,y,vx,vy) in enumerate(shots):
            s+=c(n,'Technique sound','PlaySnd',f'Time = {tick}',f'value = S1,{sound}\nchannel = 1')
            s+=projectile(n,tick,anim,damage,x,y,vx,vy,fin=i==len(shots)-1 or n==1050,low=n in [1400,1410],pid=n+i,lifetime=20 if anim in [8810,8850] else 65)
        for i,(tick,anim,damage,x,y,vx,vy) in enumerate(AWAKENED_SHOTS[n]):
            s+=awakened(c(n,'Divine chained technique sound','PlaySnd',f'Time = {tick}',f'value = S1,{sound}\nchannel = 1'))
            s+=awakened(projectile(n,tick,anim,damage,x,y,vx,vy,fin=i==len(AWAKENED_SHOTS[n])-1,low=n in [1400,1410],pid=n+8+i,lifetime=20 if anim in [8810,8850] else 65))
        s+=recover(n,f'Var(40)=0 && Time >= {last_base+25}')+recover(n);states.append(s)
    # Claw marks are fixed, readable portals, followed by a blockable burst.
    for n,cost,retreat in [(1211,300,False),(1440,650,True)]:
        animation(n,[(19,6),(20,8),(16,12),(0,22)])
        s=state(n,n,move='A',physics='N',cost=cost)+startup(n)+divine_cast(n)
        s+=claw_portal(n,'Time = 3')
        s+=c(n,'Fade into the crossed bands','Trans','Time >= 7 && Time < 11','trans = AddAlpha\nalpha = 256-(Time-7)*64,(Time-7)*64')
        s+=c(n,'Enter the slit before crossing','AssertSpecial','Time >= 10 && Time < 18','flag = Invisible')
        s+=c(n,'Emerge through the destination bands','Trans','Time >= 18 && Time < 22','trans = AddAlpha\nalpha = (Time-17)*64,256-(Time-17)*64')
        s+=c(n,'Cross without pushing through bodies','PlayerPush','Time >= 8 && Time <= 18','value = 0')
        if n==1211:
            s+=c(n,'Read saved physical mark','VarSet','Time = 0 && NumHelper(9600)>0','v = 22\nvalue = Floor(Helper(9600),Pos X)')
            s+=c(n,'Travel to placed mark, not enemy coordinates','PosSet','Time = 14','x = Var(22)')
            s+=c(n,'Face opponent after exit','Turn','Time = 15 && P2Dist X<0','')
        else:
            s+=claw_portal(n,'Time = 3',-80)
            s+=c(n,'Finite backward claw crossing','PosAdd','Time = 14','x = -80')
        s+=claw_portal(n,'Time = 15')
        s+=c(n,'Teleport sound','PlaySnd','Time = 14','value = S1,32\nchannel = 1')
        s+=projectile(n,19,8800,135,38,0,5.8,0,fin=True,lifetime=55)
        s+=awakened(projectile(n,30,8810,70,110,0,0,0,fin=True,pid=n+8,lifetime=20))
        s+=awakened(c(n,'Thunder through the exit','PlaySnd','Time = 30','value = S1,31\nchannel = 1'))
        s+=recover(n,'Var(40)=0 && Time >= 36')+recover(n);states.append(s)
    animation(1210,[(19,5),(20,8),(0,12)])
    s=state(1210,1210,cost=300,physics='S')+startup(1210)
    s+=c(1210,'Place the original flat ground mark','Helper','Time = 6','helpertype = Normal\nname = "Marca de garra"\nID = 9600\nstateno = 9600\npostype = P1\npos = 125,0\nfacing = 1\nkeyctrl = 0\nownpal = 1')
    s+=c(1210,'Audible claw placement','PlaySnd','Time = 6','value = S1,32\nchannel = 1')
    s+=recover(1210);states.append(s)
    for n in [9600,9601]:
        s=state(n,8880 if n==9600 else 8881,physics='N',body=False)
        s+=c(n,'Mark is not a fighter','PlayerPush','1','value = 0')
        s+=c(n,'Mark does not absorb hits','NotHitBy','1','value = SCA\ntime = 1')
        s+=c(n,'Ground marks stay flat; crossed bands open naturally','AngleDraw','1','value = 0\nscale = 1,1' if n==9600 else 'value = 0\nscale = IfElse(Time<6,.4+Time*.1,IfElse(Time>=30,(36-Time)/6.0,1)),1.35')
        s+=c(n,'Mark has no independent fighter shadow','AssertSpecial','1','flag = NoShadow')
        s+=c(n,'Original black bands and white studs','SprPriority','1',f'value = {-2 if n==9600 else 3}')
        expiry='trigger1 = Time >= 600\ntrigger2 = RoundState != 2\ntrigger3 = Root,StateNo = 1211\ntrigger3 = Root,Time >= 14' if n==9600 else 'trigger1 = Time >= 36\ntrigger2 = RoundState != 2'
        s+=ctl(n,'Finite portal lifetime','DestroySelf',expiry);states.append(s)
    for n,cost,ticks in [(1200,450,34),(1430,500,60)]:
        animation(n,[(19,6),(19,ticks-12),(0,6)],hitbox='-23,-78,38,-1')
        s=state(n,n,physics='S',cost=cost)+startup(n)
        if n==1430:s+=effect(n,'Time = 4',8840,0,-92,1,50)
        s+=c(n,'Reflect incoming physical attack','ReversalDef',f'Time >= 6 && Time <= {ticks-6}','reversal.attr = SCA, NA, SA, HA\npausetime = 4,7\nsparkno = S8700\nhitsound = S1,9\np1stateno = 1202')
        s+=recover(n);states.append(s)
    animation(1202,[(19,3),(16,8),(21,8),(0,8)],hitbox='-15,-65,140,-6')
    s=state(1202,1202,move='A',physics='S')+effect(1202,'Time = 2',8850,45,-38,1.2)
    s+=c(1202,'Reflected force still requires contact','HitDef','Time = 3','attr = S, SA\ndamage = 130,0\nhitflag = MAF\npriority = 6,Hit\npausetime = 8,12\nsparkno = S8700\nhitsound = S1,33\nground.type = High\nground.hittime = 24\nground.velocity = -8,-7\nair.velocity = -7,-5\nfall = 1\ngetpower = 0,0')
    s+=recover(1202);states.append(s)

def ultimate():
    animation(3000,[(12,6),(16,8),(21,10),(0,14)],hitbox='15,-68,52,-12')
    s=state(3000,3000,move='A',cost=0,physics='S')
    # Ultimate is always the full three bars, even while transcended.
    s+=c(3000,'Spend three bars even on miss','PowerAdd','Time = 0','value = -3000')+startup(3000)+divine_cast(3000)
    s+=effect(3000,'Time = 4',8830,35,-38,1.3,30)
    s+=c(3000,'Opening must hit a standing opponent','Projectile','Time = 8','projID = 3000\nprojanim = 8830\nprojhitanim = 8700\nprojremanim = 8700\nprojremovetime = 20\nprojhits = 1\nprojremove = 1\nprojedgebound = 20\noffset = 35,-38\nvelocity = 7,0\nattr = S, HP\ndamage = 0,0\nguardflag = MA\nhitflag = M\npausetime = 0,0\nsparkno = S8700\nhitsound = S1,34\nguardsound = S1,9\nground.hittime = 200\nground.velocity = 0,0\np2stateno = 3010\nID = 3000\ngetpower = 0,0\ngivepower = 0,0')
    s+=c(3000,'Confirm only fresh opening contact','ChangeState','Time>=8 && NumTarget(3000)>0 && ProjHitTime(3000)>=0 && ProjHitTime(3000)<=2','value = 3001')
    s+=recover(3000,'Time >= 55');states.append(s)
    animation(3001,[(20,20),(17,25),(21,25),(16,20),(21,30),(0,40)])
    s=state(3001,3001,physics='N')
    s+=c(3001,'Bounded cinematic','Pause','Time = 0','time = 145\nmovetime = 145\npausebg = 1')
    s+=c(3001,'Protect only confirmed sequence','NotHitBy','1','value = SCA\ntime = 1')
    s+=c(3001,'Dim world','BGPalFX','Time = 0','time = 145\nmul = 65,95,125')
    s+=c(3001,'Only the struck target','TargetBind','Time < 138 && NumTarget(3000)>0','ID = 3000\ntime = 1\npos = 100,0')
    s+=c(3001,'Bounded life-relative damage','VarSet','Time = 0 && NumTarget(3000)>0','v = 20\nvalue = IfElse((Target(3000),LifeMax)>=1000,420,Floor((Target(3000),LifeMax)*.42))')
    s+=c(3001,'Divine release sound','PlaySnd','Time = 0','value = S1,35\nchannel = 5')
    for i,tick in enumerate([18,43,68,93,122]):
        s+=effect(3001,f'Time = {tick}',[8840,8800,8810,8850,8850][i],100,[-75,0,0,-38,-38][i],f'{1.5 if i==4 else 1.2}*IfElse(Var(40)>0,1.4,1)',22,6)
        damage='-(Var(20)-Floor(Var(20)/5)*4)' if i==4 else '-Floor(Var(20)/5)'
        s+=c(3001,'Confirmed bounded damage','TargetLifeAdd',f'Time = {tick} && NumTarget(3000)>0',f'ID = 3000\nvalue = {damage}\nabsolute = 1\nkill = 1')
        s+=c(3001,'Impact sound','PlaySnd',f'Time = {tick}',f'value = S1,{31 if i==2 else 33}\nchannel = 1')
        s+=c(3001,'Impact shake','EnvShake',f'Time = {tick}','time = 7\nfreq = 65\nampl = IfElse(Var(40)>0,-6,-4)')
    s+=c(3001,'Release target safely','TargetState','Time = 140 && NumTarget(3000)>0','ID = 3000\nvalue = 3011')+recover(3001,'Time >= 160');states.append(s)
    s=state(3010,anim=None,move='H',physics='N')
    s+=c(3010,'Use victims own hurt animation','ChangeAnim','Time = 0 && SelfAnimExist(5000)','value = 5000')
    s+=ctl(3010,'Safety release','SelfState','trigger1 = Time > 200\ntrigger2 = NumEnemy = 0\ntrigger3 = Time > 12 && EnemyNear,StateNo != 3001','value = 5050\nctrl = 0');states.append(s)
    states.append(state(3011,anim=None,typ='A',move='H',physics='N',velocity='-7,-6')+c(3011,'Own fall state','SelfState','1','value = 5050\nctrl = 0'))

def utility():
    for n,ticks in [(170,None),(180,None),(190,24)]:
        s=state(n,n,physics='S')
        s+=c(n,'Intro','AssertSpecial','Time < 23','flag = Intro') if n==190 else c(n,'Round pose','Null','1')
        if ticks:s+=recover(n,f'Time >= {ticks}')
        states.append(s)
    s=state(500,500,physics='S')+c(500,'Charge energy','PowerAdd','1','value = 22')
    s+=c(500,'Charge hum','PlaySnd','Time = 0','value = S1,4\nchannel = 3\nloop = 1')
    s+=c(500,'Actual animated chakra envelope','Helper','Time = 0','helpertype = Normal\nname = "Aura de Shibai"\nID = 9550\nstateno = 9550\npostype = P1\npos = 0,-40\nfacing = 1\nkeyctrl = 0\nownpal = 1')
    s+=c(500,'Ground pressure waves','Explod','Time % 12 = 2','anim = 8910\nID = 9551\npostype = P1\npos = 0,-1\nscale = .34,.26\nremovetime = -2\nownpal = 1\nsprpriority = -1\nremoveongethit = 1')
    s+=c(500,'Ascending chakra particles','Explod','Time % 12 = 4','anim = 8920\nID = 9552\npostype = P1\npos = IfElse(Time%24<12,-19,19),-30\nvel = 0,-.9\nscale = .23,.23\nremovetime = 18\nownpal = 1\nsprpriority = 2\nremoveongethit = 1')
    s+=ctl(500,'Release charge','ChangeState','trigger1 = AILevel = 0 && command != "hold_s"\ntrigger2 = Power >= 3000\ntrigger3 = AILevel>0 && Time>=65','value = 0\nctrl = 1');states.append(s)
    s=state(520,520,physics='S')+startup(520,35)
    s+=c(520,'Awakening energy price','PowerAdd','Time = 0','value = -1500')
    s+=c(520,'Timed transcendence','VarSet','Time = 8','v = 40\nvalue = 720')
    s+=c(520,'Awakening cooldown','VarSet','Time = 8','v = 41\nvalue = 1200')
    s+=effect(520,'Time = 8',8850,0,-40,1.5,24)+c(520,'Transformation feedback','EnvShake','Time = 8','time = 10\nampl = -3')+recover(520);states.append(s)
    s=state(9550,8900,physics='N',body=False)
    s+=c(9550,'Energy follows the charging body','BindToRoot','1','time = 1\npos = 0,-40')
    s+=c(9550,'Aura never blocks the opponent','PlayerPush','1','value = 0')
    s+=c(9550,'Aura is not an extra hurt box','NotHitBy','1','value = SCA\ntime = 1')
    s+=c(9550,'Tall flowing chakra rather than a rigid cage','AngleDraw','1','value = 90\nscale = .36,.42')
    s+=c(9550,'Blue-white chakra','PalFX','1','time = 1\nmul = 80,170,256')
    s+=c(9550,'Translucent glow behind the model','Trans','1','trans = AddAlpha\nalpha = 190,256')
    s+=c(9550,'Keep the body readable','SprPriority','1','value = -2')
    s+=c(9550,'No artificial aura shadow','AssertSpecial','1','flag = NoShadow')
    s+=ctl(9550,'Stop aura immediately on release or interruption','DestroySelf','trigger1 = Root,StateNo != 500\ntrigger2 = Root,Life <= 0\ntrigger3 = RoundState != 2');states.append(s)

def common():
    common=[]
    def put(s):common.append(s)
    put(state(0,0,physics='S',control=1)+c(0,'Neutral','Null','1'))
    for n in [10,11,12]:
        s=state(n,n,'C' if n!=12 else 'S',physics='C' if n!=12 else 'S',control=1)
        if n==11:s+=c(n,'Release crouch','ChangeState','command != "holddown"','value = 0\nctrl = 1')
        else:s+=recover(n)
        put(s)
    s=state(20,None,physics='S',control=1,velocity=None)
    s+=c(20,'Walk forward','VelSet','command = "holdfwd" || AILevel>0','x = Const(velocity.walk.fwd.x)')
    s+=c(20,'Walk backward','VelSet','command = "holdback" && AILevel=0','x = Const(velocity.walk.back.x)')
    s+=c(20,'Walk animation','ChangeAnim','Anim != IfElse(Vel X<0,21,20)+IfElse(Var(40)>0,10000,0)','value = IfElse(Vel X<0,21,20)+IfElse(Var(40)>0,10000,0)')
    s+=recover(20,'AILevel=0 && command != "holdfwd" && command != "holdback"');put(s)
    for n,speed in [(100,7.6),(105,-7.6)]:
        s=state(n,n,physics='N',velocity=f'{speed},0')
        s+=c(n,'Grounded dash to either side','PosSet','1','y = 0')
        s+=c(n,'Maintain the short dash impulse','VelSet','Time < 14',f'x = {speed}\ny = 0')
        s+=c(n,'Short dash wind','PlaySnd','Time = 0','value = S1,30\nchannel = 2')
        s+=c(n,'End the short dash cue','StopSnd','Time = 8','channel = 2')
        s+=c(n,'Dash motion trail','AfterImage','Time = 0','time = 12\nlength = 4\ntimegap = 2\nframegap = 2\npalcontrast = 90,130,180\ntrans = Add')
        s+=recover(n,'Time >= 14');put(s)
    s=state(40,40,physics='S')
    s+=c(40,'Jump impulse','VelSet','Time = 3','x = IfElse(command="holdfwd",3.2,IfElse(command="holdback",-3,0))\ny = -9')
    s+=c(40,'Air control','ChangeState','Time >= 4','value = 50\nctrl = 1');put(s)
    s=state(45,41,'A',physics='A',velocity=None)+c(45,'Double jump','VelSet','Time = 0','y = -7.5')+recover(45,'Time >= 2',True);put(s)
    s=state(50,41,'A',physics='A',control=1,velocity=None)
    s+=c(50,'Descent pose','ChangeAnim','Vel Y>0 && Anim != 44+IfElse(Var(40)>0,10000,0)','value = 44+IfElse(Var(40)>0,10000,0)')
    s+=c(50,'Land','ChangeState','Vel Y>0 && Pos Y>=0','value = 52\nctrl = 1');put(s)
    put(state(52,52,physics='S')+c(52,'Feet on floor','PosSet','1','y = 0')+recover(52))
    # Native families: 120 universal start; 150/151 standing shake/recoil,
    # 152/153 crouching shake/recoil, 154/155 aerial shake/recoil.
    s=state(120,None,'U',physics='U',velocity=None)
    s+=c(120,'Preserve grounded crouch guard','StateTypeSet','StateType=S && command="holddown"','statetype=C\nphysics=C')
    s+=c(120,'Standing guard when down released','StateTypeSet','StateType=C && command!="holddown"','statetype=S\nphysics=S')
    s+=c(120,'Form-aware start pose','ChangeAnim','Time=0','value=120+(StateType=C)+(StateType=A)*2+IfElse(Var(40)>0,10000,0)')
    s+=c(120,'Enter native guard family','ChangeState','Time>=3','value=130+(StateType=C)+(StateType=A)*2\nctrl=0')
    s+=c(120,'Release early guard','ChangeState','command!="holdback"','value=IfElse(StateType=A,50,0)\nctrl=1');put(s)
    for n,typ in [(130,'S'),(131,'C'),(132,'A'),(140,'S'),(141,'C'),(142,'A')]:
        s=state(n,n,typ,physics=typ,control=0 if n<140 else 1,velocity=None if typ=='A' else '0,0')
        if n==130:s+=c(n,'Lower guard while holding down','ChangeState','command = "holddown"','value = 131\nctrl = 0')
        if n==131:s+=c(n,'Raise guard after releasing down','ChangeState','command != "holddown"','value = 130\nctrl = 0')
        if typ=='A':s+=c(n,'Land from aerial guard','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
        s+=recover(n,'command != "holdback"',typ=='A');put(s)
    for n,typ,anim,returnstate in [(150,'S',150,130),(152,'C',151,131),(154,'A',152,132)]:
        put(state(n,anim,typ,'H','N')+c(n,'Finish native guard shake','ChangeState','HitShakeOver',f'value={n+1}\nctrl=0'))
        s=state(n+1,anim,typ,'H',typ,velocity=None)
        s+=c(n+1,'Actual guard knockback','HitVelSet','Time=0','x=1'+('\ny=1' if typ=='A' else ''))
        if typ=='A':s+=c(n+1,'Land from guard recoil','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
        s+=c(n+1,'Guard recovery','ChangeState','HitOver',f'value={returnstate}\nctrl=0');put(s)
    for n,typ,pose in [(5000,'S',5000),(5010,'C',5010),(5020,'A',5020)]:
        s=state(n,pose,typ,'H','N')
        s+=c(n,'Leave shake with real hit velocity','ChangeState','HitShakeOver','value = IfElse(GetHitVar(fall) || GetHitVar(yvel)!=0 || Pos Y<0,5030,5001)')
        put(s)
    s=state(5001,None,move='H',physics='S',velocity=None)+c(5001,'Real horizontal hit velocity','HitVelSet','Time=0','x = 1')+recover(5001,'HitOver');put(s)
    for n in [5011,5030,5035,5040,5050,5070,5071,5080,5081]:
        s=state(n,5030,'A','H','N',velocity=None)
        if n in [5030,5011]:s+=c(n,'Receive real knockback','HitVelSet','Time=0','x = 1\ny = 1')
        s+=c(n,'Gravity during hit fall','VelAdd','1','y = .48')
        s+=c(n,'Touch floor','ChangeState','Pos Y>=0 && Vel Y>0','value = 5100')
        s+=c(n,'Recover non-falling air hit','ChangeState','HitOver && !GetHitVar(fall) && Time>4','value = 50\nctrl = 1');put(s)
    s=state(5100,5100,'L','H','N')+c(5100,'Floor','PosSet','1','y=0')+c(5100,'Fall damage','HitFallDamage','Time=0')+c(5100,'Lying down','ChangeState','Time>=10','value=5110');put(s)
    s=state(5110,5110,'L','H','N')+c(5110,'Floor','PosSet','1','y=0')+c(5110,'Dead','ChangeState','!Alive','value=5150')+c(5110,'Always get up while alive','ChangeState','Time>=28 && Alive','value=5120');put(s)
    s=state(5120,5120,'L',physics='N')+c(5120,'Protected getup','NotHitBy','1','value=SCA\ntime=1')+recover(5120);put(s)
    put(state(5150,5150,'L','H','N')+c(5150,'Stay defeated','Null','1'))
    for n in [5200,5210]:put(state(n,n,'A',physics='A',velocity='-2,-5')+recover(n,'Time>=8',True))
    put(state(5300,5300,physics='S')+recover(5300))
    (CHAR/'common1.cns').write_text('; Shibai common states, finite ground recovery and form-aware animations.\n'+''.join(common))

def commands():
    out='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\ns=s\n[Defaults]\ncommand.time=20\ncommand.buffer.time=4\n'
    def cmd(name,keys,buffer=4):return f'\n[Command]\nname="{name}"\ncommand={keys}\ntime=20\nbuffer.time={buffer}\n'
    for name,button,d,n,cost in MOVES:
        if d in ['F','B']:
            for keys in [f'~D,D{d},{d},{button}',f'~D,{d},{button}',f'/D{d},{button}']:out+=cmd(name,keys)
        else:out+=cmd(name,f'/D,{button}' if d=='D' else button,1 if d=='N' else 4)
    for b in ['a','b','c','x','y','z','s']:out+=cmd(b,b)+cmd('hold_'+b,'/'+b,1)
    for name,keys in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D'),('FF','F,F'),('BB','B,B'),('recovery','a+b')]:out+=cmd(name,keys,1 if keys.startswith('/') else 4)
    out+='\n[Statedef -1]\n'
    for name,button,d,n,cost in MOVES:
        extra='\ntriggerall = command != "holddown"' if d=='N' else ''
        value='IfElse(NumHelper(9600)>0,1211,1210)' if name=='Garra' else str(n)
        out+=ctl(-1,name,'ChangeState',f'triggerall = AILevel=0\ntriggerall = command="{name}"\ntriggerall = StateType!=A\ntriggerall = Power>={costexpr(cost)}{extra}\ntrigger1 = ctrl',f'value={value}')
    out+=ctl(-1,'Awakening down plus Pause','ChangeState','triggerall = AILevel=0\ntriggerall = command="s"\ntriggerall = command="holddown"\ntriggerall = Power>=3000\ntriggerall = Var(40)=0\ntriggerall = Var(41)=0\ntrigger1 = ctrl\ntrigger1 = StateType!=A','value=520')
    out+=ctl(-1,'Xbox A ultimate','ChangeState','triggerall = AILevel=0\ntriggerall = command="x"\ntriggerall = Power>=3000\ntriggerall = StateType!=A\ntrigger1=ctrl','value=3000')
    out+=ctl(-1,'Hold Pause to charge','ChangeState','triggerall = AILevel=0\ntriggerall = command="hold_s"\ntriggerall = command!="holddown"\ntriggerall = Power<3000\ntriggerall = StateType!=A\ntrigger1=ctrl','value=500')
    for button,base,airbase in [('a',200,600),('b',210,610),('c',220,620)]:
        out+=ctl(-1,'Wind combo continuation','ChangeState',f'''triggerall = AILevel=0
triggerall = command="{button}"
triggerall = StateType!=A
triggerall = command!="holddown"
trigger1 = ctrl
trigger2 = StateNo=200 || StateNo=210 || StateNo=220
trigger2 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger2 = Time>=8
trigger3 = StateNo=201 || StateNo=211 || StateNo=221
trigger3 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger3 = Time>=8''',f'value={base}+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))','ignorehitpause=1\n')
        out+=ctl(-1,'Finite aerial wind chain','ChangeState',f'''triggerall = AILevel=0
triggerall = command="{button}"
triggerall = StateType=A
triggerall = Var(12)<3
trigger1=ctrl
trigger2 = StateNo>=600 && StateNo<=622
trigger2 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger2 = Time>=8''',f'value={airbase}+Var(12)','ignorehitpause=1\n')
    for name,n in [('FF',100),('BB',105)]:out+=ctl(-1,name,'ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType=S\ntrigger1=ctrl',f'value={n}')
    # Explicit movement keeps the module standalone in both engines.
    for command,n in [('holdup',40),('holddown',11),('holdfwd',20),('holdback',20)]:
        extra='\ntriggerall=StateType=S\ntriggerall=command!="holdup"\ntriggerall=command!="holddown"' if n==20 else ''
        if n in [11,20]:extra+='\ntriggerall=StateNo<120 || StateNo>155'
        out+=ctl(-1,'Ground movement','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{command}"\ntriggerall=StateType!=A\ntriggerall=StateNo!={n}{extra}\ntrigger1=ctrl',f'value={n}\nctrl={0 if n==40 else 1}')
    out+=ctl(-1,'CPU travel through the placed claw','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=Power>={costexpr(300)}\ntriggerall=NumHelper(9600)>0\ntrigger1=P2BodyDist X>90','value=1211')
    out+=ctl(-1,'CPU claw approach from a distance','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=Power>={costexpr(600)}\ntriggerall=NumHelper(9600)=0\ntrigger1=P2BodyDist X>150','value=1210')
    for n,cost,dist in [(3000,3000,200),(1040,550,240),(1000,300,180)]:out+=ctl(-1,'CPU legal technique','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=Power>={costexpr(cost)}\ntrigger1=P2BodyDist X<{dist}\ntrigger1=Random<8+AILevel*2',f'value={n}')
    out+=ctl(-1,'CPU wind normal','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X<150','value=200')
    out+=ctl(-1,'CPU approach','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X>=150','value=20\nctrl=1')
    (CHAR/'Shibai.cmd').write_text(out)

def system():
    s='\n[Statedef -2]\n'
    for v in [40,41]:s+=c(-2,'Finite awakening timer','VarAdd',f'!IsHelper && Var({v})>0',f'v={v}\nvalue=-1')
    s+=c(-2,'Actual form animation','ChangeAnim','!IsHelper && Var(40)>0 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000\nelem=AnimElemNo(0)')
    s+=c(-2,'Return to robed form','ChangeAnim','!IsHelper && Var(40)=0 && Anim>=10000 && SelfAnimExist(Anim-10000)','value=Anim-10000\nelem=AnimElemNo(0)')
    s+=c(-2,'Strong but bounded damage','AttackMulSet','!IsHelper','value=IfElse(Var(40)>0,1.95,1.2)')
    s+=c(-2,'Transcendent durability','DefenceMulSet','!IsHelper','value=IfElse(Var(40)>0,1.25,1)')
    s+=c(-2,'Aerial count reset','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')
    s+=c(-2,'Charge hum cleanup','StopSnd','StateNo!=500','channel=3')
    for eid in [9551,9552]:s+=c(-2,'Charge particle cleanup','RemoveExplod','!IsHelper && StateNo!=500',f'ID = {eid}')
    s+=effect(-2,'!IsHelper && Var(40)>0 && RoundState=2 && GameTime%30=0',8850,0,-40,.6,16,-2)
    s+=c(-2,'Clean round effects','RemoveExplod','RoundState!=2','')
    return s

def main():
    animations();normals();specials();ultimate();utility();common();commands()
    for n,(poses,hurt,hitbox,loop) in body_actions.items():
        for form in range(2):
            out=f'\n[Begin Action {n+form*10000}]\n'
            if hitbox:out+=f'Clsn1Default: 1\n Clsn1[0] = {hitbox}\n'
            if loop:out+='Loopstart\n'
            for pose,duration in poses:
                if hurt:
                    width,height=Image.open(CHAR/f'assets/sprites/{form}_{pose}.png').size
                    half=min(48,width//2) if pose==23 else 16
                    out+=f'Clsn2: 1\n Clsn2[0] = {-half},{-min(74,height-2)},{half},-1\n'
                out+=f'{form},{pose},0,0,{duration}\n'
            air.append(out)
    constants='''[Data]
life=1300
power=3000
attack=100
defence=125
fall.defence_up=20
liedown.time=28
airjuggle=15
sparkno=2
guard.sparkno=40
KO.echo=0
volume=0
IntPersistIndex=60
FloatPersistIndex=40
[Size]
xscale=1
yscale=1
ground.back=16
ground.front=16
air.back=14
air.front=14
height=78
attack.dist=160
proj.attack.dist=250
head.pos=0,-68
mid.pos=0,-40
shadowoffset=0
draw.offset=0,0
[Velocity]
walk.fwd=2.8
walk.back=-2.5
run.fwd=6.8,0
run.back=-4.5,-4
jump.neu=0,-9
jump.back=-3
jump.fwd=3.2
runjump.back=-3,-9
runjump.fwd=4.5,-9
airjump.neu=0,-7.5
airjump.back=-3
airjump.fwd=3.2
[Movement]
airjump.num=1
airjump.height=35
yaccel=.48
stand.friction=.85
crouch.friction=.82
stand.friction.threshold=2
crouch.friction.threshold=.05
'''
    (CHAR/'Shibai.cns').write_text('; Shibai: playable fan adaptation, not a claim of confirmed manga abilities.\n'+constants+''.join(states)+system())
    (CHAR/'Shibai.air').write_text('; Two distinct body groups. Identical scale and state timing in both forms.\n'+''.join(air))
    (CHAR/'Shibai.def').write_text('''[Info]
name="Shibai"
displayname="Shibai Otsutsuki"
versiondate=10,21,2026
mugenversion=1.1
author="Vahidras (reference models), Codex (fan adaptation)"
localcoord=320,240
pal.defaults=1
[Files]
sprite=Shibai.sff
sound=Shibai.snd
anim=Shibai.air
cmd=Shibai.cmd
cns=Shibai.cns
st=Shibai.cns
stcommon=common1.cns
[Palette Keymap]
a=1
b=1
c=1
x=1
y=1
z=1
a2=1
b2=1
c2=1
x2=1
y2=1
z2=1
''')
    (CHAR/'assets/moves.json').write_text(json.dumps(dict(techniques=MOVES,awakening=dict(ticks=720,full_meter_required=True,cost=1500,technique_cost_multiplier=.6,normal_attack_multiplier=1.2,awakened_attack_multiplier=1.95,projectile_scale_multiplier=1.65,projectile_speed_multiplier=1.15,extra_attacks=AWAKENED_SHOTS),ultimate=dict(cost=3000,budget='min(420,floor(enemy_lifemax*.42))',must_hit=True),canon_note='Wind and thunder inspired by description. No Kokugan, rods or cubes. Claw marks, repulsion and scripted combat remain explicitly requested fan adaptations.'),indent=2)+'\n')
    print('Authored Shibai:',len(air),'actions, both forms and',len(MOVES),'specials')

if __name__=='__main__':main()
