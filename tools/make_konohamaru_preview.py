#!/usr/bin/env python3
"""Record every base technique, Enra mode and the massive Rasengan finisher."""
import re
from make_boruto_tbv_preview import ROOT,source
def main():
 capture=source.replace('BorutoTBVBase','KonohamaruTBV').replace('BORUTOTBV_','KONOHAMARU_').replace('check_boruto_tbv_in_engine.py','check_konohamaru_in_engine.py')
 capture=capture.replace('Original Boruto pack startup sample','Original Konohamaru pack startup sample')
 voices={'Rasengan':'rasen','Katon':'garyuEndan','Enra':'summon','Giro':'Attack03_01','Ascendente':'Attack02_01','Extension':'Attack03_01','Barrido':'Attack02_01','Clones':'summon','Fuin':'Fuin','Kunai':'Attack02_01','Shouheki':'Attack02_01','Martillo':'Attack03_01','Cuchillas':'S05','ultimate':'Haaaa','awakening':'summon'}
 capture=re.sub(r'(?m)^ voices=.*$', ' voices='+repr({k:'Khm/'+v for k,v in voices.items()}),capture)
 labels={'Rasengan':'Rasengan: avance e impacto','Katon':'Katon: Garyu Endan','Enra':'Enra: invocacion y baston','Giro':'Enra: giro y rueda de fuego','Ascendente':'Corte ascendente','Extension':'Baston extensible','Barrido':'Barrido bajo','Clones':'Dos clones de Rasengan','Fuin':'Sellado triangular','Kunai':'Kunai arrojado','Shouheki':'Rasengan: barrera','Martillo':'Enra: martillo y explosion','Cuchillas':'Combo de cuchillas de chakra','ultimate':'Rasengan masivo con clones','awakening':'Despertar: baston Enra'}
 before,rest=capture.split('display=',1);_,after=rest.split(';label=folder',1);capture=before+'display='+repr(labels)+"[rec['name']];label=folder"+after
 capture=capture.replace('CONCENTRACION UZUHIKO','BASTON ENRA').replace('Concentracion Uzuhiko','Baston Enra').replace('Boruto | TBV base','Konohamaru | TBV')
 capture=capture.replace("rec['name']=='Espiral'","rec['name']=='ultimate'").replace('KonohamaruTBV_uzuhiko_motor.mp4','KonohamaruTBV_ultimate_motor.mp4').replace("report['uzuhiko_excerpt']","report['ultimate_excerpt']")
 exec(compile(capture,str(ROOT/'tools/make_boruto_preview.py'),'exec'),dict(__file__=str(ROOT/'tools/make_boruto_preview.py'),__name__='__main__'))
if __name__=='__main__':main()
