# Remates de Pochita

`ultimate_poses.png`: ocho poses generadas con IA usando el modelo aprobado de armadura negra y bufanda roja como referencia. Dos filas de cuatro poses, con transparencia. `effects.png`: doce efectos generados con IA, cuatro cortes, cuatro salpicaduras estilizadas y cuatro impactos contra el suelo. Los autores de las referencias conservan su autoría; Chainsaw Man pertenece a Tatsuki Fujimoto.

El panel enviado por el usuario orienta la acción de extender las motosierras. No se incrusta en el SFF, ni se muestra durante la ultimate. El personaje animado realiza cinco contactos y libera al rival. El daño máximo es min(500, floor(vida máxima rival / 2)); cuesta dos barras incluso al fallar.

`tools/build_pochita_finish_assets.py` extrae, convierte y calibra estas imágenes sin redibujarlas, y crea tres mezclas no verbales de los sonidos originales seleccionados. `tools/build_pochita_climaxes.py` integra las poses y efectos en los estados y animaciones reales. Las capturas de `previews/Pochita_remates_*_motor` muestran el resultado en Ikemen GO; los MP4 usan audio montado según los eventos del motor.
