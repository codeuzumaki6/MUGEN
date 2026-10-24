# Corrección conjunta de los nueve personajes

`baseline.json` registra los archivos de la revisión aceptada antes de los cambios. `build.json` registra las secuencias nuevas. Los archivos `*_anchors.json` conservan los pivotes medidos mediante comparación con los cuerpos originales; evitan centrar un personaje dentro del rectángulo de un efecto grande.

Los paquetes aportados se conservan en `source_material/*_full_original`. Sus metadatos originales se mantienen byte por byte, incluyendo CRLF. El código de combate de Naruto Senki no se ejecuta ni se copia como estadísticas de MUGEN.

Reconstrucción: `python tools/build_roster_revision.py`. Necesita Python, Pillow y NumPy. Regenerar un pivote que no esté en la caché necesita `opencv-python-headless`; las cachés entregadas permiten la reconstrucción normal sin esa dependencia.

Las pruebas nativas necesitan el motor de Ikemen GO en `/workspace/.eida-tools/ikemen-nightly`. Se ejecuta una instancia cada vez. Las carpetas de prueba, los controles de entrada sintéticos y las modificaciones de Lua se crean en copias desechables; no se incluyen en los personajes.

- `python tools/check_roster_revision.py`: ataques, cadenas, ultis, despertar y clones.
- `python tools/check_roster_receiving.py`: golpes bajos, medios, proyectiles y cadenas de tres impactos, usando los personajes como P2.
- `python tools/check_roster_pressure.py`: regresión del primer puñetazo infinito de la CPU y posibilidad de contraatacar.
- `python tools/check_roster_dashes.py`: doble toque y toque simple en ambos sentidos.
- `python tools/package_roster_revision.py`: nueve ZIP individuales y el paquete conjunto, con validación de los archivos extraídos.
- `python tools/verify_roster_revision.py`: procedencia, conservación del dibujo, ventanas de contacto, contratos de daño y correspondencia de los ZIP con los archivos probados.

La grabación de recepción usa colisiones reales controladas por una prueba. El video de Matsuri muestra todos los especiales de ambas formas, las dos ultis y el despertar, con audio capturado del motor. La prueba local del ejecutable concreto de Jump Force MUGEN V14 y del mando físico corresponde a la instalación del usuario.
