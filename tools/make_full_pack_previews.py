#!/usr/bin/env python3
"""Record changed supplied animations in the real engine with actual SDL audio."""
from pathlib import Path
import hashlib,io,json,os,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
JOBS=[
 ('MitsukiTBV','MITSUKI','check_mitsuki_in_engine.py',['Raiton'],240,'Normal y sabio: rayos originales; Senpo Orochi Ikazuchi verde'),
 ('RyuShinju','RYU','check_ryu_in_engine.py',['Prision','Torbellino','ultimate'],320,'Ryu: prision, torbellino y ulti con alas del paquete original'),
 ('HidariShinju','HIDARI','check_hidari_susanoo_in_engine.py',['Puno','awakening'],320,'Hidari: Susanoo amarillo original, manifestacion y espada'),
 ('MatsuriShinju','MATSURI','check_matsuri_in_engine.py',['Suiton','Latigo','ultimate'],320,'Matsuri: agua y capa originales; despertar conserva su cuerpo sin capa'),
]
def sound(character,number=21):
 data=(ROOT/character/(character+'.snd')).read_bytes();count,off=__import__('struct').unpack_from('<2I',data,16)
 for _ in range(count):
  nxt,size,g,n=__import__('struct').unpack_from('<4I',data,off)
  if (g,n)==(1,number):
   with wave.open(io.BytesIO(data[off+16:off+16+size])) as w:
    raw=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
    return resample_poly(raw,44100,w.getframerate())
  off=nxt
 raise AssertionError('missing startup')
def main():
 reports=[]
 for ch,prefix,script,cases,ticks,title in JOBS:
  if sys.argv[1:] and ch not in sys.argv[1:]:continue
  base=Path('/tmp/full-pack-native')/ch;base.mkdir(parents=True,exist_ok=True)
  if os.environ.get('FULL_PACK_REUSE')=='1':folder=Path(json.loads((base/'latest.json').read_text())['folder'])
  else:
   # screenshot() skips existing filenames. Every recording needs a fresh
   # directory; otherwise old pictures can be attached to new telemetry.
   folder=Path(tempfile.mkdtemp(prefix='take-',dir=base))
   (base/'latest.json').write_text(json.dumps(dict(folder=str(folder)))+'\n')
  raw=folder/'audio.raw';env=os.environ.copy()
  env.update({prefix+'_CAPTURE':str(folder),prefix+'_AUDIO':str(raw),prefix+'_CASES':json.dumps(cases),prefix+'_TICKS':str(ticks),prefix+'_ALL_SPECIALS':'1'})
  if os.environ.get('FULL_PACK_REUSE')!='1':
   with (folder/'engine.log').open('w') as f:
    r=subprocess.run([sys.executable,str(ROOT/'tools'/script)],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
   assert r.returncode==0,(folder/'engine.log').read_text()[-5000:]
  else:
   report=json.loads((OUT/(ch+'_capture_checks.json')).read_text());files=[ch+'.'+s for s in ['def','cns','cmd','air','sff','snd']]+[ch+'_common.cns']
   assert report['runtime_sha256']==hashlib.sha256(b''.join((ROOT/ch/n).read_bytes() for n in files)).hexdigest(),'cached capture is from another runtime'
  frames=[list(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()]
  cues=[list(map(int,l.split())) for l in (folder/'cues.tsv').read_text().splitlines()]
  ids=sorted({r[2] for r in frames});assert ids and len(frames)<1000
  stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(1);cue=sound(ch)[:round(.12*44100)]
  cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)]
  den=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));scores=np.abs(cross)/np.maximum(den,1e-12)
  peaks,_=find_peaks(scores,height=.16,distance=round(.65*44100))
  if ch=='HidariShinju' and len(ids)==2:
   # Puno uses S1,0 at local time 3, whereas the awakening uses S1,21.
   assert cues[0][1]==14200 and cues[1][1]==520
   awake_peak=int(max(peaks,key=lambda p:scores[p]));estimated=int(awake_peak-(cues[1][0]-cues[0][0]-3)*44100/60)
   punch=sound(ch,0);cross2=correlate(mono,punch,mode='valid',method='fft');eng2=np.sqrt(np.maximum(0,energy[len(punch):]-energy[:-len(punch)])*np.sum(punch*punch));punch_scores=np.abs(cross2)/np.maximum(eng2,1e-12)
   lo=max(0,estimated-11025);hi=min(len(punch_scores),estimated+11025);hit=lo+int(np.argmax(punch_scores[lo:hi]));assert punch_scores[hit]>.25
   selected=[hit-round(3*44100/60),awake_peak];scores[selected[0]]=punch_scores[hit]
  else:
   assert len(peaks)>=len(ids),(ch,len(peaks),len(ids),scores.max())
   selected=sorted(sorted(peaks,key=lambda p:scores[p],reverse=True)[:len(ids)])
  listings=['ffconcat version 1.0'];samples=[];shots=[];proof=[]
  for case,p in zip(ids,selected):
   fs=[row for row in frames if row[2]==case];activation=[c for c in cues if fs[0][1]<=c[0]<=fs[-1][1]]
   assert len(activation)==1,(ch,case,activation)
   offset=p/44100-activation[0][0]/60
   start=round((fs[0][1]/60+offset)*44100);end=round(((fs[-1][1]+4)/60+offset)*44100)
   assert start>=0 and end<=len(stereo),(ch,case,start,end,len(stereo))
   samples.append(stereo[start:end]);proof.append(dict(case=case,cue_frame=activation[0][0],correlation=float(scores[p]),actual_sample_seconds=p/44100))
   for j,row in enumerate(fs):
    image=folder/f'Ikemen_GO{row[0]:03d}.png';assert image.exists()
    step=fs[j+1][1]-row[1] if j+1<len(fs) else 4
    listings += [f"file '{image}'",'option framerate 60',f'duration {step/60:.9f}']
   for t in [42,68,104,142]:shots.append(min(fs,key=lambda r:abs(r[3]-t)))
  listings += [f"file '{image}'",'option framerate 60'];listing=folder/'frames.txt';listing.write_text('\n'.join(listings)+'\n')
  audio=folder/'actual.wav';audio_data=np.concatenate(samples)
  with wave.open(str(audio),'wb') as w:w.setparams((2,2,44100,0,'NONE','not compressed'));w.writeframes(np.clip(audio_data*32768,-32768,32767).astype('<i2').tobytes())
  text=folder/'title.txt';text.write_text(title);duration=len(audio_data)/44100;video=OUT/(ch+'_paquete_completo_motor.mp4')
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-i',str(audio),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=expansion=none:textfile={text}:x=(w-tw)/2:y=690:fontsize=18:fontcolor=white','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
  sheet=Image.new('RGB',(1280,360*((len(shots)+1)//2)))
  for i,row in enumerate(shots):
   im=Image.open(folder/f'Ikemen_GO{row[0]:03d}.png');im.thumbnail((640,360));sheet.paste(im,((i%2)*640,(i//2)*360))
  sheet.save(video.with_suffix('.jpg'))
  report=dict(character=ch,frames=len(frames),cases=len(ids),duration=duration,video=video.name,sha256=hashlib.sha256(video.read_bytes()).hexdigest(),audio='Actual engine SDL stereo; no offline effect mix',activations=proof,source_log_sha256=hashlib.sha256((folder/'engine.log').read_bytes()).hexdigest())
  reports.append(report);print(json.dumps(report),flush=True)
 dest=OUT/'full_pack_preview_checks.json';old=json.loads(dest.read_text()) if dest.exists() else []
 merged={r['character']:r for r in old};merged.update({r['character']:r for r in reports});dest.write_text(json.dumps(list(merged.values()),indent=2)+'\n')
if __name__=='__main__':main()
