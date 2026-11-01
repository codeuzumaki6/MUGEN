#!/usr/bin/env python3
"""Import the supplied Konohamaru artwork and referenced audio as indexed SFF."""
import json,plistlib,re,struct,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from boruto_source import ROOT,nums,sha
from boruto_tbv_sff import save_sff,read_sff
from build_roster_revision import Archive
NAME='KonohamaruTBV';CHAR=ROOT/NAME;SRC=ROOT/'source_material/Konohamaru_original/full_archive/KonohamaruTBV by vaydra'

def main():
 A=CHAR/'assets';(A/'frames').mkdir(parents=True,exist_ok=True);(A/'sound').mkdir(exist_ok=True)
 archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries.clear();manifest=[];keys={};raw={};excluded=[]
 def put(key,g,n,im,axis,**meta):
  im=im.convert('RGBA');dest=A/'frames'/f'{g}_{n}.png';im.save(dest);a=np.array(im);alpha=a[:,:,3].astype('uint16')
  if meta.get('kind')=='effect':a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[:,:,3]=np.where(alpha>0,255,0)
  else:a[:,:,3]=np.where(alpha>=250,255,0)
  archive.put((g,n),Image.fromarray(a),axis);entry=archive.entries[g,n];keys[key]=[g,n]
  manifest.append(dict(key=key,group=g,number=n,file=str(dest.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]),storage='RLE8 indexed',redrawn=False,ai_generated=False,**meta))
 for rel in ['Kakashi/Kakashi.plist','Kakashi/Kakashi_Skill.plist']:
  p=SRC/rel;d=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/d['metadata']['textureFileName']).convert('RGBA')
  for key,f in d['frames'].items():
   x,y,w,h=map(int,nums(f['frame']));im=sheet.crop((x,y,x+w,y+h));im=im.transpose(Image.Transpose.ROTATE_90) if f.get('rotated') else im
   if not im.getbbox():excluded.append(key);continue
   ox,oy=nums(f['offset']);axis=(max(0,min(w-1,round(w/2-ox))),max(0,min(h-1,round(h+oy))));raw[key]=(im,axis)
   pure=key.startswith('MonStaff_');kind='effect' if pure else 'body_with_effect' if im.width>110 or im.height>125 else 'body'
   if pure:axis=(w//2,h//2)
   if key.startswith(('KakashiSkill01_','Kakashi_Skil01_')):
    canonical='Kakashi_Skill01_'+key.rsplit('_',1)[1];assert im.tobytes()==raw[canonical][0].tobytes();axis=raw[canonical][1]
   put(key,30000,len(raw)-1,im,axis,kind=kind,source_plist=str(p.relative_to(ROOT)),source_key=key,source_offset=f['offset'],alignment='original bottom padding and horizontal offset')
 # The seal and massive Rasengan retain their intended summoned clones.
 # Their embedded caster is removed; the full-size player renders separately.
 for stem,ns,g in [('Kakashi_Fuin',range(1,18),30100),('Kakashi_MasivRSG',range(1,32),30101)]:
  for i,n in enumerate(ns):
   key=stem+'_'+(f'{n:02}' if stem.endswith('Fuin') else str(n));im,axis=raw[key];a=np.array(im);rects=[]
   if stem.endswith('Fuin') or n<=6 or n>=28:
    centers=[axis[0],im.width-axis[0]] if stem.endswith('Fuin') else [axis[0]]
    for x in centers:
     rect=[max(0,x-40),max(0,axis[1]-105),min(im.width,x+45),min(im.height,axis[1]+5)];a[rect[1]:rect[3],rect[0]:rect[2]]=0;rects.append(rect)
   ground=axis[1] if stem.endswith('Fuin') else {500:328,400:270,480:330,420:260}[im.width]
   put(('FuinFX' if stem.endswith('Fuin') else 'MassivFX')+f'_{n:02}',g,i,Image.fromarray(a),(im.width//2,ground),kind='effect',source_parent=key,excluded_caster_rects=rects,intentional_summoned_clones=not stem.endswith('Fuin'))
 # Standalone kunai for the throw, cropped from the supplied golden projectile.
 im,axis=raw['Kakashi_Skill04_06'];a=np.array(im);keep=np.indices(a.shape[:2])[1]>im.width*.45;a[~keep]=0;tile=Image.fromarray(a);bb=tile.getbbox();tile=tile.crop(bb)
 put('ThrownKunai',30102,0,tile,(tile.width//2,tile.height//2),kind='effect',source_parent='Kakashi_Skill04_06',source_projectile_crop=list(bb))
 # Light layers contain no opaque actor pixels, and follow the actor's axes.
 for r in list(manifest):
  if r['kind'] not in ['body','body_with_effect']:continue
  a=np.array(Image.open(CHAR/r['file']).convert('RGBA'));alpha=a[:,:,3].astype('uint16');mask=(alpha>0)&(alpha<250)
  if not mask.any():continue
  a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[~mask,:3]=0;a[:,:,3]=np.where(mask,255,0)
  put(r['key']+'_Light',30200,r['number'],Image.fromarray(a),tuple(r['axis']),kind='effect',source_light_parent=r['key'])
 put('LightEmpty',30201,0,Image.new('RGBA',(1,1)),(0,0),kind='effect')
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 face=raw['Kakashi_Idle_01'][0].crop((15,2,37,29))
 for n,size in [(0,(25,25)),(1,(120,140))]:put(f'Portrait_{n}',9000,n,face.resize(size,Image.Resampling.NEAREST),(0,0),kind='portrait')
 save_sff(archive.entries,CHAR/(NAME+'.sff'));assert read_sff(CHAR/(NAME+'.sff'))==archive.entries
 for name,data in [('keys',keys),('sprites',manifest),('excluded_frames',excluded)]: (A/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 # Import all Konohamaru voices and the original effects used by these XMLs.
 requested=set()
 for p in SRC.rglob('*.xml'):
  try:d=ET.parse(p).getroot()
  except ET.ParseError:continue
  requested.update((e.text or '').strip() for e in d.iter('e') if e.get('type')=='setSound')
 files={str(p.relative_to(SRC)).lower():p for p in (SRC/'Audio').rglob('*') if p.is_file()};audio_paths=set((SRC/'Audio/Khm').glob('*'));missing=[]
 for name in requested:
  if name.lower() in files:audio_paths.add(files[name.lower()])
  else:missing.append(name)
 audio_paths.update((SRC/'Audio').glob('*.ogg'));audio_paths.update(files[k] for k in ['audio/effect/rasens.ogg','audio/effect/katon.mp3','audio/effect/charging.ogg','audio/effect/poof2.ogg','audio/effect/stick_damage.ogg'] if k in files)
 base=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',base,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',base,off);samples[g,n]=base[off+16:off+16+size];off=nxt
 audio=[];skeys={};dedup={};counts={2:0,3:0}
 for p in sorted(audio_paths):
  if not p.is_file():continue
  digest=sha(p.read_bytes());g=3 if p.parent.name=='Khm' or p.parent.name=='Audio' else 2
  if digest not in dedup:
   n=counts[g];counts[g]+=1;dest=A/'sound'/f'{g}_{n}.wav';subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(p),'-map_metadata','-1','-ac','1','-ar','22050','-c:a','pcm_s16le','-bitexact',str(dest)],check=True);samples[g,n]=dest.read_bytes();dedup[digest]=[g,n]
  g,n=dedup[digest];skeys[p.parent.name+'/'+p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=digest,group=g,number=n,wav_sha256=sha(samples[g,n])))
 h=bytearray(512);h[:12]=b'ElecbyteSnd\0';h[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',h,16,len(samples),512);parts=[];off=512
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  pad=(-len(wav))%4;nxt=off+16+len(wav)+pad if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav+bytes(pad));off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/(NAME+'.snd')).write_bytes(bytes(h)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=skeys,source_audio=audio,missing_source_references=sorted(missing)),indent=2)+'\n')
 board=Image.new('RGB',(1600,150*((len(raw)+7)//8)),(35,45,55));draw=ImageDraw.Draw(board)
 for i,(key,(im,axis)) in enumerate(raw.items()):
  im=im.copy();im.thumbnail((194,120));x=i%8*200;y=i//8*150;board.paste(im,(x+(200-im.width)//2,y),im);draw.text((x+2,y+123),key.replace('Kakashi_',''),fill='white')
 board.save(ROOT/'previews'/f'{NAME}_original_sprites.jpg');print(NAME,len(raw),'original frames;',len(manifest),'indexed sprites;',len(audio),'audio references;',len(samples),'sounds;',len(excluded),'empty cells')
if __name__=='__main__':main()
