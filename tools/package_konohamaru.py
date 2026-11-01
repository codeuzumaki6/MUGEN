#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/package_boruto.py').read_text().replace('BorutoKarmaJogan','KonohamaruTBV').replace('validate_boruto.py','validate_konohamaru.py')
exec(compile(source,str(ROOT/'tools/package_boruto.py'),'exec'),dict(__file__=str(ROOT/'tools/package_boruto.py'),__name__='__main__'))
