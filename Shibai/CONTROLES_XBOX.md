# Shibai — mando Xbox

Mapeo usado por este proyecto: X=a, Y=b, B=c, A=x, RB=y, RT=z y
LB/Pausa=s. «Adelante» significa hacia el rival; las direcciones cambian al
cambiar de lado. No se modifica tu configuración global del mando.

| Entrada | Movimiento | Energía base |
| --- | --- | ---: |
| X, X, X | Cadena de viento frontal con remate de tornado | 0 |
| Y, Y, Y | Cadena de viento de avance lento y elevación final | 0 |
| B, B, B | Barridos de viento y tornado que derriba | 0 |
| X/Y/B en el aire | Hasta tres ataques aéreos de viento; se pueden mezclar | 0 |
| ↓ adelante X | Vendaval: dos tornados que avanzan | 300 |
| ↓ atrás X | Ciclón: dos remolinos en posiciones fijas delante | 450 |
| ↓ adelante Y | Ráfaga cortante: tres cortes de viento | 400 |
| ↓ atrás Y | Trueno doble: dos descargas en posiciones distintas | 550 |
| ↓ adelante B | Tormenta: tres relámpagos en una franja delante | 550 |
| ↓ atrás B | Repulsión tipo Shinra Tensei hacia ambos lados | 650 |
| ↓ X | Ráfaga baja de viento | 250 |
| ↓ Y | Remolino bajo: dos ráfagas a ras de suelo | 350 |
| ↓ B | Descarga eléctrica cercana | 400 |
| RB | Reflejo de un golpe físico durante una ventana breve | 450 |
| ↓ RB | Senrigan: ventana de observación y contraataque más larga | 500 |
| RT sin marca | Coloca una marca de garra sobre el suelo, durante diez segundos | 300 |
| RT con marca | Entra por una garra, sale por la marca y lanza un tornado; consume la marca | 300 |
| ↓ RT | Retirada por marcas con tornado hacia el frente | 650 |
| A | Convergencia divina: ultimate que debe acertar | 3000 |
| Mantener LB/Pausa | Cargar energía con aura azul, ondas y partículas; soltar termina | — |
| ↓ LB/Pausa con 3000 | Despertar: cambia a la forma azul | 1500 |
| ← ← | Dash hacia la izquierda, también al cambiar de lado | 0 |
| → → | Dash hacia la derecha, también al cambiar de lado | 0 |

Para continuar los combos, pulsa el siguiente botón cuando el viento alcance
al rival. Fallar o ser bloqueado impide continuar la cadena. Los normales
terrestres también se pueden mezclar, por ejemplo X → Y → B. Las cadenas
aéreas tienen un máximo de tres ataques por salto.

Se aceptan ↓→, ↓←, los cuartos de círculo completos y las diagonales
mantenidas. Arriba salta, arriba diagonal salta avanzando, abajo agacha,
dos toques a izquierda o derecha hacen un dash corto por el suelo. Se suelta
entre ambos toques; no requiere mantener la segunda pulsación. Funciona en
ambas formas, termina automáticamente y respeta los bordes del escenario.

La carga tiene una envoltura de energía animada de 24 fotogramas detrás del
cuerpo, ondas en el suelo y partículas que suben. Suelta LB/Pausa para apagarla;
también se corta al recibir un golpe, al llenar la barra o al terminar la ronda.

## Despertar

Exige la barra llena y gasta 1500. Dura doce segundos y tiene veinte segundos
de espera entre activaciones. Usa los sprites azules, calibrados a la misma
altura de 78 píxeles que el cuerpo base. No agranda el modelo ni coloca un
retrato sobre él.

El multiplicador de ataque pasa de 1.20 a 1.95; los proyectiles aumentan su
escala un 65 % y avanzan un 15 % más rápido. Los especiales cuestan el 60 %
de la tabla. Las nueve técnicas de viento y relámpagos agregan una o dos
descargas o remolinos; las salidas de garra añaden un relámpago. El lanzamiento
produce un pulso divino, contraste de tormenta y sacudidas más intensas.
El cuerpo conserva su tamaño y la presión azul se dibuja detrás. A sigue costando
3000 y conserva su límite de daño. La transformación es temporal, recibe
golpes y puede caer y levantarse con ambos cuerpos.

## Ultimate

El disparo inicial tiene alcance finito. Se puede bloquear, saltar o evitar
por distancia. Solo un impacto reciente contra un rival en el suelo inicia
la secuencia de ojo, viento, tormenta y distorsión. Consume 3000 aunque falle.
El daño total es el menor entre 420 y el 42 % de la vida máxima rival; no mata
desde vida completa. El rival conserva sus propias animaciones y recupera
su sistema de estados al terminar.

La marca de RT se coloca físicamente: no sigue al rival ni lo golpea de forma
automática. Pulsa RT una segunda vez para aprovechar su posición. Dura diez
segundos o hasta usarla; tras cruzarla, RT puede colocar otra. Se muestran las
marcas bajas originales 90,3 de Code y sus bandas cruzadas 200,24 durante la
entrada y la salida, como en el video suministrado. Conservan el negro y los
puntos blancos; el tránsito incluye apertura, desaparición y reaparición.
La CPU también coloca y cruza garras para acercarse
desde lejos. Los rayos y remolinos se crean en posiciones
anunciadas y no persiguen al enemigo. No hay estacas, cubos ni Kokugan.


Consulta [la revisión conjunta](REVISION_CONJUNTA.md) para los cambios de recepción, animación y CPU.
