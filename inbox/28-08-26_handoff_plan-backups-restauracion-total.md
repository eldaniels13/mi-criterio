# 28-08-26 — Plan de backups: rediseño para restauración total

**Fecha de corte:** 2026-08-28 · **Herramienta:** Claude Code (Opus 5)
**Lente(s):** P8 ingeniería/seguridad × P2 programación, P6 ayuda futuro
**Estado global:** 🔴 bloqueado — análisis hecho, rediseño no iniciado, falta inventario de datos

---

## 1 · Objetivo y motivación

**Objetivo:** que el plan de backups cumpla lo que eldaniels declaró textualmente — *"si pierdo mi
laptop (robo, avería definitiva, rotura), restaurar en una laptop/PC nueva como si nada hubiera
pasado"*. Incluye **todo**: fotos, música, archivos, trabajo, configs del sistema. Con instrucciones
de restauración escritas en español.

**Segundo objetivo (planteado por eldaniels):** analizar si `P8_Backup_Wiki/` se puede unificar en
un solo archivo.

**Motivación — qué duele hoy si esto no existe:** el plan documentado (905 líneas) describe tres
fases; sólo se ejecutaron la 0 y la 1, ambas en marzo–abril 2026. Todo lo producido desde entonces
—trabajo TME, personalización COSMIC, scripts `refresh`, hojas de finanzas, CVs, graphify— **no está
respaldado en ningún lado**. Un robo hoy es pérdida definitiva de ~5 meses de trabajo.

| Driver | Detalle |
|---|---|
| Copia única | Sólo existe `tenochtitlan` (Kingston NV3 500 GB). FASE 2 y 3 nunca arrancaron |
| Misma ubicación física | Kingston vive en casa. Un solo evento (robo, incendio) se lleva laptop y backup |
| Backup congelado | Contenedor VeraCrypt de abril 2026; bundle `~/arch-setup-backup/` del 20-jun-2026 |
| Sin automatización | Todo manual → siempre desactualizado |
| Nunca restaurado | Cero pruebas de restore. Backup no probado = estado desconocido |

---

## 2 · Estado real verificado al cerrar

| Componente | Estado | Verificado cómo |
|---|---|---|
| Inventario de `P8_Backup_Wiki/` | ✅ | `ls -la` + `wc -l` — 4 archivos, 1223 líneas totales |
| Contenido de `~/arch-setup-backup/` | ✅ | `ls -laR` — 2 configs, 2 pkglists, `restore.sh`, `README.md`, todo con fecha 20-jun |
| Tamaño real de `$HOME` | ✅ | `du -sh /home/eldaniels` → **87 G**; `df -h /home` → 87 G usados de 415 G (23 %) |
| Desglose por directorio | ✅ | `du -sh` ordenado — ver §8 |
| Cifrado del disco raíz | ✅ | `lsblk` — `nvme0n1p2` es `crypto_LUKS` → LVM (`lv_root` 50 G, `lv_swap` 4 G, `lv_home` 422.7 G) |
| Kingston montado | ✅ (negativo) | `lsblk` no lo lista — no estaba conectado durante la sesión |
| **Inventario de fotos/música/media** | 🔴 **NO EJECUTADO** | Comando de inventario interrumpido por el usuario dos veces; nunca corrió |
| Unificación de los 4 archivos | 🟡 analizado, no ejecutado | Solapamientos identificados leyendo los 4 archivos; ningún archivo modificado |
| Rediseño del plan | 🔴 no iniciado | Se identificaron 5 huecos; no se escribió nada |

**Lo que NO quedó resuelto:**
- No se sabe dónde están las fotos ni la música. eldaniels: *"Cubot, tenochtitlan, fibonacci…
  sinceramente no estoy completamente seguro. No recuerdo bien."*
- No se unificó ningún archivo.
- No se escribió ni una línea del plan nuevo.
- No se verificó el contenido real del Kingston (no estaba conectado).
- No se sabe si el contenedor VeraCrypt `xochimilco.vc` sigue siendo legible.

---

## 3 · Archivos tocados — con ruta verificada

**Ninguno, en lo relativo a backups.** La sesión fue análisis y lectura. `git status --porcelain`
al cerrar no muestra ningún archivo de `P8_Backup_Wiki/` modificado.

Archivos **leídos** (rutas verificadas con `ls -la` y `wc -l`):

| Ruta | Líneas | Rol |
|---|---|---|
| `P8_Backup_Wiki/P8_Backup_Seguridad_Digital_Maestro.md` | 905 | Plan maestro, FASE 0–3 |
| `P8_Backup_Wiki/Archivos_Criticos_Inventory.md` | 86 | Inventario USB + configs Arch + spec del bundle |
| `P8_Backup_Wiki/Timeline_Fases.md` | 37 | Checklists por fase |
| `P8_Backup_Wiki/mft_recovery_decision.md` | 195 | Registro de incidente (corrupción MFT) |

**Cambios fuera del repo:** ninguno relacionado con backups.

> **Contexto, fuera de alcance de este handoff:** la primera mitad de la sesión reescribió el comando
> `refresh` y documentó hallazgos de sudo/HDMI. Ese trabajo está **cerrado y commiteado**
> (`4133e69 docs(P2): refresh en dos tiers + hallazgos sudo/HDMI`), documentado en
> `proyectos/P2/COSMIC_setup_custom.md` §9.1–§9.4. Relevante aquí sólo porque produjo cuatro archivos
> nuevos fuera del repo que hay que incorporar al bundle de restauración — ver §8.

---

## 4 · Evaluado y descartado

| Opción / intento | Veredicto | Razón |
|---|---|---|
| Unificar los 4 archivos de `P8_Backup_Wiki/` en uno | 🔶 3 sí, 1 no | `Timeline_Fases.md` y `Archivos_Criticos_Inventory.md` duplican secciones del maestro → fusionar. `mft_recovery_decision.md` es registro de incidente, otro género, y está citado desde `COSMIC_setup_custom.md` §9.1 → separado |
| Nube cifrada del lado cliente (restic / borg) | ❌ descartado | eldaniels eligió disco físico. Coherente con sus siete principios: sin terceros, sin pago recurrente |
| Capa doble (disco off-site + nube para lo crítico) | ❌ descartado | misma razón |
| VeraCrypt como capa de cifrado | ⚠️ señalado, sin decidir | Se eligió en 2026-03 por compatibilidad con Windows 11. La migración a Arch ya ocurrió y el disco raíz es LUKS. VeraCrypt es hoy una pieza móvil extra. **Decisión pendiente** |
| Correr el inventario de media en `fibonacci` | ⚠️ bloqueado | Comando rechazado por el usuario dos veces. Nunca se ejecutó |

**Suposiciones que resultaron falsas:**
- Se asumió que las fotos y la música estaban localizadas. No lo están: repartidas entre Cubot,
  tenochtitlan y fibonacci, sin certeza.
- Se asumió que `$HOME` (87 G) era el volumen a respaldar. Falso: **~77 G son regenerables**
  (`.local` 50 G de modelos Ollama, `.cache` 23 G, gestores de paquetes ~5.8 G). Lo irreemplazable
  ronda **~7 GB**, lo que cambia por completo la viabilidad del diseño.

---

## 5 · Decisiones tomadas

- [x] **Unificar 3 de 4 archivos** de `P8_Backup_Wiki/` — *porque* `Timeline_Fases.md` y
      `Archivos_Criticos_Inventory.md` duplican contenido del maestro y ya divergieron entre sí.
- [x] **`mft_recovery_decision.md` se queda aparte** — *porque* es un registro de incidente, no
      procedimiento, y hay una referencia cruzada viva desde `COSMIC_setup_custom.md` §9.1.
- [x] **Off-site = segundo disco físico (HDD_B), sin nube** — *porque* eldaniels descarta terceros;
      es la FASE 3 original del plan.
- [x] **Inventario antes que diseño** — *porque* no se puede respaldar lo que no se sabe dónde está.
      Invierte el orden que traía la sesión.
- [ ] **Abierta: ¿VeraCrypt o LUKS para los discos externos?** Falta decidir si se migra
      `xochimilco.vc` a LUKS o se conserva por compatibilidad con Windows.
- [ ] **Abierta: ¿qué se respalda?** ¿Sólo lo irreemplazable (~7 GB) o `$HOME` completo (87 G)?
      Afecta el tamaño de HDD_A/HDD_B y la frecuencia viable.

**Punto ciego `[!]`:** el perfil declara *"diseña sistemas antes de validar factibilidad"*. Aquí
apareció una variante distinta y peor: **el sistema está diseñado en detalle (905 líneas, 3 fases,
checklists) pero la ejecución se detuvo en la fase 1 hace 5 meses.** El documento da sensación de
cobertura que la realidad no respalda. Un plan de backups no ejecutado protege exactamente cero
bytes. La sesión reprodujo el mismo sesgo al empezar a rediseñar antes de saber dónde están los datos.

---

## 6 · Siguientes pasos

1. [ ] **Correr el inventario de media en `fibonacci`.** Ejecutable sin leer nada más:
   ```bash
   cd ~ && for spec in "fotos:jpg jpeg png heic cr2 nef dng" "audio:mp3 flac wav m4a" "video:mp4 mov mkv"; do
     label=${spec%%:*}; exts=${spec#*:}
     args=(); for e in $exts; do args+=(-iname "*.$e" -o); done; unset 'args[${#args[@]}-1]'
     find . -path ./.cache -prune -o -path ./.local -prune -o -type f \( "${args[@]}" \) -printf '%s\n' 2>/dev/null \
       | awk -v l="$label" '{n++; b+=$1} END {printf "%-8s %6d archivos  %s\n", l, n, (b/1024/1024/1024)" GB"}'
   done
   ```
2. [ ] **Conectar el Kingston e inventariar su contenido.** Verificar además que `xochimilco.vc`
   sigue montando y que el hash baseline `K:\hash_baseline_2026-04-01.csv` sigue cuadrando.
3. [ ] **Inventariar el Cubot** (fotos y música del celular). Sin eSIM, conexión por USB-C.
4. [ ] Con los tres inventarios: decidir **qué se respalda** (§5, decisión abierta).
5. [ ] Escribir el archivo unificado en `P8_Backup_Wiki/` con las 4 capas:
   qué respaldar → dónde vive → **cómo restaurar (en español, paso a paso)** → estado por fase.
6. [ ] Refrescar `~/arch-setup-backup/` — lleva 2 meses congelado y le faltan los 4 archivos nuevos
   del comando `refresh` (§8).
7. [ ] Resolver `~/.ssh` y credenciales: excluidos a propósito desde marzo con nota *"manejo aparte"*
   que nunca se ejecutó. Son justo lo que restaura el **acceso** a todo lo demás.
8. [ ] Comprar HDD_A (FASE 2) y HDD_B (FASE 3), cifrar con LUKS, `rsync`, y automatizar.
9. [ ] **Probar una restauración real** en hardware distinto o en VM. Sin esto, nada de lo anterior
   está verificado.

**Bloqueadores:**
- Paso 1 depende de que eldaniels autorice el comando (rechazado dos veces en esta sesión).
- Pasos 4–5 dependen de los tres inventarios.
- Paso 8 depende de presupuesto (FASE 2 tiene trigger explícito: *"presupuesto + Linux migrado"*;
  Linux ya está migrado, falta presupuesto).

**Riesgo mayor:** el paso 2. Si el contenedor VeraCrypt de abril no monta o el Kingston falló en
silencio, **la única copia existente ya está perdida** y nadie se ha enterado en 5 meses. Probar eso
antes de invertir en HDD_A y HDD_B — si el medio actual falló, el diseño de replicación cambia.

---

## 7 · Regla de oro para quien retome esto

1. **No escribir una línea del plan nuevo hasta tener los tres inventarios** (fibonacci, Kingston,
   Cubot). El error de esta sesión fue empezar a rediseñar sin saber dónde están los datos.
2. **Verificar primero que el backup actual sigue vivo** (paso 2). Puede llevar 5 meses muerto.
3. Lo irreemplazable son **~7 GB, no 87 G** — `.local` y `.cache` son basura regenerable. Eso hace
   viable cifrar y replicar seguido.
4. El objetivo declarado es *restaurar como si nada hubiera pasado*: sin `~/.ssh` ni credenciales
   respaldadas, eso no se cumple aunque los datos estén completos.

---

## 8 · Datos duros a preservar

```
=== $HOME — 2026-08-28 ===
df -h /home   → /dev/mapper/vg0-lv_home  415G total  87G usados  308G libres  23%
du -sh ~      → 87G

Desglose (du -sh, ordenado):
  50G   .local          ← modelos Ollama etc. — RE-DESCARGABLE
  23G   .cache          ← REGENERABLE
  3.7G  .npm            ← REINSTALABLE
  2.3G  .config         ← RESPALDAR
  1.9G  Codes           ← RESPALDAR
  924M  .nvm            ← reinstalable
  840M  .vscode-oss
  817M  .thunderbird    ← RESPALDAR (correo local)
  765M  .mozilla        ← RESPALDAR (perfiles, marcadores)
  574M  .nuget          ← reinstalable
  490M  .bun            ← reinstalable
  459M  .claude         ← RESPALDAR
  296M  Documents       ← RESPALDAR
  212M  markitdown
  141M  .claude-mem     ← RESPALDAR (memoria de sesiones)
  123M  .cargo          ← reinstalable
  73M   tools
  35M   Downloads

Irreemplazable estimado: ~6.5–7 GB
Regenerable/reinstalable:  ~77 GB

=== Layout de disco (lsblk) ===
nvme0n1                476.9G
├─nvme0n1p1              260M  vfat  LABEL=SYSTEM  /boot
└─nvme0n1p2            476.7G  crypto_LUKS
  └─cryptlvm           476.7G  LVM2_member
    ├─vg0-lv_root         50G  ext4   /
    ├─vg0-lv_swap          4G  swap   [SWAP]
    └─vg0-lv_home      422.7G  ext4   /home
Kingston (tenochtitlan): NO conectado durante la sesión.

=== ~/arch-setup-backup/ — congelado 2026-06-20 ===
restore.sh                                   2375 B  (ejecutable)
README.md                                    1524 B
pkglist-official.txt                          928 B  (pacman -Qqe)
pkglist-aur.txt                               943 B  (pacman -Qqm)
configs/wireplumber/51-bose-no-suspend.conf   543 B
configs/udev/99-bose-usb-no-autosuspend.rules 851 B
→ 2 configs en total. Nada de dotfiles, zsh, COSMIC, .gitconfig, ni ssh.

=== P8_Backup_Wiki/ ===
P8_Backup_Seguridad_Digital_Maestro.md  905 líneas  (FASE 0–3)
mft_recovery_decision.md                195 líneas  (incidente MFT)
Archivos_Criticos_Inventory.md           86 líneas
Timeline_Fases.md                        37 líneas
TOTAL                                  1223 líneas

=== Estado de fases (Timeline_Fases.md) ===
FASE 0  completada 2026-03-31
FASE 1  completada salvo 1 ítem: "Desmontar Z:\ en VeraCrypt antes de desconectar tenochtitlan"
        - xochimilco.vc creado: 200 GB, exFAT
        - hash baseline: K:\hash_baseline_2026-04-01.csv
        - K:\VeraCrypt_Linux_Montaje.txt
FASE 2  NO iniciada (trigger: presupuesto + Linux migrado — Linux ya migrado)
FASE 3  NO iniciada (trigger: completar FASE 2)

=== FALTAN en el bundle: archivos nuevos del comando refresh (2026-08-28) ===
~/.zshrc                                     (función refresh, reemplazó al alias)
~/.local/bin/refresh-system                  0755 usuario
/usr/local/bin/refresh-system-privileged     0755 root:root
/usr/local/bin/refresh-system-privileged-hard 0755 root:root
/etc/sudoers.d/refresh-system                0440
Documentados en proyectos/P2/COSMIC_setup_custom.md §9.4

=== Respuestas de eldaniels (2026-08-28) ===
Ubicación Kingston: "En casa, pero separado/guardado"
Fotos/música:       "Cubot, tenochtitlan, fibonacci... sinceramente no estoy
                     completamente seguro. No recuerdo bien"
Off-site:           "Segundo disco físico" — nube descartada
```

---

## 9 · Destino sugerido

**Doc canónico:** `P8_Backup_Wiki/` — fusionar `Timeline_Fases.md` + `Archivos_Criticos_Inventory.md`
dentro de `P8_Backup_Seguridad_Digital_Maestro.md` (o renombrarlo, p. ej.
`P8_Plan_Backup_Restauracion.md`). Conservar `mft_recovery_decision.md` aparte.

**Actualiza `perfil_maestro`:** no por ahora. Si se compran HDD_A/HDD_B, actualizar §04 Hardware —
ya están listados como *"FASE 2 (futuro)"* y *"FASE 3 (futuro)"*.

**Código a extraer:** el generador/refrescador del bundle merece ser un script versionado
(`.claude/scripts/` o `~/.local/bin/`), no un procedimiento manual. Es la causa directa de que el
bundle lleve 2 meses congelado.

**Insight cross-lens (P8 × P2 × P6):** el patrón de fallo aquí es idéntico al que se arregló hoy
mismo en el comando `refresh` — un procedimiento manual documentado se desactualiza; uno
automatizado no. `refresh-system` dejó de ser manual y por eso se mantiene vivo. El bundle de backup
sigue siendo manual y por eso murió en junio. **La automatización no es optimización: es la única
forma de que el backup exista cuando haga falta.**
