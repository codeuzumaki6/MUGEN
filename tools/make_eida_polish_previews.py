#!/usr/bin/env python3
"""Record Eida presentation with actual stereo SDL output, never offline SFX."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,resample_poly,find_peaks

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
engine=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
scenes=[
 ('charge',17,'senrigan_charge_loop.wav','LB: CARGA | Gesto Senrigan, cabello y motas discretas'),
 ('run',20,'soft_footfall.wav','CARRERA Y FRENADO | Ciclo propio, apoyo de pies y polvo'),
 ('land',20,'soft_footfall.wav','SALTO Y ATERRIZAJE | Compresion y recuperacion'),
 ('finisher',19,'daemon_impact_finish.wav','Y Y | Contacto, sonido y remate que lanza al rival'),
 ('daemon',19,'daemon_impact_finish.wav','RT: DAEMON | Entrada desde Eida, seis impactos y retirada'),
 ('win',18,'senrigan_release.wav','VICTORIA TRAS KO DE PRUEBA | Gesto, cabello y pose final')]
signature=hashlib.sha256(b''.join((ROOT/'Eida'/name).read_bytes() for name in ['Eida.def','Eida.air','Eida.cns','Eida.cmd','Eida.sff','Eida.snd','Specials.cns','Omnipotencia.cns','common1.cns'])).hexdigest()
checkpoint_path=OUT/'Eida_polish_capture_checkpoint.json'
checkpoint=json.loads(checkpoint_path.read_text()) if checkpoint_path.exists() else {'scenes':{}}
if checkpoint.get('runtime_sha256')!=signature:checkpoint=dict(runtime_sha256=signature,scenes={})
clips=[];evidence=[];reports=[]
with tempfile.TemporaryDirectory(prefix='eida-polish-preview-') as directory:
    temp=Path(directory)
    for kind,sound,sample,caption in scenes:
        clip=OUT/f'Eida_acabado_{kind}_motor.mp4';clips.append(clip);cached=checkpoint['scenes'].get(kind)
        if cached and clip.exists() and hashlib.sha256(clip.read_bytes()).hexdigest()==cached['video_sha256']:
            evidence.append(cached['audio']);reports+=cached['reports'];print('REUSE',kind,flush=True);continue
        folder=temp/kind;folder.mkdir();raw=folder/'audio.raw';env=os.environ.copy()
        env.update(EIDA_POLISH_CAPTURE=str(folder),EIDA_POLISH_CASES=json.dumps([kind]),EIDA_POLISH_TICKS='240',EIDA_RECORD_AUDIO=str(raw))
        env.pop('EIDA_WIN_CHECK',None)
        if kind=='win':env['EIDA_WIN_CHECK']='1'
        result=subprocess.run([sys.executable,str(ROOT/'tools/check_eida_polish_in_engine.py'),engine],env=env,capture_output=True,text=True)
        assert result.returncode==0,result.stdout+result.stderr
        scenario_reports=json.loads((OUT/('Eida_polish_win_visual_checks.json' if kind=='win' else 'Eida_polish_visual_checks.json')).read_text());reports+=scenario_reports
        frames=[tuple(map(int,line.split())) for line in (folder/'frames.tsv').read_text().splitlines()]
        cues=[tuple(map(int,line.split())) for line in (folder/'audio.tsv').read_text().splitlines()]
        activation=[t for t,n in cues if n==sound];assert activation,(kind,cues)
        with wave.open(str(ROOT/'Eida/assets/sound'/sample)) as f:
            assert f.getframerate()==22050;cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)
        stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
        cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)]
        norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));scores=np.abs(cross)/np.maximum(norm,1e-12)
        if len(activation)>1:
            peaks,_=find_peaks(scores,height=max(.25,float(scores.max())*.88),distance=round(.12*44100));assert len(peaks);peak=int(peaks[0])
        else:peak=int(np.argmax(scores))
        confidence=float(scores[peak]);assert confidence>.25,(kind,confidence)
        start=peak/44100-(activation[0]-frames[0][1])/60;assert start>=0,(kind,start)
        first=round(start*44100);duration=(frames[-1][1]+4-frames[0][1])/60;last=first+round(duration*44100)
        if last>len(stereo):
            assert (last-len(stereo))/44100<.35,(kind,last,len(stereo))
            limit=frames[0][1]+(len(stereo)-first)*60/44100-4;frames=[p for p in frames if p[1]<=limit]
            duration=(frames[-1][1]+4-frames[0][1])/60;last=first+round(duration*44100)
        assert len(frames)>=30 and last<=len(stereo),(kind,len(frames))
        actual=folder/'actual.wav';audio=stereo[first:last]
        with wave.open(str(actual),'wb') as f:f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(audio*32768,-32768,32767).astype('<i2').tobytes())
        lines=['ffconcat version 1.0']
        for i,(n,tick) in enumerate(frames):
            path=folder/f'Ikemen_GO{n:03d}.png';assert path.exists()
            delta=frames[i+1][1]-tick if i+1<len(frames) else 4
            lines += [f"file '{path}'",'option framerate 60',f'duration {delta/60:.9f}']
        lines += [f"file '{path}'",'option framerate 60']
        listing=folder/'frames.txt';listing.write_text('\n'.join(lines)+'\n');text=folder/'caption.txt';text.write_text(caption)
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-i',str(actual),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=expansion=none:textfile={text}:x=(w-tw)/2:y=689:fontsize=21:fontcolor=white','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(clip)],check=True)
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(clip),'-filter_complex','[0:v]fps=15,scale=640:-1:flags=neighbor,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(clip.with_suffix('.gif'))],check=True)
        target=activation[0]+18;frame=min(frames,key=lambda p:abs(p[1]-target));shutil.copy2(folder/f'Ikemen_GO{frame[0]:03d}.png',clip.with_suffix('.png'))
        item=dict(case=kind,frames=len(frames),duration=duration,cue=sample,activation_tick=activation[0],activation_correlation=confidence,alignment_start_seconds=start,audio_source='Actual SDL disk output, stereo S16LE 44100 Hz; no offline SFX mix',raw_audio_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),near_full_scale_fraction=float(np.mean(np.abs(audio)>.999)))
        evidence.append(item);checkpoint['scenes'][kind]=dict(video_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),audio=item,reports=scenario_reports)
        checkpoint_path.write_text(json.dumps(checkpoint,indent=2)+'\n');print(kind,len(frames),'frames, actual SDL correlation',round(confidence,3),flush=True)
    listing=temp/'clips.txt';listing.write_text(''.join(f"file '{p}'\n" for p in clips))
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUT/'Eida_ACABADO.mp4')],check=True)
(OUT/'Eida_polish_visual_checks.json').write_text(json.dumps(reports,indent=2)+'\n')
(OUT/'Eida_polish_audio_checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Captured six Eida presentation scenes with real audio')
