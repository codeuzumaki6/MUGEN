#!/usr/bin/env python3
"""Build a deterministic standalone ZIP and validate the extracted download."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib,json,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Shibai'
files=[f'Shibai.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['common1.cns','LEEME.md','CONTROLES_XBOX.md','CREDITOS_Y_FUENTES.md'];archive=ROOT/'Shibai_OTSUTSUKI.zip'
with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
 for name in sorted(files):
  info=ZipInfo('Shibai/'+name,(2026,10,21,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,(CHAR/name).read_bytes(),compresslevel=9)
with tempfile.TemporaryDirectory(prefix='shibai-delivery-') as tmp:
 with ZipFile(archive) as z:
  assert z.testzip() is None;z.extractall(tmp)
  for name in files:assert z.read('Shibai/'+name)==(CHAR/name).read_bytes()
 subprocess.run([sys.executable,str(ROOT/'tools/validate_shibai.py'),str(Path(tmp)/'Shibai')],check=True)
manifest=dict(archive=archive.name,bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files={n:hashlib.sha256((CHAR/n).read_bytes()).hexdigest() for n in files})
(ROOT/'previews/Shibai_delivery_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('PACKAGED',archive.name,manifest['bytes'],'bytes;',len(files),'standalone files')
