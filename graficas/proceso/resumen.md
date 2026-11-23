# Resumen del proceso completo

## Escenario real

| Operación | Momento | Actual | Propuesta | kWh/año actual | kWh/año propuesta |
|---|---|---|---|---|---|
| 1a. Lotes por vencer (rango) | ventana | 253 ms | 25 ms | 0.00316 | 0.0003071 |
| 1b. Consulta por código | alistamiento | 4.1 min | 12 ms | 3.046 | 0.0001461 |
| 2. Ordenamiento FEFO | ventana | 5.0 min | 43 ms | 3.766 | 0.000538 |
| 3. Cargue de vehículos | ventana | 12 ms | 2.1 s | 0.0001457 | 0.02622 |
| 4. Saturación (por corrida) | análisis | 106 días | 92 ms | 382.3 | 3.84e-06 |

* Ventana (1a + 2 + 3): actual 5.0 min (4.2 % de 2 h); propuesta 2.2 s (0.03 %).
* Energía al año (medida y extrapolada): actual 389.1 kWh; propuesta 0.027 kWh.

## Escenario crecimiento

| Operación | Momento | Actual | Propuesta | kWh/año actual | kWh/año propuesta |
|---|---|---|---|---|---|
| 1a. Lotes por vencer (rango) | ventana | 539 ms | 69 ms | 0.00674 | 0.0008668 |
| 1b. Consulta por código | alistamiento | 16.6 min | 30 ms | 12.45 | 0.0003693 |
| 2. Ordenamiento FEFO | ventana | 20.1 min | 86 ms | 15.06 | 0.001075 |
| 3. Cargue de vehículos | ventana | 23 ms | 4.2 s | 0.0002915 | 0.05243 |
| 4. Saturación (por corrida) | análisis | 212 días | 184 ms | 764.6 | 7.68e-06 |

* Ventana (1a + 2 + 3): actual 20.1 min (16.7 % de 2 h); propuesta 4.3 s (0.06 %).
* Energía al año (medida y extrapolada): actual 792.1 kWh; propuesta 0.055 kWh.

## Línea base reportada por el cliente

* La planeación tarda hoy 4.5 h: 0.15 kW × 4.5 h = 0.675 kWh por día y 202.5 kWh al año (300 días).
* Con la propuesta, la ventana usa 2.2 s: 0.0271 kWh al año.
* Ahorro anual frente a la línea base reportada: 202.5 kWh, unos 44.5 kg de CO₂e con el factor de 0.22 kg/kWh.
* Esos 44.5 kg de CO₂e equivalen a 17.8 kg de alimento desechado (2.5 kg CO₂e por kg).
