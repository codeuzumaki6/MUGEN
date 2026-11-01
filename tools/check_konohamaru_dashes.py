#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/check_boruto_dashes.py').read_text().replace('BorutoKarmaJogan','KonohamaruTBV').replace('Boruto in both forms','Konohamaru in both modes')
exec(compile(source,str(ROOT/'tools/check_boruto_dashes.py'),'exec'),dict(__file__=str(ROOT/'tools/check_boruto_dashes.py'),__name__='__main__'))
