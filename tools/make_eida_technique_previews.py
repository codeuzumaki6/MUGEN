#!/usr/bin/env python3
"""Prove every activation in real SDL audio and film the sprite embrace."""
from pathlib import Path
import hashlib,json,os,shutil,struct,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,resample_poly,find_peaks
from itertools import combinations
from build_moveset import MOVES
from check_eida_compact_scene import inspect_compact_scene
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
engine=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
jobs=[('especiales',[m[0] for m in MOVES],False,False),('senrigan_sin_ataque',['Senrigan sin ataque'],False,True),('omnipotencia_abrazo',['ultimatehit'],True,False)]
daemon_review=os.environ.get('EIDA_DAEMON_MODEL_REVIEW')=='1'
if daemon_review:
    jobs=[('daemon_modelo',['DaemonRapido','DaemonCombo','DaemonEleva','DaemonPatadas','DaemonBarrido','AsaltoDoble'],False,False)]
reports=[]
runtime=hashlib.sha256(b''.join((ROOT/'Eida'/n).read_bytes() for n in ['Eida.cns','Specials.cns','Omnipotencia.cns','Eida.air','Eida.sff','Eida.snd','Eida.cmd'])).hexdigest()
checkpoint_path=OUT/('Eida_Daemon_modelo_capture_checkpoint.json' if daemon_review else 'Eida_technique_capture_checkpoint.json')
checkpoint=json.loads(checkpoint_path.read_text()) if checkpoint_path.exists() else {}
def scope_hash(name):
    if name=='omnipotencia_abrazo':return runtime
    digest=hashlib.sha256()
    for n in ['Eida.cns','Specials.cns','Eida.snd','Eida.cmd','common1.cns','Eida.def']:
        digest.update((ROOT/'Eida'/n).read_bytes())
    import re
    digest.update(re.sub(rb'(?ims)^\[Begin Action 86\d{2}\].*?(?=^\[Begin Action|\Z)',b'',(ROOT/'Eida/Eida.air').read_bytes()).rstrip())
    # Hash actual decoded SFF records, excluding the ultimate-only group.
    b=(ROOT/'Eida/Eida.sff').read_bytes();sh,count,ph,_,data=struct.unpack_from('<IIIII',b,36)
    for i in range(count):
        g,no,w,h,x,y,link,fmt,depth,offset,size,pal,flags=struct.unpack_from('<HHHHhhHBBIIHH',b,sh+i*28)
        if 8600<=g<8700:continue
        _,_,_,_,po,ps=struct.unpack_from('<HHHHII',b,ph+pal*16)
        digest.update(struct.pack('<HHHHhh',g,no,w,h,x,y));digest.update(b[data+offset:data+offset+size]);digest.update(b[data+po:data+po+ps])
    return digest.hexdigest()
if checkpoint.get('runtime_sha256')==runtime:
    for name,entry in checkpoint.get('jobs',{}).items():entry.setdefault('scope_sha256',scope_hash(name))
else:
    checkpoint=dict(runtime_sha256=runtime,jobs={name:entry for name,entry in checkpoint.get('jobs',{}).items() if entry.get('scope_sha256')==scope_hash(name)})
checkpoint_path.write_text(json.dumps(checkpoint,indent=2)+'\n')
with tempfile.TemporaryDirectory(prefix='eida-technique-video-') as temp:
    for name,names,ultimate,idle in jobs:
        clip=OUT/f'Eida_{name}_nuevo_motor.mp4';cached=checkpoint['jobs'].get(name)
        if cached and clip.exists() and hashlib.sha256(clip.read_bytes()).hexdigest()==cached['video_sha256']:
            reports.append(cached['report']);print('REUSE',name,flush=True);continue
        folder=Path(temp)/name;folder.mkdir();raw=folder/'audio.raw';env=os.environ.copy()
        for key in ['EIDA_ULTIMATE_CHECK','EIDA_RECOVERY_CHECK','EIDA_CAPTURE','EIDA_SENRIGAN_IDLE_CHECK']:env.pop(key,None)
        env.update(EIDA_LIVE_CAPTURE=str(folder),EIDA_RECORD_AUDIO=str(raw),EIDA_REVIEW_FACING='1',EIDA_TEST_CASES=json.dumps(names))
        if ultimate:env['EIDA_ULTIMATE_CHECK']='1'
        if idle:env['EIDA_SENRIGAN_IDLE_CHECK']='1'
        run=subprocess.run([sys.executable,str(ROOT/'tools/check_moves_in_engine.py'),engine],env=env,capture_output=True,text=True)
        assert run.returncode==0,run.stdout+run.stderr
        checks=json.loads((OUT/'Eida_live_review_checks.json').read_text())
        frames=[tuple(map(int,l.split())) for l in (folder/'frames.tsv').read_text().splitlines()]
        trace=[list(map(float,l.split())) for l in (folder/'trace.tsv').read_text().splitlines()]
        cues=[tuple(map(int,l.split())) for l in (folder/'audio.tsv').read_text().splitlines()]
        assert len(cues)==len(names),(name,cues)
        compact_review=None
        if ultimate:
            compact_review=inspect_compact_scene(ROOT/'Eida',trace)
            # The combat fixture continues long enough to test a missed or
            # confirmed ultimate. The review video ends shortly after this
            # confirmed scene actually returns to idle, rather than showing
            # the old nine-second fixture's empty tail.
            end_frame=compact_review['engine_trace']['returned_idle_frame']+20
            frames=[p for p in frames if p[1]<=end_frame]
        with wave.open(str(ROOT/'Eida/assets/sound/special_activation.wav')) as f:
            cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)
        stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
        cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)]
        norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));score=np.abs(cross)/np.maximum(norm,1e-12)
        peaks,_=find_peaks(score,height=.28,distance=round(.85*44100));assert len(peaks)>=len(cues),(name,len(peaks),len(cues),float(score.max()))
        # SDL disk buffering and screenshot rendering use independent clocks.
        # Match one recorded waveform per cast, in order, then synchronize the
        # images at those actual sound anchors. Never remix or stretch audio.
        ticks=np.array([c[0] for c in cues],dtype=float)
        if len(cues)==1:chosen=np.array([peaks[np.argmax(score[peaks])]])
        else:
            assert len(peaks)<=len(cues)+4,(name,'unexpected extra activation waveforms',len(peaks))
            candidates=[]
            for combo in combinations(peaks,len(cues)):
                points=np.array(combo)/44100;fit=np.polyfit(ticks,points,1);residual=points-np.polyval(fit,ticks)
                if 1/75<fit[0]<1/45:candidates.append((float(np.mean(np.abs(residual)))-float(np.mean(score[list(combo)]))*.01,np.array(combo)))
            assert candidates,(name,'waveforms did not match the command sequence',list(peaks/44100),list(ticks))
            chosen=min(candidates,key=lambda p:p[0])[1]
        anchor_seconds=chosen/44100
        rate=(anchor_seconds[-1]-anchor_seconds[0])/(ticks[-1]-ticks[0]) if len(ticks)>1 else 1/60
        def audio_time(frame):
            if frame<ticks[0]:return float(anchor_seconds[0]+(frame-ticks[0])*rate)
            if frame>ticks[-1]:return float(anchor_seconds[-1]+(frame-ticks[-1])*rate)
            return float(np.interp(frame,ticks,anchor_seconds))
        matches=[(int(p),float(score[p]),float(p/44100-(anchor_seconds[0]+(tick-ticks[0])*rate))) for p,tick in zip(chosen,ticks)]
        start=audio_time(frames[0][1]);assert start>=0
        activations=[]
        for (tick,idx,_),(sample,confidence,error) in zip(cues,matches):
            rows=[r for r in trace if int(r[1])==idx]
            if not ultimate:
                assert max(r[5] for r in rows)>0 and max(r[6] for r in rows)>0,(name,idx,'activation FX absent')
                assert all(r[5]==0 and r[6]==0 for r in rows[-10:]),(name,idx,'activation did not expire')
            if idle:assert not any(r[9]>0 for r in rows) and all(r[8]==0 for r in rows if r[3]==1200 and r[4]>48)
            activations.append(dict(case=checks[idx]['case']['name'],state=checks[idx]['case']['state'],cue_frame=tick,actual_sample_seconds=sample/44100,normalized_correlation=confidence,timing_error_seconds=error))
        if ultimate:
            assert any(r[7]>0 for r in trace),'embrace absent'
            assert all(r[7]==0 for r in trace if r[3]==3001 and r[4]>=130),'embrace did not clear'
        first=round(start*44100);duration=audio_time(frames[-1][1]+4)-start;last=first+round(duration*44100)
        if last>len(stereo):
            assert (last-len(stereo))/44100<.35
            frames=[p for p in frames if audio_time(p[1]+4)<=len(stereo)/44100]
            duration=audio_time(frames[-1][1]+4)-start;last=first+round(duration*44100)
        assert last<=len(stereo) and len(frames)>=25,(name,len(frames),last,len(stereo))
        audio=stereo[first:last];wav=folder/'actual.wav'
        with wave.open(str(wav),'wb') as f:f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(audio*32768,-32768,32767).astype('<i2').tobytes())
        listing=folder/'frames.txt';lines=['ffconcat version 1.0']
        for i,(index,tick) in enumerate(frames):
            path=folder/f'Ikemen_GO{index:03d}.png';assert path.exists();following=frames[i+1][1] if i+1<len(frames) else tick+4
            lines += [f"file '{path}'",'option framerate 60',f'duration {audio_time(following)-audio_time(tick):.9f}']
        lines += [f"file '{path}'",'option framerate 60'];listing.write_text('\n'.join(lines)+'\n')
        caption=folder/'caption.txt'
        caption.write_text('DAEMON | Modelo original, poses de apoyo y seis ataques en el motor' if daemon_review else 'A: OMNIPOTENCIA | Dos sprites originales, abrazo compacto y liberacion' if ultimate else 'ABAJO + ATRAS + Y: SENRIGAN | Espera un golpe; sin golpe no hay contraataque' if idle else '14 JUTSUS | Activacion, sonido y combate capturados del motor')
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-i',str(wav),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=expansion=none:textfile={caption}:x=(w-tw)/2:y=689:fontsize=19:fontcolor=white','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(clip)],check=True)
        if ultimate or idle or daemon_review:
            subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(clip),'-filter_complex','[0:v]fps=12,scale=640:-1:flags=neighbor,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none','-loop','0',str(clip.with_suffix('.gif'))],check=True)
        thumbnail=compact_review['engine_trace']['thumbnail_frame'] if ultimate else cues[0][0]+42 if daemon_review else cues[0][0]+5
        chosen=min(frames,key=lambda p:abs(p[1]-thumbnail));shutil.copy2(folder/f'Ikemen_GO{chosen[0]:03d}.png',clip.with_suffix('.png'))
        report=dict(name=name,runtime_sha256=runtime,frames=len(frames),duration=duration,audio_source='Actual SDL stereo S16LE 44100 Hz output; no offline mix',image_sync='Piecewise synchronization to each actual activation waveform; audio is neither remixed nor time-stretched',activations=activations,combat_checks=checks,raw_audio_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),near_full_scale_fraction=float(np.mean(np.abs(audio)>.999)))
        if compact_review:
            report['compact_scene_checks']=compact_review
            (OUT/'Eida_compact_scene_checks.json').write_text(json.dumps(compact_review,indent=2)+'\n')
        reports.append(report);checkpoint['jobs'][name]=dict(video_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),report=report)
        checkpoint['jobs'][name]['scope_sha256']=scope_hash(name)
        checkpoint_path.write_text(json.dumps(checkpoint,indent=2)+'\n');print(name,'PASS',len(activations),'actual activation samples,',len(frames),'frames',flush=True)
(OUT/('Eida_Daemon_modelo_audio_checks.json' if daemon_review else 'Eida_technique_audio_checks.json')).write_text(json.dumps(reports,indent=2)+'\n')
(OUT/'Eida_live_review_checks.json').write_text(json.dumps([case for report in reports for case in report['combat_checks']],indent=2)+'\n')
print('Daemon model recorded with six real activations and actual audio' if daemon_review else 'All activations, counter whiff and Kawaki embrace recorded with actual audio')
