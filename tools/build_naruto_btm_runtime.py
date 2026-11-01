#!/usr/bin/env python3
"""Naruto BTM: original Rasengan, clones, Rasenshuriken and Kurama avatar."""
import json
from pathlib import Path
import build_boruto_runtime as b
import build_boruto_tbv_runtime as lighting
from build_sumire_runtime import c,ctl,state,hit,end,single
ROOT=Path(__file__).resolve().parents[1];NAME='NarutoBTM';CHAR=ROOT/NAME
MOVES=[('Rasengan','a','F',1000,350),('Muro','a','B',1010,400),('Rasenshuriken','b','F',1020,450),('Combo','b','B',1030,450),('Ascendente','c','F',1040,350),('Caida','c','B',1050,450),('Barrido','a','D',1400,200),('Clones','b','D',1410,400),('Impacto','c','D',1420,400),('Onda','y','N',1200,200),('Disco','z','N',1210,250),('RasenCampo','y','D',1430,550),('Bijudama','z','D',1440,600)]
PULSES=[84,112,140,168,196,224,252,284]
VOICES={'Rasengan':'rasen','Muro':'04','Rasenshuriken':'Rs Srkn','Combo':'1','Ascendente':'N','Caida':'heaa','Barrido':'Hit','Clones':'04','Impacto':'1','Onda':'Hit','Disco':'Rs Srkn','RasenCampo':'3','Bijudama':'kurama2','ultimate':'Kurama_combo','awakening':'koc'}
def seq(stem,a,z,t=3):return [(f'{stem}_{i:02}',t) for i in range(a,z+1)]
def idle(form=0):return 'NarutoNew_Idle_01'
def anim(n,p,form=0,**kw):b.action(n,p,form,**kw)
def attack(n,p,form,box='-5,-82,110,5'):anim(n,p+single(idle(),-1),form,box=box,active=list(range(len(p))))
def sound(n,t,key,ch=0):return b.sound(n,t,key,ch)
def start(n,voice):return c(n,'Technique startup','PlaySnd','Time=0','value=S1,21\nchannel=4\nvolumescale=75')+sound(n,'Time=0','BTM/'+voice)+c(n,'Brief technique focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def cast(n,t,i,x=0,y=0):return b.cast(n,t,i,x,y).replace('Boruto technique','Naruto technique')
def fx(n,t,a,x=0,y=0,s=1,life=-2,priority=-1):return b.effect(n,t,a,x,y,s,life,priority)

def basics():
 base={0:seq('NarutoNew_Idle',1,3,10),5:single(idle()),6:single('NarutoNew_Doton_01'),10:single('NarutoNew_Doton_01'),11:single('NarutoNew_Doton_01'),12:single(idle()),20:seq('NarutoNew_Walk',1,6,4),21:list(reversed(seq('NarutoNew_Walk',1,6,4))),100:seq('NarutoNew_Walk',1,6,2),105:list(reversed(seq('NarutoNew_Walk',1,6,2))),40:single('NarutoNew_NAttack_06',4),41:single('NarutoNew_Kick01_01',6),44:single('NarutoNew_AirHurt_01',6),52:single('NarutoNew_Doton_01',4)+single(idle(),4),170:single('NarutoNew_KnockDown_03',30),180:single('NarutoNew_Idle_001',24)+single('NarutoNew_Idle_002',24),190:single('NarutoNew_Idle_002',12)+seq('NarutoNew_Idle',1,3,8),500:single('NarutoNew_Idle_002',8),520:single('NarutoNew_Idle_002',8)+seq('KCM_Trans',1,8,5)+single('KCM_Trans_08',-1),5000:seq('NarutoNew_Hurt',1,3,5),5010:seq('NarutoNew_Hurt',1,3,5),5020:seq('NarutoNew_AirHurt',1,2,5),5030:single('NarutoNew_Float_01'),5100:seq('NarutoNew_KnockDown',1,3,6),5110:single('NarutoNew_KnockDown_03',28),5120:seq('NarutoNew_KnockDown',3,4,7)+single(idle(),5),5150:single('NarutoNew_KnockDown_03',60),5200:single('NarutoNew_AirHurt_01'),5210:single('NarutoNew_Float_01'),5300:single('NarutoNew_Hurt_01',20)}
 for n in [120,130,140,150,121,131,141,151,122,132,142,152]:base[n]=single('NarutoNew_NAttack_01')
 for form in [0,1]:
  for n,p in base.items():anim(n+form*10000,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-42,-25,44,0' if n in [170,5100,5110,5150] else '-18,-58,18,0' if n in [6,10,11] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:anim(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 anim(8800,seq('BlltPunchNrt',1,3,3),hurt=False,loop=True,add=True,box='-38,-28,38,28')
 anim(8801,seq('SRK_Walks',1,4,3),hurt=False,loop=True,add=True,box='-85,-100,85,10')
 anim(8802,seq('SRKBOM',1,8,3)+seq('SRKDEAD',1,6,3)+single('SRKBOM_09',4),hurt=False,add=True,box='-125,-160,125,15')
 anim(8803,seq('fxDoton',1,6,5),hurt=False,add=True,box='-135,-85,140,10')
 anim(8804,seq('SRKBOM',1,8,4)*2+seq('SRKDEAD',1,6,3)+single('SRKBOM_09',4),hurt=False,add=True,box='-140,-180,140,15')
 anim(8815,seq('AnginRibut',1,9,3),hurt=False,add=True)
 anim(8820,seq('KuramaAura',1,8,5),hurt=False,loop=True,add=True)
 for i in [9700,9701]:anim(i,seq('NarutoNew_NAttack',2,5,3)+seq('NarutoNew_NAttack',7,10,3)+single(idle(),-1),box='-5,-82,105,5')
 anim(9790,single('NarutoNew_Hurt_01',6))

def normals():
 sets=[seq('NarutoNew_NAttack',2,4,3),seq('NarutoNew_NAttack',4,6,3),seq('NarutoNew_NAttack',7,10,3)]
 for form in [0,1]:
  for family in [200,210,220,600,610,620]:
   for step in range(3):
    air=family>=600;n=family+step+10000*form;p=sets[(step+family%100//10)%3];attack(n,p,form)
    s=state(n,n,'A' if air else 'S','A','N' if air else 'S',vel=None if air else '2,0')+sound(n,'Time=0','BTM/Hit')+hit(n,3,([45,60,80] if form else [36,48,66])[step],step==2,air=air,stun=15)
    if air:s+=c(n,'Air chain limit','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Air approach','VelSet','Time<7','x=2\ny=-.4')+c(n,'Gravity','VelAdd','Time>=7','y=.48')+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
    else:s+=c(n,'Brake','VelSet','Time>=8','x=0')
    b.STATES.append(s+end(n,21 if air else 25,50 if air else 0))

def specials():
 for form in [0,1]:
  for name,button,d,base,cost in MOVES:
   n=base+10000*form
   p={1000:seq('NarutoNew_RS_CHG',1,6,3)+single('NarutoNew_RS_CHGMove_01',10)+seq('NarutoNew_RS_Hit',1,6,3)+seq('NarutoNew_RS_Dd',1,6,3),1010:seq('NarutoNew_Doton',1,2,12)+single('NarutoNew_Idle_002',12),1020:seq('NarutoNew_RS_SRK_CHG',1,4,3)+seq('NarutoNew_RS_SRK_Stnc',1,4,3)+seq('NarutoNew_RS_SRK_Tro',1,2,5),1030:seq('NarutoNew_Pnch',1,7,3)+seq('NarutoNew_Kick01',1,7,3),1040:seq('NarutoNew_Kick01',1,7,4),1050:seq('NarutoNew_Kick02',1,9,4),1400:seq('NarutoNew_NAttack',7,10,5),1410:seq('NarutoNew_Bushin',1,6,4),1420:seq('NarutoNew_Pnch',1,7,4),1200:seq('NarutoNew_NAttack',2,5,4),1210:seq('NarutoNew_RS_SRK_CHG',1,4,3)+seq('NarutoNew_RS_SRK_Tro',1,2,4),1430:seq('NarutoNew_RS_SRK_CHG',1,4,4)+seq('NarutoNew_RS_SRK_Stnc',1,4,4)+seq('NarutoNew_RS_SRK_Tro',1,2,4),1440:seq('KURAMA_Stnc',1,3,3)+seq('KURAMA_Chg',1,2,5)*2+seq('KURAMA_Trw',1,3,3)+seq('KURAMABOM',1,16,3)}[base]
   box='-5,-85,120,5'
   if base==1000:box='15,-90,125,5'
   if base in [1010,1020,1410,1200,1210,1430]:box=None
   if base==1400:box='-5,-40,90,5'
   if base==1440:box='-20,-180,150,5'
   attack(n,p,form,box);s=state(n,n,move='A',physics='N',cost=cost)+start(n,VOICES[name])
   if base==1000:
    s+=c(n,'Carry Rasengan to real contact','VelSet','Time>=18 && Time<36 && !MoveContact','x=IfElse(P2Dist X>55,6,0)')+hit(n,28,90 if form else 65,stun=32)+hit(n,44,100 if form else 75,stun=32)+hit(n,55,150 if form else 115,True)+sound(n,'Time=28','Effect/damage_rasen',2)
   elif base==1010:s+=cast(n,'Time=10',9503,80,0)+sound(n,'Time=10','Effect/Batu murag',2)
   elif base==1020:s+=cast(n,'Time=25',9501,48,0)+sound(n,'Time=25','Effect/rsShuriken',2)
   elif base==1030:s+=c(n,'Chakra combo approach','VelSet','Time<22 && !MoveContact','x=5')+hit(n,7,75 if form else 55,stun=30)+hit(n,24,90 if form else 65,stun=30)+hit(n,31,155 if form else 125,True)
   elif base==1040:s+=c(n,'Rising kick','VelSet','Time=4','x=3\ny=-6')+c(n,'Airborne','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Gravity','VelAdd','Time>4','y=.5')+hit(n,5,95 if form else 70,air=True,stun=26)+hit(n,14,145 if form else 110,True,air=True)+c(n,'Land','ChangeState','Time>18 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
   elif base==1050:s+=c(n,'A short real leap','VelSet','Time=2','x=4\ny=-4')+c(n,'Airborne','StateTypeSet','Time=2','statetype=A\nphysics=N')+c(n,'Descending strike','VelAdd','Time>2','y=.55')+hit(n,6,90 if form else 65,air=True,stun=26)+hit(n,16,155 if form else 120,True,air=True)+c(n,'Land','ChangeState','Time>20 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
   elif base==1400:s+=c(n,'Sweep step','VelSet','Time<10','x=3')+hit(n,5,145 if form else 110,True,low=True)
   elif base==1410:s+=cast(n,'Time=8 && NumHelper(9700)=0',9700,20,0)+cast(n,'Time=12 && NumHelper(9701)=0',9701,-25,0)+sound(n,'Time=8','Effect/poof2',2)
   elif base==1420:s+=hit(n,8,120 if form else 90,stun=28)+cast(n,'Time=13',9500,60,-42)+sound(n,'Time=8','Effect/damage_h',2)
   elif base==1200:s+=cast(n,'Time=6',9500,50,-38)+sound(n,'Time=6','Effect/combo3',2)
   elif base==1210:s+=cast(n,'Time=13',9502,45,0)+sound(n,'Time=13','Effect/rsShuriken',2)
   elif base==1430:s+=cast(n,'Time=33',9504,'IfElse(P2Dist X<50,50,IfElse(P2Dist X>240,240,P2Dist X))',0)+sound(n,'Time=33','Effect/Boom',2)
   elif base==1440:
    for t,dmg in [(39,85),(48,95),(60,125)]:s+=hit(n,t,dmg+(20 if form else 0),t==60,stun=36)
    s+=sound(n,'Time=38','Effect/explosion1',2)+fx(n,'Time=38',8815,35,-75,.4,27,-2)
   s+=c(n,'Stop movement on contact','VelSet','MoveContact || Time>=35','x=0')+end(n,max(36,sum(t for _,t in p)+6),50 if base in [1040,1050] else 0);b.STATES.append(s)

def helpers():
 for n,an,size,speed,boxdamage in [(9500,8800,.35,10,105),(9501,8801,.6,8,130),(9502,8801,.35,11,150)]:
  s=state(n,an,'A','A','N',vel=f'{speed},0')+c(n,'Original projectile scale','AngleDraw','1',f'scale={size},{size}')+c(n,'No projectile push','PlayerPush','1','value=0')+hit(n,0,f'IfElse((Root,Var(42)),{boxdamage+35},{boxdamage})',n!=9501,projectile=True,air=True,stun=34)
  if n==9501:s+=c(n,'Rasenshuriken bursts on actual contact','ChangeState','MoveContact','value=9511\nctrl=0')
  b.STATES.append(s+c(n,'Finite projectile','DestroySelf',('MoveContact || ' if n!=9501 else '')+'Time>=65 || RoundState!=2'))
 for n,an,size,times in [(9511,8802,.6,[6,17,28]),(9503,8803,.6,[8]),(9504,8804,.65,[4,20,36,52])]:
  s=state(n,an,'S','A','N')+c(n,'Original ground effect size','AngleDraw','1',f'scale={size},{size}')+c(n,'Ground the real burst','PosSet','Time=0','y=0')+c(n,'Let the actual victim remain visible','SprPriority','1','value=-1')+c(n,'No effect push','PlayerPush','1','value=0')
  for i,t in enumerate(times):s+=hit(n,t,'IfElse((Root,Var(42)),95,70)' if n!=9503 else 'IfElse((Root,Var(42)),185,145)',i==len(times)-1,projectile=True,stun=30)
  b.STATES.append(s+c(n,'Finite ground effect','DestroySelf','AnimTime=0 || Time>=100 || RoundState!=2'))
 for n in [9700,9701]:
  s=state(n,n,'S','A','N',vel='4,0')+c(n,'Real clone health','LifeSet','Time=0','value=120')+c(n,'No clone push','PlayerPush','1','value=0')+c(n,'Clone can be struck','HitOverride','1','attr=SCA,NA,SA,HA,NP,SP,HP,NT,ST,HT\nstateno=9790\ntime=1\nforceair=0','ignorehitpause=1')+hit(n,4,'IfElse((Root,Var(42)),70,50)',stun=28)+hit(n,14,'IfElse((Root,Var(42)),85,65)',True,stun=28)+c(n,'Stop after the attack','VelSet','Time>=20','x=0')+c(n,'Finite shadow clone','DestroySelf','Time>=70 || Life<=0 || (Root,Life)<=0 || RoundState!=2')
  b.STATES.append(s)
 b.STATES.append(state(9790,9790,'S','H','N')+sound(9790,'Time=0','Effect/poof2',2)+fx(9790,'Time=0',8710,0,-35,.5,12,3).replace('removeongethit=1','removeongethit=0')+c(9790,'A struck clone disperses immediately','DestroySelf','1','','ignorehitpause=1'))

def utility():
 for n in [170,180,190]:
  s=state(n,n)+sound(n,'Time=0','BTM/Dead' if n==170 else 'BTM/ikeze')
  if n==190:s+=c(n,'Intro','AssertSpecial','Time<32','flag=Intro')+end(n,36)
  b.STATES.append(s)
 b.STATES.append(state(500,500)+c(500,'Charge','PowerAdd','1','value=20')+sound(500,'Time=0','Effect/RsChg',3)+cast(500,'Time=0 && NumHelper(9551)=0',9551)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 b.STATES.append(state(9551,8900,'A','I','N')+c(9551,'Charge follows body','BindToRoot','1','time=1\npos=0,-42')+c(9551,'Charge aura size','AngleDraw','1','value=90\nscale=.35,.44')+c(9551,'Behind the fighter','SprPriority','1','value=-2')+c(9551,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9551,'Finite charge aura','DestroySelf','RoundState!=2 || (Root,Life)<=0 || (Root,StateNo)!=500'))
 b.STATES.append(state(9560,8820,'A','I','N')+c(9560,'Original Kurama flames follow body','BindToRoot','1','time=1\npos=0,0')+c(9560,'Behind the fighter','SprPriority','1','value=-2')+c(9560,'Hide redundant aura during original avatar composites','AssertSpecial','(Root,StateNo)%10000=1440 || (Root,StateNo)%10000=3000 || (Root,StateNo)=520','flag=Invisible')+c(9560,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9560,'Finite Kurama aura','DestroySelf','RoundState!=2 || (Root,Life)<=0 || (Root,Var(42))=0'))
 b.STATES.append(state(520,520)+start(520,VOICES['awakening'])+sound(520,'Time=24','BTM/Kurama_combo')+c(520,'Pay chakra mode','PowerAdd','Time=47','value=-1500')+c(520,'Kurama chakra mode','VarSet','Time=47','v=42\nvalue=1')+c(520,'Twenty seconds','VarSet','Time=47','v=40\nvalue=1200')+c(520,'Cooldown','VarSet','Time=47','v=41\nvalue=1500')+end(520,62))

def ultimate():
 for form in [0,1]:
  n=3000+form*10000;p=seq('NarutoNew_RS_CHG',1,4,4)+single('NarutoNew_RS_CHGMove_01',8)+seq('NarutoNew_RS_Hit',1,4,2)+seq('KCM_Trans',1,8,3)+seq('KURAMA_Stnc',1,3,3)+seq('KURAMA_Chg',1,2,6)+seq('KURAMA_Trw',1,3,2)+seq('KURAMABOM',1,6,4)*8+seq('KURAMABOM',7,16,3)+single(idle(),-1)
  anim(n,p,form,box='10,-90,130,5',active=list(range(9)))
  s=state(n,n,move='A',physics='N',cost=3000)+start(n,VOICES['ultimate'])+c(n,'Clear contact','VarSet','Time=0','v=21\nvalue=0')+c(n,'Approach with the visible Rasengan','VelSet','Time>=8 && Time<28 && !MoveContact','x=IfElse(P2Dist X>65,6,0)')+c(n,'Stop at real impact','VelSet','MoveContact || Time>=28','x=0')+hit(n,29,0,ident=3000,stun=330)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Finite damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{800 if form else 650},Floor((Target(3000),LifeMax)*{.8 if form else .65}))')+c(n,'Confirm impact','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(n,'Hold inside the Kurama blast','TargetBind','NumTarget(3000)>0 && Time<300','ID=3000\ntime=1\npos=65,-25-5*Abs(Sin(Time*.2))')
  for i,t in enumerate(PULSES):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)';s+=c(n,'Confirmed Kurama impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count impact','HitAdd',when,'value=1')+fx(n,when,8700,65,-65,.7,8,3)+sound(n,when,'Effect/explosion1',2)
  b.STATES.append(s+c(n,'Release opponent','TargetState','Time=300 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,310))
 b.STATES.append(state(3010,None,'A','H','N')+c(3010,'Keep opponent artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Independent release','SelfState','trigger1=Time>=350\ntrigger2=NumEnemy=0\ntrigger3=(EnemyNear,StateNo)%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 b.STATES.append(state(3011,None,'A','H','N')+c(3011,'Release motion','VelSet','Time=0','x=-4\ny=-6')+c(3011,'Return opponent states','SelfState','1','value=5050\nctrl=0'))

def main():
 b.CHAR=CHAR;b.NAME=NAME;b.AIR=[];b.STATES=[];b.KEY=json.loads((CHAR/'assets/keys.json').read_text());b.SPRITES={r['key']:r for r in json.loads((CHAR/'assets/sprites.json').read_text())};b.SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];b.idle=idle
 basics();normals();specials();helpers();utility();ultimate();lighting.compatible_light_layers()
 import build_sarada_runtime as commands
 saved=commands.CHAR,commands.MOVES
 try:commands.CHAR=CHAR;commands.MOVES=MOVES;commands.commands()
 finally:commands.CHAR,commands.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';cmd=p.read_text().replace('Pink Susanoo awakening','Kurama chakra awakening').replace('[State -1, Clones]\ntype=ChangeState','[State -1, Clones]\ntype=ChangeState\ntriggerall=NumHelper(9700)=0 && NumHelper(9701)=0');(CHAR/(NAME+'.cmd')).write_text(cmd);p.unlink()
 const=(ROOT/'BorutoTBVBase/BorutoTBVBase.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):]
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite mode clock','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe mode expiry','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Base animation bank','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && SelfAnimExist(Anim-10000)','value=Anim-10000')+c(-2,'Awake animation bank','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+cast(-2,'!IsHelper && RoundState=2 && Var(42)=1 && NumHelper(9560)=0',9560)+c(-2,'Awake technique power','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.18,1)')+c(-2,'Reset air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop released charge sound','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round mode cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')+cast(-2,'!IsHelper && RoundState=2 && NumHelper(9580)=0 && (MoveType=A || StateNo=500 || StateNo=520)',9580)
 (CHAR/(NAME+'.cns')).write_text('; Original Naruto BTM sprites and sounds.\n'+const+''.join(b.STATES)+s.rstrip()+'\n');(CHAR/(NAME+'.air')).write_text('; Indexed body sprites and original additive light.\n'+''.join(b.AIR));(CHAR/(NAME+'_common.cns')).write_bytes((ROOT/'BorutoTBVBase/BorutoTBVBase_common.cns').read_bytes())
 d=(ROOT/'BorutoTBVBase/BorutoTBVBase.def').read_text().replace('BorutoTBVBase',NAME).replace('Boruto Uzumaki TBV Base','Naruto Uzumaki BTM').replace('10,28,2026','11,1,2026');(CHAR/(NAME+'.def')).write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,awakening='Kurama chakra aura and avatar techniques',awakening_ticks=1200,awakening_cost=1500,ultimate_damage=[650,800],ultimate_pulses=PULSES,own_life_cost=0,clone_health=120,clone_ticks=70),indent=2)+'\n');print(NAME,len(b.STATES),'states;',len(b.AIR),'animations')
if __name__=='__main__':main()
