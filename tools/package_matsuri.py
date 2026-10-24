#!/usr/bin/env python3
"""Build and verify Matsuri's deterministic standalone character archive."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib,json,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MatsuriShinju'
FILES=[f'MatsuriShinju.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['MatsuriShinju_common.cns','LEEME.md','CONTROLES_XBOX.md','CREDITOS_Y_FUENTES.md']
def main():
 archive=ROOT/'MatsuriShinju.zip'
 with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
  for name in sorted(FILES):
   info=ZipInfo('MatsuriShinju/'+name,(2026,10,23,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,(CHAR/name).read_bytes(),compresslevel=9)
 with tempfile.TemporaryDirectory(prefix='matsuri-package-') as tmp:
  with ZipFile(archive) as z:
   assert z.testzip() is None;z.extractall(tmp)
   for name in FILES:assert z.read('MatsuriShinju/'+name)==(CHAR/name).read_bytes()
  subprocess.run([sys.executable,str(ROOT/'tools/validate_matsuri.py'),str(Path(tmp)/'MatsuriShinju')],check=True)
 result=dict(archive=archive.name,bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files={name:hashlib.sha256((CHAR/name).read_bytes()).hexdigest() for name in FILES})
 (ROOT/'previews/MatsuriShinju_delivery_manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('PACKAGED',archive.name,result['bytes'],'bytes')
if __name__=='__main__':main()
