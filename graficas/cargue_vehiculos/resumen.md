# Resumen de la medición

Generado por `medicion.py`; los números cambian un poco en cada computador.

## Factor al duplicar el tamaño

| Solución | Experimento | De → a | Tiempo × | Operaciones × | Esperado × |
|---|---|---|---|---|---|
| Programación dinámica | n pequeño (W = 1000) | 4 → 8 | 5.19 | 2.00 | 2.00 |
| Programación dinámica | n pequeño (W = 1000) | 6 → 12 | 1.66 | 2.00 | 2.00 |
| Programación dinámica | n pequeño (W = 1000) | 8 → 16 | 1.99 | 2.00 | 2.00 |
| Programación dinámica | n pequeño (W = 1000) | 10 → 20 | 1.91 | 2.00 | 2.00 |
| Exhaustiva | n pequeño (W = 1000) | 4 → 8 | 15.86 | 32.00 | 32.00 |
| Exhaustiva | n pequeño (W = 1000) | 6 → 12 | 71.26 | 128.00 | 128.00 |
| Exhaustiva | n pequeño (W = 1000) | 8 → 16 | 361.42 | 512.00 | 512.00 |
| Exhaustiva | n pequeño (W = 1000) | 10 → 20 | 1719.82 | 2048.00 | 2048.00 |
| Regla actual (vencimiento) | n pequeño (W = 1000) | 4 → 8 | 1.84 | 3.00 | 3.00 |
| Regla actual (vencimiento) | n pequeño (W = 1000) | 6 → 12 | 1.39 | 2.17 | 2.77 |
| Regla actual (vencimiento) | n pequeño (W = 1000) | 8 → 16 | 1.16 | 2.32 | 2.67 |
| Regla actual (vencimiento) | n pequeño (W = 1000) | 10 → 20 | 1.43 | 2.37 | 2.60 |
| Voraz por densidad | n pequeño (W = 1000) | 4 → 8 | 1.22 | 2.61 | 3.00 |
| Voraz por densidad | n pequeño (W = 1000) | 6 → 12 | 1.40 | 2.55 | 2.77 |
| Voraz por densidad | n pequeño (W = 1000) | 8 → 16 | 1.48 | 2.52 | 2.67 |
| Voraz por densidad | n pequeño (W = 1000) | 10 → 20 | 5.79 | 2.48 | 2.60 |
| Programación dinámica | n grande (W = 4000) | 50 → 100 | 1.96 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 100 → 200 | 1.90 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 200 → 400 | 2.08 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 300 → 600 | 1.99 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 400 → 800 | 1.98 | 2.00 | 2.00 |
| Programación dinámica | n grande (W = 4000) | 600 → 1200 | 1.66 | 2.00 | 2.00 |
| Regla actual (vencimiento) | n grande (W = 4000) | 50 → 100 | 2.20 | 2.35 | 2.35 |
| Regla actual (vencimiento) | n grande (W = 4000) | 100 → 200 | 1.87 | 2.34 | 2.30 |
| Regla actual (vencimiento) | n grande (W = 4000) | 200 → 400 | 2.68 | 2.26 | 2.26 |
| Regla actual (vencimiento) | n grande (W = 4000) | 300 → 600 | 2.19 | 2.19 | 2.24 |
| Regla actual (vencimiento) | n grande (W = 4000) | 400 → 800 | 1.95 | 2.20 | 2.23 |
| Regla actual (vencimiento) | n grande (W = 4000) | 600 → 1200 | 1.53 | 2.17 | 2.22 |
| Voraz por densidad | n grande (W = 4000) | 50 → 100 | 1.86 | 2.37 | 2.35 |
| Voraz por densidad | n grande (W = 4000) | 100 → 200 | 2.67 | 2.31 | 2.30 |
| Voraz por densidad | n grande (W = 4000) | 200 → 400 | 1.83 | 2.28 | 2.26 |
| Voraz por densidad | n grande (W = 4000) | 300 → 600 | 2.46 | 2.24 | 2.24 |
| Voraz por densidad | n grande (W = 4000) | 400 → 800 | 2.28 | 2.24 | 2.23 |
| Voraz por densidad | n grande (W = 4000) | 600 → 1200 | 1.25 | 2.23 | 2.22 |
| Programación dinámica | W creciente (n = 300) | 500 → 1000 | 3.12 | 2.00 | 2.00 |
| Programación dinámica | W creciente (n = 300) | 1000 → 2000 | 2.51 | 2.00 | 2.00 |
| Programación dinámica | W creciente (n = 300) | 2000 → 4000 | 2.17 | 2.00 | 2.00 |
| Programación dinámica | W creciente (n = 300) | 4000 → 8000 | 2.96 | 2.00 | 2.00 |
| Programación dinámica | W creciente (n = 300) | 8000 → 16000 | 2.49 | 2.00 | 2.00 |

## Constantes ajustadas

* Programación dinámica: 186.7 ns por celda (t ≈ c · n · (W + 1)).
* Regla por vencimiento: 557.5 ns por unidad de n·log2 n.
* Voraz por densidad: 767.6 ns por unidad de n·log2 n.
* Exhaustiva: 215.27 ns por unidad de n·2^n.
* Con la exhaustiva, en toda la ventana de 2 h cabe como máximo una ruta de n = 30 lotes.

## Extrapolación al volumen real (peor caso diario)

14 vehículos, 600 lotes y W = 4.000 kg cada uno (exhaustiva: 300 lotes, su caso más favorable).

| Solución | Tiempo por día | % de la ventana de 2 h | Energía por día (kWh) | Energía por año (kWh) |
|---|---|---|---|---|
| Programación dinámica | 6.27 s | 0.0872 % | 0.000261 | 0.0954 |
| Regla actual (vencimiento) | 43.22 ms | 0.0006 % | 1.8e-06 | 0.000657 |
| Voraz por densidad | 59.51 ms | 0.000826 % | 2.48e-06 | 0.000905 |
| Exhaustiva (n = 300, el caso más pequeño) | 5.84e+79 años | 2.56e+85 % | 7.67e+82 | 2.8e+85 |

La exhaustiva tardaría 5.84e+79 años, 4.23e+69 veces la edad del universo.

Diferencia anual de energía entre la programación dinámica y la regla actual: 0.0948 kWh (95 Wh).

## Un día simulado con el volumen real

Flota sintética (semilla 2026): 14 vehículos, 6193 lotes candidatos en total y 2e+07 celdas de tabla.

| Solución | Tiempo medido del día | Valor nutricional total | Ocupación media | Ocupación mínima |
|---|---|---|---|---|
| Programación dinámica | 2.67 s | 637,554 (100.0 % del óptimo) | 100.0 % | 99.9 % |
| Regla actual (vencimiento) | 55.75 ms | 270,154 (42.4 % del óptimo) | 94.2 % | 88.6 % |
| Voraz por densidad | 52.96 ms | 635,971 (99.8 % del óptimo) | 99.7 % | 99.2 % |

## Fallos de las reglas en 1.000 instancias pequeñas

* Regla actual (vencimiento): no llega al óptimo en 537 de 1000; la mayor pérdida fue 100 % del óptimo.
* Voraz por densidad: no llega al óptimo en 127 de 1000; la mayor pérdida fue 50 % del óptimo.
