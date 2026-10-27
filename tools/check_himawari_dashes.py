#!/usr/bin/env python3
"""Actual double/single taps in both directions, for Himawari in both forms."""
from pathlib import Path
import fcntl,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from check_roster_dashes import ENGINE

def main():
 lock=open(ENGINE/'.native-character-check.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
 source=(ROOT/'tools/check_roster_dashes.py').read_text().split("if __name__=='__main__':")[0]
 # Use the same centred screen-bound fixture for both forms.
 source=source.replace('-60 if side==1 else 160','0 if side==1 else 140')
 source=source.replace("if side==1:p1+=b","b+=controller('ScreenBound','1','value=1\\nmovecamera=0,0')\n            if side==1:p1+=b")
 result=[]
 for mode in [0,1]:
  text=source.replace("if side==1:p1+=b",f"if side==1:p1+=b+controller('VarSet',at(2),'v=42\\nvalue={mode}')+controller('VarSet',at(2),'v=40\\nvalue=900')")
  scope={'__file__':str(ROOT/'tools/check_roster_dashes.py'),'__name__':'himawari_dash_probe'};exec(compile(text,str(ROOT/'tools/check_roster_dashes.py'),'exec'),scope)
  rows=scope['run']('HimawariTBV');assert all(r['passed'] for r in rows)
  result.extend(dict(form=mode,**r) for r in rows)
 (ROOT/'previews/HimawariTBV_dash_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: 16 dash checks, Himawari and Kurama')
if __name__=='__main__':main()
