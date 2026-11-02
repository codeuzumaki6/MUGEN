#!/usr/bin/env python3
"""Import the supplied Naruto KCM and Baryon artwork and referenced audio as indexed SFF."""
import json,plistlib,re,struct,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from boruto_source import ROOT,nums,sha
from boruto_tbv_sff import save_sff,read_sff
from build_roster_revision import Archive
NAME='NarutoKCM';CHAR=ROOT/NAME;SRC=ROOT/'source_material/NarutoKCM_original/full_archive/NarutoAdult KCM by vaydra/NarutoAdultKCM rep Naruto'

def refresh_effects():
 A=CHAR/'assets';manifest=json.loads((A/'sprites.json').read_text());bykey={r['key']:r for r in manifest};archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries=read_sff(CHAR/(NAME+'.sff'))
 for r in manifest:
  if 'interpolated_caster_rect' not in r:continue
  parent=r['source_parent'];im=Image.open(CHAR/bykey[parent]['file']).convert('RGBA');x,y=r['axis'];n=int(parent.rsplit('_',1)[1]);rect=r['interpolated_caster_rect']
  if parent.startswith('Naruto_Skill04_Hst') or parent.startswith('Naruto_Skill04_bom') and n<=6:rect=[]
  elif parent.startswith('Naruto_Skill04_bom'):rect[1]=max(0,y-240)
  a=np.array(im)
  for yy in range(rect[1],rect[3]) if rect else []:
   lo=max(0,rect[0]-1);hi=min(im.width-1,rect[2])
   for xx in range(rect[0],rect[2]):a[yy,xx]=np.round((a[yy,lo].astype(float)*(hi-xx)+a[yy,hi].astype(float)*(xx-lo))/(hi-lo)).astype('uint8')
  if parent.startswith('Odama'):
   a=np.array(Image.open(CHAR/bykey[parent]['file']).convert('RGBA'));yy=np.indices(a.shape[:2])[0];start=y-110;finish=y-40;fade=np.clip((yy-start)/(finish-start),0,1);a[:,:,3]=np.round(a[:,:,3]*fade).astype('uint8');a[a[:,:,3]==0]=0;rect=[];r.pop('caster_fill_blur',None);r.pop('caster_fill_feather',None);r.update(source_ground_fade=[start,finish])
  im=Image.fromarray(a.copy());im.save(CHAR/r['file']);alpha=a[:,:,3].astype('uint16');a[:,:,3]=np.where(alpha>=250,255,0) if r.get('kind')=='effect_with_opaque' else np.where(alpha>0,255,0)
  if r.get('kind')!='effect_with_opaque':a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8')
  archive.put((r['group'],r['number']),Image.fromarray(a),tuple(r['axis']));entry=archive.entries[r['group'],r['number']];r.update(interpolated_caster_rect=rect,rgba_sha256=sha(im.tobytes()),pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]))
 save_sff(archive.entries,CHAR/(NAME+'.sff'));assert read_sff(CHAR/(NAME+'.sff'))==archive.entries;(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Refreshed only independent effect layers')

def split_effect_lights():
 A=CHAR/'assets';manifest=json.loads((A/'sprites.json').read_text());keys=json.loads((A/'keys.json').read_text());archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries=read_sff(CHAR/(NAME+'.sff'));extra=[]
 for r in manifest:
  if 'interpolated_caster_rect' not in r:continue
  im=Image.open(CHAR/r['file']).convert('RGBA');a=np.array(im);alpha=a[:,:,3].astype('uint16');solid=a.copy();solid[:,:,3]=np.where(alpha>=250,255,0);archive.put((r['group'],r['number']),Image.fromarray(solid),tuple(r['axis']));entry=archive.entries[r['group'],r['number']];r.update(kind='effect_with_opaque',pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]))
  mask=(alpha>0)&(alpha<250)
  if not mask.any():continue
  light=a.copy();light[:,:,:3]=((light[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');light[~mask,:3]=0;light[:,:,3]=np.where(mask,255,0);li=Image.fromarray(light.copy());n=len(extra);dest=A/'frames'/f'30202_{n}.png';li.save(dest);archive.put((30202,n),li,tuple(r['axis']));entry=archive.entries[30202,n];key=r['key']+'_Light';keys[key]=[30202,n];extra.append(dict(key=key,group=30202,number=n,file=str(dest.relative_to(CHAR)),axis=r['axis'],rgba_sha256=sha(li.tobytes()),pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]),storage='RLE8 indexed',redrawn=False,ai_generated=False,kind='effect',source_light_parent=r['key']))
 manifest=[r for r in manifest if r['group']!=30202]+extra;save_sff(archive.entries,CHAR/(NAME+'.sff'));assert read_sff(CHAR/(NAME+'.sff'))==archive.entries
 for name,data in [('keys',keys),('sprites',manifest)]:(A/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 print('Separated original opaque color from glow for',len(extra),'effect layers')

def main():
 A=CHAR/'assets';(A/'frames').mkdir(parents=True,exist_ok=True);(A/'sound').mkdir(exist_ok=True)
 archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries.clear();manifest=[];keys={};raw={};excluded=[]
 def put(key,g,n,im,axis,**meta):
  im=im.convert('RGBA');dest=A/'frames'/f'{g}_{n}.png';im.save(dest);a=np.array(im);alpha=a[:,:,3].astype('uint16')
  if meta.get('kind')=='effect':a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[:,:,3]=np.where(alpha>0,255,0)
  else:a[:,:,3]=np.where(alpha>=250,255,0)
  archive.put((g,n),Image.fromarray(a),axis);entry=archive.entries[g,n];keys[key]=[g,n]
  manifest.append(dict(key=key,group=g,number=n,file=str(dest.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]),storage='RLE8 indexed',redrawn=False,ai_generated=False,**meta))
 for rel in ['Naruto/Naruto.plist','Naruto/Naruto_Skill.plist']:
  p=SRC/rel;d=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/d['metadata']['textureFileName']).convert('RGBA')
  for key,f in d['frames'].items():
   x,y,w,h=map(int,nums(f['frame']));im=sheet.crop((x,y,x+w,y+h));im=im.transpose(Image.Transpose.ROTATE_90) if f.get('rotated') else im
   if not im.getbbox():excluded.append(dict(key=key,reason='Empty placeholder'));continue
   ox,oy=nums(f['offset']);axis=(max(0,min(w-1,round(w/2-ox))),max(0,min(h-1,round(h+oy))));raw[key]=(im,axis)
   if key.startswith('FutonSRK') or key=='vaydra':
    excluded.append(dict(key=key,reason='Embedded gameplay screenshot' if key.startswith('FutonSRK') else 'Author logo, preserved in original archive'));del raw[key];continue
   pure=key.startswith(('DustFx_','BlinkEfx_'))
   kind='effect' if pure else 'body_with_effect' if im.width>110 or im.height>125 else 'body'
   if pure:axis=(w//2,h-1 if key.startswith('DustFx_') else h//2)
   put(key,30000,len(raw)-1,im,axis,kind=kind,source_plist=str(p.relative_to(ROOT)),source_key=key,source_offset=f['offset'],alignment='original bottom padding and horizontal offset')
 # Remove only the embedded caster from independent chakra-arm effects.
 for stem,count,g in [('Naruto_Skill04_Hst',7,30100),('Naruto_Skill04_bom',13,30101),('OdamaNrt_Hit',4,30102),('OdamaNrt_Bom',6,30103)]:
  for n in range(1,count+1):
   parent=f'{stem}_{n:02}';im,axis=raw[parent];x,y=axis
   rect=[max(0,x-42),max(0,y-(230 if stem.startswith('Odama') else 110)),min(im.width,x+43),min(im.height,y-(95 if stem.startswith('Odama') else -4))]
   if stem=='Naruto_Skill04_Hst' or stem=='Naruto_Skill04_bom' and n<=6:rect=[]
   elif stem=='Naruto_Skill04_bom':rect[1]=max(0,y-240)
   a=np.array(im)
   for yy in range(rect[1],rect[3]) if rect else []:
    lo=max(0,rect[0]-1);hi=min(im.width-1,rect[2])
    for xx in range(rect[0],rect[2]):a[yy,xx]=np.round((a[yy,lo].astype(float)*(hi-xx)+a[yy,hi].astype(float)*(xx-lo))/(hi-lo)).astype('uint8')
   if stem.startswith('Odama'):
    a=np.array(im);yy=np.indices(a.shape[:2])[0];fade=np.clip((yy-(y-110))/70,0,1);a[:,:,3]=np.round(a[:,:,3]*fade).astype('uint8');a[a[:,:,3]==0]=0;rect=[]
   put(parent+'_FX',g,n-1,Image.fromarray(a),axis,kind='effect_with_opaque',source_parent=parent,interpolated_caster_rect=rect,source_ground_fade=[y-110,y-40] if stem.startswith('Odama') else None)
 for n in range(1,5):
  parent=f'OdamaNrt_CHG_{n:02}';im,_=raw[parent];rect=[120,66,210,156];im=im.crop(tuple(rect));a=np.array(im);yy,xx=np.indices(a.shape[:2]);distance=np.hypot(xx-45,yy-45);cool=(a[:,:,2].astype(float)>=a[:,:,0]*.95)&(a[:,:,1].astype(float)>=a[:,:,0]*.9);a[:,:,3]=np.round(a[:,:,3]*np.clip((45-distance)/6,0,1)*cool).astype('uint8');a[a[:,:,3]==0]=0
  put(f'OdamaOrb_{n:02}',30104,n-1,Image.fromarray(a),(45,45),kind='effect',source_parent=parent,source_effect_crop=rect,source_effect_radius=45,source_effect_feather=6,source_cool_color_mask=True)
 # Light layers contain no opaque actor pixels, and follow the actor's axes.
 for r in list(manifest):
  if r['kind'] not in ['body','body_with_effect','effect_with_opaque']:continue
  a=np.array(Image.open(CHAR/r['file']).convert('RGBA'));alpha=a[:,:,3].astype('uint16');mask=(alpha>0)&(alpha<250)
  if not mask.any():continue
  a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[~mask,:3]=0;a[:,:,3]=np.where(mask,255,0)
  put(r['key']+'_Light',30200 if r['group']==30000 else 30202,r['number'] if r['group']==30000 else sum(1 for item in manifest if item['group']==30202),Image.fromarray(a),tuple(r['axis']),kind='effect',source_light_parent=r['key'])
 put('LightEmpty',30201,0,Image.new('RGBA',(1,1)),(0,0),kind='effect')
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 face=raw['Kcm_Idle_01'][0].crop((11,0,32,26))
 for n,size in [(0,(25,25)),(1,(120,140))]:put(f'Portrait_{n}',9000,n,face.resize(size,Image.Resampling.NEAREST),(0,0),kind='portrait')
 save_sff(archive.entries,CHAR/(NAME+'.sff'));assert read_sff(CHAR/(NAME+'.sff'))==archive.entries
 for name,data in [('keys',keys),('sprites',manifest),('excluded_frames',excluded)]: (A/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 # Every supplied voice and effect is imported; XML events are reference data.
 requested=set()
 for p in SRC.rglob('*.xml'):
  try:d=ET.parse(p).getroot()
  except ET.ParseError:continue
  requested.update((e.text or '').strip() for e in d.iter('e') if e.get('type')=='setSound')
 files={str(p.relative_to(SRC)).lower():p for p in (SRC/'Audio').rglob('*') if p.is_file()}
 audio_paths=set(files.values());missing=[name for name in requested if name.lower() not in files]
 base=(ROOT/'JuraShinju/JuraShinju.snd').read_bytes();count,off=struct.unpack_from('<2I',base,16);samples={}
 for _ in range(count):nxt,size,g,n=struct.unpack_from('<4I',base,off);samples[g,n]=base[off+16:off+16+size];off=nxt
 audio=[];skeys={};dedup={};counts={2:0,3:0}
 for p in sorted(audio_paths):
  if not p.is_file():continue
  digest=sha(p.read_bytes());g=3 if p.parent.name=='BTM' or p.parent.name=='Audio' else 2
  if digest not in dedup:
   n=counts[g];counts[g]+=1;dest=A/'sound'/f'{g}_{n}.wav';subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(p),'-map_metadata','-1','-ac','1','-ar','22050','-c:a','pcm_s16le','-bitexact',str(dest)],check=True);samples[g,n]=dest.read_bytes();dedup[digest]=[g,n]
  g,n=dedup[digest];skeys[p.parent.name+'/'+p.stem]=[g,n];audio.append(dict(source=str(p.relative_to(ROOT)),source_sha256=digest,group=g,number=n,wav_sha256=sha(samples[g,n])))
 h=bytearray(512);h[:12]=b'ElecbyteSnd\0';h[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',h,16,len(samples),512);parts=[];off=512
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  pad=(-len(wav))%4;nxt=off+16+len(wav)+pad if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav+bytes(pad));off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/(NAME+'.snd')).write_bytes(bytes(h)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=skeys,source_audio=audio,missing_source_references=sorted(missing)),indent=2)+'\n')
 board=Image.new('RGB',(1600,150*((len(raw)+7)//8)),(35,45,55));draw=ImageDraw.Draw(board)
 for i,(key,(im,axis)) in enumerate(raw.items()):
  im=im.copy();im.thumbnail((194,120));x=i%8*200;y=i//8*150;board.paste(im,(x+(200-im.width)//2,y),im);draw.text((x+2,y+123),key.replace('Naruto_',''),fill='white')
 board.save(ROOT/'previews'/f'{NAME}_original_sprites.jpg');print(NAME,len(raw),'original frames;',len(manifest),'indexed sprites;',len(audio),'audio references;',len(samples),'sounds;',len(excluded),'excluded atlas cells')
if __name__=='__main__':
 import sys
 split_effect_lights() if '--split-effect-lights' in sys.argv else refresh_effects() if '--effects-only' in sys.argv else main()
