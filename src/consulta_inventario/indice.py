"""Consulta de inventario con índices construidos una vez al día.

Estrategias propuestas para la operación 1:

* Búsqueda por código con **tabla hash** (``dict`` de Python): Θ(1) en
  promedio por consulta.
* Búsqueda por código con **búsqueda binaria** sobre la lista ordenada por
  código: Θ(log n) por consulta. Es la alternativa sin hash.
* Lotes por rango de vencimiento con **búsqueda binaria** sobre la lista
  en orden FEFO: Θ(log n + r), donde r es el número de lotes del rango.

Los índices guardan referencias a los mismos lotes: el registro original
no se copia ni se modifica.
"""

from dataclasses import dataclass
from typing import Callable

from datos import Lote

_contador = {"operaciones": 0}


def reiniciar_operaciones() -> None:
    """Pone en cero el contador de operaciones del módulo."""
    _contador["operaciones"] = 0


def leer_operaciones() -> int:
    """Devuelve las operaciones contadas desde el último reinicio.

    Returns:
        Comparaciones de la búsqueda binaria, accesos a la tabla hash y
        lotes copiados al resultado.
    """
    return _contador["operaciones"]


@dataclass
class Indice:
    """Índices del inventario de un día.

    Attributes:
        por_codigo: tabla hash código → lote.
        lotes_por_codigo: lotes ordenados por código.
        codigos: los códigos de ``lotes_por_codigo``, en el mismo orden.
        fefo: lotes ordenados por (vencimiento, categoría).
        vencimientos: los vencimientos de ``fefo``, en el mismo orden.
    """

    por_codigo: dict[str, Lote]
    lotes_por_codigo: list[Lote]
    codigos: list[str]
    fefo: list[Lote]
    vencimientos: list[int]


def ordenar_mezcla(
    lotes: list[Lote], clave: Callable[[Lote], tuple]
) -> list[Lote]:
    """Ordena por mezcla (dividir y vencer), de forma estable.

    Args:
        lotes: lotes a ordenar; la lista original no se modifica.
        clave: función que da la clave de orden de cada lote.

    Returns:
        Una lista nueva con los lotes ordenados.
    """
    if len(lotes) <= 1:
        return list(lotes)
    mitad = len(lotes) // 2
    izquierda = ordenar_mezcla(lotes[:mitad], clave)
    derecha = ordenar_mezcla(lotes[mitad:], clave)
    resultado: list[Lote] = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if clave(derecha[j]) < clave(izquierda[i]):
            resultado.append(derecha[j])
            j += 1
        else:  # en empate gana la izquierda: el orden es estable
            resultado.append(izquierda[i])
            i += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


def construir_indice(
    inventario: list[Lote], fefo: list[Lote] | None = None
) -> Indice:
    """Construye los índices del día.

    En el proceso completo la lista en orden FEFO ya la produce la
    operación 2; si se recibe, no se vuelve a ordenar.

    Args:
        inventario: lotes del día, en cualquier orden.
        fefo: la misma lista ya ordenada por (vencimiento, categoría), si
            se tiene.

    Returns:
        Los índices listos para consultar.
    """
    por_codigo = {lote.codigo: lote for lote in inventario}
    lotes_por_codigo = ordenar_mezcla(inventario, lambda lote: (lote.codigo,))
    if fefo is None:
        fefo = ordenar_mezcla(
            inventario, lambda lote: (lote.vencimiento, lote.categoria))
    return Indice(
        por_codigo=por_codigo,
        lotes_por_codigo=lotes_por_codigo,
        codigos=[lote.codigo for lote in lotes_por_codigo],
        fefo=fefo,
        vencimientos=[lote.vencimiento for lote in fefo],
    )


def primera_posicion_no_menor(valores: list, objetivo: object) -> int:
    """Búsqueda binaria: primera posición con valor >= objetivo.

    Args:
        valores: lista ordenada de menor a mayor.
        objetivo: valor buscado.

    Returns:
        Un índice entre 0 y len(valores).
    """
    bajo, alto = 0, len(valores)
    while bajo < alto:
        medio = (bajo + alto) // 2
        _contador["operaciones"] += 1
        if valores[medio] < objetivo:
            bajo = medio + 1
        else:
            alto = medio
    return bajo


def primera_posicion_mayor(valores: list, objetivo: object) -> int:
    """Búsqueda binaria: primera posición con valor > objetivo.

    Args:
        valores: lista ordenada de menor a mayor.
        objetivo: valor de referencia.

    Returns:
        Un índice entre 0 y len(valores).
    """
    bajo, alto = 0, len(valores)
    while bajo < alto:
        medio = (bajo + alto) // 2
        _contador["operaciones"] += 1
        if valores[medio] <= objetivo:
            bajo = medio + 1
        else:
            alto = medio
    return bajo


def buscar_hash(indice: Indice, codigo: str) -> Lote | None:
    """Busca un lote por código en la tabla hash.

    Args:
        indice: índices del día.
        codigo: código del lote buscado.

    Returns:
        El lote, o None si no existe.
    """
    _contador["operaciones"] += 1
    return indice.por_codigo.get(codigo)


def buscar_binaria(indice: Indice, codigo: str) -> Lote | None:
    """Busca un lote por código con búsqueda binaria.

    Args:
        indice: índices del día.
        codigo: código del lote buscado.

    Returns:
        El lote, o None si no existe.
    """
    posicion = primera_posicion_no_menor(indice.codigos, codigo)
    if posicion < len(indice.codigos) and indice.codigos[posicion] == codigo:
        return indice.lotes_por_codigo[posicion]
    return None


def por_vencer_binaria(indice: Indice, desde: int, hasta: int) -> list[Lote]:
    """Devuelve los lotes que vencen entre dos días, en orden FEFO.

    Dos búsquedas binarias ubican el inicio y el fin del rango; después se
    copian solo los r lotes del rango.

    Args:
        indice: índices del día.
        desde: primer día del rango (incluido).
        hasta: último día del rango (incluido).

    Returns:
        Los lotes del rango, del que vence primero al que vence último.
    """
    if desde > hasta:
        return []
    inicio = primera_posicion_no_menor(indice.vencimientos, desde)
    fin = primera_posicion_mayor(indice.vencimientos, hasta)
    _contador["operaciones"] += max(0, fin - inicio)
    return indice.fefo[inicio:fin]
