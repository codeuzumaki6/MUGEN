# Especiales ampliados de Pochita

La referencia nueva de Chainsaw Man se revisó en cuadros temporales, con los tiempos y límites en `referencia.json`. El video demuestra preparación reconocible, avance mientras tritura y una separación final del rival. Su secuencia de 22 contactos y la cabeza gigante no se presentan como habilidades ya implementadas en Pochita.

Esta revisión amplía seis técnicas con secuencias físicas y efectos distintos. `PochitaTrueForm/assets/special_choreography.json` documenta cuadros, contactos, daño y duración sin pausas. Desgarro tiene tres contactos; Cuatro brazos cinco; Estocada tres; Barrido dos; Embestida tres; Carnicería siete. Se redistribuye el mismo daño total de cada técnica y se conserva el coste. Los pasos usan velocidad y colisiones: no se liga ni teletransporta al rival.

`special_trails.png` contiene 24 cuadros generados con IA: seis familias de cuatro fases. El constructor solo recorta, convierte y escala ese arte. Las filas tienen alturas distintas y se recortan por sus márgenes transparentes verificados. Se usan ejes comunes por familia y transparencia binaria en SFF. Los cuadros de cuerpo proceden de las hojas ya existentes; no hay nuevos dibujos de cuerpo en esta revisión.

Las seis familias son arco dentado, cuatro hojas cruzadas, estocada horizontal, polvo/fragmentos del barrido, estela de avance y cortes de Carnicería. Cada contacto muestra su estela; el pulso de remate grande, el sonido final y la vibración requieren confirmar todos los contactos. Los efectos expiran y desaparecen al interrumpir el ataque. Las cajas ofensivas siguen la hoja visible, no el tamaño de la estela.

217 escenarios de entrada y colisión comprueban, entre otros, contacto y daño exactos de las seis secuencias completas en ambas orientaciones, doce guardias, doce fallos desde lejos, energía insuficiente, cancelaciones, caída y ultimate. Se capturan seis vistas con audio real SDL y una comparación de Carnicería a la misma velocidad. El binario exacto del MUGEN del usuario y el mando físico requieren pruebas locales. Las pruebas no certifican que el arte alcance calidad profesional ni sustituyen jugar contra el plantel real.
