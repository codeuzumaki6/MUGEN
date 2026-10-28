#!/usr/bin/env python3
"""Index uploaded Senki XML as source data, preserving event/frame order."""
from pathlib import Path
import collections,hashlib,json,plistlib,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source_material/Boruto_original/uploaded_xml'
OUTPUT=ROOT/'design/boruto_karma_jogan'
def main():
 index=[];sprites=set();sounds=set();children=set();full=SOURCE.parent/'full_archive';scan=full if full.exists() else SOURCE
 for p in sorted(scan.rglob('*.xml')):
  root=ET.fromstring(re.sub(r'<!--[\s\S]*?-->','',p.read_text(errors='replace')));actions=[]
  for act in root.findall('.//action'):
   frames=[(x.text or '').strip() for x in act.iter() if x.tag in ['f','frameName']]
   events=collections.defaultdict(list)
   for x in act.iter():
    if x.tag in ['e','eventName']:events[x.get('type')].append((x.text or '').strip())
   data={x.get('type'):(x.text or '').strip() for x in act.iter() if x.tag in ['p','dateName','coldName']}
   sequence=[]
   for frame in act.findall('frame'):
    for node in frame:
     value=(node.text or '').strip()
     if node.tag in ['f','frameName']:sequence.append(dict(kind='sprite',value=value))
     elif node.tag in ['e','eventName']:sequence.append(dict(kind='event',type=node.get('type'),value=value))
   actions.append(dict(name=act.get('name') or act.get('value'),data=data,frames=frames,events=dict(events),sequence=sequence))
   sprites.update(frames);sounds.update(events['setSound']);children.update(events['setMon']);children.update(events['setBullet'])
  index.append(dict(file=str(p.relative_to(scan)),actions=actions))
 OUTPUT.mkdir(parents=True,exist_ok=True)
 (OUTPUT/'uploaded_xml_index.json').write_text(json.dumps(index,indent=2,ensure_ascii=False)+'\n')
 atlases=[]
 for p in sorted(scan.rglob('*.plist')):
  data=plistlib.loads(p.read_bytes());m=data['metadata'];texture=m.get('textureFileName',m.get('realTextureFileName'))
  atlases.append(dict(plist=str(p.relative_to(scan)),texture=texture,size=m.get('size'),frames=len(data['frames']),image_received=(p.parent/texture).is_file()))
 audio=SOURCE.parent/'uploaded_audio/manifest.json';audio_files=json.loads(audio.read_text()) if audio.exists() else []
 if full.exists():audio_files=[dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in full.rglob('*') if p.suffix.lower() in ['.ogg','.mp3','.wav']]
 main=any(a['name'] in ['Idle','Walk'] and any('Tenten_' in f or 'Pain_Idle_' in f for f in a['frames']) for item in index for a in item['actions'])
 summary=dict(full_archive_received=full.exists(),xml_files=len(index),sprite_references=sorted(sprites),audio_references=sorted(sounds),spawned_resources=sorted(children),main_character_xml_received=main,atlas_images_received=bool(atlases) and all(a['image_received'] for a in atlases),atlas_plists_received=bool(atlases),atlases=atlases,audio_received=bool(audio_files),audio_files=len(audio_files),unique_audio_files=len({a['sha256'] for a in audio_files}))
 (OUTPUT/'asset_dependencies.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
 for item in index:
  a=next((a for a in item['actions'] if a['name']=='nAttack'),dict(frames=[],events={}))
  print(item['file'],len(a['frames']),'frame steps;',len(set(a['frames'])),'unique frames;',dict(a['events']).get('setMon',[]))
 print('Sprite references:',len(sprites),'Audio references:',len(sounds),'Spawned resources:',sorted(children))
if __name__=='__main__':main()
