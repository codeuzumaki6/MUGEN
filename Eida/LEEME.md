# Eida — Boruto: Two Blue Vortex

Personaje para MUGEN 1.1 / Jump Force MUGEN V14. Daemon funciona como `Helper` independiente y ejecuta los ataques físicos principales.

Esta revisión reconstruye los sprites como SFF v2.0.1.0 nativo, el mismo formato del personaje Code suministrado como referencia. Sustituye por completo cualquier carpeta `Eida` instalada desde un ZIP anterior.

## Instalación

1. Copia la carpeta `Eida` dentro de `chars/`.
2. Añade `Eida/Eida.def` a la sección `[Characters]` de `data/select.def`.
3. Conserva todos los archivos de la carpeta; `Eida.def` referencia `Eida.sff`, `Eida.snd`, `Eida.air`, `Eida.cmd`, `Eida.cns` y `common1.cns`.

## Controles verificados contra el `mugen.cfg` suministrado

- Joystick izquierda/derecha: caminar y cambiar de orientación.
- Joystick arriba: saltar; arriba con izquierda/derecha: salto diagonal.
- Joystick abajo: agacharse.
- Botones internos `a`, `b`, `c`: ataques normales; también funcionan en el aire.
- Abajo, diagonal adelante, adelante + `a`: Daemon rápido.
- Abajo, diagonal atrás, atrás + `a`: combo de Daemon.
- Abajo, diagonal adelante, adelante + `b`: patadas de Daemon.
- Abajo, diagonal atrás, atrás + `b`: encantamiento temporal.
- Abajo, diagonal atrás, atrás + **RB**: parry de Daemon durante dos segundos. Consume 1000 de energía y el contraataque confirmado no se puede bloquear. En el `mugen.cfg` suministrado, RB llega como el botón interno `y`.
- Abajo, diagonal atrás, atrás + **RT**: Senrigan y contraataque. Consume 1000 de energía. En el `mugen.cfg` suministrado, RT llega como el botón interno `z`.
- Botón físico **A de Xbox**: Omnipotencia. En la configuración suministrada llega a MUGEN como el botón interno `x` y exige 3000 de energía.
- Mantener **LB/Pausa**: cargar energía. En la configuración suministrada llega como el botón interno `s`/Start.
- Con 3000 de energía, abajo + **LB/Pausa** activa el despertar durante 15 segundos.

Los comandos adelante/atrás son relativos a la orientación de Eida, como exige MUGEN.

## Implementación

- El reposo usa exclusivamente seis cuadros de idle; no recorre ataques.
- Los 54 cuadros originales de Eida se recortaron nuevamente desde la hoja completa para recuperar cabezas, cabello, piernas y pies que los recortes anteriores habían cortado. También se limpió la contaminación verde del fondo.
- Se añadieron 16 cuadros nuevos basados en esos originales para giro, salto, caída, aterrizaje, encantamiento, Senrigan, carga y victoria. Ninguno se usa en el idle.
- Daemon usa 16 poses reconstruidas a escala de combate, aparece cerca del rival, ataca o protege a Eida y se destruye al terminar la animación.
- Los golpes de Daemon reproducen sonido de movimiento y de impacto; los efectos se normalizaron para que sean audibles en la mezcla de Jump Force MUGEN.
- Encantamiento no causa daño: aplica una inmovilización temporal.
- Senrigan usa `ReversalDef` y llama a Daemon cuando detecta una agresión.
- Omnipotencia usa únicamente recortes, escala y transiciones de las referencias originales suministradas. No se redibujaron paneles ni caras. Es una adaptación jugable de 8,5 segundos y consume toda la barra.
- Las voces de los grupos `0,0` a `0,2` proceden de tres fragmentos femeninos aislados del MP3 japonés entregado. No se generaron voces.

## Validación realizada

- `Eida.sff`: 128 sprites indexados de 8 bits y sus paletas en SFF v2.0.1.0. El retrato de combate `9000,0` mide 25×25 y el retrato de selección `9000,1` mide 120×140.
- `Eida.snd`: 14 entradas WAV mono PCM de 16 bits decodificadas correctamente.
- `Eida.air`: 90 acciones; todas las referencias `(grupo, índice)` existen en el SFF y el idle conserva únicamente cuadros de reposo.
- `Eida.cns` y `common1.cns`: 91 estados; las referencias estáticas de estados, ayudantes y sonidos están resueltas.
- Ikemen GO nightly: esta compilación del SFF y SND cargó y completó una ronda sin errores de Eida. El salto se redujo y los 16 cuadros del despertar se normalizaron a 82 píxeles de alto para conservar la escala del personaje.

## Límite visual conocido

Los 54 cuadros base de Eida proceden de una captura de 600×868; los 16 adicionales se generaron tomando esos cuadros como referencia directa y se normalizaron a la misma escala. Daemon se creó como una hoja nueva a partir de las referencias del manga. La cinematografía de Omnipotencia conserva exclusivamente los paneles originales suministrados.

No fue posible ejecutar el binario exacto de Jump Force MUGEN V14 del usuario. Antes de sustituir una versión instalada, prueba esta carpeta como personaje adicional y revisa escala, posición del piso, volumen y mapeo del mando en una pelea local.
