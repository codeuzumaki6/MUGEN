# Referencia aportada: Sasuke BTM

El DEF original acredita a Shingeki No Mugen y a Vovan99 por los sprites. El usuario aportó los archivos para adaptar el Susanoo a Hidari, recolorearlo a amarillo y conservar sus ataques.

`Sasuke_BTM_sprites.zip` contiene el SFF original de 52.680.258 bytes. El constructor lo descomprime automáticamente si falta `Sasuke_BTM.sff`; el archivo grande descomprimido y el SND de referencia no son necesarios en el ZIP jugable.

`hidari_susanoo_source.py` lee los sprites PCX y enlaces del SFF v1, transforma únicamente los colores violetas de la paleta y conserva los cuadros originales. El negro aditivo se convierte en transparencia equivalente. El empaquetador reserva una entrada transparente sin cuantizar los colores opacos: todos los píxeles visibles se verifican contra la transformación de la fuente.

Las tres acciones normales y las seis especiales se identifican en `susanoo_reference_analysis.json`. Se adaptan colisiones, controles, coste y daño al tamaño jugable de Hidari. No se ejecutan los controladores del personaje original sin revisión ni se copian sus invulnerabilidades permanentes.
