# Acabado de Pochita

Solicitud del usuario: aplicar los detalles revisados en su video de Pochita contra Gyro a la carga, movimiento, contactos y victoria de Pochita. El video se analiza visualmente; no se afirma haber escuchado su pista. Se conserva su ficha con hash en `reference.json`.

16 poses nuevas generadas/editadas con IA a partir del modelo aprobado: cuatro de carga, cuatro de carrera, dos de frenado, dos de aterrizaje y cuatro de victoria. Se extraen siluetas completas por componentes y se calibra una sola escala corporal para ambas hojas, a partir de la pose neutral final. Polvo, chispas metálicas y corte: tres familias de cuatro cuadros, extraídas con transparencia binaria para el SFF.

La programación conserva alcance por colisión, daños, energía, controles, combos aéreos, agarres, despertar, límite de la ultimate y recuperación. Cambios de tiempo: dos ticks más de pausa en los remates seleccionados. Frenar permite cancelar inmediatamente; aterrizar sigue durando nueve ticks. Todos los efectos expiran, el motor se detiene al soltar/interrumpir la carga y la victoria termina su espera. Durante la victoria se evita la ralentización de KO para mantener el ritmo de los motores. La bandera de fin de ronda usa `RoundNotOver`, de MUGEN; el validador rechaza banderas ajenas a MUGEN.

Validación: comprobaciones nativas de archivos, reconstrucción determinista, colisiones/entradas en Ikemen GO, presentación a ambos lados y una victoria por KO real en cada orientación. Las grabaciones de motor incluyen audio SDL real, sincronizado por correlación con las muestras del SND. No sustituye pruebas en el MUGEN 1.1 exacto del usuario ni partidas de equilibrio contra todo su plantel.
