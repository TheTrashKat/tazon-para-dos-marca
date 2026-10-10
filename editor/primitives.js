// Primitivas gráficas de Tazón para Dos (equivalentes a tools/build.py).
// Todas devuelven fragmentos de SVG como texto. Los textos del usuario pasan por esc().
(function () {
  const T = window.TPD;
  const C = T.colors;
  const INK = C.ink, CORAL = C.coral, SUN = C.sun, TEAL = C.teal, CREAM = C.cream;
  const SUN_L = T.tints["sun-light"], TEAL_L = T.tints["teal-light"];
  const FONT = { cond: "'Barlow Condensed', 'Arial Narrow', sans-serif", sans: "'Barlow', 'Segoe UI', sans-serif" };

  const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const n = (v) => Math.round(v * 10) / 10;

  // ---- medición real de texto (requiere fuentes cargadas) ----
  const ctx = document.createElement("canvas").getContext("2d");
  function measure(text, kind = "cond", size = 100, weight, spacing = 0) {
    const w = weight || (kind === "cond" ? 800 : 700);
    ctx.font = `${w} ${size}px ${FONT[kind]}`;
    const t = String(text ?? "");
    return ctx.measureText(t).width + spacing * Math.max(0, t.length - 1);
  }
  // Tamaño máximo para que el texto quepa en maxW
  function fit(text, maxSize, maxW, kind = "cond", weight, spacing = 0) {
    const w = measure(text, kind, maxSize, weight, spacing);
    return w > maxW ? Math.floor(maxSize * maxW / w) : maxSize;
  }
  // Partir texto en líneas que quepan en maxW
  function wrap(text, size, maxW, kind = "sans", weight = 600) {
    const lines = [];
    for (const para of String(text ?? "").split("\n")) {
      let cur = "";
      for (const word of para.split(/\s+/).filter(Boolean)) {
        const test = cur ? cur + " " + word : word;
        if (cur && measure(test, kind, size, weight) > maxW) { lines.push(cur); cur = word; } else cur = test;
      }
      lines.push(cur);
    }
    return lines;
  }

  // Como wrap(), pero si salen 2 líneas las equilibra (evita una palabra sola en la segunda línea)
  function wrapBalanced(text, size, maxW, kind = "cond", weight = 800) {
    const lines = wrap(text, size, maxW, kind, weight);
    if (lines.length !== 2) return lines;
    const words = String(text).trim().split(/\s+/);
    let best = null, bestW = Infinity;
    for (let i = 1; i < words.length; i++) {
      const l1 = words.slice(0, i).join(" "), l2 = words.slice(i).join(" ");
      const w = Math.max(measure(l1, kind, size, weight), measure(l2, kind, size, weight));
      if (w <= maxW && w < bestW) { bestW = w; best = [l1, l2]; }
    }
    return best || lines;
  }

  // ---- definiciones compartidas ----
  function defs(fontCSS = "") {
    return `<defs><style>${fontCSS}
      .cond{font-family:${FONT.cond};font-weight:800}
      .sans{font-family:${FONT.sans}}
    </style>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.6" fill="${INK}" opacity="0.10"/></pattern>
    <pattern id="dotsLight" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.6" fill="${CREAM}" opacity="0.07"/></pattern>
    <symbol id="bowl" viewBox="0 0 120 124">${T.bowl}</symbol>
    <symbol id="sparkle" viewBox="-50 -50 100 100"><path d="M0,-50 C6,-10 10,-6 50,0 C10,6 6,10 0,50 C-6,10 -10,6 -50,0 C-10,-6 -6,-10 0,-50 Z"/></symbol>
    <symbol id="meeple" viewBox="0 0 100 100"><path d="M50,4 C62,4 70,13 70,24 C70,31 67,36 63,40 L94,52 C99,54 99,62 94,64 L72,70 L84,96 H58 L50,78 L42,96 H16 L28,70 L6,64 C1,62 1,54 6,52 L37,40 C33,36 30,31 30,24 C30,13 38,4 50,4 Z"/></symbol>
    </defs>`;
  }

  const background = (w, h, color, light) =>
    `<rect width="${w}" height="${h}" fill="${color}"/><rect width="${w}" height="${h}" fill="url(#${light ? "dotsLight" : "dots"})"/>`;
  const corner = (w, c1, c2, s = 180) =>
    `<path d="M${w - s},0 H${w} V${s} Z" fill="${c1}"/><path d="M${w - s / 2},0 H${w} V${s / 2} Z" fill="${c2}"/>`;
  const sparkle = (x, y, s, fill) => `<use href="#sparkle" x="${x - s / 2}" y="${y - s / 2}" width="${s}" height="${s}" fill="${fill}"/>`;
  const meeple = (x, y, s, fill = INK) => `<use href="#meeple" x="${x}" y="${y}" width="${s}" height="${s}" fill="${fill}"/>`;

  function header(x, y, s, ink, sub = "ESPACIO CULTURAL · ENGATIVÁ") {
    return `<circle cx="${x}" cy="${y}" r="${46 * s}" fill="${CREAM}" stroke="${INK}" stroke-width="${4 * s}"/>
    <use href="#bowl" x="${x - 29 * s}" y="${y - 31 * s}" width="${58 * s}" height="${60 * s}"/>
    <text x="${x + 66 * s}" y="${y + 2 * s}" class="cond" font-size="${44 * s}" fill="${ink}" letter-spacing="1">TAZÓN PARA DOS</text>
    <text x="${x + 68 * s}" y="${y + 33 * s}" class="sans" font-weight="600" font-size="${19 * s}" fill="${ink}" letter-spacing="${3.2 * s}">${esc(sub)}</text>`;
  }

  function pill(x, y, w, h, fill, ink, label, size, opts = {}) {
    let out = "";
    if (opts.shadow) out += `<rect x="${x + 8}" y="${y + 8}" width="${w}" height="${h}" rx="${h / 2}" fill="${INK}"/>`;
    const st = opts.stroke ? ` stroke="${opts.stroke}" stroke-width="4"` : "";
    out += `<rect x="${x}" y="${y}" width="${n(w)}" height="${h}" rx="${h / 2}" fill="${fill}"${st}/>`;
    out += `<text x="${n(x + w / 2)}" y="${n(y + h / 2 + size * 0.36)}" text-anchor="middle" class="sans" font-weight="700" font-size="${size}" fill="${ink}" letter-spacing="2">${esc(label)}</text>`;
    return out;
  }
  // Píldora con ancho calculado según el texto. anchor: "start" | "middle" | "end"
  function pillAuto(x, y, h, fill, ink, label, size, opts = {}) {
    if (!label) return "";
    const w = measure(label, "sans", size, 700, 2) + h * 1.2;
    const x0 = opts.anchor === "middle" ? x - w / 2 : opts.anchor === "end" ? x - w : x;
    return pill(x0, y, w, h, fill, ink, label, size, opts);
  }

  function headline(x, y, text, size, fg, shadow, off = 10, anchor = "start") {
    const a = anchor !== "start" ? ` text-anchor="${anchor}"` : "";
    const t = esc(text);
    const sh = shadow ? `<text x="${x + off}" y="${y + off}" class="cond" font-size="${size}" fill="${shadow}"${a}>${t}</text>` : "";
    return sh + `<text x="${x}" y="${y}" class="cond" font-size="${size}" fill="${fg}"${a}>${t}</text>`;
  }

  function paragraph(x, y, text, size, maxW, fill, opts = {}) {
    const lh = opts.lineHeight || size * 1.3;
    const lines = wrap(text, size, maxW, "sans", opts.weight || 600).slice(0, opts.maxLines || 99);
    const a = opts.anchor ? ` text-anchor="${opts.anchor}"` : "";
    const it = opts.italic ? ' font-style="italic"' : "";
    return {
      svg: `<text class="sans" font-weight="${opts.weight || 600}" font-size="${size}" fill="${fill}"${a}${it}>` +
        lines.map((l, i) => `<tspan x="${x}" y="${n(y + i * lh)}">${esc(l)}</tspan>`).join("") + `</text>`,
      height: lines.length * lh,
    };
  }

  function icon(name, cx, cy, size, color = INK, stroke = 4) {
    const ic = T.icons[name];
    if (!ic) return "";
    const k = size / 64;
    return `<g transform="translate(${n(cx - size / 2)},${n(cy - size / 2)}) scale(${k.toFixed(4)})" fill="none" stroke="${color}" stroke-width="${stroke}" stroke-linecap="round" stroke-linejoin="round" style="color:${color}">${ic.body}</g>`;
  }

  function d20(tx, ty, R, rot = -8, num = true, fill = SUN, inner = SUN_L) {
    const k = R / 200;
    const p = (a) => `${n(a[0] * k)},${n(a[1] * k)}`;
    const hexa = [[0, -200], [173, -100], [173, 100], [0, 200], [-173, 100], [-173, -100]];
    const tri = [[0, -105], [92, 58], [-92, 58]];
    const lines = [[[0, -200], [0, -105]], [[0, -105], [173, -100]], [[0, -105], [-173, -100]], [[92, 58], [173, -100]], [[92, 58], [173, 100]], [[92, 58], [0, 200]], [[-92, 58], [-173, -100]], [[-92, 58], [-173, 100]], [[-92, 58], [0, 200]]];
    const sw = Math.max(3, 7 * k * 1.4);
    const t = num ? `<text x="0" y="${n(36 * k)}" text-anchor="middle" class="cond" font-size="${n(92 * k)}" fill="${INK}" stroke="none">20</text>` : "";
    return `<g transform="translate(${tx},${ty}) rotate(${rot})" stroke="${INK}" stroke-width="${n(sw)}" stroke-linejoin="round">
      <path d="M${hexa.map(p).join(" L")} Z" fill="${fill}"/><path d="M${tri.map(p).join(" L")} Z" fill="${inner}"/>
      <path d="${lines.map(([a, b]) => `M${p(a)} L${p(b)}`).join(" ")}" fill="none"/>${t}</g>`;
  }

  function d6(tx, ty, s, rot = 14, fill = CREAM) {
    const h = 42 * s, q = 20 * s, r = 7 * s;
    const pips = [[-q, -q], [q, -q], [0, 0], [-q, q], [q, q]].map(([x, y]) => `<circle cx="${n(x)}" cy="${n(y)}" r="${n(r)}"/>`).join("");
    return `<g transform="translate(${tx},${ty}) rotate(${rot})"><rect x="${-h}" y="${-h}" width="${2 * h}" height="${2 * h}" rx="${n(15 * s)}" fill="${fill}" stroke="${INK}" stroke-width="${n(6 * s)}"/><g fill="${INK}">${pips}</g></g>`;
  }

  const card = (tx, ty, s, rot = -14) => `<g transform="translate(${tx},${ty}) rotate(${rot}) scale(${s})">
    <rect x="-62" y="-88" width="124" height="176" rx="14" fill="${CREAM}" stroke="${INK}" stroke-width="6"/>
    <path d="M0,-38 L27,0 L0,38 L-27,0 Z" fill="${CORAL}" stroke="${INK}" stroke-width="4"/>
    <circle cx="-40" cy="-64" r="6" fill="${CORAL}"/><circle cx="40" cy="64" r="6" fill="${CORAL}"/></g>`;

  function mic(tx, ty, s, stand = INK, waves = true) {
    const w = waves ? `<path d="M100,-110 A90,90 0 0 1 100,10" fill="none" stroke="${SUN}" stroke-width="12"/>
      <path d="M136,-140 A130,130 0 0 1 136,40" fill="none" stroke="${CORAL}" stroke-width="12"/>
      <path d="M-100,-110 A90,90 0 0 0 -100,10" fill="none" stroke="${SUN}" stroke-width="12"/>
      <path d="M-136,-140 A130,130 0 0 0 -136,40" fill="none" stroke="${TEAL}" stroke-width="12"/>` : "";
    return `<g transform="translate(${tx},${ty}) scale(${s})" stroke="${INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
      <path d="M-80,10 A80,80 0 0 0 80,10" fill="none" stroke="${stand}"/><line x1="0" y1="90" x2="0" y2="200" stroke="${stand}"/>
      <rect x="-60" y="196" width="120" height="22" rx="11" fill="${stand}" stroke="${stand}"/>
      <rect x="-52" y="-150" width="104" height="200" rx="52" fill="${CREAM}"/><path d="M-52,-60 H52 M-52,-20 H52" fill="none"/>
      <g fill="${INK}" stroke="none"><circle cx="-20" cy="-110" r="6"/><circle cx="0" cy="-118" r="6"/><circle cx="20" cy="-110" r="6"/><circle cx="-10" cy="-90" r="6"/><circle cx="10" cy="-90" r="6"/></g>${w}</g>`;
  }

  function waveform(x0, x1, cy, maxh, color) {
    let out = "", x = x0, i = 0;
    while (x + 10 <= x1) {
      const h = maxh * (0.25 + 0.75 * Math.abs(Math.sin(i * 0.55) * Math.cos(i * 0.21)));
      out += `<rect x="${x}" y="${n(cy - h / 2)}" width="10" height="${n(h)}" rx="5" fill="${color}"/>`;
      x += 18; i++;
    }
    return out;
  }

  function bubble(x, y, w, h, text, size) {
    const s = fit(text, size, w - 120, "sans", 600);
    return `<rect x="${x + 8}" y="${y + 8}" width="${w}" height="${h}" rx="28" fill="${INK}"/>
      <path d="M${x + 60},${y + h} l-10,46 l58,-46 Z" fill="${INK}"/>
      <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="28" fill="${CREAM}" stroke="${INK}" stroke-width="5"/>
      <path d="M${x + 56},${y + h - 3} l-12,40 l52,-40" fill="${CREAM}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
      <text x="${x + 40}" y="${n(y + h / 2 + s * 0.35)}" class="sans" font-weight="600" font-style="italic" font-size="${s}" fill="${INK}">${esc(text)}</text>
      <rect x="${x + w - 56}" y="${n(y + h / 2 - size * 0.55)}" width="6" height="${n(size * 1.1)}" rx="3" fill="${CORAL}"/>`;
  }

  // Divide una etiqueta en 2 líneas equilibradas
  function twoLines(label) {
    const w = String(label).trim().split(/\s+/);
    if (w.length < 2) return [w[0] || "", ""];
    let best = 1, diff = 1e9;
    for (let i = 1; i < w.length; i++) {
      const d = Math.abs(w.slice(0, i).join(" ").length - w.slice(i).join(" ").length);
      if (d < diff) { diff = d; best = i; }
    }
    return [w.slice(0, best).join(" "), w.slice(best).join(" ")];
  }

  function steps(cxs, cy, r, labels, ink, size) {
    const cols = [TEAL, CREAM, SUN];
    return labels.map((lab, i) => {
      const [l1, l2] = twoLines(String(lab).toUpperCase());
      const cx = cxs[i];
      return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${cols[i % 3]}" stroke="${INK}" stroke-width="4"/>
        <text x="${cx}" y="${n(cy + r * 0.42)}" text-anchor="middle" class="cond" font-size="${n(r * 1.2)}" fill="${INK}">${i + 1}</text>
        <text x="${cx}" y="${n(cy + r + size * 1.6)}" text-anchor="middle" class="sans" font-weight="700" font-size="${size}" fill="${ink}" letter-spacing="2">${esc(l1)}</text>
        <text x="${cx}" y="${n(cy + r + size * 2.9)}" text-anchor="middle" class="sans" font-weight="700" font-size="${size}" fill="${ink}" letter-spacing="2">${esc(l2)}</text>`;
    }).join("");
  }

  function infoCard(x, y, w, rows, size) {
    const rh = size * 2.6, h = rh * rows.length + size * 0.8;
    let out = `<rect x="${x + 10}" y="${y + 10}" width="${w}" height="${h}" rx="28" fill="${INK}"/>
      <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="28" fill="${CREAM}" stroke="${INK}" stroke-width="5"/>`;
    rows.forEach(([ic, label], i) => {
      const cy = y + size * 0.4 + rh * i + rh / 2;
      if (i) out += `<line x1="${x + 30}" y1="${n(cy - rh / 2)}" x2="${x + w - 30}" y2="${n(cy - rh / 2)}" stroke="${INK}" stroke-width="2" opacity="0.2"/>`;
      const fs = fit(label, size, w - 120 - size * 1.8, "sans", 700);
      out += icon(ic, x + 30 + size * 0.75, cy, size * 1.5);
      out += `<text x="${n(x + 60 + size * 1.8)}" y="${n(cy + fs * 0.36)}" class="sans" font-weight="700" font-size="${fs}" fill="${INK}">${esc(label)}</text>`;
    });
    return { svg: out, height: h };
  }

  function chips(x, y, items, h, size) {
    let out = "", cx = x;
    for (const [label, fill] of items) {
      if (!label) continue;
      const w = measure(label, "sans", size, 700, 2) + 56;
      out += pill(cx, y, w, h, fill, INK, label, size, { stroke: INK });
      cx += w + 16;
    }
    return out;
  }

  // Grupo ilustrado centrado en (cx, cy). kind: mixto | rol | mesa | podcast
  function illustration(kind, cx, cy, s = 1) {
    const g = (body) => `<g transform="translate(${cx},${cy}) scale(${s})">${body}</g>`;
    const shadow = (rx) => `<ellipse cx="0" cy="165" rx="${rx}" ry="20" fill="${INK}" opacity="0.22"/>`;
    if (kind === "rol") return g(shadow(240) + card(-250, 20, 0.9) + d20(10, 0, 165) + d6(230, 110, 0.85) + sparkle(-200, -130, 40, INK) + sparkle(220, -120, 30, CREAM));
    if (kind === "mesa") return g(shadow(260) + card(-230, 10, 1.0, -16) + card(-120, 30, 1.0, 6) + meeple(20, -60, 190) + d6(260, 100, 1.0) + sparkle(250, -110, 36, CREAM));
    if (kind === "podcast") return g(shadow(220) + mic(40, -20, 0.8) + d20(-240, 90, 70, 12) + sparkle(-230, -120, 40, CREAM));
    return g(shadow(260) + card(-300, 15, 0.9) + d20(0, 0, 160) + mic(300, -5, 0.72) + meeple(-180, 85, 80) + d6(160, 125, 0.8) + sparkle(-440 + 0, -105, 40, INK) + sparkle(160, -145, 30, CREAM));
  }

  // Recetas de color por línea de contenido
  const RECIPES = {
    general: { label: "General / Rol (turquesa)", bg: TEAL, block: CORAL, close: INK, ink: INK, hl: CREAM, hlShadow: INK, accent: SUN, corner: [SUN, CORAL], light: false },
    mesa: { label: "Juegos de mesa (coral)", bg: CORAL, block: TEAL, close: INK, ink: INK, hl: CREAM, hlShadow: INK, accent: SUN, corner: [SUN, TEAL], light: false },
    convocatoria: { label: "Convocatoria (sol)", bg: SUN, block: CORAL, close: INK, ink: INK, hl: CREAM, hlShadow: INK, accent: CORAL, corner: [TEAL, CORAL], light: false },
    podcast: { label: "Podcast (tinta)", bg: INK, block: TEAL, close: INK, ink: CREAM, hl: SUN, hlShadow: TEAL, accent: CORAL, corner: [SUN, CORAL], light: true },
  };

  // ---- fotos ----
  const FOCUS = { centro: "xMidYMid", arriba: "xMidYMin", abajo: "xMidYMax", izquierda: "xMinYMid", derecha: "xMaxYMid" };
  const FOCUS_OPTS = Object.keys(FOCUS).map((k) => [k, k[0].toUpperCase() + k.slice(1)]);
  let clipN = 0;
  // Foto recortada en un rectángulo (rx = radio). Sin foto muestra un marcador "TU FOTO AQUÍ".
  // opts: { rx, focus, stroke, shadow, path } — path: recorte libre (d de un <path>) en vez de rectángulo.
  function photo(x, y, w, h, href, opts = {}) {
    const id = "clip" + (++clipN);
    const rx = opts.rx ?? 28;
    const shape = opts.path ? `<path d="${opts.path}"/>` : `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}"/>`;
    const outline = opts.path ? `<path d="${opts.path}"` : `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}"`;
    let out = "";
    if (opts.shadow) out += opts.path ? "" : `<rect x="${x + 12}" y="${y + 12}" width="${w}" height="${h}" rx="${rx}" fill="${INK}"/>`;
    out += `<clipPath id="${id}">${shape}</clipPath>`;
    if (href) {
      out += `<image href="${esc(href)}" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="${FOCUS[opts.focus] || "xMidYMid"} slice" clip-path="url(#${id})"/>`;
    } else {
      out += `<g clip-path="url(#${id})"><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${C.cream}"/><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="url(#dots)"/></g>`;
      const s = Math.min(w, h) * 0.18;
      out += icon("camara", x + w / 2, y + h / 2 - s * 0.35, s, C.muted, 3);
      out += `<text data-guia="1" x="${x + w / 2}" y="${n(y + h / 2 + s * 0.75)}" text-anchor="middle" class="sans" font-weight="700" font-size="${n(Math.max(18, s * 0.28))}" fill="${C.muted}" letter-spacing="3">TU FOTO AQUÍ</text>`;
    }
    if (opts.stroke !== false) out += `${outline} fill="none" stroke="${INK}" stroke-width="${opts.strokeWidth || 8}" stroke-linejoin="round"/>`;
    return out;
  }

  // Insignia de reproducción (video)
  function playBadge(cx, cy, r, fill = SUN) {
    return `<circle cx="${cx + r * 0.08}" cy="${cy + r * 0.08}" r="${r}" fill="${INK}"/><circle cx="${cx}" cy="${cy}" r="${r}" fill="${fill}" stroke="${INK}" stroke-width="${n(r * 0.08)}"/>
      <path d="M${n(cx - r * 0.28)},${n(cy - r * 0.42)} L${n(cx + r * 0.46)},${cy} L${n(cx - r * 0.28)},${n(cy + r * 0.42)} Z" fill="${INK}" stroke="${INK}" stroke-width="${n(r * 0.06)}" stroke-linejoin="round"/>`;
  }

  // Caja de texto tipo "sticker" (para subtítulos y textos en pantalla)
  function textBox(cx, y, text, size, maxW, fill, ink, opts = {}) {
    const lines = wrap(text, size, maxW - size * 1.2, opts.kind || "sans", opts.weight || 700).slice(0, opts.maxLines || 3);
    const lh = size * 1.22, padX = size * 0.6, padY = size * 0.42;
    const widest = Math.max(...lines.map((l) => measure(l, opts.kind || "sans", size, opts.weight || 700)), 10);
    const w = widest + padX * 2, h = lines.length * lh + padY * 2;
    const x = cx - w / 2;
    const cls = opts.kind === "cond" ? "cond" : "sans";
    return {
      svg: `<rect x="${n(x + 8)}" y="${n(y + 8)}" width="${n(w)}" height="${n(h)}" rx="${n(size * 0.35)}" fill="${INK}" opacity="${fill === INK ? 0 : 1}"/>
        <rect x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" rx="${n(size * 0.35)}" fill="${fill}" stroke="${INK}" stroke-width="${n(size * 0.08)}"/>
        <text class="${cls}" font-weight="${opts.weight || 700}" font-size="${size}" fill="${ink}" text-anchor="middle">` +
        lines.map((l, i) => `<tspan x="${cx}" y="${n(y + padY + size * 0.95 + i * lh)}">${esc(l)}</tspan>`).join("") + `</text>`,
      height: h, width: w,
    };
  }

  window.TPDDraw = { C, INK, CORAL, SUN, TEAL, CREAM, SUN_L, TEAL_L, esc, measure, fit, wrap, defs, background, corner, sparkle, meeple, header, pill, pillAuto, headline, paragraph, icon, d20, d6, card, mic, waveform, bubble, steps, infoCard, chips, illustration, twoLines, wrapBalanced, RECIPES, photo, playBadge, textBox, FOCUS_OPTS };
})();
