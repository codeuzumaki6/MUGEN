#!/usr/bin/env python3
"""Matsuri's two original sprite forms, water, roots, cloth and claw marks."""
from pathlib import Path
import json,re
from build_hidari_runtime import c,ctl,state,snd,effect,startup,recover,hit as physical_hit
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MatsuriShinju'
MOVES=[('Lanza','a','F',1000,350),('Latigo','a','B',1010,400),('Suiton','b','F',1020,450),('Jardin','b','B',1030,500),('Ascendente','c','F',1040,450),('Atadura','c','B',1050,600),('Barrido','a','D',1400,200),('Lanzador','b','D',1410,300),('Manto','c','D',1420,400),('Agua','y','N',1200,200),('Marca','z','N',1210,250),('Erupcion','y','D',1430,600),('Emboscada','z','D',1440,600)]
air=[];states=[];POSES={}
def poses(form,role):return POSES[str(form)][role]
def p(form,role,i=0):
 values=poses(form,role);return values[min(i,len(values)-1)]
def action(n,frames,form=0,box=None,loop=False,low=False,hurt=True):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+=f'Clsn2Default: 1\n Clsn2[0]=-13,{-46 if low else -76},13,-1\n'
 if loop:s+='Loopstart\n'
 for i,(pose,duration) in enumerate(frames):
  if box and 0<i<len(frames)-1:s+=f'Clsn1: 1\n Clsn1[0]={box}\n'
  s+=f'{form},{pose},0,0,{duration}\n'
 air.append(s)
def seq(form,role,duration=6):return [(i,duration) for i in poses(form,role)]
def fx(n,g,frames,duration=3,box=None,loop=False,add=False):
 s=f'\n[Begin Action {n}]\n'
 if box:s+=f'Clsn1Default: 1\n Clsn1[0]={box}\n'
 if loop:s+='Loopstart\n'
 for i in frames:s+=f'{g},{i},0,0,{duration}'+(',,A' if add else '')+'\n'
 air.append(s)
def damage(value,helper=False):
 prefix='Root,' if helper else ''
 return f'Floor({value}*IfElse({prefix}Var(42),1.30,1)*IfElse({prefix}Var(43)>0,1.15,1))'
def strike(n,t,value,fin=False,low=False,airborne=False,stun=30,helper=False,starter=False):
 s=physical_hit(n,t,damage(value,helper),fin,low,airborne,stun,starter)
 if helper:s=s.replace('attr=A,SA','attr=A,SP')
 return s
def cast(n,t,sn,x=30,y=-32):
 return c(n,'Physical Shinju technique','Helper',f'Time={t}',f'helpertype=Normal\nname="Tecnica de Matsuri"\nID={sn}\nstateno={sn}\npostype=P1\npos={x},{y}\nownpal=1\nkeyctrl=0')
def bound_draw(n,scale='1',blend=False):
 s=c(n,'Stable effect scale during impacts','AngleDraw','1',f'value=0\nscale={scale},{scale}','ignorehitpause=1')+c(n,'Effect has no push box','PlayerPush','1','value=0','ignorehitpause=1')+c(n,'Effect has no shadow','AssertSpecial','1','flag=NoShadow','ignorehitpause=1')
 if blend:s+=c(n,'Effect light retains its color','Trans','1','trans=AddAlpha\nalpha=160,256','ignorehitpause=1')
 return s
def animations():
 for form in [0,1]:
  off=form*10000;idle=seq(form,'idle',12)
  table={0:idle,5:idle[:1],6:[(p(form,'crouch'),6)],10:[(p(form,'crouch'),4)],11:[(p(form,'crouch'),5)],12:[(p(form,'crouch'),4)],20:seq(form,'walk',5),21:list(reversed(seq(form,'walk',5))),40:[(p(form,'air'),4)],41:[(p(form,'air',1),7)],44:[(p(form,'air',2),7)],52:[(p(form,'crouch'),5),(p(form,'idle'),7)],100:seq(form,'walk',3),105:list(reversed(seq(form,'walk',3))),170:[(p(form,'hurt',4),25)],180:seq(form,'gesture',14)+idle,190:idle+seq(form,'charge',8),500:seq(form,'charge',7),5000:[(p(form,'hurt'),7),(p(form,'hurt',1),7)],5010:[(p(form,'crouch'),7)],5020:[(p(form,'hurt',2),8)],5030:[(p(form,'hurt',2),7),(p(form,'hurt',3),7)],5100:[(p(form,'hurt',4),10)],5110:[(p(form,'hurt',4),25)],5120:[(p(form,'hurt',5),7),(p(form,'crouch'),6),(p(form,'idle'),5)],5150:[(p(form,'hurt',4),60)],5200:[(p(form,'air'),8)],5210:[(p(form,'air'),8)],5300:[(p(form,'hurt'),20)]}
  for n in [120,130,140,150]:table[n]=[(p(form,'guard'),6)]
  for n in [121,131,141,151]:table[n]=[(p(form,'crouch'),6)]
  for n in [122,132,142,152]:table[n]=[(p(form,'air'),6)]
  for n,frames in table.items():action(n+off,frames,form,loop=n in [0,11,20,21,41,44,500,5150],low=n in [10,11,12,121,131,141,151])
 for g,count in [(8700,4),(8710,4),(8720,6),(8670,11),(8900,24),(8910,5),(8820,5)]:fx(g,g,range(count),2 if g!=8900 else 3,loop=g==8900,add=True)
 fx(8610,8600,[4,5,6,7],3,box='-30,-18,30,18',loop=True)
 fx(8611,8600,[0,1,2,3,4,5,6,7],4,box='-44,-40,44,40',loop=True)
 fx(8612,8601,[0,1,2,2,2,2,1,0],4,box='-50,-90,50,0')
 fx(8613,8603,[0],6,loop=True)
 fx(8614,8604,[0,1,2,3,3,3,2,1],3,box='-16,-88,16,0')
 fx(8620,8602,[0,1,0,1,1,0],7,box='-50,-160,50,0')
 fx(8630,8630,[0,1,2,3],3,box='-21,-19,21,19',loop=True)
 fx(8631,8630,[4,5,6,7],3)
def normals():
 for form in [0,1]:
  off=form*10000
  for button,base,role in [('a',200,'punch'),('b',210,'kick'),('c',220,'cloak')]:
   for step in range(3):
    n=off+base+step;ready=p(form,role);middle=p(form,role,1+step);end=p(form,role,2+step)
    action(n,[(ready,3),(middle,5),(end,4),(ready,7)],form,box='-2,-67,78,-4')
    s=state(n,n,move='A',vel='2,0')+snd(n,'Time=3',1,0,1)+strike(n,3,[44,56,80][step],step==2)+c(n,'Normal step ends','VelSet','Time>=8','x=0')+recover(n,19);states.append(s)
  for base,role in [(600,'air'),(610,'kick'),(620,'spin')]:
   for step in range(3):
    n=base+off+step;action(n,[(p(form,'air'),3),(p(form,role,step),7),(p(form,role,step+1),7),(p(form,'air'),3)],form,box='-6,-70,76,-4')
    s=state(n,n,'A','A','N',vel=None)+c(n,'Limited aerial chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Brief aerial hover','VelSet','Time<6','x=1.8\ny=-.5')+c(n,'Return to gravity','VelAdd','Time>=6','y=.48')+strike(n,3,[42,50,72][step],step==2,airborne=True)
    s+=c(n,'Land from aerial attack','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+recover(n,20,True);states.append(s)
def water(n,t,value,scale=100,fin=True):
 return c(n,'Water damage snapshot','VarSet',f'Time={t}',f'v=30\nvalue={value}')+c(n,'Water size snapshot','VarSet',f'Time={t}',f'v=31\nvalue={scale}')+c(n,'Water finisher snapshot','VarSet',f'Time={t}',f'v=32\nvalue={int(fin)}')+cast(n,t,9400,36,-33)
def techniques():
 for form in [0,1]:
  off=form*10000
  for name,button,direction,base,cost in MOVES:
   if base in [1210,1440]:continue
   n=base+off;cost=round(cost*.8) if form else cost
   if base in [1000,1020,1030,1050,1200,1430]:
    role={1000:'thrust',1020:'water',1030:'gesture',1050:'bloom',1200:'water',1430:'crouch'}[base]
    frames=[(p(form,role),10),(p(form,role,1),12),(p(form,role,2),12),(p(form,role,3),12),(p(form,role),12),(p(form,'idle'),10)]
    action(n,frames,form);s=state(n,n,move='A',cost=cost)+startup(n)
    if base==1000:s+=cast(n,22,9410,48,-36)+snd(n,'Time=22',1,30,2)
    if base==1020:
     shots=[22,34,46,58] if form else [22,34,46]
     for i,t in enumerate(shots):s+=water(n,t,55,90,i==len(shots)-1)
    if base==1200:s+=water(n,20,115,130)
    if base==1030:
     s+=cast(n,22,9430,'IfElse(P2Dist X<230,P2Dist X,230)',0)+c(n,'Root garden grants finite damage aura','VarSet','Time=36','v=43\nvalue=420')+snd(n,'Time=22',1,41,2)
    if base==1050:s+=cast(n,22,9420,'IfElse(P2Dist X<200,P2Dist X,200)',-34)+snd(n,'Time=22',1,30,2)
    if base==1430:
     for i,t in enumerate([20,28,36,44]):s+=cast(n,t,9440,45+i*48,0)
     if form:s+=cast(n,52,9440,237,0)
     s+=snd(n,'Time=20',1,41,2)
    s+=recover(n,84 if base in [1020,1430] else 76 if base in [1030,1050] else 68);states.append(s);continue
   role={1010:'cloak',1040:'spin',1400:'crouch',1410:'punch',1420:'bloom'}[base]
   frames=[(p(form,role),8)]+[(p(form,role,i),10) for i in range(1,5)]+[(p(form,role),10),(p(form,'idle'),10)]
   action(n,frames,form,box='-12,-85,85,-3' if base!=1400 else '-3,-34,72,-2',low=base==1400)
   s=state(n,n,move='A',cost=cost,physics='N')+startup(n)
   if base==1010:
    s+=c(n,'Cloth combo moves with the body','VelSet','Time>=8 && Time<34','x=2.3')+c(n,'Cloth combo brakes','VelSet','Time>=34','x=0')
    for i,t in enumerate([10,28,46]):s+=strike(n,t,[45,55,100][i],i==2,stun=38)+effect(n,f'Time={t}',8611,48,-36,1.05,12)
   if base==1400:s+=c(n,'Low sliding sweep','VelSet','Time>=8 && Time<24','x=6\ny=0')+c(n,'Sweep stops','VelSet','Time>=24','x=0\ny=0')+strike(n,8,110,True,low=True)
   if base==1040:
    s+=c(n,'Rising Shinju strike','VelSet','Time=8','x=3\ny=-6')+c(n,'Rising attack becomes airborne','StateTypeSet','Time=8','statetype=A\nphysics=N')+c(n,'Rising strike obeys gravity','VelAdd','Time>8','y=.42')+strike(n,8,80,airborne=True)+strike(n,20,100,True,airborne=True)
    s+=c(n,'Land the rising strike','ChangeState','Time>16 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
   if base==1410:s+=strike(n,8,75,stun=35)+strike(n,27,100,True,stun=40)+effect(n,'Time=27',8611,30,-35,1.1,15)
   if base==1420:
    for i,t in enumerate([10,27,44]):s+=strike(n,t,[55,65,95][i],i==2,stun=38)+effect(n,f'Time={t}',8611,25,-36,1.5,14)
   s+=recover(n,68,base==1040);states.append(s)
def helpers():
 n=9400;s=state(n,8630,'A','A','N',vel='12,0')+c(n,'Remember water damage','VarSet','Time=0','v=0\nvalue='+damage('Root,Var(30)',True))+c(n,'Remember water size','VarSet','Time=0','v=1\nvalue=Root,Var(31)')
 s+=c(n,'Remember water finisher','VarSet','Time=0','v=2\nvalue=Root,Var(32)')
 waterhit=physical_hit(n,0,'Var(0)',False,airborne=True).replace('attr=A,SA','attr=A,SP').replace('hitsound=S1,7','hitsound=S2,1').replace('ground.velocity=-0.3,0','ground.velocity=IfElse(Var(2),-5,0),IfElse(Var(2),-8,0)').replace('air.velocity=-0.5,-1','air.velocity=IfElse(Var(2),-4,0),IfElse(Var(2),-5,-.1)').replace('fall=0','fall=Var(2)')
 s+=bound_draw(n,'Var(1)/100.0',False)+waterhit+'hitonce=1\n'
 s+=snd(n,'Time=0',2,0,2,85)+c(n,'Splash after physical contact','ChangeState','MoveContact','value=9401')+c(n,'Water has finite range','DestroySelf','Time>=44 || RoundState!=2');states.append(s)
 n=9401;s=state(n,8631,'A',physics='N')+bound_draw(n,'1')+snd(n,'Time=0',2,1,2,75)+c(n,'Water splash ends','DestroySelf','AnimTime=0 || Time>=16 || RoundState!=2');states.append(s)
 n=9410;s=state(n,8610,'A','A','N',vel='9,0')+bound_draw(n,'1.4')+strike(n,0,180,True,airborne=True,helper=True)+c(n,'Cloth lance ends at contact','DestroySelf','MoveContact || Time>=27 || RoundState!=2');states.append(s)
 n=9420;s=state(n,8611,'A','A','N')+bound_draw(n,'1.4')+c(n,'Visible cloth coils turn around the victim','AngleDraw','1','value=Time*15\nscale=1.4,1.4','ignorehitpause=1')
 for i,t in enumerate([6,20,34]):s+=strike(n,t,[60,70,90][i],i==2,airborne=True,stun=30,helper=True)
 s+=c(n,'Cloth binding is finite','DestroySelf','Time>=48 || Root,MoveType=H || RoundState!=2');states.append(s)
 n=9430;s=state(n,8612,'A','A','N')+bound_draw(n,'1')+strike(n,8,145,True,airborne=True,helper=True)+c(n,'Garden roots withdraw','DestroySelf','Time>=40 || Root,MoveType=H || RoundState!=2');states.append(s)
 n=9440;s=state(n,8614,'A','A','N')+bound_draw(n,'1')+strike(n,8,55,True,airborne=True,helper=True)+c(n,'Ground spike withdraws','DestroySelf','Time>=26 || RoundState!=2');states.append(s)
 n=9450;s=state(n,8620,'A',physics='N')+bound_draw(n,'1')+c(n,'Ultimate tree ends with its capture','DestroySelf','Root,StateNo%10000!=3001 || Time>=170 || RoundState!=2');states.append(s)
 n=9550;s=state(n,8900,'A',physics='N')+c(n,'Charge aura follows Matsuri','BindToRoot','1','time=-1\npos=0,-38','ignorehitpause=1')+bound_draw(n,'.22',True)+c(n,'Vertical charge envelope','AngleDraw','1','value=90\nscale=.22,.22','ignorehitpause=1')+c(n,'Purple Shinju aura','PalFX','1','time=1\ncolor=0\nmul=180,80,240\nadd=35,0,40','ignorehitpause=1')
 s+=c(n,'Aura stays behind original body','SprPriority','1','value=-2','ignorehitpause=1')+c(n,'Charge aura cleanup','DestroySelf','Root,StateNo!=500 && Root,StateNo!=520 || Root,Life<=0 || RoundState!=2');states.append(s)
 n=9551;s=state(n,8900,'A',physics='N')+c(n,'Buff glow follows Matsuri','BindToRoot','1','time=-1\npos=0,-36','ignorehitpause=1')+bound_draw(n,'.18',True)+c(n,'Vertical garden envelope','AngleDraw','1','value=90\nscale=.18,.18','ignorehitpause=1')+c(n,'Garden aura behind original body','SprPriority','1','value=-2','ignorehitpause=1')+c(n,'Purple garden buff','PalFX','1','time=1\ncolor=0\nmul=180,60,240','ignorehitpause=1')+c(n,'Buff glow expires','DestroySelf','Root,Var(43)=0 || Root,Life<=0 || RoundState!=2');states.append(s)
def claws():
 for form in [0,1]:
  off=form*10000;n=1210+off;action(n,seq(form,'mark',9)+[(p(form,'idle'),12)],form)
  s=state(n,n,move='A',cost=200 if form else 250)+startup(n)+cast(n,12,9600,'IfElse(P2Dist X<180,P2Dist X,180)',0)+snd(n,'Time=12',1,32,2)+recover(n,54);states.append(s)
  for base,cost in [(1211,200),(1440,600)]:
   n=base+off;action(n,[(p(form,'mark'),8),(p(form,'mark',1),8),(p(form,'thrust',2),12),(p(form,'thrust',3),12),(p(form,'idle'),18)],form,box='-6,-70,92,-3')
   s=state(n,n,move='A',cost=round(cost*.8) if form else cost,physics='N')+startup(n)
   s+=cast(n,5,9600,'IfElse(P2Dist X<230,P2Dist X,230)',0).replace('trigger1=Time=5','trigger1=Time=5 && NumHelper(9600)=0')+c(n,'Travel through the visible placed mark','PosSet','Time=16 && NumHelper(9600)>0','x=(Helper(9600),Pos X)-Facing*35\ny=0')+c(n,'Face the target after portal exit','Turn','Time=17 && P2Dist X<0','')+c(n,'Pass through claw opening','PlayerPush','Time>=11 && Time<=21','value=0')
   s+=snd(n,'Time=16',1,32,2)+strike(n,26,150 if base==1211 else 180,True)+effect(n,'Time=26',8611,45,-32,1.2,16)
   if base==1440:s+=cast(n,28,9430,45,0)
   s+=recover(n,70);states.append(s)
 n=9600;s=state(n,8613,'A',physics='N')+bound_draw(n,'.7')+c(n,'Claw mark stays on the floor','SprPriority','1','value=-2','ignorehitpause=1')+ctl(n,'Consume claw mark after transit','DestroySelf','trigger1=Time>=600\ntrigger2=RoundState!=2\ntrigger3=Root,StateNo%10000=1211 || Root,StateNo%10000=1440 || Root,StateNo%10000=3000\ntrigger3=Root,Time>=17');states.append(s)
def utility():
 for n in [170,180,190]:
  s=state(n,f'{n}+10000*Var(42)')+c(n,'Original round pose','Null','1')
  if n==190:s+=c(n,'Intro waits for round','AssertSpecial','Time<36','flag=Intro')+recover(n,44)
  states.append(s)
 s=state(500,'500+10000*Var(42)')+c(500,'Hold chakra charge','PowerAdd','1','value=22')+snd(500,'Time=0',1,4,3,60)+cast(500,0,9550,0,-38).replace('trigger1=Time=0','trigger1=Time=0 && NumHelper(9550)=0')
 s+=ctl(500,'Release energy charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=65','value=0\nctrl=1');states.append(s)
 action(520,seq(0,'charge',8)+seq(0,'idle',10),0);s=state(520,520)+startup(520)+cast(520,0,9550,0,-38)
 for i in range(4):s+=effect(520,f'Time={8+i*6}',8611,0,-36,.8+i*.15,18)
 s+=c(520,'Awakening energy payment','PowerAdd','Time=24','value=-1500')+c(520,'Uncloaked awakening','VarSet','Time=24','v=42\nvalue=1')+c(520,'Fifteen seconds of awakening','VarSet','Time=24','v=40\nvalue=900')+c(520,'Awakening cooldown','VarSet','Time=24','v=41\nvalue=1500')+c(520,'Use original uncloaked poses at native scale','ChangeAnim','Time=24','value=10520')+snd(520,'Time=24',1,41,2)+recover(520,58);states.append(s)
 action(10520,seq(1,'charge',8)+seq(1,'idle',10),1)
def ultimate():
 for form in [0,1]:
  off=form*10000;n=3000+off
  action(n,[(p(form,'mark'),10),(p(form,'mark',1),10),(p(form,'thrust',2),16),(p(form,'idle'),18)],form,box='-4,-70,88,-2')
  s=state(n,n,move='A',cost=3000,physics='N')+startup(n)+cast(n,4,9600,'IfElse(P2Dist X<230,P2Dist X,230)',0).replace('trigger1=Time=4','trigger1=Time=4 && NumHelper(9600)=0')
  s+=c(n,'Ultimate travels a finite visible distance','PosSet','Time=16 && NumHelper(9600)>0 && Abs(P2Dist X)<=240','x=(Helper(9600),Pos X)-Facing*44\ny=0')+c(n,'Face target after ultimate approach','Turn','Time=17 && P2Dist X<0','')
  s+=physical_hit(n,22,0,starter=True)+c(n,'Only a real hit confirms the ultimate','ChangeState','MoveHit && NumTarget(3000)>0',f'value={3001+off}')+recover(n,60);states.append(s)
  n=3001+off;role='bloom';frames=[(p(form,role,i),12) for i in range(3)];action(n,frames,form,loop=True)
  s=state(n,n,move='A',physics='N')+c(n,'Finite protection during confirmed cinematic','NotHitBy','Time<150','value=SCA\ntime=1')+c(n,'Bounded ultimate damage','VarSet','Time=0 && NumTarget(3000)>0',f'v=20\nvalue=IfElse((Target(3000),LifeMax)>=1000,{450 if form else 420},Floor((Target(3000),LifeMax)*{.45 if form else .42}))')
  s+=c(n,'Keep captured target in the original roots','TargetBind','Time<148 && NumTarget(3000)>0','ID=3000\ntime=1\npos=60,-12')+cast(n,2,9450,62,0)
  for i,t in enumerate([38,70,102,134]):
   amount='Var(20)-3*Floor(Var(20)/4)' if i==3 else 'Floor(Var(20)/4)'
   s+=c(n,'Absolute life-relative damage slice','TargetLifeAdd',f'Time={t} && NumTarget(3000)>0',f'ID=3000\nvalue=-({amount})\nabsolute=1\nkill={int(i==3)}')+effect(n,f'Time={t}',8611,60,-42,1.5,22)+snd(n,f'Time={t}',1,41,2)
  s+=c(n,'Release target after the final blow','TargetState','Time=148 && NumTarget(3000)>0','ID=3000\nvalue=3011')+c(n,'Clear cinematic target','TargetDrop','Time=149','excludeID=-1')+recover(n,172);states.append(s)
 s=state(3010,None,'A','H','N')+c(3010,'Opponent hurt pose','ChangeAnim','Time=0','value=5030')+c(3010,'Held target has no push','PlayerPush','1','value=0')+ctl(3010,'Captured opponent has a fallback','SelfState','trigger1=Time>=190\ntrigger2=NumEnemy=0\ntrigger3=EnemyNear,StateNo%10000!=3001','value=IfElse(Life>0,5050,5150)');states.append(s)
 s=state(3011,None,'A','H','N',vel='-5,-7')+c(3011,'Released victim pose','ChangeAnim','Time=0','value=5030')+c(3011,'Released victim falls','VelAdd','1','y=.5')+c(3011,'Victim returns to own recovery','SelfState','Time>3 && Pos Y>=0 && Vel Y>0','value=IfElse(Life>0,5100,5150)');states.append(s)
def system():
 s='\n[Statedef -2]\n'
 for v in [40,41,43]:s+=c(-2,'Finite form and garden timers','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Safe awakening expiry','VarSet','!IsHelper && Var(42)>0 && Var(40)=0 && Ctrl && MoveType!=H','v=42\nvalue=0')+c(-2,'Restore original base idle after expiry','ChangeAnim','!IsHelper && Var(42)=0 && Anim>=10000 && StateNo<200','value=Anim-10000')+c(-2,'Preserve original awakened bank through common states','ChangeAnim','!IsHelper && Var(42)=1 && Anim<10000 && StateNo!=520 && SelfAnimExist(Anim+10000)','value=Anim+10000')
 s+=c(-2,'Aerial chain resets on landing','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Stop charge hum','StopSnd','!IsHelper && StateNo!=500','channel=3')
 s+=c(-2,'Garden aura is a single finite helper','Helper','!IsHelper && Var(43)>0 && NumHelper(9551)=0 && RoundState=2','helpertype=Normal\nname="Aura del jardin"\nID=9551\nstateno=9551\npostype=P1\npos=0,-5\nownpal=1\nkeyctrl=0')
 for v in [42,43]:s+=c(-2,'Round form cleanup','VarSet','!IsHelper && RoundState!=2 && StateNo!=190',f'v={v}\nvalue=0')
 return s
def commands():
 s='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\ns=s\n[Defaults]\ncommand.time=20\ncommand.buffer.time=3\n'
 def cmd(name,keys,buffer=3):return f'\n[Command]\nname="{name}"\ncommand={keys}\ntime=20\nbuffer.time={buffer}\n'
 for name,b,d,n,cost in MOVES:
  for keys in ([f'~D,D{d},{d},{b}',f'~D,{d},{b}'] if d in ['F','B'] else [f'/D,{b}'] if d=='D' else [b]):s+=cmd(name,keys,1 if d=='N' else 3)
 for b in ['a','b','c','x','y','z','s']:s+=cmd(b,b)+cmd('hold_'+b,'/'+b,1)
 for name,keys in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D'),('FF','F,F'),('BB','B,B'),('recovery','a+b')]:s+=cmd(name,keys,1 if keys.startswith('/') else 3)
 s+='\n[Statedef -1]\n'
 for name,b,d,n,cost in MOVES:
  extra='\ntriggerall=command!="holddown"' if d=='N' else ''
  dest=f'{n}+10000*Var(42)' if n!=1210 else 'IfElse(NumHelper(9600)>0,1211,1210)+10000*Var(42)'
  s+=ctl(-1,name,'ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=Power>=IfElse(Var(42),{round(cost*.8)},{cost}){extra}\ntrigger1=ctrl',f'value={dest}')
 s+=ctl(-1,'Original uncloaked awakening','ChangeState','triggerall=AILevel=0\ntriggerall=command="s"\ntriggerall=command="holddown"\ntriggerall=Power>=3000\ntriggerall=Var(42)=0\ntriggerall=Var(41)=0\ntriggerall=StateType!=A\ntrigger1=ctrl','value=520')
 s+=ctl(-1,'Ultimate Xbox A','ChangeState','triggerall=AILevel=0\ntriggerall=command="x"\ntriggerall=Power>=3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=3000+10000*Var(42)')
 s+=ctl(-1,'Hold Pause to charge','ChangeState','triggerall=AILevel=0\ntriggerall=command="hold_s"\ntriggerall=command!="holddown"\ntriggerall=Power<3000\ntriggerall=StateType!=A\ntrigger1=ctrl','value=500')
 for b,base in [('a',200),('b',210),('c',220)]:
  s+=ctl(-1,'Three hit ground chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=command!="holddown"\ntriggerall=StateType!=A\ntrigger1=ctrl\ntrigger2=StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220\ntrigger2=MoveHit\ntrigger2=Time>=6\ntrigger3=StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221\ntrigger3=MoveHit\ntrigger3=Time>=6',f'value={base}+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))','ignorehitpause=1')
  s+=ctl(-1,'Limited aerial chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=StateType=A\ntriggerall=Var(12)<3\ntrigger1=ctrl\ntrigger2=StateNo%10000>=600 && StateNo%10000<=621\ntrigger2=MoveHit\ntrigger2=Time>=6',f'value={base+400}+10000*Var(42)+Var(12)','ignorehitpause=1')
 for name,n in [('FF',100),('BB',105)]:s+=ctl(-1,'Free double tap dash','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType=S\ntrigger1=ctrl',f'value={n}')
 for n,cost,dist in [(3000,3000,180),(1030,500,220),(1020,450,300),(1000,350,230),(1200,200,280)]:s+=ctl(-1,'CPU legal special','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=Power>={cost}\ntrigger1=P2BodyDist X<{dist}\ntrigger1=Random<AILevel*3',f'value={n}+10000*Var(42)')
 s+=ctl(-1,'CPU close chain','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X<65','value=200+10000*Var(42)')+ctl(-1,'CPU approach','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X>=65','value=20\nctrl=1')
 (CHAR/'MatsuriShinju.cmd').write_text(s)
def main():
 global POSES
 POSES=json.loads((CHAR/'assets/poses.json').read_text());animations();normals();techniques();helpers();claws();utility();ultimate();commands()
 constants=(ROOT/'HidariShinju/HidariShinju.cns').read_text().split('[Statedef',1)[0];constants=constants[constants.index('[Data]'):].replace('height=83','height=78')
 (CHAR/'MatsuriShinju.cns').write_text('; Matsuri Shinju: original Vaydra base and uncloaked forms.\n'+constants+''.join(states)+system())
 (CHAR/'MatsuriShinju.air').write_text('; Original Matsuri sprites in groups 0 and 1.\n'+''.join(air))
 common=(ROOT/'HidariShinju/HidariShinju_common.cns').read_text();(CHAR/'MatsuriShinju_common.cns').write_text(common)
 definition=(ROOT/'HidariShinju/HidariShinju.def').read_text().replace('HidariShinju','MatsuriShinju').replace('Hidari Shinju','Matsuri Shinju');definition=re.sub(r'(?im)^author=.*$', 'author="Vaydra / Vahidras (sprites), Codex (fan adaptation)"',definition);(CHAR/'MatsuriShinju.def').write_text(definition)
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,awakening='Original uncloaked lower-sheet form',awakening_cost=1500,activation_requires=3000,awakening_ticks=900,cooldown_ticks=1500,garden_buff_ticks=420,ultimate_cost=3000,base_ultimate_budget='min(420,42% opponent max life)',awakened_ultimate_budget='min(450,45% opponent max life)',voices=False),indent=2)+'\n')
 print('Matsuri runtime:',len(states),'states,',len(air),'actions')
if __name__=='__main__':main()
