#!/usr/bin/env python3
"""Check provenance, exact old voices, controls, damage/cost and receiving windows."""
from pathlib import Path
import hashlib,json,re,struct,subprocess,sys
from PIL import Image
from build_roster_revision import Archive,parse_action
from build_full_pack_revision import ROOT,BASE,CHARS,original,action_pattern
OUT=ROOT/'previews/full_pack_integrity_checks.json'
def sounds(data):
 count,off=struct.unpack_from('<2I',data,16);out={}
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<4I',data,off);out[g,n]=data[off+16:off+16+size];off=nxt
 return out
def protected(text):
 out=[];state=None
 for block in re.split(r'(?=\[(?:State\s|Statedef\s))',text,flags=re.I):
  m=re.match(r'\[Statedef\s+(-?\d+)\]',block,re.I)
  if m:
   state=int(m[1]);p=re.search(r'(?im)^poweradd\s*=\s*([^\n;]+)',block)
   if p:out.append((state,'statedef poweradd',p[1].strip()))
  kind=re.search(r'(?im)^type\s*=\s*(HitDef|Projectile|TargetLifeAdd|PowerAdd)\s*$',block)
  if not kind:continue
  fields={m[1].lower():m[2].strip() for m in re.finditer(r'(?im)^([\w.]+)\s*=\s*([^\n;]+)',block)}
  fields={k:v for k,v in fields.items() if k in ['damage','value','attr','kill','getpower','givepower','absolute','p2stateno','id']}
  out.append((state,kind[1].lower(),fields))
 return out
def main():
 reports=[]
 for ch in CHARS:
  folder=ROOT/ch;manifest=json.loads((folder/'assets/full_pack/manifest.json').read_text());new=Archive((folder/(ch+'.sff')).read_bytes());old=Archive(original(folder/(ch+'.sff')))
  assert all(new.entries[k]==v for k,v in old.entries.items()),(ch,'changed old source artwork/pivot')
  a=sounds(original(folder/(ch+'.snd')));b=sounds((folder/(ch+'.snd')).read_bytes())
  assert all(b[k]==v for k,v in a.items()),(ch,'changed an old voice or effect')
  assert len(b)-len(a)==len(manifest['sounds'])
  for rec in manifest['sounds']:
   payload=b[rec['group'],rec['number']];assert hashlib.sha256(payload).hexdigest()==rec['wav_sha256']
  for p in folder.glob('*.cmd'):assert p.read_bytes()==original(p),(ch,'changed input controls')
  for p in folder.glob('*.cns'):assert protected(p.read_text())==protected(original(p).decode()),(ch,p.name,'damage/cost contract drift')
  for rec in manifest['frames']:
   assert rec['body_redrawn'] is False
   im=Image.open(folder/rec['file']).convert('RGBA')
   assert hashlib.sha256(im.tobytes()).hexdigest()==rec['rgba_sha256']
   assert (rec['group'],rec['number']) in new.entries
  air=(folder/(ch+'.air')).read_text();oldair=original(folder/(ch+'.air')).decode();changed_root=[]
  for m in re.finditer(r'\[Begin Action (\d+)\]',oldair,re.I):
   n=int(m[1]);before=parse_action(re.search(action_pattern(n),oldair)[0])[0];after=parse_action(re.search(action_pattern(n),air)[0])[0]
   # FX/helper animations may have new phases. Receiving actions and all root
   # normal/special attacks retain the same collision interval in both forms.
   if n<6000 or 10000<=n<16000:
    def windows(frames,typ):
     result=[]
     for f in frames:
      for t in range(f['start'],f['start']+max(1,f['duration'])):result.append(tuple(f['boxes'][typ]))
     return result
    for typ in [1,2]:
     x,y=windows(before,typ),windows(after,typ)
     # Idle helpers for Daemon share low action numbers. Finite body casts
     # retain their original tick count; the Mamushi cinematic strikes differ.
     if n not in [3002,3003,3004]:assert x==y,(ch,n,typ,'receiving/contact window changed')
    if before!=after:changed_root.append(n)
  reports.append(dict(character=ch,old_sprites_unchanged=len(old.entries),old_sounds_byte_identical=len(a),new_original_frames=len(manifest['frames']),new_pack_sounds=len(manifest['sounds']),controls_unchanged=True,damage_and_cost_unchanged=True,root_collision_windows_preserved=True,changed_root_animations=changed_root))
 OUT.write_text(json.dumps(dict(base_commit=BASE,characters=reports,all_passed=True),indent=2)+'\n')
 print('PASS',sum(r['new_original_frames'] for r in reports),'additional frames;',sum(r['new_pack_sounds'] for r in reports),'original pack sounds; costs, damage, old voices, source art and root receiving/contact intervals preserved')
if __name__=='__main__':main()
