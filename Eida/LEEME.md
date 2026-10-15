# Eida — Boruto: Two Blue Vortex

Carpeta para MUGEN 1.1 / Jump Force MUGEN V14. Copia `Eida` dentro de `chars/` y añade `Eida/Eida.def` en `[Characters]` de `data/select.def`. Sustituye la carpeta anterior por la nueva completa.

Consulta **CONTROLES_XBOX.md**: incluye las nueve combinaciones con abajo/diagonales y X/Y/B, las técnicas de RB y RT, los combos normales, la carga, el despertar y la ulti con A.

## Cambios de esta revisión

- Aura del despertar: 13 cuadros del efecto de energía de la referencia Nezuko, con color azul y mezcla aditiva del motor. Mantiene los sprites normales de Eida y evita el arco rígido anterior.
- Daemon: sprites reducidos al 68% del tamaño anterior, colisiones ajustadas, aparición junto a Eida, carrera con alcance limitado, ataques a corta distancia y desaparición gradual. Se puede interrumpir golpeándolo o golpeando a Eida.
- Once técnicas con consumo de energía y entradas físicas de Xbox. Los controles se invierten de acuerdo con la orientación.
- Cadenas normales en X, Y y B; launcher con Daemon y continuaciones aéreas.
- Encantamiento rasante y ascendente con colisión, bloqueo, alcance finito y aturdimiento de 45 ticks.
- Sonidos de aparición, desplazamiento, guardia, lanzamientos e impactos; chispas y polvo del combate.
- Nuevos estados en `Specials.cns`, referenciados en `Eida.def`. Conservar ese archivo junto con los demás.

## Comprobaciones

- SFF v2.0.1.0: 155 sprites, paletas y datos binarios validados. Retrato de combate 25×25 y retrato de selección 120×140.
- SND: 20 muestras mono PCM de 16 bits.
- AIR: 106 acciones con referencias válidas. El idle usa exclusivamente sus seis cuadros de reposo.
- 110 estados entre `Eida.cns`, `Specials.cns` y `common1.cns`; referencias estáticas de estados y sonidos verificadas.
- Ikemen GO nightly: 42 escenarios con entradas direccionales y botones simulados que atraviesan el CMD real, tanto mirando a derecha como a izquierda. Incluyen atajos diagonales, combos, consumo de energía, bloqueo de Encantamiento, asistencia que falla al esquivar y técnicas durante el despertar. El informe reproducible está en el repositorio (`previews/engine_moveset_checks.json`).

Las pruebas del motor usan copias temporales e instrumentación fuera de la carpeta entregada. No se pudo ejecutar el binario exacto de Jump Force MUGEN V14 del usuario ni comprobar físicamente su mando Xbox. El equilibrio frente a todo su plantel requiere partidas locales.

## Procedencia y límites visuales

Eida conserva los sprites recuperados de los recursos del usuario y los cuadros adicionales de movimiento. Daemon usa las 16 poses reconstruidas anteriormente, ahora a escala de ayudante. Esta revisión reutiliza esos dibujos en nuevas secuencias; no agrega una hoja nueva de ilustraciones. El nivel artístico de Sumire sigue siendo la referencia de acabado y no se declara alcanzado.

Omnipotencia conserva los paneles originales del manga. Las voces pertenecen a los fragmentos femeninos del MP3 japonés suministrado. Consulta `CREDITOS_Y_FUENTES.md`.
