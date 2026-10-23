#!/usr/bin/env python3
"""Standalone MUGEN 1.1 Mitsuki TBV: distinct base and Sage combat."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MitsukiTBV'
MOVES=[('Brazos','a','F',1000,350),('Serpientes','a','B',1010,400),('Raiton','b','F',1020,500),('Fuuton','b','B',1030,450),('Ascenso','c','F',1040,450),('Cerco','c','B',1050,600),('Barrido','a','D',1400,200),('Lanzador','b','D',1410,300),('Atadura','c','D',1420,350),('SerpienteRapida','y','N',1200,200),('Asalto','z','N',1210,350),('PalmaRaiton','y','D',1430,550),('Sustitucion','z','D',1440,400)]
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
def snd(n,t,g,no,channel=0,volume=80):return c(n,'Original voice' if g==0 else 'Technique sound','PlaySnd',t,f'value=S{g},{no}\nchannel={channel}\nvolumescale={volume}')
def startup(n,voice=5):return snd(n,'Time=0',1,21,4,75)+snd(n,'Time=0',0,voice)+c(n,'Technique activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')+effect(n,'Time=0',8710,6,-45,.65,8)
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
def snake(n,t,form=0,x=25,y=-35,strong=False,stationary=False,stun=False):
 sn=(9410 if strong else 9400)+form
 return c(n,'Visible autonomous serpent','Helper',f'Time={t} && NumHelper({sn})<5',f'helpertype=Normal\nname="Serpiente"\nID={sn}\nstateno={sn}\npostype=P1\npos={x},{y}\nfacing=1\nkeyctrl=0\nownpal=1')
def animations():
 base={0:[(0,10),(1,10),(2,10)],5:[(0,6)],6:[(16,6)],10:[(16,5)],11:[(16,5)],12:[(16,5)],20:[(3,5),(4,5),(5,5),(6,5),(7,5),(8,5)],21:[(8,6),(7,6),(6,6)],40:[(24,4)],41:[(48,7)],44:[(52,7)],52:[(53,7),(0,3)],100:[(3,4),(4,4),(5,6)],105:[(8,4),(7,4),(6,6)],170:[(14,30)],180:[(66,12),(57,60),(54,60)],190:[(54,12),(55,10),(56,10),(0,12)],500:[(54,8),(55,8),(56,8)],520:[(54,8),(55,10),(56,12),(0,10)],5000:[(9,8),(10,8)],5010:[(16,8)],5020:[(11,8)],5030:[(12,7),(13,7)],5100:[(14,10)],5110:[(14,28)],5120:[(15,7),(16,7),(0,5)],5150:[(14,60)],5200:[(48,8)],5210:[(48,8)],5300:[(9,20)]}
 for n in [120,130,140,150]:base[n]=[(9,5)]
 for n in [121,131,141,151]:base[n]=[(16,5)]
 for n in [122,132,142,152]:base[n]=[(50,5)]
 for n,poses in base.items():
  action(n,poses,loop=n in [0,11,20,21,41,44,500,5150])
  if n==520:continue
  if n in [20,21,100,105]:sp=[(5,5),(6,5),(7,5)]
  elif n in [0,180,190]:sp=[(0,10),(1,10),(2,10)]
  elif n in [500,5300] or n>=5000:sp=[(3,10),(4,10)]
  elif n in [41,44,40,52]:sp=[(12,8),(13,8)]
  else:sp=[(8,8)]
  action(n+10000,sp,1,loop=n in [0,11,20,21,41,44,500,5150])
 fxaction(8700,8700,range(4),3,add=True);fxaction(8710,8710,range(4),2,add=True);fxaction(8720,8720,range(6),3,add=True)
 fxaction(8601,8600,[5,6,8,5],3,box='-36,-23,36,23',loop=True)
 fxaction(8611,8610,[12,13,12,13],3,box='-68,-16,68,16',loop=True)
 fxaction(8602,8600,[5,8,6,5],4)
 fxaction(8612,8610,[12,13,10,11],4)
 fxaction(8930,8930,range(8),2,box='0,-20,230,20',loop=True,add=True)
 fxaction(8931,8931,range(8),2,box='0,-20,280,20',loop=True,add=True)
 fxaction(8932,8932,range(8),2,box='0,-14,108,14',loop=True,add=True)
 fxaction(8950,8950,range(8),2,box='0,-14,108,14',loop=True,add='AS256D96')
 fxaction(8951,8941,range(4),2,add='AS256D0')
 for n in [8940,8941]:fxaction(n,n,range(4),3,box='-40,-88,40,-3',loop=True)
 for n,g,count in [(8630,8630,21),(8640,8640,9),(8650,8650,28),(8660,8660,9),(8670,8670,11),(8680,8680,4),(8820,8820,5),(8900,8900,24),(8910,8910,5)]:fxaction(n,g,range(count),2 if n!=8900 else 3,loop=n==8900,add=n not in [8680])
 # Wind has its own contact area, rather than an invisible full-screen hit.
 fxaction(8631,8630,range(21),2,box='-38,-48,38,8',loop=True,add=True)

def normals():
 for form in [0,1]:
  off=form*10000
  for b,base in enumerate([200,210,220]):
   for step in range(3):
    n=off+base+step
    p=([(17,3),(18+step,8),(17,8)] if b==0 else [(24,3),(25+step if step<2 else 29,8),(24,8)] if b==1 else [(31,3),(32+step,8),(17,8)]) if not form else [(8,3),([9,10,11][step] if b==0 else [12,13,14][step] if b==1 else [16,17,18][step],8),(8,8)]
    action(n,p,form,box='4,-65,67,-8')
    s=state(n,n,move='A',vel='2.5,0')+snd(n,'Time=1',0,[12,13,9][step],0,65)+snd(n,'Time=3',1,0,1,60)+hit(n,3,([42,48,68] if not form else [52,60,90])[step],step==2)
    if form and step==2:s+=snake(n,5,1,40,-35)
    s+=c(n,'Short approach ends','VelSet','Time>=7','x=0')+recover(n,19);states.append(s)
  for b,base in enumerate([600,610,620]):
   for step in range(3):
    n=off+base+step;p=([(48,3),([50,51,52][step],8),(49,7)] if not form else [(12,3),([13,14,17][step],8),(12,7)])
    action(n,p,form,box='-4,-65,67,-3')
    s=state(n,n,'A','A','N',vel=None)+c(n,'Consume finite air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief juggle hover','VelSet','Time<7','x=1.8\ny=-.5')+c(n,'Resume gravity','VelAdd','Time>=7','y=.48')+hit(n,3,([40,47,70] if not form else [50,60,85])[step],step==2,airborne=True)
    if form and step==2:s+=snake(n,5,1,38,-32)
    s+=c(n,'Land safely','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+recover(n,18,True);states.append(s)

def techniques():
 for form in [0,1]:
  off=form*10000
  for name,button,d,base,cost in MOVES:
   n=off+base;price=round(cost*.8) if form else cost
   start,cast,ready=(54,57,17) if not form else (15,17,8)
   if base==1440:continue
   if base in [1000,1210]:
    if base==1000:
     poses=[(17,8),(64,8),(65,10),(66,8),(20,10),(17,12)] if not form else [(8,8),(9,10),(10,10),(11,10),(14,12),(8,12)]
    else:
     poses=[(35,8),(36,6),(37,6),(38,6),(39,6),(40,6),(41,6),(42,6),(43,6),(17,10)] if not form else [(8,8),(3,10),(4,10),(12,10),(14,10),(8,18)]
    action(n,poses,form,box='2,-66,76,-5');s=state(n,n,move='A',cost=price,physics='N')+startup(n,5)
    s+=c(n,'Forward assault','VelSet','Time>=8 && Time<38',f'x={4.5 if form else 3.5}')+c(n,'Stop rush','VelSet','Time>=38','x=0')
    for i,t in enumerate([8,21,34]):s+=hit(n,t,([45,50,80] if not form else [48,58,92])[i],i==2)
    if form:s+=snake(n,17,1,45,-30)+snake(n,36,1,55,-32)
    if base==1210:
     for t in [8,21,34]:s+=effect(n,f'Time={t}',8660,30,0,.7,18)
    s+=recover(n,66);states.append(s);continue
   if base==1020:
    # A moving lightning lance, rather than another punching rush.
    action(n,[(44,8),(45,8),(47,20),(44,14),(0,10)] if not form else [(8,8),(12,8),(14,22),(13,12),(8,10)],form)
    s=state(n,n,move='A',cost=price)+startup(n,18)
    technique='Senpo: Orochi Ikazuchi' if form else 'Raiton Hebi Mikazuchi'
    s+=c(n,'Launch Raiton lance','Helper','Time=16',f'helpertype=Normal\nname="{technique}"\nID={9432+form}\nstateno={9432+form}\npostype=P1\npos=27,-34\nownpal=1\nkeyctrl=0')
    s+=effect(n,'Time=16',8951 if form else 8650,29,-36,.55 if form else .8,12)+snd(n,'Time=16',1,42,1)+recover(n,60);states.append(s);continue
   if base in [1040,1400,1410]:
    if base==1400:
     poses=[(16,7),(53,10),(43,8),(16,8),(0,10)] if not form else [(8,7),(5,10),(7,8),(12,8),(8,10)]
     action(n,poses,form,box='0,-29,66,-2')
     s=state(n,n,move='A',cost=price,physics='N')+startup(n,9)
     s+=c(n,'Low forward slide','VelSet','Time>=7 && Time<23',f'x={7 if form else 6}\ny=0')+c(n,'Slide brakes','VelSet','Time>=23','x=0\ny=0')
     s+=hit(n,7,125 if form else 105,True,low=True)+effect(n,'Time=7',8670,0,0,.45,20)
     if form:s+=snake(n,12,1,35,-13)
     s+=recover(n,43);states.append(s);continue
    poses=([(24,8),(25,7),(28,7),(29,7),(30,10),(53,10)] if base==1040 else [(31,7),(35,6),(37,10),(36,8),(17,12)]) if not form else ([(8,8),(3,7),(4,7),(12,7),(14,10),(8,12)] if base==1040 else [(15,7),(12,6),(13,10),(14,8),(8,12)])
    action(n,poses,form,box='-4,-78,73,-2');s=state(n,n,move='A',cost=price,physics='N')+startup(n,9)
    launch=8 if base==1040 else 7
    s+=c(n,'Rising crescent' if base==1040 else 'Upward palm','VelSet',f'Time={launch}',f'x={3 if base==1040 else 1.4}\ny={-6 if base==1040 else -4}')
    s+=c(n,'Become airborne','StateTypeSet',f'Time={launch}','statetype=A\nphysics=N')+c(n,'Finite rise and fall','VelAdd',f'Time>{launch}','y=.42')
    s+=hit(n,launch,65 if base==1040 else 145 if form else 120,base!=1040,airborne=True)
    if base==1040:s+=hit(n,17,105 if form else 85,True,airborne=True)+effect(n,'Time=8',8660,25,-6,.65,22)
    else:s+=effect(n,'Time=7',8710,20,-62,.8,14)
    if form:s+=snake(n,launch,1,30,-58)
    s+=c(n,'Land with control','ChangeState',f'Time>{launch+8} && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+recover(n,70,True);states.append(s);continue
   if base==1430:
    # Down+RB is a sustained ranged beam, not a melee palm hitbox.
    action(n,[(54,8),(55,10),(47,32),(44,10),(0,10)] if not form else [(15,8),(16,10),(14,32),(13,10),(8,10)],form)
    s=state(n,n,move='A',cost=price)+startup(n,18)
    s+=c(n,'Emit continuous Raiton beam','Helper','Time=18',f'helpertype=Normal\nname="Rayo Raiton"\nID={9430+form}\nstateno={9430+form}\npostype=P1\npos=27,-34\nownpal=1\nkeyctrl=0')
    s+=snd(n,'Time=18',1,43,1)+effect(n,'Time=18',8650,29,-36,.85,26)+recover(n,70);states.append(s);continue
   if base==1050:
    # A rooted trap around a nearby target; it does not shoot the same volley.
    action(n,[(54,10),(55,10),(56,12),(53,28),(54,12)] if not form else [(15,10),(16,10),(3,12),(4,28),(8,12)],form)
    s=state(n,n,move='A',cost=price)+startup(n,6)
    s+=c(n,'Bounded visible trap position','VarSet','Time=16','v=23\nvalue=Floor(IfElse(P2Dist X<45,45,IfElse(P2Dist X>180,180,P2Dist X)))')
    s+=c(n,'Rooted serpent coils','Helper','Time=20',f'helpertype=Normal\nname="Cerco de serpientes"\nID={9440+form}\nstateno={9440+form}\npostype=P1\npos=Var(23),0\nownpal=1\nkeyctrl=0')+effect(n,'Time=20',8670,'Var(23)',0,.55,18)+recover(n,72);states.append(s);continue
   if base==1420:
    action(n,[(64,8),(65,10),(57,20),(66,14),(17,12)] if not form else [(15,8),(12,10),(14,20),(17,14),(8,12)],form)
    s=state(n,n,move='A',cost=price)+startup(n,7)+snake(n,18,form,35,-28,strong=True)
    if form:s+=snake(n,30,1,35,-20,strong=True)
    s+=recover(n,64);states.append(s);continue
   if base==1200:
    action(n,[(31,5),(34,8),(57,12),(17,10)] if not form else [(8,5),(12,8),(14,12),(8,10)],form)
    s=state(n,n,move='A',cost=price)+startup(n,7)+snake(n,9,form,28,-28)
    if form:s+=snake(n,20,1,28,-25)
    s+=recover(n,38);states.append(s);continue
   action(n,[(start,8),(55 if not form else 16,10),(cast,42 if form else 34),(ready,12)],form)
   s=state(n,n,move='A',cost=price)+startup(n,21 if base==1030 else 6)
   if base==1030:
    for t in ([18] if not form else [18,32,46]):s+=c(n,'Fuuton current','Helper',f'Time={t} && NumHelper(9420)<3','helpertype=Normal\nname="Fuuton Toppa"\nID=9420\nstateno=9420\npostype=P1\npos=42,-15\nownpal=1\nkeyctrl=0')
    s+=snd(n,'Time=18',1,30,1)
   else:
    for i,t in enumerate([18,31,44] if not form else [14,25,36,47]):
     s+=snake(n,t,form,30+i*13,[-19,-34,-48,-28][i])+effect(n,f'Time={t}',8670,30,0,.3,12)
   s+=recover(n,76 if form else 70);states.append(s)
  n=off+1440;action(n,[(54 if not form else 15,8),(55 if not form else 16,24),(17 if not form else 8,12)],form,box='-22,-76,22,-1')
  s=state(n,n,cost=320 if form else 400)+startup(n,15)+effect(n,'Time=8',8680,0,-5,.8,24)
  s+=c(n,'Finite substitution counter','ReversalDef','Time>=8 && Time<=28',f'reversal.attr=SCA,NA,SA,HA\npausetime=0,10\nsparkno=S8700\nhitsound=S1,32\np1stateno={off+1441}')+recover(n,44);states.append(s)
  n=off+1441;action(n,[(31 if not form else 16,6),(34 if not form else 17,20),(17 if not form else 8,12)],form,box='-8,-65,80,-4')
  states.append(state(n,n,move='A',physics='N',vel='5,0')+effect(n,'Time=0',8680,0,-5,1,16)+c(n,'Brief escape','NotHitBy','Time<10','value=SCA\ntime=1')+hit(n,6,165 if not form else 215,True)+snake(n,8,form,30,-28)+recover(n,38))

def lightning_helpers():
 for form in [0,1]:
  n=9430+form
  s=state(n,8930+form,'A','A','N')+c(n,'Beam stays attached to casting hand','BindToRoot','1','time=1\npos=27,-34')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
  for i,t in enumerate([0,8,16]):
   s+=hit(n,t,[65,70,85][i]+(15 if form else 0),i==2,airborne=True,stun=28).replace('attr=A,SA','attr=A,SP')
  s+=ctl(n,'Beam ends on recovery or interruption','DestroySelf','trigger1=Time>=25\ntrigger2=Root,StateNo%10000!=1430\ntrigger3=RoundState!=2');states.append(s)
  n=9432+form
  s=state(n,8950 if form else 8932,'A','A','N',vel=f'{14 if form else 11},0')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
  s+=hit(n,0,210 if form else 170,True,airborne=True).replace('attr=A,SA','attr=A,SP')+c(n,'Moving Raiton cleanup','DestroySelf','MoveContact || Time>=32 || FrontEdgeBodyDist<-120 || RoundState!=2');states.append(s)
  n=9440+form
  s=state(n,8940+form,'A','A','N')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
  for i,t in enumerate([4,14,24]):s+=hit(n,t,95 if form else 75,i==2,airborne=True,stun=26).replace('attr=A,SA','attr=A,SP')
  s+=c(n,'Trap has a fixed short duration','DestroySelf','Time>=34 || RoundState!=2');states.append(s)

def helpers():
 for form in [0,1]:
  for strong in [False,True]:
   n=(9410 if strong else 9400)+form
   s=state(n,8611 if form else 8601,'A','A','N',vel=f'{7 if form else 6},0')
   s+=c(n,'Serpent has no push or shadow','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
   s+=c(n,'Visible snake contact','HitDef','Time=0',f'attr=A,SP\ndamage={95 if strong and form else 80 if strong else 48 if form else 62},3\nguardflag=MA\nhitflag=MAF\npriority=5,Hit\npausetime=0,9\nsparkno=S8700\nhitsound=S1,7\nguardsound=S1,9\nground.type=High\nground.hittime={55 if strong else 30}\nground.slidetime=20\nground.velocity={-.1 if strong else -.7},0\nair.velocity=-2,-2\nfall=0\nfall.recover=1\nfall.recovertime=45\ngetpower=0,0\ngivepower=8,5')
   if strong:
    s+=c(n,'Visible binding coils on the struck opponent','Explod','MoveHit','anim='+str(8940+form)+'\nID=9490\npostype=P2\npos=0,0\nscale=.6,.6\nremovetime=38\nbindtime=38\nownpal=1\nsprpriority=4\nremoveongethit=0','persistent=0')
   s+=c(n,'Serpents disperse on real contact','DestroySelf','MoveContact || Time>=42 || FrontEdgeBodyDist<-60 || RoundState!=2')
   states.append(s)
 n=9420;s=state(n,8631,'A','A','N',vel='8,0')+c(n,'Scale wind','AngleDraw','1','value=0\nscale=.55,.55')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
 s+=c(n,'Finite wind impact','HitDef','Time=0','attr=A,SP\ndamage=95,4\nguardflag=MA\nhitflag=MAF\npriority=5,Hit\npausetime=0,8\nsparkno=S8700\nhitsound=S1,30\nguardsound=S1,9\nground.type=High\nground.hittime=32\nground.velocity=-3,-4\nair.velocity=-3,-3\nfall=1\nfall.recover=1\ngetpower=0,0\ngivepower=8,5')+c(n,'Finite wind cleanup','DestroySelf','MoveContact || Time>=38 || FrontEdgeBodyDist<-60 || RoundState!=2');states.append(s)
 n=9550;s=state(n,8900,'A',physics='N')+c(n,'Follow caster','BindToRoot','1','time=1\npos=0,-38')+c(n,'Upright chakra','AngleDraw','1','value=90\nscale=.32,.34')+c(n,'Mint chakra','PalFX','1','time=1\ncolor=0\nmul=80,256,180')+c(n,'Chakra blend','Trans','1','trans=AddAlpha\nalpha=160,256')+c(n,'Aura behind sprite','SprPriority','1','value=-2')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'Aura cleanup','DestroySelf','trigger1=Root,StateNo!=500 && Root,StateNo!=520 && Root,Var(42)=0\ntrigger2=Root,Life<=0\ntrigger3=RoundState!=2');states.append(s)

def utility():
 for n in [170,180,190]:
  s=state(n,f'{n}+10000*Var(42)')+c(n,'Round pose','Null','1')
  if n==190:s+=snd(n,'Time=2',0,4)+c(n,'Introduction','AssertSpecial','Time<40','flag=Intro')+recover(n,44)
  if n==180:s+=snd(n,'Time=12',0,20)
  if n==170:s+=snd(n,'Time=0',0,17)
  states.append(s)
 s=state(500,'500+10000*Var(42)')+c(500,'Charge meter','PowerAdd','1','value=22')+snd(500,'Time=0',0,2)+snd(500,'Time=0',1,4,3,60)
 s+=c(500,'Charge aura','Helper','Time=0 && NumHelper(9550)=0','helpertype=Normal\nname="Chakra Mitsuki"\nID=9550\nstateno=9550\npostype=P1\npos=0,-38\nownpal=1\nkeyctrl=0')+effect(500,'Time%14=0',8910,0,0,.3,14)
 s+=ctl(500,'Release charging','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=70','value=0\nctrl=1');states.append(s)
 s=state(520,520)+startup(520,1)+c(520,'Sage awakening cost','PowerAdd','Time=0','value=-1500')
 s+=effect(520,'Time=8',8720,0,-40,1,22)+effect(520,'Time=24',8670,0,0,.8,20)
 s+=c(520,'Start genuine Sage form','VarSet','Time=28','v=42\nvalue=1')+c(520,'Sage duration','VarSet','Time=28','v=40\nvalue=1200')+c(520,'Cooldown','VarSet','Time=28','v=41\nvalue=1500')
 s+=c(520,'Sage manifestation','ChangeAnim','Time=28','value=10500')+c(520,'Awakening aura','Helper','Time=8 && NumHelper(9550)=0','helpertype=Normal\nname="Chakra del modo sabio"\nID=9550\nstateno=9550\npostype=P1\npos=0,-38\nownpal=1\nkeyctrl=0')+recover(520,60);states.append(s)

def ultimate():
 for form in [0,1]:
  off=form*10000;n=off+3000
  action(n,[(54,8),(61,8),(18,18),(17,18)] if not form else [(15,8),(5,8),(9,18),(8,18)],form,box='0,-64,75,-5')
  s=state(n,n,move='A',cost=3000,physics='N')+startup(n,18 if not form else 8)
  s+=c(n,'Confirmed dash starter','VelSet','Time>=8 && Time<28','x=6')+c(n,'Stop if missed','VelSet','Time>=28','x=0')+hit(n,8,0,starter=True)
  s+=c(n,'Only real hit starts cinematic','ChangeState','MoveHit && NumTarget(3000)>0',f'value={off+3001}')+recover(n,56);states.append(s)
  n=off+3001;action(n,[(17,8),(18,10),(19,10),(23,10),(54,10),(55,10),(57,80),(17,12)] if not form else [(3,12),(4,12),(9,10),(10,10),(12,10),(17,74),(8,12)],form)
  s=state(n,n,physics='N')+c(n,'Finite confirmed sequence','Pause','Time=0','time=142\nmovetime=142\npausebg=1')+c(n,'Protect confirmed cinematic','NotHitBy','Time<140','value=SCA\ntime=1')
  s+=c(n,'Darken stage briefly','BGPalFX','Time=0','time=142\nmul=75,90,100')+c(n,'Bound only the struck opponent','TargetBind','Time<140 && NumTarget(3000)>0','ID=3000\ntime=1\npos=95,0')
  cap=450 if form else 360;ratio='.45' if form else '.36'
  s+=c(n,'Bounded ultimate budget','VarSet','Time=0 && NumTarget(3000)>0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{cap},Floor((Target(3000),LifeMax)*{ratio}))')
  for i,t in enumerate([18,38,58,80,112]):
   s+=effect(n,f'Time={t}',8640 if i==4 else 8700,95,-35,1 if i==4 else .8,20)
   if form:s+=effect(n,f'Time={t}',8612,70,-40,1.15,16)
   else:s+=effect(n,f'Time={t}',8602,75,-36,1,16)+effect(n,f'Time={t}',8650,75,-36,.7,22)
   s+=c(n,'Damage belongs only to confirmed target','TargetLifeAdd',f'Time={t} && NumTarget(3000)>0',f'ID=3000\nvalue=-'+('(Var(20)-Floor(Var(20)/5)*4)' if i==4 else 'Floor(Var(20)/5)')+'\nabsolute=1\nkill=1')
   s+=snd(n,f'Time={t}',1,41 if i==4 else 7,1)+c(n,'Impact shake','EnvShake',f'Time={t}','time=7\nfreq=65\nampl=-4')
  s+=c(n,'Victim released safely','TargetState','Time=140 && NumTarget(3000)>0','ID=3000\nvalue=3011')+recover(n,152);states.append(s)
 for n in [3010,3011]:
  s=state(n,None,'S','H','N')+c(n,'Victim uses own hurt animation','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')
  if n==3010:s+=c(n,'Failsafe if owner interrupted','SelfState','Time>=210','value=0\nctrl=1')
  else:s+=c(n,'Return to own knockdown','SelfState','Time>=1','value=5050\nctrl=0')+c(n,'Release knockback','VelSet','Time=0','x=-5\ny=-7')
  states.append(s)

def common():
 # Reuse the project's tested native guard, fall and dash states; all animation
 # choices are now form-aware and remain independent of another character file.
 s=(ROOT/'JuraShinju/JuraShinju_common.cns').read_text().replace('; Jura common states, derived from project native MUGEN guard and recovery.','; Mitsuki native guard, fall and dash states, derived from the project common implementation.')
 s=re.sub(r'(?m)^anim\s*=\s*(\d+)\s*$',r'anim=\1+10000*Var(42)',s)
 blocks=re.split(r'(?=\n\[State )',s);out=[]
 for block in blocks:
  if re.search(r'(?im)^type\s*=\s*ChangeAnim\s*$',block):
   block=re.sub(r'(?m)^value\s*=\s*(.+)$',r'value=(\1)+10000*Var(42)',block)
   block=block.replace('Anim != IfElse(Vel X<0,21,20)','Anim != IfElse(Vel X<0,21,20)+10000*Var(42)').replace('Anim != 44','Anim != 44+10000*Var(42)')
  out.append(block)
 (CHAR/'MitsukiTBV_common.cns').write_text(''.join(out))

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
  s+=ctl(-1,name,'ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=Power>=IfElse(Var(42),{round(cost*.8)},{cost}){extra}\ntrigger1=ctrl',f'value={n}+10000*Var(42)')
 s+=ctl(-1,'Sage awakening','ChangeState','triggerall=AILevel=0\ntriggerall=command="s"\ntriggerall=command="holddown"\ntriggerall=Power>=3000\ntriggerall=Var(42)=0\ntriggerall=Var(41)=0\ntriggerall=StateType!=A\ntrigger1=ctrl','value=520')
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
 for n,cost,dist in [(3000,3000,140),(1030,450,260),(1200,200,300),(1020,500,100),(1010,400,200)]:s+=ctl(-1,'CPU legal attack','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=Power>={cost}\ntrigger1=P2BodyDist X<{dist}\ntrigger1=Random<AILevel*3',f'value={n}+10000*Var(42)')
 s+=ctl(-1,'CPU close chain','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X<65','value=200+10000*Var(42)')+ctl(-1,'CPU approach','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X>=65','value=20\nctrl=1')
 (CHAR/'MitsukiTBV.cmd').write_text(s)

def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite form timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 # Finish the current attack/recoil in its native form before reverting.
 s+=c(-2,'Safe Sage expiry','VarSet','!IsHelper && Var(42)>0 && Var(40)=0 && Ctrl && MoveType!=H && StateNo!=500','v=42\nvalue=0')
 s+=c(-2,'Refresh form after expiry','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')
 s+=c(-2,'Preserve Sage artwork during native turn transitions','ChangeAnim','!IsHelper && Var(42)=1 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')
 s+=c(-2,'Air chain reset','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge hum','StopSnd','!IsHelper && StateNo!=500','channel=3')
 s+=c(-2,'Sage aura persists only during form','Helper','!IsHelper && RoundState=2 && Var(42)=1 && NumHelper(9550)=0','helpertype=Normal\nname="Aura sabia"\nID=9550\nstateno=9550\npostype=P1\npos=0,-38\nownpal=1\nkeyctrl=0')
 s+=c(-2,'Round form cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round drawings cleanup','RemoveExplod','!IsHelper && RoundState!=2')
 return s

def main():
 animations();normals();techniques();lightning_helpers();helpers();utility();ultimate();common();commands()
 constants=(ROOT/'JuraShinju/JuraShinju.cns').read_text().split('[Statedef',1)[0];constants=constants[constants.index('[Data]'):].replace('life=1300','life=1200').replace('defence=115','defence=105').replace('height=84','height=80').replace('head.pos=0,-72','head.pos=0,-68')
 (CHAR/'MitsukiTBV.cns').write_text('; Mitsuki TBV, original Vaydra sprites, CobraG6 dialogue.\n'+constants+''.join(states)+system())
 (CHAR/'MitsukiTBV.air').write_text('; Original TBV body banks 0 and 1.\n'+''.join(air))
 d=(ROOT/'JuraShinju/JuraShinju.def').read_text().replace('JuraShinju','MitsukiTBV').replace('Jura Shinju','Mitsuki TBV').replace('versiondate=10,22,2026','versiondate=10,23,2026').replace('Codex (fan adaptation)','CobraG6 (voice reference), Codex (fan adaptation)');(CHAR/'MitsukiTBV.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,base_states=[m[3] for m in MOVES],sage_offset=10000,sage_ticks=1200,sage_cost=1500,activation_requires=3000,ultimate_cost=3000,ultimate_budget_base='min(360,36% opponent max life)',ultimate_budget_sage='min(450,45% opponent max life)',voices='CobraG6 supplied SND group 0, unchanged WAV payloads',video='User supplied Vaydra Senki gameplay, own MUGEN adaptation'),indent=2)+'\n')
 print(len(states),'combat states,',len(air),'actions; distinct base and Sage state banks')
if __name__=='__main__':main()
