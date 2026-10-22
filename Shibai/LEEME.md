# Shibai Ōtsutsuki para MUGEN 1.1

Extrae la carpeta `Shibai` del ZIP dentro de `chars` y agrega esta línea en
la sección de personajes de `data/select.def`:

```
Shibai/Shibai.def
```

No sustituyas Code, Kawaki, Eida, Mamushi ni Pochita. Esta carpeta contiene
sus propios SFF, SND, AIR, CMD, CNS y estados comunes; no necesita los archivos
de los personajes de referencia instalados.

La forma base es la de túnica negra de la imagen suministrada. Abajo más
LB/Pausa, con la barra llena, activa durante doce segundos el cuerpo azul de
la izquierda. Ambas formas conservan la escala y tienen movimiento, guardia,
caída y recuperación. Consulta `CONTROLES_XBOX.md` para todas las entradas.

Hay combos de viento terrestres y aéreos, tornados, ráfagas cortantes,
tormentas, repulsión, contraataques y una marca de garra vertical que puedes
usar para viajar. El despertar amplía los ataques, agrega remates encadenados
y refuerza los efectos; no contiene estacas, cubos ni Kokugan. Los especiales
tienen sonido de activación en el SND real.
La ultimate con A debe conectar y no elimina desde vida completa.

Los dibujos nuevos se completaron con IA a partir de los dos modelos que
proporcionaste. La procedencia y las adaptaciones están en
`CREDITOS_Y_FUENTES.md`; no se afirma que fueran fotogramas ya existentes.

## Comprobaciones y prueba en tu juego

Se validan referencias, archivos binarios, estados no vacíos, sintaxis nativa
de MUGEN 1.1, transparencia, animaciones de ambas formas y recuperación finita.
Las pruebas de combate usan entradas de mando y colisiones reales en Ikemen GO
con copias desechables, sin controles de prueba dentro de esta carpeta.

No se dispone del ejecutable exacto de tu Jump Force MUGEN V14 ni de tu mando
físico aquí. La carga en Ikemen GO no sustituye esa comprobación final.

Al instalarlo, comprueba caminar, salto diagonal, agacharse y levantarse tras
un derribo. Prueba X X X y los especiales desde ambos lados. Carga con Pausa,
activa abajo más Pausa y verifica que vuelve a la túnica tras doce segundos.
Con RT coloca una marca y vuelve a pulsar para viajar. Prueba A cerca, a
distancia, contra guardia y contra un salto; fallar debe gastar las tres barras.
Si hay un error, conserva la primera línea útil de `mugen.log` y la ventana
completa del error para localizar el archivo y estado exactos.
