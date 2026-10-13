# AGENTS.md: Tazón para Dos brand kit

Instructions for AI agents (Claude, Codex, Cursor, etc.) that create or edit visual or written material for **Tazón para Dos**. Read this file first, then load the machine-readable sources below. The human-facing manual is `MANUAL_DE_MARCA.md` (Spanish). All copy you produce for the brand must be in **Spanish (Colombia)**.

## Sources of truth (load these, don't guess)

| File | What it holds |
|---|---|
| `brand/tokens.json` | Colors (hex + role), contrast ratios, typography, radii, strokes, shadows, dot pattern, icon spec |
| `brand/tokens.css` | Same tokens as CSS custom properties (`--ink`, `--teal`, `--coral`, `--sun`, `--cream`, `--paper`, `--muted`) |
| `brand/brand.json` | Identity, about text, taglines, manifesto, location, links, offerings, 3-step process, voice do/don't, CTAs, composition rules, color recipes per line, illustration objects, publication formats, merch |
| `tools/build.py` | Generator: SVG primitives (`header`, `pill`, `d20`, `d6`, `card`, `mic`, `waveform`, `bubble`, `steps`, `sparkle`, `text_path`) and all generated templates |
| `plantillas/*.svg` | Finished reference compositions. Copy the closest one instead of starting from scratch |

`brand.json` text marked "propuesta" is a suggestion, not a fact. Never invent schedules, prices, dates, episode names or partners. Ask the user, or leave a clearly marked placeholder such as `[FECHA]`.

## Hard rules

1. **Palette only:** ink `#28203B`, teal `#55C4BF`, coral `#EA6077`, sun `#F8CB67`, cream `#F7F2E8`. You may also use paper `#FFFDF8`, muted `#665F68` and the tints in `tokens.json`. No other hues, no gradients.
2. **Contrast:**
   - Body text, labels and buttons use ink on any brand color, or cream/sun/teal on ink.
   - Cream text on teal or coral is allowed **only** for display headlines (≥ 100 px at 1080 width), and only with an ink offset shadow. Draw the same text in ink at +8 to +12 px x/y behind it.
3. **Typography:**
   - Campaign pieces use Barlow Condensed 800 for headlines, UPPERCASE, and Barlow 500/600/700 for text.
   - Web UI uses Space Grotesk, DM Sans and DM Mono.
   - Labels are uppercase with letter-spacing of about 0.12em.
4. **Logo:** use the files in `assets/logo/`. Their text is already outlined. Brand name is always `TAZÓN PARA DOS`, with the accent. Do not recolor the mascot beyond ink/cream swaps, and do not stretch or rotate it.
5. **Illustration style:**
   - Flat fills, ink outline 6–7 px (scale proportionally), rounded joins.
   - Shadows are hard offsets only, with no blur.
   - Every illustration group has one hero object, 2–4 secondary objects, 2–4 four-point sparkles and an ink ellipse shadow at 22 % opacity.
6. **Layout:**
   - Split the piece into 2–3 color blocks with diagonals rising left to right (3–5°), and put a cream or sun stripe between blocks.
   - Put the dot pattern (22 px, r 1.6, ink at 10 %) on color blocks.
   - Put a sun + coral triangle in the top-right corner.
   - Put the header (seal + name + `ESPACIO CULTURAL · ENGATIVÁ`) at the top left.
7. **Icons:** 64×64 viewBox, `stroke-width="4"`, round caps/joins, `fill="none"`, `stroke="currentColor"`. Reuse `assets/iconos/` or the sprite (`#i-<name>`). New icons must follow the same spec. Add them to `ICONS` in `tools/build.py`.
8. **Safe areas:**
   - Stories (1080×1920): keep key text out of the top 250 px and bottom 250 px.
   - Posts: 64 px margin.
9. **Voice:**
   - Plural first person ("construimos") and informal "tú" toward the reader.
   - Warm, playful, community-minded. Inclusive language, and never assume the reader's gender.
   - Short headlines ending with a period.
   - No corporate or sales tone, no aggressive gamer slang, no exclamation-mark spam.

## Color recipe by content line

| Line | Background | Illustration block | Closing | Hero object |
|---|---|---|---|---|
| General / rol | teal | coral | ink | d20 (sun) |
| Podcast | ink | teal | (none) | microphone with sun/coral/teal waves |
| Convocatoria | sun | coral | ink | speech bubble "Mi historia trata sobre..." + teal d20 |
| Juegos de mesa | coral | teal | ink | d6 / meeple / card |

## Editable template editor (preferred for routine posts)

`editor/` is a web editor with 80 editable templates. **For routine content, prefer it over writing new SVG:**
- weekly event
- general post or story
- call for stories
- podcast promo
- episode cover
- carousel slide
- highlight cover
- photo posts and stories (single photo, collages, comparisons, event, poll, countdown)
- video covers, thumbnails, overlays, chapter cards and podcast clip stills

To produce images headlessly:
1. Write a JSON job list: `[{ "template": "<id>", "values": {...}, "output": "salida/x.png" }]`.
2. Run `python -I tools/render_editor.py jobs.json`.
3. Look at the PNGs.

To see the template ids, run `python -I tools/render_editor.py --list`. Field keys are in `editor/templates.js → fields`. Example jobs are in `editor/ejemplos/semana.json`, and full docs in `editor/README.md`.

Rules for the editor:
- **`editor/brand-data.js` is generated by `tools/build.py`. Never edit it by hand.**
- When adding a template, use `D.fit()` and `D.wrap()` (they measure real font metrics) for every user-editable text, and keep the layout rules above.
- Color combinations come from `RECIPES` in `primitives.js`: general, mesa, convocatoria, podcast.

## Template catalog (what to copy for each request)

| Request | Template(s) | Generator |
|---|---|---|
| "Invite people this Saturday" / weekly agenda | `evento_vertical`, `evento_historia` | `build_social()`, `info_card(AGENDA)`, `chips(ACTIVIDADES)` |
| Explain the process / educational post | `carrusel_01`…`carrusel_05` | `build_social()`, slides 2–4 loop over `brand.json → process` |
| General brand post / story | `post_cuadrado`, `historia` | static |
| Podcast promo | `podcast_cuadrado`, `podcast_historia` | `build_templates()` |
| Episode cover (Spotify 3000×3000) | `podcast_episodio_plantilla` | `episodio(slug, "MENÚ · <SECCIÓN>", title, bg, accent)` |
| Show cover | `podcast_portada` | `build_social()` |
| Call for stories | `convocatoria_cuadrado`, `convocatoria_historia` | `build_templates()` |
| Profile picture | `perfil` | `build_social()` |
| Instagram highlight covers | `destacada_*` | `build_social()` loop: (slug, label, bg, icon) |
| Website hero | `banner_web` | static |
| Printed roll-up 80×180 cm | `pancarta_80x180` | static |
| Stickers / merch | `aplicaciones/stickers`, `aplicaciones/merch_mockups` | `build_stickers()`, `build_print()` |
| Business card 85×55 mm | `aplicaciones/tarjeta_frente`, `tarjeta_reverso` | `build_print()` |
| Door sign with opening hours (A4) | `aplicaciones/letrero_horario_a4` | `build_print()` |
| Character sheet (A4, any RPG system) | `aplicaciones/ficha_personaje_a4` | `build_print()` + `field()` |
| Workshop certificate (A4 landscape) | `aplicaciones/certificado_taller` | `build_print()` |
| Email signature | `aplicaciones/firma_correo.html` | hand-written HTML (tables + hosted PNG, no SVG) |
| Scene divider inside a text (story, long post) | `assets/divisores/<modo>/<name>.svg` (modo: claro, noche, pergamino), CSS in `assets/divisores/divisores-<modo>.css`, gallery `divisores.html` | `tools/divisores.py` (also writes the Tinieblas kit and `D:\herramientas\pdf-historias\marca\divisores-claro.css`) |
| Print-ready PDF / logo PNG / favicon | `impresion/*.pdf`, `assets/logo/png/`, `favicon.ico` | `python -I tools/export.py` (add new print pieces to `PRINT`) |

Useful helpers in `tools/build.py`:
- `icon(name, cx, cy, size)` draws a line icon from `ICONS`.
- `headline_shadow(x, y, text, size, fg, shadow, off)` draws a display headline with its comic shadow.
- `wrap(text, maxchars)` breaks text into lines. For Barlow Condensed 800, average glyph width is about 0.44 × font-size.
- `background(w, h, color)` and `corner(w, c1, c2)` draw the background and the corner triangles.

## Podcast sub-brand

`brand.json → podcast` describes the show, a role-playing podcast that uses **cooking language**. Episodes are "platillos" (dishes) on a "menú". The menu sections and their colors are:
- **Mesa Principal** (long campaigns): coral
- **Entremeses** (lighter stories): teal
- **Dessert**: sun

When writing podcast copy, use the food vocabulary in `podcast.vocabulary` ("cada episodio es un platillo distinto"). Episode covers use the episode's section color as background, with the d20 on a cream plate.

## Workflow for a new piece

1. Pick a format from `brand.json → formats`, then copy the closest template from `plantillas/`. Alternatively, add a new function in `tools/build.py` that reuses the primitives.
2. Write copy from `brand.json` (taglines, offerings, process, ctas). Only write new copy if it follows `voice`.
3. Build: `python -I tools/build.py`
4. Render PNGs (Windows). For print pieces, also run `python -I tools/export.py` to produce PDFs at real physical size with embedded fonts: `powershell -ExecutionPolicy Bypass -File tools/render.ps1 [-Only <name>]`. The script uses Edge or Chrome headless.
5. **Look at the PNG** and check for overlaps, clipped text (Barlow Condensed is narrow, so fallback fonts overflow), and contrast.
6. Add the new files to `index.html` and, if they introduce a new format, to `brand.json → formats`.

## Photo & video

**Photos:** use the editor templates:
- Single photo: `foto_post`, `foto_cuadrado`, `foto_historia`, `foto_cita`, `foto_polaroid`, `foto_completa` (full bleed with a color band), `foto_circulo` (round frame).
- Several photos: `collage` (3), `collage_4` (4), `foto_comparada` (2, side by side), `foto_carrusel` (one slide per photo, with `numero`/`total`), `foto_tira` (3, photo-booth strip story), `foto_mosaico` (6).
- Every photo template has `invertir: true` ("Invertir colores"): the color background turns ink and that color moves to the highlighted headline and photo shadows; the ink recipe (podcast) turns cream. It uses `D.invert()` in `primitives.js`, so keep using `rec(v)` (not `RECIPES[v.receta]`) in photo templates and declare `variants: INV_VARIANTS`.
- Photo + call to action: `foto_evento` (date, time, place, button), `foto_pregunta` (story with a box for the Instagram poll sticker), `cuenta_regresiva` (countdown story).

The gallery in `index.html → Fotos` shows `plantillas/fotos/<id>.jpg` and `<id>_invertida.jpg` (rendered with the face-free `editor/ejemplos/fotos/tablero.jpg`). When you add a photo template, render both and add them there.

Image fields take a local path in `render_editor.py` jobs (relative to the JSON file), and `enfoque` sets the crop focus. Never tint the photo; brand color goes around it.

**Video kit:** lives in `video/` and is regenerated with `python -I tools/video.py` (needs ffmpeg and the `logotipo-apilado.png` from `tools/export.py`).
- Intro: 2.5 s. Outro: 4 s.
- Transparent overlays: `overlay_reel`, `tercio_inferior_h/_v`, `texto_pantalla`, `guia_zonas`. They export with alpha.
- Chapter cards: `separador_v` / `separador_h`. Podcast clip still: `audiograma`.
- Covers: `video_portada` and `miniatura`.

**Automatic editing:** to turn raw clips into a branded video, write a *guion* JSON (see `brand.json → video.montaje` and `video/ejemplos/`) and run `python -I tools/montaje.py guion.json`.
- Formats: `9x16-marco` (horizontal clips framed in a Reel), `9x16` (full-screen vertical) and `16x9`.
- Segments can be clips (`clip`), still photos with a slow pan (`foto`) or chapter cards (`separador`).
- Branding style: `"capa": {"estilo": "clasico" | "banda" | "stickers" | "marco" | "editorial" | "zine"}` (9x16) or `clasico | banda` (16x9). `marco`, `editorial` and `zine` put the clip in a window; with `editorial`/`zine` each segment's `texto` becomes the headline (`titulo2`) and the matching intro/outro is used. Prefer `editorial` or `zine` (the official lines). `tiktok` = full-screen clips with a slow punch-in, 1–3-word subtitles with the active word in sun, an optional `gancho` (hook) in the first 1.8 s and the outro from `capa.linea`; use 2–3 s segments and `"intro": false`. Subtitle look: `capa.subtitulos` = karaoke | caja | recorte | pop | editorial. List videos: per segment `numero` + `titulo` (shown after the hook).
- Templates with style options declare `variants` so `tools/validar.py` checks every variant (normal and stress).
- Horizontal clips cropped to 9:16 lose the sides: always check frames and set `"encuadre"` (izquierda | centro | derecha | 0–1) per segment so people stay in frame.
- Keep segments 2.5–5 s and Reels 15–30 s.
- One short on-screen text per segment, in brand voice.
- Inspect frames of the result (for example with `ffmpeg -ss <t> -frames:v 1`) before delivering.
- Never put real people's names in lower thirds without the user confirming consent.

Follow `brand.json → video`:
- Safe zones in 9:16: top 250 px, bottom 420 px and the right button strip.
- On-screen text: max 2 lines, 60–72 px at 1080 width, cream on ink or ink on sun.
- Branding must read on a phone: never shrink the header chip, info pill or @usuario below the sizes in `brand.json → video.branding_scale`.
- Simple cuts.
- The kit's MP4s have no audio.

## Photography

Follow `brand.json → photography`. Photos should show real people playing, hands on the table, dice, cards and microphones, in warm natural light. Put them in rounded frames with an ink outline.

**Consent is mandatory.** This is an LGBTI+ safe space, so never publish identifiable faces or names without explicit permission. Offer a hands-only option.

## Validation (mandatory, two passes)

Every new or changed editor template must pass both before it is committed:
1. **Automatic:** `python -I tools/validar.py` → must report **0 errors**. It renders each template with defaults and with long "stress" texts and checks, with real fonts: text outside the canvas, overlapping or touching texts, pills covering text, `undefined`/`NaN`; warnings for Instagram UI zones (stories: top 250/bottom 250; Reels: top 250, bottom 420, right button strip x>940 between y 900–1500), text < 18 px and text hugging the edge.
2. **Visual:** `python -I tools/validar.py --hojas` → open every sheet in `salida/validacion/` and look at both columns (normal | estrés). Fix anything that looks wrong even if the script passed, and if it is a new class of problem, add a check to `editor/validar.js`.

Research-based rules enforced by the validator (sources in `brand.json → editor.validation.research_rules`): text ≥ 22 px at 1080 width (dates, times and places ≥ 32 px), Reel covers keep text and logo inside the centered square y 420–1500 (mark them with `cover: true`), one headline + at most one subhead per piece.

For generated videos, also extract a few frames and look at them before delivering.

## Web generator (`D:\generador-web`)

A separate repo with a local panel (`iniciar.bat`, http://127.0.0.1:8765) that lets people make images and videos from their photos without touching this repo. It does not import the kit's code. Instead it runs the kit's tools and reads some of its files:
- It runs `render_editor.py` (both `--list` and job files), `montaje.py`, `validar.py` and `video.py`.
- It reads `SIZE`, `CAPA`, `VENTANA`, `TEXTO_EN_MARCO` and `TONEMAP` from `montaje.py` with `ast.literal_eval`, so they must stay top-level literals.
- It uses `window.TPDTemplates` and the editor's `?embed=1&t=&d=` mode.

`tools/generador.py` checks this contract, and `validar.py` runs it too. If you change any of these on purpose, update `tools/generador.py` and the panel together. The panel shows the result of the check in a banner (`/api/estado`).

## Repository workflow

- **Commits:** the user wants every change committed and pushed. `tools/autocommit.py` does it (commit message built from the changed folders, skips files over 90 MB) and is meant to run from a Claude Code `Stop` hook. If the hook is not active, commit and push yourself when a piece of work is done.
- **Never commit the user's raw photos or clips** (they contain identifiable people). Use paths outside the repo in jobs and guiones. Generated output goes to `salida/`, which is git-ignored. Only the neutral example photos in `editor/ejemplos/fotos/` belong in the repo.
- **Before committing generated media,** check that it opens (for example `ffprobe` on MP4s). An interrupted `tools/video.py` run once left broken intro/outro files.

## Gotchas

- **Fonts in standalone SVGs:** templates load Barlow through a CSS `@import`. That works when the SVG is opened directly or rendered headless, but **not** when the SVG is used as `<img src>`, where fonts fall back and text overflows. For logos or anything embedded as an image, outline text with `text_path()` in `build.py` (fonts are in `tools/fonts/`).
- **Static templates:** `banner_web`, `pancarta_80x180`, `post_cuadrado` and `historia` were hand-drawn. `build.py` only normalizes their colors (the `LEGACY` map), so edit those SVGs directly.
- **Generated templates:** `podcast_*` and `convocatoria_*` are generated. Edit `build.py`, not the SVG, or your changes will be overwritten.
- **Encoding:** when editing SVGs from PowerShell, write UTF-8 without BOM or the accents (Á, É, Í, Ó, Ú, Ñ, ¿) break.
- **Spotify:** the pieces mention Spotify in text only. Use the official Spotify badge only if the user asks, following Spotify's brand guidelines.
