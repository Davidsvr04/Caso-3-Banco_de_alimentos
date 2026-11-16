# Proyecto final — Caso 3: Banco de alimentos

**Integrantes**

- David Viloria
- Luis Lopera
- Leonel Antonio
- Juana Ospina

**Caso asignado:** Caso 3 — Banco de alimentos.

**Estado del informe:** esta versión corresponde al Laboratorio 4 (entrega del 18 de noviembre de 2026) y desarrolla completa la **operación 3: cargue de los vehículos**, resuelta con programación dinámica (mochila 0/1). Lo que corresponde a la otra operación y al proceso completo está marcado como pendiente.

## Contenido

1. [Análisis del problema](#1-análisis-del-problema)
2. [Diseño de la solución](#2-diseño-de-la-solución)
3. [Implementación](#3-implementación)
4. [Evaluación del desempeño](#4-evaluación-del-desempeño)
5. [Análisis comparativo](#5-análisis-comparativo)
6. [Implicaciones éticas, sociales y ambientales](#6-implicaciones-éticas-sociales-y-ambientales)
7. [Conclusiones](#7-conclusiones)
8. [Reproducción](#8-reproducción)

---

## 1. Análisis del problema

### 1.1 Proceso completo y operaciones críticas

Pendiente para la entrega del 23 de noviembre.

### 1.2 Operación 3: cargue de los vehículos

Cada madrugada, entre las 03:00 y las 05:00, el banco de alimentos planea qué lotes sube a cada vehículo. Un lote es una unidad que no se parte: o va completo en el vehículo o se queda en la bodega. El objetivo es que cada vehículo salga con el mayor valor nutricional posible sin pasarse de su capacidad.

**Entradas** (por cada vehículo, es decir, por cada ruta):

| Dato | Tipo y unidad | Límites que informa el caso |
|---|---|---|
| `capacidad_kg` (W) | entero, kilogramos | entre 2.500 y 4.000 kg |
| `lotes` | lista de tuplas `(peso_kg, valor_nutricional, dias_para_vencer)` | entre 300 y 600 lotes candidatos por ruta |
| `peso_kg` de cada lote | entero, kilogramos | mayor que 0 |
| `valor_nutricional` de cada lote | entero, raciones ponderadas por la prioridad de la categoría | mayor o igual que 0 |
| `dias_para_vencer` de cada lote | entero, días | solo lo usa la regla actual |

En un día hay 14 vehículos, así que la operación se ejecuta 14 veces, una por ruta.

**Salida:** el valor nutricional total cargado y la lista de índices (posiciones en `lotes`) de los lotes que suben, en orden creciente.

**Restricciones del negocio:**

1. La suma de los pesos de los lotes cargados no puede superar `capacidad_kg`.
2. Ningún lote se fracciona: cada índice aparece como máximo una vez y aporta su valor completo.
3. El valor cargado debe ser **el máximo posible**, no una aproximación.
4. Todo debe caber en la ventana de planeación de 2 horas (03:00 a 05:00), que la operación 3 comparte con las operaciones 1 y 2, en un computador de unos 150 W.

### 1.3 Supuestos

- **Pesos enteros en kilogramos.** El caso así lo dice, y esto es lo que permite usar la capacidad como índice de la tabla. Si llegara un peso con decimales se redondearía hacia arriba, para no correr el riesgo de pasarse de la capacidad.
- **Una ruta por vehículo.** Los 14 vehículos tienen cada uno su propia lista de lotes candidatos, y la planeación de un vehículo no afecta la de otro. Un lote no compite por dos vehículos a la vez.
- **Planeación diaria.** La ventana de 03:00 a 05:00 se repite todos los días, así que para la proyección anual usamos 365 ejecuciones.
- **Interpretación de la regla actual.** El coordinador ordena los lotes del que vence primero al que vence último. Los va subiendo en ese orden y **se detiene en el primer lote que no cabe**, aunque más adelante haya lotes más livianos que sí cabrían. Si dos lotes vencen el mismo día, va primero el que aparece antes en la lista. Ejemplo: con 100 kg de capacidad y los lotes A (60 kg, vence en 1 día), B (50 kg, 2 días) y C (10 kg, 3 días), la regla sube A, ve que B ya no cabe (110 kg) y para. C nunca se revisa. El vehículo sale con 60 kg.
- **Interpretación de la regla por densidad.** Se ordena por valor nutricional por kilogramo, de mayor a menor (en empate, el índice menor). Esta regla **no** se detiene: si un lote no cabe, lo salta y prueba el siguiente. La comparación se hace con enteros (`v_i · w_j` frente a `v_j · w_i`) para no depender del redondeo.
- **Empates en el óptimo.** Si hay varias cargas con el mismo valor máximo, cualquiera es válida. Las pruebas comparan el valor, no la lista exacta de lotes.
- **Datos sintéticos.** Los lotes de las mediciones se generan en cinco categorías inventadas por el equipo (proteína, lácteos, frutas y verduras, granos, enlatados). Cada categoría tiene sus propias raciones por kg, su prioridad y su rango de días para vencer, con pesos entre 20 y 500 kg. No son cifras del cliente: solo le dan una estructura realista a los datos.

---

## 2. Diseño de la solución

### 2.1 Estructuras de datos, diagramas y pseudocódigo del proceso completo

Pendiente para la entrega del 23 de noviembre.

### 2.2 Operación 3: por qué el problema admite programación dinámica

El cargue de un vehículo es una **mochila 0/1**: cada lote tiene un peso y un valor, el vehículo tiene una capacidad, y cada lote sube entero o no sube. Lo resolvemos decidiendo lote por lote si sube o no. Lo que queda después de cada decisión se describe con dos números: cuántos lotes faltan por decidir y cuántos kilogramos siguen libres.

**Subestructura óptima.** Tome una carga óptima para los primeros `i` lotes con `w` kg libres. Hay dos posibilidades:

- Si el lote `i` **no** está en esa carga, lo que se cargó es una carga óptima para los primeros `i − 1` lotes con los mismos `w` kg.
- Si el lote `i` **sí** está, el resto de la carga tiene que ser óptimo para los primeros `i − 1` lotes con `w − peso_i` kg. Si no lo fuera, se podría cambiar ese resto por uno mejor que pese lo mismo o menos, y la carga total subiría de valor. Eso contradice que fuera óptima.

Es decir, la mejor solución del problema grande se arma con la mejor solución de un problema más pequeño del mismo tipo.

**Subproblemas que se repiten.** Muchas decisiones distintas terminan en el mismo subproblema. En el ejemplo de la sección 2.4, el subproblema "lo mejor con L0 y L1 en 5 kg" (`K[2][5]`) lo necesitan dos casillas diferentes:

- `K[3][5]`, cuando decide **no** subir L2 (se queda con los mismos 5 kg),
- `K[3][10]`, cuando decide **sí** subir L2 (le quedan 10 − 5 = 5 kg).

Con 300 lotes, la búsqueda exhaustiva tendría que revisar 2³⁰⁰ subconjuntos. En cambio, solo existen `(n + 1)·(W + 1)` subproblemas distintos. Para el peor caso real son 601 × 4.001 ≈ 2,4 millones. Al guardar cada uno en una tabla, se calcula una sola vez.

**¿Por qué no una regla voraz?** Porque elegir un lote cambia la capacidad que queda, y un lote que parece buena idea ahora puede dejar un hueco que ningún otro lote llena. La sección 5.1 lo muestra con números para las dos reglas voraces que se usan o se podrían usar.

### 2.3 La recurrencia

Definimos `K[i][w]` como **el mayor valor nutricional que se puede cargar escogiendo solo entre los primeros `i` lotes, en un vehículo con `w` kg de capacidad**. La respuesta para un vehículo es `K[n][W]`.

```
K[0][w] = 0                                                  para todo w   (caso base)

K[i][w] = K[i-1][w]                                          si peso_i > w
K[i][w] = max( K[i-1][w] ,  valor_i + K[i-1][w - peso_i] )   si peso_i <= w
```

Cada término significa:

- `K[i-1][w]`: **no subir** el lote `i`. La capacidad sigue igual y la decisión pasa a los lotes anteriores.
- `valor_i + K[i-1][w - peso_i]`: **subir** el lote `i`. Ganamos su valor completo, gastamos su peso, y con los kilos que sobran buscamos lo mejor entre los lotes anteriores. Se usa la fila `i − 1` para que el mismo lote no pueda subir dos veces.
- `max(...)`: nos quedamos con la mejor de las dos opciones. Si el lote no cabe, solo existe la primera.
- **Caso base:** sin lotes no se carga nada, así que la fila 0 es toda de ceros. Con `w = 0` tampoco cabe nada, así que la columna 0 también queda en ceros.
- **Orden de llenado:** cada casilla solo depende de la fila de arriba. Por eso la tabla se llena **fila por fila, de arriba hacia abajo**, y dentro de cada fila el orden de las columnas no importa.
- **Reconstrucción:** partimos de `K[n][W]` y subimos una fila a la vez. Si `K[i][w] ≠ K[i-1][w]`, el lote `i` cambió el resultado y por lo tanto subió, así que restamos su peso a `w`. Si son iguales, no subió.

### 2.4 Ejemplo resuelto a mano

Es un vehículo de juguete de **10 kg** con **5 lotes**. Los días para vencer solo los usa la regla actual. Este mismo ejemplo es el contraejemplo de la sección 5.1.

| Lote | Peso (kg) | Valor nutricional | Días para vencer | Valor por kg |
|---|---|---|---|---|
| L0 | 6 | 15 | 3 | 2,50 |
| L1 | 5 | 11 | 1 | 2,20 |
| L2 | 5 | 12 | 4 | 2,40 |
| L3 | 3 | 5 | 2 | 1,67 |
| L4 | 2 | 3 | 5 | 1,50 |

Tabla `K[i][w]` completa (fila `i` = ya se decidió sobre los lotes L0 a L(i−1)):

| i \ w | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 (ninguno) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 (+L0) | 0 | 0 | 0 | 0 | 0 | 0 | 15 | 15 | 15 | 15 | 15 |
| 2 (+L1) | 0 | 0 | 0 | 0 | 0 | 11 | 15 | 15 | 15 | 15 | 15 |
| 3 (+L2) | 0 | 0 | 0 | 0 | 0 | 12 | 15 | 15 | 15 | 15 | **23** |
| 4 (+L3) | 0 | 0 | 0 | 5 | 5 | 12 | 15 | 15 | 17 | 20 | 23 |
| 5 (+L4) | 0 | 0 | 3 | 5 | 5 | 12 | 15 | 15 | 18 | 20 | **23** |

Cómo salió cada fila:

- **Fila 1 (L0: 6 kg, valor 15).** Con menos de 6 kg, L0 no cabe y la casilla vale 0. Desde 6 kg cabe: `15 + K[0][w−6] = 15`.
- **Fila 2 (L1: 5 kg, valor 11).** En `w = 5`: no subir da 0 y subir da `11 + K[1][0] = 11`, así que gana 11. De 6 a 10 kg: no subir da 15 (L0), y subir da `11 + K[1][w−5]`, que como mucho es `11 + 0 = 11` porque con 5 kg o menos L0 no cabe. Gana 15. L0 y L1 juntos pesan 11 kg y no caben.
- **Fila 3 (L2: 5 kg, valor 12).**

| w | No subir L2: `K[2][w]` | Subir L2: `12 + K[2][w−5]` | `K[3][w]` |
|---|---|---|---|
| 0–4 | 0 | no cabe | 0 |
| 5 | 11 | 12 + 0 = 12 | 12 |
| 6–9 | 15 | 12 + 0 = 12 | 15 |
| 10 | 15 | 12 + `K[2][5]` = 12 + 11 = **23** | **23** |

- **Fila 4 (L3: 3 kg, valor 5).** En `w = 8`: no subir da 15 y subir da `5 + K[3][5] = 17`, así que gana 17 (L2 + L3). En `w = 9`: `5 + K[3][6] = 20` (L0 + L3) le gana a 15. En `w = 10`: subir da `5 + K[3][7] = 20` y no subir da 23, así que se queda 23.
- **Fila 5 (L4: 2 kg, valor 3).** En `w = 8`: `3 + K[4][6] = 18` le gana a 17. En `w = 10`: subir da `3 + K[4][8] = 20` y no subir da 23, así que se queda 23.

**Reconstrucción** desde `K[5][10] = 23`:

| Fila | w | Comparación | ¿Sube? | Capacidad que queda |
|---|---|---|---|---|
| 5 (L4) | 10 | `K[5][10] = 23` = `K[4][10] = 23` | No | 10 |
| 4 (L3) | 10 | `K[4][10] = 23` = `K[3][10] = 23` | No | 10 |
| 3 (L2) | 10 | `K[3][10] = 23` ≠ `K[2][10] = 15` | **Sí** | 10 − 5 = 5 |
| 2 (L1) | 5 | `K[2][5] = 11` ≠ `K[1][5] = 0` | **Sí** | 5 − 5 = 0 |
| 1 (L0) | 0 | `K[1][0] = 0` = `K[0][0] = 0` | No | 0 |

**Resultado óptimo:** suben **L1 y L2**, con 10 kg (el vehículo sale lleno) y valor **23**. La prueba `probar_ejemplo_a_mano` de [`pruebas.py`](src/cargue_vehiculos/pruebas.py) verifica esta tabla casilla por casilla.

### 2.5 Las reglas contra las que se compara

- **Regla actual (por vencimiento).** Ordena los lotes por días para vencer, de menor a mayor, los va subiendo y se detiene en el primero que no cabe (ver los supuestos en 1.3). Es la línea base del proceso actual.
- **Voraz por densidad.** Ordena por valor por kilogramo, de mayor a menor, y sube cada lote que quepa, saltando los que no. Es la regla "tentadora" que el caso pide incluir como segundo contraste.

Las dos ordenan una sola vez y nunca deshacen una elección. Eso las hace rápidas, Θ(n log n), pero ninguna garantiza el óptimo (sección 5.1).

### 2.6 Operación de la segunda parte del proyecto

Pendiente para la entrega del 23 de noviembre.

---

## 3. Implementación

### 3.1 Operación 3: código

El código está en [`src/cargue_vehiculos/`](src/cargue_vehiculos/):

| Archivo | Qué contiene |
|---|---|
| [`estrategia.py`](src/cargue_vehiculos/estrategia.py) | `cargar_vehiculo`: mochila 0/1 por programación dinámica (`llenar_tabla`) y reconstrucción de los lotes (`reconstruir_lotes`). |
| [`exhaustivo.py`](src/cargue_vehiculos/exhaustivo.py) | `cargar_exhaustivo`: prueba los 2ⁿ subconjuntos. Es la solución exacta con la que verificamos. |
| [`regla_actual.py`](src/cargue_vehiculos/regla_actual.py) | `cargar_por_vencimiento` (procedimiento actual) y `cargar_por_densidad` (voraz por valor por kg). |
| [`pruebas.py`](src/cargue_vehiculos/pruebas.py) | Pruebas con `assert`: casos límite, ejemplo a mano, contraejemplo, restricción del negocio y 200 instancias aleatorias. |
| [`datos.py`](src/cargue_vehiculos/datos.py) | Generador de lotes sintéticos con semilla fija. |
| [`medicion.py`](src/cargue_vehiculos/medicion.py) | Experimentos, gráficas y resumen de la extrapolación. |

**Decisiones de implementación:**

- **Todo escrito a mano.** No usamos bibliotecas de optimización ni de mochila. En la solución exhaustiva usamos `itertools.product` solo para enumerar los subconjuntos (las "filas de interruptores"). Revisar el peso de cada uno y quedarse con el mejor lo hace nuestro código.
- **Una fila por lote.** La fila `i` de la tabla corresponde a `lotes[i - 1]`, porque la fila 0 es el caso base. Cada fila nueva empieza como copia de la anterior (la opción "no subir") y después solo se recorren las columnas `w ≥ peso`, donde el lote cabe. El resultado es el mismo que con la recurrencia escrita casilla por casilla, pero ahorramos los `if` de las columnas donde el lote no cabe.
- **Se guarda la tabla completa.** Con una sola fila se podría calcular el valor, pero se perdería la información para saber qué lotes subieron. Como el caso necesita la lista de lotes, guardamos las `n + 1` filas.
- **Índices en orden creciente.** Las cuatro funciones devuelven los índices ordenados, así es fácil compararlos.
- **Entradas triviales.** Si la capacidad es 0 o no hay lotes, `cargar_vehiculo` devuelve `(0, [])` sin construir la tabla.
- **Contadores de operaciones propios.** Cada módulo tiene un contador con `reiniciar_operaciones()` y `leer_operaciones()`. La programación dinámica cuenta **celdas calculadas**: suma `W + 1` por cada fila, que es exactamente una por casilla. La exhaustiva cuenta **lotes revisados**: `n` por cada subconjunto. Las reglas cuentan **comparaciones del ordenamiento más lotes revisados**. Para eso el ordenamiento usa un comparador propio (`functools.cmp_to_key`) que incrementa el contador.
- **Estilo.** Todo el código sigue PEP 8 (revisado con `flake8`), tiene *type hints* y lleva un docstring estilo Google en cada función.

### 3.2 Segunda operación del proyecto

Pendiente para la entrega del 23 de noviembre.

---

## 4. Evaluación del desempeño

### 4.1 Complejidad de la operación 3

| Solución | Tiempo | Espacio | Por qué |
|---|---|---|---|
| Programación dinámica | **Θ(n·W)** | Θ(n·W) | La tabla tiene `(n + 1)·(W + 1)` casillas y cada una se calcula en tiempo constante (una suma y una comparación). Guardamos la tabla completa para reconstruir. La reconstrucción agrega Θ(n). |
| Exhaustiva | **Θ(n·2ⁿ)** | Θ(n) | Hay 2ⁿ subconjuntos y para cada uno se suman hasta `n` pesos y valores. Solo guarda el mejor subconjunto. |
| Regla actual (vencimiento) | Θ(n log n) | Θ(n) | Ordenar domina; el recorrido es Θ(n) (y puede parar antes). |
| Voraz por densidad | Θ(n log n) | Θ(n) | Ordenar domina; el recorrido es Θ(n). |

**La trampa de Θ(n·W).** Parece un costo polinomial, pero `W` no es un número de datos, es un **valor**: los kilos de capacidad. Si la capacidad se duplica, la tabla tiene el doble de columnas y el tiempo se duplica, aunque los lotes sean los mismos. Por eso este algoritmo se llama **pseudo-polinomial**. En el caso real, `W ≤ 4.000` kg y `n ≤ 600`, así que la tabla tiene como mucho unos 2,4 millones de casillas por vehículo. Si la capacidad se expresara en gramos (`W = 4.000.000`), la misma tabla sería mil veces más grande, aunque el problema fuera el mismo. Lo comprobamos midiendo con `n` fijo y `W` creciente (sección 4.4).

**Contraste.** Con `n = 300` lotes, la programación dinámica hace como mucho 301 × 4.001 ≈ 1,2 millones de pasos. La exhaustiva tendría que hacer 300 × 2³⁰⁰ ≈ 6 × 10⁹² pasos. La exhaustiva solo gana cuando `n` es muy pequeño: con `W = 1.000` kg, las dos curvas se cruzan cerca de `n = 10` (gráfica de operaciones de la sección 4.4).

### 4.2 Verificación

El script [`pruebas.py`](src/cargue_vehiculos/pruebas.py) usa solo `assert` y se detiene en la primera falla, mostrando la instancia que falló. Cubre:

1. **Casos límite**, para las cuatro soluciones: sin lotes; un solo lote que cabe; un solo lote que no cabe; ningún lote cabe; capacidad 0; todos los lotes caben; un lote que llena exactamente la capacidad.
2. **El ejemplo resuelto a mano** (sección 2.4). La tabla `K` que calcula el programa es igual, casilla por casilla, a la que calculamos en papel, y el resultado es valor 23 con los lotes L1 y L2.
3. **El contraejemplo** (sección 5.1): por vencimiento da 16, por densidad da 20 y el óptimo es 23.
4. **El comportamiento de la regla actual**: se detiene en el primer lote que no cabe. La regla por densidad, en cambio, salta ese lote y sigue.
5. **200 instancias aleatorias pequeñas** (de 0 a 10 lotes, pesos de 1 a 8 kg, capacidad de 0 a 25 kg, semilla fija 2026). En todas, la programación dinámica obtiene el mismo valor óptimo que la exhaustiva.
6. **La restricción del negocio**, en esas 200 instancias y para las cuatro soluciones: los índices existen y no se repiten (ningún lote sube dos veces ni a medias), el peso total no supera la capacidad, el valor informado es la suma de los valores **completos** de los lotes cargados, y ninguna regla supera el óptimo.

Salida de `python src/cargue_vehiculos/pruebas.py`:

```
Casos límite: OK
Ejemplo resuelto a mano (valor 23, lotes L1 y L2): OK
Contraejemplo: vencimiento 16, densidad 20, óptimo 23: OK
La regla actual se detiene en el primer lote que no cabe: OK
200 instancias aleatorias: la programación dinámica coincide con la exhaustiva y ninguna carga supera la capacidad: OK
Todas las pruebas pasaron.
```

Además, `medicion.py` vuelve a verificar dentro de cada experimento que la programación dinámica y la exhaustiva den el mismo valor en todos los tamaños donde corren las dos (hasta 20 lotes).

### 4.3 Cómo medimos

- **Datos:** [`datos.py`](src/cargue_vehiculos/datos.py) genera lotes con semilla fija (base `2026`). En cada tamaño se generan 3 instancias distintas y **las mismas instancias** se usan para todas las soluciones.
- **Cronómetro:** [`medicion.py`](src/cargue_vehiculos/medicion.py) usa `time.perf_counter()` solo alrededor de la llamada a cada solución. La generación de datos queda por fuera. Antes de cada medición se llama a `gc.collect()` para que el recolector de basura no caiga en medio.
- **Repeticiones:** cada instancia se ejecuta 5 veces (la exhaustiva, 1 vez) y se reporta el promedio de todas las ejecuciones.
- **Experimento 1, n pequeño:** n = 4, 6, 8, 10, 12, 14, 16, 18, 20 lotes, con W = 1.000 kg fijo. Corren las cuatro soluciones. Las parejas de duplicación son 4→8, 6→12, 8→16 y 10→20.
- **Experimento 2, n grande:** n = 50, 100, 200, 300, 400, 600, 800, 1.200 lotes, con W = 4.000 kg fijo (la capacidad máxima del caso). La exhaustiva ya no corre. Las parejas de duplicación van de 50→100 a 600→1.200.
- **Experimento 3, W creciente:** n = 300 lotes fijos y W = 500, 1.000, 2.000, 4.000, 8.000, 16.000 kg, solo para la programación dinámica.
- **Un día con el volumen real:** con `generar_flota` se arman 14 vehículos (capacidad entre 2.500 y 4.000 kg, entre 300 y 600 lotes cada uno) y se ejecutan las soluciones polinomiales. Este día sirve para comprobar la extrapolación.
- **Computador:** portátil con Intel Core i5-12450H (8 núcleos), Windows 11, Python 3.12. El experimento completo tarda unos 4 minutos.
- Las mediciones crudas quedan en [`mediciones.csv`](graficas/cargue_vehiculos/mediciones.csv) y las tablas calculadas en [`resumen.md`](graficas/cargue_vehiculos/resumen.md).

### 4.4 Gráficas

![Tiempo medio frente al número de lotes](graficas/cargue_vehiculos/tiempo_vs_n.png)

*Izquierda:* con eje y logarítmico, la exhaustiva es una recta empinada, que es la forma de una exponencial. La programación dinámica crece despacio y la supera desde unos 10 lotes. *Derecha:* con n grande y ejes lineales, la programación dinámica sigue aproximadamente una recta (lineal en n con W fijo); el quiebre alrededor de 800 lotes es ruido del portátil (cambios de frecuencia del procesador y procesos en segundo plano). Las dos reglas quedan casi pegadas al cero (por debajo de 7 ms incluso con 1.200 lotes) y una tapa a la otra.

![Operaciones elementales frente al número de lotes](graficas/cargue_vehiculos/operaciones_vs_n.png)

El conteo de operaciones tiene la misma forma que el tiempo, pero sin ruido. La exhaustiva sube exactamente como n·2ⁿ y la programación dinámica como n·(W + 1).

![Tiempo de la programación dinámica frente a la capacidad](graficas/cargue_vehiculos/tiempo_vs_capacidad.png)

Con los mismos 300 lotes, el tiempo crece en línea recta con la capacidad W: de 500 a 16.000 kg pasa de unos 9 ms a unos 1.150 ms. El costo depende de W y no solo del número de lotes.

### 4.5 Lo medido contra lo esperado

Factor por el que se multiplica cada medida al duplicar el tamaño (tomado de [`resumen.md`](graficas/cargue_vehiculos/resumen.md)):

| Solución | Duplicación | Tiempo × | Operaciones × | Esperado por la complejidad |
|---|---|---|---|---|
| Programación dinámica (W fijo) | n: 300 → 600 | 1,99 | 2,00 | 2 (lineal en n) |
| Programación dinámica (W fijo) | n: 600 → 1.200 | 1,66 | 2,00 | 2 |
| Programación dinámica (n fijo) | W: 4.000 → 8.000 | 2,96 | 2,00 | 2 (lineal en W) |
| Programación dinámica (n fijo) | W: 8.000 → 16.000 | 2,49 | 2,00 | 2 |
| Exhaustiva | n: 8 → 16 | 361 | 512 | 2·2⁸ = 512 |
| Exhaustiva | n: 10 → 20 | 1.720 | 2.048 | 2·2¹⁰ = 2.048 |
| Regla actual (vencimiento) | n: 300 → 600 | 2,19 | 2,19 | 2·log₂600 / log₂300 ≈ 2,24 |
| Voraz por densidad | n: 300 → 600 | 2,46 | 2,24 | ≈ 2,24 |

Lo que se lee en la tabla:

- **Las operaciones coinciden exactamente con la teoría.** La programación dinámica cuenta celdas, y al duplicar n o W se duplican las celdas (factor 2,00). La exhaustiva revisa `n·2ⁿ` lotes, y al pasar de 10 a 20 el conteo se multiplica por 2.048, igual que la fórmula.
- **El tiempo de la programación dinámica sigue al conteo.** Da factores entre 1,66 y 2,96, alrededor del 2 esperado. La diferencia es ruido del sistema operativo, de los cambios de frecuencia del procesador del portátil y del manejo de memoria de Python, que pesa más cuando las tablas son grandes.
- **El tiempo de la exhaustiva crece menos que su conteo en n pequeño** (361 en vez de 512, y 1.720 en vez de 2.048). Con pocos lotes, una buena parte del tiempo es costo fijo: llamar la función, crear el generador de `product`, etc. Ese costo no se multiplica por 2ⁿ. A medida que n crece, el factor se acerca al teórico (de 4→8 da 15,9 de 32 esperado, y de 10→20 ya da 1.720 de 2.048).
- **En n pequeño (experimento 1), los tiempos de la programación dinámica y de las reglas son de décimas de milisegundo**, y sus factores (entre 1,2 y 5,8) son sobre todo ruido. Por eso, para la programación dinámica y las reglas nos apoyamos en el experimento 2.
- **Las reglas** crecen como n log n. El factor esperado es un poco más que 2 (≈ 2,24), y medimos 2,19 y 2,46.

### 4.6 Escala real y ventana operativa

**Volumen real (peor caso de un día):** 14 vehículos, cada uno con 600 lotes y W = 4.000 kg.

**Cómo extrapolamos.** No usamos una regla de tres sobre un solo punto. Primero confirmamos en las gráficas la forma de cada curva y después ajustamos una constante a esa forma:

- **Programación dinámica:** las gráficas muestran que el tiempo es lineal en n (con W fijo) y lineal en W (con n fijo). Por eso usamos `t ≈ c · n · (W + 1)`. Promediando los puntos de los experimentos 2 y 3 con n ≥ 100, sale `c ≈ 186,7 ns por celda`. Peor día: 14 × 600 × 4.001 ≈ 33,6 millones de celdas, es decir, **≈ 6,3 s**.
- **Reglas:** `t ≈ c · n log₂ n`, con `c ≈ 558 ns` (vencimiento) y `c ≈ 768 ns` (densidad). Peor día: **≈ 43 ms** y **≈ 60 ms**.
- **Exhaustiva:** `t ≈ c · n · 2ⁿ`, con `c ≈ 215 ns`, ajustada en n = 14 a 20, donde el costo fijo ya pesa poco. Incluso en su caso más favorable (300 lotes por ruta), da 14 × 215 ns × 300 × 2³⁰⁰ ≈ **5,8 × 10⁷⁹ años**, unas 4 × 10⁶⁹ veces la edad del universo (13.800 millones de años). **La exhaustiva sencillamente no terminaría.** Con la misma constante, en toda la ventana de 2 horas solo alcanzaría a resolver una ruta de unos **30 lotes**.

**Comprobación de la extrapolación.** Ejecutamos un día sintético completo, con 14 vehículos y 6.193 lotes en total (unos 20 millones de celdas). La programación dinámica tardó **2,67 s medidos**. El modelo predice 20 millones × 186,7 ns ≈ 3,7 s. Lo medido queda por debajo de lo predicho porque la constante se ajustó con puntos sueltos en los que el portátil tuvo más variación de velocidad; aun así, el orden de magnitud coincide y la extrapolación queda del lado conservador (sobrestima el tiempo, no lo subestima).

| Solución | Tiempo por día (peor caso) | Fracción de la ventana de 2 h | ¿Cabe? |
|---|---|---|---|
| Programación dinámica | ≈ 6,3 s | ≈ 0,09 % | Sí, con mucha holgura |
| Regla actual (vencimiento) | ≈ 43 ms | ≈ 0,0006 % | Sí |
| Voraz por densidad | ≈ 60 ms | ≈ 0,0008 % | Sí |
| Exhaustiva | ≈ 5,8 × 10⁷⁹ años | — | No: no termina |

La ventana de 2 horas la comparten las operaciones 1 a 3. Aun así, la programación dinámica usa unos 6 segundos de 7.200, lo que deja casi toda la ventana para las otras dos operaciones.

*Todos estos tiempos son estimaciones, medidas en un solo computador con datos sintéticos. En el computador del banco la constante puede ser distinta, pero la forma de las curvas no cambia.*

### 4.7 Evaluación de la segunda operación y del proceso completo

Pendiente para la entrega del 23 de noviembre.

---

## 5. Análisis comparativo

### 5.1 Contraejemplo: por qué fallan la regla actual y la regla por densidad

**Instancia:** el ejemplo de la sección 2.4, un vehículo de 10 kg con los lotes L0 (6 kg, 15, vence en 3 días), L1 (5 kg, 11, 1 día), L2 (5 kg, 12, 4 días), L3 (3 kg, 5, 2 días) y L4 (2 kg, 3, 5 días).

| Regla | Qué hace, paso a paso | Lotes | Peso | Valor |
|---|---|---|---|---|
| **Por vencimiento (actual)** | El orden es L1 (1 día), L3 (2), L0 (3), L2 (4), L4 (5). Sube L1 (5 kg) y L3 (8 kg). L0 pesaría 14 kg y no cabe, así que **se detiene**. | L1, L3 | 8 kg (80 %) | **16** |
| **Por densidad** | El orden es L0 (2,50/kg), L2 (2,40), L1 (2,20), L3 (1,67), L4 (1,50). Sube L0 (6 kg). L2 y L1 no caben (11 kg), así que los salta. Sube L3 (9 kg). L4 no cabe (11 kg). | L0, L3 | 9 kg (90 %) | **20** |
| **Óptimo (programación dinámica)** | Tabla de la sección 2.4. | L1, L2 | 10 kg (100 %) | **23** |

**Diferencia:** la regla actual pierde **7 unidades de valor (30 % del óptimo)** y deja 2 kg vacíos. La regla por densidad pierde **3 unidades (13 %)**.

**Por qué fallan.** La regla actual no tiene en cuenta el valor ni el peso, solo la fecha. Además se detiene en el primer lote que no cabe, aunque detrás haya lotes que sí cabrían. Esto concuerda con que en la realidad los vehículos salgan, en promedio, al 78 % de su capacidad. La regla por densidad sí mira el valor por kilo, pero escoge L0 porque es "el más eficiente", y L0 deja 4 kg libres que ningún lote llena bien. Nunca considera que dos lotes de 5 kg, cada uno un poco menos eficiente, llenan el vehículo exacto. Ninguna de las dos reconsidera lo que ya eligió.

**No es un caso raro.** En 1.000 instancias pequeñas aleatorias (generadas por `medicion.py`, semilla fija):

- la regla por vencimiento no llega al óptimo en **537 de 1.000**. En el peor caso pierde el 100 %: si el primer lote por vencer no cabe, el vehículo sale vacío;
- la regla por densidad no llega al óptimo en **127 de 1.000**, y en el peor caso pierde el **50 %**.

Una instancia donde una regla acierta no prueba nada. Basta una donde falla para saber que no garantiza el máximo que exige el caso.

### 5.2 Condición contraria: cuándo bastaría una estrategia voraz

La programación dinámica es necesaria porque **los lotes no se fraccionan** y porque **sus pesos son distintos**. Si cambiara alguna de estas condiciones, una regla voraz sería la adecuada:

- **Si los lotes se pudieran partir** (por ejemplo, granos a granel, de los que se puede subir solo una parte y obtener la parte proporcional de su valor), el problema sería una **mochila fraccionaria**. Ahí cargar por densidad y partir el último lote **sí** da el óptimo, en Θ(n log n). Nunca queda un hueco, porque siempre se completa con un pedazo del siguiente lote más eficiente. En el contraejemplo se podrían subir L0 (6 kg) y 4 kg de L2 (4 × 2,40 = 9,6), para un valor de 24,6.
- **Si todos los lotes pesaran lo mismo** (por ejemplo, estibas estandarizadas de igual peso), en el vehículo cabría un número fijo de lotes `k = ⌊W / peso⌋`. Subir los `k` de mayor valor sería óptimo, y una regla voraz por valor bastaría.

Que el problema permita o no fraccionar es lo que decide qué familia de estrategias sirve.

### 5.3 Recomendación para la operación 3

**Recomendamos adoptar la programación dinámica (mochila 0/1) para planear el cargue de cada vehículo.**

**Qué gana el banco frente a hoy:**

- **El máximo valor nutricional por viaje, garantizado.** No es una aproximación, que es lo que exige el caso. En el día sintético de 14 vehículos, la programación dinámica cargó **637.554** unidades de valor, contra **270.154** de la regla por vencimiento (42,4 % del óptimo). Este contraste tan grande depende de nuestras categorías sintéticas, porque las de mayor prioridad no son las que vencen primero. Con los datos reales del banco la cifra será otra, pero la dirección no cambia: la regla actual no tiene en cuenta el valor.
- **Vehículos más llenos.** En el día sintético, la programación dinámica llenó en promedio el **100 %** de la capacidad, frente al **94,2 %** de la regla actual. En los datos del cliente la regla actual llega al 78 %. La diferencia sugiere que los lotes reales son más pesados o más variados que los nuestros, y en ese caso la ganancia sería aún mayor.
- **Cabe de sobra en la ventana:** unos 6 segundos por día, en el peor caso, de una ventana de 2 horas.

**Por qué no la regla por densidad, si llegó al 99,8 %.** Es muy rápida y en datos realistas se acerca mucho al óptimo. Pero no lo garantiza: falla en el 13 % de las instancias pequeñas y puede perder hasta la mitad del valor. El caso pide el máximo exacto, y el costo de la programación dinámica (unos segundos al día) es despreciable.

**Riesgos y límites que el banco debe conocer:**

1. **El costo depende de la capacidad (pseudo-polinomial).** Si los pesos se registraran en gramos en vez de kilogramos, la tabla sería 1.000 veces más grande: unas 1 hora y 45 minutos por día (casi toda la ventana) y unos 25 GB de memoria por vehículo, más de lo que tiene un computador común. Hay que mantener los pesos en kilogramos enteros. Si llegaran vehículos más grandes (por ejemplo, de 8.000 kg), el tiempo solo se duplicaría (~13 s), lo cual sigue siendo manejable.
2. **Memoria.** La tabla del vehículo más grande (600 lotes, 4.000 kg) tiene unos 2,4 millones de casillas. Medimos con `tracemalloc` que ocupa unos 25 MB en Python. Se libera al terminar cada vehículo, así que el uso no se acumula entre los 14.
3. **La programación dinámica no mira el vencimiento.** Maximiza el valor nutricional y podría dejar en bodega lotes a punto de vencer, lo que se convertiría en desperdicio. Para mitigarlo hay dos opciones: (a) subir el valor de los lotes que vencen pronto, para que la prioridad ya lo incluya; o (b) cargar primero los lotes que vencen en 24 horas y resolver la mochila con la capacidad restante. Esta decisión le corresponde al banco y se discutirá en las implicaciones del informe final.
4. **Crecimiento.** Si la flota creciera, el tiempo crecería en proporción al número de vehículos. Si crecieran los lotes por ruta, crecería en proporción a n. Si crecieran las capacidades, en proporción a W. Duplicar cualquiera de los tres duplica el tiempo, y aun así cabe con holgura.

### 5.4 Comparación entre las estrategias de las dos operaciones y solución recomendada

Pendiente para la entrega del 23 de noviembre.

---

## 6. Implicaciones éticas, sociales y ambientales

### 6.1 Consumo energético de la operación 3

Usamos `kWh = kW × h`, con la potencia del computador del caso (150 W = 0,150 kW) y el tiempo extrapolado del peor caso diario (sección 4.6). La planeación se hace una vez al día, 365 días al año.

| Solución | Tiempo por día | Energía por día | Energía por año |
|---|---|---|---|
| Programación dinámica | ≈ 6,3 s = 1,74 × 10⁻³ h | 0,150 × 1,74 × 10⁻³ ≈ **2,6 × 10⁻⁴ kWh** (0,26 Wh) | ≈ **0,095 kWh** (95 Wh) |
| Regla actual (vencimiento) | ≈ 43 ms = 1,2 × 10⁻⁵ h | ≈ **1,8 × 10⁻⁶ kWh** | ≈ **0,00066 kWh** (0,66 Wh) |
| Voraz por densidad | ≈ 60 ms | ≈ 2,5 × 10⁻⁶ kWh | ≈ 0,00091 kWh |
| Exhaustiva | ≈ 5,8 × 10⁷⁹ años | ≈ 8 × 10⁸² kWh | No aplica: no termina |

**Diferencia anual entre la programación dinámica y la regla actual:** ≈ 0,095 − 0,0007 ≈ **0,095 kWh al año (unos 95 Wh)**. Es más o menos lo que gasta un bombillo LED de 10 W en nueve horas y media.

Cómo leer estas cifras:

- **Son estimaciones.** Asumimos que el computador consume sus 150 W completos solo durante el cálculo. Como el computador está encendido toda la ventana para las tres operaciones, lo que calculamos es el consumo *adicional* atribuible a esta operación.
- **El costo energético de la estrategia óptima es despreciable.** Pasar de la regla actual a la programación dinámica cuesta unos 95 Wh al año. A cambio, cada vehículo sale lleno con el máximo valor nutricional. Si eso evita aunque sea un viaje extra de un camión en todo el año, el ahorro de combustible supera con creces esos 95 Wh. Este impacto lo cuantificaremos en el informe final.
- **La exhaustiva no es una opción ni energéticamente.** Su cifra no tiene sentido físico: el cálculo no terminaría nunca.

### 6.2 Preguntas de impacto, marco normativo y escenario de crecimiento

Pendiente para la entrega del 23 de noviembre.

---

## 7. Conclusiones

Pendiente para la entrega del 23 de noviembre.

---

## 8. Reproducción

Requisitos: Python 3.10 o superior.

```bash
# 1. Crear y activar el entorno virtual (desde la raíz del repositorio)
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows (PowerShell o CMD)

# 2. Instalar las dependencias
pip install -r requirements.txt

# 3. Ejecutar las pruebas (menos de un segundo)
python src/cargue_vehiculos/pruebas.py

# 4. Ejecutar la medición y regenerar las gráficas (alrededor de un minuto)
python src/cargue_vehiculos/medicion.py
```

La medición usa semillas fijas (`2026` y derivadas), así que genera siempre los mismos lotes. Los tiempos cambian un poco según el computador, pero la forma de las curvas y los conteos de operaciones son idénticos. Los resultados se guardan en `graficas/cargue_vehiculos/` (`tiempo_vs_n.png`, `operaciones_vs_n.png`, `tiempo_vs_capacidad.png`, `mediciones.csv` y `resumen.md`).
