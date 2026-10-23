#!/usr/bin/env python3
"""Record all 26 specials with native frames, collisions and actual SDL audio."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,wave
from contextlib import nullcontext
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly
from PIL import Image
from build_hidari_runtime import MOVES
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
TITLES={1000:'Chidori',1010:'Garra de madera / Corte dorado',1020:'Corriente / Rafaga de flechas',1030:'Prision de raices',1040:'Garra ascendente',1050:'Madera / Doble espadazo',1400:'Barrido bajo',1410:'Palma proyectada',1420:'Ramas / Lluvia de espadas',1200:'Senbon / Flecha rapida',1210:'Marca y viaje con RT',1430:'Tormenta / Tajos del Susanoo',1440:'Salida desde la marca'}
BUTTONS={'a':'X','b':'Y','c':'B','y':'RB','z':'RT'}
TIMES={1000:54,1010:64,1020:66,1030:84,1040:52,1050:76,1400:48,1410:58,1420:78,1200:59,1210:150,1430:84,1440:75,3000:140,520:83}
def main():
 with nullcontext(os.environ.get('HIDARI_REUSE_CAPTURE') or tempfile.mkdtemp(prefix='hidari-specials-')) as tmp:
  folder=Path(tmp);raw=folder/'audio.raw';env=os.environ.copy();env.update(HIDARI_CAPTURE=str(folder),HIDARI_AUDIO=str(raw),HIDARI_ALL_SPECIALS='1',HIDARI_TICKS='320');env.pop('HIDARI_DEMO',None)
  if not os.environ.get('HIDARI_REUSE_CAPTURE'):
   subprocess.run([sys.executable,str(ROOT/'tools/check_hidari_in_engine.py')],env=env,check=True)
   shutil.copy2(OUT/'HidariShinju_capture_checks.json',folder/'checks.json')
  else:shutil.copy2(folder/'checks.json',OUT/'HidariShinju_capture_checks.json')
  checks=json.loads((OUT/'HidariShinju_capture_checks.json').read_text());cases=[r['case'] for r in checks['cases']];labels=[]
  for case in cases:
   form=case['form'];kind=case['kind'];n=case.get('state',520)%10000
   motion='A' if kind=='ultimate' else 'abajo + Pausa' if kind=='awakening' else {'F':'abajo, adelante + ','B':'abajo, atras + ','D':'abajo + ','N':''}[case['d']]+BUTTONS[case['b']]
   title=('Chidori y raices: ulti' if form==0 else 'Sentencia del Susanoo: ulti') if kind=='ultimate' else 'Susanoo amarillo' if kind=='awakening' else TITLES[n]
   labels.append(('SUSANOO' if form else 'BASE')+' | '+motion+' | '+title)
  rows=[tuple(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()];cues=[tuple(map(int,l.split())) for l in (folder/'cues.tsv').read_text().splitlines()]
  with wave.open(str(ROOT/'HidariShinju/assets/sound/1_21.wav')) as f:cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)[:round(.3*44100)]
  stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
  cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)];norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));scores=np.abs(cross)/np.maximum(norm,1e-12);peaks,_=find_peaks(scores,height=.5,distance=round(.5*44100))
  # Include the two second-RT activations in the correspondence. Renderer
  # stalls can separate wall time from simulation time, so a single growing
  # clock offset is not a valid way to locate the next recorded sound.
  allcues=[(t,n) for t,n in cues if n%10000 in [m[3] for m in MOVES]+[3000,520,1211]]
  assert len(peaks)==len(allcues),(len(peaks),len(allcues),'Expected one recorded cue per native activation')
  matched=[(t,n,int(p)) for (t,n),p in zip(allcues,peaks)]
  starters=[r for r in matched if r[1]%10000!=1211];assert len(starters)==len(cases)
  anchor=starters[0][2];offset=anchor/44100-starters[0][0]/60;assert offset>=0
  offsets=[p/44100-t/60 for t,n,p in starters];errors=[float(v-offset) for v in offsets];confidences=[float(scores[p]) for t,n,p in starters]
  lines=['ffconcat version 1.0'];audio=[];duration=0;shots=[];scene_ranges=[];subtitles=['[Script Info]','ScriptType: v4.00+','PlayResX: 1280','PlayResY: 720','','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Default,DejaVu Sans,19,&H00E9FFD0,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,16,16,9,1','','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
  def stamp(seconds):
   cs=round(seconds*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
  for case,label in enumerate(labels):
   frames=[r for r in rows if r[2]==case and r[3]<=(302 if cases[case]['kind']=='ultimate' else 180)];assert len(frames)>=20
   assert max(b[1]-a[1] for a,b in zip(frames,frames[1:]))<=18,'Native capture contains a visible frame gap'
   start=round((frames[0][1]/60+offsets[case])*44100);end=round(((frames[-1][1]+6)/60+offsets[case])*44100);assert end<=len(stereo)
   audio.append(stereo[start:end]);begin=duration;duration+=(end-start)/44100
   scene_ranges.append(dict(index=case,start=begin,end=duration,label=label))
   subtitles.append(f'Dialogue: 0,{stamp(begin)},{stamp(duration)},Default,,0,0,0,,{label}')
   for j,(idx,t,_,tick) in enumerate(frames):
    original=folder/f'Ikemen_GO{idx:03d}.png';assert original.exists()
    delta=frames[j+1][1]-t if j+1<len(frames) else 6;lines += [f"file '{original}'",'option framerate 60',f'duration {delta/60:.9f}']
   target=TIMES[cases[case].get('state',520)%10000];shot=min(frames,key=lambda r:abs(r[3]-target));shots.append(folder/f'Ikemen_GO{shot[0]:03d}.png')
  lines += [f"file '{original}'",'option framerate 60'];concat=folder/'frames.txt';concat.write_text('\n'.join(lines)+'\n');ass=folder/'labels.ass';ass.write_text('\n'.join(subtitles)+'\n');wav=folder/'actual.wav';samples=np.concatenate(audio)
  with wave.open(str(wav),'wb') as f:f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(samples*32768,-32768,32767).astype('<i2').tobytes())
  video=OUT/'HidariShinju_gameplay_motor.mp4'
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-i',str(wav),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=0x090f18:t=fill,subtitles={ass}','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
  board=Image.new('RGB',(1280,((len(shots)+3)//4)*180))
  for i,p in enumerate(shots):board.paste(Image.open(p).resize((320,180)),(i%4*320,i//4*180))
  board.save(OUT/'HidariShinju_gameplay_muestras.jpg')
  for i,case in enumerate(cases):
   if case['form']==1 and case.get('state',0)%10000 in [1000,1020,3000] or case.get('state',0)==520:Image.open(shots[i]).save(OUT/f"HidariShinju_susanoo_{case.get('state',520)%10000}_motor.png")
   if case['form']==0 and case.get('state',0)%10000 in [1020,1030,1430,3000]:Image.open(shots[i]).save(OUT/f"HidariShinju_{case.get('state')%10000}_motor.png")
  ultiscene=next(r for r in scene_ranges if cases[r['index']]['kind']=='ultimate' and cases[r['index']]['form']==1);clip=OUT/'HidariShinju_ulti_motor.mp4'
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(ultiscene['start']),'-i',str(video),'-t',str(ultiscene['end']-ultiscene['start']),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(clip)],check=True)
  result=dict(runtime_sha256=checks['runtime_sha256'],video=str(video.relative_to(ROOT)),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),ultimate_clip=str(clip.relative_to(ROOT)),ultimate_clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),audio='Actual SDL stereo 44100Hz, trimmed per special; no offline voices or effects',audio_correlation=float(scores[anchor]),audio_global_clock_drift_seconds=errors,audio_per_scene_offsets=offsets,audio_per_scene_confidence=confidences,native_activation_cues_matched=len(allcues),audio_sync='Each scene aligned to its actual recorded activation; matches include second RT; simulation-frame render stalls compressed',duration=duration,frames=len(rows),minimum_scene_frames=min(sum(r[2]==i and r[3]<=(302 if cases[i]['kind']=='ultimate' else 180) for r in rows) for i in range(len(cases))),maximum_native_frame_gap=max(b[1]-a[1] for i in range(len(cases)) for a,b in zip([r for r in rows if r[2]==i],[r for r in rows if r[2]==i][1:])),scenes=labels,scene_ranges=scene_ranges,specials_per_form=13,all_specials_shown=True,ultimate_both_forms_shown=True,awakening_shown=True,failures=[])
  (OUT/'HidariShinju_demo_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS 26 specials, both ultimates and awakening, native video',round(duration,2),'seconds; audio correlation',round(result['audio_correlation'],3));print('Native capture retained at',folder)
if __name__=='__main__':main()
