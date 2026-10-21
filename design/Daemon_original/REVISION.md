# Daemon basado en el modelo aportado

El usuario pidió sustituir el Daemon anterior por el de su hoja. `daemon.zip`
contiene `daemon/daemon_sprite_nzc_model_by_vahidras_dk9e6b8-375w-2x.jpg`,
549×475. Se conserva sin modificar como `daemon_vahidras_original.jpg`,
SHA-256 `4cb499bad7fcdc70130926f2df9fe3f51b6022c4e6943f3fefaa3deb1b64aa39`.
La atribución a Vahidras procede del nombre original del archivo.

La hoja aporta dos cuerpos completos, de pie y en carrera, y dos cabezas.
Los cuerpos originales se usan como 1000,0 y 1000,16: recorte, transparencia
del fondo verde y reducción uniforme por vecino más próximo. El JPG tiene
compresión y una cuadrícula ya ampliada; no se presenta como fuente PNG nítida.
El recorte de carrera se separa de la cabeza suelta por componentes conexos.
No se redibujan esas dos poses originales.

`supplemental_poses.png` contiene 16 poses nuevas generadas con IA siguiendo
el modelo: guardia, preparación, puños, patadas, barrido, reflejo y dos pasos
adicionales de carrera. Son arte nuevo, no fotogramas originales de Vahidras.
La primera propuesta, más cabezona, se descartó. La segunda alarga las piernas
y estrecha el cuerpo; aun existen diferencias de dibujo entre originales y
poses nuevas. El video del motor permite juzgarlas sin declarar un acabado
profesional ni identidad perfecta de cada detalle.

Hay 19 entradas SFF y 18 PNG distintos: la pose de listo se reutiliza en dos
índices para mantener referencias existentes. Un factor por hoja preserva las
alturas relativas; no se estira cada patada o agachado para llenar la altura
de pie. Los lienzos son 96×56, con pies en 48,54 y altura opaca máxima de 49.
Eida conserva sus 68 píxeles de reposo; Daemon sigue siendo un ayudante pequeño.
El empaquetador ya no aplica la antigua reducción adicional de .68.

La carrera 1510 utiliza exclusivamente 16,17,18,17. El barrido 1524 utiliza
preparación baja y la nueva patada baja 13. Guardia y parry utilizan 2,14,15.
Las cajas ofensivas siguen puños y pies; la caja de reversión amplia del parry
se conserva porque representa su mecánica de protección. Se mantienen tiempos
de contacto, daño, coste y estados; salir de Eida, recorrer la distancia,
interrumpirse y desaparecer siguen funcionando como antes.

Comprobaciones: `tools/check_daemon_reference.py` verifica los dos recortes
procesados frente al JPG intacto, procedencia de cada pose, transparencia,
escala, eje y referencias. `previews/Eida_Daemon_preservation_checks.json`
contrasta la entrega anterior y confirma 180 registros SFF ajenos a Daemon
idénticos, además de todos los CNS, CMD, SND y archivos de Pochita protegidos.
Los 80 casos de control/colisión se ejecutaron de nuevo con las nuevas cajas.
La captura muestra seis ataques con sus activaciones y audio real SDL; no es
un montaje de combate fuera del motor. Se probaron en Ikemen GO, no en el
ejecutable exacto de Jump Force MUGEN V14 ni con un mando físico.

Reconstrucción: después de `build_eida_polish.py` y `build_eida_hug_ultimate.py`,
ejecutar `build_daemon_reference.py`, `build_archives.py`, `validate_character.py`
y `check_daemon_reference.py`. La captura dedicada usa
`EIDA_DAEMON_MODEL_REVIEW=1 python3 tools/make_eida_technique_previews.py /ruta/al/ikemen`.
