// Plantillas editables de Tazón para Dos.
// Cada plantilla: { id, name, group, w, h, out?: {w,h}, fields: [...], render(v) => cuerpo SVG }
// Tipos de campo: text | textarea | select (options: [[valor, etiqueta]]) | checkbox | number
// Para crear una plantilla nueva copia una existente, cambia id/name y ajusta fields + render.
(function () {
  const D = window.TPDDraw, T = window.TPD;
  const { INK, CORAL, SUN, TEAL, CREAM, TEAL_L, RECIPES } = D;
  const L = T.location;

  const RECIPE_OPTS = Object.entries(RECIPES).map(([k, r]) => [k, r.label]);
  const ILLUS_OPTS = [["mixto", "Mixto (dado, carta, micrófono)"], ["rol", "Rol (d20)"], ["mesa", "Juegos de mesa (cartas, meeple)"], ["podcast", "Podcast (micrófono)"]];
  const ICON_OPTS = Object.entries(T.icons).map(([k, v]) => [k, `${v.label} (${k})`]);
  const COLOR_OPTS = [["teal", "Turquesa"], ["coral", "Coral"], ["sun", "Sol"], ["ink", "Tinta"]];
  const COLOR = { teal: TEAL, coral: CORAL, sun: SUN, ink: INK, cream: CREAM };
  const MENU = T.podcastMenu.map((m) => [m.name, m.name]);
  const SCHEDULE = L.schedule ? `${L.schedule.open === "11:00" ? "11:00 a.m." : L.schedule.open} – ${L.schedule.close === "21:00" ? "9:00 p.m." : L.schedule.close}` : "";
  const PLACE = `${L.address} · ${L.locality}`;
  const STEP = T.process.map((p) => p.short);

  const f = {
    receta: { key: "receta", label: "Combinación de color", type: "select", options: RECIPE_OPTS, default: "general" },
    etiqueta: (d) => ({ key: "etiqueta", label: "Etiqueta (píldora, opcional)", type: "text", default: d }),
    usuario: { key: "usuario", label: "Usuario / redes", type: "text", default: "@tazonparados" },
    ilustracion: { key: "ilustracion", label: "Ilustración", type: "select", options: ILLUS_OPTS, default: "mixto" },
  };
  const chipColors = (block) => (block === TEAL ? [CORAL, SUN, CREAM] : [TEAL, SUN, CREAM]);
  const splitList = (s) => String(s || "").split(",").map((x) => x.trim()).filter(Boolean);

  const templates = [];
  const add = (t) => templates.push(t);

  // ------------------------------------------------------------ POST GENERAL 1:1
  add({
    id: "post_general", name: "Post general", group: "Publicaciones", w: 1080, h: 1080,
    fields: [f.receta, f.etiqueta(""), { key: "linea1", label: "Titular línea 1", type: "text", default: "JUGAR TAMBIÉN" },
      { key: "linea2", label: "Titular línea 2 (destacada)", type: "text", default: "ES ESCUCHAR." }, f.ilustracion,
      { key: "pie", label: "Texto del pie", type: "text", default: "JUEGOS DE MESA · ROL · PODCAST" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const tag = v.etiqueta ? D.pillAuto(64, 186, 50, r.ink === CREAM ? TEAL : INK, r.ink === CREAM ? INK : CREAM, v.etiqueta, 20) : "";
      return `${D.background(1080, 1080, r.bg, r.light)}${D.corner(1080, ...r.corner)}${D.header(110, 104, 1, r.ink)}${tag}
        ${D.headline(64, 300, v.linea1, D.fit(v.linea1, 122, 760), r.ink)}
        ${D.headline(64, 430, v.linea2, D.fit(v.linea2, 146, 860), r.hl, r.hlShadow, 7)}
        ${D.sparkle(880, 230, 70, r.accent)}${D.sparkle(980, 340, 34, CREAM)}
        <path d="M0,560 L1080,480 L1080,518 L0,598 Z" fill="${CREAM}"/>
        <path d="M0,598 L1080,518 L1080,900 L0,950 Z" fill="${r.block}"/><path d="M0,598 L1080,518 L1080,900 L0,950 Z" fill="url(#dots)"/>
        ${D.illustration(v.ilustracion, 540, 705, 0.95)}
        <path d="M0,950 L1080,900 L1080,1080 L0,1080 Z" fill="${INK}"/><path d="M0,950 L1080,900 L1080,910 L0,960 Z" fill="${SUN}"/>
        <text x="540" y="1010" text-anchor="middle" class="sans" font-weight="700" font-size="${D.fit(v.pie, 26, 940, "sans", 700, 3)}" fill="${CREAM}" letter-spacing="3">${D.esc(v.pie)}</text>
        <text x="540" y="1052" text-anchor="middle" class="sans" font-weight="700" font-size="26" fill="${SUN}">${D.esc(v.usuario)}</text>`;
    },
  });

  // ------------------------------------------------------------ HISTORIA GENERAL 9:16
  add({
    id: "historia_general", name: "Historia general", group: "Publicaciones", w: 1080, h: 1920,
    fields: [f.receta, f.etiqueta(""), { key: "linea1", label: "Titular línea 1", type: "text", default: "JUGAR TAMBIÉN" },
      { key: "linea2", label: "Titular línea 2 (destacada)", type: "text", default: "ES ESCUCHAR." },
      { key: "texto", label: "Texto", type: "textarea", default: "Un lugar para jugar, imaginar y convertir nuestras voces en historias que se escuchan." },
      f.ilustracion, { key: "cierre1", label: "Cierre línea 1", type: "text", default: "VEN A JUGAR." },
      { key: "cierre2", label: "Cierre línea 2", type: "text", default: "QUÉDATE A COMPARTIR." },
      { key: "pie", label: "Texto del pie", type: "text", default: "JUEGOS DE MESA · ROL · PODCAST" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const tag = v.etiqueta ? D.pillAuto(76, 400, 60, r.ink === CREAM ? TEAL : INK, r.ink === CREAM ? INK : CREAM, v.etiqueta, 24) : "";
      const p = D.paragraph(76, 800, v.texto, 34, 900, r.ink, { maxLines: 3 });
      return `${D.background(1080, 1920, r.bg, r.light)}${D.corner(1080, ...r.corner, 260)}${D.header(132, 300, 1.22, r.ink)}${tag}
        ${D.headline(72, 570, v.linea1, D.fit(v.linea1, 150, 860), r.ink)}
        ${D.headline(72, 730, v.linea2, D.fit(v.linea2, 178, 900), r.hl, r.hlShadow, 9)}
        ${D.sparkle(985, 390, 74, r.accent)}${p.svg}
        <path d="M0,920 L1080,850 L1080,892 L0,962 Z" fill="${CREAM}"/>
        <path d="M0,962 L1080,892 L1080,1330 L0,1390 Z" fill="${r.block}"/><path d="M0,962 L1080,892 L1080,1330 L0,1390 Z" fill="url(#dots)"/>
        ${D.illustration(v.ilustracion, 540, 1130, 1.12)}
        <path d="M0,1390 L1080,1330 L1080,1920 L0,1920 Z" fill="${INK}"/><path d="M0,1390 L1080,1330 L1080,1342 L0,1402 Z" fill="${SUN}"/>
        <text x="540" y="1500" text-anchor="middle" class="cond" font-size="${D.fit(v.cierre1, 112, 940)}" fill="${CREAM}">${D.esc(v.cierre1)}</text>
        <text x="540" y="1580" text-anchor="middle" class="cond" font-size="${D.fit(v.cierre2, 72, 940)}" fill="${SUN}">${D.esc(v.cierre2)}</text>
        <text x="540" y="1640" text-anchor="middle" class="sans" font-weight="700" font-size="${D.fit(v.pie, 26, 940, "sans", 700, 4)}" fill="${CREAM}" letter-spacing="4">${D.esc(v.pie)}</text>
        ${D.pillAuto(540, 1672, 64, SUN, INK, v.usuario, 28, { anchor: "middle" })}`;
    },
  });

  // ------------------------------------------------------------ EVENTO SEMANAL 4:5 y 9:16
  const eventoFields = [f.receta, f.etiqueta("AGENDA SEMANAL"),
    { key: "linea1", label: "Titular línea 1", type: "text", default: "ESTE SÁBADO" },
    { key: "linea2", label: "Titular línea 2 (destacada)", type: "text", default: "JUGAMOS." },
    { key: "dia", label: "Día / fecha", type: "text", default: L.schedule ? L.schedule.days : "Sábado" },
    { key: "horario", label: "Horario", type: "text", default: SCHEDULE },
    { key: "lugar", label: "Lugar", type: "text", default: PLACE },
    { key: "actividades", label: "Actividades (separadas por coma)", type: "text", default: "ROL, JUEGOS DE MESA, PODCAST" },
    { key: "frase", label: "Frase final", type: "text", default: "Ven a jugar. Quédate a compartir." }, f.usuario,
    { key: "dado", label: "Mostrar dado", type: "checkbox", default: true }];

  add({
    id: "evento_vertical", name: "Evento semanal 4:5", group: "Eventos", w: 1080, h: 1350, fields: eventoFields,
    render(v) {
      const r = RECIPES[v.receta];
      const card = D.infoCard(64, 730, 952, [["calendario", v.dia], ["reloj", v.horario], ["ubicacion", v.lugar]], 40);
      const cc = chipColors(r.block);
      const tag = v.etiqueta ? D.pillAuto(64, 186, 50, r.ink === CREAM ? TEAL : INK, r.ink === CREAM ? INK : CREAM, v.etiqueta, 20) : "";
      return `${D.background(1080, 1350, r.bg, r.light)}${D.corner(1080, ...r.corner)}${D.header(110, 104, 1, r.ink)}${tag}
        ${D.headline(60, 390, v.linea1, D.fit(v.linea1, 146, v.dado ? 700 : 940), r.ink)}
        ${D.headline(60, 570, v.linea2, D.fit(v.linea2, 196, v.dado ? 880 : 940), r.hl, r.hlShadow, 10)}
        ${v.dado ? D.d20(915, 320, 92, 12) : ""}${D.sparkle(1000, 520, 44, CREAM)}${D.sparkle(820, 210, 40, r.ink)}
        <path d="M0,640 L1080,580 L1080,618 L0,678 Z" fill="${CREAM}"/>
        <path d="M0,678 L1080,618 L1080,1350 L0,1350 Z" fill="${r.block}"/><path d="M0,678 L1080,618 L1080,1350 L0,1350 Z" fill="url(#dots)"/>
        ${card.svg}${D.chips(64, 730 + card.height + 50, splitList(v.actividades).map((a, i) => [a.toUpperCase(), cc[i % 3]]), 60, 22)}
        <text x="64" y="1300" class="sans" font-weight="700" font-size="${D.fit(v.frase, 28, 600, "sans", 700)}" fill="${INK}">${D.esc(v.frase)}</text>
        <text x="1016" y="1300" text-anchor="end" class="sans" font-weight="700" font-size="28" fill="${INK}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "evento_historia", name: "Evento semanal historia", group: "Eventos", w: 1080, h: 1920, fields: eventoFields,
    render(v) {
      const r = RECIPES[v.receta];
      const card = D.infoCard(76, 1040, 928, [["calendario", v.dia], ["reloj", v.horario], ["ubicacion", v.lugar]], 42);
      const cc = chipColors(r.block);
      const tag = v.etiqueta ? D.pillAuto(76, 400, 60, r.ink === CREAM ? TEAL : INK, r.ink === CREAM ? INK : CREAM, v.etiqueta, 24) : "";
      return `${D.background(1080, 1920, r.bg, r.light)}${D.corner(1080, ...r.corner, 260)}${D.header(132, 300, 1.22, r.ink)}${tag}
        ${D.headline(70, 660, v.linea1, D.fit(v.linea1, 172, 930), r.ink)}
        ${D.headline(70, 880, v.linea2, D.fit(v.linea2, 236, 900), r.hl, r.hlShadow, 12)}
        ${D.sparkle(990, 560, 70, r.accent)}
        <path d="M0,960 L1080,900 L1080,942 L0,1002 Z" fill="${CREAM}"/>
        <path d="M0,1002 L1080,942 L1080,1920 L0,1920 Z" fill="${r.block}"/><path d="M0,1002 L1080,942 L1080,1920 L0,1920 Z" fill="url(#dots)"/>
        ${v.dado ? D.d20(940, 960, 80, 14) : ""}
        ${card.svg}${D.chips(76, 1040 + card.height + 50, splitList(v.actividades).map((a, i) => [a.toUpperCase(), cc[i % 3]]), 64, 24)}
        <text x="540" y="1640" text-anchor="middle" class="sans" font-weight="700" font-size="${D.fit(v.frase, 32, 920, "sans", 700)}" fill="${INK}">${D.esc(v.frase)}</text>
        ${D.pillAuto(540, 1672, 64, INK, CREAM, v.usuario, 28, { anchor: "middle" })}`;
    },
  });

  // ------------------------------------------------------------ CONVOCATORIA
  const convFields = [f.etiqueta("CONVOCATORIA ABIERTA"),
    { key: "linea1", label: "Titular línea 1", type: "text", default: "¿QUÉ MUNDO" },
    { key: "linea2", label: "Titular línea 2", type: "text", default: "QUIERES TRAER" },
    { key: "linea3", label: "Titular línea 3 (destacada)", type: "text", default: "A LA MESA?" },
    { key: "burbuja", label: "Texto del globo", type: "text", default: "Mi historia trata sobre..." },
    { key: "paso1", label: "Paso 1", type: "text", default: STEP[0] }, { key: "paso2", label: "Paso 2", type: "text", default: STEP[1] },
    { key: "paso3", label: "Paso 3", type: "text", default: STEP[2] },
    { key: "cta", label: "Botón", type: "text", default: "POSTULA TU IDEA →" },
    { key: "web", label: "Web", type: "text", default: "tazon-para-dos.online" }, f.usuario];

  add({
    id: "convocatoria_cuadrado", name: "Convocatoria 1:1", group: "Convocatorias", w: 1080, h: 1080, fields: convFields,
    render(v) {
      return `${D.background(1080, 1080, SUN)}${D.corner(1080, TEAL, CORAL)}${D.header(110, 104, 1, INK)}
        ${D.pillAuto(64, 186, 50, INK, CREAM, v.etiqueta, 20)}
        ${D.headline(60, 360, v.linea1, D.fit(v.linea1, 124, 760), INK)}${D.headline(60, 478, v.linea2, D.fit(v.linea2, 124, 760), INK)}
        ${D.headline(60, 610, v.linea3, D.fit(v.linea3, 150, 760), CREAM, INK, 10)}
        ${D.sparkle(880, 300, 70, CORAL)}${D.sparkle(960, 400, 34, CREAM)}${D.d20(900, 560, 82, 14, true, TEAL, TEAL_L)}
        <path d="M0,780 L1080,730 L1080,960 L0,960 Z" fill="${CORAL}"/><path d="M0,780 L1080,730 L1080,960 L0,960 Z" fill="url(#dots)"/>
        ${D.bubble(470, 650, 420, 92, v.burbuja, 30)}
        ${D.steps([180, 540, 900], 830, 32, [v.paso1, v.paso2, v.paso3], INK, 19)}
        <rect x="0" y="960" width="1080" height="120" fill="${INK}"/>
        ${D.pill(64, 984, Math.max(320, D.measure(v.cta, "sans", 24, 700, 2) + 90), 72, SUN, INK, v.cta, 24)}
        <text x="1016" y="1018" text-anchor="end" class="sans" font-weight="700" font-size="24" fill="${CREAM}">${D.esc(v.web)}</text>
        <text x="1016" y="1048" text-anchor="end" class="sans" font-weight="600" font-size="20" fill="${SUN}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "convocatoria_historia", name: "Convocatoria historia", group: "Convocatorias", w: 1080, h: 1920,
    fields: [...convFields.slice(0, 4), { key: "texto", label: "Texto", type: "textarea", default: "Estamos buscando voces, recuerdos y mundos para convertirlos en una nueva serie de podcast narrativo." }, ...convFields.slice(4)],
    render(v) {
      const p = D.paragraph(76, 1060, v.texto, 34, 900, INK, { maxLines: 3, lineHeight: 42 });
      return `${D.background(1080, 1920, SUN)}${D.corner(1080, TEAL, CORAL, 260)}${D.header(132, 300, 1.22, INK)}
        ${D.pillAuto(76, 400, 60, INK, CREAM, v.etiqueta, 24)}
        ${D.headline(70, 640, v.linea1, D.fit(v.linea1, 160, 900), INK)}${D.headline(70, 790, v.linea2, D.fit(v.linea2, 160, 920), INK)}
        ${D.headline(70, 970, v.linea3, D.fit(v.linea3, 196, 900), CREAM, INK, 12)}
        ${D.sparkle(990, 500, 70, CORAL)}${p.svg}
        <path d="M0,1330 L1080,1280 L1080,1920 L0,1920 Z" fill="${CORAL}"/><path d="M0,1330 L1080,1280 L1080,1920 L0,1920 Z" fill="url(#dots)"/>
        ${D.bubble(76, 1190, 640, 110, v.burbuja, 38)}${D.d20(890, 1230, 110, 14, true, TEAL, TEAL_L)}
        ${D.steps([200, 540, 880], 1420, 40, [v.paso1, v.paso2, v.paso3], INK, 22)}
        ${D.pillAuto(540, 1580, 84, INK, CREAM, v.cta, 30, { anchor: "middle" })}
        <text x="540" y="1716" text-anchor="middle" class="sans" font-weight="700" font-size="30" fill="${INK}">${D.esc([v.web, v.usuario].filter(Boolean).join(" · "))}</text>`;
    },
  });

  // ------------------------------------------------------------ PODCAST
  const podFields = [f.etiqueta("PODCAST NARRATIVO"),
    { key: "linea1", label: "Titular línea 1", type: "text", default: "DEL JUEGO" },
    { key: "linea2", label: "Titular línea 2 (destacada)", type: "text", default: "AL AIRE." },
    { key: "texto", label: "Texto", type: "textarea", default: "Reproduce nuestras series narrativas y acompáñanos a imaginar nuevos mundos." },
    { key: "cta", label: "Botón", type: "text", default: "▶  ESCÚCHALO EN SPOTIFY" }, f.usuario];

  add({
    id: "podcast_cuadrado", name: "Podcast 1:1", group: "Podcast", w: 1080, h: 1080, fields: podFields,
    render(v) {
      const p = D.paragraph(64, 800, v.texto, 30, 900, INK, { maxLines: 2, lineHeight: 40 });
      return `${D.background(1080, 1080, INK, true)}${D.corner(1080, SUN, CORAL)}${D.header(110, 104, 1, CREAM)}
        ${D.pillAuto(64, 186, 50, TEAL, INK, v.etiqueta, 20)}
        ${D.headline(60, 390, v.linea1, D.fit(v.linea1, 156, 600), CREAM)}
        ${D.headline(60, 550, v.linea2, D.fit(v.linea2, 178, 600), SUN, TEAL, 10)}
        <path d="M0,690 L1080,628 L1080,668 L0,730 Z" fill="${CREAM}"/>
        <path d="M0,730 L1080,668 L1080,1080 L0,1080 Z" fill="${TEAL}"/><path d="M0,730 L1080,668 L1080,1080 L0,1080 Z" fill="url(#dots)"/>
        ${D.mic(870, 430, 1.0, CREAM)}${D.d20(640, 640, 62, 12, false)}${D.sparkle(980, 250, 40, CREAM)}${D.sparkle(700, 210, 54, SUN)}
        ${p.svg}${D.waveform(64, 1016, 910, 56, INK)}
        ${D.pillAuto(64, 970, 70, INK, CREAM, v.cta, 24)}
        <text x="1016" y="1016" text-anchor="end" class="sans" font-weight="700" font-size="28" fill="${INK}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "podcast_historia", name: "Podcast historia", group: "Podcast", w: 1080, h: 1920, fields: podFields,
    render(v) {
      const p = D.paragraph(540, 1420, v.texto, 34, 900, INK, { maxLines: 2, lineHeight: 44, anchor: "middle" });
      return `${D.background(1080, 1920, INK, true)}${D.corner(1080, SUN, CORAL, 260)}${D.header(132, 300, 1.22, CREAM)}
        ${D.pillAuto(76, 400, 60, TEAL, INK, v.etiqueta, 24)}
        ${D.headline(70, 660, v.linea1, D.fit(v.linea1, 210, 860), CREAM)}
        ${D.headline(70, 870, v.linea2, D.fit(v.linea2, 236, 860), SUN, TEAL, 12)}
        ${D.sparkle(980, 500, 70, SUN)}${D.sparkle(930, 800, 40, CREAM)}
        <path d="M0,1300 L1080,1240 L1080,1282 L0,1342 Z" fill="${CREAM}"/>
        <path d="M0,1342 L1080,1282 L1080,1920 L0,1920 Z" fill="${TEAL}"/><path d="M0,1342 L1080,1282 L1080,1920 L0,1920 Z" fill="url(#dots)"/>
        ${D.mic(560, 1046, 0.95, CREAM)}${D.d20(190, 1160, 90, -12)}${D.meeple(845, 1110, 100, SUN)}${D.sparkle(120, 990, 44, CREAM)}
        ${p.svg}${D.waveform(76, 1004, 1540, 64, INK)}
        ${D.pillAuto(540, 1590, 80, INK, CREAM, v.cta, 28, { anchor: "middle" })}
        <text x="540" y="1730" text-anchor="middle" class="sans" font-weight="700" font-size="30" fill="${INK}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "podcast_episodio", name: "Portada de episodio (3000 px)", group: "Podcast", w: 1080, h: 1080, out: { w: 3000, h: 3000 },
    fields: [{ key: "seccion", label: "Sección del menú", type: "select", options: MENU, default: MENU[0] ? MENU[0][0] : "Mesa Principal" },
      { key: "numero", label: "Número (opcional, ej. EP. 03)", type: "text", default: "" },
      { key: "titulo", label: "Título del episodio", type: "text", default: "Press Start" }],
    render(v) {
      const sec = T.podcastMenu.find((m) => m.name === v.seccion) || { color: "coral" };
      const bg = COLOR[sec.color] || CORAL;
      const accent = bg === TEAL ? SUN : bg === SUN ? CORAL : TEAL;
      let size = 140, lines;
      for (;;) { lines = D.wrap(String(v.titulo).toUpperCase(), size, 960, "cond", 800); if (lines.length <= 2 || size <= 80) break; size -= 10; }
      const lh = size * 0.93, y0 = 900 - (lines.length - 1) * lh;
      const title = lines.map((l, k) => D.headline(540, n(y0 + k * lh), l, size, INK, CREAM, 8, "middle")).join("");
      const menu = ["MENÚ", String(v.seccion).toUpperCase(), v.numero && String(v.numero).toUpperCase()].filter(Boolean).join(" · ");
      return `${D.background(1080, 1080, bg)}${D.corner(1080, accent, CREAM, 160)}${D.header(100, 96, 0.9, INK, "PODCAST DE ROL")}
        ${D.pillAuto(64, 170, 52, INK, CREAM, menu, 22)}
        <circle cx="540" cy="${y0 - 330}" r="210" fill="${CREAM}" stroke="${INK}" stroke-width="8"/>
        <circle cx="540" cy="${y0 - 330}" r="160" fill="none" stroke="${INK}" stroke-width="3" opacity="0.25"/>
        ${D.d20(540, y0 - 340, 120, -10, true, accent === CREAM ? SUN : accent)}${D.sparkle(820, y0 - 480, 56, CREAM)}${title}`;
    },
  });
  const n = (x) => Math.round(x * 10) / 10;

  // ------------------------------------------------------------ CARRUSEL
  add({
    id: "carrusel_portada", name: "Carrusel: portada", group: "Carrusel", w: 1080, h: 1350,
    fields: [f.etiqueta("CÓMO FUNCIONA"), { key: "linea1", label: "Titular línea 1", type: "text", default: "DE LA IDEA" },
      { key: "linea2", label: "Titular línea 2 (destacada)", type: "text", default: "AL AIRE." },
      { key: "texto", label: "Texto", type: "text", default: "Encuentros que luego se convierten en sonido." },
      { key: "icono1", label: "Ícono 1", type: "select", options: ICON_OPTS, default: "idea" }, { key: "paso1", label: "Etiqueta 1", type: "text", default: "POSTULA" },
      { key: "icono2", label: "Ícono 2", type: "select", options: ICON_OPTS, default: "dado" }, { key: "paso2", label: "Etiqueta 2", type: "text", default: "JUGAMOS" },
      { key: "icono3", label: "Ícono 3", type: "select", options: ICON_OPTS, default: "microfono" }, { key: "paso3", label: "Etiqueta 3", type: "text", default: "AL AIRE" },
      { key: "total", label: "Total de láminas", type: "number", default: 5 }],
    render(v) {
      const items = [[220, TEAL, v.icono1, v.paso1], [540, CORAL, v.icono2, v.paso2], [860, SUN, v.icono3, v.paso3]];
      return `${D.background(1080, 1350, INK, true)}${D.corner(1080, SUN, CORAL)}${D.header(110, 104, 1, CREAM)}
        ${D.pillAuto(64, 186, 50, TEAL, INK, v.etiqueta, 20)}
        ${D.headline(60, 420, v.linea1, D.fit(v.linea1, 176, 860), CREAM)}
        ${D.headline(60, 610, v.linea2, D.fit(v.linea2, 200, 860), SUN, TEAL, 10)}
        <text x="64" y="690" class="sans" font-weight="600" font-size="${D.fit(v.texto, 32, 950, "sans", 600)}" fill="${CREAM}">${D.esc(v.texto)}</text>
        <path d="M220,940 H860" stroke="${CREAM}" stroke-width="6" stroke-dasharray="4 18" stroke-linecap="round"/>
        ${items.map(([cx, c, ic, t]) => `<circle cx="${cx}" cy="940" r="110" fill="${c}" stroke="${CREAM}" stroke-width="6"/>${D.icon(ic, cx, 940, 120)}
          <text x="${cx}" y="1110" text-anchor="middle" class="sans" font-weight="700" font-size="${D.fit(t, 24, 300, "sans", 700, 3)}" fill="${CREAM}" letter-spacing="3">${D.esc(String(t).toUpperCase())}</text>`).join("")}
        ${D.sparkle(960, 300, 60, SUN)}${carouselFooter(1, v.total, CREAM, "DESLIZA →")}`;
    },
  });

  function carouselFooter(pos, total, ink, label) {
    total = Math.max(1, Math.min(10, Number(total) || 5));
    const dots = Array.from({ length: total }, (_, j) => `<circle cx="${1016 - (total - 1 - j) * 30}" cy="1290" r="9" fill="${ink}" opacity="${j === pos - 1 ? 1 : 0.3}"/>`).join("");
    return `<text x="64" y="1300" class="sans" font-weight="700" font-size="24" fill="${ink}" letter-spacing="3">${D.esc(label)}</text>${dots}`;
  }

  add({
    id: "carrusel_paso", name: "Carrusel: lámina de contenido", group: "Carrusel", w: 1080, h: 1350,
    fields: [{ key: "color", label: "Color de fondo", type: "select", options: COLOR_OPTS.filter(([k]) => k !== "ink"), default: "teal" },
      { key: "numero", label: "Número grande", type: "text", default: "01" },
      { key: "icono", label: "Ícono", type: "select", options: ICON_OPTS, default: "idea" },
      { key: "titulo", label: "Título", type: "text", default: T.process[0].title },
      { key: "texto", label: "Texto", type: "textarea", default: T.process[0].text },
      { key: "boton", label: "Etiqueta inferior (opcional)", type: "text", default: T.process[0].short.toUpperCase() },
      { key: "posicion", label: "Posición de la lámina", type: "number", default: 2 }, { key: "total", label: "Total de láminas", type: "number", default: 5 },
      { key: "pie", label: "Texto del pie", type: "text", default: "DESLIZA →" }],
    render(v) {
      const bg = COLOR[v.color] || TEAL;
      let size = 124, tl;
      for (;;) { tl = D.wrap(String(v.titulo).toUpperCase(), size, 950, "cond", 800); if (tl.length <= 3 || size <= 70) break; size -= 8; }
      const lh = size * 0.95;
      const titleSvg = tl.map((l, k) => `<text x="64" y="${n(640 + k * lh)}" class="cond" font-size="${size}" fill="${INK}">${D.esc(l)}</text>`).join("");
      const p = D.paragraph(64, 640 + tl.length * lh + 40, v.texto, 38, 900, INK, { maxLines: 5, lineHeight: 50 });
      return `${D.background(1080, 1350, bg)}${D.header(110, 104, 1, INK)}
        ${D.headline(56, 470, v.numero, D.fit(v.numero, 330, 560), CREAM, INK, 14)}
        <circle cx="830" cy="350" r="170" fill="${CREAM}" stroke="${INK}" stroke-width="8"/>${D.icon(v.icono, 830, 350, 200)}
        ${D.sparkle(1000, 190, 50, INK)}${titleSvg}${p.svg}
        ${v.boton ? D.pillAuto(64, 1150, 60, INK, CREAM, v.boton, 22) : ""}
        ${carouselFooter(Number(v.posicion) || 2, v.total, INK, v.pie)}`;
    },
  });

  // ------------------------------------------------------------ DESTACADA
  add({
    id: "destacada", name: "Portada de destacada", group: "Perfil", w: 1080, h: 1920,
    fields: [{ key: "icono", label: "Ícono", type: "select", options: ICON_OPTS, default: "d20" },
      { key: "etiqueta", label: "Etiqueta", type: "text", default: "ROL" },
      { key: "color", label: "Color de fondo", type: "select", options: COLOR_OPTS, default: "teal" }],
    render(v) {
      const bg = COLOR[v.color] || TEAL;
      return `${D.background(1080, 1920, bg, bg === INK)}
        <circle cx="540" cy="960" r="330" fill="${CREAM}" stroke="${INK}" stroke-width="12"/>${D.icon(v.icono, 540, 960, 380, INK, 3.5)}
        <text x="540" y="1420" text-anchor="middle" class="cond" font-size="${D.fit(v.etiqueta, 90, 900, "cond", 800, 4)}" fill="${bg === INK ? CREAM : INK}" letter-spacing="4">${D.esc(v.etiqueta)}</text>`;
    },
  });

  window.TPDTemplates = templates;
})();
