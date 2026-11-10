"""Generador de instancias sintéticas para el cargue de los vehículos.

Todas las funciones reciben una semilla y usan su propio ``random.Random``,
de modo que la misma semilla produce siempre los mismos lotes. Así el
docente puede reproducir las pruebas y las mediciones.

Un lote es la tupla ``(peso_kg, valor_nutricional, dias_para_vencer)``:

* ``peso_kg``: entero mayor que 0.
* ``valor_nutricional``: raciones ponderadas por la prioridad de la
  categoría (entero mayor o igual que 0).
* ``dias_para_vencer``: entero mayor que 0; el que vence primero tiene el
  número más pequeño.
"""

import random

Lote = tuple[int, int, int]  # (peso_kg, valor_nutricional, dias_para_vencer)

# Categorías sintéticas del banco de alimentos:
# (nombre, raciones por kg, prioridad, días mínimos y máximos para vencer).
# Las cifras son supuestos del equipo para darle estructura a los datos;
# no son cifras del cliente.
CATEGORIAS: list[tuple[str, int, int, int, int]] = [
    ("proteina", 4, 3, 2, 10),
    ("lacteos", 5, 2, 3, 15),
    ("frutas_verduras", 3, 2, 1, 7),
    ("granos", 8, 1, 60, 180),
    ("enlatados", 3, 1, 90, 365),
]

PESO_MIN_KG = 20
PESO_MAX_KG = 500
CAPACIDAD_MIN_KG = 2500
CAPACIDAD_MAX_KG = 4000
VEHICULOS = 14
LOTES_MIN_RUTA = 300
LOTES_MAX_RUTA = 600


def generar_lote(rng: random.Random) -> Lote:
    """Genera un lote con peso, valor y vencimiento según su categoría.

    El valor es peso × raciones por kg × prioridad, con una variación de
    ±20 % para que dos lotes de la misma categoría no tengan exactamente la
    misma densidad (valor por kilogramo).

    Args:
        rng: generador aleatorio con semilla fija.

    Returns:
        Un lote ``(peso_kg, valor_nutricional, dias_para_vencer)``.
    """
    _, raciones_kg, prioridad, dias_min, dias_max = rng.choice(CATEGORIAS)
    peso = rng.randint(PESO_MIN_KG, PESO_MAX_KG)
    variacion = rng.uniform(0.8, 1.2)
    valor = round(peso * raciones_kg * prioridad * variacion)
    dias = rng.randint(dias_min, dias_max)
    return (peso, valor, dias)


def generar_lotes(n: int, semilla: int) -> list[Lote]:
    """Genera los lotes candidatos de una ruta.

    Args:
        n: número de lotes candidatos.
        semilla: semilla fija del generador.

    Returns:
        Una lista con ``n`` lotes.
    """
    rng = random.Random(semilla)
    return [generar_lote(rng) for _ in range(n)]


def generar_flota(semilla: int) -> list[tuple[list[Lote], int]]:
    """Genera un día de operación con el volumen real del caso.

    Son 14 vehículos; cada uno con capacidad entre 2.500 y 4.000 kg y una
    ruta con entre 300 y 600 lotes candidatos.

    Args:
        semilla: semilla fija del generador.

    Returns:
        Una lista de parejas ``(lotes, capacidad_kg)``, una por vehículo.
    """
    rng = random.Random(semilla)
    flota: list[tuple[list[Lote], int]] = []
    for _ in range(VEHICULOS):
        capacidad = rng.randint(CAPACIDAD_MIN_KG, CAPACIDAD_MAX_KG)
        n = rng.randint(LOTES_MIN_RUTA, LOTES_MAX_RUTA)
        lotes = [generar_lote(rng) for _ in range(n)]
        flota.append((lotes, capacidad))
    return flota


def instancias_pequenas(
    cantidad: int, semilla: int, n_max: int = 10
) -> list[tuple[list[Lote], int]]:
    """Genera instancias pequeñas para comparar con la solución exhaustiva.

    Los pesos son de 1 a 8 kg y la capacidad de 0 a 25 kg, para que en
    muchas instancias no quepan todos los lotes y la elección importe.

    Args:
        cantidad: número de instancias.
        semilla: semilla fija del generador.
        n_max: número máximo de lotes por instancia.

    Returns:
        Una lista de parejas ``(lotes, capacidad_kg)``.
    """
    rng = random.Random(semilla)
    instancias: list[tuple[list[Lote], int]] = []
    for _ in range(cantidad):
        n = rng.randint(0, n_max)
        lotes: list[Lote] = []
        for _ in range(n):
            lotes.append((rng.randint(1, 8), rng.randint(1, 20),
                          rng.randint(1, 30)))
        capacidad = rng.randint(0, 25)
        instancias.append((lotes, capacidad))
    return instancias
