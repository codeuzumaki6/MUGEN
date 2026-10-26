# Créditos y fuentes

Jigen, Naruto y Boruto pertenecen a sus autores originales. Adaptación de aficionado para MUGEN.

- **Sprites y audio:** `Jigen.zip`, aportado por el usuario, carpeta «Jigen rep Jiraiya». Los archivos originales completos, incluido `Notes.txt`, se conservan en `source_material/Jigen_original`.
- **Autor:** Vaydra. **Hoja:** Alex, según `Notes.txt`.
- **Agradecimientos originales:** Zakume, Mashashi, AmirZ, fuentes de efectos, amigos, canal y suscriptores del autor.
- **Referencia de combate:** `videoplayback.mp4`, aportado por el usuario, y las secuencias XML del paquete.
- **Recursos comunes:** gráficos de impacto y aura y 24 efectos de audio no verbales del proyecto, incluidos en el paquete.
- **Adaptación, controles, colisiones y pruebas:** Codex.

Los atlas llamados `Jiraiya` y `Jiraiya_Skill` contienen los dibujos de Jigen: esos nombres corresponden al personaje que sustituyen en Naruto Senki. Se importan sus 154 cuadros no vacíos sin redibujarlos. Se excluyen `Jigenol` (tamaño cero), `Jiraiya_Float_03` y `Jiraiya_wake_06` (transparentes). Los fragmentos de ropa de recuperación se conservan como fuentes y no se usan como cuerpos independientes.

Las diez imágenes grandes de explosión se conservan completas. Además, se recortan veinte capas exactas para separar al invocador de la explosión y colocar el impacto en la posición del rival, a ras del suelo. El cuerno se recorta del cuadro original `Jiraiya_Skill05_Trans_04`; el motor lo enlaza a la cabeza de cada pose durante el despertar. La pose quieta y la transformación usan directamente el cuerpo con cuerno del autor. Las capas visuales carecen de ataques y de cuerpos adicionales.

Se convierten a WAV PCM 44 archivos originales: los 12 de `Audio/Jigen` y 32 efectos relacionados con las técnicas. Se conserva también la biblioteca completa de efectos del ZIP entre las fuentes, aunque no se empaquetan cientos de sonidos ajenos al moveset. Los alias llamados Mei y Jiraiya no se llaman como diálogos. Los XML citan `JigenNatk.mp3` y `Jigen_hurt.ogg`, pero esos archivos no vienen en el ZIP; no se inventaron voces para sustituirlos.

No se generó arte ni se clonaron voces con IA. Los recortes PNG conservan los píxeles RGBA de las fuentes. Para el SFF se convierten a paletas indexadas. Los ejes, tiempos, cajas, cuerno por capas y reglas de daño se adaptan a MUGEN. Los nombres de técnicas describen su implementación jugable y no afirman reglas de canon.

`assets/sprites.json`, `assets/horn_anchors.json` y `assets/sounds.json` del repositorio permiten rastrear los cuadros, sus puntos de apoyo y cada audio original. `previews/JigenKara_source_checks.json` registra la comprobación contra el ZIP del usuario.
