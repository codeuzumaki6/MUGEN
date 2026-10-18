#!/usr/bin/env python3
"""Split the exact uploaded Pochita sheet and pack a MUGEN 1.1 SFFv2.
No AI redraw, interpolation, per-pose stretching or portrait-in-idle shortcuts.
"""
from pathlib import Path
import json,struct,hashlib
from PIL import Image,ImageChops,ImageDraw,ImageOps
from build_archives import png_to_indexed
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'PochitaTrueForm';ASSETS=DEST/'assets'
SOURCE=ROOT/'denji_pochita_chainsaw_devil_sprite_sheet_by_spider_monkie_dkky600.png'
ROWS=[('idle',0,178,210,550,6),('walk',20,245,275,550,7),('run',100,290,328,600,7),
('crouch',10,353,385,550,6),('jump',40,412,470,550,7),('air1',600,532,560,650,7),
('air2',610,592,621,500,5),('air3',620,652,683,700,6),('attack1',200,771,801,600,7),
('attack2',210,823,858,600,6),('attack3',220,890,929,1595,17),('attack3b',230,940,970,1000,17),
('attack4',240,1003,1044,700,6),('attack5',250,1059,1100,900,8),('damage',5000,1125,1172,950,15)]
im=Image.open(SOURCE).convert('RGBA');assert im.size==(5934,5764)
r,g,b,_=im.split();green=ImageChops.multiply(ImageChops.subtract(g,r).point(lambda x:255 if x>22 else 0),ImageChops.subtract(g,b).point(lambda x:255 if x>22 else 0));mask=ImageChops.invert(green);im.putalpha(mask)
# All poses use one scale. Crouches and horizontal frames remain shorter.
FACTOR=.84;scale=im.width/1600;records=[];metadata={};review=[]
for name,group,y0,y1,xmax,expected in ROWS:
    box=(round(45*scale),round(y0*scale),round(xmax*scale),round(y1*scale));region=mask.crop(box)
    if name=='run':region.paste(0,(0,0,round(55*scale),1100-box[1]))
    if name=='jump':region.paste(0,(0,0,round(55*scale),1550-box[1]))
    if name=='attack4':region.paste(0,(0,0,round(55*scale),round((1006-y0)*scale)))
    if name=='damage':region.paste(0,(0,0,round(55*scale),round((1129-y0)*scale)))
    projection=region.getprojection()[0];runs=[];start=None
    for x,value in enumerate(projection+[0]):
        if value and start is None:start=x
        if not value and start is not None:runs.append([start,x]);start=None
    joined=[]
    for a,b in runs:
        if joined and a-joined[-1][1]<6:joined[-1][1]=b
        else:joined.append([a,b])
    joined=[q for q in joined if q[1]-q[0]>14];assert len(joined)==expected,(name,len(joined),expected)
    metadata[name]=[]
    folder=ASSETS/'sprites'/name;folder.mkdir(parents=True,exist_ok=True)
    for index,(a,b) in enumerate(joined):
        cut=(a+box[0],box[1],b+box[0],box[3]);picture=im.crop(cut);picture.putalpha(region.crop((a,0,b,region.height)));bbox=picture.getchannel('A').getbbox();assert bbox
        assert bbox[1]>0 and bbox[3]<picture.height,(name,index,'clipped vertically',bbox)
        picture=picture.crop(bbox);picture=picture.resize((round(picture.width*FACTOR),round(picture.height*FACTOR)),Image.Resampling.NEAREST)
        # The lowest occupied band anchors feet; blades/hair cannot pull the origin sideways.
        foot=picture.getchannel('A').crop((0,max(0,picture.height-7),picture.width,picture.height)).getbbox();axis_x=(foot[0]+foot[2])//2
        padded=Image.new('RGBA',(picture.width+4,picture.height+4));padded.alpha_composite(picture,(2,2));path=folder/f'{index}.png';padded.save(path)
        axis=(axis_x+2,picture.height+2)
        records.append((group,index,path,axis));metadata[name].append(dict(group=group,number=index,file=str(path.relative_to(DEST)),axis=axis,source_box=[cut[0]+bbox[0],cut[1]+bbox[1],cut[0]+bbox[2],cut[1]+bbox[3]],size=padded.size));review.append((name,index,padded))
# Standard portraits from the supplied large illustration; it is never a body frame.
portrait=im.crop((3950,3750,5450,5250));portrait=ImageOps.fit(portrait,(120,140),method=Image.Resampling.LANCZOS)
for n,size in [(0,(25,25)),(1,(120,140))]:
    path=ASSETS/f'portrait_{n}.png';portrait.resize(size,Image.Resampling.LANCZOS).save(path);records.append((9000,n,path,(0,0)))
# Pack indexed palettes, zero transparency, and uncompressed SFFv2 sprite payloads.
packed=[]
for group,index,path,axis in records:
    pixels,palette,w,h,_,_=png_to_indexed(path)
    if group!=9000:
        palette=bytearray(palette)
        swaps={(17,15,25):(8,8,11),(49,46,67):(24,25,29),(65,60,90):(38,39,43),(102,96,132):(85,86,90),(93,87,123):(65,66,70),(131,125,160):(155,157,161),(81,13,47):(95,7,17),(121,17,69):(165,12,24),(189,0,62):(225,15,24),(71,4,26):(65,3,7)}
        for pi in range(256):
            color=tuple(palette[pi*4:pi*4+3])
            if color in swaps:palette[pi*4:pi*4+3]=bytes(swaps[color])
        palette=bytes(palette)
    packed.append((group,index,w,h,*axis,pixels,palette))
ph=512;sh=ph+len(packed)*16;ld=sh+len(packed)*28;palheaders=[];sprheaders=[];chunks=[];off=0
for i,(group,index,w,h,x,y,pixels,palette) in enumerate(packed):
    palheaders.append(struct.pack('<HHHHII',1,i+1,256,0,off,len(palette)));chunks.append(palette);off+=len(palette)
    sprheaders.append(struct.pack('<HHHHhhHBBIIHH',group,index,w,h,x,y,0,0,8,off,len(pixels),i,0));chunks.append(pixels);off+=len(pixels)
header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,1,0,2));header[24:28]=bytes((0,1,0,2));struct.pack_into('<IIIIIIII',header,36,sh,len(packed),ph,len(packed),ld,off,ld+off,0)
(DEST/'PochitaTrueForm.sff').write_bytes(bytes(header)+b''.join(palheaders)+b''.join(sprheaders)+b''.join(chunks))
(ASSETS/'sprites.json').write_text(json.dumps(metadata,indent=2)+'\n')
(ASSETS/'source.json').write_text(json.dumps({'author_credit':'Ducksysys, shared by Spider-Monkie','source_page':'https://www.deviantart.com/spider-monkie/art/Denji-Pochita-Chainsaw-Devil-Sprite-Sheet-1244509920','original_size':im.size,'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'uniform_scale':FACTOR},indent=2)+'\n')
canvas=Image.new('RGB',(1200,((len(review)+9)//10)*125),'#3a3e48');draw=ImageDraw.Draw(canvas)
for i,(name,index,picture) in enumerate(review):
    picture.thumbnail((115,100),Image.Resampling.NEAREST);x=i%10*120;y=i//10*125;canvas.paste(picture,(x+(120-picture.width)//2,y+20),picture);draw.text((x+2,y+2),f'{name}:{index}',fill='white')
(ROOT/'previews/Pochita_sprites_extraidos.png').parent.mkdir(exist_ok=True);canvas.save(ROOT/'previews/Pochita_sprites_extraidos.png')
print('Packed',len(packed),'sprites;',len(review),'original body frames; uniform scale',FACTOR)
