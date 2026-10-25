#!/usr/bin/env python3
"""Pack Delta's recreated poses and dedicated pink laser/jet effects for MUGEN."""
from pathlib import Path
import hashlib,io,json,shutil,struct,wave,sys
import numpy as np
from PIL import Image,ImageDraw
from build_roster_revision import Archive
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'DeltaKara';A=CHAR/'assets'
POSES=['idle0','idle1','idle2','walk0','walk1','walk2','walk3','walk4','run0','run1','run2','run3','run4','run5','crouch','guard','jab_ready','jab','jab_recover','palm_ready','palm','kick_ready','kick','kick_recover','lance_ready','lance','lance_recover','sweep_ready','sweep','upper_ready','upper','absorb','jump0','jump1','hover0','hover1','air_kick','dive','land','laser','hurt0','hurt1','air_hurt','prone','sit','kneel','win0','win1']
def sha(b):return hashlib.sha256(b).hexdigest()
def snd_read(data):
 count,off=struct.unpack_from('<2I',data,16);out={}
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<4I',data,off);out[g,n]=data[off+16:off+16+size];off=nxt
 return out
def main():
 try:import cv2
 except ImportError:sys.path.insert(0,'/tmp/roster-cv');import cv2
 src=ROOT/'source_material/Delta_recreated';src.mkdir(parents=True,exist_ok=True)
 for name,original in [('delta_poses.png','exec-74508a09-a163-4b00-b65d-0ccfe970c462.png'),('delta_fx.png','exec-5d6db569-8a72-4ee3-ba53-10df6447d65b.png'),('delta_blast.png','exec-a43d06d7-5e8c-499c-86df-50406e80ac7e.png')]:
  if not (src/name).exists():shutil.copy2(ROOT.parent/'generated_images'/original,src/name)
 for name in ['sprites','effects','sound']:(A/name).mkdir(parents=True,exist_ok=True)
 archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries.clear();manifest=[]
 def put(g,n,im,axis,role,source=None):
  p=A/('sprites' if g==0 else 'effects')/f'{g}_{n}.png';im.save(p);archive.put((g,n),im,axis);manifest.append(dict(group=g,number=n,file=str(p.relative_to(CHAR)),axis=list(axis),role=role,source=source,rgba_sha256=sha(im.tobytes())))
 sheet=Image.open(src/'delta_poses.png').convert('RGBA');arr=np.array(sheet)
 mask=(arr[:,:,3]>=100).astype('uint8');mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
 nn,labels,stats,centers=cv2.connectedComponentsWithStats(mask)
 objects=[(tuple(map(int,s[:4])),tuple(map(float,c))) for s,c in zip(stats[1:],centers[1:]) if s[4]>1200]
 assert len(objects)==48,len(objects);objects.sort(key=lambda r:r[1][1]);ordered=[]
 for y in range(6):ordered+=sorted(objects[y*8:y*8+8],key=lambda r:r[1][0])
 for n,((x,y,w,h),center) in enumerate(ordered):
  box=(max(0,x-2),max(0,y-2),min(sheet.width,x+w+2),min(sheet.height,y+h+2));im=sheet.crop(box)
  data=np.array(im);r,g,b=[data[:,:,j].astype(float) for j in range(3)];yy=np.indices(r.shape)[0]
  red=(r>g*1.4)&(r>b*1.15)&(r>75)&(data[:,:,3]>=128)&(yy>h*.3)&(yy<h*.85)
  # The pelvis stays fixed even when a punch or mechanical leg extends.
  if red.sum()>8:
   counts=red.sum(axis=1);peak=int(counts.argmax());near=red&(abs(yy-peak)<10);ax=round(float(np.where(near)[1].mean()))
  else:ax=round(im.width/2)
  opaque=Image.fromarray((data[:,:,3]>=128).astype('uint8')*255).getbbox();ay=opaque[3]-1
  im=im.resize((round(im.width*.5),round(im.height*.5)),Image.Resampling.NEAREST);axis=(round(ax*.5),round(ay*.5))
  put(0,n,im,axis,POSES[n],dict(sheet='delta_poses.png',rectangle=box,uniform_scale=.5,recreated=True))
 fx=Image.open(src/'delta_fx.png').convert('RGBA')
 for row,g in enumerate([8800,8801,8802,8803]):
  for n in range(4):
   box=(n*384,row*256,(n+1)*384,(row+1)*256);im=fx.crop(box)
   # All animation frames share an emission pivot, never a bounding-box centre.
   axis={8800:(192,150),8801:(32,140),8802:(192,22),8803:(128,130)}[g]
   factor={8800:.25,8801:.6,8802:.25,8803:.30}[g]
   im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST)
   put(g,n,im,tuple(round(v*factor) for v in axis),['Eye charge','Pink ocular beam','Foot thruster','Ocular absorption'][row],dict(sheet='delta_fx.png',rectangle=box,scale=factor,recreated=True))
 shared=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 blast=Image.open(src/'delta_blast.png').convert('RGBA')
 for n in range(12):
  x=n%4*blast.width//4;y=n//4*blast.height//3;w=blast.width//4;h=blast.height//3
  im=blast.crop((x,y,x+w,y+h));a=np.array(im);yy=np.indices(a.shape[:2])[0]
  light=(a[:,:,0]>180)&(a[:,:,1]>140)&(a[:,:,3]>=128)&(yy>h*.7)
  ay=int(light.sum(axis=1).argmax())+4 if n>=4 and light.any() else h-20
  axis=(w//2,ay);im=im.resize((310,310),Image.Resampling.NEAREST)
  put(8840,n,im,(155,round(ay*310/h)),'Controlled self-destruction phase',dict(sheet='delta_blast.png',cell=n,recreated=True))
 for g,count in [(8700,4),(8710,4),(8720,6),(8820,5),(8900,24)]:
  for n in range(count):
   im,axis=shared.image((g,n));put(g,n,im,axis,'Shared credited combat effect',dict(character='JuraShinju',group=g,number=n))
 head=Image.open(A/'sprites/0_0.png').convert('RGBA').crop((7,0,35,27))
 for n,size in [(0,(25,25)),(1,(120,140))]:
  portrait=Image.new('RGBA',size);part=head.copy();part.thumbnail(size,Image.Resampling.NEAREST)
  if n:part=head.resize((120,116),Image.Resampling.NEAREST)
  portrait.alpha_composite(part,((size[0]-part.width)//2,(size[1]-part.height)//2));put(9000,n,portrait,(0,0),'Delta portrait')
 archive.save(CHAR/'DeltaKara.sff')
 source=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();samples=snd_read(source)
 samples={k:v for k,v in samples.items() if k[0]==1};assert all(g==1 for g,n in samples)
 # Sound effects only: do not give Delta another character's dialogue.
 header=bytearray(source[:512]);struct.pack_into('<2I',header,16,len(samples),512);chunks=[];off=512
 for i,((g,n),wav) in enumerate(samples.items()):
  nxt=off+16+len(wav) if i<len(samples)-1 else 0;chunks.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'DeltaKara.snd').write_bytes(bytes(header)+b''.join(chunks))
 (A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n')
 # Discard obsolete derived frames from earlier Delta builds, including the
 # rejected red splatter effect. Never touch the supplied reference material.
 expected={CHAR/p['file'] for p in manifest}
 for folder in [A/'sprites',A/'effects']:
  for p in folder.glob('*.png'):
   if p not in expected:p.unlink()
 (src/'source.json').write_text(json.dumps(dict(video='Share❗ sprite Delta Kara member Moveset Gameplay.mp4',video_sediment_id='file_00000000ee1c81f6907534775c8255ff',video_author='VayDra Senki as credited in the supplied gameplay',body_art='48 recreated poses based on gameplay reference; AI-generated, not original author sprite data',fx_art='Dedicated generated pink ocular beam, absorption vortex and thruster exhaust',original_assets_recovered=False,source_reference='User supplied eye-laser and Rasengan absorption images'),indent=2)+'\n')
 board=Image.new('RGB',(1120,6*135),(31,33,39));d=ImageDraw.Draw(board)
 for n,role in enumerate(POSES):
  im,_=archive.image((0,n));im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);im.thumbnail((136,110));x=n%8*140;y=n//8*135;board.paste(im,(x+(140-im.width)//2,y),im);d.text((x+2,y+114),role,fill='white')
 (ROOT/'previews').mkdir(exist_ok=True);board.save(ROOT/'previews/DeltaKara_sprites.png')
 print('Delta assets:',len(archive.entries),'sprites;',len(samples),'nonverbal sounds; 48 recreated body poses')
if __name__=='__main__':main()
