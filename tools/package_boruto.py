#!/usr/bin/env python3
"""Deterministic standalone package and extraction/reference validation."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1];NAME='BorutoKarmaJogan'
def main():
 files=sorted(p for p in (ROOT/NAME).iterdir() if p.is_file() and p.suffix.lower() in ['.def','.cns','.cmd','.air','.sff','.snd','.md'])
 subprocess.run([sys.executable,str(ROOT/'tools/validate_boruto.py')],check=True)
 out=ROOT/(NAME+'.zip')
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in files:
   info=zipfile.ZipInfo(NAME+'/'+p.name,date_time=(2026,10,27,12,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
 with tempfile.TemporaryDirectory(prefix='boruto-package-') as tmp:
  with zipfile.ZipFile(out) as z:assert z.testzip() is None;z.extractall(tmp)
  subprocess.run([sys.executable,str(ROOT/'tools/validate_boruto.py'),str(Path(tmp)/NAME)],check=True)
  for p in files:assert p.read_bytes()==(Path(tmp)/NAME/p.name).read_bytes()
 proof=dict(archive=out.name,bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),ultimate_own_life_cost=0,files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
 (ROOT/'previews/BorutoKarmaJogan_package_checks.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items() if k!='files'}))
if __name__=='__main__':main()
