# Himawari Uzumaki — Two Blue Vortex

Extrae `HimawariTBV` dentro de `chars/` y añade a `[Characters]` de `data/select.def`:

```ini
HimawariTBV/HimawariTBV.def
```

Paquete independiente para MUGEN 1.1, probado en Ikemen GO. Incluye sprites, voces, efectos y estados comunes. Vida 1200, defensa 105 y energía máxima 3000.

La base conserva el taijutsu y Jūken del video: patada voladora, ráfaga de palmas, combinación aérea, ataque a los tenketsu y fijación con Byakugan. RB lanza una palma del vacío; abajo + RT carga y dispara la Bijūdama original. Los golpes de Jūken reducen 180 de energía al rival al confirmar contacto.

**Abajo + Pausa**, con 3000 de energía, activa el chakra de Kurama: cabello largo, aura roja y ataques de garras originales. Consume 1500 y dura veinte segundos; la recarga desde su activación es de 25 segundos. Cambian las cadenas y los trece especiales. Las poses de movimiento y reacción de esta forma usan las posturas originales disponibles de Kurama; el ZIP no contiene una segunda hoja completa de caminar y recibir golpes. Ambas formas reciben daño, bloquean y se recuperan.

**A** ejecuta la ulti del video: activación de chakra, garras, remate contra el suelo, carga, descarga y explosión de Bijūdama. Su apertura debe conectar y puede bloquearse o fallar por alcance. Ocho impactos causan como máximo `min(600, floor(vida máxima rival × .60))` en base y `min(750, floor(vida máxima rival × .75))` en despertar. Cuesta 3000 y no consume vida propia. Interrumpir a Himawari detiene el daño y libera al rival.

Mantener Pausa carga energía con aura dorada en base y roja en despertar. Doble toque a izquierda o derecha hace un dash terrestre gratuito. Incluye tres cadenas terrestres y aéreas, con un máximo de tres ataques por salto. Consulta `CONTROLES_XBOX.md`.

Los cuerpos dibujados dentro de los efectos compuestos sólo aparecen como el jugador principal. Las palmas, tajos y explosión independientes usan recursos que no contienen otra Himawari. Cada secuencia compuesta conserva sus píxeles originales y tiene cajas de recibir golpes colocadas sobre el cuerpo.

Se conservan los 212 cuadros válidos y los 39 archivos de audio originales. Algunos efectos comunes del archivo, como los ojos de otros personajes y los cubos, permanecen importados pero no se asignan a ataques de Himawari. La entrada vacía y las voces heredadas de Kinkaku se preservan entre las fuentes; esas voces no se reproducen como diálogo. No se generaron dibujos ni voces.

Las pruebas y el gameplay usan Ikemen GO y audio real del motor. El ejecutable exacto de MUGEN de Windows y un mando físico requieren comprobación local.
