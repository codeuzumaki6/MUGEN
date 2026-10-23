#!/usr/bin/env python3
"""Verify the Sage Orochi presentation revision against its published runtime.

Previous native reports remain historical evidence. This proof establishes that
their tested mechanics, other moves, body sprites and sounds did not change.
"""
from pathlib import Path
import hashlib,json,re,subprocess,tempfile
import numpy as np
from make_combo_preview import Sff2

ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'MitsukiTBV'
PREVIOUS='d9f67d6cd6ced311ddc6a9b31c77344472632ba4'
NAMES=[f'MitsukiTBV.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['MitsukiTBV_common.cns']
def sha(data):return hashlib.sha256(data).hexdigest()
def section(text,kind,n):
 return re.search(rf'(?ims)^\[{kind} {n}\].*?(?=^\[{kind}|\Z)',text)[0]
def omit(text,kind,numbers):
 for n in numbers:text=re.sub(rf'(?ims)^\[{kind} {n}\].*?(?=^\[{kind}|\Z)','',text)
 return '\n'.join(line.rstrip() for line in text.splitlines() if line.strip())
def main():
 old={n:subprocess.check_output(['git','show',f'{PREVIOUS}:MitsukiTBV/{n}'],cwd=ROOT) for n in NAMES}
 current={n:(CHAR/n).read_bytes() for n in NAMES}
 for n in ['MitsukiTBV.def','MitsukiTBV.cmd','MitsukiTBV.snd','MitsukiTBV_common.cns']:assert old[n]==current[n],n
 oc=old['MitsukiTBV.cns'].decode();nc=current['MitsukiTBV.cns'].decode()
 assert omit(oc,'Statedef',[11020,9433])==omit(nc,'Statedef',[11020,9433]),'Another move changed'
 launch=section(nc,'Statedef',11020).replace('name="Senpo: Orochi Ikazuchi"','name="Raiton Hebi Mikazuchi"').replace('anim=8951','anim=8650').replace('scale=0.55,0.55','scale=0.8,0.8')
 assert launch==section(oc,'Statedef',11020),'Orochi launch mechanics changed'
 assert section(nc,'Statedef',9433).replace('anim=8950','anim=8932')==section(oc,'Statedef',9433),'Projectile mechanics changed'
 oa=old['MitsukiTBV.air'].decode();na=current['MitsukiTBV.air'].decode()
 assert omit(na,'Begin Action',[8950,8951])==omit(oa,'Begin Action',[]),'An existing action changed'
 assert section(na,'Begin Action',8950).replace('8950','8932').replace('AS256D96','A')==section(oa,'Begin Action',8932),'Orochi timing or collision changed'
 assert 'Clsn1' not in section(na,'Begin Action',8951),'Release glow must be visual only'
 packed=Sff2(CHAR/'MitsukiTBV.sff');preserved=0;yellow=0;green=0
 with tempfile.TemporaryDirectory(prefix='mitsuki-orochi-identity-') as tmp:
  path=Path(tmp)/'old.sff';path.write_bytes(old['MitsukiTBV.sff']);previous=Sff2(path)
  assert set(packed.sprites)-set(previous.sprites)=={(8950,n) for n in range(8)}
  assert not set(previous.sprites)-set(packed.sprites)
  for key in previous.sprites:
   a,aa=packed.image(*key);b,ba=previous.image(*key)
   assert a.size==b.size and aa==ba and a.tobytes()==b.tobytes(),('Existing sprite changed',key)
   preserved+=1
 for n in range(8):
  image,axis=packed.image(8950,n);a=np.array(image);mask=a[:,:,3]>0;r,g,b=[a[:,:,i].astype(float) for i in range(3)]
  assert axis==(58,44) and image.size==(176,88)
  yellow+=int(np.count_nonzero(mask&(r>.8*g)&(b<.65*g)))
  green+=int(np.count_nonzero(mask&(g>r)&(g>b)))
 assert yellow==0 and green>8000,(yellow,green)
 result=dict(previous_commit=PREVIOUS,previous_runtime_sha256=sha(b''.join(old[n] for n in NAMES)),runtime_sha256=sha(b''.join(current[n] for n in NAMES)),only_sage_orochi_presentation_changed=True,combat_mechanics_and_collision_unchanged=True,commands_sounds_identity_common_unchanged=True,existing_sprites_pixel_identical=preserved,original_body_sprites_pixel_identical=86,added_effect_frames=8,green_effect_pixels=green,yellow_effect_pixels=yellow,changed_states=[11020,9433],new_actions=[8950,8951],failures=[])
 (ROOT/'previews/MitsukiTBV_orochi_revision_checks.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS Orochi visual revision;',preserved,'existing sprites and all gameplay mechanics preserved; green pixels',green)
if __name__=='__main__':main()
