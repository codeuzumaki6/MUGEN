#!/usr/bin/env python3
"""Ryu Shinju: original iron sand poses and video-referenced native combat."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'RyuShinju'
MOVES=[('Lluvia','a','F',1000,350),('Prisma','a','B',1010,500),('Magnetismo','b','F',1020,500),('Prision','b','B',1030,650),('Espada','c','F',1040,450),('Ola','c','B',1050,600),('Barrido','a','D',1400,200),('Lanzador','b','D',1410,300),('Enjambre','c','D',1420,400),('Aguja','y','N',1200,200),('Marca','z','N',1210,250),('Torbellino','y','D',1430,650),('SalidaGarra','z','D',1440,400)]
air=[];states=[];bodyanims=set()
def ctl(n,label,kind,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype={kind}\n{triggers}\n{params}\n{extra}\n'
def c(n,label,kind,when,params='',extra=''):return ctl(n,label,kind,'trigger1='+when,params,extra)
def state(n,anim,typ='S',move='I',physics='S',cost=0,vel='0,0',ctrl=0):return f'\n[Statedef {n}]\ntype={typ}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'+(f'anim={anim}\n' if anim is not None else '')+(f'velset={vel}\n' if vel else '')+(f'poweradd=-{cost}\n' if cost else '')
def action(n,poses,g=0,box=None,loop=False,hurt=True):
 bodyanims.add(n);s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]=-14,-76,14,-1\n'
 if loop:s+='Loopstart\n'
 for i,(p,t) in enumerate(poses):
  if box and i>0 and i<len(poses)-1:s+=f'Clsn1: 1\n Clsn1[0]={box}\n'
  s+=f'{g},{p},0,0,{t}\n'
 air.append(s)
def fxaction(n,g,nums,t=3,box=None,loop=False,add=False):
 s=f'\n[Begin Action {n}]\n'
 if box:s+=f'Clsn1Default: 1\n Clsn1[0]={box}\n'
 if loop:s+='Loopstart\n'
 for p in nums:s+=f'{g},{p},0,0,{t}'+(',,A' if add is True else ',,'+add if add else '')+'\n'
 air.append(s)
def effect(n,t,anim,x=0,y=-40,scale=.6,ticks=-2):return c(n,'Technique drawing','Explod',t,f'anim={anim}\npostype=P1\npos={x},{y}\nscale={scale},{scale}\nremovetime={ticks}\nsprpriority=3\nownpal=1\nremoveongethit=1\npausemovetime=180\nsupermovetime=180')
def snd(n,t,g,no,channel=0,volume=80):return c(n,'Technique sound','PlaySnd',t,f'value=S{g},{no}\nchannel={channel}\nvolumescale={volume}')
def startup(n,voice=5):return snd(n,'Time=0',1,21,4,75)+c(n,'Technique activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')+effect(n,'Time=0',8710,6,-45,.65,8)
def recover(n,t=55,airborne=False):return c(n,'Return control','ChangeState',f'Time>={t}',f'value={50 if airborne else 0}\nctrl=1')
def hit(n,t,damage,fin=False,low=False,airborne=False,stun=30,starter=False):
 return c(n,'Physical contact','HitDef',f'Time={t}',f'''attr={'A' if airborne else 'C' if low else 'S'},{'HP' if starter else 'SA' if n%10000>=1000 else 'NA'}
damage={damage},0
animtype={'Up' if fin else 'Medium'}
guardflag={'L' if low else 'MA'}
hitflag={'M' if starter else 'MAF'}
priority=5,Hit
pausetime=4,8
sparkno=S8700
guard.sparkno=-1
sparkxy=0,-43
hitsound=S1,{19 if fin else 7}
guardsound=S1,9
ground.type={'Low' if low else 'High'}
ground.hittime={stun}
ground.slidetime=20
ground.velocity={-5 if fin else -.3},{-8 if fin else 0}
air.hittime=32
air.velocity={-4 if fin else -.5},{-5 if fin else -1}
fall={int(fin)}
fall.recover=1
fall.recovertime=45
getpower={25 if n%10000<1000 else 0},0
givepower=10,5
envshake.time={8 if fin else 2}
envshake.ampl={-4 if fin else -1}'''+('\np2stateno=3010\nID=3000' if starter else ''))

def animations():
 base={0:[(0,10),(1,10),(2,10)],5:[(0,6)],6:[(15,6)],10:[(15,5)],11:[(15,5)],12:[(15,5)],20:[(3,5),(4,5),(5,5),(6,5),(7,5),(8,5)],21:[(8,5),(7,5),(6,5),(5,5)],40:[(63,4)],41:[(63,7)],44:[(64,7)],52:[(14,5),(15,4),(0,4)],100:[(3,3),(4,3),(5,3),(6,3),(7,3),(8,3)],105:[(8,3),(7,3),(6,3),(5,3)],170:[(13,30)],180:[(18,15),(21,18),(22,60),(18,30)],190:[(0,12),(16,12),(17,12),(0,10)],500:[(16,8),(17,8),(18,8)],520:[(57,8),(58,8),(59,12),(60,12),(18,15)],5000:[(9,8),(10,8)],5010:[(15,8)],5020:[(11,8)],5030:[(11,7),(12,7)],5100:[(13,10)],5110:[(13,28)],5120:[(14,7),(15,7),(0,5)],5150:[(13,60)],5200:[(63,8)],5210:[(63,8)],5300:[(9,20)]}
 for n in [120,130,140,150]:base[n]=[(9,5)]
 for n in [121,131,141,151]:base[n]=[(15,5)]
 for n in [122,132,142,152]:base[n]=[(63,5)]
 for n,poses in base.items():
  for form in [0,1]:
   if n==520 and form:continue
   action(n+form*10000,poses,loop=n in [0,11,20,21,41,44,500,5150])
 for g,count in [(8700,4),(8710,4),(8720,6),(8670,11),(8900,24),(8910,5),(8820,5)]:fxaction(g,g,range(count),2 if g!=8900 else 3,loop=g==8900,add=True)
 fxaction(8610,8610,[0],3,box='-26,-7,26,7',loop=True)
 air.append('\n[Begin Action 8611]\nClsn1Default: 1\n Clsn1[0]=-30,-42,30,40\nLoopstart\n8601,0,0,40,4\n')
 fxaction(8612,8601,[0],3,box='-36,-84,36,0',loop=True)
 air.append('\n[Begin Action 8613]\nLoopstart\n8603,0,0,0,8\n')
 fxaction(8615,8615,range(6),5,loop=True)
 fxaction(8620,8620,range(8),3,box='-48,-145,48,0',loop=True)
 fxaction(8625,8625,range(8),2,box='0,-20,90,20',loop=True)
 fxaction(8626,8602,[0],3,box='-26,-19,26,19',loop=True)
 fxaction(8607,8607,[0],4,loop=True)

def needle(n,t,damage,fin=False,y=-28,vx=13):
 s=c(n,'Iron needle damage','VarSet',f'Time={t}',f'v=30\nvalue={damage}')+c(n,'Iron needle finish','VarSet',f'Time={t}',f'v=31\nvalue={int(fin)}')+c(n,'Iron needle speed','VarSet',f'Time={t}',f'v=32\nvalue={vx}')
 return s+c(n,'Actual travelling iron needle','Helper',f'Time={t} && NumHelper(9400)<6',f'helpertype=Normal\nname="Aguja de hierro"\nID=9400\nstateno=9400\npostype=P1\npos=33,{y}\nownpal=1\nkeyctrl=0')+snd(n,f'Time={t}',1,30,2,55)
def cast(n,t,sn,x=28,y=-30):return c(n,'Original iron sand manifestation','Helper',f'Time={t}',f'helpertype=Normal\nname="Arena de hierro"\nID={sn}\nstateno={sn}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def normals():
 for form in [0,1]:
  off=form*10000
  for family,base in enumerate([200,210,220]):
   for step in range(3):
    n=off+base+step
    poses=([(27,3),([28,29,30][step],8),(27,8)] if family==0 else [(31,3),([32,33,35][step],8),(31,8)] if family==1 else [(67,3),([68,70,72][step],8),(67,8)])
    action(n,poses,box='0,-67,73,-4');s=state(n,n,move='A',vel='2.4,0')+snd(n,'Time=3',1,0,1,65)+hit(n,3,[46,58,82][step]+form*[8,10,14][step],step==2)
    s+=c(n,'Short step ends','VelSet','Time>=7','x=0')
    if step==2 and family==2:s+=effect(n,'Time=4',8670,40,0,.5,16)
    s+=recover(n,19);states.append(s)
  for base in [600,610,620]:
   for step in range(3):
    n=off+base+step;action(n,[(63,3),([65,66,74][step],8),(64,7)],box='-4,-70,85,-4')
    s=state(n,n,'A','A','N',vel=None)+c(n,'Finite aerial chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief juggle hover','VelSet','Time<7','x=1.8\ny=-.5')+c(n,'Return to gravity','VelAdd','Time>=7','y=.48')+hit(n,3,[40,52,78][step]+form*12,step==2,airborne=True)
    s+=c(n,'Land safely','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+recover(n,18,True);states.append(s)

def techniques():
 for form in [0,1]:
  for name,b,d,base,cost in MOVES:
   n=base+form*10000;price=round(cost*.8) if form else cost
   if base in [1210,1440]:continue
   if base in [1000,1200]:
    action(n,[(23,10),(24,10),(25,12),(26,12),(23,18),(0,14)])
    s=state(n,n,move='A',cost=price)+startup(n)
    times=([12,24,36,48,60] if form else [12,27,42]) if base==1000 else ([12,24] if form else [12])
    for i,t in enumerate(times):s+=needle(n,t,(58 if form else 52) if base==1000 else (58 if form else 88),i==len(times)-1,y=-28 if i%2==0 else -34,vx=15 if form else 13)
    s+=recover(n,82 if base==1000 else 58);states.append(s);continue
   if base==1010:
    action(n,[(37,12),(38,14),(39,20),(40,12),(0,16)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,22,9430,35,-34)+snd(n,'Time=22',1,41,1)+effect(n,'Time=18',8670,20,0,.6,18)+recover(n,76);states.append(s);continue
   if base==1020:
    action(n,[(41,10),(42,38),(41,12),(0,14)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,18,9420,27,-29)+snd(n,'Time=18',1,42,1)+recover(n,74);states.append(s);continue
   if base==1030:
    action(n,[(18,10),(21,12),(38,14),(21,52),(18,16),(0,10)]);s=state(n,n,move='A',cost=price)+startup(n)
    s+=cast(n,22,9440,'IfElse(P2Dist X<190,P2Dist X,190)',0)+snd(n,'Time=22',1,41,1)+recover(n,114);states.append(s);continue
   if base==1050:
    action(n,[(18,10),(45,8),(46,8),(47,8),(48,8),(49,8),(18,18),(0,12)],box='0,-82,88,-3');s=state(n,n,move='A',cost=price,physics='N')+startup(n)
    s+=c(n,'Iron wave advances','VelSet','Time>=10 && Time<40','x=2.2')+c(n,'Stop wave advance','VelSet','Time>=40','x=0')
    for i,t in enumerate([10,26,42]):s+=hit(n,t,[55,65,100][i]+form*18,i==2,stun=38)
    s+=recover(n,80);states.append(s);continue
   if base==1400:
    action(n,[(15,7),(55,10),(56,10),(15,8),(0,10)],box='0,-29,72,-2');s=state(n,n,move='A',cost=price,physics='N')+startup(n)
    s+=c(n,'Low iron sweep advances','VelSet','Time>=7 && Time<23',f'x={7 if form else 6}\ny=0')+c(n,'Low sweep brakes','VelSet','Time>=23','x=0\ny=0')+hit(n,7,140 if form else 110,True,low=True)+effect(n,'Time=7',8670,0,0,.5,20)+recover(n,45);states.append(s);continue
   if base in [1040,1410]:
    action(n,[(67,8),(68,7),(69,7),(70,7),(71,10),(64,10)] if base==1040 else [(37,7),(38,6),(39,10),(40,8),(18,12)],box='-4,-78,82,-2')
    s=state(n,n,move='A',cost=price,physics='N')+startup(n);launch=8 if base==1040 else 7
    s+=c(n,'Rise with iron weapon','VelSet',f'Time={launch}',f'x={3 if base==1040 else 1.4}\ny={-6 if base==1040 else -4}')+c(n,'Airborne blade','StateTypeSet',f'Time={launch}','statetype=A\nphysics=N')+c(n,'Finite rise and fall','VelAdd',f'Time>{launch}','y=.42')
    s+=hit(n,launch,75 if base==1040 else 160 if form else 130,base!=1040,airborne=True)
    if base==1040:s+=hit(n,17,115 if form else 90,True,airborne=True)
    s+=effect(n,f'Time={launch}',8710,28,-55,.65,14)+c(n,'Land with control','ChangeState',f'Time>{launch+8} && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+recover(n,70,True);states.append(s);continue
   if base==1420:
    action(n,[(57,10),(58,12),(59,12),(60,16),(61,10),(62,10),(18,16)]);s=state(n,n,move='A',cost=price)+startup(n)
    for t in [12,30,48]:s+=cast(n,t,9441,37,-23)+snd(n,f'Time={t}',1,31,1,60)
    s+=recover(n,86);states.append(s);continue
   if base==1430:
    action(n,[(18,12),(19,12),(20,58),(18,18),(0,12)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,22,9450,'IfElse(P2Dist X<170,P2Dist X,170)',0)+snd(n,'Time=22',1,30,2)+recover(n,112);states.append(s);continue

def moving_helper(n,anim,damage,speed=10,fin=True,stun=35):
 s=state(n,anim,'A','A','N',vel=f'{speed},0')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
 s+=c(n,'Root amplification applies once','VarSet','Time=0',f'v=0\nvalue=IfElse(Root,Var(42),{round(damage*1.25)},{damage})')
 s+=hit(n,1,'Var(0)',fin,airborne=True,stun=stun).replace('attr=A,SA','attr=A,SP')
 s+=effect(n,'MoveContact',8700,0,0,.6,10)+c(n,'Finite physical projectile','DestroySelf','MoveContact || Time>=48 || FrontEdgeBodyDist<-100 || RoundState!=2');return s
def helpers():
 n=9400;s=state(n,8610,'A','A','N')+c(n,'Read needle damage','VarSet','Time=0','v=0\nvalue=Parent,Var(30)')+c(n,'Read needle finish','VarSet','Time=0','v=1\nvalue=Parent,Var(31)')+c(n,'Read needle velocity','VelSet','Time=0','x=Parent,Var(32)\ny=0')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
 s+=hit(n,1,'Var(0)',False,airborne=True,stun=38).replace('attr=A,SA','attr=A,SP').replace('fall=0','fall=Var(1)').replace('ground.velocity=-0.3,0','ground.velocity=IfElse(Var(1),-5,-.3),IfElse(Var(1),-7,0)')
 s+=c(n,'Finite iron needle','DestroySelf','MoveContact || Time>=42 || FrontEdgeBodyDist<-100 || RoundState!=2');states.append(s)
 n=9430;s=moving_helper(n,8611,185,9)+c(n,'Rotating original prism','AngleDraw','1','value=Time*9\nscale=.9,.9');states.append(s)
 n=9420;s=moving_helper(n,8625,155,10,False,64)+c(n,'Electrical contact remains visible','Explod','MoveHit','anim=8625\npostype=P2\npos=-20,-32\nbindtime=35\nremovetime=35\nscale=.55,.55\nsprpriority=3\nownpal=1','persistent=0');states.append(s)
 n=9441;s=moving_helper(n,8626,70,7,False,38)+c(n,'Rolling iron shell','AngleDraw','1','value=Time*15\nscale=1,1');states.append(s)
 n=9440;s=state(n,8612,'A','A','N')+c(n,'Iron prison grows from floor','AngleDraw','1','value=0\nscale=.2+IfElse(Time<15,Time,15)*.08,.2+IfElse(Time<15,Time,15)*.08')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
 for i,t in enumerate([12,62]):s+=hit(n,t,f'IfElse(Root,Var(42),{165 if i==0 else 95},{135 if i==0 else 75})',bool(i),airborne=True,stun=54).replace('attr=A,SA','attr=A,SP')
 s+=effect(n,'Time=62',8670,0,0,.9,22)+snd(n,'Time=62',1,41,1)+c(n,'Prison breaks and disperses','DestroySelf','Time>=84 || RoundState!=2');states.append(s)
 n=9450;s=state(n,8620,'A','A','N',vel='.8,0')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
 for i,t in enumerate([4,18,32,46]):s+=hit(n,t,f'IfElse(Root,Var(42),{95 if i==3 else 60},{80 if i==3 else 45})',i==3,airborne=True,stun=32).replace('attr=A,SA','attr=A,SP')
 s+=effect(n,'Time%16=0',8670,0,0,.55,18)+snd(n,'Time=46',1,41,1)+c(n,'Tornado finite lifetime','DestroySelf','Time>=62 || FrontEdgeBodyDist<-100 || RoundState!=2');states.append(s)
 n=9550;s=state(n,8900,'A',physics='N')+c(n,'Magnetic charge follows caster','BindToRoot','1','time=1\npos=0,-38')+c(n,'Energy envelope','AngleDraw','1','value=90\nscale=.32,.36')+c(n,'Blue magnetic energy','PalFX','1','time=1\ncolor=0\nmul=80,150,256')+c(n,'Chakra blend','Trans','1','trans=AddAlpha\nalpha=160,256')+c(n,'Behind body','SprPriority','1','value=-2')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'Aura cleanup','DestroySelf','trigger1=Root,StateNo!=500 && Root,StateNo!=520 && Root,Var(42)=0\ntrigger2=Root,Life<=0\ntrigger3=RoundState!=2');states.append(s)

def claws():
 for form in [0,1]:
  off=form*10000;n=1210+off;action(n,[(43,10),(44,16),(43,18),(0,10)]);s=state(n,n,move='A',cost=200 if form else 250)+startup(n)
  s+=cast(n,12,9600,'IfElse(P2Dist X<180,P2Dist X,180)',0)+snd(n,'Time=12',1,32,1)+recover(n,54);states.append(s)
  for base,cost in [(1211,200),(1440,400)]:
   n=base+off;action(n,[(43,8),(44,8),(73,10),(74,10),(18,14),(0,12)],box='0,-68,90,-4');s=state(n,n,move='A',cost=round(cost*.8) if form else cost,physics='N')+startup(n)
   s+=cast(n,5,9600,'IfElse(P2Dist X<180,P2Dist X,180)',0).replace('trigger1=Time=5','trigger1=Time=5 && NumHelper(9600)=0')
   s+=c(n,'Travel only to the visible placed mark','PosSet','Time=14 && NumHelper(9600)>0','x=(Helper(9600),Pos X)-Facing*32\ny=0')+c(n,'Face the nearby opponent after travel','Turn','Time=15 && P2Dist X<0','')
   s+=c(n,'Pass through the narrow claw opening','PlayerPush','Time>=10 && Time<=18','value=0')+c(n,'Brief portal transit','NotHitBy','Time>=10 && Time<=16','value=SCA\ntime=1')+effect(n,'Time=13',8613,0,-32,.7,18)+snd(n,'Time=14',1,32,1)+hit(n,22,170 if form else 135,True)+recover(n,62);states.append(s)
 n=9600;s=state(n,8613,'A',physics='N')+c(n,'Flat crossed original claw bands','AngleDraw','1','value=0\nscale=.65,.55')+c(n,'Claw band floor layer','SprPriority','1','value=-2')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'One consumed mark, finite lifetime','DestroySelf','trigger1=Time>=600\ntrigger2=RoundState!=2\ntrigger3=Root,StateNo%10000=1211 || Root,StateNo%10000=1440\ntrigger3=Root,Time>=16');states.append(s)

def utility():
 for n in [170,180,190]:
  s=state(n,f'{n}+10000*Var(42)')+c(n,'Original round pose','Null','1')
  if n==190:s+=c(n,'Introduction','AssertSpecial','Time<40','flag=Intro')+recover(n,46)
  states.append(s)
 s=state(500,'500+10000*Var(42)')+c(500,'Hold to charge energy','PowerAdd','1','value=22')+snd(500,'Time=0',1,4,3,60)+cast(500,0,9550,0,-38).replace('trigger1=Time=0','trigger1=Time=0 && NumHelper(9550)=0')+effect(500,'Time%14=0',8910,0,0,.35,14)
 s+=ctl(500,'Release charging','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=70','value=0\nctrl=1');states.append(s)
 s=state(520,520)+startup(520)+c(520,'Finite amplification cost','PowerAdd','Time=0','value=-1500')+effect(520,'Time=12',8720,0,-40,1,22)+effect(520,'Time=28',8670,0,0,.8,20)
 s+=c(520,'Start magnetic amplification','VarSet','Time=28','v=42\nvalue=1')+c(520,'Amplification duration','VarSet','Time=28','v=40\nvalue=1200')+c(520,'Amplification cooldown','VarSet','Time=28','v=41\nvalue=1500')+cast(520,8,9550,0,-38).replace('trigger1=Time=8','trigger1=Time=8 && NumHelper(9550)=0')+recover(520,60);states.append(s)

def ultimate():
 for form in [0,1]:
  off=form*10000;n=3000+off;action(n,[(67,8),(73,12),(74,14),(67,20)],box='0,-65,80,-4');s=state(n,n,move='A',cost=3000,physics='N')+startup(n)
  s+=c(n,'Opening thrust has actual travel','VelSet','Time>=8 && Time<28','x=6')+c(n,'Stop if the opening misses','VelSet','Time>=28','x=0')+hit(n,8,0,starter=True)+c(n,'Only a real opening hit starts the flight','ChangeState','MoveHit && NumTarget(3000)>0',f'value={3001+off}')+recover(n,56);states.append(s)
  n=3001+off;action(n,[(75,12),(76,12),(77,18),(78,18),(77,20),(78,20),(63,18),(67,12),(68,12),(69,12),(73,12),(74,18),(79,12),(80,12),(0,14)])
  s=state(n,n,physics='N')+c(n,'Finite confirmed aerial sequence','Pause','Time=0','time=216\nmovetime=216\npausebg=1')+c(n,'Protect only the confirmed ultimate','NotHitBy','Time<214','value=SCA\ntime=1')+c(n,'Fix the struck opponent location','VarSet','Time=0 && NumTarget(3000)>0','fv=5\nvalue=Target(3000),Pos X')
  s+=c(n,'Keep the actual victim grounded during flight','TargetBind','Time<210 && NumTarget(3000)>0','ID=3000\ntime=1\npos=(FVar(5)-Pos X)*Facing,-Pos Y')+c(n,'Dim the stage for the wings','BGPalFX','Time=0','time=210\nmul=80,85,95')
  s+=c(n,'Rise on the iron wings','PosAdd','Time>=8 && Time<38','y=-2.1')+c(n,'Glide down toward the actual target','VelSet','Time=130','x=((FVar(5)-Pos X)*Facing-48)/28\ny=2.1')+c(n,'Touch the floor after the dive','VelSet','Time>=158','x=0\ny=0')+c(n,'Land the descent','PosSet','Time>=158','y=0')
  s+=cast(n,4,9500,0,-70).replace('keyctrl=0','keyctrl=0\npausemovetime=240\nsupermovetime=240')+snd(n,'Time=4',1,30,2)
  ratio='.45' if form else '.42';cap=450 if form else 420
  s+=c(n,'Ultimate damage has a life-relative ceiling','VarSet','Time=0 && NumTarget(3000)>0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{cap},Floor((Target(3000),LifeMax)*{ratio}))')
  for j,t in enumerate([70,90,110]):
   for i in range(4):s+=effect(n,f'Time={t+i*2}',8607,35+i*23,-105+i*18,1,20).replace('removeongethit=1','removeongethit=1\nvelocity=4,5\naccel=0,.15')
  for i,t in enumerate([84,104,124,156,190]):
   s+=effect(n,f'Time={t}',8720 if i==4 else 8700,'(FVar(5)-Pos X)*Facing',-25,1.25 if i==4 else .8,22)+snd(n,f'Time={t}',1,41 if i==4 else 19,1)
   s+=c(n,'Damage belongs only to the confirmed victim','TargetLifeAdd',f'Time={t} && NumTarget(3000)>0','ID=3000\nvalue=-'+('(Var(20)-Floor(Var(20)/5)*4)' if i==4 else 'Floor(Var(20)/5)')+'\nabsolute=1\nkill=1')+c(n,'Heavy iron impact','EnvShake',f'Time={t}','time=9\nfreq=65\nampl=-5')
  s+=effect(n,'Time=184',8620,'(FVar(5)-Pos X)*Facing',0,.8,22)+c(n,'Always release the victim','TargetState','Time=210 && NumTarget(3000)>0','ID=3000\nvalue=3011')+recover(n,222);states.append(s)
 for n in [3010,3011]:
  s=state(n,None,'S','H','N')+c(n,'Victim retains its own hurt drawing','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')
  if n==3010:s+=c(n,'Failsafe release','SelfState','Time>=270 || NumEnemy=0','value=0\nctrl=1')
  else:s+=c(n,'Return the victim to its own fall','SelfState','Time>=1','value=5050\nctrl=0')+c(n,'Throw velocity','VelSet','Time=0','x=-6\ny=-7')
  states.append(s)
 n=9500;s=state(n,8615,'A',physics='N')+c(n,'Wings follow the unchanged original body','BindToRoot','1','time=1\npos=0,-70')+c(n,'Wings open and fold','AngleDraw','1','value=0\nscale=IfElse(Time<20,.2+Time*.04,IfElse(Time<180,1,IfElse(Time<206,(206-Time)/26.0,.01))),IfElse(Time<20,.2+Time*.04,IfElse(Time<180,1,IfElse(Time<206,(206-Time)/26.0,.01)))')+c(n,'Wings behind the caster','SprPriority','1','value=-1')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'Finite wing lifetime','DestroySelf','trigger1=Time>=210\ntrigger2=Root,StateNo%10000!=3001\ntrigger3=RoundState!=2');states.append(s)

def common():
 # Reuse the project's tested native guard, fall and dash states; all animation
 # choices are now form-aware and remain independent of another character file.
 s=(ROOT/'JuraShinju/JuraShinju_common.cns').read_text().replace('; Jura common states, derived from project native MUGEN guard and recovery.','; Ryu native guard, fall and dash states, derived from the project common implementation.')
 s=re.sub(r'(?m)^anim\s*=\s*(\d+)\s*$',r'anim=\1+10000*Var(42)',s)
 blocks=re.split(r'(?=\n\[State )',s);out=[]
 for block in blocks:
  if re.search(r'(?im)^type\s*=\s*ChangeAnim\s*$',block):
   block=re.sub(r'(?m)^value\s*=\s*(.+)$',r'value=(\1)+10000*Var(42)',block)
   block=block.replace('Anim != IfElse(Vel X<0,21,20)','Anim != IfElse(Vel X<0,21,20)+10000*Var(42)').replace('Anim != 44','Anim != 44+10000*Var(42)')
  out.append(block)
 (CHAR/'RyuShinju_common.cns').write_text(''.join(out))

def commands():
 s='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\ns=s\n[Defaults]\ncommand.time=20\ncommand.buffer.time=3\n'
 def cmd(name,keys,buf=3):return f'\n[Command]\nname="{name}"\ncommand={keys}\ntime=20\nbuffer.time={buf}\n'
 for name,b,d,n,cost in MOVES:
  for keys in ([f'~D,D{d},{d},{b}',f'~D,{d},{b}'] if d in ['F','B'] else [f'/D,{b}'] if d=='D' else [b]):s+=cmd(name,keys,1 if d=='N' else 3)
 for b in ['a','b','c','x','y','z','s']:s+=cmd(b,b)+cmd('hold_'+b,'/'+b,1)
 for name,keys in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D'),('FF','F,F'),('BB','B,B'),('recovery','a+b')]:s+=cmd(name,keys,1 if keys.startswith('/') else 3)
 s+='\n[Statedef -1]\n'
 for name,b,d,n,cost in MOVES:
  extra='\ntriggerall=command!="holddown"' if d=='N' else ''
  s+=ctl(-1,name,'ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=Power>=IfElse(Var(42),{round(cost*.8)},{cost}){extra}\ntrigger1=ctrl',f'value={n}+10000*Var(42)' if n!=1210 else 'value=IfElse(NumHelper(9600)>0,1211,1210)+10000*Var(42)')
 s+=ctl(-1,'Magnetic amplification','ChangeState','triggerall=AILevel=0\ntriggerall=command="s"\ntriggerall=command="holddown"\ntriggerall=Power>=3000\ntriggerall=Var(42)=0\ntriggerall=Var(41)=0\ntriggerall=StateType!=A\ntrigger1=ctrl','value=520')
 s+=ctl(-1,'Ultimate Xbox A','ChangeState','triggerall=AILevel=0\ntriggerall=command="x"\ntriggerall=Power>=3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=3000+10000*Var(42)')
 s+=ctl(-1,'Hold Pause to charge','ChangeState','triggerall=AILevel=0\ntriggerall=command="hold_s"\ntriggerall=command!="holddown"\ntriggerall=Power<3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=500')
 for b,base in [('a',200),('b',210),('c',220)]:
  s+=ctl(-1,'Ground chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=command!="holddown"\ntriggerall=StateType!=A\ntrigger1=ctrl\ntrigger2=StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220\ntrigger2=MoveHit\ntrigger2=Time>=6\ntrigger3=StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221\ntrigger3=MoveHit\ntrigger3=Time>=6',f'value={base}+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))','ignorehitpause=1')
  s+=ctl(-1,'Aerial chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=StateType=A\ntriggerall=Var(12)<3\ntrigger1=ctrl\ntrigger2=StateNo%10000>=600 && StateNo%10000<=621\ntrigger2=MoveHit\ntrigger2=Time>=6',f'value={base+400}+10000*Var(42)+Var(12)','ignorehitpause=1')
 for name,n in [('FF',100),('BB',105)]:s+=ctl(-1,'Double tap dash','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType=S\ntrigger1=ctrl',f'value={n}')
 for name,n in [('holdup',40),('holddown',11),('holdfwd',20),('holdback',20)]:
  extra='\ntriggerall=StateType=S\ntriggerall=command!="holdup"\ntriggerall=command!="holddown"' if n==20 else ''
  if n in [11,20]:extra+='\ntriggerall=StateNo<120 || StateNo>155'
  s+=ctl(-1,'Movement','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=StateNo!={n}{extra}\ntrigger1=ctrl',f'value={n}\nctrl={int(n!=40)}')
 for n,cost,dist in [(3000,3000,140),(1030,650,180),(1200,200,300),(1020,500,260),(1010,500,250)]:s+=ctl(-1,'CPU legal attack','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=Power>={cost}\ntrigger1=P2BodyDist X<{dist}\ntrigger1=Random<AILevel*3',f'value={n}+10000*Var(42)')
 s+=ctl(-1,'CPU close chain','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X<65','value=200+10000*Var(42)')+ctl(-1,'CPU approach','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X>=65','value=20\nctrl=1')
 (CHAR/'RyuShinju.cmd').write_text(s)

def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite form timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 # Finish the current attack/recoil in its native form before reverting.
 s+=c(-2,'Safe amplified expiry','VarSet','!IsHelper && Var(42)>0 && Var(40)=0 && Ctrl && MoveType!=H && StateNo!=500','v=42\nvalue=0')
 s+=c(-2,'Refresh form after expiry','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')
 s+=c(-2,'Preserve amplified artwork during native turn transitions','ChangeAnim','!IsHelper && Var(42)=1 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')
 s+=c(-2,'Air chain reset','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge hum','StopSnd','!IsHelper && StateNo!=500','channel=3')
 s+=c(-2,'amplified aura persists only during form','Helper','!IsHelper && RoundState=2 && Var(42)=1 && NumHelper(9550)=0','helpertype=Normal\nname="Campo magnetico"\nID=9550\nstateno=9550\npostype=P1\npos=0,-38\nownpal=1\nkeyctrl=0')
 s+=c(-2,'Round form cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round drawings cleanup','RemoveExplod','!IsHelper && RoundState!=2')
 return s

def main():
 animations();normals();techniques();claws();helpers();utility();ultimate();common();commands()
 constants=(ROOT/'JuraShinju/JuraShinju.cns').read_text().split('[Statedef',1)[0];constants=constants[constants.index('[Data]'):].replace('life=1300','life=1250').replace('defence=115','defence=110').replace('height=84','height=81')
 (CHAR/'RyuShinju.cns').write_text('; Ryu Shinju, original Vaydra sheet and own MUGEN combat.\n'+constants+''.join(states)+system())
 (CHAR/'RyuShinju.air').write_text('; Original Ryu body artwork, group 0 in both amplification banks.\n'+''.join(air))
 d=(ROOT/'JuraShinju/JuraShinju.def').read_text().replace('JuraShinju','RyuShinju').replace('Jura Shinju','Ryu Shinju').replace('versiondate=10,22,2026','versiondate=10,23,2026');(CHAR/'RyuShinju.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,amplification_offset=10000,amplification_ticks=1200,amplification_cost=1500,activation_requires=3000,ultimate_cost=3000,ultimate_budget='min(420,42% opponent max life)',amplified_ultimate_budget='min(450,45% opponent max life)',voices=False,video='User supplied Vaydra Senki gameplay; original sheet for all body poses'),indent=2)+'\n')
 print(len(states),'combat states,',len(air),'actions; original Ryu poses and finite iron sand helpers')
if __name__=='__main__':main()

