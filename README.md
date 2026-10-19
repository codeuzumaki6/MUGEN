# Pochita True Form — revisión del combate

[**Descargar Pochita True Form para MUGEN 1.1**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/PochitaTrueForm_JUGABILIDAD.zip)

Sustituye `chars/PochitaTrueForm` por la carpeta completa del ZIP. Añade `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si todavía no aparece. Incluye la corrección de los estados vacíos 170/175/180 que impedían cargar en MUGEN.

[**Ver demostración del combate**](previews/Pochita_jugabilidad_demostracion.mp4) · [X-Y-B en GIF](previews/Pochita_jugabilidad_mixto_motor.gif) · [Persecución aérea](previews/Pochita_jugabilidad_persecucion_motor.gif) · [Dos especiales enlazados](previews/Pochita_jugabilidad_cancelaciones_motor.gif) · [RT](previews/Pochita_jugabilidad_embestida_motor.gif)

- Mezcla X, Y y B en las tres etapas: 27 secuencias posibles compartiendo nueve ataques, no 27 animaciones diferentes. X final lanza, Y tritura y empuja, B remata contra el suelo. La entrada del siguiente golpe se guarda durante el ataque; bloqueo y fallo cortan la ruta.
- XXX, mantener arriba al acertar el lanzamiento, X-Y-B en el aire: persecución con salto real y remate descendente, seis impactos y 324 de daño en el muñeco de 1000. Sin congelar ni teletransportar al rival.
- X-Y, abajo adelante X, abajo atrás X: normales hacia dos especiales diferentes, 600 de energía y 312 de daño en el muñeco. El tercer especial se rechaza durante la secuencia hasta recuperar control.
- Doce poses adicionales para persecución, embestida RT y remate aéreo. Cortes y sangre aparecen también en los golpes iniciales confirmados. El SFF contiene 161 entradas: 147 de cuerpo (138 poses fuente), doce efectos y dos retratos. Diez sonidos no verbales.

**A consume dos barras incluso si falla o la bloquean.** Debe acertar su embestida para ejecutar los cinco cortes animados. No muestra el panel del manga. Su daño máximo es min(500, la mitad de la vida máxima del rival); no mata desde vida completa, pero puede rematar a un rival previamente herido. Carga con LB, defensa con respuesta RB, embestida RT y nueve especiales direccionales.

Se estudiaron los CMD suministrados de Tanjiro, Nezuko y Luffy, y las reglas de Chainsaw Man SX. [Análisis de la revisión](design/Pochita_combate/REVISION.md) · [Controles y ejemplos](PochitaTrueForm/CONTROLES_XBOX.md) · [Instalación y límites](PochitaTrueForm/LEEME.md) · [Créditos](PochitaTrueForm/CREDITOS_Y_FUENTES.md)

Pasaron [181 escenarios de entradas y colisiones](previews/Pochita_engine_checks.json), [CPU](previews/Pochita_AI_checks.json), [dos pruebas de ultimate contra un rival de 500 de vida](previews/Pochita_low_life_ultimate_checks.json), [seis regresiones de estructura](previews/Pochita_mugen_structure_checks.json) y el [control de alcance y reproducción de archivos](previews/Pochita_validator_checks.json). El límite de cancelación comprueba que el motor reconoció el tercer comando y lo rechazó. Los videos son capturas de Ikemen GO, con audio montado de las muestras según eventos registrados. No son grabación del dispositivo de audio. Falta probar el binario exacto de Jump Force MUGEN V14 y el mando físico.

Las pruebas verifican funcionamiento; no certifican que ya sea divertido o tenga calidad artística profesional. El arte generado con IA conserva variaciones de detalle. El tamaño comprimido del ZIP no se usa como objetivo de calidad ni se rellena artificialmente.

Reconstrucción con Python, Pillow, NumPy, SciPy, ffmpeg e Ikemen GO verificado:

```sh
python3 tools/build_pochita_redesign.py
python3 tools/build_pochita_sound.py --from-wav
python3 tools/build_pochita_runtime.py
python3 tools/validate_pochita.py
python3 tools/check_pochita_mugen_structure.py
python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_AI=8 python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_DUMMY_LIFE=500 POCHITA_CASES='["ultihit"]' python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_PREVIEW_SET=flow python3 tools/make_pochita_previews.py /ruta/al/ikemen
python3 tools/package_pochita.py
```

Las fuentes y muestras seleccionadas están en el repositorio. `build_pochita_assets.py` reconstruye la primera versión desde la hoja original; no debe usarse para regenerar este diseño. Eida y los originales no se modificaron.

---

# Eida para Jump Force MUGEN V14

[Descargar Eida: coreografía y Omnipotencia](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/Eida_COREOGRAFIA_Y_OMNIPOTENCIA.zip)

Sustituye la carpeta `chars/Eida` completa por la del ZIP. Incluye todos los archivos de ejecución y los controles. Se conserva la corrección del derribo: Eida se levanta automáticamente mientras siga viva.

Esta revisión añade seis poses de apoyo de Eida, ajustadas al tamaño del reposo: preparación, observación, extensión de la mano y recuperación. Se aplican a las llamadas de Daemon, encanto y apertura de Omnipotencia. El reposo conserva sus seis cuadros originales. Daemon tiene contactos con distintos tiempos, recuperación del golpe y retirada antes de desaparecer. Hay tres efectos no verbales nuevos y chispas normales que se emiten una vez por impacto.

Omnipotencia usa ocho encuadres de los paneles originales a 1280×720, con tiempos distintos, cámara alternada y un fondo negro que separa la escena del combate. Conserva la voz japonesa suministrada. La apertura con A debe conectar: bloquearla, saltarla o dejarla fuera de alcance consume las tres barras sin iniciar la escena ni causar daño. Al acertar, causa 350 y libera al rival.

Daemon concentra la ofensiva fuerte. Senrigan prepara su respuesta física; no causa daño por observar. Encanto, parry, despertar y apertura/daño de Omnipotencia tienen reglas adaptadas a un juego de pelea. Las nuevas poses no completan todos los ciclos pendientes ni alcanzan por sí solas la referencia artística de Sumire.

[Controles físicos de Xbox](Eida/CONTROLES_XBOX.md) · [Detalles y límites](Eida/LEEME.md) · [Fuentes del arte y sonido](Eida/CREDITOS_Y_FUENTES.md)

## Capturas del motor

Capturadas en Ikemen GO. El escenario y las barras de Jump Force MUGEN V14 son diferentes. El audio del MP4 se mezcla fuera del motor con las mismas muestras y tiempos de la cinemática; no es una grabación del dispositivo de sonido del juego.

[Omnipotencia en MP4 720p con audio](previews/Omnipotencia_motor_HD.mp4) · [Omnipotencia GIF](previews/Omnipotencia_motor_HD.gif)

[Y → X con Daemon](previews/Eida_Y_X_Daemon_motor.gif) · [B → Y launcher](previews/Eida_B_Y_Daemon_motor.gif) · [Encanto → Daemon](previews/Eida_encanto_Daemon_motor.gif)

[Persecución aérea](previews/Eida_persecucion_aerea_motor.gif) · [Senrigan con respuesta física](previews/Eida_Senrigan_Daemon_motor.gif) · [Recuperación tras derribo](previews/Eida_se_levanta_motor.gif)

## Desarrollo y validación

Trabaja en el checkout existente. Requisitos: Python 3 con Pillow, ffmpeg y el motor Ikemen GO verificado en `/workspace/.eida-tools/ikemen-nightly`. No se necesitan servidores. El binario exacto de Jump Force MUGEN V14 y el mando físico requieren pruebas locales.

```sh
python3 tools/build_presentation.py
python3 tools/build_moveset.py
python3 tools/build_cinematic.py
python3 tools/build_archives.py
python3 tools/validate_character.py Eida
python3 tools/test_mugen11_compatibility.py
python3 tools/check_moves_in_engine.py /ruta/al/motor/ikemen
EIDA_RECOVERY_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/motor/ikemen
EIDA_ULTIMATE_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/motor/ikemen
python3 tools/make_recovery_combo_previews.py /ruta/al/motor/ikemen
python3 tools/make_ultimate_preview.py /ruta/al/motor/ikemen
python3 tools/package_character.py
```

Los 95 escenarios comprobados se distribuyen en [80 de movimientos, combos y defensa](previews/engine_moveset_checks.json), [6 de derribos y recuperación](previews/engine_recovery_checks.json) y [9 de Omnipotencia](previews/engine_ultimate_checks.json). Las nuevas comprobaciones verifican que bloquear los normales corta las ramas de Daemon, que bloquear/esquivar encanto evita la ayuda y su coste adicional, que golpear a Eida interrumpe una ayuda activa en un máximo de un tick, y que golpear solo a Daemon lo elimina al impacto sin dejar un ayudante bloqueado. Cuatro pruebas del validador cubren el archivo actual y las regresiones de compatibilidad y caída.

Las pruebas usan copias instrumentadas fuera de la carpeta entregada y restauran el diagnóstico del motor. Los CNS/CMD/AIR entregados usan sintaxis de MUGEN 1.1. La carga en Ikemen y el validador no sustituyen ejecutar el juego exacto del usuario ni equilibrar partidas contra todo su plantel.
