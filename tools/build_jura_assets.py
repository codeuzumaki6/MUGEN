#!/usr/bin/env python3
"""Extract Vaydra's public Jura sheet; keep its drawing and build standalone assets."""
from pathlib import Path
import hashlib,io,json,struct,wave
import numpy as np
from PIL import Image,ImageDraw
from build_mamushi_assets import pack_sff
from make_combo_preview import Sff2
from read_reference_sff import ReferenceSff

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'JuraShinju';A=CHAR/'assets';SOURCE=ROOT/'source_material/Jura_original'
# Source rectangles include every extremity. Axes follow the planted body,
# rather than centering extended punches on the whole sprite rectangle.
BODIES=[
 ('idle0',(10,12,51,100),32),('idle1',(60,12,102,100),82),('idle2',(109,12,155,100),131),
 ('hurt0',(4,105,52,187),29),('hurt1',(64,106,119,184),93),('hurt_air0',(121,106,183,190),143),
 ('hurt_air1',(187,116,261,183),212),('hurt_air2',(265,113,349,175),293),('prone',(350,120,438,156),394),('crouch',(438,113,491,169),466),
 ('punch_ready',(4,190,52,272),28),('punch0',(66,192,146,267),94),('punch1',(156,192,236,267),184),
 ('punch_recover',(251,191,332,269),279),('palm',(330,187,411,265),358),
 ('kick_ready',(12,282,60,364),38),('kick0',(66,288,146,363),89),('kick_ready1',(158,279,206,367),182),('kick1',(216,284,296,360),239),
 ('wood0',(15,386,61,474),37),('wood1',(74,386,120,474),96),('root0',(14,491,60,579),36),('root1',(76,491,119,579),97),
 ('bijudama',(12,591,58,675),34),('rinnegan',(10,686,53,774),31),('claw0',(0,793,50,881),25),('claw1',(66,793,109,881),87),
 ('ocular',(12,897,58,988),37),('run0',(8,1002,88,1072),42),('run1',(94,1001,176,1071),127),('run2',(183,1003,264,1073),215),
 ('air0',(9,1087,81,1169),44),('air1',(85,1086,158,1167),122),
 ('jump0',(17,1181,65,1269),40),('jump1',(77,1186,155,1263),110),('jump2',(156,1184,234,1261),193)]
EFFECTS={
 8600:[(138,435,158,477),(173,418,197,477),(218,395,245,477),(272,374,305,477)],
 8601:[(130,510,224,573),(223,481,348,580),(345,436,500,588)],
 8602:[(123,597,300,799),(307,592,484,811)],
 8603:[(128,821,236,869),(143,830,251,878),(156,841,264,889)],
 8604:[(310,818,485,992)],
 8605:[(79,887,145,948),(145,887,203,948),(202,887,251,948)],
 8606:[(263,904,277,918)]}

# Only the three iris shades in the supplied body poses change. Keep their
# pixel positions, black outlines and every other part of the source drawing.
RINNEGAN_PALETTE={(128,33,33):(95,83,122),
                  (185,45,45):(164,148,190),
                  (188,70,70):(204,194,224)}

def normal_rinnegan(im):
    pixels=np.array(im);original=pixels.copy();changed=0
    face=np.indices(pixels.shape[:2])[0]<24
    for old,new in RINNEGAN_PALETTE.items():
        mask=face & (original[:,:,3]>0) & np.all(original[:,:,:3]==old,axis=2)
        pixels[mask,:3]=new;changed+=int(mask.sum())
    return Image.fromarray(pixels),changed

def cut(sheet,box):
    im=sheet.crop(box).convert('RGBA');v=np.array(im);r,g,b=[v[:,:,i].astype(int) for i in range(3)]
    background=(g>r+45)&(g>b+45)&(r<65)&(b<65)
    v[:,:,3]=np.where(background,0,255);im=Image.fromarray(v)
    bb=im.getbbox();assert bb,box
    return im.crop(bb),(box[0]+bb[0],box[1]+bb[1])

def main():
    for sub in ['sprites','effects','sound']:(A/sub).mkdir(parents=True,exist_ok=True)
    source=SOURCE/'Jura_sheet.png';sheet=Image.open(source).convert('RGBA');assert sheet.size==(500,1300)
    records=[];manifest=[]
    for n,(role,box,absolute_axis) in enumerate(BODIES):
        im,origin=cut(sheet,box);im,eye_pixels=normal_rinnegan(im);path=A/'sprites'/f'0_{n}.png';im.save(path)
        axis=(absolute_axis-origin[0],im.height-1)
        records.append((0,n,path,axis));manifest.append(dict(group=0,number=n,role=role,file=str(path.relative_to(CHAR)),axis=list(axis),source_rectangle=box,redrawn=False,eye_pixels_recolored=eye_pixels,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest()))
    for group,boxes in EFFECTS.items():
        for n,box in enumerate(boxes):
            im,origin=cut(sheet,box);axis=(im.width//2,im.height-1) if group in [8600,8601,8602] else (im.width//2,im.height//2)
            path=A/'effects'/f'{group}_{n}.png';im.save(path);records.append((group,n,path,axis))
    shared=Sff2(ROOT/'Mamushi/Mamushi.sff')
    for group,count in [(8700,4),(8710,4),(8720,6)]:
        for n in range(count):
            im,axis=shared.image(group,n);p=A/'effects'/f'{group}_{n}.png';im.save(p);records.append((group,n,p,axis))
    code=ReferenceSff(ROOT/'source_material/Shibai_Code_reference/Code.sff')
    for dest,src,numbers in [(8800,10030,range(10)),(8810,1034,range(7)),(8820,7005,range(5)),(8830,7013,range(30)),(8840,1235,range(22)),(8880,90,[3]),(8881,200,[24]),(8900,576,range(24)),(8910,556,range(11,16)),(8920,7015,range(9))]:
        if any((src,sn) not in code.sprites for sn in numbers):numbers=sorted(k[1] for k in code.sprites if k[0]==src)
        for n,sn in enumerate(numbers):
            im,axis=code.image(src,sn);p=A/'effects'/f'{dest}_{n}.png';im.save(p);records.append((dest,n,p,axis))
    head=Image.open(A/'sprites/0_0.png').crop((8,0,30,27))
    for n,size in [(0,(25,25)),(1,(120,140))]:
        p=head.copy();p.thumbnail(size,Image.Resampling.NEAREST);factor=min(size[0]/head.width,size[1]/head.height);p=head.resize((round(head.width*factor),round(head.height*factor)),Image.Resampling.NEAREST)
        im=Image.new('RGBA',size);im.alpha_composite(p,((size[0]-p.width)//2,(size[1]-p.height)//2));path=A/f'portrait_{n}.png';im.save(path);records.append((9000,n,path,(0,0)))
    pack_sff(records,CHAR/'JuraShinju.sff')
    original=(ROOT/'Shibai/Shibai.snd').read_bytes();number,off=struct.unpack_from('<II',original,16);samples={}
    for _ in range(number):
        nxt,size,g,n=struct.unpack_from('<IIII',original,off);samples[g,n]=original[off+16:off+16+size];off=nxt
    rate=22050;rng=np.random.default_rng(1127927142)
    for n,duration in [(40,.65),(41,1.1),(42,.45),(43,1.5)]:
        t=np.arange(round(rate*duration))/rate;noise=rng.normal(0,1,len(t));rumble=np.convolve(noise,np.ones(23)/23,mode='same');env=np.minimum(1,t*55)*np.exp(-t/(duration*.4))
        if n==40:v=(.3*rumble+.14*np.sin(2*np.pi*(130*t+350*t*t)))*np.sin(np.pi*t/duration)
        elif n==41:v=(.45*rumble+.21*np.sin(2*np.pi*46*t)+.08*noise)*env
        elif n==42:v=(.35*rumble+.22*np.sin(2*np.pi*(240*t-260*t*t)))*env
        else:v=(.45*rumble+.23*np.sin(2*np.pi*(32*t+24*t*t))+.1*noise)*env
        out=io.BytesIO()
        with wave.open(out,'wb') as f:f.setparams((1,2,rate,0,'NONE','not compressed'));f.writeframes(np.clip(v*32767,-32768,32767).astype('<i2').tobytes())
        samples[1,n]=out.getvalue()
    header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<II',header,16,len(samples),512);parts=[];off=512
    for i,((g,n),payload) in enumerate(sorted(samples.items())):
        nxt=off+16+len(payload) if i+1<len(samples) else 0;parts.append(struct.pack('<IIII',nxt,len(payload),g,n)+payload);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(payload)
    (CHAR/'JuraShinju.snd').write_bytes(bytes(header)+b''.join(parts))
    (A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (A/'source.json').write_text(json.dumps(dict(sheet='Vahidras / Vaydra, Juura Shinju',page='https://www.deviantart.com/vahidras/art/Juura-Shinju-1127927142',sha256=hashlib.sha256(source.read_bytes()).hexdigest(),body_entries=36,redrawn=False,ai_generated=False,eye_color='Normal Rinnegan: pale violet, only original red iris pixels replaced',eye_palette=[dict(original=old,corrected=new) for old,new in RINNEGAN_PALETTE.items()],green_mask='G>R+45 and G>B+45, R/B<65',packed_palette_limit=255,tree_reference_only='Jura_tree_reference.jpg',voices=False),indent=2)+'\n')
    board=Image.new('RGB',(1200,720),(28,31,40));d=ImageDraw.Draw(board)
    for i,m in enumerate(manifest):
        im=Image.open(CHAR/m['file']);im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);im.thumbnail((190,150),Image.Resampling.NEAREST);x=i%6*200;y=i//6*120;im.thumbnail((190,96),Image.Resampling.NEAREST);board.paste(im,(x+(200-im.width)//2,y),im);d.text((x+3,y+100),f"{m['number']}: {m['role']}",fill='white')
    (ROOT/'previews').mkdir(exist_ok=True);board.save(ROOT/'previews/Jura_sprites.png')
    print('Packed Jura:',len(records),'sprites;',len(manifest),'body poses from Vaydra;',len(samples),'nonverbal sounds')

if __name__=='__main__':main()
