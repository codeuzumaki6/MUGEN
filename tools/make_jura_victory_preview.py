#!/usr/bin/env python3
"""Win a real round and record Jura's book pose with the engine's own audio."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,sys,tempfile,wave
import numpy as np
from scipy.signal import correlate,find_peaks,resample_poly

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
ENGINE=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/.eida-tools/ikemen-nightly').resolve()
FACE=int(os.environ.get('JURA_VICTORY_FACING','1'));assert FACE in [-1,1]
names=['JuraShinju.def','JuraShinju.sff','JuraShinju.snd','JuraShinju.air','JuraShinju.cns','JuraShinju.cmd','JuraShinju_common.cns']
runtime=hashlib.sha256(b''.join((ROOT/'JuraShinju'/n).read_bytes() for n in names)).hexdigest()
char=ENGINE/'chars/JuraVictory';dummy=ENGINE/'chars/JuraVictoryDummy'
shutil.copytree(ROOT/'JuraShinju',char,dirs_exist_ok=True)
shutil.copytree(ENGINE/'chars/kfm',dummy,dirs_exist_ok=True)
shutil.copy2(char/'JuraShinju.def',char/'JuraVictory.def')
shutil.copy2(dummy/'kfm.def',dummy/'JuraVictoryDummy.def')
def ctl(kind,when,params):
    return f'\n[State -2, Victory fixture only]\ntype={kind}\ntriggerall=!IsHelper\ntriggerall=RoundState=2\ntrigger1={when}\nignorehitpause=1\n{params}\n'
p1=ctl('VarAdd','1','v=58\nvalue=1')
p2=ctl('VarSet','NumEnemy>0','v=58\nvalue=EnemyNear,Var(58)')
for side in [1,2]:
    block=ctl('PosSet','Var(58)=1',f'x={(-18 if side==1 else 18)*FACE}\ny=0')
    direction=FACE if side==1 else -FACE
    block+=ctl('Turn',f'Var(58)=1 && Facing!={direction}','')
    block+=ctl('VelSet','Var(58)=1','x=0\ny=0')
    block+=ctl('LifeSet','Var(58)=1',f'value={1300 if side==1 else 24}')
    block+=ctl('ChangeState','Var(58)=1','value=0\nctrl=1')
    if side==1:p1+=block
    else:p2+=block
p1+=ctl('AssertInput','Var(58)=26','flag=a')
for path,fixture in [(char/'JuraShinju.cns',p1),(dummy/'kfm.cns',p2)]:
    text=path.read_text(encoding='latin-1')
    text=text.replace('[Statedef -2]','[Statedef -2]\n'+fixture,1) if '[Statedef -2]' in text else text+'\n[Statedef -2]\n'+fixture
    path.write_text(text,encoding='latin-1')

with tempfile.TemporaryDirectory(prefix='jura-victory-') as temp:
    folder=Path(temp);raw=folder/'audio.raw'
    lua="""modifyGameOption('Debug.RetryLoadOnError',false)
modifyGameOption('Config.ScreenshotFolder',FOLDER)
local trace=assert(io.open(FOLDER..'trace.tsv','w'));local images=assert(io.open(FOLDER..'frames.tsv','w'));local cues=assert(io.open(FOLDER..'cues.tsv','w'))
local clock=0;local seen=-1;local lasttm=-1;local cap={index=0,pending=nil,last=-1000}
hook.add('loop','jura_victory',function()
 if not player(1) or roundState()<2 then return end
 if roundState()==2 and var(58)==seen then return end
 seen=var(58);clock=clock+1
 local st=stateNo();local tm=time()-1;local rs=roundState();local g=spriteVar('group');local n=spriteVar('image')
 player(2);local hp=life();player(1)
 local book=numHelper(9570);local bg=-1;local bn=-1
 if book>0 and helper(9570) then bg=spriteVar('group');bn=spriteVar('image');player(1) end
 trace:write(clock..'\\t'..rs..'\\t'..st..'\\t'..tm..'\\t'..g..'\\t'..n..'\\t'..hp..'\\t'..screenPosX()..'\\t'..book..'\\t'..bg..'\\t'..bn..'\\n');trace:flush()
 if st==180 and tm==20 and tm~=lasttm then cues:write(clock..'\\n');cues:flush() end
 lasttm=tm
 if cap.pending~=nil then local png=io.open(FOLDER..string.format('Ikemen_GO%03d.png',cap.index),'rb');if png then png:close();images:write(cap.index..'\\t'..cap.pending..'\\n');images:flush();cap.index=cap.index+1;cap.pending=nil end end
 if clock>=12 and clock<420 and clock-cap.last>=4 and cap.pending==nil then screenshot();cap.pending=clock;cap.last=clock end
end)
""".replace('FOLDER',json.dumps(str(folder)+'/'))
    module=ENGINE/'external/mods/jura_victory.lua';module.write_text(lua)
    debug=ENGINE/'external/script/debug.lua';saved=debug.read_text()
    debug.write_text(saved+"\ndofile('external/mods/jura_victory.lua')\n")
    env=os.environ.copy();env.update(SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=str(raw),SDL_DISKAUDIODELAY='46',MESA_SHADER_CACHE_DISABLE='true')
    try:
        run=subprocess.run([str(ENGINE/'Ikemen_GO_Linux'),'-p1','JuraVictory','-p1.ai','0','-p2','JuraVictoryDummy','-p2.ai','0','-rounds','1','-time','300','-speed','0'],cwd=ENGINE,env=env,capture_output=True,text=True,timeout=100)
        assert run.returncode==0,run.stdout+run.stderr
        assert not re.search(r"WARNING: Jura Shinju's[^\n]*Unknown state controller parameter",run.stdout+run.stderr)
    finally:
        debug.write_text(saved);module.rename(module.with_name('-jura_victory.lua'))
    rows=[list(map(float,line.split())) for line in (folder/'trace.tsv').read_text().splitlines()]
    wins=[r for r in rows if r[1]==4 and r[2]==180]
    poses={(int(r[4]),int(r[5])) for r in wins}
    bookposes={(int(r[9]),int(r[10])) for r in wins if r[8]>0}
    assert wins and min(r[6] for r in rows)==0,'No real knockout and victory'
    assert poses=={(0,24),(0,19),(0,20)},('Victory substituted the original character body',poses)
    assert {(3,n) for n in range(4)}<=bookposes,('Book prop phases missing',bookposes)
    assert max(r[8] for r in rows)==1,'Book helper duplicated'
    assert max(r[3] for r in wins)>120,'Reading loop ended early'
    assert all(42<=r[7]<=278 for r in wins),'Winner outside viewport'
    frames=[tuple(map(int,line.split())) for line in (folder/'frames.tsv').read_text().splitlines()]
    activations=[int(line) for line in (folder/'cues.tsv').read_text().splitlines()]
    assert len(activations)==1,activations
    with wave.open(str(ROOT/'JuraShinju/assets/sound/1_44.wav')) as f:
        assert f.getframerate()==22050 and f.getnchannels()==1
        cue=resample_poly(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768,2,1)
    stereo=np.frombuffer(raw.read_bytes(),dtype='<i2').reshape(-1,2).astype(float)/32768;mono=stereo.mean(axis=1)
    cross=correlate(mono,cue,mode='valid',method='fft');energy=np.r_[0,np.cumsum(mono*mono)]
    norm=np.sqrt(np.maximum(0,energy[len(cue):]-energy[:-len(cue)])*np.sum(cue*cue));scores=np.abs(cross)/np.maximum(norm,1e-12)
    peaks,_=find_peaks(scores,height=max(.25,float(scores.max())*.8),distance=round(.12*44100))
    assert len(peaks),(float(scores.max()),'Book sound not audible in actual engine recording')
    peak=int(peaks[0]);confidence=float(scores[peak])
    start=peak/44100-(activations[0]-frames[0][1])/60;assert start>=0,start
    first=round(start*44100)
    limit=frames[0][1]+(len(stereo)-first)*60/44100-4
    frames=[p for p in frames if p[1]<=limit]
    duration=(frames[-1][1]+4-frames[0][1])/60
    last=first+round(duration*44100);assert len(frames)>40 and last<=len(stereo)
    actual=folder/'actual.wav'
    with wave.open(str(actual),'wb') as f:
        f.setparams((2,2,44100,0,'NONE','not compressed'));f.writeframes(np.clip(stereo[first:last]*32768,-32768,32767).astype('<i2').tobytes())
    lines=['ffconcat version 1.0']
    for i,(index,tick) in enumerate(frames):
        png=folder/f'Ikemen_GO{index:03d}.png';assert png.exists()
        delta=frames[i+1][1]-tick if i+1<len(frames) else 4
        lines += [f"file '{png}'",'option framerate 60',f'duration {delta/60:.9f}']
    lines += [f"file '{png}'",'option framerate 60'];concat=folder/'frames.txt';concat.write_text('\n'.join(lines)+'\n')
    caption=folder/'caption.txt';caption.write_text('VICTORIA | Cuerpo y cara de los sprites originales; libro animado en la mano')
    video=OUT/('Jura_victoria_motor.mp4' if FACE==1 else 'Jura_victoria_izquierda_motor.mp4')
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-i',str(actual),'-vf',f'fps=30,drawbox=x=0:y=680:w=1280:h=40:color=black@0.8:t=fill,drawtext=expansion=none:textfile={caption}:x=(w-tw)/2:y=690:fontsize=17:fontcolor=white','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(video)],check=True)
    target=next(r[0] for r in wins if r[3]>50)
    frame=min(frames,key=lambda p:abs(p[1]-target));shutil.copy2(folder/f'Ikemen_GO{frame[0]:03d}.png',video.with_suffix('.png'))
    report=dict(runtime_sha256=runtime,case='actual KO, original-body book victory',facing=FACE,cases=1,real_ko=True,round_state=4,victory_state=180,original_body_poses=sorted([list(p) for p in poses]),book_poses=sorted([list(p) for p in bookposes]),book_helpers=1,reading_loop_ticks=max(r[3] for r in wins),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),audio='Actual SDL stereo 44100Hz; no offline sound mix',book_sound_correlation=confidence,duration=duration,frames=len(frames),failures=[])
    (OUT/('Jura_victory_checks.json' if FACE==1 else 'Jura_victory_left_checks.json')).write_text(json.dumps(report,indent=2)+'\n')
    print('PASS real KO, original character body, four book prop phases, facing',FACE,';',round(duration,2),'seconds; actual paper sound correlation',round(confidence,3))
