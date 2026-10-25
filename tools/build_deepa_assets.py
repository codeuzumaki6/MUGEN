#!/usr/bin/env python3
"""Import the supplied Deepa originals; exclude unrelated donor characters."""
from pathlib import Path
import hashlib,json,plistlib,re,struct,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from build_roster_revision import Archive
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'DeepaKara';A=CHAR/'assets';SRC=ROOT/'source_material/Deepa_original/DEEPA/Deepa Kara by VayDra'
def nums(s):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',s)))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 try:import cv2
 except ImportError:sys.path.insert(0,'/tmp/roster-cv');import cv2
 for d in ['frames','sound']:(A/d).mkdir(parents=True,exist_ok=True)
 raw={};excluded=[]
 for rel in ['Kinkaku/Kinkaku.plist','Kinkaku/Kinkaku_Skill.plist','Flog/KakashiFlog.plist']:
  p=SRC/rel;data=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA')
  for key,m in data['frames'].items():
   if key.startswith('KakashiFlog_'):excluded.append(key);continue
   x,y,w,h=map(int,nums(m['frame']))
   if not w or not h:continue
   im=sheet.crop((x,y,x+w,y+h))
   if m.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
   if not im.getbbox():continue
   raw[key]=(im,m,p,1 if key.startswith('Deepa_') else 0)
 archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries.clear();manifest=[];mapping={}
 def put(key,g,n,im,axis,**meta):
  dest=A/'frames'/f'{g}_{n}.png';im.save(dest);archive.put((g,n),im,axis);mapping[key]=[g,n];manifest.append(dict(key=key,group=g,number=n,file=str(dest.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),redrawn=False,ai_generated=False,**meta))
 templates={0:[],1:[]}
 def opaque(im):return Image.fromarray((np.array(im.getchannel('A'))>=128).astype('uint8')*255).getbbox()
 for key,(im,m,p,form) in raw.items():
  eligible=key.startswith('Kinkaku_NAttack_') or key=='Kinkaku_Idle_01' or key in ['Deepa_Idle','Deepa_UnUse_01','Deepa_Hit01_07','Deepa_Hit02_07','Deepa_Trans_09']
  if not eligible:continue
  ox,oy=nums(m['offset']);bb=opaque(im);axis=(round(im.width/2-ox),bb[3]-1);v=np.array(im)
  box=(max(0,axis[0]-24),max(0,axis[1]-94),min(im.width,axis[0]+25),axis[1]+1);tile=v[box[1]:box[3],box[0]:box[2]]
  rgb=tile[:,:,:3].astype(float);cloth=(rgb[:,:,0]>55)&(rgb[:,:,0]>rgb[:,:,1]*1.25)&(rgb[:,:,2]>rgb[:,:,1]*1.15)&(tile[:,:,3]>=128)
  mask=cloth.astype('uint8')*255
  if cloth.sum()<40:mask=(tile[:,:,3]>=128).astype('uint8')*255
  templates[form].append((key,tile,mask,(axis[0]-box[0],axis[1]-box[1])))
 for key,(im,m,p,form) in raw.items():
  ox,oy=nums(m['offset']);bb=opaque(im);axis=(round(im.width/2-ox),bb[3]-1);kind='body';method='native body foot pivot';score=None
  pure='Mon' in key or key in ['Kinkaku_Float_02','Kinkaku_Float_03','Kinkaku_KnockDown_04','Kinkaku_KnockDown_05']
  if pure:axis=(im.width//2,im.height//2);kind='effect';method='standalone original effect centre'
  elif key.startswith('Deepa_Trans_') and key!='Deepa_Trans_09':axis=(im.width//2,bb[3]-1);kind='transformation';method='original transformation ground plane'
  elif im.width>180 or im.height>140:
   kind='body_with_effect';target=np.array(im);best=None
   for name,tile,mask,pivot in templates[form]:
    h,w=tile.shape[:2]
    if h>im.height or w>im.width:continue
    lo=max(0,axis[0]-pivot[0]-30);hi=min(im.width,axis[0]-pivot[0]+w+31)
    if hi-lo<w:continue
    res=cv2.matchTemplate(target[:,lo:hi],tile,cv2.TM_SQDIFF,mask=mask)/float(max(1,(mask>0).sum())*4*255**2);res[~np.isfinite(res)]=np.inf;idx=np.unravel_index(np.argmin(res),res.shape);s=float(res[idx])
    if best is None or s<best[0]:best=(s,(int(idx[1])+lo+pivot[0],int(idx[0])+pivot[1]),name)
   if best and best[0]<.025:score=best[0];axis=best[1];method='masked original cloth match '+best[2]
   else:axis=(axis[0],round(im.height/2+oy+48));method='source horizontal offset and original foot baseline';score=best[0] if best else None
  if key.startswith('Kinkaku_Skill03_Punch_'):axis=(60,165);method='original rushing body feet, independent of fist flash'
  if key.startswith('Deepa_Hit01_') and im.width>180:axis=(180,221);method='original armored left punch body feet'
  if key.startswith('Deepa_Hit02_') and im.width>180:axis=(233,210);method='original armored right punch body feet'
  put(key,28000+form,sum(p['group']==28000+form for p in manifest),im,axis,form=form,kind=kind,alignment=method,match_error=score,source_plist=str(p.relative_to(ROOT)),rectangle=m['frame'],source_offset=m['offset'],source_rotated=m.get('rotated',False))
 # The original large cube is separate from the hand. Crop only its pixels;
 # travelling helpers never contain a second copy of Deepa's body.
 im=raw['Kinkaku_Skill04_01'][0];cube=im.crop((70,0,im.width,im.height));bb=cube.getbbox();cube=cube.crop(bb)
 put('Carbon_Cube',28002,0,cube,(cube.width//2,cube.height//2),kind='effect',source_key='Kinkaku_Skill04_01',source_rectangle=[70+bb[0],bb[1],70+bb[2],bb[3]])
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 for n,size in [(0,(25,25)),(1,(120,140))]:
  im=raw['Kinkaku_Idle_01'][0].crop((10,0,39,33));im=im.resize((25,25) if n==0 else (110,125),Image.Resampling.NEAREST);out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));put(f'Portrait_{n}',9000,n,out,(0,0),kind='portrait')
 archive.save(CHAR/'DeepaKara.sff');(A/'keys.json').write_text(json.dumps(mapping,indent=2)+'\n');(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n')
 b=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',b,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',b,off);samples[g,n]=b[off+16:off+16+size];off=nxt
 smap={};audio=[]
 for g,folder in [(2,SRC/'Audio/Effect'),(3,SRC/'Audio/Deepa')]:
  for n,p in enumerate(sorted(folder.iterdir())):
   if not p.is_file():continue
   dest=A/'sound'/f'{g}_{n}.wav';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-ac','1','-ar','22050','-c:a','pcm_s16le',str(dest)],check=True);samples[g,n]=dest.read_bytes();smap[p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=sha(p.read_bytes()),group=g,number=n))
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',header,16,len(samples),512);off=512;parts=[]
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  nxt=off+16+len(wav) if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'DeepaKara.snd').write_bytes(bytes(header)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=smap,source_audio=audio),indent=2)+'\n');(A/'excluded_donor_frames.json').write_text(json.dumps(excluded,indent=2)+'\n')
 board=Image.new('RGB',(1200,((len(raw)+7)//8)*135),(35,38,43));draw=ImageDraw.Draw(board)
 for i,(key,(im,_,_,_)) in enumerate(raw.items()):
  im=im.copy();im.thumbnail((146,105),Image.Resampling.NEAREST);x=i%8*150;y=i//8*135;board.paste(im,(x+(150-im.width)//2,y),im);draw.text((x+1,y+108),key.replace('Kinkaku_',''),fill='white')
 board.save(ROOT/'previews/DeepaKara_original_sprites.jpg');print('Deepa assets:',len(raw),'original frames;',len(manifest),'sprites;',len(samples),'sounds;',len(excluded),'unrelated donor frames excluded')
if __name__=='__main__':main()
