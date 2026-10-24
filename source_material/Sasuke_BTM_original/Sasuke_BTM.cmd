;===============================================================================
;-------------------------------Comandos----------------------------------------
;===============================================================================
[Remap]
x = x
y = y
z = z
a = a
b = b
c = c
s = s

[command]
name = "HYPER"
command = ~D,DF,F,D,DF,F,a+b
time = 30

[command]
name = "SUPER 1"
command = ~D,DF,F,D,DF,F,a
time = 30

[command]
name = "SUPER 2"
command = ~D,DB,B,D,DB,B,a
time = 30

[command]
name = "SUPER 3"
command = ~D,DF,F,D,DF,F,b
time = 30

[command]
name = "SUPER 4"
command = ~D,DB,B,D,DB,B,b
time = 30

[command]
name = "SUPER 5"
command = ~D,DF,F,D,DF,F,c
time = 30

[command]
name = "SUPER 6"
command = ~D,DB,B,D,DB,B,c
time = 30

[Command]
name = "Super Jump"
command = ~x
time = 10

;-| Specials |-------------------------------------------------------
[command]
name = "SPECIAL 1"
command = ~D,DF,F,a
time = 15

[command]
name = "SPECIAL 2"
command = ~D,DB,B,a
time = 15

[command]
name = "SPECIAL 3"
command = ~D,DF,F,b
time = 15

[command]
name = "SPECIAL 4"
command = ~D,DB,B,b
time = 15

[command]
name = "SPECIAL 5"
command = ~D,DB,B,c
time = 15

[command]
name = "SPECIAL 6"
command = ~D,DF,F,c
time = 15

[command]
name = "SPECIAL 7"
command = /D,a;~B,DB,D,DF,F,a
time = 30



[command]
name = "SPECIAL 10"
command = /D,a;~F,DF,D,DB,B,b
time = 30

[command]
name = "SPECIAL 11"
command = /D,b;~B,DB,D,DF,F,c
time = 30

[command]
name = "SPECIAL 12"
command = /D,c;~F,DF,D,DB,B,c
time = 30

[command]
name = "xuong a"
command = x
time = 15

[command]
name = "xuong b"
command = y
time = 15

[command]
name = "xuong c"
command = z
time = 15

[Defaults]

;-| Double Tap |-----------------------------------------------------------
[Command]
name = "FF"     ;Required (do not remove)
command = F, F
time = 10

[Command]
name = "BB"     ;Required (do not remove)
command = B, B
time = 10

[Command]
name = "DD"     ;Required (do not remove)
command = D, D
time = 10
;-| 2/3 Button Combination |-----------------------------------------------
[Command]
name = "recovery" ;Required (do not remove)
command = x+y
time = 1

[Command]
name = "recovery"
command = y+z
time = 1

[Command]
name = "recovery"
command = x+z
time = 1

[Command]
name = "recovery"
command = a+b
time = 1

[Command]
name = "recovery"
command = b+c
time = 1

[Command]
name = "recovery"
command = a+c
time = 1
;-| Dir + Button |---------------------------------------------------------
[Command]
name = "back_x"
command = /$B,x
time = 1

[Command]
name = "back_y"
command = /$B,y
time = 1

[Command]
name = "back_z"
command = /$B,z
time = 1

[Command]
name = "down_x"
command = /$D,x
time = 1

[Command]
name = "down_y"
command = /$D,y
time = 1

[Command]
name = "down_z"
command = /$D,z
time = 1

[Command]
name = "fwd_x"
command = /$F,x
time = 1

[Command]
name = "fwd_y"
command = /$F,y
time = 1

[Command]
name = "fwd_z"
command = /$F,z
time = 1

[Command]
name = "up_x"
command = /$U,x
time = 1

[Command]
name = "up_y"
command = /$U,y
time = 1

[Command]
name = "up_z"
command = /$U,z
time = 1

[Command]
name = "back_a"
command = /$B,a
time = 1

[Command]
name = "back_b"
command = /$B,b
time = 1

[Command]
name = "back_c"
command = /$B,c
time = 1

[Command]
name = "down_a"
command = /$D,a
time = 1

[Command]
name = "down_b"
command = /$D,b
time = 1

[Command]
name = "down_c"
command = /$D,c
time = 1

[Command]
name = "fwd_a"
command = /$F,a
time = 1

[Command]
name = "fwd_b"
command = /$F,b
time = 1

[Command]
name = "fwd_c"
command = /$F,c
time = 1

[Command]
name = "up_a"
command = /$U,a
time = 1

[Command]
name = "up_b"
command = /$U,b
time = 1

[Command]
name = "up_c"
command = /$U,c
time = 1
;-| Single Button |---------------------------------------------------------
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
;-| Single Dir |------------------------------------------------------------
[Command]
name = "fwd" ;Required (do not remove)
command = $F
time = 1

[Command]
name = "downfwd"
command = $DF
time = 1

[Command]
name = "down" ;Required (do not remove)
command = $D
time = 1

[Command]
name = "downback"
command = $DB
time = 1

[Command]
name = "back" ;Required (do not remove)
command = $B
time = 1

[Command]
name = "upback"
command = $UB
time = 1

[Command]
name = "up" ;Required (do not remove)
command = $U
time = 1

[Command]
name = "upfwd"
command = $UF
time = 1
;-| Hold Button |--------------------------------------------------------------
[Command]
name = "hold_x"
command = /x
time = 1

[Command]
name = "hold_y"
command = /y
time = 1

[Command]
name = "hold_z"
command = /z
time = 1

[Command]
name = "hold_a"
command = /a
time = 1

[Command]
name = "hold_b"
command = /b
time = 1

[Command]
name = "hold_c"
command = /c
time = 1

[Command]
name = "hold_s"
command = /s
time = 1
;-| Hold Dir |--------------------------------------------------------------
[Command]
name = "holdfwd" ;Required (do not remove)
command = /$F
time = 1

[Command]
name = "holddownfwd"
command = /$DF
time = 1

[Command]
name = "holddown" ;Required (do not remove)
command = /$D
time = 1

[Command]
name = "holddownback"
command = /$DB
time = 1

[Command]
name = "holdback" ;Required (do not remove)
command = /$B
time = 1

[Command]
name = "holdupback"
command = /$UB
time = 1

[Command]
name = "holdup" ;Required (do not remove)
command = /$U
time = 1

[Command]
name = "holdupfwd"
command = /$UF
time = 1
;---------------------------------------------------------------------------
[Statedef -1]
;===========================================================================
;---------------------------Basicos-----------------------------------------
;---------------------------------------------------------------------------
; Correr Adelante
[State -1, Correr Adelante]
type = ChangeState
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = ifelse(pos y >= 0,60,65)
trigger1 = command = "FF"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Correr Atras
[State -1, Correr Atras]
type = ChangeState
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = ifelse(pos y >= 0,70,75)
trigger1 = command = "BB"
trigger1 = ctrl
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; Susanoo Charge
[State -1, Susanoo Charge]
type = ChangeState
Triggerall = var(2) = 0
Triggerall = power >= 3000
value = 4000
Triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;===========================================================================
; Supers:
;===========================================================================
; SUPER 1
[State -1, SUPER 1]
type = ChangeState
triggerall = numhelper(3050) = 0
Triggerall = power >= 2000
value = 3000
triggerall = command = "xuong a"
Triggerall = statetype != A
trigger1 = ctrl

; SUPER 2
[State -1, SUPER 2]
type = ChangeState
Triggerall = power >= 2000
value = 3100
triggerall = command = "xuong b"
Triggerall = statetype != A
trigger1 = ctrl

; SUPER 3
[State -1, SUPER 3]
type = ChangeState
Triggerall = power >= 2000
value = 3300
triggerall = command = "xuong c"
Triggerall = statetype != A
trigger1 = ctrl
;===========================================================================
; Specials:
;===========================================================================
; Katon Gokakyu no Jutsu
[State -1, SPECIAL 1]
type = ChangeState
Triggerall = power >= 1000
value = 1000
Triggerall = var(2) = 0
Triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------


;---------------------------------------------------------------------------
[State -1, SPECIAL 9]
type = ChangeState
Triggerall = power >= 1000
value = 1800
Triggerall = command = "SPECIAL 10"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
[State -1, SPECIAL 10]
type = ChangeState
Triggerall = power >= 1000
value = 1900
Triggerall = command = "SPECIAL 11"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
[State -1, SPECIAL 11]
type = ChangeState
Triggerall = power >= 1000
value = 1950
Triggerall = command = "SPECIAL 12"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Katon Bakufu Ranbu
[State -1, SPECIAL 2]
type = ChangeState
Triggerall = power >= 1000
value = 1100
Triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Kamui
[State -1, SPECIAL 3]
type = ChangeState
Triggerall = power >= 1000
value = 1200
Triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Kamui Dodge
[State -1, SPECIAL 4]
type = ChangeState
triggerall = numhelper(1350) = 0
Triggerall = power >= 1000
value = 1300
Triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Mokuton
[State -1, SPECIAL 5]
type = ChangeState
Triggerall = power >= 1000
value = 1500
Triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Kuchiyose Juubi: Tenpenchi
[State -1, SPECIAL 6]
type = ChangeState
triggerall = numhelper(1520) = 0
Triggerall = power >= 1000
value = 1401
Triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
Triggerall = power < 3000
value = 500
triggerall = command = "s"
Trigger1 = statetype != A
trigger1 = ctrl
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
; Combo 1
[State -1, Combo 1]
type = ChangeState
value = 200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Combo 2
[State -1, Combo 2]
type = ChangeState
value = 300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Combo 3
[State -1, Combo 3]
type = ChangeState
value = 400
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Air Combo
[State -1, Air Combo 1]
type = ChangeState
value = 600
triggerall = command = "a" || command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Air Combo
[State -1, Air Combo 2]
type = ChangeState
value = 620
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
