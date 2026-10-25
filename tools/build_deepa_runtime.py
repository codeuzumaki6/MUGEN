#!/usr/bin/env python3
"""Deepa Kara: supplied carbon techniques and a separate armored moveset."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'DeepaKara';AIR=[];STATES=[];KEY={};SOUNDS={}
MOVES=[('Rafaga','a','F',1000,350),('Disco','a','B',1010,400),('Perforacion','b','F',1020,450),('Asalto','b','B',1030,450),('Ascendente','c','F',1040,350),('Agujas','c','B',1050,500),('Barrido','a','D',1400,200),('Pesado','b','D',1410,300),('Estallido','c','D',1420,400),('Bala','y','N',1200,200),('Aro','z','N',1210,250),('Trampa','y','D',1430,500),('Embestida','z','D',1440,350)]
def ctl(n,label,typ,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype={typ}\n{triggers}\n{params}\n{extra}\n'
def c(n,label,typ,when,params='',extra=''):return ctl(n,label,typ,'trigger1='+when,params,extra)
def state(n,anim=None,typ='S',move='I',physics='S',cost=0,ctrl=0,vel='0,0'):return f'\n[Statedef {n}]\ntype={typ}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'+(f'anim={anim}\n' if anim is not None else '')+(f'poweradd=-{cost}\n' if cost else '')+(f'velset={vel}\n' if vel else '')
def action(n,seq,form=0,box=None,active=None,loop=False,hurt=True,add=False,loop_start=None,offsets=None,hurt_box=None):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+(hurt_box or ('-20,-92,20,0' if form else '-16,-90,16,0'))+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(seq):
  if i==loop_start:s+='Loopstart\n'
  if box and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+box+'\n'
  g,p=KEY[key];x,y=(offsets or {}).get(key,(0,0));s+=f'{g},{p},{x},{y},{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def seq(stem,start,end,t=3):return [(f'{stem}_{i:02}',t) for i in range(start,end+1)]
def single(key,t=6):return [(key,t)]
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Supplied Deepa audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def common_sound(n,when,number=21):return c(n,'Technique effect','PlaySnd',when,f'value=S1,{number}\nchannel=4\nvolumescale=75')
def startup(n,voice=None):return common_sound(n,'Time=0')+(sound(n,'Time=0',voice) if voice else '')+c(n,'Brief activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def end(n,t=52,dest=0):return c(n,'Return control','ChangeState',f'Time>={t}',f'value={dest}\nctrl=1')
def cast(n,when,ident,x='0',y='0',number=None):return c(n,'Finite physical technique','Helper',when,f'helpertype=Normal\nname="Deepa technique"\nID={ident}\nstateno={number or ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
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

def basics():
 base={0:seq('Kinkaku_Idle',1,5,10),5:single('Kinkaku_Idle_01'),6:single('Kinkaku_KnockDown_03'),10:single('Kinkaku_KnockDown_03'),11:single('Kinkaku_KnockDown_03'),12:single('Kinkaku_Idle_01'),20:seq('Kinkaku_Walk',1,6,4),21:list(reversed(seq('Kinkaku_Walk',1,6,4))),100:seq('Kinkaku_Walk',1,6,2),105:list(reversed(seq('Kinkaku_Walk',1,6,2))),40:single('Kinkaku_NAttack_06',5),41:single('Kinkaku_Float_01',8),44:single('Kinkaku_AirHurt_01',8),52:single('Kinkaku_KnockDown_03',8)+single('Kinkaku_Idle_01',5),170:single('Kinkaku_KnockDown_02',30),180:seq('Kinkaku_Idle',1,5,12),190:seq('Kinkaku_Idle',1,5,8),500:seq('Kinkaku_01_Chg',1,3,8),520:seq('Deepa_Trans',1,9,4),5000:seq('Kinkaku_Hurt',1,2,8),5010:single('Kinkaku_KnockDown_03',8),5020:single('Kinkaku_AirHurt_01',8),5030:single('Kinkaku_Float_01',8),5100:seq('Kinkaku_KnockDown',1,2,8),5110:single('Kinkaku_KnockDown_02',28),5120:single('Kinkaku_KnockDown_03',12)+single('Kinkaku_Idle_01',8),5150:single('Kinkaku_KnockDown_02',60),5200:single('Kinkaku_AirHurt_01',8),5210:single('Kinkaku_Float_01',8),5300:single('Kinkaku_Hurt_01',20)}
 for n in [120,130,140,150]:base[n]=single('Kinkaku_NAttack_01',5)
 for n in [121,131,141,151,122,132,142,152]:base[n]=single('Kinkaku_KnockDown_03',5)
 for n,poses in base.items():
  action(n,poses,loop=n in [0,11,20,21,100,105,41,44,500,5150])
  armored=seq('Deepa_Walk',1,3,4) if n in [20,21,100,105] else single('Deepa_UnUse_01',8) if n in [10,11,12,121,131,141,151,5010,5120] else single('Deepa_Idle',8)
  if n in [105,21]:armored=list(reversed(armored))
  action(n+10000,armored,1,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-48,-30,50,0' if n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{n}',3) for n in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,single('Carbon_Cube',4),hurt=False,loop=True,box='-12,-12,12,12')
 action(8801,seq('Kinkaku_Skill02_MonWalk',1,2,3),hurt=False,loop=True,box='-22,-18,22,18')
 action(8802,seq('Kinkaku_Skill02_Mon',1,4,4),hurt=False)
 action(8803,single('Carbon_Cube',4),hurt=False,loop=True,box='-25,-25,25,25')
 action(8804,seq('Kinkaku_Skill02_Mon',1,4,4),hurt=False,box='-70,-60,70,15')

def normals():
 for form in [0,1]:
  off=form*10000
  banks={200:[seq('Kinkaku_NAttack',1,3,3),seq('Kinkaku_NAttack',4,5,4),seq('Kinkaku_NAttack',6,8,4)],210:[seq('Kinkaku_NAttack',6,8,4),seq('Kinkaku_NAttack',2,3,4),seq('Kinkaku_NAttack',7,8,5)],220:[seq('Kinkaku_NAttack',4,5,4),seq('Kinkaku_NAttack',2,3,4),seq('Kinkaku_01_Chg',3,4,5)]}
  for base,poses in banks.items():
   for step in range(3):
    n=base+step+off;p=poses[step]
    if form:p=single('Deepa_Idle',3)+single('Deepa_Hit01_07' if (base+step)%2 else 'Deepa_Hit02_07',10)+single('Deepa_UnUse_01',8)
    action(n,p+single('Deepa_Idle' if form else 'Kinkaku_Idle_01',-1),form,box='-3,-83,80,0',active=list(range(1,len(p))))
    s=state(n,n,move='A',vel='2,0')+sound(n,'Time=0','haa')+hit(n,3,[48,60,78][step] if form else [40,52,70][step],step==2,stun=12)+c(n,'Brake short normal','VelSet','Time>=8','x=0')+end(n,24);STATES.append(s)
  for base in [600,610,620]:
   for step in range(3):
    n=base+step+off;p=single('Deepa_Idle',3)+single('Deepa_Hit02_07' if step!=1 else 'Deepa_Hit01_07',10)+single('Deepa_UnUse_01',6) if form else single('Kinkaku_NAttack_06',3)+single('Kinkaku_NAttack_07' if step!=1 else 'Kinkaku_NAttack_04',10)+single('Kinkaku_NAttack_08',6)
    action(n,p+single('Deepa_Idle' if form else 'Kinkaku_Idle_01',-1),form,box='-4,-85,85,0',active=list(range(len(p))))
    s=state(n,n,'A','A','N',vel=None)+c(n,'Finite air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief juggle','VelSet','Time<7','x=2\ny=-.4')+c(n,'Gravity resumes','VelAdd','Time>=7','y=.48')+hit(n,3,[42,52,72][step] if form else [35,45,62][step],step==2,air=True,stun=15)+c(n,'Land safely','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+end(n,20,50);STATES.append(s)

def specials():
 for form in [0,1]:
  off=form*10000
  baseposes={1000:seq('Kinkaku_01_Chg',1,4,2)+seq('Kinkaku_Skill01',1,17,2),1010:seq('Kinkaku_Skill02_Chg',1,5,3)+seq('Kinkaku_Skill02',1,3,4),1020:seq('Kinkaku_Skill03_Chg',1,4,3)+seq('Kinkaku_Skill03',1,9,3),1030:seq('Kinkaku_Skill03_Chg',1,4,2)+seq('Kinkaku_Skill03_Punch',1,5,5),1040:single('Kinkaku_NAttack_06',6)+seq('Kinkaku_NAttack',7,8,8),1050:seq('Kinkaku_Skill03_Chg',1,4,4)+seq('Kinkaku_Skill03',1,9,4),1400:single('Kinkaku_NAttack_06',4)+seq('Kinkaku_NAttack',7,8,8),1410:seq('Kinkaku_NAttack',1,5,4),1420:seq('Kinkaku_01_Chg',1,4,5),1200:seq('Kinkaku_01_Chg',3,4,8),1210:seq('Kinkaku_Skill02',1,3,5),1430:seq('Kinkaku_Skill02_Chg',1,5,4)+seq('Kinkaku_Skill02',1,3,4),1440:seq('Kinkaku_Walk',1,3,3)+seq('Kinkaku_NAttack',2,5,5)}
  armpose={1000:seq('Deepa_Hit01',1,7,4),1010:seq('Deepa_Hit01',1,7,3)+seq('Deepa_Hit02',1,7,3),1020:seq('Deepa_Hit02',1,7,5),1030:seq('Deepa_Walk',1,3,3)+seq('Deepa_Hit01',1,7,4),1040:single('Deepa_UnUse_01',6)+single('Deepa_Hit01_07',12)+single('Deepa_Hit02_07',8),1050:seq('Deepa_Hit01',1,7,3)+seq('Deepa_Hit02',1,7,3),1400:single('Deepa_UnUse_01',4)+single('Deepa_Hit02_07',16),1410:single('Deepa_Idle',6)+seq('Deepa_Hit01',1,7,4),1420:single('Deepa_UnUse_01',12)+single('Deepa_Idle',18),1200:single('Deepa_UnUse_01',8)+single('Deepa_Hit02_07',12),1210:single('Deepa_Idle',6)+single('Deepa_Hit02_07',18),1430:single('Deepa_UnUse_01',16)+single('Deepa_Hit01_07',18),1440:seq('Deepa_Walk',1,3,3)+seq('Deepa_Hit02',1,7,4)}
  for name,b,d,base,cost in MOVES:
   n=base+off;p=(armpose if form else baseposes)[base];box='-5,-85,100,2'
   if base==1020:box='5,-85,220,5'
   if base in [1010,1050] and form:box='0,-95,125,5'
   if base==1040:box='-5,-110,85,3'
   if base==1400:box='-5,-48,85,4'
   action(n,p+single('Deepa_Idle' if form else 'Kinkaku_Idle_01',-1),form,box=box,active=list(range(len(p))))
   s=state(n,n,move='A',physics='N',cost=cost)+startup(n,'geram' if form else 'Korewa' if base in [1000,1200] else 'haa')
   if base==1000:
    if form:s+=hit(n,4,85,False,stun=25)+hit(n,15,125,True,stun=28)+sound(n,'Time=4','lempeng2',2)
    else:
     for t in [8,16,24]:s+=cast(n,f'Time={t}',9402,'34','-35')+sound(n,f'Time={t}','Deepa Blt Sfx',2)
   elif base==1010:
    if form:s+=hit(n,4,100,False,stun=28)+hit(n,26,145,True,stun=28)+sound(n,'Time=4','Burst Deepa',2)
    else:s+=cast(n,'Time=16',9412,'30','-30')+sound(n,'Time=16','Throw',2)
   elif base==1020:s+=hit(n,12,225 if form else 175,True,stun=30)+sound(n,'Time=12','blading sfx',2)
   elif base==1030:
    s+=c(n,'Real forward charge','VelSet','Time>=8 && Time<27 && !MoveContact','x=8.5')+c(n,'Brake actual contact','VelSet','MoveContact || Time>=27','x=0')
    if form:s+=hit(n,8,65,False,stun=26)+hit(n,23,155,True,stun=30)
    else:s+=hit(n,8,195,True,stun=30)
    s+=sound(n,'Time=8','sfx01',2)
   elif base==1040:
    s+=c(n,'Rising carbon strike','VelSet','Time=6','x=3\ny=-6.5')+c(n,'Actual airborne rise','StateTypeSet','Time=6','statetype=A\nphysics=N')+c(n,'Real gravity','VelAdd','Time>6','y=.44')+hit(n,6,85 if form else 65,False,air=True)+hit(n,15,115 if form else 95,True,air=True)+c(n,'Land the ascent','ChangeState','Time>18 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
   elif base==1050:
    if form:
     for i,t in enumerate([4,15,26,37]):s+=hit(n,t,65,i==3,stun=20)
    else:
     for i,t in enumerate([16,24,32]):s+=cast(n,f'Time={t}',9401+i,'35',str(-24-i*12))
    s+=sound(n,'Time=16','Grinda',2)
   elif base==1400:s+=c(n,'Low sweeping step','VelSet','Time<14','x=4')+c(n,'Brake sweep','VelSet','Time>=14','x=0')+hit(n,4,135 if form else 105,True,low=True)
   elif base==1410:s+=hit(n,4,80 if form else 55,False,stun=24)+hit(n,15,120 if form else 100,True)
   elif base==1420:s+=cast(n,'Time=10',9430,'0','-20')+sound(n,'Time=10','Burst Deepa',2)
   elif base==1200:s+=cast(n,'Time=8',9400,'35','-30')+sound(n,'Time=8','Deepa Blt Sfx',2)
   elif base==1210:s+=cast(n,'Time=10',9410,'30','-30')+sound(n,'Time=10','Throw',2)
   elif base==1430:s+=cast(n,'Time=16',9421 if form else 9420,'IfElse(P2Dist X<180,P2Dist X,180)','-160' if form else '-15')+sound(n,'Time=16','lempeng',2)
   elif base==1440:
    s+=c(n,'Short armored approach','VelSet','Time>=7 && Time<26 && !MoveContact','x=7')+c(n,'Stop on contact','VelSet','MoveContact || Time>=26','x=0')+hit(n,8,70 if form else 145,not form,stun=26)
    if form:s+=hit(n,22,135,True,stun=28)
   s+=end(n,max(48,sum(t for _,t in p)),50 if base==1040 else 0);STATES.append(s)

def helpers():
 for n in [9400,9401,9402,9403,9410,9412,9413,9420,9421,9430]:
  anim=8800 if n<=9403 else 8801 if n in [9410,9412,9413,9420] else 8803 if n==9421 else 8804
  speed='11,0' if n==9400 else f'12,{[-1,0,1][n-9401]}' if n<=9403 else '10,0' if n==9410 else '8,0' if n==9412 else '-8,0' if n==9413 else '0,8' if n==9421 else '0,0'
  s=state(n,anim,'A','A','N',vel=speed)+c(n,'No projectile push','PlayerPush','1','value=0')+c(n,'No projectile shadow','AssertSpecial','1','flag=NoShadow')
  damage='IfElse((Root,Var(42))>0,145,105)' if n==9400 else '65' if n<=9403 else 'IfElse((Root,Var(42))>0,190,145)' if n==9410 else '145' if n==9412 else '75' if n==9413 else '165' if n==9420 else '220' if n==9421 else 'IfElse((Root,Var(42))>0,195,145)'
  s+=c(n,'Snapshot original technique power','VarSet','Time=0','v=0\nvalue='+damage)
  if n<=9403:s+=c(n,'Original carbon cube scale','AngleDraw','1','scale=IfElse((Root,Var(42))>0,.8,.55),IfElse((Root,Var(42))>0,.8,.55)')
  if n==9421:s+=c(n,'Heavy original carbon cube','AngleDraw','1','scale=1.2,1.2')
  if n==9430:s+=c(n,'Original burst size','AngleDraw','1','scale=1.2,1.2')
  s+=hit(n,22 if n==9420 else 4 if n==9430 else 0,'Var(0)',n!=9412,air=True,projectile=True,stun=28)
  if n==9412:s+=c(n,'Disc returns after actual contact','ChangeState','MoveContact || Time>=25','value=9413')
  elif n in [9410,9413,9421]:s+=c(n,'Original disc impact','ChangeState','MoveContact || (Pos Y>=-8 && Vel Y>0)','value=9411')
  else:s+=c(n,'Resolve actual projectile contact','DestroySelf','MoveContact')
  if n==9413:s+=c(n,'Returning disc reaches its caster','DestroySelf','Abs(Pos X-(Root,Pos X))<18 && Time>2')
  s+=c(n,'Finite projectile lifetime','DestroySelf','Time>=65 || RoundState!=2');STATES.append(s)
 s=state(9411,8802,'A','I','N')+c(9411,'Original impact only','Null','1')+sound(9411,'Time=0','Burst Deepa',2)+c(9411,'Impact expires','DestroySelf','AnimTime=0 || Time>=20 || RoundState!=2');STATES.append(s)

def utility():
 for n in [170,180,190]:
  s=state(n,n)+c(n,'Round pose','Null','1')+sound(n,'Time=0','die' if n==170 else 'DeepaLaugh' if n==180 else 'Korewa')
  if n==190:s+=c(n,'Brief intro','AssertSpecial','Time<40','flag=Intro')+end(n,44)
  STATES.append(s)
 s=state(500,500)+c(500,'Charge meter','PowerAdd','1','value=20')+cast(500,'Time=0 && NumHelper(9550)=0',9550)+sound(500,'Time=0','Chg Deepa',3)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1');STATES.append(s)
 s=state(9550,8900,'A','I','N')+c(9550,'Follow charge','BindToRoot','1','time=1\npos=0,-45')+c(9550,'Vertical charge aura','AngleDraw','1','value=90\nscale=.32,.38')+c(9550,'Green carbon energy','PalFX','1','time=1\ncolor=0\nmul=65,256,145')+c(9550,'Behind the real body','SprPriority','1','value=-2')+ctl(9550,'Finite charge effect','DestroySelf','trigger1=Root,StateNo!=500\ntrigger2=RoundState!=2');STATES.append(s)
 s=state(520,520)+startup(520,'geram')+sound(520,'Time=0','deepa trans',2)+c(520,'Pay for the transformation','PowerAdd','Time=32','value=-1500')+c(520,'Armored mode','VarSet','Time=32','v=42\nvalue=1')+c(520,'Twenty seconds of armor','VarSet','Time=32','v=40\nvalue=1200')+c(520,'Awakening cooldown','VarSet','Time=32','v=41\nvalue=1500')+end(520,46);STATES.append(s)

def ultimate():
 base=seq('Kinkaku_Skill04_CHG',1,7,4)+seq('Kinkaku_Skill04',1,15,4)+seq('Kinkaku_Skill04',9,13,4)*3+seq('Kinkaku_Idle',1,1,14)
 armor=single('Deepa_UnUse_01',8)+(seq('Deepa_Hit01',1,7,3)+seq('Deepa_Hit02',1,7,3))*4+single('Deepa_Idle',12)
 for form in [0,1]:
  n=3000+10000*form;action(n,(armor if form else base)+single('Deepa_Idle' if form else 'Kinkaku_Idle_01',-1),form,box='-5,-95,110,5' if form else '15,-90,250,10',active=list(range(len(armor if form else base))))
  s=state(n,n,move='A',physics='N',cost=3000)+startup(n,'geram' if form else 'tose')+c(n,'Reset confirmed damage','VarSet','Time=0','v=21\nvalue=0')
  if form:s+=c(n,'Armored finishing approach','VelSet','Time>=6 && Time<26 && !MoveContact','x=6')+c(n,'Brake confirmed contact','VelSet','MoveContact || Time>=26','x=0')
  s+=hit(n,14 if form else 28,0,False,ident=3000,stun=220)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Store only the struck enemy position','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite ultimate damage ceiling','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{700 if form else 550},Floor((Target(3000),LifeMax)*{.70 if form else .55}))')+c(n,'Confirmed collision','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')
  s+=c(n,'Hold only the confirmed enemy','TargetBind','NumTarget(3000)>0 && Time<184','ID=3000\ntime=1\npos=(FVar(0)-Pos X)*Facing,0')
  times=[35,55,75,95,115,135,155,175] if form else [60,80,100,120,140,160]
  for i,t in enumerate(times):
   value=f'Var(20)-Floor(Var(20)/{len(times)})*{len(times)-1}' if i==len(times)-1 else f'Floor(Var(20)/{len(times)})'
   when=f'Time={t} && NumTarget(3000)>0'
   s+=c(n,'Bounded confirmed damage pulse','TargetLifeAdd',when,'ID=3000\nvalue=-('+value+')\nabsolute=1\nkill=1')+c(n,'Count the carbon impact','HitAdd',when,'value=1')+sound(n,when,'lempeng2' if form else 'Beam deepa',2,80)+effect(n,when,8802,'(FVar(0)-Pos X)*Facing',-35,.8,14)
  s+=c(n,'Release the victim','TargetState','Time=184 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,202);STATES.append(s)
 s=state(3010,None,'S','H','N')+c(3010,'Opponent uses its own hurt artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Guaranteed victim release','SelfState','trigger1=Time>=230\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0');STATES.append(s)
 s=state(3011,None,'A','H','N')+c(3011,'Real release velocity','VelSet','Time=0','x=-5\ny=-6')+c(3011,'Return opponent to its own states','SelfState','1','value=5050\nctrl=0');STATES.append(s)

def commands():
 # The project controls remain familiar; each mode resolves to its own states.
 import build_sarada_runtime as ref
 saved=ref.CHAR,ref.MOVES
 try:ref.CHAR=CHAR;ref.MOVES=MOVES;ref.commands()
 finally:ref.CHAR,ref.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';s=p.read_text().replace('Pink Susanoo awakening','Carbon armor awakening')
 (CHAR/'DeepaKara.cmd').write_text(s);p.unlink()

def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite armor timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe return from armor','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Refresh base body','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')+c(-2,'Armor uses only the armored bank','ChangeAnim','!IsHelper && Var(42)=1 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')
 s+=c(-2,'Armor resists damage but remains hittable','DefenceMulSet','!IsHelper','value=IfElse(Var(42)=1,.70,1)','ignorehitpause=1')+c(-2,'Armored physical power','AttackMulSet','!IsHelper','value=IfElse(Var(42)=1,1.15,1)')
 s+=c(-2,'Reset air chains','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charging audio','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round armor cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')+sound(-2,'!IsHelper && StateNo=5000 && Time=0','hurt',0,70)
 return s

def main():
 global KEY,SOUNDS
 KEY=json.loads((CHAR/'assets/keys.json').read_text());SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];basics();normals();specials();helpers();utility();ultimate();commands()
 const=(ROOT/'JuraShinju/JuraShinju.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):].replace('life=1300','life=1250').replace('defence=115','defence=110').replace('height=84','height=92')
 (CHAR/'DeepaKara.cns').write_text(('; Deepa: original base and carbon armor artwork with separate moves.\n'+const+''.join(STATES)+system()).rstrip()+'\n');(CHAR/'DeepaKara.air').write_text(('; Original Deepa frames only, no unrelated donor body.\n'+''.join(AIR)).rstrip()+'\n')
 s=(ROOT/'JuraShinju/JuraShinju_common.cns').read_text();s=re.sub(r'(?m)^anim\s*=\s*(\d+)\s*$',r'anim=\1+10000*Var(42)',s);blocks=re.split(r'(?=\n\[State )',s)
 for i,b in enumerate(blocks):
  if re.search(r'(?im)^type\s*=\s*ChangeAnim\s*$',b):b=re.sub(r'(?m)^value\s*=\s*(.+)$',r'value=(\1)+10000*Var(42)',b).replace('Anim != IfElse(Vel X<0,21,20)','Anim != IfElse(Vel X<0,21,20)+10000*Var(42)').replace('Anim != 44','Anim != 44+10000*Var(42)')
  blocks[i]=b
 s=''.join(blocks);prone='!IsHelper && Var(42)=1 && (Anim%10000=170 || Anim%10000=5100 || Anim%10000=5110 || Anim%10000=5150)'
 extra=c(-2,'Rotate original armor for native knockdown','AngleDraw',prone,'value=90','ignorehitpause=1')+c(-2,'Align the horizontal armored body','Offset',prone,'x=44\ny=-20','ignorehitpause=1')
 p=CHAR/'DeepaKara.cns';p.write_text(p.read_text()+extra)
 (CHAR/'DeepaKara_common.cns').write_text(s)
 d=(ROOT/'JuraShinju/JuraShinju.def').read_text().replace('JuraShinju','DeepaKara').replace('Jura Shinju','Deepa Kara');d=re.sub(r'(?m)^author=.*$','author="VayDra original sprites and audio / Codex adaptation"',d);d=re.sub(r'(?m)^versiondate=.*$','versiondate=10,25,2026',d);(CHAR/'DeepaKara.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,form_offset=10000,awakening='Carbon armor, original Deepa sprites and a different moveset',activation_requires=3000,awakening_cost=1500,awakening_ticks=1200,incoming_damage_multiplier=.70,ultimate_cost=3000,own_life_cost=0,ultimate_damage='min(550,55% opponent maximum life) base; min(700,70%) armored',source_art_unchanged=True,original_voice_audio=True,ai_generated_art=False),indent=2)+'\n');print('Deepa runtime:',len(STATES),'states;',len(AIR),'animations')
if __name__=='__main__':main()
