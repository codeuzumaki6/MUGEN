# Jura Shinju — bijūdama ocular y Mokuton

[**Descargar Jura Shinju**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/JuraShinju.zip) · [Controles Xbox](JuraShinju/CONTROLES_XBOX.md) · [Instalación](JuraShinju/LEEME.md) · [Créditos](JuraShinju/CREDITOS_Y_FUENTES.md)

Se instala como `JuraShinju`, con nombre interno y visible **Jura Shinju**, para añadirlo junto a otros personajes llamados Jura.

Esta revisión corrige RB y las bijūdamas para apuntar al cuerpo de rivales pequeños y agachados. Abajo + RB es un asedio ocular de tres disparos con Jura erguido. La ultimate debe acertar primero; al confirmar, Jura se sienta sobre un trono de raíces y dispara la esfera en diagonal. Consume 3000 de energía y el daño total sigue limitado a min(450, 45% de la vida máxima rival).

[Ultimate sobre raíces](previews/Jura_ultimate_motor.mp4) · [RB contra rivales pequeños](previews/Jura_chaparros_motor.mp4) · [Abajo + RB](previews/Jura_asedio_motor.mp4) · [Regeneración con raíces](previews/Jura_despertar_motor.mp4) · [Victoria con libro](previews/Jura_victoria_motor.mp4) · [Bijūdamas](previews/Jura_ocular_motor.mp4) · [Madera](previews/Jura_madera_motor.mp4) · [Combos](previews/Jura_combos_motor.mp4) · [Aéreos](previews/Jura_aereos_motor.mp4) · [Garras](previews/Jura_garras_motor.mp4) · [Carga](previews/Jura_carga_motor.mp4)

Abajo + Pausa/LB conserva la amplificación de 12 segundos, exige tres barras y consume 1500. Al activar, un capullo de raíces se cierra y se abre mientras restaura hasta 180 de vida; la curación se interrumpe si recibe un golpe y no continúa fuera del capullo. La victoria muestra a Jura sacando y leyendo un libro turquesa.

Conserva las 36 poses fuente y los ojos de Rinnegan violeta claro. Se añaden una pose sentada, cuatro poses de libro y efectos de madera generados con IA como recursos suplementarios, con créditos separados. Tres cadenas terrestres, cadenas aéreas, 13 técnicas, marcas de garra, dash y carga con aura turquesa.

Pruebas: [entradas y colisiones](previews/Jura_engine_checks.json), [guardia](previews/Jura_guard_checks.json), [CPU](previews/Jura_CPU_checks.json), [vida reducida](previews/Jura_low_life_checks.json), [regeneración y su interrupción](previews/Jura_regen_checks.json), [puntería contra rivales pequeños agachados](previews/Jura_aim_scale_0.25_1_checks.json), [victoria con libro](previews/Jura_victory_checks.json), [capturas](previews/Jura_preview_checks.json) y [conservación/reconstrucción](previews/Jura_preservation_checks.json). Los videos nuevos proceden de Ikemen GO. El binario exacto de Jump Force MUGEN V14 y el mando físico quedan pendientes de prueba.

Extrae `JuraShinju` en `chars` y añade `JuraShinju/JuraShinju.def` a `[Characters]` de `data/select.def`. Reconstrucción con `tools/build_jura_assets.py`, `tools/build_jura_runtime.py`, `tools/validate_jura.py`, `tools/check_jura_in_engine.py`, `tools/make_jura_previews.py`, `tools/make_jura_victory_preview.py` y `tools/package_jura.py`.

---

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

# Eida — Daemon con el modelo aportado

[**Descargar Eida actualizada**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/Eida_DAEMON_ORIGINAL.zip)

[**Ver al nuevo Daemon: seis ataques con audio real**](previews/Eida_daemon_modelo_nuevo_motor.mp4) · [**GIF de Daemon**](previews/Eida_daemon_modelo_nuevo_motor.gif) · [Omnipotencia compacta conservada](previews/Eida_omnipotencia_abrazo_nuevo_motor.mp4)

- **Daemon:** adopta la hoja original de Vahidras aportada en `daemon.zip`. Las poses de pie y carrera proceden directamente del JPG; 16 poses suplementarias generadas con IA completan los puños, patadas, barrido y defensa. Son 19 entradas SFF y 18 imágenes distintas, por una pose reutilizada. Cuerpo de hasta 49 píxeles, frente a 68 de Eida. La carrera tiene sus propios cuadros, el barrido usa la patada baja y las cajas ofensivas siguen el nuevo modelo. [Procedencia y límites del dibujo](design/Daemon_original/REVISION.md).
- **Omnipotencia con A:** usa los dos cuadros originales de Eida y Kawaki de la hoja aportada, a escala nativa 1. Preparación, abrazo y estallido ocurren dentro del escenario; la escena confirmada termina en 160 ticks, unos 2.67 segundos. El video completo con apertura y recuperación dura 3.7 segundos. La apertura puede bloquearse, saltarse o fallar por distancia. Consume tres barras y causa 350 solo al confirmar.
- **Activación de especiales:** los 14 jutsus conservan el mismo sonido no verbal que Pochita, un destello y una pausa breve. El sonido se reproduce aunque el ataque falle. Está en el SND como 1,21, canal 4 al 100 %. La pausa dura 12 ticks, o seis al cancelar un normal; no cambia los costes.
- **Senrigan ↓atrás + Y:** Eida lleva la mano al ojo y observa durante unos 0.8 segundos. Si un golpe entra en su caja de reversión, Daemon responde físicamente. Sin golpe entrante no hay daño ni invocación: desaparece el ojo, baja la mano y termina.

El abrazo conserva exactamente dos poses fuente, con animación limitada. Se elimina el fondo verde y se empaquetan sin reescalar ni redibujar. El rival sigue siendo el objetivo y regresa al combate; Kawaki representa ese recuerdo canónico. Los paneles originales y las voces japonesas permanecen sin modificar. [Procedencia y tiempos](design/Eida_omnipotencia/REVISION.md) · [Sonido y lectura de Senrigan](design/Eida_acabado/ACTIVACION.md).

Se conservan carrera, frenado, aterrizaje, carga, victoria, remates, cadenas y ayudas de Daemon. El reposo mantiene sus seis cuadros y el despertar conserva cuerpo y tamaño. El SFF tiene 199 entradas, el SND 31 muestras y el AIR 124 acciones. La hoja original tiene resolución limitada; no se declara alcanzado el acabado artístico de Sumire.

Sustituye `chars/Eida` completa por la carpeta del ZIP. Añade `Eida/Eida.def` a `[Characters]` en `data/select.def` si hace falta. [Controles Xbox](Eida/CONTROLES_XBOX.md) · [Instalación y límites](Eida/LEEME.md) · [Créditos](Eida/CREDITOS_Y_FUENTES.md).

La revisión de Daemon pasó de nuevo los [80 casos de entradas y colisiones](previews/engine_moveset_checks.json), siete regresiones de compatibilidad y [dos reconstrucciones idénticas](previews/Eida_polish_rebuild_checks.json). La [comprobación de sus sprites](previews/Eida_Daemon_source_checks.json) verifica escala, originales y animaciones. La [prueba de conservación](previews/Eida_Daemon_preservation_checks.json) confirma 180 registros SFF ajenos a Daemon idénticos, además de CNS/CMD/SND y Pochita. Se conservan los informes anteriores de [nueve aperturas de ulti](previews/engine_ultimate_checks.json), [seis derribos](previews/engine_recovery_checks.json), [Senrigan sin ataque rival](previews/Eida_Senrigan_idle_checks.json), [22 casos de presentación](previews/Eida_polish_checks.json), [dos victorias](previews/Eida_polish_win_checks.json) y [procedencia de los sprites del abrazo](previews/Eida_compact_scene_checks.json).

La nueva captura de Daemon utiliza audio real SDL a 44100 Hz estéreo. [Registro de seis activaciones y combate](previews/Eida_Daemon_modelo_audio_checks.json). La captura de la ulti sigue representando la secuencia actual, cuyo arte y estados no cambian. Los videos antiguos de especiales/Senrigan muestran el Daemon anterior y se conservan como historial; sus activaciones sonoras permanecen en el SND. [Registro histórico](previews/Eida_technique_audio_checks.json). No se ejecutó el binario exacto de Jump Force MUGEN V14 ni el mando físico.

Reconstrucción con Python, Pillow, NumPy, SciPy, ffmpeg e Ikemen GO verificado:

```sh
python3 tools/build_presentation.py
python3 tools/build_moveset.py
python3 tools/build_cinematic.py
python3 tools/build_eida_polish.py
python3 tools/build_eida_hug_ultimate.py
python3 tools/build_daemon_reference.py
python3 tools/build_archives.py
python3 tools/validate_character.py Eida
python3 tools/check_eida_compact_scene.py
python3 tools/check_daemon_reference.py
python3 tools/test_mugen11_compatibility.py
python3 tools/check_eida_rebuild.py
python3 tools/check_moves_in_engine.py /ruta/al/ikemen
EIDA_RECOVERY_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/ikemen
EIDA_ULTIMATE_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/ikemen
EIDA_SENRIGAN_IDLE_CHECK=1 python3 tools/check_moves_in_engine.py /ruta/al/ikemen
python3 tools/check_eida_polish_in_engine.py /ruta/al/ikemen
python3 tools/make_eida_technique_previews.py /ruta/al/ikemen
EIDA_DAEMON_MODEL_REVIEW=1 python3 tools/make_eida_technique_previews.py /ruta/al/ikemen
python3 tools/package_character.py
```


---

# Mamushi Shinju — división autónoma y combate reconstruido

[**Descargar Mamushi**](https://github.com/codeuzumaki6/MUGEN/raw/refs/heads/main/Mamushi_SHINJU.zip)

[**Especiales pulidos con sonido real**](previews/Mamushi_especiales_motor.mp4) · [Dash con ←← / →→](previews/Mamushi_dash_motor.mp4) · [RT: mandíbula y orbe Shinju](previews/Mamushi_bramido_motor.mp4) · [División con seis copias](previews/Mamushi_division_motor.mp4) · [Combos](previews/Mamushi_combos_motor.mp4) · [Ultimate con A](previews/Mamushi_ultimate_motor.mp4)

Se reconstruyó la programación de la base AC_Mamushi incompleta. Se mantienen los dibujos, colores y escala de las 80 entradas originales de cuerpo y armas; no se generan cuerpos con IA. Los retratos vacíos ahora usan un recorte de su propio rostro. Se conservan los originales recibidos y sus hashes en `source_material/Mamushi_original/`.

- **X/X/X, Y/Y/Y y B/B/B:** cadenas de tres golpes con remate que lanza o derriba; permiten mezclar botones al acertar. Tres familias aéreas con un máximo de tres ataques por salto.
- **Dash:** ←← / →→ mueve hacia ese lado por el suelo, frena y permite enlazar un ataque. Es gratuito y vulnerable; un toque sigue caminando.
- **Especiales:** transformaciones con preparación, extensión y recogida, siguiendo la referencia de Vaydra. Brazo extensible, raíz que surge bajo el objetivo, embestida de mandíbula, taladro con viento y polvo, maza con impacto en el piso y tres ráfagas de tres espinas. Las cajas de las partes lanzadas siguen el dibujo. **RT** prepara la mandíbula gigante y dispara un orbe violeta desde la boca, en lugar del asalto anterior. Los costes y el resto de entradas se conservan.
- **Abajo + RT:** una copia autónoma por 750. Persigue y ataca mientras controlas al cuerpo principal. Las generaciones posteriores deciden más lento, con un tope de espera; sus golpes mantienen el daño base. Seis copias simultáneas, 180 de resistencia y ocho segundos de duración son reglas de esta adaptación. Se pueden derrotar individualmente; golpear al cuerpo principal no las borra.
- **A:** Enjambre Shinju por tres barras. La apertura debe tocar al rival en el suelo y se puede bloquear, saltar o evitar por distancia. Al confirmar atacan las copias de la escena; daño total min(350, 35 % de vida máxima rival), con liberación y regreso al combate. No mata desde vida completa.
- **LB/Pausa:** carga. **Abajo + LB** con tres barras activa seis segundos de concentración, cuesta una barra y aumenta un 15 % los golpes por colisión. Conserva el cuerpo y la escala, sin regeneración ni invulnerabilidad.

Instala `Mamushi` dentro de `chars/` y añade `Mamushi/Mamushi.def` a `select.def`. También se incluye `AC_Mamushi.def` como alias si copias todos los archivos a tu carpeta antigua. [Controles Xbox](Mamushi/CONTROLES_XBOX.md) · [Instalación](Mamushi/LEEME.md) · [Créditos y adaptación](Mamushi/CREDITOS_Y_FUENTES.md).

Comprobaciones en Ikemen GO: [66 casos generales](previews/Mamushi_engine_checks.json), [18 atajos y cadenas mezcladas](previews/Mamushi_extra_checks.json), [16 casos de dash](previews/Mamushi_dash_checks.json), [dos de daño independiente a las copias](previews/Mamushi_clone_health_checks.json), [ultimate contra 500 de vida](previews/Mamushi_low_life_checks.json) y [CPU](previews/Mamushi_CPU_checks.json). Se verifican ambos lados, energía, seis copias, control del jugador durante su actividad, persistencia al recibir daño, caducidad, derribo/levantada y una ulti que acierta, falla, se bloquea o no tiene energía. Hay seis regresiones de carga, arte, sonido y ayudantes, y [dos reconstrucciones idénticas](previews/Mamushi_rebuild_checks.json).

[Conservación del arte, los originales y los otros personajes](previews/Mamushi_preservation_checks.json). SFF con 139 entradas, SND con 13 efectos no verbales, 132 acciones AIR y 101 estados. Las 80 entradas originales y los estados de los clones se conservan; se añaden 42 capas de viento, tierra y energía del Code ya aportado. La [referencia observada](source_material/Mamushi_reference/reference_analysis.json) documenta qué secuencias se adaptaron. La hoja conserva su resolución y sus límites; no se presenta como nuevo arte profesional. Las capturas de especiales, división y ulti usan audio real SDL, sin mezclar golpes o voces después. La demostración de seis copias repone energía como prueba de entrenamiento; cada copia cuesta 750 en el personaje. [Registro de capturas](previews/Mamushi_preview_checks.json).

No se ejecutó el binario exacto de Jump Force MUGEN V14 ni un mando físico. La estrategia CPU es básica y el equilibrio frente al plantel completo requiere partidas locales.

```sh
python3 tools/build_mamushi_assets.py
python3 tools/build_mamushi_runtime.py
python3 tools/validate_mamushi.py
python3 tools/test_mamushi_regressions.py
python3 tools/check_mamushi_in_engine.py /ruta/al/ikemen
MAMUSHI_EXTRA_CHECKS=1 python3 tools/check_mamushi_in_engine.py /ruta/al/ikemen
MAMUSHI_CLONE_HEALTH_CHECK=1 python3 tools/check_mamushi_in_engine.py /ruta/al/ikemen
MAMUSHI_LOW_LIFE=1 python3 tools/check_mamushi_in_engine.py /ruta/al/ikemen
MAMUSHI_CPU_CHECK=1 python3 tools/check_mamushi_in_engine.py /ruta/al/ikemen
MAMUSHI_DASH_CHECK=1 MAMUSHI_TICKS=260 python3 tools/check_mamushi_in_engine.py /ruta/al/ikemen
python3 tools/make_mamushi_previews.py /ruta/al/ikemen
python3 tools/package_mamushi.py
python3 tools/verify_mamushi_delivery.py
```


# Shibai Otsutsuki — dos formas y Shinjutsu

[Descargar Shibai](https://raw.githubusercontent.com/codeuzumaki6/MUGEN/main/Shibai_OTSUTSUKI.zip). Extrae `Shibai` dentro de `chars` y añade `Shibai/Shibai.def` a `data/select.def`. El paquete contiene sus propios estados comunes, sprites, sonidos y controles; no requiere instalar los personajes de referencia.

La túnica negra es la forma base. Abajo más LB/Pausa, con la barra llena, cambia al cuerpo azul de la izquierda durante doce segundos. Cuesta 1500, usa la misma altura corporal de 78 píxeles y vuelve automáticamente a la base. La expansión nueva tiene 24 poses articuladas por forma, asistidas por IA a partir de los dos modelos de Vahidras suministrados. Las fuentes y las adaptaciones están documentadas en [los créditos](Shibai/CREDITOS_Y_FUENTES.md).

Los normales X/Y/B son cadenas de viento y remates de tornado. Hay combos aéreos limitados a tres ataques, seis especiales direccionales, técnicas con abajo más botón, ráfagas cortantes, descargas, tormenta, repulsión y contraataques. Shibai no usa Kokugan, estacas ni cubos. RT coloca la marca de suelo 90,3 de Code; una segunda pulsación abre sus bandas cruzadas 200,24, viaja hasta la marca y la consume. Se conserva el negro con puntos blancos del video de referencia, sin las tiras verticales de la entrega anterior. Doble toque a izquierda o derecha hace un dash terrestre, y la carga muestra un aura azul animada de 24 fotogramas con ondas y partículas. En el despertar el multiplicador de daño pasa de 1.20 a 1.95, los ataques crecen un 65 %, avanzan un 15 % más rápido y cuestan el 60 %. Las nueve técnicas de viento y rayos añaden uno o dos ataques; las salidas de garra añaden un relámpago. Pulsos, contraste de tormenta y sacudidas refuerzan la forma divina sin agrandar el cuerpo. A es una ultimate con apertura bloqueable y alcance finito, con daño limitado a `min(420, floor(vida máxima rival*.42))`.

[Controles Xbox y costes](Shibai/CONTROLES_XBOX.md) · [Instalación y pruebas en V14](Shibai/LEEME.md)

Grabaciones del personaje real en Ikemen GO; especiales, despertar, marcas y ultimate conservan el audio capturado del motor, sin mezcla de golpes añadida:

- [Combos base](previews/Shibai_combos_motor.mp4) — grabación visual sin audio.
- [Especiales base con sonido](previews/Shibai_especiales_motor.mp4).
- [Ataques de la forma divina](previews/Shibai_divino_motor.mp4).
- [Activación y fin del despertar](previews/Shibai_despertar_motor.mp4).
- [Marcas de garra y viaje](previews/Shibai_garras_motor.mp4).
- [Dash con doble toque a ambos lados](previews/Shibai_dash_motor.mp4) — grabación visual sin audio.
- [Aura durante la carga de energía](previews/Shibai_carga_motor.mp4).
- [Ultimate confirmada por impacto](previews/Shibai_ultimate_motor.mp4).

Las comprobaciones cubren controles en ambos lados y formas, daño por colisión, combos, recuperación, gasto real, transformación y expiración, guardia de pie/agachada/aérea, CPU y ultimate bloqueada, saltada, fuera de alcance o sin energía. El ejecutable exacto de Jump Force MUGEN V14 para Windows y el mando físico no están disponibles en este entorno; la prueba en Ikemen no sustituye esa comprobación.

```bash
python3 tools/build_shibai_assets.py
python3 tools/build_shibai_runtime.py
python3 tools/validate_shibai.py
python3 tools/test_shibai_regressions.py
python3 tools/check_shibai_in_engine.py
SHIBAI_GUARD=1 python3 tools/check_shibai_in_engine.py
SHIBAI_LOW_LIFE=1 python3 tools/check_shibai_in_engine.py
SHIBAI_CPU=1 python3 tools/check_shibai_in_engine.py
python3 tools/make_shibai_previews.py
python3 tools/package_shibai.py
python3 tools/verify_shibai_delivery.py
```

El constructor necesita Pillow, NumPy, SciPy y las referencias conservadas en `source_material`. Los informes están en `previews/Shibai_*checks.json`; la verificación final coteja dos reconstrucciones idénticas, los píxeles de la marca de Code, todas las poses empaquetadas y los archivos previos de Eida, Pochita y Mamushi. Ese informe conserva las versiones de esos tres personajes usadas al preparar la entrega de Shibai.
