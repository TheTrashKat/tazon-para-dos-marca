"""Renderiza plantillas del editor web (editor/) a PNG desde un JSON, sin interfaz.

Pensado para automatizar con IA: la IA escribe el contenido en JSON y este script produce las imágenes.

Uso:
  python -I tools/render_editor.py contenido.json            # un objeto o una lista de objetos
  python -I tools/render_editor.py --list                     # muestra plantillas y campos

Formato de cada objeto:
  { "template": "evento_vertical",
    "values":   { "linea1": "ESTE SÁBADO", "dia": "Sábado 18 de octubre" },
    "output":   "salida/evento-18-oct.png" }          # opcional (por defecto: salida/<template>.png)

Los campos que no se indiquen usan el valor por defecto de la plantilla.
Requiere Edge o Chrome. Levanta un servidor local temporal para que el editor cargue sus fuentes.
"""
import base64, functools, http.server, json, pathlib, re, shutil, socketserver, subprocess, sys, tempfile, threading, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("msedge") or ""]
BROWSER = next((b for b in BROWSERS if b and pathlib.Path(b).exists()), None)


def template_sizes():
    """Lee id, tamaño de salida y campos de editor/templates.js (sin ejecutar JS)."""
    src = (ROOT / "editor/templates.js").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'id: "([^"]+)", name: "([^"]+)".*?w: (\d+), h: (\d+)(?:, out: \{ w: (\d+), h: (\d+) \})?', src, re.S):
        tid, name, w, h, ow, oh = m.groups()
        out[tid] = {"name": name, "w": int(ow or w), "h": int(oh or h)}
    return out


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    httpd = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render(job, port, sizes):
    tid = job["template"]
    if tid not in sizes:
        raise SystemExit(f"Plantilla desconocida: {tid}. Usa --list.")
    w, h = sizes[tid]["w"], sizes[tid]["h"]
    data = base64.urlsafe_b64encode(json.dumps(job.get("values", {}), ensure_ascii=False).encode("utf-8")).decode().rstrip("=")
    url = f"http://127.0.0.1:{port}/editor/index.html?embed=1&t={tid}&d={data}"
    out = pathlib.Path(job.get("output") or f"salida/{tid}.png")
    if not out.is_absolute():
        out = pathlib.Path.cwd() / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    profile = tempfile.mkdtemp(prefix="tpd-editor-")
    for _ in range(3):
        subprocess.run([BROWSER, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={profile}",
                        "--virtual-time-budget=8000", f"--window-size={w},{h}", f"--screenshot={out}", url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if out.exists() and out.stat().st_size > 0:
                time.sleep(0.3)
                print(f"  {out}  ({w}x{h})")
                return
            time.sleep(0.25)
    raise RuntimeError(f"No se pudo generar {out}")


def main():
    sizes = template_sizes()
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    if sys.argv[1] == "--list":
        src = (ROOT / "editor/templates.js").read_text(encoding="utf-8")
        for tid, s in sizes.items():
            print(f"{tid:24} {s['w']}x{s['h']}  {s['name']}")
        print("\nCampos: ver 'fields' de cada plantilla en editor/templates.js o editor/README.md")
        return
    if not BROWSER:
        raise SystemExit("No se encontró Edge ni Chrome.")
    jobs = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    jobs = jobs if isinstance(jobs, list) else [jobs]
    httpd = serve()
    try:
        for job in jobs:
            render(job, httpd.server_address[1], sizes)
    finally:
        httpd.shutdown()


if __name__ == "__main__":
    main()
