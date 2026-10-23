#!/usr/bin/env python3
"""Decode the supplied SFFv1 losslessly. No Mamushi artwork is redrawn."""
from pathlib import Path
import hashlib,io,json,struct,wave
import numpy as np
from PIL import Image,ImageDraw
from build_archives import png_to_indexed
from make_combo_preview import Sff2
from read_reference_sff import ReferenceSff

ROOT=Path(__file__).resolve().parents[1]
CHAR=ROOT/'Mamushi';ASSETS=CHAR/'assets';SOURCE=ROOT/'source_material/Mamushi_original'

def pack_sff(records,path):
    packed=[]
    for g,n,p,axis in records:
        pixels,palette,w,h,*_=png_to_indexed(p)
        packed.append((g,n,w,h,*axis,pixels,palette))
    ph=512;sh=ph+len(packed)*16;ld=sh+len(packed)*28;pal=[];spr=[];chunks=[];off=0
    for i,(g,n,w,h,x,y,pixels,palette) in enumerate(packed):
        pal.append(struct.pack('<HHHHII',1,i+1,256,0,off,len(palette)));chunks.append(palette);off+=len(palette)
        spr.append(struct.pack('<HHHHhhHBBIIHH',g,n,w,h,x,y,0,0,8,off,len(pixels),i,0));chunks.append(pixels);off+=len(pixels)
    header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,1,0,2));header[24:28]=bytes((0,1,0,2));struct.pack_into('<IIIIIIII',header,36,sh,len(packed),ph,len(packed),ld,off,ld+off,0)
    path.write_bytes(bytes(header)+b''.join(pal)+b''.join(spr)+b''.join(chunks))

def main():
    (ASSETS/'sprites').mkdir(parents=True,exist_ok=True);(ASSETS/'sound').mkdir(exist_ok=True);(ASSETS/'effects').mkdir(exist_ok=True)
    b=(SOURCE/'AC_Mamushi.sff').read_bytes();count,offset=struct.unpack_from('<II',b,20)
    palette=None;previous=[];records=[];manifest=[]
    for i in range(count):
        nxt,size,x,y,g,n,link,same=struct.unpack_from('<IIhhHHHB',b,offset)
        payload=b[offset+32:offset+32+size]
        if size:
            if len(payload)>768 and payload[-769]==12:palette=payload[-768:]
            elif palette is not None:payload+=bytes([12])+palette
            picture=Image.open(io.BytesIO(payload));picture.load();indices=np.array(picture)
            rgba=np.array(picture.convert('RGBA'));rgba[:,:,3]=np.where(indices==0,0,255)
            image=Image.fromarray(rgba)
        else:image=previous[link].copy()
        previous.append(image);offset=nxt
        if g==9000:continue # The original two portraits are entirely empty.
        p=ASSETS/'sprites'/f'{g}_{n}.png';image.save(p)
        records.append((g,n,p,(x,y)));manifest.append(dict(group=g,number=n,file=str(p.relative_to(CHAR)),axis=[x,y],source_index=i,source_rgba_sha256=hashlib.sha256(image.tobytes()).hexdigest(),redrawn=False))
    # A safe fallback for default common animations, using the genuine idle.
    records.append((0,0,ASSETS/'sprites/0_4.png',(19,67)))
    stand=Image.open(ASSETS/'sprites/0_4.png').convert('RGBA')
    portrait=stand.crop((10,0,30,24))
    for n,size in [(0,(25,25)),(1,(120,140))]:
        im=Image.new('RGBA',size);p=portrait.copy();p.thumbnail(size,Image.Resampling.NEAREST)
        scale=min(size[0]/portrait.width,size[1]/portrait.height);p=portrait.resize((round(portrait.width*scale),round(portrait.height*scale)),Image.Resampling.NEAREST)
        im.alpha_composite(p,((size[0]-p.width)//2,(size[1]-p.height)//2));path=ASSETS/f'portrait_{n}.png';im.save(path);records.append((9000,n,path,(0,0)))
    # Shared non-character effects, already used and credited by this project.
    reference=Sff2(ROOT/'Eida/Eida.sff')
    for group,original,total,factor in [(8700,8400,4,1),(8710,8510,4,.65),(8720,8420,6,.18)]:
        for n in range(total):
            im,axis=reference.image(original,n);size=(max(1,round(im.width*factor)),max(1,round(im.height*factor)))
            im=im.resize(size,Image.Resampling.NEAREST);path=ASSETS/'effects'/f'{group}_{n}.png';im.save(path)
            records.append((group,n,path,tuple(round(v*factor) for v in axis)))
    # Presentation layers only. All original body/weapon pixels stay intact.
    code=ReferenceSff(ROOT/'source_material/Shibai_Code_reference/Code.sff')
    for group,original,numbers in [(8730,556,range(11,16)),(8740,7005,range(5)),(8750,7015,range(9)),(8760,1235,range(22)),(8770,10030,[0])]:
        for n,source_n in enumerate(numbers):
            im,axis=code.image(original,source_n);path=ASSETS/'effects'/f'{group}_{n}.png';im.save(path)
            records.append((group,n,path,axis))
    pack_sff(records,CHAR/'Mamushi.sff')
    (ASSETS/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ASSETS/'source.json').write_text(json.dumps(dict(source='source_material/Mamushi_original/AC_Mamushi.sff',sha256=hashlib.sha256(b).hexdigest(),sprite_author='Vahidras / Vaydra as credited on supplied sheet',original_author='misterioso924',original_body_entries=len(manifest),uniform_scale=1,body_rgba_preserved=True,ai_redrawn=False,fx_source='Existing Eida groups 8400,8510,8420; Code by MUGEN STARS groups 556,7005,7015,1235,10030 for wind, debris and violet blast only; see credits'),indent=2)+'\n')
    sound=(ROOT/'Eida/Eida.snd').read_bytes();number,off=struct.unpack_from('<II',sound,16);samples={}
    for i in range(number):
        nxt,size,g,n=struct.unpack_from('<IIII',sound,off)
        if g==1 and n in [0,4,5,6,7,8,9,19,21]:samples[g,n]=sound[off+16:off+16+size]
        off=nxt
    rate=22050;rng=np.random.default_rng(264);durations={30:.35,31:.28,32:.65,33:.45}
    for n,duration in durations.items():
        t=np.arange(round(rate*duration))/rate;noise=rng.normal(0,1,len(t));smooth=np.convolve(noise,np.ones(9)/9,mode='same')
        if n==30:values=(.22*smooth+.18*np.sin(2*np.pi*(135*t-60*t*t)))*np.sin(np.pi*t/duration)**2
        elif n==31:values=(.42*smooth+.25*np.sin(2*np.pi*75*t))*np.exp(-12*t)*np.minimum(1,t*300)
        elif n==32:values=(.24*smooth+.12*np.sin(2*np.pi*130*t))*(.65+.35*np.sin(2*np.pi*22*t))*np.sin(np.pi*t/duration)
        else:values=(.42*smooth+.32*np.sin(2*np.pi*(85*t-55*t*t)))*np.exp(-10*t)*np.minimum(1,t*300)
        stream=io.BytesIO()
        with wave.open(stream,'wb') as wav:wav.setparams((1,2,rate,0,'NONE','not compressed'));wav.writeframes(np.clip(values*32767,-32768,32767).astype('<i2').tobytes())
        samples[1,n]=stream.getvalue()
    header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=sound[12:16];struct.pack_into('<II',header,16,len(samples),512);parts=[];off=512
    for i,((g,n),payload) in enumerate(sorted(samples.items())):
        nxt=off+16+len(payload) if i+1<len(samples) else 0;parts.append(struct.pack('<IIII',nxt,len(payload),g,n)+payload);off=nxt
        (ASSETS/'sound'/f'{g}_{n}.wav').write_bytes(payload)
    (CHAR/'Mamushi.snd').write_bytes(bytes(header)+b''.join(parts))
    canvas=Image.new('RGB',(1200,((len(manifest)+9)//10)*110),(42,45,52));draw=ImageDraw.Draw(canvas)
    for i,m in enumerate(manifest):
        im=Image.open(CHAR/m['file']);im.thumbnail((115,88),Image.Resampling.NEAREST);x=i%10*120;y=i//10*110;canvas.paste(im,(x,y),im);draw.text((x+2,y+90),f"{m['group']},{m['number']}",fill='white')
    canvas.save(ROOT/'previews/Mamushi_sprites_originales.png')
    print(f'Mamushi: {len(manifest)} original body/weapon entries preserved, {len(records)} total SFF sprites, {len(samples)} nonverbal sounds')

if __name__=='__main__':main()
