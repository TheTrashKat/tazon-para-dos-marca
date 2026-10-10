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
Los campos de foto aceptan una ruta a una imagen local (jpg/png/webp), relativa a la carpeta del JSON o absoluta.
Las plantillas transparentes (capas para video) se exportan como PNG con canal alfa.
En computador usa Edge o Chrome. En Termux/Android usa Node + librsvg para
renderizar sin depender de un navegador gráfico. En ambos casos levanta un
servidor local temporal para que el editor cargue sus fuentes.
"""
import base64, functools, http.server, json, os, pathlib, platform, re, shutil, socketserver, subprocess, sys, tempfile, threading, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            shutil.which("google-chrome") or "", shutil.which("chromium") or "",
            shutil.which("chromium-browser") or "", shutil.which("msedge") or ""]
BROWSER = next((b for b in BROWSERS if b and pathlib.Path(b).exists()), None)


def browser_command(*args):
    """Construye el comando headless, incluyendo los ajustes necesarios en Termux."""
    command = [BROWSER, "--headless=new", "--disable-gpu", "--hide-scrollbars"]
    # El Chromium de Termux intenta lanzar procesos hijos con /proc/self/exe.
    # Android no permite que esos hijos carguen libtermux-exec.so, por lo que
    # el servicio de red se reinicia indefinidamente. Un solo proceso evita
    # ese problema y permite renderizar las plantillas desde Termux.
    if os.environ.get("TERMUX_VERSION") or platform.system() == "Android":
        command.extend([
            "--no-sandbox", "--single-process", "--no-zygote",
            "--disable-dev-shm-usage", "--disable-crash-reporter",
            "--disable-breakpad", "--disable-features=NetworkService",
        ])
    return command + list(args)


def template_sizes():
    """Lee id, tamaño de salida y campos de editor/templates.js (sin ejecutar JS)."""
    src = (ROOT / "editor/templates.js").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'id: "([^"]+)",[^\n]*?name: "([^"]+)".*?w: (\d+), h: (\d+)(?:, out: \{ w: (\d+), h: (\d+) \})?', src, re.S):
        tid, name, w, h, ow, oh = m.groups()
        out[tid] = {"name": name, "w": int(ow or w), "h": int(oh or h)}
    return out


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    # El editor solicita en paralelo sus scripts, estilos y fuentes. Un
    # TCPServer de una sola conexión puede dejar Chromium/Termux esperando.
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
TMP = ROOT / "editor" / "_tmp"
ANDROID = bool(os.environ.get("TERMUX_VERSION")) or platform.system() == "Android"


def stage_images(values, base):
    """Copia las fotos locales a editor/_tmp/ para que el editor pueda cargarlas por URL relativa."""
    out = {}
    for k, v in values.items():
        if isinstance(v, str) and not v.startswith(("data:", "http")) and pathlib.Path(v).suffix.lower() in IMG_EXT:
            src = pathlib.Path(v) if pathlib.Path(v).is_absolute() else base / v
            if not src.exists():
                raise SystemExit(f"No existe la imagen: {src}")
            TMP.mkdir(exist_ok=True)
            dst = TMP / f"{abs(hash(str(src.resolve())))}{src.suffix.lower()}"
            shutil.copyfile(src, dst)
            v = f"_tmp/{dst.name}"
        out[k] = v
    return out


def render(job, port, sizes, base=pathlib.Path.cwd()):
    tid = job["template"]
    if tid not in sizes:
        raise SystemExit(f"Plantilla desconocida: {tid}. Usa --list.")
    w, h = sizes[tid]["w"], sizes[tid]["h"]
    data = base64.urlsafe_b64encode(json.dumps(stage_images(job.get("values", {}), base), ensure_ascii=False).encode("utf-8")).decode().rstrip("=")
    url = f"http://127.0.0.1:{port}/editor/index.html?embed=1&t={tid}&d={data}"
    out = pathlib.Path(job.get("output") or f"salida/{tid}.png")
    if not out.is_absolute():
        out = pathlib.Path.cwd() / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    profile = tempfile.mkdtemp(prefix="tpd-editor-")
    for _ in range(3):
        subprocess.run(browser_command(f"--user-data-dir={profile}",
                        "--virtual-time-budget=8000", "--default-background-color=00000000",
                        f"--window-size={w},{h}", f"--screenshot={out}", url),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
        for _ in range(60):
            if out.exists() and out.stat().st_size > 0:
                time.sleep(0.3)
                print(f"  {out}  ({w}x{h})")
                return
            time.sleep(0.25)
    raise RuntimeError(f"No se pudo generar {out}")


def render_android(job, sizes, base):
    """Renderiza sin Chromium, usando Node + librsvg disponibles en Termux."""
    tid = job["template"]
    if tid not in sizes:
        raise SystemExit(f"Plantilla desconocida: {tid}. Usa --list.")
    w, h = sizes[tid]["w"], sizes[tid]["h"]
    out = pathlib.Path(job.get("output") or f"salida/{tid}.png")
    if not out.is_absolute():
        out = pathlib.Path.cwd() / out
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        handle.write(json.dumps(job, ensure_ascii=False))
        job_file = pathlib.Path(handle.name)
    try:
        subprocess.run([shutil.which("node") or "node", str(ROOT / "tools/render_node.js"),
                        str(job_file), str(base), str(out), str(w), str(h)], check=True, timeout=90)
    finally:
        job_file.unlink(missing_ok=True)
    if not out.exists() or out.stat().st_size == 0:
        raise RuntimeError(f"No se pudo generar {out}")
    print(f"  {out}  ({w}x{h})")


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
    jobs_file = pathlib.Path(sys.argv[1]).resolve()
    jobs = json.loads(jobs_file.read_text(encoding="utf-8"))
    jobs = jobs if isinstance(jobs, list) else [jobs]
    if ANDROID:
        for job in jobs:
            render_android(job, sizes, jobs_file.parent)
        return
    if not BROWSER:
        raise SystemExit("No se encontró Edge ni Chrome.")
    httpd = serve()
    try:
        for job in jobs:
            render(job, httpd.server_address[1], sizes, jobs_file.parent)
    finally:
        httpd.shutdown()
        shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    main()
