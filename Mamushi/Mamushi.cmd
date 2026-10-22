[Remap]
a = a
b = b
c = c
x = x
y = y
z = z
s = s

[Defaults]
command.time = 20
command.buffer.time = 4

[Command]
name = "Brazo"
command = ~D,DF,F,a
time = 20
buffer.time = 4

[Command]
name = "Brazo"
command = ~D,F,a
time = 20
buffer.time = 4

[Command]
name = "Brazo"
command = /DF,a
time = 20
buffer.time = 4

[Command]
name = "Latigo"
command = ~D,DB,B,a
time = 20
buffer.time = 4

[Command]
name = "Latigo"
command = ~D,B,a
time = 20
buffer.time = 4

[Command]
name = "Latigo"
command = /DB,a
time = 20
buffer.time = 4

[Command]
name = "Mandibula"
command = ~D,DF,F,b
time = 20
buffer.time = 4

[Command]
name = "Mandibula"
command = ~D,F,b
time = 20
buffer.time = 4

[Command]
name = "Mandibula"
command = /DF,b
time = 20
buffer.time = 4

[Command]
name = "Taladro"
command = ~D,DB,B,b
time = 20
buffer.time = 4

[Command]
name = "Taladro"
command = ~D,B,b
time = 20
buffer.time = 4

[Command]
name = "Taladro"
command = /DB,b
time = 20
buffer.time = 4

[Command]
name = "Maza"
command = ~D,DF,F,c
time = 20
buffer.time = 4

[Command]
name = "Maza"
command = ~D,F,c
time = 20
buffer.time = 4

[Command]
name = "Maza"
command = /DF,c
time = 20
buffer.time = 4

[Command]
name = "Espinas"
command = ~D,DB,B,c
time = 20
buffer.time = 4

[Command]
name = "Espinas"
command = ~D,B,c
time = 20
buffer.time = 4

[Command]
name = "Espinas"
command = /DB,c
time = 20
buffer.time = 4

[Command]
name = "Barrido"
command = /D,a
time = 20
buffer.time = 4

[Command]
name = "Perforacion"
command = /D,b
time = 20
buffer.time = 4

[Command]
name = "TaladroAscendente"
command = /D,c
time = 20
buffer.time = 4

[Command]
name = "Guardia"
command = y
time = 20
buffer.time = 1

[Command]
name = "Asalto"
command = z
time = 20
buffer.time = 1

[Command]
name = "Retirada"
command = /D,y
time = 20
buffer.time = 4

[Command]
name = "Division"
command = /D,z
time = 20
buffer.time = 4

[Command]
name = "a"
command = a
time = 20
buffer.time = 4

[Command]
name = "hold_a"
command = /a
time = 1
buffer.time = 1

[Command]
name = "b"
command = b
time = 20
buffer.time = 4

[Command]
name = "hold_b"
command = /b
time = 1
buffer.time = 1

[Command]
name = "c"
command = c
time = 20
buffer.time = 4

[Command]
name = "hold_c"
command = /c
time = 1
buffer.time = 1

[Command]
name = "x"
command = x
time = 20
buffer.time = 4

[Command]
name = "hold_x"
command = /x
time = 1
buffer.time = 1

[Command]
name = "y"
command = y
time = 20
buffer.time = 4

[Command]
name = "hold_y"
command = /y
time = 1
buffer.time = 1

[Command]
name = "z"
command = z
time = 20
buffer.time = 4

[Command]
name = "hold_z"
command = /z
time = 1
buffer.time = 1

[Command]
name = "s"
command = s
time = 20
buffer.time = 4

[Command]
name = "hold_s"
command = /s
time = 1
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
name = "FF"
command = F,F
time = 20
buffer.time = 4

[Command]
name = "BB"
command = B,B
time = 20
buffer.time = 4

[Command]
name = "recovery"
command = a+b
time = 20
buffer.time = 4

[Statedef -1]

[State -1, Brazo]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Brazo"
triggerall = StateType != A
triggerall = Power >= 350
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1000
ignorehitpause = 1

[State -1, Latigo]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Latigo"
triggerall = StateType != A
triggerall = Power >= 500
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1010
ignorehitpause = 1

[State -1, Mandibula]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Mandibula"
triggerall = StateType != A
triggerall = Power >= 500
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1020
ignorehitpause = 1

[State -1, Taladro]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Taladro"
triggerall = StateType != A
triggerall = Power >= 650
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1030
ignorehitpause = 1

[State -1, Maza]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Maza"
triggerall = StateType != A
triggerall = Power >= 650
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1040
ignorehitpause = 1

[State -1, Espinas]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Espinas"
triggerall = StateType != A
triggerall = Power >= 500
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1050
ignorehitpause = 1

[State -1, Barrido]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Barrido"
triggerall = StateType != A
triggerall = Power >= 250
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1400
ignorehitpause = 1

[State -1, Perforacion]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Perforacion"
triggerall = StateType != A
triggerall = Power >= 400
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1410
ignorehitpause = 1

[State -1, TaladroAscendente]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "TaladroAscendente"
triggerall = StateType != A
triggerall = Power >= 500
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1420
ignorehitpause = 1

[State -1, Guardia]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Guardia"
triggerall = StateType != A
triggerall = Power >= 500
triggerall = command != "holddown"
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1200
ignorehitpause = 1

[State -1, Asalto]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Asalto"
triggerall = StateType != A
triggerall = Power >= 1000
triggerall = command != "holddown"
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1210
ignorehitpause = 1

[State -1, Retirada]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Retirada"
triggerall = StateType != A
triggerall = Power >= 350
trigger1 = ctrl
trigger2 = StateNo = [200,222]
trigger2 = MoveHit
value = 1430
ignorehitpause = 1

[State -1, Independent Division]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "Division"
triggerall = StateType != A
triggerall = Power >= 750
triggerall = NumHelper(9500) < 6
trigger1 = ctrl
value = 1440

[State -1, Chakra focus with down and LB]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "s"
triggerall = command = "holddown"
triggerall = Power >= 3000
triggerall = Var(40) = 0
triggerall = Var(41) = 0
trigger1 = ctrl
trigger1 = StateType != A
value = 520

[State -1, Xbox A ultimate]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "x"
triggerall = StateType != A
triggerall = Power >= 3000
trigger1 = ctrl
value = 3000

[State -1, LB charge]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "hold_s"
triggerall = command != "holddown"
triggerall = StateType != A
triggerall = Power < PowerMax
trigger1 = ctrl
value = 500

[State -1, FF]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "FF"
triggerall = StateType = S
trigger1 = ctrl
value = 100

[State -1, BB]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "BB"
triggerall = StateType = S
trigger1 = ctrl
value = 105

[State -1, Ground mixed three-stage chain]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "a"
triggerall = StateType != A
triggerall = command != "holddown"
trigger1 = ctrl
trigger2 = StateNo = 200 || StateNo = 210 || StateNo = 220
trigger2 = MoveHit
trigger2 = Time >= 4
trigger3 = StateNo = 201 || StateNo = 211 || StateNo = 221
trigger3 = MoveHit
trigger3 = Time >= 4
value = 200+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause = 1

[State -1, Mixed aerial chain capped per jump]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "a"
triggerall = StateType = A
triggerall = Var(12) < 3
trigger1 = ctrl
trigger2 = StateNo = [600,622]
trigger2 = MoveHit
trigger2 = Time >= 4
value = 600+Var(12)
ignorehitpause = 1

[State -1, Ground mixed three-stage chain]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "b"
triggerall = StateType != A
triggerall = command != "holddown"
trigger1 = ctrl
trigger2 = StateNo = 200 || StateNo = 210 || StateNo = 220
trigger2 = MoveHit
trigger2 = Time >= 4
trigger3 = StateNo = 201 || StateNo = 211 || StateNo = 221
trigger3 = MoveHit
trigger3 = Time >= 4
value = 210+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause = 1

[State -1, Mixed aerial chain capped per jump]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "b"
triggerall = StateType = A
triggerall = Var(12) < 3
trigger1 = ctrl
trigger2 = StateNo = [600,622]
trigger2 = MoveHit
trigger2 = Time >= 4
value = 610+Var(12)
ignorehitpause = 1

[State -1, Ground mixed three-stage chain]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "c"
triggerall = StateType != A
triggerall = command != "holddown"
trigger1 = ctrl
trigger2 = StateNo = 200 || StateNo = 210 || StateNo = 220
trigger2 = MoveHit
trigger2 = Time >= 4
trigger3 = StateNo = 201 || StateNo = 211 || StateNo = 221
trigger3 = MoveHit
trigger3 = Time >= 4
value = 220+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause = 1

[State -1, Mixed aerial chain capped per jump]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "c"
triggerall = StateType = A
triggerall = Var(12) < 3
trigger1 = ctrl
trigger2 = StateNo = [600,622]
trigger2 = MoveHit
trigger2 = Time >= 4
value = 620+Var(12)
ignorehitpause = 1

[State -1, CPU legal technique]
type = ChangeState
triggerall = AILevel > 0
triggerall = RoundState = 2
triggerall = ctrl
triggerall = StateType != A
triggerall = Power >= 3000
trigger1 = P2BodyDist X < 150
trigger1 = Random < 8+AILevel*2
value = 3000

[State -1, CPU legal technique]
type = ChangeState
triggerall = AILevel > 0
triggerall = RoundState = 2
triggerall = ctrl
triggerall = StateType != A
triggerall = Power >= 750
triggerall = NumHelper(9500) < 6
trigger1 = P2BodyDist X < 250
trigger1 = Random < 8+AILevel*2
value = 1440

[State -1, CPU legal technique]
type = ChangeState
triggerall = AILevel > 0
triggerall = RoundState = 2
triggerall = ctrl
triggerall = StateType != A
triggerall = Power >= 650
trigger1 = P2BodyDist X < 160
trigger1 = Random < 8+AILevel*2
value = 1030

[State -1, CPU legal technique]
type = ChangeState
triggerall = AILevel > 0
triggerall = RoundState = 2
triggerall = ctrl
triggerall = StateType != A
triggerall = Power >= 350
trigger1 = P2BodyDist X < 100
trigger1 = Random < 8+AILevel*2
value = 1000

[State -1, CPU normal / follow-up]
type = ChangeState
triggerall = AILevel > 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = P2BodyDist X < 45
trigger1 = ctrl
trigger2 = (StateNo=200 || StateNo=201) && MoveHit
trigger2 = Time >= 4
value = IfElse(ctrl,200,StateNo+1)
ignorehitpause = 1

[State -1, CPU approach]
type = ChangeState
triggerall = AILevel > 0
triggerall = RoundState = 2
triggerall = ctrl
triggerall = StateType != A
trigger1 = P2BodyDist X >= 45
value = 20
ctrl = 1
