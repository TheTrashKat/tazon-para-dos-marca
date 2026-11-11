# Plantillas de publicación de partidas

Plantillas genéricas para anunciar **mesas de rol** y **noches de juegos de mesa** en redes. No dependen de ningún juego concreto: el nombre de la aventura o del juego es un campo libre.

Todas usan la tipografía de marca (Barlow Condensed ExtraBold para titulares, Barlow para texto), titulares en mayúsculas y la dirección de TagTabu.

## Familias

| Familia | Post 4:5 | Historia 9:16 | Idea |
|---|---|---|---|
| Ficha | `partida_ficha_post` | `partida_ficha_historia` | Hoja de personaje: foto, celdas de fecha, hora y dirección |
| Boleto | `partida_boleto_post` | `partida_boleto_historia` | Boleto de entrada con perforación; el talón lleva el día |
| Afiche | `partida_afiche_post` | `partida_afiche_historia` | Foto en arco, titular grande y datos en filas |

Las plantillas originales `partida_post` y `partida_historia` siguen disponibles (las usa el publicador).

## Campos

| Campo | Qué es | Ejemplo |
|---|---|---|
| `tipo` | Tipo de mesa: `rol` (Mesa de rol) o `mesa` (Juegos de mesa). Cambia el rótulo de la ficha y del boleto | `rol` |
| `titulo` | Titular, en mayúsculas en la pieza. Sin límite de juego: nombre de aventura o frase | `TU MESA TE ESPERA.` |
| `foto` | Ruta a la foto. Opcional: sin foto aparece un d20 o el espacio vacío | `fotos/mesa.jpg` |
| `enfoque` | Encuadre de la foto: `arriba`, `centro` o `abajo` | `centro` |
| `dia`, `mes` | Día y mes de la hoja de calendario | `14`, `NOV` |
| `fecha`, `hora` | Texto de fecha y horario | `Sábado 14 de noviembre`, `11:00 a. m. – 9:00 p. m.` |
| `direccion` | Dirección que aparece en su propia fila | `Transversal 76 B No. 81 F – 08, Engativá` |
| `lugar` | Nombre del espacio (si no hay dirección, se usa en la fila de ubicación) | `Tazón para Dos · Espacio cultural` |
| `nivel`, `cupos` | Chips de la pieza | `PARA PRINCIPIANTES`, `5 CUPOS` |
| `sello` | Sello opcional en la esquina (`ÚLTIMOS CUPOS`, `NUEVA CAMPAÑA`…) | `ÚLTIMOS CUPOS` |
| `cta` | Botón | `VEN A JUGAR CON NOSOTROS` |
| `usuario` | Usuario en redes | `@tazonparados` |
| `receta` | Combinación de color: `general`, `mesa`, `convocatoria`, `podcast` | `mesa` |
| `invertir` | Modo oscuro (invierte colores) | `false` |
| `logo` | Muestra el sello de la mascota (opcional, apagado por defecto) | `false` |

Cada plantilla también admite las variantes de color (`invertir`) y sin foto.

## Cómo generar las piezas

1. Escribe un trabajo JSON (ejemplo: `editor/ejemplos/partidas_redes.json`). Las rutas de foto son relativas al archivo JSON.
2. Ejecuta: `python -I tools/render_editor.py editor/ejemplos/partidas_redes.json`
3. Revisa los PNG en `salida/`.
4. Valida la plantilla: `python -I tools/validar.py` (debe dar 0 errores).

## Reglas de diseño

- Titulares en Barlow Condensed ExtraBold, en mayúsculas.
- Fechas, horas y direcciones con al menos 32 px en el ancho de 1080.
- Historia: deja libres los 250 px superiores e inferiores (zona de la interfaz de Instagram).
- Logo: solo el sello de la mascota (`logo: true`), en una esquina libre. No repite el nombre de la marca.
- Fotos de personas: solo con permiso de las personas que aparecen.
- Modo oscuro: `invertir: true`. Para juegos de Mundo de Tinieblas (vampiro, hombre lobo) usar la paleta Tinieblas de `brand/tinieblas/`.

## Estado

- Familias en el editor: sí, con validación de 0 errores.
- El publicador de partidas (`D:\tazon-partidas`) usa `partida_post` y `partida_historia`. Para usar estas familias habría que cambiar los ids en el publicador y añadir el campo `tipo` al formulario. Pendiente.
