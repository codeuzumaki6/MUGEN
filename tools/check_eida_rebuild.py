#!/usr/bin/env python3
"""Catch duplicate-state/repeated-builder regressions in the Eida artifact."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
FILES=['Eida.cns','Specials.cns','Omnipotencia.cns','Eida.air','Eida.sff','Eida.snd']
def snapshot():return {n:hashlib.sha256((ROOT/'Eida'/n).read_bytes()).hexdigest() for n in FILES}
snapshots=[]
for iteration in range(2):
    for script in ['build_eida_polish.py','build_eida_hug_ultimate.py','build_archives.py']:
        subprocess.run([sys.executable,str(ROOT/'tools'/script)],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(ROOT/'tools/validate_character.py'),str(ROOT/'Eida')],check=True)
    snapshots.append(snapshot())
assert snapshots[0]==snapshots[1],'Repeated build changed runtime or accumulated a state/controller'
(ROOT/'previews/Eida_polish_rebuild_checks.json').write_text(json.dumps(dict(deterministic=True,sha256=snapshots[-1]),indent=2)+'\n')
print('PASS: two identical rebuilds, each structurally validated')
