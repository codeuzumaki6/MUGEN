#!/usr/bin/env python3
"""Package only installed runtime files and validate the extracted artifact."""
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

root=Path(__file__).resolve().parents[1]
char=root/'Eida'
files={'Eida.def'}
text=(char/'Eida.def').read_text()
for key,value in re.findall(r'(?im)^\s*([a-z0-9]+)\s*=\s*([^;\r\n]+)',text):
    if key in {'sprite','sound','anim','cmd','cns','stcommon','st'} or re.fullmatch(r'st\d+',key):
        files.add(value.strip())
files.update(p.name for p in char.glob('*.md'))
destination=root/'Eida_FIX_CARGA_MUGEN11.zip'
with ZipFile(destination,'w',ZIP_DEFLATED,compresslevel=9) as archive:
    for name in sorted(files):
        archive.write(char/name,'Eida/'+name)
with tempfile.TemporaryDirectory(prefix='eida-delivery-') as directory:
    with ZipFile(destination) as archive:
        assert archive.testzip() is None
        archive.extractall(directory)
    subprocess.run([sys.executable,str(root/'tools/validate_character.py'),str(Path(directory)/'Eida')],check=True)
print(f'{destination}: {destination.stat().st_size} bytes; {len(files)} runtime/documentation files')
# Keep the previous branch-based download pointed at the fixed runtime too.
shutil.copyfile(destination,root/'Eida_OMNIPOTENCIA_COMBOS.zip')
