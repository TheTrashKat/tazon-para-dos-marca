# Editor de plantillas · Tazón para Dos

Un editor web para hacer publicaciones sin saber diseño. Eliges la plantilla, cambias los textos y descargas el PNG.

## Cómo abrirlo

| Dónde | Enlace |
|---|---|
| Internet (GitHub Pages) | https://thetrashkat.github.io/tazon-para-dos-marca/editor/ |
| En tu computador | Ejecuta `python -m http.server 8765` en la carpeta del repositorio y abre http://127.0.0.1:8765/editor/ |

> ⚠️ No lo abras con doble clic (`file://`). Así el navegador no puede cargar las fuentes y el PNG saldría con otra tipografía.

## Cómo se usa

1. Elige una plantilla en la columna izquierda.
2. Cambia los textos en el formulario. La vista previa se actualiza al instante.
3. Pulsa **⬇ Descargar PNG**. La imagen sale al tamaño exacto para publicar.

- **Se guarda solo:** el editor recuerda lo que escribes en ese navegador, para cada plantilla.
- **Titulares que se ajustan:** si el texto es largo, el titular se achica o se parte en dos líneas.
- **Guardar JSON / Abrir JSON:** sirven para guardar el contenido de una publicación, compartirlo o reutilizarlo.
- **SVG:** descarga la pieza en vector, con las fuentes incluidas, para editarla en Inkscape o Illustrator.
- **Restablecer:** vuelve a los textos originales.

## Plantillas

| ID | Nombre | Tamaño final |
|---|---|---|
| `post_general` | Post general | 1080 × 1080 |
| `historia_general` | Historia general | 1080 × 1920 |
| `evento_vertical` | Evento semanal 4:5 | 1080 × 1350 |
| `evento_historia` | Evento semanal historia | 1080 × 1920 |
| `convocatoria_cuadrado` | Convocatoria 1:1 | 1080 × 1080 |
| `convocatoria_historia` | Convocatoria historia | 1080 × 1920 |
| `podcast_cuadrado` | Podcast 1:1 | 1080 × 1080 |
| `podcast_historia` | Podcast historia | 1080 × 1920 |
| `podcast_episodio` | Portada de episodio | 3000 × 3000 |
| `carrusel_portada` | Carrusel: portada | 1080 × 1350 |
| `carrusel_paso` | Carrusel: lámina de contenido | 1080 × 1350 |
| `destacada` | Portada de destacada | 1080 × 1920 |
| `foto_post` | Foto con marco 4:5 | 1080 × 1350 |
| `foto_cuadrado` | Foto con marco 1:1 | 1080 × 1080 |
| `foto_historia` | Foto historia | 1080 × 1920 |
| `foto_cita` | Foto con cita 4:5 | 1080 × 1350 |
| `collage` | Collage de 3 fotos | 1080 × 1350 |
| `foto_polaroid` | Una o dos fotos instantáneas con pie de foto | 1080 × 1350 |
| `foto_comparada` | Dos fotos comparadas (personaje / jugador, antes / después) | 1080 × 1350 |
| `foto_carrusel` | Lámina de carrusel con foto, número y «Desliza» | 1080 × 1350 |
| `collage_4` | Collage de 4 fotos con el sello al centro | 1080 × 1080 |
| `foto_evento` | Foto con fecha, hora, lugar y botón | 1080 × 1350 |
| `foto_pregunta` | Historia con pregunta y recuadro para la encuesta de Instagram | 1080 × 1920 |
| `cuenta_regresiva` | Historia «Faltan 3 días», con foto o ilustración | 1080 × 1920 |
| `video_portada` | Portada de Reel / video | 1080 × 1920 |
| `miniatura` | Miniatura de video | 1280 × 720 |
| `overlay_reel` | Capa de marca para Reel (transparente) | 1080 × 1920 |
| `tercio_inferior_h` / `_v` | Rótulo de nombre (transparente) | 1920 × 1080 / 1080 × 1920 |
| `texto_pantalla` | Texto en pantalla (transparente) | 1080 × 1920 |
| `tarjeta_final_v` / `_h` | Tarjeta final de video | 1080 × 1920 / 1920 × 1080 |
| `guia_zonas` | Guía de zonas seguras (transparente) | 1080 × 1920 |
| `marco_video` | Marco para video horizontal en Reel (transparente, con ventana 16:9) | 1080 × 1920 |
| `texto_pantalla_h` | Texto en pantalla 16:9 (transparente) | 1920 × 1080 |
| `overlay_video_h` | Capa de marca 16:9 (transparente) | 1920 × 1080 |
| `separador_v` / `separador_h` | Separador de capítulo para videos | 1080 × 1920 / 1920 × 1080 |
| `audiograma` | Clip de podcast: foto, onda de sonido y frase | 1080 × 1080 |

**Fotos:** pulsa *Elegir foto* y la foto se reduce sola a un máximo de 2400 px. En el JSON para `render_editor.py`, el campo de foto lleva la ruta de la imagen, relativa al archivo JSON. Hay un ejemplo en [`ejemplos/fotos_video.json`](ejemplos/fotos_video.json).

**Transparentes:** las plantillas de capas para video se ven sobre un fondo de cuadros y el PNG se descarga con transparencia.

Los campos de cada plantilla están en `fields`, dentro de [`templates.js`](templates.js). Para ver la lista de plantillas desde la terminal: `python -I tools/render_editor.py --list`.

## Generar imágenes sin abrir el navegador (IA y automatización)

Escribe el contenido en un JSON, que puede ser un objeto o una lista:

```json
[
  { "template": "evento_vertical",
    "values": { "linea1": "ESTE SÁBADO", "linea2": "JUGAMOS.", "dia": "Sábado 18 de octubre" },
    "output": "salida/evento-18-oct.png" }
]
```

y ejecuta:

```bash
python -I tools/render_editor.py editor/ejemplos/semana.json
```

- Los campos que omitas toman su valor por defecto.
- El script levanta un servidor temporal y usa Edge o Chrome en modo headless.
- Para probar, usa el ejemplo completo en [`ejemplos/semana.json`](ejemplos/semana.json).

También puedes ver una pieza directamente por URL (modo *embed*):
`editor/index.html?embed=1&t=<id>&d=<JSON en base64url>`

## Cómo está hecho

| Archivo | Qué contiene |
|---|---|
| `brand-data.js` | Colores, íconos, mascota, agenda y menú del podcast. **Se genera** con `python -I tools/build.py` desde `brand/*.json`, así que no lo edites a mano |
| `primitives.js` | Piezas de dibujo: cabecera, píldoras, d20, d6, carta, micrófono, globo, pasos, tarjeta de agenda, ilustraciones, recetas de color y medición real de texto (`fit`, `wrap`) |
| `templates.js` | Las plantillas: campos y función `render(valores)` que devuelve el SVG |
| `app.js` | La interfaz, la vista previa, el guardado y la exportación PNG/SVG (con fuentes incrustadas) |

**Para agregar una plantilla:**
1. Copia un bloque `add({...})` en `templates.js`.
2. Cambia `id`, `name`, `w`, `h` y `fields`.
3. Dibuja en `render` usando las funciones de `TPDDraw`.
4. Usa `D.fit()` en todo texto editable para que nunca se desborde.
5. Revisa con `render_editor.py` y mira el PNG.
