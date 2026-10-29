#!/usr/bin/env python3
"""Boruto: original sword, Rasengan, Karma/Jogan sequences and a finite clone."""
from pathlib import Path
from PIL import Image
import json,re
from build_sumire_runtime import ctl,c,state,hit,end,common_sound,single
ROOT=Path(__file__).resolve().parents[1];NAME='BorutoKarmaJogan';CHAR=ROOT/NAME;AIR=[];STATES=[];KEY={};SOUNDS={}
MOVES=[('Rasengan','a','F',1000,350),('Shiden','a','B',1010,400),('Kenjutsu','b','F',1020,450),('Espiral','b','B',1030,550),('Ascendente','c','F',1040,350),('Combo','c','B',1050,450),('Barrido','a','D',1400,200),('Bunshin','b','D',1410,300),('Caida','c','D',1420,450),('Kunai','y','N',1200,200),('Disparo','z','N',1210,250),('Invocacion','y','D',1430,600),('Futon','z','D',1440,600)]
PULSES=[44,82,118,142,164,198,220,244]
def seq(stem,a,b,t=3):return [(f'Pain_{stem}_{i:02}',t) for i in range(a,b+1)]
def rawseq(stem,a,b,t=3):return [(f'{stem}_{i:02}',t) for i in range(a,b+1)]
def idle(form=0):return 'Pain_Idle_01'
def action(n,poses,form=0,box=None,active=None,hurt=True,loop=False,add=False,hurt_box=None):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+ (hurt_box or '-16,-85,18,0')+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(poses):
  actual_box=box(key) if callable(box) else box
  if actual_box and (active is None or i in active):
   boxes=actual_box if isinstance(actual_box,list) else [actual_box];s+=f'Clsn1: {len(boxes)}\n'+''.join(f' Clsn1[{j}]={b}\n' for j,b in enumerate(boxes))
  g,p=KEY[key];s+=f'{g},{p},0,0,{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def attack(n,p,form,box='-5,-85,125,5'):action(n,p+single(idle(form),-1),form,box=box,active=list(range(len(p))))
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Supplied Boruto audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def startup(n,voice='BorutoJogan/01'):
 return common_sound(n,'Time=0')+sound(n,'Time=0',voice,volume=110 if voice.endswith('/03') else 90)+c(n,'Brief technique focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def effect(n,when,anim,x=0,y=-35,scale=1,ticks=-2,priority=4):return c(n,'Separate original effect','Explod',when,f'anim={anim}\npostype=P1\npos={x},{y}\nscale={scale},{scale}\nremovetime={ticks}\nbindtime=1\nsprpriority={priority}\nownpal=1\nremoveongethit=1')
def cast(n,when,ident,x=35,y=-38):return c(n,'Finite technique resource','Helper',when,f'helpertype=Normal\nname="Boruto technique"\nID={ident}\nstateno={ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def visual_box(key,scale):
 rec=SPRITES[key];im=Image.open(CHAR/rec['file']).convert('RGBA');a=im.getchannel('A').point(lambda v:255 if v>=180 else 0);bb=a.getbbox() or im.getbbox();ax,ay=rec['axis']
 return ','.join(str(round((v-(ax if i%2==0 else ay))*scale)) for i,v in enumerate(bb))
def basic():
 base={0:seq('Idle',1,3,10),5:seq('Idle',1,1,8),6:seq('KnockDown',4,4,8),10:seq('KnockDown',4,4,6),11:seq('KnockDown',4,4,8),12:seq('Idle',1,1,6),20:seq('Walk',1,6,4),21:list(reversed(seq('Walk',1,6,4))),100:seq('Walk',1,6,2),105:list(reversed(seq('Walk',1,6,2))),40:rawseq('Unframe',1,1,6),41:seq('AirHurt',1,2,6),44:rawseq('Unframe',2,2,8),52:seq('KnockDown',4,5,5)+seq('Idle',1,1,4),170:seq('KnockDown',3,3,30),180:seq('Idle',1,3,12),190:seq('Idle',1,3,12),500:seq('Skill05',23,25,8),520:seq('Skill05',23,25,4)+seq('Skill01',49,52,5)*2+seq('Idle',1,1,10),5000:seq('Hurt',1,2,6),5010:seq('Hurt',1,2,6),5020:seq('AirHurt',1,2,6),5030:seq('KnockDown',1,2,8),5100:seq('KnockDown',1,3,8),5110:seq('KnockDown',3,3,28),5120:seq('KnockDown',4,5,8)+seq('Idle',1,1,5),5150:seq('KnockDown',3,3,60),5200:seq('AirHurt',1,1,8),5210:seq('AirHurt',2,2,8),5300:seq('Hurt',1,1,20)}
 for n in [120,130,140,150,121,131,141,151,122,132,142,152]:base[n]=rawseq('Unframe',3,3,6)
 for n in [6,10,11,12]:base[n]=seq('Skill01',60,60,6)
 base[52]=seq('Skill01',60,60,5)+seq('Idle',1,1,5)
 for form in [0,1]:
  for n,p in base.items():action(n+10000*form,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-40,-25,42,0' if n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,seq('Skill02',1,8,3),hurt=False,loop=True,box=lambda k:visual_box(k,.9))
 # RasenShot.xml supplies a spherical Rasengan and its burst. The old
 # Skill04 cells were cylindrical spirals from a different technique.
 action(8801,seq('Skill03',56,59,3),hurt=False,loop=True,box='-30,-30,30,30')
 action(8805,seq('Skill03',60,66,2),hurt=False)
 action(8802,seq('Skill02',25,32,3),hurt=False,box=lambda k:visual_box(k,.65))
 action(8803,seq('Skill04',37,44,3),hurt=False,box=lambda k:visual_box(k,.6))
 action(8804,seq('Skill03',12,30,2),hurt=False,box=lambda k:visual_box(k,.55))
 action(8810,rawseq('JouganSCR',1,5,4),hurt=False)
 action(8811,rawseq('JouganEye',1,3,5),hurt=False)
 action(8812,[(f'BOLT_{i:02}',4) for i in [1,2,3,7,8,9]],hurt=False,loop=True)
 action(8813,seq('Skill05',125,140,3),hurt=False)
 action(8814,rawseq('Duar_Move',1,17,3),hurt=False)
 # MUGEN reads additive blending from AIR. Explod's trans parameter is an
 # Ikemen extension and must not be the only source of transparency.
 action(8815,rawseq('AnginRibut',1,9,3),hurt=False,loop=True,add=True)
 action(8816,rawseq('WindHand',1,7,3),hurt=False,loop=True,add=True)
 action(8817,[(f'Uzuhiko_Tornado_{i:02}',3) for i in range(4)],hurt=False,loop=True,add=True)
 action(8820,seq('Skill01',17,19,3),hurt=False,loop=True,box='-36,-36,36,36')
 action(8821,seq('Skill01',20,31,2),hurt=False)
 action(8822,seq('Skill05',5,22,3),hurt=False,box=lambda k:visual_box(k,.55))
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
 base={1000:seq('Skill03',1,11,3),1010:seq('Skill01',49,52,4)+seq('Skill01',53,59,3),1020:seq('Skill02',34,43,4),1040:seq('Skill02',17,24,4),1050:seq('Skill04',29,36,4),1400:seq('NAttack',7,10,4),1410:rawseq('Unframe',1,3,8),1420:seq('Skill02',44,54,4),1200:throw,1210:(seq('Skill03',33,34,7)+seq('Skill03',55,55,9))*2,1430:seq('Skill04',45,81,2)}
 awake={1000:seq('Skill02',44,54,4),1010:seq('Skill05',111,124,3),1020:base[1020],1040:seq('Skill04',82,94,3),1050:seq('Skill03',6,11,3)+seq('Skill04',30,35,3),1400:seq('NAttack',13,16,4),1410:base[1410],1420:seq('Skill05',141,163,3)+seq('Skill05',164,173,2),1200:throw*2,1210:base[1210]}
 for form in [0,1]:
  for name,b,d,ident,cost in MOVES:
   if ident==1030:
    uzuhiko(ident+10000*form,form,cost);continue
   if ident==1440:
    futon_rasengan(ident+10000*form,form,cost);continue
   if form and ident==1430:
    mokuton(ident+10000*form,cost);continue
   n=ident+10000*form;p=(awake if form else base)[ident];box='-5,-85,145,5'
   if ident in [1000,1020,1050]:box='-15,-85,95,5'
   if ident==1040:box='-15,-90,90,10'
   if ident==1010:box='-80,-100,250,5'
   if ident in [1030,1420] and form:box='-100,-135,185,5'
   if ident==1400:box='-5,-40,110,5'
   if ident==1430:box='-65,-145,260,5' if not form else '-130,-150,210,5'
   if ident==1440:box='15,-110,245,5'
   aerial_single=(form and ident==1000) or (not form and ident==1420)
   giant=form and ident in [1420,1440]
   if aerial_single:box=lambda k:'-75,5,75,145' if k.startswith('Pain_Skill02_') and int(k.rsplit('_',1)[-1])>=49 else None
   if giant:box=lambda k:(['-165,-5,-15,125','15,-5,175,125'] if int(k.rsplit('_',1)[-1])<=163 else '-190,-65,190,150') if k.startswith('Pain_Skill05_') and 149<=int(k.rsplit('_',1)[-1])<=173 else None
   if not form and ident==1440:box=None
   attack(n,p,form,box);voice='BorutoJogan/'+('04' if ident==1430 else '05' if ident==1440 else '03' if ident in [1000,1030,1210,1420] else '02' if ident in [1020,1040] else '01')
   s=state(n,n,move='A',physics='N',cost=cost)+startup(n,voice)
   if ident in [1000,1020,1050] and not aerial_single:
    s+=c(n,'Physical technique approach','VelSet','Time>=6 && Time<28 && !MoveContact','x='+('10' if form and ident==1020 else '7'))+c(n,'Brake on contact','VelSet','MoveContact || Time>=28','x=0')
   if aerial_single or giant:
    # The art places the striking sphere below the caster. Move the actual
    # player into the air so both its body box and the sphere stay meaningful.
    top=90 if giant else 110;start=4;rise_end=20 if ident!=1440 else 16;finish=sum(t for _,t in p)
    s+=c(n,'Show opponent reacting in the sphere','SprPriority','1','value=-1')+c(n,'Airborne Rasengan caster','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Controlled takeoff','PosSet',f'Time>=4 && Time<{rise_end}',f'y=-{top}*(Time-4)/{rise_end-4}')+c(n,'Original airborne contact height','PosSet',f'Time>={rise_end}',f'y=-{top}')+c(n,'Airborne approach','VelSet',f'Time>=4 && Time<{rise_end}',f'x=IfElse(P2Dist X>85,4,0)\ny=0')+c(n,'Keep caster above the spheres','VelSet',f'Time>={rise_end}','x=0\ny=0')+c(n,'Descend after the original impact','VelSet',f'Time>={finish}','x=0\ny=2')+c(n,'Return through real air physics','ChangeState',f'Time>={finish}','value=50\nctrl=0')
   elif ident==1040:
    s+=c(n,'Real rising motion','VelSet','Time=4','x=4\ny=-6.5')+c(n,'Airborne','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Finite gravity','VelAdd','Time>4','y=.46')+c(n,'Original landing','ChangeState','Time>20 && Pos Y>=0 && Vel Y>0','value='+str(1060+10000*form)+'\nctrl=0')
   if not form and ident==1440:
    s+=cast(n,'Time=12',9504,40,-38)+sound(n,'Time=12','Effect/RSGfuton',2)
   elif ident in [1200,1210]:
    for t in ([14,37] if ident==1210 else [9,19,29] if form else [9]):s+=cast(n,f'Time={t}',9500 if ident==1200 else 9501)+sound(n,f'Time={t}','Effect/BladeA' if ident==1200 else 'Effect/rasenS',2)
   elif ident==1410:s+=cast(n,'Time=10 && NumHelper(9700)=0',9700,-28,0)+c(n,'Order the existing clone','VarAdd','Time=12','v=45\nvalue=1')
   else:
    times={1000:[23,35] if aerial_single else [15,28],1010:[16,28,40] if form else [16,28],1020:[6,23],1040:[6,23],1050:[5,18,30],1400:[5],1420:[28,40,54] if form else [23,35],1430:[18,36,54],1440:[22,38,52]}[ident]
    values={1000:[75,110],1010:[65,80,125] if form else [55,140],1020:[80,115],1030:[70,85,125] if form else [80,115],1040:[70,110],1050:[55,70,100],1400:[110],1420:[75,90,115] if form else [70,115],1430:[75,85,110],1440:[80,95,135] if form else [85,120]}[ident]
    for i,(t,v) in enumerate(zip(times,values)):s+=hit(n,t,v+(15 if form and ident in [1000,1020,1040,1050,1400] else 0),i==len(times)-1,low=ident==1400,air=aerial_single or giant or ident==1040,stun=30)
    if ident==1020 and form:s+=cast(n,'Time=8',9502)
    if ident==1040:s+=cast(n,'Time=13',9502)
    if ident==1440:s+=sound(n,'Time=16','Effect/RSGfuton',2)
    if ident==1430:s+=sound(n,'Time=14','Effect/windeffect' if form else 'Effect/mon2',2)+(effect(n,'Time=20',8813,0,0,.65,48,-2) if form else '')
   s+=end(n,max(50,sum(t for _,t in p)),50 if ident==1040 else 0);STATES.append(s)
  n=1060+10000*form;action(n,seq('Skill01',60,60,5)+seq('Idle',1,1,5),form);STATES.append(state(n,n)+c(n,'Ground landing','PosSet','Time=0','y=0')+end(n,10))
def uzuhiko(n,form,cost):
 p=seq('Skill04',82,94,2)+seq('Skill01',60,60,56)
 action(n,p+single(idle(),-1),form,box='5,-78,68,3',active=list(range(13,len(p))))
 s=state(n,n,move='A',physics='N',cost=cost)+startup(n,'BorutoJogan/04')+c(n,'Clear spiral contact clock','VarSet','Time=0','v=22\nvalue=-1')+cast(n,'Time=0 && NumHelper(9561)=0',9561,0,0)
 s+=c(n,'Close with the rotating chakra','VelSet','Time>=20 && Time<50 && !MoveContact','x=IfElse(P2Dist X>42,8,0)')+c(n,'Plant feet on palm contact','VelSet','MoveContact || Time>=50','x=0')
 first=105 if form else 75;step=45 if form else 35
 s+=hit(n,28,first,ident=1030,stun=85)+'p2stateno=3020\np2getp1state=1\n'
 s+=c(n,'Remember real palm contact','VarSet','MoveHit && NumTarget(1030)>0 && Var(22)<0','v=22\nvalue=Time')
 s+=c(n,'Wind at the hand','Explod','Time=23','anim=8816\npostype=P1\npos=42,-45\nscale=.23,.23\nbindtime=-1\nremovetime=48\nsprpriority=3\nownpal=1\nremoveongethit=1')
 s+=c(n,'Original tornado only after real contact','Explod','Var(22)>=0 && Time=Var(22)+1 && NumTarget(1030)>0','ID=9570\nanim=8817\npostype=P1\npos=58,0\nscale=.08,.08\nbindtime=-1\nremovetime=42\nsprpriority=-1\nownpal=1\nremoveongethit=1')
 s+=c(n,'Tornado grows around the struck opponent','ModifyExplod','Var(22)>=0 && Time>Var(22) && Time<=Var(22)+7','ID=9570\nscale=IfElse(Var(42),.55,.45)*IfElse(Time-Var(22)>=6,1,(Time-Var(22))/6.0),IfElse(Var(42),.55,.45)*IfElse(Time-Var(22)>=6,1,(Time-Var(22))/6.0)')
 s+=c(n,'Finite rotational impact','TargetBind','Var(22)>=0 && NumTarget(1030)>0 && Time-Var(22)<42','ID=1030\ntime=1\npos=58+8*Sin(Time*.3),-12-10*Abs(Sin(Time*.3))')
 for delay in [6,14,22,30]:
  when=f'Var(22)>=0 && Time=Var(22)+{delay} && NumTarget(1030)>0'
  s+=c(n,'Rotation after confirmed contact','TargetLifeAdd',when,f'ID=1030\nvalue=-{step}\nabsolute=1\nkill=1')+c(n,'Count spiral impact','HitAdd',when,'value=1')+effect(n,when,8700,58,-40,.5,8)+sound(n,when,'Effect/windeffect',2)
 s+=c(n,'Release the spinning opponent','TargetState','Var(22)>=0 && Time=Var(22)+42 && NumTarget(1030)>0','ID=1030\nvalue=3021')+end(n,100);STATES.append(s)
def futon_rasengan(n,form,cost):
 p=seq('Skill01',1,16,2)+seq('Skill03',55,55,18);action(n,p+single(idle(),-1),form)
 STATES.append(state(n,n,move='A',physics='N',cost=cost)+startup(n,'BorutoJogan/01')+sound(n,'Time=6','Effect/RsgAura',2)+cast(n,'Time=30',9505,35,-38)+sound(n,'Time=30','Effect/RSGfuton',2)+end(n,60))
def mokuton(n,cost):
 p=seq('Skill05',1,4,4)+seq('Skill05',23,25,4);action(n,p+single(idle(),-1),1)
 STATES.append(state(n,n,move='A',physics='N',cost=cost)+startup(n,'BorutoJogan/05')+cast(n,'Time=14',9540,'IfElse(P2Dist X<60,60,IfElse(P2Dist X>220,220,P2Dist X))',0)+sound(n,'Time=14','Effect/monster',2)+end(n,85))
def helpers():
 for n,anim,damage,speed,size in [(9500,8800,85,11,'.9,.9'),(9501,8801,125,9,'.65,.65'),(9502,8802,75,9,'.65,.65'),(9503,8803,100,10,'.6,.6'),(9504,8804,205,10,'.55,.55')]:
  s=state(n,anim,'A','A','N',vel=f'{speed},0')+c(n,'Standalone projectile size','AngleDraw','1','scale='+size)+c(n,'No push','PlayerPush','1','value=0')+hit(n,0,damage,n not in [9500,9501],air=True,projectile=True)
  if n==9501:s+=c(n,'Original Rasengan burst on real contact','ChangeState','MoveContact','value=9511\nctrl=0')
  s+=c(n,'Finite projectile','DestroySelf',('' if n==9501 else 'MoveContact || ')+'Time>=50 || RoundState!=2');STATES.append(s)
 STATES.append(state(9511,8805,'A','I','N',vel='0,0')+c(9511,'Original Rasengan impact size','AngleDraw','1','scale=.23,.23')+c(9511,'No impact push','PlayerPush','1','value=0')+sound(9511,'Time=0','Effect/rasenS',2,65)+c(9511,'Finite non damaging burst','DestroySelf','AnimTime=0 || Time>=16 || RoundState!=2'))
 STATES.append(state(9505,8820,'A','A','N',vel='10,0')+c(9505,'Original green Futon sphere size','AngleDraw','1','scale=IfElse((Root,Var(42)),.85,.65),IfElse((Root,Var(42)),.85,.65)')+c(9505,'No projectile push','PlayerPush','1','value=0')+hit(9505,0,'IfElse((Root,Var(42)),240,205)',True,air=True,projectile=True)+c(9505,'Green burst on actual contact','ChangeState','MoveContact','value=9512\nctrl=0')+c(9505,'Finite green Rasengan flight','DestroySelf','Time>=50 || RoundState!=2'))
 STATES.append(state(9512,8821,'A','I','N',vel='0,0')+c(9512,'Green impact at the opponents feet','PosSet','Time=0 && NumEnemy>0','y=EnemyNear,Pos Y')+c(9512,'Original green impact scale','AngleDraw','1','scale=.65,.65')+c(9512,'See the struck opponent','SprPriority','1','value=-1')+c(9512,'No impact push','PlayerPush','1','value=0')+sound(9512,'Time=0','Effect/RSGfuton',2,70)+c(9512,'Finite green impact','DestroySelf','AnimTime=0 || Time>=26 || RoundState!=2'))
 s=state(9540,8822,'S','A','N',vel='0,0')+c(9540,'Original four Mokuton creatures','AngleDraw','1','scale=.55,.55')+c(9540,'Dragons behind the actual victim','SprPriority','1','value=-1')+c(9540,'No creature push','PlayerPush','1','value=0')
 for t,d in [(9,90),(21,105),(33,150)]:s+=hit(9540,t,d,t==33,projectile=True,stun=30)+sound(9540,f'Time={t}','Effect/BugPillar',2,65)
 STATES.append(s+c(9540,'Finite Mokuton attack','DestroySelf','Time>=54 || RoundState!=2 || (Root,Life)<=0'))
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
 STATES.append(state(9561,8815,'A','I','N')+c(9561,'Wind wraps actual caster','BindToRoot','1','time=1\npos=0,-43')+c(9561,'Torso sized rotation','AngleDraw','1','scale=.24,.24')+c(9561,'Bright original chakra ribbons','Trans','1','trans=addalpha\nalpha=256,256')+c(9561,'Visible wind over the coat','SprPriority','1','value=3')+c(9561,'No push from chakra','PlayerPush','1','value=0')+c(9561,'Stop with actual technique','DestroySelf','RoundState!=2 || (Root,Life)<=0 || (Root,StateNo)%10000!=1030'))
 STATES.append(state(520,520)+startup(520,'BorutoJogan/05')+effect(520,'Time=12',8810,0,-135,.28,20)+sound(520,'Time=12','Effect/RaitonEfx',2)+c(520,'Pay resonance','PowerAdd','Time=47','value=-1500')+c(520,'Karma and Jogan resonance','VarSet','Time=47','v=42\nvalue=1')+c(520,'Twenty second resonance','VarSet','Time=47','v=40\nvalue=1200')+c(520,'Resonance cooldown','VarSet','Time=47','v=41\nvalue=1500')+end(520,62))
def ultimate():
 for form in [0,1]:
  n=3000+10000*form;p=seq('Skill05',23,25,6)+seq('Skill05',26,47,2)+seq('Skill05',56,57,2)+seq('Skill05',63,63,6)+seq('Skill05',111,124,2)+seq('Skill05',73,110,2)+seq('Skill05',141,148,2)+seq('Skill05',149,163,3)+seq('Skill05',164,177,2)+single(idle(),40)
  attack(n,p,form,'5,-100,180,5');s=state(n,n,move='A',physics='N',cost=3000)+startup(n,'BorutoJogan/05')+c(n,'See the victim inside the original effects','SprPriority','1','value=-1')+c(n,'No cinematic push','PlayerPush','1','value=0')+c(n,'Clear confirmed hit','VarSet','Time=0','v=21\nvalue=0')+hit(n,18,0,ident=3000,stun=330)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Remember actual target position','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite Jogan damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{800 if form else 650},Floor((Target(3000),LifeMax)*{.8 if form else .65}))')+c(n,'Confirm contact','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(n,'Approach actual target','PosSet','Time=40 && NumTarget(3000)>0','x=FVar(0)-Facing*90')+c(n,'Caster lifts with the lightning','PosSet','Time>=72 && Time<100','y=-60')+c(n,'Return from lightning before wind','PosSet','Time=100','y=0')+c(n,'Real double Rasengan takeoff','PosSet','Time>=176 && Time<192','y=-90*(Time-176)/16')+c(n,'Double Rasengan sphere contact height','PosSet','Time>=192 && Time<257','y=-90')+c(n,'Land with the final source frames','PosSet','Time>=257 && Time<275','y=-90+5*(Time-257)')+c(n,'Feet back on stage','PosSet','Time>=275','y=0')+c(n,'Hold opponent inside the actual ground effect','TargetBind','NumTarget(3000)>0 && Time<280','ID=3000\ntime=1\npos=(FVar(0)-Pos X)*Facing,-Pos Y')+effect(n,'Time=62 && NumTarget(3000)>0',8810,0,-135,.28,20)+effect(n,'Time=100 && NumTarget(3000)>0',8813,0,0,.65,48,-2)
  for i,t in enumerate(PULSES):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)'
   s+=c(n,'Confirmed impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count actual pulse','HitAdd',when,'value=1')+effect(n,when,8700,'(FVar(0)-Pos X)*Facing',-35,.8,9)+sound(n,when,'Effect/BladeA',2)
  s+=sound(n,'Time=184 && NumTarget(3000)>0','Effect/rasenS',2)+sound(n,'Time=244 && NumTarget(3000)>0','Effect/RSGfuton',4)+effect(n,'Time=244 && NumTarget(3000)>0',8814,'(FVar(0)-Pos X)*Facing','-Pos Y',.4,51)+c(n,'Release rival','TargetState','Time=280 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,310);STATES.append(s)
 STATES.append(state(3010,None,'S','H','N')+c(3010,'Retain opponent artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Independent victim release','SelfState','trigger1=Time>=350\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3011,None,'A','H','N')+c(3011,'Release motion','VelSet','Time=0','x=-4\ny=-6')+c(3011,'Return opponent state ownership','SelfState','1','value=5050\nctrl=0'))
 STATES.append(state(3020,None,'A','H','N')+c(3020,'Retain victim artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+c(3020,'Uzuhiko rotational reaction','AngleDraw','1','value=Time*18')+ctl(3020,'Independent spiral escape','SelfState','trigger1=Time>=90\ntrigger2=NumEnemy=0\ntrigger3=(EnemyNear,StateNo)%10000!=1030\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3021,None,'A','H','N')+c(3021,'Spiral release velocity','VelSet','Time=0','x=-5\ny=-5')+c(3021,'Restore victim state ownership','SelfState','1','value=5050\nctrl=0'))
def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite resonance timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 return s+c(-2,'Safe resonance expiry','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Restore base animation bank','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && SelfAnimExist(Anim-10000)','value=Anim-10000')+c(-2,'Resonance animation bank','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+cast(-2,'!IsHelper && RoundState=2 && Var(42)=1 && NumHelper(9560)=0',9560,0,0)+c(-2,'Karma strength','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.18,1)')+c(-2,'Reset air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+sound(-2,'!IsHelper && MoveType=H && Time=0 && StateNo=5000','BorutoJogan/hurt1',0,70)+c(-2,'Stop released charge sound','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Round resonance cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')
def main():
 global KEY,SOUNDS,SPRITES
 SPRITES={r['key']:r for r in json.loads((CHAR/'assets/sprites.json').read_text())}
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
