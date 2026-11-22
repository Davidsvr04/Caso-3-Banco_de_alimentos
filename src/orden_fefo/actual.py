"""Ordenamiento FEFO como se hace hoy: inserción sobre la lista completa.

Los lotes nuevos se anexan al final de la lista del día anterior (que ya
estaba ordenada) y se ordena todo por inserción. Los lotes viejos casi no
se mueven, pero cada lote nuevo, que suele vencer pronto, tiene que
desplazarse hasta cerca del principio: el costo es Θ(n·k), donde n es el
tamaño de la lista y k el número de lotes nuevos.
"""

from datos import Lote, clave_fefo

_contador = {"operaciones": 0}


def reiniciar_operaciones() -> None:
    """Pone en cero el contador de operaciones del módulo."""
    _contador["operaciones"] = 0


def leer_operaciones() -> int:
    """Devuelve las operaciones contadas desde el último reinicio.

    Returns:
        El número de comparaciones entre claves.
    """
    return _contador["operaciones"]


def ordenar_insercion(viejos: list[Lote], nuevos: list[Lote]) -> list[Lote]:
    """Anexa los nuevos al final y ordena todo por inserción.

    Args:
        viejos: lista del día anterior, ya en orden FEFO.
        nuevos: lotes nuevos del día, en orden de llegada.

    Returns:
        Una lista nueva en orden FEFO. Las listas recibidas no cambian.
    """
    lista = viejos + nuevos  # copia: el registro original no se toca
    comparaciones = 0
    for i in range(1, len(lista)):
        actual = lista[i]
        clave = clave_fefo(actual)
        j = i - 1
        while j >= 0:
            comparaciones += 1
            if clave_fefo(lista[j]) <= clave:
                break  # "<=" deja los empates en su orden: es estable
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    _contador["operaciones"] += comparaciones
    return lista
