; Physical Xbox controls are documented in CONTROLES_XBOX.md.
[Remap]
a = a
b = b
c = c
x = x
y = y
z = z
s = s

[Command]
name = "Omnipotencia"
command = x
time = 20
buffer.time = 3

[Command]
name = "Carga"
command = /s
time = 20
buffer.time = 1

[Command]
name = "Despertar"
command = /D,s
time = 20
buffer.time = 3

; X: carrera y dos golpes
[Command]
name = "DaemonRapido"
command = ~D,DF,F,a
time = 20
buffer.time = 3

[Command]
name = "DaemonRapido"
command = /DF,a
time = 20
buffer.time = 3

; X: rafaga de cinco golpes
[Command]
name = "DaemonCombo"
command = ~D,DB,B,a
time = 20
buffer.time = 3

[Command]
name = "DaemonCombo"
command = /DB,a
time = 20
buffer.time = 3

; X: patada ascendente
[Command]
name = "DaemonEleva"
command = /D,a
time = 20
buffer.time = 3

; Y: patada de empuje
[Command]
name = "DaemonPatadas"
command = ~D,DF,F,b
time = 20
buffer.time = 3

[Command]
name = "DaemonPatadas"
command = /DF,b
time = 20
buffer.time = 3

; Y: observacion y contraataque
[Command]
name = "Senrigan"
command = ~D,DB,B,b
time = 20
buffer.time = 3

[Command]
name = "Senrigan"
command = /DB,b
time = 20
buffer.time = 3

; Y: corazon rasante
[Command]
name = "Encantamiento"
command = /D,b
time = 20
buffer.time = 3

; B: barrido bajo
[Command]
name = "DaemonBarrido"
command = ~D,DF,F,c
time = 20
buffer.time = 3

[Command]
name = "DaemonBarrido"
command = /DF,c
time = 20
buffer.time = 3

; B: corazon antiaereo
[Command]
name = "EncantoArco"
command = ~D,DB,B,c
time = 20
buffer.time = 3

[Command]
name = "EncantoArco"
command = /DB,c
time = 20
buffer.time = 3

; B: defensa corta y contraataque
[Command]
name = "DefensaDaemon"
command = /D,c
time = 20
buffer.time = 3

; RB: parry de dos segundos
[Command]
name = "ParryDaemon"
command = y
time = 20
buffer.time = 3

; RT: asalto de seis impactos
[Command]
name = "AsaltoDoble"
command = z
time = 20
buffer.time = 3

; A con abajo: doble pulso de encanto
[Command]
name = "EncantoDoble"
command = /D,x
time = 20
buffer.time = 3

; RB con abajo: retroceso y corazon de respuesta
[Command]
name = "PasoSenrigan"
command = /D,y
time = 20
buffer.time = 3

; RT con abajo: encanto y entrada de Daemon
[Command]
name = "AperturaCombinada"
command = /D,z
time = 20
buffer.time = 3

[Command]
name = "FF"
command = F,F
time = 20
buffer.time = 3

[Command]
name = "BB"
command = B,B
time = 20
buffer.time = 3

[Command]
name = "recovery"
command = a+b
time = 20
buffer.time = 3

[Command]
name = "a"
command = a
time = 20
buffer.time = 1

[Command]
name = "b"
command = b
time = 20
buffer.time = 1

[Command]
name = "c"
command = c
time = 20
buffer.time = 1

[Command]
name = "x"
command = x
time = 20
buffer.time = 1

[Command]
name = "y"
command = y
time = 20
buffer.time = 1

[Command]
name = "z"
command = z
time = 20
buffer.time = 1

[Command]
name = "s"
command = s
time = 20
buffer.time = 1

[Command]
name = "holdfwd"
command = /$F
time = 20
buffer.time = 1

[Command]
name = "holdback"
command = /$B
time = 20
buffer.time = 1

[Command]
name = "holdup"
command = /$U
time = 20
buffer.time = 1

[Command]
name = "holddown"
command = /$D
time = 20
buffer.time = 1

[Command]
name = "up"
command = $U
time = 20
buffer.time = 1

[Command]
name = "down"
command = $D
time = 20
buffer.time = 1

[Command]
name = "fwd"
command = $F
time = 20
buffer.time = 1

[Command]
name = "back"
command = $B
time = 20
buffer.time = 1

[Statedef -1]

[State -1, Omnipotencia physical Xbox A]
type = ChangeState
value = 3000
triggerall = command = "Omnipotencia"
triggerall = command != "holddown"
triggerall = power >= 3000
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1101) = 0
trigger1 = ctrl || StateNo = 100

[State -1, Despertar abajo y pausa]
type = ChangeState
value = 4000
triggerall = command = "Despertar"
triggerall = power >= 3000
triggerall = Var(40) = 0
triggerall = statetype != A
trigger1 = ctrl || StateNo = 100

[State -1, X: carrera y dos golpes]
type = ChangeState
ignorehitpause = 1
value = 1000
triggerall = command = "DaemonRapido"
triggerall = power >= 500
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, X: rafaga de cinco golpes]
type = ChangeState
ignorehitpause = 1
value = 1010
triggerall = command = "DaemonCombo"
triggerall = power >= 750
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, X: patada ascendente]
type = ChangeState
ignorehitpause = 1
value = 1020
triggerall = command = "DaemonEleva"
triggerall = power >= 500
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
triggerall = command = "holddown"
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, Y: patada de empuje]
type = ChangeState
ignorehitpause = 1
value = 1030
triggerall = command = "DaemonPatadas"
triggerall = power >= 750
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, Y: observacion y contraataque]
type = ChangeState
ignorehitpause = 1
value = 1200
triggerall = command = "Senrigan"
triggerall = power >= 1000
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
trigger1 = ctrl || StateNo = 100

[State -1, Y: corazon rasante]
type = ChangeState
ignorehitpause = 1
value = 1100
triggerall = command = "Encantamiento"
triggerall = power >= 500
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
triggerall = NumHelper(1101) = 0
triggerall = command = "holddown"
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, B: barrido bajo]
type = ChangeState
ignorehitpause = 1
value = 1050
triggerall = command = "DaemonBarrido"
triggerall = power >= 500
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, B: corazon antiaereo]
type = ChangeState
ignorehitpause = 1
value = 1120
triggerall = command = "EncantoArco"
triggerall = power >= 750
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
triggerall = NumHelper(1101) = 0
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, B: defensa corta y contraataque]
type = ChangeState
ignorehitpause = 1
value = 1300
triggerall = command = "DefensaDaemon"
triggerall = power >= 500
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
triggerall = command = "holddown"
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = ctrl || StateNo = 100

[State -1, A con abajo: doble pulso de encanto]
type = ChangeState
ignorehitpause = 1
value = 1140
triggerall = command = "EncantoDoble"
triggerall = power >= 1000
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
triggerall = NumHelper(1101) = 0
triggerall = command = "holddown"
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, RB con abajo: retroceso y corazon de respuesta]
type = ChangeState
ignorehitpause = 1
value = 1150
triggerall = command = "PasoSenrigan"
triggerall = power >= 750
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
triggerall = NumHelper(1101) = 0
triggerall = command = "holddown"
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = ctrl || StateNo = 100

[State -1, RT con abajo: encanto y entrada de Daemon]
type = ChangeState
ignorehitpause = 1
value = 1160
triggerall = command = "AperturaCombinada"
triggerall = power >= 1500
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
triggerall = NumHelper(1101) = 0
triggerall = command = "holddown"
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, RB: parry de dos segundos]
type = ChangeState
ignorehitpause = 1
value = 1350
triggerall = command = "ParryDaemon"
triggerall = power >= 1000
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
trigger1 = ctrl || StateNo = 100

[State -1, RT: asalto de seis impactos]
type = ChangeState
ignorehitpause = 1
value = 1060
triggerall = command = "AsaltoDoble"
triggerall = power >= 1500
triggerall = statetype != A
triggerall = NumHelper(1001) = 0
triggerall = NumHelper(1351) = 0
triggerall = NumHelper(1301) = 0
trigger1 = ctrl || StateNo = 100
trigger2 = StateNo = 200
trigger2 = MoveHit
trigger3 = StateNo = 201
trigger3 = MoveHit
trigger4 = StateNo = 202
trigger4 = MoveHit
trigger5 = StateNo = 210
trigger5 = MoveHit
trigger6 = StateNo = 211
trigger6 = MoveHit
trigger7 = StateNo = 220
trigger7 = MoveHit
trigger8 = StateNo = 221
trigger8 = MoveHit

[State -1, Carga pausa]
type = ChangeState
value = 500
triggerall = command = "Carga"
triggerall = power < 3000
triggerall = statetype != A
trigger1 = ctrl || StateNo = 100

[State -1, Confirmed X into Y or B]
type = ChangeState
triggerall = StateNo = [200,202]
triggerall = MoveHit
triggerall = command != "holddown"
trigger1 = Var(27) > 0
value = IfElse(Var(27) = 1,210,220)

[State -1, Normal a]
type = ChangeState
value = 200
triggerall = command = "a"
triggerall = statetype != A
trigger1 = ctrl || StateNo = 100

[State -1, Normal b]
type = ChangeState
value = 210
triggerall = command = "b"
triggerall = statetype != A
trigger1 = ctrl || StateNo = 100

[State -1, Normal c]
type = ChangeState
value = 220
triggerall = command = "c"
triggerall = statetype != A
trigger1 = ctrl || StateNo = 100

[State -1, Aerial a]
type = ChangeState
value = 600
triggerall = command = "a"
triggerall = statetype = A
trigger1 = ctrl || StateNo = 100

[State -1, Aerial b]
type = ChangeState
value = 610
triggerall = command = "b"
triggerall = statetype = A
trigger1 = ctrl || StateNo = 100

[State -1, Aerial c]
type = ChangeState
value = 620
triggerall = command = "c"
triggerall = statetype = A
trigger1 = ctrl || StateNo = 100

[State -1, Forward dash]
type = ChangeState
value = 100
triggerall = command = "FF"
triggerall = StateType = S
triggerall = command != "holddown"
trigger1 = ctrl
