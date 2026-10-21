# Eida — Boruto: Two Blue Vortex

Carpeta para MUGEN 1.1 / Jump Force MUGEN V14. Copia `Eida` dentro de `chars/` y añade `Eida/Eida.def` en `[Characters]` de `data/select.def`. Sustituye la carpeta anterior por la nueva completa.

Consulta **CONTROLES_XBOX.md**: incluye 14 técnicas, rutas de combo, carga, despertar y Omnipotencia con A.

## Cambios de esta revisión

- 16 poses nuevas: cuatro de carga Senrigan, cuatro de carrera, dos de frenado, dos de aterrizaje y cuatro de victoria. La victoria usa la misma blusa y shorts del combate. Las nuevas poses de pie se calibran a los 68 píxeles del reposo; las poses comprimidas mantienen la escala de su hoja.
- Carrera con cabello en movimiento, apoyo de pies, frenado interrumpible y polvo que expira. Aterrizaje con compresión y recuperación; el salto conserva su altura.
- Carga LB con gesto del ojo, motas discretas y sonido continuo que se detiene al soltar, llenarse la barra o recibir un golpe. No agrega invulnerabilidad. El despertar conserva su cuerpo, tamaño y aura actuales.
- Nuevos impactos y remates de Eida/Daemon con fragmentos y sonido de contacto. Solo aparece el estallido final al acertar esa parte del ataque; un bloqueo o fallo no lo activa. Contadores separados evitan repetirlo durante hitpause o heredar el golpe anterior.
- Cuatro efectos no verbales nuevos: carga, liberación, remate y pisada. Las voces japonesas auténticas permanecen intactas.
- Victoria con gesto, cabello y pose final, énfasis temporal del escenario y margen de cámara. Se verifica después de ganar realmente por KO en una ronda de prueba, en ambas orientaciones.
- Se conservan todas las técnicas y sus costes, los combos, la limpieza de ayudantes y la recuperación del derribo. Daemon mantiene su cuerpo y tamaño. Omnipotencia mantiene ocho encuadres originales HD, apertura evadible, coste de tres barras y daño de 350.

### Correcciones y rutas conservadas

- Derribos corregidos: el impacto contra el suelo y el asentamiento tienen duración finita; el estado tumbado pasa automáticamente al levantarse cuando Eida sigue viva. El levantarse ajusta sus cajas al incorporarse.
- Nuevas rutas Y → X (ráfaga de Daemon), B → Y (launcher de Daemon) y abajo + Y → X (seguimiento de Daemon solo tras encanto confirmado, 250 de energía extra). Las dos primeras no gastan energía.
- Abajo + X permite salto de persecución hacia el rival y continuación aérea. También se puede perseguir el launcher normal de Daemon.
- Senrigan prepara un contraataque físico de Daemon: se retiró el daño directo de la observación. El encanto, el reflejo y Omnipotencia conservan reglas adaptadas al combate; no son una reproducción literal de habilidades activas del canon.
- Nuevas transiciones de poses para las rutas Y/X y B/Y, estelas cortas de movimiento para Daemon y el corazón, polvo de aparición y desaparición, y un sello pequeño de Senrigan en abajo + X. Se reutilizan los dibujos existentes.

- Corrección del error de la captura `Error parsing trigger2` en `Eida.cmd:304`: se sustituyeron las diez condiciones que combinaban un intervalo sin agrupar con `||` por grupos `trigger2` a `trigger8`, uno por estado permitido y siempre condicionado a `MoveHit`. Se mantienen las rutas de combo, los costes y los controles. La comprobación de regresión reproduce esa misma línea del ZIP anterior y la rechaza.
- Corrección de carga para MUGEN 1.1: los fundidos de Omnipotencia ahora usan `IfElse()` en lugar de `Min()`. Esta última es una extensión aceptada por Ikemen y puede impedir que MUGEN compile el personaje al seleccionarlo. La operación y la animación se conservan. El validador comprueba ahora las llamadas de las expresiones CNS/CMD; reproducir el fallo en el ZIP anterior forma parte de la comprobación de regresión. Esto no sustituye una ejecución en el MUGEN exacto del usuario.
- Omnipotencia reconstruida: ocho encuadres de los originales del manga a 1280×720, cámara suave, fundidos, sello de apertura, ambiente sonoro, transiciones y remate. Los originales se recortan y escalan; no se redibujaron ni se cambiaron sus caras.
- La apertura de la ulti debe conectar. Se puede bloquear, esquivar saltando o dejar fuera de alcance; en esos casos gasta las tres barras sin cinemática ni daño. Al conectar causa 350 de daño y libera al rival al terminar.
- Tres técnicas nuevas: abajo + A, doble encanto; abajo + RB, retroceso y respuesta de Senrigan; abajo + RT, apertura combinada con Daemon.
- Rutas mixtas X → Y → Y y X → B → B; continuaciones de Y/B y cancelaciones ofensivas aceptan pulsaciones durante las pausas de impacto.
- Salto neutral aumentado moderadamente: velocidad vertical de -6 a -7.1, con la misma gravedad. Apex medido de unas 49 unidades.
- Se conservan los sprites y el diseño de Daemon; esta revisión ajusta los tiempos y la recuperación de sus ataques.
- Segundo golpe de X: conserva la orientación hacia el rival; se eliminó el volteo horizontal del cuerpo completo.
- Enlace aéreo X → Y → B corregido según los botones físicos del mando, con memoria de la pulsación durante las pausas de impacto.
- Corazón visible sobre la cabeza del rival únicamente después de confirmar Encantamiento. No agrega daño ni prolonga el aturdimiento.
- Dash con dos toques hacia delante, interrumpible con salto o ataque y sin invulnerabilidad. Ahora usa un ciclo de carrera propio y una transición de frenado.
- Aura del despertar: 13 cuadros del efecto de energía de la referencia Nezuko, con color azul y mezcla aditiva del motor. Mantiene los sprites normales de Eida y evita el arco rígido anterior.
- Daemon: sprites reducidos al 68% del tamaño anterior, colisiones ajustadas, aparición junto a Eida, carrera con alcance limitado, ataques a corta distancia y desaparición gradual. Se puede interrumpir golpeándolo o golpeando a Eida.
- Catorce técnicas con consumo de energía y entradas físicas de Xbox. Los controles se invierten de acuerdo con la orientación.
- Cadenas normales en X, Y y B; launcher con Daemon y continuaciones aéreas.
- Encantamiento rasante y ascendente con colisión, bloqueo, alcance finito y aturdimiento de 45 ticks.
- Sonidos de aparición, desplazamiento, guardia, lanzamientos e impactos; chispas y polvo del combate.
- Estados en `Specials.cns` y `Omnipotencia.cns`, referenciados en `Eida.def`. Conservar ambos archivos junto con los demás.

## Comprobaciones

- SFF v2.0.1.0: 194 sprites; los ocho paneles conservan 1280×720 dentro del archivo. Retrato de combate 25×25 y retrato de selección 120×140.
- SND: 30 muestras mono PCM de 16 bits, incluidos tres efectos nuevos de la cinemática.
- AIR: 123 acciones con referencias válidas. El idle usa exclusivamente sus seis cuadros de reposo.
- 124 estados en cuatro CNS; referencias estáticas de estados, animaciones locales y sonidos verificadas.
- 95 escenarios en Ikemen GO con entradas y colisiones reales: 80 de movimiento/técnicas/combos, 6 de derribos y recuperación, y 9 de ultimate. Barrido, rebote y caída aérea se comprueban en ambas orientaciones: recibe daño, cae, se levanta y vuelve a atacar. Además, 22 pruebas de presentación y dos victorias reales comprueban la revisión; cinco pruebas de regresión del validador cubren los errores de carga previos, el impacto infinito y el flag de victoria inválido.
- Las pruebas cubren técnicas, rutas mixtas, enlaces durante hitpause, salto, costes, ayudas que pueden fallar y apertura de ultimate bloqueada, esquivada o fuera de alcance. Informes reproducibles en `previews/engine_moveset_checks.json` y `previews/engine_ultimate_checks.json` y `previews/engine_recovery_checks.json` del repositorio.

Las pruebas del motor usan copias temporales e instrumentación fuera de la carpeta entregada. No se pudo ejecutar el binario exacto de Jump Force MUGEN V14 del usuario ni comprobar físicamente su mando Xbox. El equilibrio frente a todo su plantel requiere partidas locales.

## Procedencia y límites visuales

Eida conserva los sprites recuperados de los recursos del usuario y los cuadros adicionales de movimiento. Daemon usa las 16 poses reconstruidas anteriormente, ahora a escala de ayudante. Se conservan las seis poses de apoyo anteriores; esta revisión añade 16 poses y doce cuadros de efectos generados con IA a partir del aspecto de los sprites actuales. Los dibujos de Daemon se conservan. El resto de las animaciones de Eida conserva el material previo. El nivel artístico de Sumire sigue siendo la referencia de acabado y no se declara alcanzado.

Omnipotencia conserva los paneles originales del manga. Las voces pertenecen a los fragmentos femeninos del MP3 japonés suministrado. Consulta `CREDITOS_Y_FUENTES.md`.

El nuevo video `Eida_ACABADO.mp4` captura imágenes y audio real SDL de Ikemen GO a 44100 Hz estéreo; se sincroniza por correlación con las muestras del SND, sin mezcla de efectos fuera del motor. El MP4 antiguo de Omnipotencia usa audio mezclado fuera del motor y representa la revisión anterior de esa cinemática.
