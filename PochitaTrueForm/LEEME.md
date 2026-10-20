# Pochita True Form — combos y remates para MUGEN 1.1

Sustituye `chars/PochitaTrueForm` completa por la carpeta de `PochitaTrueForm_SIN_SIERRA_GIGANTE.zip`. Agrega `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si todavía no está. Reinicia el juego.

## Corrección de carga en MUGEN

Se corrigió el error «Need at least one state controller» de los estados 170, 175 y 180. Son poses de final de ronda que ahora contienen un controlador `Null` válido, sin alterar los ataques. El constructor incluye la corrección y el validador rechaza cualquier estado sin controladores en CNS o CMD. Cinco pruebas de regresión reproducen y rechazan estados vacíos; otra rechaza grupos de triggers con saltos de numeración; las 221 pruebas de combate de Ikemen GO volvieron a pasar. El ZIP se valida también después de extraerlo. No se ejecutó el binario exacto de MUGEN del usuario.

## Despertar regenerativo

Mantén abajo y pulsa el botón que carga energía (LB físico, interno `s`; «Pausa» en el mapeo anterior). Exige las tres barras llenas, consume una y activa 360 ticks de regeneración, aproximadamente seis segundos de juego activo. Cura cuatro puntos cada seis ticks: hasta 240 en total, sin exceder 1250 de vida. No revive al morir. Durante el efecto, los ataques que calculan daño por HitDef tienen multiplicador 1,20; las cinemáticas conservan sus límites fijos.

El cuerpo, sus animaciones y su escala permanecen iguales. Se ven brasas rojas bajas en un efecto independiente. Puedes caminar, saltar y atacar tras la preparación de 24 ticks; puedes recibir golpes también. La curación no concede invulnerabilidad. Hay 900 ticks de espera entre activaciones, unos 15 segundos desde el inicio, y hace falta volver a llenar la barra. Mantener el botón no repite el despertar. Para cargar normalmente, mantén LB sin abajo.

## Abajo + A: Devastación

La ultimate anterior de cinco cortes pasa a abajo + A físico (interno `x`). Consume 1000 al activarla, incluso si falla. La apertura sigue siendo bloqueable, esquivable y de alcance físico. Al acertar realiza la animación de cinco cortes, con daño máximo igual al menor entre 250 y el 25 % de la vida máxima rival. No dispara la nueva ultimate cuando se pulsa abajo + A, tampoco si falta energía.

## Seis especiales con presentación de activación

Abajo adelante/atrás + X/Y/B conserva las seis técnicas y sus costes. Se añade una pose de preparación, oscurecimiento del escenario, destello rojo horizontal y el sonido de activación en un canal separado de la motosierra. La preparación dura 12 ticks (0,2 segundos); en la segunda técnica enlazada dura 6 ticks. Tras esa pausa salen las animaciones y colisiones del ataque, con un pulso dentado de suelo. No se genera daño durante el destello.

El coste se paga una sola vez al activar la preparación, incluso si después fallas o te bloquean. Sin energía suficiente no hay preparación ni sonido de especial. La presentación no concede invulnerabilidad y los efectos terminan automáticamente o se retiran al recibir un golpe. La nueva ultimate con A consume dos barras y tiene el límite de daño descrito más abajo.

El video de Goku enviado por el usuario se usó como referencia de pose/oscurecimiento/destello. No se copiaron voces, rayos ni transformaciones de Goku. El SE separado procede de Code, grupo 950,2, usado por su código como Super Charge, convertido y ajustado de volumen. No se presenta como una extracción exacta del sonido mezclado del video.

## Especiales más largos y efectos propios

Las seis técnicas adelante/atrás tienen secuencias ampliadas con poses de cuerpo existentes y 24 cuadros nuevos de efectos: arcos dentados, cuatro cortes cruzados, estela de estocada, polvo del barrido, estela de embestida y remate cruzado. No se añadieron poses nuevas de cuerpo en esta revisión. Los efectos siguen las hojas de las motosierras; el alcance de colisión sigue limitado al dibujo del arma.

| Técnica | Contactos | Animación sin pausas | Daño total | Energía |
|---|---:|---:|---:|---:|
| Desgarro | 3 | 57 ticks | 106 | 250 |
| Cuatro brazos | 5 | 66 ticks | 132 | 350 |
| Estocada con avance | 3 | 56 ticks | 126 | 350 |
| Barrido | 2 | 56 ticks | 96 | 250 |
| Embestida | 3 | 60 ticks | 145 | 500 |
| Carnicería | 7 | 90 ticks | 218 | 750 |

60 ticks equivalen a un segundo. La preparación y las pausas de impacto se suman a esos tiempos; los videos se reproducen a velocidad normal. El daño total se redistribuye entre los nuevos contactos, sin aumentar el coste. Avanza mediante velocidad y colisiones físicas. El golpe final confirmado tiene otro pulso visual, sonido y vibración breve; fallar o ser bloqueado no muestra ese impacto confirmado. Las estelas del movimiento sí aparecen al atacar sin acertar.

Abajo adelante + Y vuelve a usar el cuerpo y las motosierras de tamaño normal. Se retiró el arma gigante con cadena porque el usuario la rechazó como ajena a su referencia del personaje. El alcance proviene de un avance de Pochita; no hay una hoja alargada ni colisiones de 220 unidades desde una posición fija. Los primeros cortes pueden fallar desde lejos. Se verifican aproximación desde 200, fallo desde 280, bloqueo e interrupción. Desgarro, Embestida y RT conservan sus avances físicos.

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

Las continuaciones requieren acertar y volver a pulsar el botón. Bloquear o estar fuera de alcance corta la cadena. Los especiales ofensivos pueden cancelar un normal de suelo confirmado. Los nombres de movimientos son descripciones de adaptaciones físicas, no nombres oficiales de técnicas del manga. El borrado conceptual se representa mediante la adaptación temporal descrita más abajo; la regeneración tiene duración y cantidad limitadas.

## A: Devorar y borrado conceptual, adaptación de combate

**Consume 2000 al activarla, incluso si falla o la bloquean.** Con menos de dos barras no se ejecuta. No se activa con abajo mantenido: ese comando corresponde a Devastación. La apertura avanza por el suelo y tiene que colisionar. Bloquearla, saltarla, alejarse o golpear a Pochita durante su preparación evita la cinemática y el daño.

Al acertar usa ocho poses nuevas: acecho, aproximación, apertura de mandíbula, mordisco, masticación, deglución y recuperación. El rival conserva su propio sprite de daño, se contrae, desaparece brevemente entre fragmentos de tinta y vuelve al escenario para caer y recuperar control. Hay sangre estilizada en los mordiscos, una pausa visual blanca y efectos de cierre; no hay un panel del manga ni un retrato sustituyendo la animación. La captura confirmada protege la cinemática; no da invulnerabilidad a la apertura.

El daño total es el menor entre **450 y el 45 % de la vida máxima del rival**, redondeado hacia abajo. Contra 1000 causa 450; contra 500 causa 225. Un enemigo con vida completa sobrevive. Puede rematar a uno previamente herido. Quita hasta 500 de energía rival, sin dejar su barra negativa. El despertar no multiplica estos daños fijos.

En el manga, devorar demonios puede borrar conceptos de la existencia. Aquí se representa esa idea con devorar, una ausencia temporal y pérdida de energía. **No se borran permanentemente personajes, conceptos, nombres, recuerdos, archivos ni comandos del oponente.** Se trata de una adaptación jugable: el rival reaparece y sigue combatiendo. La regeneración automática de abajo+carga también es una adaptación con límites, no curación infinita.

## Arte y audio

Armadura negra robusta, casco dentado, cuatro brazos con motosierras y bufanda intestinal roja, según las referencias del usuario. Se generaron con IA las hojas de movimiento, ataques, daño y los nuevos remates. El SFF contiene 213 entradas: 155 de cuerpo (146 poses fuente distintas), 56 efectos y dos retratos estándar. Las repeticiones cierran ciclos y comparten movimientos. El reposo conserva seis cuadros propios. El tamaño del cuerpo permanece calibrado al reposo de 72 píxeles; no se estiran individualmente los cuadros. Las cajas ofensivas siguen las motosierras visibles.

Hay catorce sonidos no verbales: siete muestras del DENJI suministrado, tres mezclas adicionales de motores/cortes/impactos y el SE de activación del Code suministrado, más tres mezclas nuevas para mordisco, borrado y regeneración. No se incluyen voces humanas ni voces generadas. Las hojas fuente, ejes y procedencia están en el repositorio. El arte generado conserva pequeñas variaciones de detalle entre cuadros; necesita revisión artística para alcanzar la consistencia de dibujo manual cuadro por cuadro.

## Comprobaciones y prueba local

Pasaron 221 escenarios generales de entradas y colisiones en Ikemen GO, 46 casos específicos de despertar, alcance y Devastación, una prueba de CPU, cuatro pruebas de daños limitados frente a 500 de vida y una prueba de KO sin resurrección. Se verifican curación exacta, tope de vida, espera, botón mantenido, ataques durante el despertar, multiplicador que termina, falta de energía, apertura interrumpida y liberación si el atacante abandona la escena. El validador comprueba sprites, sonidos, sintaxis nativa, recuperación, controladores y alcance visible. Las regresiones de carga MUGEN y reconstrucción se mantienen.

Los MP4 nuevos `Pochita_despertar_nuevo_motor.mp4`, `Pochita_borrado_nuevo_motor.mp4`, `Pochita_devastacion_nuevo_motor.mp4` y `Pochita_estocada_nuevo_motor.mp4` y la demostración combinada contienen audio real SDL del mezclador de Ikemen GO. La señal se sincroniza por correlación con las muestras del SND. Los videos anteriores representan versiones anteriores; algunos usan audio montado por eventos. No se ejecutó el binario exacto de Jump Force MUGEN V14 ni se conectó el mando físico. La calidad artística y el equilibrio requieren revisión y partidas locales.

Prueba en tu juego: caminar, agacharse, saltar; X/Y/B tres veces mezclando botones al conectar; XXX-arriba-X-Y-B en el aire; dos especiales seguidos; especiales; RB ante un golpe; RT; cargar con LB. Con la barra llena, prueba abajo+LB: una activación, seis segundos, curación limitada y mismo tamaño. Prueba abajo+A acertada, bloqueada y desde lejos: gasta una barra. Usa A acertada, bloqueada y desde lejos: siempre gasta dos barras si se activa. Con menos de dos barras no debe salir. Recibe un barrido y un lanzamiento: debe levantarse y volver a atacar. Repite mirando hacia ambos lados. Si A o LB no coinciden, revisa el mapeo global antes de modificar el CMD. Consulta `CONTROLES_XBOX.md`.
