# Memoria del Sistema — Claude Code · eldaniels

> **Qué es este archivo.** Migración completa y sin pérdida de toda la memoria que
> Claude Code guardaba fuera de este repo, traída a `mi-criterio/` porque confías
> más en el contenido de esta carpeta.
>
> **Dos fuentes de origen:**
> 1. **Memoria de archivos** — `~/.claude/projects/-home-eldaniels/memory/` (feedback, proyectos, usuario).
> 2. **claude-mem** — base de observaciones cruzadas entre sesiones (50 observaciones, may–jun 2026).
>
> **Generado:** 2026-06-27 · **Host:** fibonacci (Dell Latitude 5400) · COSMIC DE / Arch Linux.
> Identificadores sensibles de hardware (seriales, MAC, UUID, coords precisas) redactados
> por política `feedback-hide-sensitive-info`.

---

## Índice

1. [Batería y energía (TLP)](#1-batería-y-energía-tlp)
2. [Preferencias de trabajo (feedback)](#2-preferencias-de-trabajo-feedback)
3. [Perfil de usuario](#3-perfil-de-usuario)
4. [Stack de IA local](#4-stack-de-ia-local)
5. [Filtro de luz azul / night light en COSMIC](#5-filtro-de-luz-azul--night-light-en-cosmic)
6. [Panel COSMIC, dock y atajos](#6-panel-cosmic-dock-y-atajos)
7. [Shell, zsh y aliases del sistema](#7-shell-zsh-y-aliases-del-sistema)
8. [Seguridad y hardening](#8-seguridad-y-hardening)
9. [safe-eject y gestión de dispositivos](#9-safe-eject-y-gestión-de-dispositivos)
10. [Plan de optimización del sistema](#10-plan-de-optimización-del-sistema)
11. [Mantenimiento: updates y auditoría](#11-mantenimiento-updates-y-auditoría)
12. [Índice de sesiones (claude-mem)](#12-índice-de-sesiones-claude-mem)

---

## 1. Batería y energía (TLP)

**Estado de la batería (medido 2026-06-20):**

| Dato | Valor |
|---|---|
| Batería | Dell (serial redactado) |
| Capacidad de diseño | 8948 mAh |
| Carga completa actual | 5957 mAh |
| **Salud de la batería** | **66.6 %** (degradada) |
| Carga al momento del chequeo | 14.1 %, descargando |

**TLP instalado y activo (obs 1748, 2026-06-20):**

- **TLP 1.10.1** instalado y habilitado con `sudo systemctl enable --now tlp`.
- Umbrales de carga Dell configurados vía driver **natacpi (dell_laptop)**:
  - `START_CHARGE_THRESH` = **50 %**
  - `STOP_CHARGE_THRESH` = **80 %**
  - (configuración común para alargar la vida de la batería)
- Rangos válidos del plugin Dell: START 50–95 %, STOP 55–100 %.
- `tlp.service` se "canceló" justo tras habilitar (probablemente arranque limpio en modo oneshot o conflicto menor — verificar con `tlp-stat -s`).
- **`powertop` NO está instalado** (`sudo powertop: command not found`). Pendiente si se quiere análisis de consumo más fino.

> **Nota de salud:** la batería ya está al 66.6 % de su capacidad de diseño. Los umbrales
> 50–80 % frenan la degradación pero no la revierten. Reemplazo futuro a considerar.

---

## 2. Preferencias de trabajo (feedback)

Reglas de cómo Claude debe trabajar contigo. Todas confirmadas por ti explícitamente.

### 2.1 Explicar antes de instalar o ejecutar
Antes de cualquier comando que instale, modifique el sistema o cargue módulos, explicar:
1. Qué es exactamente lo que se va a ejecutar.
2. Por qué es la mejor opción para el objetivo.
3. Qué alternativas existen y por qué no son tan buenas.

Aplica a `sudo`, `pacman`, `modprobe`, `pip install`, `npm install` y cualquier comando con efecto en el sistema. Explicar primero, ejecutar después con tu aprobación.
**Por qué:** quieres aprender y entender cada decisión, no solo ver comandos.

### 2.2 Explicar siempre `sudo`
Siempre que se use `sudo`, explicar antes de ejecutar:
1. Qué hace el comando específico.
2. Por qué necesita privilegios de root.
3. Qué riesgo tiene (si lo hay).
4. Si existe alternativa sin sudo (ej. agregar usuario a un grupo).

Terminar siempre con el comando listo para copiar/pegar — **no ejecutarlo yo mismo**.
**Por qué:** lo pediste explícitamente — quieres entender el modelo de privilegios de Linux.

### 2.3 Explicar en español amigable para principiantes
Explicar conceptos técnicos siempre en español, accesible para quien está aprendiendo. Usar analogías del mundo real. El código y los comandos pueden quedar en inglés técnico, pero la explicación alrededor siempre en español claro.
**Por qué:** el español es tu idioma nativo y prefieres entender el "por qué".

### 2.4 Delegar tareas a la IA local cuando se pueda
Cuando una tarea la pueda manejar bien el stack local (Ollama + Open WebUI + modelo local), proponer delegarla y entregar un **prompt listo para copiar-pegar** en Open WebUI (`http://localhost:8080`).

**Delegables al local** (deepseek-coder:6.7b, CPU, 30s–2min/respuesta): chat general, brainstorming, Q&A, resúmenes, traducciones, reformulaciones, explicación de código corto (<100 líneas, 1 archivo), snippets, regex, queries SQL simples, drafts de texto, cover letters, emails, RAG sobre mi-criterio.

**NO delegar al local:** refactor multi-archivo, debugging sutil, arquitectura compleja, tareas agénticas (leer/editar archivos en vivo), iteración rápida, contexto >16k tokens.

El prompt debe ser autocontenido (el local no ve la conversación), incluir contexto inline, pedir formato concreto si importa, y estar en español.
**Por qué:** estás construyendo soberanía AI y quieres maximizar el local para ahorrar créditos de IA rentada. Cada tarea delegada = ahorro real + práctica del stack.

### 2.5 Ocultar información sensible en documentos
Nunca escribir identificadores sensibles directamente en documentación, logs o cualquier archivo de mi-criterio. Redactar o generalizar antes de escribir:
- MAC reales → omitir o "la MAC real del hardware".
- UUID de LUKS/disco → `<uuid>`.
- IP públicas/reales → `<IP>`.
- Contraseñas, tokens, llaves → `<redacted>`.
- Nombres de red internos sensibles → etiquetas genéricas.

**Por qué:** estos archivos pueden ir a git, compartirse o indexarse. MAC/UUID pueden identificar el dispositivo o ayudar a ataques dirigidos. Escanear el contenido antes de cada Edit/Write.

---

## 3. Perfil de usuario

- **Gestor de contraseñas:** usa **Keeper Security**, ya configurado y en uso diario activo. **No sugerir alternativas** (Bitwarden, KeePassXC, 1Password, ProtonPass) salvo que pidas explícitamente comparación o migración. La gestión de contraseñas es una parte resuelta de tu stack.

> El perfil maestro completo (identidad, perfil cognitivo, stack técnico, financiero,
> vocacional, cultural) vive en `perfil_maestro_eldaniels_v2.txt` y en el `CLAUDE.md` global.

---

## 4. Stack de IA local

**Veredicto y estado (2026-05-18) — fuente: `project_local_ai.md` + obs 1097.**

### Lo construido y funcionando
- **Ollama** en `127.0.0.1:11434` con `OLLAMA_KEEP_ALIVE=30m`, `OLLAMA_NUM_THREAD=8`.
- **deepseek-coder:6.7b** como modelo principal (chat + código), confirmado vía Open WebUI.
  *(Nota: el `~/.zshrc` posteriormente define `OLLAMA_MODEL=qwen2.5-coder:7b` como default con switcher fzf en Alt+P — ver §7.)*
- **nomic-embed-text** instalado para embeddings RAG.
- **Open WebUI v0.9.5** en `http://localhost:8080` — chat web funcional, integración nativa Ollama.
- **Aider** instalado pero bloqueado por timeout litellm 600s → deprioritizado.
- Hardware: Dell Latitude 5400, i7-8665U, 32 GB RAM, CPU-only, ~13 GB libres en root.

### Funciona 100 % offline
Sí — en avión, sin wifi, sin VPN. Todo es localhost. Cero telemetría, cero API keys.

### Veredicto: qué reemplaza, qué no
- **✅ REEMPLAZA:** ChatGPT para chat general, brainstorming, Q&A; RAG sobre mi-criterio; escritura, traducción, explicación de código corto; trabajo reflexivo donde 30s–2min/respuesta es aceptable.
- **⚠️ COMPLEMENTA (no reemplaza):** Claude Code / Opus / Sonnet para programación seria, razonamiento multi-archivo, síntesis larga, debugging sutil.
- **❌ NO HACE:** agéntico real (no ejecuta herramientas, no edita archivos solo), tiempo real estilo Claude Code, contexto >16k tokens cómodo (Claude maneja 200k).

### Limitaciones (CPU-only)
- Latencia 30s–2min/respuesta. Modelo 6.7B ≈ GPT-3.5 en buen día. Modelos >7B densos o >16B MoE = 2–10 min = no es workflow.

### Path de upgrade (zero-migration software)
eGPU TB3 + RTX 3060 12GB usada (~$500 USD) → 10–15× speedup. Mismo Ollama, mismo Open WebUI, solo cambiar `model:`. Modelos viables tras GPU: `qwen2.5-coder:32b`, `deepseek-r1:14b`, `deepseek-coder-v2:16b`.

### Filosofía de uso
**Stack híbrido, no uno-u-otro.** Local para tareas que cubre bien (ahorro real). IA rentada (Claude) cuando el salto de calidad justifica el costo. La soberanía está en TENER la opción local funcionando, no en abandonar lo rentado.

### Próximos pasos
- Crear knowledge collection "mi-criterio" en Open WebUI (5–10 archivos clave primero).
- Validar workflow RAG con queries específicas.
- Documentar prompts útiles en `mi-criterio/proyectos/P2`.
- Postponed: resolver timeout Aider, evaluar eGPU cuando haya budget.
- No volver a sugerir Open Interpreter (descartado por bug cosmic-term).

> Veredicto detallado y bitácora en `~/Codes/mi-criterio/proyectos/P2/stack_ia_local_veredicto.md`.

---

## 5. Filtro de luz azul / night light en COSMIC

> Historia larga y con giros. Resumen ejecutable primero, hallazgos cronológicos después.

### Resumen ejecutable
- Existe un script **`~/.local/bin/blue-light-toggle`** (con guiones) que togglea un filtro de luz azul a **3500 K** vía gammastep.
- Estado en `${XDG_RUNTIME_DIR}/bluelight.on` (= `/run/user/1000/bluelight.on`); el archivo se borra al reiniciar → arranca apagado cada boot.
- Atajo COSMIC: **Super+N** → `Spawn(/home/eldaniels/.local/bin/blue-light-toggle)`.
- Tiene `.desktop` launcher y estaba pineado en favoritos del dock (luego removido, ver §6).
- **El script fue fijado al backend DRM** con `METHOD="drm:card=1"` (obs 1766).

### ⚠️ Advertencia crítica de funcionamiento
**gammastep NO controla la gamma de forma fiable en COSMIC/Wayland.** Hallazgos clave:
- COSMIC (`cosmic-comp 1.0.16-1`) **no implementa el protocolo `zwlr_gamma_control_v1`** (obs 1777, 1778). Por eso el método Wayland de gammastep falla.
- gammastep imprime "Failed to start adjustment method: wayland" pero **sale con código 0**, y el script usa `|| true`, así que **el fallo queda oculto** y el script aparenta funcionar (obs 1753).
- El método DRM de gammastep **hardcodea `/dev/dri/card0`**, pero el sistema solo tiene `card1` → falla "No such file or directory" (obs 1756). No acepta flag `-d` (obs 1755). Sí acepta `-m drm:card=1` (obs 1763, 1764).
- **DRM con `card=1` SÍ funcionó** (exit 0, 4000 K aplicado) pese a que eldaniels **no está en el grupo `video`** — acceso vía permisos de sesión logind/seat (obs 1764). Por eso el script quedó fijado a `drm:card=1`.
- `gammastep -p` reporta el estado del daemon, no el registro DRM real → tras `-O 3500` sigue diciendo 6500 K aunque el cambio físico pueda haberse aplicado (obs 1775). No fiable para verificar.
- gammastep detecta ubicación región de Guadalajara (coords precisas redactadas) para modo día/noche automático; neutral 6500 K, noche default 4500 K (obs 1761, 1774).

### Night light nativo de COSMIC: NO existe (investigación a fondo)
- `cosmic-settings 1.0.16-1` **muestra un panel "Night light" traducido a 8+ idiomas** (Luz nocturna, Mode nuit, Nachtlicht…) — la UI existe (obs 1783).
- Pero `cosmic-comp` **no tiene el backend**: sin `zwlr_gamma_control_v1`, sin namespace D-Bus, sin clave de config (obs 1780, 1781, 1782). → La UI aparece pero **el compositor no aplica el cambio**. Esto explica el "no funciona".
- Las cadenas "night" en el binario de cosmic-settings resultaron ser nombres de colores CSS (ej. "nightblue"), no identificadores de feature (obs 1786).
- Config de `cosmic-comp` (`~/.config/cosmic/com.system76.CosmicComp/v1/`, 15 archivos) **no tiene clave night light**; `appearance_settings` solo tiene clip/shadow de ventanas (obs 1781, 1782).
- **Conclusión:** night light no está implementado funcionalmente en COSMIC 1.0.16-1. Ningún tool basado en wlr-gamma-control (gammastep, wlsunset) puede funcionar sin actualización del compositor.

### Candidato de reemplazo
- **`wl-gammarelay-rs`** (AUR, v1.0.1-1, +14 votos): interfaz **DBus** para temperatura/brillo en Wayland, "sin parpadeo". Compañero: `wl-gammarelay-applet-git`. Es el candidato más probable para reemplazar gammastep en el toggle (obs 1757). El script tendría que llamar a su interfaz DBus en vez de la CLI de gammastep.

### Permisos relevantes
- `/dev/dri/card1` con permisos `0660` root:video (gid 983). eldaniels solo está en grupos `eldaniels` y `wheel` — **no en `video` ni `render`** (obs 1754, 1760). Aun así DRM card=1 funcionó vía logind seat.

---

## 6. Panel COSMIC, dock y atajos

### Objetivo de personalización (obs 1758)
Reemplazar los botones del panel por: **indicador de número de workspace** + **porcentaje de batería**.

### Entorno confirmado (obs 1759)
- DE: **COSMIC by System76** sobre Wayland (`wayland-1`).
- Config bajo `~/.config/cosmic/` con subdirectorios reverse-domain (`com.system76.Cosmic*`).
- Customización debe usar applets/config de COSMIC, **no Polybar/Waybar/i3bar**.

### Dock / favoritos
- Config: `~/.config/cosmic/com.system76.CosmicAppList/v1/favorites` (array JSON de strings).
- Apps pineadas eran: spotify, firefox, org.mozilla.Thunderbird, codium, bluelight-toggle.
- **Se removió `bluelight-toggle`** del dock (obs 1790) → quedaron 4: spotify, firefox, Thunderbird, codium. Petición tuya: *"solo limpia boton del dock"* (cambio quirúrgico, nada más tocado).

### ⚠️ Cómo reiniciar el panel correctamente (feedback `cosmic-panel-restart`)
Para recargar config del panel basta con:
```bash
pkill -x cosmic-panel
```
**NO** ejecutar `nohup cosmic-panel &` después — **cosmic-session lo reinicia solo** en 1–3 s. Si lo arrancas manualmente terminas con **2 paneles superpuestos**. Verificar con `pgrep -af '^cosmic-panel$'` que hay exactamente 1 proceso.
**Por qué:** en sesión 2026-05-26 reportaste "panel is duplicated" tras `pkill … nohup cosmic-panel`. (Confirmado de nuevo en obs 1791: editar favoritos requiere reinicio del panel, que se auto-relanza.)

### Decisión: NO scripts de automatización de ventanas (obs 1749)
Rechazaste explícitamente scripts de automatización de workspace/ventanas:
> "I do not want Workspace automation script. I like to open windows based on how I use them."

Prefieres gestión manual de ventanas según tu uso. **No sugerir ni implementar automatización de ventanas.**
*(Contexto: Firefox se lanza vía firejail sandbox, perfil `/etc/firejail/firefox.profile`; warnings menores de xdg-dbus-proxy y AppArmor, pero corre bien.)*

---

## 7. Shell, zsh y aliases del sistema

**Mapa de `~/.zshrc` (obs 1767, 1771, 1792):**

- `~/.local/bin` prepended al PATH → scripts como `blue-light-toggle` ejecutables por nombre.
- Prompt **starship**, **nvm** para Node, plugins `zsh-autosuggestions` y `zsh-syntax-highlighting` desde `/usr/share/zsh/plugins/`.
- **EDITOR** = `cosmic-text-editor`.
- **Ollama:** `OLLAMA_MODEL=qwen2.5-coder:7b` default; switcher fzf con 4 modelos en **Alt+P**. Env: `OLLAMA_HOST=127.0.0.1:11434`, `OLLAMA_API_BASE=http://localhost:11434`, `OLLAMA_KEEP_ALIVE=30m`, `OLLAMA_NUM_THREAD=8`.
- **SSH agent** en `$XDG_RUNTIME_DIR/ssh-agent.socket`; hook `chpwd` auto-carga `~/.ssh/id_github_fibonacci` al entrar a `~/Codes/`.
- Bindkeys Ctrl/Shift + flechas para navegación palabra/línea (compatibilidad cosmic-term).
- `~/.zshrc` ≈ 108 líneas; bloque de aliases desde la ~99/100.

**Aliases del sistema (obs 1768, 1792):**

| Alias | Hace |
|---|---|
| `update` | `sudo pacman -Syu && yay -Syu` (oficial + AUR) |
| `cleanup` | **función** (ver abajo) — antes era alias destructivo |
| `refresh` | `source ~/.zshrc && echo "Shell recargado"` |
| `secaudit` | auditoría 4-en-1: `journalctl -p 3` (errores), `ss -tlnp` (puertos), `lastb` (logins fallidos), `pacman -Qkk` (archivos faltantes) |
| `claude-mem` | `bun ".../claude-mem/12.1.0/scripts/worker-service.cjs"` |
| `run-help`→`man`, `which-command`→`whence` | compat zsh |

### `cleanup`: de alias ciego a función con confirmación (obs 1770, 1772)
**Decisión tuya:** prefieres limpieza **deliberada** sobre limpieza ciega — entender qué se borra antes de borrarlo.

- **Antes (peligroso):** `cleanup` = `sudo pacman -Rns $(pacman -Qtdq); sudo pacman -Sc --noconfirm` sin preview ni confirmación.
- **Ahora (`~/.zshrc` línea ~102, función de 18 líneas):**
  1. Junta los huérfanos en una variable; si no hay, sale con mensaje amable.
  2. Imprime la lista de paquetes a remover.
  3. Pregunta `¿Continuar? (y/n)` antes de tocar nada.
  4. Solo tras `y` ejecuta `pacman -Rns` y `pacman -Sc --noconfirm`.
  5. Muestra ✓/✗ por paso.
- `cleanup` es **función** sourceada desde `~/.zshrc`, no alias (obs 1793).

---

## 8. Seguridad y hardening

**Stack de seguridad personal (obs 1769):**
- **Firejail:** sandbox SUID que restringe apps no confiables vía namespaces de Linux + seccomp-bpf. Verificar con `firejail --list` (procesos sandboxed) y `firejail --tree` (jerarquía).
- **MAC randomization:** evita rastreo en Wi-Fi ciclando el identificador de hardware. Confirmar con `ip link show` o `wifi.cloned-mac-address=random` en NetworkManager.
- **Principio "no corres cualquier cosa":** superficie de ataque mínima — solo binarios verificados, nada de scripts arbitrarios.
- **Verificación de postura:** reglas de firewall (ufw/iptables), aislamiento de procesos, DNS leak tests, MAC randomization activa.
- **"Cleanup" de privacidad:** limpiar cache/cookies, flush DNS, temp files, historial bash/zsh, revocar permisos/tokens sin uso.

**Auditoría `secaudit` del 2026-06-20 (obs 1796):** hallazgos esperados en workstation de desarrollo, sin problemas serios:
- `openssl`: mismatch de permisos en `/etc/ssl/private` (posible hardening menor a revisar).
- `ollama`: mismatch UID/GID en `/var/lib/ollama` (normal, corre bajo usuario de servicio dedicado).
- `systemd`: mismatch GID en `/var/log/journal`.
- `rkhunter`, `ghc-libs`: mismatches esperados tras updates.
- `/etc/resolv.conf`: "File type mismatch" (típico con systemd-resolved vía symlink).
- Backups de config esperados: fstab, passwd, sudoers, pacman.conf, grub, mkinitcpio.conf.
- Solo **2 logins fallidos**, ambos del 2026-05-23 en tty3 — sin actividad de fuerza bruta reciente.
- Puertos escuchando: ollama `127.0.0.1:11434`, bun `127.0.0.1:37777`, Spotify `0.0.0.0:48951` y `:57621` (único en wildcard, esperado por descubrimiento de red local).

---

## 9. safe-eject y gestión de dispositivos

**Estado del proyecto safe-eject (post-reboot 2026-04-20) — fuente `project_safe_eject_state.md`.**

### Listo (no tocar)
- Script `~/.local/bin/safe-eject` — completo, funcional, con picker fuzzel, modo directo y `--list`.
- Atajo COSMIC: **Super+Shift+E** → spawn del script.
- Desktop entry: `~/.local/share/applications/safe-eject.desktop`.
- `~/.local/bin` en PATH (`.zshrc`).
- Dependencias instaladas: jq, lsblk, udisksctl, notify-send, fuzzel, veracrypt.

### Por qué se reinició aquella vez
El kernel se actualizó `6.19.11-arch1-1` → `6.19.12-arch1-1` sin reiniciar. Los módulos en disco eran de 6.19.12 pero el kernel corriendo era 6.19.11 → desincronización → `modprobe mmc_block` falló con "Module not found".

### Pendiente tras reinicio (puede que ya resuelto — verificar)
1. **Verificar micro SD:** slot lateral del Dell; debe aparecer como `/dev/mmcblk0`. Chequear `lsblk | grep mmc`.
2. **Renombrar dispositivos USB** a labels reconocibles:

   | Dispositivo | Qué es | Label | Notas |
   |---|---|---|---|
   | `sda` | Kingston DataTraveler USB 57.7G | `ARCH_202604` | ISO9660 read-only — no se puede renombrar fácil (re-grabar ISO) |
   | `sdb2` | Kingston NV3 M.2 en carcasa USB 465.7G | `Kingston NV3` | NTFS → renombrar con `ntfslabel` |
   | `mmcblk0` | Micro SD 128GB | desconocido | pendiente detectar formato |
3. **Probar safe-eject en vivo:** Super+Shift+E con dispositivos conectados, verificar picker fuzzel.

---

## 10. Plan de optimización del sistema

**Plan para Dell Latitude 5400 / COSMIC DE / dual-monitor (obs 1711, 2026-06-19).**

Hardware: i7-8665U, dual monitores vía hub UGREEN Thunderbolt 3, zsh, yay para AUR.

**Implementaciones prioritarias (bajo esfuerzo, alto impacto):**
- ✅ **TLP** para batería (hecho — ver §1).
- **autorandr** para config dual-monitor persistente entre reinicios/reconexiones.
- **brightnessctl** para control de brillo.
- **lm_sensors** para monitoreo de temperatura.
- **Deshabilitar Wi-Fi power saving** vía NetworkManager para estabilidad en este hardware.
- Aliases útiles de zsh (hecho — ver §7).

**Instalación inmediata sugerida:** `tlp brightnessctl htop autorandr lm_sensors` vía pacman.

**Otros (menor prioridad):**
- Thunderbolt puede requerir autorización manual vía `boltctl`.
- Mantenimiento mensual: `pacman -Syu`, limpieza de cache, revisión `journalctl` de errores, backup de `~/.config`.
- Estrategia de workspaces: WS1 navegador+mail, WS2 terminal+editor, WS3 media. *(Nota: rechazaste automatizar esto — ver §6.)*
- tmux para uso intensivo de terminal con split panes.

---

## 11. Mantenimiento: updates y auditoría

**Update masivo del 2026-06-20 (obs 1794, host fibonacci):** repos pacman sin cambios; 7 paquetes AUR actualizados, todas las build/test suites pasaron limpio:
- `python-mcp` 1.27.2 → 1.28.0 (1130 tests pasaron, 95 skipped, 1 xfailed).
- `python-sse-starlette` 3.4.4 → 3.4.5 (77 tests).
- `yay` 12.5.7 → 13.0.1 (salto de versión mayor).
- `rider` 2026.1.2 → 2026.1.3 (descarga de 1.95 GB).
- `google-chrome` 149.0.7827.53 → .155.
- `input-remapper` 2.2.0 → 2.2.1.
- `spotify` 1.2.90 → 1.2.92.
- `python-oslex` marcado "Out Of Date" en AUR, no actualizado.
- Cleanup iniciado pero cancelado por ti.

**Crash conocido (obs 1795):** el applet bluetooth de COSMIC (`cosmic-panel-bu`, PID 304707) dumpeó core el 2026-06-20 17:59:44 — panic de Rust (path abort) en cosmic-applets. Errores bluetooth posteriores ("br-connection-busy", "br-connection-page-timeout"). `cosmic-panel` siguió corriendo. Probable bug upstream de COSMIC, no problema de seguridad.

---

## 12. Índice de sesiones (claude-mem)

Resúmenes de sesión (one-liners) para trazabilidad. El detalle de cada una está en las observaciones citadas arriba.

| ID | Fecha | Tema |
|---|---|---|
| S151 | May 25 | Aclaración de working directory correcto (¿debió ir en `~/Codes/mi-criterio/P2`?) |
| S152 | May 25 | Customización panel COSMIC + control unificado de brillo + toggle luz azul (laptop + dual Yodoit) |
| S181 | May 25 | Panel COSMIC: indicador de workspace + porcentaje de batería |
| S182 | Jun 19 | Análisis y priorización de optimizaciones Linux para Dell Latitude 5400 / COSMIC dual-monitor |
| S186 | Jun 19 | Panel: workspace + batería; fix de blue-light-toggle; aliases zsh |
| S187 | Jun 20 | Análisis de uso de sudo en aliases — evaluación de seguridad y riesgos |
| S188 | Jun 20 | Explicación de hardening (Firejail, MAC randomization, redes confiables) + qué hace `cleanup` |
| S189 | Jun 20 | Night light ausente de settings COSMIC — investigación y workaround |
| S190 | Jun 20 | Update Arch vía yay + auditoría de seguridad (secaudit) en fibonacci |
| S191 | Jun 20 | Acceso a claude-mem (memoria cross-session) |

---

## 13. Hallazgos de sistema — agosto 2026

### 13.1 `dmidecode` era la herramienta equivocada (2026-08-06)

`/sys/class/dmi/id/` es **legible por cualquier usuario** — el firmware nunca necesitó root.
`hwinfo` mostraba `FIRMWARE: BIOS () · Board` vacío porque usaba `dmidecode -t 0 / -t 2`,
que falla en silencio sin privilegios.

`MEMORY` estaba vacío por una causa **distinta**: `dmidecode -t 17` (detalle por DIMM: tipo,
velocidad, slot) sí requiere root de verdad. Además, el bucle que imprimía las líneas de DIMM
no emitía salto de línea cuando no había datos → `GPU:` se pegaba sobre el renglón de `MEMORY:`.

| Dato | Fuente correcta | ¿Root? |
|---|---|---|
| BIOS version/date, vendor, product, board | `/sys/class/dmi/id/*` | no |
| Total/usado de RAM, swap | `/proc/meminfo` | no |
| Tipo/velocidad/slot por DIMM | `dmidecode -t 17` | **sí** |

**Lección transferible:** antes de asumir "esto necesita sudo", comprobar si el kernel ya
expone el dato por sysfs/procfs.

### 13.2 Edits a `~/.local/bin/hwinfo` (2026-08-06)

- **FIRMWARE** — `dmidecode` → `/sys/class/dmi/id/*`. Rinde sin root:
  `BIOS 1.33.0 (08/08/2024) · Dell Inc. Latitude 5400 · Board 0PD9KD`.
- **MEMORY** — `/proc/meminfo` (`MemTotal`/`MemAvailable`) + barra de uso + línea de swap.
  Detalle por DIMM sólo si `EUID == 0`; corregido el salto de línea que rompía el layout.
- **STORAGE** — barra por punto de montaje (`/`, `/home`, `/boot`) vía
  `df --output=target,used,size,pcent`, bajo la línea del dispositivo.
- **Nueva función `bar()`** — ancho 20, porcentaje centrado dentro. Umbrales:
  verde <75 %, amarillo 75–89 %, rojo ≥90 %. Fallback ASCII `[###---] 69%` sin TTY.
- **THERMAL** — marca `[!] thermal throttle range` a partir de 85 °C.

### 13.3 Caché de pacman: 17 GB sin podar (2026-08-06)

`/` (LV `vg0-lv_root`, 49 GB) llegó al **98 %** y `pacman` abortó:
`error: Partition / too full: 407724 blocks needed, 360111 blocks free`.
Causa: `/var/cache/pacman/pkg` con **17 GB / 9013 archivos** para sólo 1496 paquetes
instalados — nunca se purgó desde la instalación.

`sudo pacman -Sc` liberó ~14 GB (46 G → 32 G usados, 69 %). Los errores
`could not open file .../download-XXXX: Error reading fd 7` son inofensivos: restos de
descargas parciales que pacman no sabe leer como paquete.

**Causa estructural (sin resolver):** `lv_root` de 49 GB aloja `/usr` (16 G) + `/var` +
`/opt` (7.2 G), mientras `lv_home` tiene 415 GB al 22 %. Recurrirá.
**Restricción del usuario:** NO redimensionar el NVMe — mala experiencia previa. Decisión
respetada; la mitigación es podar caché + no acumular, no reparticionar.

### 13.4 Fallo intermitente de contraseña en `sudo` (2026-08-06) — SIN RESOLVER

Síntoma: `sudo` rechaza la contraseña correcta. El usuario creía que sólo se arreglaba
forzando apagado con el botón de encendido.

**Refutado por el journal:** 3 intentos fallidos a las 15:23–15:24, y `sudo` funcionando
normal a las 16:06 — **sin reinicio de por medio** (boot 0 arrancó 08:52 y seguía activo).
Se resuelve solo. El apagado forzado no era la cura, sólo coincidía.

Descartado: `faillock` limpio, sin `deny=` configurado → no es bloqueo de cuenta.
Hipótesis viva: modificador de teclado atascado en COSMIC/Wayland.

> ⚠️ **Riesgo:** el apagado forzado es el mecanismo que corrompe sistemas de archivos, y ya
> hay antecedente (`P8_Backup_Wiki/mft_recovery_decision.md`). No volver a usarlo para esto.
> Alternativa: cambiar a TTY con `Ctrl+Alt+F3` y autenticar ahí. Si hace falta reiniciar de
> verdad, usar SysRq (`REISUB`) antes que el botón.

### 13.5 Origen del hardware: equipo reacondicionado

**fibonacci (Dell Latitude 5400) se compró REACONDICIONADO.** La batería pudo llegar ya
usada de fábrica — la salud de **66.6 %** no implica degradación causada por el uso del
usuario, y el número real de ciclos es desconocido. Contexto necesario para no diagnosticar
mal el desgaste ni la gestión de energía (ver §1, TLP).

Térmicas 2026-08-06: **87–92 °C bajo carga** (crítico a 100 °C), **58 °C en reposo**. El pico
bajo carga en un equipo de 2019 apunta a limpieza de ventiladores y cambio de pasta térmica
— arreglo físico, no de software.

### 13.6 Exposición a "Atomic Arch" (AUR, junio 2026): **NEGATIVA**

Verificado 2026-08-06 contra el protocolo de `inbox/18-07-26_aur-atomic-arch-report.md`.
`grep -E '2026-06-1[0-6].*(installed|upgraded)' /var/log/pacman.log` en la ventana del
ataque (10–16 jun) devuelve **sólo paquetes de repos oficiales** — cero compilaciones AUR.
Los repos oficiales nunca se vieron afectados. `yay` ya está en **13.0.1** (muestra fecha de
última modificación del PKGBUILD). No se requiere rotación de credenciales.

### 13.7 `containerd` activo sin uso + `/opt/containerd` huérfano

`containerd.service` lleva **9 h corriendo** desde el arranque, pese a estar `disabled` en
preset — algo lo activa (probablemente `docker.socket`). El usuario no usa contenedores.
`/opt/containerd/{bin,lib}` existen pero están **vacíos** (fechados Apr 10) y **no pertenecen
a ningún paquete** de pacman: residuo de una instalación manual.

Contexto: la auditoría de mayo 2026 ya retiró a `eldaniels` del grupo `docker` por escalada
de privilegios. Un runtime de contenedores corriendo sin uso es superficie de ataque y
consumo inútil en un equipo con térmicas justas.

---

> **Migración completada sin pérdida.** Este archivo consolida las 10 memorias de archivo
> (`memory/`) + las 50 observaciones de claude-mem (IDs 1097, 1711, 1748–1796) + el índice
> de sesiones. Fuentes originales intactas; esta es la copia de confianza en `mi-criterio/`.
