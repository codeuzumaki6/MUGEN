#!/usr/bin/env python3
"""Konohamaru TBV: Rasengan, Katon, Enra, seals and original clone finisher."""
import json,re
from pathlib import Path
import build_boruto_runtime as b
import build_boruto_tbv_runtime as lighting
from build_sumire_runtime import c,ctl,state,hit,end,single
ROOT=Path(__file__).resolve().parents[1];NAME='KonohamaruTBV';CHAR=ROOT/NAME
MOVES=[('Rasengan','a','F',1000,350),('Katon','a','B',1010,400),('Enra','b','F',1020,450),('Giro','b','B',1030,450),('Ascendente','c','F',1040,350),('Extension','c','B',1050,450),('Barrido','a','D',1400,200),('Clones','b','D',1410,400),('Fuin','c','D',1420,450),('Kunai','y','N',1200,200),('Shouheki','z','N',1210,250),('Martillo','y','D',1430,550),('Cuchillas','z','D',1440,600)]
PULSES=[84,112,140,168,196,224,252,284]
def seq(stem,a,z,t=3):return [(f'{stem}_{i:02}',t) for i in range(a,z+1)]
def idle(form=0):return 'Skill03_Idle_01' if form else 'Kakashi_Idle_01'
def anim(n,p,form=0,**kw):b.action(n,p,form,**kw)
def attack(n,p,form,box='-5,-80,110,5'):anim(n,p+single(idle(form),-1),form,box=box,active=list(range(len(p))))
def sound(n,t,key,ch=0):
 key=next((k for k in b.SOUNDS if k.lower()==key.lower()),key);return b.sound(n,t,key,ch)
def start(n,key):return c(n,'Technique startup','PlaySnd','Time=0','value=S1,21\nchannel=4\nvolumescale=75')+sound(n,'Time=0','Khm/'+key)+c(n,'Brief technique focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def cast(n,t,i,x=0,y=0):return b.cast(n,t,i,x,y).replace('Boruto technique','Konohamaru technique')
def fx(n,t,a,x=0,y=0,s=1,life=-2,priority=-1):return b.effect(n,t,a,x,y,s,life,priority)

def basics():
 base={0:seq('Kakashi_Idle',1,3,10),5:single(idle()),6:single('Kakashi_Skill03_01'),10:single('Kakashi_Skill03_01'),11:single('Kakashi_Skill03_01'),12:single(idle()),20:seq('Kakashi_Walk',1,6,4),21:list(reversed(seq('Kakashi_Walk',1,6,4))),100:seq('Kakashi_Walk',1,6,2),105:list(reversed(seq('Kakashi_Walk',1,6,2))),40:single('Kakashi_NAttack_11',4),41:single('Kakashi_NAttack_16',6),44:single('Kakashi_NAttack_22',6),52:single('Kakashi_Skill03_01',4)+single(idle(),4),170:single('Kakashi_KnockDown_02',30),180:seq('Kakashi_Idle',4,6,12),190:seq('Kakashi_Idle',1,3,12),500:seq('Kakashi_Skill01',1,4,6),520:seq('Kakashi_Skill03',1,16,3),5000:seq('Kakashi_Hurt',1,2,5),5010:seq('Kakashi_Hurt',1,2,5),5020:single('Kakashi_AirHurt_01'),5030:single('Kakashi_Float_01'),5100:seq('Kakashi_KnockDown',1,2,7),5110:single('Kakashi_KnockDown_02',28),5120:seq('Kakashi_KnockDown',3,4,7)+single(idle(),5),5150:single('Kakashi_KnockDown_02',60),5200:single('Kakashi_AirHurt_01'),5210:single('Kakashi_Float_01'),5300:single('Kakashi_Hurt_01',20)}
 for n in [120,130,140,150,121,131,141,151,122,132,142,152]:base[n]=single('Kakashi_NAttack_01')
 base[190]=seq('Kakashi_Skill04',1,4,3)+seq('Kakashi_Skill04',8,15,2)+seq('Kakashi_Idle',1,3,3)
 base[520]+=single('Kakashi_Skill03_16',-1)
 for form in [0,1]:
  for n,p in base.items():
   if form and n in [0,5,180,190,500]:p=seq('Skill03_Idle',1,3,8)
   if form and n in [20,21,100,105]:p=seq('Skill03_Walk',1,6,2 if n>=100 else 4);p=list(reversed(p)) if n in [21,105] else p
   if form and n in [120,130,140,150]:p=single('Skill03_01_01')
   anim(n+form*10000,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-42,-25,44,0' if n in [170,5100,5110,5150] else '-18,-58,18,0' if n in [6,10,11] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:anim(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 anim(8800,single('ThrownKunai',4),hurt=False,loop=True,add=True,box='-20,-8,20,8')
 anim(8801,seq('MonStaff',1,4,3),hurt=False,loop=True,add=True,box='-24,-25,24,25')
 anim(8813,seq('FuinFX',1,17,3),hurt=False,add=True)
 p=seq('MassivFX',1,16,2)+seq('MassivFX',17,22,4)*8+seq('MassivFX',23,31,4);anim(8817,p,hurt=False,add=True)
 for i,stem in enumerate(['KakashiSkill01','Kakashi_Skil01']):anim(8825+i,seq(stem,5,24,3),box='45,-90,120,-20')
 anim(9709,single('Kakashi_Skill02_03',6),loop=True)
 anim(9790,single('Kakashi_Hurt_01',8))

def normals():
 for form in [0,1]:
  sets=[seq('Kakashi_NAttack',2,5,3),seq('Kakashi_NAttack',6,10,2),seq('Kakashi_NAttack',17,21,2)] if not form else [seq('Skill03_01',1,4,3),seq('Skill03_02',2,6,2),seq('Skill03_02',15,20,2)]
  for family in [200,210,220,600,610,620]:
   for step in range(3):
    air=family>=600;n=family+step+10000*form;p=sets[(step+family%100//10)%3];attack(n,p,form,'-8,-83,125,5' if form else '-5,-80,105,5')
    s=state(n,n,'A' if air else 'S','A','N' if air else 'S',vel=None if air else '2,0')+sound(n,'Time=0','Khm/Attack01_01')+hit(n,3,([45,60,80] if form else [36,48,66])[step],step==2,air=air,stun=15)
    if air:s+=c(n,'Air chain limit','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Air approach','VelSet','Time<7','x=2\ny=-.4')+c(n,'Gravity','VelAdd','Time>=7','y=.48')+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
    else:s+=c(n,'Brake','VelSet','Time>=8','x=0')
    b.STATES.append(s+end(n,21 if air else 25,50 if air else 0))

def specials():
 for form in [0,1]:
  for name,button,d,base,cost in MOVES:
   n=base+10000*form
   p={1000:seq('Kakashi_Skill01',1,24,2),1010:seq('Kakashi_Skill02',1,25,2),1020:([] if form else seq('Kakashi_Skill03',1,16,2))+seq('Skill03_01',1,4,4),1030:seq('Skill03_02',1,14,3),1040:seq('Kakashi_NAttack',11,16,4),1050:seq('Skill03_02',15,20,5),1400:seq('Kakashi_NAttack',6,10,4),1410:seq('Kakashi_Skill04',1,4,5)+single('Kakashi_Skill02_03',15),1420:single('Kakashi_Skill02_03',70),1200:seq('Kakashi_Skill04',4,7,5),1210:seq('Shouheki',1,4,6),1430:seq('Skill03_02',21,42,3),1440:seq('Kakashi_Skill05',1,28,3)}[base]
   box='-5,-83,125,5'
   if base==1000:box='10,-95,150,5'
   if base==1010:box='35,-125,280,5'
   if base in [1410,1200]:box=None
   if base==1400:box='-5,-40,105,5'
   if base==1420:box='25,-95,175,5'
   if base==1050:box='20,-80,155,5'
   attack(n,p,form,box);voice='garyuEndan' if base==1010 else 'Fuin' if base==1420 else 'rasen' if base==1000 else 'summon' if base in [1020,1410] else 'Attack03_01' if base in [1030,1050,1430] else 'S05' if base==1440 else 'Attack02_01';s=state(n,n,move='A',physics='N',cost=cost)+start(n,voice)
   if base==1000:
    s+=c(n,'Carry the original Rasengan','VelSet','Time>=8 && Time<34 && !MoveContact','x=IfElse(P2Dist X>65,6,0)')+hit(n,14,130 if form else 100,stun=30)+hit(n,30,155 if form else 125,True)+sound(n,'Time=14','Effect/rasenS',2)
   elif base==1010:s+=hit(n,10,90 if form else 70,stun=26)+hit(n,22,95 if form else 75,stun=26)+hit(n,34,110 if form else 85,True)+sound(n,'Time=10','Effect/Katon',2)
   elif base==1020:
    t=4 if form else 36;s+=c(n,'Enra approach','VelSet',f'Time>={t} && Time<{t+10} && !MoveContact','x=6')+hit(n,t,230 if form else 180,True)+sound(n,f'Time={t}','Effect/stick_damage',2)
   elif base==1030:s+=c(n,'Sweep forward','VelSet','Time<25 && !MoveContact','x=4')+hit(n,5,80 if form else 60,stun=27)+hit(n,25,160 if form else 125,True)+cast(n,'Time=26',9501,60,-30)
   elif base==1040:s+=c(n,'Actual upward strike','VelSet','Time=6','x=3\ny=-6')+c(n,'Airborne','StateTypeSet','Time=6','statetype=A\nphysics=N')+c(n,'Gravity','VelAdd','Time>6','y=.48')+hit(n,6,95 if form else 75,air=True)+hit(n,15,135 if form else 105,True,air=True)+c(n,'Land','ChangeState','Time>18 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
   elif base==1050:s+=hit(n,5,100 if form else 80,stun=28)+hit(n,17,170 if form else 140,True)+sound(n,'Time=5','Effect/stick_damage',2)
   elif base==1400:s+=c(n,'Low approach','VelSet','Time<14','x=4')+hit(n,5,145 if form else 110,True,low=True)
   elif base==1410:s+=cast(n,'Time=10 && NumHelper(9700)=0',9700,-45,0)+cast(n,'Time=14 && NumHelper(9701)=0',9701,-65,0)+sound(n,'Time=10','Effect/poof2',2)
   elif base==1420:
    s+=c(n,'Place the seal around the actual rival','PosAdd','Time=6','x=IfElse(P2Dist X>350,250,P2Dist X-100)')+fx(n,'Time=7',8813,100,0,.55,51,-1)+cast(n,'Time=7 && NumHelper(9710)=0',9710,200,0)+hit(n,19,40,ident=1420,stun=65)+'p2stateno=3020\np2getp1state=1\n'+c(n,'Hold only the confirmed seal','TargetBind','NumTarget(1420)>0 && Time<55','ID=1420\ntime=1\npos=100,-5')
    for t in [25,31,37,43,49]:s+=c(n,'Sealing pulse','TargetLifeAdd',f'Time={t} && NumTarget(1420)>0',f'ID=1420\nvalue=-{45 if form else 35}\nabsolute=1\nkill=1')
    s+=c(n,'Release seal','TargetState','Time=55 && NumTarget(1420)>0','ID=1420\nvalue=3021')
   elif base==1200:s+=cast(n,'Time=8',9500,45,-38)+sound(n,'Time=8','Effect/shuriken',2)
   elif base==1210:s+=c(n,'Barrier step','VelSet','Time<10 && !MoveContact','x=3')+hit(n,18,165 if form else 125,True)+c(n,'Finite projectile barrier','ReversalDef','Time>=5 && Time<=17','reversal.attr=SCA,NP,SP,HP\npausetime=2,5\nsparkno=-1\nhitsound=S1,9\np1stateno=0')
   elif base==1430:s+=c(n,'Leap with the staff','PosSet','Time>=5 && Time<20','y=-3*(Time-5)')+c(n,'Descend for the slam','PosSet','Time>=20 && Time<35','y=-45+3*(Time-20)')+c(n,'Ground the impact','PosSet','Time>=35','y=0')+hit(n,9,75 if form else 55,air=True)+hit(n,42,270 if form else 210,True)
   elif base==1440:s+=c(n,'Chakra blade dash','VelSet','Time>=8 && Time<35 && !MoveContact','x=7')+hit(n,17,80 if form else 60,stun=30)+hit(n,38,105 if form else 80,stun=30)+hit(n,66,190 if form else 150,True)+c(n,'Lift with the source blades','PosSet','Time>=48 && Time<60','y=-4*(Time-48)')+c(n,'Land before the source ground burst','PosSet','Time>=60 && Time<69','y=-48+(Time-60)*48/9.0')+c(n,'Ground burst','PosSet','Time>=69','y=0')
   s+=c(n,'Stop movement','VelSet','MoveContact || Time>=35','x=0')+end(n,max(38,sum(t for _,t in p)+6),50 if base==1040 else 0);b.STATES.append(s)

def helpers():
 s=state(9500,8800,'A','A','N',vel='11,0')+c(9500,'Kunai size','AngleDraw','1','scale=.55,.55')+c(9500,'No physical push','PlayerPush','1','value=0')+hit(9500,0,'IfElse((Root,Var(42)),125,100)',True,air=True,projectile=True)+c(9500,'Finite throw','DestroySelf','MoveContact || Time>=60 || RoundState!=2');b.STATES.append(s)
 b.STATES.append(state(9501,8801,'A','A','N',vel='8,0')+c(9501,'Original fire wheel size','AngleDraw','1','scale=.45,.45')+c(9501,'No physical push','PlayerPush','1','value=0')+hit(9501,0,'IfElse((Root,Var(42)),110,90)',True,air=True,projectile=True)+c(9501,'Finite fire wheel','DestroySelf','MoveContact || Time>=60 || RoundState!=2'))
 for n in [9700,9701,9710]:
  s=state(n,9709 if n==9710 else 8825+n-9700,'S','I' if n==9710 else 'A','N',vel='0,0' if n==9710 else '5,0')+c(n,'Real clone health','LifeSet','Time=0','value=120')+c(n,'No clone push','PlayerPush','1','value=0')+c(n,'Clone can be struck','HitOverride','1','attr=SCA,NA,SA,HA,NP,SP,HP,NT,ST,HT\nstateno=9790\ntime=1\nforceair=0','ignorehitpause=1')
  if n==9710:s+=c(n,'Face into the seal','Turn','Time=0','')+c(n,'Finite seal assistant','DestroySelf','Time>=75 || (Root,StateNo%10000)!=1420 || (Root,Life)<=0 || RoundState!=2')
  else:s+=hit(n,9,'IfElse((Root,Var(42)),115,85)',True,stun=28)+c(n,'Stop at impact','VelSet','MoveContact || Time>=35','x=0')+c(n,'Fade after the attack','Trans','Time>=56','trans=addalpha\nalpha=Floor(256*(70-Time)/14.0),Floor(256*(Time-56)/14.0)')+c(n,'Finite Rasengan assistant','DestroySelf','Time>=70 || Life<=0 || (Root,Life)<=0 || RoundState!=2')
  b.STATES.append(s)
 b.STATES.append(state(9790,9790,'S','H','N')+sound(9790,'Time=0','Effect/poof2',2)+fx(9790,'Time=0',8710,0,-35,.5,12,3).replace('removeongethit=1','removeongethit=0')+c(9790,'A struck clone disperses immediately','DestroySelf','1','','ignorehitpause=1'))

def utility():
 for n in [170,180,190]:
  s=state(n,n)+sound(n,'Time=0','Khm/dead1' if n==170 else 'Khm/Ikuzo')
  if n==190:s+=c(n,'Intro','AssertSpecial','Time<36','flag=Intro')+end(n,40)
  b.STATES.append(s)
 b.STATES.append(state(500,500)+c(500,'Charge','PowerAdd','1','value=20')+sound(500,'Time=0','Effect/Charging',3)+cast(500,'Time=0 && NumHelper(9551)=0',9551,0,0)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 for n in [9551,9560]:
  b.STATES.append(state(n,8900,'A','I','N')+c(n,'Aura follows body','BindToRoot','1','time=1\npos=0,-42')+c(n,'Chakra aura','AngleDraw','1','value=90\nscale=.35,.44')+c(n,'Behind the fighter','SprPriority','1','value=-2')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+c(n,'Finite aura','DestroySelf','RoundState!=2 || (Root,Life)<=0 || '+('(Root,StateNo)!=500' if n==9551 else '(Root,Var(42))=0')))
 b.STATES.append(state(520,520)+start(520,'summon')+sound(520,'Time=24','Khm/Enra')+c(520,'Pay staff mode','PowerAdd','Time=47','value=-1500')+c(520,'Enra staff mode','VarSet','Time=47','v=42\nvalue=1')+c(520,'Twenty seconds','VarSet','Time=47','v=40\nvalue=1200')+c(520,'Cooldown','VarSet','Time=47','v=41\nvalue=1500')+end(520,62))

def ultimate():
 for form in [0,1]:
  n=3000+form*10000;p=seq('Kakashi_Skill01',1,8,4)+single('Kakashi_Skill03_01',16)+single('Kakashi_Skill02_03',262);attack(n,p,form,'10,-95,145,5')
  s=state(n,n,move='A',physics='N',cost=3000)+start(n,'Haaaa')+c(n,'Clear contact','VarSet','Time=0','v=21\nvalue=0')+c(n,'Visible Rasengan approach','VelSet','Time>=8 && Time<28 && !MoveContact','x=IfElse(P2Dist X>65,6,0)')+c(n,'Stop at impact','VelSet','MoveContact || Time>=28','x=0')+hit(n,29,0,ident=3000,stun=330)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Finite damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{800 if form else 650},Floor((Target(3000),LifeMax)*{.8 if form else .65}))')+c(n,'Confirm hit','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+fx(n,'Time=45 && NumTarget(3000)>0',8817,65,0,.65,260,-1)+c(n,'Hold inside the Rasengan formation','TargetBind','NumTarget(3000)>0 && Time<300','ID=3000\ntime=1\npos=65,-45-5*Abs(Sin(Time*.2))')
  for i,t in enumerate(PULSES):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)';s+=c(n,'Confirmed clone impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count impact','HitAdd',when,'value=1')+fx(n,when,8700,65,-75,.7,8,3)+sound(n,when,'Effect/damage_rasen',2)
  b.STATES.append(s+c(n,'Release opponent','TargetState','Time=300 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,310))
 for n,parent,limit in [(3010,3000,350),(3020,1420,90)]:b.STATES.append(state(n,None,'A','H','N')+c(n,'Keep the opponent artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(n,'Independent release','SelfState',f'trigger1=Time>={limit}\ntrigger2=NumEnemy=0\ntrigger3=(EnemyNear,StateNo)%10000!={parent}\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 for n in [3011,3021]:b.STATES.append(state(n,None,'A','H','N')+c(n,'Release motion','VelSet','Time=0','x=-4\ny=-6')+c(n,'Return opponent states','SelfState','1','value=5050\nctrl=0'))

def main():
 b.CHAR=CHAR;b.NAME=NAME;b.AIR=[];b.STATES=[];b.KEY=json.loads((CHAR/'assets/keys.json').read_text());b.SPRITES={r['key']:r for r in json.loads((CHAR/'assets/sprites.json').read_text())};b.SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];b.idle=idle
 basics();normals();specials();helpers();utility();ultimate();lighting.compatible_light_layers()
 import build_sarada_runtime as commands
 saved=commands.CHAR,commands.MOVES
 try:commands.CHAR=CHAR;commands.MOVES=MOVES;commands.commands()
 finally:commands.CHAR,commands.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';commands_text=p.read_text().replace('Pink Susanoo awakening','Enra staff awakening').replace('[State -1, Clones]\ntype=ChangeState','[State -1, Clones]\ntype=ChangeState\ntriggerall=NumHelper(9700)=0 && NumHelper(9701)=0');(CHAR/(NAME+'.cmd')).write_text(commands_text);p.unlink()
 const=(ROOT/'BorutoTBVBase/BorutoTBVBase.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):]
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite mode clock','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe mode expiry','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Base animation bank','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && SelfAnimExist(Anim-10000)','value=Anim-10000')+c(-2,'Staff animation bank','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+cast(-2,'!IsHelper && RoundState=2 && Var(42)=1 && NumHelper(9560)=0',9560,0,0)+c(-2,'Staff technique power','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.18,1)')+c(-2,'Reset air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop released charge sound','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round mode cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')+cast(-2,'!IsHelper && RoundState=2 && NumHelper(9580)=0 && (MoveType=A || StateNo=500 || StateNo=520)',9580,0,0)
 (CHAR/(NAME+'.cns')).write_text('; Original Konohamaru TBV sprites and sounds.\n'+const+''.join(b.STATES)+s.rstrip()+'\n');(CHAR/(NAME+'.air')).write_text('; Indexed body sprites and synchronized original light.\n'+''.join(b.AIR));(CHAR/(NAME+'_common.cns')).write_bytes((ROOT/'BorutoTBVBase/BorutoTBVBase_common.cns').read_bytes())
 d=(ROOT/'BorutoTBVBase/BorutoTBVBase.def').read_text().replace('BorutoTBVBase',NAME).replace('Boruto Uzumaki TBV Base','Konohamaru Sarutobi TBV').replace('10,28,2026','10,31,2026');(CHAR/(NAME+'.def')).write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,awakening='Enra staff',awakening_ticks=1200,awakening_cost=1500,ultimate_damage=[650,800],ultimate_pulses=PULSES,own_life_cost=0,clone_health=120,clone_ticks=70),indent=2)+'\n');print(NAME,len(b.STATES),'states;',len(b.AIR),'animations')
if __name__=='__main__':main()
