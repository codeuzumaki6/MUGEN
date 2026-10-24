# Hidari Shinju — controles

**X=a · Y=b · B=c · A=x · RB=y · RT=z · Pausa/LB=s.** Adelante y atrás dependen de hacia dónde mire el personaje.

## Forma base

| Entrada | Ataque | Energía |
|---|---|---:|
| X/X/X, Y/Y/Y, B/B/B | Cadenas de tres golpes, con remate | 0 |
| X/Y/B en el aire | Cadena aérea de hasta tres golpes | 0 |
| ↓↘→ + X | Chidori con avance y electricidad en la mano | 350 |
| ↓↙← + X | Garra de madera | 450 |
| ↓↘→ + Y | Corriente de Chidori | 500 |
| ↓↙← + Y | Prisión de raíces | 650 |
| ↓↘→ + B | Garra ascendente | 450 |
| ↓↙← + B | Cadena de madera | 550 |
| ↓ + X / Y / B | Barrido / palma / ramas | 200 / 300 / 400 |
| RB | Senbon eléctrico | 200 |
| RT, luego RT | Coloca una marca y sale por ella atacando | 250 + 200 |
| ↓ + RB | Pilar eléctrico | 650 |
| ↓ + RT | Salida por marca de garra | 400 |
| A | Ulti de Chidori, marcas y presa de madera | 3000 |

## Despertar: Susanoo amarillo de Sasuke BTM

Inicia con **↓ + Pausa/LB y mantén Pausa aproximadamente 1,7 segundos**. Requiere 3000 de energía y consume 1500 cuando se manifiesta. Soltar Pausa antes cancela la carga sin consumir energía. Dura 20 segundos; el enfriamiento empieza al activarse y dura 25 segundos. Puede recibir golpes y su carga se puede interrumpir.

Se usan el dibujo y los cuadros originales de Sasuke BTM, recoloreando la paleta del Susanoo a amarillo. Sus tres golpes y seis especiales son los del personaje aportado. Durante el despertar se ve únicamente el Susanoo. Al terminar reaparece Hidari con su cuerpo original y su Rinnegan azul.

| Entrada | Ataque original del Susanoo | Energía |
|---|---|---:|
| X | Puño del Susanoo | 0 |
| Y | Patada del Susanoo | 0 |
| B | Espada ascendente | 0 |
| ↓↘→ + X | Chidori del Susanoo, nueve impactos | 500 |
| ↓↙← + X | Mountains Cutter: corte de montaña y onda | 700 |
| ↓↘→ + Y | Shinra Tensei: repulsión con anillo expansivo | 600 |
| ↓↙← + Y | Chibaku Tensei: lluvia de meteoritos del original | 800 |
| ↓↘→ + B | Amaterasu / Kagetsuchi no Tsurugi: hoja de llamas negras | 650 |
| ↓↙← + B o A | Indora no Ya: arco y flecha de Indra | 3000 |
| ↓ + X / Y / B | Acceso a los mismos tres golpes del Susanoo | 0 |
| RB / RT | Acceso a corte de montaña / Shinra Tensei | 700 / 600 |
| ↓ + RB / RT | Acceso a meteoritos / Kagetsuchi | 800 / 650 |

Chidori queda en abajo adelante + X en ambas formas, como pidió el usuario; por eso se intercambian las dos entradas de X respecto al Sasuke original. Se conserva el conjunto de ataques. La programación adapta alcance, colisiones, costes y daño a Hidari.

Indra es una flecha que debe alcanzar físicamente al rival: puede bloquearse y esquivarse. Consume 3000 incluso si falla. Al acertar, su daño máximo es **min(450, 45 % de la vida máxima del rival)**; la explosión no suma daño adicional. Puede rematar a un rival herido, pero no derrotarlo desde vida completa. La ulti de base mantiene su límite de min(420, 42 %).

En ambas formas: **→→ / ←←** hacen dash sin gasto, mantener **Pausa/LB** carga energía y mantener atrás permite bloquear. Las cadenas aéreas de Hidari siguen disponibles durante el despertar. El Susanoo amarillo y sus poderes son una adaptación fan solicitada.
