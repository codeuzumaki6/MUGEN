# Boruto Uzumaki — Karma y Jōgan

Los tres volúmenes del RAR se verificaron y extrajeron completos. El video de 3:37 y sus datos están en `video_reference.json`; los archivos originales y sus huellas están en `source_material/Boruto_original/archive_checks.json`.

Se cotejaron las secuencias de espada, rayos morados, Rasengan, Fūton, invocación de serpiente, pilares, tornados y campo final con las hojas y el XML principal del paquete. La implementación conserva los cuadros del personaje y las técnicas del mod aportado. Los comentarios de formato no estándar del XML se ignoran para su lectura; el archivo original permanece sin cambios.

La base conserva la apariencia original con marcas azules. El despertar se activa con abajo + Pausa y refuerza Karma/Jōgan durante veinte segundos: corte del ojo original, electricidad azul persistente y otro moveset. El clon de sombra es de tamaño completo, dura tres segundos y puede recibir daño. Los cuerpos incluidos en efectos compuestos se reproducen en el jugador principal.

La ulti utiliza la secuencia de pilares, tormenta, tornados y Rasengan doble. Debe confirmar contacto y liberar al rival si se interrumpe. La verificación contempla ambas orientaciones y formas, rivales pequeños, guardia, daño recibido, dash, clon autónomo y extracción del ZIP jugable.

La corrección se coteja también con `bug_video_reference.json`, el video de 34 segundos aportado después de la primera entrega. Los orígenes estables de 160 cuadros están en `reviewed_geometry.json`. Los Rasengan que nacen debajo del cuerpo usan un despegue real y cajas en las propias esferas; la reacción del rival se dibuja delante. Uzuhiko usa viento del archivo alrededor del cuerpo y una palma que debe conectar, con guardia e interrupción verificadas. El viento de baja opacidad se importa con color premultiplicado y dibujo aditivo para evitar cuadros vacíos. Se comprueban 40 contactos contra el núcleo visible de las esferas, ocho fallos fuera de alcance y la liberación tras bloquear o interrumpir las técnicas.
