#!/usr/bin/env python3
"""Record all 26 specials with native frames, collisions and actual SDL audio."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,wave
from contextlib import nullcontext
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly
from PIL import Image
from build_mitsuki_runtime import MOVES
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
TITLES={1000:'Asalto de brazos',1010:'Abanico de serpientes',1020:'Lanza Raiton',1030:'Fuuton Toppa',1040:'Patada creciente',1050:'Cerco de serpientes',1400:'Deslizamiento bajo',1410:'Golpe ascendente',1420:'Atadura de serpientes',1200:'Serpiente rapida',1210:'Asalto giratorio',1430:'Rayo Raiton sostenido',1440:'Sustitucion y contraataque'}
BUTTONS={'a':'X','b':'Y','c':'B','y':'RB','z':'RT'}
TIMES={1000:53,1010:53,1020:53,1030:51,1040:47,1050:62,1400:42,1410:43,1420:63,1200:39,1210:51,1430:60,1440:54}
def main():
 labels=[]
 for form in [0,1]:
  for name,b,d,n,cost in MOVES:
   motion={'F':'abajo, adelante + ','B':'abajo, atras + ','D':'abajo + ','N':''}[d]+BUTTONS[b]
   labels.append(('NORMAL' if not form else 'SABIO')+' | '+motion+' | '+('Senpo: Orochi Ikazuchi' if form and n==1020 else TITLES[n]))
 with nullcontext(os.environ.get('MITSUKI_REUSE_CAPTURE') or tempfile.mkdtemp(prefix='mitsuki-specials-')) as tmp:
  folder=Path(tmp);raw=folder/'audio.raw';env=os.environ.copy();env.update(MITSUKI_CAPTURE=str(folder),MITSUKI_AUDIO=str(raw),MITSUKI_ALL_SPECIALS='1',MITSUKI_TICKS='210');env.pop('MITSUKI_DEMO',None)
  if not os.environ.get('MITSUKI_REUSE_CAPTURE'):
   subprocess.run([sys.executable,str(ROOT/'tools/check_mitsuki_in_engine.py')],env=env,check=True)
   shutil.copy2(OUT/'MitsukiTBV_capture_checks.json',folder/'checks.json')
  else:shutil.copy2(folder/'checks.json',OUT/'MitsukiTBV_capture_checks.json')
  rows=[tuple(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()];cues=[tuple(map(int,l.split())) for l in (folder/'cues.tsv').read_text().splitlines()]
  with wave.open(str(ROOT/'MitsukiTBV/assets/sound/1_21.wav')) as f:cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)
  stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
  cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)];norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));scores=np.abs(cross)/np.maximum(norm,1e-12);peaks,_=find_peaks(scores,height=.24,distance=round(.5*44100));assert len(peaks)>=26,(scores.max(),len(peaks))
  anchor=int(peaks[0]);offset=anchor/44100-cues[0][0]/60;assert offset>=0
  startercues=[(t,n) for t,n in cues if n%10000 in [m[3] for m in MOVES]];assert len(startercues)==26,len(startercues)
  offsets=[];errors=[];confidences=[];previous=-1
  for t,n in startercues:
   expected=t/60+offset;choices=[int(p) for p in peaks if p>previous]
   peak=min(choices,key=lambda p:abs(p/44100-expected));drift=peak/44100-expected
   assert abs(drift)<.8,('Missing real activation cue',n,drift)
   offsets.append(peak/44100-t/60);errors.append(float(drift));confidences.append(float(scores[peak]));previous=peak
  lines=['ffconcat version 1.0'];audio=[];duration=0;shots=[];scene_ranges=[];subtitles=['[Script Info]','ScriptType: v4.00+','PlayResX: 1280','PlayResY: 720','','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Default,DejaVu Sans,19,&H00E9FFD0,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,16,16,9,1','','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
  def stamp(seconds):
   cs=round(seconds*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
  for case,label in enumerate(labels):
   frames=[r for r in rows if r[2]==case];assert len(frames)>=25
   start=round((frames[0][1]/60+offsets[case])*44100);end=round(((frames[-1][1]+6)/60+offsets[case])*44100);assert end<=len(stereo)
   audio.append(stereo[start:end]);begin=duration;duration+=(end-start)/44100
   scene_ranges.append(dict(index=case,start=begin,end=duration,label=label))
   subtitles.append(f'Dialogue: 0,{stamp(begin)},{stamp(duration)},Default,,0,0,0,,{label}')
   for j,(idx,t,_,tick) in enumerate(frames):
    original=folder/f'Ikemen_GO{idx:03d}.png';assert original.exists()
    delta=frames[j+1][1]-t if j+1<len(frames) else 6;lines += [f"file '{original}'",'option framerate 60',f'duration {delta/60:.9f}']
   target=51 if case==15 else TIMES[MOVES[case%13][3]];shot=min(frames,key=lambda r:abs(r[3]-target));shots.append(folder/f'Ikemen_GO{shot[0]:03d}.png')
  lines += [f"file '{original}'",'option framerate 60'];concat=folder/'frames.txt';concat.write_text('\n'.join(lines)+'\n');ass=folder/'labels.ass';ass.write_text('\n'.join(subtitles)+'\n');wav=folder/'actual.wav';samples=np.concatenate(audio)
  with wave.open(str(wav),'wb') as f:f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(samples*32768,-32768,32767).astype('<i2').tobytes())
  video=OUT/'MitsukiTBV_gameplay_motor.mp4'
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-i',str(wav),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=0x090f18:t=fill,subtitles={ass}','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
  board=Image.new('RGB',(1280,7*180))
  for i,p in enumerate(shots):board.paste(Image.open(p).resize((320,180)),(i%4*320,i//4*180))
  board.save(OUT/'MitsukiTBV_gameplay_muestras.jpg')
  # Inspectable full-size evidence for the specific user-reported bugs.
  for case,name in [(2,'Raiton_lanza'),(11,'Raiton_rayo'),(12,'Sustitucion'),(4,'Patada'),(6,'Barrido'),(7,'Lanzador'),(15,'Orochi_Ikazuchi')]:Image.open(shots[case]).save(OUT/f'MitsukiTBV_{name}_motor.png')
  orochi=scene_ranges[15];clip=OUT/'MitsukiTBV_Orochi_Ikazuchi_motor.mp4'
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(orochi['start']),'-i',str(video),'-t',str(orochi['end']-orochi['start']),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(clip)],check=True)
  checks=json.loads((OUT/'MitsukiTBV_capture_checks.json').read_text());result=dict(runtime_sha256=checks['runtime_sha256'],video=str(video.relative_to(ROOT)),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),orochi_clip=str(clip.relative_to(ROOT)),orochi_clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),audio='Actual SDL stereo 44100Hz, trimmed per special; no offline voices or effects',audio_correlation=float(scores[anchor]),audio_global_clock_drift_seconds=errors,audio_per_scene_offsets=offsets,audio_per_scene_confidence=confidences,audio_sync='Each independent demonstration aligned to its measured engine activation cue',duration=duration,frames=len(rows),scenes=labels,scene_ranges=scene_ranges,specials_per_form=13,all_specials_shown=True,failures=[])
  (OUT/'MitsukiTBV_demo_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS all 26 specials, native video',round(duration,2),'seconds; audio correlation',round(result['audio_correlation'],3));shutil.rmtree(folder)
if __name__=='__main__':main()
