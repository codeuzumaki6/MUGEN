#!/usr/bin/env python3
"""Extract the original Ryu sheet without redrawing or scaling its body art."""
from pathlib import Path
import hashlib,io,json,struct
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
from build_mamushi_assets import pack_sff
from make_combo_preview import Sff2

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'RyuShinju';A=CHAR/'assets';SOURCE=ROOT/'source_material/Ryu_original'
BODIES=[]
def row(role,boxes,axes):
 for i,(box,axis) in enumerate(zip(boxes,axes)):BODIES.append((role+str(i),box,axis))
row('idle',[(41,138,70,219),(79,138,108,219),(117,138,146,219)],[55,93,131])
row('walk',[(33,227,70,310),(75,227,124,309),(134,227,177,309),(186,227,219,309),(224,227,270,309),(274,227,313,309)],[54,99,156,204,247,294])
row('hurt',[(31,322,80,396),(86,324,134,395),(143,328,214,376),(234,320,305,360),(230,366,310,392),(325,341,391,385),(402,336,444,391)],[54,106,178,267,267,350,426])
row('cast',[(41,410,78,491),(85,410,115,491),(126,412,155,493),(162,411,217,492),(223,411,278,492),(290,410,334,491),(340,410,378,491)],[58,99,140,177,238,308,357])
row('needles',[(33,501,100,581),(103,501,172,583),(184,501,243,581),(252,502,311,582)],[52,122,202,270])
row('punch',[(32,590,67,666),(72,598,149,665),(149,601,228,668),(229,599,295,666),(316,595,358,671),(358,603,427,671),(428,602,491,670),(493,603,556,671),(568,594,618,671),(623,595,667,672)],[51,97,176,255,338,383,453,518,594,648])
row('sweep',[(34,682,83,775),(91,680,123,773),(135,691,191,772),(196,689,252,771)],[52,108,153,214])
row('push',[(35,783,85,860),(90,784,140,861)],[52,108])
row('claw_cast',[(37,865,87,945),(91,866,141,946)],[55,109])
row('iron_sweep',[(35,939,93,1044),(93,939,187,1043),(189,941,290,1043),(297,944,399,1045),(405,958,499,1045)],[55,114,209,316,425])
row('iron_arc',[(30,1046,104,1153),(107,1045,181,1155),(183,1052,282,1158),(286,1050,390,1158),(392,1053,482,1158)],[65,128,209,312,416])
row('iron_control',[(43,1162,131,1250),(134,1165,210,1251),(212,1164,278,1250),(281,1164,347,1249),(349,1162,408,1249),(418,1162,504,1249),(518,1166,599,1253),(605,1165,681,1251)],[64,154,243,310,375,444,546,628])
row('air',[(36,1253,94,1341),(105,1250,154,1341),(39,1352,105,1439),(98,1351,168,1437)],[64,132,63,123])
row('sword',[(25,1441,88,1527),(93,1443,154,1529),(157,1444,236,1528),(241,1442,320,1526),(315,1438,409,1520),(414,1440,487,1520)],[64,130,198,284,367,450])
row('thrust',[(33,1530,160,1607),(149,1531,274,1608)],[86,202])
row('flight',[(27,1616,97,1701),(109,1617,176,1702),(178,1634,260,1697),(271,1634,355,1694),(374,1634,440,1694),(447,1632,512,1692)],[64,143,222,315,410,482])
FX={8600:(385,485,415,579),8601:(270,684,349,767),8602:(167,803,231,843),8603:(154,893,330,928),8604:(171,1267,290,1343),8605:(308,1261,401,1341),8606:(415,1274,534,1327),8607:(197,1374,220,1399)}

def cut(sheet,box):
 v=np.array(sheet.crop(box).convert('RGBA'));v[:,:,3]=np.where(np.all(v[:,:,:3]==(44,120,167),axis=2),0,255);im=Image.fromarray(v);bb=im.getbbox();assert bb,box
 return im.crop(bb),(box[0]+bb[0],box[1]+bb[1])
def main():
 for sub in ['sprites','effects','sound']:(A/sub).mkdir(parents=True,exist_ok=True)
 sheet=Image.open(SOURCE/'Ryu_sheet.png');assert sheet.size==(707,1715)
 records=[];manifest=[];effects={}
 def put(g,n,im,axis,body=False,**info):
  p=A/('sprites' if body else 'effects')/f'{g}_{n}.png';im.save(p);records.append((g,n,p,axis));manifest.append(dict(group=g,number=n,file=str(p.relative_to(CHAR)),axis=axis,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest(),**info))
  if not body:effects[g,n]=im
 for n,(role,box,ax) in enumerate(BODIES):
  im,origin=cut(sheet,box)
  # Several tightly packed sword poses overlap neighboring rectangles. Keep
  # their connected body, while retaining deliberately detached iron FX in
  # the iron-control rows.
  if not role.startswith('iron_'):
   v=np.array(im);lab,_=label(v[:,:,3]>0,np.ones((3,3)));sizes=np.bincount(lab.ravel());sizes[0]=0;v[:,:,3]=np.where(lab==sizes.argmax(),255,0);im=Image.fromarray(v);bb=im.getbbox();im=im.crop(bb);origin=(origin[0]+bb[0],origin[1]+bb[1])
  put(0,n,im,(ax-origin[0],im.height-1),True,role=role,source_rectangle=box,redrawn=False,scale=1,neighbor_fragments_removed=not role.startswith('iron_'))
 for g,box in FX.items():
  im,_=cut(sheet,box);axis=(im.width//2,im.height-1) if g==8601 else (im.width//2,im.height//2)
  put(g,0,im,axis,source_rectangle=box,redrawn=False)
 # Horizontal iron needle and a centered feather preserve their source drawing.
 im=effects[8600,0].rotate(-75,resample=Image.Resampling.NEAREST,expand=True);im=im.crop(im.getbbox());put(8610,0,im,(im.width//2,im.height//2),derived_from='Original iron needle, rotation only')
 # Wings use the three separate original wing poses, mirrored about the spine.
 for n in range(6):
  wing=effects[[8604,8605,8606,8605,8604,8606][n],0];canvas=Image.new('RGBA',(256,100))
  wing=wing.resize((118,round(wing.height*118/wing.width)),Image.Resampling.NEAREST)
  canvas.alpha_composite(wing,(128,0));canvas.alpha_composite(wing.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(10,0))
  put(8615,n,canvas,(128,5),derived_from='Vaydra original separate iron wings, paired')
 # Supplemental effect-only cyclone. Original character and wing art remains
 # untouched; a continuous rotating funnel replaces separated wing fragments.
 atlas=Image.open(ROOT/'source_material/Ryu_generated/iron_tornado_atlas.png').convert('RGBA');frames=[]
 for n in range(8):
  col=n%4;row=n//4;im=atlas.crop((col*atlas.width//4,row*atlas.height//2,(col+1)*atlas.width//4,(row+1)*atlas.height//2));v=np.array(im);v[:,:,3]=np.where(v[:,:,3]>=128,255,0);im=Image.fromarray(v);frames.append(im.crop(im.getbbox()))
 factor=min(128/max(im.width for im in frames),146/max(im.height for im in frames))
 for n,im in enumerate(frames):
  im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST);canvas=Image.new('RGBA',(134,152));canvas.alpha_composite(im,((134-im.width)//2,150-im.height))
  put(8620,n,canvas,(67,150),derived_from='Supplemental AI-generated black iron-sand cyclone effect atlas',body_art=False,ai_generated_effect=True)
 # Shared standalone impacts, focus flash, dust and energy, already credited.
 shared=Sff2(ROOT/'MitsukiTBV/MitsukiTBV.sff')
 for g,count in [(8700,4),(8710,4),(8720,6),(8670,11),(8900,24),(8910,5),(8820,5)]:
  for n in range(count):
   im,axis=shared.image(g,n);put(g,n,im,axis,shared_project_effect=True)
 # A magnetic fist from this sheet, rimmed by a blue electrical effect.
 for n in range(8):
  lightning,_=shared.image(8932,n);v=np.array(lightning);light=np.max(v[:,:,:3],axis=2).astype(float)
  v[:,:,0]=(light*.16).astype('uint8');v[:,:,1]=(light*.56).astype('uint8');v[:,:,2]=light.astype('uint8')
  canvas=Image.new('RGBA',(112,68));bolt=Image.fromarray(v).resize((100,60),Image.Resampling.NEAREST);canvas.alpha_composite(bolt,(6,4))
  fist=effects[8602,0];canvas.alpha_composite(fist,(28,(68-fist.height)//2));put(8625,n,canvas,(20,34),derived_from='Original iron fist with a separate blue electrical rim',body_art=False)
 for n,size in [(0,(25,25)),(1,(120,140))]:
  head=Image.open(A/'sprites/0_0.png').crop((5,0,24,27));f=min(size[0]/head.width,size[1]/head.height);head=head.resize((round(head.width*f),round(head.height*f)),Image.Resampling.NEAREST);canvas=Image.new('RGBA',size);canvas.alpha_composite(head,((size[0]-head.width)//2,(size[1]-head.height)//2));put(9000,n,canvas,(0,0),portrait_from_original=True)
 pack_sff(records,CHAR/'RyuShinju.sff');(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n')
 data=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<II',data,16);samples={}
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<IIII',data,off)
  if g==1 and n!=44:samples[g,n]=data[off+16:off+16+size]
  off=nxt
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=data[12:16];struct.pack_into('<II',header,16,len(samples),512);parts=[];off=512
 for i,((g,n),payload) in enumerate(sorted(samples.items())):
  nxt=off+16+len(payload) if i+1<len(samples) else 0;parts.append(struct.pack('<IIII',nxt,len(payload),g,n)+payload);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(payload)
 (CHAR/'RyuShinju.snd').write_bytes(bytes(header)+b''.join(parts))
 board=Image.new('RGB',(1200,((len(BODIES)+9)//10)*125),(28,31,40));draw=ImageDraw.Draw(board)
 for n,(role,_,_) in enumerate(BODIES):
  im=Image.open(A/'sprites'/f'0_{n}.png');im.thumbnail((115,103),Image.Resampling.NEAREST);x=n%10*120;y=n//10*125;board.paste(im,(x+(120-im.width)//2,y),im);draw.text((x+2,y+104),f'{n}: {role}',fill='white')
 board.save(ROOT/'previews/RyuShinju_sprites_originales.png');print(len(BODIES),'original Ryu poses,',len(records),'sprites,',len(samples),'nonverbal sounds')
if __name__=='__main__':main()
