#!/usr/bin/env python3
"""Byte preservation of the uploaded archive and exact original Code crops."""
from pathlib import Path
import argparse,hashlib,json,plistlib,re,zipfile,sys
from PIL import Image
from build_code_nl_assets import snd
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'CodeNoLimiter';SOURCE=ROOT/'source_material/CodeNoLimiter_original'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);ap.add_argument('video',type=Path);args=ap.parse_args();preserved={}
 with zipfile.ZipFile(args.archive) as z:
  assert z.testzip() is None
  for i in z.infolist():
   if i.is_dir():continue
   p=SOURCE/i.filename;assert p.read_bytes()==z.read(i),i.filename;preserved[i.filename]=sha(p.read_bytes())
 manifest=json.loads((CHAR/'assets/sprites.json').read_text());cells=[r for r in manifest if r['group'] in [31000,31001]];assert len(cells)==241
 for c in cells:
  p=ROOT/c['source_plist'];meta=plistlib.loads(p.read_bytes());frame=meta['frames'][c['source_key']];sheet=Image.open(p.parent/meta['metadata']['textureFileName']).convert('RGBA');x,y,w,h=map(int,re.findall(r'-?\d+',frame['frame']));im=sheet.crop((x,y,x+w,y+h))
  if frame.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
  actual=Image.open(CHAR/c['file']).convert('RGBA');assert im.size==actual.size and im.tobytes()==actual.tobytes() and sha(im.tobytes())==c['rgba_sha256'],c['key'];assert not c['redrawn'] and not c['ai_generated']
 excluded=json.loads((CHAR/'assets/excluded_frames.json').read_text());assert excluded['empty']==['CodeNol_01'] and excluded['unrelated_frames']==23
 sounds=json.loads((CHAR/'assets/sounds.json').read_text());assert len(sounds['source_audio'])==13 and not sounds['uploaded_zip_has_audio'];original=snd(ROOT/'source_material/Shibai_Code_reference/Code.snd');delivered=snd(CHAR/'CodeNoLimiter.snd')
 for c in sounds['source_audio']:
  assert sha(original[c['source_group'],c['source_number']])==c['source_wav_sha256'];assert sha(delivered[c['group'],c['number']])==c['wav_sha256']
 proof=dict(archive=dict(name=args.archive.name,bytes=args.archive.stat().st_size,sha256=sha(args.archive.read_bytes())),gameplay_reference=dict(name=args.video.name,sha256=sha(args.video.read_bytes())),original_files=preserved,original_frames=241,original_rgba_preserved=True,excluded=excluded,uploaded_zip_has_audio=False,reused_code_samples=13,source_code_snd_sha256=sounds['source_snd_sha256'])
 for p in [ROOT/'previews/CodeNoLimiter_source_checks.json',SOURCE/'source.json']:p.write_text(json.dumps(proof,indent=2)+'\n')
 print('PASS: 17 preserved files, 241 exact original RGBA cells, 13 Code sound sources')
if __name__=='__main__':main()
