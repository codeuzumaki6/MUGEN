#!/usr/bin/env python3
"""Record six specials with actual SDL mixer output, not reconstructed audio."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,resample_poly
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews';engine=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
LONG=os.environ.get('POCHITA_SPECIAL_VERSION')=='long'
SCENARIOS=[('derecha_x','Desgarro','ABAJO > ADELANTE + X'),('izquierda_x','Cuatro brazos','ABAJO > ATRAS + X'),('derecha_y','Estocada','ABAJO > ADELANTE + Y'),('izquierda_y','Barrido','ABAJO > ATRAS + Y'),('derecha_b','Embestida','ABAJO > ADELANTE + B'),('izquierda_b','Carniceria','ABAJO > ATRAS + B')]
with wave.open(str(ROOT/'PochitaTrueForm/assets/sound/special_activation.wav'),'rb') as stream:
 assert stream.getframerate()==22050;cue=resample_poly(np.frombuffer(stream.readframes(stream.getnframes()),dtype='<i2').astype(float)/32768,2,1)
reports=[];evidence=[];clips=[]
with tempfile.TemporaryDirectory(prefix='pochita-special-video-') as temp:
 folder=Path(temp)
 for index,(label,name,caption) in enumerate(SCENARIOS):
  capture=folder/label;capture.mkdir();raw=capture/'engine_audio.raw';env=os.environ.copy();env.update(POCHITA_RECORD_AUDIO=str(raw),POCHITA_CAPTURE=str(capture),POCHITA_CAPTURE_CASES=json.dumps([name]),POCHITA_PREVIEW_SET='long' if LONG else 'special')
  run=subprocess.run([sys.executable,str(ROOT/'tools/check_pochita_in_engine.py'),engine],env=env,capture_output=True,text=True);assert run.returncode==0,run.stdout+run.stderr
  reports+=json.loads((OUT/('Pochita_long_visual_checks.json' if LONG else 'Pochita_special_visual_checks.json')).read_text())
  frames=[tuple(map(int,line.split())) for line in (capture/'frames.tsv').read_text().splitlines()];events=[tuple(map(int,line.split())) for line in (capture/'audio.tsv').read_text().splitlines()]
  activation=[tick for tick,number in events if number==10];assert len(activation)==1,(name,events)
  assert len(frames)>=35 and all(b[1]>a[1] for a,b in zip(frames,frames[1:]))
  # SDLSpeaker uses stereo AUDIO_S16SYS at 44100 Hz in this engine config.
  stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
  cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)];norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));score=np.abs(cross)/np.maximum(norm,1e-12);peak=int(np.argmax(score));confidence=float(score[peak]);assert confidence>.25,(name,confidence)
  start=peak/44100-(activation[0]-frames[0][1])/60;assert start>=0
  duration=(frames[-1][1]+4-frames[0][1])/60;first=round(start*44100);last=first+round(duration*44100);assert last<=len(stereo)
  audio=stereo[first:last];assert np.max(abs(audio))>.05
  actual=capture/'actual_engine_audio.wav'
  with wave.open(str(actual),'wb') as wav:wav.setnchannels(2);wav.setsampwidth(2);wav.setframerate(44100);wav.writeframes(np.clip(audio*32768,-32768,32767).astype('<i2').tobytes())
  lines=['ffconcat version 1.0']
  for position,(frame,tick) in enumerate(frames):
   image=capture/f'Ikemen_GO{frame:03d}.png';assert image.is_file();delta=(frames[position+1][1]-tick) if position+1<len(frames) else 4
   lines += [f"file '{image}'",'option framerate 60',f'duration {delta/60:.9f}']
  lines += [f"file '{image}'",'option framerate 60'];listing=capture/'frames.txt';listing.write_text('\n'.join(lines)+'\n')
  text=capture/'caption.txt';text.write_text(caption+'   |   Pochita - especiales')
  clip=OUT/f'Pochita_{"largo_" if LONG else ""}especial_{label}_motor.mp4';clips.append(clip)
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-i',str(actual),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=textfile={text}:x=(w-tw)/2:y=689:fontsize=23:fontcolor=white','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(clip)],check=True)
  if index==0:
   subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(clip),'-filter_complex','[0:v]fps=15,scale=640:-1:flags=neighbor,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(OUT/('Pochita_especiales_largos_motor.gif' if LONG else 'Pochita_especial_activacion_motor.gif'))],check=True)
   import shutil
   picture=min(frames,key=lambda p:abs(p[1]-(activation[0]+4)));shutil.copy2(capture/f'Ikemen_GO{picture[0]:03d}.png',OUT/('Pochita_especiales_largos_motor.png' if LONG else 'Pochita_especial_activacion_motor.png'))
  if LONG and index==5:
   import shutil
   last_hit=max(tick for tick,number in events if number==5);picture=min(frames,key=lambda p:abs(p[1]-(last_hit+2)));shutil.copy2(capture/f'Ikemen_GO{picture[0]:03d}.png',OUT/'Pochita_carniceria_larga_motor.png')
  evidence.append(dict(case=name,frames=len(frames),activation_tick=activation[0],audio_source='Actual SDL disk driver output, AUDIO_S16SYS stereo 44100 Hz; no offline mix',audio_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),activation_match_seconds=peak/44100,activation_correlation=confidence,alignment_start_seconds=start,duration=duration,peak=float(np.max(abs(audio))),rms=float(np.sqrt(np.mean(audio*audio)))))
  print(name,len(frames),'captured frames; actual audio activation match',round(confidence,3),flush=True)
 listing=folder/'clips.txt';listing.write_text(''.join(f"file '{p}'\n" for p in clips))
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUT/('Pochita_ESPECIALES_LARGOS_Y_EFECTOS.mp4' if LONG else 'Pochita_ESPECIALES_CON_SONIDO.mp4'))],check=True)
(OUT/('Pochita_long_visual_checks.json' if LONG else 'Pochita_special_visual_checks.json')).write_text(json.dumps(reports,indent=2)+'\n');(OUT/('Pochita_long_audio_checks.json' if LONG else 'Pochita_actual_audio_checks.json')).write_text(json.dumps(evidence,indent=2)+'\n')
print('Recorded all six specials with actual engine audio')

if LONG:subprocess.run([sys.executable,str(ROOT/'tools/make_pochita_special_comparison.py')],check=True)
