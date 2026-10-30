#!/usr/bin/env python3
"""Actual palm contact and the persistent source wind dome, in both forms."""
import json,os,subprocess,sys,tempfile
from pathlib import Path
from boruto_source import ROOT

def main():
    tmp=Path(tempfile.mkdtemp(prefix='tbv-palm-aura-',dir='/tmp'));trace=tmp/'positions.tsv'
    source=(ROOT/'tools/check_boruto_in_engine.py').read_text().replace('from build_boruto_runtime import MOVES','from build_boruto_tbv_runtime import MOVES').replace('BorutoKarmaJogan','BorutoTBVBase').replace('BorutoCheck','BorutoTBVCheck').replace('BorutoDummy','BorutoTBVDummy').replace('BORUTO_','BORUTOTBV_').replace('boruto_trace','boruto_tbv_trace').replace('boruto_checks','boruto_tbv_checks')
    source=source.replace("ROOT=Path(__file__).resolve().parents[1]",'ROOT=Path('+repr(str(ROOT))+')')
    source=source.replace('ipairs({9501,9505,9540})','ipairs({9501,9505,9540,9560})')
    source=source.replace(" vf:write(table.concat(values", " values[#values+1]=var(42);vf:write(table.concat(values")
    fixture=tmp/'fixture.py';fixture.write_text(source)
    env={k:v for k,v in os.environ.items() if not k.startswith('BORUTOTBV_')};env.update(PYTHONPATH=str(ROOT/'tools'),BORUTOTBV_CONTACT_TRACE=str(trace),BORUTOTBV_CASES=json.dumps(['Espiral','ultimate','awakening','expire_attack','expire_hurt']),BORUTOTBV_REPORT='BorutoTBVBase_palm_aura_native_checks.json')
    with (tmp/'engine.log').open('w') as out:run=subprocess.run([sys.executable,str(fixture)],cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT)
    assert run.returncode==0,(tmp/'engine.log').read_text()[-4000:]
    native=json.loads((ROOT/'previews/BorutoTBVBase_palm_aura_native_checks.json').read_text());rows=[r.split() for r in trace.read_text().splitlines()];contacts=[];aura=[];keys={(r['group'],r['number']):r['key'] for r in json.loads((ROOT/'BorutoTBVBase/assets/sprites.json').read_text())}
    for ci,c in enumerate(native['cases']):
        data=[r for r in rows if int(r[0])==ci and int(r[1])>5]
        if c['case']['name'] in ['Espiral','ultimate']:
            held=[r for r in data if int(r[14]) in [3010,3020]];assert held,c['case']
            first=held[0];assert int(first[4])==31020 and int(first[5])==0,(c['case'],'Contact without the extended palm',first)
            assert abs(float(first[11])-float(first[6]))<=80
            assert not any(keys[int(r[4]),int(r[5])]=='Hiruzen_Skill05_13' for r in held),'Running pose during bound damage'
            contacts.append(dict(case=c['case'],palm_visible_at_contact=True,contact_distance=abs(float(first[11])-float(first[6])),no_running_during_damage=True))
        active=[r for r in data if int(r[34])==1]
        # The activation state sets the mode after -2; its helper begins on
        # the next engine tick, then stays present even when the owner is hit.
        for r in active[1:]:assert int(r[30])==1 and int(r[32])==31100,(c['case'],'Missing wind dome',r)
        if active:aura.append(dict(case=c['case'],active_samples=len(active),persistent_source_dome=True))
    assert len(native['cases'])==14 and len(contacts)==8 and len(aura)==10,(len(native['cases']),len(contacts),len(aura))
    result=dict(runtime_sha256=native['runtime_sha256'],palm_contacts=contacts,wind_aura_cases=aura)
    (ROOT/'previews/BorutoTBVBase_palm_aura_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: eight visible palm contacts; persistent source wind dome in ten native cases')

if __name__=='__main__':main()
