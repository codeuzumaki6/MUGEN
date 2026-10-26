# Jigen

Extrae `JigenKara` dentro de `chars/` y añade a `[Characters]` de `data/select.def`:

```ini
JigenKara/JigenKara.def
```

Paquete independiente para MUGEN 1.1, probado en Ikemen GO. Incluye sprites, voces, efectos y estados comunes. Vida 1300, defensa 110 y energía máxima 3000. Los controles están en `CONTROLES_XBOX.md`.

**Abajo + Pausa** con 3000 de energía activa el despertar con cuerno durante 20 segundos. Consume 1500 y tiene una recarga de 25 segundos desde su activación. Usa la transformación original del paquete. El cuerno se conserva al caminar, atacar y recibir golpes mediante una capa visual del propio sprite, ajustada a cada pose. El cuerpo sigue siendo uno solo y conserva sus colisiones. Las ráfagas pasan de tres a cinco disparos, los cubos aumentan de tamaño y daño, y el taijutsu se refuerza. Al agotarse el tiempo regresa a base cuando recupera el control.

**RB** abre una ventana de absorción de proyectiles entre los cuadros 8 y 36. Absorbe tanto proyectiles clásicos de MUGEN como helpers con atributos de proyectil, y recupera 220 de energía al confirmar una absorción; la preparación cuesta 200. Los golpes físicos y agarres siguen pudiendo interrumpirlo. No absorbe un ataque programado por otro autor como golpe físico aunque visualmente parezca un rayo.

**Abajo + B** usa Sukunahikona: reduce realmente el cuerpo al 55 % durante 0,3 segundos, avanza y recupera el tamaño antes de golpear. Las cajas para recibir golpes también se reducen; sigue siendo alcanzable por ataques bajos y medios. **Abajo + RB** deja caer un cubo sobre la posición rival. **Abajo + RT** invoca el cuenco negro y sólo lo cierra al conectar. Aplica tres impactos, 210 de daño en base o 280 en despertar, y libera al rival. Puede bloquearse y fallar por alcance; golpear a Jigen interrumpe el sellado.

**A** ejecuta la ulti del Diez Colas del atlas original: transformación, portal, invocación, carga, disparo y explosión. La apertura debe conectar y puede bloquearse. La explosión se centra sobre el rival alcanzado y toca el suelo para incluir a personajes pequeños. Ocho pulsos causan como máximo `min(650, floor(vida máxima rival × .65))` en base y `min(800, floor(vida máxima rival × .80))` en despertar. Cuesta 3000 y no consume vida propia. Si interrumpen a Jigen, cesa el daño y el rival recupera sus estados. No mata desde vida completa a un rival de 1000 de vida.

Mantener Pausa carga energía con aura roja y rosa. Doble toque a izquierda o derecha ejecuta un dash terrestre gratuito. Las dos formas pueden recibir golpes, bloquear, caer y recuperarse.

Se importaron los 154 cuadros no vacíos del paquete. Se conservan todos los originales y se separan la explosión y el cuerno como capas para MUGEN; no se generaron dibujos ni voces. Los tres cuadros vacíos o de tamaño cero se excluyen. El SFF contiene 215 entradas y el SND 68 muestras. Véase `CREDITOS_Y_FUENTES.md`.

Las pruebas automáticas y el gameplay usan Ikemen GO y audio real del motor. El ejecutable exacto de MUGEN de Windows y un mando físico no están disponibles en este entorno.
