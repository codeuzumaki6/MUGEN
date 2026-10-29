#!/usr/bin/env python3
"""Regression: packed PNG32 retains source alpha; movement never uses hurt poses."""
import json,re
import numpy as np
from PIL import Image
from boruto_source import ROOT,sha
from boruto_tbv_sff import read_sff
NAME='BorutoTBVBase';CHAR=ROOT/NAME
def main():
    sprites=read_sff(CHAR/(NAME+'.sff'));manifest=json.loads((CHAR/'assets/sprites.json').read_text());keys={(r['group'],r['number']):r['key'] for r in manifest};byname={r['key']:r for r in manifest};semi=0;count=0
    for r in manifest:
        w,h,x,y,pixels,palette=sprites[r['group'],r['number']]
        if r['group']==31000:
            im=Image.open(CHAR/r['file']).convert('RGBA');assert not palette and pixels==im.tobytes(),r['key'];alpha=np.frombuffer(pixels,dtype=np.uint8).reshape(h,w,4)[:,:,3];semi+=int(((alpha>0)&(alpha<255)).sum());count+=1
        if r.get('source_parent'):
            im=Image.open(CHAR/byname[r['source_parent']]['file']).convert('RGBA').crop(r['source_rect']);assert im.tobytes()==Image.open(CHAR/r['file']).convert('RGBA').tobytes()
    assert count==161 and semi>10000
    actions={};current=None
    for line in (CHAR/(NAME+'.air')).read_text().splitlines():
        m=re.match(r'\[Begin Action (\d+)\]',line)
        if m:current=int(m[1]);actions[current]=[]
        elif re.match(r'\s*\d+,\d+,',line):
            a=line.split(',');actions[current].append(keys[int(a[0]),int(a[1])])
    for form in [0,1]:
        for n in [40,41,44]:assert all(k.startswith('Hiruzen_Fly_') for k in actions[n+10000*form])
        for n in [6,10,11,52]:assert not any('Hurt' in k or 'Wake' in k or 'Dead' in k for k in actions[n+10000*form])
        assert not any(k.startswith('Hiruzen_Skill05_') and 20<=int(k.rsplit('_',1)[-1])<=27 for k in actions[3000+10000*form]),'Final wave must not displace the main body'
    files=[NAME+'.'+s for s in ['def','cns','cmd','air','sff','snd']]+[NAME+'_common.cns'];result=dict(runtime_sha256=sha(b''.join((CHAR/f).read_bytes() for f in files)),exact_rgba_frames=count,retained_translucent_pixels=semi,movement_uses_movement_sprites=True,source_crops=8,final_wave_separate_from_body=True,format='MUGEN 1.1 SFF 2.01 PNG32 (12), 32-bit RGBA')
    (ROOT/'previews'/(NAME+'_rendering_checks.json')).write_text(json.dumps(result,indent=2)+'\n');print('PASS: 161 source frames retain every RGBA byte;',semi,'translucent pixels; movement and final-wave separation')
if __name__=='__main__':main()
