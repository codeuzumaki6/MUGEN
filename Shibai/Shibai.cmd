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
name="Vendaval"
command=~D,DF,F,a
time=20
buffer.time=4

[Command]
name="Vendaval"
command=~D,F,a
time=20
buffer.time=4

[Command]
name="Vendaval"
command=/DF,a
time=20
buffer.time=4

[Command]
name="Ciclon"
command=~D,DB,B,a
time=20
buffer.time=4

[Command]
name="Ciclon"
command=~D,B,a
time=20
buffer.time=4

[Command]
name="Ciclon"
command=/DB,a
time=20
buffer.time=4

[Command]
name="Estacas"
command=~D,DF,F,b
time=20
buffer.time=4

[Command]
name="Estacas"
command=~D,F,b
time=20
buffer.time=4

[Command]
name="Estacas"
command=/DF,b
time=20
buffer.time=4

[Command]
name="Cubos"
command=~D,DB,B,b
time=20
buffer.time=4

[Command]
name="Cubos"
command=~D,B,b
time=20
buffer.time=4

[Command]
name="Cubos"
command=/DB,b
time=20
buffer.time=4

[Command]
name="Tormenta"
command=~D,DF,F,c
time=20
buffer.time=4

[Command]
name="Tormenta"
command=~D,F,c
time=20
buffer.time=4

[Command]
name="Tormenta"
command=/DF,c
time=20
buffer.time=4

[Command]
name="Repulsion"
command=~D,DB,B,c
time=20
buffer.time=4

[Command]
name="Repulsion"
command=~D,B,c
time=20
buffer.time=4

[Command]
name="Repulsion"
command=/DB,c
time=20
buffer.time=4

[Command]
name="RafagaBaja"
command=/D,a
time=20
buffer.time=4

[Command]
name="EstacasBajas"
command=/D,b
time=20
buffer.time=4

[Command]
name="Descarga"
command=/D,c
time=20
buffer.time=4

[Command]
name="Reflejo"
command=y
time=20
buffer.time=1

[Command]
name="Garra"
command=z
time=20
buffer.time=1

[Command]
name="Senrigan"
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

[State -1, Vendaval]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Vendaval"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,180,300)
trigger1 = ctrl
value=1000

[State -1, Ciclon]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Ciclon"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,270,450)
trigger1 = ctrl
value=1010

[State -1, Estacas]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Estacas"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,240,400)
trigger1 = ctrl
value=1020

[State -1, Cubos]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Cubos"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,330,550)
trigger1 = ctrl
value=1030

[State -1, Tormenta]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Tormenta"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,330,550)
trigger1 = ctrl
value=1040

[State -1, Repulsion]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Repulsion"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,390,650)
trigger1 = ctrl
value=1050

[State -1, RafagaBaja]
type = ChangeState
triggerall = AILevel=0
triggerall = command="RafagaBaja"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,150,250)
trigger1 = ctrl
value=1400

[State -1, EstacasBajas]
type = ChangeState
triggerall = AILevel=0
triggerall = command="EstacasBajas"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,210,350)
trigger1 = ctrl
value=1410

[State -1, Descarga]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Descarga"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,240,400)
trigger1 = ctrl
value=1420

[State -1, Reflejo]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Reflejo"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,270,450)
triggerall = command != "holddown"
trigger1 = ctrl
value=1200

[State -1, Garra]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Garra"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,180,300)
triggerall = command != "holddown"
trigger1 = ctrl
value=IfElse(NumHelper(9600)>0,1211,1210)

[State -1, Senrigan]
type = ChangeState
triggerall = AILevel=0
triggerall = command="Senrigan"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,300,500)
trigger1 = ctrl
value=1430

[State -1, SalidaGarra]
type = ChangeState
triggerall = AILevel=0
triggerall = command="SalidaGarra"
triggerall = StateType!=A
triggerall = Power>=IfElse(Var(40)>0,390,650)
trigger1 = ctrl
value=1440

[State -1, Awakening down plus Pause]
type = ChangeState
triggerall = AILevel=0
triggerall = command="s"
triggerall = command="holddown"
triggerall = Power>=3000
triggerall = Var(40)=0
triggerall = Var(41)=0
trigger1 = ctrl
trigger1 = StateType!=A
value=520

[State -1, Xbox A ultimate]
type = ChangeState
triggerall = AILevel=0
triggerall = command="x"
triggerall = Power>=3000
triggerall = StateType!=A
trigger1=ctrl
value=3000

[State -1, Hold Pause to charge]
type = ChangeState
triggerall = AILevel=0
triggerall = command="hold_s"
triggerall = command!="holddown"
triggerall = Power<3000
triggerall = StateType!=A
trigger1=ctrl
value=500

[State -1, Wind combo continuation]
type = ChangeState
triggerall = AILevel=0
triggerall = command="a"
triggerall = StateType!=A
triggerall = command!="holddown"
trigger1 = ctrl
trigger2 = StateNo=200 || StateNo=210 || StateNo=220
trigger2 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger2 = Time>=8
trigger3 = StateNo=201 || StateNo=211 || StateNo=221
trigger3 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger3 = Time>=8
value=200+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause=1

[State -1, Finite aerial wind chain]
type = ChangeState
triggerall = AILevel=0
triggerall = command="a"
triggerall = StateType=A
triggerall = Var(12)<3
trigger1=ctrl
trigger2 = StateNo>=600 && StateNo<=622
trigger2 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger2 = Time>=8
value=600+Var(12)
ignorehitpause=1

[State -1, Wind combo continuation]
type = ChangeState
triggerall = AILevel=0
triggerall = command="b"
triggerall = StateType!=A
triggerall = command!="holddown"
trigger1 = ctrl
trigger2 = StateNo=200 || StateNo=210 || StateNo=220
trigger2 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger2 = Time>=8
trigger3 = StateNo=201 || StateNo=211 || StateNo=221
trigger3 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger3 = Time>=8
value=210+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause=1

[State -1, Finite aerial wind chain]
type = ChangeState
triggerall = AILevel=0
triggerall = command="b"
triggerall = StateType=A
triggerall = Var(12)<3
trigger1=ctrl
trigger2 = StateNo>=600 && StateNo<=622
trigger2 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger2 = Time>=8
value=610+Var(12)
ignorehitpause=1

[State -1, Wind combo continuation]
type = ChangeState
triggerall = AILevel=0
triggerall = command="c"
triggerall = StateType!=A
triggerall = command!="holddown"
trigger1 = ctrl
trigger2 = StateNo=200 || StateNo=210 || StateNo=220
trigger2 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger2 = Time>=8
trigger3 = StateNo=201 || StateNo=211 || StateNo=221
trigger3 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger3 = Time>=8
value=220+IfElse(ctrl,0,IfElse(StateNo=200 || StateNo=210 || StateNo=220,1,2))
ignorehitpause=1

[State -1, Finite aerial wind chain]
type = ChangeState
triggerall = AILevel=0
triggerall = command="c"
triggerall = StateType=A
triggerall = Var(12)<3
trigger1=ctrl
trigger2 = StateNo>=600 && StateNo<=622
trigger2 = ProjHitTime(StateNo)>=0 && ProjHitTime(StateNo)<12
trigger2 = Time>=8
value=620+Var(12)
ignorehitpause=1

[State -1, FF]
type = ChangeState
triggerall=AILevel=0
triggerall=command="FF"
triggerall=StateType=S
trigger1=ctrl
value=100

[State -1, BB]
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
triggerall=Power>=IfElse(Var(40)>0,1800,3000)
trigger1=P2BodyDist X<200
trigger1=Random<8+AILevel*2
value=3000

[State -1, CPU legal technique]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,330,550)
trigger1=P2BodyDist X<240
trigger1=Random<8+AILevel*2
value=1040

[State -1, CPU legal technique]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
triggerall=Power>=IfElse(Var(40)>0,180,300)
trigger1=P2BodyDist X<180
trigger1=Random<8+AILevel*2
value=1000

[State -1, CPU wind normal]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X<150
value=200

[State -1, CPU approach]
type = ChangeState
triggerall=AILevel>0
triggerall=RoundState=2
triggerall=ctrl
triggerall=StateType!=A
trigger1=P2BodyDist X>=150
value=20
ctrl=1
