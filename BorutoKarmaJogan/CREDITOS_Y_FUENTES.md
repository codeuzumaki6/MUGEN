# Créditos y fuentes

**Vaydra**: sprites y hoja, según `Note❗.txt` del archivo original. **AmirZ**: asistencia. Agradecimientos originales: Zakume, Mashashi, Haickal, Kayla, fuentes de efectos, amigos, canales y suscriptores. Programación para MUGEN, adaptación de controles, colisiones, empaquetado y pruebas: Codex.

Material aportado por el usuario:

- `✅Sprite BorutoJougan by Vaydra.part1.rar`, `.part2.rar` y `.part3.rar`.
- `Share❗ Sprite Boruto Karma Jougan Gameplay Skill Moveset.mp4`.
- XML, PLIST y trece archivos de audio enviados por separado.

Los tres volúmenes pasan la prueba del RAR y la suma CRC de sus 618 archivos. El contenido completo está en `source_material/Boruto_original/full_archive/`; los archivos sueltos y versiones distintas también se conservan. Las huellas están en `archive_checks.json` y `source.json`. Los volúmenes RAR no se duplican dentro del ZIP jugable ni del repositorio.

Se importan 663 recortes válidos de las ocho hojas de sprites asociadas a Boruto y sus efectos. Se conservan sus píxeles RGBA en los PNG de construcción, sin repintado. Las imágenes de SFF se indexan a 256 colores y se almacenan con RLE8 y un cuadro sin compresión; se verifica la igualdad de los píxeles indexados tras descomprimir. Los puntos de apoyo de los cuadros compuestos se obtienen mediante comparación con el cuerpo original y se revisan en el motor.

La biblioteca conserva nombres heredados como Pain, Nagato, Tenten, AsuraPath y DevaPath. Los dibujos principales muestran a Boruto, y los nombres identifican espacios reemplazados del juego original. Los recortes heredados ajenos y cuadros vacíos no se usan como personajes ni habilidades adicionales. Se emplean las invocaciones y ataques del moveset fan creado por el autor; no se presenta esa selección como una lista canónica del manga.

Se incluyen once audios de la carpeta `Audio/BorutoJogan` y 56 efectos originales seleccionados para las técnicas. Se convierten a PCM mono de 22 050 Hz, conservando los originales. Las 548 muestras generales de la carpeta Effect permanecen entre las fuentes y no se importan todas al SND. Los efectos no verbales comunes del proyecto conservan sus créditos en el repositorio. No se generan voces ni ilustraciones.

Las animaciones con Boruto dentro del dibujo se usan sobre el cuerpo principal. El clon de sombra es una entidad de apoyo intencional, a escala completa, con daño recibido y duración limitada. Las ondas, electricidad, ojos y otros efectos independientes se separan de los cuadros del personaje.

La corrección de contacto conserva los PNG RGBA originales. Para los 58 efectos de viento se convierte su alfa en color premultiplicado para el dibujo aditivo de MUGEN; así no desaparecen los trazos cuya opacidad original es menor del 50 %. Los puntos de apoyo revisados están en `design/boruto_karma_jogan/reviewed_geometry.json`. La reproducción del fallo se documenta a partir del video de MUGEN aportado por el usuario, sin ejecutar contenidos de las fuentes.

Se restablecen las secuencias originales de `Mon/RasenShot.xml`, `Mon/FutonRasen.xml`, `Mon/MonsterTanah.xml` y la sección `--uzu` del cuarto especial del XML principal. Los cuatro cuadros adicionales del tornado son recortes exactos de `Pain_Skill04_95` a `98`, dejando fuera al Boruto que ya dibuja el jugador. El corte izquierdo se desvanece al convertir el viento a color aditivo; los PNG originales y los recortes RGBA se conservan sin repintado.
