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

# Eida — especiales audibles y Omnipotencia con Kawaki

[**Descargar Eida corregida**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/Eida_SONIDO_Y_ABRAZO.zip)

[**Ver los 14 jutsus con audio real**](previews/Eida_especiales_nuevo_motor.mp4) · [**Ver la ulti del abrazo a Kawaki**](previews/Eida_omnipotencia_abrazo_nuevo_motor.mp4) · [Senrigan sin golpe recibido](previews/Eida_senrigan_sin_ataque_nuevo_motor.mp4)

- **Activación de especiales:** los 14 jutsus incorporan el mismo sonido no verbal que Pochita, un destello y una pausa breve. El sonido es independiente del impacto y se reproduce aunque el ataque falle. Está en el SND como 1,21, canal 4 al 100 %. La pausa dura 12 ticks, o seis al cancelar un normal. No añade invulnerabilidad ni cambia los costes.
- **Senrigan ↓atrás + Y:** es un contraataque. Eida lleva la mano al ojo y observa durante unos 0.8 segundos. Si recibe un golpe en su caja de reversión, Daemon aparece junto a ella y responde físicamente. Si nadie ataca, no hay daño ni invocación: desaparece el ojo, baja la mano y termina. Se conservó la caja de reversión al cambiar la pose.
- **Omnipotencia con A:** ocho poses nuevas de acercamiento y abrazo a Kawaki, con movimiento de cabello y liberación de la onda. La escena principal es de sprites, sobre un panel original de la onda atenuado. La apertura tiene que acertar; sigue siendo bloqueable, evadible y de alcance finito. Consume tres barras y causa 350 al confirmar.

El abrazo representa el recuerdo canónico con Kawaki aunque el rival sea otro personaje. El rival elegido sigue siendo el objetivo y regresa al combate; no se transforma permanentemente en Kawaki. Los sprites del abrazo son arte nuevo generado con IA. No se redibujaron ni retocaron con IA los paneles originales, y no se generaron voces. [Procedencia del abrazo](design/Eida_omnipotencia/REVISION.md) · [Sonido y lectura de Senrigan](design/Eida_acabado/ACTIVACION.md).

Se conservan carrera, frenado, aterrizaje, carga, victoria, remates, cadenas y ayudas de Daemon. El reposo mantiene sus seis cuadros y el despertar conserva el cuerpo y tamaño originales. El SFF tiene 202 entradas, el SND 31 muestras y el AIR 124 acciones; no se declara alcanzado el acabado artístico de Sumire.

Sustituye `chars/Eida` completa por la carpeta del ZIP. Añade `Eida/Eida.def` a `[Characters]` en `data/select.def` si hace falta. [Controles Xbox](Eida/CONTROLES_XBOX.md) · [Instalación y límites](Eida/LEEME.md) · [Créditos](Eida/CREDITOS_Y_FUENTES.md).

Pruebas en Ikemen GO: [80 controles y colisiones](previews/engine_moveset_checks.json), [seis derribos y recuperación](previews/engine_recovery_checks.json), [nueve aperturas de ultimate](previews/engine_ultimate_checks.json) y [dos pruebas de Senrigan sin ataque rival](previews/Eida_Senrigan_idle_checks.json). Las pruebas de la revisión de movimiento anterior se conservan en [22 casos de presentación](previews/Eida_polish_checks.json) y [dos victorias reales](previews/Eida_polish_win_checks.json). El validador tiene siete regresiones: errores de carga anteriores, impacto infinito, flag de victoria inválido, caja de reversión ausente y sonido de jutsu ausente. [Reconstrucción determinista](previews/Eida_polish_rebuild_checks.json).

Los nuevos videos capturan audio real SDL a 44100 Hz estéreo, sin mezcla de efectos fuera del motor. [Registro de activaciones y cinemática](previews/Eida_technique_audio_checks.json). Cada activación se contrasta con la muestra empaquetada; las imágenes se sincronizan con esos eventos de audio sin estirar ni mezclar la grabación. No se ejecutó el binario exacto de Jump Force MUGEN V14 ni el mando físico.

[Video anterior de movimiento y acabado](previews/Eida_ACABADO.mp4) · [Omnipotencia anterior con paneles](previews/Omnipotencia_motor_HD.mp4). Representan revisiones anteriores; el video antiguo de paneles usaba audio mezclado fuera del motor.

Reconstrucción con Python, Pillow, NumPy, SciPy, ffmpeg e Ikemen GO verificado:

```sh
python3 tools/build_presentation.py
python3 tools/build_moveset.py
python3 tools/build_cinematic.py
python3 tools/build_eida_polish.py
python3 tools/build_eida_hug_ultimate.py
python3 tools/build_archives.py
python3 tools/validate_character.py Eida
python3 tools/test_mugen11_compatibility.py
python3 tools/check_eida_rebuild.py
python3 tools/check_moves_in_engine.py /ruta/al/ikemen
EIDA_RECOVERY_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/ikemen
EIDA_ULTIMATE_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/ikemen
EIDA_SENRIGAN_IDLE_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/ikemen
python3 tools/check_eida_polish_in_engine.py /ruta/al/ikemen
python3 tools/make_eida_technique_previews.py /ruta/al/ikemen
python3 tools/package_character.py
```
