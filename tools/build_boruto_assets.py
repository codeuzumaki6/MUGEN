#!/usr/bin/env python3
"""Preserve the supplied Boruto sprites, original voices and technique sounds."""
from pathlib import Path
import collections,io,json,plistlib,re,struct,subprocess,wave
import numpy as np
from PIL import Image,ImageDraw
from build_roster_revision import Archive
from boruto_source import ROOT,SRC,BodyPivots,nums,sha,save_sff,read_sff
CHAR=ROOT/'BorutoKarmaJogan';A=CHAR/'assets'
ATLASES=['Pain/Pain.plist','Nagato/Nagato.plist','DevaPath/DevaPath.plist','AsuraPath/AsuraPath.plist','Skill/Pain_Skill.plist','Animalpath/AnimalPath.plist','Flog/IzumoFlog.plist','Flog/KakashiFlog.plist']
PREFIXES=('Pain_','PainNol','Unframe_','UnFx_','JgDm','Jougan','BOLT_','Angin','Wind','RasenShotWind_','FutonRasenWind_','Duar_Move_','Waver_')
def kind(key):
 n=int(key.rsplit('_',1)[-1]) if key.rsplit('_',1)[-1].isdigit() else 0
 if key.startswith(('JouganSCR_','JouganEye_')):return 'cutin'
 if not key.startswith(('Pain_','Unframe_')):return 'effect'
 if key.startswith('Pain_Skill01_') and (20<=n<=31 or 36<=n<=48):return 'effect'
 if key.startswith('Pain_Skill02_') and (n in list(range(1,9))+[13] or 25<=n<=32 or 55<=n<=65):return 'effect'
 if key.startswith('Pain_Skill03_') and 12<=n<=30:return 'effect'
 if key.startswith('Pain_Skill04_') and (1<=n<=28 or 37<=n<=44):return 'effect'
 if key.startswith('Pain_Skill05_') and 125<=n<=140:return 'effect'
 return 'body' if key.startswith(('Pain_Idle_','Pain_Walk_','Pain_Hurt_','Pain_AirHurt_','Pain_KnockDown_','Unframe_')) else 'body_with_effect'
def main():
 for f in ['frames','sound']:(A/f).mkdir(parents=True,exist_ok=True)
 cells=[];excluded=[];inherited=[];keys={};manifest=[];counter=collections.Counter()
 for g,rel in enumerate(ATLASES,32000):
  p=SRC/rel;data=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA')
  for source_key,m in data['frames'].items():
   key=source_key.removesuffix('.png')
   if not key.startswith(PREFIXES):inherited.append(dict(plist=rel,key=key));continue
   x,y,w,h=map(int,nums(m['frame']))
   if not w or not h:excluded.append(dict(plist=rel,key=key));continue
   im=sheet.crop((x,y,x+w,y+h));im=im.transpose(Image.Transpose.ROTATE_90) if m.get('rotated') else im;bb=im.getbbox()
   if not bb:excluded.append(dict(plist=rel,key=key));continue
   ox,oy=nums(m['offset']);axis=(round(im.width/2-ox),bb[3]-1);k=kind(key)
   if k in ['effect','cutin']:axis=(im.width//2,im.height//2)
   if key.startswith(('Duar_Move_','Pain_Skill01_2','Pain_Skill04_2')) and k=='effect':axis=(im.width//2,bb[3]-1)
   assert key not in keys,key;keys[key]=[g,counter[g]];counter[g]+=1
   cells.append(dict(key=key,group=g,number=keys[key][1],im=im,axis=axis,kind=k,source_plist=str(p.relative_to(ROOT)),source_key=source_key,source_rotated=m.get('rotated',False)))
 neutral=set()
 for stem,indices in [('Skill01',[60,65,66]),('Skill02',[9,14,15,16,17,22,24,33]),('Skill03',[32,33,34,55]),('Skill04',[29,36]),('Skill05',[1,2,3,4,23,24,25,63,143,144])]:neutral.update(f'Pain_{stem}_{i:02}' for i in indices)
 neutral.update(f'Pain_Skill01_{i:02}ex' for i in range(32,36));neutral.update(f'Pain_NAttack_{i:02}' for i in [1,11,12,17,18])
 templates=[(c['key'],c['im'],c['axis']) for c in cells if c['kind']=='body' or c['key'] in neutral]
 pivots=BodyPivots(templates);pack=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());pack.entries.clear()
 cache=Path('/tmp/boruto-review/indexed_cache');cache.mkdir(exist_ok=True)
 def put(key,g,n,im,axis,**meta):
  p=A/'frames'/f'{g}_{n}.png';im.save(p);digest=sha(im.tobytes());npz=cache/(digest+'.npz')
  if npz.exists():
   v=np.load(npz);pix=v['pix'].tobytes();pal=v['pal'].tobytes();pack.entries[g,n]=(im.width,im.height,*axis,pix,pal)
  else:
   pack.put((g,n),im,axis);e=pack.entries[g,n];np.savez_compressed(npz,pix=np.frombuffer(e[4],dtype=np.uint8),pal=np.frombuffer(e[5],dtype=np.uint8))
  e=pack.entries[g,n];manifest.append(dict(key=key,group=g,number=n,file=str(p.relative_to(CHAR)),axis=list(axis),rgba_sha256=digest,indexed_pixels_sha256=sha(e[4]),palette_sha256=sha(e[5]),redrawn=False,ai_generated=False,**meta));keys[key]=[g,n]
 for i,cell in enumerate(cells):
  im=cell['im'];axis=cell['axis'];alignment=dict(method='original body feet' if cell['kind'] in ['body','body_with_effect'] else 'standalone effect centre')
  if cell['kind']=='body_with_effect' and (im.width>160 or im.height>150):
   alignment=pivots.align(cell['key'],im,axis);axis=tuple(alignment['axis'])
  # Some full-screen composites have no opaque feet; keep pivots inside SFF bounds.
  axis=(min(max(axis[0],0),im.width-1),min(max(axis[1],0),im.height-1))
  put(cell['key'],cell['group'],cell['number'],im,axis,alignment=alignment,**{k:v for k,v in cell.items() if k not in ['key','group','number','im','axis']})
  if i%50==0:print('Imported',i,'/',len(cells),flush=True);pivots.save()
 pivots.save();common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 entry=next(c for c in cells if c['key']=='Pain_Idle_01');face=entry['im'].crop((25,0,65,40))
 for n,size in [(0,(25,25)),(1,(120,140))]:
  tile=face.resize((25,25) if n==0 else (110,120),Image.Resampling.NEAREST);im=Image.new('RGBA',size);im.alpha_composite(tile,((size[0]-tile.width)//2,(size[1]-tile.height)//2));put(f'Portrait_{n}',9000,n,im,(0,0),kind='portrait')
 save_sff(pack.entries,CHAR/'BorutoKarmaJogan.sff');actual=read_sff(CHAR/'BorutoKarmaJogan.sff');assert actual==pack.entries
 for name,data in [('keys',keys),('sprites',manifest),('excluded_frames',excluded),('unused_inherited_frames',inherited)]:(A/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 original_pixels=sum(len(v[4]) for v in actual.values());print('SFF:',len(actual),'sprites;',original_pixels,'raw pixel bytes;',(CHAR/'BorutoKarmaJogan.sff').stat().st_size,'RLE8 bytes',flush=True)
 # Import all 11 original character samples plus effects actually referenced by the main XML.
 text=(SRC/'Pain/Pain.xml').read_text();soundrefs=set(re.findall(r'<eventName type="setSound">([^<]+)</eventName>',text))
 selected=set(p for p in (SRC/'Audio/BorutoJogan').iterdir() if p.suffix.lower() in ['.mp3','.ogg','.wav'])
 for ref in soundrefs:
  p=SRC/ref
  if p.is_file():selected.add(p)
  elif p.with_suffix('.ogg').is_file():selected.add(p.with_suffix('.ogg'))
 for name in ['rasenS.ogg','RsgAura.mp3','RaitonEfx.mp3','aura.ogg','BladeA.ogg','dash_effect.ogg','windeffect.mp3','mon2.ogg','BladeC.ogg','RSGfuton.mp3','charge2.ogg']:
  p=SRC/'Audio/Effect'/name
  if p.exists():selected.add(p)
 data=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',data,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',data,off);samples[g,n]=data[off+16:off+16+size];off=nxt
 smap={};audio=[];counts=collections.Counter()
 for p in sorted(selected):
  g=3 if p.parent.name=='BorutoJogan' else 2;n=counts[g];counts[g]+=1;dest=A/'sound'/f'{g}_{n}.wav'
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-map_metadata','-1','-ac','1','-ar','22050','-c:a','pcm_s16le','-bitexact',str(dest)],check=True)
  samples[g,n]=dest.read_bytes();smap[p.parent.name+'/'+p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=sha(p.read_bytes()),group=g,number=n,wav_sha256=sha(dest.read_bytes())))
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',header,16,len(samples),512);parts=[];off=512
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  pad=(-len(wav))%4;nxt=off+16+len(wav)+pad if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav+bytes(pad));off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'BorutoKarmaJogan.snd').write_bytes(bytes(header)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=smap,source_audio=audio),indent=2)+'\n')
 board=Image.new('RGB',(1400,((len(manifest)+6)//7)*140),(35,38,43));d=ImageDraw.Draw(board)
 for i,r in enumerate(manifest):
  im=Image.open(CHAR/r['file']);im.thumbnail((194,112),Image.Resampling.NEAREST);x=i%7*200;y=i//7*140;board.paste(im,(x+(200-im.width)//2,y),im);d.text((x,y+115),r['key'].replace('Pain_',''),fill='white')
 board.save(ROOT/'previews/BorutoKarmaJogan_original_sprites.jpg');print('Original cells:',len(cells),'selected original audio:',len(audio),'shared total audio:',len(samples),'excluded empty:',len(excluded),flush=True)
if __name__=='__main__':main()
