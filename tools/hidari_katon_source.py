#!/usr/bin/env python3
"""Original Sasuke BTM Gokakyu sprites, explosion, and two nonverbal sounds."""
from pathlib import Path
import hashlib,json,struct
import numpy as np
from PIL import Image
from hidari_susanoo_source import ensure_source,actions,frames,export_action
from read_sff_v1 import Sff1
ROOT=Path(__file__).resolve().parents[1]
ACTION_IDS=[1150,1160]

def transparent_black(im):
 v=np.array(im.convert('RGBA'));v[:,:,3][np.max(v[:,:,:3],axis=2)==0]=0
 return Image.fromarray(v)

def export_assets(put):
 source=Sff1(ensure_source());acts=actions();records=[]
 for g,n in sorted({(g,n) for a in ACTION_IDS for g,n,*_ in frames(acts[a])}):
  im,axis=source.image(g,n);im=transparent_black(im)
  put(g+10000,n,im,axis,source_sasuke_katon=[g,n],original_colors=True,redrawn=False)
  records.append(dict(source=[g,n],packed=[g+10000,n],axis=axis,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest()))
 (ROOT/'HidariShinju/assets/katon_source.json').write_text(json.dumps(dict(source='Sasuke BTM supplied by the user; Shingeki No Mugen / Vovan99',actions=ACTION_IDS,original_colors=True,ai_generated=False,sprites=records,sounds={'20,0':'Sasuke 4,10','20,1':'Sasuke 4,8'}),indent=2)+'\n')

def append_sounds(original):
 data=bytearray(original);count,off=struct.unpack_from('<II',data,16)
 for _ in range(count):last=off;off=struct.unpack_from('<I',data,off)[0]
 struct.pack_into('<I',data,16,count+2);struct.pack_into('<I',data,last,len(data))
 for i,n in enumerate([10,8]):
  blob=(ROOT/f'source_material/Sasuke_BTM_original/katon_sounds/4_{n}.wav').read_bytes()
  nxt=len(data)+16+len(blob) if i==0 else 0
  data.extend(struct.pack('<4I',nxt,len(blob),20,i));data.extend(blob)
 return bytes(data)

def install(m):
 for a in ACTION_IDS:
  m.air.append(export_action(a,.32 if a==1150 else .24,loop=a==1150,box='-28,-27,28,28' if a==1150 else None))
 c,state,snd=m.c,m.state,m.snd
 n=9401;s=state(n,21150,'A','A','N',vel='9,3.5')
 s+=c(n,'Fireball descends from mouth to body height','VelSet','Time>=9','y=0')
 s+=c(n,'Original Gokakyu dimensions','AngleDraw','1','value=0\nscale=IfElse(Time<6,.17+Time*.025,.32),IfElse(Time<6,.17+Time*.025,.32)','ignorehitpause=1')
 s+=c(n,'Original additive flame','Trans','1','trans=AddAlpha\nalpha=256,96','ignorehitpause=1')+c(n,'Fire draws in front','SprPriority','1','value=3','ignorehitpause=1')+c(n,'Flame has no shadow','AssertSpecial','1','flag=NoShadow','ignorehitpause=1')+c(n,'Flame has no push box','PlayerPush','1','value=0','ignorehitpause=1')
 s+=m.hit(n,0,160,True,airborne=True,stun=35).replace('attr=A,SA','attr=A,SP').replace('hitsound=S1,19','hitsound=-1').replace('sparkno=S8700','sparkno=-1')+'hitonce=1\n'
 s+=snd(n,'Time=0',20,0,2,85)+c(n,'Explode once on real contact','ChangeState','MoveContact','value=9402')+c(n,'Finite fireball flight','DestroySelf','Time>=64 || RoundState!=2')
 m.states.append(s)
 n=9402;s=state(n,21160,'A',physics='N')+c(n,'Original explosion size','AngleDraw','1','value=0\nscale=.24,.24','ignorehitpause=1')+c(n,'Explosion glow','Trans','1','trans=AddAlpha\nalpha=256,96','ignorehitpause=1')+c(n,'Explosion has no shadow','AssertSpecial','1','flag=NoShadow','ignorehitpause=1')+c(n,'Explosion is visual only','PlayerPush','1','value=0','ignorehitpause=1')
 s+=snd(n,'Time=0',20,1,2,85)+c(n,'Clear original fire explosion','DestroySelf','AnimTime=0 || Time>=48 || RoundState!=2');m.states.append(s)
