#!/usr/bin/env python3
"""Run the shared real-input fixture against the separate TBV base character."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/check_boruto_in_engine.py').read_text().replace('from build_boruto_runtime import MOVES','from build_boruto_tbv_runtime import MOVES').replace('BorutoKarmaJogan','BorutoTBVBase').replace('BorutoCheck','BorutoTBVCheck').replace('BorutoDummy','BorutoTBVDummy').replace('BORUTO_','BORUTOTBV_').replace('boruto_trace','boruto_tbv_trace').replace('boruto_checks','boruto_tbv_checks')
exec(compile(source,str(ROOT/'tools/check_boruto_in_engine.py'),'exec'),dict(__file__=str(ROOT/'tools/check_boruto_in_engine.py'),__name__='__main__'))
