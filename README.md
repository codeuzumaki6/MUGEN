# Pochita True Form — motores, movimiento y remates

[**Descargar Pochita actualizado**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/PochitaTrueForm_ACABADO.zip)

[**Ver el acabado con audio real del motor**](previews/Pochita_ACABADO.mp4) · [Aire y bufanda anteriores](previews/Pochita_AEREOS_Y_BUFANDA.mp4) · [Revisión anterior](previews/Pochita_SIN_SIERRA_GIGANTE.mp4) · [Estocada corregida](previews/Pochita_estocada_nuevo_motor.gif) · [Devorar y borrado](previews/Pochita_borrado_nuevo_motor.gif) · [Despertar](previews/Pochita_despertar_nuevo_motor.gif)

- **Carga, movimiento e impactos:** cuatro poses de motores, carrera con bufanda animada, frenado y aterrizaje, polvo de pies, estelas dentadas y chispas propias. Los remates confirmados tienen un sonido nuevo y dos ticks más de pausa.
- **Victoria:** cuatro poses para recoger/sacudir sierras y bajar motores, con oscurecimiento temporal del escenario. Se comprueba tras ganar una ronda real.
- **X/Y/B en el aire:** tres etapas con botones repetidos o mezclados. X final lanza, Y tritura y B remata hacia abajo; máximo tres ataques por salto, sin coste. 27 rutas que comparten nueve acciones.
- **Abajo + RB (350):** lazo intestinal bloqueable, sujeción breve y tambaleo para continuar con un normal.
- **Abajo + RT (600):** sujeción confirmada y tres cortes con las motosierras normales, 190 de daño total en la prueba. Los dos movimientos pueden fallar y no sujetan objetivos aéreos. Los nombres y el tambaleo son adaptaciones jugables.
- **Abajo + LB / antiguo Pausa:** exige tres barras, consume una, dura seis segundos. Regenera hasta 240 de vida y aumenta un 20 % el daño de ataques por colisión. Conserva el cuerpo y su tamaño; añade brasas rojas. No concede invulnerabilidad ni revive. Hay 15 segundos entre activaciones y hace falta llenar otra vez la barra.
- **Abajo + A:** conserva la antigua cinemática de cinco cortes como especial por una barra, con daño limitado a min(250, 25 % de la vida máxima rival).
- **A:** nueva secuencia de devorar y borrado conceptual por dos barras. La apertura debe conectar y puede bloquearse, esquivarse o interrumpirse. Al acertar hay mordisco, deglución, desaparición temporal, pérdida de hasta 500 de energía rival y regreso al combate. Daño máximo min(450, 45 % de la vida máxima rival). No mata desde vida completa.
- **Abajo adelante + Y:** avance rápido y cortes con las motosierras normales de los brazos. Se retiraron la sierra gigante, el arma con cadena y sus colisiones extendidas. El alcance proviene del movimiento físico; las cajas de ataque siguen las hojas visibles. Desgarro, Embestida y RT mantienen sus avances. Desde lejos pueden fallar los primeros cortes.

La desaparición y pérdida de energía representan el borrado del canon en un juego de pelea. No se borran permanentemente conceptos, nombres, recuerdos, archivos ni habilidades del rival. La curación automática y los valores de combate también son reglas de adaptación. Vida 1250, defensa 110 y especiales de bajo consumo se conservan; las cinemáticas mantienen sus límites incluso durante el despertar.

Ocho poses de devorar y doce cuadros de efectos nuevos generados con IA. El SFF actual contiene 249 entradas: 179 de cuerpo, 68 efectos y dos retratos. Se añadieron ocho poses de bufanda; el acabado añade otras 16 poses de cuerpo y 12 efectos. Hay 170 poses fuente de cuerpo distintas y 18 muestras no verbales. Se mantienen las cadenas mixtas, persecución aérea, seis especiales ampliados, técnicas agachadas, parry y recuperación. El arte tiene variaciones de detalle; la demostración permite revisarlo sin presentarlo como acabado profesional.

Se revisaron visualmente los videos de Chainsaw Man y Sukuna aportados por el usuario para estudiar preparación, impactos y remates. No se escuchó el audio de referencia en este entorno ni se copiaron voces, sprites o poderes de Sukuna. [Reglas, procedencia y alcance](design/Pochita_devour/REVISION.md).

Sustituye `chars/PochitaTrueForm` completa por la carpeta del ZIP. Agrega `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si hace falta. [Controles Xbox](PochitaTrueForm/CONTROLES_XBOX.md) · [Instalación y límites](PochitaTrueForm/LEEME.md) · [Créditos](PochitaTrueForm/CREDITOS_Y_FUENTES.md).

Pruebas: [16 de presentación y control](previews/Pochita_polish_checks.json), [dos victorias reales](previews/Pochita_polish_win_checks.json), [96 de combos aéreos y bufanda](previews/Pochita_air_scarf_checks.json), [221 generales de entradas y colisiones](previews/Pochita_engine_checks.json), [46 de despertar, alcance y especial reasignado](previews/Pochita_devour_checks.json), [CPU](previews/Pochita_AI_checks.json), [cuatro de daño limitado contra 500 de vida](previews/Pochita_low_life_ultimate_checks.json), [KO sin resurrección](previews/Pochita_no_revive_checks.json), [regresiones de carga MUGEN](previews/Pochita_mugen_structure_checks.json) y [reconstrucción/alcance](previews/Pochita_validator_checks.json). Se comprueban curación exacta, tope de vida, espera, botón mantenido, ataque durante el efecto, multiplicador que expira, falta de energía, apertura interrumpida y liberación si el atacante sale de la escena. Los [registros de audio](previews/Pochita_polish_audio_checks.json) y las [capturas](previews/Pochita_polish_visual_checks.json) corresponden a seis grabaciones nuevas de acabado en Ikemen GO.

Los nuevos MP4 capturan audio real SDL a 44100 Hz estéreo, sincronizado por correlación con muestras empaquetadas; se reproducen a velocidad normal. Los videos antiguos representan revisiones anteriores. No se ejecutó el binario exacto de Jump Force MUGEN V14 ni el mando Xbox físico. El equilibrio y la diversión requieren partidas locales.

Reconstrucción con Python, Pillow, NumPy, SciPy, ffmpeg e Ikemen GO verificado:

```sh
python3 tools/build_pochita_redesign.py
python3 tools/build_pochita_sound.py --from-wav
python3 tools/build_pochita_runtime.py
python3 tools/validate_pochita.py
python3 tools/check_pochita_mugen_structure.py
python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_POLISH_CHECK=1 python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_WIN_CHECK=1 python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_AIR_SCARF_CHECK=1 python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_DEVOUR_CHECK=1 python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_KO_CHECK=1 python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_AI=8 python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
POCHITA_DUMMY_LIFE=500 POCHITA_CASES='["ultihit","Devastacion"]' python3 tools/check_pochita_in_engine.py /ruta/al/ikemen
python3 tools/make_pochita_polish_previews.py /ruta/al/ikemen
python3 tools/package_pochita.py
```

Eida y los originales se conservan sin cambios.

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
