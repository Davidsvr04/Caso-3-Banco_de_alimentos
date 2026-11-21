# Resumen de la medición — consulta de inventario

## Factor al duplicar n

| Consulta | Solución | n → 2n | Tiempo × | Operaciones × | Esperado × |
|---|---|---|---|---|---|
| codigo | Lineal (actual) | 14,312 → 28,625 | 2.06 | 2.00 | 2.00 |
| codigo | Lineal (actual) | 28,625 → 57,250 | 2.08 | 2.00 | 2.00 |
| codigo | Lineal (actual) | 57,250 → 114,500 | 1.88 | 2.00 | 2.00 |
| codigo | Lineal (actual) | 114,500 → 229,000 | 2.03 | 2.00 | 2.00 |
| codigo | Lineal (actual) | 229,000 → 458,000 | 2.04 | 2.00 | 2.00 |
| codigo | Búsqueda binaria | 14,312 → 28,625 | 1.09 | 1.07 | 1.07 |
| codigo | Búsqueda binaria | 28,625 → 57,250 | 1.21 | 1.07 | 1.07 |
| codigo | Búsqueda binaria | 57,250 → 114,500 | 1.06 | 1.06 | 1.06 |
| codigo | Búsqueda binaria | 114,500 → 229,000 | 1.23 | 1.06 | 1.06 |
| codigo | Búsqueda binaria | 229,000 → 458,000 | 1.37 | 1.06 | 1.06 |
| codigo | Tabla hash | 14,312 → 28,625 | 1.49 | 1.00 | 1.00 |
| codigo | Tabla hash | 28,625 → 57,250 | 1.31 | 1.00 | 1.00 |
| codigo | Tabla hash | 57,250 → 114,500 | 1.25 | 1.00 | 1.00 |
| codigo | Tabla hash | 114,500 → 229,000 | 1.10 | 1.00 | 1.00 |
| codigo | Tabla hash | 229,000 → 458,000 | 1.26 | 1.00 | 1.00 |
| rango | Lineal (actual) | 14,312 → 28,625 | 2.01 | 2.00 | 2.00 |
| rango | Lineal (actual) | 28,625 → 57,250 | 2.28 | 2.00 | 2.00 |
| rango | Lineal (actual) | 57,250 → 114,500 | 1.80 | 2.00 | 2.00 |
| rango | Lineal (actual) | 114,500 → 229,000 | 2.07 | 2.00 | 2.00 |
| rango | Lineal (actual) | 229,000 → 458,000 | 2.13 | 2.00 | 2.00 |
| rango | Búsqueda binaria | 14,312 → 28,625 | 1.24 | 2.01 | 2.00 |
| rango | Búsqueda binaria | 28,625 → 57,250 | 2.46 | 2.01 | 2.00 |
| rango | Búsqueda binaria | 57,250 → 114,500 | 1.53 | 1.99 | 2.00 |
| rango | Búsqueda binaria | 114,500 → 229,000 | 2.79 | 1.97 | 2.00 |
| rango | Búsqueda binaria | 229,000 → 458,000 | 3.11 | 2.01 | 2.00 |

## Volumen real: n = 229,000 lotes, 30,000 consultas por código al día

* Peor consulta lineal (código inexistente): 12.5 ms (límite: 1 s).
* Consulta con tabla hash: 0.39 µs.
* Construir la tabla hash: 0.023 s una vez al día; ordenar por código para la búsqueda binaria: 0.93 s.
* Consultas por rango en la ventana (14 al día): actual 0.25 s, propuesta 0.025 s (incluye construir la tabla hash; la lista FEFO la entrega la operación 2).
* Consultas por código del alistamiento: actual 243.7 s, hash 0.012 s, binaria 0.084 s.
* Energía al año (300 días, 150 W): actual 3.049 kWh, propuesta 0.0005 kWh.

## Volumen crecimiento: n = 458,000 lotes, 60,000 consultas por código al día

* Peor consulta lineal (código inexistente): 24.9 ms (límite: 1 s).
* Consulta con tabla hash: 0.49 µs.
* Construir la tabla hash: 0.065 s una vez al día; ordenar por código para la búsqueda binaria: 2.10 s.
* Consultas por rango en la ventana (14 al día): actual 0.54 s, propuesta 0.069 s (incluye construir la tabla hash; la lista FEFO la entrega la operación 2).
* Consultas por código del alistamiento: actual 995.9 s, hash 0.030 s, binaria 0.230 s.
* Energía al año (300 días, 150 W): actual 12.455 kWh, propuesta 0.0012 kWh.
