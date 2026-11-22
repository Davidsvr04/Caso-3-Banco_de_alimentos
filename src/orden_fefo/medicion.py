"""Experimentos y gráficas del ordenamiento FEFO (operación 2).

Se ejecuta desde la raíz del repositorio con:

    python src/orden_fefo/medicion.py

Produce en graficas/orden_fefo/: tiempo_vs_n.png, operaciones_vs_n.png,
mediciones.csv, resumen.md y resumen.json.
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

import actual  # noqa: E402
import estrategias  # noqa: E402
from datos import Lote, generar_dia, nuevos_para  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CARPETA = RAIZ / "graficas" / "orden_fefo"

SEMILLA = 2026
N_REAL = 229_000          # 220.000 activos + 9.000 nuevos (peor día)
N_CRECIMIENTO = 458_000   # segunda bodega: el doble de lotes
# Cada tamaño es el doble del anterior.
TAMANOS_INSERCION = [1_789, 3_578, 7_156, 14_312, 28_625, 57_250]
TAMANOS_RAPIDOS = TAMANOS_INSERCION + [114_500, 229_000, 458_000]
REPETICIONES = 3
DIAS_ANIO = 300
POTENCIA_KW = 0.150

Ordenar = Callable[[list[Lote], list[Lote]], list[Lote]]
SOLUCIONES: dict[str, tuple[Ordenar, object]] = {
    "Inserción (actual)": (actual.ordenar_insercion, actual),
    "Mezcla de toda la lista": (estrategias.ordenar_mezcla_total,
                                estrategias),
    "Ordenar nuevos + fusionar": (estrategias.fusionar_nuevos, estrategias),
}
COLORES = {"Inserción (actual)": "#eb6834",
           "Mezcla de toda la lista": "#6250d6",
           "Ordenar nuevos + fusionar": "#2a78d6"}
MARCADORES = {"Inserción (actual)": "s", "Mezcla de toda la lista": "D",
              "Ordenar nuevos + fusionar": "o"}
TINTA, TINTA_2 = "#0b0b0b", "#52514e"
SUPERFICIE, REJILLA = "#fcfcfb", "#e4e3df"

Medicion = dict[str, float | str]


def medir(nombre: str, viejos: list[Lote], nuevos: list[Lote],
          repeticiones: int) -> tuple[float, int, list[Lote]]:
    """Mide una estrategia sobre un día sintético.

    Args:
        nombre: clave en ``SOLUCIONES``.
        viejos: lista del día anterior, ordenada.
        nuevos: lotes nuevos.
        repeticiones: ejecuciones a promediar.

    Returns:
        Tiempo medio en segundos, comparaciones y la lista obtenida.
    """
    funcion, modulo = SOLUCIONES[nombre]
    tiempos = []
    resultado: list[Lote] = []
    operaciones = 0
    for repeticion in range(repeticiones):
        gc.collect()
        modulo.reiniciar_operaciones()
        inicio = time.perf_counter()
        resultado = funcion(viejos, nuevos)
        tiempos.append(time.perf_counter() - inicio)
        if repeticion == 0:
            operaciones = modulo.leer_operaciones()
    return sum(tiempos) / len(tiempos), operaciones, resultado


def experimento() -> list[Medicion]:
    """Mide las tres estrategias en tamaños crecientes.

    Returns:
        Una medición por tamaño y estrategia.
    """
    filas: list[Medicion] = []
    for n in TAMANOS_RAPIDOS:
        k = nuevos_para(n)
        viejos, nuevos = generar_dia(n - k, k, SEMILLA + n)
        resultados = {}
        for nombre in SOLUCIONES:
            if nombre == "Inserción (actual)" and n not in TAMANOS_INSERCION:
                continue
            repeticiones = 1 if (nombre == "Inserción (actual)"
                                 and n > 30_000) else REPETICIONES
            tiempo, ops, lista = medir(nombre, viejos, nuevos, repeticiones)
            resultados[nombre] = lista
            filas.append({"solucion": nombre, "n": n, "k": k,
                          "tiempo_s": tiempo, "operaciones": ops})
            print(f"  n={n:7d} k={k:6d} {nombre:26s} "
                  f"{tiempo * 1000:12.2f} ms  ops={ops:12d}")
        # Verificación dentro del experimento: las listas son idénticas.
        listas = list(resultados.values())
        assert all(lista == listas[0] for lista in listas), n
    return filas


def serie(filas: list[Medicion], nombre: str,
          campo: str) -> tuple[list[float], list[float]]:
    """Extrae la serie (n, valor) de una estrategia.

    Args:
        filas: mediciones.
        nombre: estrategia.
        campo: "tiempo_s" u "operaciones".

    Returns:
        Listas de n y de valores.
    """
    elegidas = [f for f in filas if f["solucion"] == nombre]
    return [f["n"] for f in elegidas], [f[campo] for f in elegidas]


def grafica(filas: list[Medicion], campo: str, escala: float,
            etiqueta_y: str, titulo: str, archivo: str) -> None:
    """Dibuja las tres estrategias en los mismos ejes (log-log).

    Args:
        filas: mediciones.
        campo: "tiempo_s" u "operaciones".
        escala: factor de unidad.
        etiqueta_y: rótulo del eje y.
        titulo: título.
        archivo: nombre del PNG.
    """
    figura, ax = plt.subplots(figsize=(9, 5.6))
    figura.patch.set_facecolor(SUPERFICIE)
    for nombre in SOLUCIONES:
        xs, ys = serie(filas, nombre, campo)
        ax.plot(xs, [y * escala for y in ys], label=nombre,
                color=COLORES[nombre], marker=MARCADORES[nombre],
                linewidth=2, markersize=6)
    ax.axvline(N_REAL, color=TINTA_2, linestyle="--", linewidth=1)
    ax.text(N_REAL * 1.04, ax.get_ylim()[0] * 3, "volumen real",
            color=TINTA_2, rotation=90)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Lotes en la lista n (escala logarítmica; k ≈ 3,9 % "
                  "son nuevos)")
    ax.set_ylabel(etiqueta_y)
    ax.set_title(titulo, color=TINTA)
    ax.set_facecolor(SUPERFICIE)
    ax.grid(True, color=REJILLA, linewidth=0.8)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.legend(frameon=False)
    figura.tight_layout()
    figura.savefig(CARPETA / archivo, dpi=130, facecolor=SUPERFICIE)
    plt.close(figura)


def modelo(nombre: str, n: int) -> float:
    """Costo teórico de cada estrategia (sin constante).

    Args:
        nombre: estrategia.
        n: lotes totales (k se deduce de n).

    Returns:
        El valor de la función de complejidad.
    """
    k = nuevos_para(n)
    if nombre == "Inserción (actual)":
        return (n - k) * k
    if nombre == "Mezcla de toda la lista":
        return n * math.log2(n)
    return k * math.log2(k) + n


def constante(filas: list[Medicion], nombre: str, minimo: int) -> float:
    """Ajusta la constante c de t ≈ c · modelo(n) con los puntos grandes.

    Args:
        filas: mediciones.
        nombre: estrategia.
        minimo: n mínimo a usar en el ajuste.

    Returns:
        La constante en segundos por unidad de costo.
    """
    puntos = [f for f in filas if f["solucion"] == nombre
              and f["n"] >= minimo]
    return sum(f["tiempo_s"] / modelo(nombre, int(f["n"]))
               for f in puntos) / len(puntos)


def resumen(filas: list[Medicion]) -> tuple[str, dict]:
    """Factores al duplicar, extrapolación y energía.

    Args:
        filas: mediciones.

    Returns:
        El texto de resumen.md y el diccionario de resumen.json.
    """
    lineas = ["# Resumen de la medición — ordenamiento FEFO", "",
              "## Factor al duplicar n", "",
              "| Estrategia | n → 2n | Tiempo × | Comparaciones × | "
              "Esperado × |", "|---|---|---|---|---|"]
    for nombre in SOLUCIONES:
        xs, ts = serie(filas, nombre, "tiempo_s")
        _, os_ = serie(filas, nombre, "operaciones")
        for i in range(len(xs) - 1):
            esperado = (modelo(nombre, int(xs[i + 1]))
                        / modelo(nombre, int(xs[i])))
            lineas.append(f"| {nombre} | {xs[i]:,} → {xs[i + 1]:,} | "
                          f"{ts[i + 1] / ts[i]:.2f} | "
                          f"{os_[i + 1] / os_[i]:.2f} | {esperado:.2f} |")
    lineas.append("")
    datos: dict = {"operacion": "2. Ordenamiento FEFO"}
    c_ins = constante(filas, "Inserción (actual)", 14_000)
    lineas += ["## Extrapolación", "",
               f"Inserción: c = {c_ins * 1e9:.1f} ns por unidad de "
               "(n − k)·k, ajustada con n ≥ 14.000.", "",
               "| Estrategia | n = 229.000 (real) | n = 458.000 "
               "(crecimiento) | Energía al año, real (kWh) |",
               "|---|---|---|---|"]
    for etiqueta, n in (("real", N_REAL), ("crecimiento", N_CRECIMIENTO)):
        medidas = {f["solucion"]: f["tiempo_s"] for f in filas
                   if f["n"] == n}
        inser = c_ins * modelo("Inserción (actual)", n)
        datos[etiqueta] = {
            "n": n, "k": nuevos_para(n),
            "ventana_actual_s": inser,
            "ventana_mezcla_s": medidas["Mezcla de toda la lista"],
            "ventana_propuesta_s": medidas["Ordenar nuevos + fusionar"],
        }
    for nombre, clave in (("Inserción (actual)", "ventana_actual_s"),
                          ("Mezcla de toda la lista", "ventana_mezcla_s"),
                          ("Ordenar nuevos + fusionar",
                           "ventana_propuesta_s")):
        real = datos["real"][clave]
        crec = datos["crecimiento"][clave]
        kwh = POTENCIA_KW * real / 3600 * DIAS_ANIO
        fuente = "extrapolado" if nombre.startswith("Inser") else "medido"
        lineas.append(f"| {nombre} | {real:.3f} s ({fuente}) | "
                      f"{crec:.3f} s ({fuente}) | {kwh:.4f} |")
    for etiqueta in ("real", "crecimiento"):
        d = datos[etiqueta]
        d["dia_actual_s"] = d["ventana_actual_s"]
        d["dia_propuesta_s"] = d["ventana_propuesta_s"]
        d["kwh_anio_actual"] = POTENCIA_KW * d["dia_actual_s"] / 3600 * \
            DIAS_ANIO
        d["kwh_anio_propuesta"] = POTENCIA_KW * d["dia_propuesta_s"] / \
            3600 * DIAS_ANIO
    lineas.append("")
    return "\n".join(lineas), datos


def main() -> None:
    """Corre el experimento, las gráficas y el resumen."""
    CARPETA.mkdir(parents=True, exist_ok=True)
    filas = experimento()
    grafica(filas, "tiempo_s", 1000, "Tiempo medio (ms, escala log)",
            "Ordenamiento FEFO: tiempo frente al tamaño de la lista",
            "tiempo_vs_n.png")
    grafica(filas, "operaciones", 1, "Comparaciones (conteo, escala log)",
            "Ordenamiento FEFO: comparaciones frente al tamaño",
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
