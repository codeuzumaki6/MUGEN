# Recursos suplementarios de Jura Shinju

Generados con la herramienta de imágenes a partir de las referencias de Vaydra y de los sprites originales proporcionados por el usuario. No son nuevos originales de Vaydra.

- `throne_and_seated.png`: raíz-trono y cuerpo sentado separados, con transparencia real. La raíz se normaliza a 256 píxeles de ancho; el cuerpo sentado a 62 de alto y canvas 72×72.
- `book_and_regeneration.png`: se usa sólo la fila inferior, con cuatro fases de capullo vegetal. Los cuerpos de la fila superior se conservan como archivo fuente y ya no se empaquetan.
- `book_props.png`: cuatro imágenes del libro sin persona, manos, brazos ni ropa. Se normalizan a un máximo de 18 píxeles por dimensión y se montan en un canvas transparente 32×24. Se animan como un objeto separado, sujeto a las manos de las poses originales 0,19 y 0,20. La victoria comienza con 0,24. El cuerpo de la victoria no se redibuja.

La normalización, recortes y eliminación de residuos de alpha se documentan en `tools/build_jura_assets.py`. Los recursos se montan como sprites y efectos animados en el escenario; no se muestran las imágenes completas como paneles. No se modifican las 36 poses fuente.
