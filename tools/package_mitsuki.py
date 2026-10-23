#!/usr/bin/env python3
"""Deterministic standalone Mitsuki TBV download and extraction validation."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib,json,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MitsukiTBV'
FILES=[f'MitsukiTBV.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['MitsukiTBV_common.cns','LEEME.md','CONTROLES_XBOX.md','CREDITOS_Y_FUENTES.md']
def main():
 archive=ROOT/'MitsukiTBV.zip'
 with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
  for name in sorted(FILES):
   i=ZipInfo('MitsukiTBV/'+name,(2026,10,23,0,0,0));i.compress_type=ZIP_DEFLATED;i.external_attr=0o644<<16;z.writestr(i,(CHAR/name).read_bytes(),compresslevel=9)
 with tempfile.TemporaryDirectory(prefix='mitsuki-download-') as tmp:
  with ZipFile(archive) as z:
   assert z.testzip() is None;z.extractall(tmp)
   for name in FILES:assert z.read('MitsukiTBV/'+name)==(CHAR/name).read_bytes()
  subprocess.run([sys.executable,str(ROOT/'tools/validate_mitsuki.py'),str(Path(tmp)/'MitsukiTBV')],check=True)
 result=dict(archive=archive.name,bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files={n:hashlib.sha256((CHAR/n).read_bytes()).hexdigest() for n in FILES})
 (ROOT/'previews/MitsukiTBV_delivery_manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('PACKAGED',archive.name,result['bytes'],'bytes')
if __name__=='__main__':main()
