# Ouga / Yatsume

Extrae `OugaYatsume` dentro de `chars/` y añade esta línea a `data/select.def`:

```ini
OugaYatsume/OugaYatsume.def
```

Personaje independiente para MUGEN 1.1, probado en Ikemen GO. Incluye sus estados comunes, sprites, voces y efectos. El ejecutable exacto de MUGEN de Windows y el mando físico no están disponibles en este entorno.

La base es **Yatsume con capa negra**. **Abajo + Pausa** con 3000 de energía cambia a **Yatsume sin capa con Raiton**, utilizando las dos apariencias y sus animaciones del paquete y video de Vaydra. Consume 1500, dura 20 segundos y tiene 25 segundos de recarga desde su activación. Al terminar el tiempo vuelve a la capa cuando recupera el control. Las dos formas conservan sus cajas para recibir golpes, guardia y recuperación.

En base, abajo-adelante + X invoca a la marioneta enmascarada de Ouga. Sigue al enemigo y ataca por sí sola mientras controlas a Yatsume. Los vórtices, lazo, bomba y corte ordenan técnicas a esa misma marioneta; si no está presente, la invocan. Hay una sola marioneta activa, con 300 de vida y una duración máxima de 15 segundos. Puede recibir golpes, quedar aturdida y ser destruida. La bomba consume la marioneta y no consume vida de Yatsume.

El despertar cambia el moveset a asaltos de chakra rosa, látigo azul, golpes de Raiton y prisión eléctrica, manteniendo las técnicas de apoyo dimensional del video. Los cuadros que ya contienen a Yatsume se reproducen sobre el personaje, sin colocar otro cuerpo como proyectil. La capa se conserva durante los ataques y el daño de la base. Como no hay cuadros de caída con capa, se rota su cuerpo original durante el derribo; la forma sin capa usa los cuadros de daño y caída incluidos.

**A** ejecuta una ulti dimensional con los escenarios originales. La base combina el pilar azul y el derrumbe de la simulación; el despertar combina el látigo y los pilares y golpes de Raiton. Ambas requieren un impacto real y aplican ocho pulsos. El daño máximo es `min(600, floor(vida máxima rival × .60))` en base y `min(750, floor(vida máxima rival × .75))` en despertar. Cuestan 3000 y no consumen vida propia. La guardia y el alcance evitan la captura; un golpe que interrumpa a Yatsume libera al rival y detiene el daño. La marioneta espera durante la ulti.

Mantener Pausa carga energía con aura azul y morada. Doble toque a izquierda o derecha hace un dash terrestre gratuito. `CONTROLES_XBOX.md` contiene los trece especiales de cada forma y las cadenas normales y aéreas.

Se importaron los 231 cuadros válidos de los atlas y los 56 audios de sus carpetas originales. Sólo se excluye `OugaNol`, una entrada de tamaño cero. No se generó arte ni voces con IA. Los créditos y las adaptaciones están documentados en `CREDITOS_Y_FUENTES.md`.
