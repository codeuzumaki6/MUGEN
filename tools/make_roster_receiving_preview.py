#!/usr/bin/env python3
"""Build a labelled video from the actual native receiving-probe screenshots."""
from pathlib import Path
import hashlib,json,subprocess
from check_roster_receiving import CHARS,ROOT
CAP=Path('/tmp/roster-final-capture')
def stamp(t):
    c=round(t*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
def main():
    folder=CAP/'edit';folder.mkdir(exist_ok=True);lines=[];events=[];clock=0
    ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 1280','PlayResY: 720','[V4+ Styles]','Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding','Style: Default,DejaVu Sans,25,&H00FFFFFF,&H00FFFFFF,&H00202020,&H00000000,1,0,0,0,100,100,0,0,1,1,0,2,8,8,6,1','[Events]','Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
    for name in CHARS:
        part=CAP/name;rows=[tuple(map(int,l.split())) for l in (part/'frames.tsv').read_text().splitlines()]
        checks=json.loads((ROOT/'previews/roster_receiving_capture'/(name+'.json')).read_text())
        for case,result in enumerate(checks):
            assert result['hits_received']==3 and result['recovered'] and result['hurt']
            frames=[r for r in rows if r[2]==case];assert len(frames)>=18
            start=clock
            for i,(idx,frame,_,tick) in enumerate(frames):
                picture=part/f'Ikemen_GO{idx:03d}.png';assert picture.exists()
                duration=(frames[i+1][1]-frame)/60 if i+1<len(frames) else .05
                lines += [f"file '{picture}'",'option framerate 60',f'duration {duration:.9f}'];clock+=duration
            label=name+(' | Susanoo' if name=='HidariShinju' and result['form'] else '')+f" | 3 impactos recibidos | vida perdida: {result['damage']}"
            ass.append(f'Dialogue: 0,{stamp(start)},{stamp(clock)},Default,,0,0,0,,{label}')
            events.append(dict(character=name,form=result['form'],start=start,end=clock,damage=result['damage'],hits=3))
    lines += [f"file '{picture}'",'option framerate 60'];(folder/'frames.txt').write_text('\n'.join(lines)+'\n');(folder/'labels.ass').write_text('\n'.join(ass)+'\n')
    out=ROOT/'previews/Personajes_recepcion_de_golpes.mp4'
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(folder/'frames.txt'),'-vf',f"fps=30,drawbox=x=0:y=680:w=1280:h=40:color=0x090f18:t=fill,subtitles={folder/'labels.ass'}",'-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(out)],check=True)
    (ROOT/'previews/roster_receiving_demo.json').write_text(json.dumps(dict(video=str(out.relative_to(ROOT)),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),scenes=events,duration=clock,engine='Ikemen GO',fixture='Controlled native collision probe; P2 receives three real HitDef contacts. No test controller is shipped.'),indent=2)+'\n')
    print(out.name,round(clock,2),'seconds;',len(events),'native scenes')
if __name__=='__main__':main()
