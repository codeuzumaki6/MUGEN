# Eida — Boruto: Two Blue Vortex

Carpeta para MUGEN 1.1 / Jump Force MUGEN V14. Copia `Eida` dentro de `chars/` y añade `Eida/Eida.def` en `[Characters]` de `data/select.def`. Sustituye la carpeta anterior por la nueva completa.

Consulta **CONTROLES_XBOX.md**: incluye 14 técnicas, rutas de combo, carga, despertar y Omnipotencia con A.

## Cambios de esta revisión

- Corrección de carga para MUGEN 1.1: los fundidos de Omnipotencia ahora usan `IfElse()` en lugar de `Min()`. Esta última es una extensión aceptada por Ikemen y puede impedir que MUGEN compile el personaje al seleccionarlo. La operación y la animación se conservan. El validador comprueba ahora las llamadas de las expresiones CNS/CMD; reproducir el fallo en el ZIP anterior forma parte de la comprobación de regresión. Esto no sustituye una ejecución en el MUGEN exacto del usuario.
- Omnipotencia reconstruida: seis encuadres de los originales del manga a 1280×720, cámara suave, fundidos, sello de apertura, ambiente sonoro, transiciones y remate. Los originales se recortan y escalan; no se redibujaron ni se cambiaron sus caras.
- La apertura de la ulti debe conectar. Se puede bloquear, esquivar saltando o dejar fuera de alcance; en esos casos gasta las tres barras sin cinemática ni daño. Al conectar causa 350 de daño y libera al rival al terminar.
- Tres técnicas nuevas: abajo + A, doble encanto; abajo + RB, retroceso y respuesta de Senrigan; abajo + RT, apertura combinada con Daemon.
- Rutas mixtas X → Y → Y y X → B → B; continuaciones de Y/B y cancelaciones ofensivas aceptan pulsaciones durante las pausas de impacto.
- Salto neutral aumentado moderadamente: velocidad vertical de -6 a -7.1, con la misma gravedad. Apex medido de unas 49 unidades.
- Los sprites y los estados ofensivos de Daemon se mantienen; no se cambió su diseño ni su escala.
- Segundo golpe de X: conserva la orientación hacia el rival; se eliminó el volteo horizontal del cuerpo completo.
- Enlace aéreo X → Y → B corregido según los botones físicos del mando, con memoria de la pulsación durante las pausas de impacto.
- Corazón visible sobre la cabeza del rival únicamente después de confirmar Encantamiento. No agrega daño ni prolonga el aturdimiento.
- Dash con dos toques hacia delante, interrumpible con salto o ataque y sin invulnerabilidad. Usa los cuadros de caminata actuales; todavía necesita un ciclo de carrera propio para parecerse al video.
- Aura del despertar: 13 cuadros del efecto de energía de la referencia Nezuko, con color azul y mezcla aditiva del motor. Mantiene los sprites normales de Eida y evita el arco rígido anterior.
- Daemon: sprites reducidos al 68% del tamaño anterior, colisiones ajustadas, aparición junto a Eida, carrera con alcance limitado, ataques a corta distancia y desaparición gradual. Se puede interrumpir golpeándolo o golpeando a Eida.
- Catorce técnicas con consumo de energía y entradas físicas de Xbox. Los controles se invierten de acuerdo con la orientación.
- Cadenas normales en X, Y y B; launcher con Daemon y continuaciones aéreas.
- Encantamiento rasante y ascendente con colisión, bloqueo, alcance finito y aturdimiento de 45 ticks.
- Sonidos de aparición, desplazamiento, guardia, lanzamientos e impactos; chispas y polvo del combate.
- Estados en `Specials.cns` y `Omnipotencia.cns`, referenciados en `Eida.def`. Conservar ambos archivos junto con los demás.

## Comprobaciones

- SFF v2.0.1.0: 157 sprites; los seis paneles conservan 1280×720 dentro del archivo. Retrato de combate 25×25 y retrato de selección 120×140.
- SND: 23 muestras mono PCM de 16 bits, incluidos tres efectos nuevos de la cinemática.
- AIR: 110 acciones con referencias válidas. El idle usa exclusivamente sus seis cuadros de reposo.
- 116 estados en cuatro CNS; referencias estáticas de estados, animaciones locales y sonidos verificadas.
- Pruebas de Ikemen GO con entradas y colisiones reales: técnicas, rutas mixtas, enlaces durante hitpause, salto, costes, ayudas que pueden fallar y apertura de ultimate bloqueada, esquivada o fuera de alcance. Informes reproducibles en `previews/engine_moveset_checks.json` y `previews/engine_ultimate_checks.json` del repositorio.

Las pruebas del motor usan copias temporales e instrumentación fuera de la carpeta entregada. No se pudo ejecutar el binario exacto de Jump Force MUGEN V14 del usuario ni comprobar físicamente su mando Xbox. El equilibrio frente a todo su plantel requiere partidas locales.

## Procedencia y límites visuales

Eida conserva los sprites recuperados de los recursos del usuario y los cuadros adicionales de movimiento. Daemon usa las 16 poses reconstruidas anteriormente, ahora a escala de ayudante. Esta revisión reutiliza esos dibujos en nuevas secuencias; no agrega una hoja nueva de ilustraciones. El nivel artístico de Sumire sigue siendo la referencia de acabado y no se declara alcanzado.

Omnipotencia conserva los paneles originales del manga. Las voces pertenecen a los fragmentos femeninos del MP3 japonés suministrado. Consulta `CREDITOS_Y_FUENTES.md`.

El MP4 de la ultimate usa imágenes capturadas del motor. Su audio se mezcla fuera del motor con las mismas muestras WAV y los tiempos de activación registrados durante esa captura; no es una grabación del dispositivo de audio del juego.
