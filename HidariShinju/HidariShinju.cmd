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
name="Chidori"
command=~D,DF,F,a
time=20
buffer.time=3

[Command]
name="Chidori"
command=~D,F,a
time=20
buffer.time=3

[Command]
name="Garra"
command=~D,DB,B,a
time=20
buffer.time=3

[Command]
name="Garra"
command=~D,B,a
time=20
buffer.time=3

[Command]
name="Corriente"
command=~D,DF,F,b
time=20
buffer.time=3

[Command]
name="Corriente"
command=~D,F,b
time=20
buffer.time=3

[Command]
name="Prision"
command=~D,DB,B,b
time=20
buffer.time=3

[Command]
name="Prision"
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
name="Madera"
command=~D,DB,B,c
time=20
buffer.time=3

[Command]
name="Madera"
command=~D,B,c
time=20
buffer.time=3

[Command]
name="Barrido"
command=/D,a
time=20
buffer.time=3

[Command]
name="Palma"
command=/D,b
time=20
buffer.time=3

[Command]
name="Ramas"
command=/D,c
time=20
buffer.time=3

[Command]
name="Senbon"
command=y
time=20
buffer.time=1

[Command]
name="Marca"
command=z
time=20
buffer.time=1

[Command]
name="Tormenta"
command=/D,y
time=20
buffer.time=3

[Command]
name="SalidaGarra"
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
[State -1, Supplied Susanoo Chidori]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Chidori"
triggerall=Power>=500
trigger1=ctrl
value=14600


[State -1, Supplied Susanoo Corte de montana]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Garra"
triggerall=Power>=700
trigger1=ctrl
value=14500


[State -1, Supplied Susanoo Shinra Tensei]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Corriente"
triggerall=Power>=600
trigger1=ctrl
value=14700


[State -1, Supplied Susanoo Chibaku Tensei]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Prision"
triggerall=Power>=800
trigger1=ctrl
value=14800


[State -1, Supplied Susanoo Kagetsuchi]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Ascendente"
triggerall=Power>=650
trigger1=ctrl
value=14850


[State -1, Supplied Susanoo Flecha de Indra]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Madera"
triggerall=Power>=3000
trigger1=ctrl
value=14900


[State -1, Supplied Susanoo Puno]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="a"
triggerall=Power>=0
trigger1=ctrl
value=14200


[State -1, Supplied Susanoo Patada]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="b"
triggerall=Power>=0
trigger1=ctrl
value=14300


[State -1, Supplied Susanoo Espada ascendente]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="c"
triggerall=Power>=0
trigger1=ctrl
value=14400


[State -1, Original Susanoo shortcut]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="x"
triggerall=Power>=3000
trigger1=ctrl
value=14900


[State -1, Original Susanoo shortcut]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Senbon"
triggerall=Power>=700
triggerall=command!="holddown"
trigger1=ctrl
value=14500


[State -1, Original Susanoo shortcut]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Marca"
triggerall=Power>=600
triggerall=command!="holddown"
trigger1=ctrl
value=14700


[State -1, Original Susanoo shortcut]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Barrido"
triggerall=Power>=0
triggerall=command="holddown"
trigger1=ctrl
value=14200


[State -1, Original Susanoo shortcut]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Palma"
triggerall=Power>=0
triggerall=command="holddown"
trigger1=ctrl
value=14300


[State -1, Original Susanoo shortcut]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Ramas"
triggerall=Power>=0
triggerall=command="holddown"
trigger1=ctrl
value=14400


[State -1, Original Susanoo shortcut]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="Tormenta"
triggerall=Power>=800
triggerall=command="holddown"
trigger1=ctrl
value=14800


[State -1, Original Susanoo shortcut]
type=ChangeState
triggerall=AILevel=0
triggerall=Var(42)=1
triggerall=StateType!=A
triggerall=command="SalidaGarra"
triggerall=Power>=650
triggerall=command="holddown"
trigger1=ctrl
value=14850



[State -1, Chidori]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Chidori"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),280,350)
trigger1=ctrl
value=1000+10000*Var(42)


[State -1, Garra]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Garra"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),360,450)
trigger1=ctrl
value=1010+10000*Var(42)


[State -1, Corriente]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Corriente"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),400,500)
trigger1=ctrl
value=1020+10000*Var(42)


[State -1, Prision]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Prision"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),520,650)
trigger1=ctrl
value=1030+10000*Var(42)


[State -1, Ascendente]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Ascendente"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),360,450)
trigger1=ctrl
value=1040+10000*Var(42)


[State -1, Madera]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Madera"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),440,550)
trigger1=ctrl
value=1050+10000*Var(42)


[State -1, Barrido]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Barrido"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),160,200)
trigger1=ctrl
value=1400+10000*Var(42)


[State -1, Palma]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Palma"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),240,300)
trigger1=ctrl
value=1410+10000*Var(42)


[State -1, Ramas]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Ramas"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),320,400)
trigger1=ctrl
value=1420+10000*Var(42)


[State -1, Senbon]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Senbon"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),160,200)
triggerall=command!="holddown"
trigger1=ctrl
value=1200+10000*Var(42)


[State -1, Marca]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Marca"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),200,250)
triggerall=command!="holddown"
trigger1=ctrl
value=IfElse(NumHelper(9600)>0,1211,1210)+10000*Var(42)


[State -1, Tormenta]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="Tormenta"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),520,650)
trigger1=ctrl
value=1430+10000*Var(42)


[State -1, SalidaGarra]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="SalidaGarra"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),320,400)
trigger1=ctrl
value=1440+10000*Var(42)


[State -1, Yellow Susanoo awakening]
type=ChangeState
triggerall=AILevel=0
triggerall=command="s"
triggerall=command="holddown"
triggerall=Power>=3000
triggerall=Var(42)=0
triggerall=Var(41)=0
triggerall=StateType!=A
trigger1=ctrl
value=520


[State -1, Ultimate Xbox A]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="x"
triggerall=Power>=3000
triggerall=StateType!=A
trigger1=ctrl
value=3000+10000*Var(42)


[State -1, Hold Pause to charge]
type=ChangeState
triggerall=AILevel=0
triggerall=command="hold_s"
triggerall=command!="holddown"
triggerall=Power<3000
triggerall=StateType!=A
trigger1=ctrl
value=500


[State -1, Ground chain]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="a"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220
trigger2=MoveHit
trigger2=Time>=6
trigger3=StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221
trigger3=MoveHit
trigger3=Time>=6
value=200+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Aerial chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="a"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo%10000>=600 && StateNo%10000<=621
trigger2=MoveHit
trigger2=Time>=6
value=600+10000*Var(42)+Var(12)
ignorehitpause=1

[State -1, Ground chain]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="b"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220
trigger2=MoveHit
trigger2=Time>=6
trigger3=StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221
trigger3=MoveHit
trigger3=Time>=6
value=210+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Aerial chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="b"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo%10000>=600 && StateNo%10000<=621
trigger2=MoveHit
trigger2=Time>=6
value=610+10000*Var(42)+Var(12)
ignorehitpause=1

[State -1, Ground chain]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel=0
triggerall=command="c"
triggerall=command!="holddown"
triggerall=StateType!=A
trigger1=ctrl
trigger2=StateNo%10000=200 || StateNo%10000=210 || StateNo%10000=220
trigger2=MoveHit
trigger2=Time>=6
trigger3=StateNo%10000=201 || StateNo%10000=211 || StateNo%10000=221
trigger3=MoveHit
trigger3=Time>=6
value=220+10000*Var(42)+IfElse(ctrl,0,IfElse(StateNo%10=0,1,2))
ignorehitpause=1

[State -1, Aerial chain]
type=ChangeState
triggerall=AILevel=0
triggerall=command="c"
triggerall=StateType=A
triggerall=Var(12)<3
trigger1=ctrl
trigger2=StateNo%10000>=600 && StateNo%10000<=621
trigger2=MoveHit
trigger2=Time>=6
value=620+10000*Var(42)+Var(12)
ignorehitpause=1

[State -1, Double tap dash]
type=ChangeState
triggerall=AILevel=0
triggerall=command="FF"
triggerall=StateType=S
trigger1=ctrl
value=100


[State -1, Double tap dash]
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


[State -1, CPU legal attack]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=3000
trigger1=P2BodyDist X<140
trigger1=Random<AILevel*3
value=3000+10000*Var(42)


[State -1, CPU legal attack]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=650
trigger1=P2BodyDist X<180
trigger1=Random<AILevel*3
value=1030+10000*Var(42)


[State -1, CPU legal attack]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=200
trigger1=P2BodyDist X<300
trigger1=Random<AILevel*3
value=1200+10000*Var(42)


[State -1, CPU legal attack]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=500
trigger1=P2BodyDist X<260
trigger1=Random<AILevel*3
value=1020+10000*Var(42)


[State -1, CPU legal attack]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=500
trigger1=P2BodyDist X<250
trigger1=Random<AILevel*3
value=1010+10000*Var(42)


[State -1, CPU close chain]
type=ChangeState
triggerall=Var(42)=0
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X<65
value=200+10000*Var(42)


[State -1, CPU approach]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X>=65
value=20
ctrl=1
