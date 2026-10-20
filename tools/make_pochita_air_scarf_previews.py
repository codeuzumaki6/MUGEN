#!/usr/bin/env python3
"""Capture real airborne routes and intestinal-scarf attacks with actual SDL audio."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,resample_poly
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews';engine=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
scenarios=[('aire_triturado','Air XYY',True,240,7,'motor_grind_finish.wav','SALTO > X Y Y | Cortes aereos y triturado final, sin coste'),('aire_descendente','Air XYB',True,240,8,'cross_saw_cut.wav','SALTO > X Y B | Remate aereo descendente'),('bufanda_lazo','Lazo RB followup',True,240,10,'special_activation.wav','ABAJO + RB > X | Lazo intestinal, tambaleo y continuacion'),('bufanda_remate','Agarre RT hit',True,240,10,'special_activation.wav','ABAJO + RT | Sujecion intestinal y tres cortes, 600 energia')]
reports=[];evidence=[];clips=[]
with tempfile.TemporaryDirectory(prefix='pochita-air-scarf-preview-') as temp:
 folder=Path(temp)
 for label,name,extension,ticks,sound,sample,caption in scenarios:
  capture=folder/label;capture.mkdir();raw=capture/'engine_audio.raw';env=os.environ.copy()
  env.update(POCHITA_RECORD_AUDIO=str(raw),POCHITA_CAPTURE=str(capture),POCHITA_CAPTURE_CASES=json.dumps([name]),POCHITA_PREVIEW_SET='air_scarf',POCHITA_TICKS=str(ticks))
  if extension:env['POCHITA_AIR_SCARF_CHECK']='1'
  else:env.pop('POCHITA_AIR_SCARF_CHECK',None)
  run=subprocess.run([sys.executable,str(ROOT/'tools/check_pochita_in_engine.py'),engine],env=env,capture_output=True,text=True);assert run.returncode==0,run.stdout+run.stderr
  reports+=json.loads((OUT/'Pochita_air_scarf_visual_checks.json').read_text())
  frames=[tuple(map(int,line.split())) for line in (capture/'frames.tsv').read_text().splitlines()];events=[tuple(map(int,line.split())) for line in (capture/'audio.tsv').read_text().splitlines()]
  activation=[t for t,n in events if n==sound];assert len(activation)==1,(name,events)
  with wave.open(str(ROOT/'PochitaTrueForm/assets/sound'/sample),'rb') as f:
   assert f.getframerate()==22050;cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)
  stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
  cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)];norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue))
  score=np.abs(cross)/np.maximum(norm,1e-12);peak=int(np.argmax(score));confidence=float(score[peak]);assert confidence>.25,(name,confidence)
  start=peak/44100-(activation[0]-frames[0][1])/60;assert start>=0
  duration=(frames[-1][1]+4-frames[0][1])/60;first=round(start*44100);last=first+round(duration*44100);assert last<=len(stereo)
  actual=capture/'audio.wav';audio=stereo[first:last]
  with wave.open(str(actual),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(44100);f.writeframes(np.clip(audio*32768,-32768,32767).astype('<i2').tobytes())
  lines=['ffconcat version 1.0']
  for i,(frame,tick) in enumerate(frames):
   path=capture/f'Ikemen_GO{frame:03d}.png';assert path.is_file();delta=frames[i+1][1]-tick if i+1<len(frames) else 4
   lines += [f"file '{path}'",'option framerate 60',f'duration {delta/60:.9f}']
  lines += [f"file '{path}'",'option framerate 60'];listing=capture/'frames.txt';listing.write_text('\n'.join(lines)+'\n')
  text=capture/'caption.txt';text.write_text(caption);clip=OUT/f'Pochita_{label}_nuevo_motor.mp4';clips.append(clip)
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-i',str(actual),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=expansion=none:textfile={text}:x=(w-tw)/2:y=689:fontsize=21:fontcolor=white','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(clip)],check=True)
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(clip),'-filter_complex','[0:v]fps=15,scale=640:-1:flags=neighbor,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(OUT/f'Pochita_{label}_nuevo_motor.gif')],check=True)
  image=min(frames,key=lambda pair:abs(pair[1]-(activation[0]+18)));shutil.copy2(capture/f'Ikemen_GO{image[0]:03d}.png',OUT/f'Pochita_{label}_nuevo_motor.png')
  evidence.append(dict(case=name,frames=len(frames),cue=sound,activation_tick=activation[0],activation_correlation=confidence,duration=duration,audio_source='Actual SDL disk driver output, stereo S16LE 44100 Hz, no offline mix',raw_audio_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),alignment_start_seconds=start))
  print(name,len(frames),'frames; actual engine audio correlation',round(confidence,3),flush=True)
 listing=folder/'clips.txt';listing.write_text(''.join(f"file '{p}'\n" for p in clips))
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUT/'Pochita_AEREOS_Y_BUFANDA.mp4')],check=True)
(OUT/'Pochita_air_scarf_visual_checks.json').write_text(json.dumps(reports,indent=2)+'\n');(OUT/'Pochita_air_scarf_audio_checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Captured two airborne routes and two intestinal-scarf skills with actual engine audio')
