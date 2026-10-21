# Omnipotencia con los dos sprites originales

Esta revisión sustituye el abrazo generado y ampliado por los dos cuadros que
aportó el usuario. La captura de `Sheet Eida` de Vaydra se conserva en
`original/Eida_sprites_en_captura.png`, recuperada del ZIP de referencias.

Los recortes fuente son `(8,624,64,709)` y `(66,622,118,707)`. El procesamiento
solo vuelve transparente el fondo verde y empaqueta el resultado. No hay
reescalado, redibujo, sustitución de colores ni poses inventadas. Las figuras
visibles miden 50×79 y 46×79; comparten lienzo de 96×88 y eje de pies 48,86.
El manifiesto de `Eida/assets/omni_hug/` conserva las cajas completas, los
recortes por alfa, el SHA-256 de la captura, `native_scale: 1` y
`ai_redrawn: false`.

La ulti usa esas poses a escala 1, junto a Eida dentro del escenario, que se
atenúa brevemente. Se retiran el fondo de manga a pantalla completa y el zoom.
La secuencia confirmada sigue estos tiempos, a 60 ticks por segundo:

| Time | Acción |
| --- | --- |
| 0–11 | Preparación con el gesto existente de Eida. |
| 12–109 | Abrazo con los dos cuadros originales. |
| 106 | Inicio del destello y estallido de liberación. |
| 122 | Aplicación de los 350 de daño confirmados. |
| 126 | Liberación del rival a sus propios estados. |
| 160 | Regreso de Eida al control. |

La escena confirmada dura unos 2.67 segundos. El abrazo tiene nueve filas AIR
con dos referencias fuente y 98 ticks en total. Sigue siendo una animación
limitada de dos cuadros: no es un nuevo ciclo dibujado de acercamiento de
manos y cuello. La hoja `embrace_sheet.png` generada con IA se conserva como
historial de la versión rechazada y ya no se usa en el personaje.

Kawaki representa ese recuerdo canónico, independientemente del rival elegido.
El rival no se transforma en Kawaki: continúa siendo el objetivo de la apertura
confirmada y regresa al combate. A conserva su apertura bloqueable, evadible
y de alcance finito, coste de 3000 y daño de 350; la escena no se inicia al
fallar. Las activaciones sonoras de los 14 jutsus y Senrigan permanecen separadas
de esta sustitución visual.

Los paneles originales y las voces japonesas se mantienen sin modificar.
La voz auténtica de la ulti dura 1.18 segundos. No se clonan ni generan voces.
Los paneles siguen conservados en los recursos históricos, pero no forman el
fondo de esta secuencia compacta.

`tools/check_eida_compact_scene.py` verifica el SHA-256 y compara los PNG con
los píxeles RGBA de ambos recortes tras aplicar únicamente la clave verde y
el empaquetado nativo. El SFF usa su paleta indexada y puede cuantizar colores;
la comparación exacta corresponde a los PNG fuente del empaquetado. El checker
también revisa las dos referencias, tamaño, eje, duración y daño. Con un registro
de motor puede comprobar presencia del abrazo, limpieza antes de Time 130 y
regreso observado a idle. Esas observaciones se registran aparte de las
comprobaciones estáticas; no equivalen por sí solas a una revisión estética.

Las pruebas de ejecución y las capturas usan Ikemen GO. No se dispone del
binario exacto de Jump Force MUGEN V14 ni del mando físico del usuario.
