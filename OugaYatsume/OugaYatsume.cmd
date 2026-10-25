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
name="Invocacion"
command=~D,DF,F,a
time=20
buffer.time=3

[Command]
name="Invocacion"
command=~D,F,a
time=20
buffer.time=3

[Command]
name="Vortice"
command=~D,DB,B,a
time=20
buffer.time=3

[Command]
name="Vortice"
command=~D,B,a
time=20
buffer.time=3

[Command]
name="Lazo"
command=~D,DF,F,b
time=20
buffer.time=3

[Command]
name="Lazo"
command=~D,F,b
time=20
buffer.time=3

[Command]
name="Bomba"
command=~D,DB,B,b
time=20
buffer.time=3

[Command]
name="Bomba"
command=~D,B,b
time=20
buffer.time=3

[Command]
name="Ascendente"
command=~D,DF,F,c
time=20
buffer.time=3

[Command]
name="Ascendente"
command=~D,F,c
time=20
buffer.time=3

[Command]
name="Prision"
command=~D,DB,B,c
time=20
buffer.time=3

[Command]
name="Prision"
command=~D,B,c
time=20
buffer.time=3

[Command]
name="Barrido"
command=/D,a
time=20
buffer.time=3

[Command]
name="Pesado"
command=/D,b
time=20
buffer.time=3

[Command]
name="Estallido"
command=/D,c
time=20
buffer.time=3

[Command]
name="Corte"
command=y
time=20
buffer.time=1

[Command]
name="Orbe"
command=z
time=20
buffer.time=1

[Command]
name="Derrumbe"
command=/D,y
time=20
buffer.time=3

[Command]
name="Paso"
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

[Statedef -1]

[State -1, Invocacion]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Invocacion"
triggerall=StateType!=A
triggerall=Power>=350
trigger1=ctrl
value=1000+10000*Var(42)


[State -1, Vortice]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Vortice"
triggerall=StateType!=A
triggerall=Power>=400
trigger1=ctrl
value=1010+10000*Var(42)


[State -1, Lazo]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Lazo"
triggerall=StateType!=A
triggerall=Power>=450
trigger1=ctrl
value=1020+10000*Var(42)


[State -1, Bomba]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Bomba"
triggerall=StateType!=A
triggerall=Power>=600
trigger1=ctrl
value=1030+10000*Var(42)


[State -1, Ascendente]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Ascendente"
triggerall=StateType!=A
triggerall=Power>=350
trigger1=ctrl
value=1040+10000*Var(42)


[State -1, Prision]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Prision"
triggerall=StateType!=A
triggerall=Power>=500
trigger1=ctrl
value=1050+10000*Var(42)


[State -1, Barrido]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Barrido"
triggerall=StateType!=A
triggerall=Power>=200
trigger1=ctrl
value=1400+10000*Var(42)


[State -1, Pesado]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Pesado"
triggerall=StateType!=A
triggerall=Power>=300
trigger1=ctrl
value=1410+10000*Var(42)


[State -1, Estallido]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Estallido"
triggerall=StateType!=A
triggerall=Power>=400
trigger1=ctrl
value=1420+10000*Var(42)


[State -1, Corte]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Corte"
triggerall=StateType!=A
triggerall=Power>=200
triggerall=command!="holddown"
trigger1=ctrl
value=1200+10000*Var(42)


[State -1, Orbe]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Orbe"
triggerall=StateType!=A
triggerall=Power>=250
triggerall=command!="holddown"
trigger1=ctrl
value=1210+10000*Var(42)


[State -1, Derrumbe]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Derrumbe"
triggerall=StateType!=A
triggerall=Power>=500
trigger1=ctrl
value=1430+10000*Var(42)


[State -1, Paso]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Paso"
triggerall=StateType!=A
triggerall=Power>=350
trigger1=ctrl
value=1440+10000*Var(42)


[State -1, Yatsume Raiton awakening]
type=ChangeState
triggerall=AILevel=0
triggerall=command="s"
triggerall=command="holddown"
triggerall=Var(42)=0
triggerall=Var(41)=0
triggerall=Power>=3000
triggerall=StateType!=A
trigger1=ctrl
value=520


[State -1, Ultimate]
type=ChangeState
triggerall=AILevel=0
triggerall=command="x"
triggerall=Power>=3000
triggerall=StateType!=A
trigger1=ctrl
value=3000+10000*Var(42)


[State -1, Charge]
type=ChangeState
triggerall=AILevel=0
triggerall=command="hold_s"
triggerall=command!="holddown"
triggerall=Power<3000
triggerall=StateType!=A
trigger1=ctrl
value=500


[State -1, Confirmed ground chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="a"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=(StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220 || StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221) && Time>=6 && MoveHit
value=200+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Finite air chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="a"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo%10000>=600 && StateNo%10000<=621 && MoveHit && Time>=6
value=600+10000*Var(42)+Var(12)
ignorehitpause=1

[State -1, Confirmed ground chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="b"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=(StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220 || StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221) && Time>=6 && MoveHit
value=210+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Finite air chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="b"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo%10000>=600 && StateNo%10000<=621 && MoveHit && Time>=6
value=610+10000*Var(42)+Var(12)
ignorehitpause=1

[State -1, Confirmed ground chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="c"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=(StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220 || StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221) && Time>=6 && MoveHit
value=220+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Finite air chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="c"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo%10000>=600 && StateNo%10000<=621 && MoveHit && Time>=6
value=620+10000*Var(42)+Var(12)
ignorehitpause=1

[State -1, Free double tap dash]
type=ChangeState
triggerall=AILevel=0
triggerall=command="FF"
triggerall=StateType=S
trigger1=ctrl
value=100


[State -1, Free double tap dash]
type=ChangeState
triggerall=AILevel=0
triggerall=command="BB"
triggerall=StateType=S
trigger1=ctrl
value=105


[State -1, Native movement]
type=ChangeState
triggerall=AILevel=0
triggerall=command="holdup"
triggerall=StateType!=A
triggerall=StateNo!=40
trigger1=ctrl
value=40
ctrl=0


[State -1, Native movement]
type=ChangeState
triggerall=AILevel=0
triggerall=command="holddown"
triggerall=StateType!=A
triggerall=StateNo!=11
triggerall=StateNo<120 || StateNo>155
trigger1=ctrl
value=11
ctrl=1


[State -1, Native movement]
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


[State -1, Native movement]
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


[State -1, CPU confirmed finite chain]
type=ChangeState
triggerall=AILevel>0
triggerall=MoveHit
triggerall=Time>=6
trigger1=StateNo%10000=200 || StateNo%10000=201
value=StateNo+1


[State -1, CPU legal attack]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=3000
trigger1=P2BodyDist X<120
trigger1=Random<AILevel*3
value=3000+10000*Var(42)


[State -1, CPU legal attack]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=350
trigger1=P2BodyDist X<180
trigger1=Random<AILevel*3
value=1000+10000*Var(42)


[State -1, CPU legal attack]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=400
trigger1=P2BodyDist X<210
trigger1=Random<AILevel*3
value=1010+10000*Var(42)


[State -1, CPU legal attack]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=450
trigger1=P2BodyDist X<240
trigger1=Random<AILevel*3
value=1020+10000*Var(42)


[State -1, CPU legal attack]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
triggerall=Power>=600
trigger1=P2BodyDist X<160
trigger1=Random<AILevel*3
value=1030+10000*Var(42)


[State -1, CPU close normal]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=P2MoveType!=H
trigger1=P2BodyDist X<55
value=200+10000*Var(42)


[State -1, CPU approach]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X>=55
value=20
ctrl=1
