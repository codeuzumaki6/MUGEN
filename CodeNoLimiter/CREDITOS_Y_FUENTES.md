# Créditos y fuentes

Code, Naruto y Boruto pertenecen a sus autores originales. Adaptación de aficionado para MUGEN.

- **Sprites:** `CodeTBV rep kankuro V.1.17 (SFILE.MOBI).zip`, aportado por el usuario. Autor identificado por el paquete y video: Vaydra / VaydraSenki. Se conservan sus 17 archivos originales en `source_material/CodeNoLimiter_original`.
- **Referencia de combate:** `Share Sprite CODE NO LIMITER. Free Kaguya 1.17 VaydraSenki.mp4`, aportado por el usuario. Se revisa la sección de Code; los personajes adicionales mostrados después no se incorporan.
- **Audio de Code:** `Code.snd` del Code de MUGEN STARS aportado previamente por el usuario, junto a sus CNS y DEF. Se conservan intactos en `source_material/Shibai_Code_reference`.
- **Recursos comunes:** gráficos de impacto y aura móvil y 24 efectos de audio no verbales del proyecto, incluidos en este paquete.
- **Adaptación, controles, colisiones y pruebas:** Codex.

Los nombres Kankuro, ThirdKazekage y Karasu pertenecen a los espacios que se sustituyen en Naruto Senki. El contenido visual de los atlas Kankuro y Kankuro_Skill corresponde a Code, Claw Grimes, marcas, escenarios y efectos. Se importan sus 241 cuadros no vacíos sin redibujarlos. Se excluye `CodeNol_01`, una entrada de tamaño cero. El atlas Karasu contiene 23 cuadros de marionetas ajenas a Code: permanece entre las fuentes y no se importa al personaje jugable.

Se reproducen los cuadros con Code sobre el cuerpo principal, incluida la secuencia completa de la columna morada. Las marcas, el árbol, el ejército y los impactos conjuntos usan capas propias. Las criaturas autónomas utilizan sus dibujos de Grime, con vida, recepción de golpes y duración finita. Las poses parciales de criaturas enterradas se usan sólo en sus secuencias de aparición o ataque.

El nuevo ZIP no contiene archivos de audio, aunque sus XML citan rutas de sonidos. Se seleccionan 13 muestras del SND anterior de Code para voces, reacciones y garra, y se convierten a PCM mono para el nuevo SND. Los originales permanecen intactos. No se extraen voces mezcladas con la música del video, ni se generan o clonan voces.

No se generó arte con IA. Los PNG importados conservan los píxeles RGBA originales; el SFF utiliza paletas indexadas. Se ajustan los puntos de apoyo, animaciones, cajas, tiempos y reglas para MUGEN. El refuerzo de Karma y los límites de daño y duración son decisiones de esta adaptación jugable.

Los registros `assets/sprites.json`, `assets/sounds.json` y `previews/CodeNoLimiter_source_checks.json` del repositorio identifican cada cuadro y sonido y verifican las fuentes. El SFF contiene 281 entradas y el SND 37 muestras. El ZIP se instala de forma independiente y no necesita los personajes usados como referencia.
