# Créditos y fuentes

Sumire, Nue, Naruto y Boruto pertenecen a sus autores originales. Adaptación de aficionado para MUGEN.

- **Sprites, hoja, voces y efectos propios:** VaydraSenki, según el archivo `Note.xml` del paquete `Sumire Kakei.zip` aportado por el usuario.
- **Fuentes preservadas:** los 61 archivos completos se guardan en `source_material/Sumire_original`, incluido el texto original de créditos.
- **Agradecimientos originales:** Zakume, suscriptores, amigos, canales de reseñas y autores de los efectos utilizados por VaydraSenki.
- **Referencia de combate:** `_Share_ Sprite Sumire Kakei + SpriteSheet Asset frame __ NARUTO SENKI MOD __.mp4`, aportado por el usuario, y los XML de animación del paquete.
- **Recursos comunes:** impactos y aura móvil y 24 efectos de audio no verbales del proyecto, incluidos en este paquete.
- **Adaptación, controles, colisiones y pruebas:** Codex.

Los atlas llamados `Tsunade` y `Tsunade_Skill` contienen los dibujos de Sumire y Nue: sus nombres proceden de los espacios que sustituyen en Naruto Senki. Se importan los 203 cuadros no vacíos conservando sus píxeles RGBA. `SumireNol` tiene tamaño cero; los tres cuadros `Slug_Move` son transparentes y no se utilizan. Todos permanecen entre las fuentes originales.

La transformación en Nue grande sigue las secuencias `skill05`, `skill10`, `skill11` y `skill12` del paquete. El cuerpo grande se controla como jugador y usa los cuadros disponibles de Nue para movimiento, ataque, guardia y reacción al daño. Sumire reaparece al terminar la transformación. El Nue pequeño tiene cuerpo, vida, colisiones y duración propios.

Los cuadros de Suiton, combos y aura que ya incluyen a Sumire se reproducen en el cuerpo principal. Los proyectiles de agua, el sello y el humo son recursos separados. La ulti de base muestra a Sumire y al Nue invocado; en despertar se utiliza el propio cuerpo de Nue, sin añadir otro Nue gigante.

Se convierten a WAV PCM mono los 48 archivos de audio del ZIP y se incluyen junto a 24 efectos comunes. Las técnicas llaman a las voces y sonidos identificados de la carpeta `SumireKakei`. Los alias llamados Tsunade se conservan como fuentes, sin utilizarlos como diálogos de otra persona. No se generan ni se clonan voces ni se copia la música del video.

No se generó arte nuevo con IA ni se redibujaron los cuadros originales. El SFF utiliza paletas indexadas; se ajustan ejes, escala, animaciones, colisiones y tiempos para MUGEN. El refuerzo, los costes, la duración y los límites de daño son reglas de esta adaptación jugable. El SFF contiene 243 entradas y el SND 72 muestras.

`assets/sprites.json`, `assets/sounds.json` y `previews/SumireKakei_source_checks.json` del repositorio permiten rastrear cada cuadro y audio y comprobarlos contra el ZIP original.
