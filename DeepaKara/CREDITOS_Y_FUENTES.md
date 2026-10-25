# Créditos y fuentes

Deepa, Kara, Naruto y Boruto pertenecen a sus autores originales. Adaptación de aficionado para MUGEN.

- **Sprites de ambas formas y sus técnicas:** paquete `DEEPA.zip`, aportado por el usuario, carpeta «Deepa Kara by VayDra». Se importan los 134 cuadros válidos de Deepa desde los atlas `Kinkaku`, `Kinkaku_Skill2` y `KakashiFlog`. Se preservan los archivos fuente completos en `source_material/Deepa_original`.
- **Voces y efectos de Deepa:** 29 archivos de `Audio/Deepa` y `Audio/Effect`, convertidos a WAV PCM para MUGEN. No se generaron ni clonaron voces.
- **Referencia de animación y ataques:** video aportado por el usuario, «NARSEN | Naruto Senki Mod | Sprite Deepa Inner Kara | Share». Los XML originales también se consultan como referencias de secuencia.
- **Recursos comunes:** 24 efectos de audio no verbales y gráficos de impacto y carga del proyecto, incluidos en el paquete. No requiere instalar a Jura ni a otro personaje.
- **Adaptación, controles, colisiones y pruebas:** Codex. No se generó arte de Deepa con IA.

Los cuadros se recortan de los atlas originales y se ajustan sus puntos de apoyo. MUGEN usa paletas indexadas en este SFF; los PNG fuente se conservan sin redibujar. Los proyectiles móviles usan el disco original y un recorte del cubo original sin el cuerpo de Deepa.

El atlas de transformación también contiene 16 cuadros de otro personaje con nombres `KakashiFlog_*`. Se conservan en el material fuente, pero se excluyen del SFF jugable para evitar que aparezca otro cuerpo en sus animaciones. La armadura no trae cuadros propios de daño o caída: se mantienen sus poses originales y se rota el cuerpo durante el derribo.

Los registros `assets/sprites.json` y `assets/sounds.json` del repositorio identifican los recortes, ejes y audios utilizados. Las cajas de colisión, el daño y los tiempos se adaptan al combate de MUGEN.
