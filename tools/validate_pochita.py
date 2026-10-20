#!/usr/bin/env python3
"""Archive, reference and MUGEN 1.1 compatibility checks for Pochita."""
from pathlib import Path
import sys,re,json,struct
import validate_character as shared

CHAR=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'PochitaTrueForm'
check=shared.check;field=shared.field;integer=shared.integer
# Target(id), trigger is a native MUGEN player redirect, not an Ikemen function.
shared.MUGEN11_CALLS.add('target')
stem='PochitaTrueForm';files=[stem+x for x in ['.def','.sff','.snd','.air','.cmd','.cns']]+['common1.cns']
for name in files:check((CHAR/name).is_file(),f'Missing {name}')
if shared.errors:raise SystemExit('\n'.join(shared.errors))
for key in ['sprite','sound','anim','cmd','cns','st','stcommon']:
 m=re.search(rf'(?im)^{key}\s*=\s*([^;\r\n]+)',(CHAR/(stem+'.def')).read_text())
 check(m is not None,f'DEF missing {key}')
 if m:check((CHAR/m[1].strip()).is_file(),f'DEF missing target for {key}')
sprites=shared.parse_sff(CHAR/(stem+'.sff'));sounds=shared.parse_snd(CHAR/(stem+'.snd'))
check(len(sprites)==213,'Expected 155 body entries, 56 effects and two portraits')
check(not any(group==9800 for group,number in sprites),'Rejected giant saw must not be packed')
check(len(sounds)==14,'Expected fourteen nonverbal effects')
raw=(CHAR/(stem+'.sff')).read_bytes();sh,count,ph,pcount,ld,*_=struct.unpack_from('<IIIIIIII',raw,36);geometry={}
palettes=[]
for i in range(pcount):
 _,_,_,_,offset,size=struct.unpack_from('<HHHHII',raw,ph+i*16);palettes.append(raw[ld+offset:ld+offset+size])
for i in range(count):
 g,n,w,h,x,y,_,_,_,offset,size,pi,_=struct.unpack_from('<HHHHhhHBBIIHH',raw,sh+i*28);p=palettes[pi]
 nonred={j for j in range(256) if p[j*4+3] and not (p[j*4]>70 and p[j*4]>p[j*4+1]*1.3)}
 positions=[j%w-x for j,pixel in enumerate(raw[ld+offset:ld+offset+size]) if pixel in nonred]
 if positions:geometry[g,n]=max(positions)
actions={};current=None;idle=[];pending_attack=None;transient=False
for line in (CHAR/(stem+'.air')).read_text().splitlines():
 m=re.match(r'(?i)\[Begin Action (\d+)\]',line)
 if m:
  current=int(m[1]);check(current not in actions,f'Duplicate action {current}');actions[current]=[];pending_attack=None
 if re.match(r'(?i)\s*Clsn1:',line):transient=True
 if re.match(r'(?i)\s*Clsn1Default:',line):transient=False
 m=re.match(r'\s*(\d+),(\d+),-?\d+,-?\d+,(-?\d+)',line)
 if m:
  ref=int(m[1]),int(m[2]);check(ref in sprites,f'Action {current}: missing sprite {ref}')
  check(current is not None,'AIR frame outside action');actions[current].append(int(m[3]))
  if current==0:idle.append(ref)
  if pending_attack is not None:
   check(ref in geometry and pending_attack<=geometry[ref]+2,f'Action {current}: attack extends beyond the rendered blade of sprite {ref}')
   pending_attack=None
 m=re.match(r'\s*Clsn[12]\[\d+\]\s*=\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)',line,re.I)
 if m:
  x1,y1,x2,y2=map(int,m.groups());check(x1<x2 and y1<y2,f'Action {current}: invalid collision rectangle')
  if transient and re.match(r'(?i)\s*Clsn1\[',line):pending_attack=x2
check(idle==[(0,n) for n in range(6)],'Idle must use only its six dedicated idle poses')
for n in [52,5100,5170,5120]:check(n in actions and actions[n] and min(actions[n])>=0,f'Recovery animation {n} must finish')
states=set();sections=[];commands=set();state_controllers={}
for name in [stem+'.cns','common1.cns',stem+'.cmd']:
 path=CHAR/name;shared.check_mugen11_calls(path);text=path.read_text(encoding='latin-1')
 check('assertinput' not in text.lower(),f'{name}: test input controller leaked into delivery')
 current_state=None
 for header,body in shared.sections(text):
  sections.append((name,header,body))
  m=re.match(r'(?i)\[Statedef (-?\d+)\]',header)
  if m:
   n=int(m[1]);check(n not in states,f'Duplicate state {n}');states.add(n)
   current_state=(name,n);state_controllers[current_state]=0
  elif re.match(r'(?i)\[State\s+',header):
   check(current_state is not None,f'{name} {header}: controller outside a Statedef')
   if current_state is not None:state_controllers[current_state]+=1
   check(bool(field(body,'type')),f'{name} {header}: controller missing type')
   check(any(re.match(r'(?i)\s*trigger[1-9]\d*\s*=',line) for line in body),f'{name} {header}: controller missing numbered trigger')
   groups={int(m[1]) for line in body if (m:=re.match(r'(?i)\s*trigger([1-9]\d*)\s*=',line))}
   if groups:check(groups==set(range(1,max(groups)+1)),f'{name} {header}: nonconsecutive trigger groups can leave cancel routes ignored')
  if header.lower()=='[command]':commands.add((field(body,'name') or '').strip('"').lower())
for (name,n),count in state_controllers.items():
 check(count>0,f'{name}: Statedef {n} needs at least one state controller (MUGEN load error)')
usedcommands=set()
for name,header,body in sections:
 typ=(field(body,'type') or '').lower();n=integer(field(body,'anim'))
 if n is not None and n>=0:check(n in actions,f'{name} {header}: missing animation {n}')
 if typ in ['changeanim','changeanim2'] and typ!='changeanim2':
  n=integer(field(body,'value'))
  if n is not None and n>=0:check(n in actions,f'{name} {header}: missing animation {n}')
 for key in (['value'] if typ in ['changestate','selfstate','targetstate'] else ['p1stateno','p2stateno'] if typ in ['hitdef','reversaldef'] else []):
  n=integer(field(body,key))
  if n is not None and n>=0:check(n in states,f'{name} {header}: missing state {n}')
 for line in body:
  usedcommands.update(m.lower() for m in re.findall(r'(?i)command\s*!?=\s*"([^"]+)"',line))
  m=re.match(r'(?i)\s*(value|hitsound|guardsound)\s*=\s*S(\d+),(\d+)\s*$',line)
  if m:check((int(m[2]),int(m[3])) in sounds,f'{name} {header}: missing sound {m[2]},{m[3]}')
check(usedcommands<=commands,f'Undefined commands: {sorted(usedcommands-commands)}')
if shared.errors:
 print('VALIDATION FAILED')
 for error in shared.errors:print('-',error.replace('Eida','PochitaTrueForm'))
 raise SystemExit(1)
print(f'PASSED: {len(sprites)} SFF sprites, {len(sounds)} decoded PCM sounds, {len(actions)} AIR actions, {len(states)} states; rendered blade reach, file references and MUGEN 1.1 expressions checked')
