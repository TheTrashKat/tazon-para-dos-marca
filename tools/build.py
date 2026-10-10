"""Generador del kit visual de Tazón para Dos.

Lee brand/tokens.json y escribe:
  brand/tokens.css            variables CSS
  assets/logo/*.svg           mascota, sello, logotipo horizontal y apilado
  assets/iconos/*.svg         set de íconos de línea (64 px) + sprite.svg
  assets/elementos/*.svg      ilustraciones sueltas (d20, d6, meeple, carta, micrófono, destello)
  plantillas/*.svg            piezas de campaña generadas
  aplicaciones/*.svg          aplicaciones de producto (stickers)

Uso:  python -I tools/build.py      (luego tools/render.ps1 para exportar PNG)
"""
import json, math, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "brand" / "tokens.json").read_text(encoding="utf-8"))
C = {k: v["value"] for k, v in T["color"].items() if isinstance(v, dict) and "value" in v}
INK, CORAL, SUN, TEAL, CREAM = C["ink"], C["coral"], C["sun"], C["teal"], C["cream"]
SUN_L = T["color"]["tint"]["sun-light"]["value"]
TEAL_L = T["color"]["tint"]["teal-light"]["value"]

FONT_IMPORT = ("@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800"
               "&amp;family=Barlow:wght@500;600;700&amp;display=swap');")
STYLE = f"""<style>
      {FONT_IMPORT}
      .cond {{ font-family: 'Barlow Condensed', 'Arial Narrow', sans-serif; font-weight: 800; }}
      .sans {{ font-family: 'Barlow', 'Segoe UI', sans-serif; }}
    </style>"""


FONTS = ROOT / "tools" / "fonts"
_font_cache = {}


def text_path(text, font, size, x, y, fill, anchor="start", tracking=0.0):
    """Convierte texto en un <path> (contornos) para que el logo no dependa de fuentes instaladas."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    if font not in _font_cache:
        f = TTFont(FONTS / font)
        _font_cache[font] = (f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm, f["hmtx"])
    f, gs, cmap, upm, hmtx = _font_cache[font]
    s = size / upm
    names = [cmap.get(ord(ch), ".notdef") for ch in text]
    width = sum(hmtx[n][0] * s for n in names) + tracking * (len(names) - 1)
    cursor = x - (width / 2 if anchor == "middle" else 0)
    pen = SVGPathPen(gs)
    for n in names:
        gs[n].draw(TransformPen(pen, (s, 0, 0, -s, cursor, y)))
        cursor += hmtx[n][0] * s + tracking
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', width


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("  ", rel)


# ------------------------------------------------------------------ piezas base
def bowl_shapes(body=INK, face=CREAM):
    """Mascota del tazón dibujada en una caja 120 x 124."""
    return f'''<g stroke="{body}" stroke-width="7" stroke-linecap="round">
      <line x1="16" y1="20" x2="29" y2="38"/><line x1="35" y1="12" x2="43" y2="31"/>
      <line x1="85" y1="12" x2="77" y2="31"/><line x1="104" y1="20" x2="91" y2="38"/>
    </g>
    <g fill="{body}">
      <circle cx="60" cy="54" r="20"/><circle cx="42" cy="61" r="16"/><circle cx="78" cy="61" r="16"/>
      <circle cx="30" cy="70" r="11"/><circle cx="90" cy="70" r="11"/>
      <rect x="20" y="64" width="80" height="12"/>
      <path d="M14,80 H106 C106,101 92,112 75,112 H45 C28,112 14,101 14,80 Z"/>
      <rect x="45" y="116" width="30" height="7" rx="3.5"/>
    </g>
    <g fill="{face}">
      <rect x="44" y="85" width="6" height="13" rx="3"/><rect x="70" y="85" width="6" height="13" rx="3"/>
      <path d="M53,101 H67 A7,7 0 0 1 53,101 Z"/>
    </g>'''


def defs():
    return f"""<defs>
    {STYLE}
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.6" fill="{INK}" opacity="0.10"/></pattern>
    <pattern id="dotsLight" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.6" fill="{CREAM}" opacity="0.07"/></pattern>
    <symbol id="bowl" viewBox="0 0 120 124">{bowl_shapes()}</symbol>
    <symbol id="sparkle" viewBox="-50 -50 100 100"><path d="M0,-50 C6,-10 10,-6 50,0 C10,6 6,10 0,50 C-6,10 -10,6 -50,0 C-10,-6 -6,-10 0,-50 Z"/></symbol>
    <symbol id="meeple" viewBox="0 0 100 100"><path d="M50,4 C62,4 70,13 70,24 C70,31 67,36 63,40 L94,52 C99,54 99,62 94,64 L72,70 L84,96 H58 L50,78 L42,96 H16 L28,70 L6,64 C1,62 1,54 6,52 L37,40 C33,36 30,31 30,24 C30,13 38,4 50,4 Z"/></symbol>
  </defs>"""


def svg(w, h, title, body, with_defs=True):
    pal = " · ".join(f"{k} {v}" for k, v in C.items())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
            f'  <title>{title} · Tazón para Dos</title>\n'
            f'  <!-- Generado por tools/build.py · Paleta: {pal} -->\n'
            f'  {defs() if with_defs else ""}\n{body}\n</svg>\n')


def sparkle(x, y, s, fill):
    return f'<use href="#sparkle" x="{x - s/2}" y="{y - s/2}" width="{s}" height="{s}" fill="{fill}"/>'


def header(x, y, s, ink, sub="ESPACIO CULTURAL · ENGATIVÁ"):
    r = 46 * s
    return f'''<circle cx="{x}" cy="{y}" r="{r}" fill="{CREAM}" stroke="{INK}" stroke-width="{4*s}"/>
  <use href="#bowl" x="{x - 29*s}" y="{y - 31*s}" width="{58*s}" height="{60*s}"/>
  <text x="{x + 66*s}" y="{y + 2*s}" class="cond" font-size="{44*s}" fill="{ink}" letter-spacing="1">TAZÓN PARA DOS</text>
  <text x="{x + 68*s}" y="{y + 32*s}" class="sans" font-weight="600" font-size="{15*s}" fill="{ink}" letter-spacing="{5*s}" opacity="0.9">{sub}</text>'''


def pill(x, y, w, h, fill, ink, label, size, stroke=None, shadow=False):
    out = ""
    if shadow:
        out += f'<rect x="{x+8}" y="{y+8}" width="{w}" height="{h}" rx="{h/2}" fill="{INK}"/>'
    st = f' stroke="{stroke}" stroke-width="4"' if stroke else ""
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}"{st}/>'
    out += (f'<text x="{x + w/2}" y="{y + h/2 + size*0.36}" text-anchor="middle" class="sans" font-weight="700" '
            f'font-size="{size}" fill="{ink}" letter-spacing="2">{label}</text>')
    return out


def mic(tx, ty, s, body=CREAM, stand=INK, waves=True):
    w = ""
    if waves:
        w = f'''<path d="M100,-110 A90,90 0 0 1 100,10" fill="none" stroke="{SUN}" stroke-width="12"/>
    <path d="M136,-140 A130,130 0 0 1 136,40" fill="none" stroke="{CORAL}" stroke-width="12"/>
    <path d="M-100,-110 A90,90 0 0 0 -100,10" fill="none" stroke="{SUN}" stroke-width="12"/>
    <path d="M-136,-140 A130,130 0 0 0 -136,40" fill="none" stroke="{TEAL}" stroke-width="12"/>'''
    return f'''<g transform="translate({tx},{ty}) scale({s})" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
    <path d="M-80,10 A80,80 0 0 0 80,10" fill="none" stroke="{stand}"/>
    <line x1="0" y1="90" x2="0" y2="200" stroke="{stand}"/>
    <rect x="-60" y="196" width="120" height="22" rx="11" fill="{stand}" stroke="{stand}"/>
    <rect x="-52" y="-150" width="104" height="200" rx="52" fill="{body}"/>
    <path d="M-52,-60 H52 M-52,-20 H52" fill="none"/>
    <g fill="{INK}" stroke="none"><circle cx="-20" cy="-110" r="6"/><circle cx="0" cy="-118" r="6"/><circle cx="20" cy="-110" r="6"/><circle cx="-10" cy="-90" r="6"/><circle cx="10" cy="-90" r="6"/></g>
    {w}
  </g>'''


def d20(tx, ty, R, rot=-8, num=True, fill=SUN, inner=SUN_L):
    k = R / 200
    pts = lambda a: f"{a[0]*k:.1f},{a[1]*k:.1f}"
    hexa = [(0, -200), (173, -100), (173, 100), (0, 200), (-173, 100), (-173, -100)]
    tri = [(0, -105), (92, 58), (-92, 58)]
    lines = [((0, -200), (0, -105)), ((0, -105), (173, -100)), ((0, -105), (-173, -100)),
             ((92, 58), (173, -100)), ((92, 58), (173, 100)), ((92, 58), (0, 200)),
             ((-92, 58), (-173, -100)), ((-92, 58), (-173, 100)), ((-92, 58), (0, 200))]
    d = " ".join(f"M{pts(a)} L{pts(b)}" for a, b in lines)
    sw = max(3, 7 * k * 1.4)
    t = (f'<text x="0" y="{36*k:.1f}" text-anchor="middle" class="cond" font-size="{92*k:.1f}" fill="{INK}" stroke="none">20</text>'
         if num else "")
    return f'''<g transform="translate({tx},{ty}) rotate({rot})" stroke="{INK}" stroke-width="{sw:.1f}" stroke-linejoin="round">
    <path d="M{' L'.join(pts(p) for p in hexa)} Z" fill="{fill}"/>
    <path d="M{' L'.join(pts(p) for p in tri)} Z" fill="{inner}"/>
    <path d="{d}" fill="none"/>{t}
  </g>'''


def d6(tx, ty, s, rot=14, fill=CREAM):
    h = 42 * s
    p, r = 20 * s, 7 * s
    pips = "".join(f'<circle cx="{x}" cy="{y}" r="{r:.1f}"/>' for x, y in [(-p, -p), (p, -p), (0, 0), (-p, p), (p, p)])
    return f'''<g transform="translate({tx},{ty}) rotate({rot})">
    <rect x="{-h}" y="{-h}" width="{2*h}" height="{2*h}" rx="{15*s:.1f}" fill="{fill}" stroke="{INK}" stroke-width="{6*s:.1f}"/>
    <g fill="{INK}">{pips}</g>
  </g>'''


def card(tx, ty, s, rot=-14):
    return f'''<g transform="translate({tx},{ty}) rotate({rot}) scale({s})">
    <rect x="-62" y="-88" width="124" height="176" rx="14" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>
    <path d="M0,-38 L27,0 L0,38 L-27,0 Z" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>
    <circle cx="-40" cy="-64" r="6" fill="{CORAL}"/><circle cx="40" cy="64" r="6" fill="{CORAL}"/>
  </g>'''


def waveform(x0, x1, cy, maxh, color):
    out, x, i = [], x0, 0
    while x + 10 <= x1:
        h = maxh * (0.25 + 0.75 * abs(math.sin(i * 0.55) * math.cos(i * 0.21)))
        out.append(f'<rect x="{x}" y="{cy - h/2:.1f}" width="10" height="{h:.1f}" rx="5" fill="{color}"/>')
        x += 18
        i += 1
    return "\n  ".join(out)


def bubble(x, y, w, h, text, size):
    return f'''<g>
    <rect x="{x+8}" y="{y+8}" width="{w}" height="{h}" rx="28" fill="{INK}"/>
    <path d="M{x+60},{y+h} l-10,46 l58,-46 Z" fill="{INK}"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>
    <path d="M{x+56},{y+h-3} l-12,40 l52,-40" fill="{CREAM}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
    <text x="{x+40}" y="{y + h/2 + size*0.35}" class="sans" font-weight="600" font-style="italic" font-size="{size}" fill="{INK}">{text}</text>
    <rect x="{x + w - 56}" y="{y + h/2 - size*0.55}" width="6" height="{size*1.1}" rx="3" fill="{CORAL}"/>
  </g>'''


def steps(cxs, cy, r, labels, ink, size):
    cols = [TEAL, CREAM, SUN]
    out = []
    for i, (cx, (l1, l2)) in enumerate(zip(cxs, labels)):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{cols[i]}" stroke="{INK}" stroke-width="4"/>')
        out.append(f'<text x="{cx}" y="{cy + r*0.42}" text-anchor="middle" class="cond" font-size="{r*1.2}" fill="{INK}">{i+1}</text>')
        out.append(f'<text x="{cx}" y="{cy + r + size*1.6}" text-anchor="middle" class="sans" font-weight="700" font-size="{size}" fill="{ink}" letter-spacing="2">{l1}</text>')
        out.append(f'<text x="{cx}" y="{cy + r + size*2.9}" text-anchor="middle" class="sans" font-weight="700" font-size="{size}" fill="{ink}" letter-spacing="2">{l2}</text>')
    return "\n  ".join(out)


# ------------------------------------------------------------------ tokens.css
def build_css():
    lines = ["/* Tazón para Dos · tokens de marca (generado por tools/build.py) */", ":root {"]
    for k, v in T["color"].items():
        if isinstance(v, dict) and "value" in v:
            lines.append(f"  --{k}: {v['value']};")
    for k, v in T["color"]["tint"].items():
        lines.append(f"  --{k}: {v['value']};")
    for k, v in T["shape"]["radius"].items():
        lines.append(f"  --radius-{k}: {v}px;")
    lines += [
        "  --shadow-comic: 8px 8px 0 rgba(40, 32, 59, 0.18);",
        "  --shadow-card: 0 8px 0 rgba(40, 32, 59, 0.18);",
        "  --font-display: 'Barlow Condensed', 'Arial Narrow', sans-serif;",
        "  --font-text: 'Barlow', 'Segoe UI', sans-serif;",
        "  --font-web-display: 'Space Grotesk', sans-serif;",
        "  --font-web-text: 'DM Sans', sans-serif;",
        "  --font-mono: 'DM Mono', monospace;",
        "  --dots: radial-gradient(rgba(40, 32, 59, 0.10) 1.6px, transparent 1.7px) 0 0 / 22px 22px;",
        "}",
    ]
    write("brand/tokens.css", "\n".join(lines) + "\n")


# ------------------------------------------------------------------ logos
def build_logos():
    write("assets/logo/mascota.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 124" width="480" height="496"><title>Mascota Tazón para Dos</title>{bowl_shapes()}</svg>\n')
    write("assets/logo/mascota-inverso.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 124" width="480" height="496"><title>Mascota Tazón para Dos (inverso)</title>{bowl_shapes(CREAM, INK)}</svg>\n')
    sello = lambda bg, stroke, body, face: (
        f'<circle cx="80" cy="80" r="74" fill="{bg}" stroke="{stroke}" stroke-width="6"/>'
        f'<g transform="translate(34,34) scale(0.77)">{bowl_shapes(body, face)}</g>')
    write("assets/logo/sello.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" width="480" height="480"><title>Sello Tazón para Dos</title>{sello(CREAM, INK, INK, CREAM)}</svg>\n')
    write("assets/logo/sello-inverso.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" width="480" height="480"><title>Sello Tazón para Dos (inverso)</title>{sello(INK, CREAM, CREAM, INK)}</svg>\n')

    COND, SANS = "BarlowCondensed-ExtraBold.ttf", "Barlow-SemiBold.ttf"

    def horizontal(ink, bg_sello, stroke, body, face, bg=None):
        name, w1 = text_path("TAZÓN PARA DOS", COND, 76, 196, 102, ink, tracking=1)
        sub, w2 = text_path("ESPACIO CULTURAL", SANS, 20, 199, 140, ink, tracking=7)
        W = int(196 + max(w1, w2) + 16)
        back = f'<rect width="{W}" height="180" fill="{bg}"/>' if bg else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 180" width="{W*2}" height="360">'
                f'<title>Logotipo horizontal Tazón para Dos</title>{back}'
                f'<g transform="translate(10,10)">{sello(bg_sello, stroke, body, face)}</g>{name}{sub}</svg>\n')
    write("assets/logo/logotipo-horizontal.svg", horizontal(INK, CREAM, INK, INK, CREAM))
    write("assets/logo/logotipo-horizontal-inverso.svg", horizontal(CREAM, CREAM, CREAM, INK, CREAM, bg=INK))

    def apilado(ink, bg=None):
        _, w1 = text_path("TAZÓN PARA DOS", COND, 70, 0, 0, ink, tracking=1)
        W = int(w1 + 40)
        cx = W / 2
        name, _ = text_path("TAZÓN PARA DOS", COND, 70, cx, 264, ink, anchor="middle", tracking=1)
        sub, _ = text_path("ESPACIO CULTURAL", SANS, 18, cx, 302, ink, anchor="middle", tracking=7)
        back = f'<rect width="{W}" height="330" fill="{bg}"/>' if bg else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 330" width="{W*2}" height="660">'
                f'<title>Logotipo apilado Tazón para Dos</title>{back}'
                f'<g transform="translate({cx - 80},10)">{sello(CREAM, ink, INK, CREAM)}</g>{name}{sub}</svg>\n')
    write("assets/logo/logotipo-apilado.svg", apilado(INK))
    write("assets/logo/logotipo-apilado-inverso.svg", apilado(CREAM, bg=INK))


# ------------------------------------------------------------------ íconos
ICONS = {
    "dado": ("Juegos de mesa", '<path d="M32 7 54 20v24L32 57 10 44V20Z"/><path d="m10 20 22 13 22-13M32 33v24"/><g fill="currentColor" stroke="none"><circle cx="32" cy="20" r="3.2"/><circle cx="19" cy="34" r="3.2"/><circle cx="24" cy="45" r="3.2"/><circle cx="45" cy="34" r="3.2"/><circle cx="40" cy="45" r="3.2"/></g>'),
    "d20": ("Rol", '<path d="M32 4 56 18v28L32 60 8 46V18Z"/><path d="M32 18 46 42H18Z"/><path d="M32 4v14M32 18H8M32 18h24M18 42 8 18M18 42 8 46M18 42l14 18M46 42l10-24M46 42l10 4M46 42 32 60"/>'),
    "meeple": ("Jugadores", '<path d="M32 8a8 8 0 0 1 6 13l14 6c3 1 3 6 0 7l-12 3 7 15H37l-5-10-5 10H17l7-15-12-3c-3-1-3-6 0-7l14-6a8 8 0 0 1 6-13Z"/>'),
    "carta": ("Cartas", '<rect x="14" y="8" width="36" height="48" rx="5"/><path d="m32 22 8 10-8 10-8-10Z"/>'),
    "idea": ("Idea / postula", '<path d="M22 42h20M25 49h14M32 8a16 16 0 0 0-9 29c2 1 3 3 3 5h12c0-2 1-4 3-5a16 16 0 0 0-9-29Z"/><path d="M28 56h8"/>'),
    "microfono": ("Podcast", '<rect x="24" y="7" width="16" height="31" rx="8"/><path d="M16 30a16 16 0 0 0 32 0M32 46v11M24 57h16"/>'),
    "audifonos": ("Escuchar", '<path d="M12 42v-8a20 20 0 0 1 40 0v8"/><path d="M12 40h8v14h-4a4 4 0 0 1-4-4ZM52 40h-8v14h4a4 4 0 0 0 4-4Z"/>'),
    "onda": ("Sonido", '<path d="M8 30v4M16 24v16M24 16v32M32 26v12M40 12v40M48 22v20M56 29v6"/>'),
    "play": ("Reproducir", '<circle cx="32" cy="32" r="26"/><path d="m27 22 14 10-14 10Z"/>'),
    "historia": ("Historias / oralidad", '<path d="M12 12h40a4 4 0 0 1 4 4v24a4 4 0 0 1-4 4H28L16 54V44h-4a4 4 0 0 1-4-4V16a4 4 0 0 1 4-4Z"/><path d="M20 24h24M20 32h14"/>'),
    "libro": ("Narración", '<path d="M8 14c8-3 16-2 24 4 8-6 16-7 24-4v36c-8-3-16-2-24 4-8-6-16-7-24-4Z"/><path d="M32 18v36"/>'),
    "comunidad": ("Comunidad", '<circle cx="22" cy="20" r="8"/><circle cx="42" cy="20" r="8"/><path d="M6 52c0-10 7-16 16-16s16 6 16 16M30 40c3-3 7-4 12-4 9 0 16 6 16 16"/>'),
    "corazon": ("Espacio seguro", '<path d="M32 54S8 40 8 24a12 12 0 0 1 24-4 12 12 0 0 1 24 4c0 16-24 30-24 30Z"/>'),
    "ubicacion": ("Engativá", '<path d="M32 58S12 38 12 26a20 20 0 0 1 40 0c0 12-20 32-20 32Z"/><circle cx="32" cy="26" r="7"/>'),
    "calendario": ("Fechas", '<rect x="10" y="14" width="44" height="40" rx="5"/><path d="M10 26h44M22 8v12M42 8v12M20 36h6M30 36h6M40 36h6M20 45h6M30 45h6"/>'),
    "votacion": ("Votación abierta", '<path d="M10 32h44v22H10Z"/><path d="M22 32V10h20v22"/><path d="m27 20 4 4 7-8M24 43h16"/>'),
    "destello": ("Destello", '<path d="M32 6C34 26 38 30 58 32 38 34 34 38 32 58 30 38 26 34 6 32 26 30 30 26 32 6Z"/>'),
    "reloj": ("Horario", '<circle cx="32" cy="32" r="24"/><path d="M32 18v14l10 6"/>'),
    "web": ("Sitio web", '<circle cx="32" cy="32" r="24"/><path d="M8 32h48M32 8c9 8 9 40 0 48M32 8c-9 8-9 40 0 48"/>'),
    "camara": ("Redes sociales", '<rect x="10" y="10" width="44" height="44" rx="12"/><circle cx="32" cy="32" r="10"/><circle cx="45" cy="19" r="1.5" fill="currentColor"/>'),
    "tazon": ("Tazón",'<path d="M8 32h48c0 13-10 21-24 21S8 45 8 32Z"/><path d="M24 59h16M14 30c0-8 5-13 11-13 2-4 12-4 14 0 6 0 11 5 11 13M17 6l4 6M47 6l-4 6M27 38v5M37 38v5"/>'),
}


def build_icons():
    ic = T["icon"]
    attrs = (f'fill="none" stroke="currentColor" stroke-width="{ic["stroke"]}" '
             f'stroke-linecap="{ic["linecap"]}" stroke-linejoin="{ic["linejoin"]}"')
    sprite = []
    for name, (label, body) in ICONS.items():
        write(f"assets/iconos/{name}.svg",
              f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" {attrs} '
              f'style="color:{INK}"><title>{label}</title>{body}</svg>\n')
        sprite.append(f'  <symbol id="i-{name}" viewBox="0 0 64 64" {attrs}><title>{label}</title>{body}</symbol>')
    write("assets/iconos/sprite.svg",
          '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n' + "\n".join(sprite) + "\n</svg>\n")


# ------------------------------------------------------------------ elementos
def build_elements():
    def el(name, w, h, body, title):
        write(f"assets/elementos/{name}.svg", svg(w, h, title, body))
    el("d20", 440, 440, d20(220, 220, 200, rot=-8), "Dado de 20 caras")
    el("d20-turquesa", 440, 440, d20(220, 220, 200, rot=-8, fill=TEAL, inner=TEAL_L), "Dado de 20 caras turquesa")
    el("d6", 140, 140, d6(70, 70, 1.2, rot=0), "Dado de 6 caras")
    el("carta", 200, 240, card(100, 120, 1.0, rot=0), "Carta")
    el("meeple", 200, 200, f'<use href="#meeple" x="0" y="0" width="200" height="200" fill="{INK}"/>', "Meeple")
    el("microfono", 340, 400, mic(170, 170, 1.0), "Micrófono con ondas")
    el("destello", 200, 200, sparkle(100, 100, 200, SUN), "Destello")
    el("tazon-mascota", 240, 248, f'<use href="#bowl" x="0" y="0" width="240" height="248"/>', "Mascota")


# ------------------------------------------------------------------ plantillas generadas
STEPS = [("POSTULA", "TU IDEA"), ("LA JUGAMOS", "EN MESA"), ("LA LLEVAMOS", "AL AIRE")]


def build_templates():
    pod_sq = f'''
  <rect width="1080" height="1080" fill="{INK}"/>
  <rect width="1080" height="1080" fill="url(#dotsLight)"/>
  <path d="M900,0 H1080 V180 Z" fill="{SUN}"/><path d="M990,0 H1080 V90 Z" fill="{CORAL}"/>
  {header(110, 104, 1, CREAM)}
  {pill(64, 186, 290, 50, TEAL, INK, "PODCAST NARRATIVO", 20)}
  <g class="cond">
    <text x="60" y="390" font-size="156" fill="{CREAM}">DEL JUEGO</text>
    <text x="70" y="560" font-size="178" fill="{TEAL}">AL AIRE.</text>
    <text x="60" y="550" font-size="178" fill="{SUN}">AL AIRE.</text>
  </g>
  <path d="M0,690 L1080,628 L1080,668 L0,730 Z" fill="{CREAM}"/>
  <path d="M0,730 L1080,668 L1080,1080 L0,1080 Z" fill="{TEAL}"/>
  <path d="M0,730 L1080,668 L1080,1080 L0,1080 Z" fill="url(#dots)"/>
  {mic(870, 430, 1.0, stand=CREAM)}
  {d20(640, 640, 62, rot=12, num=False)}
  {sparkle(980, 250, 40, CREAM)}
  {sparkle(700, 210, 54, SUN)}
  <text class="sans" font-weight="600" font-size="30" fill="{INK}">
    <tspan x="64" y="800">Reproduce nuestras series narrativas y</tspan>
    <tspan x="64" y="840">acompáñanos a imaginar nuevos mundos.</tspan>
  </text>
  {waveform(64, 1016, 910, 56, INK)}
  {pill(64, 970, 470, 70, INK, CREAM, "▶  ESCÚCHALO EN SPOTIFY", 24)}
  <text x="1016" y="1016" text-anchor="end" class="sans" font-weight="700" font-size="28" fill="{INK}">@tazonparados</text>
'''
    pod_st = f'''
  <rect width="1080" height="1920" fill="{INK}"/>
  <rect width="1080" height="1920" fill="url(#dotsLight)"/>
  <path d="M820,0 H1080 V260 Z" fill="{SUN}"/><path d="M950,0 H1080 V130 Z" fill="{CORAL}"/>
  {header(132, 300, 1.22, CREAM)}
  {pill(76, 400, 340, 60, TEAL, INK, "PODCAST NARRATIVO", 24)}
  <g class="cond">
    <text x="70" y="660" font-size="210" fill="{CREAM}">DEL JUEGO</text>
    <text x="82" y="882" font-size="236" fill="{TEAL}">AL AIRE.</text>
    <text x="70" y="870" font-size="236" fill="{SUN}">AL AIRE.</text>
  </g>
  {sparkle(980, 500, 70, SUN)}
  {sparkle(930, 800, 40, CREAM)}
  <path d="M0,1300 L1080,1240 L1080,1282 L0,1342 Z" fill="{CREAM}"/>
  <path d="M0,1342 L1080,1282 L1080,1920 L0,1920 Z" fill="{TEAL}"/>
  <path d="M0,1342 L1080,1282 L1080,1920 L0,1920 Z" fill="url(#dots)"/>
  {mic(560, 1046, 0.95, stand=CREAM)}
  {d20(190, 1160, 90, rot=-12, num=True)}
  <use href="#meeple" x="845" y="1110" width="100" height="100" fill="{SUN}"/>
  {sparkle(120, 990, 44, CREAM)}
  <text class="sans" font-weight="600" font-size="34" fill="{INK}" text-anchor="middle">
    <tspan x="540" y="1420">Reproduce nuestras series narrativas y</tspan>
    <tspan x="540" y="1464">acompáñanos a imaginar nuevos mundos.</tspan>
  </text>
  {waveform(76, 1004, 1540, 64, INK)}
  {pill(260, 1590, 560, 80, INK, CREAM, "▶  ESCÚCHALO EN SPOTIFY", 28)}
  <text x="540" y="1730" text-anchor="middle" class="sans" font-weight="700" font-size="30" fill="{INK}">@tazonparados</text>
'''
    conv_sq = f'''
  <rect width="1080" height="1080" fill="{SUN}"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <path d="M900,0 H1080 V180 Z" fill="{TEAL}"/><path d="M990,0 H1080 V90 Z" fill="{CORAL}"/>
  {header(110, 104, 1, INK)}
  {pill(64, 186, 330, 50, INK, CREAM, "CONVOCATORIA ABIERTA", 20)}
  <g class="cond">
    <text x="60" y="360" font-size="124" fill="{INK}">¿QUÉ MUNDO</text>
    <text x="60" y="478" font-size="124" fill="{INK}">QUIERES TRAER</text>
    <text x="70" y="620" font-size="150" fill="{INK}">A LA MESA?</text>
    <text x="60" y="610" font-size="150" fill="{CREAM}">A LA MESA?</text>
  </g>
  {sparkle(880, 300, 70, CORAL)}
  {sparkle(960, 400, 34, CREAM)}
  {d20(900, 560, 82, rot=14, num=True, fill=TEAL, inner=TEAL_L)}
  <path d="M0,780 L1080,730 L1080,960 L0,960 Z" fill="{CORAL}"/>
  <path d="M0,780 L1080,730 L1080,960 L0,960 Z" fill="url(#dots)"/>
  {bubble(470, 650, 420, 92, "Mi historia trata sobre...", 30)}
  {steps([180, 540, 900], 830, 32, STEPS, INK, 19)}
  <rect x="0" y="960" width="1080" height="120" fill="{INK}"/>
  {pill(64, 984, 380, 72, SUN, INK, "POSTULA TU IDEA →", 24)}
  <text x="1016" y="1018" text-anchor="end" class="sans" font-weight="700" font-size="24" fill="{CREAM}">tazon-para-dos.online</text>
  <text x="1016" y="1048" text-anchor="end" class="sans" font-weight="600" font-size="20" fill="{SUN}">@tazonparados</text>
'''
    conv_st = f'''
  <rect width="1080" height="1920" fill="{SUN}"/>
  <rect width="1080" height="1920" fill="url(#dots)"/>
  <path d="M820,0 H1080 V260 Z" fill="{TEAL}"/><path d="M950,0 H1080 V130 Z" fill="{CORAL}"/>
  {header(132, 300, 1.22, INK)}
  {pill(76, 400, 400, 60, INK, CREAM, "CONVOCATORIA ABIERTA", 24)}
  <g class="cond">
    <text x="70" y="640" font-size="160" fill="{INK}">¿QUÉ MUNDO</text>
    <text x="70" y="790" font-size="160" fill="{INK}">QUIERES TRAER</text>
    <text x="82" y="982" font-size="196" fill="{INK}">A LA MESA?</text>
    <text x="70" y="970" font-size="196" fill="{CREAM}">A LA MESA?</text>
  </g>
  {sparkle(990, 500, 70, CORAL)}
  <text class="sans" font-weight="600" font-size="34" fill="{INK}">
    <tspan x="76" y="1060">Estamos buscando voces, recuerdos y mundos</tspan>
    <tspan x="76" y="1102">para convertirlos en una nueva serie de</tspan>
    <tspan x="76" y="1144">podcast narrativo.</tspan>
  </text>
  <path d="M0,1330 L1080,1280 L1080,1920 L0,1920 Z" fill="{CORAL}"/>
  <path d="M0,1330 L1080,1280 L1080,1920 L0,1920 Z" fill="url(#dots)"/>
  {bubble(76, 1190, 640, 110, "Mi historia trata sobre...", 38)}
  {d20(890, 1230, 110, rot=14, num=True, fill=TEAL, inner=TEAL_L)}
  {steps([200, 540, 880], 1420, 40, STEPS, INK, 22)}
  {pill(250, 1580, 580, 84, INK, CREAM, "POSTULA TU IDEA →", 30)}
  <text x="540" y="1716" text-anchor="middle" class="sans" font-weight="700" font-size="30" fill="{INK}">tazon-para-dos.online · @tazonparados</text>
'''
    for name, (w, h), title, body in [
        ("podcast_cuadrado", (1080, 1080), "Post podcast", pod_sq),
        ("podcast_historia", (1080, 1920), "Historia podcast", pod_st),
        ("convocatoria_cuadrado", (1080, 1080), "Post convocatoria", conv_sq),
        ("convocatoria_historia", (1080, 1920), "Historia convocatoria", conv_st),
    ]:
        write(f"plantillas/{name}.svg", svg(w, h, title, body))


# ------------------------------------------------------------------ plantillas estáticas
# Piezas dibujadas a mano: se normalizan a la paleta oficial cada vez que se construye.
LEGACY = {"#5AB6B5": TEAL, "#55B0B3": TEAL, "#E26573": CORAL, "#F8CA68": SUN,
          "#2F223C": INK, "#FBF5E6": CREAM, "#FBD98A": SUN_L}


def normalize_static():
    for name in ["banner_web", "pancarta_80x180", "post_cuadrado", "historia"]:
        p = ROOT / "plantillas" / f"{name}.svg"
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        for old, new in LEGACY.items():
            t = re.sub(re.escape(old), new, t, flags=re.I)
        p.write_text(t, encoding="utf-8")
        print("   plantillas/%s.svg (normalizada)" % name)


# ------------------------------------------------------------------ aplicaciones
def build_stickers():
    body = f'''
  <rect width="1080" height="1080" fill="{CREAM}"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <text x="60" y="96" class="cond" font-size="56" fill="{INK}">HOJA DE STICKERS</text>
  <text x="62" y="132" class="sans" font-weight="600" font-size="18" fill="{INK}" letter-spacing="5" opacity="0.7">CORTE A 6 MM DEL BORDE · VINILO MATE</text>

  <!-- sello -->
  <circle cx="230" cy="330" r="150" fill="#FFFFFF" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"/>
  <circle cx="230" cy="330" r="132" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>
  <use href="#bowl" x="160" y="258" width="140" height="144"/>

  <!-- lema -->
  <g transform="translate(700,300) rotate(-6)">
    <rect x="-300" y="-92" width="600" height="184" rx="40" fill="#FFFFFF" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"/>
    <rect x="-282" y="-74" width="564" height="148" rx="30" fill="{INK}"/>
    <text x="0" y="-8" text-anchor="middle" class="cond" font-size="66" fill="{CREAM}">JUGAR TAMBIÉN</text>
    <text x="0" y="56" text-anchor="middle" class="cond" font-size="66" fill="{SUN}">ES ESCUCHAR.</text>
  </g>

  <!-- d20 -->
  <circle cx="230" cy="720" r="150" fill="#FFFFFF" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"/>
  {d20(230, 720, 130, rot=-10)}

  <!-- micrófono -->
  <circle cx="560" cy="700" r="150" fill="#FFFFFF" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"/>
  <circle cx="560" cy="700" r="132" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>
  {mic(560, 690, 0.52, stand=INK, waves=False)}

  <!-- espacio seguro -->
  <g transform="translate(870,700) rotate(8)">
    <rect x="-150" y="-110" width="300" height="220" rx="36" fill="#FFFFFF" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"/>
    <rect x="-132" y="-92" width="264" height="184" rx="26" fill="{SUN}" stroke="{INK}" stroke-width="6"/>
    <text x="0" y="-18" text-anchor="middle" class="cond" font-size="50" fill="{INK}">ESPACIO</text>
    <text x="0" y="40" text-anchor="middle" class="cond" font-size="50" fill="{INK}">SEGURO</text>
    <use href="#sparkle" x="84" y="-104" width="50" height="50" fill="{CORAL}"/>
  </g>

  <!-- meeple + lugar -->
  <g transform="translate(540,965)">
    <rect x="-470" y="-62" width="940" height="124" rx="62" fill="#FFFFFF" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"/>
    <rect x="-452" y="-44" width="904" height="88" rx="44" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>
    <use href="#meeple" x="-430" y="-34" width="68" height="68" fill="{INK}"/>
    <text x="20" y="16" text-anchor="middle" class="sans" font-weight="700" font-size="34" fill="{INK}" letter-spacing="4">JUEGOS DE MESA · ROL · PODCAST</text>
  </g>
'''
    write("aplicaciones/stickers.svg", svg(1080, 1080, "Hoja de stickers", body))


# ------------------------------------------------------------------ kit de redes
BRAND = json.loads((ROOT / "brand" / "brand.json").read_text(encoding="utf-8"))
LOC = BRAND["identity"]["location"]
SCHED = LOC["schedule"]


def icon(name, cx, cy, size, color=INK, stroke=4):
    """Ícono de línea del set, centrado en (cx, cy)."""
    k = size / 64
    return (f'<g transform="translate({cx - size/2:.1f},{cy - size/2:.1f}) scale({k:.4f})" fill="none" '
            f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" '
            f'style="color:{color}">{ICONS[name][1]}</g>')


def wrap(text, maxc):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + ([cur] if cur else [])


def background(w, h, color, light=False):
    pat = "dotsLight" if light else "dots"
    return f'<rect width="{w}" height="{h}" fill="{color}"/><rect width="{w}" height="{h}" fill="url(#{pat})"/>'


def corner(w, c1, c2, s=180):
    return f'<path d="M{w-s},0 H{w} V{s} Z" fill="{c1}"/><path d="M{w-s/2},0 H{w} V{s/2} Z" fill="{c2}"/>'


def headline_shadow(x, y, text, size, fg, shadow=INK, off=10, anchor="start"):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (f'<text x="{x+off}" y="{y+off}" class="cond" font-size="{size}" fill="{shadow}"{a}>{text}</text>'
            f'<text x="{x}" y="{y}" class="cond" font-size="{size}" fill="{fg}"{a}>{text}</text>')


def info_card(x, y, w, rows, size):
    """Tarjeta crema con filas ícono + texto (agenda)."""
    rh = size * 2.6
    h = rh * len(rows) + size * 0.8
    out = [f'<rect x="{x+10}" y="{y+10}" width="{w}" height="{h}" rx="28" fill="{INK}"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>']
    for i, (ic, label) in enumerate(rows):
        cy = y + size * 0.4 + rh * i + rh / 2
        if i:
            out.append(f'<line x1="{x+30}" y1="{cy - rh/2}" x2="{x+w-30}" y2="{cy - rh/2}" stroke="{INK}" stroke-width="2" opacity="0.2"/>')
        out.append(icon(ic, x + 30 + size * 0.75, cy, size * 1.5))
        out.append(f'<text x="{x + 60 + size*1.8}" y="{cy + size*0.36}" class="sans" font-weight="700" font-size="{size}" fill="{INK}">{label}</text>')
    return "\n  ".join(out), h


def chips(x, y, items, h, size):
    out, cx = [], x
    for label, fill in items:
        w = len(label) * size * 0.72 + 56
        out.append(pill(cx, y, w, h, fill, INK, label, size, stroke=INK))
        cx += w + 16
    return "".join(out)


AGENDA = [("calendario", SCHED["days"]),
          ("reloj", "11:00 a.m. – 9:00 p.m."),
          ("ubicacion", f'{LOC["address"]} · {LOC["locality"]}')]
ACTIVIDADES = [("ROL", TEAL), ("JUEGOS DE MESA", SUN), ("PODCAST", CREAM)]


def build_social():
    # --- Evento semanal (4:5 y 9:16) ---
    card, ch = info_card(64, 730, 952, AGENDA, 40)
    ev_v = f'''
  {background(1080, 1350, TEAL)}
  {corner(1080, SUN, CORAL)}
  {header(110, 104, 1, INK)}
  {pill(64, 186, 300, 50, INK, CREAM, "AGENDA SEMANAL", 20)}
  <text x="60" y="390" class="cond" font-size="146" fill="{INK}">ESTE SÁBADO</text>
  {headline_shadow(60, 570, "JUGAMOS.", 196, CREAM)}
  {d20(900, 360, 105, rot=12)}
  {sparkle(1000, 520, 44, CREAM)}
  {sparkle(820, 210, 40, INK)}
  <path d="M0,640 L1080,580 L1080,618 L0,678 Z" fill="{CREAM}"/>
  <path d="M0,678 L1080,618 L1080,1350 L0,1350 Z" fill="{CORAL}"/>
  <path d="M0,678 L1080,618 L1080,1350 L0,1350 Z" fill="url(#dots)"/>
  {card}
  {chips(64, 730 + ch + 50, ACTIVIDADES, 60, 22)}
  <text x="64" y="1300" class="sans" font-weight="700" font-size="28" fill="{INK}">Ven a jugar. Quédate a compartir.</text>
  <text x="1016" y="1300" text-anchor="end" class="sans" font-weight="700" font-size="28" fill="{INK}">@tazonparados</text>
'''
    write("plantillas/evento_vertical.svg", svg(1080, 1350, "Evento semanal 4:5", ev_v))

    card, ch = info_card(76, 1040, 928, AGENDA, 42)
    ev_s = f'''
  {background(1080, 1920, TEAL)}
  {corner(1080, SUN, CORAL, 260)}
  {header(132, 300, 1.22, INK)}
  {pill(76, 400, 360, 60, INK, CREAM, "AGENDA SEMANAL", 24)}
  <text x="70" y="660" class="cond" font-size="172" fill="{INK}">ESTE SÁBADO</text>
  {headline_shadow(70, 880, "JUGAMOS.", 236, CREAM, off=12)}
  {sparkle(990, 560, 70, SUN)}
  <path d="M0,960 L1080,900 L1080,942 L0,1002 Z" fill="{CREAM}"/>
  <path d="M0,1002 L1080,942 L1080,1920 L0,1920 Z" fill="{CORAL}"/>
  <path d="M0,1002 L1080,942 L1080,1920 L0,1920 Z" fill="url(#dots)"/>
  {d20(940, 960, 80, rot=14)}
  {card}
  {chips(76, 1040 + ch + 50, ACTIVIDADES, 64, 24)}
  <text x="540" y="1640" text-anchor="middle" class="sans" font-weight="700" font-size="32" fill="{INK}">Ven a jugar. Quédate a compartir.</text>
  {pill(340, 1672, 400, 64, INK, CREAM, "@tazonparados", 28)}
'''
    write("plantillas/evento_historia.svg", svg(1080, 1920, "Evento semanal historia", ev_s))

    # --- Foto de perfil (recorte circular) ---
    perfil = f'''
  {background(1080, 1080, TEAL)}
  <circle cx="540" cy="540" r="430" fill="{CREAM}" stroke="{INK}" stroke-width="16"/>
  <use href="#bowl" x="270" y="250" width="540" height="558"/>
'''
    write("plantillas/perfil.svg", svg(1080, 1080, "Foto de perfil", perfil))

    # --- Carrusel "De la idea al aire" (5 láminas 4:5) ---
    def dots(i, n=5, color=INK):
        return "".join(f'<circle cx="{1016 - (n-1-j)*30}" cy="1290" r="9" fill="{color}" opacity="{1 if j == i else 0.3}"/>' for j in range(n))

    def footer(i, ink):
        return (f'<text x="64" y="1300" class="sans" font-weight="700" font-size="24" fill="{ink}" letter-spacing="3">'
                f'{"DESLIZA →" if i < 4 else "@tazonparados"}</text>{dots(i, color=ink)}')

    car1 = f'''
  {background(1080, 1350, INK, light=True)}
  {corner(1080, SUN, CORAL)}
  {header(110, 104, 1, CREAM)}
  {pill(64, 186, 260, 50, TEAL, INK, "CÓMO FUNCIONA", 20)}
  <text x="60" y="420" class="cond" font-size="176" fill="{CREAM}">DE LA IDEA</text>
  {headline_shadow(60, 610, "AL AIRE.", 200, SUN, shadow=TEAL)}
  <text x="64" y="690" class="sans" font-weight="600" font-size="32" fill="{CREAM}">Encuentros que luego se convierten en sonido.</text>
  <path d="M220,940 H860" stroke="{CREAM}" stroke-width="6" stroke-dasharray="4 18" stroke-linecap="round"/>
  {"".join(f'<circle cx="{cx}" cy="940" r="110" fill="{c}" stroke="{CREAM}" stroke-width="6"/>' + icon(ic, cx, 940, 120) for cx, c, ic in [(220, TEAL, "idea"), (540, CORAL, "dado"), (860, SUN, "microfono")])}
  {"".join(f'<text x="{cx}" y="1110" text-anchor="middle" class="sans" font-weight="700" font-size="24" fill="{CREAM}" letter-spacing="3">{t}</text>' for cx, t in [(220, "POSTULA"), (540, "JUGAMOS"), (860, "AL AIRE")])}
  {sparkle(960, 300, 60, SUN)}
  {footer(0, CREAM)}
'''
    write("plantillas/carrusel_01.svg", svg(1080, 1350, "Carrusel 1/5 portada", car1))

    for i, (st, bg, ic) in enumerate(zip(BRAND["process"], [TEAL, CORAL, SUN], ["idea", "dado", "microfono"]), start=1):
        title = wrap(st["title"].upper(), 14)
        body = wrap(st["text"], 34)
        ty = 640
        tl = "".join(f'<text x="64" y="{ty + k*118}" class="cond" font-size="124" fill="{INK}">{l}</text>' for k, l in enumerate(title))
        by = ty + len(title) * 118 + 40
        bl = "".join(f'<tspan x="64" y="{by + k*50}">{l}</tspan>' for k, l in enumerate(body))
        slide = f'''
  {background(1080, 1350, bg)}
  {header(110, 104, 1, INK)}
  {headline_shadow(56, 470, f"0{i}", 330, CREAM, off=14)}
  <circle cx="830" cy="350" r="170" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>
  {icon(ic, 830, 350, 200)}
  {sparkle(1000, 190, 50, INK)}
  {tl}
  <text class="sans" font-weight="600" font-size="38" fill="{INK}">{bl}</text>
  {pill(64, 1150, 360, 60, INK, CREAM, st["short"].upper(), 22)}
  {footer(i, INK)}
'''
        write(f"plantillas/carrusel_0{i+1}.svg", svg(1080, 1350, f"Carrusel {i+1}/5 {st['title']}", slide))

    card, ch = info_card(64, 520, 952, AGENDA, 40)
    car5 = f'''
  {background(1080, 1350, INK, light=True)}
  {corner(1080, TEAL, CORAL)}
  {header(110, 104, 1, CREAM)}
  <text x="60" y="330" class="cond" font-size="150" fill="{CREAM}">VEN A JUGAR.</text>
  <text x="60" y="440" class="cond" font-size="96" fill="{SUN}">QUÉDATE A COMPARTIR.</text>
  {card}
  {pill(64, 520 + ch + 70, 560, 80, SUN, INK, "POSTULA TU IDEA →", 28, shadow=False)}
  <text x="64" y="{520 + ch + 210}" class="sans" font-weight="700" font-size="30" fill="{CREAM}">tazon-para-dos.online</text>
  {d20(900, 1040, 110, rot=12, fill=TEAL, inner=TEAL_L)}
  {footer(4, CREAM)}
'''
    write("plantillas/carrusel_05.svg", svg(1080, 1350, "Carrusel 5/5 cierre", car5))

    # --- Portadas de historias destacadas ---
    for slug, label, bg, ic, ink in [("rol", "ROL", TEAL, "d20", INK), ("mesa", "MESA", CORAL, "dado", INK),
                                     ("podcast", "PODCAST", INK, "microfono", CREAM), ("convocatoria", "CONVOCA", SUN, "idea", INK),
                                     ("ubicacion", "LLEGAR", TEAL, "ubicacion", INK), ("horario", "HORARIO", CORAL, "reloj", INK)]:
        hl = f'''
  {background(1080, 1920, bg, light=(bg == INK))}
  <circle cx="540" cy="960" r="330" fill="{CREAM}" stroke="{INK}" stroke-width="12"/>
  {icon(ic, 540, 960, 380, INK, stroke=3.5)}
  <text x="540" y="1420" text-anchor="middle" class="cond" font-size="90" fill="{ink}" letter-spacing="4">{label}</text>
'''
        write(f"plantillas/destacada_{slug}.svg", svg(1080, 1920, f"Destacada {label}", hl))

    # --- Podcast: portada del show y de episodio (3000 x 3000) ---
    pod = f'''
  {background(1080, 1080, INK, light=True)}
  {corner(1080, SUN, CORAL, 200)}
  {pill(390, 70, 300, 56, TEAL, INK, "PODCAST DE ROL", 22)}
  <circle cx="540" cy="440" r="250" fill="{TEAL}" stroke="{CREAM}" stroke-width="10"/>
  <use href="#bowl" x="390" y="290" width="300" height="310"/>
  {d20(800, 250, 70, rot=16, num=True)}
  {sparkle(250, 260, 60, SUN)}
  {sparkle(860, 600, 40, CREAM)}
  {headline_shadow(540, 850, "TAZÓN PARA DOS", 150, CREAM, shadow=TEAL, off=10, anchor="middle")}
  <text x="540" y="940" text-anchor="middle" class="sans" font-weight="600" font-style="italic" font-size="40" fill="{SUN}">Cada episodio es un platillo distinto.</text>
  <text x="540" y="1020" text-anchor="middle" class="sans" font-weight="700" font-size="22" fill="{CREAM}" letter-spacing="6" opacity="0.8">ENGATIVÁ · BOGOTÁ</text>
'''
    write("plantillas/podcast_portada.svg",
          svg(1080, 1080, "Portada del podcast", pod).replace('width="1080" height="1080"', 'width="3000" height="3000"', 1))

    def episodio(slug, menu, title, bg, accent):
        lines = wrap(title.upper(), 12)
        y0 = 900 - (len(lines) - 1) * 130
        tl = "".join(headline_shadow(540, y0 + k * 130, l, 140, INK if bg != INK else CREAM,
                                     shadow=CREAM if bg != INK else TEAL, off=8, anchor="middle") for k, l in enumerate(lines))
        body = f'''
  {background(1080, 1080, bg, light=(bg == INK))}
  {corner(1080, accent, CREAM, 160)}
  {header(100, 96, 0.9, INK if bg != INK else CREAM, sub="PODCAST DE ROL")}
  {pill(64, 170, len(menu) * 17 + 70, 52, INK, CREAM, menu, 22)}
  <circle cx="540" cy="{y0 - 330}" r="210" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>
  <circle cx="540" cy="{y0 - 330}" r="160" fill="none" stroke="{INK}" stroke-width="3" opacity="0.25"/>
  {d20(540, y0 - 340, 120, rot=-10, fill=accent if accent != CREAM else SUN)}
  {sparkle(820, y0 - 480, 56, CREAM)}
  {tl}
'''
        write(f"plantillas/podcast_episodio_{slug}.svg",
              svg(1080, 1080, f"Portada episodio {title}", body).replace('width="1080" height="1080"', 'width="3000" height="3000"', 1))

    episodio("ejemplo", "MENÚ · DESSERT", "Press Start", SUN, CORAL)
    episodio("plantilla", "MENÚ · MESA PRINCIPAL", "[Título del episodio]", CORAL, TEAL)


# ------------------------------------------------------------------ papelería, espacio y merch
LONA = "#E9E0D6"  # color de tela cruda (del CSS del sitio), solo para mockups
CONTACTO = [("web", "tazon-para-dos.online"), ("camara", "@tazonparados"),
            ("ubicacion", f'{LOC["address"]} · {LOC["locality"]}'), ("reloj", "Sábados · 11:00 a.m. – 9:00 p.m.")]


def field(x, y, w, h, label, lines=0, size=20):
    """Caja de formulario con etiqueta en mayúscula y renglones opcionales."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>',
           f'<text x="{x+22}" y="{y+size+16}" class="sans" font-weight="700" font-size="{size}" fill="{INK}" letter-spacing="3">{label}</text>']
    if lines:
        top = y + size + 40
        step = (h - (size + 40) - 16) / lines
        for k in range(1, lines + 1):
            ly = top + step * k - step / 2 + 6
            out.append(f'<line x1="{x+22}" y1="{ly:.0f}" x2="{x+w-22}" y2="{ly:.0f}" stroke="{INK}" stroke-width="2" opacity="0.18"/>')
    return "\n  ".join(out)


def build_print():
    # --- Tarjeta de presentación 85 x 55 mm (12 px/mm) ---
    frente = f'''
  {background(1020, 660, TEAL)}
  {corner(1020, SUN, CORAL, 150)}
  <circle cx="510" cy="250" r="128" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>
  <use href="#bowl" x="428" y="168" width="164" height="170"/>
  <text x="510" y="478" text-anchor="middle" class="cond" font-size="92" fill="{INK}" letter-spacing="1">TAZÓN PARA DOS</text>
  <text x="510" y="528" text-anchor="middle" class="sans" font-weight="600" font-size="22" fill="{INK}" letter-spacing="9">ESPACIO CULTURAL</text>
  {sparkle(130, 130, 50, SUN)}
  {sparkle(880, 520, 36, CREAM)}
'''
    write("aplicaciones/tarjeta_frente.svg", svg(1020, 660, "Tarjeta de presentación (frente) 85x55 mm", frente))
    rows = "".join(icon(ic, 96, 250 + k * 78, 48) +
                   f'<text x="140" y="{262 + k*78}" class="sans" font-weight="700" font-size="32" fill="{INK}">{t}</text>'
                   for k, (ic, t) in enumerate(CONTACTO))
    reverso = f'''
  {background(1020, 660, CREAM)}
  <text x="64" y="140" class="cond" font-size="72" fill="{INK}">JUGAR TAMBIÉN ES ESCUCHAR.</text>
  {rows}
  <path d="M0,600 L1020,560 L1020,660 L0,660 Z" fill="{CORAL}"/>
  <path d="M0,590 L1020,550 L1020,560 L0,600 Z" fill="{SUN}"/>
  {d20(890, 330, 90, rot=12)}
'''
    write("aplicaciones/tarjeta_reverso.svg", svg(1020, 660, "Tarjeta de presentación (reverso) 85x55 mm", reverso))

    # --- Letrero de horario A4 vertical (1240 x 1754 ≈ 150 dpi) ---
    letrero = f'''
  {background(1240, 1754, TEAL)}
  {corner(1240, SUN, CORAL, 240)}
  {header(130, 130, 1.4, INK)}
  {pill(76, 270, 330, 70, INK, CREAM, "ABRIMOS", 30)}
  <text x="70" y="540" class="cond" font-size="230" fill="{INK}">LOS SÁBADOS</text>
  {headline_shadow(70, 730, "11 A.M. – 9 P.M.", 190, CREAM, off=12)}
  <path d="M0,840 L1240,770 L1240,815 L0,885 Z" fill="{CREAM}"/>
  <path d="M0,885 L1240,815 L1240,1340 L0,1400 Z" fill="{CORAL}"/>
  <path d="M0,885 L1240,815 L1240,1340 L0,1400 Z" fill="url(#dots)"/>
  <ellipse cx="620" cy="1300" rx="360" ry="26" fill="{INK}" opacity="0.22"/>
  {card(330, 1110, 1.1, rot=-14)}
  {d20(620, 1090, 200, rot=-8)}
  <use href="#meeple" x="840" y="1060" width="170" height="170" fill="{INK}"/>
  {d6(990, 1250, 1.0)}
  {sparkle(160, 920, 56, INK)}
  {sparkle(1060, 900, 44, CREAM)}
  <path d="M0,1400 L1240,1340 L1240,1754 L0,1754 Z" fill="{INK}"/>
  <text x="620" y="1500" text-anchor="middle" class="sans" font-weight="700" font-size="36" fill="{CREAM}" letter-spacing="6">ROL · JUEGOS DE MESA · PODCAST</text>
  <text x="620" y="1570" text-anchor="middle" class="cond" font-size="60" fill="{SUN}">UN ESPACIO SEGURO PARA CREAR EN COMUNIDAD.</text>
  <text x="620" y="1660" text-anchor="middle" class="sans" font-weight="600" font-size="32" fill="{CREAM}">{LOC["address"]} · {LOC["locality"]} · @tazonparados</text>
'''
    write("aplicaciones/letrero_horario_a4.svg", svg(1240, 1754, "Letrero de horario A4", letrero))

    # --- Ficha de personaje A4 (pensada para imprimir en blanco y negro también) ---
    ficha = f'''
  <rect width="1240" height="1754" fill="{C["paper"]}"/>
  <rect width="1240" height="230" fill="{TEAL}"/><rect width="1240" height="230" fill="url(#dots)"/>
  {corner(1240, SUN, CORAL, 150)}
  <circle cx="140" cy="115" r="72" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>
  <use href="#bowl" x="95" y="68" width="90" height="93"/>
  <text x="240" y="125" class="cond" font-size="96" fill="{INK}">FICHA DE PERSONAJE</text>
  <text x="243" y="168" class="sans" font-weight="600" font-size="22" fill="{INK}" letter-spacing="6">TAZÓN PARA DOS · LA MESA ES UN TERRITORIO</text>
  {field(60, 270, 740, 110, "NOMBRE DEL PERSONAJE")}
  {field(820, 270, 360, 110, "PRONOMBRES")}
  {field(60, 400, 560, 110, "PERSONA QUE JUEGA")}
  {field(640, 400, 540, 110, "CONCEPTO / ROL")}
  {field(60, 530, 1120, 330, "¿QUIÉN ES? · SU HISTORIA", lines=5)}
  {field(60, 880, 550, 400, "RASGOS Y HABILIDADES", lines=7)}
  {field(630, 880, 550, 400, "INVENTARIO", lines=7)}
  {field(60, 1300, 550, 300, "VÍNCULOS", lines=5)}
  {field(630, 1300, 550, 300, "NOTAS DE LA MESA", lines=5)}
  {d20(1150, 1660, 46, rot=12)}
  <text x="60" y="1690" class="sans" font-weight="700" font-size="22" fill="{INK}" letter-spacing="3">tazon-para-dos.online · @tazonparados</text>
'''
    write("aplicaciones/ficha_personaje_a4.svg", svg(1240, 1754, "Ficha de personaje A4", ficha))

    # --- Certificado de taller A4 horizontal ---
    cert = f'''
  {background(1754, 1240, CREAM)}
  <rect x="40" y="40" width="1674" height="1160" rx="40" fill="none" stroke="{INK}" stroke-width="8"/>
  <path d="M40,80 a40,40 0 0 1 40,-40 H360 L180,1200 H80 a40,40 0 0 1 -40,-40 Z" fill="{TEAL}"/>
  <path d="M360,40 H410 L230,1200 H180 Z" fill="{SUN}"/>
  <circle cx="200" cy="230" r="110" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>
  <use href="#bowl" x="130" y="158" width="140" height="145"/>
  {d20(170, 1000, 90, rot=-12)}
  {sparkle(1600, 160, 70, CORAL)}
  {sparkle(1520, 260, 36, SUN)}
  {pill(520, 150, 420, 64, INK, CREAM, "TAZÓN PARA DOS", 26)}
  <text x="515" y="360" class="cond" font-size="150" fill="{INK}">CERTIFICADO</text>
  <text x="520" y="440" class="cond" font-size="80" fill="{CORAL}">DE PARTICIPACIÓN</text>
  <text x="520" y="540" class="sans" font-weight="600" font-size="34" fill="{INK}">Se otorga a</text>
  <text x="520" y="660" class="cond" font-size="110" fill="{INK}">[NOMBRE COMPLETO]</text>
  <line x1="520" y1="690" x2="1600" y2="690" stroke="{INK}" stroke-width="4"/>
  <text class="sans" font-weight="600" font-size="34" fill="{INK}">
    <tspan x="520" y="770">por su participación en el taller</tspan>
    <tspan x="520" y="825" font-weight="700">[NOMBRE DEL TALLER]</tspan>
  </text>
  <text x="520" y="900" class="sans" font-weight="600" font-size="28" fill="{C["muted"]}">Engativá, Bogotá · [FECHA]</text>
  <line x1="520" y1="1080" x2="960" y2="1080" stroke="{INK}" stroke-width="3"/>
  <line x1="1120" y1="1080" x2="1560" y2="1080" stroke="{INK}" stroke-width="3"/>
  <text x="740" y="1120" text-anchor="middle" class="sans" font-weight="700" font-size="24" fill="{INK}" letter-spacing="3">TAZÓN PARA DOS</text>
  <text x="1340" y="1120" text-anchor="middle" class="sans" font-weight="700" font-size="24" fill="{INK}" letter-spacing="3">PERSONA FACILITADORA</text>
'''
    write("aplicaciones/certificado_taller.svg", svg(1754, 1240, "Certificado de taller A4 horizontal", cert))

    # --- Mockups de merch ---
    sello_mini = (lambda x, y, s: f'<circle cx="{x}" cy="{y}" r="{60*s}" fill="{CREAM}" stroke="{INK}" stroke-width="{5*s}"/>'
                  f'<use href="#bowl" x="{x-40*s}" y="{y-42*s}" width="{80*s}" height="{83*s}"/>')
    merch = f'''
  {background(1620, 1080, CREAM)}
  <text x="60" y="110" class="cond" font-size="72" fill="{INK}">MERCH · PROPUESTAS</text>
  <rect x="60" y="170" width="480" height="760" rx="36" fill="{TEAL}"/><rect x="570" y="170" width="480" height="760" rx="36" fill="{CORAL}"/><rect x="1080" y="170" width="480" height="760" rx="36" fill="{SUN}"/>
  <!-- tazón / taza -->
  <ellipse cx="300" cy="790" rx="170" ry="22" fill="{INK}" opacity="0.22"/>
  <path d="M410,470 a70,70 0 0 1 0,160" fill="none" stroke="{INK}" stroke-width="22"/>
  <path d="M410,470 a70,70 0 0 1 0,160" fill="none" stroke="{CREAM}" stroke-width="10"/>
  <path d="M150,400 H430 V720 a40,40 0 0 1 -40,40 H190 a40,40 0 0 1 -40,-40 Z" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>
  <ellipse cx="290" cy="400" rx="140" ry="26" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>
  <use href="#bowl" x="215" y="500" width="150" height="155"/>
  <!-- bolsa de tela -->
  <ellipse cx="810" cy="860" rx="190" ry="20" fill="{INK}" opacity="0.22"/>
  <path d="M740,420 C740,280 880,280 880,420" fill="none" stroke="{INK}" stroke-width="18"/>
  <path d="M740,420 C740,280 880,280 880,420" fill="none" stroke="{LONA}" stroke-width="8"/>
  <path d="M640,410 H980 L1000,850 H620 Z" fill="{LONA}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  {sello_mini(810, 560, 1.3)}
  <text x="810" y="720" text-anchor="middle" class="cond" font-size="58" fill="{INK}">TAZÓN PARA DOS</text>
  <text x="810" y="760" text-anchor="middle" class="sans" font-weight="600" font-size="16" fill="{INK}" letter-spacing="6">ESPACIO CULTURAL</text>
  <!-- dados -->
  <ellipse cx="1320" cy="800" rx="200" ry="22" fill="{INK}" opacity="0.22"/>
  {d20(1250, 560, 130, rot=-10)}
  {d20(1430, 700, 90, rot=14, fill=TEAL, inner=TEAL_L)}
  {d6(1180, 760, 0.9)}
  {"".join(f'<text x="{x}" y="1000" text-anchor="middle" class="sans" font-weight="700" font-size="26" fill="{INK}" letter-spacing="4">{t}</text>' for x, t in [(300, "TAZA / TAZÓN"), (810, "BOLSA DE TELA"), (1320, "SET DE DADOS")])}
'''
    write("aplicaciones/merch_mockups.svg", svg(1620, 1080, "Mockups de merch (propuestas)", merch))

    # --- Favicon ---
    write("assets/logo/favicon.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"><title>Favicon Tazón para Dos</title>'
          f'<circle cx="32" cy="32" r="31" fill="{TEAL}"/><g transform="translate(9,9) scale(0.383)">{bowl_shapes()}</g></svg>\n')


# ------------------------------------------------------------------ datos para el editor web
def build_editor_data():
    data = {
        "colors": C,
        "tints": {k: v["value"] for k, v in T["color"]["tint"].items()},
        "icons": {k: {"label": v[0], "body": v[1]} for k, v in ICONS.items()},
        "location": LOC,
        "links": BRAND["identity"]["links"],
        "process": BRAND["process"],
        "podcastMenu": BRAND["podcast"]["menu_sections"],
        "bowl": bowl_shapes(),
    }
    write("editor/brand-data.js",
          "// Generado por tools/build.py a partir de brand/*.json. No editar a mano.\n"
          "window.TPD = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")


if __name__ == "__main__":
    print("Construyendo kit de marca en", ROOT)
    build_css()
    build_logos()
    build_icons()
    build_elements()
    build_templates()
    normalize_static()
    build_stickers()
    build_social()
    build_print()
    build_editor_data()
    print("Listo. Ejecuta tools/render.ps1 para exportar PNG.")
