# Matsuri Shinju

Extrae `MatsuriShinju` dentro de `chars` y añade esta línea a `[Characters]` de `data/select.def`:

```ini
MatsuriShinju/MatsuriShinju.def
```

Incluye la forma con capa y la forma sin capa de la hoja original de Vaydra. El despertar se activa con **abajo + Pausa/LB**, exige tres barras, consume 1500 y dura 15 segundos. La forma sin capa aumenta el daño un 30 %, reduce un 20 % el coste de los especiales y añade un disparo a Suiton y una erupción de raíces. Al terminar vuelve a la base.

Hay tres cadenas de golpes en tierra y en el aire, doble toque para dash, carga con aura, trece especiales por forma, marcas de garra y una ulti que necesita acertar su apertura. El jardín concede siete segundos de aura con un 15 % de daño adicional para los ataques por colisión.

La ulti cuesta 3000. Su daño absoluto total se limita a `min(420, 42 % de la vida máxima del rival)` en base y `min(450, 45 %)` en despertar. El estallido de efectos no añade daño. Puede rematar a alguien herido; no derrota a un rival desde vida completa. Si se bloquea o falla no comienza la secuencia de captura.

El ZIP es autónomo: incluye sprites, sonidos, animaciones, estados comunes y documentación. No requiere instalar otros personajes. Pruebas de entradas y colisiones en Ikemen GO y contratos de MUGEN 1.1; el binario concreto de tu instalación y el mando físico requieren prueba local.
