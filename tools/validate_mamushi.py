#!/usr/bin/env python3
"""Validate real Mamushi archives, state references and native MUGEN syntax."""
from pathlib import Path
import hashlib,json,re,sys
from PIL import Image
import validate_character as shared
from make_combo_preview import Sff2
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
CHAR=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'Mamushi'
shared.errors.clear();check=shared.check;field=shared.field;integer=shared.integer
shared.MUGEN11_CALLS.add('target')
for n in ['Mamushi.def','Mamushi.sff','Mamushi.snd','Mamushi.air','Mamushi.cns','Mamushi.cmd','common1.cns']:check((CHAR/n).is_file(),f'Missing {n}')
if shared.errors:raise SystemExit('\n'.join(shared.errors))
for key in ['sprite','sound','anim','cmd','cns','st','stcommon']:
    match=re.search(rf'(?im)^{key}\s*=\s*([^;\r\n]+)',(CHAR/'Mamushi.def').read_text())
    check(bool(match) and (CHAR/match[1].strip()).is_file(),f'DEF invalid {key}')
sprites=shared.parse_sff(CHAR/'Mamushi.sff');sounds=shared.parse_snd(CHAR/'Mamushi.snd')
check(len(sprites)==139,'Missing source sprites/effect records');check((1,21) in sounds,'Missing audible jutsu startup')
actions={};current=None
for line in (CHAR/'Mamushi.air').read_text().splitlines():
    match=re.match(r'(?i)\[Begin Action (\d+)\]',line)
    if match:
        current=int(match[1]);check(current not in actions,f'Duplicate AIR {current}');actions[current]=[]
    match=re.match(r'\s*(\d+)\s*,\s*(\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)',line)
    if match:
        g,n,x,y,t=map(int,match.groups());check((g,n) in sprites,f'Action {current}: missing {g},{n}');actions[current].append((g,n,t))
        check(not (g==0 and n in [14,15,28,40,64]),f'Action {current}: detached head / debug rectangle / sheet strip used as a fighter')
    box=re.match(r'\s*Clsn[12]\[\d+\]\s*=\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)',line)
    if box:
        x1,y1,x2,y2=map(int,box.groups());check(x1<=x2 and y1<=y2,f'Action {current}: inverted collision rectangle')
check(actions.get(0)==[(0,4,10),(0,5,10),(0,6,10)],'Idle contains non-idle poses')
for n in [52,5100,5110,5120,5170]:check(n in actions and all(row[2]>=0 for row in actions[n]),f'Infinite recovery action {n}')
states=set();sections=[];command_names=set();counts={}
for filename in ['Mamushi.cns','common1.cns','Mamushi.cmd']:
    path=CHAR/filename;shared.check_mugen11_calls(path);text=path.read_text()
    check(not re.search(r'(?im)^\s*type\s*=\s*(AssertInput|PrintToConsole)',text),f'Test fixture leaked into {filename}')
    current=None
    for header,body in shared.sections(text):
        sections.append((filename,header,body));match=re.match(r'(?i)\[Statedef (-?\d+)\]',header)
        if match:
            current=int(match[1]);check(current not in states,f'Duplicate state {current}');states.add(current);counts[current]=0
        elif re.match(r'(?i)\[State\s+',header):
            check(current is not None,f'Controller without state in {filename}')
            if current is not None:counts[current]+=1
            check(bool(field(body,'type')),f'Missing controller type: {header}')
            groups={int(m[1]) for line in body if (m:=re.match(r'(?i)\s*trigger([1-9]\d*)\s*=',line))}
            check(bool(groups),f'Missing numbered trigger: {header}')
            if groups:check(groups==set(range(1,max(groups)+1)),f'Skipped trigger group: {header}')
        if header.lower()=='[command]':command_names.add((field(body,'name') or '').strip('"'))
for n,count in counts.items():check(count>0,f'Empty Statedef {n}')
used=set()
for filename,header,body in sections:
    typ=(field(body,'type') or '').lower()
    for key in ['anim']+(['value'] if typ in ['changeanim','changeanim2'] else []):
        value=integer(field(body,key))
        if value is not None and value>=0:check(value in actions,f'{filename} {header}: animation {value} missing')
    for key in (['value'] if typ in ['changestate','selfstate','targetstate'] else ['stateno'] if typ in ['helper','hitoverride'] else ['p1stateno','p2stateno'] if typ in ['hitdef','reversaldef'] else []):
        value=integer(field(body,key))
        if value is not None and value>=0:check(value in states,f'{filename} {header}: state {value} missing')
    for line in body:
        used.update(re.findall(r'(?i)command\s*!?=\s*"([^"]+)"',line))
        match=re.match(r'(?i)\s*(value|hitsound|guardsound)\s*=\s*S(\d+),(\d+)\s*$',line)
        if match:check((int(match[2]),int(match[3])) in sounds,f'Missing sound {match[2]},{match[3]}')
check(used<=command_names,f'Undefined commands: {used-command_names}')
if (CHAR/'assets/sprites.json').exists():
    packed=Sff2(CHAR/'Mamushi.sff')
    for pose in json.loads((CHAR/'assets/sprites.json').read_text()):
        original=Image.open(CHAR/pose['file']).convert('RGBA');rgba=original.tobytes()
        check(hashlib.sha256(rgba).hexdigest()==pose['source_rgba_sha256'],f'Changed original pose {pose["number"]}')
        actual,axis=packed.image(pose['group'],pose['number']);a=np.array(actual);b=np.array(original);mask=b[:,:,3]>0
        check(actual.size==original.size and list(axis)==pose['axis'],f'Rescaled or moved original sprite {pose["number"]}')
        check(np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:,:,:3][mask],b[:,:,:3][mask]),f'Repainted packed original sprite {pose["number"]}')
runtime=(CHAR/'Mamushi.cns').read_text()
for n in [9500,9501,9503,9504,9505,9590]:
    block=re.search(rf'(?ims)^\[Statedef {n}\].*?(?=^\[Statedef|\Z)',runtime)
    check(bool(block) and bool(re.search(r'(?im)^type = HitOverride$',block[0])),f'Clone {n} has no own hit handling')
    check(bool(block) and 'GameTime-Var(1)>=' in block[0],f'Clone {n} has no own finite lifetime')
    check(bool(block) and 'Root,MoveType = H' not in block[0],f'Clone {n} incorrectly disappears with its original')
guard=re.search(r'(?ims)^\[Begin Action 1200\].*?(?=^\[Begin Action|\Z)',(CHAR/'Mamushi.air').read_text())
check(bool(guard) and 'Clsn1Default:' in guard[0],'Counter has no reversal box')
if shared.errors:
    print('VALIDATION FAILED');print('\n'.join('- '+e for e in shared.errors));raise SystemExit(1)
print(f'PASS: {len(sprites)} sprites; {len(sounds)} decoded nonverbal sounds; {len(actions)} AIR actions; {len(states)} states. Original art, finite recovery, references and MUGEN 1.1 expressions checked.')
