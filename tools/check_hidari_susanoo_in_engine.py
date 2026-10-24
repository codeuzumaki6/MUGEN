#!/usr/bin/env python3
"""Disposable engine fixtures: real inputs, collision, form expiry and guards."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,sys,fcntl
from build_hidari_susanoo import MOVES,NORMALS
ROOT=Path(__file__).resolve().parents[1];ENGINE=Path('/workspace/.eida-tools/ikemen-nightly');TICKS=int(os.environ.get('HIDARI_TICKS','360'));CAP=os.environ.get('HIDARI_CAPTURE');AUDIO=os.environ.get('HIDARI_AUDIO');LOW=os.environ.get('HIDARI_LOW')=='1';DUMMYLIFE=500 if LOW else 1000 if CAP else 10000
RANGE=os.environ.get('HIDARI_RANGE')=='1';SCALE=float(os.environ.get('HIDARI_TARGET_SCALE','1'));CROUCH=os.environ.get('HIDARI_TARGET_CROUCH')=='1'
# The engine fixtures share character files and debug.lua. Reject concurrent runs.
_engine_lock=open(ENGINE/'.native-character-check.lock','w')
fcntl.flock(_engine_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
cases=[]
for face in [1,-1]:
 for name,b,d,n,cost in NORMALS+MOVES:cases.append(dict(name=name,kind='move',form=1,face=face,b=b,d=d,state=n,cost=cost,distance=40 if n<14500 else 80 if n==14600 else 110 if n!=14900 else 90))
 for kind in ['ultimate','ultiblock','ultijump','empty','recovery','guard','crouchguard','charge','chargehit','expire_attack','expire_hurt']:
  cases.append(dict(name=kind,kind=kind,form=1,face=face,distance=40 if kind in ['recovery','guard','crouchguard','chargehit','expire_hurt'] else 90))
 for b in ['L','R']:cases.append(dict(name='dash '+b,kind='dash',form=1,face=face,b=b,state=100 if (b=='R')==(face==1) else 105,distance=120))
 for kind in ['awakening','no_awake','cancel_awake']:cases.append(dict(name=kind,kind=kind,form=0,face=face,distance=110))
if LOW:cases=[dict(name='ultimate',kind='ultimate',form=1,face=face,distance=90) for face in [1,-1]]
if RANGE:
 cases=[]
 for face in [1,-1]:
  for name,b,d,n,cost in MOVES:
   for distance,outcome in [(60,'hit'),(110,'hit'),(400 if n==14800 else 350,'hit' if n in [14500,14900] else 'miss'),(110,'guard'),(110,'airhit' if n in [14700,14800] else 'jump'),(45,'interrupt')]:
    if outcome=='interrupt' and SCALE<1:continue
    cases.append(dict(name=name,kind='ray',form=1,face=face,b=b,d=d,state=n,cost=cost,distance=distance,outcome=outcome))
if os.environ.get('HIDARI_CASES'):cases=[c for c in cases if c['name'] in json.loads(os.environ['HIDARI_CASES'])]
if os.environ.get('HIDARI_FORM'):cases=[c for c in cases if c['form']==int(os.environ['HIDARI_FORM'])]
if os.environ.get('HIDARI_FACE'):cases=[c for c in cases if c['face']==int(os.environ['HIDARI_FACE'])]
if os.environ.get('HIDARI_ALL_SPECIALS'):
 cases=[c for c in cases if c['face']==1 and c['kind'] in ['move','awakening']]
 for c in cases:
  if 'state' not in c:c['state']=520
assert cases
char=ENGINE/'chars/HidariCheck';dummy=ENGINE/'chars/HidariDummy';shutil.copytree(ROOT/'HidariShinju',char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True);shutil.copy2(char/'HidariShinju.def',char/'HidariCheck.def');shutil.copy2(dummy/'kfm.def',dummy/'HidariDummy.def')
def fctl(kind,when,params):return f'\n[State -2, Disposable test fixture]\ntype={kind}\ntriggerall=!IsHelper\ntriggerall=RoundState=2\ntrigger1={when}\nignorehitpause=1\n{params}\n'
p1=fctl('VarAdd','1','v=58\nvalue=1');p2=fctl('VarSet','NumEnemy>0','v=58\nvalue=EnemyNear,Var(58)')
if RANGE:
 p1+=fctl('ScreenBound','1','value=0\nmovecamera=0,0');p2+=fctl('ScreenBound','1','value=0\nmovecamera=0,0')
for i,case in enumerate(cases):
 base=i*TICKS;kind=case['kind'];face=case['face'];dist=case['distance'];at=lambda t:f'Var(58)={base+t}';window=lambda a,b:f'Var(58)>={base+a} && Var(58)<={base+b}'
 for side in [1,2]:
  block=fctl('PosSet',at(1),f'x={(-1 if side==1 else 1)*face*dist/2}\ny=0')+fctl('VelSet',at(1),'x=0\ny=0')+fctl('Turn',at(1)+f' && Facing!={face if side==1 else -face}','')
  block+=fctl('LifeSet',at(1),f'value={1250 if side==1 else DUMMYLIFE}')+fctl('PowerSet',at(1),f'value={0 if kind in ["charge","chargehit","empty","no_awake"] else 3000}')
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
  if case['state']%10000==1210:p1+=press(100,'z')
  if kind=='ray' and case['outcome']=='guard':
   p2+=fctl('PosSet',window(18,260),f'x={face*dist/2}\ny=0')+fctl('AssertInput',window(18,260),'flag='+('R' if face==1 else 'L'))
  if kind=='ray' and case['outcome']=='interrupt':p2+=fctl('PosSet',at(33),f'x={-face*dist/2+face*20}\ny=0')+fctl('ChangeState',at(34),'value=9700\nctrl=0')
  if kind=='ray' and case['outcome'] in ['jump','airhit']:p2+=fctl('PosSet',at(20),'y=-170')+fctl('ChangeState',at(20),'value=9702\nctrl=0')
 elif kind in ['combo','air']:
  if kind=='air':p1+=press(18,'U');p2+=fctl('PosSet',at(20),'y=-95')+fctl('ChangeState',at(20),'value=9702\nctrl=0')
  p1+=press(36 if kind=='air' else 26,case['b'])
  rng='StateNo%10000>=600 && StateNo%10000<=621' if kind=='air' else '(StateNo%10000=200 || StateNo%10000=201 || StateNo%10000=210 || StateNo%10000=211 || StateNo%10000=220 || StateNo%10000=221)'
  p1+=fctl('AssertInput',f'{window(30,150)} && ({rng}) && Time>=6 && MoveHit && Var(58)%3=0','flag='+case['b'])
 elif kind=='dash':p1+=press(20,case['b'])+press(27,case['b'])
 elif kind in ['charge','chargehit']:
  p1+=fctl('AssertInput',window(20,80),'flag=s')
  if kind=='chargehit':p2+=fctl('ChangeState',at(43),'value=9700\nctrl=0')
 elif kind in ['awakening','no_awake','cancel_awake']:
  p1+=motion('s','D')
  if kind!='cancel_awake':p1+=fctl('AssertInput',window(28,140),'flag=s')
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
for path,fixture in [(char/'HidariShinju.cns',p1),(dummy/'kfm.cns',p2)]:
 s=path.read_text(encoding='latin1');s=s.replace('[Statedef -2]','[Statedef -2]\n'+fixture,1) if '[Statedef -2]' in s else s+'\n[Statedef -2]\n'+fixture
 if path==dummy/'kfm.cns':
  s=re.sub(r'(?im)^life\s*=.*$',f'life={DUMMYLIFE}',s,count=1)
  for dim in ['xscale','yscale']:s=re.sub(rf'(?im)^{dim}\s*=.*$',f'{dim}={SCALE}',s,count=1)
 path.write_text(s,encoding='latin1')
with (dummy/'kfm.cns').open('a') as f:
 for n,fall in [(9700,0),(9701,1)]:f.write(f'\n[Statedef {n}]\ntype=S\nmovetype=A\nphysics=S\nanim=400\nctrl=0\nvelset=0,0\n[State {n}, Actual opponent strike]\ntype=HitDef\ntrigger1=Time=0\nattr=S,NA\ndamage=60,0\nhitflag=MAF\nguardflag=MA\npausetime=5,8\nground.hittime=20\nground.velocity=-2,{-6 if fall else 0}\nair.velocity=-2,-4\nfall={fall}\nfall.recover=0\nsparkno=-1\n[State {n}, End]\ntype=ChangeState\ntrigger1=Time>=24\nvalue=0\nctrl=1\n')
 f.write('\n[Statedef 9702]\ntype=A\nmovetype=I\nphysics=N\nanim=41\nvelset=0,0\nctrl=0\n[State 9702, Air target]\ntype=Null\ntrigger1=1\n')
trace=ENGINE/'hidari_trace.tsv';trace.write_text('');module=ENGINE/'external/mods/hidari_checks.lua'
lua="""modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('hidari_trace.tsv','w'));local last=-1;local rows={};local frames=0
CAPSETUP
hook.add('loop','hidari_checks',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end
 last=clock;frames=frames+1
 local case=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 if case>=CASECOUNT then player(2);setLife(1);player(1);setTime(0);return end
 if rows[case]==nil then rows[case]={states={},damage=0,received=0,apex=0,minPower=3000,maxPower=0,sage=0,aura=0,dash=0,wrong=0,distance=0,guard=0,beamHurt=0,marks=0,wings=0,guardianWrong=0,guardianFrames=0,hiddenForm=0,visibleBase=0,visibilityErrors=0,hiddenGuardian=0} end
 local r=rows[case];local st=stateNo()
 if tick==8 then r.startDist=p2DistX();r.distance=p2DistX() end
 if tick>4 then
  r.states[st]=true;r.received=math.max(r.received,1250-life());r.minPower=math.min(r.minPower,power());r.maxPower=math.max(r.maxPower,power());r.apex=math.min(r.apex,posY());r.sage=math.max(r.sage,var(40));r.aura=math.max(r.aura,numHelper(9550))
  if st==100 or st==105 then r.dash=(r.startDist-p2DistX())*FACES[case+1] end
  if var(42)==1 and spriteVar('group')~=0 and st~=520 then r.wrong=r.wrong+1 end
  if moveType()=='H' and numHelper(9430)+numHelper(9431)>0 then r.beamHurt=r.beamHurt+1 end
  if var(42)==1 and numHelper(9500)>0 then r.hiddenForm=r.hiddenForm+1;if not isAsserted('invisible') then r.visibilityErrors=r.visibilityErrors+1 end elseif var(42)==0 then r.visibleBase=r.visibleBase+1;if isAsserted('invisible') then r.visibilityErrors=r.visibilityErrors+1 end end
  r.marks=math.max(r.marks,numHelper(9600));r.wings=math.max(r.wings,numHelper(9500))
  if numHelper(9500)>0 then
   local dy=(st==14600 and 12 or ((st==14500 or st==14200 or st==14300) and 9 or (st==14400 and time()>=10 and 12 or 0)));local rx,ry,rf=posX(),posY()+dy,facing()
   if helper(9500) then
    if isAsserted('invisible') then r.hiddenGuardian=r.hiddenGuardian+1 end
    if time()>1 then r.guardianFrames=r.guardianFrames+1;if spriteVar('group')~=14090 and spriteVar('group')~=14091 or math.abs(posX()-rx)>1 or math.abs(posY()-ry)>1 or facing()~=rf then r.guardianWrong=r.guardianWrong+1 end end
    player(1)
   end
  end
  player(2);r.damage=math.max(r.damage,DUMMYLIFE-life());r.victim=stateNo();if stateNo()>=150 and stateNo()<=155 then r.guard=1 end;player(1)
 end
 if tick==TICKS-1 then
  local hh={};for _,id in ipairs({9500,9510,9550,9560,9570,9571,9575,9578,9580,9595,9596,9600}) do if numHelper(id)>0 and helper(id) then table.insert(hh,id..':'..stateNo()..':'..time());player(1) end end
  local ss={};for n,_ in pairs(r.states) do table.insert(ss,n) end;table.sort(ss);for i,v in ipairs(ss) do ss[i]=tostring(v) end
  f:write(case..'\\t'..table.concat(ss,',')..'\\t'..r.damage..'\\t'..r.received..'\\t'..r.minPower..'\\t'..r.maxPower..'\\t'..r.sage..'\\t'..var(40)..'\\t'..var(42)..'\\t'..stateNo()..'\\t'..r.victim..'\\t'..r.dash..'\\t'..r.aura..'\\t'..numHelper()..'\\t'..(numHelper(9550)+numHelper(9500))..'\\t'..r.wrong..'\\t'..tostring(ctrl())..'\\t'..r.distance..'\\t'..r.guard..'\\t'..r.apex..'\\t'..r.beamHurt..'\\t'..r.marks..'\\t'..r.wings..'\\t'..r.guardianWrong..'\\t'..r.guardianFrames..'\\t'..table.concat(hh,';')..'\\t'..r.hiddenForm..'\\t'..r.visibleBase..'\\t'..r.visibilityErrors..'\\t'..r.hiddenGuardian..'\\n');f:flush()
 end
 CAPTURE
end)
""".replace('TICKS',str(TICKS)).replace('CASECOUNT',str(len(cases))).replace('DUMMYLIFE',str(DUMMYLIFE)).replace('FACES','({'+','.join(str(c['face']) for c in cases)+'})')
if CAP:
 lua=lua.replace('local clock=var(58);','frames=frames+1;local clock=var(58);').replace('last=clock;frames=frames+1','last=clock')
 folder=Path(CAP).resolve();folder.mkdir(parents=True,exist_ok=True)
 lua=lua.replace('CAPSETUP',"modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(folder)+'/')+")\nlocal images=assert(io.open("+json.dumps(str(folder/'frames.tsv'))+",'w'));local cues=assert(io.open("+json.dumps(str(folder/'cues.tsv'))+",'w'));local cap={index=0,pending=nil,last=-1000}")
 lua=lua.replace('CAPTURE',"""
 if cap.prev~=st and (st>=14200 and st<=14900 or st==520) then cues:write(frames..'\\t'..st..'\\n');cues:flush() end;cap.prev=st
 if cap.pending~=nil then local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb');if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\t'..case..'\\t'..tick..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end end
 if frames-cap.last>=CAPSTEP and cap.pending==nil and tick>=12 and tick<=CAPEND then screenshot();cap.pending=frames;cap.last=frames end
 """.replace('FOLDER',json.dumps(str(folder)+'/')).replace('CAPEND','({'+','.join('302' if c['kind']=='ultimate' or c.get('state')==14900 else '260' for c in cases)+'})[case+1]' if os.environ.get('HIDARI_ALL_SPECIALS') else str(TICKS-12)).replace('CAPSTEP','4' if os.environ.get('HIDARI_ALL_SPECIALS') else '4'))
else:lua=lua.replace('CAPSETUP','').replace('CAPTURE','')
module.write_text(lua);debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/hidari_checks.lua')\n")
env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
if AUDIO:env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=AUDIO,SDL_DISKAUDIODELAY='46')
try:
 run=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','HidariCheck','-p1.ai','0','-p2','HidariDummy','-p2.ai','0','-rounds','1','-time','9999']+(['-speed','0'] if CAP else ['-speedtest'])+([] if AUDIO else ['-nosound']),cwd=ENGINE,env=env,capture_output=True,text=True,timeout=600 if CAP else 120)
 print(run.stdout);print(run.stderr);assert run.returncode==0,'Engine failure'
 assert not re.search(r"WARNING: Hidari Shinju's[^\n]*Unknown state controller parameter",run.stdout+run.stderr)
finally:
 debug.write_text(saved)
 if module.exists():module.rename(module.with_name('-hidari_checks.lua'))
rows={int(l.split('\t')[0]):l.split('\t') for l in trace.read_text().splitlines()};assert sorted(rows)==list(range(len(cases))),('Missing traces',sorted(rows))
report=[]
for i,case in enumerate(cases):
 row=rows[i];ss=set(map(int,row[1].split(',')));damage=int(row[2]);received=int(row[3]);power=int(row[4]);endstate=int(row[9]);form=case['form'];kind=case['kind'];bad=[]
 if kind in ['move','ray']:
  if case['state'] not in ss:bad.append('raw motion did not enter requested special')
  if (kind=='move' or case['outcome'] in ['hit','airhit']) and damage<=0:bad.append('no real collision damage')
  if kind=='ray' and case['outcome'] in ['guard','jump','miss'] and damage:bad.append('ray hit through guard, high jump or outside beam range')
  if kind=='ray' and case['outcome']=='interrupt' and received<=0:bad.append('real incoming strike did not interrupt the cast')
  if kind=='ray' and case['outcome']=='guard' and int(row[18])!=1:bad.append('ray never contacted actual guard')
  if kind=='ray' and abs(float(row[17])-case['distance'])>10:bad.append('fixture did not establish the stated real distance')
  if power>3000-case['cost']:bad.append('cost not spent')
 if kind in ['combo','air'] and (case['state'] not in ss or not 140<=damage<=310):bad.append('three-hit chain failed')
 if kind=='ultimate' or kind=='move' and case.get('state')==14900:
  budget=min(450,int(DUMMYLIFE*.45))
  if 14900 not in ss or damage!=budget:bad.append('original Indra arrow damage or real contact failed')
 if kind in ['ultiblock','ultijump','empty'] and damage:bad.append('Indra connected through guard, high jump or no energy')
 if kind=='empty' and 14900 in ss:bad.append('Indra used without energy')
 if kind=='dash' and (case['state'] not in ss or abs(float(row[11]))<50 or (float(row[11])>0)!=(case['b']=='R') or power<3000):bad.append('free double-tap dash direction or travel failed')
 if kind=='charge' and (500 not in ss or int(row[5])<900 or int(row[12])!=1):bad.append('charge/aura failed')
 if kind=='chargehit' and (not received or 500 not in ss):bad.append('charge cannot be interrupted')
 if kind in ['guard','crouchguard'] and (received or (150 if kind=='guard' else 152) not in ss):bad.append('manual guard failed')
 if kind=='recovery' and (5120 not in ss or endstate!=0):bad.append('knockdown recovery failed')
 if kind=='awakening' and (520 not in ss or int(row[6])<1190 or (TICKS>=1250 and int(row[8])!=0)):bad.append('awakening activation or expiry failed')
 if kind.startswith('expire') and (int(row[8]) or endstate!=0):bad.append('form expiry left sprite, attack or recoil stuck')
 if kind=='cancel_awake' and (int(row[8]) or power<3000):bad.append('early-release activation consumed power or manifested')
 if kind=='no_awake' and (520 in ss or int(row[8])):bad.append('awakening allowed without energy')
 # A source pose offset resets one frame after a real interruption.
 if int(row[23])>(1 if kind=='ray' and case.get('outcome')=='interrupt' else 0):bad.append('Susanoo body, attachment or facing drifted')
 if form==1 and int(row[24])<=0:bad.append('Susanoo was never drawn in awakening')
 if int(row[15])>1:bad.append('A body from outside the original Hidari bank was shown')
 if int(row[13])!=int(row[14]):bad.append('combat helper remained after recovery')
 if int(row[28]) or int(row[29]):bad.append('awakening body visibility or guardian visibility failed')
 if form==1 and int(row[26])<=0:bad.append('hidden body was never observed during awakening')
 if kind in ['awakening','cancel_awake','no_awake'] and int(row[27])<=0:bad.append('base body was never observed outside awakening')
 result=dict(hidden_awakened_body_frames=int(row[26]),visible_base_body_frames=int(row[27]),visibility_error_frames=int(row[28]),hidden_guardian_frames=int(row[29]),case=case,states=sorted(ss),damage=damage,received=received,min_power=power,max_power=int(row[5]),max_sage_timer=int(row[6]),end_timer=int(row[7]),end_form=int(row[8]),end_state=endstate,victim_end=int(row[10]),dash_distance=float(row[11]),aura=int(row[12]),end_helpers=int(row[13]),wrong_sage_body_frames=int(row[15]),actual_start_distance=float(row[17]),actual_guard=int(row[18]),jump_apex=float(row[19]),beam_during_hurt=int(row[20]),visible_claw_marks=int(row[21]),visible_susanoo=int(row[22]),guardian_bad_frames=int(row[23]),guardian_observed_frames=int(row[24]),helper_details=row[25].strip(),target_scale=SCALE,target_crouching=CROUCH,failures=bad);report.append(result);print('FAIL' if bad else 'PASS',case['name'],form,case['face'],damage,bad)
files=[f'HidariShinju.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['HidariShinju_common.cns'];runtime=hashlib.sha256(b''.join((ROOT/'HidariShinju'/n).read_bytes() for n in files)).hexdigest()
out=ROOT/'previews'/os.environ.get('HIDARI_REPORT',('HidariShinju_sasuke_capture_checks.json' if CAP else f'HidariShinju_rays_{SCALE}_{int(CROUCH)}_checks.json' if RANGE else 'HidariShinju_sasuke_low_life_checks.json' if LOW else 'HidariShinju_sasuke_engine_checks.json'));out.write_text(json.dumps(dict(runtime_sha256=runtime,cases=report),indent=2)+'\n');assert not any(r['failures'] for r in report),str(out);print('PASS',len(report),'Hidari actual-input engine cases')
