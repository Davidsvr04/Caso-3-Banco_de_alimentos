"""Experimentos y gráficas del análisis de saturación (operación 4).

Se ejecuta desde la raíz del repositorio con:

    python src/saturacion_bodega/medicion.py

Produce en graficas/saturacion_bodega/: tiempo_vs_n.png,
operaciones_vs_n.png, mediciones.csv, resumen.md y resumen.json.
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
from datos import CATEGORIAS, generar_serie  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CARPETA = RAIZ / "graficas" / "saturacion_bodega"

SEMILLA = 2026
N_REAL = 36_000        # diez años de 3.600 horas por categoría
TAMANOS = [25, 50, 100, 200, 400, 800, 1_600, 3_200, 6_400, 12_800,
           36_000, 72_000]
LIMITE = {"Fuerza bruta (actual)": 800, "Todos los tramos acumulados":
          12_800, "Dividir y vencer": 72_000, "Kadane": 72_000}
REPETICIONES = 5
CORRIDAS_ANIO = 1       # supuesto: una vez al año, antes de la temporada
POTENCIA_KW = 0.150
SEGUNDOS_ANIO = 365.25 * 24 * 3600

Tramo = tuple[int, int, int]
SOLUCIONES: dict[str, Callable[[list[int]], Tramo]] = {
    "Fuerza bruta (actual)": actual.tramo_fuerza_bruta,
    "Todos los tramos acumulados": estrategias.tramo_acumulado,
    "Dividir y vencer": estrategias.tramo_dividir_y_vencer,
    "Kadane": estrategias.tramo_kadane,
}
MODULOS = {"Fuerza bruta (actual)": actual}
COLORES = {"Fuerza bruta (actual)": "#eb6834",
           "Todos los tramos acumulados": "#eda100",
           "Dividir y vencer": "#6250d6", "Kadane": "#2a78d6"}
MARCADORES = {"Fuerza bruta (actual)": "s",
              "Todos los tramos acumulados": "^",
              "Dividir y vencer": "D", "Kadane": "o"}
TINTA, TINTA_2 = "#0b0b0b", "#52514e"
SUPERFICIE, REJILLA = "#fcfcfb", "#e4e3df"

Medicion = dict[str, float | str]


def medir(nombre: str, serie: list[int]) -> tuple[float, int, Tramo]:
    """Mide una estrategia sobre una serie.

    Args:
        nombre: clave en ``SOLUCIONES``.
        serie: serie horaria.

    Returns:
        Tiempo medio (s), operaciones contadas y el tramo obtenido.
    """
    funcion = SOLUCIONES[nombre]
    modulo = MODULOS.get(nombre, estrategias)
    repeticiones = 1 if len(serie) >= LIMITE[nombre] / 2 and \
        nombre != "Kadane" else REPETICIONES
    tiempos = []
    tramo: Tramo = (0, 0, -1)
    operaciones = 0
    for repeticion in range(repeticiones):
        gc.collect()
        modulo.reiniciar_operaciones()
        inicio = time.perf_counter()
        tramo = funcion(serie)
        tiempos.append(time.perf_counter() - inicio)
        if repeticion == 0:
            operaciones = modulo.leer_operaciones()
    return sum(tiempos) / len(tiempos), operaciones, tramo


def experimento() -> list[Medicion]:
    """Mide cada estrategia hasta su tamaño límite.

    Returns:
        Las mediciones.
    """
    filas: list[Medicion] = []
    for n in TAMANOS:
        serie = generar_serie(n, SEMILLA + n)
        sumas = {}
        for nombre in SOLUCIONES:
            if n > LIMITE[nombre]:
                continue
            tiempo, ops, tramo = medir(nombre, serie)
            sumas[nombre] = tramo[0]
            filas.append({"solucion": nombre, "n": n, "tiempo_s": tiempo,
                          "operaciones": ops})
            print(f"  n={n:6d} {nombre:28s} {tiempo * 1000:12.3f} ms  "
                  f"ops={ops:14d}")
        # Verificación dentro del experimento: la misma suma máxima.
        assert len(set(sumas.values())) == 1, (n, sumas)
    return filas


def modelo(nombre: str, n: int) -> float:
    """Función de complejidad de cada estrategia (sin constante).

    Args:
        nombre: estrategia.
        n: horas de la serie.

    Returns:
        El valor del modelo.
    """
    if nombre == "Fuerza bruta (actual)":
        return n * (n + 1) * (n + 2) / 6
    if nombre == "Todos los tramos acumulados":
        return n * (n + 1) / 2
    if nombre == "Dividir y vencer":
        return n * math.log2(n)
    return n


def constante(filas: list[Medicion], nombre: str) -> float:
    """Ajusta c en t ≈ c · modelo(n) con la mitad superior de los tamaños.

    Args:
        filas: mediciones.
        nombre: estrategia.

    Returns:
        La constante (s por unidad del modelo).
    """
    puntos = [f for f in filas if f["solucion"] == nombre]
    puntos = puntos[len(puntos) // 2:]
    return sum(f["tiempo_s"] / modelo(nombre, int(f["n"]))
               for f in puntos) / len(puntos)


def formato(segundos: float) -> str:
    """Escribe un tiempo con una unidad legible.

    Args:
        segundos: duración.

    Returns:
        Texto con unidad.
    """
    if segundos < 1:
        return f"{segundos * 1000:.1f} ms"
    if segundos < 120:
        return f"{segundos:.1f} s"
    if segundos < 7_200:
        return f"{segundos / 60:.1f} min"
    if segundos < 2 * 86_400:
        return f"{segundos / 3600:.1f} h"
    if segundos < SEGUNDOS_ANIO:
        return f"{segundos / 86_400:.0f} días"
    return f"{segundos / SEGUNDOS_ANIO:.1f} años"


def grafica(filas: list[Medicion], campo: str, escala: float,
            etiqueta_y: str, titulo: str, archivo: str) -> None:
    """Dibuja las cuatro estrategias en los mismos ejes (log-log).

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
        elegidas = [f for f in filas if f["solucion"] == nombre]
        ax.plot([f["n"] for f in elegidas],
                [f[campo] * escala for f in elegidas], label=nombre,
                color=COLORES[nombre], marker=MARCADORES[nombre],
                linewidth=2, markersize=6)
    ax.axvline(N_REAL, color=TINTA_2, linestyle="--", linewidth=1)
    ax.text(N_REAL * 0.8, ax.get_ylim()[1] / 20,
            "10 años (36.000 h)", color=TINTA_2, rotation=90,
            ha="right")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Horas de la serie n (escala logarítmica)")
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


def resumen(filas: list[Medicion]) -> tuple[str, dict]:
    """Factores al duplicar, extrapolación a 40 categorías y energía.

    Args:
        filas: mediciones.

    Returns:
        El texto de resumen.md y el diccionario de resumen.json.
    """
    lineas = ["# Resumen de la medición — saturación de la bodega", "",
              "## Factor al duplicar n", "",
              "| Estrategia | n → 2n | Tiempo × | Operaciones × | "
              "Esperado × |", "|---|---|---|---|---|"]
    for nombre in SOLUCIONES:
        puntos = {f["n"]: f for f in filas if f["solucion"] == nombre}
        for n in sorted(puntos):
            if 2 * n in puntos:
                a, b = puntos[n], puntos[2 * n]
                lineas.append(
                    f"| {nombre} | {n:,} → {2 * n:,} | "
                    f"{b['tiempo_s'] / a['tiempo_s']:.2f} | "
                    f"{b['operaciones'] / a['operaciones']:.2f} | "
                    f"{modelo(nombre, 2 * n) / modelo(nombre, n):.2f} |")
    lineas += ["", "## Una corrida completa: 40 categorías × 36.000 horas",
               "", "| Estrategia | Por categoría | 40 categorías | Fuente | "
               "Energía por corrida (kWh) | Energía al año, 1 corrida "
               "(kWh) |", "|---|---|---|---|---|---|"]
    datos: dict = {"operacion": "4. Saturación de la bodega",
                   "corridas_anio": CORRIDAS_ANIO}
    for etiqueta, categorias in (("real", CATEGORIAS),
                                 ("crecimiento", 2 * CATEGORIAS)):
        datos[etiqueta] = {"categorias": categorias, "n": N_REAL}
    for nombre in SOLUCIONES:
        medida = [f for f in filas
                  if f["solucion"] == nombre and f["n"] == N_REAL]
        if medida:
            por_categoria = float(medida[0]["tiempo_s"])
            fuente = "medido"
        else:
            por_categoria = constante(filas, nombre) * modelo(nombre, N_REAL)
            fuente = "extrapolado"
        total = CATEGORIAS * por_categoria
        kwh = POTENCIA_KW * total / 3600
        lineas.append(f"| {nombre} | {formato(por_categoria)} | "
                      f"{formato(total)} | {fuente} | {kwh:.4g} | "
                      f"{kwh * CORRIDAS_ANIO:.4g} |")
        for etiqueta in ("real", "crecimiento"):
            d = datos[etiqueta]
            d[nombre] = d["categorias"] * por_categoria
    for etiqueta in ("real", "crecimiento"):
        d = datos[etiqueta]
        d["corrida_actual_s"] = d["Fuerza bruta (actual)"]
        d["corrida_propuesta_s"] = d["Kadane"]
        d["kwh_anio_actual"] = POTENCIA_KW * d["corrida_actual_s"] / 3600 \
            * CORRIDAS_ANIO
        d["kwh_anio_propuesta"] = POTENCIA_KW * d["corrida_propuesta_s"] / \
            3600 * CORRIDAS_ANIO
    for nombre in ("Fuerza bruta (actual)", "Todos los tramos acumulados",
                   "Dividir y vencer", "Kadane"):
        lineas.append(f"\n* c ({nombre}) = "
                      f"{constante(filas, nombre) * 1e9:.2f} ns por unidad "
                      "del modelo.")
    lineas.append("")
    return "\n".join(lineas), datos


def main() -> None:
    """Corre el experimento, las gráficas y el resumen."""
    CARPETA.mkdir(parents=True, exist_ok=True)
    filas = experimento()
    grafica(filas, "tiempo_s", 1000, "Tiempo medio por categoría (ms, log)",
            "Saturación de la bodega: tiempo frente a las horas de la serie",
            "tiempo_vs_n.png")
    grafica(filas, "operaciones", 1, "Sumas realizadas (conteo, log)",
            "Saturación de la bodega: operaciones frente a las horas",
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
