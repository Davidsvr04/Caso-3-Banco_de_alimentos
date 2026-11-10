# Proyecto final — Caso 3: Banco de alimentos

**Integrantes**

- David Viloria
- Leonel Antonio
- Luis Lopera
- Juana Ospina

**Materia:** Análisis de Algoritmos

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

> _En construcción: esta parte la agrega el integrante 2._

### 2.5 Las reglas contra las que se compara

- **Regla actual (por vencimiento).** Ordena los lotes por días para vencer, de menor a mayor, los va subiendo y se detiene en el primero que no cabe (ver los supuestos en 1.3). Es la línea base del proceso actual.
- **Voraz por densidad.** Ordena por valor por kilogramo, de mayor a menor, y sube cada lote que quepa, saltando los que no. Es la regla "tentadora" que el caso pide incluir como segundo contraste.

Las dos ordenan una sola vez y nunca deshacen una elección. Eso las hace rápidas, Θ(n log n), pero ninguna garantiza el óptimo (sección 5.1).

### 2.6 Operación de la segunda parte del proyecto

Pendiente para la entrega del 23 de noviembre.

---

## 3. Implementación

### 3.1 Operación 3: código

> _En construcción: esta parte la agrega el integrante 2._

---

## 4. Evaluación del desempeño

### 4.1 Complejidad de la operación 3

> _En construcción: esta parte la agrega el integrante 2._

### 4.2 Verificación

> _En construcción: esta parte la agrega el integrante 3._

### 4.3 Cómo medimos

> _En construcción: esta parte la agrega el integrante 4._

### 4.7 Evaluación de la segunda operación y del proceso completo

Pendiente para la entrega del 23 de noviembre.

---

## 5. Análisis comparativo

### 5.1 Contraejemplo: por qué fallan la regla actual y la regla por densidad

> _En construcción: esta parte la agrega el integrante 3._

### 5.3 Recomendación para la operación 3

> _En construcción: esta parte la agrega el integrante 4._

### 5.4 Comparación entre las estrategias de las dos operaciones y solución recomendada

Pendiente para la entrega del 23 de noviembre.

---

## 6. Implicaciones éticas, sociales y ambientales

### 6.1 Consumo energético de la operación 3

> _En construcción: esta parte la agrega el integrante 4._

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
