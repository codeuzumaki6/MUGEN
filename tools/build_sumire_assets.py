#!/usr/bin/env python3
"""Preserve the supplied Sumire and Nue cells and original sound library."""
from pathlib import Path
import hashlib,json,plistlib,re,struct,subprocess
from PIL import Image,ImageDraw
from build_roster_revision import Archive
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'SumireKakei';A=CHAR/'assets';SRC=ROOT/'source_material/Sumire_original/Sumire Kakei By_Vaydra_Senki/Sumire Kakei by Vaydra'
def nums(s):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',s)))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 for d in ['frames','sound']:(A/d).mkdir(parents=True,exist_ok=True)
 pack=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());pack.entries.clear();manifest=[];keys={};excluded=['Slug_Move_01','Slug_Move_02','Slug_Move_03']
 def put(key,g,n,im,axis,**meta):
  p=A/'frames'/f'{g}_{n}.png';im.save(p);pack.put((g,n),im,axis);keys[key]=[g,n];manifest.append(dict(key=key,group=g,number=n,file=str(p.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),redrawn=False,ai_generated=False,**meta))
 for group,rel in [(32000,'Tsunade/Tsunade.plist'),(32001,'Tsunade/Tsunade_Skill.plist')]:
  p=SRC/rel;data=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA')
  for key,m in data['frames'].items():
   x,y,w,h=map(int,nums(m['frame']));key=key.removesuffix('.png')
   if not w or not h:excluded.append(key);continue
   im=sheet.crop((x,y,x+w,y+h))
   if m.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
   bb=im.getbbox()
   if not bb:excluded.append(key);continue
   ox,oy=nums(m['offset']);axis=(round(im.width/2-ox),bb[3]-1);kind='body';method='original body feet';n=int(key.rsplit('_',1)[-1])
   if key.startswith(('SumireBullet_','AsepFXSumire_','GozuTenou_')):
    kind='effect';axis=(im.width//2,im.height//2) if key.startswith(('SumireBullet_','GozuTenou_')) else (im.width//2,bb[3]-1);method='original standalone effect centre or ground'
   elif key.startswith('NueForm02_'):
    kind='familiar';axis=(55,70) if n<=3 else (65,75) if n<=9 else (315,250);method='original small Nue body feet'
   elif key.startswith('NueForm01_'):
    kind='familiar' if n<=5 else 'effect';axis=(im.width//2,im.height//2) if n<=5 else (40,85);method='original spectral Nue bite centre'
   elif key.startswith('BeastNueAtk_'):kind='beast';axis=(225,260);method='original giant Nue body feet, excluding ground sparks'
   elif key.startswith(('BeastNueWalk_','BeastNue_')):kind='beast';axis=(215,216);method='original giant Nue body ground'
   elif key.startswith('Ghost_'):kind='body_with_effect';axis=(165,263);method='single original Sumire body inside violet aura'
   elif key.startswith('Tsunade_Skill01_'):kind='body_with_effect';axis=(35,113)
   elif key.startswith('Tsunade_Skill02_'):
    kind='body_with_effect' if n not in [1,12] else 'body';axis=(165,151) if 2<=n<=6 else (115,140) if 7<=n<=11 else (245,184) if n>=13 else (35,76)
   elif key.startswith('Tsunade_Skill04_'):
    kind='body_with_effect' if n not in [12,13,14,20,21] else 'body';axis=(75,191) if n<=11 else (35,bb[3]-1) if n<=14 else (55,172) if n<=19 else (35,76) if n<=21 else (75,158) if n<=29 else (90,75)
   elif key.startswith('Tsunade_Suiton_'):kind='body_with_effect' if n>=3 else 'body';axis=(25,152) if n>=3 else (35,76)
   if key.startswith(('Tsunade_Hurt_','Tsunade_AirHurt_','Tsunade_Float_')):axis=(45,75)
   if key.startswith('Tsunade_KnockDown_'):axis=(45,bb[3]-1)
   put(key,group,sum(r['group']==group for r in manifest),im,axis,kind=kind,alignment=method,source_plist=str(p.relative_to(ROOT)),source_key=key,source_rotated=m.get('rotated',False))
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 im=Image.open(CHAR/next(r['file'] for r in manifest if r['key']=='Tsunade_Idle2_01')).convert('RGBA').crop((20,8,51,43))
 for n,size in [(0,(25,25)),(1,(120,140))]:
  tile=im.resize((25,25) if n==0 else (100,125),Image.Resampling.NEAREST);portrait=Image.new('RGBA',size);portrait.alpha_composite(tile,((size[0]-tile.width)//2,(size[1]-tile.height)//2));put(f'Portrait_{n}',9000,n,portrait,(0,0),kind='portrait')
 pack.save(CHAR/'SumireKakei.sff');(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n');(A/'keys.json').write_text(json.dumps(keys,indent=2)+'\n');(A/'excluded_frames.json').write_text(json.dumps(excluded,indent=2)+'\n')
 data=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',data,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',data,off);samples[g,n]=data[off+16:off+16+size];off=nxt
 smap={};audio=[]
 for g,folder in [(2,SRC/'Audio/Effect'),(3,SRC/'Audio/SumireKakei'),(4,SRC/'Audio')]:
  files=sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in ['.mp3','.ogg'])
  for n,p in enumerate(files):
   dest=A/'sound'/f'{g}_{n}.wav';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-ac','1','-ar','22050','-c:a','pcm_s16le',str(dest)],check=True);samples[g,n]=dest.read_bytes();smap[folder.name+'/'+p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=sha(p.read_bytes()),group=g,number=n,wav_sha256=sha(dest.read_bytes())))
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',header,16,len(samples),512);parts=[];off=512
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  nxt=off+16+len(wav) if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'SumireKakei.snd').write_bytes(bytes(header)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=smap,source_audio=audio),indent=2)+'\n')
 board=Image.new('RGB',(1400,((len(manifest)+6)//7)*140),(35,38,43));d=ImageDraw.Draw(board)
 for i,r in enumerate(manifest):
  im=Image.open(CHAR/r['file']);im.thumbnail((194,112),Image.Resampling.NEAREST);x=i%7*200;y=i//7*140;board.paste(im,(x+(200-im.width)//2,y),im);d.text((x,y+115),r['key'].replace('Tsunade_',''),fill='white')
 board.save(ROOT/'previews/SumireKakei_original_sprites.jpg');print('Sumire:',len(manifest),'sprites;',len(samples),'sounds;',len(audio),'original audio;',excluded)
if __name__=='__main__':main()
