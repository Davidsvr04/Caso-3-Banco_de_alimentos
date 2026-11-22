# Resumen de la medición — ordenamiento FEFO

## Factor al duplicar n

| Estrategia | n → 2n | Tiempo × | Comparaciones × | Esperado × |
|---|---|---|---|---|
| Inserción (actual) | 1,789 → 3,578 | 4.01 | 3.94 | 4.03 |
| Inserción (actual) | 3,578 → 7,156 | 4.61 | 4.04 | 3.99 |
| Inserción (actual) | 7,156 → 14,312 | 4.17 | 3.97 | 4.00 |
| Inserción (actual) | 14,312 → 28,625 | 4.24 | 4.00 | 4.00 |
| Inserción (actual) | 28,625 → 57,250 | 4.12 | 3.99 | 4.00 |
| Mezcla de toda la lista | 1,789 → 3,578 | 2.23 | 2.19 | 2.19 |
| Mezcla de toda la lista | 3,578 → 7,156 | 2.85 | 2.17 | 2.17 |
| Mezcla de toda la lista | 7,156 → 14,312 | 1.84 | 2.16 | 2.16 |
| Mezcla de toda la lista | 14,312 → 28,625 | 3.09 | 2.15 | 2.14 |
| Mezcla de toda la lista | 28,625 → 57,250 | 1.43 | 2.14 | 2.14 |
| Mezcla de toda la lista | 57,250 → 114,500 | 2.46 | 2.13 | 2.13 |
| Mezcla de toda la lista | 114,500 → 229,000 | 2.31 | 2.12 | 2.12 |
| Mezcla de toda la lista | 229,000 → 458,000 | 1.89 | 2.11 | 2.11 |
| Ordenar nuevos + fusionar | 1,789 → 3,578 | 2.18 | 2.37 | 2.07 |
| Ordenar nuevos + fusionar | 3,578 → 7,156 | 2.09 | 2.11 | 2.06 |
| Ordenar nuevos + fusionar | 7,156 → 14,312 | 2.84 | 2.26 | 2.06 |
| Ordenar nuevos + fusionar | 14,312 → 28,625 | 1.67 | 2.18 | 2.06 |
| Ordenar nuevos + fusionar | 28,625 → 57,250 | 2.96 | 2.16 | 2.06 |
| Ordenar nuevos + fusionar | 57,250 → 114,500 | 1.82 | 2.15 | 2.05 |
| Ordenar nuevos + fusionar | 114,500 → 229,000 | 2.28 | 2.13 | 2.05 |
| Ordenar nuevos + fusionar | 229,000 → 458,000 | 2.00 | 2.13 | 2.05 |

## Extrapolación

Inserción: c = 152.2 ns por unidad de (n − k)·k, ajustada con n ≥ 14.000.

| Estrategia | n = 229.000 (real) | n = 458.000 (crecimiento) | Energía al año, real (kWh) |
|---|---|---|---|
| Inserción (actual) | 301.289 s (extrapolado) | 1205.154 s (extrapolado) | 3.7661 |
| Mezcla de toda la lista | 0.801 s (medido) | 1.510 s (medido) | 0.0100 |
| Ordenar nuevos + fusionar | 0.043 s (medido) | 0.086 s (medido) | 0.0005 |
