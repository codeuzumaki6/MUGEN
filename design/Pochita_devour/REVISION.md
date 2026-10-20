# Despertar y devorar/borrado

El usuario pidió abajo+carga para un despertar temporal con regeneración, mover la ultimate anterior a un especial y adaptar el borrado conceptual sin muerte instantánea. También pidió que Pochita fuera fuerte y que la presentación de los personajes tenga intensidad comparable a su referencia de Sukuna. El video llegó durante el trabajo y se revisó visualmente; su ficha y una plancha están en sukuna_referencia.json y sukuna_referencia.jpg. Se estudian preparación, impactos y remates, sin copiar sus poderes a distancia como habilidades de Pochita.

Reglas: tres barras disponibles, abajo+LB/s, coste 1000, 360 ticks, cuatro puntos de vida cada seis ticks hasta 240, multiplicador HitDef 1,20, espera de 900 ticks desde la activación. La preparación dura 24 ticks y es vulnerable. Mantener el botón no renueva el efecto. KO cancela la curación. No se modifica la escala ni la animación de cuerpo durante el efecto; las brasas son un Explod separado.

La cinemática anterior se conserva en abajo+A, estados 1500/1501, coste 1000, min(250, floor(LifeMax*.25)). La nueva A usa 3000/3001: apertura por colisión, mordisco, deglución, ausencia temporal del rival, retorno y caída. Cuesta 2000 y causa min(450, floor(LifeMax*.45)) en cuatro entregas. Las cinemáticas tienen daño absoluto limitado, sin multiplicador del despertar. La nueva quita hasta 500 de energía rival al acertar. Fallar, bloquear, saltar o interrumpir la apertura evita la escena; el coste permanece pagado.

No se eliminan conceptos reales del motor ni se modifica el CMD/SFF/SND del rival. Se representa el devorar del canon mediante poses y desaparición temporal. La curación automática y los valores son adaptaciones jugables.

Arte: ocho poses nuevas con IA y doce cuadros de efectos nuevos con IA. No se redibuja el manga ni se muestra un panel en la cinemática. La escala se calibra una vez con la primera pose a 72 px; no se estiran los cuadros individualmente. Los ejes de pies y los recortes se registran en assets/sprites.json. El arte conserva variaciones de detalle.

Audio: tres mezclas nuevas de sonidos no verbales previamente suministrados, sin voces humanas generadas. La demostración usa captura real del mezclador SDL de Ikemen GO, sincronizada por correlación, con velocidad normal. El juego exacto y el mando Xbox requieren prueba local.

Alcance: abajo adelante + Y ahora muestra una cadena física con hoja de motosierra, animada en ocho cuadros fuente. Se extiende y se recoge; las colisiones siguen el dibujo. El cuerpo conserva su escala y se dibuja en una capa ligada durante esa técnica, retirada al acabar o al recibir un golpe. Desgarro, Embestida y RT mantienen velocidad de avance mientras queda distancia hasta el rival, y se detienen al acercarse. No hay salto de posición hasta el enemigo. Se añaden pruebas de alcance, bloqueo, fallo e interrupción de cadena. El SFF total pasa a 221 entradas: 155 de cuerpo, 64 efectos y dos retratos.
