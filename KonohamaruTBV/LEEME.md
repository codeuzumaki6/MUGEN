# Konohamaru Sarutobi — Two Blue Vortex

Extrae la carpeta `KonohamaruTBV` dentro de `chars/` y añade a `[Characters]` en `data/select.def`:

```ini
KonohamaruTBV/KonohamaruTBV.def
```

Personaje independiente con los sprites y audios de Vaydra aportados. Incluye los estados comunes, tres cadenas terrestres y aéreas, trece especiales por modo, doble dash gratuito y carga de energía. Vida 1200, defensa 105 y energía máxima 3000. Paquete para MUGEN 1.1; las pruebas y grabaciones se realizan en Ikemen GO.

Abajo + Pausa exige 3000, consume 1500 y activa el bastón de Enra durante veinte segundos. Cambian la postura, carrera y cadenas normales; se refuerzan los especiales. La invocación y transformación utilizan la secuencia original de Enra. Al terminar recupera la base cuando puede actuar.

La ulti con A empieza con un Rasengan que debe tocar al rival. Después aparecen los clones originales y forman el Rasengan masivo. Ocho impactos causan como máximo 650 de daño en base u 800 con Enra; contra rivales con menos de 1000 de vida máxima se limita al 65 % / 80 %. Consume tres barras, sin coste de vida propia. Admite guardia, puede fallar y libera al rival al terminar o si interrumpen al jugador.

Abajo + Y envía dos clones con Rasengan. Conservan el tamaño del personaje, atacan mientras recuperas el control y se dispersan tras el asalto o al recibir golpes. Sus desplazamientos originales de profundidad se adaptan al suelo 2D de MUGEN. El sellado triangular usa otro clon como asistente; el cuerpo principal puede recibir daño durante la técnica.

Se conservan los 301 cuadros originales de ambos atlas y se utilizan todos en las animaciones o en efectos derivados de sus píxeles. Los sprites usan formato indexado RLE8, con capas de luz aditivas sincronizadas para los resplandores. No se generan dibujos ni voces. Consulta `CONTROLES_XBOX.md` y los créditos para las fuentes.
