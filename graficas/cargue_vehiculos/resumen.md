# Resumen de la medición

Generado por `medicion.py`; los números cambian un poco en cada computador.

## Factor al duplicar el tamaño

| Solución | Experimento | De → a | Tiempo × | Operaciones × | Esperado × |
|---|---|---|---|---|---|
| Programación dinámica | n pequeño (W = 1000) | 4 → 8 | 3.44 | 2.00 | 2.00 |
| Programación dinámica | n pequeño (W = 1000) | 6 → 12 | 1.77 | 2.00 | 2.00 |
| Programación dinámica | n pequeño (W = 1000) | 8 → 16 | 1.11 | 2.00 | 2.00 |
| Programación dinámica | n pequeño (W = 1000) | 10 → 20 | 1.53 | 2.00 | 2.00 |
| Exhaustiva | n pequeño (W = 1000) | 4 → 8 | 6.29 | 32.00 | 32.00 |
| Exhaustiva | n pequeño (W = 1000) | 6 → 12 | 61.70 | 128.00 | 128.00 |
| Exhaustiva | n pequeño (W = 1000) | 8 → 16 | 388.23 | 512.00 | 512.00 |
| Exhaustiva | n pequeño (W = 1000) | 10 → 20 | 1365.94 | 2048.00 | 2048.00 |
| Regla actual (vencimiento) | n pequeño (W = 1000) | 4 → 8 | 1.11 | 3.05 | 3.00 |
| Regla actual (vencimiento) | n pequeño (W = 1000) | 6 → 12 | 1.11 | 2.10 | 2.77 |
| Regla actual (vencimiento) | n pequeño (W = 1000) | 8 → 16 | 1.22 | 2.24 | 2.67 |
| Regla actual (vencimiento) | n pequeño (W = 1000) | 10 → 20 | 1.74 | 2.28 | 2.60 |
| Voraz por densidad | n pequeño (W = 1000) | 4 → 8 | 1.19 | 2.60 | 3.00 |
| Voraz por densidad | n pequeño (W = 1000) | 6 → 12 | 1.23 | 2.50 | 2.77 |
| Voraz por densidad | n pequeño (W = 1000) | 8 → 16 | 1.47 | 2.42 | 2.67 |
| Voraz por densidad | n pequeño (W = 1000) | 10 → 20 | 1.72 | 2.42 | 2.60 |
| Programación dinámica | n grande (W = 4000) | 50 → 100 | 1.93 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 100 → 200 | 1.92 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 200 → 400 | 2.06 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 300 → 600 | 1.90 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 400 → 800 | 1.90 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 600 → 1200 | 1.99 | 2.00 | 2.00 |
| Regla actual (vencimiento) | n grande (W = 4000) | 50 → 100 | 1.84 | 2.34 | 2.35 |
| Regla actual (vencimiento) | n grande (W = 4000) | 100 → 200 | 1.76 | 2.33 | 2.30 |
| Regla actual (vencimiento) | n grande (W = 4000) | 200 → 400 | 2.80 | 2.26 | 2.26 |
| Regla actual (vencimiento) | n grande (W = 4000) | 300 → 600 | 2.07 | 2.19 | 2.24 |
| Regla actual (vencimiento) | n grande (W = 4000) | 400 → 800 | 1.72 | 2.20 | 2.23 |
| Regla actual (vencimiento) | n grande (W = 4000) | 600 → 1200 | 2.12 | 2.17 | 2.22 |
| Voraz por densidad | n grande (W = 4000) | 50 → 100 | 2.13 | 2.37 | 2.35 |
| Voraz por densidad | n grande (W = 4000) | 100 → 200 | 2.53 | 2.31 | 2.30 |
| Voraz por densidad | n grande (W = 4000) | 200 → 400 | 2.01 | 2.28 | 2.26 |
| Voraz por densidad | n grande (W = 4000) | 300 → 600 | 2.24 | 2.24 | 2.24 |
| Voraz por densidad | n grande (W = 4000) | 400 → 800 | 2.04 | 2.24 | 2.23 |
| Voraz por densidad | n grande (W = 4000) | 600 → 1200 | 2.21 | 2.23 | 2.22 |
| Programación dinámica | W creciente (n = 300) | 500 → 1000 | 3.39 | 2.00 | 2.00 |
| Programación dinámica | W creciente (n = 300) | 1000 → 2000 | 2.42 | 2.00 | 2.00 |
| Programación dinámica | W creciente (n = 300) | 2000 → 4000 | 2.23 | 2.00 | 2.00 |
| Programación dinámica | W creciente (n = 300) | 4000 → 8000 | 2.26 | 2.00 | 2.00 |
| Programación dinámica | W creciente (n = 300) | 8000 → 16000 | 1.96 | 2.00 | 2.00 |

## Constantes ajustadas

* Programación dinámica: 62.4 ns por celda (t ≈ c · n · (W + 1)).
* Regla por vencimiento: 150.4 ns por unidad de n·log2 n.
* Voraz por densidad: 212.0 ns por unidad de n·log2 n.
* Exhaustiva: 62.47 ns por unidad de n·2^n.
* Con la exhaustiva, en toda la ventana de 2 h cabe como máximo una ruta de n = 31 lotes.

## Extrapolación al volumen real (peor caso diario)

14 vehículos, 600 lotes y W = 4.000 kg cada uno (exhaustiva: 300 lotes, su caso más favorable).

| Solución | Tiempo por día | % de la ventana de 2 h | Energía por día (kWh) | Energía por año (kWh) |
|---|---|---|---|---|
| Programación dinámica | 2.10 s | 0.0291 % | 8.74e-05 | 0.0319 |
| Regla actual (vencimiento) | 11.66 ms | 0.000162 % | 4.86e-07 | 0.000177 |
| Voraz por densidad | 16.43 ms | 0.000228 % | 6.85e-07 | 0.00025 |
| Exhaustiva (n = 300, el caso más pequeño) | 1.69e+79 años | 7.42e+84 % | 2.23e+82 | 8.13e+84 |

La exhaustiva tardaría 1.69e+79 años, 1.23e+69 veces la edad del universo.

Diferencia anual de energía entre la programación dinámica y la regla actual: 0.0317 kWh (32 Wh).

## Un día simulado con el volumen real

Flota sintética (semilla 2026): 14 vehículos, 6193 lotes candidatos en total y 2e+07 celdas de tabla.

| Solución | Tiempo medido del día | Valor nutricional total | Ocupación media | Ocupación mínima |
|---|---|---|---|---|
| Programación dinámica | 1.26 s | 637,554 (100.0 % del óptimo) | 100.0 % | 99.9 % |
| Regla actual (vencimiento) | 8.49 ms | 270,154 (42.4 % del óptimo) | 94.2 % | 88.6 % |
| Voraz por densidad | 11.85 ms | 635,971 (99.8 % del óptimo) | 99.7 % | 99.2 % |

## Fallos de las reglas en 1.000 instancias pequeñas

* Regla actual (vencimiento): no llega al óptimo en 537 de 1000; la mayor pérdida fue 100 % del óptimo.
* Voraz por densidad: no llega al óptimo en 127 de 1000; la mayor pérdida fue 50 % del óptimo.
