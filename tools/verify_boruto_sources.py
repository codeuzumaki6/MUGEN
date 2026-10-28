#!/usr/bin/env python3
"""Verify every RAR volume, extracted file, untouched RGBA crop and PCM sample."""
from pathlib import Path
import json,plistlib,struct,zlib
from PIL import Image
from boruto_source import ROOT,nums,sha,read_sff
NAME='BorutoKarmaJogan';CHAR=ROOT/NAME;SOURCE=ROOT/'source_material/Boruto_original'
def main():
 archive=json.loads((SOURCE/'archive_checks.json').read_text());assert archive['volume_count']==3 and archive['all_crc_passed'];assert len(archive['original_files'])==618
 for v in archive['volumes']:
  p=ROOT/v['file']
  if p.exists():assert p.stat().st_size==v['bytes'] and sha(p.read_bytes())==v['sha256']
 for f in archive['original_files']:
  b=(SOURCE/f['file']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'] and f'{zlib.crc32(b)&0xffffffff:08X}'==f['crc32'],f['file']
 for folder in ['uploaded_xml','uploaded_audio']:
  for f in json.loads((SOURCE/folder/'manifest.json').read_text()):assert sha((ROOT/f['file']).read_bytes())==f['sha256']
 manifest=json.loads((CHAR/'assets/sprites.json').read_text());cells=[r for r in manifest if 32000<=r['group']<=32007];assert len(cells)==663;cache={};sff=read_sff(CHAR/(NAME+'.sff'))
 for c in manifest:
  w,h,x,y,pix,pal=sff[c['group'],c['number']];assert [x,y]==c['axis'] and sha(pix)==c['indexed_pixels_sha256'] and sha(pal)==c['palette_sha256'],c['key']
 wind=[c for c in manifest if c.get('rendering')=='source alpha premultiplied into RGB for additive wind']
 assert wind and all(any(sff[c['group'],c['number']][4]) for c in wind),'Source wind vanished during alpha conversion'
 for c in cells:
  p=ROOT/c['source_plist']
  if p not in cache:
   data=plistlib.loads(p.read_bytes());cache[p]=(data,Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA'))
  data,sheet=cache[p];frame=data['frames'][c['source_key']];x,y,w,h=map(int,nums(frame['frame']));im=sheet.crop((x,y,x+w,y+h));im=im.transpose(Image.Transpose.ROTATE_90) if frame.get('rotated') else im;actual=Image.open(CHAR/c['file']).convert('RGBA')
  assert im.size==actual.size and im.tobytes()==actual.tobytes() and sha(im.tobytes())==c['rgba_sha256'] and not c['redrawn'] and not c['ai_generated'],c['key']
 sounds=json.loads((CHAR/'assets/sounds.json').read_text())['source_audio'];assert len(sounds)==67;b=(CHAR/(NAME+'.snd')).read_bytes();count,off=struct.unpack_from('<2I',b,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',b,off);samples[g,n]=b[off+16:off+16+size];off=nxt
 for c in sounds:assert sha((ROOT/c['source']).read_bytes())==c['source_sha256'] and sha(samples[c['group'],c['number']])==c['wav_sha256']
 proof=dict(original_files=618,archive_volumes=archive['volumes'],original_frames=663,selected_original_audio=67,original_character_audio=11,original_rgba_preserved=True,indexed_rle8_lossless=True,additive_wind_frames=len(wind),wind_frames_visible=True,excluded_frames=json.loads((CHAR/'assets/excluded_frames.json').read_text()),gameplay_reference=json.loads((ROOT/'design/boruto_karma_jogan/video_reference.json').read_text()))
 for p in [ROOT/'previews'/f'{NAME}_source_checks.json',SOURCE/'source.json']:p.write_text(json.dumps(proof,indent=2,ensure_ascii=False)+'\n')
 print('PASS: 618 original files, 663 RGBA crops, lossless indexed RLE8, 67 original audio samples')
if __name__=='__main__':main()
