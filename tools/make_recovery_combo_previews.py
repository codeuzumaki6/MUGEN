#!/usr/bin/env python3
"""Record actual knockdown recovery, Daemon branches and air pursuit."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
engine=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly').resolve()

def record(cases,recovery=False):
    with tempfile.TemporaryDirectory(prefix='eida-recovery-combos-') as directory:
        env=os.environ.copy()
        env.update(EIDA_CAPTURE=directory,EIDA_CAPTURE_CASES=json.dumps([name for name,_ in cases]))
        if recovery:env['EIDA_RECOVERY_CHECK']='1'
        subprocess.run([sys.executable,str(ROOT/'tools/check_moves_in_engine.py'),str(engine)],env=env,check=True)
        frames=sorted(Path(directory).glob('Ikemen_GO*.png'))
        per_case=63 if recovery else 35
        assert per_case*len(cases)-1<=len(frames)<=per_case*len(cases),len(frames)
        for i,(_,name) in enumerate(cases):
            count=min(per_case,len(frames)-i*per_case)
            subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate','15',
                '-start_number',str(i*per_case),'-i',str(Path(directory)/'Ikemen_GO%03d.png'),
                '-filter_complex',f'[0:v]trim=end_frame={count},scale=768:432:flags=neighbor,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none',
                '-loop','0',str(ROOT/'previews'/name)],check=True)

record([('Recovery bounce','Eida_se_levanta_motor.gif')],recovery=True)
record([('Daemon branch b a','Eida_Y_X_Daemon_motor.gif'),
        ('Daemon branch c b','Eida_B_Y_Daemon_motor.gif'),
        ('Charm into Daemon','Eida_encanto_Daemon_motor.gif'),
        ('Natural launcher pursuit','Eida_persecucion_aerea_motor.gif'),
        ('Senrigan','Eida_Senrigan_Daemon_motor.gif')])
print('Saved six real-engine recovery/combo previews')
