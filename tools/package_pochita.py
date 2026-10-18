#!/usr/bin/env python3
"""Make a self-contained, verified runtime ZIP, excluding development assets."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'PochitaTrueForm'
files=['PochitaTrueForm'+x for x in ['.def','.sff','.snd','.air','.cmd','.cns']]+['common1.cns','LEEME.md','CONTROLES_XBOX.md','CREDITOS_Y_FUENTES.md']
subprocess.run([sys.executable,str(ROOT/'tools/validate_pochita.py'),str(CHAR)],check=True)
archive=ROOT/'PochitaTrueForm.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in files:
  info=zipfile.ZipInfo('PochitaTrueForm/'+name,date_time=(2026,10,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,(CHAR/name).read_bytes())
with tempfile.TemporaryDirectory(prefix='pochita-delivery-') as directory:
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None;z.extractall(directory)
 for name in files:assert (Path(directory)/'PochitaTrueForm'/name).read_bytes()==(CHAR/name).read_bytes()
 subprocess.run([sys.executable,str(ROOT/'tools/validate_pochita.py'),str(Path(directory)/'PochitaTrueForm')],check=True)
manifest={'archive':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files':{name:hashlib.sha256((CHAR/name).read_bytes()).hexdigest() for name in files},'validation':'Ikemen GO: 78 raw-input/collision scenarios + 1 CPU smoke; exact Jump Force MUGEN V14 not executed'}
(ROOT/'previews/Pochita_delivery_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(archive.name,manifest['bytes'],'bytes',manifest['sha256'])
