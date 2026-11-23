"""Genera informe.pdf (y informe.html) a partir del README.md.

Se ejecuta desde la raíz del repositorio con:

    python herramientas/generar_pdf.py

Convierte el README.md a HTML con el paquete ``markdown`` y después usa
Google Chrome, Chromium o Microsoft Edge sin interfaz para imprimirlo a
PDF. Si no encuentra ninguno de esos navegadores, deja informe.html: ábralo
en el navegador y use Imprimir → Guardar como PDF con el nombre
informe.pdf en la raíz del repositorio.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parents[1]
README = RAIZ / "README.md"
HTML = RAIZ / "informe.html"
PDF = RAIZ / "informe.pdf"

ESTILO = """
@page { size: Letter; margin: 18mm 16mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.45; color: #1a1a1a; max-width: 900px; margin: auto; }
h1 { font-size: 20pt; border-bottom: 2px solid #2a78d6; padding-bottom: 4px; }
h2 { font-size: 15pt; border-bottom: 1px solid #ccc; margin-top: 26px;
     page-break-after: avoid; }
h3 { font-size: 12.5pt; margin-top: 20px; page-break-after: avoid; }
h4 { font-size: 11pt; margin-top: 16px; page-break-after: avoid; }
table { border-collapse: collapse; margin: 10px 0; font-size: 9pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 4px 6px; vertical-align: top; }
th { background: #eef3fb; }
img { max-width: 100%; page-break-inside: avoid; display: block;
      margin: 8px auto; }
pre { background: #f5f5f3; padding: 8px; font-size: 8.5pt;
      white-space: pre-wrap; page-break-inside: avoid; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt; }
blockquote { color: #555; border-left: 3px solid #ccc; margin-left: 0;
             padding-left: 10px; }
"""

NAVEGADORES = [
    "google-chrome", "chrome", "chromium", "chromium-browser", "msedge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def escribir_html() -> None:
    """Convierte el README.md en informe.html con estilo para imprimir."""
    texto = README.read_text(encoding="utf-8")
    cuerpo = markdown.markdown(
        texto, extensions=["tables", "fenced_code", "toc", "sane_lists"])
    HTML.write_text(
        "<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'>"
        f"<title>Informe técnico — Caso 3</title><style>{ESTILO}</style>"
        f"</head><body>{cuerpo}</body></html>", encoding="utf-8")


def buscar_navegador() -> str | None:
    """Busca un navegador basado en Chromium instalado.

    Returns:
        La ruta del ejecutable, o None si no hay ninguno.
    """
    for candidato in NAVEGADORES:
        ruta = shutil.which(candidato)
        if ruta:
            return ruta
        if Path(candidato).exists():
            return candidato
    return None


def imprimir_pdf(navegador: str) -> bool:
    """Imprime informe.html a informe.pdf con el navegador sin interfaz.

    Args:
        navegador: ruta del ejecutable.

    Returns:
        True si el PDF quedó creado.
    """
    if PDF.exists():
        PDF.unlink()
    comando = [navegador, "--headless", "--disable-gpu", "--no-sandbox",
               "--no-pdf-header-footer", "--print-to-pdf-no-header",
               f"--print-to-pdf={PDF}", HTML.as_uri()]
    subprocess.run(comando, capture_output=True, timeout=180, check=False)
    return PDF.exists() and PDF.stat().st_size > 0


def main() -> None:
    """Genera el HTML y, si se puede, el PDF."""
    escribir_html()
    print(f"HTML generado: {HTML}")
    navegador = buscar_navegador()
    if navegador and imprimir_pdf(navegador):
        print(f"PDF generado: {PDF}")
        return
    print("No se encontró Chrome/Edge o no se pudo imprimir. Abra "
          "informe.html en el navegador y use Imprimir → Guardar como PDF "
          "con el nombre informe.pdf en la raíz del repositorio.")
    sys.exit(1)


if __name__ == "__main__":
    main()
