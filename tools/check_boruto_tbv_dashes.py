#!/usr/bin/env python3
"""Apply the shared regression fixture to TBV base."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/"tools"/'check_boruto_dashes.py').read_text().replace("BorutoKarmaJogan","BorutoTBVBase").replace("BORUTO_","BORUTOTBV_").replace("check_boruto_in_engine.py","check_boruto_tbv_in_engine.py")
exec(compile(source,str(ROOT/"tools"/'check_boruto_dashes.py'),"exec"),dict(__file__=str(ROOT/"tools"/'check_boruto_dashes.py'),__name__="__main__"))
