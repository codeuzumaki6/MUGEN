#!/usr/bin/env python3
"""Probe the released characters as P2, using real low, mid and projectile hits.

All fixture controllers live in disposable engine copies. No debug controller
is installed in the delivered characters. Run one native engine at a time.
"""
from pathlib import Path
import argparse,fcntl,json,os,re,shutil,subprocess

ROOT=Path(__file__).resolve().parents[1]
ENGINE=Path('/workspace/.eida-tools/ikemen-nightly')
CHARS=['Eida','PochitaTrueForm','Mamushi','Shibai','JuraShinju','MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju']
TICKS=190

def controller(kind,when,params):
    return f'\n[State -2, Disposable receiving probe]\ntype={kind}\ntriggerall=!IsHelper\ntriggerall=RoundState=2\ntrigger1={when}\nignorehitpause=1\n{params}\n'

def inject(path,fixture):
    s=path.read_text(encoding='latin1')
    if re.search(r'(?im)^\[Statedef -2\]',s):
        s=re.sub(r'(?im)^\[Statedef -2\]',lambda m:m[0]+'\n'+fixture,s,count=1)
    else:s+='\n[Statedef -2]\n'+fixture
    path.write_text(s,encoding='latin1')

def run(name,out,capture=None):
    target=ENGINE/'chars/RosterReceiver';attacker=ENGINE/'chars/RosterProbe'
    shutil.copytree(ROOT/name,target,dirs_exist_ok=True)
    shutil.copytree(ENGINE/'chars/kfm',attacker,dirs_exist_ok=True)
    shutil.copyfile(target/(name+'.def'),target/'RosterReceiver.def')
    shutil.copyfile(attacker/'kfm.def',attacker/'RosterProbe.def')
    deftext=(target/'RosterReceiver.def').read_text(encoding='latin1')
    main=re.search(r'(?im)^cns\s*=\s*([^;\r\n]+)',deftext)[1].strip()
    forms=[0,1] if name not in ['Mamushi'] else [0]
    cases=[dict(form=form,face=face,pose=pose,attack=attack)
           for form in forms for face in [1,-1]
           for pose in ['idle','walk','dash','backdash','charge','normal','special']
           for attack in ['low','mid','projectile','combo']]
    if name=='HidariShinju':
        cases += [dict(form=1,face=face,pose='idle',attack='high_projectile') for face in [1,-1]]
    if capture:
        cases=[c for c in cases if c['face']==1 and c['pose']=='idle' and c['attack']=='combo' and (c['form']==0 or name=='HidariShinju')]
        capture.mkdir(parents=True,exist_ok=True)
    p1=controller('VarAdd','1','v=58\nvalue=1')
    p1+=controller('NotHitBy','1','value=SCA\ntime=1')
    p1+=controller('PlayerPush','1','value=0')
    p2=controller('VarSet','1','v=58\nvalue=EnemyNear,Var(58)')
    p2+=controller('PlayerPush','1','value=0')
    for i,c in enumerate(cases):
        at=lambda t:f'Var(58)={i*TICKS+t}'
        window=lambda a,b:f'Var(58)>={i*TICKS+a} && Var(58)<={i*TICKS+b}'
        for side in [1,2]:
            fix=controller('PosSet',at(1),f'x={(-1 if side==1 else 1)*c["face"]*30}\ny=0')
            fix+=controller('VelSet',at(1),'x=0\ny=0')
            fix+=controller('Turn',at(1)+f' && Facing!={c["face"]*(1 if side==1 else -1)}','')
            fix+=controller('LifeSet',at(1),'value=Const(data.life)')
            fix+=controller('PowerSet',at(1),'value=3000')
            fix+=controller('ChangeState',at(1),'value=0\nctrl=1')
            if side==1:p1+=fix
            else:p2+=fix
        for v in [40,41,42,43]:
            value=(1 if v==42 else 800 if v==40 else 0) if c['form'] else 0
            if name=='Eida':value=(1 if v==40 else 800 if v==41 else 0) if c['form'] else 0
            p2+=controller('VarSet',at(2),f'v={v}\nvalue={value}')
        if name=='PochitaTrueForm':
            p2+=controller('VarSet',at(2),f'v=36\nvalue={800 if c["form"] else 0}')
            p2+=controller('VarSet',at(2),'v=33\nvalue=0')
        # Keep the probe aligned to the defender during movement, but do not
        # force its state or velocity while it receives and recovers from a hit.
        p1+=controller('PosSet',window(10,55),f'x=EnemyNear,Pos X-{c["face"]*60}\ny=0')
        pose=c['pose'];state={'idle':0,'walk':20,'dash':100,'backdash':105,'charge':500,'normal':200,'special':1000}[pose]
        if name=='Eida' and c['form'] and pose=='idle':state=4001
        if c['form'] and name in ['MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju','DeepaKara','OugaYatsume','JigenKara'] and pose in ['normal','special']:state+=10000
        p2+=controller('ChangeState',at(18),f'value={state}\nctrl={1 if pose in ["idle","walk"] else 0}')
        if pose=='charge':p2+=controller('AssertInput',window(18,75),'flag=s')
        if pose=='walk':p2+=controller('AssertInput',window(18,35),'flag='+('L' if c['face']==1 else 'R'))
        # Dash invulnerability is sampled inside the dash, not after recovery.
        strike=23 if pose in ['dash','backdash'] else 38
        p1+=controller('ChangeState',at(strike),'value='+str({'low':9700,'mid':9701,'projectile':9702,'combo':9703,'high_projectile':9704}[c['attack']])+'\nctrl=0')
    inject(attacker/'kfm.cns',p1);inject(target/main,p2)
    air='\n'
    with (attacker/'kfm.cns').open('a') as f:
        for i,(lo,hi) in enumerate([(-16,-2),(-52,-28),(-52,-28),(-52,-28),(-130,-110)]):
            n=9700+i
            air+=f'\n[Begin Action {n}]\nClsn1Default: 1\n Clsn1[0]=40,{lo},100,{hi}\nLoopstart\n400,0,0,0,5\n'
            projectile=i in [2,4];attack='Projectile' if projectile else 'HitDef'
            when='Time=0 || Time=8 || Time=16' if i==3 else 'Time=0'
            f.write(f'\n[Statedef {n}]\ntype=S\nmovetype=A\nphysics=N\nanim={n}\nctrl=0\nvelset=0,0\n[State {n}, Probe]\ntype={attack}\ntrigger1={when}\nattr=S,{"NP" if projectile else "NA"}\ndamage=60,0\nhitflag=MAF\nguardflag=MA\npausetime=3,5\nground.hittime=15\nground.velocity=-1,0\nair.velocity=-1,-2\nfall=0\nsparkno=-1\n')
            if projectile:f.write(f'projID={n}\nprojanim={n}\nprojhitanim=-1\nprojremanim=-1\nprojremovetime=12\nprojhits=1\nvelocity=1,0\n')
            f.write(f'\n[State {n}, End]\ntype=ChangeState\ntrigger1=Time>=24\nvalue=0\nctrl=1\n')
    with (attacker/'kfm.air').open('a') as f:f.write(air)
    trace=ENGINE/'roster_receiving.tsv';trace.write_text('');module=ENGINE/'external/mods/roster_receiving.lua'
    lua='''modifyGameOption('Debug.RetryLoadOnError',false)
CAPSETUP
local f=assert(io.open('roster_receiving.tsv','w'));local last=-1;local row=nil
hook.add('loop','roster_receiving',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end;last=clock
 local case=math.floor((clock-1)/TICKS);local tick=(clock-1)%TICKS+1
 if case>=COUNT then player(2);setLife(1);player(1);setTime(0);return end
 player(2)
 if tick==1 then row={damage=0,hurt=false,recovered=false,states={},hits=0,previous=life()} end
 if tick>5 then
  row.damage=math.max(row.damage,const('data.life')-life())
  row.hurt=row.hurt or moveType()=='H'
  if life()<row.previous then row.hits=row.hits+1 end;row.previous=life()
  row.states[stateNo()]=true
  if row.damage>0 and tick>80 and ctrl() then row.recovered=true end
 end
 if tick==TICKS-1 then
  local ss={};for n,_ in pairs(row.states) do ss[#ss+1]=tostring(n) end;table.sort(ss)
  f:write(case..'\\t'..row.damage..'\\t'..tostring(row.hurt)..'\\t'..tostring(row.recovered)..'\\t'..table.concat(ss,',')..'\\t'..row.hits..'\\n');f:flush()
 end
 CAPTURE
end)
'''.replace('TICKS',str(TICKS)).replace('COUNT',str(len(cases)))
    if capture:
        lua=lua.replace('CAPSETUP',"modifyGameOption('Config.ScreenshotFolder',"+json.dumps(str(capture)+'/')+")\nlocal images=assert(io.open("+json.dumps(str(capture/'frames.tsv'))+",'w'));local cap={index=0,last=-1000,pending=nil}")
        lua=lua.replace('CAPTURE','''
 if cap.pending~=nil then local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb');if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\t'..case..'\\t'..tick..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end end
 if clock-cap.last>=3 and cap.pending==nil and tick>=12 and tick<=135 then screenshot();cap.pending=clock;cap.last=clock end
'''.replace('FOLDER',json.dumps(str(capture)+'/')))
    else:lua=lua.replace('CAPSETUP','').replace('CAPTURE','')
    module.write_text(lua)
    debug=ENGINE/'external/script/debug.lua';saved=debug.read_text()
    debug.write_text(saved+"\ndofile('external/mods/roster_receiving.lua')\n")
    env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
    try:
        result=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','RosterProbe','-p1.ai','0','-p2','RosterReceiver','-p2.ai','0','-rounds','1','-time','9999']+(['-speed','0'] if capture else ['-speedtest'])+['-nosound','-log','roster_receiving.log'],cwd=ENGINE,env=env,capture_output=True,text=True,timeout=150)
        assert result.returncode==0,result.stdout+result.stderr
        warnings=[s for s in (result.stdout+result.stderr).splitlines() if 'Unknown state controller parameter' in s and "Kung Fu Man's state 1027" not in s]
        assert not warnings,warnings
    finally:
        debug.write_text(saved);module.rename(module.with_name('-roster_receiving.lua'))
    rows=[line.split('\t') for line in trace.read_text().splitlines()]
    assert len(rows)==len(cases),(name,len(rows),len(cases),result.stdout,result.stderr)
    report=[]
    for c,r in zip(cases,rows):
        report.append(dict(**c,damage=int(r[1]),hurt=r[2]=='true',recovered=r[3]=='true',states=list(map(int,r[4].split(','))),hits_received=int(r[5])))
    path=out/(name+'.json');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(report,indent=2)+'\n')
    failures=[c for c in report if not c['damage'] or not c['hurt'] or not c['recovered'] or (c['attack']=='combo' and c['hits_received']!=3)]
    print(name,len(report),'probes;',len(failures),'failures',flush=True)
    for c in failures:print(' ',c,flush=True)
    return failures

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--characters',nargs='+',default=CHARS);ap.add_argument('--out',type=Path,default=ROOT/'previews/roster_receiving');ap.add_argument('--capture-root',type=Path);args=ap.parse_args()
    lock=open(ENGINE/'.native-character-check.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
    failures=[]
    for name in args.characters:failures+=run(name,args.out,args.capture_root/name if args.capture_root else None)
    print('Total failing receiving cases:',len(failures))
    raise SystemExit(bool(failures))
