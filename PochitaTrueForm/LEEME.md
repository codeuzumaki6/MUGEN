# Pochita True Form — combos y remates para MUGEN 1.1

Sustituye `chars/PochitaTrueForm` completa por la carpeta de `PochitaTrueForm_CORREGIDO.zip`. Agrega `PochitaTrueForm/PochitaTrueForm.def` a `[Characters]` en `data/select.def` si todavía no está. Reinicia el juego.

## Corrección de carga en MUGEN

Se corrigió el error «Need at least one state controller» de los estados 170, 175 y 180. Son poses de final de ronda que ahora contienen un controlador `Null` válido, sin alterar los ataques. El constructor incluye la corrección y el validador rechaza cualquier estado sin controladores en CNS o CMD. Cinco pruebas de regresión reproducen y rechazan estados vacíos; las 119 pruebas de combate de Ikemen GO volvieron a pasar. El ZIP se valida también después de extraerlo. No se ejecutó el binario exacto de MUGEN del usuario.

## Cambios jugables

- X → X → X: tres cortes y lanzamiento del rival, 152 de daño en el muñeco de prueba.
- Y → Y → Y: extensión, triturado multigolpe y empuje, 180 de daño.
- B → B → B: giro, salto corto y corte contra el suelo, 205 de daño.
- X → Y → B en el aire: cadena con derribo, 172 de daño.
- Nueve especiales direccionales entre 250 y 750 de energía; RB cuesta 250 y RT 750. Cada barra equivale a 1000.
- Vida 1250, defensa 110, carga con LB de 18 unidades por tick hasta 3000. Los combos normales generan energía al conectar.

Las continuaciones requieren acertar y volver a pulsar el botón. Bloquear o estar fuera de alcance corta la cadena. Los especiales ofensivos pueden cancelar un normal de suelo confirmado. Los nombres de movimientos son descripciones de adaptaciones físicas, no nombres oficiales de técnicas del manga. No se implementa el borrado permanente de conceptos ni regeneración ilimitada.

## Ultimate con A

**Consume 2000 al activarla, incluso si falla o la bloquean.** Con menos de dos barras no se ejecuta. La embestida debe conectar; bloquear, saltar o quedarse fuera de alcance evita la secuencia y su daño. Tiene preparación y recuperación vulnerables al fallar.

Al acertar usa ocho poses nuevas: despliegue de los cuatro brazos, cortes cruzados, barrido y remate final. Cinco contactos sincronizan motosierras, arcos de corte, sangre, pausas de impacto y lanzamiento. La imagen del manga fue una referencia de acción y no se muestra en el ataque.

El daño total se limita al menor entre **500 y el 50 % de la vida máxima del rival**, redondeado hacia abajo. Un rival con 1000 de vida recibe 500; uno con 500 recibe 250. La ultimate sola no mata desde la vida completa. Puede rematar a alguien previamente herido. La secuencia libera al rival y ambos vuelven a sus estados normales.

## Arte y audio

Armadura negra robusta, casco dentado, cuatro brazos con motosierras y bufanda intestinal roja, según las referencias del usuario. Se generaron con IA las hojas de movimiento, ataques, daño y los nuevos remates. El SFF contiene 149 entradas: 135 de cuerpo (126 poses fuente distintas), 12 efectos y dos retratos estándar. Las repeticiones cierran ciclos y comparten movimientos. El reposo conserva seis cuadros propios. El tamaño del cuerpo permanece calibrado al reposo de 72 píxeles; no se estiran individualmente los cuadros. Las cajas ofensivas siguen las motosierras visibles.

Hay diez sonidos no verbales: siete muestras seleccionadas del DENJI suministrado y tres mezclas adicionales de motores, cortes e impactos. No se incluyen voces humanas ni voces generadas. Las hojas fuente, ejes y procedencia están en el repositorio. El arte generado conserva pequeñas variaciones de detalle entre cuadros; necesita revisión artística para alcanzar la consistencia de dibujo manual cuadro por cuadro.

## Comprobaciones y prueba local

Pasaron 119 escenarios de entradas y colisiones en Ikemen GO, una prueba de CPU y dos pruebas de ultimate contra un rival de solo 500 de vida. Se comprueban los costes exactos, presupuesto mínimo, cadenas X/Y/B, bloqueos y fallos, nueve especiales, atajos diagonales, defensa, movimiento, salto, carga, seis derribos con recuperación y ultimate acertada, bloqueada, saltada y fuera de alcance en ambas orientaciones. Los efectos aparecen al acertar y expiran; la sangre no aparece al bloquear. El validador revisa SFF/SND, referencias, funciones de MUGEN 1.1, recuperación finita y alcance visible; una regresión confirma que rechaza una caja ofensiva exagerada.

Los GIF y fotogramas proceden del motor real. El audio de los MP4 se monta con las muestras del personaje y los tiempos registrados de sus eventos; no es una grabación de la salida de audio del motor. Las entradas automáticas se aplican solo a copias de prueba. No se ha ejecutado el binario exacto de Jump Force MUGEN V14 ni conectado el mando físico a este entorno. El equilibrio contra todo el plantel requiere partidas locales.

Prueba en tu juego: caminar, agacharse, saltar; X/Y/B tres veces al conectar; cadena aérea; especiales; RB ante un golpe; RT; cargar con LB. Usa A acertada, bloqueada y desde lejos: siempre gasta dos barras si se activa. Con menos de dos barras no debe salir. Recibe un barrido y un lanzamiento: debe levantarse y volver a atacar. Repite mirando hacia ambos lados. Si A o LB no coinciden, revisa el mapeo global antes de modificar el CMD. Consulta `CONTROLES_XBOX.md`.
