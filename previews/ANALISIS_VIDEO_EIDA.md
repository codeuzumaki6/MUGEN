# Referencia de combate suministrada por el usuario

Archivo analizado: `videoplayback_SBDrg0Mw.mp4`, 640×360, 30 fps, 8:24.57.
Enlace suministrado: https://www.youtube.com/watch?v=Z3Coy0qJvmI&t=58s

Se revisaron muestras de toda la grabación y secuencias con mayor frecuencia
al inicio, alrededor de 00:58, 04:00 y 05:25. Los tiempos son aproximados.
El video muestra una versión ajena en desarrollo: no son capturas de esta Eida.

| Tiempo | Observación visible | Aplicación o límite en nuestra versión |
| --- | --- | --- |
| 00:08–00:09 | Carrera inclinada, con el cabello detrás del cuerpo. | Se habilita el dash; los dibujos actuales siguen siendo de caminata. Falta dibujar un ciclo de carrera coherente. |
| 04:11–04:12 | Rival teñido de rosa y señal «Love» durante la acción de Eida. | El corazón que ya viajaba y colisionaba ahora deja una señal sobre la cabeza únicamente al acertar. Se conserva bloqueo, evasión y aturdimiento finito. |
| Alrededor de 04:22 | Ayudante pequeño con pelo verde y ropa roja, en ataque bajo. | Daemon continúa como ayudante independiente; esta revisión conserva las poses que ya teníamos. No se extrajeron sprites del video. |
| Alrededor de 05:28–05:37 | Ataques y asistencias enlazados con impactos, desplazamiento y remates. | Se corrige la orientación del segundo golpe de X y el enlace aéreo X → Y → B, incluyendo pulsaciones durante hitpause. No se afirma haber reproducido la coreografía completa. |

En la grabación hay otros ayudantes y técnicas de Sasuke. Su retrato/cinemática
se distingue, por ejemplo, cerca de 04:00. No todos los rayos, fuego o efectos
azules presentes pueden atribuirse a Eida. Tampoco se incorporó el ayudante rubio
como un movimiento nuevo: el encargo del usuario sigue siendo Eida con Daemon.

El HUD de esta referencia muestra «KONAN» junto al personaje de Eida. Eso no
demuestra qué código, autor o archivos originales utiliza. El MP4 tampoco aporta
las colisiones, entradas CMD, poses tapadas ni transparencias originales.

Todavía faltan dibujos de carrera, transiciones y acciones ofensivas de Eida,
y más poses consistentes de Daemon para alcanzar ese acabado. Esta revisión
es una corrección jugable de la carpeta existente, sin una hoja nueva de arte.

`Eida_combo_revision_video.gif`, `Eida_encanto_confirmado_motor.gif` y
`Eida_dash_motor.gif` sí son capturas nuevas de nuestra carpeta en Ikemen GO.
Se generan con `python3 tools/make_video_reference_previews.py /ruta/al/motor`.
El ensayo aéreo mantiene a ambos luchadores a altura fija para aislar entradas
durante hitpause; no demuestra por sí solo que toda persecución aérea natural
sea un combo garantizado.
