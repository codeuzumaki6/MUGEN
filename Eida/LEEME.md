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
- Abajo, diagonal adelante, adelante + `c`: Senrigan y contraataque.
- Abajo, diagonal atrás, atrás + `c`: defensa y contraataque de Daemon.
- Botón físico **A de Xbox**: Omnipotencia. En la configuración suministrada llega a MUGEN como el botón interno `x` y exige 3000 de energía.
- Mantener **LB**: cargar energía. En la configuración suministrada llega como el botón interno `s`/Start.

Los comandos adelante/atrás son relativos a la orientación de Eida, como exige MUGEN.

## Implementación

- El reposo usa exclusivamente seis cuadros de idle; no recorre ataques.
- Daemon aparece cerca del rival, ataca o protege a Eida y se destruye al terminar la animación.
- Encantamiento no causa daño: aplica una inmovilización temporal.
- Senrigan usa `ReversalDef` y llama a Daemon cuando detecta una agresión.
- Omnipotencia usa únicamente recortes, escala y transiciones de las referencias originales suministradas. No se redibujaron paneles ni caras. Es una adaptación jugable de 8,5 segundos y consume toda la barra.
- Las voces de los grupos `0,0` a `0,2` proceden de tres fragmentos femeninos aislados del MP3 japonés entregado. No se generaron voces.

## Validación realizada

- `Eida.sff`: 91 sprites indexados de 8 bits y sus paletas en SFF v2.0.1.0.
- `Eida.snd`: 14 entradas WAV mono PCM de 16 bits decodificadas correctamente.
- `Eida.air`: 83 acciones; todas las referencias `(grupo, índice)` existen en el SFF.
- `Eida.cns` y `common1.cns`: 83 estados; las referencias estáticas de estados, ayudantes y sonidos están resueltas.
- Ikemen GO nightly: el personaje cargó y completó rondas sin errores de Eida en modo fuera de pantalla. Una prueba automatizada de especiales redujo a Kung Fu Man de 1000 a 73 de vida; otra ejercitó salto, ataques normales y ataques aéreos; Omnipotencia capturó y dañó al rival.

## Límite visual conocido

Los cuadros de Eida recuperados proceden de una captura de 600×868. Son coherentes y utilizables, pero su resolución original no alcanza todavía el detalle del GIF de Sumire. Daemon se creó como una hoja nueva a partir de las referencias del manga y se normalizó al tamaño nativo de Eida. Esta entrega no presenta esos cuadros como arte final equivalente a Sumire.

No fue posible ejecutar el binario exacto de Jump Force MUGEN V14 del usuario. Antes de sustituir una versión instalada, prueba esta carpeta como personaje adicional y revisa escala, posición del piso, volumen y mapeo del mando en una pelea local.
