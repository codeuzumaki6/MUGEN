#!/usr/bin/env python3
"""Measure source soles against the stage during real charge/attack inputs."""
import json,os,subprocess,sys,tempfile
from pathlib import Path
from PIL import Image
from boruto_source import ROOT
from boruto_tbv_sff import read_sff

NAME='BorutoTBVBase';CHAR=ROOT/NAME

def main():
    landmarks=json.loads((ROOT/'design/boruto_tbv_base/sole_landmarks.json').read_text())['frames']
    manifest=json.loads((CHAR/'assets/sprites.json').read_text());bykey={r['key']:r for r in manifest};sprites=read_sff(CHAR/(NAME+'.sff'))
    for key,(x,y) in landmarks.items():
        r=bykey[key];assert Image.open(CHAR/r['file']).convert('RGBA').getpixel((x,y))[3]>=250,key
        entry=sprites[r['group'],r['number']];assert entry[4][y*entry[0]+x]>0,(key,'Invisible sole')
        light=bykey.get(key+'_Light')
        if light:assert light['axis']==r['axis'],(key,'Light no longer follows body axis')
    tmp=Path(tempfile.mkdtemp(prefix='tbv-grounding-',dir='/tmp'));trace=tmp/'positions.tsv'
    env={k:v for k,v in os.environ.items() if not k.startswith('BORUTOTBV_')}
    env.update(BORUTOTBV_CASES=json.dumps(['charge','Shiden','Combo','Rasengan','Kenjutsu','Espiral','awakening']),BORUTOTBV_CONTACT_TRACE=str(trace),BORUTOTBV_REPORT=NAME+'_grounding_native_checks.json')
    with (tmp/'engine.log').open('w') as out:
        run=subprocess.run([sys.executable,str(ROOT/'tools/check_boruto_tbv_in_engine.py')],cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT)
    assert run.returncode==0,(tmp/'engine.log').read_text()[-3500:]
    native=json.loads((ROOT/'previews'/(NAME+'_grounding_native_checks.json')).read_text());keys={(r['group'],r['number']):r for r in manifest};cases=[];seen=set()
    for ci,case in enumerate(native['cases']):
        samples=[];frames=set()
        for line in trace.read_text().splitlines():
            row=line.split();key=keys[int(row[4]),int(row[5])]['key']
            if int(row[0])!=ci or int(row[1])<=5 or key not in landmarks:continue
            r=bykey[key];height=float(row[7])+landmarks[key][1]-r['axis'][1]
            assert abs(float(row[7]))<.01,(key,'Grounded action moved actor vertically')
            assert -2<=height<=0,(key,case['case'],'Soles above or below stage',height)
            samples.append(height);frames.add(key);seen.add(key)
        assert samples,case['case']
        cases.append(dict(case=case['case'],samples=len(samples),frames=sorted(frames),minimum_sole_y=min(samples),maximum_sole_y=max(samples)))
    assert len(cases)==26 and seen==set(landmarks),(len(cases),set(landmarks)-seen)
    result=dict(runtime_sha256=native['runtime_sha256'],source_sole_landmarks=len(landmarks),cases=cases,grounded_charge=True,matching_body_and_light_axes=True)
    (ROOT/'previews'/(NAME+'_grounding_checks.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 26 actual charge/attack cases; all source soles within two pixels of the stage')

if __name__=='__main__':main()
