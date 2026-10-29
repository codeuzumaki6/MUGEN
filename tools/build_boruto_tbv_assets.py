#!/usr/bin/env python3
"""Import the supplied TBV base atlas and audio without redrawing characters."""
from pathlib import Path
import hashlib,json,plistlib,re,struct,subprocess
import numpy as np
from PIL import Image,ImageDraw
from boruto_source import ROOT,nums,sha
from boruto_tbv_sff import save_sff,read_sff
from build_roster_revision import Archive

NAME='BorutoTBVBase';CHAR=ROOT/NAME;SRC=ROOT/'source_material/BorutoTBV_original/full_archive/Boruto Ver2 by Vaydra'
def number(key):return int(key.rsplit('_',1)[-1])
def effect(key):
 n=number(key)
 return key.startswith('BoruBlade_') or key.startswith('ShidenBlade_') and (6<=n<=11 or n>=17) or key.startswith('Hiruzen_Skil01_') and n<=6 or key.startswith('Hiruzen_Skill05_') and 14<=n<=19 or key.startswith('Hiruzen_04Bom_') and n>=9
def axis(key,im):
 n=number(key);w,h=im.size
 for prefix,limits,pos in [('Hiruzen_NAttack_',None,(145,161)),('Hiruzen_Skil01_',range(7,15),(155,205)),('ShidenBlade_',range(1,6),(145,208)),('ShidenBlade_',range(12,17),(160,240)),('HiruzenChg03_',None,(145,195)),('Hiruzen_04Chg_',range(1,3),(60,110)),('Hiruzen_04Chg_',range(3,11),(115,225)),('Hiruzen_04Hit_',None,(105,145)),('Hiruzen_04Bom_',range(1,9),(115,100)),('Hiruzen_skill04_',None,(65,110)),('Hiruzen_Skill05_',range(1,7),(105,235)),('Hiruzen_Skill05_',range(7,13),(75,125)),('Hiruzen_Skill05_',range(13,14),(35,76)),('Hiruzen_Skill05_',range(20,28),(125,375)),('Hiruzen_Skill03Atk_',range(3,6),(110,90)),('Hiruzen_Skill03Atk_',range(6,12),(110,115)),('Hiruzen_Skill03Atk_',range(12,14),(110,100)),('Hiruzen_Skil4ED_',None,(110,90))]:
  if key.startswith(prefix) and (limits is None or n in limits):return pos
 if key.startswith('Hiruzen_Skill05_') and 14<=n<=19:return (260,425)
 if effect(key):return (w//2,339 if key.startswith('Hiruzen_04Bom_') else 370 if key.startswith('ShidenBlade_') and n>=17 else h//2)
 if key.startswith('Hiruzen_Idle_'):return (35,92 if len(key.rsplit('_',1)[-1])==2 else 88)
 return (w//2,im.getbbox()[3]-1)
def main():
 A=CHAR/'assets';(A/'frames').mkdir(parents=True,exist_ok=True);(A/'sound').mkdir(exist_ok=True)
 archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries.clear();manifest=[];keys={};excluded=[]
 def put(key,g,n,im,xy,**meta):
  dest=A/'frames'/f'{g}_{n}.png';im.save(dest);storage=im
  if g in [31000,31010]:
   a=np.array(im.convert('RGBA'));alpha=a[:,:,3].astype('uint16')
   if g==31010:alpha=np.rint(alpha*np.minimum(np.arange(im.width)/18,1)[None,:]).astype('uint16')
   if meta.get('kind')=='effect':
    # AIR A supplies additive blending. Black adds zero on legacy renderers.
    a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[:,:,3]=np.where(alpha>0,255,0)
   else:
    # Keep the visible actor in the ordinary indexed sprite. Translucent
    # light in composite frames is exported separately for AIR A blending.
    a[:,:,3]=np.where(alpha>=(250 if meta.get('kind')=='body_with_effect' else 128),255,0)
   storage=Image.fromarray(a)
  archive.put((g,n),storage,xy)
  entry=archive.entries[g,n];keys[key]=[g,n]
  manifest.append(dict(key=key,group=g,number=n,file=str(dest.relative_to(CHAR)),axis=list(xy),rgba_sha256=sha(im.tobytes()),pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]),storage='RLE8 indexed',transparency='AIR additive' if meta.get('kind')=='effect' else 'indexed opaque actor',redrawn=False,ai_generated=False,**meta))
 for rel in ['Hiruzen/Hiruzen.plist','Hiruzen/Hiruzen_Skill.plist']:
  p=SRC/rel;data=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA')
  for raw,r in data['frames'].items():
   key=raw.removesuffix('.png');x,y,w,h=map(int,nums(r['frame']));im=sheet.crop((x,y,x+w,y+h));im=im.transpose(Image.Transpose.ROTATE_90) if r.get('rotated') else im
   if not im.getbbox():excluded.append(dict(plist=rel,key=raw,reason='empty source cell'));continue
   xy=axis(key,im);xy=(min(xy[0],im.width-1),min(xy[1],im.height-1))
   put(key,31000,len(keys),im,xy,kind='effect' if effect(key) else 'body_with_effect' if im.width>160 or im.height>170 else 'body',source_plist=str(p.relative_to(ROOT)),source_key=raw)
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 bykey={r['key']:r for r in manifest}
 for i,n in enumerate(range(20,28)):
  parent=bykey[f'Hiruzen_Skill05_{n:02}'];im=Image.open(CHAR/parent['file']).convert('RGBA');rect=(170,0,680,396)
  put(f'UzuhikoWave_{i:02}',31010,i,im.crop(rect),(-45,375),kind='effect',source_parent=parent['key'],source_rect=list(rect))
 for r in list(manifest):
  if r['group']!=31000 or r['kind']!='body_with_effect':continue
  a=np.array(Image.open(CHAR/r['file']).convert('RGBA'));alpha=a[:,:,3].astype('uint16');mask=(alpha>0)&(alpha<250)
  a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[~mask,:3]=0;a[:,:,3]=np.where(mask,255,0)
  put(r['key']+'_Light',31200,r['number'],Image.fromarray(a),tuple(r['axis']),kind='effect',source_light_parent=r['key'])
 put('LightEmpty',31201,0,Image.new('RGBA',(1,1)),(0,0),kind='effect')
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,xy=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,xy,kind='effect',shared_project_effect=True)
 face=Image.open(CHAR/manifest[3]['file']).crop((20,4,50,34))
 for n,size in [(0,(25,25)),(1,(120,140))]:
  tile=face.resize(size,Image.Resampling.NEAREST);put(f'Portrait_{n}',9000,n,tile,(0,0),kind='portrait')
 save_sff(archive.entries,CHAR/(NAME+'.sff'));assert read_sff(CHAR/(NAME+'.sff'))==archive.entries
 for name,data in [('keys',keys),('sprites',manifest),('excluded_frames',excluded)]: (A/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 base=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',base,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',base,off);samples[g,n]=base[off+16:off+16+size];off=nxt
 audio=[];skeys={};counts={2:0,3:0}
 for p in sorted((SRC/'Audio').rglob('*')):
  if p.suffix.lower() not in ['.mp3','.ogg','.wav'] or p.parent.name=='Audio':continue
  g=3 if p.parent.name=='BorutoTBv' else 2;n=counts[g];counts[g]+=1;dest=A/'sound'/f'{g}_{n}.wav'
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(p),'-map_metadata','-1','-ac','1','-ar','22050','-c:a','pcm_s16le','-bitexact',str(dest)],check=True)
  samples[g,n]=dest.read_bytes();skeys[p.parent.name+'/'+p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=sha(p.read_bytes()),group=g,number=n,wav_sha256=sha(dest.read_bytes())))
 for p in sorted((SRC/'Audio').glob('*.ogg')):
  original=next(r for r in audio if r['source_sha256']==sha(p.read_bytes()))
  audio.append(dict(original,source=str(p.relative_to(ROOT))));skeys['Audio/'+p.stem]=[original['group'],original['number']]
 h=bytearray(512);h[:12]=b'ElecbyteSnd\0';h[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',h,16,len(samples),512);parts=[];off=512
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  pad=(-len(wav))%4;nxt=off+16+len(wav)+pad if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav+bytes(pad));off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/(NAME+'.snd')).write_bytes(bytes(h)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=skeys,source_audio=audio),indent=2)+'\n')
 board=Image.new('RGB',(1400,150*((len(manifest)+6)//7)),(45,55,65));draw=ImageDraw.Draw(board)
 for i,r in enumerate(manifest):
  im=Image.open(CHAR/r['file']);im.thumbnail((195,120));x=i%7*200;y=i//7*150;board.paste(im,(x+(200-im.width)//2,y),im);draw.text((x,y+124),r['key'].replace('Hiruzen_',''),fill='white')
 board.save(ROOT/'previews/BorutoTBVBase_original_sprites.jpg')
 print('Boruto TBV base:',len(manifest),'sprites; source frames',sum(r['group']==31000 for r in manifest),'original sounds',len(audio),'total sounds',len(samples),'excluded',len(excluded))
if __name__=='__main__':main()
