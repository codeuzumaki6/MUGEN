# Mamushi — controles Xbox

Mapeo del mismo mando usado para Eida y Pochita: X=a, Y=b, B=c, A=x,
RB=y, RT=z y LB/Pausa=s. Las direcciones de la tabla son relativas a Mamushi:
adelante apunta al rival y atrás se aleja. Mirando a la derecha, adelante es →.

| Entrada física | Movimiento | Energía |
| --- | --- | ---: |
| X, X, X | Brazo, extensión y remate de maza que lanza | 0 |
| Y, Y, Y | Mandíbulas y remate de taladro | 0 |
| B, B, B | Cadena de maza y golpe descendente | 0 |
| X/Y/B en el aire | Cadena aérea de hasta tres golpes; se pueden mezclar | 0 |
| ↓ → X | Avance con brazo extensible, hasta tres contactos | 350 |
| ↓ ← X | Raíz cazadora: emerge del suelo, golpea y se retrae | 500 |
| ↓ → Y | Mordidas de la mandíbula transformada | 500 |
| ↓ ← Y | Embestida con brazo taladro | 650 |
| ↓ → B | Maza espinada con avance y remate | 650 |
| ↓ ← B | Tres ráfagas de tres espinas, a distintas alturas | 500 |
| ↓ X | Golpe bajo de maza que derriba | 250 |
| ↓ Y | Dos espinas a media distancia | 400 |
| ↓ B | Taladro ascendente que avanza por el suelo | 500 |
| RB | Guardia mutante: ventana breve de contraataque al contacto | 500 |
| RT | Bramido Shinju: mandíbula gigante y orbe violeta | 1000 |
| ↓ RB | Retirada con mordida; debe estar cerca para acertar | 350 |
| **↓ RT** | **División: una copia autónoma** | **750** |
| **A** | **Enjambre Shinju: ultimate que debe acertar** | **3000** |
| ←← / →→ | Dash corto hacia ese lado, por el suelo | 0 |
| Mantener LB/Pausa | Cargar chakra; soltar termina la carga | 0 |
| ↓ LB/Pausa con la barra llena | Concentración temporal, mismo cuerpo y tamaño | 1000 |

También se aceptan los cuartos de círculo completos (↓ ↘ → / ↓ ↙ ←) y
mantener la diagonal correspondiente antes de pulsar X/Y/B. Los normales
terrestres se pueden mezclar: por ejemplo X → Y → B. Pulsa la continuación
cuando el golpe conecte. Bloquear o fallar corta la continuación. Los finales
lanzan o derriban; no son cadenas infinitas. Arriba salta, arriba diagonal
salta avanzando y abajo agacha. Dos toques seguidos a izquierda o derecha
hacen un dash corto hacia ese lado; puedes enlazarlo con un ataque. Un solo
toque camina. El dash no consume chakra ni concede invulnerabilidad.

La raíz elige un punto del suelo al iniciar el ataque; no sigue al rival
después. RT prepara la mandíbula, carga la esfera y la dispara desde su boca.
A corta distancia también puede conectar la mordida; el orbe está pensado
para media distancia. Ambos se pueden bloquear o esquivar.

## División

Cada pulsación válida de ↓RT genera una copia junto a Mamushi. Busca al rival,
se acerca hasta su alcance físico y alterna brazo, mordida y maza por su cuenta.
Puedes caminar, atacar o cargar mientras pelea. Las generaciones posteriores
tardan más en decidir, con un máximo de 40 ticks de espera; sus golpes de
brazo/mordida/maza conservan 32/42/40 de daño base.

Reglas de esta adaptación: hasta seis copias activas, ocho segundos de duración
y 180 de resistencia por copia. Se pueden golpear y derrotar individualmente.
Golpear al Mamushi que controlas no borra sus copias. El final de la ronda sí
las limpia. Se puede crear otra al quedar un espacio libre; pulsar ↓RT con
seis copias no ejecuta RT normal ni cobra un ataque distinto.

## Ultimate y concentración

A cuesta tres barras aunque falle. El ataque inicial avanza y debe tocar al
rival en el suelo: se puede bloquear, saltar o evitar por distancia. Al
confirmar aparecen copias que atacan por turnos con los sprites de la hoja.
El daño total es el menor entre 350 y el 35 % de la vida máxima rival. No mata
desde vida completa. Las copias visuales de esa escena se retiran al terminar;
las copias autónomas de ↓RT son una habilidad distinta.

La concentración de ↓LB exige 3000 de energía, gasta 1000, aumenta un 15 % el
daño por colisión durante seis segundos y tiene 15 segundos de espera entre
activaciones. Conserva los sprites y la escala; solo aplica un tinte leve de
chakra. No regenera vida ni concede invulnerabilidad. El daño de la ulti
mantiene su límite durante ese efecto.


Consulta [la revisión conjunta](REVISION_CONJUNTA.md) para los cambios de recepción, animación y CPU.
