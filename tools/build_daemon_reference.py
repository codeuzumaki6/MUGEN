#!/usr/bin/env python3
"""Import the supplied Daemon model and supplemental poses at one child scale.

The two source poses are cropped from the unchanged Vahidras JPG. Additional
poses are AI artwork following that model, never claimed as original frames.
Only transparency, nearest-neighbour normalization and fixed-origin packing
are performed here; no drawings or visible colours are synthesized by Python.
"""
from pathlib import Path
import hashlib
import json
import re

import numpy as np
from PIL import Image
from scipy.ndimage import label

ROOT=Path(__file__).resolve().parents[1]
CHAR=ROOT/'Eida'
DESIGN=ROOT/'design/Daemon_original'
OUT=CHAR/'assets/daemon'
AXIS=(48,54)
CANVAS=(96,56)
BOXES={'stand':(5,52,170,461),'run':(190,135,530,465)}
ROW_BOXES=[(20,330),(330,641),(641,908),(908,1160)]
# The generated sheet's gutters were inspected. It does not divide into four
# equal-height rows; equal crops would cut feet and paste neighbouring hair.
GENERATED_MAP={1:0,2:1,3:0,4:2,5:3,6:4,7:5,8:6,9:7,10:8,
               11:9,12:10,13:11,14:12,15:13,17:14,18:15}

def main_component(image):
    pixels=np.array(image.convert('RGBA'))
    labels,count=label(pixels[:,:,3]>=160)
    assert count,'empty sprite'
    sizes=np.bincount(labels.ravel());sizes[0]=0
    pixels[:,:,3]=np.where(labels==sizes.argmax(),255,0).astype('uint8')
    image=Image.fromarray(pixels)
    bounds=image.getbbox();assert bounds
    return image,bounds

def source_pose(source,box):
    pic=source.crop(box).convert('RGBA');pixels=np.array(pic)
    rgb=pixels[:,:,:3].astype(float);red,green,blue=rgb.transpose(2,0,1)
    # The original is JPEG: select its matte chroma, not the teal of the hair.
    distance=np.linalg.norm(rgb-np.array([20,111,42]),axis=2)
    matte=(green>red*1.8)&(green>blue*1.8)&(distance<65)
    pixels[matte,3]=0
    pic,bounds=main_component(Image.fromarray(pixels))
    assert all([bounds[0]>0,bounds[1]>0,bounds[2]<pic.width,bounds[3]<pic.height]),bounds
    return pic,bounds

def pack(pic,bounds,factor):
    # Use the centre between the feet in the bottom 8% of the silhouette.
    # A single sheet factor preserves crouches and raised kicks at their real
    # heights. Never stretch each pose to the same opaque-height rectangle.
    left,top,right,bottom=bounds
    feet=pic.getchannel('A').crop((0,bottom-max(3,round((bottom-top)*.08)),pic.width,bottom)).getbbox()
    assert feet
    anchor=(feet[0]+feet[2])/2
    figure=pic.crop(bounds)
    size=(max(1,round(figure.width*factor)),max(1,round(figure.height*factor)))
    figure=figure.resize(size,Image.Resampling.NEAREST)
    x=round(AXIS[0]-(anchor-left)*factor);y=AXIS[1]-figure.height
    assert x>0 and y>0 and x+figure.width<CANVAS[0],(bounds,size,x,y)
    canvas=Image.new('RGBA',CANVAS)
    canvas.alpha_composite(figure,(x,y))
    return canvas,dict(trim_box=list(bounds),native_figure_size=list(size),feet_source_x=anchor,packed_pos=[x,y])

def assets():
    OUT.mkdir(parents=True,exist_ok=True)
    original=Image.open(DESIGN/'daemon_vahidras_original.jpg').convert('RGBA')
    source={name:source_pose(original,box) for name,box in BOXES.items()}
    original_factor=49/(source['stand'][1][3]-source['stand'][1][1])
    sheet=Image.open(DESIGN/'supplemental_poses.png').convert('RGBA')
    cells={}
    for index in range(16):
        col,row=index%4,index//4
        box=(col*sheet.width//4,ROW_BOXES[row][0],(col+1)*sheet.width//4,ROW_BOXES[row][1])
        cell,bounds=main_component(sheet.crop(box))
        assert min(bounds[:2])>0 and bounds[2]<cell.width and bounds[3]<cell.height,(index,bounds)
        cells[index]=(cell,bounds,box)
    supplemental_factor=48/(cells[0][1][3]-cells[0][1][1])
    manifest=[]
    for number in range(19):
        if number in (0,16):
            name='stand' if number==0 else 'run';pic,bounds=source[name];factor=original_factor
            origin=dict(kind='original supplied pose',source='design/Daemon_original/daemon_vahidras_original.jpg',source_box=list(BOXES[name]),ai_redrawn=False)
        else:
            index=GENERATED_MAP[number];pic,bounds,box=cells[index];factor=supplemental_factor
            origin=dict(kind='AI supplemental pose based on supplied model',source='design/Daemon_original/supplemental_poses.png',source_cell=index,source_box=list(box),ai_redrawn=True)
        canvas,geometry=pack(pic,bounds,factor)
        path=OUT/f'daemon_{number}.png';canvas.save(path)
        manifest.append(dict(group=1000,number=number,file=str(path.relative_to(CHAR)),axis=list(AXIS),scale=factor,source_sha256=hashlib.sha256((ROOT/origin['source']).read_bytes()).hexdigest(),**origin,**geometry))
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

def install_air():
    path=CHAR/'Eida.air';text=path.read_text()
    def replace(number,body):
        nonlocal text
        pattern=rf'(?ims)^\[Begin Action {number}\].*?(?=^\[Begin Action|\Z)'
        text,count=re.subn(pattern,lambda _:f'[Begin Action {number}]\n{body.strip()}\n\n',text,count=1)
        assert count,number
    hurt='Clsn2Default: 1\n Clsn2[0] = -11,-48,11,0\n'
    # Original neutral and run poses now have dedicated references.
    replace(1030,hurt+'1000,0,0,0,6\n1000,1,0,0,6\n1000,2,0,0,6\n1000,0,0,0,6')
    replace(1510,hurt+'Loopstart\n1000,16,0,0,3\n1000,17,0,0,3\n1000,18,0,0,3\n1000,17,0,0,3')
    replace(1020,hurt+'1000,2,0,0,5\n1000,14,0,0,7\n1000,15,0,0,7\n1000,2,0,0,5')
    replace(1350,'Clsn2Default: 1\n Clsn2[0] = -22,-72,22,0\nClsn1Default: 1\n Clsn1[0] = -25,-82,48,4\nLoopstart\n1000,2,0,0,6\n1000,14,0,0,6\n1000,15,0,0,6\n1000,14,0,0,6')
    replace(1524,'Clsn2Default: 1\n Clsn2[0] = -13,-32,13,0\n1000,12,0,0,4\nClsn1: 1\n Clsn1[0] = 2,-15,31,-2\n1000,13,0,0,5\n1000,12,0,0,4\n1000,12,0,0,6')
    replace(1584,'Clsn2Default: 1\n Clsn2[0] = -13,-32,13,0\n1000,12,0,0,4\n1000,1,0,0,4')
    replace(1590,'1000,1,0,0,4\n1000,0,0,0,4')
    # Match the new hands/feet rather than retaining the old model's reach.
    attack_boxes={5:(6,-39,25,-27),6:(4,-39,26,-24),
                  9:(3,-38,30,-20),10:(3,-44,30,-15)}
    for number in (1000,1010,1040,1520,1521,1522,1523,1525):
        pattern=rf'(?ims)^\[Begin Action {number}\].*?(?=^\[Begin Action|\Z)'
        block=re.search(pattern,text);assert block
        def contact(match):
            pose=int(match[2]);assert pose in attack_boxes,pose
            return 'Clsn1[0] = '+','.join(map(str,attack_boxes[pose]))+match[1]
        replacement=re.sub(r'Clsn1\[0\]\s*=\s*[^\r\n]+(\n1000,(\d+),[^\r\n]+)',contact,block[0])
        text=text[:block.start()]+replacement+text[block.end():]
    path.write_text(text.rstrip()+'\n')

if __name__=='__main__':
    manifest=assets();install_air()
    print(f'Imported {len(manifest)} Daemon entries: 2 original supplied poses, 16 distinct supplemental poses; native 96x56 canvas, feet 48,54')
