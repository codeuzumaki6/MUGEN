# Pochita True Form — MUGEN 1.1

Copia esta carpeta completa a `chars/PochitaTrueForm`. Agrega `PochitaTrueForm/PochitaTrueForm.def` a la sección `[Characters]` de `data/select.def`. Reinicia el juego. Esta entrega es un personaje independiente; no reemplaza a Eida ni a los Denji originales.

Se usan 127 poses de cuerpo de la hoja original de Ducksysys compartida por Spider-Monkie, más dos retratos estándar. La armadura tiene una paleta negra y gris y la bufanda intestinal es roja, siguiendo las referencias del usuario. Todos los cuadros tienen la misma escala; las poses de ataque están separadas del reposo. Camina, corre, salta, se agacha, bloquea, recibe golpes y se levanta después de derribos mientras siga vivo.

X, Y y B enlazan golpes al conectar y recibir otra pulsación. Hay tres ataques aéreos, nueve especiales de abajo/dirección y botón, defensa con respuesta en RB, asalto en RT y carga en LB. Consulta `CONTROLES_XBOX.md`. Los golpes producen sonidos de cortes, impactos y motores de motosierra; no se incluyeron diálogos humanos de Denji.

La ultimate con A consume 3000. Tiene preparación y una embestida que debe alcanzar al rival: bloquearla, saltarla o quedar fuera de alcance evita la secuencia. Al conectar, sujeta al rival durante seis cortes y un lanzamiento, causa 350 y lo libera. Es una adaptación física de las motosierras de Pochita, sin poderes de otros personajes. Los nombres de los movimientos describen su función jugable, no afirman ser nombres oficiales de técnicas del manga. No se implementó el borrado permanente de conceptos ni regeneración ilimitada.

## Comprobaciones y límites

Se verificaron 78 escenarios de entradas y colisiones en Ikemen GO: comandos y atajos diagonales, combos, especiales, defensa, salto neutral y diagonal, caminar y soltar, gasto/carga de energía, seis derribos con recuperación y nueva acción, y ultimate que acierta o falla en ambas orientaciones. Una comprobación adicional ejercitó la ofensiva de la CPU. El validador comprueba los archivos SFF/SND, referencias, animaciones de recuperación finitas y expresiones compatibles con MUGEN 1.1.

Las capturas GIF proceden del motor y no contienen sonido. Las pruebas automatizadas usan copias instrumentadas; los archivos entregados no incluyen controles de prueba. El escenario y las barras de Ikemen no son los de Jump Force MUGEN V14.

No se ha ejecutado el binario exacto de tu Jump Force MUGEN V14 ni conectado tu mando físico a este entorno. La IA es básica y el equilibrio contra el plantel completo requiere partidas locales. La hoja original tiene 127 poses, algunas similares; no se inventaron cuadros faltantes ni se presentan estas animaciones como un trabajo original del autor de la hoja.

Prueba local recomendada: X tres veces al conectar; saltar y enlazar X→Y→B; abajo+X/Y/B; los seis especiales diagonales; cargar LB; RB ante un golpe; A frente al rival, contra bloqueo y desde lejos. Recibe un barrido y un lanzamiento: debe levantarse y volver a atacar. Comprueba ambos lados del escenario. Si A o LB no coinciden, revisa el mapeo global del mando descrito en los controles antes de modificar el CMD.
