"""Experimentos y gráficas de la consulta de inventario (operación 1).

Se ejecuta desde la raíz del repositorio con:

    python src/consulta_inventario/medicion.py

Produce en graficas/consulta_inventario/: tiempo_vs_n.png,
operaciones_vs_n.png, mediciones.csv, resumen.md y resumen.json (este
último lo usa src/proceso/energia.py).
"""

import csv
import gc
import json
import math
import time
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import NullFormatter  # noqa: E402

import actual  # noqa: E402
import indice as idx  # noqa: E402
from datos import generar_consultas, generar_inventario  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CARPETA = RAIZ / "graficas" / "consulta_inventario"

SEMILLA = 2026
# Cada tamaño es el doble del anterior; 229.000 es el volumen real
# (220.000 activos + hasta 9.000 nuevos) y 458.000 el de crecimiento.
TAMANOS = [14_312, 28_625, 57_250, 114_500, 229_000, 458_000]
N_REAL = 229_000
N_CRECIMIENTO = 458_000
CONSULTAS_LINEAL = 200
CONSULTAS_RAPIDAS = 5_000
RANGOS = 10
DIAS_RANGO = 3  # "¿qué vence en las próximas 72 horas?"
REPETICIONES = 3

CONSULTAS_DIA = 30_000
RANGOS_DIA = 14  # supuesto: una consulta por ruta durante la planeación
DIAS_ANIO = 300
POTENCIA_KW = 0.150

COLORES = {"Lineal (actual)": "#eb6834", "Búsqueda binaria": "#1baf7a",
           "Tabla hash": "#2a78d6"}
MARCADORES = {"Lineal (actual)": "s", "Búsqueda binaria": "^",
              "Tabla hash": "o"}
TINTA, TINTA_2 = "#0b0b0b", "#52514e"
SUPERFICIE, REJILLA = "#fcfcfb", "#e4e3df"

Medicion = dict[str, float | str]


def cronometrar(funcion: Callable[[], object], repeticiones: int) -> float:
    """Ejecuta una función varias veces y devuelve el tiempo medio.

    Args:
        funcion: función sin argumentos que hace todo el trabajo medido.
        repeticiones: número de ejecuciones.

    Returns:
        El tiempo medio de una ejecución, en segundos.
    """
    tiempos = []
    for _ in range(repeticiones):
        gc.collect()
        inicio = time.perf_counter()
        funcion()
        tiempos.append(time.perf_counter() - inicio)
    return sum(tiempos) / len(tiempos)


def contar(funcion: Callable[[], object], reiniciar: Callable[[], None],
           leer: Callable[[], int]) -> int:
    """Ejecuta una función una vez y devuelve sus operaciones contadas.

    Args:
        funcion: función sin argumentos.
        reiniciar: pone en cero el contador del módulo.
        leer: lee el contador del módulo.

    Returns:
        Las operaciones elementales de esa ejecución.
    """
    reiniciar()
    funcion()
    return leer()


def medir_tamano(n: int) -> list[Medicion]:
    """Mide las estrategias con un inventario de ``n`` lotes.

    Args:
        n: número de lotes del inventario.

    Returns:
        Mediciones por consulta (búsqueda por código y por rango) y la
        construcción del índice.
    """
    inventario = generar_inventario(n, SEMILLA + n)
    consultas = generar_consultas(inventario, CONSULTAS_RAPIDAS, SEMILLA)
    pocas = consultas[:CONSULTAS_LINEAL]
    # En el proceso completo la lista FEFO la entrega la operación 2; aquí
    # se prepara por fuera del cronómetro.
    fefo = sorted(inventario, key=lambda lote: (lote.vencimiento,
                                                lote.categoria))
    t_hash = cronometrar(
        lambda: {lote.codigo: lote for lote in inventario}, REPETICIONES)
    t_orden_codigo = cronometrar(
        lambda: idx.ordenar_mezcla(inventario, lambda lote: (lote.codigo,)),
        1)
    indice = idx.construir_indice(inventario, fefo)

    # Verificación dentro del experimento.
    for codigo in pocas:
        esperado = actual.buscar_lineal(inventario, codigo)
        assert idx.buscar_hash(indice, codigo) == esperado
        assert idx.buscar_binaria(indice, codigo) == esperado

    def lineal() -> None:
        for codigo in pocas:
            actual.buscar_lineal(inventario, codigo)

    def binaria() -> None:
        for codigo in consultas:
            idx.buscar_binaria(indice, codigo)

    def hash_() -> None:
        for codigo in consultas:
            idx.buscar_hash(indice, codigo)

    rangos = [(d, d + DIAS_RANGO) for d in range(RANGOS)]

    def rango_lineal() -> None:
        for desde, hasta in rangos:
            actual.por_vencer_lineal(inventario, desde, hasta)

    def rango_binaria() -> None:
        for desde, hasta in rangos:
            idx.por_vencer_binaria(indice, desde, hasta)

    filas: list[Medicion] = []
    casos = [
        ("codigo", "Lineal (actual)", lineal, len(pocas), actual),
        ("codigo", "Búsqueda binaria", binaria, len(consultas), idx),
        ("codigo", "Tabla hash", hash_, len(consultas), idx),
        ("rango", "Lineal (actual)", rango_lineal, len(rangos), actual),
        ("rango", "Búsqueda binaria", rango_binaria, len(rangos), idx),
    ]
    for consulta, nombre, funcion, cuantas, modulo in casos:
        tiempo = cronometrar(funcion, REPETICIONES) / cuantas
        ops = contar(funcion, modulo.reiniciar_operaciones,
                     modulo.leer_operaciones) / cuantas
        filas.append({"consulta": consulta, "solucion": nombre, "n": n,
                      "tiempo_s": tiempo, "operaciones": ops})
        print(f"  n={n:7d} {consulta:6s} {nombre:18s} "
              f"{tiempo * 1e6:12.2f} µs  ops={ops:12.1f}")
    filas.append({"consulta": "construir", "solucion": "Tabla hash",
                  "n": n, "tiempo_s": t_hash, "operaciones": n})
    filas.append({"consulta": "construir", "solucion": "Búsqueda binaria",
                  "n": n, "tiempo_s": t_orden_codigo, "operaciones": 0})
    # Peor caso de la búsqueda lineal: un código que no existe.
    inexistente = "X"
    t_peor = cronometrar(lambda: actual.buscar_lineal(inventario,
                                                      inexistente), 3)
    filas.append({"consulta": "peor_lineal", "solucion": "Lineal (actual)",
                  "n": n, "tiempo_s": t_peor, "operaciones": n})
    return filas


def serie(filas: list[Medicion], consulta: str, nombre: str,
          campo: str) -> tuple[list[float], list[float]]:
    """Extrae una serie (n, valor) de las mediciones.

    Args:
        filas: mediciones.
        consulta: "codigo", "rango", "construir" o "peor_lineal".
        nombre: solución.
        campo: "tiempo_s" u "operaciones".

    Returns:
        Las listas de n y de valores.
    """
    elegidas = [f for f in filas
                if f["consulta"] == consulta and f["solucion"] == nombre]
    return [f["n"] for f in elegidas], [f[campo] for f in elegidas]


def estilo(ax: plt.Axes) -> None:
    """Aplica el estilo común de las gráficas.

    Args:
        ax: ejes de matplotlib.
    """
    ax.set_facecolor(SUPERFICIE)
    ax.grid(True, color=REJILLA, linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.tick_params(colors=TINTA_2)
    ax.legend(frameon=False, labelcolor=TINTA)


def grafica(filas: list[Medicion], campo: str, escala: float,
            etiqueta_y: str, titulo: str, archivo: str) -> None:
    """Dibuja búsqueda por código y por rango en dos paneles.

    Args:
        filas: mediciones.
        campo: "tiempo_s" u "operaciones".
        escala: factor de unidad del eje y.
        etiqueta_y: rótulo del eje y con unidades.
        titulo: título general.
        archivo: nombre del PNG.
    """
    figura, (izq, der) = plt.subplots(1, 2, figsize=(13, 5.2))
    figura.patch.set_facecolor(SUPERFICIE)
    for nombre in COLORES:
        xs, ys = serie(filas, "codigo", nombre, campo)
        izq.plot(xs, [y * escala for y in ys], label=nombre,
                 color=COLORES[nombre], marker=MARCADORES[nombre],
                 linewidth=2, markersize=6)
    for nombre in ("Lineal (actual)", "Búsqueda binaria"):
        xs, ys = serie(filas, "rango", nombre, campo)
        der.plot(xs, [y * escala for y in ys], label=nombre,
                 color=COLORES[nombre], marker=MARCADORES[nombre],
                 linewidth=2, markersize=6)
    izq.set_title("Consulta de un lote por código")
    der.set_title(f"Lotes que vencen en un rango de {DIAS_RANGO + 1} días")
    for ax in (izq, der):
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(TAMANOS)
        ax.set_xticklabels([f"{n // 1000}k" for n in TAMANOS])
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_xlabel("Lotes en el inventario n (escala logarítmica)")
        ax.set_ylabel(etiqueta_y)
        estilo(ax)
    figura.suptitle(titulo, color=TINTA, fontsize=14)
    figura.tight_layout()
    figura.savefig(CARPETA / archivo, dpi=130, facecolor=SUPERFICIE)
    plt.close(figura)


def valor(filas: list[Medicion], consulta: str, nombre: str, n: int,
          campo: str = "tiempo_s") -> float:
    """Busca una medición puntual.

    Args:
        filas: mediciones.
        consulta: tipo de consulta.
        nombre: solución.
        n: tamaño.
        campo: campo a devolver.

    Returns:
        El valor medido.
    """
    for f in filas:
        if (f["consulta"] == consulta and f["solucion"] == nombre
                and f["n"] == n):
            return float(f[campo])
    raise KeyError((consulta, nombre, n))


def resumen(filas: list[Medicion]) -> tuple[str, dict]:
    """Calcula factores al duplicar, escala real, energía y crecimiento.

    Args:
        filas: mediciones.

    Returns:
        El texto de resumen.md y el diccionario de resumen.json.
    """
    lineas = ["# Resumen de la medición — consulta de inventario", "",
              "## Factor al duplicar n", "",
              "| Consulta | Solución | n → 2n | Tiempo × | Operaciones × | "
              "Esperado × |", "|---|---|---|---|---|---|"]
    esperado = {"Lineal (actual)": lambda n: 2.0,
                "Búsqueda binaria":
                    lambda n: math.log2(2 * n) / math.log2(n),
                "Tabla hash": lambda n: 1.0}
    for consulta, nombres in (("codigo", list(COLORES)),
                              ("rango", ["Lineal (actual)",
                                         "Búsqueda binaria"])):
        for nombre in nombres:
            for a, b in zip(TAMANOS, TAMANOS[1:]):
                ft = (valor(filas, consulta, nombre, b)
                      / valor(filas, consulta, nombre, a))
                fo = (valor(filas, consulta, nombre, b, "operaciones")
                      / valor(filas, consulta, nombre, a, "operaciones"))
                esp = esperado[nombre](a)
                if consulta == "rango" and nombre == "Búsqueda binaria":
                    esp = 2.0  # domina copiar los r lotes, y r crece con n
                lineas.append(f"| {consulta} | {nombre} | {a:,} → {b:,} | "
                              f"{ft:.2f} | {fo:.2f} | {esp:.2f} |")
    lineas.append("")

    datos: dict = {"operacion": "1. Consulta de inventario"}
    for etiqueta, n, consultas in (("real", N_REAL, CONSULTAS_DIA),
                                   ("crecimiento", N_CRECIMIENTO,
                                    2 * CONSULTAS_DIA)):
        t_lin = valor(filas, "codigo", "Lineal (actual)", n)
        t_hash = valor(filas, "codigo", "Tabla hash", n)
        t_bin = valor(filas, "codigo", "Búsqueda binaria", n)
        r_lin = valor(filas, "rango", "Lineal (actual)", n)
        r_bin = valor(filas, "rango", "Búsqueda binaria", n)
        construir = valor(filas, "construir", "Tabla hash", n)
        construir_bin = valor(filas, "construir", "Búsqueda binaria", n)
        peor = valor(filas, "peor_lineal", "Lineal (actual)", n)
        datos[etiqueta] = {
            "n": n,
            "consultas_dia": consultas,
            "ventana_actual_s": RANGOS_DIA * r_lin,
            "ventana_propuesta_s": RANGOS_DIA * r_bin + construir,
            "alistamiento_actual_s": consultas * t_lin,
            "alistamiento_propuesta_s": consultas * t_hash,
            "alistamiento_binaria_s": consultas * t_bin,
            "construir_binaria_s": construir_bin,
            "peor_consulta_lineal_s": peor,
            "consulta_hash_s": t_hash,
            "construir_indice_s": construir,
        }
    for etiqueta in ("real", "crecimiento"):
        d = datos[etiqueta]
        d["dia_actual_s"] = d["ventana_actual_s"] + d["alistamiento_actual_s"]
        d["dia_propuesta_s"] = (d["ventana_propuesta_s"]
                                + d["alistamiento_propuesta_s"])
        d["kwh_anio_actual"] = POTENCIA_KW * d["dia_actual_s"] / 3600 * \
            DIAS_ANIO
        d["kwh_anio_propuesta"] = POTENCIA_KW * d["dia_propuesta_s"] / 3600 \
            * DIAS_ANIO
        lineas += [
            f"## Volumen {etiqueta}: n = {d['n']:,} lotes, "
            f"{d['consultas_dia']:,} consultas por código al día", "",
            f"* Peor consulta lineal (código inexistente): "
            f"{d['peor_consulta_lineal_s'] * 1000:.1f} ms (límite: 1 s).",
            f"* Consulta con tabla hash: {d['consulta_hash_s'] * 1e6:.2f} µs.",
            f"* Construir la tabla hash: {d['construir_indice_s']:.3f} s "
            f"una vez al día; ordenar por código para la búsqueda binaria: "
            f"{d['construir_binaria_s']:.2f} s.",
            f"* Consultas por rango en la ventana ({RANGOS_DIA} al día): "
            f"actual {d['ventana_actual_s']:.2f} s, propuesta "
            f"{d['ventana_propuesta_s']:.3f} s (incluye construir la "
            "tabla hash; la lista FEFO la entrega la operación 2).",
            f"* Consultas por código del alistamiento: actual "
            f"{d['alistamiento_actual_s']:.1f} s, hash "
            f"{d['alistamiento_propuesta_s']:.3f} s, binaria "
            f"{d['alistamiento_binaria_s']:.3f} s.",
            f"* Energía al año ({DIAS_ANIO} días, {POTENCIA_KW * 1000:.0f} "
            f"W): actual {d['kwh_anio_actual']:.3f} kWh, propuesta "
            f"{d['kwh_anio_propuesta']:.4f} kWh.", ""]
    return "\n".join(lineas), datos


def main() -> None:
    """Corre el experimento, las gráficas y el resumen."""
    CARPETA.mkdir(parents=True, exist_ok=True)
    filas: list[Medicion] = []
    for n in TAMANOS:
        filas += medir_tamano(n)
    grafica(filas, "tiempo_s", 1e6, "Tiempo medio por consulta (µs)",
            "Consulta de inventario: tiempo por consulta",
            "tiempo_vs_n.png")
    grafica(filas, "operaciones", 1, "Operaciones por consulta (conteo)",
            "Consulta de inventario: operaciones por consulta",
            "operaciones_vs_n.png")
    with open(CARPETA / "mediciones.csv", "w", newline="",
              encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    texto, datos = resumen(filas)
    (CARPETA / "resumen.md").write_text(texto, encoding="utf-8")
    (CARPETA / "resumen.json").write_text(
        json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
