# Naruto adulto KCM / Barión

El video y el ZIP del usuario muestran el KCM dorado y el modo Barión rojo. La adaptación emplea esos dibujos originales para dos bancos de animaciones y dos movesets. Barión se activa con abajo + Pausa, requiere la barra completa, consume 1500 de energía y dura veinte segundos; no consume vida.

El paquete contiene 74 archivos originales y 215 cuadros de atlas. Se incorporan los 198 cuadros útiles. Se conservan sin usar en combate el cuadro vacío `nol_01`, el logotipo `vaydra` y quince recortes de pantalla `FutonSRK*`. El tamaño real de los PNG se usa para leer sus regiones, pues el segundo plist declara un tamaño desactualizado.

Los brazos giratorios se dibujan como efectos independientes. Los cuadros de explosión que llevan al propio Naruto tienen una versión derivada que retira esa silueta y rellena su zona con el brillo de los lados. El impacto de Ōdama conserva la explosión del suelo con un desvanecimiento que excluye al caster aéreo incrustado. Así se puede mantener al personaje principal a su tamaño correcto. La esfera de carga de Ōdama se recorta de los cuadros originales. Los colores opacos de los efectos y su luz semitransparente se exportan por separado para conservar el dorado y el azul.

Los cuadros originales RGBA quedan intactos, con CRC y SHA-256. La versión ejecutable usa SFF 2.01 indexado RLE8, de ocho bits. Los sonidos suministrados se convierten a WAV PCM mono y se incluyen en el SND. La referencia a `RikudoNaruto_skill5.og` del XML contiene una extensión errónea; el archivo `.ogg` real se conserva y se importa.

KCM usa Rasengan, puños extensibles, taijutsu de chakra, brazos giratorios, Ōdama aéreo y el avatar de Kurama. Barión usa sus propios desplazamientos, golpes de palma, ráfagas, ganchos y remates. El XML original se consulta como referencia de secuencias; sus órdenes de invulnerabilidad y contraataque automático no se incorporan.

Las dos ultis necesitan contacto real y tienen ocho pulsos, con un máximo de 300/360 frente a un rival de 1000 de vida. Las poses de impacto de Barión están alineadas con los pulsos. El enemigo conserva su propio dibujo y vuelve a sus estados al acabar o al interrumpir a Naruto.
