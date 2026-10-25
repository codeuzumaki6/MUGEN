#!/usr/bin/env python3
"""Import the supplied Ouga / Yatsume originals, preserving both outfits and puppet artwork."""
from pathlib import Path
import hashlib,json,plistlib,re,struct,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from build_roster_revision import Archive
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'OugaYatsume';A=CHAR/'assets';SRC=ROOT/'source_material/Ouga_original/Ouga Yatsume By Vaydra'
def nums(s):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',s)))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 try:import cv2
 except ImportError:sys.path.insert(0,'/tmp/roster-cv');import cv2
 for d in ['frames','sound']:(A/d).mkdir(parents=True,exist_ok=True)
 raw={};excluded=[]
 for rel in ['Kiba/Kiba.plist','Akamaru/Akamaru.plist']:
  p=SRC/rel;data=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA')
  for key,m in data['frames'].items():
   x,y,w,h=map(int,nums(m['frame']))
   if not w or not h:excluded.append(key);continue
   im=sheet.crop((x,y,x+w,y+h))
   if m.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
   if not im.getbbox():excluded.append(key);continue
   raw[key]=(im,m,p)
 archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries.clear();manifest=[];mapping={}
 def put(key,g,n,im,axis,**meta):
  dest=A/'frames'/f'{g}_{n}.png';im.save(dest);archive.put((g,n),im,axis);mapping[key]=[g,n];manifest.append(dict(key=key,group=g,number=n,file=str(dest.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),redrawn=False,ai_generated=False,**meta))
 def bbox(im):return Image.fromarray((np.array(im.getchannel('A'))>=128).astype('uint8')*255).getbbox() or im.getbbox()
 def outfit(k):
  return 0 if k.startswith(('Kiba_Idle_','Kiba_Walk_','Kiba_NAttack2_','Kiba_Skill05_','Kiba_Skill06_')) else 1
 templates={0:[],1:[]}
 for key,(im,m,p) in raw.items():
  if not (key.startswith(('Kiba_NAttack','Kiba_Skill01_','Kiba_Run_')) or key=='Kiba_Idle_001'):continue
  ox,oy=nums(m['offset']);axis=(round(im.width/2-ox),bbox(im)[3]-1);v=np.array(im);form=outfit(key)
  box=(max(0,axis[0]-23),max(0,axis[1]-77),min(im.width,axis[0]+24),axis[1]+1);tile=v[box[1]:box[3],box[0]:box[2]];rgb=tile[:,:,:3].astype(float)
  cloth=((rgb.max(2)<90)&(rgb.max(2)>15)) if form==0 else ((rgb[:,:,1]>70)&(rgb[:,:,1]>rgb[:,:,0]*1.1)&(rgb[:,:,2]>rgb[:,:,0]*1.1))
  mask=(cloth&(tile[:,:,3]>=128)).astype('uint8')*255
  if (mask>0).sum()<25:continue
  templates[form].append((key,tile,mask,(axis[0]-box[0],axis[1]-box[1])))
 for key,(im,m,p) in raw.items():
  ox,oy=nums(m['offset']);axis=(round(im.width/2-ox),bbox(im)[3]-1);form=outfit(key);kind='body';method='original body foot';score=None
  if key.startswith('OugaDm'):axis=(im.width//2,im.height//2);kind='background';method='original dimensional scenery centre'
  elif key.startswith('OugaMon'):axis=(im.width//2,im.height//2);kind='effect';method='original floating ruins centre'
  elif key.startswith('Akamaru_Skill11_0') and len(key.rsplit('_',1)[1])==3:axis=(im.width//2,im.height//2);kind='effect';method='original standalone cyan sphere'
  elif key.startswith('Akamaru_'):
   kind='puppet';method='original puppet body and ground plane'
   if key.startswith('Akamaru_Skill01_') and len(key.rsplit('_',1)[1])==3:axis=(im.width//2,155)
   if key.startswith('Akamaru_Skill01_') and im.width==380:axis=(im.width//2,235)
   if key.startswith('Akamaru_Skill01_Down_'):axis=(125,80);method='original spider feet on the ground ring'
  elif im.width>110 or im.height>110:
   kind='body_with_effect';target=np.array(im);best=None
   for name,tile,mask,pivot in templates[form]:
    h,w=tile.shape[:2]
    if h>im.height or w>im.width:continue
    lo=0;hi=min(im.width,170) if key.startswith('Kiba_Skill06_') else im.width
    if hi-lo<w:continue
    res=cv2.matchTemplate(target[:,lo:hi],tile,cv2.TM_SQDIFF,mask=mask)/float(max(1,(mask>0).sum())*4*255**2);res[~np.isfinite(res)]=np.inf;idx=np.unravel_index(np.argmin(res),res.shape);s=float(res[idx])
    if best is None or s<best[0]:best=(s,(int(idx[1])+pivot[0],int(idx[0])+pivot[1]),name)
   if best and best[0]<.02:score=best[0];axis=best[1];method='original cloth match '+best[2]
   else:axis=(axis[0],round(im.height/2+oy+38));method='original source baseline';score=best[0] if best else None
   if key.startswith('Kiba_Skill04Ex_'):axis=(155,244);method='single original outlined body inside Raiton pillar'
  # The large canvases share a fixed body plane. Never infer the feet
  # from glow, rocks or a different outfit's recovery cell.
  if key.startswith('Kiba_Skill05_'):axis=(25,258);method='original cloaked caster feet'
  elif key.startswith('Kiba_Skill06_') and im.width>110:axis=(235,245);method='exact original raised-arm body match'
  elif key.startswith('Kiba_Skill02_'):
   axis=(45,128) if im.width==140 else (55,98);method='original pink-strike body plane'
  elif key.startswith('Kiba_Skill04_'):
   axis=(195,184) if im.width==310 else (55,149) if im.width==220 else (55,158) if im.width==280 else (75,158);method='original whip and strike body plane'
  elif key.startswith('Kiba_SkillDash_'):axis=(130,104);method='original dashing body plane'
  elif key.startswith('Kiba_Skill11_'):axis=(75,130);method='original Raiton fist body plane'
  elif key.startswith('Kiba_Skill03_'):axis=(85,124);method='original Raiton charge body plane'
  g=29001 if key.startswith(('Akamaru_','OugaDm')) else 29000
  put(key,g,sum(p['group']==g for p in manifest),im,axis,form=form,kind=kind,alignment=method,match_error=score,source_plist=str(p.relative_to(ROOT)),rectangle=m['frame'],source_offset=m['offset'],source_rotated=m.get('rotated',False))
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 for n,size in [(0,(25,25)),(1,(120,140))]:
  im=raw['Kiba_Idle_001'][0].crop((8,0,37,34));im=im.resize((25,25) if n==0 else (110,125),Image.Resampling.NEAREST);out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));put(f'Portrait_{n}',9000,n,out,(0,0),kind='portrait')
 archive.save(CHAR/'OugaYatsume.sff');(A/'keys.json').write_text(json.dumps(mapping,indent=2)+'\n');(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n');(A/'excluded_frames.json').write_text(json.dumps(excluded,indent=2)+'\n')
 b=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',b,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',b,off);samples[g,n]=b[off+16:off+16+size];off=nxt
 smap={};audio=[]
 for g,folder in [(2,'Effect'),(3,'Ouga'),(4,'Yatsume')]:
  for n,p in enumerate(sorted((SRC/'Audio'/folder).iterdir())):
   if not p.is_file():continue
   dest=A/'sound'/f'{g}_{n}.wav';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-ac','1','-ar','22050','-c:a','pcm_s16le',str(dest)],check=True);samples[g,n]=dest.read_bytes();smap[folder+'/'+p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=sha(p.read_bytes()),group=g,number=n))
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',header,16,len(samples),512);off=512;parts=[]
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  nxt=off+16+len(wav) if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'OugaYatsume.snd').write_bytes(bytes(header)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=smap,source_audio=audio),indent=2)+'\n')
 board=Image.new('RGB',(1200,((len(raw)+7)//8)*135),(35,38,43));draw=ImageDraw.Draw(board)
 for i,(key,(im,_,_)) in enumerate(raw.items()):
  im=im.copy();im.thumbnail((146,105),Image.Resampling.NEAREST);x=i%8*150;y=i//8*135;board.paste(im,(x+(150-im.width)//2,y),im);draw.text((x+1,y+108),key,fill='white')
 board.save(ROOT/'previews/OugaYatsume_original_sprites.jpg');print('Ouga assets:',len(raw),'original cells;',len(manifest),'sprites;',len(samples),'sounds;',excluded)
if __name__=='__main__':main()
