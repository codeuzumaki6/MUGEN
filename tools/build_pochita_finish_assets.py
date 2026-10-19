#!/usr/bin/env python3
"""Extract the generated ultimate poses and overlay effects, preserving the art."""
from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import label,find_objects
import json,hashlib,io,wave
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'PochitaTrueForm';SOURCE=ROOT/'design/Pochita_remates'

def append_finish_assets(metadata,review):
 records=[];im=Image.open(SOURCE/'ultimate_poses.png').convert('RGBA');a=np.array(im.getchannel('A'))>=128
 # The generated layout is two rows; separate full bodies, not fixed cell crops.
 sy=[];start=None
 for y,v in enumerate(list(a.any(axis=1))+[False]):
  if v and start is None:start=y
  if not v and start is not None:
   if y-start>50:sy.append((start,y))
   start=None
 assert len(sy)==2,sy
 poses=[]
 for y0,y1 in sy:
  labels,n=label(a[y0:y1],np.ones((3,3)));objects=find_objects(labels);areas=np.bincount(labels.ravel())
  ids=sorted([i+1 for i,s in enumerate(objects) if areas[i+1]>5000],key=lambda i:objects[i-1][1].start)
  assert len(ids)==4,[(areas[i],objects[i-1]) for i in ids]
  for i in ids:
   s=objects[i-1];mask=Image.fromarray((labels==i).astype('uint8')*255);bbox=mask.getbbox()
   pic=im.crop((0,y0,im.width,y1));pic.putalpha(mask);pic=pic.crop(bbox)
   assert bbox[0]>0 and bbox[2]<im.width and y0+bbox[1]>0 and y0+bbox[3]<im.height,('clipped pose',bbox)
   poses.append((pic,[bbox[0],y0+bbox[1],bbox[2],y0+bbox[3]]))
 factor=72/poses[0][0].height;metadata['ultimate']=[]
 for i,(pic,box) in enumerate(poses):
  pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST);foot=pic.getchannel('A').crop((0,pic.height-7,pic.width,pic.height)).getbbox();axis=((foot[0]+foot[2])//2+2,pic.height+2)
  padded=Image.new('RGBA',(pic.width+4,pic.height+4));padded.alpha_composite(pic,(2,2));folder=CHAR/'assets/sprites/ultimate';folder.mkdir(parents=True,exist_ok=True);path=folder/f'{i}.png';padded.save(path)
  pixels=np.array(padded);body=(pixels[:,:,3]>128)&~((pixels[:,:,0]>70)&(pixels[:,:,0]>pixels[:,:,1]*1.3));extent=int(np.where(body)[1].max())-axis[0]
  metadata['ultimate'].append(dict(group=3100,number=i,file=str(path.relative_to(CHAR)),size=padded.size,axis=axis,attack_extent=extent,source_sheet='ultimate_poses',source_cell=i,source_box=box));records.append((3100,i,path,axis));review.append(('ultimate',i,padded))
 fx=Image.open(SOURCE/'effects.png').convert('RGBA');w,h=fx.size
 # Gutters were inspected on the original sheet; these are extraction bounds.
 xs=[0,round(w*.205),round(w*.497),round(w*.768),w];ys=[0,round(h*.371),round(h*.724),h]
 for row,(name,group,canvas_size,axis,factor) in enumerate([('slash_fx',9200,(160,104),(80,52),.25),('blood_fx',9201,(160,100),(48,50),.20),('ground_fx',9202,(160,70),(80,64),.24)]):
  metadata[name]=[];folder=CHAR/'assets/sprites'/name;folder.mkdir(parents=True,exist_ok=True)
  for i in range(4):
   box=(xs[i],ys[row],xs[i+1],ys[row+1]);pic=fx.crop(box);pic.putalpha(pic.getchannel('A').point(lambda v:255 if v>=128 else 0));bbox=pic.getchannel('A').getbbox();assert bbox;pic=pic.crop(bbox);pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
   canvas=Image.new('RGBA',canvas_size)
   if row==0:pos=(axis[0]-pic.width//2,axis[1]-pic.height//2)
   elif row==1:pos=(axis[0]-pic.width//2 if i==0 else axis[0]-8,axis[1]-pic.height//2)
   else:pos=(axis[0]-pic.width//2,axis[1]-pic.height)
   assert pos[0]>=0 and pos[1]>=0 and pos[0]+pic.width<=canvas.width and pos[1]+pic.height<=canvas.height,(name,i,pic.size,pos)
   canvas.alpha_composite(pic,pos);path=folder/f'{i}.png';canvas.save(path)
   metadata[name].append(dict(group=group,number=i,file=str(path.relative_to(CHAR)),size=canvas.size,axis=axis,source_sheet='effects',source_cell=row*4+i,source_box=box));records.append((group,i,path,axis));review.append((name,i,canvas))
 return records

def append_finish_sounds(records,manifest):
 folder=CHAR/'assets/sound';fs=22050
 def read(name):
  with wave.open(str(folder/name),'rb') as w:
   assert w.getframerate()==fs and w.getnchannels()==1 and w.getsampwidth()==2
   return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 motor=read('chainsaw_long.wav');cut=read('chainsaw_cut.wav');impact=read('impact_heavy.wav');light=read('impact_light.wav')
 rng=np.random.default_rng(20261018)
 for number,name,duration in [(7,'motor_grind_finish',.74),(8,'cross_saw_cut',.5),(9,'heavy_saw_cleave',.92)]:
  out=np.zeros(round(fs*duration));t=np.arange(len(out))/fs
  def layer(source,gain,start=0,rate=1):
   sample=np.interp(np.arange(0,len(source)-1,rate),np.arange(len(source)),source);a=round(start*fs);n=min(len(out)-a,len(sample));out[a:a+n]+=sample[:n]*gain
  if number==7:layer(motor,.8);layer(cut,.45,.04,1.3);layer(light,.25,.10)
  elif number==8:layer(cut,.7,0,1.4);layer(cut,.45,.08,1.75);layer(light,.4,.04)
  else:
   layer(motor,.5,0,1.15);layer(impact,.8,.17);out+=np.sin(2*np.pi*(90*t-24*t*t))*np.exp(-8*t)*.14;out+=rng.normal(0,1,len(out))*np.exp(-10*t)*.035
  envelope=np.minimum(1,t/.008)*np.minimum(1,(duration-t)/.08);out*=envelope;peak=np.max(np.abs(out));out*=.92/max(peak,.92)
  stream=io.BytesIO()
  with wave.open(stream,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(fs);w.writeframes((out*32767).astype('<i2').tobytes())
  payload=stream.getvalue();path=folder/(name+'.wav');path.write_bytes(payload);records.append((1,number,payload));manifest.append({'group':1,'number':number,'filename':path.name,'type':'original nonverbal sound mix','sources':['chainsaw_long.wav','chainsaw_cut.wav','impact_heavy.wav','impact_light.wav'],'duration':duration,'sha256':hashlib.sha256(payload).hexdigest(),'voice':False})
