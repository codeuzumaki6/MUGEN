# Sprites y audio completos — 24/10/2026

Base protegida: c6d04d94934c2e83efa869744587f13eda270b59. Los movimientos, costes, daño, voces anteriores y ventanas de colisión de los ataques del cuerpo se conservan.

`tools/build_full_pack_revision.py` reconstruye siete personajes desde esa base. Los atlas/plists de Vaydra se leen como datos y se importan como fases distintas: cuerpo, carga, proyectil, impacto y transformación. No se ejecutan los XML ni se copian sus valores de daño. Los PNG originales de Jura reenviados por el usuario son idénticos a los del paquete anterior; el problema era que sus secuencias no se estaban utilizando.

- Mamushi: la mandíbula usa dos poses originales alineadas; los nueve cuadros de carga, los dos de vuelo y los quince de impacto se dibujan por separado. La silueta de Mamushi se retira del impacto utilizando su cabello y su alfa original, sin recortar la explosión con un borde rectangular.
- Jura: siete cuadros de carga, cinco de vuelo y diez de explosión de Bijūdama, cuatro del rayo ocular y siete del Mokuton. Los efectos se separan del pequeño Jura incrustado en el atlas.
- Ryū: las fases de cuerpo y efectos se separan con la silueta original, conservando manos y pies; los 47 cuadros de la técnica de las alas se distribuyen entre apertura, vuelo/ataque y explosión.
- Hidari: sus 28 cuadros del Susanoo amarillo original se usan en manifestación, postura, espada y desaparición. Se mantiene la lógica de los nueve ataques existentes de Sasuke.
- Mitsuki: animaciones originales del rayo, carga, serpientes verdes, sellos y combate de ambos modos.
- Matsuri: capa, patada, agua y erupción originales; la forma sin capa mantiene su propio cuerpo.
- Eida: abrazo de diez cuadros a tamaño nativo, efecto original de Omnipotencia con mezcla aditiva detrás de la pareja y efectos de Senrigan. Las voces japonesas existentes no se reemplazan.

Los bancos originales contienen también duplicados, rectángulos vacíos y recursos de otros personajes (como el atlas de 1×1 de Matsuri, ShinoUnused y algunos fondos de Jura). Se conservan como fuente, pero no se usan como dibujos de los luchadores.

Los sonidos seleccionados se conservan en sus formatos originales y se convierten a PCM mono de 22050 Hz para SND. El constructor puede usar los ZIP adjuntos o las copias originales seleccionadas que se incluyen en `assets/full_pack/sound`. Los manifiestos registran rectángulos, pivotes, máscaras y SHA-256.

Verificación: `tools/verify_full_pack_revision.py`, contratos de combate nativos, 954 pruebas de recepción y 72 pruebas de doble dash. Las grabaciones se hacen en directorios nuevos para evitar que el motor reutilice nombres de capturas anteriores y llevan el audio SDL real. `previews/full_pack_video_manifest.json` vincula los clips finales. Las pruebas se realizan con Ikemen GO y sintaxis de MUGEN 1.1.
