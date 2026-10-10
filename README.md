# Tazón para Dos · Kit de marca

> **Jugar también es escuchar.** Espacio cultural LGBTI+ en Engativá, Bogotá: juegos de rol, juegos de mesa y podcast narrativo.

![Banner](plantillas/png/banner_web.png)

Este repositorio reúne la identidad visual de [Tazón para Dos](https://tazon-para-dos.online/): logos, colores, íconos, ilustraciones y plantillas para redes e impresión. Incluye también documentación para que una IA pueda crear piezas nuevas siguiendo las mismas reglas.

## ¿Por dónde empiezo?

| Si eres… | Abre |
|---|---|
| Una persona que quiere ver todo de un vistazo | [`index.html`](index.html) en el navegador |
| Una persona que va a diseñar algo | [`MANUAL_DE_MARCA.md`](MANUAL_DE_MARCA.md) |
| Una IA o alguien programando | [`AGENTS.md`](AGENTS.md), [`brand/tokens.json`](brand/tokens.json) y [`brand/brand.json`](brand/brand.json) |

## Contenido

```
brand/          tokens.json · tokens.css · brand.json (fuente de verdad)
assets/logo/    mascota, sello, logotipo horizontal y apilado (+ inversos)
assets/iconos/  18 íconos de línea 64 px + sprite.svg
assets/elementos/ d20, d6, carta, meeple, micrófono, destello
plantillas/     posts, historias, banner web y pancarta (SVG + png/)
aplicaciones/   hoja de stickers
referencias/    pancarta y logo originales
tools/          build.py (generador) · render.ps1 (exporta PNG) · fonts/ (Barlow, OFL)
```

## Paleta

| Tinta | Turquesa | Coral | Sol | Crema |
|---|---|---|---|---|
| `#28203B` | `#55C4BF` | `#EA6077` | `#F8CB67` | `#F7F2E8` |

## Regenerar

```bash
python -I tools/build.py                                   # SVG desde los tokens
powershell -ExecutionPolicy Bypass -File tools/render.ps1  # PNG (Edge/Chrome)
```

Requiere Python 3 con `fonttools` (`pip install fonttools`) para convertir a trazos los textos de los logos.

## Licencias

- Marca, mascota y textos: © Tazón para Dos. Todos los derechos reservados.
- Fuentes Barlow: SIL Open Font License (`tools/fonts/OFL.txt`).
