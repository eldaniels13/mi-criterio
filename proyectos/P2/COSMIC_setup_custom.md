# COSMIC Custom Setup — compacto

> **Sistema:** Arch Linux · COSMIC DE (Wayland) · máquina `fibonacci`
> **Última actualización:** 2026-07-18 — actualizar siempre que haya hallazgo nuevo

---

## 1. Atajos de teclado (`~/.config/cosmic/com.system76.CosmicSettings.Shortcuts/v1/custom`)

| Combo | Acción |
|---|---|
| `Super+Tab` | Launcher |
| `Super+←` | Focus Left |
| `Super` (solo) | Workspace Overview |
| `Super+H` | Home Folder |
| `Super+S` | `cosmic-settings` |
| `Super+V` | `clip-history` — historial portapapeles c/imágenes |
| `Super+Shift+V` | `clip-history-del` — borrar entrada del historial |
| `Super+Shift+S` | `screenshot-clip` — captura región → portapapeles (usa `cosmic-screenshot`) |
| `Super+Shift+E` | `safe-eject` — desmonta/apaga USB (maneja VeraCrypt) |
| `Super+Shift+R` | `refresh-system` — refresh no-destructivo Arch+COSMIC |
| `Super+N` | `blue-light-toggle` — gammastep on/off |
| `Super+Shift+F` | `open-finanzas` — abre PlantillaFinanzas2026.xlsx, avisa si ya está abierto (2026-07-18) |
| `Super+F/J/K/L/W` | Disable (defaults COSMIC removidos) |
| `Super+Ctrl+Shift+L/J/Right/Down` | Disable |
| `Print` | Disable (reemplazado por Super+Shift+S) |

Backup del RON completo: `_backup_20260526_071155/`. Formato RON — al editar a mano, respetar
indentación 4-espacios y coma final en cada entrada.

---

## 2. Scripts custom (`~/.local/bin/`)

| Script | Qué hace |
|---|---|
| `clip-history` / `clip-history-del` | Frontend fuzzel sobre `cliphist` (daemon vía `wl-paste --watch`) |
| `screenshot-clip` | Región interactiva → clipboard, usa `cosmic-screenshot` nativo (no grim+slurp) |
| `safe-eject` | Desmonta USB, detecta y desmonta volúmenes VeraCrypt antes de power-off, picker fuzzel |
| `refresh-system` / `refresh-system-key` | Refresh seguro (NO toca cosmic-comp/Firefox/Spotify/Thunderbird/swap); `-key` abre cosmic-term visible |
| `blue-light-toggle` | Toggle gammastep, estado en `$XDG_RUNTIME_DIR` (reset en reboot) |
| `battery-warn` | Notificación crítica batería ≤5% descargando, loop 60s, un solo aviso por evento |
| `micled-invert` | Invierte LED `platform::micmute` según mute real (`pactl subscribe`) |
| `hwinfo` | Snapshot compacto hardware — barras de uso RAM/disco por montaje, aviso térmico ≥85 °C; sin root (DMI vía sysfs). Detalle por DIMM sólo con `sudo` — 2026-08-06 |
| `open-finanzas` | Lanza LibreOffice sobre finanzas P4, avisa si ya abierto (lock file) — 2026-07-18 |

---

## 3. Autostart (`~/.config/autostart/`)

- `battery-warn.desktop` · `cliphist.desktop` (daemon clipboard)
- Symlinks a apps del sistema: firefox, htop, thunderbird, spotify

## 4. systemd --user (enabled, no-default)

- `battery-alert.service` · `syncthing.service` · `p11-kit-server.socket` · `ssh-agent.socket`
- `org.freedesktop.impl.portal.desktop.cosmic.service` (portal nativo COSMIC)

## 5. Desktop entries custom (`~/.local/share/applications/`)

- `krokiet.desktop` — Czkawka duplicate finder (icono propio en `~/.local/share/icons/krokiet.png`)
- `syncthing.desktop` — abre `localhost:8384` (icono propio `syncthing.jpg`)
- `safe-eject.desktop` · `bluelight-toggle.desktop` · `claude-code-url-handler.desktop`

## 6. Clipboard stack (referencia)

`wl-copy` mantiene proceso en background (Ctrl+V inmediato) → `wl-paste --watch` alimenta
`cliphist` (historial) → `Super+V` decodifica y restaura al clipboard activo. Solo apps que
aceptan `image/png` pegan imágenes (limitación normal, no bug).

---

## 7. Hecho / en progreso / plan

**Hecho:**
- Atajos custom completos (tabla §1), scripts asociados (§2), autostart, desktop entries.
- Fix Super+Shift+S → screenshot-to-clipboard (rebind desde `System(Screenshot)` default).
- Quick-launch finanzas (Super+Shift+F, 2026-07-18).

**En progreso:** ninguno abierto actualmente.

**Plan / ideas pendientes (sin ejecutar):**
- Evaluar `wmctrl`/equivalente Wayland para foco real de ventana existente en `open-finanzas`
  (hoy solo notifica, no enfoca — limitación Wayland/COSMIC sin herramienta de foco por título).
- Documentar `com.system76.CosmicComp` y `CosmicPanel`/`Dock` si se personalizan a futuro.
- Revisar si conviene mover `refresh-system-key` a un atajo dedicado (hoy sin bind).

---

**Regla de mantenimiento:** cualquier hallazgo nuevo sobre config COSMIC (atajo, script, panel,
tema, systemd unit) se agrega aquí — no crear archivos nuevos para esto.
