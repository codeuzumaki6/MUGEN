# Activación audible de jutsus y lectura de Senrigan

La revisión anterior tenía sonidos de carga e impactos, pero no incorporaba
la entrada sonora específica de Pochita en los especiales. Esta corrección
añade SND **1,21** a los 14 jutsus: muestra mono PCM de Code_FUNCIONAL 950,2,
normalizada anteriormente para Pochita y copiada sin alterar sus datos.
No procede de una voz ni se extrae del video de Goku. Se reproduce una vez,
en canal 4 con volumescale 100, al entrar en el estado. Tiene su propio
destello y una pausa de 12 ticks, o seis al cancelar un normal confirmado.
No se añade invulnerabilidad ni se cambia el coste. La ultimate reutiliza
la muestra en su pausa de apertura existente.

Senrigan ↓atrás+Y conserva el contraataque físico de Daemon. La pose ahora
lleva la mano al ojo; sus iconos se sitúan cerca de la cara. La reversión
está activa entre Time 0 y 48, conserva su caja Clsn1 original y no causa
daño si nadie golpea a Eida. Al cerrarse la ventana baja la mano, desaparece
el icono y suena una salida breve. Al confirmar hay un acento distinto y
Daemon aparece junto a Eida para responder.

El validador rechaza un especial sin su muestra de activación y un Senrigan
sin caja de reversión. El informe de audio nuevo correlaciona las grabaciones
SDL con el WAV empaquetado: comprobar solo PlaySnd en el texto no demuestra
que el usuario pueda escucharlo. Las pruebas y capturas usan Ikemen GO,
con la limitación explícita de no tener el ejecutable exacto del usuario.
