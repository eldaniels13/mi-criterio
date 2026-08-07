# Core UI local multi-modelo — OpenCode como base

## Contexto

eldaniels quiere un "core UI" local estilo Claude Code: correr modelos cloud (Claude, DeepSeek, Kimi) y modelos locales (prioridad futura, vía Ollama) desde una misma interfaz, con selector visual que diferencie costo/token y local-vs-cloud, y con herramientas tipo agente (no solo chat).

Origen: pregunta sobre Alt+P (se pensó que era builtin de Claude Code; en realidad es un switcher fzf propio en `~/.zshrc`, ya construido pero desincronizado — ver hallazgos abajo).

Decisión tomada: en vez de construir desde cero en Python, usar **OpenCode** (MIT, paquete oficial en repo `extra` de Arch, sin necesidad de AUR) como base, configurando/personalizando en vez de reimplementar agent loop + tool-calling + streaming.

## Hallazgos en vivo (verificados en fibonacci, no asumidos de docs viejos)

1. **Ollama ya no tiene los 4 modelos esperados.** Hoy: `deepseek-v4-flash:0731-cloud`, `deepseek-v4-flash:cloud` (proxies remotos de **Ollama Cloud**, no locales), `nomic-embed-text`, `deepseek-coder:6.7b`. `qwen2.5-coder:7b` y `qwen2.5-coder:1.5b` ya no están, aunque Alt+P (`~/.zshrc:105-135`) los sigue referenciando — el switcher está roto/desincronizado.
2. Ollama corre como `ollama.service` de **sistema** (no `--user`), versión `0.32.6-1`. `OLLAMA_KEEP_ALIVE`/`OLLAMA_NUM_THREAD` solo están exportados en `~/.zshrc` (líneas 156-159) — no aplican si algo arranca fuera de una shell con ese `.zshrc` cargado.
3. `deepseek-coder:6.7b` no tiene capability `tools` en su manifiesto Ollama — no sirve para agente, solo chat plano.
4. Open WebUI **no está corriendo** ahora mismo (sin proceso activo, puerto 8080 sin respuesta). No es "el frontend actual" en la práctica, pese a estar documentado como tal.
5. `opencode` está en `extra/` de Arch, firmado, sin necesidad de AUR ni PKGBUILD.
6. OpenCode tiene login OAuth nativo para **Claude Pro/Max** (`opencode auth login -p anthropic`) — usaría la suscripción existente sin API key/facturación aparte. No oficialmente soportado por Anthropic fuera de sus propios clientes — validar que funciona, tener plan B (API key de console.anthropic.com, facturación separada) si se rompe.
7. Riesgo real a validar temprano: Aider + Ollama ya falló antes por timeout/deadlock (litellm.Timeout 600s) en tool-calling con modelos locales pequeños en CPU-only. No asumir que OpenCode no repite el mismo bug — probar antes de invertir en personalización.

## Plan por fases (para ejecutar cuando se retome)

**Fase 0 — Reconciliar estado real (30 min)**
```bash
systemctl status ollama
ollama list
ollama pull qwen2.5-coder:1.5b   # soporta tools, necesario para Fase 3
```
Decidir: ¿mantener los modelos `*-cloud` de Ollama Cloud bajo el proveedor "Ollama", o limpiarlos para que "Ollama" sea estrictamente local (recomendado — evita mezclar local/cloud bajo un mismo badge)?

**Fase 1 — Instalar OpenCode**
```bash
sudo pacman -Si opencode   # confirmar firma/mantenedor
sudo pacman -S opencode
```
No usar `opencode-bin` de AUR (desactualizado, y activaría el protocolo de revisión PKGBUILD sin necesidad).

**Fase 2 — Provider Ollama en OpenCode**

Config en `~/.config/opencode/opencode.json`, provider tipo `@ai-sdk/openai-compatible` apuntando a `http://127.0.0.1:11434/v1`, con `qwen2.5-coder:7b`, `qwen2.5-coder:1.5b`, `deepseek-coder:6.7b` (sin `nomic-embed-text`, es embeddings, no chat).

Subir context window de Ollama antes de probar tool-use — mismo síntoma que el deadlock de Aider:
```bash
export OLLAMA_CONTEXT_LENGTH=16384
```
Mover esto y `OLLAMA_KEEP_ALIVE`/`OLLAMA_NUM_THREAD` a override systemd (`/etc/systemd/system/ollama.service.d/override.conf`) para que apliquen siempre, no solo en shells con `.zshrc` cargado.

**Fase 3 — Validar tool-use ANTES de personalizar (paso crítico)**

En directorio desechable (no `mi-criterio`):
```bash
cd /tmp && opencode
# /models → qwen2.5-coder:1.5b (ollama)
# "lee README.md y dime cuántas líneas tiene"
# "crea test.txt con 'hola' y léelo de vuelta"
```
Criterio de éxito: ejecuta en <60s, sin timeout/deadlock estilo Aider. Repetir con `qwen2.5-coder:7b` y `deepseek-coder:6.7b` (esperar error claro o degradación a modo sin-tools).

**Si esto falla igual que Aider, detener aquí** — investigar `num_ctx` adicional o adapter nativo de Ollama antes de seguir.

**Fase 4 — Costos y API keys cloud (paso explícito, no asumido)**

No conectar ningún provider hasta:
1. Probar `opencode auth login -p anthropic` → Claude Pro/Max OAuth. Confirmar que reconoce el plan sin facturación aparte.
2. Generar/confirmar keys de DeepSeek (`platform.deepseek.com`) y Kimi/Moonshot (`platform.moonshot.ai`), revisar pricing vigente (no de memoria).
3. Evaluar si un bundle tipo "OpenCode Zen" existe y compensa gestionar una sola key vs varias.
4. Keys vía `opencode auth login` (persisten fuera de `mi-criterio` — repo de conocimiento, no de secretos).

**Fase 5 — Selector visual (costo/token, local vs cloud)**

OpenCode soporta theming real (`~/.config/opencode/themes/*.json`, `tui.json`). No confirmado si el picker `/models` ya trae costo/token nativo — verificar en vivo antes de asumir. Si no existe, truco sin fork: inyectar el dato en el campo `"name"` de cada modelo en `opencode.json`, ej. `"Qwen2.5 1.5B · local · $0"` vs `"DeepSeek V4 · cloud · $1.74/1M"`.

**Fase 6 — Qué hacer con Alt+P y Open WebUI**

- No mantener los tres en paralelo (Open WebUI ni corre hoy; Alt+P ya desincronizado — deuda silenciosa, contra "minimal").
- Reescribir Alt+P (`~/.zshrc:105-135`) para lanzar `opencode` con el modelo elegido en vez de golpear Open WebUI en :8080.
- Retirar Open WebUI del uso activo una vez Fase 3 confirme que OpenCode cubre el caso con Ollama (no desinstalar, dejar como fallback de chat puro).

**Fase 7 — Dónde vive la config**

- Config viva de OpenCode: `~/.config/opencode/` (no en `mi-criterio` — repo de conocimiento, no de sistema/dotfiles).
- Documentación de la decisión final: `mi-criterio/proyectos/P8/` o `P8_Backup_Wiki/`, patrón de `P8_Backup_Seguridad_Digital_Maestro.md`.

## Archivos críticos

- `~/.config/opencode/opencode.json` — providers y modelos del selector
- `~/.config/opencode/tui.json`, `~/.config/opencode/themes/*.json` — personalización visual
- `~/.zshrc:105-160` — switcher Alt+P a reescribir + export `OLLAMA_*` a migrar
- `/etc/systemd/system/ollama.service.d/override.conf` (nuevo) — env vars persistentes del servicio
- `mi-criterio/proyectos/P8/` — documentación de la decisión

## Verificación end-to-end (al ejecutar)

1. `systemctl status ollama` activo, `opencode --version` responde, `ollama list` muestra los 3 modelos locales esperados.
2. Alt+P reescrito (o `/models` en opencode) muestra modelos Ollama badgeados "local" ($0).
3. Tarea con herramientas en modelo local (`qwen2.5-coder:1.5b`): lee y edita archivo real, sin timeout.
4. Cloud (Claude OAuth o DeepSeek API key) badgeado "cloud" con costo/token si Fase 5 lo logró.
5. Misma tarea en modelo cloud: confirmar ejecución, comparar velocidad/calidad vs local.
6. Cambiar de modelo local→cloud dentro de la misma sesión, confirmar que conserva el hilo.
7. Completar tarea entera (leer+editar+correr comando) sin tocar Open WebUI.

## Pendiente / no resuelto en esta sesión

- No se confirmó si el repo autoritativo de OpenCode es `sst/opencode` o `anomalyco/opencode` (el paquete de Arch pacman apunta al segundo) — verificar al instalar.
- No se investigó pricing real de DeepSeek/Kimi ni se confirmaron qué API keys ya tiene el usuario ("debo investigar más de esto" — palabras propias).
- No se probó en vivo si OpenCode repite el deadlock de Aider con Ollama — es el paso de mayor riesgo, pendiente de ejecución (Fase 3).
