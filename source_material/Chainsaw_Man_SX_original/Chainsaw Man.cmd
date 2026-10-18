;--------------------------------------------------------
;Chainsaw man JUS SX Char by stand user X
;https://www.youtube.com/channel/UCVAaMeaPCrHtdoBhErAZVDg
;SPRITES BY REKULL:
;https://www.deviantart.com/rekull/gallery
;SPRITES ADDONS:
;Saxcreed
;https://www.deviantart.com/shaulmorales
;--------------------------------------------------------

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

[Command]
name = "Super Jump"
command = ~D,U
time = 10

;-| Supers |-------------------------------------------------------


[command]
name = "SUPER3"
command = ~B,D,D,F,b+c
time =60

[command]
name = "SUPER3"
command = ~B,DB,D,D,DF,F,b+c
time =60

[command]
name = "SUPER4"
command = ~D,DB,B,D,DB,B,b+c
time = 60

[command]
name = "ul"
command = ~D,F,D,B,D,B,b+c
time = 90

[command]
name = "ul"
command = ~D,DF,F,D,DB,B,D,DB,B,b+c
time = 90

[command]
name = "ul"
command = ~D,F,D,DB,B,D,DB,B,b+c
time = 90

[command]
name = "ul"
command = ~D,F,D,B,D,DB,B,b+c
time = 90

;-| Specials |-------------------------------------------------------
[command]
name = "SUPER1"
command = ~D,DF,F,a+b
time = 30

[command]
name = "SUPER2"
command = ~D,DF,F,b+c
time = 30


[command]
name = "SPECIAL 9"
command = ~B,DB,D,DF,F,b
time = 30

[command]
name = "SPECIAL 10"
command = ~F,DF,D,DB,B,b
time = 30

[command]
name = "SPECIAL 11"
command = ~B,DB,D,DF,F,c
time = 30

[command]
name = "SPECIAL 12"
command = ~F,DF,D,DB,B,c
time = 30

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
command = ~D,DF,F,c
time = 15

[command]
name = "SPECIAL 6"
command = ~D,DB,B,c
time = 15

[command]
name = "SPECIAL 7"
command = ~D,DF,F,x
time = 30

[command]
name = "SPECIAL 8"
command = ~D,DB,B,x
time = 30
;-| extra|-----------------------------------------------------------
[command]
name = "roll"
command = F,a+b
time = 30

[command]
name = "rollbacknetcode"
command = B,a+b
time = 30

[command]
name = "d_roll"
command = a+b
time = 15

[command]
name = "cawabonga"
command = ~D,D,D
time = 30


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
;---------- Comandos de la Inteligencia Artificial-----------------
; Comandos activadores
[Command]
name = "AI Prueba"
command = y+z ; con el botón A+B activamos la AI
time = 1

[Command]
name = "AI desactivado"
command = b+c ; Con el boton B+C desactivamos la AI
time = 1
;---------------------------------------------------------------------------
[Statedef -1]
;===========================================================================
;---------------------------Basicos-----------------------------------------
;---------------------------------------------------------------------------
; Correr Adelante Aire
[State -1, Correr Adelante Aire]
type = ChangeState
value = 65
trigger1 = command = "FF"
trigger1 = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Correr Atras Aire
[State -1, Correr Atras Aire]
type = ChangeState
value = 75
trigger1 = command = "BB"
trigger1 = statetype = A
trigger1 = ctrl
;-----------------------------------------------------------------------------
; Correr Adelante
[State -1, Correr Adelante]
type = ChangeState
triggerall = stateno != 60
triggerall = stateno != 70
value = 60
trigger1 = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Correr Atras
[State -1, Correr Atras]
type = ChangeState
triggerall = stateno != 60
triggerall = stateno != 70
value = 70
trigger1 = command = "BB"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Jump
[State -1, Super Jump]
type = ChangeState
value = 80
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl

[State 180, Quote]
type = victoryquote
triggerall = numenemy 
trigger1 = enemy,name = "Giorno Giovanna"
value = 5
;===========================================================================
;SUPERS:
;===========================================================================


 ; A
[State -1, A]
type = ChangeState
value = 3000
triggerall = power >= 2000
triggerall = numexplod(3002) = 0
triggerall = life <= lifemax/4
triggerall = !ailevel
triggerall = command = "ul"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact
trigger4 = stateno = 202
trigger4 = movecontact
trigger5 = stateno = 210
trigger5 = movecontact
trigger6 = stateno = 220
trigger6 = movecontact
trigger7 = stateno = 250
trigger7 = movecontact
trigger8 = stateno = 280
trigger8 = movecontact
trigger9 = stateno = 300
trigger9 = movecontact
trigger10 = stateno = 310
trigger10 = movecontact
trigger11 = stateno = 400
trigger11 = movecontact
trigger12 = stateno = 410
trigger12 = movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact

 ; A
[State -1, A]
type = ChangeState
value = 2000
triggerall = numexplod(2002) = 0
triggerall = power >= 2000
triggerall = !ailevel
triggerall = command = "SUPER3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact
trigger4 = stateno = 202
trigger4 = movecontact
trigger5 = stateno = 210
trigger5 = movecontact
trigger6 = stateno = 220
trigger6 = movecontact
trigger7 = stateno = 250
trigger7 = movecontact
trigger8 = stateno = 280
trigger8 = movecontact
trigger9 = stateno = 301
trigger9 = movecontact
trigger10 = stateno = 305
trigger10 = movecontact
trigger11 = stateno = 309
trigger11 = movecontact
trigger12 = stateno = 310
trigger12 = movecontact
trigger13 = stateno = 400
trigger13 = movecontact
trigger14 = stateno = 410
trigger14 = movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact

; A
[State -1, A]
type = ChangeState
value = 900
triggerall = ailevel = 0
triggerall = command = "a"
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 60
;===========================================================================
;SPECIALS:
;===========================================================================
; A
[State -1, A]
type = ChangeState
value = 1900
triggerall = !ailevel
triggerall = var(39) != 2
triggerall = var(39) != 1
triggerall = power >= 1000
triggerall = command = "SUPER2"
triggerall = command != "ul"
triggerall = command != "SUPER3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact
trigger4 = stateno = 202
trigger4 = movecontact
trigger5 = stateno = 210
trigger5 = movecontact
trigger6 = stateno = 220
trigger6 = movecontact
trigger7 = stateno = 250
trigger7 = movecontact
trigger8 = stateno = 280
trigger8 = movecontact
trigger9 = stateno = 300
trigger9 = movecontact
trigger10 = stateno = 310
trigger10 = movecontact
trigger11 = stateno = 400
trigger11 = movecontact
trigger12 = stateno = 410
trigger12 = movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact

; A
[State -1, A]
type = ChangeState
value = 1700
triggerall = numhelper(1725) = 0
triggerall = numhelper(1735) = 0
triggerall = numhelper(1745) = 0
triggerall = numhelper(1770) = 0
triggerall = numhelper(1728) = 0
triggerall = !ailevel
triggerall = power >= 1000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact
trigger4 = stateno = 202
trigger4 = movecontact
trigger5 = stateno = 210
trigger5 = movecontact
trigger6 = stateno = 220
trigger6 = movecontact
trigger7 = stateno = 250
trigger7 = movecontact
trigger8 = stateno = 280
trigger8 = movecontact
trigger9 = stateno = 300
trigger9 = movecontact
trigger10 = stateno = 310
trigger10 = movecontact
trigger11 = stateno = 400
trigger11 = movecontact
trigger12 = stateno = 410
trigger12 = movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact

; A
[State -1, A]
type = ChangeState
value = 1600
triggerall = !ailevel
triggerall = power >= 500
triggerall = command = "SPECIAL 6"
triggerall = command != "ul"
triggerall = command != "SUPER3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact
trigger4 = stateno = 202
trigger4 = movecontact
trigger5 = stateno = 210
trigger5 = movecontact
trigger6 = stateno = 220
trigger6 = movecontact
trigger7 = stateno = 250
trigger7 = movecontact
trigger8 = stateno = 280
trigger8 = movecontact
trigger9 = stateno = 300
trigger9 = movecontact
trigger10 = stateno = 310
trigger10 = movecontact
trigger11 = stateno = 400
trigger11 = movecontact
trigger12 = stateno = 410
trigger12 = movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact

; A
[State -1, A]
type = ChangeState
value = 1500
triggerall = numhelper(1505) = 0
triggerall = numhelper(1515) = 0
triggerall = numhelper(1517) = 0
triggerall = numhelper(1519) = 0
triggerall = numhelper(1521) = 0
triggerall = numhelper(1523) = 0
triggerall = numhelper(1525) = 0
triggerall = power >= 500
triggerall = !ailevel
triggerall = command = "SPECIAL 5"
triggerall = command != "ul"
triggerall = command != "SUPER3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact
trigger4 = stateno = 202
trigger4 = movecontact
trigger5 = stateno = 210
trigger5 = movecontact
trigger6 = stateno = 220
trigger6 = movecontact
trigger7 = stateno = 250
trigger7 = movecontact
trigger8 = stateno = 280
trigger8 = movecontact
trigger9 = stateno = 300
trigger9 = movecontact
trigger10 = stateno = 310
trigger10 = movecontact
trigger11 = stateno = 400
trigger11 = movecontact
trigger12 = stateno = 410
trigger12 = movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact

; A
[State -1, A]
type = ChangeState
value = 1550
triggerall = power >= 500
triggerall = !ailevel
triggerall = command = "SPECIAL 5"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact
trigger3 = stateno = 610
trigger3 = movecontact
trigger4 = stateno = 615
trigger4 = movecontact
trigger5 = stateno = 620
trigger5 = movecontact


; A
[State -1, A]
type = ChangeState
value = 1400
triggerall = numhelper(1405) = 0
triggerall = !ailevel
triggerall = power >= 500
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact
trigger4 = stateno = 202
trigger4 = movecontact
trigger5 = stateno = 210
trigger5 = movecontact
trigger6 = stateno = 220
trigger6 = movecontact
trigger7 = stateno = 250
trigger7 = movecontact
trigger8 = stateno = 280
trigger8 = movecontact
trigger9 = stateno = 300
trigger9 = movecontact
trigger10 = stateno = 310
trigger10 = movecontact
trigger11 = stateno = 400
trigger11 = movecontact
trigger12 = stateno = 410
trigger12 = movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact


; A
[State -1, A]
type = ChangeState
value = 1300
triggerall = numhelper(1305) = 0
triggerall = !ailevel
triggerall = power >= 500
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact
trigger4 = stateno = 202
trigger4 = movecontact
trigger5 = stateno = 210
trigger5 = movecontact
trigger6 = stateno = 220
trigger6 = movecontact
trigger7 = stateno = 250
trigger7 = movecontact
trigger8 = stateno = 280
trigger8 = movecontact
trigger9 = stateno = 300
trigger9 = movecontact
trigger10 = stateno = 310
trigger10 = movecontact
trigger11 = stateno = 400
trigger11 = movecontact
trigger12 = stateno = 410
trigger12 = movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact


; A
[State -1, A]
type = ChangeState
value = 1200
triggerall = power >= 500
triggerall = !ailevel
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200 && movecontact
trigger3 = stateno = 201 && movecontact
trigger4 = stateno = 202 && movecontact
trigger5 = stateno = 210 && movecontact
trigger6 = stateno = 220 && movecontact
trigger7 = stateno = 250 && movecontact
trigger8 = stateno = 280 && movecontact
trigger9 = stateno = 300 && movecontact
trigger10 = stateno = 310 && movecontact
trigger11 = stateno = 400 && movecontact
trigger12 = stateno = 410 && movecontact
trigger13 = stateno = 206 && movecontact
trigger14 = stateno = 260 && movecontact
trigger15 = stateno = 255 && movecontact
trigger16 = stateno = 256 && movecontact

; A
[State -1, A]
type = ChangeState
value = 1100
triggerall = power >= 500
triggerall = !ailevel
triggerall = command = "SPECIAL 2"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600 && movecontact
trigger3 = stateno = 610 && movecontact
trigger4 = stateno = 620 && movecontact

; A
[State -1, A]
type = ChangeState
value = 1000
triggerall = power >= 500
triggerall = !ailevel
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200 && movecontact
trigger3 = stateno = 201 && movecontact
trigger4 = stateno = 202 && movecontact
trigger5 = stateno = 401 
trigger6 = stateno = 402
trigger7 = stateno = 403
trigger8 = stateno = 206 && movecontact
trigger9 = stateno = 210 && movecontact
trigger10 = stateno = 255 && movecontact
trigger11 = stateno = 256 && movecontact
trigger12 = stateno = 260 && movecontact
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
value = 508
triggerall = ailevel = 0
triggerall = command = "roll"
triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 60

; Power Charge
[State -1, Power Charge]
type = ChangeState
value = 510
triggerall = ailevel = 0
triggerall = command = "rollbacknetcode"
triggerall = statetype != A
trigger1 = ctrl

; Power Charge
[State -1, Power Charge]
type = ChangeState
value = 516
triggerall = ailevel = 0
triggerall = command = "d_roll"
triggerall = statetype = A
trigger1 = ctrl

; Power Charge
[State -1, Power Charge]
type = ChangeState
value = 514
triggerall = ailevel = 0
triggerall = statetype != A
triggerall = ctrl
trigger1 = command != "holdfwd"  
trigger1 = command = "d_roll"
trigger2 = command != "holdback" 
trigger2 = command = "d_roll"
trigger3 = command != "roll"
trigger3 = command = "d_roll"
trigger4 = command != "rollbacknetcode"
trigger4 = command = "d_roll"

; C Aire
[State -1, C Aire]
type = ChangeState
value = 674
triggerall = ailevel = 0
triggerall = command = "holdback"
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype = C
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 210
trigger3 = movecontact
trigger4 = stateno = 250
trigger4 = movecontact
trigger5 = stateno = 255
trigger5 = movecontact
trigger6 = stateno = 260
trigger6 = movecontact
trigger7 = stateno = 206
trigger7 = movecontact
trigger8 = stateno = 300
trigger8 = movecontact
trigger9 = stateno = 310
trigger9 = movecontact
trigger10 = stateno = 400
trigger10 = movecontact
trigger11 = stateno = 410
trigger11 = movecontact
trigger12 = stateno = 206
trigger12 = movecontact
trigger13 = stateno = 256
trigger13 = movecontact
trigger14 = stateno = 60


; A
[State -1, A]
type = ChangeState
value = 200
triggerall = ailevel = 0
triggerall = command != "x"
triggerall = command != "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl

; A
[State -1, A]
type = ChangeState
value = 210
triggerall = ailevel = 0
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl

; A
[State -1, A]
type = ChangeState
value = 260
triggerall = ailevel = 0
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 210
trigger3 = movecontact


; A
[State -1, A]
type = ChangeState
value = 250
triggerall = ailevel = 0
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 210
trigger3 = movecontact

; A
[State -1, A]
type = ChangeState
value = 280
triggerall = ailevel = 0
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl

; C Aire
[State -1, C Aire]
type = ChangeState
value = 415
triggerall = ailevel = 0
triggerall = command = "holdback"
triggerall = command = "holddown"
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 210
trigger3 = movecontact
trigger4 = stateno = 250
trigger4 = movecontact
trigger5 = stateno = 255
trigger5 = movecontact
trigger6 = stateno = 260
trigger6 = movecontact
trigger7 = stateno = 301
trigger7 = movecontact
trigger8 = stateno = 310
trigger8 = movecontact
trigger9 = stateno = 206
trigger9 = movecontact
trigger10 = stateno = 60

; B
[State -1, B]
type = ChangeState
value = 400
triggerall = ailevel = 0
triggerall = command != "holdback"
triggerall = command != "holddown"
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 210
trigger3 = movecontact
trigger4 = stateno = 250
trigger4 = movecontact
trigger5 = stateno = 255
trigger5 = movecontact
trigger6 = stateno = 260
trigger6 = movecontact
trigger7 = stateno = 301
trigger7 = movecontact
trigger8 = stateno = 310
trigger8 = movecontact

; B
[State -1, B]
type = ChangeState
value = 405
triggerall = !ailevel
triggerall = command != "holdback"
triggerall = command = "holddown"
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 210
trigger3 = movecontact
trigger4 = stateno = 250
trigger4 = movecontact
trigger5 = stateno = 255
trigger5 = movecontact
trigger6 = stateno = 260
trigger6 = movecontact
trigger7 = stateno = 301
trigger7 = movecontact
trigger8 = stateno = 302
trigger9 = stateno = 310
trigger9 = movecontact

;----------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 300
triggerall = numhelper(305) = 0
triggerall = ailevel = 0
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 210
trigger3 = movecontact
trigger4 = stateno = 250
trigger4 = movecontact
trigger5 = stateno = 255
trigger5 = movecontact
trigger6 = stateno = 260
trigger6 = movecontact

; B
[State -1, B]
type = ChangeState
value = 310
triggerall = ailevel = 0
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 210
trigger3 = movecontact
trigger4 = stateno = 250
trigger4 = movecontact
trigger5 = stateno = 255
trigger5 = movecontact
trigger6 = stateno = 260
trigger6 = movecontact
trigger7 = stateno = 206
trigger7 = movecontact


;---------------------------------------------------------------------------


;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
Triggerall = power < 3000
value = 500
triggerall = ailevel = 0
triggerall = command = "s"
triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
value = 600
triggerall = ailevel = 0
triggerall = command = "a"
triggerall = command != "holddown"
Triggerall = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
value = 615
triggerall = ailevel = 0
triggerall = command = "a"
triggerall = command = "holddown"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact

; C Aire
[State -1, C Aire]
type = ChangeState
value = 674
triggerall = ailevel = 0
triggerall = command = "holdback"
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 200
trigger2 = movecontact
trigger3 = stateno = 206
trigger3 = movecontact
trigger4 = stateno = 210
trigger4 = movecontact
trigger5 = stateno = 250
trigger5 = movecontact
trigger6 = stateno = 255
trigger6 = movecontact
trigger7 = stateno = 256
trigger7 = movecontact
trigger8 = stateno = 260
trigger8 = movecontact
trigger9 = stateno = 300
trigger9 = movecontact
trigger10 = stateno = 310
trigger10 = movecontact
trigger11 = stateno = 400
trigger11 = movecontact
trigger12 = stateno = 406
trigger12 = movecontact

; C Aire
[State -1, C Aire]
type = ChangeState
value = 675
triggerall = numexplod(6675) = 0 
triggerall = ailevel = 0
triggerall = command = "holdback"
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact
trigger3 = stateno = 610
trigger3 = movecontact
trigger4 = stateno = 620
trigger4 = movecontact
trigger5 = stateno = 615
trigger5 = movecontact
trigger6 = stateno = 622
trigger6 = movecontact
trigger7 = stateno = 640
trigger7 = movecontact
trigger8 = stateno = 65
trigger8 = stateno = 75


; C Aire
[State -1, C Aire]
type = ChangeState
value = 650
triggerall = ailevel = 0
triggerall = command = "holdback"
triggerall = command = "holddown"
triggerall = command = "x"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact
trigger3 = stateno = 610
trigger3 = movecontact
trigger4 = stateno = 620
trigger4 = movecontact
trigger5 = stateno = 65
trigger5 = stateno = 75

; B Aire
[State -1, B Aire]
type = ChangeState
value = 610
triggerall = ailevel = 0
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact

; B Aire
[State -1, B Aire]
type = ChangeState
value = 617
triggerall = ailevel = 0
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact
trigger3 = stateno = 610
trigger3 = movecontact
trigger4 = stateno = 620
trigger4 = movecontact
trigger5 = stateno = 640
trigger5 = movecontact

; C Aire
[State -1, C Aire]
type = ChangeState
value = 620
triggerall = ailevel = 0
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact
trigger3 = stateno = 610
trigger3 = movecontact

; C Aire
[State -1, C Aire]
type = ChangeState
value = 622
triggerall = ailevel = 0
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact
trigger3 = stateno = 610
trigger3 = movecontact

; C Aire
[State -1, C Aire]
type = ChangeState
value = 640
triggerall = ailevel = 0
triggerall = command = "x"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact
trigger3 = stateno = 610
trigger3 = movecontact
trigger4 = stateno = 620
trigger4 = movecontact
trigger5 = stateno = 65
trigger6 = stateno = 75

; C Aire
[State -1, C Aire]
type = ChangeState
value = 680
triggerall = ailevel = 0
triggerall = command = "cawabonga"
Triggerall = statetype = A
triggerall = backedgebodydist <= 0
trigger1 = ctrl
trigger2 = stateno = 75

[State -1, Air Combo 1-2]
type = ChangeState
value = 705
Triggerall = ailevel = 0
triggerall = command = "y"
triggerall = command = "holdback"
trigger1 = statetype != A
trigger1 = ctrl

[State -1, Air Combo 1-2]
type = ChangeState
value = 700
Triggerall = ailevel = 0
triggerall = command = "y"
triggerall = command != "back"
triggerall = command != "back_y"
triggerall = command != "holdback"
trigger1 = statetype != A
trigger1 = ctrl

; z
[State -1, z]
type = ChangeState
value = 801
triggerall = ailevel = 0
triggerall = var(43) = 0
triggerall = numtarget
triggerall = target,statetype = L
triggerall = target,stateno != 5120
triggerall = command = "z"
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = stateno = 60

; z
[State -1, z]
type = ChangeState
value = 800
triggerall = ailevel = 0
triggerall = var(43) = 0
triggerall = command = "z"
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = stateno = 60

; z
[State -1, z]
type = ChangeState
value = 800
triggerall = ailevel = 0
triggerall = var(43) = 1
triggerall = command = "z"
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = stateno = 60



;---------------------------------------------------------------------------
