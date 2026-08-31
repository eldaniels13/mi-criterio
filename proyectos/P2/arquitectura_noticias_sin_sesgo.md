# Arquitectura de noticias sin sesgo ni telemetría

**Fecha:** 2026-08-02 · **Lens:** P2 (programación) × P5 (geopolítica/economía) × P4 (finanzas, BBB) × P8 (soberanía de datos)
**Estado:** diseñado, no ejecutado con red real — ver Pendientes

**Archivos generados (esta sesión, no en el repo):**
- `fuentes_contraste.opml` — 56 feeds RSS en 9 grupos organizados por geografía/financiamiento (no eje izquierda-derecha)
- `verificar_feeds.py` — valida feeds (HTTP, parseo, antigüedad de última entrada), genera OPML depurado
- `gdelt_contraste.py` — consulta GDELT DOC API por bloques de medios o por país/idioma/dominio, detecta blindspots

## Contexto

Sustituto del "periódico" tradicional que contraste fuentes globales y nacionales sin caer en agregadores comerciales sesgados (Ground News, AllSides), sin alimentar modelos de IA corporativos con la actividad de lectura, y sin depender de línea editorial de terceros — con la tensión de que la información llegue "digerida", lo cual es contradictorio con "sin sesgo" si la digestión la hace un tercero.

Aunque nació como proyecto de programación (P2), el objeto real del sistema es geopolítico: contrastar cómo distintos países, bloques económicos y medios financiados de forma distinta narran los mismos hechos. Agrupar los 56 feeds por **geografía/financiamiento** en vez del eje izquierda-derecha ya es una decisión de análisis geopolítico, no sólo de ingeniería — evita el sesgo más común del panorama mediático angloparlante (izq/der doméstico de EE.UU.) e incluye el eje que sí importa para un lector fuera de esa órbita: quién financia el medio y desde qué país habla.

## Arquitectura de 3 capas (resuelve la contradicción)

1. **Agregación cruda** — neutral, sin editorializar
2. **Contraste** — datos crudos comparables (GDELT): país, idioma, dominio, tono — el material de trabajo de un análisis P5 real (blindspots por bloque geopolítico, no por partido)
3. **Digestión** — reservada para el usuario mismo o un LLM local que él controle, nunca un tercero. Diseño del agente local vive en `HANDOFF_LLM_agentico_local.md` (P2), no aquí.

## Decisiones tomadas

- [x] Descartar Ground News / AllSides — propietario, anglocéntrico, eje binario izquierda-derecha (un encuadre P5 pobre: no captura Sur Global, prensa estatal no-angloparlante, ni financiamiento real de cada medio)
- [x] Arquitectura de 3 capas explícitas (agregación / contraste / digestión)
- [x] GDELT DOC API como fuente de contraste (metadatos: país, idioma, dominio, tono), no de lectura directa — gratis, sin llave, 100+ idiomas, cobertura más débil en medios pequeños en español que en agencias grandes en inglés (sesgo estructural a tener en cuenta al leer "blindspots": el propio GDELT sub-representa la prensa hispanohablante pequeña)
- [ ] Elegir agregador definitivo tras prueba real en fibonacci: **Miniflux** (Go, Apache-2.0, Postgres, un binario) preferido sobre **FreshRSS** (PHP, AGPL-3.0, más piezas) por menor superficie de mantenimiento — a confirmar

## Infraestructura

Necesita servidor 24/7 (candidato: fibonacci), no "cero infraestructura" — para sincronizar estado de lectura entre fibonacci y celular (sin servidor cada dispositivo lleva su copia sin comunicarse).

YouTube expone RSS nativo por `channel_id` sin pasar por el algoritmo de recomendación; Instagram/Telegram requieren RSS-Bridge self-hosted como puente.

## Hardware — ruta de inversión en 4 niveles

i7-8665U (fibonacci) es ULV sin AVX-512 ni GPU dedicada — cuello de botella es ancho de banda de RAM, no núcleos. Modelos 3-4B en Q4 (Phi-4 Mini, Qwen3 4B) rinden ~8-12 tok/s según benchmarks **externos** (no medición propia) — viable para batch nocturno, no agente interactivo en tiempo real.

- Nivel 0 (ya): Ollama 3-4B batch
- Nivel 1 (~$300-500): mini PC con iGPU tipo Ryzen 8845HS, 15-25 tok/s
- Nivel 2: eGPU Thunderbolt si el puerto lo soporta
- Nivel 3: RunPod/vast.ai por hora — puente honesto sin comprar hardware

Harnesses agénticos maduros disponibles para apuntar a Ollama local: OpenCode (MIT, 161k stars, 75+ proveedores — decisión ya tomada en `HANDOFF_LLM_agentico_local.md`), Aider (git-nativo, bloqueado por deadlock), Goose (Apache-2.0). Limitación actual es velocidad de hardware, no disponibilidad de herramienta.

**Nota de seguridad (base rate):** "popular = más seguro" tiene fallas documentadas — Heartbleed (2 años sin detectarse en OpenSSL), backdoor de xz-utils (2024, insertado por mantenedor de confianza tras años ganando credibilidad). Popularidad de uso ≠ auditoría real. Relevante al elegir Miniflux/FreshRSS y cualquier paquete AUR (ver `recursos/AUR_Atomic_Arch_2026_Informe.md`).

## Panorama geopolítico-económico del proyecto (P5)

- **Los 9 grupos de `fuentes_contraste.opml`** son, en la práctica, una taxonomía geopolítica de medios: agencias estatales, prensa comercial occidental, prensa de bloques no-alineados, medios independientes/no financiados por publicidad, etc. Documentar esa taxonomía explícitamente (qué grupo = qué financiamiento/Estado) es trabajo pendiente de P5, no sólo de P2 — hoy vive implícito en el OPML.
- **GDELT como termómetro de cobertura desigual entre bloques**: permite medir cuánto habla la prensa de un país/bloque sobre un evento vs. otro (blindspots), que es exactamente el tipo de evidencia que sustenta análisis de sesgo mediático estructural (Prebisch/estructuralismo aplicado a flujo de información en vez de flujo de capital — mismo patrón centro/periferia, esta vez informativo).
- **Riesgo a vigilar**: la elección de qué 56 feeds entran al OPML ya es una decisión editorial (qué cuenta como "fuente seria" por bloque). Sin un criterio explícito y documentado de inclusión/exclusión por país, el "sin sesgo" del título es aspiracional, no verificado — pendiente abrir esa lista a revisión con criterio P5 explícito antes de tratarla como neutral.
- **Estenografía presidencial (gob.mx)** como fuente primaria sin intermediación editorial es, en sí, una fuente de tipo P5 (comunicación de Estado directa) distinta en naturaleza de la prensa comercial contrastada — vale la pena mantenerla como categoría propia en el OPML, no mezclada con medios.

## Pendientes

- [ ] `pip install feedparser requests --break-system-packages` en fibonacci
- [ ] Correr `verificar_feeds.py` sobre `fuentes_contraste.opml` desde fibonacci — sesión de diseño devolvió 403 de proxy en todos los dominios de prensa, ningún feed validado en condiciones reales
- [ ] Levantar Miniflux + Postgres en Docker en fibonacci
- [ ] RSS-Bridge para Instagram/Telegram
- [ ] Obtener `channel_id` de Canal Red, La Base, SinEmbargo Al Aire, Rompeviento TV para RSS nativo de YouTube
- [ ] Probar `gdelt_contraste.py` con tema real y ventana de 48h — no ejecutado con red real
- [ ] Instalar Ollama + Phi-4 Mini o Qwen3 4B en fibonacci y medir tok/s real — números actuales son de fuentes externas
- [ ] Evaluar scraper de versión estenográfica de gob.mx/presidencia como alternativa gratuita a mananeradehoy.com (plan de pago para búsqueda ilimitada)
- [ ] Documentar explícitamente el criterio de inclusión/exclusión por país-bloque de los 9 grupos del OPML (deuda P5 identificada arriba)

## Insight cross-lens

**P2+P4:** la escalera de inversión en hardware exige uso real comprobado antes de subir de nivel — mismo criterio BBB aplicado en `P8_Backup_Wiki/` (no saltar fases). Nivel 3 (GPU rentada por hora) es el puente correcto mientras no hay presupuesto propio.

**P2+P8:** el agregador RSS self-hosted en fibonacci es el mismo patrón de soberanía ya aplicado en backups — control físico de infraestructura, sin depender de que un tercero siga ofreciendo el servicio.

**P2+P5:** un sistema de "noticias sin sesgo" construido por ingeniería (P2) sin un criterio geopolítico explícito (P5) sólo desplaza el sesgo de "editorial de un tercero" a "elección de fuentes no documentada del propio usuario". La arquitectura técnica ya está resuelta; el trabajo de P5 pendiente (criterio de inclusión por bloque, lectura de blindspots GDELT) es el que realmente entrega "sin sesgo", no el RSS ni el LLM local.
