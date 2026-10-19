# Controles físicos de Xbox

Correspondencia usada en el mando del proyecto: **X=a, Y=b, B=c, A=x, RB=y, RT=z, LB=s**. Son botones físicos distintos de las letras internas de MUGEN. El CMD no puede reasignar por sí solo un botón físico: si tu configuración global cambió, vuelve a asignarlo en las opciones de entrada del juego. Si tu mando todavía llama «Pausa» al botón que envía `s`, ese botón realiza la carga.

Adelante/atrás son relativos a la orientación: mirando a la derecha, adelante es →; mirando a la izquierda, adelante es ←. Se acepta abajo → diagonal → adelante/atrás y botón, o mantener la diagonal inferior y pulsar el botón.

| Entrada física | Movimiento | Energía |
|---|---|---:|
| Joystick izquierda/derecha | Caminar | 0 |
| Arriba / arriba diagonal | Saltar / saltar avanzando o retrocediendo | 0 |
| Abajo | Agacharse | 0 |
| Atrás / abajo+atrás | Guardia alta / baja | 0 |
| Adelante dos veces | Correr; X/Y/B permiten atacar desde carrera | 0 |
| Atrás dos veces | Retirada corta | 0 |
| X, X, X al conectar | Tres cortes y lanzamiento | 0 |
| Y, Y, Y al conectar | Extensión, triturado multigolpe y empuje | 0 |
| B, B, B al conectar | Giro, salto corto y remate contra el suelo | 0 |
| X → Y → B en el aire al conectar | Cadena aérea de tres ataques | 0 |
| Abajo+adelante+X | Desgarro: avance con dos cortes | 250 |
| Abajo+atrás+X | Cuatro brazos: tres contactos | 350 |
| Abajo+X | Ascenso: corte que eleva al rival | 250 |
| Abajo+adelante+Y | Estocada: extensión de largo alcance | 350 |
| Abajo+atrás+Y | Barrido bajo | 250 |
| Abajo+Y | Guillotina: salto corto y corte descendente | 500 |
| Abajo+adelante+B | Embestida de dos impactos | 500 |
| Abajo+atrás+B | Carnicería: cinco cortes y lanzamiento | 750 |
| Abajo+B | Rasante: corte bajo y derribo | 250 |
| RB | Guardia de motosierras y respuesta si recibe un golpe durante la ventana | 250 |
| RT | Asalto de cinco cortes con alcance extendido | 750 |
| Mantener LB / antiguo Pausa | Acelerar motores y cargar; soltar para detener | Carga hasta 3000 |
| A | Ultimate: embestida, cinco cortes con cuatro brazos y lanzamiento si conecta | 2000 |

1000 equivale a una barra. Sin la energía requerida para abajo+X/Y/B se ejecuta el normal agachado correspondiente. Los especiales ofensivos pueden cancelar un normal de suelo que haya conectado. Repetir el botón durante una guardia rival no concede automáticamente la continuación del combo. RB tiene aproximadamente 0,4 segundos de ventana activa, con preparación y recuperación; no refleja todo el daño ni asegura contras contra cualquier proyectil.

En el rediseño, Ascenso, Barrido y Rasante son de corta distancia. Las cajas de ataque se ajustaron a las motosierras visibles; no alcanzan al rival automáticamente desde lejos.

La ultimate consume **dos barras al activarla**, incluso si falla o la bloquean; exige 2000 de energía disponible. Su daño total es el menor entre 500 y la mitad de la vida máxima del rival, redondeado hacia abajo. Un rival con vida completa sobrevive; uno ya herido puede morir. No hay daño de la secuencia al bloquear o esquivar la apertura.

Los remates de X/Y/B tienen cortes visibles, sangre al acertar y respuestas distintas: lanzamiento, triturado con empuje y golpe contra el suelo. En el muñeco de 1000 de vida las cadenas completas causan 152 / 180 / 205. Estos valores pueden variar con las defensas y reglas del rival.
