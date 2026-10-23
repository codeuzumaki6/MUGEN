# Mamushi Shinju — combate reconstruido

Extrae la carpeta `Mamushi` de `Mamushi_SHINJU.zip` dentro de `chars/`.
Añade `Mamushi/Mamushi.def` a `[Characters]` en `data/select.def`. Selecciona
esa entrada; la versión anterior `AC_Mamushi` seguirá siendo otro personaje
si todavía está instalada. Mantén juntos todos los archivos de esta carpeta.

Si prefieres conservar la entrada antigua de selección, copia todo el contenido
de esta carpeta dentro de la carpeta anterior: se incluye `AC_Mamushi.def`
como alias compatible, con referencias a los archivos nuevos. Guarda antes
una copia de tu instalación anterior.

Consulta `CONTROLES_XBOX.md`. A física es la ulti; LB/Pausa carga chakra;
↓RT genera copias autónomas. Los botones internos de MUGEN son diferentes.

## Lo que incluye

- Movimiento, dash por el suelo con ←← / →→, salto vertical/diagonal, agachado, guardia, daño, caída,
  levantada automática, presentación y victoria.
- Tres cadenas terrestres de tres etapas y sus continuaciones mezcladas.
  Tres familias aéreas, hasta tres golpes por salto. Remates que lanzan o
  derriban, con sonido, pausa de impacto, polvo y vibración breve.
- Seis especiales direccionales usando las extensiones, mandíbulas, mazas,
  taladros y espinas de la hoja. Ahora las transformaciones tienen preparación,
  extensión y recogida, con ráfagas en tres alturas, raíz cazadora e impactos
  de maza contra el suelo, basados en el video de Vaydra. RT usa la mandíbula
  gigante que carga y lanza un orbe violeta. Técnicas con abajo + X/Y/B, RB/RT y abajo
  + RB/RT. Sus activaciones tienen un sonido propio, aunque el golpe falle.
- División de ↓RT: hasta seis copias que persiguen y atacan sin controlar al
  jugador. Tienen salud propia, se pueden derrotar y siguen presentes al
  golpear al cuerpo principal. Duración, resistencia y coste están en controles.
- Ultimate con A: apertura bloqueable y evadible, ataque de copias y liberación
  segura del rival. Daño limitado a min(350, 35 % de vida máxima); tres barras.
- Concentración temporal con ↓LB, conservando el mismo cuerpo y tamaño.

## Arte y archivos

Se mantiene el dibujo original de la hoja. El SFF contiene 139 entradas: las
80 originales de cuerpo/partes, una referencia segura de reposo, dos retratos
recortados y 56 efectos. No se generaron cuerpos con IA ni se agrandaron las
poses de combate. El reposo solo usa 0,4–6. Los fragmentos de cabeza, el
rectángulo auxiliar y la tira con varias figuras no se reproducen como cuerpo.

SFF v2.0.1.0, SND con 13 muestras no verbales, 132 acciones AIR y 101 estados
incluidos los comunes. La hoja conserva su resolución y sus límites de
animación; mejorar el combate no convierte los cuadros existentes en nuevos
dibujos ni garantiza el acabado de otro autor.

## Pruebas y límites

La validación comprueba archivos DEF, SFF/SND decodificados, referencias AIR,
estados y comandos, expresiones MUGEN 1.1, cuadros de recuperación finitos y
ausencia de controles de prueba en los archivos entregados. Se contrasta la
integridad de los sprites originales y se valida el ZIP ya extraído.

Las pruebas de entrada y colisión se realizan en Ikemen GO sobre copias
instrumentadas: comandos en ambas orientaciones, combos, energía, copias,
interrupción del cuerpo principal, daño a las copias, caída/levantada y ulti
que acierta, falla, se bloquea o carece de energía. Los informes y videos están
en `previews/Mamushi_*` del repositorio. Las grabaciones con sonido usan salida
real SDL; no añaden golpes o voces en una mezcla posterior.

No se ha ejecutado el binario exacto de Jump Force MUGEN V14 ni un mando físico.
El equilibrio frente al plantel completo requiere partidas locales. La CPU
usa los mismos estados y colisiones; su estrategia es básica.

Prueba local sugerida: caminar/saltar/agacharse, X-X-X y Y-Y-Y, cargar con LB,
↓RT y moverte mientras la copia golpea, golpear una copia con el rival, recibir
un derribo y levantarte, y usar A tanto cerca como fuera de alcance.
