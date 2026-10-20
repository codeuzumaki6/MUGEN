#!/usr/bin/env python3
"""Verify deterministic native archives/runtime and visible scarf/blade bounds."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'PochitaTrueForm';names=['PochitaTrueForm'+x for x in ['.sff','.snd','.air','.cns','.cmd','.def']]+['common1.cns']
def hashes():return {n:hashlib.sha256((CHAR/n).read_bytes()).hexdigest() for n in names}
def build():
 for script,args in [('build_pochita_redesign.py',[]),('build_pochita_sound.py',['--from-wav']),('build_pochita_runtime.py',[])]:subprocess.run([sys.executable,str(ROOT/'tools'/script),*args],check=True,stdout=subprocess.DEVNULL)
build();first=hashes();build();second=hashes();assert first==second,(first,second)
with tempfile.TemporaryDirectory(prefix='pochita-bound-regression-') as folder:
 copy=Path(folder)/'PochitaTrueForm';copy.mkdir()
 for p in CHAR.iterdir():
  if p.is_file():shutil.copy2(p,copy/p.name)
 p=copy/'PochitaTrueForm.air';s=p.read_text();start=s.index('[Begin Action 1200]');prefix=s[:start];tail=s[start:];tail,n=re.subn(r'(Clsn1\[0\] = 12,-66,)\d+',r'\g<1>999',tail,count=1);assert n;p.write_text(prefix+tail)
 run=subprocess.run([sys.executable,str(ROOT/'tools/validate_pochita.py'),str(copy)],capture_output=True,text=True);assert run.returncode!=0 and 'beyond the rendered weapon' in run.stdout,run.stdout+run.stderr
report=dict(deterministic=True,files=second,oversized_scarf_collision_rejected=True)
(ROOT/'previews/Pochita_validator_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS deterministic SFF/SND/AIR/CNS/CMD/DEF/common rebuild and oversized scarf regression')
