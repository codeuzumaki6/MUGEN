#!/usr/bin/env python3
"""Record the charge feet and the clone's full lifetime, with actual SDL audio."""
import re
from make_boruto_tbv_preview import ROOT,source

def main():
 capture=source.replace("prefix='BorutoTBVBase';", "prefix='BorutoTBVBase_carga_clon';")
 capture=capture.replace("BORUTOTBV_DEMO='showcase'", "BORUTOTBV_CASES='[\"Bunshin\",\"charge\"]',BORUTOTBV_FORM='0',BORUTOTBV_LONG_CAPTURE='1'")
 capture=capture.replace('activations={1000,','activations={500,1000,')
 capture=re.sub(r'(?m)^ voices=.*$', " voices={'Bunshin':'BorutoTBv/03','charge':'Effect/RsgAura'}",capture)
 capture=capture.replace("'BorutoTBVBase_motor.mp4'", "'BorutoTBVBase_carga_clon_motor.mp4'")
 capture=capture.replace("else rec['name'];label=", "else 'Abajo + Y: clon autonomo de ocho segundos' if rec['name']=='Bunshin' else 'Carga de chakra: pies en el suelo' if rec['name']=='charge' else rec['name'];label=")
 # This recording has two regression cases, without an Uzuhiko excerpt.
 capture=capture[:capture.index(' # A short excerpt')]+" (OUT/(prefix+'_preview_checks.json')).write_text(json.dumps(report,indent=2)+'\\n');print(json.dumps(report))\nif __name__=='__main__':main()\n"
 exec(compile(capture,str(ROOT/'tools/make_boruto_preview.py'),'exec'),dict(__file__=str(ROOT/'tools/make_boruto_preview.py'),__name__='__main__'))

if __name__=='__main__':main()
