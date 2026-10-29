#!/usr/bin/env python3
"""TBV base: original kenjutsu, Shiden, Hiraishin and complete Uzuhiko."""
from pathlib import Path
import json,re
import build_boruto_runtime as b
from build_sumire_runtime import c,ctl,state,hit,end,single
ROOT=Path(__file__).resolve().parents[1];NAME='BorutoTBVBase';CHAR=ROOT/NAME
MOVES=b.MOVES
PULSES=[84,112,140,168,196,224,252,284]
def seq(prefix,a,z,t=3):return [(prefix+'_'+str(i).zfill(3 if prefix=='Hiruzen_NAttack' else 2),t) for i in range(a,z+1)]
def idle(form=0):return 'Hiruzen_Idle_01'
def anim(n,p,form=0,**kw):b.action(n,p,form,**kw)
def voice(n,t,name='01',ch=0):return b.sound(n,t,'BorutoTBv/'+name,ch)
def fx(n,t,key,x=0,y=-40,scale=1,duration=-2,priority=3):return b.effect(n,t,key,x,y,scale,duration,priority)
def start(n,name='01'):return b.startup(n,'BorutoTBv/'+name)
def attack(n,p,form,box='-5,-80,105,5'):anim(n,p+single(idle(),-1),form,box=box,active=list(range(len(p))))
def basic():
 poses={0:seq('Hiruzen_Idle',1,3,10),5:single(idle()),6:single('Hiruzen_Wake_01'),10:single('Hiruzen_Wake_01'),11:single('Hiruzen_Wake_01'),12:single(idle()),20:seq('Hiruzen_Walk',1,6,4),21:list(reversed(seq('Hiruzen_Walk',1,6,4))),100:seq('Hiruzen_Walk',1,6,2),105:list(reversed(seq('Hiruzen_Walk',1,6,2))),40:single('Hiruzen_Float_01'),41:single('Hiruzen_AirHurt_001'),44:single('Hiruzen_Float_01'),52:single('Hiruzen_Wake_01',5)+single(idle(),5),170:single('Hiruzen_Dead_01',30),180:seq('Hiruzen_Idle',1,3,12),190:seq('Hiruzen_Idle',1,3,12),500:seq('HiruzenChg03',1,5,5),520:seq('Hiruzen_Skill05',1,6,6)+seq('Hiruzen_Skill05',7,12,4),5000:seq('Hiruzen_Hurt',1,3,5),5010:seq('Hiruzen_Hurt',1,3,5),5020:single('Hiruzen_AirHurt_001'),5030:single('Hiruzen_Float_01'),5100:single('Hiruzen_Knock_01',8)+single('Hiruzen_Dead_01',8),5110:single('Hiruzen_Dead_01',28),5120:seq('Hiruzen_Wake',1,2,7)+single(idle(),5),5150:single('Hiruzen_Dead_01',60),5200:single('Hiruzen_AirHurt_001'),5210:single('Hiruzen_Float_01'),5300:single('Hiruzen_Hurt_01',20)}
 for n in [120,130,140,150,121,131,141,151,122,132,142,152]:poses[n]=single('Hiruzen_NAttack_001')
 for form in [0,1]:
  for n,p in poses.items():anim(n+10000*form,p,form,loop=n in [0,11,20,21,100,105,41,44,500,5150],hurt_box='-45,-28,45,0' if n in [170,5100,5110,5150] else None)
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:anim(g,[(f'Common_{g}_{i}',3) for i in range(count)],hurt=False,loop=g==8900,add=True)
 for n,p,box,loop in [(8800,seq('BoruBlade',1,6),'-45,-14,45,14',True),(8801,seq('Hiruzen_Skil01',1,4),'-35,-35,35,35',True),(8802,seq('ShidenBlade',6,11),'-65,-28,65,28',True),(8803,seq('ShidenBlade',17,23),'-120,-150,120,3',False),(8804,seq('Hiruzen_04Bom',9,14),None,False),(8805,seq('Hiruzen_Skil01',5,6),None,False),(8817,seq('Hiruzen_Skill05',14,19),None,True)]:anim(n,p,hurt=False,box=box,loop=loop,add=True)
 anim(9700,seq('Hiruzen_Walk',1,6,3),loop=True)
 anim(9701,seq('Hiruzen_skill04',1,4,5)+seq('Hiruzen_NAttack',6,10,3),box='-5,-85,110,5')
 anim(9790,single('Hiruzen_Hurt_01',10))
def normals():
 sets=[[(f'Hiruzen_NAttack_{i:03}',2) for i in range(1,6)],[(f'Hiruzen_NAttack_{i:03}',2) for i in range(6,11)],seq('Hiruzen_skill04',1,4,3)]
 for form in [0,1]:
  for family in [200,210,220,600,610,620]:
   air=family>=600
   for step in range(3):
    n=family+step+form*10000;p=sets[(step+family%100//10)%3];attack(n,p,form)
    s=state(n,n,'A' if air else 'S','A','N' if air else 'S',vel=None if air else '2,0')+voice(n,'Time=0','Hit')+hit(n,3,([45,60,80] if form else [36,48,66])[step],step==2,air=air,stun=15)
    if air:s+=c(n,'Air chain limit','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Air approach','VelSet','Time<7','x=2\ny=-.4')+c(n,'Real gravity','VelAdd','Time>=7','y=.48')+c(n,'Land','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
    else:s+=c(n,'Brake','VelSet','Time>=8','x=0')
    b.STATES.append(s+end(n,21 if air else 25,50 if air else 0))
def specials():
 for form in [0,1]:
  for name,button,direction,base,cost in MOVES:
   n=base+10000*form
   if base==1030:uzuhiko(n,form,cost);continue
   if base==1440:giant(n,form,cost);continue
   p={1000:seq('Hiruzen_Skil01',7,14,4),1010:seq('ShidenBlade',1,5,5),1020:seq('Hiruzen_skill04',1,5,5),1040:[(f'Hiruzen_NAttack_{i:03}',3) for i in range(6,11)],1050:seq('ShidenBlade',12,16,5),1400:[(f'Hiruzen_NAttack_{i:03}',4) for i in range(6,11)],1410:single('Hiruzen_NAttack_001',24),1420:seq('Hiruzen_Skill03Atk',1,13,3),1200:seq('Hiruzen_skill04',1,5,4),1210:single('Hiruzen_NAttack_001',10)+single('Hiruzen_Skil01_14',30),1430:seq('Hiruzen_Skill03Atk',1,5,3)+seq('Hiruzen_Skill03Atk',6,13,3)}[base]
   box='-10,-85,110,5'
   if base==1000:box='5,-100,190,5'
   if base==1050:box='-30,-100,155,5'
   if base==1400:box='-5,-40,105,5'
   if base in [1010,1410,1200,1210]:box=None
   if base==1420:box='-35,-30,95,85'
   attack(n,p,form,box);s=state(n,n,move='A',physics='N',cost=cost)+start(n,'02' if base in [1010,1050] else '04' if base in [1420,1430] else '03' if base==1410 else '01')
   if base==1000:s+=c(n,'Rasengan forward pressure','VelSet','Time<24 && !MoveContact','x=IfElse(P2Dist X>80,4,0)')+hit(n,6,210 if form else 165,stun=28)+hit(n,20,90 if form else 70,True)
   elif base==1010:s+=b.cast(n,'Time=15',9505,65,-40)+b.sound(n,'Time=15','Effect/Chidori2',2)
   elif base in [1200,1210]:s+=b.cast(n,'Time=10',9500 if base==1200 else 9501,45,-38)+b.sound(n,'Time=10','Effect/shuriken' if base==1200 else 'Effect/rasenS',2)
   elif base==1410:s+=b.cast(n,'Time=8 && NumHelper(9700)=0',9700,-25,0)+c(n,'Clone order','VarAdd','Time=10','v=45\nvalue=1')
   elif base==1420:
    s+=c(n,'Actual airborne strike','PosSet','Time>=9 && Time<32','y=-45')+c(n,'Aerial approach','VelSet','Time>=8 && Time<27 && !MoveContact','x=5')+hit(n,18,265 if form else 205,True,air=True)+c(n,'Return to stage','PosSet','Time>=32','y=0')
   elif base==1430:
    s+=c(n,'Finite Hiraishin displacement','PosAdd','Time=12','x=IfElse(P2Dist X>300,235,IfElse(P2Dist X>65,P2Dist X-65,0))')+fx(n,'Time=12',8700,0,-40,.7,10)+b.sound(n,'Time=12','Effect/hiraishin_effect2',2)+hit(n,18,260 if form else 210,True)
   else:
    s+=c(n,'Approach with katana','VelSet','Time<15 && !MoveContact','x='+('6' if base==1020 else '2'))+hit(n,5,150 if form else 120,low=base==1400)+hit(n,16,120 if form else 90,True,low=base==1400)
    if base==1050:s+=b.cast(n,'Time=20',9503,90,0)+b.sound(n,'Time=20','Effect/BugPillar',2)
   s+=c(n,'Stop after contact','VelSet','MoveContact || Time>=30','x=0')+end(n,65 if base in [1000,1420,1430] else 55);b.STATES.append(s)
def uzuhiko(n,form,cost):
 p=seq('Hiruzen_Skill05',1,6,2)+seq('Hiruzen_Skill05',7,12,3)+single('Hiruzen_Skill05_13',70);attack(n,p,form,'5,-78,95,5')
 s=state(n,n,move='A',physics='N',cost=cost)+start(n,'005')+c(n,'Clear contact clock','VarSet','Time=0','v=22\nvalue=-1')+c(n,'Real palm approach','VelSet','Time>=22 && Time<55 && !MoveContact','x=IfElse(P2Dist X>42,6,0)')+c(n,'Plant feet','VelSet','MoveContact || Time>=55','x=0')+hit(n,31,105 if form else 75,ident=1030,stun=85)+'p2stateno=3020\np2getp1state=1\n'
 s+=c(n,'Remember confirmed palm hit','VarSet','MoveHit && NumTarget(1030)>0 && Var(22)<0','v=22\nvalue=Time')+c(n,'Original tornado after contact','Explod','Var(22)>=0 && Time=Var(22)+1 && NumTarget(1030)>0',f'ID=9570\nanim=8817\npostype=P1\npos=60,0\nscale={.55 if form else .45},{.55 if form else .45}\nbindtime=-1\nremovetime=42\nsprpriority=-1\nownpal=1\nremoveongethit=1')+c(n,'Finite spinning reaction','TargetBind','Var(22)>=0 && NumTarget(1030)>0 && Time-Var(22)<42','ID=1030\ntime=1\npos=60,-15-8*Abs(Sin(Time*.3))')
 for delay in [6,14,22,30]:s+=c(n,'Uzuhiko rotation','TargetLifeAdd',f'Var(22)>=0 && Time=Var(22)+{delay} && NumTarget(1030)>0',f'ID=1030\nvalue=-{45 if form else 35}\nabsolute=1\nkill=1')
 s+=c(n,'Release target','TargetState','Var(22)>=0 && Time=Var(22)+42 && NumTarget(1030)>0','ID=1030\nvalue=3021')+end(n,110);b.STATES.append(s)
def giant(n,form,cost):
 p=seq('Hiruzen_04Chg',1,2,4)+seq('Hiruzen_04Chg',3,10,3)+seq('Hiruzen_04Hit',1,6,4)+seq('Hiruzen_04Bom',1,8,3)
 anim(n,p+single(idle(),-1),form,box='-75,15,75,135',active=list(range(10,16)))
 s=state(n,n,move='A',physics='N',cost=cost)+start(n,'03')+c(n,'Close before descending','PosAdd','Time=8','x=IfElse(P2Dist X>250,180,IfElse(P2Dist X>55,P2Dist X-55,0))')+c(n,'Lift with the actual Rasengan pose','PosSet','Time>=24 && Time<72','y=-100')+hit(n,36,330 if form else 260,True,air=True)+fx(n,'MoveHit && Time=48',8804,55,100,.45,20,-1)+b.sound(n,'Time=36','Effect/rasenS',2)+c(n,'Land after impact','PosSet','Time>=72','y=0')+end(n,90);b.STATES.append(s)
def helpers():
 for n,a,damage,speed,size in [(9500,8800,100,11,.4),(9501,8801,145,9,.45),(9505,8802,205,9,.45),(9503,8803,100,0,.5)]:
  s=state(n,a,'A','A','N',vel=f'{speed},0')+c(n,'Original independent effect scale','AngleDraw','1',f'scale={size},{size}')+c(n,'No physical push','PlayerPush','1','value=0')+hit(n,0,f'IfElse((Root,Var(42)),{round(damage*1.25)},{damage})',True,air=True,projectile=True)
  if n==9501:s+=c(n,'Original Rasengan burst','ChangeState','MoveContact','value=9511\nctrl=0')
  b.STATES.append(s+c(n,'Finite projectile','DestroySelf',('' if n==9501 else 'MoveContact || ')+'Time>=55 || RoundState!=2'))
 b.STATES.append(state(9511,8805,'A','I','N')+c(9511,'Burst size','AngleDraw','1','scale=.45,.45')+c(9511,'Finite non damaging burst','DestroySelf','Time>=6 || RoundState!=2'))
 for n in [9700,9701,9790]:
  s=state(n,n,'S','H' if n==9790 else 'I' if n==9700 else 'A','N')
  if n==9700:s+=c(n,'Clone health once','LifeSet','Time=0 && Var(2)=0','value=120')+c(n,'Remember clone form','VarSet','Time=0 && Var(2)=0','v=0\nvalue=Root,Var(42)')+c(n,'Remember order','VarSet','Time=0 && Var(2)=0','v=1\nvalue=Parent,Var(45)')+c(n,'Initialize once','VarSet','Time=0','v=2\nvalue=1')
  else:s+=c(n,'Consume order','VarSet','Time=0','v=1\nvalue=Parent,Var(45)')
  s+=c(n,'Clone age','VarAdd','1','v=5\nvalue=1','ignorehitpause=1')+c(n,'No clone push','PlayerPush','1','value=0')+c(n,'Clone receives damage','HitOverride','1','attr=SCA,NA,SA,HA,NP,SP,HP,NT,ST,HT\nstateno=9790\ntime=1\nforceair=0','ignorehitpause=1')+c(n,'Finite killable clone','DestroySelf','Var(2)=1 && (Life<=0 || Var(5)>=180 || (Root,Life)<=0 || (Root,StateNo%10000)=3000 || RoundState!=2)')+c(n,'Face enemy','Turn','P2Dist X<0','')
  if n!=9790:s+=c(n,'Take order','ChangeState','(Parent,Var(45))!=Var(1)','value=9701\nctrl=0')
  if n==9700:s+=c(n,'Approach','VelSet','1','x=IfElse(Abs(P2Dist X)>90,4,0)')+c(n,'Autonomous katana assault','ChangeState','Time>=18 && Abs(P2Dist X)<130','value=9701\nctrl=0')
  elif n==9790:s+=end(n,10,9700)
  else:s+=c(n,'Actual clone movement','VelSet','Time<18 && !MoveContact','x=6')+c(n,'Stop on hit','VelSet','MoveContact || Time>=18','x=0')+hit(n,10,'IfElse(Var(0),65,45)',stun=28)+hit(n,23,'IfElse(Var(0),85,70)',True)+end(n,38,9700)
  b.STATES.append(s)
def utility():
 for n in [170,180,190]:
  s=state(n,n)+voice(n,'Time=0','Die' if n==170 else '01')
  if n==190:s+=c(n,'Intro','AssertSpecial','Time<36','flag=Intro')+end(n,40)
  b.STATES.append(s)
 b.STATES.append(state(500,500)+c(500,'Charge','PowerAdd','1','value=20')+b.sound(500,'Time=0','Effect/RsgAura',3)+b.cast(500,'Time=0 && Var(42)=0 && NumHelper(9551)=0',9551,0,0)+ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=80','value=0\nctrl=1'))
 for n in [9551,9560]:
  s=state(n,8900,'A','I','N')+c(n,'Aura follows body','BindToRoot','1','time=1\npos=0,-42')+c(n,'Chakra aura','AngleDraw','1','value=90\nscale=.38,.45')+c(n,'Aura behind fighter','SprPriority','1','value=-2')+c(n,'Finite aura','DestroySelf','RoundState!=2 || (Root,Life)<=0 || '+('(Root,StateNo)!=500' if n==9551 else '(Root,Var(42))=0'));b.STATES.append(s)
 b.STATES.append(state(520,520)+start(520,'005')+c(520,'Pay focus','PowerAdd','Time=47','value=-1500')+c(520,'Uzuhiko focus','VarSet','Time=47','v=42\nvalue=1')+c(520,'Twenty seconds','VarSet','Time=47','v=40\nvalue=1200')+c(520,'Cooldown','VarSet','Time=47','v=41\nvalue=1500')+end(520,62))
def ultimate():
 for form in [0,1]:
  n=3000+form*10000;p=seq('Hiruzen_Skill05',1,6,3)*2+seq('Hiruzen_Skill05',7,12,3)+single('Hiruzen_Skill05_13',186)+seq('Hiruzen_Skill05',20,27,3)+single(idle(),46);attack(n,p,form,'5,-85,135,5')
  s=state(n,n,move='A',physics='N',cost=3000)+start(n,'005')+c(n,'Clear contact','VarSet','Time=0','v=21\nvalue=0')+c(n,'Palm approach','VelSet','Time>=36 && Time<60 && !MoveContact','x=IfElse(P2Dist X>65,5,0)')+c(n,'Plant on contact','VelSet','MoveContact || Time>=60','x=0')+hit(n,55,0,ident=3000,stun=330)+'p2stateno=3010\np2getp1state=1\n'
  s+=c(n,'Target position','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0','fv=0\nvalue=Target(3000),Pos X')+c(n,'Finite damage budget','VarSet','MoveHit && NumTarget(3000)>0 && Var(21)=0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{800 if form else 650},Floor((Target(3000),LifeMax)*{.8 if form else .65}))')+c(n,'Confirmed','VarSet','MoveHit && NumTarget(3000)>0','v=21\nvalue=1')+c(n,'Original tornado at the struck opponent','Explod','Time=61 && NumTarget(3000)>0',f'ID=9571\nanim=8817\npostype=P1\npos=65,0\nscale={.65 if form else .55},{.65 if form else .55}\nbindtime=-1\nremovetime=220\nsprpriority=-1\nownpal=1\nremoveongethit=1')+c(n,'Finite rotating bind','TargetBind','NumTarget(3000)>0 && Time<300','ID=3000\ntime=1\npos=65,-18-8*Abs(Sin(Time*.3))')
  for i,t in enumerate(PULSES):
   when=f'Time={t} && NumTarget(3000)>0';amount='Var(20)-Floor(Var(20)/8)*7' if i==7 else 'Floor(Var(20)/8)';s+=c(n,'Confirmed rotation','TargetLifeAdd',when,'ID=3000\nvalue=-('+amount+')\nabsolute=1\nkill=1')+c(n,'Count impact','HitAdd',when,'value=1')+fx(n,when,8700,65,-35,.6,8)+b.sound(n,when,'Effect/windeffect',2)
  b.STATES.append(s+c(n,'Release rival','TargetState','Time=300 && NumTarget(3000)>0','ID=3000\nvalue=3011')+end(n,310))
 for n,parent,limit in [(3010,3000,350),(3020,1030,90)]:
  b.STATES.append(state(n,None,'A','H','N')+c(n,'Keep opponent artwork','ChangeAnim','Time=0 && SelfAnimExist(5000)','value=5000')+c(n,'Spin reaction','AngleDraw','1','value=Time*15')+ctl(n,'Independent release','SelfState',f'trigger1=Time>={limit}\ntrigger2=NumEnemy=0\ntrigger3=(EnemyNear,StateNo)%10000!={parent}\ntrigger4=RoundState!=2','value=5050\nctrl=0'))
 for n in [3011,3021]:b.STATES.append(state(n,None,'A','H','N')+c(n,'Release velocity','VelSet','Time=0','x=-4\ny=-6')+c(n,'Restore own states','SelfState','1','value=5050\nctrl=0'))
def main():
 b.CHAR=CHAR;b.NAME=NAME;b.AIR=[];b.STATES=[];b.KEY=json.loads((CHAR/'assets/keys.json').read_text());b.SPRITES={r['key']:r for r in json.loads((CHAR/'assets/sprites.json').read_text())};b.SOUNDS=json.loads((CHAR/'assets/sounds.json').read_text())['keys'];b.SOUNDS['BorutoJogan/hurt1']=b.SOUNDS['BorutoTBv/hurt1'];b.idle=idle
 basic();normals();specials();helpers();utility();ultimate()
 import build_sarada_runtime as ref
 saved=ref.CHAR,ref.MOVES
 try:ref.CHAR=CHAR;ref.MOVES=MOVES;ref.commands()
 finally:ref.CHAR,ref.MOVES=saved
 path=CHAR/'SaradaTBV.cmd';(CHAR/(NAME+'.cmd')).write_text(path.read_text().replace('Pink Susanoo awakening','Uzuhiko focus'));path.unlink()
 const=(ROOT/'BorutoKarmaJogan/BorutoKarmaJogan.cns').read_text().split('[Statedef',1)[0];const=const[const.index('[Data]'):]
 (CHAR/(NAME+'.cns')).write_text('; TBV base, original supplied sprites and voices.\n'+const+''.join(b.STATES)+b.system().replace('Karma strength','Uzuhiko focus strength'))
 (CHAR/(NAME+'.air')).write_text('; Body composites belong only to the main fighter. Effects use standard AIR A.\n'+''.join(b.AIR))
 (CHAR/(NAME+'_common.cns')).write_bytes((ROOT/'BorutoKarmaJogan/BorutoKarmaJogan_common.cns').read_bytes())
 d=(ROOT/'BorutoKarmaJogan/BorutoKarmaJogan.def').read_text().replace('BorutoKarmaJogan',NAME).replace('Boruto Uzumaki Karma Jogan','Boruto Uzumaki TBV Base').replace('versiondate=10,27,2026','versiondate=10,28,2026');(CHAR/(NAME+'.def')).write_text(d)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,awakening='Uzuhiko focus, original TBV base appearance',awakening_ticks=1200,awakening_cost=1500,ultimate_damage=[650,800],ultimate_pulses=PULSES,own_life_cost=0,clone_health=120,clone_ticks=180),indent=2)+'\n')
 print(NAME,len(b.STATES),'states',len(b.AIR),'actions')
if __name__=='__main__':main()
