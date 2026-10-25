#!/usr/bin/env python3
"""Disposable actual-input Delta tests, including real projectile absorption and healing."""
from pathlib import Path
import fcntl,hashlib,json,os,re,shutil,subprocess,sys
from build_delta_runtime import MOVES
ROOT=Path(__file__).resolve().parents[1];ENGINE=Path('/workspace/.eida-tools/ikemen-nightly');TICKS=int(os.environ.get('DELTA_TICKS','440'));CAP=os.environ.get('DELTA_CAPTURE');AUDIO=os.environ.get('DELTA_AUDIO')
lock=open(ENGINE/'.native-character-check.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
cases=[]
for face in [1,-1]:
 for name,b,d,n,cost in MOVES:cases.append(dict(name=name,kind='move',face=face,b=b,d=d,state=n,cost=cost,distance=180 if n in [1020,1200,1440] else 48 if n in [1400,1410] else 105))
 for b,n in [('a',202),('b',212),('c',222)]:
  for kind in ['combo','air']:cases.append(dict(name=kind+' '+b,kind=kind,face=face,b=b,state=n+(400 if kind=='air' else 0),distance=40))
 for kind in ['ultimate','ultiblock','ultifar','ultismall','ultimate_one_hp','ultimate_empty','charge','awakening','flight','absorb_projectile','absorb_helper','absorb_melee','absorb_supermelee','antiheal','ray_short','ray_crouch','air_ray','ray_interrupt']:
  cases.append(dict(name=kind,kind=kind,face=face,distance=360 if kind=='ultifar' else 28 if kind.startswith('absorb_') and 'melee' in kind or kind=='ray_interrupt' else 180 if kind in ['antiheal','ray_short','ray_crouch','air_ray'] else 120))
if os.environ.get('DELTA_CASES'):cases=[c for c in cases if c['name'] in json.loads(os.environ['DELTA_CASES'])]
if os.environ.get('DELTA_FACE'):cases=[c for c in cases if c['face']==int(os.environ['DELTA_FACE'])]
if not os.environ.get('DELTA_TARGET_SCALE'):cases=[c for c in cases if c['kind']!='ray_short']
assert cases
char=ENGINE/'chars/DeltaCheck';dummy=ENGINE/'chars/DeltaDummy';shutil.copytree(ROOT/'DeltaKara',char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copyfile(char/'DeltaKara.def',char/'DeltaCheck.def');shutil.copyfile(dummy/'kfm.def',dummy/'DeltaDummy.def')
if os.environ.get('DELTA_TARGET_SCALE'):
 scale=float(os.environ['DELTA_TARGET_SCALE']);p=dummy/'kfm.cns';s=p.read_text(encoding='latin1')
 s=re.sub(r'(?im)^(xscale|yscale)\s*=.*$',lambda m:m[1]+'='+str(scale),s)
 s=re.sub(r'(?im)^height\s*=\s*([0-9.]+).*$',lambda m:'height='+str(float(m[1])*scale),s)
 p.write_text(s,encoding='latin1')
def fctl(kind,when,params,helper=False):return f'\n[State -2, Disposable Delta probe]\ntype={kind}\ntriggerall={"IsHelper" if helper else "!IsHelper"}\ntriggerall=RoundState=2\ntrigger1={when}\nignorehitpause=1\n{params}\n'
def inject(p,text):
 s=p.read_text(encoding='latin1')
 if '[Statedef -2]' in s:s=s.replace('[Statedef -2]','[Statedef -2]\n'+text,1)
 else:s+='\n[Statedef -2]\n'+text
 p.write_text(s,encoding='latin1')
p1=fctl('VarAdd','1','v=58\nvalue=1')+fctl('PlayerPush','1','value=0');p2=fctl('VarSet','NumEnemy>0','v=58\nvalue=EnemyNear,Var(58)')+fctl('PlayerPush','1','value=0')
p1+=fctl('DestroySelf',f'Root,Var(58)%{TICKS}=1','',True)
for i,case in enumerate(cases):
 face=case['face'];kind=case['kind'];dist=case['distance'];at=lambda t:f'Var(58)={i*TICKS+t}';win=lambda a,b:f'Var(58)>={i*TICKS+a} && Var(58)<={i*TICKS+b}'
 for side in [1,2]:
  b=fctl('PosSet',at(1),f'x={(-1 if side==1 else 1)*face*dist/2}\ny=0')+fctl('VelSet',at(1),'x=0\ny=0')+fctl('Turn',at(1)+f' && Facing!={face if side==1 else -face}','')
  b+=fctl('LifeSet',at(1),f'value={1 if side==1 and kind=="ultimate_one_hp" else 1200 if side==1 else 500 if kind=="ultismall" else 1000}')
  b+=fctl('PowerSet',at(1),f'value={0 if kind in ["charge","ultimate_empty"] else 3000}')+fctl('ChangeState',at(1),'value=0\nctrl=1')
  if side==1:p1+=b
  else:p2+=b
 for v in [12,13,14,40,41,44,46,50,51,52,53]:p1+=fctl('VarSet',at(2),f'v={v}\nvalue={1 if v==44 and case.get("state")==1440 else 0}')
 def press(t,b):return fctl('AssertInput',at(t),'flag='+b)
 def motion(b,d,t=28):
  if d in ['F','B']:
   lr=('R' if face==1 else 'L') if d=='F' else ('L' if face==1 else 'R')
   return fctl('AssertInput',win(t-8,t-3),'flag=D')+fctl('AssertInput',win(t-5,t+1),'flag='+lr)+press(t,b)
  return (fctl('AssertInput',win(t-4,t+1),'flag=D') if d=='D' else '')+press(t,b)
 if kind=='move':p1+=motion(case['b'],case['d'])
 elif kind in ['combo','air']:
  if kind=='air':p1+=press(18,'U');p2+=fctl('PosSet',at(20),'y=-85')+fctl('ChangeState',at(20),'value=9720\nctrl=0')
  p1+=press(36 if kind=='air' else 26,case['b'])+fctl('AssertInput',win(30,140)+(' && StateNo>=600 && StateNo<=621' if kind=='air' else ' && StateNo>=200 && StateNo<=221')+' && Time>=6 && MoveHit && Var(58)%3=0','flag='+case['b'])
 elif kind.startswith('ulti'):
  p1+=press(28,'x')
  if kind=='ultiblock':p2+=fctl('AssertInput',win(20,180),'flag='+('R' if face==1 else 'L'))
 elif kind=='charge':p1+=fctl('AssertInput',win(20,100),'flag=s')
 elif kind=='awakening':p1+=motion('s','D')
 elif kind=='flight':p1+=press(18,'U')+press(35,'y')+press(35,'z')+fctl('AssertInput',win(48,70),'flag=U')+press(100,'y')+press(100,'z')
 elif kind.startswith('absorb_'):
  p1+=motion('y','D')
  p2+=fctl('ChangeState',at(44),f'value={9700 if kind=="absorb_projectile" else 9702 if kind=="absorb_helper" else 9703 if kind=="absorb_supermelee" else 9701}\nctrl=0')
 elif kind in ['antiheal','ray_short','ray_crouch','air_ray','ray_interrupt']:
  p1+=motion('b','F') if kind=='antiheal' else motion('y','N',50 if kind=='air_ray' else 28)
  if kind=='air_ray':p1+=press(18,'U')
  if kind=='ray_short':p2+=fctl('ChangeState',at(4),'value=9721\nctrl=0')
  if kind=='ray_crouch':p2+=fctl('AssertInput',win(10,150),'flag=D')
  if kind=='ray_interrupt':p2+=fctl('ChangeState',at(36),'value=9701\nctrl=0')
  if kind=='antiheal':
   for t in [140,240,300,400]:p2+=fctl('LifeAdd',at(t),'value=40\nabsolute=1')
inject(char/'DeltaKara.cns',p1);inject(dummy/'kfm.cns',p2)
# The probe uses KFM's native poses plus a real, independently colliding orb.
from read_reference_sff import ReferenceSff
from build_roster_revision import Archive
reference=ReferenceSff(dummy/'kfm.sff');pack=Archive((ROOT/'DeltaKara/DeltaKara.sff').read_bytes());pack.entries.clear()
for key in reference.sprites:
 im,axis=reference.image(*key);pack.put(key,im,axis)
art=Archive((ROOT/'DeltaKara/DeltaKara.sff').read_bytes())
for n in range(4):im,axis=art.image((8800,n));pack.put((7777,n),im,axis)
pack.save(dummy/'kfm.sff')
with (dummy/'kfm.air').open('a') as f:f.write('\n[Begin Action 7777]\nClsn1Default: 1\n Clsn1[0]=-10,-10,10,10\nLoopstart\n'+''.join(f'7777,{n},0,0,3,,A\n' for n in range(4)))
with (dummy/'kfm.cns').open('a') as f:
 f.write('''
[Statedef 9700]
type=S
movetype=A
physics=S
anim=0
ctrl=0
[State 9700, Real engine projectile]
type=Projectile
trigger1=Time=0
projID=7777
projanim=7777
projhitanim=-1
projremanim=-1
projhits=1
projremovetime=50
projscale=.35,.35
offset=15,-50
velocity=10,0
attr=S,SP
damage=80,0
hitflag=MAF
guardflag=MA
pausetime=0,5
ground.hittime=15
ground.velocity=-2,0
sparkno=-1
[State 9700, End]
type=ChangeState
trigger1=Time>=25
value=0
ctrl=1
[Statedef 9702]
type=S
movetype=A
physics=S
anim=0
[State 9702, True projectile helper]
type=Helper
trigger1=Time=0
helpertype=Normal
ID=9710
name="Chakra projectile"
stateno=9710
postype=P1
pos=15,-50
ownpal=1
[State 9702, End]
type=ChangeState
trigger1=Time>=25
value=0
ctrl=1
[Statedef 9710]
type=A
movetype=A
physics=N
anim=7777
velset=10,0
[State 9710, Orb size]
type=AngleDraw
trigger1=1
scale=.35,.35
[State 9710, Contact]
type=HitDef
trigger1=Time=0
attr=A,SP
damage=80,0
hitflag=MAF
guardflag=MA
pausetime=0,5
ground.hittime=15
ground.velocity=-2,0
sparkno=-1
[State 9710, Remove]
type=DestroySelf
trigger1=MoveContact || Time>=50
[Statedef 9720]
type=A
movetype=I
physics=N
anim=41
velset=0,0
[State 9720, Air target]
type=Null
trigger1=1
[Statedef 9721]
type=S
movetype=I
physics=N
anim=0
[State 9721, Small target]
type=Null
trigger1=1
''')
 for n,attr in [(9701,'NA'),(9703,'SA')]:f.write(f'''\n[Statedef {n}]\ntype=S\nmovetype=A\nphysics=S\nanim=200\nctrl=0\n[State {n}, Real physical strike]\ntype=HitDef\ntrigger1=Time=0\nattr=S,{attr}\ndamage=60,0\nhitflag=MAF\nguardflag=MA\npausetime=3,5\nground.hittime=18\nground.velocity=-2,0\nsparkno=-1\n[State {n}, End]\ntype=ChangeState\ntrigger1=Time>=25\nvalue=0\nctrl=1\n''')
trace=ENGINE/'delta_trace.tsv';trace.write_text('');module=ENGINE/'external/mods/delta_checks.lua'
lua='''modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('delta_trace.tsv','w'));local last=-1;local rows={};local frames=0
CAPSETUP
hook.add('loop','delta_checks',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end;last=clock;frames=frames+1
 local case=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 if case>=COUNT then player(2);setLife(1);player(1);setTime(0);return end
 if rows[case]==nil then rows[case]={states={},damage=0,minimumLife=9999,minPower=3000,maxPower=0,stored=0,mark=0,jet=0,flight=0,overdrive=0,hp1=0,hp2=0,hp3=0,hp4=0} end
 local r=rows[case];local st=stateNo()
 if tick>5 then
  r.states[st]=true;r.minimumLife=math.min(r.minimumLife,life());r.minPower=math.min(r.minPower,power());r.maxPower=math.max(r.maxPower,power());r.stored=math.max(r.stored,var(44));r.overdrive=math.max(r.overdrive,var(40));r.jet=math.max(r.jet,numHelper(9500));if st==550 then r.flight=r.flight+1 end
  if numHelper(9200)>0 and helper(9200) then if stateNo()==9210 then r.mark=r.mark+1 end;player(1) end
  if DEBUG_ENABLED and tick%5==0 then
   f:write('DEBUG '..case..' '..tick..' root '..st..' x '..posX()..' y '..posY()..' v44 '..var(44)..' h '..numHelper());player(2);f:write(' p2 '..stateNo()..' x '..posX()..' face '..facing());player(1)
   for _,id in ipairs({9110,9200,9300,9500}) do if numHelper(id)>0 and helper(id) then f:write(' helper '..id..' st '..stateNo()..' t '..time()..' v1 '..var(1)..' target '..numTarget());player(1) end end
   f:write('\\n');f:flush()
  end
  player(2);r.damage=math.max(r.damage,1000-life());if tick==145 then r.hp1=life() end;if tick==245 then r.hp2=life() end;if tick==305 then r.hp3=life() end;if tick==415 then r.hp4=life() end;player(1)
 end
 if tick==TICKS-1 then local ss={};for n,_ in pairs(r.states) do ss[#ss+1]=tostring(n) end;table.sort(ss)
  f:write(case..'\\t'..table.concat(ss,',')..'\\t'..r.damage..'\\t'..r.minimumLife..'\\t'..r.minPower..'\\t'..r.maxPower..'\\t'..r.stored..'\\t'..r.mark..'\\t'..r.jet..'\\t'..r.flight..'\\t'..r.overdrive..'\\t'..r.hp1..'\\t'..r.hp2..'\\t'..r.hp3..'\\t'..r.hp4..'\\t'..stateNo()..'\\t'..tostring(ctrl())..'\\t'..numHelper()..'\\n');f:flush()
 end
 CAPTURE
end)
'''.replace('TICKS',str(TICKS)).replace('COUNT',str(len(cases))).replace('DEBUG_ENABLED','true' if os.environ.get('DELTA_DEBUG') else 'false')
if CAP:
 folder=Path(CAP);folder.mkdir(parents=True,exist_ok=True);assert not list(folder.glob('Ikemen_GO*.png')),'capture directory must be new'
 lua=lua.replace('CAPSETUP',"modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(folder)+'/')+")\nlocal images=assert(io.open("+json.dumps(str(folder/'frames.tsv'))+",'w'));local cues=assert(io.open("+json.dumps(str(folder/'cues.tsv'))+",'w'));local cap={index=0,pending=nil,last=-1000}")
 lua=lua.replace('CAPTURE','''
 if cap.prev~=st and ((st>=1000 and st<=3000) or st==500 or st==520 or st==550) then cues:write(frames..'\\t'..case..'\\t'..st..'\\n');cues:flush() end;cap.prev=st
 if cap.pending~=nil then local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb');if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\t'..case..'\\t'..tick..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end end
 if frames-cap.last>=4 and cap.pending==nil and tick>=12 and tick<=CAPEND then screenshot();cap.pending=frames;cap.last=frames end
 '''.replace('FOLDER',json.dumps(str(folder)+'/')).replace('CAPEND','430' if any(c['kind']=='antiheal' for c in cases) else '210'))
else:lua=lua.replace('CAPSETUP','').replace('CAPTURE','')
module.write_text(lua);debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/delta_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
if AUDIO:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=AUDIO,SDL_DISKAUDIODELAY='46')
try:r=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','DeltaCheck','-p1.ai','0','-p2','DeltaDummy','-p2.ai','0','-rounds','1','-time','9999']+(['-speed','0'] if CAP else ['-speedtest'])+([] if AUDIO else ['-nosound']),cwd=ENGINE,env=env,capture_output=True,text=True,timeout=300)
finally:debug.write_text(saved);module.rename(module.with_name('-delta_checks.lua'))
print(r.stdout[-2500:]);print(r.stderr[-2500:]);assert r.returncode==0,'native engine failure'
assert not re.search(r"WARNING: Delta Kara's[^\n]*Unknown state controller parameter",r.stdout+r.stderr)
rows=[line.split('\t') for line in trace.read_text().splitlines() if not line.startswith('DEBUG')];assert len(rows)==len(cases),(len(rows),len(cases));reports=[]
for case,row in zip(cases,rows):
 ss=set(map(int,row[1].split(',')));damage=int(row[2]);life=int(row[3]);power=int(row[4]);kind=case['kind'];bad=[]
 if kind=='move':
  if case['state'] not in ss or power!=3000-case['cost']:bad.append('input or energy cost mismatch')
  if case['state']!=1430 and damage<=0:bad.append('attack did not hit')
 if kind in ['combo','air'] and (case['state'] not in ss or damage<100):bad.append('confirmed three-hit chain failed')
 if kind in ['ultimate','ultimate_one_hp','ultismall']:
  expected=450
  if 3000 not in ss or power!=0 or damage!=(500+expected if kind=='ultismall' else expected):bad.append('finite explosion cost/damage failed')
  if life!=(1 if kind=='ultimate_one_hp' else 1200):bad.append('ultimate removed own life')
 if kind in ['ultiblock','ultifar','ultimate_empty'] and (damage or life!=1200):bad.append('miss, guard, or empty-meter ultimate failed')
 if kind in ['absorb_projectile','absorb_helper'] and (life!=1200 or int(row[6])!=1 or 1431 not in ss):bad.append('real energy projectile was not absorbed')
 if kind in ['absorb_melee','absorb_supermelee'] and (life>=1200 or int(row[6])):bad.append('absorption incorrectly blocks physical attacks')
 if kind=='antiheal' and (int(row[7])==0 or not int(row[11])==int(row[12])==int(row[13]) or int(row[14])!=int(row[13])+40):bad.append('finite anti-healing or expiry failed')
 if kind in ['ray_short','ray_crouch','air_ray'] and damage==0:bad.append('aim did not reach target body')
 if kind=='flight' and (550 not in ss or int(row[9])<15 or not int(row[8])):bad.append('real jet flight failed')
 if kind=='charge' and (int(row[5])<1000 or 500 not in ss):bad.append('energy charge failed')
 if kind=='awakening' and (520 not in ss or int(row[10])<690 or power!=1500):bad.append('finite overdrive failed')
 if TICKS>=400 and kind!='awakening' and int(row[17]):bad.append('helper did not expire')
 record=dict(case=case,states=sorted(ss),damage=damage,minimum_life=life,min_power=power,max_power=int(row[5]),absorbed=int(row[6]),mark_frames=int(row[7]),jets=int(row[8]),flight_frames=int(row[9]),overdrive=int(row[10]),healing_samples=list(map(int,row[11:15])),end_state=int(row[15]),ctrl=row[16],helpers=int(row[17]),failures=bad);reports.append(record);print('FAIL' if bad else 'PASS',case['name'],case['face'],damage,life,power,bad)
files=['DeltaKara.'+s for s in ['def','cns','cmd','air','sff','snd']]+['DeltaKara_common.cns'];report=dict(runtime_sha256=hashlib.sha256(b''.join((ROOT/'DeltaKara'/f).read_bytes() for f in files)).hexdigest(),cases=reports)
out=ROOT/'previews'/os.environ.get('DELTA_REPORT','DeltaKara_capture_checks.json' if CAP else 'DeltaKara_engine_checks.json');out.write_text(json.dumps(report,indent=2)+'\n');assert not any(r['failures'] for r in reports),str(out);print('PASS',len(reports),'actual-input Delta engine checks')
