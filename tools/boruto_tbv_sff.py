#!/usr/bin/env python3
"""MUGEN 1.1 SFF 2.01: lossless PNG32 RGBA plus legacy indexed effects."""
import io,struct
from PIL import Image
from boruto_source import rle8_encode,rle8_decode

def save_sff(entries,path):
    count=len(entries);pc=sum(bool(e[5]) for e in entries.values())
    ph=512;sh=ph+pc*16;ld=sh+count*28;offset=0;pals=[];sprites=[];chunks=[]
    for (g,n),(w,h,x,y,pixels,palette) in entries.items():
        if palette:
            pi=len(pals);pals.append(struct.pack('<4H2I',1,pi+1,256,0,offset,1024));chunks.append(palette);offset+=1024
            fmt,depth=2,8;block=rle8_encode(pixels)
        else:
            pi=0;fmt,depth=12,32;png=io.BytesIO();Image.frombytes('RGBA',(w,h),pixels).save(png,format='PNG')
            block=struct.pack('<I',w*h*4)+png.getvalue()
        sprites.append(struct.pack('<4H2hH2B2I2H',g,n,w,h,x,y,0,fmt,depth,offset,len(block),pi,0));chunks.append(block);offset+=len(block)
        padding=(-offset)%4
        if padding:chunks.append(bytes(padding));offset+=padding
    h=bytearray(512);h[:12]=b'ElecbyteSpr\0';h[12:16]=bytes((0,1,0,2));h[24:28]=bytes((0,1,0,2));struct.pack_into('<8I',h,36,sh,count,ph,pc,ld,offset,ld+offset,0)
    path.write_bytes(bytes(h)+b''.join(pals)+b''.join(sprites)+b''.join(chunks))

def read_sff(path):
    b=path.read_bytes();assert b[:16]==b'ElecbyteSpr\0'+bytes((0,1,0,2));sh,count,ph,pc,ld,ls,_,_=struct.unpack_from('<8I',b,36);pals=[]
    for i in range(pc):
        _,_,colors,_,off,size=struct.unpack_from('<4H2I',b,ph+i*16);assert colors==256 and size==1024 and off+size<=ls;pals.append(b[ld+off:ld+off+size])
    entries={}
    for i in range(count):
        g,n,w,h,x,y,link,fmt,depth,off,size,pal,flags=struct.unpack_from('<4H2hH2B2I2H',b,sh+i*28);assert w and h and not flags and off+size<=ls
        data=b[ld+off:ld+off+size]
        if fmt==12:
            assert depth==32 and struct.unpack_from('<I',data)[0]==w*h*4
            im=Image.open(io.BytesIO(data[4:])).convert('RGBA');assert im.size==(w,h);pixels=im.tobytes();palette=b''
        else:
            assert depth==8 and fmt in [0,2] and pal<pc;pixels=data if fmt==0 else rle8_decode(data,w*h);palette=pals[pal]
        entries[g,n]=(w,h,x,y,pixels,palette)
    return entries
