#!/usr/bin/env python3
"""Reproduce the video's CPU jab loop, then try a real player counterattack."""
from pathlib import Path
import argparse,fcntl,json,os,re,shutil,subprocess
from check_roster_receiving import controller,inject,ENGINE,ROOT

def run(name,baseline=False):
    cpu=ENGINE/'chars/RosterCPU';victim=ENGINE/'chars/RosterPlayer'
    shutil.copytree(ROOT/name,cpu,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',victim,dirs_exist_ok=True)
    if baseline:
        from build_roster_revision import original
        for p in (ROOT/name).iterdir():
            if p.suffix in ['.def','.air','.cns','.cmd','.sff','.snd']:(cpu/p.name).write_bytes(original(p))
    shutil.copyfile(cpu/(name+'.def'),cpu/'RosterCPU.def');shutil.copyfile(victim/'kfm.def',victim/'RosterPlayer.def')
    main=re.search(r'(?im)^cns\s*=\s*([^;\r\n]+)',(cpu/'RosterCPU.def').read_text())[1].strip()
    p1=controller('VarAdd','1','v=58\nvalue=1')
    p1+=controller('PosSet','Var(58)=1','x=-25\ny=0')+controller('LifeSet','Var(58)=1','value=10000')
    # After the opening observation, the player repeatedly attempts a real
    # projectile whenever control returns. A stun lock prevents this input.
    p1+=controller('ChangeState','Var(58)>360 && Var(58)%24=0 && Ctrl','value=9700\nctrl=0')
    p2=controller('VarSet','1','v=58\nvalue=EnemyNear,Var(58)')
    p2+=controller('PosSet','Var(58)=1','x=25\ny=0')
    # Isolate the normal chain from energy-consuming techniques, for a
    # deterministic regression of the exact repeated-punch problem.
    p2+=controller('PowerSet','1','value=0')
    inject(victim/'kfm.cns',p1);inject(cpu/main,p2)
    p=victim/'kfm.cns';text=p.read_text(encoding='latin1');text=re.sub(r'(?im)^life\s*=.*$','life=10000',text,count=1);text=re.sub(r'(?im)^yscale\s*=.*$','yscale=.65',text,count=1);text=re.sub(r'(?im)^xscale\s*=.*$','xscale=.65',text,count=1)
    text+='''
[Statedef 9700]
type=S
movetype=A
physics=S
anim=200
ctrl=0
velset=0,0
[State 9700, Physical player projectile]
type=Projectile
trigger1=Time=2
projID=9700
projanim=9700
projhitanim=-1
projremanim=-1
projremovetime=60
velocity=10,0
offset=20,-25
attr=S,NP
damage=35,0
hitflag=MAF
guardflag=MA
pausetime=2,4
ground.hittime=16
ground.velocity=-2,0
air.velocity=-2,-2
sparkno=-1
[State 9700, Return]
type=ChangeState
trigger1=Time>=20
value=0
ctrl=1
''';p.write_text(text,encoding='latin1')
    with (victim/'kfm.air').open('a') as f:f.write('\n[Begin Action 9700]\nClsn1Default: 1\n Clsn1[0]=-8,-12,8,12\nLoopstart\n1000,0,0,0,3\n')
    trace=ENGINE/'roster_pressure.json';trace.write_text('');module=ENGINE/'external/mods/roster_pressure.lua'
    module.write_text('''modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('roster_pressure.json','w'));local last=-1;local run=0;local maxrun=0;local ctrlframes=0;local attempts=0;local states={};local damage=0
hook.add('loop','roster_pressure',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end;last=clock
 if moveType()=='H' then run=run+1 else run=0 end;maxrun=math.max(maxrun,run)
 if clock>100 and clock<360 and ctrl() then ctrlframes=ctrlframes+1 end
 if stateNo()==9700 and time()==1 then attempts=attempts+1 end
 player(2);states[stateNo()]=true;damage=math.max(damage,const('data.life')-life())
 if clock==1000 then
  local ss={};for n,_ in pairs(states) do ss[#ss+1]=tostring(n) end;table.sort(ss)
  f:write(string.format('{"max_continuous_hurt_ticks":%d,"player_control_ticks":%d,"player_counterattacks":%d,"cpu_damage_received":%d,"cpu_states":[%s]}',maxrun,ctrlframes,attempts,damage,table.concat(ss,',')));f:flush()
  player(2);setLife(1);player(1);setTime(0)
 end
end)
''')
    debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/roster_pressure.lua')\n")
    env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
    try:
        r=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','RosterPlayer','-p1.ai','0','-p2','RosterCPU','-p2.ai','8','-rounds','1','-time','9999','-speedtest','-nosound'],cwd=ENGINE,env=env,capture_output=True,text=True,timeout=90)
        assert r.returncode==0,r.stdout+r.stderr
    finally:debug.write_text(saved);module.rename(module.with_name('-roster_pressure.lua'))
    report=json.loads(trace.read_text());report.update(character=name,baseline=baseline)
    print(report,flush=True);return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',action='store_true');ap.add_argument('--characters',nargs='+',default=['JuraShinju','RyuShinju','MitsukiTBV','HidariShinju','MatsuriShinju','Shibai']);args=ap.parse_args()
    lock=open(ENGINE/'.native-character-check.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
    reports=[run(c,args.baseline) for c in args.characters]
    out=ROOT/'previews'/('roster_pressure_before.json' if args.baseline else 'roster_pressure_after.json');out.write_text(json.dumps(reports,indent=2)+'\n')
    if not args.baseline:
        assert all(r['player_control_ticks']>0 and r['max_continuous_hurt_ticks']<240 and r['cpu_damage_received']>0 for r in reports),reports
