# Omnipotencia: abrazo a Kawaki

El usuario pidió que la ulti mostrara el abrazo mediante animación de sprites,
en lugar de centrar toda la escena en paneles estáticos. `embrace_sheet.png`
contiene ocho poses nuevas generadas con IA usando como referencia la postura
del panel y los dos sprites aportados en la conversación: acercar las manos,
recoger la cabeza de Kawaki, abrazarlo y mover el cabello mientras se libera
Omnipotencia. Son sprites nuevos; no es un panel original retocado con IA.

El recorte sigue los componentes alfa para conservar el cabello que cruza la
cuadrícula. El primer cuadro incluye dos cuerpos separados. Todos comparten
un factor calibrado con la postura de abrazo a 180 píxeles, conservando detalle para la cinemática. El cuerpo de combate no cambia. Comparten eje de pies; sus recortes se
registran en `Eida/assets/omni_hug/manifest.json`.

El abrazo es la representación del recuerdo canónico con Kawaki, cualquiera
que sea el rival seleccionado. El rival no se convierte en Kawaki: queda
retenido por la apertura confirmada y vuelve a sus estados al terminar. La
apertura con A sigue siendo bloqueable, evadible y de alcance finito. Consume
3000 y causa 350 al confirmar, igual que antes. No se añade daño por mostrar
a Kawaki ni un impacto automático al activar A.

Un solo panel original de la onda de Omnipotencia aparece atenuado detrás de
los sprites. Los originales del manga y los tres archivos de voz japonesa se
conservan sin modificar. No se generan ni clonan voces. Hay variaciones de
detalle en los sprites nuevos y no se declara igualado el estándar de Sumire.

Las pruebas de la apertura cubren acierto, bloqueo, salto, distancia y falta
de energía en Ikemen GO. Las nuevas grabaciones incluyen audio real SDL; el
binario exacto de Jump Force MUGEN V14 necesita la prueba local del usuario.
