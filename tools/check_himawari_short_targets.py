#!/usr/bin/env python3
"""Actual attacks against a half-scale opponent, in both forms and facings."""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 env=os.environ.copy();env.update(HIMAWARI_TARGET_SCALE='.5',HIMAWARI_CASES='["Patada","Tenketsu","Vacio","Bijudama","ultimate"]',HIMAWARI_REPORT='HimawariTBV_short_target_checks.json')
 subprocess.run([sys.executable,str(ROOT/'tools/check_himawari_in_engine.py')],cwd=ROOT,env=env,check=True)
 data=json.loads((ROOT/'previews/HimawariTBV_short_target_checks.json').read_text());assert len(data['cases'])==20 and all(c['damage']>0 and not c['failures'] for c in data['cases'])
 print('PASS: 20 half-scale target cases')
