#!/usr/bin/env python3
"""Disposable engine fixtures: real inputs, collision, form expiry and guards."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,sys
from build_mitsuki_runtime import MOVES
ROOT=Path(__file__).resolve().parents[1];ENGINE=Path('/workspace/.eida-tools/ikemen-nightly');TICKS=int(os.environ.get('MITSUKI_TICKS','360'));CAP=os.environ.get('MITSUKI_CAPTURE');AUDIO=os.environ.get('MITSUKI_AUDIO');LOW=os.environ.get('MITSUKI_LOW')=='1';DUMMYLIFE=500 if LOW else 1000 if CAP else 10000
RANGE=os.environ.get('MITSUKI_RANGE')=='1';SCALE=float(os.environ.get('MITSUKI_TARGET_SCALE','1'));CROUCH=os.environ.get('MITSUKI_TARGET_CROUCH')=='1'
cases=[]
for form in [0,1]:
 for face in [1,-1]:
  for name,b,d,n,cost in MOVES:cases.append(dict(name=name,kind='move',form=form,face=face,b=b,d=d,state=n+form*10000,cost=round(cost*.8) if form else cost,distance=45 if n in [1400,1410,1040,1430,1440] else 110))
  for b,base in [('a',200),('b',210),('c',220)]:
   for kind in ['combo','air']:cases.append(dict(name=kind+' '+b,kind=kind,form=form,face=face,b=b,state=base+(400 if kind=='air' else 0)+2+form*10000,distance=38))
  for kind in ['ultimate','ultiblock','ultijump','ultifar','empty','recovery','guard','crouchguard','charge','chargehit']:
   cases.append(dict(name=kind,kind=kind,form=form,face=face,distance=370 if kind=='ultifar' else 40 if kind in ['recovery','guard','crouchguard','chargehit'] else 90))
  for b in ['L','R']:cases.append(dict(name='dash '+b,kind='dash',form=form,face=face,b=b,state=100 if (b=='R')==(face==1) else 105,distance=120))
for face in [1,-1]:
 for kind in ['awakening','expire_attack','expire_hurt','no_awake']:
  cases.append(dict(name=kind,kind=kind,form=1 if kind.startswith('expire') else 0,face=face,distance=45 if kind=='expire_hurt' else 110))
if RANGE:
 cases=[]
 for form in [0,1]:
  for face in [1,-1]:
   for name,b,d,n,cost in [m for m in MOVES if m[3] in [1020,1430]]:
    for distance,outcome in [(60,'hit'),(210,'hit'),(400,'miss' if n==1430 else 'hit'),(210,'guard'),(210,'jump'),(45,'interrupt')]:
     if outcome=='interrupt' and SCALE<1:continue
     cases.append(dict(name=name,kind='ray',form=form,face=face,b=b,d=d,state=n+form*10000,cost=round(cost*.8) if form else cost,distance=distance,outcome=outcome))
if LOW:cases=[dict(name='ultimate',kind='ultimate',form=form,face=face,distance=90) for form in [0,1] for face in [1,-1]]
if os.environ.get('MITSUKI_CASES'):cases=[c for c in cases if c['name'] in json.loads(os.environ['MITSUKI_CASES'])]
if os.environ.get('MITSUKI_FORM'):cases=[c for c in cases if c['form']==int(os.environ['MITSUKI_FORM'])]
if os.environ.get('MITSUKI_FACE'):cases=[c for c in cases if c['face']==int(os.environ['MITSUKI_FACE'])]
if os.environ.get('MITSUKI_ALL_SPECIALS'):
 cases=[c for c in cases if c['kind']=='move' and c['face']==1]
 for case in cases:
  if case['state']%10000 in [1020,1430]:case['distance']=210
if os.environ.get('MITSUKI_DEMO'):
 order=[('Raiton',0),('Fuuton',0),('Asalto',0),('awakening',0),('combo b',1),('Serpientes',1),('Fuuton',1),('ultimate',1)]
 cases=[next(c for c in cases if (c['name'],c['form'])==v and c['face']==1) for v in order]
assert cases
char=ENGINE/'chars/MitsukiCheck';dummy=ENGINE/'chars/MitsukiDummy';shutil.copytree(ROOT/'MitsukiTBV',char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True);shutil.copy2(char/'MitsukiTBV.def',char/'MitsukiCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'MitsukiDummy.def')
def fctl(kind,when,params):return f'\n[State -2, Disposable test fixture]\ntype={kind}\ntriggerall=!IsHelper\ntriggerall=RoundState=2\ntrigger1={when}\nignorehitpause=1\n{params}\n'
p1=fctl('VarAdd','1','v=58\nvalue=1');p2=fctl('VarSet','NumEnemy>0','v=58\nvalue=EnemyNear,Var(58)')
if RANGE:
 p1+=fctl('ScreenBound','1','value=0\nmovecamera=0,0');p2+=fctl('ScreenBound','1','value=0\nmovecamera=0,0')
for i,case in enumerate(cases):
 base=i*TICKS;kind=case['kind'];face=case['face'];dist=case['distance'];at=lambda t:f'Var(58)={base+t}';window=lambda a,b:f'Var(58)>={base+a} && Var(58)<={base+b}'
 for side in [1,2]:
  block=fctl('PosSet',at(1),f'x={(-1 if side==1 else 1)*face*dist/2}\ny=0')+fctl('VelSet',at(1),'x=0\ny=0')+fctl('Turn',at(1)+f' && Facing!={face if side==1 else -face}','')
  block+=fctl('LifeSet',at(1),f'value={1200 if side==1 else DUMMYLIFE}')+fctl('PowerSet',at(1),f'value={0 if kind in ["charge","chargehit","empty","no_awake"] else 3000}')
  for v in [12,20,40,41,42]:block+=fctl('VarSet',at(1),f'v={v}\nvalue={1 if v==42 and case["form"] else 800 if v==40 and case["form"] else 0}')
  block+=fctl('ChangeState',at(1),'value=0\nctrl=1')
  if side==1:p1+=block
  else:p2+=block
 def press(t,b):return fctl('AssertInput',at(t),'flag='+b)
 def motion(b,d,t=28):
  if d in ['F','B']:
   lr=('R' if face==1 else 'L') if d=='F' else ('L' if face==1 else 'R')
   return fctl('AssertInput',window(t-8,t-3),'flag=D')+fctl('AssertInput',window(t-5,t+1),'flag='+lr)+press(t,b)
  return (fctl('AssertInput',window(t-4,t+1),'flag=D') if d=='D' else '')+press(t,b)
 if kind in ['move','ray']:
  p1+=motion(case['b'],case['d'])
  if case['state']%10000==1440:p2+=fctl('ChangeState',at(46),'value=9700\nctrl=0')
  if kind=='ray' and case['outcome']=='guard':
   p2+=fctl('PosSet',window(18,140),f'x={face*dist/2}\ny=0')+fctl('AssertInput',window(18,140),'flag='+('R' if face==1 else 'L'))
  if kind=='ray' and case['outcome']=='interrupt':p2+=fctl('ChangeState',at(52),'value=9700\nctrl=0')
  if kind=='ray' and case['outcome']=='jump':p2+=fctl('PosSet',at(20),'y=-170')+fctl('ChangeState',at(20),'value=9702\nctrl=0')
 elif kind in ['combo','air']:
  if kind=='air':p1+=press(18,'U');p2+=fctl('PosSet',at(20),'y=-95')+fctl('ChangeState',at(20),'value=9702\nctrl=0')
  p1+=press(36 if kind=='air' else 26,case['b'])
  rng='StateNo%10000>=600 && StateNo%10000<=621' if kind=='air' else '(StateNo%10000=200 || StateNo%10000=201 || StateNo%10000=210 || StateNo%10000=211 || StateNo%10000=220 || StateNo%10000=221)'
  p1+=fctl('AssertInput',f'{window(30,150)} && ({rng}) && Time>=6 && MoveHit && Var(58)%3=0','flag='+case['b'])
 elif kind=='dash':p1+=press(20,case['b'])+press(27,case['b'])
 elif kind in ['charge','chargehit']:
  p1+=fctl('AssertInput',window(20,80),'flag=s')
  if kind=='chargehit':p2+=fctl('ChangeState',at(43),'value=9700\nctrl=0')
 elif kind in ['awakening','no_awake']:p1+=motion('s','D')
 elif kind=='expire_attack':p1+=fctl('VarSet',at(22),'v=40\nvalue=30')+motion('a','B')
 elif kind=='expire_hurt':p1+=fctl('VarSet',at(22),'v=40\nvalue=30');p2+=fctl('ChangeState',at(43),'value=9701\nctrl=0')
 elif kind=='recovery':p2+=fctl('ChangeState',at(24),'value=9701\nctrl=0')
 elif kind in ['guard','crouchguard']:
  p1+=fctl('AssertInput',window(20,100),'flag='+('L' if face==1 else 'R'))
  if kind=='crouchguard':p1+=fctl('AssertInput',window(20,100),'flag=D')
  p1+=fctl('PosSet',window(30,70),f'x={-face*20}\ny=0')
  p2+=fctl('PosSet',window(30,70),f'x={face*20}\ny=0')+fctl('ChangeState',at(43),'value=9700\nctrl=0')
 elif kind in ['ultimate','ultiblock','ultijump','ultifar','empty']:
  p1+=press(28,'x')
  if kind=='ultiblock':p2+=fctl('AssertInput',window(18,170),'flag='+('R' if face==1 else 'L'))
  if kind=='ultijump':p2+=fctl('PosSet',at(20),'y=-170')+fctl('ChangeState',at(20),'value=9702\nctrl=0')
if CROUCH:p2+=fctl('AssertInput','1','flag=D')
for path,fixture in [(char/'MitsukiTBV.cns',p1),(dummy/'kfm.cns',p2)]:
 s=path.read_text(encoding='latin1');s=s.replace('[Statedef -2]','[Statedef -2]\n'+fixture,1) if '[Statedef -2]' in s else s+'\n[Statedef -2]\n'+fixture
 if path==dummy/'kfm.cns':
  s=re.sub(r'(?im)^life\s*=.*$',f'life={DUMMYLIFE}',s,count=1)
  for dim in ['xscale','yscale']:s=re.sub(rf'(?im)^{dim}\s*=.*$',f'{dim}={SCALE}',s,count=1)
 path.write_text(s,encoding='latin1')
with (dummy/'kfm.cns').open('a') as f:
 for n,fall in [(9700,0),(9701,1)]:f.write(f'\n[Statedef {n}]\ntype=S\nmovetype=A\nphysics=S\nanim=400\nctrl=0\nvelset=0,0\n[State {n}, Actual opponent strike]\ntype=HitDef\ntrigger1=Time=0\nattr=S,NA\ndamage=60,0\nhitflag=MAF\nguardflag=MA\npausetime=5,8\nground.hittime=20\nground.velocity=-2,{-6 if fall else 0}\nair.velocity=-2,-4\nfall={fall}\nfall.recover=0\nsparkno=-1\n[State {n}, End]\ntype=ChangeState\ntrigger1=Time>=24\nvalue=0\nctrl=1\n')
 f.write('\n[Statedef 9702]\ntype=A\nmovetype=I\nphysics=N\nanim=41\nvelset=0,0\nctrl=0\n[State 9702, Air target]\ntype=Null\ntrigger1=1\n')
trace=ENGINE/'mitsuki_trace.tsv';trace.write_text('');module=ENGINE/'external/mods/mitsuki_checks.lua'
lua="""modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('mitsuki_trace.tsv','w'));local last=-1;local rows={};local frames=0
CAPSETUP
hook.add('loop','mitsuki_checks',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end
 last=clock;frames=frames+1
 local case=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 if case>=CASECOUNT then player(2);setLife(1);player(1);setTime(0);return end
 if rows[case]==nil then rows[case]={states={},damage=0,received=0,apex=0,minPower=3000,maxPower=0,sage=0,aura=0,dash=0,wrong=0,distance=0,guard=0,beamHurt=0,orochi=0,wrongOrochi=0} end
 local r=rows[case];local st=stateNo()
 if tick==8 then r.startDist=p2DistX();r.distance=p2DistX() end
 if tick>4 then
  r.states[st]=true;r.received=math.max(r.received,1200-life());r.minPower=math.min(r.minPower,power());r.maxPower=math.max(r.maxPower,power());r.apex=math.min(r.apex,posY());r.sage=math.max(r.sage,var(40));r.aura=math.max(r.aura,numHelper(9550))
  if st==100 or st==105 then r.dash=(r.startDist-p2DistX())*FACES[case+1] end
  if var(42)==1 and spriteVar('group')~=1 and st~=520 then r.wrong=r.wrong+1 end
  if moveType()=='H' and numHelper(9430)+numHelper(9431)>0 then r.beamHurt=r.beamHurt+1 end
  if numHelper(9433)>0 and helper(9433) then r.orochi=r.orochi+1;if spriteVar('group')~=8950 then r.wrongOrochi=r.wrongOrochi+1 end;player(1) end
  player(2);r.damage=math.max(r.damage,DUMMYLIFE-life());r.victim=stateNo();if stateNo()>=150 and stateNo()<=155 then r.guard=1 end;player(1)
 end
 if tick==TICKS-1 then
  local ss={};for n,_ in pairs(r.states) do table.insert(ss,n) end;table.sort(ss);for i,v in ipairs(ss) do ss[i]=tostring(v) end
  f:write(case..'\\t'..table.concat(ss,',')..'\\t'..r.damage..'\\t'..r.received..'\\t'..r.minPower..'\\t'..r.maxPower..'\\t'..r.sage..'\\t'..var(40)..'\\t'..var(42)..'\\t'..stateNo()..'\\t'..r.victim..'\\t'..r.dash..'\\t'..r.aura..'\\t'..numHelper()..'\\t'..numHelper(9550)..'\\t'..r.wrong..'\\t'..tostring(ctrl())..'\\t'..r.distance..'\\t'..r.guard..'\\t'..r.apex..'\\t'..r.beamHurt..'\\t'..r.orochi..'\\t'..r.wrongOrochi..'\\n');f:flush()
 end
 CAPTURE
end)
""".replace('TICKS',str(TICKS)).replace('CASECOUNT',str(len(cases))).replace('DUMMYLIFE',str(DUMMYLIFE)).replace('FACES','({'+','.join(str(c['face']) for c in cases)+'})')
if CAP:
 lua=lua.replace('local clock=var(58);','frames=frames+1;local clock=var(58);').replace('last=clock;frames=frames+1','last=clock')
 folder=Path(CAP).resolve();folder.mkdir(parents=True,exist_ok=True)
 lua=lua.replace('CAPSETUP',"modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(folder)+'/')+")\nlocal images=assert(io.open("+json.dumps(str(folder/'frames.tsv'))+",'w'));local cues=assert(io.open("+json.dumps(str(folder/'cues.tsv'))+",'w'));local cap={index=0,pending=nil,last=-1000}")
 lua=lua.replace('CAPTURE',"""
 if cap.prev~=st and (st%10000>=1000 and st%10000<=3000 or st==520) then cues:write(frames..'\\t'..st..'\\n');cues:flush() end;cap.prev=st
 if cap.pending~=nil then local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb');if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\t'..case..'\\t'..tick..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end end
 if frames-cap.last>=CAPSTEP and cap.pending==nil and tick>=12 and tick<=CAPEND then screenshot();cap.pending=frames;cap.last=frames end
 """.replace('FOLDER',json.dumps(str(folder)+'/')).replace('CAPEND',str(min(TICKS-12,230))).replace('CAPSTEP','(st==11020 and 2 or 6)' if os.environ.get('MITSUKI_ALL_SPECIALS') else '4'))
else:lua=lua.replace('CAPSETUP','').replace('CAPTURE','')
module.write_text(lua);debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/mitsuki_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
if AUDIO:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=AUDIO,SDL_DISKAUDIODELAY='46')
try:
 run=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','MitsukiCheck','-p1.ai','0','-p2','MitsukiDummy','-p2.ai','0','-rounds','1','-time','9999']+(['-speed','0'] if CAP else ['-speedtest'])+([] if AUDIO else ['-nosound']),cwd=ENGINE,env=env,capture_output=True,text=True,timeout=240 if CAP else 120)
 print(run.stdout);print(run.stderr);assert run.returncode==0,'Engine failure'
 assert not re.search(r"WARNING: Mitsuki TBV's[^\n]*Unknown state controller parameter",run.stdout+run.stderr)
finally:
 debug.write_text(saved)
 if module.exists():module.rename(module.with_name('-mitsuki_checks.lua'))
rows={int(l.split('\t')[0]):l.split('\t') for l in trace.read_text().splitlines()};assert sorted(rows)==list(range(len(cases))),('Missing traces',sorted(rows))
report=[]
for i,case in enumerate(cases):
 row=rows[i];ss=set(map(int,row[1].split(',')));damage=int(row[2]);received=int(row[3]);power=int(row[4]);endstate=int(row[9]);form=case['form'];kind=case['kind'];bad=[]
 if kind in ['move','ray']:
  if case['state'] not in ss:bad.append('raw motion did not enter requested special')
  if (kind=='move' or case['outcome']=='hit') and damage<=0:bad.append('no real collision damage')
  if kind=='ray' and case['outcome'] in ['guard','jump','miss'] and damage:bad.append('ray hit through guard, high jump or outside beam range')
  if kind=='ray' and case['outcome']=='interrupt' and (received<=0 or int(row[20])>1):bad.append('ranged cast did not stop on a real incoming hit')
  if kind=='ray' and case['outcome']=='guard' and int(row[18])!=1:bad.append('ray never contacted actual guard')
  if kind=='ray' and abs(float(row[17])-case['distance'])>10:bad.append('fixture did not establish the stated real distance')
  if power>3000-case['cost']:bad.append('cost not spent')
  if case['state']%10000==1440 and 1441+form*10000 not in ss:bad.append('counter did not trigger')
  if case['state']%10000==1040 and float(row[19])>-25:bad.append('rising kick did not actually leave the floor')
  if case['state']%10000==1400 and float(row[19])!=0:bad.append('low slide left the floor')
  if case['state']%10000==1410 and not -28<float(row[19])<-8:bad.append('uppercut rise is not distinct from kick and slide')
 if kind in ['combo','air'] and (case['state'] not in ss or not 140<=damage<=310):bad.append('three-hit chain failed')
 if kind=='ultimate':
  budget=min(450 if form else 360,round(DUMMYLIFE*(.45 if form else .36)))
  if 3001+form*10000 not in ss or damage!=budget or int(row[10]) in [3010,3011]:bad.append('confirmed ultimate budget or release failed')
 if kind in ['ultiblock','ultijump','ultifar','empty'] and (damage or 3001+form*10000 in ss):bad.append('ultimate connected despite guard/miss/no meter')
 if kind=='dash' and (case['state'] not in ss or abs(float(row[11]))<50 or (float(row[11])>0)!=(case['b']=='R') or power<3000):bad.append('free double-tap dash direction or travel failed')
 if kind=='charge' and (500 not in ss or int(row[5])<900 or int(row[12])!=1):bad.append('charge/aura failed')
 if kind=='chargehit' and (not received or 500 not in ss):bad.append('charge cannot be interrupted')
 if kind in ['guard','crouchguard'] and (received or (150 if kind=='guard' else 152) not in ss):bad.append('manual guard failed')
 if kind=='recovery' and (5120 not in ss or endstate!=0):bad.append('knockdown recovery failed')
 if kind=='awakening' and (520 not in ss or int(row[6])<1190 or (TICKS>=1250 and int(row[8])!=0)):bad.append('awakening activation or expiry failed')
 if kind.startswith('expire') and (int(row[8]) or endstate!=0):bad.append('form expiry left sprite, attack or recoil stuck')
 if kind=='no_awake' and (520 in ss or int(row[8])):bad.append('awakening allowed without energy')
 if int(row[15])>1:bad.append('Sage form showed a base body')
 if case.get('state')==11020 and (int(row[21])==0 or int(row[22])!=0):bad.append('Orochi Ikazuchi did not use its green serpent sprite group')
 if int(row[13])!=int(row[14]):bad.append('combat helper remained after recovery')
 result=dict(case=case,states=sorted(ss),damage=damage,received=received,min_power=power,max_power=int(row[5]),max_sage_timer=int(row[6]),end_timer=int(row[7]),end_form=int(row[8]),end_state=endstate,victim_end=int(row[10]),dash_distance=float(row[11]),aura=int(row[12]),end_helpers=int(row[13]),wrong_sage_body_frames=int(row[15]),actual_start_distance=float(row[17]),actual_guard=int(row[18]),jump_apex=float(row[19]),beam_during_hurt=int(row[20]),orochi_serpent_frames=int(row[21]),wrong_orochi_sprite_frames=int(row[22]),target_scale=SCALE,target_crouching=CROUCH,failures=bad);report.append(result);print('FAIL' if bad else 'PASS',case['name'],form,case['face'],damage,bad)
files=[f'MitsukiTBV.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['MitsukiTBV_common.cns'];runtime=hashlib.sha256(b''.join((ROOT/'MitsukiTBV'/n).read_bytes() for n in files)).hexdigest()
out=ROOT/'previews'/os.environ.get('MITSUKI_REPORT',('MitsukiTBV_capture_checks.json' if CAP else f'MitsukiTBV_rays_{SCALE}_{int(CROUCH)}_checks.json' if RANGE else 'MitsukiTBV_low_life_checks.json' if LOW else 'MitsukiTBV_engine_checks.json'));out.write_text(json.dumps(dict(runtime_sha256=runtime,cases=report),indent=2)+'\n');assert not any(r['failures'] for r in report),str(out);print('PASS',len(report),'Mitsuki actual-input engine cases')
