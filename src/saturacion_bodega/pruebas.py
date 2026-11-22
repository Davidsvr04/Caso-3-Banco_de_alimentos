"""Pruebas con assert del tramo de mayor crecimiento del inventario.

Se ejecuta desde la raíz del repositorio con:

    python src/saturacion_bodega/pruebas.py
"""

import random

from actual import tramo_fuerza_bruta
from datos import serie_pequena
from estrategias import (tramo_acumulado, tramo_dividir_y_vencer,
                         tramo_kadane)

ESTRATEGIAS = [tramo_fuerza_bruta, tramo_acumulado, tramo_dividir_y_vencer,
               tramo_kadane]

# Ejemplo resuelto a mano en el informe: 8 horas de una categoría.
EJEMPLO = [3, -5, 4, -1, 6, -8, 2, 1]


def tramo_valido(serie: list[int], tramo: tuple[int, int, int]) -> bool:
    """Revisa que la suma informada sea la suma real del tramo.

    Args:
        serie: la serie.
        tramo: (suma, inicio, fin).

    Returns:
        True si el tramo existe dentro de la serie y suma lo que dice.
    """
    suma, inicio, fin = tramo
    if not serie:
        return tramo == (0, 0, -1)
    return (0 <= inicio <= fin < len(serie)
            and sum(serie[inicio:fin + 1]) == suma)


def probar_casos_limite() -> None:
    """Serie vacía, una hora, todo negativo, todo positivo y ceros."""
    for estrategia in ESTRATEGIAS:
        nombre = estrategia.__name__
        assert estrategia([]) == (0, 0, -1), nombre
        assert estrategia([7]) == (7, 0, 0), nombre
        assert estrategia([-4]) == (-4, 0, 0), nombre
        # Todo negativo: la hora menos negativa.
        assert estrategia([-8, -3, -6])[0] == -3, nombre
        # Todo positivo: la serie completa.
        assert estrategia([2, 5, 1, 4]) == (12, 0, 3), nombre
        assert estrategia([0, 0, 0])[0] == 0, nombre


def probar_ejemplo_a_mano() -> None:
    """El ejemplo del informe: el mejor tramo son las horas 2 a 4 (9 kg)."""
    for estrategia in ESTRATEGIAS:
        assert estrategia(EJEMPLO) == (9, 2, 4), estrategia.__name__


def probar_aleatorias(cantidad: int = 300, semilla: int = 2026) -> None:
    """Todas las estrategias dan la misma suma que la fuerza bruta.

    Args:
        cantidad: número de series aleatorias.
        semilla: semilla fija.
    """
    rng = random.Random(semilla)
    for caso in range(cantidad):
        serie = serie_pequena(rng.randint(0, 40), rng)
        copia = list(serie)
        exacto = tramo_fuerza_bruta(serie)
        for estrategia in ESTRATEGIAS:
            tramo = estrategia(serie)
            assert tramo[0] == exacto[0], (caso, estrategia.__name__, serie)
            assert tramo_valido(serie, tramo), (caso, estrategia.__name__)
        assert serie == copia, caso  # la serie original no cambia


def main() -> None:
    """Ejecuta todas las pruebas."""
    probar_casos_limite()
    print("Casos límite: OK")
    probar_ejemplo_a_mano()
    print("Ejemplo resuelto a mano (9 kg, horas 2 a 4): OK")
    probar_aleatorias()
    print("300 series aleatorias: dividir y vencer y Kadane dan la misma "
          "suma máxima que la fuerza bruta, con un tramo válido: OK")
    print("Todas las pruebas pasaron.")


if __name__ == "__main__":
    main()
