#!/usr/bin/env python3
"""Capture the actual ultimate, with source WAVs aligned to engine state cues.

Audio is mixed offline: the headless engine's audio device is disabled.
The samples and their timings match the CNS. No voice synthesis is used.
"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
engine=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly').resolve()
with tempfile.TemporaryDirectory(prefix='eida-ultimate-') as directory:
    env=os.environ.copy()
    env.update(EIDA_ULTIMATE_CHECK='1',EIDA_CAPTURE=directory,EIDA_CAPTURE_CASES='["ultimatehit"]')
    subprocess.run([sys.executable,str(ROOT/'tools/check_moves_in_engine.py'),str(engine)],env=env,check=True)
    frames=sorted(Path(directory).glob('Ikemen_GO*.png'))
    # The headless renderer may export one fewer image than requested.
    assert 134<=len(frames)<=135,len(frames)
    duration=len(frames)/15
    rows=[list(map(int,line.split('\t'))) for line in (engine/'eida_capture_cues.tsv').read_text().splitlines()]
    start=next(tick for case,tick,state in rows if case==0 and state==3001)
    cast=next(tick for case,tick,state in rows if case==0 and state==3000)
    cinema=(start-12)/60
    sound=ROOT/'Eida/assets/sound'
    tracks=[('charm_cast.wav',(cast-12+2)/60),('voice_ultimate.wav',cinema),
            ('memory_build.wav',cinema+.05),('memory_release.wav',cinema+435/60)]
    tracks += [('memory_transition.wav',cinema+(12+i*70)/60) for i in range(6)]
    command=['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate','15',
             '-i',str(Path(directory)/'Ikemen_GO%03d.png')]
    for filename,_ in tracks:command+=['-i',str(sound/filename)]
    filters=[];labels=[]
    for i,(_,seconds) in enumerate(tracks,1):
        delay=round(seconds*1000);label=f'a{i}';labels.append(f'[{label}]')
        filters.append(f'[{i}:a]adelay={delay}:all=1[{label}]')
    filters.append(''.join(labels)+f'amix=inputs={len(tracks)}:normalize=0,alimiter=limit=.95,atrim=duration={duration}[audio]')
    command+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[audio]',
              '-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',
              '-t',str(duration),'-movflags','+faststart',str(ROOT/'previews/Omnipotencia_motor_HD.mp4')]
    subprocess.run(command,check=True)
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate','15',
        '-i',str(Path(directory)/'Ikemen_GO%03d.png'),'-filter_complex',
        '[0:v]fps=10,scale=640:360:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=none',
        '-loop','0',str(ROOT/'previews/Omnipotencia_motor_HD.gif')],check=True)
print('Saved engine cinematic and MP4 with cue-aligned source audio')
