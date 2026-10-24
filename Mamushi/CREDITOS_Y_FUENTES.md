# Créditos y procedencia

- Sprites: Vahidras/Vaydra, según el nombre de la hoja y su firma. Recursos
  aportados por el usuario: `AC_Mamushi.sff`, el BMP
  `djwatsx-6d8e1066-fb60-40d4-9f1e-de69528b8c17.bmp` y el JPG de `mamushi.zip`.
  Se conservan en `source_material/Mamushi_original/` del repositorio.
- Personaje original: `misterioso924`, según `AC_Mamushi.def`. Los archivos
  incompletos se conservaron como referencia. Se reconstruyeron ataques,
  comandos y lógica de juego; se conservaron las reacciones AIR aprovechables.
- Se decodifican las 80 entradas originales de cuerpo y partes de armas del
  SFFv1, con sus colores, transparencia y ejes, a escala 1. No son 80 poses de
  cuerpo completo: incluyen piezas separadas, un fragmento de hoja y cuadros
  auxiliares que no se usan como cuerpo. No se dibujaron sprites nuevos con IA
  ni se alteraron rostros o ropa. Los retratos vacíos se sustituyeron por un
  recorte del rostro del sprite original, a 25×25 y 120×140.
- Efectos de impacto y polvo: muestras gráficas no pertenecientes a personajes,
  ya integradas en Eida desde el Nezuko aportado por el usuario. El destello
  adicional procede del acabado previo del proyecto. Se usan como capas
  aditivas, no como nuevos poderes o modificaciones del cuerpo. Véanse
  `Eida/CREDITOS_Y_FUENTES.md` y `Mamushi/assets/source.json` del repositorio.
- Sonidos no verbales: biblioteca de efectos del proyecto usada en Eida,
  incluidos el acento de activación de Code_FUNCIONAL 950,2 y golpes. Los
  efectos nuevos 1,30–33 (estiramiento, mordida, taladro y maza) se sintetizan
  con osciladores y ruido determinista. No contienen voz ni imitan actores.
- Estados comunes: copia de la biblioteca MUGEN validada del proyecto Pochita,
  derivada del `DENJI_COMMON.cns` proporcionado, con recuperación y movimiento
  corregidos. Esa copia se conserva en `source_material/Mamushi_support/`.

Referencia de animaciones de esta revisión: video `VaydraSenki.mp4` aportado
por el usuario. Se adaptan sus fases de preparación, transformación e impacto
a los cuadros originales; se documentan los intervalos en
`source_material/Mamushi_reference/reference_analysis.json`. Los nuevos
efectos de viento, tierra, explosión y esfera violeta proceden del Code de
MUGEN STARS aportado previamente: grupos 556 (11–15), 7005 (0–4),
7015 (0–8), 1235 (0–21) y 10030 (0). Se empaquetan como capas adicionales;
no sustituyen el cuerpo de Mamushi.

Los nombres de movimientos y las reglas de daño, consumo, duración, límite
de copias y retraso de decisiones son adaptaciones para un juego de pelea.
La división toma como referencia la descripción y el panel suministrados por
el usuario; no se presenta esta implementación como una simulación literal
sin límite de su poder en el manga.


Revisión conjunta: secuencias adicionales de los paquetes completos de Vaydra/Vahidras aportados por el usuario. Los atlas, metadatos y hashes de procedencia se conservan en `source_material/*_full_original` y `assets/senki/manifest.json` del proyecto. Se adaptan los pivotes y la programación de MUGEN; los cuerpos no se redibujan.
