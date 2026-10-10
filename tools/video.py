"""Genera el kit de video de Tazón para Dos en video/.

  video/intro_9x16.mp4 · intro_16x9.mp4     logo que aparece con rebote (2,5 s)
  video/cierre_9x16.mp4 · cierre_16x9.mp4   tarjeta final con zoom suave (4 s)
  video/capas/*.png                          capas transparentes para poner encima del video
  video/portadas/*.png                       tarjetas finales en imagen fija

Requiere ffmpeg (winget install Gyan.FFmpeg), Pillow y Edge/Chrome.
Uso:  python -I tools/video.py
Los videos no llevan audio: agrega la música o el sonido en tu editor de video.
"""
import glob, json, os, pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "video"
TOKENS = json.loads((ROOT / "brand/tokens.json").read_text(encoding="utf-8"))
TEAL = TOKENS["color"]["teal"]["value"]
INK = TOKENS["color"]["ink"]["value"]


def find_ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    hits = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\**\bin\ffmpeg.exe"), recursive=True)
    if hits:
        return hits[0]
    raise SystemExit("No se encontró ffmpeg. Instálalo con: winget install Gyan.FFmpeg")


FFMPEG = find_ffmpeg()


def ff(*args):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *args], check=True)


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def dotted_background(w, h, path):
    """Fondo turquesa con el patrón de puntos de la marca."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (w, h), hex_rgb(TEAL))
    dot = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(dot)
    ink = hex_rgb(INK) + (int(255 * 0.10),)
    for y in range(11, h, 22):
        for x in range(11, w, 22):
            d.ellipse((x - 1.6, y - 1.6, x + 1.6, y + 1.6), fill=ink)
    img.paste(dot, (0, 0), dot)
    img.save(path)


def render_editor(jobs, workdir):
    jf = workdir / "jobs.json"
    jf.write_text(json.dumps(jobs, ensure_ascii=False), encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(ROOT / "tools/render_editor.py"), str(jf)], cwd=workdir, check=True,
                   stdout=subprocess.DEVNULL)


def intro(w, h, logo, out, work):
    bg = work / f"bg_{w}x{h}.png"
    dotted_background(w, h, bg)
    base = int(min(w, h) * (0.86 if w < h else 0.62))       # ancho del logotipo apilado
    # Rebote: crece de 40 % a 115 % y se asienta en 100 %
    s = "if(lt(t,0.35),0.4+0.75*t/0.35,if(lt(t,0.55),1.15-0.15*(t-0.35)/0.2,1))"
    vf = (f"[1:v]format=rgba,scale=w='trunc({base}*{s}/2)*2':h=-2:eval=frame,"
          f"fade=t=in:st=0:d=0.25:alpha=1[logo];"
          f"[0:v][logo]overlay=x='(W-w)/2':y='(H-h)/2':eval=frame,"
          f"fade=t=out:st=2.15:d=0.35,format=yuv420p[v]")
    ff("-loop", "1", "-t", "2.5", "-i", str(bg), "-loop", "1", "-t", "2.5", "-i", str(logo),
       "-filter_complex", vf, "-map", "[v]", "-r", "30", "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", str(out))


def outro(card, w, h, out):
    # Zoom suave de 106 % a 100 % (se escala ×2 antes para evitar temblores) y fundidos
    vf = (f"scale={w * 2}:{h * 2},zoompan=z='max(1.06-0.0005*on,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d=120:s={w}x{h}:fps=30,fade=t=in:st=0:d=0.4,fade=t=out:st=3.6:d=0.4,format=yuv420p")
    ff("-loop", "1", "-i", str(card), "-vf", vf, "-t", "4", "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", str(out))


def main():
    for sub in ("", "capas", "portadas"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    work = pathlib.Path(tempfile.mkdtemp(prefix="tpd-video-"))
    jobs = [
        {"template": "tarjeta_final_v", "output": str(OUT / "portadas/tarjeta_final_9x16.png")},
        {"template": "tarjeta_final_h", "output": str(OUT / "portadas/tarjeta_final_16x9.png")},
        {"template": "overlay_reel", "output": str(OUT / "capas/marca_reel_9x16.png")},
        {"template": "tercio_inferior_h", "output": str(OUT / "capas/rotulo_nombre_16x9.png")},
        {"template": "tercio_inferior_v", "output": str(OUT / "capas/rotulo_nombre_9x16.png")},
        {"template": "guia_zonas", "output": str(OUT / "capas/guia_zonas_seguras_9x16.png")},
        {"template": "marco_video", "output": str(OUT / "capas/marco_video_9x16.png")},
        {"template": "overlay_video_h", "output": str(OUT / "capas/marca_video_16x9.png")},
    ]
    print("Renderizando tarjetas y capas…")
    render_editor(jobs, work)
    logo = ROOT / "assets/logo/png/logotipo-apilado.png"
    if not logo.exists():
        raise SystemExit("Falta assets/logo/png/logotipo-apilado.png: ejecuta antes tools/export.py")
    print("Generando videos…")
    intro(1080, 1920, logo, OUT / "intro_9x16.mp4", work)
    intro(1920, 1080, logo, OUT / "intro_16x9.mp4", work)
    outro(OUT / "portadas/tarjeta_final_9x16.png", 1080, 1920, OUT / "cierre_9x16.mp4")
    outro(OUT / "portadas/tarjeta_final_16x9.png", 1920, 1080, OUT / "cierre_16x9.mp4")
    for p in sorted(OUT.rglob("*.*")):
        print(f"   {p.relative_to(ROOT)}  ({p.stat().st_size // 1024} KB)")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
