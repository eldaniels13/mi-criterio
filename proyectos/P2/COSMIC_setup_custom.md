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
| `Super+N` | `blue-light-toggle` — gammastep on/off ⚠️ **ROTO**: notifica pero no cambia la pantalla (ver §8.3) |
| `Super+Shift+D` | `theme-toggle` — dark/light COSMIC, propaga a Firefox y todo lo compatible (2026-08-07) |
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
| `theme-toggle` | Dark/light COSMIC escribiendo `is_dark`; propaga vía portal — 2026-08-07 |

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

## 8. Tema, panel y límites de COSMIC — hallazgos verificados (2026-08-07)

> Todo lo de esta sección está **medido en fibonacci**, no supuesto.
> Consultar aquí antes de volver a investigar.

### 8.1 Dark/light: cómo funciona la cadena completa

```
~/.config/cosmic/com.system76.CosmicTheme.Mode/v1/is_dark   ("true" | "false", sin newline)
   │  cosmic-config lo vigila con inotify
   ▼
xdg-desktop-portal-cosmic  publica  org.freedesktop.appearance / color-scheme
   │  1 = dark · 2 = light · 0 = no preference
   ▼
Firefox, GTK, Qt (con portal), Electron…  cambian SOLOS
```

**Verificado en vivo:** escribir el archivo cambia el portal en <2 s, sin reiniciar
panel, sesión ni apps. No hay que configurar cada aplicación por separado.

```bash
# Leer el estado que ven las apps
busctl --user call org.freedesktop.portal.Desktop /org/freedesktop/portal/desktop \
  org.freedesktop.portal.Settings Read ss "org.freedesktop.appearance" "color-scheme"
# → v v u 1   (dark)
```

Backend confirmado: `/usr/share/xdg-desktop-portal/portals/` contiene `cosmic.portal` y `gtk.portal`.

**Valores de luminancia base (`.../CosmicTheme.{Dark,Light}/v1/background` → `base`):**

| Tema | base | Nota |
|---|---|---|
| Dark | 0.10588 | **NO TOCAR** — valor validado por eldaniels para fatiga visual |
| Light | 0.84314 | salto de 73 puntos respecto a dark |

**No existe transición animada.** COSMIC hace flip de config; no hay API de fundido.
Decisión (2026-08-07): se acepta el cambio brusco. No invertir tiempo aquí de nuevo.

### 8.2 [!] Límite duro: NO hay applets custom en el panel

COSMIC alpha **no permite** applets de terceros en la zona de status. Confirmado dos veces
(2026-05-26 con blue-light, 2026-08-07 con dark/light + caps lock).

Un applet real es un binario Wayland layer-shell con `X-CosmicApplet=true`; todos son
symlinks a `/usr/bin/cosmic-applets`. Un `.desktop` que apunte a un script **no se renderiza**.

Applets disponibles (los únicos posibles): `A11y · Audio · Battery · Bluetooth ·
InputSources · Minimize · Network · Notifications · Power · StatusArea · Tiling · Time · Workspaces`.

**Consecuencia práctica:** peticiones tipo *"indicador de caps lock en el panel"* o
*"toggle de tema en el panel"* **no son ejecutables hoy**. La vía soportada es
atajo de teclado + (opcional) pin en el dock. Revaluar sólo si COSMIC llega a beta/stable.

Caps lock sí es legible por script si se necesita en otro contexto:
`/sys/class/leds/input3::capslock/brightness` → `0` off, `1` on.

### 8.3 [!] `blue-light-toggle` está roto

`Super+N` lanza la notificación pero **la pantalla no cambia**. Causa probable:
`cosmic-comp` no implementa `wlr-gamma-control-unstable-v1`, que es lo que usa `gammastep`.
Candidato de reemplazo ya identificado: `wl-gammarelay-rs` (interfaz DBus).
**Pendiente, despriorizado por eldaniels (2026-08-07).** No re-diagnosticar sin pedirlo.

### 8.4 Layout del panel — índices reales

`~/.config/cosmic/com.system76.CosmicPanel.Panel/v1/plugins_wings` → `Some(([izquierda], [derecha]))`

```
izquierda: 0 Workspaces
derecha:   0 InputSources · 1 Tiling · 2 Audio · 3 Bluetooth
           4 Network · 5 Battery · 6 Notifications · 7 Power
centro (plugins_center): 0 Time
```

Recargar panel: `pkill -x cosmic-panel` — **y nada más**, cosmic-session lo relanza en 1–3 s.
Arrancarlo a mano produce panel duplicado.

### 8.5 Editar el RON de atajos sin romperlo

El archivo `…/CosmicSettings.Shortcuts/v1/custom` es RON, no JSON. Patrón seguro
(backup + inserción tras la llave de apertura, idempotente):

```python
p = "~/.config/cosmic/com.system76.CosmicSettings.Shortcuts/v1/custom"  # expandir
s = open(p).read()
entry = '''    (
        modifiers: [
            Super,
            Shift,
        ],
        key: "d",
    ): Spawn("/home/eldaniels/.local/bin/theme-toggle"),
'''
assert 'theme-toggle' not in s          # idempotencia
i = s.index('{') + 1
open(p, 'w').write(s[:i] + "\n" + entry + s[i:].lstrip('\n'))
```

**Teclas `Super+<x>` ya ocupadas** (verificar antes de asignar nuevas):
`e f h j k l n r s v w slash Tab Left` + `Shift`: `d e f r s v`.

---

**Regla de mantenimiento:** cualquier hallazgo nuevo sobre config COSMIC (atajo, script, panel,
tema, systemd unit) se agrega aquí — no crear archivos nuevos para esto.
