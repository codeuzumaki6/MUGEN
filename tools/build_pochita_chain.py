#!/usr/bin/env python3
"""A visible physical chain extension and actual forward movement for rushes."""
from pathlib import Path
import json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]

def append_chain_assets(metadata,review):
 char=ROOT/'PochitaTrueForm';im=Image.open(ROOT/'design/Pochita_devour/chain_extension.png').convert('RGBA');poses=[];records=[];metadata['chain_extension']=[]
 for row in range(2):
  for col in range(4):
   box=(im.width*col//4,im.height*row//2,im.width*(col+1)//4,im.height*(row+1)//2);pic=im.crop(box)
   pic.putalpha(pic.getchannel('A').point(lambda a:255 if a>=128 else 0));bounds=pic.getbbox();assert bounds
   assert bounds[0]>0 and bounds[1]>0 and bounds[2]<pic.width and bounds[3]<pic.height,(row,col,bounds)
   poses.append((pic.crop(bounds),box))
 factor=min(220/max(p.width for p,_ in poses),60/max(p.height for p,_ in poses))
 folder=char/'assets/sprites/chain_extension';folder.mkdir(parents=True,exist_ok=True)
 for i,(pic,box) in enumerate(poses):
  pic=pic.resize((round(pic.width*factor),round(pic.height*factor)),Image.Resampling.NEAREST);out=Image.new('RGBA',(256,148));out.alpha_composite(pic,(16,36-pic.height//2));path=folder/f'{i}.png';out.save(path)
  metadata['chain_extension'].append(dict(group=9800,number=i,file=str(path.relative_to(char)),size=out.size,axis=(0,74),source_sheet='chain_extension',source_cell=i,source_box=box))
  records.append((9800,i,path,(0,74)));review.append(('chain_extension',i,out))
 return records

def apply_chain_runtime(char):
 cns=(char/'PochitaTrueForm.cns').read_text();air=(char/'PochitaTrueForm.air').read_text()
 meta=json.loads((char/'assets/sprites.json').read_text())['chain_extension'];poses=[0,1,2,3,3,4,3,4,3,5,6,7];contacts=[4,6,9]
 # Chain is the player's collision sprite, body is a bound visual layer. Both
 # share the same position; no helper, target snap or invisible extended Clsn.
 air+='\n[Begin Action 1031]\nClsn2Default: 1\n Clsn2[0] = -17,-72,17,0\n'
 for index,pose in enumerate(poses,1):
  if index in [4,5,6,7,9,10]:
   pic=Image.open(char/meta[pose]['file']);reach=min(220,pic.getbbox()[2]-1)
   air+=f'Clsn1: 1\n Clsn1[0] = 20,-56,{reach},-20\n'
  air+=f'9800,{pose},0,0,5\n'
 match=re.search(r'(?is)\[Statedef 1030\].*?(?=\[Statedef|\Z)',cns);assert match;block=match[0]
 block=block.replace('anim = 1030','anim = 1031',1).replace('velset = 3.5,0','velset = 0,0',1)
 for old,new in [(3,4),(7,6),(11,9)]:block=block.replace(f'trigger1 = AnimElem = {old}\n',f'trigger1 = AnimElem = {new}\n')
 block=block.replace('pos = 42,-36','pos = P2Dist X,-36').replace('pos = 38,-34','pos = P2Dist X,-34')
 body='''[State 1030, Body under the physical chain]
type = Explod
trigger1 = Time = 0
anim = 1030
ID = 9480
postype = p1
pos = 0,0
bindtime = -1
removetime = -1
sprpriority = -1
ownpal = 1
removeongethit = 1
ignorehitpause = 0
'''
 position=block.index('[State 1030, Motor]');block=block[:position]+body+block[position:]
 cns=cns[:match.start()]+block+cns[match.end():]
 cleanup='''[State -2, Remove composite body after chain move]
type = RemoveExplod
trigger1 = StateNo != 1030
ID = 9480
ignorehitpause = 1
''';cns=cns.replace('[Statedef -2]','[Statedef -2]\n'+cleanup,1)
 for state,speed,until in [(1000,4.5,20),(1060,5.5,16),(1100,6,16)]:
  match=re.search(rf'(?is)\[Statedef {state}\].*?(?=\[Statedef|\Z)',cns);assert match;block=match[0]
  motion=f'''[State {state}, Maintain physical approach speed]
type = VelSet
triggerall = Time < {until}
trigger1 = P2Dist X > 40
x = {speed}
[State {state}, Stop approach at contact distance]
type = VelSet
triggerall = Time < {until}
trigger1 = P2Dist X <= 40
x = 0
'''
  marker=f'[State {state}, End]';at=block.index(marker);block=block[:at]+motion+block[at:];cns=cns[:match.start()]+block+cns[match.end():]
 (char/'PochitaTrueForm.air').write_text(air.rstrip()+'\n');(char/'PochitaTrueForm.cns').write_text(cns.rstrip()+'\n')
 path=char/'assets/special_choreography.json';data=json.loads(path.read_text());data['1030'].update(frames=12,ticks_per_frame=5,animation_ticks=60,family='physical_chain_extension',visible_chain_reach=220);path.write_text(json.dumps(data,indent=2)+'\n')
 print('Built a visible chain extension up to 220 units and three physical approach moves')
