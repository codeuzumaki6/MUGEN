"""Exact imported sprite keys allowed for each form in native fixtures."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def lua_body_keys(character):
    records=json.loads((ROOT/character/'assets/senki/manifest.json').read_text())
    if character=='MatsuriShinju':records=[r for r in records if r['key'].startswith(('Hashirama_Nattack_','Hashirama_Skill'))]
    if character=='MitsukiTBV':records=[r for r in records if r['key'].startswith('SageGaara_')]
    keys=','.join("['%s:%s']=true"%(r['group'],r['number']) for r in records)
    return 'local SENKI_BODY={'+keys+'}\n'
