# Transparencia de Uzuhiko en MUGEN

El video `uzuhiko_bug_video_reference.json` muestra cortes rectos en el viento desde el segundo 14 y un tornado negro al conectar, visible alrededor del segundo 18.5. La prueba anterior en Ikemen aceptaba la transparencia indicada en el controlador Explod y no detectaba la falta de transparencia en AIR.

Las animaciones 8815, 8816 y 8817 ahora llevan `A` en cada cuadro del AIR. La mano y el tornado no dependen del parámetro `trans` de Explod. Los nueve cuadros originales AnginRibut mantienen sus PNG originales; únicamente se suavizan los cuatro bordes de su copia indexada antes de empacarla. Los otros 698 sprites empacados, incluidos los cuatro cuadros del tornado, conservan exactamente sus dimensiones, origen, píxeles indexados y paleta.

La prueba `check_boruto_uzuhiko_rendering.py` detecta el error en el AIR anterior. Comprueba los veinte cuadros de viento, mano y tornado sin extensiones de Explod, la suma de color sobre fondos claros y oscuros y que los bordes de los nueve lienzos no dibujen una línea. Es una comprobación de los datos empacados y de la mezcla AIR; la grabación y cuatro casos de ambas formas y direcciones se ejecutan por separado en Ikemen GO. El ejecutable de MUGEN del usuario sólo está documentado por el video aportado.

Las entradas, daño, alcance, costes, captura y liberación de Uzuhiko se mantienen. RT conserva los dos Rasengan azules, abajo + RT el Fūton verde y abajo + RB el Mokuton exclusivamente en despertar.
