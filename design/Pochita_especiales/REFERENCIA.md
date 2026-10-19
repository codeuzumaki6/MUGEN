# Activación de especiales

La grabación enviada por el usuario dura 30,333 s, 1920×1080 a 30 fps, audio AAC estéreo. Archivo: `mugen-2026-10-18-23-23-52_hMATJZgk.mp4`. SHA256: `01ad6146a204fd0420939266729a9937e8f776d1d8d0b9a07487db4a90b1befb`.

Se inspeccionaron fotogramas y los intervalos de activación, aproximadamente 13,1–13,7 s, 17,2–17,8 s, 22–23 s y 26–27 s. Goku adopta una pose, el escenario se oscurece y se muestra un destello horizontal blanco/azul antes del ataque. Esta es la estructura visual adaptada a Pochita, con rojo/blanco y un pulso dentado de suelo. La grabación no se publica en el repositorio.

El sonido de activación se toma del Code funcional aportado anteriormente: grupo 950,2, identificado en `Supers.cns` como PlaySnd - Super Charge. Autor del personaje según su DEF: MUGEN STARS, versión 17/09/2023. La muestra original se conserva sin modificar en `Code_950_2_original.wav`. El audio de la grabación de Goku contiene mezcla del juego y no se usa como muestra aislada ni se afirma identidad exacta de las ondas. No se incluye diálogo de Goku.

`activation_fx.png` contiene ocho efectos generados con IA, cuatro del destello y cuatro del anillo. El constructor recorta por los huecos transparentes inspeccionados para no cortar el destello creciente, convierte al SFF y mantiene márgenes. No altera los sprites del personaje.

Los seis especiales tienen estados de preparación 11000/11010/11030/11040/11060/11070, sonido S1,10 en canal 4, SuperPause de 12 ticks (6 en continuación) y transición a su ataque real. El coste se paga una sola vez durante la preparación; p2defmul=1, unhittable=0. La preparación no tiene HitDef. Los comandos, el límite de dos especiales, las rutas y la ultimate siguen vigentes.

La prueba audiovisual usa el controlador SDL disk del Ikemen verificado, AUDIO_S16SYS estéreo a 44100 Hz. Se captura su salida real, se busca la muestra de activación por correlación normalizada y se sincroniza con los eventos de los fotogramas. No se reconstruye la banda sonora mezclando WAV fuera del motor. Los resultados y puntajes están en `previews/Pochita_actual_audio_checks.json`. El binario exacto de MUGEN del usuario no se ejecutó.
