# Acabado de Eida

Se aplica el trabajo de presentación de Pochita a Eida: preparación, movimiento,
contactos, remates y victoria. Eida conserva su identidad, su balance y su mando.

- `charge_victory.png`: ocho poses nuevas generadas con IA a partir de
  `Eida/assets/provenance/eida_support_sheet.png`. Cuatro de carga y cuatro
  de victoria con la blusa blanca y los shorts; no se incorpora el atuendo
  diferente de la antigua victoria.
- `locomotion.png`: cuatro poses de carrera, dos de frenado y dos de aterrizaje
  generadas con la misma referencia. El cabello acompaña el desplazamiento.
- `motion_fx.png`: doce cuadros nuevos de polvo, contacto y arcos pequeños.
  Los arcos son adorno de carga/victoria, no un ataque nuevo del Senrigan.
- El recorte utiliza alfa, conserva los cuerpos completos y ajusta cada hoja
  con una pose erguida de referencia a 68 píxeles. Las otras poses comparten
  ese factor: agacharse no agranda el cuerpo. Lienzos 128×80 y eje de pies 64,78.
- Cuatro WAV no verbales nuevos con osciladores y ruido filtrado: carga,
  liberación, remate físico y pisada. Ninguna voz se genera ni modifica.

Los paneles originales de Omnipotencia, las voces japonesas de Eida, los sprites
de Daemon y los archivos de Pochita se verifican por SHA-256 contra el inicio de
esta revisión. El reposo y el cuerpo del despertar conservan sus animaciones.
La ulti mantiene apertura por colisión, coste de 3000 y daño de 350.

Las chispas de contacto tienen contadores propios por estado. Esperan al primer
HitDef del ataque actual para no reaccionar a MoveHit heredado. Los remates
requieren un contacto nuevo durante su parte final; bloquear o fallar no genera
el estallido ni su sonido. El polvo tiene límites y los efectos expiran.

La victoria se comprueba ganando una ronda por colisión contra un rival de
prueba con 24 de vida, en ambas orientaciones. RoundNotOver deja terminar el
gesto. No se usa el flag WinPose, que MUGEN 1.1 no acepta. Las capturas usan
Ikemen GO y el audio real SDL; no son pruebas del ejecutable exacto del usuario.

Esta revisión no incorpora nuevas técnicas, no iguala todas las animaciones
al GIF de Sumire y no modifica el comportamiento canónico de Omnipotencia:
el daño y la apertura siguen siendo una adaptación de juego de pelea.
