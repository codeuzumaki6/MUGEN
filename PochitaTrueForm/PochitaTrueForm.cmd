[Remap]
a = a
b = b
c = c
x = x
y = y
z = z
s = s

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
name = "holdcharge"
command = /s
time = 20
buffer.time = 1

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
name = "Desgarro"
command = ~D,DF,F,a
time = 20
buffer.time = 3

[Command]
name = "Desgarro"
command = /DF,a
time = 20
buffer.time = 3

[Command]
name = "CuatroBrazos"
command = ~D,DB,B,a
time = 20
buffer.time = 3

[Command]
name = "CuatroBrazos"
command = /DB,a
time = 20
buffer.time = 3

[Command]
name = "Ascenso"
command = /D,a
time = 20
buffer.time = 3

[Command]
name = "Estocada"
command = ~D,DF,F,b
time = 20
buffer.time = 3

[Command]
name = "Estocada"
command = /DF,b
time = 20
buffer.time = 3

[Command]
name = "Barrido"
command = ~D,DB,B,b
time = 20
buffer.time = 3

[Command]
name = "Barrido"
command = /DB,b
time = 20
buffer.time = 3

[Command]
name = "Guillotina"
command = /D,b
time = 20
buffer.time = 3

[Command]
name = "Embestida"
command = ~D,DF,F,c
time = 20
buffer.time = 3

[Command]
name = "Embestida"
command = /DF,c
time = 20
buffer.time = 3

[Command]
name = "Carniceria"
command = ~D,DB,B,c
time = 20
buffer.time = 3

[Command]
name = "Carniceria"
command = /DB,c
time = 20
buffer.time = 3

[Command]
name = "Rasante"
command = /D,c
time = 20
buffer.time = 3

[Command]
name = "Asalto"
command = z
time = 20
buffer.time = 3

[Statedef -1]

[State -1, AI counter]
type = ChangeState
value = 1400
triggerall = AILevel > 0
triggerall = StateType != A
triggerall = Power >= 500
triggerall = P2Dist X < 75
triggerall = P2MoveType = A
triggerall = Random < AILevel*3
trigger1 = Ctrl

[State -1, AI ultimate]
type = ChangeState
value = 3000
triggerall = AILevel > 0
triggerall = StateType != A
triggerall = Power >= 3000
triggerall = P2Dist X < 160
triggerall = Random < AILevel*2
trigger1 = Ctrl

[State -1, AI reach]
type = ChangeState
value = 1030
triggerall = AILevel > 0
triggerall = StateType != A
triggerall = Power >= 750
triggerall = P2Dist X = [85,150]
triggerall = Random < AILevel*5
trigger1 = Ctrl

[State -1, AI close]
type = ChangeState
value = 200
triggerall = AILevel > 0
triggerall = StateType != A
triggerall = P2Dist X < 78
triggerall = Random < 160+AILevel*30
trigger1 = Ctrl

[State -1, AI approach]
type = ChangeState
value = 100
triggerall = AILevel > 0
triggerall = StateType != A
triggerall = P2Dist X > 95
triggerall = Random < 60+AILevel*10
trigger1 = Ctrl

[State -1, AI air cut]
type = ChangeState
value = 600
triggerall = AILevel > 0
triggerall = StateType = A
triggerall = P2Dist X < 90
triggerall = Random < 180
trigger1 = Ctrl

[State -1, Xbox A Ultimate]
type = ChangeState
value = 3000
triggerall = command = "x"
triggerall = Power >= 3000
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100

[State -1, Desgarro]
type = ChangeState
value = 1000
triggerall = command = "Desgarro"
triggerall = Power >= 500
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, CuatroBrazos]
type = ChangeState
value = 1010
triggerall = command = "CuatroBrazos"
triggerall = Power >= 750
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, Ascenso]
type = ChangeState
value = 1020
triggerall = command = "Ascenso"
triggerall = Power >= 500
triggerall = StateType != A
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, Estocada]
type = ChangeState
value = 1030
triggerall = command = "Estocada"
triggerall = Power >= 750
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, Barrido]
type = ChangeState
value = 1040
triggerall = command = "Barrido"
triggerall = Power >= 500
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, Guillotina]
type = ChangeState
value = 1050
triggerall = command = "Guillotina"
triggerall = Power >= 1000
triggerall = StateType != A
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, Embestida]
type = ChangeState
value = 1060
triggerall = command = "Embestida"
triggerall = Power >= 1000
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, Carniceria]
type = ChangeState
value = 1070
triggerall = command = "Carniceria"
triggerall = Power >= 1500
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, Rasante]
type = ChangeState
value = 1080
triggerall = command = "Rasante"
triggerall = Power >= 500
triggerall = StateType != A
triggerall = command != "holdfwd"
triggerall = command != "holdback"
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, Asalto]
type = ChangeState
value = 1100
triggerall = command = "Asalto"
triggerall = Power >= 1500
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100
trigger3 = StateNo = 200
trigger3 = MoveHit
trigger4 = StateNo = 201
trigger4 = MoveHit
trigger5 = StateNo = 202
trigger5 = MoveHit
trigger6 = StateNo = 210
trigger6 = MoveHit
trigger7 = StateNo = 211
trigger7 = MoveHit
trigger8 = StateNo = 220
trigger8 = MoveHit
trigger9 = StateNo = 221
trigger9 = MoveHit

[State -1, RB Chainsaw guard]
type = ChangeState
value = 1400
triggerall = command = "y"
triggerall = Power >= 500
triggerall = StateType != A
trigger1 = Ctrl

[State -1, LB Rev motor]
type = ChangeState
value = 500
triggerall = command = "holdcharge"
triggerall = Power < 3000
triggerall = StateType != A
trigger1 = Ctrl

[State -1, FF]
type = ChangeState
value = 100
triggerall = command = "FF"
triggerall = StateType = S
trigger1 = Ctrl

[State -1, BB]
type = ChangeState
value = 105
triggerall = command = "BB"
triggerall = StateType = S
trigger1 = Ctrl

[State -1, Hit confirmed 200 to 201]
type = ChangeState
value = 201
triggerall = StateNo = 200
triggerall = MoveHit
triggerall = Time > 0
trigger1 = Var(25) = 1
ignorehitpause = 1

[State -1, Hit confirmed 201 to 202]
type = ChangeState
value = 202
triggerall = StateNo = 201
triggerall = MoveHit
triggerall = Time > 0
trigger1 = Var(25) = 1
ignorehitpause = 1

[State -1, Hit confirmed 210 to 211]
type = ChangeState
value = 211
triggerall = StateNo = 210
triggerall = MoveHit
triggerall = Time > 0
trigger1 = Var(25) = 1
ignorehitpause = 1

[State -1, Hit confirmed 220 to 221]
type = ChangeState
value = 221
triggerall = StateNo = 220
triggerall = MoveHit
triggerall = Time > 0
trigger1 = Var(25) = 1
ignorehitpause = 1

[State -1, Hit confirmed 600 to 610]
type = ChangeState
value = 610
triggerall = StateNo = 600
triggerall = MoveHit
triggerall = Time > 0
trigger1 = Var(25) = 1
ignorehitpause = 1

[State -1, Hit confirmed 610 to 620]
type = ChangeState
value = 620
triggerall = StateNo = 610
triggerall = MoveHit
triggerall = Time > 0
trigger1 = Var(25) = 1
ignorehitpause = 1

[State -1, Normal a]
type = ChangeState
value = 200
triggerall = command = "a"
triggerall = command != "holddown"
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100

[State -1, Normal b]
type = ChangeState
value = 210
triggerall = command = "b"
triggerall = command != "holddown"
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100

[State -1, Normal c]
type = ChangeState
value = 220
triggerall = command = "c"
triggerall = command != "holddown"
triggerall = StateType != A
trigger1 = Ctrl
trigger2 = StateNo = 100

[State -1, Crouch a]
type = ChangeState
value = 400
triggerall = command = "a"
triggerall = command = "holddown"
triggerall = StateType != A
trigger1 = Ctrl

[State -1, Crouch b]
type = ChangeState
value = 410
triggerall = command = "b"
triggerall = command = "holddown"
triggerall = StateType != A
trigger1 = Ctrl

[State -1, Crouch c]
type = ChangeState
value = 420
triggerall = command = "c"
triggerall = command = "holddown"
triggerall = StateType != A
trigger1 = Ctrl

[State -1, Air a]
type = ChangeState
value = 600
triggerall = command = "a"
triggerall = StateType = A
trigger1 = Ctrl

[State -1, Air b]
type = ChangeState
value = 610
triggerall = command = "b"
triggerall = StateType = A
trigger1 = Ctrl

[State -1, Air c]
type = ChangeState
value = 620
triggerall = command = "c"
triggerall = StateType = A
trigger1 = Ctrl
