# Pochita True Form — especiales más largos y efectos distintos

[**Descargar Pochita actualizado**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/PochitaTrueForm_ESPECIALES_LARGOS.zip)

[**Ver los seis especiales con audio del motor**](previews/Pochita_ESPECIALES_LARGOS_Y_EFECTOS.mp4) · [Carnicería antes/ahora](previews/Pochita_CARNICERIA_ANTES_Y_AHORA.mp4) · [GIF](previews/Pochita_especiales_largos_motor.gif)

Abajo adelante/atrás + X/Y/B ahora ejecuta secuencias ampliadas con estelas propias, cortes encadenados y remate confirmado. Desgarro tiene tres contactos, Cuatro brazos cinco, Estocada tres, Barrido dos, Embestida tres y Carnicería siete. La animación dura 56–90 ticks sin contar preparación y pausas de impacto. Se conserva el coste y daño total de cada técnica: los nuevos contactos reparten ese daño. Las grabaciones van a velocidad normal.

Se añadieron 24 cuadros de efectos en seis familias: arco dentado, hojas cruzadas, estocada, polvo de barrido, avance y Carnicería. Las secuencias combinan poses de cuerpo existentes; no se presentan como nuevos dibujos del personaje. Los efectos de remate requieren acertar todos los contactos. Fallar o bloquear permite ver el movimiento, sin ese impacto confirmado. El avance usa física y las cajas ofensivas permanecen dentro de la hoja visible.

El video nuevo de Chainsaw Man aportado por el usuario se revisó visualmente para estudiar preparación, avance de triturado y derribo. Su secuencia de 22 contactos y su cabeza gigante no se reproducen literalmente. [Ficha y alcance de la revisión](design/Pochita_especiales_largos/REVISION.md). El audio de referencia no se evaluó por escucha. Se conservan la señal de activación de Code, motores y golpes del SND anterior, con once muestras no verbales.

El SFF tiene 193 entradas: 147 de cuerpo (138 poses fuente distintas), 44 efectos y dos retratos. Se conservan las cadenas mixtas X/Y/B, persecución aérea, dos especiales por secuencia, nueve técnicas direccionales, RB, RT y carga LB. **A cuesta dos barras incluso al fallar; el daño máximo es el menor entre 500 y la mitad de la vida máxima rival.** No mata desde vida completa. La corrección del crasheo por estados vacíos 170/175/180 sigue incluida.

Sustituye `chars/PochitaTrueForm` completa por la carpeta del ZIP. Agrega `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si hace falta.

[Controles Xbox](PochitaTrueForm/CONTROLES_XBOX.md) · [Instalación y límites](PochitaTrueForm/LEEME.md) · [Créditos](PochitaTrueForm/CREDITOS_Y_FUENTES.md)

Pasaron [217 pruebas de entrada y colisión](previews/Pochita_engine_checks.json), incluyendo duración completa, número exacto de contactos y daño de los seis especiales, doce guardias, fallos, consumo de energía, cadenas, persecución y recuperación. También [CPU](previews/Pochita_AI_checks.json), [ultimate frente a 500 de vida](previews/Pochita_low_life_ultimate_checks.json), [regresiones de carga MUGEN](previews/Pochita_mugen_structure_checks.json) y [reconstrucción y alcance](previews/Pochita_validator_checks.json). Los [seis registros de audio real](previews/Pochita_long_audio_checks.json) identifican el SE en la salida SDL; las [capturas](previews/Pochita_long_visual_checks.json) verifican efectos y finalización. Se usó Ikemen GO; el binario exacto de Jump Force MUGEN V14 y el mando físico requieren prueba local.

Los MP4 nuevos contienen audio real del mezclador de Ikemen GO. La comparación mantiene velocidad normal en ambas versiones y usa audio de la revisión nueva. Las pruebas verifican funcionamiento; la calidad artística y la diversión requieren revisión y partidas. El arte generado conserva variaciones de detalle.

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
POCHITA_SPECIAL_VERSION=long python3 tools/make_pochita_special_previews.py /ruta/al/ikemen
python3 tools/package_pochita.py
```

La captura de audio usa SDL disk a 44100 Hz estéreo. No necesita dispositivo físico. Eida y los originales permanecen sin cambios.

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
