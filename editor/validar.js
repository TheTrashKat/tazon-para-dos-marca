// Validación automática de las plantillas del editor (la usa tools/validar.py; también se puede abrir validar.html).
// Cada plantilla se pinta dos veces: con sus valores por defecto y con textos largos («estrés»).
// Errores: el render falla, un texto se sale del lienzo, dos textos se enciman, aparece "undefined"/"NaN".
// Avisos: texto en la zona que tapa la interfaz de Instagram, texto pegado al borde o demasiado pequeño.
(async function () {
  const D = window.TPDDraw, TEMPLATES = window.TPDTemplates;
  const FONT_FILES = [
    ["Barlow Condensed", 800, "normal", "BarlowCondensed-ExtraBold.ttf"],
    ["Barlow", 500, "normal", "Barlow-Medium.ttf"],
    ["Barlow", 600, "normal", "Barlow-SemiBold.ttf"],
    ["Barlow", 700, "normal", "Barlow-Bold.ttf"],
    ["Barlow", 600, "italic", "Barlow-SemiBoldItalic.ttf"],
  ];
  const $status = document.getElementById("status");
  await Promise.all(FONT_FILES.map(async ([family, weight, style, file]) => {
    const buf = await (await fetch("../tools/fonts/" + file)).arrayBuffer();
    const face = new FontFace(family, buf, { weight: String(weight), style });
    await face.load();
    document.fonts.add(face);
  }));
  await document.fonts.ready;

  const SKIP = new Set(["guia_zonas"]);
  // Tamaño mínimo de texto a 1080 px de ancho (guías de legibilidad en celular: 24–32 px para texto secundario)
  const MIN_PX = Number(new URLSearchParams(location.search).get("min")) || 22;          // dibuja las zonas a propósito
  const ctx = document.createElement("canvas").getContext("2d");
  const stage = document.getElementById("stage");

  const defaults = (t) => Object.fromEntries(t.fields.map((f) => [f.key, f.default]));
  function stress(t) {
    const v = defaults(t);
    for (const f of t.fields) {
      const d = String(f.default ?? "");
      if (f.type === "text") {
        if (f.key === "usuario") v[f.key] = "@tazonparados.oficial";
        else if (!d) v[f.key] = "ETIQUETA DE PRUEBA BASTANTE LARGA";
        else if (d.length <= 4) v[f.key] = d + d;
        else v[f.key] = d + " CON MÁS PALABRAS";
      } else if (f.type === "textarea") {
        v[f.key] = d ? d + " " + d : "Un texto de prueba bastante largo para ver cómo se acomoda en la plantilla.";
      }
    }
    return v;
  }

  // Caja real de los glifos (no la caja de la fuente) en unidades del lienzo
  function glyphBox(el, svg, R, k) {
    const b = el.getBoundingClientRect();
    if (!b.width || !b.height) return null;
    const cs = getComputedStyle(el);
    const m = svg.getScreenCTM().inverse().multiply(el.getScreenCTM());
    const s = Math.hypot(m.a, m.b);
    const size = parseFloat(cs.fontSize);
    ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${size}px ${cs.fontFamily}`;
    const txt = el.textContent;
    const mm = ctx.measureText(txt);
    const fA = mm.fontBoundingBoxAscent, aA = mm.actualBoundingBoxAscent, aD = mm.actualBoundingBoxDescent, fD = mm.fontBoundingBoxDescent;
    const top = (b.top - R.top) * k, bottom = (b.bottom - R.top) * k;
    // Caja en el sistema propio del texto, desplazada a un marco común sin rotación (para comparar textos con el mismo giro)
    const bb = el.getBBox(), det = m.a * m.d - m.b * m.c;
    const tx = (m.d * m.e - m.c * m.f) / det, ty = (-m.b * m.e + m.a * m.f) / det;
    return {
      m: { a: m.a, b: m.b },
      lx0: bb.x + tx, lx1: bb.x + bb.width + tx, ly0: bb.y + ty + Math.max(0, fA - aA), ly1: bb.y + ty + bb.height - Math.max(0, fD - aD),
      x0: (b.left - R.left) * k, x1: (b.right - R.left) * k,
      y0: top + Math.max(0, fA - aA) * s, y1: bottom - Math.max(0, fD - aD) * s,
      size: size * s, txt: txt.trim(), rotated: Math.abs(m.b) > 0.01,
    };
  }

  function check(t, values) {
    const errors = [], warnings = [];
    let svgText;
    try {
      svgText = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${t.w} ${t.h}" width="${t.w}" height="${t.h}">${D.defs("")}${t.render(values)}</svg>`;
    } catch (e) {
      return { errors: ["El render falló: " + e.message], warnings };
    }
    stage.innerHTML = svgText;
    const svg = stage.querySelector("svg");
    const R = svg.getBoundingClientRect(), k = t.w / R.width;
    const textEls = [...svg.querySelectorAll("text")]
      .filter((el) => el.textContent.trim() && !el.closest("defs, clipPath, [data-guia]") && el.getAttribute("opacity") !== "0");
    const boxes = textEls.map((el) => { const g = glyphBox(el, svg, R, k); if (g) g.el = el; return g; }).filter(Boolean);
    // Formas con relleno dibujadas DESPUÉS de un texto que lo tapan (cintas, stickers, tarjetas…)
    const order = [...svg.querySelectorAll("*")];
    const pos = new Map(order.map((el, i) => [el, i]));
    const shapes = order.filter((el) => /^(rect|path|circle|ellipse|polygon|use|image)$/.test(el.tagName) && !el.closest("defs, clipPath, pattern, symbol, [data-guia], text"))
      .filter((el) => {
        const fill = el.getAttribute("fill") || (el.tagName === "use" || el.tagName === "image" ? "x" : "");
        return fill && fill !== "none" && !/^url\(#dots/.test(fill) && el.getAttribute("opacity") === null && el.getAttribute("fill-opacity") === null;
      })
      .map((el) => { const b = el.getBoundingClientRect(); return { el, i: pos.get(el), x0: (b.left - R.left) * k, x1: (b.right - R.left) * k, y0: (b.top - R.top) * k, y1: (b.bottom - R.top) * k }; });
    const short = (s) => (s.length > 28 ? s.slice(0, 26) + "…" : s);
    // Píldoras (rect con extremos redondos): no deben tapar textos que no son su etiqueta
    const pills = [...svg.querySelectorAll("rect")].filter((el) => !el.closest("defs, clipPath, [data-guia]")).map((el) => {
      const h = +el.getAttribute("height"), rx = +el.getAttribute("rx");
      if (!h || h > 200 || rx * 2 < h * 0.9 || el.getAttribute("fill") === "none" || el.getAttribute("fill-opacity") === "0.35") return null;
      const b = el.getBoundingClientRect();
      return { x0: (b.left - R.left) * k, x1: (b.right - R.left) * k, y0: (b.top - R.top) * k, y1: (b.bottom - R.top) * k };
    }).filter(Boolean);
    const vertical = t.w === 1080 && t.h === 1920;
    const reel = vertical && (t.safe ? t.safe === "reel" : t.group === "Video");
    const scale = 1080 / Math.min(t.w, 1920) * (t.w === 1920 ? 1.6 : 1);   // 16:9 se ve más grande en pantalla completa
    for (const b of boxes) {
      if (/undefined|NaN|\[object/.test(b.txt)) errors.push(`Texto inválido: «${short(b.txt)}»`);
      if (b.x0 < -2 || b.y0 < -2 || b.x1 > t.w + 2 || b.y1 > t.h + 2) errors.push(`Se sale del lienzo: «${short(b.txt)}»`);
      else if (!t.transparent && (b.x0 < 20 || b.x1 > t.w - 20)) warnings.push(`Pegado al borde: «${short(b.txt)}»`);
      if (b.size * scale < MIN_PX) warnings.push(`Texto pequeño (${Math.round(b.size)} px): «${short(b.txt)}»`);
      if (vertical) {
        const bottomLimit = reel ? 1500 : 1670;
        if (b.y0 < 250 - 4 || b.y1 > bottomLimit + 4) warnings.push(`En zona de interfaz de Instagram: «${short(b.txt)}»`);
        else if (reel && !t.cover && b.x1 > 940 && b.y1 > 900 && b.y0 < 1500) warnings.push(`Bajo los botones del Reel: «${short(b.txt)}»`);
        // Portadas de Reel: la cuadrícula del perfil recorta un cuadrado centrado (y 420–1500)
        if (t.cover && (b.y0 < 420 - 4 || b.y1 > 1500 + 4)) warnings.push(`Fuera del recorte de la cuadrícula: «${short(b.txt)}»`);
      }
    }
    for (const b of boxes) {
      const ti = pos.get(b.el);
      for (const s of shapes) {
        if (s.i <= ti) continue;
        const ix = Math.min(b.x1, s.x1) - Math.max(b.x0, s.x0), iy = Math.min(b.y1, s.y1) - Math.max(b.y0, s.y0);
        if (ix > 4 && iy > 4 && (ix * iy) / ((b.x1 - b.x0) * (b.y1 - b.y0)) > 0.03) { errors.push(`Una forma tapa el texto «${short(b.txt)}»`); break; }
      }
    }
    for (const pl of pills) {
      for (const b of boxes) {
        const cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2;
        if (cx > pl.x0 && cx < pl.x1 && cy > pl.y0 && cy < pl.y1) continue;      // es su etiqueta
        const ix = Math.min(b.x1, pl.x1) - Math.max(b.x0, pl.x0), iy = Math.min(b.y1, pl.y1) - Math.max(b.y0, pl.y0);
        if (ix > 6 && iy > 6) errors.push(`Una píldora tapa el texto «${short(b.txt)}»`);
      }
    }
    for (let i = 0; i < boxes.length; i++) {
      for (let j = i + 1; j < boxes.length; j++) {
        let a = boxes[i], c = boxes[j];
        if (a.txt === c.txt) continue;                  // sombra del mismo titular
        // Textos con la misma rotación: se comparan en su propio sistema (evita falsos positivos por la inclinación)
        if ((a.rotated || c.rotated) && Math.abs(a.m.a - c.m.a) < 1e-3 && Math.abs(a.m.b - c.m.b) < 1e-3) {
          a = { ...a, x0: a.lx0, x1: a.lx1, y0: a.ly0, y1: a.ly1 };
          c = { ...c, x0: c.lx0, x1: c.lx1, y0: c.ly0, y1: c.ly1 };
        }
        const ix = Math.min(a.x1, c.x1) - Math.max(a.x0, c.x0), iy = Math.min(a.y1, c.y1) - Math.max(a.y0, c.y0);
        if (iy > 0.3 * Math.min(a.y1 - a.y0, c.y1 - c.y0) && ix <= 0 && ix > -10) {
          errors.push(`Textos pegados: «${short(a.txt)}» y «${short(c.txt)}»`);
          continue;
        }
        if (ix <= 0 || iy <= 0) continue;
        const small = Math.min((a.x1 - a.x0) * (a.y1 - a.y0), (c.x1 - c.x0) * (c.y1 - c.y0));
        if ((ix * iy) / small > 0.12) errors.push(`Textos encimados: «${short(a.txt)}» y «${short(c.txt)}»`);
      }
    }
    return { errors, warnings };
  }

  const results = [];
  for (const t of TEMPLATES) {
    if (SKIP.has(t.id)) continue;
    // Variantes declaradas en la plantilla (p. ej. estilos de subtítulo): cada una con valores normales y de estrés
    const cases = [["normal", defaults(t)], ["estrés", stress(t)]];
    for (const vr of t.variants || []) {
      const tag = Object.values(vr).join("·");
      cases.push([`normal·${tag}`, { ...defaults(t), ...vr }], [`estrés·${tag}`, { ...stress(t), ...vr }]);
    }
    for (const [caso, values] of cases) {
      $status.textContent = `Validando ${t.id} (${caso})…`;
      const r = check(t, values);
      results.push({ id: t.id, name: t.name, group: t.group, caso, values, ...r });
    }
  }
  stage.innerHTML = "";

  const nErr = results.reduce((s, r) => s + r.errors.length, 0), nWarn = results.reduce((s, r) => s + r.warnings.length, 0);
  $status.textContent = `${TEMPLATES.length - SKIP.size} plantillas × 2 casos: ${nErr} errores, ${nWarn} avisos.`;
  document.getElementById("tbl").innerHTML = "<tr><th>Plantilla</th><th>Caso</th><th>Resultado</th></tr>" + results.map((r) =>
    `<tr><td>${D.esc(r.id)}</td><td>${r.caso}</td><td>${r.errors.length || r.warnings.length ? "" : '<span class="ok">OK</span>'}` +
    r.errors.map((e) => `<div class="err">✖ ${D.esc(e)}</div>`).join("") + r.warnings.map((w) => `<div class="warn">⚠ ${D.esc(w)}</div>`).join("") + "</td></tr>").join("");
  const out = document.getElementById("out");
  out.textContent = JSON.stringify(results);
  send(results);
})().catch((e) => {
  document.getElementById("status").textContent = "La validación falló: " + e.message;
  send({ fatal: e.message });
});

// Con ?enviar=1 (tools/validar.py) los resultados se mandan al servidor local
function send(data) {
  if (new URLSearchParams(location.search).get("enviar") === "1") fetch("/resultado", { method: "POST", body: JSON.stringify(data) });
}
