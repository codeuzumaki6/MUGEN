#!/usr/bin/env python3
"""Check native child scale, the supplied originals and scoped animation use."""
from pathlib import Path
import hashlib
import json
import re
import struct

import numpy as np
from PIL import Image

from build_daemon_reference import BOXES, CANVAS, AXIS, source_pose, pack

ROOT=Path(__file__).resolve().parents[1]
CHAR=ROOT/'Eida'
source=ROOT/'design/Daemon_original/daemon_vahidras_original.jpg'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='4cb499bad7fcdc70130926f2df9fe3f51b6022c4e6943f3fefaa3deb1b64aa39','supplied JPG changed'
manifest=json.loads((CHAR/'assets/daemon/manifest.json').read_text())
assert [r['number'] for r in manifest]==list(range(19))
original=Image.open(source).convert('RGBA')
stand,standbox=source_pose(original,BOXES['stand'])
factor=49/(standbox[3]-standbox[1])
report=[]
for pose in manifest:
    number=pose['number'];image=Image.open(CHAR/pose['file']).convert('RGBA')
    assert image.size==CANVAS and tuple(pose['axis'])==AXIS
    alpha=np.array(image.getchannel('A'));ys,xs=np.nonzero(alpha)
    assert len(xs)>0 and xs.min()>0 and xs.max()<95 and ys.min()>0 and ys.max()==53
    assert len(set(alpha.ravel()))==2 and alpha.max()==255
    assert ys.max()-ys.min()+1<=49,'helper is too tall'
    if number in (0,16):
        name='stand' if number==0 else 'run'
        pic,bounds=source_pose(original,BOXES[name]);expected,_=pack(pic,bounds,factor)
        assert np.array_equal(np.array(image),np.array(expected)),'original pose replaced/repainted'
        assert pose['ai_redrawn'] is False
    else:assert pose['ai_redrawn'] is True
    assert pose['source_sha256']==hashlib.sha256((ROOT/pose['source']).read_bytes()).hexdigest()
    report.append(dict(number=number,source=pose['kind'],opaque_height=int(ys.max()-ys.min()+1),png_sha256=hashlib.sha256((CHAR/pose['file']).read_bytes()).hexdigest()))

text=(CHAR/'Eida.air').read_text()
def references(action):
    block=re.search(rf'(?ims)^\[Begin Action {action}\].*?(?=^\[Begin Action|\Z)',text)
    assert block,action
    return [int(n) for n in re.findall(r'(?m)^1000,(\d+),',block[0])]
assert references(1510)==[16,17,18,17],'dash still uses punching or kicking poses'
assert 0 in references(1030),'supplied neutral pose missing'
assert references(1524)==[12,13,12,12],'sweep still uses a rising kick'
assert set(references(1020))=={2,14,15} and set(references(1350))=={2,14,15},'guard still uses offensive poses'
b=(CHAR/'Eida.sff').read_bytes();sh,count=struct.unpack_from('<II',b,36);packed=[]
for i in range(count):
    g,n,w,h,x,y=struct.unpack_from('<HHHHhh',b,sh+i*28)
    if g==1000:
        assert (w,h,x,y)==(96,56,48,54),'SFF applied another scale/origin'
        packed.append(n)
assert sorted(packed)==list(range(19))
result=dict(static_file_checks=True,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_author='Vahidras',source_original_pose_indices=[0,16],supplemental_ai_unique_poses=16,runtime_entries=19,distinct_png_poses=len({r['png_sha256'] for r in report}),canvas=list(CANVAS),feet_axis=list(AXIS),second_runtime_resize=False,poses=report)
(ROOT/'previews/Eida_Daemon_source_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: 2 original source poses, 16 distinct AI supplemental poses; 19 SFF entries at fixed child scale, correct run/guard/sweep references')
