# Revisión del combate de Pochita

El usuario considera que la versión jugable todavía resulta repetitiva. Esta revisión aborda decisiones entre golpes, continuidad de movimiento y respuesta visual. El tamaño comprimido del ZIP no es una métrica de calidad; no se añaden datos para inflarlo.

## Referencias estudiadas

Los CMD originales de Tanjiro S3, Nezuko Advanced Demon Form y Luffy G5, aportados por el usuario, se guardan sin modificar en `source_material/Combate_references/`. Tanjiro permite entrar a varios especiales desde muchos estados de ataque mediante `MoveContact`. Nezuko separa entradas de suelo, agachadas y aéreas. Luffy tiene variantes direccionales y movilidad aérea. Estos CMD por sí solos no permiten evaluar toda su animación ni el resultado visual de esos personajes.

`CHAINSAW MAN SX Mechanics.txt` documenta cancelación entre especiales diferentes y límites de malabar/guardia. Pochita adopta una segunda técnica al confirmar el golpe, pagando su coste, con límite de dos especiales en una secuencia. No se copia el multiplicador de primer golpe de SX ni sus QTE, voces, aliados o transformaciones de Denji. No se ha revisado el SFF/SND principal ausente de SX.

## Cambios concretos

- Tres etapas de normales que aceptan X, Y o B: 27 secuencias posibles, compartiendo los mismos nueve ataques, no 27 animaciones únicas. La pulsación se guarda durante el golpe. Bloqueo o fallo impiden continuar la cadena. X al final lanza, Y tritura y empuja, B salta y corta hacia el suelo.
- Ejemplos: X-Y-B, Y-B-X, B-X-Y. Las rutas que terminan en X dan un paso físico para compensar el empuje del golpe intermedio, sin ampliar cajas invisibles.
- XXX, mantener arriba al acertar el lanzador, X-Y-B en el aire: salto de persecución real y corte descendente. El rival se mueve con su propia física; no se ata, no se teletransporta ni se congela en las pruebas de esta ruta. Puede elegir recuperación según su personaje.
- X-Y, abajo adelante X, abajo atrás X: normales hacia dos especiales, con gasto total de 600. Un tercer especial pulsado durante la segunda técnica se reconoce pero se rechaza. Un nuevo ataque después de recuperar control inicia otra secuencia.
- Doce poses nuevas generadas con IA en `movilidad_y_remate.png`: cuatro para persecución, cuatro para embestida y cuatro para remate aéreo. Mismo modelo negro, cuatro brazos y bufanda roja. El constructor separa siluetas completas, usa escala compartida de 72 px en la pose neutral y eje del torso en poses aéreas.
- Cortes y sangre se emiten también en los ataques iniciales confirmados. Bloquear no genera sangre. RT usa la nueva animación de avance. Los efectos expiran y se retiran si interrumpen al personaje.

La ultimate conserva apertura bloqueable/esquivable, coste de dos barras aunque falle, ocho poses propias y límite min(500, floor(vida máxima rival / 2)). Los estados 170, 175 y 180 conservan sus controladores Null para MUGEN.

## Alcance de las comprobaciones

Las pruebas verifican comandos, colisiones físicas, daños, consumo, recuperación y límites de encadenamiento. No determinan si el personaje ya es divertido ni certifican una calidad artística profesional. Las poses generadas conservan variaciones de detalle; esta revisión no es una hoja de animación manual terminada.

Las vistas de `previews/Pochita_jugabilidad_*` son capturas reales de Ikemen GO. El audio se monta con los WAV del personaje según eventos registrados, no es captura del dispositivo de sonido. El video de demostración añade rótulos con las entradas. El binario exacto de Jump Force MUGEN V14 y el mando físico requieren prueba local.
