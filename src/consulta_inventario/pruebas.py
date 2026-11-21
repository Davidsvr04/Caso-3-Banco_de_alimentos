"""Pruebas con assert de la consulta de inventario.

Se ejecuta desde la raíz del repositorio con:

    python src/consulta_inventario/pruebas.py
"""

import random

from actual import buscar_lineal, por_vencer_lineal
from datos import Lote, generar_consultas, generar_inventario
from indice import (buscar_binaria, buscar_hash, construir_indice,
                    ordenar_mezcla, por_vencer_binaria)

# Ejemplo resuelto a mano en el informe: 8 lotes en orden de llegada.
EJEMPLO: list[Lote] = [
    Lote("L0000052", 3, 5, 120, 400, 1),
    Lote("L0000007", 1, 2, 80, 300, 2),
    Lote("L0000031", 0, 9, 200, 900, 1),
    Lote("L0000018", 2, 2, 60, 150, 3),
    Lote("L0000044", 1, 0, 90, 360, 2),
    Lote("L0000025", 0, 4, 150, 600, 4),
    Lote("L0000063", 2, 7, 70, 210, 3),
    Lote("L0000010", 1, 4, 110, 500, 1),
]


def codigos(lotes: list[Lote]) -> list[str]:
    """Extrae los códigos de una lista de lotes.

    Args:
        lotes: lotes.

    Returns:
        Los códigos, en el mismo orden.
    """
    return [lote.codigo for lote in lotes]


def probar_casos_limite() -> None:
    """Inventario vacío, un lote, código inexistente y rangos extremos."""
    vacio = construir_indice([])
    assert buscar_lineal([], "L0000001") is None
    assert buscar_hash(vacio, "L0000001") is None
    assert buscar_binaria(vacio, "L0000001") is None
    assert por_vencer_lineal([], 0, 10) == []
    assert por_vencer_binaria(vacio, 0, 10) == []

    uno = [Lote("L0000001", 0, 3, 10, 20, 0)]
    indice = construir_indice(uno)
    for buscar in (lambda c: buscar_lineal(uno, c),
                   lambda c: buscar_hash(indice, c),
                   lambda c: buscar_binaria(indice, c)):
        assert buscar("L0000001") == uno[0]
        assert buscar("L0000002") is None
    assert por_vencer_binaria(indice, 3, 3) == uno
    assert por_vencer_binaria(indice, 4, 9) == []
    assert por_vencer_binaria(indice, 5, 1) == []  # rango al revés


def probar_ejemplo_a_mano() -> None:
    """El ejemplo del informe, con los resultados calculados a mano."""
    indice = construir_indice(EJEMPLO)
    assert indice.codigos == ["L0000007", "L0000010", "L0000018",
                              "L0000025", "L0000031", "L0000044",
                              "L0000052", "L0000063"]
    assert indice.vencimientos == [0, 2, 2, 4, 4, 5, 7, 9]
    assert codigos(indice.fefo) == ["L0000044", "L0000007", "L0000018",
                                    "L0000025", "L0000010", "L0000052",
                                    "L0000063", "L0000031"]
    assert buscar_binaria(indice, "L0000031") == EJEMPLO[2]
    assert buscar_binaria(indice, "L0000030") is None
    # "¿Qué vence en los próximos 2 a 4 días?" → posiciones 1 a 4 de FEFO.
    assert codigos(por_vencer_binaria(indice, 2, 4)) == [
        "L0000007", "L0000018", "L0000025", "L0000010"]


def probar_aleatorias(cantidad: int = 200, semilla: int = 2026) -> None:
    """Las estrategias coinciden con la búsqueda lineal al azar.

    Args:
        cantidad: número de inventarios aleatorios.
        semilla: semilla fija.
    """
    rng = random.Random(semilla)
    for caso in range(cantidad):
        n = rng.randint(0, 60)
        inventario = generar_inventario(n, semilla + caso)
        copia = list(inventario)
        indice = construir_indice(inventario)
        for codigo in generar_consultas(inventario, 20, semilla + caso):
            esperado = buscar_lineal(inventario, codigo)
            assert buscar_hash(indice, codigo) == esperado, (caso, codigo)
            assert buscar_binaria(indice, codigo) == esperado, (caso, codigo)
        for _ in range(10):
            desde = rng.randint(-5, 370)
            hasta = desde + rng.randint(-3, 80)
            lineal = por_vencer_lineal(inventario, desde, hasta)
            binaria = por_vencer_binaria(indice, desde, hasta)
            # Mismos lotes (el orden de salida puede ser distinto).
            assert sorted(codigos(lineal)) == sorted(codigos(binaria)), caso
            # La binaria entrega el rango en orden FEFO.
            claves = [(lote.vencimiento, lote.categoria) for lote in binaria]
            assert claves == sorted(claves), caso
        # El inventario original no se modificó.
        assert inventario == copia, caso


def probar_registro_original() -> None:
    """Los índices apuntan a los mismos lotes: no copian ni modifican."""
    inventario = generar_inventario(500, 7)
    copia = list(inventario)
    indice = construir_indice(inventario)
    assert inventario == copia
    for lote in inventario[:50]:
        assert buscar_hash(indice, lote.codigo) is lote
        assert buscar_binaria(indice, lote.codigo) is lote


def probar_ordenar_mezcla() -> None:
    """El ordenamiento auxiliar coincide con sorted y es estable."""
    rng = random.Random(11)
    for _ in range(50):
        datos = [Lote(f"L{rng.randint(0, 99):07d}", rng.randint(0, 3),
                      rng.randint(0, 5), 1, 1, i) for i in range(30)]
        clave = (lambda lote: (lote.vencimiento, lote.categoria))
        assert ordenar_mezcla(datos, clave) == sorted(datos, key=clave)


def main() -> None:
    """Ejecuta todas las pruebas."""
    probar_casos_limite()
    print("Casos límite: OK")
    probar_ejemplo_a_mano()
    print("Ejemplo resuelto a mano: OK")
    probar_ordenar_mezcla()
    print("Ordenamiento por mezcla estable: OK")
    probar_registro_original()
    print("El registro original no se modifica: OK")
    probar_aleatorias()
    print("200 inventarios aleatorios: hash y búsqueda binaria coinciden "
          "con la búsqueda lineal: OK")
    print("Todas las pruebas pasaron.")


if __name__ == "__main__":
    main()
