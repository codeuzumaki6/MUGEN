#!/usr/bin/env python3
"""Integrate the supplied Susanoo's nine attacks and original animated artwork."""
from pathlib import Path
import re,json
from hidari_susanoo_source import ACTION_IDS,export_action,SCALE
ROOT=Path(__file__).resolve().parents[1]
MOVES=[('Chidori','a','F',14600,500),('Corte de montana','a','B',14500,700),('Shinra Tensei','b','F',14700,600),('Chibaku Tensei','b','B',14800,800),('Kagetsuchi','c','F',14850,650),('Flecha de Indra','c','B',14900,3000)]
NORMALS=[('Puno','a','N',14200,0),('Patada','b','N',14300,0),('Espada ascendente','c','N',14400,0)]
SOURCE_ANIMS={14200:4200,14300:4300,14400:4400,14500:4500,14600:4600,14700:4700,14800:4800,14850:4850,14900:4900}
DURATIONS={14200:38,14300:38,14400:48,14500:112,14600:118,14700:72,14800:198,14850:100,14900:224}
COSTS={n:cost for _,b,d,n,cost in MOVES+NORMALS}

def install(m):
 c,ctl,state,hit,snd,effect,cast=m.c,m.ctl,m.state,m.hit,m.snd,m.effect,m.cast
 obsolete={9500,9470,9471,9472,9473,520,13000,13001}|{10000+x for x in [1000,1010,1020,1030,1040,1050,1400,1410,1420,1200,1210,1211,1430,1440]}|{10000+x+s for x in [200,210,220] for s in range(3)}
 m.states[:]=[s for s in m.states if int(re.search(r'\[Statedef (-?\d+)\]',s)[1]) not in obsolete]
 removed_actions={8645,8646,520}|set(range(9630,9638))
 # Remove unused old awakening attacks but preserve body banks for native
 # movement, hit recovery and aerial chains.
 m.air[:]=[s for s in m.air if int(re.search(r'\[Begin Action (\d+)\]',s)[1]) not in removed_actions]
 for a in ACTION_IDS:
  scale=1.25 if a==4750 else .4 if a==4900 else .5 if a in [4860,4990] else .6 if a==4950 else SCALE
  m.air.append(export_action(a,scale,loop=a in [4005,4050,4055,4056,1030,1450],box='-40,-30,40,30' if a==4950 else '2,-78,89,-10' if a==4600 else None))
 m.action(520,[(32,8),(33,8)],loop=True)
 # Genuine source normals and six specials. Hidari's original body is still
 # independently drawn in front; source art contains no embedded Sasuke.
 for n,a in SOURCE_ANIMS.items():
  poses=[(28,14),(29,24),(30,24),(28,20)] if n==14600 else [(32,12),(49,20),(50,20),(49,20),(32,12)]
  m.action(n,poses,loop=True)
  s=state(n,n,move='A',cost=COSTS[n],physics='N')
  s+=m.startup(n) if n>=14500 else snd(n,'Time=3',1,0,1,65)
  if n==14600:
   s+=c(n,'Chidori advances with the original extended punch','VelSet','Time>=26 && Time<55','x=2.4')+c(n,'Chidori stops advancing','VelSet','Time>=55','x=0')
   for t in [4,16,32,48,64,80]:s+=effect(n,f'Time={t}',21030,5 if t<32 else 65,-90 if t<32 else -45,.35,14)
   s+=snd(n,'Time=4',1,42,2)+snd(n,'Time=32',1,42,2)
  if n==14500:s+=cast(n,33,9578,65,0)+snd(n,'Time=33',1,41,2)
  if n==14700:s+=cast(n,30,9575,0,-48)+snd(n,'Time=30',1,41,2)
  if n==14800:
   for i,t in enumerate([30,50,70,90,110,130]):s+=cast(n,t,9570,f'IfElse(P2Dist X<270,P2Dist X,270)+{[-32,16,48,-16,32,0][i]}',-180)
   s+=snd(n,'Time=30',1,41,2)
  if n==14850:s+=cast(n,30,9580,85,-32)+snd(n,'Time=30',1,42,2)
  if n==14900:
   s+=cast(n,50,9595,55,-85)+effect(n,'Time=0',24005,0,10,1.0,52)+snd(n,'Time=30',1,42,2)+snd(n,'Time=50',1,41,2)
  s+=m.recover(n,DURATIONS[n]);m.states.append(s)
 # Hold activation exactly like the supplied Sasuke; releasing early costs no
 # power. The prior 20-second duration and finite cooldown are retained.
 n=520;s=state(n,520)+m.startup(n)+cast(n,0,9560,0,12)
 s+=c(n,'Cancel charge if Pause is released early','ChangeState','Time>10 && Time<100 && AILevel=0 && command!="hold_s"','value=0\nctrl=1')
 s+=c(n,'Pay only when the Susanoo manifests','PowerAdd','Time=100','value=-1500')+c(n,'Original Susanoo awakens','VarSet','Time=100','v=42\nvalue=1')+c(n,'Twenty-second awakening','VarSet','Time=100','v=40\nvalue=1200')+c(n,'Cooldown','VarSet','Time=100','v=41\nvalue=1500')+effect(n,'Time=100',24550,0,0,.85,24)+snd(n,'Time=100',1,41,2)+m.recover(n,122);m.states.append(s)
 n=9560;s=state(n,24005,'A',physics='N')+c(n,'Original yellow charging aura','BindToRoot','1','time=1\npos=0,12')+c(n,'Original charge proportions','AngleDraw','1','value=0\nscale=.7,.7')+c(n,'Source additive energy','Trans','1','trans=Add')+c(n,'Aura layering','SprPriority','1','value=-1')+c(n,'No push','PlayerPush','1','value=0')+c(n,'Charge aura lifetime','DestroySelf','Root,StateNo!=520 || Root,Time>=100 || RoundState!=2');m.states.append(s)
 def bind(n):
  return c(n,'Source Susanoo follows Hidari','BindToRoot','1','time=-1\npos=0,IfElse(Root,StateNo=14600,12,IfElse(Root,StateNo=14500 || Root,StateNo=14200 || Root,StateNo=14300,9,IfElse(Root,StateNo=14400 && Root,Time>=10,12,0)))')+c(n,'Follow caster facing','Turn','Facing!=Root,Facing','')+c(n,'Native original Susanoo size','AngleDraw','1',f'value=0\nscale=IfElse(Root,StateNo=14900,.4,{SCALE}),IfElse(Root,StateNo=14900,.4,{SCALE})')+c(n,'Yellow source artwork retains its color over bright stages','Trans','1','trans=AddAlpha\nalpha=256,48')+c(n,'Hidari stays in front','SprPriority','1','value=-1')+c(n,'No push','PlayerPush','1','value=0')+c(n,'No shadow','AssertSpecial','1','flag=NoShadow')+ctl(n,'Finite original guardian','DestroySelf','trigger1=Root,Var(42)=0\ntrigger2=Root,Life<=0\ntrigger3=RoundState!=2')
 n=9500;s=state(n,24050,'A',physics='N')+bind(n)
 s+=c(n,'Original idle and walking animations','VarSet','1','v=1\nvalue=IfElse(Root,StateNo=20 || Root,StateNo=100,24055,IfElse(Root,StateNo=105,24056,24050))')+c(n,'Change walk pose only on transition','ChangeAnim','Anim!=Var(1)','value=Var(1)')
 condition=' || '.join('Root,StateNo='+str(x) for x in SOURCE_ANIMS)
 s+=c(n,'Each attack resets its real hit definition','ChangeState',condition,'value=9510');m.states.append(s)
 n=9510;s=state(n,None,'A','A','N')+c(n,'Remember the exact original attack','VarSet','Time=0','v=0\nvalue=Root,StateNo')+bind(n)
 for root,a in SOURCE_ANIMS.items():s+=c(n,'Play original source animation','ChangeAnim',f'Time=0 && Var(0)={root}',f'value={20000+a}')
 for root,t,damage,fin in [(14200,7,85,True),(14300,4,95,True),(14400,9,115,True)]:
  s+=hit(n,t,damage,fin,airborne=True).replace(f'trigger1=Time={t}',f'trigger1=Time={t} && Var(0)={root}')
 for i,t in enumerate(range(31,80,6)):
  s+=hit(n,t,27,i==8,airborne=True,stun=18).replace(f'trigger1=Time={t}',f'trigger1=Time={t} && Var(0)=14600')
 s+=c(n,'Return to the original idle after the cast','ChangeState','Root,StateNo!=Var(0) || Root,MoveType=H','value=9500');m.states.append(s)
 # Repulsion uses the supplied expanding ring and actual radial contact.
 n=9575;s=state(n,24750,'A','A','N')+c(n,'Ring follows caster','BindToRoot','1','time=1\npos=0,-48')+c(n,'Source ring drawing','AngleDraw','1','value=0\nscale=1.25,1.25')+c(n,'Original ring blend','Trans','1','trans=Add')+hit(n,4,185,True,airborne=True)+c(n,'Ring dissipates','DestroySelf','Time>=23 || Root,MoveType=H || RoundState!=2');m.states.append(s)
 m.fxaction(29780,11350,range(13,30),3,box='-42,-105,42,0')
 n=9578;s=state(n,29780,'A','A','N',vel='6,0')+c(n,'Original mountain-cutting wave','AngleDraw','1','value=0\nscale=.5,.5')+c(n,'Source additive sword energy','Trans','1','trans=Add')+hit(n,0,270,True,airborne=True)+c(n,'Cutter is a finite physical wave','DestroySelf','MoveContact || Time>=50 || Root,MoveType=H || RoundState!=2');m.states.append(s)
 # The original Chibaku attack rains its source meteor sprites, rather than
 # replacing it with a new unrelated prison animation.
 m.fxaction(29700,19057,[7],3,box='-35,-35,35,35',loop=True)
 n=9570;s=state(n,29700,'A','A','N',vel='0,10')+c(n,'Original rock dimensions','AngleDraw','1','value=0\nscale=.24,.24')+hit(n,0,38,False,airborne=True,stun=28)+c(n,'Rock shatters on contact or ground','ChangeState','MoveContact || Pos Y>=-10','value=9571')+c(n,'Finite meteor flight','DestroySelf','Time>=35 || RoundState!=2');m.states.append(s)
 n=9571;s=state(n,21485,'A',physics='N')+c(n,'Stone shatters on the floor','PosSet','Time=0','y=0')+c(n,'Original meteor blast','AngleDraw','1','value=0\nscale=.45,.45')+snd(n,'Time=0',1,41,2,65)+c(n,'Finite fragments','DestroySelf','AnimTime=0 || Time>=32 || RoundState!=2');m.states.append(s)
 # Kagetsuchi uses the supplied subtractive black-flame blade.
 n=9580;s=state(n,24860,'A','A','N')+c(n,'Original black blade scale','AngleDraw','1','value=0\nscale=.5,.5')+c(n,'Original black-flame blend','Trans','1','trans=Sub')+c(n,'Keep the flame at the actual caster reach','BindToRoot','1','time=1\npos=85,-32')
 for i,t in enumerate([6,14,22,30,38,46]):s+=hit(n,t,32,i==5,airborne=True,stun=18)
 s+=c(n,'Flames expire and can be interrupted','DestroySelf','Time>=54 || Root,StateNo!=14850 || Root,MoveType=H || RoundState!=2');m.states.append(s)
 # Indra is a real downward-travelling arrow. Damage is assigned only after
 # actual contact and uses an absolute life-relative ceiling.
 n=9595;s=state(n,24950,'A','A','N',vel='12,0')+c(n,'Aim from the original bow toward body height','VelSet','Time=0','y=(-27-Pos Y)/IfElse(Abs(P2Dist X)>24,Abs(P2Dist X)/12.0,2)')+c(n,'Original arrow proportions and actual trajectory','AngleDraw','1','value=45-ATan(Vel Y/12.0)*180/Pi\nscale=.6,.6')+c(n,'Source Indra light','Trans','1','trans=Add')
 s+=hit(n,0,0,True,airborne=True).replace('fall=1','fall=0').replace('attr=A,SA','attr=A,HP')+'hitonce=1\n'+'\n'
 s+=c(n,'Bounded arrow damage belongs to the struck target','TargetLifeAdd','MoveHit && NumTarget>0','value=-IfElse((Target,LifeMax)<1000,Floor((Target,LifeMax)*.45),450)\nabsolute=1\nkill=1','persistent=0')
 s+=c(n,'Original Indra explosion appears at actual collision','ChangeState','MoveContact || Pos Y>=-6','value=9596')+c(n,'Arrow cannot outlive the round','DestroySelf','Time>=55 || FrontEdgeBodyDist<-100 || RoundState!=2');m.states.append(s)
 n=9596;s=state(n,24990,'A',physics='N')+c(n,'Original Indra impact','AngleDraw','1','value=0\nscale=.65,.65')+c(n,'Source explosion light','Trans','1','trans=Add')+snd(n,'Time=0',1,41,2)+c(n,'Impact is visual and damage is not repeated','DestroySelf','AnimTime=0 || Time>=80 || RoundState!=2');m.states.append(s)

 # MUGEN resets drawing parameters each rendered frame, including hitpause.
 # Source Sasuke explicitly keeps these controllers active during hitpause.
 source_ids=set(SOURCE_ANIMS)|{520,9500,9510,9560,9570,9571,9575,9578,9580,9595,9596}
 for i,block in enumerate(m.states):
  number=int(re.search(r'\[Statedef (-?\d+)\]',block)[1])
  if number not in source_ids:continue
  parts=re.split(r'(?=\n\[State )',block)
  for j,part in enumerate(parts):
   if re.search(r'(?im)^type=(AngleDraw|Trans|BindToRoot|SprPriority|PlayerPush|AssertSpecial)$',part) and 'ignorehitpause=' not in part:parts[j]=part.rstrip()+'\nignorehitpause=1\n'
  # ChangeAnim resets draw parameters. Apply source drawing after any change.
  draw=[part for part in parts if re.search(r'(?im)^type=(AngleDraw|Trans|SprPriority)$',part)]
  m.states[i]=''.join(part for part in parts if part not in draw)+''.join(draw)

def patch_commands():
 p=ROOT/'HidariShinju/HidariShinju.cmd';s=p.read_text();where=s.index('[Statedef -1]')+len('[Statedef -1]')
 from build_hidari_runtime import ctl
 new=''
 for name,b,d,n,cost in MOVES+NORMALS:
  command=('Chidori' if n==14600 else 'Garra' if n==14500 else 'Corriente' if n==14700 else 'Prision' if n==14800 else 'Ascendente' if n==14850 else 'Madera' if n==14900 else b)
  new+=ctl(-1,'Supplied Susanoo '+name,'ChangeState',f'triggerall=AILevel=0\ntriggerall=Var(42)=1\ntriggerall=StateType!=A\ntriggerall=command="{command}"\ntriggerall=Power>={cost}\ntrigger1=ctrl',f'value={n}')
 for cmd,n,cost,down in [('x',14900,3000,None),('Senbon',14500,700,False),('Marca',14700,600,False),('Barrido',14200,0,True),('Palma',14300,0,True),('Ramas',14400,0,True),('Tormenta',14800,800,True),('SalidaGarra',14850,650,True)]:
  cond='' if down is None else '\ntriggerall=command'+('=' if down else '!=')+'"holddown"'
  new+=ctl(-1,'Original Susanoo shortcut','ChangeState',f'triggerall=AILevel=0\ntriggerall=Var(42)=1\ntriggerall=StateType!=A\ntriggerall=command="{cmd}"\ntriggerall=Power>={cost}{cond}\ntrigger1=ctrl',f'value={n}')
 # All old attacks belong to base; the six source techniques own awakening.
 before=s[:where];after=s[where:];parts=re.split(r'(?=\n\[State )',after)
 for i,part in enumerate(parts):
  if 'type=ChangeState' in part and (re.search(r'(?m)^value=(?:\d+\+10000\*Var\(42\)|IfElse\(NumHelper)',part)) and not 'Aerial chain' in part:
   part=part.replace('type=ChangeState','type=ChangeState\ntriggerall=Var(42)=0',1)
  parts[i]=part
 p.write_text((before+new+''.join(parts)).rstrip()+'\n')
 # Source data is reviewable and keeps the six attack names and controls.
 p=ROOT/'HidariShinju/assets/moves.json';d=json.loads(p.read_text());d.update(susanoo_source='Sasuke BTM by Shingeki No Mugen; sprites Vovan99',susanoo_original_moves=MOVES,susanoo_original_normals=NORMALS,awakening_hold_ticks=100,ai_generated_susanoo=False);p.write_text(json.dumps(d,indent=2)+'\n')
