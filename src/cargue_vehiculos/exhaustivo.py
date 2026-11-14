"""Cargue de un vehículo probando todos los subconjuntos de lotes.

Es la solución exacta con la que se verifica la programación dinámica.
Su costo es Θ(n·2^n): solo se ejecuta con pocos lotes (hasta unos 20).
"""

from itertools import product

Lote = tuple[int, int, int]  # (peso_kg, valor_nutricional, dias_para_vencer)

_contador = {"operaciones": 0}


def reiniciar_operaciones() -> None:
    """Pone en cero el contador de operaciones del módulo."""
    _contador["operaciones"] = 0


def leer_operaciones() -> int:
    """Devuelve las operaciones contadas desde el último reinicio.

    Returns:
        El número de lotes revisados en todos los subconjuntos explorados.
    """
    return _contador["operaciones"]


def cargar_exhaustivo(
    lotes: list[Lote], capacidad_kg: int
) -> tuple[int, list[int]]:
    """Calcula el mismo resultado probando todos los subconjuntos de lotes.

    Cada subconjunto es una fila de interruptores: ``interruptores[i] == 1``
    significa que el lote ``i`` sube al vehículo. Si dos subconjuntos
    empatan en valor, se queda el primero que encontró.

    Args:
        lotes: lotes candidatos de la ruta.
        capacidad_kg: capacidad máxima del vehículo en kilogramos.

    Returns:
        El valor nutricional máximo y los índices de los lotes cargados.
    """
    n = len(lotes)
    mejor_valor = 0
    mejor_subconjunto: list[int] = []
    for interruptores in product((0, 1), repeat=n):
        peso = 0
        valor = 0
        for i in range(n):
            if interruptores[i] == 1:
                peso += lotes[i][0]
                valor += lotes[i][1]
        _contador["operaciones"] += n  # se revisaron los n lotes
        if peso <= capacidad_kg and valor > mejor_valor:
            mejor_valor = valor
            mejor_subconjunto = [i for i in range(n) if interruptores[i] == 1]
    return mejor_valor, mejor_subconjunto
