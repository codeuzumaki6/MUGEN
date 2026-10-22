#!/usr/bin/env python3
"""Package the installed character, then validate the extracted download."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib,json,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Mamushi'
files=['Mamushi'+suffix for suffix in ['.def','.cns','.cmd','.air','.sff','.snd']]+['AC_Mamushi.def','common1.cns','LEEME.md','CONTROLES_XBOX.md','CREDITOS_Y_FUENTES.md']
archive=ROOT/'Mamushi_SHINJU.zip'
with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as out:
    for name in sorted(files):
        info=ZipInfo('Mamushi/'+name,date_time=(2026,10,21,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16
        out.writestr(info,(CHAR/name).read_bytes(),compresslevel=9)
with tempfile.TemporaryDirectory(prefix='mamushi-delivery-') as tmp:
    with ZipFile(archive) as z:
        assert z.testzip() is None;z.extractall(tmp)
        for name in files:assert z.read('Mamushi/'+name)==(CHAR/name).read_bytes()
    subprocess.run([sys.executable,str(ROOT/'tools/validate_mamushi.py'),str(Path(tmp)/'Mamushi')],check=True)
manifest=dict(archive=archive.name,bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files={name:hashlib.sha256((CHAR/name).read_bytes()).hexdigest() for name in files})
(ROOT/'previews/Mamushi_delivery_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PACKAGED',archive.name,archive.stat().st_size,'bytes;',len(files),'installed files, extracted and validated')
