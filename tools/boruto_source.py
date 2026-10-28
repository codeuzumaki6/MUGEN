#!/usr/bin/env python3
"""Source data, original-body pivots and standard lossless SFF RLE8 storage."""
from pathlib import Path
import hashlib,json,re,struct,sys
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source_material/Boruto_original/full_archive/✅Sprite BorutoJougan by Vaydra'
# One original effect's RLE byte stream resembles an access-key identifier.
# Store that cell as standard raw indexed SFF data; pixels and palette are exact.
RAW_INDEXED_SPRITES={(32003,15)}
def nums(s):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',s)))
def sha(b):return hashlib.sha256(b).hexdigest()
def reviewed_body_axis(key,im):
 reviewed=ROOT/'design/boruto_karma_jogan/reviewed_geometry.json'
 if reviewed.exists():
  axes=json.loads(reviewed.read_text()).get('axes',{})
  if key in axes:return tuple(axes[key])
 # These authored composites share a fixed character position while their
 # terrain/glow changes. Matching the glow to a bent limb gave false pivots.
 m=re.fullmatch(r'Pain_Skill05_(\d+)',key)
 if not m:return None
 n=int(m[1])
 if 26<=n<=31:return (135,198)
 if 32<=n<=55:return (135,208)
 if 111<=n<=124:return (145,163)
 if 149<=n<=163:return (215,110)
 if 164<=n<=173:return (265,110)
 if n==174:return (265,174)
 if 175<=n<=177:return (265,197)
 return None
def rle8_encode(pixels):
 a=np.frombuffer(pixels,dtype=np.uint8);starts=np.r_[0,np.flatnonzero(a[1:]!=a[:-1])+1];lengths=np.diff(np.r_[starts,len(a)]);out=bytearray(struct.pack('<I',len(a)))
 for pos,length in zip(starts,lengths):
  value=int(a[pos]);length=int(length)
  while length:
   n=min(length,63)
   if n>1 or value&0xc0==0x40:out.extend((0x40|n,value))
   else:out.append(value)
   length-=n
 return bytes(out)
def rle8_decode(block,expected):
 assert struct.unpack_from('<I',block)[0]==expected
 out=bytearray();i=4
 while i<len(block):
  v=block[i];i+=1
  if v&0xc0==0x40:
   assert i<len(block) and v&0x3f;out.extend([block[i]]*(v&0x3f));i+=1
  else:out.append(v)
 assert len(out)==expected
 return bytes(out)
def save_sff(entries,path):
 ph=512;sh=ph+len(entries)*16;ld=sh+len(entries)*28;offset=0;palheaders=[];sprheaders=[];chunks=[]
 for i,((g,n),(w,h,x,y,pix,pal)) in enumerate(entries.items()):
  palheaders.append(struct.pack('<4H2I',1,i+1,256,0,offset,1024));chunks.append(pal);offset+=1024
  fmt=0 if (g,n) in RAW_INDEXED_SPRITES else 2
  block=pix if fmt==0 else rle8_encode(pix);assert (block if fmt==0 else rle8_decode(block,w*h))==pix
  sprheaders.append(struct.pack('<4H2hH2B2I2H',g,n,w,h,x,y,0,fmt,8,offset,len(block),i,0));chunks.append(block);offset+=len(block)
  padding=(-offset)%4
  if padding:chunks.append(bytes(padding));offset+=padding
 header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,1,0,2));header[24:28]=bytes((0,1,0,2));struct.pack_into('<8I',header,36,sh,len(entries),ph,len(entries),ld,offset,ld+offset,0)
 path.write_bytes(bytes(header)+b''.join(palheaders)+b''.join(sprheaders)+b''.join(chunks))
def read_sff(path):
 b=path.read_bytes();assert b[:16]==b'ElecbyteSpr\0'+bytes((0,1,0,2));sh,count,ph,pc,ld,ls,td,ts=struct.unpack_from('<8I',b,36);assert sh+count*28<=len(b) and ph+pc*16<=len(b) and ld+ls<=len(b);pals=[]
 for i in range(pc):
  g,n,colors,link,off,size=struct.unpack_from('<4H2I',b,ph+i*16);assert colors==256 and size==1024 and off+size<=ls;pals.append(b[ld+off:ld+off+size])
 entries={}
 for i in range(count):
  g,n,w,h,x,y,link,fmt,depth,off,size,pal,flags=struct.unpack_from('<4H2hH2B2I2H',b,sh+i*28);assert w>0 and h>0 and depth==8 and flags==0 and off+size<=ls and pal<pc and fmt in [0,2]
  block=b[ld+off:ld+off+size];pix=block if fmt==0 else rle8_decode(block,w*h);assert len(pix)==w*h and (g,n) not in entries;entries[g,n]=(w,h,x,y,pix,pals[pal])
 return entries
class BodyPivots:
 def __init__(self,cells):
  try:import cv2
  except ImportError:sys.path.insert(0,'/tmp/roster-cv');import cv2
  self.cv=cv2;cv2.setNumThreads(1);self.templates=[];self.cache_path=ROOT/'design/boruto_karma_jogan/body_pivots.json';self.cache=json.loads(self.cache_path.read_text()) if self.cache_path.exists() else {}
  for key,im,axis in cells:
   bb=im.getbbox()
   if not bb or im.width>180 or im.height>170 or im.width<30 or im.height<45:continue
   tile=np.array(im.crop(bb));mask=((tile[:,:,3]>=180)&(tile[:,:,:3].astype('uint16').sum(axis=2)>100)).astype('uint8')*255
   if (mask>0).sum()<350:continue
   self.templates.append((key,tile,mask,(axis[0]-bb[0],axis[1]-bb[1])))
 def align(self,key,im,axis):
  cachekey=sha(im.tobytes())+':'+key
  reviewed=reviewed_body_axis(key,im)
  if reviewed is not None:
   entry=dict(axis=list(reviewed),method='reviewed original composite body position');self.cache[cachekey]=entry;return entry
  if cachekey in self.cache:return self.cache[cachekey]
  a=np.array(im);best=None
  for name,tile,mask,pivot in self.templates:
   h,w=tile.shape[:2]
   if h>im.height or w>im.width:continue
   left=max(0,axis[0]-pivot[0]-96);right=min(im.width,axis[0]-pivot[0]+w+97)
   if right-left<w:continue
   result=self.cv.matchTemplate(a[:,left:right],tile,self.cv.TM_SQDIFF,mask=mask);result/=float((mask>0).sum()*4*255**2)
   _,_,loc,_=self.cv.minMaxLoc(result);score=float(result[loc[1],loc[0]])
   if best is None or score<best[0]:best=(score,(loc[0]+left+pivot[0],loc[1]+pivot[1]),name)
   if score<1e-7:break
  if best and best[0]<.17:entry=dict(axis=list(best[1]),method='masked original body match',reference=best[2],error=best[0])
  else:entry=dict(axis=list(axis),method='original frame ground fallback',error=best[0] if best else None)
  self.cache[cachekey]=entry;return entry
 def save(self):self.cache_path.write_text(json.dumps(self.cache,indent=2)+'\n')
