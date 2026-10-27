#!/usr/bin/env python3
"""Import the supplied Vaydra cells without repainting their RGBA pixels."""
from pathlib import Path
import hashlib,json,plistlib,re,struct,subprocess
from PIL import Image,ImageDraw
from build_roster_revision import Archive
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'HimawariTBV';A=CHAR/'assets'
SRC=ROOT/'source_material/Himawari_original/HimawariTBV by Vaydra'
def nums(s):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',s)))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 for folder in ['frames','sound']:(A/folder).mkdir(parents=True,exist_ok=True)
 pack=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());pack.entries.clear();manifest=[];keys={};excluded=[]
 def put(key,g,n,im,axis,**meta):
  p=A/'frames'/f'{g}_{n}.png';im.save(p);pack.put((g,n),im,axis);keys[key]=[g,n]
  manifest.append(dict(key=key,group=g,number=n,file=str(p.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),redrawn=False,ai_generated=False,**meta))
 atlases=['KinkakuET/KinkakuET.plist','KinkakuET/KinkakuET_Skill.plist','Bombard.plist','FxEx.plist','Effects/Shadows.plist']
 for g,rel in enumerate(atlases,32000):
  p=SRC/rel;data=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA');n=0
  for source_key,m in data['frames'].items():
   key=source_key.removesuffix('.png');x,y,w,h=map(int,nums(m['frame']));im=sheet.crop((x,y,x+w,y+h))
   if m.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
   if not w or not h or not im.getbbox():excluded.append(key);continue
   bb=im.getbbox();ox,oy=nums(m['offset']);axis=(round(im.width/2-ox),bb[3]-1);kind='effect';idx=int(key.rsplit('_',1)[-1]) if key.rsplit('_',1)[-1].isdigit() else 0
   if key.startswith('KinkakuET_'):
    kind='body'
    if key.startswith(('KinkakuET_Float_02','KinkakuET_Float_03')):kind='unused_inherited_effect'
    elif key.startswith('KinkakuET_FlyKick_') and idx<=3:axis=(153,154);kind='body_with_effect'
    elif key.startswith('KinkakuET_Jkn_'):axis=(85,141);kind='body_with_effect'
    elif key.startswith('KinkakuET_ComKick01_') and idx<=3:axis=(75,141);kind='body_with_effect'
    elif key.startswith('KinkakuET_ComKick02_') and idx<=3:axis=(65,145);kind='body_with_effect'
    elif key.startswith('KinkakuET_ComKick03_') and 2<=idx<=5:axis=(105,135);kind='body_with_effect'
    elif key=='KinkakuET_ComKick03_06':axis=(105,100);kind='body_with_effect'
    elif key.startswith('KinkakuET_Lock_'):axis=(15,87);kind='body_with_effect'
    elif key.startswith('KinkakuET_Tksu_') and idx<=6:axis=(179,180);kind='body_with_effect'
    elif key.startswith('KinkakuET_BidamCHG_'):axis=(85,232) if idx<=6 else (65,228);kind='body_with_effect'
    elif key.startswith('KinkakuET_BidamATK_'):axis=(135,235) if idx<=7 else (25,96);kind='body_with_effect'
    elif key.startswith('KinkakuET_Trans_'):axis=(105,207);kind='body_with_effect'
    elif key.startswith('KinkakuET_kyubiCKRStance_'):axis=(70,100);kind='body_with_effect'
    elif key.startswith('KinkakuET_kyubiCKRCHG_'):axis=(62,75);kind='body_with_effect'
    elif key.startswith('KinkakuET_kyubiCKRCLAW01_'):axis=(160,202) if idx<=3 else (160,154) if idx==4 else (135,98);kind='body_with_effect'
    elif key.startswith('KinkakuET_kyubiCKRCLAW02_'):axis=(155,160);kind='body_with_effect'
    elif key.startswith('KinkakuET_kyubiUltiBom_'):axis=(300,315);kind='body_with_effect'
    elif key.startswith('KinkakuET_kyubiUlti_'):axis=(200,145);kind='effect'
   elif key.startswith('Bombard_'):axis=(im.width//2,im.height-1)
   elif key.startswith('Duar_Move_'):axis=(im.width//2,im.height-1)
   else:axis=(im.width//2,im.height//2)
   body=None
   if kind=='body_with_effect':
    if key.startswith('KinkakuET_FlyKick_'):body=(140,75,210,130)
    elif key.startswith('KinkakuET_Jkn_'):body=(60,66,130,120)
    elif key.startswith('KinkakuET_ComKick01_'):body=(52,80,110,139)
    elif key.startswith('KinkakuET_ComKick02_'):body=(50,80,95,135)
    elif key.startswith('KinkakuET_ComKick03_'):body=(76,65,120,122) if idx<=5 else (65,62,125,125)
    elif key.startswith('KinkakuET_Tksu_'):body=(150,110,218,177)
    elif key.startswith('KinkakuET_BidamCHG_'):body=(70,146,120,233) if idx<=6 else (50,142,100,229)
    elif key.startswith('KinkakuET_BidamATK_') and idx<=7:body=(122,155,162,240)
    elif key.startswith('KinkakuET_Trans_'):body=(75,140,135,207)
    elif key.startswith('KinkakuET_kyubiCKRStance_'):body=(42,45,82,101)
    elif key.startswith('KinkakuET_kyubiCKRCHG_'):body=(30,37,85,80)
    elif key.startswith('KinkakuET_kyubiCKRCLAW01_'):body=(140,140,218,200) if idx<=3 else (125,95,185,151) if idx==4 else (125,44,182,96)
    elif key.startswith('KinkakuET_kyubiCKRCLAW02_'):body=(130,105,205,160)
    elif key.startswith('KinkakuET_kyubiUltiBom_'):body=(255,265,315,317)
   collision=[body[0]-axis[0],body[1]-axis[1],body[2]-axis[0],body[3]-axis[1]] if body else None
   put(key,g,n,im,axis,kind=kind,collision_box=collision,source_plist=str(p.relative_to(ROOT)),source_key=source_key,source_rotated=m.get('rotated',False));n+=1
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 face=Image.open(CHAR/next(r['file'] for r in manifest if r['key']=='KinkakuET_Idle_01')).convert('RGBA').crop((5,3,35,34))
 for n,size in [(0,(25,25)),(1,(120,140))]:
  tile=face.resize((25,25) if n==0 else (110,115),Image.Resampling.NEAREST);im=Image.new('RGBA',size);im.alpha_composite(tile,((size[0]-tile.width)//2,(size[1]-tile.height)//2));put(f'Portrait_{n}',9000,n,im,(0,0),kind='portrait')
 pack.save(CHAR/'HimawariTBV.sff')
 for name,data in [('sprites',manifest),('keys',keys),('excluded_frames',excluded)]:(A/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 data=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',data,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',data,off);samples[g,n]=data[off+16:off+16+size];off=nxt
 smap={};audio=[]
 for g,folder in [(2,SRC/'Audio/Effect'),(3,SRC/'Audio/HimawariTBV'),(4,SRC/'Audio')]:
  for n,p in enumerate(sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in ['.mp3','.ogg'])):
   dest=A/'sound'/f'{g}_{n}.wav';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-ac','1','-ar','22050','-c:a','pcm_s16le',str(dest)],check=True);samples[g,n]=dest.read_bytes();smap[folder.name+'/'+p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=sha(p.read_bytes()),group=g,number=n,wav_sha256=sha(dest.read_bytes())))
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',header,16,len(samples),512);parts=[];off=512
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  nxt=off+16+len(wav) if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'HimawariTBV.snd').write_bytes(bytes(header)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=smap,source_audio=audio),indent=2)+'\n')
 b=Image.new('RGB',(1400,((len(manifest)+6)//7)*140),(35,38,43));d=ImageDraw.Draw(b)
 for i,r in enumerate(manifest):
  im=Image.open(CHAR/r['file']);im.thumbnail((194,112),Image.Resampling.NEAREST);x=i%7*200;y=i//7*140;b.paste(im,(x+(200-im.width)//2,y),im);d.text((x,y+115),r['key'].replace('KinkakuET_',''),fill='white')
 b.save(ROOT/'previews/HimawariTBV_original_sprites.jpg');print(len(manifest),'sprites;',len(audio),'original audio;',excluded)
if __name__=='__main__':main()
