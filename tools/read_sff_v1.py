#!/usr/bin/env python3
"""Read linked PCX sprites in supplied SFF v1 archives without redrawing."""
from pathlib import Path
import io,struct
import numpy as np
from PIL import Image
class Sff1:
 def __init__(self,path):
  self.data=Path(path).read_bytes();assert self.data[:12]==b'ElecbyteSpr\0' and self.data[15]==1
  self.groups,self.count,off,self.subheader=struct.unpack_from('<4I',self.data,16);self.sprites={};self.entries=[];self.cache={};palette=None
  for i in range(self.count):
   nxt,size,x,y,g,n,link,same=struct.unpack_from('<IIhhHHHB',self.data,off);raw=self.data[off+self.subheader:off+self.subheader+size]
   if size and len(raw)>=769 and raw[-769]==12:palette=raw[-768:]
   entry={'group':g,'number':n,'axis':(x,y),'link':link,'same_palette':same,'raw':raw,'palette':palette,'index':i};self.sprites[g,n]=entry;self.entries.append(entry);off=nxt
 def image(self,g,n):
  entry=self.sprites[g,n];v=entry;seen=set()
  while not v['raw']:
   assert v['index'] not in seen;seen.add(v['index']);v=self.entries[v['link']]
  key=v['index']
  if key not in self.cache:
   raw=v['raw']
   if not (len(raw)>=769 and raw[-769]==12):raw+=b'\x0c'+v['palette']
   im=Image.open(io.BytesIO(raw));im.load();indices=np.array(im);rgba=np.array(im.convert('RGBA'));rgba[:,:,3]=np.where(indices==0,0,255);self.cache[key]=Image.fromarray(rgba)
  return self.cache[key].copy(),entry['axis']
