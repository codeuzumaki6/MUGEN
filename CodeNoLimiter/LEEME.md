# Code No Limiter

Extrae `CodeNoLimiter` dentro de `chars/` y añade a `[Characters]` de `data/select.def`:

```ini
CodeNoLimiter/CodeNoLimiter.def
```

Personaje independiente para MUGEN 1.1, probado en Ikemen GO. Incluye sus sprites, audio y estados comunes. Se instala con nombre propio para convivir con otros personajes llamados Code. Vida 1300, defensa 110 y energía máxima 3000.

La base ya es **Code sin limitadores, con cabello blanco**. **Abajo + Pausa** con 3000 de energía refuerza el Karma durante 20 segundos: consume 1500, aumenta el daño y permite dos Claw Grimes simultáneos. Tiene 25 segundos de recarga desde la activación y termina cuando Code recupera el control. Conserva su cuerpo original; se distingue por el aura morada y los ataques reforzados.

**RB** coloca una marca de garra de ocho segundos en dirección al rival, hasta 220 unidades de distancia. **RT** viaja a esa misma marca, emerge y golpea. Si no hay marca, prepara una para el viaje. La marca permanece en su posición y se puede reutilizar mientras dure. Las emboscadas también utilizan su posición real. Los dibujos de las marcas, la entrada y la salida proceden del atlas original.

**Abajo-adelante + X** invoca un Claw Grime que sigue al rival y ataca por su cuenta mientras Code queda libre para moverse y combatir. Tiene 180 de vida y dura hasta siete segundos. Los golpes lo aturden y pueden destruirlo; no recupera la vida al volver a atacar. Hay uno como máximo en base y dos en despertar. **Abajo-atrás + Y** ordena un asalto del Grime superior. **Abajo + RB** coordina el ataque y puede invocar el segundo Grime durante el despertar. Durante la ulti esperan para conservar su límite de daño.

Las técnicas de Karma, la doble emboscada, el ascenso y los golpes del video usan sus secuencias completas. Los cuadros que ya incluyen a Code se reproducen en el personaje. Los Grimes usan sus propios cuerpos; las marcas, el árbol y las descargas son efectos separados.

**A** ejecuta el cerco de Claw Grimes y el asalto de Karma: apertura, escenario dimensional, ejército, ataques conjuntos, carga y columna morada. Requiere conectar una colisión real; puede bloquearse y fallar por alcance. Ocho impactos causan como máximo `min(650, floor(vida máxima rival × .65))` en base y `min(800, floor(vida máxima rival × .80))` en despertar. Cuesta 3000 y no consume vida propia. Un golpe que interrumpa a Code detiene el daño y libera al rival. La columna se coloca en el suelo sobre el objetivo alcanzado. Sus cuadros ya contienen a Code y sustituyen su animación principal durante esa parte de la ulti; conserva cajas para recibir golpes también dentro de la columna.

Mantener Pausa carga energía con la animación original del aura morada. Doble toque a izquierda o derecha ejecuta un dash terrestre gratuito. Las dos formas conservan sus cajas para recibir golpes, guardia y recuperación. `CONTROLES_XBOX.md` detalla las entradas y costes.

El ZIP nuevo no incluye audios: las voces y el sonido de garra se toman del Code de MUGEN STARS aportado anteriormente por el usuario. Los 241 cuadros válidos de Code y los Grimes proceden del nuevo paquete de Vaydra. No se generaron dibujos ni voces. El atlas de Karasu conserva marionetas ajenas a este personaje y se guarda entre las fuentes, sin usarlo en combate.

El gameplay y las pruebas usan Ikemen GO con audio real del motor. El ejecutable exacto de MUGEN de Windows y un mando físico no están disponibles en este entorno.
