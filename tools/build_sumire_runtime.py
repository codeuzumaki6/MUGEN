#!/usr/bin/env python3
"""Sumire: original Suiton, small Nue and controlled giant Nue."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'SumireKakei';AIR=[];STATES=[];KEY={};SOUNDS={}
MOVES=[('Suireiha','a','F',1000,350),('Muro','a','B',1010,400),('Corte','b','F',1020,450),('Cascada','b','B',1030,550),('Taijutsu','c','F',1040,350),('Ascendente','c','B',1050,450),('Bajo','a','D',1400,200),('Doble','b','D',1410,300),('Mordida','c','D',1420,400),('Nue','y','N',1200,250),('Disparo','z','N',1210,200),('AsaltoNue','y','D',1430,450),('Sello','z','D',1440,500)]
def ctl(n,label,typ,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype={typ}\n{triggers}\n{params}\n{extra}\n'
def c(n,label,typ,when,params='',extra=''):return ctl(n,label,typ,'trigger1='+when,params,extra)
def state(n,anim=None,typ='S',move='I',physics='S',cost=0,ctrl=0,vel='0,0'):return f'\n[Statedef {n}]\ntype={typ}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'+(f'anim={anim}\n' if anim is not None else '')+(f'poweradd=-{cost}\n' if cost else '')+(f'velset={vel}\n' if vel else '')
def action(n,seq,form=0,box=None,active=None,loop=False,hurt=True,add=False,loop_start=None,offsets=None,hurt_box=None):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+(hurt_box or ('-70,-120,105,0' if form else '-15,-74,15,0'))+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(seq):
  if i==loop_start:s+='Loopstart\n'
  if box and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+box+'\n'
  if key.startswith('BeastNue') and hurt:s+='Clsn2: 1\n Clsn2[0]=-70,-120,105,0\n'
  g,p=KEY[key];x,y=(offsets or {}).get(key,(0,0));s+=f'{g},{p},{x},{y},{t}'+(',,A' if add else ',H' if n==8802 and key.startswith('NueForm01_') and int(key.rsplit('_',1)[-1])>=6 else '')+'\n'
 AIR.append(s)
def seq(stem,start,end,t=3):return [(f'{stem}_{i:02}',t) for i in range(start,end+1)]
def single(key,t=6):return [(key,t)]
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Original supplied Sumire audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def common_sound(n,when,number=21):return c(n,'Technique effect','PlaySnd',when,f'value=S1,{number}\nchannel=4\nvolumescale=75')
def startup(n,voice=None):return common_sound(n,'Time=0')+(sound(n,'Time=0',voice) if voice else '')+c(n,'Brief activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def end(n,t=52,dest=0):return c(n,'Return control','ChangeState',f'Time>={t}',f'value={dest}\nctrl=1')
def cast(n,when,ident,x='0',y='0',number=None):return c(n,'Finite physical technique','Helper',when,f'helpertype=Normal\nname="Sumire technique"\nID={ident}\nstateno={number or ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def effect(n,when,anim,x=0,y=-40,scale=1,ticks=-2):return c(n,'Original supplied effect','Explod',when,f'anim={anim}\npostype=P1\npos={x},{y}\nscale={scale},{scale}\nremovetime={ticks}\nbindtime=1\nsprpriority={-3 if anim==8801 else 4}\nownpal=1\nremoveongethit=1')
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
def idle(form=0):return 'BeastNue_06' if form else 'Tsunade_Idle2_01'
def attack_action(n,p,form,box=None):
 action(n,p+single(idle(form),-1),form,box=box or ('-35,-120,175,5' if form else '-5,-74,100,3'),active=list(range(len(p))))
def basics():
 for form in [0,1]:
  stand=single(idle(form),8);down=single('Tsunade_KnockDown_05',8)
  poses={0:seq('Tsunade_Idle2',1,3,10),5:stand,6:down,10:down,11:down,12:stand,20:seq('Tsunade_Walk',1,6,4),21:list(reversed(seq('Tsunade_Walk',1,6,4))),100:seq('Tsunade_Walk',1,6,2),105:list(reversed(seq('Tsunade_Walk',1,6,2))),40:single('Tsunade_Skill04_12',6),41:single('Tsunade_AirHurt_01',8),44:single('Tsunade_Float_01',8),52:down+stand,170:single('Tsunade_KnockDown_03',30),180:seq('TsunadeAct',1,2,12)+stand,190:stand,500:seq('Ghost',1,7,5),520:seq('Ghost',1,7,4)*2+seq('BeastNue',1,4,4),5000:seq('Tsunade_Hurt',1,2,6),5010:single('Tsunade_Hurt_02',8),5020:seq('Tsunade_AirHurt',1,2,5),5030:single('Tsunade_Float_01',8),5100:seq('Tsunade_KnockDown',1,3,8),5110:single('Tsunade_KnockDown_03',28),5120:seq('Tsunade_KnockDown',4,5,8)+stand,5150:single('Tsunade_KnockDown_03',60),5200:single('Tsunade_AirHurt_01',8),5210:single('Tsunade_Float_01',8),5300:single('Tsunade_Hurt_01',20)}
  for n in [120,130,140,150,121,131,141,151,122,132,142,152]:poses[n]=single('Tsunade_NAttack_01',6)
  if form:
   poses={n:single('BeastNue_06',sum(max(t,0) for _,t in p) or 8) for n,p in poses.items()}
   for n in [0,5,11,180,190,500]:poses[n]=seq('BeastNue',5,7,8)
   for n in [20,100]:poses[n]=seq('BeastNueWalk',1,6,3 if n==100 else 5)
   for n in [21,105]:poses[n]=list(reversed(seq('BeastNueWalk',1,6,3 if n==105 else 5)))
  for n,p in poses.items():action(n+10000*form,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-45,-25,47,0' if not form and n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,seq('SumireBullet',1,2,3),hurt=False,loop=True,box='-17,-13,23,13')
 action(8801,seq('GozuTenou',1,17,3),hurt=False,add=True)
 action(8802,seq('NueForm01',1,9,3),hurt=False,box='-25,-25,30,20')
 action(8803,seq('BeastNueAtk',1,14,4)*3,hurt=False)
 action(8804,seq('AsepFXSumire',1,7,3),hurt=False)
 action(9700,seq('NueForm02',1,3,6),loop=True,hurt_box='-30,-55,40,0')
 action(9707,seq('NueForm02',4,9,3),loop=True,hurt_box='-30,-55,40,0')
 action(9701,seq('NueForm02',4,16,3),box='-5,-60,100,5',hurt_box='-30,-55,40,0')
 action(9790,single('NueForm02_02',10),hurt_box='-30,-55,40,0')

def normals():
 for form in [0,1]:
  sets=[seq('Tsunade_NAttack',1,4,3),seq('Tsunade_NAttack',5,8,3),seq('Tsunade_NAttack',9,13,3)] if not form else [seq('BeastNueAtk',1,4,3),seq('BeastNueAtk',5,8,3),seq('BeastNueAtk',9,14,3)]
  for family in [200,210,220]:
   for step in range(3):
    n=family+step+10000*form;p=sets[(step+(family-200)//10)%3];attack_action(n,p,form)
    STATES.append(state(n,n,move='A',vel='2,0')+sound(n,'Time=0','SumireKakei/nueF202' if form else 'SumireKakei/Hit',0,70)+hit(n,3,([45,60,80] if form else [36,48,66])[step],step==2,stun=13)+c(n,'Brake normal','VelSet','Time>=8','x=0')+end(n,25))
  for family in [600,610,620]:
   for step in range(3):
    n=family+step+10000*form;attack_action(n,sets[step],form)
    STATES.append(state(n,n,'A','A','N',vel=None)+c(n,'Finite air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief air strike','VelSet','Time<7','x=2\ny=-.4')+c(n,'Air gravity','VelAdd','Time>=7','y=.48')+hit(n,3,([42,54,72] if form else [34,44,60])[step],step==2,air=True,stun=15)+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+end(n,21,50))

def small_nue(n,t=10,command=False):
 s=cast(n,f'Time={t} && NumHelper(9700)=0',9700,'25','0')+effect(n,f'Time={t}',8804,20,0,.6,22)
 if command:s+=c(n,'One Nue assault command','VarAdd',f'Time={t+2}','v=45\nvalue=1')
 return s

def specials():
 for form in [0,1]:
  for name,b,d,base,cost in MOVES:
   n=base+10000*form;p=seq('Tsunade_Skill03',1,7,4);box=None
   if not form:
    if base in [1000,1210]:p=seq('Tsunade_Skill01',1,3,3)+seq('Tsunade_Skill01',4,7,3)*4 if base==1000 else seq('Tsunade_Skill01',1,7,4)
    elif base==1010:p=seq('Tsunade_Suiton',1,11,4);box='-5,-100,165,4'
    elif base==1020:p=single('Tsunade_Skill02_01',5)+seq('Tsunade_Skill02',2,11,4);box='-5,-85,135,4'
    elif base==1030:p=single('Tsunade_Skill02_12',4)+seq('Tsunade_Skill02',13,17,4)+seq('Tsunade_Suiton',1,11,3);box='-5,-90,165,4'
    elif base==1040:p=seq('Tsunade_Skill04',1,11,4)
    elif base==1050:p=seq('Tsunade_Skill04',12,29,3)
    elif base==1400:p=seq('Tsunade_NAttack',9,13,4);box='-5,-42,100,3'
    elif base==1410:p=seq('Tsunade_NAttack',1,8,3)
    elif base==1440:p=seq('Ghost',1,7,5);box='-95,-90,120,5'
   else:
    if base==1000:p=seq('BeastNueAtk',1,7,5)
    elif base==1010:p=seq('BeastNueAtk',8,14,4);box='-35,-90,170,5'
    elif base==1020:p=seq('BeastNueWalk',1,6,3)+seq('BeastNueAtk',1,7,3)
    elif base==1030:p=seq('BeastNueAtk',1,14,4)
    elif base==1040:p=list(reversed(seq('BeastNueWalk',1,6,2)))+seq('BeastNueAtk',2,7,4)
    elif base==1050:p=seq('BeastNueWalk',3,6,4)+seq('BeastNueAtk',1,5,4)
    elif base==1400:p=seq('BeastNueAtk',7,10,5);box='-20,-60,115,5'
    elif base==1410:p=seq('BeastNueAtk',9,14,5);box='-85,-100,135,5'
    elif base==1420:p=seq('BeastNue',5,7,10)
    elif base==1200:p=seq('BeastNue',5,7,10);box='-120,-125,160,5'
    elif base==1210:p=seq('BeastNue',1,4,4)+seq('BeastNueWalk',1,6,3)
    elif base==1430:p=seq('BeastNue',5,7,12);box='-120,-125,175,5'
    elif base==1440:p=seq('BeastNueAtk',8,14,5)+single('BeastNue_06',8);box='-85,-110,170,5'
   attack_action(n,p,form,box);voice='SumireKakei/nueF202' if form else 'SumireKakei/SumireSuiton' if base in [1000,1010,1210] else 'SumireKakei/sumireNue02' if base in [1200,1420,1430,1440] else 'SumireKakei/ikiyo'
   s=state(n,n,move='A',physics='N',cost=cost)+startup(n,voice)
   if not form:
    if base in [1000,1210]:
     for t in ([10,22,34,46] if base==1000 else [10]):s+=cast(n,f'Time={t}',9500,'40','-32')+sound(n,f'Time={t}','SumireKakei/SureihaSfx',2)
    elif base==1010:
     for i,t in enumerate([12,25,38]):s+=hit(n,t,55,i==2,stun=25)
     s+=sound(n,'Time=12','SumireKakei/WtrBarrier',2)
    elif base==1020:s+=c(n,'Water blade rush','VelSet','Time>=5 && Time<25 && !MoveContact','x=7.5')+c(n,'Brake water blade','VelSet','MoveContact || Time>=25','x=0')+hit(n,8,75,stun=29)+hit(n,25,110,True)
    elif base==1030:s+=hit(n,5,75,stun=30)+hit(n,27,90,stun=27)+hit(n,41,95,True)
    elif base==1040:s+=c(n,'Close kunai combination','VelSet','Time<14 && !MoveContact','x=4')+c(n,'Brake combination','VelSet','MoveContact || Time>=14','x=0')+hit(n,6,65,stun=29)+hit(n,24,110,True)
    elif base==1050:s+=c(n,'Jump into the kunai strike','VelSet','Time=4','x=4\ny=-7')+c(n,'Air state','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Gravity','VelAdd','Time>4','y=.44')+hit(n,7,70,air=True,stun=28)+hit(n,23,110,True,air=True)+c(n,'Original landing frames','ChangeState','Time>20 && Pos Y>=0 && Vel Y>0','value=1060\nctrl=0')
    elif base==1400:s+=c(n,'Low approach','VelSet','Time<13','x=3.5')+c(n,'Brake low cut','VelSet','Time>=13','x=0')+hit(n,5,100,True,low=True)
    elif base==1410:s+=hit(n,4,55,stun=25)+hit(n,16,90,True)
    elif base==1420:s+=cast(n,'Time=9',9502,'30','-30')+sound(n,'Time=9','SumireKakei/NueF1',2)
    elif base in [1200,1430]:s+=small_nue(n,10,base==1430)
    elif base==1440:s+=effect(n,'Time=8',8801,35,-70,.24,51)+hit(n,12,80,stun=28)+hit(n,29,120,True)
   else:
    if base in [1020,1210]:s+=c(n,'Nue charges physically','VelSet','Time<24 && !MoveContact','x='+('10' if base==1210 else '7.5'))+c(n,'Brake Nue','VelSet','MoveContact || Time>=24','x=0')+hit(n,9,185 if base==1210 else 110,base==1210,stun=28)+(hit(n,26,130,True) if base==1020 else '')
    elif base==1040:s+=c(n,'Nue recoils before pouncing','VelSet','Time<8','x=-4')+c(n,'Predatory countercharge','VelSet','Time>=8 && Time<25 && !MoveContact','x=10')+c(n,'Brake the pounce','VelSet','MoveContact || Time>=25','x=0')+hit(n,16,225,True)
    elif base==1050:s+=c(n,'Nue leaps','VelSet','Time=4','x=5\ny=-6.5')+c(n,'Nue in the air','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Nue gravity','VelAdd','Time>4','y=.44')+hit(n,7,95,air=True,stun=28)+hit(n,23,140,True,air=True)+c(n,'Nue lands','ChangeState','Time>20 && Pos Y>=0 && Vel Y>0','value=11060\nctrl=0')
    elif base==1000:s+=hit(n,6,90,stun=28)+hit(n,20,125,True)
    elif base==1010:s+=hit(n,6,100,stun=28,low=True)+hit(n,23,130,True,low=True)
    elif base==1030:
     for i,t in enumerate([8,24,42]):s+=hit(n,t,[75,85,110][i],i==2,stun=27)
    elif base==1400:s+=hit(n,6,175,True,low=True)
    elif base==1410:s+=hit(n,18,230,True)
    elif base==1420:s+=cast(n,'Time=9',9502,'80','-45')
    elif base==1200:s+=effect(n,'Time=8',8801,20,-65,.28,51)+hit(n,12,190,True)
    elif base==1430:s+=effect(n,'Time=8',8801,20,-65,.28,51)+hit(n,12,100,stun=30)+hit(n,32,145,True)
    elif base==1440:
     for i,t in enumerate([8,22,34]):s+=hit(n,t,[70,85,100][i],i==2,stun=27)
   s+=end(n,max(50,sum(t for _,t in p)),50 if base==1050 else 0);STATES.append(s)
  n=1060+10000*form;action(n,seq('BeastNue',5,7,4) if form else seq('Tsunade_Skill04',30,39,2),form);STATES.append(state(n,n)+c(n,'Ground the landing','PosSet','Time=0','y=0')+end(n,14 if form else 20))

def helpers():
 for n in [9500,9502]:
  s=state(n,8800 if n==9500 else 8802,'A','A','N',vel='11,0' if n==9500 else '8,0')+c(n,'No projectile push','PlayerPush','1','value=0')+c(n,'No projectile shadow','AssertSpecial','1','flag=NoShadow')+c(n,'Projectile power','VarSet','Time=0','v=0\nvalue='+('IfElse((Root,StateNo%10000)=1210,110,45)' if n==9500 else 'IfElse((Root,Var(42)),190,145)'))+c(n,'Spectral bite size','AngleDraw','1','scale='+('1,1' if n==9500 else '.8,.8'))+hit(n,0,'Var(0)',n==9502,air=True,projectile=True)+c(n,'Finite projectile','DestroySelf','MoveContact || Time>=50 || RoundState!=2');STATES.append(s)
 for n in [9700,9701,9790]:
  s=state(n,n,'S','H' if n==9790 else 'I' if n==9700 else 'A','N')
  if n==9700:s+=c(n,'Small Nue health','LifeSet','Time=0 && Var(2)=0','value=180')+c(n,'Initialize Nue command','VarSet','Time=0 && Var(2)=0','v=1\nvalue=Parent,Var(45)')+c(n,'Initialize once','VarSet','Time=0','v=2\nvalue=1')
  else:s+=c(n,'Consume Nue order','VarSet','Time=0','v=1\nvalue=Parent,Var(45)')
  s+=c(n,'Nue body size','AngleDraw','1','scale=.7,.7')+c(n,'Small Nue age','VarAdd','1','v=5\nvalue=1','ignorehitpause=1')+c(n,'No familiar push','PlayerPush','1','value=0')+c(n,'Nue can be hit','HitOverride','1','attr=SCA,NA,SA,HA,NP,SP,HP,NT,ST,HT\nstateno=9790\ntime=1\nforceair=0','ignorehitpause=1')+c(n,'Nue defeat, fusion and expiry','DestroySelf','Var(2)=1 && (Life<=0 || Var(5)>=420 || (Root,Var(42))=1 || (Root,StateNo%10000)=3000 || (Root,Life)<=0 || RoundState!=2)')+c(n,'Face the opponent','Turn','P2Dist X<0','')
  if n!=9790:s+=c(n,'Take the actual attack order','ChangeState','(Parent,Var(45))!=Var(1)','value=9701\nctrl=0')
  if n==9700:s+=c(n,'Follow the opponent','VelSet','1','x=IfElse(Abs(P2Dist X)>70,3,0)')+c(n,'Nue running pose','ChangeAnim','Abs(P2Dist X)>70 && Anim!=9707','value=9707')+c(n,'Nue idle pose','ChangeAnim','Abs(P2Dist X)<=70 && Anim!=9700','value=9700')+c(n,'Autonomous Nue assault','ChangeState','Time>=36 && Abs(P2Dist X)<100','value=9701')
  elif n==9790:s+=c(n,'Visible hit response','PalFX','1','time=1\nadd=70,-30,-30')+end(n,10,9700)
  else:s+=c(n,'Actual Nue approach','VelSet','Time<12 && !MoveContact','x=7')+c(n,'Brake on contact','VelSet','MoveContact || Time>=12','x=0')+hit(n,8,50,stun=25)+hit(n,23,65,True)+sound(n,'Time=8','SumireKakei/NueF2',2)+end(n,43,9700)
  STATES.append(s)

def utility():
 for n in [170,180,190]:
  s=state(n,n)+sound(n,'Time=0','SumireKakei/SumireKnock' if n==170 else 'SumireKakei/sumiretalk')
  if n==190:s+=c(n,'Brief intro','AssertSpecial','Time<40','flag=Intro')+end(n,44)
  STATES.append(s)
 STATES.append(state(500,500)+c(500,'Charge chakra','PowerAdd','1','value=20')+sound(500,'Time=0','Effect/AuraGate',3)+cast(500,'Time=0 && Var(42)=1 && NumHelper(9551)=0',9551)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 STATES.append(state(9551,8900,'A','I','N')+c(9551,'Nue energy follows its single body','BindToRoot','1','time=1\npos=0,-55')+c(9551,'Violet energy','PalFX','1','time=1\ncolor=0\nmul=175,70,256')+c(9551,'Energy column','AngleDraw','1','value=90\nscale=.45,.5')+c(9551,'Behind Nue','SprPriority','1','value=-2')+c(9551,'Aura ends with charging','DestroySelf','(Root,StateNo)!=500 || RoundState!=2'))
 STATES.append(state(520,520)+startup(520,'SumireKakei/Sumirevoice')+effect(520,'Time=12',8801,0,-85,.28,51)+c(520,'Pay the transformation','PowerAdd','Time=56','value=-1500')+c(520,'Control giant Nue','VarSet','Time=56','v=42\nvalue=1')+c(520,'Twenty second giant form','VarSet','Time=56','v=40\nvalue=1200')+c(520,'Transformation cooldown','VarSet','Time=56','v=41\nvalue=1500')+end(520,74))

def ultimate():
 for form in [0,1]:
  n=3000+10000*form;pose=seq('BeastNueAtk',1,14,4)*3+single('BeastNue_06',32) if form else seq('Ghost',1,7,4)*7+single('Tsunade_Skill03_07',8)
  attack_action(n,pose,form,'5,-130,240,5');s=state(n,n,move='A',physics='N',cost=3000)+startup(n,'SumireKakei/Nue02' if form else 'SumireKakei/Sumirevoice')+c(n,'No push during the confirmed ultimate','PlayerPush','1','value=0')+c(n,'Clear ultimate contact','VarSet','Time=0','v=21\nvalue=0')+hit(n,18,0,ident=3000,stun=240)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Record the actual opponent','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite Nue damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{700 if form else 550},Floor((Target(3000),LifeMax)*{.7 if form else .55}))')+c(n,'Confirm real impact','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(n,'Hold only a confirmed rival','TargetBind','NumTarget(3000)>0 && Time<200','ID=3000\ntime=1\npos=(FVar(0)-Pos X)*Facing,0')+effect(n,'Time=22 && NumTarget(3000)>0',8801,'(FVar(0)-Pos X)*Facing',-80,.28,51)
  if not form:s+=effect(n,'Time=45 && NumTarget(3000)>0',8803,'(FVar(0)-Pos X)*Facing-75',0,.65,168).replace('sprpriority=4','sprpriority=-2')
  for i,t in enumerate([44,64,84,104,124,144,164,184]):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)';s+=c(n,'Confirmed seal and claw impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count actual impact','HitAdd',when,'value=1')+effect(n,when,8700,'(FVar(0)-Pos X)*Facing',-35,.8,9)+sound(n,when,'Effect/BladeDamageMD01',2)
  s+=c(n,'Release the opponent','TargetState','Time=200 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,224);STATES.append(s)
 STATES.append(state(3010,None,'S','H','N')+c(3010,'Opponent keeps its own artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Independent victim release','SelfState','trigger1=Time>=260\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3011,None,'A','H','N')+c(3011,'Real release motion','VelSet','Time=0','x=-4\ny=-6')+c(3011,'Restore opponent state ownership','SelfState','1','value=5050\nctrl=0'))

def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite Nue timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe return to Sumire','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Restore Sumire artwork','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && SelfAnimExist(Anim-10000)','value=Anim-10000')+c(-2,'Controlled giant Nue artwork','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+c(-2,'Original giant body scale','AngleDraw','!IsHelper && (Anim>=10000 || (StateNo=520 && Time>=56))','scale=.65,.65')+c(-2,'Actual beast body width','Width','!IsHelper && Var(42)=1','player=65,95\nedge=65,95')+c(-2,'Nue physical strength','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.18,1)')+c(-2,'Reset grounded air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop released charge audio','StopSnd','!IsHelper && StateNo!=500','channel=3')+sound(-2,'!IsHelper && MoveType=H && Time=0 && StateNo=5000','SumireKakei/SumireHurt',0,70)+c(-2,'Round form cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')
 return s

def main():
 global KEY,SOUNDS
 KEY=json.loads((CHAR/'assets/keys.json').read_text());SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];basics();normals();specials();helpers();utility();ultimate()
 import build_sarada_runtime as ref
 saved=ref.CHAR,ref.MOVES
 try:ref.CHAR=CHAR;ref.MOVES=MOVES;ref.commands()
 finally:ref.CHAR,ref.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';(CHAR/'SumireKakei.cmd').write_text(p.read_text().replace('Pink Susanoo awakening','Giant Nue transformation'));p.unlink()
 const=(ROOT/'JigenKara/JigenKara.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):].replace('life=1300','life=1200').replace('defence=110','defence=105').replace('height=86','height=75')
 (CHAR/'SumireKakei.cns').write_text('; Original Sumire, Suiton, familiar and full controlled Nue form.\n'+const+(''.join(STATES)+system()).rstrip()+'\n');(CHAR/'SumireKakei.air').write_text('; Original complete bodies and separate projectiles.\n'+''.join(AIR).rstrip()+'\n');(CHAR/'SumireKakei_common.cns').write_text((ROOT/'JigenKara/JigenKara_common.cns').read_text())
 d=(ROOT/'JigenKara/JigenKara.def').read_text().replace('JigenKara','SumireKakei').replace('"Jigen"','"Sumire Kakei"');d=re.sub(r'(?m)^author=.*$','author="VaydraSenki original sprites, sheet and audio / Codex adaptation"',d);d=re.sub(r'(?m)^versiondate=.*$','versiondate=10,26,2026',d);(CHAR/'SumireKakei.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,base='Sumire Kakei',awakening='Controlled giant Nue',awakening_ticks=1200,awakening_requires=3000,awakening_cost=1500,ultimate_cost=3000,ultimate_damage=[550,700],own_life_cost=0,familiar_health=180,familiar_ticks=420,beast_scale=.65),indent=2)+'\n');print('Sumire runtime:',len(STATES),'states;',len(AIR),'animations')
if __name__=='__main__':main()
