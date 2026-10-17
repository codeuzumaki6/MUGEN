#!/usr/bin/env python3
"""Build the reviewable command map and Daemon's finite-range assist states."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAR = ROOT / 'Eida'

# Physical Xbox mapping from the supplied mugen.cfg: X=a, Y=b, B=c, A=x,
# RB=y, RT=z, energy/pause=s. Forward/back follow the fighter's facing.
MOVES = [
    ('DaemonRapido','a','F',1000,500,0,'X: carrera y dos golpes'),
    ('DaemonCombo','a','B',1010,750,1,'X: rafaga de cinco golpes'),
    ('DaemonEleva','a','D',1020,500,2,'X: patada ascendente'),
    ('DaemonPatadas','b','F',1030,750,3,'Y: patada de empuje'),
    ('Senrigan','b','B',1200,1000,None,'Y: observacion y contraataque'),
    ('Encantamiento','b','D',1100,500,None,'Y: corazon rasante'),
    ('DaemonBarrido','c','F',1050,500,4,'B: barrido bajo'),
    ('EncantoArco','c','B',1120,750,None,'B: corazon antiaereo'),
    ('DefensaDaemon','c','D',1300,500,None,'B: defensa corta y contraataque'),
    ('ParryDaemon','y','N',1350,1000,None,'RB: parry de dos segundos'),
    ('AsaltoDoble','z','N',1060,1500,5,'RT: asalto de seis impactos'),
    ('EncantoDoble','x','D',1140,1000,None,'A con abajo: doble pulso de encanto'),
    ('PasoSenrigan','y','D',1150,750,None,'RB con abajo: retroceso y corazon de respuesta'),
    ('AperturaCombinada','z','D',1160,1500,None,'RT con abajo: encanto y entrada de Daemon'),
]


def command(name, keys, buffer=3):
    return f'[Command]\nname = "{name}"\ncommand = {keys}\ntime = 20\nbuffer.time = {buffer}\n\n'


def make_commands():
    out = '; Physical Xbox controls are documented in CONTROLES_XBOX.md.\n[Remap]\n'
    out += ''.join(f'{b} = {b}\n' for b in ('a','b','c','x','y','z','s'))+'\n'
    for name, keys in [('Omnipotencia','x'),('Carga','/s'),('Despertar','/D,s')]:
        out += command(name,keys,1 if name == 'Carga' else 3)
    for name,b,d,st,cost,mode,description in MOVES:
        out += '; '+description+'\n'
        if d in ('F','B'):
            diagonal = 'DF' if d == 'F' else 'DB'
            out += command(name,f'~D,{diagonal},{d},{b}')
            out += command(name,f'/{diagonal},{b}')
        elif d=='D':
            out += command(name,f'/D,{b}')
        else:
            out += command(name,b)
    for name,keys in [('FF','F,F'),('BB','B,B'),('recovery','a+b')]:
        out += command(name,keys)
    for b in 'abcxyzs':
        out += command(b,b,1)
    for name,keys in [('holdfwd','/$F'),('holdback','/$B'),('holdup','/$U'),('holddown','/$D'),('up','$U'),('down','$D'),('fwd','$F'),('back','$B')]:
        out += command(name,keys,1)
    out+='[Statedef -1]\n\n'
    out+='''[State -1, Omnipotencia physical Xbox A]
type = ChangeState
value = 3000
triggerall = command = "Omnipotencia"
triggerall = command != "holddown"
triggerall = power >= 3000
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1101) = 0
trigger1 = ctrl

[State -1, Despertar abajo y pausa]
type = ChangeState
value = 4000
triggerall = command = "Despertar"
triggerall = power >= 3000
triggerall = Var(40) = 0
triggerall = statetype != A
trigger1 = ctrl

'''
    for name,b,d,st,cost,mode,description in sorted(MOVES,key=lambda move:move[2]=='N'):
        out+=f'''[State -1, {description}]
type = ChangeState
ignorehitpause = 1
value = {st}
triggerall = command = "{name}"
triggerall = power >= {cost}
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
'''
        if st in (1100,1120,1140,1150,1160):out+='triggerall = NumHelper(1101) = 0\n'
        if d == 'D':
            out+='triggerall = command = "holddown"\ntriggerall = command != "holdfwd"\ntriggerall = command != "holdback"\n'
        out+='trigger1 = ctrl\n'
        if mode is not None or st in (1100,1120,1140,1160):
            out+='trigger2 = StateNo = [200,202] || StateNo = 210 || StateNo = 211 || StateNo = 220 || StateNo = 221\ntrigger2 = MoveHit\n'
        out+='\n'
    out+='''[State -1, Carga pausa]
type = ChangeState
value = 500
triggerall = command = "Carga"
triggerall = power < 3000
triggerall = statetype != A
trigger1 = ctrl

'''
    out+='''[State -1, Confirmed X into Y or B]
type = ChangeState
triggerall = StateNo = [200,202]
triggerall = MoveHit
triggerall = command != "holddown"
trigger1 = Var(27) > 0
value = IfElse(Var(27) = 1,210,220)

'''
    for b,st in [('a',200),('b',210),('c',220)]:
        out+=f'''[State -1, Normal {b}]
type = ChangeState
value = {st}
triggerall = command = "{b}"
triggerall = statetype != A
trigger1 = ctrl

'''
    for b,st in [('a',600),('b',610),('c',620)]:
        out+=f'''[State -1, Aerial {b}]
type = ChangeState
value = {st}
triggerall = command = "{b}"
triggerall = statetype = A
trigger1 = ctrl

'''
    # Eida owns the dash state; Code's legacy dash references missing effects
    # and adds long invulnerability. Ground actions may interrupt this dash.
    out=out.replace('trigger1 = ctrl\n', 'trigger1 = ctrl || StateNo = 100\n')
    out+='''[State -1, Forward dash]
type = ChangeState
value = 100
triggerall = command = "FF"
triggerall = StateType = S
triggerall = command != "holddown"
trigger1 = ctrl

'''
    (CHAR/'Eida.cmd').write_text(out.rstrip()+'\n')


def make_states():
    out='; Daemon emerges beside Eida. All offensive helpers share ID 1001.\n; They run across the stage, have hurtboxes, and expire on a miss.\n\n'
    for name,b,d,st,cost,mode,description in MOVES:
        if mode is None:continue
        out+=f'''[Statedef {st}]
type = S
movetype = A
physics = S
anim = 230
ctrl = 0
velset = 0,0
poweradd = -{cost}

[State {st}, Variant]
type = VarSet
trigger1 = Time = 0
v = 45
value = {mode}

[State {st}, Call]
type = PlaySnd
trigger1 = Time = 0
value = S0,0
channel = 0

[State {st}, Summon]
type = Helper
trigger1 = Time = 4
helpertype = Normal
name = "Daemon {name}"
ID = 1001
stateno = 1500
pos = 20,0
postype = P1
facing = 1
ownpal = 1
size.ground.back = 8
size.ground.front = 8
size.height = 49

[State {st}, Recovery]
type = ChangeState
trigger1 = Time >= {36 if mode == 5 else 28}
value = 0
ctrl = 1

'''
    out+='''[Statedef 1500]
type = S
movetype = I
physics = N
anim = 1030
ctrl = 0
velset = 0,0
sprpriority = 3

[State 1500, Store requested attack]
type = VarSet
trigger1 = Time = 0
v = 45
value = Parent,Var(45)

[State 1500, Emergence sound]
type = PlaySnd
trigger1 = Time = 0
value = S1,8
channel = 2

[State 1500, Emergence flash]
type = Explod
trigger1 = Time = 0
anim = 8420
pos = 0,-23
postype = P1
removetime = -2
scale = .27,.27
sprpriority = -1
ownpal = 1
trans = Add

[State 1500, Fade in]
type = Trans
trigger1 = 1
trans = AddAlpha
alpha = 64+Time*32,256-Time*32

[State 1500, Dash]
type = ChangeState
trigger1 = Time >= 6
value = 1501

[Statedef 1501]
type = S
movetype = I
physics = N
anim = 1510
ctrl = 0
velset = 6.8,0
sprpriority = 3

[State 1501, Whoosh]
type = PlaySnd
trigger1 = Time = 0
value = S1,0
channel = 1

[State 1501, Dash trail]
type = Explod
trigger1 = Time % 7 = 0
anim = 8410
pos = -5,-3
postype = P1
removetime = -2
scale = .22,.22
sprpriority = -1
ownpal = 1
trans = Add

[State 1501, Attack when in reach]
type = ChangeState
triggerall = P2Dist X >= -8
trigger1 = P2Dist X <= 34
value = 1520+Var(45)

[State 1501, Finite dash distance]
type = ChangeState
trigger1 = Time >= 46
trigger2 = FrontEdgeDist < -12
trigger3 = P2Dist X < -35
value = 1590

'''
    # Durations are AIR element timings. Every hit uses a different pose.
    specs=[
        (0,1520,[(2,23),(3,35)],-3.8,0,False,'MA'),
        (1,1521,[(2,18),(3,18),(5,20),(6,20),(8,36)],-4.6,-3,True,'MA'),
        (2,1522,[(2,68)],-2.5,-8,True,'MA'),
        (3,1523,[(2,48),(3,56)],-8,-3.5,True,'MA'),
        (4,1524,[(2,62)],-3,-3,True,'L'),
        (5,1525,[(2,20),(3,20),(5,22),(6,22),(8,24),(9,62)],-7,-5,True,'MA'),
    ]
    for mode,st,hits,vx,vy,fall,guard in specs:
        out+=f'''[Statedef {st}]
type = {'C' if mode==4 else 'S'}
movetype = A
physics = N
anim = {st}
ctrl = 0
velset = 0,0
sprpriority = 3

'''
        for j,(element,damage) in enumerate(hits):
            last=j==len(hits)-1
            out+=f'''[State {st}, Swing {j+1}]
type = PlaySnd
trigger1 = Animelem = {element}
value = S1,0
channel = 1

[State {st}, Hit {j+1}]
type = HitDef
trigger1 = Animelem = {element}
attr = {'C' if mode==4 else 'S'}, SA
damage = {damage},{max(2,damage//9)}
animtype = {'Up' if last and mode==2 else 'Heavy' if last else 'Light'}
guardflag = {guard}
hitflag = MAF
priority = 4,Hit
pausetime = {7 if last else 4},{10 if last else 7}
sparkno = S8400
guard.sparkno = -1
sparkxy = 0,-30
hitsound = S1,{7 if last and fall else 5+j%2}
guardsound = S1,9
ground.type = {'Low' if mode==4 else 'High'}
ground.hittime = {22 if last else 18}
ground.slidetime = 14
ground.velocity = {vx if last else -.8},{vy if last else 0}
air.hittime = 24
air.velocity = {vx if last else -.8},{vy if last else -1.5}
fall = {1 if last and fall else 0}
fall.recover = 1
fall.recovertime = 28
getpower = 0,0
givepower = 16,8
envshake.time = {7 if last else 3}
envshake.ampl = {-3 if last else -1}

'''
            if not last:
                out+=f'''[State {st}, Follow connected target {j+1}]
type = VelSet
trigger1 = AnimelemTime({element}) = [0,2]
x = 1.1

[State {st}, Stop after follow {j+1}]
type = VelSet
trigger1 = AnimelemTime({element}) = 3
x = 0

'''
        out+=f'''[State {st}, Fade out]
type = ChangeState
trigger1 = AnimTime = 0
value = 1590

'''
    out+='''[Statedef 1590]
type = S
movetype = I
physics = N
anim = 1030
ctrl = 0
velset = 0,0

[State 1590, Vanish sound]
type = PlaySnd
trigger1 = Time = 0
value = S1,8
channel = 2

[State 1590, Fade]
type = Trans
trigger1 = 1
trans = AddAlpha
alpha = 256-Time*32,Time*32

[State 1590, Gone]
type = DestroySelf
trigger1 = Time >= 8

; Aura follows Eida's existing sprite and uses additive blue color mixing.
[Statedef 8301]
type = S
movetype = I
physics = N
anim = 8300
ctrl = 0
velset = 0,0
sprpriority = -2

[State 8301, Follow]
type = BindToRoot
trigger1 = 1
pos = 0,0
time = 1
ignorehitpause = 1

[State 8301, Natural scale]
type = AngleDraw
trigger1 = 1
scale = .46,.50
ignorehitpause = 1

[State 8301, Cyan blue]
type = PalFX
trigger1 = 1
time = 1
mul = 35,140,256
ignorehitpause = 1

[State 8301, Glow]
type = Trans
trigger1 = 1
trans = AddAlpha
alpha = 170,256
ignorehitpause = 1

[State 8301, No shadow]
type = AssertSpecial
trigger1 = 1
flag = NoShadow

[State 8301, Energy hum]
type = PlaySnd
trigger1 = Time = 0
value = S1,4
channel = 6
loop = 1
volume = -160

[State 8301, Stop hum]
type = StopSnd
trigger1 = Root,Var(40) = 0
trigger2 = RoundState != 2
channel = 6

[State 8301, Off]
type = DestroySelf
trigger1 = Root,Var(40) = 0
trigger2 = RoundState != 2
ignorehitpause = 1
'''
    out+='''
; New Eida support routes. Daemon's existing body and attack states are intact.
[Statedef 1140]
type = S
movetype = A
physics = S
anim = 1100
ctrl = 0
velset = 0,0
poweradd = -1000

[State 1140, Cast sound]
type = PlaySnd
trigger1 = Time = 3
value = S1,10

[State 1140, Two distinct travelling pulses]
type = Helper
trigger1 = Time = 9
trigger2 = Time = 18
helpertype = Normal
name = "Double charm pulse"
ID = 1101
stateno = 1101
pos = 24,IfElse(Time = 9,-32,-60)
postype = P1
ownpal = 1

[State 1140, Recovery]
type = ChangeState
trigger1 = Time >= 34
value = 0
ctrl = 1

[Statedef 1150]
type = S
movetype = I
physics = N
anim = 21
ctrl = 0
velset = -4,0
poweradd = -750

[State 1150, Stop retreat]
type = VelSet
trigger1 = Time = 12
x = 0

[State 1150, Cast pose]
type = ChangeAnim
trigger1 = Time = 12
value = 1100

[State 1150, Senrigan seal]
type = Explod
trigger1 = Time = 0
anim = 8100
pos = 0,-46
postype = P1
scale = .12,.12
removetime = 12
ownpal = 1
sprpriority = 3
trans = Add

[State 1150, Sound]
type = PlaySnd
trigger1 = Time = 12
value = S1,10

[State 1150, Travelling reply]
type = Helper
trigger1 = Time = 16
helpertype = Normal
name = "Senrigan retreat reply"
ID = 1101
stateno = 1101
pos = 24,-42
postype = P1
ownpal = 1

[State 1150, Recovery]
type = ChangeState
trigger1 = Time >= 36
value = 0
ctrl = 1

[Statedef 1160]
type = S
movetype = A
physics = S
anim = 1100
ctrl = 0
velset = 0,0
poweradd = -1500

[State 1160, Existing Daemon rapid mode]
type = VarSet
trigger1 = Time = 0
v = 45
value = 0

[State 1160, Cast sound]
type = PlaySnd
trigger1 = Time = 3
value = S1,10

[State 1160, Opening heart]
type = Helper
trigger1 = Time = 9
helpertype = Normal
name = "Combined opening heart"
ID = 1101
stateno = 1101
pos = 24,-42
postype = P1
ownpal = 1

[State 1160, Daemon follows from Eida]
type = Helper
trigger1 = Time = 20
helpertype = Normal
name = "Daemon combined opening"
ID = 1001
stateno = 1500
pos = 20,0
postype = P1
ownpal = 1
size.ground.back = 8
size.ground.front = 8
size.height = 49

[State 1160, Normal followup window]
type = ChangeState
trigger1 = Time >= 34
value = 0
ctrl = 1
'''
    (CHAR/'Specials.cns').write_text(out)


if __name__=='__main__':
    make_commands()
    make_states()
    print(f'Built Eida.cmd and Specials.cns: {len(MOVES)} physical-Xbox jutsus')
