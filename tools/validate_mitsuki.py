#!/usr/bin/env python3
"""Archive, references, two-form contracts and MUGEN 1.1 static validation."""
from pathlib import Path
import json,re,sys,struct,io,wave
from PIL import Image
import validate_character as shared

ROOT=Path(__file__).resolve().parents[1];CHAR=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'MitsukiTBV'
shared.errors.clear();shared.MUGEN11_CALLS.add('target');check=shared.check;field=shared.field;integer=shared.integer
for suffix in ['def','cns','cmd','air','sff','snd']:check((CHAR/f'MitsukiTBV.{suffix}').is_file(),f'Missing {suffix}')
check((CHAR/'MitsukiTBV_common.cns').is_file(),'Missing standalone common states')
if shared.errors:raise SystemExit('\n'.join(shared.errors))
for key in ['sprite','sound','anim','cmd','cns','st','stcommon']:
    m=re.search(rf'(?im)^{key}\s*=\s*([^;\r\n]+)',(CHAR/'MitsukiTBV.def').read_text());check(m and (CHAR/m[1].strip()).is_file(),f'Broken DEF {key}')
def parse_sff(path):
    data=path.read_bytes();check(data[:16]==b'ElecbyteSpr\0'+bytes((0,1,0,2)),'Invalid SFF v2 header')
    sh,count,ph,pc,lo,ls,to,ts=struct.unpack_from('<8I',data,36)
    check(sh+count*28<=len(data) and ph+pc*16<=len(data) and lo+ls<=len(data) and to+ts<=len(data),'SFF block outside file')
    for i in range(pc):
        g,n,colors,link,off,size=struct.unpack_from('<4H2I',data,ph+i*16)
        check(colors==256 and size==1024 and off+size<=ls,'Invalid indexed palette')
    sprites=set()
    for i in range(count):
        g,n,w,h,x,y,link,fmt,depth,off,size,pal,flags=struct.unpack_from('<4H2hH2B2I2H',data,sh+i*28)
        check(w>0 and h>0 and fmt==0 and depth==8 and flags==0 and size==w*h and off+size<=ls and pal<pc,f'Invalid sprite {g},{n}')
        check((g,n) not in sprites,f'Duplicate sprite {g},{n}');sprites.add((g,n))
    return sprites
sprites=parse_sff(CHAR/'MitsukiTBV.sff');sounds=set();data=(CHAR/'MitsukiTBV.snd').read_bytes();count,off=struct.unpack_from('<II',data,16)
for _ in range(count):
    nxt,size,g,n=struct.unpack_from('<IIII',data,off);check((g,n) not in sounds,'Duplicate sound');sounds.add((g,n))
    with wave.open(io.BytesIO(data[off+16:off+16+size])) as w:check(w.getnchannels() in [1,2] and w.getsampwidth()==2 and w.getnframes()>0,'Invalid PCM WAV')
    off=nxt
check((1,21) in sounds,'Missing audible startup')
for g,count in [(0,67),(1,19)]:
    for n in range(count):check((g,n) in sprites,f'Missing original body pose {g},{n}')
actions={};current=None
for line in (CHAR/'MitsukiTBV.air').read_text().splitlines():
    m=re.match(r'(?i)\[Begin Action (\d+)\]',line)
    if m:current=int(m[1]);check(current not in actions,f'Duplicate animation {current}');actions[current]=[]
    m=re.match(r'\s*(\d+),\s*(\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)',line)
    if m:
        g,n,x,y,t=map(int,m.groups());check((g,n) in sprites,f'Action {current}: missing sprite {g},{n}');actions[current].append((g,n,t))
check(actions.get(0)==[(0,0,10),(0,1,10),(0,2,10)],'Attack poses entered idle')
check(actions.get(10000)==[(1,0,10),(1,1,10),(1,2,10)],'Sage idle uses wrong art')
for n in [5100,5110,5120]:check(n in actions and all(t>=0 for _,_,t in actions[n]),f'Infinite recovery {n}')
states=set();sections=[];counts={};commands=set();used=set()
for name in ['MitsukiTBV.cns','MitsukiTBV.cmd','MitsukiTBV_common.cns']:
    path=CHAR/name;shared.check_mugen11_calls(path);text=path.read_text();current=None
    check(not re.search(r'(?im)^type\s*=\s*(AssertInput|PrintToConsole)',text),'Fixture leaked into download')
    for header,body in shared.sections(text):
        sections.append((name,header,body));m=re.match(r'(?i)\[Statedef (-?\d+)\]',header)
        if m:current=int(m[1]);check(current not in states,f'Duplicate state {current}');states.add(current);counts[current]=0
        elif re.match(r'(?i)\[State\s+',header):
            check(current is not None,'Controller outside state');counts[current]=counts.get(current,0)+1
            check(field(body,'type'),'Missing controller type')
            groups={int(m[1]) for line in body if (m:=re.match(r'(?i)\s*trigger([1-9]\d*)\s*=',line))}
            check(groups and groups==set(range(1,max(groups)+1)),f'Skipped/missing trigger {header}')
        if header.lower()=='[command]':commands.add((field(body,'name') or '').strip('"'))
for n,count in counts.items():check(count>0,f'Empty state {n}')
for n in [120,130,131,132,150,151,152,153,154,155,5000,5010,5020,5030,5050,5100,5110,5120,5150]:check(n in states,f'Missing native movement/guard/recovery state {n}')
for name,header,body in sections:
    typ=(field(body,'type') or '').lower()
    for key in ['anim','projanim','projhitanim','projremanim']+(['value'] if typ in ['changeanim','changeanim2'] else []):
        val=integer(field(body,key))
        if val is not None and val>=0:check(val in actions,f'{name} {header}: missing animation {val}')
    for key in ['value'] if typ in ['changestate','selfstate','targetstate'] else ['stateno'] if typ in ['helper','hitoverride'] else ['p1stateno','p2stateno'] if typ in ['projectile','hitdef','reversaldef'] else []:
        val=integer(field(body,key))
        if val is not None and val>=0:check(val in states,f'Missing state {val}')
    for line in body:
        used.update(re.findall(r'(?i)command\s*!?=\s*"([^"]+)"',line))
        m=re.match(r'(?i)\s*(value|hitsound|guardsound)\s*=\s*S(\d+),(\d+)\s*$',line)
        if m:check((int(m[2]),int(m[3])) in sounds,f'Missing SND {m[2]},{m[3]}')
check(used<=commands,f'Undefined command {used-commands}')
if (CHAR/'assets/sprites.json').exists():
    poses=json.loads((CHAR/'assets/sprites.json').read_text())
    for p in poses:
        if p['group'] not in [0,1]:continue
        im=Image.open(CHAR/p['file']);check(im.getchannel('A').getextrema()==(0,255),f'Incorrect body transparency {p["number"]}')
check(not any(g==8680 and n>=4 for g,n in sprites),'Donor body remains in substitution effects')
check(actions.get(8680)==[(8680,n,2) for n in range(4)],'Substitution includes non-effect donor frames')
for g,length in [(8930,230),(8931,280),(8932,108)]:
    check(all((g,n) in sprites for n in range(8)),f'Missing continuous Raiton bank {g}')
for form in [0,1]:
    motions=[tuple(actions[n+form*10000]) for n in [1040,1400,1410]]
    check(len(set(motions))==3,'Kick, slide and uppercut share a body sequence')
if shared.errors:print('\n'.join(shared.errors));raise SystemExit(1)
print(f'PASS Mitsuki TBV: {len(sprites)} sprites, {len(sounds)} sounds, {len(actions)} actions, {len(states)} states; packed artwork and MUGEN 1.1 contracts')

if __name__=='__main__':pass
