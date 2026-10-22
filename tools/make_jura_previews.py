#!/usr/bin/env python3
"""Film the actual Jura character. Audio is captured from SDL, never mixed."""
from pathlib import Path
from itertools import combinations
import hashlib,json,math,os,shutil,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews';ENGINE=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
JOBS=[('combos',['Combo a','Combo b','Combo c'],210,False,'JURA | X X X / Y Y Y / B B B: golpes y remates con derribo',0),
      ('aereos',['Aire a','Aire b','Aire c'],210,False,'JURA | Cadenas aereas de hasta tres golpes',0),
      ('madera',['Espinas','Raiz','Arbol'],230,True,'MOKUTON | Espinas sucesivas, raiz ascendente y arbol masivo',0),
      ('ocular',['Bijudama','BijudamaCargada','Francotirador','RafagaOcular'],230,True,'JURA | Bijudamas desde el ojo y disparo francotirador',0),
      ('despertar',['awakening'],850,True,'ABAJO + PAUSA | Amplificacion del Juubi durante 12 segundos',0),
      ('garras',['Marca','SalidaGarra'],230,True,'GARRAS | Colocar, viajar y salir atacando; retroceso con abajo + RT',0),
      ('ultimate',['ultimate'],420,True,'A: BIJUDAMA DEL DIEZ COLAS | Inicio esquivable y dano limitado',0),
      ('carga',['charge'],210,True,'CARGA | Chakra verde animado, ondas de presion y sonido del motor',0)]
JOBS.sort(key=lambda j:0 if j[0]=='ultimate' else 1)
runtime=hashlib.sha256(b''.join((ROOT/'Jura'/n).read_bytes() for n in ['Jura.def','Jura.sff','Jura.snd','Jura.air','Jura.cns','Jura.cmd','common1.cns'])).hexdigest()
cachepath=OUT/'Jura_capture_checkpoint.json';cache=json.loads(cachepath.read_text()) if cachepath.exists() else {};cache=cache if cache.get('runtime_sha256')==runtime else dict(runtime_sha256=runtime,jobs={})
reports=[]
with tempfile.TemporaryDirectory(prefix='jura-video-') as temp:
    for name,cases,ticks,record,caption,form in JOBS:
        video=OUT/f'Jura_{name}_motor.mp4';gif=video.with_suffix('.gif');cached=cache['jobs'].get(name)
        if cached and video.exists() and hashlib.sha256(video.read_bytes()).hexdigest()==cached['video_sha256']:
            reports.append(cached['report']);print('REUSE',name,flush=True);continue
        folder=Path(temp)/name;folder.mkdir();raw=folder/'audio.raw';env=os.environ.copy()
        for key in ['JURA_LOW_LIFE','JURA_CPU','JURA_DEBUG']:env.pop(key,None)
        env.update(JURA_CAPTURE=str(folder),JURA_CASES=json.dumps(cases),JURA_TICKS=str(ticks),JURA_FORM=str(form))
        if record:env['JURA_AUDIO']=str(raw)
        else:env.pop('JURA_AUDIO',None)
        result=subprocess.run([sys.executable,str(ROOT/'tools/check_jura_in_engine.py'),ENGINE],env=env,capture_output=True,text=True)
        assert result.returncode==0,result.stdout+result.stderr
        checks=json.loads((OUT/'Jura_capture_checks.json').read_text())
        frames=[tuple(map(int,line.split())) for line in (folder/'frames.tsv').read_text().splitlines()]
        assert len(frames)>20,name
        cues=[tuple(map(int,line.split())) for line in (folder/'audio.tsv').read_text().splitlines()]
        matches=[];audio_args=[]
        if record:
            with wave.open(str(ROOT/('Jura/assets/sound/1_35.wav' if name=='despertar' else 'Jura/assets/sound/1_4.wav' if name=='carga' else 'Jura/assets/sound/1_21.wav'))) as f:
                assert f.getsampwidth()==2
                source=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,f.getnchannels()).mean(axis=1)/32768
                divisor=math.gcd(44100,f.getframerate());cue=resample_poly(source,44100//divisor,f.getframerate()//divisor)
            stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
            cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)]
            norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));score=np.abs(cross)/np.maximum(norm,1e-12)
            peaks,_=find_peaks(score,height=.27,distance=round(.65*44100));assert len(peaks)>=len(cues),(name,len(peaks),len(cues),float(score.max()))
            ticks_sound=np.array([c[0] for c in cues],dtype=float)
            if len(cues)==1:chosen=np.array([peaks[0]])
            else:
                assert len(peaks)<=len(cues)+5,(name,'extra peaks',len(peaks))
                options=[]
                for combo in combinations(peaks,len(cues)):
                    points=np.array(combo)/44100;fit=np.polyfit(ticks_sound,points,1);res=points-np.polyval(fit,ticks_sound)
                    if 1/75<fit[0]<1/45:options.append((float(np.mean(np.abs(res)))-float(np.mean(score[list(combo)]))*.01,np.array(combo)))
                assert options,(name,'sound anchors did not match');chosen=min(options,key=lambda r:r[0])[1]
            anchors=chosen/44100;rate=(anchors[-1]-anchors[0])/(ticks_sound[-1]-ticks_sound[0]) if len(cues)>1 else 1/60
            def at(frame):
                if frame<ticks_sound[0]:return float(anchors[0]+(frame-ticks_sound[0])*rate)
                if frame>ticks_sound[-1]:return float(anchors[-1]+(frame-ticks_sound[-1])*rate)
                return float(np.interp(frame,ticks_sound,anchors))
            matches=[dict(frame=c[0],case=c[1],sample_seconds=float(sample/44100),normalized_correlation=float(score[sample])) for c,sample in zip(cues,chosen)]
        else:
            def at(frame):return frame/60
        start=at(frames[0][1]);end=at(frames[-1][1]+4);duration=end-start
        if record:
            assert start>=0 and end*44100<=len(stereo),(name,start,end,len(stereo)/44100)
            sound=folder/'actual.wav';samples=stereo[round(start*44100):round(end*44100)]
            with wave.open(str(sound),'wb') as f:f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(samples*32768,-32768,32767).astype('<i2').tobytes())
            audio_args=['-i',str(sound)]
        concat=folder/'frames.txt';lines=['ffconcat version 1.0']
        for i,(index,frame,case,tick) in enumerate(frames):
            png=folder/f'Ikemen_GO{index:03d}.png';assert png.exists()
            nxt=frames[i+1][1] if i+1<len(frames) else frame+4
            lines += [f"file '{png}'",'option framerate 60',f'duration {at(nxt)-at(frame):.9f}']
        lines += [f"file '{png}'",'option framerate 60'];concat.write_text('\n'.join(lines)+'\n')
        title=folder/'caption.txt';title.write_text(caption)
        vf=f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=expansion=none:textfile={title}:x=(w-tw)/2:y=690:fontsize=17:fontcolor=white'
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat)]+audio_args+['-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p']+(['-c:a','aac','-b:a','160k'] if record else [])+['-t',str(duration),'-movflags','+faststart',str(video)],check=True)
        if os.environ.get('JURA_GIFS')=='1':
            subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(video),'-filter_complex','[0:v]fps=12,scale=640:-1:flags=neighbor,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none','-loop','0',str(gif)],check=True)
        wanted=100 if name=='despertar' else 130 if name=='ultimate' else 110 if name=='garras' else 60 if name=='carga' else 36 if name=='dash' else 70
        candidates=[f for f in frames if f[2]==0]
        selected=min(candidates,key=lambda r:abs(r[3]-wanted));shutil.copy2(folder/f'Ikemen_GO{selected[0]:03d}.png',video.with_suffix('.png'))
        report=dict(name=name,runtime_sha256=runtime,duration=duration,frames=len(frames),audio='Actual SDL stereo 44100Hz; no offline sound mix' if record else 'Silent sprite-combo recording',activations=matches,combat_checks=checks)
        cache['jobs'][name]=dict(video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),report=report);cachepath.write_text(json.dumps(cache,indent=2)+'\n');reports.append(report)
        print('CAPTURED',name,len(frames),'frames',round(duration,2),'seconds',len(matches),'real sound anchors',flush=True)
(OUT/'Jura_preview_checks.json').write_text(json.dumps(reports,indent=2)+'\n')
print('Actual engine previews completed')
