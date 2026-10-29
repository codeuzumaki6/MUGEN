#!/usr/bin/env python3
"""Cross-check the supplied archive, original crops, packed sprites and audio."""
from pathlib import Path
import json,plistlib,struct,zlib
from PIL import Image
from boruto_source import ROOT,nums,sha
from boruto_tbv_sff import read_sff
NAME='BorutoTBVBase';CHAR=ROOT/NAME;SOURCE=ROOT/'source_material/BorutoTBV_original'
def main():
 archive=json.loads((SOURCE/'archive_checks.json').read_text());assert archive['all_crc_passed'] and len(archive['original_files'])==45
 for r in archive['original_files']:
  data=(SOURCE/r['file']).read_bytes();assert len(data)==r['bytes'] and sha(data)==r['sha256'] and f'{zlib.crc32(data)&0xffffffff:08X}'==r['crc32']
 sff=read_sff(CHAR/(NAME+'.sff'));manifest=json.loads((CHAR/'assets/sprites.json').read_text());cache={};original=0
 for r in manifest:
  w,h,x,y,pix,pal=sff[r['group'],r['number']];assert [x,y]==r['axis'] and sha(pix)==r['pixels_sha256'] and sha(pal)==r['palette_sha256']
  if r['group']!=31000:continue
  original+=1;p=ROOT/r['source_plist']
  if p not in cache:
   d=plistlib.loads(p.read_bytes());cache[p]=(d,Image.open(p.parent/d['metadata']['textureFileName']).convert('RGBA'))
  d,sheet=cache[p];frame=d['frames'][r['source_key']];xx,yy,ww,hh=map(int,nums(frame['frame']));im=sheet.crop((xx,yy,xx+ww,yy+hh));im=im.transpose(Image.Transpose.ROTATE_90) if frame.get('rotated') else im;actual=Image.open(CHAR/r['file']).convert('RGBA');assert im.tobytes()==actual.tobytes()==pix and not pal and im.size==actual.size and sha(actual.tobytes())==r['rgba_sha256'] and not r['redrawn'] and not r['ai_generated']
 assert original==161
 b=(CHAR/(NAME+'.snd')).read_bytes();count,off=struct.unpack_from('<2I',b,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',b,off);samples[g,n]=b[off+16:off+16+size];off=nxt
 audio=json.loads((CHAR/'assets/sounds.json').read_text())['source_audio']
 for r in audio:assert sha((ROOT/r['source']).read_bytes())==r['source_sha256'] and sha(samples[r['group'],r['number']])==r['wav_sha256']
 proof=dict(original_files=45,original_frames=161,original_rgba_preserved=True,packed_rgba_preserved=True,png32_original_frames=161,original_audio=len(audio),total_sounds=count,empty_cells_excluded=17,source_archive=archive['sha256'])
 (ROOT/'previews'/f'{NAME}_source_checks.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS',proof)
if __name__=='__main__':main()
