"""Consulta de inventario como se hace hoy: recorriendo toda la lista.

Es la línea base de la operación 1. Las dos consultas recorren los ``n``
lotes del inventario: Θ(n) por consulta.
"""

from datos import Lote

_contador = {"operaciones": 0}


def reiniciar_operaciones() -> None:
    """Pone en cero el contador de operaciones del módulo."""
    _contador["operaciones"] = 0


def leer_operaciones() -> int:
    """Devuelve las operaciones contadas desde el último reinicio.

    Returns:
        El número de lotes revisados (comparaciones).
    """
    return _contador["operaciones"]


def buscar_lineal(inventario: list[Lote], codigo: str) -> Lote | None:
    """Busca un lote por su código recorriendo la lista desde el inicio.

    Args:
        inventario: lotes en el orden en que están guardados.
        codigo: código del lote buscado.

    Returns:
        El lote con ese código, o None si no existe.
    """
    for lote in inventario:
        _contador["operaciones"] += 1
        if lote.codigo == codigo:
            return lote
    return None


def por_vencer_lineal(
    inventario: list[Lote], desde: int, hasta: int
) -> list[Lote]:
    """Devuelve los lotes que vencen entre dos días, revisando todos.

    Args:
        inventario: lotes en el orden en que están guardados.
        desde: primer día del rango (incluido).
        hasta: último día del rango (incluido).

    Returns:
        Los lotes del rango, en el orden en que aparecen en el inventario.
    """
    resultado: list[Lote] = []
    for lote in inventario:
        _contador["operaciones"] += 1
        if desde <= lote.vencimiento <= hasta:
            resultado.append(lote)
    return resultado
