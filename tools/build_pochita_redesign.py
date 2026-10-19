#!/usr/bin/env python3
"""Convert reviewed AI animation sheets into the existing character's SFFv2.
Only frame extraction, shared scaling, transparency and archive conversion happen
here. Creative image changes belong to the image generation/editing workflow.
"""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,struct,hashlib,statistics
import numpy as np
from scipy.ndimage import label,find_objects
from build_archives import png_to_indexed
from build_pochita_finish_assets import append_finish_assets
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'PochitaTrueForm';DESIGN=ROOT/'design/Pochita_revision_visual';ASSETS=CHAR/'assets'
SPEC=[('movimiento',[('idle',0,6),('walk',20,7),('run',100,7),('crouch',10,6),('jump',40,7)]),('basicos',[('air1',600,7),('air2',610,5),('air3',620,6),('attack1',200,7),('attack2',210,6)]),('combos',[('attack3',220,17),('attack3b',230,17)]),('remates_dano',[('attack4',240,6),('attack5',250,8),('damage',5000,15)])]
manifest=json.loads((DESIGN/'sheets/manifest.json').read_text());sheets={};allcells={}
for name,groups in SPEC:
 path=DESIGN/'sheets'/manifest[name]['file'];im=Image.open(path).convert('RGBA');sheets[name]=im
 cells=[];alpha=np.array(im.getchannel('A'))>=128
 spans=[];start=None
 for y,filled in enumerate(list(alpha.any(axis=1))+[False]):
  if filled and start is None:start=y
  if not filled and start is not None:spans.append((start,y));start=None
 spans=[p for p in spans if p[1]-p[0]>30]
 assert len(spans)==6,(name,'expected six separate animation rows',spans)
 for row,(y0,y1) in enumerate(spans):
  labels,n=label(alpha[y0:y1],np.ones((3,3)));objs=find_objects(labels);areas=np.bincount(labels.ravel())
  bodies=sorted([i+1 for i,s in enumerate(objs) if areas[i+1]>1000],key=lambda i:objs[i-1][1].start)
  expected=manifest[name].get('row_counts',[6]*6)[row]
  assert len(bodies)==expected,(name,row,'body count',len(bodies),expected)
  centers={i:np.array([(objs[i-1][0].start+objs[i-1][0].stop)/2,(objs[i-1][1].start+objs[i-1][1].stop)/2]) for i in bodies}
  members={i:[i] for i in bodies}
  # Detached tooth/highlight pixels belong to the nearest complete sprite.
  for i,s in enumerate(objs,1):
   if i in centers:continue
   center=np.array([(s[0].start+s[0].stop)/2,(s[1].start+s[1].stop)/2]);nearest=min(bodies,key=lambda b:np.linalg.norm(center-centers[b]))
   bounds=objs[nearest-1]
   if bounds[1].start-5<=center[1]<=bounds[1].stop+5 and bounds[0].start-5<=center[0]<=bounds[0].stop+5:members[nearest].append(i)
  for body in bodies:
   mask=Image.fromarray((np.isin(labels,members[body])*255).astype('uint8'));bbox=mask.getbbox();assert bbox
   globalbox=[bbox[0],bbox[1]+y0,bbox[2],bbox[3]+y0]
   assert globalbox[0]>0 and globalbox[1]>0 and globalbox[2]<im.width and globalbox[3]<im.height,(name,len(cells),'sprite clipped at source edge',globalbox)
   pic=im.crop((0,y0,im.width,y1));pic.putalpha(mask);cells.append((pic.crop(bbox),globalbox,im.width/6))
 allcells[name]=cells
# Normalize sheet pixel density; all body frames then share the same body scale.
reference=statistics.median(pic.height/cw for pic,box,cw in allcells['movimiento'][:6]);scale_per_cell=72/reference
neutral_cells={'movimiento':list(range(6)),'basicos':list(range(30,36)),'combos':[15,33,34,35],'remates_dano':[34,35]}
sheet_scales={name:72/statistics.median(allcells[name][i][0].height/allcells[name][i][2] for i in indices) for name,indices in neutral_cells.items()}
records=[];metadata={};review=[];quality={}
for sheet,groups in SPEC:
 cellindex=0
 for name,group,count in groups:
  metadata[name]=[];folder=ASSETS/'sprites'/name;folder.mkdir(parents=True,exist_ok=True)
  for index in range(count):
   sourceindex=manifest[sheet].get('groups',{}).get(name,list(range(cellindex,cellindex+count)))[index]
   pic,box,cellwidth=allcells[sheet][sourceindex];factor=sheet_scales[sheet]/cellwidth
   pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST)
   foot=pic.getchannel('A').crop((0,max(0,pic.height-7),pic.width,pic.height)).getbbox();assert foot
   axis=((foot[0]+foot[2])//2+2,pic.height+2)
   if group in [40,600,610,620] or (group==5000 and index in [8,9,10,11]):
    pixels=np.array(pic);torso=(pixels[:,:,3]>128)&(pixels[:,:,:3].max(axis=2)<65)
    torso[:round(pic.height*.3)]=False;torso[round(pic.height*.8):]=False
    yy,xx=np.where(torso);assert len(xx)
    # Air rotations pivot at the torso rather than a swinging boot tip.
    axis=(round(float(xx.mean()))+2,round(float(yy.mean()))+38)
   padded=Image.new('RGBA',(pic.width+4,pic.height+4));padded.alpha_composite(pic,(2,2));path=folder/f'{index}.png';padded.save(path)
   pixels=np.array(padded);body=(pixels[:,:,3]>128)&~((pixels[:,:,0]>70)&(pixels[:,:,0]>pixels[:,:,1]*1.3))
   extent=int(np.where(body)[1].max())-axis[0]
   row=dict(group=group,number=index,file=str(path.relative_to(CHAR)),axis=axis,size=padded.size,attack_extent=extent,source_sheet=sheet,source_cell=sourceindex,source_box=box)
   metadata[name].append(row);records.append((group,index,path,axis));review.append((name,index,padded))
  quality[name]={'frames':count,'heights':[r['size'][1]-4 for r in metadata[name]],'widths':[r['size'][0]-4 for r in metadata[name]]}
  cellindex+=count
assert len(records)==127
records.extend(append_finish_assets(metadata,review))
# Standard HUD portraits use the new model's head/upper chest.
idle=Image.open(ASSETS/'sprites/idle/0.png').convert('RGBA');portrait=idle.crop((0,0,idle.width,round(idle.height*.55)))
for number,size in [(0,(25,25)),(1,(120,140))]:
 p=ImageOps.contain(portrait,size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',size);canvas.alpha_composite(p,((size[0]-p.width)//2,(size[1]-p.height)//2));path=ASSETS/f'portrait_{number}.png';canvas.save(path);records.append((9000,number,path,(0,0)))
packed=[]
for group,index,path,(x,y) in records:
 pixels,palette,w,h,_,_=png_to_indexed(path);packed.append((group,index,w,h,x,y,pixels,palette))
ph=512;sh=ph+len(packed)*16;ld=sh+len(packed)*28;palheaders=[];sprheaders=[];chunks=[];off=0
for i,(group,index,w,h,x,y,pixels,palette) in enumerate(packed):
 palheaders.append(struct.pack('<HHHHII',1,i+1,256,0,off,len(palette)));chunks.append(palette);off+=len(palette)
 sprheaders.append(struct.pack('<HHHHhhHBBIIHH',group,index,w,h,x,y,0,0,8,off,len(pixels),i,0));chunks.append(pixels);off+=len(pixels)
header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,1,0,2));header[24:28]=bytes((0,1,0,2));struct.pack_into('<IIIIIIII',header,36,sh,len(packed),ph,len(packed),ld,off,ld+off,0)
(CHAR/'PochitaTrueForm.sff').write_bytes(bytes(header)+b''.join(palheaders)+b''.join(sprheaders)+b''.join(chunks))
(ASSETS/'sprites.json').write_text(json.dumps(metadata,indent=2)+'\n')
(ASSETS/'redesign_quality.json').write_text(json.dumps(quality,indent=2)+'\n')
unique_poses=len({(r['source_sheet'],r['source_cell']) for values in metadata.values() for r in values if r['group']<9000})
(ASSETS/'source.json').write_text(json.dumps({'type':'AI-generated visual redesign based on user references','master_reference':'design/Pochita_revision_visual/propuesta_tres_poses.png','finisher_sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'design/Pochita_remates').glob('*.png')},'body_sprite_entries':135,'effect_sprite_entries':12,'manga_panel_embedded':False,'unique_source_poses':unique_poses,'normalization':'each sheet calibrated once using neutral poses at 72px; no per-frame stretching','sheet_scales':sheet_scales,'neutral_calibration_cells':neutral_cells,'sheets':{name:{'file':manifest[name]['file'],'sha256':hashlib.sha256((DESIGN/'sheets'/manifest[name]['file']).read_bytes()).hexdigest()} for name,_ in SPEC}},indent=2)+'\n')
canvas=Image.new('RGB',(1200,((len(review)+9)//10)*125),'#a8adb7');draw=ImageDraw.Draw(canvas)
for i,(name,index,picture) in enumerate(review):
 p=picture.copy();p.thumbnail((115,100),Image.Resampling.NEAREST);x=i%10*120;y=i//10*125;canvas.paste(p,(x+(120-p.width)//2,y+20),p);draw.text((x+2,y+2),f'{name}:{index}',fill='black')
canvas.save(ROOT/'previews/Pochita_redesign_sprites.png')
print('Packed 135 body entries + 12 effects + 2 portraits; neutral-calibrated sheet scales',sheet_scales)
print(json.dumps(quality))
