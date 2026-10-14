"""Modo oscuro (Tinieblas) dentro del kit de marca: trae la sub-marca desde su propio kit.

La fuente de verdad sigue en D:/tazon-para-dos-tinieblas (https://thetrashkat.github.io/tazon-para-dos-tinieblas/).
Este script copia aquí lo necesario para que el kit de Tazón esté completo con su modo oscuro:

  brand/tinieblas/    tokens.css · tokens.json · brand.json · tema-tinieblas.css · tema-tinieblas-pergamino.css
  assets/logo/tinieblas/       logos recoloreados (sello, horizontal, apilado, mascota, favicon)
  assets/elementos/tinieblas/  luna, niebla, humedal, greca, d20 agrietado, zarpazo…
  assets/iconos/tinieblas/     íconos nuevos del modo oscuro + sprite

    python -I tools/tinieblas.py
"""
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
FUENTE = Path(r"D:\tazon-para-dos-tinieblas")

COPIAS = [
    (FUENTE / "brand", AQUI / "brand" / "tinieblas", ["tokens.css", "tokens.json", "brand.json"]),
    (FUENTE, AQUI / "brand" / "tinieblas", ["tema-tinieblas.css", "tema-tinieblas-pergamino.css"]),
    (FUENTE / "assets" / "logo", AQUI / "assets" / "logo" / "tinieblas", None),
    (FUENTE / "assets" / "elementos", AQUI / "assets" / "elementos" / "tinieblas", None),
    (FUENTE / "assets" / "iconos", AQUI / "assets" / "iconos" / "tinieblas", None),
]
LEEME = """# Modo oscuro · Tinieblas (copia)

Copia sincronizada de la sub-marca **Tazón para Dos · Tinieblas**. No edites estos archivos aquí: la fuente
de verdad es el kit Tinieblas (`D:\\tazon-para-dos-tinieblas`, https://thetrashkat.github.io/tazon-para-dos-tinieblas/).
Para actualizar la copia: `python -I tools/tinieblas.py`.
"""


def main():
    if not FUENTE.exists():
        raise SystemExit(f"No encuentro el kit Tinieblas en {FUENTE}")
    n = 0
    for origen, destino, nombres in COPIAS:
        destino.mkdir(parents=True, exist_ok=True)
        archivos = [origen / x for x in nombres] if nombres else sorted(origen.glob("*.svg"))
        for f in archivos:
            if f.exists():
                shutil.copy2(f, destino / f.name)
                n += 1
    (AQUI / "brand" / "tinieblas" / "LEEME.md").write_text(LEEME, encoding="utf-8")
    print(f"Tinieblas: {n} archivos copiados al kit de marca")


if __name__ == "__main__":
    main()
