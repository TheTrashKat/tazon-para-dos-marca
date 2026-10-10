// Render alternativo para Termux/Android: genera el SVG con Node y lo convierte
// a PNG con librsvg, sin depender de una ventana headless de Chromium.
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const vm = require("vm");

const [, , jobFile, baseDir, output, width, height] = process.argv;
if (!jobFile || !baseDir || !output) throw new Error("Faltan argumentos de render_node.js");

// Las primitivas miden texto usando canvas. Para el render sin navegador damos
// una medida estable; librsvg se encarga de dibujar el texto con las fuentes.
global.window = {};
global.document = {
  createElement: () => ({
    getContext: () => ({ measureText: (text) => ({ width: String(text ?? "").length * 50 }) }),
  }),
};
for (const file of ["brand-data.js", "primitives.js", "templates.js"]) {
  const source = fs.readFileSync(path.join(__dirname, "../editor", file), "utf8");
  vm.runInThisContext(source, { filename: file });
}

const job = JSON.parse(fs.readFileSync(jobFile, "utf8"));
const template = window.TPDTemplates.find((item) => item.id === job.template);
if (!template) throw new Error(`Plantilla desconocida: ${job.template}`);

const imageTypes = { ".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp", ".gif": "gif" };
function stage(value) {
  if (Array.isArray(value)) return value.map(stage);
  if (value && typeof value === "object") return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, stage(v)]));
  if (typeof value !== "string" || value.startsWith("data:") || value.startsWith("http")) return value;
  const ext = path.extname(value).toLowerCase();
  if (!imageTypes[ext]) return value;
  const source = path.isAbsolute(value) ? value : path.resolve(baseDir, value);
  if (!fs.existsSync(source)) throw new Error(`No existe la imagen: ${source}`);
  return `data:image/${imageTypes[ext]};base64,${fs.readFileSync(source).toString("base64")}`;
}

const fontFiles = [
  ["Barlow Condensed", 800, "BarlowCondensed-ExtraBold.ttf"],
  ["Barlow", 500, "Barlow-Medium.ttf"],
  ["Barlow", 600, "Barlow-SemiBold.ttf"],
  ["Barlow", 700, "Barlow-Bold.ttf"],
];
const fontCSS = fontFiles.map(([family, weight, file]) => {
  const data = fs.readFileSync(path.join(__dirname, "fonts", file)).toString("base64");
  return `@font-face{font-family:'${family}';font-weight:${weight};src:url(data:font/ttf;base64,${data}) format('truetype')}`;
}).join("\n");
const values = { ...Object.fromEntries(template.fields.map((field) => [field.key, field.default])), ...stage(job.values || {}) };
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${template.w} ${template.h}" width="${width || template.w}" height="${height || template.h}"><title>${window.TPDDraw.esc(template.name)} · Tazón para Dos</title>${window.TPDDraw.defs(fontCSS)}${template.render(values)}</svg>`;
const svgFile = `${output}.svg`;
fs.writeFileSync(svgFile, svg);
const result = spawnSync(process.env.RSVG_CONVERT || "rsvg-convert", ["-o", output, svgFile], { stdio: "inherit" });
fs.rmSync(svgFile, { force: true });
if (result.error) throw result.error;
if (result.status !== 0) process.exit(result.status || 1);
