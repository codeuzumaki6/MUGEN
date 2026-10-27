#!/usr/bin/env python3
"""Verify all uploaded files, unchanged Himawari/Nue crops and original audio."""
from pathlib import Path
import argparse,hashlib,json,plistlib,re,struct,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'HimawariTBV';SOURCE=ROOT/'source_material/Himawari_original'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);ap.add_argument('video',type=Path);args=ap.parse_args();preserved={}
 with zipfile.ZipFile(args.archive) as z:
  assert z.testzip() is None
  for i in z.infolist():
   if i.is_dir():continue
   p=SOURCE/i.filename;assert p.read_bytes()==z.read(i),i.filename;preserved[i.filename]=sha(p.read_bytes())
 manifest=json.loads((CHAR/'assets/sprites.json').read_text());cells=[r for r in manifest if r['group'] in [32000,32001,32002,32003,32004]];assert len(cells)==212
 cache={}
 for c in cells:
  p=ROOT/c['source_plist']
  if p not in cache:
   data=plistlib.loads(p.read_bytes());cache[p]=(data,Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA'))
  data,sheet=cache[p];frame=data['frames'][c['source_key']];x,y,w,h=map(int,re.findall(r'-?\d+',frame['frame']));im=sheet.crop((x,y,x+w,y+h))
  if frame.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
  actual=Image.open(CHAR/c['file']).convert('RGBA');assert im.size==actual.size and im.tobytes()==actual.tobytes() and sha(im.tobytes())==c['rgba_sha256'],c['key'];assert not c['redrawn'] and not c['ai_generated']
 excluded=json.loads((CHAR/'assets/excluded_frames.json').read_text());assert set(excluded)=={'KinkakuET_kyubiCKRNol_01'}
 sounds=json.loads((CHAR/'assets/sounds.json').read_text())['source_audio'];assert len(sounds)==39
 b=(CHAR/'HimawariTBV.snd').read_bytes();count,off=struct.unpack_from('<2I',b,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',b,off);samples[g,n]=b[off+16:off+16+size];off=nxt
 for c in sounds:assert sha((ROOT/c['source']).read_bytes())==c['source_sha256'] and sha(samples[c['group'],c['number']])==c['wav_sha256']
 proof=dict(archive=dict(name=args.archive.name,bytes=args.archive.stat().st_size,sha256=sha(args.archive.read_bytes())),gameplay_reference=dict(name=args.video.name,sha256=sha(args.video.read_bytes())),original_files=preserved,original_frames=212,original_audio=39,original_rgba_preserved=True,excluded_empty_frames=excluded)
 for p in [ROOT/'previews/HimawariTBV_source_checks.json',SOURCE/'source.json']:p.write_text(json.dumps(proof,indent=2)+'\n')
 print('PASS: all supplied files, 212 unchanged original cells, 39 original audio files')
if __name__=='__main__':main()
