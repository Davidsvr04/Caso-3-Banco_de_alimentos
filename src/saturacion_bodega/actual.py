"""Tramo de mayor crecimiento como se calcula hoy: todos los tramos.

El programa actual evalúa todos los tramos posibles [i, j] y, para cada
uno, vuelve a sumar sus horas. Hay unos n²/2 tramos y sumar cada uno
cuesta hasta n: Θ(n³).

Un tramo se representa como (suma, inicio, fin), con inicio y fin
incluidos. La serie vacía no tiene tramos: se devuelve (0, 0, -1).
"""

Tramo = tuple[int, int, int]  # (suma_kg, hora_inicio, hora_fin)

_contador = {"operaciones": 0}


def reiniciar_operaciones() -> None:
    """Pone en cero el contador de operaciones del módulo."""
    _contador["operaciones"] = 0


def leer_operaciones() -> int:
    """Devuelve las operaciones contadas desde el último reinicio.

    Returns:
        El número de sumas realizadas.
    """
    return _contador["operaciones"]


def tramo_fuerza_bruta(serie: list[int]) -> Tramo:
    """Evalúa todos los tramos, sumando cada uno desde cero.

    Si varios tramos empatan, se queda con el primero que encuentra (el
    que empieza antes y, entre esos, el más corto).

    Args:
        serie: cambio neto por hora, en kg.

    Returns:
        La tupla (suma, inicio, fin) del tramo de mayor suma.
    """
    n = len(serie)
    if n == 0:
        return (0, 0, -1)
    mejor: Tramo = (serie[0], 0, 0)
    sumas = 0
    for inicio in range(n):
        for fin in range(inicio, n):
            total = 0
            for hora in range(inicio, fin + 1):
                total += serie[hora]
            sumas += fin - inicio + 1
            if total > mejor[0]:
                mejor = (total, inicio, fin)
    _contador["operaciones"] += sumas
    return mejor
