#!/usr/bin/env python3
"""Extract new animation cells, calibrate both forms, and pack MUGEN archives."""
from pathlib import Path
import hashlib,io,json,struct,wave
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects
from build_mamushi_assets import pack_sff
from make_combo_preview import Sff2
from read_reference_sff import ReferenceSff

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Shibai';A=CHAR/'assets'
SOURCE=ROOT/'source_material/Shibai_generated'

def clean_cell(im):
    a=np.array(im.convert('RGBA'));mask=a[:,:,3]>=128
    labels,count=label(mask)
    if count:
        sizes=np.bincount(labels.ravel());sizes[0]=0
        mask &= np.isin(labels,np.flatnonzero(sizes>=max(5,sizes.max()*.015)))
    a[:,:,3]=np.where(mask,255,0)
    return Image.fromarray(a)

def main():
    for sub in ['sprites','effects','sound']:(A/sub).mkdir(parents=True,exist_ok=True)
    records=[];manifest=[];im=Image.open(SOURCE/'shibai_poses.png').convert('RGBA');w,h=im.size
    # Generated rows are not perfectly regular. Extract connected whole bodies,
    # never crop using an assumed grid (which could cut heads/legs).
    data=np.array(im);labels,_=label(data[:,:,3]>=128);counts=np.bincount(labels.ravel());columns={i:[] for i in range(6)}
    for ident,slices in enumerate(find_objects(labels),1):
        if counts[ident]<1000:continue
        yy,xx=slices;col=min(5,int((xx.start+xx.stop)/2/w*6));body=data[yy,xx].copy();body[:,:,3]=np.where(labels[yy,xx]==ident,255,0)
        columns[col].append((yy.start,Image.fromarray(body)))
    assert all(len(v)==8 for v in columns.values()),'Expected eight complete silhouettes per column'
    for col in columns:columns[col].sort(key=lambda row:row[0])
    repairs=[]
    if (SOURCE/'shibai_awakened_repairs.png').exists():
        repair=Image.open(SOURCE/'shibai_awakened_repairs.png').convert('RGBA');rd=np.array(repair);rl,_=label(rd[:,:,3]>=128);rc=np.bincount(rl.ravel());parts=[]
        for ident,sl in enumerate(find_objects(rl),1):
            if rc[ident]<1000:continue
            yy,xx=sl;body=rd[yy,xx].copy();body[:,:,3]=np.where(rl[yy,xx]==ident,255,0);parts.append((int((yy.start+yy.stop)/2/repair.height*2),int((xx.start+xx.stop)/2/repair.width*3),Image.fromarray(body)))
        parts.sort(key=lambda p:(p[0],p[1]));assert len(parts)==6,'Repair sheet must contain six complete bodies';repairs=[p[2] for p in parts]
    for form in range(2):
        cells=[columns[n%6][form*4+n//6][1] for n in range(24)]
        if form==1:
            assert repairs,'Awakened charge/guard/release/getup frames require completed lower limbs'
            repair_scale=float(np.median([p.height for p in cells[:3]]))/float(np.median([p.height for p in repairs[:3]]))
            cells[18:24]=[p.resize((round(p.width*repair_scale),round(p.height*repair_scale)),Image.Resampling.NEAREST) for p in repairs]
        heights=[cells[i].getbbox()[3]-cells[i].getbbox()[1] for i in range(3)]
        factor=78/float(np.median(heights))
        for n,cell in enumerate(cells):
            bbox=cell.getbbox();body=cell.crop(bbox)
            body=body.resize((max(1,round(body.width*factor)),max(1,round(body.height*factor))),Image.Resampling.NEAREST)
            # One scale per form: crouch/hurt stay naturally lower. Do not enlarge each pose.
            rgb=body.convert('RGB').quantize(colors=32,method=Image.Quantize.MEDIANCUT).convert('RGBA');rgb.putalpha(body.getchannel('A'));body=rgb
            p=A/'sprites'/f'{form}_{n}.png';body.save(p)
            axis=(body.width//2,body.height-1)
            records.append((form,n,p,axis));manifest.append(dict(group=form,number=n,file=str(p.relative_to(CHAR)),axis=list(axis),uniform_scale=factor,role=['idle0','idle1','idle2','walk0','walk1','walk2','jump_start','jump_up','jump_down','crouch','hurt0','hurt1','palm_ready','palm','sweep','rising_palm','push','invoke','charge','reflect','cast','release','getup','prone'][n]))
    fx=Image.open(SOURCE/'shibai_effects.png').convert('RGBA');fw,fh=fx.size
    sizes=[(70,112),(65,158),(44,94),(60,50),(68,46),(132,130)]
    for row,(tw,th) in enumerate(sizes):
        for n in range(6):
            cell=clean_cell(fx.crop((round(n*fw/6),round(row*fh/6),round((n+1)*fw/6),round((row+1)*fh/6))))
            cell=cell.crop(cell.getbbox());ratio=min(tw/cell.width,th/cell.height)
            cell=cell.resize((max(1,round(cell.width*ratio)),max(1,round(cell.height*ratio))),Image.Resampling.NEAREST)
            p=A/'effects'/f'{8800+row*10}_{n}.png';cell.save(p)
            axis=(cell.width//2,cell.height-1 if row in [0,1,2] else cell.height//2)
            records.append((8800+row*10,n,p,axis))
    # Otsutsuki stakes and cubes use authored geometry, with explicit visible boundaries.
    for group in [8860,8870]:
        for n in range(4):
            if group==8860:
                pic=Image.new('RGBA',(42,24));d=ImageDraw.Draw(pic)
                d.polygon([(1,12),(34,9),(41,12),(34,15)],fill=(18,14,27),outline=(164,126,196))
                d.line([(4,11),(32,10)],fill=(222,219,243),width=1);axis=(21,12)
            else:
                pic=Image.new('RGBA',(78,78));d=ImageDraw.Draw(pic);a=3+n
                d.polygon([(a,16),(50,3),(75,22),(28,37)],fill=(49,39,62),outline=(179,154,211))
                d.polygon([(a,16),(28,37),(28,75),(a,53)],fill=(17,13,24),outline=(116,96,149))
                d.polygon([(28,37),(75,22),(75,59),(28,75)],fill=(30,23,42),outline=(179,154,211))
                for y in [39,49,59]:d.line([(39,y),(60,y-6)],fill=(85,67,107))
                axis=(39,77)
            # Sukunahikona-inspired reveal: the object expands from a small
            # stored object into its full combat silhouette, on a fixed canvas.
            full=pic;factor=[.2,.45,.75,1][n];small=full.resize((max(1,round(full.width*factor)),max(1,round(full.height*factor))),Image.Resampling.NEAREST)
            pic=Image.new('RGBA',full.size)
            pic.alpha_composite(small,((full.width-small.width)//2,(full.height-small.height) if group==8870 else (full.height-small.height)//2))
            p=A/'effects'/f'{group}_{n}.png';pic.save(p);records.append((group,n,p,axis))
    reference=Sff2(ROOT/'Mamushi/Mamushi.sff')
    for g,count in [(8700,4),(8710,4),(8720,6)]:
        for n in range(count):
            pic,axis=reference.image(g,n);p=A/'effects'/f'{g}_{n}.png';pic.save(p);records.append((g,n,p,axis))
    code=ReferenceSff(ROOT/'source_material/Shibai_Code_reference/Code.sff')
    pic,axis=code.image(90,3);p=A/'effects/8880_0.png';pic.save(p);records.append((8880,0,p,axis))
    for n in range(8):
        pic,axis=code.image(590,n);factor=.18;pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST);p=A/'effects'/f'8890_{n}.png';pic.save(p);records.append((8890,n,p,tuple(round(v*factor) for v in axis)))
    base=Image.open(A/'sprites/0_0.png').convert('RGBA');head=base.crop((max(0,base.width//2-12),0,min(base.width,base.width//2+12),25))
    for n,size in [(0,(25,25)),(1,(120,140))]:
        pic=Image.new('RGBA',size);crop=head.resize((size[0],size[0]),Image.Resampling.NEAREST);pic.alpha_composite(crop,(0,(size[1]-size[0])//2));p=A/f'portrait_{n}.png';pic.save(p);records.append((9000,n,p,(0,0)))
    pack_sff(records,CHAR/'Shibai.sff')
    # Existing nonverbal project sounds, plus original wind/thunder/space effects.
    b=(ROOT/'Mamushi/Mamushi.snd').read_bytes();count,off=struct.unpack_from('<II',b,16);samples={}
    for _ in range(count):
        nxt,size,g,n=struct.unpack_from('<IIII',b,off)
        if g==1 and n in [0,4,5,6,7,8,9,19,21]:samples[g,n]=b[off+16:off+16+size]
        off=nxt
    rate=22050;rng=np.random.default_rng(6261)
    for n,duration in [(30,.75),(31,.9),(32,.5),(33,.6),(34,1.2),(35,1.8)]:
        t=np.arange(round(rate*duration))/rate;noise=rng.normal(0,1,len(t));low=np.convolve(noise,np.ones(15)/15,mode='same');env=np.minimum(1,t*60)*np.exp(-t/(duration*.4))
        if n==30:v=(.55*low+.08*np.sin(2*np.pi*(180*t-75*t*t)))*np.sin(np.pi*t/duration)
        elif n==31:v=(.24*noise+.4*low+.22*np.sin(2*np.pi*47*t))*env
        elif n==32:v=(.18*low+.2*np.sin(2*np.pi*(350*t-300*t*t)))*np.sin(np.pi*t/duration)
        elif n==33:v=(.4*low+.35*np.sin(2*np.pi*(65*t-25*t*t)))*env
        elif n==34:v=(.12*low+.16*np.sin(2*np.pi*110*t)+.1*np.sin(2*np.pi*165*t))*np.sin(np.pi*t/duration)**2
        else:v=(.2*low+.22*np.sin(2*np.pi*(50*t+25*t*t))+.08*np.sin(2*np.pi*330*t))*np.sin(np.pi*t/duration)**2
        out=io.BytesIO()
        with wave.open(out,'wb') as f:f.setparams((1,2,rate,0,'NONE','not compressed'));f.writeframes(np.clip(v*32767,-32768,32767).astype('<i2').tobytes())
        samples[1,n]=out.getvalue()
    header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<II',header,16,len(samples),512);chunks=[];off=512
    for i,((g,n),payload) in enumerate(sorted(samples.items())):
        nxt=off+16+len(payload) if i+1<len(samples) else 0;chunks.append(struct.pack('<IIII',nxt,len(payload),g,n)+payload);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(payload)
    (CHAR/'Shibai.snd').write_bytes(bytes(header)+b''.join(chunks))
    (A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (A/'source.json').write_text(json.dumps(dict(original='Vahidras, supplied JPG with two poses',new_body_animation='AI-assisted expansion from the supplied designs; 24 articulated poses per form',generated_sheets={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.glob('*.png')},body_height=78,scale_is_constant_per_form=True,voices=False),indent=2)+'\n')
    board=Image.new('RGB',(1280,1080),(28,30,40));d=ImageDraw.Draw(board)
    for i,m in enumerate(manifest):
        pic=Image.open(CHAR/m['file']);pic=pic.resize((pic.width*2,pic.height*2),Image.Resampling.NEAREST)
        if pic.width>150 or pic.height>158:pic.thumbnail((150,158),Image.Resampling.NEAREST)
        x=i%8*160;y=i//8*180;board.paste(pic,(x+(160-pic.width)//2,y),pic);d.text((x+3,y+164),f"{m['group']}:{m['role']}",fill='white')
    (ROOT/'previews').mkdir(exist_ok=True);board.save(ROOT/'previews/Shibai_sprites.png')
    print('Packed',len(records),'sprites and',len(samples),'nonverbal sounds')

if __name__=='__main__':main()
