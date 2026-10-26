#!/usr/bin/env python3
"""Jigen: original taijutsu, rods, cubes, Karma absorption and Ten Tails."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'JigenKara';AIR=[];STATES=[];KEY={};SOUNDS={};BODY_FRAMES={}
MOVES=[('Rafaga','a','F',1000,350),('Estacas','a','B',1010,400),('Embestida','b','F',1020,450),('CorteCubo','b','B',1030,600),('Rodilla','c','F',1040,350),('Patada','c','B',1050,450),('Barrido','a','D',1400,200),('Pesado','b','D',1410,300),('Sukunahikona','c','D',1420,400),('Absorcion','y','N',1200,200),('Varillas','z','N',1210,250),('Daikokuten','y','D',1430,500),('Sellado','z','D',1440,350)]
def ctl(n,label,typ,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype={typ}\n{triggers}\n{params}\n{extra}\n'
def c(n,label,typ,when,params='',extra=''):return ctl(n,label,typ,'trigger1='+when,params,extra)
def state(n,anim=None,typ='S',move='I',physics='S',cost=0,ctrl=0,vel='0,0'):return f'\n[Statedef {n}]\ntype={typ}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'+(f'anim={anim}\n' if anim is not None else '')+(f'poweradd=-{cost}\n' if cost else '')+(f'velset={vel}\n' if vel else '')
def action(n,seq,form=0,box=None,active=None,loop=False,hurt=True,add=False,loop_start=None,offsets=None,hurt_box=None):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+(hurt_box or ('-15,-86,15,0' if form else '-15,-86,15,0'))+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(seq):
  if i==loop_start:s+='Loopstart\n'
  if box and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+box+'\n'
  key='Jiraiya_Skill05_Trans_04' if form and key.startswith('Jiraiya_Idle_') else key
  if hurt:BODY_FRAMES.setdefault(key,[]).append((n,i+1))
  g,p=KEY[key];x,y=(offsets or {}).get(key,(0,0));s+=f'{g},{p},{x},{y},{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def seq(stem,start,end,t=3):return [(f'{stem}_{i:02}',t) for i in range(start,end+1)]
def single(key,t=6):return [(key,t)]
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Original Jigen audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def common_sound(n,when,number=21):return c(n,'Technique effect','PlaySnd',when,f'value=S1,{number}\nchannel=4\nvolumescale=75')
def startup(n,voice=None):return common_sound(n,'Time=0')+(sound(n,'Time=0',voice) if voice else '')+c(n,'Brief activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def end(n,t=52,dest=0):return c(n,'Return control','ChangeState',f'Time>={t}',f'value={dest}\nctrl=1')
def cast(n,when,ident,x='0',y='0',number=None):return c(n,'Finite physical technique','Helper',when,f'helpertype=Normal\nname="Jigen technique"\nID={ident}\nstateno={number or ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
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

def idle(form=0):return 'Jiraiya_Idle_01'
def attack_action(n,p,form,box='-5,-83,90,3'):
 action(n,p+single(idle(),-1),form,box=box,active=list(range(len(p))))

def basics():
 for form in [0,1]:
  poses={0:seq('Jiraiya_Idle',1,4,10),5:single(idle()),6:single('Jiraiya_wake_01'),10:single('Jiraiya_wake_01'),11:single('Jiraiya_wake_01'),12:single(idle()),20:seq('Jiraiya_Walk',1,6,4),21:list(reversed(seq('Jiraiya_Walk',1,6,4))),100:seq('Jiraiya_Walk',1,6,2),105:list(reversed(seq('Jiraiya_Walk',1,6,2))),40:single('Jiraiya_NAttack_08',5),41:single('Jiraiya_Float_01',8),44:single('Jiraiya_AirHurt_01',8),52:single('Jiraiya_wake_01',8)+single(idle(),5),170:single('Jiraiya_KnockDown_02',30),180:seq('Jiraiya_Idle',1,4,12),190:seq('Jiraiya_Idle',1,4,8),500:seq('Jiraiya_Skill03_Chg',1,3,8),520:seq('Jiraiya_Skill05_Trans',1,4,6)+single('Jiraiya_Skill05_01',20),5000:seq('Jiraiya_Hurt',1,2,6),5010:single('Jiraiya_wake_01',8),5020:single('Jiraiya_AirHurt_01',8),5030:single('Jiraiya_Float_01',8),5100:seq('Jiraiya_KnockDown',1,2,8),5110:single('Jiraiya_KnockDown_02',28),5120:single('Jiraiya_wake_01',12)+single(idle(),8),5150:single('Jiraiya_KnockDown_02',60),5200:single('Jiraiya_AirHurt_01',8),5210:single('Jiraiya_Float_01',8),5300:single('Jiraiya_Hurt_01',20)}
  for n in [120,130,140,150,121,131,141,151,122,132,142,152]:poses[n]=single('Jiraiya_Skill01_01',5)
  for n,p in poses.items():action(n+10000*form,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-45,-28,47,0' if n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,single('BesiJigen_01',4),hurt=False,loop=True,box='-27,-42,27,42')
 action(8801,single('BesiJigen_01',4),hurt=False,loop=True,box='-14,-21,14,21')
 action(8802,seq('Jiraiya_Skill02Iron02',1,6,6),hurt=False,box='-95,-150,95,5')
 for n in [8814,8815]:action(n,seq('KubusAppear',1,4,2)+seq('KubusIdle',1,3,4),hurt=False,box='-85,-145,85,5' if n==8815 else '-60,-110,60,5')
 action(8816,seq('KubusBom',1,6,4),hurt=False)
 action(8820,seq('JigenCup_Smn',1,2,6)+single('JigenCup_Idle_01',-1),hurt=False,box='-55,-130,55,5')
 action(8821,seq('JigenCup_Cls',1,3,5)+single('JigenCup_IdleCls_01',-1),hurt=False)
 action(8822,seq('JigenCup_Atk',1,5,5)+seq('JigenCup_out',1,2,5),hurt=False)
 action(8830,single('Common_8700_0',4),loop=True,hurt_box='-15,-86,15,0')
 action(8840,seq('Asap_Ngubek',1,13,3),hurt=False)
 blast=seq('Blast_Jiraiya_Ulti_Boom',1,6,5)+seq('Blast_Jiraiya_Ulti_Boom',3,6,5)*3+seq('Blast_Jiraiya_Ulti_Boom',7,10,5)
 action(8850,blast,hurt=False)
 action(8990,single('Horn_layer',-1),hurt=False)

def normals():
 for form in [0,1]:
  off=10000*form
  for family in [200,210,220]:
   for step in range(3):
    n=family+step+off;start=1+step*3 if family==200 else 4+step*2 if family==210 else 8+step
    p=seq('Jiraiya_NAttack',start,min(start+2,12),3);attack_action(n,p,form)
    STATES.append(state(n,n,move='A',vel='2,0')+common_sound(n,'Time=0',0)+hit(n,3,[42,55,75][step],step==2,stun=13)+c(n,'Brake normal','VelSet','Time>=8','x=0')+end(n,24))
  for family in [600,610,620]:
   for step in range(3):
    n=family+step+off;p=seq('Jiraiya_NAttack',8+step,min(10+step,12),4);attack_action(n,p,form,'-5,-85,90,3')
    STATES.append(state(n,n,'A','A','N',vel=None)+c(n,'Finite air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief air strike','VelSet','Time<7','x=2\ny=-.4')+c(n,'Gravity','VelAdd','Time>=7','y=.48')+hit(n,3,[36,48,66][step],step==2,air=True,stun=15)+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+end(n,20,50))

def specials():
 for form in [0,1]:
  off=form*10000
  for name,b,d,base,cost in MOVES:
   n=base+off;p=single('Jiraiya_Skill01_01',24);box='-5,-85,100,3'
   if base==1010:p=seq('Jiraiya_Skill02',1,2,12)
   elif base==1020:p=seq('Jiraiya_Skill03_Chg',1,3,3)+single('Jiraiya_Skill03_Move_01',4)+seq('Jiraiya_Skill03_cross',1,5,4);box='-5,-85,130,4'
   elif base==1030:p=seq('Jiraiya_Skill03_Chg2',1,2,4)+seq('Jiraiya_Skill03_slash',1,5,4)+seq('Jiraiya_Skill03_Cube',1,2,6);box='-5,-90,125,4'
   elif base==1040:p=seq('Jiraiya_Skill4_lutut_Chg',1,2,4)+seq('Jiraiya_Skill4_lutut',1,5,5);box='-5,-110,110,4'
   elif base==1050:p=seq('Jiraiya_Skill4_Kick_Chg',1,3,3)+seq('Jiraiya_Skill4_Kick',1,6,5);box='-5,-95,125,4'
   elif base==1400:p=seq('Jiraiya_NAttack',9,12,4);box='-5,-45,95,3'
   elif base==1410:p=seq('Jiraiya_NAttack',1,6,4)
   elif base==1420:p=single(idle(),18)+seq('Jiraiya_NAttack',4,6,5)
   elif base==1430:p=seq('Jiraiya_Skill03_Cube',1,2,8)
   elif base==1440:p=seq('Jiraiya_CupMove',1,2,12)
   attack_action(n,p,form,box)
   if base==1420:
    g,k=KEY[idle()];needle=f'{g},{k},0,0,18';AIR[-1]=AIR[-1].replace(needle,'Clsn2: 1\n Clsn2[0]=-9,-47,9,0\n'+needle,1)
   s=state(n,n,move='I' if base==1200 else 'A',physics='N',cost=cost)+startup(n,'Jigen/jigen0' if base in [1000,1200,1210] else 'Jigen/jigen1' if base==1010 else 'Jigen/jigen2' if base==1020 else 'Jigen/Jigen4')
   if base==1000:
    for t in ([8,14,20,26,32] if form else [8,16,24]):s+=cast(n,f'Time={t}',9500,'32','-43')+sound(n,f'Time={t}','Effect/besi5',2)
   elif base==1010:s+=cast(n,'Time=10',9501,'IfElse(P2Dist X<200,P2Dist X,200)','0')+sound(n,'Time=10','Effect/Kokugan',2)
   elif base==1020:s+=c(n,'Actual forward rush','VelSet','Time>=9 && Time<29 && !MoveContact','x=8.5')+c(n,'Brake contact','VelSet','MoveContact || Time>=29','x=0')+hit(n,12,190 if form else 165,True)+sound(n,'Time=9','Effect/Blade-Damage',2)
   elif base==1030:s+=hit(n,11,110 if form else 85,stun=28)+cast(n,'Time=29',9503,'IfElse(P2Dist X<210,P2Dist X,210)','-190')+sound(n,'Time=29','Effect/kubus jatuh',2)
   elif base==1040:s+=c(n,'Knee rise','VelSet','Time=6','x=3\ny=-6.5')+c(n,'Airborne knee','StateTypeSet','Time=6','statetype=A\nphysics=N')+c(n,'Knee gravity','VelAdd','Time>6','y=.44')+hit(n,7,80 if form else 65,air=True)+hit(n,19,120 if form else 100,True,air=True)+c(n,'Land knee','ChangeState','Time>18 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
   elif base==1050:s+=c(n,'Closing kick step','VelSet','Time<16 && !MoveContact','x=4')+c(n,'Stop kick','VelSet','MoveContact || Time>=16','x=0')+hit(n,10,70 if form else 55,stun=28)+hit(n,24,130 if form else 110,True)+sound(n,'Time=10','Effect/rock_hit2',2)
   elif base==1400:s+=c(n,'Sweeping step','VelSet','Time<14','x=3.5')+c(n,'Brake sweep','VelSet','Time>=14','x=0')+hit(n,4,130 if form else 105,True,low=True)
   elif base==1410:s+=hit(n,4,65 if form else 50,stun=25)+hit(n,15,115 if form else 95,True)
   elif base==1420:s+=c(n,'Temporary real shrink','AngleDraw','Time<18','scale=.55,.55')+c(n,'Shrunken advance','VelSet','Time<16','x=6')+c(n,'Stop shrunken advance','VelSet','Time>=16','x=0')+c(n,'Face the actual target after shrinking','Turn','Time=18 && P2Dist X<0','')+effect(n,'Time=18',8840,0,0,.35,20)+hit(n,20,185 if form else 155,True)+sound(n,'Time=0','Effect/sukonaMini',2)
   elif base==1200:
    s+=c(n,'Reset absorption confirmation','VarSet','Time=0','v=46\nvalue=0')+c(n,'Only projectile protection during absorption','HitBy','Time>=8 && Time<=36','value=SCA,NA,SA,HA,NT,ST,HT\ntime=1')+cast(n,'Time=8',9110,'22','0')+c(n,'Real projectile absorption confirmed','ChangeState','Var(46)>0',f'value={1201+off}')
   elif base==1210:s+=cast(n,'Time=8',9502,'35','-28')+sound(n,'Time=8','Effect/besi5',2)
   elif base==1430:s+=cast(n,'Time=12',9503,'IfElse(P2Dist X<230,P2Dist X,230)','-190')+sound(n,'Time=12','Effect/kubus jatuh',2)
   elif base==1440:s+=cast(n,'Time=12 && NumHelper(9504)=0',9504,'IfElse(P2Dist X<190,P2Dist X,190)','0')+sound(n,'Time=12','Effect/throw',2)
   s+=end(n,max(48,sum(t for _,t in p)),50 if base==1040 else 0);STATES.append(s)
  n=1201+off;attack_action(n,single('Jiraiya_Skill01_01',20),form)
  STATES.append(state(n,n)+c(n,'Finish absorbing projectile tail','HitBy','Time<=7','value=SCA,NA,SA,HA,NT,ST,HT\ntime=1')+c(n,'Recover chakra from a real projectile','PowerAdd','Time=0','value=220')+sound(n,'Time=0','Effect/absorb efx',2)+effect(n,'Time=0',8840,25,-45,.22,20)+end(n,22))

def projectiles():
 for n in [9500,9502]:
  s=state(n,8800 if n==9500 else 8801,'A','A','N',vel='12,0')+c(n,'No projectile push','PlayerPush','1','value=0')+c(n,'No rod shadow','AssertSpecial','1','flag=NoShadow')
  if n==9502:s+=c(n,'Compact flying rod fan','AngleDraw','1','scale=.5,.5')
  s+=c(n,'Snapshot rod power','VarSet','Time=0','v=0\nvalue='+('IfElse((Root,Var(42)),80,65)' if n==9500 else 'IfElse((Root,Var(42)),145,110)'))+hit(n,0,'Var(0)',n==9502,air=True,projectile=True,stun=18)+c(n,'Rod resolves on real contact','DestroySelf','MoveContact || Time>=45 || RoundState!=2');STATES.append(s)
 s=state(9501,8802,'S','A','N')+c(9501,'No ground trap push','PlayerPush','1','value=0')+c(9501,'Snapshot ground trap power','VarSet','Time=0','v=0\nvalue=Root,Var(42)')+hit(9501,8,'IfElse(Var(0),85,70)',stun=26,projectile=True)+hit(9501,22,'IfElse(Var(0),140,110)',True,projectile=True)+sound(9501,'Time=8','Effect/BesiIn',2)+c(9501,'Ground rods expire','DestroySelf','Time>=39 || RoundState!=2');STATES.append(s)
 s=state(9503,8814,'A','A','N',vel='0,9')+c(9503,'Read cube mode','VarSet','Time=0','v=0\nvalue=Root,Var(42)')+c(9503,'Actual cube collision size','ChangeAnim','Time=0','value=8814+Var(0)')+c(9503,'Original cube size','AngleDraw','1','scale=.8+.3*Var(0),.8+.3*Var(0)')+c(9503,'No cube push','PlayerPush','1','value=0')+hit(9503,0,'IfElse(Var(0),300,220)',True,air=True,projectile=True)+c(9503,'Cube lands or strikes','ChangeState','MoveContact || Pos Y>=0','value=9513')+c(9503,'Finite falling cube','DestroySelf','Time>=50 || RoundState!=2');STATES.append(s)
 STATES.append(state(9513,8816,'S','I','N')+c(9513,'Impact stays on ground','PosSet','Time=0','y=0')+c(9513,'Impact has no extra damage','VelSet','1','x=0\ny=0')+sound(9513,'Time=0','Effect/kubus2',2)+c(9513,'Cube impact ends','DestroySelf','AnimTime=0 || Time>=26 || RoundState!=2'))

def absorption():
 for n in [9110,9111]:
  s=state(n,8830,'S','I','N')+c(n,'Field follows the Karma palm','BindToRoot','1','time=1\npos=22,0')+c(n,'No field push','PlayerPush','1','value=0')+c(n,'Only projectile attributes enter the field','HitBy','1','value=SCA,NP,SP,HP\ntime=1')+c(n,'Absorption field resistance','DefenceMulSet','1','value=0')+c(n,'Invisible collision field','AssertSpecial','1','flag=Invisible\nflag2=NoShadow')
  s+=effect(n,'Time%8=0',8840,0,-45,.20,12)
  if n==9110:s+=c(n,'Physical absorption of helper and classic projectiles','HitOverride','1','attr=SCA,NP,SP,HP\nstateno=9111\ntime=1\nforceair=0')
  else:s+=c(n,'Signal real projectile contact','ParentVarSet','Time=0','v=46\nvalue=1')+c(n,'Successful field retires','DestroySelf','Time=0')
  s+=c(n,'Finite field and interruption cleanup','DestroySelf','Time>=30 || (Root,StateNo%10000)!=1200 || RoundState!=2');STATES.append(s)

def seal():
 n=9504;s=state(n,8820,'S','A','N')+c(n,'No seal push','PlayerPush','1','value=0')+c(n,'Original black bowl scale','AngleDraw','1','scale=.38,.38')+hit(n,8,0,False,ident=9504,projectile=True,stun=100)+'p2stateno=3020\np2getp1state=1\n'
 s+=c(n,'Record actual sealed enemy','VarSet','MoveHit && NumTarget(9504)>0 && Var(2)=0','fv=0\nvalue=Target(9504),Pos X')+c(n,'Finite seal damage','VarSet','MoveHit && NumTarget(9504)>0 && Var(2)=0','v=0\nvalue=IfElse((Root,Var(42)),280,210)')+c(n,'Confirm real seal collision','VarSet','MoveHit && NumTarget(9504)>0','v=2\nvalue=1')+c(n,'Close only after a hit','ChangeAnim','Var(2)=1 && Anim=8820','value=8821')
 s+=c(n,'Hold the captured enemy inside the bowl','TargetBind','NumTarget(9504)>0 && Time<72','ID=9504\ntime=1\npos=(FVar(0)-Pos X)*Facing,-20')
 for i,t in enumerate([30,48,66]):
  amount='Var(0)-Floor(Var(0)/3)*2' if i==2 else 'Floor(Var(0)/3)';when=f'Time={t} && NumTarget(9504)>0 && (Root,MoveType!=H)'
  s+=c(n,'Bounded seal impact','TargetLifeAdd',when,'ID=9504\nvalue=-('+amount+')\nabsolute=1\nkill=1')+sound(n,when,'Effect/tengs',2)
 release='Time>=72 || (Root,MoveType=H) || (Root,Life)<=0 || RoundState!=2'
 s+=c(n,'Always free a sealed enemy','TargetState',f'NumTarget(9504)>0 && Var(3)=0 && ({release})','ID=9504\nvalue=3021')+c(n,'Release once','VarSet',release,'v=3\nvalue=1')+c(n,'Original bowl departure','ChangeAnim','Time=72','value=8822')+c(n,'Finite bowl and interruption cleanup','DestroySelf','Time>=112 || (Root,MoveType=H) || (Root,Life)<=0 || RoundState!=2');STATES.append(s)
 STATES.append(state(3020,None,'S','H','N')+c(3020,'Captured opponent retains its own sprite','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+c(3020,'Opponent is inside the closed bowl','AssertSpecial','Time<75','flag=Invisible')+ctl(3020,'Independent escape failsafe','SelfState','trigger1=Time>=130\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,NumHelper(9504)=0\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3021,None,'A','H','N')+c(3021,'Seal release motion','VelSet','Time=0','x=-3\ny=-5')+c(3021,'Restore enemy ownership','SelfState','1','value=5050\nctrl=0'))

def utility():
 for n in [170,180,190]:
  s=state(n,n)+c(n,'Original round pose','Null','1')+sound(n,'Time=0','Jigen/die' if n==170 else 'Jigen/jigenlaugh' if n==180 else 'Jigen/jigen3')
  if n==190:s+=c(n,'Brief intro','AssertSpecial','Time<40','flag=Intro')+end(n,44)
  STATES.append(s)
 STATES.append(state(500,500)+c(500,'Charge energy','PowerAdd','1','value=20')+cast(500,'Time=0 && NumHelper(9550)=0',9550)+sound(500,'Time=0','Effect/charge2',3)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 for n in [9550,9551]:
  s=state(n,8900,'A','I','N')+c(n,'Karma aura follows body','BindToRoot','1','time=1\npos=0,-43')+c(n,'Vertical aura','AngleDraw','1','value=90\nscale=.29,.34')+c(n,'Karma energy colour','PalFX','1','time=1\ncolor=0\nmul=256,75,95')+c(n,'Aura behind the real body','SprPriority','1','value=-2')+c(n,'Aura transparency','Trans','1','trans=AddAlpha\nalpha='+('180' if n==9550 else '75')+',256')+c(n,'Finite aura','DestroySelf',('(Root,StateNo)!=500' if n==9550 else '(Root,Var(40))=0')+' || RoundState!=2');STATES.append(s)
 STATES.append(state(520,520)+startup(520,'Jigen/jigen3')+sound(520,'Time=0','Effect/Karma2',2)+effect(520,'Time=10',8840,0,0,.45,30)+c(520,'Pay Karma reinforcement','PowerAdd','Time=24','value=-1500')+c(520,'Reinforced Karma','VarSet','Time=24','v=42\nvalue=1')+c(520,'Twenty second mode','VarSet','Time=24','v=40\nvalue=1200')+c(520,'Mode cooldown','VarSet','Time=24','v=41\nvalue=1500')+cast(520,'Time=24 && NumHelper(9551)=0',9551)+end(520,44))

def horn_layer():
 # Head anchors in the original (uncropped, unscaled) body cells.
 # Each controller selects the actual AIR frame, including hits and dashes.
 heads={}
 def points(stem,pts):
  for i,p in enumerate(pts,1):heads[f'{stem}_{i:02}']=(*p,0) if len(p)==2 else p
 points('Jiraiya_AirHurt',[(29,3),(29,3)])
 points('Jiraiya_Float',[(25,5)])
 points('Jiraiya_Hurt',[(12,8),(12,8)])
 points('Jiraiya_KnockDown',[(13,44,180),(6,20,90)])
 points('Jiraiya_wake',[(27,6)])
 points('Jiraiya_NAttack',[(42,5),(45,5),(45,5),(25,3),(45,10),(45,10),(45,5),(44,3),(25,5),(22,4),(19,3),(46,3)])
 points('Jiraiya_Skill01',[(25,8)])
 points('Jiraiya_Skill02',[(40,7),(42,8)])
 points('Jiraiya_Skill03_Chg',[(25,9),(25,9),(25,9)])
 points('Jiraiya_Skill03_Move',[(60,31)])
 points('Jiraiya_Skill03_cross',[(162,83)]*4+[(99,8)])
 points('Jiraiya_Skill03_Chg2',[(30,9),(42,12)])
 points('Jiraiya_Skill03_slash',[(146,120)]*4+[(44,13)])
 points('Jiraiya_Skill03_Cube',[(24,13),(25,13)])
 points('Jiraiya_Skill4_lutut_Chg',[(36,19),(31,18)])
 points('Jiraiya_Skill4_lutut',[(56,40)]*4+[(41,10)])
 points('Jiraiya_Skill4_Kick_Chg',[(25,7),(25,7),(25,7)])
 points('Jiraiya_Skill4_Kick',[(115,89)]*4+[(34,16),(30,8)])
 points('Jiraiya_CupMove',[(35,7),(45,9)])
 points('Jiraiya_Walk',[(60,3),(60,4),(60,4),(60,5),(60,5),(60,3)])
 manifest=json.loads((CHAR/'assets/sprites.json').read_text());axes={r['key']:r['axis'] for r in manifest}
 n=9560;s=state(n,8990,'A','I','N')+c(n,'No horn collision or push','PlayerPush','1','value=0')+c(n,'Horn has no shadow','AssertSpecial','1','flag=NoShadow')+c(n,'Reset visual pose','VarSet','1','v=0\nvalue=0')
 saved=[]
 for i,(key,refs) in enumerate(BODY_FRAMES.items(),1):
  if key.startswith(('Jiraiya_Ulti_','Caster_','Jiraiya_Skill05_')) or key.startswith('Jiraiya_Idle_'):continue
  refs=[(a,e) for a,e in refs if a>=10000]
  if not refs:continue
  assert key in heads,key
  x,y,angle=heads[key];ax,ay=axes[key];x-=ax;y-=ay
  triggers='\n'.join(f'trigger{j}=(Root,Anim)={a} && (Root,AnimElemNo(0))={e}' for j,(a,e) in enumerate(refs,1))
  s+=ctl(n,'Select original body head '+key,'VarSet',triggers,f'v=0\nvalue={i}')
  factor='IfElse((Root,StateNo%10000)=1420 && (Root,Time)<18,.55,1)'
  s+=c(n,'Attach original horn to '+key,'BindToRoot',f'Var(0)={i}',f'time=1\nfacing=1\npos=({x})*{factor},({y})*{factor}')
  s+=c(n,'Match horn angle and real shrink','AngleDraw',f'Var(0)={i}',f'value={angle}\nscale={factor},{factor}')
  saved.append(dict(key=key,head=heads[key][:2],angle=angle,relative=[x,y],animation_frames=refs))
 s+=c(n,'Native transformation and ultimate already contain their horn','AssertSpecial','Var(0)=0','flag=Invisible')+c(n,'Horn follows the body draw order','SprPriority','1','value=2')+c(n,'Retire the visual layer after awakening','DestroySelf','(Root,Var(42))=0 || RoundState!=2')
 STATES.append(s);(CHAR/'assets/horn_anchors.json').write_text(json.dumps(saved,indent=2)+'\n')

def ultimate():
 p=seq('Jiraiya_Skill05_Trans',1,4,4)+single('Jiraiya_Skill05_01',8)+seq('Jiraiya_Ulti_Smn',1,7,4)+single('Jiraiya_Ulti_juubi_01',5)+seq('Jiraiya_Ulti_Chg',1,4,5)+seq('Jiraiya_Ulti_shoot',1,3,4)+seq('Caster_Jiraiya_Ulti_Boom',1,6,5)+seq('Caster_Jiraiya_Ulti_Boom',3,6,5)*3+seq('Caster_Jiraiya_Ulti_Boom',7,10,5)+single('Jiraiya_Ulti_out_01',8)+list(reversed(seq('Jiraiya_Skill05_Trans',1,3,3)))
 for form in [0,1]:
  n=3000+form*10000;pose=[('Jiraiya_Skill05_Trans_04',t) if form and k.startswith('Jiraiya_Skill05_Trans_') else (k,t) for k,t in p];attack_action(n,pose,form,'5,-110,255,5');s=state(n,n,move='A',physics='N',cost=3000)+startup(n,'Jigen/jigenvo')+sound(n,'Time=0','Effect/Karma2',2)+c(n,'Reset confirmation','VarSet','Time=0','v=21\nvalue=0')+hit(n,28,0,False,ident=3000,stun=240)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Record actual enemy position','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite Bijudama damage ceiling','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{800 if form else 650},Floor((Target(3000),LifeMax)*{.80 if form else .65}))')+c(n,'Confirm the real opening hit','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(n,'Bind only a confirmed enemy','TargetBind','NumTarget(3000)>0 && Time<208','ID=3000\ntime=1\npos=(FVar(0)-Pos X)*Facing,0')
  s+=c(n,'Original explosion follows the actual victim on the ground','Explod','Time=89','anim=8850\npostype=P1\npos=IfElse(NumTarget(3000)>0,(FVar(0)-Pos X)*Facing,200),0\nscale='+('.75,.75' if form else '.6,.6')+'\nbindtime=1\nremovetime=110\nsprpriority=5\nownpal=1\nremoveongethit=1')
  s+=sound(n,'Time=52','Effect/Biju',2)+sound(n,'Time=77','Effect/hyper_punch0',2)
  for i,t in enumerate([96,110,124,138,152,166,180,194]):
   value='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)';when=f'Time={t} && NumTarget(3000)>0'
   s+=c(n,'Bounded Bijudama impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+value+')\nabsolute=1\nkill=1')+c(n,'Count explosion pulse','HitAdd',when,'value=1')+sound(n,when,'Effect/BOOM2',2)+effect(n,when,8700,'(FVar(0)-Pos X)*Facing',-35,.7,9)
  s+=c(n,'Release the opponent','TargetState','Time=208 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,230);STATES.append(s)
 STATES.append(state(3010,None,'S','H','N')+c(3010,'Opponent uses its own hurt artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Independent victim release','SelfState','trigger1=Time>=270\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3011,None,'A','H','N')+c(3011,'Release into a real fall','VelSet','Time=0','x=-5\ny=-6')+c(3011,'Return enemy state ownership','SelfState','1','value=5050\nctrl=0'))

def commands():
 import build_sarada_runtime as ref
 saved=ref.CHAR,ref.MOVES
 try:ref.CHAR=CHAR;ref.MOVES=MOVES;ref.commands()
 finally:ref.CHAR,ref.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';s=p.read_text().replace('Pink Susanoo awakening','Karma reinforcement');(CHAR/'JigenKara.cmd').write_text(s);p.unlink()

def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite Karma timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe mode expiry','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Restore base bank','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')+c(-2,'Reinforced moves use their own bank','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+cast(-2,'!IsHelper && Var(42)=1 && NumHelper(9560)=0 && RoundState=2',9560)+c(-2,'Karma physical strength','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.20,1)')+c(-2,'Reset air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge audio','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round mode cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')
 return s

def main():
 global KEY,SOUNDS
 KEY=json.loads((CHAR/'assets/keys.json').read_text());SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];basics();normals();specials();projectiles();absorption();seal();utility();ultimate();horn_layer();commands()
 const=(ROOT/'JuraShinju/JuraShinju.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):].replace('life=1300','life=1300').replace('defence=115','defence=110').replace('height=84','height=86')
 (CHAR/'JigenKara.cns').write_text('; Jigen original sprites, finite physical techniques and real Karma absorption.\n'+const+(''.join(STATES)+system()).rstrip()+'\n');(CHAR/'JigenKara.air').write_text('; Original complete body frames and projectile-only props.\n'+''.join(AIR))
 s=(ROOT/'JuraShinju/JuraShinju_common.cns').read_text();s=re.sub(r'(?m)^anim\s*=\s*(\d+)\s*$',r'anim=\1+10000*Var(42)',s);blocks=re.split(r'(?=\n\[State )',s)
 for i,b in enumerate(blocks):
  if re.search(r'(?im)^type\s*=\s*ChangeAnim\s*$',b):b=re.sub(r'(?m)^value\s*=\s*(.+)$',r'value=(\1)+10000*Var(42)',b).replace('Anim != IfElse(Vel X<0,21,20)','Anim != IfElse(Vel X<0,21,20)+10000*Var(42)').replace('Anim != 44','Anim != 44+10000*Var(42)')
  blocks[i]=b
 (CHAR/'JigenKara_common.cns').write_text(''.join(blocks))
 d=(ROOT/'JuraShinju/JuraShinju.def').read_text().replace('JuraShinju','JigenKara').replace('Jura Shinju','Jigen');d=re.sub(r'(?m)^author=.*$','author="Vaydra original sprites and audio / Alex sheet / Codex adaptation"',d);d=re.sub(r'(?m)^versiondate=.*$','versiondate=10,25,2026',d);(CHAR/'JigenKara.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,form_offset=10000,awakening='Horn awakening with stronger Karma; original horn layer follows every combat pose',activation_requires=3000,awakening_cost=1500,awakening_ticks=1200,ultimate_cost=3000,own_life_cost=0,ultimate_damage='min(650,65% max enemy life) base; min(800,80%) reinforced',absorption=dict(window=[8,36],refund=220,physical_attacks_remain_legal=True),source_art_unchanged=True,ai_generated_art=False),indent=2)+'\n');print('Jigen runtime:',len(STATES),'states;',len(AIR),'animations')
if __name__=='__main__':main()
