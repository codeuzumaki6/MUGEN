#!/usr/bin/env python3
"""Apply the standalone MUGEN contract to the separate TBV base archive."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/validate_boruto.py').read_text().replace('BorutoKarmaJogan','BorutoTBVBase').replace('list(range(32000,32008))','[31000]').replace('==663','==161').replace('PainNol','Hiruzen_Nol').replace('Boruto Karma Jogan:','Boruto TBV base:')
source=source.replace('from boruto_source import read_sff','from boruto_tbv_sff import read_sff')
exec(compile(source,str(ROOT/'tools/validate_boruto.py'),'exec'),dict(__file__=str(ROOT/'tools/validate_boruto.py'),__name__='__main__'))
