# Incidente: freeze del sistema + pérdida del binario `claude`

**Fecha:** 11-12 de agosto de 2026
**Host:** fibonacci (Dell Latitude 5400, Arch Linux, COSMIC)

---

## 1. Resumen del incidente

Durante uso normal (batería entre 10-20%, YouTube en pantalla completa, Thunderbird, Firefox, terminales con Claude Code activos), el sistema entró en un estado de freeze:

- Video se congeló; audio Bluetooth siguió reproduciendo en loop (~1 segundo repetido).
- `Super+Ctrl+Esc` no tuvo respuesta.
- Se forzó apagado manteniendo el botón de encendido (hard power-off).

Al reiniciar: descifrado de disco exitoso, escritorio accesible, pero:

```
zsh: command not found: claude
```

Un soft reboot posterior no resolvió el problema.

---

## 2. Hipótesis del freeze (no confirmada a fondo)

Patrón típico de **hang del compositor/GPU**: el pipeline de audio (PipeWire/Bluetooth) es independiente del de video, por eso el audio siguió corriendo mientras el video y el input quedaban congelados. La transición de batería crítica (20%→10%) es sospechosa como disparador de un cuelgue en el driver i915, pero no se profundizó con `dmesg`/dumps de GPU en esta sesión.

---

## 3. Diagnóstico del binario faltante

### 3.1 Verificaciones descartadas

| Verificación | Resultado |
|---|---|
| `echo $PATH` | Contenía correctamente `~/.nvm/versions/node/v24.14.1/bin` |
| `npm ls -g --depth=0` | `@anthropic-ai/claude-code@2.1.221` **sí** listado |
| `pacman -Qs claude-code` | Sin resultados (no es paquete de pacman) |

Conclusión parcial: el paquete npm estaba registrado, pero el ejecutable no aparecía en el PATH.

### 3.2 Verificación decisiva

```bash
ls -la ~/.nvm/versions/node/v24.14.1/bin/claude
# → No such file or directory

ls -la ~/.nvm/versions/node/v24.14.1/lib/node_modules/@anthropic-ai/claude-code/
# → package.json, node_modules/, bin/, etc. — TODO presente
```

**El paquete completo seguía intacto; solo faltaba el symlink ejecutable en `bin/`.**

### 3.3 Causa raíz: confirmada vía `journalctl -b -1`

```
systemd-fsck[386]: /dev/mapper/vg0-lv_root: recovering journal
systemd-fsck[386]: /dev/mapper/vg0-lv_root: Clearing orphaned inode 1051711 ...
[... decenas de inodos huérfanos limpiados, también en lv_home ...]
```

El hard power-off cortó el journal de ext4 a mitad de escritura. Al arrancar, `fsck` recuperó el journal y **eliminó inodos huérfanos** — archivos en estado inconsistente (creados/modificados sin cierre correcto de su entrada de directorio). El symlink `claude` en `bin/` cayó en ese barrido: es exactamente el tipo de archivo pequeño y reciente vulnerable a esto.

**No fue un problema de configuración (`.zshrc`, PATH) — fue corrupción de filesystem por corte abrupto de energía.**

---

## 4. Solución aplicada

```bash
npm install -g @anthropic-ai/claude-code
command -v claude
```

Esto reconstruye el symlink en `bin/` sin tocar la configuración de Claude Code (sesiones, settings) que vive fuera de `node_modules`.

---

## 5. Metodología de diagnóstico (reusable)

Ante cualquier "comando no encontrado" tras un crash o corte de energía:

```
1. command -v <bin> && echo $PATH
   → ¿el PATH tiene la ruta correcta? (verificar, no asumir)

2. npm ls -g / pacman -Qs / gestor correspondiente
   → ¿el gestor de paquetes CREE que está instalado?

3. ls -la <ruta_esperada_del_binario>
   → ¿el archivo/symlink existe físicamente en disco?

4. journalctl -b -1 | grep -iE "orphan|fsck|error|remount-ro"
   → ¿hubo corrupción de filesystem en el último boot?
```

El paso 4 es el que más se omite y el que dio la respuesta real en este caso.

### Árbol de decisión usado

```
claude: command not found
        │
        ▼
¿npm ls -g muestra el paquete? ──No──> reinstalar
        │ Sí
        ▼
¿el binario existe en disco? ──No──> symlink roto/faltante → npm install -g de nuevo
        │ Sí
        ▼
¿.zshrc tiene el export del PATH? ──No──> agregar export
        │ Sí
        ▼
¿source ~/.zshrc lo resuelve? ──No──> revisar journalctl/dmesg (corrupción FS)
```

---

## 6. Medida preventiva: SysRq habilitado

Para evitar futuros cortes abruptos que generen inodos huérfanos, se configuró **Magic SysRq**:

```bash
# habilitación inmediata (root)
echo 1 > /proc/sys/kernel/sysrq

# persistencia tras reboot
echo "kernel.sysrq = 1" >> /etc/sysctl.d/99-sysctl.conf
```

El valor `1` habilita el bitmask completo (Arch trae por defecto `16`, que solo permite `sync`).

### Secuencia REISUB para futuros freezes

Ante un cuelgue similar, en vez de mantener presionado el botón de encendido, usar:

Mantener `Alt+SysRq` y presionar en orden, una tecla a la vez:

```
R → reclaim teclado (raw mode)
E → terminar procesos (SIGTERM)
I → matar procesos (SIGKILL)
S → sync de disco a memoria
U → remount de filesystems en solo-lectura
B → reboot
```

Esto ejecuta un shutdown ordenado a nivel de kernel en segundos, evitando el corte abrupto que causó la pérdida de inodos en este incidente.

---

## 7. Pendientes / no resueltos en esta sesión

- [x] Investigar causa del freeze (30-08-26): journald persistente confirmado (`/var/log/journal`, boots desde 30-06-26). Boot del incidente = boot -8 (11-08 17:xx a 22:18:23). Corte abrupto, sin target de shutdown. **Sin ningún mensaje i915/drm/hang/reset/thermal/OOM antes del corte** — última línea es un broken pipe de `cosmic-notifications` a las 22:18:23, después nada. Hipótesis original (bug i915 en transición batería crítica) **descartada por falta de evidencia**: un hang de driver i915 loguea "Resetting chip"/GPU HANG, y no aparece. Más compatible con lockup duro de sistema completo (causa aún no identificada — hw/interrupt/térmico no logueado) que con fallo aislado del driver de video.
- [x] Verificar symlinks/binarios (30-08-26): sin roturas en `~/.npm-global`, `~/.local/bin`, `~/.nvm`, `~/.claude`, `/usr/local/bin`, `/usr/lib/node_modules`, ni `node_modules/.bin` de proyectos activos en `~/Codes`. `claude` actual (`~/.nvm/versions/node/v24.14.1/bin/claude`) sano. `claude` fue la única víctima del barrido de inodos huérfanos.
- [ ] **Mitigación adoptada:** `kernel.sysrq = 1` ya activo en el sistema. Próximo freeze → usar **REISUB** (Alt+SysRq+R-E-I-S-U-B: sync + remount ro + unmount ordenado) en vez de mantener botón de encendido. Evita el corte abrupto que causó la pérdida de inodos y preserva el journal completo para diagnóstico real.
