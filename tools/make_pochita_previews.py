#!/usr/bin/env python3
"""Capture each real engine scenario separately; GIFs have no audio track."""
from pathlib import Path
import os,sys,subprocess,tempfile,json,re
ROOT=Path(__file__).resolve().parents[1]
engine=sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly'
reports=[]
for label,case in [('combo','Combo X'),('carniceria','Carniceria'),('ultimate','ultihit'),('recuperacion','Get up bounce')]:
 with tempfile.TemporaryDirectory(prefix='pochita-preview-') as directory:
  env=os.environ.copy();env['POCHITA_CAPTURE']=directory;env['POCHITA_CAPTURE_CASES']=json.dumps([case])
  r=subprocess.run([sys.executable,str(ROOT/'tools/check_pochita_in_engine.py'),engine],env=env,capture_output=True,text=True)
  assert r.returncode==0,r.stdout+r.stderr
  reports+=json.loads((ROOT/'previews/Pochita_engine_visual_checks.json').read_text())
  frames=sorted(Path(directory).glob('*.png'),key=lambda p:int(re.search(r'(\d+)\.png$',p.name)[1]))
  assert len(frames)>=45,(case,len(frames))
  # Separate runs prevent a dropped capture from mixing two attacks in a GIF.
  for i,p in enumerate(frames):p.rename(Path(directory)/f'frame_{i:04d}.png')
  target=ROOT/'previews'/f'Pochita_rediseno_{label}_motor.gif'
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate','15','-i',directory+'/frame_%04d.png','-filter_complex','[0:v]scale=640:-1:flags=neighbor,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(target)],check=True)
  print(label,len(frames),'engine captures',target.stat().st_size,'bytes',flush=True)
(ROOT/'previews/Pochita_engine_visual_checks.json').write_text(json.dumps(reports,indent=2)+'\n')
