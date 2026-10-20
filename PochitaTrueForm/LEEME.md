# Pochita True Form — combos y remates para MUGEN 1.1

Sustituye `chars/PochitaTrueForm` completa por la carpeta de `PochitaTrueForm_ESPECIALES_LARGOS.zip`. Agrega `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si todavía no está. Reinicia el juego.

## Corrección de carga en MUGEN

Se corrigió el error «Need at least one state controller» de los estados 170, 175 y 180. Son poses de final de ronda que ahora contienen un controlador `Null` válido, sin alterar los ataques. El constructor incluye la corrección y el validador rechaza cualquier estado sin controladores en CNS o CMD. Cinco pruebas de regresión reproducen y rechazan estados vacíos; otra rechaza grupos de triggers con saltos de numeración; las 217 pruebas de combate de Ikemen GO volvieron a pasar. El ZIP se valida también después de extraerlo. No se ejecutó el binario exacto de MUGEN del usuario.

## Seis especiales con presentación de activación

Abajo adelante/atrás + X/Y/B conserva las seis técnicas y sus costes. Se añade una pose de preparación, oscurecimiento del escenario, destello rojo horizontal y el sonido de activación en un canal separado de la motosierra. La preparación dura 12 ticks (0,2 segundos); en la segunda técnica enlazada dura 6 ticks. Tras esa pausa salen las animaciones y colisiones del ataque, con un pulso dentado de suelo. No se genera daño durante el destello.

El coste se paga una sola vez al activar la preparación, incluso si después fallas o te bloquean. Sin energía suficiente no hay preparación ni sonido de especial. La presentación no concede invulnerabilidad y los efectos terminan automáticamente o se retiran al recibir un golpe. La ultimate con A conserva su coste de dos barras y su límite de daño.

El video de Goku enviado por el usuario se usó como referencia de pose/oscurecimiento/destello. No se copiaron voces, rayos ni transformaciones de Goku. El SE separado procede de Code, grupo 950,2, usado por su código como Super Charge, convertido y ajustado de volumen. No se presenta como una extracción exacta del sonido mezclado del video.

## Especiales más largos y efectos propios

Las seis técnicas adelante/atrás tienen secuencias ampliadas con poses de cuerpo existentes y 24 cuadros nuevos de efectos: arcos dentados, cuatro cortes cruzados, estela de estocada, polvo del barrido, estela de embestida y remate cruzado. No se añadieron poses nuevas de cuerpo en esta revisión. Los efectos siguen las hojas de las motosierras; el alcance de colisión sigue limitado al dibujo del arma.

| Técnica | Contactos | Animación sin pausas | Daño total | Energía |
|---|---:|---:|---:|---:|
| Desgarro | 3 | 57 ticks | 106 | 250 |
| Cuatro brazos | 5 | 66 ticks | 132 | 350 |
| Estocada | 3 | 56 ticks | 126 | 350 |
| Barrido | 2 | 56 ticks | 96 | 250 |
| Embestida | 3 | 60 ticks | 145 | 500 |
| Carnicería | 7 | 90 ticks | 218 | 750 |

60 ticks equivalen a un segundo. La preparación y las pausas de impacto se suman a esos tiempos; los videos se reproducen a velocidad normal. El daño total se redistribuye entre los nuevos contactos, sin aumentar el coste. Avanza mediante velocidad y colisiones físicas. El golpe final confirmado tiene otro pulso visual, sonido y vibración breve; fallar o ser bloqueado no muestra ese impacto confirmado. Las estelas del movimiento sí aparecen al atacar sin acertar.

El video de Chainsaw Man enviado por el usuario (29,84 s) se revisó visualmente: preparación, avance de triturado con 22 contactos en la referencia, derribo y otra secuencia giratoria. Sirve de referencia de ritmo y separación entre preparación, ataque y remate. Pochita tiene las seis secuencias descritas arriba; no reproduce literalmente esa combinación de 22 contactos ni la invocación de la cabeza gigante. El audio del video no se evaluó por escucha en este entorno.

## Rutas nuevas

Pulsar tres veces X/Y/B permite mezclar botones, por ejemplo X-Y-B, Y-B-X y B-X-Y. Son 27 secuencias que comparten nueve ataques; el último X lanza, Y tritura y B remata contra el suelo. La continuación requiere acertar y pulsar, con entrada guardada durante el golpe. Al bloquear o fallar se corta la ruta.

XXX, arriba al acertar el lanzamiento, X-Y-B en el aire permite perseguir con un salto real y terminar con un corte descendente. La prueba conecta seis impactos y causa 324 sobre 1000 de vida; el rival no se congela ni se teletransporta. X-Y, abajo adelante X, abajo atrás X conecta normales y dos especiales por 600 de energía, causando 266 en el muñeco. La segunda técnica debe ser diferente y acertar la anterior; una tercera se rechaza durante la secuencia. Las técnicas aéreas no admiten esta cancelación de suelo.

Se añadieron doce poses para persecución, embestida RT y remate aéreo, con escala compartida. Los cortes iniciales también muestran efectos al acertar. Las pruebas incluyen todas las cadenas mixtas en ambas orientaciones, la persecución con física libre, el límite de especiales con una tercera entrada reconocida y los fallos/bloqueos sin cancelación ni sangre.

## Cambios jugables

- X → X → X: tres cortes y lanzamiento del rival, 152 de daño en el muñeco de prueba.
- Y → Y → Y: extensión, triturado multigolpe y empuje, 180 de daño.
- B → B → B: giro, salto corto y corte contra el suelo, 217 de daño.
- X → Y → B en el aire: cadena con derribo, 172 de daño.
- Nueve especiales direccionales entre 250 y 750 de energía; RB cuesta 250 y RT 750. Cada barra equivale a 1000.
- Vida 1250, defensa 110, carga con LB de 18 unidades por tick hasta 3000. Los combos normales generan energía al conectar.

Las continuaciones requieren acertar y volver a pulsar el botón. Bloquear o estar fuera de alcance corta la cadena. Los especiales ofensivos pueden cancelar un normal de suelo confirmado. Los nombres de movimientos son descripciones de adaptaciones físicas, no nombres oficiales de técnicas del manga. No se implementa el borrado permanente de conceptos ni regeneración ilimitada.

## Ultimate con A

**Consume 2000 al activarla, incluso si falla o la bloquean.** Con menos de dos barras no se ejecuta. La embestida debe conectar; bloquear, saltar o quedarse fuera de alcance evita la secuencia y su daño. Tiene preparación y recuperación vulnerables al fallar.

Al acertar usa ocho poses nuevas: despliegue de los cuatro brazos, cortes cruzados, barrido y remate final. Cinco contactos sincronizan motosierras, arcos de corte, sangre, pausas de impacto y lanzamiento. La imagen del manga fue una referencia de acción y no se muestra en el ataque.

El daño total se limita al menor entre **500 y el 50 % de la vida máxima del rival**, redondeado hacia abajo. Un rival con 1000 de vida recibe 500; uno con 500 recibe 250. La ultimate sola no mata desde la vida completa. Puede rematar a alguien previamente herido. La secuencia libera al rival y ambos vuelven a sus estados normales.

## Arte y audio

Armadura negra robusta, casco dentado, cuatro brazos con motosierras y bufanda intestinal roja, según las referencias del usuario. Se generaron con IA las hojas de movimiento, ataques, daño y los nuevos remates. El SFF contiene 193 entradas: 147 de cuerpo (138 poses fuente distintas), 44 efectos y dos retratos estándar. Las repeticiones cierran ciclos y comparten movimientos. El reposo conserva seis cuadros propios. El tamaño del cuerpo permanece calibrado al reposo de 72 píxeles; no se estiran individualmente los cuadros. Las cajas ofensivas siguen las motosierras visibles.

Hay once sonidos no verbales: siete muestras del DENJI suministrado, tres mezclas adicionales de motores/cortes/impactos y el SE de activación del Code suministrado. No se incluyen voces humanas ni voces generadas. Las hojas fuente, ejes y procedencia están en el repositorio. El arte generado conserva pequeñas variaciones de detalle entre cuadros; necesita revisión artística para alcanzar la consistencia de dibujo manual cuadro por cuadro.

## Comprobaciones y prueba local

Pasaron 217 escenarios de entradas y colisiones en Ikemen GO, una prueba de CPU y dos pruebas de ultimate contra un rival de solo 500 de vida. Se comprueban los costes exactos, presupuesto mínimo, cadenas X/Y/B, bloqueos y fallos, nueve especiales, atajos diagonales, defensa, movimiento, salto, carga, seis derribos con recuperación y ultimate acertada, bloqueada, saltada y fuera de alcance en ambas orientaciones. Los efectos de impacto aparecen al acertar y expiran; la sangre no aparece al bloquear. El destello de activación sí aparece al ejecutar el especial, incluso si después falla. Se comprueban doce casos de energía insuficiente y doce de especiales fallados desde lejos, en ambas orientaciones. Se comprueban también doce bloqueos de los seis especiales, duración completa, número exacto de contactos y daño de cada secuencia. Se grabaron los seis especiales ampliados con audio real y se verificó la presencia de su SE mediante correlación con la muestra empaquetada. El validador revisa SFF/SND, referencias, funciones de MUGEN 1.1, recuperación finita y alcance visible; una regresión confirma que rechaza una caja ofensiva exagerada.

Los GIF y fotogramas proceden del motor real. Los MP4 nuevos `Pochita_largo_especial_*_motor.mp4` y `Pochita_ESPECIALES_LARGOS_Y_EFECTOS.mp4` contienen salida real del mezclador de Ikemen GO, capturada con el controlador SDL a disco. Se sincronizan con las imágenes identificando la muestra de activación en la grabación. Los videos anteriores de remates/jugabilidad conservan audio montado a partir de eventos; son pruebas distintas. Las entradas automáticas se aplican solo a copias de prueba. No se ha ejecutado el binario exacto de Jump Force MUGEN V14 ni conectado el mando físico a este entorno. El equilibrio contra todo el plantel requiere partidas locales.

Prueba en tu juego: caminar, agacharse, saltar; X/Y/B tres veces mezclando botones al conectar; XXX-arriba-X-Y-B en el aire; dos especiales seguidos; especiales; RB ante un golpe; RT; cargar con LB. Usa A acertada, bloqueada y desde lejos: siempre gasta dos barras si se activa. Con menos de dos barras no debe salir. Recibe un barrido y un lanzamiento: debe levantarse y volver a atacar. Repite mirando hacia ambos lados. Si A o LB no coinciden, revisa el mapeo global antes de modificar el CMD. Consulta `CONTROLES_XBOX.md`.
