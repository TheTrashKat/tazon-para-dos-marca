"""Exporta archivos de entrega a partir de los SVG.

  assets/logo/png/*.png     logos con fondo transparente (para correo, Word, Canva…)
  assets/logo/favicon.ico   16/32/48/256 px
  impresion/*.pdf           piezas de imprenta al tamaño físico real

Requiere Edge o Chrome (headless) y Pillow.  Uso:  python -I tools/export.py
"""
import pathlib, shutil, subprocess, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            shutil.which("google-chrome") or "", shutil.which("chromium") or "",
            shutil.which("chromium-browser") or ""]
BROWSER = next((b for b in BROWSERS if b and pathlib.Path(b).exists()), None)
PROFILE = pathlib.Path(tempfile.mkdtemp(prefix="tpd-export-"))  # perfil nuevo por ejecución

# Piezas de imprenta: (svg, ancho_mm, alto_mm)
PRINT = [
    ("aplicaciones/tarjeta_frente.svg", 85, 55),
    ("aplicaciones/tarjeta_reverso.svg", 85, 55),
    ("aplicaciones/letrero_horario_a4.svg", 210, 297),
    ("aplicaciones/ficha_personaje_a4.svg", 210, 297),
    ("aplicaciones/certificado_taller.svg", 297, 210),
    ("aplicaciones/stickers.svg", 200, 200),
    ("plantillas/pancarta_80x180.svg", 800, 1800),
]


def run(args, target):
    """Ejecuta el navegador headless; reintenta porque Edge a veces sale con código != 0."""
    target = pathlib.Path(target)
    target.unlink(missing_ok=True)
    for _ in range(3):
        subprocess.run([BROWSER, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--user-data-dir={PROFILE}", *args],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Edge en Windows puede devolver el control antes de terminar de escribir.
        for _ in range(60):
            if target.exists() and target.stat().st_size > 0:
                time.sleep(0.3)
                return
            time.sleep(0.25)
    raise RuntimeError(f"No se pudo generar {target}")


def logos_png():
    import re
    out = ROOT / "assets/logo/png"
    out.mkdir(parents=True, exist_ok=True)
    for svg in sorted((ROOT / "assets/logo").glob("*.svg")):
        head = svg.read_text(encoding="utf-8")[:300]
        m = re.search(r'width="(\d+)" height="(\d+)"', head)
        w, h = (int(m.group(1)), int(m.group(2))) if m else (512, 512)
        if svg.stem == "favicon":
            w = h = 256
        png = out / f"{svg.stem}.png"
        html = pathlib.Path(tempfile.gettempdir()) / f"tpd_{svg.stem}.html"
        html.write_text(f'<html><body style="margin:0;background:transparent">'
                        f'<img src="{svg.as_uri()}" style="width:{w}px;height:{h}px;display:block"></body></html>', encoding="utf-8")
        run(["--default-background-color=00000000", f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()], png)
        print("  ", png.relative_to(ROOT))


def favicon_ico():
    from PIL import Image
    src = ROOT / "assets/logo/png/favicon.png"
    Image.open(src).save(ROOT / "assets/logo/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
    print("   assets/logo/favicon.ico")


def pdfs():
    out = ROOT / "impresion"
    out.mkdir(exist_ok=True)
    for rel, wmm, hmm in PRINT:
        svg = ROOT / rel
        body = svg.read_text(encoding="utf-8")
        body = body.replace("<svg ", '<svg preserveAspectRatio="xMidYMid slice" ', 1)
        html = pathlib.Path(tempfile.gettempdir()) / f"tpd_print_{svg.stem}.html"
        html.write_text(
            "<!doctype html><html><head><meta charset='utf-8'><style>"
            f"@page{{size:{wmm}mm {hmm}mm;margin:0}}html,body{{margin:0;padding:0}}"
            f"svg{{display:block;width:{wmm}mm;height:{hmm}mm}}</style></head><body>{body}</body></html>",
            encoding="utf-8")
        pdf = out / f"{svg.stem}.pdf"
        run(["--no-pdf-header-footer", "--print-to-pdf-no-header", "--virtual-time-budget=6000",
             f"--print-to-pdf={pdf}", html.as_uri()], pdf)
        print("  ", pdf.relative_to(ROOT), f"({wmm}x{hmm} mm)")


if __name__ == "__main__":
    if not BROWSER:
        raise SystemExit("No se encontró Edge ni Chrome.")
    logos_png()
    favicon_ico()
    pdfs()
