#!/usr/bin/env python3
"""Actual controls, costs, collisions and recovery in both NarutoKCM modes."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/check_boruto_in_engine.py').read_text().replace('from build_boruto_runtime import MOVES','from build_naruto_kcm_runtime import MOVES').replace('BorutoKarmaJogan','NarutoKCM').replace('BorutoCheck','NarutoKCMCheck').replace('BorutoDummy','NarutoKCMDummy').replace('BORUTO_','NARUTOKCM_').replace('boruto_trace','naruto_kcm_trace').replace('boruto_checks','naruto_kcm_checks')
source=source.replace("names=['Rasengan','Shiden','Kenjutsu','Espiral','Caida','Disparo','Futon','ultimate']", "names=[m[0] for m in MOVES]+['ultimate']")
source=source.replace("['Rasengan','Espiral','Caida','Disparo','Invocacion','Futon','ultimate']", "['Rasengan','Brazo','Combo','Ascendente','Kurama','ultimate']")
source=source.replace('timeout=300','timeout=420').replace('(800 if form else 650)','(360 if form else 300)')
if os.environ.get('NARUTOKCM_CLONE_TRACE'):
 source=source.replace('age=var(5)','age=time()')
if os.environ.get('NARUTOKCM_DEMO')=='compact':
 source=source.replace("=='showcase'","in ('showcase','compact')").replace("names=[m[0] for m in MOVES]+['ultimate']","names=['Rasengan','Brazo','Rueda','Odama','Kurama','ultimate']").replace("['Rasengan','Brazo','Combo','Ascendente','Kurama','ultimate']","['Rasengan','Combo','Ascendente','Kurama','ultimate']")
if os.environ.get('NARUTOKCM_DEMO') in ['showcase','compact']:
 # Keep every technique and the complete finishers below the engine's
 # 999-screenshot limit; the fight itself still runs every native tick.
 endpoints='5 or case==11' if os.environ.get('NARUTOKCM_DEMO')=='compact' else '13 or case==20'
 source=source.replace('tick<=CAPEND','tick<=CAPEND and (tick<=260 or case=='+endpoints+')')
if os.environ.get('NARUTOKCM_DEMO')=='effects':
 source=source.replace('assert cases',"cases=[c for c in cases if c['face']==1 and ((c['form']==0 and c['name'] in ['Rasengan','Rueda','Odama','Kurama','awakening']) or (c['form']==1 and c['name']=='ultimate'))]\nassert cases")
exec(compile(source,str(ROOT/'tools/check_boruto_in_engine.py'),'exec'),dict(__file__=str(ROOT/'tools/check_boruto_in_engine.py'),__name__='__main__'))
