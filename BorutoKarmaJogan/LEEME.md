# Boruto Uzumaki — Karma y Jōgan

Extrae `BorutoKarmaJogan` dentro de `chars/` y añade a `[Characters]` de `data/select.def`:

```ini
BorutoKarmaJogan/BorutoKarmaJogan.def
```

Paquete independiente para MUGEN 1.1, probado en Ikemen GO. Vida 1200, defensa 105 y energía máxima 3000. Incluye sprites, voces, efectos y estados comunes.

Conserva el Boruto con capa negra, espada y marcas azules del paquete original de Vaydra. La base combina kenjutsu, Rasengan, Shiden, tajos ascendentes, kunai, disparos, caída con Rasengan, Fūton y la invocación de serpiente que aparece en el video. Es una adaptación del moveset del mod aportado, incluyendo sus técnicas de creación del autor.

**Abajo + Pausa** con 3000 activa la resonancia de Karma y Jōgan. Consume 1500, dura veinte segundos y tiene 25 segundos de recarga desde su activación. Aparece el corte de Jōgan original y electricidad azul alrededor del cuerpo. La apariencia conserva los sprites originales; el paquete no contiene una segunda hoja completa de caminar y recibir golpes. Cambian los trece especiales: rayos, Uzuhiko, garras de viento, Rasengan doble y un campo de resonancia más potente. Las cadenas y los proyectiles también se refuerzan.

**Abajo + Y** crea un clon de sombra de tamaño completo. Se acerca al rival y ataca por su cuenta con Rasengan mientras puedes seguir controlando a Boruto. Sólo puede existir uno; tiene 120 de vida y dura como máximo tres segundos. El rival puede aturdirlo y destruirlo. Repetir el comando ordena su asalto si ya existe. El clon desaparece al comenzar la ulti, morir Boruto o terminar la ronda. Esta copia es una invocación intencional, separada de los efectos de los especiales.

**A** ejecuta la ulti de Jōgan del video: apertura, pilares, tormenta eléctrica, tornados y remate con Rasengan doble y campo de resonancia. La apertura debe acertar, tiene alcance finito y admite guardia. Ocho impactos causan como máximo `min(650, floor(vida máxima rival × .65))` en base y `min(800, floor(vida máxima rival × .80))` en despertar. Cuesta 3000 y no consume vida propia. Si interrumpen a Boruto, se detiene el daño y el rival recupera sus propios estados.

Doble toque a izquierda o derecha hace dash terrestre gratuito. Mantener Pausa carga energía con aura; el despertar mantiene electricidad azul visible y amplía el aura al cargar. Hay tres cadenas terrestres y aéreas, con un máximo de tres ataques por salto. Consulta `CONTROLES_XBOX.md`.

Se importan 663 cuadros originales de Boruto y efectos, más los efectos comunes y retratos del proyecto. Se usan las once muestras de voz de la carpeta del personaje y 56 efectos originales seleccionados. Los 618 archivos del RAR y los archivos sueltos aportados se preservan como fuentes. Los cuadros vacíos y recortes heredados de otros espacios del juego se excluyen de las animaciones. No se generan dibujos ni voces.

Los cuadros que ya contienen a Boruto se dibujan como el cuerpo principal; las ondas y proyectiles independientes no contienen otro Boruto. Las imágenes indexadas se almacenan con RLE8 y un cuadro sin compresión, sin modificar sus píxeles indexados. Las colisiones, guardia, recuperación, caducidad y liberación del rival se comprueban dentro del motor.

La validación nativa utiliza Ikemen GO. El ejecutable exacto de MUGEN de Windows y un mando físico requieren comprobación local.

Actualización de animaciones y contacto: sustituye la carpeta anterior completa y reinicia MUGEN. Se corrigen 160 puntos de apoyo, el despegue y la altura de los Rasengan grandes, las colisiones de sus esferas y la pose de agacharse y aterrizar. Uzuhiko concentra viento alrededor del cuerpo, necesita conectar la palma y provoca una reacción giratoria con liberación al terminar o interrumpirse. Los 58 efectos de viento conservan ahora su transparencia como color para dibujarse de forma aditiva. Los rivales se dibujan delante de los efectos grandes para ver la reacción al golpe.
