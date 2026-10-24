#!/usr/bin/env python3
"""Original Sasuke BTM Susanoo art, palette-only yellow conversion and AIR frames."""
from pathlib import Path
import colorsys,hashlib,json,re
import numpy as np
from PIL import Image,ImageDraw
from read_sff_v1 import Sff1
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'source_material/Sasuke_BTM_original'
ACTION_IDS=[4005,4050,4055,4056,4200,4300,4400,4500,4550,4600,4700,4750,4800,4850,4860,4900,4950,4990,1030,1450,1470,1480,1485]
SCALE=.30

def ensure_source():
 path=SOURCE/'Sasuke_BTM.sff'
 if not path.exists():
  from zipfile import ZipFile
  with ZipFile(SOURCE/'Sasuke_BTM_sprites.zip') as z:
   name=next(n for n in z.namelist() if Path(n).name=='Sasuke_BTM.sff');path.write_bytes(z.read(name))
 return path

def actions():
 text=(SOURCE/'Sasuke_BTM.air').read_text(encoding='latin1');heads=list(re.finditer(r'(?im)^\[Begin Action (\d+)\]',text));return {int(m[1]):text[m.end():heads[i+1].start() if i+1<len(heads) else len(text)] for i,m in enumerate(heads)}
def frames(block):
 out=[]
 for line in block.splitlines():
  m=re.match(r'\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)(.*)',line)
  if m:out.append((*map(int,m.groups()[:5]),m[6]))
 return out

def recolor(im):
 v=np.array(im.convert('RGBA'));rgb=v[:,:,:3].astype(np.uint32);keys=(rgb[:,:,0]<<16)|(rgb[:,:,1]<<8)|rgb[:,:,2];unique,inverse=np.unique(keys,return_inverse=True);palette=np.column_stack(((unique>>16)&255,(unique>>8)&255,unique&255)).astype('uint8')
 for i,old in enumerate(palette.copy()):
  h,s,val=colorsys.rgb_to_hsv(*(old.astype(float)/255))
  if .70<=h<=.96 and s>.12:palette[i]=np.rint(np.array(colorsys.hsv_to_rgb(54/360,s,val))*255).astype('uint8')
 v[:,:,:3]=palette[inverse].reshape(v.shape[0],v.shape[1],3);v[:,:,3][np.max(v[:,:,:3],axis=2)==0]=0
 return Image.fromarray(v)

def export_assets(put):
 source=Sff1(ensure_source());acts=actions();keys=sorted({(g,n) for a in ACTION_IDS for g,n,x,y,t,tail in frames(acts[a]) if g>=0});manifest=[]
 for g,n in keys:
  im,axis=source.image(g,n);out=recolor(im);put(g+10000,n,out,axis,source_sasuke=[g,n],source_axis=axis,source_rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest(),palette_only_yellow=True,redrawn=False,ai_generated=False)
  manifest.append(dict(source=[g,n],packed=[g+10000,n],axis=axis,source_rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest(),yellow_rgba_sha256=hashlib.sha256(out.tobytes()).hexdigest()))
 (ROOT/'HidariShinju/assets/susanoo_source.json').write_text(json.dumps(dict(author='Shingeki No Mugen; Susanoo sprites credited to Vovan99',source_sff_sha256=hashlib.sha256((SOURCE/'Sasuke_BTM.sff').read_bytes()).hexdigest(),palette_hue_degrees=54,shape_and_animation_preserved=True,ai_generated=False,actions=ACTION_IDS,sprites=manifest),indent=2)+'\n')
 samples=[(4090,n) for n in [0,1,11,12,13,15,17,19,24,25]]+[(4091,n) for n in range(8)]
 board=Image.new('RGB',(1200,((len(samples)+5)//6)*220),(22,27,38));d=ImageDraw.Draw(board)
 for i,k in enumerate(samples):
  im,_=source.image(*k);im=recolor(im);im.thumbnail((195,190),Image.Resampling.NEAREST);board.paste(im,(i%6*200+(200-im.width)//2,i//6*220),im);d.text((i%6*200,i//6*220+195),str(k),fill='white')
 board.save(ROOT/'previews/HidariShinju_susanoo_sasuke_sprites.png');return len(keys)

def export_action(a,scale=SCALE,loop=False,box=None):
 block=actions()[a];out=[f'\n[Begin Action {20000+a}]']
 if box:out+=['Clsn1Default: 1',f' Clsn1[0]={box}']
 if loop:out+=['Loopstart']
 ignore=0
 for line in block.splitlines():
  line=line.split(';',1)[0].strip()
  if not line:continue
  if re.match(r'(?i)^Clsn2',line):continue
  if re.match(r'(?i)^Clsn1(?:Default)?\s*:',line):
   if not box:out.append(line)
  elif (m:=re.match(r'(?i)^Clsn1\[(\d+)\]\s*=\s*(.*)',line)):
   if not box:out.append(' Clsn1['+m[1]+']='+','.join(str(round(float(x)*scale)) for x in m[2].split(',')))
  elif (fs:=frames(line)):
   g,n,x,y,t,tail=fs[0]
   if g>=0:out.append(f'{g+10000},{n},{round(x*scale)},{round(y*scale)},{t}{tail}')
  elif line.lower()=='loopstart' and not loop:out.append('Loopstart')
 return '\n'.join(out)+'\n'
