#!/usr/bin/env python3
"""Side-by-side same-speed Carniceria recordings; audio from the new build."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
old=OUT/'Pochita_especial_izquierda_b_motor.mp4';new=OUT/'Pochita_largo_especial_izquierda_b_motor.mp4';assert old.is_file() and new.is_file()
with tempfile.TemporaryDirectory(prefix='pochita-comparison-') as temp:
 folder=Path(temp);text=folder/'title.txt';text.write_text('ANTES                                              AHORA: MAS CORTES Y REMATE')
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(old),'-i',str(new),'-filter_complex',f'[0:v]scale=640:360,setsar=1[a];[1:v]scale=640:360,setsar=1[b];[a][b]hstack=inputs=2:shortest=1,pad=1280:400:0:40:black,drawtext=textfile={text}:x=(w-tw)/2:y=10:fontsize=22:fontcolor=white[v]','-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(OUT/'Pochita_CARNICERIA_ANTES_Y_AHORA.mp4')],check=True)
print('Built normal-speed before/after comparison; actual new engine audio')
