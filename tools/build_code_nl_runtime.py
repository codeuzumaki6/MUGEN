#!/usr/bin/env python3
"""Code: original claw marks, autonomous Grimes and Karma assault."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'CodeNoLimiter';AIR=[];STATES=[];KEY={};SOUNDS={}
MOVES=[('Grime','a','F',1000,350),('Emboscada','a','B',1010,400),('Karma','b','F',1020,450),('Superior','b','B',1030,600),('DobleMarca','c','F',1040,450),('Ascendente','c','B',1050,450),('Barrido','a','D',1400,200),('Patada','b','D',1410,300),('Remolino','c','D',1420,400),('Marca','y','N',1200,150),('Viaje','z','N',1210,250),('Cerco','y','D',1430,500),('Arbol','z','D',1440,550)]
def ctl(n,label,typ,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype={typ}\n{triggers}\n{params}\n{extra}\n'
def c(n,label,typ,when,params='',extra=''):return ctl(n,label,typ,'trigger1='+when,params,extra)
def state(n,anim=None,typ='S',move='I',physics='S',cost=0,ctrl=0,vel='0,0'):return f'\n[Statedef {n}]\ntype={typ}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'+(f'anim={anim}\n' if anim is not None else '')+(f'poweradd=-{cost}\n' if cost else '')+(f'velset={vel}\n' if vel else '')
def action(n,seq,form=0,box=None,active=None,loop=False,hurt=True,add=False,loop_start=None,offsets=None,hurt_box=None):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+(hurt_box or ('-15,-85,15,0'))+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(seq):
  if i==loop_start:s+='Loopstart\n'
  if box and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+box+'\n'
  if key.startswith('Kankuro_Skill05_') and int(key.rsplit('_',1)[-1])>=21 and hurt:s+='Clsn2: 1\n Clsn2[0]=-40,-170,40,5\n'
  g,p=KEY[key];x,y=(offsets or {}).get(key,(0,0));s+=f'{g},{p},{x},{y},{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def seq(stem,start,end,t=3):return [(f'{stem}_{i:02}',t) for i in range(start,end+1)]
def single(key,t=6):return [(key,t)]
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Original supplied Code audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def common_sound(n,when,number=21):return c(n,'Technique effect','PlaySnd',when,f'value=S1,{number}\nchannel=4\nvolumescale=75')
def startup(n,voice=None):return common_sound(n,'Time=0')+(sound(n,'Time=0',voice) if voice else '')+c(n,'Brief activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def end(n,t=52,dest=0):return c(n,'Return control','ChangeState',f'Time>={t}',f'value={dest}\nctrl=1')
def cast(n,when,ident,x='0',y='0',number=None):return c(n,'Finite physical technique','Helper',when,f'helpertype=Normal\nname="Code technique"\nID={ident}\nstateno={number or ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
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

def idle():return 'Kankuro_Idle_01'
def attack_action(n,p,form,box='-5,-84,100,3'):
 action(n,p+single(idle(),-1),form,box=box,active=list(range(len(p))))
def basics():
 for form in [0,1]:
  stand=single(idle(),10);crouch=single('Kankuro_KnockDown_05',8)
  poses={0:stand,5:stand,6:crouch,10:crouch,11:crouch,12:stand,20:seq('Kankuro_Walk',1,6,4),21:list(reversed(seq('Kankuro_Walk',1,6,4))),100:seq('Kankuro_Walk',1,6,2),105:list(reversed(seq('Kankuro_Walk',1,6,2))),40:single('Kankuro_NAttack_08',5),41:single('Kankuro_AirHurt_01',8),44:single('Kankuro_Float_01',8),52:crouch+stand,170:single('Kankuro_KnockDown_03',30),180:single('Kankuro_Skill01_01',10)+stand,190:seq('Kankuro_Skill01',1,3,10),500:seq('CodeNLAura',1,10,4),520:seq('CodeNLAura',1,10,4)+single('Kankuro_Skill01_01',8),5000:seq('Kankuro_Hurt',1,2,6),5010:single('Kankuro_Hurt_02',8),5020:single('Kankuro_AirHurt_01',8),5030:single('Kankuro_Float_01',8),5100:seq('Kankuro_KnockDown',1,3,8),5110:single('Kankuro_KnockDown_03',28),5120:seq('Kankuro_KnockDown',4,6,6)+stand,5150:single('Kankuro_KnockDown_03',60),5200:single('Kankuro_AirHurt_01',8),5210:single('Kankuro_Float_01',8),5300:single('Kankuro_Hurt_01',20)}
  for n in [120,130,140,150,121,131,141,151,122,132,142,152]:poses[n]=single('Kankuro_NAttack_01',6)
  for n,p in poses.items():action(n+10000*form,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-45,-28,47,0' if n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,seq('Tsumeato',1,4,5),hurt=False,loop=True)
 action(8801,seq('MokuShinju',1,7,5)+single('MokuShinju_07',12)+list(reversed(seq('MokuShinju',1,6,3))),hurt=False,box='-95,-120,95,5')
 action(8802,seq('Jiku',1,6,5),hurt=False)
 action(8803,seq('Troops',1,7,5),hurt=False,loop_start=4)
 action(8804,seq('TroopsAtk',0,11,4),hurt=False)
 action(8806,seq('CodeNLTILES',1,3,7),hurt=False,loop=True)
 action(9700,single('Grime_Idle_03',8),hurt_box='-18,-82,18,0',loop=True)
 action(9706,seq('Grime_Idle',1,3,5),hurt_box='-18,-82,18,0')
 action(9707,seq('Grime_Walk',1,6,4),hurt_box='-18,-82,18,0',loop=True)
 action(9701,seq('Grime_NAttack',1,5,4)+seq('Grime_Skill01',1,7,3)+single('Grime_Idle_03',6),box='-5,-75,85,4',hurt_box='-18,-82,18,0')
 action(9702,seq('PrimeTsumeaka',1,9,3)+seq('PrimeTsumeaka',10,21,3),box='-5,-100,110,5',hurt_box='-18,-82,18,0')
 action(9790,single('Grime_Idle_03',10),hurt_box='-18,-82,18,0')
def normals():
 for form in [0,1]:
  off=10000*form
  families={200:[seq('Kankuro_NAttack',1,4,3),seq('Kankuro_NAttack',5,7,3),seq('Kankuro_NAttack',8,14,2)],210:[seq('Kankuro_NAttack',4,7,3),seq('Kankuro_NAttack',8,11,3),seq('Kankuro_NAttack',12,14,3)],220:[seq('Kankuro_NAttack',8,10,3),seq('Kankuro_NAttack',11,13,3),seq('Kankuro_NAttack',12,14,3)]}
  for family,poses in families.items():
   for step,p in enumerate(poses):
    n=family+step+off;attack_action(n,p,form)
    STATES.append(state(n,n,move='A',vel='2,0')+common_sound(n,'Time=0',0)+sound(n,'Time=0','attack',0,65)+hit(n,3,[42,55,75][step],step==2,stun=13)+c(n,'Brake normal','VelSet','Time>=8','x=0')+end(n,24))
  for family in [600,610,620]:
   for step in range(3):
    n=family+step+off;p=seq('Kankuro_NAttack',8+step*2,min(10+step*2,14),4);attack_action(n,p,form)
    STATES.append(state(n,n,'A','A','N',vel=None)+c(n,'Finite air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Air strike','VelSet','Time<7','x=2\ny=-.4')+c(n,'Air gravity','VelAdd','Time>=7','y=.48')+hit(n,3,[36,48,66][step],step==2,air=True,stun=15)+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+end(n,20,50))
def mark(n,t=8):
 return cast(n,f'Time={t} && NumHelper(9600)=0',9600,'IfElse(P2Dist X<220,P2Dist X,220)','0')+effect(n,f'Time={t}',8800,0,0,1,25)+sound(n,f'Time={t}','claw',2)
def summon(n,t=10,heavy=False):
 s=cast(n,f'Time={t} && NumHelper(9700)<IfElse(Var(42),2,1)',9700,'30','0')
 if heavy:s+=c(n,'Command superior Claw Grime','VarSet',f'Time={t+2}','v=44\nvalue=9702')+c(n,'One new minion command','VarAdd',f'Time={t+2}','v=45\nvalue=1')
 return s

def specials():
 for form in [0,1]:
  for name,b,d,base,cost in MOVES:
   n=base+form*10000;p=seq('Kankuro_Skill01',2,3,8)+single('Kankuro_Skill01_01',12);box='-5,-85,105,4'
   if base in [1010,1210]:p=seq('Kankuro_Skill01',4,7,3)+seq('CodeNLTelep',1,8,2)+seq('Kankuro_Skill01',8,17,3);box='-5,-85,155,5'
   elif base==1020:p=seq('Kankuro_Skill04',1,9,4)+seq('Kankuro_Skill04',10,15,3);box='-5,-110,135,5'
   elif base==1040:p=seq('CodeNLTelep',1,8,2)+seq('Kankuro_Skill04',10,15,3)+seq('CodeNLTelep',1,8,2)+seq('Kankuro_Skill04',16,21,3);box='-5,-110,130,5'
   elif base==1050:p=seq('Kankuro_Skill04',16,25,4);box='-5,-110,115,4'
   elif base in [1400,1410]:p=seq('Kankuro_NAttack',8,14,3);box='-5,-45,100,3' if base==1400 else '-5,-85,105,4'
   elif base==1420:p=seq('Kankuro_Skill05',1,7,5);box='-55,-100,125,5'
   attack_action(n,p,form,box);s=state(n,n,move='I' if base==1200 else 'A',physics='N',cost=cost)+startup(n,'grime' if base in [1000,1430] else 'superior' if base==1030 else 'teleport' if base in [1010,1210] else 'rush')
   if base==1000:s+=mark(n,8)+summon(n,12)
   elif base in [1010,1210]:
    s+=mark(n,2)+c(n,'Travel to the actual placed claw mark','PosSet','Time=17 && NumHelper(9600)>0','x=(Helper(9600),Pos X)-30*Facing\ny=0')+c(n,'Face target after emerging','Turn','Time=18 && P2Dist X<0','')+hit(n,28,225 if form else 190,True)+sound(n,'Time=28','claw',2)
   elif base==1020:
    s+=mark(n,2)+c(n,'Approach through the real mark','PosSet','Time=6 && NumHelper(9600)>0','x=(Helper(9600),Pos X)-45*Facing\ny=0')
    for i,t in enumerate([10,24,40]):s+=hit(n,t,[65,70,105][i]+(15 if form else 0),i==2,stun=28)
   elif base==1030:s+=mark(n,6)+summon(n,10,True)
   elif base==1040:
    s+=mark(n,2)+c(n,'First claw ambush','PosSet','Time=14 && NumHelper(9600)>0','x=(Helper(9600),Pos X)-40*Facing\ny=0')+c(n,'Face first strike','Turn','Time=15 && P2Dist X<0','')+hit(n,19,95 if form else 80,stun=35)+c(n,'Emerge on the opposite side','PosSet','Time=49 && NumEnemy>0','x=(EnemyNear,Pos X)+38*Facing\ny=0')+c(n,'Turn for the second strike','Turn','Time=50 && P2Dist X<0','')+hit(n,56,150 if form else 125,True)
   elif base==1050:
    s+=c(n,'Ascending claw strike','VelSet','Time=4','x=5\ny=-7')+c(n,'Airborne ascent','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Gravity','VelAdd','Time>4','y=.44')+hit(n,6,95 if form else 75,air=True)+hit(n,17,135 if form else 110,True,air=True)+c(n,'Land ascent','ChangeState','Time>18 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
   elif base==1400:s+=c(n,'Low advancing kick','VelSet','Time<13','x=3.5')+c(n,'Brake kick','VelSet','Time>=13','x=0')+hit(n,4,140 if form else 115,True,low=True)
   elif base==1410:s+=hit(n,5,70 if form else 55,stun=27)+hit(n,15,115 if form else 95,True)
   elif base==1420:s+=hit(n,10,85 if form else 70,stun=28)+hit(n,25,120 if form else 100,True)
   elif base==1200:s+=mark(n,8)
   elif base==1430:
    s+=mark(n,4)+summon(n,8,True)
    if form:s+=summon(n,12,True)
   elif base==1440:s+=cast(n,'Time=12',9501,'IfElse(P2Dist X<220,P2Dist X,220)','0')+sound(n,'Time=12','superior')
   s+=end(n,max(48,sum(t for _,t in p)),50 if base==1050 else 0);STATES.append(s)

def minion_shared(n):
 s=c(n,'Finite Claw Grime age','VarAdd','1','v=5\nvalue=1','ignorehitpause=1')+c(n,'No minion push','PlayerPush','1','value=0')+c(n,'Claw Grime is hittable','HitOverride','1','slot=0\nattr=SCA,NA,SA,HA,NP,SP,HP,NT,ST,HT\nstateno=9790\ntime=1\nforceair=0','ignorehitpause=1')
 s+=c(n,'Defeat and seven second cleanup','DestroySelf','Var(2)=1 && (Life<=0 || Var(5)>=420 || (Root,Life)<=0 || RoundState!=2 || (Root,Var(48))!=Var(7))')
 s+=c(n,'Face opponent','Turn','P2Dist X<0','')+c(n,'Consume actual attack orders','ChangeState','Var(2)=1 && StateNo!=9790 && (Root,StateNo%10000)!=3000 && (Parent,Var(45))!=Var(1)','value=Parent,Var(44)\nctrl=0')
 if n not in [9700,9790]:s+=c(n,'Pause minion attacks during the ultimate','ChangeState','(Root,StateNo%10000)=3000','value=9700\nctrl=0')
 return s

def helpers():
 STATES.append(state(9600,8800,'S','I','N')+c(9600,'Ground claw mark','PlayerPush','1','value=0')+c(9600,'No mark shadow','AssertSpecial','1','flag=NoShadow')+c(9600,'Eight second mark lifetime','DestroySelf','Time>=480 || RoundState!=2 || (Root,Life)<=0 || (Root,Var(48))!=Var(7)')+c(9600,'Mark generation','VarSet','Time=0','v=7\nvalue=Root,Var(48)'))
 STATES.append(state(9501,8801,'S','A','N')+c(9501,'No tree push','PlayerPush','1','value=0')+c(9501,'Tree scale','AngleDraw','1','scale=.55,.55')+c(9501,'Snapshot Karma','VarSet','Time=0','v=0\nvalue=Root,Var(42)')+hit(9501,16,'IfElse(Var(0),100,80)',stun=29,projectile=True)+hit(9501,33,'IfElse(Var(0),150,120)',True,projectile=True)+c(9501,'Finite tree trap','DestroySelf','Time>=75 || RoundState!=2'))
 for n in [9700,9701,9702,9790]:
  s=state(n,n,'S','H' if n==9790 else 'I' if n==9700 else 'A','N')
  if n==9700:s+=c(n,'Original first emergence only','ChangeAnim','Time=0 && Var(2)=0','value=9706')+c(n,'Original Claw Grime health','LifeSet','Time=0 && Var(2)=0','value=180')+c(n,'Minion generation','VarSet','Time=0 && Var(2)=0','v=7\nvalue=Root,Var(48)')+c(n,'Initial command','VarSet','Time=0 && Var(2)=0','v=1\nvalue=Parent,Var(45)')+c(n,'Initialized once','VarSet','Time=0','v=2\nvalue=1')
  else:s+=c(n,'Read commanded attack','VarSet','Time=0 && (Parent,Var(45))!=Var(1)','v=1\nvalue=Parent,Var(45)')
  s+=c(n,'Snapshot minion power','VarSet','Time=0','v=3\nvalue=Root,Var(42)')+minion_shared(n)
  if n==9700:
   s+=c(n,'Follow target while Code fights','VelSet','(Root,StateNo%10000)!=3000','x=IfElse(Abs(P2Dist X)>65,3.5,0)')+c(n,'Wait during the ultimate','VelSet','(Root,StateNo%10000)=3000','x=0\ny=0')+c(n,'Walking original Grime','ChangeAnim','Time>=15 && Abs(P2Dist X)>65 && Anim!=9707','value=9707')+c(n,'Standing original Grime','ChangeAnim','Time>=15 && Abs(P2Dist X)<=65 && Anim!=9700','value=9700')+c(n,'Autonomous claw attack','ChangeState','Time>=38 && Abs(P2Dist X)<85 && (Root,StateNo%10000)!=3000','value=9701')
  elif n==9790:s+=c(n,'Visible hit response','PalFX','1','time=1\nadd=70,-30,-30')+end(n,10,9700)
  elif n==9701:s+=hit(n,5,'IfElse(Var(3),45,35)',stun=28)+hit(n,24,'IfElse(Var(3),45,35)',True)+sound(n,'Time=5','claw',2)+sound(n,'Time=24','claw',2)+end(n,50,9700)
  else:
   s+=c(n,'Superior emergence near target','PosSet','Time=0 && Abs(P2Dist X)<300','x=(EnemyNear,Pos X)-48*Facing\ny=0')+hit(n,12,'IfElse(Var(3),100,75)',stun=30)+hit(n,34,'IfElse(Var(3),160,120)',True)+effect(n,'Time=35',8801,60,0,.45,65)+sound(n,'Time=34','claw',2)+end(n,66,9700)
  STATES.append(s)

def utility():
 for n in [170,180,190]:
  s=state(n,n)+sound(n,'Time=0','die' if n==170 else 'win' if n==180 else 'intro')
  if n==190:s+=c(n,'Brief intro','AssertSpecial','Time<40','flag=Intro')+end(n,44)
  STATES.append(s)
 STATES.append(state(500,500)+c(500,'Original purple Karma charging pose','PowerAdd','1','value=20')+common_sound(500,'Time=0',30)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 STATES.append(state(9551,8900,'A','I','N')+c(9551,'Karma follows the single real body','BindToRoot','1','time=1\npos=0,-42')+c(9551,'Purple energy','PalFX','1','time=1\ncolor=0\nmul=190,70,256')+c(9551,'Vertical energy','AngleDraw','1','value=90\nscale=.28,.32')+c(9551,'Behind Code','SprPriority','1','value=-2')+c(9551,'Faint moving aura','Trans','1','trans=AddAlpha\nalpha=90,256')+c(9551,'Finite awakening aura','DestroySelf','(Root,Var(42))=0 || RoundState!=2'))
 STATES.append(state(520,520)+startup(520,'karma')+c(520,'Pay Karma awakening','PowerAdd','Time=24','value=-1500')+c(520,'Awaken Karma','VarSet','Time=24','v=42\nvalue=1')+c(520,'Twenty second awakening','VarSet','Time=24','v=40\nvalue=1200')+c(520,'Awakening cooldown','VarSet','Time=24','v=41\nvalue=1500')+end(520,48))

def ultimate():
 pose=single('Kankuro_Skill05_01',6)+seq('Kankuro_Skill05',2,7,3)+seq('CodeNLAura',1,10,4)*2+seq('Kankuro_Skill05',8,10,4)+seq('Kankuro_Skill05',11,20,4)*2+seq('EndChg',1,4,5)+seq('Kankuro_Skill05',21,40,4)
 for form in [0,1]:
  n=3000+form*10000;attack_action(n,pose,form,'5,-105,240,5');s=state(n,n,move='A',physics='N',cost=3000)+startup(n,'ultimate')+c(n,'Reset actual ultimate contact','VarSet','Time=0','v=21\nvalue=0')+hit(n,18,0,ident=3000,stun=340)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Record actual struck enemy','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite Karma damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{800 if form else 650},Floor((Target(3000),LifeMax)*{.8 if form else .65}))')+c(n,'Confirm real capture','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')
  s+=c(n,'Hold only a confirmed opponent','TargetBind','NumTarget(3000)>0 && Time<310','ID=3000\ntime=1\npos=(FVar(0)-Pos X)*Facing,0')
  s+=c(n,'Original dimensional background','Explod','Time=24 && NumTarget(3000)>0','anim=8806\npostype=left\npos=160,120\nscale=.45,.75\nbindtime=-1\nremovetime=288\nsprpriority=-9\nownpal=1\nremoveongethit=1')
  s+=effect(n,'Time=28 && NumTarget(3000)>0',8803,'(FVar(0)-Pos X)*Facing/2',0,.48,280).replace('sprpriority=4','sprpriority=-3')
  for t in [65,95,125]:s+=effect(n,f'Time={t} && NumTarget(3000)>0',8804,'(FVar(0)-Pos X)*Facing',0,.65,48)
  s+=c(n,'No push during the confirmed cinematic','PlayerPush','1','value=0')+c(n,'The complete original column contains Code as its only main body','PosSet','Time=216 && NumTarget(3000)>0','x=FVar(0)\ny=0')+c(n,'Scale the original body and column together','AngleDraw','Time>=216 && Time<296','scale='+('.6,.6' if form else '.48,.48'))+c(n,'Return beside the actual target after the column','PosSet','Time=296 && NumTarget(3000)>0','x=FVar(0)-55*Facing\ny=0')+sound(n,'Time=216 && NumTarget(3000)>0','ultimate_end')
  for i,t in enumerate([68,98,128,158,188,228,258,288]):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)'
   s+=c(n,'Confirmed finite Karma impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count real cinematic impacts','HitAdd',when,'value=1')+effect(n,when,8700,'(FVar(0)-Pos X)*Facing',-35,.7,9)+sound(n,when,'claw',2)
  s+=c(n,'Always release the confirmed victim','TargetState','Time=310 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,330);STATES.append(s)
 STATES.append(state(3010,None,'S','H','N')+c(3010,'Rival keeps its own hurt artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Independent interruption and release failsafe','SelfState','trigger1=Time>=360\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3011,None,'A','H','N')+c(3011,'Release into a real fall','VelSet','Time=0','x=-4\ny=-6')+c(3011,'Restore rival state ownership','SelfState','1','value=5050\nctrl=0'))

def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite awakening timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Expire safely after an attack or hit','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Restore base animation bank','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')+c(-2,'Awakened animation bank','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+cast(-2,'!IsHelper && Var(42)=1 && NumHelper(9551)=0 && RoundState=2',9551)+c(-2,'Awakened physical attacks','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.2,1)')+c(-2,'Reset grounded air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Round awakening cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round visual cleanup','RemoveExplod','!IsHelper && RoundState!=2')
 return s

def main():
 global KEY,SOUNDS
 KEY=json.loads((CHAR/'assets/keys.json').read_text());SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];basics();normals();specials();helpers();utility();ultimate()
 import build_sarada_runtime as ref
 saved=ref.CHAR,ref.MOVES
 try:ref.CHAR=CHAR;ref.MOVES=MOVES;ref.commands()
 finally:ref.CHAR,ref.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';(CHAR/'CodeNoLimiter.cmd').write_text(p.read_text().replace('Pink Susanoo awakening','Code Karma awakening'));p.unlink()
 const=(ROOT/'JigenKara/JigenKara.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):].replace('height=86','height=85')
 (CHAR/'CodeNoLimiter.cns').write_text('; Original Code No Limiter bodies, actual claw marks and hittable Claw Grimes.\n'+const+(''.join(STATES)+system()).rstrip()+'\n');(CHAR/'CodeNoLimiter.air').write_text('; Complete original bodies and separate props.\n'+''.join(AIR).rstrip()+'\n')
 (CHAR/'CodeNoLimiter_common.cns').write_text((ROOT/'JigenKara/JigenKara_common.cns').read_text())
 d=(ROOT/'JigenKara/JigenKara.def').read_text().replace('JigenKara','CodeNoLimiter').replace('"Jigen"','"Code No Limiter"');d=re.sub(r'(?m)^author=.*$','author="Vaydra original sprites / MUGEN STARS Code audio / Codex adaptation"',d);(CHAR/'CodeNoLimiter.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,base='White hair Code without limiters',awakening='Stronger Karma, original purple aura, two Claw Grimes',awakening_ticks=1200,requires=3000,cost=1500,ultimate_cost=3000,own_life_cost=0,ultimate_damage=[650,800],minion_health=180,minion_ticks=420,minion_cap=[1,2],mark_ticks=480),indent=2)+'\n');print('Code runtime:',len(STATES),'states;',len(AIR),'animations')
if __name__=='__main__':main()
