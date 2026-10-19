# Pochita True Form — combos y remates

[**Descargar Pochita True Form para MUGEN 1.1**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/PochitaTrueForm_REMATES.zip)

Sustituye `chars/PochitaTrueForm` por la carpeta completa del ZIP. Añade `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si todavía no aparece.

X/X/X termina con lanzamiento; Y/Y/Y tritura y empuja; B/B/B salta y remata contra el suelo. Los cortes confirmados tienen sangre y efectos de impacto. Los especiales cuestan entre 250 y 750; RB 250 y RT 750. La carga sigue en LB. El modelo conserva armadura negra robusta, cuatro brazos con motosierras y bufanda roja.

**A consume dos barras incluso si falla o la bloquean.** Debe acertar su embestida para ejecutar los cinco cortes animados. Ocho poses nuevas despliegan los cuatro brazos; no se muestra el panel del manga. Su daño máximo es el menor entre 500 y la mitad de la vida máxima del rival. No mata desde la vida completa; puede rematar a un rival ya herido.

[Combo X](previews/Pochita_remates_combo_x_motor.gif) · [Combo Y](previews/Pochita_remates_combo_y_motor.gif) · [Combo B](previews/Pochita_remates_combo_b_motor.gif) · [Ultimate GIF](previews/Pochita_remates_ultimate_motor.gif) · [Ultimate MP4 con audio montado](previews/Pochita_remates_ultimate_motor.mp4)

Las capturas son reales de Ikemen GO. El audio del MP4 se mezcla con las muestras del personaje y los tiempos registrados de sus eventos; no es grabación de la salida de audio del juego. Pasaron [119 escenarios de entradas y colisiones](previews/Pochita_engine_checks.json), [CPU](previews/Pochita_AI_checks.json), [dos pruebas contra un rival de 500 de vida](previews/Pochita_low_life_ultimate_checks.json) y [el control de alcance del validador](previews/Pochita_validator_checks.json). Falta probar el binario exacto de Jump Force MUGEN V14 y el mando físico.

El SFF incluye 149 entradas: 135 de cuerpo (126 poses fuente distintas), doce efectos y dos retratos. Hay diez sonidos no verbales. Arte generado con IA; algunos detalles varían entre cuadros. [Controles Xbox](PochitaTrueForm/CONTROLES_XBOX.md) · [Instalación y límites](PochitaTrueForm/LEEME.md) · [Créditos](PochitaTrueForm/CREDITOS_Y_FUENTES.md) · [Fuentes de los remates](design/Pochita_remates/LEEME.md)

Reconstrucción con Python, Pillow, NumPy, SciPy, ffmpeg e Ikemen GO verificado:

```sh
python3 tools/build_pochita_redesign.py
python3 tools/build_pochita_sound.py --from-wav
python3 tools/build_pochita_runtime.py
python3 tools/validate_pochita.py
python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_AI=8 python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_DUMMY_LIFE=500 POCHITA_CASES='["ultihit"]' python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
python3 tools/make_pochita_previews.py /ruta/al/ikemen
python3 tools/package_pochita.py
```

Las fuentes de arte y las muestras seleccionadas están en el repositorio. El constructor `build_pochita_assets.py` conserva la versión anterior desde la hoja original; no debe ejecutarse para regenerar este diseño. Eida y los originales no se modificaron.

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
