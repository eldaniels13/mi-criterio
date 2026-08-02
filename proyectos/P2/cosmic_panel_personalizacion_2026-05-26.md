# COSMIC Panel — Personalización y Filtro Luz Azul
**Fecha:** 2026-05-26
**Host:** fibonacci (Dell Latitude 5400)
**DE:** COSMIC (Wayland) — alpha
**Motivo:** Limpiar botones no usados del panel, formato de reloj personalizado, toggle de filtro de luz azul en todos los monitores

---

## Cambios aplicados

| Componente | Antes | Después |
|---|---|---|
| Panel zona status | A11y, Status Area, Tiling, Audio, BT, Net, Bat, Notif, Power | Sin A11y, sin Status Area (resto igual) |
| Reloj | Formato default COSMIC | `dd-mm-yy \| hh:mm:ss` |
| Filtro luz azul | Inexistente | Toggle vía Super+N o icono en panel (zona launcher) |
| Sync brillo externos | Manual | Manual (descartado — ver veredicto) |

---

## Veredicto DDC/CI (sync de brillo a monitores externos)

**Descartado sin instalar.** Investigación previa indicó probabilidad baja (~20%) por dos factores combinados:

- **Yodoit 15.6" portátiles:** documentación oficial no menciona DDC/CI; monitores portátiles de bajo costo casi nunca implementan el chip controlador.
- **UGREEN Revodok Pro 210:** sin documentación de passthrough DDC/CI. Issue #444 de `rockowitz/ddcutil` reporta que el Pro 308 (modelo hermano) falla con 2 monitores simultáneos.

Decisión: dejar brillo externos manual. No se invirtió tiempo en armar el sync.

---

## Archivos modificados/creados

```
~/.config/cosmic/com.system76.CosmicPanel.Panel/v1/plugins_wings        # quitados A11y + StatusArea
~/.config/cosmic/com.system76.CosmicAppletTime/v1/format_strftime       # nuevo, contiene "%d-%m-%y | %H:%M:%S"
~/.config/cosmic/com.system76.CosmicAppList/v1/favorites                # añadido "bluelight-toggle"
~/.config/cosmic/com.system76.CosmicSettings.Shortcuts/v1/custom        # añadido Super+N → toggle script
~/.local/bin/blue-light-toggle                                          # script bash, +x
~/.local/share/applications/bluelight-toggle.desktop                    # entrada .desktop
```

**Backup completo previo a los cambios:** `~/.config/cosmic/_backup_20260526_071155/`

---

## Detalle técnico: clave oculta `format_strftime`

El applet `cosmic-applet-time` expone solo 4 toggles en cosmic-settings UI (`military_time`, `show_seconds`, `show_date_in_top_panel`, `first_day_of_week`). Sin embargo, el binario contiene strings adicionales no documentadas: `format_strftime` y `show_weekday`.

Creando manualmente `~/.config/cosmic/com.system76.CosmicAppletTime/v1/format_strftime` con un string strftime entre comillas, el applet lo respeta. Formato strftime estándar (POSIX): `%d` día, `%m` mes, `%y` año 2-dig, `%H` hora 24h, `%M` min, `%S` seg.

---

## Detalle técnico: toggle luz azul

- **Tool:** `gammastep` (instalado desde repo extra de Arch).
- **Modo:** one-shot. `gammastep -O 3500` aplica temperatura y sale; `gammastep -x` la resetea.
- **Estado:** rastreado con archivo en `$XDG_RUNTIME_DIR/bluelight.on` (se borra al reboot → estado fresco en cada sesión).
- **Cobertura:** gammastep aplica gamma a todos los outputs que el compositor Wayland gestiona — eDP-1 + DP-3 + DP-4 (laptop + 2 Yodoit), sin configuración adicional.
- **Limitación:** ajusta gamma (la imagen tira a naranja), NO el backlight físico del monitor. El consumo no cambia. Pero el efecto sobre los ojos sí.

**Pendiente conocido:** COSMIC alpha no permite un applet de panel custom que ejecute scripts arbitrarios y muestre estado en zona "status". Por eso el toggle vive como pin en zona launcher + atajo de teclado. Revaluar cuando COSMIC pase a beta/stable.

---

## Comandos de mantenimiento

```bash
# Toggle manual
~/.local/bin/blue-light-toggle

# Verificar estado actual
test -f "$XDG_RUNTIME_DIR/bluelight.on" && echo ON || echo OFF

# Forzar apagado
gammastep -x

# Recargar panel sin reiniciar sesión (SOLO esto, no arrancarlo manual)
pkill -x cosmic-panel
```

---

*Sesión completada: 2026-05-26, ~07:35 CST*
