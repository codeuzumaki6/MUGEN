#!/usr/bin/env python3
"""Check original archive bytes, atlas crops, actor-free effects and coverage."""
import json,plistlib,re,struct,zlib
import numpy as np
from PIL import Image
from boruto_source import ROOT,nums,sha
from boruto_tbv_sff import read_sff
NAME='NarutoKCM';CHAR=ROOT/NAME;SOURCE=ROOT/'source_material/NarutoKCM_original'
def main():
 archive=json.loads((SOURCE/'archive_checks.json').read_text());assert archive['all_crc_passed']
 for r in archive['original_files']:
  data=(SOURCE/r['file']).read_bytes();assert len(data)==r['bytes'] and sha(data)==r['sha256'] and f'{zlib.crc32(data)&0xffffffff:08X}'==r['crc32']
 packed=read_sff(CHAR/(NAME+'.sff'));manifest=json.loads((CHAR/'assets/sprites.json').read_text());bykey={r['key']:r for r in manifest};byid={(r['group'],r['number']):r for r in manifest};cache={};originals=set();light=0;cleaned=0
 data=(CHAR/(NAME+'.sff')).read_bytes();sh,count=struct.unpack_from('<2I',data,36)
 for i in range(count):assert struct.unpack_from('<4H2hH2B2I2H',data,sh+i*28)[7:9]==(2,8)
 for r in manifest:
  w,h,x,y,pix,pal=packed[r['group'],r['number']];assert [x,y]==r['axis'] and sha(pix)==r['pixels_sha256'] and sha(pal)==r['palette_sha256'];im=Image.open(CHAR/r['file']).convert('RGBA');assert sha(im.tobytes())==r['rgba_sha256']
  if r['group']==30000:
   originals.add(r['key']);p=ROOT/r['source_plist']
   if p not in cache:
    d=plistlib.loads(p.read_bytes());cache[p]=(d,Image.open(p.parent/d['metadata']['textureFileName']).convert('RGBA'))
   d,sheet=cache[p];f=d['frames'][r['source_key']];xx,yy,ww,hh=map(int,nums(f['frame']));actual=sheet.crop((xx,yy,xx+ww,yy+hh));actual=actual.transpose(Image.Transpose.ROTATE_90) if f.get('rotated') else actual;assert actual.tobytes()==im.tobytes()
   a=np.array(im);idx=np.frombuffer(pix,np.uint8).reshape(h,w);assert np.all(idx[a[:,:,3]>=250]>0) and np.all(idx[a[:,:,3]==0]==0)
  if r.get('source_light_parent'):
   parent=np.array(Image.open(CHAR/bykey[r['source_light_parent']]['file']).convert('RGBA'));mask=(parent[:,:,3]>0)&(parent[:,:,3]<250);assert np.array_equal(np.frombuffer(pix,np.uint8).reshape(h,w)>0,mask) and r['axis']==bykey[r['source_light_parent']]['axis'];light+=1
  if 'interpolated_caster_rect' in r:
   a=np.array(Image.open(CHAR/bykey[r['source_parent']]['file']).convert('RGBA'));rect=r['interpolated_caster_rect']
   for yy in range(rect[1],rect[3]) if rect else []:
    lo=max(0,rect[0]-1);hi=min(w-1,rect[2])
    for xx in range(rect[0],rect[2]):a[yy,xx]=np.round((a[yy,lo].astype(float)*(hi-xx)+a[yy,hi].astype(float)*(xx-lo))/(hi-lo)).astype('uint8')
   if r.get('source_ground_fade'):
    start,finish=r['source_ground_fade'];yy=np.indices(a.shape[:2])[0];a[:,:,3]=np.round(a[:,:,3]*np.clip((yy-start)/(finish-start),0,1)).astype('uint8');a[a[:,:,3]==0]=0
   assert np.array_equal(a,np.array(im));cleaned+=bool(rect) or bool(r.get('source_ground_fade'))
  if r.get('source_effect_crop'):
   parent=Image.open(CHAR/bykey[r['source_parent']]['file']).convert('RGBA');a=np.array(parent.crop(tuple(r['source_effect_crop'])));yy,xx=np.indices(a.shape[:2]);radius=r['source_effect_radius'];distance=np.hypot(xx-radius,yy-radius);cool=(a[:,:,2].astype(float)>=a[:,:,0]*.95)&(a[:,:,1].astype(float)>=a[:,:,0]*.9);a[:,:,3]=np.round(a[:,:,3]*np.clip((radius-distance)/r['source_effect_feather'],0,1)*cool).astype('uint8');a[a[:,:,3]==0]=0;assert np.array_equal(a,np.array(im))
 used=set()
 for line in (CHAR/(NAME+'.air')).read_text().splitlines():
  m=re.match(r'\s*(\d+),(\d+),',line)
  if not m:continue
  r=byid[int(m[1]),int(m[2])]
  if r['group']==30000:used.add(r['key'])
  if r.get('source_parent'):used.add(r['source_parent'])
 assert len(originals)==198 and used==originals,('Unused supplied frames',originals-used)
 excluded=json.loads((CHAR/'assets/excluded_frames.json').read_text());assert len(excluded)==17 and {r['key'] for r in excluded}=={'nol_01','vaydra'}|{f'FutonSRK2_Move_{i:02}' for i in range(1,4)}|{'FutonSRK2_Dead_07'}|{f'FutonSRK_Dead_{i:02}' for i in range(1,9)}|{f'FutonSRK_Move_{i:02}' for i in range(1,4)}
 data=(CHAR/(NAME+'.snd')).read_bytes();count,off=struct.unpack_from('<2I',data,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',data,off);samples[g,n]=data[off+16:off+16+size];off=nxt
 audio=json.loads((CHAR/'assets/sounds.json').read_text())
 for r in audio['source_audio']:assert sha((ROOT/r['source']).read_bytes())==r['source_sha256'] and sha(samples[r['group'],r['number']])==r['wav_sha256']
 result=dict(original_files=len(archive['original_files']),original_frames=len(originals),used_source_frames=len(used),original_rgba_preserved=True,indexed_sprites=len(packed),png32_sprites=0,light_layers=light,actor_free_effects=cleaned,excluded_atlas_cells=len(excluded),source_audio_references=len(audio['source_audio']),total_sounds=len(samples),missing_original_audio=audio['missing_source_references'],source_archive_sha256=archive['sha256'])
 (ROOT/'previews'/(NAME+'_source_checks.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
