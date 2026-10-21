# Eida — Daemon con el modelo aportado y Omnipotencia compacta

Sustituye `chars/Eida` completa por la carpeta del ZIP `Eida_DAEMON_ORIGINAL.zip`. Añade `Eida/Eida.def` a `[Characters]` en `data/select.def` si no estaba. Conserva juntos todos los archivos referenciados por el DEF.

Consulta **CONTROLES_XBOX.md**. Mapeo físico conservado: X/Y/B para normales y jutsus, A para Omnipotencia, LB/Pausa para cargar, ↓LB/Pausa con tres barras para despertar.

## Omnipotencia compacta

A conserva la apertura por colisión: puede bloquearse, saltarse o quedar fuera de alcance. Cuesta 3000 incluso si falla; solo al acertar empieza la escena y se aplican sus 350 de daño.

El abrazo utiliza exactamente los dos sprites originales de Eida y Kawaki de la hoja suministrada. Se retira su fondo verde y se empaquetan a escala nativa 1, sin redibujar, agrandar ni sustituir sus píxeles visibles. Las figuras miden 50×79 y 46×79, dentro de lienzos transparentes de 96×88 con eje de pies 48,86. El cuerpo del personaje durante el combate no cambia.

La escena permanece dentro del escenario, que se atenúa brevemente. No hay fondo de manga a pantalla completa ni acercamiento cinematográfico. Eida prepara el gesto durante los primeros 12 ticks; los dos cuadros del abrazo aparecen entre Time 12 y 109. El estallido comienza en 106, el daño se aplica en 122, el rival sale de la retención en 126 y Eida vuelve al control en 160: unos 2.67 segundos desde que se confirma la escena.

Son dos cuadros originales con animación limitada. No se presenta su alternancia como un nuevo ciclo dibujado de acercamiento de manos y cuello. Las ocho poses generadas con IA de la versión anterior ya no se usan en el personaje. Los paneles originales y las voces japonesas se conservan sin modificar; no se generan voces.

El abrazo representa el recuerdo canónico con Kawaki aunque el rival sea otro personaje. El rival elegido sigue siendo el objetivo y regresa a sus propios estados; no se convierte permanentemente en Kawaki. La apertura y el daño son una adaptación para un juego de pelea.

## Especiales y Senrigan conservados

- Los 14 jutsus mantienen el efecto de activación no verbal que utiliza Pochita: muestra de Code_FUNCIONAL 950,2, empaquetada como SND 1,21, canal 4 al 100 %. Se oye al iniciar el jutsu, aunque el golpe falle. Hay destello y pausa de 12 ticks, o seis al cancelar un normal confirmado. No agrega invulnerabilidad ni cambia el coste.
- Senrigan ↓atrás+Y espera un golpe durante unos 0.8 segundos. Eida lleva la mano al ojo y su caja de reversión funciona entre Time 0 y 48. Al confirmar, Daemon aparece junto a Eida y responde físicamente. Sin golpe entrante no hay daño ni invocación: baja la mano, desaparece el icono y termina.

Se conservan carrera, frenado, aterrizaje, carga, victoria, remates, cadenas mixtas, persecución aérea, encanto por proyectil y parry de Daemon. El reposo mantiene sus seis cuadros exclusivos. El despertar mantiene el cuerpo, tamaño y aura existentes. Daemon adopta el modelo de la hoja aportada: dos poses originales y 16 poses suplementarias generadas con IA para cubrir los movimientos ausentes. Hay 19 entradas de animación y 18 imágenes distintas. Conserva su escala de ayudante (hasta 49 píxeles de cuerpo frente a los 68 de Eida) y aparece junto a ella; puede fallar y ser interrumpido. La carrera tiene poses propias y el barrido usa una patada baja. Se mantienen los tiempos, costes y daños.

La recuperación tras derribos permanece corregida: mientras siga viva, Eida cae, se levanta y recupera el control. Los ayudantes golpeados se eliminan en sus propios estados en lugar de usar los de daño de Eida.

## Archivos y comprobaciones

La revisión de Daemon pasó de nuevo los 80 casos de entradas y colisiones y siete regresiones de compatibilidad. Se grabaron seis ataques en el motor con audio real. `tools/check_daemon_reference.py` comprueba la procedencia de los originales, el eje fijo de pies, la transparencia y el uso de poses de carrera, defensa y barrido. La hoja original es JPG; tiene compresión y las poses nuevas presentan algunas diferencias de dibujo. Consulta el video antes de valorar su acabado.


SFF v2.0.1.0 con 199 entradas; SND con 31 muestras mono PCM de 16 bits; AIR con 124 acciones; 124 estados en cuatro CNS. Retrato de combate 25×25 y selección 120×140. Los ocho paneles originales conservados a 1280×720 siguen en los recursos, pero no forman el fondo de esta ulti.

`tools/check_eida_compact_scene.py` contrasta los dos PNG con los recortes exactos de la hoja original, su SHA-256 y el empaquetado a escala 1. Comprueba las referencias AIR/SFF, la duración finita, el retorno previsto en 160 y el daño de 350. Con un registro de motor también comprueba la presencia del abrazo, su desaparición antes de Time 130 y el regreso observado a idle. Distingue esas comprobaciones de archivo de las observaciones del motor; no infiere control físico ni calidad visual a partir del texto. El informe de captura se guarda en `previews/Eida_compact_scene_checks.json` del repositorio.

Las comprobaciones de combate y las capturas se realizan en Ikemen GO sobre copias instrumentadas fuera de la carpeta entregada. Las grabaciones nuevas usan audio real SDL a 44100 Hz estéreo, contrastado con las muestras del SND; no mezclan efectos fuera del motor. Los videos de revisiones anteriores no representan esta ulti.

No se ejecutó el binario exacto de Jump Force MUGEN V14 ni el mando Xbox físico. El equilibrio frente a todo el plantel requiere partidas locales. La hoja recuperada tiene resolución limitada y no se declara alcanzada la referencia artística de Sumire. Consulta `CREDITOS_Y_FUENTES.md` para la procedencia del arte, voces y sonido.
