"""Estrategias propuestas para el ordenamiento FEFO (operación 2).

* ``ordenar_mezcla_total``: ordenamiento por mezcla (dividir y vencer) de
  toda la lista. Θ(n log n) sin importar cómo llegue la lista.
* ``fusionar_nuevos``: aprovecha que la lista vieja ya está ordenada.
  Ordena por mezcla solo los k lotes nuevos y después fusiona las dos
  listas ordenadas en una sola pasada: Θ(k log k + n).
* ``despachables``: con la lista en orden FEFO, separa los lotes vencidos
  con una búsqueda binaria, para que ninguno se despache.

Todas las funciones devuelven listas nuevas: el registro original de los
lotes no se modifica.
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


def fusionar(izquierda: list[Lote], derecha: list[Lote]) -> list[Lote]:
    """Fusiona dos listas en orden FEFO en una sola, de forma estable.

    En un empate gana el lote de la izquierda, así que los lotes que ya
    estaban antes conservan su lugar relativo.

    Args:
        izquierda: lista ordenada.
        derecha: lista ordenada.

    Returns:
        Una lista nueva con todos los lotes, ordenada.
    """
    resultado: list[Lote] = []
    i = j = 0
    comparaciones = 0
    while i < len(izquierda) and j < len(derecha):
        comparaciones += 1
        if clave_fefo(derecha[j]) < clave_fefo(izquierda[i]):
            resultado.append(derecha[j])
            j += 1
        else:
            resultado.append(izquierda[i])
            i += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    _contador["operaciones"] += comparaciones
    return resultado


def ordenar_mezcla(lotes: list[Lote]) -> list[Lote]:
    """Ordenamiento por mezcla: divide, ordena cada mitad y fusiona.

    Args:
        lotes: lotes en cualquier orden.

    Returns:
        Una lista nueva en orden FEFO.
    """
    if len(lotes) <= 1:
        return list(lotes)
    mitad = len(lotes) // 2
    return fusionar(ordenar_mezcla(lotes[:mitad]),
                    ordenar_mezcla(lotes[mitad:]))


def ordenar_mezcla_total(
    viejos: list[Lote], nuevos: list[Lote]
) -> list[Lote]:
    """Anexa los nuevos y ordena toda la lista por mezcla.

    Args:
        viejos: lista del día anterior, en orden FEFO.
        nuevos: lotes nuevos del día.

    Returns:
        Una lista nueva en orden FEFO.
    """
    return ordenar_mezcla(viejos + nuevos)


def fusionar_nuevos(viejos: list[Lote], nuevos: list[Lote]) -> list[Lote]:
    """Ordena solo los lotes nuevos y los fusiona con la lista vieja.

    Args:
        viejos: lista del día anterior, en orden FEFO.
        nuevos: lotes nuevos del día.

    Returns:
        Una lista nueva en orden FEFO, igual a la de las otras estrategias.
    """
    return fusionar(viejos, ordenar_mezcla(nuevos))


def despachables(ordenados: list[Lote], hoy: int = 0) -> list[Lote]:
    """Quita los lotes vencidos de una lista en orden FEFO.

    Un lote está vencido si su fecha de vencimiento es anterior a ``hoy``.
    Como la lista está ordenada por vencimiento, los vencidos forman un
    bloque al principio; una búsqueda binaria encuentra dónde termina.

    Args:
        ordenados: lotes en orden FEFO.
        hoy: día de referencia (0 en los datos sintéticos).

    Returns:
        Los lotes que se pueden despachar, en orden FEFO.
    """
    bajo, alto = 0, len(ordenados)
    while bajo < alto:
        medio = (bajo + alto) // 2
        _contador["operaciones"] += 1
        if ordenados[medio].vencimiento < hoy:
            bajo = medio + 1
        else:
            alto = medio
    return ordenados[bajo:]
