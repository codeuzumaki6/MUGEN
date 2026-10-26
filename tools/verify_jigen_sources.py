#!/usr/bin/env python3
"""Verify the uploaded archive, exact sprite crops and original audio sources."""
from pathlib import Path
import argparse, hashlib, json, plistlib, re, zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source_material/Jigen_original'
CHAR=ROOT/'JigenKara'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);ap.add_argument('video',type=Path);args=ap.parse_args()
 preserved={}
 with zipfile.ZipFile(args.archive) as z:
  assert z.testzip() is None
  for info in z.infolist():
   if info.is_dir():continue
   path=SOURCE/info.filename
   assert path.read_bytes()==z.read(info),info.filename
   preserved[info.filename]=sha(path.read_bytes())
 manifest=json.loads((CHAR/'assets/sprites.json').read_text());originals=[p for p in manifest if p['group'] in [30000,30001]];derived=[p for p in manifest if p['group'] in [30002,30003,30004]]
 assert len(originals)==154 and len(derived)==21
 for cell in originals:
  plist=ROOT/cell['source_plist'];data=plistlib.loads(plist.read_bytes());sheet=Image.open(plist.parent/data['metadata']['textureFileName']).convert('RGBA');frame=data['frames'][cell['key']]
  x,y,w,h=map(int,re.findall(r'-?\d+',frame['frame']));im=sheet.crop((x,y,x+w,y+h))
  if frame.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
  actual=Image.open(CHAR/cell['file']).convert('RGBA')
  assert im.size==actual.size and im.tobytes()==actual.tobytes(),cell['key']
  assert sha(im.tobytes())==cell['rgba_sha256'] and not cell['redrawn'] and not cell['ai_generated']
 bykey={r['key']:r for r in manifest}
 for cell in derived:
  im=Image.open(CHAR/bykey[cell['source_key']]['file']).convert('RGBA').crop(cell['source_rectangle']);actual=Image.open(CHAR/cell['file']).convert('RGBA')
  assert im.size==actual.size and im.tobytes()==actual.tobytes(),cell['key']
  assert sha(im.tobytes())==cell['rgba_sha256']
 excluded=json.loads((CHAR/'assets/excluded_frames.json').read_text());keys=json.loads((CHAR/'assets/keys.json').read_text())
 assert set(excluded)=={'Jigenol','Jiraiya_Float_03','Jiraiya_wake_06'} and not set(excluded)&keys.keys()
 sounds=json.loads((CHAR/'assets/sounds.json').read_text())['source_audio'];assert len(sounds)==44
 for item in sounds:assert sha((ROOT/item['source']).read_bytes())==item['source_sha256']
 for cell in originals+derived:
  if cell['kind'] in ['body','body_with_effect']:
   im=Image.open(CHAR/cell['file']);x,y=cell['axis'];assert 0<=x<im.width and 0<=y<im.height,cell['key']
 anchors=json.loads((CHAR/'assets/horn_anchors.json').read_text());assert len(anchors)>50
 for anchor in anchors:
  cell=bykey[anchor['key']];im=Image.open(CHAR/cell['file']);x,y=anchor['head'];assert 0<=x<im.width and 0<=y<im.height
 proof=dict(archive=dict(name=args.archive.name,bytes=args.archive.stat().st_size,sha256=sha(args.archive.read_bytes())),gameplay_reference=dict(name=args.video.name,bytes=args.video.stat().st_size,sha256=sha(args.video.read_bytes())),original_files=preserved,original_frames=154,derived_crops=21,original_audio=44,original_rgba_preserved=True,excluded_empty_frames=excluded,horn_poses=len(anchors),horn_uses_original_pixels=True)
 for p in [ROOT/'previews/JigenKara_source_checks.json',SOURCE/'source.json']:p.write_text(json.dumps(proof,indent=2)+'\n')
 print(f'PASS: {len(preserved)} original files, 154 original cells, 21 exact derived crops, 44 original audio sources, {len(anchors)} horn anchors')
if __name__=='__main__':main()
