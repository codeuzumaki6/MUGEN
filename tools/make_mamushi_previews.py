#!/usr/bin/env python3
"""Film the actual Mamushi character. Audio is captured from SDL, never mixed."""
from pathlib import Path
from itertools import combinations
import hashlib,json,os,shutil,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews';ENGINE=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
JOBS=[('combos',['Combo a','Combo b','Combo c'],210,False,'X X X / Y Y Y / B B B | Cadenas y remates con los sprites originales'),
      ('especiales',['Brazo','Latigo','Mandibula','Taladro','Maza','Espinas'],210,True,'SEIS ESPECIALES | Abajo adelante / atras + X, Y, B'),
      ('division',['clone_limit'],1040,True,'DIVISION: ABAJO + RT | Seis copias autonomas; prueba con energia repuesta'),
      ('ultimate',['ultimate'],420,True,'A: ENJAMBRE SHINJU | Apertura por colision y ataque de las copias')]
runtime=hashlib.sha256(b''.join((ROOT/'Mamushi'/n).read_bytes() for n in ['Mamushi.def','Mamushi.sff','Mamushi.snd','Mamushi.air','Mamushi.cns','Mamushi.cmd','common1.cns'])).hexdigest()
cachepath=OUT/'Mamushi_capture_checkpoint.json';cache=json.loads(cachepath.read_text()) if cachepath.exists() else {};cache=cache if cache.get('runtime_sha256')==runtime else dict(runtime_sha256=runtime,jobs={})
reports=[]
with tempfile.TemporaryDirectory(prefix='mamushi-video-') as temp:
    for name,cases,ticks,record,caption in JOBS:
        video=OUT/f'Mamushi_{name}_motor.mp4';gif=video.with_suffix('.gif');cached=cache['jobs'].get(name)
        if cached and video.exists() and hashlib.sha256(video.read_bytes()).hexdigest()==cached['video_sha256']:
            reports.append(cached['report']);print('REUSE',name,flush=True);continue
        folder=Path(temp)/name;folder.mkdir();raw=folder/'audio.raw';env=os.environ.copy()
        for key in ['MAMUSHI_LOW_LIFE','MAMUSHI_CLONE_HEALTH_CHECK','MAMUSHI_DEBUG']:env.pop(key,None)
        env.update(MAMUSHI_CAPTURE=str(folder),MAMUSHI_CASES=json.dumps(cases),MAMUSHI_TICKS=str(ticks))
        if record:env['MAMUSHI_AUDIO']=str(raw)
        else:env.pop('MAMUSHI_AUDIO',None)
        result=subprocess.run([sys.executable,str(ROOT/'tools/check_mamushi_in_engine.py'),ENGINE],env=env,capture_output=True,text=True)
        assert result.returncode==0,result.stdout+result.stderr
        checks=json.loads((OUT/'Mamushi_capture_checks.json').read_text())
        frames=[tuple(map(int,line.split())) for line in (folder/'frames.tsv').read_text().splitlines()]
        assert len(frames)>20,name
        cues=[tuple(map(int,line.split())) for line in (folder/'audio.tsv').read_text().splitlines()]
        matches=[];audio_args=[]
        if record:
            with wave.open(str(ROOT/'Mamushi/assets/sound/1_21.wav')) as f:
                cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)
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
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat)]+audio_args+['-vf',vf,'-c:v','libx264','-crf','18','-pix_fmt','yuv420p']+(['-c:a','aac','-b:a','160k'] if record else [])+['-t',str(duration),'-movflags','+faststart',str(video)],check=True)
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(video),'-filter_complex','[0:v]fps=12,scale=640:-1:flags=neighbor,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none','-loop','0',str(gif)],check=True)
        wanted=350 if name=='division' else 130 if name=='ultimate' else 70
        selected=min(frames,key=lambda r:abs(r[3]-wanted));shutil.copy2(folder/f'Ikemen_GO{selected[0]:03d}.png',video.with_suffix('.png'))
        report=dict(name=name,runtime_sha256=runtime,duration=duration,frames=len(frames),audio='Actual SDL stereo 44100Hz; no offline sound mix' if record else 'Silent sprite-combo recording',activations=matches,combat_checks=checks)
        cache['jobs'][name]=dict(video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),report=report);cachepath.write_text(json.dumps(cache,indent=2)+'\n');reports.append(report)
        print('CAPTURED',name,len(frames),'frames',round(duration,2),'seconds',len(matches),'real sound anchors',flush=True)
(OUT/'Mamushi_preview_checks.json').write_text(json.dumps(reports,indent=2)+'\n')
print('Actual engine previews completed')
