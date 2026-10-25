# Deepa Kara

Extrae la carpeta `DeepaKara` dentro de `chars/` y añade esta línea a `data/select.def`:

```ini
DeepaKara/DeepaKara.def
```

El paquete es independiente y contiene sus sprites, voces, efectos y estados comunes. Está preparado para MUGEN 1.1 y se ha probado en Ikemen GO. No se dispone aquí del ejecutable exacto de MUGEN de Windows ni del mando físico.

La base utiliza los cuadros originales del paquete de VayDra: cubos de carbono, disco, abanico de agujas, puño propulsado y cañón de carbono. La apariencia base sin el abrigo largo coincide con los sprites y el video aportados.

**Abajo + Pausa**, con 3000 de energía, activa la armadura de carbono. Consume 1500 y dura 20 segundos. La armadura tiene sus propios golpes y especiales, mayor fuerza física y resistencia durante las secuencias de daño. El primer golpe conserva el comportamiento estándar de `DefenceMulSet` de MUGEN; los siguientes golpes durante el daño se reducen al 70 %. Puede recibir golpes, patadas y proyectiles, bloquear, caer y levantarse. La transformación caduca al recuperar el control, con 25 segundos de recarga desde su activación.

**A** consume 3000 y ejecuta una ulti distinta en cada forma: cañón de carbono en base y una ráfaga de puños de la armadura. El daño máximo es `min(550, floor(vida máxima rival × .55))` en base y `min(700, floor(vida máxima rival × .70))` con armadura. Ambas requieren acertar, admiten guardia y alcance finito y no consumen vida propia. Si Deepa recibe un golpe que interrumpe la técnica, el rival queda libre y cesa el daño.

Mantén Pausa para cargar con un aura verde. Dos pulsaciones seguidas a la izquierda o derecha hacen un dash terrestre gratuito. Los controles completos figuran en `CONTROLES_XBOX.md`.

Se importaron los 134 cuadros válidos de Deepa de los atlas originales. Los ayudantes de proyectil contienen únicamente el cubo o el disco; las secuencias que ya incluyen el cuerpo se reproducen sobre el personaje. La fuente no trae poses de caída propias de la armadura: se conserva su cuerpo original y se rota al caer, sin volver a la ropa base. Los 16 cuadros de otro personaje mezclados en el atlas de transformación se excluyen del personaje jugable.

Las comprobaciones del repositorio incluyen entradas en ambas direcciones y formas, cadenas terrestres y aéreas, coste de energía, guardia, recuperación, transformación y caducidad, daño real como oponente, dash y ultis acertadas, bloqueadas, lejanas, sin barra, a 1 de vida e interrumpidas por un ataque real. La muestra de gameplay conserva el audio capturado del motor.
