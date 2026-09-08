# 08-09-26 — Rescate Carta Blanca completado + runbook backup + limpieza Gaby

**Fecha de corte:** 2026-09-08 · **Herramienta:** OpenCode (deepseek-v4-flash)
**Lente(s):** P8 (backup/seguridad) × P2 (desarrollo/scripts)
**Estado global:** 🟡 — backup Gaby cerrado ✅; runbook creado ✅ pero scripts sin validar en
dispositivo real; swap de SO en Acer + migración = pendientes para próxima sesión.

> **Continuación 2026-09-08 (misma sesión, desagüe del proyecto):** investigación del sustituto
> FreeCell ejecutada (3 IAs) → **decisión Aisleriot**; stats de Carta Blanca diferidas a
> validación en dispositivo. Detalle en §5 y §6.

---

## 1 · Objetivo y motivación

**Objetivo:** cerrar el rescate del backup de la laptop "rojita" (Acer Aspire One D270, Win7) y
dejar infraestructura reutilizable para respaldar/auditar cualquier dispositivo en el futuro.

**Motivación:** los datos de Gaby (71.55 GB, incluida la historia de 2092 partidas de Carta
Blanca) son irremplazables; el rescate quedó a medias si no se extrae la lección a un
procedimiento repetible antes de formatear la Acer.

| Driver | Detalle |
|---|---|
| Preservar stats Carta Blanca | objetivo vital del proyecto — resuelto esta sesión |
| No repetir el proceso a mano | runbook P2 con scripts inline |
| Dejar backup limpio para Gaby | organizar sin borrar datos únicos |
| Próximo hito | swap SO Acer + migración fibonacci → rojita |

---

## 2 · Estado real verificado al cerrar

| Componente | Estado | Verificado cómo |
|---|---|---|
| Stats Carta Blanca extraídos | ✅ | XML UTF-16LE parseado con `iconv`; coincide con captura |
| `.gamestats` copiados | ✅ | `find` (4 archivos, 1,066–3,320 B) en `00_METADATA/gameexplorer/` |
| Backup Gaby completo | ✅ | 18,019 únicos / 60G + cuarentena 4,104 / 7.6G; FALTA=0 vs 71.55G |
| Limpieza (18 sueltos → Reciente/) | ✅ | `mv` ×18, conteo 18,019 antes=después, 0 borrados |
| Runbook P2 creado | ✅ | `backup_cualquier_dispositivo_runbook.md` escrito |
| Scripts .bat/.ps1 inline | 🟡 | diseñados, **NO probados en Windows real** |
| Handoff | ✅ | este archivo |

**Lo que NO quedó resuelto:** del rescate Gaby, nada. Pendiente completo: swap de SO Acer (MX
32-bit XFCE), migración `~/Documents/backupGABY` → rojita, dejar fibonacci limpio. La
investigación del sustituto FreeCell (prompt IA) **sí se ejecutó** el 2026-09-08 → decisión
Aisleriot (ver §5).

---

## 3 · Archivos tocados — con ruta verificada

**Fuera del repo** (la mayor parte del trabajo vivo):

| Ruta | Acción |
|---|---|
| `~/Documents/backupGABY/00_METADATA/gameexplorer/` | creado — fetch GameExplorer desde Acer |
| `~/Documents/backupGABY/00_METADATA/carta_blanca_stats.md` | creado — stats + GUIDs |
| `~/Documents/backupGABY/00_METADATA/carta_blanca_estado.md` | creado + editado |
| `~/Documents/backupGABY/00_METADATA/LEEME_primero.md` | modificado (checklist + Carta Blanca) |
| `~/Documents/backupGABY/RESPALDO-MGCS/Reciente/` | +18 archivos (los sueltos de la raíz) |
| `~/Documents/backupGABY/RESPALDO-MGCS/` (raíz) | limpiada: 0 archivos sueltos (18,001 en 17 carpetas) |
| `/tmp/hkcu.reg` | efímero (reg HKCU convertido), borrable |
| USB `/dev/sda1` `/run/media/eldaniels/KINGSTON` | aún con `GameExplorer/` + `gaby_HKCU.reg` + logs (redundante) |

**En el repo (mi-criterio):**

| Ruta | Acción |
|---|---|
| `proyectos/P2/backup_cualquier_dispositivo_runbook.md` | **creado** esta sesión |
| `inbox/08-09-26_handoff_respaldo-gaby-runbook.md` | **creado** esta sesión (este) |
| `_index.md` | pendiente de actualizar (tabla P2) |
| `inbox/06-09-26_auditoria_y_respaldo_laptopMadre.sh` | untracked de sesión previa, superseded por el runbook |

**Cambios fuera del repo (sistema):** ninguno en fibonacci. En la Acer (sesiones previas): nada
nuevo esta sesión.

---

## 4 · Evaluado y descartado

| Opción / intento | Veredicto | Razón |
|---|---|---|
| Buscar stats de Carta Blanca en el registro (.reg) | ❌ descartado | medido: solo `GameStats\{GUID}\LastPlayed`; sin Played/Won/Streak en todo el hive |
| `.gamestats` como OLE/binary | ❌ suposición falsa | es **XML UTF-16LE** (`fffe 3c00 3f00 7800`) |
| "Borrar duplicados por path más corto" | ❌ descartado | same-name ≠ same-content medido: ARM.jpg 150 KB vs 8.5 KB, Saludo al sol 35 vs 42 KB — borraría únicos |
| Dedupe por nombre | ❌ descartado | mismo motivo |
| Re-dedup czkawka | ❌ no necesario | 18,019 ya únicos por hash (cuarentena 4,104 = true dups) |
| Robocopy en Acer (batch 1) | ✅ adoptado | funcionó; gotcha: no `/DCOPY` en XP027 |
| Heurística RAM→distro del script `.sh` (≥2GB→Mint XFCE) | ❌ descartado | refutado: Atom 32-bit, Mint sin 32-bit → se eligió MX Linux 32-bit XFCE (decision-record en runbook §2.5) |
| DMDE / testdisk / ntfsfix (histórico) | ❌ descartado | MFT corrupta irrecuperable → instalación limpia (ver mft_recovery_decision.md) |
| Cuarentena de duplicados (czkawka) | ✅ adoptado | keep-newest, reversible; 0 errores |

**Suposiciones falsas:** (1) "los duplicados de Gaby son repeticiones" — son archivos distintos
con el mismo nombre; (2) "las stats de juegos están en el registro" — viven en `.gamestats`;
(3) "`.gamestats` es binario" — es XML.

---

## 5 · Decisiones tomadas

- [x] **Limpieza Gaby = organizar + conservar** — mover los 18 archivos sueltos de la raíz a
  `Reciente/`, NO borrar nada único, cuarentena intacta (reversible). *Porque* el dedup por
  nombre/path borraría archivos distintos (evidencia §4).
- [x] **Scripts inline en el runbook** (bloques de código), sin carpeta `scripts/`. *Porque*
  decisión del usuario; el repo no es un proyecto de software.
- [x] **Runbook cubre Windows + Linux.** *Porque* "cualquier dispositivo" incluye ambos; scripts
  nativos Windows + comandos rsync/find/tree Linux.
- [x] **Regla dura dedup por hash**, nunca por nombre/ruta (documentada en runbook §0).
- [ ] Abierta: `/MIR` vs `/E` por defecto en el script Windows — decidido `/E` (no borrar); `/MIR`
  solo espejo dedicado confirmado.
- [x] **Sustituto FreeCell = Aisleriot** (decisión cerrada 2026-09-08; consulta a 3 IAs —
  ChatGPT/DeepSeek/Gemini — unánime para Acer AOD270 · Atom N2600 · 2 GB · MX 32-bit XFCE):
  FreeCell real (8 columnas, 4 freecells, 4 foundations, undo), **GTK3 nativo de XFCE**, i386 en
  repos Debian, ligero (~15–20 MB RAM). Instalar: `sudo apt install aisleriot` → lanzar `sol`.
  Descartados a conciencia: **PySolFC** (mejor motor de stats pero NO empaquetado en Debian
  Bookworm / MX 23 — solo Bullseye y Trixie+; Python/Tk, arranque lento en Atom; y tampoco
  importa stats de Win7); **KPat** (FreeCell válido pero arrastra stack Qt5/KDE, ~120+ MB RAM —
  injustificable en 2 GB); **XSok** (no es FreeCell — es Sokoban). *Supersede la "opción A
  PySolFC + sembrar stats.dat" registrada en `carta_blanca_stats.md`.*
- [ ] **Stats 2092/1769/84%/73/11: continuidad diferida a validación en dispositivo.** Ningún
  sustituto importa el `.gamestats` de Win7; el backfill manual de Aisleriot es especulativo
  (formato interno no verificado; falsearía rachas). Récord legacy ya preservado en el backup
  (`carta_blanca_stats.md` + `.gamestats` XML original + `gaby_HKCU.reg`). Decidir en el swap si
  se siembra en Aisleriot o se arranca en limpio con el histórico aparte (recomendación).

**Punto ciego `[!]`:** diseñar la herramienta (runbook/scripts) antes de validarla en el
dispositivo real — patrón del perfil "diseñar antes de validar factibilidad". Mitigado con la
nota de estado 🟡 en §1 del runbook; **validar en un USB de prueba** antes de usarlo en producción.

---

## 6 · Siguientes pasos

1. [x] **Sustituto FreeCell** investigado (2026-09-08, 3 IAs) → **Aisleriot** (`sol`). Ver §5.
      *Siguiente en el swap:* validar en el dispositivo real el formato de stats de Aisleriot
      (p. ej. `~/.config/aisleriot/history`) y decidir backfill vs. récord legacy; verificar
      antes: `dpkg --print-architecture` (esperado `i386`) y `apt-cache policy aisleriot`
      (versión real del repo MX). Si el MX instalado resulta Trixie-based (MX-25), PySolFC 3.2.0
      vuelve a estar disponible — pero sigue 2ª opción por peso en el Atom.
2. [ ] Actualizar `_index.md` (tabla P2: añadir `backup_cualquier_dispositivo_runbook.md`).
3. [ ] Commit sugerido: `docs(P2): runbook backup cualquier dispositivo + handoff 08-09-26`
   (usuario ejecuta a mano).
4. [ ] **Swap SO en la Acer**: MX Linux 32-bit XFCE (decisión previa). Preparar USB de arranque.
5. [ ] Migración `~/Documents/backupGABY` (18,019 + 00_METADATA) → rojita.
6. [ ] Dejar fibonacci limpio (decidir qué conservar en `~/Documents`).
7. [ ] Validar scripts del runbook en un USB/SSD de prueba (Windows) antes de dar el runbook por
   bueno.
8. [ ] Decidir destino final de los `.lnk` huérfanos en `Reciente/` (accesos directos viejos a
   OneDrive/cloud — no existen ya; candidatos a limpieza con Gaby).
9. [ ] Actualizar `~/Documents/backupGABY/00_METADATA/carta_blanca_stats.md` §"Integración
   futura": aún dice "opción A = PySolFC + sembrar stats.dat", superseded por la investigación →
   Aisleriot. Corregir para que no engañe a quien configure la Acer en el swap.

**Bloqueadores:** acceso físico a la Acer + USB KINGSTON para el swap y la migración.
**Riesgo mayor:** validar los scripts `.bat`/`.ps1` — probarlos en dispositivo de prueba real
antes de confiar en el runbook; el `.ps1` (PS 2.0 Win7) es el de mayor riesgo de no funcionar tal
cual.

---

## 7 · Regla de oro para quien retome esto

1. **Nunca borres por nombre ni por longitud de ruta**: en este backup same-name ≠ same-content;
   los duplicados verdaderos ya están aislados en `00_METADATA/duplicados/`.
2. **`.gamestats` de Win7 = XML UTF-16LE**, no binario; el registro NO guarda stats de juegos
   (solo `LastPlayed`).
3. En la Acer, al pegar comandos en cmd **se pierde el 1er carácter** (`cho`/`obocopy`) — revisar
   antes de Enter.

---

## 8 · Datos duros a preservar

```
FreeCell (Carta blanca): GUID {A8977498-2FDF-42B7-A726-8D3B2A53CD2C}
Stats (categoría General): 2092 jugados · 1769 ganados · 84% · racha victorias 73 ·
                           racha derrotas 11 · racha actual 1
Otros juegos (GameStatistics): Solitario {768E2DCF-73B0-420A-AA99-4DB04FBC3637} 37/9 máx 1158 ·
  Spider {8669ECE8-D1C3-4345-8310-E60F6D44FDAF} 2 jugados · Buscaminas {89FE5CB3-11CB-489C-AC0D-0C0B6707E1F6} 15 jugados
.rss GUID RSS: {977B5905-4D14-47F1-BBBF-7B92F596695D} · PlayTask Bejeweled3 {b87f2bde-5d44-4e86-bd37-a71616b35ea6}

Backup Gaby: RESPALDO-MGCS 18,019 archivos/60G únicos + cuarentena 4,104/7.6G (czkawka keep-newest)
  Total 72.16G ≥ fuente Acer 71.55G · 17 carpetas temáticas + Reciente (18 sueltos movidos)
gaby_HKCU.reg: 48.5 MB (no contiene stats de juegos)
USB: /dev/sda1 KINGSTON NTFS → /run/media/eldaniels/KINGSTON

Acer: AOD270 · Atom N2600 1.6GHz 2C/4T · 2GB RAM · TOSHIBA 320GB · Win7 Starter 32-bit
  MX Linux 32-bit XFCE elegido · robocopy XP027 sin /DCOPY
Sustituto FreeCell (2026-09-08, 3 IAs unánimes): Aisleriot · `sudo apt install aisleriot` · lanzar `sol`
  Descartados: PySolFC (no en Debian Bookworm/MX23; solo Bullseye + Trixie+), KPat (Qt5/KDE ~120+MB),
  XSok (es Sokoban, no FreeCell). Ninguno importa .gamestats de Win7; stats legacy = carta_blanca_stats.md
Distintos por nombre (NO duplicados): ARM.jpg 150,240 vs 8,583 B · Saludo al sol.jpg 35,880 vs
  42,843 B · Sueñografo3.jpg 116,230 vs 117,968 B · Consultorio.jpg 3 copias distintas
```

---

## 9 · Destino sugerido

**Doc canónico:** `proyectos/P2/backup_cualquier_dispositivo_runbook.md` — ya creado (nuevo).
Estrategia sigue en `P8_Backup_Wiki/P8_Backup_Seguridad_Digital_Maestro.md` (no fusionar; el
runbook es operativo, el wiki es estrategia).
**Actualiza `perfil_maestro`:** señalar — nueva competencia recurrente "backup/auditoría
multi-dispositivo Windows+Linux + rescate de datos" (hardware/proyectos en desarrollo activo).
No editar en process-inbox; solo señalizar.
**Código a extraer:** los scripts del runbook podrían pasar a `~/Codes/` como proyecto si se
validan y crece la demanda.
**Insight cross-lens:** P8 (estrategia/seguridad) → P2 (ejecución) — el runbook es el puente; el
rescate de Gaby es ahora un caso de estudio con medidas reales (72.16G, FALTA=0) citable.
