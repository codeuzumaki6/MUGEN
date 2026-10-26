#!/usr/bin/env python3
"""Import Jigen originals, preserving authored bodies and projectile-only props."""
from pathlib import Path
import hashlib,json,plistlib,re,struct,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from build_roster_revision import Archive
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'JigenKara';A=CHAR/'assets';SRC=ROOT/'source_material/Jigen_original/Jigen rep Jiraiya'
def nums(s):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',s)))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 for d in ['frames','sound']:(A/d).mkdir(parents=True,exist_ok=True)
 raw={};excluded=[]
 for rel in ['jiraiya/Jiraiya.plist','jiraiya/Jiraiya_Skill.plist']:
  p=SRC/rel;data=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA')
  for key,m in data['frames'].items():
   x,y,w,h=map(int,nums(m['frame']))
   if not w or not h:excluded.append(key);continue
   im=sheet.crop((x,y,x+w,y+h))
   if m.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
   if not im.getbbox():excluded.append(key);continue
   raw[key]=(im,m,p)
 archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries.clear();manifest=[];mapping={}
 def put(key,g,n,im,axis,**meta):
  dest=A/'frames'/f'{g}_{n}.png';im.save(dest);archive.put((g,n),im,axis);mapping[key]=[g,n];manifest.append(dict(key=key,group=g,number=n,file=str(dest.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),redrawn=False,ai_generated=False,**meta))
 def box(im):return Image.fromarray((np.array(im.getchannel('A'))>=128).astype('uint8')*255).getbbox() or im.getbbox()
 for key,(im,m,p) in raw.items():
  offset=nums(m['offset']);ox,oy=offset[0],sum(offset[1:]);bb=box(im);axis=(round(im.width/2-ox),bb[3]-1);kind='body';method='original body foot';form=0
  if key.startswith(('BesiJigen','Asap_','Kubus','JigenCup_','Jiraiya_Skill02Iron')) or key=='Jiraiya_Float_02' or key.startswith(('Jiraiya_wake_02','Jiraiya_wake_03','Jiraiya_wake_04','Jiraiya_wake_05')):
   kind='effect';axis=(im.width//2,bb[3]-1);method='original standalone prop ground plane'
   if key.startswith('BesiJigen'):axis=(im.width//2,im.height//2);method='original flying rods centre'
   if key.startswith('Jiraiya_Skill02Iron'):axis=(137,180);method='original rod and ground plane'
   if key.startswith('KubusIdle'):axis=(im.width//2,125);method='original solid cube base'
  elif key.startswith('Jiraiya_Ulti_'):
   form=1;kind='body_with_effect';method='original Jigen body ground plane inside Ten Tails sequence'
   y=359 if '_Smn_' in key else 239 if '_Chg_' in key or '_juubi_' in key else 290 if '_shoot_' in key or key.endswith('Boom_01') else 348 if '_Boom_' in key else 247
   axis=(215,y)
  elif key.startswith('Jiraiya_Skill03_cross_'):
   kind='body_with_effect';axis=(142,130) if im.width==260 else (95,66);method='original flying body plane independent of blue streak'
  elif key.startswith('Jiraiya_Skill03_slash_'):
   kind='body_with_effect' if im.width>100 else 'body';axis=(127,186) if im.width>100 else (35,83);method='original slash body plane'
  elif key.startswith('Jiraiya_Skill4_lutut_') and '_Chg_' not in key:
   kind='body_with_effect' if im.width>100 else 'body';axis=(56,117) if im.width>100 else (35,85);method='original knee body plane'
  elif key.startswith('Jiraiya_Skill4_Kick_') and '_Chg_' not in key:
   kind='body_with_effect' if im.width>100 else 'body';axis=(115,142) if im.width>100 else (35,box(im)[3]-1);method='original kicking body plane'
  if key.startswith('Jiraiya_Skill05_'):form=1
  g=30001 if '_Ulti_' in key else 30000
  put(key,g,sum(e['group']==g for e in manifest),im,axis,kind=kind,form=form,alignment=method,source_plist=str(p.relative_to(ROOT)),rectangle=m['frame'],source_offset=m['offset'],source_rotated=m.get('rotated',False))
 # Keep the complete original cells and split only the distant explosion
 # from the caster so its ground plane can follow the actual struck enemy.
 for i in range(1,11):
  key=f'Jiraiya_Ulti_Boom_{i:02}';im,_,_=raw[key];original=next(v for v in manifest if v['key']==key)
  caster=im.crop((0,0,390,im.height));blast=im.crop((390,0,im.width,im.height));bb=blast.getbbox()
  put('Caster_'+key,30002,i,caster,tuple(original['axis']),kind='body_with_effect',source_key=key,source_rectangle=[0,0,390,im.height],form=1,alignment='original caster plane, explosion separated')
  put('Blast_'+key,30003,i,blast,(blast.width//2,bb[3]-1),kind='effect',source_key=key,source_rectangle=[390,0,im.width,im.height],alignment='original explosion grounded at the struck enemy')
 # The authored horn is a separate runtime layer, never a second body.
 # Keeping its exact pixels lets the engine attach it to each original pose.
 horn_key='Jiraiya_Skill05_Trans_04';horn_rect=[17,0,36,10]
 put('Horn_layer',30004,0,raw[horn_key][0].crop(horn_rect),(9,8),kind='effect',source_key=horn_key,source_rectangle=horn_rect,alignment='original horn attached to the current body head')
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 for n,size in [(0,(25,25)),(1,(120,140))]:
  im=raw['Jiraiya_Idle_01'][0].crop((10,0,39,34));im=im.resize((25,25) if n==0 else (110,125),Image.Resampling.NEAREST);out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));put(f'Portrait_{n}',9000,n,out,(0,0),kind='portrait')
 archive.save(CHAR/'JigenKara.sff');(A/'keys.json').write_text(json.dumps(mapping,indent=2)+'\n');(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n');(A/'excluded_frames.json').write_text(json.dumps(excluded,indent=2)+'\n')
 b=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',b,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',b,off);samples[g,n]=b[off+16:off+16+size];off=nxt
 import xml.etree.ElementTree as ET
 selected=set()
 for p in SRC.rglob('*.xml'):
  for e in ET.parse(p).iter('e'):
   if e.attrib.get('type')=='setSound' and e.text:selected.add(e.text.strip())
 extras=['absorb efx.mp3','sukonaMini.mp3','karma.mp3','Karma2.mp3','BesiJatoh.mp3','BesiNancep.mp3','BesiIn.mp3','Kubus.ogg','kubus jatuh.mp3','kubus2.mp3','Kokugan.ogg','DashFx.mp3','AuraGates.ogg','charge2.ogg','rock_hit2.ogg','stick_damage.mp3','throw.ogg','besi5.ogg','tengs.mp3']
 for name in extras:selected.add('Audio/Effect/'+name)
 effect_paths=sorted(SRC/p for p in selected if p.startswith('Audio/Effect/') and (SRC/p).is_file());missing=sorted(p for p in selected if not (SRC/p).is_file())
 smap={};audio=[]
 for g,paths in [(2,effect_paths),(3,sorted((SRC/'Audio/Jigen').iterdir()))]:
  for n,p in enumerate(paths):
   if not p.is_file():continue
   dest=A/'sound'/f'{g}_{n}.wav';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-ac','1','-ar','22050','-c:a','pcm_s16le',str(dest)],check=True);samples[g,n]=dest.read_bytes();smap[p.parent.name+'/'+p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=sha(p.read_bytes()),group=g,number=n))
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',header,16,len(samples),512);off=512;parts=[]
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  nxt=off+16+len(wav) if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'JigenKara.snd').write_bytes(bytes(header)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=smap,source_audio=audio,missing_source_references=missing),indent=2)+'\n')
 board=Image.new('RGB',(1200,((len(raw)+7)//8)*135),(35,38,43));draw=ImageDraw.Draw(board)
 for i,(key,(im,_,_)) in enumerate(raw.items()):
  im=im.copy();im.thumbnail((146,105),Image.Resampling.NEAREST);x=i%8*150;y=i//8*135;board.paste(im,(x+(150-im.width)//2,y),im);draw.text((x+1,y+108),key,fill='white')
 board.save(ROOT/'previews/JigenKara_original_sprites.jpg');print('Jigen assets:',len(raw),'original cells;',len(manifest),'sprites;',len(samples),'sounds;',len(audio),'imported audio;',excluded)
if __name__=='__main__':main()
