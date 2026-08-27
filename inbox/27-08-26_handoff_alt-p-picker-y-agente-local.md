# 27-08-26 — Fix picker Alt+P + retomar agente local (OpenCode) + auditoría Ollama Cloud

**Fecha de corte:** 2026-08-27 · **Herramienta:** Claude Code
**Lente(s):** P2 (programación/agente local) principal × P8 (seguridad/config)
**Estado global:** 🟡 parcial

---

## 1 · Objetivo y motivación

**Objetivo:** diagnosticar por qué el selector Alt+P mostraba "default" como modelo custom en vez de heredar el modelo global, y retomar la decisión pendiente del stack de LLM agéntico local (P2) — específicamente confirmar el estado de Aider/OpenCode y descartar exposición accidental a modelos cloud vía Ollama.

**Motivación — por qué, no sólo qué:** Alt+P mostraba una entrada "Custom model" no explicada, y `ollama list` tenía dos modelos `deepseek-v4-flash` marcados `:cloud` con 0 bytes en disco — riesgo directo contra los principios declarados (`safe · private · stable · open source · copyleft · minimal · clean`), ya que esos modelos reenvían prompts a servidores de Ollama sin que quedara explícito en ningún doc.

| Driver | Detalle |
|---|---|
| Config drift | `.claude/settings.json` del proyecto forzaba `"model": "default"`, string no reconocida por el picker, generando entrada fantasma |
| Riesgo de privacidad | Dos modelos Ollama `:cloud` registrados (uno usado hace 3 meses) sin marcarlos como salida de red |
| Continuidad P2 | Sesión previa (09-ago) dejó OpenCode como siguiente paso, nunca instalado; usuario recordaba el nombre mal ("Openclaw") |

---

## 2 · Estado real verificado al cerrar

| Componente | Estado | Verificado cómo |
|---|---|---|
| `.claude/settings.json` (mi-criterio) sin `"model": "default"` | ✅ | `git diff --stat` → `.claude/settings.json \| 1 -`; Edit aplicado línea 3 |
| Alt+P hereda modelo global correctamente | 🟡 | Screenshot post-fix: checkmark ahora en "1. Default (recommended) ✓ Sonnet 5" (antes estaba en slot 6 "Custom model"). Slot 6 sigue listando "default" sin check y sin descripción — entrada fantasma residual, no bloqueante, causa no identificada (probable caché en `~/.claude.json` fuera de `additionalModelOptionsCache`, no inspeccionado a fondo) |
| Modelos Ollama `:cloud` | ✅ removidos | `ollama list` en el turno de seguimiento del usuario ya no los muestra (solo `nomic-embed-text:latest` y `deepseek-coder:6.7b`). Ejecutado por el usuario fuera de esta sesión — comando exacto no capturado en transcript |
| `OLLAMA_MODEL=qwen2.5-coder:7b` (env var apunta a modelo no instalado) | 🔴 no resuelto | detectado, no corregido esta sesión |
| Causa histórica de fallo de Aider confirmada | ✅ | recuperado de memoria claude-mem (obs. 2661, 2669) + doc `proyectos/P2/HANDOFF_LLM_agentico_local.md`: `litellm.Timeout: 600s` sistemático en endpoint CPU-only, hipótesis = litellm satura con múltiples requests pequeños |
| Nombre correcto de la herramienta pendiente ("Openclaw") | ✅ aclarado | es **OpenCode** (MIT, repo `extra/` de Arch, login OAuth nativo con Claude Pro/Max) — nunca llegó a instalarse en la sesión del 09-ago ni en esta |

**Lo que NO quedó resuelto:**
- Entrada fantasma "default" en slot 6 del picker Alt+P — cosmética, causa raíz no rastreada, usuario decidió no perseguirla esta sesión
- `OLLAMA_MODEL` sigue apuntando a modelo ausente
- OpenCode sigue sin instalar — es el siguiente bloqueador real de la línea agéntica local
- No se escribió una regla explícita por escrito para el "trust boundary" de red (usuario declinó explícitamente: "no more vigilance")

---

## 3 · Archivos tocados — con ruta verificada

```
git diff --stat
 .claude/settings.json | 1 -
 1 file changed, 1 deletion(-)
```

| Ruta | Acción | Qué cambió y por qué |
|---|---|---|
| `.claude/settings.json` | modificado | Se eliminó línea `"model": "default",` — el picker no reconocía ese literal como alias válido y lo mostraba como "Custom model" en vez de heredar `opus`/default global |

**Cambios fuera del repo:**
- Dos modelos Ollama `:cloud` (`deepseek-v4-flash:cloud`, `deepseek-v4-flash:0731-cloud`) eliminados por el usuario entre turnos (`ollama rm` presumible, no capturado literal). Recomendado también `ollama signout` — no confirmado si se ejecutó.

---

## 4 · Evaluado y descartado

| Opción / intento | Veredicto | Razón |
|---|---|---|
| Registrar modelos Ollama descargados automáticamente en el picker Alt+P de Claude Code | ❌ descartado | Arquitectura no lo permite: el picker sólo enumera modelos Anthropic accesibles por la cuenta. No existe registro local editable. Único puente es `ANTHROPIC_BASE_URL` apuntando a un proxy — swap global, no aditivo, y rompe open source/private/minimal al meter un backend local dentro de un cliente closed-source |
| Replicar N.O.M.A.D. (Crosstalk-Solutions) tal cual | 🔶 evaluado, no adoptado | Verificado vía WebFetch: Apache 2.0 (permisivo, NO copyleft — tensión directa con principio declarado), stack Docker pesado (Kiwix+Kolibri+ProtoMaps+Qdrant+CyberChef+FlatNotes), hardware recomendado para IA (RTX 3060+, 32GB) muy por encima del hardware actual. Componentes de conocimiento (Kiwix/Qdrant) sí aplican; el LLM local del stack no es viable en hardware actual |
| Aider como agente local | ⚠️ bloqueado (confirmado en sesiones previas, no repetido esta sesión) | `litellm.Timeout: 600s` sistemático en CPU-only. Causa: litellm probablemente fragmenta en múltiples requests pequeños que saturan inferencia CPU |
| deepseek-coder:6.7b como modelo agéntico | ❌ descartado (confirmado previamente) | No declara capability `tools` en el manifest de Ollama — sólo sirve para chat plano, no para tool-use |
| OpenCode como siguiente harness agéntico | 🔶 evaluado, no adoptado aún | Seleccionado en sesión 09-ago por: MIT license, disponible en repo oficial Arch `extra/`, OAuth nativo con Claude Pro/Max (sin necesitar API key separada). Nunca instalado — sigue siendo el siguiente paso real |

**Suposiciones que resultaron falsas:**
- Que "auto-discover de modelos Ollama en Claude Code" era un problema de configuración — en realidad es una limitación arquitectónica del picker, no un flag faltante.
- Que los dos modelos Ollama Cloud eran modelos locales grandes ejecutándose en CPU — imposible (304B params FP8 ≈ 304GB, vs 32GB RAM disponibles); eran proxies remotos activos desde hace ~3 meses sin marcarlos como tal.

---

## 5 · Decisiones tomadas

- [x] Eliminar `"model": "default"` de `.claude/settings.json` del proyecto — *porque* rompía la herencia del modelo global sin dar ningún beneficio, sólo confundía el picker
- [x] Mantener Claude Code y el stack de LLM agéntico local como sistemas separados, no fusionarlos vía proxy — *porque* fusionar viola open source/private/minimal sin ganar nada que un stack local independiente no dé ya
- [x] No escribir una regla de "trust boundary" de red por ahora — *decisión explícita del usuario*: "no more vigilance"
- [x] mi-criterio repo confirmado como el corpus offline objetivo (no un corpus externo tipo Wikipedia/NOMAD) — el RAG debe indexar el propio repo, no reemplazarlo
- [ ] Decisión abierta — ¿instalar OpenCode ahora, o primero terminar la sesión pendiente de graphify (113 nodos débiles) y usar su output como fuente de contexto para el agente? No resuelto esta sesión.

**Punto ciego `[!]`:** el usuario diseñó arquitectura (NOMAD, proxy Claude Code↔Ollama) antes de medir throughput real del hardware — patrón ya documentado en el perfil maestro §02. Se hizo explícito en esta sesión y el usuario lo aceptó sin objeción.

---

## 6 · Siguientes pasos

1. [ ] Instalar OpenCode: `sudo pacman -S opencode` (Arch `extra/`) y correr `opencode auth login -p anthropic` para validar OAuth con la suscripción Claude existente
2. [ ] Probar tool-use real con OpenCode contra `qwen2.5-coder` (modelo que sí declara `tools`, no `deepseek-coder:6.7b`) — nota: `qwen2.5-coder:7b` está referenciado en `OLLAMA_MODEL` pero NO instalado (`ollama list` no lo muestra); habrá que decidir si se reinstala o se usa `qwen2.5-coder:1.5b` (mencionado en handoff previo como eliminado)
3. [ ] Retomar sesión de graphify pendiente (113 nodos débiles / edges INFERRED sin verificar) antes o en paralelo — decidir si su output alimenta el contexto del agente OpenCode
4. [ ] Corregir o eliminar `OLLAMA_MODEL=qwen2.5-coder:7b` del entorno (apunta a modelo ausente)
5. [ ] Verificar `ollama signout` efectivamente ejecutado y revisar `~/.ollama/config.json` (`integrations` key) por si queda credencial de cloud activa

**Bloqueadores:** ninguno externo — todo depende de que el usuario decida instalar OpenCode.
**Riesgo mayor:** que OpenCode tenga el mismo problema de saturación CPU que Aider al usar `qwen2.5-coder` para tool-use — probarlo con una tarea trivial antes de construir cualquier flujo encima.

---

## 7 · Regla de oro para quien retome esto

1. "Openclaw" = **OpenCode** (MIT, `pacman -S opencode`, Arch `extra/`) — no buscar un proyecto con ese nombre, no existe.
2. Antes de tocar Ollama Cloud de nuevo: `ollama list` con columna SIZE en `-` (0 bytes) = modelo remoto, prompt sale de la máquina. Verificar antes de asumir "local".
3. `deepseek-coder:6.7b` sirve para chat, NO para tool-use (sin capability `tools` en manifest). No reintentar como agente sin verificar capability primero.

---

## 8 · Datos duros a preservar

```
Hardware: Dell Latitude 5400, i7-8665U, CPU-only, 32GB RAM (perfil dice 32GB; handoff P2 previo dice "8GB+ disponibles" — posible discrepancia entre RAM total y RAM libre, no reconciliado)

ollama list (verificado tras limpieza, turno de seguimiento del usuario):
NAME                       ID              SIZE      MODIFIED
nomic-embed-text:latest    0a109f422b47    274 MB    4 months ago
deepseek-coder:6.7b        ce298d984115    3.8 GB    4 months ago

Modelos Ollama Cloud eliminados (antes presentes, verificados por ollama show):
deepseek-v4-flash:cloud         — arch deepseek4, 304,180,418,494 params, FP8, ctx 1,048,576
deepseek-v4-flash:0731-cloud    — mismo modelo, snapshot distinto

env vars activos (sesión):
OLLAMA_MODEL=qwen2.5-coder:7b   [modelo NO instalado — inconsistente]
OLLAMA_HOST=127.0.0.1:11434     [correcto — bind local, no expuesto a LAN]
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_KEEP_ALIVE=30m
OLLAMA_NUM_THREAD=8

git diff --stat (este repo, fin de sesión):
 .claude/settings.json | 1 -
 1 file changed, 1 deletion(-)

Docs fuente recuperados de memoria/repo:
- proyectos/P2/HANDOFF_LLM_agentico_local.md (handoff 09-ago, referencia de calidad)
- proyectos/P2/stack_ia_local_veredicto.md
- Observaciones claude-mem #2661, #2669 (14-ago) — verdicto Aider/deepseek-coder/OpenCode

Ollama config local:
~/.ollama/config.json → keys: integrations, last_model, last_selection [contenido no inspeccionado]
```

---

## 9 · Destino sugerido

**Doc canónico:** `proyectos/P2/HANDOFF_LLM_agentico_local.md` — fusionar ahí: actualizar sección de estado con "OpenCode aún no instalado, cloud models limpiados, causa Aider confirmada y archivada". Este handoff es continuación directa de ese doc, no un tema nuevo.
**Actualiza `perfil_maestro`:** no — nada cambió en identidad/stack declarado, sólo estado de un proyecto en curso.
**Código a extraer:** ninguno esta sesión (solo config + investigación).
**Insight cross-lens:** el objetivo declarado "expansión de consciencia" (P7/filosófico) aterrizó en una decisión P2 muy concreta — priorizar RAG sobre el propio repo (P2↔P6, corpus de decisiones propias) por encima de replicar un stack de conocimiento genérico tipo NOMAD. Vale la pena anotar en P6 si en el futuro se retoma el ángulo "expansión de consciencia" explícitamente.
