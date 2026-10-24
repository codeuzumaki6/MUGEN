#!/usr/bin/env python3
"""Extract both original Matsuri forms without redrawing or enlarging them."""
from pathlib import Path
import hashlib,json,struct,wave
import numpy as np
from scipy.ndimage import label,find_objects
from scipy.signal import butter,sosfilt
from PIL import Image,ImageDraw
from pack_hidari_sff import pack_sff
from make_combo_preview import Sff2
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MatsuriShinju';A=CHAR/'assets';SOURCE=ROOT/'source_material/Matsuri_original'
ROWS=[('idle',160,260),('walk',270,365),('hurt',375,475),('punch',480,575),('stretch',580,675),('thrust',680,780),('air',780,890),('cloak',890,985),('kick',990,1080),('spin',1080,1175),('palm',1175,1270),('gesture',1270,1360),('charge',1360,1450),('crouch',1470,1530),('water',1530,1620),('mark',1620,1720),('bloom',1720,1835)]

def components(sheet):
 rgb=np.array(sheet.convert('RGB'));bg=rgb[0,0];labels,count=label(np.any(rgb!=bg,axis=2),np.ones((3,3)));out=[]
 for i,bounds in enumerate(find_objects(labels)):
  y,x=bounds;area=int((labels[bounds]==i+1).sum())
  if area>=800 and y.stop-y.start>=24:out.append(dict(id=i+1,box=(x.start,y.start,x.stop,y.stop),area=area))
 return rgb,labels,out

def select_rows(items):
 groups={0:{},1:{}}
 for role,lo,hi in ROWS:
  found=[row for row in items if lo<=row['box'][1]<hi and (role!='mark' or row['box'][0]<280)]
  found.sort(key=lambda row:row['box'][0])
  if role=='hurt':found.sort(key=lambda row:(round(row['box'][0]/20),row['box'][1]))
  groups[0][role]=found
 def choose(role,lo,hi,xlo=0,xhi=707):
  groups[1][role]=sorted([r for r in items if lo<=r['box'][1]<hi and xlo<=r['box'][0]<xhi],key=lambda r:(round(r['box'][0]/20),r['box'][1]))
 choose('idle',1910,1950,0,95);choose('charge',1910,1950,430,560)
 choose('walk',2000,2020,0,145);choose('guard',2000,2030,430,560);choose('crouch',1960,1990,290,340)
 choose('punch',2088,2175);choose('kick',2176,2263);choose('spin',2263,2342)
 choose('water',2342,2426,0,160);choose('hurt',2342,2426,160,600)
 groups[1]['kick']=[r for r in groups[1]['kick'] if r['box'][0]!=93]
 return groups

def anchor(im):
 v=np.array(im);h,w=v.shape[:2];rgb=v[:,:,:3].astype(int);active=v[:,:,3]>0
 # Feet anchor extended arms and capes at the torso, rather than at the full
 # sprite's midpoint. Purple cloth and black outline pixels are excluded.
 gray=(np.max(rgb,axis=2)-np.min(rgb,axis=2)<40)&(np.min(rgb,axis=2)>18)
 skin=(rgb[:,:,0]>100)&(rgb[:,:,1]>75)&(rgb[:,:,2]<rgb[:,:,0])
 bottom=np.indices((h,w))[0]>=h-7;ys,xs=np.where(active&bottom&(gray|skin))
 if not len(xs):ys,xs=np.where(active&bottom)
 return (round(float(np.median(xs))) if len(xs) else w//2,h-1)

def soundbank():
 data=(ROOT/'RyuShinju/RyuShinju.snd').read_bytes();count,off=struct.unpack_from('<II',data,16);samples=[]
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<4I',data,off);samples.append((g,n,data[off+16:off+16+size]));off=nxt
 rate=22050;rng=np.random.default_rng(614)
 for n,duration in [(0,.32),(1,.44)]:
  t=np.arange(round(rate*duration))/rate;noise=sosfilt(butter(3,[900,7500],fs=rate,btype='bandpass',output='sos'),rng.normal(size=len(t)))
  signal=noise*.22*np.exp(-t*(11 if n==0 else 8))
  for i in range(9):
   begin=.012+i*.025;u=np.maximum(0,t-begin);freq=850-i*65
   signal+=.12*np.sin(2*np.pi*(freq*u-700*u*u))*np.exp(-u*65)*(t>=begin)
  signal/=max(1,np.max(np.abs(signal))/.8);p=A/'sound'/f'2_{n}.wav'
  with wave.open(str(p),'wb') as f:f.setparams((1,2,rate,0,'NONE','not compressed'));f.writeframes((signal*32767).astype('<i2').tobytes())
  samples.append((2,n,p.read_bytes()))
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=data[12:16];struct.pack_into('<II',header,16,len(samples),512);chunks=[];off=512
 for i,(g,n,wav) in enumerate(samples):
  nxt=off+16+len(wav) if i<len(samples)-1 else 0;chunks.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off+=16+len(wav);(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'MatsuriShinju.snd').write_bytes(bytes(header)+b''.join(chunks));return len(samples)

def main():
 for sub in ['sprites','effects','sound']:(A/sub).mkdir(parents=True,exist_ok=True)
 sheet=Image.open(SOURCE/'Matsuri_sheet.png').convert('RGBA');assert sheet.size==(707,3000)
 rgb,labels,items=components(sheet);groups=select_rows(items);records=[];manifest=[];roles={};bodies=[]
 def put(g,n,im,axis,body=False,**info):
  p=A/('sprites' if body else 'effects')/f'{g}_{n}.png';im.save(p);records.append((g,n,p,axis));manifest.append(dict(group=g,number=n,file=str(p.relative_to(CHAR)),axis=axis,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest(),**info))
 for form,parts in groups.items():
  roles[str(form)]={};number=0
  for role,found in parts.items():
   assert found,(form,role);roles[str(form)][role]=[]
   for row in found:
    x,y,right,bottom=row['box'];v=np.array(sheet.crop(row['box']));v[:,:,3]=np.where(labels[y:bottom,x:right]==row['id'],255,0);im=Image.fromarray(v)
    put(form,number,im,anchor(im),True,role=role,source_rectangle=row['box'],source_component=row['id'],redrawn=False,native_scale=True);roles[str(form)][role].append(number);bodies.append((form,number,role,im));number+=1
 # Uncloaked form has its own original poses. Missing action roles use its
 # relevant original punches/kicks, never a miniature or a redrawn character.
 for role,fallback in dict(air='kick',cloak='spin',palm='punch',thrust='punch',stretch='punch',gesture='charge',mark='punch',bloom='spin').items():roles['1'][role]=roles['1'].get(role,roles['1'][fallback])
 roles['0']['guard']=roles['0']['hurt'][:1]
 def cut(box):
  v=np.array(sheet.crop(box));v[:,:,3]=np.where(np.all(v[:,:,:3]==rgb[0,0],axis=2),0,255);im=Image.fromarray(v);return im.crop(im.getbbox())
 cloak=[(97,1923,139,1972),(148,1923,213,1967),(229,1925,300,1963),(311,1927,388,1958),(149,2012,180,2055),(193,2017,231,2060),(244,2023,289,2064),(306,2026,355,2057)]
 for n,box in enumerate(cloak):
  im=cut(box);put(8600,n,im,(im.width//2,im.height//2),source_rectangle=box,original_matsuri_effect=True)
 im=cut((301,1664,476,1698));put(8603,0,im,(im.width//2,im.height//2),source_rectangle=(301,1664,476,1698),original_matsuri_effect=True)
 jura=Sff2(ROOT/'JuraShinju/JuraShinju.sff')
 for g,count in [(8601,3),(8602,2)]:
  for n in range(count):
   im,axis=jura.image(g,n);put(g,n,im,axis,original_jura_wood=True)
 for n in range(4):
  im,axis=jura.image(8600,n);put(8604,n,im,axis,original_jura_wood=True)
 shared=Sff2(ROOT/'MitsukiTBV/MitsukiTBV.sff')
 for g,count in [(8700,4),(8710,4),(8720,6),(8670,11),(8900,24),(8910,5),(8820,5)]:
  for n in range(count):
   im,axis=shared.image(g,n);put(g,n,im,axis,shared_project_effect=True)
 atlas=Image.open(ROOT/'source_material/Matsuri_generated/water_atlas.png').convert('RGBA')
 for n in range(8):
  col,row=n%4,n//4;im=atlas.crop((col*atlas.width//4,row*atlas.height//2,(col+1)*atlas.width//4,(row+1)*atlas.height//2));im=im.crop(im.getbbox())
  im=im.resize((76,round(im.height*76/im.width)),Image.Resampling.NEAREST);v=np.array(im);v[:,:,3]=np.where(v[:,:,3]>=128,255,0);v[:,:,:3]=np.array(im.convert('RGB').quantize(colors=255).convert('RGB'));im=Image.fromarray(v)
  put(8630,n,im,(round(im.width*.73),im.height//2) if n<4 else (im.width//2,im.height//2),ai_generated_effect=True,contains_character=False)
 for n,size in [(0,(25,25)),(1,(120,140))]:
  im=Image.open(A/'sprites/0_0.png').crop((8,4,34,34));factor=min(size[0]/im.width,size[1]/im.height);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST);canvas=Image.new('RGBA',size);canvas.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));put(9000,n,canvas,(0,0),portrait_from_original=True)
 pack_sff(records,CHAR/'MatsuriShinju.sff');count=soundbank();(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n');(A/'poses.json').write_text(json.dumps(roles,indent=2)+'\n')
 board=Image.new('RGB',(1200,((len(bodies)+9)//10)*120),(24,27,35));d=ImageDraw.Draw(board)
 for i,(form,num,role,im) in enumerate(bodies):
  x=i%10*120;y=i//10*120;board.paste(im,(x+(120-im.width)//2,y),im);d.text((x+2,y+101),f'{form},{num} {role}',fill='white')
 board.save(ROOT/'previews/MatsuriShinju_original_poses.png');print('Matsuri assets:',len(bodies),'original body entries,',len(records),'sprites,',count,'sounds')
if __name__=='__main__':main()
