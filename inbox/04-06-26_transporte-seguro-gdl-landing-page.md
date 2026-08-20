# Sesion: Landing Page — Transporte Seguro GDL

**Fecha:** 2026-06-04
**Tipo:** Diseno y desarrollo frontend
**Archivo fuente:** `~/Downloads/closing_session_transporte_seguro_gdl.md`
**Output:** `~/Downloads/transporte-seguro-gdl/index.html`

---

## Contexto

Se retomo el proyecto **Transporte Seguro GDL** (traslados privados desde el Aeropuerto Internacional de Guadalajara para visitantes del Mundial FIFA 2026) a partir de un documento de cierre de sesion estrategica previa.

El objetivo fue convertir ese documento de planeacion en una pagina web funcional y lista para publicar.

---

## Proceso

### 1. Lectura del brief

Brief leido desde `closing_session_transporte_seguro_gdl.md`. Puntos clave extraidos:

- Servicio de traslados privados desde el aeropuerto
- Diferenciadores pendientes de definir: velocidad, precio fijo, privacidad, atencion a turistas internacionales, grupos
- Rutas identificadas: Centro GDL, Expo Guadalajara, y otras zonas por confirmar
- Precios, capacidad y metodos de pago aun no definidos
- CTA principal: WhatsApp

### 2. Design Read y decisiones de diseno

**Design Read declarado:**
> "Consumer service landing para turistas internacionales en aeropuerto, trust-first + dark premium, cobalt blue accent."

**Diales configurados:**
- `DESIGN_VARIANCE: 7` — asimetria moderada, no agencia experimental
- `MOTION_INTENSITY: 4` — scroll reveals via IntersectionObserver, CSS transitions, sin GSAP
- `VISUAL_DENSITY: 4` — limpio, escaneable en movil

**Decisiones de paleta:**
- Base: dark navy (`#07091a`) — paleta calida/beige descartada intencionalmente
- Acento: cobalt blue (`#2563eb`) — lectura de confianza y autoridad
- CTA: WhatsApp green (`#22c55e`) — estandar reconocible internacionalmente

**Tipografia:**
- Outfit (Google Fonts CDN) — moderna, geometrica, sin Inter

### 3. Arquitectura de la pagina

8 secciones con 7 familias de layout distintas:

| Seccion | Layout |
|---|---|
| Nav sticky | Glassmorphism, una linea |
| Hero | Split screen 50/50 (copy + foto ciudad) |
| Marquee strip | Scroll infinito, unico en la pagina |
| Como funciona | 3 tarjetas con flechas conectoras |
| Rutas y precios | Grid de tarjetas (auto-fill) |
| Por que elegirnos | Bento grid 6 columnas, 5 celdas variadas |
| FAQ | Acordeon JS nativo |
| CTA + Footer | Full-width centrado + footer minimalista |

### 4. Funcionalidades implementadas

- **Bilingue (ES/EN)** — toggle en el nav, via clase CSS `body.lang-en` + atributos `data-lang`
- **Scroll reveal** — IntersectionObserver con `threshold: 0.08`, respeta `prefers-reduced-motion`
- **FAQ accordion** — JS nativo, sin dependencias
- **Mobile nav** — hamburger para < 640px, nav desplegable
- **Precios de referencia** — 4 rutas con tarifas MXN + equivalencia USD aproximada, nota de aclaracion incluida
- **WhatsApp CTA consistente** — mismo label en nav, hero, CTA band (sin duplicacion de intent)

### 5. Stack tecnico

- HTML/CSS/JS vanilla, archivo unico `index.html`
- Sin frameworks, sin build step — abre directo en navegador
- Fuentes via Google Fonts (CDN)
- Imagenes via Picsum con seed descriptivo (placeholder)
- Iconos inline SVG (no dependencia externa)

---

## Pendientes para publicacion

Busquedas en el archivo: `5233XXXXXXXX`

1. **Numero de WhatsApp real** — reemplazar `5233XXXXXXXX` (aparece en 3 lugares)
2. **Telefono de contacto** — reemplazar `+52 33 XXXX XXXX` en la seccion CTA
3. **Precios finales** — las 4 rutas usan tarifas de referencia; actualizar con precios reales
4. **Foto hero** — actualmente Picsum placeholder; sustituir con foto real del aeropuerto o ciudad
5. **Credenciales SEO** — meta description, OG tags, favicon pendientes
6. **Google Business** — crear ficha antes de lanzar (identificado como prioridad media en el brief original)

---

## Archivos generados

```
~/Downloads/transporte-seguro-gdl/
└── index.html   ← pagina completa, lista para abrir en navegador o subir a hosting
```

