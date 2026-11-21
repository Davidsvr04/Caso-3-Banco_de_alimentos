"""Generador del inventario sintético para la consulta de lotes.

Un lote se representa con la tupla con nombre ``Lote``. Las fechas de
vencimiento se guardan como un número entero de día (día 0 = hoy), lo que
permite compararlas y restarlas sin convertir fechas.

Todas las funciones usan su propio ``random.Random`` con semilla fija.
"""

import random
from typing import NamedTuple

CATEGORIAS = 40
DONANTES = 350


class Lote(NamedTuple):
    """Registro de un lote del inventario (no se modifica nunca)."""

    codigo: str
    categoria: int
    vencimiento: int  # días desde hoy; 0 = vence hoy
    peso_kg: int
    raciones: int
    donante: int


def codigo_de(numero: int) -> str:
    """Escribe el código de un lote a partir de un número.

    Args:
        numero: número entero no negativo.

    Returns:
        Un código de la forma ``"L0001234"``.
    """
    return f"L{numero:07d}"


def generar_lote(rng: random.Random, numero: int) -> Lote:
    """Genera un lote del inventario.

    Los vencimientos van de 0 a 365 días, con más lotes en las primeras
    semanas porque muchas donaciones llegan próximas a vencer.

    Args:
        rng: generador aleatorio con semilla fija.
        numero: número que se convierte en el código del lote.

    Returns:
        Un lote con todos sus campos.
    """
    if rng.random() < 0.4:
        vencimiento = rng.randint(0, 30)
    else:
        vencimiento = rng.randint(0, 365)
    return Lote(
        codigo=codigo_de(numero),
        categoria=rng.randrange(CATEGORIAS),
        vencimiento=vencimiento,
        peso_kg=rng.randint(20, 500),
        raciones=rng.randint(40, 4000),
        donante=rng.randrange(DONANTES),
    )


def generar_inventario(n: int, semilla: int) -> list[Lote]:
    """Genera un inventario de ``n`` lotes en orden de llegada.

    Los códigos son únicos, pero no llegan en orden: se toman de un rango
    mayor y se barajan, como pasa cuando los lotes de varios donantes se
    registran intercalados.

    Args:
        n: número de lotes.
        semilla: semilla fija.

    Returns:
        La lista de lotes, sin ningún orden en particular.
    """
    rng = random.Random(semilla)
    numeros = rng.sample(range(10 * n + 10), n)
    return [generar_lote(rng, numero) for numero in numeros]


def generar_consultas(
    inventario: list[Lote], cantidad: int, semilla: int,
    fraccion_inexistentes: float = 0.1
) -> list[str]:
    """Genera códigos para consultar, con algunos que no existen.

    Args:
        inventario: lotes existentes.
        cantidad: número de consultas.
        semilla: semilla fija.
        fraccion_inexistentes: parte de las consultas con código que no
            está en el inventario (por ejemplo, mal digitado).

    Returns:
        La lista de códigos a consultar.
    """
    rng = random.Random(semilla)
    existentes = {lote.codigo for lote in inventario}
    tope = 10 * len(inventario) + 10
    consultas: list[str] = []
    for _ in range(cantidad):
        if inventario and rng.random() >= fraccion_inexistentes:
            consultas.append(rng.choice(inventario).codigo)
        else:
            while True:
                codigo = codigo_de(rng.randrange(tope, 2 * tope))
                if codigo not in existentes:
                    consultas.append(codigo)
                    break
    return consultas
