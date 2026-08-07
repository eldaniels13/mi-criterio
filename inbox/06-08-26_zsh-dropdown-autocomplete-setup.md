# Setup: Dropdown de autocompletado + preview en Zsh
**Host:** fibonacci (Dell Latitude 5400, Arch Linux + COSMIC)
**Shell:** Zsh 5.9.2
**Fecha spec:** 2026-08-06 · **Ejecutado:** 2026-08-06 · **Estado: ✅ FUNCIONANDO**

> Este documento fue **corregido tras la ejecución**. El spec original contenía
> 3 errores técnicos que habrían roto la instalación. Se conserva lo que se
> planeó, marcado contra lo que resultó, porque la diferencia es la lección.

---

## 1. Objetivo

Al presionar `Tab` sobre un prefijo parcial (`h<Tab>`, `re<Tab>`), mostrar un menú
navegable con preview de la descripción del comando (`tldr`, fallback a `man`),
navegación 100 % teclado, sin tocar `zsh-autosuggestions`.

Objetivo dual: velocidad de tipeo + **aprendizaje de comandos Linux por descubrimiento**.

## 2. Resultado real

```
Tab    ─► ¿qué comandos existen?     → descubrimiento (preview tldr/man)
Ctrl+R ─► ¿qué he escrito yo antes?  → recuperación (fzf sobre 100k líneas)
```

Quedaron **separados a propósito** (ver error #3 abajo).

## 3. Stack final

| Componente | Herramienta | Estado |
|---|---|---|
| Sugerencia inline | `zsh-autosuggestions` | ya estaba · intacto |
| Coloreado de sintaxis | `zsh-syntax-highlighting` | **ya estaba** · intacto |
| Motor de completion | zsh compsys (`compinit`) | nativo |
| UI del menú | `fzf-tab` | clonado en `~/.zsh/fzf-tab` |
| Fuzzy finder | `fzf` | ya estaba |
| Descripciones | `tealdeer` (`tldr`) | instalado + `tldr --update` |
| Fallback | `man` / `whatis` | `man-db` ya estaba |

## 4. Configuración aplicada en `.zshrc`

### Historial (prerrequisito, no estaba en el spec original)

```zsh
HISTSIZE=100000        # RAM — DEBE ser >= SAVEHIST o zsh poda el archivo
SAVEHIST=100000
setopt HIST_IGNORE_ALL_DUPS HIST_IGNORE_SPACE HIST_REDUCE_BLANKS SHARE_HISTORY

HISTORY_IGNORE='(*--password*|*--token*|*API_KEY*|*SECRET*|*Authorization:*)'
ZSH_AUTOSUGGEST_HISTORY_IGNORE=$HISTORY_IGNORE
```

Estaba en `HISTSIZE=1000` con el archivo ya en 1272 líneas → **estaba borrando historial
en cada cierre**. Con `Ctrl+R` como herramienta principal de historial, esto era bloqueante.

### Marca visual de modo privado

```zsh
autoload -Uz add-zle-hook-widget
_private_mode_indicator() {
  [[ $BUFFER == ' '* ]] && region_highlight+=("0 ${#BUFFER} fg=magenta,bold")
}
add-zle-hook-widget zle-line-pre-redraw _private_mode_indicator
```

Comando con espacio inicial → línea en magenta = "esto NO entra al historial".
Privacidad visible, no supuesta.

### fzf-tab

```zsh
# ORDEN: después de compinit, ANTES de autosuggestions/syntax-highlighting
zstyle ':completion:*:descriptions' format '[%d]'
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' menu no                      # OBLIGATORIO
zstyle ':completion:*:git-checkout:*' sort false

source ~/.zsh/fzf-tab/fzf-tab.plugin.zsh

zstyle ':fzf-tab:complete:(-command-|-parameter-|-brace-parameter-):*' \
  fzf-preview '(tldr --color always $word 2>/dev/null \
                || man $word 2>/dev/null \
                || whatis $word 2>/dev/null) | head -200'
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'ls --color=always $realpath'

zstyle ':fzf-tab:*' fzf-bindings 'ctrl-j:down,ctrl-k:up'
zstyle ':fzf-tab:*' switch-group '<' '>'
zstyle ':fzf-tab:*' fzf-flags --height=60% --layout=reverse --border \
  --preview-window='right:55%:wrap'
```

### fzf key-bindings

```zsh
source /usr/share/fzf/key-bindings.zsh
# NO cargar /usr/share/fzf/completion.zsh — ver error #4
```

## 5. Keybindings finales

| Tecla | Acción |
|---|---|
| `Tab` | Abre el menú de completado |
| `Ctrl+J` / `Ctrl+K` o `↑` `↓` | Navega candidatos |
| `<` / `>` | Cambia entre grupos |
| `Ctrl+Space` | Multi-selección |
| `/` | Completado continuo (rutas profundas) |
| `Esc` | Cancela |
| `Ctrl+R` | Búsqueda difusa en historial completo |
| `Ctrl+T` / `Alt+C` | Archivos / cambiar de directorio |

---

## 6. Errores del spec original (Claude) — corregidos

**#1 · Orden de carga invertido.**
El spec decía cargar `fzf-tab` **después** de `zsh-autosuggestions`. El README oficial dice
lo contrario: *"fzf-tab needs to be loaded after `compinit`, but before plugins which will
wrap widgets"*. El orden del spec habría dejado el menú sin enganchar.

**#2 · Faltaba `zstyle ':completion:*' menu no`.**
Es obligatorio en versiones actuales — permite a fzf-tab capturar el prefijo no ambiguo.
Sin él, el menú nativo interfiere.

**#3 · "Historial primero" no es una función de fzf-tab.**
El spec proponía `zstyle ':completion:*:*:-command-:*:*' group-order history-words commands`.
fzf-tab **sólo muestra los resultados del sistema de completado de zsh**; el historial no es
una fuente de completado de comandos. Nunca habría funcionado. La herramienta correcta es
`Ctrl+R` (fzf sobre el historial), que además cumple mejor el objetivo real.

**#4 · Diagnóstico incompleto → dos suposiciones falsas.**
El spec listaba `man` como *"Nativo — ya está en el sistema"* (no estaba al empezar) y
`zsh-autosuggestions` como *"Instalado (asumido)"*. Peor: el grep de diagnóstico **no
incluía `syntax-highlighting`**, así que se dio por ausente un plugin que ya estaba cargado
en la línea 23 del `.zshrc`. Eso llevó a proponer `zle -N zle-line-pre-redraw`, que habría
**sobrescrito el hook y roto el coloreado de sintaxis**. La versión correcta encadena con
`add-zle-hook-widget` y apende a `region_highlight` con `+=`, nunca `=()`.

**#5 · Conflicto de `^I` no previsto.**
Al añadir `source /usr/share/fzf/completion.zsh`, fzf enlazó `^I` a `fzf-completion` y le
robó el Tab a fzf-tab. Detectado con `bindkey "^I"`. Los dos hacen el mismo trabajo → se
eliminó el de fzf. El README lo advierte: *"make sure it is the last plugin to bind ^I"*.

**#6 · Preview sin `wrap`.**
fzf **corta** las líneas largas del preview en vez de envolverlas. Las descripciones de
comandos quedaban ilegibles. Se requiere `--preview-window='...:wrap'` explícito.

> **Patrón común a #1–#6:** todos eran verificables antes de escribir la config
> (leer el README local, `bindkey "^I"`, leer el `.zshrc` completo). Se escribió
> primero y se verificó después.

## 7. Errores de ejecución (eldaniels) — para el registro

**#1 · `HISTSIZE=100` con `SAVEHIST=99999`.**
Intención correcta (limitar exposición), palanca equivocada. `HISTSIZE` es el buffer en RAM;
si es menor que `SAVEHIST`, zsh **poda el archivo al cerrar** — habría destruido el historial
que se quería conservar. La exposición se controla con `HIST_IGNORE_SPACE` + `HISTORY_IGNORE`
(qué *entra*), no con el tamaño (cuánto *cabe*).

**#2 · Comandos ya ejecutados, reportados como fallo.**
`pacman -Rns rider` / `linux-wallpaperengine` devolvieron `target not found` porque ya se
habían borrado a las 18:37–18:38 en otra terminal. Se diagnosticó con `/var/log/pacman.log`.
Sin ese log se habría perseguido un fantasma. **Lección:** verificar estado antes de repetir
un comando "fallido".

**#3 · Apagado forzado como remedio del fallo de `sudo`.**
Refutado por el journal: `sudo` falló 15:23–15:24 y funcionaba a las 16:06 **sin reinicio**.
Se resuelve solo. El apagado forzado es el mecanismo que corrompe sistemas de archivos, y
ya hay antecedente en este equipo (`P8_Backup_Wiki/mft_recovery_decision.md`).
Ver `recursos/MEMORIA_SISTEMA_CLAUDE.md` §13.4.

**#4 · Caché de pacman nunca podada.**
17 GB / 9013 archivos para 1496 paquetes instalados. `/` llegó al 98 % y bloqueó la
instalación que originó toda esta sesión. Ver §13.3.

## 8. Rollback

```zsh
# Comentar en .zshrc el bloque fzf-tab (source + zstyle ':fzf-tab:*')
# zsh-autosuggestions y zsh-syntax-highlighting no se tocan en ningún paso.
exec zsh
```

## 9. Verificación

```zsh
bindkey "^I"          # → fzf-tab-complete   (NO fzf-completion)
bindkey "^R"          # → fzf-history-widget
zle -l | grep pre-redraw
#   → _zsh_highlight__zle-line-pre-redraw
#   → zle-line-pre-redraw (azhw:zle-line-pre-redraw)   ← ambos vivos
```

## 10. Pendientes

- [ ] Documentar el bloque final en `proyectos/P2/COSMIC_setup_custom.md`
- [ ] Si algún día se instala `fast-syntax-highlighting` o `zsh-autocomplete`:
      revisar el conflicto de `zle-line-pre-redraw` y de `^I` **antes** de instalar
- [ ] `build-fzf-tab-module` (módulo binario) si el coloreado se siente lento

## 11. Insight cross-lens

**P2 + P8:** terminal optimizada para descubrimiento acelera el aprendizaje de Linux (P2),
y el 100 % teclado preserva control auditable (P8).

**Meta-lección de la sesión:** el spec se escribió antes de medir el sistema, y 6 de sus
puntos fallaron por eso — el mismo punto ciego `[!]` que el perfil maestro ya nombra
(*"diseña sistemas antes de validar factibilidad"*). El paso 4 del spec original ("diagnóstico
previo") era correcto; el error fue **ponerlo después** de haber comprometido el stack.
