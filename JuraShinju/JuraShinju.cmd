[Remap]
a=a
b=b
c=c
x=x
y=y
z=z
s=s
[Defaults]
command.time=20
command.buffer.time=4

[Command]
name="Espinas"
command=~D,DF,F,a
time=20
buffer.time=4

[Command]
name="Espinas"
command=~D,F,a
time=20
buffer.time=4

[Command]
name="Espinas"
command=/DF,a
time=20
buffer.time=4

[Command]
name="Raiz"
command=~D,DB,B,a
time=20
buffer.time=4

[Command]
name="Raiz"
command=~D,B,a
time=20
buffer.time=4

[Command]
name="Raiz"
command=/DB,a
time=20
buffer.time=4

[Command]
name="Bijudama"
command=~D,DF,F,b
time=20
buffer.time=4

[Command]
name="Bijudama"
command=~D,F,b
time=20
buffer.time=4

[Command]
name="Bijudama"
command=/DF,b
time=20
buffer.time=4

[Command]
name="BijudamaCargada"
command=~D,DB,B,b
time=20
buffer.time=4

[Command]
name="BijudamaCargada"
command=~D,B,b
time=20
buffer.time=4

[Command]
name="BijudamaCargada"
command=/DB,b
time=20
buffer.time=4

[Command]
name="Garras"
command=~D,DF,F,c
time=20
buffer.time=4

[Command]
name="Garras"
command=~D,F,c
time=20
buffer.time=4

[Command]
name="Garras"
command=/DF,c
time=20
buffer.time=4

[Command]
name="Arbol"
command=~D,DB,B,c
time=20
buffer.time=4

[Command]
name="Arbol"
command=~D,B,c
time=20
buffer.time=4

[Command]
name="Arbol"
command=/DB,c
time=20
buffer.time=4

[Command]
name="Barrido"
command=/D,a
time=20
buffer.time=4

[Command]
name="Lanzador"
command=/D,b
time=20
buffer.time=4

[Command]
name="RafagaOcular"
command=/D,c
time=20
buffer.time=4

[Command]
name="Francotirador"
command=y
time=20
buffer.time=1

[Command]
name="Marca"
command=z
time=20
buffer.time=1

[Command]
name="AsedioOcular"
command=/D,y
time=20
buffer.time=4

[Command]
name="SalidaGarra"
command=/D,z
time=20
buffer.time=4

[Command]
name="a"
command=a
time=20
buffer.time=4

[Command]
name="hold_a"
command=/a
time=20
buffer.time=1

[Command]
name="b"
command=b
time=20
buffer.time=4

[Command]
name="hold_b"
command=/b
time=20
buffer.time=1

[Command]
name="c"
command=c
time=20
buffer.time=4

[Command]
name="hold_c"
command=/c
time=20
buffer.time=1

[Command]
name="x"
command=x
time=20
buffer.time=4

[Command]
name="hold_x"
command=/x
time=20
buffer.time=1

[Command]
name="y"
command=y
time=20
buffer.time=4

[Command]
name="hold_y"
command=/y
time=20
buffer.time=1

[Command]
name="z"
command=z
time=20
buffer.time=4

[Command]
name="hold_z"
command=/z
time=20
buffer.time=1

[Command]
name="s"
command=s
time=20
buffer.time=4

[Command]
name="hold_s"
command=/s
time=20
buffer.time=1

[Command]
name="holdfwd"
command=/$F
time=20
buffer.time=1

[Command]
name="holdback"
command=/$B
time=20
buffer.time=1

[Command]
name="holdup"
command=/$U
time=20
buffer.time=1

[Command]
name="holddown"
command=/$D
time=20
buffer.time=1

[Command]
name="FF"
command=F,F
time=20
buffer.time=4

[Command]
name="BB"
command=B,B
time=20
buffer.time=4

[Command]
name="recovery"
command=a+b
time=20
buffer.time=4

[Statedef -1]

[State -1, Finite CPU confirmed three-hit chain]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=MoveHit
triggerall=Time>=6
trigger1=StateNo%10000=200 || StateNo%10000=201
value=StateNo+1
ignorehitpause=1


[State -1, Espinas]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Espinas"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,262,350)
trigger1=ctrl
value=1000

[State -1, Raiz]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Raiz"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,338,450)
trigger1=ctrl
value=1010

[State -1, Bijudama]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Bijudama"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,375,500)
trigger1=ctrl
value=1020

[State -1, BijudamaCargada]
type = ChangeState
triggerall=AILevel=0
triggerall=command="BijudamaCargada"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,525,700)
trigger1=ctrl
value=1030

[State -1, Garras]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Garras"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,300,400)
trigger1=ctrl
value=1040

[State -1, Arbol]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Arbol"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,488,650)
trigger1=ctrl
value=1050

[State -1, Barrido]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Barrido"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,188,250)
trigger1=ctrl
value=1400

[State -1, Lanzador]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Lanzador"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,300,400)
trigger1=ctrl
value=1410

[State -1, RafagaOcular]
type = ChangeState
triggerall=AILevel=0
triggerall=command="RafagaOcular"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,300,400)
trigger1=ctrl
value=1420

[State -1, Francotirador]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Francotirador"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,188,250)
triggerall=command!="holddown"
trigger1=ctrl
value=1200

[State -1, Marca]
type = ChangeState
triggerall=AILevel=0
triggerall=command="Marca"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,225,300)
triggerall=command!="holddown"
trigger1=ctrl
value=IfElse(NumHelper(9600)>0,1211,1210)

[State -1, AsedioOcular]
type = ChangeState
triggerall=AILevel=0
triggerall=command="AsedioOcular"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,262,350)
trigger1=ctrl
value=1430

[State -1, SalidaGarra]
type = ChangeState
triggerall=AILevel=0
triggerall=command="SalidaGarra"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,375,500)
trigger1=ctrl
value=1440

[State -1, Awakening]
type = ChangeState
triggerall=AILevel=0
triggerall=command="s"
triggerall=command="holddown"
triggerall=Power>=3000
triggerall=Var(40)=0
triggerall=Var(41)=0
trigger1=ctrl
trigger1=StateType!=A
value=520

[State -1, Xbox A ultimate]
type = ChangeState
triggerall=AILevel=0
triggerall=command="x"
triggerall=Power>=3000
triggerall=StateType!=A
trigger1=ctrl
value=3000

[State -1, Hold Pause to charge]
type = ChangeState
triggerall=AILevel=0
triggerall=command="hold_s"
triggerall=command!="holddown"
triggerall=Power<3000
triggerall=StateType!=A
trigger1=ctrl
value=500

[State -1, Ground combo]
type = ChangeState
triggerall=AILevel=0
triggerall=command="a"
triggerall=StateType!=A
triggerall=command!="holddown"
trigger1=ctrl
trigger2=StateNo=200 || StateNo=210 || StateNo=220
trigger2=MoveHit
trigger2=Time>=6
trigger3=StateNo=201 || StateNo=211 || StateNo=221
trigger3=MoveHit
trigger3=Time>=6
value=200+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause=1

[State -1, Finite aerial chain]
type = ChangeState
triggerall=AILevel=0
triggerall=command="a"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo>=600 && StateNo<=621
trigger2=MoveHit
trigger2=Time>=6
value=600+Var(12)
ignorehitpause=1

[State -1, Ground combo]
type = ChangeState
triggerall=AILevel=0
triggerall=command="b"
triggerall=StateType!=A
triggerall=command!="holddown"
trigger1=ctrl
trigger2=StateNo=200 || StateNo=210 || StateNo=220
trigger2=MoveHit
trigger2=Time>=6
trigger3=StateNo=201 || StateNo=211 || StateNo=221
trigger3=MoveHit
trigger3=Time>=6
value=210+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause=1

[State -1, Finite aerial chain]
type = ChangeState
triggerall=AILevel=0
triggerall=command="b"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo>=600 && StateNo<=621
trigger2=MoveHit
trigger2=Time>=6
value=610+Var(12)
ignorehitpause=1

[State -1, Ground combo]
type = ChangeState
triggerall=AILevel=0
triggerall=command="c"
triggerall=StateType!=A
triggerall=command!="holddown"
trigger1=ctrl
trigger2=StateNo=200 || StateNo=210 || StateNo=220
trigger2=MoveHit
trigger2=Time>=6
trigger3=StateNo=201 || StateNo=211 || StateNo=221
trigger3=MoveHit
trigger3=Time>=6
value=220+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause=1

[State -1, Finite aerial chain]
type = ChangeState
triggerall=AILevel=0
triggerall=command="c"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo>=600 && StateNo<=621
trigger2=MoveHit
trigger2=Time>=6
value=620+Var(12)
ignorehitpause=1

[State -1, Double-tap dash]
type = ChangeState
triggerall=AILevel=0
triggerall=command="FF"
triggerall=StateType=S
trigger1=ctrl
value=100

[State -1, Double-tap dash]
type = ChangeState
triggerall=AILevel=0
triggerall=command="BB"
triggerall=StateType=S
trigger1=ctrl
value=105

[State -1, Ground movement]
type = ChangeState
triggerall=AILevel=0
triggerall=command="holdup"
triggerall=StateType!=A
triggerall=StateNo!=40
trigger1=ctrl
value=40
ctrl=0

[State -1, Ground movement]
type = ChangeState
triggerall=AILevel=0
triggerall=command="holddown"
triggerall=StateType!=A
triggerall=StateNo!=11
triggerall=StateNo<120 || StateNo>155
trigger1=ctrl
value=11
ctrl=1

[State -1, Ground movement]
type = ChangeState
triggerall=AILevel=0
triggerall=command="holdfwd"
triggerall=StateType!=A
triggerall=StateNo!=20
triggerall=StateType=S
triggerall=command!="holdup"
triggerall=command!="holddown"
triggerall=StateNo<120 || StateNo>155
trigger1=ctrl
value=20
ctrl=1

[State -1, Ground movement]
type = ChangeState
triggerall=AILevel=0
triggerall=command="holdback"
triggerall=StateType!=A
triggerall=StateNo!=20
triggerall=StateType=S
triggerall=command!="holdup"
triggerall=command!="holddown"
triggerall=StateNo<120 || StateNo>155
trigger1=ctrl
value=20
ctrl=1

[State -1, CPU legal technique]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,225,300)
triggerall=NumHelper(9600)>0
triggerall=P2BodyDist X>90
trigger1=P2BodyDist X<999
trigger1=Random<8+AILevel*2
triggerall=P2MoveType!=H
value=1211

[State -1, CPU legal technique]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,450,600)
triggerall=NumHelper(9600)=0
triggerall=P2BodyDist X>170
trigger1=P2BodyDist X<999
trigger1=Random<8+AILevel*2
triggerall=P2MoveType!=H
value=1210

[State -1, CPU legal technique]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,2250,3000)
trigger1=P2BodyDist X<190
trigger1=Random<8+AILevel*2
triggerall=P2MoveType!=H
value=3000

[State -1, CPU legal technique]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,188,250)
trigger1=P2BodyDist X<310
trigger1=Random<8+AILevel*2
triggerall=P2MoveType!=H
value=1200

[State -1, CPU legal technique]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,375,500)
trigger1=P2BodyDist X<230
trigger1=Random<8+AILevel*2
triggerall=P2MoveType!=H
value=1020

[State -1, CPU legal technique]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,262,350)
trigger1=P2BodyDist X<170
trigger1=Random<8+AILevel*2
triggerall=P2MoveType!=H
value=1000

[State -1, CPU taijutsu]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X<70
triggerall=P2MoveType!=H
value=200

[State -1, CPU approach]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X>=70
value=20
ctrl=1
