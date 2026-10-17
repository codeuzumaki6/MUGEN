# Traspaso del proyecto Eida — conversación de ChatGPT a Codex

> Este documento **resume** la conversación; no es una copia literal de todos los mensajes. Los archivos incluidos son los que seguían disponibles de las cargas del usuario. El asistente no pudo transferir automáticamente el historial de ChatGPT a Codex.

## Objetivo final
Construir una **carpeta instalable `chars/Eida/`** para **Jump Force MUGEN V14**, tomando como referencia técnica un personaje real `Code` que el usuario ya puede jugar en su MUGEN 1.1. El personaje debe ser Eida (Ada) de *Boruto / Two Blue Vortex*; Daemon aparecerá como ayudante para sus ataques físicos. El usuario desea calidad gráfica y de animación comparable al GIF de Sumire de Vahidras adjunto. **No reemplazar una animación por una secuencia aleatoria de poses ni por carteles de IA**.

## Intención estética (prioridad máxima)
- Eida mantiene rostro, ojos Senrigan, cuerpo, cabello y vestimenta coherentes en todos los cuadros.
- Daemon con el **atuendo rojo del manga *Two Blue Vortex***; no inventar otra chamarra, ojos, pelo o cara. Referencias originales en `referencias/visuales_usuario`.
- Pixel art estilo MUGEN como la Sumire del GIF, no sprites geométricos o deformes. El usuario detesta las V1-V4 anteriores.
- **Los paneles de Omnipotencia son los paneles que el usuario proporcionó: NO modificar, redibujar, retocar con IA, cambiar expresiones ni reemplazar por una portada.** Solo recortes, encuadres, fades y capas con los originales.
- Captura con sprites de Eida: `Eida_sprites_en_captura.png`. Puede rescatarse lo visible, pero tiene resolución limitada, fotogramas incompletos y no basta para animación profesional. **No afirmar que su calidad ya es profesional**. `recortes_de_captura_BAJA_CALIDAD.zip` son recortes de prueba, no sprites finales.
- La hoja de Sumire y especialmente `Sumire_animacion_referencia.gif` son el estándar **de calidad de dibujo, proporciones y animación**. No copiar a Sumire para convertirla en Eida; usar como nivel de acabado.

## Diseño jugable
- Especificaciones de interfaz reales del usuario: joystick izquierdo hacia izquierda/derecha = caminar, arriba = saltar, diagonales superiores = salto direccional, abajo = agacharse, con orientación y colisiones válidas. No crear animaciones de idle que recorran poses de ataque.
- 3 ataques normales fluidos y ataques aéreos. Golpes físicos ejecutados prioritariamente por Daemon, no inventar habilidades ofensivas no canónicas para Eida.
- Comandos **simples**: abajo→ + botón o abajo← + botón; seis especiales, pudiendo incluir Daemon rápido, combo, contraataque/reflejo y encantamiento de Eida, Senrigan como mecánica de vigilancia/contraataque. Evitar inputs difíciles.
- Ultimate con botón **físico A del control Xbox**, mientras haya suficiente poder, se llama **Omnipotencia**: cinematografía de 8-10 s aprox. con paneles originales y transiciones/sfx. La Omnipotencia en el canon no es una técnica de daño que Eida activa a voluntad; es una adaptación jugable que representa el evento de reescritura de recuerdos.
- Barra/carga de energía con **LB físico** (según captura de controles), mantener para cargar. Efectos de sonido creados sintéticamente sí; no generar voces artificiales.
- Voz japonesa exclusivamente de Eida (actriz Kana Hanazawa), tomando los fragmentos femeninos del `Eida_voz_japonesa_fuente.mp3`. Las voces masculinas del MP3 corresponden a Code: no incluirlas.
- Daemon protege a Eida y realiza animaciones particulares de golpes, aparición, desaparición y reflejo de hostilidad. Representar el canon en lo posible.

## Aclaración CRÍTICA de botones y controles
- Los botones físicos Xbox **no coinciden necesariamente con letras internas de MUGEN**. Usuario mostró captura `controles_configuracion_real.png`, que indica internos **a/b/c** para especiales diagonales, interno **x** para ultimate y **s** para carga en su configuración. Verificar de verdad mapeo contra la captura y el ejecutable, no asumir.
- En `Code.cmd` original los seis especiales son `~D,DF,F,a`, `~D,DB,B,a`, y lo mismo para `b`, `c` (MUGEN significa forward/back relativo al personaje). `[command] SUPER1` usa `~y` en Code original: **no copiar ciegamente**, porque el usuario quiere ultimate física A (captura indica MUGEN `x`).
- La mayoría de fallos anteriores estuvieron en vincular entradas, `StateDef`, estados comunes, animaciones y sprite-group/index. Hay que hacer pruebas de movimiento, ataque, salto y caer al suelo, no solo validar ZIP.

## Entrega correcta y QA
1. Auditar `referencias/Code_FUNCIONAL/Code.def`, `.cmd`, `.cns`, `.air`, `.sff`, `.snd` y archivos `Specials.cns`, `Supers.cns`, `AI.cns`, `common1.cns`. `Code.def` confirma `mugenversion = 1.1` y lista todos los recursos. **Ese Code es referencia técnica, no usar su aspecto como Eida.**
2. Definir mapeo mandos + estados MUGEN y crear pruebas automatizadas de integridad: los nombres y rutas en `Eida.def`; existencias de archivos; `statedef` y `changestate` referencian estados válidos; animaciones del `.air` usan (grupo, índice) presentes en `.sff`; sonidos corresponden a entradas del `.snd`; movimiento/velocidades y estados suelo/aire están configurados.
3. Preparar **una animación de reposo legítima** (mínimos cuadros de reposo solamente), caminar, girar, saltar, caer y aterrizar. Probar cada fase; luego ataques básicos y Daemon; al final Omnipotencia. No crear ZIP final sin validaciones y sin reportar lo no probado.
4. Comparar visualmente Eida con Code en escala dentro de resolución real de MUGEN, no solo reducciones arbitrarias. Cuidar `xscale/yscale`, punto origen y `Clsn1`/`Clsn2`.
5. Distinguir resultados **comprobados mediante script** frente a los **no comprobables sin ejecutable de Jump Force MUGEN V14**; solicitar al usuario una prueba en su computadora solo cuando la build funcione estáticamente.
6. La calidad artística equivalente a Sumire NO está resuelta por los archivos actuales: la captura de Eida es de baja resolución. No simular dibujos profesionales ni prometerlo sin fotogramas reales. Ser transparente, priorizar fase de arte antes de construir una multitud de animaciones ficticias.

## Fallos de las versiones previas (LEER ANTES DE CODIFICAR)
- Primera alfa: Eida gigantesca, controles no respondían, no caminaba ni saltaba, ataques incorrectos; una imagen o portada del manga aparecía como ataque.
- Beta 2: reducción arbitraria del tamaño (56%), estados no corregidos de manera fiable; arreglar solamente `.cmd` no repara movimiento.
- V3: pixel art generado simplificado, desproporcionado, cara estilo "South Park", Daemon incorrecto; usuario rechazó completamente la estética.
- V4: estado de reposo reproduce varios sprites/poses incongruentes como GIF constante sin tocar botones; captura de error en `fallos_anteriores/capturas`. El ZIP V4 se proporciona **solo como ejemplo defectuoso para diagnóstico**, no debe copiarse como base.
- Errores procesales: se prometieron versiones acabadas/compatibles sin poder probar ejecutable; se usaron sprites generados en vez del arte de referencia entregado. No repetir.

## Recursos proporcionados
- `referencias/Code_FUNCIONAL/` — Code completo según `Code.def`, incluidos SFF, SND, AIR, CNS, CMD, adicionales y `code.aseprite`.
- `referencias/Kawashiki_PARCIAL/` — config y archivos de texto recibidos; faltan varios subarchivos listados en su `.def` (por eso no debe considerarse completo).
- `referencias/visuales_usuario/` — manga, Daemon, Eida, controles, Sumire, GIF.
- `referencias/audio/` — clip MP3 con voces de Eida y Code.
- `referencias/recortes_de_captura_BAJA_CALIDAD.zip` — recortes realizados a partir de captura, baja calidad.
- `fallos_anteriores/` — capturas de errores y ZIP V4 roto, para diagnóstico solamente.

## Mensaje de inicio para Codex
"Revisa AGENTS.md y CONTEXTO_PROYECTO.md. Usa Code como referencia funcional y el GIF de Sumire como estándar visual. No copies las betas rotas ni generes pósteres o caricaturas. Haz una auditoría de los archivos y un plan de reparación por fases. Empieza verificando comandos, movimiento en el mando, salto y una animación de reposo coherente; identifica qué recursos gráficos reales faltan antes de prometer una versión final."
