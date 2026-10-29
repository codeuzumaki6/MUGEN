#!/usr/bin/env python3
"""Archive, references, two-form contracts and MUGEN 1.1 static validation."""
from pathlib import Path
import json,re,sys,struct
from PIL import Image
import validate_character as shared

ROOT=Path(__file__).resolve().parents[1];CHAR=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'BorutoKarmaJogan'
shared.errors.clear();shared.MUGEN11_CALLS.add('target');check=shared.check;field=shared.field;integer=shared.integer
for suffix in ['def','cns','cmd','air','sff','snd']:check((CHAR/f'BorutoKarmaJogan.{suffix}').is_file(),f'Missing {suffix}')
check((CHAR/'BorutoKarmaJogan_common.cns').is_file(),'Missing standalone common states')
if shared.errors:raise SystemExit('\n'.join(shared.errors))
for key in ['sprite','sound','anim','cmd','cns','st','stcommon']:
    m=re.search(rf'(?im)^{key}\s*=\s*([^;\r\n]+)',(CHAR/'BorutoKarmaJogan.def').read_text());check(m and (CHAR/m[1].strip()).is_file(),f'Broken DEF {key}')
sprite_layout={}
def parse_sff(path):
    from boruto_source import read_sff
    entries=read_sff(path)
    for k,(w,h,x,y,pix,pal) in entries.items():sprite_layout[k]=(w,h,x,y)
    return set(entries)
sprites=parse_sff(CHAR/'BorutoKarmaJogan.sff');sounds=shared.parse_snd(CHAR/'BorutoKarmaJogan.snd')
check((1,21) in sounds,'Missing audible startup')
actions={};current=None
for line in (CHAR/'BorutoKarmaJogan.air').read_text().splitlines():
    m=re.match(r'(?i)\[Begin Action (\d+)\]',line)
    if m:current=int(m[1]);check(current not in actions,f'Duplicate animation {current}');actions[current]=[]
    m=re.match(r'\s*(\d+),\s*(\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)',line)
    if m:
        g,n,x,y,t=map(int,m.groups());check((g,n) in sprites,f'Action {current}: missing sprite {g},{n}');actions[current].append((g,n,t))
        if current in [8815,8816,8817]:
            parts=[s.strip().upper() for s in line.split(',')]
            check(len(parts)>=7 and parts[6]=='A',f'Action {current}: missing standard MUGEN AIR additive transparency')
check(len(actions.get(0,[]))==3,'Invalid original idle')
for n in [5100,5110,5120]:check(n in actions and all(t>=0 for _,_,t in actions[n]),f'Infinite recovery {n}')
states=set();sections=[];counts={};commands=set();used=set()
for name in ['BorutoKarmaJogan.cns','BorutoKarmaJogan.cmd','BorutoKarmaJogan_common.cns']:
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
        if p['group'] not in list(range(32000,32008)):continue
        im=Image.open(CHAR/p['file']);check(im.getbbox() is not None,f'Empty original image {p["key"]}')


for _,header,body in sections:
    if (field(body,'type') or '').lower() in ['lifeadd','lifeset']:
        check('9700' in header and field(body,'value')=='120','Unexpected own life modification')
check(not re.search(r'(?im)^\[State[^\]\r\n]*;',(CHAR/'BorutoKarmaJogan.cns').read_text()),'Semicolon truncates controller header')
keys=json.loads((ROOT/'BorutoKarmaJogan/assets/keys.json').read_text())
check('PainNol' not in keys,'Zero source cell used')
check(sum(r['group'] in list(range(32000,32008)) for r in json.loads((ROOT/'BorutoKarmaJogan/assets/sprites.json').read_text()))==663,'Missing valid original frame')
manifest=json.loads((ROOT/'BorutoKarmaJogan/assets/sprites.json').read_text())
for p in manifest:
    if p.get('kind') not in ['body','body_with_effect','beast']:continue
    w,h,x,y=sprite_layout[p['group'],p['number']]
    check(0<=x<w and 0<=y<h,f'Body pivot outside original frame {p["key"]}')
# Original Boruto composites may only be drawn as the main body, never effects.
code_sprites={(r['group'],r['number']) for r in manifest if r.get('kind') in ['body','body_with_effect']}
for _,header,body in sections:
    if (field(body,'type') or '').lower()=='explod':
        anim=integer(field(body,'anim'))
        if anim is not None:check(not any((g,n) in code_sprites for g,n,_ in actions[anim]),f'Extra Boruto body in effect {header}')
if shared.errors:print('\n'.join(shared.errors));raise SystemExit(1)
print(f'PASS Boruto Karma Jogan: {len(sprites)} sprites, {len(sounds)} sounds, {len(actions)} actions, {len(states)} states; packed artwork and MUGEN 1.1 contracts')

if __name__=='__main__':pass
