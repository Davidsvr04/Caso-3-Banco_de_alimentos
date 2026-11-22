"""Pruebas con assert del ordenamiento FEFO.

Se ejecuta desde la raíz del repositorio con:

    python src/orden_fefo/pruebas.py
"""

import random

from actual import ordenar_insercion
from datos import Lote, clave_fefo, generar_dia
from estrategias import despachables, fusionar_nuevos, ordenar_mezcla_total

ESTRATEGIAS = [ordenar_insercion, ordenar_mezcla_total, fusionar_nuevos]


def lote(codigo: str, vencimiento: int, categoria: int) -> Lote:
    """Crea un lote de prueba con peso y raciones fijos.

    Args:
        codigo: código del lote.
        vencimiento: día de vencimiento.
        categoria: categoría.

    Returns:
        El lote.
    """
    return Lote(codigo, categoria, vencimiento, 10, 10, 0)


# Ejemplo resuelto a mano en el informe.
VIEJOS = [lote("V", -1, 3), lote("A", 1, 2), lote("B", 3, 0),
          lote("C", 3, 4), lote("D", 6, 1), lote("E", 9, 0)]
NUEVOS = [lote("F", 2, 1), lote("G", 3, 0), lote("H", 1, 5)]
ESPERADO = ["V", "A", "H", "F", "B", "G", "C", "D", "E"]


def codigos(lotes: list[Lote]) -> list[str]:
    """Extrae los códigos de una lista de lotes.

    Args:
        lotes: lotes.

    Returns:
        Los códigos en el mismo orden.
    """
    return [x.codigo for x in lotes]


def respeta_fefo(lotes: list[Lote]) -> bool:
    """Revisa la restricción: dentro de cada categoría, sale primero lo que
    vence primero.

    Args:
        lotes: lista en el orden de despacho.

    Returns:
        True si ninguna categoría tiene un lote que vence después antes de
        uno que vence primero.
    """
    ultimo: dict[int, int] = {}
    for x in lotes:
        if x.vencimiento < ultimo.get(x.categoria, x.vencimiento):
            return False
        ultimo[x.categoria] = x.vencimiento
    return True


def probar_casos_limite() -> None:
    """Listas vacías, solo viejos, solo nuevos y un único lote."""
    unico = [lote("X", 4, 1)]
    for estrategia in ESTRATEGIAS:
        assert estrategia([], []) == []
        assert estrategia(VIEJOS, []) == VIEJOS  # nada nuevo: no cambia
        assert codigos(estrategia([], NUEVOS)) == ["H", "F", "G"]
        assert estrategia([], unico) == unico
        assert estrategia(unico, []) == unico
    assert despachables([]) == []
    assert despachables([lote("Y", -3, 0)]) == []


def probar_ejemplo_a_mano() -> None:
    """El ejemplo del informe, con el orden calculado a mano."""
    for estrategia in ESTRATEGIAS:
        assert codigos(estrategia(VIEJOS, NUEVOS)) == ESPERADO, estrategia
    listos = despachables(fusionar_nuevos(VIEJOS, NUEVOS), hoy=0)
    assert codigos(listos) == ESPERADO[1:]  # V ya venció


def probar_aleatorias(cantidad: int = 200, semilla: int = 2026) -> None:
    """Las tres estrategias dan exactamente la misma lista al azar.

    Args:
        cantidad: número de instancias.
        semilla: semilla fija.
    """
    rng = random.Random(semilla)
    for caso in range(cantidad):
        viejos, nuevos = generar_dia(rng.randint(0, 80), rng.randint(0, 20),
                                     semilla + caso)
        copia_viejos, copia_nuevos = list(viejos), list(nuevos)
        esperado = sorted(viejos + nuevos, key=clave_fefo)  # estable
        for estrategia in ESTRATEGIAS:
            obtenido = estrategia(viejos, nuevos)
            assert obtenido == esperado, (caso, estrategia.__name__)
            assert respeta_fefo(obtenido), caso
        listos = despachables(esperado, hoy=0)
        assert all(x.vencimiento >= 0 for x in listos), caso
        assert len(listos) == sum(1 for x in esperado if x.vencimiento >= 0)
        # Los registros originales no cambiaron.
        assert viejos == copia_viejos and nuevos == copia_nuevos, caso


def probar_estabilidad() -> None:
    """A igual vencimiento y categoría, conserva el orden de llegada."""
    viejos = [lote("a1", 5, 2), lote("a2", 5, 2)]
    nuevos = [lote("n1", 5, 2), lote("n2", 1, 0), lote("n3", 5, 2)]
    for estrategia in ESTRATEGIAS:
        assert codigos(estrategia(viejos, nuevos)) == [
            "n2", "a1", "a2", "n1", "n3"], estrategia.__name__


def main() -> None:
    """Ejecuta todas las pruebas."""
    probar_casos_limite()
    print("Casos límite: OK")
    probar_ejemplo_a_mano()
    print("Ejemplo resuelto a mano (y lote vencido excluido): OK")
    probar_estabilidad()
    print("Estabilidad en empates: OK")
    probar_aleatorias()
    print("200 instancias aleatorias: las tres estrategias dan la misma "
          "lista, respetan FEFO y no modifican el original: OK")
    print("Todas las pruebas pasaron.")


if __name__ == "__main__":
    main()
