# Runbook: Backup y auditoría de cualquier dispositivo

**Propósito:** procedimiento único y probado para respaldar y auditar contenido en cualquier
dispositivo — USB, SSD, M.2, laptop, PC — tanto Windows como Linux. Creado tras el rescate del
backup de la laptop "rojita" (Acer, 2026-09) y destilado de la estrategia en
`P8_Backup_Wiki/`. **Canónico P2.** Scripts inline: copiar los bloques a archivos propios.

> Este runbook es **operativo** (cómo). La **filosofía/estado** vive en
> `P8_Backup_Wiki/P8_Backup_Seguridad_Digital_Maestro.md` y los incidentes que lo moldearon en
> `P8_Backup_Wiki/freeze_i915_fsck_incidente.md` y `P8_Backup_Wiki/mft_recovery_decision.md`.

---

## 0 · Principios (lecciones destiladas, no negociables)

1. **La verificación es parte de la copia.** Una copia sin verificar no es un respaldo.
   "Un respaldo sin restaurar es una hipótesis, no un hecho."
2. **Verificar-no-asumir.** Ante cualquier anomalía, confirmar con el comando exacto antes de
   actuar. Nunca reportar como funcionando algo que no se ejecutó.
3. **El contenido manda, no el nombre.** Dos archivos con el mismo nombre pueden ser distintos
   (verificado en el backup de Gaby: `ARM.jpg` 150 KB vs 8.5 KB). Deduplicar SIEMPRE por hash de
   contenido, NUNCA por nombre ni por longitud de ruta.
4. **Nunca borrar en el destino por defecto.** Sin `/MIR` (robocopy) ni `--delete` (rsync) salvo
   espejo dedicado y confirmado — un espejo mal apuntado destruye la única copia.
5. **Idempotencia.** Correr la copia dos veces debe dar una segunda pasada limpia (0 cambios).
   Esa segunda pasada en modo simulación es la verificación de completitud.
6. **Fuentes del sistema: montar de solo-lectura.** Nunca escribir sobre el disco de origen
   mientras se respalda.
7. **Cortes de energía corrompen.** Un apagado brusco + `fsck` puede borrar archivos recientes
   (inodo huérfano — el symlink `claude` se perdió así). Freeze → **REISUB** (R-E-I-S-U-B), no
   botón de encendido.
8. **Discos NTFS de sistema: no `ntfsfix` ni particionar desde Linux entre operaciones.** MFT
   corrupta ≈ pérdida del índice. Operar desde Windows (`chkdsk`), y al hacer dual boot: shrink
   desde Windows primero, nunca `ntfsresize`.
9. **Los metadatos de Windows viven en archivos, no solo en el registro.** (Stats de juegos =
   `.gamestats` XML; el registro solo guarda `LastPlayed`.) Exportar registro HKCU + AppData.

---

## 1 · Procedimiento WINDOWS

> **Estado de los scripts (honesto):** v1 diseñada 2026-09-08 desde la experiencia del rescate
> rojita (robocopy verificado en la Acer). **Pendiente de validación** en dispositivo Windows real
> — en particular el `.ps1` de auditoría (compatible PS 2.0 de Win7 por diseño, no probado).
> Validar en un USB de prueba antes de dar el procedimiento por bueno.

### 1.1 Preparación
1. Conectar el dispositivo destino (USB/SSD), preferentemente formateado NTFS.
2. Anotar su **etiqueta** (ej. `KINGSTON`) — la usará el script.
3. Anotar la ruta **origen** exacta (ej. `C:\Users\gaby\Documents`).
4. Si el origen es un disco de sistema encendido, ideal: arrancar a un sistema distinto y montar
   la partición NTFS de solo-lectura; si es la propia máquina en uso, aceptar que algunos
   archivos (en uso/abiertos) pueden quedar fuera — ver 1.4.

### 1.2 Script de backup — `backup_dispositivo.bat`
Guardar como `backup_dispositivo.bat`. Doble clic o desde cmd. **No borra nada del destino** por
defecto (`/E`, no `/MIR`); deja copia adicional con fecha. Hace copia + pasada de verificación.

```bat
@echo off
setlocal EnableExtensions
chcp 65001 >nul
title backup_dispositivo.bat - copia verificada (robocopy)
echo ==================================================================
echo  backup_dispositivo.bat  —  copia verificada con robocopy
echo ==================================================================

set "SRC=%~1"
if "%SRC%"=="" set /p SRC="Origen a respaldar (ej C:\Users\gaby\Documents): "
if not exist "%SRC%\"  (echo [ERROR] Origen no existe: %SRC% & exit /b 1)

set "ETIQUETA=%~2"
if "%ETIQUETA%"=="" set /p ETIQUETA="Etiqueta del USB/SSD destino (ej KINGSTON): "

REM ---- detectar letra del volumen por etiqueta ----
set "DEST="
for /f "delims=" %%d in ('wmic logicaldisk where "VolumeName='%ETIQUETA%'" get deviceid ^| findstr ":"') do set "DEST=%%d"
if not defined DEST (echo [ERROR] No se encontro volumen con etiqueta "%ETIQUETA%". & exit /b 1)

REM ---- carpeta destino con fecha y host ----
for /f %%t in ('wmic os get localdatetime ^| findstr /b "[0-9]"') do set DT=%%t
set "DST=%DEST%\Respaldo_%COMPUTERNAME%_%DT:~6,4%%DT:~4,2%%DT:~6,2%_%DT:~8,2%%DT:~10,2%"
mkdir "%DST%" 2>nul

echo  Origen : %SRC%
echo  Destino: %DST%
echo.
echo [1/2] Copiando...  (no borra nada en destino)
robocopy "%SRC%" "%DST%" /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ /MT:16 /NP /LOG:"%DST%\00_robocopy_copia.log"
set "RC1=%ERRORLEVEL%"
if %RC1% GEQ 8 (echo [ERROR] La copia fallo. Revisar el log. & exit /b %RC1%)
echo   Copia OK (codigo robocopy %RC1%: 0-7 = exito).

echo [2/2] Verificando...  (segunda pasada en simulacion: debe dar 0 pendientes)
robocopy "%SRC%" "%DST%" /L /E /COPY:DAT /R:0 /W:0 /XJ /NP /LOG:"%DST%\00_robocopy_verif.log"
set "RC2=%ERRORLEVEL%"
if %RC2% EQU 0 (
  echo   VERIFICACION OK: destino identico al origen.
) else (
  if %RC2% EQU 1 (echo   [ATENCION] Hay %_ archivos que se volverian a copiar: revisar 00_robocopy_verif.log)
  else (echo   [ATENCION] Diferencias detectadas (codigo %RC2%). Revisar 00_robocopy_verif.log)
)

REM ---- manifiesto ----
echo %DATE% %TIME%  RC1=%RC1% RC2=%RC2%  SRC=%SRC%  DST=%DST% > "%DST%\00_manifesto.txt"
echo ==================================================================
echo  FIN. Logs y manifiesto en: %DST%
echo   00_robocopy_copia.log   00_robocopy_verif.log   00_manifesto.txt
echo ==================================================================
endlocal
```

**Cómo leer los códigos robocopy:** `<8` éxito · `1` = copiados · `2` = extras en destino ·
`4` = no coinciden · `8` = fallos. En la pasada de verificación `/L` no copia nada: `0` =
idéntico (ideal), `1` = re-copiaría algo (revisar), `8+` = problema.

> **Nota sobre `/MIR`:** solo usar si el destino es un **espejo dedicado** de esa fuente y se
> acepta que borre lo que no esté en origen (caso "replicar a disco clon de respaldo"). Reemplazar
> ambos `/E` por `/MIR` **solo** en ese caso. Por defecto: nunca.

### 1.3 Auditoría en árbol — `auditoria_arbol.ps1` + lanzador `.bat`
Dos archivos. El `.bat` solo lanza PowerShell con política bypass (doble clic). Salida: árbol
`arbol.txt` (nombre + tamaño legible, total por carpeta) + `arbol.csv` + resumen.

`auditoria_arbol.bat`:
```bat
@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0auditoria_arbol.ps1" %*
```

`auditoria_arbol.ps1` (compatible PowerShell 2.0, Win7):
```powershell
param(
  [string]$Ruta  = ".",
  [string]$Salida = ""
)
$ErrorActionPreference = "Stop"
if ($Ruta -eq ".") { $Ruta = (Get-Location).Path }
if ($Salida -eq "") { $Salida = Join-Path (Get-Location).Path "arbol_$((Get-Date).ToString('yyyyMMdd_HHmmss')).txt" }
$csv = $Salida -replace '\.txt$', '.csv'

function Tam-Legible([double]$b) {
  if ($b -ge 1TB) { return "{0,8:N2} TB" -f ($b/1TB) }
  if ($b -ge 1GB) { return "{0,8:N2} GB" -f ($b/1GB) }
  if ($b -ge 1MB) { return "{0,8:N2} MB" -f ($b/1MB) }
  if ($b -ge 1KB) { return "{0,8:N2} KB" -f ($b/1KB) }
  return "{0,8} B " -f $b
}

$totalArchivos = 0
$totalBytes   = [long]0
$lineas = New-Object System.Collections.ArrayList

function Recorre($dir, $nivel) {
  $indent = "  " * $nivel
  $subBytes = [long]0; $subArch = 0
  $dirs = Get-ChildItem -LiteralPath $dir -Directory -Force -ErrorAction SilentlyContinue
  $files = Get-ChildItem -LiteralPath $dir -File -Force -ErrorAction SilentlyContinue
  foreach ($f in $files) { $subBytes += $f.Length; $subArch++ }
  foreach ($d in $dirs)  {
    $r = Recorre $d.FullName ($nivel+1)
    $subBytes += $r[0]; $subArch += $r[1]
    [void]$lineas.Add(("{0}{1}  [{2} archivos]" -f $indent, $d.Name, $r[1]))
  }
  [void]$lineas.Add(("{0}{1}\  ({2} archivos, {3})" -f $indent, (Split-Path $dir -Leaf), $subArch, (Tam-Legible $subBytes)))
  return ,@($subBytes, $subArch)
}

$raiz = (Split-Path $Ruta -Leaf)
if ([string]::IsNullOrEmpty($raiz)) { $raiz = $Ruta }
[void]$lineas.Add("ARBOL DE: $Ruta")
[void]$lineas.Add("")

$enc = @()
$todos = Get-ChildItem -LiteralPath $Ruta -Recurse -Force -ErrorAction SilentlyContinue
foreach ($x in $todos) {
  if (-not $x.PSIsContainer) {
    $totalArchivos++; $totalBytes += $x.Length
    $rel = $x.FullName.Substring($Ruta.Length).TrimStart('\','/')
    $enc += [pscustomobject]@{ RutaRelativa=$rel; Bytes=$x.Length; Tamano=(Tam-Legible $x.Length) }
  }
}
$r = Recorre $Ruta 0

[void]$lineas.Add("")
[void]$lineas.Add(("TOTAL: {0} archivos  {1}  ({2} bytes)" -f $totalArchivos, (Tam-Legible $totalBytes), $totalBytes))
$lineas | Out-File -FilePath $Salida -Encoding UTF8
$enc | Export-Csv -Path $csv -NoTypeInformation -Encoding UTF8
Write-Host "Listo: $Salida"
Write-Host "CSV : $csv"
Write-Host "TOTAL: $totalArchivos archivos  $(Tam-Legible $totalBytes)"
```

Uso: `auditoria_arbol.bat "E:\"` → árbol con tamaños, total por carpeta, total global, y CSV con
todo archivo (ruta relativa + bytes). Funciona sobre cualquier unidad montada en Windows.

### 1.4 Excepciones típicas
- **Archivos en uso** (Outlook, bases de datos, `ntuser.dat`): robocopy `/R:1 /W:1` reintenta 1 vez
  y sigue; quedan marcados en el log como `ERROR 32`. Verificar en `00_robocopy_copia.log`.
- **Metadatos de juegos / AppData** (stats FreeCell, Solitario): vivir en
  `%LOCALAPPDATA%\Microsoft\Windows\GameExplorer\GameStatistics\{GUID}\*.gamestats` (XML UTF-16LE,
  NO binario; el registro NO los guarda). Para respaldo total de un perfil Windows, además:
  `reg export HKCU "%DST%\00_registro_HKCU.reg"` (48 MB típico en perfil con historia).
- **robocopy de Windows 7 (XP027)**: no soporta `/DCOPY`; quitarlo de la línea.
  Gotcha de cmd: al pegar comandos largos se puede perder el 1er carácter (`cho`/`obocopy`).

---

## 2 · Procedimiento LINUX

### 2.1 Preparación
1. Conectar destino y verificar montaje: `lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT,MODEL`.
2. Si el origen es partición NTFS de un Windows apagado: montar de **solo-lectura**:
   `sudo mount -o ro /dev/sdXN /mnt/windows`.
   (Auto-detección opcional de la partición NTFS: `lsblk -no NAME,FSTYPE | awk '$2=="ntfs"{print "/dev/"$1}' | head -1`.)
3. Anotar rutas origen/destino absolutas.

### 2.2 Copia verificada (rsync)
```bash
SRC="/mnt/windows/Users/gaby/Documents"     # origen
DST="/run/media/eldaniels/KINGSTON/Respaldo" # destino (adaptar)
LOGS="$DST/00_logs"; mkdir -p "$LOGS"

# [1/2] copia: archivo (a), checksum (c), enlaces, permisos; NUNCA --delete por defecto
rsync -ah --checksum --info=progress2 "$SRC"/ "$DST"/ 2>&1 | tee "$LOGS/copia.log"

# [2/2] verificación: segunda pasada en seco debe reportar 0 archivos a transferir
rsync -ah --checksum --dry-run --itemize-changes "$SRC"/ "$DST"/ | tee "$LOGS/verif.log"
echo "ARCHIVOS QUE FALTARIAN: $(grep -c '^>f' "$LOGS/verif.log" || true)"
```
`--dry-run` con 0 líneas `>f` = destino idéntico. Para un **espejo dedicado** (borra lo extra en
destino), añadir `--delete` solo con confirmación explícita.

### 2.3 Auditoría en árbol (Linux)
```bash
# Árbol simple con tamaños por carpeta (total acumulado por directorio)
du -h --max-depth=2 "$DST" | sort -rh | head -40

# Árbol de estructura con nombre (instalar 'tree' si falta: sudo pacman -S tree / apt install tree)
tree -a --dirsfirst -h "$DST" > arbol_estructura.txt

# Inventario plano nombre+bytes (útil como manifiesto)
find "$DST" -type f -printf '%s\t%p\n' | sort -k2 > inventario.txt
wc -l inventario.txt                       # total de archivos
awk -F'\t' '{s+=$1} END {printf "Total: %.2f GiB\n", s/1024/1024/1024}' inventario.txt
```

### 2.4 Herramienta personal específica
Para el respaldo del propio `$HOME` de fibonacci existe `respaldar-fibonacci` (fuera del repo,
no publicable: la lista de rutas es el mapa de dónde están los secretos). Simulación con
`respaldar-fibonacci`, copia real con `--ejecutar`, verificación de manifiesto con `--verificar`.

### 2.5 Procedencia del enfoque (proceso 2026-09, decision-record)
Este procedimiento Linux **no fue el que ejecutó el rescate real de "rojita"**: se redactó un
script automático (`inbox/06-09-26_auditoria_y_respaldo_laptopMadre.sh`, DESCARTADO) pero la
Acer se respaldó con **robocopy manual en 2 batches** (más fiable para un sistema en uso). Del
draft se conserva lo que sigue siendo válido (montaje `ro`, rsync con verificación, inventario) —
aquí destilado. Decisiones del draft que **se descartaron a conciencia** (conservarlas como guía
documentaría una mentira):
- **Heurística RAM→distro refutada:** "≥2 GB → Linux Mint XFCE" era incorrecto para la Acer
  (Atom N2600 32-bit; Mint no publica 32-bit). Elección real: **MX Linux 32-bit XFCE**.
- **Metadatos de juegos vía `find` de directorios refutada:** apuntaba a directorios "Solitaire/
  FreeCell" que no existen así; lo real fue `GameExplorer\GameStatistics\*.gamestats` (ver §1.4).

---

## 3 · Verificación post-backup (siempre)

1. **Conteo de archivos** origen vs destino (debe coincidir, tolerando los "en uso").
2. **Segunda pasada limpia**: robocopy `/L` en Windows / rsync `--dry-run` en Linux → 0 pendientes.
3. **Hash de muestra**: `Get-FileHash` (PS) / `sha256sum` (Linux) sobre archivos clave del destino
   y comparar contra el origen.
4. **Prueba de apertura**: abrir un archivo de cada tipo (foto, doc, pdf) directamente desde el
   destino.
5. **Registrar**: fecha, RC, conteo, bytes en el manifiesto/LEEME dentro del respaldo.

> "Un respaldo sin restaurar es una hipótesis." La verificación real final es restaurar a otro
> medio y abrir.

---

## 4 · Checklist repetible (cualquier dispositivo)

```
[ ] 1. Identificar origen exacto + tipo de medio (USB/SSD/M.2/laptop/PC, SO, FS)
[ ] 2. Montar origen de SOLO-LECTURA si es disco de sistema
[ ] 3. Conectar y verificar destino (etiqueta, espacio libre suficiente)
[ ] 4. Correr copia (script .bat / rsync) -> leer log completo, no solo el final
[ ] 5. Correr segunda pasada de verificación -> 0 pendientes
[ ] 6. Auditar en árbol el DESTINO (sorprende: revela lo que no esperabas)
[ ] 7. Deduplicar por HASH de contenido si hace falta (nunca por nombre/ruta)
[ ] 8. Registrar manifiesto + LEEME dentro del respaldo
[ ] 9. Probar apertura de archivos de muestra desde el destino
[ ] 10. Etiquetar físicamente el medio (contenido + fecha)
```

---

## 5 · Referencias cruzadas

| Archivo | Rol |
|---|---|
| `P8_Backup_Wiki/P8_Backup_Seguridad_Digital_Maestro.md` | estrategia/estado global, fases HDD_A/B, respaldar-fibonacci |
| `P8_Backup_Wiki/freeze_i915_fsck_incidente.md` | REISUB, inodos huérfanos, metodología diag "command not found" |
| `P8_Backup_Wiki/mft_recovery_decision.md` | MFT, shrink desde Windows, no ntfsfix entre operaciones |
| `inbox/06-09-26_auditoria_y_respaldo_laptopMadre.sh` | draft Linux del rescate rojita — DESCARTADO (criterio → §2.5/§2; ver decision-record) |
| `~/Documents/backupGABY/` | ejemplo real aplicado: 18,019 archivos, verificación FALTA=0, Carta Blanca rescatada |
| `P8_Backup_Wiki` maestría cruzada con `proyectos/P2/COSMIC_setup_custom.md` §9 | referencia interna backup/restore Arch |
```
