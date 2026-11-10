"""Reglas de cargue que no garantizan el óptimo.

* ``cargar_por_vencimiento``: el procedimiento que usa hoy el coordinador
  (línea base del proceso actual).
* ``cargar_por_densidad``: la variante voraz por valor por kilogramo, que se
  incluye como segundo contraste.

Ambas cuentan sus operaciones elementales (comparaciones del ordenamiento
más lotes revisados) en un contador propio del módulo, que usa medicion.py.
"""

from functools import cmp_to_key

Lote = tuple[int, int, int]  # (peso_kg, valor_nutricional, dias_para_vencer)

_contador = {"operaciones": 0}


def reiniciar_operaciones() -> None:
    """Pone en cero el contador de operaciones del módulo."""
    _contador["operaciones"] = 0


def leer_operaciones() -> int:
    """Devuelve las operaciones contadas desde el último reinicio.

    Returns:
        Comparaciones del ordenamiento más lotes revisados.
    """
    return _contador["operaciones"]


def _orden_vencimiento(lotes: list[Lote]) -> list[int]:
    """Ordena las posiciones de los lotes del que vence primero al último.

    Si dos lotes vencen el mismo día, va primero el de menor posición
    (el que aparece antes en la lista de candidatos).

    Args:
        lotes: lotes candidatos de la ruta.

    Returns:
        Las posiciones de los lotes en el orden de cargue.
    """
    def comparar(i: int, j: int) -> int:
        _contador["operaciones"] += 1
        if lotes[i][2] != lotes[j][2]:
            return lotes[i][2] - lotes[j][2]
        return i - j

    return sorted(range(len(lotes)), key=cmp_to_key(comparar))


def _orden_densidad(lotes: list[Lote]) -> list[int]:
    """Ordena las posiciones de los lotes de mayor a menor valor por kg.

    La comparación se hace con enteros (v_i · w_j frente a v_j · w_i) para
    no depender del redondeo de los decimales. Si dos lotes tienen la misma
    densidad, va primero el de menor posición.

    Args:
        lotes: lotes candidatos de la ruta; todos con peso mayor que 0.

    Returns:
        Las posiciones de los lotes en el orden de cargue.
    """
    def comparar(i: int, j: int) -> int:
        _contador["operaciones"] += 1
        izquierda = lotes[i][1] * lotes[j][0]
        derecha = lotes[j][1] * lotes[i][0]
        if izquierda != derecha:
            return -1 if izquierda > derecha else 1
        return i - j

    return sorted(range(len(lotes)), key=cmp_to_key(comparar))


def cargar_por_vencimiento(
    lotes: list[Lote], capacidad_kg: int
) -> tuple[int, list[int]]:
    """Reproduce el procedimiento actual: carga por vencimiento.

    Se detiene en el primer lote que ya no cabe.

    Args:
        lotes: lotes candidatos de la ruta.
        capacidad_kg: capacidad máxima del vehículo en kilogramos.

    Returns:
        El valor nutricional cargado y los índices de los lotes cargados.
    """
    libre = capacidad_kg
    valor = 0
    cargados: list[int] = []
    for i in _orden_vencimiento(lotes):
        _contador["operaciones"] += 1
        peso, valor_lote, _ = lotes[i]
        if peso > libre:
            break  # el coordinador no sigue buscando lotes más pequeños
        cargados.append(i)
        libre -= peso
        valor += valor_lote
    cargados.sort()
    return valor, cargados


def cargar_por_densidad(
    lotes: list[Lote], capacidad_kg: int
) -> tuple[int, list[int]]:
    """Carga por mayor valor por kilogramo; no garantiza el óptimo.

    A diferencia de la regla por vencimiento, no se detiene en el primer
    lote que no cabe: lo salta y sigue probando los siguientes.

    Args:
        lotes: lotes candidatos de la ruta.
        capacidad_kg: capacidad máxima del vehículo en kilogramos.

    Returns:
        El valor nutricional cargado y los índices de los lotes cargados.
    """
    libre = capacidad_kg
    valor = 0
    cargados: list[int] = []
    for i in _orden_densidad(lotes):
        _contador["operaciones"] += 1
        peso, valor_lote, _ = lotes[i]
        if peso <= libre:
            cargados.append(i)
            libre -= peso
            valor += valor_lote
    cargados.sort()
    return valor, cargados
