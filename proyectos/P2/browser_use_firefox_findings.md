# browser-use × Firefox — hallazgos (2026-09-05)

## Objetivo original
Instalar/actualizar browser-use (latest stable) con uv + Python 3.12,
registrar el skill y conectar el navegador.

## Lo que se hizo
1. `uv tool install --upgrade browser-use --python 3.12` → OK
   - uv provisionó Python 3.12.13 automáticamente (no estaba en sistema;
     Python del sistema es 3.14.7)
   - 5 executables: browser, browser-use, browser-use-tui, browseruse, bu
2. `browser-use skill install` → OK
   - Skill registrada en: ~/.agents, ~/.claude, ~/.codex, ~/.copilot,
     ~/.cursor, ~/.gemini, ~/.openclaw, ~/.config/opencode/skills
3. `browser-use --doctor` → FAIL
   ```
   [FAIL] chrome running — start chrome/edge
   [FAIL] daemon alive — see install.md
   [FAIL] active browser connections — 0
   [FAIL] Browser Use cloud auth — optional
   ```
4. Búsqueda de navegadores instalados:
   - No hay chrome/chromium/brave/vivaldi/edge/opera (binarios)
   - Firefox 155.0.1-1 instalado vía pacman (`/usr/local/bin/firefox`)
   - Existen configs residuales `~/.config/chromium` y `~/.config/google-chrome`

## Hallazgo clave
browser-use / browser-harness es **CDP-only** (Chrome DevTools Protocol).
Funciona con Chrome/Chromium/Edge únicamente.
Firefox habla WebDriver BiDi / Marionette → **incompatible**.
El doctor del harness lo confirma: "start chrome/edge".

## Alternativas mapeadas (no ejecutadas)
| Opción | Costo | Nota |
|---|---|---|
| Chromium vía pacman (solo para automatización) | local, gratis | Firefox queda intacto como daily driver |
| Playwright / Selenium con BiDi | setup adicional | Firefox nativo, stack distinto |
| Browser Use Cloud | cuenta + posible costo | navegador en la nube, sin Chrome local |

## Estado
Pendiente decidir herramienta Firefox-compatible → ToDo_global_eldaniels.md
(browser-use queda instalado y con skill registrada; inutilizable sin Chromium)
