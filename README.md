# Eida para Jump Force MUGEN V14

[Descargar Eida: recuperación y nuevos combos de Daemon](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/Eida_FIX3_DERRIBO_Y_COMBOS.zip)

Corregido el bloqueo al caer al suelo: las animaciones de impacto terminan y Eida pasa del estado tumbado al levantarse automáticamente mientras siga viva. Sustituye la carpeta `chars/Eida` completa por la del ZIP.

Añade **Y → X** para una ráfaga de Daemon, **B → Y** para su launcher, **abajo + Y → X** para seguir un encanto confirmado, y **abajo + X → arriba → X** para perseguir al rival y golpear en el aire. Daemon conserva su diseño y aparece junto a Eida. Las rutas tienen nuevas transiciones de poses, estelas cortas y efectos de llegada y salida.

Senrigan prepara una respuesta física de Daemon; se retiró el daño directo de la observación. Los corazones, el parry, el despertar y la apertura/daño de Omnipotencia representan adaptaciones de juego, no habilidades nuevas del manga. Se conservan las correcciones de compatibilidad `IfElse()` y condiciones de cancelación válidas para MUGEN 1.1.

[Controles físicos de Xbox](Eida/CONTROLES_XBOX.md) · [Detalles y límites de las pruebas](Eida/LEEME.md)

Omnipotencia ahora empieza con un sello que viaja hasta el rival: se puede bloquear, saltar o dejar fuera de alcance. Al fallar consume las tres barras sin cinemática ni daño. Al conectar muestra seis encuadres originales del manga a 1280×720, con fundidos, cámara, sonido y remate de 350 de daño. Se eliminaron los paneles reducidos a 320×240.

Añade doble encanto (↓A), retroceso de Senrigan (↓RB) y apertura combinada con Daemon (↓RT), además de rutas X → Y → Y y X → B → B y cancelaciones ofensivas durante hitpause. El salto sube moderadamente. Los sprites de Daemon, el cuerpo normal de Eida y el aura del despertar se conservan. Todavía falta un ciclo dibujado de carrera: el dash reutiliza sus cuadros de caminata.

## Capturas del motor

Estas animaciones se capturaron en Ikemen GO; el escenario y las barras de Jump Force MUGEN V14 son diferentes.

[Ver cómo se levanta](previews/Eida_se_levanta_motor.gif) · [Y → X con Daemon](previews/Eida_Y_X_Daemon_motor.gif) · [B → Y launcher](previews/Eida_B_Y_Daemon_motor.gif)

[Encanto → Daemon](previews/Eida_encanto_Daemon_motor.gif) · [Persecución aérea](previews/Eida_persecucion_aerea_motor.gif) · [Senrigan con respuesta física](previews/Eida_Senrigan_Daemon_motor.gif)

[Ver Omnipotencia en MP4 720p con sonido](previews/Omnipotencia_motor_HD.mp4)

![Omnipotencia capturada en el motor](previews/Omnipotencia_motor_HD.gif)

[Combo mixto](previews/Eida_combo_mixto_motor.gif) · [Apertura combinada](previews/Eida_apertura_combinada_motor.gif) · [Doble encanto](previews/Eida_doble_encanto_motor.gif) · [Paso de Senrigan](previews/Eida_paso_senrigan_motor.gif)

[Dash actual](previews/Eida_dash_motor.gif) · [Daemon junto a Eida](previews/Daemon_desde_Eida_motor.gif) · [Aura del despertar](previews/Eida_aura_azul_motor.gif)

## Desarrollo

Trabaja en el checkout existente. Requisitos: Python 3 con Pillow, ffmpeg para convertir efectos de sonido y un motor Ikemen GO para pruebas compatibles; el binario exacto de Jump Force MUGEN V14 requiere pruebas locales del usuario.

```sh
python3 tools/build_moveset.py
python3 tools/build_cinematic.py
python3 tools/build_archives.py
python3 tools/validate_character.py Eida
python3 tools/test_mugen11_compatibility.py
python3 tools/check_moves_in_engine.py /ruta/al/motor/ikemen
EIDA_RECOVERY_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/motor/ikemen
EIDA_ULTIMATE_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/motor/ikemen
python3 tools/make_recovery_combo_previews.py /ruta/al/motor/ikemen
python3 tools/make_video_reference_previews.py /ruta/al/motor/ikemen
python3 tools/make_ultimate_preview.py /ruta/al/motor/ikemen
python3 tools/package_character.py
```

El ZIP contiene los archivos de ejecución y la guía de controles. Los recursos fuente están en `Eida/assets/`. Los generadores conservan los ejes de los efectos de la referencia original; la coloración azul y la transparencia aditiva se aplican en el motor. No se necesitan procesos de servidor para editar el personaje.

El informe [engine_moveset_checks.json](previews/engine_moveset_checks.json) registra 68 escenarios de movimiento, técnicas y combos. Las nueve pruebas adicionales de la ulti están en [engine_ultimate_checks.json](previews/engine_ultimate_checks.json): acierto, bloqueo, evasión, rival fuera de alcance en ambas orientaciones, y falta de energía. Para reproducirlas: `EIDA_ULTIMATE_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/motor`.

Las seis pruebas de recuperación están en [engine_recovery_checks.json](previews/engine_recovery_checks.json): barrido, rebote y caída aérea en ambas orientaciones, con comprobación de daño recibido, levantarse y nuevo ataque. Se reproducen con `EIDA_RECOVERY_CHECK=1`. En total pasan 83 escenarios y cuatro pruebas del validador.

Las pruebas modifican únicamente copias temporales y restauran el script de diagnóstico del motor al terminar. Los archivos entregados son CNS/CMD/AIR para MUGEN 1.1 y no incluyen instrumentación de Ikemen. No se ejecutó la versión exacta de Jump Force MUGEN V14 del usuario ni se probó físicamente su mando. El motor oficial verificado de este entorno está en `/workspace/.eida-tools/ikemen-nightly`; no requiere servidores. El MP4 usa capturas reales del motor con audio mezclado a partir de las muestras originales del SND y los tiempos de activación registrados. El arte del manga no fue redibujado con IA.
