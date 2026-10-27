# Sumire Kakei

Extrae `SumireKakei` dentro de `chars/` y añade a `[Characters]` de `data/select.def`:

```ini
SumireKakei/SumireKakei.def
```

Paquete independiente para MUGEN 1.1, probado en Ikemen GO. Incluye sprites, voces, efectos y estados comunes. Vida 1200, defensa 105 y energía máxima 3000. Conserva la apariencia de Sumire del paquete de VaydraSenki.

En base utiliza Suiton, kunai y las combinaciones del video. Suireiha dispara cuatro proyectiles de agua; RT dispara uno más potente. El muro, los cortes y la cascada reproducen las secuencias completas sobre el cuerpo principal. Las animaciones con Sumire dibujada no se utilizan como proyectiles ni como personajes adicionales.

**RB** invoca a Nue pequeño. Sigue al rival y ataca por su cuenta mientras puedes mover y controlar a Sumire. Tiene 180 de vida, puede ser golpeado y dura como máximo siete segundos. **Abajo + RB** ordena un asalto inmediato; lo invoca si hace falta. Hay un solo familiar activo. Desaparece al iniciar la ulti o al transformarse en Nue gigante.

**Abajo + Pausa** con 3000 de energía activa el despertar: el sello de Gozu Tennō y el aura dan paso a **Nue gigante, controlado directamente por el jugador**, siguiendo el cambio de cuerpo del paquete original. Consume 1500, dura veinte segundos y tiene 25 segundos de recarga desde su activación. El cuerpo de Sumire vuelve cuando termina el tiempo y recupera el control. Nue tiene zarpazos, cargas, retroceso con embestida, salto, rugido, mordida espectral, sello y pisotones. Sus cuadros, escala y cajas corresponden al cuerpo grande; puede recibir golpes, bloquear y recuperarse.

**A** ejecuta la ulti del sello y Nue. En base, Sumire canaliza el aura e invoca al Nue grande para el asalto. En despertar, el propio Nue controlado realiza la secuencia. La apertura debe conectar y puede bloquearse o fallar por alcance. Ocho impactos causan como máximo `min(550, floor(vida máxima rival × .55))` en base y `min(700, floor(vida máxima rival × .70))` en despertar. Cuesta 3000 y no consume vida propia. Interrumpir al atacante detiene el daño y libera al rival.

Mantener Pausa carga energía con aura violeta. Doble toque a izquierda o derecha hace un dash terrestre gratuito. Ambas formas tienen tres cadenas terrestres y aéreas, hasta tres ataques por salto y trece especiales. Las entradas están en `CONTROLES_XBOX.md`.

Se importaron los 203 cuadros válidos de Sumire y Nue y los 48 audios del ZIP. Se preservan todos los archivos originales; sólo se excluyen de las animaciones una entrada de tamaño cero y tres cuadros transparentes. No se generaron dibujos ni voces. Véase `CREDITOS_Y_FUENTES.md`.

Las pruebas y el gameplay usan Ikemen GO con audio real del motor. El ejecutable exacto de MUGEN de Windows y un mando físico no están disponibles en este entorno.
