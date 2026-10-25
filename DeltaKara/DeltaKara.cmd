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
command.buffer.time=3

[Command]
name="Piston"
command=~D,DF,F,a
time=20
buffer.time=3

[Command]
name="Piston"
command=~D,F,a
time=20
buffer.time=3

[Command]
name="Pierna"
command=~D,DB,B,a
time=20
buffer.time=3

[Command]
name="Pierna"
command=~D,B,a
time=20
buffer.time=3

[Command]
name="RayoDestructor"
command=~D,DF,F,b
time=20
buffer.time=3

[Command]
name="RayoDestructor"
command=~D,F,b
time=20
buffer.time=3

[Command]
name="Picado"
command=~D,DB,B,b
time=20
buffer.time=3

[Command]
name="Picado"
command=~D,B,b
time=20
buffer.time=3

[Command]
name="Ascenso"
command=~D,DF,F,c
time=20
buffer.time=3

[Command]
name="Ascenso"
command=~D,F,c
time=20
buffer.time=3

[Command]
name="Impacto"
command=~D,DB,B,c
time=20
buffer.time=3

[Command]
name="Impacto"
command=~D,B,c
time=20
buffer.time=3

[Command]
name="Barrido"
command=/D,a
time=20
buffer.time=3

[Command]
name="Lanzador"
command=/D,b
time=20
buffer.time=3

[Command]
name="Onda"
command=/D,c
time=20
buffer.time=3

[Command]
name="Rayo"
command=y
time=20
buffer.time=1

[Command]
name="Propulsion"
command=z
time=20
buffer.time=1

[Command]
name="Absorcion"
command=/D,y
time=20
buffer.time=3

[Command]
name="Devolver"
command=/D,z
time=20
buffer.time=3

[Command]
name="a"
command=a
time=20
buffer.time=3

[Command]
name="hold_a"
command=/a
time=20
buffer.time=1

[Command]
name="b"
command=b
time=20
buffer.time=3

[Command]
name="hold_b"
command=/b
time=20
buffer.time=1

[Command]
name="c"
command=c
time=20
buffer.time=3

[Command]
name="hold_c"
command=/c
time=20
buffer.time=1

[Command]
name="x"
command=x
time=20
buffer.time=3

[Command]
name="hold_x"
command=/x
time=20
buffer.time=1

[Command]
name="y"
command=y
time=20
buffer.time=3

[Command]
name="hold_y"
command=/y
time=20
buffer.time=1

[Command]
name="z"
command=z
time=20
buffer.time=3

[Command]
name="hold_z"
command=/z
time=20
buffer.time=1

[Command]
name="s"
command=s
time=20
buffer.time=3

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
buffer.time=3

[Command]
name="BB"
command=B,B
time=20
buffer.time=3

[Command]
name="recovery"
command=a+b
time=20
buffer.time=3

[Command]
name="flight"
command=y+z
time=20
buffer.time=3

[Statedef -1]

[State -1, Jet flight]
type=ChangeState
triggerall=AILevel=0
triggerall=command="flight"
triggerall=StateType=A
triggerall=StateNo!=550
triggerall=Var(14)=0
triggerall=Power>=100
trigger1=ctrl
value=550


[State -1, Piston]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Piston"
triggerall=StateType!=A
triggerall=Power>=300
trigger1=ctrl
value=1000


[State -1, Pierna]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Pierna"
triggerall=StateType!=A
triggerall=Power>=350
trigger1=ctrl
value=1010


[State -1, RayoDestructor]
type=ChangeState
triggerall=AILevel=0
triggerall=command="RayoDestructor"
triggerall=StateType!=A
triggerall=Power>=500
trigger1=ctrl
value=1020


[State -1, Picado]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Picado"
triggerall=StateType!=A
triggerall=Power>=450
trigger1=ctrl
value=1030


[State -1, Ascenso]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Ascenso"
triggerall=StateType!=A
triggerall=Power>=400
trigger1=ctrl
value=1040


[State -1, Impacto]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Impacto"
triggerall=StateType!=A
triggerall=Power>=500
trigger1=ctrl
value=1050


[State -1, Barrido]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Barrido"
triggerall=StateType!=A
triggerall=Power>=200
trigger1=ctrl
value=1400


[State -1, Lanzador]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Lanzador"
triggerall=StateType!=A
triggerall=Power>=300
trigger1=ctrl
value=1410


[State -1, Onda]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Onda"
triggerall=StateType!=A
triggerall=Power>=400
trigger1=ctrl
value=1420


[State -1, Rayo]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Rayo"
triggerall=StateType!=A
triggerall=Power>=200
triggerall=command!="holddown"
trigger1=ctrl
value=1200


[State -1, Propulsion]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Propulsion"
triggerall=StateType!=A
triggerall=Power>=350
triggerall=command!="holddown"
trigger1=ctrl
value=1210


[State -1, Absorcion]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Absorcion"
triggerall=StateType!=A
triggerall=Power>=150
triggerall=Var(44)<3
trigger1=ctrl
value=1430


[State -1, Devolver]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Devolver"
triggerall=StateType!=A
triggerall=Power>=250
triggerall=Var(44)>0
trigger1=ctrl
value=1440


[State -1, Aerial ocular ray]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Rayo"
triggerall=command!="holddown"
triggerall=command!="flight"
triggerall=StateType=A
triggerall=Power>=200
trigger1=ctrl || StateNo=550
value=11200


[State -1, Overdrive down Pause]
type=ChangeState
triggerall=AILevel=0
triggerall=command="s"
triggerall=command="holddown"
triggerall=StateType!=A
triggerall=Var(40)=0
triggerall=Var(41)=0
triggerall=Power>=1500
trigger1=ctrl
value=520


[State -1, Energy-only self destruction]
type=ChangeState
triggerall=AILevel=0
triggerall=command="x"
triggerall=StateType!=A
triggerall=Power>=3000
trigger1=ctrl
value=3000


[State -1, Hold Pause to charge]
type=ChangeState
triggerall=AILevel=0
triggerall=command="hold_s"
triggerall=command!="holddown"
triggerall=StateType!=A
triggerall=Power<3000
trigger1=ctrl
value=500


[State -1, Three-hit grounded chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="a"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=(StateNo=200 || StateNo=210 || StateNo=220) && MoveHit && Time>=6
trigger3=(StateNo=201 || StateNo=211 || StateNo=221) && MoveHit && Time>=6
value=200+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Three-hit aerial chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="a"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo>=600 && StateNo<=621 && MoveHit && Time>=6
value=600+Var(12)
ignorehitpause=1

[State -1, Three-hit grounded chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="b"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=(StateNo=200 || StateNo=210 || StateNo=220) && MoveHit && Time>=6
trigger3=(StateNo=201 || StateNo=211 || StateNo=221) && MoveHit && Time>=6
value=210+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Three-hit aerial chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="b"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo>=600 && StateNo<=621 && MoveHit && Time>=6
value=610+Var(12)
ignorehitpause=1

[State -1, Three-hit grounded chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="c"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=(StateNo=200 || StateNo=210 || StateNo=220) && MoveHit && Time>=6
trigger3=(StateNo=201 || StateNo=211 || StateNo=221) && MoveHit && Time>=6
value=220+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Three-hit aerial chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="c"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo>=600 && StateNo<=621 && MoveHit && Time>=6
value=620+Var(12)
ignorehitpause=1

[State -1, Free double-tap dash]
type=ChangeState
triggerall=AILevel=0
triggerall=command="FF"
triggerall=StateType=S
trigger1=ctrl
value=100


[State -1, Free double-tap dash]
type=ChangeState
triggerall=AILevel=0
triggerall=command="BB"
triggerall=StateType=S
trigger1=ctrl
value=105


[State -1, Movement]
type=ChangeState
triggerall=AILevel=0
triggerall=command="holdup"
triggerall=StateType!=A
triggerall=StateNo!=40
trigger1=ctrl
value=40
ctrl=0


[State -1, Movement]
type=ChangeState
triggerall=AILevel=0
triggerall=command="holddown"
triggerall=StateType!=A
triggerall=StateNo!=11
triggerall=StateNo<120 || StateNo>155
trigger1=ctrl
value=11
ctrl=1


[State -1, Movement]
type=ChangeState
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


[State -1, Movement]
type=ChangeState
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


[State -1, Finite confirmed CPU chain]
type=ChangeState
triggerall=AILevel>0
triggerall=MoveHit
triggerall=Time>=6
trigger1=StateNo=200 || StateNo=201
value=StateNo+1
ignorehitpause=1

[State -1, CPU legal technique]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=3000
trigger1=P2BodyDist X<140
trigger1=Random<AILevel*3
value=3000


[State -1, CPU legal technique]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=500
trigger1=P2BodyDist X<260
trigger1=Random<AILevel*3
value=1020


[State -1, CPU legal technique]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=200
trigger1=P2BodyDist X<290
trigger1=Random<AILevel*3
value=1200


[State -1, CPU legal technique]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=350
trigger1=P2BodyDist X<110
trigger1=Random<AILevel*3
value=1010


[State -1, CPU legal technique]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=350
trigger1=P2BodyDist X<170
trigger1=Random<AILevel*3
value=1210


[State -1, CPU close normal]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
trigger1=P2BodyDist X<55
value=200


[State -1, CPU approach]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X>=55
value=20
ctrl=1

