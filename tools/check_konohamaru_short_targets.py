#!/usr/bin/env python3
"""Full techniques against a short, half-scale fighter."""
import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 env=os.environ.copy();env.update(KONOHAMARU_TARGET_SCALE='.5',KONOHAMARU_CASES=json.dumps(['Rasengan','Katon','Clones','Fuin','Shouheki','ultimate']),KONOHAMARU_REPORT='KonohamaruTBV_short_target_checks.json')
 subprocess.run([sys.executable,str(ROOT/'tools/check_konohamaru_in_engine.py')],cwd=ROOT,env=env,check=True)
 result=json.loads((ROOT/'previews/KonohamaruTBV_short_target_checks.json').read_text());assert len(result['cases'])==24 and all(c['damage']>0 and not c['failures'] for c in result['cases']);print('PASS: 24 half-scale target cases')
if __name__=='__main__':main()
