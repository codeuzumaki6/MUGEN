#!/usr/bin/env python3
"""Record Eida's own combo/charm/dash in the engine, not the reference video."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
engine=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly').resolve()
cases=[('X chain','Eida_combo_revision_video.gif'),
       ('Encantamiento','Eida_encanto_confirmado_motor.gif'),
       ('Forward dash and attack','Eida_dash_motor.gif')]
if os.environ.get('EIDA_EXPANDED_PREVIEW')=='1':
    cases=[('Mixed X b','Eida_combo_mixto_motor.gif'),
           ('AperturaCombinada','Eida_apertura_combinada_motor.gif'),
           ('EncantoDoble','Eida_doble_encanto_motor.gif'),
           ('PasoSenrigan','Eida_paso_senrigan_motor.gif')]
with tempfile.TemporaryDirectory(prefix='eida-video-review-') as directory:
    env=os.environ.copy()
    env.update(EIDA_CAPTURE=directory,EIDA_CAPTURE_CASES=json.dumps([name for name,_ in cases]))
    subprocess.run([sys.executable,str(ROOT/'tools/check_moves_in_engine.py'),str(engine)],env=env,check=True)
    frames=sorted(Path(directory).glob('Ikemen_GO*.png'))
    # 12..148 ticks, sampled every 4 ticks, for every selected scenario.
    assert 35*len(cases)-1<=len(frames)<=35*len(cases),f'Unexpected capture count: {len(frames)}'
    for i,(_,filename) in enumerate(cases):
        count=min(35,len(frames)-i*35)
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error',
            '-framerate','15','-start_number',str(i*35),'-i',str(Path(directory)/'Ikemen_GO%03d.png'),
            '-filter_complex',f'[0:v]trim=end_frame={count},scale=768:432:flags=neighbor,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none',
            '-loop','0',str(ROOT/'previews'/filename)],check=True)
print(f'Saved {len(cases)} actual engine captures in previews/')
