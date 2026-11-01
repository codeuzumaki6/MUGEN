#!/usr/bin/env python3
"""Original ZIP/atlas/audio integrity, indexed visibility and frame coverage."""
import json,plistlib,struct,zlib,re
import numpy as np
from PIL import Image
from boruto_source import ROOT,nums,sha
from boruto_tbv_sff import read_sff
NAME='KonohamaruTBV';CHAR=ROOT/NAME;SOURCE=ROOT/'source_material/Konohamaru_original'
def main():
 archive=json.loads((SOURCE/'archive_checks.json').read_text());assert archive['all_crc_passed']
 for r in archive['original_files']:
  data=(SOURCE/r['file']).read_bytes();assert len(data)==r['bytes'] and sha(data)==r['sha256'] and f'{zlib.crc32(data)&0xffffffff:08X}'==r['crc32']
 sprites=read_sff(CHAR/(NAME+'.sff'));manifest=json.loads((CHAR/'assets/sprites.json').read_text());bykey={r['key']:r for r in manifest};byid={(r['group'],r['number']):r for r in manifest};cache={};original=0;opaque=0;light=0
 data=(CHAR/(NAME+'.sff')).read_bytes();sh,count=struct.unpack_from('<2I',data,36)
 for i in range(count):
  header=struct.unpack_from('<4H2hH2B2I2H',data,sh+i*28);assert header[7:9]==(2,8),'Non-indexed sprite in release'
 for r in manifest:
  w,h,x,y,pix,pal=sprites[r['group'],r['number']];assert [x,y]==r['axis'] and sha(pix)==r['pixels_sha256'] and sha(pal)==r['palette_sha256'];actual=Image.open(CHAR/r['file']).convert('RGBA');assert sha(actual.tobytes())==r['rgba_sha256']
  if r['group']==30000:
   original+=1;p=ROOT/r['source_plist']
   if p not in cache:
    d=plistlib.loads(p.read_bytes());cache[p]=(d,Image.open(p.parent/d['metadata']['textureFileName']).convert('RGBA'))
   d,sheet=cache[p];f=d['frames'][r['source_key']];xx,yy,ww,hh=map(int,nums(f['frame']));im=sheet.crop((xx,yy,xx+ww,yy+hh));im=im.transpose(Image.Transpose.ROTATE_90) if f.get('rotated') else im;assert im.tobytes()==actual.tobytes()
   a=np.array(actual);idx=np.frombuffer(pix,np.uint8).reshape(h,w);solid=a[:,:,3]>=250;assert np.all(idx[solid]>0) and np.all(idx[a[:,:,3]==0]==0);opaque+=int(solid.sum())
   if r['key'].startswith(('KakashiSkill01_','Kakashi_Skil01_')):assert r['axis']==bykey['Kakashi_Skill01_'+r['key'].rsplit('_',1)[1]]['axis'],'Unflattened 2.5D clone offset'
  if r.get('source_light_parent'):
   parent=np.array(Image.open(CHAR/bykey[r['source_light_parent']]['file']).convert('RGBA'));mask=(parent[:,:,3]>0)&(parent[:,:,3]<250);idx=np.frombuffer(pix,np.uint8).reshape(h,w);assert np.array_equal(idx>0,mask);assert r['axis']==bykey[r['source_light_parent']]['axis'];light+=1
  if r.get('excluded_caster_rects') is not None:
   a=np.array(Image.open(CHAR/bykey[r['source_parent']]['file']).convert('RGBA'))
   for x0,y0,x1,y1 in r['excluded_caster_rects']:a[y0:y1,x0:x1]=0
   assert np.array_equal(a,np.array(actual))
 used=set()
 for line in (CHAR/(NAME+'.air')).read_text().splitlines():
  m=re.match(r'\s*(\d+),(\d+),',line)
  if not m:continue
  r=byid[int(m[1]),int(m[2])]
  if r['group']==30000:used.add(r['key'])
  if r.get('source_parent'):used.add(r['source_parent'])
 assert original==301 and used=={r['key'] for r in manifest if r['group']==30000},('Unused original frames',set(bykey)-used)
 data=(CHAR/(NAME+'.snd')).read_bytes();count,off=struct.unpack_from('<2I',data,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',data,off);samples[g,n]=data[off+16:off+16+size];off=nxt
 audio=json.loads((CHAR/'assets/sounds.json').read_text())
 for r in audio['source_audio']:assert sha((ROOT/r['source']).read_bytes())==r['source_sha256'] and sha(samples[r['group'],r['number']])==r['wav_sha256']
 result=dict(original_files=len(archive['original_files']),original_frames=original,used_source_frames=len(used),original_rgba_preserved=True,indexed_sprites=len(sprites),png32_sprites=0,preserved_opaque_pixels=opaque,light_layers=light,source_audio_references=len(audio['source_audio']),total_sounds=len(samples),missing_original_audio=audio['missing_source_references'],source_archive_sha256=archive['sha256'])
 (ROOT/'previews'/(NAME+'_source_checks.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
