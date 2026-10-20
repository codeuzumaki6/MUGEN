#!/usr/bin/env python3
"""Build Pochita's finite, hit-confirmed combat using current sprite geometry.
SX is the mechanical reference (chains, air followups, recovery), not a blind
sprite swap: no Denji dialogue, dance, allies, large first-hit multipliers or QTE.
"""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1];CHAR=ROOT/'PochitaTrueForm'
SPR=json.loads((CHAR/'assets/sprites.json').read_text());air=[]
GEOMETRY={(frame['group'],frame['number']):frame for frames in SPR.values() for frame in frames}
def action(no,group,indices,times=4,active=(),reach=70,low=False,loop=False):
    if isinstance(times,int):times=[times]*len(indices)
    body=f'[Begin Action {no}]\nClsn2Default: 1\n Clsn2[0] = -17,{-44 if low else -72},17,0\n'
    if loop:body+='Loopstart\n'
    for e,(idx,t) in enumerate(zip(indices,times),1):
        if e in active:
            visible=GEOMETRY[(group,idx)].get('attack_extent',reach)
            actualreach=min(reach,max(24,visible+1))
            body+=f'Clsn1: 1\n Clsn1[0] = 12,{-38 if low else -66},{actualreach},{-2 if low else -18}\n'
        body+=f'{group},{idx},0,0,{t}\n'
    air.append(body+'\n')
action(0,0,list(range(6)),7,loop=True);action(5,0,[1,0],[3,3]);action(6,10,[1,0],[3,3])
action(10,10,[0,1,2],[3,3,3],low=True);action(11,10,[2,3,4,5],7,low=True,loop=True);action(12,10,[2,1,0],[3,3,3],low=True)
action(20,20,list(range(7)),5,loop=True);action(21,20,list(reversed(range(7))),6,loop=True)
action(40,10,[1,2],[2,2],low=True);action(41,40,[0,1,2],[5,5,5]);action(42,40,[3,4,5],[5,5,5]);action(43,40,[3,4,5],[5,5,5]);action(44,40,[2,3,6],[4,4,4]);action(47,40,[2],[-1]);action(52,40,[6,6,3],[3,3,3],low=True)
action(100,100,list(range(7)),3,loop=True);action(105,100,[3,4,5],[4,4,4])
for n in [120,121,122,130,131,132,140,150,151,152]:action(n,10,[2],[-1],low=n in [121,131,151])
action(170,5000,[12,13,14],[6,6,-1]);action(175,5000,[14],[-1]);action(180,0,[0,1,2,3,4,5],7,loop=True);action(190,0,[0,1,2],[6,6,8]);action(195,0,[0,1,2],[6,6,8])
# Every contact has a visible active pose, with recovery frames after it.
NORMALS=[(200,200,list(range(7)),(3,4,5),70,32,False),(201,210,list(range(6)),(2,3,4),75,40,False),
(202,240,list(range(6)),(3,4,5),70,80,True),(210,230,list(range(8)),(3,4,5),75,48,False),
(211,220,list(range(7,17)),(2,3,4,5),145,42,False),(220,250,list(range(8)),(3,4,5,6),75,55,False),
(221,250,list(range(1,8)),(2,3,4,5),80,45,False),(600,600,list(range(7)),(2,3,4,5),70,50,False),
(610,610,list(range(5)),(2,3,4),75,52,False),(620,620,list(range(6)),(2,3,4,5),80,70,True),(400,10,[1,2,3,4,5],(2,3,4),55,25,False),(410,10,[2,3,4,5],(2,3),60,32,False),(420,10,[2,4,5],(2,),65,40,True)]
for no,g,idx,active,reach,damage,fall in NORMALS:action(no,g,idx,3 if no!=211 else 4,active,reach,low=no in [400,410,420])
# Nine simple directional specials, RB guard, RT rush. All are physical collisions.
MOVES=[('Desgarro','a','F',1000,250,200,list(range(7)),[3,5],(48, 58),80,False),
('CuatroBrazos','a','B',1010,350,230,list(range(8)),[3,5,7],(36, 36, 60),85,False),
('Ascenso','a','D',1020,250,240,list(range(6)),[3],(98,),80,True),
('Estocada','b','F',1030,350,220,list(range(7,17)),[3,5],(50, 76),150,False),
('Barrido','b','B',1040,250,250,list(range(1,8)),[4],(96,),82,True),
('Guillotina','b','D',1050,500,620,list(range(6)),[3],(145,),90,True),
('Embestida','c','F',1060,500,200,list(range(7)),[3,5],(65, 80),90,True),
('Carniceria','c','B',1070,750,230,list(range(17)),[3,5,7,9,12],(30, 30, 34, 34, 90),90,True),
('Rasante','c','D',1080,250,250,list(range(8)),[5],(92,),80,True),
('Asalto','z','N',1100,750,220,list(range(17)),[3,5,7,9,12],(32, 32, 36, 36, 100),145,True)]
for name,b,d,no,cost,g,idx,hits,damages,reach,fall in MOVES:action(no,g,idx,4,tuple(range(2,max(hits)+2)),reach,low=no in [1040,1080])
action(1400,10,[2,3,4,5],6,loop=True);air[-1]=air[-1].replace('Loopstart','Clsn1Default: 1\n Clsn1[0] = -25,-80,55,4\nLoopstart');action(1401,210,list(range(6)),4,(2,3,4),95)
action(500,0,list(range(6)),4,loop=True)
action(3000,100,list(range(7)),3,(4,5,6,7),85)
# Three original attack sequences instead of manga or an invented laser.
combo=[(230,i) for i in range(8)]+[(200,i) for i in range(7)]+[(240,i) for i in range(6)]+[(250,i) for i in range(8)]
air.append('[Begin Action 3001]\nClsn2Default: 1\n Clsn2[0] = -17,-72,17,0\n'+''.join(f'{g},{i},0,0,3\n' for g,i in combo)+'\n')
for n,idx,t in [(5000,0,-1),(5001,0,-1),(5002,1,-1),(5010,3,-1),(5011,3,-1),(5012,4,-1),(5020,6,-1),(5030,8,-1),(5035,8,-1),(5040,8,-1),(5050,9,-1),(5060,9,-1),(5070,9,6),(5071,10,6),(5080,12,-1),(5090,12,-1),(5100,12,6),(5110,13,-1),(5140,14,-1),(5150,14,-1),(5160,12,-1),(5170,12,4),(5200,6,8),(5210,6,8)]:action(n,5000,[idx],[t],low=n>=5070)
action(5120,5000,[13,12,10,7,0],[5,5,5,5,4],low=True)
action(5300,5000,[0,1,0],8,loop=True)
action(5500,5000,[0,1,0],8,loop=True)
(CHAR/'PochitaTrueForm.air').write_text(''.join(air).rstrip()+'\n')
# Common movement and get-hit logic from the supplied working reference. Strip
# custom animation scaling, palette swaps, voices, and source-specific helpers.
s=(ROOT/'source_material/Denji_original/DENJI_COMMON.cns').read_bytes().decode('cp932',errors='replace')
sections=re.split(r'(?im)(?=^\[)',s);clean=[];state=None
for section in sections:
    lines=[l.split(';',1)[0].strip() for l in section.splitlines()];lines=[l for l in lines if l]
    if not lines or not lines[0].startswith('['):continue
    st=re.match(r'(?i)\[Statedef\s+(-?\d+)',lines[0])
    if st:state=int(st[1])
    if state in (0,52,100,105,106,170,175,190):continue
    if not st and any(re.match(r'(?i)^type\s*=\s*(PlaySnd|AngleDraw|Helper|RemapPal)',l) for l in lines):continue
    # Source-only dust and recovery graphics do not exist in this SFF.
    if not st and any(re.match(r'(?i)^type\s*=\s*Explod',l) for l in lines) and any(re.match(r'(?i)^anim\s*=\s*\d',l) for l in lines):continue
    if not st:lines[0]=f'[State {state}, Common {len(clean)}]'
    clean.append('\n'.join(lines)+'\n\n')
common=''.join(clean)
common+='''[Statedef 52]
type = S
movetype = I
physics = S
anim = 52
ctrl = 0
velset = 0,0
[State 52, Ground]
type = PosSet
trigger1 = Time = 0
y = 0
[State 52, Recover]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

'''
common=re.sub(r'(?im)^anim = F\(60[^\n]*','anim = F60',common)
common=common.replace('[Statedef 5120]','[Statedef 5120]',1)
# Explicit get-up also works in engines where 5110's automatic transition varies.
pos=common.index('[Statedef 5120]')
common=common[:pos]+'''[State 5110, Get up while alive]
type = ChangeState
trigger1 = Alive
trigger1 = Time >= Const(data.liedown.time)
value = 5120
ctrl = 0

'''+common[pos:]
common+='''[Statedef 0]
type = S
movetype = I
physics = S
anim = 0
ctrl = 1
[State 0, Stop]
type = VelSet
trigger1 = 1
x = 0
y = 0

[Statedef 100]
type = S
movetype = I
physics = N
anim = 100
velset = 6.8,0
ctrl = 0
[State 100, Jump]
type = ChangeState
trigger1 = command = "holdup"
value = 40
[State 100, Stop]
type = ChangeState
trigger1 = Time > 5
trigger1 = command != "holdfwd"
trigger2 = Time >= 40
value = 0
ctrl = 1

[Statedef 105]
type = A
movetype = I
physics = A
anim = 105
velset = -4.2,-3.5
ctrl = 0
[State 105, Land]
type = ChangeState
trigger1 = Pos Y >= 0
trigger1 = Vel Y > 0
value = 52
ctrl = 1
'''
(CHAR/'common1.cns').write_text(common,encoding='ascii',errors='ignore')
# Human and simple situational AI inputs share the same moves; no hidden damage.
cmd='[Remap]\n'+''.join(f'{b} = {b}\n' for b in 'abcxyzs')+'\n'
def command(name,keys,buffer=3):return f'[Command]\nname = "{name}"\ncommand = {keys}\ntime = 20\nbuffer.time = {buffer}\n\n'
for b in 'abcxyzs':cmd+=command(b,b,1)
for name,keys in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D'),('holdcharge','/s'),('FF','F,F'),('BB','B,B'),('recovery','a+b')]:cmd+=command(name,keys,1 if name.startswith('hold') else 3)
for name,b,d,no,*_ in MOVES:
    if d in 'FB':
        diag='DF' if d=='F' else 'DB';cmd+=command(name,f'~D,{diag},{d},{b}')+command(name,f'/{diag},{b}')
    elif d=='D':cmd+=command(name,f'/D,{b}')
    else:cmd+=command(name,b)
cmd+='[Statedef -1]\n\n'
def change(label,no,conditions):return f'[State -1, {label}]\ntype = ChangeState\nvalue = {no}\n'+conditions+'\n'
# Lightweight CPU decisions use the same states/costs as human input.
for label,no,extra in [
 ('AI counter',1400,'triggerall = Power >= 250\ntriggerall = P2Dist X < 75\ntriggerall = P2MoveType = A\ntriggerall = Random < AILevel*3\n'),
 ('AI ultimate',3000,'triggerall = Power >= 2000\ntriggerall = P2Dist X < 160\ntriggerall = Random < AILevel*2\n'),
 ('AI reach',1030,'triggerall = Power >= 350\ntriggerall = P2Dist X = [55,75]\ntriggerall = Random < AILevel*5\n'),
 ('AI close','IfElse(Random < 333,200,IfElse(Random < 500,210,220))','triggerall = P2Dist X < 55\ntriggerall = Random < 160+AILevel*30\n'),
 ('AI approach',100,'triggerall = P2Dist X > 55\ntriggerall = Random < 60+AILevel*10\n')]:
 cmd+=change(label,no,'triggerall = AILevel > 0\ntriggerall = StateType != A\n'+extra+'trigger1 = Ctrl\n')
cmd+=change('AI air cut',600,'triggerall = AILevel > 0\ntriggerall = StateType = A\ntriggerall = P2Dist X < 90\ntriggerall = Random < 180\ntrigger1 = Ctrl\n')
cmd+=change('Xbox A Ultimate',3000,'triggerall = command = "x"\ntriggerall = Power >= 2000\ntriggerall = StateType != A\ntrigger1 = Ctrl\ntrigger2 = StateNo = 100\n')
for name,b,d,no,cost,*_ in MOVES:
    conditions=f'triggerall = command = "{name}"\ntriggerall = Power >= {cost}\ntriggerall = StateType != A\n'
    if d=='D':conditions+='triggerall = command != "holdfwd"\ntriggerall = command != "holdback"\n'
    conditions+='trigger1 = Ctrl\ntrigger2 = StateNo = 100\n'
    for j,state in enumerate([200,201,202,210,211,220,221],3):conditions+=f'trigger{j} = StateNo = {state}\ntrigger{j} = MoveHit\n'
    cmd+=change(name,no,conditions)
cmd+=change('RB Chainsaw guard',1400,'triggerall = command = "y"\ntriggerall = Power >= 250\ntriggerall = StateType != A\ntrigger1 = Ctrl\n')
cmd+=change('LB Rev motor',500,'triggerall = command = "holdcharge"\ntriggerall = Power < 3000\ntriggerall = StateType != A\ntrigger1 = Ctrl\n')
for label,no in [('FF',100),('BB',105)]:cmd+=change(label,no,f'triggerall = command = "{label}"\ntriggerall = StateType = S\ntrigger1 = Ctrl\n')
# Input buffering during hitpause requires a NEW press after entering a normal.
chains=[(200,201,'a'),(201,202,'a'),(210,211,'b'),(220,221,'c'),(600,610,'b'),(610,620,'c')]
for a,b,button in chains:cmd+=change(f'Hit confirmed {a} to {b}',b,f'triggerall = StateNo = {a}\ntriggerall = MoveHit\ntriggerall = Time > 0\ntrigger1 = Var(25) = 1\nignorehitpause = 1\n')
for b,no in [('a',200),('b',210),('c',220)]:cmd+=change('Normal '+b,no,f'triggerall = command = "{b}"\ntriggerall = command != "holddown"\ntriggerall = StateType != A\ntrigger1 = Ctrl\ntrigger2 = StateNo = 100\n')
for b,no in [('a',400),('b',410),('c',420)]:cmd+=change('Crouch '+b,no,f'triggerall = command = "{b}"\ntriggerall = command = "holddown"\ntriggerall = StateType != A\ntrigger1 = Ctrl\n')
for b,no in [('a',600),('b',610),('c',620)]:cmd+=change('Air '+b,no,f'triggerall = command = "{b}"\ntriggerall = StateType = A\ntrigger1 = Ctrl\n')
(CHAR/'PochitaTrueForm.cmd').write_text(cmd.rstrip()+'\n')
cns='''[Data]
life = 1250
power = 3000
attack = 100
defence = 110
fall.defence_up = 50
liedown.time = 55
airjuggle = 12
sparkno = -1
guard.sparkno = -1
KO.echo = 0
volume = 0
IntPersistIndex = 60
FloatPersistIndex = 40
[Size]
xscale = 1
yscale = 1
ground.back = 17
ground.front = 18
air.back = 17
air.front = 18
height = 72
attack.dist = 85
proj.attack.dist = 90
proj.doscale = 0
head.pos = 0,-65
mid.pos = 0,-38
shadowoffset = 0
draw.offset = 0,0
[Velocity]
walk.fwd = 2.5
walk.back = -2
run.fwd = 6.8,0
run.back = -4.2,-3.5
jump.neu = 0,-8.2
jump.fwd = 3.8
jump.back = -3.3
runjump.fwd = 5.5,-8.2
runjump.back = -3.5,-7
airjump.neu = 0,-8.2
airjump.fwd = 3.8
airjump.back = -3.3
[Movement]
airjump.num = 0
airjump.height = 35
yaccel = .55
stand.friction = .82
crouch.friction = .82

[Statedef -2]
[State -2, Stop rev loop outside charge]
type = StopSnd
trigger1 = StateNo != 500
channel = 6
ignorehitpause = 1
[State -2, Land out of an air attack]
type = ChangeState
triggerall = StateNo = [600,620]
trigger1 = Pos Y >= 0
trigger1 = Vel Y > 0
value = 52
ctrl = 1
'''
for no,end,anim in [(170,999,170),(175,999,175),(180,999,180),(190,20,190),(195,20,195)]:
    cns+=f'\n[Statedef {no}]\ntype = S\nmovetype = I\nphysics = S\nanim = {anim}\nctrl = 0\nvelset = 0,0\n'
    if no==190:cns+='[State 190, Intro]\ntype = AssertSpecial\ntrigger1 = Time < 20\nflag = Intro\n'
    if end<999:cns+=f'[State {no}, End]\ntype = ChangeState\ntrigger1 = Time >= {end}\nvalue = 0\nctrl = 1\n'
    else:
        # MUGEN rejects a Statedef with no controllers, even for held round-end
        # poses. Ikemen accepts it, so engine checks alone missed this failure.
        cns+=f'[State {no}, Hold round-end pose]\ntype = Null\ntrigger1 = 1\n'
def hitdef(no,element,damage,fall=False,last=True,reach=70,air=False,vy=None,guard='MA',ultimate=False):
    value=f'''[State {no}, Contact {element}]
type = HitDef
trigger1 = AnimElem = {element}
attr = {'A' if air else 'S'}, {'HA' if ultimate else 'SA' if no>=1000 else 'NA'}
damage = {damage},{max(1,damage//12) if damage else 0}
animtype = {'Heavy' if last else 'Light'}
guardflag = {guard}
hitflag = MAF
priority = 4,Hit
pausetime = {7 if last else 4},{10 if last else 7}
sparkno = 1
guard.sparkno = -1
hitsound = S1,{5 if last else 4}
guardsound = S1,6
ground.type = {'Low' if guard=='L' else 'High'}
ground.hittime = {28 if not last else 22}
ground.slidetime = 12
ground.velocity = {-3.2 if last else -.6},{vy if vy is not None else -5 if fall and last else 0}
air.hittime = 24
air.velocity = {-3.2 if last else -.6},{vy if vy is not None else -5 if last else -1.1}
fall = {int(fall and last)}
fall.recover = 1
fall.recovertime = 28
getpower = {0 if no>=1000 else 40},10
givepower = 15,5
envshake.time = {5 if last else 2}
envshake.ampl = {-2 if last else -1}
'''
    if ultimate:value+='p1stateno = 3001\np2stateno = 3010\nID = 3000\nkill = 0\n'
    return value+'\n'
for no,g,indices,active,reach,damage,fall in NORMALS:
    aerial=no in [600,610,620];cns+=f'\n[Statedef {no}]\ntype = {"A" if aerial else "S"}\nmovetype = A\nphysics = {"A" if aerial else "S"}\nanim = {no}\nctrl = 0\n'
    if not aerial:cns+='velset = 0,0\n'
    cns+=f'[State {no}, Saw]\ntype = PlaySnd\ntrigger1 = Time = 0\nvalue = S1,{1 if no in [202,211,221] else 0}\nchannel = 1\n'
    cns+=hitdef(no,active[0],damage,fall,reach=reach,air=aerial,vy=-6.0 if no==202 else None)
    cns+=f'[State {no}, Reset press]\ntype = VarSet\ntrigger1 = Time = 0\nv = 25\nvalue = 0\nignorehitpause = 1\n'
    follows={200:'a',201:'a',210:'b',220:'c',600:'b',610:'c'}
    if no in follows:cns+=f'[State {no}, Buffer press]\ntype = VarSet\ntrigger1 = Time > 0\ntrigger1 = command = "{follows[no]}"\nv = 25\nvalue = 1\nignorehitpause = 1\n'
    cns+=f'[State {no}, End]\ntype = ChangeState\ntrigger1 = AnimTime = 0\nvalue = {50 if aerial else 0}\nctrl = 1\n'
for name,b,d,no,cost,g,indices,hits,damages,reach,fall in MOVES:
    cns+=f'\n[Statedef {no}]\ntype = S\nmovetype = A\nphysics = S\nanim = {no}\nctrl = 0\nvelset = {5.5 if no in [1000,1060,1100] else 3.5 if no==1030 else 1.2 if no in [1010,1070] else 0},0\npoweradd = -{cost}\n'
    cns+=f'[State {no}, Motor]\ntype = PlaySnd\ntrigger1 = Time = 0\nvalue = S1,{3 if no in [1070,1100] else 1}\nchannel = 1\n'
    if no in [1000,1060,1100]:cns+=f'[State {no}, Stop lunge]\ntype = VelSet\ntrigger1 = Time >= {10 if no==1000 else 16}\nx = 0\n'
    for i,(element,damage) in enumerate(zip(hits,damages)):
        cns+=hitdef(no,element,damage,fall,last=i==len(hits)-1,reach=reach,air=no==1050,vy=-6.8 if no==1020 else None,guard='L' if no in [1040,1080] else 'MA')
    cns+=f'[State {no}, End]\ntype = ChangeState\ntrigger1 = AnimTime = 0\nvalue = 0\nctrl = 1\n'
    if no==1020:cns+='[State 1020, Jump after contact]\ntype = ChangeState\ntriggerall = MoveHit\ntrigger1 = command = "holdup"\nvalue = 40\n'
cns+='''
[Statedef 500]
type = S
movetype = I
physics = S
anim = 500
ctrl = 0
velset = 0,0
[State 500, Rev]
type = PlaySnd
trigger1 = Time = 0
value = S1,3
channel = 6
loop = 1
volume = -160
[State 500, Power]
type = PowerAdd
trigger1 = 1
value = 18
[State 500, Stop]
type = ChangeState
trigger1 = command != "holdcharge"
trigger2 = Power >= 3000
value = 0
ctrl = 1

[Statedef 1400]
type = S
movetype = I
physics = S
anim = 1400
ctrl = 0
velset = 0,0
poweradd = -250
[State 1400, Guard motor]
type = PlaySnd
trigger1 = Time = 0
value = S1,1
[State 1400, Catch physical attack]
type = ReversalDef
trigger1 = Time = [4,28]
reversal.attr = SCA, NA, SA, HA
pausetime = 5,8
sparkno = -1
hitsound = S1,5
p1stateno = 1401
p2stateno = 1410
[State 1400, End]
type = ChangeState
trigger1 = Time >= 40
value = 0
ctrl = 1
[Statedef 1401]
type = S
movetype = A
physics = S
anim = 1401
ctrl = 0
velset = 0,0
'''
cns+=hitdef(1401,2,115,True)
cns+='''[State 1401, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1
[Statedef 1410]
type = S
movetype = H
physics = S
ctrl = 0
velset = 0,0
[State 1410, Own hurt pose]
type = ChangeAnim
trigger1 = Time = 0
value = 5000
[State 1410, Release]
type = SelfState
trigger1 = Time >= 14
value = 0
ctrl = 1

[Statedef 3000]
type = S
movetype = A
physics = N
anim = 3000
ctrl = 0
velset = 0,0
poweradd = -2000
[State 3000, Tell]
type = PlaySnd
trigger1 = Time = 0
value = S1,3
[State 3000, Rush]
type = VelSet
trigger1 = Time = 8
x = 7
[State 3000, Stop]
type = VelSet
trigger1 = Time = 26
x = 0
'''
cns+=hitdef(3000,4,0,False,ultimate=True)
cns+='''[State 3000, Recover on miss]
type = ChangeState
trigger1 = Time >= 52
value = 0
ctrl = 1

[Statedef 3001]
type = S
movetype = A
physics = N
anim = 3001
ctrl = 0
velset = 0,0
[State 3001, Confirmed protection]
type = NotHitBy
trigger1 = 1
value = SCA
time = 1
[State 3001, Red scene]
type = BGPalFX
trigger1 = Time = 0
time = 82
mul = 140,70,70
[State 3001, Bind close]
type = TargetBind
trigger1 = Time < 76
ID = 3000
pos = 52,0
[State 3001, Motor]
type = PlaySnd
trigger1 = Time = 0
trigger2 = Time = 24
trigger3 = Time = 48
value = S1,3
channel = 1
'''
for time,damage in [(10,35),(22,35),(34,40),(46,40),(58,50),(74,150)]:
    cns+=f'''[State 3001, Confirmed cut {time}]
type = TargetLifeAdd
trigger1 = Time = {time}
trigger1 = NumTarget(3000) > 0
ID = 3000
value = -{damage}
kill = {1 if time==74 else 0}
absolute = 1
[State 3001, Cut sound {time}]
type = PlaySnd
trigger1 = Time = {time}
value = S1,5
channel = 2
[State 3001, Cut shake {time}]
type = EnvShake
trigger1 = Time = {time}
time = {9 if time==74 else 3}
freq = 90
ampl = {-4 if time==74 else -1}
'''
cns+='''[State 3001, Release]
type = TargetState
trigger1 = Time = 78
ID = 3000
value = 3011
[State 3001, End]
type = ChangeState
trigger1 = Time >= 96
value = 0
ctrl = 1
[Statedef 3010]
type = S
movetype = H
physics = N
ctrl = 0
velset = 0,0
[State 3010, Hurt]
type = ChangeAnim
trigger1 = Time = 0
value = 5000
[State 3010, Emergency release]
type = SelfState
trigger1 = Time >= 140
trigger2 = NumEnemy > 0
trigger2 = EnemyNear,StateNo != 3000
trigger2 = EnemyNear,StateNo != 3001
value = 0
ctrl = 1
[Statedef 3011]
type = A
movetype = H
physics = N
ctrl = 0
velset = -5,-6
[State 3011, Fall]
type = SelfState
trigger1 = 1
value = 5050
ctrl = 0
'''
start=cns.index('[Statedef 1050]');end=cns.index('[Statedef 1060]',start)
block=cns[start:end].replace('type = S','type = A',1).replace('physics = S','physics = A',1).replace('velset = 0,0','velset = 3.8,-5.4',1)
block=block.replace('[State 1050, End]','[State 1050, Land]\ntype = ChangeState\ntrigger1 = Pos Y >= 0\ntrigger1 = Vel Y > 0\nvalue = 52\nctrl = 1\n[State 1050, End]').replace('value = 0\nctrl = 1','value = 50\nctrl = 1')
cns=cns[:start]+block+cns[end:]
# CPU chains wait for a real hit, and use the same buffer as the player.
for state in [200,201,210,220,600,610]:
 marker=f'[State {state}, End]'
 at=cns.index(marker)
 cns=cns[:at]+f'[State {state}, CPU confirms chain]\ntype = VarSet\ntrigger1 = AILevel > 0\ntrigger1 = Time > 0\ntrigger1 = MoveHit\nv = 25\nvalue = 1\nignorehitpause = 1\n'+cns[at:]
(CHAR/'PochitaTrueForm.cns').write_text(cns)
(CHAR/'PochitaTrueForm.def').write_text('''[Info]
name = "Pochita True Form"
displayname = "Pochita"
mugenversion = 1.1
author = "Pochita project; AI visual redesign; gameplay reference STAND USER X"
[Files]
sprite = PochitaTrueForm.sff
sound = PochitaTrueForm.snd
anim = PochitaTrueForm.air
cmd = PochitaTrueForm.cmd
cns = PochitaTrueForm.cns
st = PochitaTrueForm.cns
stcommon = common1.cns
[Arcade]
intro.storyboard =
ending.storyboard =
''')
print('Built geometry-aware AIR, Xbox commands and finite Pochita combat states')

from build_pochita_climaxes import apply_climax_runtime
apply_climax_runtime(CHAR)
from build_pochita_flow import apply_flow_runtime
apply_flow_runtime(CHAR)

from build_pochita_special_startup import apply_startup_runtime
apply_startup_runtime(CHAR)

from build_pochita_spectacle import apply_spectacle_runtime
apply_spectacle_runtime(CHAR)
