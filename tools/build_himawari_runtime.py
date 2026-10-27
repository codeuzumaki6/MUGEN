#!/usr/bin/env python3
"""Himawari TBV: original Juken, taijutsu, Kurama claws and Bijudama."""
from pathlib import Path
import json,re
from build_sumire_runtime import ctl,c,state,hit,end,common_sound,single
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'HimawariTBV';AIR=[];STATES=[];KEY={};SOUNDS={};BOXES={}
MOVES=[('Patada','a','F',1000,350),('Juken','a','B',1010,400),('Tenketsu','b','F',1020,450),('Combo','b','B',1030,550),('Ascendente','c','F',1040,350),('Contraataque','c','B',1050,450),('Barrido','a','D',1400,200),('Palmas','b','D',1410,300),('Caida','c','D',1420,400),('Vacio','y','N',1200,250),('Impacto','z','N',1210,300),('Byakugan','y','D',1430,450),('Bijudama','z','D',1440,600)]
def seq(stem,a,b,t=3):return [(f'KinkakuET_{stem}_{i:02}',t) for i in range(a,b+1)]
def idle(form):return 'KinkakuET_kyubiCKRStance_01' if form else 'KinkakuET_Idle_01'
def action(n,poses,form=0,box=None,active=None,hurt=True,loop=False,add=False,hurt_box=None):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+ (hurt_box or '-14,-68,16,0')+'\n'
 if loop:s+='Loopstart\n'
 for i,(key,t) in enumerate(poses):
  if box and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+box+'\n'
  if hurt and not hurt_box and BOXES.get(key):s+='Clsn2: 1\n Clsn2[0]='+','.join(map(str,BOXES[key]))+'\n'
  g,p=KEY[key];s+=f'{g},{p},0,0,{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def attack(n,p,form,box='-5,-70,105,3'):action(n,p+single(idle(form),-1),form,box=box,active=list(range(len(p))))
def sound(n,when,name,channel=0,volume=80):
 g,p=SOUNDS[name];return c(n,'Original supplied Himawari audio','PlaySnd',when,f'value=S{g},{p}\nchannel={channel}\nvolumescale={volume}')
def startup(n,voice='HimawariTBV/Skil'):
 return common_sound(n,'Time=0')+sound(n,'Time=0',voice)+c(n,'Activation focus','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')
def effect(n,when,anim,x=0,y=-35,scale=1,ticks=-2,priority=4):
 return c(n,'Original standalone effect','Explod',when,f'anim={anim}\npostype=P1\npos={x},{y}\nscale={scale},{scale}\nremovetime={ticks}\nbindtime=1\nsprpriority={priority}\nownpal=1\nremoveongethit=1')
def cast(n,when,ident,x=30,y=-32):return c(n,'Separate chakra projectile','Helper',when,f'helpertype=Normal\nname="Himawari chakra"\nID={ident}\nstateno={ident}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def basic():
 base={0:seq('Idle',1,3,10),5:seq('Idle',1,1,8),6:seq('Down',1,1,8),10:seq('Down',1,1,6),11:seq('Down',1,1,8),12:seq('Idle',1,1,6),20:seq('Walk',1,6,4),21:list(reversed(seq('Walk',1,6,4))),100:seq('Walk',1,6,2),105:list(reversed(seq('Walk',1,6,2))),40:seq('CHGKICK',1,1,6),41:seq('AirHurt',1,2,6),44:seq('Float',1,1,8),52:seq('Down',1,3,4)+seq('Idle',1,1,4),170:seq('KnockDown',2,2,30),180:seq('Idle',1,3,12),190:seq('Idle',1,3,12),500:seq('Skill05',1,1,8),520:seq('Skill05',1,1,12)+seq('Trans',1,7,5),5000:seq('Hurt',1,2,6),5010:seq('Hurt',1,2,6),5020:seq('AirHurt',1,2,6),5030:seq('Float',1,1,8),5100:seq('KnockDown',1,2,8),5110:seq('KnockDown',2,2,28),5120:seq('KnockDown',3,4,8)+seq('Idle',1,1,5),5150:seq('KnockDown',2,2,60),5200:seq('AirHurt',1,1,8),5210:seq('AirHurt',2,2,8),5300:seq('Hurt',1,1,20)}
 for n in [120,130,140,150,121,131,141,151,122,132,142,152]:base[n]=seq('JknChg',1,1,6)
 for form in [0,1]:
  for n,p in base.items():
   if form:
    p=seq('kyubiCKRStance',1,3,8) if n in [0,5,11,180,190,500] else seq('kyubiCKRCHG',1,1,max(6,sum(t for _,t in p)))
   action(n+form*10000,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-34,-24,37,0' if not form and n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:action(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 action(8800,[(f'Waver_{i:02}',4) for i in range(1,4)],hurt=False,box='-20,-25,24,25',loop=True,add=True)
 action(8801,seq('kyubiUlti',1,8,3),hurt=False,box='-30,-30,40,30')
 action(8802,[(f'ByakuganEye_{i:02}',4) for i in range(1,4)],hurt=False)
 action(8803,[(f'Bombard_{i:02}',2) for i in range(1,26)],hurt=False,add=True)
 action(8804,[(f'Duar_Move_{i:02}',3) for i in range(1,18)],hurt=False)
def normals():
 for form in [0,1]:
  poses=[seq('NAttack',1,3,3),seq('NAttack',4,6,3),seq('NAttack',7,9,3)] if not form else [seq('kyubiCKRCLAW01',1,3,3),seq('kyubiCKRCLAW01',4,6,3),seq('kyubiCKRCLAW02',1,4,3)]
  for family in [200,210,220,600,610,620]:
   air=family>=600
   for step in range(3):
    n=family+step+form*10000;p=poses[(step+(family%100)//10)%3];attack(n,p,form,'-5,-70,115,3' if form else '-5,-67,90,3')
    s=state(n,n,'A' if air else 'S','A','N' if air else 'S',vel=None if air else '2,0')+sound(n,'Time=0',f'HimawariTBV/hit{step+1}',volume=75)+hit(n,3,([45,60,80] if form else [36,48,66])[step],step==2,air=air,stun=15)
    if air:s+=c(n,'Count air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief air approach','VelSet','Time<7','x=2\ny=-.4')+c(n,'Air gravity','VelAdd','Time>=7','y=.48')+c(n,'Grounded landing','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
    else:s+=c(n,'End normal approach','VelSet','Time>=8','x=0')
    STATES.append(s+end(n,21 if air else 24,50 if air else 0))
def specials():
 base={1000:seq('CHGKICK',1,1,6)+seq('FlyKick',1,3,4)*2+seq('FlyKick',4,4,6),1010:seq('JknChg',1,1,8)+seq('Jkn',1,6,3)*2,1020:seq('Lock',1,1,8)+seq('TksuChg',1,1,5)+seq('Tksu',1,7,4),1030:seq('CHGKICK',1,1,5)+seq('ComKick01',1,4,3)+seq('ComKick02',1,4,3)+seq('ComKick03',1,6,3)+seq('Down',1,3,3),1040:seq('NAttack',7,7,4)+seq('ComKick02',1,4,4),1050:seq('ComKick03',1,1,9)+seq('NAttack',7,9,5),1400:seq('NAttack',4,6,5),1410:seq('NAttack',1,6,4),1420:seq('CHGKICK',1,1,5)+seq('FlyKick',4,4,7)+seq('ComKick03',2,6,4)+seq('Down',1,3,3),1200:seq('JknChg',1,1,7)+seq('NAttack',2,3,8),1210:seq('TksuChg',1,1,8)+seq('Tksu',1,7,4),1430:seq('Lock',1,1,8)+seq('Walk',1,6,3)+seq('NAttack',2,3,5),1440:seq('BidamCHG',1,7,4)+seq('BidamATK',1,8,4)}
 awake={1000:seq('kyubiCKRCHG',1,1,6)+seq('kyubiCKRCLAW01',1,6,4),1010:seq('kyubiCKRCLAW02',1,4,6),1020:seq('kyubiCKRCLAW01',1,6,3)+seq('kyubiCKRCLAW02',1,4,4),1030:seq('kyubiCKRCHG',1,1,5)+seq('kyubiCKRCLAW01',1,6,4),1040:seq('kyubiCKRCLAW02',1,4,5),1050:seq('kyubiCKRCHG',1,1,9)+seq('kyubiCKRCLAW01',1,6,4),1400:seq('kyubiCKRCLAW01',4,6,5),1410:seq('kyubiCKRCLAW02',1,4,4)+seq('kyubiCKRCLAW01',1,3,4),1420:seq('kyubiUltiBom',1,7,4),1200:seq('kyubiCKRStance',1,3,8),1210:seq('kyubiCKRCLAW02',1,4,5),1430:seq('kyubiCKRCLAW01',1,6,3)*3,1440:base[1440]}
 for form in [0,1]:
  for name,b,d,ident,cost in MOVES:
   n=ident+form*10000;p=(awake if form else base)[ident];box='-5,-70,115,3' if form else '-5,-68,100,3'
   if ident in [1020,1210]:box='-5,-80,155,5'
   if ident==1400:box='-5,-35,105,3'
   if ident==1420 and form:box='-90,-85,125,5'
   if ident==1440:box='25,-90,290,5'
   attack(n,p,form,box);s=state(n,n,move='A',physics='N',cost=cost)+startup(n,'HimawariTBV/02' if ident==1440 else 'HimawariTBV/lock' if ident in [1010,1020,1430] else 'HimawariTBV/Skil')
   if ident in [1000,1010,1020,1030,1040,1050,1430]:
    start=9 if ident==1050 else 6;stop=25 if ident==1430 else 22
    s+=c(n,'Actual approach','VelSet',f'Time>={start} && Time<{stop} && !MoveContact','x='+('8' if ident in [1000,1430] else '5'))+c(n,'Brake after contact','VelSet',f'MoveContact || Time>={stop}','x=0')
    if ident==1050:s+=c(n,'Counterstep retreat','VelSet','Time<9','x=-4')
   if ident in [1030,1040,1420] and not (form and ident==1420):
    s+=c(n,'Real jump','VelSet','Time=4','x=4\ny=-6.5')+c(n,'Airborne strike','StateTypeSet','Time=4','statetype=A\nphysics=N')+c(n,'Gravity','VelAdd','Time>4','y=.46')+c(n,'Original landing','ChangeState','Time>20 && Pos Y>=0 && Vel Y>0','value='+str(1060+form*10000)+'\nctrl=0')
   if ident==1200:s+=cast(n,'Time=9',9501 if form else 9500)+sound(n,'Time=9','Effect/Blade-Damage' if form else 'Effect/hyper_punch',2)
   elif ident==1440:
    s+=hit(n,29,100 if form else 80,stun=28)+hit(n,43,185 if form else 145,True)+sound(n,'Time=0','Effect/charge2',2)+sound(n,'Time=29','Effect/BijuDama',2)
   else:
    times={1000:[8,21],1010:[10,22,34],1020:[14,27],1030:[7,18,28],1040:[5,15],1050:[12,22],1400:[5],1410:[4,16],1420:[13,25],1210:[10,22],1430:[15,29] }[ident]
    values={1000:[75,100],1010:[50,55,85],1020:[80,120],1030:[55,65,95],1040:[65,105],1050:[65,110],1400:[105],1410:[55,95],1420:[75,110],1210:[65,100],1430:[70,115]}[ident]
    for i,(t,v) in enumerate(zip(times,values)):s+=hit(n,t,v+(15 if form else 0),i==len(times)-1,low=ident==1400,air=ident in [1030,1040,1420] and not (form and ident==1420),stun=28)
    if ident in [1010,1020]:
     s+=effect(n,'Time=1',8802,0,-85,.25,12)+c(n,'Juken disrupts confirmed chakra','TargetPowerAdd','Time=35 && NumTarget>0','value=-180')+sound(n,'Time=1','Effect/baiyan',2)
   duration=max(48,sum(t for _,t in p));s+=end(n,duration,50 if ident in [1030,1040,1420] and not (form and ident==1420) else 0);STATES.append(s)
  n=1060+10000*form;action(n,seq('kyubiCKRStance',1,3,4) if form else seq('Down',1,3,4),form);STATES.append(state(n,n)+c(n,'Land at ground','PosSet','Time=0','y=0')+end(n,12))
def utility():
 for n in [170,180,190]:
  s=state(n,n)+sound(n,'Time=0','HimawariTBV/die' if n==170 else 'HimawariTBV/hima')
  if n==190:s+=c(n,'Intro','AssertSpecial','Time<36','flag=Intro')+end(n,40)
  STATES.append(s)
 STATES.append(state(500,500)+c(500,'Real chakra charge','PowerAdd','1','value=20')+sound(500,'Time=0','HimawariTBV/chg')+cast(500,'Time=0 && NumHelper(9551)=0',9551,0,0)+ctl(500,'Release energy charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 STATES.append(state(9551,8900,'A','I','N')+c(9551,'Aura follows real body','BindToRoot','1','time=1\npos=0,-35')+c(9551,'Gold and red Kurama aura','PalFX','1','time=1\ncolor=0\nmul=256,IfElse((Root,Var(42)),65,200),35')+c(9551,'Aura size','AngleDraw','1','value=90\nscale=.32,.36')+c(9551,'Aura behind Himawari','SprPriority','1','value=-2')+c(9551,'Finite charge aura','DestroySelf','(Root,StateNo)!=500 || RoundState!=2'))
 STATES.append(state(520,520)+startup(520,'HimawariTBV/02')+sound(520,'Time=12','Effect/Biju mode',2)+c(520,'Pay Kurama awakening','PowerAdd','Time=47','value=-1500')+c(520,'Awaken Kurama','VarSet','Time=47','v=42\nvalue=1')+c(520,'Twenty second Kurama mode','VarSet','Time=47','v=40\nvalue=1200')+c(520,'Kurama cooldown','VarSet','Time=47','v=41\nvalue=1500')+end(520,62))
 for n,anim,damage,speed,size in [(9500,8800,125,10,'.3,.3'),(9501,8801,175,12,'.4,.4')]:
  STATES.append(state(n,anim,'A','A','N',vel=f'{speed},0')+c(n,'Projectile scale','AngleDraw','1','scale='+size)+c(n,'No projectile push','PlayerPush','1','value=0')+hit(n,0,damage,True,air=True,projectile=True)+c(n,'Finite original projectile','DestroySelf','MoveContact || Time>=42 || RoundState!=2'))
def ultimate():
 for form in [0,1]:
  n=3000+10000*form;p=(seq('kyubiCKRStance',1,3,6) if form else seq('Skill05',1,1,18))+seq('Trans',1,7,4)+seq('kyubiCKRCLAW01',1,6,4)+seq('kyubiCKRCLAW02',1,4,4)*3+seq('kyubiUltiBom',1,7,4)+seq('BidamCHG',1,7,5)+seq('BidamATK',1,8,4)+single(idle(form),40)
  attack(n,p,form,'5,-80,180,5');s=state(n,n,move='A',physics='N',cost=3000)+startup(n,'HimawariTBV/02')+c(n,'No cinematic push','PlayerPush','1','value=0')+c(n,'Clear confirmed contact','VarSet','Time=0','v=21\nvalue=0')+hit(n,18,0,ident=3000,stun=260)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Remember true target position','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite Kurama damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{750 if form else 600},Floor((Target(3000),LifeMax)*{.75 if form else .6}))')+c(n,'Confirm contact','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(n,'Approach confirmed opponent','PosSet','Time=40 && NumTarget(3000)>0','x=FVar(0)-Facing*55')+c(n,'Hold confirmed opponent','TargetBind','NumTarget(3000)>0 && Time<236','ID=3000\ntime=1\npos=(FVar(0)-Pos X)*Facing,0')
  for i,t in enumerate([44,64,84,104,124,144,164,184]):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)'
   s+=c(n,'Confirmed Kurama impact','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count actual pulse','HitAdd',when,'value=1')+effect(n,when,8700,'(FVar(0)-Pos X)*Facing',-30,.8,9)+sound(n,when,'Effect/Blade-Damage',2)
  s+=effect(n,'Time=80 && NumTarget(3000)>0',8801,'(FVar(0)-Pos X)*Facing',-45,.5,24)+sound(n,'Time=153 && NumTarget(3000)>0','Effect/charge2',2)+sound(n,'Time=181 && NumTarget(3000)>0','Effect/BijuDama',2)+effect(n,'Time=184 && NumTarget(3000)>0',8803,'(FVar(0)-Pos X)*Facing',0,.48,50,2)+effect(n,'Time=184 && NumTarget(3000)>0',8804,'(FVar(0)-Pos X)*Facing',0,.4,51,3)+sound(n,'Time=184 && NumTarget(3000)>0','Effect/explosion1',4)+c(n,'Release rival','TargetState','Time=236 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,260);STATES.append(s)
 STATES.append(state(3010,None,'S','H','N')+c(3010,'Keep opponent artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+ctl(3010,'Independent victim release','SelfState','trigger1=Time>=290\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3000\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 STATES.append(state(3011,None,'A','H','N')+c(3011,'Release velocity','VelSet','Time=0','x=-4\ny=-6')+c(3011,'Return state ownership','SelfState','1','value=5050\nctrl=0'))
def system():
 s='\n[Statedef -2]\n'
 for v in [40,41]:s+=c(-2,'Finite Kurama timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe awakening expiry','VarSet','!IsHelper && Var(42)=1 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Restore base body','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && SelfAnimExist(Anim-10000)','value=Anim-10000')+c(-2,'Kurama full body','ChangeAnim','!IsHelper && Var(42)=1 && StateNo!=520 && Anim<10000 && SelfAnimExist(Anim+10000)','value=Anim+10000')+c(-2,'Kurama physical strength','AttackMulSet','!IsHelper','value=IfElse(Var(42),1.15,1)')+c(-2,'Reset grounded air chain','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+sound(-2,'!IsHelper && MoveType=H && Time=0 && StateNo=5000','HimawariTBV/hurt',0,70)+c(-2,'Round form cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190','v=42\nvalue=0')+c(-2,'Round effect cleanup','RemoveExplod','!IsHelper && RoundState!=2')
 return s
def main():
 global KEY,SOUNDS,BOXES
 KEY=json.loads((CHAR/'assets/keys.json').read_text());SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];BOXES={r['key']:r.get('collision_box') for r in json.loads((CHAR/'assets/sprites.json').read_text())};basic();normals();specials();utility();ultimate()
 import build_sarada_runtime as ref
 saved=ref.CHAR,ref.MOVES
 try:ref.CHAR=CHAR;ref.MOVES=MOVES;ref.commands()
 finally:ref.CHAR,ref.MOVES=saved
 p=CHAR/'SaradaTBV.cmd';(CHAR/'HimawariTBV.cmd').write_text(p.read_text().replace('Pink Susanoo awakening','Kurama awakening'));p.unlink()
 const=(ROOT/'SumireKakei/SumireKakei.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):].replace('height=75','height=68').replace('head.pos=0,-72','head.pos=0,-62').replace('mid.pos=0,-42','mid.pos=0,-34')
 (CHAR/'HimawariTBV.cns').write_text('; Original Himawari TBV and Kurama moves.\n'+const+(''.join(STATES)+system()).rstrip()+'\n');(CHAR/'HimawariTBV.air').write_text('; Original bodies only on the main player.\n'+''.join(AIR).rstrip()+'\n');(CHAR/'HimawariTBV_common.cns').write_text((ROOT/'SumireKakei/SumireKakei_common.cns').read_text())
 d=(ROOT/'SumireKakei/SumireKakei.def').read_text().replace('SumireKakei','HimawariTBV').replace('Sumire Kakei','Himawari Uzumaki TBV');d=re.sub(r'(?m)^author=.*$','author="Vaydra original sprites and audio / Codex adaptation"',d);(CHAR/'HimawariTBV.def').write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,awakening='Kurama chakra, original long-haired red cloak',awakening_requires=3000,awakening_cost=1500,awakening_ticks=1200,ultimate_damage=[600,750],ultimate_cost=3000,own_life_cost=0),indent=2)+'\n');print('Himawari:',len(STATES),'states;',len(AIR),'animations')
if __name__=='__main__':main()
