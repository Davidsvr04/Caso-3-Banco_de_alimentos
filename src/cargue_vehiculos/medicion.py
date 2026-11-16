"""Experimentos y gráficas del cargue de los vehículos.

Se ejecuta desde la raíz del repositorio con:

    python src/cargue_vehiculos/medicion.py

Produce en graficas/cargue_vehiculos/:

* tiempo_vs_n.png: tiempo medio frente al número de lotes.
* operaciones_vs_n.png: operaciones elementales frente al número de lotes.
* tiempo_vs_capacidad.png: tiempo de la programación dinámica con n fijo y
  la capacidad W creciente.
* mediciones.csv: todas las mediciones crudas.
* resumen.md: tablas de factores al duplicar, extrapolación y energía, para
  copiar al informe.

Todas las instancias se generan con semilla fija (datos.py) y se usan las
mismas instancias para todas las soluciones en cada tamaño. Solo se
cronometra la ejecución de cada solución, nunca la generación de datos.
"""

import csv
import gc
import math
import time
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

import estrategia  # noqa: E402
import exhaustivo  # noqa: E402
import regla_actual  # noqa: E402
from datos import (  # noqa: E402
    generar_flota, generar_lotes, instancias_pequenas)

Lote = tuple[int, int, int]
Solucion = Callable[[list[Lote], int], tuple[int, list[int]]]

RAIZ = Path(__file__).resolve().parents[2]
CARPETA_GRAFICAS = RAIZ / "graficas" / "cargue_vehiculos"

SEMILLA = 2026
INSTANCIAS = 3          # instancias distintas por tamaño
REPETICIONES = 5        # ejecuciones de cada instancia (se promedian)
REPETICIONES_EXHAUSTIVA = 1

# Experimento 1: tamaños donde la exhaustiva todavía corre (W fijo).
TAMANOS_PEQUENOS = [4, 6, 8, 10, 12, 14, 16, 18, 20]
CAPACIDAD_PEQUENA = 1000
# Experimento 2: solo estrategia y reglas, tamaños mucho mayores (W fijo).
TAMANOS_GRANDES = [50, 100, 200, 300, 400, 600, 800, 1200]
CAPACIDAD_GRANDE = 4000
# Experimento 3: número de lotes fijo y capacidad creciente.
LOTES_FIJOS = 300
CAPACIDADES = [500, 1000, 2000, 4000, 8000, 16000]

# Cifras del caso.
VEHICULOS = 14
LOTES_MAX = 600
LOTES_MIN = 300
CAPACIDAD_MAX = 4000
VENTANA_HORAS = 2.0
POTENCIA_KW = 0.150
DIAS_ANIO = 365
EDAD_UNIVERSO_ANIOS = 1.38e10
SEGUNDOS_ANIO = 365.25 * 24 * 3600

# Colores de la paleta de referencia (modo claro), en orden fijo.
COLORES = {
    "Programación dinámica": "#2a78d6",
    "Exhaustiva": "#eb6834",
    "Regla actual (vencimiento)": "#1baf7a",
    "Voraz por densidad": "#6250d6",
}
MARCADORES = {
    "Programación dinámica": "o",
    "Exhaustiva": "s",
    "Regla actual (vencimiento)": "^",
    "Voraz por densidad": "D",
}
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
SUPERFICIE = "#fcfcfb"
REJILLA = "#e4e3df"

SOLUCIONES: dict[str, tuple[Solucion, Callable[[], None],
                            Callable[[], int]]] = {
    "Programación dinámica": (estrategia.cargar_vehiculo,
                              estrategia.reiniciar_operaciones,
                              estrategia.leer_operaciones),
    "Exhaustiva": (exhaustivo.cargar_exhaustivo,
                   exhaustivo.reiniciar_operaciones,
                   exhaustivo.leer_operaciones),
    "Regla actual (vencimiento)": (regla_actual.cargar_por_vencimiento,
                                   regla_actual.reiniciar_operaciones,
                                   regla_actual.leer_operaciones),
    "Voraz por densidad": (regla_actual.cargar_por_densidad,
                           regla_actual.reiniciar_operaciones,
                           regla_actual.leer_operaciones),
}

Medicion = dict[str, float]


def medir(
    nombre: str, instancias: list[tuple[list[Lote], int]], repeticiones: int
) -> tuple[float, float, list[int]]:
    """Mide una solución sobre un grupo de instancias del mismo tamaño.

    Args:
        nombre: clave de la solución en ``SOLUCIONES``.
        instancias: parejas (lotes, capacidad) ya generadas.
        repeticiones: ejecuciones de cada instancia.

    Returns:
        Tiempo medio por instancia en segundos, operaciones medias por
        instancia y el valor obtenido en cada instancia.
    """
    solucion, reiniciar, leer = SOLUCIONES[nombre]
    tiempos: list[float] = []
    operaciones: list[int] = []
    valores: list[int] = []
    for lotes, capacidad in instancias:
        for repeticion in range(repeticiones):
            gc.collect()
            reiniciar()
            inicio = time.perf_counter()
            valor, _ = solucion(lotes, capacidad)
            fin = time.perf_counter()
            tiempos.append(fin - inicio)
            if repeticion == 0:
                operaciones.append(leer())
                valores.append(valor)
    return (sum(tiempos) / len(tiempos),
            sum(operaciones) / len(operaciones), valores)


def experimento(
    nombres: list[str],
    tamanos: list[int],
    capacidades: list[int],
    semilla_base: int,
) -> list[Medicion]:
    """Mide varias soluciones en una serie de tamaños.

    Args:
        nombres: soluciones a medir.
        tamanos: número de lotes de cada punto.
        capacidades: capacidad de cada punto (misma longitud que tamanos).
        semilla_base: semilla de la serie; cada punto usa una derivada.

    Returns:
        Una medición por punto y solución, con n, W, tiempo y operaciones.
    """
    filas: list[Medicion] = []
    for punto, (n, capacidad) in enumerate(zip(tamanos, capacidades)):
        instancias = [
            (generar_lotes(n, semilla_base + 100 * punto + k), capacidad)
            for k in range(INSTANCIAS)
        ]
        valores_por_solucion: dict[str, list[int]] = {}
        for nombre in nombres:
            repeticiones = (REPETICIONES_EXHAUSTIVA if nombre == "Exhaustiva"
                            else REPETICIONES)
            tiempo, ops, valores = medir(nombre, instancias, repeticiones)
            valores_por_solucion[nombre] = valores
            filas.append({"solucion": nombre, "n": n, "W": capacidad,
                          "tiempo_s": tiempo, "operaciones": ops})
            print(f"  {nombre:28s} n={n:5d} W={capacidad:6d} "
                  f"t={tiempo * 1000:12.3f} ms  ops={ops:14.0f}")
        # Verificación dentro del experimento: misma respuesta óptima.
        if "Exhaustiva" in valores_por_solucion:
            assert (valores_por_solucion["Exhaustiva"]
                    == valores_por_solucion["Programación dinámica"]), n
        optimos = valores_por_solucion["Programación dinámica"]
        for nombre, valores in valores_por_solucion.items():
            assert all(v <= o for v, o in zip(valores, optimos)), nombre
    return filas


def serie(
    filas: list[Medicion], nombre: str, eje: str, campo: str
) -> tuple[list[float], list[float]]:
    """Extrae una serie (x, y) de las mediciones.

    Args:
        filas: mediciones.
        nombre: solución.
        eje: "n" o "W".
        campo: "tiempo_s" u "operaciones".

    Returns:
        Las listas de valores x e y, en el orden en que se midieron.
    """
    xs = [f[eje] for f in filas if f["solucion"] == nombre]
    ys = [f[campo] for f in filas if f["solucion"] == nombre]
    return xs, ys


def estilo_ejes(ax: plt.Axes) -> None:
    """Aplica el estilo común: rejilla tenue y bordes discretos.

    Args:
        ax: ejes de matplotlib.
    """
    ax.set_facecolor(SUPERFICIE)
    ax.grid(True, color=REJILLA, linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(TINTA_SECUNDARIA)
    ax.tick_params(colors=TINTA_SECUNDARIA)
    if ax.get_yscale() == "linear":
        # Miles separados con punto, sin el multiplicador "1e6" del eje.
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", ".")))
    ax.title.set_color(TINTA)
    ax.xaxis.label.set_color(TINTA)
    ax.yaxis.label.set_color(TINTA)


def dibujar(
    ax: plt.Axes, filas: list[Medicion], nombres: list[str], eje: str,
    campo: str, escala_y: float
) -> None:
    """Dibuja varias soluciones en los mismos ejes.

    Args:
        ax: ejes de matplotlib.
        filas: mediciones.
        nombres: soluciones a dibujar.
        eje: "n" o "W".
        campo: "tiempo_s" u "operaciones".
        escala_y: factor para cambiar de unidad (1000 para ms).
    """
    for nombre in nombres:
        xs, ys = serie(filas, nombre, eje, campo)
        ax.plot(xs, [y * escala_y for y in ys], label=nombre,
                color=COLORES[nombre], marker=MARCADORES[nombre],
                linewidth=2, markersize=6)


def grafica_por_n(
    pequenos: list[Medicion], grandes: list[Medicion], campo: str,
    titulo: str, etiqueta_y: str, escala_y: float, archivo: str
) -> None:
    """Gráfica de dos paneles: tamaños pequeños (log) y grandes (lineal).

    Args:
        pequenos: mediciones del experimento 1.
        grandes: mediciones del experimento 2.
        campo: "tiempo_s" u "operaciones".
        titulo: título general.
        etiqueta_y: rótulo del eje y con unidades.
        escala_y: factor de unidad del eje y.
        archivo: nombre del PNG.
    """
    figura, (izq, der) = plt.subplots(1, 2, figsize=(13, 5.2))
    figura.patch.set_facecolor(SUPERFICIE)
    todas = list(SOLUCIONES)
    dibujar(izq, pequenos, todas, "n", campo, escala_y)
    izq.set_yscale("log")
    izq.set_title(f"n pequeño, W = {CAPACIDAD_PEQUENA} kg (eje y logarítmico)")
    izq.set_xlabel("Número de lotes candidatos n (lotes)")
    izq.set_ylabel(etiqueta_y)
    izq.set_xticks(TAMANOS_PEQUENOS)
    sin_exhaustiva = [s for s in todas if s != "Exhaustiva"]
    dibujar(der, grandes, sin_exhaustiva, "n", campo, escala_y)
    der.set_title(f"n grande, W = {CAPACIDAD_GRANDE} kg "
                  "(la exhaustiva ya no termina)")
    der.set_xlabel("Número de lotes candidatos n (lotes)")
    der.set_ylabel(etiqueta_y)
    for ax in (izq, der):
        estilo_ejes(ax)
        ax.legend(frameon=False, labelcolor=TINTA)
    figura.suptitle(titulo, color=TINTA, fontsize=14)
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / archivo, dpi=130,
                   facecolor=SUPERFICIE)
    plt.close(figura)


def grafica_capacidad(capacidad: list[Medicion]) -> None:
    """Tiempo y celdas de la programación dinámica frente a la capacidad.

    Args:
        capacidad: mediciones del experimento 3.
    """
    nombre = "Programación dinámica"
    figura, (izq, der) = plt.subplots(1, 2, figsize=(13, 5.2))
    figura.patch.set_facecolor(SUPERFICIE)
    xs, ys = serie(capacidad, nombre, "W", "tiempo_s")
    izq.plot(xs, [y * 1000 for y in ys], label=nombre,
             color=COLORES[nombre], marker="o", linewidth=2, markersize=6)
    # Recta de referencia Θ(n·W) ajustada al último punto.
    pendiente = ys[-1] / xs[-1]
    izq.plot(xs, [pendiente * x * 1000 for x in xs], linestyle="--",
             color=TINTA_SECUNDARIA, linewidth=1.2,
             label="Referencia lineal en W")
    izq.set_title("Tiempo medio por vehículo")
    izq.set_xlabel("Capacidad del vehículo W (kg)")
    izq.set_ylabel("Tiempo medio (ms)")
    xs, ops = serie(capacidad, nombre, "W", "operaciones")
    der.plot(xs, ops, label=nombre, color=COLORES[nombre], marker="o",
             linewidth=2, markersize=6)
    der.set_title("Celdas de la tabla calculadas")
    der.set_xlabel("Capacidad del vehículo W (kg)")
    der.set_ylabel("Operaciones (celdas calculadas)")
    for ax in (izq, der):
        estilo_ejes(ax)
        ax.legend(frameon=False, labelcolor=TINTA)
    figura.suptitle(f"Mochila 0/1 con n = {LOTES_FIJOS} lotes fijos y "
                    "capacidad creciente", color=TINTA, fontsize=14)
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / "tiempo_vs_capacidad.png", dpi=130,
                   facecolor=SUPERFICIE)
    plt.close(figura)


def factores_duplicar(
    filas: list[Medicion], nombre: str, eje: str
) -> list[tuple[int, int, float, float]]:
    """Calcula cuánto se multiplica tiempo y operaciones al duplicar.

    Args:
        filas: mediciones.
        nombre: solución.
        eje: "n" o "W".

    Returns:
        Tuplas (x, 2x, factor de tiempo, factor de operaciones).
    """
    puntos = {f[eje]: f for f in filas if f["solucion"] == nombre}
    resultado = []
    for x in sorted(puntos):
        if 2 * x in puntos:
            a, b = puntos[x], puntos[2 * x]
            resultado.append((int(x), int(2 * x),
                              b["tiempo_s"] / a["tiempo_s"],
                              b["operaciones"] / a["operaciones"]))
    return resultado


def esperado(nombre: str, eje: str, x: int) -> float:
    """Factor que predice la complejidad al pasar de x a 2x.

    Args:
        nombre: solución.
        eje: "n" o "W".
        x: tamaño inicial.

    Returns:
        El cociente teórico f(2x) / f(x).
    """
    if eje == "W" or nombre == "Programación dinámica":
        return 2.0
    if nombre == "Exhaustiva":
        return 2.0 * 2.0 ** x
    return 2.0 * math.log2(2 * x) / math.log2(x)


def ajustar_constante(
    filas: list[Medicion], nombre: str, costo: Callable[[Medicion], float],
    minimo_n: int = 0
) -> float:
    """Estima la constante c de t ≈ c · costo(n, W) con los puntos grandes.

    Args:
        filas: mediciones.
        nombre: solución.
        costo: función de complejidad evaluada en cada medición.
        minimo_n: se ignoran los puntos con n menor (dominados por ruido).

    Returns:
        La constante media en segundos por unidad de costo.
    """
    cocientes = [f["tiempo_s"] / costo(f) for f in filas
                 if f["solucion"] == nombre and f["n"] >= minimo_n]
    return sum(cocientes) / len(cocientes)


def formato_tiempo(segundos: float) -> str:
    """Escribe un tiempo con la unidad más legible.

    Args:
        segundos: duración en segundos.

    Returns:
        Texto con la unidad.
    """
    if segundos < 1e-3:
        return f"{segundos * 1e6:.1f} µs"
    if segundos < 1:
        return f"{segundos * 1e3:.2f} ms"
    if segundos < 120:
        return f"{segundos:.2f} s"
    if segundos < 7200:
        return f"{segundos / 60:.1f} min"
    if segundos < SEGUNDOS_ANIO:
        return f"{segundos / 3600:.1f} h"
    return f"{segundos / SEGUNDOS_ANIO:.2e} años"


def flota_real() -> dict[str, dict[str, float]]:
    """Corre las soluciones polinomiales sobre un día con el volumen real.

    Returns:
        Por solución: tiempo total del día, valor total y ocupación media.
    """
    flota = generar_flota(SEMILLA)
    resumen: dict[str, dict[str, float]] = {}
    for nombre in ("Programación dinámica", "Regla actual (vencimiento)",
                   "Voraz por densidad"):
        solucion = SOLUCIONES[nombre][0]
        total_t = 0.0
        total_valor = 0
        ocupaciones = []
        for lotes, capacidad in flota:
            gc.collect()
            inicio = time.perf_counter()
            valor, cargados = solucion(lotes, capacidad)
            total_t += time.perf_counter() - inicio
            total_valor += valor
            peso = sum(lotes[i][0] for i in cargados)
            assert peso <= capacidad
            ocupaciones.append(peso / capacidad)
        resumen[nombre] = {
            "tiempo_s": total_t,
            "valor": total_valor,
            "ocupacion": sum(ocupaciones) / len(ocupaciones),
            "ocupacion_min": min(ocupaciones),
        }
    resumen["_flota"] = {
        "lotes": sum(len(lotes) for lotes, _ in flota),
        "celdas": sum(len(lotes) * (c + 1) for lotes, c in flota),
    }
    return resumen


def fallos_reglas(cantidad: int = 1000) -> dict[str, tuple[int, float]]:
    """Cuenta en cuántas instancias pequeñas cada regla no llega al óptimo.

    Args:
        cantidad: número de instancias aleatorias.

    Returns:
        Por regla: número de fallos y la mayor pérdida relativa.
    """
    instancias = instancias_pequenas(cantidad, SEMILLA + 7)
    resultado: dict[str, tuple[int, float]] = {}
    for nombre in ("Regla actual (vencimiento)", "Voraz por densidad"):
        fallos = 0
        peor = 0.0
        for lotes, capacidad in instancias:
            optimo, _ = estrategia.cargar_vehiculo(lotes, capacidad)
            obtenido, _ = SOLUCIONES[nombre][0](lotes, capacidad)
            if obtenido < optimo:
                fallos += 1
                peor = max(peor, (optimo - obtenido) / optimo)
        resultado[nombre] = (fallos, peor)
    return resultado


def escribir_resumen(
    pequenos: list[Medicion], grandes: list[Medicion],
    capacidad: list[Medicion], flota: dict[str, dict[str, float]],
    fallos: dict[str, tuple[int, float]]
) -> str:
    """Arma el texto Markdown con factores, extrapolación y energía.

    Args:
        pequenos: experimento 1.
        grandes: experimento 2.
        capacidad: experimento 3.
        flota: resultado de ``flota_real``.
        fallos: resultado de ``fallos_reglas``.

    Returns:
        El contenido de resumen.md.
    """
    lineas = ["# Resumen de la medición", "",
              "Generado por `medicion.py`; los números cambian un poco en "
              "cada computador.", ""]

    lineas += ["## Factor al duplicar el tamaño", "",
               "| Solución | Experimento | De → a | Tiempo × | "
               "Operaciones × | Esperado × |",
               "|---|---|---|---|---|---|"]
    grupos = [("n pequeño (W = 1000)", pequenos, "n"),
              ("n grande (W = 4000)", grandes, "n"),
              ("W creciente (n = 300)", capacidad, "W")]
    for etiqueta, filas, eje in grupos:
        nombres = sorted({f["solucion"] for f in filas},
                         key=list(SOLUCIONES).index)
        for nombre in nombres:
            for x, x2, ft, fo in factores_duplicar(filas, nombre, eje):
                lineas.append(
                    f"| {nombre} | {etiqueta} | {x} → {x2} | {ft:.2f} | "
                    f"{fo:.2f} | {esperado(nombre, eje, x):.2f} |")
    lineas.append("")

    # Constantes ajustadas a la forma de cada curva.
    c_pd = ajustar_constante(grandes + capacidad, "Programación dinámica",
                             lambda f: f["n"] * (f["W"] + 1), minimo_n=100)
    c_venc = ajustar_constante(grandes, "Regla actual (vencimiento)",
                               lambda f: f["n"] * math.log2(f["n"]), 200)
    c_dens = ajustar_constante(grandes, "Voraz por densidad",
                               lambda f: f["n"] * math.log2(f["n"]), 200)
    c_exh = ajustar_constante(pequenos, "Exhaustiva",
                              lambda f: f["n"] * 2.0 ** f["n"], 14)

    peor_pd = VEHICULOS * c_pd * LOTES_MAX * (CAPACIDAD_MAX + 1)
    peor_venc = VEHICULOS * c_venc * LOTES_MAX * math.log2(LOTES_MAX)
    peor_dens = VEHICULOS * c_dens * LOTES_MAX * math.log2(LOTES_MAX)
    mejor_exh = VEHICULOS * c_exh * LOTES_MIN * 2.0 ** LOTES_MIN
    ventana_s = VENTANA_HORAS * 3600
    n_max_exh = 1
    while c_exh * (n_max_exh + 1) * 2.0 ** (n_max_exh + 1) <= ventana_s:
        n_max_exh += 1

    lineas += ["## Constantes ajustadas", "",
               f"* Programación dinámica: {c_pd * 1e9:.1f} ns por celda "
               "(t ≈ c · n · (W + 1)).",
               f"* Regla por vencimiento: {c_venc * 1e9:.1f} ns por "
               "unidad de n·log2 n.",
               f"* Voraz por densidad: {c_dens * 1e9:.1f} ns por unidad "
               "de n·log2 n.",
               f"* Exhaustiva: {c_exh * 1e9:.2f} ns por unidad de n·2^n.",
               f"* Con la exhaustiva, en toda la ventana de 2 h cabe como "
               f"máximo una ruta de n = {n_max_exh} lotes.", ""]

    filas_extra = [
        ("Programación dinámica", peor_pd),
        ("Regla actual (vencimiento)", peor_venc),
        ("Voraz por densidad", peor_dens),
        ("Exhaustiva (n = 300, el caso más pequeño)", mejor_exh),
    ]
    lineas += ["## Extrapolación al volumen real (peor caso diario)", "",
               "14 vehículos, 600 lotes y W = 4.000 kg cada uno "
               "(exhaustiva: 300 lotes, su caso más favorable).", "",
               "| Solución | Tiempo por día | % de la ventana de 2 h | "
               "Energía por día (kWh) | Energía por año (kWh) |",
               "|---|---|---|---|---|"]
    for nombre, segundos in filas_extra:
        horas = segundos / 3600
        kwh = POTENCIA_KW * horas
        lineas.append(
            f"| {nombre} | {formato_tiempo(segundos)} | "
            f"{100 * segundos / ventana_s:.3g} % | {kwh:.3g} | "
            f"{kwh * DIAS_ANIO:.3g} |")
    anios = mejor_exh / SEGUNDOS_ANIO
    lineas += ["", f"La exhaustiva tardaría {anios:.2e} años, "
               f"{anios / EDAD_UNIVERSO_ANIOS:.2e} veces la edad del "
               "universo.", ""]
    dif_kwh = POTENCIA_KW * (peor_pd - peor_venc) / 3600 * DIAS_ANIO
    lineas += [f"Diferencia anual de energía entre la programación dinámica "
               f"y la regla actual: {dif_kwh:.3g} kWh "
               f"({dif_kwh * 1000:.0f} Wh).", ""]

    lineas += ["## Un día simulado con el volumen real", "",
               f"Flota sintética (semilla {SEMILLA}): {VEHICULOS} vehículos, "
               f"{flota['_flota']['lotes']:.0f} lotes candidatos en total y "
               f"{flota['_flota']['celdas']:.3g} celdas de tabla.", "",
               "| Solución | Tiempo medido del día | Valor nutricional total"
               " | Ocupación media | Ocupación mínima |",
               "|---|---|---|---|---|"]
    optimo_total = flota["Programación dinámica"]["valor"]
    for nombre in ("Programación dinámica", "Regla actual (vencimiento)",
                   "Voraz por densidad"):
        d = flota[nombre]
        lineas.append(
            f"| {nombre} | {formato_tiempo(d['tiempo_s'])} | "
            f"{d['valor']:,.0f} ({100 * d['valor'] / optimo_total:.1f} % "
            f"del óptimo) | {100 * d['ocupacion']:.1f} % | "
            f"{100 * d['ocupacion_min']:.1f} % |")
    lineas.append("")

    lineas += ["## Fallos de las reglas en 1.000 instancias pequeñas", ""]
    for nombre, (cuantos, peor) in fallos.items():
        lineas.append(f"* {nombre}: no llega al óptimo en {cuantos} de 1000;"
                      f" la mayor pérdida fue {100 * peor:.0f} % del óptimo.")
    lineas.append("")
    return "\n".join(lineas)


def guardar_csv(filas: list[Medicion]) -> None:
    """Guarda todas las mediciones crudas.

    Args:
        filas: mediciones de los tres experimentos.
    """
    with open(CARPETA_GRAFICAS / "mediciones.csv", "w", newline="",
              encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo, fieldnames=["experimento", "solucion", "n", "W",
                                 "tiempo_s", "operaciones"])
        escritor.writeheader()
        escritor.writerows(filas)


def main() -> None:
    """Corre los tres experimentos, las gráficas y el resumen."""
    CARPETA_GRAFICAS.mkdir(parents=True, exist_ok=True)
    print("Experimento 1: n pequeño, todas las soluciones")
    pequenos = experimento(list(SOLUCIONES), TAMANOS_PEQUENOS,
                           [CAPACIDAD_PEQUENA] * len(TAMANOS_PEQUENOS),
                           SEMILLA)
    print("Experimento 2: n grande, sin la exhaustiva")
    grandes = experimento(
        [s for s in SOLUCIONES if s != "Exhaustiva"], TAMANOS_GRANDES,
        [CAPACIDAD_GRANDE] * len(TAMANOS_GRANDES), SEMILLA + 10_000)
    print("Experimento 3: n fijo, capacidad creciente")
    capacidad = experimento(["Programación dinámica"],
                            [LOTES_FIJOS] * len(CAPACIDADES), CAPACIDADES,
                            SEMILLA + 20_000)

    grafica_por_n(pequenos, grandes, "tiempo_s",
                  "Cargue de vehículos: tiempo medio frente al número de "
                  "lotes", "Tiempo medio por vehículo (ms)", 1000,
                  "tiempo_vs_n.png")
    grafica_por_n(pequenos, grandes, "operaciones",
                  "Cargue de vehículos: operaciones elementales frente al "
                  "número de lotes", "Operaciones elementales (conteo)", 1,
                  "operaciones_vs_n.png")
    grafica_capacidad(capacidad)

    for nombre, filas in (("n_pequeno", pequenos), ("n_grande", grandes),
                          ("capacidad", capacidad)):
        for fila in filas:
            fila["experimento"] = nombre
    guardar_csv(pequenos + grandes + capacidad)

    print("Día simulado con el volumen real...")
    flota = flota_real()
    fallos = fallos_reglas()
    texto = escribir_resumen(pequenos, grandes, capacidad, flota, fallos)
    (CARPETA_GRAFICAS / "resumen.md").write_text(texto, encoding="utf-8")
    print(texto)
    print(f"Gráficas y resumen guardados en {CARPETA_GRAFICAS}")


if __name__ == "__main__":
    main()
