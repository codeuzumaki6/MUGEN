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
name="Lanza"
command=~D,DF,F,a
time=20
buffer.time=3

[Command]
name="Lanza"
command=~D,F,a
time=20
buffer.time=3

[Command]
name="Latigo"
command=~D,DB,B,a
time=20
buffer.time=3

[Command]
name="Latigo"
command=~D,B,a
time=20
buffer.time=3

[Command]
name="Suiton"
command=~D,DF,F,b
time=20
buffer.time=3

[Command]
name="Suiton"
command=~D,F,b
time=20
buffer.time=3

[Command]
name="Jardin"
command=~D,DB,B,b
time=20
buffer.time=3

[Command]
name="Jardin"
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
name="Atadura"
command=~D,DB,B,c
time=20
buffer.time=3

[Command]
name="Atadura"
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
name="Manto"
command=/D,c
time=20
buffer.time=3

[Command]
name="Agua"
command=y
time=20
buffer.time=1

[Command]
name="Marca"
command=z
time=20
buffer.time=1

[Command]
name="Erupcion"
command=/D,y
time=20
buffer.time=3

[Command]
name="Emboscada"
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

[State -1, Finite CPU confirmed three-hit chain]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=MoveHit
triggerall=Time>=6
trigger1=StateNo%10000=200 || StateNo%10000=201
value=StateNo+1
ignorehitpause=1


[State -1, Lanza]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Lanza"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),280,350)
trigger1=ctrl
value=1000+10000*Var(42)


[State -1, Latigo]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Latigo"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),320,400)
trigger1=ctrl
value=1010+10000*Var(42)


[State -1, Suiton]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Suiton"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),360,450)
trigger1=ctrl
value=1020+10000*Var(42)


[State -1, Jardin]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Jardin"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),400,500)
trigger1=ctrl
value=1030+10000*Var(42)


[State -1, Ascendente]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Ascendente"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),360,450)
trigger1=ctrl
value=1040+10000*Var(42)


[State -1, Atadura]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Atadura"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),480,600)
trigger1=ctrl
value=1050+10000*Var(42)


[State -1, Barrido]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Barrido"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),160,200)
trigger1=ctrl
value=1400+10000*Var(42)


[State -1, Lanzador]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Lanzador"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),240,300)
trigger1=ctrl
value=1410+10000*Var(42)


[State -1, Manto]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Manto"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),320,400)
trigger1=ctrl
value=1420+10000*Var(42)


[State -1, Agua]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Agua"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),160,200)
triggerall=command!="holddown"
trigger1=ctrl
value=1200+10000*Var(42)


[State -1, Marca]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Marca"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),200,250)
triggerall=command!="holddown"
trigger1=ctrl
value=IfElse(NumHelper(9600)>0,1211,1210)+10000*Var(42)


[State -1, Erupcion]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Erupcion"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),480,600)
trigger1=ctrl
value=1430+10000*Var(42)


[State -1, Emboscada]
type=ChangeState
triggerall=AILevel=0
triggerall=command="Emboscada"
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(42),480,600)
trigger1=ctrl
value=1440+10000*Var(42)


[State -1, Original uncloaked awakening]
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


[State -1, Three hit ground chain]
type=ChangeState
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

[State -1, Limited aerial chain]
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

[State -1, Three hit ground chain]
type=ChangeState
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

[State -1, Limited aerial chain]
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

[State -1, Three hit ground chain]
type=ChangeState
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

[State -1, Limited aerial chain]
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


[State -1, CPU legal special]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=3000
trigger1=P2BodyDist X<180
trigger1=Random<AILevel*3
triggerall=P2MoveType!=H
value=3000+10000*Var(42)


[State -1, CPU legal special]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=500
trigger1=P2BodyDist X<220
trigger1=Random<AILevel*3
triggerall=P2MoveType!=H
value=1030+10000*Var(42)


[State -1, CPU legal special]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=450
trigger1=P2BodyDist X<300
trigger1=Random<AILevel*3
triggerall=P2MoveType!=H
value=1020+10000*Var(42)


[State -1, CPU legal special]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=350
trigger1=P2BodyDist X<230
trigger1=Random<AILevel*3
triggerall=P2MoveType!=H
value=1000+10000*Var(42)


[State -1, CPU legal special]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=200
trigger1=P2BodyDist X<280
trigger1=Random<AILevel*3
triggerall=P2MoveType!=H
value=1200+10000*Var(42)


[State -1, CPU close chain]
type=ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X<65
triggerall=P2MoveType!=H
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

