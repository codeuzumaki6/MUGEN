#!/usr/bin/env python3
"""Original adult KCM moves and a separate Baryon awakening moveset."""
import json
from pathlib import Path
import build_boruto_runtime as b
import build_boruto_tbv_runtime as lighting
from build_sumire_runtime import c,ctl,state,hit,end,single
ROOT=Path(__file__).resolve().parents[1];NAME='NarutoKCM';CHAR=ROOT/NAME
MOVES=[('Rasengan','a','F',1000,350),('Brazo','a','B',1010,400),('Combo','b','F',1020,450),('Rueda','b','B',1030,450),('Ascendente','c','F',1040,350),('Descenso','c','B',1050,450),('Barrido','a','D',1400,200),('Destello','b','D',1410,350),('Palma','c','D',1420,400),('Puno','y','N',1200,200),('RasenCorto','z','N',1210,250),('Odama','y','D',1430,550),('Kurama','z','D',1440,600)]
PULSES=[84,112,140,168,196,224,252,284];ULTIMATE_DAMAGE=[300,360]
VOICES={'Rasengan':'rasen','Brazo':'NAttack02','Combo':'naruto_combo','Rueda':'heaa','Ascendente':'NarutoSannin_Combo_02','Descenso':'N','Barrido':'Hit','Destello':'wes','Palma':'1','Puno':'Hit','RasenCorto':'rasen','Odama':'Nrto OdamaRsg','Kurama':'kurama2','ultimate':'Kurama_combo','awakening':'NarutoBaryon'}
def seq(stem,a,z,t=3):return [(f'{stem}_{i:02}',t) for i in range(a,z+1)]
def idle(form=0):return 'Baryon_idle_01' if form else 'Kcm_Idle_01'
def anim(n,p,form=0,**kw):b.action(n,p,form,**kw)
def attack(n,p,form,box='-5,-85,115,5',hurt_box=None):anim(n,p+single(idle(form),-1),form,box=box,active=list(range(len(p))),hurt_box=hurt_box or ('-18,-90,20,0' if form else None))
def sound(n,t,key,ch=0):return b.sound(n,t,key,ch)
def start(n,voice):return c(n,'Technique startup','PlaySnd','Time=0','value=S1,21\nchannel=4\nvolumescale=75')+sound(n,'Time=0','BTM/'+voice)+c(n,'Brief technique focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def cast(n,t,i,x=0,y=0):return b.cast(n,t,i,x,y).replace('Boruto technique','Naruto KCM technique')
def fx(n,t,a,x=0,y=0,s=1,life=-2,priority=-1):return b.effect(n,t,a,x,y,s,life,priority)

def basics():
 base={0:seq('Kcm_Idle',1,3,10),5:single(idle()),6:single('Naruto_Wake_03'),10:single('Naruto_Wake_03'),11:single('Naruto_Wake_03'),12:single(idle()),20:seq('Naruto_Walk',1,6,4),21:list(reversed(seq('Naruto_Walk',1,6,4))),100:seq('Naruto_Walk',1,6,2),105:list(reversed(seq('Naruto_Walk',1,6,2))),40:single('Naruto_Natk_06',4),41:single('Naruto_Skill03_Kick_01',6),44:single('Naruto_AirHurt_01'),52:single('Naruto_Wake_03',4)+single(idle(),4),170:single('Naruto_Dead_01',30),180:seq('Kcm_Idle',1,3,12),190:seq('Kcm_Idle',1,3,12),500:seq('Kcm_Idle',1,3,8),520:seq('Naruto_Transform',1,9,5)+single('Baryon_idle_01',-1),5000:seq('Naruto_Hurt',1,2,5),5010:seq('Naruto_Hurt',1,2,5),5020:single('Naruto_AirHurt_01'),5030:single('Naruto_Float_01'),5100:single('Naruto_Knock_01',8)+single('Naruto_Dead_01',12),5110:single('Naruto_Dead_01',28),5120:seq('Naruto_Wake',1,3,7)+single(idle(),5),5150:single('Naruto_Dead_01',60),5200:single('Naruto_AirHurt_01'),5210:single('Naruto_Float_01'),5300:single('Naruto_Hurt_01',20)}
 for n in [120,130,140,150,121,131,141,151,122,132,142,152]:base[n]=single('Naruto_Natk_01')
 for form in [0,1]:
  for n,original in base.items():
   p=original
   if form:
    p=single(idle(1),sum(max(0,t) for _,t in original) or 8)
    if n in [0,5,180,190,500]:p=seq('Baryon_idle',1,3,8)
    if n in [20,21,100,105]:p=seq('Baryon_Walk',1,6,2 if n>=100 else 4);p=list(reversed(p)) if n in [21,105] else p
    if n in [6,10,11,5000,5010,5300]:p=single('BaryonEnd_04',8)
    if n in [40,41,44,5020,5030,5200,5210]:p=single('Baryon_Walk_03',8)
    if n in [5100,5110,5150,170]:p=single('BaryonEnd_04',28)
    if n==5120:p=list(reversed(seq('BaryonEnd',1,4,4)))+single(idle(1),5)
   anim(n+10000*form,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-42,-25,44,0' if n in [170,5100,5110,5150] else '-18,-58,20,0' if n in [6,10,11] else '-18,-90,20,0' if form else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:anim(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 armposes=[(f'Naruto_Skill04_Hst_{i:02}_FX',3) for i in range(1,8)]*2+[(f'Naruto_Skill04_bom_{i:02}_FX',3) for i in range(1,14)];anim(8800,armposes,hurt=False,box='-105,-135,105,10');anim(8802,[(k+'_Light' if k+'_Light' in b.KEY else 'LightEmpty',t) for k,t in armposes],hurt=False,add=True)
 anim(8810,[(f'DustFx_{i:02}',3) for i in range(4)],hurt=False,add=True)
 anim(8811,[(f'BlinkEfx_{i:02}',2) for i in range(5)],hurt=False,add=True)
 anim(8830,seq('OdamaOrb',1,4,3),hurt=False,loop=True,add=True)
 odamaposes=[(f'OdamaNrt_Hit_{i:02}_FX',3) for i in range(1,5)]+[(f'OdamaNrt_Bom_{i:02}_FX',3) for i in range(1,7)];anim(8831,odamaposes,hurt=False,box='-110,-70,110,10');anim(8832,[(k+'_Light' if k+'_Light' in b.KEY else 'LightEmpty',t) for k,t in odamaposes],hurt=False,add=True)

def normals():
 for form in [0,1]:
  sets=[seq('Naruto_Natk',2,4,3),seq('Naruto_Natk',4,6,3),seq('Naruto_Natk',7,10,3)] if not form else [seq('Baryon_Hit01',1,4,3),seq('Baryon_Hit02',1,4,3),seq('BaryonUK',8,13,2)]
  for family in [200,210,220,600,610,620]:
   for step in range(3):
    air=family>=600;n=family+step+form*10000;p=sets[(step+family%100//10)%3];attack(n,p,form)
    s=state(n,n,'A' if air else 'S','A','N' if air else 'S',vel=None if air else '2,0')+sound(n,'Time=0','BTM/Hit')+hit(n,3,([28,38,52] if form else [24,32,44])[step],step==2,air=air,stun=15)
    if air:s+=c(n,'Air chain limit','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Air approach','VelSet','Time<7','x=2\ny=-.4')+c(n,'Gravity','VelAdd','Time>=7','y=.48')+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
    else:s+=c(n,'Brake','VelSet','Time>=8','x=0')
    b.STATES.append(s+end(n,21 if air else 25,50 if air else 0))

def special_poses(base,form):
 if form:return {1000:seq('BaryonDash',1,7,2)+seq('Baryon_Hit01',1,6,3),1010:seq('Baryon_Hit02',1,6,5),1020:seq('Baryon_Hit01',1,6,3)+seq('Baryon_Hit02',1,6,3),1030:seq('BaryonUK',1,7,4),1040:seq('BaryonUK',1,7,3),1050:seq('BaryonUK',8,14,4),1400:seq('BaryonEnd',1,4,2)+seq('Baryon_Hit01',1,4,3),1410:seq('BaryonDash',1,7,2)+seq('Baryon_Hit02',1,6,3),1420:seq('Baryon_Hit02',1,6,3)+seq('BaryonUK',8,14,2),1200:seq('Baryon_Hit01',1,6,3),1210:seq('BaryonDash',1,7,2)+seq('Baryon_Hit02',1,6,2),1430:seq('BaryonUK',1,14,3),1440:seq('BaryonDash',1,7,2)+seq('Baryon_Hit01',1,6,2)+seq('Baryon_Hit02',1,6,2)+seq('BaryonUK',1,14,2)}[base]
 return {1000:seq('NarutoRSCHG',1,6,3)+single('Naruto_Skill01_Dash_01',10)+seq('Naruto_RSHIT',1,6,3)+seq('Naruto_RSDD',1,6,3),1010:seq('Naruto_Skill04_Punch',1,5,5)+seq('Naruto_Skill02_punch',2,5,3),1020:seq('Naruto_Skill02_punch',1,5,2)+seq('Naruto_Skill02_KickA',1,5,2)+seq('Naruto_Skill02_KickB',1,7,2),1030:single('Naruto_Natk_01',58),1040:seq('Naruto_Skill03_Kick',1,8,3),1050:seq('Naruto_Skill03_Kick',7,11,5),1400:seq('Naruto_Natk',7,10,5),1410:seq('Naruto_Skill02_punch',1,5,4),1420:seq('Naruto_Skill02_punch',1,5,4)+seq('Naruto_Skill02_KickA',1,5,3),1200:seq('Naruto_Skill04_Punch',1,5,3),1210:seq('NarutoRSCHG',5,6,4)+seq('Naruto_RSHIT',1,6,3)+seq('Naruto_RSDD',1,6,2),1430:seq('Naruto_Skill03_Kick',7,8,4)+single('Naruto_Skill03_Kick_07',14)+seq('Naruto_RSDD',1,6,3),1440:seq('Naruto_Skill03_Kurama',1,20,4)}[base]

def specials():
 for form in [0,1]:
  for name,button,d,base,cost in MOVES:
   n=base+form*10000;p=special_poses(base,form);box='-5,-90,120,5'
   if not form and base in [1010,1200]:box='10,-100,245,5'
   if base in [1000,1210] and not form:box='10,-100,175,5'
   if base in [1030,1430] and not form:box=None
   if base==1400:box='-5,-45,105,5'
   if base==1440 and not form:box='-20,-160,170,10'
   attack(n,p,form,box,hurt_box='-18,-110,20,10' if not form and base==1430 else None)
   s=state(n,n,move='A',physics='N',cost=cost)+start(n,'NarutoBaryon' if form and base==1440 else 'NAttack02' if form else VOICES[name])
   if base in [1000,1020,1210] or form and base in [1410,1440]:s+=c(n,'Real technique approach','VelSet','Time>=6 && Time<28 && !MoveContact','x=IfElse(P2Dist X>50,6,0)')
   if base==1010 and form:s+=c(n,'Brief backstep before the counterpalm','VelSet','Time<4','x=-3')+c(n,'Plant before striking','VelSet','Time=4','x=0')
   if base in [1040,1050] or base==1430:
    s+=c(n,'Actual takeoff','VelSet','Time=4','x=2.5\ny='+('-7' if base==1430 and not form else '-6' if base==1040 else '-4'))+c(n,'Airborne body','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Finite gravity','VelAdd','Time>4','y=.5')+c(n,'Land with control','ChangeState','Time>20 && Pos Y>=0 && Vel Y>0',f'value={1060+10000*form}\nctrl=0')
   if base==1410:s+=fx(n,'Time=3',8811,0,-40,.45,10,3)+c(n,'Visible speed step','PosAdd','Time=8','x=IfElse(P2Dist X>220,170,IfElse(P2Dist X>55,P2Dist X-55,0))')
   if not form and base==1030:s+=cast(n,'Time=8 && NumHelper(9500)=0',9500,'IfElse(P2Dist X>180,180,P2Dist X)',0)+sound(n,'Time=8','Effect/dash_effect',2)
   elif not form and base==1430:s+=c(n,'Hold the original blue sphere above the raised hand','Explod','Time=4','anim=8830\npostype=P1\npos=0,-100\nscale=.7,.7\nbindtime=-1\nremovetime=20\nsprpriority=3\nownpal=1\nremoveongethit=1')+cast(n,'Time=22 && NumHelper(9503)=0',9503,'IfElse(P2Dist X<45,45,IfElse(P2Dist X>190,190,P2Dist X))',0)+sound(n,'Time=22','Effect/kawaki bom',2)
   else:
    times={1000:[26,38,51] if not form else [14,23],1010:[10,27] if not form else [9,22],1020:[6,16,28] if not form else [5,18,30],1030:[7,19],1040:[6,14],1050:[11],1400:[5] if not form else [10],1410:[12] if not form else [17],1420:[7,24],1200:[6] if not form else [4],1210:[11,24] if not form else [15,23],1430:[6,20],1440:[28,44,62] if not form else [10,25,45]}[base]
    values=({1000:[35,40,55],1010:[50,80],1020:[40,45,55],1040:[45,65],1050:[135],1400:[75],1410:[100],1420:[50,70],1200:[95],1210:[45,65],1440:[50,55,70]} if not form else {1000:[65,85],1010:[60,80],1020:[45,50,65],1030:[65,85],1040:[55,75],1050:[155],1400:[90],1410:[120],1420:[65,85],1200:[110],1210:[55,75],1430:[50,140],1440:[45,65,85]})[base]
    for i,(t,damage) in enumerate(zip(times,values)):s+=hit(n,t,damage,i==len(times)-1,low=base==1400,air=base in [1040,1050,1430],stun=30)
    if base in [1000,1210] and not form:s+=sound(n,f'Time={times[0]}','Effect/damage_rasen',2)
    if base==1440 and not form:s+=sound(n,'Time=28','Effect/Biju',2)
   b.STATES.append(s+c(n,'Stop after contact','VelSet','MoveContact || Time>=30','x=0')+end(n,max(36,sum(t for _,t in p)+6),50 if base in [1040,1050,1430] else 0))
  n=1060+10000*form;anim(n,seq('Naruto_Skill03_Kick',9,11,4)+single(idle(),4) if not form else seq('BaryonEnd',1,4,3)+single(idle(1),4),form);b.STATES.append(state(n,n)+c(n,'Ground the landing','PosSet','Time=0','y=0')+fx(n,'Time=0',8810,0,0,.7,12,-1)+sound(n,'Time=0','Effect/landing2',2)+end(n,16))

def helpers():
 for n,an,size,times,damages in [(9500,8800,.55,[9,30,52],[40,45,55]),(9503,8831,.6,[5,13,21],[45,50,65])]:
  s=state(n,an,'S','A','N')+c(n,'Original effect scale','AngleDraw','1',f'scale={size},{size}')+c(n,'Ground the actual field','PosSet','Time=0','y=0')+c(n,'See the real opponent inside the effect','SprPriority','1','value=-1')+c(n,'No effect push','PlayerPush','1','value=0')+c(n,'No effect shadow','AssertSpecial','1','flag=NoShadow')
  s+=c(n,'Original synchronized soft light','Explod','Time=0',f'anim={8802 if n==9500 else 8832}\npostype=P1\npos=0,0\nscale={size},{size}\nbindtime=-1\nremovetime={81 if n==9500 else 30}\nsprpriority=-1\nownpal=1\nremoveongethit=1')
  for i,(t,damage) in enumerate(zip(times,damages)):s+=hit(n,t,damage,i==len(times)-1,projectile=True,stun=28)
  b.STATES.append(s+c(n,'Finite original field','DestroySelf','AnimTime=0 || Time>=100 || RoundState!=2'))

def utility():
 for n in [170,180,190]:
  s=state(n,n)+sound(n,'Time=0','BTM/Dead' if n==170 else 'BTM/ikeze')
  if n==190:s+=c(n,'Intro','AssertSpecial','Time<32','flag=Intro')+end(n,36)
  b.STATES.append(s)
 b.STATES.append(state(500,500)+c(500,'Charge energy','PowerAdd','1','value=20')+sound(500,'Time=0','Effect/RsChg',3)+cast(500,'Time=0 && NumHelper(9551)=0',9551)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 b.STATES.append(state(9551,8900,'A','I','N')+c(9551,'Charge follows the real body','BindToRoot','1','time=1\npos=0,-42')+c(9551,'Golden chakra size','AngleDraw','1','value=90\nscale=.32,.42')+c(9551,'Golden chakra tint','PalFX','1','time=1\ncolor=0\nmul=256,210,64')+c(9551,'Behind the fighter','SprPriority','1','value=-2')+c(9551,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9551,'Finite charge glow','DestroySelf','RoundState!=2 || (Root,Life)<=0 || (Root,StateNo)!=500'))
 b.STATES.append(state(520,520)+start(520,VOICES['awakening'])+sound(520,'Time=24','Effect/BEAM',2)+c(520,'Pay Baryon mode','PowerAdd','Time=47','value=-1500')+c(520,'Original Baryon form','VarSet','Time=47','v=42\nvalue=1')+c(520,'Twenty seconds','VarSet','Time=47','v=40\nvalue=1200')+c(520,'Cooldown','VarSet','Time=47','v=41\nvalue=1500')+end(520,62))

def ultimate():
 for form in [0,1]:
  n=3000+10000*form
  prep=(seq('NarutoRSCHG',1,4,4)+single('Naruto_Skill01_Dash_01',6)+seq('Naruto_RSHIT',1,5,2)+seq('Naruto_Skill03_Kurama',1,9,4)+single('Naruto_Skill03_Kurama_09',14)) if not form else (seq('BaryonDash',1,7,3)+single('Baryon_Hit01_01',5)+single('Baryon_Hit01_02',6)+seq('Baryon_Hit01',3,6,4)+seq('BaryonUK',1,7,4)+single(idle(1),6))
  assert sum(t for _,t in prep)==82
  p=list(prep)
  for i in range(8):
   if i==7:p+=single(idle(1) if form else 'Naruto_Skill03_Kurama_09',4)
   if form:
    stem='Baryon_Hit01' if i%2==0 else 'Baryon_Hit02'
    p+=single(stem+'_01',2)+seq(stem,2,6,4)+single(idle(1),6) if i!=7 else single('BaryonUK_08',2)+seq('BaryonUK',9,13,4)+single('BaryonUK_14',6)
   else:p+=[(f'Naruto_Skill03_Kurama_{j:02}',4) for j in ([10,11,12,13,14,15,9] if i<7 else [10,11,12,16,17,18,19])]
  assert sum(t for _,t in p)==310
  anim(n,p+single(idle(form),-1),form,box='10,-95,150,5' if not form else '10,-90,110,5',active=list(range(10)),hurt_box='-18,-90,20,0' if form else None)
  s=state(n,n,move='A',physics='N',cost=3000)+start(n,'NarutoBaryon' if form else 'Kurama_combo')+c(n,'Clear confirmed contact','VarSet','Time=0','v=21\nvalue=0')+c(n,'Approach for the actual opening strike','VelSet','Time>=8 && Time<28 && !MoveContact','x=IfElse(P2Dist X>65,6,0)')+c(n,'Stop at contact','VelSet','MoveContact || Time>=28','x=0')+hit(n,29,0,ident=3000,stun=330)+'p2stateno=3010\np2getp1state=1\n'
  budget=ULTIMATE_DAMAGE[form];point=58 if form else 80
  s+=c(n,'Bounded damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{budget},Floor((Target(3000),LifeMax)*{budget/1000}))')+c(n,'Confirm actual opening hit','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(n,'Hold at the real impact point','TargetBind','NumTarget(3000)>0 && Time<300',f'ID=3000\ntime=1\npos={point},-20-5*Abs(Sin(Time*.2))')
  for i,t in enumerate(PULSES):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)';s+=c(n,'Confirmed finite impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count actual impact','HitAdd',when,'value=1')+fx(n,when,8700,point,-55,.65,8,3)+sound(n,when,'Effect/hit01' if form else 'Effect/Biju',2)
  b.STATES.append(s+c(n,'Release the opponent','TargetState','Time=300 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,310))
 b.STATES.append(state(3010,None,'A','H','N')+c(3010,'Preserve opponent artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Independent interruption release','SelfState','trigger1=Time>=350\ntrigger2=NumEnemy=0\ntrigger3=(EnemyNear,StateNo)%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 b.STATES.append(state(3011,None,'A','H','N')+c(3011,'Real release velocity','VelSet','Time=0','x=-4\ny=-6')+c(3011,'Return opponent ownership','SelfState','1','value=5050\nctrl=0'))

def main():
 b.CHAR=CHAR;b.NAME=NAME;b.AIR=[];b.STATES=[];b.KEY=json.loads((CHAR/'assets/keys.json').read_text());b.SPRITES={r['key']:r for r in json.loads((CHAR/'assets/sprites.json').read_text())};b.SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];b.idle=idle
 basics();normals();specials();helpers();utility();ultimate();lighting.compatible_light_layers()
 import build_sarada_runtime as commands
 saved=commands.CHAR,commands.MOVES
 try:commands.CHAR=CHAR;commands.MOVES=MOVES;commands.commands()
 finally:commands.CHAR,commands.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';cmd=p.read_text().replace('Pink Susanoo awakening','Original Baryon awakening')
 for name,helper in [('Rueda',9500),('Odama',9503)]:cmd=cmd.replace(f'[State -1, {name}]\ntype=ChangeState',f'[State -1, {name}]\ntype=ChangeState\ntriggerall=Var(42)=1 || NumHelper({helper})=0')
 (CHAR/(NAME+'.cmd')).write_text(cmd);p.unlink()
 const=(ROOT/'NarutoBTM/NarutoBTM.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):];s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite Baryon clock','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe mode expiry','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'KCM animation bank','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && SelfAnimExist(Anim-10000)','value=Anim-10000')+c(-2,'Baryon animation bank','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+c(-2,'Reset air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge sound','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round form cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')+cast(-2,'!IsHelper && RoundState=2 && NumHelper(9580)=0 && (MoveType=A || StateNo=500 || StateNo=520)',9580)
 (CHAR/(NAME+'.cns')).write_text('; Original KCM and Baryon sprites.\n'+const+''.join(b.STATES)+s.rstrip()+'\n');(CHAR/(NAME+'.air')).write_text('; Indexed actors and original additive effects.\n'+''.join(b.AIR));(CHAR/(NAME+'_common.cns')).write_bytes((ROOT/'NarutoBTM/NarutoBTM_common.cns').read_bytes())
 d=(ROOT/'NarutoBTM/NarutoBTM.def').read_text().replace('NarutoBTM',NAME).replace('Naruto Uzumaki BTM','Naruto Uzumaki KCM');(CHAR/(NAME+'.def')).write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,awakening='Original red Baryon form with separate taijutsu moves',awakening_ticks=1200,awakening_cost=1500,ultimate_damage=ULTIMATE_DAMAGE,ultimate_pulses=PULSES,own_life_cost=0),indent=2)+'\n');print(NAME,len(b.STATES),'states;',len(b.AIR),'animations')
if __name__=='__main__':main()
