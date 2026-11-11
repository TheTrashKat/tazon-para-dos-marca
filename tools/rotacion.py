"""Publicación rotativa: cada N días genera la siguiente pieza (juegos de mesa o mesas de rol).

Uso:  python -I tools/rotacion.py              genera la siguiente pieza y la deja pendiente
      python -I tools/rotacion.py --estado     muestra la cola y la próxima fecha

Modo 'aprobar' (default): la pieza queda en salida/rotacion/pendientes.json esperando tu OK.
Modo 'automatico': la pieza se marca lista para que el publicador la envíe (no se envía aquí).
"""
import datetime as dt, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "tools" / "rotacion_config.json").read_text(encoding="utf-8"))
OUT = ROOT / "salida" / "rotacion"
ESTADO = OUT / "estado.json"
OUT.mkdir(parents=True, exist_ok=True)


def cargar_estado():
    if ESTADO.exists():
        return json.loads(ESTADO.read_text(encoding="utf-8"))
    return {"siguiente": 0, "ultima": None, "cola": []}


def proxima_fecha(estado):
    base = dt.date.today() if not estado["ultima"] else dt.date.fromisoformat(estado["ultima"])
    return base + dt.timedelta(days=CFG["cada_dias"])


def elegir(estado):
    """Alterna tipo (juegos / mesas) y rota dentro de cada tipo para no repetir."""
    n = estado["siguiente"]
    tipo = CFG["alternar"][n % len(CFG["alternar"])]
    ciclo = n // len(CFG["alternar"])
    if tipo == "juegos":
        lista = CFG["juegos_de_mesa"]
        item = lista[ciclo % len(lista)]
        grupo = item["juegos"]
        receta = CFG["recetas"][ciclo % len(CFG["recetas"])]
        return tipo, item, receta, grupo
    lista = CFG["mesas_de_rol"]
    item = lista[ciclo % len(lista)]
    receta = CFG["recetas"][ciclo % len(CFG["recetas"])]
    return tipo, item, receta, None


def job_juegos(item, receta, invertir, nombre):
    v = {"receta": receta, "invertir": invertir, "foto": "", "invita": "Tazón para Dos te invita",
         "titulo": item["titulo"], "subtitulo": "Juegos de mesa en Tag Tabú",
         "fecha": CFG["fecha_evento"].split(" · ")[0], "hora": CFG["fecha_evento"].split(" · ")[1],
         "lugar": CFG["lugar"], "contacto": CFG["contacto"]}
    for i, (j, d) in enumerate(item["juegos"][:4], 1):
        v[f"j{i}"], v[f"d{i}"] = j, d
    return [{"template": "ludoteca_post", "values": v, "output": f"salida/rotacion/{nombre}.png"}]


def job_mesas(item, receta, nombre):
    v = {"fondo": "completo", "invita": "Tazón para Dos te invita", "titulo": "Sábado",
         "subtitulo": item["titulo"], "info": CFG["fecha_evento"], "lugar": CFG["lugar"], "contacto": CFG["contacto"]}
    for i, m in enumerate(item["mesas"][:3], 1):
        v[f"n{i}"], v[f"t{i}"], v[f"i{i}"], v[f"h{i}"] = m["nombre"], m["tipo"], m["inicio"], m["horario"]
        v[f"b{i}"], v[f"d{i}"], v[f"p{i}"], v[f"m{i}"], v[f"c{i}"] = m["buscamos"], m["desc"], m["nivel"], m["master"], m["color"]
        v[f"url{i}"] = m.get("url", "")
    return [{"template": "mesas_rol_post", "values": v, "output": f"salida/rotacion/{nombre}.png"}]


def texto(tipo, item):
    if tipo == "juegos":
        lineas = [f"🎲 {item['titulo']}", ""] + [f"• {j}: {d}" for j, d in item["juegos"][:4]]
    else:
        lineas = [f"🎲 {item['titulo']}", ""]
        for m in item["mesas"]:
            lineas.append(f"• {m['nombre']} ({m['tipo']}) · inicia {m['inicio']} · buscamos {m['buscamos']} players")
    lineas += ["", CFG["fecha_evento"], CFG["lugar"], f"Reserva: {CFG['contacto']}", CFG["usuario"]]
    return "\n".join(lineas)


def main():
    if "--estado" in sys.argv:
        e = cargar_estado()
        print(f"Modo: {CFG['modo']} · cada {CFG['cada_dias']} días · próxima: {proxima_fecha(e)}")
        for c in e["cola"]:
            print(f"  [{c['estado']}] {c['fecha']} {c['tipo']}: {c['titulo']}")
        return
    estado = cargar_estado()
    tipo, item, receta, grupo = elegir(estado)
    nombre = f"{estado['siguiente']:03d}_{tipo}"
    invertir = (estado["siguiente"] // len(CFG["alternar"])) % 2 == 1
    jobs = job_juegos(item, receta, invertir, nombre) if tipo == "juegos" else job_mesas(item, receta, nombre)
    jf = OUT / f"{nombre}.json"
    jf.write_text(json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(ROOT / "tools" / "render_editor.py"), str(jf)], check=True, cwd=str(ROOT))
    (OUT / f"{nombre}.txt").write_text(texto(tipo, item), encoding="utf-8")
    fecha = proxima_fecha(estado).isoformat()
    estado["cola"].append({"id": nombre, "fecha": fecha, "tipo": tipo, "titulo": item["titulo"],
                           "estado": "pendiente_aprobacion" if CFG["modo"] == "aprobar" else "listo_automatico"})
    estado["siguiente"] += 1
    estado["ultima"] = fecha
    ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Pieza {nombre} lista ({CFG['modo']}). Imagen y texto en {OUT}.")


if __name__ == "__main__":
    main()
