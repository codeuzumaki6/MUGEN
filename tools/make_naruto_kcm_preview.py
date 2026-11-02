#!/usr/bin/env python3
"""Record original KCM and Baryon techniques with actual engine audio."""
import re
from make_boruto_tbv_preview import ROOT,source
from build_naruto_kcm_runtime import VOICES
def main():
 capture=source.replace('BorutoTBVBase','NarutoKCM').replace('BORUTOTBV_','NARUTOKCM_').replace('check_boruto_tbv_in_engine.py','check_naruto_kcm_in_engine.py')
 capture=capture.replace("NARUTOKCM_DEMO='showcase'","NARUTOKCM_DEMO='compact'")
 capture=capture.replace('Original Boruto pack startup sample','Original Naruto KCM pack startup sample')
 voices=VOICES
 capture=re.sub(r'(?m)^ voices=.*$', ' voices='+repr({k:'BTM/'+v for k,v in voices.items()}),capture)
 capture=capture.replace("name='Shared/startup' if case==ids[0] else voices[rec['name']]","name='Shared/startup' if case==ids[0] else 'BTM/NarutoBaryon' if rec['form'] and rec['name'] in ['ultimate','Kurama'] else 'BTM/NAttack02' if rec['form'] else voices[rec['name']]")
 labels={'Rasengan': 'Rasengan KCM', 'Brazo': 'Brazos de chakra', 'Combo': 'Combo de chakra', 'Rueda': 'Brazos giratorios y explosion', 'Ascendente': 'Patada ascendente', 'Descenso': 'Ataque descendente', 'Barrido': 'Barrido bajo', 'Destello': 'Paso veloz', 'Palma': 'Golpe de chakra', 'Puno': 'Puno de chakra extensible', 'RasenCorto': 'Rasengan corto', 'Odama': 'Odama Rasengan aereo', 'Kurama': 'Kurama: asalto del avatar', 'ultimate': 'Ulti: avatar de Kurama', 'awakening': 'Despertar: modo Barion'}
 baryon={'Rasengan': 'Asalto Barion', 'Brazo': 'Contra de palma', 'Combo': 'Rafaga Barion', 'Rueda': 'Giro ascendente', 'Ascendente': 'Gancho Barion', 'Descenso': 'Descenso Barion', 'Barrido': 'Embestida baja', 'Destello': 'Destello Barion', 'Palma': 'Palma de ruptura', 'Puno': 'Palma rapida', 'RasenCorto': 'Paso y golpe Barion', 'Odama': 'Gancho de ruptura', 'Kurama': 'Combo completo Barion', 'ultimate': 'Ulti: remate Barion', 'awakening': 'Modo Barion'}
 before,rest=capture.split('display=',1);_,after=rest.split(';label=folder',1);capture=before+'display='+repr(baryon)+"[rec['name']] if rec['form'] else "+repr(labels)+"[rec['name']];label=folder"+after
 capture=capture.replace('CONCENTRACION UZUHIKO','MODO BARION').replace('Concentracion Uzuhiko','Modo Barion').replace('Boruto | TBV base','Naruto | KCM / Barion')
 capture=capture.replace("rec['name']=='Espiral'","rec['name']=='ultimate'").replace('NarutoKCM_uzuhiko_motor.mp4','NarutoKCM_ultimate_motor.mp4').replace("report['uzuhiko_excerpt']","report['ultimate_excerpt']")
 exec(compile(capture,str(ROOT/'tools/make_boruto_preview.py'),'exec'),dict(__file__=str(ROOT/'tools/make_boruto_preview.py'),__name__='__main__'))
if __name__=='__main__':main()
