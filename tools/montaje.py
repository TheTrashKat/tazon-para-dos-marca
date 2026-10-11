"""Monta videos con la identidad de Tazón para Dos a partir de un guion en JSON.

Uso:  python -I tools/montaje.py guion.json

Formato del guion:
{
  "formato": "9x16-marco",          # 9x16-marco (clips horizontales dentro del marco de marca en un Reel)
                                     # 9x16       (clips a pantalla completa vertical)
                                     # 16x9       (YouTube / Facebook)
  "salida": "reel.mp4",              # relativo a la carpeta del guion
  "intro": true, "cierre": true,     # intro y cierre animados del kit (video/)
  "audio": "original",               # original | silencio
  "marco": { "receta": "general", "titulo": "...", "etiqueta": "...", "usuario": "@tazonparados" },   # solo 9x16-marco
  "capa":  { "estilo": "clasico", "etiqueta": "...", "usuario": "@tazonparados", "info": "..." },  # 9x16 y 16x9
            # estilo 9x16: clasico | banda | stickers | marco | editorial | zine | tiktok
            #   tiktok: video a pantalla completa con acercamiento, subtítulos de 1-3 palabras con la palabra
            #   activa en amarillo, marca discreta arriba y "gancho" opcional al inicio (en el nivel principal
            #   del guion o dentro de capa): "gancho": {"linea1": "¿PLAN PARA", "linea2": "EL SÁBADO?"};
            #   cierre según capa.linea (zine | editorial)
            #   capa.subtitulos: karaoke | caja | recorte | pop | editorial
            #   formato lista: en cada segmento "numero": "3", "titulo": "CATAN" (número grande y título arriba)
            #   marco, editorial y zine ponen el clip en una ventana; en editorial y zine el texto de cada
            #   segmento se vuelve el titular (titulo2) y la intro/cierre usan la línea correspondiente
            # estilo 16x9: clasico | banda
  "segmentos": [
    { "clip": "ruta/al/video.mp4", "inicio": 2.0, "duracion": 4.0,
      "texto": "Jugamos en comunidad.",          # opcional
      "encuadre": "centro",                      # qué parte del clip se ve al recortar: izquierda | centro | derecha | 0–1
      "estilo_texto": "tinta",                   # tinta | sol | crema | turquesa | coral
      "rotulo": { "nombre": "...", "rol": "..." } },  # opcional: rótulo de nombre (pedir permiso antes)
    { "foto": "ruta/a/foto.jpg", "duracion": 3.5, "texto": "..." },   # foto fija con paneo suave (sin audio)
    { "separador": { "numero": "02", "titulo": "LA GRABACIÓN", "receta": "podcast" }, "duracion": 2.5 }   # tarjeta de capítulo
  ]
}
Requiere ffmpeg, Edge/Chrome y el kit de video generado (python -I tools/video.py).
"""
import json, pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
sys.path.insert(0, str(ROOT / "tools"))
from video import FFMPEG  # noqa: E402  (reutiliza la búsqueda de ffmpeg)

FFPROBE = str(pathlib.Path(FFMPEG).with_name("ffprobe" + pathlib.Path(FFMPEG).suffix))
SIZE = {"9x16-marco": (1080, 1920), "9x16": (1080, 1920), "16x9": (1920, 1080)}
CAPA = {("v", "clasico"): "overlay_reel", ("v", "banda"): "overlay_reel_banda", ("v", "stickers"): "overlay_reel_stickers",
        ("v", "marco"): "marco_vertical", ("v", "editorial"): "editorial_marco_v", ("v", "zine"): "zine_marco_v",
        ("v", "tiktok"): "overlay_tiktok",
        ("h", "clasico"): "overlay_video_h", ("h", "banda"): "overlay_video_h_banda"}
# Ventana del clip (ancho, alto, x, y) para los estilos con marco
VENTANA = {"marco": (960, 1000, 60, 400), "editorial": (984, 860, 48, 250), "zine": (880, 780, 100, 280)}
# El texto de cada segmento va dentro del marco (no como texto en pantalla aparte)
TEXTO_EN_MARCO = {"editorial", "zine"}
INTRO = {"editorial": "video/intro_editorial_9x16.mp4"}
CIERRE = {"editorial": "video/cierre_editorial_9x16.mp4", "zine": "video/cierre_zine_9x16.mp4"}


def chunks(texto, max_words=3, max_chars=16):
    """Parte el texto en bloques cortos de subtítulo (estilo TikTok)."""
    out, cur = [], []
    for w in str(texto).split():
        if cur and (len(cur) >= max_words or len(" ".join(cur + [w])) > max_chars):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out
ENC = ["-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]


def ff(*args):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *args], check=True)


def has_audio(path):
    out = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return bool(out)


# Videos HDR de celular (HDR10/HDR10+/HLG): convertir a SDR para que no se vean lavados
TONEMAP = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv,"


def is_hdr(path):
    out = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return out.split(",")[0].strip() in ("smpte2084", "arib-std-b67")


def render_overlays(jobs, work):
    if not jobs:
        return
    jf = work / "overlays.json"
    jf.write_text(json.dumps(jobs, ensure_ascii=False), encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(ROOT / "tools/render_editor.py"), str(jf)], cwd=work, check=True, stdout=subprocess.DEVNULL)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    gfile = pathlib.Path(sys.argv[1]).resolve()
    g = json.loads(gfile.read_text(encoding="utf-8"))
    fmt = g.get("formato", "9x16-marco")
    W, H = SIZE[fmt]
    base = gfile.parent
    out = (base / g.get("salida", "montaje.mp4")).resolve()
    work = pathlib.Path(tempfile.mkdtemp(prefix="tpd-montaje-"))
    segs = g["segmentos"]

    # 1) Capas PNG con el editor
    jobs = []
    vertical = fmt.startswith("9x16")
    capa = dict(g.get("capa", {}))
    estilo = capa.pop("estilo", "clasico")
    por_segmento = fmt == "9x16" and estilo in TEXTO_EN_MARCO
    tiktok = fmt == "9x16" and estilo == "tiktok"
    timed = {}           # segmento -> [(png, inicio, fin)] capas con tiempo (subtítulos y gancho)
    for i, s in enumerate(segs):
        if s.get("separador") is not None:
            jobs.append({"template": "separador_v" if vertical else "separador_h", "values": s["separador"], "output": str(work / f"sep_{i}.png")})
            continue
        if tiktok and s.get("numero"):   # formato lista: número grande y título durante todo el segmento
            png = work / f"numero_{i}.png"
            jobs.append({"template": "numero_tiktok", "values": {"numero": s["numero"], "titulo": s.get("titulo", "")}, "output": str(png)})
            timed.setdefault(i, []).append((png, 0, round(float(s.get("duracion", 4)), 3)))
        if fmt == "9x16-marco":
            jobs.append({"template": "marco_video", "values": {**g.get("marco", {}), "texto": s.get("texto", "")}, "output": str(work / f"capa_{i}.png")})
        elif tiktok and s.get("texto"):
            dur = float(s.get("duracion", 4))
            sub = g.get("capa", {}).get("subtitulos", "karaoke")
            parts_ = chunks(s["texto"], max_words=1) if sub == "pop" else chunks(s["texto"])
            t0, span = 0.12, max(0.5, dur - 0.22)
            per = span / len(parts_)
            for c, ws in enumerate(parts_):
                for j in range(len(ws)):
                    png = work / f"sub_{i}_{c}_{j}.png"
                    vals = {"texto": " ".join(ws), "destacar": j + 1, "estilo": sub, "color": len(timed.get(i, [])) + i}
                    if sub == "editorial":
                        vals["y"] = 1300
                    jobs.append({"template": "subtitulo_tiktok", "values": vals, "output": str(png)})
                    a = t0 + c * per + j * per / len(ws)
                    timed.setdefault(i, []).append((png, round(a, 3), round(a + per / len(ws), 3)))
        elif por_segmento:
            vals = {**capa, **({"titulo2": s["texto"]} if s.get("texto") else {})}
            jobs.append({"template": CAPA[("v", estilo)], "values": vals, "output": str(work / f"capa_{i}.png")})
        elif s.get("texto"):
            jobs.append({"template": "texto_pantalla" if vertical else "texto_pantalla_h",
                         "values": {"texto": s["texto"], "caja": s.get("estilo_texto", "tinta"), "pos": "abajo"}, "output": str(work / f"texto_{i}.png")})
        if s.get("rotulo"):
            jobs.append({"template": "tercio_inferior_v" if vertical else "tercio_inferior_h", "values": s["rotulo"], "output": str(work / f"rotulo_{i}.png")})
    gancho = g.get("gancho") or capa.pop("gancho", None)   # se acepta arriba en el guion o dentro de "capa"
    capa.pop("gancho", None)
    if tiktok and gancho:
        first = next((k for k, s in enumerate(segs) if s.get("separador") is None), None)
        if first is not None:
            png = work / "gancho.png"
            jobs.append({"template": "gancho_tiktok", "values": gancho, "output": str(png)})
            fin = round(min(1.8, float(segs[first].get("duracion", 4))), 3)
            timed.setdefault(first, []).append((png, 0, fin))
            # el número de lista y los subtítulos del primer segmento aparecen cuando termina el gancho
            # (los subtítulos se reparten en el tiempo que queda, para no encimarse con él)
            dur0 = float(segs[first].get("duracion", 4))
            k = max(0.0, dur0 - fin) / dur0
            timed[first] = [(p_, max(a, fin), b) if p_.name.startswith("numero_")
                            else (p_, round(fin + a * k, 3), round(fin + b * k, 3)) if p_.name.startswith("sub_")
                            else (p_, a, b) for p_, a, b in timed[first]]
    if fmt != "9x16-marco" and not por_segmento:
        key = ("v" if vertical else "h", estilo)
        if key not in CAPA:
            raise SystemExit(f"Estilo de capa desconocido para {fmt}: {estilo}")
        jobs.append({"template": CAPA[key], "values": capa, "output": str(work / "marca.png")})
    ventana = VENTANA.get(estilo) if fmt == "9x16" else None
    print(f"Renderizando {len(jobs)} capas…")
    render_overlays(jobs, work)

    # 2) Segmentos
    parts = []
    if g.get("intro", True):
        parts.append(("intro", ROOT / (INTRO.get(estilo, "video/intro_9x16.mp4") if vertical else "video/intro_16x9.mp4")))
    for i, s in enumerate(segs):
        dur = float(s.get("duracion", 4))
        if s.get("separador") is not None:
            seg = work / f"seg_{i:02d}.mp4"
            ff("-loop", "1", "-framerate", "30", "-t", str(dur), "-i", str(work / f"sep_{i}.png"), "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo",
               "-vf", f"scale={W}:{H},setsar=1,fade=t=in:d=0.25,fade=t=out:st={max(0, dur - 0.25)}:d=0.25,format=yuv420p", "-map", "0:v", "-map", "1:a", "-t", str(dur), *ENC, str(seg))
            parts.append((f"segmento {i + 1}", seg))
            print(f"  segmento {i + 1}/{len(segs)} listo (separador)")
            continue
        still = s.get("foto") is not None
        if still:   # foto fija: se trata como un clip sin audio, con paneo lento de izquierda a derecha
            clip = pathlib.Path(s["foto"])
            clip = clip if clip.is_absolute() else base / clip
            inputs = ["-loop", "1", "-framerate", "30", "-t", str(dur), "-i", str(clip)]
        else:
            clip = pathlib.Path(s["clip"])
            clip = clip if clip.is_absolute() else base / clip
            inputs = ["-ss", str(s.get("inicio", 0)), "-t", str(dur), "-i", str(clip)]
        enc = s.get("encuadre", "centro")
        fx = {"izquierda": 0.12, "centro": 0.5, "derecha": 0.88}.get(enc, enc)
        fx = min(1.0, max(0.0, float(fx)))

        def cover(w, h):
            if not still:
                return f"{TONEMAP if is_hdr(clip) else ''}scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}:x='(iw-{w})*{fx}':y='(ih-{h})/2'"
            bw, bh = int(w * 1.12) // 2 * 2, int(h * 1.12) // 2 * 2
            return f"scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={w}:{h}:x='(iw-{w})*t/{dur}':y='(ih-{h})/2'"
        if ventana:
            vw, vh, vx, vy = ventana
            chain = f"[0:v]{cover(vw, vh)},setsar=1,pad=1080:1920:{vx}:{vy}:black[b0]"
            layers = [p for p in (work / f"capa_{i}.png", work / "marca.png", work / f"texto_{i}.png") if p.exists()]
        elif fmt == "9x16-marco":
            chain = f"[0:v]{cover(960, 540)},setsar=1,pad=1080:1920:60:650:black[b0]"
            layers = [work / f"capa_{i}.png"]
        elif tiktok:
            zoom = "" if still else (",fps=30,zoompan=z='min(1+0.0015*on,1.09)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                                     f":s={W}x{H}:fps=30")
            chain = f"[0:v]{cover(W, H)},setsar=1{zoom}[b0]"
            layers = [work / "marca.png"] + timed.get(i, [])
        else:
            chain = f"[0:v]{cover(W, H)},setsar=1[b0]"
            layers = [p for p in (work / "marca.png", work / f"texto_{i}.png") if p.exists()]
        rot = work / f"rotulo_{i}.png"
        idx = 1
        for layer in layers:
            path, when = (layer[0], f":enable='between(t,{layer[1]},{layer[2]})'") if isinstance(layer, tuple) else (layer, "")
            inputs += ["-loop", "1", "-t", str(dur), "-i", str(path)]
            chain += f";[b{idx - 1}][{idx}:v]overlay=0:0{when}[b{idx}]"
            idx += 1
        if rot.exists():
            inputs += ["-loop", "1", "-t", str(dur), "-i", str(rot)]
            chain += f";[{idx}:v]format=rgba,fade=t=in:st=0.4:d=0.3:alpha=1,fade=t=out:st={max(0.8, min(dur, 5) - 0.4)}:d=0.3:alpha=1[r];[b{idx - 1}][r]overlay=0:0[b{idx}]"
            idx += 1
        chain += f";[b{idx - 1}]fps=30,format=yuv420p[v]"
        if not still and g.get("audio", "original") == "original" and has_audio(clip):
            chain += f";[0:a]afade=t=in:d=0.15,afade=t=out:st={max(0, dur - 0.25)}:d=0.25,aresample=48000,aformat=channel_layouts=stereo[a]"
            amap = ["-map", "[a]"]
        else:
            inputs += ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
            amap = ["-map", f"{idx}:a"]
        seg = work / f"seg_{i:02d}.mp4"
        ff(*inputs, "-filter_complex", chain, "-map", "[v]", *amap, "-t", str(dur), *ENC, str(seg))
        parts.append((f"segmento {i + 1}", seg))
        print(f"  segmento {i + 1}/{len(segs)} listo")
    if g.get("cierre", True):
        linea = g.get("capa", {}).get("linea", "zine") if tiktok else estilo
        parts.append(("cierre", ROOT / (CIERRE.get(linea, "video/cierre_9x16.mp4") if vertical else "video/cierre_16x9.mp4")))

    # 3) Normalizar intro/cierre (agregar audio en silencio) y unir
    final = []
    for name, p in parts:
        if name in ("intro", "cierre"):
            q = work / f"{name}.mp4"
            ff("-i", str(p), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-vf", f"scale={W}:{H},fps=30,format=yuv420p",
               "-map", "0:v", "-map", "1:a", "-shortest", *ENC, str(q))
            p = q
        final.append(p)
    lst = work / "lista.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in final), encoding="utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    ff("-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(out))
    dur = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
    print(f"Listo: {out}  ({W}x{H}, {float(dur):.1f} s, {out.stat().st_size // 1024} KB)")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
