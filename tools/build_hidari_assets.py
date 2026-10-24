#!/usr/bin/env python3
"""Pack Vaydra's Hidari sheet; change only the two original red iris colors."""
from pathlib import Path
import hashlib,json,struct
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
from pack_hidari_sff import pack_sff
from make_combo_preview import Sff2
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'HidariShinju';A=CHAR/'assets';SOURCE=ROOT/'source_material/Hidari_original'
# Rectangles in the native 512x1300 public original; axes follow the body,
# independently of the long wood arm and lightning effects.
BODIES=[]
def row(role,boxes,axes):
 for i,(box,axis) in enumerate(zip(boxes,axes)):BODIES.append((role+str(i),box,axis))
row('idle',[(10,77,46,160),(51,77,90,162)],[28,71])
row('run',[(101,87,176,152),(182,87,260,152),(269,88,339,153),(350,85,425,151),(435,81,491,157)],[139,220,306,387,462])
row('hurt',[(12,166,62,243),(71,165,124,244),(128,167,199,234),(208,163,287,216),(293,160,367,200),(290,204,373,235),(384,177,436,228)],[35,99,167,246,329,331,408])
row('crouch',[(443,176,483,230)],[463])
row('walk',[(8,251,44,336),(51,255,105,340),(113,254,167,338),(177,253,212,337),(231,255,285,339),(291,252,343,337)],[27,78,140,195,258,317])
row('strike',[(5,350,67,426),(77,352,154,422),(164,349,222,420),(230,353,283,420),(286,351,340,424),(349,347,433,420),(439,343,499,421)],[35,110,187,253,309,379,466])
row('chidori',[(6,439,54,516),(64,441,153,515),(154,442,232,516)],[29,112,185])
row('wood_cast',[(8,529,54,580)],[29])
row('focus',[(8,597,50,675),(57,600,107,675)],[29,82])
row('stretch',[(4,680,50,758),(51,678,116,756),(135,691,210,756),(219,687,330,753),(337,690,442,756)],[29,80,172,261,370])
row('wood_combo',[(7,763,65,858),(71,791,146,856),(146,757,246,864),(247,756,312,863),(322,755,385,862),(387,786,433,861)],[31,108,194,277,349,410])
row('discharge',[(6,869,50,947),(54,881,155,947),(159,882,256,948),(260,879,346,945)],[29,105,209,298])
row('push',[(7,953,69,1036),(84,952,146,1035)],[30,109])
row('marks',[(9,1044,51,1122),(61,1043,103,1121),(264,1038,308,1123)],[30,82,286])
row('sink',[(9,1129,38,1210),(43,1148,69,1210),(78,1170,104,1210),(110,1193,136,1210),(141,1181,180,1210),(182,1166,229,1210),(237,1167,287,1211),(288,1166,342,1210),(346,1172,419,1210)],[27,61,98,124,164,206,264,316,384])
EYES={(185,45,45):(145,185,248),(128,33,33):(68,100,180)}
FX={8600:[(75,560,111,587),(123,546,178,587),(192,521,255,584)],8601:[(439,688,470,726),(474,700,512,731),(486,728,503,771),(435,749,479,766)],8602:[(175,1239,246,1293),(247,1219,358,1295),(359,1222,461,1295)],8603:[(309,1013,440,1067),(127,1085,240,1116),(315,1081,441,1120)]}
def cut(sheet,box):
 v=np.array(sheet.crop(box).convert('RGBA'));v[:,:,3]=np.where(np.all(v[:,:,:3]==(3,138,14),axis=2),0,255);im=Image.fromarray(v);bb=im.getbbox();assert bb,box
 return im.crop(bb),(box[0]+bb[0],box[1]+bb[1])
def body(sheet,box):
 im,origin=cut(sheet,box);v=np.array(im);lab,_=label(v[:,:,3]>0,np.ones((3,3)));sizes=np.bincount(lab.ravel());sizes[0]=0;v[:,:,3]=np.where(lab==sizes.argmax(),255,0);im=Image.fromarray(v);bb=im.getbbox();im=im.crop(bb);origin=(origin[0]+bb[0],origin[1]+bb[1]);v=np.array(im);pixels=0
 for old,new in EYES.items():
  mask=np.all(v[:,:,:3]==old,axis=2)&(v[:,:,3]>0);pixels+=int(mask.sum());v[:,:,:3][mask]=new
 return Image.fromarray(v),origin,pixels

def main():
 for sub in ['sprites','effects','sound']:(A/sub).mkdir(parents=True,exist_ok=True)
 sheet=Image.open(SOURCE/'Hidari_sheet.png');assert sheet.size==(512,1300);records=[];manifest=[]
 def put(g,n,im,axis,body=False,**info):
  p=A/('sprites' if body else 'effects')/f'{g}_{n}.png';im.save(p);records.append((g,n,p,axis));manifest.append(dict(group=g,number=n,file=str(p.relative_to(CHAR)),axis=axis,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest(),**info))
 for n,(role,box,ax) in enumerate(BODIES):
  im,origin,pixels=body(sheet,box);put(0,n,im,(ax-origin[0],im.height-1),True,role=role,source_rectangle=box,redrawn=False,scale=1,eye_pixels_recolored=pixels)
 for g,boxes in FX.items():
  for n,box in enumerate(boxes):
   im,origin=cut(sheet,box)
   if g==8601:
    v=np.array(im);lab,_=label(v[:,:,3]>0,np.ones((3,3)));sizes=np.bincount(lab.ravel());sizes[0]=0;v[:,:,3]=np.where(lab==sizes.argmax(),255,0);im=Image.fromarray(v);im=im.crop(im.getbbox())
   if g==8602: # the last source row contains caster heads; retain only wood pixels
    v=np.array(im);rgb=v[:,:,:3].astype(int);keep=(rgb[:,:,0]>105)&(rgb[:,:,1]>95)&(rgb[:,:,2]>75)&(rgb[:,:,2]<205)&(rgb[:,:,0]-rgb[:,:,2]>15)&(rgb[:,:,1]-rgb[:,:,2]<90)&(v[:,:,3]>0);lab,_=label(keep,np.ones((3,3)));sizes=np.bincount(lab.ravel());sizes[0]=0;keep=binary_dilation(lab==sizes.argmax(),iterations=1)&(v[:,:,3]>0);v[:,:,3]=np.where(keep,255,0);im=Image.fromarray(v);im=im.crop(im.getbbox())
   axis=(im.width//2,im.height-1) if g==8600 else (0,im.height//2) if g==8602 else (im.width//2,im.height//2)
   put(g,n,im,axis,source_rectangle=box,redrawn=False)
 from hidari_susanoo_source import export_assets
 export_assets(put)
 shared=Sff2(ROOT/'MitsukiTBV/MitsukiTBV.sff')
 for g,count in [(8700,4),(8710,4),(8720,6),(8670,11),(8900,24),(8910,5),(8820,5)]:
  for n in range(count):
   im,axis=shared.image(g,n);put(g,n,im,axis,shared_project_effect=True)
 # Blue lightning is visibly electrical; it does not contain a miniature body.
 for n in range(8):
  im,axis=shared.image(8932,n);v=np.array(im);bright=np.max(v[:,:,:3],axis=2).astype(float);v[:,:,0]=(bright*.38).astype('uint8');v[:,:,1]=(bright*.73).astype('uint8');v[:,:,2]=bright.astype('uint8');im=Image.fromarray(v)
  put(8640,n,im,(0,im.height//2),shared_project_effect=True,lightning_blue=True)
 for n,size in [(0,(25,25)),(1,(120,140))]:
  head=Image.open(A/'sprites/0_0.png').crop((9,1,31,32));f=min(size[0]/head.width,size[1]/head.height);head=head.resize((round(head.width*f),round(head.height*f)),Image.Resampling.NEAREST);canvas=Image.new('RGBA',size);canvas.alpha_composite(head,((size[0]-head.width)//2,(size[1]-head.height)//2));put(9000,n,canvas,(0,0),portrait_from_original=True)
 pack_sff(records,CHAR/'HidariShinju.sff');(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n')
 data=(ROOT/'RyuShinju/RyuShinju.snd').read_bytes();(CHAR/'HidariShinju.snd').write_bytes(data);count,off=struct.unpack_from('<II',data,16)
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<IIII',data,off);(A/'sound'/f'{g}_{n}.wav').write_bytes(data[off+16:off+16+size]);off=nxt
 board=Image.new('RGB',(1200,((len(BODIES)+9)//10)*125),(28,31,40));draw=ImageDraw.Draw(board)
 for n,(role,_,_) in enumerate(BODIES):
  im=Image.open(A/'sprites'/f'0_{n}.png');im.thumbnail((115,103),Image.Resampling.NEAREST);x=n%10*120;y=n//10*125;board.paste(im,(x+(120-im.width)//2,y),im);draw.text((x+2,y+104),f'{n}: {role}',fill='white')
 board.save(ROOT/'previews/HidariShinju_sprites_originales.png');print(len(BODIES),'original poses,',len(records),'sprites,',count,'nonverbal sounds')
if __name__=='__main__':main()
