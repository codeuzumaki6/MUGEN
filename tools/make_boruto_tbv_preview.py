#!/usr/bin/env python3
"""Record the TBV base character with its actual engine audio."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/make_boruto_preview.py').read_text().replace('BorutoKarmaJogan','BorutoTBVBase').replace('BORUTO_','BORUTOTBV_').replace('check_boruto_in_engine.py','check_boruto_tbv_in_engine.py')
voices={'Rasengan':'01','Shiden':'02','Kenjutsu':'01','Espiral':'005','Ascendente':'01','Combo':'02','Barrido':'01','Bunshin':'03','Caida':'04','Kunai':'01','Disparo':'01','Invocacion':'04','Futon':'03','ultimate':'005','awakening':'005'}
source=re.sub(r'(?m)^ voices=.*$', ' voices='+repr({k:'BorutoTBv/'+v for k,v in voices.items()}),source)
source=source.replace("name='BorutoJogan/05' if rec['name']=='Invocacion' and rec['form'] else voices[rec['name']]","name=voices[rec['name']]")
# The intro uses the same voice as the first Rasengan. Anchor that first
# activation to its actual startup effect so the intro cannot win the match.
source=source.replace("entries=[];selected=[];scores={};voicenames={}","entries=[];selected=[];scores={};voicenames={};soundmap['Shared/startup']=[1,21]")
source=source.replace("name=voices[rec['name']]", "name='Shared/startup' if case==ids[0] else voices[rec['name']]")
source=source.replace("anchor='Original Boruto pack startup sample'", "anchor='Shared startup effect' if voicenames[case]=='Shared/startup' else 'Original Boruto pack startup sample'")
# Large original effects can stall software screenshot readback while SDL
# keeps recording wall time. Measure that drift instead of assuming 60 fps.
source=source.replace('prediction-2*44100','prediction-8*44100').replace('prediction+2*44100','prediction+8*44100')
# FFT roundoff divided by a near-zero denominator can create false peaks
# inside exact silence. Require measurable captured audio for every anchor.
source=source.replace("candidates,_=find_peaks(local", "local=np.where((energy[len(cue):]-energy[:-len(cue)])>len(cue)*1e-6,local,0);candidates,_=find_peaks(local")
source=source.replace("'Mokuton' if rec['name']=='Invocacion' and rec['form']","'Hiraishin' if rec['name']=='Invocacion'").replace('Rasengan doble gigante','Hiraishin: golpe aereo').replace('Futon Rasengan verde','Hiraishin: Rasengan descendente').replace('RT: dos Rasengan azules','RT: Rasengan').replace('KARMA / JOGAN','CONCENTRACION UZUHIKO').replace('Resonancia Karma / Jogan','Concentracion Uzuhiko').replace('Karma y Jogan','TBV base')
exec(compile(source,str(ROOT/'tools/make_boruto_preview.py'),'exec'),dict(__file__=str(ROOT/'tools/make_boruto_preview.py'),__name__='__main__'))
