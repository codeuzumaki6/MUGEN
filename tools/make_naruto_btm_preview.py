#!/usr/bin/env python3
"""Record the corrected Rasengan techniques and reduced-damage finishers."""
import re
from make_boruto_tbv_preview import ROOT,source
from build_naruto_btm_runtime import VOICES
def main():
 capture=source.replace('BorutoTBVBase','NarutoBTM').replace('BORUTOTBV_','NARUTOBTM_').replace('check_boruto_tbv_in_engine.py','check_naruto_btm_in_engine.py')
 capture=capture.replace("NARUTOBTM_DEMO='showcase'","NARUTOBTM_DEMO='rasengan_fix'")
 capture=capture.replace('Original Boruto pack startup sample','Original Naruto BTM pack startup sample')
 voices=VOICES
 capture=re.sub(r'(?m)^ voices=.*$', ' voices='+repr({k:'BTM/'+v for k,v in voices.items()}),capture)
 labels={'Rasengan': 'Rasengan: avance e impacto', 'Muro': 'Doton: muro de tierra', 'Rasenshuriken': 'Rasenshuriken: vuelo y explosion', 'Combo': 'Combo de chakra', 'Ascendente': 'Patada ascendente', 'Caida': 'Asalto descendente', 'Barrido': 'Barrido bajo', 'Clones': 'Dos clones de sombra', 'Impacto': 'Rasengan de impacto', 'Onda': 'Rasengan arrojado', 'Disco': 'Disco Rasenshuriken rapido', 'RasenCampo': 'Campo Rasenshuriken', 'Bijudama': 'Kurama: Bijudama', 'ultimate': 'Ulti: asalto Rasengan y Kurama', 'awakening': 'Despertar: chakra de Kurama'}
 before,rest=capture.split('display=',1);_,after=rest.split(';label=folder',1);capture=before+'display='+repr(labels)+"[rec['name']];label=folder"+after
 capture=capture.replace('CONCENTRACION UZUHIKO','CHAKRA DE KURAMA').replace('Concentracion Uzuhiko','Chakra de Kurama').replace('Boruto | TBV base','Naruto | BTM')
 capture=capture.replace("rec['name']=='Espiral'","rec['name']=='ultimate'").replace('NarutoBTM_uzuhiko_motor.mp4','NarutoBTM_ultimate_motor.mp4').replace("report['uzuhiko_excerpt']","report['ultimate_excerpt']")
 exec(compile(capture,str(ROOT/'tools/make_boruto_preview.py'),'exec'),dict(__file__=str(ROOT/'tools/make_boruto_preview.py'),__name__='__main__'))
if __name__=='__main__':main()
