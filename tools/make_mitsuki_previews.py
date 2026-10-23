#!/usr/bin/env python3
"""Actual engine frames and SDL audio; no offline effects or body animation."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
labels=['NORMAL | Raiton: abajo, adelante + Y','NORMAL | Fuuton: abajo, atras + Y','NORMAL | Asalto giratorio: RT','DESPERTAR | Abajo + Pausa / LB','MODO SABIO | Combo Y, Y, Y','MODO SABIO | Serpientes: abajo, atras + X','MODO SABIO | Tres corrientes Fuuton','MODO SABIO | Ulti: A, requiere acertar']
def main():
 with tempfile.TemporaryDirectory(prefix='mitsuki-native-') as tmp:
  folder=Path(tmp);raw=folder/'audio.raw';env=os.environ.copy();env.update(MITSUKI_CAPTURE=str(folder),MITSUKI_AUDIO=str(raw),MITSUKI_DEMO='1',MITSUKI_TICKS='360')
  subprocess.run([sys.executable,str(ROOT/'tools/check_mitsuki_in_engine.py')],env=env,check=True)
  rows=[tuple(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()];cues=[tuple(map(int,l.split())) for l in (folder/'cues.tsv').read_text().splitlines()]
  with wave.open(str(ROOT/'MitsukiTBV/assets/sound/1_21.wav')) as f:cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)
  stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
  cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)];norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));scores=np.abs(cross)/np.maximum(norm,1e-12);peaks,_=find_peaks(scores,height=max(.25,float(scores.max())*.65),distance=round(.5*44100));assert len(peaks)>=7,(scores.max(),len(peaks))
  # One measured anchor for the continuous SDL recording. Keep all pauses
  # in the capture timestamps; validate subsequent activations against it.
  anchor=int(peaks[0]);offset=anchor/44100-cues[0][0]/60;assert offset>=0
  expected=[t/60+offset for t,n in cues if n%10000 in [1000,1010,1020,1030,1210,3000] or n==520]
  errors=[min(abs(peaks/44100-t)) for t in expected];assert max(errors)<.25,('Audio and native capture clocks diverged',errors)
  lines=['ffconcat version 1.0'];audio=[];duration=0;shots=[]
  for case,label in enumerate(labels):
   frames=[r for r in rows if r[2]==case];assert len(frames)>35
   start=round((frames[0][1]/60+offset)*44100);end=round(((frames[-1][1]+4)/60+offset)*44100);assert end<=len(stereo)
   audio.append(stereo[start:end]);duration+=(end-start)/44100
   text=folder/f'label{case}.txt';text.write_text(label)
   chosen=[]
   for j,(idx,t,_,tick) in enumerate(frames):
    original=folder/f'Ikemen_GO{idx:03d}.png';im=Image.open(original).convert('RGB');d=ImageDraw.Draw(im);d.rectangle((0,680,1280,720),fill=(9,15,24));d.text((25,691),label,fill=(205,255,235),font_size=19);decorated=folder/f'frame_{idx:04d}.png';im.save(decorated)
    delta=frames[j+1][1]-t if j+1<len(frames) else 4;lines += [f"file '{decorated}'",'option framerate 60',f'duration {delta/60:.9f}']
    if 40<=tick<=105:chosen.append((tick,decorated))
   target={0:65,1:65,2:65,3:90,4:75,5:60,6:75,7:145}[case]
   shot=min(frames,key=lambda r:abs(r[3]-target));shots.append(folder/f'frame_{shot[0]:04d}.png')
  lines += [f"file '{decorated}'",'option framerate 60'];concat=folder/'frames.txt';concat.write_text('\n'.join(lines)+'\n');wav=folder/'actual.wav'
  samples=np.concatenate(audio)
  with wave.open(str(wav),'wb') as f:f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(samples*32768,-32768,32767).astype('<i2').tobytes())
  video=OUT/'MitsukiTBV_gameplay_motor.mp4'
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-i',str(wav),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
  board=Image.new('RGB',(1280,4*360))
  for i,p in enumerate(shots):board.paste(Image.open(p).resize((640,360)),(i%2*640,i//2*360))
  board.save(OUT/'MitsukiTBV_gameplay_muestras.jpg');shutil.copy2(shots[3],OUT/'MitsukiTBV_despertar_motor.png')
  checks=json.loads((OUT/'MitsukiTBV_capture_checks.json').read_text());result=dict(runtime_sha256=checks['runtime_sha256'],video=str(video.relative_to(ROOT)),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),audio='Actual SDL stereo 44100Hz, trimmed per showcase scene; no offline voices or effects',audio_correlation=float(scores[anchor]),audio_anchor_errors_seconds=[float(e) for e in errors],duration=duration,frames=len(rows),scenes=labels,failures=[])
  (OUT/'MitsukiTBV_demo_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS native video',round(duration,2),'seconds; audio correlation',round(result['audio_correlation'],3))
if __name__=='__main__':main()
