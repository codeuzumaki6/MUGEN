# Pochita True Form — rediseño visual para MUGEN 1.1

Sustituye `chars/PochitaTrueForm` completa por la carpeta del ZIP `PochitaTrueForm_REDISENO.zip`. Agrega `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si todavía no está. Reinicia el juego.

Esta revisión usa el modelo robusto de armadura negra, casco dentado, cuatro brazos con motosierras y bufanda intestinal roja de las imágenes de referencia del usuario. El arte nuevo se generó con IA a partir de esa propuesta visual. Hay 118 poses fuente distintas, organizadas en 127 entradas de cuerpo del SFF y dos retratos estándar. Algunas poses se reutilizan para cerrar ciclos o compartir movimientos; no se presentan como 127 dibujos diferentes. Cada hoja se calibra con sus poses neutrales a una altura de 72 píxeles, sin estirar individualmente los cuadros. El reposo conserva seis cuadros propios y no recorre los ataques.

Se renovaron reposo, caminar, carrera, agacharse, salto, ataques de suelo y aire, especiales, ultimate, daño y caída. Las rotaciones aéreas usan el torso como eje. Los alcances de los golpes se limitaron al extremo visible de las motosierras. Ascenso, Barrido y Rasante necesitan cercanía; pueden fallar desde lejos aunque gasten energía. La estocada tiene un avance corto para acompañar su alcance. El lanzamiento del tercer X mantiene al rival más cerca del encuadre.

Se conservan los combos X/Y/B y la cadena aérea, nueve especiales direccionales, defensa con respuesta en RB, asalto en RT, carga en LB y ultimate con A. Los siete efectos de motosierras, cortes e impactos siguen en el SND; no se incluyen voces humanas de Denji. `CONTROLES_XBOX.md` contiene las entradas y sus costes.

La ultimate cuesta 3000 y su embestida debe conectar. Bloquearla, saltarla o quedar fuera de alcance evita la secuencia. Al acertar, realiza seis cortes, causa 350 y libera al rival con un lanzamiento. Los movimientos son adaptaciones físicas de Pochita; sus nombres descriptivos no son nombres oficiales de nuevas técnicas del manga. No se implementa el borrado permanente de conceptos ni regeneración ilimitada.

## Validación y límites

Pasaron 84 escenarios de entradas y colisiones en Ikemen GO: comandos, atajos diagonales, combos, defensa, movimiento, saltos, carga y consumo, seis derribos con recuperación, ultimate acertada/bloqueada/esquivada/fuera de alcance y seis comprobaciones de que los cortes cortos fallan a distancia. Otra prueba ejercitó la CPU. El validador revisa SFF/SND, referencias, recuperación finita, funciones de MUGEN 1.1 y que las cajas ofensivas no sobrepasen las hojas visibles de los sprites empaquetados. Una prueba alteró una caja para confirmar que el validador rechaza el alcance invisible.

Los GIF son capturas reales del motor y no tienen audio. Las entradas automáticas se aplicaron solo a copias de prueba, fuera de esta carpeta. No se ha ejecutado el binario exacto de Jump Force MUGEN V14 ni conectado el mando físico a este entorno. El escenario y las barras de las capturas son distintos de los de tu juego.

El arte generado conserva variaciones pequeñas de detalle entre cuadros y necesita revisión artística si se busca la consistencia de una hoja dibujada manualmente cuadro por cuadro. Las pruebas de colisiones no certifican calidad artística. La IA es básica y el equilibrio contra todo el plantel requiere partidas locales.

Prueba local: caminar, agacharse y saltar; X tres veces al conectar; salto X→Y→B; los nueve especiales; RB ante un golpe; RT; cargar LB; A acertada, bloqueada y desde lejos. Recibe un barrido y un lanzamiento: debe levantarse y volver a atacar. Repite mirando hacia ambos lados. Si A o LB no coinciden, revisa el mapeo global del mando antes de modificar el CMD.
