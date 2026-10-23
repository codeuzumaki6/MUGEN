# Jura Shinju — MUGEN 1.1

Adaptación jugable de la hoja de Vahidras / Vaydra. Conserva sus 36 poses a escala nativa: cuerpo, capa, puños, patadas, madera y disparo ocular. El video Vaydra Senki.mp4 se usó como referencia visual; el combate está programado para MUGEN.

## Instalación

1. Extrae la carpeta `JuraShinju` del ZIP dentro de `chars`.
2. Añade `JuraShinju/JuraShinju.def` al apartado `[Characters]` de `data/select.def`.
3. Consulta CONTROLES_XBOX.md. Las letras Xbox dependen de la asignación de tu juego.

El nombre interno y visible es **Jura Shinju**. La carpeta y los archivos usan el prefijo `JuraShinju` para evitar el conflicto con otro Jura instalado.

La carpeta es independiente; no necesita Code, Kawaki ni otros personajes instalados. Incluye archivos DEF, AIR, CMD, CNS, SFF, SND y estados comunes.

## Combate

Tres cadenas de tres golpes, cadenas aéreas, remates que lanzan, espinas y raíces que crecen, bijūdama de dos tamaños, francotirador ocular, ráfaga de mini bijūdamas, asedio ocular y marcas de garra que se colocan y se consumen al viajar. Los ataques usan colisiones reales, sonidos de activación, impactos y recuperación.

Tiene 1300 de vida y 3000 de energía. La amplificación dura 12 segundos: aumenta el daño y abarata técnicas. La activación crea un capullo de raíces que se cierra y se abre mientras recupera hasta 180 de vida; un golpe puede interrumpir esa curación. La ultimate consume tres barras incluso si falla. Su proyectil inicial toma la altura del rival y se puede bloquear o esquivar; sólo al conectar comienza la secuencia con Jura sentado sobre un trono de raíces y la esfera disparada en diagonal. El daño total es el menor entre 450 y el 45% de la vida máxima rival, y puede rematar si ya estaba herido.

## Compatibilidad y pruebas

Formato MUGEN 1.1, SFF 2.0.1, estados comunes incluidos. Se comprueban entradas equivalentes al mando, colisiones, bloqueo, caída y levantada, coste de energía y limpieza de efectos en Ikemen GO. La ejecución exacta en el pack Windows Jump Force MUGEN V14 queda pendiente de probar en ese equipo.

No sustituye los personajes anteriores. Los videos de demostración muestran este personaje ejecutándose en el motor, con el sonido capturado del juego.

En esta revisión RB y las bijūdamas apuntan al cuerpo de objetivos pequeños y agachados; abajo + RB usa una postura erguida y tres disparos. La victoria tiene cuatro poses nuevas de sacar, abrir y leer un libro.
