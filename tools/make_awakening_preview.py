#!/usr/bin/env python3
"""Capture the actual engine-rendered aura and Daemon approach as GIFs.

Usage: python3 tools/make_awakening_preview.py [/tmp/ikemen-nightly]
"""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parents[1]
engine=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/ikemen-nightly').resolve()
with tempfile.TemporaryDirectory(prefix='eida-capture-') as directory:
    env=os.environ.copy();env['EIDA_CAPTURE']=directory
    subprocess.run([sys.executable,str(root/'tools/check_moves_in_engine.py'),str(engine)],env=env,check=True)
    frames=sorted(Path(directory).glob('Ikemen_GO*.png'))
    assert len(frames)>=40, f'Only {len(frames)} engine frames captured'
    half=len(frames)//2
    for start,count,name in [(0,half,'Daemon_desde_Eida_motor.gif'),(half,len(frames)-half,'Eida_aura_azul_motor.gif')]:
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate','15','-start_number',str(start),'-i',str(Path(directory)/'Ikemen_GO%03d.png'),'-filter_complex',f'[0:v]trim=end_frame={count},scale=768:432:flags=neighbor,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none','-loop','0',str(root/'previews'/name)],check=True)
shutil.copyfile(root/'previews/Eida_aura_azul_motor.gif',root/'previews/Eida_Despertar_Start.gif')
print('Captured Eida aura and Daemon approach directly from Ikemen GO')
