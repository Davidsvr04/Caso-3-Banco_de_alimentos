"""Cargue de un vehículo del banco de alimentos por programación dinámica.

Es una mochila 0/1: cada lote sube completo o no sube. La tabla
``K[i][w]`` guarda el mayor valor nutricional que se logra escogiendo solo
entre los ``i`` primeros lotes con un vehículo de ``w`` kilogramos.
"""

Lote = tuple[int, int, int]  # (peso_kg, valor_nutricional, dias_para_vencer)

_contador = {"operaciones": 0}


def reiniciar_operaciones() -> None:
    """Pone en cero el contador de operaciones del módulo."""
    _contador["operaciones"] = 0


def leer_operaciones() -> int:
    """Devuelve las operaciones contadas desde el último reinicio.

    Returns:
        El número de celdas de la tabla calculadas.
    """
    return _contador["operaciones"]


def llenar_tabla(lotes: list[Lote], capacidad_kg: int) -> list[list[int]]:
    """Llena la tabla de la mochila 0/1, fila por fila.

    Recurrencia, para i de 1 a n y w de 0 a W:

        K[i][w] = K[i-1][w]                              si peso_i > w
        K[i][w] = max(K[i-1][w], valor_i + K[i-1][w - peso_i])  si no

    con caso base K[0][w] = 0.

    Args:
        lotes: lotes candidatos de la ruta; la fila i corresponde al lote
            ``lotes[i - 1]``.
        capacidad_kg: capacidad del vehículo en kilogramos (W).

    Returns:
        La tabla K de (n + 1) filas y (W + 1) columnas.
    """
    columnas = capacidad_kg + 1
    tabla: list[list[int]] = [[0] * columnas]  # fila 0: sin lotes, valor 0
    for i in range(1, len(lotes) + 1):
        peso, valor, _ = lotes[i - 1]
        anterior = tabla[i - 1]
        # Opción (a), no subir el lote: se copia la fila de arriba en todas
        # las columnas. Para w < peso es la única opción.
        fila = anterior[:]
        # Opción (b), subir el lote: solo en las columnas donde cabe.
        for w in range(peso, columnas):
            subir = valor + anterior[w - peso]
            if subir > fila[w]:
                fila[w] = subir
        tabla.append(fila)
        # Cada fila calcula W + 1 celdas (las que copian y las que comparan).
        _contador["operaciones"] += columnas
    return tabla


def reconstruir_lotes(
    lotes: list[Lote], tabla: list[list[int]], capacidad_kg: int
) -> list[int]:
    """Recupera qué lotes forman una carga óptima.

    Se recorre la tabla desde la esquina inferior derecha: si
    ``K[i][w]`` es distinto de ``K[i-1][w]``, el lote ``i - 1`` subió y la
    capacidad libre baja en su peso.

    Args:
        lotes: los mismos lotes con que se llenó la tabla.
        tabla: tabla devuelta por ``llenar_tabla``.
        capacidad_kg: capacidad con que se llenó la tabla.

    Returns:
        Los índices de los lotes cargados, en orden creciente.
    """
    cargados: list[int] = []
    w = capacidad_kg
    for i in range(len(lotes), 0, -1):
        if tabla[i][w] != tabla[i - 1][w]:
            cargados.append(i - 1)
            w -= lotes[i - 1][0]
    cargados.reverse()
    return cargados


def cargar_vehiculo(
    lotes: list[Lote], capacidad_kg: int
) -> tuple[int, list[int]]:
    """Elige los lotes de mayor valor nutricional que caben en el vehículo.

    Args:
        lotes: lotes candidatos de la ruta; no se fraccionan.
        capacidad_kg: capacidad máxima del vehículo en kilogramos.

    Returns:
        El valor nutricional máximo y los índices de los lotes cargados.
    """
    if capacidad_kg <= 0 or not lotes:
        return 0, []
    tabla = llenar_tabla(lotes, capacidad_kg)
    cargados = reconstruir_lotes(lotes, tabla, capacidad_kg)
    return tabla[len(lotes)][capacidad_kg], cargados
