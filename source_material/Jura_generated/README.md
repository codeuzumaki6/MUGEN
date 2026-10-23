# Recursos suplementarios de Jura Shinju

Generados con la herramienta de imágenes a partir de las referencias de Vaydra y de los sprites originales proporcionados por el usuario. No son nuevos originales de Vaydra.

- `throne_and_seated.png`: raíz-trono y cuerpo sentado separados, con transparencia real. La raíz se normaliza a 256 píxeles de ancho; el cuerpo sentado a 62 de alto y canvas 72×72.
- `book_and_regeneration.png`: cuatro poses de sacar/abrir/leer un libro y cuatro fases de capullo vegetal, en una cuadrícula de cuatro columnas por dos filas. Las poses comparten escala y eje de pies, y los capullos comparten escala y eje de suelo.

La normalización, recortes y eliminación de residuos de alpha se documentan en `tools/build_jura_assets.py`. Los recursos se montan como sprites y efectos animados en el escenario; no se muestran las imágenes completas como paneles. No se modifican las 36 poses fuente.
