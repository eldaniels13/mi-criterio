# Handoff: OpenClaw ↔ Ollama

**Fuente:** página "Ollama - OpenClaw" (documentación OpenClaw)

## Endpoint y modos

- OpenClaw usa la API nativa de Ollama (`/api/chat`), **no** el endpoint compatible OpenAI (`/v1`).
- Tres modos de operación:

| Modo | Qué usa |
|---|---|
| Nube + local | Host de Ollama accesible con modelos locales + modelos `:cloud` (si hay sesión iniciada) |
| Solo nube | `https://ollama.com` directo, sin daemon local (provider dedicado `ollama-cloud`) |
| Solo local | Host de Ollama accesible, solo modelos locales |

- Clave de configuración canónica: `baseUrl` (se acepta `baseURL` por compatibilidad, pero usar `baseUrl` en configs nuevas).
- Usar referencias `ollama-cloud/` para separar el enrutamiento de nube de un provider local `ollama`.

## Autenticación

- **Hosts locales/LAN** (loopback, red privada, `.local`, hostname simple): no requieren token real → OpenClaw usa el marcador `ollama-local`.
- **Hosts remotos / Ollama Cloud**: requieren credencial real vía `OLLAMA_API_KEY`, perfil de auth, o `apiKey` del provider. Para uso alojado directo se recomienda el provider `ollama-cloud`.
- **Providers personalizados** con `api: "ollama"` siguen las mismas reglas (ej. `ollama-remote` apuntando a LAN puede usar `apiKey: "ollama-local"`).
- `memory.search.provider` puede apuntar a un provider id personalizado para que los embeddings usen ese endpoint.
- **Perfiles de auth** (`auth-profiles.json`): guardan solo la credencial; la config del endpoint (`baseUrl`, `api`, modelos, headers, timeouts) va en `models.providers.<id>`.
  - Formato plano antiguo (`{"ollama-windows": {"apiKey": "ollama-local"}}`) no es válido en runtime → `openclaw doctor --fix` lo reescribe como perfil canónico `ollama-windows:default` (con backup).
- **Scope de embeddings de memoria**: la clave de un provider solo se envía a su host; `OLLAMA_API_KEY` puro se trata como convención de Ollama Cloud y no se envía a hosts locales por defecto.

## Primeros pasos

### Onboarding (recomendado)
```bash
openclaw onboard
```
- Elegir Ollama → modo (Nube+local / Solo nube / Solo local).
- OpenClaw verifica el host default/configurado; solo ofrece auto-selección de modelo instalado si `/api/show` confirma soporte de herramientas y contexto ≥16K.
- La comprobación automática nunca descarga modelos.

**Selección de modelo:**
- *Solo nube*: pide `OLLAMA_API_KEY`, sugiere defaults alojados.
- *Nube+local* / *Solo local*: pide base URL, detecta modelos disponibles, descarga el modelo local elegido si falta.
- Tags `:latest` no se duplican en el listado.

**Verificar:**
```bash
openclaw models list --provider ollama
```

**No interactivo:**
```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --custom-base-url "http://ollama-host:11434" \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk
```

### Configuración manual
```bash
ollama pull gemma4
export OLLAMA_API_KEY="ollama-local"   # host local/LAN
# export OLLAMA_API_KEY="your-real-key"  # solo https://ollama.com

openclaw models list
openclaw models set ollama/gemma4
```
O vía config:
```json5
{ agents: { defaults: { model: { primary: "ollama/gemma4" } } } }
```

### Nube + Local
- Enruta modelos locales y `:cloud` mediante un único host accesible.
- Pide base URL, detecta modelos locales, verifica estado de `ollama signin`.
- Con sesión iniciada sugiere: `kimi-k2.5:cloud`, `minimax-m2.7:cloud`, `glm-5.1:cloud`, `glm-5.2:cloud`.
- Sin sesión: permanece en modo local hasta ejecutar `ollama signin`.

### Solo nube (sin daemon local)
```bash
openclaw onboard --auth-choice ollama-cloud
openclaw models set ollama-cloud/kimi-k2.5:cloud
```
- Lista de modelos cloud obtenida en vivo de `ollama.com/api/tags` (límite 500 entradas).
- Si no hay acceso a ollama.com, recurre a lista codificada de sugerencias.

## Detección automática de modelos

Se activa cuando hay `OLLAMA_API_KEY`/perfil de auth y **no** hay `models.providers.ollama` ni provider personalizado `api:"ollama"` definido. Consulta `http://127.0.0.1:11434`:

- **Catálogo**: `/api/tags`
- **Capacidades**: `/api/show` (best-effort) → `contextWindow`, `num_ctx`, visión/herramientas/razonamiento
- **Visión**: capacidad `vision` → `input: ["text","image"]`
- **Razonamiento**: capacidad `thinking`; si falta, heurística por nombre (`r1`, `reason`, `reasoning`, `think`). `glm-5.2:cloud` y `deepseek-v4-flash|pro:cloud` siempre se tratan como razonamiento.
- **maxTokens**: default = límite máximo de Ollama en OpenClaw
- **Costes**: siempre 0

```bash
ollama list
openclaw models list
```

Definir `models.providers.ollama` con array `models` explícito (o provider personalizado no-loopback) **desactiva** la detección automática. Loopback personalizado (ej. `127.0.0.2:11434`) sigue considerándose local y mantiene auto-detección.

Referencia `ollama/<modelo>:latest` sin entrada manual en `models.json` se resuelve en runtime. En hosts con sesión iniciada, una referencia `:cloud` no listada se valida vía `/api/show` y se agrega al catálogo runtime solo si Ollama confirma metadata.

## Pruebas de humo (smoke tests)

Prueba de texto, sin herramientas de agente:
```bash
OLLAMA_API_KEY=ollama-local \
openclaw infer model run --local \
  --model ollama/llama3.2:latest \
  --prompt "Responde exactamente: pong" --json
```

Prueba de visión (`--file`, PNG/JPEG/WebP; no-imágenes se rechazan):
```bash
OLLAMA_API_KEY=ollama-local \
openclaw infer model run --local \
  --model ollama/qwen2.5vl:7b \
  --prompt "Describe esta imagen en una oración." \
  --file ./photo.jpg --json
```
- Ninguna ruta carga herramientas/memoria/contexto de sesión → si esto funciona pero el agente falla, el problema es capacidad tool-use del modelo, no el endpoint.
- `/model ollama/<x>` es elección exacta: si el `baseUrl` no es accesible, falla con error de provider (no fallback silencioso).

**Cron aislado**: verifica `/api/tags` antes de iniciar turno si el modelo resuelve a provider Ollama local/privado/.local; si falla, marca ejecución `skipped`. Cache de esta verificación: 5 min por host.

**Verificación en vivo (self-hosted):**
```bash
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_OLLAMA=1 OPENCLAW_LIVE_OLLAMA_WEB_SEARCH=0 \
pnpm test:live -- extensions/ollama/ollama.live.test.ts
```

**Verificación en vivo (Ollama Cloud):**
```bash
export OLLAMA_API_KEY=''
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_OLLAMA=1 \
OPENCLAW_LIVE_OLLAMA_BASE_URL=https://ollama.com \
OPENCLAW_LIVE_OLLAMA_MODEL=glm-5.1:cloud \
OPENCLAW_LIVE_OLLAMA_WEB_SEARCH=1 \
pnpm test:live -- extensions/ollama/ollama.live.test.ts
```
(Embeddings omitidos por default; forzar con `OPENCLAW_LIVE_OLLAMA_EMBEDDINGS=1`, ya que una key de nube puede no autorizar `/api/embed`.)

Nuevo modelo → auto-detectado tras descarga:
```bash
ollama pull mistral
```

## Inferencia local en Node remoto

- Agentes pueden delegar tareas breves a Ollama corriendo en un Node de escritorio/servidor emparejado.
- El prompt/respuesta viaja por la conexión autenticada Gateway↔Node existente; la solicitud se ejecuta en el endpoint loopback del propio Node (`http://127.0.0.1:11434`).

```bash
# En el Node:
ollama pull qwen3:0.6b
ollama list

# Conectar el Node:
openclaw node run --host <ip> --port 18789 --display-na...
```
*(comando truncado en el origen)*
