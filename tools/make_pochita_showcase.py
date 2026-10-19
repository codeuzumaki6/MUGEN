#!/usr/bin/env python3
"""Join real engine clips with readable control captions; no drawn gameplay."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
clipspec=[('mixto','X > Y > B: corte, extension y remate'),('persecucion','XXX + ARRIBA > X > Y > B: persecucion aerea'),('cancelaciones','X > Y > ABAJO ADELANTE X > ABAJO ATRAS X: 600 energia'),('embestida','RT: embestida de motosierras')]
with tempfile.TemporaryDirectory(prefix='pochita-showcase-') as directory:
 folder=Path(directory);clips=[]
 for index,(label,caption) in enumerate(clipspec):
  source=ROOT/'previews'/f'Pochita_jugabilidad_{label}_motor.mp4';assert source.is_file()
  clip=folder/f'{index}.mp4';text=folder/f'{index}.txt';text.write_text(caption);clips.append(clip)
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),'-vf',f'drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=textfile={text}:x=(w-tw)/2:y=689:fontsize=23:fontcolor=white','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-ar','22050','-ac','1',str(clip)],check=True)
 listing=folder/'clips.txt';listing.write_text(''.join(f"file '{p}'\n" for p in clips))
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(ROOT/'previews/Pochita_jugabilidad_demostracion.mp4')],check=True)
print('Built four-route showcase from real engine video clips')
