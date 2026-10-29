#!/usr/bin/env python3
"""Regression: every release sprite uses visible, compatible indexed data."""
import json,re,struct
import numpy as np
from PIL import Image
from boruto_source import ROOT,sha
from boruto_tbv_sff import read_sff
NAME='BorutoTBVBase';CHAR=ROOT/NAME
def main():
    sprites=read_sff(CHAR/(NAME+'.sff'));manifest=json.loads((CHAR/'assets/sprites.json').read_text());keys={(r['group'],r['number']):r['key'] for r in manifest};byname={r['key']:r for r in manifest};opaque=0;count=0;light_layers=0
    data=(CHAR/(NAME+'.sff')).read_bytes();sh,total=struct.unpack_from('<2I',data,36)
    for i in range(total):
        header=struct.unpack_from('<4H2hH2B2I2H',data,sh+i*28)
        assert header[7]==2 and header[8]==8, 'PNG/true-colour sprite leaked into compatible release'
    for r in manifest:
        w,h,x,y,pixels,palette=sprites[r['group'],r['number']]
        assert len(pixels)==w*h and len(palette)==1024,r['key']
        if r['group']==31000:
            im=Image.open(CHAR/r['file']).convert('RGBA');alpha=np.array(im)[:,:,3];index=np.frombuffer(pixels,dtype=np.uint8).reshape(h,w);solid=alpha>=250
            assert any(pixels),r['key']
            assert np.all(index[solid]>0),(r['key'],'Opaque character pixels became invisible')
            assert np.all(index[alpha==0]==0),(r['key'],'Transparent canvas became opaque')
            opaque+=int(solid.sum());count+=1
        if r.get('source_light_parent'):
            source=np.array(Image.open(CHAR/byname[r['source_light_parent']]['file']).convert('RGBA'));alpha=source[:,:,3];mask=(alpha>0)&(alpha<250);index=np.frombuffer(pixels,dtype=np.uint8).reshape(h,w)
            assert np.array_equal(index>0,mask),(r['key'],'Light layer contains opaque actor pixels')
            colour=np.frombuffer(palette,dtype=np.uint8).reshape(256,4)[index,:3];expected=((source[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8')
            if mask.any():assert np.abs(colour[mask].astype(int)-expected[mask].astype(int)).mean()<8
            light_layers+=1
        if r.get('source_parent'):
            im=Image.open(CHAR/byname[r['source_parent']]['file']).convert('RGBA').crop(r['source_rect']);assert im.tobytes()==Image.open(CHAR/r['file']).convert('RGBA').tobytes()
    assert count==161 and opaque>10000 and light_layers==77
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
    files=[NAME+'.'+s for s in ['def','cns','cmd','air','sff','snd']]+[NAME+'_common.cns'];result=dict(runtime_sha256=sha(b''.join((CHAR/f).read_bytes() for f in files)),original_source_frames=count,indexed_release_sprites=total,png32_release_sprites=0,preserved_opaque_pixels=opaque,source_light_layers=light_layers,no_opaque_actor_in_light=True,movement_uses_movement_sprites=True,source_crops=8,final_wave_separate_from_body=True,format='SFF RLE8, 8-bit indexed; no PNG32 dependency')
    (ROOT/'previews'/(NAME+'_rendering_checks.json')).write_text(json.dumps(result,indent=2)+'\n');print('PASS:',total,'indexed RLE8 sprites, no PNG32;',opaque,'opaque pixels retained; movement corrections retained')
if __name__=='__main__':main()
