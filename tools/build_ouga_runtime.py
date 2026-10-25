#!/usr/bin/env python3
"""Ouga / Yatsume: original cloaked and Raiton movesets with a hittable puppet."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'OugaYatsume';AIR=[];STATES=[];KEY={};SOUNDS={}
MOVES=[('Invocacion','a','F',1000,350),('Vortice','a','B',1010,400),('Lazo','b','F',1020,450),('Bomba','b','B',1030,600),('Ascendente','c','F',1040,350),('Prision','c','B',1050,500),('Barrido','a','D',1400,200),('Pesado','b','D',1410,300),('Estallido','c','D',1420,400),('Corte','y','N',1200,200),('Orbe','z','N',1210,250),('Derrumbe','y','D',1430,500),('Paso','z','D',1440,350)]
def ctl(n,label,typ,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype={typ}\n{triggers}\n{params}\n{extra}\n'
def c(n,label,typ,when,params='',extra=''):return ctl(n,label,typ,'trigger1='+when,params,extra)
def state(n,anim=None,typ='S',move='I',physics='S',cost=0,ctrl=0,vel='0,0'):return f'\n[Statedef {n}]\ntype={typ}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'+(f'anim={anim}\n' if anim is not None else '')+(f'poweradd=-{cost}\n' if cost else '')+(f'velset={vel}\n' if vel else '')
def action(n,seq,form=0,box=None,active=None,loop=False,hurt=True,add=False,loop_start=None,offsets=None,hurt_box=None):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+(hurt_box or ('-15,-76,15,0' if form else '-14,-76,14,0'))+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(seq):
  if i==loop_start:s+='Loopstart\n'
  if box and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+box+'\n'
  g,p=KEY[key];x,y=(offsets or {}).get(key,(0,0));s+=f'{g},{p},{x},{y},{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def seq(stem,start,end,t=3,pad=3):return [(f'{stem}_{i:0{pad}}',t) for i in range(start,end+1)]
def single(key,t=6):return [(key,t)]
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Supplied Ouga and Yatsume audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def common_sound(n,when,number=21):return c(n,'Technique effect','PlaySnd',when,f'value=S1,{number}\nchannel=4\nvolumescale=75')
def startup(n,voice=None):return common_sound(n,'Time=0')+(sound(n,'Time=0',voice) if voice else '')+c(n,'Brief activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def end(n,t=52,dest=0):return c(n,'Return control','ChangeState',f'Time>={t}',f'value={dest}\nctrl=1')
def cast(n,when,ident,x='0',y='0',number=None):return c(n,'Finite physical technique','Helper',when,f'helpertype=Normal\nname="Ouga technique"\nID={ident}\nstateno={number or ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def effect(n,when,anim,x=0,y=-40,scale=1,ticks=-2):return c(n,'Original supplied effect','Explod',when,f'anim={anim}\npostype=P1\npos={x},{y}\nscale={scale},{scale}\nremovetime={ticks}\nbindtime=1\nsprpriority=4\nownpal=1\nremoveongethit=1')
def hit(n,t,damage,fin=False,low=False,air=False,ident=0,stun=22,projectile=False):return c(n,'Real attack collision','HitDef',f'Time={t}',f'''attr={'A' if air else 'C' if low else 'S'},{'SP' if projectile else 'HP' if n%10000==3000 else 'SA' if n%10000>=1000 else 'NA'}
damage={damage},0
animtype={'Up' if fin else 'Medium'}
guardflag={'L' if low else 'MA'}
hitflag=MAF
priority=5,Hit
pausetime=4,8
sparkno=S8700
guard.sparkno=-1
sparkxy=0,-35
hitsound=S1,{19 if fin else 7}
guardsound=S1,9
ground.type={'Low' if low else 'High'}
ground.hittime={stun}
ground.slidetime=14
ground.velocity={-5 if fin else -.3},{-6 if fin else 0}
air.hittime=30
air.velocity={-4 if fin else -.5},{-5 if fin else -1}
fall={int(fin)}
fall.recover=1
fall.recovertime=45
getpower={25 if n%10000<1000 else 0},0
givepower=10,5
ID={ident}
hitonce=1
envshake.time={6 if fin else 2}
envshake.ampl={-4 if fin else -1}''')

def idle(form):return 'Kiba_Skill10_001' if form else 'Kiba_Idle_001'
def casting(form):return seq('Kiba_Skill01',1,4,5) if form else seq('Kiba_NAttack2',1,5,4)
def attack_action(n,p,form,box='-4,-73,85,3'):
 action(n,p+single(idle(form),-1),form,box=box,active=list(range(len(p))))

def basics():
 for form in [0,1]:
  off=form*10000;stand=single(idle(form),8)
  poses={0:seq('Kiba_Skill10' if form else 'Kiba_Idle',1,4 if form else 3,10),5:stand,6:stand,10:stand,11:stand,12:stand,20:seq('Kiba_Run' if form else 'Kiba_Walk',1,6,4,pad=2),21:list(reversed(seq('Kiba_Run' if form else 'Kiba_Walk',1,6,4,pad=2))),100:seq('Kiba_Run' if form else 'Kiba_Walk',1,6,2,pad=2),105:list(reversed(seq('Kiba_Run' if form else 'Kiba_Walk',1,6,2,pad=2))),40:single('Kiba_NAttack_007' if form else 'Kiba_NAttack2_006',5),41:single('Kiba_Float_001' if form else 'Kiba_NAttack2_007',8),44:single('Kiba_AirHurt_001' if form else 'Kiba_NAttack2_010',8),52:stand,170:single('Kiba_KnockDown_002' if form else idle(0),30),180:seq('Kiba_Skill10' if form else 'Kiba_Idle',1,4 if form else 3,12),190:stand,500:casting(form),520:seq('Kiba_Skill03',1,4,6) if form else seq('Kiba_NAttack2',1,5,4)+seq('Kiba_Skill01',1,4,5),5000:seq('Kiba_Hurt',1,2,6,pad=2) if form else stand,5010:stand,5020:single('Kiba_AirHurt_001',8) if form else stand,5030:single('Kiba_Float_001',8) if form else stand,5100:seq('Kiba_KnockDown',1,2,7) if form else stand,5110:single('Kiba_KnockDown_002' if form else idle(0),28),5120:seq('Kiba_KnockDown',3,4,7)+stand if form else stand+stand,5150:single('Kiba_KnockDown_002' if form else idle(0),60),5200:single('Kiba_AirHurt_001',8) if form else stand,5210:single('Kiba_Float_001',8) if form else stand,5300:stand}
  for n in [120,130,140,150,121,131,141,151,122,132,142,152]:poses[n]=stand
  for n,p in poses.items():action(n+off,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-46,-28,47,0' if n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{n}',3) for n in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,seq('Akamaru_Skill11',1,4,4),hurt=False,loop=True,box='-28,-28,28,28')
 action(8801,seq('OugaMon',1,6,5,pad=2),hurt=False,box='-100,-110,100,35')
 action(8802,seq('Akamaru_Skill01',6,17,3,pad=2),hurt=False)
 action(8803,seq('Akamaru_Skill11',1,4,4),hurt=False,box='-75,-60,75,25')
 for i in [1,2]:action(8810+i,seq(f'OugaDm{i}',1,3,10,pad=2),hurt=False,loop=True)

def normals():
 for form in [0,1]:
  off=form*10000
  sets=([seq('Kiba_NAttack',1,3,3),seq('Kiba_NAttack',4,6,3),seq('Kiba_NAttack',7,8,5)] if form else [seq('Kiba_NAttack2',1,3,3),seq('Kiba_NAttack2',4,5,5),seq('Kiba_NAttack2',6,9,3)])
  for family in [200,210,220]:
   for step in range(3):
    n=family+step+off;p=sets[step] if family==200 else sets[(step+1)%3] if family==210 else seq('Kiba_NAttack' if form else 'Kiba_NAttack2',7 if form else 10,8 if form else 13,3) if step==2 else sets[step]
    attack_action(n,p,form)
    STATES.append(state(n,n,move='A',vel='2,0')+sound(n,'Time=0','Yatsume/yatsuN' if form else 'Yatsume/Hit')+hit(n,3,[42,55,75][step] if form else [36,48,66][step],step==2,stun=13)+c(n,'Brake normal','VelSet','Time>=8','x=0')+end(n,24))
  for family in [600,610,620]:
   for step in range(3):
    n=family+step+off;p=seq('Kiba_NAttack' if form else 'Kiba_NAttack2',7 if form else 10,8 if form else 13,4);attack_action(n,p,form,'-4,-75,83,1')
    STATES.append(state(n,n,'A','A','N',vel=None)+c(n,'Three air attacks per jump','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief air strike','VelSet','Time<7','x=2\ny=-.4')+c(n,'Gravity resumes','VelAdd','Time>=7','y=.48')+hit(n,3,[38,49,68][step] if form else [34,44,60][step],step==2,air=True,stun=15)+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+end(n,20,50))

def order(n,which,t=8):
 return cast(n,'Time=0 && NumHelper(9700)=0',9700,'35','0')+c(n,'Order the existing puppet','VarSet',f'Time={t}',f'v=44\nvalue={which}')+c(n,'Unique puppet command','VarAdd',f'Time={t}','v=45\nvalue=1')

def specials():
 for form in [0,1]:
  off=form*10000
  for name,b,d,base,cost in MOVES:
   n=base+off;p=casting(form);box='-5,-76,95,3'
   if not form:
    if base==1050:p=seq('Kiba_Skill05',1,14,4);box='20,-110,245,10'
    elif base==1430:p=single('Kiba_Skill06_001',8)+seq('Kiba_Skill06',2,25,3);box='-40,-130,250,10'
    elif base in [1400,1440]:p=seq('Kiba_NAttack2',10,13,4)
    elif base==1410:p=seq('Kiba_NAttack2',1,5,4)
   else:
    if base==1000:p=seq('Kiba_SkillDash',1,3,3)+seq('Kiba_Skill02',1,15,3);box='-3,-80,120,4'
    elif base==1020:p=seq('Kiba_Skill04',1,19,3);box='5,-95,230,5'
    elif base==1040:p=seq('Kiba_NAttack',6,8,7)
    elif base==1050:p=casting(1)+seq('Kiba_Skill04Ex',1,8,6);box='-115,-145,115,5'
    elif base==1200:p=seq('Kiba_Skill11',1,13,3);box='-5,-90,115,3'
    elif base==1400:p=seq('Kiba_NAttack',7,8,8);box='-5,-45,85,3'
    elif base==1410:p=seq('Kiba_NAttack',1,6,4)
    elif base==1440:p=seq('Kiba_SkillDash',1,3,3)+seq('Kiba_Skill04',1,6,4,pad=2);box='-5,-85,105,5'
   attack_action(n,p,form,box);s=state(n,n,move='A',physics='N',cost=cost)+startup(n,'Yatsume/S2' if form else 'Yatsume/S1')
   if base==1000:
    if form:s+=c(n,'Raiton approach','VelSet','Time>=8 && Time<28 && !MoveContact','x=8')+c(n,'Brake contact','VelSet','MoveContact || Time>=28','x=0')+hit(n,10,70,stun=27)+hit(n,24,110,True,stun=28)+sound(n,'Time=8','Effect/Blade-Damage',2)
    else:s+=order(n,9701)
   elif base==1010:s+=order(n,9702)
   elif base==1020:
    if form:s+=hit(n,12,80,stun=29)+hit(n,30,130,True)+sound(n,'Time=12','Effect/rantai',2)
    else:s+=order(n,9703)
   elif base==1030:s+=order(n,9704)+sound(n,'Time=8','Ouga/ouga2')
   elif base==1040:
    if form:s+=c(n,'Rise','VelSet','Time=6','x=3\ny=-6.5')+c(n,'Air state','StateTypeSet','Time=6','statetype=A\nphysics=N')+c(n,'Gravity','VelAdd','Time>6','y=.44')+hit(n,6,75,air=True)+hit(n,15,105,True,air=True)+c(n,'Land the ascent','ChangeState','Time>18 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
    else:s+=cast(n,'Time=12',9501,'IfElse(P2Dist X<190,P2Dist X,190)','-130')+sound(n,'Time=12','Effect/MonStep',2)
   elif base==1050:
    if form:
     for i,t in enumerate([22,34,46]):s+=hit(n,t,70,i==2,stun=26)
     s+=sound(n,'Time=22','Yatsume/IkazuchiInagi')+sound(n,'Time=22','Effect/raitonsfx1',2)
    else:s+=hit(n,8,75,stun=30)+hit(n,24,115,True)+sound(n,'Time=8','Effect/m_exp',2)
   elif base==1400:s+=c(n,'Low step','VelSet','Time<13','x=3.5')+c(n,'Brake sweep','VelSet','Time>=13','x=0')+hit(n,4,120 if form else 100,True,low=True)
   elif base==1410:s+=hit(n,4,70 if form else 50,stun=24)+hit(n,15,105 if form else 90,True)
   elif base==1420:s+=cast(n,'Time=9',9502,'0','-25')+sound(n,'Time=9','Effect/Jutsu',2)
   elif base==1200:
    if form:s+=hit(n,7,75,stun=24)+hit(n,21,100,True)+sound(n,'Time=7','Effect/RtnSfx',2)
    else:s+=order(n,9705)
   elif base==1210:s+=cast(n,'Time=8',9500,'30','-28')+sound(n,'Time=8','Effect/Sign',2)
   elif base==1430:
    if form:s+=cast(n,'Time=14',9501,'IfElse(P2Dist X<210,P2Dist X,210)','-130')+cast(n,'Time=28',9501,'IfElse(P2Dist X<210,P2Dist X,210)','-130')
    else:s+=hit(n,12,65,stun=28)+hit(n,30,85,stun=28)+hit(n,49,110,True)
    s+=sound(n,'Time=12','Effect/break_sound3',2)
   elif base==1440:s+=c(n,'Finite dimensional step','PosSet','Time=8 && Abs(P2Dist X)<240','x=(EnemyNear,Pos X)-40*Facing')+effect(n,'Time=8',8710,0,-30,.7,12)+hit(n,12,165 if form else 140,True)+sound(n,'Time=8','Effect/dash',2)
   s+=end(n,max(48,sum(t for _,t in p)),50 if form and base==1040 else 0);STATES.append(s)

def puppet_system():
 s=''
 when='1'
 s+=c(-2,'Finite autonomous puppet age','VarAdd',when,'v=5\nvalue=1','ignorehitpause=1')+c(-2,'Puppet collision does not push','PlayerPush',when,'value=0')
 s+=c(-2,'Puppet can receive ordinary attacks','HitOverride',when,'slot=0\nattr=SCA,NA,SA,HA,NP,SP,HP,NT,ST,HT\nstateno=9790\ntime=1\nforceair=0','ignorehitpause=1')
 s+=c(-2,'Puppet cleans up on defeat or expiry','DestroySelf',when+' && Var(2)=1 && (Life<=0 || Var(5)>=900 || (Root,Life)<=0 || RoundState!=2 || (Parent,Var(48))!=Var(7))')
 s+=c(-2,'Face the real target','Turn',when+' && NumEnemy>0 && P2Dist X<0','')
 s+=c(-2,'One existing puppet consumes new orders','ChangeState',when+' && Var(2)=1 && StateNo!=9790 && (Parent,Var(45))!=Var(1)','value=Parent,Var(44)\nctrl=0')
 s+=c(-2,'Hold support during the ultimate','VelSet',when+' && (Root,StateNo%10000)=3000','x=0\ny=0')
 return s

def puppet():
 poses={9700:seq('Akamaru_Idle',1,4,7),9701:seq('Akamaru_Move',1,4,4)*2,9702:seq('Akamaru_Skill01',1,12,3)+seq('Akamaru_Skill01_Down',1,5,3)+seq('Akamaru_Skill01',1,5,3,pad=2),9703:seq('Akamaru_Skill11',1,4,5,pad=2),9704:seq('Akamaru_Skill10',1,3,5,pad=2)+seq('Akamaru_Skill01',1,5,2,pad=2)+seq('Akamaru_Skill01',6,17,3,pad=2),9705:seq('Akamaru_Move',1,4,3)*2,9790:single('Akamaru_Idle_001',10)}
 for n,p in poses.items():
  action(n,p,box='-50,-70,75,4' if n!=9702 else '-80,-100,80,15',hurt_box='-16,-65,16,0',loop=n==9700)
  s=state(n,n,'S','H' if n==9790 else 'I' if n==9700 else 'A','N')
  if n==9700:
   s+=c(n,'Puppet health','LifeSet','Time=0 && Var(2)=0','value=300')+c(n,'Puppet generation','VarSet','Time=0 && Var(2)=0','v=7\nvalue=Parent,Var(48)')+c(n,'Initialize current order','VarSet','Time=0 && Var(2)=0','v=1\nvalue=Parent,Var(45)')+sound(n,'Time=0 && Var(2)=0','Ouga/ouga1')+c(n,'Puppet initialized once','VarSet','Time=0','v=2\nvalue=1')
  s+=c(n,'Commanded or autonomous strike','VarSet','Time=0','v=4\nvalue=IfElse((Parent,Var(45))!=Var(1),1,0)')+c(n,'Consume this order','VarSet','Time=0 && StateNo=(Parent,Var(44))','v=1\nvalue=Parent,Var(45)')+c(n,'Snapshot mode','VarSet','Time=0','v=3\nvalue=Parent,Var(42)')
  s+=puppet_system()
  if n==9700:
   s+=c(n,'Follow target','VelSet','(Root,StateNo%10000)!=3000','x=IfElse(Abs(P2Dist X)>65,3,0)')+c(n,'Walk pose','ChangeAnim','Abs(P2Dist X)>65 && Anim!=9706','value=9706')+c(n,'Idle pose','ChangeAnim','Abs(P2Dist X)<=65 && Anim!=9700','value=9700')+c(n,'Autonomous physical attack','ChangeState','Time>=40 && Abs(P2Dist X)<85 && (Root,StateNo%10000)!=3000','value=9701')
  elif n==9790:s+=end(n,10,9700)
  else:
   if n in [9702,9703,9704]:s+=c(n,'Actual finite portal placement','PosSet','Time=0','x=(Root,Pos X)+(Root,Facing)*IfElse((Root,P2Dist X)<210,(Root,P2Dist X)-20,190)\ny=0')
   if n==9701:s+=hit(n,4,'IfElse(Var(4),IfElse(Var(3),115,85),IfElse(Var(3),60,45))',True,stun=22)+sound(n,'Time=4','Effect/blade_dmg',2)
   elif n==9702:
    for i,t in enumerate([6,22,40]):s+=hit(n,t,'IfElse(Var(3),85,70)',i==2,stun=23)
    s+=sound(n,'Time=0','Ouga/OugaLaug')+sound(n,'Time=4','Effect/Sign',2)
   elif n==9703:s+=effect(n,'Time=0',8800,0,-25,1,26)+hit(n,8,70,stun=25)+hit(n,18,'IfElse(Var(3),120,100)',True)
   elif n==9704:s+=hit(n,25,'IfElse(Var(3),300,250)',True)+sound(n,'Time=25','Effect/Explosion2',2)
   elif n==9705:s+=c(n,'Puppet rush','VelSet','Time<23 && !MoveContact','x=8')+c(n,'Stop after impact','VelSet','MoveContact || Time>=23','x=0')+hit(n,4,'IfElse(Var(3),150,110)',True)
   s+=c(n,'Bomb consumes the puppet','DestroySelf','Time>=64') if n==9704 else end(n,max(34,sum(t for _,t in p)),9700)
  STATES.append(s)
 action(9706,seq('Akamaru_Walk',1,6,4),loop=True,hurt_box='-16,-65,16,0')

def effects():
 for n in [9500,9501,9502]:
  a=8801 if n==9501 else 8803 if n==9502 else 8800
  s=state(n,a,'A','A','N',vel='9,0' if n==9500 else '0,6' if n==9501 else '0,0')+c(n,'No effect push','PlayerPush','1','value=0')+c(n,'No effect shadow','AssertSpecial','1','flag=NoShadow')
  s+=c(n,'Effect size','AngleDraw','1','scale='+('.45,.45' if n==9500 else '.6,.6' if n==9501 else '1.4,1.4'))
  s+=c(n,'Snapshot effect damage','VarSet','Time=0','v=0\nvalue='+('IfElse((Root,Var(42)),140,100)' if n==9500 else '150' if n==9501 else 'IfElse((Root,Var(42)),180,135)'))
  s+=hit(n,8 if n==9501 else 6 if n==9502 else 0,'Var(0)',True,air=True,projectile=True,stun=28)+c(n,'Resolve physical contact','DestroySelf','MoveContact')+c(n,'Finite effect lifetime','DestroySelf',f'Time>={50 if n==9500 else 45 if n==9501 else 22} || RoundState!=2');STATES.append(s)

def utility():
 for n in [170,180,190]:
  s=state(n,n)+c(n,'Original round pose','Null','1')+sound(n,'Time=0','Yatsume/YatsuDead' if n==170 else 'Yatsume/Y00' if n==180 else 'Yatsume/yatsuIntr')
  if n==190:s+=c(n,'Brief intro','AssertSpecial','Time<40','flag=Intro')+end(n,44)
  STATES.append(s)
 s=state(500,500)+c(500,'Charge energy','PowerAdd','1','value=20')+cast(500,'Time=0 && NumHelper(9550)=0',9550)+sound(500,'Time=0','Effect/RaitonEfx',3)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1');STATES.append(s)
 STATES.append(state(9550,8900,'A','I','N')+c(9550,'Charge aura follows body','BindToRoot','1','time=1\npos=0,-38')+c(9550,'Vertical aura','AngleDraw','1','value=90\nscale=.27,.3')+c(9550,'Blue and purple energy','PalFX','1','time=1\ncolor=0\nmul=125,125,256')+c(9550,'Behind the body','SprPriority','1','value=-2')+ctl(9550,'Aura expires','DestroySelf','trigger1=Root,StateNo!=500\ntrigger2=RoundState!=2'))
 s=state(520,520)+startup(520,'Yatsume/S3')+effect(520,'Time=8',8710,0,-30,1.2,24)+sound(520,'Time=8','Effect/Jutsu',2)+c(520,'Pay transformation','PowerAdd','Time=20','value=-1500')+c(520,'Remove the cloak','VarSet','Time=20','v=42\nvalue=1')+c(520,'Twenty seconds of Raiton','VarSet','Time=20','v=40\nvalue=1200')+c(520,'Transformation cooldown','VarSet','Time=20','v=41\nvalue=1500')+end(520,44);STATES.append(s)

def ultimate():
 base=casting(0)+seq('Kiba_Skill05',1,14,4)+single('Kiba_Skill06_001',8)+seq('Kiba_Skill06',2,25,4)
 awake=casting(1)+seq('Kiba_Skill04',1,19,3)+seq('Kiba_Skill04Ex',1,4,6)*3+seq('Kiba_Skill04Ex',5,8,5)+seq('Kiba_Skill11',1,13,3)
 for form,p in [(0,base),(1,awake)]:
  n=3000+form*10000;attack_action(n,p,form,'-10,-110,245,5');s=state(n,n,move='A',physics='N',cost=3000)+startup(n,'Yatsume/IkazuchiInagi' if form else 'Yatsume/S5')
  s+=c(n,'Pause autonomous support for the cinematic','VarSet','Time=0','v=44\nvalue=9700')+c(n,'One cinematic support order','VarAdd','Time=0','v=45\nvalue=1')+c(n,'Reset confirmed hit','VarSet','Time=0','v=21\nvalue=0')
  s+=c(n,'Original dimensional scenery','Explod','Time=0',f'anim={8811 if form else 8812}\npostype=left\npos=160,120\nscale=.65,.8\nfacing=1\nbindtime=-1\nremovetime=210\nsprpriority=-9\nownpal=1\nremoveongethit=1')
  s+=hit(n,18,0,False,ident=3000,stun=230)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Record the actual struck target','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite confirmed damage','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{750 if form else 600},Floor((Target(3000),LifeMax)*{.75 if form else .60}))')+c(n,'Confirm collision','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')
  s+=c(n,'Bind only the confirmed opponent','TargetBind','NumTarget(3000)>0 && Time<196','ID=3000\ntime=1\npos=(FVar(0)-Pos X)*Facing,0')
  times=[42,62,82,102,122,142,162,182]
  for i,t in enumerate(times):
   amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)';when=f'Time={t} && NumTarget(3000)>0'
   s+=c(n,'Confirmed dimensional pulse','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count impact','HitAdd',when,'value=1')+effect(n,when,8700,'(FVar(0)-Pos X)*Facing',-35,.7,9)+sound(n,when,'Effect/raitonsfx1' if form else 'Effect/break_sound3',2)
  s+=c(n,'Release the opponent','TargetState','Time=196 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,max(218,sum(t for _,t in p)));STATES.append(s)
 STATES.append(state(3010,None,'S','H','N')+c(3010,'Victim retains its own artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Guaranteed release','SelfState','trigger1=Time>=255\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3011,None,'A','H','N')+c(3011,'Real throw velocity','VelSet','Time=0','x=-5\ny=-6')+c(3011,'Restore victim state ownership','SelfState','1','value=5050\nctrl=0'))

def commands():
 import build_sarada_runtime as ref
 saved=ref.CHAR,ref.MOVES
 try:ref.CHAR=CHAR;ref.MOVES=MOVES;ref.commands()
 finally:ref.CHAR,ref.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';s=p.read_text().replace('Pink Susanoo awakening','Yatsume Raiton awakening');(CHAR/'OugaYatsume.cmd').write_text(s);p.unlink()

def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite Raiton timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Return to the cloak safely','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Restore cloaked bank','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')+c(-2,'Raiton uses its own outfit','ChangeAnim','!IsHelper && Var(42)=1 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+c(-2,'Raiton physical strength','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.15,1)')
 s+=c(-2,'Reset air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge audio','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round mode cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')+sound(-2,'!IsHelper && StateNo=5000 && Time=0','Yatsume/Hurt',0,70)
 prone='!IsHelper && Var(42)=0 && (Anim=170 || Anim=5100 || Anim=5110 || Anim=5150)'
 s+=c(-2,'Keep the cloak on during knockdown','AngleDraw',prone,'value=90','ignorehitpause=1')+c(-2,'Cloaked body ground alignment','Offset',prone,'x=35\ny=-15','ignorehitpause=1')

 return s

def main():
 global KEY,SOUNDS
 KEY=json.loads((CHAR/'assets/keys.json').read_text());SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];basics();normals();specials();puppet();effects();utility();ultimate();commands()
 const=(ROOT/'JuraShinju/JuraShinju.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):].replace('life=1300','life=1100').replace('defence=115','defence=100').replace('height=84','height=76')
 (CHAR/'OugaYatsume.cns').write_text('; Original Yatsume outfits, original Ouga puppet, physical collision.\n'+const+''.join(STATES)+system());(CHAR/'OugaYatsume.air').write_text('; Original atlas artwork, each outfit uses its own bank.\n'+''.join(AIR))
 s=(ROOT/'JuraShinju/JuraShinju_common.cns').read_text();s=re.sub(r'(?m)^anim\s*=\s*(\d+)\s*$',r'anim=\1+10000*Var(42)',s);blocks=re.split(r'(?=\n\[State )',s)
 for i,b in enumerate(blocks):
  if re.search(r'(?im)^type\s*=\s*ChangeAnim\s*$',b):b=re.sub(r'(?m)^value\s*=\s*(.+)$',r'value=(\1)+10000*Var(42)',b).replace('Anim != IfElse(Vel X<0,21,20)','Anim != IfElse(Vel X<0,21,20)+10000*Var(42)').replace('Anim != 44','Anim != 44+10000*Var(42)')
  blocks[i]=b
 (CHAR/'OugaYatsume_common.cns').write_text(''.join(blocks))
 d=(ROOT/'JuraShinju/JuraShinju.def').read_text().replace('JuraShinju','OugaYatsume').replace('Jura Shinju','Ouga Yatsume');d=re.sub(r'(?m)^author=.*$','author="VayDra original sprites and audio / Codex adaptation"',d);d=re.sub(r'(?m)^versiondate=.*$','versiondate=10,25,2026',d);(CHAR/'OugaYatsume.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,form_offset=10000,base='Yatsume with black cloak',awakening='Yatsume without cloak and Raiton',activation_requires=3000,awakening_cost=1500,awakening_ticks=1200,puppet_id=9700,puppet_maximum=1,puppet_health=300,puppet_ticks=900,ultimate_cost=3000,own_life_cost=0,ultimate_damage='min(600,60% maximum enemy life) base; min(750,75%) Raiton',source_art_unchanged=True,ai_generated_art=False),indent=2)+'\n');print('Ouga runtime:',len(STATES),'states;',len(AIR),'animations')
if __name__=='__main__':main()

