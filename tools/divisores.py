"""Divisores de Tazón para Dos: genera las propuestas en los tres modos (claro, noche y pergamino).

Fuente única de los divisores para:
  - el kit de marca          -> assets/divisores/<modo>/<nombre>.svg, assets/divisores/divisores-<modo>.css, divisores.html
  - el kit Tinieblas         -> D:/tazon-para-dos-tinieblas/assets/divisores/<modo>/ y divisores-<modo>.css (lo usa su build.py)
  - la herramienta de historias -> D:/herramientas/pdf-historias/marca/divisores-claro.css (lo usa maquetar.py)

    python -I tools/divisores.py
"""
import math
import re
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
TINIEBLAS = Path(r"D:\tazon-para-dos-tinieblas")
HERRAMIENTA = Path(r"D:\herramientas\pdf-historias")

# Paletas por modo: a/b/c = rellenos, t = contorno, l = líneas laterales, fondo = página de muestra
MODOS = {
    "claro": dict(a="#55C4BF", b="#F8CB67", c="#EA6077", crema="#F7F2E8", t="#28203B", l="#28203B", fondo="#FFFDF8",
                  texto="#28203B", nombre="Tazón · claro"),
    "noche": dict(a="#7FA68C", b="#E3B35C", c="#E07D84", crema="#E9DDC1", t="#0B0811", l="#A39AB0", fondo="#1C1629",
                  texto="#CFCADF", nombre="Tinieblas · noche"),
    "pergamino": dict(a="#3E5E50", b="#E3B35C", c="#9E3A48", crema="#F3EAD3", t="#28203B", l="#28203B", fondo="#E9DDC1",
                      texto="#28203B", nombre="Tinieblas · pergamino"),
}
ALTO_MM = 8.0  # alto del divisor en la página


def destello(cx, cy, r, fill, t, sw=2.2):
    k1, k2 = r * 0.12, r * 0.2
    d = (f"M{cx},{cy - r} C{cx + k1},{cy - k2} {cx + k2},{cy - k1} {cx + r},{cy} "
         f"C{cx + k2},{cy + k1} {cx + k1},{cy + k2} {cx},{cy + r} C{cx - k1},{cy + k2} {cx - k2},{cy + k1} {cx - r},{cy} "
         f"C{cx - k2},{cy - k1} {cx - k1},{cy - k2} {cx},{cy - r}Z")
    return f'<path d="{d}" fill="{fill}" stroke="{t}" stroke-width="{sw}" stroke-linejoin="round"/>'


def d6(cx, cy, s, rot, fill, t, pip):
    h = s / 2
    pips = "".join(f'<circle cx="{cx + dx * s * .26:.1f}" cy="{cy + dy * s * .26:.1f}" r="{s * .085:.1f}" fill="{pip}"/>'
                   for dx, dy in ((-1, -1), (1, 1), (0, 0), (1, -1), (-1, 1)))
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx - h + 2.5}" y="{cy - h + 2.5}" width="{s}" height="{s}" rx="{s * .2:.1f}" fill="{t}"/>'
            f'<rect x="{cx - h}" y="{cy - h}" width="{s}" height="{s}" rx="{s * .2:.1f}" fill="{fill}" stroke="{t}" stroke-width="2.4"/>{pips}</g>')


def d20(cx, cy, r, fill, t):
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(-90, 270, 60)]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    sombra = " ".join(f"{x + 2.5:.1f},{y + 2.5:.1f}" for x, y in pts)
    (x0, y0), (x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5) = pts
    ti = f"{cx:.1f},{cy - r * .45:.1f} {cx + r * .5:.1f},{cy + r * .38:.1f} {cx - r * .5:.1f},{cy + r * .38:.1f}"
    lineas = (f'M{x0:.1f} {y0:.1f}L{cx:.1f} {cy - r * .45:.1f}M{x2:.1f} {y2:.1f}L{cx + r * .5:.1f} {cy + r * .38:.1f}'
              f'M{x4:.1f} {y4:.1f}L{cx - r * .5:.1f} {cy + r * .38:.1f}M{x1:.1f} {y1:.1f}L{cx + r * .5:.1f} {cy + r * .38:.1f}'
              f'M{x3:.1f} {y3:.1f}L{cx - r * .5:.1f} {cy + r * .38:.1f}M{x5:.1f} {y5:.1f}L{cx:.1f} {cy - r * .45:.1f}')
    return (f'<polygon points="{sombra}" fill="{t}"/><polygon points="{poly}" fill="{fill}" stroke="{t}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<polygon points="{ti}" fill="none" stroke="{t}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="{lineas}" stroke="{t}" stroke-width="1.6"/>')


def meeple(cx, cy, s, fill, t):
    # Meeple simplificado (cabeza, brazos y piernas), alto ≈ s
    k = s / 30
    d = ("M0,-15 C4,-15 6,-12 6,-9 C6,-7 5,-6 4,-5 L12,-2 C15,-1 15,3 12,3 L6,3 L10,13 C11,15 9,16 7,15 L0,8 "
         "L-7,15 C-9,16 -11,15 -10,13 L-6,3 L-12,3 C-15,3 -15,-1 -12,-2 L-4,-5 C-5,-6 -6,-7 -6,-9 C-6,-12 -4,-15 0,-15Z")
    def tr(dx, dy):
        return re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)",
                      lambda m: f"{cx + dx + float(m.group(1)) * k:.1f},{cy + dy + float(m.group(2)) * k:.1f}", d)
    return f'<path d="{tr(2.5, 2.5)}" fill="{t}"/><path d="{tr(0, 0)}" fill="{fill}" stroke="{t}" stroke-width="2.2" stroke-linejoin="round"/>'


def disenos(p):
    a, b, c, t, cr = p["a"], p["b"], p["c"], p["t"], p["crema"]
    D = {}
    # 1. Cinta: tres tiras cortas inclinadas, con sombra dura
    tiras = ""
    for i, col in enumerate((a, b, c)):
        x = 8 + i * 48
        forma = lambda dx, dy: f"{x + dx},{29 + dy} {x + 12 + dx},{11 + dy} {x + 52 + dx},{11 + dy} {x + 40 + dx},{29 + dy}"
        tiras += f'<polygon points="{forma(3, 3)}" fill="{t}"/><polygon points="{forma(0, 0)}" fill="{col}" stroke="{t}" stroke-width="2.4" stroke-linejoin="round"/>'
    D["cinta"] = dict(w=168, lineas="solida", svg=tiras, nota="Tres tiras de color con sombra cómic. Enérgico, para separar escenas.")
    # 2. Destellos: uno grande coral entre dos pequeños sol
    D["destellos"] = dict(w=120, lineas="solida", svg=destello(30, 20, 8, b, t) + destello(60, 20, 16, c, t) + destello(90, 20, 8, b, t),
                          nota="Editorial y ligero. El más discreto: va bien en texto largo.")
    # 3. Dados: d6 · d20 · d6
    D["dados"] = dict(w=150, lineas="solida", svg=d6(32, 21, 22, -10, cr, t, t) + d20(75, 20, 17, b, t) + d6(118, 21, 22, 10, a, t, t),
                      nota="El más «de mesa». Para historias de rol y crónicas de partida.")
    # 4. Puntos: la trama de la marca convertida en línea
    radios = [2.2, 3, 4, 5.2, 7, 5.2, 4, 3, 2.2]
    xs, x = [], 6
    for r in radios:
        x += r; xs.append(x); x += r + 6
    cols = [a, b, c, a, c, a, c, b, a]
    pts = "".join(f'<circle cx="{xx:.1f}" cy="20" r="{r}" fill="{col}"' + (f' stroke="{t}" stroke-width="2"' if r > 5 else "") + "/>"
                  for xx, r, col in zip(xs, radios, cols))
    D["puntos"] = dict(w=round(x), lineas="ninguna", svg=pts, nota="La trama de puntos hecha línea. Suave, sin líneas laterales.")
    # 5. Escalón: la diagonal de siempre, corta y centrada
    esc = ""
    for k, col in enumerate((a, b, c)):
        x0, y0 = 10 + k * 66, 27 - k * 6.5
        forma = lambda dx, dy: f"{x0 + dx},{y0 + dy} {x0 + 70 + dx},{y0 - 14 + dy} {x0 + 70 + dx},{y0 - 4 + dy} {x0 + dx},{y0 + 10 + dy}"
        esc += f'<polygon points="{forma(3, 3)}" fill="{t}"/><polygon points="{forma(0, 0)}" fill="{col}" stroke="{t}" stroke-width="2.2" stroke-linejoin="round"/>'
    D["escalon"] = dict(w=220, lineas="ninguna", svg=esc,
                        nota="La diagonal de la marca en tres escalones cortos que suben a la derecha, con sombra.")
    # 6. Camino: sendero punteado con un meeple
    D["camino"] = dict(w=150, lineas="punteada",
                       svg=(f'<path d="M4 24 C30 14 46 30 75 22 C104 14 120 30 146 20" fill="none" stroke="{t}" stroke-width="2.4" stroke-dasharray="5 5" stroke-linecap="round"/>'
                            + destello(24, 12, 5, b, t, 1.6) + meeple(75, 19, 26, c, t) + destello(126, 12, 5, b, t, 1.6)),
                       nota="Un meeple en el camino: para transiciones de lugar o de tiempo.")
    # 7. Tazón: el tazón con vapor, guiño al nombre
    D["tazon"] = dict(w=110, lineas="solida",
                      svg=(f'<path d="M37 21 H75 C75 31 67 37 56 37 C45 37 37 31 37 21Z" fill="{t}" transform="translate(2.5 2.5)"/>'
                           f'<path d="M35 21 H77 C77 31 68 37 56 37 C44 37 35 31 35 21Z" fill="{a}" stroke="{t}" stroke-width="2.4" stroke-linejoin="round"/>'
                           f'<rect x="33" y="18" width="46" height="5" rx="2.5" fill="{cr}" stroke="{t}" stroke-width="2.2"/>'
                           f'<path d="M48 14 c-3 -4 3 -6 0 -10 M56 14 c-3 -4 3 -6 0 -10 M64 14 c-3 -4 3 -6 0 -10" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>'
                           + destello(18, 22, 6, b, t, 1.6) + destello(94, 22, 6, b, t, 1.6)),
                      nota="El tazón con vapor: firma de la casa, para cerrar capítulos.")
    # 8. Luna: creciente con estrellas (pensado para Tinieblas)
    f = p["fondo"]
    D["luna"] = dict(w=150, lineas="niebla",
                     svg=(f'<circle cx="77.5" cy="22.5" r="15" fill="{t}"/><circle cx="75" cy="20" r="15" fill="{b}" stroke="{t}" stroke-width="2.2"/>'
                          f'<circle cx="83" cy="15" r="12.5" fill="{f}"/>'
                          f'<path d="M71.2 34.6 A15 15 0 0 1 70.6 5.7" fill="none" stroke="{t}" stroke-width="2.2" stroke-linecap="round"/>'
                          + destello(30, 16, 6, cr, t, 1.6) + destello(46, 28, 3.6, b, t, 1.3)
                          + destello(110, 12, 4, b, t, 1.3) + destello(124, 27, 6, cr, t, 1.6)),
                     nota="Luna creciente y estrellas. La más nocturna: ideal en modo Tinieblas.")
    # 9. Greca muisca: escalonado geométrico con rombo central
    paso = ""
    for i in range(6):
        x0 = 8 + i * 40
        paso += f"M{x0} 30 h10 v-12 h10 v-8 h10 v8 h10" if i < 5 else ""
    greca = (f'<path d="{paso}" fill="none" stroke="{t}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" transform="translate(2 2)"/>'
             f'<path d="{paso}" fill="none" stroke="{b}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
             f'<polygon points="108,8 120,20 108,32 96,20" fill="{c}" stroke="{t}" stroke-width="2.2" stroke-linejoin="round"/>')
    D["greca"] = dict(w=216, lineas="ninguna", svg=greca, nota="Geometría escalonada de inspiración muisca. Respetuosa, sin copiar piezas reales.")
    # 10. Zarpazo: tres marcas inclinadas (Hombre Lobo)
    garras = ""
    for i, dx in enumerate((0, 14, 28)):
        d = f"M{40 + dx} 36 C{44 + dx} 26 {52 + dx} 14 {62 + dx} 4 C{58 + dx} 16 {52 + dx} 28 {46 + dx} 37Z"
        garras += f'<path d="{d}" fill="{t}" transform="translate(2.5 1.5)"/><path d="{d}" fill="{c}" stroke="{t}" stroke-width="2" stroke-linejoin="round"/>'
    D["zarpazo"] = dict(w=140, lineas="solida", svg=garras + destello(18, 20, 5, b, t, 1.5) + destello(122, 20, 5, b, t, 1.5),
                        nota="Tres zarpazos que suben a la derecha. Para escenas de Hombre Lobo o de tensión.")
    return D


def svg_de(w, cuerpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40">{cuerpo}</svg>'


def uri(svg):
    s = re.sub(r"\s+", " ", svg.strip())
    return "data:image/svg+xml;utf8," + s.replace("#", "%23").replace('"', "'")


def css_modo(modo, D):
    p = MODOS[modo]
    reglas = [f"/* Divisores Tazón para Dos · {p['nombre']} · generado por tools/divisores.py */"]
    for nombre, x in D.items():
        ancho_mm = x["w"] / 40 * ALTO_MM
        hueco = f"calc(50% - {ancho_mm / 2 + 3:.1f}mm)"
        capas = [f'url("{uri(svg_de(x["w"], x["svg"]))}") center/auto 100% no-repeat']
        if x["lineas"] in ("solida", "niebla"):
            col = p["l"]
            op = "1.1pt" if x["lineas"] == "solida" else "0.9pt"
            capas += [f"linear-gradient({col},{col}) left center/{hueco} {op} no-repeat",
                      f"linear-gradient({col},{col}) right center/{hueco} {op} no-repeat"]
        elif x["lineas"] == "punteada":
            g = f"repeating-linear-gradient(90deg,{p['l']} 0 1.6mm,transparent 1.6mm 3.2mm)"
            capas += [f"{g} left center/{hueco} 1.2pt no-repeat", f"{g} right center/{hueco} 1.2pt no-repeat"]
        reglas.append(f".divisor.d-{nombre}{{height:{ALTO_MM}mm;background:{','.join(capas)}}}"
                      f".divisor.d-{nombre}::after{{content:none}}")
    return "\n".join(reglas) + "\n"


def pagina(todos):
    filas = []
    for nombre in todos["claro"]:
        celdas = []
        for modo, p in MODOS.items():
            x = todos[modo][nombre]
            celdas.append(
                f'<div class="muestra" style="background:{p["fondo"]};color:{p["texto"]}">'
                f'<p>…y la niebla tocó tres veces la puerta. Nadie en el barrio se atrevió a abrir.</p>'
                f'<div class="divisor d-{nombre} m-{modo}"></div>'
                f'<p>A la mañana siguiente, la plaza amaneció llena de hojas de eucalipto.</p>'
                f'<span class="modo">{p["nombre"]}</span></div>')
        nota = todos["claro"][nombre]["nota"]
        filas.append(f'<section class="fila" id="{nombre}"><header><span class="pildora">{nombre}</span><p>{nota}</p>'
                     f'<code>::: divisor {nombre}</code></header><div class="celdas">{"".join(celdas)}</div></section>')
    css = "".join(css_modo(m, todos[m]).replace(".divisor.d-", f".m-{m}.divisor.d-") for m in MODOS)
    actual = ('<section class="fila" id="diagonal"><header><span class="pildora">diagonal (actual)</span>'
              '<p>La diagonal a todo el ancho que usan hoy las historias. Sigue disponible.</p><code>::: divisor</code></header></section>')
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Divisores Tazón para Dos</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@500&family=DM+Sans:wght@400;600&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
<style>
:root{{--ink:#28203B;--cream:#F7F2E8;--paper:#FFFDF8;--coral:#EA6077;--sun:#F8CB67}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--cream);background-image:radial-gradient(rgba(40,32,59,.10) 1.4px,transparent 1.5px);background-size:22px 22px;color:var(--ink);font:16px/1.55 'DM Sans',sans-serif}}
.wrap{{max-width:1240px;margin:0 auto;padding:28px 16px 60px}}
h1{{font:700 clamp(30px,5vw,48px)/1.05 'Space Grotesk';margin:0 0 8px}}
.lead{{max-width:70ch;margin:0 0 24px}}
.fila{{background:var(--paper);border:2px solid var(--ink);border-radius:16px;box-shadow:5px 5px 0 var(--ink);padding:16px;margin:0 0 22px}}
.fila header{{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin-bottom:12px}}
.fila header p{{margin:0;flex:1;min-width:220px}}
.pildora{{font:500 12px 'DM Mono';letter-spacing:.12em;text-transform:uppercase;background:var(--ink);color:var(--sun);padding:5px 12px;border-radius:999px}}
code{{font:500 13px 'DM Mono';background:var(--cream);border:1.5px solid var(--ink);border-radius:8px;padding:3px 8px}}
.celdas{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}
.muestra{{position:relative;border-radius:10px;padding:16px 18px 30px;border:1.5px solid rgba(40,32,59,.25);font-size:14px}}
.muestra p{{margin:0}}
.muestra .divisor{{margin:14px 0;height:30px!important}}
.modo{{position:absolute;right:10px;bottom:8px;font:500 10.5px 'DM Mono';letter-spacing:.1em;text-transform:uppercase;opacity:.7}}
@media (max-width:820px){{.celdas{{grid-template-columns:1fr}}}}
{css}
</style></head><body><div class="wrap">
<h1>Divisores.</h1>
<p class="lead">Diez propuestas para separar escenas en historias, posts y piezas impresas, cada una en los tres modos de la marca: Tazón claro, Tinieblas noche y Tinieblas pergamino. En una historia se usan con <code>::: divisor nombre</code>, o eligiendo el estilo en el editor.</p>
{actual}
{''.join(filas)}
</div></body></html>"""


def main():
    todos = {m: disenos(p) for m, p in MODOS.items()}
    destinos = [AQUI / "assets" / "divisores"]
    if TINIEBLAS.exists():
        destinos.append(TINIEBLAS / "assets" / "divisores")
    for raiz in destinos:
        for modo, D in todos.items():
            if raiz.parent.parent == TINIEBLAS and modo == "claro":
                continue
            (raiz / modo).mkdir(parents=True, exist_ok=True)
            for nombre, x in D.items():
                (raiz / modo / f"{nombre}.svg").write_text(svg_de(x["w"], x["svg"]), encoding="utf-8")
            (raiz / f"divisores-{modo}.css").write_text(css_modo(modo, D), encoding="utf-8")
    (AQUI / "divisores.html").write_text(pagina(todos), encoding="utf-8")
    if (HERRAMIENTA / "navegacion.py").exists():  # barra común Tazón para Dos (sitios y herramientas)
        import sys
        sys.path.insert(0, str(HERRAMIENTA))
        import navegacion
        navegacion.main([(str(AQUI / "divisores.html"), "divisores")])
    if HERRAMIENTA.exists():
        shutil.copy(AQUI / "assets" / "divisores" / "divisores-claro.css", HERRAMIENTA / "marca" / "divisores-claro.css")
    print("Divisores:", ", ".join(todos["claro"]), "·", len(MODOS), "modos")


if __name__ == "__main__":
    main()
