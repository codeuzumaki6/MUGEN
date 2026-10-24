#!/usr/bin/env python3
"""Record all nine original Susanoo attacks and hold-to-awaken with real audio."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly
from PIL import Image
from build_hidari_susanoo import MOVES,NORMALS
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
END={14200:136,14300:136,14400:136,14500:184,14600:190,14700:148,14800:260,14850:175,14900:302,520:210}
SHOT={14200:40,14300:39,14400:43,14500:74,14600:81,14700:66,14800:125,14850:83,14900:91,520:142}

def main():
 folder=Path(os.environ.get('HIDARI_REUSE_CAPTURE') or tempfile.mkdtemp(prefix='hidari-original-susanoo-'));raw=folder/'audio.raw'
 if not os.environ.get('HIDARI_REUSE_CAPTURE'):
  env=os.environ.copy();env.update(HIDARI_CAPTURE=str(folder),HIDARI_AUDIO=str(raw),HIDARI_ALL_SPECIALS='1',HIDARI_TICKS='360')
  subprocess.run(['python',str(ROOT/'tools/check_hidari_susanoo_in_engine.py')],env=env,check=True);shutil.copy2(OUT/'HidariShinju_sasuke_capture_checks.json',folder/'checks.json')
 checks=json.loads((folder/'checks.json').read_text());cases=[c['case'] for c in checks['cases']];assert len(cases)==10 and all(not c['failures'] for c in checks['cases'])
 rows=[tuple(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()];cues=[tuple(map(int,l.split())) for l in (folder/'cues.tsv').read_text().splitlines()];stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(1)
 # Watch the two source poses that previously enlarged during impact pauses.
 areas=[]
 for idx,clock,scene,tick in rows:
  if cases[scene]['state'] not in [14300,14600]:continue
  rgb=np.array(Image.open(folder/f'Ikemen_GO{idx:03d}.png').convert('RGB'),dtype=np.int16)[160:]
  r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2];areas.append(int(((r>120)&(g>95)&(np.abs(r-g)<65)&(b<r*.8)).sum()))
 assert areas and max(areas)<250000,('Source guardian enlarged during impact',max(areas))
 (OUT/'HidariShinju_sasuke_scale_checks.json').write_text(json.dumps(dict(runtime_sha256=checks['runtime_sha256'],frames_checked=len(areas),max_yellow_area=max(areas),limit=250000,failures=[]),indent=2)+'\n')
 def match(sample,prefix=.3):
  with wave.open(str(ROOT/f'HidariShinju/assets/sound/1_{sample}.wav')) as f:
   rate=f.getframerate();x=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768
  from fractions import Fraction
  ratio=Fraction(44100,rate);x=resample_poly(x,ratio.numerator,ratio.denominator)[:round(prefix*44100)];cross=correlate(mono,x,mode='valid',method='fft');en=np.r_[0,np.cumsum(mono*mono)];den=np.sqrt(np.maximum(0,en[len(x):]-en[:-len(x)])*np.sum(x*x));scores=np.abs(cross)/np.maximum(den,1e-12);peaks,_=find_peaks(scores,height=.5,distance=round(.5*44100));return scores,peaks
 scores,peaks=match(21);events=[c for c in cues if c[1]>=14500 or c[1]==520];assert len(events)==len(peaks)==7,(len(events),len(peaks));matched={n:(t,int(p),float(scores[p])) for (t,n),p in zip(events,peaks)}
 scores,hits=match(0,.16);hits=[p for p in hits if p<peaks[0]-.3*44100];normals=[c for c in cues if 14200<=c[1]<=14400];assert len(hits)==len(normals)==3,(len(hits),len(normals))
 for (t,n),p in zip(normals,hits):matched[n]=(t+3,int(p),float(scores[p]))
 labels=[];lines=['ffconcat version 1.0'];audio=[];ranges=[];shots=[];duration=0
 ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 1280','PlayResY: 720','','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Default,DejaVu Sans,21,&H00BFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,16,16,9,1','','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
 def stamp(t):
  cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
 for i,case in enumerate(cases):
  n=case['state'];label='abajo + mantener Pausa | Despertar' if n==520 else {'a':'X','b':'Y','c':'B'}[case['b']]+' | '+case['name'] if n<14500 else {'F':'abajo, adelante + ','B':'abajo, atras + '}[case['d']]+{'a':'X','b':'Y','c':'B'}[case['b']]+' | '+case['name'];labels.append(label)
  fs=[r for r in rows if r[2]==i and r[3]<=END[n]];assert len(fs)>=12
  t,p,confidence=matched[n];offset=p/44100-t/60;start=round((fs[0][1]/60+offset)*44100);end=round(((fs[-1][1]+6)/60+offset)*44100);assert 0<=start<end<=len(stereo)
  audio.append(stereo[start:end]);begin=duration;duration+=(end-start)/44100;ranges.append(dict(state=n,start=begin,end=duration,label=label));ass.append(f'Dialogue: 0,{stamp(begin)},{stamp(duration)},Default,,0,0,0,,{label}')
  for j,(idx,clock,scene,tick) in enumerate(fs):
   image=folder/f'Ikemen_GO{idx:03d}.png';assert image.exists();delta=fs[j+1][1]-clock if j+1<len(fs) else 6;lines += [f"file '{image}'",'option framerate 60',f'duration {delta/60:.9f}']
  shot=min(fs,key=lambda r:abs(r[3]-SHOT[n]));shots.append(folder/f'Ikemen_GO{shot[0]:03d}.png')
 lines += [f"file '{image}'",'option framerate 60'];(folder/'frames.txt').write_text('\n'.join(lines)+'\n');(folder/'labels.ass').write_text('\n'.join(ass)+'\n')
 with wave.open(str(folder/'actual.wav'),'wb') as f:f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(np.concatenate(audio)*32768,-32768,32767).astype('<i2').tobytes())
 video=OUT/'HidariShinju_susanoo_sasuke_motor.mp4';subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(folder/'frames.txt'),'-i',str(folder/'actual.wav'),'-vf',f"fps=30,drawbox=x=0:y=680:w=1280:h=40:color=0x090f18:t=fill,subtitles={folder/'labels.ass'}",'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
 board=Image.new('RGB',(1280,540))
 for i,p in enumerate(shots):
  im=Image.open(p);board.paste(im.resize((320,180)),(i%4*320,i//4*180));im.save(OUT/f"HidariShinju_original_{cases[i]['state']}_motor.png")
 board.save(OUT/'HidariShinju_susanoo_sasuke_muestras.jpg');scene=next(r for r in ranges if r['state']==14900);clip=OUT/'HidariShinju_indra_motor.mp4';subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(scene['start']),'-i',str(video),'-t',str(scene['end']-scene['start']),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(clip)],check=True)
 result=dict(runtime_sha256=checks['runtime_sha256'],source='Sasuke BTM original Susanoo; palette recolored yellow',nine_source_attacks_shown=True,hold_activation_shown=True,video=video.name,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),indra_clip=clip.name,indra_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),duration=duration,scenes=ranges,audio='Actual SDL audio, native activation matched per scene; render stalls compressed',native_audio_cues_matched=10,audio_confidences={str(n):c for n,(t,p,c) in matched.items()},failures=[]);(OUT/'HidariShinju_sasuke_demo_checks.json').write_text(json.dumps(result,indent=2)+'\n');shutil.copy2(video,OUT/'HidariShinju_gameplay_motor.mp4');shutil.copy2(clip,OUT/'HidariShinju_ulti_motor.mp4');(OUT/'HidariShinju_demo_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS original nine attacks and awakening',round(duration,2),'seconds; capture',folder)
if __name__=='__main__':main()
