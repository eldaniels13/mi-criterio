# Closing Session — Transporte Seguro GDL (Mundial 2026)

## Contexto

Se realizó una sesión de revisión estratégica sobre el proyecto **Transporte Seguro GDL**, enfocado en traslados privados desde el Aeropuerto Internacional de Guadalajara para visitantes del Mundial FIFA 2026.

El objetivo principal fue comenzar a validar la propuesta comercial y detectar los puntos que requieren refinamiento antes de lanzar la página web y las campañas de captación de clientes.

---

## Temas Revisados

### 1. Propuesta de Valor

Se identificó que el proyecto necesita definir con claridad cuál será su principal diferenciador:

- Velocidad y eficiencia.
- Servicio privado.
- Seguridad.
- Precio fijo.
- Atención a turistas internacionales.
- Transporte para grupos.

Durante la conversación surgió la idea de enfatizar la rapidez y facilidad del servicio para visitantes del Mundial.

---

### 2. Validación de Rutas y Precios

Se inició la revisión de rutas reales y tarifas previstas.

Se mencionó:

- Ruta hacia el Centro de Guadalajara.
- Opciones diferenciadas según capacidad de pasajeros.
- Cobertura de la zona Expo Guadalajara.

Se acordó continuar posteriormente con la recopilación completa de:

- Destinos.
- Tarifas.
- Capacidad de pasajeros.
- Restricciones operativas.
- Tiempos estimados de traslado.

---

### 3. Aspectos Pendientes de Refinar

#### Credibilidad

Validar información que aparecerá en la página:

- Número de viajes realizados.
- Calificación en Google.
- Años de experiencia.
- Evidencia de reputación.

#### Operación

Definir:

- Número de vehículos disponibles.
- Capacidad diaria.
- Horarios.
- Métodos de pago.
- Facturación.
- Gestión de reservas simultáneas.

#### SEO

Revisar:

- Palabras clave en español.
- Palabras clave en inglés.
- Posibles páginas específicas para rutas relevantes.
- Estrategia de posicionamiento para búsquedas relacionadas con el Mundial 2026.

---

## Próximos Pasos

### Prioridad Alta

1. Elaborar listado completo de rutas.
2. Definir tarifas finales.
3. Confirmar capacidades de pasajeros y equipaje.
4. Identificar rutas más rentables.
5. Definir propuesta de valor principal.

### Prioridad Media

1. Revisar requisitos legales y seguros.
2. Crear ficha de Google Business.
3. Preparar evidencia de reseñas.
4. Optimizar estructura SEO.

### Prioridad Baja

1. Automatización de reservas.
2. Integración avanzada con WhatsApp Business.
3. Formularios inteligentes.
4. Traducción y localización avanzada.

---

## Estado Actual

Proyecto en fase de definición y refinamiento comercial.

La siguiente sesión debería centrarse en:

- Rutas.
- Precios.
- Capacidad operativa.
- Rentabilidad.
- Competencia (Uber, taxis autorizados y otros servicios privados).

---

## Resultado de la Sesión

Se estableció una estructura clara para continuar el desarrollo del proyecto y se identificaron los principales vacíos de información que deben resolverse antes de la publicación definitiva de la página web.

---

## Sesión 2026-06-04 — Landing page construida

A partir de este documento como brief, se construyó una página web funcional lista para publicar (no solo planeación).

**Output:** `~/Downloads/transporte-seguro-gdl/index.html` — HTML/CSS/JS vanilla, archivo único, sin frameworks ni build step, abre directo en navegador.

**Design read declarado:** *"Consumer service landing para turistas internacionales en aeropuerto, trust-first + dark premium, cobalt blue accent."* Diales: `DESIGN_VARIANCE: 7` (asimetría moderada) · `MOTION_INTENSITY: 4` (scroll reveals vía IntersectionObserver, sin GSAP) · `VISUAL_DENSITY: 4` (limpio, escaneable en móvil).

**Paleta:** dark navy `#07091a` (paleta cálida/beige descartada intencionalmente) · acento cobalt blue `#2563eb` (lectura de confianza/autoridad) · CTA WhatsApp green `#22c55e` (estándar reconocible). Tipografía: Outfit (Google Fonts).

**Arquitectura — 8 secciones, 7 familias de layout:** nav sticky (glassmorphism) · hero split 50/50 · marquee strip (scroll infinito, único en la página) · "cómo funciona" (3 tarjetas con flechas) · rutas y precios (grid auto-fill) · "por qué elegirnos" (bento grid 6 columnas) · FAQ (acordeón JS nativo) · CTA + footer.

**Funcionalidades:** bilingüe ES/EN (`body.lang-en` + `data-lang`) · scroll reveal (`threshold: 0.08`, respeta `prefers-reduced-motion`) · FAQ accordion sin dependencias · nav móvil hamburger (<640px) · 4 rutas con tarifas MXN + equivalencia USD · WhatsApp CTA consistente (nav/hero/CTA band, sin duplicar intent) · iconos SVG inline, imágenes Picsum placeholder.

**Pendientes para publicación (bloqueantes):**
1. Número de WhatsApp real — reemplazar placeholder `5233XXXXXXXX` (3 lugares)
2. Teléfono de contacto real — reemplazar `+52 33 XXXX XXXX` en CTA
3. Precios finales (las 4 rutas usan tarifas de referencia)
4. Foto hero real (aeropuerto/ciudad) en vez de Picsum
5. Meta description, OG tags, favicon
6. Ficha de Google Business (prioridad media ya identificada en el brief original)
