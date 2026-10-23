#!/usr/bin/env python3
"""Jura's own combat: Vaydra poses, ocular shots, growing wood and finite claw travel."""
from pathlib import Path
import json,re
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'JuraShinju'
MOVES=[('Espinas','a','F',1000,350),('Raiz','a','B',1010,450),
 ('Bijudama','b','F',1020,500),('BijudamaCargada','b','B',1030,700),
 ('Garras','c','F',1040,400),('Arbol','c','B',1050,650),
 ('Barrido','a','D',1400,250),('Lanzador','b','D',1410,400),
 ('RafagaOcular','c','D',1420,400),('Francotirador','y','N',1200,250),
 ('Marca','z','N',1210,300),('AsedioOcular','y','D',1430,350),('SalidaGarra','z','D',1440,500)]
air=[];states=[];body_actions={};meta={m['number']:m for m in json.loads((CHAR/'assets/sprites.json').read_text())}
def ctl(n,label,kind,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype = {kind}\n{triggers}\n{params}\n{extra}'
def c(n,label,kind,when,params='',extra=''):return ctl(n,label,kind,'trigger1 = '+when,params,extra)
def costexpr(cost):return f'IfElse(Var(40)>0,{round(cost*.75)},{cost})'
def state(n,anim=None,typ='S',move='I',physics='N',cost=0,velocity='0,0',control=0,body=True):
    s=f'\n[Statedef {n}]\ntype = {typ}\nmovetype = {move}\nphysics = {physics}\nctrl = {control}\n'
    if anim is not None:s+=f'anim = {anim}\n'
    if velocity is not None:s+='velset = '+velocity+'\n'
    if cost:s+='poweradd = -'+costexpr(cost)+'\n'
    return s
def animation(n,poses,hurt=True,hitbox=None,loop=False):body_actions[n]=(poses,hurt,hitbox,loop)
def fxaction(n,g,count,ticks=3,box=None,loop=False,add=True):
    s=f'\n[Begin Action {n}]\n'
    if box:s+=f'Clsn1Default: 1\n Clsn1[0] = {box}\n'
    if n==8800:s+='Clsn2Default: 1\n Clsn2[0] = -30,-30,30,30\n'
    if loop:s+='Loopstart\n'
    for i in range(count):s+=f'{g},{i},0,0,{ticks}'+(',,A' if add else '')+'\n'
    air.append(s)
def posed_action(n,frames,loop_at=None):
    s=f'\n[Begin Action {n}]\nClsn2Default: 1\n Clsn2[0] = -16,-84,16,-1\n'
    for i,(g,no,x,y,ticks) in enumerate(frames):
        if i==loop_at:s+='Loopstart\n'
        s+=f'{g},{no},{x},{y},{ticks}\n'
    air.append(s)
def effect(n,when,anim,x=0,y=0,scale=1,seconds=-2,priority=3):
    return c(n,'Visible technique effect','Explod',when,f'anim = {anim}\npostype = P1\npos = {x},{y}\nscale = {scale},{scale}\nremovetime = {seconds}\nownpal = 1\nsprpriority = {priority}\npausemovetime = 999\nsupermovetime = 999\nremoveongethit = 0')
def startup(n,sound=21):
    return c(n,'Audible technique activation','PlaySnd','Time = 0',f'value = S1,{sound}\nchannel = 4','persistent = 0\nignorehitpause = 1\n')+c(n,'Brief technique focus','SuperPause','Time = 0','time = 10\nmovetime = 0\nanim = -1\nsound = -1\ndarken = 1\nunhittable = 0\np2defmul = 1\npoweradd = 0','persistent = 0\nignorehitpause = 1\n')+effect(n,'Time = 0',8710,10,-55,.75,10)
def recover(n,when='AnimTime = 0',aerial=False):return c(n,'Return to movement','ChangeState',when,f'value = {50 if aerial else 0}\nctrl = 1')
def projectile(n,tick,anim,damage,x=17,y=-65,vx=14,vy=0,fin=False,low=False,pid=None,lifetime=30,scale=1,normal=False):
    return c(n,'Visible physical projectile','Projectile',f'Time = {tick}',f'''projID = {n if pid is None else pid}
projanim = {anim}
projhitanim = 8820
projremanim = 8700
projremove = 1
projremovetime = {lifetime}
projhits = 1
projedgebound = 25
projpriority = 2
projscale = {scale},{scale}
offset = {x},{y}
velocity = {vx},{vy}
attr = {'A' if 600<=n<=622 else 'S'}, {'NP' if normal else 'SP'}
damage = {damage},{0 if normal else 5}
guardflag = {'L' if low else 'MA'}
hitflag = MAF
priority = 5,Hit
pausetime = 0,{12 if fin else 8}
sparkno = S8700
guard.sparkno = -1
hitsound = S1,{41 if anim in [8600,8601,8602] else 42}
guardsound = S1,9
ground.type = {'Low' if low else 'High'}
ground.hittime = {28 if fin else 33}
ground.slidetime = 20
ground.velocity = {-6 if fin else -.7},{-7 if fin else 0}
air.hittime = 30
air.velocity = {-5 if fin else -.7},{-5 if fin else -1.5}
fall = {int(fin)}
fall.recover = 1
fall.recovertime = 45
getpower = {25 if normal else 0},0
givepower = 12,8
envshake.time = {8 if fin else 3}
envshake.ampl = {-4 if fin else -1}''')
def hit(n,tick,damage,fin=False,low=False,airborne=False):
    return c(n,'Contact sound','PlaySnd',f'Time = {tick}','value = S1,0\nchannel = 1')+c(n,'Actual taijutsu contact','HitDef',f'Time = {tick}',f'''attr = {'A' if airborne else 'C' if low else 'S'}, {'SA' if n>=1000 else 'NA'}
damage = {damage},0
animtype = {'Up' if fin else 'Medium'}
guardflag = {'L' if low else 'MA'}
hitflag = MAF
priority = 5,Hit
pausetime = {7 if fin else 4},{11 if fin else 7}
sparkno = S8700
guard.sparkno = -1
sparkxy = 0,-45
hitsound = S1,{19 if fin else 7}
guardsound = S1,9
ground.type = {'Low' if low else 'High'}
ground.hittime = 27
ground.slidetime = 18
ground.velocity = {-5 if fin else -.4},{-7 if fin else 0}
air.hittime = 30
air.velocity = {-5 if fin else -.4},{-5 if fin else -1.5}
fall = {int(fin)}
fall.recover = 1
fall.recovertime = 45
getpower = {30 if n<1000 else 0},0
givepower = 12,8
envshake.time = {8 if fin else 2}
envshake.ampl = {-4 if fin else -1}''')
def eye_aim(n,tick,speed):
    when=f'Time = {tick}'
    s=c(n,'Safe ground target height','VarSet',when,'v=24\nvalue=60')
    s+=c(n,'Read opponent body height','VarSet',when+' && NumEnemy>0','v=24\nvalue=Floor(EnemyNear,Const(size.height))')
    s+=c(n,'Clamp minimum target height','VarSet',when+' && Var(24)<12','v=24\nvalue=12')
    s+=c(n,'Clamp maximum ground aim height','VarSet',when+' && Var(24)>64','v=24\nvalue=64')
    s+=c(n,'Grounded body aim point','VarSet',when,'fv=14\nvalue=Var(24)*.35')
    s+=c(n,'Lower aim against crouching opponents','VarSet',when+' && NumEnemy>0 && EnemyNear,StateType=C','fv=14\nvalue=Var(24)*.15')
    s+=c(n,'Avoid skipping close small bodies','VarSet',when,f'fv=11\nvalue=IfElse(P2Dist X<70,5,{speed})')
    s+=c(n,'Aim once from eye toward ground body','VarSet',when,'fv=12\nvalue=(65-FVar(14))*FVar(11)/IfElse(P2Dist X>26,P2Dist X-18,8)')
    return s

def ball(n,tick,damage,size=.6,speed=8,fin=True,lifetime=70):
    s=eye_aim(n,tick,speed)+c(n,'Orb damage','VarSet',f'Time = {tick}',f'v = 30\nvalue = {damage}')
    s+=c(n,'Orb velocity','VarSet',f'Time = {tick}','v = 31\nvalue = Floor(FVar(11))')
    s+=c(n,'Orb knockback','VarSet',f'Time = {tick}',f'v = 32\nvalue = {int(fin)}')
    s+=c(n,'Orb lifetime','VarSet',f'Time = {tick}',f'v = 33\nvalue = {lifetime}')
    s+=c(n,'Orb scale','VarSet',f'Time = {tick}',f'fv = 10\nvalue = {size}')
    s+=c(n,'Eye actually emits the Bijudama','Helper',f'Time = {tick} && NumHelper(9300)<3','helpertype = Normal\nname = "Bijudama ocular"\nID = 9300\nstateno = 9300\npostype = P1\npos = 18,-65\nfacing = 1\nkeyctrl = 0\nownpal = 1')
    s+=c(n,'Bijudama release','PlaySnd',f'Time = {tick}','value = S1,40\nchannel = 1')
    return s

def animations():
    animation(0,[(0,10),(1,10),(2,10)],loop=True)
    for n in [5,120,122,130,132,140,142,150,152]:animation(n,[(13,6)])
    for n in [6,10,11,12,121,131,141,151]:animation(n,[(9,5)])
    for n,poses in [(20,[28,29,30]),(21,[30,29,28]),(100,[28,29,30]),(105,[30,29,28])]:animation(n,[(p,4 if n<100 else 3) for p in poses],loop=True)
    animation(40,[(33,4)])
    for n in range(41,48):animation(n,[(34 if n<44 else 35,6)])
    animation(52,[(34,4),(33,3),(0,3)])
    for n in [170,190]:animation(n,[(0,8),(1,8),(2,8)],loop=n!=190)
    posed_action(180,[(0,24,0,0,8),(0,19,0,0,12),(0,20,0,0,12),(0,19,0,0,10),(0,19,0,0,20),(0,20,0,0,20)],loop_at=4)
    # Move the prop up from the cloak while the original hands rise; then
    # hold it at the palm. The character drawing is never replaced.
    air.append('\n[Begin Action 8960]\n3,0,-7,20,3\n3,0,-5,14,3\n3,0,-2,7,3\n3,0,0,0,3\n3,1,0,0,12\n3,2,0,0,10\nLoopstart\n3,2,0,0,20\n3,3,0,0,20\n')
    animation(500,[(19,8),(20,8)],loop=True);animation(520,[(24,12),(0,60),(24,12),(0,12)])
    for n in [5000,5001,5002,5005,5006,5007,5010,5011,5012,5015,5016,5017,5020,5021,5022,5025,5026,5027,5030,5035,5040,5050,5051,5052,5060,5061,5062,5070,5080,5090,5200,5210]:animation(n,[(3,5),(4,5),(5,5)])
    for n in [5100,5110,5140,5150,5160,5170]:animation(n,[(8,6)])
    animation(5120,[(8,4),(9,6),(33,5),(0,3)]);animation(5300,[(3,6),(0,6)]);animation(5500,[(0,1)])
    for g,count in [(8700,4),(8710,4),(8720,6)]:fxaction(g,g,count,2)
    for g,count,ticks,box,loop,add in [(8600,4,4,'-12,-80,12,-1',True,False),(8601,3,5,'-48,-95,48,-1',True,False),(8602,2,8,'-60,-145,60,-1',True,False),(8603,3,4,'-45,-20,45,20',False,False),(8604,1,12,None,False,False),(8605,3,3,None,False,True),(8606,1,5,'-5,-5,5,5',True,False),(8800,10,3,'-30,-30,30,30',True,True),(8810,7,2,None,False,True),(8820,5,3,None,False,True),(8830,0,2,None,False,True),(8840,22,2,None,True,True),(8880,1,6,None,True,False),(8881,1,6,None,True,False),(8900,24,2,None,True,True),(8910,5,2,None,False,True),(8920,9,2,None,False,True)]:
        if g==8830:fxaction(8830,8840,22,2,None,False,True)
        else:fxaction(g,g,count,ticks,box,loop,add)
    # An opaque dark core with a separate luminous ring; no giant stone sphere.
    fxaction(8841,8800,1,3,'-30,-30,30,30',True,False)
    fxaction(8842,8800,1,3,'-12,-12,12,12',True,False)
    fxaction(8940,8940,1,8,None,True,False)
    air.append('\n[Begin Action 8950]\n8950,0,0,0,12\n8950,1,0,0,30\n8950,2,0,0,18\n8950,3,0,0,16\n')

def normals():
    for family,base in enumerate([200,210,220]):
        for stage in range(3):
            n=base+stage;fin=stage==2;attack=[11,12,18][stage] if family==0 else [16,18,14][stage] if family==1 else [13,14,16][stage]
            animation(n,[(10 if family==0 else 15,3),(attack,6),(13,5),(0,8)],hitbox=f'12,{-38 if family==2 else -68},65,{-4 if family==2 else -28}')
            s=state(n,n,move='A',physics='S',velocity='2.5,0')+hit(n,3,[48,62,95][stage],fin,low=family==2)
            s+=c(n,'Stop the approach','VelSet','Time >= 8','x = 0')
            if fin:
                s+=projectile(n,12,8600 if family==1 else 8606,25,x=50 if family==1 else 18,y=0 if family==1 else -58,vx=0 if family==1 else 10,fin=True,lifetime=18,scale=.65 if family==1 else 1.2,normal=True)
            s+=recover(n);states.append(s)
    for family,base in enumerate([600,610,620]):
        for stage in range(3):
            n=base+stage;animation(n,[(31,3),([32,16,18][stage],6),(34,10)],hitbox='8,-68,64,-12')
            s=state(n,n,'A','A','A',velocity=None)+c(n,'Finite air chain','VarAdd','Time = 0','v = 12\nvalue = 1')+hit(n,3,42+stage*14,stage==2,airborne=True)
            s+=c(n,'Brief lift on actual contact','VelSet','MoveHit = 1','y = -1.5','persistent = 0\nignorehitpause = 1\n')
            s+=c(n,'Land safely','ChangeState','Vel Y>0 && Pos Y>=0','value = 52\nctrl = 1')+recover(n,aerial=True);states.append(s)

def techniques():
    specs={1000:(350,19,[(10,8600,55,65),(20,8600,55,110),(30,8600,80,155)]),
           1010:(450,21,[(15,8601,155,90)]),1050:(650,21,[(18,8602,185,115)]),
           1040:(400,25,[(12,8603,135,55)]),1410:(400,19,[(12,8600,135,50)])}
    for n,(cost,pose,shots) in specs.items():
        end=max(x[0] for x in shots)+28;animation(n,[(pose,8),(pose+1 if pose in [19,21,25] else pose,end-16),(0,8)])
        s=state(n,n,move='A',cost=cost,physics='S')+startup(n)
        for i,(tick,anim,damage,x) in enumerate(shots):
            s+=c(n,'Wood or claw release','PlaySnd',f'Time = {tick}',f'value = S1,{41 if anim!=8603 else 32}\nchannel = 1')
            s+=projectile(n,tick,anim,damage,x=x,y=-27 if anim==8603 else 0,vx=7 if anim==8603 else 0,fin=i==len(shots)-1,low=n==1000,pid=n+i,lifetime=28 if anim==8603 else 35,scale=.85 if anim==8603 else 1)
        s+=recover(n);states.append(s)
    for n,cost,size,damage,release in [(1020,500,.65,145,15),(1030,700,1.1,225,30)]:
        animation(n,[(23,8),(23,release+10),(0,12)])
        s=state(n,n,move='A',cost=cost,physics='S')+startup(n)+effect(n,'Time = 5',8605,13,-65,.55,12)
        s+=ball(n,release,damage,size,8 if n==1020 else 6)
        if n==1020:
            extra=ball(n,30,65,.4,10);s+=extra.replace('trigger1 = ', 'triggerall = Var(40)>0\ntrigger1 = ')
        s+=recover(n);states.append(s)
    for n,cost,times in [(1200,250,[10]),(1420,400,[10,20,30])]:
        animation(n,[(27,8),(27,max(times)+10),(0,10)])
        s=state(n,n,move='A',physics='S',cost=cost)+startup(n)+effect(n,'Time = 4',8605,13,-65,.38,10)
        for i,t in enumerate(times):
            s+=ball(n,t,115 if n==1200 else 55,.38 if n==1200 else .32,18 if n==1200 else 15,i==len(times)-1,30)
            s+=c(n,'Ocular shot crack','PlaySnd',f'Time = {t}','value = S1,42\nchannel = 1')
            s+=effect(n,f'Time = {t}',8605,18,-65,.35,8)
        s+=recover(n);states.append(s)
    animation(1400,[(9,4),(16,7),(9,7),(0,8)],hitbox='5,-30,68,-2')
    states.append(state(1400,1400,move='A',cost=250,physics='S',velocity='4,0')+startup(1400)+hit(1400,4,115,True,True)+recover(1400))
    animation(1430,[(24,10),(23,48),(24,10),(0,8)])
    s=state(1430,1430,move='A',physics='S',cost=350)+startup(1430)
    s+=effect(1430,'Time=5',8605,13,-65,.5,12)
    for i,t in enumerate([12,26,40]):s+=ball(1430,t,70 if i==2 else 50,.42,10,i==2,35)
    s+=recover(1430);states.append(s)

def claw_helper(n,when,x=0):return c(n,'Original crossed claw bands','Helper',when,f'helpertype = Normal\nname = "Bandas de garra"\nID = 9601\nstateno = 9601\npostype = P1\npos = {x},0\nfacing = 1\nownpal = 1\nkeyctrl = 0')
def claws():
    animation(1210,[(25,7),(26,8),(0,10)])
    s=state(1210,1210,cost=300,physics='S')+startup(1210)
    s+=c(1210,'Place a physical ground mark','Helper','Time = 6','helpertype = Normal\nname = "Marca de garra"\nID = 9600\nstateno = 9600\npostype = P1\npos = 125,0\nfacing = 1\nownpal = 1\nkeyctrl = 0')+recover(1210);states.append(s)
    for n,cost,retreat in [(1211,300,False),(1440,500,True)]:
        animation(n,[(25,8),(26,10),(14,12),(0,10)],hitbox='10,-74,82,-4')
        s=state(n,n,move='A',physics='N',cost=cost)+startup(n)+claw_helper(n,'Time = 3')
        s+=c(n,'Enter the mark','AssertSpecial','Time>=10 && Time<18','flag = Invisible')
        s+=c(n,'Travel without pushing bodies','PlayerPush','Time>=8 && Time<=18','value = 0')
        if not retreat:
            s+=c(n,'Read saved mark','VarSet','Time=0 && NumHelper(9600)>0','v = 22\nvalue = Floor(Helper(9600),Pos X)')
            s+=c(n,'Travel to mark, never enemy coordinates','PosSet','Time=14','x = Var(22)')
            s+=c(n,'Face opponent after exit','Turn','Time=15 && P2Dist X<0')
        else:s+=claw_helper(n,'Time = 3',-80)+c(n,'Finite retreat','PosAdd','Time=14','x = -80')
        s+=claw_helper(n,'Time = 15')+c(n,'Claw travel sound','PlaySnd','Time = 14','value = S1,32\nchannel = 1')
        s+=projectile(n,22,8603,150,x=40,y=-35,vx=7,fin=True,lifetime=24,scale=.65)+recover(n);states.append(s)
    for n in [9600,9601]:
        s=state(n,8880 if n==9600 else 8881,physics='N')
        s+=c(n,'No push','PlayerPush','1','value = 0')+c(n,'No hurt box','NotHitBy','1','value = SCA\ntime = 1')+c(n,'No extra shadow','AssertSpecial','1','flag = NoShadow')
        s+=c(n,'Native flat mark and crossed bands','AngleDraw','1','value = 0\nscale = 1,1' if n==9600 else 'value = 0\nscale = 1,1.45')
        s+=c(n,'Band layer','SprPriority','1',f'value = {-2 if n==9600 else 3}')
        expiry='trigger1 = Time>=600\ntrigger2 = RoundState!=2\ntrigger3 = Root,StateNo=1211\ntrigger3 = Root,Time>=14' if n==9600 else 'trigger1 = Time>=36\ntrigger2 = RoundState!=2'
        s+=ctl(n,'Finite mark lifetime','DestroySelf',expiry);states.append(s)

def orbs():
    s=state(9300,8841,'A','A','N')
    s+=c(9300,'Read damage','VarSet','Time=0','v=0\nvalue=Parent,Var(30)')+c(9300,'Read knockback','VarSet','Time=0','v=1\nvalue=Parent,Var(32)')+c(9300,'Read velocity','VarSet','Time=0','v=2\nvalue=Parent,Var(31)')+c(9300,'Read size','VarSet','Time=0','fv=0\nvalue=Parent,FVar(10)')
    s+=c(9300,'Read downward aim','VarSet','Time=0','fv=1\nvalue=Parent,FVar(12)')+c(9300,'Read finite lifetime','VarSet','Time=0','v=3\nvalue=Parent,Var(33)')
    s+=c(9300,'Collision follows visible orb size','ChangeAnim','Time=0','value=IfElse(FVar(0)<=.5,8842,8841)')
    s+=c(9300,'Stable orb scale','AngleDraw','1','value=0\nscale=FVar(0),FVar(0)')+c(9300,'Purple-black ocular chakra','PalFX','1','time=1\ncolor=0\nmul=22,4,36')
    s+=c(9300,'Violet chakra rim','Explod','Time=0','anim=8840\nID=9309\npostype=P1\npos=0,0\nbindtime=-1\nscale=FVar(0)*.36,FVar(0)*.36\nremovetime=70\nsprpriority=3\nownpal=1\nremoveongethit=1')
    s+=c(9300,'Actual orb velocity','VelSet','1','x=Var(2)\ny=FVar(1)')+c(9300,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9300,'No push','PlayerPush','1','value=0')
    s+=c(9300,'Root power applies to the projectile','AttackMulSet','1','value=IfElse(Root,Var(40)>0,1.5,1.15)')
    s+=c(9300,'Visible orb contact','HitDef','Time=0','attr=A,SP\ndamage=Var(0),7\nguardflag=MA\nhitflag=MAF\npriority=5,Hit\npausetime=0,10\nsparkno=S8820\nguard.sparkno=-1\nhitsound=S1,41\nguardsound=S1,9\nground.type=High\nground.hittime=30\nground.slidetime=20\nground.velocity=-6,IfElse(Var(1),-7,0)\nair.velocity=-5,-5\nfall=Var(1)\nfall.recover=1\nfall.recovertime=45\ngetpower=0,0\ngivepower=15,10\nenvshake.time=9\nenvshake.ampl=-4')
    s+=c(9300,'Projectile trade','HitOverride','1','attr=SCA,NP,SP,HP\nstateno=9301\ntime=1')
    s+=c(9300,'Remove rim after contact','RemoveExplod','MoveContact || Time>=Var(3)','ID=9309')+c(9300,'Burst after contact','ChangeState','MoveContact || Time>=Var(3)','value=9301');states.append(s)
    s=state(9301,8820,'A',physics='N')+c(9301,'Orb burst sound','PlaySnd','Time=0','value=S1,41\nchannel=1')+c(9301,'Safe final effect','DestroySelf','Time>=15');states.append(s)

def utility():
    for n in [170,180,190]:
        s=state(n,n,physics='S')+c(n,'Round pose','Null','1')
        if n==190:s+=c(n,'Intro','AssertSpecial','Time<22','flag=Intro')+recover(n,'Time>=24')
        if n==180:
            s+=c(180,'Book prop held by original sprite hands','Helper','Time=8','helpertype=Normal\nname="Libro de Jura"\nID=9570\nstateno=9570\npostype=P1\npos=23,-48\nownpal=1\nkeyctrl=0')
            s+=ctl(180,'Draw and open the book','PlaySnd','trigger1=Time=20\ntrigger2=Time=32','value=S1,44\nchannel=6\nvolumescale=75')
            s+=c(180,'Turn a page while reading','PlaySnd','Time>=64 && Time%80=64','value=S1,44\nchannel=6\nvolumescale=45')
        states.append(s)
    s=state(9570,8960,physics='N')+c(9570,'Book follows original palm','BindToRoot','1','time=1\npos=23,-48')
    s+=c(9570,'Book is a visual prop','PlayerPush','1','value=0')+c(9570,'Book has no shadow','AssertSpecial','1','flag=NoShadow')+c(9570,'Book in front of the palm','SprPriority','1','value=3')
    s+=c(9570,'Remove book when victory ends','DestroySelf','Root,StateNo!=180','');states.append(s)
    s=state(500,500,physics='S')+c(500,'Charge real energy','PowerAdd','1','value=22')+c(500,'Charge hum','PlaySnd','Time=0','value=S1,4\nchannel=3\nloop=1')
    s+=c(500,'Animated green chakra','Helper','Time=0','helpertype=Normal\nname="Chakra del Juubi"\nID=9550\nstateno=9550\npostype=P1\npos=0,-44\nownpal=1\nkeyctrl=0')
    s+=c(500,'Pressure ring','Explod','Time%12=2','anim=8910\nID=9551\npostype=P1\npos=0,-1\nscale=.34,.25\nremovetime=-2\nsprpriority=-1\nownpal=1\nremoveongethit=1')
    s+=ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=65','value=0\nctrl=1');states.append(s)
    s=state(9550,8900,physics='N')+c(9550,'Follow charge','BindToRoot','1','time=1\npos=0,-44')+c(9550,'Energy envelope','AngleDraw','1','value=90\nscale=.34,.4')+c(9550,'Green Juubi chakra','PalFX','1','time=1\ncolor=0\nmul=60,256,90')+c(9550,'Additive energy','Trans','1','trans=AddAlpha\nalpha=180,256')+c(9550,'Behind body','SprPriority','1','value=-2')+c(9550,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9550,'No push','PlayerPush','1','value=0')+ctl(9550,'Charge aura cleanup','DestroySelf','trigger1=Root,StateNo!=500\ntrigger2=Root,Life<=0\ntrigger3=RoundState!=2');states.append(s)
    s=state(520,520,physics='S')+startup(520,35)+c(520,'Awakening price','PowerAdd','Time=0','value=-1500')
    s+=c(520,'Living wood encloses the body','Helper','Time=8','helpertype=Normal\nname="Regeneracion Shinju"\nID=9560\nstateno=9560\npostype=P1\npos=0,0\nownpal=1\nkeyctrl=0')
    s+=c(520,'Temporary chakra amplification','VarSet','Time=24','v=40\nvalue=720')+c(520,'Awakening cooldown','VarSet','Time=24','v=41\nvalue=1200')
    s+=c(520,'Regenerate inside the living tree','LifeAdd','Time>=24 && Time<84 && Time%3=0 && Alive && Life<LifeMax','value=9')
    s+=ctl(520,'Growing and opening wood','PlaySnd','trigger1=Time=12\ntrigger2=Time=52','value=S1,41\nchannel=5\nvolumescale=50')+recover(520);states.append(s)
    s=state(9560,8950,physics='N')+c(9560,'Cocoon follows the body','BindToRoot','1','time=1\npos=0,0')
    s+=c(9560,'Regenerative roots in front','SprPriority','1','value=3')+c(9560,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9560,'No push','PlayerPush','1','value=0')
    s+=ctl(9560,'Cocoon finishes or breaks on interruption','DestroySelf','trigger1=AnimTime=0\ntrigger2=Root,StateNo!=520\ntrigger3=RoundState!=2');states.append(s)

def ultimate():
    animation(3000,[(23,8),(27,12),(0,22)])
    s=state(3000,3000,move='A',physics='S')+c(3000,'Three bars even on miss','PowerAdd','Time=0','value=-3000')+startup(3000)+effect(3000,'Time=4',8605,13,-65,.6,12)
    s+=eye_aim(3000,10,11)
    s+=c(3000,'Ocular opening must physically hit','Projectile','Time=10','projID=3000\npausemovetime=180\nprojanim=8606\nprojhitanim=8700\nprojremanim=8700\nprojremovetime=22\nprojhits=1\nprojremove=1\nprojscale=1.5,1.5\noffset=18,-65\nvelocity=FVar(11),FVar(12)\nattr=S,HP\ndamage=0,0\nguardflag=MA\nhitflag=M\npausetime=0,0\nsparkno=S8700\nhitsound=S1,42\nguardsound=S1,9\nground.hittime=260\nground.velocity=0,0\np2stateno=3010\nID=3000\ngetpower=0,0\ngivepower=0,0')
    s+=c(3000,'Only fresh contact confirms','ChangeState','Time>=10 && NumTarget(3000)>0 && ProjHitTime(3000)>=0 && ProjHitTime(3000)<=2','value=3001')+recover(3000,'Time>=58');states.append(s)
    frames=[(0,19,0,0,6),(0,20,0,0,6)]
    frames += [(2,0,0,-round((i+1)*96/10),2) for i in range(10)]
    frames += [(2,0,0,-96,108)]
    frames += [(2,0,0,-round(i*96/10),2) for i in range(9,-1,-1)]
    frames += [(0,0,0,0,6)]
    posed_action(3001,frames)
    s=state(3001,3001,physics='N')+c(3001,'Bounded confirmed sequence','Pause','Time=0','time=152\nmovetime=152\npausebg=1')+c(3001,'Protect only the confirmed animation','NotHitBy','1','value=SCA\ntime=1')
    s+=c(3001,'Dim background','BGPalFX','Time=0','time=152\nmul=75,95,80')+c(3001,'Bind only hit target','TargetBind','Time<150 && NumTarget(3000)>0','ID=3000\ntime=1\npos=145,0')
    s+=c(3001,'Life-relative damage budget','VarSet','Time=0 && NumTarget(3000)>0','v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,450,Floor((Target(3000),LifeMax)*.45))')
    s+=c(3001,'Grow a throne under the seated body','Helper','Time=4','helpertype=Normal\nname="Trono de raices"\nID=9540\nstateno=9540\npostype=P1\npos=0,0\nkeyctrl=0\nownpal=1\npausemovetime=170\nsupermovetime=170')
    s+=c(3001,'Charge the ocular sphere from the raised seat','Helper','Time=32','helpertype=Normal\nname="Bijudama del Diez Colas"\nID=9530\nstateno=9530\npostype=P1\npos=32,-146\nkeyctrl=0\nownpal=1\npausemovetime=170\nsupermovetime=170')
    s+=c(3001,'Growing wood sound','PlaySnd','Time=4','value=S1,41\nchannel=5\nvolumescale=65')
    s+=c(3001,'Ocular chakra roar','PlaySnd','Time=32','value=S1,43\nchannel=5')+effect(3001,'Time=32',8605,13,-146,.45,18)
    for i,t in enumerate([80,94,108,122,136]):
        s+=effect(3001,f'Time={t}',8820,145,'-FVar(14)',1.1 if i==4 else .6,16,6)
        s+=effect(3001,f'Time={t}',8830,145,'-FVar(14)',.6 if i==4 else .32,16,5)
        amount='-(Var(20)-Floor(Var(20)/5)*4)' if i==4 else '-Floor(Var(20)/5)'
        s+=c(3001,'Confirmed bounded damage','TargetLifeAdd',f'Time={t} && NumTarget(3000)>0',f'ID=3000\nvalue={amount}\nabsolute=1\nkill=1')+c(3001,'Impact sound','PlaySnd',f'Time={t}','value=S1,41\nchannel=1')+c(3001,'Impact feedback','EnvShake',f'Time={t}','time=7\nfreq=65\nampl=-5')
    s+=c(3001,'Safe release','TargetState','Time=150 && NumTarget(3000)>0','ID=3000\nvalue=3011')+recover(3001,'Time>=166');states.append(s)
    s=state(3010,move='H',physics='N')+c(3010,'Victim keeps own graphics','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Safety release','SelfState','trigger1=Time>260\ntrigger2=NumEnemy=0\ntrigger3=Time>12 && EnemyNear,StateNo!=3001','value=5050\nctrl=0');states.append(s)
    states.append(state(3011,typ='A',move='H',physics='N',velocity='-7,-6')+c(3011,'Victim own fall state','SelfState','1','value=5050\nctrl=0'))
    s=state(9530,8841,'A',physics='N')+c(9530,'Dark ocular core','PalFX','1','time=1\ncolor=0\nmul=22,4,36')
    s+=c(9530,'Sphere growth from the eye','AngleDraw','1','value=0\nscale=.15+IfElse(Time<24,Time,24)*.04,.15+IfElse(Time<24,Time,24)*.04')
    s+=c(9530,'Charge at the elevated eye','BindToRoot','Time<24','time=1\npos=32,-146')
    s+=c(9530,'Diagonal shot toward the confirmed body','VelSet','Time>=24','x=113.0/24\ny=(146-(Root,FVar(14)))/24')
    s+=c(9530,'Living violet rim','Explod','Time%4=0','anim=8840\npostype=P1\npos=0,0\nbindtime=-1\nscale=(.15+IfElse(Time<24,Time,24)*.04)*.36,(.15+IfElse(Time<24,Time,24)*.04)*.36\nremovetime=5\nsprpriority=4\nownpal=1\npausemovetime=170')
    s+=c(9530,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9530,'No push','PlayerPush','1','value=0')+ctl(9530,'Finite cinematic sphere','DestroySelf','trigger1=Time>=48\ntrigger2=Root,StateNo!=3001');states.append(s)
    s=state(9540,8940,physics='N')+c(9540,'Throne stays grounded','BindToRoot','1','time=1\npos=0,0')
    s+=c(9540,'Roots grow then withdraw','AngleDraw','1','value=0\nscale=IfElse(Time<28,.1+Time*.9/28,IfElse(Time<136,1,IfElse(Time<160,(160-Time)/24.0,.01))),IfElse(Time<28,.1+Time*.9/28,IfElse(Time<136,1,IfElse(Time<160,(160-Time)/24.0,.01)))')
    s+=c(9540,'Throne behind the seated caster','SprPriority','1','value=-2')+c(9540,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9540,'No push','PlayerPush','1','value=0')
    s+=ctl(9540,'Finite throne lifetime','DestroySelf','trigger1=Time>=160\ntrigger2=Root,StateNo!=3001');states.append(s)

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
    s+=c(20,'Walk animation','ChangeAnim','Anim != IfElse(Vel X<0,21,20)','value = IfElse(Vel X<0,21,20)')
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
    s+=c(50,'Descent pose','ChangeAnim','Vel Y>0 && Anim != 44','value = 44')
    s+=c(50,'Land','ChangeState','Vel Y>0 && Pos Y>=0','value = 52\nctrl = 1');put(s)
    put(state(52,52,physics='S')+c(52,'Feet on floor','PosSet','1','y = 0')+recover(52))
    # Native families: 120 universal start; 150/151 standing shake/recoil,
    # 152/153 crouching shake/recoil, 154/155 aerial shake/recoil.
    s=state(120,None,'U',physics='U',velocity=None)
    s+=c(120,'Preserve grounded crouch guard','StateTypeSet','StateType=S && command="holddown"','statetype=C\nphysics=C')
    s+=c(120,'Standing guard when down released','StateTypeSet','StateType=C && command!="holddown"','statetype=S\nphysics=S')
    s+=c(120,'Form-aware start pose','ChangeAnim','Time=0','value=120+(StateType=C)+(StateType=A)*2')
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
    (CHAR/'JuraShinju_common.cns').write_text('; Jura common states, derived from project native MUGEN guard and recovery.\n'+''.join(common))


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
    for name,b,d,n,cost in MOVES:
        extra='\ntriggerall=command!="holddown"' if d=='N' else ''
        value='IfElse(NumHelper(9600)>0,1211,1210)' if name=='Marca' else str(n)
        out+=ctl(-1,name,'ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=Power>={costexpr(cost)}{extra}\ntrigger1=ctrl',f'value={value}')
    out+=ctl(-1,'Awakening','ChangeState','triggerall=AILevel=0\ntriggerall=command="s"\ntriggerall=command="holddown"\ntriggerall=Power>=3000\ntriggerall=Var(40)=0\ntriggerall=Var(41)=0\ntrigger1=ctrl\ntrigger1=StateType!=A','value=520')
    out+=ctl(-1,'Xbox A ultimate','ChangeState','triggerall=AILevel=0\ntriggerall=command="x"\ntriggerall=Power>=3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=3000')
    out+=ctl(-1,'Hold Pause to charge','ChangeState','triggerall=AILevel=0\ntriggerall=command="hold_s"\ntriggerall=command!="holddown"\ntriggerall=Power<3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=500')
    for b,base,airbase in [('a',200,600),('b',210,610),('c',220,620)]:
        out+=ctl(-1,'Ground combo','ChangeState',f'''triggerall=AILevel=0
triggerall=command="{b}"
triggerall=StateType!=A
triggerall=command!="holddown"
trigger1=ctrl
trigger2=StateNo=200 || StateNo=210 || StateNo=220
trigger2=MoveHit
trigger2=Time>=6
trigger3=StateNo=201 || StateNo=211 || StateNo=221
trigger3=MoveHit
trigger3=Time>=6''',f'value={base}+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))','ignorehitpause=1\n')
        out+=ctl(-1,'Finite aerial chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=StateType=A\ntriggerall=Var(12)<3\ntrigger1=ctrl\ntrigger2=StateNo>=600 && StateNo<=621\ntrigger2=MoveHit\ntrigger2=Time>=6',f'value={airbase}+Var(12)','ignorehitpause=1\n')
    for name,n in [('FF',100),('BB',105)]:out+=ctl(-1,'Double-tap dash','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType=S\ntrigger1=ctrl',f'value={n}')
    for command,n in [('holdup',40),('holddown',11),('holdfwd',20),('holdback',20)]:
        extra='\ntriggerall=StateType=S\ntriggerall=command!="holdup"\ntriggerall=command!="holddown"' if n==20 else ''
        if n in [11,20]:extra+='\ntriggerall=StateNo<120 || StateNo>155'
        out+=ctl(-1,'Ground movement','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{command}"\ntriggerall=StateType!=A\ntriggerall=StateNo!={n}{extra}\ntrigger1=ctrl',f'value={n}\nctrl={0 if n==40 else 1}')
    for n,cost,dist in [(1211,300,999),(1210,600,999),(3000,3000,190),(1200,250,310),(1020,500,230),(1000,350,170)]:
        extra='\ntriggerall=NumHelper(9600)>0\ntriggerall=P2BodyDist X>90' if n==1211 else '\ntriggerall=NumHelper(9600)=0\ntriggerall=P2BodyDist X>170' if n==1210 else ''
        out+=ctl(-1,'CPU legal technique','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=Power>={costexpr(cost)}{extra}\ntrigger1=P2BodyDist X<{dist}\ntrigger1=Random<8+AILevel*2',f'value={n}')
    out+=ctl(-1,'CPU taijutsu','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X<70','value=200')
    out+=ctl(-1,'CPU approach','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X>=70','value=20\nctrl=1')
    (CHAR/'JuraShinju.cmd').write_text(out)

def system():
    s='\n[Statedef -2]\n'
    for v in [40,41]:s+=c(-2,'Finite amplification timer','VarAdd',f'!IsHelper && Var({v})>0',f'v={v}\nvalue=-1')
    s+=c(-2,'Bounded power','AttackMulSet','!IsHelper','value=IfElse(Var(40)>0,1.5,1.15)')+c(-2,'Awakened durability','DefenceMulSet','!IsHelper','value=IfElse(Var(40)>0,1.1,1)')
    s+=c(-2,'Air-chain reset','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge hum','StopSnd','StateNo!=500','channel=3')+c(-2,'Charge wave cleanup','RemoveExplod','!IsHelper && StateNo!=500','ID=9551')
    s+=effect(-2,'!IsHelper && Var(40)>0 && RoundState=2 && GameTime%24=0',8605,10,-65,.4,12,-1)
    s+=c(-2,'Round effect cleanup','RemoveExplod','RoundState!=2')
    return s

def main():
    animations();normals();techniques();claws();orbs();utility();ultimate();common();commands()
    for n,(poses,hurt,box,loop) in body_actions.items():
        s=f'\n[Begin Action {n}]\n'
        if box:s+=f'Clsn1Default: 1\n Clsn1[0] = {box}\n'
        if loop:s+='Loopstart\n'
        for pose,ticks in poses:
            if hurt:
                width,height=Image.open(CHAR/meta[pose]['file']).size
                s+=f'Clsn2: 1\n Clsn2[0] = {-min(42,width//2) if pose==8 else -15},{-min(80,height-2)},{min(42,width//2) if pose==8 else 15},-1\n'
            s+=f'0,{pose},0,0,{ticks}\n'
        air.append(s)
    constants='''[Data]
life=1300
power=3000
attack=100
defence=115
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
height=84
attack.dist=90
proj.attack.dist=280
head.pos=0,-72
mid.pos=0,-42
shadowoffset=0
draw.offset=0,0
[Velocity]
walk.fwd=2.8
walk.back=-2.5
run.fwd=7.6,0
run.back=-7.6,0
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
    (CHAR/'JuraShinju.cns').write_text('; Jura: Vaydra sheet, own MUGEN combat and finite helpers.\n'+constants+''.join(states)+system())
    (CHAR/'JuraShinju.air').write_text('; Original Jura poses; no body redraw or alternate giant model.\n'+''.join(air))
    (CHAR/'JuraShinju.def').write_text('''[Info]
name="Jura Shinju"
displayname="Jura Shinju"
versiondate=10,22,2026
mugenversion=1.1
author="Vahidras / Vaydra (sprites), Codex (fan adaptation)"
localcoord=320,240
pal.defaults=1
[Files]
sprite=JuraShinju.sff
sound=JuraShinju.snd
anim=JuraShinju.air
cmd=JuraShinju.cmd
cns=JuraShinju.cns
st=JuraShinju.cns
stcommon=JuraShinju_common.cns
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
    (CHAR/'assets/moves.json').write_text(json.dumps(dict(techniques=MOVES,body_poses=36,awakening=dict(ticks=720,full_meter_required=True,cost=1500,technique_cost_multiplier=.75,attack_multiplier_base=1.15,attack_multiplier_awake=1.5,regen='9 life / 3 ticks during tree-cocoon state 520, ticks 24..81; max 180 life; interrupts on hit'),ultimate=dict(cost=3000,must_hit=True,budget='min(450,floor(enemy_lifemax*.45))'),source_video='Vaydra Senki.mp4; visual reference only, own MUGEN states',canon_note='Ocular Bijudama, wood and claw marks are the core. The ultimate is an original ocular Bijudama adaptation. No Kokugan or black cubes; fan Chibaku rock is not used by attacks.'),indent=2)+'\n')
    print('Authored Jura:',len(air),'actions,',len(MOVES),'techniques and finite common recovery')

if __name__=='__main__':main()
