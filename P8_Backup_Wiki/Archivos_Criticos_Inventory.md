# Archivos_Criticos_Inventory (actualizar)
**Backup actual**: USB 32GB · F:\backup_danyb_2026 · 7.7GB usados
**Fecha**: 2026-03-31

## Contenido del USB

| Carpeta en USB | Origen | Contenido |
|---|---|---|
| Programas PerformanceDesigns\ | C:\Users\danyb\ | CutWindow_2, DeepNestSharp, NestingTesting, O2BToDxf y más — código fuente completo |
| Música\Hard Groove | C:\Users\danyb\Music\ | MP3s personales |
| Música\Mi Musica | C:\Users\danyb\Music\ | MP3s personales |
| Música\MIXO | C:\Users\danyb\Music\ | MP3s DJ |
| Música\PsyTrance | C:\Users\danyb\Music\ | MP3s personales |
| MATLAB\ | C:\Users\danyb\Documents\MATLAB\ | Ejemplo3_BombaCentrifuga, ICE codes, Vibraciones |
| jueguitos\Sid Meier's Civilization VI saves | C:\Users\danyb\Documents\My Games\ | Partidas nombradas (Moctezuma, Cleopatra, Gorgo...) |
| jueguitos\Los Sims 4 | C:\Users\danyb\Documents\Electronic Arts\ | Slots 1-4 |
| jueguitos\GTA V Profiles | C:\Users\danyb\Documents\Rockstar Games\ | Saves historia |
| jueguitos\Minecraft | C:\Users\danyb\AppData\ | Worlds |
| VSCode_user_config\ | C:\Users\danyb\AppData\Roaming\Code\User\ | settings.json, keybindings, snippets, historial |
| VSCode_extensions.txt | — | Lista de 14 extensiones instaladas |
| AppData_Roaming\Cura_perfiles\ | C:\Users\danyb\AppData\Roaming\cura\ | Perfiles Creality Ender-3 v2 Neo |
| AppData_Roaming\CIMCO_AS\ | C:\Users\danyb\AppData\Roaming\CIMCO AS\ | Macros .MAC (haas, heidenhain, iso), configs máquina |

## Archivos sueltos en raíz del USB
| Archivo | Contenido |
|---|---|
| .gitconfig | Config global git (user: eldaniels13, editor: nvim) |
| VSCode_extensions.txt | Lista extensiones para reinstalar: `cat VSCode_extensions.txt | xargs -L 1 code --install-extension` |

## Categorías cubiertas
- A (irreemplazables personales): ✅ música
- B (credenciales/configs): ✅ git, VSCode, Cura, CIMCO
- C (documentos): ✅ universidad + MATLAB
- D (proyectos activos): ✅ código fuente completo
- E (referencias/juegos): ✅ saves seleccionados

## Lo que NO está en el backup (decisiones conscientes)
- Instaladores SOLIDWORKS (8.9GB) — reinstalable desde cuenta uni
- AutoCAD — licencia educativa caducada
- FL Studio — sin proyectos propios, reinstalable
- rekordbox — uso básico sin personalizar
- AppData caché (Mozilla, Discord, minecraft caché, etc.) — regenerable

---

## Configs de sistema Arch Linux (FUERA del repo — backup obligatorio)
**Migración a Arch:** este bloque cubre el setup actual (Arch + COSMIC), no el backup Windows de arriba.
**Regla dura:** estos archivos viven en `~/.config/` y `/etc/` — NUNCA dentro de `mi-criterio/`.
El repo solo los **documenta** (ver `recursos/ARCH_LINUX_SETUP_REFERENCE.md`); los archivos vivos van al backup externo.

| Archivo vivo (ruta real) | Qué hace | Cómo recrear |
|---|---|---|
| `~/.config/wireplumber/wireplumber.conf.d/51-bose-no-suspend.conf` | Evita que WirePlumber suspenda por inactividad el sink Bose USB (audio mudo tras pausa) | `restore.sh` del bundle externo (ver § Reproducibilidad) |
| `/etc/udev/rules.d/99-bose-usb-no-autosuspend.rules` | Desactiva USB autosuspend del Bose (05a7:1020), persistente a reboot/replug | idem |

> El **contenido** de estos archivos NO está en el repo (regla content-free). Vive en el bundle de restauración del backup externo.

**Verificación post-restauración:**
- `pactl list short sinks \| grep -i bose` → `IDLE` (no `SUSPENDED`) tras reproducir y pausar
- Bose `power/control` = `on` (los hubs 05e3 quedan en `auto`, es correcto)

---

## Reproducibilidad post-reinstall
**Decisión (2026-06-20):** el mecanismo de restauración es un **bundle en el backup externo**
(Kingston/USB), NO en ningún repo. El repo solo describe; el backup contiene y restaura.

**Bundle:** `arch-setup-backup/` (se genera en `~/arch-setup-backup/` y se copia al backup externo)
```
arch-setup-backup/
├── restore.sh              # recrea configs + reinstala paquetes (idempotente)
├── README.md               # qué hace y cómo correrlo tras reinstall
├── configs/
│   ├── wireplumber/51-bose-no-suspend.conf
│   └── udev/99-bose-usb-no-autosuspend.rules
├── pkglist-official.txt    # pacman -Qqe
└── pkglist-aur.txt         # pacman -Qqm
```
**Refrescar el bundle** cuando cambie el setup: re-correr el generador y re-copiar al backup.

**NO incluido en el bundle (manejo aparte, backup cifrado):**
- `~/.ssh/` claves privadas — nunca en repo ni en bundle plano
- credenciales / tokens

**Crecimiento futuro (cuando aplique):** dotfiles COSMIC, config zsh, `.gitconfig`,
roadmap i3wm/Hyprland (la capa WirePlumber se conserva intacta entre DEs).
