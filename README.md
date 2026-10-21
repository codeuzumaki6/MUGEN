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

# Eida — movimiento, Senrigan e impactos

[**Descargar Eida actualizada**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/Eida_ACABADO.zip)

[**Ver el acabado con audio real del motor**](previews/Eida_ACABADO.mp4) · [Carga](previews/Eida_acabado_charge_motor.gif) · [Carrera y frenado](previews/Eida_acabado_run_motor.gif) · [Daemon](previews/Eida_acabado_daemon_motor.gif) · [Victoria](previews/Eida_acabado_win_motor.gif)

- **Movimiento y carga:** 16 poses nuevas repartidas entre carrera, frenado, aterrizaje, carga Senrigan y victoria. Cabello en movimiento, apoyo de pies y polvo. La carga se detiene al soltar LB, llenar la barra o recibir un golpe.
- **Contactos y remates:** doce cuadros de efectos nuevos y cuatro sonidos no verbales. Eida y Daemon distinguen impacto, bloqueo y fallo; el estallido final requiere acertar esa parte del ataque. Contadores por estado evitan repetir efectos durante hitpause o heredar el impacto del ataque anterior.
- **Victoria:** gesto, cabello y pose final con la misma blusa y shorts del combate; énfasis temporal del escenario y margen de cámara. Se comprueba tras un KO real de prueba en ambas orientaciones.
- **Combate conservado:** 14 técnicas, ramas de Daemon, persecución aérea, encanto por proyectil, parry, costes y recuperación tras derribo. El reposo mantiene sus seis cuadros y el despertar mantiene su cuerpo y tamaño. Daemon conserva su diseño y escala.
- **Omnipotencia con A:** ocho encuadres originales a 1280×720, voz japonesa intacta, coste de tres barras y daño de 350. La apertura debe conectar: bloquearla, saltarla o dejarla fuera de alcance consume la energía sin iniciar la escena.

Sustituye `chars/Eida` completa por la carpeta del ZIP. Añade `Eida/Eida.def` a `[Characters]` en `data/select.def` si hace falta. [Controles Xbox](Eida/CONTROLES_XBOX.md) · [Instalación y límites](Eida/LEEME.md) · [Créditos y fuentes](Eida/CREDITOS_Y_FUENTES.md) · [Procedencia del nuevo arte](design/Eida_acabado/REVISION.md).

La voz, los paneles originales del manga y los dibujos de Daemon se conservan. Las poses y efectos nuevos se generaron con IA; no se modificaron caras de los paneles ni se generaron voces. Las nuevas poses se calibran a los 68 píxeles del reposo y comparten escala dentro de cada hoja. El SFF contiene 194 entradas, el SND 30 muestras y el AIR 123 acciones. El material conserva variaciones de detalle y no se declara alcanzado el acabado de Sumire.

Senrigan prepara la respuesta física de Daemon; observar no causa daño. Encanto, parry, despertar y apertura/daño de Omnipotencia mantienen reglas adaptadas al juego de pelea. No se añadieron poderes ofensivos nuevos.

Pruebas en Ikemen GO: [80 controles y colisiones](previews/engine_moveset_checks.json), [seis derribos y recuperación](previews/engine_recovery_checks.json), [nueve aperturas de ultimate](previews/engine_ultimate_checks.json), [22 de presentación](previews/Eida_polish_checks.json) y [dos victorias reales](previews/Eida_polish_win_checks.json): **119 escenarios**. Se añaden cinco regresiones del validador para errores de carga, impacto infinito y flag de victoria inválido, y [reconstrucción determinista](previews/Eida_polish_rebuild_checks.json).

El [video nuevo](previews/Eida_ACABADO.mp4) reproduce seis escenas a velocidad normal y captura audio real SDL a 44100 Hz estéreo, alineado por correlación con las muestras del SND. [Registro de audio](previews/Eida_polish_audio_checks.json) · [Comprobaciones de captura](previews/Eida_polish_visual_checks.json). No se ejecutó el binario exacto de Jump Force MUGEN V14 ni el mando físico; el escenario y las barras de las pruebas son diferentes.

[Omnipotencia anterior en MP4 720p](previews/Omnipotencia_motor_HD.mp4) · [Y → X con Daemon](previews/Eida_Y_X_Daemon_motor.gif) · [Persecución aérea](previews/Eida_persecucion_aerea_motor.gif) · [Recuperación](previews/Eida_se_levanta_motor.gif). El MP4 antiguo de Omnipotencia usa audio mezclado fuera del motor y representa la revisión anterior de esa cinemática.

Reconstrucción con Python, Pillow, NumPy, SciPy, ffmpeg e Ikemen GO verificado:

```sh
python3 tools/build_presentation.py
python3 tools/build_moveset.py
python3 tools/build_cinematic.py
python3 tools/build_eida_polish.py
python3 tools/build_archives.py
python3 tools/validate_character.py Eida
python3 tools/test_mugen11_compatibility.py
python3 tools/check_eida_rebuild.py
python3 tools/check_moves_in_engine.py /ruta/al/ikemen
EIDA_RECOVERY_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/ikemen
EIDA_ULTIMATE_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/ikemen
python3 tools/check_eida_polish_in_engine.py /ruta/al/ikemen
EIDA_WIN_CHECK=1 python3 tools/check_eida_polish_in_engine.py /ruta/al/ikemen
EIDA_WIN_CHECK=1 EIDA_WIN_FACING=-1 python3 tools/check_eida_polish_in_engine.py /ruta/al/ikemen
python3 tools/make_eida_polish_previews.py /ruta/al/ikemen
python3 tools/package_character.py
```
