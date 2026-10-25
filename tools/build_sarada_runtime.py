#!/usr/bin/env python3
"""Sarada TBV: original gameplay sequences, pink Susanoo and finite Ohirume."""
from pathlib import Path
import json,re
from hidari_susanoo_source import actions,frames
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'SaradaTBV';AIR=[];STATES=[];KEY={};SOUNDS={}
MOVES=[('Chidori','a','F',1000,350),('Katon','a','B',1010,400),('Raiton','b','F',1020,450),('Aoda','b','B',1030,600),('Ascendente','c','F',1040,350),('Asalto','c','B',1050,450),('Barrido','a','D',1400,200),('Punetazo','b','D',1410,300),('Descarga','c','D',1420,400),('Gokakyu','y','N',1200,200),('Orbe','z','N',1210,250),('Tormenta','y','D',1430,600),('Sharingan','z','D',1440,350)]
SUS={200:4200,210:4300,220:4400,600:4200,610:4300,620:4400,1000:4600,1010:4500,1020:4700,1030:4700,1040:4400,1050:4900,1400:4300,1410:4200,1420:4400,1200:4500,1210:4900,1430:4700,1440:4850,3000:4700}
def ctl(n,label,typ,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype={typ}\n{triggers}\n{params}\n{extra}\n'
def c(n,label,typ,when,params='',extra=''):return ctl(n,label,typ,'trigger1='+when,params,extra)
def state(n,anim=None,typ='S',move='I',physics='S',cost=0,ctrl=0,vel='0,0'):return f'\n[Statedef {n}]\ntype={typ}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'+(f'anim={anim}\n' if anim is not None else '')+(f'poweradd=-{cost}\n' if cost else '')+(f'velset={vel}\n' if vel else '')
def action(n,seq,form=0,box=None,active=None,loop=False,hurt=True,add=False):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+('-34,-175,34,0' if form else '-14,-80,14,0')+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(seq):
  if box and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+box+'\n'
  g,p=KEY[key];s+=f'{g},{p},0,0,{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def seq(stem,start,end,t=3):return [(f'Sarada2_{stem}_{i:02}',t) for i in range(start,end+1)]
def sus(n,source,box=None,hurt=True,loop=False):
 fs=frames(actions()[source]);seq2=[(f'Susanoo_{g}_{p}',max(1,t) if t>=0 else 8) for g,p,x,y,t,tail in fs if g>=0]
 action(n,seq2,1,box=box,loop=loop,hurt=hurt)
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Supplied Sarada audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def common_sound(n,when,number=21):return c(n,'Technique effect','PlaySnd',when,f'value=S1,{number}\nchannel=4\nvolumescale=75')
def startup(n,voice=None):return common_sound(n,'Time=0')+(sound(n,'Time=0',voice) if voice else '')+c(n,'Brief activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def end(n,t=52,dest=0):return c(n,'Return control','ChangeState',f'Time>={t}',f'value={dest}\nctrl=1')
def cast(n,when,ident,x='0',y='0',number=None):return c(n,'Finite physical technique','Helper',when,f'helpertype=Normal\nname="Sarada technique"\nID={ident}\nstateno={number or ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def effect(n,when,anim,x=0,y=-40,scale=1,ticks=-2):return c(n,'Original supplied effect','Explod',when,f'anim={anim}\npostype=P1\npos={x},{y}\nscale={scale},{scale}\nremovetime={ticks}\nbindtime=1\nsprpriority=4\nownpal=1\nremoveongethit=1')
def hit(n,t,damage,fin=False,low=False,air=False,ident=0,stun=22,projectile=False):return c(n,'Real attack collision','HitDef',f'Time={t}',f'''attr={'A' if air else 'C' if low else 'S'},{'SP' if projectile else 'HP' if n%10000==3000 or n==9800 else 'SA' if n%10000>=1000 else 'NA'}
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
 base={0:seq('Idle',1,3,10),5:seq('Idle',1,1,6),6:seq('KnockDown',5,5,6),10:seq('KnockDown',5,5,5),11:seq('KnockDown',5,5,6),12:seq('Idle',1,1,4),20:seq('Walk',1,6,4),21:list(reversed(seq('Walk',1,6,4))),100:seq('Walk',1,6,2),105:list(reversed(seq('Walk',1,6,2))),40:seq('Natk',7,7,5),41:seq('AirHurt',1,2,6),44:seq('KnockDown',1,1,8),52:seq('KnockDown',4,5,6)+seq('Idle',1,1,5),170:seq('KnockDown',3,3,30),180:seq('Natk',11,11,24)+seq('Idle',1,3,12),190:seq('Idle',1,3,12),500:seq('skill01',15,16,8),520:seq('skill05',1,21,3),5000:seq('Hurt',1,2,8),5010:seq('KnockDown',5,5,8),5020:seq('AirHurt',1,1,8),5030:seq('AirHurt',1,2,8),5100:seq('KnockDown',2,3,8),5110:seq('KnockDown',3,3,28),5120:seq('KnockDown',4,5,8)+seq('Idle',1,1,5),5150:seq('KnockDown',3,3,60),5200:seq('AirHurt',1,1,8),5210:seq('AirHurt',2,2,8),5300:seq('Hurt',1,1,20)}
 for n in [120,130,140,150]:base[n]=seq('Natk',11,11,5)
 for n in [121,131,141,151,122,132,142,152]:base[n]=seq('KnockDown',5,5,5)
 for n,poses in base.items():
  action(n,poses,loop=n in [0,11,20,21,100,105,41,44,500,5150])
  sus(n+10000,4055 if n in [20,100] else 4056 if n in [21,105] else 4050,loop=True)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{n}',3) for n in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,seq('skill02',1,3,3),hurt=False,add=True)
 action(8801,seq('skill01',22,30,3),hurt=False,box='-12,-12,12,12',loop=True)
 for j in [1,2,3]:action(8801+j,seq('skill01Ex'+str(j),22,30,3),hurt=False,box='-12,-12,12,12',loop=True)
 action(8810,[(f'SaradaEye_{i:02}',4) for i in [1,2,3]],hurt=False)
 action(8811,seq('skill05',22,31,3),hurt=False)
 action(8820,seq('skill05',32,43,3),hurt=False,box='-100,-130,100,100')
 action(8830,[(f'Susanoo_1350_{n}',2) for n in range(13,30)],hurt=False,box='-20,-80,70,0')
 sus(8831,4950,box='-25,-25,25,25',hurt=False)
 sus(8832,4750,box='-190,-110,190,65',hurt=False)
def normals():
 for form in [0,1]:
  off=form*10000
  for base,ranges in [(200,[(1,3),(4,6),(7,10)]),(210,[(7,10),(12,15),(20,23)]),(220,[(11,15),(16,19),(20,23)])]:
   for step,(a,b) in enumerate(ranges):
    n=base+step+off
    if form:sus(n,SUS[base],box='0,-85,100,0')
    else:action(n,seq('Natk',a,b,3),box='-3,-72,70,0',active=list(range(1,b-a+1)))
    s=state(n,n,move='A',vel='2,0')+sound(n,'Time=0','nAtk')+hit(n,3,[50,60,80][step] if form else [38,50,68][step],step==2,stun=12)
    s+=c(n,'Brake the approach','VelSet','Time>=8','x=0')+end(n,26 if form else max(20,(b-a+1)*3));STATES.append(s)
  for base in [600,610,620]:
   for step in range(3):
    n=base+step+off
    if form:sus(n,SUS[base],box='-10,-90,110,15')
    else:action(n,seq('Natk',7 if step==0 else 12 if step==1 else 20,10 if step==0 else 15 if step==1 else 23,3),box='-3,-75,75,0')
    s=state(n,n,'A','A','N',vel=None)+c(n,'Finite air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief juggle','VelSet','Time<7','x=2\ny=-.4')+c(n,'Real gravity','VelAdd','Time>=7','y=.48')+hit(n,3,[40,50,70][step] if form else [34,44,60][step],step==2,air=True,stun=14)
    s+=c(n,'Landing','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+end(n,20,50);STATES.append(s)
def base_specials():
 costs={n:cost for _,_,_,n,cost in MOVES}
 # Whole original composites remain on one caster: no miniature duplicate body.
 poses={1000:seq('skill02',4,16,2)+seq('skill02',17,22,3)+seq('skill02',23,23,8),1010:seq('skill01',1,14,3),1020:seq('skill01',15,21,4)+seq('skill01',31,40,3),1030:seq('skill03',1,15,4),1040:seq('Natk',20,23,4),1050:seq('Natk',12,23,3),1400:seq('Natk',7,10,4),1410:seq('Natk',1,6,4),1420:seq('skill02',4,16,3),1200:seq('skill01',1,14,2),1210:seq('skill01',15,16,10),1430:seq('skill01',15,21,4)+seq('skill01',31,40,3),1440:seq('Natk',11,11,12)+seq('Natk',16,23,4)}
 for _,_,_,n,cost in MOVES:
  box='-3,-72,78,0'
  if n in [1010,1200]:box='30,-68,230,5'
  if n==1030:box='-145,-160,90,3'
  if n==1050:box='-20,-90,100,0'
  if n==1420:box='-65,-90,65,0'
  action(n,poses[n],box=box,active=None)
  voice='chidori' if n==1000 else 'gokakyu' if n in [1010,1200] else 'Raiton' if n in [1020,1210,1420,1430] else 'sharingan' if n==1440 else 'shanaro'
  s=state(n,n,move='A',physics='N',cost=cost)+startup(n,voice)
  if n==1000:
   s+=sound(n,'Time=4','Chidori0',2)+c(n,'Real Chidori travel','VelSet','Time>=26 && Time<45 && !MoveContact','x=8.5')+c(n,'Brake actual contact','VelSet','MoveContact || Time>=45','x=0')+hit(n,26,185,True,stun=30)
  elif n in [1010,1200]:s+=hit(n,6,190 if n==1010 else 135,True,stun=26)+sound(n,'Time=6','Explo',2)
  elif n in [1020,1210,1430]:
   times=[20] if n==1210 else [16,26,36] if n==1020 else [16,24,32,40]
   for i,t in enumerate(times):s+=cast(n,f'Time={t}',9400+i,'28',str(-28-i%2*15),9400+i%4)
   s+=sound(n,'Time=12','Power',2)
  elif n==1030:s+=hit(n,12,90,False,stun=25)+hit(n,28,125,True,stun=30)+sound(n,'Time=12','Explo',2)
  elif n==1040:s+=c(n,'Rising strike','VelSet','Time=4','x=3\ny=-6')+c(n,'Rise is airborne','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Gravity after ascent','VelAdd','Time>4','y=.44')+hit(n,4,80,False,air=True)+hit(n,11,100,True,air=True)+c(n,'Land safely','ChangeState','Time>12 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
  elif n==1050:
   s+=c(n,'Finite taijutsu advance','VelSet','Time>=4 && Time<28','x=4')+c(n,'End advance','VelSet','Time>=28','x=0')
   for i,t in enumerate([4,15,26]):s+=hit(n,t,[45,55,85][i],i==2,stun=20)
  elif n==1400:s+=hit(n,4,105,True,low=True)+c(n,'Sweeping approach','VelSet','Time<14','x=4')
  elif n==1410:s+=hit(n,3,55,False)+hit(n,12,100,True)
  elif n==1420:s+=hit(n,10,155,True)+sound(n,'Time=6','Chidori0',2)
  elif n==1440:
   s+=effect(n,'Time=2',8810,0,-65,.35,12)+c(n,'Sharingan approach remains hittable','VelSet','Time>=12 && Time<30','x=6')+c(n,'Finish the approach','VelSet','Time>=30','x=0')+hit(n,14,165,True)
  s+=end(n,max(48,sum(t for _,t in poses[n])),50 if n==1040 else 0);STATES.append(s)
def awake_specials():
 for _,_,_,base,cost in MOVES:
  n=base+10000;source=SUS[base];sus(n,source,box='-10,-100,115,3')
  s=state(n,n,move='A',physics='N',cost=cost)+startup(n,'Skil5' if base in [1030,1430] else 'chidori' if base==1000 else None)
  if base==1030:s+=cast(n,'Time=20',9801,'IfElse(P2Dist X<210,P2Dist X,210)','-65')
  elif base==1430:
   for t in [18,38,58]:s+=cast(n,f'Time={t}',9473,'0','-45')
  elif base in [1010,1200]:s+=cast(n,'Time=20',9470,'45','-35')+sound(n,'Time=20','Explo',2)
  elif base in [1050,1210]:s+=cast(n,'Time=22',9471,'30','-90')+sound(n,'Time=22','Power',2)
  elif base in [1020,1420]:s+=cast(n,'Time=20',9472,'0','-45')+sound(n,'Time=20','Explo',2)
  elif base==1000:
   s+=c(n,'Susanoo fist advance','VelSet','Time>=16 && Time<36','x=4')+c(n,'Stop fist advance','VelSet','Time>=36','x=0')
   for i,t in enumerate([16,24,32]):s+=hit(n,t,[65,70,100][i],i==2,stun=20)
  else:s+=hit(n,8,175 if base==1440 else 150,True,low=base==1400,stun=26)
  s+=end(n,86 if base in [1030,1430] else 68);STATES.append(s)
def helpers():
 for i in range(4):
  n=9400+i;s=state(n,8801+i,'A','A','N',vel='10,0')+c(n,'No push','PlayerPush','1','value=0')+hit(n,0,115 if i==0 else 65,True,air=True,projectile=True)
  s+=c(n,'Original orb size','AngleDraw','1','scale=.55,.55')+c(n,'Finite projectile','DestroySelf','MoveContact || Time>=42 || RoundState!=2');STATES.append(s)
 for n,anim,damage,vel in [(9470,8830,210,'9,0'),(9471,8831,220,'12,0'),(9472,8832,195,'0,0'),(9473,8832,70,'0,0')]:
  s=state(n,anim,'A','A','N',vel=vel)+c(n,'No push','PlayerPush','1','value=0')
  if n in [9472,9473]:s+=c(n,'Full visible chakra ring','AngleDraw','1','scale=1.6,1.6')
  if n==9471:s+=c(n,'Arrow aims at the actual torso','VelSet','Time=0','y=(-30-Pos Y)/IfElse(P2Dist X>24,P2Dist X/12.0,2)')
  s+=hit(n,0,damage,True,air=True,projectile=n!=9472)+c(n,'Finite Susanoo attack','DestroySelf','MoveContact || Time>=42 || RoundState!=2');STATES.append(s)
 for n in [9800,9801]:
  s=state(n,8820,'A','A','N')+c(n,'No push','PlayerPush','1','value=0')+c(n,'Original three Ohirume vortices','AngleDraw','1','scale=.65,.65')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')
  s+=hit(n,6,0 if n==9800 else 200,True,air=True,ident=n,stun=42,projectile=True)
  if n==9800:
   s+=c(n,'Finite damage budget for a confirmed victim','VarSet','MoveHit && NumTarget(9800)>0 && Var(2)=0','v=0\nvalue=IfElse((Target(9800),LifeMax)>=1000,450,Floor((Target(9800),LifeMax)*.45))')
   s+=c(n,'Ohirume only draws in the struck enemy','TargetBind','MoveHit && NumTarget(9800)>0 && Time<22','ID=9800\ntime=1\npos=0,-10')
   s+=c(n,'Bounded Ohirume damage','TargetLifeAdd','Time>=22 && NumTarget(9800)>0 && Var(2)=0','ID=9800\nvalue=-Var(0)\nabsolute=1\nkill=1')+c(n,'Damage is applied once','VarSet','Time>=22 && NumTarget(9800)>0','v=2\nvalue=1')
  s+=c(n,'Ohirume expires and releases the enemy','DestroySelf','Time>=42 || RoundState!=2');STATES.append(s)
def utility():
 for n in [170,180,190]:
  s=state(n,n+10000*0)+c(n,'Round pose','Null','1')
  if n==190:s+=sound(n,'Time=0','Intro')+c(n,'Brief intro','AssertSpecial','Time<42','flag=Intro')+end(n,46)
  if n==180:s+=sound(n,'Time=0','UchihaSarada')
  STATES.append(s)
 s=state(500,500)+c(500,'Energy charge','PowerAdd','1','value=20')+cast(500,'Time=0 && NumHelper(9550)=0',9550)+sound(500,'Time=0','Power',3)
 s+=ctl(500,'Release energy charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1');STATES.append(s)
 s=state(9550,8900,'A','I','N')+c(9550,'Bind charge aura','BindToRoot','1','time=1\npos=0,-42')+c(9550,'Vertical aura','AngleDraw','1','value=90\nscale=.3,.35')+c(9550,'Pink energy','PalFX','1','time=1\ncolor=0\nmul=256,80,200')+c(9550,'Behind the fighter','SprPriority','1','value=-1')+ctl(9550,'Aura cleanup','DestroySelf','trigger1=Root,StateNo!=500\ntrigger2=RoundState!=2');STATES.append(s)
 s=state(520,520)+startup(520,'sharingan')+effect(520,'Time=8',8810,0,-70,.7,20)+c(520,'Original Mangekyou cut-in','Explod','Time=22','anim=8811\npostype=left\npos=160,75\nscale=.5,.5\nremovetime=30\nsprpriority=10\nownpal=1')
 s+=c(520,'Pay for the manifestation','PowerAdd','Time=55','value=-1500')+c(520,'Pink Susanoo mode','VarSet','Time=60','v=42\nvalue=1')+c(520,'Twenty second duration','VarSet','Time=60','v=40\nvalue=1200')+c(520,'Awakening cooldown','VarSet','Time=60','v=41\nvalue=1500')+sound(520,'Time=60','SharinganEye',2)+end(520,72);STATES.append(s)
def ultimate():
 action(3000,seq('skill04',1,25,3),box='-30,-95,110,0')
 s=state(3000,3000,move='A',physics='N',cost=3000)+startup(3000,'chidori')+sound(3000,'Time=0','Chidori0',2)
 s+=c(3000,'Ultimate physically advances','VelSet','Time>=15 && Time<30 && !MoveContact','x=7')+c(3000,'Stop the rush','VelSet','MoveContact || Time>=30','x=0')+hit(3000,15,0,True,ident=3000,stun=40)
 s+=c(3000,'Budget belongs to an actual hit','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,350,Floor((Target(3000),LifeMax)*.35))')+c(3000,'Bounded Chidori damage','TargetLifeAdd','MoveHit && NumTarget(3000)>0 && Var(21)=0','ID=3000\nvalue=-Var(20)\nabsolute=1\nkill=1')+c(3000,'Apply damage once','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(3000,'Reset the scene flag','VarSet','Time=0','v=21\nvalue=0')+sound(3000,'Time=42','Explo',2)+end(3000,82);STATES.append(s)
 sus(13000,4700)
 s=state(13000,13000,move='A',physics='N',cost=3000)+startup(13000,'Skil5')+c(13000,'Original Mangekyou eye','Explod','Time=3','anim=8811\npostype=left\npos=160,70\nscale=.5,.5\nremovetime=30\nsprpriority=10\nownpal=1')+cast(13000,'Time=30',9800,'IfElse(P2Dist X<210,P2Dist X,210)','-65')+sound(13000,'Time=30','KamuiKKS',2)+end(13000,90);STATES.append(s)
def commands():
 s='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\ns=s\n[Defaults]\ncommand.time=20\ncommand.buffer.time=3\n'
 def cmd(n,k,buf=3):return f'\n[Command]\nname="{n}"\ncommand={k}\ntime=20\nbuffer.time={buf}\n'
 for name,b,d,n,cost in MOVES:
  for keys in ([f'~D,D{d},{d},{b}',f'~D,{d},{b}'] if d in ['F','B'] else [f'/D,{b}'] if d=='D' else [b]):s+=cmd(name,keys,1 if d=='N' else 3)
 for b in ['a','b','c','x','y','z','s']:s+=cmd(b,b)+cmd('hold_'+b,'/'+b,1)
 for name,keys in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D'),('FF','F,F'),('BB','B,B'),('recovery','a+b')]:s+=cmd(name,keys,1 if keys.startswith('/') else 3)
 s+='\n[Statedef -1]\n'
 for name,b,d,n,cost in MOVES:
  extra='\ntriggerall=command!="holddown"' if d=='N' else ''
  s+=ctl(-1,name,'ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=Power>={cost}{extra}\ntrigger1=ctrl',f'value={n}+10000*Var(42)')
 s+=ctl(-1,'Pink Susanoo awakening','ChangeState','triggerall=AILevel=0\ntriggerall=command="s"\ntriggerall=command="holddown"\ntriggerall=Var(42)=0\ntriggerall=Var(41)=0\ntriggerall=Power>=3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=520')
 s+=ctl(-1,'Ultimate','ChangeState','triggerall=AILevel=0\ntriggerall=command="x"\ntriggerall=Power>=3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=3000+10000*Var(42)')+ctl(-1,'Charge','ChangeState','triggerall=AILevel=0\ntriggerall=command="hold_s"\ntriggerall=command!="holddown"\ntriggerall=Power<3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=500')
 for b,base in [('a',200),('b',210),('c',220)]:
  s+=ctl(-1,'Confirmed ground chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=command!="holddown"\ntriggerall=StateType!=A\ntrigger1=ctrl\ntrigger2=(StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220 || StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221) && Time>=6 && MoveHit',f'value={base}+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))','ignorehitpause=1')
  s+=ctl(-1,'Finite air chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=StateType=A\ntriggerall=Var(12)<3\ntrigger1=ctrl\ntrigger2=StateNo%10000>=600 && StateNo%10000<=621 && MoveHit && Time>=6',f'value={base+400}+10000*Var(42)+Var(12)','ignorehitpause=1')
 for name,n in [('FF',100),('BB',105)]:s+=ctl(-1,'Free double tap dash','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType=S\ntrigger1=ctrl',f'value={n}')
 for name,n in [('holdup',40),('holddown',11),('holdfwd',20),('holdback',20)]:
  extra='\ntriggerall=StateType=S\ntriggerall=command!="holdup"\ntriggerall=command!="holddown"' if n==20 else ''
  if n in [11,20]:extra+='\ntriggerall=StateNo<120 || StateNo>155'
  s+=ctl(-1,'Native movement','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=StateNo!={n}{extra}\ntrigger1=ctrl',f'value={n}\nctrl={int(n!=40)}')
 s+=ctl(-1,'CPU confirmed finite chain','ChangeState','triggerall=AILevel>0\ntriggerall=MoveHit\ntriggerall=Time>=6\ntrigger1=StateNo%10000=200 || StateNo%10000=201','value=StateNo+1')
 for n,cost,dist in [(3000,3000,120),(1000,350,180),(1010,400,210),(1020,450,240),(1030,600,160)]:s+=ctl(-1,'CPU legal attack','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=P2MoveType!=H\ntriggerall=Power>={cost}\ntrigger1=P2BodyDist X<{dist}\ntrigger1=Random<AILevel*3',f'value={n}+10000*Var(42)')
 s+=ctl(-1,'CPU close normal','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=P2MoveType!=H\ntrigger1=P2BodyDist X<55','value=200+10000*Var(42)')+ctl(-1,'CPU approach','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X>=55','value=20\nctrl=1')
 (CHAR/'SaradaTBV.cmd').write_text(s.rstrip()+'\n')
def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite awakening timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe mode expiry','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')
 s+=c(-2,'Refresh original body after expiry','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')+c(-2,'Full pink Susanoo replaces the human sprite','ChangeAnim','!IsHelper && Var(42)=1 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')
 s+=c(-2,'Reset finite air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge sound','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round visual cleanup','RemoveExplod','!IsHelper && RoundState!=2')
 s+=sound(-2,'!IsHelper && MoveType=H && Time=0 && StateNo=5000','Hurt',0,70)
 return s
def main():
 global KEY,SOUNDS
 KEY=json.loads((CHAR/'assets/keys.json').read_text());SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys']
 basics();normals();base_specials();awake_specials();helpers();utility();ultimate();commands()
 const=(ROOT/'JuraShinju/JuraShinju.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):].replace('life=1300','life=1150').replace('defence=115','defence=105').replace('height=84','height=80')
 (CHAR/'SaradaTBV.cns').write_text(('; Original Sarada by Vaydra, pink source Susanoo, actual collision.\n'+const+''.join(STATES)+system()).rstrip()+'\n')
 (CHAR/'SaradaTBV.air').write_text(('; Original supplied atlas frames and palette-converted Susanoo.\n'+''.join(AIR)).rstrip()+'\n')
 text=(ROOT/'JuraShinju/JuraShinju_common.cns').read_text();text=re.sub(r'(?m)^anim\s*=\s*(\d+)\s*$',r'anim=\1+10000*Var(42)',text)
 blocks=re.split(r'(?=\n\[State )',text)
 for i,b in enumerate(blocks):
  if re.search(r'(?im)^type\s*=\s*ChangeAnim\s*$',b):b=re.sub(r'(?m)^value\s*=\s*(.+)$',r'value=(\1)+10000*Var(42)',b).replace('Anim != IfElse(Vel X<0,21,20)','Anim != IfElse(Vel X<0,21,20)+10000*Var(42)').replace('Anim != 44','Anim != 44+10000*Var(42)')
  blocks[i]=b
 (CHAR/'SaradaTBV_common.cns').write_text(''.join(blocks))
 d=(ROOT/'JuraShinju/JuraShinju.def').read_text().replace('JuraShinju','SaradaTBV').replace('Jura Shinju','Sarada Uchiha TBV');d=re.sub(r'(?m)^author=.*$', 'author="Vaydra sprites / Vovan99 and Shingeki No Mugen Susanoo / Codex adaptation"',d);d=re.sub(r'(?m)^versiondate=.*$','versiondate=10,24,2026',d);(CHAR/'SaradaTBV.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,awakening='Pink Susanoo with Ohirume',awakening_cost=1500,activation_requires=3000,awakening_ticks=1200,form_offset=10000,ultimate_cost=3000,own_life_cost=0,ultimate_damage='min(350,35% target maximum life) base; min(450,45%) awakened',original_body_art=True,original_voice_audio=True,ai_generated_art=False),indent=2)+'\n')
 print('Sarada runtime:',len(STATES),'states,',len(AIR),'animations, original art and voices')
if __name__=='__main__':main()
