"""Valida todas las plantillas del editor dos veces: automática y visual.

1) Validación automática: abre editor/validar.html en Edge/Chrome sin interfaz. Cada plantilla se pinta
   con sus valores por defecto y con textos largos («estrés»), y se mide cada texto con las fuentes reales.
   - Errores: el render falla, un texto se sale del lienzo, dos textos se enciman, aparece "undefined"/"NaN".
   - Avisos: texto en la zona que tapa la interfaz de Instagram, bajo los botones del Reel,
     pegado al borde o demasiado pequeño.
2) Validación visual (--hojas): renderiza las dos versiones de cada plantilla a PNG y arma hojas de
   contacto en salida/validacion/ para revisarlas a ojo (persona o IA).

Uso:
  python -I tools/validar.py              # solo la validación automática
  python -I tools/validar.py --hojas      # automática + hojas de contacto para la revisión visual
  python -I tools/validar.py --solo id1,id2 [--hojas]

Sale con código 1 si hay errores.
"""
import functools, http.server, json, pathlib, re, socketserver, subprocess, sys, tempfile, threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from render_editor import BROWSER  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def run_checks(timeout=300):
    """Abre validar.html sin interfaz; la página envía los resultados por POST a este servidor."""
    got = {}
    done = threading.Event()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            got["body"] = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8")
            self.send_response(204)
            self.end_headers()
            done.set()

    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Handler, directory=str(ROOT)))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{httpd.server_address[1]}/editor/validar.html?enviar=1"
    profile = tempfile.mkdtemp(prefix="tpd-validar-")
    proc = subprocess.Popen([BROWSER, "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--window-size=1400,1000",
                             "--remote-debugging-port=0", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not done.wait(timeout):
            raise SystemExit("La página de validación no devolvió resultados a tiempo (¿Edge/Chrome disponible?).")
    finally:
        proc.terminate()
        httpd.shutdown()
    data = json.loads(got["body"])
    if isinstance(data, dict) and data.get("fatal"):
        raise SystemExit("La validación falló: " + data["fatal"])
    return data


def contact_sheets(results, outdir):
    """Renderiza normal y estrés de cada plantilla y arma una hoja por grupo."""
    from PIL import Image, ImageDraw
    outdir.mkdir(parents=True, exist_ok=True)
    png = outdir / "png"
    def fname(r):
        caso = r["caso"].replace("estrés", "estres").replace("·", "_")
        return png / f"{r['id']}__{caso}.png"
    jobs = [{"template": r["id"], "values": r["values"], "output": str(fname(r))} for r in results]
    jf = outdir / "jobs.json"
    jf.write_text(json.dumps(jobs, ensure_ascii=False), encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(ROOT / "tools/render_editor.py"), str(jf)], check=True, stdout=subprocess.DEVNULL)
    groups = {}
    for r in results:
        if r["caso"] == "normal":
            groups.setdefault(r["group"], []).append(r["id"])
    sheets = []
    for g, ids in groups.items():
        H = 520
        cells = []
        for tid in ids:
            pair = []
            for caso in ("normal", "estres"):
                im = Image.open(png / f"{tid}__{caso}.png").convert("RGBA")
                bg = Image.new("RGBA", im.size, (128, 128, 128, 255))
                bg.alpha_composite(im)
                pair.append(bg.convert("RGB").resize((max(1, int(im.width * H / im.height)), H)))
            w = pair[0].width + pair[1].width + 10
            cell = Image.new("RGB", (w, H + 34), (247, 242, 232))
            cell.paste(pair[0], (0, 34))
            cell.paste(pair[1], (pair[0].width + 10, 34))
            ImageDraw.Draw(cell).text((4, 8), f"{tid}   (normal | estrés)", fill=(40, 32, 59))
            cells.append(cell)
        cols = 3
        rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
        W = max(sum(c.width for c in row) + 20 * (len(row) + 1) for row in rows)
        sheet = Image.new("RGB", (W, sum(max(c.height for c in row) + 20 for row in rows) + 20), (40, 32, 59))
        y = 20
        for row in rows:
            x = 20
            for c in row:
                sheet.paste(c, (x, y))
                x += c.width + 20
            y += max(c.height for c in row) + 20
        name = outdir / f"hoja_{re.sub(r'[^a-z0-9]+', '_', g.lower())}.jpg"
        sheet.save(name, quality=86)
        sheets.append(name)
    return sheets


def main():
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return
    results = run_checks()
    if "--solo" in args:
        only = set(args[args.index("--solo") + 1].split(","))
        results = [r for r in results if r["id"] in only]
    n_err = n_warn = 0
    for r in results:
        if not r["errors"] and not r["warnings"]:
            continue
        print(f"\n{r['id']} ({r['caso']})")
        for e in r["errors"]:
            print(f"  ERROR  {e}")
        for w in r["warnings"]:
            print(f"  aviso  {w}")
        n_err += len(r["errors"])
        n_warn += len(r["warnings"])
    ids = sorted({r["id"] for r in results})
    print(f"\n{len(ids)} plantillas × 2 casos: {n_err} errores, {n_warn} avisos.")
    if "--hojas" in args:
        sheets = contact_sheets(results, ROOT / "salida/validacion")
        print("Hojas para la revisión visual:")
        for s in sheets:
            print(f"  {s}")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
