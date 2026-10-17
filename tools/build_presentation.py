#!/usr/bin/env python3
"""Import a reviewed AI support sheet, author AIR timing and non-verbal SFX.

The sheet is preserved verbatim. Processing only splits cells, normalizes the
game's pixel height, packs a fixed origin and indexes alpha for the SFF pipeline.
No manga art or authentic voice recordings are altered here.
"""
from pathlib import Path
import math
import random
import re
import struct
import wave
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'Eida/assets'
sheet=Image.open(ASSETS/'provenance/eida_support_sheet.png').convert('RGBA')
destination=ASSETS/'eida_support';destination.mkdir(parents=True,exist_ok=True)
for index in range(6):
    x=(index%3)*sheet.width//3;y=(index//3)*sheet.height//2
    cell=sheet.crop((x,y,x+sheet.width//3,y+sheet.height//2))
    alpha=cell.getchannel('A').point(lambda v:255 if v>=128 else 0)
    box=alpha.getbbox()
    assert box and box[0]>0 and box[1]>0 and box[2]<cell.width and box[3]<cell.height
    cell.putalpha(alpha)
    figure=cell.crop(box)
    # Match the actual 68px opaque height of idle_0, not its padded canvas.
    factor=68/figure.height
    # Feet anchor the body, independently of how far the hair or hand extends.
    feet=alpha.crop((0,box[3]-round(figure.height*.12),cell.width,box[3])).getbbox()
    assert feet
    anchor=(feet[0]+feet[2])/2
    figure=figure.resize((round(figure.width*factor),68),Image.Resampling.NEAREST)
    canvas=Image.new('RGBA',(96,72))
    canvas.alpha_composite(figure,(round(48-(anchor-box[0])*factor),2))
    assert canvas.getchannel('A').getbbox()[3]==70
    canvas.save(destination/f'support_{index}.png')

# Short accents layer under the existing impacts, only on a confirmed finisher.
# These are oscillators/noise, never speech or imitation of an actor.
rate=22050;rng=random.Random(184)
for name,duration in [('daemon_finish',.28),('daemon_lift',.30),('support_gesture',.16)]:
    data=[];smooth=0
    for i in range(round(rate*duration)):
        t=i/rate;p=t/duration;smooth=.65*smooth+.35*rng.uniform(-1,1)
        if name=='daemon_finish':
            value=(.40*math.sin(2*math.pi*(120*t-110*t*t))+.38*smooth)*math.exp(-14*t)*min(1,t*500)
        elif name=='daemon_lift':
            value=(.30*math.sin(2*math.pi*(85*t+160*t*t))+.25*smooth)*math.sin(math.pi*p)*math.exp(-6*t)
        else:
            value=.26*smooth*math.sin(math.pi*p)**2
        data.append(struct.pack('<h',round(max(-.9,min(.9,value))*32767)))
    with wave.open(str(ASSETS/'sound'/f'{name}.wav'),'wb') as stream:
        stream.setparams((1,2,rate,0,'NONE','not compressed'))
        stream.writeframes(b''.join(data))

air=ROOT/'Eida/Eida.air'
text=air.read_text()
def action(number,frames,boxes=True):
    global text
    header=f'[Begin Action {number}]\n'
    if boxes:header+='Clsn2Default: 1\n Clsn2[0] = -15,-70,15,0\n'
    body=header+frames.strip()+'\n\n'
    pattern=rf'(?im)^\[Begin Action {number}\][\s\S]*?(?=^\[Begin Action |\Z)'
    if re.search(pattern,text):text=re.sub(pattern,lambda _:body,text,count=1)
    else:text+='\n'+body

# Keep every original offensive active frame and hitbox. New Eida frames are
# support gestures only; idle, walking, normals and hurt reactions stay intact.
gesture='340,0,0,0,2\n340,1,0,0,2\n340,2,0,0,2\n340,3,0,0,2\n340,4,0,0,8\n340,5,0,0,6\n0,0,0,0,4'
action(230,gesture)
action(203,gesture)
action(231,'210,3,0,0,3\n'+gesture)
action(232,'220,1,0,0,3\n220,0,0,0,3\n'+gesture)
action(1100,gesture+'\n0,0,0,0,2')
action(3000,'340,0,0,0,3\n340,1,0,0,3\n340,2,0,0,8\n340,3,0,0,3\n340,4,0,0,5\n340,5,0,0,5\n0,0,0,0,-1')

# Readable contacts: short hand exchanges, a held wind-up, then the final kick.
durations={1520:[4,4,4,6],1521:[4,3,3,3,3,3,5,5,6],
           1522:[4,5,4,6],1523:[4,4,5,6],1524:[4,5,4,6],
           1525:[4,3,3,3,3,3,5,4,5,8]}
for number,times in durations.items():
    pattern=rf'(?im)(^\[Begin Action {number}\][\s\S]*?)(?=^\[Begin Action |\Z)'
    match=re.search(pattern,text);assert match
    counter=iter(times)
    block=re.sub(r'(?m)^(1000,\d+,0,0,)\d+',lambda m:m[1]+str(next(counter)),match[1])
    assert next(counter,None) is None
    text=text[:match.start()]+block+text[match.end():]

hurt='Clsn2Default: 1\n Clsn2[0] = -12,-46,12,0\n'
action(1580,hurt+'1000,11,0,0,4\n1000,8,0,0,4',False)
action(1581,hurt+'1000,7,0,0,4\n1000,4,0,0,4',False)
action(1584,hurt+'1000,13,0,0,4\n1000,4,0,0,4',False)
action(1590,'1000,15,0,0,4\n1000,15,0,0,4',False)
action(8006,'8000,6,0,0,-1',False)
action(8007,'8000,7,0,0,-1',False)
action(8090,'8001,0,0,0,-1',False)
air.write_text(text.rstrip()+'\n')
print('Imported six support frames matching the 68px idle silhouette; authored recovery poses and three non-verbal accents')
