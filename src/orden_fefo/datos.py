"""Generador de datos sintéticos para el ordenamiento FEFO.

Cada día hay una lista de lotes que ya quedó ordenada el día anterior y
un grupo de lotes nuevos que se anexan al final. Los lotes nuevos son
donaciones que suelen estar próximas a vencer, así que en el orden FEFO
les corresponde un lugar cerca del principio de la lista.

Las fechas de vencimiento son enteros: días contados desde hoy.
"""

import random
from typing import NamedTuple

CATEGORIAS = 40


class Lote(NamedTuple):
    """Registro de un lote (no se modifica nunca)."""

    codigo: str
    categoria: int
    vencimiento: int  # días desde hoy; negativo = ya vencido
    peso_kg: int
    raciones: int
    donante: int


def clave_fefo(lote: Lote) -> tuple[int, int]:
    """Clave del orden FEFO: vencimiento y, a igual fecha, categoría.

    Args:
        lote: un lote.

    Returns:
        La pareja (vencimiento, categoría).
    """
    return (lote.vencimiento, lote.categoria)


def _lote(rng: random.Random, numero: int, minimo: int, maximo: int) -> Lote:
    """Genera un lote con vencimiento entre dos días.

    Args:
        rng: generador con semilla fija.
        numero: número para el código.
        minimo: menor día de vencimiento.
        maximo: mayor día de vencimiento.

    Returns:
        Un lote.
    """
    return Lote(
        codigo=f"L{numero:07d}",
        categoria=rng.randrange(CATEGORIAS),
        vencimiento=rng.randint(minimo, maximo),
        peso_kg=rng.randint(20, 500),
        raciones=rng.randint(40, 4000),
        donante=rng.randrange(350),
    )


def generar_dia(
    n_viejos: int, k_nuevos: int, semilla: int
) -> tuple[list[Lote], list[Lote]]:
    """Genera la lista del día anterior (ordenada) y los lotes nuevos.

    La lista vieja se deja ordenada con ``sorted`` porque así la entrega
    el día anterior: preparar los datos no es parte de lo que se mide.

    Args:
        n_viejos: lotes que ya estaban en la lista ordenada.
        k_nuevos: lotes nuevos del día, en orden de llegada.
        semilla: semilla fija.

    Returns:
        La pareja (viejos en orden FEFO, nuevos sin ordenar).
    """
    rng = random.Random(semilla)
    viejos = [_lote(rng, i, -2, 365) for i in range(n_viejos)]
    viejos.sort(key=clave_fefo)
    nuevos = [_lote(rng, n_viejos + i, 1, 30) for i in range(k_nuevos)]
    return viejos, nuevos


def nuevos_para(n_total: int) -> int:
    """Número de lotes nuevos que corresponde a un tamaño total.

    Se conserva la proporción del peor día del caso: 9.000 nuevos sobre
    229.000 lotes (220.000 activos + 9.000).

    Args:
        n_total: lotes totales del día.

    Returns:
        Cuántos de ellos son nuevos.
    """
    return max(1, round(n_total * 9_000 / 229_000))
