# HANDOFF — LLM agéntico local (fibonacci / Dell Latitude 5400)

> **Propósito:** documento único de traspaso. Reúne todo lo trabajado sobre correr modelos de lenguaje localmente y construir una capa agéntica propia (ejecución de herramientas/comandos) sobre hardware CPU-only. Sustituye la necesidad de reconstruir contexto desde cero en una sesión nueva.
>
> **Fecha de corte:** 2026-09-05 · **Estado global:** OpenCode instalado y en uso activo (modelos remotos); **prueba crítica de tool-use sobre Ollama local aún pendiente** (Bloque B)
> **Lens:** P2 (programación) × P8 (soberanía de datos) × P4 (BBB / inversión en hardware)

---

## 1 · Contexto y objetivo del proyecto

### Objetivo

Tener un asistente de IA **agéntico** (que lea archivos, edite código y ejecute comandos, no solo chatee) corriendo **100% local**, sin API keys, sin telemetría, sin conexión.

### Motivación (por qué, no solo qué)

| Driver | Detalle |
|---|---|
| **Privacidad** | Datos personales, código sensible y exploración filosófica no deberían salir de la máquina |
| **Independencia** | Trabajar sin wifi (avión, viajes, cortes de red) |
| **Costo cero** | Tareas repetitivas y de alto volumen sin pagar por token |
| **Seguro contra precio** | Si mañana Claude sube 5x, no quedarse en cero |
| **Principios de sistema** | Alineado a: seguro, privado, estable, open source, copyleft, minimal, clean |

### Filosofía operativa ya decidida

> La soberanía **no** está en abandonar lo rentado. Está en **TENER la opción local funcionando**.

Stack **híbrido**, no uno-u-otro: local cubre lo que cubre bien; se reserva la IA rentada para el salto de calidad que la justifique.

### Tres workflows objetivo (definidos 2026-05)

1. **Coding assistant** — edición, refactor, debug sobre repos reales
2. **RAG sobre `mi-criterio`** — Q&A semántico sobre el repo de conocimiento personal
3. **Chat / razonamiento general** — sustituto de ChatGPT/Claude en preguntas no-código

### Proyectos aguas abajo que dependen de esta base

- **Motor de búsqueda personal + LLM agentivo** (P2 × P8, planning-only) — alternativa a Google/Perplexity: Ollama + Meilisearch + agente propio + integración a Firefox vía OpenSearch XML. Documentado en `memory/project_personal_search_engine_with_llm.md` y en `ToDo_global_eldaniels.md`.
- **Arquitectura de noticias sin sesgo** (`proyectos/P2/arquitectura_noticias_sin_sesgo.md`) — su "capa 3 · digestión" es explícitamente un LLM local controlado por el usuario. Decisión registrada ahí: *el diseño del agente local queda como raíz de P2, no de ese proyecto*.

---

## 2 · Decisiones técnicas ya tomadas (con justificación)

| # | Decisión | Justificación | Fecha |
|---|---|---|---|
| D1 | **Ollama** como runtime de inferencia | Integración nativa con todo el ecosistema, cero config extra, mismo backend para todas las interfaces (no duplica modelos en disco) | 2026-05 |
| D2 | **No comprar hardware ahora** — exprimir el setup actual | El software stack es idéntico independiente del hardware: al upgradear a GPU la migración es **cero** (mismo Ollama, misma config, solo cambia `model:`). El trabajo se acumula. | 2026-05 |
| D3 | **Open WebUI** como interfaz de chat + RAG | RAG built-in usando `nomic-embed-text` (ya instalado), UI familiar, conversaciones guardadas localmente, instalación trivial vía `uv tool install` | 2026-05-18 |
| D4 | **Aider deprioritizado, no eliminado** | Timeout sistemático `litellm.Timeout: 600s` aun con `map-tokens: 128`, mientras `ollama run` directo responde en 48s. Es un **deadlock** entre litellm y Ollama en CPU-only, no lentitud. | 2026-05-18 |
| D5 | Modelo principal **`deepseek-coder:6.7b`** (3.8 GB) | Mejor relación calidad/velocidad que cabe cómodo en RAM y responde en tiempo tolerable | 2026-05 |
| D6 | `OLLAMA_KEEP_ALIVE=30m` + `OLLAMA_NUM_THREAD=8` | Mantiene el modelo caliente en RAM (evita recarga de 3.8 GB por prompt) y usa los 8 hilos lógicos del i7-8665U | 2026-05 |
| D7 | **OpenCode como base agéntica**, en vez de construir en Python desde cero | MIT, paquete oficial en repo `extra` de Arch (sin AUR → no activa el protocolo de revisión de PKGBUILD), soporta 75+ proveedores. Configurar > reimplementar agent loop + tool-calling + streaming. | 2026-08-06 |
| D8 | La config viva **no vive en `mi-criterio`** | `mi-criterio` es repo de conocimiento, no de dotfiles ni de secretos. Config → `~/.config/opencode/`; keys → `opencode auth login`. | 2026-08-06 |
| D9 | Ruta de upgrade en **4 niveles**, cada peldaño exige uso real comprobado antes de subir | Criterio BBB aplicado: no comprar antes de validar que el flujo agente+Ollama se usa a diario. Nivel 0 (hoy, CPU) → Nivel 1 (~$300-500, mini PC iGPU Ryzen 8845HS, 15-25 tok/s) → Nivel 2 (eGPU Thunderbolt) → Nivel 3 (RunPod/vast.ai por hora = puente honesto sin comprar). | 2026-08-02 |
| D10 | Validar tool-use **antes** de personalizar nada | El deadlock de Aider es el riesgo #1 de repetirse. Si OpenCode falla igual, se detiene ahí. | 2026-08-06 |

### Punto ciego ya nombrado [!]

La tentación de decir *"ya no necesito pagar por IA"*. La realidad medida: se **ahorra** en chat/RAG/código simple, se **reserva** lo rentado para refactor multi-archivo, debugging sutil y arquitectura. Ver tabla de decisión en `stack_ia_local_veredicto.md`.

---

## 3 · Herramientas y modelos evaluados o descartados

### Runtimes de inferencia

| Herramienta | Veredicto | Razón |
|---|---|---|
| **Ollama** | ✅ **Adoptado** | Runtime activo. Simple, integración universal, mismo store de modelos para todas las interfaces |
| llama.cpp | 🔶 Conocido, no adoptado | Más eficiente y sin overhead de servidor, pero Ollama ya lo abstrae. Reservado por si el overhead de Ollama estorba |
| vLLM | ❌ Descartado | Requiere GPU potente. No aplica a CPU-only |
| LM Studio | ❌ Descartado | No open-source puro; contradice el principio de stack abierto |
| LocalAI | 🔶 Evaluado, no probado | Redundante con Ollama para este caso |

### Interfaces / harnesses agénticos

| Herramienta | Veredicto | Razón |
|---|---|---|
| **Open WebUI** v0.9.5 | ✅ Adoptado (2026-05) · ⚠️ **inactivo hoy** | Cubre chat + RAG. Instalado vía `uv tool install open-webui`. Fix necesario: `audioop-lts` (Python 3.13 rompe `pydub`, que no encuentra el módulo `audioop`). Hoy no corre — puerto 8080 sin respuesta |
| **Aider** v0.86.2 | ⚠️ Instalado, **bloqueado** | `litellm.Timeout: 600s` sistemático. Hipótesis: la orquestación de litellm hace muchas requests pequeñas que saturan el endpoint CPU-only. Queda para reinvestigar con GPU |
| **OpenCode** | ✅ **Instalado (1.18.25-1, pacman) y en uso activo desde 2026-09** · ⚠️ prueba crítica de tool-use sobre Ollama local pendiente | MIT, en `extra/` de Arch firmado. Login OAuth nativo para Claude Pro/Max (`opencode auth login -p anthropic`) — usaría la suscripción existente sin API key aparte. *No oficialmente soportado por Anthropic fuera de sus clientes → necesita plan B (API key de console)* |
| Goose | 🔶 Anotado como alternativa | Apache-2.0, Agentic AI Foundation. No evaluado en vivo |
| Continue.dev / Cline / LibreChat / AnythingLLM | ❌ Descartados | No aportan sobre Aider + Open WebUI para este workflow |
| LangChain / LlamaIndex / Haystack | 🔶 Conceptualmente evaluados | Válidos para orquestación custom, pero D7 (usar harness maduro) los pospone |
| AutoGPT | ❌ Descartado | Overkill; solo como referencia de implementación |

### Modelos

| Modelo | Estado | Razón |
|---|---|---|
| **`deepseek-coder:6.7b`** (3.8 GB) | ✅ Instalado, principal para chat | Calidad ≈ GPT-3.5 en buen día. **Limitación crítica descubierta 2026-08-06: no declara capability `tools` en su manifiesto Ollama → NO sirve para uso agéntico, solo chat plano** |
| **`nomic-embed-text`** (274 MB) | ✅ Instalado | Embeddings para RAG. No usar para chat |
| `deepseek-coder-v2:16b` (8.9 GB) | ❌ **Eliminado** | MoE 16B → 2-10 min por respuesta en CPU = no es workflow. Liberó 8.9 GB |
| `qwen2.5-coder:1.5b` (986 MB) | ❌ Eliminado (2026-05) · 🔁 **Se necesita de vuelta** | Se borró por redundante con 6.7b, pero **sí soporta `tools`** → es el candidato para validar el agent loop (Fase 3 del plan OpenCode) |
| `qwen2.5-coder:7b` | ❌ Ya no presente | Desapareció del sistema; Alt+P todavía lo referencia (drift) |
| `deepseek-v4-flash:cloud` / `:0731-cloud` | ⚠️ Presentes, **son proxies remotos** | Son de **Ollama Cloud**, NO locales. Riesgo de confusión: aparecen bajo el mismo badge "Ollama". Decisión pendiente: limpiarlos para que "Ollama" sea estrictamente local (recomendado) |
| Phi-4 Mini / Qwen3 4B (Q4) | 🔶 Candidatos para batch | ~8-12 tok/s estimados en i7-8665U según benchmarks **externos, sin medición propia**. Viables para batch nocturno, no para agente interactivo |
| Modelos >16B | ❌ Fuera de alcance en CPU | No caben o son inutilizables |

### Indexado (para el motor de búsqueda, aún sin decidir)

Meilisearch (Rust, favorito) · Typesense · Whoosh · ~~Elasticsearch~~ (overkill personal).

---

## 4 · Código, scripts y configs existentes

> Ninguno de estos vive dentro de `mi-criterio` (D8). Rutas absolutas del sistema `fibonacci`.

| Ruta | Contenido | Estado |
|---|---|---|
| `~/.aider.conf.yml` | `model/weak-model/editor-model: ollama/deepseek-coder:6.7b`, `map-tokens: 128`, `map-refresh: manual`, `no-analytics`, `no-auto-commits`, `no-suggest-shell-commands` | Vigente, pero Aider bloqueado |
| `~/Codes/mi-criterio/.aider.conf.yml` | Carga `.claude/CLAUDE.md` + `perfil_maestro_eldaniels_v2.txt` como read-only por sesión | Versionado en el repo |
| `~/.zshrc:115-144` | **Switcher Alt+P** — `_ollama_switch_model()`, widget ZLE con `fzf`, exporta `OLLAMA_MODEL` | ⚠️ **Roto/desincronizado**: lista `qwen2.5-coder:7b` (default) y `:1.5b`, ninguno existe ya |
| `~/.zshrc:165-168` | `OLLAMA_HOST=127.0.0.1:11434`, `OLLAMA_API_BASE`, `OLLAMA_KEEP_ALIVE=30m`, `OLLAMA_NUM_THREAD=8` | ⚠️ Solo aplican a shells con `.zshrc` cargado — **no** al servicio systemd |
| `/etc/systemd/system/ollama.service.d/override.conf` | Env vars persistentes del servicio | ❌ **No existe** — pendiente de crear |
| `~/.config/opencode/opencode.jsonc` | Providers y modelos del selector | ✅ Existe (OpenCode instalado; config viva en `jsonc`, D8 cumplida) |
| `inbox/02-08-26` → `verificar_feeds.py`, `gdelt_contraste.py`, `fuentes_contraste.opml` | Scripts del proyecto de noticias (capa 1-2); la capa 3 los conectaría al LLM local | Generados, **no ejecutados con red real** |

### Documentos fuente en el repo

| Archivo | Rol |
|---|---|
| `proyectos/P2/stack_ia_local_veredicto.md` | **Bitácora + veredicto honesto**. Hito 2026-05-18, tabla local-vs-rentado, path de upgrade |
| `proyectos/P2/Plan: Stack IA local privado completo para CPU-only (3 workflows).txt` | Plan por fases 0-3 con verificación end-to-end |
| `inbox/26-05-26_modelos-locales-llm-mi-criterio.md` | 🔴 **Borrado en consolidación 53a7ec8 — contenido del marco conceptual (cuantización FP16→Q4, distillation, modelos ligeros) NO localizado en ningún canónico actual.** Recuperable: `git show 53a7ec8^:inbox/26-05-26_modelos-locales-llm-mi-criterio.md` — re-fusionar si se reabre el tema |
| `inbox/06-08-26_local-core-ui-opencode.md` | Plan OpenCode fases 0-7 — **absorbido en §7 de este doc** (Bloques A–F; borrado en 53a7ec8) |
| `proyectos/P2/arquitectura_noticias_sin_sesgo.md` | Escalera de inversión de 4 niveles + benchmarks estimados |
| `memory/project_personal_search_engine_with_llm.md` | Motor de búsqueda personal (parked) |

---

## 5 · Limitaciones de hardware identificadas

### La máquina

**Dell Latitude 5400 "fibonacci"** · i7-8665U (4C/8T, ULV) · 31 GB RAM · Intel UHD 620 (iGPU, sin uso para inferencia) · sin GPU dedicada · Arch Linux + COSMIC · root 49 GB, 21 GB libres.

### Cuellos de botella (en orden de impacto)

1. **Ancho de banda de RAM, no núcleos.** El i7-8665U es ULV y no tiene AVX-512. Agregar hilos no compra velocidad lineal — el modelo espera datos de memoria.
2. **Sin GPU utilizable.** La UHD 620 no es ruta viable de inferencia. CPU-only es el techo.
3. **Latencia: 30 s – 2 min por respuesta** con `deepseek-coder:6.7b`. Aceptable para trabajo reflexivo; frustrante para iteración rápida.
4. **Ventana de contexto.** Modelos 7B manejan bien ~8-16k tokens vs 200k de Claude → conversaciones largas o repos grandes se olvidan antes.
5. **Los agentic loops son el caso peor.** 10+ rondas autónomas × 30-120 s cada una = inutilizable. El deadlock de Aider probablemente es esto agravado por la orquestación de litellm.
6. **Disco frágil.** Historial de *disk-full incident* que dejó manifests de Ollama corruptos (modelos visibles en `ollama list` pero `ollama rm` decía "not found"). Cada modelo nuevo son GB.

### Lo que SÍ funciona en este hardware

Chat general y brainstorming · RAG sobre `mi-criterio` · escritura/traducción/resumen · código corto (1 archivo, <100 líneas) · **offline 100%, cero telemetría, todo `localhost`**.

### Lo que NO

Refactor multi-archivo (solo con mucha paciencia) · debugging sutil de race conditions · arquitectura de sistema completo · edición agéntica del repo en vivo · respuestas en tiempo real estilo Claude Code.

---

## 6 · Estado real verificado hoy (2026-08-09)

> ⚠️ **Leer esto antes que cualquier plan**: los documentos de mayo describen un stack que ya no coincide con la máquina. Verificado en vivo, no asumido.

| Componente | Documentado | Realidad hoy |
|---|---|---|
| `ollama.service` | activo | ✅ activo (servicio **de sistema**, no `--user`) |
| Versión Ollama | 0.32.6 | ⚠️ servidor **0.32.1**, cliente 0.32.6 — *drift de versión* |
| Modelos locales | 4 (2× qwen, deepseek, nomic) | ⚠️ **2**: `deepseek-coder:6.7b`, `nomic-embed-text` |
| Modelos extra | — | ⚠️ `deepseek-v4-flash:cloud` y `:0731-cloud` = **proxies de Ollama Cloud, no locales** |
| Open WebUI | "frontend actual" | ⚠️ instalado (uv, v0.9.5) pero **no corriendo**, :8080 sin respuesta |
| Aider | instalado | ✅ instalado (uv, v0.86.2), bloqueado por timeout |
| OpenCode | elegido como base | ✅ instalado (1.18.25-1) — **superado: ver §10** |
| Switcher Alt+P | funcional | ⚠️ **roto** — apunta a 3 modelos, 2 no existen |
| `OLLAMA_*` env vars | aplicadas | ⚠️ solo en shells zsh; el servicio systemd **no las ve** |

**Traducción:** el estado agéntico real hoy es **cero**. Hay un chat local funcional (`deepseek-coder:6.7b` vía `ollama run`) y nada más levantado.

---

## 7 · Pendientes y próximos pasos

### Bloque A — Reconciliar el estado (30-45 min, hacer primero)

- [ ] `ollama pull qwen2.5-coder:1.5b` — **necesario**: es el único modelo local con capability `tools` para probar el agent loop
- [x] Decidir sobre los `*-cloud`: eliminarlos para que "Ollama" sea estrictamente local — **hecho 2026-08-27**, ver §9
- [ ] Resolver el drift de versión servidor/cliente de Ollama (`pacman -Syu` + `systemctl restart ollama`)
- [ ] Crear `/etc/systemd/system/ollama.service.d/override.conf` con `OLLAMA_KEEP_ALIVE`, `OLLAMA_NUM_THREAD=8`, `OLLAMA_CONTEXT_LENGTH=16384`; retirar los exports duplicados de `~/.zshrc`
- [ ] Arreglar o retirar el switcher Alt+P (`~/.zshrc:115-144`) — hoy es deuda silenciosa que contradice "minimal"

### Bloque B — Validar la capa agéntica (el paso de mayor riesgo)

- [ ] `sudo pacman -Si opencode` → confirmar firma y mantenedor · **verificar si el repo autoritativo es `sst/opencode` o `anomalyco/opencode`** (el paquete de Arch apunta al segundo) — sin resolver
- [ ] `sudo pacman -S opencode` (**no** `opencode-bin` de AUR: desactualizado y activaría el protocolo de revisión de PKGBUILD sin necesidad)
- [ ] Configurar provider `@ai-sdk/openai-compatible` → `http://127.0.0.1:11434/v1` en `~/.config/opencode/opencode.json`
- [ ] **Prueba crítica** en directorio desechable (`/tmp`, NO `mi-criterio`), con `qwen2.5-coder:1.5b`:
      `"lee README.md y dime cuántas líneas tiene"` → `"crea test.txt con 'hola' y léelo de vuelta"`
      **Criterio de éxito:** ejecuta en <60 s, sin timeout/deadlock estilo Aider
- [ ] **Si falla igual que Aider → DETENERSE.** Investigar `num_ctx` adicional o el adapter nativo de Ollama antes de invertir un minuto más en personalización

### Bloque C — Después de que B pase (y solo entonces)

- [ ] Probar `opencode auth login -p anthropic` (Claude Pro/Max OAuth) · plan B: API key de `console.anthropic.com` con facturación aparte
- [ ] Investigar pricing vigente de DeepSeek (`platform.deepseek.com`) y Kimi/Moonshot (`platform.moonshot.ai`) — **nunca de memoria**
- [ ] Selector visual con costo/token y badge local-vs-cloud (truco sin fork: inyectar el dato en el campo `"name"` de cada modelo)
- [ ] Reescribir Alt+P para lanzar `opencode` con el modelo elegido, en vez de golpear Open WebUI en :8080
- [ ] Retirar Open WebUI del uso activo (no desinstalar — dejarlo como fallback de chat puro)

### Bloque D — Deuda de mayo, aún abierta

- [ ] Crear knowledge collection `mi-criterio-test` en Open WebUI con 5-10 archivos clave
- [ ] Validar RAG: *"¿cuáles son mis empresas objetivo en energía?"* → ¿cita `perfil_maestro_eldaniels_v2.txt` correctamente?
- [ ] Documentar 5-10 prompts útiles (qué funciona, qué no)
- [ ] **Diario de uso**: cada vez que se use el local en lugar de Claude, anotar tarea + satisfacción (1-5). Es la evidencia que justifica (o no) el Nivel 1 de inversión
- [ ] Investigar el timeout de Aider cuando haya GPU

### Bloque E — Medición y hardware (P4 × BBB)

- [ ] **Medir tok/s reales** en el i7-8665U con Phi-4 Mini o Qwen3 4B Q4 — los números de 8-12 tok/s son de fuentes externas, sin medición propia
- [ ] Decidir budget y timeline del Nivel 1 (~$300-500, mini PC iGPU) — **post primer ingreso digital activo**, y solo si el diario de uso demuestra uso diario real
- [ ] Considerar Nivel 3 (RunPod/vast.ai por hora) como puente antes de comprar

### Bloque F — Motor de búsqueda personal (parked, depende de todo lo anterior)

- [ ] Stack: Ollama (inferencia) + Meilisearch (indexado) + agente custom
- [ ] Prototipo: indexar top 100 sitios confiables
- [ ] Integración Firefox: OpenSearch XML → barra de búsqueda
- [ ] Medir latencia vs calidad

---

## 8 · Regla de oro para quien retome esto

1. **Verificar en vivo antes de leer docs viejos.** Este proyecto ya generó drift dos veces (modelos borrados, Open WebUI apagado, Alt+P desincronizado).
2. **El deadlock de Aider es el riesgo #1.** Cualquier herramienta agéntica nueva sobre Ollama CPU-only debe probarse contra ese mismo escenario **antes** de invertir en configurarla.
3. **Nada de config ni secretos dentro de `mi-criterio`.** Es repo de conocimiento.
4. **No subir de peldaño de hardware sin evidencia de uso diario.** Criterio BBB.

---

## 9 · Actualización 2026-08-27 — fix Alt+P, limpieza Ollama Cloud, "Openclaw" aclarado

**Estado global sigue igual:** OpenCode elegido en D7 sigue **sin instalar**. Esta sesión fue diagnóstico de config drift, no avance en Bloque B.

**Aclaración de nombre:** "Openclaw" (paquete npm `openclaw@2026.7.1-2`, gateway multi-canal de bots IA, requiere Node ≥24.15.0, falló por mismatch de versión con Node v24.14.1 instalado) **NO es** la herramienta decidida en D7. La decidida es **OpenCode** (MIT, `pacman -S opencode`, Arch `extra/`). Mismo patrón de riesgo de typosquatting ya documentado en `recursos/AUR_Atomic_Arch_2026_Informe.md` — se optó por no instalar nada hasta confirmar el nombre correcto. Decisión del usuario: *"no hacer nada por ahora"* con openclaw.

**Fix aplicado (este repo):** `.claude/settings.json` tenía `"model": "default"` — string no reconocida por el picker de Claude Code, generaba entrada fantasma "Custom model" en el selector Alt+P en vez de heredar el modelo global. Se eliminó la línea (`git diff --stat`: `.claude/settings.json | 1 -`). Alt+P ahora hereda correctamente (checkmark en "Default ✓ Sonnet 5"); queda un residuo cosmético no bloqueante en el slot 6 del picker (entrada "default" sin check), causa no rastreada.

**Modelos `*-cloud` de Ollama:** confirmados como proxies remotos de Ollama Cloud (`deepseek-v4-flash:cloud`, `:0731-cloud`, 304B params FP8 — imposible correr en 32GB RAM, por eso eran remotos). Decisión pendiente del Bloque A ("decidir sobre los `*-cloud`") **ya ejecutada por el usuario entre sesiones**: `ollama list` post-limpieza solo muestra `nomic-embed-text` y `deepseek-coder:6.7b` — "Ollama" es estrictamente local de nuevo.

**Nuevo hallazgo — env var inconsistente:** `OLLAMA_MODEL=qwen2.5-coder:7b` sigue exportado mientras ese modelo no está instalado (`ollama list` no lo muestra). Pendiente: reinstalar `qwen2.5-coder:7b` o cambiar la env var a `qwen2.5-coder:1.5b` (candidato ya identificado en Bloque A para probar tool-use).

**NOMAD (Crosstalk-Solutions/project-nomad) evaluado y no adoptado:** Apache 2.0 (permisivo, no copyleft — tensión con principio declarado), stack Docker pesado (Kiwix+Kolibri+ProtoMaps+Qdrant+CyberChef+FlatNotes), hardware recomendado (RTX 3060+, 32GB) muy por encima del actual. Componentes de conocimiento (Kiwix/Qdrant) sí aplican conceptualmente; el LLM local del stack no es viable en fibonacci hoy. Ver también evaluación en `recursos/Herramientas_IA_Evaluadas.md` (open-notebook es alternativa más ligera para RAG personal, self-hosted, SurrealDB).

**Decisión reafirmada:** no fusionar Claude Code con el stack local vía proxy (`ANTHROPIC_BASE_URL`) — rompería open source/private/minimal sin ganar nada que un stack local independiente no dé ya. Mantener sistemas separados.

**Datos duros de la sesión:**
```
ollama list (tras limpieza):
NAME                       ID              SIZE      MODIFIED
nomic-embed-text:latest    0a109f422b47    274 MB    4 months ago
deepseek-coder:6.7b        ce298d984115    3.8 GB    4 months ago

env vars activos:
OLLAMA_MODEL=qwen2.5-coder:7b   [modelo NO instalado — inconsistente]
OLLAMA_HOST=127.0.0.1:11434
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_KEEP_ALIVE=30m
OLLAMA_NUM_THREAD=8
```

**Nota cross-lens (P7):** decisión pendiente sobre si retomar el ángulo "expansión de consciencia" al reabrir esta línea — priorizar RAG sobre el propio repo (corpus de decisiones propias) por encima de replicar un stack de conocimiento genérico tipo NOMAD.

**Regla de oro añadida:** `ollama list` con columna SIZE en `-` (0 bytes) = modelo remoto, el prompt sale de la máquina. Verificar antes de asumir "local".

---

## 10 · Actualización 2026-09-05 — OpenCode instalado + referencia técnica Ollama

**OpenCode instalado y en uso activo.** `opencode 1.18.25-1` (pacman, repo `extra/`) corriendo en sesiones reales sobre modelos remotos. `~/.config/opencode/opencode.jsonc` existe (D8 cumplida: config fuera del repo). La verificación "¿`sst/opencode` o `anomalyco/opencode`?" del Bloque B sigue sin resolverse formalmente.

**Lo que SIGUE pendiente del Bloque B:**
- [ ] La **prueba crítica** de tool-use en `/tmp` (NO mi-criterio) con `qwen2.5-coder:1.5b` — el deadlock de Aider sigue siendo el riesgo #1.
- [ ] `ollama pull qwen2.5-coder:1.5b` — sigue sin reinstalarse (es el único modelo local con capability `tools`).
- [ ] Drift `OLLAMA_MODEL=qwen2.5-coder:7b` en `~/.zshrc` — modelo no instalado (`ollama list`: solo `deepseek-coder:6.7b` + `nomic-embed-text`).

**Referencia técnica Ollama** (del handoff OpenClaw 30-08-26 — conservada pese al descarte de la herramienta; aplica a cualquier harness sobre Ollama local):

- **Endpoint nativo `/api/chat`** (no el compatible `/v1`). Clave canónica `baseUrl` (no `baseURL`). Refs `ollama-cloud/` para separar nube de provider local `ollama`.
- **3 modos:** nube+local (host accesible + modelos `:cloud`), solo nube (`https://ollama.com`, requiere `OLLAMA_API_KEY` real), solo local.
- **Auth:** hosts locales/LAN (loopback, red privada, `.local`, hostname simple) → marcador `ollama-local` sin token real. Remotos → `OLLAMA_API_KEY` o perfil de auth. `auth-profiles.json` guarda solo la credencial; la config del endpoint (`baseUrl`, `api`, modelos, headers, timeouts) va en `models.providers.<id>`.
- **Auto-detección de modelos:** `/api/tags` (catálogo) + `/api/show` (capabilities: `contextWindow`, `num_ctx`, vision, thinking). Provider explícito con array `models` la **desactiva**; loopback personalizado (ej. `127.0.0.2:11434`) la mantiene. maxTokens default = límite máximo de Ollama; costes siempre 0.
- **Smoke tests aislados** (no cargan tools/memoria/contexto de sesión):
  ```bash
  OLLAMA_API_KEY=ollama-local \
  openclaw infer model run --local \
    --model ollama/llama3.2:latest \
    --prompt "Responde exactamente: pong" --json
  # visión: --file ./photo.jpg (PNG/JPEG/WebP; no-imágenes se rechazan)
  ```
  **Criterio reutilizable en la prueba crítica de OpenCode:** si el smoke test pasa y el agente falla → el problema es tool-use del modelo, no el endpoint.
- **Cron aislado:** verifica `/api/tags` antes de cada turno si el modelo resuelve a provider Ollama local/privado; fallo → turno `skipped`. Cache de la verificación: 5 min por host.
- **Onboarding:** `openclaw onboard` (interactivo) o `--non-interactive --auth-choice ollama --custom-base-url "http://host:11434" --custom-model-id "..." --accept-risk`. La comprobación automática nunca descarga modelos.
- **Modo nube+local:** requiere `ollama signin` para habilitar modelos `:cloud`; con sesión iniciada sugiere `kimi-k2.5:cloud`, `minimax-m2.7:cloud`, `glm-5.1:cloud`, `glm-5.2:cloud`. Sin sesión: permanece en modo local.
- **Resolución runtime:** referencia `ollama/<modelo>:latest` sin entrada manual en `models.json` se resuelve en runtime; en hosts con sesión iniciada, una referencia `:cloud` no listada se valida vía `/api/show` y se agrega al catálogo solo si Ollama confirma metadata.
- **Verificación en vivo (self-hosted):**
  ```bash
  OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_OLLAMA=1 OPENCLAW_LIVE_OLLAMA_WEB_SEARCH=0 \
  pnpm test:live -- extensions/ollama/ollama.live.test.ts
  ```
  Nube: `OPENCLAW_LIVE_OLLAMA_BASE_URL=https://ollama.com` + `OPENCLAW_LIVE_OLLAMA_MODEL=glm-5.1:cloud` + `OPENCLAW_LIVE_OLLAMA_WEB_SEARCH=1`. Embeddings omitidos por default (forzar con `OPENCLAW_LIVE_OLLAMA_EMBEDDINGS=1` — una key de nube puede no autorizar `/api/embed`).

**Hallazgo 🔴 (consolidación anterior, no este lote):** `inbox/26-05-26_modelos-locales-llm-mi-criterio.md` (479 líneas, marco conceptual de cuantización) fue borrado en `53a7ec8` y su contenido no se localiza en ningún canónico actual (búsqueda `FP16`/`Q4`/`distill` = 0 resultados fuera de la fila pointer de §4). Recuperable vía `git show 53a7ec8^:inbox/26-05-26_modelos-locales-llm-mi-criterio.md` — re-fusionar en `Plan_Stack IA local privado completo para CPU-only (3 workflows).txt` si se reabre el tema de modelos.

---

## 11 · Actualización 2026-09-06 — Bloque B ejecutado: la prueba crítica FALLA (tool-calling no real)

**Q1 drift resuelto:** `OLLAMA_MODEL` en `~/.zshrc` apunta ahora a `deepseek-coder:6.7b` (instalado), no al fantasma `qwen2.5-coder:7b`. El switcher Alt+P se reordenó: 6.7b como principal, 7b marcado `(no instalado)`.

**Q2 ejecutado — proveedor local configurado:** `ollama pull qwen2.5-coder:1.5b` (986 MB, único modelo local con capability `tools`) + provider `ollama` añadido a `~/.config/opencode/opencode.jsonc` (npm `@ai-sdk/openai-compatible`, baseURL `http://localhost:11434/v1`, modelos `qwen2.5-coder:1.5b` y `deepseek-coder:6.7b`). Ambos visibles en `opencode models`.

**🔴 Resultado de la prueba crítica (criterio de éxito NO cumplido):**

1. `opencode run -m ollama/qwen2.5-coder:1.5b "lee README.md y dime cuántas líneas tiene"` en `/tmp` → **colgado >180 s** consumiendo CPU (llama-server al 347 %, sin respuesta). Hubo que matar el proceso; mismo patrón deadlock que Aider. El `--print-logs` mostró además ~55 warnings de skills duplicadas inflando el system prompt.
2. **Test aislado de tool-use** (sin harness, endpoint `/v1/chat/completions` con `tools` declarado) → el modelo **NO emite `tool_calls` estructurados**: `finish_reason: stop`, devuelve el JSON como `content` (`{"name": "count_lines", "arguments": {"path": "README.md"}}`). Con `num_ctx: 16384` idem.
3. Endpoint nativo `/api/chat` → igual: JSON en `content`, sin `tool_calls`.
4. `deepseek-coder:6.7b` **rechaza payload con tools** (HTTP 400) — su capability es solo `['completion']`.
5. Velocidad real en el i7-8665U (datos medidos, no de fuente externa): prompt-eval ~**8.6 tok/s**, generación ~**4.2 tok/s** (qwen2.5-coder:1.5b). El system prompt agéntico de opencode (miles de tokens con tools/skills) solo en prompt-eval tardaría minutos — inviable en este hardware.

**Conclusión (regla de oro #2 y Bloque B):** la capa agéntica de OpenCode sobre Ollama local **no es viable con los modelos actuales en este hardware**. `qwen2.5-coder:1.5b` *declara* capability `tools` pero no hace tool-calling real (emite texto con forma de JSON, no llamadas estructuradas), y el throughput CPU-only no sostiene el contexto de un agente. **DETENERSE antes de personalizar nada** — exactamente lo que pedía el Bloque B. No es un problema del endpoint ni del harness (el endpoint crudo responde en ~5 s), es del modelo + hardware.

**Estado de los ítems:**
- [x] `ollama pull qwen2.5-coder:1.5b` (Bloque A)
- [x] Configurar provider `ollama` local en opencode (Bloque B)
- [x] Prueba crítica tool-use en `/tmp` → **FALLA** (Bloque B, criterio no cumplido)
- [x] Fix drift `OLLAMA_MODEL` (zshrc)
- [ ] Bloque C — queda bloqueado aguas arriba mientras no haya un modelo local con tool-calling real o GPU (el diario de uso y Nivel 1 siguen supeditados a esto)
- [ ] `OLLAMA_KEEP_ALIVE`/`OLLAMA_NUM_THREAD`/`OLLAMA_CONTEXT_LENGTH` vía systemd override + retirar exports duplicados de zshrc (Bloque A) — ahora de bajo valor mientras no haya agente local

**Candidato a reconsiderar cuando haya GPU/hardware:** modelos con tool-calling nativo fiable en CPU serían qwen2.5-coder:7b (no probado por costo de RAM/CPU) o qwen3; medición de tok/s en §Bloque E queda como tarea pendiente con hardware mejor.

---

## Próximo hito a registrar

Añadir a `stack_ia_local_veredicto.md` una entrada `## Hito YYYY-MM-DD — título corto` en cuanto la Fase 3 (validación de tool-use en OpenCode) dé resultado — pase o falle. El fallo también es información.
