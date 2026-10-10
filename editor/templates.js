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
  const INFO = SCHEDULE ? `SÁBADOS · ${SCHEDULE.toUpperCase()}` : "";

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
      for (;;) { lines = D.wrapBalanced(String(v.titulo).toUpperCase(), size, 960, "cond", 800); if (lines.length <= 2 || size <= 80) break; size -= 10; }
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
      for (;;) { tl = D.wrapBalanced(String(v.titulo).toUpperCase(), size, 950, "cond", 800); if (tl.length <= 3 || size <= 70) break; size -= 8; }
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

  // ============================================================ FOTOS
  const foto = (key = "foto", label = "Foto") => ({ key, label, type: "image", default: "" });
  const enfoque = (key = "enfoque") => ({ key, label: "Enfoque de la foto", type: "select", options: D.FOCUS_OPTS, default: "centro" });
  const STICKER_OPTS = [["d20", "Dado d20"], ["mic", "Micrófono"], ["meeple", "Meeple"], ["destello", "Destellos"], ["ninguno", "Ninguno"]];
  function sticker(kind, x, y, s = 1) {
    if (kind === "d20") return D.d20(x, y, 95 * s, 12);
    if (kind === "mic") return `<circle cx="${x}" cy="${y}" r="${95 * s}" fill="${CORAL}" stroke="${INK}" stroke-width="${7 * s}"/>${D.mic(x, y - 8 * s, 0.38 * s, INK, false)}`;
    if (kind === "meeple") return `<circle cx="${x}" cy="${y}" r="${90 * s}" fill="${SUN}" stroke="${INK}" stroke-width="${7 * s}"/>${D.meeple(x - 60 * s, y - 62 * s, 120 * s, INK)}`;
    if (kind === "destello") return D.sparkle(x, y, 110 * s, SUN) + D.sparkle(x - 90 * s, y + 70 * s, 50 * s, CREAM);
    return "";
  }
  const headerChip = (x, y, s = 1) => `<rect x="${x}" y="${y}" width="${470 * s}" height="${104 * s}" rx="${52 * s}" fill="${CREAM}" stroke="${INK}" stroke-width="${4 * s}"/>${D.header(x + 56 * s, y + 52 * s, s * 0.95, INK)}`;

  add({
    id: "foto_post", name: "Foto con marco 4:5", group: "Fotos", w: 1080, h: 1350,
    fields: [foto(), enfoque(), f.receta, f.etiqueta("ARCHIVO"), { key: "titulo", label: "Título", type: "text", default: "LA MESA ES UN TERRITORIO" },
      { key: "texto", label: "Texto", type: "textarea", default: "Personas que se reúnen para imaginar juntas." },
      { key: "sticker", label: "Sticker", type: "select", options: STICKER_OPTS, default: "d20" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const p = D.paragraph(64, 1160, v.texto, 32, 950, r.ink, { maxLines: 2, lineHeight: 40 });
      return `${D.background(1080, 1350, r.bg, r.light)}${D.corner(1080, ...r.corner)}${D.header(110, 96, 1, r.ink)}
        ${D.photo(64, 170, 952, 800, v.foto, { focus: v.enfoque, shadow: true })}
        ${v.etiqueta ? D.pillAuto(96, 200, 52, INK, CREAM, v.etiqueta, 20) : ""}
        ${sticker(v.sticker, 955, 950)}
        ${D.headline(64, 1100, v.titulo, D.fit(v.titulo, 100, v.sticker === "ninguno" ? 950 : 820), r.ink)}
        ${p.svg}
        <text x="1016" y="1300" text-anchor="end" class="sans" font-weight="700" font-size="28" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "foto_cuadrado", name: "Foto con marco 1:1", group: "Fotos", w: 1080, h: 1080,
    fields: [foto(), enfoque(), f.receta, f.etiqueta(""), { key: "titulo", label: "Título", type: "text", default: "HISTORIAS COMPARTIDAS" },
      { key: "texto", label: "Texto (1 línea)", type: "text", default: "Encuentros que luego se convierten en sonido." },
      { key: "sticker", label: "Sticker", type: "select", options: STICKER_OPTS, default: "meeple" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      return `${D.background(1080, 1080, r.bg, r.light)}${D.corner(1080, ...r.corner, 150)}${D.header(110, 96, 1, r.ink)}
        ${D.photo(64, 170, 952, 640, v.foto, { focus: v.enfoque, shadow: true })}
        ${v.etiqueta ? D.pillAuto(96, 200, 52, INK, CREAM, v.etiqueta, 20) : ""}
        ${sticker(v.sticker, 960, 790, 0.9)}
        ${D.headline(64, 920, v.titulo, D.fit(v.titulo, 96, v.sticker === "ninguno" ? 950 : 830), r.ink)}
        <text x="64" y="975" class="sans" font-weight="600" font-size="${D.fit(v.texto, 30, 950, "sans", 600)}" fill="${r.ink}">${D.esc(v.texto)}</text>
        <text x="1016" y="1040" text-anchor="end" class="sans" font-weight="700" font-size="26" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "foto_historia", name: "Foto historia 9:16", group: "Fotos", w: 1080, h: 1920,
    fields: [foto(), enfoque(), f.receta, f.etiqueta(""), { key: "titulo1", label: "Título línea 1", type: "text", default: "ESTO PASÓ" },
      { key: "titulo2", label: "Título línea 2 (destacada)", type: "text", default: "EN LA MESA." },
      { key: "texto", label: "Texto", type: "textarea", default: "Personas que se reúnen para imaginar juntas." }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const p = D.paragraph(76, 1615, v.texto, 40, 920, r.ink, { maxLines: 2, lineHeight: 50 });
      return `${D.background(1080, 1920, r.bg, r.light)}
        ${D.photo(0, 0, 1080, 1260, v.foto, { focus: v.enfoque, stroke: false, path: "M0,0 H1080 V1180 L0,1262 Z" })}
        <path d="M0,1262 L1080,1180 L1080,1222 L0,1304 Z" fill="${CREAM}"/><path d="M0,1262 L1080,1180" stroke="${INK}" stroke-width="6"/>
        ${headerChip(64, 250)}
        ${v.etiqueta ? D.pillAuto(76, 1120, 56, INK, CREAM, v.etiqueta, 22) : ""}
        ${D.headline(72, 1440, v.titulo1, D.fit(v.titulo1, 130, 930), r.ink)}
        ${D.headline(72, 1560, v.titulo2, D.fit(v.titulo2, 150, 900), r.hl, r.hlShadow, 9)}
        ${p.svg}
        <text x="1004" y="1720" text-anchor="end" class="sans" font-weight="700" font-size="30" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "foto_cita", name: "Foto con cita 4:5", group: "Fotos", w: 1080, h: 1350,
    fields: [foto(), enfoque(), { key: "cita", label: "Cita / frase", type: "textarea", default: "Nos reunimos para inventar mundos y terminamos encontrando nuevas formas de habitar el nuestro." },
      { key: "autor", label: "Autor/a (opcional)", type: "text", default: "Tazón para Dos" }, f.usuario],
    render(v) {
      let size = 74, lines;
      for (;;) { lines = D.wrap(String(v.cita).toUpperCase(), size, 950, "cond", 800); if (lines.length <= 4 || size <= 44) break; size -= 4; }
      lines = lines.slice(0, 4);
      const lh = size * 0.98, y0 = 1010;
      const quote = lines.map((l, i) => `<text x="64" y="${Math.round(y0 + i * lh)}" class="cond" font-size="${size}" fill="${CREAM}">${D.esc(l)}</text>`).join("");
      const ay = y0 + (lines.length - 1) * lh + 62;
      return `${D.photo(0, 0, 1080, 960, v.foto, { focus: v.enfoque, stroke: false, rx: 0 })}
        <path d="M0,900 L1080,840 V1350 H0 Z" fill="${INK}"/><path d="M0,900 L1080,840 V1350 H0 Z" fill="url(#dotsLight)"/>
        <path d="M0,900 L1080,840 L1080,852 L0,912 Z" fill="${SUN}"/>
        ${headerChip(64, 64)}
        <circle cx="950" cy="850" r="74" fill="${SUN}" stroke="${INK}" stroke-width="7"/>
        <text x="950" y="925" text-anchor="middle" class="cond" font-size="190" fill="${INK}">“</text>
        ${quote}
        ${v.autor ? `<text x="64" y="${Math.round(ay)}" class="sans" font-weight="700" font-size="30" fill="${SUN}" letter-spacing="2">— ${D.esc(v.autor)}</text>` : ""}
        <text x="1016" y="1300" text-anchor="end" class="sans" font-weight="700" font-size="26" fill="${CREAM}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "collage", name: "Collage de 3 fotos 4:5", group: "Fotos", w: 1080, h: 1350,
    fields: [foto("foto1", "Foto grande"), enfoque("enfoque1"), foto("foto2", "Foto 2"), enfoque("enfoque2"), foto("foto3", "Foto 3"), enfoque("enfoque3"),
      f.receta, f.etiqueta("ASÍ VAMOS"), { key: "titulo", label: "Título", type: "text", default: "CRÓNICAS DE LA MESA" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      return `${D.background(1080, 1350, r.bg, r.light)}${D.corner(1080, ...r.corner, 150)}${D.header(110, 96, 1, r.ink)}
        ${D.photo(64, 170, 952, 560, v.foto1, { focus: v.enfoque1, shadow: true })}
        ${D.photo(64, 760, 466, 400, v.foto2, { focus: v.enfoque2, shadow: true, rx: 22 })}
        ${D.photo(560, 760, 456, 400, v.foto3, { focus: v.enfoque3, shadow: true, rx: 22 })}
        ${v.etiqueta ? D.pillAuto(96, 200, 52, INK, CREAM, v.etiqueta, 20) : ""}
        ${D.sparkle(1010, 735, 70, r.accent)}
        ${D.headline(64, 1270, v.titulo, D.fit(v.titulo, 96, 700), r.ink)}
        <text x="1016" y="1268" text-anchor="end" class="sans" font-weight="700" font-size="26" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  // ============================================================ VIDEO
  const BOX = { sol: [SUN, INK], crema: [CREAM, INK], turquesa: [TEAL, INK], coral: [CORAL, INK], tinta: [INK, CREAM] };
  const BOX_OPTS = [["sol", "Tinta sobre sol"], ["crema", "Tinta sobre crema"], ["turquesa", "Tinta sobre turquesa"], ["coral", "Tinta sobre coral"], ["tinta", "Crema sobre tinta"]];

  add({
    id: "video_portada", name: "Portada de Reel / video 9:16", group: "Video", w: 1080, h: 1920,
    fields: [foto("foto", "Foto o fotograma"), enfoque(), f.etiqueta("REEL"), { key: "titulo", label: "Título", type: "text", default: "ASÍ SE VIVE UNA PARTIDA" },
      { key: "caja", label: "Color de la caja del título", type: "select", options: BOX_OPTS, default: "sol" },
      { key: "play", label: "Mostrar botón de reproducción", type: "checkbox", default: true }, f.usuario],
    render(v) {
      const [fill, ink] = BOX[v.caja] || BOX.sol;
      let size = 120, tb;
      for (;;) { tb = D.textBox(540, 700, String(v.titulo).toUpperCase(), size, 900, fill, ink, { kind: "cond", weight: 800, maxLines: 3 }); if (tb.width <= 940 || size <= 70) break; size -= 6; }
      return `${D.photo(0, 0, 1080, 1920, v.foto, { focus: v.enfoque, stroke: false, rx: 0 })}
        ${headerChip(64, 250, 1.3)}
        ${v.etiqueta ? D.pillAuto(540, 590, 76, INK, CREAM, v.etiqueta, 32, { anchor: "middle" }) : ""}
        ${tb.svg}
        ${v.play ? D.playBadge(540, 700 + tb.height + 190, 110) : ""}
        ${D.pillAuto(540, 1400, 84, CREAM, INK, v.usuario, 36, { anchor: "middle", stroke: INK })}`;
    },
  });

  add({
    id: "miniatura", name: "Miniatura de video 16:9", group: "Video", w: 1280, h: 720,
    fields: [foto("foto", "Foto o fotograma"), enfoque(), f.receta, f.etiqueta("PODCAST · EP. 07"),
      { key: "titulo", label: "Título", type: "text", default: "LA TABERNA DEL DRAGÓN" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      let size = 110, lines;
      for (;;) { lines = D.wrapBalanced(String(v.titulo).toUpperCase(), size, 500, "cond", 800); if (lines.length <= 3 || size <= 56) break; size -= 6; }
      lines = lines.slice(0, 3);
      const lh = size * 0.95, y0 = 250 + size * 0.8;
      const title = lines.map((l, i) => D.headline(56, Math.round(y0 + i * lh), l, size, i === lines.length - 1 ? r.hl : r.ink, i === lines.length - 1 ? r.hlShadow : null, 6)).join("");
      return `${D.background(1280, 720, r.bg, r.light)}
        ${D.photo(0, 0, 1280, 720, v.foto, { focus: v.enfoque, stroke: false, path: "M640,0 H1280 V720 H540 Z" })}
        <path d="M612,0 H640 L540,720 H512 Z" fill="${CREAM}"/><path d="M640,0 L540,720" stroke="${INK}" stroke-width="6"/>
        ${D.header(96, 80, 0.85, r.ink)}
        ${v.etiqueta ? D.pillAuto(56, 160, 52, r.ink === CREAM ? TEAL : INK, r.ink === CREAM ? INK : CREAM, v.etiqueta, 20) : ""}
        ${title}
        ${D.playBadge(1150, 590, 70)}
        <text x="56" y="670" class="sans" font-weight="700" font-size="26" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "overlay_reel", name: "Capa de marca para Reel (transparente)", group: "Video", w: 1080, h: 1920, transparent: true,
    fields: [f.etiqueta(""), f.usuario, { key: "info", label: "Información (horario, lugar…)", type: "text", default: INFO },
      { key: "sello", label: "Mostrar cabecera con el logo", type: "checkbox", default: true },
      { key: "pos", label: "Posición de usuario e información", type: "select", options: [["izquierda", "Abajo a la izquierda"], ["centro", "Abajo al centro"]], default: "izquierda" }],
    render(v) {
      const c = v.pos === "centro";
      const o = (extra = {}) => (c ? { anchor: "middle", ...extra } : extra);
      const x = c ? 540 : 64;
      return `${v.sello ? headerChip(64, 250, 1.25) : ""}
        ${v.etiqueta ? D.pillAuto(64, v.sello ? 404 : 270, 72, INK, CREAM, v.etiqueta, 30) : ""}
        ${v.info ? D.pillAuto(x, 1306, 72, SUN, INK, v.info, 30, o({ stroke: INK })) : ""}
        ${D.pillAuto(x, 1396, 84, CREAM, INK, v.usuario, 36, o({ stroke: INK }))}`;
    },
  });

  function lowerThird(x, y, nombre, rol, s = 1, maxW = 1100) {
    const ns = D.fit(String(nombre).toUpperCase(), 64 * s, maxW - 210 * s), rs = D.fit(rol, 30 * s, maxW - 210 * s, "sans", 700);
    const w = Math.max(D.measure(String(nombre).toUpperCase(), "cond", ns), D.measure(rol, "sans", rs, 700)) + 210 * s;
    const h = 150 * s;
    return `<rect x="${x + 10 * s}" y="${y + 10 * s}" width="${w}" height="${h}" rx="${24 * s}" fill="${INK}" opacity="0.35"/>
      <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${24 * s}" fill="${INK}"/>
      <rect x="${x}" y="${y + h - 12 * s}" width="${w}" height="${12 * s}" fill="${SUN}"/>
      <circle cx="${x + 80 * s}" cy="${y + h / 2 - 4 * s}" r="${54 * s}" fill="${CREAM}" stroke="${TEAL}" stroke-width="${5 * s}"/>
      <use href="#bowl" x="${x + 46 * s}" y="${y + h / 2 - 40 * s}" width="${68 * s}" height="${70 * s}"/>
      <text x="${x + 160 * s}" y="${y + 74 * s}" class="cond" font-size="${ns}" fill="${CREAM}">${D.esc(String(nombre).toUpperCase())}</text>
      <text x="${x + 162 * s}" y="${y + 116 * s}" class="sans" font-weight="700" font-size="${rs}" fill="${SUN}">${D.esc(rol)}</text>`;
  }
  const ltFields = [{ key: "nombre", label: "Nombre", type: "text", default: "Nombre Apellido" }, { key: "rol", label: "Rol / descripción", type: "text", default: "Narración · Tazón para Dos" }];
  add({ id: "tercio_inferior_h", name: "Rótulo de nombre 16:9 (transparente)", group: "Video", w: 1920, h: 1080, transparent: true, fields: ltFields, render: (v) => lowerThird(96, 790, v.nombre, v.rol, 1.2, 1300) });
  add({ id: "tercio_inferior_v", name: "Rótulo de nombre 9:16 (transparente)", group: "Video", w: 1080, h: 1920, transparent: true, fields: ltFields, render: (v) => lowerThird(64, 1130, v.nombre, v.rol, 1.05, 952) });

  add({
    id: "texto_pantalla", name: "Texto en pantalla 9:16 (transparente)", group: "Video", w: 1080, h: 1920, transparent: true,
    fields: [{ key: "texto", label: "Texto", type: "textarea", default: "¿Qué harías si tu personaje tuviera que elegir?" },
      { key: "caja", label: "Estilo", type: "select", options: BOX_OPTS, default: "tinta" },
      { key: "fuente", label: "Tipografía", type: "select", options: [["sans", "Texto (Barlow)"], ["cond", "Titular (Barlow Condensed)"]], default: "sans" },
      { key: "tam", label: "Tamaño", type: "number", default: 66 },
      { key: "pos", label: "Posición", type: "select", options: [["arriba", "Arriba"], ["centro", "Centro"], ["abajo", "Abajo (zona de subtítulos)"]], default: "abajo" }],
    render(v) {
      const [fill, ink] = BOX[v.caja] || BOX.tinta;
      const kind = v.fuente === "cond" ? "cond" : "sans";
      const txt = kind === "cond" ? String(v.texto).toUpperCase() : v.texto;
      const tb = D.textBox(540, 0, txt, Math.max(24, Math.min(120, Number(v.tam) || 54)), 900, fill, ink, { kind, weight: kind === "cond" ? 800 : 700, maxLines: 4 });
      const y = v.pos === "arriba" ? 440 : v.pos === "centro" ? 960 - tb.height / 2 : 1276 - tb.height;   // termina sobre la información de la capa de marca
      return `<g transform="translate(0,${Math.round(y)})">${tb.svg}</g>`;
    },
  });

  function endCard(w, h, v) {
    const r = RECIPES[v.receta];
    const H = w < h;   // vertical
    const icons = ["dado", "d20", "microfono"].map((ic, i) => {
      const cx = H ? 540 + (i - 1) * 200 : 1080 + i * 180, cy = H ? 1520 : 920;
      return `<circle cx="${cx}" cy="${cy}" r="72" fill="${[TEAL, CORAL, SUN][i] === r.bg ? CREAM : [TEAL, CORAL, SUN][i]}" stroke="${INK}" stroke-width="6"/>${D.icon(ic, cx, cy, 80)}`;
    }).join("");
    const seal = (cx, cy, rr) => `<circle cx="${cx + 12}" cy="${cy + 12}" r="${rr}" fill="${INK}"/><circle cx="${cx}" cy="${cy}" r="${rr}" fill="${CREAM}" stroke="${INK}" stroke-width="10"/><use href="#bowl" x="${cx - rr * 0.6}" y="${cy - rr * 0.63}" width="${rr * 1.2}" height="${rr * 1.24}"/>`;
    if (H) return `${D.background(w, h, r.bg, r.light)}${D.corner(w, ...r.corner, 260)}${seal(540, 560, 180)}
      ${D.headline(540, 920, v.linea1, D.fit(v.linea1, 130, 940), r.ink, null, 0, "middle")}
      ${D.headline(540, 1080, v.linea2, D.fit(v.linea2, 170, 900), r.hl, r.hlShadow, 10, "middle")}
      ${D.pillAuto(540, 1150, 104, r.bg === INK ? SUN : INK, r.bg === INK ? INK : CREAM, v.cta, 46, { anchor: "middle" })}
      <text x="540" y="1350" text-anchor="middle" class="sans" font-weight="700" font-size="${D.fit(v.sub, 42, 960, "sans", 700)}" fill="${r.ink}">${D.esc(v.sub)}</text>${icons}
      ${D.sparkle(180, 360, 80, r.accent)}${D.sparkle(900, 820, 50, CREAM)}`;
    return `${D.background(w, h, r.bg, r.light)}${D.corner(w, ...r.corner, 260)}${seal(440, 540, 240)}
      ${D.headline(780, 400, v.linea1, D.fit(v.linea1, 120, 1060), r.ink)}
      ${D.headline(780, 560, v.linea2, D.fit(v.linea2, 160, 1040), r.hl, r.hlShadow, 10)}
      ${D.pillAuto(780, 610, 104, r.bg === INK ? SUN : INK, r.bg === INK ? INK : CREAM, v.cta, 46)}
      <text x="782" y="800" class="sans" font-weight="700" font-size="${D.fit(v.sub, 42, 1080, "sans", 700)}" fill="${r.ink}">${D.esc(v.sub)}</text>${icons}
      ${D.sparkle(160, 180, 80, r.accent)}`;
  }
  const endFields = [f.receta, { key: "linea1", label: "Línea 1", type: "text", default: "¿TE GUSTÓ?" }, { key: "linea2", label: "Línea 2 (destacada)", type: "text", default: "VEN A JUGAR." },
    { key: "cta", label: "Botón", type: "text", default: "@tazonparados" }, { key: "sub", label: "Texto inferior", type: "text", default: "tazon-para-dos.online · Sábados 11 a.m. – 9 p.m." }];
  add({ id: "tarjeta_final_v", name: "Tarjeta final de video 9:16", group: "Video", w: 1080, h: 1920, fields: endFields, render: (v) => endCard(1080, 1920, v) });
  add({ id: "tarjeta_final_h", name: "Tarjeta final de video 16:9", group: "Video", w: 1920, h: 1080, fields: endFields, render: (v) => endCard(1920, 1080, v) });

  add({
    id: "guia_zonas", name: "Guía de zonas seguras 9:16 (transparente)", group: "Video", w: 1080, h: 1920, transparent: true,
    fields: [{ key: "notas", label: "Mostrar etiquetas", type: "checkbox", default: true }],
    render(v) {
      const lab = (x, y, t, a = "start") => v.notas ? `<text x="${x}" y="${y}" class="sans" font-weight="700" font-size="26" fill="${INK}" text-anchor="${a}" letter-spacing="2">${t}</text>` : "";
      return `<rect x="0" y="0" width="1080" height="250" fill="${CORAL}" opacity="0.45"/>${lab(540, 140, "INTERFAZ (NOMBRE, AUDIO) · EVITAR TEXTO", "middle")}
        <rect x="0" y="1500" width="1080" height="420" fill="${CORAL}" opacity="0.45"/>${lab(540, 1720, "DESCRIPCIÓN Y BOTONES · EVITAR TEXTO", "middle")}
        <rect x="940" y="900" width="140" height="600" fill="${CORAL}" opacity="0.45"/>${lab(1010, 880, "BOTONES", "middle")}
        <rect x="64" y="285" width="952" height="1350" fill="none" stroke="${TEAL}" stroke-width="6" stroke-dasharray="18 12"/>${lab(80, 325, "RECORTE 4:5 EN LA CUADRÍCULA")}
        <rect x="64" y="250" width="876" height="1250" fill="none" stroke="${INK}" stroke-width="4"/>${lab(80, 1480, "ZONA SEGURA PARA TEXTO")}`;
    },
  });

  // ---- Marco de video: deja una ventana transparente 16:9 para poner clips horizontales en un Reel 9:16
  const roundRect = (x, y, w, h, r) => `M${x + r},${y} H${x + w - r} A${r},${r} 0 0 1 ${x + w},${y + r} V${y + h - r} A${r},${r} 0 0 1 ${x + w - r},${y + h} H${x + r} A${r},${r} 0 0 1 ${x},${y + h - r} V${y + r} A${r},${r} 0 0 1 ${x + r},${y} Z`;
  add({
    id: "marco_video", name: "Marco para video horizontal en Reel (transparente)", group: "Video", w: 1080, h: 1920, transparent: true,
    fields: [f.receta, f.etiqueta("SÁBADOS · 11 A.M. – 9 P.M."), { key: "titulo", label: "Título (arriba)", type: "text", default: "ASÍ SE VIVE TAZÓN PARA DOS" },
      { key: "texto", label: "Texto (debajo del video)", type: "textarea", default: "Jugamos en comunidad." }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const W = { x: 60, y: 650, w: 960, h: 540, r: 26 };
      const win = roundRect(W.x, W.y, W.w, W.h, W.r);
      const full = "M0,0 H1080 V1920 H0 Z";
      const top = v.etiqueta ? 486 : 400;                       // debajo de la cabecera (y la etiqueta)
      let size = 100, lines;
      for (;;) {
        lines = D.wrapBalanced(String(v.titulo).toUpperCase(), size, 960, "cond", 800);
        const fits = lines.length <= 2 && top + size * (0.72 + (lines.length - 1) * 0.95) <= W.y - 28;
        if (fits || size <= 56) break;
        size -= 4;
      }
      lines = lines.slice(0, 2);
      const ty = Math.max(top + size * 0.72, W.y - 30 - (lines.length - 1) * size * 0.95);
      const title = lines.map((l, i) => D.headline(60, Math.round(ty + i * size * 0.95), l, size, i === lines.length - 1 ? r.hl : r.ink, i === lines.length - 1 ? r.hlShadow : null, 8)).join("");
      const tb = v.texto ? D.textBox(540, 1236, v.texto, 54, 960, r.bg === INK ? SUN : INK, r.bg === INK ? INK : CREAM, { maxLines: 2 }) : { svg: "" };
      return `<path fill-rule="evenodd" d="${full} ${win}" fill="${r.bg}"/><path fill-rule="evenodd" d="${full} ${win}" fill="url(#${r.light ? "dotsLight" : "dots"})"/>
        <path fill-rule="evenodd" d="${roundRect(W.x + 14, W.y + 14, W.w, W.h, W.r)} ${win}" fill="${INK}"/>
        <path d="${win}" fill="none" stroke="${INK}" stroke-width="10"/>
        ${D.corner(1080, ...r.corner, 260)}${headerChip(64, 250, 1.2)}
        ${v.etiqueta ? D.pillAuto(64, 398, 62, r.ink === CREAM ? TEAL : INK, r.ink === CREAM ? INK : CREAM, v.etiqueta, 26) : ""}
        ${title}${tb.svg}
        ${D.pillAuto(540, 1412, 80, CREAM, INK, v.usuario, 34, { anchor: "middle", stroke: INK })}
        ${D.sparkle(1012, 1212, 56, r.accent)}`;
    },
  });

  add({
    id: "texto_pantalla_h", name: "Texto en pantalla 16:9 (transparente)", group: "Video", w: 1920, h: 1080, transparent: true,
    fields: [{ key: "texto", label: "Texto", type: "textarea", default: "Ven a jugar. Quédate a compartir." },
      { key: "caja", label: "Estilo", type: "select", options: BOX_OPTS, default: "tinta" },
      { key: "fuente", label: "Tipografía", type: "select", options: [["sans", "Texto (Barlow)"], ["cond", "Titular (Barlow Condensed)"]], default: "sans" },
      { key: "tam", label: "Tamaño", type: "number", default: 72 },
      { key: "pos", label: "Posición", type: "select", options: [["arriba", "Arriba"], ["centro", "Centro"], ["abajo", "Abajo (subtítulos)"]], default: "abajo" }],
    render(v) {
      const [fill, ink] = BOX[v.caja] || BOX.tinta;
      const kind = v.fuente === "cond" ? "cond" : "sans";
      const txt = kind === "cond" ? String(v.texto).toUpperCase() : v.texto;
      const tb = D.textBox(960, 0, txt, Math.max(24, Math.min(140, Number(v.tam) || 56)), 1500, fill, ink, { kind, weight: kind === "cond" ? 800 : 700, maxLines: 3 });
      const y = v.pos === "arriba" ? 230 : v.pos === "centro" ? 540 - tb.height / 2 : 1000 - tb.height;
      return `<g transform="translate(0,${Math.round(y)})">${tb.svg}</g>`;
    },
  });

  add({
    id: "overlay_video_h", name: "Capa de marca 16:9 (transparente)", group: "Video", w: 1920, h: 1080, transparent: true,
    fields: [f.etiqueta(""), f.usuario, { key: "info", label: "Información (horario, lugar…)", type: "text", default: INFO },
      { key: "sello", label: "Mostrar cabecera con el logo", type: "checkbox", default: true }],
    render(v) {
      return `${v.sello ? headerChip(56, 48, 1.25) : ""}
        ${v.etiqueta ? D.pillAuto(56, v.sello ? 200 : 56, 72, INK, CREAM, v.etiqueta, 30) : ""}
        ${D.pillAuto(1864, 56, 84, CREAM, INK, v.usuario, 36, { anchor: "end", stroke: INK })}
        ${v.info ? D.pillAuto(1864, 160, 72, SUN, INK, v.info, 30, { anchor: "end", stroke: INK }) : ""}`;
    },
  });

  // ============================================================ FOTOS (más formatos)
  // Líneas de titular que caben en maxW, bajando el tamaño hasta maxLines
  function fitLines(text, size, maxW, maxLines, min = 48) {
    let lines;
    for (;;) { lines = D.wrapBalanced(String(text).toUpperCase(), size, maxW, "cond", 800); if (lines.length <= maxLines || size <= min) break; size -= 4; }
    return { lines: lines.slice(0, maxLines), size };
  }

  add({
    id: "foto_polaroid", name: "Fotos instantáneas 4:5", group: "Fotos", w: 1080, h: 1350,
    fields: [foto("foto", "Foto principal"), enfoque(), { key: "pie", label: "Pie de la foto principal", type: "text", default: "la primera tirada de la noche" },
      foto("foto2", "Segunda foto (opcional)"), enfoque("enfoque2"), f.receta,
      { key: "titulo", label: "Título", type: "text", default: "RECUERDOS DE LA MESA." }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const two = !!v.foto2;
      const pola = (cx, cy, rot, w, href, focus, cap, tape) => {
        const pw = w - 80, h = pw + (cap !== null ? 200 : 80);
        const x = -w / 2, y = -h / 2;
        const cs = cap ? D.fit(cap, 44, pw, "sans", 600) : 0;
        return `<g transform="translate(${cx},${cy}) rotate(${rot})">
          <rect x="${x + 14}" y="${y + 14}" width="${w}" height="${h}" rx="10" fill="${INK}"/>
          <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="${CREAM}" stroke="${INK}" stroke-width="7"/>
          ${D.photo(x + 40, y + 40, pw, pw, href, { focus, rx: 4, strokeWidth: 5 })}
          ${cap ? `<text x="0" y="${y + pw + 135}" text-anchor="middle" class="sans" font-weight="600" font-style="italic" font-size="${cs}" fill="${INK}">${D.esc(cap)}</text>` : ""}
          <rect x="-80" y="${y - 28}" width="160" height="56" fill="${tape}" stroke="${INK}" stroke-width="4" transform="rotate(${-rot * 0.8 + 3} 0 ${y})"/></g>`;
      };
      const t = fitLines(v.titulo, 96, 950, 1, 56);
      return `${D.background(1080, 1350, r.bg, r.light)}${D.corner(1080, ...r.corner)}${D.header(110, 96, 1, r.ink)}
        ${two ? pola(820, 470, 8, 380, v.foto2, v.enfoque2, null, r.accent) : D.sparkle(930, 330, 80, r.accent) + D.sparkle(1000, 430, 36, CREAM)}
        ${pola(two ? 440 : 520, 690, -4, 720, v.foto, v.enfoque, v.pie, SUN)}
        ${D.headline(64, 1240, t.lines[0], t.size, r.ink)}
        <text x="1016" y="1305" text-anchor="end" class="sans" font-weight="700" font-size="28" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "foto_comparada", name: "Dos fotos comparadas 4:5", group: "Fotos", w: 1080, h: 1350,
    fields: [foto("foto1", "Foto izquierda"), enfoque("enfoque1"), { key: "etiqueta1", label: "Etiqueta izquierda", type: "text", default: "PERSONAJE" },
      foto("foto2", "Foto derecha"), enfoque("enfoque2"), { key: "etiqueta2", label: "Etiqueta derecha", type: "text", default: "JUGADOR" },
      { key: "insignia", label: "Insignia central", type: "select", options: [["flecha", "Flecha"], ["vs", "VS"], ["ninguna", "Ninguna"]], default: "flecha" },
      f.receta, { key: "titulo", label: "Título", type: "text", default: "DETRÁS DE CADA PERSONAJE." },
      { key: "texto", label: "Texto (1 línea)", type: "text", default: "Hay alguien que lo imaginó." }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const L = "M64,170 H600 L480,1110 H64 Z", R = "M624,170 H1016 V1110 H504 Z";
      const badge = v.insignia === "vs"
        ? `<circle cx="562" cy="650" r="74" fill="${SUN}" stroke="${INK}" stroke-width="7"/><text x="562" y="680" text-anchor="middle" class="cond" font-size="84" fill="${INK}">VS</text>`
        : v.insignia === "flecha"
          ? `<circle cx="562" cy="650" r="74" fill="${SUN}" stroke="${INK}" stroke-width="7"/><path d="M522,650 H600 M574,620 L604,650 L574,680" fill="none" stroke="${INK}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`
          : "";
      const t = fitLines(v.titulo, 90, 950, 1, 56);
      return `${D.background(1080, 1350, r.bg, r.light)}${D.corner(1080, ...r.corner, 150)}${D.header(110, 96, 1, r.ink)}
        <path d="M76,182 H1028 V1122 H76 Z" fill="${INK}"/>
        ${D.photo(64, 170, 536, 940, v.foto1, { focus: v.enfoque1, path: L })}
        ${D.photo(504, 170, 512, 940, v.foto2, { focus: v.enfoque2, path: R })}
        ${D.pillAuto(96, 200, 56, INK, CREAM, v.etiqueta1, 22)}${D.pillAuto(984, 1030, 56, CREAM, INK, v.etiqueta2, 22, { anchor: "end", stroke: INK })}
        ${badge}
        ${D.headline(64, 1225, t.lines[0], t.size, r.ink)}
        <text x="64" y="1290" class="sans" font-weight="600" font-size="${D.fit(v.texto, 32, 620, "sans", 600)}" fill="${r.ink}">${D.esc(v.texto)}</text>
        <text x="1016" y="1290" text-anchor="end" class="sans" font-weight="700" font-size="28" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "foto_carrusel", name: "Carrusel de fotos (lámina) 4:5", group: "Fotos", w: 1080, h: 1350,
    fields: [foto(), enfoque(), f.receta, { key: "numero", label: "Número de lámina", type: "number", default: 2 }, { key: "total", label: "Total de láminas", type: "number", default: 5 },
      { key: "titulo", label: "Título", type: "text", default: "PRIMERO, LA MESA." },
      { key: "texto", label: "Texto (hasta 2 líneas)", type: "textarea", default: "Llegamos temprano, sacamos los dados y repartimos las fichas de personaje." },
      { key: "desliza", label: "Mostrar «Desliza»", type: "checkbox", default: true }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const num = `${Number(v.numero) || 1}/${Number(v.total) || 1}`;
      const t = fitLines(v.titulo, 84, 800, 1, 52);
      const p = D.paragraph(64, 1185, v.texto, 32, 950, r.ink, { maxLines: 2, lineHeight: 42 });
      return `${D.background(1080, 1350, r.bg, r.light)}
        ${D.photo(0, 0, 1080, 1010, v.foto, { focus: v.enfoque, stroke: false, path: "M0,0 H1080 V940 L0,1010 Z" })}
        <path d="M0,1010 L1080,940 L1080,980 L0,1050 Z" fill="${CREAM}"/><path d="M0,1010 L1080,940" stroke="${INK}" stroke-width="6"/>
        ${headerChip(48, 48, 0.85)}
        <circle cx="${960 + 8}" cy="${960 + 8}" r="76" fill="${INK}"/><circle cx="960" cy="960" r="76" fill="${SUN}" stroke="${INK}" stroke-width="7"/>
        <text x="960" y="${960 + D.fit(num, 64, 120) * 0.36}" text-anchor="middle" class="cond" font-size="${D.fit(num, 64, 120)}" fill="${INK}">${D.esc(num)}</text>
        ${D.headline(64, 1125, t.lines[0], t.size, r.ink)}
        ${p.svg}
        ${v.desliza ? D.pillAuto(1016, 1250, 60, r.ink === CREAM ? SUN : INK, r.ink === CREAM ? INK : CREAM, "DESLIZA →", 24, { anchor: "end" }) : ""}
        <text x="64" y="1290" class="sans" font-weight="700" font-size="28" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "collage_4", name: "Collage de 4 fotos 1:1", group: "Fotos", w: 1080, h: 1080,
    fields: [foto("foto1", "Foto 1"), enfoque("enfoque1"), foto("foto2", "Foto 2"), enfoque("enfoque2"), foto("foto3", "Foto 3"), enfoque("enfoque3"), foto("foto4", "Foto 4"), enfoque("enfoque4"),
      f.receta, f.etiqueta(""), { key: "titulo", label: "Título", type: "text", default: "UN SÁBADO CUALQUIERA." }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const cells = [[64, 160], [550, 160], [64, 560], [550, 560]];
      const ph = cells.map(([x, y], i) => D.photo(x, y, 466, 380, v[`foto${i + 1}`], { focus: v[`enfoque${i + 1}`], shadow: true, rx: 22, strokeWidth: 6 })).join("");
      const t = fitLines(v.titulo, 80, 700, 1, 48);
      return `${D.background(1080, 1080, r.bg, r.light)}${D.corner(1080, ...r.corner, 150)}${D.header(110, 90, 0.95, r.ink)}
        ${ph}
        <circle cx="552" cy="562" r="88" fill="${INK}"/><circle cx="540" cy="550" r="88" fill="${CREAM}" stroke="${INK}" stroke-width="8"/>
        <use href="#bowl" x="487" y="495" width="106" height="110"/>
        ${v.etiqueta ? D.pillAuto(92, 186, 50, INK, CREAM, v.etiqueta, 20) : ""}
        ${D.headline(64, 1030, t.lines[0], t.size, r.ink)}
        <text x="1016" y="1030" text-anchor="end" class="sans" font-weight="700" font-size="26" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "foto_evento", name: "Foto + datos del evento 4:5", group: "Fotos", w: 1080, h: 1350,
    fields: [foto(), enfoque(), f.receta, f.etiqueta("ESTE SÁBADO"),
      { key: "dia", label: "Día (número)", type: "text", default: "18" }, { key: "mes", label: "Mes (abreviado)", type: "text", default: "OCT" },
      { key: "titulo", label: "Título", type: "text", default: "NOCHE DE ROL ABIERTA." },
      { key: "hora", label: "Hora", type: "text", default: SCHEDULE ? `Sábado · ${SCHEDULE}` : "[HORA]" },
      { key: "lugar", label: "Lugar", type: "text", default: PLACE },
      { key: "cta", label: "Botón", type: "text", default: "ESCRÍBENOS PARA RESERVAR" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const t = fitLines(v.titulo, 96, 950, 1, 56);
      const card = D.infoCard(64, 930, 952, [["reloj", v.hora], ["ubicacion", v.lugar]], 30);
      const date = v.dia ? `<g transform="translate(900,250) rotate(6)">
          <rect x="-96" y="-90" width="192" height="200" rx="22" fill="${INK}" transform="translate(10,10)"/>
          <rect x="-96" y="-90" width="192" height="200" rx="22" fill="${SUN}" stroke="${INK}" stroke-width="7"/>
          <rect x="-96" y="-90" width="192" height="56" rx="22" fill="${CORAL}" stroke="${INK}" stroke-width="7"/><rect x="-92" y="-50" width="184" height="14" fill="${CORAL}"/>
          <text x="0" y="-48" text-anchor="middle" class="sans" font-weight="700" font-size="${D.fit(v.mes, 30, 160, "sans", 700, 3)}" fill="${INK}" letter-spacing="3">${D.esc(String(v.mes).toUpperCase())}</text>
          <text x="0" y="88" text-anchor="middle" class="cond" font-size="${D.fit(v.dia, 120, 160)}" fill="${INK}">${D.esc(v.dia)}</text></g>` : "";
      return `${D.background(1080, 1350, r.bg, r.light)}${D.corner(1080, ...r.corner, 150)}${D.header(110, 96, 1, r.ink)}
        ${D.photo(64, 170, 952, 600, v.foto, { focus: v.enfoque, shadow: true })}
        ${v.etiqueta ? D.pillAuto(96, 200, 56, INK, CREAM, v.etiqueta, 22) : ""}
        ${date}
        ${D.headline(64, 880, t.lines[0], t.size, r.ink)}
        ${card.svg}
        ${v.cta ? D.pillAuto(64, 930 + card.height + 40, 76, r.ink === CREAM ? SUN : INK, r.ink === CREAM ? INK : CREAM, v.cta, 28, { shadow: r.ink !== CREAM }) : ""}
        <text x="1016" y="1305" text-anchor="end" class="sans" font-weight="700" font-size="28" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  add({
    id: "foto_pregunta", name: "Historia con pregunta (encuesta) 9:16", group: "Fotos", w: 1080, h: 1920,
    fields: [foto(), enfoque(), f.receta, f.etiqueta("PREGUNTA DE LA SEMANA"),
      { key: "pregunta", label: "Pregunta", type: "textarea", default: "¿Qué clase jugarías en tu primera partida?" },
      { key: "guia", label: "Mostrar recuadro para el sticker de Instagram", type: "checkbox", default: true }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const q = fitLines(v.pregunta, 104, 940, 3, 60);
      const qTop = 1040, lh = q.size * 0.95;
      const qsvg = q.lines.map((l, i) => D.headline(72, Math.round(qTop + q.size * 0.8 + i * lh), l, q.size, i === q.lines.length - 1 ? r.hl : r.ink, i === q.lines.length - 1 ? r.hlShadow : null, 8)).join("");
      const zy = Math.round(qTop + q.lines.length * lh + 70), zh = Math.max(200, 1560 - zy);
      return `${D.background(1080, 1920, r.bg, r.light)}${D.corner(1080, ...r.corner, 200)}
        ${D.photo(0, 0, 1080, 920, v.foto, { focus: v.enfoque, stroke: false, path: "M0,0 H1080 V840 L0,920 Z" })}
        <path d="M0,920 L1080,840 L1080,880 L0,960 Z" fill="${CREAM}"/><path d="M0,920 L1080,840" stroke="${INK}" stroke-width="6"/>
        ${headerChip(64, 250)}
        ${v.etiqueta ? D.pillAuto(72, 970, 56, r.ink === CREAM ? TEAL : INK, r.ink === CREAM ? INK : CREAM, v.etiqueta, 22) : ""}
        ${qsvg}
        ${v.guia ? `<rect x="140" y="${zy}" width="800" height="${zh}" rx="36" fill="${CREAM}" fill-opacity="0.35" stroke="${r.ink}" stroke-width="5" stroke-dasharray="20 14"/>
          <text x="540" y="${zy + zh / 2 + 10}" text-anchor="middle" class="sans" font-weight="700" font-size="26" fill="${r.ink}" letter-spacing="3" opacity="0.8">PON AQUÍ LA ENCUESTA</text>` : ""}
        ${D.sparkle(990, zy + 30, 70, r.accent)}${D.sparkle(90, zy + zh - 10, 40, CREAM)}
        ${D.pillAuto(540, 1600, 60, CREAM, INK, v.usuario, 26, { anchor: "middle", stroke: INK })}`;
    },
  });

  add({
    id: "cuenta_regresiva", name: "Cuenta regresiva (historia) 9:16", group: "Fotos", w: 1080, h: 1920,
    fields: [foto("foto", "Foto (opcional)"), enfoque(), f.receta, { key: "numero", label: "Número", type: "text", default: "3" },
      { key: "unidad", label: "Unidad", type: "text", default: "DÍAS" }, { key: "evento", label: "Para qué", type: "text", default: "PARA LA NOCHE DE ROL." },
      { key: "fecha", label: "Fecha", type: "text", default: "SÁBADO 18 DE OCTUBRE" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      const ns = Math.min(360, D.fit(v.numero, 360, 480));
      const nw = D.measure(v.numero, "cond", ns);
      const us = D.fit(String(v.unidad).toUpperCase(), 140, 1016 - (64 + nw + 40));
      const ev = fitLines(v.evento, 80, 950, 1, 48);
      const ph = v.foto ? D.photo(64, 400, 952, 560, v.foto, { focus: v.enfoque, shadow: true }) : D.illustration("mixto", 540, 700, 0.85);
      return `${D.background(1080, 1920, r.bg, r.light)}${D.corner(1080, ...r.corner, 220)}${D.header(110, 320, 1, r.ink)}
        ${ph}
        ${D.headline(64, 1110, "FALTAN", 96, r.ink)}
        ${D.headline(64, 1420, v.numero, ns, r.hl, r.hlShadow, 14)}
        ${D.headline(64 + nw + 40, 1420, String(v.unidad).toUpperCase(), us, r.ink)}
        ${D.headline(64, 1520, ev.lines[0], ev.size, r.ink)}
        ${v.fecha ? D.pillAuto(64, 1560, 70, r.ink === CREAM ? SUN : INK, r.ink === CREAM ? INK : CREAM, v.fecha, 28) : ""}
        ${D.sparkle(960, 1180, 90, r.accent)}${D.sparkle(880, 1290, 40, CREAM)}
        <text x="1016" y="1660" text-anchor="end" class="sans" font-weight="700" font-size="30" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  // ============================================================ VIDEO (más formatos)
  function separador(w, h, v) {
    const r = RECIPES[v.receta];
    const H = w < h;
    const num = String(v.numero || "");
    const t = fitLines(v.titulo, H ? 150 : 140, H ? 940 : 960, 2, 70);
    const cx = H ? 540 : 470, cy = H ? 720 : 540, R = H ? 210 : 230;
    const circle = num ? `<circle cx="${cx + 14}" cy="${cy + 14}" r="${R}" fill="${INK}"/><circle cx="${cx}" cy="${cy}" r="${R}" fill="${SUN}" stroke="${INK}" stroke-width="12"/>
      <text x="${cx}" y="${cy + D.fit(num, 230, R * 1.5) * 0.36}" text-anchor="middle" class="cond" font-size="${D.fit(num, 230, R * 1.5)}" fill="${INK}">${D.esc(num)}</text>` : "";
    const lh = t.size * 0.95;
    const tx = H ? 540 : (num ? 800 : 960), anchor = H || !num ? "middle" : "start";
    const ty0 = H ? 1120 : 540 - ((t.lines.length - 1) * lh) / 2 + t.size * 0.3 - (v.subtitulo ? 30 : 0);
    const title = t.lines.map((l, i) => D.headline(tx, Math.round(ty0 + i * lh), l, t.size, i === t.lines.length - 1 ? r.hl : r.ink, i === t.lines.length - 1 ? r.hlShadow : null, 10, anchor)).join("");
    const sy = Math.round(ty0 + (t.lines.length - 1) * lh + (H ? 90 : 80));
    const sub = v.subtitulo ? `<text x="${tx}" y="${sy}" text-anchor="${anchor}" class="sans" font-weight="700" font-size="${D.fit(v.subtitulo, 40, H ? 900 : 1000, "sans", 700)}" fill="${r.ink}">${D.esc(v.subtitulo)}</text>` : "";
    const band = H ? `<path d="M0,1640 L1080,1560 L1080,1600 L0,1680 Z" fill="${CREAM}"/><path d="M0,1680 L1080,1600 V1920 H0 Z" fill="${r.block}"/><path d="M0,1680 L1080,1600 V1920 H0 Z" fill="url(#dots)"/>`
      : `<path d="M0,1000 L1920,940 L1920,964 L0,1024 Z" fill="${CREAM}"/><path d="M0,1024 L1920,964 V1080 H0 Z" fill="${r.block}"/>`;
    return `${D.background(w, h, r.bg, r.light)}${D.corner(w, ...r.corner, H ? 260 : 220)}${band}
      ${circle}${title}${sub}
      ${D.sparkle(H ? 200 : 140, H ? 420 : 160, 80, r.accent)}${D.sparkle(H ? 900 : 1780, H ? 1000 : 820, 50, CREAM)}`;
  }
  const sepFields = [f.receta, { key: "numero", label: "Número (opcional)", type: "text", default: "01" },
    { key: "titulo", label: "Título", type: "text", default: "LA PARTIDA." }, { key: "subtitulo", label: "Subtítulo (opcional)", type: "text", default: "Donde todo empieza a rodar." }];
  add({ id: "separador_v", name: "Separador de capítulo 9:16", group: "Video", w: 1080, h: 1920, fields: sepFields, render: (v) => separador(1080, 1920, v) });
  add({ id: "separador_h", name: "Separador de capítulo 16:9", group: "Video", w: 1920, h: 1080, fields: sepFields, render: (v) => separador(1920, 1080, v) });

  add({
    id: "audiograma", name: "Clip de podcast (audiograma) 1:1", group: "Video", w: 1080, h: 1080,
    fields: [foto("foto", "Foto o portada"), enfoque(), { key: "receta", label: "Combinación de color", type: "select", options: RECIPE_OPTS, default: "podcast" },
      f.etiqueta("PODCAST · EP. 07"), { key: "cita", label: "Frase del clip", type: "textarea", default: "En la mesa aprendimos que cada voz cuenta una parte de la historia." },
      { key: "episodio", label: "Episodio", type: "text", default: "La taberna del dragón" }, f.usuario],
    render(v) {
      const r = RECIPES[v.receta];
      let size = 58, lines;
      for (;;) { lines = D.wrap(String(v.cita).toUpperCase(), size, 950, "cond", 800); if (lines.length <= 3 || size <= 36) break; size -= 3; }
      lines = lines.slice(0, 3);
      const y0 = 790, lh = size * 1.0;
      const quote = lines.map((l, i) => `<text x="64" y="${Math.round(y0 + size * 0.8 + i * lh)}" class="cond" font-size="${size}" fill="${r.ink}">${D.esc(l)}</text>`).join("");
      const ey = Math.round(y0 + size * 0.8 + (lines.length - 1) * lh + 58);
      return `${D.background(1080, 1080, r.bg, r.light)}${D.corner(1080, ...r.corner, 150)}${D.header(110, 90, 0.95, r.ink)}
        ${D.photo(64, 160, 952, 470, v.foto, { focus: v.enfoque, shadow: true })}
        ${v.etiqueta ? D.pillAuto(92, 186, 52, r.ink === CREAM ? SUN : INK, r.ink === CREAM ? INK : CREAM, v.etiqueta, 20) : ""}
        ${D.playBadge(950, 600, 62)}
        ${D.waveform(64, 860, 720, 80, r.ink === CREAM ? TEAL : INK)}
        ${quote}
        <text x="64" y="${ey}" class="sans" font-weight="700" font-size="${D.fit("— " + v.episodio, 30, 640, "sans", 700)}" fill="${r.ink === CREAM ? SUN : r.ink}">— ${D.esc(v.episodio)}</text>
        <text x="1016" y="1040" text-anchor="end" class="sans" font-weight="700" font-size="26" fill="${r.ink}">${D.esc(v.usuario)}</text>`;
    },
  });

  function introLogo(w, h, v) {
    const H = w < h;
    const cx = H ? 540 : 560, cy = H ? 760 : 540, R = H ? 270 : 280;
    const seal = `<circle cx="${cx + 18}" cy="${cy + 18}" r="${R}" fill="${INK}"/><circle cx="${cx}" cy="${cy}" r="${R}" fill="${CREAM}" stroke="${INK}" stroke-width="16"/>
      <use href="#bowl" x="${cx - R * 0.62}" y="${cy - R * 0.66}" width="${R * 1.24}" height="${R * 1.28}"/>`;
    const tx = H ? 540 : 940, a = H ? "middle" : "start", mw = H ? 980 : 920;
    const ns = D.fit("TAZÓN PARA DOS", H ? 170 : 160, mw);
    const ty = H ? 1250 : 500;
    const sub = String(v.sub || "").toUpperCase();
    return `${seal}
      ${D.headline(tx, ty, "TAZÓN PARA DOS", ns, INK, null, 0, a)}
      <text x="${tx}" y="${ty + 70}" text-anchor="${a}" class="sans" font-weight="700" font-size="${D.fit(sub, 40, mw, "sans", 700, 8)}" fill="${INK}" letter-spacing="8">${D.esc(sub)}</text>
      ${v.info ? D.pillAuto(tx, ty + 120, 88, INK, CREAM, v.info, 36, H ? { anchor: "middle" } : {}) : ""}`;
  }
  const introFields = [{ key: "sub", label: "Subtítulo", type: "text", default: "Espacio cultural · Engativá" }, { key: "info", label: "Información", type: "text", default: INFO }];
  add({ id: "intro_logo_v", name: "Logo para intro de video 9:16 (transparente)", group: "Video", w: 1080, h: 1920, transparent: true, fields: introFields, render: (v) => introLogo(1080, 1920, v) });
  add({ id: "intro_logo_h", name: "Logo para intro de video 16:9 (transparente)", group: "Video", w: 1920, h: 1080, transparent: true, fields: introFields, render: (v) => introLogo(1920, 1080, v) });

  window.TPDTemplates = templates;
})();
