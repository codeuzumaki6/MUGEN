#!/usr/bin/env python3
"""Hidari Shinju: source sprites, Chidori, wood and a yellow Susanoo awakening."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'HidariShinju'
MOVES=[('Chidori','a','F',1000,350),('Garra','a','B',1010,450),('Corriente','b','F',1020,500),('Prision','b','B',1030,650),('Ascendente','c','F',1040,450),('Madera','c','B',1050,550),('Barrido','a','D',1400,200),('Palma','b','D',1410,300),('Ramas','c','D',1420,400),('Senbon','y','N',1200,200),('Marca','z','N',1210,250),('Tormenta','y','D',1430,650),('SalidaGarra','z','D',1440,400)]
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
 base={0:[(0,14),(1,10),(1,10),(0,12)],5:[(1,6)],6:[(14,6)],10:[(14,5)],11:[(14,5)],12:[(14,5)],20:[(15,5),(16,5),(17,5),(18,5),(19,5),(20,5)],21:[(20,5),(19,5),(18,5),(17,5)],40:[(21,4)],41:[(2,7)],44:[(6,7)],52:[(13,5),(14,4),(0,4)],100:[(2,3),(3,3),(4,3),(5,3),(6,3)],105:[(6,3),(5,3),(4,3),(3,3)],170:[(12,30)],180:[(32,12),(33,18),(1,60),(0,30)],190:[(0,12),(32,12),(33,12),(0,10)],500:[(32,8),(33,8),(32,8)],520:[(0,10),(32,8),(33,12),(49,12),(50,15)],5000:[(7,8),(8,8)],5010:[(14,8)],5020:[(9,8)],5030:[(9,7),(10,7)],5100:[(12,10)],5110:[(12,28)],5120:[(13,7),(14,7),(0,5)],5150:[(12,60)],5200:[(2,8)],5210:[(2,8)],5300:[(7,20)]}
 for n in [120,130,140,150]:base[n]=[(7,5)]
 for n in [121,131,141,151]:base[n]=[(14,5)]
 for n in [122,132,142,152]:base[n]=[(2,5)]
 for n,poses in base.items():
  for form in [0,1]:
   if n==520 and form:continue
   action(n+form*10000,poses,loop=n in [0,11,20,21,41,44,500,5150])
 for g,count in [(8700,4),(8710,4),(8720,6),(8670,11),(8900,24),(8910,5),(8820,5)]:fxaction(g,g,range(count),2 if g!=8900 else 3,loop=g==8900,add=True)
 fxaction(8610,8640,range(8),2,box='0,-12,85,12',loop=True,add='AS256D96')
 fxaction(8611,8602,[0,1,2],4,box='0,-30,95,30',loop=True)
 fxaction(8612,8600,[0,1,2,2,2,2],3,box='-32,-60,32,0',loop=True)
 fxaction(8613,8603,[0,1,2,1],5,loop=True)
 fxaction(8614,8601,range(4),3,loop=True)
 fxaction(8620,8640,range(8),3,box='0,-22,95,22',loop=True,add='AS256D96')
 fxaction(8625,8640,range(8),2,loop=True,add='AS256D96')
 fxaction(8645,8645,range(4),3,box='0,-9,90,9',loop=True)
 for i in range(8):fxaction(9630+i,8630,[i],4,loop=True)

def cast(n,t,sn,x=28,y=-30):return c(n,'Physical manifestation','Helper',f'Time={t}',f'helpertype=Normal\nname="Shinjutsu de Hidari"\nID={sn}\nstateno={sn}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def blue(n,when,x=42,y=-38,scale=.22,ticks=20):return effect(n,when,8625,x,y,scale,ticks)
def base_chidori():
 # The supplied Sasuke's original AIR 1030 is already packed as 21030.
 # Keep Hidari's three source poses; electricity follows his actual hand.
 n=1000
 action(n,[(28,20),(29,4),(30,4),(29,4),(30,4),(29,4),(30,4),(29,4)],box='12,-73,66,-14')
 s=state(n,n,move='A',cost=350,physics='N')+startup(n)+snd(n,'Time=4',1,42,2)+cast(n,1,9460,7,-50)
 s+=c(n,'Physical Chidori rush','VelSet','Time>=20 && Time<44 && !MoveContact','x=9.5\ny=0')+c(n,'Brake on contact or finite rush end','VelSet','MoveContact || Time>=44','x=0\ny=0')
 s+=hit(n,20,30,False,stun=45).replace('pausetime=4,8','pausetime=7,10').replace('ground.velocity=-0.3,0','ground.velocity=0,0').replace('ground.velocity=-.3,0','ground.velocity=0,0').replace('air.velocity=-0.5,-1','air.velocity=0,-.1').replace('air.velocity=-.5,-1','air.velocity=0,-.1')
 s+=snd(n,'Time=20',1,42,2)+c(n,'Blue rush afterimage','AfterImage','Time=20','time=22\nlength=5\ntimegap=2\nframegap=2\npalcolor=0\npaladd=0,18,35\npalmul=.65,.8,1')
 s+=c(n,'Only real contact starts the Chidori impact','ChangeState','MoveHit','value=1001')+c(n,'Guard or miss ends the rush','ChangeState','MoveGuarded || Time>=46','value=1002');states.append(s)
 n=1001;action(n,[(30,4),(29,5),(30,5),(29,5),(30,8),(29,5),(30,4)],box='10,-73,68,-14')
 s=state(n,n,move='A',physics='N')
 s+=c(n,'Close the real gap after fingertip contact','VelSet','Time<8 && P2BodyDist X>18','x=3.5\ny=0')+c(n,'Stop at close contact without crossing the opponent','VelSet','Time>=8 || P2BodyDist X<=18','x=0\ny=0')
 for t in [4,9,14,19]:
  s+=hit(n,t,25,False,stun=32).replace('pausetime=4,8','pausetime=2,3').replace('ground.velocity=-0.3,0','ground.velocity=0,0').replace('air.velocity=-0.5,-1','air.velocity=0,-.1')
 s+=hit(n,27,55,True,stun=38)+snd(n,'Time=0',1,42,2)+c(n,'Finish the physical Chidori','ChangeState','Time>=36','value=1002');states.append(s)
 n=1002;action(n,[(30,5),(28,8),(0,6)])
 states.append(state(n,n,physics='N')+c(n,'End rush trail','AfterImageTime','Time=0','time=0')+recover(n,19))
 n=9460;s=state(n,21030,'A',physics='N')
 s+=c(n,'Sasuke lightning follows Hidari hand','BindToRoot','1','time=-1\npos=IfElse(Root,StateNo=1000 && Root,Time<20,7,44),IfElse(Root,StateNo=1000 && Root,Time<20,-50,-54)','ignorehitpause=1')
 s+=c(n,'Lightning faces with Hidari','Turn','Facing!=Root,Facing','')
 s+=c(n,'Original electrical nucleus fits Hidari','AngleDraw','1','value=0\nscale=IfElse(Root,StateNo=1000,IfElse(Root,Time<20,.10+(Root,Time)*.005,.24),.29),IfElse(Root,StateNo=1000,IfElse(Root,Time<20,.10+(Root,Time)*.005,.24),.29)','ignorehitpause=1')
 s+=c(n,'Original Sasuke additive lightning','Trans','1','trans=Add','ignorehitpause=1')+c(n,'Hand lightning in front','SprPriority','1','value=3','ignorehitpause=1')+c(n,'No separate body or shadow','AssertSpecial','1','flag=NoShadow','ignorehitpause=1')+c(n,'Electricity has no independent push box','PlayerPush','1','value=0','ignorehitpause=1')
 s+=ctl(n,'Clear electricity on release or interruption','DestroySelf','trigger1=Root,StateNo!=1000 && Root,StateNo!=1001 && Root,StateNo!=1002\ntrigger2=Root,StateNo=1002 && Root,Time>=5\ntrigger3=Root,MoveType=H\ntrigger4=RoundState!=2\ntrigger5=Root,Life<=0','','ignorehitpause=1');states.append(s)
def normals():
 for form in [0,1]:
  off=form*10000
  for family,base in enumerate([200,210,220]):
   for step in range(3):
    n=off+base+step;poses=([(21,3),([22,23,24][step],8),(21,8)] if family==0 else [(24,3),([25,26,27][step],8),(24,8)] if family==1 else [(34,3),([35,37,38][step],8),(34,8)])
    action(n,poses,box='0,-67,78,-4');s=state(n,n,move='A',vel='2.4,0')+snd(n,'Time=3',1,0,1,65)+hit(n,3,[46,58,82][step]+form*[8,10,14][step],step==2)
    s+=c(n,'Step ends','VelSet','Time>=7','x=0')
    if family==2:s+=effect(n,'Time=4',8614,52,-38,.55,14)
    s+=recover(n,19);states.append(s)
  for base in [600,610,620]:
   for step in range(3):
    n=off+base+step;action(n,[(2,3),([22,26,40][step],8),(6,7)],box='-4,-70,85,-4')
    s=state(n,n,'A','A','N',vel=None)+c(n,'Finite aerial chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Juggle hover','VelSet','Time<7','x=1.8\ny=-.5')+c(n,'Return to gravity','VelAdd','Time>=7','y=.48')+hit(n,3,[40,52,78][step]+form*12,step==2,airborne=True)
    s+=c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+recover(n,18,True);states.append(s)

def techniques():
 for form in [0,1]:
  for name,b,d,base,cost in MOVES:
   if base in [1210,1440]:continue
   n=base+form*10000;price=round(cost*.8) if form else cost
   if base==1000: # Both forms keep the user's requested Chidori input.
    if not form:base_chidori();continue
    action(n,[(28,14),(29,18),(30,20),(28,16),(0,10)],box='16,-55,82,-14')
    s=state(n,n,move='A',cost=price,physics='N')+startup(n)+snd(n,'Time=8',1,42,2)
    s+=blue(n,'Time>=8 && Time<=42 && Time%8=0',61,-48,.27,12)+c(n,'Chidori hand glow follows the rush','Explod','Time=10','anim=8710\npostype=P1\npos=64,-48\nbindtime=34\nremovetime=34\nscale=.45,.45\nsprpriority=3\nownpal=1\nremoveongethit=1')
    s+=c(n,'Real forward Chidori dash','VelSet','Time>=14 && Time<43',f'x={10 if form else 8.5}\ny=0')+c(n,'Stop on contact or dash end','VelSet','MoveContact || Time>=43','x=0\ny=0')+hit(n,14,245 if form else 185,True,stun=38)+c(n,'Chidori afterimage','AfterImage','Time=14','time=24\nlength=8\ntimegap=2\nframegap=3\npalcolor=0\npaladd=0,25,55\npalmul=.7,.8,1')+recover(n,78);states.append(s);continue
   if form:
    # A genuine guardian move set, with distinct sword, hand and bow effects.
    if base in [1010,1020,1200,1420]:
     action(n,[(32,10),(49,12),(50,36),(32,16),(0,10)])
     s=state(n,n,move='A',cost=price)+startup(n)
     times=[22,36,50] if base in [1020,1420] else [22]
     for i,t in enumerate(times):
      if base==1420:s+=cast(n,t,9472,f'IfElse(P2Dist X<220,P2Dist X,220)+{[-24,0,24][i]}',-170)+snd(n,f'Time={t}',1,30,2,65)
      else:s+=cast(n,t,9470 if base==1010 else 9471,55 if base==1010 else 'IfElse(P2Dist X<102,IfElse(P2Dist X>48,P2Dist X-32,16),70)',-29 if base==1010 else -92)+snd(n,f'Time={t}',1,30,2,65)
     s+=recover(n,88 if len(times)>1 else 78);states.append(s);continue
    if base==1030:
     action(n,[(31,12),(49,12),(50,52),(32,16),(0,12)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,24,9440,'IfElse(P2Dist X<190,P2Dist X,190)',0)+snd(n,'Time=24',1,41,2)+recover(n,108);states.append(s);continue
    if base in [1050,1430]:
     action(n,[(32,12),(49,18),(50,18),(49,18),(32,18),(0,16)],box='0,-80,145,-2');s=state(n,n,move='A',cost=price,physics='N')+startup(n)
     if base==1430:s+=c(n,'Cleave step reaches the opponent','VelSet','Time>=12 && Time<46','x=3.2')+c(n,'Cleave step ends','VelSet','Time>=46','x=0')
     for i,t in enumerate([18,42,66] if base==1430 else [18,46]):s+=hit(n,t,[70,80,130][i] if base==1430 else [100,165][i],i==(2 if base==1430 else 1),stun=40)+effect(n,f'Time={t}',8720,95,-32,.9,20)+snd(n,f'Time={t}',1,41,2)
     s+=recover(n,100);states.append(s);continue
   if base==1010:
    action(n,[(31,12),(34,18),(35,18),(34,20),(0,10)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,20,9430,45,-34)+snd(n,'Time=20',1,31,2)+recover(n,78);states.append(s);continue
   if base==1020:
    action(n,[(45,10),(46,12),(47,12),(48,18),(45,18),(0,10)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,22,9420,40,-27)+snd(n,'Time=22',1,42,2)+blue(n,'Time=12',8,-38,.5,30)+recover(n,84);states.append(s);continue
   if base==1030:
    action(n,[(31,12),(34,12),(35,52),(34,16),(0,12)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,24,9440,'IfElse(P2Dist X<190,P2Dist X,190)',0)+snd(n,'Time=24',1,41,2)+recover(n,108);states.append(s);continue
   if base==1050:
    action(n,[(34,10),(35,12),(37,12),(38,12),(40,12),(41,12),(34,16),(0,12)],box='0,-78,107,-3');s=state(n,n,move='A',cost=price,physics='N')+startup(n)
    s+=c(n,'Wood combo advances','VelSet','Time>=10 && Time<42','x=2.4')+c(n,'Combo brakes','VelSet','Time>=42','x=0')
    for i,t in enumerate([10,34,58]):s+=hit(n,t,[55,65,105][i],i==2,stun=40)+effect(n,f'Time={t}',8614,65,-40,.7,12)
    s+=recover(n,98);states.append(s);continue
   if base==1400:
    action(n,[(14,7),(21,10),(24,10),(14,8),(0,10)],box='0,-29,72,-2');s=state(n,n,move='A',cost=price,physics='N')+startup(n)
    s+=c(n,'Low sweep travels','VelSet','Time>=7 && Time<23',f'x={7 if form else 6}\ny=0')+c(n,'Low sweep brakes','VelSet','Time>=23','x=0\ny=0')+hit(n,7,150 if form else 110,True,low=True)+effect(n,'Time=7',8670,0,0,.5,20)+recover(n,45);states.append(s);continue
   if base==1040:
    action(n,[(39,8),(40,7),(41,7),(42,7),(43,10),(44,10)],box='-4,-100,82,-2');s=state(n,n,move='A',cost=price,physics='N')+startup(n)
    s+=c(n,'Wood claw rises','VelSet','Time=8','x=3\ny=-6')+c(n,'Airborne claw','StateTypeSet','Time=8','statetype=A\nphysics=N')+c(n,'Finite rise','VelAdd','Time>8','y=.42')+hit(n,8,85,False,airborne=True)+hit(n,17,140 if form else 100,True,airborne=True)+c(n,'Land','ChangeState','Time>16 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+recover(n,70,True);states.append(s);continue
   if base==1410:
    action(n,[(49,10),(50,30),(49,16),(0,12)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,18,9473 if form else 9431,28,-27)+snd(n,'Time=18',1,31,2)+recover(n,68);states.append(s);continue
   if base==1420:
    action(n,[(34,10),(35,12),(37,12),(38,16),(34,20),(0,12)]);s=state(n,n,move='A',cost=price)+startup(n)
    for t in [18,34,50]:s+=cast(n,t,9441,45,-28)+snd(n,f'Time={t}',1,31,2,65)
    s+=recover(n,86);states.append(s);continue
   if base==1200:
    if not form:
     action(n,[(28,8),(33,16),(33,14),(32,10),(0,8)])
     s=state(n,n,move='A',cost=price)+startup(n)+cast(n,24,9401,22,-61)+recover(n,56);states.append(s);continue
    action(n,[(32,10),(33,12),(49,18),(32,14),(0,10)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,16,9400,40,-27)+snd(n,'Time=16',1,42,2)+recover(n,64);states.append(s);continue
   if base==1430:
    action(n,[(45,12),(46,16),(47,16),(48,30),(45,18),(0,12)]);s=state(n,n,move='A',cost=price)+startup(n)+cast(n,24,9450,'IfElse(P2Dist X<170,P2Dist X,170)',0)+snd(n,'Time=24',1,42,2)+recover(n,108);states.append(s);continue

def moving_helper(n,anim,damage,speed=10,fin=True,stun=35):
 s=state(n,anim,'A','A','N',vel=f'{speed},0')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
 s+=hit(n,0,damage,fin,airborne=True,stun=stun).replace('attr=A,SA','attr=A,SP')+c(n,'Finite travelling technique','DestroySelf','MoveContact || Time>=52 || FrontEdgeBodyDist<-100 || Root,MoveType=H || RoundState!=2');return s

def helpers():
 states.append(moving_helper(9400,8610,105,14)+c(9400,'Thin blue Chidori senbon','AngleDraw','1','value=0\nscale=.75,.38'))
 states.append(moving_helper(9430,8611,180,10)+c(9430,'Original wood arm','AngleDraw','1','value=0\nscale=.82,.82'))
 states.append(moving_helper(9420,8620,185,11,False,60)+c(9420,'Electric discharge','AngleDraw','1','value=0\nscale=1.15,.75'))
 states.append(moving_helper(9431,8611,145,10)+c(9431,'Expanded wood palm','AngleDraw','1','value=0\nscale=.9,.9'))
 states.append(moving_helper(9441,8611,78,10,False,36)+c(9441,'Wood palm projectile','AngleDraw','1','value=0\nscale=.7,.7'))
 states.append(moving_helper(9470,8645,205,14)+c(9470,'Broad golden sword wave','AngleDraw','1','value=0\nscale=1.2,2.4'))
 states.append(moving_helper(9471,8645,87,16,False,40)+c(9471,'Arrow descends from the visible bow toward chest height','VelSet','Time=0','y=(-27-Pos Y)/IfElse(Abs(P2Dist X)>16,Abs(P2Dist X)/16.0,1)')+c(9471,'Arrow follows its actual velocity','AngleDraw','1','value=-ATan(Vel Y/16.0)*180/Pi'))
 fxaction(8646,8645,range(4),3,box='-10,0,10,90',loop=True)
 n=9472;s=state(n,8646,'A','A','N',vel='0,11')+c(n,'Golden sword rain points down','AngleDraw','1','value=-90')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+hit(n,0,85,False,airborne=True,stun=38).replace('attr=A,SA','attr=A,SP')+c(n,'Rain ends at contact or the floor','DestroySelf','MoveContact || Pos Y>=0 || Time>=25 || Root,MoveType=H || RoundState!=2');states.append(s)
 states.append(moving_helper(9473,8611,190,10,False,55)+c(9473,'Golden chakra palm','PalFX','1','time=1\ncolor=0\nmul=256,240,32')+c(9473,'Expanded guardian palm','AngleDraw','1','value=0\nscale=1.2,1.2'))

 n=9440;s=state(n,8612,'A','A','N')+c(n,'Root claw grows from floor','AngleDraw','1','value=0\nscale=.3+IfElse(Time<15,Time,15)*.085,.3+IfElse(Time<15,Time,15)*.085')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
 for i,t in enumerate([12,56]):s+=hit(n,t,f'IfElse(Root,Var(42),{160 if i==0 else 120},{130 if i==0 else 85})',bool(i),airborne=True,stun=50).replace('attr=A,SA','attr=A,SP')
 s+=effect(n,'Time=56',8670,0,0,.85,22)+c(n,'Root bind is finite','DestroySelf','Time>=80 || Root,MoveType=H || RoundState!=2');states.append(s)
 n=9450;s=state(n,8620,'A','A','N')+c(n,'Vertical Chidori pillar','AngleDraw','1','value=90\nscale=1.2,.65')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
 # A vertical drawing needs its own vertical collision action, not a rotated
 # horizontal hitbox (AngleDraw only rotates the visual in MUGEN).
 fxaction(8621,8640,range(8),3,box='-32,-110,32,0',loop=True,add='AS256D96');s=s.replace('anim=8620','anim=8621')
 for i,t in enumerate([3,21,39]):s+=hit(n,t,[55,65,115][i],i==2,airborne=True,stun=30).replace('attr=A,SA','attr=A,SP')
 s+=snd(n,'Time=0',1,42,2)+c(n,'Pillar dissipates','DestroySelf','Time>=57 || Root,MoveType=H || RoundState!=2');states.append(s)
 n=9550;s=state(n,8900,'A',physics='N')+c(n,'Energy follows body','BindToRoot','1','time=1\npos=0,-38')+c(n,'Energy envelope','AngleDraw','1','value=90\nscale=.32,.36')+c(n,'Blue chakra, gold during awakening','PalFX','1','time=1\ncolor=0\nmul=IfElse(Root,Var(42),256,80),IfElse(Root,Var(42),220,160),IfElse(Root,Var(42),30,256)')+c(n,'Chakra blend','Trans','1','trans=AddAlpha\nalpha=160,256')+c(n,'Behind body','SprPriority','1','value=-2')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'Charge aura cleanup','DestroySelf','trigger1=Root,StateNo!=500 && Root,StateNo!=520\ntrigger2=Root,Life<=0\ntrigger3=RoundState!=2');states.append(s)

def guardian():
 n=9500;s=state(n,9630,'A',physics='N')+c(n,'Follow real body in air and on floor','BindToRoot','1','time=1\npos=0,0')+c(n,'Follow both facing directions','Turn','Facing!=Root,Facing','')+c(n,'Read current technique','VarSet','1','v=0\nvalue=Root,StateNo%10000')+c(n,'Read technique phase','VarSet','1','v=1\nvalue=Root,Time')
 # 0 guard, 1 raise, 2 slash, 3 cleave, 4 hand, 5 brace, 6 bow, 7 release.
 pose='IfElse(Root,MoveType=H,5,IfElse(Var(0)=3001,IfElse(Var(1)<40,1,IfElse(Var(1)<85,2,IfElse(Var(1)<135,3,7))),IfElse(Var(0)=1000,IfElse(Var(1)<14,1,IfElse(Var(1)<45,4,0)),IfElse(Var(0)=1010 || Var(0)=1050 || Var(0)=1440 || Var(0)=1211,IfElse(Var(1)<18,1,IfElse(Var(1)<65,2,0)),IfElse(Var(0)=1020 || Var(0)=1200,IfElse(Var(1)<22,6,IfElse(Var(1)<60,7,0)),IfElse(Var(0)=1040 || Var(0)=1430 || Var(0)=1420,IfElse(Var(1)<18,1,IfElse(Var(1)<70,3,0)),IfElse(Var(0)=1030 || Var(0)=1400 || Var(0)=1410,IfElse(Var(1)<15,0,IfElse(Var(1)<70,4,0)),IfElse(Var(0)>=200 && Var(0)<=222,IfElse(Var(1)<4,1,2),0))))))))'
 s+=c(n,'Pose follows the active technique','VarSet','1','v=2\nvalue=9630+'+pose)+c(n,'Change guardian pose only when necessary','ChangeAnim','Anim!=Var(2)','value=Var(2)')+c(n,'Open and breathe without enlarging Hidari','AngleDraw','1','value=0\nscale=IfElse(Time<14,.25+Time*.05357,1),IfElse(Time<14,.25+Time*.05357,1)')+c(n,'Golden translucent guardian','Trans','1','trans=AddAlpha\nalpha=210,160')+c(n,'Keep original Hidari in front','SprPriority','1','value=-1')+c(n,'Guardian is not a second fighter','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'Clean guardian on expiry, death and round end','DestroySelf','trigger1=Root,Var(42)=0\ntrigger2=Root,Life<=0\ntrigger3=RoundState!=2');states.append(s)

def claws():
 for form in [0,1]:
  off=form*10000;n=1210+off;action(n,[(51,10),(52,16),(53,18),(0,10)]);s=state(n,n,move='A',cost=200 if form else 250)+startup(n)+cast(n,12,9600,'IfElse(P2Dist X<180,P2Dist X,180)',0)+snd(n,'Time=12',1,32,1)+recover(n,54);states.append(s)
  for base,cost in [(1211,200),(1440,400)]:
   n=base+off;action(n,[(51,8),(54,5),(55,5),(56,5),(57,6),(58,6),(59,6),(60,6),(61,6),(62,12),(0,12)],box='0,-68,90,-4');s=state(n,n,move='A',cost=round(cost*.8) if form else cost,physics='N')+startup(n)
   s+=cast(n,5,9600,'IfElse(P2Dist X<180,P2Dist X,180)',0).replace('trigger1=Time=5','trigger1=Time=5 && NumHelper(9600)=0')+c(n,'Travel to a placed visible claw mark','PosSet','Time=22 && NumHelper(9600)>0','x=(Helper(9600),Pos X)-Facing*32\ny=0')+c(n,'Face opponent after the exit','Turn','Time=23 && P2Dist X<0','')+c(n,'Claw transit','PlayerPush','Time>=14 && Time<=25','value=0')+c(n,'Brief opening passage','NotHitBy','Time>=16 && Time<=24','value=SCA\ntime=1')+effect(n,'Time=21',8613,0,-32,.7,18)+snd(n,'Time=22',1,32,1)+hit(n,35,180 if form else 140,True)+recover(n,78);states.append(s)
 n=9600;s=state(n,8613,'A',physics='N')+c(n,'Original crossed claw bands','AngleDraw','1','value=0\nscale=.75,.8')+c(n,'Floor layer','SprPriority','1','value=-2')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'Consumed mark has finite lifetime','DestroySelf','trigger1=Time>=600\ntrigger2=RoundState!=2\ntrigger3=Root,StateNo%10000=1211 || Root,StateNo%10000=1440\ntrigger3=Root,Time>=24');states.append(s)

def utility():
 for n in [170,180,190]:
  s=state(n,f'{n}+10000*Var(42)')+c(n,'Original round pose','Null','1')
  if n==190:s+=c(n,'Intro','AssertSpecial','Time<40','flag=Intro')+recover(n,46)
  states.append(s)
 s=state(500,'500+10000*Var(42)')+c(500,'Hold energy charge','PowerAdd','1','value=22')+snd(500,'Time=0',1,4,3,60)+cast(500,0,9550,0,-38).replace('trigger1=Time=0','trigger1=Time=0 && NumHelper(9550)=0')+effect(500,'Time%14=0',8910,0,0,.35,14)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=70','value=0\nctrl=1');states.append(s)
 s=state(520,520)+startup(520)+c(520,'Susanoo consumes energy','PowerAdd','Time=0','value=-1500')+effect(520,'Time=12',8720,0,-40,1,22)+effect(520,'Time=28',8670,0,0,.8,20)+snd(520,'Time=28',1,41,2)+c(520,'Yellow Susanoo activation','VarSet','Time=28','v=42\nvalue=1')+c(520,'Susanoo duration','VarSet','Time=28','v=40\nvalue=1200')+c(520,'Susanoo cooldown','VarSet','Time=28','v=41\nvalue=1500')+cast(520,8,9550,0,-38).replace('trigger1=Time=8','trigger1=Time=8 && NumHelper(9550)=0')+recover(520,60);states.append(s)

def ultimate():
 for form in [0,1]:
  off=form*10000;n=3000+off;action(n,[(28,8),(29,12),(30,14),(28,20)],box='0,-65,80,-4');s=state(n,n,move='A',cost=3000,physics='N')+startup(n)+blue(n,'Time=8',60,-45,.3,28)
  s+=c(n,'Opening Chidori has actual travel','VelSet','Time>=8 && Time<28','x=6')+c(n,'Stop if opening misses','VelSet','Time>=28','x=0')+hit(n,8,0,starter=True)+c(n,'Only a hit confirms the ultimate','ChangeState','MoveHit && NumTarget(3000)>0',f'value={3001+off}')+recover(n,56);states.append(s)
  n=3001+off;action(n,[(51,10),(54,5),(55,5),(56,5),(57,5),(58,8),(59,8),(62,10),(29,12),(30,12),(49,12),(50,12),(34,10),(35,12),(39,10),(41,12),(43,12),(0,14)])
  s=state(n,n,physics='N')+c(n,'Finite hit-confirmed scene','Pause','Time=0','time=190\nmovetime=190\npausebg=1')+c(n,'Protection only during confirmed scene','NotHitBy','Time<184','value=SCA\ntime=1')+c(n,'Store actual victim position','VarSet','Time=0 && NumTarget(3000)>0','fv=5\nvalue=Target(3000),Pos X')+c(n,'Bind only the struck enemy','TargetBind','Time<180 && NumTarget(3000)>0','ID=3000\ntime=1\npos=(FVar(5)-Pos X)*Facing,0')+c(n,'Dim stage briefly','BGPalFX','Time=0','time=180\nmul=80,85,105')
  s+=c(n,'Cross through the mark beside the real victim','PosSet','Time=40','x=FVar(5)-Facing*54\ny=0')+effect(n,'Time=26',8613,18,-38,.95,26)+snd(n,'Time=40',1,32,2)
  cap=450 if form else 420;ratio='.45' if form else '.42'
  s+=c(n,'Life-relative damage ceiling','VarSet','Time=0 && NumTarget(3000)>0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{cap},Floor((Target(3000),LifeMax)*{ratio}))')
  for i,t in enumerate([50,76,102,132,164]):
   s+=effect(n,f'Time={t}',8720 if form or i==4 else 8625,'(FVar(5)-Pos X)*Facing',-30,1.2 if i==4 else .65,22)+snd(n,f'Time={t}',1,41 if i==4 else 42,1)+c(n,'Bounded target-only damage','TargetLifeAdd',f'Time={t} && NumTarget(3000)>0','ID=3000\nvalue=-'+('(Var(20)-Floor(Var(20)/5)*4)' if i==4 else 'Floor(Var(20)/5)')+'\nabsolute=1\nkill=1')+c(n,'Cleave impact','EnvShake',f'Time={t}','time=9\nfreq=65\nampl=-5')
  if not form:s+=effect(n,'Time=112',8612,'(FVar(5)-Pos X)*Facing',0,1.6,58)
  s+=c(n,'Always release the victim','TargetState','Time=180 && NumTarget(3000)>0','ID=3000\nvalue=3011')+recover(n,194);states.append(s)
 for n in [3010,3011]:
  s=state(n,None,'S','H','N')+c(n,'Victim keeps own body sprite','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')
  if n==3010:s+=c(n,'Failsafe release','SelfState','Time>=240 || NumEnemy=0','value=0\nctrl=1')
  else:s+=c(n,'Return to own fall','SelfState','Time>=1','value=5050\nctrl=0')+c(n,'Throw velocity','VelSet','Time=0','x=-6\ny=-7')
  states.append(s)
def common():
 # Reuse the project's tested native guard, fall and dash states; all animation
 # choices are now form-aware and remain independent of another character file.
 s=(ROOT/'JuraShinju/JuraShinju_common.cns').read_text().replace('; Jura common states, derived from project native MUGEN guard and recovery.','; Hidari native guard, fall and dash states, derived from the project common implementation.')
 s=re.sub(r'(?m)^anim\s*=\s*(\d+)\s*$',r'anim=\1+10000*Var(42)',s)
 blocks=re.split(r'(?=\n\[State )',s);out=[]
 for block in blocks:
  if re.search(r'(?im)^type\s*=\s*ChangeAnim\s*$',block):
   block=re.sub(r'(?m)^value\s*=\s*(.+)$',r'value=(\1)+10000*Var(42)',block)
   block=block.replace('Anim != IfElse(Vel X<0,21,20)','Anim != IfElse(Vel X<0,21,20)+10000*Var(42)').replace('Anim != 44','Anim != 44+10000*Var(42)')
  out.append(block)
 (CHAR/'HidariShinju_common.cns').write_text(''.join(out))

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
 s+=ctl(-1,'Yellow Susanoo awakening','ChangeState','triggerall=AILevel=0\ntriggerall=command="s"\ntriggerall=command="holddown"\ntriggerall=Power>=3000\ntriggerall=Var(42)=0\ntriggerall=Var(41)=0\ntriggerall=StateType!=A\ntrigger1=ctrl','value=520')
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
 (CHAR/'HidariShinju.cmd').write_text(s.rstrip()+'\n')


def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite Susanoo timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe awakening expiry','VarSet','!IsHelper && Var(42)>0 && Var(40)=0 && Ctrl && MoveType!=H && StateNo!=500','v=42\nvalue=0')+c(-2,'Refresh form after expiry','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')+c(-2,'Keep original body animation through turn','ChangeAnim','!IsHelper && Var(42)=1 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+c(-2,'Aerial chain reset','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge hum','StopSnd','!IsHelper && StateNo!=500','channel=3')
 s+=c(-2,'Create exactly one yellow Susanoo','Helper','!IsHelper && RoundState=2 && Var(42)=1 && NumHelper(9500)=0','helpertype=Normal\nname="Susanoo amarillo"\nID=9500\nstateno=9500\npostype=P1\npos=0,0\nownpal=1\nkeyctrl=0\npausemovetime=240\nsupermovetime=240')+c(-2,'Round form cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round drawing cleanup','RemoveExplod','!IsHelper && RoundState!=2')
 s+=c(-2,'Only Susanoo is visible during awakening','AssertSpecial','!IsHelper && Var(42)=1','flag=Invisible\nflag2=NoShadow','ignorehitpause=1')
 return s

def main():
 animations();normals();techniques();claws();helpers();guardian();utility();ultimate();common();commands()
 import sys
 import build_hidari_susanoo
 build_hidari_susanoo.install(sys.modules[__name__])
 import hidari_katon_source
 hidari_katon_source.install(sys.modules[__name__])
 constants=(ROOT/'JuraShinju/JuraShinju.cns').read_text().split('[Statedef',1)[0];constants=constants[constants.index('[Data]'):].replace('life=1300','life=1250').replace('defence=115','defence=110').replace('height=84','height=83')
 (CHAR/'HidariShinju.cns').write_text(('; Hidari: original Vaydra sprites, blue Rinnegan, Chidori and golden Susanoo.\n'+constants+''.join(states)+system()).rstrip()+'\n')
 (CHAR/'HidariShinju.air').write_text(('; Original body group 0; supplemental yellow Susanoo is a separate guardian.\n'+''.join(air)).rstrip()+'\n')
 d=(ROOT/'JuraShinju/JuraShinju.def').read_text().replace('JuraShinju','HidariShinju').replace('Jura Shinju','Hidari Shinju').replace('versiondate=10,22,2026','versiondate=10,23,2026').replace('Vahidras / Vaydra (sprites), Codex (fan adaptation)','Vaydra (Hidari), Vovan99 / Shingeki No Mugen (Susanoo), Codex (adaptation)');(CHAR/'HidariShinju.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,form_offset=10000,awakening='Yellow Susanoo; requested fan adaptation',awakening_ticks=1200,awakening_cost=1500,activation_requires=3000,ultimate_cost=3000,ultimate_budget='min(420,42% opponent max life)',awakened_ultimate_budget='min(450,45% opponent max life)',rinnegan='blue iris, source body otherwise preserved',voices=False),indent=2)+'\n');build_hidari_susanoo.patch_commands();print(len(states),'combat states,',len(air),'actions')
if __name__=='__main__':main()
