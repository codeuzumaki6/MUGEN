#!/usr/bin/env python3
"""Import the supplied Naruto BTM artwork and referenced audio as indexed SFF."""
import json,plistlib,re,struct,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from boruto_source import ROOT,nums,sha
from boruto_tbv_sff import save_sff,read_sff
from build_roster_revision import Archive
NAME='NarutoBTM';CHAR=ROOT/NAME;SRC=ROOT/'source_material/NarutoBTM_original/full_archive/NarutoBTM rep NarutoNew By Vaydra'


def aura_without_actor(im,axis,body,body_axis):
 """Replace only the embedded caster silhouette with adjacent source glow."""
 a=np.array(im);silhouette=body.getchannel('A').point(lambda v:255 if v>=250 else 0).filter(ImageFilter.MaxFilter(5));mask=Image.new('L',im.size);mask.paste(silhouette,(axis[0]-body_axis[0],axis[1]-body_axis[1]))
 for y,row in enumerate(np.array(mask)>0):
  xs=np.flatnonzero(row)
  if not len(xs):continue
  for run in np.split(xs,np.where(np.diff(xs)>1)[0]+1):
   lo=max(0,int(run[0])-1);hi=min(im.width-1,int(run[-1])+1)
   for x in run:a[y,x]=np.round((a[y,lo].astype(float)*(hi-x)+a[y,hi].astype(float)*(x-lo))/(hi-lo)).astype('uint8')
 return Image.fromarray(a)

def refresh_aura():
 """Repack just the eight derived layers; preserve every other packed entry."""
 A=CHAR/'assets';manifest=json.loads((A/'sprites.json').read_text());bykey={r['key']:r for r in manifest};archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries=read_sff(CHAR/(NAME+'.sff'));body=bykey['NarutoNew_Idle_002']
 for n in range(1,9):
  r=bykey[f'KuramaAura_{n:02}'];parent=bykey[r['source_parent']];im=aura_without_actor(Image.open(CHAR/parent['file']).convert('RGBA'),parent['axis'],Image.open(CHAR/body['file']).convert('RGBA'),body['axis']);im.save(CHAR/r['file']);a=np.array(im);alpha=a[:,:,3].astype('uint16');a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[:,:,3]=np.where(alpha>0,255,0);archive.put((r['group'],r['number']),Image.fromarray(a),tuple(r['axis']));entry=archive.entries[r['group'],r['number']];r.update(rgba_sha256=sha(im.tobytes()),pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]),silhouette_fill='horizontal interpolation of adjacent original glow')
 save_sff(archive.entries,CHAR/(NAME+'.sff'));assert read_sff(CHAR/(NAME+'.sff'))==archive.entries;(A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Updated eight original aura layers; other sprites unchanged')

def rasengan_sphere(im):
 """Extract the rotating blue sphere, excluding the caster and motion streaks."""
 im=im.crop((133,73,191,131));a=np.array(im);y,x=np.indices(a.shape[:2]);distance=np.hypot(x-29,y-29)
 cool=(a[:,:,2].astype(float)>=a[:,:,0]*.95)&(a[:,:,1].astype(float)>=a[:,:,0]*.9)
 a[:,:,3]=np.round(a[:,:,3]*np.clip((29-distance)/5,0,1)*cool).astype('uint8');a[a[:,:,3]==0]=0
 return Image.fromarray(a)

def refresh_spheres():
 A=CHAR/'assets';manifest=json.loads((A/'sprites.json').read_text());keys=json.loads((A/'keys.json').read_text());bykey={r['key']:r for r in manifest};archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries=read_sff(CHAR/(NAME+'.sff'))
 for n in range(1,6):
  parent=f'NarutoNew_RS_Hit_{n:02}';key=f'RasenganSphere_{n:02}';im=rasengan_sphere(Image.open(CHAR/bykey[parent]['file']).convert('RGBA'));dest=A/'frames'/f'30101_{n-1}.png';im.save(dest);a=np.array(im);alpha=a[:,:,3].astype('uint16');a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[:,:,3]=np.where(alpha>0,255,0);archive.put((30101,n-1),Image.fromarray(a),(29,29));entry=archive.entries[30101,n-1]
  rec=dict(key=key,group=30101,number=n-1,file=str(dest.relative_to(CHAR)),axis=[29,29],rgba_sha256=sha(im.tobytes()),pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]),storage='RLE8 indexed',redrawn=False,ai_generated=False,kind='effect',source_parent=parent,source_effect_crop=[133,73,191,131],source_effect_radius=29,source_effect_feather=5,source_cool_color_mask=True)
  if key in bykey:bykey[key].update(rec)
  else:manifest.append(rec)
  keys[key]=[30101,n-1]
 save_sff(archive.entries,CHAR/(NAME+'.sff'));assert read_sff(CHAR/(NAME+'.sff'))==archive.entries
 for name,data in [('keys',keys),('sprites',manifest)]:(A/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 print('Packed five rotating Rasengan sphere crops from the original artwork')

def main():
 A=CHAR/'assets';(A/'frames').mkdir(parents=True,exist_ok=True);(A/'sound').mkdir(exist_ok=True)
 archive=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());archive.entries.clear();manifest=[];keys={};raw={};excluded=[]
 def put(key,g,n,im,axis,**meta):
  im=im.convert('RGBA');dest=A/'frames'/f'{g}_{n}.png';im.save(dest);a=np.array(im);alpha=a[:,:,3].astype('uint16')
  if meta.get('kind')=='effect':a[:,:,:3]=((a[:,:,:3].astype('uint16')*alpha[:,:,None]+127)//255).astype('uint8');a[:,:,3]=np.where(alpha>0,255,0)
  else:a[:,:,3]=np.where(alpha>=250,255,0)
  archive.put((g,n),Image.fromarray(a),axis);entry=archive.entries[g,n];keys[key]=[g,n]
  manifest.append(dict(key=key,group=g,number=n,file=str(dest.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),pixels_sha256=sha(entry[4]),palette_sha256=sha(entry[5]),storage='RLE8 indexed',redrawn=False,ai_generated=False,**meta))
 for rel in ['AnginRibut.plist','NarutoNew/NarutoNew.plist','NarutoNew/NarutoNew_Skill.plist']:
  p=SRC/rel;d=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/d['metadata']['textureFileName']).convert('RGBA')
  for key,f in d['frames'].items():
   x,y,w,h=map(int,nums(f['frame']));im=sheet.crop((x,y,x+w,y+h));im=im.transpose(Image.Transpose.ROTATE_90) if f.get('rotated') else im
   if not im.getbbox():excluded.append(key);continue
   ox,oy=nums(f['offset']);axis=(max(0,min(w-1,round(w/2-ox))),max(0,min(h-1,round(h+oy))));raw[key]=(im,axis)
   if key in ['NarutoNew_Float_02','NarutoNew_Float_03','NarutoNew_KnockDown_05','NarutoNew_KnockDown_06']:
    excluded.append(dict(key=key,reason='Embedded gameplay screenshot, not character artwork'));del raw[key];continue
   pure=key.startswith(('AnginRibut_','BlltPunchNrt_','SRK_Walks_','SRKBOM_','SRKDEAD_','fxDoton_'))
   kind='effect' if pure else 'body_with_effect' if im.width>110 or im.height>125 else 'body'
   if key.startswith('BlltPunchNrt_'):axis=(w//2,h//2)
   put(key,30000,len(raw)-1,im,axis,kind=kind,source_plist=str(p.relative_to(ROOT)),source_key=key,source_offset=f['offset'],alignment='original bottom padding and horizontal offset')
 # Original golden flames with the embedded actor masked out, so awakening
 # does not render another Naruto on top of the moving fighter.
 for n in range(1,9):
  key=f'KCM_Trans_{n:02}';im,axis=raw[key];body,body_axis=raw['NarutoNew_Idle_002'];aura=aura_without_actor(im,axis,body,body_axis)
  put(f'KuramaAura_{n:02}',30100,n-1,aura,axis,kind='effect',source_parent=key,excluded_caster_silhouette='NarutoNew_Idle_002',silhouette_filter_size=5,silhouette_fill='horizontal interpolation of adjacent original glow')
 for n in range(1,6):
  parent=f'NarutoNew_RS_Hit_{n:02}';put(f'RasenganSphere_{n:02}',30101,n-1,rasengan_sphere(raw[parent][0]),(29,29),kind='effect',source_parent=parent,source_effect_crop=[133,73,191,131],source_effect_radius=29,source_effect_feather=5,source_cool_color_mask=True)
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
 face=raw['NarutoNew_Idle_01'][0].crop((12,0,31,24))
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
  im=im.copy();im.thumbnail((194,120));x=i%8*200;y=i//8*150;board.paste(im,(x+(200-im.width)//2,y),im);draw.text((x+2,y+123),key.replace('NarutoNew_',''),fill='white')
 board.save(ROOT/'previews'/f'{NAME}_original_sprites.jpg');print(NAME,len(raw),'original frames;',len(manifest),'indexed sprites;',len(audio),'audio references;',len(samples),'sounds;',len(excluded),'excluded atlas cells')
if __name__=='__main__':
 import sys
 refresh_aura() if '--aura-only' in sys.argv else refresh_spheres() if '--spheres-only' in sys.argv else main()
