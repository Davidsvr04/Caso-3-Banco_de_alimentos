"""Consumo de tiempo y energía del proceso completo: actual frente a propuesta.

Se ejecuta desde la raíz del repositorio, después de las mediciones de las
cuatro operaciones:

    python src/proceso/energia.py

Lee graficas/<operacion>/resumen.json de las operaciones 1, 2 y 4, y
graficas/cargue_vehiculos/mediciones.csv de la operación 3. Produce en
graficas/proceso/: ventana.png, energia_anual.png, resumen.md y
resumen.json.
"""

import csv
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
GRAFICAS = RAIZ / "graficas"
CARPETA = GRAFICAS / "proceso"

POTENCIA_KW = 0.150          # computador de escritorio de la fundación
DIAS_ANIO = 300              # operación 300 días al año
VENTANA_S = 2 * 3600         # 03:00 a 05:00
TIEMPO_REPORTADO_H = 4.5     # lo que tarda hoy la planeación (cliente)
FACTOR_CO2_KG_KWH = 0.220    # factor de emisión del SIN 2024 (UPME)
CO2_POR_KG_ALIMENTO = 2.5    # dato del informe de sostenibilidad del banco
VEHICULOS = 14
LOTES_MAX = 600
CAPACIDAD_MAX = 4000

TINTA, TINTA_2 = "#0b0b0b", "#52514e"
SUPERFICIE, REJILLA = "#fcfcfb", "#e4e3df"
COLOR_ACTUAL, COLOR_PROPUESTA = "#eb6834", "#2a78d6"


def leer_json(operacion: str) -> dict:
    """Lee el resumen.json que dejó la medición de una operación.

    Args:
        operacion: nombre de la carpeta de la operación.

    Returns:
        El diccionario guardado.
    """
    ruta = GRAFICAS / operacion / "resumen.json"
    return json.loads(ruta.read_text(encoding="utf-8"))


def cargue_vehiculos() -> dict:
    """Recalcula la extrapolación de la operación 3 desde sus mediciones.

    Usa las mismas fórmulas de src/cargue_vehiculos/medicion.py:
    t ≈ c · n · (W + 1) para la programación dinámica y t ≈ c · n log2 n
    para la regla por vencimiento, en el peor caso diario (14 vehículos,
    600 lotes y 4.000 kg).

    Returns:
        Tiempos por día, real y con el doble de vehículos.
    """
    ruta = GRAFICAS / "cargue_vehiculos" / "mediciones.csv"
    with open(ruta, encoding="utf-8") as archivo:
        filas = list(csv.DictReader(archivo))
    c_pd = [float(f["tiempo_s"]) / (int(f["n"]) * (int(f["W"]) + 1))
            for f in filas if f["solucion"] == "Programación dinámica"
            and f["experimento"] in ("n_grande", "capacidad")
            and int(f["n"]) >= 100]
    c_venc = [float(f["tiempo_s"]) / (int(f["n"]) * math.log2(int(f["n"])))
              for f in filas if f["solucion"] == "Regla actual (vencimiento)"
              and f["experimento"] == "n_grande" and int(f["n"]) >= 200]
    pd = (sum(c_pd) / len(c_pd)) * LOTES_MAX * (CAPACIDAD_MAX + 1)
    venc = (sum(c_venc) / len(c_venc)) * LOTES_MAX * math.log2(LOTES_MAX)
    resultado = {"operacion": "3. Cargue de los vehículos"}
    for etiqueta, vehiculos in (("real", VEHICULOS),
                                ("crecimiento", 2 * VEHICULOS)):
        resultado[etiqueta] = {
            "vehiculos": vehiculos,
            "dia_actual_s": vehiculos * venc,
            "dia_propuesta_s": vehiculos * pd,
        }
    return resultado


def kwh(segundos: float) -> float:
    """Convierte segundos de cómputo a kWh con la potencia del caso.

    Args:
        segundos: tiempo de ejecución.

    Returns:
        La energía en kWh (kW × h).
    """
    return POTENCIA_KW * segundos / 3600


def formato(segundos: float) -> str:
    """Escribe un tiempo con una unidad legible.

    Args:
        segundos: duración.

    Returns:
        Texto con unidad.
    """
    if segundos < 1:
        return f"{segundos * 1000:.0f} ms"
    if segundos < 120:
        return f"{segundos:.1f} s"
    if segundos < 7200:
        return f"{segundos / 60:.1f} min"
    if segundos < 2 * 86400:
        return f"{segundos / 3600:.1f} h"
    return f"{segundos / 86400:.0f} días"


def construir_tabla() -> tuple[list[dict], dict]:
    """Reúne los tiempos de las cuatro operaciones.

    Returns:
        Las filas por operación y los totales de la ventana.
    """
    op1 = leer_json("consulta_inventario")
    op2 = leer_json("orden_fefo")
    op3 = cargue_vehiculos()
    op4 = leer_json("saturacion_bodega")
    filas = []
    for etiqueta in ("real", "crecimiento"):
        filas += [
            {"escenario": etiqueta, "operacion": "1a. Lotes por vencer "
             "(rango)", "momento": "ventana",
             "actual_s": op1[etiqueta]["ventana_actual_s"],
             "propuesta_s": op1[etiqueta]["ventana_propuesta_s"],
             "veces_anio": DIAS_ANIO},
            {"escenario": etiqueta, "operacion": "1b. Consulta por código",
             "momento": "alistamiento",
             "actual_s": op1[etiqueta]["alistamiento_actual_s"],
             "propuesta_s": op1[etiqueta]["alistamiento_propuesta_s"],
             "veces_anio": DIAS_ANIO},
            {"escenario": etiqueta, "operacion": "2. Ordenamiento FEFO",
             "momento": "ventana",
             "actual_s": op2[etiqueta]["ventana_actual_s"],
             "propuesta_s": op2[etiqueta]["ventana_propuesta_s"],
             "veces_anio": DIAS_ANIO},
            {"escenario": etiqueta, "operacion": "3. Cargue de vehículos",
             "momento": "ventana",
             "actual_s": op3[etiqueta]["dia_actual_s"],
             "propuesta_s": op3[etiqueta]["dia_propuesta_s"],
             "veces_anio": DIAS_ANIO},
            {"escenario": etiqueta, "operacion": "4. Saturación (por "
             "corrida)", "momento": "análisis",
             "actual_s": op4[etiqueta]["corrida_actual_s"],
             "propuesta_s": op4[etiqueta]["corrida_propuesta_s"],
             "veces_anio": op4["corridas_anio"]},
        ]
    for fila in filas:
        fila["kwh_anio_actual"] = kwh(fila["actual_s"]) * fila["veces_anio"]
        fila["kwh_anio_propuesta"] = kwh(fila["propuesta_s"]) * \
            fila["veces_anio"]
    totales = {}
    for etiqueta in ("real", "crecimiento"):
        en_ventana = [f for f in filas
                      if f["escenario"] == etiqueta
                      and f["momento"] == "ventana"]
        totales[etiqueta] = {
            "ventana_actual_s": sum(f["actual_s"] for f in en_ventana),
            "ventana_propuesta_s": sum(f["propuesta_s"] for f in en_ventana),
            "kwh_anio_actual": sum(f["kwh_anio_actual"] for f in filas
                                   if f["escenario"] == etiqueta),
            "kwh_anio_propuesta": sum(f["kwh_anio_propuesta"] for f in filas
                                      if f["escenario"] == etiqueta),
        }
    return filas, totales


def grafica_puntos(filas: list[dict], campo_a: str, campo_p: str,
                   titulo: str, etiqueta_x: str, archivo: str,
                   linea: float | None = None) -> None:
    """Gráfica de puntos: actual frente a propuesta por operación (log).

    Args:
        filas: filas del escenario real.
        campo_a: campo del valor actual.
        campo_p: campo del valor propuesto.
        titulo: título.
        etiqueta_x: rótulo del eje x con unidades.
        archivo: nombre del PNG.
        linea: valor de referencia vertical (por ejemplo, la ventana).
    """
    figura, ax = plt.subplots(figsize=(10, 4.8))
    figura.patch.set_facecolor(SUPERFICIE)
    nombres = [f["operacion"] for f in filas]
    ys = list(range(len(filas)))[::-1]
    for y, fila in zip(ys, filas):
        ax.plot([fila[campo_p], fila[campo_a]], [y, y], color=REJILLA,
                linewidth=3, zorder=1)
    ax.scatter([f[campo_a] for f in filas], ys, color=COLOR_ACTUAL, s=70,
               label="Proceso actual", zorder=2, edgecolor=SUPERFICIE,
               linewidth=2)
    ax.scatter([f[campo_p] for f in filas], ys, color=COLOR_PROPUESTA,
               s=70, marker="D", label="Propuesta", zorder=3,
               edgecolor=SUPERFICIE, linewidth=2)
    if linea is not None:
        ax.axvline(linea, color=TINTA_2, linestyle="--", linewidth=1)
        ax.text(linea / 1.15, ys[0] + 0.35, "ventana de 2 h",
                color=TINTA_2, ha="right")
    ax.set_ylim(ys[-1] - 0.6, ys[0] + 0.7)
    ax.set_yticks(ys)
    ax.set_yticklabels(nombres)
    ax.set_xscale("log")
    ax.set_xlabel(etiqueta_x)
    ax.set_title(titulo, color=TINTA)
    ax.set_facecolor(SUPERFICIE)
    ax.grid(True, axis="x", color=REJILLA, linewidth=0.8)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    figura.tight_layout()
    figura.savefig(CARPETA / archivo, dpi=130, facecolor=SUPERFICIE)
    plt.close(figura)


def resumen(filas: list[dict], totales: dict) -> str:
    """Arma el texto de resumen.md.

    Args:
        filas: filas por operación y escenario.
        totales: totales por escenario.

    Returns:
        El texto Markdown.
    """
    lineas = ["# Resumen del proceso completo", ""]
    for etiqueta in ("real", "crecimiento"):
        lineas += [f"## Escenario {etiqueta}", "",
                   "| Operación | Momento | Actual | Propuesta | kWh/año "
                   "actual | kWh/año propuesta |",
                   "|---|---|---|---|---|---|"]
        for f in filas:
            if f["escenario"] != etiqueta:
                continue
            lineas.append(
                f"| {f['operacion']} | {f['momento']} | "
                f"{formato(f['actual_s'])} | {formato(f['propuesta_s'])} | "
                f"{f['kwh_anio_actual']:.4g} | "
                f"{f['kwh_anio_propuesta']:.4g} |")
        t = totales[etiqueta]
        lineas += ["",
                   f"* Ventana (1a + 2 + 3): actual "
                   f"{formato(t['ventana_actual_s'])} "
                   f"({100 * t['ventana_actual_s'] / VENTANA_S:.1f} % de 2 "
                   f"h); propuesta {formato(t['ventana_propuesta_s'])} "
                   f"({100 * t['ventana_propuesta_s'] / VENTANA_S:.2f} %).",
                   f"* Energía al año (medida y extrapolada): actual "
                   f"{t['kwh_anio_actual']:.1f} kWh; propuesta "
                   f"{t['kwh_anio_propuesta']:.3f} kWh.", ""]
    reportado = kwh(TIEMPO_REPORTADO_H * 3600)
    propuesta = totales["real"]["ventana_propuesta_s"]
    ahorro = (reportado - kwh(propuesta)) * DIAS_ANIO
    co2 = ahorro * FACTOR_CO2_KG_KWH
    lineas += ["## Línea base reportada por el cliente", "",
               f"* La planeación tarda hoy {TIEMPO_REPORTADO_H} h: "
               f"{POTENCIA_KW} kW × {TIEMPO_REPORTADO_H} h = "
               f"{reportado:.3f} kWh por día y "
               f"{reportado * DIAS_ANIO:.1f} kWh al año ({DIAS_ANIO} días).",
               f"* Con la propuesta, la ventana usa {formato(propuesta)}: "
               f"{kwh(propuesta) * DIAS_ANIO:.4f} kWh al año.",
               f"* Ahorro anual frente a la línea base reportada: "
               f"{ahorro:.1f} kWh, unos {ahorro * FACTOR_CO2_KG_KWH:.1f} kg "
               f"de CO₂e con el factor de {FACTOR_CO2_KG_KWH} kg/kWh.",
               f"* Esos {co2:.1f} kg de CO₂e equivalen a "
               f"{co2 / CO2_POR_KG_ALIMENTO:.1f} kg de alimento desechado "
               f"({CO2_POR_KG_ALIMENTO} kg CO₂e por kg).", ""]
    return "\n".join(lineas)


def main() -> None:
    """Calcula la tabla, las gráficas y el resumen del proceso."""
    CARPETA.mkdir(parents=True, exist_ok=True)
    filas, totales = construir_tabla()
    reales = [f for f in filas if f["escenario"] == "real"]
    grafica_puntos([f for f in reales if f["momento"] == "ventana"],
                   "actual_s", "propuesta_s",
                   "Tiempo diario dentro de la ventana de planeación",
                   "Tiempo por día (s, escala logarítmica)", "ventana.png",
                   linea=VENTANA_S)
    grafica_puntos(reales, "kwh_anio_actual", "kwh_anio_propuesta",
                   "Energía al año por operación (150 W)",
                   "kWh al año (escala logarítmica)", "energia_anual.png")
    texto = resumen(filas, totales)
    (CARPETA / "resumen.md").write_text(texto, encoding="utf-8")
    (CARPETA / "resumen.json").write_text(
        json.dumps({"filas": filas, "totales": totales}, indent=2,
                   ensure_ascii=False), encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
