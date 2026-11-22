# Resumen de la medición — saturación de la bodega

## Factor al duplicar n

| Estrategia | n → 2n | Tiempo × | Operaciones × | Esperado × |
|---|---|---|---|---|
| Fuerza bruta (actual) | 25 → 50 | 6.35 | 7.56 | 7.56 |
| Fuerza bruta (actual) | 50 → 100 | 7.38 | 7.77 | 7.77 |
| Fuerza bruta (actual) | 100 → 200 | 7.19 | 7.88 | 7.88 |
| Fuerza bruta (actual) | 200 → 400 | 9.72 | 7.94 | 7.94 |
| Fuerza bruta (actual) | 400 → 800 | 8.18 | 7.97 | 7.97 |
| Todos los tramos acumulados | 25 → 50 | 2.74 | 3.92 | 3.92 |
| Todos los tramos acumulados | 50 → 100 | 3.57 | 3.96 | 3.96 |
| Todos los tramos acumulados | 100 → 200 | 4.09 | 3.98 | 3.98 |
| Todos los tramos acumulados | 200 → 400 | 4.66 | 3.99 | 3.99 |
| Todos los tramos acumulados | 400 → 800 | 4.26 | 4.00 | 4.00 |
| Todos los tramos acumulados | 800 → 1,600 | 3.58 | 4.00 | 4.00 |
| Todos los tramos acumulados | 1,600 → 3,200 | 4.16 | 4.00 | 4.00 |
| Todos los tramos acumulados | 3,200 → 6,400 | 3.77 | 4.00 | 4.00 |
| Todos los tramos acumulados | 6,400 → 12,800 | 4.27 | 4.00 | 4.00 |
| Dividir y vencer | 25 → 50 | 1.60 | 2.35 | 2.43 |
| Dividir y vencer | 50 → 100 | 2.09 | 2.30 | 2.35 |
| Dividir y vencer | 100 → 200 | 1.87 | 2.26 | 2.30 |
| Dividir y vencer | 200 → 400 | 2.23 | 2.23 | 2.26 |
| Dividir y vencer | 400 → 800 | 3.47 | 2.21 | 2.23 |
| Dividir y vencer | 800 → 1,600 | 1.12 | 2.19 | 2.21 |
| Dividir y vencer | 1,600 → 3,200 | 2.08 | 2.17 | 2.19 |
| Dividir y vencer | 3,200 → 6,400 | 2.19 | 2.16 | 2.17 |
| Dividir y vencer | 6,400 → 12,800 | 1.96 | 2.15 | 2.16 |
| Dividir y vencer | 36,000 → 72,000 | 2.77 | 2.12 | 2.13 |
| Kadane | 25 → 50 | 1.78 | 2.00 | 2.00 |
| Kadane | 50 → 100 | 0.82 | 2.00 | 2.00 |
| Kadane | 100 → 200 | 1.56 | 2.00 | 2.00 |
| Kadane | 200 → 400 | 1.67 | 2.00 | 2.00 |
| Kadane | 400 → 800 | 2.03 | 2.00 | 2.00 |
| Kadane | 800 → 1,600 | 1.70 | 2.00 | 2.00 |
| Kadane | 1,600 → 3,200 | 2.02 | 2.00 | 2.00 |
| Kadane | 3,200 → 6,400 | 2.04 | 2.00 | 2.00 |
| Kadane | 6,400 → 12,800 | 1.87 | 2.00 | 2.00 |
| Kadane | 36,000 → 72,000 | 3.22 | 2.00 | 2.00 |

## Una corrida completa: 40 categorías × 36.000 horas

| Estrategia | Por categoría | 40 categorías | Fuente | Energía por corrida (kWh) | Energía al año, 1 corrida (kWh) |
|---|---|---|---|---|---|
| Fuerza bruta (actual) | 3 días | 106 días | extrapolado | 382.3 | 382.3 |
| Todos los tramos acumulados | 31.0 s | 20.7 min | extrapolado | 0.05167 | 0.05167 |
| Dividir y vencer | 47.4 ms | 1.9 s | medido | 7.897e-05 | 7.897e-05 |
| Kadane | 2.3 ms | 92.2 ms | medido | 3.84e-06 | 3.84e-06 |

* c (Fuerza bruta (actual)) = 29.50 ns por unidad del modelo.

* c (Todos los tramos acumulados) = 47.84 ns por unidad del modelo.

* c (Dividir y vencer) = 95.62 ns por unidad del modelo.

* c (Kadane) = 75.71 ns por unidad del modelo.
