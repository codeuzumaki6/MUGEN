# Naruto BTM: material entregado y adaptación

El ZIP original contiene 73 archivos: tres atlases con sus plist, un PNG opcional de vista HD, XML de movimientos, 59 muestras de audio y datos auxiliares. Se conserva cada archivo con su CRC y SHA-256. Los XML y el Lua incluidos se tratan como datos de referencia; no se ejecutan sus instrucciones.

El video muestra cinco familias: Rasengan cargado y su choque, clones con Doton, combo de puño y dos patadas de chakra, Rasenshuriken arrojado con explosión, y transformación/avatar de Kurama con ataque de área. El montaje adjunto permite revisar esas secuencias.

Se importan 160 cuadros útiles de los 164 del atlas. `Float_02`, `Float_03`, `KnockDown_05` y `KnockDown_06` contienen capturas de la cámara del juego, por lo que se excluyen. Los cuadros originales usados conservan sus píxeles RGBA; los archivos de ejecución usan RLE8 indexado para evitar la invisibilidad que producía PNG32 en MUGEN.

Los ejes respetan la posición de los pies: ancho/2 menos offset horizontal y alto más offset vertical. La luz semitransparente se exporta aparte, con el mismo eje y tiempo que el cuerpo y con transparencia AIR aditiva. No lleva otra silueta opaca ni colisiones. Los proyectiles y explosiones independientes también usan transparencia AIR estándar.

El moveset de trece entradas amplía las cinco secuencias originales usando sus poses correspondientes. Los clones son entidades intencionales de tamaño completo, con vida y caducidad. El despertar mantiene una llama dorada derivada de los cuadros KCM, retirando la silueta del Naruto incrustado antes de superponerla, rellenando únicamente esa silueta con el brillo original de sus lados para conservar la continuidad de la llama. Kurama completo aparece en las técnicas grandes y en la ulti, conservando el Naruto que forma parte del propio dibujo original del avatar.

La ulti necesita un impacto real de Rasengan antes de sujetar y dañar al rival. Ocho pulsos tienen un presupuesto total finito de 300/360 frente a 1000 de vida. El rival sale de la captura si Naruto es interrumpido. No se incorpora la invulnerabilidad del XML original ni se consume vida del jugador.

Las pruebas verifican entradas reales en el motor, daño recibido en ambos modos, rivales de media escala, clones que golpean y pueden ser derrotados, dash en ambos sentidos y una grabación con el audio real del motor. La grabación y las pruebas nativas se realizan en Ikemen GO; la validación estática y el formato de recursos apuntan a MUGEN 1.1.

Revisión por los dos videos del usuario: RB y abajo + B mostraban `BlltPunchNrt`, un efecto de impacto del XML original, como si fuera una esfera viajando. Ahora se usa solo como destello breve del combo de taijutsu. RB tiene cinco recortes de la esfera original, giro continuo y liberación con palma abierta; abajo + B usa la carga, contacto y disipación originales del Rasengan. Los especiales se reducen al 50 % de sus valores previos, los golpes normales al 65 % y el multiplicador adicional del despertar pasa de 1.18 a 1.05. La ulti queda limitada a 300/360.
