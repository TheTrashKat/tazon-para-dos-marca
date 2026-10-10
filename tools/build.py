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
    "tazon": ("Tazón", '<path d="M8 32h48c0 13-10 21-24 21S8 45 8 32Z"/><path d="M24 59h16M14 30c0-8 5-13 11-13 2-4 12-4 14 0 6 0 11 5 11 13M17 6l4 6M47 6l-4 6M27 38v5M37 38v5"/>'),
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


if __name__ == "__main__":
    print("Construyendo kit de marca en", ROOT)
    build_css()
    build_logos()
    build_icons()
    build_elements()
    build_templates()
    normalize_static()
    build_stickers()
    print("Listo. Ejecuta tools/render.ps1 para exportar PNG.")
