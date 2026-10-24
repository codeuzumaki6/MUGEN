#!/usr/bin/env python3
"""Double taps in both world directions, both facings, plus single-tap checks."""
from pathlib import Path
import fcntl,json,os,re,shutil,subprocess
from check_roster_receiving import controller,inject,ENGINE,ROOT,CHARS

def run(name):
    char=ENGINE/'chars/RosterDash';dummy=ENGINE/'chars/RosterDashDummy'
    shutil.copytree(ROOT/name,char,dirs_exist_ok=True);shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
    shutil.copyfile(char/(name+'.def'),char/'RosterDash.def');shutil.copyfile(dummy/'kfm.def',dummy/'RosterDashDummy.def')
    main=re.search(r'(?im)^cns\s*=\s*([^;\r\n]+)',(char/'RosterDash.def').read_text())[1].strip()
    cases=[dict(face=face,direction=d,kind=kind) for face in [1,-1] for d in ['L','R'] for kind in ['double','single']]
    p1=controller('VarAdd','1','v=58\nvalue=1');p2=controller('VarSet','1','v=58\nvalue=EnemyNear,Var(58)')
    for i,c in enumerate(cases):
        at=lambda t:f'Var(58)={i*180+t}'
        for side in [1,2]:
            b=controller('PosSet',at(1),f'x={c["face"]*(-60 if side==1 else 160)}\ny=0')+controller('VelSet',at(1),'x=0\ny=0')
            b+=controller('Turn',at(1)+f' && Facing!={c["face"]*(1 if side==1 else -1)}','')
            b+=controller('PowerSet',at(1),'value=3000')+controller('ChangeState',at(1),'value=0\nctrl=1')
            if side==1:p1+=b
            else:p2+=b
        if c['kind']=='double':p1+=controller('AssertInput',at(20),'flag='+c['direction'])
        p1+=controller('AssertInput',at(27),'flag='+c['direction'])
    inject(char/main,p1);inject(dummy/'kfm.cns',p2)
    trace=ENGINE/'roster_dash.tsv';trace.write_text('');module=ENGINE/'external/mods/roster_dash.lua'
    module.write_text('''modifyGameOption('Debug.RetryLoadOnError',false)
local f=assert(io.open('roster_dash.tsv','w'));local last=-1;local r=nil
hook.add('loop','roster_dash',function()
 if not player(1) or roundState()~=2 then return end
 local clock=var(58);if clock<1 or clock==last then return end;last=clock
 local case=math.floor((clock-1)/180);local tick=(clock-1)%180+1
 if case>=8 then player(2);setLife(1);player(1);setTime(0);return end
 if tick==5 then r={dist=p2DistX(),y=0,power=3000,states={}} end
 if tick>5 then r.states[stateNo()]=true;r.y=math.max(r.y,math.abs(posY()));r.power=math.min(r.power,power()) end
 if tick==170 then
  local ss={};for n,_ in pairs(r.states) do ss[#ss+1]=tostring(n) end;table.sort(ss)
  f:write(case..'\\t'..((r.dist-p2DistX())*facing())..'\\t'..r.y..'\\t'..r.power..'\\t'..tostring(ctrl())..'\\t'..table.concat(ss,',')..'\\n');f:flush()
 end
end)
''')
    debug=ENGINE/'external/script/debug.lua';saved=debug.read_text();debug.write_text(saved+"\ndofile('external/mods/roster_dash.lua')\n")
    env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy',MESA_SHADER_CACHE_DISABLE='true')
    try:
        r=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','RosterDash','-p1.ai','0','-p2','RosterDashDummy','-p2.ai','0','-rounds','1','-time','9999','-speedtest','-nosound'],cwd=ENGINE,env=env,capture_output=True,text=True,timeout=90)
        assert r.returncode==0,r.stdout+r.stderr
    finally:debug.write_text(saved);module.rename(module.with_name('-roster_dash.lua'))
    rows=[l.split('\t') for l in trace.read_text().splitlines()];assert len(rows)==len(cases)
    reports=[]
    for c,row in zip(cases,rows):
        dx=float(row[1]);states=list(map(int,row[5].split(',')));expected=100 if (c['direction']=='R')==(c['face']==1) else 105
        ok=(float(row[2])==0 and int(row[3])==3000 and row[4]=='true')
        if c['kind']=='double':ok=ok and expected in states and abs(dx)>30 and (dx>0)==(c['direction']=='R')
        else:ok=ok and not any(s in states for s in [100,105])
        reports.append(dict(**c,states=states,travel=dx,max_air_height=float(row[2]),minimum_power=int(row[3]),passed=ok))
    print(name,'PASS' if all(r['passed'] for r in reports) else reports,flush=True)
    return reports

if __name__=='__main__':
    lock=open(ENGINE/'.native-character-check.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
    reports={name:run(name) for name in CHARS}
    (ROOT/'previews/roster_dash_checks.json').write_text(json.dumps(reports,indent=2)+'\n')
    assert all(r['passed'] for rows in reports.values() for r in rows),reports
