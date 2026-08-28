# COSMIC Custom Setup — compacto

> **Sistema:** Arch Linux · COSMIC DE (Wayland) · máquina `fibonacci`
> **Última actualización:** 2026-08-28 — actualizar siempre que haya hallazgo nuevo

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
| `refresh-system` / `refresh-system-key` | Refresh seguro, dos tiers (§9.4). NO toca cosmic-comp/i915/Firefox/Spotify/Thunderbird/swap; `-key` abre cosmic-term visible — 2026-08-28 |
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

## 9. Teclado y display — hallazgos verificados (2026-08-28)

> Medido en fibonacci durante un fallo real, no supuesto.

### 9.1 [!] `sudo` rechaza la contraseña correcta

**Síntoma:** agota los 3 intentos con la contraseña correcta. Intermitente, sin horario. Afecta
`tty1` (greeter/lock) **y** `pts/N` en la misma ventana → estado del compositor, no de la terminal.

**Causa (hipótesis vigente):** modificador (`Ctrl`/`Alt`/`Shift`/`Super`) queda lógicamente pegado
en COSMIC/Wayland → cada tecla llega como `Mod+tecla` y la contraseña alcanza PAM corrupta.

**Fix: `Super+Espacio`** antes de teclear. Fuerza a COSMIC a re-evaluar el estado de modificadores
y libera el pegado. Verificado 28-08.

**Descartado — no reinvestigar:**

| Descartado | Evidencia |
|---|---|
| Layout `us,latam` | La contraseña funciona igual en ambos layouts — sus caracteres coinciden. `Super+Espacio` es *también* el toggle de layout, lo que hace parecer que el layout era la causa. No lo es |
| `faillock` / bloqueo de cuenta | `faillock --user eldaniels` sin bloqueos activos; `faillock.conf` en defaults, sin `deny=` |
| Contraseña cambiada / cuenta corrupta | El mismo día autentica al primer intento en otras sesiones |
| capslock / numlock | LEDs normales durante el fallo (capslock 0, numlock 1) |

⚠️ **Nunca apagar con el botón.** Se resuelve solo: journal 06-08 mostró `sudo` recuperándose 43 min
después sin reinicio (boot 0 arrancó 08:52 y siguió activo). El apagado forzado es lo que corrompe
el FS en esta máquina — daño previo en `P8_Backup_Wiki/mft_recovery_decision.md`.
Escalado: 1) `Ctrl+Alt+F3` → autenticar en TTY, evita el compositor · 2) esperar, se limpia solo ·
3) SysRq `REISUB` si de verdad hace falta reiniciar — nunca el botón.

Historial: 06-08 primer diagnóstico · 28-08 recurrencia + fix confirmado.

### 9.2 Layout — `us,latam`, toggle `Super+Espacio`

Atajo propio de COSMIC, **no** opción xkb (`options: None` y aun así alterna). Tres archivos que
deben mantenerse coherentes:

| Archivo | Valor |
|---|---|
| `~/.config/cosmic/com.system76.CosmicComp/v1/xkb_config` | `layout: "us,latam"` ← el que COSMIC usa |
| `/etc/X11/xorg.conf.d/00-keyboard.conf` | `XkbLayout "us,latam"` |
| `/etc/vconsole.conf` | `XKBLAYOUT=us,latam` · `KEYMAP=us` (el TTY solo tiene `us`) |

### 9.3 HDMI no detectado tras conectar el cable — re-probe DRM

**Síntoma:** cable conectado después del boot, no pasa nada, `status` sigue `disconnected`.
Antes se resolvía reiniciando.

**Causa:** se perdió la interrupción HPD (hot-plug detect). Comportamiento conocido de `i915` en
puertos HDMI de laptop, sobre todo tras suspend/resume o al conectar post-boot. El cable está bien;
el kernel no se enteró.

```bash
echo detect | sudo tee /sys/class/drm/card1-HDMI-A-2/status   # 28-08: disconnected → connected 1920x1080
```

`detect` **restaura** la auto-detección (`connector->force = 0`), no es override — `on`/`off` sí lo
serían y no deben usarse. Nada persiste: sysfs se resetea en cada boot.

**Conectores reales** (Dell Latitude 5400, un solo puerto HDMI físico):

| Conector | Qué es |
|---|---|
| `card1-eDP-1` | Panel interno — **no re-sondear**, es la pantalla activa |
| `card1-HDMI-A-2` | El puerto HDMI físico |
| `card1-HDMI-A-1` | Fantasma, no existe físicamente |
| `card1-DP-1` / `DP-2` | DisplayPort vía USB-C (dock UGREEN) |

Escalado si `detect` no basta: `udevadm trigger --subsystem-match=drm --action=change` → recargar
`i915`, que exige cerrar sesión (`cosmic-comp` mantiene el device DRM abierto).

### 9.4 `refresh` — reemplaza al reboot para lo que sí se puede en caliente (2026-08-28)

Antes: `alias refresh='source ~/.zshrc && echo "Shell recargado"'`. Ahora tres piezas, porque el
scope lo obliga — `source` **debe** correr en el shell actual, un script hijo no puede recargarlo.

| Pieza | Ubicación | Permisos |
|---|---|---|
| `refresh()` función | `~/.zshrc` (reemplaza el alias) | usuario |
| `refresh-system` | `~/.local/bin/` | `0755` usuario |
| `refresh-system-privileged` | `/usr/local/bin/` | `0755 root:root` |
| `refresh-system-privileged-hard` | `/usr/local/bin/` | `0755 root:root` |

Invocación: `refresh` · `refresh --hard` · `Super+Shift+R` (ya apuntaba a `refresh-system`, hereda
todo menos la recarga de shell, irrelevante fuera de terminal).

**Seguridad — los scripts root no aceptan argumentos.** Decisión central. Dar NOPASSWD a `tee` con
patrón de ruta (`/sys/class/drm/*/status`) dejaría superficie de inyección: un argumento fabricado
puede escapar del patrón. Sin argumentos no hay nada que fabricar. Por eso son **dos binarios
separados** en vez de uno con flag `--hard`: la elección de tier ocurre del lado usuario y sudoers
nombra rutas exactas. Mismo principio que `auditar_pre_push.sh` — prevenir por arquitectura, no filtrar.

```
/etc/sudoers.d/refresh-system   (0440, validado con visudo -cf antes de instalar)
eldaniels ALL=(root) NOPASSWD: /usr/local/bin/refresh-system-privileged, /usr/local/bin/refresh-system-privileged-hard
```

⚠️ Si esos binarios quedaran escribibles por el usuario, el NOPASSWD es escalada a root trivial.
Verificar `ls -l` → `root root -rwxr-xr-x` tras cada reinstalación.

**Cobertura:**

| Capa | `refresh` | `--hard` |
|---|---|---|
| Re-probe DRM (§9.3) + `udevadm trigger` drm | ✅ | ✅ |
| `sync` → `drop_caches` → `compact_memory` | ✅ | ✅ |
| `journalctl --vacuum-size=500M` + `fstrim` (timeout 120s) | ✅ | ✅ |
| Cachés `~/.cache` (thumbnails, mesa_shader, fontconfig, pip, go-build, node-gyp) + `fc-cache` | ✅ | ✅ |
| `systemctl --user daemon-reload` | ✅ | ✅ |
| `source ~/.zshrc` | ✅ | ✅ |
| `systemctl daemon-reexec` — re-ejecuta PID 1 sin matar nada | — | ✅ |
| Unidades en `failed` → leer lista, `reset-failed`, restart | — | ✅ |
| `udevadm control --reload` + trigger todos los subsistemas | — | ✅ |
| NetworkManager + `resolvectl flush-caches` | — | ✅ |
| Bluetooth | — | ✅ |
| Audio (pipewire/wireplumber) + `xdg-desktop-portal` | — | ✅ |

Audio fuera del tier normal a propósito: corta ~1s y Spotify a veces necesita play/pausa para
reenganchar. Suelto: `systemctl --user restart wireplumber pipewire pipewire-pulse`.

**[!] Fuera de alcance en ambos tiers** — exigen cerrar sesión o reiniciar:
recargar `i915` (`cosmic-comp` mantiene el device DRM abierto) · kernel nuevo · unbind/bind de
controladores USB (tumbaría teclado y trackpad, recuperación no garantizada).

**Notificación — solo deltas medidos, no estado actual.** Los scripts root emiten
`##DELTA key=value` por stdout; `refresh-system` los cosecha y arma el resumen. Contrato explícito
en el header de cada archivo. Si nada cambió: `Nada que reparar — sistema ya estaba limpio`.

| Delta | Medición |
|---|---|
| `pantalla recuperada: HDMI-A-2` | status por conector antes vs después del `detect` |
| `26MB RAM` | `MemAvailable` antes vs después de `drop_caches` |
| `1.5MB caché` | `du -sk` de cada dir **antes** de borrar |
| `312MB journal` | `du -sk /var/log/journal` antes vs después del vacuum |
| `143MB trim` | suma de bytes de `fstrim -av`. **No es espacio liberado** — es el rango de extents libres descartados, sale igual en cada corrida |
| `3 unidad(es) recuperada(s)` | `--hard`: unidades `failed` reiniciadas con éxito |

Log completo: `~/.local/state/refresh-system.log`.

**Bugs corregidos durante el desarrollo** (para no repetirlos):

| Bug | Causa |
|---|---|
| `d[journal_freed_kb]: unbound variable` | Faltaba espacio antes de `]` en `[ -n "${d[k]:-}"]`. Slip de alineación por columnas → se eliminó el padding y se extrajeron helpers `have()`/`add()` |
| Separadores salían como espacios | `IFS=' · '` — IFS es un *conjunto de caracteres*, no un separador multi-carácter; `"${parts[*]}"` une con el primero. Se concatena a mano |
| `refresh` en terminal no notificaba | El alias viejo seguía vivo en la shell y gana sobre la función. `unalias refresh; source ~/.zshrc` |

---

**Regla de mantenimiento:** cualquier hallazgo nuevo sobre config COSMIC (atajo, script, panel,
tema, systemd unit) se agrega aquí — no crear archivos nuevos para esto.
