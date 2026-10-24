#!/usr/bin/env python3
"""Exact per-sprite palettes: reserve transparency without quantizing opaque art."""
import struct
import numpy as np
from PIL import Image

def pack_sff(records,path):
 images=[]
 for g,n,p,axis in records:
  im=Image.open(p).convert('RGBA');v=np.array(im);mask=v[:,:,3]>=128;rgb=v[:,:,:3][mask].astype(np.uint32);keys=(rgb[:,0]<<16)|(rgb[:,1]<<8)|rgb[:,2];unique,inverse=np.unique(keys,return_inverse=True);colors=np.column_stack(((unique>>16)&255,(unique>>8)&255,unique&255)).astype('uint8');assert len(colors)<=255,(g,n,len(colors))
  pixels=np.zeros((im.height,im.width),dtype=np.uint8);pixels[mask]=inverse+1;pal=np.zeros((256,4),dtype=np.uint8);pal[1:,3]=255;pal[1:len(colors)+1,:3]=colors;images.append((g,n,im.width,im.height,*axis,pixels.tobytes(),pal.tobytes()))
 ph=512;sh=ph+len(images)*16;ld=sh+len(images)*28;headers=[];sprites=[];chunks=[];off=0
 for i,(g,n,w,h,x,y,pixels,palette) in enumerate(images):
  headers.append(struct.pack('<HHHHII',1,i+1,256,0,off,len(palette)));chunks.append(palette);off+=len(palette);sprites.append(struct.pack('<HHHHhhHBBIIHH',g,n,w,h,x,y,0,0,8,off,len(pixels),i,0));chunks.append(pixels);off+=len(pixels)
 header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,1,0,2));header[24:28]=bytes((0,1,0,2));struct.pack_into('<8I',header,36,sh,len(images),ph,len(images),ld,off,ld+off,0);path.write_bytes(bytes(header)+b''.join(headers)+b''.join(sprites)+b''.join(chunks))
