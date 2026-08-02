# Arquitectura de noticias sin sesgo ni telemetría

**Fecha:** 2026-08-02 · **Lens:** P2 (programación) ↔ P4 (finanzas, BBB) ↔ P8 (soberanía de datos)
**Tags:** rss, self-hosted, gdelt, llm-local, ollama, agentes-open-source
**Archivos generados:**
- `fuentes_contraste.opml` — 56 feeds RSS en 9 grupos organizados por geografía/financiamiento (no eje izquierda-derecha)
- `verificar_feeds.py` — valida feeds (HTTP, parseo, antigüedad de última entrada), genera OPML depurado
- `gdelt_contraste.py` — consulta GDELT DOC API por bloques de medios o por país/idioma/dominio, detecta blindspots

## Contexto

Buscaba un sustituto del "periódico" tradicional que contrastara fuentes globales y nacionales sin caer en agregadores comerciales sesgados (Ground News, AllSides), sin alimentar modelos de IA corporativos con la actividad de lectura, y sin depender de una línea editorial de terceros — pidiendo a la vez que la información llegara "digerida", lo cual es contradictorio con "sin sesgo".

## Puntos clave

- La contradicción del pedido original se resolvió separando 3 capas: agregación cruda (neutral, sin editorializar) → contraste (datos crudos comparables) → digestión (reservada para mí mismo o un LLM que yo controle, no un tercero).
- Miniflux (Go, Apache-2.0, Postgres, un binario) preferido sobre FreshRSS (PHP, AGPL-3.0, más piezas) por menor superficie de mantenimiento — a confirmar con prueba real.
- Necesito servidor 24/7 (candidato: fibonacci), no "cero infraestructura", porque quiero estado de lectura sincronizado entre fibonacci y el celular — sin servidor cada dispositivo lleva su copia sin comunicarse entre sí.
- YouTube expone RSS nativo por `channel_id` sin pasar por el algoritmo de recomendación; Instagram/Telegram requieren RSS-Bridge self-hosted como puente.
- GDELT DOC API: gratis, sin llave, indexa prensa mundial en 100+ idiomas, pero da metadatos (país, idioma, dominio, tono) — no lectura digerida. Cobertura más débil en medios pequeños en español que en agencias grandes en inglés.
- "Popular = más seguro" es cierto en general pero con fallas documentadas: Heartbleed (2 años sin detectarse en OpenSSL) y el backdoor de xz-utils (2024, insertado por mantenedor de confianza tras años de ganarse credibilidad). Popularidad de uso ≠ auditoría real.
- Hardware real: i7-8665U (fibonacci) es ULV sin AVX-512 ni GPU dedicada — cuello de botella es ancho de banda de RAM, no núcleos. Modelos 3-4B en Q4 (Phi-4 Mini, Qwen3 4B) rinden ~8-12 tok/s según benchmarks externos (no medición propia todavía) — viable para batch nocturno, no para agente interactivo en tiempo real.
- Existen harnesses agénticos open source ya maduros que se pueden apuntar a Ollama local: OpenCode (MIT, 161k estrellas, 75+ proveedores), Aider (git-nativo), Goose (Apache-2.0, Agentic AI Foundation). La limitación actual es velocidad de hardware, no disponibilidad de herramienta.
- Ruta de inversión en 4 niveles: Nivel 0 (ya, Ollama 3-4B batch) → Nivel 1 (~$300-500, mini PC con iGPU tipo Ryzen 8845HS, 15-25 tok/s) → Nivel 2 (eGPU Thunderbolt si el puerto lo soporta) → Nivel 3 (RunPod/vast.ai por hora, puente honesto sin comprar hardware).

## Decisiones tomadas

- [x] Descartar Ground News / AllSides como base del sistema — propietario, anglocéntrico, eje binario izquierda-derecha.
- [x] Arquitectura de 3 capas: agregación / contraste / digestión, separadas explícitamente.
- [x] GDELT DOC API como fuente de contraste (metadatos crudos), no como fuente de lectura directa.
- [x] Digestión (capa 3, LLM) se pospone para mí mismo por ahora; el diseño del agente local queda como raíz de P2, no de este proyecto de noticias.
- [ ] Elegir agregador definitivo (Miniflux vs FreshRSS) tras prueba real en fibonacci.

## Pendientes

- [ ] `pip install feedparser requests --break-system-packages` en fibonacci
- [ ] Correr `verificar_feeds.py` sobre `fuentes_contraste.opml` desde fibonacci — el contenedor de esta sesión devolvió 403 de proxy en todos los dominios de prensa (sin salida de red real), no se validó ningún feed en condiciones reales
- [ ] Levantar Miniflux + Postgres en Docker en fibonacci
- [ ] RSS-Bridge para Instagram/Telegram
- [ ] Obtener `channel_id` de Canal Red, La Base, SinEmbargo Al Aire, Rompeviento TV para RSS nativo de YouTube
- [ ] Probar `gdelt_contraste.py` con un tema real y ventana de 48h — no se ejecutó con red real esta sesión
- [ ] Instalar Ollama + Phi-4 Mini o Qwen3 4B en fibonacci y medir tok/s real en el i7-8665U (los números de esta sesión son de fuentes externas, no medición propia)
- [ ] Evaluar scraper de versión estenográfica de gob.mx/presidencia como alternativa gratuita a mananeradehoy.com (que tiene plan de pago para búsqueda ilimitada)

## Insight cross-lens

**P2 + P4** → la ruta de inversión en hardware para LLM local es una escalera de 4 niveles donde cada peldaño exige uso real comprobado antes de subir al siguiente — mismo criterio BBB ya aplicado en P8 (`Timeline_Fases.md`: no saltar fases). Nivel 3 (GPU rentada por hora) es el puente correcto mientras no hay presupuesto para hardware propio, evitando comprar antes de validar que el flujo agente+Ollama se usa a diario.

**P2 + P8** → el agregador RSS self-hosted en fibonacci es el mismo patrón de soberanía ya aplicado en backups: control físico de la infraestructura, sin depender de que un tercero decida seguir ofreciendo el servicio.
