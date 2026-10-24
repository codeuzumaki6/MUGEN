#!/usr/bin/env python3
"""Capture Hidari's RB Gokakyu with original Sasuke fire and audio."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'

def main():
 folder=Path(os.environ.get('HIDARI_REUSE_KATON_CAPTURE') or tempfile.mkdtemp(prefix='hidari-base-katon-'))
 if not os.environ.get('HIDARI_REUSE_KATON_CAPTURE'):
  env=os.environ.copy();env.update(HIDARI_CAPTURE=str(folder),HIDARI_AUDIO=str(folder/'audio.raw'),HIDARI_RANGE='1',HIDARI_CASES='["Senbon"]',HIDARI_FACE='1',HIDARI_OUTCOMES='["hit","guard","jump","interrupt"]',HIDARI_DISTANCES='[45,60,210]',HIDARI_TICKS='220',HIDARI_REPORT='HidariShinju_katon_capture_checks.json')
  subprocess.run(['python',str(ROOT/'tools/check_hidari_in_engine.py')],env=env,check=True)
  shutil.copy2(OUT/'HidariShinju_katon_capture_checks.json',folder/'checks.json')
 checks=json.loads((folder/'checks.json').read_text());cases=[r['case'] for r in checks['cases']]
 assert len(cases)==5 and all(not r['failures'] for r in checks['cases'])
 rows=[tuple(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()]
 cues=[tuple(map(int,l.split())) for l in (folder/'cues.tsv').read_text().splitlines() if int(l.split()[1])==1200]
 stereo=np.frombuffer((folder/'audio.raw').read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(1)
 with wave.open(str(ROOT/'HidariShinju/assets/sound/1_21.wav')) as f:
  rate=f.getframerate();sample=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768
 from fractions import Fraction
 ratio=Fraction(44100,rate);sample=resample_poly(sample,ratio.numerator,ratio.denominator)[:13230]
 cross=correlate(mono,sample,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)]
 den=np.sqrt(np.maximum(0,energy[len(sample):]-energy[:-len(sample)])*np.sum(sample*sample));scores=np.abs(cross)/np.maximum(den,1e-12)
 peaks,_=find_peaks(scores,height=.5,distance=22050);assert len(cues)==len(peaks)==5,(len(cues),len(peaks))
 lines=['ffconcat version 1.0'];audio=[];duration=0;scenes=[];shots=[]
 ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 1280','PlayResY: 720','','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Default,DejaVu Sans,21,&H00FFFFBB,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,16,16,9,1','','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
 def stamp(t):
  cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
 for i,case in enumerate(cases):
  title={'hit':'Impacto cercano' if case['distance']==60 else 'Bola de fuego a distancia','guard':'El rival bloquea','jump':'El rival salta por encima','interrupt':'Carga interrumpida'}[case['outcome']]
  label='HIDARI BASE | RB | Katon: Gokakyu | '+title
  fs=[r for r in rows if r[2]==i and r[3]<=180];assert len(fs)>20
  offset=peaks[i]/44100-cues[i][0]/60;start=round((fs[0][1]/60+offset)*44100);end=round(((fs[-1][1]+6)/60+offset)*44100);assert 0<=start<end<=len(stereo)
  audio.append(stereo[start:end]);begin=duration;duration+=(end-start)/44100
  scenes.append(dict(label=label,start=begin,end=duration,case=case));ass.append(f'Dialogue: 0,{stamp(begin)},{stamp(duration)},Default,,0,0,0,,{label}')
  for j,(idx,clock,scene,tick) in enumerate(fs):
   picture=folder/f'Ikemen_GO{idx:03d}.png';assert picture.exists();delta=fs[j+1][1]-clock if j+1<len(fs) else 6
   lines += [f"file '{picture}'",'option framerate 60',f'duration {delta/60:.9f}']
  target=checks['cases'][i]['first_contact_tick']+15 if case['outcome']=='hit' else 70
  shot=min(fs,key=lambda r:abs(r[3]-target));shots.append(folder/f'Ikemen_GO{shot[0]:03d}.png')
 lines += [f"file '{picture}'",'option framerate 60'];(folder/'frames.txt').write_text('\n'.join(lines)+'\n');(folder/'labels.ass').write_text('\n'.join(ass)+'\n')
 with wave.open(str(folder/'actual.wav'),'wb') as f:
  f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(np.concatenate(audio)*32768,-32768,32767).astype('<i2').tobytes())
 video=OUT/'HidariShinju_katon_base_motor.mp4'
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(folder/'frames.txt'),'-i',str(folder/'actual.wav'),'-vf',f"fps=30,drawbox=x=0:y=680:w=1280:h=40:color=0x090f18:t=fill,subtitles={folder/'labels.ass'}",'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
 board=Image.new('RGB',(960,360))
 for i,path in enumerate(shots):board.paste(Image.open(path).resize((320,180)),(i%3*320,i//3*180))
 board.save(OUT/'HidariShinju_katon_base_muestras.jpg')
 for title,tick in [('carga',40),('avance',65),('impacto',60)]:
  scene=1 if title=='avance' else 0;shot=min((r for r in rows if r[2]==scene),key=lambda r:abs(r[3]-tick))
  shutil.copy2(folder/f'Ikemen_GO{shot[0]:03d}.png',OUT/f'HidariShinju_katon_{title}_motor.png')
 result=dict(runtime_sha256=checks['runtime_sha256'],source='Original Sasuke BTM Gokakyu AIR 1150/1160, sprites 1052/1054 and sounds 4,10 / 4,8; adapted to the mouth and body height of Hidari',video=video.name,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),duration=duration,scenes=scenes,native_audio_cues_matched=len(peaks),audio_confidences=[float(scores[p]) for p in peaks],audio='Actual native SDL audio, matched to each activation; rendering stalls compressed',failures=[])
 (OUT/'HidariShinju_katon_demo_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS RB Gokakyu native video',round(duration,2),'seconds;',folder)
if __name__=='__main__':main()
