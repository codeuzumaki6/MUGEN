#!/usr/bin/env python3
"""Record the polished combat and an actual round victory with real SDL audio."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,resample_poly,find_peaks
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews';engine=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
scenarios=[
 ('carga','Carga con motores','polish',240,0,'chainsaw_accel.wav','LB: CARGA | Motores, vibracion, bufanda y chispas de las sierras'),
 ('carrera','Carrera frenado','polish',240,17,'footfall_dust.wav','CARRERA Y FRENADO | Bufanda animada, polvo y apoyo de los pies'),
 ('aterrizaje','Salto aterrizaje','polish',240,17,'footfall_dust.wav','SALTO Y ATERRIZAJE | Compresion, polvo y recuperacion'),
 ('remate','Remate X','polish',240,16,'serrated_finish.wav','X X X | Estela dentada, contacto metalico y remate confirmado'),
 ('remate_aereo','Air XYB','air',240,8,'cross_saw_cut.wav','X Y B EN EL AIRE | Cortes, estelas rojas y remate descendente'),
 ('victoria','Victoria real','win',420,15,'motor_spindown.wav','VICTORIA TRAS KO DE PRUEBA | Sacudir sierras y bajar motores')]
reports=[];evidence=[];clips=[]
signature=hashlib.sha256(b''.join((ROOT/'PochitaTrueForm'/('PochitaTrueForm'+ext)).read_bytes() for ext in ['.cns','.cmd','.air','.sff','.snd'])).hexdigest()
checkpoint_path=OUT/'Pochita_polish_capture_checkpoint.json'
checkpoint=json.loads(checkpoint_path.read_text()) if checkpoint_path.exists() else {}
scopes={'carga':[-2,500],'carrera':[-2,106],'aterrizaje':[-2],'remate':[-2,200,201,202],'remate_aereo':[-2,600,661,672],'victoria':[-2,180,200]}
def scope_hash(label):
 char=ROOT/'PochitaTrueForm';cns=(char/'PochitaTrueForm.cns').read_bytes();shared=b''.join((char/name).read_bytes() for name in ['PochitaTrueForm.sff','PochitaTrueForm.snd','PochitaTrueForm.air','PochitaTrueForm.cmd','PochitaTrueForm.def','common1.cns'])
 blocks=[re.search(rb'(?ims)^\[Statedef '+str(n).encode()+rb'\].*?(?=^\[Statedef|\Z)',cns)[0] for n in scopes[label]]
 return hashlib.sha256(shared+b''.join(blocks)).hexdigest()
# Reuse only captures whose referenced combat states and shared assets match.
if 'scenarios' not in checkpoint:checkpoint=dict(scenarios={})
checkpoint['runtime_sha256']=signature
with tempfile.TemporaryDirectory(prefix='pochita-polish-preview-') as temp:
 folder=Path(temp)
 for label,name,mode,ticks,sound,sample,caption in scenarios:
  clip=OUT/f'Pochita_acabado_{label}_motor.mp4'
  cached=checkpoint['scenarios'].get(label)
  if cached and cached.get('scope_sha256')==scope_hash(label) and clip.exists() and hashlib.sha256(clip.read_bytes()).hexdigest()==cached['video_sha256']:
   reports+=cached['reports'];evidence.append(cached['audio']);clips.append(clip);print('REUSE verified capture',name,flush=True);continue
  scenario_reports=[]
  capture=folder/label;capture.mkdir();raw=capture/'engine_audio.raw';env=os.environ.copy()
  env.update(POCHITA_RECORD_AUDIO=str(raw),POCHITA_CAPTURE=str(capture),POCHITA_CAPTURE_CASES=json.dumps([name]),POCHITA_PREVIEW_SET='polish',POCHITA_TICKS=str(ticks))
  for option in ['POCHITA_AIR_SCARF_CHECK','POCHITA_POLISH_CHECK','POCHITA_WIN_CHECK','POCHITA_DEVOUR_CHECK']:env.pop(option,None)
  env[{'polish':'POCHITA_POLISH_CHECK','air':'POCHITA_AIR_SCARF_CHECK','win':'POCHITA_WIN_CHECK'}[mode]]='1'
  run=subprocess.run([sys.executable,str(ROOT/'tools/check_pochita_in_engine.py'),engine],env=env,capture_output=True,text=True);assert run.returncode==0,run.stdout+run.stderr
  if mode!='win':scenario_reports=json.loads((OUT/'Pochita_polish_visual_checks.json').read_text());reports+=scenario_reports
  frames=[tuple(map(int,line.split())) for line in (capture/'frames.tsv').read_text().splitlines()];events=[tuple(map(int,line.split())) for line in (capture/'audio.tsv').read_text().splitlines()]
  activation=[t for t,n in events if n==sound];assert activation,(name,events);assert len(frames)>=30,(name,len(frames))
  with wave.open(str(ROOT/'PochitaTrueForm/assets/sound'/sample),'rb') as f:
   assert f.getframerate()==22050;cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)
  stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
  cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)];norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue))
  score=np.abs(cross)/np.maximum(norm,1e-12)
  if len(activation)>1:
   peaks,_=find_peaks(score,height=max(.25,float(score.max())*.88),distance=round(.12*44100));assert len(peaks);peak=int(peaks[0])
  else:peak=int(np.argmax(score))
  confidence=float(score[peak]);assert confidence>.25,(name,confidence)
  start=peak/44100-(activation[0]-frames[0][1])/60;assert start>=0,(name,start)
  duration=(frames[-1][1]+4-frames[0][1])/60;first=round(start*44100);last=first+round(duration*44100)
  if last>len(stereo):
   assert mode=='win' and (last-len(stereo))/44100<.35,(name,last,len(stereo))
   # SDL may finish its last buffer before the final held victory screenshots.
   # Trim those screenshots to real recorded audio rather than invent a tail.
   limit=frames[0][1]+(len(stereo)-first)*60/44100-4
   frames=[pair for pair in frames if pair[1]<=limit]
   duration=(frames[-1][1]+4-frames[0][1])/60;last=first+round(duration*44100)
  assert last<=len(stereo) and len(frames)>=30,(name,last,len(stereo))
  actual=capture/'audio.wav';audio=stereo[first:last]
  with wave.open(str(actual),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(44100);f.writeframes(np.clip(audio*32768,-32768,32767).astype('<i2').tobytes())
  lines=['ffconcat version 1.0']
  for i,(frame,tick) in enumerate(frames):
   path=capture/f'Ikemen_GO{frame:03d}.png';assert path.is_file();delta=frames[i+1][1]-tick if i+1<len(frames) else 4
   lines += [f"file '{path}'",'option framerate 60',f'duration {delta/60:.9f}']
  lines += [f"file '{path}'",'option framerate 60'];listing=capture/'frames.txt';listing.write_text('\n'.join(lines)+'\n')
  text=capture/'caption.txt';text.write_text(caption);clip=OUT/f'Pochita_acabado_{label}_motor.mp4';clips.append(clip)
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-i',str(actual),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=expansion=none:textfile={text}:x=(w-tw)/2:y=689:fontsize=21:fontcolor=white','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(clip)],check=True)
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(clip),'-filter_complex','[0:v]fps=15,scale=640:-1:flags=neighbor,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(OUT/f'Pochita_acabado_{label}_motor.gif')],check=True)
  thumbnail_tick=activation[0]+18;chosen=min(frames,key=lambda p:abs(p[1]-thumbnail_tick));shutil.copy2(capture/f'Ikemen_GO{chosen[0]:03d}.png',OUT/f'Pochita_acabado_{label}_motor.png')
  evidence.append(dict(case=name,frames=len(frames),cue=sound,activation_tick=activation[0],activation_correlation=confidence,duration=duration,audio_source='Actual SDL disk driver output, stereo S16LE 44100 Hz, no offline mix',raw_audio_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),alignment_start_seconds=start,near_full_scale_fraction=float(np.mean(np.abs(audio)>.999))))
  checkpoint['scenarios'][label]=dict(runtime_sha256=signature,scope_sha256=scope_hash(label),video_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),reports=scenario_reports,audio=evidence[-1]);checkpoint_path.write_text(json.dumps(checkpoint,indent=2)+'\n')
  print(name,len(frames),'frames; actual SDL correlation',round(confidence,3),flush=True)
 listing=folder/'clips.txt';listing.write_text(''.join(f"file '{p}'\n" for p in clips))
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUT/'Pochita_ACABADO.mp4')],check=True)
(OUT/'Pochita_polish_visual_checks.json').write_text(json.dumps(reports,indent=2)+'\n');(OUT/'Pochita_polish_audio_checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Captured polished motors, locomotion, landing, two finishers and an actual victory')
