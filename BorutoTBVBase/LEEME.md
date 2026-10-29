# Boruto Uzumaki — TBV base

Extrae la carpeta `BorutoTBVBase` dentro de `chars/` y añade a `[Characters]` de `data/select.def`:

```ini
BorutoTBVBase/BorutoTBVBase.def
```

Personaje independiente para MUGEN 1.1, validado en Ikemen GO. Incluye sprites, audio y estados comunes. Vida 1200, defensa 105 y energía máxima 3000.

Se utiliza el paquete Boruto Ver2 de Vaydra recibido para esta versión: capa con interior rosa, katana, Rasengan, Shiden, Hiraishin y las secuencias completas de Uzuhiko. Los cuadros que incluyen a Boruto se dibujan sobre el jugador principal. Los proyectiles y tornados usan recursos independientes y transparencia aditiva del AIR compatible con MUGEN.

La ulti con A encadena el capullo de viento, la envoltura del cuerpo, el impacto de palma, el tornado sostenido y la onda final originales. Debe acertar y permite guardia. Ocho aplicaciones de daño alcanzan un máximo de 650 en base o 800 con concentración; contra rivales con menos de 1000 de vida máxima se limita al 65 % / 80 %. El rival recupera sus propios estados al terminar o si interrumpen a Boruto. La ulti cuesta tres barras y no consume vida propia.

Abajo + Pausa requiere 3000, consume 1500 y activa veinte segundos de concentración de Uzuhiko. Refuerza las técnicas manteniendo la apariencia TBV base. Hay tres cadenas terrestres y aéreas, doble dash gratuito, carga con aura y un clon autónomo de 120 de vida y tres segundos de duración. Puede recibir daño y ser derrotado.

Se conservan los 45 archivos originales del ZIP, los 161 cuadros válidos, las 38 referencias de audio originales (36 archivos de audio únicos) y sus colores. Los 17 cuadros vacíos se excluyen de las animaciones. Los sprites y voces no se redibujan ni generan. Los nombres de recursos Hiruzen corresponden al espacio reemplazado por el mod original.

Consulta `CONTROLES_XBOX.md`. Las pruebas nativas se realizan en Ikemen GO; el ejecutable exacto de MUGEN del usuario y el mando físico se comprueban localmente.

Revisión de animaciones: los 161 cuadros originales conservan ahora todos sus colores y niveles de transparencia mediante PNG32 de MUGEN 1.1. Saltar, agacharse y aterrizar usan poses de movimiento; el Rasengan aéreo despega y desciende de forma continua. El remate de Uzuhiko mantiene el cuerpo estable y separa la onda final para controlar su tamaño.
