"""Contrato con el generador web (D:\\generador-web): revisa que el kit siga exponiendo lo que el panel usa.

El panel no importa código del kit: ejecuta sus scripts y lee algunos archivos. Si algo de esto cambia de
forma, el panel se rompe sin avisar. Este script lo detecta.

Lo que el panel usa del kit:
  - tools/render_editor.py --list   → líneas «<id>  <ancho>x<alto>  <nombre>»; y render_editor.py <jobs.json>
  - tools/montaje.py <guion.json>   → y lee sin ejecutar (ast.literal_eval) SIZE, CAPA, VENTANA, TEXTO_EN_MARCO, TONEMAP
  - tools/validar.py (sale 0/1) y tools/video.py
  - editor/brand-data.js, primitives.js, templates.js (window.TPDTemplates) para formularios y vista previa
  - editor/index.html?embed=1&t=<id>&d=<json base64url> para la vista previa de las capas de video
  - carpetas públicas en modo lectura: editor/, brand/, assets/, tools/fonts/

Uso:
  python -I tools/generador.py          # informe legible; sale con 1 si hay errores
  python -I tools/generador.py --json   # lo mismo en JSON (lo pide el panel en /api/estado)
"""
import ast, json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from render_editor import BROWSER, template_sizes  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LIST_LINE = re.compile(r"^(\S+)\s+(\d+x\d+)\s+(.+)$")   # mismo patrón que server.py del panel
MONTAJE_CONSTS = {"SIZE": dict, "CAPA": dict, "VENTANA": dict, "TEXTO_EN_MARCO": (set, list, tuple), "TONEMAP": str}
FILES = ["tools/render_editor.py", "tools/montaje.py", "tools/validar.py", "tools/video.py",
         "editor/index.html", "editor/app.js", "editor/brand-data.js", "editor/primitives.js", "editor/templates.js"]
PUBLIC = ["editor", "brand", "assets", "tools/fonts"]


def check():
    errors, warnings = [], []
    for f in FILES:
        if not (ROOT / f).is_file():
            errors.append(f"Falta {f}")
    for d in PUBLIC:
        if not (ROOT / d).is_dir():
            errors.append(f"Falta la carpeta {d}/")

    # Lista de plantillas, tal como la lee el panel
    ids = set()
    proc = subprocess.run([sys.executable, "-I", "-X", "utf8", str(ROOT / "tools/render_editor.py"), "--list"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    for line in proc.stdout.splitlines():
        m = LIST_LINE.match(line)
        if m:
            ids.add(m.group(1))
    if proc.returncode or not ids:
        errors.append("render_editor.py --list no devolvió plantillas con el formato «id  ANCHOxALTO  nombre»")
    elif len(ids) != len(template_sizes()):
        warnings.append(f"--list muestra {len(ids)} plantillas, templates.js define {len(template_sizes())}")

    # Constantes de montaje.py (el panel las lee con ast.literal_eval, sin ejecutar el script)
    consts = {}
    try:
        for node in ast.parse((ROOT / "tools/montaje.py").read_text(encoding="utf-8")).body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                try:
                    consts[node.targets[0].id] = ast.literal_eval(node.value)
                except ValueError:
                    pass
    except (OSError, SyntaxError) as exc:
        errors.append(f"No se pudo leer montaje.py: {exc}")
    for name, kind in MONTAJE_CONSTS.items():
        if name not in consts:
            errors.append(f"montaje.py: {name} ya no es un literal de nivel superior")
        elif not isinstance(consts[name], kind):
            errors.append(f"montaje.py: {name} cambió de tipo ({type(consts[name]).__name__})")
    for key, tid in consts.get("CAPA", {}).items():
        if not (isinstance(key, tuple) and len(key) == 2 and key[0] in ("v", "h")):
            errors.append(f"montaje.py: clave de CAPA inesperada {key!r} (se espera ('v'|'h', estilo))")
        elif ids and tid not in ids:
            errors.append(f"montaje.py: CAPA {key} usa la plantilla «{tid}», que no existe")
    for name, win in consts.get("VENTANA", {}).items():
        if not (isinstance(win, tuple) and len(win) == 4):
            errors.append(f"montaje.py: VENTANA[{name!r}] debe ser (ancho, alto, x, y)")

    # Editor: global de plantillas y modo embed
    js = (ROOT / "editor/templates.js").read_text(encoding="utf-8") if (ROOT / "editor/templates.js").is_file() else ""
    if "window.TPDTemplates" not in js:
        errors.append("editor/templates.js ya no publica window.TPDTemplates")
    app = (ROOT / "editor/app.js").read_text(encoding="utf-8") if (ROOT / "editor/app.js").is_file() else ""
    if not all(s in app for s in ('get("embed")', 'get("t")', 'get("d")')):
        errors.append("editor/app.js ya no acepta ?embed=1&t=&d= (vista previa de capas en el panel)")

    # Programas externos (no son del kit, pero sin ellos el panel no genera nada)
    if not BROWSER:
        errors.append("No se encontró Edge ni Chrome: no se pueden generar imágenes")
    for exe in ("ffmpeg", "ffprobe"):
        if not shutil.which(exe):
            warnings.append(f"No se encontró {exe}: los videos no funcionarán")
    return {"ok": not errors, "kit": str(ROOT), "plantillas": len(ids), "estilos_video": len(consts.get("CAPA", {})),
            "errores": errors, "avisos": warnings}


def main():
    result = check()
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Contrato con el generador web · {result['plantillas']} plantillas · {result['estilos_video']} estilos de video")
        for e in result["errores"]:
            print(f"  ERROR  {e}")
        for w in result["avisos"]:
            print(f"  aviso  {w}")
        print("OK" if result["ok"] else f"{len(result['errores'])} errores")
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
