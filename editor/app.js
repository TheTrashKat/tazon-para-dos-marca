// Editor de plantillas de Tazón para Dos.
// Modo normal: formulario + vista previa + descarga PNG/SVG.
// Modo embed (?embed=1&t=<id>&d=<json base64url>): solo el SVG a tamaño final, para render automático (tools/render_editor.py).
(function () {
  const D = window.TPDDraw, TEMPLATES = window.TPDTemplates;
  const FONT_FILES = [
    ["Barlow Condensed", 800, "normal", "BarlowCondensed-ExtraBold.ttf"],
    ["Barlow", 500, "normal", "Barlow-Medium.ttf"],
    ["Barlow", 600, "normal", "Barlow-SemiBold.ttf"],
    ["Barlow", 700, "normal", "Barlow-Bold.ttf"],
    ["Barlow", 600, "italic", "Barlow-SemiBoldItalic.ttf"],
  ];
  const FONT_DIR = "../tools/fonts/";
  let embeddedFontCSS = "";       // @font-face con data URI (para exportar)
  const params = new URLSearchParams(location.search);
  const EMBED = params.get("embed") === "1";

  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem("tpd-editor:" + k)); } catch { return null; } },
    set(k, v) { try { localStorage.setItem("tpd-editor:" + k, JSON.stringify(v)); } catch { /* sin almacenamiento */ } },
    del(k) { try { localStorage.removeItem("tpd-editor:" + k); } catch { /* nada */ } },
  };

  async function loadFonts() {
    const css = [];
    await Promise.all(FONT_FILES.map(async ([family, weight, style, file]) => {
      try {
        const buf = await (await fetch(FONT_DIR + file)).arrayBuffer();
        const face = new FontFace(family, buf, { weight: String(weight), style });
        await face.load();
        document.fonts.add(face);
        let bin = "";
        const bytes = new Uint8Array(buf);
        for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
        css.push(`@font-face{font-family:'${family}';font-weight:${weight};font-style:${style};src:url(data:font/ttf;base64,${btoa(bin)}) format('truetype')}`);
      } catch (e) {
        console.warn("No se pudo cargar", file, e);
      }
    }));
    embeddedFontCSS = css.join("\n");
    return css.length === FONT_FILES.length;
  }

  const defaults = (t) => Object.fromEntries(t.fields.map((f) => [f.key, f.default]));
  const outSize = (t) => t.out || { w: t.w, h: t.h };

  function buildSVG(t, values, { embedFonts = false } = {}) {
    const o = outSize(t);
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${t.w} ${t.h}" width="${o.w}" height="${o.h}">` +
      `<title>${D.esc(t.name)} · Tazón para Dos</title>` + D.defs(embedFonts ? embeddedFontCSS : "") + t.render(values) + `</svg>`;
  }

  function download(name, blob) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  async function toPNG(t, values) {
    const o = outSize(t);
    const svg = buildSVG(t, values, { embedFonts: true });
    const url = URL.createObjectURL(new Blob([svg], { type: "image/svg+xml" }));
    try {
      const img = new Image();
      img.src = url;
      await img.decode();
      await new Promise((r) => setTimeout(r, 120)); // margen para que el SVG aplique las fuentes incrustadas
      const canvas = document.createElement("canvas");
      canvas.width = o.w; canvas.height = o.h;
      canvas.getContext("2d").drawImage(img, 0, 0, o.w, o.h);
      return await new Promise((res) => canvas.toBlob(res, "image/png"));
    } finally {
      URL.revokeObjectURL(url);
    }
  }

  const b64urlDecode = (s) => decodeURIComponent(escape(atob(s.replace(/-/g, "+").replace(/_/g, "/"))));

  // ---------------------------------------------------------------- modo embed
  async function runEmbed() {
    document.documentElement.classList.add("embed");
    await loadFonts();
    const t = TEMPLATES.find((x) => x.id === params.get("t")) || TEMPLATES[0];
    let data = {};
    try { if (params.get("d")) data = JSON.parse(b64urlDecode(params.get("d"))); } catch (e) { console.error("JSON inválido", e); }
    document.body.innerHTML = buildSVG(t, { ...defaults(t), ...data });
    document.body.dataset.ready = "1";
  }

  // ---------------------------------------------------------------- editor
  async function runEditor() {
    const $ = (s) => document.querySelector(s);
    const list = $("#templates"), form = $("#form"), preview = $("#preview"), status = $("#status");
    const ok = await loadFonts();
    if (!ok) status.textContent = "⚠️ No se pudieron cargar las fuentes. Abre el editor desde un servidor (no con doble clic) para que el PNG salga con la tipografía correcta.";

    let current = null, values = {};
    const groups = {};
    TEMPLATES.forEach((t) => (groups[t.group] = groups[t.group] || []).push(t));
    list.innerHTML = Object.entries(groups).map(([g, ts]) =>
      `<p class="group">${D.esc(g)}</p>` + ts.map((t) => `<button type="button" data-id="${t.id}"><span>${D.esc(t.name)}</span><small>${outSize(t).w}×${outSize(t).h}</small></button>`).join("")).join("");
    list.addEventListener("click", (e) => { const b = e.target.closest("button[data-id]"); if (b) select(b.dataset.id); });

    function renderForm() {
      form.innerHTML = current.fields.map((f) => {
        const id = "f-" + f.key, val = values[f.key];
        let input;
        if (f.type === "textarea") input = `<textarea id="${id}" data-key="${f.key}" rows="3">${D.esc(val)}</textarea>`;
        else if (f.type === "select") input = `<select id="${id}" data-key="${f.key}">${f.options.map(([v, l]) => `<option value="${D.esc(v)}"${v === val ? " selected" : ""}>${D.esc(l)}</option>`).join("")}</select>`;
        else if (f.type === "checkbox") return `<label class="check"><input type="checkbox" id="${id}" data-key="${f.key}"${val ? " checked" : ""}> ${D.esc(f.label)}</label>`;
        else input = `<input id="${id}" data-key="${f.key}" type="${f.type === "number" ? "number" : "text"}" value="${D.esc(val)}">`;
        return `<label for="${id}">${D.esc(f.label)}</label>${input}`;
      }).join("");
    }

    function renderPreview() {
      preview.innerHTML = buildSVG(current, values);
      const o = outSize(current);
      preview.style.aspectRatio = `${o.w} / ${o.h}`;
    }

    form.addEventListener("input", (e) => {
      const el = e.target, key = el.dataset.key;
      if (!key) return;
      values[key] = el.type === "checkbox" ? el.checked : el.type === "number" ? Number(el.value) : el.value;
      store.set(current.id, values);
      renderPreview();
    });

    function select(id) {
      current = TEMPLATES.find((t) => t.id === id) || TEMPLATES[0];
      values = { ...defaults(current), ...(store.get(current.id) || {}) };
      list.querySelectorAll("button").forEach((b) => b.classList.toggle("active", b.dataset.id === current.id));
      $("#title").textContent = current.name;
      $("#size").textContent = `${outSize(current).w} × ${outSize(current).h} px`;
      history.replaceState(null, "", "#" + current.id);
      renderForm();
      renderPreview();
    }

    const fileName = (ext) => `tazon-${current.id}-${new Date().toISOString().slice(0, 10)}.${ext}`;
    $("#png").addEventListener("click", async () => {
      status.textContent = "Generando PNG…";
      try { download(fileName("png"), await toPNG(current, values)); status.textContent = "✅ PNG descargado."; }
      catch (e) { console.error(e); status.textContent = "❌ No se pudo generar el PNG: " + e.message; }
    });
    $("#svg").addEventListener("click", () => {
      download(fileName("svg"), new Blob([buildSVG(current, values, { embedFonts: true })], { type: "image/svg+xml" }));
      status.textContent = "✅ SVG descargado (con fuentes incluidas).";
    });
    $("#reset").addEventListener("click", () => { store.del(current.id); select(current.id); status.textContent = "Textos restablecidos."; });
    $("#export").addEventListener("click", () => {
      download(`tazon-${current.id}.json`, new Blob([JSON.stringify({ template: current.id, values }, null, 2)], { type: "application/json" }));
    });
    $("#import").addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      try {
        const data = JSON.parse(await file.text());
        const t = TEMPLATES.find((x) => x.id === data.template);
        if (!t) throw new Error("plantilla desconocida: " + data.template);
        store.set(t.id, { ...defaults(t), ...data.values });
        select(t.id);
        status.textContent = "✅ Contenido importado.";
      } catch (err) { status.textContent = "❌ JSON inválido: " + err.message; }
      e.target.value = "";
    });

    select(location.hash.slice(1) || TEMPLATES[0].id);
  }

  window.TPDEditor = { buildSVG, toPNG, defaults, templates: TEMPLATES };
  (EMBED ? runEmbed : runEditor)();
})();
