#!/usr/bin/env python3
"""Independent indexed MUGEN 1.1 contract for Naruto BTM."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/validate_boruto.py').read_text().replace('BorutoKarmaJogan','NarutoBTM').replace('list(range(32000,32008))','[30000]').replace('==663','==160').replace('PainNol','UnusedZeroCell').replace('Boruto Karma Jogan:','Naruto BTM:')
source=source.replace('from boruto_source import read_sff','from boruto_tbv_sff import read_sff').replace("'9700' in header and field(body,'value')=='120'","any(str(n) in header for n in [9700,9701]) and field(body,'value')=='120'")
exec(compile(source,str(ROOT/'tools/validate_boruto.py'),'exec'),dict(__file__=str(ROOT/'tools/validate_boruto.py'),__name__='__main__'))
