#!/usr/bin/env python3
"""Full techniques against a short, half-scale fighter."""
import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 env=os.environ.copy();env.update(NARUTOKCM_TARGET_SCALE='.5',NARUTOKCM_CASES=json.dumps(['Rasengan','Brazo','Rueda','Destello','Palma','Odama','Kurama','ultimate']),NARUTOKCM_REPORT='NarutoKCM_short_target_checks.json')
 subprocess.run([sys.executable,str(ROOT/'tools/check_naruto_kcm_in_engine.py')],cwd=ROOT,env=env,check=True)
 result=json.loads((ROOT/'previews/NarutoKCM_short_target_checks.json').read_text());assert len(result['cases'])==32 and all(c['damage']>0 and not c['failures'] for c in result['cases']);print('PASS: 32 half-scale target cases')
if __name__=='__main__':main()
