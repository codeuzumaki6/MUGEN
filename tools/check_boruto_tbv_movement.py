#!/usr/bin/env python3
"""Actual jump, crouch and landing inputs, in both directions and forms."""
import json,os,subprocess,sys,tempfile
from pathlib import Path
from boruto_source import ROOT

def main():
    tmp=Path(tempfile.mkdtemp(prefix='tbv-movement-',dir='/tmp'));trace=tmp/'positions.tsv'
    source=(ROOT/'tools/check_boruto_in_engine.py').read_text().replace('from build_boruto_runtime import MOVES','from build_boruto_tbv_runtime import MOVES').replace('BorutoKarmaJogan','BorutoTBVBase').replace('BorutoCheck','BorutoTBVCheck').replace('BorutoDummy','BorutoTBVDummy').replace('BORUTO_','BORUTOTBV_').replace('boruto_trace','boruto_tbv_trace').replace('boruto_checks','boruto_tbv_checks')
    source=source.replace("if os.environ.get('BORUTOTBV_DEMO')=='showcase':", "cases=[dict(name='movement',kind='movement',form=form,face=face,distance=180) for form in [0,1] for face in [1,-1]]\nif os.environ.get('BORUTOTBV_DEMO')=='showcase':")
    needle=" if kind=='move':p1+=motion(case['b'],case['d'])"
    assert needle in source
    source=source.replace(needle," if kind=='movement':p1+=press(18,'U')+ctl('AssertInput',win(85,105),'flag=D')\n"+needle)
    source=source.replace('ROOT=Path(__file__).resolve().parents[1]', 'ROOT=Path('+repr(str(ROOT))+')')
    fixture=tmp/'fixture.py';fixture.write_text(source)
    env={k:v for k,v in os.environ.items() if not k.startswith('BORUTOTBV_')};env.update(PYTHONPATH=str(ROOT/'tools'),BORUTOTBV_TICKS='200',BORUTOTBV_CONTACT_TRACE=str(trace),BORUTOTBV_REPORT='BorutoTBVBase_movement_native_checks.json')
    with (tmp/'engine.log').open('w') as out:r=subprocess.run([sys.executable,str(fixture)],cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT)
    assert r.returncode==0,(tmp/'engine.log').read_text()[-3000:]
    report=json.loads((ROOT/'previews/BorutoTBVBase_movement_native_checks.json').read_text());rows=[r.split() for r in trace.read_text().splitlines()];manifest=json.loads((ROOT/'BorutoTBVBase/assets/sprites.json').read_text());keys={(r['group'],r['number']):r['key'] for r in manifest};checks=[]
    for i,c in enumerate(report['cases']):
        data=[r for r in rows if int(r[0])==i and int(r[1])>5];air=[r for r in data if int(r[2])%10000==50];crouch=[r for r in data if int(r[2])%10000==11];land=[r for r in data if int(r[2])%10000==52]
        assert air and crouch and land and min(float(r[7]) for r in air)<-30
        assert all(keys[int(r[4]),int(r[5])].startswith('Hiruzen_Fly_') for r in air)
        assert all(keys[int(r[4]),int(r[5])]=='Hiruzen_NAttack_006' for r in crouch)
        assert all('Wake' not in keys[int(r[4]),int(r[5])] and 'Hurt' not in keys[int(r[4]),int(r[5])] for r in land)
        assert data[-1][10]=='true' and abs(float(data[-1][7]))<.01
        checks.append(dict(form=c['case']['form'],face=c['case']['face'],actual_jump=True,correct_air_sprites=True,correct_crouch=True,correct_landing=True,control_returned=True))
    (ROOT/'previews/BorutoTBVBase_movement_checks.json').write_text(json.dumps(dict(runtime_sha256=report['runtime_sha256'],cases=checks),indent=2)+'\n');print('PASS: four real jump/crouch/landing cases, both facings and forms')

if __name__=='__main__':main()
