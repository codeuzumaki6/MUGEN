#!/usr/bin/env python3
"""Delta Kara: real projectile absorption, pink ocular rays, jets and energy-only ultimate."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'DeltaKara'
MOVES=[('Piston','a','F',1000,300),('Pierna','a','B',1010,350),('RayoDestructor','b','F',1020,500),('Picado','b','B',1030,450),('Ascenso','c','F',1040,400),('Impacto','c','B',1050,500),('Barrido','a','D',1400,200),('Lanzador','b','D',1410,300),('Onda','c','D',1420,400),('Rayo','y','N',1200,200),('Propulsion','z','N',1210,350),('Absorcion','y','D',1430,150),('Devolver','z','D',1440,250)]
AIR=[];STATES=[]
def ctl(n,label,kind,triggers,params='',extra=''):return f'\n[State {n}, {label}]\ntype={kind}\n{triggers}\n{params}\n{extra}\n'
def c(n,label,kind,when,params='',extra=''):return ctl(n,label,kind,'trigger1='+when,params,extra)
def state(n,anim=None,typ='S',move='I',physics='S',cost=0,vel='0,0',ctrl=0):return f'\n[Statedef {n}]\ntype={typ}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'+(f'anim={anim}\n' if anim is not None else '')+(f'velset={vel}\n' if vel else '')+(f'poweradd=-{cost}\n' if cost else '')
def action(n,frames,g=0,hurt='-14,-82,14,0',attack=None,active=None,loop=False,add=False):
 s=f'\n[Begin Action {n}]\n'
 if hurt:s+='Clsn2Default: 1\n Clsn2[0]='+hurt+'\n'
 if loop:s+='Loopstart\n'
 for i,(p,t) in enumerate(frames):
  if attack and (active is None or i in active):s+='Clsn1: 1\n Clsn1[0]='+attack+'\n'
  s+=f'{g},{p},0,0,{t}'+(',,A' if add else '')+'\n'
 AIR.append(s)
def snd(n,t,number=21,channel=4,volume=75):return c(n,'Technique sound','PlaySnd',t,f'value=S1,{number}\nchannel={channel}\nvolumescale={volume}')
def fx(n,anim,t,pos='0,-40',scale='.5,.5',duration=-2,priority=4):return c(n,'Visible technique','Explod',t,f'anim={anim}\nID={anim}\npostype=P1\npos={pos}\nscale={scale}\nremovetime={duration}\nbindtime=1\nownpal=1\nsprpriority={priority}\nremoveongethit=1\npausemovetime=100\nsupermovetime=100')
def startup(n):return snd(n,'Time=0')+c(n,'Brief activation','SuperPause','Time=0','time=8\nmovetime=0\nanim=-1\nsound=-1\ndarken=1\nunhittable=0\np2defmul=1\npoweradd=0','persistent=0')+fx(n,8710,'Time=0',pos='8,-60',scale='.5,.5',duration=8)
def end(n,t=52,dest=0):return c(n,'Restore control','ChangeState',f'Time>={t}',f'value={dest}\nctrl=1')
def helper(n,t,ident,number=None,pos='0,0',name='Delta technique',extra=''):return c(n,'Physical technique','Helper',t,f'helpertype=Normal\nname="{name}"\nID={ident}\nstateno={number or ident}\npostype=P1\npos={pos}\nkeyctrl=0\nownpal=1\n{extra}')
def hit(n,t,damage,fin=False,low=False,air=False,attr=None,stun=18,ident=0,guard='MA'):
 return c(n,'Actual collision','HitDef',f'Time={t}',f'''attr={attr or ('A' if air else 'C' if low else 'S')+','+('SA' if n>=1000 else 'NA')}
damage={damage},0
animtype={'Up' if fin else 'Medium'}
guardflag={'L' if low else guard}
hitflag=MAF
priority=5,Hit
pausetime=4,8
sparkno=S8700
guard.sparkno=-1
sparkxy=0,-42
hitsound=S1,{19 if fin else 7}
guardsound=S1,9
ground.type={'Low' if low else 'High'}
ground.hittime={stun}
ground.slidetime=16
ground.velocity={-6 if fin else -.35},{-7 if fin else 0}
air.hittime=28
air.velocity={-4 if fin else -.6},{-5 if fin else -1}
fall={int(fin)}
fall.recover=1
fall.recovertime=40
getpower={25 if n<1000 else 0},0
givepower=10,5
ID={ident}
hitonce=1
envshake.time={7 if fin else 2}
envshake.ampl={-4 if fin else -1}''')
def basics():
 anims={0:([(0,10),(1,10),(2,10)],True),5:([(0,6)],False),6:([(0,6)],False),10:([(14,5)],False),11:([(14,6)],True),12:([(14,4),(0,3)],False),20:([(p,5) for p in range(3,8)],True),21:([(p,5) for p in reversed(range(3,8))],True),100:([(p,3) for p in range(8,14)],True),105:([(p,3) for p in reversed(range(8,14))],True),40:([(38,4),(32,3)],False),41:([(33,6),(32,6)],True),44:([(34,6),(35,6)],True),52:([(38,6),(0,4)],False),170:([(43,30)],False),180:([(46,30),(47,60)],True),190:([(47,24),(46,20)],False),500:([(15,8),(31,8)],True),520:([(15,10),(31,10),(39,10),(0,12)],False),550:([(34,8),(35,8)],True),5000:([(40,8),(41,7)],False),5010:([(14,8)],False),5020:([(42,7)],False),5030:([(42,7)],False),5100:([(43,9)],False),5110:([(43,28)],False),5120:([(44,8),(45,8),(0,5)],False),5150:([(43,60)],True),5200:([(33,8)],False),5210:([(33,8)],False),5300:([(40,20)],False)}
 for n,(frames,loop) in anims.items():action(n,frames,hurt='-45,-28,55,0' if n in [170,5100,5110,5150] else '-16,-60,18,0' if n in [10,11,12,5010] else '-14,-82,14,0',loop=loop)
 for n in [120,130,140,150]:action(n,[(15,5)])
 for n in [121,131,141,151,122,132,142,152]:action(n,[(14,5)],hurt='-16,-60,18,0')
 for n in [8700,8710,8720,8820,8900,8800,8801,8802,8803]:
  count=24 if n==8900 else 6 if n==8720 else 5 if n==8820 else 4
  action(n,[(p,3) for p in range(count)],g=n,hurt=None,loop=n in [8800,8801,8802,8803,8900],add=True)
 action(9110,[(0,4),(1,4),(2,4),(3,4)],g=8803,hurt='-16,-82,30,0',loop=True,add=True)
 action(9200,[(2,3),(3,3)],g=8800,hurt=None,attack='-12,-12,12,12',loop=True,add=True)
 action(9300,[(n,3 if n<11 else -1) for n in range(12)],g=8840,hurt=None,attack='-155,-160,155,8',active=[4,5,6])
def normals():
 for base,ready,strikes in [(200,16,[17,20,25]),(210,21,[22,25,36]),(220,19,[20,30,37])]:
  for step,p in enumerate(strikes):
   n=base+step;action(n,[(ready,3),(p,8),(18 if base==200 else 23,9)],attack='0,-72,'+str(90 if p==25 else 65)+',-5',active=[1])
   s=state(n,n,move='A',vel='2,0')+snd(n,'Time=3',0,1,60)+hit(n,3,[42,55,72][step],step==2,stun=12)
   s+=c(n,'Short approach','VelSet','Time>=7','x=0')+end(n,20);STATES.append(s)
 for base,poses in [(600,[17,36,37]),(610,[36,22,25]),(620,[20,30,37])]:
  for step,p in enumerate(poses):
   n=base+step;action(n,[(34,3),(p,8),(35,7)],attack='-3,-74,75,-5',active=[1])
   s=state(n,n,'A','A','N',vel=None)+c(n,'Finite air chain','VarAdd','Time=0','v=12\nvalue=1')+c(n,'Short juggle','VelSet','Time<7','x=2\ny=-.4')+c(n,'Gravity resumes','VelAdd','Time>=7','y=.48')
   s+=hit(n,3,[38,46,64][step],step==2,air=True,stun=16)+c(n,'Land safely','ChangeState','Pos Y>=0 && Vel Y>0','value=52\nctrl=1')+end(n,18,50);STATES.append(s)
def aim(n,t):
 s=c(n,'Conservative opponent height','VarSet',f'Time={t}','v=24\nvalue=60')
 s+=c(n,'Actual target height','VarSet',f'Time={t} && NumEnemy>0','v=24\nvalue=Floor(EnemyNear,Const(size.height))')
 s+=c(n,'Keep short targets hittable','VarSet',f'Time={t}','v=24\nvalue=IfElse(Var(24)<12,12,IfElse(Var(24)>80,80,Var(24)))')
 s+=c(n,'Aim inside target body','VarSet',f'Time={t}','fv=12\nvalue=Var(24)*.4')
 s+=c(n,'Lower crouching aim','VarSet',f'Time={t} && NumEnemy>0 && EnemyNear,StateType=C','fv=12\nvalue=Var(24)*.18')
 s+=c(n,'Projectile vertical speed','VarSet',f'Time={t}','fv=13\nvalue=(55-Pos Y-FVar(12))*11/IfElse(P2Dist X>57,P2Dist X-35,22)')
 s+=c(n,'Track actual airborne target height','VarSet',f'Time={t} && NumEnemy>0','fv=13\nvalue=(55+(EnemyNear,Pos Y)-Pos Y-FVar(12))*11/IfElse(P2Dist X>57,P2Dist X-35,22)')
 return s
def shoot(n,t,damage,duration=180,kind=1):
 return aim(n,t)+c(n,'Ocular damage','VarSet',f'Time={t}',f'v=50\nvalue={damage}')+c(n,'Regeneration interference duration','VarSet',f'Time={t}',f'v=51\nvalue={duration}')+c(n,'New beam contact flag','VarSet',f'Time={t}','v=52\nvalue=0')+c(n,'Shot kind','VarSet',f'Time={t}',f'v=53\nvalue={kind}')+helper(n,f'Time={t}',9200,pos='35,-55',name='Pink ocular shot')+(helper(n,f'Time={t}',9202,pos='35,-55',name='Pink beam trail') if kind else '')+snd(n,f'Time={t}',42,1,80)
def techniques():
 melee={1000:([(16,8),(17,10),(20,10),(25,12),(18,12)],[8,20,30],[45,55,80],False),1010:([(24,8),(25,22),(26,10),(0,12)],[8],[190],False),1040:([(29,8),(30,12),(36,12),(38,16)],[8,20],[65,110],False),1210:([(8,8),(9,12),(36,12),(18,20)],[8,22],[70,100],False),1400:([(27,7),(28,18),(14,8),(0,10)],[7],[105],True),1410:([(29,7),(30,18),(0,20)],[7],[135],False)}
 costs={n:cost for name,b,d,n,cost in MOVES}
 for n,(poses,times,damage,low) in melee.items():
  action(n,poses,attack='-3,'+('-32' if low else '-78')+','+('115' if n==1010 else '78')+',0',active=list(range(1,len(poses)-1)))
  s=state(n,n,move='A',physics='N',cost=costs[n])+startup(n)
  if n in [1000,1210,1400]:s+=c(n,'Powered approach','VelSet','Time>=8 && Time<29',f'x={7 if n==1210 else 5 if n==1400 else 3.2}')+c(n,'Stop approach','VelSet','Time>=29','x=0')
  if n in [1040,1410]:
   s+=c(n,'Jet-assisted rise','VelSet','Time=8','x=2.8\ny=-6.5')+c(n,'Airborne rise','StateTypeSet','Time=8','statetype=A\nphysics=N')+c(n,'Real gravity','VelAdd','Time>8','y=.44')+helper(n,'Time=8',9500,name='Foot thrusters')
   s+=c(n,'Land rising strike','ChangeState','Time>18 && Pos Y>=0 && Vel Y>0','value=52\nctrl=1')
  if n==1210:s+=helper(n,'Time=0',9500,name='Dash thrusters')
  for i,(t,d) in enumerate(zip(times,damage)):s+=hit(n,t,d,i==len(times)-1,low=low,air=n in [1040,1410],stun=22)
  s+=end(n,sum(t for p,t in poses),50 if n in [1040,1410] else 0);STATES.append(s)
 for n,heavy in [(1200,False),(1020,True),(11200,False)]:
  air=n==11200;action(n,[(31,8),(39,36),(0 if not air else 34,18)])
  s=state(n,n,'A' if air else 'S','A','N' if air else 'S',cost=500 if heavy else 200)+startup(n)
  if air:s+=c(n,'Short stable firing hover','VelSet','Time<26','x=0\ny=0')+c(n,'Gravity after firing','VelAdd','Time>=26','y=.44')
  s+=fx(n,8800,'Time=7',pos='35,-55',scale='.3,.3',duration=10)+shoot(n,14,230 if heavy else 115,300 if heavy else 180,2 if heavy else 1)+end(n,58 if heavy else 48,50 if air else 0);STATES.append(s)
 # A distinct diagonal aerial rush, with proper landing, not another eye shot.
 for n,cost in [(1030,450),(1050,500)]:
  action(n,[(32,8),(34,8),(37,24),(38,18),(0,10)],attack='-8,-75,74,0',active=[1,2,3])
  s=state(n,n,move='A',physics='N',cost=cost)+startup(n)+helper(n,'Time=4',9500,name='Propulsion')
  s+=c(n,'Launch','VelSet','Time=8',f'x={5 if n==1030 else 1.4}\ny=-7')+c(n,'Become airborne','StateTypeSet','Time=8','statetype=A\nphysics=N')
  s+=c(n,'Dive','VelSet','Time=18',f'x={5 if n==1030 else 1.5}\ny=7')+hit(n,18,150 if n==1030 else 95,False,air=True,stun=22)
  s+=c(n,'Land and resolve impact','ChangeState','Time>18 && Pos Y>=0 && Vel Y>0',f'value={1031 if n==1030 else 1051}')+end(n,80,50);STATES.append(s)
 for n,damage in [(1031,80),(1051,160),(1420,130)]:
  action(n,[(38,7),(20,12),(0,18)],attack='-75,-60,110,2',active=[1]);s=state(n,n,move='A',cost=400 if n==1420 else 0)+ (startup(n) if n==1420 else '')
  s+=hit(n,7,damage,True,stun=24)+fx(n,8720,'Time=7',pos='0,-20',scale='.9,.5')+snd(n,'Time=7',41,1)+end(n,37);STATES.append(s)
 # Absorption protects from projectile attributes only. Physical attacks remain legal.
 action(1430,[(15,8),(31,30),(0,12)])
 s=state(1430,1430,cost=150)+startup(1430)+c(1430,'Clear absorption event','VarSet','Time=0','v=46\nvalue=0')
 s+=c(1430,'Brief projectile immunity, never melee immunity','HitBy','Time>=8 && Time<=36 && Var(44)<3','value=SCA,NA,SA,HA,NT,ST,HT\ntime=1')+helper(1430,'Time=8 && Var(44)<3',9110,pos='20,0',name='Ocular absorption')
 s+=c(1430,'Actual absorbed projectile confirms','ChangeState','Var(46)>0','value=1431')+end(1430,50);STATES.append(s)
 action(1431,[(31,12),(0,10)])
 STATES.append(state(1431,1431)+c(1431,'Finish absorbing the projectile tail','HitBy','Time<=7','value=SCA,NA,SA,HA,NT,ST,HT\ntime=1')+c(1431,'Recover energy from absorbed chakra','PowerAdd','Time=0','value=220')+c(1431,'Finite storage','VarSet','Time=0','v=44\nvalue=IfElse(Var(44)<3,Var(44)+1,3)')+snd(1431,'Time=0',40,1)+fx(1431,8803,'Time=0',pos='13,-68',scale='.35,.35',duration=18)+end(1431,22))
 action(1440,[(31,7),(39,18),(0,20)])
 STATES.append(state(1440,1440,move='A',cost=250)+startup(1440)+c(1440,'Use one absorbed charge','VarAdd','Time=0','v=44\nvalue=-1')+shoot(1440,10,180,0,0)+end(1440,45))
def energy_helpers():
 for n in [9110,9111]:
  s=state(n,9110,'S','I','N')+c(n,'Follow the absorbing eye','BindToRoot','1','time=1\npos=20,0')+c(n,'No collision push','PlayerPush','1','value=0')+c(n,'Only projectile attributes enter the field','HitBy','1','value=SCA,NP,SP,HP\ntime=1')+c(n,'Field cannot be killed by absorbed damage','DefenceMulSet','1','value=0')+c(n,'No field shadow','AssertSpecial','1','flag=NoShadow')
  s+=c(n,'Small eye vortex','Explod','Time%6=0','anim=8803\npostype=P1\npos=-7,-68\nscale=.35,.35\nremovetime=8\nownpal=1\nsprpriority=5')+c(n,'Do not draw a body-sized vortex','AssertSpecial','1','flag=Invisible')
  if n==9110:s+=c(n,'Absorb real helper and engine projectiles','HitOverride','1','attr=SCA,NP,SP,HP\nstateno=9111\ntime=1\nforceair=0')
  else:s+=c(n,'Signal actual absorption','ParentVarSet','Time=0','v=46\nvalue=1')+snd(n,'Time=0',40,1)+c(n,'Retire successful field','DestroySelf','Time=0')
  s+=ctl(n,'Finite field and interruption cleanup','DestroySelf','trigger1=Time>=30\ntrigger2=(Root,StateNo!=1430)\ntrigger3=RoundState!=2');STATES.append(s)
 s=state(9200,9200,'A','A','N')
 for v,parent in [(0,50),(1,51),(2,53)]:s+=c(9200,'Read immutable shot data','VarSet','Time=0',f'v={v}\nvalue=Parent,Var({parent})')
 s+=c(9200,'Read downward aim','VarSet','Time=0','fv=0\nvalue=Parent,FVar(13)')+c(9200,'Aim at real short and crouched targets','VelSet','Time=0','x=11\ny=FVar(0)')
 s+=c(9200,'Head follows trajectory','AngleDraw','1','scale=.35,.35')+c(9200,'No push','PlayerPush','1','value=0')+c(9200,'No shadow','AssertSpecial','1','flag=NoShadow')
 s+=hit(9200,0,'Var(0)',True,air=True,attr='A,SP',stun=25,ident=9200)
 s+=c(9200,'Stop beam on real contact','ParentVarSet','MoveContact','v=52\nvalue=1')
 s+=c(9200,'Cell destruction requires a real player hit','ChangeState','MoveHit && NumTarget(9200)>0 && Var(1)>0','value=9210')+c(9200,'Resolve shot','DestroySelf','MoveContact || Time>=28 || FrontEdgeBodyDist<-120 || RoundState!=2');STATES.append(s)
 s=state(9202,8801,'A','I','N')+c(9202,'Read beam angle','VarSet','Time=0','fv=0\nvalue=Parent,FVar(13)')+c(9202,'Attach emission to eye','BindToRoot','1','time=1\npos=35,-55')
 s+=c(9202,'Beam grows to the physical tip','AngleDraw','1','value=-ATan(FVar(0)/11)*180/3.14159265\nscale=IfElse(Time<27,Time,27)*Exp(.5*Ln(121+FVar(0)*FVar(0)))/211.0,.48')+c(9202,'No push','PlayerPush','1','value=0')+c(9202,'No shadow','AssertSpecial','1','flag=NoShadow')+c(9202,'Clear on actual contact, miss or interruption','DestroySelf','Time>=28 || (Root,Var(52))>0 || (Root,MoveType=H) || RoundState!=2');STATES.append(s)
 # This helper keeps its own confirmed target while the opponent recovers.
 # No permanent custom state or global opponent LifeSet is used.
 s=state(9210,8800,'A','A','N')+c(9210,'Keep only the already confirmed target after recovery','ReversalDef','Time=0','reversal.attr=SCA,NP,SP,HP\nhitflag=MAF\nsparkno=-1\npausetime=0,0')+c(9210,'Remember post-hit life','VarSet','Time=0 && NumTarget>0','v=3\nvalue=Target,Life')
 s+=c(9210,'Observe only positive healing since the previous tick','VarSet','NumTarget>0','v=4\nvalue=IfElse((Target,Life)>Var(3),(Target,Life)-Var(3),0)')
 s+=c(9210,'Prevent healing for a finite duration','TargetLifeAdd','NumTarget>0 && Var(4)>0','ID=-1\nvalue=-Var(4)\nabsolute=1\nkill=0')+c(9210,'Follow subsequent real damage without restoring it','VarSet','NumTarget>0','v=3\nvalue=Target,Life')
 s+=c(9210,'Small persistent effect on actual target','PosSet','NumTarget>0','x=Target,Pos X\ny=(Target,Pos Y)-40')+c(9210,'Subtle cellular interference marker','AngleDraw','1','scale=.16,.16')+c(9210,'No push','PlayerPush','1','value=0')+c(9210,'No shadow','AssertSpecial','1','flag=NoShadow')
 s+=c(9210,'Finite debuff and target cleanup','DestroySelf','Time>=Var(1) || NumTarget=0 || RoundState!=2');STATES.append(s)
def utility():
 for n in [170,180,190]:STATES.append(state(n,n)+c(n,'Round pose','Null','1')+(c(n,'Brief intro','AssertSpecial','Time<40','flag=Intro')+end(n,44) if n==190 else ''))
 s=state(500,500)+c(500,'Recharge energy','PowerAdd','1','value=20')+snd(500,'Time=0',4,3,65)+helper(500,'Time=0',9550,name='Delta energy aura')
 s+=ctl(500,'Release charge','ChangeState','trigger1=AILevel=0 && command!="hold_s"\ntrigger2=Power>=3000\ntrigger3=AILevel>0 && Time>=75','value=0\nctrl=1');STATES.append(s)
 s=state(520,520,cost=1500)+startup(520)+c(520,'Activate overdrive','VarSet','Time=20','v=40\nvalue=720')+c(520,'Overdrive cooldown','VarSet','Time=20','v=41\nvalue=1500')+fx(520,8720,'Time=20',pos='0,-42',scale='1,1')+end(520,42);STATES.append(s)
 s=state(550,550,'A','I','N',ctrl=0)+c(550,'Remember jet flight','VarSet','Time=0','v=13\nvalue=1')+c(550,'Neutral jet velocity','VelSet','1','x=0\ny=0')
 for command,axis,value in [('holdfwd','x','6.5'),('holdback','x','-6.5'),('holdup','y','-4.5'),('holddown','y','4.5')]:s+=c(550,'Steer flight','VelSet',f'command="{command}"',f'{axis}={value}')
 s+=c(550,'Flight consumes energy','PowerAdd','Time%15=0','value=-25')+helper(550,'Time=0 && NumHelper(9500)=0',9500,name='Flight thrusters')
 s+=c(550,'Debounce the flight chord after shutdown','VarSet','Time>12 && command="flight"','v=14\nvalue=12')+c(550,'Flight can be toggled off','ChangeState','Time>12 && command="flight"','value=50\nctrl=1')+c(550,'Land or run out of flight fuel','ChangeState','Power<25 || Time>=480 || (Pos Y>=0 && Vel Y>=0)','value=50\nctrl=1');STATES.append(s)
 s=state(9500,8802,'A','I','N')+c(9500,'Boot exhaust follows the actual fighter','BindToRoot','1','time=1\npos=-5,-3')+c(9500,'Exhaust direction','AngleDraw','1','value=IfElse((Root,StateNo)=100 || (Root,StateNo)=1210,-90,IfElse((Root,StateNo)=105,90,0))\nscale=.4,.4')+c(9500,'No push','PlayerPush','1','value=0')+c(9500,'No shadow','AssertSpecial','1','flag=NoShadow')
 s+=c(9500,'Exhaust does not outlive movement or a hit','DestroySelf','(Root,MoveType=H) || RoundState!=2 || ((Root,StateNo)!=550 && (Root,StateNo)!=100 && (Root,StateNo)!=105 && (Root,StateNo)!=1210 && (Root,StateNo)!=1030 && (Root,StateNo)!=1050 && (Root,StateNo)!=1040 && (Root,StateNo)!=1410)');STATES.append(s)
 for n in [9550,9551]:
  s=state(n,8900,'A','I','N')+c(n,'Follow energy source','BindToRoot','1','time=1\npos=0,-40')+c(n,'Vertical energy','AngleDraw','1','value=90\nscale=.3,.38')+c(n,'Pink scientific energy','PalFX','1','time=1\ncolor=0\nmul=256,70,220')+c(n,'Aura transparency','Trans','1',f'trans=AddAlpha\nalpha={180 if n==9550 else 95},256')+c(n,'Behind the fighter','SprPriority','1','value=-2')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'Finite energy aura','DestroySelf','trigger1=Time>=720\ntrigger2='+('(Root,StateNo!=500)' if n==9550 else '(Root,Var(40)=0)')+'\ntrigger3=(Root,Life<=0)\ntrigger4=RoundState!=2');STATES.append(s)
def ultimate():
 action(3000,[(31,16),(15,16),(39,16),(43,24),(44,14),(45,14),(0,20)])
 s=state(3000,3000,move='A',physics='N',cost=3000)+startup(3000)+snd(3000,'Time=20',43,1,85)
 s+=fx(3000,8800,'Time=10',pos='0,-40',scale='.8,.8',duration=38)+c(3000,'Brief protection during the actual explosion','NotHitBy','Time>=46 && Time<=64','value=SCA\ntime=1')
 s+=helper(3000,'Time=48',9300,name='Autodestruccion de Delta')+c(3000,'Bright detonation','EnvColor','Time=60','value=255,240,250\ntime=3\nunder=0')+snd(3000,'Time=60',41,1,95)+c(3000,'Large area feedback','EnvShake','Time=60','time=16\nfreq=65\nampl=-7')+end(3000,120);STATES.append(s)
 # The ultimate has NO own LifeAdd/LifeSet. It costs three energy bars only.
 s=state(9300,9300,'S','A','N')+c(9300,'No explosion push','PlayerPush','1','value=0')+c(9300,'No shadow','AssertSpecial','1','flag=NoShadow')
 s+=hit(9300,12,0,True,attr='S,HP',stun=30,ident=9300)
 s+=c(9300,'Finite life-relative area budget','VarSet','MoveHit && NumTarget(9300)>0 && Var(2)=0','v=0\nvalue=IfElse((Target(9300),LifeMax)>=1000,450,Floor((Target(9300),LifeMax)*.45))')
 s+=c(9300,'Damage only a target actually struck by the explosion','TargetLifeAdd','MoveHit && NumTarget(9300)>0 && Var(2)=0','ID=9300\nvalue=-Var(0)\nabsolute=1\nkill=1')+c(9300,'Single damage application','VarSet','MoveHit && NumTarget(9300)>0','v=2\nvalue=1')+c(9300,'Explosion finishes','DestroySelf','Time>=36 || RoundState!=2');STATES.append(s)
def commands():
 s='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\ns=s\n[Defaults]\ncommand.time=20\ncommand.buffer.time=3\n'
 def cmd(name,keys,buffer=3):return f'\n[Command]\nname="{name}"\ncommand={keys}\ntime=20\nbuffer.time={buffer}\n'
 for name,b,d,n,cost in MOVES:
  for keys in ([f'~D,D{d},{d},{b}',f'~D,{d},{b}'] if d in ['F','B'] else [f'/D,{b}'] if d=='D' else [b]):s+=cmd(name,keys,1 if d=='N' else 3)
 for b in ['a','b','c','x','y','z','s']:s+=cmd(b,b)+cmd('hold_'+b,'/'+b,1)
 for name,keys in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D'),('FF','F,F'),('BB','B,B'),('recovery','a+b'),('flight','y+z')]:s+=cmd(name,keys,1 if keys.startswith('/') else 3)
 s+='\n[Statedef -1]\n'
 s+=ctl(-1,'Jet flight','ChangeState','triggerall=AILevel=0\ntriggerall=command="flight"\ntriggerall=StateType=A\ntriggerall=StateNo!=550\ntriggerall=Var(14)=0\ntriggerall=Power>=100\ntrigger1=ctrl','value=550')
 for name,b,d,n,cost in MOVES:
  extra='\ntriggerall=command!="holddown"' if d=='N' else ''
  if n==1430:extra+='\ntriggerall=Var(44)<3'
  if n==1440:extra+='\ntriggerall=Var(44)>0'
  s+=ctl(-1,name,'ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=Power>={cost}{extra}\ntrigger1=ctrl',f'value={n}')
 s+=ctl(-1,'Aerial ocular ray','ChangeState','triggerall=AILevel=0\ntriggerall=command="Rayo"\ntriggerall=command!="holddown"\ntriggerall=command!="flight"\ntriggerall=StateType=A\ntriggerall=Power>=200\ntrigger1=ctrl || StateNo=550','value=11200')
 s+=ctl(-1,'Overdrive down Pause','ChangeState','triggerall=AILevel=0\ntriggerall=command="s"\ntriggerall=command="holddown"\ntriggerall=StateType!=A\ntriggerall=Var(40)=0\ntriggerall=Var(41)=0\ntriggerall=Power>=1500\ntrigger1=ctrl','value=520')
 s+=ctl(-1,'Energy-only self destruction','ChangeState','triggerall=AILevel=0\ntriggerall=command="x"\ntriggerall=StateType!=A\ntriggerall=Power>=3000\ntrigger1=ctrl','value=3000')
 s+=ctl(-1,'Hold Pause to charge','ChangeState','triggerall=AILevel=0\ntriggerall=command="hold_s"\ntriggerall=command!="holddown"\ntriggerall=StateType!=A\ntriggerall=Power<3000\ntrigger1=ctrl','value=500')
 for b,base in [('a',200),('b',210),('c',220)]:
  s+=ctl(-1,'Three-hit grounded chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=command!="holddown"\ntriggerall=StateType!=A\ntrigger1=ctrl\ntrigger2=(StateNo=200 || StateNo=210 || StateNo=220) && MoveHit && Time>=6\ntrigger3=(StateNo=201 || StateNo=211 || StateNo=221) && MoveHit && Time>=6',f'value={base}+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))','ignorehitpause=1')
  s+=ctl(-1,'Three-hit aerial chain','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{b}"\ntriggerall=StateType=A\ntriggerall=Var(12)<3\ntrigger1=ctrl\ntrigger2=StateNo>=600 && StateNo<=621 && MoveHit && Time>=6',f'value={base+400}+Var(12)','ignorehitpause=1')
 for name,n in [('FF',100),('BB',105)]:s+=ctl(-1,'Free double-tap dash','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType=S\ntrigger1=ctrl',f'value={n}')
 for name,n in [('holdup',40),('holddown',11),('holdfwd',20),('holdback',20)]:
  extra='\ntriggerall=StateType=S\ntriggerall=command!="holdup"\ntriggerall=command!="holddown"' if n==20 else ''
  if n in [11,20]:extra+='\ntriggerall=StateNo<120 || StateNo>155'
  s+=ctl(-1,'Movement','ChangeState',f'triggerall=AILevel=0\ntriggerall=command="{name}"\ntriggerall=StateType!=A\ntriggerall=StateNo!={n}{extra}\ntrigger1=ctrl',f'value={n}\nctrl={int(n!=40)}')
 s+=ctl(-1,'Finite confirmed CPU chain','ChangeState','triggerall=AILevel>0\ntriggerall=MoveHit\ntriggerall=Time>=6\ntrigger1=StateNo=200 || StateNo=201','value=StateNo+1','ignorehitpause=1')
 for n,cost,dist in [(3000,3000,140),(1020,500,260),(1200,200,290),(1010,350,110),(1210,350,170)]:s+=ctl(-1,'CPU legal technique','ChangeState',f'triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=P2MoveType!=H\ntriggerall=Power>={cost}\ntrigger1=P2BodyDist X<{dist}\ntrigger1=Random<AILevel*3',f'value={n}')
 s+=ctl(-1,'CPU close normal','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntriggerall=P2MoveType!=H\ntrigger1=P2BodyDist X<55','value=200')+ctl(-1,'CPU approach','ChangeState','triggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=ctrl\ntriggerall=StateType!=A\ntrigger1=P2BodyDist X>=55','value=20\nctrl=1')
 (CHAR/'DeltaKara.cmd').write_text(s)
def system():
 s='\n[Statedef -2]\n'
 for v in [14,40,41]:s+=c(-2,'Finite overdrive timer','VarAdd',f'!IsHelper && RoundState=2 && Var({v})>0',f'v={v}\nvalue=-1','ignorehitpause=1')
 s+=c(-2,'Overdrive attack power','AttackMulSet','!IsHelper','value=IfElse(Var(40)>0,1.2,1)')
 s+=c(-2,'Projectile power follows the same mode once','AttackMulSet','IsHelper','value=IfElse((Root,Var(40))>0,1.2,1)')
 s+=c(-2,'Finite aerial chain reset','VarSet','!IsHelper && StateType!=A','v=12\nvalue=0')+c(-2,'Flight reset on ground','VarSet','!IsHelper && StateType!=A','v=13\nvalue=0')
 s+=c(-2,'Dash foot exhaust','Helper','!IsHelper && (StateNo=100 || StateNo=105) && NumHelper(9500)=0','helpertype=Normal\nname="Propulsores"\nID=9500\nstateno=9500\npostype=P1\npos=0,0\nownpal=1\nkeyctrl=0')
 s+=c(-2,'Overdrive has a visible finite aura','Helper','!IsHelper && Var(40)>0 && NumHelper(9551)=0 && Life>0 && RoundState=2','helpertype=Normal\nname="Sobrecarga de Delta"\nID=9551\nstateno=9551\npostype=P1\npos=0,-40\nownpal=1\nkeyctrl=0')
 s+=c(-2,'Stop charge sound','StopSnd','!IsHelper && StateNo!=500','channel=3')+c(-2,'Clear effects at round end','RemoveExplod','!IsHelper && RoundState!=2')
 return s
def main():
 basics();normals();techniques();energy_helpers();utility();ultimate();commands()
 constants=(ROOT/'JuraShinju/JuraShinju.cns').read_text().split('[Statedef',1)[0];constants=constants[constants.index('[Data]'):].replace('life=1300','life=1200').replace('defence=115','defence=105').replace('height=84','height=82')
 (CHAR/'DeltaKara.cns').write_text('; Delta Kara: scientific ninja tools. Ultimate consumes energy only.\n'+constants+''.join(STATES)+system())
 (CHAR/'DeltaKara.air').write_text('; Recreated Delta poses; independent pink ocular and jet effects.\n'+''.join(AIR))
 common=(ROOT/'JuraShinju/JuraShinju_common.cns').read_text().replace('; Jura common states, derived from project native MUGEN guard and recovery.','; Delta native guard, dash and recovery states; project common implementation.')
 (CHAR/'DeltaKara_common.cns').write_text(common)
 (CHAR/'DeltaKara.def').write_text('''[Info]
name="Delta Kara"
displayname="Delta Kara"
versiondate=10,24,2026
mugenversion=1.1
author="Codex adaptation / recreated art / VayDra reference"
localcoord=320,240
pal.defaults=1
[Files]
sprite=DeltaKara.sff
sound=DeltaKara.snd
anim=DeltaKara.air
cmd=DeltaKara.cmd
cns=DeltaKara.cns
st=DeltaKara.cns
stcommon=DeltaKara_common.cns
[Palette Keymap]
a=1
b=1
c=1
x=1
y=1
z=1
s=1
''')
 (CHAR/'assets/moves.json').write_text(json.dumps(dict(moves=MOVES,ultimate=dict(state=3000,power_cost=3000,own_life_cost=0,damage_cap='min(450,45% opponent max life)',radius=155,startup=48),absorption=dict(window=[8,36],capacity=3,refund=220,physical_attacks_are_not_absorbed=True),anti_healing=dict(light_ticks=180,heavy_ticks=300),flight='Airborne RB+RT, arrows to steer, consumes energy; toggle off with RB+RT',overdrive=dict(power=1500,ticks=720),voices='Nonverbal effects only; no impersonated dialogue'),indent=2)+'\n')
 print('Delta runtime:',len(STATES),'combat states,',len(AIR),'animations; no self-damage from ultimate')
if __name__=='__main__':main()
