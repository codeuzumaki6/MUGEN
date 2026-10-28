#!/usr/bin/env python3
"""Boruto: original sword, Rasengan, Karma/Jogan sequences and a finite clone."""
from pathlib import Path
import json,re
from build_sumire_runtime import ctl,c,state,hit,end,common_sound,single
ROOT=Path(__file__).resolve().parents[1];NAME='BorutoKarmaJogan';CHAR=ROOT/NAME;AIR=[];STATES=[];KEY={};SOUNDS={}
MOVES=[('Rasengan','a','F',1000,350),('Shiden','a','B',1010,400),('Kenjutsu','b','F',1020,450),('Espiral','b','B',1030,550),('Ascendente','c','F',1040,350),('Combo','c','B',1050,450),('Barrido','a','D',1400,200),('Bunshin','b','D',1410,300),('Caida','c','D',1420,450),('Kunai','y','N',1200,200),('Disparo','z','N',1210,250),('Invocacion','y','D',1430,600),('Futon','z','D',1440,600)]
PULSES=[44,72,100,128,156,184,212,244]
def seq(stem,a,b,t=3):return [(f'Pain_{stem}_{i:02}',t) for i in range(a,b+1)]
def rawseq(stem,a,b,t=3):return [(f'{stem}_{i:02}',t) for i in range(a,b+1)]
def idle(form=0):return 'Pain_Idle_01'
def action(n,poses,form=0,box=None,active=None,hurt=True,loop=False,add=False,hurt_box=None):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+ (hurt_box or '-16,-85,18,0')+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(poses):
  if box and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+box+'\n'
  g,p=KEY[key];s+=f'{g},{p},0,0,{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def attack(n,p,form,box='-5,-85,125,5'):action(n,p+single(idle(form),-1),form,box=box,active=list(range(len(p))))
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Supplied Boruto audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def startup(n,voice='BorutoJogan/01'):
 return common_sound(n,'Time=0')+sound(n,'Time=0',voice,volume=110 if voice.endswith('/03') else 90)+c(n,'Brief technique focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def effect(n,when,anim,x=0,y=-35,scale=1,ticks=-2,priority=4):return c(n,'Separate original effect','Explod',when,f'anim={anim}\npostype=P1\npos={x},{y}\nscale={scale},{scale}\nremovetime={ticks}\nbindtime=1\nsprpriority={priority}\nownpal=1\nremoveongethit=1')
def cast(n,when,ident,x=35,y=-38):return c(n,'Finite technique resource','Helper',when,f'helpertype=Normal\nname="Boruto technique"\nID={ident}\nstateno={ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def basic():
 base={0:seq('Idle',1,3,10),5:seq('Idle',1,1,8),6:seq('KnockDown',4,4,8),10:seq('KnockDown',4,4,6),11:seq('KnockDown',4,4,8),12:seq('Idle',1,1,6),20:seq('Walk',1,6,4),21:list(reversed(seq('Walk',1,6,4))),100:seq('Walk',1,6,2),105:list(reversed(seq('Walk',1,6,2))),40:rawseq('Unframe',1,1,6),41:seq('AirHurt',1,2,6),44:rawseq('Unframe',2,2,8),52:seq('KnockDown',4,5,5)+seq('Idle',1,1,4),170:seq('KnockDown',3,3,30),180:seq('Idle',1,3,12),190:seq('Idle',1,3,12),500:seq('Skill05',23,25,8),520:seq('Skill05',23,25,4)+seq('Skill01',49,52,5)*2+seq('Idle',1,1,10),5000:seq('Hurt',1,2,6),5010:seq('Hurt',1,2,6),5020:seq('AirHurt',1,2,6),5030:seq('KnockDown',1,2,8),5100:seq('KnockDown',1,3,8),5110:seq('KnockDown',3,3,28),5120:seq('KnockDown',4,5,8)+seq('Idle',1,1,5),5150:seq('KnockDown',3,3,60),5200:seq('AirHurt',1,1,8),5210:seq('AirHurt',2,2,8),5300:seq('Hurt',1,1,20)}
 for n in [120,130,140,150,121,131,141,151,122,132,142,152]:base[n]=rawseq('Unframe',3,3,6)
 for form in [0,1]:
  for n,p in base.items():action(n+10000*form,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-40,-25,42,0' if n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,seq('Skill02',1,8,3),hurt=False,loop=True,box='-16,-12,20,12')
 action(8801,seq('Skill04',1,8,3),hurt=False,loop=True,box='-26,-25,30,25')
 action(8802,seq('Skill02',25,32,3),hurt=False,box='-30,-30,40,30')
 action(8803,seq('Skill04',37,44,3),hurt=False,box='-30,-45,40,45')
 action(8810,rawseq('JouganSCR',1,5,4),hurt=False)
 action(8811,rawseq('JouganEye',1,3,5),hurt=False)
 action(8812,[(f'BOLT_{i:02}',4) for i in [1,2,3,7,8,9]],hurt=False,loop=True)
 action(8813,seq('Skill05',125,140,3),hurt=False)
 action(8814,rawseq('Duar_Move',1,17,3),hurt=False)
 action(9700,seq('Walk',1,6,3),loop=True)
 action(9701,seq('Skill03',1,11,3),box='-5,-85,130,5')
 action(9790,seq('Hurt',1,2,5))
def normals():
 sets=[seq('NAttack',1,5,2),seq('NAttack',6,10,2),seq('NAttack',11,18,2)]
 for form in [0,1]:
  for family in [200,210,220,600,610,620]:
   air=family>=600
   for step in range(3):
    n=family+step+10000*form;p=sets[(step+(family%100)//10)%3];attack(n,p,form)
    s=state(n,n,'A' if air else 'S','A','N' if air else 'S',vel=None if air else '2,0')+sound(n,'Time=0','BorutoJogan/Hit',volume=70)+hit(n,3,([45,60,80] if form else [36,48,66])[step],step==2,air=air,stun=15)
    if air:s+=c(n,'Count air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Air approach','VelSet','Time<7','x=2\ny=-.4')+c(n,'Gravity','VelAdd','Time>=7','y=.48')+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
    else:s+=c(n,'Brake','VelSet','Time>=8','x=0')
    STATES.append(s+end(n,21 if air else 25,50 if air else 0))
def specials():
 throw=[(f'Pain_Skill01_{i:02}ex',5) for i in range(32,36)]
 base={1000:seq('Skill03',1,11,3),1010:seq('Skill01',49,52,4)+seq('Skill01',53,59,3),1020:seq('Skill02',34,43,4),1030:seq('Skill03',44,54,4),1040:seq('Skill02',17,24,4),1050:seq('Skill04',29,36,4),1400:seq('NAttack',7,10,4),1410:rawseq('Unframe',1,3,8),1420:seq('Skill02',49,54,5),1200:throw,1210:seq('Skill03',33,34,7)+seq('Skill03',55,55,9),1430:seq('Skill04',45,81,2),1440:seq('Skill03',35,45,4)}
 awake={1000:seq('Skill02',44,54,3),1010:seq('Skill05',111,124,3),1020:base[1020],1030:seq('Skill05',73,102,2),1040:seq('Skill04',82,94,3),1050:seq('Skill03',6,11,3)+seq('Skill04',30,35,3),1400:seq('NAttack',13,16,4),1410:base[1410],1420:seq('Skill05',141,163,3),1200:throw*2,1210:base[1210]*2,1430:seq('Skill05',73,110,2),1440:seq('Skill05',145,177,2)}
 for form in [0,1]:
  for name,b,d,ident,cost in MOVES:
   n=ident+10000*form;p=(awake if form else base)[ident];box='-5,-85,145,5'
   if ident==1010:box='-80,-100,250,5'
   if ident in [1030,1420] and form:box='-100,-135,185,5'
   if ident==1400:box='-5,-40,110,5'
   if ident==1430:box='-65,-145,260,5' if not form else '-130,-150,210,5'
   if ident==1440:box='15,-110,245,5'
   attack(n,p,form,box);voice='BorutoJogan/'+('04' if ident==1430 else '05' if ident==1440 else '03' if ident in [1000,1030,1210,1420] else '02' if ident in [1020,1040] else '01')
   s=state(n,n,move='A',physics='N',cost=cost)+startup(n,voice)
   if ident in [1000,1020,1050]:
    s+=c(n,'Physical technique approach','VelSet','Time>=6 && Time<28 && !MoveContact','x='+('10' if form and ident==1020 else '7'))+c(n,'Brake on contact','VelSet','MoveContact || Time>=28','x=0')
   if ident in [1040,1420] and not (form and ident==1420):
    s+=c(n,'Real rising motion','VelSet','Time=4','x=4\ny=-6.5')+c(n,'Airborne','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Finite gravity','VelAdd','Time>4','y=.46')+c(n,'Original landing','ChangeState','Time>20 && Pos Y>=0 && Vel Y>0','value='+str(1060+10000*form)+'\nctrl=0')
   if ident in [1200,1210]:
    for t in ([9,19,29] if form and ident==1200 else [9,24] if form else [9]):s+=cast(n,f'Time={t}',9500 if ident==1200 else 9501)+sound(n,f'Time={t}','Effect/BladeA' if ident==1200 else 'Effect/rasenS',2)
   elif ident==1410:s+=cast(n,'Time=10 && NumHelper(9700)=0',9700,-28,0)+c(n,'Order the existing clone','VarAdd','Time=12','v=45\nvalue=1')
   else:
    times={1000:[15,28],1010:[16,28,40] if form else [16,28],1020:[6,23],1030:[8,26,44] if form else [15,30],1040:[6,23],1050:[5,18,30],1400:[5],1420:[14,32,50] if form else [7,21],1430:[18,36,54],1440:[10,25,42] if form else [10,25]}[ident]
    values={1000:[75,110],1010:[65,80,125] if form else [55,140],1020:[80,115],1030:[70,85,125] if form else [80,115],1040:[70,110],1050:[55,70,100],1400:[110],1420:[75,90,115] if form else [70,115],1430:[75,85,110],1440:[80,95,135] if form else [85,120]}[ident]
    for i,(t,v) in enumerate(zip(times,values)):s+=hit(n,t,v+(15 if form and ident in [1000,1020,1040,1050,1400] else 0),i==len(times)-1,low=ident==1400,air=ident in [1040,1420] and not (form and ident==1420),stun=30)
    if ident==1020 and form:s+=cast(n,'Time=8',9502)
    if ident==1040:s+=cast(n,'Time=13',9502)
    if ident==1440:s+=cast(n,'Time=9',9503)+sound(n,'Time=9','Effect/RSGfuton',2)
    if ident==1430:s+=sound(n,'Time=14','Effect/windeffect' if form else 'Effect/mon2',2)+(effect(n,'Time=20',8813,0,0,.65,48,-2) if form else '')
   s+=end(n,max(50,sum(t for _,t in p)),50 if ident in [1040,1420] and not (form and ident==1420) else 0);STATES.append(s)
  n=1060+10000*form;action(n,seq('KnockDown',4,5,5),form);STATES.append(state(n,n)+c(n,'Ground landing','PosSet','Time=0','y=0')+end(n,10))
def helpers():
 for n,anim,damage,speed,size in [(9500,8800,85,11,'.9,.9'),(9501,8801,125,9,'.45,.45'),(9502,8802,75,9,'.65,.65'),(9503,8803,100,10,'.6,.6')]:
  s=state(n,anim,'A','A','N',vel=f'{speed},0')+c(n,'Standalone projectile size','AngleDraw','1','scale='+size)+c(n,'No push','PlayerPush','1','value=0')+hit(n,0,damage,n not in [9500,9501],air=True,projectile=True)+c(n,'Finite projectile','DestroySelf','MoveContact || Time>=50 || RoundState!=2');STATES.append(s)
 for n in [9700,9701,9790]:
  s=state(n,n,'S','H' if n==9790 else 'I' if n==9700 else 'A','N')
  if n==9700:s+=c(n,'Finite clone health','LifeSet','Time=0 && Var(2)=0','value=120')+c(n,'Remember clone form','VarSet','Time=0 && Var(2)=0','v=0\nvalue=Root,Var(42)')+c(n,'Remember order','VarSet','Time=0 && Var(2)=0','v=1\nvalue=Parent,Var(45)')+c(n,'Initialize once','VarSet','Time=0','v=2\nvalue=1')
  else:s+=c(n,'Consume command','VarSet','Time=0','v=1\nvalue=Parent,Var(45)')
  s+=c(n,'Finite clone age','VarAdd','1','v=5\nvalue=1','ignorehitpause=1')+c(n,'No clone push','PlayerPush','1','value=0')+c(n,'Clone can receive real damage','HitOverride','1','attr=SCA,NA,SA,HA,NP,SP,HP,NT,ST,HT\nstateno=9790\ntime=1\nforceair=0','ignorehitpause=1')+c(n,'Clone defeat and cleanup','DestroySelf','Var(2)=1 && (Life<=0 || Var(5)>=180 || (Root,Life)<=0 || (Root,StateNo%10000)=3000 || RoundState!=2)')+c(n,'Face actual enemy','Turn','P2Dist X<0','')
  if n!=9790:s+=c(n,'Take clone order','ChangeState','(Parent,Var(45))!=Var(1)','value=9701\nctrl=0')
  if n==9700:s+=c(n,'Close on opponent','VelSet','1','x=IfElse(Abs(P2Dist X)>90,4,0)')+c(n,'Autonomous clone Rasengan','ChangeState','Time>=18 && Abs(P2Dist X)<130','value=9701\nctrl=0')
  elif n==9790:s+=c(n,'Clone hurt flash','PalFX','1','time=1\nadd=60,80,100')+end(n,10,9700)
  else:s+=c(n,'Clone actual approach','VelSet','Time<18 && !MoveContact','x=7')+c(n,'Clone brake','VelSet','MoveContact || Time>=18','x=0')+hit(n,15,'IfElse(Var(0),65,45)',stun=28)+hit(n,27,'IfElse(Var(0),85,70)',True)+sound(n,'Time=10','Effect/rasenS',2)+end(n,38,9700)
  STATES.append(s)
def utility():
 for n in [170,180,190]:
  s=state(n,n)+sound(n,'Time=0','BorutoJogan/Dead' if n==170 else 'BorutoJogan/Tenten')
  if n==190:s+=c(n,'Brief intro','AssertSpecial','Time<36','flag=Intro')+end(n,40)
  STATES.append(s)
 STATES.append(state(500,500)+c(500,'Real chakra charge','PowerAdd','1','value=20')+sound(500,'Time=0','Effect/aura',3)+cast(500,'Time=0 && Var(42)=0 && NumHelper(9551)=0',9551,0,0)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 for n in [9551,9560]:
  s=state(n,8900,'A','I','N')+c(n,'Follow main body','BindToRoot','1','time=1\npos=0,-45')
  if n==9551:s+=c(n,'Green charge aura','PalFX','1','time=1\ncolor=0\nmul=70,230,120')+c(n,'Charge aura drawing','AngleDraw','1','value=90\nscale=.38,.4')
  else:s+=c(n,'Blue Jogan electricity','ChangeAnim','(Root,StateNo)!=500 && Anim!=8812','value=8812')+c(n,'Charging resonance aura','ChangeAnim','(Root,StateNo)=500 && Anim!=8900','value=8900')+c(n,'Original blue arcs drawing','AngleDraw','1','value=IfElse((Root,StateNo)=500,90,0)\nscale=IfElse((Root,StateNo)=500,.45,.28),IfElse((Root,StateNo)=500,.5,.28)')
  s+=c(n,'Behind main body','SprPriority','1','value=-2')+c(n,'Aura cleanup','DestroySelf','RoundState!=2 || (Root,Life)<=0 || '+('(Root,StateNo)!=500' if n==9551 else '(Root,Var(42))=0'));STATES.append(s)
 STATES.append(state(520,520)+startup(520,'BorutoJogan/05')+effect(520,'Time=12',8810,0,-135,.28,20)+sound(520,'Time=12','Effect/RaitonEfx',2)+c(520,'Pay resonance','PowerAdd','Time=47','value=-1500')+c(520,'Karma and Jogan resonance','VarSet','Time=47','v=42\nvalue=1')+c(520,'Twenty second resonance','VarSet','Time=47','v=40\nvalue=1200')+c(520,'Resonance cooldown','VarSet','Time=47','v=41\nvalue=1500')+end(520,62))
def ultimate():
 for form in [0,1]:
  n=3000+10000*form;p=seq('Skill05',23,25,6)+seq('Skill05',26,47,2)+seq('Skill05',56,57,2)+seq('Skill05',63,63,6)+seq('Skill05',111,124,2)+seq('Skill05',73,110,2)+seq('Skill05',141,177,2)+single(idle(),40)
  attack(n,p,form,'5,-100,180,5');s=state(n,n,move='A',physics='N',cost=3000)+startup(n,'BorutoJogan/05')+c(n,'No cinematic push','PlayerPush','1','value=0')+c(n,'Clear confirmed hit','VarSet','Time=0','v=21\nvalue=0')+hit(n,18,0,ident=3000,stun=330)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Remember actual target position','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite Jogan damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{800 if form else 650},Floor((Target(3000),LifeMax)*{.8 if form else .65}))')+c(n,'Confirm contact','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(n,'Approach actual target','PosSet','Time=40 && NumTarget(3000)>0','x=FVar(0)-Facing*70')+c(n,'Hold confirmed opponent','TargetBind','NumTarget(3000)>0 && Time<268','ID=3000\ntime=1\npos=(FVar(0)-Pos X)*Facing,0')+effect(n,'Time=62 && NumTarget(3000)>0',8810,0,-135,.28,20)+effect(n,'Time=100 && NumTarget(3000)>0',8813,0,0,.65,48,-2)
  for i,t in enumerate(PULSES):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)'
   s+=c(n,'Confirmed impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count actual pulse','HitAdd',when,'value=1')+effect(n,when,8700,'(FVar(0)-Pos X)*Facing',-35,.8,9)+sound(n,when,'Effect/BladeA',2)
  s+=sound(n,'Time=184 && NumTarget(3000)>0','Effect/rasenS',2)+sound(n,'Time=244 && NumTarget(3000)>0','Effect/RSGfuton',4)+effect(n,'Time=244 && NumTarget(3000)>0',8814,'(FVar(0)-Pos X)*Facing',0,.4,51)+c(n,'Release rival','TargetState','Time=268 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,290);STATES.append(s)
 STATES.append(state(3010,None,'S','H','N')+c(3010,'Retain opponent artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Independent victim release','SelfState','trigger1=Time>=350\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3011,None,'A','H','N')+c(3011,'Release motion','VelSet','Time=0','x=-4\ny=-6')+c(3011,'Return opponent state ownership','SelfState','1','value=5050\nctrl=0'))
def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite resonance timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 return s+c(-2,'Safe resonance expiry','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Restore base animation bank','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && SelfAnimExist(Anim-10000)','value=Anim-10000')+c(-2,'Resonance animation bank','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+cast(-2,'!IsHelper && RoundState=2 && Var(42)=1 && NumHelper(9560)=0',9560,0,0)+c(-2,'Karma strength','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.18,1)')+c(-2,'Reset air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+sound(-2,'!IsHelper && MoveType=H && Time=0 && StateNo=5000','BorutoJogan/hurt1',0,70)+c(-2,'Stop released charge sound','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round resonance cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')
def main():
 global KEY,SOUNDS
 KEY=json.loads((CHAR/'assets/keys.json').read_text());SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];basic();normals();specials();helpers();utility();ultimate()
 import build_sarada_runtime as ref
 saved=ref.CHAR,ref.MOVES
 try:ref.CHAR=CHAR;ref.MOVES=MOVES;ref.commands()
 finally:ref.CHAR,ref.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';(CHAR/(NAME+'.cmd')).write_text(p.read_text().replace('Pink Susanoo awakening','Karma Jogan resonance'));p.unlink()
 const=(ROOT/'HimawariTBV/HimawariTBV.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):].replace('height=68','height=86').replace('head.pos=0,-62','head.pos=0,-78').replace('mid.pos=0,-34','mid.pos=0,-45')
 (CHAR/(NAME+'.cns')).write_text('; Boruto original sword, Karma, Jogan and Rasengan.\n'+const+(''.join(STATES)+system()).rstrip()+'\n');(CHAR/(NAME+'.air')).write_text('; Original body composites stay on the main player.\n'+''.join(AIR).rstrip()+'\n');(CHAR/(NAME+'_common.cns')).write_text((ROOT/'HimawariTBV/HimawariTBV_common.cns').read_text())
 d=(ROOT/'HimawariTBV/HimawariTBV.def').read_text().replace('HimawariTBV',NAME).replace('Himawari Uzumaki TBV','Boruto Uzumaki Karma Jogan');d=re.sub(r'(?m)^versiondate=.*$','versiondate=10,27,2026',d);(CHAR/(NAME+'.def')).write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,awakening='Karma Jogan resonance; original appearance retained',awakening_requires=3000,awakening_cost=1500,awakening_ticks=1200,ultimate_damage=[650,800],ultimate_cost=3000,ultimate_pulses=PULSES,own_life_cost=0,clone_health=120,clone_ticks=180),indent=2)+'\n');print(NAME,len(STATES),'states;',len(AIR),'animations')
if __name__=='__main__':main()
