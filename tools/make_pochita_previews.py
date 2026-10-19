#!/usr/bin/env python3
"""Capture real engine frames; MP4 sound is mixed from logged game events."""
from pathlib import Path
import json, os, subprocess, sys, tempfile, wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
engine=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
reports=[]; manifest=[]
sounds=json.loads((ROOT/'PochitaTrueForm/assets/sound/provenance.json').read_text())
for label,case in [('combo_x','Combo X'),('combo_y','Combo Y'),('combo_b','Combo B'),('ultimate','ultihit')]:
 with tempfile.TemporaryDirectory(prefix='pochita-preview-') as directory:
  folder=Path(directory);env=os.environ.copy();env['POCHITA_CAPTURE']=directory;env['POCHITA_CAPTURE_CASES']=json.dumps([case])
  run=subprocess.run([sys.executable,str(ROOT/'tools/check_pochita_in_engine.py'),engine],env=env,capture_output=True,text=True)
  assert run.returncode==0,run.stdout+run.stderr
  reports+=json.loads((ROOT/'previews/Pochita_engine_visual_checks.json').read_text())
  frames=[tuple(map(int,line.split())) for line in (folder/'frames.tsv').read_text().splitlines()]
  cues=[tuple(map(int,line.split())) for line in (folder/'audio.tsv').read_text().splitlines()]
  assert len(frames)>=35,(case,len(frames))
  assert all(b[1]>a[1] for a,b in zip(frames,frames[1:]))
  concat=['ffconcat version 1.0']
  for pos,(index,tick) in enumerate(frames):
   png=folder/f'Ikemen_GO{index:03d}.png';assert png.is_file()
   duration=((frames[pos+1][1]-tick) if pos+1<len(frames) else 4)/60
   concat += [f"file '{png}'",'option framerate 60',f'duration {duration:.9f}']
  concat += [f"file '{png}'",'option framerate 60']
  (folder/'frames.txt').write_text('\n'.join(concat)+'\n')
  duration=(frames[-1][1]+4-frames[0][1])/60
  mix=np.zeros(int((duration+2)*22050),dtype=np.float64)
  for tick,number in cues:
   start=round((tick-frames[0][1])*22050/60)
   with wave.open(str(ROOT/'PochitaTrueForm/assets/sound'/sounds[number]['filename']),'rb') as wav:
    assert wav.getframerate()==22050 and wav.getnchannels()==1 and wav.getsampwidth()==2
    samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(np.float64)/32768
   if start<0:samples=samples[-start:];start=0
   count=min(len(samples),len(mix)-start)
   if count>0:mix[start:start+count]+=samples[:count]*.65
  mix=mix[:round(duration*22050)];peak=np.max(np.abs(mix));mix/=max(1,peak/.95)
  with wave.open(str(folder/'audio.wav'),'wb') as wav:
   wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(22050);wav.writeframes((mix*32767).astype('<i2').tobytes())
  target=ROOT/'previews'/f'Pochita_remates_{label}_motor'
  base=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(folder/'frames.txt')]
  subprocess.run(base+['-filter_complex','[0:v]fps=15,scale=640:-1:flags=neighbor,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(target.with_suffix('.gif'))],check=True)
  subprocess.run(base+['-i',str(folder/'audio.wav'),'-vf','fps=30','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-t',str(duration),'-movflags','+faststart',str(target.with_suffix('.mp4'))],check=True)
  if label=='ultimate':
   import shutil
   peakframe=min(frames,key=lambda entry:abs(entry[1]-110))
   shutil.copy2(folder/f'Ikemen_GO{peakframe[0]:03d}.png',ROOT/'previews/Pochita_remates_ultimate_motor.png')
  manifest.append(dict(case=case,frames=frames,cues=cues,duration=duration,audio='Offline mix of character WAV samples using engine event timestamps; not device audio capture.'))
  print(label,len(frames),'real engine captures',round(duration,3),'seconds',flush=True)
(ROOT/'previews/Pochita_engine_visual_checks.json').write_text(json.dumps(reports,indent=2)+'\n')
(ROOT/'previews/Pochita_preview_timing.json').write_text(json.dumps(manifest,indent=2)+'\n')
