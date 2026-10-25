#!/usr/bin/env python3
"""Actual engine screenshots plus SDL audio, with measured activation alignment."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks
from PIL import Image
from make_full_pack_previews import sound
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
CASES=['Piston','Pierna','RayoDestructor','Propulsion','ultimate_one_hp','absorb_projectile','awakening']
ACTIVATIONS={1000,1010,1020,1210,3000,1430,520}
def main():
 folder=Path(tempfile.mkdtemp(prefix='delta-native-',dir='/tmp'));raw=folder/'audio.raw'
 env=os.environ.copy();env.update(DELTA_CAPTURE=str(folder),DELTA_AUDIO=str(raw),DELTA_CASES=json.dumps(CASES),DELTA_FACE='1',DELTA_TICKS='440')
 Path('/tmp/DeltaKara_latest_capture.json').write_text(json.dumps(dict(folder=str(folder)))+'\n')
 with (folder/'engine.log').open('w') as f:r=subprocess.run([sys.executable,str(ROOT/'tools/check_delta_in_engine.py')],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,(folder/'engine.log').read_text()[-5000:]
 frames=[list(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()]
 cues=[list(map(int,l.split())) for l in (folder/'cues.tsv').read_text().splitlines()]
 ids=sorted({r[2] for r in frames});assert len(ids)==7 and len(frames)<1000
 stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(1);cue=sound('DeltaKara')[:round(.12*44100)]
 cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)]
 den=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));scores=np.abs(cross)/np.maximum(den,1e-12)
 peaks,_=find_peaks(scores,height=.16,distance=round(.65*44100));assert len(peaks)>=7,(len(peaks),scores.max())
 selected=sorted(sorted(peaks,key=lambda p:scores[p],reverse=True)[:7]);listing=['ffconcat version 1.0'];samples=[];shots=[];proof=[]
 for case,p in zip(ids,selected):
  fs=[row for row in frames if row[2]==case];activation=[c for c in cues if c[1]==case and c[2] in ACTIVATIONS]
  assert len(activation)==1,(case,activation)
  offset=p/44100-activation[0][0]/60
  start=round((fs[0][1]/60+offset)*44100);end=round(((fs[-1][1]+4)/60+offset)*44100)
  assert start>=0 and end<=len(stereo),(case,start,end,len(stereo))
  samples.append(stereo[start:end]);proof.append(dict(case=case,cue_frame=activation[0][0],state=activation[0][2],correlation=float(scores[p]),actual_sample_seconds=p/44100))
  for j,row in enumerate(fs):
   image=folder/f'Ikemen_GO{row[0]:03d}.png';assert image.exists();step=fs[j+1][1]-row[1] if j+1<len(fs) else 4
   listing.extend([f"file '{image}'",'option framerate 60',f'duration {step/60:.9f}'])
  for tick in [56,64,100]:shots.append(min(fs,key=lambda r:abs(r[3]-tick)))
 listing.extend([f"file '{image}'",'option framerate 60']);(folder/'frames.txt').write_text('\n'.join(listing)+'\n')
 audio=np.concatenate(samples)
 with wave.open(str(folder/'actual.wav'),'wb') as w:w.setparams((2,2,44100,0,'NONE','not compressed'));w.writeframes(np.clip(audio*32768,-32768,32767).astype('<i2').tobytes())
 title=folder/'title.txt';title.write_text('Delta Kara | Ulti sin coste de vida | Sprites recreados | Motor y audio reales')
 video=OUT/'DeltaKara_motor.mp4';duration=len(audio)/44100
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(folder/'frames.txt'),'-i',str(folder/'actual.wav'),'-vf',f'fps=30,drawbox=x=0:y=ih-38:w=iw:h=38:color=black@0.8:t=fill,drawtext=expansion=none:textfile={title}:x=(w-tw)/2:y=h-28:fontsize=18:fontcolor=white','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
 sheet=Image.new('RGB',(960,180*((len(shots)+2)//3)))
 for i,row in enumerate(shots):
  im=Image.open(folder/f'Ikemen_GO{row[0]:03d}.png');im.thumbnail((320,180));sheet.paste(im,((i%3)*320,(i//3)*180))
 sheet.save(OUT/'DeltaKara_motor.jpg')
 report=dict(character='DeltaKara',frames=len(frames),cases=len(ids),duration=duration,video=video.name,sha256=hashlib.sha256(video.read_bytes()).hexdigest(),audio='Actual engine SDL stereo; no offline sound effects',activations=proof,runtime_sha256=json.loads((OUT/'DeltaKara_capture_checks.json').read_text())['runtime_sha256'])
 (OUT/'DeltaKara_preview_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
