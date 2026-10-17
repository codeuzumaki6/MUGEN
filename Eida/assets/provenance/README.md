# Hoja de apoyo de Eida

`eida_support_sheet.png` conserva la salida generada mediante IA a partir de los sprites actuales de Eida. Contiene seis poses de preparación, observación, extensión de palma y regreso. No contiene manga ni voz.

`tools/build_presentation.py` separa las seis celdas, normaliza a 68 píxeles de silueta (la altura visible del reposo original), conserva proporciones y empaqueta cada figura en un lienzo de 96×72 con eje de pies común (48,70). Solo se usan en acciones de apoyo. Los sprites de reposo originales se conservan.

Los cuadros nuevos no completan los ciclos pendientes de carrera, golpe y reacciones. La referencia de acabado de Sumire sigue siendo una meta, no una calidad declarada.
