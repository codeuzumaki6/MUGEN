#!/usr/bin/env python3
"""Actual Rasengan, lightning and projectiles against a half-scale opponent."""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 env=os.environ.copy();env.update(BORUTO_TARGET_SCALE='.5',BORUTO_CASES='["Rasengan","Shiden","Disparo","Futon","ultimate"]',BORUTO_REPORT='BorutoKarmaJogan_short_target_checks.json')
 subprocess.run([sys.executable,str(ROOT/'tools/check_boruto_in_engine.py')],cwd=ROOT,env=env,check=True)
 data=json.loads((ROOT/'previews/BorutoKarmaJogan_short_target_checks.json').read_text());assert len(data['cases'])==20 and all(c['damage']>0 and not c['failures'] for c in data['cases']);print('PASS: 20 half-scale target cases')
