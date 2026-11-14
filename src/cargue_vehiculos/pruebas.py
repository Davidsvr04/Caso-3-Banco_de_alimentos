"""Pruebas con assert del cargue de los vehículos.

Se ejecuta desde la raíz del repositorio con:

    python src/cargue_vehiculos/pruebas.py

Si alguna prueba falla, el script se detiene con AssertionError e indica la
instancia que falló.
"""

from datos import instancias_pequenas
from estrategia import cargar_vehiculo, llenar_tabla
from exhaustivo import cargar_exhaustivo
from regla_actual import cargar_por_densidad, cargar_por_vencimiento

Lote = tuple[int, int, int]  # (peso_kg, valor_nutricional, dias_para_vencer)

# Ejemplo resuelto a mano en el informe (vehículo de 10 kg, 5 lotes).
EJEMPLO: list[Lote] = [
    (6, 15, 3),  # L0
    (5, 11, 1),  # L1
    (5, 12, 4),  # L2
    (3, 5, 2),   # L3
    (2, 3, 5),   # L4
]
CAPACIDAD_EJEMPLO = 10
TABLA_A_MANO = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15],
    [0, 0, 0, 0, 0, 11, 15, 15, 15, 15, 15],
    [0, 0, 0, 0, 0, 12, 15, 15, 15, 15, 23],
    [0, 0, 0, 5, 5, 12, 15, 15, 17, 20, 23],
    [0, 0, 3, 5, 5, 12, 15, 15, 18, 20, 23],
]

SOLUCIONES = [
    cargar_vehiculo,
    cargar_exhaustivo,
    cargar_por_vencimiento,
    cargar_por_densidad,
]


def carga_valida(
    lotes: list[Lote], capacidad_kg: int, resultado: tuple[int, list[int]]
) -> bool:
    """Revisa la restricción del negocio sobre un resultado.

    Comprueba que los índices existan y no se repitan (un lote sube una
    sola vez y completo), que el peso total no supere la capacidad y que el
    valor informado sea la suma de los valores completos de los lotes.

    Args:
        lotes: lotes candidatos.
        capacidad_kg: capacidad del vehículo.
        resultado: pareja (valor, índices) que devolvió una solución.

    Returns:
        True si la carga cumple todas las condiciones.
    """
    valor, indices = resultado
    if len(set(indices)) != len(indices):
        return False
    if any(i < 0 or i >= len(lotes) for i in indices):
        return False
    peso_total = sum(lotes[i][0] for i in indices)
    valor_total = sum(lotes[i][1] for i in indices)
    return peso_total <= capacidad_kg and valor_total == valor


def probar_casos_limite() -> None:
    """Entrada vacía, un solo lote, nada cabe, todo cabe y capacidad 0."""
    for solucion in SOLUCIONES:
        # Sin lotes candidatos.
        assert solucion([], 3000) == (0, []), solucion.__name__
        # Un solo lote que cabe.
        assert solucion([(100, 400, 5)], 3000) == (400, [0]), solucion.__name__
        # Un solo lote que no cabe.
        assert solucion([(3500, 900, 5)], 3000) == (0, []), solucion.__name__
        # Ningún lote cabe.
        nada = [(10, 5, 1), (12, 8, 2), (15, 9, 3)]
        assert solucion(nada, 9) == (0, []), solucion.__name__
        # Capacidad 0: no sube nada.
        cero = [(1, 1, 1), (2, 3, 1)]
        assert solucion(cero, 0) == (0, []), solucion.__name__
        # Todos los lotes caben: suben todos.
        todos = [(5, 10, 3), (7, 2, 1), (3, 6, 2)]
        assert solucion(todos, 15) == (18, [0, 1, 2]), solucion.__name__
        # Lote que llena exactamente la capacidad.
        assert solucion([(50, 70, 1)], 50) == (70, [0]), solucion.__name__


def probar_ejemplo_a_mano() -> None:
    """El ejemplo de la Parte 1, con la tabla calculada a mano."""
    assert llenar_tabla(EJEMPLO, CAPACIDAD_EJEMPLO) == TABLA_A_MANO
    assert cargar_vehiculo(EJEMPLO, CAPACIDAD_EJEMPLO) == (23, [1, 2])
    assert cargar_exhaustivo(EJEMPLO, CAPACIDAD_EJEMPLO) == (23, [1, 2])


def probar_contraejemplo() -> None:
    """La instancia donde las dos reglas quedan por debajo del óptimo."""
    optimo, _ = cargar_vehiculo(EJEMPLO, CAPACIDAD_EJEMPLO)
    vencimiento = cargar_por_vencimiento(EJEMPLO, CAPACIDAD_EJEMPLO)
    densidad = cargar_por_densidad(EJEMPLO, CAPACIDAD_EJEMPLO)
    # Por vencimiento: L1 (vence en 1 día), L3 (2 días) y se detiene en L0.
    assert vencimiento == (16, [1, 3])
    # Por densidad: L0 (2,50 por kg), salta L2 y L1, sube L3.
    assert densidad == (20, [0, 3])
    assert optimo == 23
    assert vencimiento[0] < optimo and densidad[0] < optimo
    assert optimo - vencimiento[0] == 7
    assert optimo - densidad[0] == 3


def probar_aleatorias(cantidad: int = 200, semilla: int = 2026) -> int:
    """Compara la programación dinámica con la exhaustiva al azar.

    Args:
        cantidad: número de instancias aleatorias pequeñas.
        semilla: semilla fija.

    Returns:
        El número de instancias revisadas.
    """
    instancias = instancias_pequenas(cantidad, semilla)
    for lotes, capacidad in instancias:
        dinamica = cargar_vehiculo(lotes, capacidad)
        exacta = cargar_exhaustivo(lotes, capacidad)
        assert dinamica[0] == exacta[0], (lotes, capacidad)
        # La restricción del negocio, en todas las soluciones.
        for solucion in SOLUCIONES:
            resultado = solucion(lotes, capacidad)
            assert carga_valida(lotes, capacidad, resultado), (
                solucion.__name__, lotes, capacidad)
            # Ninguna regla puede superar el óptimo.
            assert resultado[0] <= exacta[0], (solucion.__name__, lotes)
    return len(instancias)


def probar_regla_vencimiento_se_detiene() -> None:
    """La regla actual no salta un lote que no cabe para buscar otro."""
    # Orden de vencimiento: L0 (60 kg), L1 (50 kg, ya no cabe), L2 (10 kg).
    lotes = [(60, 100, 1), (50, 70, 2), (10, 30, 3)]
    assert cargar_por_vencimiento(lotes, 100) == (100, [0])
    # La densidad, en cambio, sí sigue buscando y sube L2.
    assert cargar_por_densidad(lotes, 100) == (130, [0, 2])


def main() -> None:
    """Ejecuta todas las pruebas e informa el resultado."""
    probar_casos_limite()
    print("Casos límite: OK")
    probar_ejemplo_a_mano()
    print("Ejemplo resuelto a mano (valor 23, lotes L1 y L2): OK")
    probar_contraejemplo()
    print("Contraejemplo: vencimiento 16, densidad 20, óptimo 23: OK")
    probar_regla_vencimiento_se_detiene()
    print("La regla actual se detiene en el primer lote que no cabe: OK")
    revisadas = probar_aleatorias()
    print(f"{revisadas} instancias aleatorias: la programación dinámica "
          "coincide con la exhaustiva y ninguna carga supera la capacidad: OK")
    print("Todas las pruebas pasaron.")


if __name__ == "__main__":
    main()
