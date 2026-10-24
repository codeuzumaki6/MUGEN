#!/usr/bin/env python3
"""Install phase-separated animations and original pack sounds over the repaired roster.

Builds from a fixed, reviewed runtime. Atlas rectangles are data, never scripts.
Caster-containing Senki composites are cropped before they become free projectiles.
No HitDef damage, power cost, input command, CPU or receiving box is reset.
"""
from pathlib import Path
import hashlib,json,re,struct,subprocess,sys,zipfile
import numpy as np
from PIL import Image,ImageFilter
from build_roster_revision import Archive,Atlas,ROOT,recolor,parse_action,replace_action,retime_states

BASE='c6d04d94934c2e83efa869744587f13eda270b59'
CHARS={'Mamushi':'Mamushi','JuraShinju':'Jura','MitsukiTBV':'Mitsuki','RyuShinju':'Ryu','HidariShinju':'Hidari','MatsuriShinju':'Matsuri','Eida':'Eida'}
OUT=ROOT/'design/full_sprite_revision'
def original(path):return subprocess.check_output(['git','show',BASE+':'+str(path.relative_to(ROOT))],cwd=ROOT)
def sha(data):return hashlib.sha256(data).hexdigest()
def state_pattern(n):return r'(?ims)^\[Statedef\s+'+str(n)+r'\].*?(?=^\[Statedef|\Z)'
def action_pattern(n):return r'(?ims)^\[Begin Action\s+'+str(n)+r'\].*?(?=^\[Begin Action|\Z)'
def transform_state(text,n,fn):
    text,count=re.subn(state_pattern(n),lambda m:fn(m[0]),text,count=1)
    assert count,(n,'state missing');return text
def remove_controller(block,label):
    return re.sub(r'(?ims)^\[State\s+[^,]+,\s*'+re.escape(label)+r'\].*?(?=^\[State|\Z)','',block)
def controller(n,label,kind,values):return '\n[State '+str(n)+', '+label+']\ntype='+kind+'\n'+values.strip()+'\n'
def explod(n,anim,t,pos='0,0',scale='1,1',duration=-2,priority=4,bind=0):
    return controller(n,'Original pack animation '+str(anim),'Explod',f'trigger1=Time={t}\nanim={anim}\nID={anim}\npostype=P1\npos={pos}\nscale={scale}\nremovetime={duration}\nbindtime={bind}\nownpal=1\nsprpriority={priority}\nremoveongethit=1\npausemovetime=180\nsupermovetime=180')

class Revision:
    def __init__(self,ch,stem):
        self.ch=ch;self.stem=stem;self.folder=ROOT/ch
        self.archive=Archive(original(self.folder/(ch+'.sff')))
        self.atlas=Atlas(stem,ch,self.archive)
        self.texts={p.name:original(p).decode('utf-8') for p in self.folder.iterdir() if p.suffix in ['.cns','.air','.cmd']}
        self.records=[];self.actions={};self.changes={};self.sounds=[];self.sound_names={}
        self.old_records=json.loads(original(self.folder/'assets/senki/manifest.json'))
        self.bank=27000;self.keys={}
    def names(self,prefix,lo=None,hi=None):
        ns=[]
        for k in self.atlas.frames:
            if not k.startswith(prefix+'_'):continue
            tail=k[len(prefix)+1:]
            if tail.isdigit() and (lo is None or int(tail)>=lo) and (hi is None or int(tail)<=hi):ns.append((int(tail),k))
        assert ns,(self.ch,prefix,lo,hi)
        return [k for _,k in sorted(ns)]
    def use(self,key,role='body',crop=None,axis=None,size=None,erase=None,body_mask=None):
        cache=(key,role,str(crop),str(axis),str(size),str(erase),str(body_mask))
        if cache in self.keys:return self.keys[cache]
        im,default,path,meta,pi=self.atlas.frames[key];im=im.copy()
        alignment=None
        if role=='body':
            default,alignment=self.atlas.align_body(im,key,default)
        if axis is None:
            if role=='ground':
                bb=Image.fromarray((np.array(im.getchannel('A'))>=128).astype('uint8')*255).getbbox()
                default=(im.width//2,bb[3]-1)
            elif role=='center':default=(im.width//2,im.height//2)
            axis=default
        if erase:
            a=np.array(im);x,y,x2,y2=erase;a[y:y2,x:x2,3]=0;im=Image.fromarray(a)
        if body_mask:
            reference,ref_axis=self.archive.image(tuple(body_mask))
            mask=Image.new('L',im.size);mask.paste(reference.getchannel('A'),(axis[0]-ref_axis[0],axis[1]-ref_axis[1]))
            mask=mask.filter(ImageFilter.MaxFilter(3));a=np.array(im);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));im=Image.fromarray(a)
        if crop:
            im=im.crop(crop);axis=(axis[0]-crop[0],axis[1]-crop[1])
        if size:
            sx,sy=size;axis=(round(axis[0]*sx),round(axis[1]*sy));im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.NEAREST)
        if self.ch in ['Mamushi','JuraShinju','RyuShinju','HidariShinju','MatsuriShinju']:
            im,eyes=recolor(im)
        else:eyes=0
        dest=(self.bank,len(self.records));self.archive.put(dest,im,axis)
        name=f'{dest[0]}_{dest[1]}.png';p=self.folder/'assets/full_pack'/name;p.parent.mkdir(exist_ok=True);im.save(p)
        self.records.append(dict(group=dest[0],number=dest[1],key=key,role=role,file='assets/full_pack/'+name,axis=axis,source=str(path.relative_to(ROOT)),source_rectangle=meta['frame'],source_rotation=meta.get('rotated',False),crop=crop,erase=erase,size=size,body_mask_reference=body_mask,alignment=alignment,eye_pixels_recolored=eyes,rgba_sha256=sha(im.tobytes()),body_redrawn=False))
        self.keys[cache]=dest;return dest
    def seq(self,prefix,lo=None,hi=None,**kw):return [self.use(k,**kw) for k in self.names(prefix,lo,hi)]
    def cast_body(self,prefix,lo=None,hi=None):
        frames=[]
        for k in self.names(prefix,lo,hi):
            im,default,*_=self.atlas.frames[k];axis,alignment=self.atlas.align_body(im,k,default)
            reference=alignment.get('original_sprite')
            if reference:
                w,h,rx,ry,*_=self.archive.entries[tuple(reference)]
                box=(max(0,axis[0]-rx-2),max(0,axis[1]-ry-2),min(im.width,axis[0]+w-rx+2),min(im.height,axis[1]+h-ry+2))
            else:box=(max(0,axis[0]-35),max(0,axis[1]-100),min(im.width,axis[0]+55),min(im.height,axis[1]+2))
            frames.append(self.use(k,role='body',axis=axis,crop=box,body_mask=reference))
        return frames
    def without_caster(self,key,candidates,limit=(220,310),axis=None):
        """Remove a baked fighter by its actual source alpha, preserving FX contours.

        A rectangular crop through the explosion gives it a hard vertical edge.
        Match only the supplied fighter silhouette and clear that exact mask.
        """
        try:import cv2
        except ImportError:
            sys.path.insert(0,'/tmp/roster-cv');import cv2
        im,default,path,meta,pi=self.atlas.frames[key];a=np.array(im);best=None
        for old in candidates:
            src,_=self.archive.image(old);tile=np.array(src);mask=(tile[:,:,3]>=128).astype('uint8')*255
            target=a[:min(limit[1],a.shape[0]),:min(limit[0],a.shape[1])]
            if target.shape[0]<tile.shape[0] or target.shape[1]<tile.shape[1]:continue
            # Cyan hair is unique to Mamushi; energy/rocks must not pull the
            # mask onto a similarly coloured dark patch inside the explosion.
            hair=(tile[:,:,3]>=128)&(tile[:,:,1]>60)&(tile[:,:,2]>80)&(tile[:,:,1]>tile[:,:,0].astype(float)*1.3)&(tile[:,:,2]>tile[:,:,0].astype(float)*1.3)
            matchmask=hair.astype('uint8')*255
            v=cv2.matchTemplate(target,tile,cv2.TM_SQDIFF,mask=matchmask);v/=max(1,hair.sum()*4*255**2)
            loc=np.unravel_index(np.argmin(v),v.shape);score=float(v[loc])
            if best is None or score<best[0]:best=(score,loc,mask,old)
        assert best and best[0]<.30,(self.ch,key,best[0] if best else None)
        score,(y,x),mask,old=best;mask=cv2.dilate(mask,np.ones((3,3),np.uint8))
        alpha=a[y:y+mask.shape[0],x:x+mask.shape[1],3];alpha[mask>0]=0
        fixed=Image.fromarray(a);dest=(self.bank,len(self.records));self.archive.put(dest,fixed,axis or default)
        p=self.folder/'assets/full_pack'/f'{dest[0]}_{dest[1]}.png';p.parent.mkdir(exist_ok=True);fixed.save(p)
        self.records.append(dict(group=dest[0],number=dest[1],key=key,role='impact',file=str(p.relative_to(self.folder)),axis=axis or default,source=str(path.relative_to(ROOT)),source_rectangle=meta['frame'],caster_mask=dict(reference=old,location=[int(x),int(y)],score=score),rgba_sha256=sha(fixed.tobytes()),body_redrawn=False))
        return dest
    def action(self,n,seq,step=3,loop=False,boxes=None,times=None):
        text=f'\n[Begin Action {n}]\n; Original supplied atlas: independent visual phase.\n'
        if boxes:
            for typ,bs in boxes.items():
                text+=f'Clsn{typ}Default: {len(bs)}\n'
                for i,b in enumerate(bs):text+=f' Clsn{typ}[{i}]='+','.join(map(str,b))+'\n'
        if loop:text+='Loopstart\n'
        for i,(g,k) in enumerate(seq):text+=f'{g},{k},0,0,{times[i] if times else step}\n'
        self.set_action(n,text)
    def set_action(self,n,text):
        name=self.ch+'.air';old=re.search(action_pattern(n),self.texts[name])
        if old:self.texts[name]=re.sub(action_pattern(n),lambda m:text+'\n',self.texts[name],count=1)
        else:self.texts[name]+='\n'+text
        self.actions[n]=text
    def replace(self,n,seq):
        old=re.search(action_pattern(n),self.texts[self.ch+'.air']);assert old,(self.ch,n)
        text,frames=replace_action(old[0],seq);self.set_action(n,text);self.changes[n]=frames
    def edit(self,n,fn,file=None):
        file=file or self.ch+'.cns';self.texts[file]=transform_state(self.texts[file],n,fn)
    def add(self,n,extra,file=None):self.edit(n,lambda b:b+'\n'+extra,file)
    def audio(self,suffix):
        if suffix in self.sound_names:return self.sound_names[suffix]
        info=json.loads((OUT/'audio_inventory.json').read_text())[self.stem]
        num=len(self.sounds);dest=self.folder/'assets/full_pack/sound';dest.mkdir(parents=True,exist_ok=True)
        src=dest/(str(num)+'_'+Path(suffix).name)
        if Path(info['archive']).exists():
            with zipfile.ZipFile(info['archive']) as z:
                matches=[n for n in z.namelist() if n.endswith('/'+suffix)]
                assert len(matches)==1,(self.stem,suffix,matches)
                member=matches[0];data=z.read(member)
        else:
            # A fresh checkout includes the selected original sound bytes;
            # it does not need the old attachment directory on this machine.
            previous=json.loads((self.folder/'assets/full_pack/manifest.json').read_text())['sounds']
            rec=next(r for r in previous if r['member'].endswith('/'+suffix))
            data=src.read_bytes();assert sha(data)==rec['source_sha256'];member=rec['member']
        src.write_bytes(data)
        wav=dest/f'5_{num}.wav'
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(src),'-ac','1','-ar','22050','-c:a','pcm_s16le',str(wav)],check=True)
        self.sounds.append(dict(group=5,number=num,source_zip=info['archive'],member=member,source_sha256=sha(data),wav=str(wav.relative_to(self.folder)),wav_sha256=sha(wav.read_bytes())))
        self.sound_names[suffix]=num;return num
    def sound(self,n,suffix,t=0,channel=7,volume=70,file=None):
        num=self.audio(suffix)
        self.add(n,controller(n,'Supplied pack sound '+Path(suffix).name,'PlaySnd',f'trigger1=Time={t}\nvalue=S5,{num}\nchannel={channel}\nvolumescale={volume}\nignorehitpause=1\npersistent=0'),file)
    def finish(self):
        for name,t in list(self.texts.items()):
            if name.endswith('.cns'):self.texts[name]=retime_states(t,self.changes)
        for name,t in self.texts.items():(self.folder/name).write_text(t)
        self.archive.save(self.folder/(self.ch+'.sff'))
        data=original(self.folder/(self.ch+'.snd'));count,off=struct.unpack_from('<2I',data,16);sounds=[]
        for _ in range(count):
            nxt,size,g,n=struct.unpack_from('<4I',data,off);sounds.append((g,n,data[off+16:off+16+size]));off=nxt
        assert not any(g==5 for g,n,p in sounds)
        sounds += [(5,r['number'],(self.folder/r['wav']).read_bytes()) for r in self.sounds]
        header=bytearray(data[:512]);struct.pack_into('<2I',header,16,len(sounds),512);chunks=[];off=512
        for i,(g,n,payload) in enumerate(sounds):
            nxt=off+16+len(payload) if i<len(sounds)-1 else 0;chunks.append(struct.pack('<4I',nxt,len(payload),g,n)+payload);off=nxt
        (self.folder/(self.ch+'.snd')).write_bytes(bytes(header)+b''.join(chunks))
        (self.folder/'assets/full_pack/manifest.json').write_text(json.dumps(dict(base_commit=BASE,frames=self.records,actions=sorted(self.actions),sounds=self.sounds),indent=2)+'\n')
        # Existing native form fixtures accept exact source keys, not entire ranges.
        (self.folder/'assets/senki/manifest.json').write_text(json.dumps(self.old_records+self.records,indent=2)+'\n')
        runtime_names=sorted(self.texts)+[self.ch+'.sff',self.ch+'.snd']
        return dict(character=self.ch,new_frames=len(self.records),source_families=sorted(set(r['key'].rsplit('_',1)[0] for r in self.records)),actions=sorted(self.actions),sounds=len(self.sounds),runtime_sha256=sha(b''.join((self.folder/n).read_bytes() for n in runtime_names)),runtime_files=runtime_names)

def mamushi(r):
    # Keep the original clean fighter at the jaw; the full Senki images also
    # contain that fighter and MUST NOT be played on the moving sphere.
    clean=[]
    for n,axis in [(81,(15,95)),(83,(8,95))]:
        im,_=r.archive.image((0,n));key=(27001,len(clean));r.archive.put(key,im,axis);clean.append(key)
    baseline=subprocess.check_output(['git','show','38dd5362fe76610a7c7d5a1c033868deb37519ec:Mamushi/Mamushi.air'],cwd=ROOT).decode()
    old=re.search(action_pattern(1210),baseline)[0]
    block=old.replace('0,81,',f'{clean[0][0]},{clean[0][1]},').replace('0,82,',f'{clean[1][0]},{clean[1][1]},')
    r.set_action(1210,block)
    charge=r.seq('Orochimaru_Skill05',1,9,role='center',crop=(145,0,300,217),axis=(192,114))
    r.action(27100,charge,step=2)
    flight=r.seq('Orochimaru_Skill05',10,11,role='center',crop=(145,0,400,246),axis=(285,139))
    r.replace(9400,flight)
    impact=[]
    for k in r.names('Orochimaru_Skill05',12,26):
        if int(k.rsplit('_',1)[1])<=24:
            impact.append(r.without_caster(k,[(0,81),(0,83)],axis=(330,350)))
        else:
            im=r.atlas.frames[k][0]
            impact.append(r.use(k,role='center',erase=(0,0,85,180),axis=(330,350)))
    r.action(27101,impact,step=2)
    r.edit(1210,lambda b:remove_controller(remove_controller(b,'Timed presentation accent'),'Mouth charge sound')+explod(1210,27100,10,pos='125,-32',scale='.48,.48',duration=18,bind=-1))
    r.edit(9400,lambda b:remove_controller(remove_controller(remove_controller(b,'Purple-black core'),'Living violet rim'),'Visible dark core')+controller(9400,'Preserve original sphere dimensions','AngleDraw','trigger1=1\nscale=.42,.42'))
    r.edit(9401,lambda b:re.sub(r'(?im)^anim\s*=\s*8740','anim=27101',remove_controller(b,'Timed presentation accent')).replace('Time>=18','Time>=30')+controller(9401,'Original impact dimensions','AngleDraw','trigger1=1\nscale=.28,.28')+controller(9401,'Ground the source impact','PosSet','trigger1=Time=0\ny=0'))
    r.replace(9200,r.seq('Orochimaru_Blt',1,4,role='center'))
    r.replace(9100,r.seq('Orochimaru_Akar',role='ground'))
    r.replace(3002,r.seq('Orochimaru_Skill04',1,9))
    r.replace(3003,r.seq('Orochimaru_Skill04',10,12))
    r.replace(3004,r.seq('Orochimaru_Skill04',13,23))
    for n,f,t in [(1210,'Effect/charge2.ogg',10),(1210,'Effect/BijuDama.mp3',28),(9401,'Effect/Duar.ogg',0),(1010,'Effect/Kayu.ogg',8),(1030,'Effect/Bor0.ogg',8),(1040,'Effect/Cambuk.wav',8),(1440,'Effect/codeClawEfx.mp3',8)]:r.sound(n,f,t)

def jura(r):
    charge=[]
    for k in r.names('juura_BijuDamaChg'):
        im=r.atlas.frames[k][0];charge.append(r.use(k,role='center',axis=(96,80),erase=(0,82,47,im.height)))
    r.action(27110,charge,step=2)
    shots=[]
    for i,k in enumerate(r.names('juura_BijuDamaShot')):
        im=r.atlas.frames[k][0];left=65 if i==0 else 140
        axis=[(150,78),(273,132),(285,130),(300,130),(318,130)][i]
        shots.append(r.use(k,role='center',crop=(left,0,im.width,im.height),axis=axis))
    r.action(27111,shots,step=3,loop=True,boxes={1:[(-28,-24,28,24)],2:[(-28,-24,28,24)]})
    bomb=[]
    for k in r.names('juura_BijuDamaBom'):
        im=r.atlas.frames[k][0];bb=Image.fromarray((np.array(im.getchannel('A'))>=128).astype('uint8')*255).getbbox()
        bomb.append(r.use(k,role='ground',crop=(70,0,im.width,im.height),axis=(340,bb[3]-1)))
    r.action(27112,bomb,step=4)
    # Original ocular sniper beam, separated from the miniature caster baked
    # into the left edge of the Senki composite. The physical aimed shot stays.
    beam=[]
    for k in r.names('JuraExShot',1,4):
        im=r.atlas.frames[k][0];beam.append(r.use(k,role='center',crop=(90,0,im.width,im.height),axis=(90,110)))
    r.action(27113,beam,step=3)
    r.add(1200,explod(1200,27113,10,pos='18,-65',scale='.35,.35',duration=12,bind=-1))
    # Replace generic circles; the physical helper still uses the accepted
    # downward aim, life budget and contact tests against small opponents.
    r.edit(9300,lambda b:remove_controller(remove_controller(remove_controller(b,'Purple-black ocular chakra'),'Violet chakra rim'),'Collision follows visible orb size').replace('anim = 8841','anim = 27111'))
    r.edit(9301,lambda b:b.replace('anim = 8820','anim = 27112').replace('Time>=15','Time>=40')+controller(9301,'Ground the actual source explosion','PosSet','trigger1=Time=0\ny=0')+controller(9301,'Impact scale follows the fired orb','AngleDraw','trigger1=1\nscale=.20+FVar(0)*.18,.20+FVar(0)*.18'))
    r.edit(9530,lambda b:remove_controller(remove_controller(b,'Dark ocular core'),'Living violet rim').replace('anim = 8841','anim = 27110')+controller(9530,'Launch original travelling bijudama','ChangeAnim','trigger1=Time=24\nvalue=27111'))
    for n,t,scale in [(1020,1,'.30,.30'),(1030,4,'.48,.48'),(1200,1,'.16,.16'),(1420,1,'.2,.2'),(1430,4,'.32,.32')]:
        r.add(n,explod(n,27110,t,pos='18,-65',scale=scale,duration=14,bind=-1))
    for t in [24,44]:r.add(1430,explod(1430,27110,t,pos='18,-65',scale='.32,.32',duration=14,bind=-1))
    def cinematic(b):
        blocks=re.split(r'(?=\[State\s+)',b,flags=re.I);added=False;out=[]
        for p in blocks:
            if 'type = Explod' in p and re.search(r'(?im)^anim\s*=\s*(8820|8830)',p):
                if not added:
                    p=explod(3001,27112,80,pos='145,0',scale='.56,.56',duration=60,priority=6);added=True
                else:p=''
            out.append(p)
        return ''.join(out)
    r.edit(3001,cinematic)
    r.replace(8602,r.seq('MokuShinju',role='ground'))
    for n,f,t in [(1020,'Effect/BijuDama.mp3',15),(1030,'Effect/BijuDama.mp3',31),(1200,'Effect/BijuDama.mp3',10),(1430,'Effect/BijuDama.mp3',14),(3001,'Effect/charge2.ogg',32),(3001,'Effect/BijuDama.mp3',56),(1000,'Effect/mokutonMsv.mp3',8),(1050,'Effect/mokutonMsv.mp3',8),(1210,'Effect/codeClawEfx.mp3',6),(1211,'Effect/codeClawEfx.mp3',6)]:r.sound(n,f,t)

def mitsuki(r):
    # This bank is the original six green snake-shaped electrical frames.
    # No yellow palette substitution is applied to Sage Mode.
    green=r.seq('SageGaara_Snakes',role='center')
    r.replace(8950,green)
    r.replace(11020,r.seq('SageGaara_Chg'))
    r.replace(8932,r.seq('Gaara_HebiMikazuchi',1,4,role='center'))
    # Separate finish bursts, only after the physical lightning connects.
    r.action(27120,r.seq('Gaara_HebiMikazuchi',5,10,role='center'),step=2)
    r.add(9432,controller(9432,'Original lightning contact burst','Explod','trigger1=MoveContact\nanim=27120\npostype=P1\npos=0,0\nremovetime=-2\nownpal=1\nsprpriority=5\npersistent=0'))
    # Restore the actual full cast families previously skipped in base mode.
    r.replace(1000,r.seq('Gaara_NAttack',1,10))
    r.replace(1200,r.seq('Gaara_SegelTangan'))
    r.replace(11050,r.seq('SageGaara_Ulti'))
    for n,p,t in [(1010,'Mitsuki/ToppaEfx.mp3',8),(1020,'Mitsuki/Raiton2.ogg',16),(11020,'Mitsuki/EfxorochiIkazuchi.mp3',16),(1030,'Mitsuki/efxKamaitachi.mp3',8),(11030,'Mitsuki/efxKamaitachi.mp3',8),(520,'Mitsuki/MitsukiSageTransform.mp3',0),(1050,'Effect/snake.wav',8),(11050,'Effect/snake.wav',8)]:r.sound(n,p,t)

def ryu(r):
    # Caster and free projectile are independent. The Senki rectangles contain
    # both; leaving both copies visible makes two tornadoes/prisons overlap.
    for n,p,lo,hi in [(1000,'Shino_Skill01_Blt',1,4),(1010,'Shino_Skill04',16,25),(1020,'Shino_Skill02',1,13),(1030,'Shino_Skill03',13,20),(1200,'Shino_Skill01_Blt',1,4),(1430,'Shino_Skill04',1,10)]:
        seq=r.cast_body(p,lo,hi);r.replace(n,seq);r.replace(n+10000,seq)
    for n in [3000,13000]:r.replace(n,r.seq('Shino_Skill05',1,8))
    # The wing atlas contains Ryu himself. Render it once as the cinematic
    # helper, hide the duplicate root, and keep both at the exact same pivot.
    r.action(8615,r.seq('Shino_Skill05',9,31),step=8)
    r.edit(9500,lambda b:remove_controller(b,'Wings open and fold').replace('pos=0,-70','pos=0,0')+controller(9500,'Native supplied winged body','AngleDraw','trigger1=1\nscale=1,1'))
    for n in [3001,13001]:r.add(n,controller(n,'Single supplied winged figure','AssertSpecial','trigger1=NumHelper(9500)>0\nflag=Invisible'))
    tornado=[]
    for k in r.names('Shino_Skill04',1,14):
        im=r.atlas.frames[k][0];tornado.append(r.use(k,role='ground',crop=(80,0,im.width,im.height)))
    r.replace(8620,tornado)
    prison=r.seq('Shino_Skill03_2',8,16,role='ground',size=(.38,.38))
    burst=r.seq('Shino_Skill03_2',17,23,role='ground',size=(.38,.38))
    r.action(8612,prison+prison[-1:]+burst,times=[2]*len(prison)+[44]+[3]*len(burst),boxes={1:[(-40,-100,40,0)]})
    # Include the full end of the source iron-shuriken strike, at contact.
    r.action(27130,r.seq('Shino_Skill04',26,36,role='ground'),step=2)
    r.add(9430,controller(9430,'Original iron impact','Explod','trigger1=MoveContact\nanim=27130\npostype=P1\npos=0,0\nscale=.6,.6\nremovetime=-2\nownpal=1\nsprpriority=4\npersistent=0'))
    blast=[]
    for k in r.names('Shino_Skill05',32,47):
        im,axis,*_=r.atlas.frames[k];left=max(0,min(im.width-1,round(axis[0]+45)))
        # The landing explosion contains a tiny caster at the left edge.
        blast.append(r.use(k,role='ground',crop=(left,0,im.width,im.height)))
    r.action(27131,blast,step=2)
    for n in [3001,13001]:r.add(n,explod(n,27131,160,pos='75,0',scale='.65,.65',duration=32))
    for n,s,t in [(1000,'Effect/CyborgTranshand.mp3',8),(1010,'Effect/Blade00.mp3',8),(1020,'Effect/elect2.ogg',8),(1030,'Effect/break_sound3.ogg',8),(1430,'Effect/hao_chg2.ogg',8),(1210,'Effect/codeClawEfx.mp3',6),(1211,'Effect/codeClawEfx.mp3',6)]:
        r.sound(n,s,t)
        if re.search(state_pattern(n+10000),r.texts[r.ch+'.cns']):r.sound(n+10000,s,t)

def hidari(r):
    # The supplied Hidari sheet already has a complete YELLOW Susanoo.
    # Keep the accepted Sasuke-derived move logic and all nine guardian moves;
    # use Hidari's own arrival, idle, sword strike and disappearance artwork.
    def guardian(lo,hi,extra=0):
        seq=[]
        for k in r.names('Zabuza_Skill05',lo,hi):
            im=r.atlas.frames[k][0];bb=Image.fromarray((np.array(im.getchannel('A'))>=128).astype('uint8')*255).getbbox()
            seq.append(r.use(k,role='ground',axis=(255,bb[3]-1+extra)))
        return seq
    r.replace(24050,guardian(8,11))
    r.replace(24200,guardian(12,21,30))
    r.replace(24550,guardian(1,7))
    r.action(27140,guardian(22,28),step=2)
    r.add(-2,controller(-2,'Original yellow guardian dissolves at expiry','Explod','trigger1=Var(42)=1 && Var(40)=1\nanim=27140\nID=27140\npostype=P1\npos=0,0\nscale=.3,.3\nremovetime=-2\nownpal=1\nsprpriority=-1\nremoveongethit=1'))
    for n,s,t in [(1010,'Effect/CyborgTranshand2.mp3',8),(1030,'Effect/Katon.mp3',8),(1050,'hidari/codeClawEfx.mp3',8),(1210,'hidari/codeClawEfx.mp3',6),(1211,'hidari/codeClawEfx.mp3',6),(1430,'hidari/Kirin.mp3',8),(520,'Effect/Transform.mp3',100)]:r.sound(n,s,t)

def matsuri(r):
    waves=[]
    for p in ['Hashirama_Stn01','Hashirama_Stn01A','Hashirama_Stn01B','Hashirama_Stn01C']:
        waves+=r.seq(p,role='center')
    r.replace(8630,waves)
    r.replace(8631,r.seq('Hashirama_Stn02',5,8,role='center'))
    # Cape-in-place rush is a BODY sequence, not a detached floating cape.
    r.replace(1010,r.seq('Hashirama_Skill04_Ex'))
    r.replace(1040,r.seq('Hashirama_Skill04_Kick'))
    # Large source floor eruptions can play in both forms without changing
    # the uncloaked awakening body or reintroducing loose clothing frames.
    roots=[]
    for k in r.names('Hashirama_Skill04',6,27):
        im,ax,*_=r.atlas.frames[k];left=max(0,min(im.width-1,int(ax[0]+40)))
        roots.append(r.use(k,role='ground',crop=(left,0,im.width,im.height)))
    r.action(27150,roots,step=2)
    for n in [3001,13001]:r.add(n,explod(n,27150,102,pos='60,0',scale='.65,.65',duration=44))
    for n,s,t in [(1000,'Effect/mokuBlade.mp3',8),(1020,'Matsuri/MizuWater.mp3',8),(1030,'Effect/mokutonMsv.mp3',8),(1050,'Matsuri/DotonFx.mp3',8),(1210,'Matsuri/codeClawEfx.mp3',6),(1211,'Matsuri/codeClawEfx.mp3',6),(3001,'Matsuri/DotonFx.mp3',102)]:
        r.sound(n,s,t)
        if re.search(state_pattern(n+10000),r.texts[r.ch+'.cns']):r.sound(n+10000,s,t)

def eida(r):
    # Full paired embrace remains at the fighter's natural 85-pixel scale.
    # Keep the real Japanese Eida voice, and the previously accepted timing.
    hug=[]
    for k in r.names('Chiyo_S5_PreUp'):
        im=r.atlas.frames[k][0];bb=Image.fromarray((np.array(im.getchannel('A'))>=128).astype('uint8')*255).getbbox()
        hug.append(r.use(k,role='ground',axis=(im.width//2,bb[3]-1)))
    r.action(8600,hug,times=[10]*9+[8])
    r.action(27160,r.seq('Omnipotence',role='center'),step=3)
    r.add(3001,explod(3001,27160,66,pos='0,-40',scale='.18,.18',duration=42,priority=-2,bind=-1)+'trans=AddAlpha\nalpha=200,256\n','Omnipotencia.cns')
    r.replace(1300,r.seq('Chiyo_S1'))
    # Daemon's authentic charge and impact sequence, preserving collision times.
    r.replace(1000,r.seq('Parents_Skill01'))
    r.replace(1010,r.seq('Parents_Skill01'))
    r.sound(3001,'Effect/OmnipotenceSFx.mp3',66,file='Omnipotencia.cns')
    r.sound(1300,'Effect/Senrigan.mp3',0)
    r.sound(1350,'Effect/Senrigan.mp3',0)

def main():
    OUT.mkdir(exist_ok=True);reports=[]
    for ch,stem in CHARS.items():
        if sys.argv[1:] and ch not in sys.argv[1:]:continue
        r=Revision(ch,stem);globals()[stem.lower()](r);reports.append(r.finish());print(json.dumps(reports[-1]),flush=True)
    p=OUT/'build.json';previous=json.loads(p.read_text()) if p.exists() else []
    merged={r['character']:r for r in previous};merged.update({r['character']:r for r in reports})
    p.write_text(json.dumps(list(merged.values()),indent=2)+'\n')
if __name__=='__main__':main()
