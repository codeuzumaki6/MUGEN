#!/usr/bin/env python3
"""Import the supplied Sarada atlases/audio and palette-convert the supplied Susanoo."""
from pathlib import Path
import colorsys,hashlib,io,json,plistlib,re,struct,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from build_roster_revision import Archive
from read_sff_v1 import Sff1
from hidari_susanoo_source import ensure_source,actions,frames
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'SaradaTBV';A=CHAR/'assets';SRC=ROOT/'source_material/Sarada_TBV_original/✅SARADA/✅Sprit'
SUS_ACTIONS=[4005,4050,4055,4056,4200,4300,4400,4500,4550,4600,4700,4750,4850,4860,4900,4950,4990,1030]
SCALE=.30
def nums(v):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',v)))
def sha(v):return hashlib.sha256(v).hexdigest()
def main():
 try:import cv2
 except ImportError:sys.path.insert(0,'/tmp/roster-cv');import cv2
 for d in ['frames','sound']:(A/d).mkdir(parents=True,exist_ok=True)
 archive=Archive((ROOT/'DeltaKara/DeltaKara.sff').read_bytes());archive.entries.clear();manifest=[];mapping={};raw={}
 def put(key,g,n,im,axis,**meta):
  dest=A/'frames'/f'{g}_{n}.png';im.save(dest);archive.put((g,n),im,axis);mapping[key]=[g,n]
  manifest.append(dict(key=key,group=g,number=n,file=str(dest.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),redrawn=False,ai_generated=False,**meta))
 for bank,stem in enumerate(['Sarada2','Sarada2_Skill']):
  path=SRC/'Sarada2'/(stem+'.plist');sheet=Image.open(path.with_suffix('.png')).convert('RGBA')
  for key,meta in plistlib.loads(path.read_bytes())['frames'].items():
   x,y,w,h=map(int,nums(meta['frame']))
   if not w or not h:continue
   im=sheet.crop((x,y,x+w,y+h))
   if meta.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
   raw[key]=(im,meta,bank)
 # Body-only originals provide masked templates for the large composites.
 templates=[]
 for key,(im,meta,bank) in raw.items():
  if not re.match(r'Sarada2_(Idle|Walk|Hurt|AirHurt|KnockDown|Natk)_(\d+)$',key):continue
  if '_Natk_' in key and int(key.rsplit('_',1)[1])>11:continue
  v=np.array(im);bb=im.getbbox();ox,oy=nums(meta['offset']);axis=(round(im.width/2-ox),bb[3]-1)
  # Alpha-masked original torso/legs identify the character inside its VFX.
  box=(max(0,axis[0]-18),max(0,axis[1]-75),min(im.width,axis[0]+19),axis[1]+1)
  tile=v[box[1]:box[3],box[0]:box[2]];mask=(tile[:,:,3]>=128).astype('uint8')*255
  templates.append((key,tile,mask,(axis[0]-box[0],axis[1]-box[1])))
 for key,(im,meta,bank) in raw.items():
  ox,oy=nums(meta['offset']);axis=(round(im.width/2-ox),round(im.height/2+oy+45.5));alignment='author horizontal offset and original body match';score=None
  body_only=bool(re.match(r'Sarada2_(Idle|Walk|Hurt|AirHurt|KnockDown|Natk)_(\d+)$',key)) and not ('_Natk_' in key and int(key.rsplit('_',1)[1])>11)
  pure_fx=key.startswith('SaradaEye') or 'Ex' in key or bool(re.match(r'Sarada2_skill0[125]_(\d+)$',key) and (key.startswith('Sarada2_skill01_') and 22<=int(key[-2:])<=30 or key.startswith('Sarada2_skill02_') and int(key[-2:])<=3 or key.startswith('Sarada2_skill05_') and int(key[-2:])>=22))
  if body_only:axis=(axis[0],im.getbbox()[3]-1);alignment='original body lower bound'
  elif pure_fx:axis=(im.width//2,im.height//2);alignment='standalone effect centre'
  else:
   target=np.array(im);best=None
   for name,tile,mask,pivot in templates:
    h,w=tile.shape[:2]
    if h>im.height or w>im.width:continue
    lo=max(0,axis[0]-pivot[0]-30);hi=min(im.width,axis[0]-pivot[0]+w+31)
    if hi-lo<w:continue
    result=cv2.matchTemplate(target[:,lo:hi],tile,cv2.TM_SQDIFF,mask=mask)/float(max(1,(mask>0).sum())*4*255**2)
    result[~np.isfinite(result)]=np.inf;idx=np.unravel_index(np.argmin(result),result.shape);s=float(result[idx])
    if best is None or s<best[0]:best=(s,(int(idx[1])+lo+pivot[0],int(idx[0])+pivot[1]),name)
   if best and best[0]<.19:score=best[0];axis=best[1];alignment='masked original '+best[2]
   else:alignment='sequence anchor reviewed against supplied composite'
  # Strongly illuminated bodies are deliberately obscured by their original
  # effects. Keep their anatomical foot position, never the debris bottom.
  if re.match(r'Sarada2_skill02_\d+',key):
   n=int(key[-2:])
   if 4<=n<=16:axis=(85,126);alignment='consistent original Chidori charge feet'
   if 17<=n<=22:axis=(225,147);alignment='consistent original Chidori dash feet'
  if key.startswith('Sarada2_skill04_') and int(key[-2:])>=14:axis=(415,295);alignment='original crater body feet, not crater bottom'
  if key.startswith('Sarada2_skill05_') and int(key[-2:])<=21:axis=(135,im.getbbox()[3]-1);alignment='original vortex floor with levitating body preserved'
  if key.startswith('Sarada2_Natk_') and int(key[-2:])>=12:
   if im.size==(260,216):axis=(125,177);alignment='consistent original taijutsu effect body pivot'
   else:
    # 15, 19 and 23 are small body-only recovery cells, not the large
    # slash composites. Their own foot pivot prevents a distant second body.
    assert im.size==(80,90),(key,im.size)
    axis=(round(im.width/2-ox),im.getbbox()[3]-1);alignment='original body-only recovery foot pivot'
  if key.startswith('Sarada2_skill03_'):axis=(235,261);alignment='original crouching summoner hand on floor'
  if key.startswith('Sarada2_skill04_'):
   n=int(key[-2:])
   if 1<=n<=5 or 11<=n<=13:axis=(round(im.width/2-ox),im.getbbox()[3]-1);alignment='original Chidori body feet'
   if 6<=n<=10:axis=(165,146);alignment='original Chidori forward stride'
  put(key,26000+bank,sum(p['group']==26000+bank for p in manifest),im,axis,source_plist=str((SRC/'Sarada2'/(('Sarada2' if bank==0 else 'Sarada2_Skill')+'.plist')).relative_to(ROOT)),rectangle=meta['frame'],source_offset=meta['offset'],source_rotated=meta.get('rotated',False),alignment=alignment,match_error=score)
 source=Sff1(ensure_source());acts=actions()
 for g,n in sorted({(g,n) for a in SUS_ACTIONS for g,n,*_ in frames(acts[a]) if g>=0}):
  im,axis=source.image(g,n);v=np.array(im.convert('RGBA'));rgb=v[:,:,:3].astype('uint32');codes=(rgb[:,:,0]<<16)|(rgb[:,:,1]<<8)|rgb[:,:,2];unique,inv=np.unique(codes,return_inverse=True);pal=np.column_stack(((unique>>16)&255,(unique>>8)&255,unique&255)).astype('uint8')
  for i,old in enumerate(pal.copy()):
   hue,sat,val=colorsys.rgb_to_hsv(*(old.astype(float)/255))
   if .68<=hue<=.98 and sat>.12:pal[i]=np.rint(np.array(colorsys.hsv_to_rgb(328/360,sat,val))*255).astype('uint8')
  v[:,:,:3]=pal[inv].reshape(v.shape[0],v.shape[1],3);v[:,:,3][np.max(v[:,:,:3],axis=2)==0]=0
  out=Image.fromarray(v).resize((max(1,round(im.width*SCALE)),max(1,round(im.height*SCALE))),Image.Resampling.LANCZOS)
  put('Susanoo_'+str(g)+'_'+str(n),g+15000,n,out,tuple(round(a*SCALE) for a in axis),source_sasuke=[g,n],source_rgba_sha256=sha(im.tobytes()),palette_hue=328,uniform_scale=SCALE)
 shared=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=shared.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,shared_project_effect=True)
 idle=raw['Sarada2_Idle_01'][0]
 for n,size in [(0,(25,25)),(1,(120,140))]:
  im=idle.crop((14,0,40,29));im.thumbnail(size,Image.Resampling.NEAREST)
  if n:im=im.resize((110,123),Image.Resampling.NEAREST)
  portrait=Image.new('RGBA',size);portrait.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));put(f'Portrait_{n}',9000,n,portrait,(0,0))
 archive.save(CHAR/'SaradaTBV.sff');(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n');(A/'keys.json').write_text(json.dumps(mapping,indent=2)+'\n')
 samples={};b=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',b,16)
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',b,off);samples[g,n]=b[off+16:off+16+size];off=nxt
 soundmap={};audio=[]
 for g,folder in [(2,SRC/'Audio/Effect'),(3,SRC/'Audio/SaradaTBV2')]:
  for n,p in enumerate(sorted(folder.iterdir())):
   if not p.is_file():continue
   dest=A/'sound'/f'{g}_{n}.wav';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-ac','1','-ar','22050','-c:a','pcm_s16le',str(dest)],check=True);samples[g,n]=dest.read_bytes();soundmap[p.stem]=[g,n];audio.append(dict(group=g,number=n,source=str(p.relative_to(ROOT)),source_sha256=sha(p.read_bytes()),wav_sha256=sha(dest.read_bytes())))
 head=bytearray(512);head[:12]=b'ElecbyteSnd\0';head[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',head,16,len(samples),512);parts=[];off=512
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  nxt=off+16+len(wav) if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'SaradaTBV.snd').write_bytes(bytes(head)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=soundmap,source_audio=audio),indent=2)+'\n')
 board=Image.new('RGB',(1200,((len(raw)+7)//8)*135),(34,36,42));draw=ImageDraw.Draw(board)
 for i,(key,(im,_,_)) in enumerate(raw.items()):
  im=im.copy();im.thumbnail((146,105),Image.Resampling.NEAREST);x=i%8*150;y=i//8*135;board.paste(im,(x+(150-im.width)//2,y),im);draw.text((x+2,y+108),key.replace('Sarada2_',''),fill='white')
 board.save(ROOT/'previews/SaradaTBV_original_sprites.jpg');print('Sarada:',len(raw),'original atlas frames;',len(manifest),'total sprites;',len(samples),'sounds')
if __name__=='__main__':main()
