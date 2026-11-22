"""Estrategias propuestas para el tramo de mayor crecimiento (operación 4).

Es el problema del subarreglo de suma máxima. Un tramo se representa como
(suma, inicio, fin), con inicio y fin incluidos; la serie vacía devuelve
(0, 0, -1). El tramo siempre tiene al menos una hora: si todas las horas
son negativas, el resultado es la hora menos negativa.

* ``tramo_acumulado``: todos los tramos, pero sumando de forma
  incremental. Θ(n²). Sirve de solución exacta para verificar.
* ``tramo_dividir_y_vencer``: parte la serie a la mitad; el mejor tramo
  está a la izquierda, a la derecha o cruza la mitad. Θ(n log n).
* ``tramo_kadane``: programación dinámica sobre "el mejor tramo que
  termina en la hora i". Θ(n) y espacio Θ(1).
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


def tramo_acumulado(serie: list[int]) -> Tramo:
    """Evalúa todos los tramos, reutilizando la suma del tramo anterior.

    Args:
        serie: cambio neto por hora, en kg.

    Returns:
        El tramo (suma, inicio, fin) de mayor suma.
    """
    n = len(serie)
    if n == 0:
        return (0, 0, -1)
    mejor: Tramo = (serie[0], 0, 0)
    for inicio in range(n):
        total = 0
        for fin in range(inicio, n):
            total += serie[fin]  # suma(inicio..fin) = suma(inicio..fin-1) + x
            if total > mejor[0]:
                mejor = (total, inicio, fin)
    _contador["operaciones"] += n * (n + 1) // 2
    return mejor


def _mejor_cruzado(serie: list[int], bajo: int, medio: int,
                   alto: int) -> Tramo:
    """Mejor tramo que contiene las horas ``medio`` y ``medio + 1``.

    Args:
        serie: la serie completa.
        bajo: primera hora del subproblema.
        medio: última hora de la mitad izquierda.
        alto: última hora del subproblema.

    Returns:
        El mejor tramo que cruza la mitad.
    """
    total = 0
    mejor_izq = serie[medio]
    inicio = medio
    for hora in range(medio, bajo - 1, -1):  # crece hacia la izquierda
        total += serie[hora]
        if total > mejor_izq:
            mejor_izq, inicio = total, hora
    total = 0
    mejor_der = serie[medio + 1]
    fin = medio + 1
    for hora in range(medio + 1, alto + 1):  # crece hacia la derecha
        total += serie[hora]
        if total > mejor_der:
            mejor_der, fin = total, hora
    _contador["operaciones"] += alto - bajo + 1
    return (mejor_izq + mejor_der, inicio, fin)


def _dividir(serie: list[int], bajo: int, alto: int) -> Tramo:
    """Resuelve el subproblema serie[bajo..alto] por dividir y vencer.

    Args:
        serie: la serie completa.
        bajo: primera hora del subproblema.
        alto: última hora del subproblema.

    Returns:
        El mejor tramo dentro de [bajo, alto].
    """
    if bajo == alto:  # caso base: una sola hora
        _contador["operaciones"] += 1
        return (serie[bajo], bajo, bajo)
    medio = (bajo + alto) // 2
    izquierda = _dividir(serie, bajo, medio)
    derecha = _dividir(serie, medio + 1, alto)
    cruzado = _mejor_cruzado(serie, bajo, medio, alto)
    mejor = izquierda
    if cruzado[0] > mejor[0]:
        mejor = cruzado
    if derecha[0] > mejor[0]:
        mejor = derecha
    return mejor


def tramo_dividir_y_vencer(serie: list[int]) -> Tramo:
    """Tramo de mayor suma por dividir y vencer.

    Args:
        serie: cambio neto por hora, en kg.

    Returns:
        El tramo (suma, inicio, fin) de mayor suma.
    """
    if not serie:
        return (0, 0, -1)
    return _dividir(serie, 0, len(serie) - 1)


def tramo_kadane(serie: list[int]) -> Tramo:
    """Tramo de mayor suma por programación dinámica (Kadane).

    ``aqui`` es la mejor suma de un tramo que termina exactamente en la
    hora actual: o se extiende el tramo anterior (aqui + x) o se empieza
    de nuevo en esta hora (x), lo que sea mayor.

    Args:
        serie: cambio neto por hora, en kg.

    Returns:
        El tramo (suma, inicio, fin) de mayor suma.
    """
    if not serie:
        return (0, 0, -1)
    aqui = serie[0]
    inicio_aqui = 0
    mejor: Tramo = (serie[0], 0, 0)
    for hora in range(1, len(serie)):
        x = serie[hora]
        if aqui + x < x:  # el tramo anterior resta: conviene empezar aquí
            aqui = x
            inicio_aqui = hora
        else:
            aqui += x
        if aqui > mejor[0]:
            mejor = (aqui, inicio_aqui, hora)
    _contador["operaciones"] += len(serie)
    return mejor
