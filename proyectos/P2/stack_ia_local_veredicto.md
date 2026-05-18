# Stack IA Local Privado — Bitácora y Veredicto

> **Propósito:** documentar la construcción, decisiones y estado del stack IA local propio. No quiero perder el hilo de esta herramienta que estoy desarrollando. Este archivo crece con cada milestone.

---

## Hito 2026-05-18 — Open WebUI vivo, primer chat exitoso

### Lo que tengo funcionando hoy
- **Ollama** corriendo en `127.0.0.1:11434`
  - `OLLAMA_KEEP_ALIVE=30m` — modelo se queda caliente en RAM
  - `OLLAMA_NUM_THREAD=8` — usa los 8 cores del i7-8665U
- **Modelo principal: `deepseek-coder:6.7b`** (3.8 GB)
  - Confirmado: responde chat vía Open WebUI
  - Latencia observada: 30s-2min por respuesta
- **`nomic-embed-text`** instalado (274 MB) — para RAG futuro
- **Open WebUI v0.9.5** en `http://localhost:8080`
  - Instalado vía `uv tool install open-webui`
  - Fix aplicado: `audioop-lts` para Python 3.13 (pydub no encuentra módulo `audioop`)
- **Aider** instalado pero bloqueado: timeout litellm 600s sistemático aún con `map-tokens: 128`. Deprioritizado, ruta principal ahora es Open WebUI.

### Hardware
Dell Latitude 5400 · i7-8665U · 32 GB RAM · sin GPU · Arch Linux (COSMIC) · ~13 GB libres en root tras limpieza.

### Configs clave
- `~/.aider.conf.yml` — apunta a `ollama/deepseek-coder:6.7b`, `map-tokens: 128`, sin auto-commits
- `~/Codes/mi-criterio/.aider.conf.yml` — carga `perfil_maestro_eldaniels_v2.txt` y `.claude/CLAUDE.md` como read-only por sesión
- `~/.zshrc` — bloque Ollama con `OLLAMA_HOST`, `OLLAMA_API_BASE`, `OLLAMA_KEEP_ALIVE`, `OLLAMA_NUM_THREAD`

### Modelos eliminados del plan activo
- `deepseek-coder-v2:16b` — MoE 16B, 2-10 min/respuesta en CPU = no workflow. Liberó 8.9 GB.
- `qwen2.5-coder:1.5b` — redundante con 6.7b. Liberó ~1 GB.

---

## Veredicto honesto (la pregunta que me importa)

> *"¿Esto significa que ya no tengo que rentar IA agéntica a terceros? ¿Puedo trabajar con esto en un avión sin wifi?"*

### Sí, funciona offline 100%
En avión, sin wifi, sin VPN. Todo es `localhost`. Cero telemetría, cero API keys, soberanía real.

### Pero no es equivalente a Claude Code. Cuatro matices:

1. **No es agéntico.**
   Los LLMs locales vía Ollama no ejecutan herramientas reales: no leen archivos por sí solos, no corren comandos, no editan código. Open WebUI te da chat + RAG, no un agente que actúa sobre tu sistema.

2. **Calidad de razonamiento.**
   `deepseek-coder:6.7b` ≈ GPT-3.5 en buen día. Claude Opus / Sonnet 4 están 2-3 generaciones arriba en:
   - Razonamiento complejo
   - Código multi-archivo
   - Síntesis larga
   - Debugging sutil

   Para tareas simples-medias: suficiente. Para arquitectura compleja: notarás el techo.

3. **Velocidad.**
   CPU-only = 30s-2min por respuesta. Aceptable para trabajo reflexivo, frustrante para iteración rápida.

4. **Contexto.**
   Modelos 7B manejan bien ~8-16k tokens. Claude maneja 200k. Conversaciones largas o repos grandes → el local olvida antes.

### Tabla de decisión

| Tarea | Local (6.7b) | Claude rentado |
|---|---|---|
| Chat general, brainstorming | ✅ Suficiente | Lujo |
| Q&A sobre mi-criterio (RAG) | ✅ Adecuado | Lujo |
| Escritura, traducción, resúmenes | ✅ Sí | Lujo |
| Código corto (1 archivo, <100 líneas) | ✅ Sí | Lujo |
| Refactor multi-archivo | ⚠️ Con paciencia | ✅ Donde brilla |
| Debugging sutil de race conditions | ❌ Techo evidente | ✅ |
| Arquitectura de sistema completo | ❌ | ✅ |
| Edición agéntica del repo en vivo | ❌ No hace | ✅ Claude Code |

### Punto ciego [!]
La tentación es decir *"ya no necesito pagar por IA"*. La realidad pragmática:
- **Ahorras** en tareas que el local cubre bien (chat, RAG personal, código simple)
- **Reservas** la IA rentada para los momentos donde el salto de calidad justifica el costo
- **No es uno-u-otro, es un stack híbrido**

### Filosofía operativa
La soberanía no está en abandonar lo rentado. Está en **TENER la opción local funcionando** para:
- Privacidad cuando importa (datos personales, código sensible, exploración filosófica)
- Independencia cuando no hay wifi (avión, viajes, cortes de red)
- Costo cero para tareas repetitivas y de alto volumen
- Garantía de que si mañana sube el precio de Claude 5x, no me quedo en cero

---

## Path de upgrade futuro (zero-migration software)

Cuando haya budget para GPU:
- **Setup:** eGPU TB3 (caja Thunderbolt 3) + RTX 3060 12GB usada (~$500 USD total)
- **Ganancia esperada:** 10-15x speedup en latencia
- **Cambio en software:** una línea (`model:` en `.aider.conf.yml` y Open WebUI ajusta solo)
- **Modelos que se vuelven viables:**
  - `qwen2.5-coder:32b` — top tier coding open
  - `deepseek-r1:14b` — razonamiento estilo o1
  - `deepseek-coder-v2:16b` — vuelve al menú

Mismo Ollama, mismo Open WebUI, misma config. Por eso este stack es la apuesta correcta hoy.

---

## Por qué Aider quedó deprioritizado (no eliminado)

Timeout sistemático `litellm.Timeout: 600s` aún cuando `ollama run` directo responde en 48s. Es un deadlock entre Aider/litellm y Ollama en CPU-only, no un problema de velocidad. Hipótesis: orchestration de litellm hace muchas requests pequeñas que saturan el endpoint.

**Decisión:** ruta principal = Open WebUI. Aider queda para investigar después o cuando upgrade a GPU lo haga irrelevante (con GPU las requests serán suficientemente rápidas para no deadlock).

---

## Próximos pasos (no perderlos)

- [ ] Crear knowledge collection `mi-criterio-test` en Open WebUI con 5-10 archivos clave (perfil_maestro + 2-3 P*)
- [ ] Validar workflow RAG: ¿"¿cuáles son mis empresas objetivo en energía?" cita fuentes correctamente?
- [ ] Expandir collection con el resto del repo si el primer test funciona
- [ ] Documentar 5-10 prompts útiles que pruebo (qué funciona, qué no)
- [ ] Diario de uso: cada vez que uso el local en lugar de Claude, anotar tarea + satisfacción (1-5)
- [ ] Decidir budget eGPU + timeline (post primer ingreso digital activo)
- [ ] Investigar timeout Aider cuando haya GPU

---

## Bitácora futura

> Añadir entradas con formato `## Hito YYYY-MM-DD — título corto` cada vez que pase algo importante: nuevo modelo, problema resuelto, decisión de arquitectura, hito de uso real.

