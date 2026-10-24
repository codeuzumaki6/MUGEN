#!/usr/bin/env python3
"""Reproducible fleet repair over the accepted roster at BASE.

Keep hit/cost/controller contracts; import complete supplied Senki sequences,
preserve each old collision window, repair reception and finite CPU chains.
"""
from pathlib import Path
import collections,hashlib,json,plistlib,re,struct,subprocess
import sys
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
BASE='38dd5362fe76610a7c7d5a1c033868deb37519ec'
CHARS=['Eida','PochitaTrueForm','Mamushi','Shibai','JuraShinju','MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju']
EYES={(128,33,33):(79,92,150),(185,45,45):(157,168,222),(188,70,70):(204,207,241),
      (137,13,13):(79,92,150),(168,69,69):(181,185,226),
      (200,56,29):(157,168,222),(139,34,16):(79,92,150)}

def original(path):return subprocess.check_output(['git','show',BASE+':'+str(path.relative_to(ROOT))],cwd=ROOT)
def sha(data):return hashlib.sha256(data).hexdigest()
def nums(text):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',text)))

class Archive:
    def __init__(self,data):
        sh,count,ph,pc,ld,ls,td,ts=struct.unpack_from('<8I',data,36);self.entries={}
        palettes=[]
        for i in range(pc):
            g,n,c,link,off,size=struct.unpack_from('<4H2I',data,ph+i*16)
            assert size==1024
            palettes.append(data[ld+off:ld+off+size])
        for i in range(count):
            g,n,w,h,x,y,link,fmt,depth,off,size,pal,flags=struct.unpack_from('<4H2hH2B2I2H',data,sh+i*28)
            assert fmt==0 and flags==0 and depth==8 and size==w*h
            self.entries[g,n]=(w,h,x,y,data[ld+off:ld+off+size],palettes[pal])
    def image(self,key):
        w,h,x,y,pix,pal=self.entries[key]
        rgba=np.array(list(pal),dtype=np.uint8).reshape(256,4)[np.frombuffer(pix,dtype=np.uint8).reshape(h,w)]
        return Image.fromarray(rgba),(x,y)
    def put(self,key,im,axis):
        v=np.array(im.convert('RGBA'));mask=v[:,:,3]>=128
        colors=v[:,:,:3][mask];unique=np.unique(colors,axis=0)
        if len(unique)>255:
            rgb=Image.fromarray(v[:,:,:3]);q=rgb.quantize(colors=255,method=Image.Quantize.MEDIANCUT);pix=np.array(q,dtype=np.uint8)+1
            pal=np.zeros((256,4),dtype=np.uint8);p=q.getpalette();pal[1:,:3]=np.array(p[:765],dtype=np.uint8).reshape(255,3)
        else:
            keys=(v[:,:,0].astype('uint32')<<16)|(v[:,:,1].astype('uint32')<<8)|v[:,:,2]
            uk=(unique[:,0].astype('uint32')<<16)|(unique[:,1].astype('uint32')<<8)|unique[:,2]
            pix=np.zeros(mask.shape,dtype=np.uint8);pix[mask]=np.searchsorted(uk,keys[mask])+1
            pal=np.zeros((256,4),dtype=np.uint8);pal[1:len(unique)+1,:3]=unique
        pix[~mask]=0;pal[1:,3]=255
        self.entries[key]=(im.width,im.height,*axis,pix.tobytes(),pal.tobytes())
    def save(self,path):
        ph=512;sh=ph+len(self.entries)*16;ld=sh+len(self.entries)*28;off=0;ps=[];ss=[];chunks=[]
        for i,((g,n),(w,h,x,y,pix,pal)) in enumerate(self.entries.items()):
            ps.append(struct.pack('<4H2I',1,i+1,256,0,off,len(pal)));chunks.append(pal);off+=len(pal)
            ss.append(struct.pack('<4H2hH2B2I2H',g,n,w,h,x,y,0,0,8,off,len(pix),i,0));chunks.append(pix);off+=len(pix)
        header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,1,0,2));header[24:28]=bytes((0,1,0,2));struct.pack_into('<8I',header,36,sh,len(ss),ph,len(ps),ld,off,ld+off,0)
        path.write_bytes(bytes(header)+b''.join(ps)+b''.join(ss)+b''.join(chunks))

def recolor(im,axis=None):
    a=np.array(im);before=a.copy();count=0
    for old,new in EYES.items():
        mask=(before[:,:,3]>0)&np.all(before[:,:,:3]==old,axis=2)
        if axis:
            yy,xx=np.indices(mask.shape)
            mask&=(abs(xx-axis[0])<32)&(yy<axis[1]-35)&(yy>axis[1]-115)
        # Without an atlas pivot these exact shades are the native iris
        # palette, including heads rotated downwards in aerial/get-hit poses.
        # Ryu's coat lining uses different gold/orange palette entries.
        count+=int(mask.sum());a[mask,:3]=new
    return Image.fromarray(a),count

class Atlas:
    def __init__(self,stem,char,archive):
        self.char=char;self.archive=archive;self.frames={};self.used={};self.manifest=[]
        self.anchor_cache_path=ROOT/'design/roster_repair'/f'{char}_anchors.json'
        self.anchor_cache=json.loads(self.anchor_cache_path.read_text()) if self.anchor_cache_path.exists() else {}
        self.templates=[]
        for key,entry in archive.entries.items():
            g,n=key;w,h,ax,ay,*_=entry
            eligible=(g in [0,1]) if char!='Eida' else (g<400 or g==1000)
            if not eligible or h<40:continue
            im,_=archive.image(key);left=max(0,ax-20);top=max(0,ay-90);right=min(w,ax+22);bottom=min(h,ay+1)
            if right-left<12 or bottom-top<35:continue
            tile=np.array(im.crop((left,top,right,bottom)));mask=(tile[:,:,3]>=128).astype('uint8')*255
            if (mask>0).sum()<300:continue
            self.templates.append((key,tile,mask,(ax-left,ay-top)))
        paths=sorted((ROOT/'source_material'/(stem+'_full_original')).rglob('*.plist'))
        for i,path in enumerate(paths):
            png=path.with_suffix('.png')
            if not png.exists():continue
            im=Image.open(png).convert('RGBA')
            if im.width<=1 or 'Shino_Skill' in path.name:continue
            data=plistlib.loads(path.read_bytes())['frames']
            prefix={'Matsuri':'Hashirama_Idle_','Mamushi':'Orochimaru_Idle_','Ryu':'Shino_Idle_','Mitsuki':'Gaara_Idle_','Jura':'Orochimaru_Idle_','Eida':'Chiyo_Idle_','Hidari':'Zabuza_Idle_'}[stem]
            idle=next((v for k,v in data.items() if k.startswith(prefix)),None)
            baseline=45
            if idle:
                x,y,w,h=map(int,nums(idle['frame']));off=nums(idle['offset']);bb=im.crop((x,y,x+w,y+h)).getbbox()
                if bb:baseline=bb[3]-h/2-off[1]
            # Secondary Daemon and Jura FX sheets get their own idle anchor.
            if path.stem=='Parents':baseline=38
            for key,v in data.items():
                if 'frame' not in v:continue
                x,y,w,h=map(int,nums(v['frame']))
                if w<=0 or h<=0 or x+w>im.width or y+h>im.height:continue
                frame=im.crop((x,y,x+w,y+h))
                if v.get('rotated'):frame=frame.transpose(Image.Transpose.ROTATE_90)
                if not frame.getbbox():continue
                ox,oy=nums(v.get('offset','{0,0}'))
                axis=(round(frame.width/2-ox),round(frame.height/2+oy+baseline))
                self.frames[key.removesuffix('.png')]=(frame,axis,path,v,i)
    def align_body(self,im,key,axis):
        """Match the actual body, independent of the wide effect's rectangle.

        These mod plists use hand-authored offsets and untrimmed frames; their
        Y offset is not a reliable MUGEN foot pivot. Match original body pixels
        with transparency masks instead of centering the entire VFX frame.
        """
        if self.char=='HidariShinju' and key in ['Zabuza_Skill03_04','Zabuza_Skill03_05']:
            # Same 480x279 canvas/body position as frames 06/07. Their
            # impact flash occludes the body; the bottom is ground debris.
            return (265,183),dict(method='adjacent matching source sequence',reference='Zabuza_Skill03_07',error=None)
        cachekey=sha(im.tobytes())+':'+key
        if cachekey in self.anchor_cache:
            hit=self.anchor_cache[cachekey];return tuple(hit['axis']),hit['alignment']
        try:import cv2
        except ImportError:
            sys.path.insert(0,'/tmp/roster-cv');import cv2
        target=np.array(im);best=None
        for source,tile,mask,pivot in self.templates:
            if self.char=='MitsukiTBV' and source[0]!=(1 if key.startswith('SageGaara_') else 0):continue
            if self.char=='Eida' and (source[0]==1000)!=key.startswith('Parents_'):continue
            h,w=tile.shape[:2]
            if h>im.height or w>im.width:continue
            xleft=max(0,axis[0]-pivot[0]-32);xright=min(im.width,axis[0]-pivot[0]+w+33)
            if xright-xleft<w:continue
            result=cv2.matchTemplate(target[:,xleft:xright],tile,cv2.TM_SQDIFF,mask=mask)
            result/=float((mask>0).sum()*4*255**2)
            # Horizontal plist offsets are correct. Reject distant identical
            # fragments inside projectiles or summons.
            columns=np.arange(result.shape[1])+pivot[0]+xleft
            result[:,abs(columns-axis[0])>32]=np.inf
            idx=np.unravel_index(np.argmin(result),result.shape);score=float(result[idx])
            if best is None or score<best[0]:best=(score,(int(idx[1])+xleft+pivot[0],int(idx[0])+pivot[1]),source)
            if score<1e-6:break
        if best and best[0]<.16:
            result=(best[1],dict(method='masked original body match',error=best[0],original_sprite=best[2]))
            self.anchor_cache[cachekey]=dict(axis=result[0],alignment=result[1]);self.anchor_cache_path.write_text(json.dumps(self.anchor_cache,indent=2)+'\n')
            return result
        # Body-only frames can be anchored directly. Large unresolved effect
        # composites are reported for review instead of silently moved.
        bb=im.getbbox()
        result=((axis[0],bb[3]-1),dict(method='visible lower bound',error=best[0] if best else None))
        self.anchor_cache[cachekey]=dict(axis=result[0],alignment=result[1]);self.anchor_cache_path.write_text(json.dumps(self.anchor_cache,indent=2)+'\n')
        return result
    def seq(self,prefix,start=None,end=None):
        found=[]
        for key in self.frames:
            if not key.startswith(prefix+'_'):continue
            tail=key[len(prefix)+1:]
            if not tail.isdigit():continue
            n=int(tail)
            if (start is None or n>=start) and (end is None or n<=end):found.append((n,key))
        found.sort();assert found,(self.char,prefix,start,end)
        return [self.use(key) for _,key in found]
    def use(self,key,center=False):
        cache=(key,center)
        if cache in self.used:return self.used[cache]
        im,axis,path,meta,pi=self.frames[key]
        alignment=None
        if center:axis=(im.width//2,im.height//2)
        elif 'Mktn' in key or 'Mokuton' in key:
            # SFF's indexed palette drops alpha below 128. Anchor the solid
            # ground rim, not the faint shadow/padding in the RGBA canvas.
            opaque=Image.fromarray((np.array(im.getchannel('A'))>=128).astype('uint8')*255).getbbox()
            axis=(im.width//2,opaque[3]-1)
        elif 'Stn' not in key and 'Mokuton' not in key:axis,alignment=self.align_body(im,key,axis)
        im,eyes=recolor(im,axis) if self.char in ['Mamushi','RyuShinju','JuraShinju','HidariShinju','MatsuriShinju'] else (im,0)
        g=26000+pi;n=sum(1 for gg,nn in self.archive.entries if gg==g)
        dest=ROOT/self.char/'assets/senki'/f'{g}_{n}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
        self.archive.put((g,n),im,axis);self.used[cache]=(g,n)
        self.manifest.append(dict(group=g,number=n,key=key,file=str(dest.relative_to(ROOT/self.char)),axis=axis,alignment=alignment,plist=str(path.relative_to(ROOT)),rectangle=meta['frame'],source_offset=meta['offset'],source_rotated=meta.get('rotated',False),rgba_sha256=sha(im.tobytes()),eye_pixels_recolored=eyes,body_redrawn=False))
        return g,n

def parse_action(block):
    defaults={1:[],2:[]};pending={};frames=[];start=0
    for line in block.splitlines():
        m=re.match(r'\s*Clsn([12])(Default)?:\s*(\d+)',line,re.I)
        if m:
            typ=int(m[1]);pending[typ]=[]
            if m[2]:defaults[typ]=pending[typ]
        m=re.match(r'\s*Clsn([12])\[\d+\]\s*=\s*(.*)',line,re.I)
        if m:pending[int(m[1])].append(tuple(map(int,nums(m[2]))))
        m=re.match(r'\s*(\d+),\s*(\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)',line)
        if m:
            g,n,x,y,t=map(int,m.groups());frames.append(dict(start=start,duration=t,key=(g,n),xy=(x,y),boxes={typ:list(pending.get(typ,defaults[typ])) for typ in [1,2]}));start+=max(1,t);pending={}
    return frames,start

def replace_action(block,seq,*,effect=False,center=False):
    old,total=parse_action(block);assert old
    # Split on BOTH source drawing and original collision boundaries. This
    # preserves every contact window while displaying all supplied frames.
    total=max(total,len(seq));times=[round(i*total/len(seq)) for i in range(len(seq)+1)]
    points=sorted(set(times+[f['start'] for f in old if f['start']<total]+[total]))
    n=int(re.search(r'\[Begin Action (\d+)\]',block,re.I)[1]);out=f'\n[Begin Action {n}]\n; Complete original sequence; original contact windows retained.\n'
    if 'loopstart' in block.lower():out+='Loopstart\n'
    for a,b in zip(points,points[1:]):
        frame=next((f for f in reversed(old) if f['start']<=a),old[0]);idx=max(i for i,t in enumerate(times[:-1]) if t<=a);g,num=seq[idx]
        for typ in [1,2]:
            boxes=frame['boxes'][typ]
            if boxes:
                out+=f'Clsn{typ}: {len(boxes)}\n'
                for j,box in enumerate(boxes):out+=f' Clsn{typ}[{j}]='+','.join(map(str,box))+'\n'
        out+=f'{g},{num},0,0,{b-a}\n'
    return out,old

def retime_states(text,changed):
    blocks=re.split(r'(?=\[Statedef\s+-?\d+\])',text,flags=re.I);out=[]
    for block in blocks:
        m=re.search(r'(?im)^anim\s*=\s*(\d+)\s*$',block)
        if m and int(m[1]) in changed:
            frames=changed[int(m[1])]
            def tick(n):return frames[min(int(n)-1,len(frames)-1)]['start']
            block=re.sub(r'(?i)AnimElem\s*=\s*(\d+)(?!\s*,)',lambda m:'Time = '+str(tick(m[1])),block)
            block=re.sub(r'(?i)AnimElemNo\(0\)\s*>=\s*(\d+)',lambda m:'Time >= '+str(tick(m[1])),block)
        out.append(block)
    return ''.join(out)

def selections(ch,a):
    s=a.seq;maps={}
    def add(n,prefix,lo=None,hi=None,forms=False):
        maps[n]=s(prefix,lo,hi)
        if forms:maps[n+10000]=maps[n]
    if ch=='MatsuriShinju':
        for n,p,lo,hi in [(1000,'Hashirama_Skill01',None,None),(1010,'Hashirama_Nattack',14,19),(1020,'Hashirama_Skill02',1,11),(1030,'Hashirama_Skill03',None,None),(1040,'Hashirama_Nattack',14,19),(1050,'Hashirama_Skill05_Pre',None,None),(1400,'Hashirama_Nattack',8,13),(1410,'Hashirama_Nattack',14,19),(1420,'Hashirama_Nattack',1,7),(1430,'Hashirama_Skill04',1,5)]:add(n,p,lo,hi)
        add(8612,'Hashirama_Mktn02');add(8620,'Hashirama_Mktn02')
        # These were unrelated loose cape pieces, not a lance or a binding.
        add(8610,'Hashirama_Mktn01');add(8611,'Hashirama_Mktn01')
        water=s('Hashirama_Stn01');splash=s('Hashirama_Stn02',5,8)
        # Projectile origins use their centres rather than the caster's feet.
        maps[8630]=[a.use(next(m['key'] for m in a.manifest if (m['group'],m['number'])==k),True) for k in water]
        maps[8631]=[a.use(next(m['key'] for m in a.manifest if (m['group'],m['number'])==k),True) for k in splash]
    elif ch=='Mamushi':
        for n,p,lo,hi in [(1000,'Orochimaru_NAttack',1,7),(1010,'Orochimaru_Skill02',1,5),(1020,'Orochimaru_NAttack',8,13),(1030,'Orochimaru_Skill02',6,13),(1040,'Orochimaru_Skill01',1,4),(1050,'Orochimaru_Skill03',1,6),(1410,'Orochimaru_NAttack',1,7),(1420,'Orochimaru_Skill02',6,13),(1210,'Orochimaru_Skill05',1,26),(1430,'Orochimaru_Skill05_Jump',1,4),(1440,'Orochimaru_Skill05_Teleport',1,6)]:add(n,p,lo,hi)
    elif ch=='RyuShinju':
        for n,p,lo,hi in [(1000,'Shino_Skill01_Blt',1,4),(1010,'Shino_Skill04',16,25),(1020,'Shino_Skill02',1,13),(1030,'Shino_Skill03',13,20),(1040,'Shino_NAttack',1,8),(1050,'Shino_Skill03',1,12),(1200,'Shino_Skill01_Blt',1,4),(1420,'Shino_Skill01',1,6),(1430,'Shino_Skill04',1,10),(1440,'Shino_NAttack',15,31)]:add(n,p,lo,hi,True)
    elif ch=='MitsukiTBV':
        for n,p in [(1010,'Gaara_Toppa'),(1030,'Gaara_Slash1'),(1040,'Gaara_Kick'),(1050,'Gaara_Slash2')]:add(n,p)
        for n,p in [(10200,'SageGaara_Atk'),(10201,'SageGaara_Atk'),(10202,'SageGaara_Atk'),(11000,'SageGaara_Ulti')]:
            add(n,p)
        # Keep the previously approved snake-shaped green Orochi Ikazuchi
        # (11020 / source electrical helper) and both separate movesets.
    elif ch=='JuraShinju':
        for n,p,lo,hi in [(1010,'Orochimaru_Skill02',1,3),(1040,'Orochimaru_NAttack',10,14),(1050,'Orochimaru_Skill02',1,3),(1400,'Orochimaru_NAttack',10,14),(1410,'Orochimaru_NAttack',10,14)]:add(n,p,lo,hi)
        recovery=s('JuraExShot',5,5)
        maps[1020]=s('JuraExChg',1,4)+recovery*8
        maps[1030]=s('JuraExChg',1,8)+recovery*8
        maps[1200]=s('JuraExChg',1,3)+recovery*8
        add(8600,'JuuraMokuton')
    elif ch=='Eida':
        # Eida's root casts are separate from her Daemon attack helpers.
        add(1100,'Chiyo_S1');add(1300,'Chiyo_S1')
        for n,lo,hi in [(1000,1,4),(1010,1,7),(1040,1,5)]:add(n,'Parents_Skill01',lo,hi)
        add(1350,'Chiyo_S1')
    elif ch=='HidariShinju':
        # Preserve Sasuke's accepted Chidori, Gokakyu and yellow Susanoo.
        for n,p,lo,hi in [(1010,'Zabuza_Skill01',9,15),(1020,'Zabuza_Skill02',1,5),(1030,'Zabuza_Skill03',1,9),(1040,'Zabuza_Skill01',9,15),(1050,'Zabuza_Skill01',1,8),(1430,'Zabuza_Skill04',1,19)]:add(n,p,lo,hi)
    return maps

def repairs(ch,texts):
    main=ch+'.cns';air=ch+'.air';cmd=ch+'.cmd'
    # The generic later characters restarted jab 1 before its 27/30-tick
    # hitstun ended. Confirmed chains finish; neutral starts wait for recovery.
    if ch in ['JuraShinju','MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju','Shibai']:
        blocks=re.split(r'(?=\[Statedef\s+-?\d+\])',texts[main],flags=re.I)
        for i,block in enumerate(blocks):
            m=re.match(r'\[Statedef (\d+)\]',block,re.I)
            if m and int(m[1])%10000 in [200,201,210,211,220,221]:
                block=re.sub(r'(?im)^ground\.hittime\s*=.*$','ground.hittime=12',block)
                blocks[i]=block
        texts[main]=''.join(blocks)
        blocks=re.split(r'(?=\[State\s+-1,)',texts[cmd],flags=re.I)
        for i,block in enumerate(blocks):
            if re.search(r'(?im)^triggerall\s*=\s*AILevel\s*>\s*0',block) and re.search(r'(?im)^triggerall\s*=\s*ctrl\s*$',block) and 'CPU approach' not in block:
                block=block.replace('\nvalue=', '\ntriggerall=P2MoveType!=H\nvalue=',1)
                if '\ntriggerall=P2MoveType!=H\n' not in block:
                    block=re.sub(r'(?im)^value\s*=', 'triggerall=P2MoveType!=H\nvalue=',block,count=1)
                blocks[i]=block
        texts[cmd]=''.join(blocks)
        # Confirm hits rather than automatically repeating the opening jab.
        if ch!='Shibai':
            offset='+10000*Var(42)' if ch in ['MitsukiTBV','RyuShinju','HidariShinju','MatsuriShinju'] else ''
            follow=f'\n[State -1, Finite CPU confirmed three-hit chain]\ntype=ChangeState\ntriggerall=AILevel>0\ntriggerall=RoundState=2\ntriggerall=MoveHit\ntriggerall=Time>=6\ntrigger1=StateNo%10000=200 || StateNo%10000=201\nvalue=StateNo+1\nignorehitpause=1\n'
            texts[cmd]=texts[cmd].replace('[Statedef -1]','[Statedef -1]\n'+follow,1)
    # Mamushi's supplied get-hit bank had NO reception boxes at all: the
    # first hit removed him from all subsequent attack collisions.
    if ch=='Mamushi':
        blocks=re.split(r'(?=\[Begin Action)',texts[air],flags=re.I)
        for i,b in enumerate(blocks):
            m=re.match(r'(\[Begin Action (\d+)\])',b,re.I)
            if m and 5000<=int(m[2])<=5210 and 'Clsn2' not in b:
                n=int(m[2]);box='-28,-26,28,0' if n in [5080,5090,5100,5110,5150,5160,5170] else '-17,-68,17,0'
                blocks[i]=b.replace(m[1],m[1]+'\nClsn2Default: 1\n Clsn2[0]='+box,1)
        texts[air]=''.join(blocks)
    if ch=='PochitaTrueForm':
        common=texts['common1.cns']
        for n,sign in [(100,1),(105,-1)]:
            block=f'\n[Statedef {n}]\ntype=S\nmovetype=I\nphysics=N\nanim={n}\nvelset={sign*7.6},0\nctrl=0\n[State {n}, Fixed ground dash direction]\ntype=AssertSpecial\ntrigger1=1\nflag=NoAutoTurn\n[State {n}, Ground dash]\ntype=PosSet\ntrigger1=1\ny=0\n[State {n}, End short dash]\ntype=ChangeState\ntrigger1=Time>=14\nvalue=0\nctrl=1\n'
            if n==100:block=block.replace('value=0\nctrl=1','value=106\nctrl=1')
            common=re.sub(r'(?ims)^\[Statedef '+str(n)+r'\][\s\S]*?(?=^\[Statedef|\Z)',lambda m:block,common,count=1)
        texts['common1.cns']=common
        dashback='''[Begin Action 105]
Clsn2Default: 1
 Clsn2[0]=-17,-72,17,0
Loopstart
3501,3,0,0,3
3501,2,0,0,3
3501,1,0,0,3
3501,0,0,0,3
'''
        texts[air]=re.sub(r'(?ims)^\[Begin Action 105\].*?(?=^\[Begin Action|\Z)',lambda m:dashback+'\n',texts[air],count=1)
    if ch=='Eida':
        b='''[Statedef 105]
type=S
movetype=I
physics=N
anim=21
ctrl=0
velset=-6.5,0
[State 105, Retire legacy effect helper]
type=DestroySelf
trigger1=IsHelper
[State 105, Grounded backward dash]
type=PosSet
trigger1=!IsHelper
y=0
[State 105, Fixed facing]
type=AssertSpecial
trigger1=!IsHelper
flag=NoAutoTurn
[State 105, Return control]
type=ChangeState
trigger1=Time>=14
value=0
ctrl=1
'''
        texts[main]=re.sub(r'(?ims)^\[Statedef 105\].*?(?=^\[Statedef|\Z)',lambda m:b+'\n',texts[main],count=1)
        texts[main]=texts[main].replace('trigger1 = command != "holdfwd"\ntrigger2 = Time >= 40','trigger1 = Time >= 14',1)
        texts[cmd]+='''
[State -1, Backward ground dash]
type=ChangeState
value=105
triggerall=command="BB"
triggerall=StateType=S
triggerall=command!="holddown"
trigger1=ctrl
'''
    if ch=='HidariShinju':
        # The visible guardian is larger than the hidden body's old box.
        blocks=re.split(r'(?=\[Begin Action)',texts[air],flags=re.I)
        for i,b in enumerate(blocks):
            m=re.match(r'\[Begin Action (\d+)\]',b,re.I)
            if m and 10000<=int(m[1])<16000 and 'Clsn2' in b:
                blocks[i]=re.sub(r'(?im)(Clsn2\[0\]\s*=)[^\r\n]*',r'\g<1>-30,-140,30,0',b)
        texts[air]=''.join(blocks)
    if ch=='MatsuriShinju':
        # Do not rotate whole capes around the victim. The new original root
        # binding grows from the floor, with the same three contact times.
        b=texts[main]
        b=re.sub(r'(?ims)\[State 9420, Visible cloth coils turn around the victim\][\s\S]*?(?=\[State|\[Statedef)', '',b)
        # Root manifestations emerge at ground level, not at neck height.
        b=re.sub(r'(?ims)(\[State 1050, Physical Shinju technique\].*?^pos=)([^\n]+)',lambda m:m[1]+m[2].rsplit(',',1)[0]+',0',b)
        b=re.sub(r'(?ims)(\[State 11050, Physical Shinju technique\].*?^pos=)([^\n]+)',lambda m:m[1]+m[2].rsplit(',',1)[0]+',0',b)
        b=b.replace('[State 9410, Stable effect scale during impacts]','[State 9410, Roots stay on the floor]\ntype=PosSet\ntrigger1=1\ny=0\n\n[State 9410, Stable effect scale during impacts]')
        # Impact flashes belong at the hand/foot. Ground root bindings are
        # rendered only by their actual grounded helper, not as floating props.
        controls=re.split(r'(?=\[State\s+)',b,flags=re.I)
        for i,block in enumerate(controls):
            if re.search(r'(?im)^type\s*=\s*Explod\s*$',block):
                controls[i]=re.sub(r'(?im)^anim\s*=\s*8611\s*$','anim=8700',block)
        b=''.join(controls)
        for n,scale in [(9430,'.55'),(9450,'.7')]:
            b=re.sub(r'(?ims)(\[State '+str(n)+r', Stable effect scale during impacts\].*?^scale=)[^\r\n]+',lambda m:m[1]+scale+','+scale,b)
        texts[main]=b
    return texts

def main():
    report={}
    for ch in CHARS:
        folder=ROOT/ch;texts={p.name:original(p).decode('utf-8') for p in folder.iterdir() if p.suffix in ['.cns','.cmd','.air']}
        archive=Archive(original(folder/(ch+'.sff')));eyes=0
        if ch in ['Mamushi','RyuShinju','JuraShinju','HidariShinju','MatsuriShinju']:
            for key in list(archive.entries):
                if key[0] not in [0,1,2,9000]:continue
                im,axis=archive.image(key);fixed,count=recolor(im)
                if count:
                    archive.put(key,fixed,axis);eyes+=count
                    p=folder/'assets/eye_revision'/f'{key[0]}_{key[1]}.png';p.parent.mkdir(exist_ok=True);fixed.save(p)
        changed={};atlas=None
        stem={'Eida':'Eida','Mamushi':'Mamushi','JuraShinju':'Jura','MitsukiTBV':'Mitsuki','RyuShinju':'Ryu','HidariShinju':'Hidari','MatsuriShinju':'Matsuri'}.get(ch)
        if stem:
            atlas=Atlas(stem,ch,archive);maps=selections(ch,atlas)
            blocks=re.split(r'(?=\[Begin Action)',texts[ch+'.air'],flags=re.I)
            for i,b in enumerate(blocks):
                m=re.match(r'\[Begin Action (\d+)\]',b,re.I)
                if m and int(m[1]) in maps:blocks[i],changed[int(m[1])]=replace_action(b,maps[int(m[1])])
            texts[ch+'.air']=''.join(blocks)
            for name in list(texts):
                if name.endswith('.cns'):texts[name]=retime_states(texts[name],changed)
        texts=repairs(ch,texts)
        for name,content in texts.items():(folder/name).write_text(content)
        archive.save(folder/(ch+'.sff'))
        if ch=='MatsuriShinju':
            data=original(folder/(ch+'.snd'));count,off=struct.unpack_from('<2I',data,16);sounds=[]
            for _ in range(count):
                nxt,size,g,n=struct.unpack_from('<4I',data,off);payload=data[off+16:off+16+size]
                if g==2 and n in [0,1]:payload=(folder/'assets/sound'/f'2_{n}.wav').read_bytes()
                sounds.append((g,n,payload));off=nxt
            header=bytearray(data[:512]);struct.pack_into('<2I',header,16,len(sounds),512);chunks=[];off=512
            for i,(g,n,payload) in enumerate(sounds):
                nxt=off+16+len(payload) if i<len(sounds)-1 else 0;chunks.append(struct.pack('<4I',nxt,len(payload),g,n)+payload);off=nxt
            (folder/(ch+'.snd')).write_bytes(bytes(header)+b''.join(chunks))
        if atlas:
            (folder/'assets/senki/manifest.json').write_text(json.dumps(atlas.manifest,indent=2)+'\n')
        report[ch]=dict(base_commit=BASE,source_frames=len(atlas.manifest) if atlas else 0,updated_actions=sorted(changed),old_iris_pixels_recolored=eyes,files={name:sha((folder/name).read_bytes()) for name in texts})
        print(ch,report[ch]['source_frames'],'new source frames;',len(changed),'complete sequences;',eyes,'old iris pixels',flush=True)
    (ROOT/'design/roster_repair/build.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
