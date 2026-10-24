#!/usr/bin/env python3
"""Record both Matsuri forms in separate native sessions with denser frames."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly
from PIL import Image
from build_matsuri_runtime import MOVES
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
TITLES={1000:'Lanza de Shinju',1010:'Latigo del manto',1020:'Suiton: rafaga de agua',1030:'Jardin de raices y aura',1040:'Ataque ascendente',1050:'Atadura del manto',1400:'Barrido deslizante',1410:'Lanzador',1420:'Floracion del manto',1200:'Bala de agua grande',1210:'Marca de garra y viaje',1430:'Erupcion de madera',1440:'Emboscada del arbol'}
BUTTONS={'a':'X','b':'Y','c':'B','y':'RB','z':'RT'}
SHOTS={1000:66,1010:64,1020:80,1030:72,1040:52,1050:70,1400:48,1410:60,1420:70,1200:62,1210:132,1430:75,1440:65,3000:114,520:68}
def stamp(t):
 cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
def main():
 folder=Path(os.environ.get('MATSURI_REUSE_CAPTURE') or tempfile.mkdtemp(prefix='matsuri-final-'));combined=[];parts=[]
 for form in [0,1]:
  part=folder/f'form-{form}';part.mkdir(parents=True,exist_ok=True);report=OUT/f'MatsuriShinju_capture_{form}_checks.json'
  if not os.environ.get('MATSURI_REUSE_CAPTURE'):
   env=os.environ.copy();env.update(MATSURI_CAPTURE=str(part),MATSURI_AUDIO=str(part/'audio.raw'),MATSURI_ALL_SPECIALS='1',MATSURI_FORM=str(form),MATSURI_TICKS='320',MATSURI_REPORT=report.name)
   with (part/'engine.log').open('w') as log:
    run=subprocess.run([sys.executable,str(ROOT/'tools/check_matsuri_in_engine.py')],env=env,stdout=log,stderr=subprocess.STDOUT)
   if run.returncode:print((part/'engine.log').read_text()[-10000:]);raise RuntimeError('Matsuri native preview failed')
   shutil.copy2(report,part/'checks.json')
  checks=json.loads((part/'checks.json').read_text());assert all(not r['failures'] for r in checks['cases'])
  parts.append((part,checks));combined+=checks['cases'];print('Captured native Matsuri form',form,'scenes',len(checks['cases']),part,flush=True)
 assert len(combined)==29 and parts[0][1]['runtime_sha256']==parts[1][1]['runtime_sha256']
 runtime=parts[0][1]['runtime_sha256'];(OUT/'MatsuriShinju_capture_checks.json').write_text(json.dumps(dict(runtime_sha256=runtime,sessions=2,cases=combined),indent=2)+'\n')
 with wave.open(str(ROOT/'MatsuriShinju/assets/sound/1_21.wav')) as f:sample=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)[:13230]
 lines=['ffconcat version 1.0'];audio=[];duration=0;scenes=[];shots=[];confidences=[];native_cues=0
 ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 1280','PlayResY: 720','','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Default,DejaVu Sans,19,&H00F6C7FF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,16,16,9,1','','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
 for part,checks in parts:
  cases=[r['case'] for r in checks['cases']];rows=[tuple(map(int,l.split())) for l in (part/'frames.tsv').read_text().splitlines()];cues=[tuple(map(int,l.split())) for l in (part/'cues.tsv').read_text().splitlines()]
  stereo=np.frombuffer((part/'audio.raw').read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(1)
  cross=correlate(mono,sample,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)];den=np.sqrt(np.maximum(0,energy[len(sample):]-energy[:-len(sample)])*np.sum(sample*sample));scores=np.abs(cross)/np.maximum(den,1e-12)
  peaks,_=find_peaks(scores,height=.5,distance=22050);events=[r for r in cues if r[1]%10000 in [m[3] for m in MOVES]+[3000,520,1211]]
  assert len(peaks)==len(events),(len(peaks),len(events));native_cues+=len(events)
  starts=[(clock,n,int(peak)) for (clock,n),peak in zip(events,peaks) if n%10000!=1211];assert len(starts)==len(cases)
  for i,case in enumerate(cases):
   form=case['form'];kind=case['kind'];n=case['state']%10000
   motion='A' if kind=='ultimate' else 'abajo + Pausa' if kind=='awakening' else {'F':'abajo, adelante + ','B':'abajo, atras + ','D':'abajo + ','N':''}[case['d']]+BUTTONS[case['b']]
   title='Caceria del Arbol Divino' if kind=='ultimate' else 'Despertar sin capa' if kind=='awakening' else TITLES[n];label=('DESPERTAR' if form else 'BASE')+' | '+motion+' | '+title
   fs=[r for r in rows if r[2]==i and r[3]<=(302 if kind=='ultimate' else 180)];assert len(fs)>=18 and fs[0][3]<35 and fs[-1][3]>(260 if kind=='ultimate' else 155),(label,len(fs))
   clock,state,peak=starts[i];offset=peak/44100-clock/60;start=round((fs[0][1]/60+offset)*44100);end=round(((fs[-1][1]+4)/60+offset)*44100);assert 0<=start<end<=len(stereo)
   audio.append(stereo[start:end]);begin=duration;duration+=(end-start)/44100;confidences.append(float(scores[peak]));scenes.append(dict(start=begin,end=duration,label=label,case=case));ass.append(f'Dialogue: 0,{stamp(begin)},{stamp(duration)},Default,,0,0,0,,{label}')
   for j,(idx,frame,scene,tick) in enumerate(fs):
    picture=part/f'Ikemen_GO{idx:03d}.png';assert picture.exists();delta=fs[j+1][1]-frame if j+1<len(fs) else 4;lines += [f"file '{picture}'",'option framerate 60',f'duration {delta/60:.9f}']
   shot=min(fs,key=lambda r:abs(r[3]-SHOTS[n]));path=part/f'Ikemen_GO{shot[0]:03d}.png';shots.append(path)
   if n in [1020,1030,1430,3000,520]:shutil.copy2(path,OUT/f'MatsuriShinju_{form}_{n}_motor.png')
 assert native_cues==31
 lines += [f"file '{picture}'",'option framerate 60'];(folder/'frames.txt').write_text('\n'.join(lines)+'\n');(folder/'labels.ass').write_text('\n'.join(ass)+'\n')
 with wave.open(str(folder/'actual.wav'),'wb') as f:f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(np.concatenate(audio)*32768,-32768,32767).astype('<i2').tobytes())
 video=OUT/'MatsuriShinju_gameplay_motor.mp4';subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(folder/'frames.txt'),'-i',str(folder/'actual.wav'),'-vf',f"fps=30,drawbox=x=0:y=680:w=1280:h=40:color=0x090f18:t=fill,subtitles={folder/'labels.ass'}",'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
 board=Image.new('RGB',(1280,((len(shots)+3)//4)*180))
 for i,path in enumerate(shots):board.paste(Image.open(path).resize((320,180)),(i%4*320,i//4*180))
 board.save(OUT/'MatsuriShinju_gameplay_muestras.jpg');scene=next(s for s in scenes if s['case']['kind']=='ultimate' and s['case']['form']==0);clip=OUT/'MatsuriShinju_ulti_motor.mp4'
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(scene['start']),'-i',str(video),'-t',str(scene['end']-scene['start']),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(clip)],check=True)
 result=dict(runtime_sha256=runtime,video=str(video.relative_to(ROOT)),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),ultimate_clip=str(clip.relative_to(ROOT)),ultimate_clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),duration=duration,scenes=[s['label'] for s in scenes],scene_ranges=scenes,audio='Actual SDL stereo 44100Hz, aligned per native activation; rendering stalls compressed',audio_per_scene_confidence=confidences,native_activation_cues_matched=native_cues,specials_per_form=13,all_specials_shown=True,ultimate_both_forms_shown=True,awakening_shown=True,native_capture_sessions=2,failures=[])
 (OUT/'MatsuriShinju_demo_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS all Matsuri specials and awakening',round(duration,2),'seconds;',folder)
if __name__=='__main__':main()
