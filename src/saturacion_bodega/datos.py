"""Generador de series horarias sintéticas de cambio neto del inventario.

Cada valor es el cambio neto de una hora de operación para una categoría,
en kilogramos: lo que entró menos lo que salió o se descartó (puede ser
negativo). Hay 12 horas de operación por día y 300 días al año, así que
diez años son unas 36.000 horas.

La serie tiene ruido alrededor de un promedio levemente negativo y, una
vez al año, una "temporada" de cosecha de 4 a 8 semanas en la que el
inventario tiende a crecer. Ese es el tipo de tramo que busca la
Dirección para dimensionar el cuarto frío.
"""

import random

HORAS_DIA = 12
DIAS_ANIO = 300
HORAS_ANIO = HORAS_DIA * DIAS_ANIO  # 3.600
CATEGORIAS = 40


def generar_serie(n: int, semilla: int) -> list[int]:
    """Genera ``n`` horas de cambio neto del inventario de una categoría.

    Args:
        n: número de horas.
        semilla: semilla fija.

    Returns:
        Lista de enteros (kg por hora).
    """
    rng = random.Random(semilla)
    duracion = rng.randint(4, 8) * 6 * HORAS_DIA  # entre 4 y 8 semanas
    inicio_temporada = rng.randrange(HORAS_ANIO - duracion)
    serie: list[int] = []
    for hora in range(n):
        en_anio = hora % HORAS_ANIO
        tendencia = -6.0
        if inicio_temporada <= en_anio < inicio_temporada + duracion:
            tendencia = 20.0
        serie.append(round(rng.gauss(tendencia, 25)))
    return serie


def serie_pequena(n: int, rng: random.Random) -> list[int]:
    """Genera una serie corta con valores pequeños para las pruebas.

    Args:
        n: longitud.
        rng: generador con semilla fija.

    Returns:
        Lista de enteros entre -20 y 20.
    """
    return [rng.randint(-20, 20) for _ in range(n)]
