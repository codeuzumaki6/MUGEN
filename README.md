# Pochita True Form — especiales con sonido y presentación

[**Descargar Pochita con los seis especiales actualizados**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/PochitaTrueForm_ESPECIALES_CON_SONIDO.zip)

[**Ver los seis especiales con audio real del motor**](previews/Pochita_ESPECIALES_CON_SONIDO.mp4) · [Ver el arranque en GIF](previews/Pochita_especial_activacion_motor.gif)

Abajo adelante/atrás + X, Y o B ahora inicia una pose, oscurecimiento breve y destello horizontal rojo con sonido de activación separado; después sale la técnica de motosierras. La señal usa un canal propio y el motor no la corta. El coste se paga una sola vez, aunque el ataque falle o sea bloqueado; sin energía suficiente no se activa la presentación. La preparación dura 12 ticks, o 6 al enlazar una segunda técnica.

La referencia fue el video de Goku enviado por el usuario. Se adapta su arranque visual; no se copian rayos, voces ni transformaciones. El SE proviene del Code funcional suministrado, grupo 950,2 (Super Charge), de MUGEN STARS. No se presenta como extracción exacta del audio mezclado del video. Se añadieron ocho efectos de destello/anillo generados con IA. El SFF tiene 169 entradas (147 de cuerpo, veinte efectos, dos retratos) y el SND once sonidos no verbales.

Se conservan las cadenas mixtas de X/Y/B, XXX-arriba-X-Y-B en el aire, la segunda técnica enlazada con límite de dos, los nueve especiales direccionales, RB, RT y carga LB. **A cuesta dos barras incluso al fallar; su daño máximo es el menor entre 500 y la mitad de la vida máxima rival.** No mata a un rival desde vida completa.

Sustituye `chars/PochitaTrueForm` completa por la carpeta del ZIP. Agrega `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si hace falta. La corrección del crasheo por estados vacíos 170/175/180 sigue incluida.

[Controles Xbox](PochitaTrueForm/CONTROLES_XBOX.md) · [Instalación y límites](PochitaTrueForm/LEEME.md) · [Créditos](PochitaTrueForm/CREDITOS_Y_FUENTES.md) · [Referencia y procedencia](design/Pochita_especiales/REFERENCIA.md) · [Revisión anterior del combate](design/Pochita_combate/REVISION.md)

Pasaron [205 pruebas de comandos y colisiones](previews/Pochita_engine_checks.json), incluyendo los seis especiales y atajos diagonales, doce intentos sin energía suficiente, doce fallos desde lejos, costes exactos, combos, persecución y límite de cancelaciones. También [CPU](previews/Pochita_AI_checks.json), [ultimate contra un rival de 500 de vida](previews/Pochita_low_life_ultimate_checks.json), [seis regresiones de estructura](previews/Pochita_mugen_structure_checks.json) y [reconstrucción y alcance](previews/Pochita_validator_checks.json). Los [seis registros de audio real](previews/Pochita_actual_audio_checks.json) identifican el SE en la salida SDL del motor; las [capturas](previews/Pochita_special_visual_checks.json) verifican los efectos y su finalización. No se ejecutó el binario exacto de Jump Force MUGEN V14 ni se conectó el mando físico.

Los nuevos MP4 de especiales contienen audio real del mezclador de Ikemen GO, sincronizado por correlación con el SE de activación. Los videos anteriores de remates/jugabilidad mantienen audio montado según eventos; son versiones anteriores. Las pruebas verifican funcionamiento, no una calidad artística profesional ni el equilibrio contra todo el plantel. El arte generado conserva variaciones de detalle.

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
python3 tools/make_pochita_special_previews.py /ruta/al/ikemen
python3 tools/package_pochita.py
```

La grabación real requiere la configuración de sonido predeterminada de la herramienta: 44100 Hz estéreo, con SDL disk. No necesita un dispositivo físico. Eida y los originales no se modificaron.

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
