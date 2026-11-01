#!/usr/bin/env python3
"""Actual controls, costs, collisions and recovery in both NarutoBTM modes."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/check_boruto_in_engine.py').read_text().replace('from build_boruto_runtime import MOVES','from build_naruto_btm_runtime import MOVES').replace('BorutoKarmaJogan','NarutoBTM').replace('BorutoCheck','NarutoBTMCheck').replace('BorutoDummy','NarutoBTMDummy').replace('BORUTO_','NARUTOBTM_').replace('boruto_trace','naruto_btm_trace').replace('boruto_checks','naruto_btm_checks')
source=source.replace("names=['Rasengan','Shiden','Kenjutsu','Espiral','Caida','Disparo','Futon','ultimate']", "names=[m[0] for m in MOVES]+['ultimate']")
source=source.replace("['Rasengan','Espiral','Caida','Disparo','Invocacion','Futon','ultimate']", "['Rasengan','Rasenshuriken','Clones','RasenCampo','Bijudama','ultimate']")
source=source.replace('timeout=300','timeout=420')
if os.environ.get('NARUTOBTM_CLONE_TRACE'):
 source=source.replace('age=var(5)','age=time()')
if os.environ.get('NARUTOBTM_DEMO')=='showcase':
 # Keep every technique and the complete finishers below the engine's
 # 999-screenshot limit; the fight itself still runs every native tick.
 source=source.replace('tick<=CAPEND','tick<=CAPEND and (tick<=260 or case==13 or case==20)')
exec(compile(source,str(ROOT/'tools/check_boruto_in_engine.py'),'exec'),dict(__file__=str(ROOT/'tools/check_boruto_in_engine.py'),__name__='__main__'))
