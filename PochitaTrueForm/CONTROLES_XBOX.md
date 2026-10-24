# Controles físicos de Xbox

Correspondencia usada en el mando del proyecto: **X=a, Y=b, B=c, A=x, RB=y, RT=z, LB=s**. Son botones físicos distintos de las letras internas de MUGEN. El CMD no puede reasignar por sí solo un botón físico: si tu configuración global cambió, vuelve a asignarlo en las opciones de entrada del juego. Si tu mando todavía llama «Pausa» al botón que envía `s`, ese botón realiza la carga.

Adelante/atrás son relativos a la orientación: mirando a la derecha, adelante es →; mirando a la izquierda, adelante es ←. Se acepta abajo → diagonal → adelante/atrás y botón, o mantener la diagonal inferior y pulsar el botón.

| Entrada física | Movimiento | Energía |
|---|---|---:|
| Joystick izquierda/derecha | Caminar | 0 |
| Arriba / arriba diagonal | Saltar / saltar avanzando o retrocediendo | 0 |
| Abajo | Agacharse | 0 |
| Atrás / abajo+atrás | Guardia alta / baja | 0 |
| Adelante dos veces | Correr; X/Y/B permiten atacar desde carrera | 0 |
| Atrás dos veces | Retirada corta | 0 |
| Tres pulsaciones mezclando X/Y/B al acertar | Ruta de tres golpes; X final lanza, Y tritura, B derriba | 0 |
| X, X, X al conectar | Tres cortes y lanzamiento | 0 |
| Y, Y, Y al conectar | Extensión, triturado multigolpe y empuje | 0 |
| B, B, B al conectar | Giro, salto corto y remate contra el suelo | 0 |
| XXX y mantener arriba al acertar, luego X → Y → B en el aire | Perseguir el lanzamiento y rematar hacia el suelo | 0 |
| Tres pulsaciones mezclando X/Y/B en el aire | 27 rutas: X final lanza, Y tritura, B remata hacia abajo | 0 |
| Abajo+adelante+X | Desgarro: avance con tres cortes | 250 |
| Abajo+atrás+X | Cuatro brazos: cinco contactos | 350 |
| Abajo+X | Ascenso: corte que eleva al rival | 250 |
| Abajo+adelante+Y | Estocada con avance: cortes con motosierras normales | 350 |
| Abajo+atrás+Y | Barrido bajo de dos contactos | 250 |
| Abajo+Y | Guillotina: salto corto y corte descendente | 500 |
| Abajo+adelante+B | Embestida de tres impactos | 500 |
| Abajo+atrás+B | Carnicería: siete cortes y lanzamiento | 750 |
| Abajo+B | Rasante: corte bajo y derribo | 250 |
| RB | Guardia de motosierras y respuesta si recibe un golpe durante la ventana | 250 |
| RT | Asalto de cinco cortes con alcance extendido | 750 |
| Abajo + RB | Lazo intestinal: sujeta y deja un tambaleo breve para enlazar un normal | 350 |
| Abajo + RT | Sujeción intestinal y tres cortes de motosierras, con lanzamiento | 600 |
| Mantener LB / antiguo Pausa | Acelerar motores y cargar; soltar para detener | Carga hasta 3000 |
| Abajo + LB / antiguo Pausa | Despertar de 6 s, hasta 240 de curación y daño físico +20 %; exige barra llena | 1000 |
| Abajo + A | Devastación: antigua ultimate de cinco cortes, daño limitado al 25 % rival o 250 | 1000 |
| A | Devorar / borrado: apertura física, mordisco y desaparición temporal si conecta | 2000 |

1000 equivale a una barra. Sin la energía requerida para abajo+X/Y/B se ejecuta el normal agachado correspondiente. Los especiales ofensivos pueden cancelar un normal de suelo que haya conectado. Repetir el botón durante una guardia rival no concede automáticamente la continuación del combo. RB tiene aproximadamente 0,4 segundos de ventana activa, con preparación y recuperación; no refleja todo el daño ni asegura contras contra cualquier proyectil.

En el rediseño, Ascenso, Barrido y Rasante son de corta distancia. Las cajas de ataque se ajustaron a las motosierras visibles; no alcanzan al rival automáticamente desde lejos.

La ultimate consume **dos barras al activarla**, incluso si falla o la bloquean; exige 2000 de energía disponible. Su daño total es el menor entre 450 y el 45 % de la vida máxima del rival, redondeado hacia abajo. Un rival con vida completa sobrevive; uno ya herido puede morir. No hay daño de la secuencia al bloquear o esquivar la apertura.

Los remates de X/Y/B tienen cortes visibles, sangre al acertar y respuestas distintas: lanzamiento, triturado con empuje y golpe contra el suelo. En el muñeco de 1000 de vida las cadenas completas causan 152 / 180 / 205. Estos valores pueden variar con las defensas y reglas del rival.

## Rutas para empezar a jugar

- **X → Y → B**: corte rápido, extensión de motosierras y remate contra el suelo; 179 en el muñeco de prueba.
- **Y → B → X**: entrada fuerte, giro y lanzamiento; 173.
- **B → X → Y**: giro, corte y triturado; 185.
- **X → X → X + arriba, después X → Y → B en el aire**: persecución con salto real y corte descendente; 357 en seis impactos. Mantén arriba al conectar el último X; pulsa el X aéreo durante el salto. No es un teletransporte.
- **X → Y → abajo adelante X → abajo atrás X**: enlaza dos especiales diferentes; gasto total 600, daño 266 en el muñeco. El ejemplo cancela la primera técnica tras sus dos contactos iniciales; dejarla terminar ejecuta su tercer corte.

Puedes mezclar los tres botones en las tres etapas: son 27 secuencias que comparten ataques, no 27 animaciones diferentes. La pulsación del siguiente golpe se guarda durante el ataque y se ejecuta al acertar. Si fallas o te bloquean, la ruta se corta. Un golpe independiente tras recuperar control puede iniciar otra cadena.

Se permite **como máximo una segunda técnica especial en la misma secuencia**, siempre diferente de la actual, acertando y pagando su coste. Una tercera técnica se rechaza hasta recuperar control. Las continuaciones de especiales se ejecutan en suelo; Guillotina es un salto corto y no recibe nuevas cancelaciones mientras siga en el aire. La ulti conserva su entrada A y no se encadena automáticamente desde los normales.

## Sonido y destello de los seis especiales

Abajo adelante/atrás + X/Y/B inicia una preparación breve, destello rojo y sonido de activación; después sale la técnica. Se mantiene el mismo mapeo Xbox. Mirando a la derecha, abajo adelante es abajo → derecha y abajo atrás es abajo → izquierda; al cambiar de lado se invierten.

La señal debe escucharse aunque el ataque falle o sea bloqueado, siempre que haya energía suficiente. Usa un canal separado de la motosierra. No debe sonar al pulsar un normal ni al intentar el especial sin su energía mínima. La preparación paga el coste una sola vez: 250/350 para X, 350/250 para Y y 500/750 para B (adelante/atrás, respectivamente).

## Duración y remates de los seis especiales

Se ampliaron las secuencias de abajo adelante/atrás + X/Y/B, manteniendo costes y daño total. Tienen estelas animadas distintas, más contactos y recuperación visible. Carnicería conecta siete veces y termina lanzando al rival. Los destellos finales grandes, la vibración y el sonido de remate requieren acertar la secuencia; una guardia o un fallo no generan ese impacto confirmado.

Los seis especiales direccionales mantienen sus botones y costes. Los 24 cuadros nuevos son efectos; las secuencias combinan poses de cuerpo que ya existían.

## Despertar y nueva ultimate

Con tres barras, mantén abajo y pulsa LB (o el botón «Pausa» que envía `s` en tu configuración). Consume una barra, dura 360 ticks y cura hasta 240 sin exceder la vida máxima. Daño de ataques por colisión +20 % durante el efecto; las dos cinemáticas mantienen sus topes. No cambia el cuerpo ni su tamaño y no evita recibir golpes. Hay 900 ticks entre activaciones. Mantener el botón no lo renueva. Carga normal: LB sin abajo.

Abajo + A ejecuta ahora la antigua secuencia de cinco cortes por una barra. A sin abajo activa devorar/borrado por dos barras: debe conectar, daña hasta min(450, 45 % de la vida máxima rival) y quita hasta 500 de energía rival. La desaparición es temporal: el oponente vuelve al combate. Puedes fallar y te pueden bloquear o interrumpir la apertura. Las dos habilidades consumen su coste al iniciarse.

Abajo adelante + Y usa un avance físico y las motosierras normales de sus brazos, por 350 de energía. Se retiró la sierra gigante con cadena. Desgarro, Embestida y RT conservan su avance. Puedes bloquear, interrumpir o esquivar la estocada; desde lejos pueden fallar los cortes iniciales.

## Combos aéreos y bufanda intestinal

Salta y pulsa de nuevo X, Y o B al acertar: puedes repetir o mezclar los botones en las tres etapas. **XXX** aéreo causa 180 y lanza; **XYY** causa 200 con triturado de tres contactos en el último Y; **XYB** causa 205 y remata hacia abajo en el muñeco de 1000 de vida. Las 27 secuencias comparten nueve acciones, no son 27 animaciones dibujadas diferentes. No cuestan energía. Hay un máximo de tres ataques aéreos por vuelo: recuperar control en el aire no reinicia ese límite. Aterrizar o recibir un golpe lo reinicia. Un fallo o bloqueo no permite cancelar al siguiente ataque; puedes volver a atacar después de recuperar control si queda presupuesto del salto. El salto y la caída conservan física y las continuaciones dan un impulso corto al acertar.

**Abajo + RB (350)** extiende la bufanda roja de intestinos, sujeta al conectar y libera con 20 ticks de tambaleo; recuperas control cuatro ticks después de soltarlo, dejando una ventana para un normal. Daño inicial: 40. **Abajo + RT (600)** sujeta y remata con tres cortes, daño total 190 antes de las defensas particulares del rival; la parte de cortes usa daño fijo. Ambas aperturas son bloqueables, interrumpibles, de alcance limitado al dibujo y fallan contra un rival en el aire. No agarran automáticamente desde cualquier distancia. El rival recupera sus estados propios al terminar o si Pochita abandona el agarre. Sujete/remate son adaptaciones jugables del apéndice intestinal; no son nombres ni técnicas oficiales del manga. RB y RT sin abajo conservan sus movimientos anteriores.

## Acabado visual y sonoro

LB carga con poses y motores propios; al soltar, el motor desacelera. La carrera mueve la bufanda, y frenar o aterrizar muestra apoyo de los pies y polvo. Los cortes añaden estelas y chispas propias; los remates confirmados tienen sonido y una pausa más marcada. La victoria recoge y sacude las sierras antes de bajar los motores. Se conservan los comandos de esta tabla, incluidos los combos aéreos, abajo+RB/RT, despertar y A.


Consulta [la revisión conjunta](REVISION_CONJUNTA.md) para los cambios de recepción, animación y CPU.
