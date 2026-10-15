[Remap]
x = x
y = y
z = z
a = a
b = b
c = c
s = s

[Command]
name = "Omnipotencia"
command = x
time = 1

[Command]
name = "Carga"
command = /s
time = 1

[Command]
name = "Despertar"
command = s
time = 1

[Command]
name = "DaemonRapido"
command = ~D,DF,F,a
time = 18

[Command]
name = "DaemonCombo"
command = ~D,DB,B,a
time = 18

[Command]
name = "DaemonPatadas"
command = ~D,DF,F,b
time = 18

[Command]
name = "Encantamiento"
command = ~D,DB,B,b
time = 18

[Command]
name = "Senrigan"
command = ~DB,z
time = 10

[Command]
name = "ParryDaemon"
command = ~DB,y
time = 10

[Command]
name = "FF"
command = F,F
time = 10

[Command]
name = "BB"
command = B,B
time = 10

[Command]
name = "recovery"
command = x+y
time = 1

[Command]
name = "a"
command = a
time = 1

[Command]
name = "b"
command = b
time = 1

[Command]
name = "c"
command = c
time = 1

[Command]
name = "x"
command = x
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "z"
command = z
time = 1

[Command]
name = "s"
command = s
time = 1

[Command]
name = "holdfwd"
command = /$F
time = 1

[Command]
name = "holdback"
command = /$B
time = 1

[Command]
name = "holdup"
command = /$U
time = 1

[Command]
name = "holddown"
command = /$D
time = 1

[Command]
name = "up"
command = $U
time = 1

[Command]
name = "down"
command = $D
time = 1

[Command]
name = "fwd"
command = $F
time = 1

[Command]
name = "back"
command = $B
time = 1

[Statedef -1]

[State -1, Omnipotencia]
type = ChangeState
value = 3000
triggerall = AILevel = 0
triggerall = command = "Omnipotencia"
triggerall = power >= 3000
triggerall = statetype != A
triggerall = numhelper = 0
trigger1 = ctrl

[State -1, Despertar Eida]
type = ChangeState
value = 4000
triggerall = AILevel = 0
triggerall = command = "Despertar"
triggerall = power >= 3000
triggerall = Var(40) = 0
triggerall = statetype != A
trigger1 = ctrl

[State -1, Carga]
type = ChangeState
value = 500
triggerall = AILevel = 0
triggerall = command = "Carga"
triggerall = power < 3000
triggerall = statetype != A
trigger1 = ctrl

[State -1, Despertar ataque]
type = ChangeState
value = 4003
triggerall = AILevel = 0
triggerall = Var(40) = 1
triggerall = ctrl
trigger1 = command = "a"
trigger2 = command = "b"
trigger3 = command = "c"

[State -1, Despertar salto]
type = ChangeState
value = 40
triggerall = AILevel = 0
triggerall = Var(40) = 1
triggerall = ctrl
trigger1 = command = "holdup"

[State -1, Despertar agacharse]
type = ChangeState
value = 10
triggerall = AILevel = 0
triggerall = Var(40) = 1
triggerall = ctrl
trigger1 = command = "holddown"

[State -1, Despertar avance]
type = ChangeState
value = 4002
triggerall = AILevel = 0
triggerall = Var(40) = 1
triggerall = ctrl
trigger1 = command = "holdfwd"

[State -1, Regresar a postura despierta]
type = ChangeState
value = 4001
triggerall = Var(40) = 1
triggerall = ctrl
trigger1 = StateNo = 0

[State -1, Daemon rapido]
type = ChangeState
value = 1000
triggerall = AILevel = 0
triggerall = command = "DaemonRapido"
triggerall = statetype != A
triggerall = numhelper(1001) = 0
trigger1 = ctrl

[State -1, Daemon combo]
type = ChangeState
value = 1010
triggerall = AILevel = 0
triggerall = command = "DaemonCombo"
triggerall = statetype != A
triggerall = numhelper(1011) = 0
trigger1 = ctrl

[State -1, Daemon patadas]
type = ChangeState
value = 1030
triggerall = AILevel = 0
triggerall = command = "DaemonPatadas"
triggerall = statetype != A
triggerall = numhelper(1031) = 0
trigger1 = ctrl

[State -1, Encantamiento]
type = ChangeState
value = 1100
triggerall = AILevel = 0
triggerall = command = "Encantamiento"
triggerall = statetype != A
trigger1 = ctrl

[State -1, Senrigan]
type = ChangeState
value = 1200
triggerall = AILevel = 0
triggerall = command = "Senrigan"
triggerall = power >= 1000
triggerall = statetype != A
trigger1 = ctrl

[State -1, Parry Daemon dos segundos]
type = ChangeState
value = 1350
triggerall = AILevel = 0
triggerall = command = "ParryDaemon"
triggerall = power >= 1000
triggerall = statetype != A
triggerall = numhelper(1351) = 0
trigger1 = ctrl

[State -1, Ataque ligero]
type = ChangeState
value = 200
triggerall = AILevel = 0
triggerall = command = "a"
triggerall = statetype != A
trigger1 = ctrl

[State -1, Ataque fuerte]
type = ChangeState
value = 210
triggerall = AILevel = 0
triggerall = command = "b"
triggerall = statetype != A
trigger1 = ctrl

[State -1, Ataque bajo]
type = ChangeState
value = 220
triggerall = AILevel = 0
triggerall = command = "c"
triggerall = statetype != A
trigger1 = ctrl

[State -1, Ataque aereo ligero]
type = ChangeState
value = 600
triggerall = AILevel = 0
triggerall = command = "a"
triggerall = statetype = A
trigger1 = ctrl

[State -1, Ataque aereo fuerte]
type = ChangeState
value = 610
triggerall = AILevel = 0
triggerall = command = "b"
triggerall = statetype = A
trigger1 = ctrl
