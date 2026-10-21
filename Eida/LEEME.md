# Eida — especiales audibles y Omnipotencia con Kawaki

Sustituye `chars/Eida` completa por la carpeta del ZIP `Eida_SONIDO_Y_ABRAZO.zip`. Añade `Eida/Eida.def` a `[Characters]` en `data/select.def` si no estaba. Todos los archivos referenciados están incluidos.

Consulta **CONTROLES_XBOX.md**. Mapeo físico conservado: X/Y/B para normales y jutsus, A para Omnipotencia, LB/Pausa para cargar, ↓LB/Pausa con tres barras para despertar.

## Cambios

- Los 14 jutsus reproducen el efecto de activación no verbal que utiliza Pochita: muestra de Code_FUNCIONAL 950,2, empaquetada como SND 1,21, canal 4 al 100 %. Se oye al iniciar el jutsu, aunque el golpe falle. Hay un destello y una pausa de 12 ticks, o seis al cancelar un normal confirmado. No agrega invulnerabilidad ni cambia el coste.
- Senrigan ↓atrás+Y es una espera de contraataque de unos 0.8 segundos. Eida lleva la mano al ojo; su caja de reversión conserva el tamaño anterior y funciona entre Time 0 y 48. Al confirmar, Daemon sale desde Eida y responde con un ataque físico. Sin golpe entrante no hay daño ni invocación: baja la mano, desaparece el icono y termina.
- A inicia una apertura por colisión. Solo al acertar empieza Omnipotencia: ocho poses nuevas de acercamiento y abrazo a Kawaki, cabello animado y liberación de la onda. Los sprites de la cinemática conservan 180 píxeles de detalle de altura y se muestran a una escala controlada; no cambian el tamaño del cuerpo de combate.
- El abrazo representa el recuerdo canónico con Kawaki aunque el rival sea otro personaje. El rival elegido sigue siendo el objetivo y regresa a sus propios estados. La apertura puede bloquearse, saltarse o quedar fuera de alcance. Cuesta 3000 incluso si falla; al confirmar causa 350 de daño, igual que antes.
- El fondo de la escena usa un panel original de la onda de Omnipotencia atenuado, sin redibujarlo. No se retocaron los paneles ni las voces japonesas auténticas. Los ocho sprites nuevos sí se generaron con IA a partir de las referencias de postura y sprites aportadas.

Se conservan carrera, frenado, aterrizaje, carga, victoria y remates, las cadenas mixtas, persecución aérea, encanto por proyectil y parry de Daemon. El reposo mantiene sus seis cuadros exclusivos. El despertar mantiene el cuerpo, tamaño y aura existentes. Daemon conserva diseño, escala y aparición junto a Eida; puede fallar y ser interrumpido.

La recuperación tras derribos permanece corregida: mientras siga viva, Eida cae, se levanta y recupera el control. Los ayudantes golpeados se eliminan en sus propios estados en lugar de usar los de daño de Eida.

## Comprobaciones

SFF v2.0.1.0 con 202 entradas; SND con 31 muestras mono PCM de 16 bits; AIR con 124 acciones; 124 estados en cuatro CNS. Retrato de combate 25×25 y selección 120×140. Los ocho paneles originales siguen conservados a 1280×720 en el SFF, aunque la nueva escena principal utiliza los sprites del abrazo.

Pruebas en Ikemen GO: 80 escenarios de comandos/combate, seis de recuperación, nueve de apertura de ultimate, 22 de presentación, dos victorias reales y dos esperas de Senrigan sin ataque. Las siete regresiones estáticas incluyen los errores anteriores de carga, impacto infinito, flag de victoria inválido, caja de reversión ausente y especial sin sonido de activación. La reconstrucción repetida valida que no se acumulen estados o controladores.

Los videos nuevos de especiales, Senrigan y abrazo capturan audio real SDL a 44100 Hz estéreo. Cada activación se contrasta con el WAV empaquetado; las imágenes se sincronizan con esos eventos de audio sin estirar ni mezclar la grabación. Los videos de revisiones anteriores no representan todos estos cambios.

No se ejecutó el binario exacto de Jump Force MUGEN V14 ni el mando Xbox físico. Las pruebas usan copias instrumentadas fuera de la carpeta entregada. El equilibrio contra todo el plantel requiere partidas locales. Las poses generadas tienen variaciones de detalle; no se declara alcanzada la referencia artística de Sumire.

Los ataques de Daemon, encanto, parry, despertar y la apertura/daño de Omnipotencia son adaptaciones para un juego de pelea; no equivalen a que Eida controle a voluntad todos esos efectos en el canon. Consulta `CREDITOS_Y_FUENTES.md` para la procedencia del arte, voces y sonido.
