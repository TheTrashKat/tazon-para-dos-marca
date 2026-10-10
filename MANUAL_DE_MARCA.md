# Tazón para Dos · Manual de marca

> **Jugar también es escuchar.**
> Espacio cultural · Engativá, Bogotá

Este manual reúne todo lo necesario para que cualquier persona del colectivo pueda hacer piezas que se vean y suenen a Tazón para Dos: un afiche, un post, una historia o un sticker. Para verlo todo de un vistazo, abre [`index.html`](index.html) en el navegador.

---

## 1. Quiénes somos

Tazón para Dos es una **agrupación cultural LGBTI+** que crea espacios seguros para imaginar en colectivo. Usamos el **juego de rol**, la **narración oral** y la **producción sonora** para transformar recuerdos, preguntas y realidades en relatos compartidos.

| | |
|---|---|
| **Lema** | Jugar también es escuchar. |
| **Promesa** | Un espacio seguro para crear en comunidad. |
| **Qué hacemos** | Juegos de rol · Juegos de mesa · Podcast narrativo |
| **Pilares** | Comunidad · Oralidad · Memoria local · Podcast |
| **Dónde** | Tv. 76b #81f-08, Engativá, Bogotá |
| **Horario** | Sábados · 11:00 a.m. – 9:00 p.m. |
| **Web** | [tazon-para-dos.online](https://tazon-para-dos.online/) |
| **Redes** | [@tazonparados](https://www.instagram.com/tazonparados/) · [Facebook](https://www.facebook.com/61577811222885/) · [Spotify](https://open.spotify.com/show/2o68dbyhq4YvyRE3lmVXWY) |

### Manifiesto (del sitio)

> El juego es el puente. Juntamos escritura, interpretación, escucha y tecnología para que las ideas de la comunidad encuentren su propia voz.
>
> Nos reunimos para inventar mundos y terminamos encontrando nuevas formas de habitar el nuestro.
>
> Desde Engativá, hacemos de cada mesa un pequeño mundo posible: uno donde escuchar también es una forma de crear.

---

## 2. Logotipo

La **mascota** es un tazón de arroz sonriente con vapor saliendo: dos ojos, una sonrisa y una base. Representa compartir la mesa entre dos (o más).

| Versión | Archivo | Cuándo usarla |
|---|---|---|
| Logotipo horizontal | `assets/logo/logotipo-horizontal.svg` | Cabeceras, web, firmas de correo |
| Horizontal inverso | `assets/logo/logotipo-horizontal-inverso.svg` | Sobre fondo tinta |
| Logotipo apilado | `assets/logo/logotipo-apilado.svg` | Piezas cuadradas, merch, portadas |
| Sello | `assets/logo/sello.svg` | Avatar de redes, favicon, stickers |
| Sello inverso | `assets/logo/sello-inverso.svg` | Sobre fondo tinta |
| Mascota sola | `assets/logo/mascota.svg` | Ilustraciones, detalles, patrones |

**Reglas**
- El nombre siempre va en **mayúsculas**: TAZÓN PARA DOS (con tilde).
- Los textos del logotipo ya están en **trazos**, así que no necesitas instalar fuentes.
- Deja alrededor del sello un margen libre de al menos **la mitad de su radio**.
- Tamaño mínimo: sello de 24 px en pantalla o 10 mm impreso.
- ❌ No deformes, rotes ni cambies los colores de la mascota fuera de tinta/crema.
- ❌ No pongas el sello crema sobre fondo crema sin el contorno tinta.

---

## 3. Paleta de colores

Son los colores oficiales del sitio web (variables CSS). Las pancartas antiguas usaban versiones aproximadas; ya están todas normalizadas a estos valores.

| Color | HEX | RGB | Variable | Uso |
|---|---|---|---|---|
| **Tinta** | `#28203B` | 40 32 59 | `--ink` | Texto, contornos, fondos oscuros, sombras |
| **Turquesa** | `#55C4BF` | 85 196 191 | `--teal` | Fondo protagonista, rol, ondas |
| **Coral** | `#EA6077` | 234 96 119 | `--coral` | Bloque de ilustración, juegos de mesa |
| **Sol** | `#F8CB67` | 248 203 103 | `--sun` | Dados, destellos, CTA, convocatorias |
| **Crema** | `#F7F2E8` | 247 242 232 | `--cream` | Superficies claras, franjas, titulares |
| Papel | `#FFFDF8` | 255 253 248 | `--paper` | Fondo del sitio web |
| Gris cálido | `#665F68` | 102 95 104 | `--muted` | Texto secundario sobre claro |

**Proporción sugerida por pieza:** 45 % color de fondo · 25 % bloque de ilustración · 20 % tinta · 10 % acentos.

### Contraste (accesibilidad)

| Combinación | Contraste | ¿Texto normal? |
|---|---|---|
| Tinta sobre crema / papel | 13.8 / 15.2 | ✅ Sí |
| Tinta sobre sol | 10.1 | ✅ Sí |
| Tinta sobre turquesa | 7.4 | ✅ Sí |
| Tinta sobre coral | 4.7 | ✅ Sí |
| Crema / sol / turquesa sobre tinta | 13.8 / 10.1 / 7.4 | ✅ Sí |
| Crema sobre turquesa | 1.9 | ❌ Solo titular grande **con sombra tinta** |
| Crema sobre coral | 2.9 | ❌ Solo titular grande **con sombra tinta** |
| Coral / sol sobre crema | 2.9 / 1.4 | ❌ No usar para texto |

**Regla de oro:** el texto va en **tinta sobre color**, o en **color claro sobre tinta**.

---

## 4. Tipografía

| Medio | Rol | Fuente | Detalles |
|---|---|---|---|
| Campaña (afiches, redes) | Titulares | **Barlow Condensed ExtraBold (800)** | MAYÚSCULAS, interlineado 0.95 |
| Campaña | Texto, botones, etiquetas | **Barlow** 500/600/700 | Etiquetas en mayúscula con tracking amplio |
| Sitio web | Titulares | **Space Grotesk** | |
| Sitio web | Texto corrido | **DM Sans** | |
| Sitio web | Eyebrows y números | **DM Mono** | |

Todas son gratuitas en [Google Fonts](https://fonts.google.com). Las de Barlow también están en `tools/fonts/` (licencia OFL).

**Jerarquía en un post de 1080 px:** titular 124–178 px · subtítulo 62 px · texto 30 px · etiqueta 20 px.

---

## 5. Iconografía

Los íconos son de **línea**, como los del sitio web: grilla de 64 × 64, trazo de 4 px, puntas y uniones redondeadas y sin relleno. Usan `currentColor`, así que toman el color del texto.

| Ícono | Archivo | Significado |
|---|---|---|
| dado | `dado.svg` | Juegos de mesa |
| d20 | `d20.svg` | Rol |
| meeple | `meeple.svg` | Jugadores |
| carta | `carta.svg` | Cartas |
| idea | `idea.svg` | Postula tu idea |
| micrófono | `microfono.svg` | Podcast |
| audífonos | `audifonos.svg` | Escuchar |
| onda | `onda.svg` | Sonido |
| play | `play.svg` | Reproducir |
| historia | `historia.svg` | Historias, oralidad |
| libro | `libro.svg` | Narración |
| comunidad | `comunidad.svg` | Comunidad |
| corazón | `corazon.svg` | Espacio seguro |
| ubicación | `ubicacion.svg` | Engativá |
| calendario | `calendario.svg` | Fechas |
| reloj | `reloj.svg` | Horario |
| votación | `votacion.svg` | Votación abierta |
| destello | `destello.svg` | Acento decorativo |
| tazón | `tazon.svg` | Marca |

En la web puedes usar el sprite: `<svg><use href="assets/iconos/sprite.svg#i-microfono"/></svg>`.

---

## 6. Estilo gráfico: "Pop y cómic"

La identidad mezcla la energía del cómic con la calidez de una mesa de juego.

**Ingredientes**
1. **Bloques diagonales.** La pieza se divide en 2 o 3 bloques de color separados por diagonales que suben hacia la derecha (unos 3–5°), con una franja crema o sol entre bloques.
2. **Patrón de puntos.** Encima de los bloques de color va una trama de puntos de 22 px, en tinta al 10 %.
3. **Esquina de color.** Arriba a la derecha va un triángulo sol con otro coral más pequeño.
4. **Ilustración plana con contorno tinta grueso.** Contorno de 6–7 px, sin degradados.
5. **Sombra cómic.** Va desplazada (8–12 px) y sin desenfoque. Se usa en titulares claros y botones.
6. **Destellos de 4 puntas.** Pon entre 2 y 4 por pieza, en sol, crema o tinta.

**Objetos ilustrados** (en `assets/elementos/`)
- **d20** (sol): el objeto principal para **rol**.
- **Micrófono con ondas**: el objeto principal para **podcast**.
- **Carta, d6 y meeple**: objetos secundarios para **juegos de mesa**.
- **Dos manos** de distinto color que se acercan: la idea de "para dos" (ver la pancarta).
- **Globo de diálogo** con "Mi historia trata sobre...": para **convocatorias**.
- **Forma de onda**: para piezas de **audio**.

Pon siempre un objeto principal con 2 a 4 secundarios y una sombra elíptica tinta al 22 % debajo del grupo.

---

## 7. Fórmulas de color por línea

| Línea | Fondo | Bloque de ilustración | Cierre | Titular |
|---|---|---|---|---|
| General / rol | Turquesa | Coral | Tinta | Tinta + **crema con sombra** |
| Podcast | Tinta | Turquesa | — | Crema + **sol con sombra turquesa** |
| Convocatoria | Sol | Coral | Tinta | Tinta + **crema con sombra** |
| Juegos de mesa | Coral | Turquesa | Tinta | Tinta + **crema con sombra** |

---

## 8. Voz y tono

Hablamos como **amistades que te invitan a la mesa**, no como una empresa.

| Sí ✅ | No ❌ |
|---|---|
| "Ven a jugar. Quédate a compartir." | "¡¡Participa YA en nuestro evento!!" |
| "¿Qué mundo quieres traer a la mesa?" | "Inscríbete para acceder al servicio" |
| Verbos como jugar, imaginar, escuchar, narrar o crear | Jerga competitiva ("dominar", "aplastar") |
| Primera persona plural y tuteo | Tono corporativo o de venta |
| Lenguaje inclusivo ("personas que se reúnen") | Suponer el género de quien lee |
| Nombrar Engativá y Bogotá | Prometer fechas o precios sin confirmar |

**Titulares probados**
- Jugar también es escuchar.
- Tu historia empieza aquí.
- Del juego al aire.
- ¿Qué mundo quieres traer a la mesa?
- La mesa es un territorio.
- Ven a jugar. Quédate a compartir.

**Llamados a la acción:** Quiero participar · Postula tu idea · Escúchalo en Spotify · Enviar historia · Cómo llegar.

---

## 9. Formatos de publicación

| Formato | Tamaño (px) | Zona segura | Plantillas |
|---|---|---|---|
| Post cuadrado | 1080 × 1080 | 64 px de margen | `post_cuadrado`, `podcast_cuadrado`, `convocatoria_cuadrado` |
| Post vertical 4:5 | 1080 × 1350 | 64 px | `evento_vertical`, `carrusel_01`…`05` |
| Historia / estado | 1080 × 1920 | 250 px arriba y abajo libres de texto clave | `historia`, `podcast_historia`, `convocatoria_historia` |
| Banner web | 1920 × 720 | 86 px | `banner_web` |
| Pancarta roll-up | 80 × 180 cm | 4 cm | `pancarta_80x180` |
| Portada podcast y episodio | 3000 × 3000 | 100 px | `podcast_portada`, `podcast_episodio_plantilla` |
| Foto de perfil | 1080 × 1080 | círculo central | `perfil` |
| Destacadas | 1080 × 1920 | círculo central | `destacada_*` |

Cada plantilla está en `plantillas/` (SVG editable) y en `plantillas/png/` (lista para subir).

**Estructura de una publicación**
1. **Cabecera:** sello y nombre arriba a la izquierda.
2. **Etiqueta (opcional):** píldora con la línea, por ejemplo "PODCAST NARRATIVO" o "CONVOCATORIA ABIERTA".
3. **Titular:** 2 o 3 líneas, con la última destacada.
4. **Ilustración:** un objeto principal y varios secundarios.
5. **Cierre:** el llamado a la acción y @tazonparados o la web.

**Texto para acompañar el post (caption)**
- **Primera línea:** el titular de la pieza.
- **Después:** 2 o 3 frases con el qué, el cuándo y el dónde.
- **Al final:** el llamado a la acción y el enlace en la biografía.
- **Hashtags sugeridos** *(propuesta)*: #TazónParaDos #Engativá #JuegosDeRol #JuegosDeMesa #PodcastNarrativo #CulturaLGBTI #Bogotá

---

### Kit de redes para el día a día

| Pieza | Archivos | Para qué |
|---|---|---|
| **Evento semanal** | `evento_vertical` (4:5), `evento_historia` | Invitar cada sábado: día, horario, dirección y actividades |
| **Carrusel "De la idea al aire"** | `carrusel_01` … `carrusel_05` | Explicar cómo funciona Tazón para Dos en 5 láminas |
| **Foto de perfil** | `perfil` | Instagram, Facebook, Spotify y WhatsApp (se recorta en círculo) |
| **Portadas de destacadas** | `destacada_rol`, `_mesa`, `_podcast`, `_convocatoria`, `_ubicacion`, `_horario` | Historias destacadas de Instagram |

**Reglas del carrusel**
- **Portada:** fondo tinta.
- **Láminas de contenido:** cada una en un color (turquesa, coral, sol), con número gigante, ícono en un círculo y "DESLIZA →" abajo.
- **Cierre:** fondo tinta con el llamado a la acción.

---

## 10. Podcast: identidad propia

El podcast de Tazón para Dos es un **podcast de rol que habla en lenguaje de cocina**: *"cada episodio es un platillo distinto, servido con imaginación y sazón narrativa"*. Los episodios se organizan como un **menú**:

| Sección del menú | Qué es | Color de portada |
|---|---|---|
| **Mesa Principal** | Campañas largas "cocinadas a fuego lento" | Coral |
| **Entremeses** | Historias más ligeras | Turquesa |
| **Dessert** | Por ejemplo, el episodio "Press Start - Dessert" | Sol |

**Vocabulario:** menú, platillo, comensales, sazón, a fuego lento, chef, receta.

**Portadas (3000 × 3000)**
- **Del show:** `podcast_portada` lleva la mascota en un círculo turquesa, un d20 que sale como vapor y el lema "Cada episodio es un platillo distinto."
- **De cada episodio:** `podcast_episodio_plantilla` tiene el fondo del color de la sección, la etiqueta "MENÚ · SECCIÓN", un d20 servido en un plato crema y el título. El ejemplo real es `podcast_episodio_ejemplo` ("Press Start").

---

## 11. Fotografía

Las fotos muestran **la mesa viva**: manos con dados, cartas y fichas, grupos riendo, la grabación del podcast y detalles como tazas, mapas u hojas de personaje.

| Aspecto | Guía |
|---|---|
| **Luz** | Cálida y natural. Evita el flash directo |
| **Encuadre** | Fotos desde arriba de la mesa, primeros planos de manos y planos medios de grupo. Deja espacio libre para poner titulares |
| **Color** | Sin filtros fuertes. El color de marca lo ponen los bloques gráficos, no la foto |
| **Tratamiento** | Marco con esquinas redondeadas y contorno tinta, o recorte siguiendo las diagonales |
| **Evitar** | Fotos de banco de imágenes, pantallas con datos personales y filtros que cambien el tono de piel |

### 🛡️ Consentimiento (obligatorio)

Somos un **espacio seguro LGBTI+**. Antes de publicar una foto donde se reconozca a alguien, **pide permiso explícito**. Ofrece siempre la opción de salir solo con las manos. Nunca etiquetes ni nombres a nadie sin su consentimiento.

---

## 12. Productos y aplicaciones

| Aplicación | Estado | Notas |
|---|---|---|
| Hoja de stickers | ✅ Plantilla lista | `aplicaciones/stickers.svg`, en vinilo mate con corte a 6 mm |
| Tarjeta de presentación | ✅ Lista (PDF) | `tarjeta_frente` / `tarjeta_reverso`, 85 × 55 mm |
| Letrero de horario | ✅ Listo (PDF) | `letrero_horario_a4`, para la puerta del espacio |
| Ficha de personaje | ✅ Lista (PDF) | `ficha_personaje_a4`, sirve para cualquier sistema de rol y tiene campo de pronombres |
| Certificado de taller | ✅ Listo (PDF) | `certificado_taller`: cambia el nombre, el taller y la fecha |
| Firma de correo | ✅ Lista | `firma_correo.html`: ábrela, cópiala y pégala en Gmail |
| Tazón de cerámica | Propuesta con fotomontaje (`merch_mockups`) | Mascota en tinta y "Jugar también es escuchar." al reverso |
| Bolsa de tela | Propuesta con fotomontaje | Logotipo apilado en tinta sobre lona cruda |
| Set de dados | Propuesta con fotomontaje | d20 sol y turquesa con el tazón en la cara del 20 |

---

## 13. Para imprimir

- **PDF listos en `impresion/`.** Tienen el tamaño físico real y las fuentes incrustadas, así que no hace falta convertir textos a trazos:

  | Archivo | Tamaño |
  |---|---|
  | `tarjeta_frente.pdf` y `tarjeta_reverso.pdf` | 85 × 55 mm |
  | `letrero_horario_a4.pdf` y `ficha_personaje_a4.pdf` | A4 |
  | `certificado_taller.pdf` | A4 horizontal |
  | `stickers.pdf` | 20 × 20 cm |
  | `pancarta_80x180.pdf` | 80 × 180 cm |

- **Sangrado y CMYK:** los PDF vienen **en RGB y sin sangrado**. Para impresión offset o una pancarta grande, pregunta a la imprenta si necesita 3 mm de sangrado y conversión a CMYK. Normalmente lo hacen ellos.
- **Colores:** pide una **prueba de color**. El turquesa y el coral cambian bastante entre pantalla e impresión.
- **Para regenerar los PDF:** `python -I tools/export.py`.
- **Logos en PNG con fondo transparente:** están en `assets/logo/png/` y sirven para Word, Canva o el correo. El ícono de pestaña está en `assets/logo/favicon.ico` y `favicon.svg`.

---

## 14. Cómo hacer una pieza nueva

1. Copia la plantilla más parecida de `plantillas/`.
2. Cambia los textos y respeta la estructura del punto 9.
3. Usa solo los colores de la paleta y los elementos de `assets/`.
4. Revisa el contraste: el texto va en tinta sobre color.
5. Exporta a PNG con `tools/render.ps1` (o desde Inkscape).

Si trabajas con una IA (Claude, ChatGPT…), dale el archivo [`AGENTS.md`](AGENTS.md). Tiene las reglas en un formato que las máquinas entienden.
