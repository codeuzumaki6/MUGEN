# Créditos y fuentes

- Personaje y universo: Boruto / Naruto, sus autores y titulares. Adaptación de fans.
- Hoja corporal y madera: **Vahidras / Vaydra**, “Juura Shinju”, 29 de noviembre de 2024: https://www.deviantart.com/vahidras/art/Juura-Shinju-1127927142 . PNG original 500×1300, SHA256 `ba763257d89940e5ab90428085d2f7d0036abb94837bf935168ca3170a6bb808`.
- Referencia adicional de raíces: https://www.deviantart.com/vahidras/art/Jura-V2-sprite-Nzc-godtree-massive-thorn-roots-1229915979 . El JPG con tablero dibujado se conserva sólo como referencia; no se coloca como panel ni como sprite en combate.
- Referencia audiovisual aportada por el usuario: `Vaydra Senki.mp4`, 68.254 segundos. Su jugabilidad de Naruto Senki se adapta a controles y colisiones nativos de MUGEN.
- Efectos complementarios: bancos seleccionados del Code de MUGEN STARS que aportó el usuario y recursos de impactos/energía ya presentes en el proyecto Mamushi/Shibai. Conserva la autoría de sus respectivos creadores; no se atribuyen a Vaydra. Las bandas negras de garra con puntos claros proceden del Code original.
- Sonidos no verbales: biblioteca del proyecto y cuatro efectos de chakra, disparo y explosión sintetizados para esta adaptación. Sin voces generadas ni doblaje imitado.
- Programación de combate, estados comunes, ensamblado y validación: Codex, adaptación para el usuario.

Por petición del usuario, únicamente los tres tonos rojos de los iris pasan a violeta claro de Rinnegan normal, también en los retratos. Se conservan posiciones, contornos y todos los demás píxeles.

Las 36 poses corporales originales se recortan de la hoja sin redibujarlas ni cambiar su escala. Se elimina el fondo verde y se indexan las paletas a un máximo de 255 colores opacos por sprite para el SFF. Los ejes se anclan al cuerpo y al suelo para que puños extendidos y patadas no desplacen toda la figura.

La implementación se centra en bijūdama ocular, Mokuton y marcas de garra. La ultimate y la amplificación son adaptaciones de jugabilidad. No utiliza el Kokugan de Kawaki ni sus cubos negros. La esfera gris de la referencia fan no se usa como bijūdama.


La victoria usa las poses originales 0,24, 0,19 y 0,20, conservando sus píxeles, cara, capa, proporciones y escala. El libro es una pieza separada con cuatro cuadros de cerrado, apertura y página; se ancla a la mano sin sustituir el cuerpo. Sólo ese objeto se genera con IA para la victoria. Las 36 poses originales y su corrección de ojos se conservan. La pose sentada de la ultimate, el trono y las cuatro fases del capullo son los recursos suplementarios anteriores. Fuentes y parámetros en `source_material/Jura_generated`, `assets/supplemental.json` y `tools/build_jura_assets.py`. El sonido de papel se conserva.


Revisión conjunta: secuencias adicionales de los paquetes completos de Vaydra/Vahidras aportados por el usuario. Los atlas, metadatos y hashes de procedencia se conservan en `source_material/*_full_original` y `assets/senki/manifest.json` del proyecto. Se adaptan los pivotes y la programación de MUGEN; los cuerpos no se redibujan.
