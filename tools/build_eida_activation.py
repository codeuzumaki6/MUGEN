#!/usr/bin/env python3
"""Add an audible, finite startup to every metered jutsu, using the Code SE."""
from pathlib import Path
import hashlib,json,re,shutil,wave
import numpy as np
from build_moveset import MOVES
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'Eida'
BEGIN='; EIDA ACTIVATION BEGIN';END='; EIDA ACTIVATION END'

def remove_activation(text):
    return re.sub(r'(?ms)^; EIDA ACTIVATION BEGIN.*?^; EIDA ACTIVATION END\n?','',text)

def install():
    # Identical to Pochita's reviewed nonverbal activation sample. The source
    # is Code's supplied 950,2 effect, not an actor or audio lifted from video.
    source=ROOT/'PochitaTrueForm/assets/sound/special_activation.wav'
    destination=CHAR/'assets/sound/special_activation.wav';shutil.copyfile(source,destination)
    with wave.open(str(destination)) as f:
        assert (f.getnchannels(),f.getsampwidth(),f.getframerate())==(1,2,22050)
        samples=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768
    (CHAR/'assets/polish/activation_sound.json').write_text(json.dumps(dict(group=1,number=21,file=destination.name,source='User-supplied Code_FUNCIONAL, SND 950,2; same processed sample as Pochita',voice=False,sha256=hashlib.sha256(destination.read_bytes()).hexdigest(),rms=float(np.sqrt(np.mean(samples*samples))),peak=float(np.max(np.abs(samples)))),indent=2)+'\n')
    for filename in ['Eida.cns','Specials.cns']:
        path=CHAR/filename;text=remove_activation(path.read_text())
        for move in MOVES:
            state=move[3]
            pattern=rf'(?ims)^\[Statedef {state}\].*?(?=^\[Statedef|\Z)'
            match=re.search(pattern,text)
            if not match:continue
            block=match[0];first=re.search(r'(?m)^(?:; EIDA POLISH BEGIN|\[State )',block);assert first
            controllers=f'''[State {state}, Distinct special activation sound]
type = PlaySnd
trigger1 = Time = 0
value = S1,21
channel = 4
volumescale = 100
persistent = 0
ignorehitpause = 1
[State {state}, Brief special focus]
type = SuperPause
trigger1 = Time = 0
time = IfElse(PrevStateNo >= 200 && PrevStateNo <= 221,6,12)
movetime = 0
anim = -1
sound = -1
darken = 1
unhittable = 0
p2defmul = 1
poweradd = 0
persistent = 0
ignorehitpause = 1
[State {state}, Activation flash]
type = Explod
trigger1 = Time = 0
anim = 8510
ID = 8560
postype = P1
pos = 14,-48
scale = .7,.4
bindtime = 1
removetime = 12
sprpriority = 6
ownpal = 1
trans = AddAlpha
alpha = 230,256
supermovetime = 12
pausemovetime = 12
removeongethit = 1
persistent = 0
ignorehitpause = 1
[State {state}, Senrigan activation crescent]
type = Explod
trigger1 = Time = 0
anim = 8520
ID = 8561
postype = P1
pos = 4,-56
scale = .35,.35
bindtime = 1
removetime = 12
sprpriority = 7
ownpal = 1
trans = AddAlpha
alpha = 200,256
supermovetime = 12
pausemovetime = 12
removeongethit = 1
persistent = 0
ignorehitpause = 1
'''
            at=first.start();text=text[:match.start()]+block[:at]+BEGIN+'\n'+controllers+END+'\n'+block[at:]+text[match.end():]
        path.write_text(text)
    # Make Senrigan readable as a waiting counter rather than an idle eye icon.
    air=CHAR/'Eida.air';text=air.read_text()
    action='[Begin Action 1200]\nClsn1Default: 1\n Clsn1[0] = -16,-70,30,0\nClsn2Default: 1\n Clsn2[0] = -15,-70,15,0\n340,0,0,0,3\n340,1,0,0,3\n340,2,0,0,-1\n\n'
    text,count=re.subn(r'(?ims)^\[Begin Action 1200\].*?(?=^\[Begin Action|\Z)',lambda _:action,text,count=1);assert count
    air.write_text(text)
    path=CHAR/'Eida.cns';text=path.read_text()
    match=re.search(r'(?ims)^\[Statedef 1200\].*?(?=^\[Statedef|\Z)',text);block=match[0]
    block=block.replace('pos = 0,-38','pos = 4,-56').replace('sprpriority = -2','sprpriority = 5')
    # Counter is live as soon as the eye appears, including an overlapping
    # incoming strike at startup; never advertise an inactive observation pose.
    block=block.replace('trigger1 = Time = [8,48]','trigger1 = Time = [0,48]')
    block=block.replace('trigger1 = Time < 55','trigger1 = Time <= 48')
    for old,new in [('.12,.12','.07,.07'),('.14,.14','.08,.08'),('.16,.16','.085,.085')]:block=block.replace('scale = '+old,'scale = '+new)
    close='''[State 1200, Observation window closes without a hit]
type = PlaySnd
trigger1 = Time = 49
value = S1,18
channel = 3
volumescale = 55
[State 1200, Lower the hand after observation closes]
type = ChangeAnim
trigger1 = Time = 49
value = 0
'''
    # Insert outside the activation block so repeated builds remain flat.
    block=block.replace('[State 1200, End]',BEGIN+'\n'+close+END+'\n[State 1200, End]')
    text=text[:match.start()]+block+text[match.end():]
    match=re.search(r'(?ims)^\[Statedef 1201\].*?(?=^\[Statedef|\Z)',text);block=match[0]
    first=re.search(r'(?m)^\[State ',block).start()
    cue='''[State 1201, Confirmed observation cue]
type = PlaySnd
trigger1 = Time = 0
value = S1,19
channel = 3
volumescale = 75
'''
    text=text[:match.start()]+block[:first]+BEGIN+'\n'+cue+END+'\n'+block[first:]+text[match.end():]
    match=re.search(r'(?ims)^\[Statedef -2\].*?(?=^\[Statedef|\Z)',text);block=match[0]
    at=re.search(r'(?m)^(?:; EIDA POLISH BEGIN|\[State )',block).start()
    clear=''.join(f'[State -2, Clear observation icon {i}]\ntype = RemoveExplod\ntriggerall = IsHelper = 0\ntrigger1 = StateNo != 1200\ntrigger2 = StateNo = 1200\ntrigger2 = Time > 48\nID = {i}\nignorehitpause = 1\n' for i in [8100,8101,8102])
    text=text[:match.start()]+block[:at]+BEGIN+'\n'+clear+END+'\n'+block[at:]+text[match.end():];path.write_text(text)
    print('Installed 14 audible special startups and readable Senrigan counter')

if __name__=='__main__':install()
