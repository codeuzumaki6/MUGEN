#!/usr/bin/env python3
"""Pack Vaydra's unchanged TBV pixels and CobraG6's supplied voices/effects."""
from pathlib import Path
import hashlib,io,json,struct
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
from build_mamushi_assets import pack_sff
from make_combo_preview import Sff2
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MitsukiTBV';A=CHAR/'assets';SRC=ROOT/'source_material/Mitsuki_TBV_original';DONOR=ROOT/'source_material/Mitsuki_CobraG6_voice_reference'
B=[]
def row(role,y0,y1,items):
 for i,(x0,x1,axis) in enumerate(items):B.append((role+str(i),(x0,y0,x1,y1),axis))
row('idle',186,274,[(47,80,64),(80,114,97),(114,150,131)]) #0
row('run',282,349,[(35,106,77),(106,179,143),(180,237,212),(237,305,276),(305,377,343),(380,437,411)]) #3
row('hurt',352,433,[(41,83,64),(85,134,103),(134,182,151),(188,265,220),(265,341,298),(342,429,381),(433,506,460),(507,553,531)]) #9
row('punch',440,521,[(43,87,65),(90,172,123),(176,257,206),(257,334,288),(334,408,364),(408,480,439),(480,552,510)]) #17
row('kick',525,611,[(46,83,66),(90,170,118),(174,253,202),(267,306,286),(310,397,341),(401,485,434),(489,558,518)]) #24
row('arm',616,701,[(41,91,65),(92,144,119),(147,202,175),(205,259,230)]) #31
row('spin',702,800,[(46,99,70),(101,147,124),(147,190,168),(190,245,213),(235,289,257),(288,341,310),(347,391,369),(390,441,418),(449,500,476)]) #35
row('wind',807,891,[(43,89,65),(91,161,119),(171,214,194),(226,298,254)]) #44
row('air',894,981,[(37,83,63),(84,130,109),(139,179,159),(185,221,204),(223,280,250),(281,324,307)]) #48
row('cast',981,1064,[(38,81,59),(84,125,104),(132,171,150),(198,259,224)]) #54 skip the separate prop at x171
row('cast2',1067,1148,[(39,81,60),(83,126,104),(132,171,150),(186,241,216),(237,290,266),(289,339,317)]) #58
row('stretch',1153,1236,[(38,83,61),(84,145,106),(188,237,212)]) #64
S=[]
def sage(role,box,axis):S.append((role,box,axis))
for i,(x0,x1,a) in enumerate([(44,79,62),(85,120,102),(128,163,146)]):sage('idle'+str(i),(x0,1240,x1,1332),a)
sage('coiled',(231,1226,305,1331),271);sage('coiled_fast',(304,1241,387,1332),347)
for i,(x0,x1,a) in enumerate([(37,108,77),(108,177,146),(178,250,216)]):sage('run'+str(i),(x0,1334,x1,1403),a)
for i,(x0,x1,a) in enumerate([(32,75,54),(83,165,113),(168,249,197),(249,328,279)]):sage('punch'+str(i),(x0,1406,x1,1490),a)
for i,(x0,x1,a) in enumerate([(32,95,57),(103,147,124),(151,223,181)]):sage('palm'+str(i),(x0,1486,x1,1576),a)
for i,(x0,x1,a) in enumerate([(27,77,51),(77,130,101),(134,188,159),(191,245,218)]):sage('cast'+str(i),(x0,1581,x1,1670),a)
FX={8600:[(496,858,536,910),(577,884,616,900),(657,907,698,925),(473,923,514,950),(543,923,605,1005),(615,958,712,1012),(741,951,796,1014),(387,1013,436,1082),(437,1005,528,1057),(535,1024,606,1087),(623,1063,666,1107)],
8610:[(410,1253,455,1340),(449,1256,496,1305),(499,1251,569,1330),(567,1249,637,1335),(645,1268,719,1338),(721,1256,808,1345),(378,1370,440,1451),(445,1369,524,1423),(498,1391,564,1451),(381,1471,455,1515),(453,1488,540,1540),(556,1490,668,1541),(480,1545,657,1586),(475,1591,651,1632)],
8620:[(254,1633,279,1662),(279,1633,307,1662),(308,1633,335,1662),(339,1631,368,1662),(371,1632,400,1663),(324,1605,349,1633),(349,1606,375,1634),(374,1605,400,1635)]}

def cut(sheet,box):
 v=np.array(sheet.crop(box).convert('RGBA'));v[:,:,3]=np.where(np.all(v[:,:,:3]==(44,120,167),axis=2),0,255);im=Image.fromarray(v);bb=im.getbbox();assert bb,box
 return im.crop(bb),(box[0]+bb[0],box[1]+bb[1])
def read_v1(path):
 b=path.read_bytes();count,off=struct.unpack_from('<II',b,20);pal=None;prev=[];records={}
 for i in range(count):
  nxt,size,x,y,g,n,link,same=struct.unpack_from('<IIhhHHHB',b,off);payload=b[off+32:off+32+size]
  if size:
   if len(payload)>768 and payload[-769]==12:pal=payload[-768:]
   elif pal is not None:payload+=bytes([12])+pal
   pic=Image.open(io.BytesIO(payload));pic.load();idx=np.array(pic);v=np.array(pic.convert('RGBA'));v[:,:,3]=np.where(idx==0,0,255);im=Image.fromarray(v)
  else:im=prev[link].copy()
  prev.append(im);records[g,n]=(im,(x,y));off=nxt
 return records

def main():
 for d in ['sprites','effects','sound']:(A/d).mkdir(parents=True,exist_ok=True)
 sheet=Image.open(SRC/'Mitsuki_TBV_sheet.png').convert('RGBA');assert sheet.size==(836,1715)
 records=[];manifest=[]
 def put(g,n,im,axis,body=False,**info):
  p=A/('sprites' if body else 'effects')/f'{g}_{n}.png';im.save(p);records.append((g,n,p,axis));manifest.append(dict(group=g,number=n,file=str(p.relative_to(CHAR)),axis=axis,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest(),**info))
 for g,poses in [(0,B),(1,S)]:
  for n,(role,box,ax) in enumerate(poses):
   im,origin=cut(sheet,box)
   v=np.array(im);lab,count=label(v[:,:,3]>0,np.ones((3,3)));sizes=np.bincount(lab.ravel());sizes[0]=0;v[:,:,3]=np.where(lab==sizes.argmax(),255,0);im=Image.fromarray(v);bb=im.getbbox();im=im.crop(bb);origin=(origin[0]+bb[0],origin[1]+bb[1])
   put(g,n,im,(ax-origin[0],im.height-1),True,role=role,source_rectangle=box,retained_component='largest connected original body; exclude neighboring pose fragments',redrawn=False)
 for g,boxes in FX.items():
  for n,box in enumerate(boxes):
   im,origin=cut(sheet,box);put(g,n,im,(im.width//2,im.height//2),source_rectangle=box,redrawn=False)
 donor=read_v1(DONOR/'Mitsuki.sff')
 # 1550,4..6 contain the donor's small body, not a standalone effect.
 # Never include those frames in the replacement character or archive.
 for old in range(4,7):
  path=A/'effects'/f'8680_{old}.png'
  if path.exists():path.unlink()
 for dest,src,nums in [(8630,1050,range(21)),(8640,1063,range(9)),(8650,2007,range(28)),(8660,9012,range(9)),(8670,9010,range(11)),(8680,1550,range(4))]:
  for n,sn in enumerate(nums):
   im,axis=donor[src,sn];put(dest,n,im,axis,donor_group=src,donor_number=sn)
 # Fit continuous electrical arcs from the supplied horizontal Raiton FX.
 # The body art is untouched; only the electrical effect is stretched to its actual hit range.
 for group,length in [(8930,230),(8931,280),(8932,108)]:
  for frame in range(8):
   canvas=Image.new('RGBA',(length,48))
   tile=donor[2007,11+frame%5][0].copy();v=np.array(tile);bright=np.max(v[:,:,:3],axis=2)>60
   yy,xx=np.where(bright);tile=tile.crop((int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1))
   tile=tile.resize((length,30+(frame%3)*3),Image.Resampling.NEAREST)
   canvas.alpha_composite(tile,(0,(48-tile.height)//2))
   put(group,frame,canvas,(0,24),role='Continuous Raiton arc',assembled_from='CobraG6 effect 2007,11..15',body_art=False)
 # Rooted coils have a distinct silhouette from travelling snake shots.
 for group,sourcegroup,numbers in [(8940,8600,[4,5,6,8]),(8941,8610,[6,7,10,11])]:
  for frame in range(4):
   canvas=Image.new('RGBA',(100,100))
   for j in range(3):
    part=Image.open(A/'effects'/f'{sourcegroup}_{numbers[(frame+j)%4]}.png')
    part=part.resize((70,48),Image.Resampling.NEAREST).rotate(j*120,resample=Image.Resampling.NEAREST,expand=True)
    canvas.alpha_composite(part,((100-part.width)//2,(100-part.height)//2))
   put(group,frame,canvas,(50,96),role='Rooted serpent coil',source_group=sourcegroup,body_art=False)
 shared=Sff2(ROOT/'JuraShinju/JuraShinju.sff')
 for g,count in [(8700,4),(8710,4),(8720,6),(8820,5),(8900,24),(8910,5)]:
  for n in range(count):
   im,axis=shared.image(g,n);put(g,n,im,axis,shared_project_effect=True)
 head=Image.open(A/'sprites/0_0.png').crop((7,0,25,25))
 for n,size in [(0,(25,25)),(1,(120,140))]:
  f=min(size[0]/head.width,size[1]/head.height);h=head.resize((round(head.width*f),round(head.height*f)),Image.Resampling.NEAREST);im=Image.new('RGBA',size);im.alpha_composite(h,((size[0]-h.width)//2,(size[1]-h.height)//2));put(9000,n,im,(0,0))
 pack_sff(records,CHAR/'MitsukiTBV.sff')
 samples={}
 for path,keep in [(DONOR/'Mitsuki.snd',lambda g,n:g==0 and 1<=n<=23),(ROOT/'JuraShinju/JuraShinju.snd',lambda g,n:g==1)]:
  b=path.read_bytes();num,off=struct.unpack_from('<II',b,16)
  for _ in range(num):
   nxt,size,g,n=struct.unpack_from('<IIII',b,off)
   if keep(g,n):samples[g,n]=b[off+16:off+16+size]
   off=nxt
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<II',header,16,len(samples),512);parts=[];off=512
 for i,((g,n),payload) in enumerate(sorted(samples.items())):
  nxt=off+16+len(payload) if i+1<len(samples) else 0;parts.append(struct.pack('<IIII',nxt,len(payload),g,n)+payload);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(payload)
 (CHAR/'MitsukiTBV.snd').write_bytes(bytes(header)+b''.join(parts));(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n')
 body=[m for m in manifest if m['group'] in [0,1]];board=Image.new('RGB',(1200,((len(body)+7)//8)*130),(35,39,49));d=ImageDraw.Draw(board)
 for i,m in enumerate(body):
  im=Image.open(CHAR/m['file']);im.thumbnail((144,100),Image.Resampling.NEAREST);x=i%8*150;y=i//8*130;board.paste(im,(x+(150-im.width)//2,y+100-im.height),im);d.text((x+3,y+105),f"{m['group']},{m['number']} {m['role']}",fill='white')
 board.save(ROOT/'previews/MitsukiTBV_sprites.png');print(len(records),'sprites,',len(body),'original body poses,',len(samples),'sounds')
if __name__=='__main__':main()
