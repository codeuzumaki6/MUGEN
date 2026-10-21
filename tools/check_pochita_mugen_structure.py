#!/usr/bin/env python3
"""Regress the MUGEN crash: reject controllerless states across CNS and CMD."""
from pathlib import Path
import json,re,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'PochitaTrueForm'
validator=ROOT/'tools/validate_pochita.py'
results=[]
def validate(folder):return subprocess.run([sys.executable,str(validator),str(folder)],capture_output=True,text=True)
valid=validate(CHAR);assert valid.returncode==0,valid.stdout+valid.stderr
results.append(dict(case='delivered character',passed=True))
with tempfile.TemporaryDirectory(prefix='pochita-mugen-structure-') as temp:
 copy=Path(temp)/'PochitaTrueForm';copy.mkdir()
 for path in CHAR.iterdir():
  if path.is_file():shutil.copy2(path,copy/path.name)
 for name,state in [('PochitaTrueForm.cns',170),('PochitaTrueForm.cns',175),('PochitaTrueForm.cns',180),('common1.cns',0),('PochitaTrueForm.cmd',-1)]:
  path=copy/name;original=path.read_text();pattern=rf'(?ims)(^\[Statedef {state}\]\s*\n)(.*?)(?=^\[Statedef |\Z)';match=re.search(pattern,original);assert match,(name,state)
  # Leave the state declaration and parameters; remove all its controllers.
  header=re.split(r'(?im)^\[State\s+',match[2],maxsplit=1)[0]
  path.write_text(original[:match.start()]+match[1]+header+original[match.end():])
  run=validate(copy);expected=f'Statedef {state} needs at least one state controller'
  assert run.returncode!=0 and expected in run.stdout,(name,state,run.stdout,run.stderr)
  path.write_text(original);results.append(dict(case=f'empty {name} state {state}',rejected=True,passed=True))
 path=copy/'PochitaTrueForm.cmd';original=path.read_text();assert 'trigger10 = StateNo' in original
 path.write_text(original.replace('trigger10 = StateNo','trigger30 = StateNo',1))
 run=validate(copy);assert run.returncode!=0 and 'nonconsecutive trigger groups' in run.stdout,run.stdout
 path.write_text(original);results.append(dict(case='gap before special cancel trigger group',rejected=True,passed=True))
 path=copy/'PochitaTrueForm.cns';original=path.read_text();assert 'flag = RoundNotOver' in original
 path.write_text(original.replace('flag = RoundNotOver','flag = WinPose',1))
 run=validate(copy);assert run.returncode!=0 and 'invalid MUGEN AssertSpecial flag WinPose' in run.stdout,run.stdout
 path.write_text(original);results.append(dict(case='unsupported victory assertion',rejected=True,passed=True))
(ROOT/'previews/Pochita_mugen_structure_checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(f'PASS: valid character and {len(results)-1} MUGEN structure regression fixtures')
