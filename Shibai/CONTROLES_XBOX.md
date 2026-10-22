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
| ↓ adelante Y | Tres estacas que se expanden al salir | 400 |
| ↓ atrás Y | Dos cubos que crecen y caen en posiciones distintas | 550 |
| ↓ adelante B | Tormenta: tres relámpagos en una franja delante | 550 |
| ↓ atrás B | Repulsión tipo Shinra Tensei hacia ambos lados | 650 |
| ↓ X | Ráfaga baja de viento | 250 |
| ↓ Y | Dos estacas bajas | 350 |
| ↓ B | Descarga eléctrica cercana | 400 |
| RB | Reflejo de un golpe físico durante una ventana breve | 450 |
| ↓ RB | Senrigan: ventana de observación y contraataque más larga | 500 |
| RT sin marca | Coloca una marca de garra delante, durante diez segundos | 300 |
| RT con marca | Viaja a esa marca y lanza un tornado desde la salida | 300 |
| ↓ RT | Retirada por marcas con tornado hacia el frente | 650 |
| A | Convergencia divina: ultimate que debe acertar | 3000 |
| Mantener LB/Pausa | Cargar energía; soltar termina | — |
| ↓ LB/Pausa con 3000 | Despertar: cambia a la forma azul | 1500 |

Para continuar los combos, pulsa el siguiente botón cuando el viento alcance
al rival. Fallar o ser bloqueado impide continuar la cadena. Los normales
terrestres también se pueden mezclar, por ejemplo X → Y → B. Las cadenas
aéreas tienen un máximo de tres ataques por salto.

Se aceptan ↓→, ↓←, los cuartos de círculo completos y las diagonales
mantenidas. Arriba salta, arriba diagonal salta avanzando, abajo agacha,
dos toques adelante corren y dos toques atrás retroceden con salto corto.

## Despertar

Exige la barra llena y gasta 1500. Dura doce segundos y tiene veinte segundos
de espera entre activaciones. Usa los sprites azules, calibrados a la misma
altura de 78 píxeles que el cuerpo base. No agranda el modelo ni coloca un
retrato sobre él.

El multiplicador de ataque pasa de 1.20 a 1.65; los proyectiles aumentan su
escala un 35 %, y los especiales cuestan el 60 % de la tabla. Vendaval,
estacas, cubos y tormenta agregan un ataque adicional. A sigue costando
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
automática. Pulsa RT una segunda vez para aprovechar su posición. Los cubos,
rayos y remolinos se crean en posiciones anunciadas y no persiguen al enemigo.
