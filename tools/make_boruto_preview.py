#!/usr/bin/env python3
"""Actual engine screenshots plus SDL audio, with measured activation alignment."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,wave,io
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly
from PIL import Image
from make_full_pack_previews import sound
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
def main():
 activations={1000,1010,1020,1030,1040,1050,1200,1210,1400,1410,1420,1430,1440,3000,11000,11010,11020,11030,11040,11050,11200,11210,11400,11410,11420,11430,11440,13000,520}
 prefix='BorutoKarmaJogan';capture_report=prefix+'_capture_checks.json'
 latest=Path('/tmp/'+prefix+'_latest_capture.json')
 if os.environ.get('BORUTO_PREVIEW_REUSE')=='1':
  folder=Path(json.loads(latest.read_text())['folder']);raw=folder/'audio.raw'
  files=['BorutoKarmaJogan.'+s for s in ['def','cns','cmd','air','sff','snd']]+['BorutoKarmaJogan_common.cns']
  assert json.loads((OUT/capture_report).read_text())['runtime_sha256']==hashlib.sha256(b''.join((ROOT/'BorutoKarmaJogan'/f).read_bytes() for f in files)).hexdigest()
 else:
  folder=Path(tempfile.mkdtemp(prefix='boruto-native-',dir='/tmp'));raw=folder/'audio.raw'
  env=os.environ.copy();env.update(BORUTO_CAPTURE=str(folder),BORUTO_AUDIO=str(raw),BORUTO_FACE='1',BORUTO_TICKS='660',BORUTO_REPORT=capture_report,BORUTO_DEMO='showcase')
  latest.write_text(json.dumps(dict(folder=str(folder)))+'\n')
  with (folder/'engine.log').open('w') as f:r=subprocess.run([sys.executable,str(ROOT/'tools/check_boruto_in_engine.py')],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
  assert r.returncode==0,(folder/'engine.log').read_text()[-5000:]
 frames=[list(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()]
 cues=[list(map(int,l.split())) for l in (folder/'cues.tsv').read_text().splitlines()]
 ids=sorted({r[2] for r in frames});reports=json.loads((OUT/capture_report).read_text())['cases'];expected=sum(r['case']['kind']!='recovery' for r in reports);assert len(ids)==len(reports)
 stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(1)
 # The claw effect shares the startup effect's opening waveform. Anchor to
 # each original startup voice instead, so later minion hits cannot win.
 voices={name:'BorutoJogan/'+('05' if name in ['Futon','ultimate','awakening'] else '04' if name=='Invocacion' else '03' if name in ['Rasengan','Espiral','Caida'] else '02' if name in ['Kenjutsu','Ascendente'] else '01') for name in ['Rasengan','Shiden','Kenjutsu','Espiral','Ascendente','Combo','Barrido','Bunshin','Caida','Kunai','Disparo','Invocacion','Futon','ultimate','awakening']}
 soundmap=json.loads((ROOT/'BorutoKarmaJogan/assets/sounds.json').read_text())['keys'];entries=[];selected=[];scores={};voicenames={}
 for case in ids:
  act=[c for c in cues if c[1]==case and c[2] in activations];assert len(act)==1,(case,act);entries.append(act[0])
  rec=reports[case]['case'];name='BorutoJogan/05' if rec['name']=='Espiral' or (rec['name']=='Invocacion' and rec['form']) else voices[rec['name']];g,n=soundmap[name];voicenames[case]=name
  with wave.open(str(ROOT/'BorutoKarmaJogan/assets/sound'/f'{g}_{n}.wav')) as wav:
   cue=resample_poly(np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)/32768,44100,wav.getframerate())[:round(.6*44100)]
  prediction=None if not selected else selected[-1]+(act[0][0]-entries[-2][0])*44100/60
  lo=0 if prediction is None else max(0,round(prediction-2*44100));hi=min(len(mono),8*44100 if prediction is None else round(prediction+2*44100)+len(cue));part=mono[lo:hi]
  cross=correlate(part,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(part*part)];den=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));local=np.abs(cross)/np.maximum(den,1e-12)
  candidates,_=find_peaks(local,height=.20,distance=round(.10*44100));assert len(candidates),(case,name,local.max())
  best=int(max(candidates,key=lambda p:local[p]-(0 if prediction is None else .12*abs(p+lo-prediction)/44100)));sample=lo+best;selected.append(sample);scores[sample]=float(local[best])
 listing=['ffconcat version 1.0'];samples=[];shots=[];proof=[];labels=[];elapsed=0
 selected=iter(selected)
 for case in ids:
  fs=[row for row in frames if row[2]==case];activation=[c for c in cues if c[1]==case and c[2] in activations]
  if reports[case]['case']['kind']=='recovery':
   for tick in [65,100,145]:shots.append(min(fs,key=lambda r:abs(r[3]-tick)))
   continue
  p=next(selected);assert len(activation)==1,(case,activation)
  offset=p/44100-activation[0][0]/60
  start=round((fs[0][1]/60+offset)*44100);end=round(((fs[-1][1]+6)/60+offset)*44100)
  assert start>=0 and end<=len(stereo),(case,start,end,len(stereo))
  rec=reports[case]['case'];display='Uzuhiko reforzado' if rec['name']=='Invocacion' and rec['form'] else 'Uzuhiko' if rec['name']=='Espiral' else 'Rasengan doble' if rec['name']=='Caida' and rec['form'] else 'Rasengan doble y resonancia' if rec['name']=='Futon' and rec['form'] else rec['name'];label=folder/f'label-{case}.txt';label.write_text(('KARMA / JOGAN' if rec['form'] else 'BASE')+' | '+display if rec['kind']!='awakening' else 'ABAJO + PAUSA | Resonancia Karma / Jogan');segment=(end-start)/44100;labels.append((label,elapsed,elapsed+segment));elapsed+=segment
  samples.append(stereo[start:end]);proof.append(dict(case=case,cue_frame=activation[0][0],state=activation[0][2],correlation=float(scores[p]),actual_sample_seconds=p/44100,voice=voicenames[case],anchor='Original Boruto pack startup sample'))
  for j,row in enumerate(fs):
   image=folder/f'Ikemen_GO{row[0]:03d}.png';assert image.exists();step=fs[j+1][1]-row[1] if j+1<len(fs) else 6
   listing.extend([f"file '{image}'",'option framerate 60',f'duration {step/60:.9f}'])
  for tick in [45,65,105,185]:shots.append(min(fs,key=lambda r:abs(r[3]-tick)))
 listing.extend([f"file '{image}'",'option framerate 60']);(folder/'frames.txt').write_text('\n'.join(listing)+'\n')
 audio=np.concatenate(samples)
 with wave.open(str(folder/'actual.wav'),'wb') as w:w.setparams((2,2,44100,0,'NONE','not compressed'));w.writeframes(np.clip(audio*32768,-32768,32767).astype('<i2').tobytes())
 title=folder/'title.txt';title.write_text('Boruto | Karma y Jogan | Sprites originales')
 video=OUT/'BorutoKarmaJogan_motor.mp4';duration=len(audio)/44100
 vf='fps=30,drawbox=x=0:y=ih-40:w=iw:h=40:color=black@0.8:t=fill'
 for label,a,b in labels:vf+=f",drawtext=expansion=none:textfile={label}:x=(w-tw)/2:y=h-31:fontsize=24:fontcolor=white:enable='between(t,{a:.6f},{b:.6f})'"
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(folder/'frames.txt'),'-i',str(folder/'actual.wav'),'-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
 sheet=Image.new('RGB',(960,180*((len(shots)+2)//3)))
 for i,row in enumerate(shots):
  im=Image.open(folder/f'Ikemen_GO{row[0]:03d}.png');im.thumbnail((320,180));sheet.paste(im,((i%3)*320,(i//3)*180))
 sheet.save(video.with_suffix('.jpg'))
 report=dict(character='BorutoKarmaJogan',frames=len(frames),cases=len(ids),duration=duration,video=video.name,sha256=hashlib.sha256(video.read_bytes()).hexdigest(),audio='Actual engine SDL stereo; no offline sound effects',activations=proof,runtime_sha256=json.loads((OUT/capture_report).read_text())['runtime_sha256'])
 (OUT/(prefix+'_preview_checks.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
