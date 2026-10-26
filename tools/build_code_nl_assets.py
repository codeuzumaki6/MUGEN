#!/usr/bin/env python3
"""Import Code No Limiter atlases and selected sounds from the user's Code."""
from pathlib import Path
import hashlib,json,plistlib,re,struct,subprocess
from PIL import Image,ImageDraw
from build_roster_revision import Archive
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'CodeNoLimiter';A=CHAR/'assets';SRC=ROOT/'source_material/CodeNoLimiter_original/Code'
def nums(s):return list(map(float,re.findall(r'-?\d+(?:\.\d+)?',s)))
def sha(b):return hashlib.sha256(b).hexdigest()
def snd(path):
 b=path.read_bytes();count,off=struct.unpack_from('<2I',b,16);out={}
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<4I',b,off);out[g,n]=b[off+16:off+16+size];off=nxt
 return out
VOICES={'intro':(190,5),'win':(180,0),'die':(170,1),'attack':(300,0),'claw':(950,2),'teleport':(1000,0),'rush':(1100,0),'grime':(1200,0),'superior':(1300,0),'karma':(1400,0),'ultimate':(3000,7),'ultimate_end':(3000,4),'hurt':(5000,3)}
def main():
 for d in ['frames','sound']:(A/d).mkdir(parents=True,exist_ok=True)
 pack=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes());pack.entries.clear();manifest=[];mapping={};excluded=[]
 def put(key,g,n,im,axis,**extra):
  p=A/'frames'/f'{g}_{n}.png';im.save(p);pack.put((g,n),im,axis);mapping[key]=[g,n];manifest.append(dict(key=key,group=g,number=n,file=str(p.relative_to(CHAR)),axis=list(axis),rgba_sha256=sha(im.tobytes()),redrawn=False,ai_generated=False,**extra))
 for group,rel in [(31000,'Kankuro/Kankuro.plist'),(31001,'Skill/Kankuro_Skill.plist')]:
  p=SRC/rel;data=plistlib.loads(p.read_bytes());sheet=Image.open(p.parent/data['metadata']['textureFileName']).convert('RGBA')
  for key,m in data['frames'].items():
   x,y,w,h=map(int,nums(m['frame']));key=key.removesuffix('.png')
   if not w or not h:excluded.append(key);continue
   im=sheet.crop((x,y,x+w,y+h))
   if m.get('rotated'):im=im.transpose(Image.Transpose.ROTATE_90)
   bb=im.getbbox()
   if not bb:excluded.append(key);continue
   ox,oy=nums(m['offset']);axis=(round(im.width/2-ox),bb[3]-1);kind='body';method='original body feet'
   n=int(key.rsplit('_',1)[-1])
   if key.startswith(('Tsumeato_','MokuShinju_','CodeNLTILES_','Jiku_','Troops_','TroopsAtk_')) or key.startswith('Kankuro_Skill05_') and n>=21:
    kind='effect';axis=(im.width//2,bb[3]-1);method='original prop ground plane'
    if key.startswith('Kankuro_Skill05_') and n>=21:kind='body_with_effect';axis=(im.width//2,440);method='original Code inside the complete Karma column, grounded final body feet'
    if key.startswith('CodeNLTILES_'):axis=(im.width//2,im.height//2)
    if key.startswith('MokuShinju_'):axis=(im.width//2,220);method='original tree root and terrain centre'
   elif key.startswith(('Grime_','ThirdKazekage_','PrimeTsumeaka_')):
    kind='minion';method='original Claw Grime body foot';axis=(round(im.width/2-ox),87)
    if '_Skill01_' in key:axis=(105,152)
    if key.startswith('PrimeTsumeaka_'):
     axis=(55,87) if n<=3 else (60,152) if n<=9 else (200,181) if n<=14 else (65,130)
    if key.startswith('ThirdKazekage_') and ('_Idle_' in key or '_Hurt_' in key or '_KnockDown_' in key):kind='fragment';axis=(55,81)
   elif key.startswith('Kankuro_NAttack_'):axis=(55,103);kind='body_with_effect'
   elif key.startswith('Kankuro_Skill01_'):
    axis=(45,86) if n<=3 else (65,86) if n<=11 else (135,103);kind='body_with_effect' if n>=4 else 'body'
   elif key.startswith('Kankuro_Skill04_'):
    axis=(65,160) if n<=9 else (155,177) if n<=15 else (65,220) if n<=21 else (45,113);kind='body_with_effect' if n<=21 else 'body'
   elif key.startswith('Kankuro_Skill05_'):
    axis=(115,160) if n<=7 else (35,72) if n<=10 else (200,130);kind='body_with_effect'
   elif key.startswith('CodeNLTelep_'):
    axis=(65,90);kind='body_with_effect' if n>=4 else 'effect'
   elif key.startswith('CodeNLAura_'):axis=(70,160);kind='body_with_effect'
   elif key.startswith('EndChg_'):axis=(80,145);kind='body_with_effect'
   if key.startswith('Kankuro_Walk_'):axis=(45,72)
   if key.startswith(('Kankuro_Hurt_','Kankuro_AirHurt_','Kankuro_Float_')):axis=(45,86)
   if key.startswith('Kankuro_KnockDown_'):axis=(45,94 if n in [3,4] else 91 if n==5 else 86)
   put(key,group,sum(v['group']==group for v in manifest),im,axis,kind=kind,alignment=method,source_plist=str(p.relative_to(ROOT)),source_key=key+'.png',source_rectangle=[x,y,x+w,y+h],source_rotated=m.get('rotated',False))
 common=Archive((ROOT/'JuraShinju/JuraShinju.sff').read_bytes())
 for g,count in [(8700,4),(8710,4),(8720,6),(8900,24)]:
  for n in range(count):im,axis=common.image((g,n));put(f'Common_{g}_{n}',g,n,im,axis,kind='effect',shared_project_effect=True)
 idle=Image.open(CHAR/next(v for v in manifest if v['key']=='Kankuro_Idle_01')['file']).convert('RGBA')
 for n,size in [(0,(25,25)),(1,(120,140))]:
  im=idle.crop((10,0,45,43));im=im.resize((25,25) if n==0 else (100,125),Image.Resampling.NEAREST);portrait=Image.new('RGBA',size);portrait.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));put(f'Portrait_{n}',9000,n,portrait,(0,0),kind='portrait')
 pack.save(CHAR/'CodeNoLimiter.sff')
 (A/'sprites.json').write_text(json.dumps(manifest,indent=2)+'\n');(A/'keys.json').write_text(json.dumps(mapping,indent=2)+'\n');(A/'excluded_frames.json').write_text(json.dumps(dict(empty=excluded,unrelated_donor_atlas='Karasu/Karasu.plist',unrelated_frames=23),indent=2)+'\n')
 samples=snd(ROOT/'JuraShinju/JuraShinju.snd');reference=ROOT/'source_material/Shibai_Code_reference/Code.snd';original=snd(reference);sounds={};proof=[]
 for i,(name,pair) in enumerate(VOICES.items()):
  raw=original[pair];dest=A/'sound'/f'4_{i}.wav';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','pipe:0','-ac','1','-ar','22050','-c:a','pcm_s16le',str(dest)],input=raw,capture_output=True,check=True);wav=dest.read_bytes();samples[4,i]=wav;sounds[name]=[4,i];proof.append(dict(name=name,group=4,number=i,source=str(reference.relative_to(ROOT)),source_group=pair[0],source_number=pair[1],source_wav_sha256=sha(raw),wav_sha256=sha(wav)))
 header=bytearray(512);header[:12]=b'ElecbyteSnd\0';header[12:16]=bytes((1,0,1,0));struct.pack_into('<2I',header,16,len(samples),512);off=512;parts=[]
 for i,((g,n),wav) in enumerate(sorted(samples.items())):
  nxt=off+16+len(wav) if i+1<len(samples) else 0;parts.append(struct.pack('<4I',nxt,len(wav),g,n)+wav);off=nxt;(A/'sound'/f'{g}_{n}.wav').write_bytes(wav)
 (CHAR/'CodeNoLimiter.snd').write_bytes(bytes(header)+b''.join(parts));(A/'sounds.json').write_text(json.dumps(dict(keys=sounds,source_audio=proof,source_snd_sha256=sha(reference.read_bytes()),uploaded_zip_has_audio=False),indent=2)+'\n')
 board=Image.new('RGB',(1400,((len(manifest)+6)//7)*135),(35,38,43));d=ImageDraw.Draw(board)
 for i,r in enumerate(manifest):
  im=Image.open(CHAR/r['file']);im.thumbnail((195,105),Image.Resampling.NEAREST);x=i%7*200;y=i//7*135;board.paste(im,(x+(200-im.width)//2,y),im);d.text((x,y+108),r['key'].replace('Kankuro_',''),fill='white')
 board.save(ROOT/'previews/CodeNoLimiter_original_sprites.jpg');print('Code:',len(manifest),'sprites;',len(samples),'sounds;',excluded)
if __name__=='__main__':main()
